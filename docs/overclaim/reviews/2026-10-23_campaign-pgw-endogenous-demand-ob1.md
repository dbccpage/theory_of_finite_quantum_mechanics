# Review of the declared Genesis demand-policy extension

AuthorityEffect: None. AI self-review, awaiting human review.

Scope: PGW-ENDOGENOUS-DEMAND-OB1 on main 4a1e551210459ca8b410fada1e8eddb75e7b052c.
Method: inspect all declaration types and executable syntax, source predicates,
the independent checker and every finite number. Not rebuilt by this review;
the completed target receipt supplies compilation evidence.

Result: NARROWED. The declared extended language has an internal next-demand
instruction. The sealed Alpha harness is unchanged and the node stays OPEN.

All following anchors refer to lean4/CampaignGenesisDemandPolicy.lean.

| Atomic claim | Declaration and line | Verdict |
|---|---|---|
| Every source well-formed context is enumerated, without an arity cutoff | `mem_contexts`, :32; `mem_tuples`, :19 | FULL |
| Finite test equals actual source collapse | `collapseTest_correct`, :42 | FULL |
| Agenda is exactly the fresh ordered collapsed pairs | `mem_agenda`, :59 | FULL under the declared policy |
| Every chosen target is admitted, ordered, collapsed and fresh | `next_sound`, :76 | FULL |
| No target iff all collapsed pairs are already requirements | `next_none_iff`, :85 | FULL for separateAll |
| Generated demand is exactly a source impose event | `seek_is_recorded_source_step`, :105; `instruction_records_demand`, :157 | FULL |
| Request grows once, preserves observations and cannot immediately repeat | `seek_grows_one`, :111; `seek_preserves_observations`, :115; `no_immediate_repeat`, :123 | FULL |
| Policy follows from the source alone | `policy_is_not_forced`, :130 | REFUSED by the explicit same-regime control |
| The program needs no host target | `no_host_target_in_program`, :164 | FULL for the explicit program; syntax/interpreter are at :137-152 |
| Infinite autonomous continuation, responder or Alpha refinement | not proved | NOT CLAIMED |

Numbers recomputed: the checker evaluates all 8,424 declared regimes and all
6,517 fresh SEEK steps, reaching agenda saturation in each case. Its SymPy
census includes every initial requirement subset. Three semantic mutants each
produce an incorrect concrete pair. The successful receipt parses seventeen
terminal audits; normal and optimized checker output are identical.

Corrections and boundaries: saturation means requests recorded, not demands
satisfied. Existing reading-L requirements are not called fresh. The admitted
policy is an explicit extension and the lexicographic choice is not claimed
invariant under every writing. No token glyph is inspected by this model.

What the scanner cannot decide: whether this is the desired internal policy,
and whether Alpha's actual search/license implementation is a faithful host.
The original goal-free demand obligation is not silently marked proved.

Final gates: all prescribed checks and 24 tests pass. Strict scanner HIGH=0, MEDIUM=0, LOW=3; the LOW findings are inherited tensor metadata. The executed TFQ-0084 prompt delta and unchanged malformed HilbertLiftOperators companion remain additional diagnostic failures. No status is raised or scanner exception introduced.
