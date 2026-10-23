# [TFQ-0515] sn-endpoint-lemma

> **Stage**: `MSSN_SN` | **Status**: `PROVED_LEAN`  
> **UUID**: `73f17d1a-9cbe-5e41-aeb2-52d91dcce353`  
> **Parent Derivation**: [TFQ-0514](tfq_0514_sn3_cost_two_unary_mark.md)

---

## 1. Abstract & Formal Statement

For a supplied irreflexive relation R, R(a,b) implies a ≠ b, since a = b would turn the witness into R(a,a); so the support of an asserted pair has exactly two elements, |{a,b}| = 2. This counts endpoints, not witnesses: single_oriented_witness_consistent builds a model with one forward witness and no reverse witness, so endpoints are 2 while witnesses can be 1. For the pointed two-element directed graph D₂ = ({0,1}, 0→1), each asserted pair (a,b) receives exactly one point-preserving map with f(0) = a and f(1) = b, and that map preserves the edge (D2_initial_pointed).

### Governing Obligation
From irreflexivity and R(a,b) derive a ≠ b, report endpoint count 2 separately from witness multiplicity, and give the unique point-preserving map from D₂ to each asserted pair.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Irreflexivity and orientation of R as declared inputs, not consequences of <> (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> D₂ is initial only among pointed structures with an asserted pair; the combined paper says this does not make D₂ initial in an unspecified category of all systems. The sn-wire grammar accepts <a->a>, so irreflexivity is checked by verify_wir and not by parsing.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/Derivation/PrimDiff.lean::D2_initial_pointed`](../../../lean4/Imported/Genesis19l57g1/Derivation/PrimDiff.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/PrimDiff.lean::irrefl_witness_ne`](../../../lean4/Imported/Genesis19l57g1/Derivation/PrimDiff.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/PrimDiff.lean::single_oriented_witness_consistent`](../../../lean4/Imported/Genesis19l57g1/Derivation/PrimDiff.lean)
- [`lean4/Imported/OeSn/SnTheorems.lean::irrefl_witness_distinct`](../../../lean4/Imported/OeSn/SnTheorems.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust check of the endpoint lemma in the S(n) strand`

### Python Oracles & Numerical Evaluators
- [`omega_engine_education/documentation/002_oesn/code/sn_audit.py::verify_wir`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_education/documentation/002_oesn/code/sn_audit.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md:302-307`
  - `omega_engine_education/documentation/002_oesn/sn.md:58-66`
  - `omega_engine_education/documentation/002_oesn/reading_guide.md:32-35`
