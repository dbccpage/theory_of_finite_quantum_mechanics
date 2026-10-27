import Mathlib.Algebra.Ring.Int.Parity
import Mathlib.Algebra.Order.Field.Rat
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# A parity frame function on rational rays of `S²` that is not a quadratic form

AuthorityEffect: None.

Scope.  This is the `d = 3` rational-sphere analogue of the Meyer (1999) / Kochen–Specker
colouring fact.  The carrier is the set of *rays*: integer vectors `(a, b, c)` with not all
coordinates even and `a² + b² + c²` a perfect square.  Every rational point of the unit sphere
has a primitive integer representative, which is a ray; a ray may also be an odd multiple of a
primitive representative, and the function below is invariant under such scalings
(`parity_odd_smul`), so it is a function of the rational ray.

The two-valued function `parity (a, b, c) = [c odd]` sums to `1` on every orthogonal triple of
rays (`parity_frame_function`), yet no rational symmetric `3 × 3` form `Q` satisfies
`Q(v) = parity v · (a² + b² + c²)` on all rays (`parity_not_quadratic`).  Hence frame additivity on
orthogonal triples of rational rays does not force a quadratic form: Gleason's conclusion fails on
the rational carrier once the continuum hypothesis (all real orthonormal bases) and any
effect-additivity hypothesis are dropped.  Nothing here is a statement about physics.

Import note.  Only the integer parity lemmas, the ordered field `ℚ`, and the tactics `omega`,
`norm_num`, `linarith` are used; `import Mathlib` is deliberately avoided.
-/

namespace BornFinite.RationalSphere

/-- An integer vector `(a, b, c) ∈ ℤ³`. -/
structure Vec3 where
  a : ℤ
  b : ℤ
  c : ℤ

namespace Vec3

/-- The squared Euclidean norm `a² + b² + c²`. -/
def normSq (v : Vec3) : ℤ := v.a ^ 2 + v.b ^ 2 + v.c ^ 2

/-- The integer dot product. -/
def dot (u v : Vec3) : ℤ := u.a * v.a + u.b * v.b + u.c * v.c

/-- `v` is a *ray*: not all coordinates are even, and `a² + b² + c²` is a perfect square. -/
def IsRay (v : Vec3) : Prop :=
  ¬ (Even v.a ∧ Even v.b ∧ Even v.c) ∧ ∃ n : ℤ, v.normSq = n ^ 2

end Vec3

/-- The parity frame function: `1` if the third coordinate is odd, `0` otherwise. -/
def parity (v : Vec3) : ℚ := if Odd v.c then 1 else 0

/-! ### Squares modulo 8 -/

/-- An odd square is `1 (mod 8)`; an even square is `0` or `4 (mod 8)`. -/
theorem sq_emod_eight (a : ℤ) :
    (a % 2 = 1 ∧ a * a % 8 = 1) ∨ (a % 2 = 0 ∧ (a * a % 8 = 0 ∨ a * a % 8 = 4)) := by
  have h : a * a % 8 = a % 8 * (a % 8) % 8 := Int.mul_emod a a 8
  have hr : a % 8 = 0 ∨ a % 8 = 1 ∨ a % 8 = 2 ∨ a % 8 = 3 ∨ a % 8 = 4 ∨ a % 8 = 5 ∨
      a % 8 = 6 ∨ a % 8 = 7 := by omega
  rcases hr with hr | hr | hr | hr | hr | hr | hr | hr <;> rw [hr] at h <;> omega

/-- A ray has exactly one odd coordinate. -/
theorem ray_exactly_one_odd {v : Vec3} (hv : v.IsRay) :
    (Odd v.a ∧ Even v.b ∧ Even v.c) ∨ (Even v.a ∧ Odd v.b ∧ Even v.c) ∨
      (Even v.a ∧ Even v.b ∧ Odd v.c) := by
  obtain ⟨hne, n, hn⟩ := hv
  simp only [Vec3.normSq, sq] at hn
  simp only [Int.even_iff, Int.odd_iff] at hne ⊢
  have ha := sq_emod_eight v.a
  have hb := sq_emod_eight v.b
  have hc := sq_emod_eight v.c
  have hn' := sq_emod_eight n
  omega

/-- A product is odd exactly when both factors are odd (in `% 2` form). -/
theorem mul_emod_two_eq_one (x y : ℤ) : x * y % 2 = 1 ↔ x % 2 = 1 ∧ y % 2 = 1 := by
  have h := Int.odd_mul (m := x) (n := y)
  simp only [Int.odd_iff] at h
  exact h

/-- Orthogonal rays do not have their odd coordinate in the same position. -/
theorem orthogonal_rays_odd_positions_differ {u v : Vec3} (hu : u.IsRay) (hv : v.IsRay)
    (h : u.dot v = 0) :
    ¬ ((Odd u.a ∧ Odd v.a) ∨ (Odd u.b ∧ Odd v.b) ∨ (Odd u.c ∧ Odd v.c)) := by
  have hu' := ray_exactly_one_odd hu
  have hv' := ray_exactly_one_odd hv
  have h1 := mul_emod_two_eq_one u.a v.a
  have h2 := mul_emod_two_eq_one u.b v.b
  have h3 := mul_emod_two_eq_one u.c v.c
  simp only [Vec3.dot] at h
  simp only [Int.even_iff, Int.odd_iff] at hu' hv' ⊢
  omega

