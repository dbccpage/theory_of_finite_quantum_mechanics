# [TFQ-0530] mssn-alphabet-declarations

> **Stage**: `MSSN_SN` | **Status**: `DEFINITION`  
> **UUID**: `78654ef3-111a-5519-9b8d-75184e9037be`  
> **Parent Derivation**: [TFQ-0529](tfq_0529_mssn_ascent_triad.md)

---

## 1. Abstract & Formal Statement

The MSS-N alphabet Γ38 is 26 lowercase letters, 10 digits and the two marks < and >; the grammar's word production uses Σ36, the letters and digits, and raw_glyphs treats < and > as ordinary marks, so balanced pairing is not an axiom there. A model must declare eight things separately: terminal spellings, tokenization, grammar, public start, layout, identity policy, annotation decoding and manipulation rules. Three relations that share notation stay apart: an encoded relation E ⊆ V × V, a rewrite relation, and an observation map q: V → O.

### Governing Obligation
Declare all eight dimensions for each MSS-N model, accept raw glyphs only from Γ38, and keep encoded, rewrite and observation relations distinct.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Alphabet size is independent of atlas row and of Genesis stage, and a glyph has a role only once a grammar gives it one.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `missing obligation: MssnSyntax.lean holds unrestricted syntax sketches with no recognizer for the alphabet`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust MSS-N alphabet check`

### Python Oracles & Numerical Evaluators
- `omega_engine_education/documentation/003_oemssn/code/mssn_codec.py::RawGlyphs` (private upstream source, not in this repository)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0531](tfq_0531_mssn_many_readings.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_education/documentation/003_oemssn/grammar/mssn.ebnf:10-11`
  - `omega_engine_education/documentation/003_oemssn/curriculum.md:42-43`
  - `omega_engine_education/documentation/003_oemssn/curriculum.md:44-48`
