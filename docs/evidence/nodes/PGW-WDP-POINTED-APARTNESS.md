# PGW-WDP-POINTED-APARTNESS

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> WDP-CH01-P02: for a pointed relation (X, R, a, b) on a finite carrier, R(a,b) does not imply a ≠ b (one-point carrier with R = {(a,a)} and b = a), a ≠ b does not imply R(a,b) (the empty relation on two points), and R(a,b) with R irreflexive implies a ≠ b, since a = b would give R(a,a). Irreflexivity is therefore a declared ingredient of the admitted package, not a consequence of relatedness, and a carrier hosting an irreflexive related pair has at least two elements; PrimDiff.lean states the same endpoint fact for an irreflexive witness. The Python census over every pointed relation on carriers of size 1 to 3 counts 4674 relations, 2337 with R(a,b), 196 with R(a,b) and R irreflexive, 3104 with a ≠ b, and none with R irreflexive, R(a,b) and a = b.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared irreflexivity law on the relation R (assumption)

## Bottleneck

Lean pointed_relation_independence_fin gives the Fin 1 and Fin 2 countermodels and the irreflexive implication over every type; the census stops at size 3, and neither the relation nor the irreflexivity law is derived from \<\>.

## Source status

WDP monograph §1.4 WDP-CH01-P02; Lean PointedRelation.pointed_relation_independence_fin; Python census to size 3

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/PointedRelation.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/PointedRelation.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/PointedRelation.lean)
- sha256 (`bytes`): `9a5d905d70db6124a31a54d1616dfb70308ee04c095302061e86919afbe9d5d8`
- cited in: node.lean, record TFQ-0537
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.WitnessedDifference.WitnessedDifference.PointedRelation`): recorded sha256 `9a5d905d70db6124a31a54d1616dfb70308ee04c095302061e86919afbe9d5d8` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/PointedRelation.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `pointed_relation_independence_fin` | yes | yes | yes | propext | `#print axioms pointed_relation_independence_fin` |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_pointed_relation.py`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_pointed_relation.py](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_pointed_relation.py)
- sha256 (`bytes`): `4390bd6e7e5874e1634047828d8ab4dac7c4ed26e6823f09e6cd7ffcfec884bc`
- cited in: record TFQ-0537
- check: `python -m pytest atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_pointed_relation.py::test_census_matches_the_closed_forms_on_carriers_up_to_three`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_census_matches_the_closed_forms_on_carriers_up_to_three` (python_test) | yes | yes | yes | - | `python -m pytest atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_pointed_relation.py::test_census_matches_the_closed_forms_on_carriers_up_to_three` |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/pointed_relation.py`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/pointed_relation.py](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/pointed_relation.py)
- sha256 (`bytes`): `cb5677d478bc16e2b26d182c3b0e8bb4ca8eaad3de687c4e1d80999b1935b70f`
- cited in: record TFQ-0537

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `enumerate_pointed_relations` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/genesis_to_wdp_derivation_programme.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/genesis_to_wdp_derivation_programme.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/genesis_to_wdp_derivation_programme.md)
- sha256 (`lf-normalised`): `616280b727abb20440caea09709a0e8f5512fbc8de20da8a3db124de2dc262ff`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md)
- sha256 (`lf-normalised`): `753d1c99c799f84f9a71912b98082d590c89c531f980c112b62ee2a86ab2726b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0537_wdp_pointed_apartness.md`

- file: [dag/derivations/06_wdp/tfq_0537_wdp_pointed_apartness.md](../../../dag/derivations/06_wdp/tfq_0537_wdp_pointed_apartness.md)
- sha256 (`lf-normalised`): `f806febdaebabfbdb70d7ffbaa25e933d1a97f6fb93465aa7dce6323931819d5`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0537
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:3301e36106cfe1fb4415d4f6218951cd83516f0a714d773fcb477ea3dce63814::GenesisAdmissionKernel`
- `external:sha256:b3182646c084a1d31b4c382572524489dcfa76f74bf74ee0863573424d048c65:165-170`
- `external:upstream/external:sha256:3301e36106cfe1fb4415d4f6218951cd83516f0a714d773fcb477ea3dce63814::GenesisAdmissionKernel`

## Routes

Incoming (1):

- `PGW-R-WDP-POINTED-APARTNESS` `DERIVED_LEAN`: [PG-ADMISSION-FLOOR](PG-ADMISSION-FLOOR.md) (PROVED_LEAN), [PGW-SN-ENDPOINT-LEMMA](PGW-SN-ENDPOINT-LEMMA.md) (PROVED_LEAN)

Outgoing (0):

