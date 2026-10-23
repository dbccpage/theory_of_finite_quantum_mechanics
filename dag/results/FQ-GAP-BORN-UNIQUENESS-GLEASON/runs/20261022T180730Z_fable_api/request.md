# Problem: frame functions on Gaussian-rational rays in dimension 3

You are working on the open part of DAG node `FQ-GAP-BORN-UNIQUENESS-GLEASON` in a Lean 4 project that builds finite quantum mechanics from exact arithmetic. You have no tools. Everything you need is in this message, and your answer will be compiled and audited by the host.

## Setting

Let K = ℚ(i), the Gaussian rationals, and V = K³ with the Hermitian form ⟨u, v⟩ = Σₖ conj(uₖ) vₖ.
- A **ray** is a line K·v with v ≠ 0.
- An **orthogonal frame** is a triple of pairwise orthogonal rays.
- A **frame function** is a map f from rays to ℚ such that f(a) + f(b) + f(c) = 1 for every orthogonal frame (a, b, c).
- f is **quadratic** (Born) if there is a Hermitian 3×3 matrix ρ over K, of trace 1, with f(K·v) = ⟨v, ρ v⟩ / ⟨v, v⟩ for every v ≠ 0.

## What the repository already proves

- `BornFable.RationalSphere.parity_frame_function` and `parity_not_quadratic`, in `lean4/BornRationalSphereObstruction.lean` (included below). On primitive integer rays of ℤ³ whose squared norm is a perfect square, exactly one coordinate is odd. The 0/1 "last coordinate odd" function is additive on orthogonal frames, and no rational symmetric form represents it. So over the **real** rational sphere the frame-function route to Gleason is obstructed.
- `lean4/GleasonRationalPlane.lean` (included below): in dimension 2 there is a binary non-quadratic frame function on ℚ².
- The Gaussian-rational field is available as `BornFable.GaussRat` (`lean4/BornGaussRat.lean`, included below), together with its star ring structure.
- With **effect additivity** assumed, the repository already kernel-checks the Born rule over Gaussian-rational Hermitian matrices. This problem is about the **projection-only (frame-function) route**, without effect additivity.

## The question

Over K = ℚ(i) in dimension 3, is every frame function on rays quadratic?

Decide it, and prove your answer in Lean 4. Either outcome is a result for this project.
- **(A) Obstruction.** Construct an explicit frame function on Gaussian-rational rays of K³, and prove (1) frame additivity over every orthogonal frame and (2) that no Hermitian trace-one ρ over K represents it. A natural route is to adapt the parity argument to primitive Gaussian-integer vectors, for example using norms and congruences modulo (1+i) powers. Check carefully which rays exist, because non-real frames are allowed here.
- **(B) Uniqueness.** If no such function exists, prove that every frame function on K³ rays is quadratic. This would contradict the expectation set by the ℚ³ case, so double-check before claiming it.

If neither (A) nor (B) can be completed, prove the largest honest finite piece. Examples: additivity on a stated infinite family of frames, or a non-representability lemma. State exactly what is missing.

## Deliverable format

1. **A short mathematical argument,** in plain prose, first.
2. **One or more complete Lean files.** Each goes in a fenced block whose first line is `-- FILE: lean4/<Name>.lean`. Suggested name: `lean4/BornGaussianRationalFrameObstruction.lean`.
   - Target: Lean `4.35.0` with Mathlib `v4.35.0` (sha `56a005855ea17e0b0958f73ec801ae140b0a1679`).
   - You may `import` the included repository files by module name, e.g. `import BornRationalSphereObstruction`.
   - **Forbidden:** `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`. The host rejects any file that contains them, and requires `#print axioms` to show only `propext`, `Classical.choice`, `Quot.sound`.
   - End each file with `#print axioms` lines for its main theorems.
3. **A final section "WHAT IS PROVED".** State exactly the theorem(s) the Lean establishes, in one or two sentences each, and anything left unproved. Do not overstate. The host compares this section with the compiled statements.

## Included repository files


