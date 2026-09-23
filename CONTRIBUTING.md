# Contributing

Thank you for helping build Open Partial Discharge Monitor.

## Principles

- Keep the core analytics hardware-agnostic.
- Add DAQ-specific behavior through acquisition drivers/adapters.
- Preserve raw evidence and provenance where practical.
- Do not present unvalidated outputs as calibrated apparent charge.
- Keep simulator mode functional so contributors can test without physical hardware.
- Add tests for new processing behavior.
- Treat electrical safety changes as safety-sensitive.

## Proposed workflow

1. Open an issue describing the change.
2. Create a focused branch.
3. Add implementation and tests.
4. Update documentation/configuration examples.
5. Open a pull request describing assumptions, validation and limitations.

Hardware drivers should document vendor SDK/driver prerequisites, supported host OS, container/device-access requirements and tested hardware.