import D01D02Records
import T01FactorizationFiberConstancy
import T02BridgeAdmissibility
import T03NamedTerminalizers
import Algebra

/-!
# CODA-CS-Q programme wrapper (binding only)

Re-exports kernels and reconstruction CS-Q algebra. Not a second theorem home.
AuthorityEffect: None.
-/

namespace CodaCsQ

open CodaCsQ

#print axioms factorization_implies_fiber_constancy
#print axioms q_bar_on_image_well_defined
#print axioms factorization_iff_fiber_constancy_on_image
#print axioms BridgePacket14.field_count_eq_fourteen
#print axioms admissible_implies_all_eight
#print axioms bridge_admissible8_implies_fiber_constancy
#print axioms factorization_implies_named_terminalizers_agree
#print axioms terminalizers_not_automatic_from_flags

#print axioms Coda.CSQ.exact_on_image
#print axioms Coda.CSQ.approximate_collision_bound
#print axioms Coda.CSQ.metric_zero_error_implies_equality
#print axioms Coda.CSQ.pseudometric_zero_error_does_not_imply_equality
#print axioms Coda.CSQ.lipschitz_access
#print axioms Coda.CSQ.samples_not_query
#print axioms Coda.CSQ.whole_codomain_needs_extension
#print axioms Coda.CSQ.total_factor_of_inhabited

end CodaCsQ

#check Coda.CSQ.image_factor_unique
#print axioms Coda.CSQ.image_factor_unique
