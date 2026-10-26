# [TFQ-0426] replay-necessity

> **Stage**: `PREGENESIS` | **Status**: `PROVED_LEAN`  
> **UUID**: `6d93266a-fad6-538f-a44f-e8ad235d7b4b`  
> **Parent Derivation**: [TFQ-0364](tfq_0364_three_trial_record_bound.md)

---

## 1. Abstract & Formal Statement

Let H be the possible histories, σ(h) the state that history h produces and π(h) the part of h an auditor sees, for example only the last turn. If π(h₁) = π(h₂) but σ(h₁) ≠ σ(h₂), no auditor A that sees only π reports σ(h) for every h, because A(π(h₁)) = A(π(h₂)) would give σ(h₁) = σ(h₂). The trial failures motivate the theorem: the blind auditor flagged the licensed words 'We' (Trial 1) and 'rule' (Trial 2) as imports, so an audit needs two levels; in Trial 2, Prompt 14's false attribution was answered without objection, so claim provenance is a check separate from claim correctness, Result 15 lost the state, saying the regime contains only <> after <a> had been supplied; and the two-level auditor, shown only that turn, answered None. State certification therefore needs replay information that separates the relevant histories, and on a declared finite population a summary on which σ is constant per fiber of the view can stand in for the raw history.

### Governing Obligation
Reject any auditor that certifies the adopted state from a view π under which two admissible histories with different states coincide, and give it the replayed history or a summary on which σ is constant per fiber.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Further Prerequisites
- [TFQ-0365](tfq_0365_collapsed_observation_barrier.md) collapsed-observation-barrier
- [TFQ-0366](tfq_0366_history_report_fiber_criterion.md) history-report-fiber-criterion

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The trial contrasts motivate the theorem and do not instantiate it: the truncated window and the full replay received different inputs, so they are not a checked pair with equal auditor views; raw history retention is a provenance policy, and task-sufficient reconstruction is the mathematical requirement.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/Paper000.lean::insufficient_history_view`](../../../lean4/Imported/Genesis19l57g1/Paper000.lean)
- [`lean4/Imported/Genesis19l57g1/Paper000.lean::no_factor_through_common_view`](../../../lean4/Imported/Genesis19l57g1/Paper000.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/code/rust/src/main.rs::factor`](../../../atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/code/rust/src/main.rs)

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/genesis/code/genesis_checks.py::history_auditor`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/genesis_checks.py)
- [`atlas/papers/finite_obstruction_calculus/genesis/code/tests/test_genesis_checks.py::test_quotient_and_history_refuse_collapsed_answers`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/tests/test_genesis_checks.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0427](tfq_0427_context_fidelity.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_education/documentation/000_oepregen/sources/analysis_derivation_v1.md:1009-1047`
  - `omega_engine_education/documentation/000_oepregen/03_results_and_arguments.md:100-106`
  - `omega_engine_education/documentation/000_oepregen/02_trial_record.md:101-111`
