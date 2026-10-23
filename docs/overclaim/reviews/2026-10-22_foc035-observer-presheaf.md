# Review of branch foc035-observer-presheaf (FOC-035 import)

Scope: branch `foc035-observer-presheaf`, base `origin/main` `3924d378f`. Reviewed against the statements as they stand at the branch head. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound. The change adds 33 nodes in one new stage, OBSERVER_PRESHEAF, and changes no existing node's status or statement.

Method: read `.claude/skills/overclaim-hunter/SKILL.md` and `rubric.md`; ran `overclaim_scan.py --changed-since origin/main --strict`; read the 33 node statements against the claim ledger and the note (`sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/`) line by line; read `lean4/LggrFiniteResults.lean` in full; read the proofs of Propositions B3, B4, B5 and Lemma A2 in the note; recomputed every number with `checks/independent/foc035_observer_presheaf.py` (exact `Fraction` arithmetic, no repository imports) and with pytest. Not rebuilt: Lean (the module is on main; this branch adds no Lean and did not elaborate it) and cargo (no Rust was built or run). No LLM or provider call was made. External identifiers were checked against the arXiv API and the Crossref record.

Result: 33 nodes reviewed. PROVED_LEAN 2 nodes: 2 NARROWED to the Lean statement, kept as stated by the node, with no replay receipt (see below). PROVED_PROSE 7 nodes: the note's prose proof was read and no gap was found; these are not machine-checked. COMPUTATIONALLY_CHECKED 7 nodes: 0 OVERCLAIM as worded. No node was raised above the evidence; four pieces of text were changed by this review (next section).

## Corrections to the branch's own text

- OPS-TEST-482-REPAIR: the first draft imported the repaired Test 482 as `code/python/tests/test_vorobev_gyo_acyclicity.py` and called the node computed by that test. As one test with fixed inputs and no edge-case handling it scores L3 under `SCORING.md`, below the L4 floor set for code in this change, so the file was removed. The node now states the instances the test checks, which `checks/independent/foc035_observer_presheaf.py` recomputes (two rational tables, the GYO reduction, the exhaustion of eight assignments), and says the source test is not imported.
- OPS-REGRESS-COROLLARY: the route text said "as derived in the note"; the scanner (R6) read it as calling an imported and a conditional node derived. Reworded to "the note's argument ... conditional on (iii)".
- Fragment text used the word "proves" in one source-status sentence; the validator's forbidden list refused it. Reworded to "gives a direct proof".
- Test counts: the note says the Python gate has 13 tests and the ledger says 14; running the imported file gives 15 tests and 33 subtests, and the node says 15. The note says the Rust test file has 15 tests; the file defines 23 `#[test]` functions. The node does not state the Rust count.
- The ledger names the Lean file `lean4/quantum_mechanics/LggrFiniteResults.lean`; in this repository it is `lean4/LggrFiniteResults.lean` (the older route `IMPL-R-LGGR-FINITE-RESULTS` still cites the old path). The nodes cite the path that exists.
- The ledger header says Lean 4.34.0; this repository pins 4.35.0. The two Lean nodes say the module was not rebuilt and give the ledger's account as the ledger's.
- The note's reference list gives "Contextual fraction as a measure of contextuality"; the arXiv title is "The contextual fraction as a measure of contextuality". Not used in any node statement.

## Per-node table

