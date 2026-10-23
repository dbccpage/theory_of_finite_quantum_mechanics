# [TFQ-0450] policy-endpoint-all-separated

> **Stage**: `GENESIS` | **Status**: `PROVED_LEAN`  
> **UUID**: `77bc0055-07ba-56a8-a148-041337e9eb62`  
> **Parent Derivation**: [TFQ-0449](tfq_0449_closed_baseline_terminates.md)

---

## 1. Abstract & Formal Statement

Call a regime a policy terminal when no unseparated admitted pair i < j has a valid response. The companion theorem policy_terminal_separates shows that a well-formed policy terminal whose imposed requirements are all separated separates every admitted pair: an unresolved pair would have the fresh-mark response of mark_progress, contradicting terminality. Together with the round bound, an unguarded maximal run of the declared closure policy cannot continue indefinitely and cannot stop on an unresolved pair for lack of a response.

### Governing Obligation
Show that a well-formed regime with satisfied requirements and no valid response for any unseparated pair separates every admitted pair.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The proof goes by contradiction and its axiom report lists Classical.choice; a bounded implementation can instead stop at a search or resource limit, which is not the all-pairs-separated result.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/Paper.lean::policy_terminal_separates`](../../../lean4/Imported/Genesis19l57g1/Paper.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/closure.rs::the_fixpoint_is_empty_and_genesis_has_no_demand`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/closure.rs)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/engine.py::closure_challenge_orbits`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/engine.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0451](tfq_0451_no_endogenous_demand_generator.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md:366-371`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md:370-371`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/axiom_report.txt:1042`
