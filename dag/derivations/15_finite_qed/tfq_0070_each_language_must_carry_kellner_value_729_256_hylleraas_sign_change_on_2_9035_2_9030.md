# [TFQ-0070] Each language must carry: Kellner value -729/256, Hylleraas sign change on [-2.9035,-2.9030],

> **Stage**: `FINITE_QED` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `63fc5ee7-3b6b-5deb-b447-9191cd2cb0fb`  
> **Parent Derivation**: [TFQ-0069](tfq_0069_each_language_must_carry_the_uehling_prefix_and_the_lamb_bands_only.md)

---

## 1. Abstract & Formal Statement

QM-225, in the same atomic file, computes finite helium and closed-shell screening identities. The product trial energy is Z_eff^2 - (27/8) Z_eff, so the stationary value at 27/16 is -729/256 and the virial combination vanishes there. The bare perturbation value at Z_eff = 2 is -11/4. The four-term Hylleraas secular determinant at 2 zeta = 73/20 changes sign between -2.9035 and -2.9030 hartree. Slater integrals give J = 34/81 and K = 32/729 at Z = 2, so the para-ortho gap is 64/729. The Roothaan screening map is claimed contractive with factor 1/4 on the declared He, Be and Ne shells.

### Governing Obligation
Each language must carry: Kellner value -729/256, Hylleraas sign change on [-2.9035,-2.9030], exchange gap 64/729, and screening contraction factor 1/4 on the declared shells.

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
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/atomic_dirac_lamb_hartree_fock.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/atomic_dirac_lamb_hartree_fock_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0071](tfq_0071_each_language_must_carry_hermitian_k_yields_a_unitary_cayley_s_on.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent`
