# FSP-THETA-TERM-COMPLEX-WEIGHT

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For angle indices 0, 1, 2 and 3, one quarter turn of the Gaussian integer (1, 0) by the pair (0, -1) yields (1, 0), (0, -1), (-1, 0) and (0, 1), and the fourth turn returns to (1, 0). That turn is multiplication by (0, -1), and (1, 0) times (0, -1) is (0, -1). Charge 0 keeps the weight (1, 0) at each of those four indices. Charge 1 uses the quarter-turn value. The second coordinate at charge 1 is 0, -1, 0 and 1, hence nonzero at indices 1 and 3. At index 2 with charge 1 the first coordinate is -1, so that pair is not positive in the first coordinate. Among the four charge-1 pairs, only index 0 has a positive first coordinate and second coordinate 0.

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
- sha256 (`lf-normalised`): `47c8be251c0322568587f7f846d6e531e3eb74ca6df5e8355ca05c5395d9342a`
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
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-THETA-TERM-COMPLEX-WEIGHT` `CONDITIONAL_ON_IMPORT`: [FSP-U1-WILSON-ACTION](FSP-U1-WILSON-ACTION.md) (PROVED_LEAN)

Outgoing (0):

