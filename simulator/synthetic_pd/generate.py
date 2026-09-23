"""Deterministic Step 1B synthetic HF waveform generator.

Development data only. Amplitude is arbitrary mV-like simulation output and is
NOT calibrated apparent charge (pC).
"""
from dataclasses import dataclass
from datetime import datetime, timezone
import math
import random

@dataclass(frozen=True)
class SimulationConfig:
    sample_rate_hz: int = 1_000_000
    duration_ms: float = 40.0
    mains_frequency_hz: float = 50.0
    noise_rms: float = 1.2
    pulse_frequency_hz: float = 120_000.0
    pulse_decay_samples: float = 22.0
    seed: int = 7

def _angle_distance(a, b):
    return abs((a-b+180.0)%360.0-180.0)

def generate(config=SimulationConfig(), run_id="DT-PD-STEP1B-001",
             asset_id="M-101", start_utc=None, fault=True):
    rng=random.Random(config.seed)
    n=int(config.sample_rate_hz*config.duration_ms/1000.0)
    start_utc=start_utc or datetime.now(timezone.utc)
    waveform=[rng.gauss(0.0,config.noise_rms) for _ in range(n)]
    phases=[((i/config.sample_rate_hz)*config.mains_frequency_hz*360.0)%360.0 for i in range(n)]

    injected=[]
    if fault:
        # Synthetic phase-related clusters for pipeline testing only.
        for center in (70.0,85.0,250.0,265.0):
            candidates=[i for i,p in enumerate(phases) if _angle_distance(p,center)<0.7]
            if not candidates: continue
            stride=max(1,len(candidates)//3)
            for i in candidates[::stride][:3]:
                amp=rng.uniform(14.0,32.0)*rng.choice((-1.0,1.0))
                for k in range(min(120,n-i)):
                    waveform[i+k]+=amp*math.exp(-k/config.pulse_decay_samples)*math.sin(
                        2.0*math.pi*config.pulse_frequency_hz*k/config.sample_rate_hz)
                injected.append({"sample_index":i,"phase_deg":round(phases[i],3),
                                 "injected_peak_scale":round(amp,3)})

    return {
        "metadata":{
            "timestamp_utc":start_utc.isoformat().replace("+00:00","Z"),
            "asset_id":asset_id,"pump_asset_id":"P-101","run_id":run_id,
            "source":"pd-simulator","sample_rate_hz":config.sample_rate_hz,
            "mains_frequency_hz":config.mains_frequency_hz,
            "measurement_status":"synthetic_not_calibrated_pc",
            "fault_injected":fault,"seed":config.seed},
        "waveform":waveform,"phase_deg":phases,"injected_events":injected}

if __name__=="__main__":
    x=generate()
    print(x["metadata"])
    print(f'samples={len(x["waveform"])} injected_events={len(x["injected_events"])}')
