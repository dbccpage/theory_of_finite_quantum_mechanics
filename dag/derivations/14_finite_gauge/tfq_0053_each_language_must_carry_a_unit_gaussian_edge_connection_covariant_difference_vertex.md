# [TFQ-0053] Each language must carry: a unit Gaussian edge connection, covariant difference, vertex

> **Stage**: `FINITE_GAUGE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `1f121d18-5f8a-5667-bf5f-f6adc1d26517`  
> **Parent Derivation**: [TFQ-0052](tfq_0052_each_language_must_carry_on_a_declared_m_2_q_i_packet_d0_of_an.md)

---

## 1. Abstract & Formal Statement

u1_graph_connection.rs stores a declared U(1) connection as one unit Gaussian rational on each oriented edge of a FiniteCochainPacket. The scalars are rational points of the circle, not a completed circle. A real cochain becomes a connection only through a separately declared CochainExponential, and that map loses information. The module computes the covariant difference (D_A psi)(u,v) = psi(v) - A_(u,v) psi(u), the vertex gauge A'_(u,v) = g(v) A_(u,v) conj(g(u)), and edgewise covariance of D_A. Closed-walk holonomy is gauge invariant; open-walk transport is covariant at its endpoints.

### Governing Obligation
Each language must carry: a unit Gaussian edge connection, covariant difference, vertex gauge, and closed-walk holonomy, with the exponential from an additive cochain declared and lossy.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `circle group U(1) (assumption)`
- **Admitted**: `circle group U(1): assumption`
- **Admitted**: `continuity of one-parameter phase group (assumption)`
- **Admitted**: `finite oriented graph (assumption)`
- **Admitted**: `non-triviality and order N of the edge phase cochain (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Finite N-torsion gauge invariance and sign-group separation are mechanized; completion to R/Z remains in FQ-GAP-U1-CIRCLE.

> [!WARNING]
> See L1-U1-SELECTOR-OTHER-SEGMENT.

> [!WARNING]
> Algebraic non-square obstruction in Q(i) and rational Cayley punctured-circle parameterization are mechanized; compact continuous R/Z completion remains a declared external import.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_gap_u1_circle_pythagorean_half_exponent_obstruction`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_u1_selector_split_real_zero_divisors_and_cayley_unit_circle`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_u1_transport_n_torsion_and_sign_separation`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011Circle.lean::sign_excluded_circle_still_imported`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011Circle.lean::sign_fails_connectedness_shadow`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011U1SelectorBoundary.lean::selector_not_free`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011U1SelectorBoundary.lean::u1_selector_boundary`](../../code/lean4/)
- [`not located`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`external:sha256:ddaee3d0d77722244a6451750ca1e5acf7a57b4f02e75ecec70e810976d57d9e`](../../code/rust/src/)
- [`external:sha256:6573cc4b53a02a97b89680e4bce638a9b06c197bb1a8eea2aae104001597f30d::gauge_equivalence`](../../code/rust/src/)
- [`external:sha256:a2c0d7450948662c89ffb80f0ebcfa02f1f013179a207d3d24db3421e81e84c6::UnitPhaseGroup`](../../code/rust/src/)
- [`external:sha256:376085dc410bbb86117c8efb40f2280ed15cb5734a22d050f6e1718aef3be579::evaluate_qm207_holonomy_bridge`](../../code/rust/src/)
- [`external:sha256:c2b85e3d42e7b05c158b418cbf2a803bdc86262cde384177ac8264c9c67ef6fe`](../../code/rust/src/)
- [`external:sha256:c2b85e3d42e7b05c158b418cbf2a803bdc86262cde384177ac8264c9c67ef6fe::U1Connection`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche9_bloch_gap_cayley_u1_hadamard_coherence_and_destructive_interference_witness`](../../code/rust/src/)
- [`external:sha256:77726675ace7bc93c8e8203260618f203aa20359b38d15cd48dee38f04c7a89f::half_exponent_obstruction`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0054](tfq_0054_each_language_must_carry_pure_gauge_iff_every_off_forest_edge_is_1.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
  - `external:git-tree:0fb81f77bbeba84143f574b5a4bc956196140991`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-U1-SELECTOR-OTHER-SEGMENT`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-U1-SELECTOR-OTHER-SEGMENT` (`L1_TO_L2` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-L1_TO_L2-L1-U1-SELECTOR-OTHER-SEGMENT`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [940, -1880, 1410]`, `chord_potential = 1410`, `holonomy_gamma2 = 1880`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(L1-U1-SELECTOR-OTHER-SEGMENT): 4*idx(94) + 3*stage_rank(6) + route_degree(3) == 397` ($\text{value} = 397$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(L1-U1-SELECTOR-OTHER-SEGMENT): R_raw(218) - G_cob(106) - S_decoy(6) == 106 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 106$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `sources/atlas/papers/finite_quantum_mechanics/lean/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm062_and_l1_u1_selector_frob_exclusions_and_gaussian_ring_injectivity`
- **Sovereign Rust Witness Anchor**: `sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs::verify_tranche19_ds_qm062_094_101_206_u1_selector_everett_threshold_and_boundary_synthesis_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 25bbbb501bd826d64e5304b7235044a63b218647d94ad13773d4426e9fd619dd`