/-- Frame additivity: on a pairwise orthogonal triple of rays the parity values sum to `1`. -/
theorem parity_frame_function {u v w : Vec3} (hu : u.IsRay) (hv : v.IsRay) (hw : w.IsRay)
    (huv : u.dot v = 0) (huw : u.dot w = 0) (hvw : v.dot w = 0) :
    parity u + parity v + parity w = 1 := by
  have hu' := ray_exactly_one_odd hu
  have hv' := ray_exactly_one_odd hv
  have hw' := ray_exactly_one_odd hw
  have huv' := orthogonal_rays_odd_positions_differ hu hv huv
  have huw' := orthogonal_rays_odd_positions_differ hu hw huw
  have hvw' := orthogonal_rays_odd_positions_differ hv hw hvw
  simp only [Int.even_iff, Int.odd_iff] at hu' hv' hw' huv' huw' hvw'
  have hc : (u.c % 2 = 1 ∧ v.c % 2 = 0 ∧ w.c % 2 = 0) ∨
      (u.c % 2 = 0 ∧ v.c % 2 = 1 ∧ w.c % 2 = 0) ∨
      (u.c % 2 = 0 ∧ v.c % 2 = 0 ∧ w.c % 2 = 1) := by omega
  rcases hc with ⟨h1, h2, h3⟩ | ⟨h1, h2, h3⟩ | ⟨h1, h2, h3⟩ <;>
    simp [parity, Int.odd_iff, h1, h2, h3]

/-- The parity function is two-valued. -/
theorem parity_two_valued (v : Vec3) : parity v = 0 ∨ parity v = 1 := by
  by_cases h : Odd v.c <;> simp [parity, h]

/-- The parity function is invariant under scaling by an odd integer, so it depends only on the
rational ray represented by `v`. -/
theorem parity_odd_smul {k : ℤ} (hk : Odd k) (v : Vec3) :
    parity ⟨k * v.a, k * v.b, k * v.c⟩ = parity v := by
  simp [parity, Int.odd_mul, hk]

/-! ### Six explicit rays -/

theorem ray_e1 : (⟨1, 0, 0⟩ : Vec3).IsRay := ⟨by decide, 1, by norm_num [Vec3.normSq]⟩
theorem ray_e2 : (⟨0, 1, 0⟩ : Vec3).IsRay := ⟨by decide, 1, by norm_num [Vec3.normSq]⟩
theorem ray_e3 : (⟨0, 0, 1⟩ : Vec3).IsRay := ⟨by decide, 1, by norm_num [Vec3.normSq]⟩
theorem ray_340 : (⟨3, 4, 0⟩ : Vec3).IsRay := ⟨by decide, 5, by norm_num [Vec3.normSq]⟩
theorem ray_034 : (⟨0, 3, 4⟩ : Vec3).IsRay := ⟨by decide, 5, by norm_num [Vec3.normSq]⟩
theorem ray_043 : (⟨0, 4, 3⟩ : Vec3).IsRay := ⟨by decide, 5, by norm_num [Vec3.normSq]⟩

/-! ### The obstruction -/

/-- No rational symmetric `3 × 3` form agrees with `parity v · (a² + b² + c²)` on all rays.
The right-hand side is the Born value of the normalised vector times the norm squared, so the
statement is scale-free. -/
theorem parity_not_quadratic :
    ¬ ∃ r00 r11 r22 r01 r02 r12 : ℚ, ∀ v : Vec3, v.IsRay →
      r00 * (v.a : ℚ) ^ 2 + r11 * (v.b : ℚ) ^ 2 + r22 * (v.c : ℚ) ^ 2
        + 2 * r01 * ((v.a : ℚ) * v.b) + 2 * r02 * ((v.a : ℚ) * v.c) + 2 * r12 * ((v.b : ℚ) * v.c)
        = parity v * ((v.a : ℚ) ^ 2 + (v.b : ℚ) ^ 2 + (v.c : ℚ) ^ 2) := by
  rintro ⟨r00, r11, r22, r01, r02, r12, h⟩
  have h1 := h _ ray_e1
  have h2 := h _ ray_e2
  have h3 := h _ ray_e3
  have h4 := h _ ray_340
  have h5 := h _ ray_034
  have h6 := h _ ray_043
  norm_num [parity, Int.odd_iff] at h1 h2 h3 h4 h5 h6
  linarith

end BornFinite.RationalSphere

#print axioms BornFinite.RationalSphere.sq_emod_eight
#print axioms BornFinite.RationalSphere.ray_exactly_one_odd
#print axioms BornFinite.RationalSphere.mul_emod_two_eq_one
#print axioms BornFinite.RationalSphere.orthogonal_rays_odd_positions_differ
#print axioms BornFinite.RationalSphere.parity_frame_function
#print axioms BornFinite.RationalSphere.parity_two_valued
#print axioms BornFinite.RationalSphere.parity_odd_smul
#print axioms BornFinite.RationalSphere.ray_e1
#print axioms BornFinite.RationalSphere.ray_e2
#print axioms BornFinite.RationalSphere.ray_e3
#print axioms BornFinite.RationalSphere.ray_340
#print axioms BornFinite.RationalSphere.ray_034
#print axioms BornFinite.RationalSphere.ray_043
#print axioms BornFinite.RationalSphere.parity_not_quadratic
