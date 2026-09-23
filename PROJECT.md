# Partial Discharge Monitoring System --- PROJECT.md

**Status:** Steps 1A–1C software baseline validated and frozen; Step 1D physical HFCT/DAQ bench validation next\
**Deployment model:** On-premises\
**Implementation gates:** Step 1 --- local PC POC; Step 2 --- fixed
field acquisition integrated to SCADA through OPC UA\
**Repository rule:** No GitHub push, pull-request merge, or repository
implementation without explicit project-owner approval.

------------------------------------------------------------------------

## Current Build Status

| Stage | Scope | Status |
|---|---|---|
| Step 1A | Architecture, repository baseline and electrical SLD | Complete |
| Step 1B | Deterministic synthetic HFCT waveform, pulse detection, phase association and PRPD evidence | Validated |
| Step 1C | M-101 PD evidence synchronized with P-101 operational Digital Twin telemetry | **Validated / frozen** |
| Step 1D | Physical HFCT / high-speed DAQ bench acquisition and validation | Next |

### Step 1C frozen validation baseline

GitHub Actions run #3 at PD repository commit `a76c30d871e7cc61f575e41f00c33663a8d2f055` successfully executed the synchronized experiment `DT-PD-STEP1C-001`.

The run produced 16 detected synthetic PD events and correlated all 16 to the appropriate P-101 Digital Twin operating context. Maximum timestamp correlation delta was 0.034712 s. The healthy capture produced no detected events; the precursor and post-trip captures each produced and correlated eight events. CI also validated the evidence files and uploaded `step1c-synchronized-evidence`.

This gate validates the cross-project data contract and synchronization architecture. It does not validate a physical HFCT/DAQ chain, calibrated apparent charge in pC, defect classification, or a causal relationship between the Digital Twin failure scenario and synthetic PD activity.

The Step 1C software baseline is now frozen. The next engineering gate is Step 1D: physical HFCT/DAQ bench validation.

------------------------------------------------------------------------

## 1. Project Goal

Develop a home-grown, practical and scalable Partial Discharge (PD)
measurement and monitoring platform using commercially purchased sensors
and hardware.

The project will not initially attempt to manufacture PD sensors. The
engineering value will be created in the acquisition architecture,
signal processing, phase-resolved analysis, local data platform,
visualization, diagnostics, integration and future scalability.

The first implementation will validate the complete measurement chain on
a controlled, limited asset such as an MV cable/termination. After
validation, the architecture will be converted into fixed field nodes
and integrated with SCADA through OPC UA.

The engineering progression is:

**Detect → characterize → phase-resolve → trend → validate → integrate →
scale**

The initial platform is a PD detection/trending system. Apparent charge
in pC shall not be reported as a calibrated measurement until the
measurement chain and calibration method have been independently
validated.

------------------------------------------------------------------------

## 2. Scope

### Step 1 --- Local PC Proof of Concept

Step 1 shall prove that a commercially available fixed/clamp-on PD
sensor can be connected to a high-speed acquisition system and that
locally developed software can:

-   acquire raw high-frequency waveforms;
-   identify impulsive activity above the established noise floor;
-   timestamp and store measurement events;
-   derive pulse amplitude and pulse-rate features;
-   acquire an isolated 50 Hz phase reference;
-   associate pulses with electrical phase;
-   generate Phase Resolved Partial Discharge (PRPD) information;
-   trend PD activity over time;
-   display sensor status, waveforms, PRPD and trends on a local
    dashboard;
-   preserve raw data for later algorithm development and validation;
-   support comparison of two sensors where required.

The first preferred asset is an accessible cable/termination earth
conductor suitable for an HFCT.

### Step 2 --- Fixed Field System + SCADA

After Step 1 validation, the platform shall evolve to permanent field
acquisition:

