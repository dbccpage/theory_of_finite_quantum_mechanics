import Mathlib.Algebra.Order.Ring.Basic
import Mathlib.Algebra.Order.Field.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FieldSimp

/-!
# Campaign: FSP-HUBBARD-PROTECTED-REPRESENTATIONS

AuthorityEffect: None. Scope: Finite Trotter Hubbard auxiliary-field determinant representations.
Target 4 from `dag/pfp/campaign/derivation_queue.json` (score 28).

Statement:
"Hubbard determinant positivity is restricted to the package stated half-filled
bipartite or attractive spin-balanced hypotheses; exact negative fields outside
those protections remain distinct witnesses."

Outcome: Narrowed
- Stated in Lean 4: arithmetic consequences of the pairing relations. A product `C * (d * d)`
  with `0 ≤ C` is nonnegative, and `d_up * d_down` is nonnegative when `d_down = d_up / det_P`
  with `0 < det_P`. The pairing relations themselves (`P_up = P_down`, and
  `d_down = d_up / det P_up` from `η T η = T⁻¹`) are NOT derived from Hubbard transfer matrices
  here: the attractive case is entered as the form `C * (d * d)` and the half-filled bipartite
  case as the hypothesis `h_pair`.
- Stated in Lean 4: two stored rational pairs, `(d_up, d_down)` for masks 15721 and 1281, have
  `d_up > 0 > d_down`, hence negative product. That these pairs are `det (I + P_σ)` of the
  stated four-site ring and triangle matrices is NOT derived in Lean; it is recomputed exactly
  by `checks/independent/fsp-hubbard-protected-representations.py`.
- `¬ (∀ p : DeterminantPair ℚ, 0 ≤ p.weight)` is a statement about arbitrary pairs of
  rationals. Any pair of opposite sign refutes it, so it has no Hubbard content beyond the
  witnesses above.
-/

namespace CampaignFspHubbardProtected

/-! ## 1. Attractive Spin-Balanced Pairing Identity -/

/-- In the attractive spin-balanced Hubbard auxiliary representation, the up and down
    single-particle propagators are identical: `P_up = P_down`, hence `d_up = d_down = d`.
    The determinant product is an algebraic square `d * d = d^2`.
    Over any ordered commutative ring, this product is non-negative.
    This theorem states only that arithmetic fact: the equality `P_up = P_down` of the
    transfer-matrix products is not derived in Lean. -/
theorem attractive_pairing_sq_nonneg {R : Type*} [CommRing R] [LinearOrder R] [IsStrictOrderedRing R]
    (d : R) : 0 ≤ d * d := by
  nlinarith

/-- With the positive field prefactor `C ≥ 0` (e.g. `C = h^(-∑ s) > 0`),
    the total attractive auxiliary-field weight is non-negative. -/
theorem attractive_weight_nonneg {R : Type*} [CommRing R] [LinearOrder R] [IsStrictOrderedRing R]
    (C d : R) (hC : 0 ≤ C) : 0 ≤ C * (d * d) := by
  nlinarith

/-- If `C > 0` and `d ≠ 0`, the attractive weight is strictly positive. -/
theorem attractive_weight_pos {R : Type*} [CommRing R] [LinearOrder R] [IsStrictOrderedRing R]
    (C d : R) (hC : 0 < C) (hd : d ≠ 0) : 0 < C * (d * d) := by
  have hd2 : 0 < d * d := by
    rcases lt_or_gt_of_ne hd with hneg | hpos
    · nlinarith
    · nlinarith
  nlinarith


/-! ## 2. Half-Filled Bipartite Pairing Identity (Repulsive Channel) -/

