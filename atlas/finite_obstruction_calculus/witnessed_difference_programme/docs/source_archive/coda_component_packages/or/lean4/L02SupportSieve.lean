import D01D02Records

/-!
# CODA-OR L02: Authority Support Sieve Necessity (GTOR-03, GTOR-04, GTOR-16)

Formalizes:
1. Support sieve membership invariants (GTOR-03).
2. Hard Refusal Theorem: Empty support sieve implies zero comparison authority (GTOR-04 / GTOR-16).
3. Uncredentialed source and uncertified arrow exclusion lemmas.

AuthorityEffect: None.
-/

namespace CodaOr

open CodaOr

/-- An arrow with uncredentialed source cannot be auth-supporting. -/
theorem uncredentialed_source_not_auth_supporting (u : SupportArrow)
    (h : u.source_has_authority = false) : u.is_auth_supporting = false := by
  dsimp [SupportArrow.is_auth_supporting]
  rw [h]
  rfl

/-- An arrow lacking a descent certificate cannot be auth-supporting. -/
theorem uncertified_arrow_not_auth_supporting (u : SupportArrow)
    (h : u.has_descent_certificate = false) : u.is_auth_supporting = false := by
  dsimp [SupportArrow.is_auth_supporting]
  rw [h]
  cases u.source_has_authority <;> rfl

/-- Sieve with empty arrow list is empty. -/
theorem empty_arrow_list_sieve_is_empty (target : String) :
    (SupportSieve.mk target []).isEmpty := by
  intro u hu
  cases hu

/-- Load-bearing Theorem GTOR-04 / GTOR-16:
    An empty support sieve implies zero comparison authority.
    Supp_Auth(X) = ∅ ⟹ Auth(X) = ∅. -/
theorem empty_support_sieve_implies_zero_authority (X : ComparisonObject)
    (hEmpty : X.support_sieve.isEmpty) : ¬ HasAuthority X := by
  intro hAuth
  rcases hAuth with ⟨hNonEmpty, _, _, _⟩
  exact hNonEmpty hEmpty

/-- Inhabited authority requires non-empty support sieve. -/
theorem authority_requires_non_empty_support (X : ComparisonObject)
    (hAuth : HasAuthority X) : ¬ X.support_sieve.isEmpty := by
  rcases hAuth with ⟨hNonEmpty, _, _, _⟩
  exact hNonEmpty

/-- Target binding is part of standing, not an unused side predicate. -/
theorem authority_requires_target_binding (X : ComparisonObject)
    (hAuth : HasAuthority X) : X.sieveTargetBound :=
  hAuth.2.2.2

/-- A sieve for a different object cannot provide standing. -/
theorem target_mismatch_blocks_authority (X : ComparisonObject)
    (hne : X.support_sieve.target_id ≠ X.object_id) : ¬ HasAuthority X := by
  intro hAuth
  exact hne (authority_requires_target_binding X hAuth).1

/-- Every supporting record in an authorized object has the declared target. -/
theorem authority_arrow_targets_object (X : ComparisonObject)
    (hAuth : HasAuthority X) (u : SupportArrow) (hu : u ∈ X.support_sieve.arrows) :
    u.target_id = X.object_id := by
  have h := authority_requires_target_binding X hAuth
  exact (h.2 u hu).trans h.1

/-- A concrete three-target countermodel admitted by the old unbound predicate. -/
def mismatchedTargetExample : ComparisonObject where
  object_id := "X"
  weight_class := ⟨"finite", true⟩
  support_sieve := ⟨"Z", [⟨"A", "Y", true, true⟩]⟩
  has_local_terminalizer := true
  has_descent_triplet := true

theorem old_flags_admit_mismatched_targets :
    ¬ mismatchedTargetExample.support_sieve.isEmpty ∧
    mismatchedTargetExample.has_local_terminalizer = true ∧
    mismatchedTargetExample.has_descent_triplet = true := by
  simp [mismatchedTargetExample, SupportSieve.isEmpty, SupportArrow.is_auth_supporting]

theorem mismatched_targets_have_no_authority : ¬ HasAuthority mismatchedTargetExample := by
  apply target_mismatch_blocks_authority
  decide

/-- Binding all targets makes the same finite support usable. -/
def boundTargetExample : ComparisonObject where
  object_id := "X"
  weight_class := ⟨"finite", true⟩
  support_sieve := ⟨"X", [⟨"A", "X", true, true⟩]⟩
  has_local_terminalizer := true
  has_descent_triplet := true

theorem bound_target_example_has_authority : HasAuthority boundTargetExample := by
  simp [HasAuthority, boundTargetExample, SupportSieve.isEmpty,
    SupportArrow.is_auth_supporting, ComparisonObject.sieveTargetBound, SupportSieve.targetBound]

end CodaOr
