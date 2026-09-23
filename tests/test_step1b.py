from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"simulator"))
sys.path.insert(0,str(ROOT/"simulator"/"synthetic_pd"))
sys.path.insert(0,str(ROOT/"signal-processing"/"pulse_detection"))
sys.path.insert(0,str(ROOT/"pd-analytics"/"prpd"))
from synthetic_pd.generate import generate, SimulationConfig
from detect import detect_pulses
from build import build_prpd

def test_step1b_is_deterministic_and_phase_resolved():
    cfg=SimulationConfig(seed=7)
    a=generate(cfg,start_utc=__import__("datetime").datetime(2026,9,23,tzinfo=__import__("datetime").timezone.utc)
    b=generate(cfg,start_utc=__import__("datetime").datetime(2026,9,23,tzinfo=__import__("datetime").timezone.utc)
    assert a["waveform"]==b["waveform"]
    events=detect_pulses(a["waveform"],a["phase_deg"])
    assert events
    assert all(0 <= e["phase_deg"] < 360 for e in events)
    assert build_prpd(events)

def test_healthy_case_has_no_injected_events():
    data=generate(fault=False)
    assert data["injected_events"]==[]

def test_metadata_contract():
    data=generate(run_id="DT-PD-TEST-001",asset_id="M-101")
    m=data["metadata"]
    assert m["asset_id"]=="M-101"
    assert m["pump_asset_id"]=="P-101"
    assert m["run_id"]=="DT-PD-TEST-001"
    assert m["source"]=="pd-simulator"
    assert m["timestamp_utc"].endswith("Z")
    assert m["measurement_status"]=="synthetic_not_calibrated_pc"
