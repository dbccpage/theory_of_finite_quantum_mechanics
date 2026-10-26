# PGW-POLICY-ENDPOINT-ALL-SEPARATED

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Call a regime a policy terminal when no unseparated admitted pair i \< j has a valid response. The companion theorem policy_terminal_separates shows that a well-formed policy terminal whose imposed requirements are all separated separates every admitted pair: an unresolved pair would have the fresh-mark response of mark_progress, contradicting terminality. Together with the round bound, an unguarded maximal run of the declared closure policy cannot continue indefinitely and cannot stop on an unresolved pair for lack of a response.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The proof goes by contradiction and its axiom report lists Classical.choice; a bounded implementation can instead stop at a search or resource limit, which is not the all-pairs-separated result.

## Source status

paper.md section 8 written consequence (ledger WDP-P000-016); companion Paper.lean policy_terminal_separates

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Paper.lean`

- file: [lean4/Imported/Genesis19l57g1/Paper.lean](../../../lean4/Imported/Genesis19l57g1/Paper.lean)
- sha256 (`bytes`): `9503a9507c67532a9c0a7a51eb8f3ea66fc8c3371692bab8579b04e77ba4b89c`
- cited in: node.lean, record TFQ-0450
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Paper`): recorded sha256 `9503a9507c67532a9c0a7a51eb8f3ea66fc8c3371692bab8579b04e77ba4b89c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Paper.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `policy_terminal_separates` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms policy_terminal_separates` |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/closure.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/closure.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/closure.rs)
- sha256 (`bytes`): `f9de5073d9258eac42c4e875a0c61f35f8ae2470dc4695097195387f270ec21a`
- cited in: node.rust, record TFQ-0450

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `the_fixpoint_is_empty_and_genesis_has_no_demand` (rust_test) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/engine.py)
- sha256 (`bytes`): `23803a3dcce2adf0dee623caba33791d41a25d2da3fdfd226da3cad2ee140b5e`
- cited in: record TFQ-0450

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `closure_challenge_orbits` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/lean4/axiom_report.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/lean4/axiom_report.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/lean4/axiom_report.txt)
- sha256 (`lf-normalised`): `d975388461d37acf0fbaa4e1d3a45bc854f108461503cfbbe5eb8e4431f10f4d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/paper.md`

- file: [atlas/papers/finite_obstruction_calculus/genesis/paper.md](../../../atlas/papers/finite_obstruction_calculus/genesis/paper.md)
- sha256 (`lf-normalised`): `0dde974e14ff1b54ff6e65705a1194aea38fad7e65bf77b159a07ea1b96bb9a5`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0450_policy_endpoint_all_separated.md`

- file: [dag/derivations/02_genesis/tfq_0450_policy_endpoint_all_separated.md](../../../dag/derivations/02_genesis/tfq_0450_policy_endpoint_all_separated.md)
- sha256 (`lf-normalised`): `31cd092156b836a975063a90b58ad73e7e507ff79fdfcd33446428f448a1168d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0450
- counts toward the grade: no

## Routes

Incoming (1):

- `PGW-R-POLICY-ENDPOINT-ALL-SEPARATED` `DERIVED_LEAN`: [PGW-CLOSED-BASELINE-TERMINATES](PGW-CLOSED-BASELINE-TERMINATES.md) (COMPUTATIONALLY_CHECKED)

Outgoing (1):

- `PGW-R-NO-ENDOGENOUS-DEMAND-GENERATOR` `DERIVED_PROSE`: [PGW-NO-ENDOGENOUS-DEMAND-GENERATOR](PGW-NO-ENDOGENOUS-DEMAND-GENERATOR.md) (PROVED_PROSE)
