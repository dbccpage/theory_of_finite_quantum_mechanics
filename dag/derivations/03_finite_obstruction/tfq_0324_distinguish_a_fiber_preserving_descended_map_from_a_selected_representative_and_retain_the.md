# [TFQ-0324] Distinguish a fiber-preserving descended map from a selected representative, and retain the

> **Stage**: `FINITE_OBSTRUCTION` | **Status**: `SOURCE_RECORD`  
> **UUID**: `b8232100-12ab-50bf-b4a3-d56f8b55e13f`  
> **Parent Derivation**: [TFQ-0323](tfq_0323_carry_a_declared_report_its_fibers_and_any_section_as_separate_data.md)

---

## 1. Abstract & Formal Statement

Chapter 05 separates fiber preservation from a selected representative map, with formal Lean and executable control. The mirror lists E012_unique_descended_dynamics.lean, E013_selected_projected_map.lean, and E014_descent_agreement.lean, together with E016_semigroup_defect.lean and E017_escape_with_exact_descent.lean. test_descent.py sits in the same Python tests_unit tree. The candidate README says these modules retain a candidate-only scope marker. Descent agreement in a file name is not a discharge of the Genesis map in S000-GAP-GENESIS-TO-PD. AuthorityEffect is None.

### Governing Obligation
Distinguish a fiber-preserving descended map from a selected representative, and retain the semigroup defect when they disagree.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/lean4/FromPrimitiveDifferenceToFiniteObstructionCalculus/E012_unique_descended_dynamics.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/lean4/FromPrimitiveDifferenceToFiniteObstructionCalculus/E013_selected_projected_map.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/lean4/FromPrimitiveDifferenceToFiniteObstructionCalculus/E014_descent_agreement.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/lean4/FromPrimitiveDifferenceToFiniteObstructionCalculus/E016_semigroup_defect.lean`](../../code/lean4/)

### Sovereign Rust Certifiers
*Computational witness tracked under `theory_of_finite_qm` crate.*

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/python/tests_unit/test_descent.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0325](tfq_0325_do_not_treat_the_primitive_difference_walk_as_paper_0_and_do.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000`, `F000.S000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/lean4/FromPrimitiveDifferenceToFiniteObstructionCalculus/README.md`
