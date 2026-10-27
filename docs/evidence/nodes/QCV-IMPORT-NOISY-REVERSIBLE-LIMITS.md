# QCV-IMPORT-NOISY-REVERSIBLE-LIMITS

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Aharonov, Ben-Or, Impagliazzo and Nisan (1996) show that noisy reversible or quantum computation with no supply of fresh low-entropy bits cannot preserve its input beyond a short depth; the result is cited, not re-proved or imported as a proof here.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 39
- distinct cited Lean declarations covered by a current replay receipt: 19
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- ABIN limitation theorem for noisy reversible computation without a fresh supply

## Bottleneck

The Aharonov, Ben-Or, Impagliazzo and Nisan limitation for noisy reversible or quantum computation with no fresh low-entropy supply stays a citation under that paper's own noise and depth hypotheses. These four integer pairs are not that theorem. They are not a trace norm, not a depolarizing channel, and not an independent per-qubit noise model. The history-distance product for global depolarizing noise stays on the noisy-history record.

## Source status

dag/research/quantum_computation_self_obstruction.md record QCV-IMP-ABIN claims IMPORTED_ASSUMPTION; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/NoisyReversibleLimitsImport.lean`

- file: [lean4/NoisyReversibleLimitsImport.lean](../../../lean4/NoisyReversibleLimitsImport.lean)
- sha256 (`bytes`): `69c64b7f9f295d3ac3d68ed779b807f6fb393afeab4370b1d385e2b83b73024e`
- cited in: node.lean, receipt dag/research/campaign_qcv-import-noisy-reversible-limits_lean_replay.json (NoisyReversibleLimitsImport), record TFQ-1321
- replay: `verified`
  - receipt [dag/research/campaign_qcv-import-noisy-reversible-limits_lean_replay.json](../../../dag/research/campaign_qcv-import-noisy-reversible-limits_lean_replay.json) (module `NoisyReversibleLimitsImport`): recorded sha256 `69c64b7f9f295d3ac3d68ed779b807f6fb393afeab4370b1d385e2b83b73024e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build NoisyReversibleLimitsImport`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `NoisyReversibleLimitsImport.below1` | yes | yes | yes | none | `#print axioms NoisyReversibleLimitsImport.below1` |
