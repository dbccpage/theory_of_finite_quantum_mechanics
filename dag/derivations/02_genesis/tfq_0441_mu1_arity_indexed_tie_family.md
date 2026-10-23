# [TFQ-0441] mu1-arity-indexed-tie-family

> **Stage**: `GENESIS` | **Status**: `PROVED_LEAN`  
> **UUID**: `c05b09d1-786f-5529-930e-962bb745d7af`  
> **Parent Derivation**: [TFQ-0440](tfq_0440_mu1_minimum_not_unique_l.md)

---

## 1. Abstract & Formal Statement

For every arity k ≥ 1 the k-ary mark, one k-ary form and one instance (1, ..., 1), is a valid two-item response to Challenge 3 on R2L (deltaK_valid, deltaK_length), since the all-hole context separates the two required data. Distinct arities give non-isomorphic results because an isomorphism preserves form arity (markK_pairwise_noniso), so the mu1 tie class in reading L is countably infinite. A concrete enumeration is therefore complete only relative to an arity bound, and the arity-at-most-two census is one slice of this family.

### Governing Obligation
Show that each k-ary mark with k ≥ 1 is a valid two-item response on R2L and that marks of different arities have non-isomorphic results.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared item grammar, measure mu1 and the implemented isomorphism relation (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Stated over R2L only: no reading-F analogue of the k-ary family is formalized, and the family leaves the mu2 minimum (2, 1) unique up to isomorphism.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean::deltaK_length`](../../../lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean::deltaK_valid`](../../../lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean::markK_pairwise_noniso`](../../../lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust check of the unbounded arity family; the Rust census enumerates form arity at most two`

### Python Oracles & Numerical Evaluators
- `missing obligation: no Python check of the unbounded arity family; the Python census enumerates form arity at most two`

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:320-328`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md:322-326`
  - `lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean:362-363`
