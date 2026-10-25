# MAJ-IMPORT-KITAEV-CHAIN

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The spinless p-wave Kitaev chain H = -sum(t c_j^dag c_{j+1} + Delta c_j c_{j+1} + h.c.) - mu sum(c_j^dag c_j - 1/2), its BdG spectrum, the phase region |mu| \< 2t with Delta nonzero, and the sweet-spot form H = -i t sum gamma_{2j} gamma_{2j+1} with free edge modes gamma_1, gamma_{2L} are imported models.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declaration references covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Kitaev 2001 chain Hamiltonian and topological phase table

## Bottleneck

No statement that a physical wire realizes this Hamiltonian without disorder or trivial subgap states is made or supported.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-C6 claims DEFINITION; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

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
- sha256 (`lf-normalised`): `86a798d5e3c1fc5b7afd59a3d1d9b5d13c4fe917b6cd6cb75ddc858b81408a51`
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
