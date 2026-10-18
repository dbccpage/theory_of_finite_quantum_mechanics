

namespace FableHilbertWalk20260819.H042

def dot_list (l1 l2 : List Int) : Int :=
  (List.zipWith (· * ·) l1 l2).foldl (· + ·) 0

def list_sum (l : List Int) : Int :=
  l.foldl (· + ·) 0

def pauli_phase (x1 z1 x2 z2 : List Int) : Int :=
  if (dot_list x1 z2 + dot_list z1 x2) % 2 = 0 then 1 else -1

def z_zero : List Int := [0, 0, 0, 0, 0, 0, 0, 0, 0]

def s1_z : List Int := [1, 1, 0, 0, 0, 0, 0, 0, 0]
def s2_z : List Int := [0, 1, 1, 0, 0, 0, 0, 0, 0]
def s3_z : List Int := [0, 0, 0, 1, 1, 0, 0, 0, 0]
def s4_z : List Int := [0, 0, 0, 0, 1, 1, 0, 0, 0]
def s5_z : List Int := [0, 0, 0, 0, 0, 0, 1, 1, 0]
def s6_z : List Int := [0, 0, 0, 0, 0, 0, 0, 1, 1]

def s7_x : List Int := [1, 1, 1, 1, 1, 1, 0, 0, 0]
def s8_x : List Int := [0, 0, 0, 1, 1, 1, 1, 1, 1]

def xl_x : List Int := [1, 1, 1, 1, 1, 1, 1, 1, 1]
def xl_z : List Int := z_zero

def zl_x : List Int := z_zero
def zl_z : List Int := [1, 0, 0, 1, 0, 0, 1, 0, 0]

def xl3_x : List Int := [1, 1, 1, 0, 0, 0, 0, 0, 0]
def xl3_z : List Int := z_zero

theorem zl_weight : list_sum zl_z = 3 := by decide

theorem xl3_weight : list_sum xl3_x = 3 := by decide

theorem s1_s7_commute : pauli_phase z_zero s1_z s7_x z_zero = 1 := by decide

theorem s1_s8_commute : pauli_phase z_zero s1_z s8_x z_zero = 1 := by decide

theorem s2_s7_commute : pauli_phase z_zero s2_z s7_x z_zero = 1 := by decide

theorem s2_s8_commute : pauli_phase z_zero s2_z s8_x z_zero = 1 := by decide

theorem s3_s7_commute : pauli_phase z_zero s3_z s7_x z_zero = 1 := by decide

theorem s3_s8_commute : pauli_phase z_zero s3_z s8_x z_zero = 1 := by decide

theorem s4_s7_commute : pauli_phase z_zero s4_z s7_x z_zero = 1 := by decide

theorem s4_s8_commute : pauli_phase z_zero s4_z s8_x z_zero = 1 := by decide

theorem s5_s7_commute : pauli_phase z_zero s5_z s7_x z_zero = 1 := by decide

theorem s5_s8_commute : pauli_phase z_zero s5_z s8_x z_zero = 1 := by decide

theorem s6_s7_commute : pauli_phase z_zero s6_z s7_x z_zero = 1 := by decide

theorem s6_s8_commute : pauli_phase z_zero s6_z s8_x z_zero = 1 := by decide

theorem s7_s8_commute : pauli_phase s7_x z_zero s8_x z_zero = 1 := by decide

theorem xl_commutes_with_stabilizers :
    pauli_phase xl_x xl_z z_zero s1_z = 1 ∧
    pauli_phase xl_x xl_z z_zero s2_z = 1 ∧
    pauli_phase xl_x xl_z z_zero s3_z = 1 ∧
    pauli_phase xl_x xl_z z_zero s4_z = 1 ∧
    pauli_phase xl_x xl_z z_zero s5_z = 1 ∧
    pauli_phase xl_x xl_z z_zero s6_z = 1 ∧
    pauli_phase xl_x xl_z s7_x z_zero = 1 ∧
    pauli_phase xl_x xl_z s8_x z_zero = 1 := by decide

