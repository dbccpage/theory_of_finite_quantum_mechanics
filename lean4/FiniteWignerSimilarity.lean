import FiniteWignerTheorem
import SectorFormHermitian
import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Fin.VecNotation
import Mathlib.Data.Rat.Lemmas
import Mathlib.Tactic.FinCases

/-
Similarities, unitary normalisation and the exact countermodel.  AuthorityEffect: None.

The finite exact Wigner theorem (`FiniteWignerTheorem.finite_wigner`) delivers a *similarity*
`Fᴴ F = d • 1` with a positive rational scale `d`, not a unitary.  This module records exactly when
the scale can be removed:

* `unitary_of_norm`, `similarity_of_unitary`, `exists_unitary_iff`: `F` is a scalar multiple of a
  ℚ(i)-unitary iff `d` is a norm from ℚ(i), i.e. a sum of two rational squares.
* `three_not_sum_two_sq`: `3` is not a sum of two rational squares (descent modulo 3, exact over
  ℤ); hence `three_not_norm`.
* `F3 = [[1, −1 + i], [1 + i, 1]]` has `F3ᴴ F3 = 3 • 1` (`F3_similarity`), so `x ↦ F3 x` preserves
  transition probabilities (`F3_tpPreserving`) and is reversible, yet is induced by no ℚ(i)-unitary
  (`F3_not_induced_by_unitary`) and by no ℚ(i)-antiunitary (`F3_not_induced_by_antiunitary`).  Over
  the exact carrier, "unitary or antiunitary" is strictly stronger than what transition-probability
  preservation gives; the correct finite statement is "linear or conjugate-linear similarity".
* `eq_smul_one_of_rays`: a matrix fixing every ray is a scalar (used for the countermodel).
* `permMatrix`: the PermutationUnitary permutation envelope `permute σ` of `SectorFormHermitian` is the unitary
  `permMatrix σ` (`permMatrix_mulVec`, `permMatrix_unitary`), hence a special case of the derived
  class.
* `tpPreserving_iff_born`: transition-probability preservation is the preservation of the Born
  readout of rank-one effects (`BornHermitianCarrier.P`), the operational form of the hypothesis.

Nothing physical is claimed; the carrier, the scalar field and the readout are supplied.
-/

namespace WignerFinite.Similarity

open Matrix BornFinite BornFinite.HermitianCarrier BornFinite.HermitianPsd WignerFinite.Kernel
  WignerFinite.Theorem

variable {n : ℕ}

/-! ### Unitary normalisation -/

/-- A ℚ(i)-unitary: `Uᴴ * U = 1`. -/
def Unitary (U : Matrix (Fin n) (Fin n) GaussRat) : Prop := Uᴴ * U = 1

theorem unitary_iff_similarity_one (U : Matrix (Fin n) (Fin n) GaussRat) :
    Unitary U ↔ Similarity U 1 := by
  unfold Unitary Similarity
  rw [one_smul]

theorem Unitary.ip_mulVec {U : Matrix (Fin n) (Fin n) GaussRat} (hU : Unitary U)
    (x y : Fin n → GaussRat) : ip (U *ᵥ x) (U *ᵥ y) = ip x y := by
  rw [((unitary_iff_similarity_one U).mp hU).ip_mulVec, one_smul]

theorem Unitary.mul_conjTranspose {U : Matrix (Fin n) (Fin n) GaussRat} (hU : Unitary U) :
    U * Uᴴ = 1 := mul_eq_one_comm.mp hU

theorem qsmul_eq_smul (q : ℚ) (M : Matrix (Fin n) (Fin n) GaussRat) :
    q • M = ((q : ℚ) : GaussRat) • M := by
  refine Matrix.ext fun i j => ?_
  rw [Matrix.smul_apply, Matrix.smul_apply, smul_eq_mul, ratCast_mul]

