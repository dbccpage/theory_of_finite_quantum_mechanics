# L1-QM002-O022A-PHI1-QUOTIENT

Stage: [L1_EMERGENCE](../stages/L1_EMERGENCE.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a finite-dimensional repair packet with c = d0, Phi1(\[x\]) equals the Banach-quotient norm of the cofiber shadow. The Lean statement named in the ledger is definitional, so the analytic identity is carried by the prose proof only. The unrestricted CODA-A bridge is refused / OPEN.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Banach quotient construction on finite-dim packet: lift

## Bottleneck

The identity Phi1(\[x\]) = Banach-quotient norm is not in Lean (the source says its Lean statement is definitional). The cited Lean has the gauge-shift identity on one edge and additivity of an edge residual sum. The prose argument in the source paper has not been reviewed here.

## Source status

Exact coboundary quotient invariance of edgewise residual mechanized in DerivationDagQMClosure.lean

## Review

- PFP review: [dag/results/L1-QM002-O022A-PHI1-QUOTIENT/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/L1-QM002-O022A-PHI1-QUOTIENT/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Exact rational triangle primal construction, minimum weighted cost and gauge-shift invariance, plus general telescoping and lower-bound assumptions in Lean.
  - does not support: Refine arbitrary finite repair packets to Banach quotients and the unrestricted CODA-A bridge. The literal Lean bound theorem is a scalar interface, not an array refinement.
  - next test: Refine arbitrary finite repair packets to Banach quotients and the unrestricted CODA-A bridge. The literal Lean bound theorem is a scalar interface, not an array refinement.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.l1_gs001_replica_and_phi1_quotient_invariance` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gs001_replica_and_phi1_quotient_invariance` |
| `QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0359_keep_the_phi1_banach_quotient_reading_on_a_finite_dimensional_repair_packet_and_leave.md`

- file: [dag/derivations/07_l1_emergence/tfq_0359_keep_the_phi1_banach_quotient_reading_on_a_finite_dimensional_repair_packet_and_leave.md](../../../dag/derivations/07_l1_emergence/tfq_0359_keep_the_phi1_banach_quotient_reading_on_a_finite_dimensional_repair_packet_and_leave.md)
- sha256 (`lf-normalised`): `31b5b03dc9a8eac2eb20b17eb53d63fa9b85492e3f1087a1b55106fa427fca5d`
- generated view: listed, not counted
- cited in: record TFQ-0359
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:0afca57b5b9d44930fdafc79b2199989c1617b63981a2718bcfd3960a957dfd0`
- `external:sha256:0c0765fc5764c70a5288d29e18459286d32fe55a9848613a7092505ecd0e3526#O022a`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`
- `external:sha256:6d5d5d60c5905f79d67d8a8bc365e337b56a0ffb2270da01f2589b4c1a2620f0`

## Routes

Incoming (1):

- `L1-R-PHI1-QUOTIENT` `GAP_NO_DERIVATION`: [L1-WDP-WINDOW-PHI1-GAMMA2](L1-WDP-WINDOW-PHI1-GAMMA2.md) (DEFINITION), [L1-CHAIN-D1D0-AXIOM](L1-CHAIN-D1D0-AXIOM.md) (ADMITTED_PRIMITIVE)

Outgoing (1):

- `L1-R-DENSITY-LIFT-PUB009` `GAP_NO_DERIVATION`: [L1-DENSITY-LIFT-SIGNED-SQRT-PUB009](L1-DENSITY-LIFT-SIGNED-SQRT-PUB009.md) (OPEN)
