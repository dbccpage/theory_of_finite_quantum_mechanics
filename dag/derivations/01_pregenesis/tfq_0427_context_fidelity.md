# [TFQ-0427] context-fidelity

> **Stage**: `PREGENESIS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `a869a901-9113-5d27-94f3-6a82867a61af`  
> **Parent Derivation**: [TFQ-0426](tfq_0426_replay_necessity.md)

---

## 1. Abstract & Formal Statement

A trace that starts from a declared context s′ and takes steps valid relative to s′ need not be valid relative to the actual replayed state s ≠ s′: ValidTrace(τ | s′) does not imply ValidTrace(τ | s). Trial 2's Result 15 is the example, with internally consistent reasoning from the stale premise s′ = {<>} after Prompt 12 had designated <a> as current. A sound execution contract therefore accepts a context binding C(s′) only when s′ = Replay(H). The analysis calls this a clean theorem target and gives no proof. The Prompt 17 contrast fits it: a truncated window answered Verified and the full replay Retracted, each right for the history it received, which the appended analysis calls an information boundary rather than a reasoning failure.

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
- [`lean4/PregenesisContextFidelity.lean::answers_follow_received_history`](../../../lean4/PregenesisContextFidelity.lean)
- [`lean4/PregenesisContextFidelity.lean::sound_iff_only_replay`](../../../lean4/PregenesisContextFidelity.lean)
- [`lean4/PregenesisContextFidelity.lean::stale_not_transferred`](../../../lean4/PregenesisContextFidelity.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/certification.rs::certifies`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/certification.rs)

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/genesis/code/derivation/model.py::certify`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/model.py)
- [`checks/independent/pgw-context-fidelity.py::main`](../../../checks/independent/pgw-context-fidelity.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `education/pregenesis_empty_mark/sources/analysis_derivation_v1.md:1065-1087`
  - `external:sha256:1713d12cc07cce5f295bb69922c49e278be2277c31d4fecee6b41ecb87d639bb:127-134`
  - `external:sha256:2e49c338376d7a78a6a89cdd340c9b3c351c485c20d4127e3c455b3fb1570428:120-130`
