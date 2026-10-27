import Mathlib.Algebra.Ring.Int.Parity
import Mathlib.Algebra.Order.Field.Rat
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# A non-quadratic frame function on *all* rational rays of `ℚ³`

AuthorityEffect: None.

Scope.  `BornRationalSphereObstruction` gives a two-valued frame function on the rational points
of the unit sphere (rays whose integer representative has square norm).  Here the carrier is the
set of *all* rational rays of `ℚ³`: integer vectors `(a, b, c)` with not all coordinates even.
Every nonzero rational vector is a rational multiple of such a vector, and the function below is
invariant under `v ↦ -v` and under scaling by odd integers (`sgn_neg`, `sgn_odd_smul`), so it is a
function of the rational ray.

The function.  Call a coordinate pattern *weight two* when exactly two coordinates are odd.  For
such a vector put `pairSign = -1` if the two odd coordinates are congruent modulo `4` and `+1`
otherwise; for all other patterns put `sgn = 0`.  Then `exotic v = (1 + sgn v) / 3`.

Main results.
* `exotic_frame_function`: `exotic u + exotic v + exotic w = 1` on every pairwise orthogonal
  triple of rays.  The proof is a parity analysis: modulo `2` the three odd-coordinate patterns
  are pairwise orthogonal in `𝔽₂³`, which forces every weight-two pattern in a frame to occur
  exactly twice (or three times), and for two orthogonal weight-two vectors with the same pattern
  the exact orthogonality relation modulo `4` forces opposite signs (`pairSign_add_eq_zero`).
* `exotic_not_quadratic`: no rational symmetric `3 × 3` form `Q` has
  `Q(v) = exotic v · (a² + b² + c²)` on all rays; seven rays suffice.
* `exotic_values`, `exotic_nonneg`: the function takes the values `0, 1/3, 2/3`.

So, over `ℚ³`, frame additivity on all orthogonal triples of rational rays does not force the
Born (quadratic) form, even for nonnegative frame functions.  Nothing here concerns `ℚ(i)³`, and
nothing here is a statement about physics.
-/

namespace BornFinite.RationalRays

/-- An integer vector `(a, b, c) ∈ ℤ³`. -/
structure Vec3 where
  a : ℤ
  b : ℤ
  c : ℤ

namespace Vec3

/-- The integer dot product. -/
def dot (u v : Vec3) : ℤ := u.a * v.a + u.b * v.b + u.c * v.c

/-- `v` represents a rational ray: not all coordinates are even. -/
def IsRay (v : Vec3) : Prop := ¬ (Even v.a ∧ Even v.b ∧ Even v.c)

end Vec3

/-- For two odd integers: `-1` if they are congruent modulo `4`, else `+1`. -/
def pairSign (x y : ℤ) : ℤ := if (x - y) % 4 = 0 then -1 else 1

/-- The sign of a vector: `pairSign` of the two odd coordinates when exactly two coordinates are
odd, and `0` otherwise. -/
def sgn (v : Vec3) : ℤ :=
  if v.a % 2 = 1 ∧ v.b % 2 = 1 ∧ v.c % 2 = 0 then pairSign v.a v.b
  else if v.a % 2 = 1 ∧ v.c % 2 = 1 ∧ v.b % 2 = 0 then pairSign v.a v.c
  else if v.b % 2 = 1 ∧ v.c % 2 = 1 ∧ v.a % 2 = 0 then pairSign v.b v.c
  else 0

/-- The exotic frame function `(1 + sgn v) / 3`. -/
def exotic (v : Vec3) : ℚ := (1 + (sgn v : ℚ)) / 3

/-! ### The key congruence modulo `4` -/

/-- If `a, b, c, d` are odd, `e, f` are even and `a c + b d + e f = 0`, then exactly one of the
pairs `(a, b)`, `(c, d)` is congruent modulo `4`; equivalently the two pair signs cancel. -/
theorem pairSign_add_eq_zero {a b c d e f : ℤ} (ha : a % 2 = 1) (hb : b % 2 = 1)
    (hc : c % 2 = 1) (hd : d % 2 = 1) (he : e % 2 = 0) (hf : f % 2 = 0)
    (h : a * c + b * d + e * f = 0) : pairSign a b + pairSign c d = 0 := by
  have hac := Int.mul_emod a c 4
  have hbd := Int.mul_emod b d 4
  have hef := Int.mul_emod e f 4
  have ha4 : a % 4 = 1 ∨ a % 4 = 3 := by omega
  have hb4 : b % 4 = 1 ∨ b % 4 = 3 := by omega
  have hc4 : c % 4 = 1 ∨ c % 4 = 3 := by omega
  have hd4 : d % 4 = 1 ∨ d % 4 = 3 := by omega
  have he4 : e % 4 = 0 ∨ e % 4 = 2 := by omega
  have hf4 : f % 4 = 0 ∨ f % 4 = 2 := by omega
  unfold pairSign
  rcases ha4 with ha4 | ha4 <;> rcases hb4 with hb4 | hb4 <;> rcases hc4 with hc4 | hc4 <;>
    rcases hd4 with hd4 | hd4 <;> rcases he4 with he4 | he4 <;> rcases hf4 with hf4 | hf4 <;>
    simp only [ha4, hb4, hc4, hd4, he4, hf4] at hac hbd hef <;> split_ifs <;> omega

