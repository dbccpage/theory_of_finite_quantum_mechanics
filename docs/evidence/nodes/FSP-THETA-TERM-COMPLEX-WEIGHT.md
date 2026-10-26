# FSP-THETA-TERM-COMPLEX-WEIGHT

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Adding S_theta = i theta Q_top with real lattice charge Q_top multiplies the Boltzmann weight by exp(-i theta Q_top), which is nonreal unless theta Q_top lies in pi Z for every configuration, so positive-weight importance sampling is lost for generic theta != 0.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 26
- distinct cited Lean declarations covered by a current replay receipt: 25
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- lattice topological charge Q_top and theta vacuum term (standard)

## Bottleneck

The record is this four-index Gaussian-integer table. It does not introduce an exponential, a real angle, a plaquette sum, or a Monte Carlo sampler. The source sentence that an added term i theta Q_top multiplies a Boltzmann weight by a complex phase, and that a positive-weight sampler fails for a nonzero angle outside a discrete set, stays an imported reading. AuthorityEffect is None.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-034 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspThetaTermComplexWeight.lean`

- file: [lean4/CampaignFspThetaTermComplexWeight.lean](../../../lean4/CampaignFspThetaTermComplexWeight.lean)
- sha256 (`bytes`): `7077123bd408a147d59803e312add757b2361f554b0e037a1d1afce4423bc11e`
- cited in: node.lean, receipt dag/research/campaign_fsp-theta-term-complex-weight_lean_replay.json (CampaignFspThetaTermComplexWeight), record TFQ-1198
- replay: `verified`
  - receipt [dag/research/campaign_fsp-theta-term-complex-weight_lean_replay.json](../../../dag/research/campaign_fsp-theta-term-complex-weight_lean_replay.json) (module `CampaignFspThetaTermComplexWeight`): recorded sha256 `7077123bd408a147d59803e312add757b2361f554b0e037a1d1afce4423bc11e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspThetaTermComplexWeight`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspThetaTermComplexWeight.charge1PositiveOnlyAtZero` | yes | yes | yes | none | `#print axioms CampaignFspThetaTermComplexWeight.charge1PositiveOnlyAtZero` |
