# MAJ-ISING-BRAID-EXACT-OPEN

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `OPEN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For B1 = R and B2 = F R F over Q(zeta16), B1 B2 B1 = B2 B1 B2, F^2 = I and the hexagon equations hold as exact identities.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Run the identities in exact cyclotomic arithmetic; the paper code checks only Yang-Baxter in floating point.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-ISING-BRAID-CHECK claims COMPUTATIONALLY_CHECKED; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `papers/core/majorana/code/majorana_evaluator.py`

- file: [papers/core/majorana/code/majorana_evaluator.py](../../../papers/core/majorana/code/majorana_evaluator.py)
- sha256 (`bytes`): `86798eabea510363b59e164c516625c6055df24b4e12086cfe2fde5db16835c3`
- cited in: record TFQ-1171

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `IsingFusionAlgebra.verify_quantum_dimensions` (python_symbol) | yes | yes | yes | - | - |
| `IsingFusionAlgebra.verify_yang_baxter_braid` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py`

- file: [papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py](../../../papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py)
- sha256 (`bytes`): `3389fbeaad7f67b996a8bc8aa2cef6d2ae1ae841d8b6cfa83564a3305190a60b`
- cited in: record TFQ-1171
- check: `python -m pytest papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py::test_ising_fusion_and_braid_relations`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_ising_fusion_and_braid_relations` (python_test) | yes | yes | yes | - | `python -m pytest papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py::test_ising_fusion_and_braid_relations` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1171_maj_ising_braid_exact_open.md`

- file: [dag/derivations/28_majorana/tfq_1171_maj_ising_braid_exact_open.md](../../../dag/derivations/28_majorana/tfq_1171_maj_ising_braid_exact_open.md)
- sha256 (`lf-normalised`): `d1ce22d98187bb3906574ac789bf033b04ba71e9f5266724bb23c3845c3c24fc`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1171
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

- `APP-R-MAJ-ISING-BRAID-EXACT-OPEN` `GAP_NO_DERIVATION`: [MAJ-IMPORT-ISING-ANYONS](MAJ-IMPORT-ISING-ANYONS.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

