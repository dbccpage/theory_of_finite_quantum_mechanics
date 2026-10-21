# [TFQ-0473] rung10-responder-adjacency-reach

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `9a1f1b2d-2654-5522-840d-6b9514b2ec5b`  
> **Parent Derivation**: [TFQ-0472](tfq_0472_rung9_two_ness_observational_classes.md)

---

## 1. Abstract & Formal Statement

Rung ten (pull request 265) takes X-6 for adjacency, reach, branching and exhaustion through the sealed responder: the demand is a collapsed pair, a response is a minimum of the sealed candidate space of at most two items and arity two under mu1 or mu2, and the responder refuses a regime holding a uniform rule. Adjacency, reach and branching are useful realizations at two declared capabilities, and exhaustion is definable: in Lean a form is exhausted exactly when it does not distinguish, exhaustion is carried by the isomorphism, and for a well-formed base a pair a history moves is mentioned by an instance admission of the history or the history holds a rule admission. On the rectangle 3110 demands are answered with none refused within two items, reach is at most three and finite adjacency distance at most two, and the measure changes the adjacency graph and the tie counts.

### Governing Obligation
Compute adjacency, reach and branching through the sealed responder on the rectangle at their declared price, and carry exhaustion and the moved-pair mention law over every history.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Lean declaration SecondResponse.Exhaust.exhausted_iff_not_distinguishes at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`
- **Admitted**: `Lean declaration SecondResponse.Move.moved_pairs_meet_mentions at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`
- **Admitted**: `Sealed responder under mu1 or mu2 at two items and arity two, priced as two declared capabilities (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> No Lean statement is about a minimum, a cost or a tie (S-3); response_collapses_a_pair is about one instance admission, not a sealed-responder minimum; the distance bound of two is not known to be the grammar's (S-4), and branching is finite computation only.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_response/lean/SecondResponse/Exhaust.lean::exhausted_iff_not_distinguishes`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_response/lean/SecondResponse/Exhaust.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_response/lean/SecondResponse/Move.lean::moved_pairs_meet_mentions`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_response/lean/SecondResponse/Move.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_response/lean/SecondResponse/Move.lean::response_collapses_a_pair`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_response/lean/SecondResponse/Move.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: the second-derivation rung trees hold no Rust`

### Python Oracles & Numerical Evaluators
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_response/response_rows.py::adjacency`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_response/response_rows.py)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_response/response_rows.py::moved_pairs`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_response/response_rows.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0474](tfq_0474_c1_engine_class_144.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt:311`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt:455-464`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt:349-352`
