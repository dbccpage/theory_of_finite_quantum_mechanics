# [TFQ-0438] responses-costs-mu1-mu2

> **Stage**: `GENESIS` | **Status**: `DEFINITION`  
> **UUID**: `0f6c5fdd-5427-5699-9d39-086b367df925`  
> **Parent Derivation**: [TFQ-0433](tfq_0433_contexts_plugging_profiles.md)

---

## 1. Abstract & Formal Statement

A response (delta) is an ordered finite list of NewDatum, NewForm(arity), NewInst(form, args) and NewRuleAll(form) items applied in order; an instance may name a form added earlier in the same list, and the reverse order is an ill-formed admission. The declared costs are mu1 = item count and mu2 = (item count, sum of new-form arities) compared lexicographically, where the sum counts every NewForm item, including distinct forms of equal arity. A valid response to Separate(i, j) applies, separates the target, and keeps every previously imposed requirement separated, because requirements are persistent constraints.

### Governing Obligation
Apply response items in order, cost them by mu1 and by lexicographic mu2, and accept a response only when it applies, separates the target and keeps every prior requirement separated.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared item grammar and cost measures mu1 and mu2, genesis_source.txt sections 3.6-3.7 (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Both measures and the item grammar are declared, not derived; bundling a form and an instance into one primitive would change every cost, and the enumerator's canonical item order makes a delta a multiset only up to that convention.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/Derivation/Basic.lean::applyDelta`](../../../lean4/Imported/Genesis19l57g1/Derivation/Basic.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Basic.lean::validResponse`](../../../lean4/Imported/Genesis19l57g1/Derivation/Basic.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean::aritySum`](../../../lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/measure.rs::arity_sum`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/measure.rs)
- [`atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/response.rs::response_valid_naive`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/response.rs)

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py::mu1`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py)
- [`atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py::mu2`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py)
- [`atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py::response_valid_naive`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt:154-163`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt:164-167`
  - `atlas/papers/finite_obstruction_calculus/genesis/paper.md:339-341`
