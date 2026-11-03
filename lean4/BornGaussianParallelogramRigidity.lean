import BornGaussianTomographyReduction

/-!
# Parallelogram Rigidity of Zero-Weight Residuals on `ℚ(i)³`

AuthorityEffect: None.

This module closes the algebraic half of the Gleason hinge on `ℚ(i)³`: a zero-weight frame
function `g` that vanishes on the nine tomography rays and satisfies the two-point orthogonal
parallelogram zero-propagation law `SatisfiesOrthoParallelogramZero g` (from
`BornGaussianTomographyReduction`) vanishes on every nonzero vector. No coordinate-sign symmetry
is assumed; this removes the `IsCoordSignSymmetric` hypothesis of
`zero_of_coordSignSymmetric_and_orthoParallelogram`.

## Method

Write `R_u` for the map `v ↦ u + v, u − v` on vectors orthogonal to a zero ray `u`. The law
`g (u + v) + g (u − v) = 0` at a pair of zero rays `(u, v)` says that `g` is odd under the
reflection through `u` inside the plane spanned by `u` and `v`.

* In the coordinate plane `x = 0` there are three zero poles `e₂`, `e₂ + e₃` and `e₂ + i e₃`
  (squared norms `1`, `2`, `2`), each paired with an in-plane orthogonal zero partner of the same
  norm, `e₃`, `e₂ − e₃` and `e₂ − i e₃`; the partners are zero rays by the frame relation with `e₁`. The three reflections are
  `(y, z) ↦ (y, −z)`, `(y, z) ↦ (z, y)` and `(y, z) ↦ (z, −y)` on rays; their composite is
  the identity on rays, so `g = −g` on the plane (`plane_x_zero_of_orthoParallelogram`).
* The other two coordinate planes follow by composing `g` with a coordinate permutation, which
  preserves frames, orthogonality, vector addition and the nine tomography rays
  (`zeroWeight_comp_perm`, `orthoParallelogramZero_comp_perm`).
* Off the coordinate planes, the three reflections through `e₁`, `e₂`, `e₃` are
  `(x, y, z) ↦ (x, −y, −z)`, `(−x, y, −z)`, `(−x, −y, z)`, whose composite is again the
  identity on rays (`zero_of_orthoParallelogramZero_and_vanishesOnNineRays`).

Only the following instances of the parallelogram law are used: pairs `(u, v)` of zero rays with
`u` a scalar multiple of a coordinate axis or of one of the six in-plane tomography rays. So the
analytic half of the hinge only needs to supply the law at those pairs.

## Main Results

* `plane_x_zero_of_orthoParallelogram`: vanishing on the plane `x = 0` from the five rays
  `e₁, e₂, e₃, e₂ + e₃, e₂ + i e₃`.
* `zero_of_orthoParallelogramZero_and_vanishesOnNineRays`: every zero-weight frame function on
  `ℚ(i)³` that vanishes on the nine tomography rays and satisfies
  `SatisfiesOrthoParallelogramZero` vanishes on all nonzero vectors.
* `signed_rigidity_of_orthoParallelogramZero_residual`: a frame function whose residual
  `f - quadRay (tomographyForm f)` satisfies `SatisfiesOrthoParallelogramZero` equals
  `quadRay (tomographyForm f)` on every nonzero vector. No sign condition is assumed, so a
  nonnegative frame function is covered as a special case; there is no separate nonnegative export.
-/

namespace BornFinite.GaussianTomography

open BornFinite
open BornFinite.GaussRat
open BornFinite.GaussianFrames

/-! ### 1. Reflection form of the zero-pair parallelogram law -/

/-- At a pair of orthogonal zero rays, `g (u + v) = − g (u − v)`. -/
theorem orthoParallelogramZero_add_eq_neg_sub {g : GVec → ℚ}
    (hpara : SatisfiesOrthoParallelogramZero g) {u v : GVec}
    (huv : GVec.inner u v = 0) (hu : g u = 0) (hv : g v = 0) :
    g (GVec.add u v) = - g (GVec.sub u v) := by
  have := hpara u v huv hu hv
  linarith

