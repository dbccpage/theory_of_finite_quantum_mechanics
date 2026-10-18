# [TFQ-0312] Four necessity verdicts stay open beside the matrix gap

> **Stage**: `FINITE_HILBERT` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `791b42e4-6447-5e86-b8d6-44203ea1dad6`  
> **Parent Derivation**: [TFQ-0311](TFQ-0311_ordinary_matrix_algebra_over_c_is_not_recovered.md)

---

## 1. Abstract & Formal Statement

qm_122_finite_hilbert_boundary_from_primitive_difference.md, in the drop-one census, still marks four necessity verdicts open after the matrix gap is stated: CPTP channels, uniqueness of a Hilbert tensor, the circle group, and a Python dual of the named Lean statements. Gleason uniqueness at n at least 3 is the separate gap already recorded. The finite obligation here is not to upgrade those four open verdicts because a later finish table pairs them with host facts. The paper says that finish table is not a necessity theorem.

### Governing Obligation
Leave CPTP, Hilbert-tensor uniqueness, the circle, and a Python dual as open necessity verdicts.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Gleason: assumption`
- **Admitted**: `circle group: assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> A selector for C / U(1) is not derived here. Detail in QM_028 / QM_062 (other segment).

> [!WARNING]
> The file's own header says candidate only; the status PROVED_LEAN follows the ledger and the existence of named theorems, not a rebuild by me.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011Circle.lean::sign_excluded_circle_still_imported`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011Circle.lean::sign_fails_connectedness_shadow`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011U1SelectorBoundary.lean::selector_not_free`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011U1SelectorBoundary.lean::u1_selector_boundary`](../../code/lean4/)
- [`lean4/quantum_mechanics/H013BornPairingBoundary.lean::born_nonuniqueness_open`](../../code/lean4/)
- [`lean4/quantum_mechanics/H013BornPairingBoundary.lean::pairing_exists`](../../code/lean4/)
- [`lean4/quantum_mechanics/H013BornPairingBoundary.lean::quartic_rival`](../../code/lean4/)
- [`lean4/quantum_mechanics/H013BornPairingBoundary.lean::uniqueness_not_discharged`](../../code/lean4/)
- [`lean4/quantum_mechanics/H017Finish.lean::two_label_host_not_gleason_dimension`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/complex_structure_selector.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/pairing_audit.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/_code/qm_122/qm122_lib/qm122_dual.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0313](TFQ-0313_operator-algebra_shadow_slot_is_still_a_stub.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`
