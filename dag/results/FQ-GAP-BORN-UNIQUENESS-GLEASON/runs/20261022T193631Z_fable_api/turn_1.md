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
```

## 3. WHAT IS PROVED

**Not proved:** neither (A) nor (B). No frame function on *all* Gaussian‑rational rays is constructed, and no uniqueness theorem over `ℚ(i)³` is proved. The question remains open; the files below give the largest honest pieces.

**File `BornRationalPlaneObstruction.lean` (over ℚ, all rational rays, new relative to the repository):**
- `exotic_frame_function`: for any three integer vectors `u, v, w ∈ ℤ³`, each with not all coordinates even (`IsPrimitive`) and pairwise orthogonal for the integer dot product, `exotic u + exotic v + exotic w = 1`. No square‑norm hypothesis.
- `exotic_not_quadratic`: there is no rational symmetric form `(r_ij)` with `Q(v) = exotic v · (a²+b²+c²)` for all odd‑primitive `v`.
- `exotic_three_valued`: `exotic v ∈ {0, 1/3, 2/3}`.
- `sgn_eq_of_odd_scalings`, `exotic_eq_of_odd_scalings`, `sgn_neg`, `exotic_neg`, `sgn_odd_smul`: if `q·u = p·u'` with `p, q` odd (in particular `u' = ±u`), then `exotic u = exotic u'`; so `exotic` is a function of the rational ray (odd‑primitive representatives of one ray differ by exactly such a factor — this last sentence is stated in prose, not in Lean).
- `exotic_eq_third_of_isRay`, `sgn_eq_zero_of_isRay`: on the repository's rays (square norm) `exotic` is the constant `1/3`; `isPrimitive_of_isRay` links the two carriers.
- `no_real_triangle`: no orthogonal triple of odd‑primitive integer vectors has all three members `≡ (1,1,0) (mod 2)`.
- Auxiliary: `sgn_spec`, `sgn_spec'`, `sgn_mem`, `mul_emod_four`, `odd_mul_emod_four`, and explicit‑vector lemmas.

**File `BornGaussianRationalFrameObstruction.lean` (over K = ℚ(i)):**
- `frame_tri_110`, `frame_tri_101`, `frame_tri_011`: explicit non‑real orthogonal frames of `K³` (e.g. `(1,1,0), (1,−1,1+i), (1,−1,−1−i)`) whose three members share the `(1+i)`‑parity class; `frame_e3_110`, `frame_e1_011`, `frame_e2_101`, `frame_111_110`: four real frames.
- `parity_class_function_is_third`: if `f : K³ → ℚ` sums to `1` on every orthogonal frame of nonzero pairwise‑orthogonal vectors (`IsFrameFunction`), and on every Gaussian‑integer vector not all of whose components are divisible by `1+i` the value `f` depends only on the triple `((a+b)%2, (c+d)%2, (e+g)%2)` (`ParityDetermined`), then `f = 1/3` on every such vector. (That `1/3` is the Born function of `ρ = I/3` is stated in prose only.)

**File `BornGaussianFrameRays.lean`:**
- `exists_frame_completion`: every nonzero `v ∈ K³` completes to a frame `(v, w, u)`, with the same `w, u` for every nonzero rescaling of `v`.
- `frameFunction_smul`: for any `IsFrameFunction f`, `f (l • v) = f v` whenever `v ≠ 0`, `l ≠ 0`; so vector‑level frame functions are functions on rays.

Left unproved: existence of a non‑quadratic frame function on all `ℚ(i)`‑rays (A); quadraticity of every frame function on `ℚ(i)`‑rays (B); whether the ℚ‑function `exotic` extends to a frame function on `K³` rays. The `(1+i)`‑divisibility criterion `(1+i) ∣ a+bi ⇔ a ≡ b (mod 2)` is used as the definition of "parity class" and is justified only in prose.