







import HWKernel
import H003ReversibilityGate
import H004FreeLinearization
import H005InnerProductAdmission

namespace FableHilbertWalk20260819.H006

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H003 (Reversible toggle toggleRev)
open FableHilbertWalk20260819.H004
open FableHilbertWalk20260819.H005 (sesq delta_orthonormal)

def permU {K Q : Type} (_ : StarRingPack K) {τ : Q → Q}
    (R : Reversible τ) (v : Vec K Q) : Vec K Q :=
  fun q => v (R.inv q)

theorem permutation_isometry {K Q : Type} (P : StarRingPack K)
    [DecidableEq Q] (E : Enum Q) {τ : Q → Q} (R : Reversible τ)
    (u v : Vec K Q) :
    sesq P E (permU P R u) (permU P R v) = sesq P E u v := by
  unfold sesq permU
  exact rsum_reindex P E R.right R.left
    (fun q => P.mul (P.conj (u q)) (v q))

#print axioms permutation_isometry

theorem permutation_norm {K Q : Type} (P : StarRingPack K)
    [DecidableEq Q] (E : Enum Q) {τ : Q → Q} (R : Reversible τ)
    (v : Vec K Q) :
    sesq P E (permU P R v) (permU P R v) = sesq P E v v :=
  permutation_isometry P E R v v

#print axioms permutation_norm

def revInv {Q : Type} {τ : Q → Q} (R : Reversible τ) :
    Reversible R.inv where
  inv := τ
  left := R.right
  right := R.left

theorem permU_left_inverse {K Q : Type} (P : StarRingPack K)
    {τ : Q → Q} (R : Reversible τ) (v : Vec K Q) :
    permU P (revInv R) (permU P R v) = v := by
  funext q
  show v (R.inv (τ q)) = v q
  rw [R.left]

theorem permU_right_inverse {K Q : Type} (P : StarRingPack K)
    {τ : Q → Q} (R : Reversible τ) (v : Vec K Q) :
    permU P R (permU P (revInv R) v) = v := by
  funext q
  show v (τ (R.inv q)) = v q
  rw [R.right]

#print axioms permU_left_inverse
#print axioms permU_right_inverse

theorem permutation_on_basis {K Q : Type} (P : StarRingPack K)
    [DecidableEq Q] {τ : Q → Q} (R : Reversible τ) (q x : Q) :
    permU P R (delta P q) x = delta P (τ q) x := by
  unfold permU delta
  by_cases hx : x = τ q
  · subst hx
    rw [if_pos (by rw [R.left q]; exact beq_self_eq_true q),
      if_pos (beq_self_eq_true (τ q))]
  · have h1 : ¬((q == R.inv x) = true) := by
      intro h
      exact hx (by rw [← R.right x, ← beq_iff_eq.mp h])
    have h2 : ¬((τ q == x) = true) := by
      intro h
      exact hx (beq_iff_eq.mp h).symm
    rw [if_neg h1, if_neg h2]

#print axioms permutation_on_basis


def swapI (v : Vec GaussInt Bool) : Vec GaussInt Bool :=
  fun q => GaussInt.gmul GaussInt.gi (v (!q))

