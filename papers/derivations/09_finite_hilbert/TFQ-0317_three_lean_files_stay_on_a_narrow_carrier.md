# [TFQ-0317] Three Lean files stay on a narrow carrier

> **Stage**: `FINITE_HILBERT` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `00e5569d-d7d9-54f9-af6d-033630b0d8b3`  
> **Parent Derivation**: [TFQ-0316](TFQ-0316_package_chapter_states_a_conditional_lift.md)

---

## 1. Abstract & Formal Statement

The finite obligation is to read the three Lean files as narrow. BornRedundancy.lean works with rational lists: normalization, ray comparison, a coordinate sign defect, and row sparsity. Its header stays inside propositional extensionality, classical choice, and quotient soundness, and it does not express a complex modulus. BornNormalization.lean is a two-level natural-number diagonal density and a binary POVM sum. FiniteQM.lean is a degree-4 polynomial identity on the rational unit sphere and five 2-by-2 import-independence countermodels. None of the three is a finite Hilbert carrier with complex structure.

### Governing Obligation
Cite BornRedundancy, BornNormalization, and FiniteQM only inside the narrow statements they contain.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Born/quadratic readout (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The cited declarations live in lean4/original_lean_20260809/qm_l010_01_born_redundancy.lean (2,215 lines, Mathlib.Tactic import); repo-level lean4/quantum_mechanics copy is Mathlib-free but this extraction did not run a build. Zenodo 20683775 needs the narrowing erratum.

> [!WARNING]
> none for the finite rational statement. Ledger-cited names PaperQF002 / L010_01_BornRedundancy were not found as modules; BornRedundancy.lean (axioms include Classical.choice per its header) is the located home.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/BornNormalization.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/BornRedundancy.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/BornRedundancy.lean::listSum_normalize`](../../code/lean4/)
- [`lean4/quantum_mechanics/BornRedundancy.lean::normalize_idempotent`](../../code/lean4/)
- [`lean4/quantum_mechanics/BornRedundancy.lean::ray_quotient_classification`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition`](../../code/lean4/)
- [`lean4/quantum_mechanics/FiniteQM.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_finite_probability/src/simplex.rs::try_from_weights`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0318](TFQ-0318_float_lift_helper_is_not_the_exact_embedding.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`, `F003`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`
  - `omega_engine_atlas/coda_atlas/F003_omega_engine/floor.yaml`
