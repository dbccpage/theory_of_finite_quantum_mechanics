# PGW-SN-ENDPOINT-LEMMA

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a supplied irreflexive relation R, R(a,b) implies a ≠ b, since a = b would turn the witness into R(a,a); so the support of an asserted pair has exactly two elements, |{a,b}| = 2. This counts endpoints, not witnesses: single_oriented_witness_consistent builds a model with one forward witness and no reverse witness, so endpoints are 2 while witnesses can be 1. For the pointed two-element directed graph D₂ = ({0,1}, 0→1), each asserted pair (a,b) receives exactly one point-preserving map with f(0) = a and f(1) = b, and that map preserves the edge (D2_initial_pointed).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
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

000_pre_genesis_to_mssn paper.md section 9; 002_oesn sn.md section 3; Lean SnTheorems and Derivation/PrimDiff

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/PrimDiff.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/PrimDiff.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/PrimDiff.lean)
- sha256 (`bytes`): `1f3f373e979d9199c73ef9e63ea863a0ac41692c247e23052dba6588c6e16f26`
- cited in: node.lean, record TFQ-0515
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.PrimDiff`): recorded sha256 `1f3f373e979d9199c73ef9e63ea863a0ac41692c247e23052dba6588c6e16f26` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/PrimDiff.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `D2_initial_pointed` | yes | yes | yes | propext | `#print axioms D2_initial_pointed` |
| `irrefl_witness_ne` | yes | yes | yes | none | `#print axioms irrefl_witness_ne` |
| `single_oriented_witness_consistent` | yes | yes | yes | none | `#print axioms single_oriented_witness_consistent` |

- counts toward the grade: yes

### Lean: `lean4/Imported/OeSn/SnTheorems.lean`

- file: [lean4/Imported/OeSn/SnTheorems.lean](../../../lean4/Imported/OeSn/SnTheorems.lean)
- sha256 (`bytes`): `acbabe52a9557e71a1ca32cd81122a70859a1f25c7c4654ec78102c8fc1fcf81`
- cited in: node.lean, record TFQ-0515
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mssn_sn.json](../../../dag/research/lean_replay_campaign_mssn_sn.json) (module `Imported.OeSn.SnTheorems`): recorded sha256 `acbabe52a9557e71a1ca32cd81122a70859a1f25c7c4654ec78102c8fc1fcf81` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/OeSn/SnTheorems.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `irrefl_witness_distinct` | yes | yes | yes | none | `#print axioms irrefl_witness_distinct` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0515_sn_endpoint_lemma.md`

- file: [dag/derivations/05_mssn_sn/tfq_0515_sn_endpoint_lemma.md](../../../dag/derivations/05_mssn_sn/tfq_0515_sn_endpoint_lemma.md)
- sha256 (`lf-normalised`): `3d27653739452eabf32ead4c115c2d46e42f069c4fa23d59639ea9960b8f3490`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0515
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/reading_guide.md`

- file: `omega_engine_education/documentation/002_oesn/reading_guide.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/sn.md`

- file: `omega_engine_education/documentation/002_oesn/sn.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:upstream/omega_engine_education/documentation/002_oesn/code/sn_audit.py::verify_wir`

## Absences recorded by the TFQ records

- TFQ-0515 rust: no Rust check of the endpoint lemma in the S(n) strand

## Routes

Incoming (1):

- `PGW-R-SN-ENDPOINT-LEMMA` `DERIVED_LEAN`: [PGW-SN3-COST-TWO-UNARY-MARK](PGW-SN3-COST-TWO-UNARY-MARK.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-POINTED-APARTNESS` `DERIVED_LEAN`: [PGW-WDP-POINTED-APARTNESS](PGW-WDP-POINTED-APARTNESS.md) (PROVED_LEAN)
