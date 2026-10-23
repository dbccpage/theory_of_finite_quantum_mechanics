# [TFQ-0477] go-reach-ceiling

> **Stage**: `GENESIS` | **Status**: `PROVED_LEAN`  
> **UUID**: `97908fda-7b94-5274-864e-6c5c4f8f852f`  
> **Parent Derivation**: [TFQ-0389](tfq_0389_fewest_changes_formula.md)

---

## 1. Abstract & Formal Statement

In the base genesis-ongoing seed (terms a and b, arb asserted, xrx forbidden; the changes are identification, removal, adding a term and adding an assertion), ledger row D9 says every finite legal state with at least one term, names anywhere, is a result under either beginning. The Lean edit path reach_by_edits reaches a legal well-formed goal that contains the start's terms and keeps its names, by removing what the goal does not assert, adding the missing terms and adding the missing assertions, in that many changes; givenA_to_oneTerm and givenB_to_oneTerm reach the one-term result in two and three changes. Row N5 is the expressive ceiling that follows from D9: no statement about the asserting that holds in one finite legal state and fails in another follows from the seed.

### Governing Obligation
Exhibit for every finite legal state with a term an edit path from either beginning of length removals plus added terms plus added assertions, and read N5 from it.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared exploration bound C8 (at most 5 terms FREE, 4 terms ANCHORED) for the computed half of D9 (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The Lean witnesses fix the names at a = 0, b = 1 or a = b = 0; names elsewhere rest on the rewriting step that ledger row O3 tracks (TFQ-0390), and the computed half of D9 stops at the declared term bound.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/GenesisOngoing/H3V7N5QF/Paths.lean::givenA_to_oneTerm`](../../../lean4/Imported/GenesisOngoing/H3V7N5QF/Paths.lean)
- [`lean4/Imported/GenesisOngoing/H3V7N5QF/Paths.lean::givenB_to_oneTerm`](../../../lean4/Imported/GenesisOngoing/H3V7N5QF/Paths.lean)
- [`lean4/Imported/GenesisOngoing/H3V7N5QF/Paths.lean::reach_by_edits`](../../../lean4/Imported/GenesisOngoing/H3V7N5QF/Paths.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: the H3V7N5QF package holds no Rust`

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/xry/explore.py::explore`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/xry/explore.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0478](tfq_0478_go_contraction_step2_step3.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/claim_ledger.md:44`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/claim_ledger.md:82`
  - `omega_engine_education/documentation/005_oegenong/levels/level_07_graph_reachability_closure.md:33`
