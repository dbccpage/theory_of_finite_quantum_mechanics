/-
  H006 -- permutation "unitary" (work order rung name; what is
  proved is an ISOMETRY, see below). AuthorityEffect: None.
  Candidate only. Not PROVEN. Kind: LIFT RUNG.

  Claim identifier: HW-H006
  Source-paper contact: QM_121 rung "unitary dynamics"; work order
  hard obligation 1. H003 reversibility + H004 linearization + H005
  form are the inputs; each was a separate import.

  Target proposition
    A bijection of finite report states, linearly extended over an
    imported coefficient pack against the declared orthonormal
    basis, preserves the admitted sesquilinear form: the
    permutation-ISOMETRY envelope. This proves an ENVELOPE, not
    general unitary dynamics: the GaussInt/Bool fixture below has a
    concrete non-permutation isometry.

  Imports added at this rung
    Nothing new: this rung is the first PAYOFF rung. Its theorem
    consumes the H003 inverse, the H004 module, and the H005 form.

  Theorem or counterexample
    permutation_isometry (obligation 1, general): U_tau preserves
    sesq for every reversible tau, every pack, every enumeration --
    an isometry of a possibly-degenerate form, NOT a unitary.
    permU_left_inverse / permU_right_inverse: U_tau is invertible
    with form-preserving inverse (an isometric AUTOMORPHISM); the
    word "unitary" is earned only over a positive-definite host
    (permU_isometric_automorphism_over_posdef), and even there it is
    not a Hilbert unitary.
    permutation_on_basis: U_tau delta_q = delta_(tau q).
    swapI_isometry + swapI_not_permutation: over GaussInt, the map
    (u,v) -> (i*v, i*u) preserves the form but is NOT the linear
    extension of any report bijection: the envelope is strict.

  Nonclaim boundary
    Not all isometries arise from report dynamics: proved here, not
    just disclaimed. No continuous parameter (H016). No claim of
    quantum mechanics: this is linear algebra over an imported
    carrier.

    NAMING (adversarial-review response, 2026-08-19): "permutation
    unitary" is the WORK ORDER's rung name and is used only in that
    sense. What is proved in general (permutation_isometry) is
    form-preservation over an ARBITRARY *-module -- including
    degenerate ones: over F2 the same form is isotropic (H005
    f2_isotropic), so the general statement is an isometry of a
    possibly-degenerate form, NOT a unitary. The word "unitary" is
    earned only up to specialization: over the Int host the standard
    form is positive-definite (H005 gramStd_pos_def), and there
    permU is an isometric AUTOMORPHISM (isometry + two-sided
    inverse) -- theorem permU_isometric_automorphism_over_posdef
    below. Even that is NOT a Hilbert-space unitary: the carrier is
    a *-ring, not a field, and the finite-free host has no field /
    completeness structure that "unitary" proper presupposes. The
    honest ceiling is a finite pre-Hilbert isometric automorphism.

  AuthorityEffect: None
-/

import HWKernel
import H003ReversibilityGate
import H004FreeLinearization
import H005InnerProductAdmission

namespace FableHilbertWalk20260819.H006

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H003 (Reversible toggle toggleRev)
open FableHilbertWalk20260819.H004
open FableHilbertWalk20260819.H005 (sesq delta_orthonormal)

/-- Linear extension of a reversible report map: precomposition
    with the supplied inverse, so that U delta_q = delta_(tau q). -/
def permU {K Q : Type} (_ : StarRingPack K) {τ : Q → Q}
    (R : Reversible τ) (v : Vec K Q) : Vec K Q :=
  fun q => v (R.inv q)

/-- Obligation 1: a bijection of finite report states extends to a
    form-preserving operator once basis and form are supplied.
    General: any pack, any enumeration, any reversible tau. -/
theorem permutation_isometry {K Q : Type} (P : StarRingPack K)
    [DecidableEq Q] (E : Enum Q) {τ : Q → Q} (R : Reversible τ)
    (u v : Vec K Q) :
    sesq P E (permU P R u) (permU P R v) = sesq P E u v := by
  unfold sesq permU
  exact rsum_reindex P E R.right R.left
    (fun q => P.mul (P.conj (u q)) (v q))

#print axioms permutation_isometry

/-- Norm-squared preservation is the diagonal case. -/
theorem permutation_norm {K Q : Type} (P : StarRingPack K)
    [DecidableEq Q] (E : Enum Q) {τ : Q → Q} (R : Reversible τ)
    (v : Vec K Q) :
    sesq P E (permU P R v) (permU P R v) = sesq P E v v :=
  permutation_isometry P E R v v

#print axioms permutation_norm

/-- The reversed inverse pack: reversibility is symmetric. -/
def revInv {Q : Type} {τ : Q → Q} (R : Reversible τ) :
    Reversible R.inv where
  inv := τ
  left := R.right
  right := R.left

/-- U_tau is invertible: U_(tau^-1) undoes it pointwise. Together
    with permutation_isometry this gives a form-preserving
    AUTOMORPHISM (an isometry with a two-sided inverse) -- "unitary"
    only after specializing to a positive-definite host, see
    permU_isometric_automorphism_over_posdef. -/
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

/-- The extension acts on the basis as the report map: U delta_q =
    delta_(tau q). -/
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

/-! ## The envelope is strict on the GaussInt/Bool fixture: a
    non-permutation isometry exists. Refusal made into a theorem. -/

/-- Swap with a phase: (u_false, u_true) -> (i * u_true, i * u_false). -/
def swapI (v : Vec GaussInt Bool) : Vec GaussInt Bool :=
  fun q => GaussInt.gmul GaussInt.gi (v (!q))

/-- swapI preserves the standard form. -/
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

/-- swapI is not the linear extension of ANY report bijection:
    evaluating on delta_false exposes the coefficient i, which no
    permutation extension produces. The envelope is strict. -/
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

/-- Over the Int host with its positive-definite standard form
    (H005 gramStd_pos_def), permU is an isometric AUTOMORPHISM:
    form-preserving and two-sided invertible, preserving a form
    that is positive-definite. This is the strongest HONEST reading
    of "unitary" here -- and it is still NOT a Hilbert-space
    unitary (Int is a *-ring, not a field; no completeness). -/
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

/-- H006 punchline: the permutation-ISOMETRY envelope exists under
    explicit imports; over the GaussInt/Bool fixture it is strictly
    smaller than the isometry group. (Named "isometry envelope",
    not "unitary": the statement is form-preservation over a
    *-ring, degenerate forms included; "unitary" holds only up to
    the positive-definite-host specialization, see
    permU_isometric_automorphism_over_posdef.) -/
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
