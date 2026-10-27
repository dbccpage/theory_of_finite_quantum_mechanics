# [TFQ-0507] pfp-carrier-origin-nilpotency

> **Stage**: `AUTHORIZATION` | **Status**: `PROVED_LEAN`  
> **UUID**: `e23ba9b7-570c-59ac-b932-81c60739c74b`  
> **Parent Derivation**: [TFQ-0506](tfq_0506_pfp_tripartite_law.md)

---

## 1. Abstract & Formal Statement

CarrierOrigin.lean (namespace SymbolCarrier.V02) establishes two small facts about its own declarations. no_difference_without_distinguishability: a Simplex1 V carries a proof that its source and target differ, so when src = tgt no 1-simplex with those endpoints exists. nilpotency_composition: for d₀ : α → β and d₁ : β → γ with a zero on γ and the hypothesis ∀ x, d₁ (d₀ x) = 0, the composite vanishes at every 0-cochain a; the proof applies the hypothesis to a. The file has no imports and elaborates under Lean 4.33.1 with no sorry.

### Governing Obligation
Use the two theorems only as stated: a 1-simplex needs distinct endpoints, and a supplied d₁ ∘ d₀ = 0 propagates pointwise; establish nilpotency for each concrete complex separately.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> nilpotency_composition restates its hypothesis and establishes d₁ ∘ d₀ = 0 for no complex; the ProtoSupport obligations and the trilemma classification in the same file are declarations with no theorem about them.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/PfpCarriers/CarrierOrigin.lean::nilpotency_composition`](../../../lean4/Imported/PfpCarriers/CarrierOrigin.lean)
- [`lean4/Imported/PfpCarriers/CarrierOrigin.lean::no_difference_without_distinguishability`](../../../lean4/Imported/PfpCarriers/CarrierOrigin.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust counterpart of CarrierOrigin.lean`

### Python Oracles & Numerical Evaluators
- `missing obligation: no Python counterpart of CarrierOrigin.lean`

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0508](tfq_0508_pfp_stealth_cochain_phi1_gamma2.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `lean4/Imported/PfpCarriers/CarrierOrigin.lean:70-79`
  - `lean4/Imported/PfpCarriers/CarrierOrigin.lean:81-88`
