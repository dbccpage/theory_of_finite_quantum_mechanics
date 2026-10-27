# CT-INFORMATION-MEDIA-INTEROPERABILITY

Stage: [CONSTRUCTOR_THEORY](../stages/CONSTRUCTOR_THEORY.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Imported principles, audited and corrected against Deutsch and Marletto (2015, arXiv:1405.5563, Sections 3-6 pp. 9-12): a computation variable is a set S of at least two possible attributes for which all permutation tasks are possible with side-effects (Section 3 p. 9); a variable S is clonable if the cloning task R_S(x0) = union_{x in S} {(x, x0) -\> (x, x)} is possible with side-effects for some preparable blank attribute x0 (Section 4 eq. (3) p. 10); an information variable is a clonable computation variable, and an information medium is a substrate with at least one information variable (Section 4 p. 10). Distinguishability is defined afterward in Section 5 (eq. (4) p. 11) by mapping into an information variable, avoiding circularity, and every information variable is then shown to be distinguishable. Principle III (interoperability, Section 6 p. 12) states that the composite S1 + S2 of two substrates with information variables S1 and S2 is an information medium with information variable S1 x S2.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 6
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- information medium and interoperability principle (assumption)

## Bottleneck

The declared functional task model does not prove the physical possibility of cloning or joint operations with side-effects. The imported interoperability principle and any Hilbert tensor-product/local-tomography conclusion remain separate obligations. Original target retained as an obligation: Imported principles, audited and corrected against Deutsch and Marletto (2015, arXiv:1405.5563, Sections 3-6 pp. 9-12): a computation variable is a set S of at least two possible attributes for which all permutation tasks are possible with side-effects (Section 3 p. 9); a variable S is clonable if the cloning task R_S(x0) = union_{x in S} {(x, x0) -\> (x, x)} is possible with side-effects for some preparable blank attribute x0 (Section 4 eq. (3) p. 10); an information variable is a clonable computation variable, and an information medium is a substrate with at least one information variable (Section 4 p. 10). Distinguishability is defined afterward in Section 5 (eq. (4) p. 11) by mapping into an information variable, avoiding circularity, and every information variable is then shown to be distinguishable. Principle III (interoperability, Section 6 p. 12) states that the composite S1 + S2 of two substrates with information variables S1 and S2 is an information medium with information variable S1 x S2. Prior boundary: The interoperability principle (Principle III, Section 6 p. 12) constrains composite information variables to include S1 x S2 in the source's framework. It is not shown to select the Hilbert tensor product, local tomography or any positive cone, so it does not discharge FQ-GAP-TENSOR-UNIQUENESS.

## Source status

Audited and corrected against the full text of arXiv:1405.5563 (Sections 3-6, eqs. (3)-(4), Principle III, pp. 9-12) on 2026-10-22; taken as an imported assumption of this branch.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/InformationProductBoundary.lean`

- file: [lean4/InformationProductBoundary.lean](../../../lean4/InformationProductBoundary.lean)
- sha256 (`bytes`): `b9fb0fc2e132c89a49c4068013d2e5e36de23d25b366bf9c6ea9e8f400780687`
- cited in: node.lean, receipt dag/research/campaign_ct-information-media-interoperability_lean_replay.json (InformationProductBoundary), receipt dag/research/pr_381_round2_replay.json (InformationProductBoundary), record TFQ-2006
- replay: `verified`
  - receipt [dag/research/campaign_ct-information-media-interoperability_lean_replay.json](../../../dag/research/campaign_ct-information-media-interoperability_lean_replay.json) (module `InformationProductBoundary`): recorded sha256 `b9fb0fc2e132c89a49c4068013d2e5e36de23d25b366bf9c6ea9e8f400780687` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
  - receipt [dag/research/pr_381_round2_replay.json](../../../dag/research/pr_381_round2_replay.json) (module `InformationProductBoundary`): recorded sha256 `b9fb0fc2e132c89a49c4068013d2e5e36de23d25b366bf9c6ea9e8f400780687` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build InformationProductBoundary`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `InformationProductBoundary.Clones` | yes | yes | yes | none | `#print axioms InformationProductBoundary.Clones` |
| `InformationProductBoundary.clones_product` | yes | yes | yes | propext | `#print axioms InformationProductBoundary.clones_product` |
| `InformationProductBoundary.controlledFlip` | yes | yes | yes | none | `#print axioms InformationProductBoundary.controlledFlip` |
| `InformationProductBoundary.controlledFlip_involution` | yes | yes | yes | none | `#print axioms InformationProductBoundary.controlledFlip_involution` |
| `InformationProductBoundary.controlledFlip_not_product` | yes | yes | yes | propext | `#print axioms InformationProductBoundary.controlledFlip_not_product` |
| `InformationProductBoundary.productCloner` | yes | yes | yes | none | `#print axioms InformationProductBoundary.productCloner` |

- counts toward the grade: yes

### Python: `checks/independent/ct-information-media-interoperability.py`

- file: [checks/independent/ct-information-media-interoperability.py](../../../checks/independent/ct-information-media-interoperability.py)
- sha256 (`bytes`): `15b0f6e62a64db4abb02d6f3af2a1b22957eb3b04028ec61067806316e20d17f`
- cited in: record TFQ-2006
- counts toward the grade: yes

### Documents and data: `dag/derivations/30_constructor_theory/tfq_2006_ct_information_media_interoperability.md`

- file: [dag/derivations/30_constructor_theory/tfq_2006_ct_information_media_interoperability.md](../../../dag/derivations/30_constructor_theory/tfq_2006_ct_information_media_interoperability.md)
- sha256 (`lf-normalised`): `81f9d87587f4294c426d59421df0173e09fdb9255e7d338791dad2ddf30c117f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2006
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/ct-information-media-interoperability.md`

- file: [dag/derivations/independent/ct-information-media-interoperability.md](../../../dag/derivations/independent/ct-information-media-interoperability.md)
- sha256 (`lf-normalised`): `70ca57ba6ff044bc594ad5e1590a5fd2c6e4a0abc80416055b46f7bfb4409d9a`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_ct-information-media-interoperability_lean_replay.json`

- file: [dag/research/campaign_ct-information-media-interoperability_lean_replay.json](../../../dag/research/campaign_ct-information-media-interoperability_lean_replay.json)
- sha256 (`lf-normalised`): `f06441262630cd2f64087940c11d19dd79698ea74d508356bc0999856385c336`
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
