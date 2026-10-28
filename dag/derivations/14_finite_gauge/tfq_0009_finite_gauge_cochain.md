# [TFQ-0009] Finite gauge cochain

> **Stage**: `FINITE_GAUGE` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `f5035e38-3362-5fdc-8586-8d2caabbba12`  
> **Parent Derivation**: [TFQ-0008](../11_finite_qm_dynamics/tfq_0008_finite_dynamics_instruments_and_channels.md)

---

## 1. Abstract & Formal Statement

A finite gauge step is a cochain of group-valued or Hopf-valued data on a finite complex, together with holonomy around finite loops and a coboundary that plays the role of curvature. tfqm_holonomy is a zero-float discrete holonomy library and is a control, not this derivation. The three languages must share one finite complex, one coefficient object, and one holonomy identity. U(1) and a non-abelian color shadow fork after this node. Neither fork is continuum Yang-Mills theory.

### Governing Obligation
Define connection, holonomy, and curvature on a finite complex before any continuum gauge theory.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Formalization (`lean4/FiniteGaugeCochainHolonomy.lean`)
- `FiniteGaugeCochainHolonomy.chain_boundary_squared_zero_on_plaquette`: Proves that the 0-chain boundary of the 1-chain square plaquette boundary vanishes at every vertex (`∂₁ ∘ ∂₂ = 0`).
- `FiniteGaugeCochainHolonomy.shared_edge_cancellation_two_plaquettes`: Proves that combining two adjacent square plaquettes with equal orientation cancels their oppositely oriented shared interior edge.
- `FiniteGaugeCochainHolonomy.abelian_cochain_coboundary_squared_zero`: Proves that the plaquette coboundary `d₁` of a pure-gauge 0-cochain coboundary `d₀ λ` vanishes identically (`d₁ ∘ d₀ = 0`).
- `FiniteGaugeCochainHolonomy.abelian_curvature_gauge_invariant`: Proves that abelian plaquette curvature `d₁ A` is strictly invariant under any vertex gauge transformation `A ↦ A + d₀ λ`.
- `FiniteGaugeCochainHolonomy.abelian_bianchi_identity_cube`: Proves the discrete abelian Bianchi identity (`d₂ ∘ d₁ = 0`) on the 6-face, 12-edge 3-cube complex.
- `FiniteGaugeCochainHolonomy.nonabelian_holonomy_conjugation_identity`: Proves the telescoping non-abelian plaquette holonomy conjugation identity `H(U^g) = g₀ H(U) g₀⁻¹` around the 4-edge square loop.
- `FiniteGaugeCochainHolonomy.nonabelian_wilson_loop_trace_gauge_invariant`: Proves cyclic trace invariance and Wilson loop trace gauge invariance `tr(g₀ H g₀⁻¹) = tr(H)`.
- `FiniteGaugeCochainHolonomy.abelian_vs_nonabelian_fork_commutator_witness`: Exhibits the fork between commutative abelian link addition and non-commutative `SL(2, ℤ)` shear links with non-central basepointed holonomy conjugation.
- `FiniteGaugeCochainHolonomy.finite_cochain_cardinality_and_quotient_bound`: Evaluates the finite cardinality `N^E` of `ℤ/Nℤ` 1-cochains on an `E`-edge complex (`2^4 = 16`, `8^4 = 4096`).
- `FiniteGaugeCochainHolonomy.combinatorial_coboundary_metric_free_vs_yang_mills_action_fence`: Proves that the combinatorial curvature coboundary `d₁ A` is metric-free whereas the Yang-Mills plaquette action `w * (d₁ A)²` depends on an unimported metric coupling `w = 1 / g²`.

### Independent Python Verification (`checks/independent/tfq-0009.py`)
- Executes `6263` exact integer and rational checks across plaquette boundary exactness, abelian coboundary and 3-cube Bianchi identities, `SL(2, ℤ)` non-abelian holonomy conjugation and Wilson loop trace invariance, and the Yang-Mills metric-coupling fence (`0` failures).

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0010](../15_finite_qed/tfq_0010_finite_qed_and_electroweak_shadow.md)
- [TFQ-0011](../17_finite_qcd/tfq_0011_finite_qcd_shadow.md)
- [TFQ-0012](../17_finite_qcd/tfq_0012_locate_a_hopf_gauge_file_or_keep_the_gauge_datum_as_the.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
  - `external:sha256:9504a35b2a33de8f85af42c874eb8da62364cbb364219de602dcfa98b26569e1`
