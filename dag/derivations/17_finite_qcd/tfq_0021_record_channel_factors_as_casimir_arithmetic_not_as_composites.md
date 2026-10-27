# [TFQ-0021] Record channel factors as Casimir arithmetic, not as composites

> **Stage**: `FINITE_QCD` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `579c8ba7-e6e9-54e9-8de7-dc42fb33d23f`  
> **Parent Derivation**: [TFQ-0020](tfq_0020_call_the_three_diagonal_slots_representation_labels_not_a_completed_color_group.md)

---

## 1. Abstract & Formal Statement

QM-221 projects one-gluon exchange onto four rational channel factors at N_c=3. The color-singlet quark-antiquark factor is -C_F=-4/3, the color-octet factor is 1/6, the symmetric sextet diquark factor is 1/3, and the antisymmetric antitriplet diquark factor is -2/3. Lean suNSingletChannelCoeff, suNOctetChannelCoeff, suNSextetChannelCoeff, and suNAntitripletChannelCoeff record those signs over Rat. The Rust report stores the same four strings. These are quadratic Casimir arithmetic on a three-dimensional matrix carrier. They are not meson or baryon wavefunctions, and they do not state a binding energy.

### Governing Obligation
Record channel factors as Casimir arithmetic, not as composites.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/FiniteQM.lean`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:b76d75cf31011b45adf41918beb988b8a475fb6967032f0649c5a0fb300eba30`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/qcd_beta0_wilson_confinement_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0022](tfq_0022_keep_the_81_entry_fierz_replay_in_rust_and_python_do_not_equate.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