/-- A product is odd exactly when both factors are odd (in `% 2` form). -/
theorem mul_emod_two_eq_one (x y : ℤ) : x * y % 2 = 1 ↔ x % 2 = 1 ∧ y % 2 = 1 := by
  have h := Int.odd_mul (m := x) (n := y)
  simp only [Int.odd_iff] at h
  exact h

/-- The pair-sign cancellation for two vectors sharing the weight-two pattern `{a, b}`. -/
theorem cancel_ab {u v : Vec3} (huv : u.dot v = 0) :
    u.a % 2 = 1 → u.b % 2 = 1 → u.c % 2 = 0 → v.a % 2 = 1 → v.b % 2 = 1 → v.c % 2 = 0 →
      pairSign u.a u.b + pairSign v.a v.b = 0 := fun h1 h2 h3 h4 h5 h6 =>
  pairSign_add_eq_zero h1 h2 h4 h5 h3 h6 (by simp only [Vec3.dot] at huv; linarith)

/-- The pair-sign cancellation for two vectors sharing the weight-two pattern `{a, c}`. -/
theorem cancel_ac {u v : Vec3} (huv : u.dot v = 0) :
    u.a % 2 = 1 → u.c % 2 = 1 → u.b % 2 = 0 → v.a % 2 = 1 → v.c % 2 = 1 → v.b % 2 = 0 →
      pairSign u.a u.c + pairSign v.a v.c = 0 := fun h1 h2 h3 h4 h5 h6 =>
  pairSign_add_eq_zero h1 h2 h4 h5 h3 h6 (by simp only [Vec3.dot] at huv; linarith)

/-- The pair-sign cancellation for two vectors sharing the weight-two pattern `{b, c}`. -/
theorem cancel_bc {u v : Vec3} (huv : u.dot v = 0) :
    u.b % 2 = 1 → u.c % 2 = 1 → u.a % 2 = 0 → v.b % 2 = 1 → v.c % 2 = 1 → v.a % 2 = 0 →
      pairSign u.b u.c + pairSign v.b v.c = 0 := fun h1 h2 h3 h4 h5 h6 =>
  pairSign_add_eq_zero h1 h2 h4 h5 h3 h6 (by simp only [Vec3.dot] at huv; linarith)

set_option maxHeartbeats 4000000 in
/-- Frame additivity of the sign: on a pairwise orthogonal triple of rays the signs sum to `0`.
The proof is a case analysis over the `2⁹` parity patterns of the nine coordinates: the
non-orthogonal patterns are excluded by the dot products modulo `2`, and in the remaining
patterns the two vectors sharing a weight-two pattern cancel by `pairSign_add_eq_zero`. -/
theorem sgn_frame_sum {u v w : Vec3} (hu : u.IsRay) (hv : v.IsRay) (hw : w.IsRay)
    (huv : u.dot v = 0) (huw : u.dot w = 0) (hvw : v.dot w = 0) :
    sgn u + sgn v + sgn w = 0 := by
  have cuv1 := cancel_ab huv
  have cuv2 := cancel_ac huv
  have cuv3 := cancel_bc huv
  have cuw1 := cancel_ab huw
  have cuw2 := cancel_ac huw
  have cuw3 := cancel_bc huw
  have cvw1 := cancel_ab hvw
  have cvw2 := cancel_ac hvw
  have cvw3 := cancel_bc hvw
  have muva := Int.mul_emod u.a v.a 2
  have muvb := Int.mul_emod u.b v.b 2
  have muvc := Int.mul_emod u.c v.c 2
  have muwa := Int.mul_emod u.a w.a 2
  have muwb := Int.mul_emod u.b w.b 2
  have muwc := Int.mul_emod u.c w.c 2
  have mvwa := Int.mul_emod v.a w.a 2
  have mvwb := Int.mul_emod v.b w.b 2
  have mvwc := Int.mul_emod v.c w.c 2
  simp only [Vec3.IsRay, Int.even_iff] at hu hv hw
  simp only [Vec3.dot] at huv huw hvw
  unfold sgn
  rcases Int.emod_two_eq_zero_or_one u.a with hua | hua <;>
  rcases Int.emod_two_eq_zero_or_one u.b with hub | hub <;>
  rcases Int.emod_two_eq_zero_or_one u.c with huc | huc <;>
  rcases Int.emod_two_eq_zero_or_one v.a with hva | hva <;>
  rcases Int.emod_two_eq_zero_or_one v.b with hvb | hvb <;>
  rcases Int.emod_two_eq_zero_or_one v.c with hvc | hvc <;>
  rcases Int.emod_two_eq_zero_or_one w.a with hwa | hwa <;>
  rcases Int.emod_two_eq_zero_or_one w.b with hwb | hwb <;>
  rcases Int.emod_two_eq_zero_or_one w.c with hwc | hwc <;>
  simp only [hua, hub, huc, hva, hvb, hvc, hwa, hwb, hwc, Int.reduceEq, Int.reduceMul, Int.reduceMod, and_true, and_self, true_implies, false_implies, implies_true, ite_true, ite_false, not_false_eq_true, not_true_eq_false, and_false] at cuv1 cuv2 cuv3 cuw1 cuw2 cuw3 cvw1 cvw2 cvw3 muva muvb muvc muwa muwb muwc mvwa mvwb mvwc hu hv hw ⊢ <;>
  omega

