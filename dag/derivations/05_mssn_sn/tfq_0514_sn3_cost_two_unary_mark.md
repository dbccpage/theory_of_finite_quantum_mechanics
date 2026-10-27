# [TFQ-0514] sn3-cost-two-unary-mark

> **Stage**: `MSSN_SN` | **Status**: `SOURCE_RECORD`  
> **UUID**: `b6c3cbd8-ff69-500b-933a-29bcc3cbf6a1`  
> **Parent Derivation**: [TFQ-0513](tfq_0513_sn2_opaque_collapse.md)

---

## 1. Abstract & Formal Statement

S(3) requires the admitted opaque data <a> and <ab> to be separated, starting from a form-less, instance-less regime and counting each admitted item once. No response of at most one item separates the pair (cost1_insufficient_general), and one new unary form with one instance at a demanded endpoint does, so the minimum item count is 2 in both readings. Under item count the minima tie: at max_items 2 and max_arity 2 reading L has 6 valid deltas in 3 classes (unary mark, binary link, binary self-loop) and reading F has 10 in 5, and in reading L the tie class over all arities is countably infinite. Under the lexicographic cost mu2 = (items, new-form arity sum) the unique minimum up to source isomorphism is the unary mark (2,1), in reading L (mu2_unique) and reading F (mu2_unique_F).

### Governing Obligation
Show that no response of at most one item separates the pair and that every valid two-item response with new-form arity sum at most 1 is isomorphic to the unary mark, and keep the binary edge out of the minimizer.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared response grammar NewDatum, NewForm, NewInst, NewRuleAll and the costs mu1 and mu2 of the sealed Genesis account (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The mu2 minimizer is a unary mark, not a binary edge: a binary link is one of the tied mu1 responses and an edge reading is an additional interpretation. S3Separation.cost_floor in sn_core.py is a fixture parameter, and testing that it equals 2 does not reprove minimality; the cost belongs to this item grammar only.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/GenesisDerivation/Derivation/Minimality.lean::cost1_insufficient_general`](../../../lean4/Imported/GenesisDerivation/Derivation/Minimality.lean)
- [`lean4/Imported/GenesisDerivation/Derivation/Minimality.lean::mu2_unique`](../../../lean4/Imported/GenesisDerivation/Derivation/Minimality.lean)
- [`lean4/Imported/GenesisDerivation/Derivation/MinimalityF.lean::mu2_unique_F`](../../../lean4/Imported/GenesisDerivation/Derivation/MinimalityF.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/minima.rs::min_responses`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/minima.rs)

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py::iter_cost2_deltas`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py)
- [`atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py::mu2`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/candidates.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0515](tfq_0515_sn_endpoint_lemma.md)
- [TFQ-0516](tfq_0516_sn4_policy_closure_cycle_space.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt:332-339`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt:305-313`
  - `omega_engine_education/documentation/002_oesn/levels/level_03_abstract_simplices.md:28-36`
