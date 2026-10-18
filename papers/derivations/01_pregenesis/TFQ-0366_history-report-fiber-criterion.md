# [TFQ-0366] history-report-fiber-criterion

> **Stage**: `PREGENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `a6075523-4bdf-5bde-987e-6b0cbaba4a64`  
> **Parent Derivation**: [TFQ-0365](TFQ-0365_collapsed-observation-barrier.md)

---

## 1. Abstract & Formal Statement

Opened PreMssn.history_report_criterion in 000_pre_genesis_to_mssn/lean4/Paper.lean says a question factors through the report image exactly when it is constant on report fibers, and the file header says Classical.choice is used for arbitrary report images. history_factor_unique is the companion declaration. DAG node PG-HISTORY-REPORT-CRITERION and ledger rows WDP-P000-005 and WDP-P001-018 record that image-restricted criterion. The finite statement still required is to keep the choice-using direction for unlisted images separate from a listed population.

### Governing Obligation
A question over histories factors through the realized report image exactly when it is constant on report fibers, and the factor is unique on that image.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Classical.choice (assumption: in Paper.lean, per its header comment)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Constructive version for explicitly listed histories is the Fable 04 target (PG-PREGEN-CONSTRUCTIVE-SUMMARY).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`declaration obligation: history_report_criterion and history_factor_unique, with Classical.choice left visible on the unlisted direction`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean::history_factor_unique`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean::history_report_criterion`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Descent.lean::function_descends_iff_fiber_constant`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/ProposalAdmissionBridge.lean::factorization_iff_fiber_constancy`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::descent_unique`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::exists_descent_of_constant`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: a report-factor checker in crate pre_mssn_preservation that refuses answers outside the realized image`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_category_theory/src/finite_report_query.rs::FactorizationCertificate`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: preservation.report_factor must be checked against fiber constancy and must return no factor off the image`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/preservation.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0367](TFQ-0367_listed-history-choice-free-summary.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/book/ch05_descent_versus_selected_representatives.md`
