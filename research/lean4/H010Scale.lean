


import HWKernel
import H004FreeLinearization
import H008PhaseBlindPresentation
import H010InterferenceNonDescent

namespace FableHilbertWalk20260819.H010Scale

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H004 (Vec)
open FableHilbertWalk20260819.H008
open FableHilbertWalk20260819.H010

def nsq (z : GaussInt) : Int :=
  z.re * z.re + z.im * z.im

theorem phaseBlind_nsq (v : Vec GaussInt Bool) (q : Bool) :
    phaseBlind v q = nsq (v q) := by
  cases h : v q with
  | mk a b =>
      simp [phaseBlind, nsq, h, GaussInt.gmul, GaussInt.gconj,
        Int.sub_eq_add_neg, Int.neg_mul, Int.neg_neg]

#print axioms phaseBlind_nsq

theorem mix_false (v : Vec GaussInt Bool) :
    mix v false = GaussInt.gadd (v false) (v true) :=
  rfl

theorem mix_true (v : Vec GaussInt Bool) :
    mix v true = GaussInt.gadd (v false) (GaussInt.gneg (v true)) :=
  rfl

theorem nsq_parallelogram (z w : GaussInt) :
    nsq (GaussInt.gadd z w) + nsq (GaussInt.gadd z (GaussInt.gneg w)) =
      2 * (nsq z + nsq w) := by
  cases z with
  | mk a b =>
      cases w with
      | mk c d =>
          simp only [nsq, GaussInt.gadd, GaussInt.gneg,
            Int.mul_add, Int.add_mul, Int.mul_neg, Int.neg_neg,
            Int.mul_comm, Int.add_assoc, Int.add_comm,
            Int.add_left_comm]
          omega

#print axioms nsq_parallelogram

theorem rsum_two (f : Bool → Int) :
    rsum intPack (enumBool.elems.map f) =
      intPack.add (f false) (f true) := by
  simp [enumBool, rsum, List.map, intPack]

#print axioms rsum_two

theorem mix_doubles_total_any (v : Vec GaussInt Bool) :
    totalWeight enumBool (mix v) = 2 * totalWeight enumBool v := by
  unfold totalWeight
  rw [rsum_two (phaseBlind (mix v)), rsum_two (phaseBlind v)]
  change
    phaseBlind (mix v) false + phaseBlind (mix v) true =
      2 * (phaseBlind v false + phaseBlind v true)
  simp only [phaseBlind_nsq, mix_false, mix_true]
  exact nsq_parallelogram (v false) (v true)

#print axioms mix_doubles_total_any

theorem witnesses_are_the_special_case :
    totalWeight enumBool (mix psi1) = 2 * totalWeight enumBool psi1 ∧
      totalWeight enumBool (mix psi2) = 2 * totalWeight enumBool psi2 :=
  ⟨mix_doubles_total_any psi1, mix_doubles_total_any psi2⟩

#print axioms witnesses_are_the_special_case

end FableHilbertWalk20260819.H010Scale

private def l5aProvenance : String :=
  "Origin: lean4/H010Scale.lean Claim: phaseBlind_nsq AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
