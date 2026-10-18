# [TFQ-0365] collapsed-observation-barrier

> **Stage**: `PREGENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `d9859fc8-43ad-53a4-903d-2fdeb98dfcca`  
> **Parent Derivation**: [TFQ-0364](TFQ-0364_three-trial-record-bound.md)

---

## 1. Abstract & Formal Statement

PG-COLLAPSE-BARRIER records that if two data have equal profiles, no function of that collapsed quotient separates them. Pre-Genesis paper.md section 5 is the DAG source span, and historical row WDP-P000-004 states the written proposition that a task separating a collapsed pair cannot factor through the current quotient. Opened Paper.lean declares collapsed_observation_barrier. The finite statement still required is that separation of one collapsed pair needs an added instance or tag outside the quotient. Chapter 4 of the S000 book says two marks do not supply a report map.

### Governing Obligation
Equal profiles yield no separating function of the collapsed quotient; separation needs data outside that quotient.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Axiom report: see lean4/axiom_report.txt lines 2264-3280 (not individually re-read for this node).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`declaration obligation: collapsed_observation_barrier stays tied to equal profiles and does not invent a separating tag`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean::collapsed_observation_barrier`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: a quotient-barrier check in crate pre_mssn_preservation`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/rust/src/main.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: a counterexample beside preservation.refine where equal reports yield no separating function`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/preservation.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0366](TFQ-0366_history-report-fiber-criterion.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/book/ch04_report_maps_fibers_quotients_and_sections.md`
