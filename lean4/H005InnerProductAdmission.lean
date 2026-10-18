/-
  H005 -- inner-product admission. AuthorityEffect: None. Candidate
  only. Not PROVEN. Kind: LIFT RUNG.

  Claim identifier: HW-H005
  Source-paper contact: QM_200 (inner product admission), QM_201
  (braket section). Audited as proposals, not authority.

  Target proposition
    A sesquilinear form with the report basis declared orthonormal
    is ADMITTED, not derived: two unequal Gram forms live on the
    same free module (so free linearization does not canonically
    supply one), and over F2 the standard form is degenerate (so
    positivity is a property of the coefficient import, not of the
    construction).

  Imports added at this rung
    The form itself: conjugation placement, basis orthonormality.
    Positivity holds at Int and GaussInt instantiations and FAILS
    at F2 -- it rides on the carrier import.

  Theorem or counterexample
    delta_orthonormal (general, any pack): the declared basis is
    orthonormal for the standard form.
    gram_not_unique + gramStd_pos_def + gramWeighted_pos_def: two
    positive-definite Grams on Bool -> Int (definiteness proved,
    not asserted) disagree on delta_true (work order countermodel).
    f2_isotropic: (1,1) is nonzero with zero self-pairing over F2.
    int_pos_semidef / gauss_self_real: positivity facts at the
    instantiations that support them.

  Nonclaim boundary
    No claim the standard form is canonical or unique. No claim
    positivity transfers to any other carrier. Adjoints and
    projections are downstream (H012), not established here.

  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import HWKernel
import H004FreeLinearization

namespace FableHilbertWalk20260819.H005

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H004

/-- The admitted sesquilinear form: conjugate-linear in the first
    slot by convention (a declared choice, not a theorem). -/
def sesq {K Q : Type} (P : StarRingPack K) (E : Enum Q)
    (u v : Vec K Q) : K :=
  rsum P (E.elems.map (fun q => P.mul (P.conj (u q)) (v q)))

/-- The declared report basis is orthonormal for the standard form:
    general over any pack and enumeration. -/
theorem delta_orthonormal {K Q : Type} (P : StarRingPack K)
    [DecidableEq Q] (E : Enum Q) (a b : Q) :
    sesq P E (delta P a) (delta P b) =
      if (a == b) = true then P.one else P.zero := by
  unfold sesq
  by_cases hab : a = b
  · subst hab
    rw [if_pos (beq_self_eq_true a)]
    have h : E.elems.map (fun q =>
        P.mul (P.conj (delta P a q)) (delta P a q)) =
        E.elems.map (fun q =>
          if (a == q) = true then P.one else P.zero) := by
      apply map_congr_mem
      intro q _
      unfold delta
      by_cases hq : a = q
      · subst hq
        rw [if_pos (beq_self_eq_true a), P.conj_one, P.one_mul]
      · rw [if_neg (fun h => hq (beq_iff_eq.mp h)), P.conj_zero,
          P.zero_mul]
    rw [h, rsum_map_delta P P.one (E.complete a) E.nodup]
  · rw [if_neg (fun h => hab (beq_iff_eq.mp h))]
    have h : E.elems.map (fun q =>
        P.mul (P.conj (delta P a q)) (delta P b q)) =
        E.elems.map (fun _ => P.zero) := by
      apply map_congr_mem
      intro q _
      unfold delta
      by_cases hqa : a = q
      · subst hqa
        rw [if_pos (beq_self_eq_true a),
          if_neg (fun h => hab (beq_iff_eq.mp h).symm),
          P.conj_one, P.one_mul]
      · rw [if_neg (fun h => hqa (beq_iff_eq.mp h)), P.conj_zero,
          P.zero_mul]
    rw [h, rsum_map_zero]

#print axioms delta_orthonormal

/-! ## Refusal 1: the Gram form is not canonical. Two unequal
    positive-definite forms on the same free module. -/

def gramStd (u v : Vec Int Bool) : Int :=
  sesq intPack enumBool u v

/-- A second positive-definite Gram: weight 2 on the true sector. -/
def gramWeighted (u v : Vec Int Bool) : Int :=
  u false * v false + 2 * (u true * v true)

theorem gram_not_unique :
    gramStd deltaTrueInt deltaTrueInt = 1 ∧
      gramWeighted deltaTrueInt deltaTrueInt = 2 ∧
      gramStd deltaTrueInt deltaTrueInt ≠
        gramWeighted deltaTrueInt deltaTrueInt := by
  refine ⟨by decide, by decide, by decide⟩

#print axioms gram_not_unique

/-! ## Refusal 2: positivity rides on the coefficient import.
    Over F2 the standard form is degenerate. -/

def oneOneF2 : Vec Bool Bool := fun _ => true

theorem f2_isotropic :
    sesq f2Pack enumBool oneOneF2 oneOneF2 = f2Pack.zero ∧
      ¬(∀ q : Bool, oneOneF2 q = f2Pack.zero) := by
  refine ⟨by decide, ?_⟩
  intro h
  have h1 := h true
  revert h1
  decide

#print axioms f2_isotropic

/-! ## Positivity where the carrier supports it. -/

