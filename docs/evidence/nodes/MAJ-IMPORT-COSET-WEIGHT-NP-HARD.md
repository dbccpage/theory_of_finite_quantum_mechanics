# MAJ-IMPORT-COSET-WEIGHT-NP-HARD

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Minimum-weight coset decoding of a binary linear code given by its matrix is NP-hard (Berlekamp, McEliece and van Tilborg 1978).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 8
- cited Lean, Rust or Python symbols found in their in-repo files: 12
- cited Lean declarations covered by a current replay receipt: 10
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Berlekamp-McEliece-van Tilborg 1978 hardness of coset weights

## Bottleneck

Literature result (Berlekamp, McEliece, and van Tilborg 1978); the Cook-Levin / 3-Dimensional Matching NP-completeness reduction remains an imported external theorem. Narrowed in lean4/CampaignMajImportCosetWeightNpHard.lean and checks/independent/maj-import-coset-weight-np-hard.py while keeping status IMPORTED_ASSUMPTION to: (1) F2^n involutive vector addition ((r ^ c) ^ c = r) and Hamming weight subadditivity wt(u ^ v) + 2 overlap(u, v) = wt(u) + wt(v); (2) exact primal coset-weight decision equivalence (exists alpha, wt(r ^ d0 alpha) \<= w) \<-\> parity-check syndrome-decoding decision (exists e, H(e) = H(r) and wt(e) \<= w), gauge-shift invariance under r -\> r ^ d0 beta, and budget-capped upper-bound witness inequalities; (3) constructive 5-coordinate (n = 5, k = 2) greedy single-generator flip local-minimum trap where wt(r) = 3, single flips give wt(r ^ g1) = 4 and wt(r ^ g2) = 4, and the joint flip gives the coset leader wt(r ^ g1 ^ g2) = 2 \< 3; and (4) 3x4 vs 6x6 tetron torus coset budget overflow (2^11 = 2048 \< 2^20 \< 2^35 = 34,359,738,368) and explicit scope fences separating general linear codes from planar/toric graph-incidence families.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-IMPORT-BMVT claims IMPORTED_ASSUMPTION; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignMajImportCosetWeightNpHard.lean`

- file: [lean4/CampaignMajImportCosetWeightNpHard.lean](../../../lean4/CampaignMajImportCosetWeightNpHard.lean)
- sha256 (`bytes`): `f62c1d69a7c84608222ab6dd92e7111566e1992932bf18ee371204e5209c1ff5`
- cited in: node.lean, receipt dag/research/campaign_maj-import-coset-weight-np-hard_lean_replay.json (CampaignMajImportCosetWeightNpHard), record TFQ-1157
- replay: `verified`
  - receipt [dag/research/campaign_maj-import-coset-weight-np-hard_lean_replay.json](../../../dag/research/campaign_maj-import-coset-weight-np-hard_lean_replay.json) (module `CampaignMajImportCosetWeightNpHard`): recorded sha256 `f62c1d69a7c84608222ab6dd92e7111566e1992932bf18ee371204e5209c1ff5` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignMajImportCosetWeightNpHard`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignMajImportCosetWeightNpHard.bmvt_import_scope_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajImportCosetWeightNpHard.bmvt_import_scope_fence` |
| `CampaignMajImportCosetWeightNpHard.coset_decoding_iff_syndrome_decoding` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajImportCosetWeightNpHard.coset_decoding_iff_syndrome_decoding` |
| `CampaignMajImportCosetWeightNpHard.coset_search_budget_overflow_witness` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajImportCosetWeightNpHard.coset_search_budget_overflow_witness` |
| `CampaignMajImportCosetWeightNpHard.coset_weight_decision_gauge_invariant` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajImportCosetWeightNpHard.coset_weight_decision_gauge_invariant` |
| `CampaignMajImportCosetWeightNpHard.f2_hamming_weight_subadditive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajImportCosetWeightNpHard.f2_hamming_weight_subadditive` |
| `CampaignMajImportCosetWeightNpHard.f2_pointwise_bit_weight_identity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajImportCosetWeightNpHard.f2_pointwise_bit_weight_identity` |
| `CampaignMajImportCosetWeightNpHard.f2_vector_space_involutive_cancel` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajImportCosetWeightNpHard.f2_vector_space_involutive_cancel` |
| `CampaignMajImportCosetWeightNpHard.greedy_single_gauge_flip_local_minimum_trap` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajImportCosetWeightNpHard.greedy_single_gauge_flip_local_minimum_trap` |
| `CampaignMajImportCosetWeightNpHard.sampled_gauge_upper_bounds_coset_leader` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajImportCosetWeightNpHard.sampled_gauge_upper_bounds_coset_leader` |
| `CampaignMajImportCosetWeightNpHard.worst_case_code_hardness_vs_planar_toric_scope` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajImportCosetWeightNpHard.worst_case_code_hardness_vs_planar_toric_scope` |
- counts toward the grade: yes