/-- In the repulsive Hubbard model at half filling (`z = 1`, `μ = 0`) on a bipartite lattice,
    the sublattice particle-hole involution yields the matrix relation
    `η P_down η = (P_up^T)⁻¹`, which implies the determinant pairing
    `d_down = d_up / det(P_up)`.
    Over any field, the determinant product satisfies
    `d_up * d_down = (d_up * d_up) / det(P_up)`.
    The relation `h_pair` is a hypothesis here: the sublattice conjugation `η T η = T⁻¹`
    and the multi-slice product are not formalized. -/
theorem half_filled_bipartite_weight_eq {F : Type*} [Field F]
    (d_up d_down det_P : F) (h_pair : d_down = d_up / det_P) :
    d_up * d_down = (d_up * d_up) / det_P := by
  rw [h_pair]
  ring

/-- When `det(P_up) > 0` (as guaranteed by `det(P_up) = h^(∑ s) > 0`),
    the half-filled bipartite determinant product weight is non-negative. -/
theorem half_filled_bipartite_weight_nonneg {F : Type*} [Field F] [LinearOrder F] [IsStrictOrderedRing F]
    (d_up d_down det_P : F) (h_det_pos : 0 < det_P) (h_pair : d_down = d_up / det_P) :
    0 ≤ d_up * d_down := by
  rw [half_filled_bipartite_weight_eq d_up d_down det_P h_pair]
  have h_sq : 0 ≤ d_up * d_up := by nlinarith
  exact div_nonneg h_sq (le_of_lt h_det_pos)

/-- If `d_up ≠ 0` and `det(P_up) > 0`, the half-filled bipartite weight is strictly positive. -/
theorem half_filled_bipartite_weight_pos {F : Type*} [Field F] [LinearOrder F] [IsStrictOrderedRing F]
    (d_up d_down det_P : F) (h_det_pos : 0 < det_P) (h_pair : d_down = d_up / det_P)
    (h_up_ne : d_up ≠ 0) :
    0 < d_up * d_down := by
  rw [half_filled_bipartite_weight_eq d_up d_down det_P h_pair]
  have h_sq_pos : 0 < d_up * d_up := by
    rcases lt_or_gt_of_ne h_up_ne with hneg | hpos
    · nlinarith
    · nlinarith
  exact div_pos h_sq_pos h_det_pos


/-! ## 3. Determinant Pairs and Sign Analysis -/

/-- An auxiliary-field spin-determinant pair `(d_up, d_down)`. -/
structure DeterminantPair (F : Type*) where
  d_up : F
  d_down : F

/-- The determinant product weight of a pair. -/
def DeterminantPair.weight {F : Type*} [Mul F] (p : DeterminantPair F) : F :=
  p.d_up * p.d_down

/-- When spin determinants have opposite strict signs, their product weight is strictly negative. -/
theorem opposite_signs_weight_neg {R : Type*} [CommRing R] [LinearOrder R] [IsStrictOrderedRing R]
    (p : DeterminantPair R) (h_up : 0 < p.d_up) (h_down : p.d_down < 0) :
    p.weight < 0 := by
  unfold DeterminantPair.weight
  nlinarith


/-! ## 4. Explicit Negative Determinant Witnesses Outside Protection -/

/-- Witness 1: 4-site ring with 4 time slices, repulsive U, doped away from half-filling
    (`r = 2`, `h = 8`, `z = 2`, field mask 15721). The two rationals are stored values;
    Lean does not derive them from the ring transfer matrices.
    From `papers/core/fsp/docs/sql_meron_hubbard.md` §5 and `code/python/src/fsp/sign_sql/exact_models.py`. -/
def witness_doped_ring : DeterminantPair ℚ := {
  d_up := 11072073737867929807204939234025 / 2305843009213693952,
  d_down := -1034021712177776419381618902295 / 147573952589676412928
}

theorem witness_doped_ring_d_up_pos : 0 < witness_doped_ring.d_up := by
  unfold witness_doped_ring
  norm_num

theorem witness_doped_ring_d_down_neg : witness_doped_ring.d_down < 0 := by
  unfold witness_doped_ring
  norm_num

