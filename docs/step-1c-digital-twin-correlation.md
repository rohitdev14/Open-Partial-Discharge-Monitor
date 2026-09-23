# Step 1C — Synchronized Digital Twin–PD Experiment

**Status: VALIDATED / FROZEN**

Frozen software-integration baseline: GitHub Actions run #3, commit `a76c30d871e7cc61f575e41f00c33663a8d2f055`, run ID `DT-PD-STEP1C-001`.

Step 1C correlates synthetic PD evidence from M-101 with the operating context of pump package P-101 from the separate operational-digital-twin repository.

## Join contract

A synchronized experiment uses the same `run_id`. PD metadata maps `M-101` to `P-101`; both systems use UTC timestamps. Each PD pulse timestamp is reconstructed from the capture start timestamp plus its sample index / sample rate and is associated with the nearest P-101 operational telemetry sample within a configurable tolerance.

## Initial correlated context

The first implementation carries the Digital Twin scenario, run status, common VSD speed reference, pump flow and electrical input power beside each PD event.

This makes it possible to ask whether synthetic PD-like activity changed with operating context without merging the two repositories or allowing either project to control the other.

## Boundary

Correlation is evidence alignment, not diagnosis. Step 1C does not claim that a PRPD pattern identifies a physical defect, and amplitude remains synthetic/not calibrated pC.


## Validation result

The synchronized CI experiment completed successfully with 16 detected synthetic PD events and 16 correlated events. The maximum timestamp correlation delta was 0.034712 s.

- Healthy capture at 30 s: 0 detected / 0 correlated.
- P-101 precursor capture at 105 s: 8 detected / 8 correlated while P-101 was RUNNING, common speed reference 0.87399 pu, pump flow 100.0 m³/h and electrical input power 14.857 kW.
- P-101 post-trip capture at 125 s: 8 detected / 8 correlated while P-101 was TRIPPED, common speed reference 0.89716 pu, pump flow 0.0 m³/h and electrical input power 0.0 kW.

CI validated the contract tests, synchronized experiment, evidence checks and artifact upload. The frozen evidence artifact is named `step1c-synchronized-evidence`.

## Closure

Step 1C is closed as the validated synthetic synchronization/correlation baseline. Further synthetic work should not expand this gate unless needed to support a discovered defect or the physical acquisition interface. The next project gate is Step 1D physical HFCT/DAQ bench validation.