| `NoisyReversibleLimitsImport.below2` | yes | yes | yes | none | `#print axioms NoisyReversibleLimitsImport.below2` |
| `NoisyReversibleLimitsImport.below3` | yes | yes | yes | none | `#print axioms NoisyReversibleLimitsImport.below3` |
| `NoisyReversibleLimitsImport.u1` | yes | yes | yes | none | `#print axioms NoisyReversibleLimitsImport.u1` |
| `NoisyReversibleLimitsImport.u2` | yes | yes | yes | none | `#print axioms NoisyReversibleLimitsImport.u2` |
| `NoisyReversibleLimitsImport.u3` | yes | yes | yes | none | `#print axioms NoisyReversibleLimitsImport.u3` |
| `NoisyReversibleLimitsImport.u_step` | yes | yes | yes | none | `#print axioms NoisyReversibleLimitsImport.u_step` |
| `NoisyReversibleLimitsImport.u_zero` | yes | yes | yes | none | `#print axioms NoisyReversibleLimitsImport.u_zero` |
| `NoisyReversibleLimitsImport.v1` | yes | yes | yes | none | `#print axioms NoisyReversibleLimitsImport.v1` |
| `NoisyReversibleLimitsImport.v2` | yes | yes | yes | none | `#print axioms NoisyReversibleLimitsImport.v2` |
| `NoisyReversibleLimitsImport.v3` | yes | yes | yes | none | `#print axioms NoisyReversibleLimitsImport.v3` |
| `NoisyReversibleLimitsImport.v_step` | yes | yes | yes | none | `#print axioms NoisyReversibleLimitsImport.v_step` |
| `NoisyReversibleLimitsImport.v_zero` | yes | yes | yes | none | `#print axioms NoisyReversibleLimitsImport.v_zero` |
| `NoisyReversibleLimitsImport.w0_u` | yes | yes | yes | none | `#print axioms NoisyReversibleLimitsImport.w0_u` |
| `NoisyReversibleLimitsImport.w1` | yes | yes | yes | none | `#print axioms NoisyReversibleLimitsImport.w1` |
| `NoisyReversibleLimitsImport.w2` | yes | yes | yes | none | `#print axioms NoisyReversibleLimitsImport.w2` |
| `NoisyReversibleLimitsImport.w3` | yes | yes | yes | none | `#print axioms NoisyReversibleLimitsImport.w3` |
| `NoisyReversibleLimitsImport.w_step` | yes | yes | yes | none | `#print axioms NoisyReversibleLimitsImport.w_step` |
| `NoisyReversibleLimitsImport.w_zero` | yes | yes | yes | none | `#print axioms NoisyReversibleLimitsImport.w_zero` |
| `below1` | yes | yes | yes | none | `#print axioms below1` |
| `below2` | yes | yes | yes | none | `#print axioms below2` |
| `below3` | yes | yes | yes | none | `#print axioms below3` |
| `u1` | yes | yes | yes | none | `#print axioms u1` |
| `u2` | yes | yes | yes | none | `#print axioms u2` |
| `u3` | yes | yes | yes | none | `#print axioms u3` |
| `u_step` | yes | yes | yes | none | `#print axioms u_step` |
| `u_zero` | yes | yes | yes | none | `#print axioms u_zero` |
| `v1` | yes | yes | yes | none | `#print axioms v1` |
| `v2` | yes | yes | yes | none | `#print axioms v2` |
| `v3` | yes | yes | yes | none | `#print axioms v3` |
| `v_step` | yes | yes | yes | none | `#print axioms v_step` |
| `v_zero` | yes | yes | yes | none | `#print axioms v_zero` |
| `w0_u` | yes | yes | yes | none | `#print axioms w0_u` |
| `w1` | yes | yes | yes | none | `#print axioms w1` |
| `w2` | yes | yes | yes | none | `#print axioms w2` |
| `w3` | yes | yes | yes | none | `#print axioms w3` |
| `w_step` | yes | yes | yes | none | `#print axioms w_step` |
| `w_zero` | yes | yes | yes | none | `#print axioms w_zero` |

- counts toward the grade: yes

### Python: `checks/independent/qcv-import-noisy-reversible-limits.py`

- file: [checks/independent/qcv-import-noisy-reversible-limits.py](../../../checks/independent/qcv-import-noisy-reversible-limits.py)
- sha256 (`bytes`): `e63302be906e87895899c8ab3437ac87299f763396710847320faeaa0ca10c1b`
- cited in: record TFQ-1321

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `check` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1321_qcv_import_noisy_reversible_limits.md`

- file: [dag/derivations/29_computation/tfq_1321_qcv_import_noisy_reversible_limits.md](../../../dag/derivations/29_computation/tfq_1321_qcv_import_noisy_reversible_limits.md)
- sha256 (`lf-normalised`): `fa7190ec8fc18e04731dec996295edf8f6b8755d383aa507382c81c91bd6b5ed`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1321
- counts toward the grade: no

### Documents and data: `dag/research/quantum_computation_self_obstruction.md`

- file: [dag/research/quantum_computation_self_obstruction.md](../../../dag/research/quantum_computation_self_obstruction.md)
- sha256 (`lf-normalised`): `8ae1b2ae291ee74f773da07740ebd0c1f98842bc01d7ec6a4d3c267e0077d178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-QCV-IMPORT-NOISY-REVERSIBLE-LIMITS` `CONDITIONAL_ON_IMPORT`: [DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE](DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE.md) (OPEN)

Outgoing (1):

- `APP-R-QCV-NOISY-HISTORY-TRACE-DISTANCE-DECAY` `DERIVED_LEAN`: [QCV-NOISY-HISTORY-TRACE-DISTANCE-DECAY](QCV-NOISY-HISTORY-TRACE-DISTANCE-DECAY.md) (PROVED_LEAN)
