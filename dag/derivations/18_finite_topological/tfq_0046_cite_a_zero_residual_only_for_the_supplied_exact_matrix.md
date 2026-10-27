# [TFQ-0046] Cite a zero residual only for the supplied exact matrix

> **Stage**: `FINITE_TOPOLOGICAL` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `37fd819d-8548-5339-9c6c-f466a9b6a907`  
> **Parent Derivation**: [TFQ-0045](tfq_0045_admit_an_exchange_only_after_the_exact_inverse_check_and_do_not.md)

---

## 1. Abstract & Formal Statement

yang_baxter_equation.rs keeps the residual matrix of a braid-form defect or of a spectral defect R12(u-v) R13(u) R23(v), including a multiplicative form that divides the spectral parameters. holds is true only when that residual matrix is the zero matrix over the exact scalar field, and first_failing_entry points at a nonzero coordinate. The defect itself is computed by omega_fusion_categories::yang_baxter. There is no tolerance and no floating-point comparison. A zero residual is a finite identity for the matrix that was supplied. It is not a QCD braid of quark color and not a substitute for the Fierz replay.

### Governing Obligation
Cite a zero residual only for the supplied exact matrix.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: the residual matrix test is not in FiniteQM.lean`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:81cef7530a42b0fd9c77ebad734ec9001b102541d55b056c07911c1b8934d0c5`](../../code/rust/src/)
- [`code/rust/src/fusion_categories/yang_baxter.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: Yang-Baxter residual has no finite_qm use case`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0047](tfq_0047_keep_genus_degeneracy_on_the_topological_branch_and_away_from_a_qcd.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
