import D01D02Records
import L01ContinuumNonCreation
import L02QueryAuthority
import T01FiberConstancy
import T02BridgeAdmissibility
import Algebra

/-!
# CODA-CS programme wrapper (binding only)

Re-exports kernels and reconstruction CS algebra. Not a second theorem home.
-/

-- Axiom audits
#print axioms CodaCs.continuum_limit_does_not_create_authority
#print axioms CodaCs.shadow_slice_necessity
#print axioms CodaCs.factorization_implies_fiber_constancy
#print axioms CodaCs.non_fiber_constant_precludes_factorization
#print axioms CodaCs.bridge_admissible_iff_all_steps
