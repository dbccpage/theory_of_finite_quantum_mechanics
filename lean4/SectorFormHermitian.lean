import BornHermitianCarrier
import BornHermitianPsdDecomposition
import Mathlib.Data.Fin.VecNotation
import Mathlib.Logic.Equiv.Basic
import Mathlib.Tactic.FinCases

/-
Uniqueness of the inner product on the sector carrier (Gaussian-rational case).  AuthorityEffect: None.

Carrier.  V := Fin n → ℚ(i), the sector carrier over the Gaussian rationals; a candidate inner product
is a Hermitian matrix H with real readout `hf H x = re (x* H x)`, the readout `BornHermitianCarrier`
uses to order effects, imported unchanged.

The two hypotheses of `SectorFormUniqueness` are transcribed verbatim: `SectorAdditive H` (the readout
is additive on disjointly supported Gaussian-rational vectors) and `Invariant H σ` for every sector
permutation σ in a set whose generated group is transitive (`Generated`, `eq_smul_one_generated`).
Over ℚ(i) sector additivity is tested along two directions in
each off-diagonal pair, `Pi.single j 1` and `Pi.single j I`: the first kills the real part of
`H i j + H j i`, the second the imaginary part of `H j i − H i j` (`offdiag_re_add_re`,
`offdiag_im_sub_im`); with `Hᴴ = H` both parts of `H i j` vanish (`offdiag_eq_zero`).  Transitive
invariance collapses the (real) diagonal, so `H = c • 1` with the rational scalar `c = re H i₀ i₀`
(`eq_smul_one`), the readout is `c · ⟨x, x⟩` (`hf_eq_scale_vnorm`), `c > 0` for a positive-definite
form (`scale_pos`), two selected forms agree once normalised (`unique_of_normalized`), and the standard
form `1` satisfies the hypotheses (`one_sectorAdditive`, `one_invariant`).

Control.  `imagLeak12 = [[1, i], [−i, 1]]` is Hermitian and additive on the pair `(e₀, e₁)` along the
real direction, yet not sector additive: along `(e₀, i·e₁)` its readout is not additive.  So the
second direction is needed over ℚ(i); the rational countermodels of `SectorFormUniqueness` apply
unchanged to real matrices.

What is not claimed: the carrier, the scalar field ℚ(i) and the quadratic shape of the readout are
supplied; the two laws are hypotheses; the scale is a unit choice.  Exact arithmetic throughout.
-/

namespace InnerProductFinite.HermitianSectorForm

open Matrix BornFinite BornFinite.HermitianCarrier BornFinite.HermitianPsd

variable {n : ℕ}

/-! ### Disjoint supports and sector additivity -/

/-- Two carrier vectors have disjoint sector supports. -/
def DisjointSupport (u v : Fin n → GaussRat) : Prop := ∀ k, u k = 0 ∨ v k = 0

/-- Sector additivity of the Hermitian readout on disjointly supported vectors. -/
def SectorAdditive (H : Matrix (Fin n) (Fin n) GaussRat) : Prop :=
  ∀ u v, DisjointSupport u v → hf H (u + v) = hf H u + hf H v

theorem disjoint_single_single {i j : Fin n} (h : i ≠ j) (s t : GaussRat) :
    DisjointSupport (Pi.single i s) (Pi.single j t) := by
  intro k
  by_cases hk : k = i
  · right
    subst hk
    rw [Pi.single_eq_of_ne h]
  · left
    rw [Pi.single_eq_of_ne hk]

theorem cross_single (A : Matrix (Fin n) (Fin n) GaussRat) (i j : Fin n) (s t : GaussRat) :
    star (Pi.single i s) ⬝ᵥ (A *ᵥ Pi.single j t) = star s * (t * A i j) := by
  rw [Pi.star_single, mulVec_single', single_dotProduct, Pi.smul_apply, smul_eq_mul,
    transpose_apply]