### lean4/BornRationalSphereObstruction.lean
```lean
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

namespace BornFable.RationalSphere

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

end BornFable.RationalSphere

#print axioms BornFable.RationalSphere.sq_emod_eight
#print axioms BornFable.RationalSphere.ray_exactly_one_odd
#print axioms BornFable.RationalSphere.mul_emod_two_eq_one
#print axioms BornFable.RationalSphere.orthogonal_rays_odd_positions_differ
#print axioms BornFable.RationalSphere.parity_frame_function
#print axioms BornFable.RationalSphere.parity_two_valued
#print axioms BornFable.RationalSphere.parity_odd_smul
#print axioms BornFable.RationalSphere.ray_e1
#print axioms BornFable.RationalSphere.ray_e2
#print axioms BornFable.RationalSphere.ray_e3
#print axioms BornFable.RationalSphere.ray_340
#print axioms BornFable.RationalSphere.ray_034
#print axioms BornFable.RationalSphere.ray_043
#print axioms BornFable.RationalSphere.parity_not_quadratic

```


### lean4/GleasonRationalPlane.lean
```lean
namespace FiniteQm.GleasonRationalPlane

def binaryRay (x y : Rat) : Rat :=
  if 0 < x*y then 1 else if x*y < 0 then 0 else if y = 0 then 1 else 0

theorem binary_values (x y : Rat) : binaryRay x y = 0 ∨ binaryRay x y = 1 := by
  grind [binaryRay]

theorem perpendicular_complement (x y : Rat) (h : x ≠ 0 ∨ y ≠ 0) :
    binaryRay x y + binaryRay (-y) x = 1 := by
  have hz : x*y = 0 ↔ x=0 ∨ y=0 := Rat.mul_eq_zero
  grind [binaryRay]

theorem no_quadratic_representation : ¬ ∃ a b c : Rat, ∀ x y : Rat,
    x ≠ 0 ∨ y ≠ 0 → a*x*x + 2*b*x*y + c*y*y = binaryRay x y * (x*x + y*y) := by
  rintro ⟨a,b,c,h⟩
  have h0 := h 1 0 (by decide)
  have h1 := h 0 1 (by decide)
  have h2 := h 1 1 (by decide)
  have h3 := h 1 2 (by decide)
  have e0 : binaryRay 1 0 = 1 := by grind [binaryRay]
  have e1 : binaryRay 0 1 = 0 := by grind [binaryRay]
  have e2 : binaryRay 1 1 = 1 := by grind [binaryRay]
  have e3 : binaryRay 1 2 = 1 := by grind [binaryRay]
  grind
theorem scale_invariant (x y k : Rat) (hk : k ≠ 0) :
    binaryRay (k*x) (k*y) = binaryRay x y := by
  have kk : 0 < k*k := by
    by_cases hp : 0 < k
    · exact Rat.mul_pos hp hp
    · have hn : 0 < -k := by grind
      have h := Rat.mul_pos hn hn
      grind
  have sameprod : (k*x)*(k*y) = (k*k)*(x*y) := by grind
  have pos := Rat.mul_pos_iff_of_pos_left (b := x*y) kk
  have neg := Rat.mul_lt_mul_left (a := x*y) (b := 0) kk
  have zero : k*y = 0 ↔ y = 0 := by grind [Rat.mul_eq_zero]
  grind [binaryRay]

theorem orthogonal_frame_sum (x y u v : Rat)
    (hxy : x ≠ 0 ∨ y ≠ 0) (huv : u ≠ 0 ∨ v ≠ 0)
    (horth : x*u + y*v = 0) : binaryRay x y + binaryRay u v = 1 := by
  by_cases hx : x = 0
  · have hz : y*v = 0 ↔ y=0 ∨ v=0 := Rat.mul_eq_zero
    have hv0 : v = 0 := by grind
    have hx0 : x*y = 0 := by rw [hx, Rat.zero_mul]
    have hu0 : u*v = 0 := by rw [hv0, Rat.mul_zero]
    grind [binaryRay]
  · have hxi := Rat.mul_inv_cancel x hx
    have hu : u = (v/x)*(-y) := by grind
    have hv : v = (v/x)*x := by grind
    have hk : v/x ≠ 0 := by grind
    calc
      binaryRay x y + binaryRay u v =
          binaryRay x y + binaryRay ((v/x)*(-y)) ((v/x)*x) := by rw [← hu, ← hv]
      _ = binaryRay x y + binaryRay (-y) x := by rw [scale_invariant _ _ _ hk]
      _ = 1 := perpendicular_complement x y hxy

#print axioms orthogonal_frame_sum
#print axioms binary_values
#print axioms perpendicular_complement
#print axioms scale_invariant
#print axioms no_quadratic_representation

end FiniteQm.GleasonRationalPlane

private def l5aProvenance : String :=
  "Origin: lean4/GleasonRationalPlane.lean Claim: binary_values AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"

```


