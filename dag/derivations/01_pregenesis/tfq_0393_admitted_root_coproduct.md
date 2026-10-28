# [TFQ-0393] admitted-root-coproduct

> **Stage**: `PREGENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `b4d1bc9d-0514-5ac5-8679-19aed83d4cda`  
> **Parent Derivation**: [TFQ-0392](tfq_0392_inscription_to_coproduct_gap.md)

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
- [`external:sha256:2e264c28e45671b646ce8e6ad290f689f7fb8ecf3625b109b9e97df3a74ee073`](../../code/lean4/)
- [`external:sha256:1758a99dfa72fba91d01d0dfa5fc4fa5aced126b77ab906cd01118b497793533::Real0`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: a coproduct struct whose constructors are independent of the inscription token in wire_primitives`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche16_master_177_node_172_route_dag_completeness_and_operad_audit_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)
- [`external:sha256:273fb96233ba30a85e30a4045bee2e4a1750a78880e5e26a58cd80c6da7e4a80::PrimitiveDifference`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: a two-summand carrier in the S000 python package that is not constructed from preservation.py token data`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0394](tfq_0394_primitive_axiom_list_underived.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `external:sha256:eed47042e450b5608d203687f53103f3f8f4cbc3e5056c8a3b73b9992a1811db`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-ROOT-DIFF-STRUCTURE`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-ROOT-DIFF-STRUCTURE` (`PREGENESIS` / `ADMITTED_PRIMITIVE`)
- **Mined Operad Family (`M2`)**: `OP-PREGENESIS-PG-ROOT-DIFF-STRUCTURE`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [360, -720, 540]`, `chord_potential = 540`, `holonomy_gamma2 = 720`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-ROOT-DIFF-STRUCTURE): 4*idx(36) + 3*stage_rank(1) + route_degree(4) == 151` ($\text{value} = 151$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-ROOT-DIFF-STRUCTURE): R_raw(77) - G_cob(38) - S_decoy(1) == 38 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 38$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche16_master_177_node_172_route_dag_completeness_and_operad_audit_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 99dcda861d27c22f53e0bc2d9bf8a58cc8ee851f5c84a144b3301fc634ca4eba`
