# [TFQ-0395] law-bearing-cut-not-two-marks

> **Stage**: `PREGENESIS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `ae047cb3-3880-5b4e-9efc-412b184091eb`  
> **Parent Derivation**: [TFQ-0394](TFQ-0394_primitive-axiom-list-underived.md)

---

## 1. Abstract & Formal Statement

PG-ADMISSION-FLOOR says that for an exhibited cut with two distinct endpoints under a law, the endpoints are apart, no cut exists on a subsingleton carrier, and identifying the endpoints breaks the law. The Lean file named for that floor was not opened. Chapter 2, opened, says a carrier and a witness that a is not b state a raw distinction and do not identify points, form a quotient, or infer a preferred representation. The finite statement still required is a law-bearing cut as extra data beyond two marks. A pointed relation, the DAG says, does not decide distinctness in either direction.

### Governing Obligation
An exhibited cut needs a law as well as two endpoints; two marks alone do not supply that law, a quotient, or a preferred representation.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Exhibited cut with law (assumption: supplied, not selected from equality alone)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Shows a law is needed to separate endpoints; does not derive the law from <> or from Real_0.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`](../../code/lean4/)
- [`missing declaration obligation: endpoints-apart under a law, no cut on a subsingleton, beyond TwoPointMarks`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/lean4/FromPrimitiveDifferenceToFiniteObstructionCalculus/B001_raw_distinction.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/PointedRelation.lean::pointed_relation_independence`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/PrimitiveAdmissionFloor.lean::endpoints_apart`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/PrimitiveAdmissionFloor.lean::identification_breaks_law`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/PrimitiveAdmissionFloor.lean::no_cut_on_subsingleton`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: a cut struct with an explicit law field, absent from the opened genesis regime header`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: test_zero_laws.py was listed and not opened; a law must stay an input, not a consequence of two marks`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/python/tests_unit/test_zero_laws.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0396](../02_genesis/TFQ-0396_sealed-tag-to-carrier-gap.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/book/ch02_primitive_difference_and_finite_carrier.md`