| Node | Declarations or checks that discharge it | Verdict | Reason |
|---|---|---|---|
| OPS-PUSHFORWARD-FUNCTOR-LEAN | `push_id`, `push_comp`, `mass_push`, `weightAt_push` (`lean4/LggrFiniteResults.lean:17-39`) | NARROWED, kept | Statement is the four Lean types for natural-number weighted lists. The reading of marginalisation as pushforward, rational weights and the context poset are said to be outside. No replay receipt: Lean not rebuilt. |
| OPS-PARITY-HOLONOMY-LEAN | `section_exists_iff_holonomy_zero` (`:83`), `no_joint_measure_when_holonomy_one` (`:141`) | NARROWED, kept | Statement is the two Lean types. Arc-cover, NCF and nerve clauses are said to be outside. No replay receipt: Lean not rebuilt. |
| OPS-NCF-LHV-EQUIVALENCE | note Prop. B3(1), proof read | prose, no gap found | Feasibility of sum lambda = 1 with A lambda <= e forces equality because each context of e sums to 1. |
| OPS-STRONG-CONTEXTUALITY-NCF-ZERO | note Prop. B3(3), proof read | prose, no gap found | Both directions are in the proof. |
| OPS-MAXIMAL-COVER-DESCENT | note Prop. B4(1), proof read | prose, no gap found | Set-level statement only; the Rust classifier reading is said not to be checked. |
| OPS-NGE-NOT-CONTEXTUALITY | rows B6 and B7 | prose | Follows from the two nodes it names. |
| OPS-CECH-COBOUNDARY | note Prop. B5, proof read | prose, no gap found | Rational case rests on the prose proof; Lean covers natural weights only (said in the route). |
| OPS-ZERO-COCYCLE-BLIND | note section 2.4 | prose | Stated as a statement about the test, as in the ledger. |
| OPS-UNDERDETERMINATION | note Lemma A2 and its table | prose | Does not claim non-existence of a function; norm and Term rows are said to be arithmetic. |
| OPS-NOISY-PR-NCF, OPS-ARC-COVER-NGE-WITNESS, OPS-PARITY-CYCLE-DESCENT-NCF, OPS-VOROBEV-PATH-INSTANCE, OPS-TEST-482-REPAIR | `checks/independent/foc035_observer_presheaf.py`, run by `dag/test_foc035_observer_presheaf.py` | matched on the instances | Finite instances only; each node says so. Not the Rust tests named in the ledger. |
| OPS-THREE-ROLE-GATE, OPS-SELF-CERTIFICATION-PACKET | `code/python/tests/test_three_role_gate.py` (15 tests, 33 subtests) | matched | One fixture; the node says the gate is not linked to the Rust evaluator. |
| OPS-OBSERVER-DECLARATION-REFUSAL, OPS-RUST-RECEIPTS-AND-LIMITS | Rust tests of the source repository | CONDITIONAL, not run here | `omega_solvers` is external; `cargo metadata --no-deps` lists no such package; source tests not imported. |
| OPS-AXIS3-RELABELING, OPS-REGRESS-COROLLARY | note section 3.1 | CONDITIONAL | Conditional on (iii), and on NS-14 and CL-13 cited and not re-run. |
| OPS-NO-SIGNALLING-SIGNED-SECTION, OPS-Z2-WITNESS-FALSE-NEGATIVES, OPS-VOROBEV-THEOREM, OPS-AXIS1-WELLFOUNDED-ADMISSION, OPS-AXIS2-META-CARRIER | none | IMPORTED_ASSUMPTION | Cited; three have external identifiers checked against arXiv and Crossref. |
| OPS-REFUTED-AXIS3-WIDE | countermodel recomputed in the independent script | matched | Shows V((a)) = true and V(sigma((a))) = false with (i) and (ii) holding. |
| OPS-REFUTED-NB9, OPS-REFUTED-EARLIER-GATE, OPS-REFUTED-EARLIER-RUST | ledger rows C4, N1, N8, N4 to N7 | recorded | Earlier heads are not in this repository; only the count-rule miss and the 2^64 wrap are recomputed. |
| OPS-OBSERVER-TUPLE, OPS-AP-CARD-PROPOSAL, OPS-PR1050-ABSENCE, OPS-LEAN-GAP | none | definition, source records, open | N2 is a SOURCE_RECORD, not REFUTED: it records an absence in another repository. |

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| PR box defect | 2 | exact simplex, primal and dual certificate re-verified | match |
| PR box on the acyclic sub-cover {ab, ab'} | defect 0 | same | match |
| PR box in the no-signalling polytope | defect 0 | all overlap marginals agree | match |
| norm row | 2 x 2 = 4 | arithmetic | match |
| PR box | NCF 0, |G| = 0 | LP and enumeration of 16 assignments | match |
| noisy PR | NCF 1/2 at 1/4, 1 at 1/2 (2 lam), |G| = 16 at both, defect 0 at 1/2, positive at 1/4 | LP and enumeration | match |
| mixture of (0,0,0,0), (1,0,0,1) | NCF 1, |G| = 2 | LP and enumeration | match |
| maximal cover | 0 and 16 families, 16 with one gluing | enumeration | match |
| arc cover | 4 families, 2 with one gluing, 2 with none | enumeration | match |
| parity cycles | 8 + 16 + 32 = 56 cases agree | enumeration, LP | match |
| Bell nerve | 4 edges, no triple; Phi_1 = 2 | edge count; value 2 at alpha = 0 and dual witness of sup norm 1 annihilating delta0 | match |
| 3-context nerve | delta1 delta0 alpha = 0; delta1 beta = [1, 0] | Fraction arithmetic | match |
| signed section of the PR box | sum 1, negative entry | Gauss-Jordan over Fractions, all 16 equations | match |
| path cover | product formula, 3 marginals, NCF 1 | Fractions, LP | match |
| Test 482 tables | mass 1, both tables reproduced | Fractions | match |
| ceilings | 2^20, 2^22; 2^64 and 2^21 above 2^20; 1024 and 20 x 1024 inside | integer arithmetic; `MAX_GLOBAL_ASSIGNMENTS = 1 << 20` and `MAX_LP_ENTRIES = 1 << 22` read in `mod.rs` | match |
| count-rule miss | 2 identifiers and 2 principals in both cases | fixture packets read | match |
| gate tests | 15 tests, 33 subtests, 17 fixture cases | pytest run; fixture length | match (note says 13, ledger 14) |
| Rust test functions in the source file | 23 | `#[test]` count by regex | note says 15; not used in a node |
| ledger rows | 40, all mapped | regex over the ledger table; `dag/test_foc035_observer_presheaf.py` | match |
| nodes, routes, records | 33, 37, 33; TFQ-2500 to TFQ-2532 | fragment | match |
| mutation campaign of the gate | killed 191, survived 63, R = 191/254 = 0.752 | `evidence/quality/foc035_observer_presheaf/` | recorded, no exclusions |

## Scanner output

`overclaim_scan.py --changed-since origin/main --strict` exits 0 with 16 baseline entries added by this branch: R9 for the 16 new nodes whose status is PROVED_PROSE, COMPUTATIONALLY_CHECKED or PROVED_LEAN. R9 asks for a resolving Lean reference with a new replay receipt, or for a per-node `checks/independent/<id>.py`. None applies to prose-proved nodes (no Lean exists), to nodes sharing one independent script, or to nodes restating a module that is already on main and was not rebuilt. Each entry carries its reason. The two PROVED_LEAN entries are the ones a reviewer may prefer to lower: the evidence map flags both (`proved_lean_below_e3`), and a replay of `lean4/LggrFiniteResults.lean` under Lean 4.35.0 would remove the flag.

The earlier R6 findings (two) were fixed by rewording, not baselined. LOW findings (R5) were not decided one by one; the numbers of the nodes were recomputed above.

What the scanner could not decide: whether the note's prose proofs are right beyond the reading above; whether the ledger's account of the Rust tests holds (they were not run); whether the cited Genesis and Argon results hold (cited by name only); the correctness of the AST mutation operators used for the gate's score.
