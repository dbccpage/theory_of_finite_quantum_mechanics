# [TFQ-0026] Add Python and Lean replays of the declared doubling count, or leave

> **Stage**: `FINITE_QCD` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `03e30d86-3d2e-5196-9cae-e241acf96041`  
> **Parent Derivation**: [TFQ-0025](tfq_0025_do_not_let_a_12_decimal_print_authorize_beta0_or_the_creutz_identity.md)

---

## 1. Abstract & Formal Statement

lattice_dirac_doubling.rs declares a Euclidean Clifford family, a period N at least 3, and a rational Wilson coefficient r. The naive operator is the symmetric difference with gamma_mu, and its symbol i sum gamma_mu sin k_mu vanishes at corners k in {0, pi}^d. For even N and periodic boundaries, naive_species_count is 2^d before spin multiplicity. The file states that these counts are computed on declared lattices and that no continuum limit is taken. Carrier dimension above 128 is refused. No matching Python use case was found under 006_finite_qm/python, and FiniteQM.lean has no lattice Dirac theorem.

### Governing Obligation
Add Python and Lean replays of the declared doubling count, or leave the obstruction as Rust-only.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: FiniteQM.lean has no lattice Dirac doubling theorem`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/lattice_dirac_doubling.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no lattice Dirac use case under 006_finite_qm/python`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0027](tfq_0027_do_not_cite_the_three_cycle_charge_doubling_file_as_the_lattice_dirac_obstruction.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
