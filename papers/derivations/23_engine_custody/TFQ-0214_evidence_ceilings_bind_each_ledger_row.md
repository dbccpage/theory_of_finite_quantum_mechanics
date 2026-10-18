# [TFQ-0214] Evidence ceilings bind each ledger row

> **Stage**: `ENGINE_CUSTODY` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `844e8df1-0631-592a-9e9f-b273f2b60809`  
> **Parent Derivation**: [TFQ-0213](TFQ-0213_a_claim_ledger_row_is_not_a_proof.md)

---

## 1. Abstract & Formal Statement

Each ledger row a derivation cites must keep its ceiling beside the identifier. On the quantum book, QM-000 is marked candidate_mirror, QM-020-UNIQ is marked continuum_interface, and several rows are source_claim. Where the map uses the label formal_finite_result, the row still has to name a source locus, a hash, assumptions, and replay status. The certifier catalog stores an author-supplied status string while authority_effect on the record remains None. The runtime copies ceiling, assumptions, and replay status with the row. Dropping the ceiling and keeping only the title is a failed binding.

### Governing Obligation
Copy ceiling, assumptions, and replay status with every cited claim identifier.

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
- [`omega_engine/crates_rs/omega_certifiers/src/mathematical_claim.rs`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0215](TFQ-0215_finite_quantum_shelf_is_a_custody_binding.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000:001_from_primitive_difference_to_quantum_mechanics`, `F003.S000`, `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F003_omega_engine/S000_prime_algorithms_and_runtime`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
