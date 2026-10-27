import Mathlib.Tactic.NormNum

/-!
Two quadratic forms for one diagonal matrix in the Gribov fence.

`H23` and `H12` are the symmetric generators with a single off-diagonal pair.
The forms `Tr(Ω1 H^2)` on those generators are `-2` and `0`. No continuum
operator is constructed.
-/

namespace DressingFieldGribovContinuumFence

@[ext]
structure M3 where
  a00 : Rat
  a01 : Rat
  a02 : Rat
  a10 : Rat
  a11 : Rat
  a12 : Rat
  a20 : Rat
  a21 : Rat
  a22 : Rat

def mul (A B : M3) : M3 where
  a00 := A.a00 * B.a00 + A.a01 * B.a10 + A.a02 * B.a20
  a01 := A.a00 * B.a01 + A.a01 * B.a11 + A.a02 * B.a21
  a02 := A.a00 * B.a02 + A.a01 * B.a12 + A.a02 * B.a22
  a10 := A.a10 * B.a00 + A.a11 * B.a10 + A.a12 * B.a20
  a11 := A.a10 * B.a01 + A.a11 * B.a11 + A.a12 * B.a21
  a12 := A.a10 * B.a02 + A.a11 * B.a12 + A.a12 * B.a22
  a20 := A.a20 * B.a00 + A.a21 * B.a10 + A.a22 * B.a20
  a21 := A.a20 * B.a01 + A.a21 * B.a11 + A.a22 * B.a21
  a22 := A.a20 * B.a02 + A.a21 * B.a12 + A.a22 * B.a22

def trace (A : M3) : Rat := A.a00 + A.a11 + A.a22

def diag (x y z : Rat) : M3 where
  a00 := x
  a01 := 0
  a02 := 0
  a10 := 0
  a11 := y
  a12 := 0
  a20 := 0
  a21 := 0
  a22 := z

def eye : M3 := diag 1 1 1
def omega1 : M3 := diag 1 (-1) (-1)
def h23 : M3 where
  a00 := 0
  a01 := 0
  a02 := 0
  a10 := 0
  a11 := 0
  a12 := 1
  a20 := 0
  a21 := 1
  a22 := 0
def h12 : M3 where
  a00 := 0
  a01 := 1
  a02 := 0
  a10 := 1
  a11 := 0
  a12 := 0
  a20 := 0
  a21 := 0
  a22 := 0

theorem h23_square : mul h23 h23 = diag 0 1 1 := by
  apply M3.ext
  all_goals simp only [mul, h23, diag]
  all_goals norm_num

theorem h12_square : mul h12 h12 = diag 1 1 0 := by
  apply M3.ext
  all_goals simp only [mul, h12, diag]
  all_goals norm_num

theorem omega1_square_and_det :
    mul omega1 omega1 = eye ∧
    omega1.a00 * omega1.a11 * omega1.a22 = 1 ∧
    trace eye = 3 ∧
    trace omega1 = -1 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · apply M3.ext
    all_goals simp only [mul, omega1, eye, diag]
    all_goals norm_num
  · simp only [omega1, diag]; norm_num
  · simp only [trace, eye, diag]; norm_num
  · simp only [trace, omega1, diag]; norm_num

theorem trace_pair :
    trace (mul eye (mul h23 h23)) = 2 ∧
    trace (mul omega1 (mul h23 h23)) = -2 ∧
    trace (mul omega1 (mul h12 h12)) = 0 := by
  refine ⟨?_, ?_, ?_⟩
  all_goals simp only [trace, mul, eye, omega1, h23, h12, diag]
  all_goals norm_num

theorem forms_differ :
    trace (mul omega1 (mul h23 h23)) ≠ trace (mul omega1 (mul h12 h12)) := by
  simp only [trace, mul, omega1, h23, h12, diag]
  norm_num

#print axioms DressingFieldGribovContinuumFence.h23_square
#print axioms DressingFieldGribovContinuumFence.h12_square
#print axioms DressingFieldGribovContinuumFence.omega1_square_and_det
#print axioms DressingFieldGribovContinuumFence.trace_pair
#print axioms DressingFieldGribovContinuumFence.forms_differ

end DressingFieldGribovContinuumFence
