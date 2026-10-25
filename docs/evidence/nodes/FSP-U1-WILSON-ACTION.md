# FSP-U1-WILSON-ACTION

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> With link phases U_ij = exp(i A_ij) on ordered vertex pairs and oriented closed-path products U_p over a finite plaquette family, the Wilson action S = beta_g sum_p (1 - Re U_p) is invariant under local U(1) gauge transformations and is nonnegative for beta_g \>= 0.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 13
- cited Lean declaration references covered by a current replay receipt: 13
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Lean: CampaignFspU1WilsonAction.fsp_u1_wilson_action states gauge invariance (for every g: V -\> U(1) and for every angle shift A_ij -\> A_ij + theta_i - theta_j) and nonnegativity for beta_g \>= 0, for any vertex type and any finite family of closed paths; the periodic hypercubic lattice (ZMod L)^d is one instance. beta_g \>= 0 is required: one self-link plaquette with phase -1 and beta_g = -1 gives S = -2. Links are functions of ordered vertex pairs, so for L \<= 2 the two parallel links between neighbours are identified. No fermion-sign consequence, continuum limit, reflection positivity, transfer matrix or non-abelian action is claimed. Audited PROVED_LEAN applies only to the narrowed DAG statement; the source record FSP-DERIV-032 claims strict positivity and a Haar-measure bound, neither established here.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-032 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspU1WilsonAction.lean`

- file: [lean4/CampaignFspU1WilsonAction.lean](../../../lean4/CampaignFspU1WilsonAction.lean)
- sha256 (`bytes`): `5f78709a5e554f44dc52e0fe3bf79e80f34985c8c970e5128284ab7f53c3ecb0`
- cited in: node.lean, receipt dag/research/campaign_fsp-u1-wilson-action_lean_replay.json (CampaignFspU1WilsonAction), record TFQ-1196
- replay: `verified`
  - receipt [dag/research/campaign_fsp-u1-wilson-action_lean_replay.json](../../../dag/research/campaign_fsp-u1-wilson-action_lean_replay.json) (module `CampaignFspU1WilsonAction`): recorded sha256 `5f78709a5e554f44dc52e0fe3bf79e80f34985c8c970e5128284ab7f53c3ecb0` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspU1WilsonAction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspU1WilsonAction.fsp_u1_wilson_action` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspU1WilsonAction.fsp_u1_wilson_action` |
| `CampaignFspU1WilsonAction.gaugeAct_gaugeAct` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFspU1WilsonAction.gaugeAct_gaugeAct` |
| `CampaignFspU1WilsonAction.gaugeAct_reversal` | yes | yes | yes | propext | `#print axioms CampaignFspU1WilsonAction.gaugeAct_reversal` |
| `CampaignFspU1WilsonAction.holonomy_gaugeAct` | yes | yes | yes | propext | `#print axioms CampaignFspU1WilsonAction.holonomy_gaugeAct` |
| `CampaignFspU1WilsonAction.hypercubicWilson_gauge_invariant` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspU1WilsonAction.hypercubicWilson_gauge_invariant` |
| `CampaignFspU1WilsonAction.hypercubicWilson_nonneg` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspU1WilsonAction.hypercubicWilson_nonneg` |
| `CampaignFspU1WilsonAction.linkOfAngle_gaugeAngle` | yes | yes | yes | module-level | `#print axioms CampaignFspU1WilsonAction.linkOfAngle_gaugeAngle` |
| `CampaignFspU1WilsonAction.loopHolonomy_gaugeAct` | yes | yes | yes | propext | `#print axioms CampaignFspU1WilsonAction.loopHolonomy_gaugeAct` |
| `CampaignFspU1WilsonAction.wilsonAction_eq_zero_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspU1WilsonAction.wilsonAction_eq_zero_iff` |
| `CampaignFspU1WilsonAction.wilsonAction_gauge_invariant` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspU1WilsonAction.wilsonAction_gauge_invariant` |
| `CampaignFspU1WilsonAction.wilsonAction_linkOfAngle` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspU1WilsonAction.wilsonAction_linkOfAngle` |
| `CampaignFspU1WilsonAction.wilsonAction_nonneg` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspU1WilsonAction.wilsonAction_nonneg` |
| `CampaignFspU1WilsonAction.wilsonAction_nonneg_needs_beta` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspU1WilsonAction.wilsonAction_nonneg_needs_beta` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1196_fsp_u1_wilson_action.md`

- file: [dag/derivations/26_fsp/tfq_1196_fsp_u1_wilson_action.md](../../../dag/derivations/26_fsp/tfq_1196_fsp_u1_wilson_action.md)
- sha256 (`lf-normalised`): `6a35677edfc6a9891d9ea667dc4180b4f981d70ac84f2de6f395a09c4f9c9109`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1196
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-u1-wilson-action.md`

- file: [dag/derivations/independent/fsp-u1-wilson-action.md](../../../dag/derivations/independent/fsp-u1-wilson-action.md)
- sha256 (`lf-normalised`): `d0c1b888b6261efa44ab3b452f77664ae6198b43b2792c4cdc20fa02e89d9957`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-U1-WILSON-ACTION` `DERIVED_LEAN`: [DS-QM063-HOLONOMY-COHERENT-INTENSITY](DS-QM063-HOLONOMY-COHERENT-INTENSITY.md) (PROVED_LEAN), [FSP-HUBBARD-PROTECTED-REPRESENTATIONS](FSP-HUBBARD-PROTECTED-REPRESENTATIONS.md) (CONDITIONAL)

Outgoing (3):

- `APP-R-FSP-SU2-ADJOINT-REAL-DET` `CONDITIONAL_ON_IMPORT`: [FSP-SU2-ADJOINT-REAL-DET](FSP-SU2-ADJOINT-REAL-DET.md) (IMPORTED_ASSUMPTION)
- `APP-R-FSP-THETA-TERM-COMPLEX-WEIGHT` `CONDITIONAL_ON_IMPORT`: [FSP-THETA-TERM-COMPLEX-WEIGHT](FSP-THETA-TERM-COMPLEX-WEIGHT.md) (IMPORTED_ASSUMPTION)
- `APP-R-FSP-WILSON-DIRAC-GAMMA5` `CONDITIONAL_ON_IMPORT`: [FSP-WILSON-DIRAC-GAMMA5](FSP-WILSON-DIRAC-GAMMA5.md) (IMPORTED_ASSUMPTION)
