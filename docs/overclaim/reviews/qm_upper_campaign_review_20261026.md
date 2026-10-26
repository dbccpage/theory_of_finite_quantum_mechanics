# Independent source review of QM PRs 407–420

AuthorityEffect: None. Reviewer: Codex independent review agent, 26 October 2026.

Base: `4fea09ae176aae31115e38bb2b21819237055811`. Heads below were read from the live GitHub open-PR inventory and matched locally fetched Git objects. The foreign dirty checkout was not edited or checked out. This review did not approve, comment on, push, close, or merge a PR.

## Method and evidence ceiling

Read the overclaim-hunter skill and rubric, REVIEWING.md and CONTRIBUTING.md. Compared changed DAG statements and bottlenecks with new Lean declaration types, definitions, proofs, axiom-print lines, retained replay receipts, independent-check source, notes, PR bodies, and substantive derivative-prose changes. Used normalized line differences to avoid treating CRLF conversion as new mathematical prose. Compared all DAG nodes as JSON objects: each PR changes only its own target node; none changes a status.

All fourteen exact Git-blob SHA-256 hashes match the corresponding retained Lean receipt, including the after-build hash. All receipt bases match the base above. Every receipt anchor has a matching `#print axioms` line; listed axioms are restricted to propext, Classical.choice, Quot.sound. Comment-stripped new Lean source has no sorry, admit, axiom declaration, native_decide, or unsafe token. These are retained-receipt/source checks, **not a fresh Lean elaboration or kernel replay**. No Lean, Cargo, native build, cache download, provider call, or production implementation was run.

An attempted batch dynamic execution of PR Python source was rejected by auto-review because escalated execution of untrusted PR code can have process, filesystem, or network side effects. It was not retried by another execution mechanism. The PR independent scripts were consequently **not run by this reviewer**. Instead, reviewer-authored exact integer/rational/polynomial arithmetic recomputed the principal constants and finite examples without loading or executing repository source. An initial arithmetic run reached its final JSON print after all assertions but failed to serialize Fraction objects; subsequent pure-integer polynomial/count output succeeded. No mathematical mismatch was observed.

## Blocking acceptance issue common to all fourteen heads

CONTRIBUTING.md, Acceptance rule: added or changed Lean source under lean4/ needs an adjacent SHA-bound `<name>.contract.score.yaml` and the existing L4/D acceptance floor. Each of these PRs adds a new `lean4/Campaign*.lean` without that adjacent companion. This is an existing acceptance requirement, not a proposed new gate. The parent integrator owns policy-compliant contract repair and any expressly authorized existing finite-proof treatment; this review does not grant an exception or invent a score. The changed lakefile's existing scope also needs the normal owner checks.

## Per-PR statement review

The verdict “scoped pass” below means the finite statement matches the source declarations on inspection and is fenced from the larger import. It does not mean the original physical/literature target was derived, that fresh Lean compilation succeeded, or that missing contracts are accepted.

