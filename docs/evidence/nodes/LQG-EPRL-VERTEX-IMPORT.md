# LQG-EPRL-VERTEX-IMPORT

Stage: [LOOP_QUANTUM_GRAVITY](../stages/LOOP_QUANTUM_GRAVITY.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Imported construction, audited against Engle, Livine, Pereira and Rovelli (2008, arXiv:0711.0146, Section III eqs. (18)-(22), (27)-(30) pp. 6-9 and Section IV eqs. (24)-(25) p. 8) and Freidel and Krasnov (2008, arXiv:0708.1595, Section II.C Lemmas 2.1-2.4 pp. 10-12 and Section V eqs. (80)-(91) pp. 24-27): for a four-simplex with ten triangle spins k_ab and five tetrahedral SU(2) intertwiners i_a, the Euclidean EPRL vertex amplitude embeds each SU(2) representation k into Spin(4) = SU(2)_+ x SU(2)_- at j^+- = |1 +- gamma| k / 2 (so k = j^+ + j^- for 0 \< gamma \< 1 and k = j^+ - j^- for gamma \> 1, eqs. (18)-(20)) and contracts the resulting boosters with the Spin(4) 15j symbol (eqs. (29)-(30)), while the Lorentzian vertex embeds k into the SL(2,C) unitary principal series at (n, rho) = (2k, 2 gamma k) in EPRL's integer-n convention (eq. (24) p. 8, often written (j, gamma j) when indexing by half-integer spin j = n/2 = k). It requires continuum Lie-group representations, the boundary Hilbert space of spin networks and sums over spins whose convergence and continuum limit are open research questions. The repository has finite cyclotomic amplitudes (TFQ-0198) that it refuses to identify with a continuum spin foam.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 12
- distinct cited Lean declarations covered by a current replay receipt: 6
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
- check: `cd lean4 && lake build CampaignLqgEprlVertexImport`

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
- sha256 (`lf-normalised`): `ec35f9d1661d84919f86c6919d8c8d5fbda220ec5090deceacfd74ca1033fdca`
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
