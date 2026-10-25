# AUTHF-CARRIER-ADMISSION-GATE

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On this closed slice the record admission status is the string open. The direct candidate identifier is AIT-DTM0, its admission status is partial, its syntax-and-encoding status is partial, its execution-semantics status is partial, and its universality status is open. The direct candidate selected flag is false.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Adequacy, replay closure, extensionality, nontriviality and effective reduction stay outside this slice. The other three candidate identifiers stay outside it. A frozen carrier and a Rice-style claim stay open. The structural validator over the whole JSON record stays with the cited Python check.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record AUTHF-24 claims OPEN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignAuthfCarrierAdmissionGate.lean`

- file: [lean4/CampaignAuthfCarrierAdmissionGate.lean](../../../lean4/CampaignAuthfCarrierAdmissionGate.lean)
- sha256 (`bytes`): `4d9d32925fcb9b6f7ad1ae2c386d7057081e6effd49c6a52c8656b6059172c23`
- cited in: node.lean, receipt dag/research/campaign_authf-carrier-admission-gate_lean_replay.json (CampaignAuthfCarrierAdmissionGate), receipt dag/research/pr_372_review_replay.json (CampaignAuthfCarrierAdmissionGate), record TFQ-1362
- replay: `verified`
  - receipt [dag/research/campaign_authf-carrier-admission-gate_lean_replay.json](../../../dag/research/campaign_authf-carrier-admission-gate_lean_replay.json) (module `CampaignAuthfCarrierAdmissionGate`): recorded sha256 `4d9d32925fcb9b6f7ad1ae2c386d7057081e6effd49c6a52c8656b6059172c23` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr_372_review_replay.json](../../../dag/research/pr_372_review_replay.json) (module `CampaignAuthfCarrierAdmissionGate`): recorded sha256 `4d9d32925fcb9b6f7ad1ae2c386d7057081e6effd49c6a52c8656b6059172c23` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignAuthfCarrierAdmissionGate`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignAuthfCarrierAdmissionGate.directCeilings` | yes | yes | yes | none | `#print axioms CampaignAuthfCarrierAdmissionGate.directCeilings` |
| `CampaignAuthfCarrierAdmissionGate.directNotSelected` | yes | yes | yes | none | `#print axioms CampaignAuthfCarrierAdmissionGate.directNotSelected` |
| `directCeilings` | yes | yes | yes | none | `#print axioms directCeilings` |
| `directNotSelected` | yes | yes | yes | none | `#print axioms directNotSelected` |
- counts toward the grade: yes

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
- sha256 (`lf-normalised`): `6e9be85012000298cfdda54958c0d8881a97731d3851897128bb82e12305828f`
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

