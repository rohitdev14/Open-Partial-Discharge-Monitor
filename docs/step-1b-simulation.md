# Step 1B — Digital-Twin PD Simulation

**Status: VALIDATED — GitHub Actions validation #2 successful after test syntax correction at commit `f53a4c770f858615d9003f8cd7c243181e99f487`.**

Step 1B builds a deterministic synthetic Partial Discharge development branch around the M-101 electrical feeder before physical HFCT/DAQ procurement.

## Pipeline

M-101 synthetic HFCT waveform -> pulse detector -> phase association -> PRPD bins -> timestamped artifacts.

The generator produces 40 ms of waveform by default, equivalent to two cycles at 50 Hz. It injects damped high-frequency pulse trains around selected electrical phase regions solely to exercise the processing pipeline.

## Cross-project contract

Every run carries:

- timestamp_utc
- asset_id = M-101
- pump_asset_id = P-101
- run_id
- source = pd-simulator
- sample rate and mains frequency
- explicit synthetic/not-calibrated measurement status

The matching operational-digital-twin experiment should use the same run_id. UTC timestamp plus persistent asset identity and run_id allow PD evidence to be correlated with pump flow, head, VSD speed and electrical power.

## Outputs

Running simulator/run_step1b.py creates:

- metadata.json
- waveform.csv
- events.csv
- prpd.json

## Engineering boundary

This is synthetic development data. Pulse amplitude is not calibrated apparent charge in pC, and the injected phase pattern must not be interpreted as a validated diagnosis of a real insulation defect. Physical validation follows later with approved sensing/acquisition hardware and appropriate electrical-safety controls.
