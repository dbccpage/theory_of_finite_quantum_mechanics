# [TFQ-0127] Hilbert carriers and tensor index

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `b6cb76a2-e7d9-5fcf-b719-1d87badeeb34`  
> **Parent Derivation**: [TFQ-0126](tfq_0126_finite_configurations_and_complex_structure.md)

---

## 1. Abstract & Formal Statement

Covers hilbert_space.rs, higher_dim.rs, dagger_category.rs, and operational_axiom_selection.rs. hilbert_space.rs takes HilbertSpace as a labeled carrier C^d, d at least 1, in the declared standard basis, and TensorCarrier as a lexicographic flat index. Overflow past operation limits is a typed refusal. The other files check a PPT Tiles complement, the dagger compact category of finite Gaussian-rational spaces, and local tomography versus dimension. A Python replay and a Lean 4 declaration would still have to match the flat-index bijection and those refusals.

### Governing Obligation
Match the declared lexicographic flat-index bijection, dimension product, and typed refusal past operation limits.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/dagger_category.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/higher_dim.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/hilbert_space.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/operational_axiom_selection.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`not located`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/operational_axiom_selection.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0128](tfq_0128_declared_u_1_connections.md)
- [TFQ-0129](tfq_0129_exact_rays_and_pure_states.md)
- [TFQ-0164](tfq_0164_ribbon_anyons_and_yang_baxter.md)
- [TFQ-0165](tfq_0165_spin_network_area_labels.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-GAP-TENSOR-UNIQUENESS`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-GAP-TENSOR-UNIQUENESS` (`FINITE_QM_CORE` / `CONDITIONAL`)
- **Mined Operad Family (`M2`)**: `OP-FQ-TENSOR-CONE-BRACKETING`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [70, -140, 105]`, `chord_potential = 105`, `holonomy_gamma2 = 140`
- **Finite Shadow Exact Witness (`M4`)**: `cone_bracketing_sum: min_cone(50) + hilbert_cone(70) + max_cone(100) == 220` ($\text{value} = 220$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `projDump_pauliZ_covariance_defect: |(1,0) - (-1,0)|_1 == 2 (rival bilinear map violates local Pauli-Z covariance)` ($\text{value} = 2$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4-flash` | `status = PASS` | `receipt_sha256 = f797bcf12dc545d42a2a96b7dd02fe0b59613b8cfc18c337d4470e9c4bee4e7f`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`GP-IMPORT-TENSOR-PRODUCT`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `GP-IMPORT-TENSOR-PRODUCT` (`L1_TO_L2` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-GP-TENSOR-BILINEAR-RIVAL`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [260, -520, 390]`, `chord_potential = 390`, `holonomy_gamma2 = 520`
- **Finite Shadow Exact Witness (`M4`)**: `kronecker_dimension_2x2: 2 * 2 == 4` ($\text{value} = 4$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `projDump_collision_defect: ||projDump(e0,e0) - projDump(e0,e1)||_1 == ||(1,0) - (1,0)||_1 == 0 (collapses distinct second-system states)` ($\text{value} = 0$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = c8aef65056eec1f595edaf2a9feac20558bfc7c4c8de960ec337c4965eab6cf5`
