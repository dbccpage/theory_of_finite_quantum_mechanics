import A

/-!
# Reconstruction algebra used by CODA-GTLA

There is no separate reconstruction GTLA module. Layered leftover claims
reuse `CodaReconstruction.A`: residual of an idempotent correction, kernel
placement, transport along a commuting map, and leftover classes as the
cokernel.
-/

#check Coda.A.residual_zero_iff
#print axioms Coda.A.residual_zero_iff
#check Coda.A.residual_in_kernel
#print axioms Coda.A.residual_in_kernel
#check Coda.A.residual_idempotent
#print axioms Coda.A.residual_idempotent
#check Coda.A.residual_transport
#print axioms Coda.A.residual_transport
#check Coda.A.range_fixed_iff
#print axioms Coda.A.range_fixed_iff
#check Coda.A.quotient_residual_iff
#print axioms Coda.A.quotient_residual_iff
#check Coda.A.quotient_universal
#print axioms Coda.A.quotient_universal
#check Coda.A.quotient_section
#print axioms Coda.A.quotient_section
