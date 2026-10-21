# [TFQ-0469] rung6-succession-element-count

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `b6fa2aa4-84d2-5399-829d-1d10543adeb3`  
> **Parent Derivation**: [TFQ-0468](tfq_0468_rung5_symmetry_along_history.md)

---

## 1. Abstract & Formal Statement

Rung six (pull request 259) takes Z-4, succession of accepted rounds through the element count, under three readings of a round: EVERY event, every ADMITTING event (not a supply) and every CHANGING event (the regime differs after it). In Lean, under CHANGING the count of any replayed history is the element count of the regime reached less the base's, so it is a function of base and regime, and counted from the empty regime a function of the regime alone; for every history CHANGING is at most ADMITTING, which is at most EVERY. Countermodels: EVERY and ADMITTING are not functions of base and regime, and CHANGING is not a function of the regime alone across bases (the Lean reading regime R2L is reached from the empty regime with count three and from itself with count zero).

### Governing Obligation
Carry the CHANGING count as element count less the base's over every replayed history, the ordering of the three counts, and the three countermodels.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Lean declaration SecondSuccession.Count.changes_counted at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`
- **Admitted**: `Lean declaration SecondSuccession.Readings.every_not_given_base at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`
- **Admitted**: `Lean declaration SecondSuccession.Readings.changing_not_of_regime at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The readings are of histories of the sealed step, not of an engine's run; class-level succession was OPEN at this rung and is closed for clean bases only by rung eight, and within continuation attempt two's runs one state is reached in five rounds and in six.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_succession/lean/SecondSuccession/Count.lean::changes_counted`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_succession/lean/SecondSuccession/Count.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_succession/lean/SecondSuccession/Count.lean::changes_given_base`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_succession/lean/SecondSuccession/Count.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_succession/lean/SecondSuccession/Readings.lean::admitting_not_given_base`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_succession/lean/SecondSuccession/Readings.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_succession/lean/SecondSuccession/Readings.lean::changing_not_of_regime`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_succession/lean/SecondSuccession/Readings.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_succession/lean/SecondSuccession/Readings.lean::every_not_given_base`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_succession/lean/SecondSuccession/Readings.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: the second-derivation rung trees hold no Rust`

### Python Oracles & Numerical Evaluators
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_succession/succession.py::counts`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_succession/succession.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0470](tfq_0470_rung7_duration_under_changing.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt:205-207`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt:307`
  - `github:dbccpage/19L57G1@85a83ae7c/research/second/claim_ledger.md:195`
