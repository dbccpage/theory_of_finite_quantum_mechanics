# [TFQ-0427] context-fidelity

> **Stage**: `PREGENESIS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `a869a901-9113-5d27-94f3-6a82867a61af`  
> **Parent Derivation**: [TFQ-0426](tfq_0426_replay_necessity.md)

---

## 1. Abstract & Formal Statement

On a two-value carrier, replay is the left fold of supplyDiamond, which keeps the value, and designateA, which sets the value true, starting from false. A one-step trace that is valid at a declared context s' need not be valid at a different replayed value s: when s differs from s' there is a trace valid at s' and not at s. A contract on this carrier preserves trace validity at replay(H) if and only if it accepts a context binding only when the context equals replay(H). The history consisting of supplyDiamond replays to false and the only-diamond answer on it is verified; the history supplyDiamond then designateA replays to true and the only-diamond answer on it is retracted.

### Governing Obligation
Define a trace semantics in which ValidTrace(τ | s′) is checkable, and make the verifier reconstruct Replay(H) and accept a declared context s′ only when s′ = Replay(H) before certifying any step taken from s′.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The two-value carrier is not the sealed Genesis event grammar, and ValidTrace here is not the Rust certifies predicate. Trial 2 Result 15, Prompt 12, and the Prompt 17 window are not instantiated. A general trace semantics for arbitrary regimes stays open.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CampaignPgwContextFidelity.lean::answers_follow_received_history`](../../../lean4/CampaignPgwContextFidelity.lean)
- [`lean4/CampaignPgwContextFidelity.lean::sound_iff_only_replay`](../../../lean4/CampaignPgwContextFidelity.lean)
- [`lean4/CampaignPgwContextFidelity.lean::stale_not_transferred`](../../../lean4/CampaignPgwContextFidelity.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/certification.rs::certifies`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/certification.rs)

### Python Oracles & Numerical Evaluators
- [`checks/independent/pgw-context-fidelity.py::main`](../../../checks/independent/pgw-context-fidelity.py)
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