/-- Exact negative determinant product weight for the doped 4-site ring witness. -/
theorem witness_doped_ring_weight_neg : witness_doped_ring.weight < 0 := by
  exact opposite_signs_weight_neg witness_doped_ring witness_doped_ring_d_up_pos witness_doped_ring_d_down_neg

/-- Witness 2: 3-site triangle (frustrated / non-bipartite), 4 time slices, repulsive U
    (`r = 2`, `h = 8`, `z = 1`, field mask 1281). Stored values, as for witness 1.
    From `papers/core/fsp/docs/sql_meron_hubbard.md` §5 and `code/python/src/fsp/sign_sql/exact_models.py`. -/
def witness_triangle : DeterminantPair ℚ := {
  d_up := 2661572208368287551525625 / 9223372036854775808,
  d_down := -323903084369592224375 / 35184372088832
}

theorem witness_triangle_d_up_pos : 0 < witness_triangle.d_up := by
  unfold witness_triangle
  norm_num

theorem witness_triangle_d_down_neg : witness_triangle.d_down < 0 := by
  unfold witness_triangle
  norm_num

/-- Exact negative determinant product weight for the frustrated 3-site triangle witness. -/
theorem witness_triangle_weight_neg : witness_triangle.weight < 0 := by
  exact opposite_signs_weight_neg witness_triangle witness_triangle_d_up_pos witness_triangle_d_down_neg


/-! ## 5. Refutation of Unconditional Positivity (Narrowing Theorem) -/

/-- Nonnegativity of `d_up * d_down` fails for arbitrary rational pairs: the stored witness
    pair has a strictly negative product. Any opposite-sign pair would do, so this theorem
    has Hubbard content only through the identification of the witness with masks 15721 and
    1281, which is checked outside Lean. -/
theorem not_unconditional_positivity :
    ¬ (∀ (p : DeterminantPair ℚ), 0 ≤ p.weight) := by
  intro h_all
  have h_w := h_all witness_doped_ring
  have h_neg := witness_doped_ring_weight_neg
  linarith

/-- Summary of the arithmetic statements above: nonnegativity under the pairing relation
    `d_down = d_up / det_P` with `0 < det_P`, nonnegativity of `C * (d * d)`, and the
    negative product of the two stored witness pairs. Not a statement about Hubbard
    transfer matrices. -/
theorem hubbard_determinant_positivity_is_restricted :
    (∀ (d_up d_down det_P : ℚ),
      0 < det_P → d_down = d_up / det_P → 0 ≤ d_up * d_down) ∧
    (∀ (C d : ℚ),
      0 ≤ C → 0 ≤ C * (d * d)) ∧
    (witness_doped_ring.weight < 0) ∧
    (witness_triangle.weight < 0) ∧
    (¬ (∀ (p : DeterminantPair ℚ), 0 ≤ p.weight)) := by
  refine ⟨fun d_up d_down det_P => half_filled_bipartite_weight_nonneg d_up d_down det_P,
          fun C d => attractive_weight_nonneg C d,
          witness_doped_ring_weight_neg,
          witness_triangle_weight_neg,
          not_unconditional_positivity⟩

#print axioms attractive_pairing_sq_nonneg
#print axioms attractive_weight_nonneg
#print axioms attractive_weight_pos
#print axioms half_filled_bipartite_weight_eq
#print axioms half_filled_bipartite_weight_nonneg
#print axioms half_filled_bipartite_weight_pos
#print axioms opposite_signs_weight_neg
#print axioms witness_doped_ring_d_up_pos
#print axioms witness_doped_ring_d_down_neg
#print axioms witness_doped_ring_weight_neg
#print axioms witness_triangle_d_up_pos
#print axioms witness_triangle_d_down_neg
#print axioms witness_triangle_weight_neg
#print axioms not_unconditional_positivity
#print axioms hubbard_determinant_positivity_is_restricted

end CampaignFspHubbardProtected
