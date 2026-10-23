# [TFQ-0540] wdp-asymmetry-injection-ledger

> **Stage**: `WDP` | **Status**: `DEFINITION`  
> **UUID**: `e062b03f-acd7-56c6-99c0-f546bcb9abc1`  
> **Parent Derivation**: [TFQ-0536](tfq_0536_wdp_failed_sameness.md)

---

## 1. Abstract & Formal Statement

For any proposed selection the injection ledger records the first input that breaks the relevant symmetry: a named element or base point, an orientation, an order or clock, a measure or weighting, a boundary condition, a representation, an observer profile, a stochastic device with its distribution, or a physical law outside the root package. WDP-CH03-D01 defines the asymmetry-price frontier, relative to a specified implementation class and dependency preorder, as the family of inclusion-minimal declared input sets whose removal restores a symmetry that moves the output; a scalar price needs a stated cost function, and frontier elements may tie or be incomparable. In the declare-then-assert search, a refinement can leave a single class made of two responses exchanged by the swap of the data, so choosing one is a further declared input recorded in the ledger.

### Governing Obligation
Enter the first symmetry-breaking input of every selection in the injection ledger, and report frontier elements relative to the declared implementation class and preorder without claiming a unique or global minimum.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared implementation class and dependency preorder for the frontier (assumption)`

### Further Prerequisites
- [TFQ-0340](tfq_0340_refuse_a_symmetry_equivariant_distinguished_point_on_a_finite_set_of_size_at.md) Refuse a symmetry-equivariant distinguished point on a finite set of size at

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Definition only: no uniqueness or global-minimality theorem holds for the frontier in general; it rests on the nonselection row WDP-CH03-P01 (TFQ-0340), and the declare-then-assert separation row CH03-P03 takes no Lean credit.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/WitnessedDifference/WitnessedDifference/Symmetry.lean::no_invariant_oriented_edge`](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Symmetry.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust implementation of the injection ledger or the asymmetry-price frontier`

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/symmetry.py::exhaustive_relation_audit`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/symmetry.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md:669-692`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md:736-763`
  - `omega_engine_education/documentation/006_oewdp/levels/level_02_residuals_obstructions.md:98-113`
