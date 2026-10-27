# PGW-SN-TWO-BOXED-LAWS

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `DEFINITION`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The S(n) strand states two boxed laws: S(n+1) may contain only structure forced by an unresolved Genesis obstruction at S(n), and a mathematical realization R(S(n)) has no authority to extend S(n). sn.md section 1 reads them as design requirements on later work, not as independent theorems that force the next event, and accepts an external continuation request and a chosen response grammar as recorded inputs. A property shown in a model returns to Genesis only through an explicitly proved reflection bridge. No checker enforces the two laws; they mark which arguments are not allowed.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- The S(n) stage labels and the two boxed laws, declared by the 002_oesn strand and not by 19L57G1 (assumption)

## Bottleneck

Design rules with no checker, not theorems: the archived 000_sn ledger row SN-C01 labelled the realization law a proved law, but that archive is superseded and this record does not adopt the label; evaluate_two_boxed_laws_gate in the MSS-N Rust crate tests supplied flags and does not enforce either law.

## Source status

002_oesn sn.md section 1 and curriculum.md Lesson 1 (declared design rules)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `education/minimal_symbol_systems/code/rust/src/obstruction_detector.rs`

- file: [education/minimal_symbol_systems/code/rust/src/obstruction_detector.rs](../../../education/minimal_symbol_systems/code/rust/src/obstruction_detector.rs)
- sha256 (`bytes`): `439bafc4a90225a06b9e80fb2d9458ecd3718cd1908db47b734056ef8b6c3de2`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `evaluate_two_boxed_laws_gate` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/source_archive/000_sn/paper_claim_ledger.md`

- file: [atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/source_archive/000_sn/paper_claim_ledger.md](../../../atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/source_archive/000_sn/paper_claim_ledger.md)
- sha256 (`lf-normalised`): `e6e075190c6de2815dc0997bdecf3e1d34ec1fec0baded0aceb47bc64320c637`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0510_sn_two_boxed_laws.md`

- file: [dag/derivations/05_mssn_sn/tfq_0510_sn_two_boxed_laws.md](../../../dag/derivations/05_mssn_sn/tfq_0510_sn_two_boxed_laws.md)
- sha256 (`lf-normalised`): `5143f7c71e2b364646286bdc0a372bb2fa4d426a024f3a4184f990e622d5dcca`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0510
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:7cd90f66662c2628f0fcc5d8fb3154cfa6b0c4274de439fb73be21b2eb5673f7:26-30`
- `external:sha256:a51ceb8d0d5703baac230c14caa4638cf25f3ae46fdc77013c7e09f27caaa1e9:26-33`
- `external:upstream/education/minimal_symbol_systems/code/rust/src/obstruction_detector.rs::evaluate_two_boxed_laws_gate`

## Absences recorded by the TFQ records

- TFQ-0510 lean4: no Lean statement of the boxed laws; they are declared design rules
- TFQ-0510 python: no Python check of the boxed laws

## Routes

Incoming (1):

- `PGW-R-SN-TWO-BOXED-LAWS` `DERIVED_PROSE`: [PGW-GENESIS-TO-SN-CROSSWALK](PGW-GENESIS-TO-SN-CROSSWALK.md) (DEFINITION), [TFQ-0368](TFQ-0368.md) (SOURCE_RECORD), [PGW-DECLARED-CHALLENGE-IMPORT-PER-LEVEL](PGW-DECLARED-CHALLENGE-IMPORT-PER-LEVEL.md) (DEFINITION)

Outgoing (2):

- `GTH-R-GTH-LANG-CORE` `GAP_NO_DERIVATION`: [GTH-LANG-CORE](GTH-LANG-CORE.md) (OPEN)
- `PGW-R-SN0-GROUND-INERTIA` `DERIVED_LEAN`: [PGW-SN0-GROUND-INERTIA](PGW-SN0-GROUND-INERTIA.md) (PROVED_LEAN)
