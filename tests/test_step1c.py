from datetime import datetime, timezone
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"pd-analytics"/"trending"))
from correlate_digital_twin import correlate

def test_step1c_correlates_pd_event_to_matching_twin_run():
    metadata={"timestamp_utc":"2026-09-24T00:00:00.000000Z","asset_id":"M-101",
              "pump_asset_id":"P-101","run_id":"DT-PD-STEP1C-001","sample_rate_hz":1_000_000}
    events=[{"sample_index":20000,"amplitude":21.5,"phase_deg":72.0}]
    twin=[{"timestamp_utc":"2026-09-24T00:00:00.000000Z","run_id":"DT-PD-STEP1C-001",
           "asset_id":"P-101","scenario":"S0_HEALTHY","status":"RUNNING",
           "common_speed_ref_pu":0.874,"pump_flow_m3h":100.0,"electrical_input_power_kw":18.2}]
    joined=correlate(events,metadata,twin)
    assert len(joined)==1
    assert joined[0]["pd_asset_id"]=="M-101"
    assert joined[0]["pump_asset_id"]=="P-101"
    assert joined[0]["scenario"]=="S0_HEALTHY"
    assert joined[0]["correlation_delta_s"]==0.02

def test_step1c_rejects_wrong_run_id():
    metadata={"timestamp_utc":"2026-09-24T00:00:00Z","asset_id":"M-101",
              "pump_asset_id":"P-101","run_id":"RUN-A","sample_rate_hz":1_000_000}
    events=[{"sample_index":0,"amplitude":10,"phase_deg":60}]
    twin=[{"timestamp_utc":"2026-09-24T00:00:00Z","run_id":"RUN-B","asset_id":"P-101"}]
    assert correlate(events,metadata,twin)==[]
