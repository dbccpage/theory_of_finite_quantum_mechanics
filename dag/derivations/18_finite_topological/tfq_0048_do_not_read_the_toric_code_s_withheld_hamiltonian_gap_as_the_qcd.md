# [TFQ-0048] Do not read the toric code's withheld Hamiltonian gap as the QCD

> **Stage**: `FINITE_TOPOLOGICAL` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `146f88e8-ef14-5c6a-84cd-288d6854c156`  
> **Parent Derivation**: [TFQ-0043](tfq_0043_keep_ribbon_charges_off_the_color_and_wilson_spine.md)

---

## 1. Abstract & Formal Statement

toric_code.rs builds a rectangular CSS code on periodic_square_complex, with a budget of 256 plaquettes. It computes star and plaquette stabilizers, logical operators, distance, ground-state degeneracy, endpoint defects of e and m strings, and the sign of an e loop around an m string. The header says no Hamiltonian gap and no threshold is asserted. That refusal is local to this topological code. It is not the QCD gap in the Creutz discussion, and the Z2 anyon strings are not color-electric flux on the su(3)_c graph. A Kitaev-Preskill entropy of one bit, where the test records it, remains a stabilizer calculation.

### Governing Obligation
Do not read the toric code's withheld Hamiltonian gap as the QCD gap.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: the rectangular toric code is not a FiniteQM QCD theorem`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:18a4dc1ca3a6770620ae1052c15115527d101914c7a984bc359605f26fd06034`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: toric CSS has no finite_qm QCD use case`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0049](tfq_0049_keep_frobenius_and_multiplicity_free_fusion_off_the_missing_color_hopf_algebra.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
