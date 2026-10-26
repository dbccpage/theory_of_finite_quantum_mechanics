# [TFQ-0459] canonical-key-classification

> **Stage**: `GENESIS` | **Status**: `PROVED_LEAN`  
> **UUID**: `15191fb5-1981-54cb-87f2-68a5a5173f37`  
> **Parent Derivation**: [TFQ-0431](tfq_0431_regime_isomorphism_unordered_pairs.md)

---

## 1. Abstract & Formal Statement

If a representative map C lies in each regime's isomorphism orbit and is constant on orbits, then C(R) = C(S) exactly when R ≅ S, and an injective serialization of the representatives gives the same criterion for keys (key_classification, conditional on both hypotheses). Companion results remove those hypotheses for the concrete search: equal sorted five-field tuples after relabeling by supplied bijections imply isomorphism (serializedRelabel_sound), and the length-prefixed unsigned 64-bit wire encoding is injective on words below 2^64 (portableBytes_injective). Exhaustive search over all datum and form permutations attains a least structural key (canonicalKey_attained), and for well-formed regimes with duplicate-free collections the keys, and under the word bounds their byte encodings, are equal exactly when the regimes are isomorphic (canonicalKey_classification, canonicalBytes_classification).

### Governing Obligation
Show that the exhaustive-search canonical key and its portable byte encoding are equal exactly when two well-formed, duplicate-free regimes are isomorphic, within the unsigned-word bounds.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The abstract key_classification needs an in-orbit, orbit-invariant choice; the concrete search results assume no orbit oracle but cover the Lean search only, and refinement of the optimized Python and Rust programs remains a separate engineering obligation, checked by finite agreement on 1,436 labelled regimes.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/CanonicalMinimizer.lean::key_classification`](../../../lean4/Imported/Genesis19l57g1/CanonicalMinimizer.lean)
- [`lean4/Imported/Genesis19l57g1/PaperCanonical.lean::serializedRelabel_sound`](../../../lean4/Imported/Genesis19l57g1/PaperCanonical.lean)
- [`lean4/Imported/Genesis19l57g1/PaperSearch.lean::canonicalBytes_classification`](../../../lean4/Imported/Genesis19l57g1/PaperSearch.lean)
- [`lean4/Imported/Genesis19l57g1/PaperSearch.lean::canonicalKey_attained`](../../../lean4/Imported/Genesis19l57g1/PaperSearch.lean)
- [`lean4/Imported/Genesis19l57g1/PaperWire.lean::portableBytes_injective`](../../../lean4/Imported/Genesis19l57g1/PaperWire.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/canonical.rs::portable_key_v1`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/canonical.rs)

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/genesis/code/portable_key.py::portable_key_v1`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/portable_key.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/paper.md:484-492`
  - `atlas/papers/finite_obstruction_calculus/genesis/paper.md:508-521`
  - `atlas/papers/finite_obstruction_calculus/genesis/code/fixtures/historical_claim_ledger.md:33`
