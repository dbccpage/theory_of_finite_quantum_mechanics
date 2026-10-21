# [TFQ-0501] runs-past-declared-bounds

> **Stage**: `GENESIS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `3efbdd85-b75c-5743-a3cf-b3360016d8a7`  
> **Parent Derivation**: [TFQ-0486](tfq_0486_genesis_freeze_endpoint_ledger.md)

---

## 1. Abstract & Formal Statement

Challenge 4 was run to declared bounds only (fifteen rounds, a node guard of 250 per run, growth below four data, two items): 11,266 nodes stopped at the guard and 368 at the bound, and 116 runs are not closed. Attempt two's leftovers H-2 to H-9 remain: the 970 refused same demands (H-2), the twenty-eight merges rung two's observable budget refused (H-3), the 482 regimes above the brute-force key limit (H-4), a distance on adjacency (H-5), a reading of carrying forward that admits switch (H-6), the forty-four closed runs with switch cycles UNDECIDED under ONE VALUE PER NODE (H-7), why E1 and E5 share one run under mu2 (H-8), and five data (H-9). Whether the augmentation sequence is unbounded is unresolved in the sealed paper (question 7): with the external continuation policy every requested depth tried was reached and every supplied demand has a response (mark_progress), and no unboundedness claim is made.

### Governing Obligation
Run the declared class past the bounds or prove the FORCED verdicts that are computations at the bounds, and dispose of each of H-2 to H-9 with its own evidence.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Open; every FORCED verdict other than the element count, irreversibility and two-ness over the LIVE members is a computation at the declared bounds.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Progress.lean::mark_progress`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Progress.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust port of the forward runs`

### Python Oracles & Numerical Evaluators
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_run/fwd_runs.py::frontier`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_run/fwd_runs.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt:1039-1044`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt:1045-1053`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:599-606`
