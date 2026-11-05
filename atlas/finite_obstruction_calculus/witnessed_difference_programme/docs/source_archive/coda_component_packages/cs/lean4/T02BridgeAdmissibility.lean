import D01D02Records

/-!
# CODA-CS T02: 8-Step Bridge Admissibility Soundness (BRIDGE-003)

Formalizes:
1. BRIDGE-003: 8-Step BridgeAdmissible conjunction.
2. Hard Refusal Theorem: Failure of any single step refutes admissibility.

AuthorityEffect: None.
-/

namespace CodaCs

open CodaCs

/-- Theorem: Conjunction equivalence of all 8 bridge admissibility steps. -/
theorem bridge_admissible_iff_all_steps
    (b : BridgeAdmissible8) :
    b.isAllAdmissible = true ↔
    (b.is_degree_bounded = true ∧
     b.is_cofinal = true ∧
     b.is_shadow_finite = true ∧
     b.is_profile_surjective = true ∧
     b.is_factorable = true ∧
     b.is_fiber_constant = true ∧
     b.is_transition_coherent = true ∧
     b.has_local_terminalizer = true) := by
  dsimp [BridgeAdmissible8.isAllAdmissible]
  constructor
  · intro h
    revert h
    cases b.is_degree_bounded <;> cases b.is_cofinal <;> cases b.is_shadow_finite <;>
    cases b.is_profile_surjective <;> cases b.is_factorable <;> cases b.is_fiber_constant <;>
    cases b.is_transition_coherent <;> cases b.has_local_terminalizer <;> decide
  · intro ⟨h1, h2, h3, h4, h5, h6, h7, h8⟩
    rw [h1, h2, h3, h4, h5, h6, h7, h8]
    rfl

/-- Individual step failures refute overall bridge admissibility. -/
theorem factorable_failure_refutes_admissibility
    (b : BridgeAdmissible8) (h : b.is_factorable = false) :
    b.isAllAdmissible = false := by
  rcases b with ⟨b1, b2, b3, b4, b5, b6, b7, b8⟩
  dsimp [BridgeAdmissible8.isAllAdmissible]
  dsimp at h
  rw [h]
  cases b1 <;> cases b2 <;> cases b3 <;> cases b4 <;> rfl

theorem fiber_constancy_failure_refutes_admissibility
    (b : BridgeAdmissible8) (h : b.is_fiber_constant = false) :
    b.isAllAdmissible = false := by
  rcases b with ⟨b1, b2, b3, b4, b5, b6, b7, b8⟩
  dsimp [BridgeAdmissible8.isAllAdmissible]
  dsimp at h
  rw [h]
  cases b1 <;> cases b2 <;> cases b3 <;> cases b4 <;> cases b5 <;> rfl

end CodaCs
