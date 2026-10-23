# DFM-TREE-CHORD-COORDINATES

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the triangle graph with tree edges 01, 12 and chord 02, for rational 2x2 matrices with right inverses and an anchored gauge (1, G1, G2), the rooted tree dressing sends both gauged tree links to the identity and sends the gauged chord to U02 U12^{-1} U01^{-1}, the ungauged rooted cycle holonomy.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The general bijection (u_T on V minus the root, dressed chords) \<-\> H^{|E|} for every finite connected graph and group is stated in the dossier without proof and is not in Lean; the general neutralization and residual statements are TFQ-0398 and TFQ-0399.

## Source status

papers/ravera_dfm_dossier.md record DFM-DEF-2.2-COORDS claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/RaveraDfmFiniteToContinuum.lean`

- file: [lean4/RaveraDfmFiniteToContinuum.lean](../../../lean4/RaveraDfmFiniteToContinuum.lean)
- sha256 (`bytes`): `70687535990869370ddb6ec8b17a080e48992047692f26fbb478703b631c1cdf`
- cited in: node.lean, node.source, record TFQ-1100
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_dressing_field.json](../../../dag/research/lean_replay_campaign_dressing_field.json) (module `RaveraDfmFiniteToContinuum`): recorded sha256 `70687535990869370ddb6ec8b17a080e48992047692f26fbb478703b631c1cdf` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build RaveraDfmFiniteToContinuum`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `mat2_mul_assoc` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms mat2_mul_assoc` |
| `spanning_tree_nonabelian_mat2_factorization` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms spanning_tree_nonabelian_mat2_factorization` |
- counts toward the grade: yes

### Python: `code/python/src/qm/ravera_dfm.py`

- file: [code/python/src/qm/ravera_dfm.py](../../../code/python/src/qm/ravera_dfm.py)
- sha256 (`bytes`): `42e89a39e29b524dbca2b39adff5c8fc4d12161266116f60314134dbf827f4aa`
- cited in: record TFQ-1100

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_pillar2_nonabelian_borel_two_stage_dfm` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_1100_dfm_tree_chord_coordinates.md`

- file: [dag/derivations/24_dressing_field/tfq_1100_dfm_tree_chord_coordinates.md](../../../dag/derivations/24_dressing_field/tfq_1100_dfm_tree_chord_coordinates.md)
- sha256 (`lf-normalised`): `babde2f29e3c40f93a89beedd6c19da373c63a6e5b024b47d2ea0297b07c707c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1100
- counts toward the grade: no

### Documents and data: `papers/ravera_dfm_dossier.md`

- file: [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- sha256 (`lf-normalised`): `76ae630ecb514d278773cdf5ea98ce77c80d8f969d1326f1b55e6772d13afcaa`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-TREE-CHORD-COORDINATES` `DERIVED_LEAN`: [DFM-GENERAL-GRAPH-DRESSING](DFM-GENERAL-GRAPH-DRESSING.md) (PROVED_LEAN), [DFM-TREE-CHANGE](DFM-TREE-CHANGE.md) (PROVED_LEAN)

Outgoing (0):

