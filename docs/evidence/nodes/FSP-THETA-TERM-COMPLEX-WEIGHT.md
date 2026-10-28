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

### Lean: `lean4/FermionSignThetaTermComplexWeight.lean`

- file: [lean4/FermionSignThetaTermComplexWeight.lean](../../../lean4/FermionSignThetaTermComplexWeight.lean)
- sha256 (`bytes`): `8aad90bf52adf206cc224ef107e0e3cea21a8427773c3dd0816e2d2e20b370bb`
- cited in: node.lean, receipt dag/research/campaign_fsp-theta-term-complex-weight_lean_replay.json (FermionSignThetaTermComplexWeight), record TFQ-1198
- replay: `verified`
  - receipt [dag/research/campaign_fsp-theta-term-complex-weight_lean_replay.json](../../../dag/research/campaign_fsp-theta-term-complex-weight_lean_replay.json) (module `FermionSignThetaTermComplexWeight`): recorded sha256 `8aad90bf52adf206cc224ef107e0e3cea21a8427773c3dd0816e2d2e20b370bb` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FermionSignThetaTermComplexWeight`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FermionSignThetaTermComplexWeight.charge1PositiveOnlyAtZero` | yes | yes | yes | none | `#print axioms FermionSignThetaTermComplexWeight.charge1PositiveOnlyAtZero` |
| `FermionSignThetaTermComplexWeight.im01` | yes | yes | yes | none | `#print axioms FermionSignThetaTermComplexWeight.im01` |
| `FermionSignThetaTermComplexWeight.im11` | yes | yes | yes | none | `#print axioms FermionSignThetaTermComplexWeight.im11` |
| `FermionSignThetaTermComplexWeight.im11_ne` | yes | yes | yes | none | `#print axioms FermionSignThetaTermComplexWeight.im11_ne` |
| `FermionSignThetaTermComplexWeight.im21` | yes | yes | yes | none | `#print axioms FermionSignThetaTermComplexWeight.im21` |
| `FermionSignThetaTermComplexWeight.im31` | yes | yes | yes | none | `#print axioms FermionSignThetaTermComplexWeight.im31` |
| `FermionSignThetaTermComplexWeight.im31_ne` | yes | yes | yes | none | `#print axioms FermionSignThetaTermComplexWeight.im31_ne` |
| `FermionSignThetaTermComplexWeight.mulNegI_eq_gMul` | yes | yes | yes | Quot.sound, propext | `#print axioms FermionSignThetaTermComplexWeight.mulNegI_eq_gMul` |
| `FermionSignThetaTermComplexWeight.notPositive21` | yes | yes | yes | none | `#print axioms FermionSignThetaTermComplexWeight.notPositive21` |
| `FermionSignThetaTermComplexWeight.phaseProduct` | yes | yes | yes | none | `#print axioms FermionSignThetaTermComplexWeight.phaseProduct` |
| `FermionSignThetaTermComplexWeight.positive01` | yes | yes | yes | none | `#print axioms FermionSignThetaTermComplexWeight.positive01` |
| `FermionSignThetaTermComplexWeight.quarter0` | yes | yes | yes | none | `#print axioms FermionSignThetaTermComplexWeight.quarter0` |
| `FermionSignThetaTermComplexWeight.quarter1` | yes | yes | yes | none | `#print axioms FermionSignThetaTermComplexWeight.quarter1` |
| `FermionSignThetaTermComplexWeight.quarter2` | yes | yes | yes | none | `#print axioms FermionSignThetaTermComplexWeight.quarter2` |
| `FermionSignThetaTermComplexWeight.quarter3` | yes | yes | yes | none | `#print axioms FermionSignThetaTermComplexWeight.quarter3` |
| `FermionSignThetaTermComplexWeight.quarter4` | yes | yes | yes | none | `#print axioms FermionSignThetaTermComplexWeight.quarter4` |
| `FermionSignThetaTermComplexWeight.re21` | yes | yes | yes | none | `#print axioms FermionSignThetaTermComplexWeight.re21` |
| `FermionSignThetaTermComplexWeight.weight00` | yes | yes | yes | none | `#print axioms FermionSignThetaTermComplexWeight.weight00` |
| `FermionSignThetaTermComplexWeight.weight01` | yes | yes | yes | none | `#print axioms FermionSignThetaTermComplexWeight.weight01` |
| `FermionSignThetaTermComplexWeight.weight10` | yes | yes | yes | none | `#print axioms FermionSignThetaTermComplexWeight.weight10` |
| `FermionSignThetaTermComplexWeight.weight11` | yes | yes | yes | none | `#print axioms FermionSignThetaTermComplexWeight.weight11` |
| `FermionSignThetaTermComplexWeight.weight20` | yes | yes | yes | none | `#print axioms FermionSignThetaTermComplexWeight.weight20` |
| `FermionSignThetaTermComplexWeight.weight21` | yes | yes | yes | none | `#print axioms FermionSignThetaTermComplexWeight.weight21` |
| `FermionSignThetaTermComplexWeight.weight30` | yes | yes | yes | none | `#print axioms FermionSignThetaTermComplexWeight.weight30` |
| `FermionSignThetaTermComplexWeight.weight31` | yes | yes | yes | none | `#print axioms FermionSignThetaTermComplexWeight.weight31` |

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
- sha256 (`lf-normalised`): `3e91bbc2261f1798486de74df3d5dbc9ab9ce26d3ef36da0ba6ea4d0a6e1abd0`
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

