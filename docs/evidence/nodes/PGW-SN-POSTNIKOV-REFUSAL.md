# PGW-SN-POSTNIKOV-REFUSAL

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The construction index n of S(n) is distinct from Postnikov depth j. For j ≥ 0 the Postnikov truncations of a fixed space preserve π₀, so an empty space followed by a point cannot be two truncations of one space. If a topological realization ρ is supplied, its tower at fixed n is written P_j(ρ(S(n))) with its own hypotheses, and growth across n stays a separate construction that needs its own maps and preservation proofs. The combined paper lists S(n) is automatically a Postnikov tower among withdrawn inferences, and ledger row WDP-P001-017 withdraws automatic Postnikov structure.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- A topological realization ρ of S(n) with preservation maps, which the source does not supply (assumption)

## Bottleneck

This refuses the identification of S(n) with a Postnikov tower; it constructs no realization ρ and no Postnikov tower of one, and the withdrawn WDP-P001-017 row is not reactivated.

## Source status

Postnikov pi0 preservation vs S(0)-\>S(1) component change and (n,j) independence mechanized in WdpBatch8.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch8.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch8.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch8.lean)
- sha256 (`bytes`): `42063910b1edb4aa7f509fb0310b262235a7ce77dd5d2e3a5cf03556ecb175b1`
- cited in: node.lean, record TFQ-0520
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch8.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch8.postnikov_preserves_pi0_refutes_sn_tower` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch8.postnikov_preserves_pi0_refutes_sn_tower` |
| `WitnessedDifference.WdpBatch8.sn_stage_and_postnikov_depth_independent` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch8.sn_stage_and_postnikov_depth_independent` |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md`

- file: [atlas/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md](../../../atlas/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md)
- sha256 (`lf-normalised`): `a4a7d840b11e912896032aebc9ead95f7978c0e6f60656f44645c6d8fadf593b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/paper_claim_ledger.md`

- file: [atlas/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/paper_claim_ledger.md](../../../atlas/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/paper_claim_ledger.md)
- sha256 (`lf-normalised`): `ca7ad135453d393688ceadf73eb214ccc6976589928f1dc43597e287bbfc6209`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0520_sn_postnikov_refusal.md`

- file: [dag/derivations/05_mssn_sn/tfq_0520_sn_postnikov_refusal.md](../../../dag/derivations/05_mssn_sn/tfq_0520_sn_postnikov_refusal.md)
- sha256 (`lf-normalised`): `6267ecbfa69e11b75dc17cc96ba88082cf1f8a156d80fee4693769e5565393c2`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0520
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:7cd90f66662c2628f0fcc5d8fb3154cfa6b0c4274de439fb73be21b2eb5673f7:106-109`

## Absences recorded by the TFQ records

- TFQ-0520 python: no Python check of Postnikov truncations
- TFQ-0520 rust: no Rust check of Postnikov truncations

## Routes

Incoming (1):

- `PGW-R-SN-POSTNIKOV-REFUSAL` `DERIVED_LEAN`: [PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL](PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-GENESIS-BRIDGES-LEDGER` `DERIVED_PROSE`: [PGW-WDP-GENESIS-BRIDGES-LEDGER](PGW-WDP-GENESIS-BRIDGES-LEDGER.md) (DEFINITION)
