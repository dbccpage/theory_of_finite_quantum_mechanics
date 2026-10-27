# [TFQ-0455] d2-initial-pointed

> **Stage**: `GENESIS` | **Status**: `PROVED_LEAN`  
> **UUID**: `13caa413-e57d-5f15-a1b5-84d4e5603b63`  
> **Parent Derivation**: [TFQ-0454](tfq_0454_sealed_terminal_statement.md)

---

## 1. Abstract & Formal Statement

Let D₂ have carrier {0, 1} and the single edge 0 → 1. For any relation R with a supplied witness R(a, b), the map f(0) = a, f(1) = b preserves the edge, and every map sending 0 to a and 1 to b equals it, so f is the unique endpoint-preserving map from D₂ (D2_initial_pointed). Under irreflexivity this map is injective, because the endpoints of an irreflexive witnessed edge differ (irrefl_witness_ne).

### Governing Obligation
Show that a supplied edge R(a, b) receives exactly one endpoint-preserving map from the oriented two-point witness D₂, and that this map preserves the edge.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Further Prerequisites
- [TFQ-0387](tfq_0387_irreflexive_endpoints_distinct.md) irreflexive-endpoints-distinct

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> This represents the chosen witness only: the map need not describe every edge of R or preserve non-edges, needs no reverse edge or composition law, and does not force irreflexivity from opaque marks.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/GenesisDerivation/Derivation/PrimDiff.lean::D2_initial_pointed`](../../../lean4/Imported/GenesisDerivation/Derivation/PrimDiff.lean)
- [`lean4/Imported/GenesisDerivation/Derivation/PrimDiff.lean::irrefl_witness_ne`](../../../lean4/Imported/GenesisDerivation/Derivation/PrimDiff.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust check of the pointed two-point witness map`

### Python Oracles & Numerical Evaluators
- `missing obligation: no Python check of the pointed two-point witness map`

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0456](tfq_0456_five_presentation_questions.md)
- [TFQ-0460](tfq_0460_incidence_construction_betti.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/paper.md:430-438`
  - `lean4/Imported/GenesisDerivation/Derivation/PrimDiff.lean:129-131`
  - `atlas/papers/finite_obstruction_calculus/genesis/code/fixtures/historical_claim_ledger.md:21`
