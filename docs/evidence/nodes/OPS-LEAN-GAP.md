# OPS-LEAN-GAP

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On four Boolean variables a, a', b and b', no assignment satisfies a xor b = false, a xor b' = false, a' xor b = false and a' xor b' = true together. The exclusive-or of those four left-hand sides is false for every assignment, and the exclusive-or of false, false, false and true is true. There are 16 assignments.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

This record is the four-constraint table above. Equivalences among global sections, conv(A) and the noncontextual fraction, strong contextuality and NCF 0, Vorob'ev sufficiency and its converse, the criterion delta0 e = 0 for no-signalling, rational normalisation of weights, and any link from natural-number-weighted lists to the Rust Scenario type stay outside. lean4/LggrFiniteResults.lean still covers only OPS-PUSHFORWARD-FUNCTOR-LEAN and OPS-PARITY-HOLONOMY-LEAN among the older rows. AuthorityEffect: None.

## Source status

Ledger row L035-L1, status open.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignOpsLeanGap.lean`

- file: [lean4/CampaignOpsLeanGap.lean](../../../lean4/CampaignOpsLeanGap.lean)
- sha256 (`bytes`): `28ba5a6e40e191c1060bd6bf67d33c795a5fdf937e95ed18b894e67649306414`
- cited in: node.source, receipt dag/research/campaign_ops-lean-gap_lean_replay.json (CampaignOpsLeanGap), record TFQ-2520
- replay: `verified`
  - receipt [dag/research/campaign_ops-lean-gap_lean_replay.json](../../../dag/research/campaign_ops-lean-gap_lean_replay.json) (module `CampaignOpsLeanGap`): recorded sha256 `28ba5a6e40e191c1060bd6bf67d33c795a5fdf937e95ed18b894e67649306414` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignOpsLeanGap`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignOpsLeanGap.lhsSum` | yes | yes | yes | none | `#print axioms CampaignOpsLeanGap.lhsSum` |
| `CampaignOpsLeanGap.noAssignment` | yes | yes | yes | none | `#print axioms CampaignOpsLeanGap.noAssignment` |
| `CampaignOpsLeanGap.rhsSum` | yes | yes | yes | none | `#print axioms CampaignOpsLeanGap.rhsSum` |
| `CampaignOpsLeanGap.sixteen` | yes | yes | yes | none | `#print axioms CampaignOpsLeanGap.sixteen` |

- counts toward the grade: yes

### Python: `checks/independent/ops-lean-gap.py`

- file: [checks/independent/ops-lean-gap.py](../../../checks/independent/ops-lean-gap.py)
- sha256 (`bytes`): `d423f9b903eeb3b8c2ae92421533569849e09541b0cd8e454eb438b62d171803`
- cited in: node.source, record TFQ-2520
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2520_ops_lean_gap.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2520_ops_lean_gap.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2520_ops_lean_gap.md)
- sha256 (`lf-normalised`): `c14a06ad958c9ef5e407fbb0052e1681487b8e008ab29ab1042f86f5da1ea5ea`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2520
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md`

- file: [sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md](../../../sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md)
- sha256 (`lf-normalised`): `da99779add73314574622d0db46ea4dfbc9b66c4938caf29ab98590033592ab4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md`

- file: [sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md](../../../sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md)
- sha256 (`lf-normalised`): `649532625cf9e8ec085a420fd1bad9227fcc4dae9f06ba02be1eb19f497e3ec7`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (2):

- `OPS-R-LEAN-GAP` `GAP_NO_DERIVATION`: [IMPL-LGGR-FINITE-RESULTS-LEAN](IMPL-LGGR-FINITE-RESULTS-LEAN.md) (PROVED_LEAN)
- `OPS-R-LEAN-GAP-2` `GAP_NO_DERIVATION`: [OPS-NCF-LHV-EQUIVALENCE](OPS-NCF-LHV-EQUIVALENCE.md) (PROVED_PROSE)

Outgoing (0):

