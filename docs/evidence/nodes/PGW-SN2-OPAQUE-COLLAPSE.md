# PGW-SN2-OPAQUE-COLLAPSE

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> S(2) retains opaque wholes: reading L admits (\<a\>, \<ab\>) and reading F admits (\<\>, \<a\>, \<ab\>). R2L_collapsed and R2F_collapsed show that every pair of admitted data stays observationally collapsed before distinguishing instances are admitted, so two externally different inscriptions remain internally indistinguishable, and the source does not decompose \<ab\> into a and b. A collapsed pair by itself is not an active obstruction; it becomes one only when a supplied question or separation requirement demands different answers. The later flat grammar sn.ebnf parses \<ab\> as a pair of glyphs, which is a new interpretation with its own parser.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Collapse is relative to the source's derivability profiles; the ledger value s₂ = 1 needs a supplied separation demand, and a two-vertex graph or permutation representation of the pair (as in S2Collapse) is declared structure, not an admitted directed relation.

## Source status

genesis_source.txt sections 6 and 9 (Challenge 2, continuation); 002_oesn level_02_relational_pairings.md; Lean Derivation/Inertia

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean)
- sha256 (`bytes`): `9386f41cf6bbefae8ccb8fdae47f69a33140a0c45b3e6ca9a08f1e9596a922a7`
- cited in: node.lean, record TFQ-0513
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Inertia`): recorded sha256 `9386f41cf6bbefae8ccb8fdae47f69a33140a0c45b3e6ca9a08f1e9596a922a7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `R2F_collapsed` | yes | yes | yes | propext | `#print axioms R2F_collapsed` |
| `R2L_collapsed` | yes | yes | yes | propext | `#print axioms R2L_collapsed` |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt)
- sha256 (`lf-normalised`): `8e0a3f2333e9ae5740b26c59f88fd41cd1ee9c9b92ca4f0a19dad53747ddf3cd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0513_sn2_opaque_collapse.md`

- file: [dag/derivations/05_mssn_sn/tfq_0513_sn2_opaque_collapse.md](../../../dag/derivations/05_mssn_sn/tfq_0513_sn2_opaque_collapse.md)
- sha256 (`lf-normalised`): `a7a93e2843f67775d421154ddb7e51fb5376d71953384c843995ddc7a7e50bc8`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0513
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/levels/level_02_relational_pairings.md`

- file: `omega_engine_education/documentation/002_oesn/levels/level_02_relational_pairings.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:upstream/omega_engine_education/documentation/002_oesn/code/sn_core.py::S2Collapse`

## Absences recorded by the TFQ records

- TFQ-0513 rust: no Rust check of opaque collapse in the S(n) strand

## Routes

Incoming (1):

- `PGW-R-SN2-OPAQUE-COLLAPSE` `DERIVED_LEAN`: [PGW-SN1-SUPPLY-NOT-ADMISSION](PGW-SN1-SUPPLY-NOT-ADMISSION.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-SN3-COST-TWO-UNARY-MARK` `DERIVED_LEAN`: [PGW-SN3-COST-TWO-UNARY-MARK](PGW-SN3-COST-TWO-UNARY-MARK.md) (PROVED_LEAN)
