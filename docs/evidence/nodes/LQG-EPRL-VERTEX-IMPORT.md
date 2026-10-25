# LQG-EPRL-VERTEX-IMPORT

Stage: [LOOP_QUANTUM_GRAVITY](../stages/LOOP_QUANTUM_GRAVITY.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For rational gamma and rational k, the imported Euclidean labels are j+ = |1 + gamma| k / 2 and j- = |1 - gamma| k / 2. When 0 \< gamma \< 1 they equal (1 + gamma) k / 2 and (1 - gamma) k / 2, their sum is k, and their difference is gamma k. When gamma \> 1 they equal (1 + gamma) k / 2 and (gamma - 1) k / 2, their difference is k, and their sum is gamma k. At gamma = 1/2 and k = 2 the labels are 3/2 and 1/2, the sum is 2, and the difference is 1, which is not 2. At gamma = 3 and k = 2 the labels are 4 and 2, the difference is 2, and the sum is 6, which is not 2. At gamma = 1 and k = 2 the labels are 2 and 0, and both the sum and the difference equal 2. The imported Lorentzian pair is (n, rho) = (2 k, 2 gamma k), with rho = gamma n = 2 gamma (n / 2). At gamma = 1/2 and k = 2 this pair is (4, 2), the index j = n / 2 equals 2, and gamma j equals 1, so rho = 2 gamma j rather than gamma j. The number of unordered pairs among five indices is 10. A Spin(4) 15j contraction, booster factors, a continuum Lie-group representation, a spin-network boundary space, a sum over spins, a continuum limit, a semiclassical limit, and a cosmological constant stay imported and are not constructed. The finite cyclotomic amplitudes named by TFQ-0198 are not identified with an EPRL-FK vertex.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 12
- cited Lean declarations covered by a current replay receipt: 12
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- SU(2) and Spin(4) representation theory (assumption)
- simplicity constraints and Immirzi parameter (assumption)

## Bottleneck

The checked identities are rational arithmetic for the imported labels j+ = |1 + gamma| k / 2 and j- = |1 - gamma| k / 2, the pair (n, rho) = (2 k, 2 gamma k), and the count of 10 unordered pairs among five indices. They are not a Spin(4) 15j symbol, not a booster contraction, and not a continuum, semiclassical, or cosmological-constant limit. No source maps the finite cyclotomic amplitudes to the EPRL-FK amplitude.

## Source status

Rational Euclidean and Lorentzian label identities were checked in Lean 4 on 2026-10-24. The EPRL-FK vertex, the 15j contraction, and any continuum or semiclassical limit remain an imported assumption. The 2008 embedding formulas were audited on 2026-10-22.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignLqgEprlVertexImport.lean`

- file: [lean4/CampaignLqgEprlVertexImport.lean](../../../lean4/CampaignLqgEprlVertexImport.lean)
- sha256 (`bytes`): `da05f4cd6010a04604e4e8d51775bf0ae08dc1a13065978e038e819ddc41833f`
- cited in: node.lean, node.source, receipt dag/research/campaign_lqg-eprl-vertex-import_lean_replay.json (CampaignLqgEprlVertexImport), record TFQ-2314
- replay: `verified`
  - receipt [dag/research/campaign_lqg-eprl-vertex-import_lean_replay.json](../../../dag/research/campaign_lqg-eprl-vertex-import_lean_replay.json) (module `CampaignLqgEprlVertexImport`): recorded sha256 `da05f4cd6010a04604e4e8d51775bf0ae08dc1a13065978e038e819ddc41833f` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/CampaignLqgEprlVertexImport.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignLqgEprlVertexImport.euclidean_above` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgEprlVertexImport.euclidean_above` |
| `CampaignLqgEprlVertexImport.euclidean_below` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgEprlVertexImport.euclidean_below` |
| `CampaignLqgEprlVertexImport.five_tetrahedron_pairs` | yes | yes | yes | none | `#print axioms CampaignLqgEprlVertexImport.five_tetrahedron_pairs` |
| `CampaignLqgEprlVertexImport.lorentzian_embedding` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgEprlVertexImport.lorentzian_embedding` |
| `CampaignLqgEprlVertexImport.lorentzian_half_two` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgEprlVertexImport.lorentzian_half_two` |
| `CampaignLqgEprlVertexImport.recorded_euclidean_points` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgEprlVertexImport.recorded_euclidean_points` |
| `euclidean_above` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms euclidean_above` |
| `euclidean_below` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms euclidean_below` |
| `five_tetrahedron_pairs` | yes | yes | yes | none | `#print axioms five_tetrahedron_pairs` |
| `lorentzian_embedding` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms lorentzian_embedding` |
| `lorentzian_half_two` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms lorentzian_half_two` |
| `recorded_euclidean_points` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms recorded_euclidean_points` |
- counts toward the grade: yes

### Python: `checks/independent/lqg-eprl-vertex-import.py`

- file: [checks/independent/lqg-eprl-vertex-import.py](../../../checks/independent/lqg-eprl-vertex-import.py)
- sha256 (`bytes`): `2c3d405d7ec94e0a1573b30ace3e7d3c19cf987f238977e712b64534e95ca0af`
- cited in: node.source, record TFQ-2314
- counts toward the grade: yes

### Documents and data: `dag/derivations/33_loop_quantum_gravity/tfq_2314_lqg_eprl_vertex_import.md`

- file: [dag/derivations/33_loop_quantum_gravity/tfq_2314_lqg_eprl_vertex_import.md](../../../dag/derivations/33_loop_quantum_gravity/tfq_2314_lqg_eprl_vertex_import.md)
- sha256 (`lf-normalised`): `31869d6d8ab75ce88a5cd90d888816c5f094dbb116741cedab3fb9dfdbf49051`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2314
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/lqg-eprl-vertex-import.md`

- file: [dag/derivations/independent/lqg-eprl-vertex-import.md](../../../dag/derivations/independent/lqg-eprl-vertex-import.md)
- sha256 (`lf-normalised`): `667eb098e1c1905b22a1e1fbc017915311f20dedfee97d03ae14cb407aa44fcb`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:0708.1595`
- `external:arXiv:0711.0146`
- `external:arXiv:1205.2019`

## Routes

Incoming (1):

- `FRO-R-LQG-EPRL-VERTEX-IMPORT` `CONDITIONAL_ON_IMPORT`: [LQG-EPRL-2007-SOURCE](LQG-EPRL-2007-SOURCE.md) (SOURCE_RECORD), [TFQ-0198](TFQ-0198.md) (COMPUTATIONALLY_CHECKED)

Outgoing (1):

- `FRO-R-LQG-CONTINUUM-LIMIT-GAP` `GAP_NO_DERIVATION`: [LQG-CONTINUUM-LIMIT-GAP](LQG-CONTINUUM-LIMIT-GAP.md) (OPEN)
