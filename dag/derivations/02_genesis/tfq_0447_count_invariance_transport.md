# [TFQ-0447] count-invariance-transport

> **Stage**: `GENESIS` | **Status**: `PROVED_LEAN`  
> **UUID**: `ef7a76c9-dcc4-5bd8-95f5-5c64b6dd4f36`  
> **Parent Derivation**: [TFQ-0444](tfq_0444_orbit_branching_repairs_least_pair.md)

---

## 1. Abstract & Formal Statement

Observational collapse is invariant under a renaming of datum indices with forms fixed: the renamed regime collapses the renamed pair exactly when the original regime collapses the original pair (collapsed_rename). For any caller-supplied candidate pair list with deciders that track collapse, the collapsed-pair counts before and after renaming agree (collapsedCount_rename). Collapse also transports across a full two-bijection regime isomorphism (collapsed_transport) and under the combined datum-and-form action (collapsed_renameDataForm). Requirements never enter collapse, so the renaming action leaves them alone.

### Governing Obligation
Show that collapse and the collapsed-pair count over a supplied pair list are invariant under datum-index renaming, and that collapse transports across a regime isomorphism.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The count transport acts on datum indices with forms fixed and takes the pair list and decider as parameters; token renaming is inexpressible in the token-erased Lean model, and the executable count and the identification of the mapped list with the engine's pair enumeration stay computational.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/Derivation/CountTransport.lean::collapsedCount_rename`](../../../lean4/Imported/Genesis19l57g1/Derivation/CountTransport.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/CountTransport.lean::collapsed_rename`](../../../lean4/Imported/Genesis19l57g1/Derivation/CountTransport.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/FormTransport.lean::collapsed_renameDataForm`](../../../lean4/Imported/Genesis19l57g1/Derivation/FormTransport.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/IsoCollapse.lean::collapsed_transport`](../../../lean4/Imported/Genesis19l57g1/Derivation/IsoCollapse.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/canonical.rs::the_key_is_invariant_under_every_renaming`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/canonical.rs)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/closure.rs::a_single_collapsed_pair_transports_under_renaming`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/closure.rs)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/iso.py::rename`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/iso.py)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/observe.py::collapsed_pairs`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/observe.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:607-618`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:759-772`