-   fixed HFCT/TEV/other suitable PD sensors;
-   multi-channel field acquisition nodes;
-   industrial edge gateway;
-   Ethernet/IP network;
-   centralized on-prem PD server;
-   local storage and analytics;
-   OPC UA server interface;
-   SCADA visualization and alarm integration;
-   scalable asset/sensor/channel hierarchy.

SCADA shall receive processed operational information. High-rate raw PD
waveform data shall remain in the PD platform rather than being
continuously transported into SCADA.

### Out of Scope for Initial POC

-   manufacturing a proprietary PD sensor;
-   automatic control or tripping of electrical equipment;
-   claiming IEC 60270 apparent-charge values without
    calibration/validation;
-   cloud dependency;
-   AI/ML defect classification before sufficient labelled real data
    exists;
-   permanent SCADA integration during Step 1.

------------------------------------------------------------------------

## 3. Overall Architecture

``` text
                         PARTIAL DISCHARGE PLATFORM

 STEP 1 — POC
 ──────────────────────────────────────────────────────────────────────

     Cable / Termination
             │
             │ earth conductor
             ▼
          HFCT-01 ──────────────┐
                                │
          HFCT-02 ──────────────┤
                                ▼
                       Input protection /
                       conditioning
                                │
                                ▼
                    High-Speed 4-Ch DAQ
                       │      │      │
                       │      │      └── CH-C: isolated 50 Hz phase
                       │      └───────── CH-B: HFCT-02
                       └──────────────── CH-A: HFCT-01
                                │
                             USB 3
                                │
                                ▼
                         LOCAL POC PC
                    ┌─────────────────────┐
                    │ Acquisition service │
                    │ Signal processing   │
                    │ Pulse detection     │
                    │ Phase correlation   │
                    │ PRPD generation     │
                    │ Event/trend storage │
                    │ FastAPI             │
                    │ Local dashboard     │
                    └─────────────────────┘


 STEP 2 — FIELD / SCALE
 ──────────────────────────────────────────────────────────────────────

 HFCT / TEV / future PD sensors
              │
              ▼
      Fixed acquisition node
      ┌─────────────────────┐
      │ Multi-channel ADC   │
      │ Local filtering     │
      │ Pulse/event capture │
      │ Health diagnostics  │
      └──────────┬──────────┘
                 │
                 ▼
        Industrial Edge Gateway
                 │
              Ethernet
                 │
                 ▼
        CENTRAL ON-PREM PD SERVER
      ┌───────────────────────────┐
      │ Asset/sensor registry     │
      │ Event + waveform storage  │
      │ PRPD + trend analytics    │
      │ Alarm/severity engine     │
      │ Web UI                    │
      │ OPC UA server             │
      └────────────┬──────────────┘
                   │ OPC UA
                   ▼
                 SCADA
```

------------------------------------------------------------------------


## 3A. Open-Source and Containerization Architecture

The public repository shall be structured as a reusable product rather than a one-off laboratory script.

**Target user experience:**

```text
git clone <public-repository>
configure .env + hardware profile
docker compose --profile simulator up
            OR
docker compose --profile hardware up
```

### Deployment Profiles

**Simulator profile**  
Runs without physical PD hardware. It shall generate representative phase reference, background noise and synthetic PD-like events so that contributors can exercise the full processing, database, API and dashboard pipeline.

**Hardware profile**  
Enables one or more supported DAQ drivers and passes acquired data into the same standard processing pipeline used by the simulator.

**SCADA profile / Step 2 extension**  
Adds the OPC UA service and the production-oriented asset hierarchy, alarms and integration services.

### Containerized Service Model

```text
                         DOCKERIZED PD PLATFORM

                ┌─────────────────────────────┐
DAQ / Simulator ─► acquisition-service       │
                │             │               │
                │             ▼               │
                │ signal-processing-service  │
                │             │               │
                │             ▼               │
                │ pd-analytics / PRPD         │
                │             │               │
                │      ┌──────┴───────┐       │
                │      ▼              ▼       │
                │   database       backend    │
                │                     │       │
                │                     ▼       │
                │                  frontend   │
                │                     │       │
                │              opcua-service │
                └─────────────────────┼───────┘
                                      │
                                    SCADA
```

