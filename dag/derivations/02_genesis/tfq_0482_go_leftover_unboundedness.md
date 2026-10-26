# [TFQ-0482] go-leftover-unboundedness

> **Stage**: `GENESIS` | **Status**: `PROVED_LEAN`  
> **UUID**: `1c3ac00a-5d11-5b75-990b-4f773d22cb47`  
> **Parent Derivation**: [TFQ-0481](tfq_0481_go_admission_gate.md)

---

## 1. Abstract & Formal Statement

The tenth derivation records a leftover with each change in a side ledger and keeps the ninth's state model; the sixteenth admits the recorded leftover back into the state. The feedback does not terminate: remove-then-admit is a two-change cycle at every state with an assertion, and a term added and identified away is one at every state with a term, while the ninth's add-then-remove is not a cycle. In Lean, if Reach16 s t n holds from a well-formed state with a term then Reach16 s t (2k + n) holds for every k (Reach16.unbounded), and ara reaches itself in 2k changes by removing and admitting for every k (admit_remove_unbounded), so the lengths of sequences reaching a result are unbounded.

### Governing Obligation
Exhibit the two-change cycles of the sixteenth seed and carry Reach16 s t (2k + n) for every k from a well-formed state with a term.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Unbounded lengths of sequences reaching a result, not an unbounded set of results; the fewest changes to a result stays its potential (ledger D3), and nothing here is a claim about time or physical recurrence.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/GenesisOngoing/Sixteenth/Reach.lean::Reach16.unbounded`](../../../lean4/Imported/GenesisOngoing/Sixteenth/Reach.lean)
- [`lean4/Imported/GenesisOngoing/Sixteenth/Reach.lean::admit_remove_unbounded`](../../../lean4/Imported/GenesisOngoing/Sixteenth/Reach.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: the H3V7N5QF package holds no Rust`

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/sixteenth/reach.py::reachable16`](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/sixteenth/reach.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0483](tfq_0483_go_h1_cancellation_excess.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/sixteenth/claim_ledger.md:48`
  - `lean4/Imported/GenesisOngoing/Sixteenth/Reach.lean:150-153`
  - `omega_engine_education/documentation/005_oegenong/levels/level_18_leftovers_unboundedness.md:38`
