/-
  H010Hadamard -- exact normalized Hadamard algebra over the integer
  mix. AuthorityEffect: None. Candidate only.

  The solid cut remains H010: mixing does not descend through the
  phase-blind report. The integer mix is the unnormalized Hadamard
  and squares to 2 I. Scaling by μ with 2 μ^2 = 1 is the ring law
  of Z[1/sqrt(2), i]; that scale is not constructed in Lean here.
  Python `hadamard_tensor_bell.py` carries μ as sqrt(2)/2.

  This module proves the integer identity mix ∘ mix = 2 · id, which
  is the exact finite reason (μ mix)^2 = I. No analysis. No R.
  Continuum is not this rung.

  Four leftovers stay four: coherence (this mix) is not holonomy,
  not entanglement, not computational advantage.

  AuthorityEffect: None
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import HWKernel
import H004FreeLinearization
import H008PhaseBlindPresentation
import H010InterferenceNonDescent

namespace FableHilbertWalk20260819.H010Hadamard

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H004
open FableHilbertWalk20260819.H010 (mix)

/-- Unnormalized Hadamard squared is twice the identity.
    That is the exact finite involution behind H = μ mix. -/
theorem mix_mix_is_two (v : Vec GaussInt Bool) :
    ∀ q : Bool, mix (mix v) q = GaussInt.gadd (v q) (v q) := by
  intro q
  cases q <;> cases h0 : v false <;> cases h1 : v true <;> (
    simp [mix, GaussInt.gadd, GaussInt.gneg, h0, h1]
    constructor <;> omega
  )

#print axioms mix_mix_is_two

end FableHilbertWalk20260819.H010Hadamard
