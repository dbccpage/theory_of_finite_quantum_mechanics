import «gomc_01_architecture»

/-!
# GOMC Terminal Authority

This module formalizes the Terminal Authority gate within the General Obstruction Management Calculus.
It proves that Authority (Terminalization / GTFDA Pi_sharp) cannot be constructed
from a mere diagnostic representation (such as a density matrix or branch ranking).
Authority requires finite descent closure.
-/

namespace GOMC

universe u v w z

open ObstructionCore

/--
Authority represents the terminal status of a node in the finite evaluator graph.
It is an independent coordinate from the diagnostic representation.
-/
structure TerminalAuthority {Alpha : Type u} {Authority : Type z} where
  readout : Alpha → Authority

/--
Terminal Authority is fundamentally decoupled from diagnostic representations.
If the terminal authority readout distinguishes two zero-equivalent representations,
then the Authority coordinate is globally red for that diagnostic representation.
-/
theorem authority_not_constructed_from_diagnostic
    {Alpha : Type u} {Beta : Type v} {Rho : Type w} {Authority : Type z}
    (P : PrimitiveDifference Alpha Beta)
    (rep : DiagnosticRepresentation P (Rho := Rho))
    (auth : TerminalAuthority (Alpha := Alpha) (Authority := Authority))
    (x y : Alpha)
    (h_zero : P.ZeroRel x y)
    (h_auth_neq : auth.readout x ≠ auth.readout y) :
    ¬ ∃ F : P.ResidualQuotient → Rho × Authority,
        ∀ a : Alpha, F (P.classOf a) = (rep.diagnostic a, auth.readout a) := by
  have h_nonfaithful : IsNonfaithful P rep auth.readout := ⟨x, y, h_zero, h_auth_neq⟩
  exact nonfaithful_implies_global_red P rep auth.readout h_nonfaithful

end GOMC
