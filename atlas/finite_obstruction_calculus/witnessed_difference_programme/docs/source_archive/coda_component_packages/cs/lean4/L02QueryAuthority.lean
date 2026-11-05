import D01D02Records

/-!
# CODA-CS L02: Query-Relative Authority & Finite Shadow Necessity (GTTC-01, GTTC-03, GTTC-2B)

Formalizes:
1. GTTC-03: Query-relative scope of authority.
2. GTTC-2B: Finite shadow necessity (unauthorized or infinite shadows block query authority).
3. Cofinality necessity (non-cofinal slices block query authority).

AuthorityEffect: None.
-/

namespace CodaCs

open CodaCs

/-- Load-bearing Theorem GTTC-2B (Finite Shadow Necessity):
    If shadow slices lack local authority or finiteness, query authority fails. -/
theorem shadow_slice_necessity
    (X : ContinuumSignal) (q : ContinuumQuery) (b : BridgeAdmissible8)
    (h : b.is_shadow_finite = false) : ¬ HasQueryAuthority X q b := by
  intro hAuth
  rcases b with ⟨b1, b2, b3, b4, b5, b6, b7, b8⟩
  dsimp [HasQueryAuthority, BridgeAdmissible8.isAllAdmissible] at hAuth
  dsimp at h
  rw [h] at hAuth
  cases b1 <;> cases b2 <;> contradiction

/-- Load-bearing Theorem (Cofinality Necessity):
    If the shadow slice is not cofinal in the tower, query authority fails. -/
theorem cofinality_necessity
    (X : ContinuumSignal) (q : ContinuumQuery) (b : BridgeAdmissible8)
    (h : b.is_cofinal = false) : ¬ HasQueryAuthority X q b := by
  intro hAuth
  rcases b with ⟨b1, b2, b3, b4, b5, b6, b7, b8⟩
  dsimp [HasQueryAuthority, BridgeAdmissible8.isAllAdmissible] at hAuth
  dsimp at h
  rw [h] at hAuth
  cases b1 <;> contradiction

/-- Query authority requires all 8 conditions to be simultaneously true. -/
theorem query_authority_implies_all_admissible
    (X : ContinuumSignal) (q : ContinuumQuery) (b : BridgeAdmissible8)
    (hAuth : HasQueryAuthority X q b) :
    b.is_degree_bounded = true ∧
    b.is_cofinal = true ∧
    b.is_shadow_finite = true ∧
    b.is_profile_surjective = true ∧
    b.is_factorable = true ∧
    b.is_fiber_constant = true ∧
    b.is_transition_coherent = true ∧
    b.has_local_terminalizer = true := by
  rcases b with ⟨b1, b2, b3, b4, b5, b6, b7, b8⟩
  dsimp [HasQueryAuthority, BridgeAdmissible8.isAllAdmissible] at hAuth
  cases b1 <;> cases b2 <;> cases b3 <;> cases b4 <;>
  cases b5 <;> cases b6 <;> cases b7 <;> cases b8 <;>
  first | contradiction | exact ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩

end CodaCs
