# MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Narrowed boundary, status left OPEN. For the integer envelope f(T) = 4 + T^3 and the comparison 3 T^2, f(1) = 5 which is greater than 3, f(2) = 12 which equals 12, and f(3) = 31 which is greater than 27. The value 12 is positive, and 0 is strictly below 12, so a positive envelope value does not force a transfer defect to be positive.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The Lindblad derivation, the four-mode braiding model, the exponential poisoning term, the Landau-Zener square, and a positive lower bound on the physical transfer defect stay open. Older Nat positivity facts in MajoranaCore do not state this envelope. A positive envelope value stays separate from a positive transfer defect.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-C18 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignMajOpenLindbladTransferEnvelope.lean`

- file: [lean4/CampaignMajOpenLindbladTransferEnvelope.lean](../../../lean4/CampaignMajOpenLindbladTransferEnvelope.lean)
- sha256 (`bytes`): `0f2c5315fbd195a186e8f03a1336639adf6d2d5aed2709fb2756ac2fd5af5c2e`
- cited in: node.lean, receipt dag/research/campaign_maj-open-lindblad-transfer-envelope_lean_replay.json (CampaignMajOpenLindbladTransferEnvelope), record TFQ-1177
- replay: `verified`
  - receipt [dag/research/campaign_maj-open-lindblad-transfer-envelope_lean_replay.json](../../../dag/research/campaign_maj-open-lindblad-transfer-envelope_lean_replay.json) (module `CampaignMajOpenLindbladTransferEnvelope`): recorded sha256 `0f2c5315fbd195a186e8f03a1336639adf6d2d5aed2709fb2756ac2fd5af5c2e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignMajOpenLindbladTransferEnvelope`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `defect_zero_below_envelope` | yes | yes | yes | none | `#print axioms defect_zero_below_envelope` |
| `envelope_at_one` | yes | yes | yes | none | `#print axioms envelope_at_one` |
| `envelope_at_three` | yes | yes | yes | none | `#print axioms envelope_at_three` |
| `envelope_at_two` | yes | yes | yes | none | `#print axioms envelope_at_two` |
| `envelope_positive` | yes | yes | yes | none | `#print axioms envelope_positive` |
- counts toward the grade: yes

### Python: `checks/independent/maj-open-lindblad-transfer-envelope.py`

- file: [checks/independent/maj-open-lindblad-transfer-envelope.py](../../../checks/independent/maj-open-lindblad-transfer-envelope.py)
- sha256 (`bytes`): `4b5e0d0edff88df5c18227efc6547ccb24a8f2cdc89b3de4cbb34e169705a9ac`
- cited in: record TFQ-1177
- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1177_maj_open_lindblad_transfer_envelope.md`

- file: [dag/derivations/28_majorana/tfq_1177_maj_open_lindblad_transfer_envelope.md](../../../dag/derivations/28_majorana/tfq_1177_maj_open_lindblad_transfer_envelope.md)
- sha256 (`lf-normalised`): `2b9116f9a4c03618fc7b165fcc9cacd802f6c43536198eaf61b538af2debd6a8`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1177
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/maj-open-lindblad-transfer-envelope.md`

- file: [dag/derivations/independent/maj-open-lindblad-transfer-envelope.md](../../../dag/derivations/independent/maj-open-lindblad-transfer-envelope.md)
- sha256 (`lf-normalised`): `9e4a520bfbc0740a3e0875e9d821707ae49c7dca9ce757638b9dc3b38a08822b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_maj-open-lindblad-transfer-envelope_lean_replay.json`

- file: [dag/research/campaign_maj-open-lindblad-transfer-envelope_lean_replay.json](../../../dag/research/campaign_maj-open-lindblad-transfer-envelope_lean_replay.json)
- sha256 (`lf-normalised`): `887d95db7653b850296d2d03322ad2de6ffd4327b6a9197ea3a23ea9352f6c21`
- cited in: node.source
- counts toward the grade: yes

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

- `APP-R-MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE` `GAP_NO_DERIVATION`: [MAJ-REALIZATION-PACKET-GAP](MAJ-REALIZATION-PACKET-GAP.md) (DEFINITION), [MAJ-HARDWARE-NARRATIVE-QUARANTINE](MAJ-HARDWARE-NARRATIVE-QUARANTINE.md) (DEFINITION)

Outgoing (3):

- `APP-R-MAJ-ENVELOPE-NAT-ARITHMETIC` `DERIVED_LEAN`: [MAJ-ENVELOPE-NAT-ARITHMETIC](MAJ-ENVELOPE-NAT-ARITHMETIC.md) (PROVED_LEAN)
- `APP-R-MAJ-OPEN-MULTITERMINAL-ENVELOPE` `GAP_NO_DERIVATION`: [MAJ-OPEN-MULTITERMINAL-ENVELOPE](MAJ-OPEN-MULTITERMINAL-ENVELOPE.md) (OPEN)
- `APP-R-MAJ-OPEN-NON-MARKOVIAN-ENVELOPE` `GAP_NO_DERIVATION`: [MAJ-OPEN-NON-MARKOVIAN-ENVELOPE](MAJ-OPEN-NON-MARKOVIAN-ENVELOPE.md) (OPEN)
