# AUTHF-CARRIER-ADMISSION-GATE

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `OPEN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The recovered candidate record stays globally open: for AIT-DTM0 only syntax, execution semantics, adequacy and replay closure are partial and universality, extensionality, nontriviality and effective reduction are open, and PO-022, PO-023 and AIT-PACKET4 are open; the validator refuses any selection or admission.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

A carrier with syntax, execution, simulation, an extensional property with encoded witnesses, an effective reduction and a replay boundary must be frozen before any Rice-style claim.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record AUTHF-24 claims OPEN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `code/python/src/qm/auth_incompleteness/carrier_candidates.py`

- file: [code/python/src/qm/auth_incompleteness/carrier_candidates.py](../../../code/python/src/qm/auth_incompleteness/carrier_candidates.py)
- sha256 (`bytes`): `353a2b52526861d5861dde36fe9fb6cae27ae0a3772ad38c9df1b251e5a347fe`
- cited in: node.source, record TFQ-1362

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `mutation_cases` (python_symbol) | yes | yes | yes | - | - |
| `validate_record` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/tests/test_auth_incompleteness_candidates.py`

- file: [code/python/tests/test_auth_incompleteness_candidates.py](../../../code/python/tests/test_auth_incompleteness_candidates.py)
- sha256 (`bytes`): `34d6ab470ae90bad38aedfbb15c9412128372f04fce22c4d75a3c2f3584b3062`
- cited in: record TFQ-1362
- check: `python -m pytest code/python/tests/test_auth_incompleteness_candidates.py::test_record_is_globally_open_and_selects_nothing`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_record_is_globally_open_and_selects_nothing` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/test_auth_incompleteness_candidates.py::test_record_is_globally_open_and_selects_nothing` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1362_authf_carrier_admission_gate.md`

- file: [dag/derivations/29_computation/tfq_1362_authf_carrier_admission_gate.md](../../../dag/derivations/29_computation/tfq_1362_authf_carrier_admission_gate.md)
- sha256 (`lf-normalised`): `0a6293022c0501393dcae76d616663e3b8bb723894dae33d14dd1f869d390b08`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1362
- counts toward the grade: no

### Documents and data: `papers/foundations/authorization_incompleteness/evidence/original/computability_carrier_candidates.json`

- file: [papers/foundations/authorization_incompleteness/evidence/original/computability_carrier_candidates.json](../../../papers/foundations/authorization_incompleteness/evidence/original/computability_carrier_candidates.json)
- sha256 (`lf-normalised`): `8f951b3afd30a62ffe0a6e667b8a171ee513e821cb75bc3aaa0552eca0c39f29`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-AUTHF-CARRIER-ADMISSION-GATE` `GAP_NO_DERIVATION`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION)

Outgoing (0):

