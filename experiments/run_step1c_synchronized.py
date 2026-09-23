"""Full Step 1C synchronized Operational Digital Twin ↔ PD experiment."""
import argparse, csv, json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

def load_module_paths(pd_root,twin_root):
    sys.path.insert(0,str(pd_root/"simulator"))
    sys.path.insert(0,str(pd_root/"simulator"/"synthetic_pd"))
    sys.path.insert(0,str(pd_root/"signal-processing"/"pulse_detection"))
    sys.path.insert(0,str(pd_root/"pd-analytics"/"trending"))
    sys.path.insert(0,str(twin_root))

def git_sha(root):
    return subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()

def run(pd_root,twin_root,output):
    load_module_paths(pd_root,twin_root)
    from synthetic_pd.generate import generate, SimulationConfig
    from detect import detect_pulses
    from correlate_digital_twin import correlate
    from model.failure_simulation import simulate_failures

    run_id="DT-PD-STEP1C-001"
    start=datetime(2026,9,24,0,0,0,tzinfo=timezone.utc)

    # Generate the full 480 s twin experiment. PD captures are taken in three
    # operating windows to prove that evidence can be aligned to changing context.
    twin=simulate_failures(duration_s=480,run_id=run_id,start_utc=start)
    captures=[("healthy",30),("p101_precursor",105),("p101_tripped",125)]
    correlated=[]
    capture_summary=[]

    for label,offset_s in captures:
        capture_start=datetime.fromtimestamp(start.timestamp()+offset_s,tz=timezone.utc)
        data=generate(SimulationConfig(seed=7+offset_s),run_id=run_id,
                      asset_id="M-101",start_utc=capture_start,fault=(label!="healthy"))
        events=detect_pulses(data["waveform"],data["phase_deg"])
        joined=correlate(events,data["metadata"],twin,max_delta_s=1.0)
        for row in joined:
            row["capture_label"]=label
        correlated.extend(joined)
        capture_summary.append({"label":label,"offset_s":offset_s,
                                "detected_events":len(events),"correlated_events":len(joined)})

    output.mkdir(parents=True,exist_ok=True)
    fields=["capture_label","run_id","pd_asset_id","pump_asset_id","pd_event_time_utc",
            "phase_deg","pd_amplitude","twin_timestamp_utc","correlation_delta_s",
            "scenario","status","common_speed_ref_pu","pump_flow_m3h","electrical_input_power_kw"]
    with (output/"correlated_events.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(correlated)

    contexts=sorted({(r["capture_label"],r["scenario"],r["status"],
                      r["common_speed_ref_pu"],r["pump_flow_m3h"],r["electrical_input_power_kw"])
                     for r in correlated})
    summary={
        "run_id":run_id,
        "correlated_event_count":len(correlated),
        "max_correlation_delta_s":max((r["correlation_delta_s"] for r in correlated),default=None),
        "captures":capture_summary,
        "operating_contexts":[{"capture_label":x[0],"scenario":x[1],"status":x[2],
                               "common_speed_ref_pu":x[3],"pump_flow_m3h":x[4],
                               "electrical_input_power_kw":x[5]} for x in contexts],
        "interpretation_boundary":"Synthetic correlation evidence only; not defect diagnosis or calibrated pC."
    }
    (output/"summary.json").write_text(json.dumps(summary,indent=2))
    manifest={
        "run_id":run_id,"started_at_utc":start.isoformat().replace("+00:00","Z"),
        "pd_asset_id":"M-101","pump_asset_id":"P-101",
        "pd_repo":"rohitdev14/Open-Partial-Discharge-Monitor","pd_commit":git_sha(pd_root),
        "digital_twin_repo":"rohitdev14/operational-digital-twin","digital_twin_commit":git_sha(twin_root),
        "schema_version":"1.0","capture_windows_s":[x[1] for x in captures]
    }
    (output/"experiment_manifest.json").write_text(json.dumps(manifest,indent=2))
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    a=argparse.ArgumentParser()
    a.add_argument("--pd-root",type=Path,required=True)
    a.add_argument("--twin-root",type=Path,required=True)
    a.add_argument("--output",type=Path,required=True)
    args=a.parse_args(); run(args.pd_root.resolve(),args.twin_root.resolve(),args.output.resolve())