theorem conjTranspose_gsmul (c : GaussRat) (M : Matrix (Fin n) (Fin n) GaussRat) :
    (c • M)ᴴ = star c • Mᴴ := by
  refine Matrix.ext fun i j => ?_
  rw [conjTranspose_apply, Matrix.smul_apply, Matrix.smul_apply, conjTranspose_apply, smul_eq_mul,
    smul_eq_mul, star_mul']

/-- A scalar multiple of a unitary is a similarity with scale `|c|²`. -/
theorem similarity_of_unitary {U : Matrix (Fin n) (Fin n) GaussRat} (hU : Unitary U) (c : GaussRat) :
    Similarity (c • U) (GaussRat.normSq c) := by
  unfold Similarity
  rw [conjTranspose_gsmul, smul_mul, Matrix.mul_smul, smul_smul, hU, GaussRat.star_mul_self,
    qsmul_eq_smul]
  rfl

/-- Rescaling a similarity by a scalar of norm `d` yields a unitary. -/
theorem unitary_of_norm {F : Matrix (Fin n) (Fin n) GaussRat} {d : ℚ} (hF : Similarity F d)
    {c : GaussRat} (hc : GaussRat.normSq c = d) (hc0 : c ≠ 0) : Unitary (c⁻¹ • F) := by
  unfold Unitary
  rw [conjTranspose_gsmul, smul_mul, Matrix.mul_smul, smul_smul, hF, qsmul_eq_smul, smul_smul]
  have hn : c.re ^ 2 + c.im ^ 2 ≠ 0 := fun h0 => hc0 ((GaussRat.normSq_eq_zero_iff c).mp h0)
  have h1 : star c⁻¹ * c⁻¹ * (d : GaussRat) = 1 := by
    rw [← hc]
    ext
    · simp only [GaussRat.re_mul, GaussRat.im_mul, GaussRat.re_star, GaussRat.im_star,
        GaussRat.re_inv, GaussRat.im_inv, GaussRat.re_ratCast, GaussRat.im_ratCast, GaussRat.re_one,
        GaussRat.normSq]
      field_simp
      ring
    · simp only [GaussRat.re_mul, GaussRat.im_mul, GaussRat.re_star, GaussRat.im_star,
        GaussRat.re_inv, GaussRat.im_inv, GaussRat.re_ratCast, GaussRat.im_ratCast, GaussRat.im_one,
        GaussRat.normSq]
      ring
  rw [h1, one_smul]

/-- With at least one sector, a similarity is a scalar multiple of a unitary iff its scale is a
norm from ℚ(i). -/
theorem exists_unitary_iff {F : Matrix (Fin n) (Fin n) GaussRat} {d : ℚ} (hF : Similarity F d)
    (hd : 0 < d) (i₀ : Fin n) :
    (∃ (c : GaussRat) (U : Matrix (Fin n) (Fin n) GaussRat), Unitary U ∧ F = c • U) ↔
      ∃ c : GaussRat, GaussRat.normSq c = d := by
  constructor
  · rintro ⟨c, U, hU, rfl⟩
    refine ⟨c, ?_⟩
    have h1 := similarity_of_unitary hU c
    unfold Similarity at h1 hF
    have h2 : (GaussRat.normSq c • (1 : Matrix (Fin n) (Fin n) GaussRat)) i₀ i₀ =
        (d • (1 : Matrix (Fin n) (Fin n) GaussRat)) i₀ i₀ := by rw [h1.symm.trans hF]
    rw [Matrix.smul_apply, Matrix.smul_apply, Matrix.one_apply_eq] at h2
    have := congrArg GaussRat.re h2
    simpa using this
  · rintro ⟨c, hc⟩
    have hc0 : c ≠ 0 := fun h0 => by
      rw [h0, (GaussRat.normSq_eq_zero_iff 0).mpr rfl] at hc
      exact hd.ne hc
    refine ⟨c, c⁻¹ • F, unitary_of_norm hF hc hc0, ?_⟩
    rw [smul_smul, mul_inv_cancel₀ hc0, one_smul]

theorem norm_iff_sum_two_sq (d : ℚ) :
    (∃ c : GaussRat, GaussRat.normSq c = d) ↔ ∃ a b : ℚ, a ^ 2 + b ^ 2 = d := by
  constructor
  · rintro ⟨c, hc⟩
    exact ⟨c.re, c.im, hc⟩
  · rintro ⟨a, b, h⟩
    exact ⟨⟨a, b⟩, h⟩

/-! ### `3` is not a sum of two rational squares -/

theorem three_dvd_of_sq_add_sq {a b : ℤ} (h : (3 : ℤ) ∣ a ^ 2 + b ^ 2) :
    (3 : ℤ) ∣ a ∧ (3 : ℤ) ∣ b := by
  have h3 : ((a : ZMod 3)) ^ 2 + (b : ZMod 3) ^ 2 = 0 := by
    have := (ZMod.intCast_zmod_eq_zero_iff_dvd (a ^ 2 + b ^ 2) 3).mpr (by exact_mod_cast h)
    push_cast at this
    exact this
  have key : ∀ x y : ZMod 3, x ^ 2 + y ^ 2 = 0 → x = 0 ∧ y = 0 := by decide
  obtain ⟨ha, hb⟩ := key _ _ h3
  exact ⟨by exact_mod_cast (ZMod.intCast_zmod_eq_zero_iff_dvd a 3).mp ha,
    by exact_mod_cast (ZMod.intCast_zmod_eq_zero_iff_dvd b 3).mp hb⟩

/-- Descent: `a² + b² = 3 c²` over `ℤ` forces `c = 0`. -/
theorem descent_three : ∀ m : ℕ, ∀ a b c : ℤ, c.natAbs = m → a ^ 2 + b ^ 2 = 3 * c ^ 2 → c = 0 := by
  intro m
  induction m using Nat.strong_induction_on with
  | _ m ih =>
    intro a b c hm h
    by_contra hc
    obtain ⟨ha, hb⟩ := three_dvd_of_sq_add_sq (a := a) (b := b) ⟨c ^ 2, h⟩
    obtain ⟨a', rfl⟩ := ha
    obtain ⟨b', rfl⟩ := hb
    have hc2 : (3 : ℤ) ∣ c ^ 2 + 0 ^ 2 := ⟨a' ^ 2 + b' ^ 2, by
      ring_nf
      ring_nf at h
      linarith⟩
    obtain ⟨c', rfl⟩ := (three_dvd_of_sq_add_sq hc2).1
    have h' : a' ^ 2 + b' ^ 2 = 3 * c' ^ 2 := by
      ring_nf
      ring_nf at h
      linarith
    have hc' : c' ≠ 0 := fun h0 => hc (by rw [h0, mul_zero])
    have hlt : c'.natAbs < (3 * c').natAbs := by
      rw [Int.natAbs_mul]
      have h3 : (3 : ℤ).natAbs = 3 := rfl
      rw [h3]
      have : 0 < c'.natAbs := Int.natAbs_pos.mpr hc'
      omega
    exact hc' (ih _ (hm ▸ hlt) a' b' c' rfl h')

