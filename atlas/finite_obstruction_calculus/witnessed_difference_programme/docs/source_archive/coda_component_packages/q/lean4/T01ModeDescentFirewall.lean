import D01D02Records

/-!
# CODA-Q T01: Mode Descent & Quarantine Firewall Theorems

These retained model declarations use historical Q-LEGACY labels.
They are not the metric-completion theorems Q-T1 through Q-T5.

Formalizes:
1. Historical model label Q-LEGACY-T0: Mode-being is descent plus terminalization.
2. Mode refinement pushforward: descent and being push forward along mode refinement.
3. Historical model label Q-LEGACY-T1: Q statuses are not authority terminals (pointwise disjointness).
4. Historical model label Q-LEGACY-T1a: Claim-machine statuses are not authority terminals.
5. 7-Guard Halt Conjunction equivalence.

AuthorityEffect: None.
-/

namespace CodaQ

universe u

/-- A declared mode of repeatable engagement for a candidate. -/
structure DescentMode (Candidate : Type u) where
  noticed : Candidate → Prop
  measured : Candidate → Prop
  repeated : Candidate → Prop
  compared : Candidate → Prop
  shared : Candidate → Prop
  terminalized : Candidate → Prop

/--
Primitive descent is repeatable, shareable, constrained engagement under a
declared mode. It replaces bare "being" in Level Q.
-/
def PrimitiveDescent {Candidate : Type u}
    (mode : DescentMode Candidate) (candidate : Candidate) : Prop :=
  mode.noticed candidate ∧
  mode.measured candidate ∧
  mode.repeated candidate ∧
  mode.compared candidate ∧
  mode.shared candidate

/-- Mode-being is shorthand for primitive descent plus terminalization. -/
def ModeBeing {Candidate : Type u}
    (mode : DescentMode Candidate) (candidate : Candidate) : Prop :=
  PrimitiveDescent mode candidate ∧ mode.terminalized candidate

/-- A stricter engagement mode implies a weaker one coordinate by coordinate. -/
structure ModeRefines {Candidate : Type u}
    (strong weak : DescentMode Candidate) : Prop where
  noticed : ∀ candidate, strong.noticed candidate → weak.noticed candidate
  measured : ∀ candidate, strong.measured candidate → weak.measured candidate
  repeated : ∀ candidate, strong.repeated candidate → weak.repeated candidate
  compared : ∀ candidate, strong.compared candidate → weak.compared candidate
  shared : ∀ candidate, strong.shared candidate → weak.shared candidate
  terminalized : ∀ candidate, strong.terminalized candidate → weak.terminalized candidate

/-- Historical model label Q-LEGACY-T0: Mode-Being unpacks to descent and terminalization. -/
theorem mode_being_unpacks_to_descent_and_terminalization
    {Candidate : Type u} (mode : DescentMode Candidate) (candidate : Candidate) :
    ModeBeing mode candidate ↔
      PrimitiveDescent mode candidate ∧ mode.terminalized candidate :=
  Iff.rfl

theorem mode_being_requires_primitive_descent
    {Candidate : Type u} (mode : DescentMode Candidate) {candidate : Candidate} :
    ModeBeing mode candidate → PrimitiveDescent mode candidate :=
  fun h => h.left

theorem mode_descent_pushes_forward
    {Candidate : Type u} {strong weak : DescentMode Candidate}
    (hRef : ModeRefines strong weak) {candidate : Candidate} :
    PrimitiveDescent strong candidate → PrimitiveDescent weak candidate := by
  intro ⟨h1, h2, h3, h4, h5⟩
  exact ⟨hRef.noticed _ h1, hRef.measured _ h2, hRef.repeated _ h3, hRef.compared _ h4, hRef.shared _ h5⟩

/-- Mode-being pushes forward along mode refinement. -/
theorem mode_being_pushes_forward_along_mode_refinement
    {Candidate : Type u} {strong weak : DescentMode Candidate}
    (hRef : ModeRefines strong weak) {candidate : Candidate} :
    ModeBeing strong candidate → ModeBeing weak candidate := by
  intro ⟨hDesc, hTerm⟩
  exact ⟨mode_descent_pushes_forward hRef hDesc, hRef.terminalized _ hTerm⟩

/-- Historical model label Q-LEGACY-T1: Q statuses are not authority terminals. -/
theorem q_terminal_not_authority_terminal
    (status : QuarantineStatus) (terminal : AuthorityTerminal) :
    QOrAuthority.q status ≠ QOrAuthority.authority terminal := by
  intro h
  cases h

theorem no_q_status_equals_authority_terminal :
    ¬ ∃ (status : QuarantineStatus) (terminal : AuthorityTerminal),
      QOrAuthority.q status = QOrAuthority.authority terminal := by
  intro ⟨status, terminal, hEq⟩
  exact q_terminal_not_authority_terminal status terminal hEq

/-- Historical model label Q-LEGACY-T1a: Claim-machine statuses are not authority terminals. -/
theorem claim_machine_status_not_authority_terminal
    (status : ClaimMachineStatus) (terminal : AuthorityTerminal) :
    ClaimMachineOrAuthority.claim status ≠ ClaimMachineOrAuthority.authority terminal := by
  intro h
  cases h

theorem no_claim_machine_status_equals_authority_terminal :
    ¬ ∃ (status : ClaimMachineStatus) (terminal : AuthorityTerminal),
      ClaimMachineOrAuthority.claim status = ClaimMachineOrAuthority.authority terminal := by
  intro ⟨status, terminal, hEq⟩
  exact claim_machine_status_not_authority_terminal status terminal hEq

/-- 7-Guard Halt Conjunction boolean equivalence. -/
theorem halt_guards_is_auth_iff_all_seven (g : HaltGuards) :
    g.is_auth = true ↔
      (g.accepted = true ∧
       g.deterministic = true ∧
       g.zero_residual_mass = true ∧
       g.skeleton_preserving = true ∧
       g.exhaustive = true ∧
       g.no_pending_lift = true ∧
       g.no_refusal = true) := by
  unfold HaltGuards.is_auth
  simp only [Bool.and_eq_true]
  constructor
  · rintro ⟨⟨⟨⟨⟨⟨h1, h2⟩, h3⟩, h4⟩, h5⟩, h6⟩, h7⟩
    exact ⟨h1, h2, h3, h4, h5, h6, h7⟩
  · rintro ⟨h1, h2, h3, h4, h5, h6, h7⟩
    exact ⟨⟨⟨⟨⟨⟨h1, h2⟩, h3⟩, h4⟩, h5⟩, h6⟩, h7⟩

end CodaQ

