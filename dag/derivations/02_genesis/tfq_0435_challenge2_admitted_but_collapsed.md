# [TFQ-0435] challenge2-admitted-but-collapsed

> **Stage**: `GENESIS` | **Status**: `PROVED_LEAN`  
> **UUID**: `fbf53bee-06f5-59eb-9386-d486c542f7eb`  
> **Parent Derivation**: [TFQ-0380](tfq_0380_readings_left_unselected.md)

---

## 1. Abstract & Formal Statement

At Challenge 2 both <a> and <ab> are supplied and retained, so reading L admits (<a>, <ab>) and reading F admits (<>, <a>, <ab>). In both readings every admitted pair is observationally collapsed (R2L_collapsed, R2F_collapsed): two externally distinct inscriptions remain internally indistinguishable. The countermodel admission_without_expressive_increase admits a fresh datum, a real state change, while the pair stays collapsed, a counterexample to the claim that a new external inscription necessarily increases internal expressive power. The recorded Challenge 0-3 histories replay exactly to the Challenge 3 regimes R2L and R2F (historyL_replays, historyF_replays).

### Governing Obligation
Replay the recorded reading L and reading F histories to R2L and R2F, show every admitted pair collapsed in both, and exhibit one datum admission that changes the regime and leaves the pair collapsed.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Further Prerequisites
- [TFQ-0434](tfq_0434_collapse_without_instances.md) collapse-without-instances

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Admission changed only the metatheoretic datum count and the replayable history; glyph identity, component count, order and substring structure stay internally unavailable, and the readings stay unselected (TFQ-0380).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean::R2F_collapsed`](../../../lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean::R2L_collapsed`](../../../lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean::admission_without_expressive_increase`](../../../lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean::historyF_replays`](../../../lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean::historyL_replays`](../../../lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/reading.rs::challenge2_admission_need_not_increase_expressive_power`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/reading.rs)

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py::challenge2_report`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0439](tfq_0439_challenge3_current_regime_fails.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt:246-248`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt:249-252`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt:256-259`