/-! ### 2. Vanishing on the coordinate plane `x = 0` -/

/-- The in-plane partners of `e₂ + e₃` and `e₂ + i e₃` are zero rays by the frame relation
with `e₁`. -/
theorem zero_on_plane_partners {g : GVec → ℚ} (hg : IsZeroWeightFrameFunction g)
    (h1 : g tomo_e1 = 0) (h23 : g tomo_e23 = 0) (h23i : g tomo_e23i = 0) :
    g ⟨0, 1, -1⟩ = 0 ∧ g ⟨0, 1, -I⟩ = 0 := by
  have hfr1 : IsFrame tomo_e1 tomo_e23 ⟨0, 1, -1⟩ :=
    ⟨tomo_e1_nonZero, tomo_e23_nonZero, nonZero_of_y (by norm_num),
     by simp only [tomo_e1, tomo_e23]; gauss_arith,
     by simp only [tomo_e1]; gauss_arith,
     by simp only [tomo_e23]; gauss_arith⟩
  have hfr2 : IsFrame tomo_e1 tomo_e23i ⟨0, 1, -I⟩ :=
    ⟨tomo_e1_nonZero, tomo_e23i_nonZero, nonZero_of_y (by norm_num),
     by simp only [tomo_e1, tomo_e23i]; gauss_arith,
     by simp only [tomo_e1]; gauss_arith,
     by simp only [tomo_e23i]; ext <;> simp [GVec.inner, gv, I]⟩
  have e1 := hg _ _ _ hfr1
  have e2 := hg _ _ _ hfr2
  constructor <;> linarith

theorem tomo_e2_eq : tomo_e2 = ⟨0, 1, 0⟩ := by ext <;> simp [tomo_e2, gv]
theorem tomo_e3_eq : tomo_e3 = ⟨0, 0, 1⟩ := by ext <;> simp [tomo_e3, gv]
theorem tomo_e23_eq : tomo_e23 = ⟨0, 1, 1⟩ := by ext <;> simp [tomo_e23, gv]
theorem tomo_e23i_eq : tomo_e23i = ⟨0, 1, I⟩ := by ext <;> simp [tomo_e23i, gv, I]

