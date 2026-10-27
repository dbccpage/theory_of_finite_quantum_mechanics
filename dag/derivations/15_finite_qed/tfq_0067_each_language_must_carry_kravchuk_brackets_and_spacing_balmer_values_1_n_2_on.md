# [TFQ-0067] Each language must carry: Kravchuk brackets and spacing, Balmer values -1/n^2 on

> **Stage**: `FINITE_QED` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `d4f12d15-46ef-5fd3-a2d1-1c27586aee8a`  
> **Parent Derivation**: [TFQ-0066](tfq_0066_each_language_must_carry_the_twelve_digit_prefixes_for_pi_r_9_m_2_4_the_running.md)

---

## 1. Abstract & Formal Statement

algebraic_bound_state_spectra.rs computes finite su(2) and so(4) spectra over Q. For N = 2j in {1,2,3,4} the Kravchuk ladder satisfies the sl(2) brackets, the Casimir j(j+1), and G-adjointness without square roots. The shifted Hamiltonian is the diagonal of half-integers from 1/2 through 2j+1/2 with spacing 1. Ground second moments of the scaled quadratures are 1/4 and saturate the discrete Robertson relation. On the hydrogen shell of dimension n^2 the Pauli Hamiltonian is -1/n^2. Projectors Pi_2S = I - L^2/2 and Pi_2P = L^2/2 split the n=2 shell into traces 1 and 3, commute with L, and fail to commute with K_z.

### Governing Obligation
Each language must carry: Kravchuk brackets and spacing, Balmer values -1/n^2 on n^2 shells, 2S/2P projector traces 1 and 3, and the contact enclosure at coefficient 91/120.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `completion to R/C, Stone, period integrals (lift)`
- **Admitted**: `each row s5.2 "Residual import" column (assumption)`
- **Admitted**: `finite dimension (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> All finite rational/integer control theorems for QM-207..231 are mechanized; continuum completions in QM-207..211 remain priced as explicit imports.

> [!WARNING]
> General n is prose; Lean is 2x2 (integer/rational entries).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: not located`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:a10da92df13ef926419410d2e5c98c7366f31aa5dd28fa48718916ad8f904b62`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/algebraic_bound_state_spectra_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0068](tfq_0068_each_language_must_carry_n_2_coefficients_5_128_5_128_and_1_128_splitting_1_32.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
  - `external:git-tree:0fb81f77bbeba84143f574b5a4bc956196140991`