/-- Squares are nonnegative in Int. Own proof: core lacks the name. -/
theorem int_sq_nonneg (a : Int) : 0 ≤ a * a := by
  rcases Int.le_total 0 a with h | h
  · exact Int.mul_nonneg h h
  · rw [← Int.neg_mul_neg]
    exact Int.mul_nonneg (Int.neg_nonneg.mpr h) (Int.neg_nonneg.mpr h)

theorem rsum_int_nonneg :
    ∀ {l : List Int}, (∀ a ∈ l, 0 ≤ a) → 0 ≤ rsum intPack l := by
  intro l
  induction l with
  | nil => intro _; exact Int.le_refl 0
  | cons a t ih =>
      intro h
      exact Int.add_nonneg (h a List.mem_cons_self)
        (ih (fun b hb => h b (List.mem_cons_of_mem a hb)))

/-- Positive semidefiniteness of the standard form over Int. -/
theorem int_pos_semidef {Q : Type} (E : Enum Q) (v : Vec Int Q) :
    0 ≤ sesq intPack E v v := by
  unfold sesq
  apply rsum_int_nonneg
  intro a ha
  rcases List.mem_map.mp ha with ⟨q, _, rfl⟩
  exact int_sq_nonneg (v q)

#print axioms int_pos_semidef

/-- Squares of nonzero integers are strictly positive. -/
theorem int_sq_pos {a : Int} (h : a ≠ 0) : 0 < a * a := by
  rcases Int.lt_trichotomy a 0 with hneg | hz | hpos
  · rw [← Int.neg_mul_neg]
    have hp : 0 < -a := Int.neg_pos.mpr hneg
    exact Int.mul_pos hp hp
  · exact absurd hz h
  · exact Int.mul_pos hpos hpos

/-- The standard Gram is positive-DEFINITE over Int, not just
    semidefinite: definiteness proved, not asserted. -/
theorem gramStd_pos_def (v : Vec Int Bool)
    (hv : ¬(∀ q : Bool, v q = 0)) : 0 < gramStd v v := by
  have hcase : v false ≠ 0 ∨ v true ≠ 0 := by
    by_cases hf : v false = 0
    · by_cases ht : v true = 0
      · exact absurd
          (fun q => match q with | false => hf | true => ht) hv
      · exact Or.inr ht
    · exact Or.inl hf
  show 0 < v false * v false + (v true * v true + 0)
  have h1 := int_sq_nonneg (v false)
  have h2 := int_sq_nonneg (v true)
  rcases hcase with h | h
  · have h3 := int_sq_pos h
    omega
  · have h3 := int_sq_pos h
    omega

#print axioms gramStd_pos_def

/-- The weighted rival Gram is also positive-definite. -/
theorem gramWeighted_pos_def (v : Vec Int Bool)
    (hv : ¬(∀ q : Bool, v q = 0)) : 0 < gramWeighted v v := by
  have hcase : v false ≠ 0 ∨ v true ≠ 0 := by
    by_cases hf : v false = 0
    · by_cases ht : v true = 0
      · exact absurd
          (fun q => match q with | false => hf | true => ht) hv
      · exact Or.inr ht
    · exact Or.inl hf
  show 0 < v false * v false + 2 * (v true * v true)
  have h1 := int_sq_nonneg (v false)
  have h2 := int_sq_nonneg (v true)
  rcases hcase with h | h
  · have h3 := int_sq_pos h
    omega
  · have h3 := int_sq_pos h
    omega

#print axioms gramWeighted_pos_def

/-- Componentwise: conj(x) * x is real with nonnegative real part
    in the Gaussian integers. -/
theorem gauss_self_real (x : GaussInt) :
    (GaussInt.gmul (GaussInt.gconj x) x).im = 0 ∧
      0 ≤ (GaussInt.gmul (GaussInt.gconj x) x).re := by
  cases x with
  | mk re im =>
      constructor
      · simp [GaussInt.gmul, GaussInt.gconj, Int.neg_mul,
          Int.mul_neg, Int.mul_comm]
        omega
      · simp [GaussInt.gmul, GaussInt.gconj, Int.neg_mul,
          Int.mul_neg, Int.sub_eq_add_neg, Int.neg_neg]
        have h1 : 0 ≤ re * re := int_sq_nonneg re
        have h2 : 0 ≤ im * im := int_sq_nonneg im
        omega

#print axioms gauss_self_real

/-- H005 punchline: orthonormality is declared and replays; the
    Gram is not unique; positivity is carrier-dependent. -/
theorem inner_product_admission :
    (sesq intPack enumBool deltaTrueInt deltaTrueInt = 1) ∧
      gramWeighted deltaTrueInt deltaTrueInt = 2 ∧
      (sesq f2Pack enumBool oneOneF2 oneOneF2 = f2Pack.zero ∧
        ¬(∀ q : Bool, oneOneF2 q = f2Pack.zero)) ∧
      (∀ v : Vec Int Bool, 0 ≤ sesq intPack enumBool v v) := by
  refine ⟨by decide, by decide, f2_isotropic,
    fun v => int_pos_semidef enumBool v⟩

#print axioms inner_product_admission

end FableHilbertWalk20260819.H005
