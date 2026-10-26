# AUTH-RICE-THEOREM-IMPORT

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> No total computable procedure is sound and complete for a nontrivial extensional property of the programs of a Turing-complete language (Rice 1953); the source cites the theorem with its hypotheses and does not formalize it.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 25
- distinct cited Lean declarations covered by a current replay receipt: 12
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Rice theorem for the programs of a Turing-complete language
- Mathlib Nat.Partrec.Code with ComputablePred.rice and rice₂

## Bottleneck

Rice's theorem for the programs of a Turing-complete language stays a citation. No declaration here states that no total computable procedure is sound and complete for a nontrivial extensional property. Mathlib ComputablePred.rice and rice₂ are not instantiated, and no semantic property of Nat.Partrec.Code is named. This three-code table does not decide an infinite language.

## Source status

papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md record AIT-5 claims cited; local formalization open; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignAuthRiceTheoremImport.lean`

- file: [lean4/CampaignAuthRiceTheoremImport.lean](../../../lean4/CampaignAuthRiceTheoremImport.lean)
- sha256 (`bytes`): `fa852f8f903aa8188f83b6d870d6b5ac32386698e7fe4b310936dda28697fd2f`
- cited in: node.lean, receipt dag/research/campaign_auth-rice-theorem-import_lean_replay.json (CampaignAuthRiceTheoremImport), record TFQ-1337
- replay: `verified`
  - receipt [dag/research/campaign_auth-rice-theorem-import_lean_replay.json](../../../dag/research/campaign_auth-rice-theorem-import_lean_replay.json) (module `CampaignAuthRiceTheoremImport`): recorded sha256 `fa852f8f903aa8188f83b6d870d6b5ac32386698e7fe4b310936dda28697fd2f` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignAuthRiceTheoremImport`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignAuthRiceTheoremImport.beh00` | yes | yes | yes | propext | `#print axioms CampaignAuthRiceTheoremImport.beh00` |
| `CampaignAuthRiceTheoremImport.beh01` | yes | yes | yes | propext | `#print axioms CampaignAuthRiceTheoremImport.beh01` |
| `CampaignAuthRiceTheoremImport.beh10` | yes | yes | yes | propext | `#print axioms CampaignAuthRiceTheoremImport.beh10` |
| `CampaignAuthRiceTheoremImport.beh11` | yes | yes | yes | propext | `#print axioms CampaignAuthRiceTheoremImport.beh11` |
| `CampaignAuthRiceTheoremImport.beh20` | yes | yes | yes | propext | `#print axioms CampaignAuthRiceTheoremImport.beh20` |
| `CampaignAuthRiceTheoremImport.beh21` | yes | yes | yes | propext | `#print axioms CampaignAuthRiceTheoremImport.beh21` |
| `CampaignAuthRiceTheoremImport.id0` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignAuthRiceTheoremImport.id0` |
| `CampaignAuthRiceTheoremImport.id1` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignAuthRiceTheoremImport.id1` |
| `CampaignAuthRiceTheoremImport.id2` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignAuthRiceTheoremImport.id2` |
| `CampaignAuthRiceTheoremImport.z0` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignAuthRiceTheoremImport.z0` |
| `CampaignAuthRiceTheoremImport.z1` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignAuthRiceTheoremImport.z1` |
| `CampaignAuthRiceTheoremImport.z2` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignAuthRiceTheoremImport.z2` |
| `beh00` | yes | yes | yes | propext | `#print axioms beh00` |
| `beh01` | yes | yes | yes | propext | `#print axioms beh01` |
| `beh10` | yes | yes | yes | propext | `#print axioms beh10` |
| `beh11` | yes | yes | yes | propext | `#print axioms beh11` |
| `beh20` | yes | yes | yes | propext | `#print axioms beh20` |
| `beh21` | yes | yes | yes | propext | `#print axioms beh21` |
| `id0` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms id0` |
| `id1` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms id1` |
| `id2` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms id2` |
| `z0` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms z0` |
| `z1` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms z1` |
| `z2` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms z2` |

- counts toward the grade: yes

### Python: `checks/independent/auth-rice-theorem-import.py`

- file: [checks/independent/auth-rice-theorem-import.py](../../../checks/independent/auth-rice-theorem-import.py)
- sha256 (`bytes`): `4cbd652df0398e081232c960b75d61d868f52e9ac040619cf1d4a6cb9d5a11fb`
- cited in: record TFQ-1337

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `check` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1337_auth_rice_theorem_import.md`

- file: [dag/derivations/29_computation/tfq_1337_auth_rice_theorem_import.md](../../../dag/derivations/29_computation/tfq_1337_auth_rice_theorem_import.md)
- sha256 (`lf-normalised`): `f8e394f304eaf4f851d437f4270e8037798d833b7748aba67cb9b3a17c0ecb22`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1337
- counts toward the grade: no

### Documents and data: `papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md`

- file: [papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md](../../../papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md)
- sha256 (`lf-normalised`): `4ca81b6ae8e724b54c7abf43ea951c119c2cff31a375e45cd7d79299adc7f70c`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/foundations/authorization_incompleteness/authorization_incompleteness_theory_claim_ledger.md`

- file: [papers/foundations/authorization_incompleteness/authorization_incompleteness_theory_claim_ledger.md](../../../papers/foundations/authorization_incompleteness/authorization_incompleteness_theory_claim_ledger.md)
- sha256 (`lf-normalised`): `28aa3a825d1b0296270b62f9a33a4a67b6c2a2d708028444a7f725ad46697feb`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/foundations/authorization_incompleteness/controlled_turing_derivation_series.md`

- file: [papers/foundations/authorization_incompleteness/controlled_turing_derivation_series.md](../../../papers/foundations/authorization_incompleteness/controlled_turing_derivation_series.md)
- sha256 (`lf-normalised`): `2573123162731ea63495b0ece777ae4b9e704e27b976fbc031df51c6f81c6f7b`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-AUTH-RICE-THEOREM-IMPORT` `CONDITIONAL_ON_IMPORT`: [AUTH-G5B-CARRIER-ADMISSION-GATE](AUTH-G5B-CARRIER-ADMISSION-GATE.md) (DEFINITION)

Outgoing (1):

- `APP-R-AUTH-G5-GLOBAL-COMPUTABILITY-LIFT` `GAP_NO_DERIVATION`: [AUTH-G5-GLOBAL-COMPUTABILITY-LIFT](AUTH-G5-GLOBAL-COMPUTABILITY-LIFT.md) (OPEN)
