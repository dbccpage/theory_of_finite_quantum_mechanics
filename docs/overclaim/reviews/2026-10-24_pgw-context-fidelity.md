# Review of PGW-CONTEXT-FIDELITY

Scope: campaign derive/PGW-CONTEXT-FIDELITY against origin/main 1fa451fe1eac640d84f0c34ba88a71dcdd32dfb6. Reviewed against the statements as they stand in this worktree. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: `scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH=0 MEDIUM=0 LOW=3). Read the PGW-CONTEXT-FIDELITY statement and bottleneck, the TFQ-0427 record, `lean4/CampaignPgwContextFidelity.lean`, the replay receipt, and `checks/independent/pgw-context-fidelity.py` (`checked 23 claims, failures 0`). Lake build of `CampaignPgwContextFidelity` completed with empty axiom lists before this review. Cargo was not run. The trial record was not treated as a checked source.

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. Status stays OPEN. record_status stays OPEN_OBLIGATION. AuthorityEffect stays None.

Corrections to the PR's own text:

- None. The narrowed statement matches the two-code theorems. Trial 2 Result 15, Prompt 12, Prompt 17, and a general ValidTrace semantics stay unresolved.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| PGW-CONTEXT-FIDELITY | `pgwContext_codes_differ` (`lean4/CampaignPgwContextFidelity.lean:24`), `pgwContext_empty_claim_on_stale` (`:27`), `pgwContext_empty_claim_on_replay` (`:30`), `pgwContext_binding_refuses_stale` (`:33`), `pgwContext_binding_accepts_match` (`:37`), `pgwContext_accept_count` (`:41`) | NARROWED | One two-code witness. Status stays OPEN. |

Atomic claims:

| Claim | Match |
|---|---|
| Stale context code is 0 and replayed context code is 1 | `pgwContextStale` and `pgwContextReplay` |
| The codes differ | `pgwContext_codes_differ` |
| Empty-claim step holds at 0 | `pgwContext_empty_claim_on_stale` |
| Empty-claim step fails at 1 | `pgwContext_empty_claim_on_replay` |
| Binding refuses (0, 1) | `pgwContext_binding_refuses_stale` |
| Binding accepts (1, 1) | `pgwContext_binding_accepts_match` |
| Exactly two of the four ordered pairs from {0, 1} are accepted | `pgwContext_accept_count` |
| Trial 2, Prompt 12, Prompt 17, general ValidTrace | stated as unresolved; no declaration decides them |

`#print axioms` for all six theorems: does not depend on any axioms. No `sorry`, `admit`, `axiom`, `native_decide`, or `unsafe` in the new module.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| Context codes | 0 and 1 | definitions; `0 ≠ 1` | match |
| Empty claim | holds at 0, fails at 1 | `ctx == 0` | match |
| Binding | refuses (0, 1), accepts (1, 1) | equality of the codes | match |
| Pair census | 2 of 4 | the pairs (0, 0), (0, 1), (1, 0), (1, 1) | match |
| Independent check | 23 claims, 0 failures | `python -I -X utf8 checks/independent/pgw-context-fidelity.py` | match |
| Lake build | exit 0, wall 17.429s, module job 957ms | receipt | match |
| README facts | nodes 925, routes 934, records 977, failures 3; lean refs 2286; lean4 files 999; Lake 90 / 942 | `build_readme_facts.py --check` current | match |
| Validator | failures=3 | pre-existing unknown key `python` on three import nodes | left as on main |

## Scanner output

HIGH 0, MEDIUM 0. LOW findings are outside this node and were left in place: R10 `TENSOR-ASSUMPTION-COUNTERMODELS`; R5 on `tfq_1019_fq_gap_tensor_uniqueness.md` (`20261019`); R5 on `tfq_0413_tensor_assumption_countermodels.md` (`1/2`, `1/4`). No baseline entry proposed. `sync_pregenesis_to_wdp.py --check` stays stale, including the four TFQ-0519 paths. That phrase was not rewritten. The hand-edited TFQ-0427 paper is also stale against a full pregenesis render, and that render was not run.
