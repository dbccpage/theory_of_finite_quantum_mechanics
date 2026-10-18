# [TFQ-0188] Refuse the f64 lift_scale on CycleLiftSpec as a licence for an exact

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `GAP`  
> **UUID**: `8872f729-8203-5290-891d-5a3032139b2f`  
> **Parent Derivation**: [TFQ-0187](TFQ-0187_keep_lift_licences_as_descent-paired_obstruction_metadata_not_as_a_hilbert_derivation.md)

---

## 1. Abstract & Formal Statement

CycleLiftSpec breaks the exact-licence story by storing lift_scale as f64. src/cycle_lift_spec.rs declares cycle_node_indices as a vector of usize and lift_scale as f64, and its error NonFiniteLiftScale only rejects a non-finite float. That is not a BigRational descent witness. FQ-IMPL-F64-GATING counts three omega_lifts files in legacy_debt and says a float may propose but never authorize a result. The obligation is to refuse this f64 scale as a lift licence. PrimitiveLiftCertificate.lean is only a boolean checklist of propositions and does not supply the missing exact scale.

### Governing Obligation
Refuse the f64 lift_scale on CycleLiftSpec as a licence for an exact finite lift.

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
- [`lean4/quantum_mechanics/PrimitiveLiftCertificate.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_lifts/src/cycle_lift_result.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_lifts/src/cycle_lift_spec.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_lifts/src/lift_primitive.rs`](../../code/rust/src/)
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

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/shelf.yaml`
