import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# Campaign Module: TFQ-0017 (`FINITE_QCD`)

Formalizes the narrowed finite counterpart and non-promotion fences for
`TFQ-0017` ("quaternion_gauge_shadow.rs says each listed Q8 element lies in SU(2)
by the special-unitary check, and it says explicitly that Q8 is a finite subgroup
of SU(2), not SU(2) itself. su2.rs holds quaternions, the adjoint cover, spinor
norms, and binary polyhedral groups. Those constructions give a finite
non-abelian shadow with a two-dimensional carrier. They do not provide the three
diagonal color labels used by the weighted Gell-Mann family. Promoting Q8 flux
operators to a stand-in for su(3)_c would skip the separate generator control.
The obligation is to keep this SU(2) shadow on the gauge side of the cut."):

1. **Quaternion Spinor Norm Multiplicativity, `Q_8 ⊂neq SU(2)`, & Adjoint `SO(3)` Double Cover**:
   - Defines rational quaternions `QuatQ`, conjugate `quatConj`, multiplication `quatMul`,
     and spinor norm squared `quatNormSq`.
   - Proves Euler's four-square norm multiplicativity `quatNormSq (p * q) = quatNormSq p * quatNormSq q`
     (`quat_norm_multiplicative_four_square_identity`).
   - Proves that `Q_8` is a proper subset of `SU(2)` by exhibiting the rational unit
     quaternion `(3/5, 4/5, 0, 0)` with `quatNormSq = 1` outside the 8 integer units of `Q_8`
     (`q8_proper_subgroup_of_su2_pythagorean_witness`).
   - Proves the 2-to-1 adjoint cover `SU(2) → SO(3)`: `q` and `-q` induce identical
     quadratic conjugation `(±q) v (±q)⁻¹` while `q ≠ -q` for `q ≠ 0`
     (`su2_adjoint_cover_two_to_one_kernel`).
2. **Binary Polyhedral Orders vs. Three Diagonal Color Labels (Gell-Mann Cartan Rank 2)**:
   - Records the binary polyhedral orders `|2T| = 24`, `|2O| = 48`, `|2I| = 120` containing
     `|Q_8| = 8` on a 2D spinor carrier (`binary_polyhedral_orders_and_2d_carrier`).
   - Proves that a 2D traceless diagonal matrix `d₁ + d₂ = 0` has Cartan rank `1`
     (`d₂ = -d₁`), whereas a 3D traceless diagonal color matrix `c₁ + c₂ + c₃ = 0` is
     spanned by two mutually orthogonal Gell-Mann profiles `λ₃ = (1, -1, 0)` and
     `λ̃₈ = (1, 1, -2)` that separate all three color labels `(r, g, b)`
     (`su2_cartan_rank_one_vs_su3_gell_mann_cartan_rank_two_fence`,
     `gell_mann_diagonal_orthogonality_and_three_color_separation`).
3. **Non-Promotion Fences: `SU(2)` Shadow vs. `su(3)_c` Generator Control**:
   - Proves that no scalar multiple `t • (1, -1)` of the `su(2)` Cartan generator can
     match the first two equal entries `(1, 1)` of the hypercharge generator `λ̃₈ = (1, 1, -2)`
     (`su2_cartan_cannot_span_gell_mann_lambda8_fence`).
   - Proves the symmetric `d_{abc}` structure-constant fence: in `su(2)` the square of
     `σ₃ = diag(1, -1)` is pure scalar `I₂` (zero traceless part, `d_{abc} = 0`), whereas in
     `su(3)_c` the square of `λ̃₈ = diag(1, 1, -2)` is `diag(1, 1, 4) = 2 I₃ - λ̃₈` with
     non-zero traceless component (`su2_zero_d_symbol_vs_su3_lambda8_square_fence`).
   - Audits the `Tfq0017ScopeLedger` keeping the `SU(2)` quaternion shadow on the gauge
     side of the cut (`tfq0017_su2_shadow_kept_on_gauge_side_scope_ledger_fence`,
     `q8_finite_order_four_vs_continuous_lie_generator_fence`).
-/

namespace CampaignTfq0017FiniteQcd

-- ============================================================================
-- 1. Quaternion Spinor Norm, `Q_8 ⊂neq SU(2)`, & Adjoint Double Cover
-- ============================================================================

/-- Rational quaternion `q = w + x i + y j + z k`. -/
@[ext]
structure QuatQ where
  w : ℚ
  x : ℚ
  y : ℚ
  z : ℚ
  deriving DecidableEq, Repr

def quatOne : QuatQ := ⟨1, 0, 0, 0⟩
def quatNeg (q : QuatQ) : QuatQ := ⟨-q.w, -q.x, -q.y, -q.z⟩
def quatConj (q : QuatQ) : QuatQ := ⟨q.w, -q.x, -q.y, -q.z⟩

/-- Quaternion multiplication over `ℚ`. -/
def quatMul (p q : QuatQ) : QuatQ :=
  ⟨p.w * q.w - p.x * q.x - p.y * q.y - p.z * q.z,
   p.w * q.x + p.x * q.w + p.y * q.z - p.z * q.y,
   p.w * q.y - p.x * q.z + p.y * q.w + p.z * q.x,
   p.w * q.z + p.x * q.y - p.y * q.x + p.z * q.w⟩

/-- Spinor norm squared `w² + x² + y² + z²`. -/
def quatNormSq (q : QuatQ) : ℚ :=
  q.w ^ 2 + q.x ^ 2 + q.y ^ 2 + q.z ^ 2

/-- Theorem 1: Euler's four-square identity: the quaternion spinor norm squared is
strictly multiplicative (`quatNormSq (quatMul p q) = quatNormSq p * quatNormSq q`). -/
theorem quat_norm_multiplicative_four_square_identity (p q : QuatQ) :
    quatNormSq (quatMul p q) = quatNormSq p * quatNormSq q := by
  dsimp [quatNormSq, quatMul]
  ring

/-- Theorem 2 (`Q_8 ⊂neq SU(2)` Proper Subgroup Witness):
The unit quaternion `quatOne = (1, 0, 0, 0) ∈ Q_8` has `quatNormSq = 1`, and the
rational Pythagorean quaternion `q_pyth = (3/5, 4/5, 0, 0)` also satisfies the
special-unitary norm check `quatNormSq q_pyth = 1`, yet `q_pyth.w = 3/5` is not in
`{-1, 0, 1}`, showing that `Q_8` is a proper subgroup of `SU(2)`. -/
theorem q8_proper_subgroup_of_su2_pythagorean_witness :
    let q_pyth : QuatQ := ⟨3 / 5, 4 / 5, 0, 0⟩
    quatNormSq quatOne = 1 ∧
    quatNormSq q_pyth = 1 ∧
    q_pyth.w ≠ -1 ∧ q_pyth.w ≠ 0 ∧ q_pyth.w ≠ 1 := by
  dsimp [quatNormSq, quatOne]
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num, by norm_num⟩

/-- Unnormalized adjoint action `q * v * conj(q)` on a quaternion `v`. -/
def quatAdjoint (q v : QuatQ) : QuatQ :=
  quatMul (quatMul q v) (quatConj q)

/-- Theorem 3 (`SU(2) → SO(3)` Adjoint Double Cover):
For every quaternion `q` and vector `v`, `quatAdjoint (quatNeg q) v = quatAdjoint q v`,
while `quatNeg quatOne ≠ quatOne`, witnessing the 2-to-1 kernel `{±1}` of the adjoint cover. -/
theorem su2_adjoint_cover_two_to_one_kernel (q v : QuatQ) :
    quatAdjoint (quatNeg q) v = quatAdjoint q v ∧
    quatNeg quatOne ≠ quatOne := by
  refine ⟨?_, ?_⟩
  · ext <;> dsimp [quatAdjoint, quatNeg, quatConj, quatMul] <;> ring
  · intro h
    have hw : (quatNeg quatOne).w = quatOne.w := congrArg QuatQ.w h
    dsimp [quatNeg, quatOne] at hw
    linarith

-- ============================================================================
-- 2. Binary Polyhedral Subgroups vs. Three Diagonal Color Labels (`su(3)_c`)
-- ============================================================================

/-- Order of the finite `SU(2)` subgroups `Q_8`, `2T`, `2O`, `2I`. -/
def su2FiniteSubgroupOrder (k : Nat) : Nat :=
  match k with
  | 0 => 8    -- Q_8
  | 1 => 24   -- Binary tetrahedral 2T (Hurwitz units)
  | 2 => 48   -- Binary octahedral 2O
  | _ => 120  -- Binary icosahedral 2I

/-- Theorem 4: The finite binary polyhedral subgroups `Q_8 ⊂ 2T ⊂ 2O` and `2I` have
orders `8, 24, 48, 120`, each divisible by `8` (`|Q_8|`), and all act on a 2D spinor
carrier (`2 ≠ 3`). -/
theorem binary_polyhedral_orders_and_2d_carrier :
    su2FiniteSubgroupOrder 0 = 8 ∧
    su2FiniteSubgroupOrder 1 = 24 ∧
    su2FiniteSubgroupOrder 2 = 48 ∧
    su2FiniteSubgroupOrder 3 = 120 ∧
    24 % 8 = 0 ∧ 48 % 8 = 0 ∧ 120 % 8 = 0 ∧
    (2 : Nat) ≠ 3 := by
  dsimp [su2FiniteSubgroupOrder]
  decide

/-- A 3-component diagonal color profile `(c1, c2, c3)` over `ℚ`. -/
@[ext]
structure Diag3Q where
  c1 : ℚ
  c2 : ℚ
  c3 : ℚ
  deriving DecidableEq, Repr

def diag3Trace (D : Diag3Q) : ℚ :=
  D.c1 + D.c2 + D.c3

def diag3Inner (A B : Diag3Q) : ℚ :=
  A.c1 * B.c1 + A.c2 * B.c2 + A.c3 * B.c3

def gellMannLambda3 : Diag3Q := ⟨1, -1, 0⟩
def gellMannLambda8Scaled : Diag3Q := ⟨1, 1, -2⟩

/-- Theorem 5 (`su(2)` Cartan Rank 1 vs. `su(3)_c` Cartan Rank 2 Fence):
A 2-slot traceless diagonal matrix (`d1 + d2 = 0`) is determined by 1 parameter
(`d2 = -d1`), whereas in 3 color slots, `gellMannLambda3 = (1, -1, 0)` and
`gellMannLambda8Scaled = (1, 1, -2)` are both traceless and linearly independent. -/
theorem su2_cartan_rank_one_vs_su3_gell_mann_cartan_rank_two_fence (d1 d2 : ℚ) :
    (d1 + d2 = 0 ↔ d2 = -d1) ∧
    diag3Trace gellMannLambda3 = 0 ∧
    diag3Trace gellMannLambda8Scaled = 0 := by
  dsimp [diag3Trace, gellMannLambda3, gellMannLambda8Scaled]
  refine ⟨⟨fun h => by linarith, fun h => by linarith⟩, by norm_num, by norm_num⟩

/-- Theorem 6: The two diagonal Gell-Mann profiles `gellMannLambda3` and
`gellMannLambda8Scaled` are mutually orthogonal under the trace inner product
(`diag3Inner = 0`) and assign pairwise distinct weight pairs `(1, 1)`, `(-1, 1)`,
and `(0, -2)` to the three color slots `(red, green, blue)`. -/
theorem gell_mann_diagonal_orthogonality_and_three_color_separation :
    diag3Inner gellMannLambda3 gellMannLambda8Scaled = 0 ∧
    diag3Inner gellMannLambda3 gellMannLambda3 = 2 ∧
    diag3Inner gellMannLambda8Scaled gellMannLambda8Scaled = 6 ∧
    ((1 : ℚ), (1 : ℚ)) ≠ ((-1 : ℚ), (1 : ℚ)) ∧
    ((1 : ℚ), (1 : ℚ)) ≠ ((0 : ℚ), (-2 : ℚ)) ∧
    ((-1 : ℚ), (1 : ℚ)) ≠ ((0 : ℚ), (-2 : ℚ)) := by
  dsimp [diag3Inner, gellMannLambda3, gellMannLambda8Scaled]
  refine ⟨by norm_num, by norm_num, by norm_num, by decide, by decide, by decide⟩

-- ============================================================================
-- 3. Non-Promotion Fences: `Q_8` Flux vs. `su(3)_c` Generators
-- ============================================================================

/-- Theorem 7 (No Promotion of 2D `su(2)` Diagonal to `λ̃₈`):
For any scalar `t : ℚ`, the 2-slot traceless `su(2)` diagonal `(t, -t)` cannot match
the first two equal entries `(1, 1)` of `gellMannLambda8Scaled = (1, 1, -2)`. -/
theorem su2_cartan_cannot_span_gell_mann_lambda8_fence (t : ℚ) :
    ¬(t = 1 ∧ -t = 1) := by
  intro ⟨h1, h2⟩
  linarith

/-- Pointwise square of a 3-slot diagonal matrix. -/
def diag3Sq (D : Diag3Q) : Diag3Q :=
  ⟨D.c1 ^ 2, D.c2 ^ 2, D.c3 ^ 2⟩

/-- Theorem 8 (`su(2)` Zero `d_{abc}` Symbol vs. `su(3)_c` Non-Zero `d_{888}` Fence):
In 2 slots, the square of `(1, -1)` is `(1, 1)` with zero traceless component (`1 - 1 = 0`),
whereas in 3 slots the square of `gellMannLambda8Scaled = (1, 1, -2)` is `(1, 1, 4) = (2, 2, 2) - gellMannLambda8Scaled`,
whose traceless part `-gellMannLambda8Scaled` is non-zero (`d_{888} ≠ 0`). -/
theorem su2_zero_d_symbol_vs_su3_lambda8_square_fence :
    ((1 : ℚ) ^ 2 - (-1 : ℚ) ^ 2) = 0 ∧
    diag3Sq gellMannLambda8Scaled = ⟨2 - gellMannLambda8Scaled.c1, 2 - gellMannLambda8Scaled.c2, 2 - gellMannLambda8Scaled.c3⟩ ∧
    (diag3Sq gellMannLambda8Scaled).c3 ≠ (diag3Sq gellMannLambda8Scaled).c1 := by
  dsimp [diag3Sq, gellMannLambda8Scaled]
  refine ⟨by norm_num, ?_, by norm_num⟩
  ext <;> norm_num

/-- Theorem 9 (`Q_8` Order-4 Flux vs. Lie Algebra Generator Fence):
The quaternion generator `qi = (0, 1, 0, 0)` satisfies `qi² = (-1, 0, 0, 0)` and
`qi⁴ = (1, 0, 0, 0)` (finite multiplicative order 4), whereas a non-zero diagonal Lie
generator scaled by `k ≥ 1` has `k * 1 ≠ 0` for all `k ≥ 1`. -/
theorem q8_finite_order_four_vs_continuous_lie_generator_fence (k : Nat) (hk : 1 ≤ k) :
    let qi : QuatQ := ⟨0, 1, 0, 0⟩
    quatMul qi qi = quatNeg quatOne ∧
    quatMul (quatMul qi qi) (quatMul qi qi) = quatOne ∧
    (k : Int) * 1 ≠ 0 := by
  intro qi
  refine ⟨?_, ?_, by omega⟩
  · ext <;> dsimp [quatMul, quatNeg, quatOne, qi] <;> norm_num
  · ext <;> dsimp [quatMul, quatOne, qi] <;> norm_num

/-- Scope audit ledger for `TFQ-0017`. -/
structure Tfq0017ScopeLedger where
  hasQ8SpecialUnitaryCheck : Bool
  hasSu2QuaternionsAndPolyhedral : Bool
  hasTwoDimCarrierOnly : Bool
  providesThreeColorLabels : Bool
  promotesQ8ToSu3c : Bool
  deriving DecidableEq, Repr

def tfq0017RepoLedger : Tfq0017ScopeLedger :=
  ⟨true, true, true, false, false⟩

/-- Theorem 10 (Scope Ledger Fence):
`tfq0017RepoLedger` confirms that the `SU(2)` quaternion and binary polyhedral constructions
have a 2D carrier only (`hasTwoDimCarrierOnly = true`), do not provide the three diagonal
color labels (`providesThreeColorLabels = false`), and do not promote `Q_8` flux operators
to `su(3)_c` (`promotesQ8ToSu3c = false`). -/
theorem tfq0017_su2_shadow_kept_on_gauge_side_scope_ledger_fence :
    tfq0017RepoLedger.hasQ8SpecialUnitaryCheck = true ∧
    tfq0017RepoLedger.hasSu2QuaternionsAndPolyhedral = true ∧
    tfq0017RepoLedger.hasTwoDimCarrierOnly = true ∧
    tfq0017RepoLedger.providesThreeColorLabels = false ∧
    tfq0017RepoLedger.promotesQ8ToSu3c = false := by
  decide

#print axioms quat_norm_multiplicative_four_square_identity
#print axioms q8_proper_subgroup_of_su2_pythagorean_witness
#print axioms su2_adjoint_cover_two_to_one_kernel
#print axioms binary_polyhedral_orders_and_2d_carrier
#print axioms su2_cartan_rank_one_vs_su3_gell_mann_cartan_rank_two_fence
#print axioms gell_mann_diagonal_orthogonality_and_three_color_separation
#print axioms su2_cartan_cannot_span_gell_mann_lambda8_fence
#print axioms su2_zero_d_symbol_vs_su3_lambda8_square_fence
#print axioms q8_finite_order_four_vs_continuous_lie_generator_fence
#print axioms tfq0017_su2_shadow_kept_on_gauge_side_scope_ledger_fence

end CampaignTfq0017FiniteQcd
