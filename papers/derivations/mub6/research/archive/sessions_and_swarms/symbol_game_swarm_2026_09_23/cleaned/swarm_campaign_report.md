# MUB(6) Symbol Game swarm: research inventory and next checks

**AuthorityEffect:** None. `stated region only; mints no authority`.

## Executive summary

The supplied export contains 250 Round 1 sessions, 50 Round 2 deep dives, and 500 Round 1 proposal IDs across ten teams. The observed source census is 320 files: 300 sessions, eight steering files, eight raw JSONL logs, and four top-level files. Teams 01–05 address the G1 orbit and triad program; Teams 06–10 address projector moment soundness. This deliverable preserves the 500 IDs in a structured [database](proposals_all_500.json), links each selected Round 2 follow-up to its Round 1 identity, and separates proposed mathematics from checked graph arithmetic. The original session and steering files were left in place.

The strongest replayable result within these session files is narrow. Using exact `Fraction` arithmetic on each printed four-edge graph, [`audit_source_graphs.py`](audit_source_graphs.py) finds that all 250 Round 1 sessions have balanced, bounded dual vectors whose values equal the cycle lower bound; all 250 proposed sections reproduce their reported post-cut residuals. Seventy graph instances have zero cycle obstruction and 180 retain a positive one. This supports only the printed local graph computations. The sessions do not provide a checked semantics map from those graphs to a Hadamard variety cell, a full projector moment cone, or a Lean theorem discharging either target. The [steering protocol](../steering_team/how_to_play_operationalization.md) itself requires such exact host recomputation.

Every one of the 50 Round 2 graph witnesses fails the directed-cycle divergence test: the shared alternating vector has divergence `(-1/2,1/2,-1/2,1/2)`. Each trace records a `CUT` ending at `1/4`, then a `VERIFY` changing the defect to `0`, while the A-proposal payload itself says the cut ends at `0`. The underlying cycle sum is zero and a zero-residual section exists, but the printed trace does not exhibit a consistent terminal cut/verification pair. Consequently, the Round 2 `defect=0`, dual-check labels, and `100/100` scores are source metadata pending repair, not target certificates. The [audit script](audit_source_graphs.py) and an [example G1 session](../round2_sessions/team_01_prompt_01.md) give the exact inputs.

For G1, the highest-value leads are explicit corner-elimination data, real branch coverage, continuous chart interfaces, and correctly indexed triad counting. The current [G1 digest](../steering_team/target_g1_problem_digest.md) poses orbit exhaustiveness as an open obligation; it does not certify the five-family catalog as exhaustive. Several Round 2 descriptions need correction before formalization, including a corner reconstruction premise that conflicts with rank six and a seven-basis count that includes the fixed identity basis. The current Lean [`target_g1_orbit_exhaustiveness_theorem`](../../../lean4/gluing/TargetG1OrbitExhaustiveness.lean) has classification, transition, bridge, and gluing hypotheses in its type; this is a conditional dependency path.

For Q-Soundness, exact fixed-candidate dual traces, projector word reduction, and a typed quadratic-module checker are useful next artifacts. The [Q digest](../steering_team/target_q_soundness_problem_digest.md) distinguishes a refuted candidate from all physical realizations. The Round 2 rank-25 claim conflicts with four projector-completeness relations on the 25 unreduced degree-one words. The current Lean [`sound_universal_exclusion_via_positivstellensatz`](../../../lean4/sdp/MomentPositivityObligation.lean) takes an `h_exhaust` premise that every realization matches the refuted candidate; [`sound_universal_exclusion_via_rank_loop`](../../../lean4/sdp/MomentPositivityObligation.lean) takes the analogous `h_gns_exhaust`. The same file's `PhysicalProjectorRealization` structure does not encode a rank-one condition, a dimension-six carrier, completeness, or mutual unbiasedness. These interfaces alone therefore do not supply the physical model or the required exhaustion premise.

| Scope check for this report | Statement |
|---|---|
| **Supports** | A traceable campaign inventory, exact replay of the printed local graphs, identified inconsistencies, and a prioritized test plan. |
| **Does not support** | Discharge of G1 orbit exhaustiveness, Q-Soundness, or a global MUB(6) bound. |
| **Narrowest defensible claim** | The Round 1 four-edge graphs admit the recorded exact dual checks; the Round 2 graph trace and several mathematical extrapolations need new receipts. |
| **Next test** | Repair one Round 2 graph receipt, then attach and independently check a typed map to one concrete matrix or projector obligation with a negative control. |

## Data handling and ranking method

The [manifest](../round1_manifest_500.json) contains 250 `CUT` entries scored 100 and 250 `VERIFY` entries scored 99. That score split follows move type and does not distinguish mathematical novelty. The [parser](build_proposals.py) checked all 500 Round 1 proposal payloads, reported digest fields, dual vectors, defects, prompt IDs, and targets field-for-field against their session files. It did not authenticate proposal digest values against a canonical payload encoding. Each of the 50 Round 2 sessions reuses its Round 1 prompt's A/B proposal IDs while changing title, digest, payload, and focus; the database retains one canonical Round 1 entry per ID and stores Round 2 as a separate linked follow-up. The 500 records form 160 exact payload groups, with 430 records sharing a payload with at least one other record. This groups repeated graph data without collapsing distinct prompt IDs or mathematical topics. The database's `certificate_type` names the submitted local graph move; `proposed_certificate_type` is an inferred topic label, and `named_mathematical_certificate_in_focus` records a target type only when the focus names one. Neither field asserts that the target certificate exists.

The [ranked table](ranked_proposals.md) begins with the 50 prompts selected for Round 2, chooses the Round 1 A record as the representative of each prompt, and orders them by obligation leverage, a bounded falsification test, and correction cost. This is a research priority order, not an acceptance score. `CLOSED` requires a complete checked certificate for the named target; a local graph zero or source assertion does not meet that standard. `PROMISING` means a relevant, bounded next test is available; `INCREMENTAL` means primarily a local method or supporting identity; `BLOCKED` means the stated route needs correction or an absent premise. These are editorial labels, not mathematical verdicts.

The eight `transcripts_raw/` JSONL files remain source provenance. This pass extracts from the 300 session Markdown files and the Round 1 manifest; it does not reconcile each raw conversation turn with its rendered session.

Source custody check: the 308 files under `round1_sessions/`, `round2_sessions/`, and `steering_team/` had the same aggregate SHA-256 before and after this work: `25324EFCEE13E7D375D846231C1031487F545C457CBC3338313F5E38ACFF0BFF`. The aggregate hashes the UTF-8 newline join of sorted `relative-path file-SHA256` lines. This checks those source folders were not changed during preparation.

## Target G1: orbit and triad program

The [G1 digest](../steering_team/target_g1_problem_digest.md) specifies 50 real coordinates and 55 polynomial equations for a dephased `6×6` complex Hadamard matrix. Its critical question is whether a proposed family catalog covers every relevant matrix and whether transition matrices permit the needed triads. The Round 1 graph receipts do not evaluate those 55 equations. The following table treats the Round 2 sessions as proposed attacks only.

| Candidate vector | Recorded support | Limit and narrowest claim | Next exact test |
|---|---|---|---|
| [Corner reconstruction, T05_03](../round2_sessions/team_05_prompt_03.md) | Names a `3×3` corner as an elimination interface. | The stated vanishing `4×4` minors conflict with `HH†=6I`, which gives rank six. It is a candidate coordinate strategy. | Replace the false minor premise with explicit generators and test exact completions of one corner. |
| [Branch factorization, T05_06](../round2_sessions/team_05_prompt_06.md) | Lists intended known-family branches. | No real-radical or saturation receipt is supplied. This is a target decomposition, not catalog closure. | Publish generators, rational reductions, and a real-solution check for every residual branch. |
| [Mixed transition triads, T05_10](../round2_sessions/team_05_prompt_10.md) | Identifies `H₁†H₂` as the pairwise compatibility object. | The reported bad cross-ratio count lacks a full parameter/gauge certificate. It is a proposed obstruction. | Derive exact transition entries and cover all continuous strata with rational enclosures. |
| [Chart interfaces, T04_07/T04_10](../round2_sessions/team_04_prompt_07.md) | Proposes collar overlap and cocycle checks. | A volume total or local margin does not cover an omitted boundary stratum. These are cover obligations. | Check containment, relative interior overlaps, and each leaf bound in active coordinates. |
| [Triad count, T05_11](../round2_sessions/team_05_prompt_11.md) | Conditional arithmetic `C(5,3)=10`. | The session fixes `B₀=I` but counts seven catalog candidates; among six nonidentity bases, excluding two leaves four. This is a counting target with unmet orbit premises. | Reindex the six bases and discharge all family caps and catalog coverage. |
| [Conditional synthesis, T05_25](../round2_sessions/team_05_prompt_25.md) | Names a Lean dependency chain. | The present theorem accepts classification and bridges as inputs. Its narrowest claim is conditional. | Supply the concrete hypotheses or retain the conditional theorem type in every downstream claim. |

Team 01's Fourier/Diță seeds and Team 02's Tao invariant checks are useful fixed-fixture work; Team 03's cusp charts and Team 04's boundary overlaps target continuous coverage. Team 05 contains the central orbit and counting obligations. [T02_10](../round2_sessions/team_02_prompt_10.md) is recorded under G1 by source team, but its degree-eight synthetic-candidate trace is Q-style candidate evidence, not an orbit-exhaustiveness step. The individual evidence and gap notes appear in the [team summaries](team_summaries/).

## Target Q-Soundness: moment positivity and operator semantics

The [Q digest](../steering_team/target_q_soundness_problem_digest.md) states the core separation: a negative exact trace can reject one candidate moment functional without excluding all physical realizations. The Round 2 files propose algebra, moments, Positivstellensatz, flat extensions, and a fail-closed gate. Their shared graph witness is invalid, so each mathematical claim needs its own independent artifact.

| Candidate vector | Recorded support | Limit and narrowest claim | Next exact test |
|---|---|---|---|
| [Projector word basis, T06_08](../round2_sessions/team_06_prompt_08.md) | Counts 21 reduced words through degree one. | The 25-word full-rank claims in [T07_01](../round2_sessions/team_07_prompt_01.md) and [T09_03](../round2_sessions/team_09_prompt_03.md) conflict with completeness. The narrow claim is a basis-consistency requirement. | Pin the reduction rules and an exact 21-dimensional or singular 25-dimensional matrix, then check relation rows. |
| [Fixed-candidate witnesses, T07_06/08/09](../round2_sessions/team_07_prompt_06.md) | Gives named rational negative-trace targets. | No complete matrix/factor data are in the sessions for independent replay; a candidate result stays candidate-scoped. | Publish full rational moment matrix `M`, dual witness `W=L D Lᵀ`, relation basis, SHA-256, and sign-flip negative controls. |
| [Norm identity, T08_03](../round2_sessions/team_08_prompt_03.md) | Idempotency and completeness yield `ΣΠ²=4·1` in the quotient, hence `25·1−ΣΠ²=21·1`. | This is an algebraic identity, not a realization-to-candidate exhaustion theorem. | Check polynomial identity coefficients in a genuine quadratic-module representation. |
| [Flat extension/GNS, T09_10/T09_21](../round2_sessions/team_09_prompt_10.md) | Identifies a finite-rank extraction route. | The stated rank sequence starts from an inconsistent rank 25; the Lean exclusion interface takes `h_gns_exhaust` as an input. This is a conditional bridge plan. | Correct ranks, build an exact positive flat extension, and show the extracted representation has the required dimension and projector properties. |
| [Fail-closed gate, T10_01/T10_19](../round2_sessions/team_10_prompt_01.md) | Keeps candidate rejection distinct from missing global obligations. | A status flag does not certify the missing operator theorem. It is useful bookkeeping. | Make the gate consume actual checked receipt digests and refuse altered or absent ones. |

## Team map

| Team | Focus and best bounded lead | Main gap |
|---|---|---|
| [01](team_summaries/team_01_summary.md) | Fourier/Diță exact seeds and chart interfaces | Fixed seeds do not cover the full affine torus. |
| [02](team_summaries/team_02_summary.md) | Tao matrix invariant and transition fixtures | Single-orbit checks do not cover all gauges or partners. |
| [03](team_summaries/team_03_summary.md) | Szöllősi/Haagerup algebra and cusp charts | The named family relation and cusp coverage need correction and exact artifacts. |
| [04](team_summaries/team_04_summary.md) | Karlsson boundary overlaps and cocycles | Active-coordinate coverage and every interface remain to be checked. |
| [05](team_summaries/team_05_summary.md) | Corner elimination and triad reduction | Rank-conflicting reconstruction premise and misindexed basis count. |
| [06](team_summaries/team_06_summary.md) | Projector rewriting and canonical word basis | Confluence and semantic quotient still need exact checks. |
| [07](team_summaries/team_07_summary.md) | Fixed-candidate rational dual traces | Complete matrix receipts and consistent word basis are absent. |
| [08](team_summaries/team_08_summary.md) | Algebraic module identity | The all-realization bridge is still a hypothesis. |
| [09](team_summaries/team_09_summary.md) | Flat extension and GNS diagnostics | Rank-25 starting point conflicts with projector completeness. |
| [10](team_summaries/team_10_summary.md) | Fail-closed audit and exact arithmetic tooling | Status and sign-off records are not mathematical certificates. |

## Ten next mathematical vectors, ordered by expected impact and first-test clarity

Each row names a bounded deliverable. Its stated benefit is conditional on the test passing; the linked session supplies the proposed topic, not the completed mathematics.

