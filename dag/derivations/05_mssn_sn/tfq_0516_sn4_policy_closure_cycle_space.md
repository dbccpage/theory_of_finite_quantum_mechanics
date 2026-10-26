# [TFQ-0516] sn4-policy-closure-cycle-space

> **Stage**: `MSSN_SN` | **Status**: `SOURCE_RECORD`  
> **UUID**: `d59a360a-630d-51f0-984b-8cd671f1f702`  
> **Parent Derivation**: [TFQ-0514](tfq_0514_sn3_cost_two_unary_mark.md)

---

## 1. Abstract & Formal Statement

S(4) applies a supplied pair-separation closure policy. The sealed source derives no object-language endogenous demand generator; under the declared policy, which reads admitted structure and automorphism orbits and issues one requirement per orbit, the fixed finite datum set reaches the all-pairs-separated fixpoint, and a closed run from an empty requirement store makes at most n(n−1)/2 rounds (closedRun_round_bound_from_empty). At that terminal state the active separation-demand set is empty, so W₄ = ∅ and s₄ = 0, while the retained history H₄ stays nonempty. A complete graph K_m records the separated pairs of m data; for m ≥ 1 it is connected with cycle-space dimension m(m−1)/2 − m + 1.

### Governing Obligation
Under the declared closure policy, reach W₄ = ∅ with H₄ retained, bound a closed run by n(n−1)/2 rounds, and compute the cycle-space dimension m(m−1)/2 − m + 1 of K_m as a graph count, not a demand count.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared pair-separation closure policy of the sealed Genesis account, token-blind and isomorphism-equivariant (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Neither supply nor a stage number selects the policy, and there is no claim that the carrier has four data or that exactly five receipts were issued, so dual_ledger_independence_at_stage_4 (s₄ = 0, |H₄| = 5) is a table identity; K_m edges need not be admitted binary relations, and S4Orbit counts complete-graph edges without orbit search.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/Derivation/Rounds.lean::closedRun_round_bound_from_empty`](../../../lean4/Imported/Genesis19l57g1/Derivation/Rounds.lean)
- [`lean4/Imported/OeSn/SnTheorems.lean::dual_ledger_independence_at_stage_4`](../../../lean4/Imported/OeSn/SnTheorems.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust check of the S(4) ledger or of K_m cycle-space dimension`

### Python Oracles & Numerical Evaluators
- `omega_engine_education/documentation/002_oesn/code/sn_core.py::S4Orbit` (private upstream source, not in this repository)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0517](tfq_0517_sn5_continuation_recorded_request.md)
- [TFQ-0522](tfq_0522_sn_e08_weighted_l1_duality.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:531-537`
  - `omega_engine_education/documentation/002_oesn/levels/level_04_simplex_graph_expansions.md:24-27`
  - `omega_engine_education/documentation/002_oesn/levels/level_04_simplex_graph_expansions.md:35-37`
