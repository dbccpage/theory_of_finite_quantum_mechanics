/-!
Finite Gaussian-integer slice of the imported complex-field target.
AuthorityEffect: None.
The module has no import.
-/

namespace CampaignGpImportComplexField

@[ext]
structure G where
  re : Int
  im : Int
  deriving DecidableEq, Repr

def gAdd (z w : G) : G := ⟨z.re + w.re, z.im + w.im⟩
def gSub (z w : G) : G := ⟨z.re - w.re, z.im - w.im⟩
def gMul (z w : G) : G := ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩
def gConj (z : G) : G := ⟨z.re, -z.im⟩
def gZero : G := ⟨0, 0⟩
def gOne : G := ⟨1, 0⟩
def gSq (z : G) : G := gMul z z
def gNorm (z : G) : Int := z.re * z.re + z.im * z.im

theorem gNorm_mul (z w : G) : gNorm (gMul z w) = gNorm z * gNorm w := by
  rcases z with ⟨zr, zi⟩
  rcases w with ⟨wr, wi⟩
  simp [gNorm, gMul]
  grind

theorem int_sq_nonneg (a : Int) : 0 ≤ a * a := by
  rcases Int.le_total 0 a with h | h
  · exact Int.mul_nonneg h h
  · rw [← Int.neg_mul_neg]
    exact Int.mul_nonneg (Int.neg_nonneg_of_nonpos h) (Int.neg_nonneg_of_nonpos h)

theorem gNorm_eq_zero_iff (z : G) : gNorm z = 0 ↔ z = gZero := by
  constructor
  · intro h
    rcases z with ⟨zr, zi⟩
    have hsum : zr * zr + zi * zi = 0 := by simpa [gNorm] using h
    have hre : 0 ≤ zr * zr := int_sq_nonneg zr
    have him : 0 ≤ zi * zi := int_sq_nonneg zi
    generalize ardef : zr * zr = ar at hre hsum
    generalize aidef : zi * zi = ai at him hsum
    have hz : ar = 0 ∧ ai = 0 := by omega
    have hzr : zr = 0 := by
      have : zr * zr = 0 := ardef.trans hz.1
      rcases Int.mul_eq_zero.mp this with h0 | h0
      · exact h0
      · exact h0
    have hzi : zi = 0 := by
      have : zi * zi = 0 := aidef.trans hz.2
      rcases Int.mul_eq_zero.mp this with h0 | h0
      · exact h0
      · exact h0
    simp [gZero, hzr, hzi]
  · rintro rfl
    simp [gNorm, gZero]

theorem gMul_eq_zero (z w : G) (h : gMul z w = gZero) : z = gZero ∨ w = gZero := by
  have hn : gNorm (gMul z w) = 0 := (gNorm_eq_zero_iff (gMul z w)).mpr h
  rw [gNorm_mul] at hn
  rcases Int.mul_eq_zero.mp hn with hz | hw
  · exact Or.inl ((gNorm_eq_zero_iff z).mp hz)
  · exact Or.inr ((gNorm_eq_zero_iff w).mp hw)

theorem onePlusI_mul_coords (a : G) :
    gMul ⟨1, 1⟩ a = ⟨a.re - a.im, a.re + a.im⟩ := by
  rcases a with ⟨ar, ai⟩
  ext <;> simp [gMul] <;> grind

theorem onePlusI_mul_ne_one (a : G) : gMul ⟨1, 1⟩ a ≠ gOne := by
  intro h
  have hre : a.re - a.im = 1 := by
    have := congrArg G.re h
    rw [onePlusI_mul_coords] at this
    simpa [gOne] using this
  have him : a.re + a.im = 0 := by
    have := congrArg G.im h
    rw [onePlusI_mul_coords] at this
    simpa [gOne] using this
  omega

theorem gMul_comm (z w : G) : gMul z w = gMul w z := by
  rcases z with ⟨zr, zi⟩
  rcases w with ⟨wr, wi⟩
  ext <;> simp [gMul] <;> grind

/-- `(1+i)` is not a unit: neither side multiplies to the real unit. -/
theorem onePlusI_not_unit (a : G) :
    gMul ⟨1, 1⟩ a ≠ gOne ∧ gMul a ⟨1, 1⟩ ≠ gOne := by
  refine ⟨onePlusI_mul_ne_one a, ?_⟩
  rw [gMul_comm]
  exact onePlusI_mul_ne_one a

