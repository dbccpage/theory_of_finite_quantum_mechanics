# [TFQ-0249] Trace-zero summaries do not fix commutation

> **Stage**: `FINITE_QM_STRUCTURE` | **Status**: `SOURCE_RECORD`  
> **UUID**: `8ea3e4b4-211c-54e0-b0fd-6e21ad75e376`  
> **Parent Derivation**: [TFQ-0245](../11_finite_qm_dynamics/TFQ-0245_unitary_finite-shadow_slot_still_reserved.md)

---

## 1. Abstract & Formal Statement

QM_040 is a redirect whose surviving content is one Gaussian-integer example, not a matrix-versus-differential-equation correspondence. The opened pages embed three Pauli matrices into three-by-three matrices, note that each has trace zero, and note that the commutators are still nonzero and match the su(2) relations. The operational reading is observer information loss: a trace-zero local summary does not determine whether the operators commute. DS-QM040-GAUSSINT-LAMBDA-COMMUTATOR-WITNESS is the derivation-graph id. The obligation sits beside the unfinished unitary and Hamiltonian slots.

### Governing Obligation
Keep the Gaussian-integer commutator witness as a finite counterexample to reading trace zero as commutation, without a continuum equation.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Gaussian integer entries Z[i] (assumption); Z[i] is not a field`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> LEAN_BOUND file not verified by me.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm021_040_041_043_commutator_heisenberg_global_weight_and_conditioning`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm040_commutator_nonzero_and_trace_zero`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_ds_qm_dynamics_structure_and_majorana_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0250](TFQ-0250_mermin-peres_contextuality_on_a_finite_cochain.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM040-GAUSSINT-LAMBDA-COMMUTATOR-WITNESS`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM040-GAUSSINT-LAMBDA-COMMUTATOR-WITNESS` (`FINITE_QM_DYNAMICS` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_DYNAMICS-DS-QM040-GAUSSINT-LAMBDA-COMMUTATOR-WITNESS`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1400, -2800, 2100]`, `chord_potential = 2100`, `holonomy_gamma2 = 2800`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM040-GAUSSINT-LAMBDA-COMMUTATOR-WITNESS): 4*idx(140) + 3*stage_rank(9) + route_degree(2) == 589` ($\text{value} = 589$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM040-GAUSSINT-LAMBDA-COMMUTATOR-WITNESS): R_raw(325) - G_cob(158) - S_decoy(9) == 158 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 158$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm021_040_041_043_commutator_heisenberg_global_weight_and_conditioning`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = bc58f9bf456feb2c058429396ab9944cf9e8e1373c556350811a7433a52fa376`
