# [TFQ-0497] context-decision-procedure

> **Stage**: `GENESIS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `5e9af5a2-14e5-5838-8153-60f15fb2000d`  
> **Parent Derivation**: [TFQ-0486](tfq_0486_genesis_freeze_endpoint_ledger.md)

---

## 1. Abstract & Formal Statement

A finite Genesis context decision procedure in the existing Regime enumerates every admitted form with all arity-matched slot tuples containing a hole, including multiple holes and uniform all-tuples rule coverage. Collapse and separability are decidable; returned witnesses distinguish, and no witness is equivalent to collapse. Computed profiles coincide exactly for collapsed data, their finite image cardinality equals the cardinality of the observational quotient, holding two is equivalent to at least two classes, and form exhaustion is decidable. First-count existence, Y-2 history-level uniformity necessity and external implementation refinement remain open.

### Governing Obligation
Use the complete finite context decisions for the remaining first-count and Y-2 history claims under their explicit predicates; establish the external implementation refinement separately.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The finite context, class-count, holding-two and exhaustion clauses have local Lean evidence for arbitrary finite regimes in the declared slot/all-tuples-rule language. The bundled node remains OPEN for first-count existence, Y-2 necessity and the external Python/Rust refinement; the earlier unary-only mirror is not used as a full context decider.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CampaignGenesisContextDecision.lean::CampaignGenesisContextDecision.classCount_eq_quotient_card`](../../../lean4/CampaignGenesisContextDecision.lean)
- [`lean4/CampaignGenesisContextDecision.lean::CampaignGenesisContextDecision.collapseTest_correct`](../../../lean4/CampaignGenesisContextDecision.lean)
- [`lean4/CampaignGenesisContextDecision.lean::CampaignGenesisContextDecision.exhaustionTest_correct`](../../../lean4/CampaignGenesisContextDecision.lean)
- [`lean4/CampaignGenesisContextDecision.lean::CampaignGenesisContextDecision.holdsTwo_iff_classCount`](../../../lean4/CampaignGenesisContextDecision.lean)
- [`lean4/CampaignGenesisContextDecision.lean::CampaignGenesisContextDecision.mem_contexts`](../../../lean4/CampaignGenesisContextDecision.lean)
- [`lean4/CampaignGenesisContextDecision.lean::CampaignGenesisContextDecision.profile_eq_iff`](../../../lean4/CampaignGenesisContextDecision.lean)
- [`lean4/CampaignGenesisContextDecision.lean::CampaignGenesisContextDecision.uniform_rule_exhausted`](../../../lean4/CampaignGenesisContextDecision.lean)
- [`lean4/CampaignGenesisContextDecision.lean::CampaignGenesisContextDecision.witness_none_iff`](../../../lean4/CampaignGenesisContextDecision.lean)
- [`lean4/CampaignGenesisContextDecision.lean::CampaignGenesisContextDecision.witness_sound`](../../../lean4/CampaignGenesisContextDecision.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/context.rs::contexts`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/context.rs)

### Python Oracles & Numerical Evaluators
- [`checks/independent/pgw-context-decision-procedure.py::main`](../../../checks/independent/pgw-context-decision-procedure.py)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/observe.py::separable`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/observe.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt:1073-1076`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt:484`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt:171-175`
  - `dag/derivations/independent/pgw-context-decision-procedure.md:5-8`