theorem hf_single_add_single (A : Matrix (Fin n) (Fin n) GaussRat) (i j : Fin n) (s t : GaussRat) :
    hf A (Pi.single i s + Pi.single j t) =
      hf A (Pi.single i s) + (star s * (t * A i j)).re + (star t * (s * A j i)).re +
        hf A (Pi.single j t) := by
  rw [hf_add_vec, cross_single, cross_single]

/-! ### Sector additivity forces an orthogonal sector basis -/

/-- The real direction: the real part of `H i j + H j i` vanishes. -/
theorem offdiag_re_add_re {H : Matrix (Fin n) (Fin n) GaussRat} (hA : SectorAdditive H) {i j : Fin n}
    (h : i ≠ j) : (H i j).re + (H j i).re = 0 := by
  have := hA _ _ (disjoint_single_single h 1 1)
  rw [hf_single_add_single] at this
  simp at this
  linarith

/-- The imaginary direction: the imaginary part of `H j i − H i j` vanishes. -/
theorem offdiag_im_sub_im {H : Matrix (Fin n) (Fin n) GaussRat} (hA : SectorAdditive H) {i j : Fin n}
    (h : i ≠ j) : (H j i).im - (H i j).im = 0 := by
  have := hA _ _ (disjoint_single_single h 1 GaussRat.I)
  rw [hf_single_add_single] at this
  simp [GaussRat.star_I] at this
  linarith

/-- For a Hermitian sector-additive form every off-diagonal entry is zero. -/
theorem offdiag_eq_zero {H : Matrix (Fin n) (Fin n) GaussRat} (hH : Hᴴ = H) (hA : SectorAdditive H)
    {i j : Fin n} (h : i ≠ j) : H i j = 0 := by
  have h1 := offdiag_re_add_re hA h
  have h2 := offdiag_im_sub_im hA h
  have h3 := hermitian_apply hH i j
  have hre : (H j i).re = (H i j).re := by rw [← h3, GaussRat.re_star]
  have him : (H j i).im = -(H i j).im := by rw [← h3, GaussRat.im_star]
  ext
  · rw [GaussRat.re_zero]
    linarith
  · rw [GaussRat.im_zero]
    linarith

/-! ### Transitive sector symmetry collapses the diagonal -/

/-- Coordinate action of a sector permutation, `(permute σ x) i = x (σ.symm i)`. -/
def permute (σ : Equiv.Perm (Fin n)) (x : Fin n → GaussRat) : Fin n → GaussRat :=
  fun i => x (σ.symm i)

theorem permute_single (σ : Equiv.Perm (Fin n)) (j : Fin n) (t : GaussRat) :
    permute σ (Pi.single j t) = Pi.single (σ j) t := by
  funext i
  simp only [permute, Pi.single_apply, Equiv.symm_apply_eq]

/-- `H` is invariant under the sector permutation `σ` when its readout is. -/
def Invariant (H : Matrix (Fin n) (Fin n) GaussRat) (σ : Equiv.Perm (Fin n)) : Prop :=
  ∀ x, hf H (permute σ x) = hf H x

/-- A set of sector permutations acts transitively on sectors: any two distinct sectors are
exchanged by some member. -/
def TransitiveOn (S : Set (Equiv.Perm (Fin n))) : Prop := ∀ i j : Fin n, i ≠ j → ∃ σ ∈ S, σ i = j

theorem hf_single_one (H : Matrix (Fin n) (Fin n) GaussRat) (a : Fin n) :
    hf H (Pi.single a 1) = (H a a).re := by
  rw [hf_single, normSq_one, one_mul]

theorem diag_re_eq_of_invariant {H : Matrix (Fin n) (Fin n) GaussRat} {σ : Equiv.Perm (Fin n)}
    (h : Invariant H σ) (j : Fin n) : (H (σ j) (σ j)).re = (H j j).re := by
  have := h (Pi.single j 1)
  rwa [permute_single, hf_single_one, hf_single_one] at this