/-- Frame additivity: on a pairwise orthogonal triple of rays the exotic values sum to `1`. -/
theorem exotic_frame_function {u v w : Vec3} (hu : u.IsRay) (hv : v.IsRay) (hw : w.IsRay)
    (huv : u.dot v = 0) (huw : u.dot w = 0) (hvw : v.dot w = 0) :
    exotic u + exotic v + exotic w = 1 := by
  have h := sgn_frame_sum hu hv hw huv huw hvw
  have h' : ((sgn u : ℤ) : ℚ) + (sgn v : ℚ) + (sgn w : ℚ) = 0 := by exact_mod_cast h
  unfold exotic
  linarith

/-! ### Values and ray invariance -/

theorem pairSign_values (x y : ℤ) : pairSign x y = -1 ∨ pairSign x y = 1 := by
  unfold pairSign; split_ifs <;> simp

theorem sgn_values (v : Vec3) : sgn v = -1 ∨ sgn v = 0 ∨ sgn v = 1 := by
  unfold sgn
  split_ifs
  · rcases pairSign_values v.a v.b with h | h <;> simp [h]
  · rcases pairSign_values v.a v.c with h | h <;> simp [h]
  · rcases pairSign_values v.b v.c with h | h <;> simp [h]
  · simp

/-- The exotic function takes the values `0`, `1/3`, `2/3`. -/
theorem exotic_values (v : Vec3) : exotic v = 0 ∨ exotic v = 1 / 3 ∨ exotic v = 2 / 3 := by
  unfold exotic
  rcases sgn_values v with h | h | h <;> rw [h] <;> norm_num

theorem exotic_nonneg (v : Vec3) : 0 ≤ exotic v := by
  rcases exotic_values v with h | h | h <;> rw [h] <;> norm_num

/-- `pairSign` is invariant under an odd common scaling and under negation. -/
theorem pairSign_odd_smul {k : ℤ} (hk : k % 2 = 1) (x y : ℤ) :
    pairSign (k * x) (k * y) = pairSign x y := by
  have e : k * x - k * y = k * (x - y) := by ring
  have hm := Int.mul_emod k (x - y) 4
  have hk4 : k % 4 = 1 ∨ k % 4 = 3 := by omega
  have hxy : (x - y) % 4 = 0 ∨ (x - y) % 4 = 1 ∨ (x - y) % 4 = 2 ∨ (x - y) % 4 = 3 := by omega
  have h : (k * x - k * y) % 4 = 0 ↔ (x - y) % 4 = 0 := by
    rw [e]
    rcases hk4 with hk4 | hk4 <;> rcases hxy with hxy | hxy | hxy | hxy <;>
      simp only [hk4, hxy] at hm <;> omega
  unfold pairSign
  simp only [h]

