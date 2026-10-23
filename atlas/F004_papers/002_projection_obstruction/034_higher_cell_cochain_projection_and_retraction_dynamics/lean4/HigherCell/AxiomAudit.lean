import HigherCell.Core
import HigherCell.Theorem41_Idempotence
import HigherCell.Theorem42_Isolation

/-!
  # HigherCell.AxiomAudit — Axiom and Sorry Totality Audit
  Audits the seven named conditional abstract projector declarations below.
  Structure fields remain mathematical hypotheses even when no global axioms appear.
  Compilation is required for a fresh result; the report in this package is stored evidence.
  AuthorityEffect: None.
-/

namespace HigherCell

-- Theorem 4.1 Axiom Audits
#print axioms theorem41_marginal_preservation
#print axioms theorem41_idempotence
#print axioms theorem41_normal_annihilates_tangent

-- Theorem 4.2 Axiom Audits
#print axioms theorem42_P_sigma_one_local
#print axioms theorem42_one_local_isolation
#print axioms theorem42_tangent_isolation
#print axioms theorem42_tangent_fixed

end HigherCell
