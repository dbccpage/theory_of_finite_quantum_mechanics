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

### Lean: `lean4/FiniteGroupPachner.lean`

- file: [lean4/FiniteGroupPachner.lean](../../../lean4/FiniteGroupPachner.lean)
- sha256 (`bytes`): `2f4916b1ac6b688304948b5ad00aa570a0a2cae0770ab80587307f6acffda82e`
- cited in: node.lean, receipt dag/research/campaign_fsp-pachner-invariance-claim_lean_replay.json (FiniteGroupPachner), record TFQ-1214
- replay: `verified`
  - receipt [dag/research/campaign_fsp-pachner-invariance-claim_lean_replay.json](../../../dag/research/campaign_fsp-pachner-invariance-claim_lean_replay.json) (module `FiniteGroupPachner`): recorded sha256 `2f4916b1ac6b688304948b5ad00aa570a0a2cae0770ab80587307f6acffda82e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteGroupPachner`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FiniteGroupPachner.BoundaryOne` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.BoundaryOne` |
| `FiniteGroupPachner.BoundaryThree` | yes | yes | yes | Quot.sound, propext | `#print axioms FiniteGroupPachner.BoundaryThree` |
| `FiniteGroupPachner.BoundaryTwo` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.BoundaryTwo` |
| `FiniteGroupPachner.Coloring` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.Coloring` |
| `FiniteGroupPachner.Complete` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.Complete` |
| `FiniteGroupPachner.Connection` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.Connection` |
| `FiniteGroupPachner.FlatOn` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.FlatOn` |
| `FiniteGroupPachner.Matches` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.Matches` |
| `FiniteGroupPachner.OneNew` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.OneNew` |
| `FiniteGroupPachner.SelfFillings` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.SelfFillings` |
| `FiniteGroupPachner.ThreeLeft` | yes | yes | yes | Quot.sound, propext | `#print axioms FiniteGroupPachner.ThreeLeft` |
| `FiniteGroupPachner.ThreeNew` | yes | yes | yes | Quot.sound, propext | `#print axioms FiniteGroupPachner.ThreeNew` |
| `FiniteGroupPachner.ThreeOld` | yes | yes | yes | Quot.sound, propext | `#print axioms FiniteGroupPachner.ThreeOld` |
| `FiniteGroupPachner.ThreeRight` | yes | yes | yes | Quot.sound, propext | `#print axioms FiniteGroupPachner.ThreeRight` |
| `FiniteGroupPachner.TwoNew` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.TwoNew` |
| `FiniteGroupPachner.Vertex` | yes | yes | yes | none | `#print axioms FiniteGroupPachner.Vertex` |
| `FiniteGroupPachner.boundary_has_triangle_cone` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.boundary_has_triangle_cone` |
| `FiniteGroupPachner.boundary_three_flat` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.boundary_three_flat` |
| `FiniteGroupPachner.card_of_unique_witness` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.card_of_unique_witness` |
| `FiniteGroupPachner.coloringFintype` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.coloringFintype` |
| `FiniteGroupPachner.complete_eq_of_row` | yes | yes | yes | Quot.sound, propext | `#print axioms FiniteGroupPachner.complete_eq_of_row` |
| `FiniteGroupPachner.complete_from_row` | yes | yes | yes | Quot.sound, propext | `#print axioms FiniteGroupPachner.complete_from_row` |
| `FiniteGroupPachner.connectionFintype` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.connectionFintype` |
| `FiniteGroupPachner.edgeOne` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.edgeOne` |
| `FiniteGroupPachner.edgeTwo` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.edgeTwo` |
| `FiniteGroupPachner.edge_from_root` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.edge_from_root` |
| `FiniteGroupPachner.face_is_in_a_facet` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.face_is_in_a_facet` |
| `FiniteGroupPachner.facetFace` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.facetFace` |
| `FiniteGroupPachner.facetFaceDecidable` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.facetFaceDecidable` |
| `FiniteGroupPachner.facet_counts` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.facet_counts` |
| `FiniteGroupPachner.fillOne` | yes | yes | yes | Quot.sound, propext | `#print axioms FiniteGroupPachner.fillOne` |
| `FiniteGroupPachner.fillThreeNew` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.fillThreeNew` |
| `FiniteGroupPachner.fillThreeOld` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.fillThreeOld` |
| `FiniteGroupPachner.fillTwo` | yes | yes | yes | Quot.sound, propext | `#print axioms FiniteGroupPachner.fillTwo` |
| `FiniteGroupPachner.fill_one_parameter` | yes | yes | yes | Quot.sound, propext | `#print axioms FiniteGroupPachner.fill_one_parameter` |
| `FiniteGroupPachner.five_facet_edges` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.five_facet_edges` |
| `FiniteGroupPachner.five_facet_triangles` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.five_facet_triangles` |
| `FiniteGroupPachner.flat_boundary_of_matching` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.flat_boundary_of_matching` |
| `FiniteGroupPachner.four_facet_edges` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.four_facet_edges` |
| `FiniteGroupPachner.four_facet_triangles` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.four_facet_triangles` |
| `FiniteGroupPachner.glued_one_five` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.glued_one_five` |
| `FiniteGroupPachner.glued_three_three` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.glued_three_three` |
| `FiniteGroupPachner.glued_two_four` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.glued_two_four` |
| `FiniteGroupPachner.group_order_ne_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.group_order_ne_zero` |
| `FiniteGroupPachner.interiorVertices` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.interiorVertices` |
| `FiniteGroupPachner.localAmplitude` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.localAmplitude` |
| `FiniteGroupPachner.localFacets` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.localFacets` |
| `FiniteGroupPachner.local_facets_have_five_vertices` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.local_facets_have_five_vertices` |
| `FiniteGroupPachner.nonflat_boundary_has_no_extension` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.nonflat_boundary_has_no_extension` |
| `FiniteGroupPachner.oneFillingEquiv` | yes | yes | yes | Quot.sound, propext | `#print axioms FiniteGroupPachner.oneFillingEquiv` |
| `FiniteGroupPachner.oneNewFintype` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.oneNewFintype` |
| `FiniteGroupPachner.oneParameter` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.oneParameter` |
| `FiniteGroupPachner.onePotential` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.onePotential` |
| `FiniteGroupPachner.one_boundary_skeleton` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.one_boundary_skeleton` |
| `FiniteGroupPachner.one_facet_edges` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.one_facet_edges` |
| `FiniteGroupPachner.one_facet_triangles` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.one_facet_triangles` |
| `FiniteGroupPachner.one_filling_count` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.one_filling_count` |
| `FiniteGroupPachner.one_new_interior` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.one_new_interior` |
| `FiniteGroupPachner.one_old_interior` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.one_old_interior` |
| `FiniteGroupPachner.one_parameter_fill` | yes | yes | yes | Quot.sound, propext | `#print axioms FiniteGroupPachner.one_parameter_fill` |
| `FiniteGroupPachner.one_root_triangle` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.one_root_triangle` |
| `FiniteGroupPachner.pachner_one_five` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.pachner_one_five` |
| `FiniteGroupPachner.pachner_three_three` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.pachner_three_three` |
| `FiniteGroupPachner.pachner_two_four` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.pachner_two_four` |
| `FiniteGroupPachner.pureColoring` | yes | yes | yes | Quot.sound, propext | `#print axioms FiniteGroupPachner.pureColoring` |
| `FiniteGroupPachner.pureConnection` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.pureConnection` |
| `FiniteGroupPachner.selfFilling` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.selfFilling` |
| `FiniteGroupPachner.selfFillingsFintype` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.selfFillingsFintype` |
| `FiniteGroupPachner.self_filling_count` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.self_filling_count` |
| `FiniteGroupPachner.self_filling_unique` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.self_filling_unique` |
| `FiniteGroupPachner.stateSum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.stateSum` |
| `FiniteGroupPachner.threeNewFintype` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.threeNewFintype` |
| `FiniteGroupPachner.threeOldFintype` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.threeOldFintype` |
| `FiniteGroupPachner.three_boundary_skeleton` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.three_boundary_skeleton` |
| `FiniteGroupPachner.three_facet_edges` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.three_facet_edges` |
| `FiniteGroupPachner.three_facet_triangles` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.three_facet_triangles` |
| `FiniteGroupPachner.three_new_count` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.three_new_count` |
| `FiniteGroupPachner.three_new_interior` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.three_new_interior` |
| `FiniteGroupPachner.three_new_unique` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.three_new_unique` |
| `FiniteGroupPachner.three_old_count` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.three_old_count` |
| `FiniteGroupPachner.three_old_interior` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.three_old_interior` |
| `FiniteGroupPachner.three_old_unique` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.three_old_unique` |
| `FiniteGroupPachner.triangleBoundary` | yes | yes | yes | Quot.sound, propext | `#print axioms FiniteGroupPachner.triangleBoundary` |
| `FiniteGroupPachner.triangleLeft` | yes | yes | yes | Quot.sound, propext | `#print axioms FiniteGroupPachner.triangleLeft` |
| `FiniteGroupPachner.triangleOne` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.triangleOne` |
| `FiniteGroupPachner.triangleRight` | yes | yes | yes | Quot.sound, propext | `#print axioms FiniteGroupPachner.triangleRight` |
| `FiniteGroupPachner.triangleTwo` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.triangleTwo` |
| `FiniteGroupPachner.triangle_from_cone` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.triangle_from_cone` |
| `FiniteGroupPachner.twoNewFintype` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.twoNewFintype` |
| `FiniteGroupPachner.two_boundary_skeleton` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.two_boundary_skeleton` |
| `FiniteGroupPachner.two_facet_edges` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.two_facet_edges` |
| `FiniteGroupPachner.two_facet_triangles` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.two_facet_triangles` |
| `FiniteGroupPachner.two_filling_count` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.two_filling_count` |
| `FiniteGroupPachner.two_filling_unique` | yes | yes | yes | Quot.sound, propext | `#print axioms FiniteGroupPachner.two_filling_unique` |
| `FiniteGroupPachner.two_new_interior` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.two_new_interior` |
| `FiniteGroupPachner.two_old_interior` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.two_old_interior` |
| `FiniteGroupPachner.two_root_edges` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.two_root_edges` |
| `FiniteGroupPachner.two_root_triangle` | yes | yes | yes | propext | `#print axioms FiniteGroupPachner.two_root_triangle` |
| `FiniteGroupPachner.unnormalized_one_five_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FiniteGroupPachner.unnormalized_one_five_iff` |

