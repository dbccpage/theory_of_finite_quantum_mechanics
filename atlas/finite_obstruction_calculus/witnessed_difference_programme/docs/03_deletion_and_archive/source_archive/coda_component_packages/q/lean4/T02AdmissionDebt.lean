import D01D02Records

/-!
# CODA-Q T02: Admission Debt & Scope Terminalization Theorems

These retained model declarations use historical Q-LEGACY labels.
They are not the metric-completion theorems Q-T1 through Q-T5.

Formalizes:
1. Historical model label Q-LEGACY-T1b: Q admission requires complete debt.
2. Individual field blocking theorems: missing any field blocks QHeld.
3. TerminalWithinScope admissibility: requires both QHeld and witness support.
4. Blocking theorems: missing witness or QHeld blocks TerminalWithinScope.

AuthorityEffect: None.
-/

namespace CodaQ

/-- Historical model label Q-LEGACY-T1b: QHeld is admissible iff complete admission debt is present. -/
theorem qheld_admissible_iff_complete_admission_debt
    (evidence : QAdmissionEvidence) :
    QHeldAdmissible evidence ↔
      evidence.finite_shadow ∧
      evidence.refinement_relation ∧
      evidence.declared_topology ∧
      evidence.convergence_certificate_route ∧
      evidence.descent_trigger :=
  Iff.rfl

/-- TerminalWithinScope is admissible iff QHeld is admissible and witness support holds. -/
theorem terminal_within_scope_admissible_iff_qheld_and_witness
    (evidence : QAdmissionEvidence) :
    TerminalWithinScopeAdmissible evidence ↔
      QHeldAdmissible evidence ∧ evidence.witness_support :=
  Iff.rfl

/-- Missing finite shadow blocks QHeld admission. -/
theorem missing_finite_shadow_blocks_qheld
    (evidence : QAdmissionEvidence) :
    ¬ evidence.finite_shadow → ¬ QHeldAdmissible evidence :=
  fun hNot hHeld => hNot hHeld.1

/-- Missing refinement relation blocks QHeld admission. -/
theorem missing_refinement_relation_blocks_qheld
    (evidence : QAdmissionEvidence) :
    ¬ evidence.refinement_relation → ¬ QHeldAdmissible evidence :=
  fun hNot hHeld => hNot hHeld.2.1

/-- Missing declared topology blocks QHeld admission. -/
theorem missing_declared_topology_blocks_qheld
    (evidence : QAdmissionEvidence) :
    ¬ evidence.declared_topology → ¬ QHeldAdmissible evidence :=
  fun hNot hHeld => hNot hHeld.2.2.1

/-- Missing convergence certificate route blocks QHeld admission. -/
theorem missing_convergence_certificate_route_blocks_qheld
    (evidence : QAdmissionEvidence) :
    ¬ evidence.convergence_certificate_route → ¬ QHeldAdmissible evidence :=
  fun hNot hHeld => hNot hHeld.2.2.2.1

/-- Missing descent trigger blocks QHeld admission. -/
theorem missing_descent_trigger_blocks_qheld
    (evidence : QAdmissionEvidence) :
    ¬ evidence.descent_trigger → ¬ QHeldAdmissible evidence :=
  fun hNot hHeld => hNot hHeld.2.2.2.2

/-- TerminalWithinScope requires QHeld admission. -/
theorem terminal_within_scope_requires_qheld_admission
    (evidence : QAdmissionEvidence) :
    TerminalWithinScopeAdmissible evidence → QHeldAdmissible evidence :=
  fun h => h.1

/-- TerminalWithinScope requires witness support. -/
theorem terminal_within_scope_requires_witness_support
    (evidence : QAdmissionEvidence) :
    TerminalWithinScopeAdmissible evidence → evidence.witness_support :=
  fun h => h.2

/-- TerminalWithinScope without witness support is blocked. -/
theorem terminal_within_scope_without_witness_blocked
    (evidence : QAdmissionEvidence) :
    ¬ evidence.witness_support → ¬ TerminalWithinScopeAdmissible evidence :=
  fun hNot hTerm => hNot hTerm.2

/-- TerminalWithinScope without QHeld admission is blocked. -/
theorem terminal_within_scope_without_qheld_admission_blocked
    (evidence : QAdmissionEvidence) :
    ¬ QHeldAdmissible evidence → ¬ TerminalWithinScopeAdmissible evidence :=
  fun hNot hTerm => hNot hTerm.1

end CodaQ
