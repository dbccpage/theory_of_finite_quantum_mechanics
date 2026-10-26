# OPS-AXIS3-RELABELING

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Axis 3 of WDP-CH14-T01 under three hypotheses. (i) NS-14: an injective renaming sigma of presentation tokens commutes with the transition step and with full-history replay. (ii) CL-13 (passage_charge_const): a quantity conserved by internal transitions is constant on reachable states and equals its genesis value. (iii) The verdict V reads a history only through a declared export Exp, so V = Vbar o Exp, with Exp(sigma(H)) = Exp(H) for every injective renaming sigma; this is the identical-accessible-exports premise of Proposition 3.1 of the Argon synthesis. Then V(sigma(H)) = V(H), because V(sigma(H)) = Vbar(Exp(sigma(H))) = Vbar(Exp(H)) = V(H). Without (iii) the statement is false (node OPS-REFUTED-AXIS3-WIDE). A drop in the internal defect Delta_O stays computable and renaming-invariant; whether a drop is a repair or a reinterpretation is a question about the grounding map of the tokens, which no export-reading verdict decides.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Hypotheses (i) NS-14 and (ii) CL-13 are cited, not re-run. Their Lean sources are not in this repository. The checked slice is the composition step: an export unchanged by sigma yields an unchanged verdict of that export, including list length under the map that swaps 0 with 1. Injectivity of sigma, a defect value, and whether a drop is a repair or a reinterpretation stay outside this slice. WDP-CH14 has no node in this graph. The unconditional form without an export hypothesis is node OPS-REFUTED-AXIS3-WIDE.

## Source status

Ledger row L035-C3: proved (conditional on (iii)) + cited. NS-14 and CL-13 are read from the Argon synthesis; their Lean sources are not in the source repository and were cited, not re-run.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignOpsAxis3Relabeling.lean`

- file: [lean4/CampaignOpsAxis3Relabeling.lean](../../../lean4/CampaignOpsAxis3Relabeling.lean)
- sha256 (`bytes`): `8f6cc92938943a0dd559263f075aa7496c2bb25fab1db596f18a5fc078c01150`
- cited in: node.source, receipt dag/research/campaign_ops-axis3-relabeling_lean_replay.json (CampaignOpsAxis3Relabeling), receipt dag/research/pr_387_round2_replay.json (CampaignOpsAxis3Relabeling), record TFQ-2526
- replay: `verified`
  - receipt [dag/research/campaign_ops-axis3-relabeling_lean_replay.json](../../../dag/research/campaign_ops-axis3-relabeling_lean_replay.json) (module `CampaignOpsAxis3Relabeling`): recorded sha256 `8f6cc92938943a0dd559263f075aa7496c2bb25fab1db596f18a5fc078c01150` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
  - receipt [dag/research/pr_387_round2_replay.json](../../../dag/research/pr_387_round2_replay.json) (module `CampaignOpsAxis3Relabeling`): recorded sha256 `8f6cc92938943a0dd559263f075aa7496c2bb25fab1db596f18a5fc078c01150` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignOpsAxis3Relabeling`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignOpsAxis3Relabeling.exportVerdictRelabel` | yes | yes | yes | none | `#print axioms CampaignOpsAxis3Relabeling.exportVerdictRelabel` |
| `CampaignOpsAxis3Relabeling.lengthMapInvariant` | yes | yes | yes | propext | `#print axioms CampaignOpsAxis3Relabeling.lengthMapInvariant` |
| `CampaignOpsAxis3Relabeling.lengthVerdictRelabel` | yes | yes | yes | propext | `#print axioms CampaignOpsAxis3Relabeling.lengthVerdictRelabel` |
| `CampaignOpsAxis3Relabeling.swap01` | yes | yes | yes | none | `#print axioms CampaignOpsAxis3Relabeling.swap01` |

- counts toward the grade: yes

### Python: `checks/independent/ops-axis3-relabeling.py`

- file: [checks/independent/ops-axis3-relabeling.py](../../../checks/independent/ops-axis3-relabeling.py)
- sha256 (`bytes`): `7fd8f8fb6db09ed3556b917be4f557b5c32635d24c8a226dfc3e4c6ee7e7989d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2526_ops_axis3_relabeling.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2526_ops_axis3_relabeling.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2526_ops_axis3_relabeling.md)
- sha256 (`lf-normalised`): `67e9f323eb2c84560de77449748efe628ee329a1a2df3b6904bc66395f01678a`
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
- sha256 (`lf-normalised`): `2877fc98daf3fe82d9b2668fb541b5b959c9cd8e4728726e7a05549db486927a`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/claim_ledger.md`

- file: [sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/claim_ledger.md](../../../sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/claim_ledger.md)
- sha256 (`lf-normalised`): `da99779add73314574622d0db46ea4dfbc9b66c4938caf29ab98590033592ab4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md`

- file: [sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md](../../../sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md)
- sha256 (`lf-normalised`): `ae5564735bb6591e0f149868f83bd9f9793f297be0f8af3cc889c293ae4059cb`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `OPS-R-AXIS3-RELABELING` `CONDITIONAL_ON_IMPORT`: [PGW-WDP-OBSERVER-QUOTIENT-PASSIVITY](PGW-WDP-OBSERVER-QUOTIENT-PASSIVITY.md) (DEFINITION)

Outgoing (3):

- `OPS-R-REFUTED-AXIS3-WIDE` `DERIVED_PROSE`: [OPS-REFUTED-AXIS3-WIDE](OPS-REFUTED-AXIS3-WIDE.md) (REFUTED)
- `OPS-R-REFUTED-NB9` `RECORD_PARENT`: [OPS-REFUTED-NB9](OPS-REFUTED-NB9.md) (REFUTED)
- `OPS-R-REGRESS-COROLLARY` `CONDITIONAL_ON_IMPORT`: [OPS-REGRESS-COROLLARY](OPS-REGRESS-COROLLARY.md) (CONDITIONAL)
