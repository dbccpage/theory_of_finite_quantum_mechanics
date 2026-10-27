# [TFQ-0462] rung0-inheritance-replay

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `02afe41a-eeda-5192-97b5-ad5c157ece12`  
> **Parent Derivation**: [TFQ-0461](tfq_0461_genesis_three_axis_verdict.md)

---

## 1. Abstract & Formal Statement

Rung zero of the second derivation (pull request 130) answers Challenge 0 at stated scope: the sealed challenge reports and both sealed closed baselines regenerate exactly (reading L, 4 nodes, 3 terminal; reading F, 20 nodes, 16 terminal). The sealed grammar has six event kinds, of which only the supply preserves the state, and the two remaining declared inputs are named: the stake and the stream. Inertia is a finite computation from both readings: up to eight supplies leave the regime unchanged, and growth to five data under the all-free stake admits no form, raises no demand and leaves every state totally collapsed. The only Lean evidence cited is the sealed supply_no_op.

### Governing Obligation
Replay the sealed receipts byte for byte, census the six event kinds and the two declared inputs, and check inertia from both sealed readings to eight supplies and five data under no stake and under the all-free stake.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Sealed genesis kernel, its receipts and the two sealed Python genesis readings L and F as bases (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> A finite computation to eight supplies and five data plus the sealed supply_no_op; it does not show that nothing follows from the inheritance beyond those bounds, and rung zero is not blind to its author's expectation, since the seed's author ran it.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/GenesisDerivation/Derivation/Inertia.lean::supply_no_op`](../../../lean4/Imported/GenesisDerivation/Derivation/Inertia.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/supply.rs::supply`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/supply.rs)

### Python Oracles & Numerical Evaluators
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_inheritance/inheritance.py::all_free_growth`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_inheritance/inheritance.py)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_inheritance/inheritance.py::supplies_are_inert`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_inheritance/inheritance.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0463](tfq_0463_rung1_stream_as_response.md)
- [TFQ-0464](tfq_0464_rung2a_stake_declared_label.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:258`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:342-350`
  - `github:dbccpage/19L57G1@85a83ae7c/research/second/claim_ledger.md:104`
