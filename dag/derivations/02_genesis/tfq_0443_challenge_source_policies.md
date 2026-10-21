# [TFQ-0443] challenge-source-policies

> **Stage**: `GENESIS` | **Status**: `DEFINITION`  
> **UUID**: `7d159f5d-e3cb-5d6b-bc9f-d0797685681b`  
> **Parent Derivation**: [TFQ-0382](tfq_0382_refined_minimum_class.md)

---

## 1. Abstract & Formal Statement

After Challenge 3 the challenge source is a pair of declared policies. The pair-separation closure policy reissues the admitted separation requirement pattern on collapsed pairs, one challenge branch per automorphism orbit of collapsed pairs, or nothing at the fixpoint where every pair is separated; it reads only profile equality and automorphism structure, supplies no data and imports no new goal kind. At that fixpoint the external continuation policy supplies and admits one fresh opaque token, and runs with this policy disabled are the closed-system baseline. Round 1 of every tree answers the externally imposed Challenge 3 requirement, and later separation rounds answer the closure policy.

### Governing Obligation
Issue later demands only from the declared closure policy, one per automorphism orbit of collapsed pairs, and supply a fresh opaque token only through the declared external continuation policy at the closure fixpoint.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared pair-separation closure policy and external continuation policy, genesis_source.txt sections 3.9-3.10 (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> A collapsed pair is not an active obstruction by itself; the declared policy makes it one, its orbit-representative selection is also declared, and choosing it among conceivable policies is a declared-metatheory judgment, not a derived transition.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `missing obligation: no Lean statement of the closure policy; Lean states the selection-free transition relation and its transport (TFQ-0444)`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/closure.rs::closure_challenge_orbits`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/closure.rs)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/engine.py::closure_challenge_orbits`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/engine.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0444](tfq_0444_orbit_branching_repairs_least_pair.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:174-185`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:186-190`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:357-362`
