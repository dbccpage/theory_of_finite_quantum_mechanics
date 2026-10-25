# AUTHF-DTM0-SIMULATION-OPEN

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `OPEN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> DTM0 has no simulation theorem, no machine that runs encoded machines, no input or configuration encoding, no parser-to-execution agreement and no equivalence with Mathlib's Turing.TM0 or with Nat.Partrec.Code; its fuel-bounded evaluator decides only bounded runs.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

A faithful comparison needs a finite-support tape restriction, the stay move split into Mathlib's move-or-write statements, and a halting predicate such as exists fuel with execute returning halted.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record AUTHF-26 claims OPEN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `code/python/src/qm/auth_incompleteness/finite_models.py`

- file: [code/python/src/qm/auth_incompleteness/finite_models.py](../../../code/python/src/qm/auth_incompleteness/finite_models.py)
- sha256 (`bytes`): `ff6008a75c55f6fa8b55fb5889835109ea58f61355d9b09702e701cdf92ced97`
- cited in: record TFQ-1364

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `execute` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1364_authf_dtm0_simulation_open.md`

- file: [dag/derivations/29_computation/tfq_1364_authf_dtm0_simulation_open.md](../../../dag/derivations/29_computation/tfq_1364_authf_dtm0_simulation_open.md)
- sha256 (`lf-normalised`): `0ea11217026b9c84fdc16e4f90b48ef8d903651d99fb3fa3fa56f385ee634372`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1364
- counts toward the grade: no

### Documents and data: `papers/foundations/authorization_incompleteness/evidence/original/computability_carrier_candidates.json`

- file: [papers/foundations/authorization_incompleteness/evidence/original/computability_carrier_candidates.json](../../../papers/foundations/authorization_incompleteness/evidence/original/computability_carrier_candidates.json)
- sha256 (`lf-normalised`): `8f951b3afd30a62ffe0a6e667b8a171ee513e821cb75bc3aaa0552eca0c39f29`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-AUTHF-DTM0-SIMULATION-OPEN` `GAP_NO_DERIVATION`: [AUTHF-DTM0-RULE-MACHINE](AUTHF-DTM0-RULE-MACHINE.md) (DEFINITION), [PGW-RUNS-PAST-DECLARED-BOUNDS](PGW-RUNS-PAST-DECLARED-BOUNDS.md) (OPEN)

Outgoing (0):

