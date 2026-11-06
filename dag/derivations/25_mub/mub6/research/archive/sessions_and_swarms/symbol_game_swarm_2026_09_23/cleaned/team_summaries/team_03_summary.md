# Team 03 — Szöllősi family, Haagerup point, and cusp charts

**Target:** G1. **AuthorityEffect:** None. **Status:** chart and interval proposals with unresolved algebraic premises.

## Source and certificate boundary

The [round-one manifest](../../round1_manifest_500.json) (`manifest_sha256: 4ff7e82c98c92251f5aac24dd14534880a0e3b4a717d7c2dbcf5829ba69f93c4`) lists 50 proposals from 25 Team 03 sessions; seven recorded graph cuts end at zero and 18 leave positive residuals. Round 2 selects prompts 03, 06, 08, 10, and 25. This supports an inventory of proposed exact-algebra and cusp-cover work, not a classification of the Szöllősi family. The narrowest claim is that the sessions specify potential identities and rational margins for testing. The next test is to produce the parameterized matrices and residual polynomials before attaching graph data to them.

The only Round 2 `CUT` in [SESSION_R2_PROMPT_T03_08](../../round2_sessions/team_03_prompt_08.md) ends at `1/4`; a terminal `VERIFY` then reports `0`. Its alternating dual values fail the directed-cycle divergence check. This pattern repeats in all five Team 03 Round 2 sessions. Their terminal zero is a recorded assertion, not a checked local certificate. Correct the trace and supply a valid dual or exact section. Round 2 proposals reuse Round 1 IDs, so `PROP_PROMPT_T03_08_A` alone is ambiguous. The A/B payloads do not contain the cusp polynomials or interval leaves discussed in the prose.

## Candidate vectors

| Source and proposal | Recorded support | What it does not support; narrowest claim | Next test |
|---|---|---|---|
| [SESSION_R2_PROMPT_T03_03](../../round2_sessions/team_03_prompt_03.md), `PROP_PROMPT_T03_03_A` | Suggests an algebraic description of a Haagerup point over `Q(√3,i)`. | The source also places that point on `B₆(θ)` while asserting positive distance from the same family. Both cannot hold as stated; no isolated-orbit certificate follows. | Supply an exact matrix, clarify the family relation, and compute a certified tangent rank and invariant spectrum. |
| [SESSION_R2_PROMPT_T03_06](../../round2_sessions/team_03_prompt_06.md), `PROP_PROMPT_T03_06_A` | Identifies transition-matrix entry moduli as the right pairwise MU test. | The function `f(θ₁,θ₂)` and its claimed vanishing locus are not given. The narrowest claim is a proposed obstruction equation. | Derive exact entry formulas on a correct parameter domain; solve all modulus-one equations, including endpoint and gauge cases. |
| [SESSION_R2_PROMPT_T03_08](../../round2_sessions/team_03_prompt_08.md), `PROP_PROMPT_T03_08_A` | Proposes blow-up coordinates near a Segre-locus cusp. | The displayed substitution divides by `u`, leaving `u=0` untreated; the corner polynomial and claimed factorization are absent. It is one candidate chart, not a desingularized cover. | State the exact corner polynomial, verify factorization and exceptional divisor, and add/check complementary charts. |
| [SESSION_R2_PROMPT_T03_10](../../round2_sessions/team_03_prompt_10.md), `PROP_PROMPT_T03_10_A` | Displays the rational arithmetic `19/100 − (142/15)(1/1000) = 2708/15000 > 0`. | No certified base margin, derivative bound, or list of cusp cells is supplied. The narrowest claim is a conditional gap calculation. | Produce rational interval proofs of both inputs on every chart and a coverage/overlap receipt. |

## Gap and next priority

The [round-one cusp prompt](../../round1_sessions/team_03_prompt_08.md) records a four-vertex defect of `1/12`, which is unrelated to a verified blow-up of the Hadamard corner variety. [SESSION_R2_PROMPT_T03_25](../../round2_sessions/team_03_prompt_25.md) cites continuous chaining and cusp work without their exact artifacts. Prioritize resolving the Haagerup-family contradiction and constructing a complete algebraic cusp atlas. Those bounded checks precede any family-wide nonextendibility statement.
