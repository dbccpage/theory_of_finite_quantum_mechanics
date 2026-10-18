# [TFQ-0257] Separability witness relative to a declared family

> **Stage**: `FINITE_QM_STRUCTURE` | **Status**: `SOURCE_RECORD`  
> **UUID**: `f74098bf-9646-5bd2-93d3-80c405629e8d`  
> **Parent Derivation**: [TFQ-0256](TFQ-0256_product_defect_on_a_bipartite_weight_table.md)

---

## 1. Abstract & Formal Statement

QM_071, in the consolidated account, separates three grades: classical table independence, membership in the convex hull of a declared finite product family, and membership in the convex hull of all product density operators. A separating functional certifies the middle grade when it sits on one side of every declared product point and on the other side of the tested table. DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS says that certificate is soundness only. Completeness, in the sense that every entangled state has a witness, is not claimed, and general separability is not addressed.

### Governing Obligation
Certify non-membership only against a declared finite product family, and leave completeness unclaimed.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `coherence coordinates in the carrier (assumption)`
- **Admitted**: `declared product-point family (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Completeness converse (finite LP duality) is an upgrade target.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm070_071_product_nonfactorization_and_entanglement_witness`](../../code/lean4/)
- [`lean4/quantum_mechanics/DualWitness.lean::dual_witness_certifies_trace_distance`](../../code/lean4/)
- [`lean4/quantum_mechanics/Entanglement.lean::bell_state_is_entangled`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/entanglement.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/entanglement.rs::entanglement`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0258](TFQ-0258_qubit_not_derived_from_the_bit-shadow.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS` (`FINITE_QM_STRUCTURE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1510, -3020, 2265]`, `chord_potential = 2265`, `holonomy_gamma2 = 3020`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS): 4*idx(151) + 3*stage_rank(8) + route_degree(3) == 631` ($\text{value} = 631$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS): R_raw(342) - G_cob(167) - S_decoy(8) == 167 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 167$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm070_071_product_nonfactorization_and_entanglement_witness`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 569f2515d598a0fb977226becddfab51072c61c4dfcb278fcb81b36fb78c3615`
