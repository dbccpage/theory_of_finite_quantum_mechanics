/-!
Lean 4 proof kernel for GTMUR-L02 / MUR-T6: Terminal Non-Bypass.

The point is deliberately small. A descent certificate may permit a transport
attempt, but target authority is a separate target-side terminalization witness
plus target-side `IsAuth`. This file proves the definitional projection and a
concrete countermodel to "χ alone implies authority", as well as an explicit
concrete transport countermodel where the commuting square is verified.

AuthorityEffect: None.
-/

namespace CODA_MUR

set_option linter.checkUnivs false

universe u v

/-- Minimal target-regime data needed for terminal non-bypass. -/
structure TerminalRegime where
  Rep : Type u
  Terminal : Type v
  terminalize : Rep -> Option Terminal
  IsAuth : Terminal -> Prop

/-- Target authority requires an accepted terminal representation. -/
def TargetAuthority (R : TerminalRegime) (x : R.Rep) : Prop :=
  ∃ t, R.terminalize x = some t ∧ R.IsAuth t

/-- GTMUR-L02: target authority unfolds to a target terminal plus `IsAuth`. -/
theorem targetAuthority_unfolds
    (B : TerminalRegime.{u, v}) (x : B.Rep) :
    TargetAuthority B x ↔
      ∃ t : B.Terminal, B.terminalize x = some t ∧ B.IsAuth t :=
  Iff.rfl

/-- A target authority proof contains target terminalization. -/
theorem targetAuthority_implies_terminalized
    (B : TerminalRegime.{u, v}) (x : B.Rep) :
    TargetAuthority B x -> ∃ t : B.Terminal, B.terminalize x = some t := by
  intro h
  rcases h with ⟨t, ht, _⟩
  exact ⟨t, ht⟩

/-- A target authority proof contains the target-side authority predicate. -/
theorem targetAuthority_implies_isAuth
    (B : TerminalRegime.{u, v}) (x : B.Rep) :
    TargetAuthority B x -> ∃ t : B.Terminal, B.IsAuth t := by
  intro h
  rcases h with ⟨t, _, ht⟩
  exact ⟨t, ht⟩

/-- A target regime where no representation terminalizes. -/
def noTerminalRegime : TerminalRegime where
  Rep := Unit
  Terminal := Unit
  terminalize := fun _ => none
  IsAuth := fun _ => True

/-- In the no-terminal regime, target authority cannot be inhabited. -/
theorem noTerminalRegime_no_authority :
    ¬ TargetAuthority noTerminalRegime () := by
  intro h
  rcases h with ⟨t, ht, _⟩
  cases ht

/--
There is no valid CODA_MUR rule saying "a descent certificate proposition χ alone
implies target authority". The countermodel has χ true but no target terminal.
-/
theorem chi_alone_does_not_imply_target_authority :
    ¬ (∀ (B : TerminalRegime.{0, 0}) (x : B.Rep) (χ : Prop),
        χ -> TargetAuthority B x) := by
  intro h
  exact noTerminalRegime_no_authority (h noTerminalRegime () True trivial)

/--
MUR-T6 concrete transport countermodel (`4.2):
A concrete commuting square (Bool -> Unit with p = id, q = id, states = const (), observations = const ())
commutes definitionally, yet target authority in noTerminalRegime is strictly uninhabited.
-/
theorem concrete_commuting_square_uninhabited_standing :
    (∀ x : Bool, (fun _ : Unit => ()) ((fun _ : Bool => ()) x) = (fun _ : Bool => ()) (id x)) ∧
    ¬ TargetAuthority noTerminalRegime () := by
  constructor
  · intro x; rfl
  · exact noTerminalRegime_no_authority

end CODA_MUR

#print axioms CODA_MUR.targetAuthority_unfolds
#print axioms CODA_MUR.targetAuthority_implies_terminalized
#print axioms CODA_MUR.targetAuthority_implies_isAuth
#print axioms CODA_MUR.noTerminalRegime_no_authority
#print axioms CODA_MUR.chi_alone_does_not_imply_target_authority
#print axioms CODA_MUR.concrete_commuting_square_uninhabited_standing
