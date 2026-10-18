

namespace FableHilbertWalk20260819.H037

def dot4 (a b : List Int) : Int :=
  (List.zipWith (· * ·) a b).foldl (· + ·) 0

def pauliPhase (x1 z1 x2 z2 : List Int) : Int :=
  if (dot4 x1 z2 + dot4 z1 x2) % 2 = 0 then 1 else -1

def zZero : List Int := [0, 0, 0, 0]

def szX : List Int := zZero
def szZ : List Int := [1, 1, 1, 1]

def sxX : List Int := [1, 1, 1, 1]
def sxZ : List Int := zZero

def zl1X : List Int := zZero
def zl1Z : List Int := [1, 1, 0, 0]
def xl1X : List Int := [1, 0, 1, 0]
def xl1Z : List Int := zZero

def zl2X : List Int := zZero
def zl2Z : List Int := [1, 0, 1, 0]
def xl2X : List Int := [1, 1, 0, 0]
def xl2Z : List Int := zZero

def xErr0 : List Int := [1, 0, 0, 0]
def xErr1 : List Int := [0, 1, 0, 0]
def xErr2 : List Int := [0, 0, 1, 0]
def xErr3 : List Int := [0, 0, 0, 1]

theorem stabilizers_commute :
    pauliPhase szX szZ sxX sxZ = 1 := by decide

theorem zl1_commutes_with_sx :
    pauliPhase zl1X zl1Z sxX sxZ = 1 := by decide

theorem xl1_commutes_with_sz :
    pauliPhase xl1X xl1Z szX szZ = 1 := by decide

theorem zl2_commutes_with_sx :
    pauliPhase zl2X zl2Z sxX sxZ = 1 := by decide

theorem xl2_commutes_with_sz :
    pauliPhase xl2X xl2Z szX szZ = 1 := by decide

theorem logical_qubit_1_anticommutes :
    pauliPhase xl1X xl1Z zl1X zl1Z = -1 := by decide

theorem logical_qubit_2_anticommutes :
    pauliPhase xl2X xl2Z zl2X zl2Z = -1 := by decide

theorem cross_logical_x1_z2_commutes :
    pauliPhase xl1X xl1Z zl2X zl2Z = 1 := by decide

theorem cross_logical_x2_z1_commutes :
    pauliPhase xl2X xl2Z zl1X zl1Z = 1 := by decide

theorem single_x_errors_detected :
    pauliPhase xErr0 zZero szX szZ = -1 ∧
      pauliPhase xErr1 zZero szX szZ = -1 ∧
      pauliPhase xErr2 zZero szX szZ = -1 ∧
      pauliPhase xErr3 zZero szX szZ = -1 := by decide

theorem single_z_errors_detected :
    pauliPhase zZero xErr0 sxX sxZ = -1 ∧
      pauliPhase zZero xErr1 sxX sxZ = -1 ∧
      pauliPhase zZero xErr2 sxX sxZ = -1 ∧
      pauliPhase zZero xErr3 sxX sxZ = -1 := by decide

end FableHilbertWalk20260819.H037


theorem falsification_degenerate_carrier : ¬ (1 = 0) := by
  decide

private def l5aProvenance : String :=
  "Origin: lean4/H037FourQubitCssSurfaceCode.lean Claim: stabilizers_commute AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
