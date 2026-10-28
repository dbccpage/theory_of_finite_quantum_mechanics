# [TFQ-0394] primitive-axiom-list-underived

> **Stage**: `PREGENESIS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `c182247d-b2e8-58ea-94fe-4c2a71ad2aa0`  
> **Parent Derivation**: [TFQ-0393](tfq_0393_admitted_root_coproduct.md)

---

## 1. Abstract & Formal Statement

PG-PRIMDIFF-AXIOMS records a Rust-side list A1 through A10 and an admission kernel that admits an ordered pair under a token. The DAG calls that an implementation of an admitted floor, not a derivation of the floor, and it names bridge obligation GEN-WDP-O01 as open. The Rust file cited for the axiom enum was not opened. B001_raw_distinction.lean, which was searched, declares HasRawDistinction and TwoPointMarks for a carrier with two unequal points. The finite statement still required is either an explicit admission of that axiom list or a justification that does not treat B001 as the list.

### Governing Obligation
The primitive-difference axiom list A1-A10 stays an admitted implementation debt under GEN-WDP-O01, not a consequence of HasRawDistinction.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Finite carrier items (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Bridge obligation GEN-WDP-O01 (justify or explicitly admit the primitive-to-witness carrier, signature, law and challenge-generation floor) is open; the explicit admission is done, the stronger derivation is not.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`declaration obligation: HasRawDistinction is not a stand-in for an unread A1-A10 enum`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_root_coproduct_inert_diamond_and_six_operation_separation`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_six_operations_and_primdiff_admission_gate`](../../code/lean4/)
- [`external:sha256:2e264c28e45671b646ce8e6ad290f689f7fb8ecf3625b109b9e97df3a74ee073`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: the axiom enum cited by the DAG was not opened; do not equate it with wire_primitives until a path is checked`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)
- [`external:sha256:3301e36106cfe1fb4415d4f6218951cd83516f0a714d773fcb477ea3dce63814::GenesisAdmissionKernel`](../../code/rust/src/)
- [`external:sha256:3301e36106cfe1fb4415d4f6218951cd83516f0a714d773fcb477ea3dce63814::PrimitiveDifferenceAxiom`](../../code/rust/src/)
- [`external:sha256:3301e36106cfe1fb4415d4f6218951cd83516f0a714d773fcb477ea3dce63814::TriadSignature`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: test_primitive_difference.py was listed and not opened; it must not be read as the A1-A10 list`](../../code/python/)
- [`external:sha256:83ae72f62c2009c887a2a21d1fbd5669a0959874e2a4e9f3c34410d5175e9807`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0395](tfq_0395_law_bearing_cut_not_two_marks.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `external:sha256:2e264c28e45671b646ce8e6ad290f689f7fb8ecf3625b109b9e97df3a74ee073`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-PRIMDIFF-AXIOMS`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-PRIMDIFF-AXIOMS` (`PREGENESIS` / `DEFINITION`)
- **Mined Operad Family (`M2`)**: `OP-PREGENESIS-PG-PRIMDIFF-AXIOMS`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [390, -780, 585]`, `chord_potential = 585`, `holonomy_gamma2 = 780`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-PRIMDIFF-AXIOMS): 4*idx(39) + 3*stage_rank(1) + route_degree(2) == 161` ($\text{value} = 161$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-PRIMDIFF-AXIOMS): R_raw(83) - G_cob(41) - S_decoy(1) == 41 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 41$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_root_coproduct_inert_diamond_and_six_operation_separation`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 4dca55db1e670e1142617dc1292d8d2d2d076586332e911b559667d196308e6d`
