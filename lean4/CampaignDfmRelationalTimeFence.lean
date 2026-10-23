import Mathlib.Tactic.NormNum

/-!
One order-4 rational step and its four clock blocks.

`step` is the real matrix `[[0, -1], [1, 0]]`. Each block
`(step^{t+1})^T step step^t` equals `I` for `t = 0, 1, 2, 3`.
No continuous-time generator is constructed.
-/

namespace CampaignDfmRelationalTimeFence

@[ext]
structure M2 where
  a00 : Rat
  a01 : Rat
  a10 : Rat
  a11 : Rat

@[ext]
structure V2 where
  x : Rat
  y : Rat

def mmul (A B : M2) : M2 where
  a00 := A.a00 * B.a00 + A.a01 * B.a10
  a01 := A.a00 * B.a01 + A.a01 * B.a11
  a10 := A.a10 * B.a00 + A.a11 * B.a10
  a11 := A.a10 * B.a01 + A.a11 * B.a11

def transp (A : M2) : M2 where
  a00 := A.a00
  a01 := A.a10
  a10 := A.a01
  a11 := A.a11

def apply (A : M2) (v : V2) : V2 where
  x := A.a00 * v.x + A.a01 * v.y
  y := A.a10 * v.x + A.a11 * v.y

def eye : M2 where
  a00 := 1
  a01 := 0
  a10 := 0
  a11 := 1

def minusEye : M2 where
  a00 := -1
  a01 := 0
  a10 := 0
  a11 := -1

def step : M2 where
  a00 := 0
  a01 := -1
  a10 := 1
  a11 := 0

def u0 : M2 := eye
def u1 : M2 := step
def u2 : M2 := mmul u1 step
def u3 : M2 := mmul u2 step
def u4 : M2 := mmul u3 step

def psi : V2 where
  x := 3 / 5
  y := 4 / 5

def block (tNext tCur : M2) : M2 := mmul (mmul (transp tNext) step) tCur

theorem step_square_and_order :
    u2 = minusEye ∧
    u4 = eye ∧
    mmul (transp step) step = eye := by
  refine ⟨?_, ?_, ?_⟩
  all_goals apply M2.ext
  all_goals simp only [u2, u4, u3, u1, mmul, transp, step, eye, minusEye]
  all_goals norm_num

theorem four_blocks :
    block u1 u0 = eye ∧
    block u2 u1 = eye ∧
    block u3 u2 = eye ∧
    block u4 u3 = eye := by
  refine ⟨?_, ?_, ?_, ?_⟩
  all_goals apply M2.ext
  all_goals simp only [block, u0, u1, u2, u3, u4, mmul, transp, step, eye]
  all_goals norm_num

theorem psi_recover :
    psi.x ^ 2 + psi.y ^ 2 = 1 ∧
    apply (transp u0) (apply u0 psi) = psi ∧
    apply (transp u1) (apply u1 psi) = psi ∧
    apply (transp u2) (apply u2 psi) = psi ∧
    apply (transp u3) (apply u3 psi) = psi ∧
    (apply u1 psi).x ≠ psi.x ∧
    (apply u2 psi).x ≠ psi.x := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · simp only [psi]; norm_num
  · apply V2.ext
    all_goals simp only [apply, transp, u0, eye, psi]
    all_goals norm_num
  · apply V2.ext
    all_goals simp only [apply, transp, u1, step, psi]
    all_goals norm_num
  · apply V2.ext
    all_goals simp only [apply, transp, u2, u1, mmul, step, psi]
    all_goals norm_num
  · apply V2.ext
    all_goals simp only [apply, transp, u3, u2, u1, mmul, step, psi]
    all_goals norm_num
  · simp only [apply, u1, step, psi]; norm_num
  · simp only [apply, u2, u1, mmul, step, psi]; norm_num

#print axioms CampaignDfmRelationalTimeFence.step_square_and_order
#print axioms CampaignDfmRelationalTimeFence.four_blocks
#print axioms CampaignDfmRelationalTimeFence.psi_recover

end CampaignDfmRelationalTimeFence
