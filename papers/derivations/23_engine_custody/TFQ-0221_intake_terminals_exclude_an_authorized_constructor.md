# [TFQ-0221] Intake terminals exclude an authorized constructor

> **Stage**: `ENGINE_CUSTODY` | **Status**: `SOURCE_RECORD`  
> **UUID**: `26327c2c-2091-5b24-a35d-a1692257f58b`  
> **Parent Derivation**: [TFQ-0220](TFQ-0220_prime_002_stops_when_continuation_is_unauthorized.md)

---

## 1. Abstract & Formal Statement

The intake contract keeps an authorized terminal out of the status vocabulary. Python TerminalStatus lists evidence_only, unresolved, refused, and not_admitted. RefusalClass names a failed gate. Lean repeats those four constructors and comments that no constructor is named authorized. The prime book's firewall chapter separates identity and scope while the ceiling stays None. A finished prime cycle therefore lands on evidence, an unresolved mark, a refusal, or a not-admitted mark. The firewall records that landing and does not mint a stronger effect.

### Governing Obligation
Land a finished prime cycle on evidence, unresolved, refused, or not-admitted.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`omega_engine_atlas/coda_atlas/F003_omega_engine/S000_prime_algorithms_and_runtime/000_omega_engine_prime_algorithms_and_runtime/lean4/OmegaEnginePrimeAlgorithmsRuntime/IntakeContract.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_pipelines/src/runtime.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F003_omega_engine/S000_prime_algorithms_and_runtime/000_omega_engine_prime_algorithms_and_runtime/python/src/omega_engine_rc/intake_status.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0222](TFQ-0222_a_finite_receipt_records_local_checks_only.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F003.S000:000_omega_engine_prime_algorithms_and_runtime`, `F003.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F003_omega_engine/S000_prime_algorithms_and_runtime/000_omega_engine_prime_algorithms_and_runtime`
  - `omega_engine_atlas/coda_atlas/F003_omega_engine/S000_prime_algorithms_and_runtime`
