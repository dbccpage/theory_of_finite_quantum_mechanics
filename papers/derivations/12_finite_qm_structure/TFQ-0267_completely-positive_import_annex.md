# [TFQ-0267] Completely-positive import annex

> **Stage**: `FINITE_QM_STRUCTURE` | **Status**: `SOURCE_RECORD`  
> **UUID**: `903dacf1-9488-5bd2-9c29-97b5153811e3`  
> **Parent Derivation**: [TFQ-0266](TFQ-0266_no_derivation_from_stochastic_kernels_to_complete_positivity.md)

---

## 1. Abstract & Formal Statement

QM_083 is an annex redirect onto QM_082. The opened rules say not to mint an independent public theorem at this root, and that historical claim identifiers remain only for packaging. The annex role is the completely-positive and Kraus import fence. Because the stem already withholds a derivation from kernels to complete positivity, this node adds no second channel law and no second tolerance. DS-QM064-074-083-ANNEX-REDIRECT-ROWS is the derivation-graph id that groups the redirect.

### Governing Obligation
Redirect completely-positive import claims to QM_082 and add no independent channel theorem at the annex.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `complete positivity (assumption)`
- **Admitted**: `environment extension (assumption)`
- **Admitted**: `tensor product with identity (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Mechanized directly in DerivationDagQMClosure.lean and bound to Rust witness.

> [!WARNING]
> Open upgrade row: when off-diagonal transport is admissible.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_and_fq_cptp_partial_transpose_born_lp_and_f64_diagnostic_firewall`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm064_triangle_holonomy_gauge_invariant`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm081_stochastic_l1_contraction`](../../code/lean4/)
- [`lean4/quantum_mechanics/H063CptpChannelsStinespring.lean::stinespring_requires_extension_verified`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_ds_qm_dynamics_structure_and_majorana_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM064-074-083-ANNEX-REDIRECT-ROWS`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM064-074-083-ANNEX-REDIRECT-ROWS` (`FINITE_QM_STRUCTURE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-DS-QM064-074-083-ANNEX-REDIRECT-ROWS`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1490, -2980, 2235]`, `chord_potential = 2235`, `holonomy_gamma2 = 2980`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM064-074-083-ANNEX-REDIRECT-ROWS): 4*idx(149) + 3*stage_rank(8) + route_degree(2) == 622` ($\text{value} = 622$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM064-074-083-ANNEX-REDIRECT-ROWS): R_raw(338) - G_cob(165) - S_decoy(8) == 165 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 165$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm081_stochastic_l1_contraction`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = c9e237ad331688801780b909b1dde5c227f7c744b065c75395c2a5450b31049f`