| Priority | Vector and source | Expected impact; bounded first test | Failure condition |
|---:|---|---|---|
| 1 | [Canonical projector word basis, T06_08](../round2_sessions/team_06_prompt_08.md) | Removes a rank inconsistency affecting several Q claims; enumerate degree-one words modulo completeness and replay the exact relation matrix. | A purported 25-dimensional positive matrix violates one of the four sum-to-identity rows. |
| 2 | [Fixed-candidate witness replay, T07_06](../round2_sessions/team_07_prompt_06.md) | Establishes a trustworthy candidate-scoped Q receipt; publish exact `M=L D Lᵀ` data and recompute the negative trace. | A rational pivot, relation residual, or trace sign fails under replay. |
| 3 | [Quadratic-module semantics, T08_03](../round2_sessions/team_08_prompt_03.md) | Makes the proposed norm identity checkable; encode generators and verify the `21·1` identity coefficient by coefficient. | The purported SOS/module terms do not expand to the claimed polynomial. |
| 4 | [Corner elimination repair, T05_03](../round2_sessions/team_05_prompt_03.md) | Opens a concrete G1 classification route; replace the rank-conflicting minor premise and test one exact corner completion. | Two inequivalent completions share the proposed determining corner. |
| 5 | [Residual branch search, T05_06](../round2_sessions/team_05_prompt_06.md) | Directly addresses G1's missing exotic-branch check; publish one rational Gröbner/saturation fixture with a real-solution audit. | A residual component or point survives the claimed factorization. |
| 6 | [Mixed-orbit transitions, T05_10](../round2_sessions/team_05_prompt_10.md) | Tests a triad compatibility bottleneck; derive exact entry moduli over a complete parameter stratum. | A parameter/gauge case satisfies every proposed violating invariant. |
| 7 | [Karlsson collar interface, T04_07](../round2_sessions/team_04_prompt_07.md) | Closes a specific atlas gap if receipts exist; check one pair of cells for containment, active-coordinate overlap, and bound preservation. | A relative-interior point is uncovered or a bound changes sign. |
| 8 | [Corrected triad indexing, T05_11](../round2_sessions/team_05_prompt_11.md) | Clarifies what classification would need to imply; state the six-nonidentity-basis partition and prove the exact combinatorial consequence. | The required five-family count cannot be derived from the stated caps. |
| 9 | [Flat extension with physical semantics, T09_10](../round2_sessions/team_09_prompt_10.md) | Tests a soundness bridge; construct one rational flat moment extension and verify the extracted representation's dimension and projector equations. | The extracted representation misses rank-one, completeness, or MU relations. |
| 10 | [Cusp blow-up charts, T03_08](../round2_sessions/team_03_prompt_08.md) | Tests a singular G1 interface; verify one exact factorization and its exceptional-divisor chart. | The proposed substitution omits a point of the divisor or fails the polynomial identity. |

## Appendix: full Round 1 proposal inventory

The table below has one row per canonical Round 1 proposal ID. `defect` is the local graph transition; `status` is an editorial research-work label. Each row links to its exact session, and the [JSON database](proposals_all_500.json) contains the full focus, certificate type, move trace, exact rational payload, hashes, Round 2 link where present, and four-part claim boundary.

