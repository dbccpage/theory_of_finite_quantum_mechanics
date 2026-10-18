/-
  H012 -- operator-algebra host. AuthorityEffect: None. Candidate
  only. Not PROVEN. Kind: LIFT RUNG.

  Claim identifier: HW-H012
  Source-paper contact: QM_202 and QM_209 (audited as proposals).

  Target proposition
    A finite matrix host over the admitted module supports
    noncommuting operators, while the diagonal shadow -- the part
    visible to the phase-blind report layer -- is commutative.
    Noncommutativity is a property of the operator IMPORT, absent
    from the L1 simplex alone.

  Imports added at this rung
    Linear operators as matrices, composition, and the observable
    class. Adjoints and spectral structure are NOT constructed:
    they remain priced imports.

  Theorem or counterexample
    noncomm_witness: two nilpotent 2x2 integer matrices with
    NN' != N'N (finite, decide).
    diagonal_commutes: diagonal matrices commute (general theorem
    over any commutative pack carrier -- here Int).

  Nonclaim boundary
    No adjoint, no C*-structure, no spectral theorem: each is an
    import this rung does not supply. No claim that contextuality
    phenomena (QM_209 territory) are reached at this dimension.

  AuthorityEffect: None
-/

import HWKernel

namespace FableHilbertWalk20260819.H012

open FableHilbertWalk20260819.HWKernel

/-- 2x2 integer matrices indexed by Bool. -/
def Mat : Type := Bool → Bool → Int

/-- Matrix product over the Bool index set. -/
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

/-- Diagonal matrices: the operator shadow of the weight layer. -/
def diag (d : Bool → Int) : Mat :=
  fun i j => if i == j then d i else 0

/-- The diagonal shadow is commutative: general theorem. -/
theorem diagonal_commutes (d e : Bool → Int) :
    ∀ i j : Bool, mmul (diag d) (diag e) i j = mmul (diag e) (diag d) i j := by
  intro i j
  cases i <;> cases j <;> simp [mmul, diag, Int.mul_comm]

#print axioms diagonal_commutes

/-- H012 punchline: the operator host adds noncommutativity that
    the diagonal (report-visible) layer provably lacks. -/
theorem operator_algebra_shadow :
    ¬(∀ i j : Bool, mmul nMat nMat' i j = mmul nMat' nMat i j) ∧
      (∀ (d e : Bool → Int) (i j : Bool),
        mmul (diag d) (diag e) i j = mmul (diag e) (diag d) i j) :=
  ⟨noncomm_witness, fun d e i j => diagonal_commutes d e i j⟩

#print axioms operator_algebra_shadow

end FableHilbertWalk20260819.H012
