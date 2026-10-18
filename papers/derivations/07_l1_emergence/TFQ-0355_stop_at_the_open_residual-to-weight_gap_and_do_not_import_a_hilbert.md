# [TFQ-0355] Stop at the open residual-to-weight gap and do not import a Hilbert

> **Stage**: `L1_EMERGENCE` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `3d7f91c4-f456-585f-8eac-df5bd38c00b1`  
> **Parent Derivation**: [TFQ-0354](TFQ-0354_do_not_derive_declared_l1_sector_weights_from_the_phi1_and_gamma2.md)

---

## 1. Abstract & Formal Statement

The slice stops before the Hilbert lift. DAG node L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY and the imported-structure nodes for a complex field, circle phases, an inner product, orthogonal additivity, Haar phases, and linear isometric dynamics are outside this tree. Node L1-DENSITY-LIFT-SIGNED-SQRT-PUB009 is also outside: its statement uses real square roots and a trace norm on real symmetric matrices. O04 in the bridge register still asks for scalar and Hilbert choices to be justified, and classical, signed, and realification alternatives remain live.

### Governing Obligation
Stop at the open residual-to-weight gap and do not import a Hilbert inner product, a complex field, or the signed-sqrt density lift in this slice.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `complex scalars with modulus: lift`
- **Admitted**: `free linearization coefficient pack: assumption`
- **Admitted**: `inner product: assumption`
- **Admitted**: `real square roots (real field): lift`
- **Admitted**: `square root field: lift`
- **Admitted**: `trace norm on real symmetric matrices: lift`
- **Admitted**: `unit phases: lift`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> No Lean theorem for |c|^2 normalization over C found; BornNormalization.lean treats discrete 2x2 density / POVM. Rust exact_amplitudes returns None unless every p_j is a rational square.

> [!WARNING]
> Prose proofs of the strict bound are not in Lean. Rust xi.rs uses f64 (XiResult::value returns f64), so it is numeric evidence only. Lean symbols in Xi.lean not individually grepped.

> [!WARNING]
> Uniqueness of the inner product is not available.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/BornNormalization.lean::born_normalization_redundancy`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm020_thm4_hilbert_lift_redundancy`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.signed_sqrt_density_lift_cauchy_schwarz`](../../code/lean4/)
- [`lean4/quantum_mechanics/H005InnerProductAdmission.lean::gram_not_unique`](../../code/lean4/)
- [`lean4/quantum_mechanics/H005InnerProductAdmission.lean::inner_product_admission`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/009_conditional_density_lift_and_dual_witness_xi_functional/lean4/Xi.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_functional/src/xi.rs::DensityLift`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_functional/src/xi.rs::XiResult`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/hilbert_space.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mass_phase_embedding.rs::born_weights`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mass_phase_embedding.rs::exact_amplitudes`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_l1_sector_weights_and_density_lift_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_l1_to_l2_bridges_and_ladder_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:
