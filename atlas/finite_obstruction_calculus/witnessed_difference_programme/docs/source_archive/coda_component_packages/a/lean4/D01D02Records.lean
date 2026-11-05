/-!
# CODA-A D01/D02: Records for Typed Residual Closure & Anomalon Terminal

Formalizes:
1. Residual terminalization taxonomy (GTLA-01):
   `closureAbsorbed`, `closedResidual`, `openResidual`, `liftRequired`, `refusedClosure`.
2. Anomalon predicate: `IsAnomalon` holds strictly for `closedResidual`.
3. Disjoint global terminal type: `AuthEvidence` vs `ResidualTerminal`.
4. GTLA objects carrying independent residual closure and descent classifier readings.
5. Co-carrying representability and constructible pure-residual toy witness.

AuthorityEffect: None.
-/

namespace CodaA

set_option linter.unusedVariables false

/-- Authority terminal evidence produced by Omega_A finite descent. -/
structure AuthEvidence where
  packetId : String
  terminalizerId : String
  replayable : Bool := true
  deriving Repr, DecidableEq

/-- Living CODA-A 5-case residual taxonomy (GTLA-01). -/
inductive ResidualTerminal where
  | closureAbsorbed
  | closedResidual  -- The Anomalon Terminal
  | openResidual
  | liftRequired
  | refusedClosure
  deriving Repr, DecidableEq

/-- Anomalon is the ClosedResidual class, not the whole taxonomy. -/
def IsAnomalon : ResidualTerminal → Prop
  | .closedResidual => True
  | _ => False

/-- The global terminal type: authority evidence ⊕ residual taxonomy.
    Constructed disjoint: inl carries AuthEvidence, inr carries ResidualTerminal. -/
inductive Terminal where
  | auth (evidence : AuthEvidence)
  | residual (outcome : ResidualTerminal)
  deriving Repr, DecidableEq

/-- Authority predicate: terminal lies in the auth summand and carries replayable evidence. -/
def IsAuth : Terminal → Prop
  | .auth evidence => evidence.replayable = true
  | .residual _ => False

/-- Residual terminalizer output: lands in the disjoint residual summand. -/
def residualTerminal (r : ResidualTerminal) : Terminal := Terminal.residual r

/-- GTLA-14 / GTLA-03: No residual terminal is an authority terminal. -/
theorem residual_not_auth (r : ResidualTerminal) : ¬ IsAuth (residualTerminal r) := by
  intro h
  contradiction

/-- A GTLA object carries two independent readings:
    1. residualClosure: Option ResidualTerminal (none = absorbed, some r = residual exposed)
    2. descentClassifier: Terminal -/
structure GtlaObject where
  residualClosure : Option ResidualTerminal
  descentClassifier : Terminal
  deriving Repr

/-- Object exposes a residual. -/
def HasResidual (X : GtlaObject) : Prop := ∃ r, X.residualClosure = some r

/-- Object-level authority: descentClassifier lands in Auth. -/
def ObjAuth (X : GtlaObject) : Prop := IsAuth X.descentClassifier

/-- Independence is real: co-carrying (residue AND authority) is representable. -/
theorem coCarrying_representable : ∃ X : GtlaObject, HasResidual X ∧ ObjAuth X :=
  ⟨{ residualClosure := some .closedResidual
   , descentClassifier := Terminal.auth ⟨"p1", "tau1", true⟩ },
   ⟨.closedResidual, rfl⟩,
   rfl⟩

/-- Concrete pure-residual toy object: exposed residual with residual descent classifier. -/
def anomalonToy : GtlaObject :=
  { residualClosure := some .closedResidual
  , descentClassifier := residualTerminal .closedResidual }

theorem anomalonToy_hasResidual : HasResidual anomalonToy :=
  ⟨.closedResidual, rfl⟩

theorem anomalonToy_no_auth : ¬ ObjAuth anomalonToy :=
  residual_not_auth .closedResidual

end CodaA
