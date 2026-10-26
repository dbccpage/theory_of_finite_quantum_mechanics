# [TFQ-0436] context-count-formula

> **Stage**: `GENESIS` | **Status**: `PROVED_LEAN`  
> **UUID**: `2fa455df-5c68-5adb-9ca9-bdf32979728c`  
> **Parent Derivation**: [TFQ-0433](tfq_0433_contexts_plugging_profiles.md)

---

## 1. Abstract & Formal Statement

For a regime with n admitted data, a form of arity a has (n+1)^a − n^a well-formed contexts: each slot is a hole or one of n data, less the n^a hole-free tuples, so |Ctx(R)| = Σ_f ((n+1)^{a_f} − n^{a_f}), with distinct form identifiers kept disjoint even when their arities coincide. The companion Lean module establishes the per-form count for the recursive word enumeration (contextWords_length), characterizes its members as exactly the well-formed words of that length containing a hole (contextWords_mem), and shows the enumeration has no repetitions (contextWords_nodup). The standalone replay checks the formula against the frozen Python enumeration in 35 cases (n from 0 to 4, arity 1 to 7), and Python and Rust enumerate the contexts independently.

### Governing Obligation
Count the contexts of each admitted form as (n+1)^a − n^a, sum over forms, and check the count against an explicit context enumeration.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The Lean statement is a companion result for the slot words of one form; the sum over forms is the written corollary of ledger row WDP-P000-015, which attributes it to no compiled source theorem, and large arities make profile enumeration expensive.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/Paper.lean::contextWords_length`](../../../lean4/Imported/Genesis19l57g1/Paper.lean)
- [`lean4/Imported/Genesis19l57g1/Paper.lean::contextWords_mem`](../../../lean4/Imported/Genesis19l57g1/Paper.lean)
- [`lean4/Imported/Genesis19l57g1/Paper.lean::contextWords_nodup`](../../../lean4/Imported/Genesis19l57g1/Paper.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/context.rs::a_binary_form_over_two_data_has_five_contexts` (private upstream source, not in this repository)
- `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/context.rs::contexts` (private upstream source, not in this repository)

### Python Oracles & Numerical Evaluators
- `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/observe.py::contexts` (private upstream source, not in this repository)
- `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/reproduce.py::python_replay` (private upstream source, not in this repository)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md:258-261`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/fixtures/historical_claim_ledger.md:26`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md:603-604`
