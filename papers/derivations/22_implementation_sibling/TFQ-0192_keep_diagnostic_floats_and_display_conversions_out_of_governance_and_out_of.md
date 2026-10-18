# [TFQ-0192] Keep diagnostic floats and display conversions out of governance and out of

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `3e798744-bc10-52c3-bfa6-b57153d314d2`  
> **Parent Derivation**: [TFQ-0189](TFQ-0189_keep_exact_rational_measurement_evidence_distinct_and_free_of_float_authority.md)

---

## 1. Abstract & Formal Statement

Diagnostic floats are a fourth arm and are barred from governance even when a display conversion exists. MeasurementValue::DiagnosticFloat carries an f64 plus a DiagnosticPurpose limited to logging or visualization. MeasurementError variants RawF64ForbiddenInGovernance and DiagnosticFloatForbiddenInGovernance name the refusal. try_to_f64_for_display is documented as forbidden for governance decisions. The obligation is to leave that display path outside every licence, probability, and MUB certificate. FQ-IMPL-F64-GATING counts two omega_measurement files in legacy_debt.

### Governing Obligation
Keep diagnostic floats and display conversions out of governance and out of exact certificates.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `floating point as diagnostic only (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Exact faces use BigRational/Q(i)/Q(zeta_n); f64 faces are legacy debt, not agreed use. Which quantum_physics results still route through f64 is not audited here.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_and_fq_cptp_partial_transpose_born_lp_and_f64_diagnostic_firewall`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_impl_amplitude_realification_and_pairing_bridges`](../../code/lean4/)
- [`not located`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_measurement/src/documentary_traceability.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_measurement/src/measurement_access.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_measurement/src/measurement_kernel.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/engine_bridge.rs::DiagnosticBridgeError`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