theorem swapI_isometry (u v : Vec GaussInt Bool) :
    sesq gaussPack enumBool (swapI u) (swapI v) =
      sesq gaussPack enumBool u v := by
  unfold sesq swapI
  show gaussPack.add
      (gaussPack.mul (gaussPack.conj (GaussInt.gmul GaussInt.gi (u true)))
        (GaussInt.gmul GaussInt.gi (v true)))
      (gaussPack.add
        (gaussPack.mul (gaussPack.conj (GaussInt.gmul GaussInt.gi (u false)))
          (GaussInt.gmul GaussInt.gi (v false)))
        gaussPack.zero) =
    gaussPack.add
      (gaussPack.mul (gaussPack.conj (u false)) (v false))
      (gaussPack.add
        (gaussPack.mul (gaussPack.conj (u true)) (v true))
        gaussPack.zero)
  have key : ∀ a b : GaussInt,
      gaussPack.mul (gaussPack.conj (GaussInt.gmul GaussInt.gi a))
        (GaussInt.gmul GaussInt.gi b) =
      gaussPack.mul (gaussPack.conj a) b := by
    intro a b
    cases a with
    | mk ar ai =>
        cases b with
        | mk br bi =>
            show GaussInt.gmul
                (GaussInt.gconj (GaussInt.gmul GaussInt.gi ⟨ar, ai⟩))
                (GaussInt.gmul GaussInt.gi ⟨br, bi⟩) =
              GaussInt.gmul (GaussInt.gconj ⟨ar, ai⟩) ⟨br, bi⟩
            simp only [GaussInt.gmul, GaussInt.gconj, GaussInt.gi,
              Int.neg_mul, Int.mul_neg, Int.neg_neg,
              Int.sub_eq_add_neg, Int.neg_add, Int.zero_mul,
              Int.mul_zero, Int.zero_add, Int.add_zero,
              Int.mul_comm, Int.one_mul, Int.mul_one,
              GaussInt.mk.injEq]
            exact ⟨Int.add_comm _ _, Int.add_comm _ _⟩
  rw [key (u true) (v true), key (u false) (v false),
    gaussPack.add_zero, gaussPack.add_zero, gaussPack.add_comm]

#print axioms swapI_isometry

theorem swapI_not_permutation :
    ¬ ∃ (τ : Bool → Bool) (R : Reversible τ),
      ∀ v : Vec GaussInt Bool, swapI v = permU gaussPack R v := by
  intro h
  rcases h with ⟨τ, R, hall⟩
  have h1 := congrFun (hall (delta gaussPack false)) (τ false)
  rw [permutation_on_basis gaussPack R false (τ false)] at h1
  have h2 : delta gaussPack (τ false) (τ false) = GaussInt.gone := by
    unfold delta
    rw [if_pos (beq_self_eq_true (τ false))]
    rfl
  rw [h2] at h1
  unfold swapI delta at h1
  by_cases hb : (false == !(τ false)) = true
  · rw [if_pos hb] at h1
    exact absurd h1 (by decide)
  · rw [if_neg hb] at h1
    exact absurd h1 (by decide)

#print axioms swapI_not_permutation

theorem permU_isometric_automorphism_over_posdef
    {τ : Bool → Bool} (R : Reversible τ) :
    (∀ u v : Vec Int Bool,
      sesq intPack enumBool (permU intPack R u) (permU intPack R v) =
        sesq intPack enumBool u v) ∧
      (∀ v : Vec Int Bool,
        permU intPack (revInv R) (permU intPack R v) = v) ∧
      (∀ v : Vec Int Bool,
        permU intPack R (permU intPack (revInv R) v) = v) ∧
      (∀ v : Vec Int Bool, ¬(∀ q : Bool, v q = 0) →
        0 < sesq intPack enumBool v v) :=
  ⟨fun u v => permutation_isometry intPack enumBool R u v,
    fun v => permU_left_inverse intPack R v,
    fun v => permU_right_inverse intPack R v,
    fun v hv => FableHilbertWalk20260819.H005.gramStd_pos_def v hv⟩

#print axioms permU_isometric_automorphism_over_posdef

theorem permutation_isometry_envelope :
    (∀ (u v : Vec Int Bool),
      sesq intPack enumBool (permU intPack toggleRev u)
        (permU intPack toggleRev v) = sesq intPack enumBool u v) ∧
      (∀ (u v : Vec GaussInt Bool),
        sesq gaussPack enumBool (swapI u) (swapI v) =
          sesq gaussPack enumBool u v) ∧
      ¬ ∃ (τ : Bool → Bool) (R : Reversible τ),
        ∀ v : Vec GaussInt Bool, swapI v = permU gaussPack R v :=
  ⟨fun u v => permutation_isometry intPack enumBool toggleRev u v,
    swapI_isometry, swapI_not_permutation⟩

#print axioms permutation_isometry_envelope

end FableHilbertWalk20260819.H006

private def l5aProvenance : String :=
  "Origin: lean4/H006PermutationUnitary.lean Claim: permutation_isometry AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
