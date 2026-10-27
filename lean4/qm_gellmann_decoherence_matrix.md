import Mathlib.Tactic.Ring
import primitive_difference

/-!
# QMGellMannDecoherenceMatrix - Two-History Integer Residual

This module formalizes a static integer carrier
`(d11, d12, d22) : Int × Int × Int`. It does not formalize complex history
operators, Hermiticity, positive semidefiniteness, normalization, graph
cohomology, dynamics, or a continuum limit.

Key mechanized theorems:
* `decoherent_probability_additive`: the legacy additivity name for the
  zero-off-diagonal weight identity;
* `total_probability_minus_diagonal_eq_offdiagonal`: the legacy residual name;
* `offdiagonal_global_red`: the pure arithmetic nonzero-residual lemma;
* `local_green_global_residual`: nonnegative diagonal weights coexist with a
  nonzero global-minus-local residual;
* `offdiagonal_primitive_difference_nonzero`: the shared-kernel residual is
  nonzero when `d12` is nonzero;
* `decoherence_structure_not_auth`: the encoded structure mints no authority.
-/

namespace QM
namespace GellMann

/-- A two-history integer residual carrier. No matrix-analytic structure is
encoded by this record. -/
structure DecoherenceMatrix2x2 where
  d11 : Int
  d12 : Int
  d22 : Int
deriving DecidableEq, Repr

namespace DecoherenceMatrix2x2

/-- Local Green checks only the two diagonal integer weights. -/
def IsLocalGreen (D : DecoherenceMatrix2x2) : Prop :=
  D.d11 ≥ 0 ∧ D.d22 ≥ 0

/-- Compatibility alias for the original local predicate. -/
abbrev IsValid (D : DecoherenceMatrix2x2) : Prop :=
  IsLocalGreen D

/-- Global integer weight, including twice the off-diagonal coordinate. This
need not be nonnegative and is not declared to be a probability. -/
def globalWeight (D : DecoherenceMatrix2x2) : Int :=
  D.d11 + D.d22 + 2 * D.d12

/-- Compatibility alias for the original global-weight name. -/
abbrev totalProbability (D : DecoherenceMatrix2x2) : Int :=
  globalWeight D

/-- Locally visible diagonal integer weight. -/
def localDiagonalWeight (D : DecoherenceMatrix2x2) : Int :=
  D.d11 + D.d22

/-- Compatibility alias for the original diagonal-weight name. -/
abbrev diagonalSum (D : DecoherenceMatrix2x2) : Int :=
  localDiagonalWeight D

/-- The off-diagonal coordinate vanishes. -/
def IsDecoherent (D : DecoherenceMatrix2x2) : Prop :=
  D.d12 = 0

/-- Legacy additivity theorem: a zero off-diagonal coordinate removes the
global-minus-diagonal residual. -/
theorem decoherent_probability_additive (D : DecoherenceMatrix2x2)
    (h : IsDecoherent D) :
    totalProbability D = D.d11 + D.d22 := by
  dsimp [IsDecoherent] at h
  dsimp [totalProbability, globalWeight]
  rw [h]
  ring

/-- The canonical global-minus-local residual is twice the off-diagonal term. -/
theorem global_weight_sub_local_diagonal_eq_offdiagonal
    (D : DecoherenceMatrix2x2) :
    globalWeight D - localDiagonalWeight D = 2 * D.d12 := by
  dsimp [globalWeight, localDiagonalWeight]
  ring

/-- Compatibility theorem under the original names. -/
theorem total_probability_minus_diagonal_eq_offdiagonal
    (D : DecoherenceMatrix2x2) :
    totalProbability D - diagonalSum D = 2 * D.d12 := by
  exact global_weight_sub_local_diagonal_eq_offdiagonal D

/-- Pure arithmetic compatibility lemma: nonzero `d12` makes the global weight
different from the diagonal weight. The local hypothesis is not needed for
this implication. -/
theorem offdiagonal_global_red
    (D : DecoherenceMatrix2x2) (_hlocal : IsValid D) (h : D.d12 ≠ 0) :
    totalProbability D ≠ diagonalSum D := by
  dsimp [totalProbability, diagonalSum, globalWeight, localDiagonalWeight]
  omega

/-- Finite LGGR witness. Local diagonal nonnegativity coexists with a nonzero
global-minus-local residual. -/
theorem local_green_global_residual
    (D : DecoherenceMatrix2x2)
    (hlocal : IsLocalGreen D)
    (hoff : D.d12 ≠ 0) :
    0 ≤ localDiagonalWeight D ∧
      globalWeight D ≠ localDiagonalWeight D := by
  rcases hlocal with ⟨h11, h22⟩
  constructor
  · dsimp [localDiagonalWeight]
    omega
  · dsimp [globalWeight, localDiagonalWeight]
    omega

/-- The same off-diagonal witness as a shared Primitive Difference residual. -/
theorem offdiagonal_primitive_difference_nonzero
    (D : DecoherenceMatrix2x2) (h : D.d12 ≠ 0) :
    ObstructionCore.gellMannDecoherencePrimitiveDifference
        (totalProbability D) (diagonalSum D) ≠ 0 := by
  dsimp [totalProbability, diagonalSum, globalWeight, localDiagonalWeight]
  exact ObstructionCore.decoherence_nonzero_of_offdiagonal_weight D.d11 D.d12 D.d22 h

end DecoherenceMatrix2x2

/-! ## Firewall - derived does not imply authority -/

def IsDecoherenceAuth (_carrier : Type) : Prop := False

theorem decoherence_structure_not_auth (C : Type) : ¬ IsDecoherenceAuth C :=
  fun h => h

end GellMann
end QM

#print axioms QM.GellMann.DecoherenceMatrix2x2.decoherent_probability_additive
#print axioms QM.GellMann.DecoherenceMatrix2x2.global_weight_sub_local_diagonal_eq_offdiagonal
#print axioms QM.GellMann.DecoherenceMatrix2x2.total_probability_minus_diagonal_eq_offdiagonal
#print axioms QM.GellMann.DecoherenceMatrix2x2.offdiagonal_global_red
#print axioms QM.GellMann.DecoherenceMatrix2x2.local_green_global_residual
#print axioms QM.GellMann.DecoherenceMatrix2x2.offdiagonal_primitive_difference_nonzero
#print axioms QM.GellMann.decoherence_structure_not_auth
