# [TFQ-0170] Keep majorization, finite Markov laws, and row-stochastic maps on exact rational kernels

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `29d57b03-7925-559d-9d0c-2f52cd2796cc`  
> **Parent Derivation**: [TFQ-0167](tfq_0167_admit_only_exact_nonnegative_rational_masses_that_sum_to_one_with_no.md)

---

## 1. Abstract & Formal Statement

Majorization, Markov chains, and stochastic maps are exact controls on the rational simplex, still without float authority. src/lib.rs assigns majorization.rs to the majorization preorder, thermal ladders, Nielsen criterion, and T-transform chains; markov_chain.rs to classes, recurrence, period, stationary laws, absorption, and exact mixing; stochastic_map.rs to row-stochastic kernels, Bayesian inversion, and the Dobrushin coefficient. The obligation is to treat those constructions as finite kernel algebra over BigRational. They do not select a quantum channel, a CPTP class, or a continuous-time generator.

### Governing Obligation
Keep majorization, finite Markov laws, and row-stochastic maps on exact rational kernels.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: not located`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/finite_probability/majorization.rs`](../../code/rust/src/)
- [`code/rust/src/finite_probability/markov_chain.rs`](../../code/rust/src/)
- [`code/rust/src/finite_probability/stochastic_map.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000`
- **Primary Source Paths**:
  - `external:sha256:9504a35b2a33de8f85af42c874eb8da62364cbb364219de602dcfa98b26569e1`
