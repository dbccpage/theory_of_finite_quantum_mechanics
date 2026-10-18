import BornRedundancy

open BornRedundancy

/-- Two-outcome weights `[1, 3]` have idempotent normalization and the same
    ray as their double. -/
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