The exact service boundaries may be consolidated during implementation if separate containers create unnecessary operational complexity, but the interfaces shall remain modular.

### Hardware Abstraction Layer

No core analytics code shall depend directly on one DAQ vendor.

```text
                    Acquisition Interface
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
       PicoScope driver  Future DAQ   Simulator
              │            │            │
              └────────────┼────────────┘
                           ▼
                  Standard acquisition
                  record / waveform
```

DAQ-specific code belongs in a driver/adaptor layer. The first supported physical driver may target the selected POC DAQ, but future contributors shall be able to add alternatives without changing the PD analytics layer.

Sensor characteristics shall likewise be configuration-driven rather than hard-coded.

Example:

```yaml
sensor:
  id: HFCT-001
  type: HFCT
  manufacturer: TBD
  model: TBD
  output_impedance_ohm: 50
  frequency_min_hz: TBD
  frequency_max_hz: TBD
  transfer_impedance: TBD
  calibration_file: null
```

### USB / DAQ Container Boundary

USB DAQs may require vendor drivers or host-level device access. The architecture shall therefore support a clean boundary between the host and acquisition service. Where a vendor SDK cannot run reliably inside a container, a thin host acquisition adapter may be used, but all downstream platform services shall remain containerized. This exception must be documented per supported DAQ.

### Proposed Public Repository Structure

```text
open-pd-monitor/
├── README.md
├── PROJECT.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── docker-compose.yml
├── .env.example
├── acquisition/
│   ├── drivers/
│   │   ├── simulator/
│   │   └── picoscope/
│   └── service/
├── signal-processing/
│   ├── filters/
│   ├── pulse_detection/
│   ├── noise_rejection/
│   └── features/
├── pd-analytics/
│   ├── prpd/
│   ├── trending/
│   └── severity/
├── backend/
├── frontend/
├── database/
├── opcua/
├── simulator/
│   ├── noise/
│   ├── synthetic_pd/
│   └── phase_reference/
├── config/
│   ├── sensors/
│   ├── daq/
│   └── assets/
├── tests/
├── docs/
│   ├── architecture/
│   ├── hardware/
│   ├── installation/
│   ├── calibration/
│   ├── scada/
│   └── safety/
└── examples/
```

### Open-Source Governance

The repository shall include:

- an OSI-compatible license selected before the first public software release;
- `CONTRIBUTING.md`;
- `SECURITY.md`;
- documented hardware compatibility;
- versioned configuration examples;
- automated tests that can run against the simulator without physical hardware;
- clear separation between experimental features and validated measurement functionality;
- safety and calibration disclaimers appropriate to electrical PD monitoring.


## 4. Asset and Data Hierarchy

The software shall not assume a single sensor. From the first
implementation the logical model shall support:

``` text
Site
└── Electrical System
    └── Equipment
        └── Measurement Point
            └── Sensor
                └── Channel
                    └── Measurement / Event
```

Example:

``` text
POC-Site
└── MV-System-01
    └── Cable-01
        └── Termination-R
            └── HFCT-001
                └── CH-A
```

This model shall allow future deployment from one sensor to many
distributed measurement points without changing the core data model.

------------------------------------------------------------------------

## 5. Sensor Strategy

The platform shall be sensor-agnostic.

  -----------------------------------------------------------------------
  Asset/Application       Preferred Sensor        Project Stage
  ----------------------- ----------------------- -----------------------
  MV cable / termination  HFCT                    Step 1 priority

  Metal-clad MV           TEV, with HFCT/acoustic Step 2 / subsequent POC
  switchgear              where appropriate       

  Motor feeder / motor    HFCT                    Later

  VFD-fed motor           HFCT with enhanced      Later
                          noise discrimination    

  GIS/GIL                 UHF                     Future
  -----------------------------------------------------------------------

