# [TFQ-0281] Residual mass to a declared diagonal

> **Stage**: `L1_TO_L2` | **Status**: `SOURCE_RECORD`  
> **UUID**: `dee8fb9b-d0af-5456-b67e-390d40e884c9`  
> **Parent Derivation**: [TFQ-0280](tfq_0280_finite_repair_cokernel_as_a_quotient_norm.md)

---

## 1. Abstract & Formal Statement

qm_003_residual_density_calculus_l1_l2_boundary.md normalizes finite nonnegative residual masses with positive total into sector weights and places those weights on a diagonal matrix. The finite obligation is that diagonal presentation: nonnegative diagonal entries, trace one, and recovery of the weights by a declared basis measurement. The claim ledger types phase and sign data as not fixed by those weights. A pure-state projector with the same populations is a different object, and the stub says the two disagree in purity on a three-weight example. Imports: a declared representative, not a quotient invariant.

### Governing Obligation
Normalize residual mass only on a declared representative and keep the diagonal report orientation-blind.

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

- [TFQ-0282](tfq_0282_diagonal_presentation_and_lost_total_scale.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000`, `F000.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/shelf.yaml`
