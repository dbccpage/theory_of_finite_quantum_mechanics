

namespace FableHilbertWalk20260819.H040

def phiPlus  : List Int := [1, 0, 0, 1]
def psiPlus  : List Int := [0, 1, 1, 0]
def phiMinus : List Int := [1, 0, 0, -1]
def psiMinus : List Int := [0, 1, -1, 0]

def inner_prod (l1 l2 : List Int) : Int :=
  (List.zipWith (· * ·) l1 l2).foldl (· + ·) 0

theorem phi_plus_norm_sq : inner_prod phiPlus phiPlus = 2 := by decide

theorem psi_plus_norm_sq : inner_prod psiPlus psiPlus = 2 := by decide

theorem phi_minus_norm_sq : inner_prod phiMinus phiMinus = 2 := by decide

theorem psi_minus_norm_sq : inner_prod psiMinus psiMinus = 2 := by decide

theorem phiPlus_psiPlus_ortho : inner_prod phiPlus psiPlus = 0 := by decide

theorem phiPlus_phiMinus_ortho : inner_prod phiPlus phiMinus = 0 := by decide

theorem phiPlus_psiMinus_ortho : inner_prod phiPlus psiMinus = 0 := by decide

theorem psiPlus_phiMinus_ortho : inner_prod psiPlus phiMinus = 0 := by decide

theorem psiPlus_psiMinus_ortho : inner_prod psiPlus psiMinus = 0 := by decide

theorem phiMinus_psiMinus_ortho : inner_prod phiMinus psiMinus = 0 := by decide

structure Message2 where
  b1 : Int
  b0 : Int
  deriving DecidableEq, Repr

inductive BellState where
  | statePhiPlus
  | statePsiPlus
  | statePhiMinus
  | statePsiMinus
  deriving DecidableEq, Repr

def decodeBell : BellState → Message2
  | .statePhiPlus  => ⟨0, 0⟩
  | .statePsiPlus  => ⟨0, 1⟩
  | .statePhiMinus => ⟨1, 0⟩
  | .statePsiMinus => ⟨1, 1⟩

theorem messages_pairwise_distinct :
    decodeBell .statePhiPlus ≠ decodeBell .statePsiPlus ∧
    decodeBell .statePhiPlus ≠ decodeBell .statePhiMinus ∧
    decodeBell .statePhiPlus ≠ decodeBell .statePsiMinus ∧
    decodeBell .statePsiPlus ≠ decodeBell .statePhiMinus ∧
    decodeBell .statePsiPlus ≠ decodeBell .statePsiMinus ∧
    decodeBell .statePhiMinus ≠ decodeBell .statePsiMinus := by decide

theorem dense_coding_capacity : (2 : Int) ^ 2 = 4 := by decide

#print axioms phi_plus_norm_sq
#print axioms phiPlus_psiPlus_ortho
#print axioms phiPlus_phiMinus_ortho
#print axioms phiPlus_psiMinus_ortho
#print axioms psiPlus_phiMinus_ortho
#print axioms psiPlus_psiMinus_ortho
#print axioms phiMinus_psiMinus_ortho
#print axioms messages_pairwise_distinct
#print axioms dense_coding_capacity

end FableHilbertWalk20260819.H040

private def l5aProvenance : String :=
  "Origin: lean4/H040DiscreteSuperdenseCoding.lean Claim: phi_plus_norm_sq AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
