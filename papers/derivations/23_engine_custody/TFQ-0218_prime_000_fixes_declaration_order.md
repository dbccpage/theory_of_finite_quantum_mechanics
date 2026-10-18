# [TFQ-0218] Prime 000 fixes declaration order

> **Stage**: `ENGINE_CUSTODY` | **Status**: `SOURCE_RECORD`  
> **UUID**: `7c738d48-c0c7-5a35-932f-09d45a4cc9fb`  
> **Parent Derivation**: [TFQ-0217](TFQ-0217_a_replay_digest_does_not_widen_the_statement.md)

---

## 1. Abstract & Formal Statement

Prime 000 is the declaration-order gate inside the F003 runtime. Python lists source_locus, carrier, observer, primitive_difference, zero_relation, witness, and route, and validate_prime000 rejects a reordered tuple, a blank field, or an authority effect other than None. Lean declarationOrder has those seven stages, and the length check is reflexivity on the list. Rust prime_algorithm_0 tags every run with AuthorityEffect None and separates fixture numbers from verifier-produced numbers. A finite quantum derivation enters by filling the seven atlas fields. Order and nonblank text are the check.

### Governing Obligation
Accept a prime packet only when the seven fields are present, ordered, and set to None.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`omega_engine_atlas/coda_atlas/F003_omega_engine/S000_prime_algorithms_and_runtime/000_omega_engine_prime_algorithms_and_runtime/lean4/OmegaEnginePrimeAlgorithmsRuntime/Prime000.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_wdp/src/prime_algos/prime_algorithm_0.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F003_omega_engine/S000_prime_algorithms_and_runtime/000_omega_engine_prime_algorithms_and_runtime/python/src/omega_engine_rc/prime_triad.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0219](TFQ-0219_prime_001_blocks_adapter_descent_on_debt.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F003.S000:000_omega_engine_prime_algorithms_and_runtime`, `F003.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F003_omega_engine/S000_prime_algorithms_and_runtime/000_omega_engine_prime_algorithms_and_runtime`
  - `omega_engine_atlas/coda_atlas/F003_omega_engine/S000_prime_algorithms_and_runtime`
