import A

/-!
# Reconstruction A algebra

Publication wrapper for `CodaReconstruction.A`.
Source: `A.lean`.

Theorems A-T1 through A-T7 and the induced quotient section:
- A-D1 / Decomposition: x = C x + residual C x
- A-T1: residual C x = 0 ↔ C x = x
- A-T2: C (residual C x) = 0 for projection C
- A-T3: residual C (residual C x) = residual C x for projection C
- A-T4: range C = fixed C for projection C
- A-T5: T (residual C x) = residual D (T x) under commuting T
- A-T6: x - y ∈ im C ↔ residual C x = residual C y
- A-T7: universal factorization on quotient V/R
- Section 4: induced section s : V / im C → V identifying V / im C ≅ ker C

AuthorityEffect: None.
-/

#check Coda.A.decomposition
#print axioms Coda.A.decomposition
#check Coda.A.residual_zero_iff
#print axioms Coda.A.residual_zero_iff
#check Coda.A.residual_in_kernel
#print axioms Coda.A.residual_in_kernel
#check Coda.A.residual_idempotent
#print axioms Coda.A.residual_idempotent
#check Coda.A.range_fixed_iff
#print axioms Coda.A.range_fixed_iff
#check Coda.A.direct_sum_decomposition
#print axioms Coda.A.direct_sum_decomposition
#check Coda.A.direct_sum_unique
#print axioms Coda.A.direct_sum_unique
#check Coda.A.residual_transport
#print axioms Coda.A.residual_transport
#check Coda.A.quotient_residual_iff
#print axioms Coda.A.quotient_residual_iff
#check Coda.A.quotient_universal
#print axioms Coda.A.quotient_universal
#check Coda.A.quotient_section
#print axioms Coda.A.quotient_section
