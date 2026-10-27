# [TFQ-0425] forced-separation-lift-not-unique

> **Stage**: `PREGENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `1f1e47f1-86d8-54df-ad7a-8d50ee91e39d`  
> **Parent Derivation**: [TFQ-0424](tfq_0424_absence_of_rule_not_identification.md)

---

## 1. Abstract & Formal Statement

Suppose an external task requires <a> and <ab> to differ while the current regime has <a> ≈ₙ <ab>. Every operation f on the quotient S_n/≈ₙ gives f([<a>]) = f([<ab>]), so no operation on the current quotient answers the task on every input, and a refinement adding at least one observation o with o(<a>) ≠ o(<ab>) is forced; the analysis gives this as an argument with proof. The lift is not unique: under a supplied string decoder, 'payload has more than one position' and 'payload contains b' both separate <a> from <ab> but disagree on <aa> (true and false), and full inscription identity also separates the pair while carrying more than one bit. A canonical tower therefore needs a declared minimality or initiality policy, such as fewest new predicates, minimum description length, maximal preservation of old equivalences, a free or initial completion, or retention of every tied minimum branch.

### Governing Obligation
Refuse any answer to a separation task computed only from the collapsed quotient, require an added separating observation, and keep every tied separating predicate as a branch unless a declared minimality or initiality policy selects one.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Supplied string decoder for the payloads of <a>, <ab> and <aa>, used only by the non-uniqueness example (assumption)`

### Further Prerequisites
- [TFQ-0365](tfq_0365_collapsed_observation_barrier.md) collapsed-observation-barrier

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The Lean declarations cover the quotient barrier; the non-uniqueness of the lift rests on the two-predicate example, and no selection policy, fixed ladder of quotients or minimal multiplicity lift is derived.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/GenesisDerivation/Derivation/Quot.lean::quotient_barrier`](../../../lean4/Imported/GenesisDerivation/Derivation/Quot.lean)
- [`lean4/Imported/GenesisDerivation/Paper000.lean::separation_not_on_quotient`](../../../lean4/Imported/GenesisDerivation/Paper000.lean)
- [`lean4/Imported/PreGenesisToMssn/Observation.lean::collapsed_quotient_barrier`](../../../lean4/Imported/PreGenesisToMssn/Observation.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/code/rust/src/main.rs::factor`](../../../atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/code/rust/src/main.rs)

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/genesis/code/genesis_checks.py::quotient_factor`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/genesis_checks.py)
- [`atlas/papers/finite_obstruction_calculus/genesis/code/tests/test_genesis_checks.py::test_quotient_and_history_refuse_collapsed_answers`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/tests/test_genesis_checks.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/paper.md:118-133`
  - `external:sha256:0a9068781f8c282418f8ae2933ae6502b1bef56df91c16758cf730de1e359149:283-305`
  - `external:sha256:1713d12cc07cce5f295bb69922c49e278be2277c31d4fecee6b41ecb87d639bb:81-88`
