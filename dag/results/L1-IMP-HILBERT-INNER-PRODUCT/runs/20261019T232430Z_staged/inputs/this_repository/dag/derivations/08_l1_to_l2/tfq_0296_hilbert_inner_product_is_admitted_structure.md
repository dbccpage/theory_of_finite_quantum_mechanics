# [TFQ-0296] Hilbert inner product is admitted structure

> **Stage**: `L1_TO_L2` | **Status**: `GAP`  
> **UUID**: `3c8ee17d-25fb-5c6c-8711-2c569e56f4c4`  
> **Parent Derivation**: [TFQ-0295](tfq_0295_born_readout_of_a_supplied_lift_is_redundant.md)

---

## 1. Abstract & Formal Statement

A Hilbert inner product on the linearized carrier is an import. qm_122_finite_hilbert_boundary_from_primitive_difference.md says an inner product with a declared orthonormal report basis is extra structure and not unique: two positive-definite Gram matrices can disagree on the same module. The finite obligation is to admit one named form and to keep rival Gram forms visible. derivation_dag.json records L1-IMP-HILBERT-INNER-PRODUCT and says uniqueness of the inner product is not available.

### Governing Obligation
Admit one declared inner product and do not treat it as the unique form on the carrier.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `free linearization coefficient pack: assumption`
- **Admitted**: `inner product: assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Uniqueness of the inner product is not available.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`](../../code/lean4/)
- [`lean4/quantum_mechanics/H005InnerProductAdmission.lean::gram_not_unique`](../../code/lean4/)
- [`lean4/quantum_mechanics/H005InnerProductAdmission.lean::inner_product_admission`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/hilbert_space.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_state.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0297](../09_finite_hilbert/tfq_0297_inner_product_admission_slot_is_still_a_stub.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-IMP-HILBERT-INNER-PRODUCT`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-IMP-HILBERT-INNER-PRODUCT` (`L1_TO_L2` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-L1-GRAM-INNER-PRODUCT-H005`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [290, -580, 435]`, `chord_potential = 435`, `holonomy_gamma2 = 580`
- **Finite Shadow Exact Witness (`M4`)**: `standard_gram_norm_v11: (1,1)^T I_2 (1,1) = 1 + 1 == 2` ($\text{value} = 2$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `anisotropic_gram_norm_gap_v11: (1,1)^T diag(2,3) (1,1) - (1,1)^T I_2 (1,1) = 5 - 2 == 3 (distinct admissible Gram forms)` ($\text{value} = 3$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = f43cd2701d04b840881c03a2422b39addf88a6103350b20d80c6fb01588990c3`
