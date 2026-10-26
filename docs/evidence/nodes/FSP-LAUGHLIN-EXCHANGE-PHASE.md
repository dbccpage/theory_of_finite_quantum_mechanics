# FSP-LAUGHLIN-EXCHANGE-PHASE

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Arovas-Schrieffer-Wilczek: adiabatic exchange of two quasiholes in the nu = 1/m Laughlin state gives statistical phase theta = pi/m.

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

- Laughlin nu = 1/m state and quasihole Berry phase (literature)

## Bottleneck

The statistical exchange phase of Laughlin quasiholes requires the wavefunction, adiabatic transport and Berry connection, plus a branch/continuity convention. The algebraic non-uniqueness does not refute the Arovas-Schrieffer-Wilczek result. Original target retained as an obligation: Arovas-Schrieffer-Wilczek: adiabatic exchange of two quasiholes in the nu = 1/m Laughlin state gives statistical phase theta = pi/m. Prior boundary: No Berry-phase or torus computation is in this checkout; the local module fixes m = 3 and checks numeric constants only (ledger GIN-C16 withdraws its reading).

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-044 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignLaughlinRootAmbiguity.lean`

- file: [lean4/CampaignLaughlinRootAmbiguity.lean](../../../lean4/CampaignLaughlinRootAmbiguity.lean)
- sha256 (`bytes`): `c9e55336640123ef8a0d3d2abe8cfc5c0cac5f6fab6400bfee83c5a6025ae314`
- cited in: node.lean, receipt dag/research/campaign_fsp-laughlin-exchange-phase_lean_replay.json (CampaignLaughlinRootAmbiguity), receipt dag/research/pr_379_round2_replay.json (CampaignLaughlinRootAmbiguity), record TFQ-1208
- replay: `verified`
  - receipt [dag/research/campaign_fsp-laughlin-exchange-phase_lean_replay.json](../../../dag/research/campaign_fsp-laughlin-exchange-phase_lean_replay.json) (module `CampaignLaughlinRootAmbiguity`): recorded sha256 `c9e55336640123ef8a0d3d2abe8cfc5c0cac5f6fab6400bfee83c5a6025ae314` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/pr_379_round2_replay.json](../../../dag/research/pr_379_round2_replay.json) (module `CampaignLaughlinRootAmbiguity`): recorded sha256 `c9e55336640123ef8a0d3d2abe8cfc5c0cac5f6fab6400bfee83c5a6025ae314` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignLaughlinRootAmbiguity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignLaughlinRootAmbiguity.monodromy` | yes | yes | yes | none | `#print axioms CampaignLaughlinRootAmbiguity.monodromy` |
| `CampaignLaughlinRootAmbiguity.monodromy_not_injective` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignLaughlinRootAmbiguity.monodromy_not_injective` |
| `CampaignLaughlinRootAmbiguity.roots_at_third_filling` | yes | yes | yes | none | `#print axioms CampaignLaughlinRootAmbiguity.roots_at_third_filling` |
| `CampaignLaughlinRootAmbiguity.two_distinct_exchange_roots` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignLaughlinRootAmbiguity.two_distinct_exchange_roots` |

- counts toward the grade: yes

### Python: `checks/independent/fsp-laughlin-exchange-phase.py`

- file: [checks/independent/fsp-laughlin-exchange-phase.py](../../../checks/independent/fsp-laughlin-exchange-phase.py)
- sha256 (`bytes`): `d6e5d0954e3d144a5cbc51987c5622b3465c98be7fd81b215a5ffa0eab9c73ba`
- cited in: record TFQ-1208
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1208_fsp_laughlin_exchange_phase.md`

- file: [dag/derivations/26_fsp/tfq_1208_fsp_laughlin_exchange_phase.md](../../../dag/derivations/26_fsp/tfq_1208_fsp_laughlin_exchange_phase.md)
- sha256 (`lf-normalised`): `e6a151bb3050790f1b44b5a880bba69e9d35402ab2475be18f00d4d1c0df2653`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1208
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-laughlin-exchange-phase.md`

- file: [dag/derivations/independent/fsp-laughlin-exchange-phase.md](../../../dag/derivations/independent/fsp-laughlin-exchange-phase.md)
- sha256 (`lf-normalised`): `a73514b196b8d7cfa78615844aaf7f4567abfac96050dc13045994c9dfe199e4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-laughlin-exchange-phase_lean_replay.json`

- file: [dag/research/campaign_fsp-laughlin-exchange-phase_lean_replay.json](../../../dag/research/campaign_fsp-laughlin-exchange-phase_lean_replay.json)
- sha256 (`lf-normalised`): `2f01ae58807dee6deabfc323533448ae97c649de25ce65fc9b8e8dbd70d947ee`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign.md)
- sha256 (`lf-normalised`): `f894f295fb17dc831f4e961602bea56223bf79ae6b34c3350cfa6fe358789808`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-LAUGHLIN-EXCHANGE-PHASE` `CONDITIONAL_ON_IMPORT`: [FSP-KITAEV-HONEYCOMB-SOLUTION](FSP-KITAEV-HONEYCOMB-SOLUTION.md) (IMPORTED_ASSUMPTION)

Outgoing (2):

- `APP-R-FSP-BF-2GROUP-SIGN-CLAIM` `GAP_NO_DERIVATION`: [FSP-BF-2GROUP-SIGN-CLAIM](FSP-BF-2GROUP-SIGN-CLAIM.md) (OPEN)
- `APP-R-FSP-FIBONACCI-ANYON-DATA` `CONDITIONAL_ON_IMPORT`: [FSP-FIBONACCI-ANYON-DATA](FSP-FIBONACCI-ANYON-DATA.md) (IMPORTED_ASSUMPTION)
