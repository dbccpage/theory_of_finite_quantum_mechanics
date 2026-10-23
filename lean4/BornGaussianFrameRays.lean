import BornGaussianRationalFrameObstruction

/-!
# Frame functions on `ℚ(i)³` are functions of rays

AuthorityEffect: None.

Every nonzero `v ∈ K³` completes to an orthogonal frame `(v, w, u)` in which `w, u` do not depend
on rescaling `v` (`exists_frame_completion`).  Hence any frame function on vectors satisfies
`f (l • v) = f v` for `l ≠ 0` (`frameFunction_smul`): the vector-level definition
`IsFrameFunction` in `BornGaussianRationalFrameObstruction` is a function on rays.
-/

namespace BornFable.GaussianFrames

open BornFable

theorem inner_smul_left (l : GaussRat) (u v : GVec) :
    (GVec.smul l u).inner v = star l * u.inner v := by
  simp only [GVec.inner, GVec.smul, star_mul]
  ring

theorem nonZero_smul {l
: GaussRat} (hl : l ≠ 0) {v : GVec} (hv : v.NonZero) :
    (GVec.smul l v).NonZero := by
  rcases hv with h | h | h
  · exact Or.inl (mul_ne_zero hl h)
  · exact Or.inr (Or.inl (mul_ne_zero hl h))
  · exact Or.inr (Or.inr (mul_ne_zero hl h))

/-- Every nonzero vector completes to a frame `(v, w, u)`, with the same `w, u` working for every
nonzero rescaling of `v`. -/
theorem exists_frame_completion {v : GVec} (hv : v.NonZero) :
    ∃ w u : GVec, IsFrame v w u ∧ ∀ l : GaussRat, l ≠ 0 → IsFrame (GVec.smul l v) w u := by
  by_cases hxy : v.x = 0 ∧ v.y = 0
  · obtain ⟨hx, hy⟩ := hxy
    have e1 : GVec.NonZero ⟨1, 0, 0⟩ := Or.inl one_ne_zero
    have e2 : GVec.NonZero ⟨0, 1, 0⟩ := Or.inr (Or.inl one_ne_zero)
    have i1 : v.inner ⟨1, 0, 0⟩ = 0 := by simp [GVec.inner, hx]
    have i2 : v.inner ⟨0, 1, 0⟩ = 0 := by simp [GVec.inner, hy]
    have i3 : GVec.inner ⟨1, 0, 0⟩ ⟨0, 1, 0⟩ = 0 := by simp [GVec.inner]
    refine ⟨⟨1, 0, 0⟩, ⟨0, 1, 0⟩, ⟨hv, e1, e2, i1, i2, i3⟩, ?_⟩
    intro l hl
    refine ⟨nonZero_smul hl hv, e1, e2, ?_, ?_, i3⟩
    · rw [inner_smul_left, i1, mul_zero]
    · rw [inner_smul_left, i2, mul_zero]
  · have hpos : 0 < GaussRat.normSq v.x + GaussRat.normSq v.y := by
      rcases not_and_or.mp hxy with hx | hy
      · have h1 : 0 < GaussRat.normSq v.x :=
          lt_of_le_of_ne (GaussRat.normSq_nonneg _)
            (fun h => hx ((GaussRat.normSq_eq_zero_iff _).mp h.symm))
        linarith [GaussRat.normSq_nonneg v.y]
      · have h1 : 0 < GaussRat.normSq v.y :=
          lt_of_le_of_ne (GaussRat.normSq_nonneg _)
            (fun h => hy ((GaussRat.normSq_eq_zero_iff _).mp h.symm))
        linarith [GaussRat.normSq_nonneg v.x]
    have hw : GVec.NonZero ⟨-star v.y, star v.x, 0⟩ := by
      rcases not_and_or.mp hxy with hx | hy
      · exact Or.inr (Or.inl (fun h => hx (star_eq_zero.mp h)))
      · exact Or.inl (fun h => hy (star_eq_zero.mp (neg_eq_zero.mp h)))
    have hz : (star v.x * v.x + star v.y * v.y).re ≠ 0 := by
      rw [GaussRat.re_add, GaussRat.re_star_mul_self, GaussRat.re_star_mul_self]
      exact hpos.ne'
    have hu : GVec.NonZero
        ⟨-(v.x * star v.z), -(v.y * star v.z), star v.x * v.x + star v.y * v.y⟩ :=
      nonZero_of_z hz
    have i1 : v.inner ⟨-star v.y, star v.x, 0⟩ = 0 := by
      simp only [GVec.inner]
      ring
    have i2 : v.inner
        ⟨-(v.x * star v.z), -(v.y * star v.z), star v.x * v.x + star v.y * v.y⟩ = 0 := by
      simp only [GVec.inner]
      ring
    have i3 : GVec.inner ⟨-star v.y, star v.x, 0⟩
        ⟨-(v.x * star v.z), -(v.y * star v.z), star v.x * v.x + star v.y * v.y⟩ = 0 := by
      simp only [GVec.inner, star_neg, star_star, star_zero]
      ring
    refine ⟨⟨-star v.y, star v.x, 0⟩,
      ⟨-(v.x * star v.z), -(v.y * star v.z), star v.x * v.x + star v.y * v.y⟩,
      ⟨hv, hw, hu, i1, i2, i3⟩, ?_⟩
    intro l hl
    refine ⟨nonZero_smul hl hv, hw, hu, ?_, ?_, i3⟩
    · rw [inner_smul_left, i1, mul_zero]
    · rw [inner_smul_left, i2, mul_zero]

/-- A frame function on vectors is constant on rays. -/
theorem frameFunction_smul {f : GVec → ℚ} (hF : IsFrameFunction f) {v : GVec} (hv : v.NonZero)
    {l : GaussRat} (hl : l ≠ 0) : f (GVec.smul l v) = f v := by
  obtain ⟨w, u, h1, h2⟩ := exists_frame_completion hv
  have e1 := hF _ _ _ h1
  have e2 := hF _ _ _ (h2 l hl)
  linarith

end BornFable.GaussianFrames

#print axioms BornFable.GaussianFrames.inner_smul_left
#print axioms BornFable.GaussianFrames.nonZero_smul
#print axioms BornFable.GaussianFrames.exists_frame_completion
#print axioms BornFable.GaussianFrames.frameFunction_smul
