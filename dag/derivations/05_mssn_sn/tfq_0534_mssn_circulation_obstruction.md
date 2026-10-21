# [TFQ-0534] mssn-circulation-obstruction

> **Stage**: `MSSN_SN` | **Status**: `PROVED_LEAN`  
> **UUID**: `075e9e55-a165-5d67-a1da-04817bdfde7f`  
> **Parent Derivation**: [TFQ-0533](tfq_0533_mssn_rows_1_to_6_specified.md)

---

## 1. Abstract & Formal Statement

MssnObstructionDetector.lean defines a Boolean active-obstruction predicate obstP on a passage state with witness pairs, protected pairs and an optional list of observation columns, and shows that it equals the conjunction of four gates: retained, protected, observation declared, and declared observation not separating the pair (obstP_factors, obst_of_gates). On the triangle a→b→c→a it shows that the cycle circulation vanishes on every integer coboundary d₀g (cycle_circulation_coboundary_vanishes), that x = (1,0,0) has circulation 1 (circulation_flux_obstruction), and that no integer potential g has d₀g = (1,0,0) (no_scalar_potential_for_unit_flux). candidateLiftCondition is a necessary condition on supplied metadata, not an implementation of the lift laws or an authorization decision.

### Governing Obligation
Factor obstP into its four gates, show I(d₀g) = 0 for every integer potential and I(1,0,0) = 1, conclude that no potential exists, and keep candidateLiftCondition distinct from a lift.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Supplied observation columns in PState, not a checked partition or the full Genesis passage state (assumption)`

### Further Prerequisites
- [TFQ-0523](tfq_0523_sn_e12_circulation_functional.md) sn-e12-circulation-functional

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The circulation results are relative to the displayed d₀ over ℤ; candidateLiftCondition consumes a supplied Boolean and verifies neither that an edit resolves an obstruction nor that it is authorized, and the Rust audit returns the circulation value without a potential search.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`omega_engine_education/documentation/003_oemssn/lean4/MssnObstructionDetector.lean::circulation_flux_obstruction`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_education/documentation/003_oemssn/lean4/MssnObstructionDetector.lean)
- [`omega_engine_education/documentation/003_oemssn/lean4/MssnObstructionDetector.lean::cycle_circulation_coboundary_vanishes`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_education/documentation/003_oemssn/lean4/MssnObstructionDetector.lean)
- [`omega_engine_education/documentation/003_oemssn/lean4/MssnObstructionDetector.lean::no_scalar_potential_for_unit_flux`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_education/documentation/003_oemssn/lean4/MssnObstructionDetector.lean)
- [`omega_engine_education/documentation/003_oemssn/lean4/MssnObstructionDetector.lean::obstP_factors`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_education/documentation/003_oemssn/lean4/MssnObstructionDetector.lean)
- [`omega_engine_education/documentation/003_oemssn/lean4/MssnObstructionDetector.lean::obst_of_gates`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_education/documentation/003_oemssn/lean4/MssnObstructionDetector.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine_education/documentation/003_oemssn/code/rust/src/obstruction_detector.rs::audit_layer_2_circulation_flux`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_education/documentation/003_oemssn/code/rust/src/obstruction_detector.rs)
- [`omega_engine_education/documentation/003_oemssn/code/rust/src/obstruction_detector.rs::verify_four_gate_factorization`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_education/documentation/003_oemssn/code/rust/src/obstruction_detector.rs)

### Python Oracles & Numerical Evaluators
- `missing obligation: no Python check of the four-gate detector or the triangle circulation in 003_oemssn`

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0535](tfq_0535_mssn_l1_cuts_hodge_rows.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_education/documentation/003_oemssn/lean4/MssnObstructionDetector.lean:4-9`
  - `omega_engine_education/documentation/003_oemssn/lean4/MssnObstructionDetector.lean:123-124`
  - `omega_engine_education/documentation/003_oemssn/lean4/README.md:11`
