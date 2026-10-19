# [TFQ-0181] Keep omega_majorana a GF(2) diagnostic and do not treat it as an

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `b52b525c-5784-5264-9715-036cbb08b19b`  
> **Parent Derivation**: [TFQ-0166](tfq_0166_record_these_sibling_crates_as_controls_under_authorityeffect_none_not_as_completed.md)

---

## 1. Abstract & Formal Statement

omega_majorana is a GF(2) diagnostic, not an authority terminal. src/lib.rs titles the crate a GF(2) Majorana parity diagnostic playground, sets AuthorityEffect None on every receipt, and says it does not mint CertifiedAuthority and does not claim physical Majorana modes, topological qubits, or NISQ hardware. Status labels Exact, ClosedResidual, and OpenObstruction are diagnostic schedule classes, not FOC ExactRepair. The obligation is to cite the crate only as that diagnostic. derivation_dag.json id DS-QM212-MAJORANA-PROBLEM names lib.rs, but that citation does not lift the fence written in the file.

### Governing Obligation
Keep omega_majorana a GF(2) diagnostic and do not treat it as an authority terminal.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Finite Majorana Clifford parity algebra and tetron braid/parity checks are mechanized; experimental device noise models remain external.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm102_110_111_212_syndrome_hamming_lqg_wilson_and_majorana_braid`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm212_majorana_clifford_relations`](../../code/lean4/)
- [`not located`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_majorana/src/lib.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_ds_qm_dynamics_structure_and_majorana_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/009_ms_majorana/code/majorana_gf2_diagnostic.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0182](tfq_0182_treat_gf_2_terminalize_receipts_as_diagnostic_schedule_classes_not_as_minted_authority.md)
- [TFQ-0183](tfq_0183_do_not_promote_tetron_rs_physical_wording_past_the_gf_2_diagnostic_fence_in.md)
- [TFQ-0184](tfq_0184_do_not_read_paper_009_reflexivity_declarations_as_measured_tetron_homology.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM212-MAJORANA-PROBLEM`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM212-MAJORANA-PROBLEM` (`FINITE_QM_STRUCTURE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-DS-QM212-MAJORANA-PROBLEM`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1740, -3480, 2610]`, `chord_potential = 2610`, `holonomy_gamma2 = 3480`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM212-MAJORANA-PROBLEM): 4*idx(174) + 3*stage_rank(8) + route_degree(2) == 722` ($\text{value} = 722$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM212-MAJORANA-PROBLEM): R_raw(388) - G_cob(190) - S_decoy(8) == 190 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 190$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm102_110_111_212_syndrome_hamming_lqg_wilson_and_majorana_braid`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = d573819a6844e67c349b255f1e273d5d53248f4e295b62ace5bda30c6189b0b5`
