# [TFQ-0293] Complex field as a declared carrier

> **Stage**: `L1_TO_L2` | **Status**: `GAP`  
> **UUID**: `df25fd2a-a9a7-58b1-880a-f11321a15b8d`  
> **Parent Derivation**: [TFQ-0292](tfq_0292_square_root_field_for_amplitude_coordinates.md)

---

## 1. Abstract & Formal Statement

A complex field for sector amplitudes is an import. qm_122_finite_hilbert_boundary_from_primitive_difference.md records Gaussian integers as a finite stand-in and states that they are not a field, since one plus i has no inverse there. The finite obligation is to keep Q(i), when used, as a declared coefficient pack rather than a consequence of primitive difference. complex_structure_selector.rs checks pairings on Gaussian rationals under the identity or conjugation. That is a pairing check, not a construction of the continuum complex field. derivation_dag.json records the id L1-IMP-COMPLEX-FIELD.

### Governing Obligation
Declare any complex coefficient pack and do not read it off the report fiber.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `complex field C: assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> No derivation of C from <> or from the window in the sources read. See route L1-R-COMPLEX-GAP.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.gp_and_l1_imported_field_circle_dilation_and_time_interpolation_boundaries`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`](../../code/lean4/)
- [`lean4/quantum_mechanics/H007Complexification.lean::gi_not_embedded`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`external:sha256:1ae9121daca3f6d1f5cb700a325bc1aaa0d5a6988db99eee907e24ca729e876e`](../../code/rust/src/)
- [`external:sha256:ddaee3d0d77722244a6451750ca1e5acf7a57b4f02e75ecec70e810976d57d9e`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0294](tfq_0294_circle_phases_as_an_imported_unit_group.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`, `F002`
- **Primary Source Paths**:
  - `external:sha256:ddbf8bad986fa5587b534c0f96f2c4ff370f95cb696c6245df0526d4bad32351`
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
  - `external:sha256:aa96a8bb76ae8bc4e83571f57783f369b645332421db0e1fdd8a7d9cf333aac9`
  - `external:sha256:b4ded5af7203501488fee5e61c915a8d553f0f71a6a3ff5b07969cfda8abaa07`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`GP-IMPORT-COMPLEX-FIELD`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `GP-IMPORT-COMPLEX-FIELD` (`L1_TO_L2` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-GP-COMPLEX-FIELD-GAUSSIAN-GAP`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [210, -420, 315]`, `chord_potential = 315`, `holonomy_gamma2 = 420`
- **Finite Shadow Exact Witness (`M4`)**: `gaussian_norm_multiplicativity: N(1+i) * N(2+i) = 2 * 5 == 10` ($\text{value} = 10$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `non_unit_norm_1_plus_i: N(1+i) == 2 != 1 (so (1+i)*(a+bi) = 1 has 2*(a^2+b^2)=1, has no integer solution in Z)` ($\text{value} = 2$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = fbaa7c263e1f933fe5bdd5a8676697b23f365b2650ecd76ba3a21e2f213135d5`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-IMP-COMPLEX-FIELD`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-IMP-COMPLEX-FIELD` (`L1_TO_L2` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-L1-COMPLEX-FIELD-H007`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [270, -540, 405]`, `chord_potential = 405`, `holonomy_gamma2 = 540`
- **Finite Shadow Exact Witness (`M4`)**: `gaussian_unit_group_cardinality: |{1, -1, i, -i}| == 4` ($\text{value} = 4$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `non_invertible_gaussian_integer_norm: N(2 + i) = 2^2 + 1^2 == 5 != 1 (not a field element inverse in Z[i])` ($\text{value} = 5$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 4a47ba81bc9fb2f8636d646d7e989614dd2d704052c54b653b024e81ec51b6b9`