- counts toward the grade: yes

### Python: `checks/independent/fsp-pachner-invariance-claim.py`

- file: [checks/independent/fsp-pachner-invariance-claim.py](../../../checks/independent/fsp-pachner-invariance-claim.py)
- sha256 (`bytes`): `ec9f5bf0c4bdf2d8b829f23871f376b08c3f329746aaadfde6cb8293cd0b38b5`
- cited in: record TFQ-1214
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1214_fsp_pachner_invariance_claim.md`

- file: [dag/derivations/26_fsp/tfq_1214_fsp_pachner_invariance_claim.md](../../../dag/derivations/26_fsp/tfq_1214_fsp_pachner_invariance_claim.md)
- sha256 (`lf-normalised`): `130e156bdb079b1072bca8b55cce438ecfe5a8fdd1d80e681d68c38a6a409007`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1214
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-pachner-invariance-claim.md`

- file: [dag/derivations/independent/fsp-pachner-invariance-claim.md](../../../dag/derivations/independent/fsp-pachner-invariance-claim.md)
- sha256 (`lf-normalised`): `ab24522dc1d8226870cf4b2800274ad6ac1bb7c352583ab8bff8c408126c9154`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-pachner-invariance-claim_lean_replay.json`

- file: [dag/research/campaign_fsp-pachner-invariance-claim_lean_replay.json](../../../dag/research/campaign_fsp-pachner-invariance-claim_lean_replay.json)
- sha256 (`lf-normalised`): `14f5f9aefd737f4f8c4b771d115c3c6692d1db00e25fa2dfb9d6c136103af597`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `5a72c2f6006ea18c3362f0a63e8525b65d41898e8f1bd437b7e4c2e368c7e102`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-PACHNER-INVARIANCE-CLAIM` `DERIVED_LEAN`: [DFM-GROUP-CONNECTION](DFM-GROUP-CONNECTION.md) (DEFINITION)

Outgoing (1):

- `APP-R-FSP-CDT-FOLIATION-POSITIVITY` `GAP_NO_DERIVATION`: [FSP-CDT-FOLIATION-POSITIVITY](FSP-CDT-FOLIATION-POSITIVITY.md) (OPEN)
