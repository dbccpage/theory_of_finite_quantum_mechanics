# DFM-HIERARCHICAL-BOREL

Stage: [DRESSING_FIELD](../stages/DRESSING_FIELD.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Let B_2(Q) be the invertible upper-triangular 2x2 matrices over Q, T the diagonal matrices and N the unit upper-triangular matrices. Every invertible element factors uniquely as D * n with D in T and n in N, and conjugation of an element of N by an invertible element stays in N. torusProj preserves multiplication. On any vertex type with a root, a parent function fixing the root, and a natural depth function that is zero at the root and strictly decreases along parents off the root, and for invertible labels off the root, root-to-vertex transport multiplies labels on the left: T(root) = I and T(v) = U(v) * T(parent(v)). The stage-one field u_N(v) equals D(v) * n(v)^{-1} * D(v)^{-1}, lies in N, and equals \[\[1, -b(v)/d2(v)\], \[0, 1\]\]. Dressing a tree edge by u_N yields D(child) * D(parent)^{-1}. For every label g and every pair of vertices, torusProj(u_N(target) * g * u_N(source)^{-1}) equals torusProj(g). A further diagonal vertex field, multiplied on the left at the child and on the right by its inverse at the parent, leaves that dressed tree edge diagonal. The stage-two field u_T(v) = D(v)^{-1} satisfies u_T(v) * u_N(v) = T(v)^{-1}, and u_T(target) * (u_N(target) * g * u_N(source)^{-1}) * u_T(source)^{-1} equals T(target)^{-1} * g * T(source). That dressed label equals I if and only if g = T(target) * T(source)^{-1}. A vertex field that is invertible at every vertex, equals I at the root, and satisfies U(v) = g(v) * g(parent(v))^{-1} off the root, equals the rooted transport. The factorization identity fails on \[\[0, 1\], \[0, 1\]\]. Replacing the (2, 2) entry by 1 does not preserve the product of \[\[2, 1\], \[0, 3\]\] with itself. On any commutative ring R, for A : R -\> R -\> R, the operators (bA)(u, v, w) = -A(u, w) and (A smile A)(u, v, w) = A(u, v) * A(v, w) with (bK)(u,v,w,z) = -K(u,w,z) + K(u,v,z) satisfy b composed with b equal to 0, the Bianchi identity for K = bA + A smile A, and endpoint gauge covariance K(A^g) = g(u) * K(A) * g(w)^{-1} for supplied g and g_inv with g(x) * g_inv(x) = 1 at every x, writing g_inv as g^{-1}, when A^g(x, y) = g(x) * A(x, y) * g_inv(y). For A(0,1)=1, A(1,2)=1, A(0,2)=0, g(0)=1 and g(1)=2, the source-only expression (g(0)*A(0,1))*(g(1)*A(1,2)) - (g(0)*A(0,2)) is not equal to g(0)*(A(0,1)*A(1,2) - A(0,2)). The same values with g(2)=1 and g(1)^{-1}=1/2 satisfy the endpoint identity. The arithmetic comparison of 2 with 3 records that these integers differ. On the four-vertex tree with parents 0, 0, 0, 2, transport at vertex 3 equals U(3) * U(2).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 42
- distinct cited Lean declarations covered by a current replay receipt: 21
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- supplied root fixed by parent, natural depth zero at root and strictly decreasing off root, and invertible off-root labels
- specified scalar commutative cochain operators b1, b2 and cup products; no bundled incidence DGA construction

## Bottleneck

The rooted tree, given by a parent function and a strictly decreasing depth, and the incidence cochain are supplied data. This statement does not construct a spanning tree from an arbitrary graph, does not identify an obstruction with a computed cohomology group, and does not build a 2-plaquette prism. Continuum gauge theory, color transport and smooth patching stay outside this statement. No bundled incidence DGA or noncommutative matrix-valued curvature is constructed.

## Source status

Lean 4.35.0 module DressingFieldHierarchicalBorel; the printed axioms are propext, Classical.choice and Quot.sound.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DressingFieldHierarchicalBorel.lean`

- file: [lean4/DressingFieldHierarchicalBorel.lean](../../../lean4/DressingFieldHierarchicalBorel.lean)
- sha256 (`bytes`): `d5366519d454b57ed1a436eb257ff615fd94998cdc4fdf9cd7e15ec355ef117e`
- cited in: node.lean, receipt dag/research/campaign_dfm-hierarchical-borel_lean_replay.json (DressingFieldHierarchicalBorel), record TFQ-0400
- replay: `verified`
  - receipt [dag/research/campaign_dfm-hierarchical-borel_lean_replay.json](../../../dag/research/campaign_dfm-hierarchical-borel_lean_replay.json) (module `DressingFieldHierarchicalBorel`): recorded sha256 `d5366519d454b57ed1a436eb257ff615fd94998cdc4fdf9cd7e15ec355ef117e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DressingFieldHierarchicalBorel`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `DressingFieldHierarchicalBorel.UpperTri2.b2_factorization_unique` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldHierarchicalBorel.UpperTri2.b2_factorization_unique` |
| `DressingFieldHierarchicalBorel.UpperTri2.b2_semidirect_factorization` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldHierarchicalBorel.UpperTri2.b2_semidirect_factorization` |
| `DressingFieldHierarchicalBorel.UpperTri2.badProj_not_homomorphism` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldHierarchicalBorel.UpperTri2.badProj_not_homomorphism` |
| `DressingFieldHierarchicalBorel.UpperTri2.factorization_fails_if_singular` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldHierarchicalBorel.UpperTri2.factorization_fails_if_singular` |
| `DressingFieldHierarchicalBorel.UpperTri2.torusProj_mul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldHierarchicalBorel.UpperTri2.torusProj_mul` |
| `DressingFieldHierarchicalBorel.UpperTri2.unipotent_subgroup_normal` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldHierarchicalBorel.UpperTri2.unipotent_subgroup_normal` |
| `DressingFieldHierarchicalBorel.anchored_transport_unique` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldHierarchicalBorel.anchored_transport_unique` |
| `DressingFieldHierarchicalBorel.b_squared_zero` | yes | yes | yes | propext | `#print axioms DressingFieldHierarchicalBorel.b_squared_zero` |
| `DressingFieldHierarchicalBorel.carrier_dimension_two_ne_three` | yes | yes | yes | none | `#print axioms DressingFieldHierarchicalBorel.carrier_dimension_two_ne_three` |
| `DressingFieldHierarchicalBorel.curvature_gauge_covariance` | yes | yes | yes | Quot.sound, propext | `#print axioms DressingFieldHierarchicalBorel.curvature_gauge_covariance` |
| `DressingFieldHierarchicalBorel.diamond_transport_three` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldHierarchicalBorel.diamond_transport_three` |
| `DressingFieldHierarchicalBorel.discrete_bianchi_identity` | yes | yes | yes | Quot.sound, propext | `#print axioms DressingFieldHierarchicalBorel.discrete_bianchi_identity` |
| `DressingFieldHierarchicalBorel.dressed_one_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldHierarchicalBorel.dressed_one_iff` |
| `DressingFieldHierarchicalBorel.endpoint_dressing_matches_curvature` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldHierarchicalBorel.endpoint_dressing_matches_curvature` |
| `DressingFieldHierarchicalBorel.source_only_dressing_breaks_curvature` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldHierarchicalBorel.source_only_dressing_breaks_curvature` |
| `DressingFieldHierarchicalBorel.stage1_preserves_quotient` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldHierarchicalBorel.stage1_preserves_quotient` |
| `DressingFieldHierarchicalBorel.stage1_residual_torus` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldHierarchicalBorel.stage1_residual_torus` |
| `DressingFieldHierarchicalBorel.stage1_tree_edge` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldHierarchicalBorel.stage1_tree_edge` |
| `DressingFieldHierarchicalBorel.stage2_reproduces` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldHierarchicalBorel.stage2_reproduces` |
| `DressingFieldHierarchicalBorel.two_stage_factorization` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldHierarchicalBorel.two_stage_factorization` |
| `DressingFieldHierarchicalBorel.u_N_eq_conjugate` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms DressingFieldHierarchicalBorel.u_N_eq_conjugate` |
| `anchored_transport_unique` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms anchored_transport_unique` |
| `b2_factorization_unique` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms b2_factorization_unique` |
| `b2_semidirect_factorization` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms b2_semidirect_factorization` |
| `b_squared_zero` | yes | yes | yes | propext | `#print axioms b_squared_zero` |
| `badProj_not_homomorphism` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms badProj_not_homomorphism` |
| `carrier_dimension_two_ne_three` | yes | yes | yes | none | `#print axioms carrier_dimension_two_ne_three` |
| `curvature_gauge_covariance` | yes | yes | yes | Quot.sound, propext | `#print axioms curvature_gauge_covariance` |
| `diamond_transport_three` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms diamond_transport_three` |
| `discrete_bianchi_identity` | yes | yes | yes | Quot.sound, propext | `#print axioms discrete_bianchi_identity` |
| `dressed_one_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms dressed_one_iff` |
| `endpoint_dressing_matches_curvature` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms endpoint_dressing_matches_curvature` |
| `factorization_fails_if_singular` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms factorization_fails_if_singular` |
| `source_only_dressing_breaks_curvature` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms source_only_dressing_breaks_curvature` |
| `stage1_preserves_quotient` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms stage1_preserves_quotient` |
| `stage1_residual_torus` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms stage1_residual_torus` |
| `stage1_tree_edge` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms stage1_tree_edge` |
| `stage2_reproduces` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms stage2_reproduces` |
| `torusProj_mul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms torusProj_mul` |
| `two_stage_factorization` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms two_stage_factorization` |
| `u_N_eq_conjugate` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms u_N_eq_conjugate` |
| `unipotent_subgroup_normal` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms unipotent_subgroup_normal` |

- counts toward the grade: yes

### Python: `checks/independent/dfm-hierarchical-borel.py`

- file: [checks/independent/dfm-hierarchical-borel.py](../../../checks/independent/dfm-hierarchical-borel.py)
- sha256 (`bytes`): `0fadffb5b1cff5acd5e6433bacc93e69fa1c04183f97b891eadef46ab8b4557a`
- cited in: node.source, record TFQ-0400
- counts toward the grade: yes

### Documents and data: `dag/derivations/24_dressing_field/tfq_0400_dfm_hierarchical_borel.md`

- file: [dag/derivations/24_dressing_field/tfq_0400_dfm_hierarchical_borel.md](../../../dag/derivations/24_dressing_field/tfq_0400_dfm_hierarchical_borel.md)
- sha256 (`lf-normalised`): `97cce5adfa884fce52e55214ad462ce5e0e74d7f905cf186a5ab8d0a34884cb7`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0400
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/dfm-hierarchical-borel.md`

- file: [dag/derivations/independent/dfm-hierarchical-borel.md](../../../dag/derivations/independent/dfm-hierarchical-borel.md)
- sha256 (`lf-normalised`): `2142d869cdf61cc9ca7d9bbce0779c58762a288ceda40b7377deaacb905c0b02`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_dfm-hierarchical-borel_lean_replay.json`

- file: [dag/research/campaign_dfm-hierarchical-borel_lean_replay.json](../../../dag/research/campaign_dfm-hierarchical-borel_lean_replay.json)
- sha256 (`lf-normalised`): `bbfd0f641dd80bf8f67117ab0e155822dc0f25da129188eeb987ba047121da52`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/hierarchical_nonabelian_dfm_finite_map.md`

- file: [dag/research/hierarchical_nonabelian_dfm_finite_map.md](../../../dag/research/hierarchical_nonabelian_dfm_finite_map.md)
- sha256 (`lf-normalised`): `91082c6bbe1df302b72be629945e0bde9a93bda33d84f0ad308f4f2c6889c445`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-DFM-HIERARCHICAL-BOREL` `DERIVED_LEAN`: [DFM-TREE-CHANGE](DFM-TREE-CHANGE.md) (PROVED_LEAN)

Outgoing (3):

- `APP-R-DFM-BOREL-LEVI-FACTORIZATION` `DERIVED_PROSE`: [DFM-BOREL-LEVI-FACTORIZATION](DFM-BOREL-LEVI-FACTORIZATION.md) (DEFINITION)
- `APP-R-DFM-BOREL-TWO-STAGE-DIAMOND` `COMPUTED`: [DFM-BOREL-TWO-STAGE-DIAMOND](DFM-BOREL-TWO-STAGE-DIAMOND.md) (COMPUTATIONALLY_CHECKED)
- `APP-R-DFM-CONTINUUM-INTERFACE` `GAP_NO_DERIVATION`: [DFM-CONTINUUM-INTERFACE](DFM-CONTINUUM-INTERFACE.md) (OPEN)