theorem diag_re_const_of_transitive {H : Matrix (Fin n) (Fin n) GaussRat}
    {S : Set (Equiv.Perm (Fin n))} (hS : ∀ σ ∈ S, Invariant H σ) (hT : TransitiveOn S) (i j : Fin n) :
    (H i i).re = (H j j).re := by
  by_cases hij : i = j
  · rw [hij]
  · obtain ⟨σ, hσ, rfl⟩ := hT i j hij
    exact (diag_re_eq_of_invariant (hS σ hσ) i).symm

/-- The group generated by a set of sector permutations. -/
inductive Generated (S : Set (Equiv.Perm (Fin n))) : Equiv.Perm (Fin n) → Prop
  | of {σ : Equiv.Perm (Fin n)} (h : σ ∈ S) : Generated S σ
  | one : Generated S 1
  | mul {σ τ : Equiv.Perm (Fin n)} (hσ : Generated S σ) (hτ : Generated S τ) : Generated S (σ * τ)
  | inv {σ : Equiv.Perm (Fin n)} (hσ : Generated S σ) : Generated S σ⁻¹

theorem permute_one (x : Fin n → GaussRat) : permute (1 : Equiv.Perm (Fin n)) x = x := by
  funext i
  rfl

theorem permute_mul (σ τ : Equiv.Perm (Fin n)) (x : Fin n → GaussRat) :
    permute (σ * τ) x = permute σ (permute τ x) := by
  funext i
  simp only [permute, Equiv.Perm.mul_def, Equiv.symm_trans_apply]

theorem permute_inv_left (σ : Equiv.Perm (Fin n)) (x : Fin n → GaussRat) :
    permute σ⁻¹ (permute σ x) = x := by
  funext i
  simp only [permute, Equiv.Perm.inv_def, Equiv.symm_symm, Equiv.symm_apply_apply]

theorem permute_inv_right (σ : Equiv.Perm (Fin n)) (x : Fin n → GaussRat) :
    permute σ (permute σ⁻¹ x) = x := by
  have := permute_inv_left σ⁻¹ x
  rwa [inv_inv] at this

theorem invariant_one (H : Matrix (Fin n) (Fin n) GaussRat) : Invariant H 1 := fun x => by
  rw [permute_one]

theorem invariant_mul {H : Matrix (Fin n) (Fin n) GaussRat} {σ τ : Equiv.Perm (Fin n)}
    (hσ : Invariant H σ) (hτ : Invariant H τ) : Invariant H (σ * τ) := fun x => by
  rw [permute_mul, hσ, hτ]

theorem invariant_inv {H : Matrix (Fin n) (Fin n) GaussRat} {σ : Equiv.Perm (Fin n)}
    (hσ : Invariant H σ) : Invariant H σ⁻¹ := fun x => by
  have h := hσ (permute σ⁻¹ x)
  rw [permute_inv_right] at h
  exact h.symm

theorem invariant_of_generated {H : Matrix (Fin n) (Fin n) GaussRat} {S : Set (Equiv.Perm (Fin n))}
    (hS : ∀ σ ∈ S, Invariant H σ) {σ : Equiv.Perm (Fin n)} (h : Generated S σ) : Invariant H σ := by
  induction h with
  | of hm => exact hS _ hm
  | one => exact invariant_one H
  | mul _ _ ih₁ ih₂ => exact invariant_mul ih₁ ih₂
  | inv _ ih => exact invariant_inv ih

theorem diag_eq_of_hermitian_transitive {H : Matrix (Fin n) (Fin n) GaussRat}
    {S : Set (Equiv.Perm (Fin n))} (hH : Hᴴ = H) (hS : ∀ σ ∈ S, Invariant H σ) (hT : TransitiveOn S)
    (i i₀ : Fin n) : H i i = (H i₀ i₀).re • (1 : GaussRat) := by
  ext
  · rw [GaussRat.re_smul, GaussRat.re_one, mul_one]
    exact diag_re_const_of_transitive hS hT i i₀
  · rw [GaussRat.im_smul, GaussRat.im_one, mul_zero]
    exact diag_real_of_hermitian hH i

