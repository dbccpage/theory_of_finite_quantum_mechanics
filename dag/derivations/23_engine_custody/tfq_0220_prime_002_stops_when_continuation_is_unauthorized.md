# [TFQ-0220] Prime 002 stops when continuation is unauthorized

> **Stage**: `ENGINE_CUSTODY` | **Status**: `SOURCE_RECORD`  
> **UUID**: `f3bdbcb9-6129-5e2a-8657-9a13d92af998`  
> **Parent Derivation**: [TFQ-0219](tfq_0219_prime_001_blocks_adapter_descent_on_debt.md)

---

## 1. Abstract & Formal Statement

Prime 002 stops continuation when the request is unauthorized. Python can_continue demands an outstanding obligation, a witness, a declared next carrier, adapter soundness, detector adequacy, a licensed lift, a preserved skeleton, budget, and an authorization bit, plus distinct runner and authorizer ids. If continuation_refused is set, the conjunction fails. Lean continuationAllowed copies that conjunction, and a false authorization bit yields false. Rust prime_algorithm_2 is the runtime face of the same control law. Another carrier step is allowed only when this predicate holds. AuthorityEffect stays None.

### Governing Obligation
Block another carrier step unless the continuation predicate holds, still at None.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`omega_engine_atlas/coda_atlas/F003_omega_engine/S000_prime_algorithms_and_runtime/000_omega_engine_prime_algorithms_and_runtime/lean4/OmegaEnginePrimeAlgorithmsRuntime/Prime002.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_wdp/src/prime_algos/prime_algorithm_2.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F003_omega_engine/S000_prime_algorithms_and_runtime/000_omega_engine_prime_algorithms_and_runtime/python/src/omega_engine_rc/prime_triad.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0221](tfq_0221_intake_terminals_exclude_an_authorized_constructor.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F003.S000:000_omega_engine_prime_algorithms_and_runtime`, `F003.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F003_omega_engine/S000_prime_algorithms_and_runtime/000_omega_engine_prime_algorithms_and_runtime`
  - `omega_engine_atlas/coda_atlas/F003_omega_engine/S000_prime_algorithms_and_runtime`