theorem int_sq_add_sq_eq_three_mul_sq {a b c : ℤ} (h : a ^ 2 + b ^ 2 = 3 * c ^ 2) : c = 0 :=
  descent_three _ a b c rfl h

theorem three_not_sum_two_sq : ¬ ∃ a b : ℚ, a ^ 2 + b ^ 2 = 3 := by
  rintro ⟨a, b, h⟩
  set A : ℤ := a.num * b.den with hAdef
  set B : ℤ := b.num * a.den with hBdef
  set C : ℤ := (a.den : ℤ) * b.den with hCdef
  have hA : (A : ℚ) = a * (C : ℚ) := by
    rw [hAdef, hCdef]
    push_cast
    rw [← Rat.mul_den_eq_num]
    ring
  have hB : (B : ℚ) = b * (C : ℚ) := by
    rw [hBdef, hCdef]
    push_cast
    rw [← Rat.mul_den_eq_num]
    ring
  have hC : C ≠ 0 := by
    rw [hCdef]
    exact mul_ne_zero (by exact_mod_cast a.den_ne_zero) (by exact_mod_cast b.den_ne_zero)
  have key : A ^ 2 + B ^ 2 = 3 * C ^ 2 := by
    have : (A : ℚ) ^ 2 + (B : ℚ) ^ 2 = 3 * (C : ℚ) ^ 2 := by
      rw [hA, hB]
      linear_combination (C : ℚ) ^ 2 * h
    exact_mod_cast this
  exact hC (int_sq_add_sq_eq_three_mul_sq key)

theorem three_not_norm : ¬ ∃ c : GaussRat, GaussRat.normSq c = 3 := by
  rw [norm_iff_sum_two_sq]
  exact three_not_sum_two_sq

/-! ### A matrix fixing every ray is a scalar; an antilinear ray action kills a basis vector -/

