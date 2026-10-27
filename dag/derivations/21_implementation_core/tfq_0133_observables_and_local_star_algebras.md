# [TFQ-0133] Observables and local star algebras

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `b0b42608-dfe8-5e77-94d0-5605adab58dd`  
> **Parent Derivation**: [TFQ-0131](tfq_0131_density_operators_over_q_i.md)

---

## 1. Abstract & Formal Statement

Covers observable.rs, hermitian_spectral.rs, commutator.rs, commuting_observables.rs, local_operator_algebra.rs, superselection_sector.rs, and algebraic_qft.rs. observable.rs takes an observable to be an exact Hermitian over Q(i), with rational expectation and a checked Robertson-Schrodinger comparison. The other files isolate bounded-dimension eigenvalues, record the Weyl commutator, finite star-subalgebras, superselection, and local nets that do not establish continuum Haag duality. A Python replay and a Lean 4 declaration would still have to match the exact expectation and that net boundary.

### Governing Obligation
Match exact rational expectations of Hermitian observables and the statement that finite local nets do not establish continuum Haag duality.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: no local lean twin located for lean4/quantum_mechanics`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:d2174cadc3e253afb3631b8aa626911a607a1f18ee82be59b0f8c32d2708fd8f`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:7a5a4b3d6e1f9185b75b7b143c03a40c4838e58cffd4a77e2c900968c4467ba7`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:aaa24b2955f9d6b460c2aec041d1c9ebfa58a61bf4056394a372e45942b81f40`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:f2a261d179774c9344c1bf8ae35a9e0b8229111bf48e6304162794f776843999`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:54341faf5455b48716dd42f351b6727b58d7fa6ce32fee5ae1f30bd626712559`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:f61366a09184ce73ed59f4266bad09e884dd5c9815f5b35b30eebdecd24185eb`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:2c3063603fd3462c580b0cbfda3f2af787a0b06292ac7ea296360d6330ce0139`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: The python twin is not located for observable.rs under 006_finite_qm/python/finite_qm.`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0134](tfq_0134_pauli_group_and_exchange_characters.md)
- [TFQ-0137](tfq_0137_unitary_steps_and_hamiltonians.md)
- [TFQ-0144](tfq_0144_projective_measurement_and_instruments.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
