# PGW-RUNG0-INHERITANCE-REPLAY

Stage: [GENESIS](../stages/GENESIS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Rung zero of the second derivation (pull request 130) answers Challenge 0 at stated scope: the sealed challenge reports and both sealed closed baselines regenerate exactly (reading L, 4 nodes, 3 terminal; reading F, 20 nodes, 16 terminal). The sealed grammar has six event kinds, of which only the supply preserves the state, and the two remaining declared inputs are named: the stake and the stream. Inertia is a finite computation from both readings: up to eight supplies leave the regime unchanged, and growth to five data under the all-free stake admits no form, raises no demand and leaves every state totally collapsed. The only Lean evidence cited is the sealed supply_no_op.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 1 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- Sealed genesis kernel, its receipts and the two sealed Python genesis readings L and F as bases (assumption)

## Bottleneck

A finite computation to eight supplies and five data plus the sealed supply_no_op; it does not show that nothing follows from the inheritance beyond those bounds, and rung zero is not blind to its author's expectation, since the seed's author ran it.

## Source status

continuation.txt section 4 row 0 and section 6 rung zero; run ledger SD-00-1 to SD-00-5; finite computation

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisDerivation/Derivation/Inertia.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/Inertia.lean](../../../lean4/Imported/GenesisDerivation/Derivation/Inertia.lean)
- sha256 (`bytes`): `f13ac6bc0563ae6e1c731e705e79fbb7bd28cc3d287f5bb90ad7fe9fae607f67`
- cited in: node.lean, record TFQ-0462
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.Derivation.Inertia`): recorded sha256 `f13ac6bc0563ae6e1c731e705e79fbb7bd28cc3d287f5bb90ad7fe9fae607f67` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/Inertia.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `supply_no_op` | yes | yes | yes | propext | `#print axioms supply_no_op` |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/supply.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/supply.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/supply.rs)
- sha256 (`bytes`): `4d659fa55dec91d900e307d56244065f52eb9dad695ff3acf256ebb66e9b67fc`
- cited in: node.rust, record TFQ-0462

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `supply` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt)
- sha256 (`lf-normalised`): `7e774b9a5cd0b326f884716c49a18055df522968e659438910dceeaa332b73ad`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0462_rung0_inheritance_replay.md`

- file: [dag/derivations/02_genesis/tfq_0462_rung0_inheritance_replay.md](../../../dag/derivations/02_genesis/tfq_0462_rung0_inheritance_replay.md)
- sha256 (`lf-normalised`): `940ccea524dd8be90d25cd8c367596fb80595e8703da6f4dd6169b8e5fe6a292`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0462
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second/claim_ledger.md:104`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_inheritance/inheritance.py::all_free_growth`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_inheritance/inheritance.py::supplies_are_inert`

## Routes

Incoming (1):

- `PGW-R-RUNG0-INHERITANCE-REPLAY` `COMPUTED`: [PGW-GENESIS-THREE-AXIS-VERDICT](PGW-GENESIS-THREE-AXIS-VERDICT.md) (COMPUTATIONALLY_CHECKED)

Outgoing (2):

- `PGW-R-RUNG1-STREAM-AS-RESPONSE` `GAP_NO_DERIVATION`: [PGW-RUNG1-STREAM-AS-RESPONSE](PGW-RUNG1-STREAM-AS-RESPONSE.md) (OPEN)
- `PGW-R-RUNG2A-STAKE-DECLARED-LABEL` `CONDITIONAL_ON_IMPORT`: [PGW-RUNG2A-STAKE-DECLARED-LABEL](PGW-RUNG2A-STAKE-DECLARED-LABEL.md) (CONDITIONAL)