theorem mulVec_e_apply (M : Matrix (Fin n) (Fin n) GaussRat) (k j : Fin n) :
    (M *ᵥ e k) j = M j k := by
  rw [e, mulVec_single', one_smul, transpose_apply]

/-- A matrix that maps every ray to itself is a scalar multiple of the identity. -/
theorem eq_smul_one_of_rays {M : Matrix (Fin n) (Fin n) GaussRat} (i₀ : Fin n)
    (h : ∀ x, x ≠ 0 → ∃ μ : GaussRat, M *ᵥ x = μ • x) :
    M = (M i₀ i₀) • (1 : Matrix (Fin n) (Fin n) GaussRat) := by
  have hcol : ∀ k j, M j k = if j = k then M k k else 0 := by
    intro k j
    obtain ⟨μ, hμ⟩ := h (e k) (e_ne_zero k)
    have hj := congrFun hμ j
    have hk := congrFun hμ k
    rw [mulVec_e_apply, Pi.smul_apply, smul_eq_mul] at hj hk
    rw [e_apply_self, mul_one] at hk
    rw [e_apply] at hj
    rw [hj, hk]
    split_ifs <;> simp
  have hoff : ∀ k j, j ≠ k → M j k = 0 := by
    intro k j hjk
    rw [hcol k j]
    simp [hjk]
  have hdiag : ∀ k, M k k = M i₀ i₀ := by
    intro k
    by_cases hk : k = i₀
    · rw [hk]
    · obtain ⟨ν, hν⟩ := h (e i₀ + e k) (by
        intro h0
        have := congrFun h0 i₀
        rw [Pi.add_apply, e_apply_self, e_apply_ne (Ne.symm hk), add_zero, Pi.zero_apply] at this
        exact one_ne_zero this)
      have h₀ := congrFun hν i₀
      have h₁ := congrFun hν k
      simp only [mulVec_add, Pi.add_apply, mulVec_e_apply, Pi.smul_apply, smul_eq_mul,
        e_apply_self, e_apply_ne (Ne.symm hk), e_apply_ne hk, add_zero, zero_add, mul_one,
        hoff k i₀ (Ne.symm hk), hoff i₀ k hk] at h₀ h₁
      rw [h₁, h₀]
  refine Matrix.ext fun j k => ?_
  rw [Matrix.smul_apply, Matrix.one_apply, smul_eq_mul]
  by_cases hjk : j = k
  · subst hjk
    rw [hdiag j]
    simp
  · rw [hoff k j hjk]
    simp [hjk]

/-- If `M x` is always proportional to `star x` (with two distinct sectors available), then `M`
kills a basis vector. -/
theorem mulVec_e_eq_zero_of_antilinear_rays {M : Matrix (Fin n) (Fin n) GaussRat} {a b : Fin n}
    (hab : a ≠ b) (h : ∀ x, x ≠ 0 → ∃ μ : GaussRat, M *ᵥ x = μ • star x) : M *ᵥ e a = 0 := by
  obtain ⟨μa, hμa⟩ := h (e a) (e_ne_zero a)
  obtain ⟨μb, hμb⟩ := h (e b) (e_ne_zero b)
  have hstar : ∀ k, star (e k : Fin n → GaussRat) = e k := by
    intro k
    funext j
    rw [Pi.star_apply, e_apply]
    split_ifs <;> simp
  rw [hstar] at hμa hμb
  -- the probe e a + e b
  obtain ⟨ν, hν⟩ := h (e a + e b) (by
    intro h0
    have := congrFun h0 a
    rw [Pi.add_apply, e_apply_self, e_apply_ne hab, add_zero, Pi.zero_apply] at this
    exact one_ne_zero this)
  rw [mulVec_add, hμa, hμb, star_add, hstar, hstar] at hν
  have hνa := congrFun hν a
  have hνb := congrFun hν b
  simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul, e_apply_self, e_apply_ne (Ne.symm hab),
    e_apply_ne hab, mul_one, mul_zero, add_zero, zero_add] at hνa hνb
  -- the probe e a + i e b
  obtain ⟨ρ, hρ⟩ := h (e a + GaussRat.I • e b) (by
    intro h0
    have := congrFun h0 a
    rw [Pi.add_apply, e_apply_self, Pi.smul_apply, e_apply_ne hab, smul_zero, add_zero,
      Pi.zero_apply] at this
    exact one_ne_zero this)
  rw [mulVec_add, mulVec_smul, hμa, hμb, star_add] at hρ
  have hρa := congrFun hρ a
  have hρb := congrFun hρ b
  simp only [Pi.add_apply, Pi.smul_apply, Pi.star_apply, smul_eq_mul, e_apply_self,
    e_apply_ne (Ne.symm hab), e_apply_ne hab, mul_one, mul_zero, add_zero, zero_add, star_one,
    star_zero, GaussRat.star_I] at hρa hρb
  -- μa = ν = μb and μa = ρ, i μb = -ρ i, hence μa = 0
  have h1 : μa = μb := by rw [hνa, hνb]
  have h2 : GaussRat.I * μb = -(μa * GaussRat.I) := by
    rw [hρb, ← hρa]
    ring
  have h3 : μa = 0 := by
    rw [← h1] at h2
    have h4 : (2 * GaussRat.I) * μa = 0 := by linear_combination h2
    rcases mul_eq_zero.mp h4 with h5 | h5
    · exfalso
      have := congrArg GaussRat.im h5
      simp at this
    · exact h5
  rw [hμa, h3, zero_smul]

