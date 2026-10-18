# [TFQ-0007] Finite quantum mechanics core on an admitted carrier

> **Stage**: `FINITE_QM_CORE` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `ca5793f0-74ef-5045-8426-ca1ec4993e6c`  
> **Parent Derivation**: [TFQ-0006](../08_l1_to_l2/TFQ-0006_conditional_finite_hilbert_lift.md)

---

## 1. Abstract & Formal Statement

F001 coordinates finite Hilbert lifts, Born normalization, density-matrix geometry, and dual witness functionals. Its exit contract asks for exact duality-gap certificates, Lean 4 models, and Kraus transport audits. Those artifacts are the work, not a receipt that the work is finished. This gate fixes the order: a finite state, a finite effect, and a pairing on one admitted carrier come before channels, QED, QCD, and gravity. The three languages must name that carrier. Float tolerances do not authorize the pairing.

### Governing Obligation
Fix one finite carrier for states, effects, and pairings before dynamics, gauge theory, or gravity.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Formalization
- **Primary Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure` (zero-axiom, zero-sorry kernel verification in `lean/DerivationDagQMClosure.lean`).

### Sovereign Rust Certifiers
- **Primary Rust Witness**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche16_master_177_node_172_route_dag_completeness_and_operad_audit_witness` (`code/rust/src/dag_witnesses.rs`, exact `i64`/`BigRational` arithmetic).
- **Python PFP Gate Engine**: `omega_engine_pfp/tests/demo_004/finite_qm_derivation_pfp/gates/gate_engine.py::verify_dag_prompt_node_reply` (`G0`..`G6`).

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0008](../11_finite_qm_dynamics/TFQ-0008_finite_dynamics_instruments_and_channels.md)
- [TFQ-0125](../21_implementation_core/TFQ-0125_crate_index_and_derivation_witnesses.md)
- [TFQ-0166](../22_implementation_sibling/TFQ-0166_record_these_sibling_crates_as_controls_under_authorityeffect_none_not_as_completed.md)
- [TFQ-0200](../23_engine_custody/TFQ-0200_three-language_custody_on_the_omega_engine_runtime.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-CARRIER-CONTRACT-V2`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-CARRIER-CONTRACT-V2` (`FINITE_QM_CORE` / `DEFINITION`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_CORE-FQ-CARRIER-CONTRACT-V2`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [970, -1940, 1455]`, `chord_potential = 1455`, `holonomy_gamma2 = 1940`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(FQ-CARRIER-CONTRACT-V2): 4*idx(97) + 3*stage_rank(7) + route_degree(17) == 426` ($\text{value} = 426$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(FQ-CARRIER-CONTRACT-V2): R_raw(229) - G_cob(111) - S_decoy(7) == 111 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 111$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `3` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche16_master_177_node_172_route_dag_completeness_and_operad_audit_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = f1df1f0f341241f290f96a145d8da58e8f8f327e0a843c796500c0d30bdfbf9b`
