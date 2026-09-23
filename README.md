# Open Partial Discharge Monitor

Open-source, Dockerized partial-discharge monitoring platform for commercially available HFCT/TEV sensors, local analytics, PRPD, trending, and OPC UA/SCADA integration.

> **Project status: Steps 1A–1C complete; Step 1C synchronized Digital Twin–PD software integration frozen as the validated baseline. Step 1D physical HFCT/DAQ bench validation is next. Not a certified protection or calibrated PD measurement instrument.**

## Build status

| Stage | Outcome | Status |
|---|---|---|
| Step 1A | Architecture, open-source baseline and electrical SLD | ✅ Complete |
| Step 1B | Deterministic M-101 synthetic HF waveform → pulse detection → phase association → PRPD → evidence artifacts | ✅ Validated |
| Step 1C | Synchronize PD evidence with operational-digital-twin telemetry using UTC + asset identity + run ID | ✅ Validated / frozen |
| Step 1D | Physical HFCT / DAQ acquisition and bench validation | ⏳ Planned |

**Step 1B validation baseline:** fix commit `f53a4c770f858615d9003f8cd7c243181e99f487`; GitHub Actions validation #2 reported successful by the project owner. This validates the software simulation pipeline only, not calibrated pC measurement or real defect diagnosis.

**Step 1C frozen baseline:** GitHub Actions run #3 at commit `a76c30d871e7cc61f575e41f00c33663a8d2f055` completed successfully. Run `DT-PD-STEP1C-001` produced 16 detected/correlated synthetic PD events, with maximum Digital Twin correlation delta 0.034712 s. Healthy capture: 0 events; P-101 precursor window: 8/8 correlated; P-101 post-trip window: 8/8 correlated. The evidence artifact `step1c-synchronized-evidence` was uploaded by CI. This validates synchronization/correlation architecture only; it does not establish physical causation, real defect diagnosis or calibrated apparent charge.

## Mission

Build a practical, hardware-extensible, on-premises Partial Discharge (PD) platform that can grow from a single-sensor local proof of concept into distributed fixed monitoring integrated with industrial SCADA.

The project intentionally separates **commercial sensing/acquisition hardware** from an **open software platform** for acquisition, signal processing, phase-resolved analysis, storage, visualization, diagnostics and integration.

## Two-step roadmap

**Step 1 — Local POC:** HFCT sensor(s) → high-speed DAQ → local PC → Dockerized acquisition/analytics/database/API/dashboard. The goal is waveform acquisition, noise characterization, pulse detection, 50 Hz phase correlation, PRPD and trending.

**Step 2 — Field deployment:** fixed PD sensors → modular acquisition/edge nodes → on-prem PD server → OPC UA → SCADA. The same core software stack is retained and extended rather than replaced.

## Architecture

```text
STEP 1
HFCT(s) ──> High-speed DAQ ──> Acquisition Adapter
                                      │
                                      ▼
                           Dockerized PD Platform
                         ┌────────────────────────┐
                         │ signal processing      │
50 Hz isolated ref ─────>│ PD analytics / PRPD   │
                         │ database + API         │
                         │ dashboard              │
                         └────────────────────────┘

STEP 2
Fixed HFCT/TEV sensors
          │
          ▼
Field acquisition / edge nodes
          │ Ethernet
          ▼
Dockerized on-prem PD platform
          │
        OPC UA
          ▼
         SCADA
```

## Deployment philosophy

The target user experience is:

```bash
git clone <repository>
cp .env.example .env
docker compose --profile simulator up
```

The **simulator profile** will allow development and CI without physical PD hardware. The **hardware profile** will use supported DAQ adapters. A later **SCADA profile** will expose approved operational tags through OPC UA.

The current repository is a baseline: service Dockerfiles and executable application code will be added incrementally after architecture and hardware requirements are validated.

## Hardware abstraction

Core PD analytics must not depend on a single DAQ vendor. Vendor-specific acquisition belongs behind a driver/adapter interface.

Initial planned drivers:

- simulator — first implementation target;
- PicoScope-class DAQ — first physical acquisition target;
- additional DAQs — contributor/extensibility path.

Sensor characteristics will be configuration-driven.

## Repository map

```text
acquisition/        DAQ adapters and acquisition service
signal-processing/  filtering, pulse detection, noise rejection, features
pd-analytics/       PRPD, trending and severity logic
backend/            application API
frontend/           local web UI
database/           schema/migrations
opcua/              Step 2 OPC UA interface
simulator/          synthetic signals, noise and phase reference
config/             sensor, DAQ and asset configuration
tests/              automated tests
docs/               architecture, hardware, installation, calibration, SCADA, safety
examples/           example configurations and workflows
```

See **[PROJECT.md](PROJECT.md)** for the engineering scope, architecture, POC BOM/BOQ, acceptance criteria and Step 2 design.

## Safety

Partial-discharge monitoring may involve energized MV/HV equipment. This repository does **not** authorize electrical work. Installation and testing must follow applicable site procedures, equipment ratings and competent-person requirements.

Do not connect a development DAQ directly to mains or MV/HV circuits. Phase-reference and measurement interfaces must use suitable isolation and protection.

This software must not be used as a protection or automatic-trip system.

## Measurement limitation

Early versions focus on **PD-like pulse detection, phase-resolved analysis and trending**. The project will not report an unvalidated value as calibrated apparent charge in pC. Calibrated measurement requires a documented and validated measurement/calibration chain.

## Contributing

The project is intended to become community-extensible. See [CONTRIBUTING.md](CONTRIBUTING.md). Security and safety-sensitive reports should follow [SECURITY.md](SECURITY.md).

## License

Apache License 2.0. See [LICENSE](LICENSE).