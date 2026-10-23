# [TFQ-0430] metatheory-object-language-split

> **Stage**: `GENESIS` | **Status**: `DEFINITION`  
> **UUID**: `df7e8c78-cc86-58d8-9512-1834d5c19967`  
> **Parent Derivation**: [TFQ-0002](tfq_0002_genesis_regime_events_as_a_separate_admission_record.md)

---

## 1. Abstract & Formal Statement

The sealed manuscript declares two levels. The metatheory holds presentation tokens (strings), event sequences, indices, finite data structures and arithmetic; the object language holds only what a regime admits. Token glyphs, component counts, order, concatenation, multiplicity, substring structure, matching and string equality live in the metatheory unless an admitted judgment internalizes a distinction. Presentation identity (token equality) is metatheory only, internal identity is the datum index, and no semantic interpretation is ever assigned.

### Governing Obligation
Keep every glyph, count, order and string-equality test in the metatheory, and let object-language observables read only admitted data indices, forms, instances, rules and requirements.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared two-level metatheory/object-language split of genesis_source.txt section 2 (assumption)`

### Further Prerequisites
- [TFQ-0378](tfq_0378_regime_tuple_and_events.md) regime-tuple-and-events

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> A declared split, not a theorem: the Lean model has no tokens by construction, so token-blindness is structural there and is checked in Python and Rust by renaming tests; admission order is visible to the token-aware metatheory and erased at the object level.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/Derivation/Bridge.lean::order_erased_at_object_level`](../../../lean4/Imported/Genesis19l57g1/Derivation/Bridge.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Bridge.lean::order_visible_to_metatheory`](../../../lean4/Imported/Genesis19l57g1/Derivation/Bridge.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/token.rs::tokens_are_forgotten_by_the_key`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/token.rs)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/iso.py::serialize`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/iso.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0431](tfq_0431_regime_isomorphism_unordered_pairs.md)
- [TFQ-0432](tfq_0432_challenge0_inertia_second_token.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:79-85`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:87-93`
  - `omega_engine_education/documentation/001_oegen/genesis.md:7`
