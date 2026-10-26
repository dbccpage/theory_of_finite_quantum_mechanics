# Local Lean companion

Run `lake build`, then `lake env lean AxiomAudit.lean` from this directory.
Lean 4.33.0 and its bundled `Std` library are the only dependencies.

`Foundations.lean` formalizes witnessed distinction, a detector-pair
bridge, image factorization, collisions, menu exhaustion, and tied-cost
comparison. `Boundaries.lean` contains a transported factor, the
Boolean triangle, and elementary policy/constant-map counterexamples.
`Coda.lean` imports both modules, so the default build reaches every local
theorem. `AxiomAudit.lean` names all twenty audited declarations.

The image construction/specification and its iff theorem use
`Classical.choice`; function uniqueness reports `Quot.sound`. The other
seventeen declarations report no axioms. The current compiler output is
retained in [axiom_report.txt](axiom_report.txt). This differs
from the older foundational ledger's report for the truncated-search proof;
the new proof has no axiom dependencies.

No sealed derivation source is imported or reproduced. These are independent
CODA-side proofs of the elementary statements written in the manuscript.
No Mathlib fragment from the historical discipline subtree is a dependency.
The project does not mechanize general norm optimization, analytic
integration, category/functor construction, or operational authorization.
See the [formal claim map](../coda_claim_ledger.md) for exact coverage.
