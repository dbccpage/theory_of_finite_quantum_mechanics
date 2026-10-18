# [TFQ-0073] Each language must carry: isotony, locality and optional complement duality on a

> **Stage**: `FINITE_QED` | **Status**: `GAP`  
> **UUID**: `f25f3290-ec26-53ba-a375-805b00ca8c4d`  
> **Parent Derivation**: [TFQ-0072](TFQ-0072_each_language_must_carry_channel_amplitude_optical_defect_finite_born_partial_sum.md)

---

## 1. Abstract & Formal Statement

algebraic_qft.rs checks a finite local net and refuses the continuum reading in its own header. try_new requires a declared algebra for every region of one common carrier, including the empty region and its complement. qubit_chain builds the subset net from Pauli supports and refuses more than four parties. defects records an isotony failure when a smaller region is not a subalgebra of a larger one, a locality failure when disjoint regions fail to commute, and, if requested, a duality failure when an algebra is not the commutant of its complement.

### Governing Obligation
Each language must carry: isotony, locality and optional complement duality on a declared finite subset net of at most four parties, and must state that this net is not continuum Haag duality.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `complex field C (assumption)`
- **Admitted**: `continuum Hilbert space (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Z[i] non-field obstruction and discriminant-5 spectral exit from Q(i) are mechanized; continuum Hilbert completion remains an explicit import.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_gap_stone_rational_rotation_infinite_order_and_zi_non_field_obstruction`](../../code/lean4/)
- [`not located`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/algebraic_qft.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche8_tensor_stone_continuum_embedding_and_leftover_mnc_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0074](TFQ-0074_each_language_must_carry_klein-nishina_forward_value_1_thomson_shape_1_u_2_2_s-u.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent`
