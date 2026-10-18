# Team 01 — Fourier and Diță affine charts

**Target:** G1. **AuthorityEffect:** None. **Status:** research leads, with no established orbit classification or global nonextendibility result.

## Source and certificate boundary

The [round-one manifest](../../round1_manifest_500.json) (`manifest_sha256: 4ff7e82c98c92251f5aac24dd14534880a0e3b4a717d7c2dbcf5829ba69f93c4`) lists 50 proposals from 25 Team 01 sessions. Their four-vertex cochain records have seven post-`CUT` zero defects and 18 positive residuals. The five [round-two sessions](../../round2_sessions/team_01_prompt_25.md) revisit prompts 01, 04, 08, 16, and 25. These counts support only an inventory of the recorded Symbol Game runs; they do not certify the Diță torus, its parameter cover, or its orbit boundary. The narrowest usable result is a set of local rational graph examples awaiting independent replay. The next test is to replay the graph certificates and connect each graph relation to explicit Hadamard matrix equations.

The Round 2 trace in [SESSION_R2_PROMPT_T01_08](../../round2_sessions/team_01_prompt_08.md) has one `CUT` from `7/3` to `1/4`, followed by a terminal `VERIFY` from `1/4` to `0`. Its displayed alternating dual values `1/4, -1/4, 1/4, -1/4` are not divergence free on the directed four-cycle. The same pattern occurs in the other four Team 01 Round 2 sessions. This supports a concrete audit finding, not their stated terminal certificate. The next test is a corrected exact trace with a valid dual vector and a replayable state transition. Round 2 reuses Round 1 proposal IDs such as `PROP_PROMPT_T01_08_A`; round and session ID are necessary to identify a proposal. Its A/B payloads contain graph moves, while the Diță-specific assertions are in session prose.

## Candidate vectors

| Source and proposal | Recorded support | What it does not support; narrowest claim | Next test |
|---|---|---|---|
| [SESSION_R2_PROMPT_T01_04](../../round2_sessions/team_01_prompt_04.md), `PROP_PROMPT_T01_04_A` | Specifies six Diță seed points and a proposed 225 cross-ratio census over cyclotomic entries. | No six explicit matrices or exponent table is supplied. It is a seed-census specification, not an orbit-invariant certificate. | Enumerate each exact seed matrix and all 225 cross-ratios; check phase/permutation equivalence and perturbation controls. |
| [SESSION_R2_PROMPT_T01_08](../../round2_sessions/team_01_prompt_08.md), `PROP_PROMPT_T01_08_A` | Gives a proposed box `[0,1/180]^2`, residual bound `37249/90000`, Lipschitz value `85/9`, and derived margin `12133/30000`. | No residual polynomial list, rational interval leaves, or coverage record is present. The displayed rational subtraction is a candidate local calculation only. | Publish exact ZeroRel equations, interval enclosures, box containment and overlap checks, then replay every leaf. |
| [SESSION_R2_PROMPT_T01_16](../../round2_sessions/team_01_prompt_16.md), `PROP_PROMPT_T01_16_A` | Proposes the coordinate transition `(α,β) ↦ (α,β,0)` into a Karlsson boundary chart. | No explicit Karlsson matrix identity or verified overlap is supplied. This is a chart-map conjecture, not a glued cover. | Check equality up to allowed gauge/permutations with exact matrix formulas and verify the boundary in active coordinates. |

## Gap and next priority

[SESSION_R2_PROMPT_T01_25](../../round2_sessions/team_01_prompt_25.md) assembles named cover and gap lemmas into a claimed Diță/Fourier theorem. The session does not include the leaf receipts or Lean theorem bodies. The narrowest defensible claim is that the program identifies a dependency chain. The best next step is the bounded seed-box replay from prompt 08, followed by a separately checked chart transition from prompt 16. A local four-cycle defect of zero in [SESSION_PROMPT_T01_25](../../round1_sessions/team_01_prompt_25.md) does not discharge those dependencies.
