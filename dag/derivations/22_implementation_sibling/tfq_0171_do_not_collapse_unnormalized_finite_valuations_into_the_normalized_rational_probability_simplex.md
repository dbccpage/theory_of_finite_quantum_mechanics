# [TFQ-0171] Do not collapse unnormalized finite valuations into the normalized rational probability simplex

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `GAP`  
> **UUID**: `ad624434-8292-540c-b408-bc43541823ec`  
> **Parent Derivation**: [TFQ-0167](tfq_0167_admit_only_exact_nonnegative_rational_masses_that_sum_to_one_with_no.md)

---

## 1. Abstract & Formal Statement

Unnormalized mass is a different carrier from the probability simplex. src/finite_valuation.rs states exact nonnegative Boolean valuations with no normalization requirement, and it admits an empty carrier that FinN refuses. src/lib.rs also declares signed_representation.rs, local_deterministic.rs, and marginal_compatibility.rs; those three bodies were not opened, so only the module declarations are in scope. The obligation is to keep an unnormalized valuation from standing in for a law that sums to one. H001ProbabilitySimplex.lean says its scaled integer grid is not the ordinary rational simplex.

### Governing Obligation
Do not collapse unnormalized finite valuations into the normalized rational probability simplex.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/H001ProbabilitySimplex.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/H001Rats.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_finite_probability/src/finite_valuation.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_finite_probability/src/local_deterministic.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_finite_probability/src/marginal_compatibility.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_finite_probability/src/signed_representation.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/floor.yaml`
