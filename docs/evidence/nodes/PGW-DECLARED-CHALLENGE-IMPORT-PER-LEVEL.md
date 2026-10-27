# PGW-DECLARED-CHALLENGE-IMPORT-PER-LEVEL

Stage: [GENESIS](../stages/GENESIS.md). Status: `DEFINITION`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Declared here as this programme's stage-change rule: each stage change S(n) to S(n+1) consumes exactly one declared, priced and recorded challenge import, either a fresh datum (external supply) or a new requirement kind (external goal), entered as one row of the demand ledger. It is the sealed external continuation policy (the supply and admission of one fresh opaque token at the closure fixpoint, declared metatheory and not a derived transition) made a typed ledger entry, and it follows the education audit's reading that progression requires one declared challenge import per level. In the Alpha slice the import is host-supplied: the host gives the target pair, the measure and the bounds, and nothing in the harness chooses a next demand.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- External continuation policy of genesis_source §3 item 10, declared metatheory (assumption)
- One-import-per-level budgeting rule, a construction declared by this programme from the education audit (assumption)

## Bottleneck

A declared budgeting policy, not a derived law: it does not show that one import suffices for any later stage, and it supplies no endogenous demand generator (OB-1 stays open).

## Source status

declared here; genesis_source.txt §3 item 10 external continuation policy; ALPHA_HANDOFF §4; education archive §1

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/outside.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/outside.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/outside.rs)
- sha256 (`bytes`): `79461000d78d732752daca76f68288e27be855dc36605c2de578e0478e1798d1`
- cited in: node.rust, record TFQ-0488

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Outside` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py)
- sha256 (`bytes`): `23803a3dcce2adf0dee623caba33791d41a25d2da3fdfd226da3cad2ee140b5e`
- cited in: record TFQ-0488

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `build_tree` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt)
- sha256 (`lf-normalised`): `8e0a3f2333e9ae5740b26c59f88fd41cd1ee9c9b92ca4f0a19dad53747ddf3cd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0488_declared_challenge_import_per_level.md`

- file: [dag/derivations/02_genesis/tfq_0488_declared_challenge_import_per_level.md](../../../dag/derivations/02_genesis/tfq_0488_declared_challenge_import_per_level.md)
- sha256 (`lf-normalised`): `f2424a99c5e12a357b3254eaa8959976aa2e14f660253f0cbc142cdde946e604`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0488
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/docs/ALPHA_HANDOFF.md:78-88`
- `external:sha256:0d098004a566c40656af6035d6e66ff13f7e873b11966677df080686a1b29cf9:947`

## Absences recorded by the TFQ records

- TFQ-0488 lean4: no Lean statement of a per-level import ledger; the class-relative exclusion G1Class.g1_class_exclusion motivates it (TFQ-0487)

## Routes

Incoming (1):

- `PGW-R-DECLARED-CHALLENGE-IMPORT-PER-LEVEL` `DERIVED_PROSE`: [PGW-ENDOGENOUS-DEMANDS-EXOGENOUS-PAYMENTS](PGW-ENDOGENOUS-DEMANDS-EXOGENOUS-PAYMENTS.md) (PROVED_LEAN)

Outgoing (6):

- `PGW-R-CANDIDATE-EXTENSION-GENERATOR` `DERIVED_PROSE`: [PGW-CANDIDATE-EXTENSION-GENERATOR](PGW-CANDIDATE-EXTENSION-GENERATOR.md) (DEFINITION)
- `PGW-R-CAPABILITY-STAGE-COUNTER` `DERIVED_PROSE`: [PGW-CAPABILITY-STAGE-COUNTER](PGW-CAPABILITY-STAGE-COUNTER.md) (DEFINITION)
- `PGW-R-K-ITEM-DELTA-GRAMMAR` `GAP_NO_DERIVATION`: [PGW-K-ITEM-DELTA-GRAMMAR](PGW-K-ITEM-DELTA-GRAMMAR.md) (OPEN)
- `PGW-R-SN-TWO-BOXED-LAWS` `DERIVED_PROSE`: [PGW-SN-TWO-BOXED-LAWS](PGW-SN-TWO-BOXED-LAWS.md) (DEFINITION)
- `PGW-R-SN5-CONTINUATION-RECORDED-REQUEST` `DERIVED_PROSE`: [PGW-SN5-CONTINUATION-RECORDED-REQUEST](PGW-SN5-CONTINUATION-RECORDED-REQUEST.md) (DEFINITION)
- `PGW-R-TYPED-REQUIREMENT-KINDS` `DERIVED_PROSE`: [PGW-TYPED-REQUIREMENT-KINDS](PGW-TYPED-REQUIREMENT-KINDS.md) (DEFINITION)
