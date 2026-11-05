import FOC

/-!
# Reconstruction FOC algebra

Publication wrapper for `FOC`.
Source of truth: `FOC.lean`.

Claim map: FOC-01 `repair_refl`/`symm`/`trans`; FOC-02 `separator_obstructs`,
`separator_exists`; FOC-03 `exact_closed`; FOC-04 `weighted_diagonal_lower`,
`diagonal_minimum`, `diagonal_zero_iff`; FOC-05 `transport_bound`,
`repair_distance_transport`.
-/

#check Coda.FOC.repair_refl
#print axioms Coda.FOC.repair_refl
#check Coda.FOC.repair_symm
#print axioms Coda.FOC.repair_symm
#check Coda.FOC.repair_trans
#print axioms Coda.FOC.repair_trans
#check Coda.FOC.separator_obstructs
#print axioms Coda.FOC.separator_obstructs
#check Coda.FOC.exact_closed
#print axioms Coda.FOC.exact_closed
#check Coda.FOC.weighted_diagonal_lower
#print axioms Coda.FOC.weighted_diagonal_lower
#check Coda.FOC.diagonal_minimum
#print axioms Coda.FOC.diagonal_minimum
#check Coda.FOC.diagonal_zero_iff
#print axioms Coda.FOC.diagonal_zero_iff
#check Coda.FOC.transport_bound
#print axioms Coda.FOC.transport_bound
#check Coda.FOC.repair_distance_transport
#print axioms Coda.FOC.repair_distance_transport
#check Coda.FOC.separator_exists
#print axioms Coda.FOC.separator_exists
