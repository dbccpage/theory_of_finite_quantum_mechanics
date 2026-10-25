# OPS-AXIS3-RELABELING

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Let Exp send each history to an export and let Vbar send each export to a verdict. Define V(H) as Vbar applied to Exp(H). If sigma is a function on histories and Exp(sigma(H)) equals Exp(H) for each history H, then V(sigma(H)) equals V(H) for each history H. One such export is the length of a list of natural numbers. The map that sends 0 to 1, sends 1 to 0, and sends each other natural number to itself leaves that length unchanged, so a verdict of the length is unchanged.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Hypotheses (i) NS-14 and (ii) CL-13 are cited, not re-run. Their Lean sources are not in this repository. The standing slice is the composition step: an export unchanged by sigma yields an unchanged verdict of that export, including list length under the map that swaps 0 with 1. Injectivity of sigma, a defect value, and whether a drop is a repair or a reinterpretation stay outside this slice. WDP-CH14 has no node in this graph. The unconditional form without an export hypothesis is node OPS-REFUTED-AXIS3-WIDE.

## Source status

Ledger row L035-C3: proved (conditional on (iii)) + cited. NS-14 and CL-13 are read from the Argon synthesis; their Lean sources are not in the source repository and were cited, not re-run.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignOpsAxis3Relabeling.lean`

- file: [lean4/CampaignOpsAxis3Relabeling.lean](../../../lean4/CampaignOpsAxis3Relabeling.lean)
- sha256 (`bytes`): `12ec56e7053207be28507d9f1b78b6a17cb124bd99e0b54a1371c79c5d0bada4`
- cited in: node.source, receipt dag/research/campaign_ops-axis3-relabeling_lean_replay.json (CampaignOpsAxis3Relabeling)
- replay: `verified`
  - receipt [dag/research/campaign_ops-axis3-relabeling_lean_replay.json](../../../dag/research/campaign_ops-axis3-relabeling_lean_replay.json) (module `CampaignOpsAxis3Relabeling`): recorded sha256 `12ec56e7053207be28507d9f1b78b6a17cb124bd99e0b54a1371c79c5d0bada4` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignOpsAxis3Relabeling`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `exportVerdictRelabel` | yes | yes | yes | none | `#print axioms exportVerdictRelabel` |
| `lengthMapInvariant` | yes | yes | yes | propext | `#print axioms lengthMapInvariant` |
| `lengthVerdictRelabel` | yes | yes | yes | propext | `#print axioms lengthVerdictRelabel` |

- counts toward the grade: yes

### Python: `checks/independent/ops-axis3-relabeling.py`

- file: [checks/independent/ops-axis3-relabeling.py](../../../checks/independent/ops-axis3-relabeling.py)
- sha256 (`bytes`): `7fd8f8fb6db09ed3556b917be4f557b5c32635d24c8a226dfc3e4c6ee7e7989d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2526_ops_axis3_relabeling.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2526_ops_axis3_relabeling.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2526_ops_axis3_relabeling.md)
- sha256 (`lf-normalised`): `fc04dfd320fd0fa0770aab53b3b6c42810df2716d29f1b6bc34e26da43088877`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2526
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/ops-axis3-relabeling.md`

- file: [dag/derivations/independent/ops-axis3-relabeling.md](../../../dag/derivations/independent/ops-axis3-relabeling.md)
- sha256 (`lf-normalised`): `1d83b99807ba29206c0565c6041fb5b88ec1c3592fb9ec810d42859f0c725090`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_ops-axis3-relabeling_lean_replay.json`

- file: [dag/research/campaign_ops-axis3-relabeling_lean_replay.json](../../../dag/research/campaign_ops-axis3-relabeling_lean_replay.json)
- sha256 (`lf-normalised`): `40edc4f8045dd6c792b19e06213edfc4d889dede96e5cc7fa35551e3817960fa`
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

- `OPS-R-AXIS3-RELABELING` `CONDITIONAL_ON_IMPORT`: [PGW-WDP-OBSERVER-QUOTIENT-PASSIVITY](PGW-WDP-OBSERVER-QUOTIENT-PASSIVITY.md) (DEFINITION)

Outgoing (3):

- `OPS-R-REFUTED-AXIS3-WIDE` `DERIVED_PROSE`: [OPS-REFUTED-AXIS3-WIDE](OPS-REFUTED-AXIS3-WIDE.md) (REFUTED)
- `OPS-R-REFUTED-NB9` `RECORD_PARENT`: [OPS-REFUTED-NB9](OPS-REFUTED-NB9.md) (REFUTED)
- `OPS-R-REGRESS-COROLLARY` `CONDITIONAL_ON_IMPORT`: [OPS-REGRESS-COROLLARY](OPS-REGRESS-COROLLARY.md) (CONDITIONAL)
