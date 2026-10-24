# Final scope review of PR 251

AuthorityEffect: None.

Scope: reviewed head 2e8913a68bcf518c572b778a4db2cf14f2cc5d04, followed by
companion-alias metadata repairs and an appended historical-process note.
This is a model-authored review, not independent human approval.

Method: inspected both implementations, the supplied-list scope limits and the
CodeRabbit findings. Verified the two exact source pins, unchanged current
contract/score contents, all raw history records, and the unchanged baseline
bytes. Rehashed the committed category source snapshot and raw replay logs.
Cargo and Lean were not rebuilt for this metadata-only follow-up. The existing
category replay and campaign records are retained with their original scopes.

Result: 0 nodes FULL, 0 NARROWED, 0 OVERCLAIM. No scientific node changes.
The mathematical ceiling remains the one documented in functor.rs:10 and
full_functor.rs:3,217,668: metadata validation does not certify category laws,
actual fullness or nonfaithfulness.

## Corrections

- The Functor contract and scoring records shared an ambiguous backslash alias
  (functor.contract.score.yaml:258,750). FullFunctor had the same collision with
  a forward-slash alias. Each now has a distinct contract/scoring fragment label.
  The helper scripts/contract_scores.py add/load/save operations preserve the raw
  record bytes and current selections; no filesystem fragment-routing API was
  introduced. Exact before/after metadata and hashes are in review_fixes.json.
- The old FullFunctor assessment's no-exception paragraph is historical
  (evidence/quality/full_functor_validation/REVIEW.md:35). An appended superseding
  note cites the approval; its original committed prefix is preserved.

## Per-node table

| Node | Verdict | Reason |
|---|---|---|
| None | Not applicable | Source pins, baseline exceptions, statuses, statements and scientific scope fences are unchanged. |

## Numbers recomputed

| Claim | Route | Result |
|---|---|---|
| Both scores remain L2D | L2 and minimum of C,C,C,D,D | Match |
| Prior 494 library and 7 serde tests | Parse and rehash stored baseline Cargo log | Match; not newly executed |
| Prior 17 selected mutants | Rehash each log; check compilation succeeded and exact intended test failed | Match; no exhaustive-coverage claim |

## Scanner and remaining checks

Strict changed-since scanner and focused contract regression results are stored
in review_verification.json. Full hosted checks must pass on the repaired head
before merge. The protected Rust files, exact-source baseline exceptions and
scientific records are unchanged; a sparse checkout was used after full-checkout
creation exhausted local disk space.

The scanner cannot infer completeness of obligation lists, actual functor laws
or a categorical theorem from these mutable metadata shells. Those scope fences
remain explicit. No node needs narrowing or reverting in this PR.
