# [TFQ-0068] Each language must carry: n=2 coefficients 5/128, 5/128 and 1/128, splitting 1/32,

> **Stage**: `FINITE_QED` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `f052d85a-9b92-5648-8c91-2b229c2d075a`  
> **Parent Derivation**: [TFQ-0067](tfq_0067_each_language_must_carry_kravchuk_brackets_and_spacing_balmer_values_1_n_2_on.md)

---

## 1. Abstract & Formal Statement

atomic_dirac_lamb_hartree_fock.rs evaluates QM-224 rational fine-structure coefficients. dirac_coulomb_alpha4_coeff and verify_qm224_dirac_coulomb_and_lamb_shift decompose the n=2 order-alpha^4 pieces: 2S is 13/128 - 8/128 = 5/128, 2P with j=1/2 is 7/384 + 8/384 = 5/128, and 2P with j=3/2 is 3/384 = 1/128. The j=1/2 levels therefore match at this order, and the 2P splitting coefficient is 1/32. The Lamb contact stored by the certificate is again 91/120. FiniteQM.lean, which is not a filename-stem twin, contains dirac_coulomb_fine_structure_n2_and_darwin_spin_orbit_degeneracy and.

### Governing Obligation
Each language must carry: n=2 coefficients 5/128, 5/128 and 1/128, splitting 1/32, and Lamb contact 91/120, with alpha^6 and the Bethe logarithm left imported.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `completion to R/C, Stone, period integrals (lift)`
- **Admitted**: `each row s5.2 "Residual import" column (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> All finite rational/integer control theorems for QM-207..231 are mechanized; continuum completions in QM-207..211 remain priced as explicit imports.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: not located`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:dee13d74d257e960c55d1b3da0a35f7276c33ede91adba5203a17a7bb91cb34f`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/atomic_dirac_lamb_hartree_fock_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0069](tfq_0069_each_language_must_carry_the_uehling_prefix_and_the_lamb_bands_only.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
  - `external:git-tree:0fb81f77bbeba84143f574b5a4bc956196140991`
