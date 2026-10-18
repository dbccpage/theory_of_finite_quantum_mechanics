# [TFQ-0264] Monotonicity does not select the trace norm

> **Stage**: `FINITE_QM_STRUCTURE` | **Status**: `SOURCE_RECORD`  
> **UUID**: `eb96554f-1083-5b34-bff4-90061fa310fa`  
> **Parent Derivation**: [TFQ-0263](TFQ-0263_trace_norm_under_a_supplied_cptp_family.md)

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
