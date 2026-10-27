# [TFQ-0453] minimal-or-initial-refused

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `677ff5ab-6652-5c00-bbf4-9c8d2c9479d7`  
> **Parent Derivation**: [TFQ-0451](tfq_0451_no_endogenous_demand_generator.md)

---

## 1. Abstract & Formal Statement

Question 10 asks whether the final process is minimal or initial among a defined class of finite processes satisfying the same challenges. The sealed answer is that the claim is refused and tagged unresolved: no such initiality or minimality property was established. What is established is narrower: determinism of the artifacts across the exercised runs and platforms is a finite computation (byte-identical artifacts are repeated-run agreement, not an engine theorem), completeness of enumerations within declared bounds is a bounded theorem under its ledger conditions, and the per-stage minimality and uniqueness results are theorems with their stated scopes. An earlier wording, what is proved: determinism of the engine, was corrected on 2026-09-08.

### Governing Obligation
Refuse any minimality or initiality claim for the whole process, and keep artifact determinism, bounded enumeration completeness and per-stage minimality under their own tags.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> An explicit clock-closed observed-process class now has a proved initiality obstruction, including the actual source-regime supply self-loop, and a reachable/reduced finite-model minimum-state criterion. These supplementary results do not certify the full Alpha engine, its class membership, or minimum program/declaration cost; the historical refusal remains accurate.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/GenesisProcessComparison.lean::GenesisProcessComparison.all_words_agree`](../../../lean4/GenesisProcessComparison.lean)
- [`lean4/GenesisProcessComparison.lean::GenesisProcessComparison.all_words_minimum_size`](../../../lean4/GenesisProcessComparison.lean)
- [`lean4/GenesisProcessComparison.lean::GenesisProcessComparison.no_clock_hom_of_self_loop`](../../../lean4/GenesisProcessComparison.lean)
- [`lean4/GenesisProcessComparison.lean::GenesisProcessComparison.no_initial_in_clock_closed_class`](../../../lean4/GenesisProcessComparison.lean)
- [`lean4/GenesisProcessComparison.lean::GenesisProcessComparison.no_source_initial_in_clock_closed_class`](../../../lean4/GenesisProcessComparison.lean)
- [`lean4/GenesisProcessComparison.lean::GenesisProcessComparison.nonminimal_adequate_process`](../../../lean4/GenesisProcessComparison.lean)
- [`lean4/GenesisProcessComparison.lean::GenesisProcessComparison.source_run_matches`](../../../lean4/GenesisProcessComparison.lean)
- [`lean4/GenesisProcessComparison.lean::GenesisProcessComparison.source_supply_self_loop`](../../../lean4/GenesisProcessComparison.lean)
- `missing obligation: no Lean statement of minimality or initiality among finite processes satisfying the sealed challenges`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust check; artifact determinism is repeated-run byte agreement, not a program`

### Python Oracles & Numerical Evaluators
- [`checks/independent/pgw-minimal-or-initial-refused.py`](../../../checks/independent/pgw-minimal-or-initial-refused.py)
- `missing obligation: no Python check; artifact determinism is repeated-run byte agreement, not a program`

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt:623-633`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt:626-629`
  - `lean4/Imported/Genesis19l57g1/Derivation/Initiality.lean:49-52`
  - `dag/derivations/independent/pgw-minimal-or-initial-refused.md:1`