/-- Main theorem over ℚ(i): a Hermitian, sector-additive form invariant under a transitive set of
sector permutations is the rational scalar `re H i₀ i₀` times the identity. -/
theorem eq_smul_one {H : Matrix (Fin n) (Fin n) GaussRat} {S : Set (Equiv.Perm (Fin n))} (hH : Hᴴ = H)
    (hA : SectorAdditive H) (hS : ∀ σ ∈ S, Invariant H σ) (hT : TransitiveOn S) (i₀ : Fin n) :
    H = (H i₀ i₀).re • (1 : Matrix (Fin n) (Fin n) GaussRat) := by
  refine Matrix.ext fun i j => ?_
  by_cases h : i = j
  · subst h
    rw [Matrix.smul_apply, Matrix.one_apply_eq]
    exact diag_eq_of_hermitian_transitive hH hS hT i i₀
  · rw [Matrix.smul_apply, Matrix.one_apply_ne h, smul_zero]
    exact offdiag_eq_zero hH hA h

/-- The main theorem with the symmetry hypothesis on generators only. -/
theorem eq_smul_one_generated {H : Matrix (Fin n) (Fin n) GaussRat} {S : Set (Equiv.Perm (Fin n))}
    (hH : Hᴴ = H) (hA : SectorAdditive H) (hS : ∀ σ ∈ S, Invariant H σ)
    (hT : TransitiveOn (Generated S)) (i₀ : Fin n) :
    H = (H i₀ i₀).re • (1 : Matrix (Fin n) (Fin n) GaussRat) :=
  eq_smul_one hH hA (fun _ hσ => invariant_of_generated hS hσ) hT i₀

theorem hf_eq_scale_vnorm {H : Matrix (Fin n) (Fin n) GaussRat} {S : Set (Equiv.Perm (Fin n))}
    (hH : Hᴴ = H) (hA : SectorAdditive H) (hS : ∀ σ ∈ S, Invariant H σ) (hT : TransitiveOn S)
    (i₀ : Fin n) (x : Fin n → GaussRat) : hf H x = (H i₀ i₀).re * vnorm x := by
  have hG := eq_smul_one hH hA hS hT i₀
  calc hf H x = hf ((H i₀ i₀).re • (1 : Matrix (Fin n) (Fin n) GaussRat)) x := by rw [← hG]
    _ = (H i₀ i₀).re * vnorm x := by rw [hf_smul, hf_one]

theorem single_ne_zero (i : Fin n) : (Pi.single i (1 : GaussRat) : Fin n → GaussRat) ≠ 0 := by
  intro h
  have := congrFun h i
  simp at this

/-- Positive definiteness of the readout makes the scale positive. -/
theorem scale_pos {H : Matrix (Fin n) (Fin n) GaussRat} (hpos : ∀ x, x ≠ 0 → 0 < hf H x)
    (i₀ : Fin n) : 0 < (H i₀ i₀).re := by
  have := hpos _ (single_ne_zero i₀)
  rwa [hf_single_one] at this

/-! ### Uniqueness and nonvacuity -/

