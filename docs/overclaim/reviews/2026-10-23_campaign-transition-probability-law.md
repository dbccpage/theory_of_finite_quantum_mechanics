# Review of campaign transition-probability law

Scope: campaign/l1-imp-transition-probability-law, base
3924d378ff1de685948bf2b419dc63a5a9560881. AuthorityEffect: None.
This is an AI author self-review; it does not substitute for the required named
human review of the derivation note.

Method: read the complete changed node, derivation note, all new Lean declarations,
their imported Wigner definitions/theorems, current replay receipts, independent
checker, generated-view diff and scored companions. Lean was **not rebuilt by
this review**: it relies on the separately recorded campaign build and fresh
kernel replay, whose source digest was rechecked. No cargo build was run.
All explicitly named source declarations have axiom reports containing only subsets of
propext, Classical.choice and Quot.sound. The independent checker is a separate
arithmetic implementation; its finite sample is not used as a universal proof.

Result: **0 nodes FULL, 1 NARROWED, 0 OVERCLAIM**. No node was raised.
The full physical law remains IMPORTED_ASSUMPTION.

Corrections to the PR's own text: none proposed after this review. The submitted
statement already distinguishes the supplied law, conditional sufficient routes
and the exact countermodels. No baseline entries are added.

## Per-node table

All new declaration locations below are in lean4/CampaignTransitionProbability.lean.

| Atomic claim | Declaration and line | Verdict and scope |
|---|---|---|
| Primitive difference implies the physical probability-preservation law | Not proved | NOT PROVED; the target remains imported |
| A matrix lift, finite basis/balanced orthogonality calibration and one nonzero anchor suffice | linear_calibration_tpPreserving:71; calibration_similarity:59 | FULL conditional theorem for arbitrary positive dimension; linear structure is explicitly supplied |
| Finite fixed-frame basis/real/imaginary probe statistics in every nonzero state suffice | tomography_sameRay:314; tomography_tpPreserving:365 | FULL conditional theorem; these premises actually fix every ray and are not a strictly weaker dynamics law |
| The derived premise feeds the existing exact Wigner result | linear_calibration_wigner:90 | FULL conditional composition; similarity rather than guaranteed unitary normalization |
| Born formula, reversibility, norm and basis statistics, report-swap covariance, orthogonality in both directions and finite calibration are jointly insufficient | insufficient_operational_package:290; countermodelRayEquiv:268 | FULL counterexample on the entire dimension-two ray quotient |
| Adding real pair probes does not repair that package | conditionalConjugation_realProbes:450; imaginary_probe_probabilities:457 | FULL; the imaginary probe detects the failure |
| Linear reversible subspace-lattice order automorphisms need not preserve probabilities | insufficient_lattice_package:488; stretchLattice:398; stretchRayEquiv:427 | FULL on dimension two; no claim about orthocomplements or affine positive effects |
| Nonvanishing suffices in dimension one | oneSector_tpPreserving:512 | FULL single-ray boundary |
| The two countermodels establish independence from every repository primitive | Not proved or claimed | NOT PROVED; only the defined candidate packages are refuted |

The sufficient hypotheses are definitions rather than synonyms for TpPreserving:
LinearLift supplies a single matrix on all vectors; OrthogonalCalibration is a
finite family of zero-inner-product tests; NonzeroAnchor is one nonzero image;
TomographicStatistics uses only a fixed finite effect frame, albeit in all
states. BornRule supplies a static readout formula. ReportSwapCovariant is
covariance under a named permutation, not equality of every transported
effect/state probability. No sufficient theorem assumes TpPreserving.

Current narrowed statement (accepted verbatim):

> Imported dynamical law: the evolution of rays preserves the Born probability of every transported rank-one effect in every state; conditional on this law the dynamics is a linear or conjugate-linear similarity. Campaign hypothesis map on Q(i)^n: a supplied linear lift with finite orthogonality calibration and a nonzero anchor preserves transition probabilities; fixed-frame statistics for all basis, real pair and imaginary pair probes in every nonzero state, together with nonvanishing, also suffice and fix every ray. On Q(i)^2, reversible ray dynamics can preserve norms, basis and real pair statistics, report-swap covariance and orthogonality while changing a transition probability from 9/10 to 1/10. A reversible linear subspace-lattice automorphism changes another probability from 1/2 to 1/5. The dynamical law remains supplied, not derived from primitive difference.

Current bottleneck (accepted verbatim):

