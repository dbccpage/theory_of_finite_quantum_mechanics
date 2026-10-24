# CT-INFORMATION-MEDIA-INTEROPERABILITY

Stage: [CONSTRUCTOR_THEORY](../stages/CONSTRUCTOR_THEORY.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Imported principle (Deutsch-Marletto Principle III): the composite of two information media is an information medium whose information variable is the Cartesian product of the component information variables, and information can be copied from one medium to another. This gives Cartesian product of attribute sets at the level of information variables, not yet the complex Hilbert tensor product of quantum state spaces. Narrowed in Lean 4 and an independent Python verifier to exact finite/algebraic components and non-selection fences: (1) on ZMod n, cnotClone n (x, y) = (x, x + y) and cnotUnclone n (x, y) = (x, y - x) are two-sided inverses so cnotClone n is a bijection that clones every x from blank 0 and is an involution for n = 2; (2) Fin 1 has 1 permutation and no distinct attributes whereas Fin (n + 2) has distinct attributes 0 != 1 swapped by Equiv.swap 0 1, and any injective encoding separates distinct attributes after cloning; (3) for composite media ZMod n1 x ZMod n2, componentwise cloning compositeClone n1 n2 is bijective with blank (0, 0), |Fin d1 x Fin d2| = d1 * d2, and cross-medium copy composed with any target permutation pi realizes (x1, pi x1); and (4) Principle III does not discharge FQ-GAP-TENSOR-UNIQUENESS because 2-qubit CNOT maps the superposition (1, 0, 1, 0) to the entangled Bell state (1, 0, 0, 1) with Schmidt determinant 1 != 0, the 4-element attribute set Fin 2 x Fin 2 is shared by four distinct composite state-space dimensions (classical simplex 3 \< real local product 9 \< real quantum symmetric 10 \< complex Hermitian 16), and the quantum PSD cone and Partially-Transposed (PT) cone agree on all classical diagonal matrices over {0, 1}^2 and all product vectors while differing on the Bell witness evaluated on the singlet vector.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 11
- cited Lean declarations covered by a current replay receipt: 11
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- information medium and interoperability principle (assumption)

## Bottleneck

Narrowed algebraic checks only. Modular-addition maps have explicit inverses; finite-set cardinalities multiply; supplied integer CNOT/Bell/partial-transpose models obey the displayed polynomial identities. ZMod 0 is infinite, so the arbitrary-n theorem is algebraic rather than an exclusively finite-carrier theorem. The dimension functions are declared formulas, not constructed state spaces; normalized and unnormalized dimensions must not be conflated. The integer quadratic-form example does not construct two full physical cone theories satisfying all constructor axioms. Status is unchanged. The original physical or operational bridge remains open.

## Source status

Taken from the cited source as an assumption of this branch; narrowed to reversible modular-addition cloning on ZMod n, computation variable cardinality threshold and injective distinguishability, Principle III composite Cartesian cloning and cross-medium copy/recoding, and four explicit non-selection fences (2-qubit CNOT off-diagonal entanglement, composite state-space dimension trichotomy 3 \< 9 \< 10 \< 16, real vs complex local tomography holism excess, and PSD vs Partially-Transposed cone separation) in Lean 4 and an independent Python verifier on 2026-10-24.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignCtInformationMediaInteroperability.lean`

- file: [lean4/CampaignCtInformationMediaInteroperability.lean](../../../lean4/CampaignCtInformationMediaInteroperability.lean)
- sha256 (`bytes`): `4f150b51c5e3dba2813c52d547e9b5dbff1420a6477ab31bc3bfab3498d258d4`
- cited in: node.lean, node.source, record TFQ-2006
- replay: `verified`
  - receipt [dag/research/campaign_ct-information-media-interoperability_lean_replay.json](../../../dag/research/campaign_ct-information-media-interoperability_lean_replay.json) (module `CampaignCtInformationMediaInteroperability`): recorded sha256 `4f150b51c5e3dba2813c52d547e9b5dbff1420a6477ab31bc3bfab3498d258d4` matches the current file; exit code 0; Lean None; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignCtInformationMediaInteroperability`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignCtInformationMediaInteroperability.clonable_computation_implies_distinguishable` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignCtInformationMediaInteroperability.clonable_computation_implies_distinguishable` |
| `CampaignCtInformationMediaInteroperability.cnotClone_bijective_and_clones_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignCtInformationMediaInteroperability.cnotClone_bijective_and_clones_zero` |
| `CampaignCtInformationMediaInteroperability.cnotClone_zmod2_involutive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignCtInformationMediaInteroperability.cnotClone_zmod2_involutive` |
| `CampaignCtInformationMediaInteroperability.composite_state_space_dimension_trichotomy_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignCtInformationMediaInteroperability.composite_state_space_dimension_trichotomy_fence` |
| `CampaignCtInformationMediaInteroperability.cross_medium_copy_transfer` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignCtInformationMediaInteroperability.cross_medium_copy_transfer` |
| `CampaignCtInformationMediaInteroperability.principle_III_composite_cloning_and_cardinality` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignCtInformationMediaInteroperability.principle_III_composite_cloning_and_cardinality` |
| `CampaignCtInformationMediaInteroperability.psd_vs_pt_cone_bell_witness_separation_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignCtInformationMediaInteroperability.psd_vs_pt_cone_bell_witness_separation_fence` |
| `CampaignCtInformationMediaInteroperability.psd_vs_pt_cone_classical_interoperability_agreement_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignCtInformationMediaInteroperability.psd_vs_pt_cone_classical_interoperability_agreement_fence` |
| `CampaignCtInformationMediaInteroperability.real_vs_complex_bilinear_tomography_fence` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignCtInformationMediaInteroperability.real_vs_complex_bilinear_tomography_fence` |
| `CampaignCtInformationMediaInteroperability.singleton_not_computation_variable_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignCtInformationMediaInteroperability.singleton_not_computation_variable_fence` |
| `CampaignCtInformationMediaInteroperability.unitary_cnot_clones_computational_basis_not_superposition_fence` | yes | yes | yes | propext | `#print axioms CampaignCtInformationMediaInteroperability.unitary_cnot_clones_computational_basis_not_superposition_fence` |
- counts toward the grade: yes

### Python: `checks/independent/ct-information-media-interoperability.py`

- file: [checks/independent/ct-information-media-interoperability.py](../../../checks/independent/ct-information-media-interoperability.py)
- sha256 (`bytes`): `2f2eed1e1ff96004a1c1f95b9de7b297f1af2d2e7bfcb88c029a8c6695d3d24d`
- cited in: node.source, record TFQ-2006
- counts toward the grade: yes

### Documents and data: `dag/derivations/30_constructor_theory/tfq_2006_ct_information_media_interoperability.md`

- file: [dag/derivations/30_constructor_theory/tfq_2006_ct_information_media_interoperability.md](../../../dag/derivations/30_constructor_theory/tfq_2006_ct_information_media_interoperability.md)
- sha256 (`lf-normalised`): `19ad3faea28577b5036c239408c353887c964612eae08be008e6dd0bfb9b1730`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2006
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/ct-information-media-interoperability.md`

- file: [dag/derivations/independent/ct-information-media-interoperability.md](../../../dag/derivations/independent/ct-information-media-interoperability.md)
- sha256 (`lf-normalised`): `91ae84e81859f3184c6450c50e1e911de48fe51c7728850ad39e7d42058c3403`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_ct-information-media-interoperability_independent.json`

- file: [dag/research/campaign_ct-information-media-interoperability_independent.json](../../../dag/research/campaign_ct-information-media-interoperability_independent.json)
- sha256 (`lf-normalised`): `f78e9f05659cd1e05b9d4a0e57548fd25b6635858b267799496450396350c62d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_ct-information-media-interoperability_lean_mutation.json`

- file: [dag/research/campaign_ct-information-media-interoperability_lean_mutation.json](../../../dag/research/campaign_ct-information-media-interoperability_lean_mutation.json)
- sha256 (`lf-normalised`): `06513ee0022bedb6e7ba7a2aa0f9871fa94c821b9ff9799c43f3f0f6caeedd81`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_ct-information-media-interoperability_lean_replay.json`

- file: [dag/research/campaign_ct-information-media-interoperability_lean_replay.json](../../../dag/research/campaign_ct-information-media-interoperability_lean_replay.json)
- sha256 (`lf-normalised`): `24bd829695eb15c664a97ecf4ae61100d91ba81a3041f532c68afc78d47422f1`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:1405.5563`

## Routes

Incoming (1):

- `FRO-R-CT-INFORMATION-MEDIA-INTEROPERABILITY` `CONDITIONAL_ON_IMPORT`: [CT-DEUTSCH-MARLETTO-2015-SOURCE](CT-DEUTSCH-MARLETTO-2015-SOURCE.md) (SOURCE_RECORD)

Outgoing (2):

- `FRO-R-BACK-CT-INTEROP-TO-TENSOR` `GAP_NO_DERIVATION`: [FQ-GAP-TENSOR-UNIQUENESS](FQ-GAP-TENSOR-UNIQUENESS.md) (CONDITIONAL)
- `FRO-R-CT-SUPERINFORMATION-MEDIUM-DEFINITION` `CONDITIONAL_ON_IMPORT`: [CT-SUPERINFORMATION-MEDIUM-DEFINITION](CT-SUPERINFORMATION-MEDIUM-DEFINITION.md) (IMPORTED_ASSUMPTION)
