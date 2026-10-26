# FSP-PACHNER-INVARIANCE-CLAIM

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For every finite group G, the untwisted flat-connection count on the canonical 4D 1-5, 2-4 and 3-3 Pachner pairs, divided by |G| to the number of interior vertices, agrees for every fixed flat common boundary. The normalized total counts also agree for every finite compatible exterior family represented by dependent pairs, with the same outside-vertex count.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 99
- distinct cited Lean declarations covered by a current replay receipt: 99
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- supplied finite group G and group axioms
- untwisted flat-connection counting model with one factor |G| per interior vertex
- canonical 4D Pachner facet pairs and finite compatible exterior configurations represented by dependent pairs

## Bottleneck

Construct flat fillings by group potentials and boundary triangle cancellation; count them with interior-vertex normalization and sum over the declared exterior family. Remaining scope: The supplied finite group, untwisted flat-connection model, canonical local complexes and compatible finite exterior interface are explicit. No general triangulation/gluing-equivalence or PL-homeomorphism library is formalized; no Regge, twisted/Crane-Yetter, fermion-sign or continuum conclusion follows. Human review remains pending. Historical unnamed partition-function claim remains unsupported.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-050 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFiniteGroupPachner.lean`

- file: [lean4/CampaignFiniteGroupPachner.lean](../../../lean4/CampaignFiniteGroupPachner.lean)
- sha256 (`bytes`): `e8b2c28cf6e0a0536ba15941742f07d59dc2adcbae86bdfa7311678f6c00cdca`
- cited in: node.lean, receipt dag/research/campaign_fsp-pachner-invariance-claim_lean_replay.json (CampaignFiniteGroupPachner), record TFQ-1214
- replay: `verified`
  - receipt [dag/research/campaign_fsp-pachner-invariance-claim_lean_replay.json](../../../dag/research/campaign_fsp-pachner-invariance-claim_lean_replay.json) (module `CampaignFiniteGroupPachner`): recorded sha256 `e8b2c28cf6e0a0536ba15941742f07d59dc2adcbae86bdfa7311678f6c00cdca` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFiniteGroupPachner`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFiniteGroupPachner.BoundaryOne` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.BoundaryOne` |
