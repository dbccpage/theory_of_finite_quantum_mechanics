# [TFQ-0069] Each language must carry the Uehling prefix and the Lamb bands only

> **Stage**: `FINITE_QED` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `ddc50e06-b292-59dd-8ab5-b0ae303c3009`  
> **Parent Derivation**: [TFQ-0068](tfq_0068_each_language_must_carry_n_2_coefficients_5_128_5_128_and_1_128_splitting_1_32.md)

---

## 1. Abstract & Formal Statement

The Lamb finite map in this tree is the pair of interval certificates, not a continuum self-energy integral. QM-216 stores the Uehling megahertz prefix -27.128756729153. QM-224 combines the contact 91/120 with a declared Bethe-log window and records a one-loop non-recoil band, a reduced-mass band, and a two-loop band that the note places around 1057.845 MHz. Those bands use CODATA-style and Bethe inputs as exact rationals or rational intervals. verify_qm224_dirac_coulomb_and_lamb_shift returns a typed certificate or an AtomicPhysicsError.

### Governing Obligation
Each language must carry the Uehling prefix and the Lamb bands only as interval membership under the declared alpha, mass-ratio and Bethe-log inputs.

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

- [TFQ-0070](tfq_0070_each_language_must_carry_kellner_value_729_256_hylleraas_sign_change_on_2_9035_2_9030.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
  - `external:git-tree:0fb81f77bbeba84143f574b5a4bc956196140991`
