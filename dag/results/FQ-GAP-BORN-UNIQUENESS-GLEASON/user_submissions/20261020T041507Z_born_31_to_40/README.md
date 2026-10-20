# BR-31 through BR-40: typed instruments, filed and reviewed

AuthorityEffect: None. Written mathematical review and exact finite controls; all Lean kernel verification remains pending.

Both attachments are preserved byte-for-byte: [submitted proofs](submission/BR-31_40_typed_instruments.md) and [submitted checks](submission/br31_40_checks.py). The [reviewed manuscript](BR-31_40_typed_instruments.md) incorporates corrections; [corrections and general arguments](corrections.md) explain each change. [Review verdict](review.md), [per-item status](lemma_status.json), [operation records](operad_delta.json), and [BR-41 through BR-50 requests](next_born_requests_41_to_50.md) are separate artifacts.

Accepted core results include typed branch-state semantics, the general Choi/adjoint conjugation formula and CP transpose specialization, rational mixing, certifying PSD recursion, the qubit probability ball, the Choi link product, rational padded unitary matching and the typed-dilation state identity.

Substantive repairs:

- BR-31: merge is generally an irreversible CPTP tag-forgetting channel; component-unit laws hold on the tagged direct-sum algebra, not every full-matrix extension.
- BR-33: an explicit invertible merged channel passes the kernel condition but requires a nonpositive inverse, demonstrating the CP obstruction.
- BR-34: the finite real convex hull of rational instruments misses irrational extreme projective instruments. The closure theorem is distinct. Normalized continuation mixtures are affine in each argument.
- BR-38: the rational non-norm argument needs primitive-denominator descent, not only an integer search. Grouping four real squares into two Gaussian norms gives the additional rank-to-2rank Kraus-count bound.
- BR-39: the original single-pair global interchange has incompatible outcome counts. The replacement substitutes continuations across all affected rows and columns of the outcome grid.
- BR-40: unitary implementation requires an explicit input encoding or common-dimension product padding. Nested direct and product-pointer dilations agree after an environment embedding.

The submitted script has **86 PASS checks per mode**, replayed as received. Its reviewed derivative retains **86 fixture checks per mode**, with explicit Gaussian-rational/domain guards, integer square-root bounds, corrected rectangular input-first vectorization and optimization-safe failure behavior. The host [independent controls](verification/independent_checks.py) pass **72 controls and 13 expected refusals per mode**, including full-grid and heterogeneous-dilation examples. These counts are not counts of kernel proofs.

[Normal independent receipt](verification/independent_normal.command.json), [optimized independent receipt](verification/independent_optimized.command.json), [script repair record](verification/script_repairs.json), [attachment custody](attachment_custody.json), [validation](validation.json), [provenance](provenance.json), and [seal](manifest.json) bind the evidence. The first host hardened replay's namespace failure is [retained](verification/retained_failures/README.md), separately from passing retries.

Earlier sealed evidence and operation records are preserved. No live native source or manuscript was edited, no provider call was made, and no commit/push/PR/merge was performed. Stop for review.
