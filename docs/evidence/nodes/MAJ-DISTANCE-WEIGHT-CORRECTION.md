# MAJ-DISTANCE-WEIGHT-CORRECTION

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `OPEN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> With d = min{wt(z) : z in ker Q minus B}, the weight-bounded set E_t = {e : wt(e) \<= t} satisfies the recovery criterion if and only if 2t \< d.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Knill-Laflamme conditions P Ea^dagger Eb P = c_ab P (cited for general channels)

## Bottleneck

Write the two-direction weight argument from Theorem 4.4 (sum of two weight-t errors has weight at most 2t; a weight-d logical splits into two weight-at-most-t halves when d \<= 2t); the Knill-Laflamme correspondence is cited, not derived.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-COR-DISTANCE-WEIGHT claims PROVED_PROSE; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `code/rust/src/majorana/repair_capacity.rs`

- file: [code/rust/src/majorana/repair_capacity.rs](../../../code/rust/src/majorana/repair_capacity.rs)
- sha256 (`bytes`): `bc76df0ad5de2ff252284f581fc68812d1654cf8e794f648b2db1bf0cf0eb835`
- cited in: node.rust, record TFQ-1148

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `assert_repair_capacity_invariant` (rust_symbol) | yes | yes | yes | - | - |
| `repair_capacity_from_distance` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1148_maj_distance_weight_correction.md`

- file: [dag/derivations/28_majorana/tfq_1148_maj_distance_weight_correction.md](../../../dag/derivations/28_majorana/tfq_1148_maj_distance_weight_correction.md)
- sha256 (`lf-normalised`): `b69fb4ac02de0f48870476bd4bdae698b68df99eff9f3b92ea1f3c32a606a482`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1148
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `e92416bb1739e51de20a8ad6a26d4b5f3d76b974d7556507b13149b29e8edb47`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-DISTANCE-WEIGHT-CORRECTION` `GAP_NO_DERIVATION`: [MAJ-SYNDROME-RECOVERY-CRITERION](MAJ-SYNDROME-RECOVERY-CRITERION.md) (PROVED_PROSE)

Outgoing (0):

