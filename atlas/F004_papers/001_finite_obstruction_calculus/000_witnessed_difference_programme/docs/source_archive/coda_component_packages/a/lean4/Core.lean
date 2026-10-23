import D01D02Records
import T01AnomalonTerminal
import T02ResidualNonCreation
import T03ToyAnomalonWitness
import Algebra

/-!
# CODA-A programme wrapper (binding only)

Re-exports kernels and reconstruction A algebra. Not a second theorem home.
AuthorityEffect: None.
-/

namespace CodaA

open CodaA

#print axioms closedResidual_is_anomalon
#print axioms openResidual_is_not_anomalon
#print axioms residual_not_auth
#print axioms authExtractor_empty
#print axioms authority_only_via_evidence
#print axioms firewall_toy
#print axioms toy_anomalon_exists
#print axioms firewall_from_toy_anomalon

end CodaA
