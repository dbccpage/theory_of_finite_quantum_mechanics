# [TFQ-0427] context-fidelity

> **Stage**: `PREGENESIS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `a869a901-9113-5d27-94f3-6a82867a61af`  
> **Parent Derivation**: [TFQ-0426](tfq_0426_replay_necessity.md)

---

## 1. Abstract & Formal Statement

Narrowed boundary, status left OPEN: in the two-code model the stale context is 0 and the replayed context is 1. These codes differ. The empty-claim step holds at 0 and fails at 1. The binding check accepts a pair exactly when the two codes are equal, so it refuses (0, 1) and accepts (1, 1). Of the four ordered pairs drawn from {0, 1}, exactly two are accepted. Trial 2 Result 15, Prompt 12, Prompt 17, and a general ValidTrace semantics stay unresolved. Status stays OPEN.

### Governing Obligation
Keep the two-code witness separate from a general trace semantics. A verifier that reconstructs Replay(H) and accepts a declared context only when it equals that replay, before certifying a step, stays open.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The identities are one two-code witness. They do not define ValidTrace for an arbitrary trace, do not reconstruct a history, and do not read the trial record. The listed replay certifiers still do not define ValidTrace. Status stays OPEN.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CampaignPgwContextFidelity.lean::pgwContext_accept_count`](../../../lean4/CampaignPgwContextFidelity.lean)
- [`lean4/CampaignPgwContextFidelity.lean::pgwContext_binding_accepts_match`](../../../lean4/CampaignPgwContextFidelity.lean)
- [`lean4/CampaignPgwContextFidelity.lean::pgwContext_binding_refuses_stale`](../../../lean4/CampaignPgwContextFidelity.lean)
- [`lean4/CampaignPgwContextFidelity.lean::pgwContext_codes_differ`](../../../lean4/CampaignPgwContextFidelity.lean)
- [`lean4/CampaignPgwContextFidelity.lean::pgwContext_empty_claim_on_replay`](../../../lean4/CampaignPgwContextFidelity.lean)
- [`lean4/CampaignPgwContextFidelity.lean::pgwContext_empty_claim_on_stale`](../../../lean4/CampaignPgwContextFidelity.lean)
- `missing obligation: no Lean definition of ValidTrace or of the context-fidelity non-implication; Represented.replay_deterministic in 000_genesis_19l57g1/lean4/Derivation/Represented.lean shows only that replay is a function of the history`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/certification.rs::certifies`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/certification.rs)

### Python Oracles & Numerical Evaluators
- [`checks/independent/pgw-context-fidelity.py`](../../../checks/independent/pgw-context-fidelity.py)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/model.py::certify`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/model.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_education/documentation/000_oepregen/sources/analysis_derivation_v1.md:1065-1087`
  - `omega_engine_education/documentation/000_oepregen/03_results_and_arguments.md:127-134`
  - `omega_engine_education/documentation/000_oepregen/02_trial_record.md:120-130`
