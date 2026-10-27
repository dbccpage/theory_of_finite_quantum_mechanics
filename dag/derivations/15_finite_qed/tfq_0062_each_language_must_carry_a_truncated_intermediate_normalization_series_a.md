# [TFQ-0062] Each language must carry: a truncated intermediate-normalization series, a

> **Stage**: `FINITE_QED` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `86c92853-ef3c-5f34-9dd1-6bc3def15633`  
> **Parent Derivation**: [TFQ-0061](tfq_0061_each_language_must_carry_2_forest_f0_equals_the_schur_complement_on_the.md)

---

## 1. Abstract & Formal Statement

perturbation_theory.rs runs a nondegenerate Rayleigh-Schrodinger series in intermediate normalization on a declared rational diagonal H0 plus a Gaussian-rational perturbation. series and energy_coefficients build the truncated expansion. characteristic_polynomial_residual interpolates det(E I - H(g)) from native characteristic-polynomial evaluations and substitutes the series. hellmann_feynman_holds is an independent check on that same finite matrix. degenerate_first_order exposes rational blocks when levels meet.

### Governing Obligation
Each language must carry: a truncated intermediate-normalization series, a characteristic-polynomial residual, a Hellmann-Feynman check, and an explicit refusal outside disjoint Gershgorin disks.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `declared unitary step (assumption)`
- **Admitted**: `generator branch selection for periodic sector (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The dichotomy is instance-level; the price theorems are definitional.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: not located`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:a60d347705d09f5b9f8544dc54af5241d756b5b8e476337baf9eb9d4f93d82b3`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0063](tfq_0063_each_language_must_carry_at_every_rational_loop_momentum_q_contracted_into.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
  - `external:git-tree:0fb81f77bbeba84143f574b5a4bc956196140991`
