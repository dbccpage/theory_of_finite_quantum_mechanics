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

### Lean: `lean4/Imported/GenesisDerivation/Derivation/Inertia.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/Inertia.lean](../../../lean4/Imported/GenesisDerivation/Derivation/Inertia.lean)
- sha256 (`bytes`): `f13ac6bc0563ae6e1c731e705e79fbb7bd28cc3d287f5bb90ad7fe9fae607f67`
- cited in: node.lean, record TFQ-0513
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.Derivation.Inertia`): recorded sha256 `f13ac6bc0563ae6e1c731e705e79fbb7bd28cc3d287f5bb90ad7fe9fae607f67` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/Inertia.lean`

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
- sha256 (`lf-normalised`): `93f4713452d8c193c2d4c449cbc9405c20e7d35e9fa6a43febd7c9172f99ac56`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0513
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:75489b76e5af44bcf0edfd71b8b4e127881c8275ecc8b3bfb767d121d38f6d9b:33-35`
- `external:upstream/education/symmetric_group_presentations/code/sn_core.py::S2Collapse`

## Absences recorded by the TFQ records

- TFQ-0513 rust: no Rust check of opaque collapse in the S(n) strand

## Routes

Incoming (1):

- `PGW-R-SN2-OPAQUE-COLLAPSE` `DERIVED_LEAN`: [PGW-SN1-SUPPLY-NOT-ADMISSION](PGW-SN1-SUPPLY-NOT-ADMISSION.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-SN3-COST-TWO-UNARY-MARK` `DERIVED_LEAN`: [PGW-SN3-COST-TWO-UNARY-MARK](PGW-SN3-COST-TWO-UNARY-MARK.md) (PROVED_LEAN)
