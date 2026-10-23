# [TFQ-0513] sn2-opaque-collapse

> **Stage**: `MSSN_SN` | **Status**: `SOURCE_RECORD`  
> **UUID**: `2e1dd528-952c-56b1-99b1-3789752e105b`  
> **Parent Derivation**: [TFQ-0512](tfq_0512_sn1_supply_not_admission.md)

---

## 1. Abstract & Formal Statement

S(2) retains opaque wholes: reading L admits (<a>, <ab>) and reading F admits (<>, <a>, <ab>). R2L_collapsed and R2F_collapsed show that every pair of admitted data stays observationally collapsed before distinguishing instances are admitted, so two externally different inscriptions remain internally indistinguishable, and the source does not decompose <ab> into a and b. A collapsed pair by itself is not an active obstruction; it becomes one only when a supplied question or separation requirement demands different answers. The later flat grammar sn.ebnf parses <ab> as a pair of glyphs, which is a new interpretation with its own parser.

### Governing Obligation
Keep <a> and <ab> as opaque admitted data with equal observation profiles, and record a collapse as an obstruction only after a separation demand is supplied.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Collapse is relative to the source's derivability profiles; the ledger value s₂ = 1 needs a supplied separation demand, and a two-vertex graph or permutation representation of the pair (as in S2Collapse) is declared structure, not an admitted directed relation.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean::R2F_collapsed`](../../../lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean::R2L_collapsed`](../../../lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust check of opaque collapse in the S(n) strand`

### Python Oracles & Numerical Evaluators
- [`omega_engine_education/documentation/002_oesn/code/sn_core.py::S2Collapse`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_education/documentation/002_oesn/code/sn_core.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0514](tfq_0514_sn3_cost_two_unary_mark.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:243-248`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:531-533`
  - `omega_engine_education/documentation/002_oesn/levels/level_02_relational_pairings.md:33-35`
