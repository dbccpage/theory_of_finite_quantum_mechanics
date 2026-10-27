






import HWKernel
import ReversibilityGate
import FreeLinearization

namespace HilbertWalk.ContinuousDynamicsFork

open HilbertWalk.HWKernel
open HilbertWalk.ReversibilityGate (toggle)
open HilbertWalk.FreeLinearization

theorem no_report_half_step :
    ¬ ∃ σ : Bool → Bool, ∀ q : Bool, σ (σ q) = toggle q := by
  intro h
  rcases h with ⟨σ, hσ⟩
  cases hff : σ false with
  | false =>
      have h1 := hσ false
      rw [hff, hff] at h1
      cases h1
  | true =>
      cases hft : σ true with
      | false =>
          have h1 := hσ false
          rw [hff, hft] at h1
          cases h1
      | true =>
          have h1 := hσ true
          rw [hft, hft] at h1
          cases h1

#print axioms no_report_half_step


def ampSwap (v : Vec GaussInt Bool) : Vec GaussInt Bool :=
  fun q => v (!q)

def sqrtSwap (v : Vec GaussInt Bool) : Vec GaussInt Bool :=
  fun q =>
    GaussInt.gadd
      (GaussInt.gmul (if q then ⟨1, -1⟩ else ⟨1, 1⟩) (v false))
      (GaussInt.gmul (if q then ⟨1, 1⟩ else ⟨1, -1⟩) (v true))

def scale4 (v : Vec GaussInt Bool) : Vec GaussInt Bool :=
  fun q => GaussInt.gmul ⟨4, 0⟩ (v q)

theorem sqrtSwap_squares_to_scaled_swap (v : Vec GaussInt Bool) :
    ∀ q : Bool, sqrtSwap (sqrtSwap v) q = scale4 (ampSwap v) q := by
  intro q
  rcases hf : v false with ⟨af, bf⟩
  rcases ht : v true with ⟨at', bt⟩
  cases q <;>
    simp [sqrtSwap, scale4, ampSwap, hf, ht, GaussInt.gmul,
      GaussInt.gadd, Bool.not_false, Bool.not_true, if_true, if_false,
      GaussInt.mk.injEq] <;>
    constructor <;> omega

#print axioms sqrtSwap_squares_to_scaled_swap

def sqrtSwapNeg (v : Vec GaussInt Bool) : Vec GaussInt Bool :=
  fun q => GaussInt.gneg (sqrtSwap v q)

theorem sqrtSwapNeg_also_squares (v : Vec GaussInt Bool) :
    ∀ q : Bool, sqrtSwapNeg (sqrtSwapNeg v) q = scale4 (ampSwap v) q := by
  intro q
  rcases hf : v false with ⟨af, bf⟩
  rcases ht : v true with ⟨at', bt⟩
  cases q <;>
    simp [sqrtSwapNeg, sqrtSwap, scale4, ampSwap, hf, ht,
      GaussInt.gmul, GaussInt.gadd, GaussInt.gneg, Bool.not_false,
      Bool.not_true, if_true, if_false, GaussInt.mk.injEq] <;>
    constructor <;> omega

#print axioms sqrtSwapNeg_also_squares

theorem interpolant_not_unique :
    ¬(∀ v : Vec GaussInt Bool, ∀ q : Bool,
      sqrtSwap v q = sqrtSwapNeg v q) := by
  intro h
  have h1 := h (delta gaussPack false) false
  revert h1
  decide

#print axioms interpolant_not_unique

theorem continuous_dynamics_fork :
    (¬ ∃ σ : Bool → Bool, ∀ q : Bool, σ (σ q) = toggle q) ∧
      (∀ (v : Vec GaussInt Bool) (q : Bool),
        sqrtSwap (sqrtSwap v) q = scale4 (ampSwap v) q) ∧
      (∀ (v : Vec GaussInt Bool) (q : Bool),
        sqrtSwapNeg (sqrtSwapNeg v) q = scale4 (ampSwap v) q) ∧
      ¬(∀ v : Vec GaussInt Bool, ∀ q : Bool,
        sqrtSwap v q = sqrtSwapNeg v q) :=
  ⟨no_report_half_step,
    fun v q => sqrtSwap_squares_to_scaled_swap v q,
    fun v q => sqrtSwapNeg_also_squares v q,
    interpolant_not_unique⟩

#print axioms continuous_dynamics_fork

end HilbertWalk.ContinuousDynamicsFork

private def l5aProvenance : String :=
  "Origin: lean4/ContinuousDynamicsFork.lean Claim: no_report_half_step AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
