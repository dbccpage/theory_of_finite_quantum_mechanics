# [TFQ-0395] law-bearing-cut-not-two-marks

> **Stage**: `PREGENESIS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `ae047cb3-3880-5b4e-9efc-412b184091eb`  
> **Parent Derivation**: [TFQ-0394](tfq_0394_primitive_axiom_list_underived.md)

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
- [`external:sha256:2e264c28e45671b646ce8e6ad290f689f7fb8ecf3625b109b9e97df3a74ee073`](../../code/lean4/)
- [`atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/PointedRelation.lean::pointed_relation_independence`](../../code/lean4/)
- [`atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/PrimitiveAdmissionFloor.lean::endpoints_apart`](../../code/lean4/)
- [`atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/PrimitiveAdmissionFloor.lean::identification_breaks_law`](../../code/lean4/)
- [`atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/PrimitiveAdmissionFloor.lean::no_cut_on_subsingleton`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: a cut struct with an explicit law field, absent from the opened genesis regime header`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: test_zero_laws.py was listed and not opened; a law must stay an input, not a consequence of two marks`](../../code/python/)
- [`external:sha256:dfd5a9d9f39a47b64ef5618e637944f21532c403db19c64a7232c538f9852b9c`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0396](../02_genesis/tfq_0396_sealed_tag_to_carrier_gap.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `external:sha256:07724476310fc38ea18d221fb21dde8539d81abdf022c569173d1b10f9085473`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-ADMISSION-FLOOR`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-ADMISSION-FLOOR` (`PREGENESIS` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-PREGENESIS-PG-ADMISSION-FLOOR`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [400, -800, 600]`, `chord_potential = 600`, `holonomy_gamma2 = 800`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-ADMISSION-FLOOR): 4*idx(40) + 3*stage_rank(1) + route_degree(4) == 167` ($\text{value} = 167$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-ADMISSION-FLOOR): R_raw(85) - G_cob(42) - S_decoy(1) == 42 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 42$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 601fef8267a9f287db8124c1fe87db4c736f4c2c6dc42e7639200b0c8d38fda4`
