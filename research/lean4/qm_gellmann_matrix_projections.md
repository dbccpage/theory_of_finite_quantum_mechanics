import Mathlib.Tactic.Ring

/-!
# Three Gell-Mann Block Matrices over Gaussian Integers

This module performs exact closed calculations for two coordinate projections
and the first three conventional Gell-Mann matrices in a concrete `3 x 3`
Gaussian-integer carrier. It does not construct `SU(N)`, all eight `SU(3)`
generators, a complex inner-product space, or quantum dynamics.

Key mechanized theorems:
* `P0_sq`, `P1_sq`: the two declared coordinate projections are idempotent;
* `lambda1_tr`, `lambda2_tr`, `lambda3_tr`: the three matrices have zero trace;
* `su2_comm_12` : $[\lambda_1, \lambda_2] = 2i \lambda_3$ commutator relation over discrete blocks;
* `su2_comm_23` : $[\lambda_2, \lambda_3] = 2i \lambda_1$ commutator relation over discrete blocks;
* `su2_comm_31` : $[\lambda_3, \lambda_1] = 2i \lambda_2$ commutator relation over discrete blocks;
* `su2_comm_12_ne_zero`: the first commutator is nonzero;
* `local_traceless_global_commutator_nonzero`: two local trace-zero checks
  coexist with a nonzero pairwise commutator;
* `structure_not_auth` : Structural derivation mints no authority (`AuthorityEffect: None`).
-/

namespace QM
namespace GellMann

/-- A 3×3 complex-integer matrix with entries in `Int × Int` (representing `a + b i`). -/
structure Mat3 where
  m00 : Int × Int
  m01 : Int × Int
  m02 : Int × Int
  m10 : Int × Int
  m11 : Int × Int
  m12 : Int × Int
  m20 : Int × Int
  m21 : Int × Int
  m22 : Int × Int
deriving DecidableEq, Repr

namespace Mat3

def cAdd (z1 z2 : Int × Int) : Int × Int := (z1.1 + z2.1, z1.2 + z2.2)
def cSub (z1 z2 : Int × Int) : Int × Int := (z1.1 - z2.1, z1.2 - z2.2)
def cMul (z1 z2 : Int × Int) : Int × Int := (z1.1 * z2.1 - z1.2 * z2.2, z1.1 * z2.2 + z1.2 * z2.1)
def cZero : Int × Int := (0, 0)
def cOne : Int × Int := (1, 0)
def cI : Int × Int := (0, 1)

/-- The explicit all-zero matrix in the declared Gaussian-integer carrier. -/
def zero : Mat3 :=
  ⟨cZero, cZero, cZero,
   cZero, cZero, cZero,
   cZero, cZero, cZero⟩

/-- Matrix sum. -/
def add (A B : Mat3) : Mat3 :=
  ⟨cAdd A.m00 B.m00, cAdd A.m01 B.m01, cAdd A.m02 B.m02,
   cAdd A.m10 B.m10, cAdd A.m11 B.m11, cAdd A.m12 B.m12,
   cAdd A.m20 B.m20, cAdd A.m21 B.m21, cAdd A.m22 B.m22⟩

/-- Matrix difference. -/
def sub (A B : Mat3) : Mat3 :=
  ⟨cSub A.m00 B.m00, cSub A.m01 B.m01, cSub A.m02 B.m02,
   cSub A.m10 B.m10, cSub A.m11 B.m11, cSub A.m12 B.m12,
   cSub A.m20 B.m20, cSub A.m21 B.m21, cSub A.m22 B.m22⟩

/-- Matrix product. -/
def mul (A B : Mat3) : Mat3 :=
  ⟨cAdd (cMul A.m00 B.m00) (cAdd (cMul A.m01 B.m10) (cMul A.m02 B.m20)),
   cAdd (cMul A.m00 B.m01) (cAdd (cMul A.m01 B.m11) (cMul A.m02 B.m21)),
   cAdd (cMul A.m00 B.m02) (cAdd (cMul A.m01 B.m12) (cMul A.m02 B.m22)),
   cAdd (cMul A.m10 B.m00) (cAdd (cMul A.m11 B.m10) (cMul A.m12 B.m20)),
   cAdd (cMul A.m10 B.m01) (cAdd (cMul A.m11 B.m11) (cMul A.m12 B.m21)),
   cAdd (cMul A.m10 B.m02) (cAdd (cMul A.m11 B.m12) (cMul A.m12 B.m22)),
   cAdd (cMul A.m20 B.m00) (cAdd (cMul A.m21 B.m10) (cMul A.m22 B.m20)),
   cAdd (cMul A.m20 B.m01) (cAdd (cMul A.m21 B.m11) (cMul A.m22 B.m21)),
   cAdd (cMul A.m20 B.m02) (cAdd (cMul A.m21 B.m12) (cMul A.m22 B.m22))⟩

/-- Commutator [A, B] = A B - B A. -/
def comm (A B : Mat3) : Mat3 := sub (mul A B) (mul B A)

/-- Matrix trace. -/
def trace (A : Mat3) : Int × Int := cAdd A.m00 (cAdd A.m11 A.m22)