### Python: `checks/independent/maj-import-coset-weight-np-hard.py`

- file: [checks/independent/maj-import-coset-weight-np-hard.py](../../../checks/independent/maj-import-coset-weight-np-hard.py)
- sha256 (`bytes`): `48cb13da64b2a80170fe8011af0a9826c083b9a0fd8f4833966d595a719b8efa`
- cited in: record TFQ-1157

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `papers/core/majorana/code/majorana_evaluator.py`

- file: [papers/core/majorana/code/majorana_evaluator.py](../../../papers/core/majorana/code/majorana_evaluator.py)
- sha256 (`bytes`): `86798eabea510363b59e164c516625c6055df24b4e12086cfe2fde5db16835c3`
- cited in: record TFQ-1157

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `compute_coset_weight` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1157_maj_import_coset_weight_np_hard.md`

- file: [dag/derivations/28_majorana/tfq_1157_maj_import_coset_weight_np_hard.md](../../../dag/derivations/28_majorana/tfq_1157_maj_import_coset_weight_np_hard.md)
- sha256 (`lf-normalised`): `6575f240fa6507a617cf1a15d431a992ccd8d3bc1ce46a20216f0911e28e9d2f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1157
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/maj-import-coset-weight-np-hard.md`

- file: [dag/derivations/independent/maj-import-coset-weight-np-hard.md](../../../dag/derivations/independent/maj-import-coset-weight-np-hard.md)
- sha256 (`lf-normalised`): `7f42e54f79c2b8a4f6509837d36c57cce4e342816a1f403849dc4e8f91e3924a`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_maj-import-coset-weight-np-hard_independent.json`

- file: [dag/research/campaign_maj-import-coset-weight-np-hard_independent.json](../../../dag/research/campaign_maj-import-coset-weight-np-hard_independent.json)
- sha256 (`lf-normalised`): `9c8fd6596d902aae25505834d762720c29d25008acefa7c6ed0e569bc4d55c64`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_maj-import-coset-weight-np-hard_lean_mutation.json`

- file: [dag/research/campaign_maj-import-coset-weight-np-hard_lean_mutation.json](../../../dag/research/campaign_maj-import-coset-weight-np-hard_lean_mutation.json)
- sha256 (`lf-normalised`): `75e8842f5f553ecdf4ef23767b3d6411ee5f82d5a95577048fd3f9f4ae29b92b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_maj-import-coset-weight-np-hard_lean_replay.json`

- file: [dag/research/campaign_maj-import-coset-weight-np-hard_lean_replay.json](../../../dag/research/campaign_maj-import-coset-weight-np-hard_lean_replay.json)
- sha256 (`lf-normalised`): `2329693a5d38f38d3fd8af270420184a98177e2cdc92dd03aebda4a30371344e`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `e92416bb1739e51de20a8ad6a26d4b5f3d76b974d7556507b13149b29e8edb47`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-IMPORT-COSET-WEIGHT-NP-HARD` `CONDITIONAL_ON_IMPORT`: [MAJ-PHI1-HAMMING-COSET](MAJ-PHI1-HAMMING-COSET.md) (DEFINITION)

Outgoing (1):

- `APP-R-MAJ-PHI1-SYNDROME-DECODING` `CONDITIONAL_ON_IMPORT`: [MAJ-PHI1-SYNDROME-DECODING](MAJ-PHI1-SYNDROME-DECODING.md) (CONDITIONAL)