### HFCT-PD-01 Recommended Specification

The initial HFCT shall preferably have:

-   passive split-core construction;
-   suitability for online PD detection;
-   non-invasive clamp-on installation around an appropriate
    earth/ground conductor;
-   50-ohm-compatible coaxial signal chain;
-   BNC/coax output;
-   useful PD bandwidth target approximately 100 kHz to 30 MHz or wider;
-   manufacturer-documented frequency response;
-   manufacturer-documented transfer impedance/sensitivity;
-   aperture sized for the actual conductor, with approximately 30 mm or
    greater used only as an initial planning target;
-   industrial operating temperature;
-   repeatable permanent mounting arrangement;
-   unique serial number;
-   calibration/test documentation preferred.

Two identical HFCTs are recommended for Step 1 to support correlation,
noise experiments and comparison.

------------------------------------------------------------------------

## 6. Step 1 DAQ Specification

### Minimum Requirements

-   4 analog channels preferred;
-   at least 100 MHz analog bandwidth recommended for development;
-   at least 100 MS/s sampling capability;
-   12-bit or better resolution preferred;
-   sufficient onboard capture memory for triggered waveform
    acquisition;
-   external/software triggering;
-   USB 3 or equivalent high-speed PC interface;
-   manufacturer SDK/API;
-   Python-accessible interface preferred;
-   Windows and/or Linux support.

### Reference Development Instrument

**PicoScope 5444D or technically equivalent**

Reference capability:

-   4 analog channels;
-   200 MHz bandwidth;
-   up to 1 GS/s;
-   flexible 8--16 bit resolution;
-   512 MS capture memory;
-   USB 3;
-   programmable SDK.

The selected development DAQ is a laboratory/reference instrument. It is
not intended to be duplicated at every future field measurement point.

### Proposed Channel Allocation

  DAQ Channel   Step 1 Function
  ------------- -----------------------------------------------
  CH-A          HFCT-01 --- primary PD sensor
  CH-B          HFCT-02 --- comparison/noise/reference sensor
  CH-C          isolated 50 Hz phase reference
  CH-D          spare / TEV / experimental channel

------------------------------------------------------------------------

## 7. Phase Reference

A phase reference is mandatory for PRPD development.

Requirements:

-   electrically isolated from the mains/MV measurement system;
-   safe low-voltage signal presented to the DAQ;
-   sufficient fidelity to derive the 50 Hz electrical phase;
-   repeatable mapping of detected PD events to 0--360 degrees;
-   no direct unprotected mains connection to the development DAQ.

Final device selection depends on the auxiliary voltage and safe access
available at the POC location.

------------------------------------------------------------------------

## 8. Input Protection and Signal Conditioning

The initial analog interface shall remain modular.

``` text
HFCT
  │
50 Ω coax
  │
  ▼
┌──────────────────────────┐
│ INPUT MODULE             │
│ - transient protection   │
│ - selectable attenuation │
│ - impedance management   │
│ - optional filtering     │
└────────────┬─────────────┘
             │
             ▼
            DAQ
```

Step 1 should retain as much raw information as practical. Filtering
shall initially be developed in software. An optimized analog front end
can be designed only after real measurements establish the useful signal
and noise bands.

------------------------------------------------------------------------

## 9. Step 1 Software Architecture

Recommended local stack:

-   Python;
-   DAQ vendor SDK/API;
-   NumPy/SciPy for signal processing;
-   FastAPI backend;
-   PostgreSQL, with TimescaleDB considered for time-series scaling;
-   local filesystem/object-style directory for raw waveform captures;
-   web frontend/dashboard;
-   Docker for reproducible local services.

Suggested implementation modules:

