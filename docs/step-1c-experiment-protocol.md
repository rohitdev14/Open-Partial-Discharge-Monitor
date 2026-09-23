# Step 1C synchronized experiment protocol

The full experiment runs the 480-second deterministic Operational Digital Twin scenario with shared run ID `DT-PD-STEP1C-001` and UTC epoch `2026-09-24T00:00:00Z`.

Three M-101 PD capture windows are aligned to P-101 operating context:

| Capture | Twin offset | Intended context |
|---|---:|---|
| healthy | 30 s | P-101 running in S0_HEALTHY |
| p101_precursor | 105 s | P-101 running during the synthetic bearing-degradation precursor window |
| p101_tripped | 125 s | P-101 tripped in S1_P101_BEARING_VSD_TRIP |

The experiment records each correlated PD event beside the nearest Digital Twin timestamp, scenario, P-101 status, common VSD speed reference, pump flow and electrical input power. A manifest records both repository commit SHAs.

The healthy capture deliberately has no injected PD-like fault. The later captures use synthetic PD-like impulses to exercise correlation. This does not assert that bearing degradation causes PD or that the generated PRPD pattern represents a real bearing defect. The two synthetic evidence streams are co-timed solely to validate the integration architecture.

Successful CI requires Step 1C tests, non-empty synchronized evidence, matching run/asset IDs, correlation tolerance no greater than 1 second, and uploaded experiment artifacts.
