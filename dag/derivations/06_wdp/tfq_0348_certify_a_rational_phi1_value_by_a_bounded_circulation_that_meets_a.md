# [TFQ-0348] Certify a rational Phi1 value by a bounded circulation that meets a

> **Stage**: `WDP` | **Status**: `SOURCE_RECORD`  
> **UUID**: `4f0476d6-1a5b-54c7-84af-a9ef8eb5ffad`  
> **Parent Derivation**: [TFQ-0345](tfq_0345_on_a_declared_window_with_d1_d0_0_compute_q1_kappa1.md)

---

## 1. Abstract & Formal Statement

WDP-CH04-P07 states that over Q, with positive rational weights, any circulation y with d0-star y equal to zero and absolute values bounded by the weights gives a pairing at most Phi1,w, so a repair and such a circulation with equal values certify the value without importing strong duality. WDP-CH04-P08 records the filled triangle with edges (01, 12, 02) and delta (1, 1, 0): Phi1 = 2 at f = (0, 1, 0), dual y = (1, 1, -1), Gamma2 = 2, and R_cl = 1. obstruction.rs says it emits a Kirchhoff divergence-free dual witness with zero duality gap against Phi1, using an exact rational simplex.

### Governing Obligation
Certify a rational Phi1 value by a bounded circulation that meets a repair, as on the filled triangle, without treating that certificate as a Genesis derivation of the window.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Norm hypothesis over R, C, or Q restricted from the real extension (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Ledger rows carry prose (P03) and prose plus computed (P04, P05) bindings, no L: binding. Lean symbols with matching names exist in Obstruction.lean (not checked against statements); they cover the exact sequence and ratio bounds at the symbols named, not necessarily every clause (claim_map.md not re-checked row by row).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Formalization
*Formalization active. Proof obligations tracked under zero-sorry regime.*

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/wdp/obstruction.rs`](../../code/rust/src/)
- [`code/rust/src/wdp/fenchel_duality.rs`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0548](tfq_0548_wdp_filled_triangle.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:
