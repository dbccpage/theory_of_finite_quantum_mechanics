# OPS-AXIS1-WELLFOUNDED-ADMISSION

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Finite admission chain on three candidates. Candidate 0 has no predecessor. Candidate 1 names candidate 0 as its predecessor. Candidate 2 names candidate 1 as its predecessor. For every base assignment of boolean bits, admission of candidate 0 equals the base bit at candidate 0, admission of candidate 1 equals the disjunction of the base bit at candidate 1 with admission of candidate 0, and admission of candidate 2 equals the disjunction of the base bit at candidate 2 with admission of candidate 1. The base assignment that is false at each candidate admits none of the three. The base assignment that is true at candidate 0 and false at candidate 1 and at candidate 2 admits all three. The Genesis theorem collapsed_of_no_insts stays imported by name and is not re-run. The chain says nothing about other shapes of admission.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 15
- distinct cited Lean declarations covered by a current replay receipt: 15
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Genesis theorem collapsed_of_no_insts: with no base instance no rule instance is admitted (assumption; cited by name, not re-run)

## Bottleneck

Cited by name, not re-run. WDP-CH14 has no node in this graph; the closest node is the admission gate PGW-GO-ADMISSION-GATE, and no source relates the two. The finite chain is a separate checked case and does not re-run collapsed_of_no_insts.

## Source status

Ledger row L035-C1, status cited. Only a pinned copy of the Genesis claim ledger is in the source repository, and the note did not re-run it. This repository has not re-run it either.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignOpsAxis1WellfoundedAdmission.lean`

- file: [lean4/CampaignOpsAxis1WellfoundedAdmission.lean](../../../lean4/CampaignOpsAxis1WellfoundedAdmission.lean)
- sha256 (`bytes`): `48ae845d90038e03dbf566d022128a9d2a282563a0beacd84c587f5e7faa1b4d`
- cited in: node.source, receipt dag/research/campaign_ops-axis1-wellfounded-admission_lean_replay.json (CampaignOpsAxis1WellfoundedAdmission), record TFQ-2524
- replay: `verified`
  - receipt [dag/research/campaign_ops-axis1-wellfounded-admission_lean_replay.json](../../../dag/research/campaign_ops-axis1-wellfounded-admission_lean_replay.json) (module `CampaignOpsAxis1WellfoundedAdmission`): recorded sha256 `48ae845d90038e03dbf566d022128a9d2a282563a0beacd84c587f5e7faa1b4d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignOpsAxis1WellfoundedAdmission`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignOpsAxis1WellfoundedAdmission.adm0` | yes | yes | yes | propext | `#print axioms CampaignOpsAxis1WellfoundedAdmission.adm0` |
| `CampaignOpsAxis1WellfoundedAdmission.adm1` | yes | yes | yes | propext | `#print axioms CampaignOpsAxis1WellfoundedAdmission.adm1` |
| `CampaignOpsAxis1WellfoundedAdmission.adm2` | yes | yes | yes | propext | `#print axioms CampaignOpsAxis1WellfoundedAdmission.adm2` |
| `CampaignOpsAxis1WellfoundedAdmission.none0` | yes | yes | yes | propext | `#print axioms CampaignOpsAxis1WellfoundedAdmission.none0` |
| `CampaignOpsAxis1WellfoundedAdmission.none1` | yes | yes | yes | propext | `#print axioms CampaignOpsAxis1WellfoundedAdmission.none1` |
| `CampaignOpsAxis1WellfoundedAdmission.none2` | yes | yes | yes | propext | `#print axioms CampaignOpsAxis1WellfoundedAdmission.none2` |
| `CampaignOpsAxis1WellfoundedAdmission.pred0` | yes | yes | yes | propext | `#print axioms CampaignOpsAxis1WellfoundedAdmission.pred0` |
| `CampaignOpsAxis1WellfoundedAdmission.pred1` | yes | yes | yes | propext | `#print axioms CampaignOpsAxis1WellfoundedAdmission.pred1` |
| `CampaignOpsAxis1WellfoundedAdmission.pred2` | yes | yes | yes | propext | `#print axioms CampaignOpsAxis1WellfoundedAdmission.pred2` |
| `CampaignOpsAxis1WellfoundedAdmission.zb0` | yes | yes | yes | propext | `#print axioms CampaignOpsAxis1WellfoundedAdmission.zb0` |
| `CampaignOpsAxis1WellfoundedAdmission.zb1` | yes | yes | yes | propext | `#print axioms CampaignOpsAxis1WellfoundedAdmission.zb1` |
| `CampaignOpsAxis1WellfoundedAdmission.zb2` | yes | yes | yes | propext | `#print axioms CampaignOpsAxis1WellfoundedAdmission.zb2` |
| `CampaignOpsAxis1WellfoundedAdmission.zero0` | yes | yes | yes | propext | `#print axioms CampaignOpsAxis1WellfoundedAdmission.zero0` |
| `CampaignOpsAxis1WellfoundedAdmission.zero1` | yes | yes | yes | propext | `#print axioms CampaignOpsAxis1WellfoundedAdmission.zero1` |
| `CampaignOpsAxis1WellfoundedAdmission.zero2` | yes | yes | yes | propext | `#print axioms CampaignOpsAxis1WellfoundedAdmission.zero2` |

- counts toward the grade: yes

### Python: `checks/independent/ops-axis1-wellfounded-admission.py`

- file: [checks/independent/ops-axis1-wellfounded-admission.py](../../../checks/independent/ops-axis1-wellfounded-admission.py)
- sha256 (`bytes`): `54d781108232627123c6cb7612ce0a29e85d1e1427e77023a22a370066d214b7`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2524_ops_axis1_wellfounded_admission.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2524_ops_axis1_wellfounded_admission.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2524_ops_axis1_wellfounded_admission.md)
- sha256 (`lf-normalised`): `bbc96d4e80a832fd3066eae3a807470422f0e7560ada3fe3204c174afa640983`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2524
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/ops-axis1-wellfounded-admission.md`

- file: [dag/derivations/independent/ops-axis1-wellfounded-admission.md](../../../dag/derivations/independent/ops-axis1-wellfounded-admission.md)
- sha256 (`lf-normalised`): `6de34af34cafa774d1d0c2df22e7bd7fd4a70a5a522c588b7a215bcf925f7568`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_ops-axis1-wellfounded-admission_lean_replay.json`

- file: [dag/research/campaign_ops-axis1-wellfounded-admission_lean_replay.json](../../../dag/research/campaign_ops-axis1-wellfounded-admission_lean_replay.json)
- sha256 (`lf-normalised`): `da57f0471f372f7a85e819a45ad616c703e7a225d0e6dd6b151eb0bcb79bdcb3`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md`

- file: [sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md](../../../sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md)
- sha256 (`lf-normalised`): `da99779add73314574622d0db46ea4dfbc9b66c4938caf29ab98590033592ab4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md`

- file: [sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md](../../../sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md)
- sha256 (`lf-normalised`): `649532625cf9e8ec085a420fd1bad9227fcc4dae9f06ba02be1eb19f497e3ec7`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `OPS-R-AXIS1-WELLFOUNDED-ADMISSION` `GAP_NO_DERIVATION`: [PGW-GO-ADMISSION-GATE](PGW-GO-ADMISSION-GATE.md) (DEFINITION)

Outgoing (0):

