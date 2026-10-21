# [TFQ-0449] closed-baseline-terminates

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `7e838afc-09e9-550d-92f3-040a0cea91c5`  
> **Parent Derivation**: [TFQ-0383](tfq_0383_closure_round_inequality.md)

---

## 1. Abstract & Formal Statement

With the external continuation policy disabled, the closed-system baselines are small: reading L has 4 nodes and 3 terminal branches, reading F has 20 nodes and 16 terminal branches, and both have zero guard-cut, round-cut and open branches. Every maximal branch ends at the all-pairs-separated fixpoint within the pair bound, using 1 round in L (bound 1) and 3 in F (bound 3), and the termination flag is computed over all maximal branches rather than from one terminal node. Under the declared round shape a closed run from an empty requirement store makes at most n(n−1)/2 rounds (closedRun_round_bound_from_empty).

### Governing Obligation
Regenerate both closed-system baselines and report node counts, terminal branches and rounds used, with every maximal branch terminal within the n(n−1)/2 pair bound.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared resource bounds of genesis_source.txt section 1 with the external continuation policy disabled (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> A bounded theorem: termination of every maximal branch is computed within the declared bounds, and that each exported round has the declared shape (one fresh imposition, no fresh-datum item) stays computational.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Rounds.lean::closedRun_round_bound_from_empty`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Rounds.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/tree.rs::closed_system_baseline_reading_f`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/tree.rs)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/tree.rs::closed_system_baseline_reading_l`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/tree.rs)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/engine.py::build_tree`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/engine.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0450](tfq_0450_policy_endpoint_all_separated.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:517-522`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:494-497`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:506-515`