### lean4/BornGaussRat.lean
```lean
import Mathlib.Algebra.Algebra.Defs
import Mathlib.Algebra.BigOperators.Group.Finset.Defs
import Mathlib.Algebra.CharZero.Defs
import Mathlib.Algebra.Order.Field.Rat
import Mathlib.Algebra.Order.Ring.Unbundled.Basic
import Mathlib.Algebra.Star.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-
Gaussian rationals ℚ(i) as a concrete structure; AuthorityEffect: None; supplied carrier arithmetic, no physical claim.

`GaussRat` is the pair type `⟨re, im⟩` over ℚ with the usual complex arithmetic, conjugation
`star ⟨a, b⟩ = ⟨a, -b⟩`, the unit `I = ⟨0, 1⟩`, and `normSq z = z.re ^ 2 + z.im ^ 2`.  It carries
`CommRing`, `StarRing`, `Algebra ℚ`, `Field`, `Nontrivial` and `CharZero` instances, componentwise
simp lemmas, the positivity facts `normSq_nonneg` / `normSq_eq_zero_iff` / `star_mul_self`, and
the ℚ-linearity of the real part over finite sums (`re_sum`, `im_sum`).  Everything is exact
arithmetic over ℚ; nothing here is a physical statement.
-/

namespace BornFable

/-- The Gaussian rationals ℚ(i), stored as a real and an imaginary rational part. -/
@[ext]
structure GaussRat where
  re : ℚ
  im : ℚ
  deriving DecidableEq, Inhabited

namespace GaussRat

/-! ### Primitive operations -/

instance instZero : Zero GaussRat := ⟨⟨0, 0⟩⟩
instance instOne : One GaussRat := ⟨⟨1, 0⟩⟩
instance instAdd : Add GaussRat := ⟨fun z w => ⟨z.re + w.re, z.im + w.im⟩⟩
instance instNeg : Neg GaussRat := ⟨fun z => ⟨-z.re, -z.im⟩⟩
instance instSub : Sub GaussRat := ⟨fun z w => ⟨z.re - w.re, z.im - w.im⟩⟩
instance instMul : Mul GaussRat :=
  ⟨fun z w => ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩⟩
instance instSMul : SMul ℚ GaussRat := ⟨fun q z => ⟨q * z.re, q * z.im⟩⟩
instance instNatSMul : SMul ℕ GaussRat := ⟨fun n z => ⟨n * z.re, n * z.im⟩⟩
instance instIntSMul : SMul ℤ GaussRat := ⟨fun n z => ⟨n * z.re, n * z.im⟩⟩
instance instStar : Star GaussRat := ⟨fun z => ⟨z.re, -z.im⟩⟩
instance instNatCast : NatCast GaussRat := ⟨fun n => ⟨n, 0⟩⟩
instance instIntCast : IntCast GaussRat := ⟨fun n => ⟨n, 0⟩⟩
instance instRatCast : RatCast GaussRat := ⟨fun q => ⟨q, 0⟩⟩

/-- The imaginary unit `i = ⟨0, 1⟩`. -/
def I : GaussRat := ⟨0, 1⟩

/-- The squared modulus `re ^ 2 + im ^ 2`, a rational number. -/
def normSq (z : GaussRat) : ℚ := z.re ^ 2 + z.im ^ 2

/-! ### Componentwise simp lemmas -/

@[simp] theorem re_zero : (0 : GaussRat).re = 0 := rfl
@[simp] theorem im_zero : (0 : GaussRat).im = 0 := rfl
@[simp] theorem re_one : (1 : GaussRat).re = 1 := rfl
@[simp] theorem im_one : (1 : GaussRat).im = 0 := rfl
@[simp] theorem re_add (z w : GaussRat) : (z + w).re = z.re + w.re := rfl
@[simp] theorem im_add (z w : GaussRat) : (z + w).im = z.im + w.im := rfl
@[simp] theorem re_neg (z : GaussRat) : (-z).re = -z.re := rfl
@[simp] theorem im_neg (z : GaussRat) : (-z).im = -z.im := rfl
@[simp] theorem re_sub (z w : GaussRat) : (z - w).re = z.re - w.re := rfl
@[simp] theorem im_sub (z w : GaussRat) : (z - w).im = z.im - w.im := rfl
@[simp] theorem re_mul (z w : GaussRat) : (z * w).re = z.re * w.re - z.im * w.im := rfl
@[simp] theorem im_mul (z w : GaussRat) : (z * w).im = z.re * w.im + z.im * w.re := rfl
@[simp] theorem re_smul (q : ℚ) (z : GaussRat) : (q • z).re = q * z.re := rfl
@[simp] theorem im_smul (q : ℚ) (z : GaussRat) : (q • z).im = q * z.im := rfl
@[simp] theorem re_nsmul (n : ℕ) (z : GaussRat) : (n • z).re = n * z.re := rfl
@[simp] theorem im_nsmul (n : ℕ) (z : GaussRat) : (n • z).im = n * z.im := rfl
@[simp] theorem re_zsmul (n : ℤ) (z : GaussRat) : (n • z).re = n * z.re := rfl
@[simp] theorem im_zsmul (n : ℤ) (z : GaussRat) : (n • z).im = n * z.im := rfl
@[simp] theorem re_star (z : GaussRat) : (star z).re = z.re := rfl
@[simp] theorem im_star (z : GaussRat) : (star z).im = -z.im := rfl
@[simp] theorem re_I : I.re = 0 := rfl
@[simp] theorem im_I : I.im = 1 := rfl
@[simp] theorem re_natCast (n : ℕ) : (n : GaussRat).re = n := rfl
@[simp] theorem im_natCast (n : ℕ) : (n : GaussRat).im = 0 := rfl
@[simp] theorem re_intCast (n : ℤ) : (n : GaussRat).re = n := rfl
@[simp] theorem im_intCast (n : ℤ) : (n : GaussRat).im = 0 := rfl
@[simp] theorem re_ratCast (q : ℚ) : (q : GaussRat).re = q := rfl
@[simp] theorem im_ratCast (q : ℚ) : (q : GaussRat).im = 0 := rfl

@[simp] theorem smul_mk (q a b : ℚ) : q • (⟨a, b⟩ : GaussRat) = ⟨q * a, q * b⟩ := rfl

/-! ### Commutative ring structure -/

instance instCommRing : CommRing GaussRat where
  add_assoc a b c := by ext <;> simp <;> ring
  zero_add a := by ext <;> simp
  add_zero a := by ext <;> simp
  nsmul_zero z := by ext <;> simp
  nsmul_succ n z := by
    ext
    · simp only [re_nsmul, re_add, Nat.cast_succ]
      ring
    · simp only [im_nsmul, im_add, Nat.cast_succ]
      ring
  sub_eq_add_neg a b := by ext <;> simp <;> ring
  zsmul_zero' z := by ext <;> simp
  zsmul_succ' n z := by
    ext
    · simp only [re_zsmul, re_add]
      push_cast
      ring
    · simp only [im_zsmul, im_add]
      push_cast
      ring
  zsmul_neg' n z := by
    ext
    · simp only [re_zsmul, re_neg, Int.cast_negSucc]
      push_cast
      ring
    · simp only [im_zsmul, im_neg, Int.cast_negSucc]
      push_cast
      ring
  neg_add_cancel a := by ext <;> simp
  add_comm a b := by ext <;> simp <;> ring
  left_distrib a b c := by ext <;> simp <;> ring
  right_distrib a b c := by ext <;> simp <;> ring
  zero_mul a := by ext <;> simp
  mul_zero a := by ext <;> simp
  mul_assoc a b c := by ext <;> simp <;> ring
  one_mul a := by ext <;> simp
  mul_one a := by ext <;> simp
  natCast_zero := by ext <;> simp
  natCast_succ n := by ext <;> simp
  intCast_ofNat n := by ext <;> simp
  intCast_negSucc n := by ext <;> simp
  mul_comm a b := by ext <;> simp <;> ring

@[simp] theorem re_ofNat (n : ℕ) [n.AtLeastTwo] : (ofNat(n) : GaussRat).re = ofNat(n) := rfl
@[simp] theorem im_ofNat (n : ℕ) [n.AtLeastTwo] : (ofNat(n) : GaussRat).im = 0 := rfl

instance instNontrivial : Nontrivial GaussRat :=
  ⟨⟨0, 1, fun h => zero_ne_one (congrArg re h)⟩⟩

instance instCharZero : CharZero GaussRat where
  cast_injective := by
    intro m n h
    have h' : (m : ℚ) = (n : ℚ) := congrArg re h
    exact Nat.cast_injective h'

/-! ### Star ring structure (complex conjugation) -/

instance instStarRing : StarRing GaussRat where
  star_involutive z := by ext <;> simp
  star_mul z w := by ext <;> simp <;> ring
  star_add z w := by
    ext
    · rfl
    · simp only [im_star, im_add]
      ring

theorem star_I : star I = -I := by ext <;> simp

/-! ### ℚ-algebra structure -/

/-- The canonical ring embedding `ℚ →+* ℚ(i)`, `q ↦ ⟨q, 0⟩`. -/
def ofRat : ℚ →+* GaussRat where
  toFun q := ⟨q, 0⟩
  map_one' := rfl
  map_mul' q r := by ext <;> simp
  map_zero' := rfl
  map_add' q r := by ext <;> simp

@[simp] theorem re_ofRat (q : ℚ) : (ofRat q).re = q := rfl
@[simp] theorem im_ofRat (q : ℚ) : (ofRat q).im = 0 := rfl

instance instAlgebra : Algebra ℚ GaussRat where
  algebraMap := ofRat
  commutes' q z := mul_comm (ofRat q) z
  smul_def' q z := by ext <;> simp

@[simp] theorem re_algebraMap (q : ℚ) : (algebraMap ℚ GaussRat q).re = q := rfl
@[simp] theorem im_algebraMap (q : ℚ) : (algebraMap ℚ GaussRat q).im = 0 := rfl
theorem algebraMap_eq_ratCast (q : ℚ) : algebraMap ℚ GaussRat q = (q : GaussRat) := rfl

theorem I_mul_I : I * I = -1 := by ext <;> simp

theorem mk_eq_add_mul_I (a b : ℚ) :
    (⟨a, b⟩ : GaussRat) = algebraMap ℚ GaussRat a + algebraMap ℚ GaussRat b * I := by
  ext <;> simp

/-! ### The squared modulus and Hermitian products -/

theorem normSq_nonneg (z : GaussRat) : 0 ≤ normSq z :=
  add_nonneg (sq_nonneg _) (sq_nonneg _)

theorem normSq_eq_zero_iff (z : GaussRat) : normSq z = 0 ↔ z = 0 := by
  rw [normSq, sq, sq, mul_self_add_mul_self_eq_zero, GaussRat.ext_iff, re_zero, im_zero]

theorem normSq_mul (z w : GaussRat) : normSq (z * w) = normSq z * normSq w := by
  simp only [normSq, re_mul, im_mul]
  ring

@[simp] theorem normSq_natCast (n : ℕ) : normSq (n : GaussRat) = (n : ℚ) ^ 2 := by
  rw [normSq, re_natCast, im_natCast]
  ring

theorem star_mul_self (z : GaussRat) : star z * z = algebraMap ℚ GaussRat (normSq z) := by
  ext
  · rw [re_mul, re_star, im_star, re_algebraMap, normSq]
    ring
  · rw [im_mul, re_star, im_star, im_algebraMap]
    ring

theorem re_star_mul_self (z : GaussRat) : (star z * z).re = normSq z := by
  rw [GaussRat.star_mul_self, re_algebraMap]

theorem im_star_mul_self (z : GaussRat) : (star z * z).im = 0 := by
  rw [GaussRat.star_mul_self, im_algebraMap]

theorem re_star_mul (z w : GaussRat) : (star z * w).re = z.re * w.re + z.im * w.im := by
  rw [re_mul, re_star, im_star]
  ring

theorem im_star_mul (z w : GaussRat) : (star z * w).im = z.re * w.im - z.im * w.re := by
  rw [im_mul, re_star, im_star]
  ring

theorem re_star_mul_comm (z w : GaussRat) : (star z * w).re = (star w * z).re := by
  rw [re_star_mul, re_star_mul]
  ring

theorem im_star_mul_comm (z w : GaussRat) : (star z * w).im = -(star w * z).im := by
  rw [im_star_mul, im_star_mul]
  ring

theorem re_smul_rat (q : ℚ) (z : GaussRat) : (q • z).re = q * z.re := rfl

theorem re_algebraMap_mul (q : ℚ) (z : GaussRat) :
    (algebraMap ℚ GaussRat q * z).re = q * z.re := by
  rw [re_mul, re_algebraMap, im_algebraMap, zero_mul, sub_zero]

/-! ### The real and imaginary parts are additive (hence ℚ-linear) -/

/-- The real part as an additive monoid homomorphism `ℚ(i) →+ ℚ`. -/
def reAddMonoidHom : GaussRat →+ ℚ where
  toFun := re
  map_zero' := rfl
  map_add' _ _ := rfl

/-- The imaginary part as an additive monoid homomorphism `ℚ(i) →+ ℚ`. -/
def imAddMonoidHom : GaussRat →+ ℚ where
  toFun := im
  map_zero' := rfl
  map_add' _ _ := rfl

@[simp] theorem reAddMonoidHom_apply (z : GaussRat) : reAddMonoidHom z = z.re := rfl
@[simp] theorem imAddMonoidHom_apply (z : GaussRat) : imAddMonoidHom z = z.im := rfl

@[simp] theorem re_sum {ι : Type*} (s : Finset ι) (f : ι → GaussRat) :
    (∑ i ∈ s, f i).re = ∑ i ∈ s, (f i).re :=
  map_sum reAddMonoidHom f s

@[simp] theorem im_sum {ι : Type*} (s : Finset ι) (f : ι → GaussRat) :
    (∑ i ∈ s, f i).im = ∑ i ∈ s, (f i).im :=
  map_sum imAddMonoidHom f s

/-! ### Field structure -/

instance instInv : Inv GaussRat := ⟨fun z => (normSq z)⁻¹ • star z⟩

@[simp] theorem re_inv (z : GaussRat) : z⁻¹.re = (normSq z)⁻¹ * z.re := rfl
@[simp] theorem im_inv (z : GaussRat) : z⁻¹.im = (normSq z)⁻¹ * -z.im := rfl

protected theorem inv_zero : (0 : GaussRat)⁻¹ = 0 := by ext <;> simp

protected theorem mul_inv_cancel (z : GaussRat) (hz : z ≠ 0) : z * z⁻¹ = 1 := by
  have h : normSq z ≠ 0 := fun h0 => hz ((normSq_eq_zero_iff z).mp h0)
  have h2 : z.re * ((normSq z)⁻¹ * z.re) - z.im * ((normSq z)⁻¹ * -z.im) =
      (normSq z)⁻¹ * normSq z := by
    unfold normSq
    ring
  ext
  · rw [re_mul, re_inv, im_inv, re_one, h2, inv_mul_cancel₀ h]
  · rw [im_mul, re_inv, im_inv, im_one]
    ring

instance instDivInvMonoid : DivInvMonoid GaussRat where

instance instField : Field GaussRat where
  mul_inv_cancel := GaussRat.mul_inv_cancel
  inv_zero := GaussRat.inv_zero
  nnqsmul := _
  qsmul := (· • ·)
  qsmul_def q z := by ext <;> simp
  ratCast_def q := by
    have hd : (q.den : ℚ) ≠ 0 := Nat.cast_ne_zero.mpr q.den_ne_zero
    have h2 : ((q.den : ℚ) ^ 2)⁻¹ * (q.den : ℚ) = (q.den : ℚ)⁻¹ := by
      rw [sq, mul_inv, mul_assoc, inv_mul_cancel₀ hd, mul_one]
    ext
    · simp only [re_ratCast, div_eq_mul_inv, re_mul, re_inv, im_inv, re_intCast, im_intCast,
        re_natCast, im_natCast, normSq_natCast, zero_mul, sub_zero]
      rw [h2, ← div_eq_mul_inv, Rat.num_div_den]
    · simp [div_eq_mul_inv]

/-! ### Instance sanity checks -/

example : Module ℚ GaussRat := inferInstance
example : IsScalarTower ℚ GaussRat GaussRat := inferInstance
example : SMulCommClass ℚ GaussRat GaussRat := inferInstance
example : ((⟨3, 4⟩ : GaussRat) * star ⟨3, 4⟩).re = 25 := by norm_num
example : normSq ⟨3, 4⟩ = 25 := by norm_num [normSq]

end GaussRat

end BornFable

#print axioms BornFable.GaussRat.instCommRing
#print axioms BornFable.GaussRat.instStarRing
#print axioms BornFable.GaussRat.instAlgebra
#print axioms BornFable.GaussRat.instField
#print axioms BornFable.GaussRat.instNontrivial
#print axioms BornFable.GaussRat.instCharZero
#print axioms BornFable.GaussRat.re_zero
#print axioms BornFable.GaussRat.im_zero
#print axioms BornFable.GaussRat.re_one
#print axioms BornFable.GaussRat.im_one
#print axioms BornFable.GaussRat.re_add
#print axioms BornFable.GaussRat.im_add
#print axioms BornFable.GaussRat.re_neg
#print axioms BornFable.GaussRat.im_neg
#print axioms BornFable.GaussRat.re_sub
#print axioms BornFable.GaussRat.im_sub
#print axioms BornFable.GaussRat.re_mul
#print axioms BornFable.GaussRat.im_mul
#print axioms BornFable.GaussRat.re_smul
#print axioms BornFable.GaussRat.im_smul
#print axioms BornFable.GaussRat.re_star
#print axioms BornFable.GaussRat.im_star
#print axioms BornFable.GaussRat.re_I
#print axioms BornFable.GaussRat.im_I
#print axioms BornFable.GaussRat.re_natCast
#print axioms BornFable.GaussRat.im_natCast
#print axioms BornFable.GaussRat.re_intCast
#print axioms BornFable.GaussRat.im_intCast
#print axioms BornFable.GaussRat.re_ratCast
#print axioms BornFable.GaussRat.im_ratCast
#print axioms BornFable.GaussRat.smul_mk
#print axioms BornFable.GaussRat.re_nsmul
#print axioms BornFable.GaussRat.im_nsmul
#print axioms BornFable.GaussRat.re_zsmul
#print axioms BornFable.GaussRat.im_zsmul
#print axioms BornFable.GaussRat.re_ofNat
#print axioms BornFable.GaussRat.im_ofNat
#print axioms BornFable.GaussRat.star_I
#print axioms BornFable.GaussRat.re_ofRat
#print axioms BornFable.GaussRat.im_ofRat
#print axioms BornFable.GaussRat.re_algebraMap
#print axioms BornFable.GaussRat.im_algebraMap
#print axioms BornFable.GaussRat.algebraMap_eq_ratCast
#print axioms BornFable.GaussRat.I_mul_I
#print axioms BornFable.GaussRat.mk_eq_add_mul_I
#print axioms BornFable.GaussRat.normSq_nonneg
#print axioms BornFable.GaussRat.normSq_eq_zero_iff
#print axioms BornFable.GaussRat.normSq_mul
#print axioms BornFable.GaussRat.normSq_natCast
#print axioms BornFable.GaussRat.star_mul_self
#print axioms BornFable.GaussRat.re_star_mul_self
#print axioms BornFable.GaussRat.im_star_mul_self
#print axioms BornFable.GaussRat.re_star_mul
#print axioms BornFable.GaussRat.im_star_mul
#print axioms BornFable.GaussRat.re_star_mul_comm
#print axioms BornFable.GaussRat.im_star_mul_comm
#print axioms BornFable.GaussRat.re_smul_rat
#print axioms BornFable.GaussRat.re_algebraMap_mul
#print axioms BornFable.GaussRat.reAddMonoidHom_apply
#print axioms BornFable.GaussRat.imAddMonoidHom_apply
#print axioms BornFable.GaussRat.re_sum
#print axioms BornFable.GaussRat.im_sum
#print axioms BornFable.GaussRat.re_inv
#print axioms BornFable.GaussRat.im_inv
#print axioms BornFable.GaussRat.inv_zero
#print axioms BornFable.GaussRat.mul_inv_cancel

```
