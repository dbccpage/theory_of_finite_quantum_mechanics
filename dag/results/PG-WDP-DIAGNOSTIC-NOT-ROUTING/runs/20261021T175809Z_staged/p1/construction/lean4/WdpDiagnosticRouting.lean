import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Pi
import Mathlib.Data.Fintype.Prod
import Mathlib.Data.Fintype.Perm
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Data.Fintype.CardEmbedding

/-!
# Diagnostic class, routing terminal and authority are different axes (WDP-CH04-N01)

AuthorityEffect: None.  Scope: transcription of the finite enumerations and total maps of the_symbol_game
`omega_types/src/routing.rs` (RoutingTerminal, TerminalStatus -> RoutingTerminal, PfpTerminal -> RoutingTerminal),
`omega_types/src/terminal_status.rs` (TerminalStatus, ResidualClass, the authority tag, `terminal_from_fiber`),
`omega_policy/src/trichotomy.rs` (ObstructionDiagnosticClass; the Rust variant for the exact class is named
`ExactRepair`, the ledger calls it `ExactClass`), `omega_id_run/src/run.rs` lines 626-633 (emits a status-tag STRING per
diagnostic class), `omega_certifiers/src/checked_packet.rs` line 248 (an eligibility gate: only the exact class can seal a
checked-packet certificate, which keeps AuthorityEffect None) and a re-transcription of external WitnessedDifference/Routing.lean
(`RelativeStatus`, `route`, a FOURTH axis with Bool inputs that is not the 7-valued routing terminal; copies, not the external
theorems).  The enumerations are hand transcriptions shared by Lean, producer and checker.
No source code composes the run.rs tag with the PfpTerminal map (omega_id_run never references terminal_routing or PfpTerminal): `diagRoute`
is OUR composition by string identity, and the tag "ExactRepair" is not a key of terminal_routing.json, so the exact class has no route
by this composition (`runTag .ExactClass = none` encodes "tag is not a Pfp" by definition).
Identification of `terminal_status::ResidualClass` with the diagnostic class is NOT made here (a second, unrelated Rust enum
`omega_homology::...::ResidualClass` {ExactRepair, StabilizedSurvivor, OpenObstruction} has the diagnostic class's three values and is not modelled).
`AuthTag` has no `Certified` constructor, so "tag never Certified" is true BY CONSTRUCTION of the modelled type; `Situation.authority` and
`Situation.terminal` are defined from (status, witness) only, so `diag_cannot_set_*` hold by construction of the model (`rfl`); the only link
from the class to authority is the eligibility gate `sealed`.  The policy theorems are cardinality facts about maps from any 3-set to any 7-set.
`exactRepairAllowed` is the same predicate as `certEligible`: the ledger clause "ExactClass is not ExactRepair" has no anchor of its own here.
-/

namespace WdpDiagnosticRouting

inductive DiagClass where
  | ExactClass | ClosedResidual | ActiveClosureFailure
  deriving DecidableEq, Repr

inductive Routing where
  | CheckPassed | RequiresLift | Repair | Refusal | NoRule | BudgetUnknown | Refused
  deriving DecidableEq, Repr

inductive Residual where
  | Exact | ClosedSurvivor | Open | Refused
  deriving DecidableEq, Repr

inductive AuthTag where
  | Certifiable | Refused | Uncertified
  deriving DecidableEq, Repr

inductive RelStatus where
  | supported | refuted | outsideProfile | undetermined
  deriving DecidableEq, Repr

inductive Pfp where
  | Exact | Verified | VerifiedWithResiduals | StabilizedSurvivor | NeedsExternalOracle
  | OpenObstruction | BlockedByEvidence | InfrastructureFailure | Refused | BudgetExhausted
  deriving DecidableEq, Repr

inductive TermStatus where
  | ExactRuleDerived | UniqueOutputDerived | NoRuleInSearchClass | NonUniqueOutput | EnumeratorFailure
  | Refused | LabelConflictsWithDerivation | BudgetUnknown | InvalidProposal | OperatorConflict
  | UnknownSector | NoDescentYet | LabelOnlyUncertified | LiftRequired | ParseRefused
  | ReplayMismatch | PolicyAmbiguous | NoPacket | VerifierDisabled | SearchIncomplete | PolicyUnderspecified
  deriving DecidableEq, Repr

/-- Literal enumerations (the derive handler is not used). -/
instance : Fintype DiagClass := ⟨{.ExactClass, .ClosedResidual, .ActiveClosureFailure}, fun x => by cases x <;> simp⟩
instance : Fintype Routing :=
  ⟨{.CheckPassed, .RequiresLift, .Repair, .Refusal, .NoRule, .BudgetUnknown, .Refused}, fun x => by cases x <;> simp⟩
instance : Fintype Residual := ⟨{.Exact, .ClosedSurvivor, .Open, .Refused}, fun x => by cases x <;> simp⟩
instance : Fintype AuthTag := ⟨{.Certifiable, .Refused, .Uncertified}, fun x => by cases x <;> simp⟩
instance : Fintype RelStatus := ⟨{.supported, .refuted, .outsideProfile, .undetermined}, fun x => by cases x <;> simp⟩
instance : Fintype Pfp :=
  ⟨{.Exact, .Verified, .VerifiedWithResiduals, .StabilizedSurvivor, .NeedsExternalOracle, .OpenObstruction,
    .BlockedByEvidence, .InfrastructureFailure, .Refused, .BudgetExhausted}, fun x => by cases x <;> simp⟩
instance : Fintype TermStatus :=
  ⟨{.ExactRuleDerived, .UniqueOutputDerived, .NoRuleInSearchClass, .NonUniqueOutput, .EnumeratorFailure, .Refused,
    .LabelConflictsWithDerivation, .BudgetUnknown, .InvalidProposal, .OperatorConflict, .UnknownSector, .NoDescentYet,
    .LabelOnlyUncertified, .LiftRequired, .ParseRefused, .ReplayMismatch, .PolicyAmbiguous, .NoPacket, .VerifierDisabled,
    .SearchIncomplete, .PolicyUnderspecified}, fun x => by cases x <;> simp⟩

open DiagClass Routing

/-- routing.rs `From<TerminalStatus> for RoutingTerminal`. -/
def routeStatus : TermStatus → Routing
  | .ExactRuleDerived => .CheckPassed
  | .UniqueOutputDerived => .CheckPassed
  | .NoRuleInSearchClass => .NoRule
  | .NonUniqueOutput => .Repair
  | .EnumeratorFailure => .Repair
  | .Refused => .Refused
  | .LabelConflictsWithDerivation => .Refused
  | .BudgetUnknown => .BudgetUnknown
  | .InvalidProposal => .Refused
  | .OperatorConflict => .Refused
  | .UnknownSector => .Repair
  | .NoDescentYet => .Repair
  | .LabelOnlyUncertified => .Repair
  | .LiftRequired => .RequiresLift
  | .ParseRefused => .Refusal
  | .ReplayMismatch => .Repair
  | .PolicyAmbiguous => .Repair
  | .NoPacket => .Refusal
  | .VerifierDisabled => .Repair
  | .SearchIncomplete => .Repair
  | .PolicyUnderspecified => .Repair

/-- routing.rs `From<PfpTerminal> for RoutingTerminal` (equal to terminal_routing.json). -/
def routePfp : Pfp → Routing
  | .Exact => .CheckPassed
  | .Verified => .CheckPassed
  | .VerifiedWithResiduals => .CheckPassed
  | .StabilizedSurvivor => .RequiresLift
  | .NeedsExternalOracle => .RequiresLift
  | .OpenObstruction => .Refusal
  | .BlockedByEvidence => .Refusal
  | .InfrastructureFailure => .Refusal
  | .Refused => .Refused
  | .BudgetExhausted => .BudgetUnknown

/-- terminal_status.rs `TerminalStatus::residual_class`. -/
def residualOf : TermStatus → Residual
  | .ExactRuleDerived => .Exact
  | .UniqueOutputDerived => .Exact
  | .NoRuleInSearchClass => .ClosedSurvivor
  | .Refused => .Refused
  | .LabelConflictsWithDerivation => .Refused
  | .InvalidProposal => .Refused
  | .OperatorConflict => .Refused
  | .ParseRefused => .Refused
  | _ => .Open

/-- terminal_status.rs `authority_level` below `Certified`; the type has no `Certified` value, so tag-level never-certified holds by construction. -/
def authTag : TermStatus → AuthTag
  | .ExactRuleDerived => .Certifiable
  | .UniqueOutputDerived => .Certifiable
  | .Refused => .Refused
  | .LabelConflictsWithDerivation => .Refused
  | .InvalidProposal => .Refused
  | .OperatorConflict => .Refused
  | _ => .Uncertified

/-- terminal_status.rs `authority_terminal().is_some()`. -/
def authTerminal : TermStatus → Bool
  | .ExactRuleDerived => true
  | .UniqueOutputDerived => true
  | _ => false

/-- External Routing.lean `route`: a different axis with Bool inputs. -/
def relRoute (inProfile contradicted supported : Bool) : RelStatus :=
  match inProfile, contradicted, supported with
  | false, _, _ => .outsideProfile
  | true, true, _ => .refuted
  | true, false, true => .supported
  | true, false, false => .undetermined

/-- terminal_status.rs `terminal_from_fiber`; `none` is an `Err`. `agr = none` defaults to (true, true). -/
def fiberStatus (selected : Bool) (cand out : Nat) (exh : Bool) (agr : Option (Bool × Bool)) (verifier : Bool) :
    Option TermStatus :=
  if selected = false then
    (if cand ≠ 0 ∨ out ≠ 0 ∨ exh = true then none else some .NoPacket)
  else if verifier = false then some .VerifierDisabled
  else if 0 < cand ∧ out = 0 then none
  else if cand < out then none
  else if cand = 0 then some (if exh = true then .NoRuleInSearchClass else .SearchIncomplete)
  else if cand = 1 then some .ExactRuleDerived
  else if out = 1 then
    (if (agr.getD (true, true)).1 = false then some .PolicyAmbiguous
     else if (agr.getD (true, true)).2 = false then some .ReplayMismatch
     else some .UniqueOutputDerived)
  else some .NonUniqueOutput

/-- run.rs 626-633 emits a status-tag string per class; the exact class emits "ExactRepair", which is not a `Pfp` (encoded as `none` by definition). -/
def runTag : DiagClass → Option Pfp
  | .ExactClass => none
  | .ClosedResidual => some .StabilizedSurvivor
  | .ActiveClosureFailure => some .OpenObstruction

/-- OUR composition by string identity of the run.rs tag with the PfpTerminal map (no source code performs it); `none` where there is no route. -/
def diagRoute (d : DiagClass) : Option Routing := (runTag d).map routePfp

/-- checked_packet.rs line 248: only the exact class is certificate-eligible (necessary, not sufficient). -/
def certEligible : DiagClass → Bool
  | .ExactClass => true
  | _ => false

/-- op_verification.rs `ExactRepairFromNonExactClass`: the repair operation has the exact class as a precondition. -/
def exactRepairAllowed : DiagClass → Bool
  | .ExactClass => true
  | _ => false

/-- Certified authority needs a witness AND an authority-bearing terminal. -/
def certified (s : TermStatus) (witness : Bool) : Bool := witness && authTerminal s

/-- checked_packet.rs line 248 as a gate: the class selects the authority terminal (exact class only) and a witness is also required. -/
def sealTerminal : DiagClass → Option TermStatus
  | .ExactClass => some .ExactRuleDerived
  | _ => none

/-- A certificate can be sealed only for an eligible class and with a witness (the sealed certificate keeps AuthorityEffect None). -/
def sealed (d : DiagClass) (witness : Bool) : Bool := witness && (sealTerminal d).isSome

/-- A situation: the three axes plus the witness flag. -/
structure Situation where
  diag : DiagClass
  status : TermStatus
  witness : Bool

/-- Defined from (status, witness) only: the independence from `diag` below is by construction of this model. -/
def Situation.authority (x : Situation) : Bool := certified x.status x.witness
def Situation.terminal (x : Situation) : Routing := routeStatus x.status

/-! ### Counts of the axes -/

theorem card_axes :
    Fintype.card DiagClass = 3 ∧ Fintype.card Routing = 7 ∧ Fintype.card TermStatus = 21 ∧
    Fintype.card Pfp = 10 ∧ Fintype.card Residual = 4 ∧ Fintype.card RelStatus = 4 ∧
    Fintype.card (DiagClass × Routing) = 21 := by
  refine ⟨by decide, by decide, by decide, by decide, by decide, by decide, ?_⟩
  simp [Fintype.card_prod]
  decide

/-! ### The diagnostic class does not determine the terminal: all policies are possible -/

/-- Policies are independent per class: any two classes can take any two terminals. -/
theorem policy_values_independent (d d' : DiagClass) (h : d ≠ d') (r r' : Routing) :
    ∃ p : DiagClass → Routing, p d = r ∧ p d' = r' :=
  ⟨Function.update (fun _ => r) d' r', by simp [Function.update, h], by simp⟩

theorem no_value_forced (d : DiagClass) (r : Routing) :
    (∃ p : DiagClass → Routing, p d = r) ∧ (∃ p : DiagClass → Routing, p d ≠ r) := by
  refine ⟨⟨fun _ => r, rfl⟩, ?_⟩
  by_cases h : r = CheckPassed
  · exact ⟨fun _ => RequiresLift, by subst h; simp⟩
  · exact ⟨fun _ => CheckPassed, fun e => h e.symm⟩

theorem card_policies : Fintype.card (DiagClass → Routing) = 343 := by
  simp only [Fintype.card_fun]
  have h1 : Fintype.card Routing = 7 := by decide
  have h2 : Fintype.card DiagClass = 3 := by decide
  rw [h1, h2]
  decide

theorem no_surjective_policy (p : DiagClass → Routing) : ¬ Function.Surjective p := by
  intro h
  have := Fintype.card_le_of_surjective p h
  have h1 : Fintype.card Routing = 7 := by decide
  have h2 : Fintype.card DiagClass = 3 := by decide
  omega

theorem no_injective_from_routing (g : Routing → DiagClass) : ¬ Function.Injective g := by
  intro h
  have := Fintype.card_le_of_injective g h
  have h1 : Fintype.card Routing = 7 := by decide
  have h2 : Fintype.card DiagClass = 3 := by decide
  omega

/-- Injective policies DO exist (210 of them); what is missing is any forced, surjective or bijective one. -/
theorem card_injective_policies : Fintype.card (DiagClass ↪ Routing) = 210 := by
  rw [Fintype.card_embedding_eq]
  have h1 : Fintype.card Routing = 7 := by decide
  have h2 : Fintype.card DiagClass = 3 := by decide
  rw [h1, h2]
  decide

/-- The one declared policy (run.rs + terminal_routing.json) is partial: the exact class has no route. -/
theorem diagRoute_values :
    diagRoute .ExactClass = none ∧ diagRoute .ClosedResidual = some .RequiresLift ∧
    diagRoute .ActiveClosureFailure = some .Refusal := by decide

/-- The declared partial policy extends to injective total policies (it is injective where defined). -/
theorem diagRoute_injective_where_defined (d d' : DiagClass) (r : Routing)
    (h : diagRoute d = some r) (h' : diagRoute d' = some r) : d = d' := by
  revert d d' r
  decide

/-! ### Source tables: the axes are genuinely different -/

theorem routeStatus_surjective : Function.Surjective routeStatus := by
  intro r
  cases r
  · exact ⟨.ExactRuleDerived, rfl⟩
  · exact ⟨.LiftRequired, rfl⟩
  · exact ⟨.NonUniqueOutput, rfl⟩
  · exact ⟨.ParseRefused, rfl⟩
  · exact ⟨.NoRuleInSearchClass, rfl⟩
  · exact ⟨.BudgetUnknown, rfl⟩
  · exact ⟨.Refused, rfl⟩

theorem routePfp_not_surjective : ¬ Function.Surjective routePfp := by
  intro h
  obtain ⟨p, hp⟩ := h Routing.Repair
  cases p <;> simp [routePfp] at hp

/-- Both Repair and NoRule are missing from the image of the PfpTerminal map (so its image has at most 5 values). -/
theorem routePfp_misses_repair_and_norule (p : Pfp) : routePfp p ≠ Routing.Repair ∧ routePfp p ≠ Routing.NoRule := by
  cases p <;> simp [routePfp]

theorem residual_not_determine_route : ¬ ∃ f : Residual → Routing, ∀ s, routeStatus s = f (residualOf s) := by
  rintro ⟨f, hf⟩
  have h1 := hf .NonUniqueOutput
  have h2 := hf .LiftRequired
  simp [routeStatus, residualOf] at h1 h2
  rw [← h2] at h1
  exact absurd h1 (by decide)

theorem route_not_determine_residual : ¬ ∃ g : Routing → Residual, ∀ s, residualOf s = g (routeStatus s) := by
  rintro ⟨g, hg⟩
  have h1 := hg .ParseRefused
  have h2 := hg .NoPacket
  simp [routeStatus, residualOf] at h1 h2
  rw [← h2] at h1
  exact absurd h1 (by decide)

theorem auth_not_determine_route : ¬ ∃ f : AuthTag → Routing, ∀ s, routeStatus s = f (authTag s) := by
  rintro ⟨f, hf⟩
  have h1 := hf .NonUniqueOutput
  have h2 := hf .LiftRequired
  simp [routeStatus, authTag] at h1 h2
  rw [← h2] at h1
  exact absurd h1 (by decide)

/-- Positive: at tag level the authority tag IS a function of the routing terminal in these tables. -/
theorem authTag_factors_through_route : ∃ f : Routing → AuthTag, ∀ s, authTag s = f (routeStatus s) := by
  refine ⟨fun r => match r with
    | .CheckPassed => .Certifiable
    | .Refused => .Refused
    | _ => .Uncertified, ?_⟩
  intro s
  cases s <;> rfl

/-- The tag alone is never certified (source test); certification needs a witness. -/
theorem certified_needs_witness (s : TermStatus) : certified s false = false := by simp [certified]

theorem certified_only_for_authority_terminals (s : TermStatus) (w : Bool) (h : certified s w = true) :
    s = .ExactRuleDerived ∨ s = .UniqueOutputDerived := by
  cases s <;> simp_all [certified, authTerminal]

/-- By construction of `Situation.authority` (it omits `diag`): changing the class changes nothing in this model. -/
theorem diag_cannot_set_authority (x : Situation) (d : DiagClass) :
    ({ x with diag := d } : Situation).authority = x.authority := rfl

theorem diag_cannot_set_terminal (x : Situation) (d : DiagClass) :
    ({ x with diag := d } : Situation).terminal = x.terminal := rfl

/-- ExactClass is certificate-eligible and repair-admissible but still not authority without witness and terminal. -/
theorem exactClass_not_authority :
    ∃ x : Situation, x.diag = .ExactClass ∧ certEligible x.diag = true ∧ exactRepairAllowed x.diag = true ∧
      x.authority = false :=
  ⟨⟨.ExactClass, .ExactRuleDerived, false⟩, rfl, rfl, rfl, rfl⟩

theorem certEligible_iff (d : DiagClass) : certEligible d = true ↔ d = .ExactClass := by cases d <;> simp [certEligible]

/-- The class IS a necessary gate for sealing a certificate (checked_packet.rs line 248): only the exact class can be sealed. -/
theorem sealed_only_exact (d : DiagClass) (w : Bool) (h : sealed d w = true) : d = .ExactClass := by
  cases d <;> simp_all [sealed, sealTerminal]

/-- ... and never sufficient: without a witness even the exact class is not sealed. -/
theorem sealed_needs_witness (d : DiagClass) : sealed d false = false := by simp [sealed]

theorem sealed_exact_with_witness : sealed .ExactClass true = true := by decide

/-- Tension between two source tables if the closed classes are identified (a modelling choice, not asserted). -/
theorem closed_tension :
    residualOf .NoRuleInSearchClass = .ClosedSurvivor ∧ routeStatus .NoRuleInSearchClass = .NoRule ∧
    diagRoute .ClosedResidual = some .RequiresLift ∧ Routing.NoRule ≠ Routing.RequiresLift := by decide

/-! ### What the fiber classifier can reach (general over all counts) -/

theorem fiber_route_in (selected : Bool) (cand out : Nat) (exh : Bool) (agr : Option (Bool × Bool)) (verifier : Bool)
    (s : TermStatus) (h : fiberStatus selected cand out exh agr verifier = some s) :
    routeStatus s = .CheckPassed ∨ routeStatus s = .Repair ∨ routeStatus s = .NoRule ∨ routeStatus s = .Refusal := by
  unfold fiberStatus at h
  split_ifs at h <;> cases h
  all_goals simp [routeStatus]

/-- Three of the seven terminals are not reachable from the fiber classifier whatever the counts. -/
theorem fiber_never_lift_budget_refused (selected : Bool) (cand out : Nat) (exh : Bool) (agr : Option (Bool × Bool))
    (verifier : Bool) (s : TermStatus) (h : fiberStatus selected cand out exh agr verifier = some s) :
    routeStatus s ≠ .RequiresLift ∧ routeStatus s ≠ .BudgetUnknown ∧ routeStatus s ≠ .Refused := by
  rcases fiber_route_in selected cand out exh agr verifier s h with h1 | h1 | h1 | h1 <;> rw [h1] <;> decide

/-- Instance: the four reachable terminals are each reached (so the bound above is attained). -/
theorem fiber_reaches_four :
    fiberStatus true 1 1 true none true = some .ExactRuleDerived ∧
    fiberStatus true 0 0 true none true = some .NoRuleInSearchClass ∧
    fiberStatus true 2 2 true none true = some .NonUniqueOutput ∧
    fiberStatus false 0 0 false none true = some .NoPacket := by decide

/-! ### The external Routing.lean `route` is a separate four-valued axis -/

theorem outside_profile_ne_refuted : RelStatus.outsideProfile ≠ RelStatus.refuted := by decide

theorem relRoute_outside (c s : Bool) : relRoute false c s = .outsideProfile := by cases c <;> cases s <;> rfl

theorem refuted_requires_profile {i c s : Bool} (h : relRoute i c s = .refuted) : i = true := by
  cases i <;> simp_all [relRoute]

theorem relRoute_surjective : Function.Surjective (fun x : Bool × Bool × Bool => relRoute x.1 x.2.1 x.2.2) := by
  intro r
  cases r
  · exact ⟨(true, false, true), rfl⟩
  · exact ⟨(true, true, false), rfl⟩
  · exact ⟨(false, false, false), rfl⟩
  · exact ⟨(true, false, false), rfl⟩

end WdpDiagnosticRouting

#print axioms WdpDiagnosticRouting.card_axes
#print axioms WdpDiagnosticRouting.policy_values_independent
#print axioms WdpDiagnosticRouting.no_value_forced
#print axioms WdpDiagnosticRouting.card_policies
#print axioms WdpDiagnosticRouting.no_surjective_policy
#print axioms WdpDiagnosticRouting.no_injective_from_routing
#print axioms WdpDiagnosticRouting.card_injective_policies
#print axioms WdpDiagnosticRouting.diagRoute_values
#print axioms WdpDiagnosticRouting.diagRoute_injective_where_defined
#print axioms WdpDiagnosticRouting.routeStatus_surjective
#print axioms WdpDiagnosticRouting.routePfp_not_surjective
#print axioms WdpDiagnosticRouting.routePfp_misses_repair_and_norule
#print axioms WdpDiagnosticRouting.residual_not_determine_route
#print axioms WdpDiagnosticRouting.route_not_determine_residual
#print axioms WdpDiagnosticRouting.auth_not_determine_route
#print axioms WdpDiagnosticRouting.authTag_factors_through_route
#print axioms WdpDiagnosticRouting.certified_needs_witness
#print axioms WdpDiagnosticRouting.certified_only_for_authority_terminals
#print axioms WdpDiagnosticRouting.diag_cannot_set_authority
#print axioms WdpDiagnosticRouting.diag_cannot_set_terminal
#print axioms WdpDiagnosticRouting.exactClass_not_authority
#print axioms WdpDiagnosticRouting.certEligible_iff
#print axioms WdpDiagnosticRouting.sealed_only_exact
#print axioms WdpDiagnosticRouting.sealed_needs_witness
#print axioms WdpDiagnosticRouting.sealed_exact_with_witness
#print axioms WdpDiagnosticRouting.closed_tension
#print axioms WdpDiagnosticRouting.fiber_route_in
#print axioms WdpDiagnosticRouting.fiber_never_lift_budget_refused
#print axioms WdpDiagnosticRouting.fiber_reaches_four
#print axioms WdpDiagnosticRouting.outside_profile_ne_refuted
#print axioms WdpDiagnosticRouting.relRoute_outside
#print axioms WdpDiagnosticRouting.refuted_requires_profile
#print axioms WdpDiagnosticRouting.relRoute_surjective
