# PGW-SN-ENDPOINT-LEMMA

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a supplied irreflexive relation R, R(a,b) implies a ≠ b, since a = b would turn the witness into R(a,a); so the support of an asserted pair has exactly two elements, |{a,b}| = 2. This counts endpoints, not witnesses: single_oriented_witness_consistent builds a model with one forward witness and no reverse witness, so endpoints are 2 while witnesses can be 1. For the pointed two-element directed graph D₂ = ({0,1}, 0→1), each asserted pair (a,b) receives exactly one point-preserving map with f(0) = a and f(1) = b, and that map preserves the edge (D2_initial_pointed).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Irreflexivity and orientation of R as declared inputs, not consequences of \<\> (assumption)

## Bottleneck

D₂ is initial only among pointed structures with an asserted pair; the combined paper says this does not make D₂ initial in an unspecified category of all systems. The sn-wire grammar accepts \<a-\>a\>, so irreflexivity is checked by verify_wir and not by parsing.

## Source status

pregenesis_to_minimal_symbol_systems paper.md section 9; 002_oesn sn.md section 3; Lean SnTheorems and Derivation/PrimDiff

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisDerivation/Derivation/PrimDiff.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/PrimDiff.lean](../../../lean4/Imported/GenesisDerivation/Derivation/PrimDiff.lean)
- sha256 (`bytes`): `c861f21ee5a8b701b4cf4f4acfd8ee03746074c4599827a972bd1c9c17fcd1fe`
- cited in: node.lean, record TFQ-0515
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.Derivation.PrimDiff`): recorded sha256 `c861f21ee5a8b701b4cf4f4acfd8ee03746074c4599827a972bd1c9c17fcd1fe` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/PrimDiff.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `D2_initial_pointed` | yes | yes | yes | propext | `#print axioms D2_initial_pointed` |
| `irrefl_witness_ne` | yes | yes | yes | none | `#print axioms irrefl_witness_ne` |
| `single_oriented_witness_consistent` | yes | yes | yes | none | `#print axioms single_oriented_witness_consistent` |

- counts toward the grade: yes

### Lean: `lean4/Imported/SymmetricGroupPresentations/SnTheorems.lean`

- file: [lean4/Imported/SymmetricGroupPresentations/SnTheorems.lean](../../../lean4/Imported/SymmetricGroupPresentations/SnTheorems.lean)
- sha256 (`bytes`): `1c2c2b2a0774d7bc849eb584d2b135353e6d7ceb0d77041e70c175182ef93016`
- cited in: node.lean, record TFQ-0515
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mssn_sn.json](../../../dag/research/lean_replay_campaign_mssn_sn.json) (module `Imported.SymmetricGroupPresentations.SnTheorems`): recorded sha256 `1c2c2b2a0774d7bc849eb584d2b135353e6d7ceb0d77041e70c175182ef93016` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/SymmetricGroupPresentations/SnTheorems.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `irrefl_witness_distinct` | yes | yes | yes | none | `#print axioms irrefl_witness_distinct` |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md`

- file: [atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md](../../../atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md)
- sha256 (`lf-normalised`): `a4a7d840b11e912896032aebc9ead95f7978c0e6f60656f44645c6d8fadf593b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0515_sn_endpoint_lemma.md`

- file: [dag/derivations/05_mssn_sn/tfq_0515_sn_endpoint_lemma.md](../../../dag/derivations/05_mssn_sn/tfq_0515_sn_endpoint_lemma.md)
- sha256 (`lf-normalised`): `0c0ae8db718764b24787921f89ecbf8367aaba7ed944f743084ab8850b1cb232`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0515
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:17ebebc4a063d888d237da44f44f0937e15f6920e8e6fc63fbdf83909718616c:32-35`
- `external:sha256:7cd90f66662c2628f0fcc5d8fb3154cfa6b0c4274de439fb73be21b2eb5673f7:58-66`
- `external:upstream/education/symmetric_group_presentations/code/sn_audit.py::verify_wir`

## Absences recorded by the TFQ records

- TFQ-0515 rust: no Rust check of the endpoint lemma in the S(n) strand

## Routes

Incoming (1):

- `PGW-R-SN-ENDPOINT-LEMMA` `DERIVED_LEAN`: [PGW-SN3-COST-TWO-UNARY-MARK](PGW-SN3-COST-TWO-UNARY-MARK.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-POINTED-APARTNESS` `DERIVED_LEAN`: [PGW-WDP-POINTED-APARTNESS](PGW-WDP-POINTED-APARTNESS.md) (PROVED_LEAN)