| `CampaignFspThetaTermComplexWeight.im01` | yes | yes | yes | none | `#print axioms CampaignFspThetaTermComplexWeight.im01` |
| `CampaignFspThetaTermComplexWeight.im11` | yes | yes | yes | none | `#print axioms CampaignFspThetaTermComplexWeight.im11` |
| `CampaignFspThetaTermComplexWeight.im11_ne` | yes | yes | yes | none | `#print axioms CampaignFspThetaTermComplexWeight.im11_ne` |
| `CampaignFspThetaTermComplexWeight.im21` | yes | yes | yes | none | `#print axioms CampaignFspThetaTermComplexWeight.im21` |
| `CampaignFspThetaTermComplexWeight.im31` | yes | yes | yes | none | `#print axioms CampaignFspThetaTermComplexWeight.im31` |
| `CampaignFspThetaTermComplexWeight.im31_ne` | yes | yes | yes | none | `#print axioms CampaignFspThetaTermComplexWeight.im31_ne` |
| `CampaignFspThetaTermComplexWeight.mulNegI_eq_gMul` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFspThetaTermComplexWeight.mulNegI_eq_gMul` |
| `CampaignFspThetaTermComplexWeight.notPositive21` | yes | yes | yes | none | `#print axioms CampaignFspThetaTermComplexWeight.notPositive21` |
| `CampaignFspThetaTermComplexWeight.phaseProduct` | yes | yes | yes | none | `#print axioms CampaignFspThetaTermComplexWeight.phaseProduct` |
| `CampaignFspThetaTermComplexWeight.positive01` | yes | yes | yes | none | `#print axioms CampaignFspThetaTermComplexWeight.positive01` |
| `CampaignFspThetaTermComplexWeight.quarter0` | yes | yes | yes | none | `#print axioms CampaignFspThetaTermComplexWeight.quarter0` |
| `CampaignFspThetaTermComplexWeight.quarter1` | yes | yes | yes | none | `#print axioms CampaignFspThetaTermComplexWeight.quarter1` |
| `CampaignFspThetaTermComplexWeight.quarter2` | yes | yes | yes | none | `#print axioms CampaignFspThetaTermComplexWeight.quarter2` |
| `CampaignFspThetaTermComplexWeight.quarter3` | yes | yes | yes | none | `#print axioms CampaignFspThetaTermComplexWeight.quarter3` |
| `CampaignFspThetaTermComplexWeight.quarter4` | yes | yes | yes | none | `#print axioms CampaignFspThetaTermComplexWeight.quarter4` |
| `CampaignFspThetaTermComplexWeight.re21` | yes | yes | yes | none | `#print axioms CampaignFspThetaTermComplexWeight.re21` |
| `CampaignFspThetaTermComplexWeight.weight00` | yes | yes | yes | none | `#print axioms CampaignFspThetaTermComplexWeight.weight00` |
| `CampaignFspThetaTermComplexWeight.weight01` | yes | yes | yes | none | `#print axioms CampaignFspThetaTermComplexWeight.weight01` |
| `CampaignFspThetaTermComplexWeight.weight10` | yes | yes | yes | none | `#print axioms CampaignFspThetaTermComplexWeight.weight10` |
| `CampaignFspThetaTermComplexWeight.weight11` | yes | yes | yes | none | `#print axioms CampaignFspThetaTermComplexWeight.weight11` |
| `CampaignFspThetaTermComplexWeight.weight20` | yes | yes | yes | none | `#print axioms CampaignFspThetaTermComplexWeight.weight20` |
| `CampaignFspThetaTermComplexWeight.weight21` | yes | yes | yes | none | `#print axioms CampaignFspThetaTermComplexWeight.weight21` |
| `CampaignFspThetaTermComplexWeight.weight30` | yes | yes | yes | none | `#print axioms CampaignFspThetaTermComplexWeight.weight30` |
| `CampaignFspThetaTermComplexWeight.weight31` | yes | yes | yes | none | `#print axioms CampaignFspThetaTermComplexWeight.weight31` |

- counts toward the grade: yes

### Python: `checks/independent/fsp-theta-term-complex-weight.py`

- file: [checks/independent/fsp-theta-term-complex-weight.py](../../../checks/independent/fsp-theta-term-complex-weight.py)
- sha256 (`bytes`): `ac68d013a92ef81144ed8c8e1b91f6d2a1247ac2d913d51ba8aa3074bf4662c2`
- cited in: record TFQ-1198

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `check` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1198_fsp_theta_term_complex_weight.md`

- file: [dag/derivations/26_fsp/tfq_1198_fsp_theta_term_complex_weight.md](../../../dag/derivations/26_fsp/tfq_1198_fsp_theta_term_complex_weight.md)
- sha256 (`lf-normalised`): `62cbe6f9d7fcbafbac10425deff9700d43b72a7c611acc130b6cc7af58258286`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1198
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-theta-term-complex-weight.md`

- file: [dag/derivations/independent/fsp-theta-term-complex-weight.md](../../../dag/derivations/independent/fsp-theta-term-complex-weight.md)
- sha256 (`lf-normalised`): `c5c9befeb2823e3de35b52d480ac392c69eaefdde4101985568ec0558a7735a4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign.md)
- sha256 (`lf-normalised`): `f894f295fb17dc831f4e961602bea56223bf79ae6b34c3350cfa6fe358789808`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `5a72c2f6006ea18c3362f0a63e8525b65d41898e8f1bd437b7e4c2e368c7e102`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-THETA-TERM-COMPLEX-WEIGHT` `CONDITIONAL_ON_IMPORT`: [FSP-U1-WILSON-ACTION](FSP-U1-WILSON-ACTION.md) (PROVED_LEAN)

Outgoing (0):

