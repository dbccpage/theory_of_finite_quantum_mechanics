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

### Lean: `lean4/ReggeFiniteAction.lean`

- file: [lean4/ReggeFiniteAction.lean](../../../lean4/ReggeFiniteAction.lean)
- sha256 (`bytes`): `86b051674e156ec6e9e1fb03030dde563663d336259e385aabe485661d9442fc`
- cited in: node.lean, receipt dag/research/campaign_fsp-regge-deficit-action_lean_replay.json (ReggeFiniteAction), record TFQ-1212
- replay: `verified`
  - receipt [dag/research/campaign_fsp-regge-deficit-action_lean_replay.json](../../../dag/research/campaign_fsp-regge-deficit-action_lean_replay.json) (module `ReggeFiniteAction`): recorded sha256 `86b051674e156ec6e9e1fb03030dde563663d336259e385aabe485661d9442fc` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build ReggeFiniteAction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ReggeFiniteAction.action` | yes | yes | yes | Quot.sound, propext | `#print axioms ReggeFiniteAction.action` |
| `ReggeFiniteAction.area_linearity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ReggeFiniteAction.area_linearity` |
| `ReggeFiniteAction.declared_areas_change_action` | yes | yes | yes | Quot.sound, propext | `#print axioms ReggeFiniteAction.declared_areas_change_action` |
| `ReggeFiniteAction.deficit_expansion` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ReggeFiniteAction.deficit_expansion` |
| `ReggeFiniteAction.flat_deficits_give_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ReggeFiniteAction.flat_deficits_give_zero` |
| `ReggeFiniteAction.same_deficit_area_split` | yes | yes | yes | propext | `#print axioms ReggeFiniteAction.same_deficit_area_split` |
| `ReggeFiniteAction.zero_action_does_not_imply_flat` | yes | yes | yes | Quot.sound, propext | `#print axioms ReggeFiniteAction.zero_action_does_not_imply_flat` |

- counts toward the grade: yes

### Python: `checks/independent/fsp-regge-deficit-action.py`

- file: [checks/independent/fsp-regge-deficit-action.py](../../../checks/independent/fsp-regge-deficit-action.py)
- sha256 (`bytes`): `9a72e9d17ea58b451d96a1b313791dfda8be923ab5f8d067e0e04ae2e40d27cf`
- cited in: record TFQ-1212
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1212_fsp_regge_deficit_action.md`

- file: [dag/derivations/26_fsp/tfq_1212_fsp_regge_deficit_action.md](../../../dag/derivations/26_fsp/tfq_1212_fsp_regge_deficit_action.md)
- sha256 (`lf-normalised`): `bd0fad0dafd79d0b01cc32d0a75389cd6dd331afc8cea8f89c22c2e3eff692be`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1212
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-regge-deficit-action.md`

- file: [dag/derivations/independent/fsp-regge-deficit-action.md](../../../dag/derivations/independent/fsp-regge-deficit-action.md)
- sha256 (`lf-normalised`): `f5d3b55bcb2acea1d442af4b1a1abecd13a8314a1e7e942acaf4756acb86c84d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-regge-deficit-action_lean_replay.json`

- file: [dag/research/campaign_fsp-regge-deficit-action_lean_replay.json](../../../dag/research/campaign_fsp-regge-deficit-action_lean_replay.json)
- sha256 (`lf-normalised`): `fdfc1d5bea996047431b34b41d5185ca6ed250b3d6758a2b75778ebbbe96ac71`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign.md)
- sha256 (`lf-normalised`): `5f5dfaa7a3794d1fee0299865df221b6db1c14ebf6f3925b1729e784a28e3194`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `3e88f1a70b66b0b90cc915acb5c802c118775e65cc8970af6c5a423f27ddd755`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-REGGE-DEFICIT-ACTION` `CONDITIONAL_ON_IMPORT`: [PGW-WDP-DEGREE-K-TORSION-BALANCE](PGW-WDP-DEGREE-K-TORSION-BALANCE.md) (PROVED_PROSE), [FSP-COBORDISM-INTRINSIC-SIGN](FSP-COBORDISM-INTRINSIC-SIGN.md) (OPEN)

Outgoing (1):

- `APP-R-FSP-DISCRETE-WDW-CONSTRAINT` `GAP_NO_DERIVATION`: [FSP-DISCRETE-WDW-CONSTRAINT](FSP-DISCRETE-WDW-CONSTRAINT.md) (OPEN)
