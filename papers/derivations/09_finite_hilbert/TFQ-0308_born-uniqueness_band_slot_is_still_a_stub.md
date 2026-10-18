# [TFQ-0308] Born-uniqueness band slot is still a stub

> **Stage**: `FINITE_HILBERT` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `462d8349-de7a-5c7a-b0d0-09e386b22fa7`  
> **Parent Derivation**: [TFQ-0307](TFQ-0307_gleason_route_for_dimension_at_least_three.md)

---

## 1. Abstract & Formal Statement

qm_204_born_uniqueness_import_boundary.md and its claim ledger leave QM_204-C0 as a reserved band slot with stub status. The finite obligation is open: the boundary is named, and the slot does not yet carry a self-contained finite certificate separating redundant normalization from uniqueness. Until that slot is written, the working statement stays the conditional section in qm_020 and the leftover list in qm_122, not a new discharge. FiniteQM.lean separates five rational import predicates by countermodels, which is a different and narrower check than Gleason at n at least 3. AuthorityEffect is None.

### Governing Obligation
Leave the QM_204 slot open while it is only a reserved band, and do not promote it.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/FiniteQM.lean`](../../code/lean4/)

### Sovereign Rust Certifiers
*Computational witness tracked under `theory_of_finite_qm` crate.*

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0309](TFQ-0309_ingredient_ladder_stops_before_the_imported_ceiling.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`
