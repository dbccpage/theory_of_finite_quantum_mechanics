# Independent scoped review: QM PRs 393-406 excluding 401

AuthorityEffect: None. Base: `4fea09ae176aae31115e38bb2b21819237055811`.

Read-only review from Git objects in the foreign dirty checkout. No repository files changed, no checkout, no Lean/Lake/Cargo build, no dependency installation, no provider call. Lean evidence below is retained receipt evidence, not a fresh kernel verification. Each narrowed standing statement matches the actual declaration types; original broad obligations and statuses remain unchanged. All 13 Lean source digests match their PR receipts; admission scan found no added forbidden executable tokens. Recorded axiom sets are subsets of propext, Classical.choice, Quot.sound.

## Exact heads and source bindings

| PR | Reviewed head | Lean source / claim lines | SHA-256 | Scoped verdict |
|---|---|---|---|---|
| 393 | b17fc3948e28df01dc2a201f3e9e9e52992bc5b1 | lean4/CampaignFqGapCustodyAndReceipts.lean:10,12,14 | c33d992442c75c81cad274e786a8f34ae95fb666ba10298e89f5a2332011e012 | FULL: three Nat facts only; OPEN |
| 394 | 3d82f525d1efd62a153c34fa0aca0152cefb3419 | lean4/CampaignFqGapC500OriginalTargets.lean:14,18,22,25,28,35,47 | b0b2c3723f85472fd6099601c25bdd6c8650302e4c8047ab11aa89e705630090 | FULL: runs and supplied lists, not original contracts; OPEN |
| 395 | c316f6470c9742263a050ac63209abb69d96dd17 | lean4/CampaignGpImportGleason.lean:36,40,43,46,49 | 13a68c5bb1a92476960aa77de7ef1dd8dfe1a912ebc9ebb325fab5c1bbffa06a | FULL: two-label arithmetic, not Gleason; IMPORTED_ASSUMPTION |
| 396 | 74182be08f0de21c6e8b8659bea5d6f1eaf691e1 | lean4/CampaignBfCocycleObstruction.lean:21,25,30,34,41,45 | 882c2767c327fb2be146c2069898bea71eac43e6c1adf5b61c044475feb4eddc | FULL: explicit normalized Z2 cochains, not BF dynamics; OPEN |
| 397 | 37e3f462ce8a1c3f18ff11fd4ab53e89a19d3e19 | lean4/CampaignSignedTriangleSwitching.lean:24,29,35,47,54,59,63 | dee0cbf7bf415fd8202e0668f45757288dbf4bbce05aba16e8aaffd080ab57c1 | FULL: vertex switching on one triangle, not bordism; OPEN |
| 398 | 421a0dfb72738fa4da38eb533d77a3f0ec525de7 | lean4/CampaignIdentityConvention.lean:13,20,25,34,53,57,61 | fa42557ad55d2b9150bea0a4c9d38a205d41e2d688115bb71091d0b96c6f8ff6 | FULL: convention-relative identity, not computability undecidability; CONDITIONAL |
| 399 | c53d52d07c1dd4c29578bcbaa8c0b99076083d4d | lean4/CampaignReggeFiniteAction.lean:14,25,30,36,39,44 | dd1ccb8b8bc8e402055f561c46b161f41d2c3b007203e9716c5f067c4e131089 | FULL: commutative-ring finite sums, not geometric convergence; IMPORTED_ASSUMPTION |
| 400 | f7468340f750132b78af72fcb4007a32788b91cb | lean4/CampaignConstraintKernelProjector.lean:19,24,35,37,40,52,57,60,64 | 4a01928ee24ba7b0f5432ede8b95a1c974f09ba942a596f849a6df520946b0d6 | FULL: integer-triple model, not Wheeler-DeWitt; OPEN |
| 402 | 74763ec1d8cfb8863ec3c8502c4fd57df47ae578 | lean4/CampaignMajImportCosetWeight.lean:32,34,37,40,42,44,46,48,51 | 29b2497864b3b9c7e9b9500c6c90cbb902df4b81029253c70acc2923d1971008 | FULL: one 2 by 4 matrix, not NP-hardness; IMPORTED_ASSUMPTION |
| 403 | 67e11447c3a4bc322a5e0dae814a4fffb510bef0 | lean4/CampaignGpImportTensorProduct.lean:19,37,82,123,129,136,149,156,164,176,180 | 5d83a84e8099d4d38e989378b276244c701c6bbfe31aab4c78171d09e5277a42 | FULL: Bool-by-Bool integer tagged bilinear map, not physical tensor uniqueness; IMPORTED_ASSUMPTION |
| 404 | e571e6e54f44378d811decd35fb67a5dee8b7445 | lean4/CampaignGpImportCptpClass.lean:12,17,27,31,35,39,45,88,103,218 | 5667a581f964eb7babec906cc92c49ea4dd4c859a71a49fdc4327c812fcf54b7 | FULL: finite Boolean reversible dilations, not a CPTP class; IMPORTED_ASSUMPTION |
| 405 | c8c6556a4ed98eba12a279ad1ed22ed8897f2ca9 | lean4/CampaignGpImportContinuousTime.lean:9,12,40,43,50,60,63,70,77,81 | efc118c4a3ef4ec32ac5fdad45c4b4db15e393cc2298e84156076b31eeaaf7b1 | FULL: Boolean toggle / integer-pair interpolants, not continuous dynamics; IMPORTED_ASSUMPTION |
| 406 | da6cfad376079f5d8edd1848c2e225ae54c30984 | lean4/CampaignGpImportContinuumHilbert.lean:7,11,15,22,26,30,33,36,39,42,45,48,53 | c295d54bb448053163b2de830650a5724201901cb8b4f00e1a3c70418524e965 | FULL: finite sums for arbitrary finite n, not Hilbert completion; IMPORTED_ASSUMPTION |