> The sufficient packages add explicit structure: a Gaussian-rational linear lift plus finite zero-probability calibration, or nonvanishing plus all-state fixed-frame tomographic statistics. Neither package is a derivation from primitive difference or a strictly weaker replacement for the full law. Static Born readout, reversibility, report-swap covariance, norms, basis and real pair statistics and orthogonality are jointly insufficient in dimension two. Subspace order preservation without orthocomplement preservation is also insufficient. Arbitrary ray bijections in higher dimensions under orthogonality alone, affine positive-effect automorphisms and evolving measurement-frame covariance are not classified here.

The status stays IMPORTED_ASSUMPTION. This is not a Reduced result: neither the
physical applicability of the sufficient packages nor their derivation from
primitive difference is established.

## Numbers recomputed

| Claim | Exact recomputation | Match |
|---|---|---|
| Dimensions two and one | Explicit Fin 2 countermodel carriers and Fin 1 boundary in the Lean types | yes |
| Two report-sector permutations | list(itertools.permutations(range(2))) gives (0,1), (1,0) | yes |
| Witness norms 2, 5; inner products 3, -1 | Independent Gaussian Fraction arithmetic | yes |
| Probabilities 9/10, 1/10 | countermodel_probabilities plus independent projector readout | yes |
| Imaginary-probe probabilities 1, 0 | imaginary_probe_probabilities plus independent checker | yes |
| Stretch factor 2, inverse 1/2; probabilities 1/2, 1/5 | Lean LinearEquiv inverse identities and stretch_probabilities; independent exact inverse/matrix tests | yes |
| Real/imaginary probe coefficients 2 | SymPy polynomial identities from expanded Gaussian norms | yes |
| Finite sample: 80 vectors, 6400 ordered pairs, 512 orthogonal pairs | Independently enumerated checker output | yes |
| Boundary and mutation counts: 7 rejections, 5 killed, 0 other outcomes | Counted executable results in independent replay receipt | yes |
| 80 named-source axiom reports | Counted #print axioms and matched kernel output in Lean replay receipt | yes |
| Scores L4B, L4C, L4D | Complete current companion records; each grade is the ordinal minimum of its five gates | yes |
| README/generated inventory counts | Repository generators recompute these as inventories; they are not test/build success counts | yes |
| Toolchain and Mathlib identifiers | Live version commands and cache Git HEAD in the source-bound replay receipt | yes |

The original unrestricted phrase about arbitrary ray bijections is not used as
a classification theorem. The countermodel proves two concrete admissible maps
under their specified packages. The live TFQ-0016 operad regeneration repairs
malformed YAML serialization; its mathematical source statement is unchanged.
Executed prompt TFQ-0084 and saved runs remain untouched.

## Scanner output

Command: python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict.
Result after receipt/view refresh: exit 0; HIGH=0, MEDIUM=0, LOW=3.
No HIGH/MEDIUM findings need triage. The three LOW findings concern unchanged
tensor nodes pulled into scan scope by the mandated tensor-receipt re-pin:

- R5, TFQ-1019: 20261019 is the existing scope-audit date, not a numerical theorem.
- R5, TFQ-0413: exact SymPy matrices recompute the coherent-test traces 0 and 1/2,
  and the dephasing-test traces 1/2 and 1/4. The definitions are the displayed
  Bell matrix, its partial transpose, and product effects; see the validation
  receipt for expressions and values. No number mismatch was found.
- R10, TENSOR-ASSUMPTION-COUNTERMODELS: five pre-existing modules have no receipt
  recognized by this scanner. Their compile evidence was not rebuilt or
  promoted by this campaign. This inherited coverage limitation remains open.

The final staged diff is scanned again before publication. No baseline changes.

## What the scanner could not decide

The semantic comparison above is required even with an empty scan. In particular,
finite-effect tomography is a stronger fixed-frame invariance assumption, and
subspace order preservation does not assert preservation of orthocomplements.
Orthogonality for arbitrary ray bijections above dimension two, affine
positive-effect automorphisms, physical applicability, the scale-normalization
gap and continuous-time questions remain open.

The repository-wide contract-history audit independently reports an unchanged
malformed JSON record at lean4/HilbertLiftOperators.contract.score.yaml:202.
Its bytes match the base; this is not a successful repository-wide contract
audit. All campaign-changed code companions pass their focused custody,
schema, evidence-digest and minimum-score checks.
