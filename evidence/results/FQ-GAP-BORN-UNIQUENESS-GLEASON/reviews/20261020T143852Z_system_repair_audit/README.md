# Reviewed System repair and classical exclusion

Status: **focused review passed; prepared for commit, PR and merge**. AuthorityEffect: None.

The four accepted reconstruction/geometry sources are byte-identical to the earlier sealed repair. No false theorem or fudged numerical value was found in their stated scopes. This audit fixes evidence publication/replay controls and assumption visibility, and adds an inhabited-System witness and phantom rejection check.

- [Findings and fixes](review_findings.md) and [explicit assumption ledger](assumptions.json).
- [System and guarded classification interface](ReconstructionGeometry.lean), [concrete affine/classical-exclusion geometry](ClassicalExclusion.lean), [preserved arithmetic](ReconstructionArithmetic.lean), and [unary substitution laws](ConvexSubstitution.lean).
- [Concrete System0 and negative control](SystemAudit.lean): rank1, dimension1, spectral and strongly symmetric; rank1/dimension2 spectral systems are excluded without a Jordan input.
- [Exact type exports](TheoremSignatures.lean), [75 exported signatures](verification/exported_signatures.json), and [59 axiom receipts](verification/kernel_axioms.json). A clean axiom report does **not** discharge the parameters displayed in these signatures.
- [16 scoped operation records](operad_delta.json): 15 collections with checked declarations, plus one explicitly unproved classification contract. Only unary affine substitution is formalized; no complete higher-arity operad is claimed.
- [Fresh compilation/custody checks](verification/review_checks.json), [five optimized-Python mutation controls](verification/mutation_controls.json), [dependency trust boundary](verification/dependency_packages.json), and [historical index custody](verification/historical_indices.json).
- [Historical file closure](provenance.json), [publication file inventory](publication_paths.json), [validation](validation.json), and [seal](manifest.json).

Six Lean sources were compiled in a fresh local-module build: the original four, the new audit witness, and the signature exporter. The original 51 printed receipts and eight audit receipts contain no custom axioms. The 19 arithmetic receipts and all four original source files are unchanged. Lean 4.33.1 and the pinned existing Mathlib cache were used; **Mathlib itself was not rebuilt**. Compiler binaries, direct imported artifacts and source-package commits are recorded. Failed exploratory attempts remain separate from accepted receipts.

**Open inputs:** real scalar/topological structure and the full affine-effect convention are declared. The Jordan catalogue, capacity-preserving representation certificates and classification proof are not constructed here. The combined classical-factor theorem requires its displayed dichotomy, dimension-product and rank-bound premises. Operational local tomography, Jordan multiplication, complex-field selection, tensor coherence, dynamics and full process equivalence remain open. Catalogue ball geometry is an input to the tag-to-ball theorem; the actual affine nonpolytope marginal argument does not use a classification bridge.

All 927 previously sealed file entries across 22 manifests were reverified. Their 949 files/manifests are included as immutable publication dependencies, including the earlier provider run and hand-proof submissions. This focused audit does not re-prove every historical claim. The result-subtree Git policy preserves captured bytes and whitespace. Authored source/report whitespace is checked separately.

Replay in a **fresh copy** of this folder with tools/replay.py SOURCE NEW_LABEL --lean PATH_TO_PINNED_LEAN --project PATH_TO_CONFIGURED_LEAN4_PROJECT, in dependency order: arithmetic and classical geometry; reconstruction geometry and substitution; SystemAudit; TheoremSignatures. The recorded receipts describe the original Windows host. tools/verify_review.py --repo CHECKOUT --sealed also checks the recorded live external compiler/cache paths; checking those exact host artifacts requires that environment. No private key is required for compilation.

No new provider inference or native Rust/Python implementation change was performed. Publication status is confirmed separately against the actual GitHub PR after this seal.
