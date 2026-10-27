# [TFQ-0060] Each language must carry: C1 = 1/2 exactly, and higher coefficients only

> **Stage**: `FINITE_QED` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `04ac58db-2d31-5412-9887-552078f19169`  
> **Parent Derivation**: [TFQ-0059](tfq_0059_each_language_must_carry_even_leg_wick_pairings_through_20_legs_a_hard.md)

---

## 1. Abstract & Formal Statement

The dressed-graph control encloses a finite truncation of the mass-independent anomalous-moment series with rational intervals. C1 is the exact rational 1/2. C2 and C3 are imported rational linear combinations of periods, and each period is replaced by a finite series with a declared remainder: Machin for pi, a binary series for ln 2 and Li4(1/2), an Apery series for zeta(3), and an Euler-Maclaurin tail for zeta(5). At the declared alpha inverse 137035999166/10^9 the note records a 3-loop truncation whose twelve-digit prefix is 0.001159652231 and a 4-loop window whose width is below 10^-12.

### Governing Obligation
Each language must carry: C1 = 1/2 exactly, and higher coefficients only as named rational interval enclosures with explicit tails, never as a summed continuum series.

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
- [`absent: no local rust twin located for external:sha256:376085dc410bbb86117c8efb40f2280ed15cb5734a22d050f6e1718aef3be579`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/dressed_qed_g2_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0061](tfq_0061_each_language_must_carry_2_forest_f0_equals_the_schur_complement_on_the.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
  - `external:git-tree:0fb81f77bbeba84143f574b5a4bc956196140991`