<!-- INVENTORY_START -->
| Proposal ID | Team | Target | Proposed focus (abbreviated) | Local defect | Status | R2 link |
|---|---|---|---|---|---|---|
| [`PROP_PROMPT_T01_01_A`](../round1_sessions/team_01_prompt_01.md) | `team_01` | G1 | Discrete Fourier matrix $F_6 \cong F_2 \otimes F_3$ character… | `5/6 → 0/1` | PROMISING | [follow-up](../round2_sessions/team_01_prompt_01.md) |
| [`PROP_PROMPT_T01_01_B`](../round1_sessions/team_01_prompt_01.md) | `team_01` | G1 | Dual witness certificate for Discrete Fourier matrix $F_6 \cong… | `0/1 → 0/1` | INCREMENTAL | [follow-up](../round2_sessions/team_01_prompt_01.md) |
| [`PROP_PROMPT_T01_02_A`](../round1_sessions/team_01_prompt_02.md) | `team_01` | G1 | Diță 2-parameter affine phase family $D_6(\alpha, \beta) =… | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_02_B`](../round1_sessions/team_01_prompt_02.md) | `team_01` | G1 | Dual witness certificate for Diță 2-parameter affine phase family… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_03_A`](../round1_sessions/team_01_prompt_03.md) | `team_01` | G1 | 1-parameter slice $D_6(\alpha, 0)$ algebraic reduction to $T^1$. | `7/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_03_B`](../round1_sessions/team_01_prompt_03.md) | `team_01` | G1 | Dual witness certificate for 1-parameter slice $D_6(\alpha, 0)$… | `1/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_04_A`](../round1_sessions/team_01_prompt_04.md) | `team_01` | G1 | 6 locked Diță point seeds in orbits $Y_2 \otimes Q_1$ and $Y_2… | `11/6 → 1/3` | PROMISING | [follow-up](../round2_sessions/team_01_prompt_04.md) |
| [`PROP_PROMPT_T01_04_B`](../round1_sessions/team_01_prompt_04.md) | `team_01` | G1 | Dual witness certificate for 6 locked Diță point seeds in orbits… | `1/3 → 1/3` | INCREMENTAL | [follow-up](../round2_sessions/team_01_prompt_04.md) |
| [`PROP_PROMPT_T01_05_A`](../round1_sessions/team_01_prompt_05.md) | `team_01` | G1 | Phase difference holonomy around Diță 3-cycle faces in the collar… | `19/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_05_B`](../round1_sessions/team_01_prompt_05.md) | `team_01` | G1 | Dual witness certificate for Phase difference holonomy around Diță… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_06_A`](../round1_sessions/team_01_prompt_06.md) | `team_01` | G1 | Exact rational cross-ratio invariants $cr_{ij,kl}(D_6(\alpha… | `2/1 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_06_B`](../round1_sessions/team_01_prompt_06.md) | `team_01` | G1 | Dual witness certificate for Exact rational cross-ratio invariants… | `1/2 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_07_A`](../round1_sessions/team_01_prompt_07.md) | `team_01` | G1 | Desingularization of the boundary collision locus $(\alpha, \beta)… | `25/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_07_B`](../round1_sessions/team_01_prompt_07.md) | `team_01` | G1 | Dual witness certificate for Desingularization of the boundary… | `7/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_08_A`](../round1_sessions/team_01_prompt_08.md) | `team_01` | G1 | ZeroRel curvature lower bound $\Psi^{\text{sq}}(D_6(\alpha), U)… | `19/12 → 1/12` | PROMISING | [follow-up](../round2_sessions/team_01_prompt_08.md) |
| [`PROP_PROMPT_T01_08_B`](../round1_sessions/team_01_prompt_08.md) | `team_01` | G1 | Dual witness certificate for ZeroRel curvature lower bound… | `1/12 → 1/12` | INCREMENTAL | [follow-up](../round2_sessions/team_01_prompt_08.md) |
| [`PROP_PROMPT_T01_09_A`](../round1_sessions/team_01_prompt_09.md) | `team_01` | G1 | Elimination of candidate 4th basis vectors in the Diță affine… | `11/2 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_09_B`](../round1_sessions/team_01_prompt_09.md) | `team_01` | G1 | Dual witness certificate for Elimination of candidate 4th basis… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_10_A`](../round1_sessions/team_01_prompt_10.md) | `team_01` | G1 | Invariance of the Diță cycle defect under diagonal phase gauge… | `7/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_10_B`](../round1_sessions/team_01_prompt_10.md) | `team_01` | G1 | Dual witness certificate for Invariance of the Diță cycle defect… | `1/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_11_A`](../round1_sessions/team_01_prompt_11.md) | `team_01` | G1 | Smale $\alpha$-theory approximate zero exclusion on the Diță… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_11_B`](../round1_sessions/team_01_prompt_11.md) | `team_01` | G1 | Dual witness certificate for Smale $\alpha$-theory approximate… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_12_A`](../round1_sessions/team_01_prompt_12.md) | `team_01` | G1 | Exact cyclotomic representation of $D(\alpha, \beta)$ for rational… | `23/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_12_B`](../round1_sessions/team_01_prompt_12.md) | `team_01` | G1 | Dual witness certificate for Exact cyclotomic representation of… | `5/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_13_A`](../round1_sessions/team_01_prompt_13.md) | `team_01` | G1 | Evaluation of the 108 ZeroRel polynomials on the boundary of the… | `47/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_13_B`](../round1_sessions/team_01_prompt_13.md) | `team_01` | G1 | Dual witness certificate for Evaluation of the 108 ZeroRel… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_14_A`](../round1_sessions/team_01_prompt_14.md) | `team_01` | G1 | Bounded-depth rational bisection on $D_6(\alpha, \beta)$ parameter… | `25/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_14_B`](../round1_sessions/team_01_prompt_14.md) | `team_01` | G1 | Dual witness certificate for Bounded-depth rational bisection on… | `7/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_15_A`](../round1_sessions/team_01_prompt_15.md) | `team_01` | G1 | Cycle circulation $\Phi_1 > 0$ verification across Diță grid… | `19/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_15_B`](../round1_sessions/team_01_prompt_15.md) | `team_01` | G1 | Dual witness certificate for Cycle circulation $\Phi_1 > 0$… | `1/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_16_A`](../round1_sessions/team_01_prompt_16.md) | `team_01` | G1 | Moduli coordinate transition from Diță chart to Karlsson chart. | `5/3 → 1/6` | PROMISING | [follow-up](../round2_sessions/team_01_prompt_16.md) |
| [`PROP_PROMPT_T01_16_B`](../round1_sessions/team_01_prompt_16.md) | `team_01` | G1 | Dual witness certificate for Moduli coordinate transition from… | `1/6 → 1/6` | INCREMENTAL | [follow-up](../round2_sessions/team_01_prompt_16.md) |
| [`PROP_PROMPT_T01_17_A`](../round1_sessions/team_01_prompt_17.md) | `team_01` | G1 | Obstruction of circulant symmetric Hadamard extensions within the… | `61/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_17_B`](../round1_sessions/team_01_prompt_17.md) | `team_01` | G1 | Dual witness certificate for Obstruction of circulant symmetric… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_18_A`](../round1_sessions/team_01_prompt_18.md) | `team_01` | G1 | Non-extendibility of $(I_6, F_6, D_6(\alpha))$ to a 4-MUB set for… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_18_B`](../round1_sessions/team_01_prompt_18.md) | `team_01` | G1 | Dual witness certificate for Non-extendibility of $(I_6, F_6… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_19_A`](../round1_sessions/team_01_prompt_19.md) | `team_01` | G1 | Nullstellensatz certificate for emptiness of… | `23/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_19_B`](../round1_sessions/team_01_prompt_19.md) | `team_01` | G1 | Dual witness certificate for Nullstellensatz certificate for… | `5/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_20_A`](../round1_sessions/team_01_prompt_20.md) | `team_01` | G1 | Topological triviality of the tangent bundle over the interior of… | `2/1 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_20_B`](../round1_sessions/team_01_prompt_20.md) | `team_01` | G1 | Dual witness certificate for Topological triviality of the tangent… | `1/2 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_21_A`](../round1_sessions/team_01_prompt_21.md) | `team_01` | G1 | Exact rational interval bounds on Diță gradient variations. | `25/2 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_21_B`](../round1_sessions/team_01_prompt_21.md) | `team_01` | G1 | Dual witness certificate for Exact rational interval bounds on… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_22_A`](../round1_sessions/team_01_prompt_22.md) | `team_01` | G1 | Uniform derivative bounds $L_{\text{Dita}} \le 85/9$ across the 2D… | `19/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_22_B`](../round1_sessions/team_01_prompt_22.md) | `team_01` | G1 | Dual witness certificate for Uniform derivative bounds… | `1/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_23_A`](../round1_sessions/team_01_prompt_23.md) | `team_01` | G1 | Rejection of floating-point perturbation in Diță phase matrices. | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_23_B`](../round1_sessions/team_01_prompt_23.md) | `team_01` | G1 | Dual witness certificate for Rejection of floating-point… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_24_A`](../round1_sessions/team_01_prompt_24.md) | `team_01` | G1 | Verification of $F_6^\dagger D_6(\alpha, \beta) \in \mathcal{H}_6$… | `7/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_24_B`](../round1_sessions/team_01_prompt_24.md) | `team_01` | G1 | Dual witness certificate for Verification of $F_6^\dagger… | `1/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T01_25_A`](../round1_sessions/team_01_prompt_25.md) | `team_01` | G1 | Master synthesis of the Diță/Fourier component obstruction… | `89/6 → 0/1` | PROMISING | [follow-up](../round2_sessions/team_01_prompt_25.md) |
| [`PROP_PROMPT_T01_25_B`](../round1_sessions/team_01_prompt_25.md) | `team_01` | G1 | Dual witness certificate for Master synthesis of the Diță/Fourier… | `0/1 → 0/1` | INCREMENTAL | [follow-up](../round2_sessions/team_01_prompt_25.md) |
| [`PROP_PROMPT_T02_01_A`](../round1_sessions/team_02_prompt_01.md) | `team_02` | G1 | Construction of Tao matrix $S_6$ over $\mathbb{Q}(\zeta_3)$ from… | `5/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_01_B`](../round1_sessions/team_02_prompt_01.md) | `team_02` | G1 | Dual witness certificate for Construction of Tao matrix $S_6$ over… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_02_A`](../round1_sessions/team_02_prompt_02.md) | `team_02` | G1 | Exact rational proposed task to establish whether defect $d(S_6) =… | `5/3 → 1/6` | PROMISING | [follow-up](../round2_sessions/team_02_prompt_02.md) |
| [`PROP_PROMPT_T02_02_B`](../round1_sessions/team_02_prompt_02.md) | `team_02` | G1 | Dual witness certificate for Exact rational proposed task to… | `1/6 → 1/6` | INCREMENTAL | [follow-up](../round2_sessions/team_02_prompt_02.md) |
| [`PROP_PROMPT_T02_03_A`](../round1_sessions/team_02_prompt_03.md) | `team_02` | G1 | Topological isolation of $S_6$: proposed task to establish whether… | `7/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_03_B`](../round1_sessions/team_02_prompt_03.md) | `team_02` | G1 | Dual witness certificate for Topological isolation of $S_6$… | `1/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_04_A`](../round1_sessions/team_02_prompt_04.md) | `team_02` | G1 | Evaluation of all 225 cross-ratios of $S_6$ showing $e_m \in \{0… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_04_B`](../round1_sessions/team_02_prompt_04.md) | `team_02` | G1 | Dual witness certificate for Evaluation of all 225 cross-ratios of… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_05_A`](../round1_sessions/team_02_prompt_05.md) | `team_02` | G1 | proposed task to establish whether no cross-ratio of $S_6$ equals… | `19/6 → 0/1` | PROMISING | [follow-up](../round2_sessions/team_02_prompt_05.md) |
| [`PROP_PROMPT_T02_05_B`](../round1_sessions/team_02_prompt_05.md) | `team_02` | G1 | Dual witness certificate for proposed task to establish whether no… | `0/1 → 0/1` | INCREMENTAL | [follow-up](../round2_sessions/team_02_prompt_05.md) |
| [`PROP_PROMPT_T02_06_A`](../round1_sessions/team_02_prompt_06.md) | `team_02` | G1 | Evaluation of transition matrix $H_{12} = S_6^\dagger (D_1 P_1 S_6… | `2/1 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_06_B`](../round1_sessions/team_02_prompt_06.md) | `team_02` | G1 | Dual witness certificate for Evaluation of transition matrix… | `1/2 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_07_A`](../round1_sessions/team_02_prompt_07.md) | `team_02` | G1 | proposed task to establish whether $H_{12} \notin \mathcal{H}_6$… | `25/12 → 7/12` | PROMISING | [follow-up](../round2_sessions/team_02_prompt_07.md) |
| [`PROP_PROMPT_T02_07_B`](../round1_sessions/team_02_prompt_07.md) | `team_02` | G1 | Dual witness certificate for proposed task to establish whether… | `7/12 → 7/12` | INCREMENTAL | [follow-up](../round2_sessions/team_02_prompt_07.md) |
| [`PROP_PROMPT_T02_08_A`](../round1_sessions/team_02_prompt_08.md) | `team_02` | G1 | ZeroRel curvature evaluation $\Psi^{\text{sq}}(S_6, U) \ge… | `19/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_08_B`](../round1_sessions/team_02_prompt_08.md) | `team_02` | G1 | Dual witness certificate for ZeroRel curvature evaluation… | `1/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_09_A`](../round1_sessions/team_02_prompt_09.md) | `team_02` | G1 | Exact rational sum-of-squares certificate for… | `11/2 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_09_B`](../round1_sessions/team_02_prompt_09.md) | `team_02` | G1 | Dual witness certificate for Exact rational sum-of-squares… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_10_A`](../round1_sessions/team_02_prompt_10.md) | `team_02` | G1 | Non-commutative moment SDP refutation of synthetic $S_6$… | `7/4 → 1/4` | PROMISING | [follow-up](../round2_sessions/team_02_prompt_10.md) |
| [`PROP_PROMPT_T02_10_B`](../round1_sessions/team_02_prompt_10.md) | `team_02` | G1 | Dual witness certificate for Non-commutative moment SDP refutation… | `1/4 → 1/4` | INCREMENTAL | [follow-up](../round2_sessions/team_02_prompt_10.md) |
| [`PROP_PROMPT_T02_11_A`](../round1_sessions/team_02_prompt_11.md) | `team_02` | G1 | Invariant polynomial spectrum distinguishing $\mathcal{O}(S_6)$… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_11_B`](../round1_sessions/team_02_prompt_11.md) | `team_02` | G1 | Dual witness certificate for Invariant polynomial spectrum… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_12_A`](../round1_sessions/team_02_prompt_12.md) | `team_02` | G1 | Smale $\alpha$-theory certification bounding distance to nearest… | `23/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_12_B`](../round1_sessions/team_02_prompt_12.md) | `team_02` | G1 | Dual witness certificate for Smale $\alpha$-theory certification… | `5/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_13_A`](../round1_sessions/team_02_prompt_13.md) | `team_02` | G1 | proposed task to establish whether $(I_6, S_6)$ cannot extend to… | `47/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_13_B`](../round1_sessions/team_02_prompt_13.md) | `team_02` | G1 | Dual witness certificate for proposed task to establish whether… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_14_A`](../round1_sessions/team_02_prompt_14.md) | `team_02` | G1 | Evaluation of cross-orbit pairing $(I_6, S_6, D_6(\alpha))$… | `25/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_14_B`](../round1_sessions/team_02_prompt_14.md) | `team_02` | G1 | Dual witness certificate for Evaluation of cross-orbit pairing… | `7/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_15_A`](../round1_sessions/team_02_prompt_15.md) | `team_02` | G1 | Exact rational $LDL^T$ certificate of curvature matrix at $S_6$… | `19/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_15_B`](../round1_sessions/team_02_prompt_15.md) | `team_02` | G1 | Dual witness certificate for Exact rational $LDL^T$ certificate of… | `1/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_16_A`](../round1_sessions/team_02_prompt_16.md) | `team_02` | G1 | Simplicial 1-cocycle circulation $\Phi_1(S_6) \ge 12133/5000 > 0$… | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_16_B`](../round1_sessions/team_02_prompt_16.md) | `team_02` | G1 | Dual witness certificate for Simplicial 1-cocycle circulation… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_17_A`](../round1_sessions/team_02_prompt_17.md) | `team_02` | G1 | Rejection of near-Tao perturbation candidates under 100% exact… | `61/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_17_B`](../round1_sessions/team_02_prompt_17.md) | `team_02` | G1 | Dual witness certificate for Rejection of near-Tao perturbation… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_18_A`](../round1_sessions/team_02_prompt_18.md) | `team_02` | G1 | Gröbner basis decomposition of $S_6$ local dephased ideal in 50… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_18_B`](../round1_sessions/team_02_prompt_18.md) | `team_02` | G1 | Dual witness certificate for Gröbner basis decomposition of $S_6$… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_19_A`](../round1_sessions/team_02_prompt_19.md) | `team_02` | G1 | Flat extension obstruction: proposed task to establish whether… | `23/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_19_B`](../round1_sessions/team_02_prompt_19.md) | `team_02` | G1 | Dual witness certificate for Flat extension obstruction: proposed… | `5/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_20_A`](../round1_sessions/team_02_prompt_20.md) | `team_02` | G1 | Projective blow-up of the singular intersection between $S_6$ and… | `2/1 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_20_B`](../round1_sessions/team_02_prompt_20.md) | `team_02` | G1 | Dual witness certificate for Projective blow-up of the singular… | `1/2 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_21_A`](../round1_sessions/team_02_prompt_21.md) | `team_02` | G1 | proposed task to establish whether $\mathcal{O}(S_6)$ supports at… | `25/2 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_21_B`](../round1_sessions/team_02_prompt_21.md) | `team_02` | G1 | Dual witness certificate for proposed task to establish whether… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_22_A`](../round1_sessions/team_02_prompt_22.md) | `team_02` | G1 | Network Simplex dual witness on the Tao isolated neighborhood graph. | `19/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_22_B`](../round1_sessions/team_02_prompt_22.md) | `team_02` | G1 | Dual witness certificate for Network Simplex dual witness on the… | `1/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_23_A`](../round1_sessions/team_02_prompt_23.md) | `team_02` | G1 | Elimination of real Hadamard sub-configurations within… | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_23_B`](../round1_sessions/team_02_prompt_23.md) | `team_02` | G1 | Dual witness certificate for Elimination of real Hadamard… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_24_A`](../round1_sessions/team_02_prompt_24.md) | `team_02` | G1 | Lean 4 formalization of $S_6$ algebraic matrix and dephased form. | `7/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_24_B`](../round1_sessions/team_02_prompt_24.md) | `team_02` | G1 | Dual witness certificate for Lean 4 formalization of $S_6$… | `1/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T02_25_A`](../round1_sessions/team_02_prompt_25.md) | `team_02` | G1 | Master synthesis of the Tao isolated orbit non-extendibility… | `89/6 → 0/1` | PROMISING | [follow-up](../round2_sessions/team_02_prompt_25.md) |
| [`PROP_PROMPT_T02_25_B`](../round1_sessions/team_02_prompt_25.md) | `team_02` | G1 | Dual witness certificate for Master synthesis of the Tao isolated… | `0/1 → 0/1` | INCREMENTAL | [follow-up](../round2_sessions/team_02_prompt_25.md) |
| [`PROP_PROMPT_T03_01_A`](../round1_sessions/team_03_prompt_01.md) | `team_03` | G1 | Parameterization of Szöllősi 1-parameter family $B_6(\theta)$ for… | `5/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_01_B`](../round1_sessions/team_03_prompt_01.md) | `team_03` | G1 | Dual witness certificate for Parameterization of Szöllősi… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_02_A`](../round1_sessions/team_03_prompt_02.md) | `team_03` | G1 | Algebraic phase equations for $B_6(\theta)$ derived from… | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_02_B`](../round1_sessions/team_03_prompt_02.md) | `team_03` | G1 | Dual witness certificate for Algebraic phase equations for… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_03_A`](../round1_sessions/team_03_prompt_03.md) | `team_03` | G1 | Exact algebraic identification of Haagerup matrix $H_6$ at… | `7/4 → 1/4` | BLOCKED | [follow-up](../round2_sessions/team_03_prompt_03.md) |
| [`PROP_PROMPT_T03_03_B`](../round1_sessions/team_03_prompt_03.md) | `team_03` | G1 | Dual witness certificate for Exact algebraic identification of… | `1/4 → 1/4` | INCREMENTAL | [follow-up](../round2_sessions/team_03_prompt_03.md) |
| [`PROP_PROMPT_T03_04_A`](../round1_sessions/team_03_prompt_04.md) | `team_03` | G1 | Generic defect calculation $d(B_6(\theta)) = 1$ for $\theta \in… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_04_B`](../round1_sessions/team_03_prompt_04.md) | `team_03` | G1 | Dual witness certificate for Generic defect calculation… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_05_A`](../round1_sessions/team_03_prompt_05.md) | `team_03` | G1 | Evaluation of transition matrix $H_{12} = B_6(\theta_1)^\dagger… | `19/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_05_B`](../round1_sessions/team_03_prompt_05.md) | `team_03` | G1 | Dual witness certificate for Evaluation of transition matrix… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_06_A`](../round1_sessions/team_03_prompt_06.md) | `team_03` | G1 | proposed task to establish whether no two distinct Szöllősi… | `2/1 → 1/2` | PROMISING | [follow-up](../round2_sessions/team_03_prompt_06.md) |
| [`PROP_PROMPT_T03_06_B`](../round1_sessions/team_03_prompt_06.md) | `team_03` | G1 | Dual witness certificate for proposed task to establish whether no… | `1/2 → 1/2` | INCREMENTAL | [follow-up](../round2_sessions/team_03_prompt_06.md) |
| [`PROP_PROMPT_T03_07_A`](../round1_sessions/team_03_prompt_07.md) | `team_03` | G1 | Desingularization of the deltoid cusp singularities at $\theta \in… | `25/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_07_B`](../round1_sessions/team_03_prompt_07.md) | `team_03` | G1 | Dual witness certificate for Desingularization of the deltoid cusp… | `7/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_08_A`](../round1_sessions/team_03_prompt_08.md) | `team_03` | G1 | Projective blow-up coordinates $(u, v)$ along the Segre variety… | `19/12 → 1/12` | PROMISING | [follow-up](../round2_sessions/team_03_prompt_08.md) |
| [`PROP_PROMPT_T03_08_B`](../round1_sessions/team_03_prompt_08.md) | `team_03` | G1 | Dual witness certificate for Projective blow-up coordinates $(u… | `1/12 → 1/12` | INCREMENTAL | [follow-up](../round2_sessions/team_03_prompt_08.md) |
| [`PROP_PROMPT_T03_09_A`](../round1_sessions/team_03_prompt_09.md) | `team_03` | G1 | Factored corner determinant on blow-up chart: $P_{\text{corner}} =… | `11/2 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_09_B`](../round1_sessions/team_03_prompt_09.md) | `team_03` | G1 | Dual witness certificate for Factored corner determinant on… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_10_A`](../round1_sessions/team_03_prompt_10.md) | `team_03` | G1 | Desingularized Lipschitz gap propagation: $f(u, v) \ge… | `7/4 → 1/4` | PROMISING | [follow-up](../round2_sessions/team_03_prompt_10.md) |
| [`PROP_PROMPT_T03_10_B`](../round1_sessions/team_03_prompt_10.md) | `team_03` | G1 | Dual witness certificate for Desingularized Lipschitz gap… | `1/4 → 1/4` | INCREMENTAL | [follow-up](../round2_sessions/team_03_prompt_10.md) |
| [`PROP_PROMPT_T03_11_A`](../round1_sessions/team_03_prompt_11.md) | `team_03` | G1 | Exact rational interval enclosure of Haagerup point $H_6$ over… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_11_B`](../round1_sessions/team_03_prompt_11.md) | `team_03` | G1 | Dual witness certificate for Exact rational interval enclosure of… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_12_A`](../round1_sessions/team_03_prompt_12.md) | `team_03` | G1 | ZeroRel curvature lower bound across the Haagerup rational ball… | `23/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_12_B`](../round1_sessions/team_03_prompt_12.md) | `team_03` | G1 | Dual witness certificate for ZeroRel curvature lower bound across… | `5/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_13_A`](../round1_sessions/team_03_prompt_13.md) | `team_03` | G1 | Cross-ratio invariant spectrum of $H_6$ verifying orbit isolation… | `47/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_13_B`](../round1_sessions/team_03_prompt_13.md) | `team_03` | G1 | Dual witness certificate for Cross-ratio invariant spectrum of… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_14_A`](../round1_sessions/team_03_prompt_14.md) | `team_03` | G1 | Bounded-depth rational bisection on Szöllősi arc parameter cells. | `25/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_14_B`](../round1_sessions/team_03_prompt_14.md) | `team_03` | G1 | Dual witness certificate for Bounded-depth rational bisection on… | `7/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_15_A`](../round1_sessions/team_03_prompt_15.md) | `team_03` | G1 | Cycle circulation $\Phi_1 > 0$ across the composite Szöllősi… | `19/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_15_B`](../round1_sessions/team_03_prompt_15.md) | `team_03` | G1 | Dual witness certificate for Cycle circulation $\Phi_1 > 0$ across… | `1/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_16_A`](../round1_sessions/team_03_prompt_16.md) | `team_03` | G1 | Connecting the Szöllősi family boundary to the Karlsson… | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_16_B`](../round1_sessions/team_03_prompt_16.md) | `team_03` | G1 | Dual witness certificate for Connecting the Szöllősi family… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_17_A`](../round1_sessions/team_03_prompt_17.md) | `team_03` | G1 | Evaluating pairing between $B_6(\theta)$ and Diță family… | `61/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_17_B`](../round1_sessions/team_03_prompt_17.md) | `team_03` | G1 | Dual witness certificate for Evaluating pairing between… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_18_A`](../round1_sessions/team_03_prompt_18.md) | `team_03` | G1 | Nullstellensatz certificate for emptiness of… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_18_B`](../round1_sessions/team_03_prompt_18.md) | `team_03` | G1 | Dual witness certificate for Nullstellensatz certificate for… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_19_A`](../round1_sessions/team_03_prompt_19.md) | `team_03` | G1 | Network Simplex dual witness certification on blown-up cusp cells. | `23/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_19_B`](../round1_sessions/team_03_prompt_19.md) | `team_03` | G1 | Dual witness certificate for Network Simplex dual witness… | `5/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_20_A`](../round1_sessions/team_03_prompt_20.md) | `team_03` | G1 | Non-existence of 4-MUB sets containing a Szöllősi matrix and a Tao… | `2/1 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_20_B`](../round1_sessions/team_03_prompt_20.md) | `team_03` | G1 | Dual witness certificate for Non-existence of 4-MUB sets… | `1/2 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_21_A`](../round1_sessions/team_03_prompt_21.md) | `team_03` | G1 | Exact rational representation of algebraic roots of $B_6(\theta)$… | `25/2 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_21_B`](../round1_sessions/team_03_prompt_21.md) | `team_03` | G1 | Dual witness certificate for Exact rational representation of… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_22_A`](../round1_sessions/team_03_prompt_22.md) | `team_03` | G1 | Uniform derivative bounds on the Szöllősi arc away from cusps. | `19/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_22_B`](../round1_sessions/team_03_prompt_22.md) | `team_03` | G1 | Dual witness certificate for Uniform derivative bounds on the… | `1/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_23_A`](../round1_sessions/team_03_prompt_23.md) | `team_03` | G1 | Rejection of non-unitary / non-unimodular perturbations along… | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_23_B`](../round1_sessions/team_03_prompt_23.md) | `team_03` | G1 | Dual witness certificate for Rejection of non-unitary /… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_24_A`](../round1_sessions/team_03_prompt_24.md) | `team_03` | G1 | Lean 4 verification of Szöllősi deltoid cusp desingularization. | `7/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_24_B`](../round1_sessions/team_03_prompt_24.md) | `team_03` | G1 | Dual witness certificate for Lean 4 verification of Szöllősi… | `1/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T03_25_A`](../round1_sessions/team_03_prompt_25.md) | `team_03` | G1 | Master synthesis of the Szöllősi / Haagerup orbit… | `89/6 → 0/1` | PROMISING | [follow-up](../round2_sessions/team_03_prompt_25.md) |
| [`PROP_PROMPT_T03_25_B`](../round1_sessions/team_03_prompt_25.md) | `team_03` | G1 | Dual witness certificate for Master synthesis of the Szöllősi /… | `0/1 → 0/1` | INCREMENTAL | [follow-up](../round2_sessions/team_03_prompt_25.md) |
| [`PROP_PROMPT_T04_01_A`](../round1_sessions/team_04_prompt_01.md) | `team_04` | G1 | Parameterization of Karlsson 3-parameter continuous family… | `5/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_01_B`](../round1_sessions/team_04_prompt_01.md) | `team_04` | G1 | Dual witness certificate for Parameterization of Karlsson… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_02_A`](../round1_sessions/team_04_prompt_02.md) | `team_04` | G1 | Degeneracy locus where $K_6^{(3)}$ specializes to the Diță affine… | `5/3 → 1/6` | PROMISING | [follow-up](../round2_sessions/team_04_prompt_02.md) |
| [`PROP_PROMPT_T04_02_B`](../round1_sessions/team_04_prompt_02.md) | `team_04` | G1 | Dual witness certificate for Degeneracy locus where $K_6^{(3)}$… | `1/6 → 1/6` | INCREMENTAL | [follow-up](../round2_sessions/team_04_prompt_02.md) |
| [`PROP_PROMPT_T04_03_A`](../round1_sessions/team_04_prompt_03.md) | `team_04` | G1 | Boundary stratum where $K_6^{(3)}$ connects to the Szöllősi family… | `7/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_03_B`](../round1_sessions/team_04_prompt_03.md) | `team_04` | G1 | Dual witness certificate for Boundary stratum where $K_6^{(3)}$… | `1/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_04_A`](../round1_sessions/team_04_prompt_04.md) | `team_04` | G1 | Generic defect analysis $d(K_6^{(3)}) = 3$, jumping to 4 on Diță… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_04_B`](../round1_sessions/team_04_prompt_04.md) | `team_04` | G1 | Dual witness certificate for Generic defect analysis $d(K_6^{(3)})… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_05_A`](../round1_sessions/team_04_prompt_05.md) | `team_04` | G1 | Evaluation of transition matrix $H_1^\dagger H_2$ for internal… | `19/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_05_B`](../round1_sessions/team_04_prompt_05.md) | `team_04` | G1 | Dual witness certificate for Evaluation of transition matrix… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_06_A`](../round1_sessions/team_04_prompt_06.md) | `team_04` | G1 | proposed task to establish whether internal MU pairs in… | `2/1 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_06_B`](../round1_sessions/team_04_prompt_06.md) | `team_04` | G1 | Dual witness certificate for proposed task to establish whether… | `1/2 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_07_A`](../round1_sessions/team_04_prompt_07.md) | `team_04` | G1 | Exterior boundary interface between Karlsson volume and the 2D… | `25/12 → 7/12` | PROMISING | [follow-up](../round2_sessions/team_04_prompt_07.md) |
| [`PROP_PROMPT_T04_07_B`](../round1_sessions/team_04_prompt_07.md) | `team_04` | G1 | Dual witness certificate for Exterior boundary interface between… | `7/12 → 7/12` | INCREMENTAL | [follow-up](../round2_sessions/team_04_prompt_07.md) |
| [`PROP_PROMPT_T04_08_A`](../round1_sessions/team_04_prompt_08.md) | `team_04` | G1 | Exact rational boundary overlap evaluator between collar partition… | `19/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_08_B`](../round1_sessions/team_04_prompt_08.md) | `team_04` | G1 | Dual witness certificate for Exact rational boundary overlap… | `1/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_09_A`](../round1_sessions/team_04_prompt_09.md) | `team_04` | G1 | Positive curvature margin $\varepsilon_{\text{interface}} > 0$ on… | `11/2 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_09_B`](../round1_sessions/team_04_prompt_09.md) | `team_04` | G1 | Dual witness certificate for Positive curvature margin… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_10_A`](../round1_sessions/team_04_prompt_10.md) | `team_04` | G1 | Multi-chart transition cocycle chaining across the Karlsson… | `7/4 → 1/4` | PROMISING | [follow-up](../round2_sessions/team_04_prompt_10.md) |
| [`PROP_PROMPT_T04_10_B`](../round1_sessions/team_04_prompt_10.md) | `team_04` | G1 | Dual witness certificate for Multi-chart transition cocycle… | `1/4 → 1/4` | INCREMENTAL | [follow-up](../round2_sessions/team_04_prompt_10.md) |
| [`PROP_PROMPT_T04_11_A`](../round1_sessions/team_04_prompt_11.md) | `team_04` | G1 | Volume conservation certification: $\sum \text{vol}(C_i) =… | `11/6 → 1/3` | PROMISING | [follow-up](../round2_sessions/team_04_prompt_11.md) |
| [`PROP_PROMPT_T04_11_B`](../round1_sessions/team_04_prompt_11.md) | `team_04` | G1 | Dual witness certificate for Volume conservation certification… | `1/3 → 1/3` | INCREMENTAL | [follow-up](../round2_sessions/team_04_prompt_11.md) |
| [`PROP_PROMPT_T04_12_A`](../round1_sessions/team_04_prompt_12.md) | `team_04` | G1 | Network Simplex acceleration confirming $\Phi_1 > 0$ across all… | `23/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_12_B`](../round1_sessions/team_04_prompt_12.md) | `team_04` | G1 | Dual witness certificate for Network Simplex acceleration… | `5/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_13_A`](../round1_sessions/team_04_prompt_13.md) | `team_04` | G1 | Elimination of candidate 4th bases across the Karlsson volume via… | `47/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_13_B`](../round1_sessions/team_04_prompt_13.md) | `team_04` | G1 | Dual witness certificate for Elimination of candidate 4th bases… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_14_A`](../round1_sessions/team_04_prompt_14.md) | `team_04` | G1 | Algebraic characterization of the Karlsson non-affine phase… | `25/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_14_B`](../round1_sessions/team_04_prompt_14.md) | `team_04` | G1 | Dual witness certificate for Algebraic characterization of the… | `7/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_15_A`](../round1_sessions/team_04_prompt_15.md) | `team_04` | G1 | Bounded-depth rational bisection on 3D Karlsson interval boxes. | `19/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_15_B`](../round1_sessions/team_04_prompt_15.md) | `team_04` | G1 | Dual witness certificate for Bounded-depth rational bisection on… | `1/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_16_A`](../round1_sessions/team_04_prompt_16.md) | `team_04` | G1 | Rejection of gapped boundary interfaces between Karlsson and Diță… | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_16_B`](../round1_sessions/team_04_prompt_16.md) | `team_04` | G1 | Dual witness certificate for Rejection of gapped boundary… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_17_A`](../round1_sessions/team_04_prompt_17.md) | `team_04` | G1 | Exact cyclotomic evaluations on rational Karlsson grid points. | `61/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_17_B`](../round1_sessions/team_04_prompt_17.md) | `team_04` | G1 | Dual witness certificate for Exact cyclotomic evaluations on… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_18_A`](../round1_sessions/team_04_prompt_18.md) | `team_04` | G1 | Smale $\alpha$-theory sentry verifying absence of roots on the… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_18_B`](../round1_sessions/team_04_prompt_18.md) | `team_04` | G1 | Dual witness certificate for Smale $\alpha$-theory sentry… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_19_A`](../round1_sessions/team_04_prompt_19.md) | `team_04` | G1 | Nullstellensatz certificate for emptiness of… | `23/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_19_B`](../round1_sessions/team_04_prompt_19.md) | `team_04` | G1 | Dual witness certificate for Nullstellensatz certificate for… | `5/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_20_A`](../round1_sessions/team_04_prompt_20.md) | `team_04` | G1 | proposed task to establish whether no putative MUB quadruple… | `2/1 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_20_B`](../round1_sessions/team_04_prompt_20.md) | `team_04` | G1 | Dual witness certificate for proposed task to establish whether no… | `1/2 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_21_A`](../round1_sessions/team_04_prompt_21.md) | `team_04` | G1 | Invariant cross-ratio mapping across the 3 parameters of… | `25/2 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_21_B`](../round1_sessions/team_04_prompt_21.md) | `team_04` | G1 | Dual witness certificate for Invariant cross-ratio mapping across… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_22_A`](../round1_sessions/team_04_prompt_22.md) | `team_04` | G1 | Uniform gradient bounds on the Karlsson interior. | `19/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_22_B`](../round1_sessions/team_04_prompt_22.md) | `team_04` | G1 | Dual witness certificate for Uniform gradient bounds on the… | `1/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_23_A`](../round1_sessions/team_04_prompt_23.md) | `team_04` | G1 | AST zero-float linting on Karlsson exact rational evaluator. | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_23_B`](../round1_sessions/team_04_prompt_23.md) | `team_04` | G1 | Dual witness certificate for AST zero-float linting on Karlsson… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_24_A`](../round1_sessions/team_04_prompt_24.md) | `team_04` | G1 | Lean 4 formalization of the Karlsson volume boundary interface. | `7/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_24_B`](../round1_sessions/team_04_prompt_24.md) | `team_04` | G1 | Dual witness certificate for Lean 4 formalization of the Karlsson… | `1/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T04_25_A`](../round1_sessions/team_04_prompt_25.md) | `team_04` | G1 | Master synthesis of the Karlsson manifold coverage and boundary… | `89/6 → 0/1` | PROMISING | [follow-up](../round2_sessions/team_04_prompt_25.md) |
| [`PROP_PROMPT_T04_25_B`](../round1_sessions/team_04_prompt_25.md) | `team_04` | G1 | Dual witness certificate for Master synthesis of the Karlsson… | `0/1 → 0/1` | INCREMENTAL | [follow-up](../round2_sessions/team_04_prompt_25.md) |
| [`PROP_PROMPT_T05_01_A`](../round1_sessions/team_05_prompt_01.md) | `team_05` | G1 | Formulation of the 55 polynomial equations in 50 real variables… | `5/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_01_B`](../round1_sessions/team_05_prompt_01.md) | `team_05` | G1 | Dual witness certificate for Formulation of the 55 polynomial… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_02_A`](../round1_sessions/team_05_prompt_02.md) | `team_05` | G1 | Elimination ideal of the $3 \times 3$ corner submatrix: 9 complex… | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_02_B`](../round1_sessions/team_05_prompt_02.md) | `team_05` | G1 | Dual witness certificate for Elimination ideal of the $3 \times 3$… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_03_A`](../round1_sessions/team_05_prompt_03.md) | `team_05` | G1 | Finite-incidence algebraic corner reconstruction theorem (Cárdenes… | `7/4 → 1/4` | BLOCKED | [follow-up](../round2_sessions/team_05_prompt_03.md) |
| [`PROP_PROMPT_T05_03_B`](../round1_sessions/team_05_prompt_03.md) | `team_05` | G1 | Dual witness certificate for Finite-incidence algebraic corner… | `1/4 → 1/4` | INCREMENTAL | [follow-up](../round2_sessions/team_05_prompt_03.md) |
| [`PROP_PROMPT_T05_04_A`](../round1_sessions/team_05_prompt_04.md) | `team_05` | G1 | proposed task to establish whether every dephased $6 \times 6$ CHM… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_04_B`](../round1_sessions/team_05_prompt_04.md) | `team_05` | G1 | Dual witness certificate for proposed task to establish whether… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_05_A`](../round1_sessions/team_05_prompt_05.md) | `team_05` | G1 | Irreducible component decomposition of the corner variety… | `19/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_05_B`](../round1_sessions/team_05_prompt_05.md) | `team_05` | G1 | Dual witness certificate for Irreducible component decomposition… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_06_A`](../round1_sessions/team_05_prompt_06.md) | `team_05` | G1 | proposed task to establish whether all viable corner determinants… | `2/1 → 1/2` | PROMISING | [follow-up](../round2_sessions/team_05_prompt_06.md) |
| [`PROP_PROMPT_T05_06_B`](../round1_sessions/team_05_prompt_06.md) | `team_05` | G1 | Dual witness certificate for proposed task to establish whether… | `1/2 → 1/2` | INCREMENTAL | [follow-up](../round2_sessions/team_05_prompt_06.md) |
| [`PROP_PROMPT_T05_07_A`](../round1_sessions/team_05_prompt_07.md) | `team_05` | G1 | Absence of exotic isolated points: proposed task to establish… | `25/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_07_B`](../round1_sessions/team_05_prompt_07.md) | `team_05` | G1 | Dual witness certificate for Absence of exotic isolated points… | `7/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_08_A`](../round1_sessions/team_05_prompt_08.md) | `team_05` | G1 | Formulation of the Triad Compatibility Variety $V_{\text{triple}}… | `19/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_08_B`](../round1_sessions/team_05_prompt_08.md) | `team_05` | G1 | Dual witness certificate for Formulation of the Triad… | `1/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_09_A`](../round1_sessions/team_05_prompt_09.md) | `team_05` | G1 | proposed task to establish whether $H_1^\dagger H_2 \in… | `11/2 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_09_B`](../round1_sessions/team_05_prompt_09.md) | `team_05` | G1 | Dual witness certificate for proposed task to establish whether… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_10_A`](../round1_sessions/team_05_prompt_10.md) | `team_05` | G1 | Cross-orbit triad obstruction: proposed task to establish whether… | `7/4 → 1/4` | PROMISING | [follow-up](../round2_sessions/team_05_prompt_10.md) |
| [`PROP_PROMPT_T05_10_B`](../round1_sessions/team_05_prompt_10.md) | `team_05` | G1 | Dual witness certificate for Cross-orbit triad obstruction… | `1/4 → 1/4` | INCREMENTAL | [follow-up](../round2_sessions/team_05_prompt_10.md) |
| [`PROP_PROMPT_T05_11_A`](../round1_sessions/team_05_prompt_11.md) | `team_05` | G1 | Combinatorial Pigeonhole Lemma: Any complete 7-MUB configuration… | `11/6 → 1/3` | BLOCKED | [follow-up](../round2_sessions/team_05_prompt_11.md) |
| [`PROP_PROMPT_T05_11_B`](../round1_sessions/team_05_prompt_11.md) | `team_05` | G1 | Dual witness certificate for Combinatorial Pigeonhole Lemma: Any… | `1/3 → 1/3` | INCREMENTAL | [follow-up](../round2_sessions/team_05_prompt_11.md) |
| [`PROP_PROMPT_T05_12_A`](../round1_sessions/team_05_prompt_12.md) | `team_05` | G1 | proposed task to establish whether $\ge 5$ Diță/Fourier bases… | `23/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_12_B`](../round1_sessions/team_05_prompt_12.md) | `team_05` | G1 | Dual witness certificate for proposed task to establish whether… | `5/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_13_A`](../round1_sessions/team_05_prompt_13.md) | `team_05` | G1 | Connecting the Pigeonhole Lemma to the certified Diță moduli atlas. | `47/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_13_B`](../round1_sessions/team_05_prompt_13.md) | `team_05` | G1 | Dual witness certificate for Connecting the Pigeonhole Lemma to… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_14_A`](../round1_sessions/team_05_prompt_14.md) | `team_05` | G1 | Formal discharge of Premise $G_1$ without continuum cover of the… | `25/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_14_B`](../round1_sessions/team_05_prompt_14.md) | `team_05` | G1 | Dual witness certificate for Formal discharge of Premise $G_1$… | `7/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_15_A`](../round1_sessions/team_05_prompt_15.md) | `team_05` | G1 | Exact rational Gröbner basis computation on the 18-variable corner… | `19/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_15_B`](../round1_sessions/team_05_prompt_15.md) | `team_05` | G1 | Dual witness certificate for Exact rational Gröbner basis… | `1/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_16_A`](../round1_sessions/team_05_prompt_16.md) | `team_05` | G1 | Real radical ideal computation $\sqrt[\mathbb{R}]{I(\mathcal{H}_6)}… | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_16_B`](../round1_sessions/team_05_prompt_16.md) | `team_05` | G1 | Dual witness certificate for Real radical ideal computation… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_17_A`](../round1_sessions/team_05_prompt_17.md) | `team_05` | G1 | Degree bounds on the Nullstellensatz certificates for the corner… | `61/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_17_B`](../round1_sessions/team_05_prompt_17.md) | `team_05` | G1 | Dual witness certificate for Degree bounds on the Nullstellensatz… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_18_A`](../round1_sessions/team_05_prompt_18.md) | `team_05` | G1 | Network Simplex dual witness certifying non-extendibility of… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_18_B`](../round1_sessions/team_05_prompt_18.md) | `team_05` | G1 | Dual witness certificate for Network Simplex dual witness… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_19_A`](../round1_sessions/team_05_prompt_19.md) | `team_05` | G1 | Exact rational certifier verifying corner reconstruction in Python… | `23/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_19_B`](../round1_sessions/team_05_prompt_19.md) | `team_05` | G1 | Dual witness certificate for Exact rational certifier verifying… | `5/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_20_A`](../round1_sessions/team_05_prompt_20.md) | `team_05` | G1 | Negative control test suite rejecting corrupted or perturbed… | `2/1 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_20_B`](../round1_sessions/team_05_prompt_20.md) | `team_05` | G1 | Dual witness certificate for Negative control test suite rejecting… | `1/2 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_21_A`](../round1_sessions/team_05_prompt_21.md) | `team_05` | G1 | Lean 4 formalization of the 50-variable variety equations in… | `25/2 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_21_B`](../round1_sessions/team_05_prompt_21.md) | `team_05` | G1 | Dual witness certificate for Lean 4 formalization of the… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_22_A`](../round1_sessions/team_05_prompt_22.md) | `team_05` | G1 | Lean 4 proposed derivation of the Triad Compatibility Hadamard… | `19/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_22_B`](../round1_sessions/team_05_prompt_22.md) | `team_05` | G1 | Dual witness certificate for Lean 4 proposed derivation of the… | `1/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_23_A`](../round1_sessions/team_05_prompt_23.md) | `team_05` | G1 | Lean 4 proposed derivation of `TriadModuliPigeonhole` lemma. | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_23_B`](../round1_sessions/team_05_prompt_23.md) | `team_05` | G1 | Dual witness certificate for Lean 4 proposed derivation of… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_24_A`](../round1_sessions/team_05_prompt_24.md) | `team_05` | G1 | Axiom audit of the Target G1 Lean formalization: strictly… | `7/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_24_B`](../round1_sessions/team_05_prompt_24.md) | `team_05` | G1 | Dual witness certificate for Axiom audit of the Target G1 Lean… | `1/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T05_25_A`](../round1_sessions/team_05_prompt_25.md) | `team_05` | G1 | Master synthesis of Target G1 Foundation & Orbit Exhaustiveness… | `89/6 → 0/1` | PROMISING | [follow-up](../round2_sessions/team_05_prompt_25.md) |
| [`PROP_PROMPT_T05_25_B`](../round1_sessions/team_05_prompt_25.md) | `team_05` | G1 | Dual witness certificate for Master synthesis of Target G1… | `0/1 → 0/1` | INCREMENTAL | [follow-up](../round2_sessions/team_05_prompt_25.md) |
| [`PROP_PROMPT_T06_01_A`](../round1_sessions/team_06_prompt_01.md) | `team_06` | Q-Soundness | Generation of the free unital $*$-algebra on 24 formal symbols… | `5/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_01_B`](../round1_sessions/team_06_prompt_01.md) | `team_06` | Q-Soundness | Dual witness certificate for Generation of the free unital… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_02_A`](../round1_sessions/team_06_prompt_02.md) | `team_06` | Q-Soundness | Formalization of the self-adjoint involution $w \mapsto w^*$ by… | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_02_B`](../round1_sessions/team_06_prompt_02.md) | `team_06` | Q-Soundness | Dual witness certificate for Formalization of the self-adjoint… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_03_A`](../round1_sessions/team_06_prompt_03.md) | `team_06` | Q-Soundness | Canonical term rewriting system for idempotency $\Pi_{i, a}^2 \to… | `7/4 → 1/4` | PROMISING | [follow-up](../round2_sessions/team_06_prompt_03.md) |
| [`PROP_PROMPT_T06_03_B`](../round1_sessions/team_06_prompt_03.md) | `team_06` | Q-Soundness | Dual witness certificate for Canonical term rewriting system for… | `1/4 → 1/4` | INCREMENTAL | [follow-up](../round2_sessions/team_06_prompt_03.md) |
| [`PROP_PROMPT_T06_04_A`](../round1_sessions/team_06_prompt_04.md) | `team_06` | Q-Soundness | Canonical term rewriting for intra-basis orthogonality $\Pi_{i, a}… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_04_B`](../round1_sessions/team_06_prompt_04.md) | `team_06` | Q-Soundness | Dual witness certificate for Canonical term rewriting for… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_05_A`](../round1_sessions/team_06_prompt_05.md) | `team_06` | Q-Soundness | Resolution of identity reduction $\sum_{a=0}^5 \Pi_{i, a} \to… | `19/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_05_B`](../round1_sessions/team_06_prompt_05.md) | `team_06` | Q-Soundness | Dual witness certificate for Resolution of identity reduction… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_06_A`](../round1_sessions/team_06_prompt_06.md) | `team_06` | Q-Soundness | Confluence and termination of the non-commutative term rewriting… | `2/1 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_06_B`](../round1_sessions/team_06_prompt_06.md) | `team_06` | Q-Soundness | Dual witness certificate for Confluence and termination of the… | `1/2 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_07_A`](../round1_sessions/team_06_prompt_07.md) | `team_06` | Q-Soundness | Basis monomial enumeration for word lengths $d \in \{1, 2, 3, 4\}$. | `25/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_07_B`](../round1_sessions/team_06_prompt_07.md) | `team_06` | Q-Soundness | Dual witness certificate for Basis monomial enumeration for word… | `7/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_08_A`](../round1_sessions/team_06_prompt_08.md) | `team_06` | Q-Soundness | Dimension count of the truncated word subspace $\mathcal{W}_{\le… | `19/12 → 1/12` | PROMISING | [follow-up](../round2_sessions/team_06_prompt_08.md) |
| [`PROP_PROMPT_T06_08_B`](../round1_sessions/team_06_prompt_08.md) | `team_06` | Q-Soundness | Dual witness certificate for Dimension count of the truncated word… | `1/12 → 1/12` | INCREMENTAL | [follow-up](../round2_sessions/team_06_prompt_08.md) |
| [`PROP_PROMPT_T06_09_A`](../round1_sessions/team_06_prompt_09.md) | `team_06` | Q-Soundness | Dimension count of $\mathcal{W}_{\le 2}$ (projector pairs, NPA… | `11/2 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_09_B`](../round1_sessions/team_06_prompt_09.md) | `team_06` | Q-Soundness | Dual witness certificate for Dimension count of $\mathcal{W}_{\le… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_10_A`](../round1_sessions/team_06_prompt_10.md) | `team_06` | Q-Soundness | Dimension count of $\mathcal{W}_{\le 3}$ (projector triples, NPA… | `7/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_10_B`](../round1_sessions/team_06_prompt_10.md) | `team_06` | Q-Soundness | Dual witness certificate for Dimension count of $\mathcal{W}_{\le… | `1/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_11_A`](../round1_sessions/team_06_prompt_11.md) | `team_06` | Q-Soundness | Dimension count of $\mathcal{W}_{\le 4}$ (projector quadruples… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_11_B`](../round1_sessions/team_06_prompt_11.md) | `team_06` | Q-Soundness | Dual witness certificate for Dimension count of $\mathcal{W}_{\le… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_12_A`](../round1_sessions/team_06_prompt_12.md) | `team_06` | Q-Soundness | Mutual unbiasedness trace condition $\operatorname{Tr}(\Pi_{i, a}… | `23/12 → 5/12` | PROMISING | [follow-up](../round2_sessions/team_06_prompt_12.md) |
| [`PROP_PROMPT_T06_12_B`](../round1_sessions/team_06_prompt_12.md) | `team_06` | Q-Soundness | Dual witness certificate for Mutual unbiasedness trace condition… | `5/12 → 5/12` | INCREMENTAL | [follow-up](../round2_sessions/team_06_prompt_12.md) |
| [`PROP_PROMPT_T06_13_A`](../round1_sessions/team_06_prompt_13.md) | `team_06` | Q-Soundness | Representation of the quadratic module… | `47/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_13_B`](../round1_sessions/team_06_prompt_13.md) | `team_06` | Q-Soundness | Dual witness certificate for Representation of the quadratic… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_14_A`](../round1_sessions/team_06_prompt_14.md) | `team_06` | Q-Soundness | Exact rational polynomial arithmetic over reduced words in Python… | `25/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_14_B`](../round1_sessions/team_06_prompt_14.md) | `team_06` | Q-Soundness | Dual witness certificate for Exact rational polynomial arithmetic… | `7/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_15_A`](../round1_sessions/team_06_prompt_15.md) | `team_06` | Q-Soundness | Exact rational polynomial arithmetic over reduced words in Rust… | `19/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_15_B`](../round1_sessions/team_06_prompt_15.md) | `team_06` | Q-Soundness | Dual witness certificate for Exact rational polynomial arithmetic… | `1/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_16_A`](../round1_sessions/team_06_prompt_16.md) | `team_06` | Q-Soundness | Verification of involution preservation under multiplication: $(u… | `5/3 → 1/6` | PROMISING | [follow-up](../round2_sessions/team_06_prompt_16.md) |
| [`PROP_PROMPT_T06_16_B`](../round1_sessions/team_06_prompt_16.md) | `team_06` | Q-Soundness | Dual witness certificate for Verification of involution… | `1/6 → 1/6` | INCREMENTAL | [follow-up](../round2_sessions/team_06_prompt_16.md) |
| [`PROP_PROMPT_T06_17_A`](../round1_sessions/team_06_prompt_17.md) | `team_06` | Q-Soundness | Characterization of the non-commutative commutator ideal $[\Pi_{i… | `61/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_17_B`](../round1_sessions/team_06_prompt_17.md) | `team_06` | Q-Soundness | Dual witness certificate for Characterization of the… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_18_A`](../round1_sessions/team_06_prompt_18.md) | `team_06` | Q-Soundness | Non-triviality of the commutator ideal for $i \neq j$ (quantum… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_18_B`](../round1_sessions/team_06_prompt_18.md) | `team_06` | Q-Soundness | Dual witness certificate for Non-triviality of the commutator… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_19_A`](../round1_sessions/team_06_prompt_19.md) | `team_06` | Q-Soundness | Truncated test vector representation $c : \mathcal{W}_{\le d} \to… | `23/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_19_B`](../round1_sessions/team_06_prompt_19.md) | `team_06` | Q-Soundness | Dual witness certificate for Truncated test vector representation… | `5/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_20_A`](../round1_sessions/team_06_prompt_20.md) | `team_06` | Q-Soundness | Exact inner product $\langle u, v \rangle = \tilde{\mathbb{E}}[u^*… | `2/1 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_20_B`](../round1_sessions/team_06_prompt_20.md) | `team_06` | Q-Soundness | Dual witness certificate for Exact inner product $\langle u, v… | `1/2 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_21_A`](../round1_sessions/team_06_prompt_21.md) | `team_06` | Q-Soundness | Negative control testing: rejecting unreduced words with adjacent… | `25/2 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_21_B`](../round1_sessions/team_06_prompt_21.md) | `team_06` | Q-Soundness | Dual witness certificate for Negative control testing: rejecting… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_22_A`](../round1_sessions/team_06_prompt_22.md) | `team_06` | Q-Soundness | Lean 4 formalization of the reduced word inductive type in… | `19/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_22_B`](../round1_sessions/team_06_prompt_22.md) | `team_06` | Q-Soundness | Dual witness certificate for Lean 4 formalization of the reduced… | `1/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_23_A`](../round1_sessions/team_06_prompt_23.md) | `team_06` | Q-Soundness | Lean 4 proposed derivation of involution anti-automorphism: $(w_1… | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_23_B`](../round1_sessions/team_06_prompt_23.md) | `team_06` | Q-Soundness | Dual witness certificate for Lean 4 proposed derivation of… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_24_A`](../round1_sessions/team_06_prompt_24.md) | `team_06` | Q-Soundness | Axiom audit on algebraic word reduction: zero non-standard axioms. | `7/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_24_B`](../round1_sessions/team_06_prompt_24.md) | `team_06` | Q-Soundness | Dual witness certificate for Axiom audit on algebraic word… | `1/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T06_25_A`](../round1_sessions/team_06_prompt_25.md) | `team_06` | Q-Soundness | Master synthesis of the non-commutative projector algebra… | `89/6 → 0/1` | PROMISING | [follow-up](../round2_sessions/team_06_prompt_25.md) |
| [`PROP_PROMPT_T06_25_B`](../round1_sessions/team_06_prompt_25.md) | `team_06` | Q-Soundness | Dual witness certificate for Master synthesis of the… | `0/1 → 0/1` | INCREMENTAL | [follow-up](../round2_sessions/team_06_prompt_25.md) |
| [`PROP_PROMPT_T07_01_A`](../round1_sessions/team_07_prompt_01.md) | `team_07` | Q-Soundness | Construction of Degree-2 moment matrix $M_2$ (size $25 \times 25$)… | `5/6 → 0/1` | BLOCKED | [follow-up](../round2_sessions/team_07_prompt_01.md) |
| [`PROP_PROMPT_T07_01_B`](../round1_sessions/team_07_prompt_01.md) | `team_07` | Q-Soundness | Dual witness certificate for Construction of Degree-2 moment… | `0/1 → 0/1` | INCREMENTAL | [follow-up](../round2_sessions/team_07_prompt_01.md) |
| [`PROP_PROMPT_T07_02_A`](../round1_sessions/team_07_prompt_02.md) | `team_07` | Q-Soundness | Exact rational $LDL^T$ decomposition of $M_2$ verifying pivot… | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_02_B`](../round1_sessions/team_07_prompt_02.md) | `team_07` | Q-Soundness | Dual witness certificate for Exact rational $LDL^T$ decomposition… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_03_A`](../round1_sessions/team_07_prompt_03.md) | `team_07` | Q-Soundness | Construction of Degree-4 moment matrix $M_4$ incorporating… | `7/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_03_B`](../round1_sessions/team_07_prompt_03.md) | `team_07` | Q-Soundness | Dual witness certificate for Construction of Degree-4 moment… | `1/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_04_A`](../round1_sessions/team_07_prompt_04.md) | `team_07` | Q-Soundness | Exact rational $LDL^T$ decomposition of $M_4$ and pivot spectrum… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_04_B`](../round1_sessions/team_07_prompt_04.md) | `team_07` | Q-Soundness | Dual witness certificate for Exact rational $LDL^T$ decomposition… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_05_A`](../round1_sessions/team_07_prompt_05.md) | `team_07` | Q-Soundness | Construction of Degree-6 moment matrix $M_6$ incorporating… | `19/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_05_B`](../round1_sessions/team_07_prompt_05.md) | `team_07` | Q-Soundness | Dual witness certificate for Construction of Degree-6 moment… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_06_A`](../round1_sessions/team_07_prompt_06.md) | `team_07` | Q-Soundness | Evaluation of candidate completion $X = 0$ on $M_6$… | `2/1 → 1/2` | PROMISING | [follow-up](../round2_sessions/team_07_prompt_06.md) |
| [`PROP_PROMPT_T07_06_B`](../round1_sessions/team_07_prompt_06.md) | `team_07` | Q-Soundness | Dual witness certificate for Evaluation of candidate completion $X… | `1/2 → 1/2` | INCREMENTAL | [follow-up](../round2_sessions/team_07_prompt_06.md) |
| [`PROP_PROMPT_T07_07_A`](../round1_sessions/team_07_prompt_07.md) | `team_07` | Q-Soundness | Construction of Degree-8 moment matrix $M_8$ incorporating… | `25/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_07_B`](../round1_sessions/team_07_prompt_07.md) | `team_07` | Q-Soundness | Dual witness certificate for Construction of Degree-8 moment… | `7/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_08_A`](../round1_sessions/team_07_prompt_08.md) | `team_07` | Q-Soundness | Evaluation of candidate completion $X = 0$ on $M_8$… | `19/12 → 1/12` | PROMISING | [follow-up](../round2_sessions/team_07_prompt_08.md) |
| [`PROP_PROMPT_T07_08_B`](../round1_sessions/team_07_prompt_08.md) | `team_07` | Q-Soundness | Dual witness certificate for Evaluation of candidate completion $X… | `1/12 → 1/12` | INCREMENTAL | [follow-up](../round2_sessions/team_07_prompt_08.md) |
| [`PROP_PROMPT_T07_09_A`](../round1_sessions/team_07_prompt_09.md) | `team_07` | Q-Soundness | Evaluation of synthetic $S_6$ candidate completion on $M_8$… | `11/2 → 0/1` | PROMISING | [follow-up](../round2_sessions/team_07_prompt_09.md) |
| [`PROP_PROMPT_T07_09_B`](../round1_sessions/team_07_prompt_09.md) | `team_07` | Q-Soundness | Dual witness certificate for Evaluation of synthetic $S_6$… | `0/1 → 0/1` | INCREMENTAL | [follow-up](../round2_sessions/team_07_prompt_09.md) |
| [`PROP_PROMPT_T07_10_A`](../round1_sessions/team_07_prompt_10.md) | `team_07` | Q-Soundness | Factored dual witness representation $W = \sum D_k c^{(k)}… | `7/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_10_B`](../round1_sessions/team_07_prompt_10.md) | `team_07` | Q-Soundness | Dual witness certificate for Factored dual witness representation… | `1/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_11_A`](../round1_sessions/team_07_prompt_11.md) | `team_07` | Q-Soundness | Constructive proposed task to establish whether… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_11_B`](../round1_sessions/team_07_prompt_11.md) | `team_07` | Q-Soundness | Dual witness certificate for Constructive proposed task to… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_12_A`](../round1_sessions/team_07_prompt_12.md) | `team_07` | Q-Soundness | Bit-for-bit SHA-256 fingerprint agreement for $M_2, M_4, M_6, M_8$… | `23/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_12_B`](../round1_sessions/team_07_prompt_12.md) | `team_07` | Q-Soundness | Dual witness certificate for Bit-for-bit SHA-256 fingerprint… | `5/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_13_A`](../round1_sessions/team_07_prompt_13.md) | `team_07` | Q-Soundness | Pivot signature verification: confirming zero negative pivots in… | `47/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_13_B`](../round1_sessions/team_07_prompt_13.md) | `team_07` | Q-Soundness | Dual witness certificate for Pivot signature verification… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_14_A`](../round1_sessions/team_07_prompt_14.md) | `team_07` | Q-Soundness | Cross-runtime fixture validation in `test_target_q4_degree8_sdp.py`. | `25/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_14_B`](../round1_sessions/team_07_prompt_14.md) | `team_07` | Q-Soundness | Dual witness certificate for Cross-runtime fixture validation in… | `7/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_15_A`](../round1_sessions/team_07_prompt_15.md) | `team_07` | Q-Soundness | Native Rust release-mode test suite in `test_degree8_sdp.rs`. | `19/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_15_B`](../round1_sessions/team_07_prompt_15.md) | `team_07` | Q-Soundness | Dual witness certificate for Native Rust release-mode test suite… | `1/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_16_A`](../round1_sessions/team_07_prompt_16.md) | `team_07` | Q-Soundness | Negative control suite: rejecting non-symmetric matrices and… | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_16_B`](../round1_sessions/team_07_prompt_16.md) | `team_07` | Q-Soundness | Dual witness certificate for Negative control suite: rejecting… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_17_A`](../round1_sessions/team_07_prompt_17.md) | `team_07` | Q-Soundness | AST-level zero-float verification on Rust moment matrix builders. | `61/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_17_B`](../round1_sessions/team_07_prompt_17.md) | `team_07` | Q-Soundness | Dual witness certificate for AST-level zero-float verification on… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_18_A`](../round1_sessions/team_07_prompt_18.md) | `team_07` | Q-Soundness | Recursive `assert_no_float` on all Python moment matrix entries. | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_18_B`](../round1_sessions/team_07_prompt_18.md) | `team_07` | Q-Soundness | Dual witness certificate for Recursive `assert_no_float` on all… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_19_A`](../round1_sessions/team_07_prompt_19.md) | `team_07` | Q-Soundness | Unified diagnostic ledger API for multi-degree SDP moments. | `23/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_19_B`](../round1_sessions/team_07_prompt_19.md) | `team_07` | Q-Soundness | Dual witness certificate for Unified diagnostic ledger API for… | `5/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_20_A`](../round1_sessions/team_07_prompt_20.md) | `team_07` | Q-Soundness | Separation between candidate refutation and global search refusal. | `2/1 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_20_B`](../round1_sessions/team_07_prompt_20.md) | `team_07` | Q-Soundness | Dual witness certificate for Separation between candidate… | `1/2 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_21_A`](../round1_sessions/team_07_prompt_21.md) | `team_07` | Q-Soundness | Lean 4 formalization of factored dual witness and trace inner… | `25/2 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_21_B`](../round1_sessions/team_07_prompt_21.md) | `team_07` | Q-Soundness | Dual witness certificate for Lean 4 formalization of factored dual… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_22_A`](../round1_sessions/team_07_prompt_22.md) | `team_07` | Q-Soundness | Lean 4 constructive theorem: `certified_candidate_refutation`. | `19/12 → 1/12` | PROMISING | [follow-up](../round2_sessions/team_07_prompt_22.md) |
| [`PROP_PROMPT_T07_22_B`](../round1_sessions/team_07_prompt_22.md) | `team_07` | Q-Soundness | Dual witness certificate for Lean 4 constructive theorem… | `1/12 → 1/12` | INCREMENTAL | [follow-up](../round2_sessions/team_07_prompt_22.md) |
| [`PROP_PROMPT_T07_23_A`](../round1_sessions/team_07_prompt_23.md) | `team_07` | Q-Soundness | Lean 4 constructive theorem: `dual_witness_trace_nonneg_of_moment_p… | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_23_B`](../round1_sessions/team_07_prompt_23.md) | `team_07` | Q-Soundness | Dual witness certificate for Lean 4 constructive theorem… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_24_A`](../round1_sessions/team_07_prompt_24.md) | `team_07` | Q-Soundness | Axiom audit of Lean 4 moment matrix theorems: strictly `[propext… | `7/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_24_B`](../round1_sessions/team_07_prompt_24.md) | `team_07` | Q-Soundness | Dual witness certificate for Axiom audit of Lean 4 moment matrix… | `1/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_25_A`](../round1_sessions/team_07_prompt_25.md) | `team_07` | Q-Soundness | Master synthesis of the multi-degree moment SDP hierarchy ledger. | `89/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T07_25_B`](../round1_sessions/team_07_prompt_25.md) | `team_07` | Q-Soundness | Dual witness certificate for Master synthesis of the multi-degree… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_01_A`](../round1_sessions/team_08_prompt_01.md) | `team_08` | Q-Soundness | Formulation of the quadratic module… | `5/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_01_B`](../round1_sessions/team_08_prompt_01.md) | `team_08` | Q-Soundness | Dual witness certificate for Formulation of the quadratic module… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_02_A`](../round1_sessions/team_08_prompt_02.md) | `team_08` | Q-Soundness | Definition of the Archimedean property: $\exists R \in \mathbb{Q}$… | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_02_B`](../round1_sessions/team_08_prompt_02.md) | `team_08` | Q-Soundness | Dual witness certificate for Definition of the Archimedean… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_03_A`](../round1_sessions/team_08_prompt_03.md) | `team_08` | Q-Soundness | Construction of explicit exact rational Archimedean certificate… | `7/4 → 1/4` | PROMISING | [follow-up](../round2_sessions/team_08_prompt_03.md) |
| [`PROP_PROMPT_T08_03_B`](../round1_sessions/team_08_prompt_03.md) | `team_08` | Q-Soundness | Dual witness certificate for Construction of explicit exact… | `1/4 → 1/4` | INCREMENTAL | [follow-up](../round2_sessions/team_08_prompt_03.md) |
| [`PROP_PROMPT_T08_04_A`](../round1_sessions/team_08_prompt_04.md) | `team_08` | Q-Soundness | Bound radius calculation: proving $R = \sqrt{24} \le 5$ (exact… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_04_B`](../round1_sessions/team_08_prompt_04.md) | `team_08` | Q-Soundness | Dual witness certificate for Bound radius calculation: proving $R… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_05_A`](../round1_sessions/team_08_prompt_05.md) | `team_08` | Q-Soundness | Algebraic identity: $1 - \Pi_{i,a} = (1 - \Pi_{i,a})^2 \in… | `19/6 → 0/1` | PROMISING | [follow-up](../round2_sessions/team_08_prompt_05.md) |
| [`PROP_PROMPT_T08_05_B`](../round1_sessions/team_08_prompt_05.md) | `team_08` | Q-Soundness | Dual witness certificate for Algebraic identity: $1 - \Pi_{i,a} =… | `0/1 → 0/1` | INCREMENTAL | [follow-up](../round2_sessions/team_08_prompt_05.md) |
| [`PROP_PROMPT_T08_06_A`](../round1_sessions/team_08_prompt_06.md) | `team_08` | Q-Soundness | Sum-of-squares decomposition of the norm bound in the projector… | `2/1 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_06_B`](../round1_sessions/team_08_prompt_06.md) | `team_08` | Q-Soundness | Dual witness certificate for Sum-of-squares decomposition of the… | `1/2 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_07_A`](../round1_sessions/team_08_prompt_07.md) | `team_08` | Q-Soundness | Helton-McCullough non-commutative Positivstellensatz application… | `25/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_07_B`](../round1_sessions/team_08_prompt_07.md) | `team_08` | Q-Soundness | Dual witness certificate for Helton-McCullough non-commutative… | `7/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_08_A`](../round1_sessions/team_08_prompt_08.md) | `team_08` | Q-Soundness | proposed derivation of asymptotic convergence of the NPA /… | `19/12 → 1/12` | PROMISING | [follow-up](../round2_sessions/team_08_prompt_08.md) |
| [`PROP_PROMPT_T08_08_B`](../round1_sessions/team_08_prompt_08.md) | `team_08` | Q-Soundness | Dual witness certificate for proposed derivation of asymptotic… | `1/12 → 1/12` | INCREMENTAL | [follow-up](../round2_sessions/team_08_prompt_08.md) |
| [`PROP_PROMPT_T08_09_A`](../round1_sessions/team_08_prompt_09.md) | `team_08` | Q-Soundness | Bridging pseudo-expectations to true states: Gelfand-Naimark-Segal… | `11/2 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_09_B`](../round1_sessions/team_08_prompt_09.md) | `team_08` | Q-Soundness | Dual witness certificate for Bridging pseudo-expectations to true… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_10_A`](../round1_sessions/team_08_prompt_10.md) | `team_08` | Q-Soundness | proposed task to establish whether an Archimedean certificate… | `7/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_10_B`](../round1_sessions/team_08_prompt_10.md) | `team_08` | Q-Soundness | Dual witness certificate for proposed task to establish whether an… | `1/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_11_A`](../round1_sessions/team_08_prompt_11.md) | `team_08` | Q-Soundness | Exact rational certificate generator in Python for the Archimedean… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_11_B`](../round1_sessions/team_08_prompt_11.md) | `team_08` | Q-Soundness | Dual witness certificate for Exact rational certificate generator… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_12_A`](../round1_sessions/team_08_prompt_12.md) | `team_08` | Q-Soundness | Exact rational certificate verifier in Rust with zero float leakage. | `23/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_12_B`](../round1_sessions/team_08_prompt_12.md) | `team_08` | Q-Soundness | Dual witness certificate for Exact rational certificate verifier… | `5/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_13_A`](../round1_sessions/team_08_prompt_13.md) | `team_08` | Q-Soundness | Evaluation of degree bounds for Archimedean Positivstellensatz… | `47/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_13_B`](../round1_sessions/team_08_prompt_13.md) | `team_08` | Q-Soundness | Dual witness certificate for Evaluation of degree bounds for… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_14_A`](../round1_sessions/team_08_prompt_14.md) | `team_08` | Q-Soundness | Connecting Archimedean Positivstellensatz to the Artin-Schreier… | `25/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_14_B`](../round1_sessions/team_08_prompt_14.md) | `team_08` | Q-Soundness | Dual witness certificate for Connecting Archimedean… | `7/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_15_A`](../round1_sessions/team_08_prompt_15.md) | `team_08` | Q-Soundness | Negative control suite: rejecting perturbed or non-SOS quadratic… | `19/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_15_B`](../round1_sessions/team_08_prompt_15.md) | `team_08` | Q-Soundness | Dual witness certificate for Negative control suite: rejecting… | `1/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_16_A`](../round1_sessions/team_08_prompt_16.md) | `team_08` | Q-Soundness | Exact rational certificate serialization into JSON schema format. | `5/3 → 1/6` | PROMISING | [follow-up](../round2_sessions/team_08_prompt_16.md) |
| [`PROP_PROMPT_T08_16_B`](../round1_sessions/team_08_prompt_16.md) | `team_08` | Q-Soundness | Dual witness certificate for Exact rational certificate… | `1/6 → 1/6` | INCREMENTAL | [follow-up](../round2_sessions/team_08_prompt_16.md) |
| [`PROP_PROMPT_T08_17_A`](../round1_sessions/team_08_prompt_17.md) | `team_08` | Q-Soundness | Cryptographic SHA-256 digest pinning of the Archimedean… | `61/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_17_B`](../round1_sessions/team_08_prompt_17.md) | `team_08` | Q-Soundness | Dual witness certificate for Cryptographic SHA-256 digest pinning… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_18_A`](../round1_sessions/team_08_prompt_18.md) | `team_08` | Q-Soundness | Lean 4 formalization of `ArchimedeanPositivstellensatzCertificate`… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_18_B`](../round1_sessions/team_08_prompt_18.md) | `team_08` | Q-Soundness | Dual witness certificate for Lean 4 formalization of… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_19_A`](../round1_sessions/team_08_prompt_19.md) | `team_08` | Q-Soundness | Lean 4 proof: `sound_global_exclusion_via_positivstellensatz`. | `23/12 → 5/12` | PROMISING | [follow-up](../round2_sessions/team_08_prompt_19.md) |
| [`PROP_PROMPT_T08_19_B`](../round1_sessions/team_08_prompt_19.md) | `team_08` | Q-Soundness | Dual witness certificate for Lean 4 proof… | `5/12 → 5/12` | INCREMENTAL | [follow-up](../round2_sessions/team_08_prompt_19.md) |
| [`PROP_PROMPT_T08_20_A`](../round1_sessions/team_08_prompt_20.md) | `team_08` | Q-Soundness | Lean 4 proposed task to establish whether physical quantum… | `2/1 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_20_B`](../round1_sessions/team_08_prompt_20.md) | `team_08` | Q-Soundness | Dual witness certificate for Lean 4 proposed task to establish… | `1/2 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_21_A`](../round1_sessions/team_08_prompt_21.md) | `team_08` | Q-Soundness | Discharging the open proof obligation… | `25/2 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_21_B`](../round1_sessions/team_08_prompt_21.md) | `team_08` | Q-Soundness | Dual witness certificate for Discharging the open proof obligation… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_22_A`](../round1_sessions/team_08_prompt_22.md) | `team_08` | Q-Soundness | Axiom audit on Positivstellensatz theorems: strictly `[propext… | `19/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_22_B`](../round1_sessions/team_08_prompt_22.md) | `team_08` | Q-Soundness | Dual witness certificate for Axiom audit on Positivstellensatz… | `1/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_23_A`](../round1_sessions/team_08_prompt_23.md) | `team_08` | Q-Soundness | Boundary check: distinguishing between asymptotic convergence and… | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_23_B`](../round1_sessions/team_08_prompt_23.md) | `team_08` | Q-Soundness | Dual witness certificate for Boundary check: distinguishing… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_24_A`](../round1_sessions/team_08_prompt_24.md) | `team_08` | Q-Soundness | Integration of Archimedean Positivstellensatz with the master… | `7/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_24_B`](../round1_sessions/team_08_prompt_24.md) | `team_08` | Q-Soundness | Dual witness certificate for Integration of Archimedean… | `1/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_25_A`](../round1_sessions/team_08_prompt_25.md) | `team_08` | Q-Soundness | Master synthesis of the Archimedean Positivstellensatz Soundness… | `89/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T08_25_B`](../round1_sessions/team_08_prompt_25.md) | `team_08` | Q-Soundness | Dual witness certificate for Master synthesis of the Archimedean… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_01_A`](../round1_sessions/team_09_prompt_01.md) | `team_09` | Q-Soundness | Formulation of the non-commutative flat extension condition… | `5/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_01_B`](../round1_sessions/team_09_prompt_01.md) | `team_09` | Q-Soundness | Dual witness certificate for Formulation of the non-commutative… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_02_A`](../round1_sessions/team_09_prompt_02.md) | `team_09` | Q-Soundness | Curto-Fialkow flat extension theorem adapted to non-commutative… | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_02_B`](../round1_sessions/team_09_prompt_02.md) | `team_09` | Q-Soundness | Dual witness certificate for Curto-Fialkow flat extension theorem… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_03_A`](../round1_sessions/team_09_prompt_03.md) | `team_09` | Q-Soundness | Rank calculation on Degree-2 moment matrix $M_2$… | `7/4 → 1/4` | BLOCKED | [follow-up](../round2_sessions/team_09_prompt_03.md) |
| [`PROP_PROMPT_T09_03_B`](../round1_sessions/team_09_prompt_03.md) | `team_09` | Q-Soundness | Dual witness certificate for Rank calculation on Degree-2 moment… | `1/4 → 1/4` | INCREMENTAL | [follow-up](../round2_sessions/team_09_prompt_03.md) |
| [`PROP_PROMPT_T09_04_A`](../round1_sessions/team_09_prompt_04.md) | `team_09` | Q-Soundness | Rank calculation on Degree-4 moment matrix $M_4$: checking… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_04_B`](../round1_sessions/team_09_prompt_04.md) | `team_09` | Q-Soundness | Dual witness certificate for Rank calculation on Degree-4 moment… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_05_A`](../round1_sessions/team_09_prompt_05.md) | `team_09` | Q-Soundness | Rank calculation on Degree-6 moment matrix $M_6$: checking… | `19/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_05_B`](../round1_sessions/team_09_prompt_05.md) | `team_09` | Q-Soundness | Dual witness certificate for Rank calculation on Degree-6 moment… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_06_A`](../round1_sessions/team_09_prompt_06.md) | `team_09` | Q-Soundness | Rank calculation on Degree-8 moment matrix $M_8$: checking… | `2/1 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_06_B`](../round1_sessions/team_09_prompt_06.md) | `team_09` | Q-Soundness | Dual witness certificate for Rank calculation on Degree-8 moment… | `1/2 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_07_A`](../round1_sessions/team_09_prompt_07.md) | `team_09` | Q-Soundness | Evaluation of the rank-gap sequence $\Delta_d =… | `25/12 → 7/12` | BLOCKED | [follow-up](../round2_sessions/team_09_prompt_07.md) |
| [`PROP_PROMPT_T09_07_B`](../round1_sessions/team_09_prompt_07.md) | `team_09` | Q-Soundness | Dual witness certificate for Evaluation of the rank-gap sequence… | `7/12 → 7/12` | INCREMENTAL | [follow-up](../round2_sessions/team_09_prompt_07.md) |
| [`PROP_PROMPT_T09_08_A`](../round1_sessions/team_09_prompt_08.md) | `team_09` | Q-Soundness | proposed task to establish whether $\Delta_d > 0$ across all… | `19/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_08_B`](../round1_sessions/team_09_prompt_08.md) | `team_09` | Q-Soundness | Dual witness certificate for proposed task to establish whether… | `1/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_09_A`](../round1_sessions/team_09_prompt_09.md) | `team_09` | Q-Soundness | Exact rational spectral analysis of the non-commutative GNS kernel… | `11/2 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_09_B`](../round1_sessions/team_09_prompt_09.md) | `team_09` | Q-Soundness | Dual witness certificate for Exact rational spectral analysis of… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_10_A`](../round1_sessions/team_09_prompt_10.md) | `team_09` | Q-Soundness | Construction of the GNS pre-Hilbert space… | `7/4 → 1/4` | PROMISING | [follow-up](../round2_sessions/team_09_prompt_10.md) |
| [`PROP_PROMPT_T09_10_B`](../round1_sessions/team_09_prompt_10.md) | `team_09` | Q-Soundness | Dual witness certificate for Construction of the GNS pre-Hilbert… | `1/4 → 1/4` | INCREMENTAL | [follow-up](../round2_sessions/team_09_prompt_10.md) |
| [`PROP_PROMPT_T09_11_A`](../round1_sessions/team_09_prompt_11.md) | `team_09` | Q-Soundness | GNS operator representation: $\pi(w)[u] = [w u]$. | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_11_B`](../round1_sessions/team_09_prompt_11.md) | `team_09` | Q-Soundness | Dual witness certificate for GNS operator representation… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_12_A`](../round1_sessions/team_09_prompt_12.md) | `team_09` | Q-Soundness | Well-definedness of GNS representation iff flat extension… | `23/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_12_B`](../round1_sessions/team_09_prompt_12.md) | `team_09` | Q-Soundness | Dual witness certificate for Well-definedness of GNS… | `5/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_13_A`](../round1_sessions/team_09_prompt_13.md) | `team_09` | Q-Soundness | Algebraic obstruction to flat extension: proposed task to… | `47/6 → 0/1` | BLOCKED | [follow-up](../round2_sessions/team_09_prompt_13.md) |
| [`PROP_PROMPT_T09_13_B`](../round1_sessions/team_09_prompt_13.md) | `team_09` | Q-Soundness | Dual witness certificate for Algebraic obstruction to flat… | `0/1 → 0/1` | INCREMENTAL | [follow-up](../round2_sessions/team_09_prompt_13.md) |
| [`PROP_PROMPT_T09_14_A`](../round1_sessions/team_09_prompt_14.md) | `team_09` | Q-Soundness | Exact rational rank evaluation algorithm over $\mathbb{Q}$ using… | `25/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_14_B`](../round1_sessions/team_09_prompt_14.md) | `team_09` | Q-Soundness | Dual witness certificate for Exact rational rank evaluation… | `7/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_15_A`](../round1_sessions/team_09_prompt_15.md) | `team_09` | Q-Soundness | Rust implementation of exact rational rank evaluator over… | `19/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_15_B`](../round1_sessions/team_09_prompt_15.md) | `team_09` | Q-Soundness | Dual witness certificate for Rust implementation of exact rational… | `1/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_16_A`](../round1_sessions/team_09_prompt_16.md) | `team_09` | Q-Soundness | Python implementation of exact rational rank evaluator over… | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_16_B`](../round1_sessions/team_09_prompt_16.md) | `team_09` | Q-Soundness | Dual witness certificate for Python implementation of exact… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_17_A`](../round1_sessions/team_09_prompt_17.md) | `team_09` | Q-Soundness | Negative control suite: rejecting rank over-claims or near-zero… | `61/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_17_B`](../round1_sessions/team_09_prompt_17.md) | `team_09` | Q-Soundness | Dual witness certificate for Negative control suite: rejecting… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_18_A`](../round1_sessions/team_09_prompt_18.md) | `team_09` | Q-Soundness | proposed task to establish whether finite rank closure… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_18_B`](../round1_sessions/team_09_prompt_18.md) | `team_09` | Q-Soundness | Dual witness certificate for proposed task to establish whether… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_19_A`](../round1_sessions/team_09_prompt_19.md) | `team_09` | Q-Soundness | Dimension bound: if flat extension holds, $\dim(\mathcal{H}) =… | `23/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_19_B`](../round1_sessions/team_09_prompt_19.md) | `team_09` | Q-Soundness | Dual witness certificate for Dimension bound: if flat extension… | `5/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_20_A`](../round1_sessions/team_09_prompt_20.md) | `team_09` | Q-Soundness | Lean 4 formalization of `RankLoopClosure` structure. | `2/1 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_20_B`](../round1_sessions/team_09_prompt_20.md) | `team_09` | Q-Soundness | Dual witness certificate for Lean 4 formalization of… | `1/2 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_21_A`](../round1_sessions/team_09_prompt_21.md) | `team_09` | Q-Soundness | Lean 4 constructive theorem: `sound_global_exclusion_via_rank_loop`. | `25/2 → 0/1` | PROMISING | [follow-up](../round2_sessions/team_09_prompt_21.md) |
| [`PROP_PROMPT_T09_21_B`](../round1_sessions/team_09_prompt_21.md) | `team_09` | Q-Soundness | Dual witness certificate for Lean 4 constructive theorem… | `0/1 → 0/1` | INCREMENTAL | [follow-up](../round2_sessions/team_09_prompt_21.md) |
| [`PROP_PROMPT_T09_22_A`](../round1_sessions/team_09_prompt_22.md) | `team_09` | Q-Soundness | Lean 4 proposed derivation of the Soundness Gap… | `19/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_22_B`](../round1_sessions/team_09_prompt_22.md) | `team_09` | Q-Soundness | Dual witness certificate for Lean 4 proposed derivation of the… | `1/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_23_A`](../round1_sessions/team_09_prompt_23.md) | `team_09` | Q-Soundness | Axiom audit on rank-loop theorems: strictly `[propext, Quot.sound]`. | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_23_B`](../round1_sessions/team_09_prompt_23.md) | `team_09` | Q-Soundness | Dual witness certificate for Axiom audit on rank-loop theorems… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_24_A`](../round1_sessions/team_09_prompt_24.md) | `team_09` | Q-Soundness | Integration of rank-loop diagnostics into the unified moment… | `7/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_24_B`](../round1_sessions/team_09_prompt_24.md) | `team_09` | Q-Soundness | Dual witness certificate for Integration of rank-loop diagnostics… | `1/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_25_A`](../round1_sessions/team_09_prompt_25.md) | `team_09` | Q-Soundness | Master synthesis of the Rank-Loop Flat Extension & GNS Extraction… | `89/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T09_25_B`](../round1_sessions/team_09_prompt_25.md) | `team_09` | Q-Soundness | Dual witness certificate for Master synthesis of the Rank-Loop… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_01_A`](../round1_sessions/team_10_prompt_01.md) | `team_10` | Q-Soundness | Formulation of the fail-closed epistemic audit schema: `SDPStatus`. | `5/6 → 0/1` | PROMISING | [follow-up](../round2_sessions/team_10_prompt_01.md) |
| [`PROP_PROMPT_T10_01_B`](../round1_sessions/team_10_prompt_01.md) | `team_10` | Q-Soundness | Dual witness certificate for Formulation of the fail-closed… | `0/1 → 0/1` | INCREMENTAL | [follow-up](../round2_sessions/team_10_prompt_01.md) |
| [`PROP_PROMPT_T10_02_A`](../round1_sessions/team_10_prompt_02.md) | `team_10` | Q-Soundness | Definition of status `CERTIFIED_CANDIDATE_REFUTATION` for fixed… | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_02_B`](../round1_sessions/team_10_prompt_02.md) | `team_10` | Q-Soundness | Dual witness certificate for Definition of status… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_03_A`](../round1_sessions/team_10_prompt_03.md) | `team_10` | Q-Soundness | Definition of status `MISSING_PROOF_OBLIGATION` for global search… | `7/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_03_B`](../round1_sessions/team_10_prompt_03.md) | `team_10` | Q-Soundness | Dual witness certificate for Definition of status… | `1/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_04_A`](../round1_sessions/team_10_prompt_04.md) | `team_10` | Q-Soundness | Python implementation of `MissingProofObligationError` in… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_04_B`](../round1_sessions/team_10_prompt_04.md) | `team_10` | Q-Soundness | Dual witness certificate for Python implementation of… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_05_A`](../round1_sessions/team_10_prompt_05.md) | `team_10` | Q-Soundness | Rust implementation of `MomentSdpStatus::MissingProofObligation`… | `19/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_05_B`](../round1_sessions/team_10_prompt_05.md) | `team_10` | Q-Soundness | Dual witness certificate for Rust implementation of… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_06_A`](../round1_sessions/team_10_prompt_06.md) | `team_10` | Q-Soundness | Smale $\alpha$-theory sentry for complex polynomial systems over… | `2/1 → 1/2` | BLOCKED | [follow-up](../round2_sessions/team_10_prompt_06.md) |
| [`PROP_PROMPT_T10_06_B`](../round1_sessions/team_10_prompt_06.md) | `team_10` | Q-Soundness | Dual witness certificate for Smale $\alpha$-theory sentry for… | `1/2 → 1/2` | INCREMENTAL | [follow-up](../round2_sessions/team_10_prompt_06.md) |
| [`PROP_PROMPT_T10_07_A`](../round1_sessions/team_10_prompt_07.md) | `team_10` | Q-Soundness | Calculation of Smale invariant $\alpha(x) = \beta(x) \gamma(x)$… | `25/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_07_B`](../round1_sessions/team_10_prompt_07.md) | `team_10` | Q-Soundness | Dual witness certificate for Calculation of Smale invariant… | `7/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_08_A`](../round1_sessions/team_10_prompt_08.md) | `team_10` | Q-Soundness | proposed task to establish whether $\alpha(x) < (13 -… | `19/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_08_B`](../round1_sessions/team_10_prompt_08.md) | `team_10` | Q-Soundness | Dual witness certificate for proposed task to establish whether… | `1/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_09_A`](../round1_sessions/team_10_prompt_09.md) | `team_10` | Q-Soundness | Smale $\alpha$-theory rejection sentry: certifying that candidate… | `11/2 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_09_B`](../round1_sessions/team_10_prompt_09.md) | `team_10` | Q-Soundness | Dual witness certificate for Smale $\alpha$-theory rejection… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_10_A`](../round1_sessions/team_10_prompt_10.md) | `team_10` | Q-Soundness | Exact cyclotomic inner product verification engine over… | `7/4 → 1/4` | PROMISING | [follow-up](../round2_sessions/team_10_prompt_10.md) |
| [`PROP_PROMPT_T10_10_B`](../round1_sessions/team_10_prompt_10.md) | `team_10` | Q-Soundness | Dual witness certificate for Exact cyclotomic inner product… | `1/4 → 1/4` | INCREMENTAL | [follow-up](../round2_sessions/team_10_prompt_10.md) |
| [`PROP_PROMPT_T10_11_A`](../round1_sessions/team_10_prompt_11.md) | `team_10` | Q-Soundness | Rejection of approximate or floating-point unitary matrices by the… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_11_B`](../round1_sessions/team_10_prompt_11.md) | `team_10` | Q-Soundness | Dual witness certificate for Rejection of approximate or… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_12_A`](../round1_sessions/team_10_prompt_12.md) | `team_10` | Q-Soundness | Master CLI verifier in Python: `mub6_verify_all.py` validating… | `23/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_12_B`](../round1_sessions/team_10_prompt_12.md) | `team_10` | Q-Soundness | Dual witness certificate for Master CLI verifier in Python… | `5/12 → 5/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_13_A`](../round1_sessions/team_10_prompt_13.md) | `team_10` | Q-Soundness | Master native release binary in Rust: `omega_mub_verify_all.rs`. | `47/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_13_B`](../round1_sessions/team_10_prompt_13.md) | `team_10` | Q-Soundness | Dual witness certificate for Master native release binary in Rust… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_14_A`](../round1_sessions/team_10_prompt_14.md) | `team_10` | Q-Soundness | Bit-for-bit SHA-256 digest matching across all canonical receipts… | `25/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_14_B`](../round1_sessions/team_10_prompt_14.md) | `team_10` | Q-Soundness | Dual witness certificate for Bit-for-bit SHA-256 digest matching… | `7/12 → 7/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_15_A`](../round1_sessions/team_10_prompt_15.md) | `team_10` | Q-Soundness | Full text claim hygiene regex audit across all project… | `19/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_15_B`](../round1_sessions/team_10_prompt_15.md) | `team_10` | Q-Soundness | Dual witness certificate for Full text claim hygiene regex audit… | `1/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_16_A`](../round1_sessions/team_10_prompt_16.md) | `team_10` | Q-Soundness | Verification of zero forbidden hype terms (zero declared hype… | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_16_B`](../round1_sessions/team_10_prompt_16.md) | `team_10` | Q-Soundness | Dual witness certificate for Verification of zero forbidden hype… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_17_A`](../round1_sessions/team_10_prompt_17.md) | `team_10` | Q-Soundness | Verification of mandatory firewall line: `NOT MUB(6)=3, NOT… | `61/6 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_17_B`](../round1_sessions/team_10_prompt_17.md) | `team_10` | Q-Soundness | Dual witness certificate for Verification of mandatory firewall… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_18_A`](../round1_sessions/team_10_prompt_18.md) | `team_10` | Q-Soundness | Verification of `AuthorityEffect: None` in every emitted artifact… | `11/6 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_18_B`](../round1_sessions/team_10_prompt_18.md) | `team_10` | Q-Soundness | Dual witness certificate for Verification of `AuthorityEffect… | `1/3 → 1/3` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_19_A`](../round1_sessions/team_10_prompt_19.md) | `team_10` | Q-Soundness | Lean 4 formalization of `fail_closed_epistemic_audit_soundness`. | `23/12 → 5/12` | PROMISING | [follow-up](../round2_sessions/team_10_prompt_19.md) |
| [`PROP_PROMPT_T10_19_B`](../round1_sessions/team_10_prompt_19.md) | `team_10` | Q-Soundness | Dual witness certificate for Lean 4 formalization of… | `5/12 → 5/12` | INCREMENTAL | [follow-up](../round2_sessions/team_10_prompt_19.md) |
| [`PROP_PROMPT_T10_20_A`](../round1_sessions/team_10_prompt_20.md) | `team_10` | Q-Soundness | Lean 4 formalization of `global_exclusion_requires_bridge`. | `2/1 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_20_B`](../round1_sessions/team_10_prompt_20.md) | `team_10` | Q-Soundness | Dual witness certificate for Lean 4 formalization of… | `1/2 → 1/2` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_21_A`](../round1_sessions/team_10_prompt_21.md) | `team_10` | Q-Soundness | Full Lean 4 package build audit: `lake build` with 0 sorry and… | `25/2 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_21_B`](../round1_sessions/team_10_prompt_21.md) | `team_10` | Q-Soundness | Dual witness certificate for Full Lean 4 package build audit… | `0/1 → 0/1` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_22_A`](../round1_sessions/team_10_prompt_22.md) | `team_10` | Q-Soundness | Full Python regression suite verification: `python -m pytest… | `19/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_22_B`](../round1_sessions/team_10_prompt_22.md) | `team_10` | Q-Soundness | Dual witness certificate for Full Python regression suite… | `1/12 → 1/12` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_23_A`](../round1_sessions/team_10_prompt_23.md) | `team_10` | Q-Soundness | Full Rust test suite verification: `cargo test -p omega_mub… | `5/3 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_23_B`](../round1_sessions/team_10_prompt_23.md) | `team_10` | Q-Soundness | Dual witness certificate for Full Rust test suite verification… | `1/6 → 1/6` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_24_A`](../round1_sessions/team_10_prompt_24.md) | `team_10` | Q-Soundness | Reproducible release archive generation… | `7/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_24_B`](../round1_sessions/team_10_prompt_24.md) | `team_10` | Q-Soundness | Dual witness certificate for Reproducible release archive… | `1/4 → 1/4` | INCREMENTAL | — |
| [`PROP_PROMPT_T10_25_A`](../round1_sessions/team_10_prompt_25.md) | `team_10` | Q-Soundness | Master Grand Synthesis & Epistemic Gate Final Sign-Off. | `89/6 → 0/1` | BLOCKED | [follow-up](../round2_sessions/team_10_prompt_25.md) |
| [`PROP_PROMPT_T10_25_B`](../round1_sessions/team_10_prompt_25.md) | `team_10` | Q-Soundness | Dual witness certificate for Master Grand Synthesis & Epistemic… | `0/1 → 0/1` | INCREMENTAL | [follow-up](../round2_sessions/team_10_prompt_25.md) |
<!-- INVENTORY_END -->
