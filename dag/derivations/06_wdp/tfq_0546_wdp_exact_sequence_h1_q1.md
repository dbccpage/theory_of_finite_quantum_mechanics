# [TFQ-0546] wdp-exact-sequence-h1-q1

> **Stage**: `WDP` | **Status**: `PROVED_LEAN`  
> **UUID**: `4a6a4ef2-08bd-5b80-8552-97333289af2b`  
> **Parent Derivation**: [TFQ-0004](tfq_0004_witnessed_difference_degree_1_window.md)

---

## 1. Abstract & Formal Statement

WDP-CH04-P03: in a window with d₁d₀ = 0, κ¹([h]) = d₁h is well defined on Q¹ because d₁(h + d₀α) = d₁h + d₁d₀α = d₁h, and 0 → H¹ → Q¹ → im d₁ → 0 is exact with H¹ = ker κ¹; closedness of a class does not depend on the representative, so H¹ is the usual Z¹/B¹ of the window. The sequence is an extension: in finite dimension it splits, but a splitting Q¹ ≅ H¹ ⊕ im d₁ requires a chosen section and is not canonical. Lean kappa_exact_sequence, with kappa_well_defined and kappa_mk, establishes on the literal quotient Quot (Repair d₀), for an additive d₁ with d₁ ∘ d₀ = 0, that the inclusion of H¹ is injective, its image is the kernel of κ, a class has zero charge exactly when every representative is closed, and κ maps onto the image of d₁; these three declarations use no axioms.

### Governing Obligation
Construct κ¹ on the repair quotient from an additive d₁ with a d₁d₀ = 0 certificate, check the four exactness clauses, and fix no splitting of Q¹ without a declared section.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared window with additive d₁ and a d₁d₀ = 0 certificate (assumption)`

### Further Prerequisites
- [TFQ-0345](tfq_0345_on_a_declared_window_with_d1_d0_0_compute_q1_kappa1.md) On a declared window with d1 d0 = 0, compute Q1, kappa1,

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The Lean statement is narrower than the row: set-level exactness on the literal quotient, without additive structure on Q¹, additivity of κ¹ or the splitting remark; it takes the window as declared and is not a Genesis derivation of it (TFQ-0344).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean::kappa_exact_sequence`](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean)
- [`lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean::kappa_mk`](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean)
- [`lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean::kappa_well_defined`](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust statement of the degree-1 exact sequence`

### Python Oracles & Numerical Evaluators
- `missing obligation: the ledger binds WDP-CH04-P03 to no executable; obstruction.py computes signatures, not the sequence`

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0547](tfq_0547_wdp_trichotomy_bounds.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean:98-117`
  - `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md:1518-1535`
  - `omega_engine_education/documentation/006_oewdp/levels/level_03_discrete_complex_cochains.md:319-328`
