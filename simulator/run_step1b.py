"""Run the Step 1B M-101 synthetic PD experiment."""
import csv
import json
from pathlib import Path
from synthetic_pd.generate import generate
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"signal-processing"/"pulse_detection"))
sys.path.insert(0,str(ROOT/"pd-analytics"/"prpd"))
from detect import detect_pulses
from build import build_prpd

def run(output_dir="artifacts/step1b"):
    data=generate()
    events=detect_pulses(data["waveform"],data["phase_deg"])
    prpd=build_prpd(events)
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    (out/"metadata.json").write_text(json.dumps(data["metadata"],indent=2))
    with (out/"waveform.csv").open("w",newline="") as f:
        w=csv.writer(f); w.writerow(["sample_index","amplitude","phase_deg"])
        w.writerows((i,data["waveform"][i],data["phase_deg"][i]) for i in range(len(data["waveform"])))
    with (out/"events.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["sample_index","amplitude","phase_deg"]); w.writeheader(); w.writerows(events)
    (out/"prpd.json").write_text(json.dumps(prpd,indent=2))
    return data["metadata"],events,prpd

if __name__=="__main__":
    metadata,events,prpd=run()
    print(metadata); print(f"detected_events={len(events)} prpd_bins={len(prpd)}")
