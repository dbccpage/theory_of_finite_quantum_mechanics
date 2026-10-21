# [TFQ-0531] mssn-many-readings

> **Stage**: `MSSN_SN` | **Status**: `DEFINITION`  
> **UUID**: `22a059ff-1017-590f-b429-bfae14aa7982`  
> **Parent Derivation**: [TFQ-0530](tfq_0530_mssn_alphabet_declarations.md)

---

## 1. Abstract & Formal Statement

mssn.ebnf declares 22 public starts, and every conformance case names its start; there is no guessed union or default start. The string a>b>c>a is accepted by raw_glyphs, label_path and glyph_path and refused by suffix_path, whose vertices need a digit annotation; a0>b2>c1>a0 is accepted by raw_glyphs, label_path and suffix_path and refused by glyph_path, which reads a0 as two adjacent vertices with no direction. check_mssn.py runs 39 cases over the 22 starts.

### Governing Obligation
Parse every MSS-N string under an explicitly named public start, and report acceptance per start rather than under a default reading.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The 22 starts are syntax profiles, not 22 completed semantic adapters (WDP-P001-014), and the historical inventory of 22 starts with six runtime profiles is not evidence of 28 evaluators.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `missing obligation: MssnSyntax.lean holds unrestricted syntax sketches with no recognizer or parser-correspondence theorem`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust recognizer for mssn.ebnf`

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/code/sn_mssn_checks.py::grammar_inventory_matches`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/code/sn_mssn_checks.py)
- [`omega_engine_education/documentation/003_oemssn/code/check_mssn.py::main`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_education/documentation/003_oemssn/code/check_mssn.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0532](tfq_0532_mssn_syntax_not_decoding.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_education/documentation/003_oemssn/grammar/mssn.ebnf:3-4`
  - `omega_engine_education/documentation/003_oemssn/curriculum.md:58-67`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md:679-680`
