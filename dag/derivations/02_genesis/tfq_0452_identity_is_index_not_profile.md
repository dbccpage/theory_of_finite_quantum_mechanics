# [TFQ-0452] identity-is-index-not-profile

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `3faf6bec-8e88-51ff-a142-ac2a9644aba1`  
> **Parent Derivation**: [TFQ-0451](tfq_0451_no_endogenous_demand_generator.md)

---

## 1. Abstract & Formal Statement

Internal identity in the model is the datum index, never the profile (CL-IDENTITY-NOT-PROFILE). In reading F the first-round mu2 minimum admits one unary form with an instance marking datum 1; its only context is that form with one hole, so data 0 and 2 keep distinct indices with identical empty profiles while datum 1 is separated from both. A valid response separates the challenged pair by profiles, and other distinct data may stay observationally equivalent. The earlier sentence that from Challenge 3 round 1 onward each datum's internal identity is exactly its profile is false in the model and was withdrawn on 2026-09-08.

### Governing Obligation
Keep datum identity as the admission index, and check on the reading-F mu2 minimum that data 0 and 2 have equal empty profiles.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Question 11 itself stays unanswered by instruction, because naming external structures is withheld; the two surviving discrimination styles, attribute-like unary marks and relation-like binary links, are internal descriptions only.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/MinimalityF.lean::U0F`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/MinimalityF.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/profile.rs::profiles`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/profile.rs)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/observe.py::profiles`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/observe.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:634-644`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:641-643`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:645-648`