theorem intSqNeFive (k : Int) : k * k ≠ 5 := by
  intro h
  by_cases hle : k.natAbs ≤ 2
  · have hvals : k.natAbs = 0 ∨ k.natAbs = 1 ∨ k.natAbs = 2 := by omega
    rcases hvals with h0 | h1 | h2
    · have hk : k = 0 := Int.natAbs_eq_zero.mp h0
      simp [hk] at h
    · rcases Int.natAbs_eq_iff.mp h1 with hk | hk
      · rw [hk] at h
        exact absurd h (by decide)
      · rw [show k = -1 by simpa using hk] at h
        exact absurd h (by decide)
    · rcases Int.natAbs_eq_iff.mp h2 with hk | hk
      · rw [hk] at h
        exact absurd h (by decide)
      · rw [show k = -2 by simpa using hk] at h
        exact absurd h (by decide)
  · have h3 : 3 ≤ k.natAbs := by omega
    have h9 : 9 ≤ k.natAbs * k.natAbs := by
      have hmul : 3 * 3 ≤ k.natAbs * k.natAbs := Nat.mul_le_mul h3 h3
      omega
    have h9i : (9 : Int) ≤ (k.natAbs * k.natAbs : Int) := Int.ofNat_le.mpr h9
    rw [Int.natAbs_mul_self'] at h9i
    omega

theorem twice_sub_one_sq (p : Int) (h : p * p = p + 1) :
    (2 * p - 1) * (2 * p - 1) = 5 := by
  grind

/-- `λ * λ = λ + 1` has no solution in `G`. -/
theorem gauss_sq_ne_succ (lam : G) : gSq lam ≠ gAdd lam gOne := by
  intro h
  have hre : (gSq lam).re = (gAdd lam gOne).re := congrArg G.re h
  have him : (gSq lam).im = (gAdd lam gOne).im := congrArg G.im h
  simp [gSq, gMul, gAdd, gOne] at hre him
  have him0 : lam.im * (2 * lam.re - 1) = 0 := by
    grind
  rcases Int.mul_eq_zero.mp him0 with hq | hp
  · have hsq : lam.re * lam.re = lam.re + 1 := by
      grind
    exact intSqNeFive (2 * lam.re - 1) (twice_sub_one_sq lam.re hsq)
  · omega

theorem gMul_zero_left (z : G) : gMul gZero z = gZero := by
  rcases z with ⟨zr, zi⟩
  simp [gMul, gZero]

theorem gMul_zero_right (z : G) : gMul z gZero = gZero := by
  rw [gMul_comm]
  exact gMul_zero_left z

theorem gMul_one_left (z : G) : gMul gOne z = z := by
  rcases z with ⟨zr, zi⟩
  ext <;> simp [gMul, gOne]

theorem gAdd_zero_left (z : G) : gAdd gZero z = z := by
  rcases z with ⟨zr, zi⟩
  simp [gAdd, gZero]

theorem gMul_add_left (a b c : G) :
    gMul (gAdd a b) c = gAdd (gMul a c) (gMul b c) := by
  rcases a with ⟨ar, ai⟩
  rcases b with ⟨br, bi⟩
  rcases c with ⟨cr, ci⟩
  ext <;> simp [gMul, gAdd] <;> grind

theorem gMul_assoc (a b c : G) : gMul (gMul a b) c = gMul a (gMul b c) := by
  rcases a with ⟨ar, ai⟩
  rcases b with ⟨br, bi⟩
  rcases c with ⟨cr, ci⟩
  ext <;> simp [gMul] <;> grind

theorem gMul_sub_left (a b c : G) :
    gMul (gSub a b) c = gSub (gMul a c) (gMul b c) := by
  rcases a with ⟨ar, ai⟩
  rcases b with ⟨br, bi⟩
  rcases c with ⟨cr, ci⟩
  ext <;> simp [gMul, gSub] <;> grind

theorem gSub_eq_zero_iff (a b : G) : gSub a b = gZero ↔ a = b := by
  constructor
  · intro h
    rcases a with ⟨ar, ai⟩
    rcases b with ⟨br, bi⟩
    have hre : ar - br = 0 := by
      have := congrArg G.re h
      simpa [gSub, gZero] using this
    have him : ai - bi = 0 := by
      have := congrArg G.im h
      simpa [gSub, gZero] using this
    have har : ar = br := by omega
    have hai : ai = bi := by omega
    simp [har, hai]
  · rintro rfl
    rcases a with ⟨ar, ai⟩
    simp [gSub, gZero]

structure M2 where
  m11 : G
  m12 : G
  m21 : G
  m22 : G
  deriving DecidableEq, Repr

/-- Rows `(0, 1)` and `(1, 1)`. -/
def fib : M2 := ⟨⟨0, 0⟩, ⟨1, 0⟩, ⟨1, 0⟩, ⟨1, 0⟩⟩

def mulVec (M : M2) (x y : G) : G × G :=
  (gAdd (gMul M.m11 x) (gMul M.m12 y), gAdd (gMul M.m21 x) (gMul M.m22 y))

def scaleVec (lam x y : G) : G × G := (gMul lam x, gMul lam y)

theorem fib_conjugate_transpose :
    gConj fib.m11 = fib.m11 ∧
    gConj fib.m22 = fib.m22 ∧
    gConj fib.m12 = fib.m21 ∧
    gConj fib.m21 = fib.m12 := by
  decide

theorem fib_mulVec (x y : G) : mulVec fib x y = (y, gAdd x y) := by
  simp only [mulVec, fib]
  rw [show (⟨0, 0⟩ : G) = gZero from rfl, show (⟨1, 0⟩ : G) = gOne from rfl]
  rw [gMul_zero_left, gMul_one_left, gAdd_zero_left, gMul_one_left]

/-- A nonzero column is not a Gauss-integer eigenvector of `fib`. -/
theorem fib_no_gauss_eigenpair (lam x y : G)
    (h : mulVec fib x y = scaleVec lam x y)
    (hv : x ≠ gZero ∨ y ≠ gZero) : False := by
  have hy : y = gMul lam x := by
    have := congrArg Prod.fst h
    simpa [fib_mulVec, scaleVec] using this
  have hx : gAdd x y = gMul lam y := by
    have := congrArg Prod.snd h
    simpa [fib_mulVec, scaleVec] using this
  have hx0 : x ≠ gZero := by
    intro hx0
    have hy0 : y = gZero := by
      rw [hy, hx0]
      exact gMul_zero_right lam
    exact hv.elim (fun hne => hne hx0) (fun hne => hne hy0)
  rw [hy] at hx
  have hleft : gAdd x (gMul lam x) = gMul (gAdd gOne lam) x := by
    have hdist := (gMul_add_left gOne lam x).symm
    simpa [gMul_one_left] using hdist
  have hright : gMul lam (gMul lam x) = gMul (gSq lam) x := by
    simpa [gSq] using (gMul_assoc lam lam x).symm
  rw [hleft, hright] at hx
  have hsub : gSub (gMul (gSq lam) x) (gMul (gAdd gOne lam) x) = gZero :=
    (gSub_eq_zero_iff _ _).mpr hx.symm
  have hfac0 : gMul (gSub (gSq lam) (gAdd gOne lam)) x = gZero := by
    rw [gMul_sub_left]
    exact hsub
  rcases gMul_eq_zero _ _ hfac0 with hchar | hxz
  · have hsq0 : gSq lam = gAdd gOne lam := (gSub_eq_zero_iff _ _).mp hchar
    have hcomm : gAdd gOne lam = gAdd lam gOne := by
      ext <;> simp [gAdd, gOne] <;> omega
    exact gauss_sq_ne_succ lam (hsq0.trans hcomm)
  · exact hx0 hxz

#print axioms CampaignGpImportComplexField.onePlusI_mul_coords
#print axioms CampaignGpImportComplexField.onePlusI_mul_ne_one
#print axioms CampaignGpImportComplexField.onePlusI_not_unit
#print axioms CampaignGpImportComplexField.gNorm_mul
#print axioms CampaignGpImportComplexField.intSqNeFive
#print axioms CampaignGpImportComplexField.gauss_sq_ne_succ
#print axioms CampaignGpImportComplexField.fib_conjugate_transpose
#print axioms CampaignGpImportComplexField.fib_mulVec
#print axioms CampaignGpImportComplexField.fib_no_gauss_eigenpair

end CampaignGpImportComplexField