| `CampaignFiniteGroupPachner.BoundaryThree` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.BoundaryThree` |
| `CampaignFiniteGroupPachner.BoundaryTwo` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.BoundaryTwo` |
| `CampaignFiniteGroupPachner.Coloring` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.Coloring` |
| `CampaignFiniteGroupPachner.Complete` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.Complete` |
| `CampaignFiniteGroupPachner.Connection` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.Connection` |
| `CampaignFiniteGroupPachner.FlatOn` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.FlatOn` |
| `CampaignFiniteGroupPachner.Matches` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.Matches` |
| `CampaignFiniteGroupPachner.OneNew` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.OneNew` |
| `CampaignFiniteGroupPachner.SelfFillings` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.SelfFillings` |
| `CampaignFiniteGroupPachner.ThreeLeft` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.ThreeLeft` |
| `CampaignFiniteGroupPachner.ThreeNew` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.ThreeNew` |
| `CampaignFiniteGroupPachner.ThreeOld` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.ThreeOld` |
| `CampaignFiniteGroupPachner.ThreeRight` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.ThreeRight` |
| `CampaignFiniteGroupPachner.TwoNew` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.TwoNew` |
| `CampaignFiniteGroupPachner.Vertex` | yes | yes | yes | none | `#print axioms CampaignFiniteGroupPachner.Vertex` |
| `CampaignFiniteGroupPachner.boundary_has_triangle_cone` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.boundary_has_triangle_cone` |
| `CampaignFiniteGroupPachner.boundary_three_flat` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.boundary_three_flat` |
| `CampaignFiniteGroupPachner.card_of_unique_witness` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.card_of_unique_witness` |
| `CampaignFiniteGroupPachner.coloringFintype` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.coloringFintype` |
| `CampaignFiniteGroupPachner.complete_eq_of_row` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.complete_eq_of_row` |
| `CampaignFiniteGroupPachner.complete_from_row` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.complete_from_row` |
| `CampaignFiniteGroupPachner.connectionFintype` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.connectionFintype` |
| `CampaignFiniteGroupPachner.edgeOne` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.edgeOne` |
| `CampaignFiniteGroupPachner.edgeTwo` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.edgeTwo` |
| `CampaignFiniteGroupPachner.edge_from_root` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.edge_from_root` |
| `CampaignFiniteGroupPachner.face_is_in_a_facet` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.face_is_in_a_facet` |
| `CampaignFiniteGroupPachner.facetFace` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.facetFace` |
| `CampaignFiniteGroupPachner.facetFaceDecidable` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.facetFaceDecidable` |
| `CampaignFiniteGroupPachner.facet_counts` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.facet_counts` |
| `CampaignFiniteGroupPachner.fillOne` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.fillOne` |
| `CampaignFiniteGroupPachner.fillThreeNew` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.fillThreeNew` |
| `CampaignFiniteGroupPachner.fillThreeOld` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.fillThreeOld` |
| `CampaignFiniteGroupPachner.fillTwo` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.fillTwo` |
| `CampaignFiniteGroupPachner.fill_one_parameter` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.fill_one_parameter` |
| `CampaignFiniteGroupPachner.five_facet_edges` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.five_facet_edges` |
| `CampaignFiniteGroupPachner.five_facet_triangles` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.five_facet_triangles` |
| `CampaignFiniteGroupPachner.flat_boundary_of_matching` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.flat_boundary_of_matching` |
| `CampaignFiniteGroupPachner.four_facet_edges` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.four_facet_edges` |
| `CampaignFiniteGroupPachner.four_facet_triangles` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.four_facet_triangles` |
| `CampaignFiniteGroupPachner.glued_one_five` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.glued_one_five` |
| `CampaignFiniteGroupPachner.glued_three_three` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.glued_three_three` |
| `CampaignFiniteGroupPachner.glued_two_four` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.glued_two_four` |
| `CampaignFiniteGroupPachner.group_order_ne_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.group_order_ne_zero` |
| `CampaignFiniteGroupPachner.interiorVertices` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.interiorVertices` |
| `CampaignFiniteGroupPachner.localAmplitude` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.localAmplitude` |
| `CampaignFiniteGroupPachner.localFacets` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.localFacets` |
| `CampaignFiniteGroupPachner.local_facets_have_five_vertices` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.local_facets_have_five_vertices` |
| `CampaignFiniteGroupPachner.nonflat_boundary_has_no_extension` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.nonflat_boundary_has_no_extension` |
| `CampaignFiniteGroupPachner.oneFillingEquiv` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.oneFillingEquiv` |
| `CampaignFiniteGroupPachner.oneNewFintype` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.oneNewFintype` |
| `CampaignFiniteGroupPachner.oneParameter` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.oneParameter` |
| `CampaignFiniteGroupPachner.onePotential` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.onePotential` |
| `CampaignFiniteGroupPachner.one_boundary_skeleton` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.one_boundary_skeleton` |
| `CampaignFiniteGroupPachner.one_facet_edges` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.one_facet_edges` |
| `CampaignFiniteGroupPachner.one_facet_triangles` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.one_facet_triangles` |
| `CampaignFiniteGroupPachner.one_filling_count` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.one_filling_count` |
| `CampaignFiniteGroupPachner.one_new_interior` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.one_new_interior` |
| `CampaignFiniteGroupPachner.one_old_interior` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.one_old_interior` |
| `CampaignFiniteGroupPachner.one_parameter_fill` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.one_parameter_fill` |
| `CampaignFiniteGroupPachner.one_root_triangle` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.one_root_triangle` |
| `CampaignFiniteGroupPachner.pachner_one_five` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.pachner_one_five` |
| `CampaignFiniteGroupPachner.pachner_three_three` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.pachner_three_three` |
| `CampaignFiniteGroupPachner.pachner_two_four` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.pachner_two_four` |
| `CampaignFiniteGroupPachner.pureColoring` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.pureColoring` |
| `CampaignFiniteGroupPachner.pureConnection` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.pureConnection` |
| `CampaignFiniteGroupPachner.selfFilling` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.selfFilling` |
| `CampaignFiniteGroupPachner.selfFillingsFintype` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.selfFillingsFintype` |
| `CampaignFiniteGroupPachner.self_filling_count` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.self_filling_count` |
| `CampaignFiniteGroupPachner.self_filling_unique` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.self_filling_unique` |
| `CampaignFiniteGroupPachner.stateSum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.stateSum` |
| `CampaignFiniteGroupPachner.threeNewFintype` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.threeNewFintype` |
| `CampaignFiniteGroupPachner.threeOldFintype` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.threeOldFintype` |
| `CampaignFiniteGroupPachner.three_boundary_skeleton` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.three_boundary_skeleton` |
| `CampaignFiniteGroupPachner.three_facet_edges` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.three_facet_edges` |
| `CampaignFiniteGroupPachner.three_facet_triangles` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.three_facet_triangles` |
| `CampaignFiniteGroupPachner.three_new_count` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.three_new_count` |
| `CampaignFiniteGroupPachner.three_new_interior` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.three_new_interior` |
| `CampaignFiniteGroupPachner.three_new_unique` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.three_new_unique` |
| `CampaignFiniteGroupPachner.three_old_count` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.three_old_count` |
| `CampaignFiniteGroupPachner.three_old_interior` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.three_old_interior` |
| `CampaignFiniteGroupPachner.three_old_unique` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.three_old_unique` |
| `CampaignFiniteGroupPachner.triangleBoundary` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.triangleBoundary` |
| `CampaignFiniteGroupPachner.triangleLeft` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.triangleLeft` |
| `CampaignFiniteGroupPachner.triangleOne` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.triangleOne` |
| `CampaignFiniteGroupPachner.triangleRight` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.triangleRight` |
| `CampaignFiniteGroupPachner.triangleTwo` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.triangleTwo` |
| `CampaignFiniteGroupPachner.triangle_from_cone` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.triangle_from_cone` |
| `CampaignFiniteGroupPachner.twoNewFintype` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.twoNewFintype` |
| `CampaignFiniteGroupPachner.two_boundary_skeleton` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.two_boundary_skeleton` |
| `CampaignFiniteGroupPachner.two_facet_edges` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.two_facet_edges` |
| `CampaignFiniteGroupPachner.two_facet_triangles` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.two_facet_triangles` |
| `CampaignFiniteGroupPachner.two_filling_count` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.two_filling_count` |
| `CampaignFiniteGroupPachner.two_filling_unique` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.two_filling_unique` |
| `CampaignFiniteGroupPachner.two_new_interior` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.two_new_interior` |
| `CampaignFiniteGroupPachner.two_old_interior` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.two_old_interior` |
| `CampaignFiniteGroupPachner.two_root_edges` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.two_root_edges` |
| `CampaignFiniteGroupPachner.two_root_triangle` | yes | yes | yes | propext | `#print axioms CampaignFiniteGroupPachner.two_root_triangle` |
| `CampaignFiniteGroupPachner.unnormalized_one_five_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFiniteGroupPachner.unnormalized_one_five_iff` |

