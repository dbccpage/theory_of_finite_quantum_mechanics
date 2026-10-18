/-
  H007 -- complexification. AuthorityEffect: None. Candidate only.
  Not PROVEN. Kind: LIFT RUNG.

  Claim identifier: HW-H007
  Source-paper contact: QM_062 (U(1) selector, audited as proposal),
  QM_207 (complex phase fiber, audited as proposal). Work order hard
  obligation 6.

  Target proposition
    A complex-like structure (GaussInt = Z[i], with i*i = -1 and
    genuine conjugation) is AVAILABLE over the free module, and the
    real-like carrier Int embeds in it respecting the operations.
    Obligation 6: the entire H000-H006 pipeline already ran over
    Int with trivial conjugation, so the complex carrier has NOT
    been selected by anything below this rung.

  Imports added at this rung
    The carrier Z[i] itself. In this host R and C are unavailable
    (see the HWKernel Rat boundary receipt): Z[i] is the cheapest
    complex-like carrier the host supports choice-free, and taking
    it is an explicit import, not a derivation.

  Theorem or counterexample
    gi_squared: i * i = -1 in the imported carrier.
    embed_add / embed_mul / embed_conj: Int embeds respecting
    operations and (trivial) conjugation.
    real_pipeline_complete: re-export of the intPack instantiations
    of H004/H005/H006 punchline theorems -- the obligation 6 model.

  Nonclaim boundary
    No claim that Z[i], C, or any phase carrier is forced. No claim
    that Z[i] approximates C in any analytic sense: density and
    completeness are unavailable imports here.

  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
-/

import HWKernel
import H004FreeLinearization
import H005InnerProductAdmission
import H006PermutationUnitary

namespace FableHilbertWalk20260819.H007

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H004
open FableHilbertWalk20260819.H005 (sesq delta_orthonormal)
open FableHilbertWalk20260819.H006

/-- i * i = -1: the defining property of the imported unit. -/
theorem gi_squared :
    GaussInt.gmul GaussInt.gi GaussInt.gi =
      GaussInt.gneg GaussInt.gone :=
  GaussInt.gi_sq

#print axioms gi_squared

/-! ## The real-like carrier embeds. -/

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

/-- The imaginary unit lies outside the embedded real-like line:
    the complexification genuinely adds something. -/
theorem gi_not_embedded : ¬ ∃ a : Int, embed a = GaussInt.gi := by
  intro h
  rcases h with ⟨a, ha⟩
  have h1 : (embed a).im = GaussInt.gi.im := by rw [ha]
  simp [embed, GaussInt.gi] at h1

#print axioms gi_not_embedded

/-! ## Obligation 6: H000-H006 runs over the real-like carrier, so
    the complex import has not been selected by any earlier rung. -/

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

/-- H007 punchline: complex structure is available (i exists, i^2 =
    -1, the real line embeds) but not forced (the full pipeline
    below this rung runs real). -/
theorem complexification :
    (GaussInt.gmul GaussInt.gi GaussInt.gi =
      GaussInt.gneg GaussInt.gone) ∧
      (∀ a b : Int,
        embed (a * b) = GaussInt.gmul (embed a) (embed b)) ∧
      (¬ ∃ a : Int, embed a = GaussInt.gi) :=
  ⟨gi_squared, embed_mul, gi_not_embedded⟩

#print axioms complexification

end FableHilbertWalk20260819.H007
