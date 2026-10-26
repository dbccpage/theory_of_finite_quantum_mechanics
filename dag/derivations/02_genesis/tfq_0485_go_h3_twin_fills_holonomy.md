# [TFQ-0485] go-h3-twin-fills-holonomy

> **Stage**: `GENESIS` | **Status**: `PROVED_LEAN`  
> **UUID**: `919e367f-8b9a-5b19-8546-11dd40f40fe3`  
> **Parent Derivation**: [TFQ-0484](tfq_0484_go_h2_state_raising_gauge.md)

---

## 1. Abstract & Formal Statement

Climbing round H3 is two fills on the H2 carrier. In the twenty-fourth derivation a fifth change fills one term, and a filled term x balances exactly when its loop excess e(x,x) is zero, the same in every state of a result and every writing (balances_iff); a result is told from the one asserting nothing exactly when some filled term's loop excess is non-zero (told_iff). In the twenty-fifth a filled triple (x,y,z) balances when the sum around e(x,y) + e(y,z) + e(z,x) is zero, which the sameness keeps; a result is told exactly when some filled triple does not balance (nothing_balanced, told_iff), with three terms it is blind exactly when the sum around 0,1,2 is zero and the two-way sums add up to zero (blind_three_iff), and with every loop and two-way sum zero the triples through one term decide (cone_decides). A scratch rank computation of the sums around filled triples modulo raising gives 2 of 7 dimensions at three terms, 7 of 13 at four and 16 of 21 at five, only the loops unseen from five terms.

### Governing Obligation
Carry loop balance for filled terms, triangle balance for filled triples, the told criteria, blind_three_iff and cone_decides, and keep the rank figures as scratch computation.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `H2 sameness of the twenty-third derivation (Same3) as the carrier of both fills (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The ranks come from research/twentyfifth/scratch_rank.py, which labels itself scratch and not evidence; the general rank criterion C(n − 1, 2), the four-term blind converse and the counts are ledger row O2, proved in the paper and checked by computation up to five terms, with no Lean statement.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/GenesisOngoingCore/Twentyfifth/Balance.lean::nothing_balanced`](../../../lean4/Imported/GenesisOngoingCore/Twentyfifth/Balance.lean)
- [`lean4/Imported/GenesisOngoingCore/Twentyfifth/Balance.lean::told_iff`](../../../lean4/Imported/GenesisOngoingCore/Twentyfifth/Balance.lean)
- [`lean4/Imported/GenesisOngoingCore/Twentyfifth/Blind.lean::blind_three_iff`](../../../lean4/Imported/GenesisOngoingCore/Twentyfifth/Blind.lean)
- [`lean4/Imported/GenesisOngoingCore/Twentyfifth/Blind.lean::cone_decides`](../../../lean4/Imported/GenesisOngoingCore/Twentyfifth/Blind.lean)
- [`lean4/Imported/GenesisOngoingCore/Twentyfourth/Same.lean::balances_iff`](../../../lean4/Imported/GenesisOngoingCore/Twentyfourth/Same.lean)
- [`lean4/Imported/GenesisOngoingCore/Twentyfourth/Tell.lean::told_iff`](../../../lean4/Imported/GenesisOngoingCore/Twentyfourth/Tell.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: the H3V7N5QF package holds no Rust`

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/twentyfifth/told.py::decides`](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/twentyfifth/told.py)
- [`atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/twentyfifth/told.py::rank`](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/twentyfifth/told.py)
- [`atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/twentyfourth/state.py::balances`](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/twentyfourth/state.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/twentyfourth/claim_ledger.md:63`
  - `atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/twentyfifth/claim_ledger.md:68`
  - `atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/twentyfifth/reading_the_seed.md:104-107`
