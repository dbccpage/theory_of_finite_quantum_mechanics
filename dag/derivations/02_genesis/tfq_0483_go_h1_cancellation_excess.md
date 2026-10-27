# [TFQ-0483] go-h1-cancellation-excess

> **Stage**: `GENESIS` | **Status**: `PROVED_LEAN`  
> **UUID**: `f584a729-4a88-5417-a9e6-a4755abe035d`  
> **Parent Derivation**: [TFQ-0482](tfq_0482_go_leftover_unboundedness.md)

---

## 1. Abstract & Formal Statement

Climbing round H1, installed as the twenty-second derivation, replaces one sameness sentence of the ninth seed: two results are the same when they differ only in how their terms are written, or only by an xry and an xsy asserted together. Two states are then one result exactly when they have equally many terms and, after one rewriting, the same excess e = M_r − M_s at every ordered pair (gen_iff_same, same_iff_excess), and each result has one plain state up to writing, asserting no pair in both relations (plain_reduced). The fewest changes to a result is Φ(G) = n + Σ|e(x,y)|, the plain state's size, and a shortest sequence is additions only through plain states (fewest_changes).

### Governing Obligation
Carry sameness as equal term count and equal excess after one rewriting, the plain state as the representative of each result, and fewest changes n + Σ|e| on every well-formed state.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Chosen reading C-J1: one more xry and xsy on one pair, x = y allowed, sameness the equivalence generated with rewriting (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> For the chosen reading C-J1 only (the unchosen C-J2 and C-J3 give 29 and 1081 results against 673 at two terms and eight rounds); here an addition can undo an addition, so the ninth's no-return for additions does not survive the new sameness.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/GenesisOngoingCore/Twentysecond/Cost.lean::fewest_changes`](../../../lean4/Imported/GenesisOngoingCore/Twentysecond/Cost.lean)
- [`lean4/Imported/GenesisOngoingCore/Twentysecond/Plain.lean::plain_reduced`](../../../lean4/Imported/GenesisOngoingCore/Twentysecond/Plain.lean)
- [`lean4/Imported/GenesisOngoingCore/Twentysecond/Same.lean::gen_iff_same`](../../../lean4/Imported/GenesisOngoingCore/Twentysecond/Same.lean)
- [`lean4/Imported/GenesisOngoingCore/Twentysecond/Same.lean::same_iff_excess`](../../../lean4/Imported/GenesisOngoingCore/Twentysecond/Same.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: the H3V7N5QF package holds no Rust`

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/twentysecond/state.py::cost`](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/twentysecond/state.py)
- [`atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/twentysecond/state.py::excess`](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/twentysecond/state.py)
- [`atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/twentysecond/state.py::plain`](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/twentysecond/state.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0484](tfq_0484_go_h2_state_raising_gauge.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/twentysecond/claim_ledger.md:50`
  - `atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/twentysecond/claim_ledger.md:53`
  - `external:sha256:f016b739d1272d0f46037a65694f050bde85456ebe26cab5e029212bdbf8e34e:47`
