# [TFQ-0305] Sector weights do not force the quadratic form

> **Stage**: `L1_TO_L2` | **Status**: `SOURCE_RECORD`  
> **UUID**: `e1ac77e5-11d6-5ed6-b319-2e8024610db8`  
> **Parent Derivation**: [TFQ-0304](tfq_0304_lift_capacity_is_not_a_dynamics_derivation.md)

---

## 1. Abstract & Formal Statement

The section labeled Theorem 6, part 1, in qm_020_born_normalization_and_conditional_hilbert_lift.md is a scope fence: additive sector weights already give a unit-sum profile and do not force a complex vector space, an inner product, phases, unitary dynamics, projectors, POVMs, interference, or a measurement lattice. The finite obligation is to keep those alternatives on the record. The same weights can be left as the classical profile, or encoded with real signed amplitudes, or given some other redundant encoding. The claim ledger types this part as a scope fence.

### Governing Obligation
State that l1 weights do not force the quadratic Born form, and stop at that fence.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The Lean declaration originally cited was a True stub per the audit. H013BornPairingBoundary.lean is a candidate (header: Candidate only. Not PROVEN. Kind: IMPORT BOUNDARY), not a mechanization of this Part 1.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/BornRedundancy.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm020_thm6_p1_scope_fence`](../../code/lean4/)
- [`lean4/quantum_mechanics/H013BornPairingBoundary.lean::born_nonuniqueness_open`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/pairing_audit.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_l1_to_l2_bridges_and_ladder_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/_code/qm_020/code/qm_020_born_normalization_and_conditional_hilbert_lift_core.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0306](tfq_0306_born_uniqueness_stays_an_imported_boundary.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-QM020-THM6-P1-SCOPE-FENCE`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-QM020-THM6-P1-SCOPE-FENCE` (`L1_TO_L2` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-L1_TO_L2-L1-QM020-THM6-P1-SCOPE-FENCE`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [860, -1720, 1290]`, `chord_potential = 1290`, `holonomy_gamma2 = 1720`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(L1-QM020-THM6-P1-SCOPE-FENCE): 4*idx(86) + 3*stage_rank(6) + route_degree(3) == 365` ($\text{value} = 365$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(L1-QM020-THM6-P1-SCOPE-FENCE): R_raw(202) - G_cob(98) - S_decoy(6) == 98 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 98$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm020_thm6_p1_scope_fence`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_l1_to_l2_bridges_and_ladder_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 96cbf58738acf6615765fe837f1b7e3a3b53ae2d2096adb9e587b171ac83e7ce`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM204-BORN-UNIQUENESS-IMPORT-BOUNDARY`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM204-BORN-UNIQUENESS-IMPORT-BOUNDARY` (`FINITE_QM_STRUCTURE` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-DS-BORN-LP-RIVAL-BOUNDARY`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [190, -380, 285]`, `chord_potential = 285`, `holonomy_gamma2 = 380`
- **Finite Shadow Exact Witness (`M4`)**: `born_l2_pairing_3_4: 3^2 + 4^2 == 25` ($\text{value} = 25$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quartic_rival_minus_born_l2: (3^4 + 4^4) - (3^2 + 4^2) = 337 - 25 == 312 (valid L^4 measure pairing differs by 312)` ($\text{value} = 312$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_and_fq_cptp_partial_transpose_born_lp_and_f64_diagnostic_firewall`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 99a067b813765b36860b763b2b0dff609434c74d277c0bcdef05a2edc2ab18e8`
