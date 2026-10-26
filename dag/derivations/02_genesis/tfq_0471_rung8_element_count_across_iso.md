# [TFQ-0471] rung8-element-count-across-iso

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `c83ddeaf-d108-58a3-9059-4ac2549cd6c5`  
> **Parent Derivation**: [TFQ-0470](tfq_0470_rung7_duration_under_changing.md)

---

## 1. Abstract & Formal Statement

Rung eight (pull request 262) takes Z-1, the element count across the sealed isomorphism. In Lean every inhabitant of the isomorphism keeps the numbers of data and forms with no hypothesis, and two clean regimes (well-formed, no list holding an entry twice) that it relates have all five component counts equal; six exhibited pairs show neither hypothesis can be dropped for instances, rules or requirements. Every event keeps cleanness and the empty and both Lean reading regimes are clean; from a clean base no class left is reached again, a class revisited is the very regime reached by unchanging events, so recurrence is only a stutter, and the counts of a history are functions of the class it reaches. Across two bases the class does not carry the count.

### Governing Obligation
Carry the component counts across the isomorphism between clean regimes and the no-return-to-class and stutter laws from every clean base, with the six hypothesis countermodels.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Lean declaration SecondClass.Count.size_iso at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`
- **Admitted**: `Lean declaration SecondClass.Recur.no_return_class at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`
- **Admitted**: `Lean declaration SecondClass.Recur.recurrence_is_stutter at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Clean regimes and bases only: recurrence from an unclean base (U-1) and the Lean form of a history recurring exactly when it holds an unchanging event (U-2) are OPEN, and the Lean countermodel's two sides lie in two Python classes because Python reading L holds no requirement (P-13 missed).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_class/lean/SecondClass/Count.lean::size_iso`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_class/lean/SecondClass/Count.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_class/lean/SecondClass/Counter.lean::counts_not_of_class`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_class/lean/SecondClass/Counter.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_class/lean/SecondClass/Recur.lean::no_return_class`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_class/lean/SecondClass/Recur.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_class/lean/SecondClass/Recur.lean::recurrence_is_stutter`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_class/lean/SecondClass/Recur.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: the second-derivation rung trees hold no Rust`

### Python Oracles & Numerical Evaluators
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_class/class_count.py::recurrences`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_class/class_count.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0472](tfq_0472_rung9_two_ness_observational_classes.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:309`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:436-444`
  - `github:dbccpage/19L57G1@85a83ae7c/research/second/claim_ledger.md:218`
