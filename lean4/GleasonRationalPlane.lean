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
