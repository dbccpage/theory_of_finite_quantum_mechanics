# [TFQ-0498] declared-input-floor

> **Stage**: `GENESIS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `55d68a4f-522d-5581-9299-3ee49eebef8f`  
> **Parent Derivation**: [TFQ-0486](tfq_0486_genesis_freeze_endpoint_ledger.md)

---

## 1. Abstract & Formal Statement

No floor proof exists for the count of declared inputs (D10, H-1); the count stays two. Continuation attempt two found, at its declared bounds (fifteen rounds, a node guard of 250 per run, growth below four data, two items) and under its literal reading of carrying forward, four engines that carry the grammar forward declaring the stake and not the stream (SD-R-11), and calls this neither a floor proof nor a reduction outside those bounds. The completion-gate clause admits two readings of these bounded one-input carriers and was frozen as NOT_ESTABLISHED; whether the four carry forward past the bounds is OPEN (H-1, which needs the responder in Lean).

### Governing Obligation
Prove a floor for the declared-input count, or exhibit a reduction below two that holds past attempt two's bounds, with every bound stated. This file checks four carriers on the two names stake and stream: each declares the stake only, so the count is 1, below 2. The numerals 15, 250, 4, and 2 are recorded and are not a search. A floor for every carrier, a reduction past these four, and the attempt-two replay stay open.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Open; the bounded one-input carriers are a computation at declared bounds, and the clause's other reading was left to the author, who approved the freeze without a separate ruling. This file checks four carriers on the two names stake and stream: each declares the stake only, so the count is 1, below 2. The numerals 15, 250, 4, and 2 are recorded and are not a search. A floor for every carrier, a reduction past these four, and the attempt-two replay stay open. Checked slice, status unchanged. Narrowed in Lean 4 to two named inputs, stake and stream, and four carriers that each declare the stake and not the stream. The named list has length 2. Each of the four carriers has declared count 1, and 1 is below 2. The reading that every one of these four has count at least 2 is false. The reading that one of them has count 1 is true. The declared numerals are 15 rounds, a node guard of 250, a data bound of 4, and an item bound of 2. A carrier that declares neither input has count 0 and is not one of the four. These four carriers are not a floor for every later carrier, and the attempt-two search is not replayed. AuthorityEffect is None.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/PregenesisDeclaredInputFloor.lean::declared_bounds`](../../../lean4/PregenesisDeclaredInputFloor.lean)
- [`lean4/PregenesisDeclaredInputFloor.lean::each_count_is_one`](../../../lean4/PregenesisDeclaredInputFloor.lean)
- [`lean4/PregenesisDeclaredInputFloor.lean::each_declares_stake_not_stream`](../../../lean4/PregenesisDeclaredInputFloor.lean)
- [`lean4/PregenesisDeclaredInputFloor.lean::empty_carrier_is_not_among_the_four`](../../../lean4/PregenesisDeclaredInputFloor.lean)
- [`lean4/PregenesisDeclaredInputFloor.lean::four_engines`](../../../lean4/PregenesisDeclaredInputFloor.lean)
- [`lean4/PregenesisDeclaredInputFloor.lean::one_below_two`](../../../lean4/PregenesisDeclaredInputFloor.lean)
- [`lean4/PregenesisDeclaredInputFloor.lean::readings_disagree`](../../../lean4/PregenesisDeclaredInputFloor.lean)
- [`lean4/PregenesisDeclaredInputFloor.lean::vocabulary_is_two`](../../../lean4/PregenesisDeclaredInputFloor.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust check of the input count`

### Python Oracles & Numerical Evaluators
- [`checks/independent/pgw-declared-input-floor.py`](../../../checks/independent/pgw-declared-input-floor.py)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_run/fwd_runs.py::carries_forward`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_run/fwd_runs.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt:386`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:1064-1066`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt:333-336`
