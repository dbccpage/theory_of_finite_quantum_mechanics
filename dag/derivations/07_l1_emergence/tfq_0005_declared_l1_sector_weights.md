# [TFQ-0005] Declared L1 sector weights

> **Stage**: `L1_EMERGENCE` | **Status**: `GAP`  
> **UUID**: `2a6092a9-b7d9-5575-b78d-d5a61f3df2f5`  
> **Parent Derivation**: [TFQ-0004](../06_wdp/tfq_0004_witnessed_difference_degree_1_window.md)

---

## 1. Abstract & Formal Statement

No source read for the existing derivation graph derives L1 sector weights from the Phi1 and Gamma2 residual. Weights enter as declared mass, as a definition of a finite residual sector, or as an input to later papers. The three languages must store a finite list of nonnegative weights and the statement that the list was supplied. They must not describe that list as an amplitude, a Born probability, or a consequence of the residual. A later derivation of the weights would replace this gap. It is not written here.

### Governing Obligation
Keep L1 sector weights as declared mass until a derivation from the Phi1 and Gamma2 residual exists.

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

- [TFQ-0006](../08_l1_to_l2/tfq_0006_conditional_finite_hilbert_lift.md)
- [TFQ-0279](../08_l1_to_l2/tfq_0279_finite_nonnegative_sector_weights.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/shelf.yaml`
