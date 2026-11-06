# [TFQ-0575] wdp-out-5-future-faithful-compression

> **Stage**: `WDP` | **Status**: `SOURCE_RECORD`  
> **UUID**: `21bb2bf6-e9a6-59ec-8da3-65fe7b01a6fe`  
> **Parent Derivation**: [TFQ-0574](tfq_0574_wdp_out_4_rejection_rule_reuse.md)

---

## 1. Abstract & Formal Statement

Outstanding Derivation Target 5 (GEN-WDP-73): on the bounded five-edit native carrier (at most 3 literal terms, count total at most 4, horizon h=2), clipped signed counts and a 13-coordinate integer report determine all horizon-2 future observations.

### Governing Obligation
Extend the Lean 4 horizon-2 compression proof (NativeFutureCompression.lean) to the general-horizon retention converse on larger finite carriers.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Further Prerequisites
- [TFQ-0567](tfq_0567_wdp_bridge_o02_observer_repair.md) wdp-bridge-o02-observer-repair

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Horizon h=2 and count bound 4 are proved in NativeFutureCompression.lean, with bound-5 collision counterexample; general-horizon converse for arbitrary native carriers remains open.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/NativeFutureCompression.lean::horizon_two_composition_bound`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/NativeFutureCompression.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/NativeFutureCompression.lean::two_removal_answers_determine_clip`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/NativeFutureCompression.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: horizon-2 native compression verified in Lean 4 and Python`

### Python Oracles & Numerical Evaluators
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/retention_choices.py::RetentionSignature`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/retention_choices.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0576](tfq_0576_wdp_additive_tensor_completion.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/five_outstanding_derivations.md:139-175`
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md:84`
