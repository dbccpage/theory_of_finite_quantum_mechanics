






import HWKernel

namespace HilbertWalk.OperatorAlgebraShadow

open HilbertWalk.HWKernel

def Mat : Type := Bool → Bool → Int

def mmul (A B : Mat) : Mat :=
  fun i j => A i false * B false j + A i true * B true j

def nMat : Mat := fun i j => if !i && j then 1 else 0

def nMat' : Mat := fun i j => if i && !j then 1 else 0

theorem noncomm_witness :
    ¬(∀ i j : Bool, mmul nMat nMat' i j = mmul nMat' nMat i j) := by
  intro h
  have h1 := h false false
  revert h1
  decide

#print axioms noncomm_witness

def diag (d : Bool → Int) : Mat :=
  fun i j => if i == j then d i else 0

theorem diagonal_commutes (d e : Bool → Int) :
    ∀ i j : Bool, mmul (diag d) (diag e) i j = mmul (diag e) (diag d) i j := by
  intro i j
  cases i <;> cases j <;> simp [mmul, diag, Int.mul_comm]

#print axioms diagonal_commutes

theorem operator_algebra_shadow :
    ¬(∀ i j : Bool, mmul nMat nMat' i j = mmul nMat' nMat i j) ∧
      (∀ (d e : Bool → Int) (i j : Bool),
        mmul (diag d) (diag e) i j = mmul (diag e) (diag d) i j) :=
  ⟨noncomm_witness, fun d e i j => diagonal_commutes d e i j⟩

#print axioms operator_algebra_shadow

end HilbertWalk.OperatorAlgebraShadow

private def l5aProvenance : String :=
  "Origin: lean4/OperatorAlgebraShadow.lean Claim: noncomm_witness AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
