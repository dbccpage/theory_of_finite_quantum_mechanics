# [TFQ-0470] rung7-duration-under-changing

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `9220d16d-e497-5b67-a318-8fa7076f757c`  
> **Parent Derivation**: [TFQ-0469](tfq_0469_rung6_succession_element_count.md)

---

## 1. Abstract & Formal Statement

Rung seven (pull request 260) takes W-1, duration under CHANGING: a growth is a changing round that adds a datum, a rest round a changing round that does not, and the duration vector counts rest rounds between successive growths. In Lean the growths and rest rounds of any replayed history are functions of base and regime, so the number of segments and their sum are definable, and the data that instances and requirements name bound later segments from below. Countermodels: no segment is a function of position, base and regime, and no duration between the first two growths is a function of the regime, even over histories from the empty regime. On the rectangle the vectors reached at every regime are exactly the envelope, and the envelope is not a class invariant.

### Governing Obligation
Carry the growth and rest counts as functions of base and regime and the naming lower bound over every replayed history, and exhibit the segment and gap countermodels.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Lean declaration SecondDuration.Rounds.growths_counted at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`
- **Admitted**: `Lean declaration SecondDuration.Gaps.gap_not_from_genesis at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Each duration between growths is not definable from the state; attainment of the envelope beyond the four-event rectangle (V-1) and the multiset of envelopes of a class (V-3) are OPEN.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_duration/lean/SecondDuration/Gaps.lean::gap_not_from_genesis`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_duration/lean/SecondDuration/Gaps.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_duration/lean/SecondDuration/Gaps.lean::segment_not_given_base`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_duration/lean/SecondDuration/Gaps.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_duration/lean/SecondDuration/Rounds.lean::growths_counted`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_duration/lean/SecondDuration/Rounds.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_duration/lean/SecondDuration/Rounds.lean::rest_given_base`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_duration/lean/SecondDuration/Rounds.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: the second-derivation rung trees hold no Rust`

### Python Oracles & Numerical Evaluators
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_duration/duration.py::envelope`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_duration/duration.py)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_duration/duration.py::vector`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_duration/duration.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0471](tfq_0471_rung8_element_count_across_iso.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt:308`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt:428-434`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt:207-209`
