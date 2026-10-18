# Team 06 — projector words and reduction

**AuthorityEffect:** None.  
**Firewall Line:** `stated region only; mints no authority`

## Source and focus

Team 06's 25 Round 1 sessions range from [`SESSION_PROMPT_T06_01`](../../round1_sessions/team_06_prompt_01.md) to [`SESSION_PROMPT_T06_25`](../../round1_sessions/team_06_prompt_25.md). The [Round 1 manifest](../../round1_manifest_500.json) (`SYMBOL_GAME_ROUND_1_MANIFEST_V1`, SHA-256 `4ff7e82c98c92251f5aac24dd14534880a0e3b4a717d7c2dbcf5829ba69f93c4`) records 50 proposals for this team: 25 scored 100, 25 scored 99, and 14 with graph defect recorded as zero. Those scores measure the four-vertex Symbol Game packet; they are not a word-algebra or moment-soundness certificate. The focus spans formal words, involution, same-basis reduction, dimensions, commutators, and Lean interfaces (Round 1 prompts [03](../../round1_sessions/team_06_prompt_03.md), [06](../../round1_sessions/team_06_prompt_06.md), [08](../../round1_sessions/team_06_prompt_08.md), [12](../../round1_sessions/team_06_prompt_12.md), [22](../../round1_sessions/team_06_prompt_22.md)).

## Best vectors and gaps

| Vector and source | What it supports | What it does not support; narrowest claim | Next test |
|---|---|---|---|
| Orient idempotency, same-basis orthogonality, and one completeness equation for exact rewriting ([`SESSION_R2_PROMPT_T06_03`](../../round2_sessions/team_06_prompt_03.md)). | A concrete rule set and an example critical-pair reduction. | The one example does not establish termination and confluence for every overlap. Narrowest claim: these three rule families are candidate rewrite rules. | Enumerate all critical overlaps, show each joins, prove a decreasing order, and compare normal forms with direct quotient reductions. |
| Enumerate reduced words through length four ([`SESSION_R2_PROMPT_T06_08`](../../round2_sessions/team_06_prompt_08.md)). | A proposed census of 21 words through degree one after eliminating one outcome per basis. | The larger counts rely on a complete canonical-basis argument. Narrowest claim: the 21 count follows from the proposed degree-one elimination; it conflicts with the claimed 25 independent degree-one words in [`SESSION_R2_PROMPT_T07_01`](../../round2_sessions/team_07_prompt_01.md). | Derive independence and spanning in the actual quotient, then reconstruct each moment index set from that basis. |
| Word reversal as involution ([`SESSION_R2_PROMPT_T06_16`](../../round2_sessions/team_06_prompt_16.md)). | A precise anti-automorphism target for Lean. | The transcript names a Lean theorem, while the current [word definitions](../../../../lean4/sdp/MomentPositivityObligation.lean) define `Word.inv` without that theorem. Narrowest claim: the operation is defined on formal words. | Add and kernel-check the concatenation identity and its compatibility with quotient relations. |
| A canonical projector quotient ([`SESSION_R2_PROMPT_T06_25`](../../round2_sessions/team_06_prompt_25.md)). | A useful formalization target. | The current [`ProjectorWordAlgebra`](../../../../lean4/sdp/TargetQArchimedeanPositivstellensatz.lean) stores a count and a list of relation labels; it does not encode multiplication, quotient equality, or unique normal forms. Narrowest claim: the Lean file contains metadata for a proposed algebra. | Build the actual free algebra, star ideal, normalization function, and soundness/completeness lemmas. |

The noncommutativity discussion in [`SESSION_R2_PROMPT_T06_12`](../../round2_sessions/team_06_prompt_12.md) is a research direction. The stated growth conclusion is not derived from the shown commutator observation. Trace constraints also need an explicit algebraic or tracial-state encoding before they can participate in this quotient.

## Claim boundary

**Supports:** a scoped rewrite-system design and exact rational local graph packets. **Does not support:** a certified canonical basis or a bridge from word reductions to physical rank-one projectors. **Narrowest claim:** Team 06 identifies algebraic definitions and checks needed before moment matrices can use reduced words. **Next test:** finish the quotient and confluence checks, then rerun exact moment indexing against completeness. The Round 2 cycle witness common to this team has entries `(1/4,-1/4,1/4,-1/4)` and net divergence `1/2` at vertex `q_proj_v1`, contrary to its recorded zero-divergence label ([`SESSION_R2_PROMPT_T06_03`](../../round2_sessions/team_06_prompt_03.md)); its zero graph defect does not certify the Q target.
