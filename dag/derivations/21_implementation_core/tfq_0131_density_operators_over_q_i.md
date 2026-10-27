# [TFQ-0131] Density operators over Q(i)

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `cad05840-f131-5526-a70e-978ef2e0bbcb`  
> **Parent Derivation**: [TFQ-0129](tfq_0129_exact_rays_and_pure_states.md)

---

## 1. Abstract & Formal Statement

Covers density_matrix.rs, exact_hermitian.rs, packed_hermitian.rs, residual_density_calculus.rs, and exact_operator.rs. density_matrix.rs admits ExactDensityMatrix only when the Q(i) matrix is Hermitian, positive semidefinite by exact LDL, and of trace 1. Mixtures, partial traces, and channel actions are revalidated. The population shadow is the diagonal, not the state. The other files carry Hermitian admission, packed physical storage, pointer-sector updates, and the exact real spectrum. A Python replay and a Lean 4 declaration would still have to match that admission gate and the shadow split.

### Governing Obligation
Match Hermitian, exact-LDL, trace-one admission and the split between a density and its population shadow.

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
- [`external:sha256:a9858061f68a9165aeb743a82864df532a5026453c94ca6eed5b5a7b4a704499`](../../code/rust/src/)
- [`external:sha256:a9fd670f9cb50b43c77a2353570f76a49b6416ce82e53371978297e66620dd8e`](../../code/rust/src/)
- [`external:sha256:d8a797c3e2b79dea816a3ec3cffb85eb0179b327e0ffd5f08789bd59d72829a6`](../../code/rust/src/)
- [`external:sha256:fb191f3f4dd0d504f69d2f792adf83dc6dfb0b7196e5d1eb498bb454f336f338`](../../code/rust/src/)
- [`external:sha256:91902ad0b3daed220b6cb851493f83faf8fe90131ef5b3e5e3260cc721968c14`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`external:sha256:e5884d1527023af19775b9c000a135a80f4ba943367af9afd1981840489029ef`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0132](tfq_0132_trace_norm_certificates.md)
- [TFQ-0133](tfq_0133_observables_and_local_star_algebras.md)
- [TFQ-0154](tfq_0154_canonical_mub_inversion.md)
- [TFQ-0160](tfq_0160_import_finite_maps_qm_207_to_qm_215.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-IMPL-REALIFICATION-ADAPTER`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-IMPL-REALIFICATION-ADAPTER` (`IMPLEMENTATION` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-IMPLEMENTATION-FQ-IMPL-REALIFICATION-ADAPTER`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1280, -2560, 1920]`, `chord_potential = 1920`, `holonomy_gamma2 = 2560`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(FQ-IMPL-REALIFICATION-ADAPTER): 4*idx(128) + 3*stage_rank(10) + route_degree(4) == 546` ($\text{value} = 546$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(FQ-IMPL-REALIFICATION-ADAPTER): R_raw(306) - G_cob(148) - S_decoy(10) == 148 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 148$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_impl_wdp_amplitude_realification_pairing_and_gauss_matrix_algebra`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_fq_core_and_k23_duality_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 1c56a98cc8cf257130cd64356714a78d4a73d6560cd1967d2996270a706d64d7`