/-! ### The countermodel `F3` with scale `3` -/

/-- `F3 = [[1, −1 + i], [1 + i, 1]]`. -/
def F3 : Matrix (Fin 2) (Fin 2) GaussRat :=
  Matrix.of ![![1, ⟨-1, 1⟩], ![⟨1, 1⟩, 1]]

theorem F3_apply_00 : F3 0 0 = 1 := rfl
theorem F3_apply_01 : F3 0 1 = ⟨-1, 1⟩ := rfl
theorem F3_apply_10 : F3 1 0 = ⟨1, 1⟩ := rfl
theorem F3_apply_11 : F3 1 1 = 1 := rfl

theorem F3_similarity : Similarity F3 3 := by
  unfold Similarity
  refine Matrix.ext fun i j => ?_
  rw [Matrix.mul_apply, Fin.sum_univ_two, Matrix.smul_apply, conjTranspose_apply,
    conjTranspose_apply]
  fin_cases i <;> fin_cases j <;>
    simp [F3, GaussRat.ext_iff] <;> norm_num

theorem F3_tpPreserving : TpPreserving (fun x : Fin 2 → GaussRat => F3 *ᵥ x) where
  ne_zero x hx := F3_similarity.mulVec_ne_zero (by norm_num) hx
  tp_eq x y _ _ := F3_similarity.tp_mulVec (by norm_num) x y

theorem F3_mulVec_e_ne_zero : F3 *ᵥ e 0 ≠ 0 :=
  F3_similarity.mulVec_ne_zero (by norm_num) (e_ne_zero 0)

/-- No ℚ(i)-unitary induces the ray map of `F3`. -/
theorem F3_not_induced_by_unitary :
    ¬ ∃ U : Matrix (Fin 2) (Fin 2) GaussRat, Unitary U ∧
      ∀ x, x ≠ 0 → ∃ μ : GaussRat, μ ≠ 0 ∧ F3 *ᵥ x = μ • (U *ᵥ x) := by
  rintro ⟨U, hU, h⟩
  set M : Matrix (Fin 2) (Fin 2) GaussRat := Uᴴ * F3 with hM
  have hrays : ∀ x, x ≠ 0 → ∃ μ : GaussRat, M *ᵥ x = μ • x := by
    intro x hx
    obtain ⟨μ, _, hμ⟩ := h x hx
    refine ⟨μ, ?_⟩
    rw [hM, ← mulVec_mulVec, hμ, mulVec_smul, mulVec_mulVec, hU, one_mulVec]
  have hscalar := eq_smul_one_of_rays (0 : Fin 2) hrays
  have hF3 : F3 = (M 0 0) • U := by
    calc F3 = (U * Uᴴ) * F3 := by rw [hU.mul_conjTranspose, Matrix.one_mul]
      _ = U * M := by rw [hM, Matrix.mul_assoc]
      _ = (M 0 0) • U := by
          conv_lhs => rw [hscalar]
          rw [Matrix.mul_smul, Matrix.mul_one]
  have hex : ∃ c : GaussRat, GaussRat.normSq c = 3 :=
    (exists_unitary_iff F3_similarity (by norm_num) (0 : Fin 2)).mp ⟨M 0 0, U, hU, hF3⟩
  exact three_not_norm hex

