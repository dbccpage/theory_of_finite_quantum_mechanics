# [TFQ-0084] Finite quantum-gravity shadow

> **Stage**: `FINITE_QG` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `338b3e14-5d40-5f7a-8ed0-e0a22d7c4a63`  
> **Parent Derivation**: [TFQ-0008](../11_finite_qm_dynamics/tfq_0008_finite_dynamics_instruments_and_channels.md)

---

## 1. Abstract & Formal Statement

A finite gravity shadow is relational point coincidence, a Regge deficit on a finite simplicial complex, a spin-foam or area-spectrum control, and the kinematical shadows named in the quantum-foundations notes. The exact rational proxy that sums squared areas times deficits is not the Einstein-Hilbert action. The float script l1_regge.py is not that proxy. The three languages must say which finite identity they check. A certificate on a small complex is not quantum gravity, and it is not a derivation of the Einstein equation.

### Governing Obligation
Keep Regge, spin-foam, and relational certificates finite and separate from the Einstein equation.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Formalization
*Formalization active. Proof obligations tracked under zero-sorry regime.*

### Sovereign Rust Certifiers
*Computational witness tracked under `theory_of_finite_qm` crate.*

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0085](../20_continuum_interface/tfq_0085_open_finite_to_continuum_interface.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F002.S000`, `F000.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/shelf.yaml`

---

## 6. Narrowed census (2026-10-24)

Status stays OPEN. The census is the integer boundary in `dag/derivations/independent/tfq-0084.md` and `lean4/CampaignTfq0084ReggeProxyBoundary.lean`.

On the declared pairs (area-square, defect) = (1, 2) and (4, 5), the sum of products is 22 and the defect sum is 7. 22 ≠ 7 and 22 ≠ 0. The pairs are declared integers, not areas read from a manifold.

For inputs 1/3, 1/4, 2, and 1/16, the difference numerator is 1 and the denominator is 12. The squared-gap denominator is 144. The allowance 2*(1/16) reduces to 1/8, and the squared allowance has denominator 64. 1*64 < 1*144, so 1/144 < 1/64. On the second inputs, 1*16 > 1, so 1 > 1/16. The comparison -1 < 0 holds.

`einstein_hilbert_fence` returns `rational_regge_proxy`. `flat_einstein_hilbert` returns `BigRational::zero()`. The float script `papers/core/constraint_closure/code/l1_regge.py` is a separate text. This census leaves a continuum Einstein equation, a spin-foam sum, an area spectrum, and relational point coincidence open.
