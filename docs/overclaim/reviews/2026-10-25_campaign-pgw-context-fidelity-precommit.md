# Review of campaign PGW-CONTEXT-FIDELITY

Scope: branch `derive/PGW-CONTEXT-FIDELITY` against `origin/main` `7fa69d621`. Reviewed against the statement written by `dag/sync_pregenesis_to_wdp.py` from `dag/fragments/pregenesis_to_wdp.json`. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only `propext`, `Classical.choice` and `Quot.sound`.

Method: read `.claude/skills/overclaim-hunter/SKILL.md` and `rubric.md`; ran `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3). Read `lean4/CampaignPgwContextFidelity.lean` and the `#print axioms` lines from `lake build CampaignPgwContextFidelity` (Lean 4.35.0, Mathlib `56a005855ea17e0b0958f73ec801ae140b0a1679`). Re-ran `checks/independent/pgw-context-fidelity.py` (38 conditions, 0 failures). Not rebuilt: Rust and cargo. No status was raised.

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| PGW-CONTEXT-FIDELITY | `stale_not_transferred`, `sound_iff_only_replay`, `answers_follow_received_history` in `lean4/CampaignPgwContextFidelity.lean` | NARROWED | The standing statement is the two-value carrier. The trial transcript stays in the bottleneck. Status stays OPEN. |

## Statement versus theorem

| Claim in the standing statement | Declaration | Verdict |
|---|---|---|
| Replay is the left fold from false; `supplyDiamond` keeps the value and `designateA` sets it true | `replay` and `replayStep` (`lean4/CampaignPgwContextFidelity.lean:29-34`); `replay_supply` line 95; `replay_full` line 97 | FULL |
| When `s` differs from `s'`, some one-step trace is valid at `s'` and not at `s` | `stale_not_transferred` line 56 | FULL |
| A contract preserves trace validity at `replay(H)` if and only if it accepts a binding only when the context equals `replay(H)` | `sound_iff_only_replay` line 88, using `ContractSound` line 69 | FULL |
| History `supplyDiamond` replays to false and the only-diamond answer is verified | `replay_supply` line 95; `truncated_verified` line 99; `answers_follow_received_history` line 107 | FULL |
| History `supplyDiamond` then `designateA` replays to true and the only-diamond answer is retracted | `replay_full` line 97; `full_retracted` line 103 | FULL |
| Trial 2 Result 15, Prompt 12, Prompt 17, and the Rust `certifies` predicate | not proved; bottleneck of the node | NOT PROVED |

## Axioms

`sound_implies_equal` and `sound_iff_only_replay` use `propext`, `Classical.choice` and `Quot.sound`. `stale_not_transferred`, `separatingStep_valid`, `separatingStep_invalid`, `truncated_verified`, `full_retracted` and `answers_follow_received_history` use `propext`. `acceptEqual_sound`, `equal_implies_sound`, `replay_supply`, `replay_full`, `unequal_pair_count` and `history_count` use no axioms. No `sorry`, `admit`, `axiom`, `native_decide` or `unsafe`.

## Numbers recomputed

| Where | Claimed | Recomputed | Match |
|---|---|---|---|
| Unequal state pairs | 2 | `unequal_pair_count` reduces to 2; the Python script counts the same filtered pairs | Match |
| Histories of length at most 2 | 7 | `history_count` reduces to 7; the Python script enumerates 1 + 2 + 4 lists | Match |
| `replay([supplyDiamond])` | false | `replay_supply` and the Python replay | Match |
| `replay([supplyDiamond, designateA])` | true | `replay_full` and the Python replay | Match |
| Independent check | 38 conditions, 0 failures | re-ran `python -I -X utf8 checks/independent/pgw-context-fidelity.py` | Match |

README inventory lines and the evidence grade census were rewritten by `scripts/build_readme_facts.py --write` and `dag/evidence/build_evidence.py --write`. Those counts are the scripts' output, not a hand census. The evidence rebuild also stops listing result paths as missing when the files are present in this checkout. That is a generator refresh, not a new theorem.

## Scanner output

HIGH 0, MEDIUM 0. LOW 3, all pre-existing and outside this carrier: R10 on `TENSOR-ASSUMPTION-COUNTERMODELS`; R5 number `20261019` in `dag/derivations/10_finite_qm_core/tfq_1019_fq_gap_tensor_uniqueness.md`; R5 numbers `1/2` and `1/4` in `dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md`. They surfaced because the required tensor-receipt re-pin touches those nodes. Not changed here.

## What is open

The node stays OPEN. The two-value carrier is not the sealed Genesis grammar, and `ValidTrace` here is not `certifies`.
