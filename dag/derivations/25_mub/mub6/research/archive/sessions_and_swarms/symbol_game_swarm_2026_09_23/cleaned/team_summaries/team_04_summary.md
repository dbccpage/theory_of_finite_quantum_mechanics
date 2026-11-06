# Team 04 — Karlsson boundary and chart coverage

**Target:** G1. **AuthorityEffect:** None. **Status:** proposed interface invariants without a replayable cover.

## Source and certificate boundary

The [round-one manifest](../../round1_manifest_500.json) (`manifest_sha256: 4ff7e82c98c92251f5aac24dd14534880a0e3b4a717d7c2dbcf5829ba69f93c4`) lists 50 Team 04 proposals from 25 sessions. Seven four-cycle cuts record zero residual; 18 retain positive residual. Round 2 selects prompts 02, 07, 10, 11, and 25. The inventory supports a decomposition of work into degeneration, boundary adjacency, circulation, and volume checks. It does not establish coverage of a Karlsson manifold. The narrowest claim is a list of proposed exact checks. The next test is to supply explicit parameter maps and the actual partition leaves.

In [SESSION_R2_PROMPT_T04_11](../../round2_sessions/team_04_prompt_11.md), the only `CUT` ends at `1/4`, while terminal `VERIFY` reports `0`; its alternating dual vector fails divergence on the displayed directed four-cycle. All five Team 04 Round 2 sessions share this trace defect. Their terminal state is not a checked certificate. Repair the graph witness before using any Round 2 defect value. A proposal ID such as `PROP_PROMPT_T04_11_A` occurs in both rounds and needs a round-qualified session citation. The A/B payloads contain graph moves rather than the boundary cells and transition maps described in the prose.

## Candidate vectors

| Source and proposal | Recorded support | What it does not support; narrowest claim | Next test |
|---|---|---|---|
| [SESSION_R2_PROMPT_T04_02](../../round2_sessions/team_04_prompt_02.md), `PROP_PROMPT_T04_02_A` | Proposes a Karlsson-to-Diță limit at `z=0` and rank-two boundary embedding. | No parameterized Karlsson matrix or Jacobian is supplied. It is a candidate degeneration map, not a checked chart identity. | Write both exact matrix families, verify equality up to allowed equivalence, and compute the boundary Jacobian and singular strata. |
| [SESSION_R2_PROMPT_T04_07](../../round2_sessions/team_04_prompt_07.md), `PROP_PROMPT_T04_07_A` | Specifies adjacency between 28 collar boxes and Karlsson boundary faces, with a proposed rational margin `12133/30000`. | Neither box/facet endpoints nor a full boundary-domain definition appear. The narrowest claim is an overlap-check plan. | Publish all cells; check dimensions, containment, active-coordinate relative volume, every relative-interior overlap, and per-cell margins. |
| [SESSION_R2_PROMPT_T04_10](../../round2_sessions/team_04_prompt_10.md), `PROP_PROMPT_T04_10_A` | Proposes Čech transition products and a circulation threshold `12133/5000`. | No transition matrices, loop basis, or edge cochain is supplied. The threshold is not a checked topological obstruction. | Verify exact cocycle identities on each triple overlap and replay circulation on a justified generating-loop list. |
| [SESSION_R2_PROMPT_T04_11](../../round2_sessions/team_04_prompt_11.md), `PROP_PROMPT_T04_11_A` | States that 28 leaf volumes sum to one in normalized five-dimensional coordinates. | The leaf list is absent; a volume sum alone cannot establish union coverage or disjointness. The narrowest claim is a proposed aggregate check. | Supply leaf coordinates and independently check containment, pairwise relative interiors, boundary face matching, and exact union volume. |

## Gap and next priority

[SESSION_R2_PROMPT_T04_25](../../round2_sessions/team_04_prompt_25.md) depends on the unlisted cells and chart transitions while asserting a Lean result. No proof body or cover receipt is included in that session. Begin with an explicit boundary map and complete cell inventory, then replay the rational overlap and volume checks. The local graph residual in [SESSION_PROMPT_T04_25](../../round1_sessions/team_04_prompt_25.md) does not bridge to geometric coverage.
