# Team 07 — truncated moments and candidate refutations

**AuthorityEffect:** None.  
**Firewall Line:** `stated region only; mints no authority`

## Source and focus

The team's 25 Round 1 sessions run from [`SESSION_PROMPT_T07_01`](../../round1_sessions/team_07_prompt_01.md) to [`SESSION_PROMPT_T07_25`](../../round1_sessions/team_07_prompt_25.md). The [Round 1 manifest](../../round1_manifest_500.json) (`SYMBOL_GAME_ROUND_1_MANIFEST_V1`, SHA-256 `4ff7e82c98c92251f5aac24dd14534880a0e3b4a717d7c2dbcf5829ba69f93c4`) lists 50 Team 07 proposals, 25 scored 100 and 25 scored 99; 14 record zero four-vertex graph defect. The mathematical focus is exact rational moment construction, factored dual witnesses, cross-runtime replay, and fixed-candidate refutation (Round 1 prompts [06](../../round1_sessions/team_07_prompt_06.md), [08](../../round1_sessions/team_07_prompt_08.md), [09](../../round1_sessions/team_07_prompt_09.md), [22](../../round1_sessions/team_07_prompt_22.md)).

## Best vectors and gaps

| Vector and source | What it supports | What it does not support; narrowest claim | Next test |
|---|---|---|---|
| Exact moment indexing and rational pivots ([`SESSION_R2_PROMPT_T07_01`](../../round2_sessions/team_07_prompt_01.md)). | A proposed table of degree-one moments under a normalized tracial functional. | Its claim of 25 positive pivots conflicts with each completeness relation `sum_a Pi_(i,a)=1`: the coefficient vector `-1 + sum_a Pi_(i,a)` is in the moment kernel. Narrowest claim: the displayed entries are a candidate table, and a consistent 25-by-25 table has rank at most 21. | Recompute exact rank and pivots after enforcing all four completeness relations. |
| Factored witness against the fixed `X=0` completion at degrees six and eight ([`SESSION_R2_PROMPT_T07_06`](../../round2_sessions/team_07_prompt_06.md), [`SESSION_R2_PROMPT_T07_08`](../../round2_sessions/team_07_prompt_08.md)). | The sessions report exact trace value `-9071/10800` for that named completion. | Neither session includes the full matrix and factor vectors needed for independent replay. Narrowest claim: a negative trace is reported for the fixed fixture; it says nothing about other completions. | Reconstruct `M` and `W=L D L^T` from serialized rational data, check `D>=0`, and replay the trace with a sign-flip control. |
| Synthetic `S6` completion ([`SESSION_R2_PROMPT_T07_09`](../../round2_sessions/team_07_prompt_09.md)). | A second fixed candidate with reported degree-eight trace `-5046587/129600`. | The source does not establish that this fixture covers every physical operator state. Narrowest claim: the stated trace would refute this one matrix if its entries and witness replay exactly. | Pin its complete matrix, factorization, SHA-256, and Python/Rust agreement. |
| Lean conditional candidate lemma ([`SESSION_R2_PROMPT_T07_22`](../../round2_sessions/team_07_prompt_22.md)). | The current [`certified_candidate_refutation`](../../../../lean4/sdp/MomentPositivityObligation.lean) takes a nonnegative factored witness and a negative trace hypothesis and concludes failure of positivity for that candidate test space. | It does not construct the numerical witness or discharge its negative-trace hypothesis. Narrowest claim: the implication is formalized at the abstract test-space level. | Supply the exact serialized fixture and connect its evaluated trace to the Lean hypothesis. |

The [Q problem digest](../../steering_team/target_q_soundness_problem_digest.md) itself distinguishes a fixed candidate from physical realization. The common Round 2 four-edge witness is also internally inconsistent: entries `(1/4,-1/4,1/4,-1/4)` have net divergence `1/2` at `q_proj_v1`, while the packet labels divergence zero ([`SESSION_R2_PROMPT_T07_06`](../../round2_sessions/team_07_prompt_06.md)).

## Claim boundary

**Supports:** targeted tests of exact rational fixed-candidate moments and a conditional Lean refutation rule. **Does not support:** a negative result for every completion or a finished operator-state soundness bridge. **Narrowest claim:** the proposed witnesses, once independently replayed, can reject only the named matrices. **Next test:** repair the degree-one indexing contradiction, publish complete exact witness data, and verify each trace against a matrix that satisfies all projector linear relations.
