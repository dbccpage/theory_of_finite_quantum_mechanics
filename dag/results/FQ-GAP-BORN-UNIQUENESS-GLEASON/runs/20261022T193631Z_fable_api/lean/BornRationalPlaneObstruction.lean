import BornRationalSphereObstruction
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# An exotic frame function on *all* rational rays of `ℚ³`

AuthorityEffect: None.

Scope.  `BornRationalSphereObstruction` works on the rational *unit sphere* (integer vectors with
square norm).  Here the carrier is every integer vector `v = (a, b, c)` with not all coordinates
even (`IsPrimitive`); every rational ray of `ℚ³` has such a representative, and two such
representatives of the same ray differ by a factor `p/q` with `p, q` odd.

`sgn v ∈ {-1, 0, 1}` is `0` unless exactly two coordinates `x, y` are odd, in which case it is
`-1` if `x ≡ y (mod 4)` and `1` if `x ≡ -y (mod 4)`.  `exotic v = (1 + sgn v) / 3`.

Main results:
* `exotic_frame_function`: on every pairwise orthogonal triple of primitive vectors the values of
  `exotic` sum to `1` (no square-norm hypothesis).
* `exotic_eq_of_odd_scalings`, `exotic_neg`: `exotic` is a function of the rational ray.
* `exotic_not_quadratic`: no rational symmetric `3 × 3` form represents `exotic`.
* `exotic_eq_third_of_isRay`: on the rational unit sphere `exotic` is the constant `1/3`.
* `no_real_triangle`: over `ℤ³` there is no orthogonal triple all of whose members are
  `≡ (1,1,0) (mod 2)` (contrast with the Gaussian case in `BornGaussianRationalFrameObstruction`).

Nothing here is a statement about physics.
-/

namespace BornFable.RationalPlane

open BornFable.RationalSphere

/-- `v ∈ ℤ³` is *odd-primitive*: not all coordinates are even. -/
def IsPrimitive (v : Vec3) : Prop := ¬ (v.a % 2 = 0 ∧ v.b % 2 = 0 ∧ v.c % 2 = 0)

theorem isPrimitive_of_isRay {v : Vec3} (h : v.IsRay) : IsPrimitive v := by
  intro hc
  exact h.1 ⟨Int.even_iff.mpr hc.1, Int.even_iff.mpr hc.2.1, Int.even_iff.mpr hc.2.2⟩

/-- For odd `x, y`: `-1` if `x ≡ y (mod 4)`, `1` if `x ≡ -y (mod 4)`. -/
def pairSign (x y : ℤ) : ℤ := if (x - y) % 4 = 0 then -1 else 1

/-- The sign invariant: nonzero exactly when exactly two coordinates are odd. -/
def sgn (v : Vec3) : ℤ :=
  if v.a % 2 = 1 ∧ v.b % 2 = 1 ∧ v.c % 2 = 0 then pairSign v.a v.b
  else if v.a % 2 = 1 ∧ v.c % 2 = 1 ∧ v.b % 2 = 0 then pairSign v.a v.c
  else if v.b % 2 = 1 ∧ v.c % 2 = 1 ∧ v.a % 2 = 0 then pairSign v.b v.c
  else 0

/-- The exotic frame function, with values in `{0, 1/3, 2/3}`. -/
def exotic (v : Vec3) : ℚ := (1 + sgn v) / 3

/-! ### Specification of `sgn` by congruences -/

/-- Complete case description of `sgn ⟨a, b, c⟩`. -/
theorem sgn_spec (a b c : ℤ) :
    (a % 2 = 1 ∧ b % 2 = 1 ∧ c % 2 = 0 ∧
        (((a - b) % 4 = 0 ∧ sgn ⟨a, b, c⟩ = -1) ∨ ((a - b) % 4 ≠ 0 ∧ sgn ⟨a, b, c⟩ = 1))) ∨
    (a % 2 = 1 ∧ c % 2 = 1 ∧ b % 2 = 0 ∧
        (((a - c) % 4 = 0 ∧ sgn ⟨a, b, c⟩ = -1) ∨ ((a - c) % 4 ≠ 0 ∧ sgn ⟨a, b, c⟩ = 1))) ∨
    (b % 2 = 1 ∧ c % 2 = 1 ∧ a % 2 = 0 ∧
        (((b - c) % 4 = 0 ∧ sgn ⟨a, b, c⟩ = -1) ∨ ((b - c) % 4 ≠ 0 ∧ sgn ⟨a, b, c⟩ = 1))) ∨
    (((a % 2 = 0 ∧ b % 2 = 0 ∧ c % 2 = 0) ∨ (a % 2 = 1 ∧ b % 2 = 0 ∧ c % 2 = 0) ∨
        (a % 2 = 0 ∧ b % 2 = 1 ∧ c % 2 = 0) ∨ (a % 2 = 0 ∧ b % 2 = 0 ∧ c % 2 = 1) ∨
        (a % 2 = 1 ∧ b % 2 = 1 ∧ c % 2 = 1)) ∧ sgn ⟨a, b, c⟩ = 0) := by
  simp only [sgn, pairSign]
  split_ifs <;> omega