- counts toward the grade: yes

### Python: `checks/independent/fsp-pachner-invariance-claim.py`

- file: [checks/independent/fsp-pachner-invariance-claim.py](../../../checks/independent/fsp-pachner-invariance-claim.py)
- sha256 (`bytes`): `ec9f5bf0c4bdf2d8b829f23871f376b08c3f329746aaadfde6cb8293cd0b38b5`
- cited in: record TFQ-1214
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1214_fsp_pachner_invariance_claim.md`

- file: [dag/derivations/26_fsp/tfq_1214_fsp_pachner_invariance_claim.md](../../../dag/derivations/26_fsp/tfq_1214_fsp_pachner_invariance_claim.md)
- sha256 (`lf-normalised`): `fbf1d99a504872b1e468b96813aee7127f12c0ef16466b4b13048ce1cebbd07c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1214
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-pachner-invariance-claim.md`

- file: [dag/derivations/independent/fsp-pachner-invariance-claim.md](../../../dag/derivations/independent/fsp-pachner-invariance-claim.md)
- sha256 (`lf-normalised`): `59b067444ededaf7a754e33e1487c7b14c0ffe6e447ccb3b4b16073f09bc6a04`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-pachner-invariance-claim_lean_replay.json`

- file: [dag/research/campaign_fsp-pachner-invariance-claim_lean_replay.json](../../../dag/research/campaign_fsp-pachner-invariance-claim_lean_replay.json)
- sha256 (`lf-normalised`): `cea239c2894d9939b604a3859a3028ce92e70c901db51d7a1a778150da74a1af`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-PACHNER-INVARIANCE-CLAIM` `DERIVED_LEAN`: [DFM-GROUP-CONNECTION](DFM-GROUP-CONNECTION.md) (DEFINITION)

Outgoing (1):

- `APP-R-FSP-CDT-FOLIATION-POSITIVITY` `GAP_NO_DERIVATION`: [FSP-CDT-FOLIATION-POSITIVITY](FSP-CDT-FOLIATION-POSITIVITY.md) (OPEN)