/-- Every nonzero vector on the plane `x = 0` is a zero of `g`, given the zero-pair
parallelogram law and vanishing on `e₁, e₂, e₃, e₂ + e₃, e₂ + i e₃`. -/
theorem plane_x_zero_of_orthoParallelogram {g : GVec → ℚ}
    (hg : IsZeroWeightFrameFunction g) (hpara : SatisfiesOrthoParallelogramZero g)
    (h1 : g tomo_e1 = 0) (h2 : g tomo_e2 = 0) (h3 : g tomo_e3 = 0)
    (h23 : g tomo_e23 = 0) (h23i : g tomo_e23i = 0) :
    ∀ y z : GaussRat, (y ≠ 0 ∨ z ≠ 0) → g ⟨0, y, z⟩ = 0 := by
  obtain ⟨hm, hmi⟩ := zero_on_plane_partners hg h1 h23 h23i
  rw [tomo_e2_eq] at h2
  rw [tomo_e3_eq] at h3
  rw [tomo_e23_eq] at h23
  rw [tomo_e23i_eq] at h23i
  -- scalar multiples of the six in-plane zero rays
  have hsc : ∀ (w : GVec), w.NonZero → g w = 0 → ∀ l : GaussRat, l ≠ 0 →
      g (GVec.smul l w) = 0 := by
    intro w hw hgw l hl
    rw [zeroWeight_smul hg hw hl, hgw]
  have hy0 : ∀ y : GaussRat, y ≠ 0 → g ⟨0, y, 0⟩ = 0 := by
    intro y hy
    have := hsc ⟨0, 1, 0⟩ (nonZero_of_y (by norm_num)) h2 y hy
    simpa [GVec.smul] using this
  have hz0 : ∀ z : GaussRat, z ≠ 0 → g ⟨0, 0, z⟩ = 0 := by
    intro z hz
    have := hsc ⟨0, 0, 1⟩ (nonZero_of_z (by norm_num)) h3 z hz
    simpa [GVec.smul] using this
  have hI : (I : GaussRat) ≠ 0 := by
    intro h; have := congrArg GaussRat.im h; simp at this
  have hnegI : (-I : GaussRat) ≠ 0 := neg_ne_zero.mpr hI
  have h2ne : (2 : GaussRat) ≠ 0 := by
    intro h; have := congrArg GaussRat.re h; norm_num at this
  have hneg2I : (-2 * I : GaussRat) ≠ 0 := mul_ne_zero (neg_ne_zero.mpr h2ne) hI
  -- the ray (0, i, 1) = i (0, 1, −i)
  have hi1 : g ⟨0, I, 1⟩ = 0 := by
    have := hsc ⟨0, 1, -I⟩ (nonZero_of_y (by norm_num)) hmi I hI
    have heq : GVec.smul I ⟨0, 1, -I⟩ = ⟨0, I, 1⟩ := by
      ext <;> simp [GVec.smul, I]
    rwa [heq] at this
  -- (P1) reflection through e₂: g(0, y, z) + g(0, y, −z) = 0
  have P1 : ∀ y z : GaussRat, y ≠ 0 → z ≠ 0 → g ⟨0, y, z⟩ + g ⟨0, y, -z⟩ = 0 := by
    intro y z hy hz
    have horth : GVec.inner ⟨0, y, 0⟩ ⟨0, 0, z⟩ = 0 := by simp [GVec.inner]
    have := hpara ⟨0, y, 0⟩ ⟨0, 0, z⟩ horth (hy0 y hy) (hz0 z hz)
    have hadd : GVec.add ⟨0, y, 0⟩ ⟨0, 0, z⟩ = ⟨0, y, z⟩ := by ext <;> simp [GVec.add]
    have hsub : GVec.sub ⟨0, y, 0⟩ ⟨0, 0, z⟩ = ⟨0, y, -z⟩ := by ext <;> simp [GVec.sub]
    rwa [hadd, hsub] at this
  -- (P2) reflection through e₂ + e₃: g(0, y, z) + g(0, z, y) = 0
  have P2 : ∀ y z : GaussRat, y + z ≠ 0 → y - z ≠ 0 → g ⟨0, y, z⟩ + g ⟨0, z, y⟩ = 0 := by
    intro y z hp hm'
    have hyz : y ≠ 0 ∨ z ≠ 0 := by
      by_contra hcon
      have hc := not_or.mp hcon
      exact hp (by rw [not_not.mp hc.1, not_not.mp hc.2]; ring)
    have hu : g (GVec.smul (y + z) ⟨0, 1, 1⟩) = 0 :=
      hsc ⟨0, 1, 1⟩ (nonZero_of_y (by norm_num)) h23 (y + z) hp
    have hv : g (GVec.smul (z - y) ⟨0, -1, 1⟩) = 0 := by
      have hzy : z - y ≠ 0 := fun h => hm' (by linear_combination -h)
      have := hsc ⟨0, 1, -1⟩ (nonZero_of_y (by norm_num)) hm (y - z) hm'
      have heq : GVec.smul (y - z) ⟨0, 1, -1⟩ = GVec.smul (z - y) ⟨0, -1, 1⟩ := by
        ext <;> simp [GVec.smul]
      rwa [heq] at this
    have horth : GVec.inner (GVec.smul (y + z) ⟨0, 1, 1⟩) (GVec.smul (z - y) ⟨0, -1, 1⟩) = 0 := by
      ext <;> simp [GVec.inner, GVec.smul] <;> ring
    have := hpara _ _ horth hu hv
    have hadd : GVec.add (GVec.smul (y + z) ⟨0, 1, 1⟩) (GVec.smul (z - y) ⟨0, -1, 1⟩)
        = GVec.smul 2 ⟨0, y, z⟩ := by
      ext <;> simp [GVec.add, GVec.smul] <;> ring
    have hsub : GVec.sub (GVec.smul (y + z) ⟨0, 1, 1⟩) (GVec.smul (z - y) ⟨0, -1, 1⟩)
        = GVec.smul 2 ⟨0, z, y⟩ := by
      ext <;> simp [GVec.sub, GVec.smul] <;> ring
    rw [hadd, hsub] at this
    have hnz1 : (⟨0, y, z⟩ : GVec).NonZero := by
      rcases hyz with h | h
      · exact Or.inr (Or.inl h)
      · exact Or.inr (Or.inr h)
    have hnz2 : (⟨0, z, y⟩ : GVec).NonZero := by
      rcases hyz with h | h
      · exact Or.inr (Or.inr h)
      · exact Or.inr (Or.inl h)
    rwa [zeroWeight_smul hg hnz1 h2ne, zeroWeight_smul hg hnz2 h2ne] at this
  -- (P3) reflection through e₂ + i e₃: g(0, y, z) + g(0, z, −y) = 0
  have P3 : ∀ y z : GaussRat, y - I * z ≠ 0 → z - I * y ≠ 0 →
      g ⟨0, y, z⟩ + g ⟨0, z, -y⟩ = 0 := by
    intro y z ha hb
    have hyz : y ≠ 0 ∨ z ≠ 0 := by
      by_contra hcon
      have hc := not_or.mp hcon
      exact ha (by rw [not_not.mp hc.1, not_not.mp hc.2]; ring)
    have hu : g (GVec.smul (y - I * z) ⟨0, 1, I⟩) = 0 :=
      hsc ⟨0, 1, I⟩ (nonZero_of_y (by norm_num)) h23i (y - I * z) ha
    have hv : g (GVec.smul (z - I * y) ⟨0, I, 1⟩) = 0 :=
      hsc ⟨0, I, 1⟩ (nonZero_of_z (by norm_num)) hi1 (z - I * y) hb
    have horth : GVec.inner (GVec.smul (y - I * z) ⟨0, 1, I⟩)
        (GVec.smul (z - I * y) ⟨0, I, 1⟩) = 0 := by
      ext <;> simp [GVec.inner, GVec.smul, I] <;> ring
    have := hpara _ _ horth hu hv
    have hadd : GVec.add (GVec.smul (y - I * z) ⟨0, 1, I⟩) (GVec.smul (z - I * y) ⟨0, I, 1⟩)
        = GVec.smul 2 ⟨0, y, z⟩ := by
      ext <;> simp [GVec.add, GVec.smul, I] <;> ring
    have hsub : GVec.sub (GVec.smul (y - I * z) ⟨0, 1, I⟩) (GVec.smul (z - I * y) ⟨0, I, 1⟩)
        = GVec.smul (-2 * I) ⟨0, z, -y⟩ := by
      ext <;> simp [GVec.sub, GVec.smul, I] <;> ring
    rw [hadd, hsub] at this
    have hnz1 : (⟨0, y, z⟩ : GVec).NonZero := by
      rcases hyz with h | h
      · exact Or.inr (Or.inl h)
      · exact Or.inr (Or.inr h)
    have hnz2 : (⟨0, z, -y⟩ : GVec).NonZero := by
      rcases hyz with h | h
      · exact Or.inr (Or.inr (neg_ne_zero.mpr h))
      · exact Or.inr (Or.inl h)
    rwa [zeroWeight_smul hg hnz1 h2ne, zeroWeight_smul hg hnz2 hneg2I] at this
  -- main argument
  intro y z hyz
  by_cases hy : y = 0
  · subst hy
    exact hz0 z (hyz.resolve_left (by simp))
  by_cases hz : z = 0
  · subst hz
    exact hy0 y hy
  -- degenerate directions z = u y for a unit u are scalar multiples of zero rays
  by_cases hd1 : y + z = 0
  · have hz' : z = -y := by linear_combination hd1
    subst hz'
    have := hsc ⟨0, 1, -1⟩ (nonZero_of_y (by norm_num)) hm y hy
    simpa [GVec.smul] using this
  by_cases hd2 : y - z = 0
  · have hz' : z = y := by linear_combination -hd2
    rw [hz']
    have := hsc ⟨0, 1, 1⟩ (nonZero_of_y (by norm_num)) h23 y hy
    simpa [GVec.smul] using this
  by_cases hd3 : y + I * z = 0
  · have hz' : z = y * I := by
      have hI2 : I * I = -1 := I_mul_I
      linear_combination (-I) * hd3 + z * hI2
    subst hz'
    have := hsc ⟨0, 1, I⟩ (nonZero_of_y (by norm_num)) h23i y hy
    simpa [GVec.smul] using this
  by_cases hd4 : z + I * y = 0
  · have hz' : z = -(y * I) := by linear_combination hd4
    subst hz'
    have := hsc ⟨0, 1, -I⟩ (nonZero_of_y (by norm_num)) hmi y hy
    simpa [GVec.smul] using this
  -- generic case: compose the three reflections
  have s1 := P1 y z hy hz
  have s2 := P2 y (-z) (by intro h; exact hd2 (by linear_combination h))
    (by intro h; exact hd1 (by linear_combination h))
  have s3 := P3 (-z) y (by intro h; exact hd4 (by linear_combination -h))
    (by intro h; exact hd3 (by linear_combination h))
  have hnn : (⟨0, y, -(-z)⟩ : GVec) = ⟨0, y, z⟩ := by ext <;> simp
  rw [hnn] at s3
  linarith

/-! ### 3. Transport to the other coordinate planes by coordinate permutations -/

/-- Zero-weight frame functions are preserved by composition with a map that preserves
nonzeroness and inner products. -/
theorem zeroWeight_comp_perm {g : GVec → ℚ} (hg : IsZeroWeightFrameFunction g)
    (σ : GVec → GVec) (hnz : ∀ v : GVec, v.NonZero → (σ v).NonZero)
    (hinner : ∀ u v : GVec, GVec.inner (σ u) (σ v) = GVec.inner u v) :
    IsZeroWeightFrameFunction (fun v => g (σ v)) := by
  intro u v w ⟨hu, hv, hw, huv, huw, hvw⟩
  exact hg (σ u) (σ v) (σ w)
    ⟨hnz u hu, hnz v hv, hnz w hw, by rw [hinner, huv], by rw [hinner, huw], by rw [hinner, hvw]⟩

/-- The zero-pair parallelogram law is preserved by composition with a map that preserves inner
products, addition and subtraction. -/
theorem orthoParallelogramZero_comp_perm {g : GVec → ℚ} (hpara : SatisfiesOrthoParallelogramZero g)
    (σ : GVec → GVec)
    (hinner : ∀ u v : GVec, GVec.inner (σ u) (σ v) = GVec.inner u v)
    (hadd : ∀ u v : GVec, σ (GVec.add u v) = GVec.add (σ u) (σ v))
    (hsub : ∀ u v : GVec, σ (GVec.sub u v) = GVec.sub (σ u) (σ v)) :
    SatisfiesOrthoParallelogramZero (fun v => g (σ v)) := by
  intro u v huv hu hv
  have := hpara (σ u) (σ v) (by rw [hinner, huv]) hu hv
  simpa [hadd, hsub] using this

/-- Swap of the first two coordinates. -/
def swapXY (v : GVec) : GVec := ⟨v.y, v.x, v.z⟩

/-- Cyclic shift `(x, y, z) ↦ (y, z, x)`. -/
def cycXYZ (v : GVec) : GVec := ⟨v.y, v.z, v.x⟩

theorem swapXY_nonZero {v : GVec} (hv : v.NonZero) : (swapXY v).NonZero := by
  rcases hv with h | h | h
  · exact Or.inr (Or.inl h)
  · exact Or.inl h
  · exact Or.inr (Or.inr h)

theorem cycXYZ_nonZero {v : GVec} (hv : v.NonZero) : (cycXYZ v).NonZero := by
  rcases hv with h | h | h
  · exact Or.inr (Or.inr h)
  · exact Or.inl h
  · exact Or.inr (Or.inl h)

theorem swapXY_inner (u v : GVec) : GVec.inner (swapXY u) (swapXY v) = GVec.inner u v := by
  simp only [GVec.inner, swapXY]; ring

theorem cycXYZ_inner (u v : GVec) : GVec.inner (cycXYZ u) (cycXYZ v) = GVec.inner u v := by
  simp only [GVec.inner, cycXYZ]; ring

theorem swapXY_add (u v : GVec) : swapXY (GVec.add u v) = GVec.add (swapXY u) (swapXY v) := by
  ext <;> simp [swapXY, GVec.add]

theorem swapXY_sub (u v : GVec) : swapXY (GVec.sub u v) = GVec.sub (swapXY u) (swapXY v) := by
  ext <;> simp [swapXY, GVec.sub]

theorem cycXYZ_add (u v : GVec) : cycXYZ (GVec.add u v) = GVec.add (cycXYZ u) (cycXYZ v) := by
  ext <;> simp [cycXYZ, GVec.add]

theorem cycXYZ_sub (u v : GVec) : cycXYZ (GVec.sub u v) = GVec.sub (cycXYZ u) (cycXYZ v) := by
  ext <;> simp [cycXYZ, GVec.sub]

/-- Vanishing on the plane `y = 0`. -/
theorem plane_y_zero_of_orthoParallelogram {g : GVec → ℚ}
    (hg : IsZeroWeightFrameFunction g) (hpara : SatisfiesOrthoParallelogramZero g)
    (h9 : VanishesOnNineRays g) :
    ∀ x z : GaussRat, (x ≠ 0 ∨ z ≠ 0) → g ⟨x, 0, z⟩ = 0 := by
  obtain ⟨h1, h2, h3, _, h13, _, _, h13i, _⟩ := h9
  have hg' := zeroWeight_comp_perm hg swapXY (fun _ hv => swapXY_nonZero hv) swapXY_inner
  have hp' := orthoParallelogramZero_comp_perm hpara swapXY swapXY_inner swapXY_add swapXY_sub
  have e1 : swapXY tomo_e1 = tomo_e2 := by ext <;> simp [swapXY, tomo_e1, tomo_e2, gv]
  have e2 : swapXY tomo_e2 = tomo_e1 := by ext <;> simp [swapXY, tomo_e1, tomo_e2, gv]
  have e3 : swapXY tomo_e3 = tomo_e3 := by ext <;> simp [swapXY, tomo_e3, gv]
  have e23 : swapXY tomo_e23 = tomo_e13 := by ext <;> simp [swapXY, tomo_e23, tomo_e13, gv]
  have e23i : swapXY tomo_e23i = tomo_e13i := by
    ext <;> simp [swapXY, tomo_e23i, tomo_e13i, gv]
  have hplane := plane_x_zero_of_orthoParallelogram hg' hp'
    (by show g (swapXY tomo_e1) = 0; rw [e1, h2])
    (by show g (swapXY tomo_e2) = 0; rw [e2, h1])
    (by show g (swapXY tomo_e3) = 0; rw [e3, h3])
    (by show g (swapXY tomo_e23) = 0; rw [e23, h13])
    (by show g (swapXY tomo_e23i) = 0; rw [e23i, h13i])
  intro x z hxz
  have := hplane x z hxz
  simpa [swapXY] using this

/-- Vanishing on the plane `z = 0`. -/
theorem plane_z_zero_of_orthoParallelogram {g : GVec → ℚ}
    (hg : IsZeroWeightFrameFunction g) (hpara : SatisfiesOrthoParallelogramZero g)
    (h9 : VanishesOnNineRays g) :
    ∀ x y : GaussRat, (x ≠ 0 ∨ y ≠ 0) → g ⟨x, y, 0⟩ = 0 := by
  obtain ⟨h1, h2, h3, h12, _, _, h12i, _, _⟩ := h9
  have hg' := zeroWeight_comp_perm hg cycXYZ (fun _ hv => cycXYZ_nonZero hv) cycXYZ_inner
  have hp' := orthoParallelogramZero_comp_perm hpara cycXYZ cycXYZ_inner cycXYZ_add cycXYZ_sub
  have e1 : cycXYZ tomo_e1 = tomo_e3 := by ext <;> simp [cycXYZ, tomo_e1, tomo_e3, gv]
  have e2 : cycXYZ tomo_e2 = tomo_e1 := by ext <;> simp [cycXYZ, tomo_e1, tomo_e2, gv]
  have e3 : cycXYZ tomo_e3 = tomo_e2 := by ext <;> simp [cycXYZ, tomo_e3, tomo_e2, gv]
  have e23 : cycXYZ tomo_e23 = tomo_e12 := by ext <;> simp [cycXYZ, tomo_e23, tomo_e12, gv]
  have e23i : cycXYZ tomo_e23i = tomo_e12i := by
    ext <;> simp [cycXYZ, tomo_e23i, tomo_e12i, gv]
  have hplane := plane_x_zero_of_orthoParallelogram hg' hp'
    (by show g (cycXYZ tomo_e1) = 0; rw [e1, h3])
    (by show g (cycXYZ tomo_e2) = 0; rw [e2, h1])
    (by show g (cycXYZ tomo_e3) = 0; rw [e3, h2])
    (by show g (cycXYZ tomo_e23) = 0; rw [e23, h12])
    (by show g (cycXYZ tomo_e23i) = 0; rw [e23i, h12i])
  intro x y hxy
  have := hplane x y hxy
  simpa [cycXYZ] using this

/-! ### 4. Vanishing on all of `ℚ(i)³` -/

/-- **Parallelogram rigidity.** A zero-weight frame function on `ℚ(i)³` that vanishes on the nine
tomography rays and satisfies the two-point orthogonal parallelogram zero-propagation law vanishes
on every nonzero vector. No coordinate-sign symmetry is assumed. -/
theorem zero_of_orthoParallelogramZero_and_vanishesOnNineRays {g : GVec → ℚ}
    (hg : IsZeroWeightFrameFunction g) (hpara : SatisfiesOrthoParallelogramZero g)
    (h9 : VanishesOnNineRays g) :
    ∀ v : GVec, v.NonZero → g v = 0 := by
  have hX := plane_x_zero_of_orthoParallelogram hg hpara h9.1 h9.2.1 h9.2.2.1
    h9.2.2.2.2.2.1 h9.2.2.2.2.2.2.2.2
  have hY := plane_y_zero_of_orthoParallelogram hg hpara h9
  have hZ := plane_z_zero_of_orthoParallelogram hg hpara h9
  have hax : ∀ x : GaussRat, x ≠ 0 → g ⟨x, 0, 0⟩ = 0 := by
    intro x hx
    have := zeroWeight_smul hg tomo_e1_nonZero hx
    have heq : GVec.smul x tomo_e1 = ⟨x, 0, 0⟩ := by ext <;> simp [GVec.smul, tomo_e1, gv]
    rw [heq, h9.1] at this
    exact this
  have hay : ∀ y : GaussRat, y ≠ 0 → g ⟨0, y, 0⟩ = 0 := by
    intro y hy
    have := zeroWeight_smul hg tomo_e2_nonZero hy
    have heq : GVec.smul y tomo_e2 = ⟨0, y, 0⟩ := by ext <;> simp [GVec.smul, tomo_e2, gv]
    rw [heq, h9.2.1] at this
    exact this
  have haz : ∀ z : GaussRat, z ≠ 0 → g ⟨0, 0, z⟩ = 0 := by
    intro z hz
    have := zeroWeight_smul hg tomo_e3_nonZero hz
    have heq : GVec.smul z tomo_e3 = ⟨0, 0, z⟩ := by ext <;> simp [GVec.smul, tomo_e3, gv]
    rw [heq, h9.2.2.1] at this
    exact this
  intro ⟨x, y, z⟩ hv
  by_cases hx : x = 0
  · subst hx
    apply hX y z
    rcases hv with h | h | h
    · exact absurd rfl h
    · exact Or.inl h
    · exact Or.inr h
  by_cases hy : y = 0
  · subst hy
    exact hY x z (Or.inl hx)
  by_cases hz : z = 0
  · subst hz
    exact hZ x y (Or.inl hx)
  -- (Q2) reflection through e₂: g(x, y, z) + g(−x, y, −z) = 0
  have q2 : g ⟨x, y, z⟩ + g ⟨-x, y, -z⟩ = 0 := by
    have horth : GVec.inner ⟨0, y, 0⟩ ⟨x, 0, z⟩ = 0 := by simp [GVec.inner]
    have := hpara ⟨0, y, 0⟩ ⟨x, 0, z⟩ horth (hay y hy) (hY x z (Or.inl hx))
    have hadd : GVec.add ⟨0, y, 0⟩ ⟨x, 0, z⟩ = ⟨x, y, z⟩ := by ext <;> simp [GVec.add]
    have hsub : GVec.sub ⟨0, y, 0⟩ ⟨x, 0, z⟩ = ⟨-x, y, -z⟩ := by ext <;> simp [GVec.sub]
    rwa [hadd, hsub] at this
  -- (Q1) reflection through e₁ at (−x, y, −z): g(−x, y, −z) + g(−x, −y, z) = 0
  have q1 : g ⟨-x, y, -z⟩ + g ⟨-x, -y, z⟩ = 0 := by
    have horth : GVec.inner ⟨-x, 0, 0⟩ ⟨0, y, -z⟩ = 0 := by simp [GVec.inner]
    have := hpara ⟨-x, 0, 0⟩ ⟨0, y, -z⟩ horth (hax (-x) (neg_ne_zero.mpr hx))
      (hX y (-z) (Or.inl hy))
    have hadd : GVec.add ⟨-x, 0, 0⟩ ⟨0, y, -z⟩ = ⟨-x, y, -z⟩ := by ext <;> simp [GVec.add]
    have hsub : GVec.sub ⟨-x, 0, 0⟩ ⟨0, y, -z⟩ = ⟨-x, -y, z⟩ := by ext <;> simp [GVec.sub]
    rwa [hadd, hsub] at this
  -- (Q3) reflection through e₃: g(x, y, z) + g(−x, −y, z) = 0
  have q3 : g ⟨x, y, z⟩ + g ⟨-x, -y, z⟩ = 0 := by
    have horth : GVec.inner ⟨0, 0, z⟩ ⟨x, y, 0⟩ = 0 := by simp [GVec.inner]
    have := hpara ⟨0, 0, z⟩ ⟨x, y, 0⟩ horth (haz z hz) (hZ x y (Or.inl hx))
    have hadd : GVec.add ⟨0, 0, z⟩ ⟨x, y, 0⟩ = ⟨x, y, z⟩ := by ext <;> simp [GVec.add]
    have hsub : GVec.sub ⟨0, 0, z⟩ ⟨x, y, 0⟩ = ⟨-x, -y, z⟩ := by ext <;> simp [GVec.sub]
    rwa [hadd, hsub] at this
  linarith

/-! ### 5. Consequences for quadratic rigidity -/

/-- Signed quadratic rigidity holds for every frame function whose tomography residual satisfies
the zero-pair parallelogram law. -/
theorem signed_rigidity_of_orthoParallelogramZero_residual {f : GVec → ℚ}
    (hf : IsFrameFunction f) (hpara : SatisfiesOrthoParallelogramZero (residual f)) :
    ∀ v : GVec, v.NonZero → f v = quadRay (tomographyForm f) v := by
  intro v hv
  have hz := zero_of_orthoParallelogramZero_and_vanishesOnNineRays
    (residual_is_zero_weight hf) hpara (residual_vanishes_on_nine_rays f) v hv
  unfold residual at hz
  linarith

end BornFinite.GaussianTomography

#print axioms BornFinite.GaussianTomography.orthoParallelogramZero_add_eq_neg_sub
#print axioms BornFinite.GaussianTomography.zero_on_plane_partners
#print axioms BornFinite.GaussianTomography.plane_x_zero_of_orthoParallelogram
#print axioms BornFinite.GaussianTomography.zeroWeight_comp_perm
#print axioms BornFinite.GaussianTomography.orthoParallelogramZero_comp_perm
#print axioms BornFinite.GaussianTomography.plane_y_zero_of_orthoParallelogram
#print axioms BornFinite.GaussianTomography.plane_z_zero_of_orthoParallelogram
#print axioms BornFinite.GaussianTomography.zero_of_orthoParallelogramZero_and_vanishesOnNineRays
#print axioms BornFinite.GaussianTomography.signed_rigidity_of_orthoParallelogramZero_residual
