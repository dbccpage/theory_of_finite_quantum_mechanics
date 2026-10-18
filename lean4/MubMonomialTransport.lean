import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.Matrix.ConjTranspose
import Mathlib.Tactic.Ring

/-!
# Simultaneous transport of concrete quartet completions

AuthorityEffect: None.

All predicates below concern actual complex matrices. A common left monomial
action and independent right monomial actions preserve the raw Gram norm
equations. Thus single-matrix equivalence preserves completion by two further
raw Hadamard matrices. No classification or nonextension premise is proved.
-/

noncomputable section
namespace MUB.MonomialTransport
open scoped BigOperators

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

abbrev Mat (ι : Type*) := Matrix ι ι ℂ

def RawHadamard (H : Mat ι) : Prop :=
  (∀ i j, Complex.normSq (H i j) = 1) ∧
    H.conjTranspose * H = (Fintype.card ι : ℂ) • (1 : Mat ι)

def RawMU (H U : Mat ι) : Prop :=
  ∀ i j, Complex.normSq ((H.conjTranspose * U) i j) = (Fintype.card ι : ℝ)

/-- The identity and the three normalized raw matrices form the quartet. -/
def HasRawQuartet (H : Mat ι) : Prop :=
  RawHadamard H ∧ ∃ U V : Mat ι,
    RawHadamard U ∧ RawHadamard V ∧ RawMU H U ∧ RawMU H V ∧ RawMU U V

def action (H : Mat ι) (σ τ : Equiv.Perm ι) (r c : ι → ℂ) : Mat ι :=
  fun i j => r i * H (σ i) (τ j) * c j

def MonomialEquivalent (H K : Mat ι) : Prop :=
  ∃ (σ τ : Equiv.Perm ι) (r c : ι → ℂ),
    (∀ i, Complex.normSq (r i) = 1) ∧
    (∀ j, Complex.normSq (c j) = 1) ∧ K = action H σ τ r c

private theorem phase_cancel (z : ℂ) (hz : Complex.normSq z = 1) :
    star z * z = 1 := by
  simpa [Complex.star_def, Complex.normSq_eq_conj_mul_self] using
    congrArg (fun t : ℝ => (t : ℂ)) hz

omit [DecidableEq ι] in
/-- The row action must be common to both matrices; column actions may differ. -/
theorem action_gram (H U : Mat ι) (σ τ υ : Equiv.Perm ι)
    (r c d : ι → ℂ) (hr : ∀ i, Complex.normSq (r i) = 1) :
    (action H σ τ r c).conjTranspose * action U σ υ r d =
      fun i j => star (c i) * (H.conjTranspose * U) (τ i) (υ j) * d j := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.conjTranspose_apply, action]
  calc
    (∑ k, star (r k * H (σ k) (τ i) * c i) *
        (r k * U (σ k) (υ j) * d j)) =
        ∑ k, star (c i) * (star (H (σ k) (τ i)) * U (σ k) (υ j)) * d j := by
      apply Finset.sum_congr rfl
      intro k _
      rw [show star (r k * H (σ k) (τ i) * c i) *
          (r k * U (σ k) (υ j) * d j) =
          (star (r k) * r k) *
            (star (c i) * (star (H (σ k) (τ i)) * U (σ k) (υ j)) * d j) by
          simp only [star_mul]
          ring]
      rw [phase_cancel _ (hr k), one_mul]
    _ = star (c i) * (∑ k, star (H (σ k) (τ i)) * U (σ k) (υ j)) * d j := by
      rw [Finset.mul_sum, Finset.sum_mul]
    _ = star (c i) * (∑ k, star (H k (τ i)) * U k (υ j)) * d j := by
      rw [Equiv.sum_comp σ (fun k : ι => star (H k (τ i)) * U k (υ j))]

theorem action_hadamard (H : Mat ι) (σ τ : Equiv.Perm ι) (r c : ι → ℂ)
    (hr : ∀ i, Complex.normSq (r i) = 1)
    (hc : ∀ j, Complex.normSq (c j) = 1) (hH : RawHadamard H) :
    RawHadamard (action H σ τ r c) := by
  constructor
  · intro i j
    simp [action, Complex.normSq_mul, hr, hc, hH.1]
  · rw [action_gram H H σ τ τ r c c hr, hH.2]
    ext i j
    by_cases hij : i = j
    · subst j
      simp only [Matrix.smul_apply, Matrix.one_apply_eq, smul_eq_mul, mul_one]
      calc
        star (c i) * (Fintype.card ι : ℂ) * c i =
            (Fintype.card ι : ℂ) * (star (c i) * c i) := by ring
        _ = (Fintype.card ι : ℂ) := by rw [phase_cancel _ (hc i), mul_one]
    · have hτ : τ i ≠ τ j := fun h => hij (τ.injective h)
      simp [Matrix.smul_apply, hij, hτ]

