# [TFQ-0487] endogenous-demands-exogenous-payments

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `45df2a61-85ea-57df-b5e3-1f007c0ba792`  
> **Parent Derivation**: [TFQ-0486](tfq_0486_genesis_freeze_endpoint_ledger.md)

---

## 1. Abstract & Formal Statement

Without the external continuation policy the closed system saturates: under the declared round shape a closed run from an empty requirement store makes at most n(n-1)/2 rounds (Lean closedRun_round_bound_from_empty, 2 * rounds ≤ n * (n - 1)), and at the fixpoint any further requirement needs a fresh datum (external supply) or a new requirement kind (external goal) (genesis_source §9 item 6). With external supply the runs grow in width, not in kind: the sealed mu2 trees record 53 (reading L) and 83 (reading F) innovation edges (fresh form plus instance), which the education audit reads as unary forms with 0 binary (finite computation to the requested depth of 15 transition steps). In the reflective composite reflState n demand never dries: for n ≥ 3 the distinct data 1 and 2 have equal depth-one profiles (Lean Generator.generation_never_dries). Within the declared local finite-alphabet class (one radius d, one colour bound k independent of chain length) every strategy fires and none clears (Lean G1Class.g1_class_exclusion), while the clearing members perPairFreshMark (recurring import) and valued (one-time identity-grade rule) lie outside the finite declaration. The education audit names the pattern 'endogenous demands, exogenous payments'.

### Governing Obligation
Carry the three Lean statements with their hypotheses (ClosedRun from an empty store; n ≥ 3 in reflState; FiniteDeclaration k S) and keep the unary-innovation count as a finite computation over the exported mu2 trees.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared round shape of a closed run: a fresh imposed target and a response admitting no fresh datum (assumption)`
- **Admitted**: `Declared local finite-alphabet strategy class LocalStrategy d with FiniteDeclaration k (assumption)`

### Further Prerequisites
- [TFQ-0451](tfq_0451_no_endogenous_demand_generator.md) no-endogenous-demand-generator

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Class-relative and carrier-relative: g1_class_exclusion speaks only of finite-alphabet local strategies on the reflective chain, the one-time valued rule clears with no recurring import (clears_does_not_imply_not_fires), and the unary-only innovation count is a bounded computation, not a theorem about longer runs.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/G1Class.lean::clears_does_not_imply_not_fires`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/G1Class.lean)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/G1Class.lean::g1_class_exclusion`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/G1Class.lean)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Generator.lean::generation_never_dries`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Generator.lean)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Rounds.lean::closedRun_round_bound_from_empty`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Rounds.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/closure.rs::closure_round_bound`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/closure.rs)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/engine.py::closure_challenge_orbits`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/engine.py)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/local_strategy.py::classification`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/local_strategy.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0488](tfq_0488_declared_challenge_import_per_level.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:563-569`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:480-487`
  - `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md:936-947`
