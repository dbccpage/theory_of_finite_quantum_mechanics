# MAJ-IMPORT-KITAEV-CHAIN

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For every natural number L with 2 \<= L and every natural number j with 1 \<= j and j \<= L - 1, the index 2 * j differs from 1 and from 2 * L, and the index 2 * j + 1 differs from 1 and from 2 * L. At L = 2 and j = 1, 2 * 1 = 2, 2 * 1 + 1 = 3, and 2 * 2 = 4, and 2 differs from 1 and from 4, and 3 differs from 1 and from 4. The integers t = 1, mu = 1 and delta = 1 satisfy mu * mu \< (2 * t) * (2 * t) and delta differs from 0. The integers t = 1, mu = 3 and delta = 1 fail mu * mu \< (2 * t) * (2 * t), and delta differs from 0.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 8
- distinct cited Lean declarations covered by a current replay receipt: 7
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Kitaev 2001 chain Hamiltonian and topological phase table

## Bottleneck

The fermion Hamiltonian, the BdG spectrum, the phase region as a physical claim, and a wire without disorder or trivial subgap states stay imported. The index split and the two integer comparisons are one finite reading of the sweet-spot labels and the stated bound. They do not select a topological phase.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-C6 claims DEFINITION; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignMajImportKitaevChain.lean`

- file: [lean4/CampaignMajImportKitaevChain.lean](../../../lean4/CampaignMajImportKitaevChain.lean)
- sha256 (`bytes`): `4be2d26217c40beea3ab808e5140bd95ff3aef37867556343ea2d9c18b582585`
- cited in: node.lean, receipt dag/research/campaign_maj-import-kitaev-chain_lean_replay.json (CampaignMajImportKitaevChain), record TFQ-1167
- replay: `verified`
  - receipt [dag/research/campaign_maj-import-kitaev-chain_lean_replay.json](../../../dag/research/campaign_maj-import-kitaev-chain_lean_replay.json) (module `CampaignMajImportKitaevChain`): recorded sha256 `4be2d26217c40beea3ab808e5140bd95ff3aef37867556343ea2d9c18b582585` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignMajImportKitaevChain`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignMajImportKitaevChain.edgeAbsent` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajImportKitaevChain.edgeAbsent` |
| `CampaignMajImportKitaevChain.edgeWitness` | yes | yes | yes | none | `#print axioms CampaignMajImportKitaevChain.edgeWitness` |
| `CampaignMajImportKitaevChain.insidePoint` | yes | yes | yes | none | `#print axioms CampaignMajImportKitaevChain.insidePoint` |
| `CampaignMajImportKitaevChain.outsidePoint` | yes | yes | yes | none | `#print axioms CampaignMajImportKitaevChain.outsidePoint` |

- counts toward the grade: yes

### Lean: `papers/core/majorana/lean4/MajoranaCore.lean`

- file: [papers/core/majorana/lean4/MajoranaCore.lean](../../../papers/core/majorana/lean4/MajoranaCore.lean)
- sha256 (`bytes`): `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071`
- cited in: node.lean, record TFQ-1167
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_majorana.json](../../../dag/research/lean_replay_campaign_majorana.json) (module `papers.core.majorana.lean4.MajoranaCore`): recorded sha256 `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `KitaevSweetSpotChain` | yes | yes | yes | module-level | `#print axioms KitaevSweetSpotChain` |
| `disjoint_majorana_pair_commute` | yes | yes | yes | module-level | `#print axioms disjoint_majorana_pair_commute` |
| `mzm_boundary_decoupling` | yes | yes | yes | module-level | `#print axioms mzm_boundary_decoupling` |

- counts toward the grade: yes

### Python: `papers/core/majorana/code/majorana_evaluator.py`

- file: [papers/core/majorana/code/majorana_evaluator.py](../../../papers/core/majorana/code/majorana_evaluator.py)
- sha256 (`bytes`): `86798eabea510363b59e164c516625c6055df24b4e12086cfe2fde5db16835c3`
- cited in: record TFQ-1167

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `KitaevSweetSpotChain` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1167_maj_import_kitaev_chain.md`

- file: [dag/derivations/28_majorana/tfq_1167_maj_import_kitaev_chain.md](../../../dag/derivations/28_majorana/tfq_1167_maj_import_kitaev_chain.md)
- sha256 (`lf-normalised`): `6e7890e727a3f97b52cc43d6dae878e6eb1c81b4d9bd51cd20e58e27017cdb4d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1167
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `e92416bb1739e51de20a8ad6a26d4b5f3d76b974d7556507b13149b29e8edb47`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/majorana/the_majorana_problem_claim_ledger.md`

- file: [papers/core/majorana/the_majorana_problem_claim_ledger.md](../../../papers/core/majorana/the_majorana_problem_claim_ledger.md)
- sha256 (`lf-normalised`): `2d2b91881568780f56d7cdb53c97eec42bbfa09c21b2f1c6302665a79aad7565`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-IMPORT-KITAEV-CHAIN` `CONDITIONAL_ON_IMPORT`: [DS-QM212-MAJORANA-PROBLEM](DS-QM212-MAJORANA-PROBLEM.md) (PROVED_LEAN), [MAJ-HARDWARE-NARRATIVE-QUARANTINE](MAJ-HARDWARE-NARRATIVE-QUARANTINE.md) (DEFINITION)

Outgoing (2):

- `APP-R-MAJ-KITAEV-EDGE-INDEX-DISJOINT` `DERIVED_LEAN`: [MAJ-KITAEV-EDGE-INDEX-DISJOINT](MAJ-KITAEV-EDGE-INDEX-DISJOINT.md) (PROVED_LEAN)
- `APP-R-MAJ-KITAEV-SWEETSPOT-EXACT` `COMPUTED`: [MAJ-KITAEV-SWEETSPOT-EXACT](MAJ-KITAEV-SWEETSPOT-EXACT.md) (COMPUTATIONALLY_CHECKED)
