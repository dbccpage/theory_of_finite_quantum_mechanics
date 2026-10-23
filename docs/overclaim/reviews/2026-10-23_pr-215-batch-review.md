# Review of PR #215

AuthorityEffect: None. AI-assisted independent review; no human approval is claimed.

Scope: f1eefb8d7749269777d9a66d3d2965aa320f5a32 and the repairs recorded here. No mathematical node is changed. The Rust production verifier, policy, CLI and evidence boundaries were reviewed; the independent crate build avoids the workspace's unavailable external dependencies.

A concrete custody failure was reproduced in descriptor.rs: a record could be changed while its separate raw_utf8 bytes and digest remained intact. The verifier evaluated that changed record. The new regression alters a score level and a contract view, fails on the original implementation, and passes after requiring equality with the JSON parsed from the hashed bytes.

The evidence-copy tool no longer recursively deletes an existing --copy directory, including the source crate. It creates a new retained snapshot and records the bytes actually tested, checking that the snapshot stayed unchanged. The mutation tool creates a fresh source copy per candidate, retains per-mutant output, and requires an actual libtest failure before reporting KILLED. Cargo download, linker, launch and missing-test failures are inconclusive rather than killed. The source-change check refuses to credit a campaign whose Rust source manifest changes during the run.

Fresh isolated Rust verification passes 48 library tests and 10 binary tests (one doctest remains ignored). The separate all-target strict clippy run passes after flattening two nested test loops. A fresh capture of tests, library/binary clippy and lizard also passes. Thirteen focused Python regressions and strict mypy of all three repaired Python files pass. Original failed regression and clippy runs remain in the review evidence.

Acceptance is withheld. descriptor.rs is L4D for its repaired custody API. score.rs is L3D: the enum vocabulary, token parser and minimum comparison do not become a substantive L4 architecture because other code consumes them. The two evidence runners remain L3D bounded utilities; the new regression suite is L2D under the explicit support-file exception. The substantive L3 modules are outside that exception. Additional original changed artifacts still lack independently completed source-bound assessments. No baseline addition or higher capability label was used to conceal the floor failure.

The original mutation totals are historical author evidence. This review does not establish those classifications from raw per-mutant logs and does not repeat them as current ratios for the repaired bytes. Process-tree cancellation, scratch retention, larger resource bounds and complete whole-PR contract coverage remain open. The full multi-crate workspace was not certified.

Evidence: evidence/quality/pr215_independent_review.json and evidence/governance/pr215-independent-review/receipt.json. All five repaired code artifacts have preserved-history companions (or new companions for the previously unscored tools/test) bound to their exact bytes. This focused repair is not permission to merge the PR below the maintainer's L4D floor.