/-- `sgn_spec` for an arbitrary vector. -/
theorem sgn_spec' (v : Vec3) :
    (v.a % 2 = 1 ∧ v.b % 2 = 1 ∧ v.c % 2 = 0 ∧
        (((v.a - v.b) % 4 = 0 ∧ sgn v = -1) ∨ ((v.a - v.b) % 4 ≠ 0 ∧ sgn v = 1))) ∨
    (v.a % 2 = 1 ∧ v.c % 2 = 1 ∧ v.b % 2 = 0 ∧
        (((v.a - v.c) % 4 = 0 ∧ sgn v = -1) ∨ ((v.a - v.c) % 4 ≠ 0 ∧ sgn v = 1))) ∨
    (v.b % 2 = 1 ∧ v.c % 2 = 1 ∧ v.a % 2 = 0 ∧
        (((v.b - v.c) % 4 = 0 ∧ sgn v = -1) ∨ ((v.b - v.c) % 4 ≠ 0 ∧ sgn v = 1))) ∨
    (((v.a % 2 = 0 ∧ v.b % 2 = 0 ∧ v.c % 2 = 0) ∨ (v.a % 2 = 1 ∧ v.b % 2 = 0 ∧ v.c % 2 = 0) ∨
        (v.a % 2 = 0 ∧ v.b % 2 = 1 ∧ v.c % 2 = 0) ∨ (v.a % 2 = 0 ∧ v.b % 2 = 0 ∧ v.c % 2 = 1) ∨
        (v.a % 2 = 1 ∧ v.b % 2 = 1 ∧ v.c % 2 = 1)) ∧ sgn v = 0) := by
  obtain ⟨a, b, c⟩ := v
  exact sgn_spec a b c

theorem sgn_mem (v : Vec3) : sgn v = -1 ∨ sgn v = 0 ∨ sgn v = 1 := by
  have := sgn_spec' v
  omega

/-! ### Products modulo 4 -/

/-- The residue of a product modulo `4` in terms of the factors. -/
theorem mul_emod_four (x y : ℤ) :
    (x % 2 = 0 ∧ y % 2 = 0 ∧ x * y % 4 = 0) ∨
    (x % 2 = 1 ∧ y % 2 = 1 ∧ (x - y) % 4 = 0 ∧ x * y % 4 = 1) ∨
    (x % 2 = 1 ∧ y % 2 = 1 ∧ (x - y) % 4 ≠ 0 ∧ x * y % 4 = 3) ∨
    ((x + y) % 2 = 1 ∧ x * y % 2 = 0) := by
  have h : x * y % 4 = x % 4 * (y % 4) % 4 := Int.mul_emod x y 4
  have hx : x % 4 = 0 ∨ x % 4 = 1 ∨ x % 4 = 2 ∨ x % 4 = 3 := by omega
  have hy : y % 4 = 0 ∨ y % 4 = 1 ∨ y % 4 = 2 ∨ y % 4 = 3 := by omega
  rcases hx with hx | hx | hx | hx <;> rcases hy with hy | hy | hy | hy <;>
    rw [hx, hy] at h <;> omega

