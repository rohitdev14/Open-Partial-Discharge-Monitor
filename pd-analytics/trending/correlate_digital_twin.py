"""Step 1C cross-project correlation.

Joins operational-digital-twin telemetry to PD event evidence by shared run_id
and asset mapping, then associates each PD event with the nearest operational
telemetry sample in UTC time.

Synthetic development data only. No defect diagnosis and no calibrated pC.
"""
from datetime import datetime
from typing import Iterable

def _utc(s):
    return datetime.fromisoformat(s.replace("Z","+00:00"))

def correlate(pd_events: Iterable[dict], pd_metadata: dict,
              twin_rows: Iterable[dict], max_delta_s: float = 1.0):
    run_id=pd_metadata["run_id"]
    pump_asset=pd_metadata["pump_asset_id"]
    pd_start=_utc(pd_metadata["timestamp_utc"])
    sample_rate=float(pd_metadata["sample_rate_hz"])

    twin=[r for r in twin_rows
          if r.get("run_id")==run_id and r.get("asset_id")==pump_asset]
    twin.sort(key=lambda r:_utc(r["timestamp_utc"]))
    joined=[]
    for event in pd_events:
        event_time=pd_start.timestamp()+float(event["sample_index"])/sample_rate
        if not twin:
            continue
        nearest=min(twin,key=lambda r:abs(_utc(r["timestamp_utc"]).timestamp()-event_time))
        delta=abs(_utc(nearest["timestamp_utc"]).timestamp()-event_time)
        if delta <= max_delta_s:
            joined.append({
                "run_id":run_id,
                "pd_asset_id":pd_metadata["asset_id"],
                "pump_asset_id":pump_asset,
                "pd_event_time_utc":datetime.fromtimestamp(event_time, pd_start.tzinfo).isoformat().replace("+00:00","Z"),
                "phase_deg":event["phase_deg"],
                "pd_amplitude":event["amplitude"],
                "twin_timestamp_utc":nearest["timestamp_utc"],
                "correlation_delta_s":round(delta,6),
                "scenario":nearest.get("scenario"),
                "status":nearest.get("status"),
                "common_speed_ref_pu":nearest.get("common_speed_ref_pu"),
                "pump_flow_m3h":nearest.get("pump_flow_m3h"),
                "electrical_input_power_kw":nearest.get("electrical_input_power_kw"),
            })
    return joined
