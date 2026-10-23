# Review of PR #209

AuthorityEffect: None. AI-assisted independent review; no human review is claimed.

Scope: author head ed447cc0e2cd0a89e2036c4902ea5ca5fc0a9a07, integrated with the current main and the isolated-contract repair. The full added Lean module, independent checker, derivation note and target record were read. A fresh target build and direct Lean invocation passed; warnings are retained in the receipt.

Result: the contribution is NARROWED. FSP-WILSON-DIRAC-GAMMA5 remains IMPORTED_ASSUMPTION with no resolving Lean reference. The generic Clifford data and polynomial/block determinant lemmas do not establish the Wilson operator's gamma5 adjoint identity. No node is raised.

| Atomic claim | Declaration or check | Verdict |
|---|---|---|
| Euclidean Clifford data in dimensions 2 and 4 | CampaignFspWilsonDiracGamma5.euclideanClifford2 and euclideanClifford4 | FULL for these supplied finite matrix families |
| Conjugate roots have equal multiplicity | charpoly_rootMultiplicity_conj | FULL under the explicitly required conjugation-fixed coefficient hypothesis; not a Wilson characteristic-polynomial theorem |
| Duplicating a finite complex matrix gives the determinant square | two_flavor_det_eq_sq | FULL |
| A conjugation-fixed scalar has a real nonnegative square | two_flavor_det_real_nonneg | FULL under its realness hypothesis |
| Wilson gamma5 adjoint, real determinant, and the resulting spectral statement for every Wilson operator | not proved in this module | NOT PROVED, retained in the bottleneck |

Exact independent replay, under normal and optimized Python, obtains determinant -3, two-flavor determinant 9, and characteristic polynomial coefficients [1, -8, 28, -56, 66, -40, 4, 8, -3] for the stated periodic 2 by 2 lattice fixture. This is one fixture, not a general operator proof. Strict typing of the independent checker passed. Five printed axiom reports use only propext, Classical.choice and Quot.sound.

The proof module is L4D: its finite matrix interfaces carry the Clifford invariants, but many Lean linter warnings remain and no complete resource benchmark is claimed. The independent regression checker is L3D under the maintainer-approved test-support exception. Declarative Lake registration is L1D under the same support-file policy. Historical contracts are preserved and new active records bind the reviewed bytes. The source-scoped validator alone does not enforce the capability floor.

The executable evidence is in dag/research/campaign_fsp-wilson-dirac-gamma5_review_validation.json. The final integration pipeline is recorded separately. No general Wilson-Dirac derivation, whole-estate score certification or human approval follows from these checks.

Final integration: all six sync checks, rendered views, invariants, DAG validation (zero failures), evidence map, tensor pins, generated status and results table checks pass; all 24 selected campaign regressions and the full README check pass. The overclaim scan has zero HIGH, zero MEDIUM and three inherited tensor-repin LOW hints (date identifier, prior fractions, legacy missing receipts). Their mathematical statements are unchanged; the five legacy modules were not re-certified here. Details are preserved in the pipeline receipt.
