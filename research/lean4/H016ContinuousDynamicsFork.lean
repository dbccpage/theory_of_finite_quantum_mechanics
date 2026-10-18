/-
  H016 -- continuous dynamics fork. AuthorityEffect: None.
  Candidate only. Not PROVEN. Kind: IMPORT BOUNDARY.

  Claim identifier: HW-H016
  Source-paper contact: QM_211 (audited as proposal), QM_121
  continuum rung. Work order hard obligation 10.

  Target proposition
    Discrete reversible report dynamics has no preferred
    interpolation: the toggle has NO report-level half-step, while
    at the amplitude level (after the H007 complex import, at a
    disclosed integer scale) interpolants EXIST and are NOT unique.
    The continuum itself (topology, one-parameter group, Stone
    hypotheses) remains an unpriced import beyond this host.

  Imports added at this rung
    None taken. The rung prices what a continuous-time lift would
    require and shows the finite data does not determine it.

  Theorem or counterexample
    no_report_half_step: no sigma : Bool -> Bool with sigma o sigma
    = toggle (exhaustive, four cases).
    sqrtSwap_squares_to_scaled_swap: over Z[i], M with rows
    (1+i, 1-i) / (1-i, 1+i) satisfies M^2 = 4 * SWAP -- an
    amplitude-level interpolant at declared scale 4, available only
    AFTER the complex import.
    interpolant_not_unique: -M is a second distinct interpolant.

  Nonclaim boundary
    No topology, no continuity, no Hamiltonian: obligation 10 is
    answered by naming these as the exact assumptions a continuum
    passage needs. No claim that scale-4 interpolation is the
    physical normalization.

  AuthorityEffect: None
-/

import HWKernel
import H003ReversibilityGate
import H004FreeLinearization

namespace FableHilbertWalk20260819.H016

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H003 (toggle)
open FableHilbertWalk20260819.H004

/-- Obligation 10a: the toggle has no report-level square root.
    Exhaustive over the four endomaps of Bool. -/
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

/-! ## After the complex import: interpolants exist at a disclosed
    scale, and are not unique. -/

/-- Amplitude swap (the linearized toggle). -/
def ampSwap (v : Vec GaussInt Bool) : Vec GaussInt Bool :=
  fun q => v (!q)

/-- Scaled square root of swap over Z[i]: rows (1+i, 1-i) and
    (1-i, 1+i). -/
def sqrtSwap (v : Vec GaussInt Bool) : Vec GaussInt Bool :=
  fun q =>
    GaussInt.gadd
      (GaussInt.gmul (if q then ⟨1, -1⟩ else ⟨1, 1⟩) (v false))
      (GaussInt.gmul (if q then ⟨1, 1⟩ else ⟨1, -1⟩) (v true))

/-- Scale-4 multiplication. -/
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

/-- The negated interpolant. -/
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

/-- H016 punchline: no preferred interpolation exists at the report
    level; the complex import buys interpolants but not uniqueness;
    the continuum remains an unpriced import. -/
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

end FableHilbertWalk20260819.H016
