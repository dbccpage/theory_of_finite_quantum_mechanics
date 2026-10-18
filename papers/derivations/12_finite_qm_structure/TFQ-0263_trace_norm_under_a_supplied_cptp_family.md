# [TFQ-0263] Trace norm under a supplied CPTP family

> **Stage**: `FINITE_QM_STRUCTURE` | **Status**: `SOURCE_RECORD`  
> **UUID**: `cb38f3cf-c630-5ced-a714-9904a0b91f99`  
> **Parent Derivation**: [TFQ-0262](TFQ-0262_cptp_class_recorded_as_a_definition.md)

---

## 1. Abstract & Formal Statement

QM_080 obliges trace-norm geometry only as CPTP-compatible, not as selected by monotonicity alone. The corrected title says monotonicity is necessary for the trace-distance gauge and not sufficient to select it. Finite Quantum Mechanics section 11.3 states the conditional result that was read: if every CPTP map between matrix algebras fails to increase a family of norms on trace-zero Hermitian matrices, then those norms are one positive multiple of the trace norm. The text says this is a result on the full stated channel and matrix domain, not a selection of that domain from primitive difference.

### Governing Obligation
Attach the trace-norm multiple to the hypothesis that every map in the stated CPTP class is monotone, and do not drop that hypothesis.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `CPTP maps (assumption)`
- **Admitted**: `complex matrices and full CPTP class (assumption)`
- **Admitted**: `density matrices and M_n(C) (assumption)`
- **Admitted**: `spectral theorem (assumption)`
- **Admitted**: `spectral theorem for the matrix lift (assumption)`
- **Admitted**: `tensor product (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> No Lean statement of the uniqueness-up-to-scale theorem found; TraceZeroDuality.lean item 3 states only that c||.||_1 is monotone for every c > 0. Rust certifies trace norms of given Hermitian matrices over Q(i), not the theorem.

> [!WARNING]
> Spectral selection theorem has no Lean (NOT-STARTED); duplicates FQ-TRACE-NORM-FROM-CPTP-MONOTONICITY in the other fragment.

> [!WARNING]
> Overlaps FQ trace-norm nodes in the other fragment.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.trace_zero_pinching_contraction`](../../code/lean4/)
- [`lean4/quantum_mechanics/DualWitness.lean::dual_witness_certifies_trace_distance`](../../code/lean4/)
- [`lean4/quantum_mechanics/TraceZeroDuality.lean::trace_zero_duality_gap_zero`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/exact_channel.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/trace_norm_certificate.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/trace_norm_certificate.rs::TraceNormCertificate`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_ds_qm_dynamics_structure_and_majorana_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_fq_core_and_k23_duality_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0264](TFQ-0264_monotonicity_does_not_select_the_trace_norm.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