/-- No ℚ(i)-antiunitary (`x ↦ U (star x)`, `U` unitary) induces the ray map of `F3`. -/
theorem F3_not_induced_by_antiunitary :
    ¬ ∃ U : Matrix (Fin 2) (Fin 2) GaussRat, Unitary U ∧
      ∀ x, x ≠ 0 → ∃ μ : GaussRat, μ ≠ 0 ∧ F3 *ᵥ x = μ • (U *ᵥ star x) := by
  rintro ⟨U, hU, h⟩
  set M : Matrix (Fin 2) (Fin 2) GaussRat := Uᴴ * F3 with hM
  have hrays : ∀ x, x ≠ 0 → ∃ μ : GaussRat, M *ᵥ x = μ • star x := by
    intro x hx
    obtain ⟨μ, _, hμ⟩ := h x hx
    refine ⟨μ, ?_⟩
    rw [hM, ← mulVec_mulVec, hμ, mulVec_smul, mulVec_mulVec, hU, one_mulVec]
  have hzero := mulVec_e_eq_zero_of_antilinear_rays (a := (0 : Fin 2)) (b := 1) (by decide) hrays
  apply F3_mulVec_e_ne_zero
  calc F3 *ᵥ e 0 = (U * Uᴴ * F3) *ᵥ e 0 := by rw [hU.mul_conjTranspose, Matrix.one_mul]
    _ = U *ᵥ (M *ᵥ e 0) := by rw [hM, Matrix.mul_assoc, mulVec_mulVec]
    _ = 0 := by rw [hzero, mulVec_zero]

/-! ### The permutation envelope is unitary -/

/-- The permutation matrix of `σ`: `(permMatrix σ) i j = 1` iff `σ j = i`. -/
def permMatrix (σ : Equiv.Perm (Fin n)) : Matrix (Fin n) (Fin n) GaussRat :=
  Matrix.of fun i j => if σ j = i then 1 else 0

theorem permMatrix_apply (σ : Equiv.Perm (Fin n)) (i j : Fin n) :
    permMatrix σ i j = if σ j = i then 1 else 0 := rfl

/-- The PermutationUnitary coordinate action `permute σ x = x ∘ σ.symm` of `SectorFormHermitian` is
`permMatrix σ *ᵥ x`. -/
theorem permMatrix_mulVec (σ : Equiv.Perm (Fin n)) (x : Fin n → GaussRat) :
    permMatrix σ *ᵥ x = InnerProductFinite.HermitianSectorForm.permute σ x := by
  funext i
  rw [mulVec_apply_eq_sum]
  simp only [permMatrix_apply, ite_mul, one_mul, zero_mul]
  rw [Finset.sum_eq_single (σ.symm i)]
  · simp [InnerProductFinite.HermitianSectorForm.permute]
  · intro j _ hj
    have hσ : σ j ≠ i := fun hσ => hj (by rw [← hσ, Equiv.symm_apply_apply])
    simp [hσ]
  · intro h
    exact absurd (Finset.mem_univ _) h

theorem permMatrix_unitary (σ : Equiv.Perm (Fin n)) : Unitary (permMatrix σ) := by
  unfold Unitary
  refine Matrix.ext fun i j => ?_
  rw [Matrix.mul_apply]
  simp only [conjTranspose_apply, permMatrix_apply]
  rw [Finset.sum_eq_single (σ i)]
  · by_cases hij : i = j
    · subst hij
      simp
    · have hσ : σ j ≠ σ i := fun h => hij (σ.injective h).symm
      simp [Matrix.one_apply_ne hij, hσ]
  · intro k _ hk
    have hσ : σ i ≠ k := fun h => hk h.symm
    simp [hσ]
  · intro h
    exact absurd (Finset.mem_univ _) h

theorem permMatrix_ip (σ : Equiv.Perm (Fin n)) (x y : Fin n → GaussRat) :
    ip (permMatrix σ *ᵥ x) (permMatrix σ *ᵥ y) = ip x y :=
  (permMatrix_unitary σ).ip_mulVec x y

/-! ### The Born form of the hypothesis -/

