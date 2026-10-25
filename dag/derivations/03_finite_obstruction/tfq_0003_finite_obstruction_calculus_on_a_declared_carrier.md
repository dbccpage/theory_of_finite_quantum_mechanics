# [TFQ-0003] Finite obstruction calculus on a declared carrier

> **Stage**: `FINITE_OBSTRUCTION` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `da17a26b-624d-5a88-9183-1ef5a3ddf622`  
> **Parent Derivation**: [TFQ-0002](../02_genesis/tfq_0002_genesis_regime_events_as_a_separate_admission_record.md)

---

## 1. Abstract & Formal Statement

On one declared carrier, the integer 1-cochains (z0, z1, z2) of the 3-cycle, comparison by those integer entries, and coboundary (d0 h) = (h1 - h0, h2 - h1, h0 - h2): for every cochain c and every vertex cochain h, the holonomy of c - d0 h equals the holonomy of c, where holonomy is the sum of the three entries. A cochain is a coboundary if and only if its holonomy is 0. Two cochains lie in the same coboundary coset if and only if their holonomies agree. Phi1(c), the absolute value of the holonomy, lower-bounds the unweighted L1 norm of every cochain in the class and is attained by the classical residual (holonomy, 0, 0) and by (0, holonomy, 0). If the holonomy is not 0, those two residuals differ. Gamma2 in this finite case is that holonomy, and the coboundary gauge leaves it unchanged. For the cochain (1, -2, 4) the holonomy is 3, Phi1 is 3, and the unweighted L1 norm is 7, so that cochain is not a Phi1 minimizer.

The shelf obligation that remains open is the original one: F000 admits finite sets, typed distinction steps, combinatorial coboundaries, and finite witness functionals, and the shelf book states that the volume is not by itself a completed pass from Genesis into the obstruction calculus. A witness with the same statement in Python, Rust, and Lean 4 is not supplied here. A Lake build of the Lean module is not that correspondence.

### Governing Obligation
Still open: one witness of this signature stated the same way in Python, Rust, and Lean 4. This module is only the Lean side of one unweighted 3-cycle, and a Lake build of it is not that correspondence. The shelf reading that the F000 volume is not by itself a completed pass from Genesis into the obstruction calculus is not a theorem of this note. Weighted edge masses, any complex other than this 3-cycle, and any Gamma2 other than the holonomy, including a sum of squares of weights, remain open.

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

- [TFQ-0004](../06_wdp/tfq_0004_witnessed_difference_degree_1_window.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/shelf.yaml`