All independent notes retain `Status: AI-drafted, awaiting human review.`. This AI review is not named human review. Derivation prose and PR claim tables were compared with the proof types, rather than inferred from declaration names. Integers are not a finite carrier: PR400 explicitly distinguishes finite dimension from its infinite integer-triple carrier.

## Exact independent-check replay observations

The committed independent scripts were read before execution and compiled from `git show` bytes in an in-memory namespace. They import no repository implementation. Plain checks used Python 3.12 `-I -X utf8 -B`; symbolic checks used existing Python 3.10/SymPy 1.11.1 with the same isolation flags. Python 3.12 lacks SymPy and Python 3.9 is not installed; nothing was installed.

| PR | checks/independent script stem | Observed successful output |
|---|---|---|
| 393 | fq-gap-custody-and-receipts | checks=3 failures=0 gap=24 remainder=31 proper=True |
| 394 | fq-gap-c500-original-targets | checks=8 failures=0 cover=250 product=250 clause_sum=21 last=5 labels=5 |
| 395 | gp-import-gleason | checks=6 failures=0 w2=4 w1=1 unit=5 direct=4 swapped=1 |
| 396 | fsp-bf-2group-sign-claim | pentagon_cases=16 cochains=16 normalized_cochains=2 generator_phase=-1 failures=0 |
| 397 | fsp-cobordism-intrinsic-sign | triangles=8 switching_cases=64 balanced=4 obstructed=4 failures=0 |
| 398 | pgw-identity-convention-undecidable | observer_families=16 restrictions=81 empty_relation_pairs=4 exact_relation_pairs=2 failures=0 |
| 399 | fsp-regge-deficit-action | symbolic_identities=3 integer_cases=729 nonflat_action=0 area_actions=[1, 2] failures=0 |
| 400 | fsp-discrete-wdw-constraint | vectors=125 rank=2 kernel_dimension=1 quadratic_values=(2,-1) nonprojector=True failures=0 |
| 402 | maj-import-coset-weight-np-hard | CHECKS22 FAILURES0; coset[1,6,10,13], weights[1,2,2,3], minimum1, weight_one[1], coordinates(1,0,0,0), kernel[0,7,11,12] |
| 403 | gp-import-tensor-product | checks=10048 failures=0 samples=625 witness_dump=0 witness_tensor=1 points=4 |
| 404 | gp-import-cptp-class | checks=37 failures=0 maps=256 dilations=4 named=4 mass=(5,0) collapse=(0,0) |
| 405 | gp-import-continuous-time | checks=14 failures=0 maps=4 witness=(((1,1),(1,-1)),((-1,-1),(-1,1))) scale=4 |
| 406 | gp-import-continuum-hilbert | checks=261 failures=0 window=(8,4,2,1) squares=(64,16,4,1) sum=85 scaled=256 lengths=41 |

These observations do not independently reproduce the PRs' earlier whole-suite counts, queue rankings, generated-view census or retained kernel build logs.

## Actionable acceptance / integration issues

1. At reviewed heads, PR393-395 and PR402-406 add a formal source without a score companion and edit `lean4/lakefile.lean` without rebinding its existing companion. They cannot be represented as satisfying current source-governance acceptance. Add honest evidence-backed assessments; scoped low-level examples require human-authorized exact-source exceptions, not invented L4 grades.
2. PR396-400 have source/registry/checker companions with matching source and evidence digests. Proof scores are L3D for PR396, L2D for PR397-400; checkers L2D; registry L1D. Their policy changes preserve the global floor and add only recorded exact proof pins. All 15 companion artifact bindings and their cited evidence digests matched.
3. Shared DAG/generated files and the Lake registry must be reconciled on current main; do not overwrite another merged campaign with each branch's stale full generated view. PR393 and PR394 were CONFLICTING at review time; all other assigned heads reported MERGEABLE, which does not establish correct integration.
4. Retained receipt source hashes can remain truthful after shared-registry integration, but original receipt Lakefile hashes describe the historical branch build, not a new integrated build. Do not edit historical build claims into fresh verification.

No blocking mathematical defect or required statement narrowing beyond the existing scoped statements was found in this review.


