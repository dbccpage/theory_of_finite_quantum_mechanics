# MAJ-IMPORT-KITAEV-CHAIN

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The spinless p-wave Kitaev chain H = -sum(t c_j^dag c_{j+1} + Delta c_j c_{j+1} + h.c.) - mu sum(c_j^dag c_j - 1/2), its BdG spectrum, the phase region |mu| \< 2t with Delta nonzero, and the sweet-spot form H = -i t sum gamma_{2j} gamma_{2j+1} with free edge modes gamma_1, gamma_{2L} are imported models.

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

### Python: `code/python/src/majorana/majorana_mzm_ising.py`

- file: [code/python/src/majorana/majorana_mzm_ising.py](../../../code/python/src/majorana/majorana_mzm_ising.py)
- sha256 (`bytes`): `a4ac5734a5ab1a872aeaafd3835ed71261f069dfb29c17c9b5572a03e63b1310`
- cited in: record TFQ-1167

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `KitaevSweetSpotChain` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1167_maj_import_kitaev_chain.md`

- file: [dag/derivations/28_majorana/tfq_1167_maj_import_kitaev_chain.md](../../../dag/derivations/28_majorana/tfq_1167_maj_import_kitaev_chain.md)
- sha256 (`lf-normalised`): `ba0e5dfbde1c43613cb312be2f20406febcf237973389d68575345d70ca7d5a4`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1167
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `2f55c0f24f87388cfa9d7a4a7d832f34c0fa30b857d344811f4336f634c1684b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/majorana/the_majorana_problem_claim_ledger.md`

- file: [papers/core/majorana/the_majorana_problem_claim_ledger.md](../../../papers/core/majorana/the_majorana_problem_claim_ledger.md)
- sha256 (`lf-normalised`): `37cc191a881cbb0f8fb52e30c2b865f9e9e70e235b4530df7bdd7d1b5728cb86`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-IMPORT-KITAEV-CHAIN` `CONDITIONAL_ON_IMPORT`: [DS-QM212-MAJORANA-PROBLEM](DS-QM212-MAJORANA-PROBLEM.md) (PROVED_LEAN), [MAJ-HARDWARE-NARRATIVE-QUARANTINE](MAJ-HARDWARE-NARRATIVE-QUARANTINE.md) (DEFINITION)

Outgoing (2):

- `APP-R-MAJ-KITAEV-EDGE-INDEX-DISJOINT` `DERIVED_LEAN`: [MAJ-KITAEV-EDGE-INDEX-DISJOINT](MAJ-KITAEV-EDGE-INDEX-DISJOINT.md) (PROVED_LEAN)
- `APP-R-MAJ-KITAEV-SWEETSPOT-EXACT` `COMPUTED`: [MAJ-KITAEV-SWEETSPOT-EXACT](MAJ-KITAEV-SWEETSPOT-EXACT.md) (COMPUTATIONALLY_CHECKED)