omit [DecidableEq ι] in
theorem action_mu (H U : Mat ι) (σ τ υ : Equiv.Perm ι) (r c d : ι → ℂ)
    (hr : ∀ i, Complex.normSq (r i) = 1)
    (hc : ∀ j, Complex.normSq (c j) = 1)
    (hd : ∀ j, Complex.normSq (d j) = 1) (hHU : RawMU H U) :
    RawMU (action H σ τ r c) (action U σ υ r d) := by
  intro i j
  rw [action_gram H U σ τ υ r c d hr]
  simpa [Complex.normSq_mul, Complex.star_def, Complex.normSq_conj, hc, hd]
    using hHU (τ i) (υ j)

omit [Fintype ι] [DecidableEq ι] in
theorem monomialEquivalent_symm {H K : Mat ι} (h : MonomialEquivalent H K) :
    MonomialEquivalent K H := by
  rcases h with ⟨σ, τ, r, c, hr, hc, rfl⟩
  refine ⟨σ.symm, τ.symm, (fun i => star (r (σ.symm i))),
    (fun j => star (c (τ.symm j))), ?_, ?_, ?_⟩
  · intro i
    simpa [Complex.star_def, Complex.normSq_conj] using hr (σ.symm i)
  · intro j
    simpa [Complex.star_def, Complex.normSq_conj] using hc (τ.symm j)
  · ext i j
    simp only [action, Equiv.apply_symm_apply]
    symm
    calc
      star (r (σ.symm i)) * (r (σ.symm i) * H i j * c (τ.symm j)) *
          star (c (τ.symm j)) =
          (star (r (σ.symm i)) * r (σ.symm i)) * H i j *
            (star (c (τ.symm j)) * c (τ.symm j)) := by ring
      _ = H i j := by rw [phase_cancel _ (hr _), phase_cancel _ (hc _)]; simp

theorem hasRawQuartet_transport {H K : Mat ι} (hHK : MonomialEquivalent H K)
    (hH : HasRawQuartet H) : HasRawQuartet K := by
  rcases hHK with ⟨σ, τ, r, c, hr, hc, rfl⟩
  rcases hH with ⟨hH, U, V, hU, hV, hHU, hHV, hUV⟩
  have hone : ∀ i : ι, Complex.normSq (1 : ℂ) = 1 := by intro i; simp
  refine ⟨action_hadamard H σ τ r c hr hc hH,
    action U σ (Equiv.refl ι) r (fun _ => 1),
    action V σ (Equiv.refl ι) r (fun _ => 1),
    action_hadamard U _ _ _ _ hr hone hU,
    action_hadamard V _ _ _ _ hr hone hV,
    action_mu H U _ _ _ _ _ _ hr hc hone hHU,
    action_mu H V _ _ _ _ _ _ hr hc hone hHV,
    action_mu U V _ _ _ _ _ _ hr hone hone hUV⟩

theorem hasRawQuartet_iff_of_monomialEquivalent {H K : Mat ι}
    (hHK : MonomialEquivalent H K) : HasRawQuartet H ↔ HasRawQuartet K :=
  ⟨hasRawQuartet_transport hHK, hasRawQuartet_transport (monomialEquivalent_symm hHK)⟩

/-- A complete representative theorem can be used only together with actual exclusions. -/
theorem no_raw_quartet_of_complete_representatives (S : Set (Mat ι))
    (hcover : ∀ H, RawHadamard H → ∃ K ∈ S, MonomialEquivalent H K)
    (hexclude : ∀ K ∈ S, ¬ HasRawQuartet K) : ∀ H : Mat ι, ¬ HasRawQuartet H := by
  intro H hH
  obtain ⟨K, hKS, hHK⟩ := hcover H hH.1
  exact hexclude K hKS (hasRawQuartet_transport hHK hH)

#print axioms action_gram
#print axioms action_hadamard
#print axioms action_mu
#print axioms monomialEquivalent_symm
#print axioms hasRawQuartet_transport
#print axioms hasRawQuartet_iff_of_monomialEquivalent
#print axioms no_raw_quartet_of_complete_representatives
end MUB.MonomialTransport
