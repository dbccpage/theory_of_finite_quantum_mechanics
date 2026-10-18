/-
  H018Channel -- integer mixing conjugation vs its diagonal shadow.
  AuthorityEffect: None. Candidate only.

  QM_082: a stochastic kernel on the computational diagonal does
  not determine a channel. This module exhibits that on GaussInt,
  using the integer mix matrix of H010. CPTP remains imported
  (H017Finish.finish_cptp_imported). No uniqueness, no continuum.

  AuthorityEffect: None
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import HWKernel
import H004FreeLinearization
import H017MatrixFiniteRecovery
import H018Density

namespace FableHilbertWalk20260819.H018Channel

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H004 (delta)
open FableHilbertWalk20260819.H017Matrix
open FableHilbertWalk20260819.H018Density

/-- Integer mix matrix: rows (1,1) and (1,-1). -/
def mixMat : Mat GaussInt :=
  fun i j =>
    if i == false then GaussInt.gone
    else if j == false then GaussInt.gone
    else GaussInt.gneg GaussInt.gone

theorem mixMat_adj : adj gaussPack mixMat = mixMat := by
  funext i j
  cases i <;> cases j <;>
    simp [adj, mixMat, gaussPack, GaussInt.gconj, GaussInt.gneg, GaussInt.gone]

#print axioms mixMat_adj

def dephase (A : Mat GaussInt) : Mat GaussInt :=
  fun i j => if i == j then A i j else GaussInt.gzero

def conjMix (A : Mat GaussInt) : Mat GaussInt :=
  mmul gaussPack mixMat (mmul gaussPack A (adj gaussPack mixMat))

theorem conjMix_e00_ff : conjMix e00 false false = GaussInt.gone := by
  simp [conjMix, mixMat_adj, mmul, e00, ketbra, delta, mixMat, gaussPack, adj,
    GaussInt.gmul, GaussInt.gadd, GaussInt.gconj, GaussInt.gneg, GaussInt.gone,
    GaussInt.gzero]

#print axioms conjMix_e00_ff

theorem conjMix_e00_ft : conjMix e00 false true = GaussInt.gone := by
  simp [conjMix, mixMat_adj, mmul, e00, ketbra, delta, mixMat, gaussPack, adj,
    GaussInt.gmul, GaussInt.gadd, GaussInt.gconj, GaussInt.gneg, GaussInt.gone,
    GaussInt.gzero]

#print axioms conjMix_e00_ft

theorem conjMix_e00_tf : conjMix e00 true false = GaussInt.gone := by
  simp [conjMix, mixMat_adj, mmul, e00, ketbra, delta, mixMat, gaussPack, adj,
    GaussInt.gmul, GaussInt.gadd, GaussInt.gconj, GaussInt.gneg, GaussInt.gone,
    GaussInt.gzero]

#print axioms conjMix_e00_tf

theorem conjMix_e00_tt : conjMix e00 true true = GaussInt.gone := by
  simp [conjMix, mixMat_adj, mmul, e00, ketbra, delta, mixMat, gaussPack, adj,
    GaussInt.gmul, GaussInt.gadd, GaussInt.gconj, GaussInt.gneg, GaussInt.gone,
    GaussInt.gzero]

#print axioms conjMix_e00_tt

/-- Reading only the output diagonal of conjMix e00 recovers I.
    The full matrix is not I. Two maps that agree on that diagonal
    need not be the same channel. -/
theorem diagonal_shadow_does_not_fix_channel :
    dephase (conjMix e00) = ident gaussPack ∧
      conjMix e00 false true ≠ ident gaussPack false true := by
  constructor
  · funext i j
    cases i <;> cases j
    · simp [dephase, ident, gaussPack]; exact conjMix_e00_ff
    · simp [dephase, ident, gaussPack]
    · simp [dephase, ident, gaussPack]
    · simp [dephase, ident, gaussPack]; exact conjMix_e00_tt
  · rw [conjMix_e00_ft]
    simp [ident, gaussPack]
    decide

#print axioms diagonal_shadow_does_not_fix_channel

end FableHilbertWalk20260819.H018Channel
