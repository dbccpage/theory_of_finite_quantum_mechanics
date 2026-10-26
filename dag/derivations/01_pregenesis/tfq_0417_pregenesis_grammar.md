# [TFQ-0417] pregenesis-grammar

> **Stage**: `PREGENESIS` | **Status**: `DEFINITION`  
> **UUID**: `516a59f9-8a9e-5216-8947-e3befea8dbda`  
> **Parent Derivation**: [TFQ-0362](tfq_0362_four_host_conditions.md)

---

## 1. Abstract & Formal Statement

The Pre-Genesis host grammar declares the inscription alphabet {<, >, a, b} and three public starts: ground_token (exactly <>), inscription (one balanced, non-nested bracketed inscription) and pre_genesis_regime (zero or more inscriptions between braces, where {} is host list notation and not the empty word). It keeps four states apart: absent input, the empty word, the literal token <> and the ground carrier that S(0) adopts. It has no event productions: the first event, supply(<>), is the Genesis boundary, and parsing a word admits no carrier, transition or observational operation.

### Governing Obligation
Parse Pre-Genesis words with the declared grammar only, refuse the empty word at every public start, and admit nothing by parsing; supply(<>) belongs to Genesis.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared host grammar pre_genesis.ebnf, a later host notation not tested by the model trials (assumption)`

### Further Prerequisites
- [TFQ-0361](tfq_0361_inert_literal_inscription.md) inert-literal-inscription

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> A grammar verdict is a syntax check of host notation; it assigns no semantics to <> and does not decide whether an inscription is admitted.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `missing obligation: no Lean statement of the Pre-Genesis grammar; the grammar is checked in Python only`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust parser for pre_genesis.ebnf`

### Python Oracles & Numerical Evaluators
- `omega_engine_education/documentation/000_oepregen/code/check_pre_genesis.py::validate_cases` (private upstream source, not in this repository)
- `omega_engine_education/documentation/000_oepregen/code/tests/test_pre_genesis_grammar.py::test_four_state_separation` (private upstream source, not in this repository)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0418](tfq_0418_no_transition_quiescence.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_education/documentation/000_oepregen/grammar/pre_genesis.ebnf:14-19`
  - `omega_engine_education/documentation/000_oepregen/grammar/pre_genesis.ebnf:26-28`
