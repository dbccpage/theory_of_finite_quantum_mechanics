






import HWKernel
import H004FreeLinearization
import H005InnerProductAdmission
import H006PermutationUnitary

namespace FableHilbertWalk20260819.H007

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H004
open FableHilbertWalk20260819.H005 (sesq delta_orthonormal)
open FableHilbertWalk20260819.H006

theorem gi_squared :
    GaussInt.gmul GaussInt.gi GaussInt.gi =
      GaussInt.gneg GaussInt.gone :=
  GaussInt.gi_sq

#print axioms gi_squared


def embed (a : Int) : GaussInt := ⟨a, 0⟩

theorem embed_add (a b : Int) :
    embed (a + b) = GaussInt.gadd (embed a) (embed b) := by
  simp [embed, GaussInt.gadd]

theorem embed_mul (a b : Int) :
    embed (a * b) = GaussInt.gmul (embed a) (embed b) := by
  simp [embed, GaussInt.gmul]

theorem embed_conj (a : Int) :
    GaussInt.gconj (embed a) = embed a := by
  simp [embed, GaussInt.gconj]

#print axioms embed_mul

theorem gi_not_embedded : ¬ ∃ a : Int, embed a = GaussInt.gi := by
  intro h
  rcases h with ⟨a, ha⟩
  have h1 : (embed a).im = GaussInt.gi.im := by rw [ha]
  simp [embed, GaussInt.gi] at h1

#print axioms gi_not_embedded


theorem real_pipeline_complete :
    (∀ (v : Vec Int Bool) (x : Bool),
      rsum intPack (enumBool.elems.map
        (fun q => intPack.mul (v q) (delta intPack q x))) = v x) ∧
      (∀ a b : Bool,
        sesq intPack enumBool (delta intPack a) (delta intPack b) =
          if (a == b) = true then intPack.one else intPack.zero) ∧
      (∀ (u v : Vec Int Bool),
        sesq intPack enumBool
          (permU intPack FableHilbertWalk20260819.H003.toggleRev u)
          (permU intPack FableHilbertWalk20260819.H003.toggleRev v) =
        sesq intPack enumBool u v) :=
  ⟨fun v x => basis_expansion intPack enumBool v x,
    fun a b => delta_orthonormal intPack enumBool a b,
    fun u v => permutation_isometry intPack enumBool
      FableHilbertWalk20260819.H003.toggleRev u v⟩

#print axioms real_pipeline_complete

theorem complexification :
    (GaussInt.gmul GaussInt.gi GaussInt.gi =
      GaussInt.gneg GaussInt.gone) ∧
      (∀ a b : Int,
        embed (a * b) = GaussInt.gmul (embed a) (embed b)) ∧
      (¬ ∃ a : Int, embed a = GaussInt.gi) :=
  ⟨gi_squared, embed_mul, gi_not_embedded⟩

#print axioms complexification

end FableHilbertWalk20260819.H007

private def l5aProvenance : String :=
  "Origin: lean4/H007Complexification.lean Claim: gi_squared AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
