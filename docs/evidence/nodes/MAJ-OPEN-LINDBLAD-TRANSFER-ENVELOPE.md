# MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For four MZMs under a Lindblad braiding model with gap Delta, length L/xi and poisoning rate Gamma_qp \> 0, the trace-norm transfer defect obeys Delta_transfer(T) \<= min(1, C_LZ (hbar/(Delta T))^2 + (Delta/hbar) e^{-L/xi} T + 1 - e^{-Gamma_qp T}) for T \>\> hbar/Delta, and that envelope has a positive minimum.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 5
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

### Lean: `lean4/MajoranaOpenLindbladTransferEnvelope.lean`

- file: [lean4/MajoranaOpenLindbladTransferEnvelope.lean](../../../lean4/MajoranaOpenLindbladTransferEnvelope.lean)
- sha256 (`bytes`): `155e98450ce628f679f85c171e9bc0f323c8199e695b94085d32a4ba9c8af079`
- cited in: node.lean, receipt dag/research/campaign_maj-open-lindblad-transfer-envelope_lean_replay.json (MajoranaOpenLindbladTransferEnvelope), receipt dag/research/pr_360_review_replay.json (MajoranaOpenLindbladTransferEnvelope), record TFQ-1177
- replay: `verified`
  - receipt [dag/research/campaign_maj-open-lindblad-transfer-envelope_lean_replay.json](../../../dag/research/campaign_maj-open-lindblad-transfer-envelope_lean_replay.json) (module `MajoranaOpenLindbladTransferEnvelope`): recorded sha256 `155e98450ce628f679f85c171e9bc0f323c8199e695b94085d32a4ba9c8af079` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr_360_review_replay.json](../../../dag/research/pr_360_review_replay.json) (module `MajoranaOpenLindbladTransferEnvelope`): recorded sha256 `155e98450ce628f679f85c171e9bc0f323c8199e695b94085d32a4ba9c8af079` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build MajoranaOpenLindbladTransferEnvelope`

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
- sha256 (`lf-normalised`): `c572f6ec9d7f6f31c18249f961648ab0d61a0df08442f366a8b4a5cbaa113cec`
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
- sha256 (`lf-normalised`): `81862bd19af6b166d221adc65dcaa408176237798809de1857f7239e995dca92`
- cited in: node.source
- counts toward the grade: yes

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

- `APP-R-MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE` `GAP_NO_DERIVATION`: [MAJ-REALIZATION-PACKET-GAP](MAJ-REALIZATION-PACKET-GAP.md) (DEFINITION), [MAJ-HARDWARE-NARRATIVE-QUARANTINE](MAJ-HARDWARE-NARRATIVE-QUARANTINE.md) (DEFINITION)

Outgoing (3):

- `APP-R-MAJ-ENVELOPE-NAT-ARITHMETIC` `DERIVED_LEAN`: [MAJ-ENVELOPE-NAT-ARITHMETIC](MAJ-ENVELOPE-NAT-ARITHMETIC.md) (PROVED_LEAN)
- `APP-R-MAJ-OPEN-MULTITERMINAL-ENVELOPE` `GAP_NO_DERIVATION`: [MAJ-OPEN-MULTITERMINAL-ENVELOPE](MAJ-OPEN-MULTITERMINAL-ENVELOPE.md) (OPEN)
- `APP-R-MAJ-OPEN-NON-MARKOVIAN-ENVELOPE` `GAP_NO_DERIVATION`: [MAJ-OPEN-NON-MARKOVIAN-ENVELOPE](MAJ-OPEN-NON-MARKOVIAN-ENVELOPE.md) (OPEN)
