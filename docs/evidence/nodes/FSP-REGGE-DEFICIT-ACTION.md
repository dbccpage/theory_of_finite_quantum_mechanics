# FSP-REGGE-DEFICIT-ACTION

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On a 4D triangulation with squared edge lengths, the deficit angle at a hinge h is epsilon_h = 2 pi - sum of dihedral angles at h and the Regge action is S = sum_h A_h epsilon_h; its convergence to the Einstein-Hilbert action under refinement is a literature result imported here.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- distinct cited Lean declarations covered by a current replay receipt: 7
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Regge calculus (Regge 1961; Cheeger-Mueller-Schrader convergence)

## Bottleneck

Areas, angles and the full-turn parameter are declared algebraic data. Geometric realizability, actual triangulation moves, Lorentzian signature, convergence to the Einstein-Hilbert action, and fermion-sign consequences are not established. Original target retained as an obligation: On a 4D triangulation with squared edge lengths, the deficit angle at a hinge h is epsilon_h = 2 pi - sum of dihedral angles at h and the Regge action is S = sum_h A_h epsilon_h; its convergence to the Einstein-Hilbert action under refinement is a literature result imported here. Prior boundary: Regge calculus carries no fermion-sign content in this package; Lorentzian signature, convergence conditions and any sign consequence need separate evidence (ledger GIN-C13).

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-048 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignReggeFiniteAction.lean`

- file: [lean4/CampaignReggeFiniteAction.lean](../../../lean4/CampaignReggeFiniteAction.lean)
- sha256 (`bytes`): `dd1ccb8b8bc8e402055f561c46b161f41d2c3b007203e9716c5f067c4e131089`
- cited in: node.lean, receipt dag/research/campaign_fsp-regge-deficit-action_lean_replay.json (CampaignReggeFiniteAction), record TFQ-1212
- replay: `verified`
  - receipt [dag/research/campaign_fsp-regge-deficit-action_lean_replay.json](../../../dag/research/campaign_fsp-regge-deficit-action_lean_replay.json) (module `CampaignReggeFiniteAction`): recorded sha256 `dd1ccb8b8bc8e402055f561c46b161f41d2c3b007203e9716c5f067c4e131089` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignReggeFiniteAction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignReggeFiniteAction.action` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignReggeFiniteAction.action` |
| `CampaignReggeFiniteAction.area_linearity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignReggeFiniteAction.area_linearity` |
| `CampaignReggeFiniteAction.declared_areas_change_action` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignReggeFiniteAction.declared_areas_change_action` |
| `CampaignReggeFiniteAction.deficit_expansion` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignReggeFiniteAction.deficit_expansion` |
| `CampaignReggeFiniteAction.flat_deficits_give_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignReggeFiniteAction.flat_deficits_give_zero` |
| `CampaignReggeFiniteAction.same_deficit_area_split` | yes | yes | yes | propext | `#print axioms CampaignReggeFiniteAction.same_deficit_area_split` |
| `CampaignReggeFiniteAction.zero_action_does_not_imply_flat` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignReggeFiniteAction.zero_action_does_not_imply_flat` |

- counts toward the grade: yes

### Python: `checks/independent/fsp-regge-deficit-action.py`

- file: [checks/independent/fsp-regge-deficit-action.py](../../../checks/independent/fsp-regge-deficit-action.py)
- sha256 (`bytes`): `9a72e9d17ea58b451d96a1b313791dfda8be923ab5f8d067e0e04ae2e40d27cf`
- cited in: record TFQ-1212
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1212_fsp_regge_deficit_action.md`

- file: [dag/derivations/26_fsp/tfq_1212_fsp_regge_deficit_action.md](../../../dag/derivations/26_fsp/tfq_1212_fsp_regge_deficit_action.md)
- sha256 (`lf-normalised`): `11cd763976e4bad44d70e1256fbfefa45867dcea3ebca28336e2d2625291f4e4`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1212
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-regge-deficit-action.md`

- file: [dag/derivations/independent/fsp-regge-deficit-action.md](../../../dag/derivations/independent/fsp-regge-deficit-action.md)
- sha256 (`lf-normalised`): `94a6ab93c604d14ff24bbd79f2cd05a00d441b3f7a94c1e7a87815ea25d7b674`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-regge-deficit-action_lean_replay.json`

- file: [dag/research/campaign_fsp-regge-deficit-action_lean_replay.json](../../../dag/research/campaign_fsp-regge-deficit-action_lean_replay.json)
- sha256 (`lf-normalised`): `3605da9669819fb75a49cbd397107abc04be9f5bb4b8fce04b8c306a4a99903e`
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

- `APP-R-FSP-REGGE-DEFICIT-ACTION` `CONDITIONAL_ON_IMPORT`: [PGW-WDP-DEGREE-K-TORSION-BALANCE](PGW-WDP-DEGREE-K-TORSION-BALANCE.md) (PROVED_PROSE), [FSP-COBORDISM-INTRINSIC-SIGN](FSP-COBORDISM-INTRINSIC-SIGN.md) (OPEN)

Outgoing (1):

- `APP-R-FSP-DISCRETE-WDW-CONSTRAINT` `GAP_NO_DERIVATION`: [FSP-DISCRETE-WDW-CONSTRAINT](FSP-DISCRETE-WDW-CONSTRAINT.md) (OPEN)
