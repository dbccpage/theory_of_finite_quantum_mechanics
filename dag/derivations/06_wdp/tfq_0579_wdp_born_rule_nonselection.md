# [TFQ-0579] wdp-born-rule-nonselection

> **Stage**: `WDP` | **Status**: `SOURCE_RECORD`  
> **UUID**: `1e971fe2-779f-561d-949d-d1ab30fb174e`  
> **Parent Derivation**: [TFQ-0578](tfq_0578_wdp_finite_hermitianization.md)

---

## 1. Abstract & Formal Statement

Positivity, normalization, phase invariance, and affinity admit a one-parameter family of state-effect readouts distinct from trace pairing, showing in this finite model that trace Born weights require an additional assumption (GEN-WDP-65).

### Governing Obligation
Mechanize the full one-parameter non-trace readout family countermodel of GEN-WDP-65 in Lean 4 alongside FiniteStateEffectReadout.lean.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> FiniteStateEffectReadout.lean formalizes factored Gaussian-rational trace readouts; the full one-parameter affine non-trace countermodel family is proved in prose and Python fixtures.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteStateEffectReadout.lean::WDP.FiniteStateEffectReadout.born_numerator_identity`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteStateEffectReadout.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteStateEffectReadout.lean::WDP.FiniteStateEffectReadout.probability_normalized`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteStateEffectReadout.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: checked in Lean 4 and Python state-effect readout fixtures`

### Python Oracles & Numerical Evaluators
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quantum.py::to_gaussian_rational`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quantum.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0580](tfq_0580_wdp_exact_scalar_hadamard_obstruction.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md:76`
