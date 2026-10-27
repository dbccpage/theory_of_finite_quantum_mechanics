# [TFQ-0532] mssn-syntax-not-decoding

> **Stage**: `MSSN_SN` | **Status**: `DEFINITION`  
> **UUID**: `022495d0-6a1f-53e9-a002-8b27719488c3`  
> **Parent Derivation**: [TFQ-0531](tfq_0531_mssn_many_readings.md)

---

## 1. Abstract & Formal Statement

A grammar verdict is recognition, not decoding: a:1/0 parses in scalar_path, and division by zero is a later numeric refusal unless the grammar is changed to exclude zero denominators. Side conditions fall into three classes: zero denominators can be excluded lexically, bracket matching is context-free, and acyclicity or triangle inequalities are semantic obligations. a>2<b is refused in edge_weight_path because both marks on a step must agree. Recognition, AST construction, decoding, evaluation and exact serialization are distinct checks.

### Governing Obligation
Classify each side condition as lexical, context-free or semantic, enforce semantic conditions in a decoder or evaluator, and never read a parse as a decoded value.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Conformance cases MSSN_020 (a:1/0>b:2 accepted) and MSSN_023 (a>2<b refused) check syntax only, and finite differential tests are not an all-input argument for the codec.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `missing obligation: no Lean statement separating lexical, context-free and semantic conditions`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust MSS-N decoder for scalar or edge-weight paths`

### Python Oracles & Numerical Evaluators
- `external:sha256:f2944b0fca54f5d5a13593c337da8f9887447e447a6ffe2cc7c4731e750cec63::main` (private upstream source, not in this repository)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0533](tfq_0533_mssn_rows_1_to_6_specified.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md:681-684`
  - `external:sha256:ea610e33827464418f0f2786ff65c9af072659bf2884a9411900e07d482e9740:76-78`
  - `external:sha256:ea610e33827464418f0f2786ff65c9af072659bf2884a9411900e07d482e9740:79`
