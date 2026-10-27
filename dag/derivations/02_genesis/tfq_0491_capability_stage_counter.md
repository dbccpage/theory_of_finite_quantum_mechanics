# [TFQ-0491] capability-stage-counter

> **Stage**: `GENESIS` | **Status**: `DEFINITION`  
> **UUID**: `3380012e-3ffa-5b48-99ed-7ea054ceee41`  
> **Parent Derivation**: [TFQ-0488](tfq_0488_declared_challenge_import_per_level.md)

---

## 1. Abstract & Formal Statement

Declared here as the stage index n of S(n): it counts licensed stage changes, each consuming one recorded challenge import (TFQ-0488), and not rounds or events. The second derivation's census motivates the choice: succession of accepted rounds is NOT FORCED under EVERY and CHANGING because one state is reached in five rounds and in six (SD-CF-3), so a round count is not a function of the state, while under the CHANGING reading (an accepted round after which the regime differs) the count is definable from base and regime, and from the regime alone when counted from the empty regime. In Lean, along any history of sealed events and switch markers the element count never falls, and a step or history that changes the regime raises it (estep_elems_lt_of_ne, ereplay_elems_lt_of_ne).

### Governing Obligation
Increment n only on a licensed stage change with its import row, keep the round and event counters separate, and never read n off a round count.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Stage index counting licensed stage changes, a construction declared by this programme (assumption)`

### Further Prerequisites
- [TFQ-0469](tfq_0469_rung6_succession_element_count.md) rung6-succession-element-count

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> A declared counter, not a derived invariant: no theorem makes a stage count a function of the state under EVERY or ADMITTING, and the education audit's link to nf.derivation.lsnf names a skeletal filtration form, not a stage counter.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/GenesisDerivation/SecondRun/Run.lean::ereplay_elems_lt_of_ne`](../../../lean4/Imported/GenesisDerivation/SecondRun/Run.lean)
- [`lean4/Imported/GenesisDerivation/SecondRun/Run.lean::estep_elems_lt_of_ne`](../../../lean4/Imported/GenesisDerivation/SecondRun/Run.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust stage counter`

### Python Oracles & Numerical Evaluators
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_succession/succession.py::counts`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_succession/succession.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:485`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:205-209`
  - `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md:1102`