theorem sgn_odd_smul {k : ℤ} (hk : k % 2 = 1) (v : Vec3) :
    sgn ⟨k * v.a, k * v.b, k * v.c⟩ = sgn v := by
  have ha := mul_emod_two_eq_one k v.a
  have hb := mul_emod_two_eq_one k v.b
  have hc := mul_emod_two_eq_one k v.c
  have ha' : (k * v.a) % 2 = 1 ↔ v.a % 2 = 1 := by rw [ha]; omega
  have hb' : (k * v.b) % 2 = 1 ↔ v.b % 2 = 1 := by rw [hb]; omega
  have hc' : (k * v.c) % 2 = 1 ↔ v.c % 2 = 1 := by rw [hc]; omega
  have ha0 : (k * v.a) % 2 = 0 ↔ v.a % 2 = 0 := by omega
  have hb0 : (k * v.b) % 2 = 0 ↔ v.b % 2 = 0 := by omega
  have hc0 : (k * v.c) % 2 = 0 ↔ v.c % 2 = 0 := by omega
  simp only [sgn, ha', hb', hc', ha0, hb0, hc0, pairSign_odd_smul hk]

/-- `sgn` is invariant under negation. -/
theorem sgn_neg (v : Vec3) : sgn ⟨-v.a, -v.b, -v.c⟩ = sgn v := by
  have h := sgn_odd_smul (k := -1) (by norm_num) v
  simp only [neg_one_mul] at h
  exact h

theorem exotic_odd_smul {k : ℤ} (hk : k % 2 = 1) (v : Vec3) :
    exotic ⟨k * v.a, k * v.b, k * v.c⟩ = exotic v := by
  simp only [exotic, sgn_odd_smul hk]

theorem exotic_neg (v : Vec3) : exotic ⟨-v.a, -v.b, -v.c⟩ = exotic v := by
  simp only [exotic, sgn_neg]

/-! ### Seven explicit rays and the obstruction -/

theorem ray_e1 : (⟨1, 0, 0⟩ : Vec3).IsRay := by simp [Vec3.IsRay]
theorem ray_e2 : (⟨0, 1, 0⟩ : Vec3).IsRay := by simp [Vec3.IsRay]
theorem ray_e3 : (⟨0, 0, 1⟩ : Vec3).IsRay := by simp [Vec3.IsRay]
theorem ray_110 : (⟨1, 1, 0⟩ : Vec3).IsRay := by simp [Vec3.IsRay]
theorem ray_101 : (⟨1, 0, 1⟩ : Vec3).IsRay := by simp [Vec3.IsRay]
theorem ray_011 : (⟨0, 1, 1⟩ : Vec3).IsRay := by simp [Vec3.IsRay]
theorem ray_111 : (⟨1, 1, 1⟩ : Vec3).IsRay := by simp [Vec3.IsRay]

theorem exotic_e1 : exotic ⟨1, 0, 0⟩ = 1 / 3 := by simp [exotic, sgn]
theorem exotic_e2 : exotic ⟨0, 1, 0⟩ = 1 / 3 := by simp [exotic, sgn]
theorem exotic_e3 : exotic ⟨0, 0, 1⟩ = 1 / 3 := by simp [exotic, sgn]
theorem exotic_110 : exotic ⟨1, 1, 0⟩ = 0 := by simp [exotic, sgn, pairSign]
theorem exotic_101 : exotic ⟨1, 0, 1⟩ = 0 := by simp [exotic, sgn, pairSign]
theorem exotic_011 : exotic ⟨0, 1, 1⟩ = 0 := by simp [exotic, sgn, pairSign]
theorem exotic_111 : exotic ⟨1, 1, 1⟩ = 1 / 3 := by simp [exotic, sgn]

/-- No rational symmetric `3 × 3` form agrees with `exotic v · (a² + b² + c²)` on all rays. -/
theorem exotic_not_quadratic :
    ¬ ∃ r00 r11 r22 r01 r02 r12 : ℚ, ∀ v : Vec3, v.IsRay →
      r00 * (v.a : ℚ) ^ 2 + r11 * (v.b : ℚ) ^ 2 + r22 * (v.c : ℚ) ^ 2
        + 2 * r01 * ((v.a : ℚ) * v.b) + 2 * r02 * ((v.a : ℚ) * v.c) + 2 * r12 * ((v.b : ℚ) * v.c)
        = exotic v * ((v.a : ℚ) ^ 2 + (v.b : ℚ) ^ 2 + (v.c : ℚ) ^ 2) := by
  rintro ⟨r00, r11, r22, r01, r02, r12, h⟩
  have h1 := h _ ray_e1
  have h2 := h _ ray_e2
  have h3 := h _ ray_e3
  have h4 := h _ ray_110
  have h5 := h _ ray_101
  have h6 := h _ ray_011
  have h7 := h _ ray_111
  rw [exotic_e1] at h1
  rw [exotic_e2] at h2
  rw [exotic_e3] at h3
  rw [exotic_110] at h4
  rw [exotic_101] at h5
  rw [exotic_011] at h6
  rw [exotic_111] at h7
  norm_num at h1 h2 h3 h4 h5 h6 h7
  linarith

end BornFinite.RationalRays

#print axioms BornFinite.RationalRays.pairSign_add_eq_zero
#print axioms BornFinite.RationalRays.sgn_frame_sum
#print axioms BornFinite.RationalRays.exotic_frame_function
#print axioms BornFinite.RationalRays.exotic_values
#print axioms BornFinite.RationalRays.exotic_nonneg
#print axioms BornFinite.RationalRays.exotic_odd_smul
#print axioms BornFinite.RationalRays.exotic_neg
#print axioms BornFinite.RationalRays.exotic_not_quadratic
