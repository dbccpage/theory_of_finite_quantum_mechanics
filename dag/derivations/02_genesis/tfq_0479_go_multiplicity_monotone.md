# [TFQ-0479] go-multiplicity-monotone

> **Stage**: `GENESIS` | **Status**: `PROVED_LEAN`  
> **UUID**: `5ed7752f-d340-574c-9b73-cc7563b7fc3b`  
> **Parent Derivation**: [TFQ-0478](tfq_0478_go_contraction_step2_step3.md)

---

## 1. Abstract & Formal Statement

The fourth derivation counts assertions: a state has terms, a multiplicity per ordered pair and the names, arb is asserted once to begin with, and every change adds one term or raises one multiplicity by one, taking nothing away. Every change leaves its state contained in its outcome and containment composes, so along every sequence Reach4 s t n each multiplicity is the same or higher (Reach4.mult_le), at the pair writing arb as well (Reach4.arb_mult_le); terms, assertions and names persist and an obstruction is never cleared. A counted containment gives a containment of the supports, so the third derivation's conclusions survive on the supports.

### Governing Obligation
Carry multiplicity monotonicity at every ordered pair along every sequence of fourth-seed changes, through counted containment.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Reading C1': asserted means multiplicity at least one, with support and indicator maps to the earlier model (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Monotone for the fourth seed's additions only; the fifth derivation restores the four kinds of change on counted assertions, so this monotonicity is not claimed there, and a multiplicity can rise above one (arb_twice).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/GenesisOngoing/Fourth/Contain.lean::Reach4.arb_mult_le`](../../../lean4/Imported/GenesisOngoing/Fourth/Contain.lean)
- [`lean4/Imported/GenesisOngoing/Fourth/Contain.lean::Reach4.contains`](../../../lean4/Imported/GenesisOngoing/Fourth/Contain.lean)
- [`lean4/Imported/GenesisOngoing/Fourth/Contain.lean::Reach4.mult_le`](../../../lean4/Imported/GenesisOngoing/Fourth/Contain.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: the H3V7N5QF package holds no Rust`

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/fourth/invariants.py::never_decreases`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/fourth/invariants.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0480](tfq_0480_go_two_relations_swap.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `lean4/Imported/GenesisOngoing/Fourth/Contain.lean:15-16`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/fourth/claim_ledger.md:59`
  - `omega_engine_education/documentation/005_oegenong/levels/level_05_monotone_mass_growth.md:37`
