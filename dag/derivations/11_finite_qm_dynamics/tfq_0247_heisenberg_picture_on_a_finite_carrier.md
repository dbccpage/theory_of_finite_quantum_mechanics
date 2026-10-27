# [TFQ-0247] Heisenberg picture on a finite carrier

> **Stage**: `FINITE_QM_DYNAMICS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `00357ae4-5bdf-571d-b2c6-bc6dcdb14c37`  
> **Parent Derivation**: [TFQ-0245](tfq_0245_unitary_finite_shadow_slot_still_reserved.md)

---

## 1. Abstract & Formal Statement

QM_041 is a redirect. The opened pages keep a finite-dimensional Heisenberg evolution: for a fixed Hermitian operator and a unitary built as an exponential of that operator, the evolved observable is the conjugate action, and its derivative is the commutator with the generator. The sign depends on the exponential convention, which the paper records rather than hiding. The same redirect sends the history-sum rules to QM_043 and names heisenberg_picture.rs as the implementation home. DS-QM041-HEISENBERG-PICTURE-FINITE is the derivation-graph id.

### Governing Obligation
Conjugate a supplied observable by a supplied finite unitary, and keep the generator and the sign convention as declared data.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `complex matrices (assumption)`
- **Admitted**: `unitary family U(t) and generator H (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> U(t) and H not produced by anything upstream.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm021_040_041_043_commutator_heisenberg_global_weight_and_conditioning`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality`](../../code/lean4/)
- [`sources/atlas/papers/finite_quantum_mechanics/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`external:sha256:d425fe2c91956b215477384bfdbca9273ec86548579684941d9656cc15f3659a::heisenberg_observable`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0248](tfq_0248_finite_history_decoherence_matrix.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM041-HEISENBERG-PICTURE-FINITE`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM041-HEISENBERG-PICTURE-FINITE` (`FINITE_QM_DYNAMICS` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_DYNAMICS-DS-QM041-HEISENBERG-PICTURE-FINITE`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1410, -2820, 2115]`, `chord_potential = 2115`, `holonomy_gamma2 = 2820`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM041-HEISENBERG-PICTURE-FINITE): 4*idx(141) + 3*stage_rank(9) + route_degree(2) == 593` ($\text{value} = 593$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM041-HEISENBERG-PICTURE-FINITE): R_raw(327) - G_cob(159) - S_decoy(9) == 159 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 159$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm021_040_041_043_commutator_heisenberg_global_weight_and_conditioning`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 1bf0e9b9abf926f3cee0439a1a9e8b4138788c812abf6d8b59e91302068d7a6f`
