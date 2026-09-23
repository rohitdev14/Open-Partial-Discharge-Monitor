# Container Architecture

Step 1 and Step 2 use the same core software platform.

- Simulator and physical DAQ drivers produce a standard acquisition record.
- Signal processing and PD analytics remain independent of DAQ vendor.
- Raw/high-rate waveform data remains in the PD platform.
- SCADA receives approved processed operational tags through OPC UA.
- The simulator is the basis for automated tests and contributor onboarding.

Executable containers are intentionally not included in the architecture-only baseline; implementation follows after the initial repository baseline is reviewed and approved.
