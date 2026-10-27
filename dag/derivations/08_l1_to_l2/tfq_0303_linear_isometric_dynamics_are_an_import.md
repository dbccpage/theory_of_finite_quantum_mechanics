# [TFQ-0303] Linear isometric dynamics are an import

> **Stage**: `L1_TO_L2` | **Status**: `GAP`  
> **UUID**: `f8fa4c78-b475-538f-a132-74bad24cfc9b`  
> **Parent Derivation**: [TFQ-0302](tfq_0302_phase_averaged_shadow_under_declared_phases.md)

---

## 1. Abstract & Formal Statement

Reversible linear isometric dynamics on the lift are an import. qm_020_born_normalization_and_conditional_hilbert_lift.md lists them as assumption five in the section labeled Theorem 6. qm_122_finite_hilbert_boundary_from_primitive_difference.md records a different finite object: a reversible report update extends to a linear map preserving an admitted form, and that map is an isometric automorphism of a ring with conjugation, not a Hilbert-space unitary, because there is no completeness and the coefficients need not be a field. A deterministic report update need not be reversible.

### Governing Obligation
Import linear isometric Hilbert dynamics, and do not equate them with report-level isometries.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `isometry / unitarity: assumption`
- **Admitted**: `linear structure on dynamics: assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Lean module symbols not grepped; file existence only checked via listing in prior survey.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`](../../code/lean4/)
- [`lean4/quantum_mechanics/H003ReversibilityGate.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/H006PermutationUnitary.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`external:sha256:1021ae73186e67c501f0b2ecf0234074c4bdbf2a08bbc2af5a5a1794604a140b`](../../code/rust/src/)
- [`external:sha256:904a09d9ca4b18f97838457416046361842e537e895afce0374f8b6c670a1ef1`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0304](tfq_0304_lift_capacity_is_not_a_dynamics_derivation.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `external:sha256:ddbf8bad986fa5587b534c0f96f2c4ff370f95cb696c6245df0526d4bad32351`
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
  - `external:sha256:aa96a8bb76ae8bc4e83571f57783f369b645332421db0e1fdd8a7d9cf333aac9`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-IMP-LINEAR-ISOMETRIC-DYNAMICS`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-IMP-LINEAR-ISOMETRIC-DYNAMICS` (`L1_TO_L2` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-L1-ISOMETRIC-DYNAMICS-H003`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [300, -600, 450]`, `chord_potential = 450`, `holonomy_gamma2 = 600`
- **Finite Shadow Exact Witness (`M4`)**: `permutation_l2_norm_preservation: ||P(3,4)||_2^2 = 4^2 + 3^2 == 25` ($\text{value} = 25$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `reset_map_l2_norm_distortion: ||R(3,4)||_2^2 - ||(3,4)||_2^2 = (3+4)^2 - 25 = 49 - 25 == 24 != 0` ($\text{value} = 24$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = b11618c4bdc564cb8530c1c33def5425e3eddf813415be539e18ce7748a6fdd7`
