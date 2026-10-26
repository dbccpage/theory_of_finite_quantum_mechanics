# [TFQ-0511] sn0-ground-inertia

> **Stage**: `MSSN_SN` | **Status**: `PROVED_LEAN`  
> **UUID**: `59269d06-9e1f-5766-aa4a-9f8e5c5c9024`  
> **Parent Derivation**: [TFQ-0510](tfq_0510_sn_two_boxed_laws.md)

---

## 1. Abstract & Formal Statement

S(0) supplies the literal <> as one opaque token: one presentation-token slot and two ASCII bytes, and neither count is the number of admitted data. In the sealed Genesis model nothing is derivable at genesis (genesis_underivable) and a bare supply leaves every regime unchanged (supply_no_op). The sealed Challenge 0 computation records admitted data empty in reading L and the single opaque datum in reading F, with no internal observables in either reading. The local S(n) Lean model has carrierCard 0 = 0 beside the two-character wire form of the ground token (ground_presentation_vs_carrier), and Carrier 0 has no inhabitant (ground_carrier_empty).

### Governing Obligation
Keep the two-byte, one-token presentation <> apart from the admitted carrier: at S(0) nothing is derivable, supply changes no admitted state, and the declared index-0 carrier has no element.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared S(n) example carrier table carrierCard in SnCarrier.lean, chosen and not derived from 19L57G1 (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Zero admitted data is the reading-L and initial-regime statement; in reading F the inscription <> is the single admitted datum after its admission event, so the education phrase does not cover reading F. ground_carrier_empty concerns the declared example carrier, not a source replay.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean::genesis_underivable`](../../../lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean::supply_no_op`](../../../lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean)
- [`lean4/Imported/OeSn/SnTheorems.lean::ground_carrier_empty`](../../../lean4/Imported/OeSn/SnTheorems.lean)
- [`lean4/Imported/OeSn/SnTheorems.lean::ground_presentation_vs_carrier`](../../../lean4/Imported/OeSn/SnTheorems.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust check of the S(0) ground in the S(n) strand`

### Python Oracles & Numerical Evaluators
- `omega_engine_education/documentation/002_oesn/code/sn_core.py::S0Ground` (private upstream source, not in this repository)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0512](tfq_0512_sn1_supply_not_admission.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:218-221`
  - `omega_engine_education/documentation/002_oesn/levels/level_00_ground.md:19-22`
  - `omega_engine_education/documentation/002_oesn/sn.md:44-45`
