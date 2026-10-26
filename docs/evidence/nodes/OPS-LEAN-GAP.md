# OPS-LEAN-GAP

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Not formalised in Lean: the equivalences between global sections, conv(A) and the noncontextual fraction, and between strong contextuality and NCF 0 (nodes OPS-NCF-LHV-EQUIVALENCE and OPS-STRONG-CONTEXTUALITY-NCF-ZERO); Vorob'ev sufficiency and its converse (node OPS-VOROBEV-THEOREM); delta0 e = 0 if and only if e is no-signalling; rational normalisation of weights; and any link from the Lean model of natural-number-weighted lists to the Rust Scenario type or to the Rust and Python gates. Separate finite result: For all four Boolean variables, the four specified parity constraints have no common assignment; their left XOR is false and the right XOR is true. The arithmetic identity 2*2*2*2 = 16 holds; the separate independent enumeration counts 16 assignments.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
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

Missing: Lean proofs of the unresolved global-section/NCF, strong-contextuality, Vorobev, no-signalling, rational-normalization and Rust-refinement items listed first in the statement. The separate four-variable parity obstruction and arithmetic product are already proved in CampaignOpsLeanGap. The Lean file lean4/LggrFiniteResults.lean covers only the statements of nodes OPS-PUSHFORWARD-FUNCTOR-LEAN and OPS-PARITY-HOLONOMY-LEAN among these rows. This one parity box does not establish the listed global-section/NCF equivalences, strong-contextuality criterion, Vorobev theorem, no-signalling coboundary equivalence, rational normalization or Rust Scenario refinement. The Lean sixteen lemma is arithmetic, not a type-cardinality theorem. The original OPS obligation remains OPEN.

## Source status

Ledger row L035-L1, status open.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignOpsLeanGap.lean`

- file: [lean4/CampaignOpsLeanGap.lean](../../../lean4/CampaignOpsLeanGap.lean)
- sha256 (`bytes`): `28ba5a6e40e191c1060bd6bf67d33c795a5fdf937e95ed18b894e67649306414`
- cited in: node.source, receipt dag/research/campaign_ops-lean-gap_lean_replay.json (CampaignOpsLeanGap), receipt dag/research/pr439_review_lean_replay.json (CampaignOpsLeanGap), record TFQ-2520
- replay: `verified`
  - receipt [dag/research/campaign_ops-lean-gap_lean_replay.json](../../../dag/research/campaign_ops-lean-gap_lean_replay.json) (module `CampaignOpsLeanGap`): recorded sha256 `28ba5a6e40e191c1060bd6bf67d33c795a5fdf937e95ed18b894e67649306414` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr439_review_lean_replay.json](../../../dag/research/pr439_review_lean_replay.json) (module `CampaignOpsLeanGap`): recorded sha256 `28ba5a6e40e191c1060bd6bf67d33c795a5fdf937e95ed18b894e67649306414` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
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
- sha256 (`bytes`): `360b54c718ad8a21b4f9c99a98c8450ab8c31b8d387ca9728f02b997a3d3453a`
- cited in: node.source, record TFQ-2520
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2520_ops_lean_gap.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2520_ops_lean_gap.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2520_ops_lean_gap.md)
- sha256 (`lf-normalised`): `42b1b4fe0f7a8fd46efe131f4aa8e237262e5d2dc26829550a41d211ed851b1b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2520
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/ops-lean-gap.md`

- file: [dag/derivations/independent/ops-lean-gap.md](../../../dag/derivations/independent/ops-lean-gap.md)
- sha256 (`lf-normalised`): `afd46784373b963349931f59f8b2fa207c77486313851a60b475e6f1bc1fc600`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/pr439_review_lean_replay.json`

- file: [dag/research/pr439_review_lean_replay.json](../../../dag/research/pr439_review_lean_replay.json)
- sha256 (`lf-normalised`): `6e23a872fd26fa8c214157f92ac97d73c6f510d1b181408c3e520dbccdd2a9f5`
- cited in: node.source
- counts toward the grade: yes

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

