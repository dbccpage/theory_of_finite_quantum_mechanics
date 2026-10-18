# [TFQ-0228] Finite-shadow exact arithmetic refuses a continuum upgrade

> **Stage**: `ENGINE_CUSTODY` | **Status**: `GAP`  
> **UUID**: `779a2a1a-c3af-535f-892e-e1594f8d5129`  
> **Parent Derivation**: [TFQ-0227](TFQ-0227_pipeline_runtime_refuses_to_mint_authority.md)

---

## 1. Abstract & Formal Statement

Finite-shadow exact arithmetic refuses a silent continuum upgrade. finite_shadow_exact.rs carries residual masses, uses exact integer or rational budgets, and says a continuum request without a convergence witness stays at an oracle-needed mark. The header calls the module a diagnostic dual, not a continuum theorem, and says Python duals remain test-only prototypes. That agrees with the F002 register, which still lists the finite-to-continuum bridge as open. A derivation may call this code for a diagnostic terminal. The call does not remove GAP-F000-F002-001 and does not authorize a smooth limit.

### Governing Obligation
Allow shadow diagnostics and refuse to delete the open finite-to-continuum gap.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent/002_from_primitive_difference_to_mtheory/lean4/FromPrimitiveDifferenceToMTheory/ContinuumLimit.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_wdp/src/coda/q/finite_shadow_exact.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent/002_from_primitive_difference_to_mtheory/python/src/mtheory_interfaces/cochain_limit.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0229](TFQ-0229_structure_checks_do_not_assign_a_derived_status.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F002.S000`, `F003.S000`, `F001.S000`, `F000.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent`
  - `omega_engine_atlas/coda_atlas/F003_omega_engine/S000_prime_algorithms_and_runtime`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction`
