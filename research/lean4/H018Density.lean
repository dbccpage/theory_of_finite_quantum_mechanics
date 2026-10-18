



import HWKernel
import H004FreeLinearization
import H017MatrixFiniteRecovery

namespace FableHilbertWalk20260819.H018Density

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H004
open FableHilbertWalk20260819.H017Matrix

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

def bellAmp (p : Bool × Bool) : GaussInt :=
  if p.1 == p.2 then GaussInt.gone else GaussInt.gzero

def ketbra4 (w : Bool × Bool → GaussInt) :
    (Bool × Bool) → (Bool × Bool) → GaussInt :=
  fun p q => GaussInt.gmul (w p) (GaussInt.gconj (w q))

def ptrSecond (A : (Bool × Bool) → (Bool × Bool) → GaussInt) :
    Mat GaussInt :=
  fun i j =>
    GaussInt.gadd (A (i, false) (j, false)) (A (i, true) (j, true))

theorem bell_ptr_eq_ident :
    ptrSecond (ketbra4 bellAmp) = ident gaussPack := by
  funext i j
  cases i <;> cases j <;>
    simp [ptrSecond, ketbra4, bellAmp, ident, gaussPack,
      GaussInt.gmul, GaussInt.gconj, GaussInt.gadd, GaussInt.gone,
      GaussInt.gzero]

#print axioms bell_ptr_eq_ident

end FableHilbertWalk20260819.H018Density

private def l5aProvenance : String :=
  "Origin: lean4/H018Density.lean Claim: ketbra_adj AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
