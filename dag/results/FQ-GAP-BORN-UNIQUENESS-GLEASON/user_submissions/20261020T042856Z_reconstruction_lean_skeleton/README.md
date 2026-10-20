# Row 8 Lean skeleton: filed, compiled and semantically audited

AuthorityEffect: None. Full operational reconstruction remains NOT ESTABLISHED.

The [original attachment](submission/ReconstructionOriginal.lean) compiles unchanged under core Lean 4.33.1 and reproduces its reported axiom receipts. The arithmetic proofs are useful. The unrestricted imported Jordan bridge is unsafe over the file's bare System interface: an explicit Lean diagnostic derives False from that signature.

- [Review and mathematical scope](review.md).
- [Arithmetic-only extraction](ReconstructionArithmetic.lean): 19 printed theorem receipts; no custom axioms; encoded classification only.
- [Explicit conditional reconstruction](ReconstructionConditional.lean): predicates and all five per-theory bridge fields are hypotheses, with no supplied instance. Includes two axiom-free finite-hull interface lemmas.
- [Unsafe-signature diagnostic](ReconstructionUnsafeDiagnostic.lean): original source plus the one-state rank1/dim2 counterexample. Audit evidence only; do not import the unsafe declarations into a production proof library.
- [Parsed kernel receipts](verification/kernel_axioms.json), [compiler pin](verification/toolchain.json), and [validation](validation.json).
- [Five concrete classical-exclusion lemmas](next_classical_exclusion_lemmas.md), [claim statuses](claim_status.json), [operation records](operad_delta.json), and [primary-source observations](source_observations.json).
- [Attachment custody](attachment_custody.json), [provenance](provenance.json), and [seal](manifest.json).

The arithmetic and conditional extracts have separate namespaces. They are self-contained alternative modules with no Mathlib imports. The diagnostic deliberately includes the original declarations; its successful compilation proves the interface problem rather than validating reconstruction. A clean axiom list for a theorem with explicit bridge hypotheses does not prove those hypotheses.

No live native source or manuscript was edited. No provider invocation, commit, push, PR or merge occurred. Stop for review.
