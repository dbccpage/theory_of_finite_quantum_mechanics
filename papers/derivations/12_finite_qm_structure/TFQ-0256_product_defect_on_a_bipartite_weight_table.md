# [TFQ-0256] Product defect on a bipartite weight table

> **Stage**: `FINITE_QM_STRUCTURE` | **Status**: `SOURCE_RECORD`  
> **UUID**: `9ed5b9fe-e7f5-582c-89a7-84ae327e84fe`  
> **Parent Derivation**: [TFQ-0234](../10_finite_qm_core/TFQ-0234_supplied_hilbert_carrier_after_the_conditional_lift.md)

---

## 1. Abstract & Formal Statement

QM_070, retained inside the consolidated QM_071 account, obliges a product defect on a nonnegative joint table. The defect is the table minus the normalized product of its marginals, and the l1 mass of that defect vanishes exactly when the table factors. The scale-free form is the l1 distance from the normalized table to its own marginal product, which need not be the distance to every product table. DS-QM070-PRODUCT-NONFACTORIZATION adds the firewall seen in the derivation graph: the defect is basis-relative and does not see entanglement, because a Bell state and a classical mixture can share one table.

### Governing Obligation
Test factorization of a finite joint table by the product defect, and do not read a nonzero defect as entanglement.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `bipartite product structure A x B on a joint table (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Lean file for Phi_zero_iff_factors not verified; the tensor-product rule itself is not derived (H014 lists it as open).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm070_071_product_nonfactorization_and_entanglement_witness`](../../code/lean4/)
- [`lean4/quantum_mechanics/H014TensorCompositionBoundary.lean::tensor_not_forced_open`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/entanglement.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/entanglement.rs::entanglement`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0257](TFQ-0257_separability_witness_relative_to_a_declared_family.md)
- [TFQ-0259](TFQ-0259_finite_chsh_ceiling_on_one_global_joint_table.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-BELL-CLASSICAL-JOINT-EXTENSION`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-BELL-CLASSICAL-JOINT-EXTENSION` (`FINITE_QM_CORE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_CORE-FQ-BELL-CLASSICAL-JOINT-EXTENSION`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1140, -2280, 1710]`, `chord_potential = 1710`, `holonomy_gamma2 = 2280`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(FQ-BELL-CLASSICAL-JOINT-EXTENSION): 4*idx(114) + 3*stage_rank(7) + route_degree(3) == 480` ($\text{value} = 480$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(FQ-BELL-CLASSICAL-JOINT-EXTENSION): R_raw(263) - G_cob(128) - S_decoy(7) == 128 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 128$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_bell_classical_joint_extension_convex_bound`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 22c87a7cc081b29fb96b6b3983b03b35c699ed9445f9a1cf0cd57046616791a6`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM070-PRODUCT-NONFACTORIZATION`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM070-PRODUCT-NONFACTORIZATION` (`FINITE_QM_STRUCTURE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-DS-QM070-PRODUCT-NONFACTORIZATION`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1500, -3000, 2250]`, `chord_potential = 2250`, `holonomy_gamma2 = 3000`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM070-PRODUCT-NONFACTORIZATION): 4*idx(150) + 3*stage_rank(8) + route_degree(5) == 629` ($\text{value} = 629$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM070-PRODUCT-NONFACTORIZATION): R_raw(340) - G_cob(166) - S_decoy(8) == 166 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 166$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm070_071_product_nonfactorization_and_entanglement_witness`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 9b7b203675cd581ecd15511bdd7832c6c361d581a33c1d487e500f76f0d25b83`
