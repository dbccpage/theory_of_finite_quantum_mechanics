# PGW-RUNG2A-STAKE-DECLARED-LABEL

Stage: [GENESIS](../stages/GENESIS.md). Status: `CONDITIONAL`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Rung two track one (pull request 136) extends the reconstructed sealed grammar by a declared two-sided stake: a label apart, same or free on every ordered pair of datum indices, free on the diagonal, declared once, with a demand a held labelled pair the regime does not honour. A demand comes from a declared label only, at the level of a definition: the free stake carries no demand at any regime and a supply changes no demand. Supply, imposition and, at a well-formed regime, form admission are demand-inert, and from a well-formed base every run of inert events carries exactly the base's demands, so from a demand-free base no demand is first under such a run. Growth generates an apart demand where no instance is admitted, and a same demand only under a separability hypothesis the rung did not discharge.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Lean declaration SecondNoFirst.NoFirst.no_first_demand at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondNoFirst.Run.no_demand_is_first_under_an_inert_run at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Lean declaration SecondNoFirst.Propagate.growth_generates_apart_of_no_insts at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)
- Declared two-sided stake: apart, same or free on each ordered datum pair (assumption)

## Bottleneck

The names no_first_demand and grammar_carries_no_stake are wider than their statements, which are definitional assemblies with no run, first-occurrence or causal-source conclusion; the represented state is not bridged to the sealed regime (L-1), and a sentence giving the first demand of every run one source was withdrawn against a two-admission counterexample.

## Source status

continuation.txt section 5.2 attempt 3 and section 6 rung two track one; run ledger SD-02a-1 to SD-02a-13; Lean at 19L57G1 only

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/02_genesis/tfq_0464_rung2a_stake_declared_label.md`

- file: [dag/derivations/02_genesis/tfq_0464_rung2a_stake_declared_label.md](../../../dag/derivations/02_genesis/tfq_0464_rung2a_stake_declared_label.md)
- sha256 (`lf-normalised`): `0910cd445e64ad64e83196906623daa8030d780a0325f1c0d1a0e3b8a1867e66`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0464
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
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

- `PGW-R-RUNG2A-STAKE-DECLARED-LABEL` `CONDITIONAL_ON_IMPORT`: [PGW-RUNG0-INHERITANCE-REPLAY](PGW-RUNG0-INHERITANCE-REPLAY.md) (COMPUTATIONALLY_CHECKED)

Outgoing (2):

- `PGW-R-RUNG2B-STAKE-MENU` `COMPUTED`: [PGW-RUNG2B-STAKE-MENU](PGW-RUNG2B-STAKE-MENU.md) (COMPUTATIONALLY_CHECKED)
- `PGW-R-RUNG3-FIRST-DEMAND-INDEX` `CONDITIONAL_ON_IMPORT`: [PGW-RUNG3-FIRST-DEMAND-INDEX](PGW-RUNG3-FIRST-DEMAND-INDEX.md) (CONDITIONAL)
