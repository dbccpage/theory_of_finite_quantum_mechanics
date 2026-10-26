# [TFQ-0467] rung4-index-up-to-isomorphism

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `a6e062a3-1ca7-5232-86a7-4f1dfacf8d25`  
> **Parent Derivation**: [TFQ-0466](tfq_0466_rung3_first_demand_index.md)

---

## 1. Abstract & Formal Statement

Rung four (pull request 255) takes leftover X-3, the first-demand index up to the sealed isomorphism. In Lean separability and honour transport across the isomorphism, a label-preserving isomorphism carries a demand, and under a uniform stake (one label on every distinct pair) carrying a demand is class-invariant and class-matched histories have one first count; renaming supply tokens moves no first count. Under the three index readers parity, chain and residueThree the index escapes: isomorphic regimes of three or four data differ in carrying a demand, and class-matched histories of eight and eleven events have first counts eight or eleven against none. On the rectangle (2316 regimes in 402 classes, automorphism counts one to 240) the first count is constant on every trajectory class inside four events, which the Lean witnesses show is the bound's doing.

### Governing Obligation
Carry demand transport and first-count transport under a uniform stake for every pair of related regimes, and exhibit the non-uniform countermodels of eight and eleven events through Boolean checks proved sound.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Lean declaration SecondIso.Transport.hasDemand_iff_of_uniform at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`
- **Admitted**: `Lean declaration SecondIso.Trajectory.first_demand_matched_of_uniform at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`
- **Admitted**: `Lean declaration SecondIso.Countermodel.first_count_not_trajectory_invariant at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Necessity of uniformity (Y-2) and the shortest class-matched witnesses (Y-1) are OPEN; the countermodel checks are proved sound with no converse, and the four-event rectangle hides the non-constancy that the longer Lean witnesses exhibit.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_iso/lean/SecondIso/Countermodel.lean::demand_not_class_invariant`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_iso/lean/SecondIso/Countermodel.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_iso/lean/SecondIso/Countermodel.lean::first_count_not_trajectory_invariant`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_iso/lean/SecondIso/Countermodel.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_iso/lean/SecondIso/Trajectory.lean::first_demand_matched_of_uniform`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_iso/lean/SecondIso/Trajectory.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_iso/lean/SecondIso/Transport.lean::hasDemand_iff_of_uniform`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_iso/lean/SecondIso/Transport.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: the second-derivation rung trees hold no Rust`

### Python Oracles & Numerical Evaluators
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_iso/iso_index.py::trajectory_report`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_iso/iso_index.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0468](tfq_0468_rung5_symmetry_along_history.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:305`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:1095-1100`
  - `github:dbccpage/19L57G1@85a83ae7c/research/second/claim_ledger.md:170`