| PR | Exact head | Finite content and declaration locations | Verdict |
| --- | --- | --- | --- |
| 407 | `b19b175ed7d3d51fa21976fe5bb5cf52a792fca2` | CampaignDsContinuousTimeExpGenerator.lean:10–13, 38–40, 73–83, 103–120: four Boolean-map obstruction, two scale-4 Gaussian squares, integer Cayley identity, odd-energy injectivity, forced nilpotent corner. | Scoped pass; IMPORTED_ASSUMPTION unchanged. Continuous time, analytic exp/log, generator choice and measure remain outside. |
| 408 | `8f047b4c6b1cd0238cab2d585ff928ed6472d139` | CampaignDsQm043DecoherenceFunctional.lean:7–46 and closed witness declarations following them: integer square nonnegativity, rank-one Gram determinant identity and cleared (1,1)/2, (3,4)/5 arithmetic. | Scoped pass; IMPORTED_ASSUMPTION unchanged. No density/class-operator transport or general trace-normalization theorem supplied. |
| 409 | `ba10a13bd86a8c43da8073d04091cc3e84482ebb` | CampaignDsQm062U1Residues.lean:9–27, 34–35, 46–52, 65–99: ordinary integer 2×2 product, genuine inductive J-power/modulo-four bridge and iff identity criterion. | Scoped pass; IMPORTED_ASSUMPTION unchanged. Finite order four is not a U(1), topology, tomography or field-uniqueness derivation. |
| 410 | `f514fca8701c2524adb00509045033027a501224` | CampaignDsCptpCompletePositivity.lean:13–44, 46–60: nonnegative integer product and strict negative t·(-2) only for t>0; t=0 explicitly zero. | Scoped pass; IMPORTED_ASSUMPTION unchanged. No tensor/channel/Kraus/Choi/Stinespring identification claimed. |
| 411 | `fff7a9b2917d400bfc6c96004fbbb7ab6661415c` | CampaignDsQm204BornUniqueness.lean:8–51, 53–69: integer rotation identity and fixed (3,4) linear/quadratic/quartic inequalities. | Scoped pass; IMPORTED_ASSUMPTION unchanged. No frame-function/effect/continuity/dimension uniqueness result supplied. |
| 412 | `0526fe249a92ec3bd4615093f079b381ab2fccd4` | CampaignMajImportKitaevChain.lean:7–22: quantified natural-index separation with L≥2, 1≤j≤L−1 and two closed integer comparisons. | Scoped pass; IMPORTED_ASSUMPTION unchanged. The L−1 natural subtraction is controlled by L≥2; no physical phase/edge-mode theorem follows. |
| 413 | `2d7eb92579361cc7c59f166bdb0464111b4580ad` | CampaignFspThetaTermComplexWeight.lean:7–18, 20–60: declared quarter-turn recursion, Gaussian product bridge, charge-0/1 table and four-entry positive-real test. | Scoped pass; IMPORTED_ASSUMPTION unchanged. Real angles, exponentials, plaquette charge and sampler remain excluded. |
| 414 | `7de23a2debb553c303612a45f2be1f1586a00e05` | CampaignMub6WeylHeisenbergD6.lean:16–32, 399–410, 493–500, 600–731, 812–860: cyclotomic integer-pair table, chosen clock convention ZX=wXZ, actual matrix-power entry bridge and trace orthogonality for Fin 6 indices. | Scoped mathematical pass; IMPORTED_ASSUMPTION unchanged. Checker-header correction below is needed. No complex exponential identification or MUB count follows. |
| 415 | `f9f994b4b3d3770b881ddf3531923553cdac50db` | CampaignMub6FiniteCornerReduction.lean:9–21, 98–117: ordinary 3×3 integer product/transpose, two-sided inverse, one D formula, cross-zero and zero-D refusal. | Scoped pass; IMPORTED_ASSUMPTION unchanged. No complex Hadamard classification or universal reconstruction equivalence claimed. |
| 416 | `eb1369a8b7b497b4a4d6d318861771886e3c0113` | CampaignQcvImportThresholdTheorem.lean:6–24: definition t(n)=2n², four closed values, three-step orbit and two scalar products. | Scoped pass; IMPORTED_ASSUMPTION unchanged. No code, noise model, physical constant or threshold theorem supplied. |
| 417 | `001ec7a8748d4dee06e93a0473ceaafb6530ed37` | CampaignQcvImportNoisyReversibleLimits.lean:6–54: three supplied natural recursions and four closed rows. | Scoped pass; IMPORTED_ASSUMPTION unchanged. No trace norm/depolarizing channel or asymptotic noisy-computation theorem supplied. |
| 418 | `d2ebdb92248a1202f162087cd567fb176f031171` | CampaignAuthRiceTheoremImport.lean:6–43: six behavior entries on Fin 3×Fin 2 and six Boolean labels. | Scoped pass; IMPORTED_ASSUMPTION unchanged. No Partrec.Code semantic property or Rice theorem instantiated. |
| 419 | `d59f05a982ae41ab545f681398c49655d08e5ac1` | CampaignOpsAxis1WellfoundedAdmission.lean:6–43: separately declared predecessor/admission definitions, three recurrence equations for arbitrary base bits, two closed assignments. | Scoped pass; IMPORTED_ASSUMPTION unchanged. Definitions encode this chain rather than deriving general well-foundedness; Genesis result remains explicitly not rerun. |
| 420 | `f2ec14dcdd377895195d32587926ff8f77dd2c9b` | CampaignTfq0183FourModeDisk.lean:7–25: constants 4,4,1 and five arithmetic declarations, not a matrix-rank proof. | Scoped mathematical pass; OPEN unchanged. Checker-header correction below is needed. No device, hardware, physical Majorana or larger-grid theorem supplied. |

Lean paths in the table are under lean4/. All independent derivation notes retain the required first-line AI-drafted/awaiting-human-review marker; no human-review claim was introduced.

## Two actionable checker-claim corrections

### PR 414: no independent polynomial-matrix oracle

