# COMP-C5-CLOSURES-HALTING

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Forward and backward simulation extend to the closures, and the machine halts from c iff some word reachable from a word representing c is irreducible.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 5 Lean reference(s) cited, 5 in this checkout (replay: none 5). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Existential in the target word because a configuration has many padded representations.

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C5b claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisCompTM.lean`

- file: [lean4/GenesisCompTM.lean](../../../lean4/GenesisCompTM.lean)
- sha256 (`bytes`): `5e02374ea98ced960a8d3deef1dd84f1b0d053ef00b268d66804af665e2dfe5c`
- cited in: node.lean, node.source, record TFQ-1300
- replay: `none`
- check: `cd lean4 && lake build GenesisCompTM`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Halts` | yes | yes | yes | - | `#print axioms Halts` |
| `Irreducible` | yes | yes | yes | - | `#print axioms Irreducible` |
| `halts_iff` | yes | yes | yes | - | `#print axioms halts_iff` |
| `reach_bwd` | yes | yes | yes | - | `#print axioms reach_bwd` |
| `reaches_fwd` | yes | yes | yes | - | `#print axioms reaches_fwd` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1300_comp_c5_closures_halting.md`

- file: [dag/derivations/29_computation/tfq_1300_comp_c5_closures_halting.md](../../../dag/derivations/29_computation/tfq_1300_comp_c5_closures_halting.md)
- sha256 (`lf-normalised`): `4e926b8cf5074fbf6098aceb568d8329c7b7b4793dbb971bdde1788f055347e2`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1300
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C5-CLOSURES-HALTING` `DERIVED_LEAN`: [COMP-C5-TM0-STEP-SIMULATION](COMP-C5-TM0-STEP-SIMULATION.md) (PROVED_LEAN)

Outgoing (4):

- `APP-R-COMP-C5-SMALL-MACHINES-CHECKED` `COMPUTED`: [COMP-C5-SMALL-MACHINES-CHECKED](COMP-C5-SMALL-MACHINES-CHECKED.md) (COMPUTATIONALLY_CHECKED)
- `APP-R-COMP-C6-EVAL-HAS-A-CODE` `DERIVED_LEAN`: [COMP-C6-EVAL-HAS-A-CODE](COMP-C6-EVAL-HAS-A-CODE.md) (PROVED_LEAN)
- `APP-R-COMP-C6-TM0-HALTING-EQUIVALENCE` `DERIVED_LEAN`: [COMP-C6-TM0-HALTING-EQUIVALENCE](COMP-C6-TM0-HALTING-EQUIVALENCE.md) (PROVED_LEAN)
- `APP-R-COMP-C7-NF-REACH-UNDECIDABLE` `DERIVED_LEAN`: [COMP-C7-NF-REACH-UNDECIDABLE](COMP-C7-NF-REACH-UNDECIDABLE.md) (PROVED_LEAN)
