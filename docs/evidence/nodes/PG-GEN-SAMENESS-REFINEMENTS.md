# PG-GEN-SAMENESS-REFINEMENTS

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Derivations 22-25 sameness refinements (together pairs, raising terms, filled terms, filled triples) and their loop, two-way, and triangle circulation invariants are mechanized in Twentysecond..Twentyfifth and WdpBatch4.lean.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 7 Lean reference(s) cited, 7 in this checkout (replay: none 7). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Claim ledgers 22-25 inventoried and sameness refinement invariants mechanized in Twentysecond..Twentyfifth and WdpBatch4.lean; continuum limits remain outside scope.

## Source status

MECHANIZED in Twentysecond..Twentyfifth Lean modules and WdpBatch4.lean

## Review

- PFP review: [evidence/results/PG-GEN-SAMENESS-REFINEMENTS/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../evidence/results/PG-GEN-SAMENESS-REFINEMENTS/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Actual excess/plain/together arrays, cancellation cost and bounded two-term rewriting orbits are exact; pointwise excess/cost identities are kernel checked.
  - does not support: Formalize the generated-sameness equivalence with rewriting, then address raising (23), filled terms (24) and filled triples/balance (25). Their ledgers are inspected source material, not newly verified results.
  - next test: Formalize the generated-sameness equivalence with rewriting, then address raising (23), filled terms (24) and filled triples/balance (25). Their ledgers are inspected source material, not newly verified results.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/genesis_ongoing/lean4_core/Twentyfifth/Balance.lean`

- file: [atlas/finite_obstruction_calculus/genesis_ongoing/lean4_core/Twentyfifth/Balance.lean](../../../atlas/finite_obstruction_calculus/genesis_ongoing/lean4_core/Twentyfifth/Balance.lean)
- sha256 (`bytes`): `ae7ea5f7e16d1736a20387d0538beeeca21a96fe2e8a82d84737a6c6c52cdc95`
- cited in: node.lean, record TFQ-0391
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/genesis_ongoing/lean4_core/Twentyfifth/Balance.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Twentyfifth.nothing_balanced` | yes | yes | yes | - | `#print axioms Twentyfifth.nothing_balanced` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/genesis_ongoing/lean4_core/Twentyfourth/Same.lean`

- file: [atlas/finite_obstruction_calculus/genesis_ongoing/lean4_core/Twentyfourth/Same.lean](../../../atlas/finite_obstruction_calculus/genesis_ongoing/lean4_core/Twentyfourth/Same.lean)
- sha256 (`bytes`): `88f1fc73ba8b52ef5379d7253b0dcc192d0c91abedf4ed91f546a0d58355a701`
- cited in: node.lean, record TFQ-0391
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/genesis_ongoing/lean4_core/Twentyfourth/Same.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Twentyfourth.Same24.balances` | yes | yes | yes | - | `#print axioms Twentyfourth.Same24.balances` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/genesis_ongoing/lean4_core/Twentysecond/Same.lean`

- file: [atlas/finite_obstruction_calculus/genesis_ongoing/lean4_core/Twentysecond/Same.lean](../../../atlas/finite_obstruction_calculus/genesis_ongoing/lean4_core/Twentysecond/Same.lean)
- sha256 (`bytes`): `08b55ce30724b47a6300012fbdc08bbecf3ef4b8f7689665bf900079cd8555c6`
- cited in: node.lean, record TFQ-0391
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/genesis_ongoing/lean4_core/Twentysecond/Same.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Twentysecond.same_iff_excess` | yes | yes | yes | - | `#print axioms Twentysecond.same_iff_excess` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/genesis_ongoing/lean4_core/Twentythird/Same.lean`

- file: [atlas/finite_obstruction_calculus/genesis_ongoing/lean4_core/Twentythird/Same.lean](../../../atlas/finite_obstruction_calculus/genesis_ongoing/lean4_core/Twentythird/Same.lean)
- sha256 (`bytes`): `42ed016bc8b42d4a442ad149c8bc57a78ed041ed60aa6a02722575ff2743868e`
- cited in: node.lean, record TFQ-0391
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/genesis_ongoing/lean4_core/Twentythird/Same.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Twentythird.Same.same3` | yes | yes | yes | - | `#print axioms Twentythird.Same.same3` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch4.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch4.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch4.lean)
- sha256 (`bytes`): `4f63ebe575318a31ee55f58fe2008082727873250bd2ddcfc0ee960086a56e19`
- cited in: node.lean, record TFQ-0391
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch4.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch4.same23_preserves_around` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch4.same23_preserves_around` |
| `WitnessedDifference.WdpBatch4.same24_balances_iff` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch4.same24_balances_iff` |
| `WitnessedDifference.WdpBatch4.same25_balances_iff` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch4.same25_balances_iff` |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/genesis_ongoing/run_contract.md`

- file: [atlas/finite_obstruction_calculus/genesis_ongoing/run_contract.md](../../../atlas/finite_obstruction_calculus/genesis_ongoing/run_contract.md)
- sha256 (`lf-normalised`): `fc831dfb1ad1e60db868714fb801c437532ac6aa5443e2b3845c303c9c463392`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md)
- sha256 (`lf-normalised`): `e411f9eace9de18c2583922d16d85be03fcbe4c35976ca3d7a33a0c3cfdea143`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0391_sameness_refinement_ledgers.md`

- file: [dag/derivations/02_genesis/tfq_0391_sameness_refinement_ledgers.md](../../../dag/derivations/02_genesis/tfq_0391_sameness_refinement_ledgers.md)
- sha256 (`lf-normalised`): `8a0f72ad1f42f1df9a76ebf42fcf098e7512ff3c0cc6d658a6ae8f767424df2c`
- generated view: listed, not counted
- cited in: record TFQ-0391
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_genesis_rewriting_and_sameness_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`

## Absences recorded by the TFQ records

- TFQ-0391 python: missing obligation: do not import a sameness refinement into genesis_ongoing/code until the four unread claim ledgers are inventoried
- TFQ-0391 rust: missing obligation: no Rust sameness crate was listed; do not add one from the unread ledgers

## Routes

Incoming (1):

- `PG-R-SAMENESS` `DERIVED_LEAN`: [PG-GEN-ONGOING-FEWEST-CHANGES](PG-GEN-ONGOING-FEWEST-CHANGES.md) (PROVED_LEAN)

Outgoing (0):

