# [TFQ-0442] bounded-tie-census

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `cef5cf1c-9549-5229-b73e-86afe9b26892`  
> **Parent Derivation**: [TFQ-0440](tfq_0440_mu1_minimum_not_unique_l.md)

---

## 1. Abstract & Formal Statement

Within the declared bounds of at most two items and form arity at most two, exhaustive enumeration under mu1, cross-checked against the unpruned space, finds at (2,2) six valid deltas in three isomorphism classes for reading L (unary mark, binary link, binary self-loop) and ten valid deltas in five classes for reading F. Reading F's two extra classes link to and from the never-required genesis datum, and they are non-isomorphic to each other because the bijection must preserve the requirement pair. Under mu2 each reading has two minimal deltas in one class. The standalone replay reproduces all four counts.

### Governing Obligation
Enumerate every valid delta of at most two items and arity at most two for R2L and R2F, quotient by the declared isomorphism, and report 6 deltas in 3 classes for L and 10 in 5 for F under mu1, and 2 in 1 class for each reading under mu2.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared resource bounds max_items 2 and max_arity 2 and the implemented isomorphism relation (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> A bounded census: it is the max_arity = 2 slice of the infinite mu1 tie family of reading L (TFQ-0441), and no reading-F Lean non-uniqueness statement exists.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `missing obligation: no Lean census of the bounded tie classes; reading-F non-uniqueness has no Lean statement`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/minima.rs::sealed_challenge3_reading_f`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/minima.rs)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/minima.rs::sealed_challenge3_reading_l`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/minima.rs)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/candidates.py::min_responses`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/candidates.py)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/reproduce.py::python_replay`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/reproduce.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:305-318`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md:326-328`
  - `omega_engine_education/documentation/001_oegen/genesis.md:19`
