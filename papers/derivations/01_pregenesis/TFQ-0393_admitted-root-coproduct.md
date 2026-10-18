# [TFQ-0393] admitted-root-coproduct

> **Stage**: `PREGENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `b4d1bc9d-0514-5ac5-8679-19aed83d4cda`  
> **Parent Derivation**: [TFQ-0392](TFQ-0392_inscription-to-coproduct-gap.md)

---

## 1. Abstract & Formal Statement

PG-ROOT-DIFF-STRUCTURE is a separate admitted primitive in derivation_dag.json: Real_0 is recorded there as PrimitiveDifference joined with Structure, a typed coproduct of two channels, with no reduction of either channel to the other. The parent link of this node is only the gap route from the inscription. It is not a derivation of the coproduct from <>. The reading note names ENC-1138 and GTLA rule 2 as the separate definition site. The finite statement still required is to keep this coproduct admitted on its own record, or to leave it unjoined. Chapter 1 does not replay it.

### Governing Obligation
Record Difference joined with Structure as its own admitted coproduct, and do not obtain it from literal <>.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Primitive difference delta_0 (assumption: admitted primitive)`
- **Admitted**: `Structure carrier (assumption: declared, not derived)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Admitted, not derived. Two sources mark the lineage withdrawn/unassigned (ENC-1138 layer_withdrawn 2026-08-18). The coproduct is not connected by any derivation to the literal inscription <> (see PG-INERT-DIAMOND).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_root_coproduct_inert_diamond_and_six_operation_separation`](../../code/lean4/)
- [`missing declaration obligation: a coproduct Real_0 distinct from HasRawDistinction in B001_raw_distinction.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/lean4/FromPrimitiveDifferenceToFiniteObstructionCalculus/B001_raw_distinction.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/029_the_anomalon_boundary/lean4/OntologyBasic.lean::Real0`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: a coproduct struct whose constructors are independent of the inscription token in omega_ooutwire_primitives`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche16_master_177_node_172_route_dag_completeness_and_operad_audit_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_types/src/primitive_difference.rs::PrimitiveDifference`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: a two-summand carrier in the S000 python package that is not constructed from preservation.py token data`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0394](TFQ-0394_primitive-axiom-list-underived.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/book/ch01_genesis_of_difference.md`
