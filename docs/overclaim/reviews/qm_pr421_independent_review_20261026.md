# Independent review: QM PR 421

AuthorityEffect: None. Codex source review, not independent human mathematical review. Date: 26 October 2026.

PR: [QM #421](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/pull/421).

Exact reviewed head: `72b3595fd6f4aca9c22aa8508074b7f860ce30cc`.
Exact base: `4fea09ae176aae31115e38bb2b21819237055811`.
Node: `FSP-PACHNER-INVARIANCE-CLAIM`, record `TFQ-1214`.

## Result

**Source-fidelity pass for the explicitly revised finite-group statement.** No mathematical blocker was found in the 417-line proof, the filling definitions, or the finite-exterior interface. Unlike the earlier fixed-table campaign examples, this proof is genuinely parameterized by an arbitrary group and a finite carrier; it does not generalize from the C1–C5/S3 computations. The narrowed statement alone changes OPEN to PROVED_LEAN. No other node changes its status.

Acceptance remains conditional on verifying the actual human authorization for this exact source exception. The PR adds a record quoting “Approve this exact pin,” but that record and the PR body are source material, not independent evidence of human authority in this review task. The parent integrator should verify the originating human reply before relying on the policy addition. This reviewer grants no exception or merge authority.

No PR source, checker, repository validation script, Lean or native build was executed by this reviewer. No source files, checkout, branch, Git objects, comments or PR state were changed. Only this external review artifact was written. The existing overclaim rubric, REVIEWING and CONTRIBUTING policies were applied. Retained compilation/audit receipts are checked as retained evidence, not described as a fresh kernel replay.

## Revised statement and theorem correspondence

The node states:

> For every finite group G, the untwisted flat-connection count on the canonical 4D 1-5, 2-4 and 3-3 Pachner pairs, divided by |G| to the number of interior vertices, agrees for every fixed flat common boundary. The normalized total counts also agree for every finite compatible exterior family represented by dependent pairs, with the same outside-vertex count.

All Lean locations below are in `lean4/CampaignFiniteGroupPachner.lean` at the exact reviewed head.

| Atomic claim | Matching source | Review |
| --- | --- | --- |
| Canonical complementary facets on six vertices | `facetFace` 28–29, `localFacets` 322–324, `face_is_in_a_facet` 326–328, five-vertex facets 330–333, facet counts 335–338 | The complexes are explicitly specified as the complementary omitted-vertex collections of the boundary of a 5-simplex. This is not an arbitrary triangulation API. |
| The common edge/triangle skeletons are those used by the field types | Predicate definitions 19–26; geometry identities 38–83, especially boundary identities 61–74 | Finite `decide` is appropriate here because the advertised combinatorial carriers really are `Fin 6`. No universal-group conclusion is obtained from finite geometry alone. |
| A connection is an actual oriented group-valued edge assignment, not a potential entered as the definition of a filling count | `Connection` 87–90; `FlatOn` 94–95; `Coloring` 97–98 | Diagonal/reversal constraints and all declared triangle equations are explicit. Nonedges carry identity placeholders, eliminating rather than adding free labels. |
| The result applies to every group, including noncommutative ones | `variable (G : Type*) [Group G]` 85; local cardinality/amplitude theorems add `[Fintype G]` | Cancellation/associativity, not commutativity, is used. Group nonemptiness supplies a nonzero order. |
| Every 1–5 flat boundary has one old filling and exactly \|G\| new fillings | `SelfFillings` 179–180, `OneNew` 182–183; uniqueness 209–219; explicit inverse maps 227–257; cardinalities 295–301 | A genuine equivalence between the new filling type and G is proved, with both inverse laws. The old count is not merely assumed. |
| Every 2–4 flat boundary extends uniquely | `TwoNew` 184–185; root extension 259–263, uniqueness 265–271; count 303–304 | Root 2 meets every boundary edge. The absent 01 edge is computed by flatness rather than silently fixed to the identity. |
| Every 3–3 common flat boundary extends uniquely to both sides | `boundary_has_triangle_cone` 81–83; cancellation 127–140; filling definitions/uniqueness 273–288; counts 306–310 | The common boundary already forces both missing triangle equations. All edges match, so no additional free edge is counted. |
| The normalization is exactly one group-order factor per interior vertex | `interiorVertices` 317–319; counts 340–345; `localAmplitude` 347–349; nonzero order 351–352 | Interior counts are 0/1, 0/0, 0/0. Counts are rational and the denominator is genuinely nonzero. This is a normalized connection count, not unit weight per gauge orbit. |
| The three normalized local amplitudes agree | `pachner_one_five` 354–357, `pachner_two_four` 359–362, `pachner_three_three` 364–367 | These theorem types are the advertised three local equalities for arbitrary fixed flat boundary values. |
| Counts agree after the specified finite compatible exterior interface | `stateSum` 369–374; `glued_one_five` 376–385, `glued_two_four` 387–393, `glued_three_three` 395–401 | Arbitrary finite X and arbitrary maps to the respective flat boundary type are quantified. Sigma-type cardinality sums filling multiplicities. The same supplied outsideVertices parameter is used on both sides; it is not a theorem relating a separately formalized global triangulation to this interface. |
| Nonflat boundary data cannot be hidden by a flat bulk extension | `flat_boundary_of_matching` 144–155, `nonflat_boundary_has_no_extension` 157–164 | This is an actual restriction theorem with explicit face/matching hypotheses. The main filling theorems themselves correctly quantify only over flat boundary types. |

The note explicitly excludes a general triangulation/gluing-equivalence library and a theorem relating arbitrary PL-homeomorphic triangulations by move sequences (`dag/derivations/independent/fsp-pachner-invariance-claim.md:137–141`). Regge, twisted/Crane–Yetter, fermion-sign, continuum and physical claims remain outside the revised statement. No fixed-case-vs-general-group overclaim was found.

## Retained-source and receipt integrity

Verified against exact Git blobs:

| Artifact | SHA-256 |
| --- | --- |
| Lean source | `e8b2c28cf6e0a0536ba15941742f07d59dc2adcbae86bdfa7311678f6c00cdca` |
| Replay receipt | `cea239c2894d9939b604a3859a3028ce92e70c901db51d7a1a778150da74a1af` |
| Independent Python checker | `ec9f5bf0c4bdf2d8b829f23871f376b08c3f329746aaadfde6cb8293cd0b38b5` |
| Approval proposal | `25bb9d5e041c3bcd33ef99a723aa5545401481312f791bd086b7d1d34b08e1a3` |

The receipt binds the exact Lean source before and after the retained build and binds the independent checker source. Its base matches the reviewed base. It records Lean 4.35.0, commit eb6cafb7290e8bd5f2937522d8d804f58f02bafc, and Mathlib source 56a005855ea17e0b0958f73ec801ae140b0a1679. The recorded build scope is an exact-source minimal package; the full repository Lean workspace was **not** built.

Comment-stripped new source contains no sorry, admit, axiom declaration, native_decide, or unsafe token. Its 99 explicit named definitions, theorems, abbreviations, structure and named instances match all 99 entries in the retained full audit importer; no explicit name is omitted. The importer input SHA-256 matches its retained contents, and its output mentions all 99 declarations. The receipt's 99 axiom lists contain only propext, Classical.choice and Quot.sound. The source itself prints 14 principal theorem/equivalence audits, while the retained separate importer covers the other explicit declarations. No claim that all 99 source audit commands are literally present in the proof file is made.

All three new/current companions' artifact hashes match the source bytes. Their referenced receipt/note/review evidence hashes match. Every stored contract/scoring-history raw UTF-8 digest matches its stored SHA-256.

## Independent checker inspection and reviewer arithmetic

`checks/independent/fsp-pachner-invariance-claim.py` uses only standard-library imports and imports no repository module. Its table validator checks closure, unit, inverses and associativity (36–46). S3 is built by permutation composition and an explicit noncommutativity witness is required (54–60, 206–207). Edge constraints are propagated by solving g_ab g_bc = g_ac in the correct noncommutative order (96–109). Each branch copies its current assignments (113–117); triangle failures are refused. The independent full Cartesian C2 set comparison checks both local sides (124–130, 167–169). This is a meaningful second enumeration route, not a polynomial image of an already accepted result.

The checker reconstructs faces from facets rather than hard-coding final counts. It requires every and only flat boundary value to extend on both sides; checks fiber cardinalities and normalization; and tests nonconstant finite exterior multiplicities. Negative controls explicitly cover a nonflat boundary, omitted normalization, falsely fixed new edge, and omitted interior flatness. Failures use a runtime exception rather than removable Python assertions. Its negative controls have the limited meaning of detecting those deliberately damaged mathematical models; they are not a claim of exhaustive program mutation coverage.

The original checker was **not run by this reviewer**. Instead, reviewer-authored GF(2) bit-row elimination independently checked geometry, all C2 solution-space dimensions and restriction-map image/fiber dimensions. This is a different route from the PR's edge-CSP and Cartesian enumeration:

| Move | Boundary vertices/tetrahedra | Interior counts | C2 left: edges, triangles, rank, states | C2 right: edges, triangles, rank, states | Flat boundaries; fiber counts |
| --- | --- | --- | --- | --- | --- |
| 1–5 | 5 / 5 | 0 / 1 | 10,10,6,16 | 15,20,10,32 | 16; 1 / 2 |
| 2–4 | 6 / 8 | 0 / 0 | 14,16,9,32 | 15,20,10,32 | 32; 1 / 1 |
| 3–3 | 6 / 9 | 0 / 0 | 15,19,10,32 | 15,19,10,32 | 32; 1 / 1 |

The restriction image dimension equals the flat-boundary space dimension in each case, so this arithmetic independently checks extension of every C2 flat boundary, not just total counts. The normalized fiber amplitudes are exactly1. Separately recomputed integer powers for group orders1…6 give the claimed 1–5 total pairs [1,1], [16,32], [81,243], [256,1024], [625,3125], [1296,7776], and 2–4/3–3 boundary counts1,32,243,1024,3125,7776. Omitting interior flatness leaves five free new C2 edge labels: 2^5=32 fillings per boundary and normalized amplitude16. These arithmetic checks do not replace the general noncommutative Lean theorem or execute the PR's S3 checker.

## Score, policy and integration review

- Proof companion: L3D, complete, gates C/C/C/D/C. This is an honest below-L4 research finite-group theorem assessment; the exception category is finite_proof_example. The source is not renamed L4 or presented as a global production framework. The D-level verification ceiling acknowledges incomplete exhaustive mutation coverage and full-workspace build. No concrete E defect was identified in this source review; that is not a fresh complete assessment.
- Checker companion: L3D with the same gate vector and exact current bytes; it is outside the governed code/Lean population. No score is inferred solely from a passing hash.
- Lake registry companion: L1D with the existing build_registration category rebound to exact registry hash `be27b3748c704f49fa471f233ee7dc59a7e0b4eec5ee08101be70ca56278573e`.
- Policy diff versus the reviewed base changes only support_exceptions: adds this one proof path/digest and updates the registry digest. It preserves the other 48 proof pins, default floor, exclusions, discovery and enforcement. No category-wide exception or grade-E/incomplete allowance is introduced.
- The PR's approval record claims a human approval for this exact pin. As above, verify that human reply independently; another artifact saying “approved” is not sufficient authority by itself.
- Registry adds one independent, non-default CampaignFiniteGroupPachner library and removes no existing library/root versus its base. When integrating after the earlier campaign batches, **union** the new root with those already merged; do not replace the current registry or policy with this older-base file. Recompute the combined registry digest/companion and correct documentation pin counts after integration.
- Exactly one DAG node changes and rises OPEN→PROVED_LEAN. Its sole owning route changes GAP_NO_DERIVATION→DERIVED_LEAN and replaces FSP-REGGE-DEFICIT-ACTION with the supplied-group premise DFM-GROUP-CONNECTION. Regge is retained only as see_also; the old parent/child link is removed from the generated record. This is a meaningful premise change and is explicitly disclosed, not an inference that the Regge action became Pachner invariant.
- The dated pre-approval proposal and short overclaim review retain pending-exception language. The new approval record explicitly identifies them as preserved pre-approval evidence rather than silently rewriting them. This is not a current mathematical contradiction; nevertheless, the human authorization itself still needs the independent check above.

## Recommendation

The narrowed mathematical statement is supported by the inspected theorem types and exact retained-source evidence. No further statement narrowing is proposed. After independently confirming the exact human pin approval, normal current-head contract/governance/CI checks and careful registry/policy union are the remaining integration requirements. This review does not establish a fresh kernel replay, the reported 191 regressions, a full Lean workspace build, general PL invariance, or independent human review.
