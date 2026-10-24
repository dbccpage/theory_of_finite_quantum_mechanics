# [TFQ-0017] Do not promote the SU(2) quaternion shadow to su(3)_c

> **Stage**: `FINITE_QCD` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `8f94210b-4e82-5312-9072-19e7a34d28b5`  
> **Parent Derivation**: [TFQ-0016](tfq_0016_su2_spinor_and_quaternion_shadow.md)

---

## 1. Abstract & Formal Statement

quaternion_gauge_shadow.rs says each listed Q8 element lies in SU(2) by the special-unitary check, and it says explicitly that Q8 is a finite subgroup of SU(2), not SU(2) itself. su2.rs holds quaternions, the adjoint cover, spinor norms, and binary polyhedral groups. Those constructions give a finite non-abelian shadow with a two-dimensional carrier. They do not provide the three diagonal color labels used by the weighted Gell-Mann family. Promoting Q8 flux operators to a stand-in for su(3)_c would skip the separate generator control. The obligation is to keep this SU(2) shadow on the gauge side of the cut.

### Governing Obligation
Do not promote the SU(2) quaternion shadow to su(3)_c.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems (`lean4/CampaignTfq0017FiniteQcd.lean`)
- `CampaignTfq0017FiniteQcd.quat_norm_multiplicative_four_square_identity`: Proves Euler's four-square spinor norm multiplicativity `quatNormSq (p * q) = quatNormSq p * quatNormSq q`.
- `CampaignTfq0017FiniteQcd.q8_proper_subgroup_of_su2_pythagorean_witness`: Proves that the rational Pythagorean quaternion `(3/5, 4/5, 0, 0)` has unit spinor norm `1` outside the 8 integer units of `Q_8` (`Q_8 ⊂neq SU(2)`).
- `CampaignTfq0017FiniteQcd.su2_adjoint_cover_two_to_one_kernel`: Proves that `q` and `-q` induce identical adjoint conjugation `quatAdjoint (±q) v` while `1 ≠ -1` (the 2-to-1 `SU(2) → SO(3)` cover).
- `CampaignTfq0017FiniteQcd.binary_polyhedral_orders_and_2d_carrier`: Verifies the binary polyhedral subgroup orders `|Q_8| = 8`, `|2T| = 24`, `|2O| = 48`, `|2I| = 120` and `2 ≠ 3` carrier dimension.
- `CampaignTfq0017FiniteQcd.su2_cartan_rank_one_vs_su3_gell_mann_cartan_rank_two_fence`: Contrasts the 1-parameter 2D traceless diagonal `d₂ = -d₁` against the two traceless 3-color Gell-Mann diagonal profiles `λ₃ = (1, -1, 0)` and `λ̃₈ = (1, 1, -2)`.
- `CampaignTfq0017FiniteQcd.gell_mann_diagonal_orthogonality_and_three_color_separation`: Proves trace orthogonality `⟨λ₃, λ̃₈⟩ = 0` and pairwise separation of the three color weight pairs `(1, 1)`, `(-1, 1)`, `(0, -2)`.
- `CampaignTfq0017FiniteQcd.su2_cartan_cannot_span_gell_mann_lambda8_fence`: Proves that no scalar multiple `t • (1, -1)` of the `su(2)` Cartan generator matches `(1, 1)` in `λ̃₈ = (1, 1, -2)`.
- `CampaignTfq0017FiniteQcd.su2_zero_d_symbol_vs_su3_lambda8_square_fence`: Proves that `(1, -1)² = (1, 1)` has zero traceless part (`d_{abc} = 0` in `su(2)`), whereas `λ̃₈² = (1, 1, 4) = 2 I₃ - λ̃₈` has non-zero traceless part (`d_{888} ≠ 0` in `su(3)_c`).
- `CampaignTfq0017FiniteQcd.q8_finite_order_four_vs_continuous_lie_generator_fence`: Proves that `qi ∈ Q_8` has finite multiplicative order `4` (`qi² = -1`, `qi⁴ = 1`).
- `CampaignTfq0017FiniteQcd.tfq0017_su2_shadow_kept_on_gauge_side_scope_ledger_fence`: Audits `tfq0017RepoLedger` (`hasTwoDimCarrierOnly = true`, `providesThreeColorLabels = false`, `promotesQ8ToSu3c = false`).

### Independent Python Verification (`checks/independent/tfq-0017.py`)
- Executes `557` exact rational checks across quaternion four-square norm multiplicativity, `SU(2) → SO(3)` adjoint double cover, Gell-Mann diagonal orthogonality, and `su(3)_c` non-promotion fences (`0` failures).

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0018](tfq_0018_gell_mann_color_generators_and_jacobi_closure.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