`checks/independent/mub6-weyl-heisenberg-d6.py:1` calls the table “checked again by polynomial remainder.” At lines 123 and 137, the checker compares a computed integer pair with an expected integer pair, then maps those same pairs through `sym_of`. Once the pair equality passes, the polynomial images necessarily agree. Only lines 95–98 are an additional scalar polynomial-remainder sanity check. The SymPy path does not independently construct or multiply polynomial matrices and cannot catch a shared pair-operation defect through those redundant image comparisons.

Lowest-cost correction: replace the header with “Integer-pair clock and shift at dimension 6, with polynomial-remainder scalar sanity checks.” Keep actual arithmetic checks intact. Alternatively add an actual independent polynomial-matrix path, but that is a larger change and not required to preserve the correctly scoped finite statement.

### PR 420: synthetic fixtures are not production verification

`checks/independent/tfq-0183.py:2–18` claims verification of named Rust and Python production functions. No such implementation is imported, executed, read, bound by a digest, or compared with the synthetic outputs. The source independently builds finite grids and a skew matrix; those checks have their stated finite fixture value, not implementation conformance. Lines 237–240 only test that the chosen recurrence's masked state is in the u64 range; they do not test Bernoulli sampling. Lines 242–247 construct trials as the sum of supplied counts, so exact fraction summation is an arithmetic identity, not observed conservation of real GF2 schedule statuses. No `authority_effect` assertion is made for those sampler fixtures.

Lowest-cost correction: explicitly describe separately constructed finite fixtures and state that the script does not execute or verify the named Rust/Python production implementations or sampler outcomes. Keep the actual finite assertions; do not call them production conformance. The added count-triple note already distinguishes computed matrix ranks from what the new Lean module proves.

## Independently recomputed numbers

| PR | Reviewer arithmetic result |
| --- | --- |
| 407 | Four Boolean maps have no toggle square root; scale-4 swap square matches; Cayley identity on integers −100…100; forced candidate corner 2; source loop count 679. |
| 408 | Half-pair square-sum 1/2; (3/5,4/5) square-sum 1 and global square 49/25; source count 61+169·20+18=3459. |
| 409 | J powers I,J,−I,−J,I; source count 17+40·6=257. |
| 410 | Pairing −2, norm square 2, zero scale 0; source count 82+162+49+294+1+34+24+2=648. |
| 411 | Squares 25, fourth powers 337, splits 3033≠2025 and 75≠63; rotation witness −7,24 gives 49+576=625. Additional integer rotation box −5…5 had no mismatch. |
| 412 | L=2 witness 2,3 against endpoints 1,4; inside 1<4 and outside 9<4 false; original L≤12 box has 66 pairs. Larger reviewer L≤100 index box had no mismatch. |
| 413 | Quarter pairs (1,0),(0,−1),(−1,0),(0,1),(1,0); among indices 0…3 only 0 is positive-real at charge 1. |
| 414 | Reviewer-authored polynomial coefficient reduction modulo w²−w+1: 36 operators, 1296 ordered sparse-column inner products, zero mismatches; opposite commutation differs in all six nonzero positions. Root powers w²=(-1,1), w³=(-1,0), w⁶=(1,0). Repetitive mAdj/mMul/op fields independently matched all 36 intended coordinate assignments. |
| 415 | Rational elimination gives the stated inverse; -C·inverse(B)^T gives rows (1,−1,0),(−1,1,−1),(−1,0,0); cross sum zero; zero-D cross has 3 nonzero entries. |
| 416 | Orbit 1,2,8,128; scale products 0 and 2; 9 source rows. |
| 417 | Rows (1,1),(3,4),(9,16),(27,64); three strict inequalities. |
| 418 | Behaviors (0,1),(0,1),(0,0); identity bit true twice, code-zero bit once; 12 source rows. |
| 419 | Eight base assignments; all-false admits none and seed-at-zero admits all. `rows=15` matches the 15 Lean anchors, but is not the number of Python conditions: the source actually calls its predicate 36 times. |
| 420 | 4−4+1=1, (4−1)−(4−1)=0, 1+1 even, 4·2=8 even, 4≠2; total source condition count 13+27·7+(21+73+157)+25+4=482. No synthetic sampler result promoted to production evidence. |

## Result

Fourteen scoped finite statements matched source types on inspection; thirteen imported labels and one OPEN label are preserved. No status promotion recommended. Two checker-description corrections are actionable. All fourteen new Lean additions still require existing acceptance-contract handling by the parent integrator. No fresh Lean, native or full-suite success is asserted; original independent scripts were not executed by this reviewer.


