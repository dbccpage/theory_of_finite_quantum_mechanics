# [TFQ-0475] c2-run-forward-every-history

> **Stage**: `GENESIS` | **Status**: `PROVED_LEAN`  
> **UUID**: `9d38a1eb-4b20-5ba5-af54-95ea4ab588e5`  
> **Parent Derivation**: [TFQ-0474](tfq_0474_c1_engine_class_144.md)

---

## 1. Abstract & Formal Statement

Continuation attempt two (pull request 269) takes Challenge 4 and runs every one of the 144 engines forward from both sealed readings to declared bounds (two items, growth below four data, fifteen rounds, a node guard of 250 per run): 288 runs, 25,932 nodes, 69,490 edges and 43,846 merges, every node and edge replayed and quotiented by the implemented isomorphism. In the local Lean package SecondRun/Run.lean, for every history of sealed events and switch markers from any engine state, the element count never falls (ereplay_elems_le), a history leaving it unchanged leaves the regime unchanged, no further history reaches a regime once left (no_return), and on a history returning to its starting state every state part of the way holds the starting regime (cycle_regime_const). A pair collapsed with a common third datum is not separable in that regime (not_separable_through), the shape of all 772 refused apart demands of the runs.

### Governing Obligation
Carry ereplay_elems_le, no_return and cycle_regime_const for every history of sealed events and switch markers, and replay every node and edge of the 288 bounded runs.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Sealed kernel slice reconstructed verbatim in SecondRun/Kernel.lean from Derivation/Basic.lean and Derivation/Inertia.lean (assumption)`
- **Admitted**: `Engine event grammar: a sealed event, or a switch marker that keeps the regime and flips the mode (assumption)`

### Further Prerequisites
- [TFQ-0384](tfq_0384_cumulative_count_no_return.md) cumulative-count-no-return

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The Lean speaks of histories, not of the Python runs: that each run edge is such a history is read, not proved; the responder and generators are not reconstructed in Lean, not_separable_through is about one regime, and the run counts hold at the declared bounds only.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/SecondRun/Run.lean::cycle_regime_const`](../../../lean4/Imported/Genesis19l57g1/SecondRun/Run.lean)
- [`lean4/Imported/Genesis19l57g1/SecondRun/Run.lean::ereplay_elems_le`](../../../lean4/Imported/Genesis19l57g1/SecondRun/Run.lean)
- [`lean4/Imported/Genesis19l57g1/SecondRun/Run.lean::no_return`](../../../lean4/Imported/Genesis19l57g1/SecondRun/Run.lean)
- [`lean4/Imported/Genesis19l57g1/SecondRun/Run.lean::not_separable_through`](../../../lean4/Imported/Genesis19l57g1/SecondRun/Run.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: the second-derivation run tree holds no Rust; the sealed Rust predates the switch marker`

### Python Oracles & Numerical Evaluators
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_run/fwd_runs.py::build_run`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_run/fwd_runs.py)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_run/fwd_runs.py::replay_mismatches`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_run/fwd_runs.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0476](tfq_0476_forced_census_column.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:262`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:910-922`
  - `lean4/Imported/Genesis19l57g1/SecondRun/Run.lean:276-280`
