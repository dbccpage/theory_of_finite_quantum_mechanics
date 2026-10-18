
import BornRedundancy

open BornRedundancy

theorem two_outcome_ray_redundancy :
    normalize (normalize ([1, 3] : List Rat)) = normalize [1, 3] ∧
      normalize (smul (2 : Rat) [1, 3]) = normalize [1, 3] := by
  refine ⟨normalize_idempotent [1, 3] ?_, normalize_smul 2 [1, 3] ?_ ?_⟩
  · simp [listSum]; grind
  · decide
  · simp [listSum]; grind

#print axioms normalize_idempotent
#print axioms normalize_smul
#print axioms ray_quotient_classification
#print axioms D1_zero_iff_mul_nonneg
#print axioms descent_compatible_iff_row_sparse

private def l5aProvenance : String :=
  "Origin: lean4/BornRedundancyAxioms.lean Claim: two_outcome_ray_redundancy AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
