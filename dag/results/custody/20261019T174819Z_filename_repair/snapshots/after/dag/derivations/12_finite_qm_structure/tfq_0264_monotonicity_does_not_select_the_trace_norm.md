# [TFQ-0264] Monotonicity does not select the trace norm

> **Stage**: `FINITE_QM_STRUCTURE` | **Status**: `SOURCE_RECORD`  
> **UUID**: `eb96554f-1083-5b34-bff4-90061fa310fa`  
> **Parent Derivation**: [TFQ-0263](tfq_0263_trace_norm_under_a_supplied_cptp_family.md)

---

## 1. Abstract & Formal Statement

QM_081 audits transport and states that monotonicity under CPTP maps is necessary and not sufficient to single out trace distance. The opened abstract says a finite counterexample carries two distinct functionals, a trace-norm scale and a positive rescaling, both monotone. Contractivity of trace distance is recorded only after state-discrimination axioms are imported. DS-QM081-CPTP-MONOTONE-NOT-SELECTING is the derivation-graph id, and the segment note says the order runs from an imported CPTP class toward the trace norm, not from the trace norm back to the class.

### Governing Obligation
Refuse to treat CPTP monotonicity by itself as a selection of the trace norm.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Scalar-family non-selection only.

> [!WARNING]
> Operator trace-norm contractivity on M_n(C) not mechanized (upgrade row QM-081-C4).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm081_082_090_093_stochastic_contraction_channel_shadow_firewall_and_cochain`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm081_stochastic_l1_contraction`](../../code/lean4/)
- [`lean4/quantum_mechanics/TraceZeroDuality.lean::monotone_metric_distinct`](../../code/lean4/)
- [`lean4/quantum_mechanics/TraceZeroDuality.lean::scaleMetric_monotone`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_channel.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/trace_norm_certificate.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_ds_qm_dynamics_structure_and_majorana_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM081-CPTP-MONOTONE-NOT-SELECTING`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM081-CPTP-MONOTONE-NOT-SELECTING` (`FINITE_QM_STRUCTURE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-DS-QM081-CPTP-MONOTONE-NOT-SELECTING`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1580, -3160, 2370]`, `chord_potential = 2370`, `holonomy_gamma2 = 3160`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM081-CPTP-MONOTONE-NOT-SELECTING): 4*idx(158) + 3*stage_rank(8) + route_degree(3) == 659` ($\text{value} = 659$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM081-CPTP-MONOTONE-NOT-SELECTING): R_raw(356) - G_cob(174) - S_decoy(8) == 174 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 174$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/TraceZeroDuality.lean::monotone_metric_distinct`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = fa51b9de64c8e1776bbe2de053a9516ad3026dc3b0b8258938d1b5c6778fbd7e`