theorem unique_of_normalized {H H' : Matrix (Fin n) (Fin n) GaussRat} {S : Set (Equiv.Perm (Fin n))}
    (hH : Hᴴ = H) (hA : SectorAdditive H) (hS : ∀ σ ∈ S, Invariant H σ)
    (hH' : H'ᴴ = H') (hA' : SectorAdditive H') (hS' : ∀ σ ∈ S, Invariant H' σ)
    (hT : TransitiveOn S) (i₀ : Fin n) (hnorm : (H i₀ i₀).re = (H' i₀ i₀).re) : H = H' := by
  rw [eq_smul_one hH hA hS hT i₀, eq_smul_one hH' hA' hS' hT i₀, hnorm]

theorem eq_one_of_normalized {H : Matrix (Fin n) (Fin n) GaussRat} {S : Set (Equiv.Perm (Fin n))}
    (hH : Hᴴ = H) (hA : SectorAdditive H) (hS : ∀ σ ∈ S, Invariant H σ) (hT : TransitiveOn S)
    (i₀ : Fin n) (hnorm : (H i₀ i₀).re = 1) : H = 1 := by
  rw [eq_smul_one hH hA hS hT i₀, hnorm, one_smul]

theorem normSq_add_of_disjoint {a b : GaussRat} (h : a = 0 ∨ b = 0) :
    GaussRat.normSq (a + b) = GaussRat.normSq a + GaussRat.normSq b := by
  rcases h with rfl | rfl
  · simp [GaussRat.normSq]
  · simp [GaussRat.normSq]

theorem vnorm_add_of_disjoint {u v : Fin n → GaussRat} (h : DisjointSupport u v) :
    vnorm (u + v) = vnorm u + vnorm v := by
  unfold vnorm
  rw [← Finset.sum_add_distrib]
  exact Finset.sum_congr rfl (fun i _ => normSq_add_of_disjoint (h i))

/-- The standard form is sector additive. -/
theorem one_sectorAdditive : SectorAdditive (1 : Matrix (Fin n) (Fin n) GaussRat) := by
  intro u v h
  rw [hf_one, hf_one, hf_one, vnorm_add_of_disjoint h]

theorem vnorm_permute (σ : Equiv.Perm (Fin n)) (x : Fin n → GaussRat) :
    vnorm (permute σ x) = vnorm x := by
  unfold vnorm permute
  exact Equiv.sum_comp σ.symm (fun i => GaussRat.normSq (x i))

/-- The standard form is invariant under every sector permutation. -/
theorem one_invariant (σ : Equiv.Perm (Fin n)) :
    Invariant (1 : Matrix (Fin n) (Fin n) GaussRat) σ := by
  intro x
  rw [hf_one, hf_one, vnorm_permute]

theorem one_posdef (x : Fin n → GaussRat) (hx : x ≠ 0) :
    0 < hf (1 : Matrix (Fin n) (Fin n) GaussRat) x := by
  rw [hf_one]
  exact vnorm_pos hx

/-! ### Control: both directions are needed over ℚ(i) -/

/-- `[[1, i], [−i, 1]]`: Hermitian, additive on `(e₀, e₁)` along the real direction, not sector
additive. -/
def imagLeak12 : Matrix (Fin 2) (Fin 2) GaussRat :=
  Matrix.of ![![1, GaussRat.I], ![-GaussRat.I, 1]]

theorem imagLeak12_apply_00 : imagLeak12 0 0 = 1 := rfl
theorem imagLeak12_apply_01 : imagLeak12 0 1 = GaussRat.I := rfl
theorem imagLeak12_apply_10 : imagLeak12 1 0 = -GaussRat.I := rfl
theorem imagLeak12_apply_11 : imagLeak12 1 1 = 1 := rfl

theorem imagLeak12_hermitian : imagLeak12ᴴ = imagLeak12 := by
  refine Matrix.ext fun i j => ?_
  rw [Matrix.conjTranspose_apply]
  fin_cases i <;> fin_cases j <;>
    simp [imagLeak12, GaussRat.star_I, star_neg]

theorem imagLeak12_real_direction_additive :
    hf imagLeak12 (Pi.single 0 1 + Pi.single 1 1) =
      hf imagLeak12 (Pi.single 0 1) + hf imagLeak12 (Pi.single 1 1) := by
  rw [hf_single_add_single, imagLeak12_apply_01, imagLeak12_apply_10]
  simp

theorem imagLeak12_imag_direction_not_additive :
    hf imagLeak12 (Pi.single 0 1 + Pi.single 1 GaussRat.I) ≠
      hf imagLeak12 (Pi.single 0 1) + hf imagLeak12 (Pi.single 1 GaussRat.I) := by
  rw [hf_single_add_single, imagLeak12_apply_01, imagLeak12_apply_10, hf_single_one, hf_single,
    imagLeak12_apply_00, imagLeak12_apply_11]
  simp [GaussRat.star_I, GaussRat.normSq]
  norm_num

theorem imagLeak12_not_sectorAdditive : ¬ SectorAdditive imagLeak12 := by
  intro h
  exact imagLeak12_imag_direction_not_additive
    (h _ _ (disjoint_single_single (show (0 : Fin 2) ≠ 1 by decide) 1 GaussRat.I))

end InnerProductFinite.HermitianSectorForm

#print axioms InnerProductFinite.HermitianSectorForm.DisjointSupport
#print axioms InnerProductFinite.HermitianSectorForm.SectorAdditive
#print axioms InnerProductFinite.HermitianSectorForm.disjoint_single_single
#print axioms InnerProductFinite.HermitianSectorForm.cross_single
#print axioms InnerProductFinite.HermitianSectorForm.hf_single_add_single
#print axioms InnerProductFinite.HermitianSectorForm.offdiag_re_add_re
#print axioms InnerProductFinite.HermitianSectorForm.offdiag_im_sub_im
#print axioms InnerProductFinite.HermitianSectorForm.offdiag_eq_zero
#print axioms InnerProductFinite.HermitianSectorForm.permute
#print axioms InnerProductFinite.HermitianSectorForm.permute_single
#print axioms InnerProductFinite.HermitianSectorForm.Invariant
#print axioms InnerProductFinite.HermitianSectorForm.TransitiveOn
#print axioms InnerProductFinite.HermitianSectorForm.hf_single_one
#print axioms InnerProductFinite.HermitianSectorForm.diag_re_eq_of_invariant
#print axioms InnerProductFinite.HermitianSectorForm.diag_re_const_of_transitive
#print axioms InnerProductFinite.HermitianSectorForm.Generated
#print axioms InnerProductFinite.HermitianSectorForm.permute_one
#print axioms InnerProductFinite.HermitianSectorForm.permute_mul
#print axioms InnerProductFinite.HermitianSectorForm.permute_inv_left
#print axioms InnerProductFinite.HermitianSectorForm.permute_inv_right
#print axioms InnerProductFinite.HermitianSectorForm.invariant_one
#print axioms InnerProductFinite.HermitianSectorForm.invariant_mul
#print axioms InnerProductFinite.HermitianSectorForm.invariant_inv
#print axioms InnerProductFinite.HermitianSectorForm.invariant_of_generated
#print axioms InnerProductFinite.HermitianSectorForm.diag_eq_of_hermitian_transitive
#print axioms InnerProductFinite.HermitianSectorForm.eq_smul_one
#print axioms InnerProductFinite.HermitianSectorForm.eq_smul_one_generated
#print axioms InnerProductFinite.HermitianSectorForm.hf_eq_scale_vnorm
#print axioms InnerProductFinite.HermitianSectorForm.single_ne_zero
#print axioms InnerProductFinite.HermitianSectorForm.scale_pos
#print axioms InnerProductFinite.HermitianSectorForm.unique_of_normalized
#print axioms InnerProductFinite.HermitianSectorForm.eq_one_of_normalized
#print axioms InnerProductFinite.HermitianSectorForm.normSq_add_of_disjoint
#print axioms InnerProductFinite.HermitianSectorForm.vnorm_add_of_disjoint
#print axioms InnerProductFinite.HermitianSectorForm.one_sectorAdditive
#print axioms InnerProductFinite.HermitianSectorForm.vnorm_permute
#print axioms InnerProductFinite.HermitianSectorForm.one_invariant
#print axioms InnerProductFinite.HermitianSectorForm.one_posdef
#print axioms InnerProductFinite.HermitianSectorForm.imagLeak12
#print axioms InnerProductFinite.HermitianSectorForm.imagLeak12_apply_00
#print axioms InnerProductFinite.HermitianSectorForm.imagLeak12_apply_01
#print axioms InnerProductFinite.HermitianSectorForm.imagLeak12_apply_10
#print axioms InnerProductFinite.HermitianSectorForm.imagLeak12_apply_11
#print axioms InnerProductFinite.HermitianSectorForm.imagLeak12_hermitian
#print axioms InnerProductFinite.HermitianSectorForm.imagLeak12_real_direction_additive
#print axioms InnerProductFinite.HermitianSectorForm.imagLeak12_imag_direction_not_additive
#print axioms InnerProductFinite.HermitianSectorForm.imagLeak12_not_sectorAdditive
