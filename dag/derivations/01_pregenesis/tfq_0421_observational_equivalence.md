# [TFQ-0421] observational-equivalence

> **Stage**: `PREGENESIS` | **Status**: `DEFINITION`  
> **UUID**: `bec909db-412a-5b1b-a6bb-7c0099a7bc15`  
> **Parent Derivation**: [TFQ-0362](tfq_0362_four_host_conditions.md)

---

## 1. Abstract & Formal Statement

Relative to the family O_n of internal observations available at stage n, x ≈ₙ y holds exactly when o(x) = o(y) for every o in O_n, with equality taken in each observation's codomain. If O_n is empty, every pair is equivalent vacuously, so with no observations <a> ≈ₙ <ab>. This is regime-relative equivalence: it does not make the strings equal and does not install an equality operator inside the regime.

### Governing Obligation
Define x ≈ₙ y as agreement of every declared observation in O_n, and with O_n empty put all inscriptions in one class without asserting string equality or an internal equality rule.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `A declared carrier of inscriptions and a declared family O_n of observations on it (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The relation depends on the declared O_n and compares observation values in the metatheory; it is not literal string equality and does not say which observations a regime should have.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/PreGenesisToMssn/Observation.lean::SameProfile`](../../../lean4/Imported/PreGenesisToMssn/Observation.lean)
- [`lean4/Imported/PreGenesisToMssn/Observation.lean::empty_profiles_equal`](../../../lean4/Imported/PreGenesisToMssn/Observation.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust observation-family type for Pre-Genesis inscriptions; the Genesis profile instance is separable in genesis/code/rust/src/separability.rs`

### Python Oracles & Numerical Evaluators
- `missing obligation: no Python ≈ₙ check over Pre-Genesis inscriptions; the Genesis profile instance is separable in genesis/code/derivation/observe.py`

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0422](tfq_0422_presentation_not_expressive_lift.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/paper.md:107-116`
  - `omega_engine_education/documentation/000_oepregen/sources/analysis_derivation_v1.md:177-215`
  - `omega_engine_education/documentation/000_oepregen/03_results_and_arguments.md:64-70`
