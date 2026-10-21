# PR 118 self-review

AuthorityEffect: None. The broader quality campaign is stopped at the user's request.

Reviewed the executable changes, admission/resource limits, immutable ownership, exact arithmetic, source-bound score claims, Rust fixture custody, SQL arithmetic and transaction lifecycle, and the evidence replay/accounting boundaries. Current main a47c5f964a2f0f4abeb77a9fab657e32d922e7ef was integrated before validation; this is a focused review, not a whole-program verification.

## Findings and repairs

1. P2: The database replay supplied a deeply nested pytest temporary directory without creating its parent. This made the Python adapter baseline inconclusive and left 14 faults unrun. Use a short deterministic directory under the owned pytest cache, creating its parent before each subprocess. Baseline success and candidate outcomes are rechecked; the original failed receipt remains unchanged.
2. P2: Removing WITHOUT ROWID from a STRICT witness table was mislabeled as admitting a nullable primary key. STRICT still rejects that NULL. Rename the fault to describe the actual storage-layout change and assert the declared STRICT/WITHOUT ROWID properties using the running engine's PRAGMA table_list. The survivor is detected against the storage invariant, not retroactively called a NULL defect.
3. P2: The first SQL observer classified a missing BEGIN's transaction-protocol error as invalid syntax. The repaired observer distinguishes transaction framing errors from compilation/name-resolution failures and continues probing the tail after constraint refusals. Deliberately malformed controls, including malformed tails following semantic refusal, must remain INVALID and never count as detected semantic faults.

The earlier checkpoint archives with newline-normalized embedded strings remain historical. Their corrected archives independently verify all 187 embedded byte digests. All 25 completed source assessments still match their current source hashes. Database source/test/support assessments remain partial; no new L4 score is manufactured from this replay. Other database schemas and the broad inventory remain unresolved as documented.

## Validation and custody

The adjacent pr-review-receipt.json pins the final logs, executable repairs, complete-source pin audit, corrected archive audit, and final database challenge receipt. It records exact passing counts and refuses incomplete fault outcomes. No compiled binaries are included. The shared checkout's unrelated QM, Lean, paper, DAG and problem-set edits are preserved.
