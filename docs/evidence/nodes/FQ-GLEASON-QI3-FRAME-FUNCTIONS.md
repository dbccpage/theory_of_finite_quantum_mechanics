# FQ-GLEASON-QI3-FRAME-FUNCTIONS

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Let V = Q(i)^3 with the standard Hermitian form. Decide whether every function f from the nonzero vectors of V to Q with f(u) + f(v) + f(w) = 1 for every orthogonal triple of nonzero vectors has the form f(v) = \<v, rho v\>/\<v, v\> for a Hermitian trace-one 3 x 3 matrix rho over Q(i), or exhibit one that does not; state separately the signed, nonnegative and {0,1}-valued variants, and whether the non-quadratic Q^3 frame function extends to Q(i)^3.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 11
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 3
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (3 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

General signed and nonnegative quadratic rigidity on all Q(i)^3 rays remain open. The {0,1}-valued variant is excluded by a finite real-ray obstruction. The specific exotic Q^3 frame function has no signed extension, by an exact finite linear certificate. The remaining problem reduces in prose to vanishing of zero-weight frame functions on Q(i)^3 that vanish on nine tomography rays (all residuals for signed rigidity; bounded residuals for nonnegative rigidity). Neither finite obstruction establishes either general vanishing assertion.

## Source status

Partial finite obstructions: no {0,1}-valued frame function on Q(i)^3, and no signed extension of the specified exotic Q^3 function. General signed and nonnegative quadratic rigidity remain open. Exact independent checks and scoped Lean declarations are linked; see the replay receipt for build evidence.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BornGaussianMod2ClassRigidity.lean`

- file: [lean4/BornGaussianMod2ClassRigidity.lean](../../../lean4/BornGaussianMod2ClassRigidity.lean)
- sha256 (`bytes`): `ab4aceb7e4aac1f76ef2c7ad3d780f422796878ab6ab8d616f73d75d05386b9d`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/campaign_fq-gap-born-uniqueness-gleason-rays_lean_replay.json](../../../dag/research/campaign_fq-gap-born-uniqueness-gleason-rays_lean_replay.json) (module `BornGaussianMod2ClassRigidity`): recorded sha256 `ab4aceb7e4aac1f76ef2c7ad3d780f422796878ab6ab8d616f73d75d05386b9d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornGaussianMod2ClassRigidity`
- counts toward the grade: yes

### Lean: `lean4/BornGaussianRationalExtensionObstruction.lean`

- file: [lean4/BornGaussianRationalExtensionObstruction.lean](../../../lean4/BornGaussianRationalExtensionObstruction.lean)
- sha256 (`bytes`): `aa68f3cdf925dcbe35b7aa2d23f51bc9bf1171963f060c8540988e5c77b1fb33`
- cited in: node.lean, receipt dag/research/campaign_fq-gleason-qi3-frame-functions_lean_replay.json (BornGaussianRationalExtensionObstruction), record TFQ-1055
- replay: `verified`
  - receipt [dag/research/campaign_fq-gleason-qi3-frame-functions_lean_replay.json](../../../dag/research/campaign_fq-gleason-qi3-frame-functions_lean_replay.json) (module `BornGaussianRationalExtensionObstruction`): recorded sha256 `aa68f3cdf925dcbe35b7aa2d23f51bc9bf1171963f060c8540988e5c77b1fb33` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornGaussianRationalExtensionObstruction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.GaussianExtension.no_exotic_extension` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianExtension.no_exotic_extension` |
| `BornFinite.GaussianExtension.no_prescribed_frame_function` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianExtension.no_prescribed_frame_function` |

- counts toward the grade: yes

### Lean: `lean4/BornGaussianRationalNoColouring.lean`

- file: [lean4/BornGaussianRationalNoColouring.lean](../../../lean4/BornGaussianRationalNoColouring.lean)
- sha256 (`bytes`): `fffb58fbf26650d8e27fcabb2935937eda3d919dee03d9b481a21b67ea0ac778`
- cited in: node.lean, receipt dag/research/campaign_fq-gleason-qi3-frame-functions_lean_replay.json (BornGaussianRationalNoColouring), record TFQ-1055
- replay: `verified`
  - receipt [dag/research/campaign_fq-gleason-qi3-frame-functions_lean_replay.json](../../../dag/research/campaign_fq-gleason-qi3-frame-functions_lean_replay.json) (module `BornGaussianRationalNoColouring`): recorded sha256 `fffb58fbf26650d8e27fcabb2935937eda3d919dee03d9b481a21b67ea0ac778` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornGaussianRationalNoColouring`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFinite.GaussianFrames.NoColouring.no_zero_one_frame_function` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFinite.GaussianFrames.NoColouring.no_zero_one_frame_function` |

- counts toward the grade: yes

### Lean: `lean4/BornRationalRayObstruction.lean`

- file: [lean4/BornRationalRayObstruction.lean](../../../lean4/BornRationalRayObstruction.lean)
- sha256 (`bytes`): `db82ac8f931e9f0d1c6870a141f3dac4e55f17d4feb437d0109df3ef51649ff0`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/campaign_fq-gap-born-uniqueness-gleason-rays_lean_replay.json](../../../dag/research/campaign_fq-gap-born-uniqueness-gleason-rays_lean_replay.json) (module `BornRationalRayObstruction`): recorded sha256 `db82ac8f931e9f0d1c6870a141f3dac4e55f17d4feb437d0109df3ef51649ff0` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornRationalRayObstruction`
- counts toward the grade: yes

### Python: `checks/independent/fq-gleason-qi3-extension.py`

- file: [checks/independent/fq-gleason-qi3-extension.py](../../../checks/independent/fq-gleason-qi3-extension.py)
- sha256 (`bytes`): `e54fbb9b4babc7324cf22aa43cab27a89b72208ba1f482c893cbf18128a99d0d`
- cited in: node.source
- counts toward the grade: yes

### Python: `checks/independent/fq-gleason-qi3-frame-functions.py`

- file: [checks/independent/fq-gleason-qi3-frame-functions.py](../../../checks/independent/fq-gleason-qi3-frame-functions.py)
- sha256 (`bytes`): `79b9d9fac2eea13b1e5a498c6aefa6017c787e3f5a8c9224e503c7d71e1c939d`
- cited in: node.source
- counts toward the grade: yes

### Python: `checks/independent/fq-gleason-qi3-tomography.py`

- file: [checks/independent/fq-gleason-qi3-tomography.py](../../../checks/independent/fq-gleason-qi3-tomography.py)
- sha256 (`bytes`): `c9225143f4f7d24e972fa966fd0313c574ce93d7036305e2cdc4439a57c0d43d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `checks/independent/data/fq_gleason_qi3_extension.json`

- file: [checks/independent/data/fq_gleason_qi3_extension.json](../../../checks/independent/data/fq_gleason_qi3_extension.json)
- sha256 (`lf-normalised`): `fd0fd770fd92f7cb60203c2b813936717db74707e9e3ac5954fab3eaed0f226b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1055_fq_gleason_qi3_frame_functions.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1055_fq_gleason_qi3_frame_functions.md](../../../dag/derivations/10_finite_qm_core/tfq_1055_fq_gleason_qi3_frame_functions.md)
- sha256 (`lf-normalised`): `6aff3f111d5d3ee4b0e7143fec82eccd5bc4855cd9782258bb224db8a247b726`
- generated view: listed, not counted
- cited in: record TFQ-1055
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fq-gap-born-uniqueness-gleason-rays.md`

- file: [dag/derivations/independent/fq-gap-born-uniqueness-gleason-rays.md](../../../dag/derivations/independent/fq-gap-born-uniqueness-gleason-rays.md)
- sha256 (`lf-normalised`): `117b3b26afb3b5286eb706c59b1b4427e6aecc82d15289a90045cf78fd762132`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/independent/fq-gleason-qi3-frame-functions.md`

- file: [dag/derivations/independent/fq-gleason-qi3-frame-functions.md](../../../dag/derivations/independent/fq-gleason-qi3-frame-functions.md)
- sha256 (`lf-normalised`): `7bd2d063e88b4921a02925352ba3bd788820007d1a2a8cbc2fec5f48931ecf05`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/independent/fq-gleason-qi3-rigidity-reduction.md`

- file: [dag/derivations/independent/fq-gleason-qi3-rigidity-reduction.md](../../../dag/derivations/independent/fq-gleason-qi3-rigidity-reduction.md)
- sha256 (`lf-normalised`): `da27e5ee0f224eb715640d0f16def2091d00a6b980f10bbd305bf3f222745884`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FQ-R-GLEASON-QI3-FRAME-FUNCTIONS` `GAP_NO_DERIVATION`: [FQ-GAP-BORN-UNIQUENESS-GLEASON](FQ-GAP-BORN-UNIQUENESS-GLEASON.md) (CONDITIONAL)

Outgoing (0):

