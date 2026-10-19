# [TFQ-0289] Diagonal density with coherences unfixed

> **Stage**: `FINITE_HILBERT` | **Status**: `SOURCE_RECORD`  
> **UUID**: `ee30af94-3251-5b9f-b3de-57e7872f0af7`  
> **Parent Derivation**: [TFQ-0288](../08_l1_to_l2/tfq_0288_pairing_audit_does_not_select_the_born_row.md)

---

## 1. Abstract & Formal Statement

qm_012_density_matrices_as_diagonal_residual_weights.md reads a finite residual-weight distribution as a diagonal density: nonnegative diagonal, trace one, and purity equal to the sum of squared weights. The finite obligation is that diagonal carrier and the purity number computed from the weights alone. Off-diagonal coherences are not fixed by the weights. The note calls them the same non-forced lift that the Born paper found for a Hilbert encoding, so coherence is an import. The claim ledger points at a mechanization name that this record does not replay. AuthorityEffect is None.

### Governing Obligation
Keep diagonal residual weights as a trace-one population shadow and import any off-diagonal coherence.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/lean4/FromPrimitiveDifferenceToQuantumMechanics/FiniteDensity.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/density_matrix.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/python/src/finite_quantum/density_matrix.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0290](../08_l1_to_l2/tfq_0290_direct_normalization_of_sector_weights.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`