``` text
pd-monitor/
├── acquisition/
│   ├── daq_drivers/
│   ├── waveform_capture/
│   └── phase_reference/
├── signal_processing/
│   ├── filters/
│   ├── pulse_detection/
│   ├── noise_rejection/
│   └── feature_extraction/
├── pd_analysis/
│   ├── prpd/
│   ├── trending/
│   └── severity/
├── backend/
├── database/
├── frontend/
├── simulator/
├── tests/
├── docs/
└── docker/
```

This is a proposed project structure only. It shall not be implemented
in GitHub until explicit approval is given.

------------------------------------------------------------------------

## 10. Step 1 BOM / BOQ

### POC Procurement Baseline

  -----------------------------------------------------------------------------------
  Item            Recommended Specification                  Qty  Planning Cost (SGD)
  --------------- ------------------------- -------------------- --------------------
  HFCT PD sensor  Split-core, passive, 50                      2         1,000--3,000
                  Ω/BNC, documented                              
                  response/transfer                              
                  impedance, suitable for                        
                  online cable PD                                

  High-speed DAQ  4 ch, ≥100 MHz                               1         4,000--5,000
                  recommended, ≥100 MS/s,                        
                  ≥12-bit preferred, SDK;                        
                  PicoScope 5444D class                          

  Isolated 50 Hz  Safe isolated LV output                      1             150--400
  phase reference suitable for DAQ                               

  50 Ω coaxial    Shielded BNC-BNC,                            3             100--150
  cable           RG58/RG223 or                                  
                  sensor-approved                                
                  equivalent                                     

  50 Ω BNC        Precision termination                        4               40--80
  terminators                                                    

  BNC attenuators 10 dB / 20 dB selection                      4              80--150

  DAQ input       Replaceable/clamped                       2 ch             100--300
  protection      transient protection                           

  BNC adapter kit T adapters, couplers,                    1 set              50--100
                  male/female adapters                           

  Shielded        Metal enclosure for                          1              80--150
  enclosure       protection/conditioning                        

  Local           ≥4-core CPU, ≥16 GB RAM,                     1             Existing
  development PC  USB 3, GbE                                     

  SSD             1 TB recommended                             1              80--120

  Cat6 Ethernet   Patch cables                                 2                   20

  Test/mounting   BNC leads, labels,                       1 set                  100
  accessories     clamps, mounting hardware                      

  **Estimated     **Planning allowance                             **\~5,800--9,500**
  Step 1 hardware pending vendor RFQs**                          
  envelope**                                                     
  -----------------------------------------------------------------------------------

**Cost note:** HFCT, phase-reference and several accessory values are
planning allowances rather than supplier quotations. A purchase-ready
BOM shall replace these with manufacturer, part number, supplier,
quotation date and actual SGD price before procurement.

------------------------------------------------------------------------

## 11. Step 1 BOQ by Functional Package

### Package A --- Sensing

-   2 × identical HFCT PD sensors;
-   3 × 50 Ω coaxial signal cables;
-   sensor mounting hardware;
-   sensor identification labels.

### Package B --- Acquisition

-   1 × four-channel high-speed development DAQ;
-   1 × isolated phase-reference device;
-   4 × 50 Ω terminators;
-   attenuation set;
-   BNC adapter set;
-   input protection components.

### Package C --- Compute / Storage

-   1 × existing local PC;
-   1 × 1 TB SSD if existing capacity is insufficient;
-   2 × Cat6 patch leads.

### Package D --- Integration / Bench Hardware

-   1 × shielded signal-conditioning enclosure;
-   test leads;
-   mounting hardware;
-   labels and identification.

------------------------------------------------------------------------

## 12. Step 1 Acceptance Criteria

Step 1 shall not be considered complete merely because a waveform is
visible.

Minimum technical acceptance should include:

