/-
  H018Density -- unnormalized projectors and the Bell partial trace.
  AuthorityEffect: None. Candidate only.

  After H010Hadamard the finite host still has no 1/2 in Lean.
  This module stays on GaussInt. The scale μ = 1/sqrt(2) and the
  normalized I/2 mixed state live in the Python ring of GOM_023.
  What is proved here: the integer Bell projector, after tracing
  the second factor, is the 2x2 identity. That is mixedness as a
  leftover of entanglement, without a density-matrix postulate
  and without M_n(C).

  Coherence is off-diagonal data. The partial-trace identity is
  diagonal. Those are not the same leftover.

  AuthorityEffect: None
-/

import HWKernel
import H004FreeLinearization
import H017MatrixFiniteRecovery

namespace FableHilbertWalk20260819.H018Density

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H004
open FableHilbertWalk20260819.H017Matrix

/-- Unnormalized |v⟩⟨v| on the two-label GaussInt module. -/
def ketbra (v : Vec GaussInt Bool) : Mat GaussInt :=
  fun i j => GaussInt.gmul (v i) (GaussInt.gconj (v j))

theorem ketbra_adj (v : Vec GaussInt Bool) :
    adj gaussPack (ketbra v) = ketbra v := by
  funext i j
  simp [adj, ketbra, gaussPack]
  have h := GaussInt.gconj_mul (v j) (GaussInt.gconj (v i))
  rw [h, GaussInt.gconj_conj]
  exact GaussInt.gmul_comm _ _

#print axioms ketbra_adj

def e00 : Mat GaussInt := ketbra (delta gaussPack false)

theorem e00_is_computational_projector :
    e00 false false = GaussInt.gone ∧
      e00 true true = GaussInt.gzero ∧
      e00 false true = GaussInt.gzero ∧
      e00 true false = GaussInt.gzero := by
  simp [e00, ketbra, delta, gaussPack]
  decide

#print axioms e00_is_computational_projector

/-- Integer Bell amplitude on Bool × Bool: 1 on the diagonal, 0 off. -/
def bellAmp (p : Bool × Bool) : GaussInt :=
  if p.1 == p.2 then GaussInt.gone else GaussInt.gzero

def ketbra4 (w : Bool × Bool → GaussInt) :
    (Bool × Bool) → (Bool × Bool) → GaussInt :=
  fun p q => GaussInt.gmul (w p) (GaussInt.gconj (w q))

/-- Partial trace of the second Bool factor. -/
def ptrSecond (A : (Bool × Bool) → (Bool × Bool) → GaussInt) :
    Mat GaussInt :=
  fun i j =>
    GaussInt.gadd (A (i, false) (j, false)) (A (i, true) (j, true))

/-- Tracing the second factor of the integer Bell projector yields
    the 2×2 identity: unnormalized I, the mixed leftover. -/
theorem bell_ptr_eq_ident :
    ptrSecond (ketbra4 bellAmp) = ident gaussPack := by
  funext i j
  cases i <;> cases j <;>
    simp [ptrSecond, ketbra4, bellAmp, ident, gaussPack,
      GaussInt.gmul, GaussInt.gconj, GaussInt.gadd, GaussInt.gone,
      GaussInt.gzero]

#print axioms bell_ptr_eq_ident

end FableHilbertWalk20260819.H018Density
