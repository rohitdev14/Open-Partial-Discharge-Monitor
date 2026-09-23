# Step 1C — Synchronized Digital Twin–PD Experiment

**Status: IN DEVELOPMENT**

Step 1C correlates synthetic PD evidence from M-101 with the operating context of pump package P-101 from the separate operational-digital-twin repository.

## Join contract

A synchronized experiment uses the same `run_id`. PD metadata maps `M-101` to `P-101`; both systems use UTC timestamps. Each PD pulse timestamp is reconstructed from the capture start timestamp plus its sample index / sample rate and is associated with the nearest P-101 operational telemetry sample within a configurable tolerance.

## Initial correlated context

The first implementation carries the Digital Twin scenario, run status, common VSD speed reference, pump flow and electrical input power beside each PD event.

This makes it possible to ask whether synthetic PD-like activity changed with operating context without merging the two repositories or allowing either project to control the other.

## Boundary

Correlation is evidence alignment, not diagnosis. Step 1C does not claim that a PRPD pattern identifies a physical defect, and amplitude remains synthetic/not calibrated pC.
