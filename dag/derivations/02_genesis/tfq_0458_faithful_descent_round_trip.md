# [TFQ-0458] faithful-descent-round-trip

> **Stage**: `GENESIS` | **Status**: `PROVED_LEAN`  
> **UUID**: `19ef0827-652c-53c0-a73a-1d3f6ee3dadb`  
> **Parent Derivation**: [TFQ-0457](tfq_0457_quotient_retention.md)

---

## 1. Abstract & Formal Statement

For supplied translations f : P → Q and g : Q → P, injective maps i : P → C and j : Q → C with i = j ∘ f and j = i ∘ g exist if and only if g ∘ f = id_P and f ∘ g = id_Q (faithful_descent_iff_round_trip_coherent). One direction substitutes the identifying equations and cancels the injective maps (faithful_descent_to_coherent); the other takes C = P, i = id and j = g. A failed round trip for this declared pair therefore excludes a faithful common carrier that eliminates the presentation index.

### Governing Obligation
Show that compatible injective embeddings of two presentations into a common carrier exist exactly when both round trips of the supplied translations are identities.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Failure concerns the declared translation pair only: another pair of translations may still close, and no common world prior to P and Q is assumed.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/Derivation/PresentationDescent.lean::faithful_descent_iff_round_trip_coherent`](../../../lean4/Imported/Genesis19l57g1/Derivation/PresentationDescent.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/PresentationDescent.lean::faithful_descent_to_coherent`](../../../lean4/Imported/Genesis19l57g1/Derivation/PresentationDescent.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust check of presentation descent`

### Python Oracles & Numerical Evaluators
- `missing obligation: no Python check of presentation descent`

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md:469-482`
  - `lean4/Imported/Genesis19l57g1/Derivation/PresentationDescent.lean:32-36`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/fixtures/historical_claim_ledger.md:32`
