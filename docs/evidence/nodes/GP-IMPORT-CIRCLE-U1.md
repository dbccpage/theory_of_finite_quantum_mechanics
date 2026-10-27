# GP-IMPORT-CIRCLE-U1

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The circle group U(1) as phase group. The leftover (1,1) vs (1,-1) is already seen over {+1,-1}, so it does not select the circle. Under the extra 'not of exponent two' the sign group is excluded; Gaussian units and a three-cycle meet the extra. The circle itself and continuity of a one-parameter phase group stay hypotheses.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 20
- distinct cited Lean declarations covered by a current replay receipt: 12
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- U(1) phase group: assumption
- continuity of one-parameter phase group: assumption

## Bottleneck

The circle group U(1), a continuous one-parameter phase group, and a selector for that circle remain imported. The sign, Gaussian-integer pair and three-cycle examples neither construct U(1) nor rule it out.

## Source status

Lean-checked finite sign, pair and cycle examples; U(1), continuity and the circle selector remain imported.

## Review

- PFP review: [dag/research/pr_391_current_scope_review.json](../../../dag/research/pr_391_current_scope_review.json); file present and sha256 matches the node's record: yes; verdict `scoped_sign_pair_cycle_result_reviewed`; scope effect `caveat_added`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Each sign squares to 1. The pairs (1, 1) and (1, -1) differ, and each of their coordinates is a sign. The integer pair 0, 1 has square norm 1, and the product of that pair with itself is the pair -1, 0, which differs from the pair 1, 0. The map sending 0 to 1, 1 to 2 and 2 to 0 returns 2 at the second step from 0 and returns 0 at the third step from 0.
  - does not support: The circle group U(1), a continuous one-parameter phase group, and a selector for that circle remain imported. The sign, Gaussian-integer pair and three-cycle examples neither construct U(1) nor rule it out.
  - next test: Keep the circle and continuity imports explicit; any broader construction needs a separate statement-level review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CircleU1Import.lean`

- file: [lean4/CircleU1Import.lean](../../../lean4/CircleU1Import.lean)
- sha256 (`bytes`): `aa70a67a514c00e935ad1faa56f34039b1a0c558d3751afbca0507e9fcd64c92`
- cited in: node.lean, receipt dag/research/campaign_gp-import-circle-u1_lean_replay.json (CircleU1Import), receipt dag/research/pr_391_round2_replay.json (CircleU1Import), record TFQ-1030
- replay: `verified`
  - receipt [dag/research/campaign_gp-import-circle-u1_lean_replay.json](../../../dag/research/campaign_gp-import-circle-u1_lean_replay.json) (module `CircleU1Import`): recorded sha256 `aa70a67a514c00e935ad1faa56f34039b1a0c558d3751afbca0507e9fcd64c92` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr_391_round2_replay.json](../../../dag/research/pr_391_round2_replay.json) (module `CircleU1Import`): recorded sha256 `aa70a67a514c00e935ad1faa56f34039b1a0c558d3751afbca0507e9fcd64c92` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CircleU1Import`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CircleU1Import.cyc` | yes | yes | yes | none | `#print axioms CircleU1Import.cyc` |
| `CircleU1Import.cycThrice` | yes | yes | yes | none | `#print axioms CircleU1Import.cycThrice` |
| `CircleU1Import.cycTwice` | yes | yes | yes | none | `#print axioms CircleU1Import.cycTwice` |
| `CircleU1Import.gMul` | yes | yes | yes | none | `#print axioms CircleU1Import.gMul` |
| `CircleU1Import.gNorm` | yes | yes | yes | none | `#print axioms CircleU1Import.gNorm` |
| `CircleU1Import.iNorm` | yes | yes | yes | none | `#print axioms CircleU1Import.iNorm` |
| `CircleU1Import.iSquare` | yes | yes | yes | none | `#print axioms CircleU1Import.iSquare` |
| `CircleU1Import.iSquareNeOne` | yes | yes | yes | none | `#print axioms CircleU1Import.iSquareNeOne` |
| `CircleU1Import.isSign` | yes | yes | yes | none | `#print axioms CircleU1Import.isSign` |
| `CircleU1Import.pairCoordsAreSigns` | yes | yes | yes | none | `#print axioms CircleU1Import.pairCoordsAreSigns` |
| `CircleU1Import.pairsDiffer` | yes | yes | yes | none | `#print axioms CircleU1Import.pairsDiffer` |
| `CircleU1Import.signSquare` | yes | yes | yes | none | `#print axioms CircleU1Import.signSquare` |
| `cycThrice` | yes | yes | yes | none | `#print axioms cycThrice` |
| `cycTwice` | yes | yes | yes | none | `#print axioms cycTwice` |
| `iNorm` | yes | yes | yes | none | `#print axioms iNorm` |
| `iSquare` | yes | yes | yes | none | `#print axioms iSquare` |
| `iSquareNeOne` | yes | yes | yes | none | `#print axioms iSquareNeOne` |
| `pairCoordsAreSigns` | yes | yes | yes | none | `#print axioms pairCoordsAreSigns` |
| `pairsDiffer` | yes | yes | yes | none | `#print axioms pairsDiffer` |
| `signSquare` | yes | yes | yes | none | `#print axioms signSquare` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1030_gp_import_circle_u1.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1030_gp_import_circle_u1.md](../../../dag/derivations/08_l1_to_l2/tfq_1030_gp_import_circle_u1.md)
- sha256 (`lf-normalised`): `bcf454547527a6377c65919fb7633c6c10095ef40c8bbe1a02f6f9bc9398cd8f`
- generated view: listed, not counted
- cited in: record TFQ-1030
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:49250fc3940b574236fe8aeb8acabb9673af35fe28f17474e9deb52ecd18a713#GAP-F001-S000-005`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`
- `external:sha256:a635008d68c51a062b794996dc85a68693522928a157d619d01ffada1ba595f1#PRICE-HD-01`
- `external:sha256:f4ef85f405ba846ddf92fd6bbd8fc7aaa86d658c4678b4b841989f2cb97ee004:152`

## Routes

Incoming (0):


Outgoing (1):

- `X-R-DROP-ONE-CENSUS` `DERIVED_LEAN`: [GP-DROP-ONE-CENSUS](GP-DROP-ONE-CENSUS.md) (PROVED_LEAN)

No incoming route.
