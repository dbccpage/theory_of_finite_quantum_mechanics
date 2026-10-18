# Team 02 — Tao matrix and isolated-orbit tests

**Target:** G1. **AuthorityEffect:** None. **Status:** exact-algebra candidates and a synthetic fixture, with no established orbit-wide exclusion.

## Source and certificate boundary

The [round-one manifest](../../round1_manifest_500.json) (`manifest_sha256: 4ff7e82c98c92251f5aac24dd14534880a0e3b4a717d7c2dbcf5829ba69f93c4`) lists 50 proposals from 25 Team 02 sessions. Their local four-cycle records have seven post-`CUT` zero defects and 18 positive residuals. The five Round 2 sessions treat tangent rank, cross-ratios, Tao-orbit transitions, a synthetic moment fixture, and synthesis. This supports a map of candidate checks; it does not support an orbit-wide MU compatibility claim. The narrowest reusable artifact is the explicit cubic-root matrix written in [SESSION_R2_PROMPT_T02_02](../../round2_sessions/team_02_prompt_02.md). The next test is to check its Hadamard equations and tangent Jacobian with exact cyclotomic arithmetic.

The Round 2 trace in [SESSION_R2_PROMPT_T02_07](../../round2_sessions/team_02_prompt_07.md) changes `1/4` to `0` at `VERIFY` after its only `CUT` ended at `1/4`. Its displayed alternating dual vector is not divergence free on the directed four-cycle. The same defect appears in all five Team 02 Round 2 sessions. Thus their terminal graph state is not an independently checked certificate. Correct the trace and dual before promoting any Round 2 proposal. Round 2 IDs such as `PROP_PROMPT_T02_07_A` reuse Round 1 IDs; use the round and `SESSION_R2_...` identifier together. The A/B payloads describe graph moves rather than Tao-specific rank, phase, or moment data.

## Candidate vectors

| Source and proposal | Recorded support | What it does not support; narrowest claim | Next test |
|---|---|---|---|
| [SESSION_R2_PROMPT_T02_02](../../round2_sessions/team_02_prompt_02.md), `PROP_PROMPT_T02_02_A` | Prints a 6×6 cubic-root candidate matrix and asserts a 50-column tangent Jacobian has full rank. | No Jacobian coefficients, pivots, or row-reduction receipt is included. The rank is a testable claim about that matrix, not a checked isolation result. | Construct the dephased tangent matrix exactly over the relevant number field; publish pivots and verify rank in two runtimes. |
| [SESSION_R2_PROMPT_T02_05](../../round2_sessions/team_02_prompt_05.md), `PROP_PROMPT_T02_05_A` | Every nonzero entry in the displayed Tao matrix belongs to `{1,ω,ω²}`; products and quotients of such entries also lie there. | The entrywise fact excludes cross-ratio `-1` for that displayed matrix, but says nothing by itself about MU partners or the whole orbit. | Recompute all 225 cross-ratios from the exact matrix and check the equivalence-invariant multiset. |
| [SESSION_R2_PROMPT_T02_07](../../round2_sessions/team_02_prompt_07.md), `PROP_PROMPT_T02_07_A` | Writes the transition condition for a phase/permutation partner. | Its statement that 720 permutations and diagonal phases yield only a finite list overlooks continuous diagonal phases. This is a proposed elimination problem, not an orbit exclusion. | Keep phases symbolic and use exact elimination or a rational interval cover over the full phase torus, with permutation-coset reduction justified. |
| [SESSION_R2_PROMPT_T02_10](../../round2_sessions/team_02_prompt_10.md), `PROP_PROMPT_T02_10_A` | Gives the negative rational target `-5046587/129600` for a synthetic degree-eight moment fixture. | The matrices `M₈`, `W₈`, and exact `LDLᵀ` factors are absent. Even a checked trace would address the stated synthetic fixture only. | Publish the indexed matrices, PSD factorization, exact trace, and a map from any intended real candidate to the fixture assumptions. |

## Gap and next priority

[SESSION_R2_PROMPT_T02_25](../../round2_sessions/team_02_prompt_25.md) combines the proposed tangent, curvature, and moment arguments into an orbit-wide statement without their replayable certificates. The narrowest defensible output is a dependency plan. Begin with the cubic-root cross-ratio census and exact tangent-rank receipt; treat the phase-uniform transition test as a separate continuum obligation. A zero local graph residual in [SESSION_PROMPT_T02_25](../../round1_sessions/team_02_prompt_25.md) does not replace it.
