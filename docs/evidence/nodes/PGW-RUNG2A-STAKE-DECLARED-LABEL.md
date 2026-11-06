# PGW-RUNG2A-STAKE-DECLARED-LABEL

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Rung two track one (pull request 136) extends the reconstructed sealed grammar by a declared two-sided stake: a label apart, same or free on every ordered pair of datum indices, free on the diagonal, declared once, with a demand a held labelled pair the regime does not honour. A demand comes from a declared label only, at the level of a definition: the free stake carries no demand at any regime and a supply changes no demand. Supply, imposition and, at a well-formed regime, form admission are demand-inert, and from a well-formed base every run of inert events carries exactly the base's demands, so from a demand-free base no demand is first under such a run. Growth generates an apart demand where no instance is admitted, and a same demand only under a separability hypothesis the rung did not discharge.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- Lean declaration SecondNoFirst.NoFirst.no_first_demand at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondNoFirst.Run.no_demand_is_first_under_an_inert_run at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondNoFirst.Propagate.growth_generates_apart_of_no_insts at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Declared two-sided stake: apart, same or free on each ordered datum pair (assumption)

## Bottleneck

The names no_first_demand and grammar_carries_no_stake are wider than their statements, which are definitional assemblies with no run, first-occurrence or causal-source conclusion; the represented state is not bridged to the sealed regime (L-1), and a sentence giving the first demand of every run one source was withdrawn against a two-admission counterexample.

## Source status

continuation.txt section 5.2 attempt 3 and section 6 rung two track one; run ledger SD-02a-1 to SD-02a-13; Lean at 19L57G1 only; mechanized in WitnessedDifference/WdpBatch10.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10.lean)
- sha256 (`bytes`): `c11c08954dc32c9203e93e7615edd4b6e7ec6320d02543c4617226256a7964d7`
- cited in: node.lean, record TFQ-0464
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch10.free_stake_carries_no_demand` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch10.free_stake_carries_no_demand` |
| `WitnessedDifference.WdpBatch10.growth_generates_apart_of_no_insts` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch10.growth_generates_apart_of_no_insts` |
| `WitnessedDifference.WdpBatch10.rung2a_stake_declared_label_and_growth_cases` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch10.rung2a_stake_declared_label_and_growth_cases` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10Rep.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10Rep.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10Rep.lean)
- sha256 (`bytes`): `bc49f2f3c659583494e3e796ac38a509874bcc8931aeb04542aff9e5b68aab24`
- cited in: node.lean, record TFQ-0464
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch10Rep.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch10Rep.rep_rung2a_stake_declared_label` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch10Rep.rep_rung2a_stake_declared_label` |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/genesis/docs/sources/closeout.txt`

- file: [atlas/finite_obstruction_calculus/genesis/docs/sources/closeout.txt](../../../atlas/finite_obstruction_calculus/genesis/docs/sources/closeout.txt)
- sha256 (`lf-normalised`): `c613e357809438876d1fcec34ea896548f17f4e9d4ea7f21048fafe9451651ac`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt`

- file: [atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt](../../../atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt)
- sha256 (`lf-normalised`): `7e774b9a5cd0b326f884716c49a18055df522968e659438910dceeaa332b73ad`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0464_rung2a_stake_declared_label.md`

- file: [dag/derivations/02_genesis/tfq_0464_rung2a_stake_declared_label.md](../../../dag/derivations/02_genesis/tfq_0464_rung2a_stake_declared_label.md)
- sha256 (`lf-normalised`): `66ec0607cc4f64425ef4937b48f52675618eb6987eb06269271d942a2d4e67ca`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0464
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_nofirst/lean/SecondNoFirst/NoFirst.lean::grammar_carries_no_stake`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_nofirst/lean/SecondNoFirst/NoFirst.lean::no_first_demand`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_nofirst/lean/SecondNoFirst/Propagate.lean::growth_generates_apart_of_no_insts`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_nofirst/lean/SecondNoFirst/Propagate.lean::growth_generates_same`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_nofirst/lean/SecondNoFirst/Run.lean::no_demand_is_first_under_an_inert_run`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_nofirst/nofirst.py::first_demand`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_nofirst/nofirst.py::inert_event_kinds`

## Absences recorded by the TFQ records

- TFQ-0464 rust: the second-derivation rung trees hold no Rust

## Routes

Incoming (1):

- `PGW-R-RUNG2A-STAKE-DECLARED-LABEL` `DERIVED_LEAN`: [PGW-RUNG0-INHERITANCE-REPLAY](PGW-RUNG0-INHERITANCE-REPLAY.md) (PROVED_LEAN)

Outgoing (2):

- `PGW-R-RUNG2B-STAKE-MENU` `DERIVED_LEAN`: [PGW-RUNG2B-STAKE-MENU](PGW-RUNG2B-STAKE-MENU.md) (PROVED_LEAN)
- `PGW-R-RUNG3-FIRST-DEMAND-INDEX` `DERIVED_LEAN`: [PGW-RUNG3-FIRST-DEMAND-INDEX](PGW-RUNG3-FIRST-DEMAND-INDEX.md) (PROVED_LEAN)
