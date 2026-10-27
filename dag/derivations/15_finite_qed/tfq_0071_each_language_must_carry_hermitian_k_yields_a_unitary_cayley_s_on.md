# [TFQ-0071] Each language must carry: Hermitian K yields a unitary Cayley S on

> **Stage**: `FINITE_QED` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `b1a438ec-f9b7-5abe-bce5-698b8df0a301`  
> **Parent Derivation**: [TFQ-0070](tfq_0070_each_language_must_carry_kellner_value_729_256_hylleraas_sign_change_on_2_9035_2_9030.md)

---

## 1. Abstract & Formal Statement

s_matrix.rs builds an exact finite scattering matrix over Q(i) at a declared energy. from_k takes a Hermitian reaction matrix and returns S = (I + i K)(I - i K)^(-1), then replays unitarity with the shared exact linear algebra. from_unitary refuses a matrix that is not unitary. Non-Hermitian K is refused. Carrier dimension above MAX_SCATTERING_CHANNELS = 128 is refused. transition_operator returns T = (S - I)/(2 i). The file header says this is finite channel scattering at a declared energy, not an asymptotic continuum scattering construction. Modular S-data are left to omega_fusion_categories.

### Governing Obligation
Each language must carry: Hermitian K yields a unitary Cayley S on at most 128 channels, T = (S-I)/(2i), and the construction is not an asymptotic continuum scattering operator.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `complex field C (assumption)`
- **Admitted**: `continuum Hilbert space (assumption)`
- **Admitted**: `continuum path category (assumption)`
- **Admitted**: `refinement system and convergence certificate (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Forward-Euler norm growth 1 + e^2 > 1 vs Cayley norm preservation is mechanized; continuum path-integral convergence remains conditional.

> [!WARNING]
> Z[i] non-field obstruction and discriminant-5 spectral exit from Q(i) are mechanized; continuum Hilbert completion remains an explicit import.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: not located`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:2d9da71f2a615ba2de86c6896030b306594bc1169d72e912cd6e525b06887b66`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0072](tfq_0072_each_language_must_carry_channel_amplitude_optical_defect_finite_born_partial_sum.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
  - `external:git-tree:0fb81f77bbeba84143f574b5a4bc956196140991`
