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
- [`absent: no local lean twin located for external:sha256:3d9181bb97724a3cc5c644973f9e75ca0485bc59c9e7035c14c82e92f79e3123`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/wdp/prime_algos/prime_algorithm_2.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for external:sha256:118b9549a600eee604e58f81e4d692d85eacc23649fb6d451821820ca6f89911`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0221](tfq_0221_intake_terminals_exclude_an_authorized_constructor.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F003.S000:000_omega_engine_prime_algorithms_and_runtime`, `F003.S000`
- **Primary Source Paths**:
  - `external:git-tree:e03ce30c258cf9ca164637ea387b5267bad58df9`
  - `external:git-tree:5d358f5062016c742016b891fa7891bb0f0e19ef`