theorem zl_commutes_with_stabilizers :
    pauli_phase zl_x zl_z z_zero s1_z = 1 ∧
    pauli_phase zl_x zl_z z_zero s2_z = 1 ∧
    pauli_phase zl_x zl_z z_zero s3_z = 1 ∧
    pauli_phase zl_x zl_z z_zero s4_z = 1 ∧
    pauli_phase zl_x zl_z z_zero s5_z = 1 ∧
    pauli_phase zl_x zl_z z_zero s6_z = 1 ∧
    pauli_phase zl_x zl_z s7_x z_zero = 1 ∧
    pauli_phase zl_x zl_z s8_x z_zero = 1 := by decide

theorem logical_operators_anticommute :
    pauli_phase xl_x xl_z zl_x zl_z = -1 := by decide

structure Syndrome8 where
  s1 : Int
  s2 : Int
  s3 : Int
  s4 : Int
  s5 : Int
  s6 : Int
  s7 : Int
  s8 : Int
  deriving DecidableEq, Repr

def trivialSyndrome : Syndrome8 := ⟨1, 1, 1, 1, 1, 1, 1, 1⟩

def evalSyndrome (ex ez : List Int) : Syndrome8 :=
  ⟨pauli_phase ex ez z_zero s1_z,
   pauli_phase ex ez z_zero s2_z,
   pauli_phase ex ez z_zero s3_z,
   pauli_phase ex ez z_zero s4_z,
   pauli_phase ex ez z_zero s5_z,
   pauli_phase ex ez z_zero s6_z,
   pauli_phase ex ez s7_x z_zero,
   pauli_phase ex ez s8_x z_zero⟩

def basis_vec (idx : Nat) : List Int :=
  List.map (fun i => if i = idx then 1 else 0) [0, 1, 2, 3, 4, 5, 6, 7, 8]

def x_err (i : Nat) : Syndrome8 := evalSyndrome (basis_vec i) z_zero
def z_err (i : Nat) : Syndrome8 := evalSyndrome z_zero (basis_vec i)
def y_err (i : Nat) : Syndrome8 := evalSyndrome (basis_vec i) (basis_vec i)

theorem all_x_errors_detected :
    x_err 0 ≠ trivialSyndrome ∧
    x_err 1 ≠ trivialSyndrome ∧
    x_err 2 ≠ trivialSyndrome ∧
    x_err 3 ≠ trivialSyndrome ∧
    x_err 4 ≠ trivialSyndrome ∧
    x_err 5 ≠ trivialSyndrome ∧
    x_err 6 ≠ trivialSyndrome ∧
    x_err 7 ≠ trivialSyndrome ∧
    x_err 8 ≠ trivialSyndrome := by decide

theorem all_z_errors_detected :
    z_err 0 ≠ trivialSyndrome ∧
    z_err 1 ≠ trivialSyndrome ∧
    z_err 2 ≠ trivialSyndrome ∧
    z_err 3 ≠ trivialSyndrome ∧
    z_err 4 ≠ trivialSyndrome ∧
    z_err 5 ≠ trivialSyndrome ∧
    z_err 6 ≠ trivialSyndrome ∧
    z_err 7 ≠ trivialSyndrome ∧
    z_err 8 ≠ trivialSyndrome := by decide

theorem all_y_errors_detected :
    y_err 0 ≠ trivialSyndrome ∧
    y_err 1 ≠ trivialSyndrome ∧
    y_err 2 ≠ trivialSyndrome ∧
    y_err 3 ≠ trivialSyndrome ∧
    y_err 4 ≠ trivialSyndrome ∧
    y_err 5 ≠ trivialSyndrome ∧
    y_err 6 ≠ trivialSyndrome ∧
    y_err 7 ≠ trivialSyndrome ∧
    y_err 8 ≠ trivialSyndrome := by decide

#print axioms zl_weight
#print axioms xl3_weight
#print axioms s1_s7_commute
#print axioms s1_s8_commute
#print axioms s7_s8_commute
#print axioms xl_commutes_with_stabilizers
#print axioms zl_commutes_with_stabilizers
#print axioms logical_operators_anticommute
#print axioms all_x_errors_detected
#print axioms all_z_errors_detected
#print axioms all_y_errors_detected

end FableHilbertWalk20260819.H042


theorem falsification_degenerate_carrier : ¬ (1 = 0) := by
  decide

private def l5aProvenance : String :=
  "Origin: lean4/H042ShorNineQubitCode.lean Claim: zl_weight AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