1.  DAQ communicates reliably with the local PC.
2.  Both HFCT channels can be acquired independently.
3.  Noise floor is characterized and documented.
4.  Raw waveform captures are timestamped and retained.
5.  Repeatable impulsive events can be detected.
6.  Pulse features can be calculated.
7.  A safe isolated 50 Hz phase reference is acquired.
8.  Events can be mapped to electrical phase.
9.  A PRPD visualization is generated.
10. Event/pulse trends are stored.
11. Local dashboard shows sensor health, activity and trends.
12. Known noise/transient behavior is documented.
13. Results are compared with a known/reference PD source or commercial
    measurement where practical.
14. No unvalidated pC value is presented as a calibrated PD measurement.

------------------------------------------------------------------------

## 13. Step 2 Field Architecture Specification

Step 2 converts the POC into a permanent monitoring architecture.

### Field Acquisition Node --- Target Requirements

-   approximately 4 PD sensor channels per node as an initial modular
    target;
-   separate phase-reference capability;
-   simultaneous or appropriately synchronized acquisition;
-   local pulse/event detection;
-   configurable digital filtering;
-   event buffering;
-   local health diagnostics;
-   timestamp synchronization;
-   store-and-forward behavior during network interruption;
-   industrial 24 VDC power;
-   Ethernet;
-   fanless/industrial installation where required;
-   watchdog;
-   remote configuration;
-   DIN-rail/panel mounting where practical;
-   industrial EMC/environmental design appropriate to the installation;
-   communication to central on-prem PD server.

The final field DAQ architecture shall be selected only after Step 1
establishes the bandwidth, dynamic range, sampling rate and processing
requirements from real data.

------------------------------------------------------------------------

## 14. Step 2 On-Prem Server

The central PD server shall provide:

-   equipment/asset hierarchy;
-   sensor registry;
-   channel configuration;
-   measurement/event database;
-   waveform repository;
-   PRPD processing;
-   trend analytics;
-   severity/alarm engine;
-   sensor/edge-node health monitoring;
-   configuration management;
-   local dashboard;
-   OPC UA server;
-   audit/event logs;
-   future analytics/ML interface.

------------------------------------------------------------------------

## 15. OPC UA / SCADA Integration

SCADA shall consume operational PD information rather than high-rate raw
waveforms.

Proposed initial namespace:

``` text
PD.<Site>.<Equipment>.<MeasurementPoint>.<Sensor>.Status
PD.<Site>.<Equipment>.<MeasurementPoint>.<Sensor>.PulseRate
PD.<Site>.<Equipment>.<MeasurementPoint>.<Sensor>.PeakAmplitude
PD.<Site>.<Equipment>.<MeasurementPoint>.<Sensor>.RMSNoise
PD.<Site>.<Equipment>.<MeasurementPoint>.<Sensor>.ActivityIndex
PD.<Site>.<Equipment>.<MeasurementPoint>.<Sensor>.Severity
PD.<Site>.<Equipment>.<MeasurementPoint>.<Sensor>.Trend
PD.<Site>.<Equipment>.<MeasurementPoint>.<Sensor>.Alarm
PD.<Site>.<Equipment>.<MeasurementPoint>.<Sensor>.SensorHealth
PD.<Site>.<Equipment>.<MeasurementPoint>.<Sensor>.LastEvent
```

`ApparentCharge_pC` shall be added only after the system has an accepted
calibration and validation method.

------------------------------------------------------------------------

## 16. Step 2 Preliminary BOQ Model

This is a scaling model, not yet a purchase BOM.

For each four-channel field node:

  Functional Item                         Typical Qty / Node
  ------------------------------------- --------------------
  Fixed PD sensor                                    up to 4
  Multi-channel PD acquisition module                      1
  Phase-reference interface                                1
  Industrial edge gateway                                  1
  24 VDC industrial PSU                                    1
  Industrial enclosure/panel hardware                      1
  Ethernet connection                                      1
  Coax/sensor cables                                 up to 4
  Protection/conditioning channels                   up to 4

