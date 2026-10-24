# Functor shell scope review

AuthorityEffect: None.

Scope: codex/functor-shell-validation, source tree 53a75069ce0173c717b6d88d665417e6703d0d87,
base 5b22322289839eaa308c91b01500225aa31ddaba. This is a model-authored scope review, not an
independent human approval or a categorical theorem.

Method: read both implementations, the supplied review, the source-bound
contracts, guard tests, serde boundaries, mutation recipes and raw logs. Cargo
was run separately for the category snapshot and the standalone governance crate.
Lean and Mathlib were not rebuilt; neither changes in this PR. The strict scanner
output is retained in evidence/quality/functor_shell_pr/acceptance_checks.json.

Result: 0 nodes FULL, 0 NARROWED, 0 OVERCLAIM. No node is affected or raised.
The custody.json receipt verifies the unchanged DAG, sealed prompt blobs,
global policy and historical contract bytes.

Corrections to the proposal and assessment:
- Partial pair lists and raw deserialization do not certify a functor
  (code/rust/src/category_theory/functor/functor.rs:10).
- Coverage of supplied target-arrow obligations does not quantify over every
  source-object pair, so it does not certify fullness
  (code/rust/src/category_theory/functor/full_functor.rs:3).
- Repeated witness copies count once. Collisions across different source Hom-sets
  do not refute faithfulness
  (code/rust/src/category_theory/functor/full_functor.rs:217).
- Both assessments remain L2D. Explicit user approval authorizes only the named
  exact-source baseline exceptions; it does not establish L4 capability.
  Earlier no-exception reviews and failed-policy receipts remain historical records.

## Per-node table

| Node | Evidence | Verdict | Reason |
|---|---|---|---|
| None | Unchanged dag/derivation_dag.json bytes against the base | Not applicable | No scientific claim or status changes. |

## Statement versus implementation

| Claim | Evidence | Boundary |
|---|---|---|
| Nonblank names/tags and unique source keys | functor.rs:74, isolated guard tests from functor.rs:158 | String shape and partial maps only. |
| Explicit owned admission and image lookup | functor.rs:109, functor.rs:117, functor.rs:127, serde tests in replay | Public mutation/raw Deserialize remain unchecked; no persistent certificate. |
| Supplied-obligation coverage and strict map agreement | full_functor.rs:129, full_functor.rs:244, full_functor.rs:280 | No enumeration completeness, category membership, identities or composition. |
| Diagnostics cannot establish actual fullness or nonfaithfulness | full_functor.rs:668 | Finite runtime counterexample using admitted finite categories, not a Lean theorem. |

## Numbers recomputed

| Claim | Recomputed route | Result |
|---|---|---|
| 494 library and 7 serde tests | Parse baseline Cargo log; replay.json | Match |
| 17 selected mutations: 5 Functor, 12 FullFunctor | Each compiles and fails its exact intended test with exit 101; replay.json | Match; no exhaustive coverage percentage |
| 65 governance tests; 1 ignored doctest | Raw Cargo output in acceptance_checks.json | Match |
| 105 Python tests | Final pytest output in campaign_checks.json | Match |
| 18 campaign checks | Count zero-exit command records | Match |
| L2D for each source | L2 capability assessment; minimum of C,C,C,D,D is D | Match; exception does not rescore |
| 9 / 23 production functions; 18 / 25 subject tests | Source scan in custody.json plus manual review | Match |
| 2 missing cross-object Hom-pair lifts | full_functor.rs:668 constructs the discrete-to-terminal example and enumerates source pairs | Match |
| 177 sealed prompts and 925 statuses unchanged | Complete base-versus-candidate blob comparison in custody.json | Match |
| 8,152 other baseline entries unchanged | Exact mapping comparison in custody.json | Match |
| README Rust test inventory 7,014 to 7,049, increase 35 | Generated facts plus source test inventory | Match; inventory is not a pass result |

## Scanner output and limits

Strict changed-since scan exits zero; existing main findings are not blanket
claims of correctness. The overclaim baseline is unchanged. The two governance
baseline reasons come from the explicit human instruction recorded in
exception_authorization.json; they are separate from the scanner baseline.

No mathematical node requires narrowing or reverting in this PR. Runtime tests
cannot decide completeness of the supplied obligation list or actual categorical
laws. Original category Cargo workspace/build-hook integration and optional
external packages were not compiled by the isolated harness. No Lean theorem
or full-workspace pass is asserted.
