import D01D02Records
import T01SpanPullback
import T02MasterNormalForm
import T03AuthorityFirewall
import Algebra

/-!
# CODA-GTLA programme wrapper (binding only)

Re-exports kernels and reconstruction leftover algebra. Not a second theorem home.
-/

namespace CodaGtla

-- Axiom Audits
#print axioms diagSpan_cost_zero
#print axioms compSpan_cost_subadditive
#print axioms idTrace_work_zero
#print axioms eraseTrace_id
#print axioms eraseTrace_comp
#print axioms pipeline_empty_sieve_refused
#print axioms pipeline_licensed_exact_authorized
#print axioms pipeline_closed_residual_anomalon
#print axioms auth_disjoint_anomalon
#print axioms auth_disjoint_refused
#print axioms anomalon_disjoint_refused
#print axioms non_promotion_firewall
#print axioms observation_collision_distinct_authority

end CodaGtla