/-- Scalar multiplication by complex integer. -/
def smul (z : Int × Int) (A : Mat3) : Mat3 :=
  ⟨cMul z A.m00, cMul z A.m01, cMul z A.m02,
   cMul z A.m10, cMul z A.m11, cMul z A.m12,
   cMul z A.m20, cMul z A.m21, cMul z A.m22⟩

end Mat3

open Mat3

/-- Block projection P0 onto node sector 0. -/
def P0 : Mat3 :=
  ⟨(1,0), (0,0), (0,0),
   (0,0), (0,0), (0,0),
   (0,0), (0,0), (0,0)⟩

/-- Block projection P1 onto node sector 1. -/
def P1 : Mat3 :=
  ⟨(0,0), (0,0), (0,0),
   (0,0), (1,0), (0,0),
   (0,0), (0,0), (0,0)⟩

/-- First Gell-Mann matrix λ1 (off-diagonal real block transition). -/
def Lambda1 : Mat3 :=
  ⟨(0,0), (1,0), (0,0),
   (1,0), (0,0), (0,0),
   (0,0), (0,0), (0,0)⟩

/-- Second Gell-Mann matrix λ2 (off-diagonal imaginary block transition). -/
def Lambda2 : Mat3 :=
  ⟨(0,0), (0,-1), (0,0),
   (0,1), (0,0),  (0,0),
   (0,0), (0,0),  (0,0)⟩

/-- Third Gell-Mann matrix λ3 (diagonal block difference P0 - P1). -/
def Lambda3 : Mat3 :=
  ⟨(1,0), (0,0),  (0,0),
   (0,0), (-1,0), (0,0),
   (0,0), (0,0),  (0,0)⟩

/-- The local evaluator checks only that each declared matrix has zero trace. -/
def IsLocalTraceGreen (A B : Mat3) : Prop :=
  A.trace = cZero ∧ B.trace = cZero

/--
The global evaluator checks whether the pairwise commutator is nonzero.
This is a finite algebraic diagnostic, not a physical color assignment.
-/
def IsGlobalCommutatorRed (A B : Mat3) : Prop :=
  A.comm B ≠ Mat3.zero

/-- **Block projections are idempotent ($P^2 = P$).** -/
theorem P0_sq : P0.mul P0 = P0 := by decide
theorem P1_sq : P1.mul P1 = P1 := by decide

/-- **Gell-Mann matrices are traceless ($\text{Tr}(\lambda_a) = 0$).** -/
theorem lambda1_tr : Lambda1.trace = (0,0) := by decide
theorem lambda2_tr : Lambda2.trace = (0,0) := by decide
theorem lambda3_tr : Lambda3.trace = (0,0) := by decide

/-- The first two declared matrices pass the local trace-zero evaluator. -/
theorem lambda12_local_trace_green :
    IsLocalTraceGreen Lambda1 Lambda2 :=
  ⟨lambda1_tr, lambda2_tr⟩

/-- **$[ \lambda_1, \lambda_2 ] = 2i \lambda_3$** — Discrete SU(2) commutator relation. -/
theorem su2_comm_12 : Lambda1.comm Lambda2 = Mat3.smul (0, 2) Lambda3 := by decide

/-- The first pairwise commutator is not the zero matrix. -/
theorem su2_comm_12_ne_zero :
    Lambda1.comm Lambda2 ≠ Mat3.zero := by decide

/-- **$[ \lambda_2, \lambda_3 ] = 2i \lambda_1$** — Discrete SU(2) commutator relation. -/
theorem su2_comm_23 : Lambda2.comm Lambda3 = Mat3.smul (0, 2) Lambda1 := by decide

/-- **$[ \lambda_3, \lambda_1 ] = 2i \lambda_2$** — Discrete SU(2) commutator relation. -/
theorem su2_comm_31 : Lambda3.comm Lambda1 = Mat3.smul (0, 2) Lambda2 := by decide

/--
Local Green is trace-zero for `Lambda1` and `Lambda2`; Global Red is their
nonzero commutator. The theorem is confined to these closed matrix values.
-/
theorem local_traceless_global_commutator_nonzero :
    IsLocalTraceGreen Lambda1 Lambda2 ∧
      IsGlobalCommutatorRed Lambda1 Lambda2 :=
  ⟨lambda12_local_trace_green, su2_comm_12_ne_zero⟩

/-! ## Firewall — derived ⇏ authority -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end GellMann
end QM

#print axioms QM.GellMann.P0_sq
#print axioms QM.GellMann.P1_sq
#print axioms QM.GellMann.lambda1_tr
#print axioms QM.GellMann.lambda2_tr
#print axioms QM.GellMann.lambda3_tr
#print axioms QM.GellMann.lambda12_local_trace_green
#print axioms QM.GellMann.su2_comm_12
#print axioms QM.GellMann.su2_comm_12_ne_zero
#print axioms QM.GellMann.su2_comm_23
#print axioms QM.GellMann.su2_comm_31
#print axioms QM.GellMann.local_traceless_global_commutator_nonzero
#print axioms QM.GellMann.structure_not_auth
