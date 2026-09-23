# Pump Digital Twin — PD Simulation Branch

**Status:** Step 1B simulation baseline  
**Linked project:** rohitdev14/operational-digital-twin  
**Integration key:** asset ID + UTC timestamp

## Purpose

Use the centrifugal-pump operational digital twin as a controlled operating context for developing the Partial Discharge (PD) acquisition and analytics pipeline before purchasing physical HFCT/DAQ hardware.

## Electrical study basis

Conceptual simulation basis only; not a construction design:

- Supply: 400 V AC, 3-phase, 50 Hz.
- Distribution board: MDB-PUMP-01.
- Pumps: P-101 to P-105.
- Motors: M-101 to M-105, 30 kW each.
- VSD reference: Danfoss VLT AQUA Drive FC 202, 30 kW class.
- Alternative VSD reference: Schneider Altivar Process ATV630, 30 kW class.
- DB-to-VSD study cable: Cu XLPE/PVC 0.6/1 kV, 4C x 16 mm2.
- VSD-to-motor study cable: screened VFD cable, 3C + PE x 16 mm2.
- Final cable/protection selection requires engineering calculations and coordination.

## Step 1B measurement branch

Initial simulated measurement point: M-101 feeder / motor cable.

Data path:

Motor/VSD cable -> synthetic HFCT waveform -> acquisition interface -> pulse detection -> phase correlation -> PRPD -> trending.

A separate isolated 50 Hz phase-reference channel supplies the electrical phase used to map detected pulses to 0–360 degrees.

The synthetic electrical-fault case introduces repeatable high-frequency impulses and phase-related clustering so the software pipeline can be developed and tested. It is not calibrated apparent charge in pC and is not a claim that a specific real defect must produce the same PRPD pattern.

## Cross-project time alignment

Both repositories shall use UTC timestamps in ISO 8601 form, for example:

2026-09-23T11:30:15.123456Z

The digital twin and PD simulator should publish records containing at minimum:

- timestamp_utc
- asset_id
- source
- run_id
- operating state / measurement values

Recommended common asset IDs include P-101 and M-101. A single simulation run should use the same run_id in both projects.

This permits later joins such as:

timestamp + M-101 + run_id -> pump/VSD operating state + PD pulse activity + PRPD features

## GitHub traceability

Git commits provide immutable source-history timestamps. Cross-repository documentation should link the relevant commit SHA from each repository. For important synchronized test baselines, create matching release/tag names in both repositories, for example:

dt-pd-integration-v0.1

A reproducibility record should contain both commit SHAs, the run_id, UTC start/end timestamps and configuration versions.

## Boundary

The operational digital twin owns pump/process/control operating context. Open Partial Discharge Monitor owns high-frequency electrical waveform simulation, pulse/PRPD analytics and PD measurement evidence. Integration occurs through timestamped asset/run metadata rather than tightly coupling the two codebases.
