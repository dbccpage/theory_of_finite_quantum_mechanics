# Team 09 — rank loops and GNS extraction

**AuthorityEffect:** None.  
**Firewall Line:** `stated region only; mints no authority`

## Source and focus

The 25 Round 1 sessions run from [`SESSION_PROMPT_T09_01`](../../round1_sessions/team_09_prompt_01.md) to [`SESSION_PROMPT_T09_25`](../../round1_sessions/team_09_prompt_25.md). The [Round 1 manifest](../../round1_manifest_500.json) (`SYMBOL_GAME_ROUND_1_MANIFEST_V1`, SHA-256 `4ff7e82c98c92251f5aac24dd14534880a0e3b4a717d7c2dbcf5829ba69f93c4`) records 50 proposals, split 25 at score 100 and 25 at 99; 14 record zero four-vertex graph defect. The team's mathematical focus is exact ranks of truncated moments, flatness checks, GNS extraction, and Lean rank-loop interfaces (Round 1 prompts [03](../../round1_sessions/team_09_prompt_03.md), [07](../../round1_sessions/team_09_prompt_07.md), [13](../../round1_sessions/team_09_prompt_13.md), [21](../../round1_sessions/team_09_prompt_21.md)).

## Best vectors and gaps

| Vector and source | What it supports | What it does not support; narrowest claim | Next test |
|---|---|---|---|
| Exact rational row reduction on named moment fixtures ([`SESSION_R2_PROMPT_T09_03`](../../round2_sessions/team_09_prompt_03.md), [`SESSION_R2_PROMPT_T09_07`](../../round2_sessions/team_09_prompt_07.md)). | An implementable rank diagnostic with zero tolerance and proposed dimensions/ranks. | The stated `rank(M2)=25` contradicts projector completeness: for each basis, `-1+sum_a Pi_(i,a)` is a nonzero coefficient vector in the 25-index moment kernel. Narrowest claim: the reported rank sequence is a hypothesis about fixtures whose relation compliance has not been demonstrated. | Reconstruct each rational matrix, check all linear constraints, then calculate rank with exact elimination and retained pivots. |
| A flatness test for GNS extraction ([`SESSION_R2_PROMPT_T09_10`](../../round2_sessions/team_09_prompt_10.md)). | The right research target: a positive functional, a null space, and multiplication on its quotient. | At a truncated degree, left multiplication can leave the domain; null-space stability and a valid extension need separate arguments. Narrowest claim: the transcript sketches a GNS construction. | Supply a positive, relation-compatible flat extension and prove multiplication is well-defined on the quotient. |
| Claimed forced rank growth ([`SESSION_R2_PROMPT_T09_13`](../../round2_sessions/team_09_prompt_13.md)). | A falsifiable conjecture about particular moment fixtures. | No exact rank data or frame-potential derivation is supplied for the asserted contradiction. Completeness itself supplies linear relations and cannot by itself force strictly increasing rank. Narrowest claim: this is an unverified proposed obstruction. | Test the claim against relation-compatible finite-dimensional projector examples, then state any surviving restricted hypothesis. |
| Lean rank-loop route ([`SESSION_R2_PROMPT_T09_21`](../../round2_sessions/team_09_prompt_21.md)). | A conditional interface for using rank closure. | The current [Lean theorem](../../../../../../../../../lean4/MomentPositivityObligation.lean) takes `loop_cert` and `h_gns_exhaust` as inputs; the latter says every physical realization matches the one refuted candidate. Narrowest claim: the file records an implication under this strong coverage assumption. | Encode and verify a concrete flat moment extension and derive the needed coverage statement from its actual semantics. |

The team's Round 2 packets also reuse a cycle vector `(1/4,-1/4,1/4,-1/4)` whose net divergence at `q_proj_v1` is `1/2`, despite a zero-divergence label ([`SESSION_R2_PROMPT_T09_07`](../../round2_sessions/team_09_prompt_07.md)). The recorded graph descent is not a rank-loop certificate.

## Claim boundary

**Supports:** a focused exact-rank and flat-extension work plan. **Does not support:** the listed rank sequence, forced rank growth, or a constructed physical representation. **Narrowest claim:** Team 09 identifies checks required for a valid GNS extraction, while its numeric rank starting point conflicts with completeness. **Next test:** repair the degree-one matrix, publish exact rank receipts, and formalize flatness together with relation and dimension constraints.