/-- Multiplication by an odd integer preserves divisibility by `4`. -/
theorem odd_mul_emod_four (k m : ℤ) (hk : k % 2 = 1) : k * m % 4 = 0 ↔ m % 4 = 0 := by
  have h : k * m % 4 = k % 4 * (m % 4) % 4 := Int.mul_emod k m 4
  have hk' : k % 4 = 1 ∨ k % 4 = 3 := by omega
  have hm : m % 4 = 0 ∨ m % 4 = 1 ∨ m % 4 = 2 ∨ m % 4 = 3 := by omega
  rcases hk' with hk' | hk' <;> rcases hm with hm | hm | hm | hm <;>
    rw [hk', hm] at h <;> omega

/-! ### Frame additivity -/

/-- On every pairwise orthogonal triple of odd-primitive integer vectors the signs sum to `0`. -/
set_option maxHeartbeats 4000000 in
theorem sgn_frame {u v w : Vec3} (hu : IsPrimitive u) (hv : IsPrimitive v) (hw : IsPrimitive w)
    (huv : u.dot v = 0) (huw : u.dot w = 0) (hvw : v.dot w = 0) :
    sgn u + sgn v + sgn w = 0 := by
  simp only [IsPrimitive, Vec3.dot] at hu hv hw huv huw hvw
  have su := sgn_spec' u
  have sv := sgn_spec' v
  have sw := sgn_spec' w
  have m₁ := mul_emod_four u.a v.a
  have m₂ := mul_emod_four u.b v.b
  have m₃ := mul_emod_four u.c v.c
  have m₄ := mul_emod_four u.a w.a
  have m₅ := mul_emod_four u.b w.b
  have m₆ := mul_emod_four u.c w.c
  have m₇ := mul_emod_four v.a w.a
  have m₈ := mul_emod_four v.b w.b
  have m₉ := mul_emod_four v.c w.c
  have p₁ : u.a % 2 = 0 ∨ u.a % 2 = 1 := by omega
  have p₂ : u.b % 2 = 0 ∨ u.b % 2 = 1 := by omega
  have p₃ : u.c % 2 = 0 ∨ u.c % 2 = 1 := by omega
  have p₄ : v.a % 2 = 0 ∨ v.a % 2 = 1 := by omega
  have p₅ : v.b % 2 = 0 ∨ v.b % 2 = 1 := by omega
  have p₆ : v.c % 2 = 0 ∨ v.c % 2 = 1 := by omega
  have p₇ : w.a % 2 = 0 ∨ w.a % 2 = 1 := by omega
  have p₈ : w.b % 2 = 0 ∨ w.b % 2 = 1 := by omega
  have p₉ : w.c % 2 = 0 ∨ w.c % 2 = 1 := by omega
  rcases p₁ with p₁ | p₁ <;> rcases p₂ with p₂ | p₂ <;> rcases p₃ with p₃ | p₃ <;>
    rcases p₄ with p₄ | p₄ <;> rcases p₅ with p₅ | p₅ <;> rcases p₆ with p₆ | p₆ <;>
    rcases p₇ with p₇ | p₇ <;> rcases p₈ with p₈ | p₈ <;> rcases p₉ with p₉ | p₉ <;>
    omega

/-- Frame additivity of `exotic` on all orthogonal triples of odd-primitive integer vectors. -/
theorem exotic_frame_function {u v w : Vec3} (hu : IsPrimitive u) (hv : IsPrimitive v)
    (hw : IsPrimitive w) (huv : u.dot v = 0) (huw : u.dot w = 0) (hvw : v.dot w = 0) :
    exotic u + exotic v + exotic w = 1 := by
  have h := sgn_frame hu hv hw huv huw hvw
  have h' : ((sgn u : ℚ) + sgn v + sgn w) = 0 := by exact_mod_cast h
  unfold exotic
  linarith

theorem exotic_three_valued (v : Vec3) :
    exotic v = 0 ∨ exotic v = 1 / 3 ∨ exotic v = 2 / 3 := by
  unfold exotic
  rcases sgn_mem v with h | h | h <;> rw [h] <;> norm_num

/-- Over `ℤ³` no orthogonal triple has all three members `≡ (1, 1, 0) (mod 2)`. -/
theorem no_real_triangle {u v w : Vec3} (hu : IsPrimitive u) (hv : IsPrimitive v)
    (hw : IsPrimitive w) (huv : u.dot v = 0) (huw : u.dot w = 0) (hvw : v.dot w = 0) :
    ¬ ((u.a % 2 = 1 ∧ u.b % 2 = 1 ∧ u.c % 2 = 0) ∧ (v.a % 2 = 1 ∧ v.b % 2 = 1 ∧ v.c % 2 = 0) ∧
        (w.a % 2 = 1 ∧ w.b % 2 = 1 ∧ w.c % 2 = 0)) := by
  intro h
  have h0 := sgn_frame hu hv hw huv huw hvw
  have su := sgn_spec' u
  have sv := sgn_spec' v
  have sw := sgn_spec' w
  omega

/-! ### Ray invariance -/

theorem sgn_neg (a b c : ℤ) : sgn ⟨-a, -b, -c⟩ = sgn ⟨a, b, c⟩ := by
  have h1 := sgn_spec (-a) (-b) (-c)
  have h2 := sgn_spec a b c
  omega

theorem sgn_odd_smul {k : ℤ} (hk : k % 2 = 1) (a b c : ℤ) :
    sgn ⟨k * a, k * b, k * c⟩ = sgn ⟨a, b, c⟩ := by
  have h1 := sgn_spec (k * a) (k * b) (k * c)
  have h2 := sgn_spec a b c
  have e1 := mul_emod_two_eq_one k a
  have e2 := mul_emod_two_eq_one k b
  have e3 := mul_emod_two_eq_one k c
  have f1 := odd_mul_emod_four k (a - b) hk
  have f2 := odd_mul_emod_four k (a - c) hk
  have f3 := odd_mul_emod_four k (b - c) hk
  have r1 : k * a - k * b = k * (a - b) := by ring
  have r2 : k * a - k * c = k * (a - c) := by ring
  have r3 : k * b - k * c = k * (b - c) := by ring
  omega

/-- If `q • u = p • u'` with `p, q` odd (the only way two odd-primitive vectors can represent the
same rational ray), the signs agree. -/
theorem sgn_eq_of_odd_scalings {p q : ℤ} (hp : p % 2 = 1) (hq : q % 2 = 1) {u u' : Vec3}
    (h1 : q * u.a = p * u'.a) (h2 : q * u.b = p * u'.b) (h3 : q * u.c = p * u'.c) :
    sgn u = sgn u' := by
  have e1 : sgn ⟨q * u.a, q * u.b, q * u.c⟩ = sgn u := sgn_odd_smul hq u.a u.b u.c
  have e2 : sgn ⟨p * u'.a, p * u'.b, p * u'.c⟩ = sgn u' := sgn_odd_smul hp u'.a u'.b u'.c
  rw [h1, h2, h3] at e1
  exact e1.symm.trans e2

theorem exotic_neg (a b c : ℤ) : exotic ⟨-a, -b, -c⟩ = exotic ⟨a, b, c⟩ := by
  unfold exotic
  rw [sgn_neg]

theorem exotic_eq_of_odd_scalings {p q : ℤ} (hp : p % 2 = 1) (hq : q % 2 = 1) {u u' : Vec3}
    (h1 : q * u.a = p * u'.a) (h2 : q * u.b = p * u'.b) (h3 : q * u.c = p * u'.c) :
    exotic u = exotic u' := by
  unfold exotic
  rw [sgn_eq_of_odd_scalings hp hq h1 h2 h3]

/-! ### Comparison with the rational unit sphere -/

/-- On repository rays (square norm) exactly one coordinate is odd, so `sgn = 0`. -/
theorem sgn_eq_zero_of_isRay {v : Vec3} (hv : v.IsRay) : sgn v = 0 := by
  have h := ray_exactly_one_odd hv
  simp only [Int.odd_iff, Int.even_iff] at h
  have hs := sgn_spec' v
  omega

/-- On the rational unit sphere `exotic` is the constant `1/3` (the Born value of `ρ = I/3`). -/
theorem exotic_eq_third_of_isRay {v : Vec3} (hv : v.IsRay) : exotic v = 1 / 3 := by
  unfold exotic
  rw [sgn_eq_zero_of_isRay hv]
  norm_num

/-! ### Seven explicit primitive vectors -/

theorem prim_100 : IsPrimitive ⟨1, 0, 0⟩ := by
  first | (unfold IsPrimitive; decide) | (norm_num [IsPrimitive])
theorem prim_010 : IsPrimitive ⟨0, 1, 0⟩ := by
  first | (unfold IsPrimitive; decide) | (norm_num [IsPrimitive])
theorem prim_001 : IsPrimitive ⟨0, 0, 1⟩ := by
  first | (unfold IsPrimitive; decide) | (norm_num [IsPrimitive])
theorem prim_110 : IsPrimitive ⟨1, 1, 0⟩ := by
  first | (unfold IsPrimitive; decide) | (norm_num [IsPrimitive])
theorem prim_101 : IsPrimitive ⟨1, 0, 1⟩ := by
  first | (unfold IsPrimitive; decide) | (norm_num [IsPrimitive])
theorem prim_011 : IsPrimitive ⟨0, 1, 1⟩ := by
  first | (unfold IsPrimitive; decide) | (norm_num [IsPrimitive])
theorem prim_111 : IsPrimitive ⟨1, 1, 1⟩ := by
  first | (unfold IsPrimitive; decide) | (norm_num [IsPrimitive])

theorem sgn_100 : sgn ⟨1, 0, 0⟩ = 0 := by first | decide | norm_num [sgn, pairSign]
theorem sgn_010 : sgn ⟨0, 1, 0⟩ = 0 := by first | decide | norm_num [sgn, pairSign]
theorem sgn_001 : sgn ⟨0, 0, 1⟩ = 0 := by first | decide | norm_num [sgn, pairSign]
theorem sgn_110 : sgn ⟨1, 1, 0⟩ = -1 := by first | decide | norm_num [sgn, pairSign]
theorem sgn_101 : sgn ⟨1, 0, 1⟩ = -1 := by first | decide | norm_num [sgn, pairSign]
theorem sgn_011 : sgn ⟨0, 1, 1⟩ = -1 := by first | decide | norm_num [sgn, pairSign]
theorem sgn_111 : sgn ⟨1, 1, 1⟩ = 0 := by first | decide | norm_num [sgn, pairSign]
theorem sgn_1m10 : sgn ⟨1, -1, 0⟩ = 1 := by first | decide | norm_num [sgn, pairSign]

theorem exotic_100 : exotic ⟨1, 0, 0⟩ = 1 / 3 := by rw [exotic, sgn_100]; norm_num
theorem exotic_010 : exotic ⟨0, 1, 0⟩ = 1 / 3 := by rw [exotic, sgn_010]; norm_num
theorem exotic_001 : exotic ⟨0, 0, 1⟩ = 1 / 3 := by rw [exotic, sgn_001]; norm_num
theorem exotic_110 : exotic ⟨1, 1, 0⟩ = 0 := by rw [exotic, sgn_110]; norm_num
theorem exotic_101 : exotic ⟨1, 0, 1⟩ = 0 := by rw [exotic, sgn_101]; norm_num
theorem exotic_011 : exotic ⟨0, 1, 1⟩ = 0 := by rw [exotic, sgn_011]; norm_num
theorem exotic_111 : exotic ⟨1, 1, 1⟩ = 1 / 3 := by rw [exotic, sgn_111]; norm_num
theorem exotic_1m10 : exotic ⟨1, -1, 0⟩ = 2 / 3 := by rw [exotic, sgn_1m10]; norm_num

/-! ### The obstruction -/

/-- No rational symmetric `3 × 3` form `Q` satisfies `Q(v) = exotic v · (a² + b² + c²)` on all
odd-primitive integer vectors (the Born value of the ray times the norm squared). -/
theorem exotic_not_quadratic :
    ¬ ∃ r00 r11 r22 r01 r02 r12 : ℚ, ∀ v : Vec3, IsPrimitive v →
      r00 * (v.a : ℚ) ^ 2 + r11 * (v.b : ℚ) ^ 2 + r22 * (v.c : ℚ) ^ 2
        + 2 * r01 * ((v.a : ℚ) * v.b) + 2 * r02 * ((v.a : ℚ) * v.c) + 2 * r12 * ((v.b : ℚ) * v.c)
        = exotic v * ((v.a : ℚ) ^ 2 + (v.b : ℚ) ^ 2 + (v.c : ℚ) ^ 2) := by
  rintro ⟨r00, r11, r22, r01, r02, r12, h⟩
  have h1 := h _ prim_100
  have h2 := h _ prim_010
  have h3 := h _ prim_001
  have h4 := h _ prim_110
  have h5 := h _ prim_101
  have h6 := h _ prim_011
  have h7 := h _ prim_111
  norm_num [exotic_100, exotic_010, exotic_001, exotic_110, exotic_101, exotic_011, exotic_111]
    at h1 h2 h3 h4 h5 h6 h7
  linarith

end BornFable.RationalPlane

#print axioms BornFable.RationalPlane.isPrimitive_of_isRay
#print axioms BornFable.RationalPlane.sgn_spec
#print axioms BornFable.RationalPlane.sgn_spec'
#print axioms BornFable.RationalPlane.sgn_mem
#print axioms BornFable.RationalPlane.mul_emod_four
#print axioms BornFable.RationalPlane.odd_mul_emod_four
#print axioms BornFable.RationalPlane.sgn_frame
#print axioms BornFable.RationalPlane.exotic_frame_function
#print axioms BornFable.RationalPlane.exotic_three_valued
#print axioms BornFable.RationalPlane.no_real_triangle
#print axioms BornFable.RationalPlane.sgn_neg
#print axioms BornFable.RationalPlane.sgn_odd_smul
#print axioms BornFable.RationalPlane.sgn_eq_of_odd_scalings
#print axioms BornFable.RationalPlane.exotic_neg
#print axioms BornFable.RationalPlane.exotic_eq_of_odd_scalings
#print axioms BornFable.RationalPlane.sgn_eq_zero_of_isRay
#print axioms BornFable.RationalPlane.exotic_eq_third_of_isRay
#print axioms BornFable.RationalPlane.exotic_not_quadratic