Central infrastructure:

  Item                                                              Qty
  ---------------------------------------- ----------------------------
  On-prem PD application/database server                      1 primary
  Storage/backup                                               1 system
  OPC UA service                                               software
  SCADA OPC UA client/integration            existing/new as applicable
  Engineering workstation                                   as required

The field-node BOM and actual per-point scaling cost shall be frozen
only after Step 1 measurements determine the necessary ADC, bandwidth
and edge-compute performance.

------------------------------------------------------------------------

## 17. Implementation Approach

### Gate 0 --- Requirements Freeze

Confirm POC asset, voltage class, cable/termination type, earth
conductor arrangement, sensor aperture, safe installation method,
auxiliary phase-reference source and test duration.

### Gate 1 --- Purchase-Ready BOM

Shortlist actual HFCT, DAQ and phase-reference models. Record
manufacturer, part number, specification, supplier, price, lead time and
alternatives.

### Gate 2 --- Bench Bring-Up

Connect sensor, protection, DAQ and local PC. Verify acquisition without
connection to operational HV equipment.

### Gate 3 --- Acquisition Software

Develop repeatable waveform capture, metadata, configuration and
storage.

### Gate 4 --- Signal Processing

Establish noise floor, filtering, pulse detection and feature
extraction.

### Gate 5 --- Phase-Resolved Analysis

Integrate phase reference and generate PRPD.

### Gate 6 --- POC Validation

Deploy on approved asset under appropriate electrical safety controls
and compare observations with reference/commercial measurements where
practical.

### Gate 7 --- Step 1 Design Freeze

Document sampling requirements, bandwidth, dynamic range, storage rate,
noise behavior, algorithms and limitations.

### Gate 8 --- Step 2 Field Node

Select/design the permanent acquisition node based on measured Step 1
requirements.

### Gate 9 --- OPC UA

Expose approved processed tags through OPC UA and integrate with SCADA.

### Gate 10 --- Scale

Expand to multiple cables/switchgear points and later additional sensor
types.

------------------------------------------------------------------------

## 18. Safety and Engineering Controls

PD monitoring may involve energized MV equipment. The POC architecture
does not itself authorize installation or testing.

-   Sensor installation shall follow site electrical safety procedures.
-   No direct connection from an MV circuit to the development DAQ is
    permitted.
-   Phase reference shall be appropriately isolated.
-   Equipment access, earthing arrangements and sensor installation
    shall be reviewed by competent electrical personnel.
-   DAQ input limits shall be protected and respected.
-   Bench testing shall precede energized field deployment.
-   Automatic trip/control actions are outside the initial scope.
-   The monitoring system shall fail safe and shall not interfere with
    protection systems.

------------------------------------------------------------------------

## 19. Key Design Principles

1.  **Commercial sensors, home-grown platform.**
2.  **On-premises by design.**
3.  **Raw evidence retained.**
4.  **Measurement before AI.**
5.  **Sensor-agnostic architecture.**
6.  **SCADA receives operational information, not raw RF data.**
7.  **Step 1 determines Step 2 hardware requirements.**
8.  **No pC claim without calibration.**
9.  **Scale through modular multi-channel field nodes.**
10. **No GitHub push or PR merge without explicit project-owner
    approval.**

------------------------------------------------------------------------

## 20. Immediate Next Action

Before procurement, complete the **Step 1 Purchase-Ready BOM**.

For each major component, the next selection record shall contain:

-   manufacturer;
-   exact model/part number;
-   measured/claimed bandwidth;
-   transfer impedance or input characteristics;
-   channel count;
-   sampling rate/resolution;
-   interface/API;
-   environmental rating;
-   supplier;
-   Singapore availability;
-   unit price in SGD;
-   lead time;
-   primary choice;
-   alternate choice;
-   reason for selection.

The first three components to freeze are:

1.  **HFCT sensor**
2.  **4-channel high-speed development DAQ**
3.  **isolated 50 Hz phase-reference method**

Only after these are approved should procurement or implementation
begin.