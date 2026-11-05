import D01D02Records
import L01NonCreation
import L02SupportSieve
import T01SquareClassification
import T02LimitAuthority
import Algebra

/-!
# CODA-OR programme wrapper (binding only)

Re-exports kernels and reconstruction OR algebra. Not a second theorem home.
-/

-- Axiom audits
#print axioms CodaOr.completion_reflector_does_not_create_authority
#print axioms CodaOr.empty_support_sieve_implies_zero_authority
#print axioms CodaOr.exact_repair_is_closed
#print axioms CodaOr.limit_missing_terminalizer_lacks_authority
#print axioms CodaOr.omniversal_not_assumed