/-- Transition-probability preservation is the preservation of the normalised Born readout
`hf (P x) y / vnorm y` of rank-one effects. -/
theorem tpPreserving_iff_born (T : (Fin n → GaussRat) → (Fin n → GaussRat)) :
    TpPreserving T ↔ (∀ x, x ≠ 0 → T x ≠ 0) ∧
      ∀ x y, x ≠ 0 → y ≠ 0 → hf (P (T x)) (T y) / vnorm (T y) = hf (P x) y / vnorm y := by
  constructor
  · intro h
    refine ⟨h.ne_zero, fun x y hx hy => ?_⟩
    rw [← tp_eq_born, ← tp_eq_born]
    exact h.tp_eq x y hx hy
  · rintro ⟨h0, h⟩
    refine ⟨h0, fun x y hx hy => ?_⟩
    rw [tp_eq_born, tp_eq_born]
    exact h x y hx hy

/-- Unitaries are exact isometries of the selected form `hf 1 = vnorm`. -/
theorem Unitary.vnorm_mulVec {U : Matrix (Fin n) (Fin n) GaussRat} (hU : Unitary U)
    (x : Fin n → GaussRat) : vnorm (U *ᵥ x) = vnorm x := by
  rw [((unitary_iff_similarity_one U).mp hU).vnorm_mulVec, one_mul]

/-- A similarity is an isometry between the selected form and its `d`-scaled copy. -/
theorem similarity_hf_one_mulVec {F : Matrix (Fin n) (Fin n) GaussRat} {d : ℚ} (hF : Similarity F d)
    (x : Fin n → GaussRat) : hf 1 (F *ᵥ x) = d * hf 1 x := by
  rw [hf_one, hf_one, hF.vnorm_mulVec]

end WignerFinite.Similarity

#print axioms WignerFinite.Similarity.Unitary
#print axioms WignerFinite.Similarity.unitary_iff_similarity_one
#print axioms WignerFinite.Similarity.Unitary.ip_mulVec
#print axioms WignerFinite.Similarity.Unitary.mul_conjTranspose
#print axioms WignerFinite.Similarity.qsmul_eq_smul
#print axioms WignerFinite.Similarity.conjTranspose_gsmul
#print axioms WignerFinite.Similarity.similarity_of_unitary
#print axioms WignerFinite.Similarity.unitary_of_norm
#print axioms WignerFinite.Similarity.exists_unitary_iff
#print axioms WignerFinite.Similarity.norm_iff_sum_two_sq
#print axioms WignerFinite.Similarity.three_dvd_of_sq_add_sq
#print axioms WignerFinite.Similarity.descent_three
#print axioms WignerFinite.Similarity.int_sq_add_sq_eq_three_mul_sq
#print axioms WignerFinite.Similarity.three_not_sum_two_sq
#print axioms WignerFinite.Similarity.three_not_norm
#print axioms WignerFinite.Similarity.mulVec_e_apply
#print axioms WignerFinite.Similarity.eq_smul_one_of_rays
#print axioms WignerFinite.Similarity.mulVec_e_eq_zero_of_antilinear_rays
#print axioms WignerFinite.Similarity.F3
#print axioms WignerFinite.Similarity.F3_apply_00
#print axioms WignerFinite.Similarity.F3_apply_01
#print axioms WignerFinite.Similarity.F3_apply_10
#print axioms WignerFinite.Similarity.F3_apply_11
#print axioms WignerFinite.Similarity.F3_similarity
#print axioms WignerFinite.Similarity.F3_tpPreserving
#print axioms WignerFinite.Similarity.F3_mulVec_e_ne_zero
#print axioms WignerFinite.Similarity.F3_not_induced_by_unitary
#print axioms WignerFinite.Similarity.F3_not_induced_by_antiunitary
#print axioms WignerFinite.Similarity.permMatrix
#print axioms WignerFinite.Similarity.permMatrix_apply
#print axioms WignerFinite.Similarity.permMatrix_mulVec
#print axioms WignerFinite.Similarity.permMatrix_unitary
#print axioms WignerFinite.Similarity.permMatrix_ip
#print axioms WignerFinite.Similarity.tpPreserving_iff_born
#print axioms WignerFinite.Similarity.Unitary.vnorm_mulVec
#print axioms WignerFinite.Similarity.similarity_hf_one_mulVec
