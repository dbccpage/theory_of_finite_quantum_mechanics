# PLAN-7D-PREFLIGHT

Goal id: PLAN-7D-PREFLIGHT

AuthorityEffect: None.

## Selected scope

Dependency, path, and controller-guard preflight for the staged PFP runner `omega_engine_education/scripts/run_staged_demos.py` and the canonical PFP controller `omega_engine_pfp/application/services/pfp_run_controller.py`:

1. **Runner path and dependency preflight:** `omega_engine_education/scripts/run_staged_demos.py` resolves inside the repository, `jsonschema` imports cleanly (remediating the historical `--help` probe failure), and `run_staged_demos.py --help` exits with code `0`.
2. **Legacy live-dispatch refusal (`LEGACY_LIVE_REQUIRES_CANONICAL_PFP`):** Calling `run_staged_demos.main(["--pilot", "1", "--live"])` without `--i-accept-unbounded-legacy-live-spend` returns exit code `2` and refuses unguarded legacy live dispatch in favor of the canonical `omega_engine_pfp` controller.
3. **Canonical controller reservation and unknown-cost collation:** `omega_engine_pfp/application/services/pfp_run_controller.py` is importable and enforces fail-closed budget reservation where unknown-cost provider outcomes retain their reserved budget rather than releasing it.

## Claims this note does not make

- Preflighting dependencies, paths, and controller guards does not execute paid live provider trials or certify empirical model performance.
