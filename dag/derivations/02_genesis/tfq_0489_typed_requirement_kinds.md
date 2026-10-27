# [TFQ-0489] typed-requirement-kinds

> **Stage**: `GENESIS` | **Status**: `DEFINITION`  
> **UUID**: `4bfe1283-c997-5389-b8a2-5a13781923e4`  
> **Parent Derivation**: [TFQ-0488](tfq_0488_declared_challenge_import_per_level.md)

---

## 1. Abstract & Formal Statement

Declared here as the requirement kinds a challenge import may introduce beyond the sealed one, an ordered pair of admitted data to be separated (a regime with n data has n(n-1)/2 such pairs, allPairs_length). The second derivation's declared stake is the typed extension it ran: a label apart, same or free on every ordered pair of datum indices, free on the diagonal, declared once; a pair is honoured when apart pairs are separable and same pairs collapsed, so its two demand kinds are a held apart pair that is collapsed and a held same pair that is separable. In rung two's menu of nine rules E4 alone generates both demand kinds (continuation §4), and stake invariance for E3, E4 and E6 is OPEN at target-regime transport replay, with no Lean statement about any menu rule (G-3 asks for the other five rules in Lean and E6's invariance). The education audit cites the Desc 64-toggle and KindDesc 1024-member families; in the sealed Lean these count guard toggles (Constitution.allDescs_length) and event-kind enable bits (ControllerCategory.allKinds_length), not requirement kinds.

### Governing Obligation
Type each requirement by kind (separate, apart, same) with its label source, and do not count a requirement kind as available to a stage until its invariance under the declared isomorphism is checked.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared stake of the second derivation, an input declared once (continuation.txt §3 definition 7) (assumption)`

### Further Prerequisites
- [TFQ-0465](tfq_0465_rung2b_stake_menu.md) rung2b-stake-menu

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> No requirement-kind grammar is derived: the stake is a declared input, its invariance for E3, E4 and E6 is OPEN, and the Desc and KindDesc families are guard and event-kind toggles, not requirement-kind families.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/GenesisDerivation/Derivation/Constitution.lean::allDescs_length`](../../../lean4/Imported/GenesisDerivation/Derivation/Constitution.lean)
- [`lean4/Imported/GenesisDerivation/Derivation/ControllerCategory.lean::allKinds_length`](../../../lean4/Imported/GenesisDerivation/Derivation/ControllerCategory.lean)
- [`lean4/Imported/GenesisDerivation/Derivation/Counting.lean::allPairs_length`](../../../lean4/Imported/GenesisDerivation/Derivation/Counting.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust port of the stake menu`

### Python Oracles & Numerical Evaluators
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_stake/rules.py::StakeRule`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_stake/rules.py)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_stake/rules.py::demands`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_stake/rules.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:189-193`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:1071-1072`
  - `external:sha256:0d098004a566c40656af6035d6e66ff13f7e873b11966677df080686a1b29cf9:1100`
