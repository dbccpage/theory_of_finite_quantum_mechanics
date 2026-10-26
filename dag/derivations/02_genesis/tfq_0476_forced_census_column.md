# [TFQ-0476] forced-census-column

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `80e2daa0-9f5d-56e7-bd59-7f03667874b8`  
> **Parent Derivation**: [TFQ-0475](tfq_0475_c2_run_forward_every_history.md)

---

## 1. Abstract & Formal Statement

Continuation attempt two decides the FORCED column of all twelve rows of the definability census over the declared engine class at its bounds (rounds zero to fifteen, both readings), each NOT FORCED verdict naming a first failing engine and a path of its run. The element count and irreversibility are FORCED, at the bounds by computation and beyond them by the every-history theorems, every cycle of every run being made of switch edges; two-ness is FORCED over the 64 LIVE engines, every path holding two before any bound or guard node. Every other row (the observational class count, succession, duration, adjacency, reach, symmetry, branching, exhaustion and recurrence) is NOT FORCED with an executable countermodel; one state of one run is reached in five rounds and in six, so succession and duration are not functions of the state.

### Governing Obligation
Read each census row off every node and run of the 288 bounded runs, record FORCED or NOT FORCED with a first failing engine and path, and carry only the element count and irreversibility beyond the bounds.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared engine class of continuation attempt one, 144 members, run from both sealed readings (assumption)`
- **Admitted**: `Declared policy of how the runs read the DEFINABLE and USEFUL REALIZATION columns (SD-R-14) (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Verdicts other than the element count, irreversibility and two-ness over the LIVE members are computations at fifteen rounds and a guard of 250; whether the four streamless E4 carriers continue past the bounds is OPEN (H-1), and two is not shown to be the floor of declared inputs.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/SecondRun/Run.lean::ereplay_elems_le`](../../../lean4/Imported/Genesis19l57g1/SecondRun/Run.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: the second-derivation run tree holds no Rust`

### Python Oracles & Numerical Evaluators
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_run/fwd_census.py::forced_over`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_run/fwd_census.py)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_run/fwd_census.py::stage_verdict`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_run/fwd_census.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0486](tfq_0486_genesis_freeze_endpoint_ledger.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:489`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:485`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:483`
