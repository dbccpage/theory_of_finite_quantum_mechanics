# FSP-WITTEN-INDEX-INVARIANCE

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On a finite-dimensional graded Hilbert space with an exact supercharge Q and H = {Q, Q^dagger}, positive-energy levels pair bosons with fermions, so W = Tr\[(-1)^F exp(-beta H)\] = n_B(E=0) - n_F(E=0) for every beta, and unbroken supersymmetry has ground energy 0.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 6
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- exact supercharge with H = {Q, Q^dagger} on a finite graded space (assumption)

## Bottleneck

Pairing is supplied by the shared spectral list; this does not derive that pairing from an arbitrary supercharge, spectral decomposition on a Hilbert space, the analytic exponential trace, or the ground-energy theorem. The full imported Witten-index statement remains open here. Original target retained as an obligation: On a finite-dimensional graded Hilbert space with an exact supercharge Q and H = {Q, Q^dagger}, positive-energy levels pair bosons with fermions, so W = Tr\[(-1)^F exp(-beta H)\] = n_B(E=0) - n_F(E=0) for every beta, and unbroken supersymmetry has ground energy 0. Prior boundary: Standard result imported; it presupposes an exact lattice supercharge, which FSP-DERIV-040 leaves open, and gives no sign-free sampling of Z itself.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-042 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignWittenPairing.lean`

- file: [lean4/CampaignWittenPairing.lean](../../../lean4/CampaignWittenPairing.lean)
- sha256 (`bytes`): `daf7755630c62ceac5984345d2d6cece20a53ffe21fa3d217eebf6e0179fdab1`
- cited in: node.lean, receipt dag/research/campaign_fsp-witten-index-invariance_lean_replay.json (CampaignWittenPairing), receipt dag/research/pr_376_round2_replay.json (CampaignWittenPairing), record TFQ-1206
- replay: `verified`
  - receipt [dag/research/campaign_fsp-witten-index-invariance_lean_replay.json](../../../dag/research/campaign_fsp-witten-index-invariance_lean_replay.json) (module `CampaignWittenPairing`): recorded sha256 `daf7755630c62ceac5984345d2d6cece20a53ffe21fa3d217eebf6e0179fdab1` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/pr_376_round2_replay.json](../../../dag/research/pr_376_round2_replay.json) (module `CampaignWittenPairing`): recorded sha256 `daf7755630c62ceac5984345d2d6cece20a53ffe21fa3d217eebf6e0179fdab1` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignWittenPairing`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignWittenPairing.paired_trace` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignWittenPairing.paired_trace` |
| `CampaignWittenPairing.traceWeight` | yes | yes | yes | none | `#print axioms CampaignWittenPairing.traceWeight` |
| `CampaignWittenPairing.trace_append` | yes | yes | yes | propext | `#print axioms CampaignWittenPairing.trace_append` |
| `CampaignWittenPairing.trace_zero_modes` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignWittenPairing.trace_zero_modes` |
| `CampaignWittenPairing.weight_independent` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignWittenPairing.weight_independent` |
| `CampaignWittenPairing.zero_index_with_ground_modes` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignWittenPairing.zero_index_with_ground_modes` |

- counts toward the grade: yes

### Lean: `papers/core/fsp/lean4/regge_wdw_core.lean`

- file: [papers/core/fsp/lean4/regge_wdw_core.lean](../../../papers/core/fsp/lean4/regge_wdw_core.lean)
- sha256 (`bytes`): `8f20ead1eb7c40441e6ccee48c7b5c828d0d93319928ea2df7ec322226e164b9`
- cited in: node.source
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains papers/core/fsp/lean4/regge_wdw_core.lean`
- counts toward the grade: yes

### Python: `checks/independent/fsp-witten-index-invariance.py`

- file: [checks/independent/fsp-witten-index-invariance.py](../../../checks/independent/fsp-witten-index-invariance.py)
- sha256 (`bytes`): `e61e0ba0575adfe8eeb6ee651d947c1dc1cfe0428a841d33351bd6beb78a0d20`
- cited in: record TFQ-1206
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1206_fsp_witten_index_invariance.md`

- file: [dag/derivations/26_fsp/tfq_1206_fsp_witten_index_invariance.md](../../../dag/derivations/26_fsp/tfq_1206_fsp_witten_index_invariance.md)
- sha256 (`lf-normalised`): `68cd6183c980a084269aea85084073decd3b7f6c3b09a402b7162c43b2542a84`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1206
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-witten-index-invariance.md`

- file: [dag/derivations/independent/fsp-witten-index-invariance.md](../../../dag/derivations/independent/fsp-witten-index-invariance.md)
- sha256 (`lf-normalised`): `2024509e60844c5b63874ccc544256ea8a69196c73210409c3295673c09d50db`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-witten-index-invariance_lean_replay.json`

- file: [dag/research/campaign_fsp-witten-index-invariance_lean_replay.json](../../../dag/research/campaign_fsp-witten-index-invariance_lean_replay.json)
- sha256 (`lf-normalised`): `c18f5022854d4da4dea1081c2563bc97fbce4e28b7fb77c4b57e06348a77c4ca`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `5a72c2f6006ea18c3362f0a63e8525b65d41898e8f1bd437b7e4c2e368c7e102`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-WITTEN-INDEX-INVARIANCE` `CONDITIONAL_ON_IMPORT`: [FSP-LATTICE-WESS-ZUMINO-SUSY](FSP-LATTICE-WESS-ZUMINO-SUSY.md) (OPEN)

Outgoing (2):

- `APP-R-FSP-KITAEV-HONEYCOMB-SOLUTION` `CONDITIONAL_ON_IMPORT`: [FSP-KITAEV-HONEYCOMB-SOLUTION](FSP-KITAEV-HONEYCOMB-SOLUTION.md) (IMPORTED_ASSUMPTION)
- `APP-R-FSP-MASTER-DICHOTOMY-REFUTED` `DERIVED_PROSE`: [FSP-MASTER-DICHOTOMY-REFUTED](FSP-MASTER-DICHOTOMY-REFUTED.md) (REFUTED)
