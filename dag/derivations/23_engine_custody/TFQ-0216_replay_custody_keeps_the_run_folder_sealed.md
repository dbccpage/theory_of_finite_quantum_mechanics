# [TFQ-0216] Replay custody keeps the run folder sealed

> **Stage**: `ENGINE_CUSTODY` | **Status**: `SOURCE_RECORD`  
> **UUID**: `d158438e-20e1-50e7-96d4-e086cf2c1dc7`  
> **Parent Derivation**: [TFQ-0215](TFQ-0215_finite_quantum_shelf_is_a_custody_binding.md)

---

## 1. Abstract & Formal Statement

Replay custody means a later reader can reopen the bytes the runtime accepted. omega_replay exports run-folder sealing and AUTHORITY_EFFECT_NONE, and run_folder.rs rejects a receipt whose authority effect is not that constant. ReplayHash and the append log sit beside the seal so a trace can be named without being rewritten in place. The authorization book adds ReplayFiber, which hashes proposal bytes, and its docstring says the helper is not certification or authorization. Prime issue_finite_receipt builds a digest from the local packet checks. Custody keeps the sealed folder, the hash, and the None marker.

### Governing Obligation
Seal the accepted bytes with a replay hash and with authority effect None.

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
- [`omega_engine/crates_rs/omega_replay/src/lib.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_replay/src/replay_hash.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_replay/src/run_folder.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F000_finite/S001_authorization_and_incompleteness/001_authorization_an_incompleteness_theory/python/src/authorization_incompleteness/replay_fiber.py`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F003_omega_engine/S000_prime_algorithms_and_runtime/000_omega_engine_prime_algorithms_and_runtime/python/src/omega_engine_rc/prime_triad.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0217](TFQ-0217_a_replay_digest_does_not_widen_the_statement.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F003.S000`, `F003.S000:000_omega_engine_prime_algorithms_and_runtime`, `F000.S001:001_authorization_an_incompleteness_theory`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F003_omega_engine/S000_prime_algorithms_and_runtime`
  - `omega_engine_atlas/coda_atlas/F003_omega_engine/S000_prime_algorithms_and_runtime/000_omega_engine_prime_algorithms_and_runtime`
  - `omega_engine_atlas/coda_atlas/F000_finite/S001_authorization_and_incompleteness/001_authorization_an_incompleteness_theory`
