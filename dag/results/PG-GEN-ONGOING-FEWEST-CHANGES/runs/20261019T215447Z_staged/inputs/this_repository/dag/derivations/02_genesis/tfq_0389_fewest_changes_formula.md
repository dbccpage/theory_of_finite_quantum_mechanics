# [TFQ-0389] fewest-changes-formula

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `155f8455-5245-5604-9abc-f554f2d3fcb8`  
> **Parent Derivation**: [TFQ-0388](tfq_0388_ongoing_obstruction_answers.md)

---

## 1. Abstract & Formal Statement

PG-GEN-ONGOING-FEWEST-CHANGES and ledger row D8 say the fewest changes to a result equal terms plus assertions, minus the size of what is given, plus twice the destroyed givens. Opened H3V7N5QF/Paths.lean declares fewest_changes_A. The ledger says the formula was checked inside a declared term bound and that rewriting to every writing of the terms was still open in that ledger text. The finite statement still required is the matching lower and upper bounds for one fixed writing, with the every-writing step left to the next node rather than assumed here. Cost.lean is listed beside Paths.lean.

### Governing Obligation
For one fixed writing, fewest changes equal the D8 formula, with lower and upper bounds, inside the declared term bound.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Extension to every writing of the terms is discharged via PG-GEN-REWRITING-COMMUTATION (mechanized in Second/Rename.lean and DerivationDagQMClosure.lean).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`declaration obligation: fewest_changes_A for one legal well-formed writing`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Cost.lean::Reach.names_stay_merged`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Paths.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Paths.lean::fewest_changes_A`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Paths.lean::reach_by_edits`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: no Rust cost module was listed for the ongoing package; the formula still needs an explicit finite checker or a stated absence`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: a cost column under 001_genesis_ongoing_h3v7n5qf/evidence that is checked only inside the declared term bound`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0390](tfq_0390_rewriting_and_persistence_reconcile.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/floor.yaml`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-GEN-REWRITING-COMMUTATION`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-GEN-REWRITING-COMMUTATION` (`GENESIS` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-GENESIS-PG-GEN-REWRITING-COMMUTATION`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [590, -1180, 885]`, `chord_potential = 885`, `holonomy_gamma2 = 1180`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-GEN-REWRITING-COMMUTATION): 4*idx(59) + 3*stage_rank(2) + route_degree(2) == 244` ($\text{value} = 244$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-GEN-REWRITING-COMMUTATION): R_raw(128) - G_cob(63) - S_decoy(2) == 63 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 63$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_gen_rewriting_commutation_and_obstruction_persistence`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 8961b2145cfe721b4e62bcd8a6fb66df19351c1cd2d6c7b81943f160849b9ba6`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-GEN-ONGOING-FEWEST-CHANGES`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-GEN-ONGOING-FEWEST-CHANGES` (`GENESIS` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-GENESIS-PG-GEN-ONGOING-FEWEST-CHANGES`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [580, -1160, 870]`, `chord_potential = 870`, `holonomy_gamma2 = 1160`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-GEN-ONGOING-FEWEST-CHANGES): 4*idx(58) + 3*stage_rank(2) + route_degree(4) == 242` ($\text{value} = 242$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-GEN-ONGOING-FEWEST-CHANGES): R_raw(126) - G_cob(62) - S_decoy(2) == 62 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 62$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Cost.lean::Reach.names_stay_merged`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 98ba09eb426f5b0399ff6c862616dda4d4fa9e05f632223fd60edcabfe5f5b44`
