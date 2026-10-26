# [TFQ-0440] mu1-minimum-not-unique-l

> **Stage**: `GENESIS` | **Status**: `PROVED_LEAN`  
> **UUID**: `fde46a48-8064-5120-a019-dbdd920dd52b`  
> **Parent Derivation**: [TFQ-0439](tfq_0439_challenge3_current_regime_fails.md)

---

## 1. Abstract & Formal Statement

Under mu1 in reading L the minimum corrective augmentation is not unique. The unary mark deltaU0 and the binary link deltaBL are both valid two-item responses to Challenge 3 on R2L, no response of at most one item is valid, and their results U0 and BL are non-isomorphic because form arity is an isomorphism invariant (mu1_minimum_not_unique, U0_not_iso_BL). The theorem is stated over R2L only.

### Governing Obligation
Show on R2L that two valid two-item responses have non-isomorphic results and that no response of at most one item is valid.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared item grammar, measure mu1 and the implemented isomorphism relation (assumption)`

### Further Prerequisites
- [TFQ-0381](tfq_0381_cost_two_first_separation.md) cost-two-first-separation

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Reading L only: reading-F non-uniqueness is the bounded engine enumeration of five classes (TFQ-0442), and under mu2 the minimum is unique up to isomorphism (TFQ-0382).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean::U0_not_iso_BL`](../../../lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean::mu1_minimum_not_unique`](../../../lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/minima.rs::nothing_below_two_items_separates_the_target`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/minima.rs)

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py::min_responses`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0441](tfq_0441_mu1_arity_indexed_tie_family.md)
- [TFQ-0442](tfq_0442_bounded_tie_census.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt:295-299`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt:299-303`
  - `lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean:290-292`
