# FSP-LAUGHLIN-EXCHANGE-PHASE

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Arovas-Schrieffer-Wilczek: adiabatic exchange of two quasiholes in the nu = 1/m Laughlin state gives statistical phase theta = pi/m.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 10
- cited Lean declarations covered by a current replay receipt: 10
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Laughlin nu = 1/m state and quasihole Berry phase (literature)

## Bottleneck

Narrowed algebraic checks only. Jastrow exchange identities hold in commutative rings. A supplied 2x2 integer companion matrix and its square satisfy cyclotomic identities and fail involution tests. The quasihole polynomial is symmetric. The matrix model is not identified with a physical Berry holonomy, and symmetry alone does not derive a Berry phase or its physical origin. Status is unchanged. The original physical or operational bridge remains open.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-044 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspLaughlinExchangePhase.lean`

- file: [lean4/CampaignFspLaughlinExchangePhase.lean](../../../lean4/CampaignFspLaughlinExchangePhase.lean)
- sha256 (`bytes`): `ce6c4862a88bb315a12e5e3865898dafb56986b59cb303839b9ec35dc55f467f`
- cited in: node.lean, record TFQ-1208
- replay: `verified`
  - receipt [dag/research/campaign_fsp-laughlin-exchange-phase_lean_replay.json](../../../dag/research/campaign_fsp-laughlin-exchange-phase_lean_replay.json) (module `CampaignFspLaughlinExchangePhase`): recorded sha256 `ce6c4862a88bb315a12e5e3865898dafb56986b59cb303839b9ec35dc55f467f` matches the current file; exit code 0; Lean None; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspLaughlinExchangePhase`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspLaughlinExchangePhase.abelian_anyon_modular_s_exponent_and_z3_character_sum` | yes | yes | yes | module-level | `#print axioms CampaignFspLaughlinExchangePhase.abelian_anyon_modular_s_exponent_and_z3_character_sum` |
| `CampaignFspLaughlinExchangePhase.general_m_monodromy_residue_and_odd_coprime` | yes | yes | yes | module-level | `#print axioms CampaignFspLaughlinExchangePhase.general_m_monodromy_residue_and_odd_coprime` |
| `CampaignFspLaughlinExchangePhase.laughlin_m3_exchange_companion_cyclotomic_relations` | yes | yes | yes | module-level | `#print axioms CampaignFspLaughlinExchangePhase.laughlin_m3_exchange_companion_cyclotomic_relations` |
| `CampaignFspLaughlinExchangePhase.laughlin_m3_monodromy_cyclotomic_and_non_involution` | yes | yes | yes | module-level | `#print axioms CampaignFspLaughlinExchangePhase.laughlin_m3_monodromy_cyclotomic_and_non_involution` |
| `CampaignFspLaughlinExchangePhase.laughlin_odd_m_fermionic_and_even_m_bosonic` | yes | yes | yes | module-level | `#print axioms CampaignFspLaughlinExchangePhase.laughlin_odd_m_fermionic_and_even_m_bosonic` |
| `CampaignFspLaughlinExchangePhase.laughlin_quasihole_holomorphic_polynomial_symmetric_fence` | yes | yes | yes | module-level | `#print axioms CampaignFspLaughlinExchangePhase.laughlin_quasihole_holomorphic_polynomial_symmetric_fence` |
| `CampaignFspLaughlinExchangePhase.laughlin_three_body_vandermonde_transposition_flips_sign_for_odd_m` | yes | yes | yes | module-level | `#print axioms CampaignFspLaughlinExchangePhase.laughlin_three_body_vandermonde_transposition_flips_sign_for_odd_m` |
| `CampaignFspLaughlinExchangePhase.laughlin_two_body_jastrow_exchange_parity` | yes | yes | yes | module-level | `#print axioms CampaignFspLaughlinExchangePhase.laughlin_two_body_jastrow_exchange_parity` |
| `CampaignFspLaughlinExchangePhase.no_z2_involution_matches_m3_monodromy_fence` | yes | yes | yes | module-level | `#print axioms CampaignFspLaughlinExchangePhase.no_z2_involution_matches_m3_monodromy_fence` |
| `CampaignFspLaughlinExchangePhase.unequal_quasihole_quasielectron_weights_prevent_z3_cancellation_fence` | yes | yes | yes | module-level | `#print axioms CampaignFspLaughlinExchangePhase.unequal_quasihole_quasielectron_weights_prevent_z3_cancellation_fence` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1208_fsp_laughlin_exchange_phase.md`

- file: [dag/derivations/26_fsp/tfq_1208_fsp_laughlin_exchange_phase.md](../../../dag/derivations/26_fsp/tfq_1208_fsp_laughlin_exchange_phase.md)
- sha256 (`lf-normalised`): `6afc89dd294fb1a3b6abeb899c494cc6985ba4e721d560a8c32c9b6312704317`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1208
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-laughlin-exchange-phase.md`

- file: [dag/derivations/independent/fsp-laughlin-exchange-phase.md](../../../dag/derivations/independent/fsp-laughlin-exchange-phase.md)
- sha256 (`lf-normalised`): `bfdf79d1fa7b27ba4bbd143ec5078469b9c54a0c5c097165f4b84342b0855780`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-laughlin-exchange-phase_independent.json`

- file: [dag/research/campaign_fsp-laughlin-exchange-phase_independent.json](../../../dag/research/campaign_fsp-laughlin-exchange-phase_independent.json)
- sha256 (`lf-normalised`): `89cb50b7afc65e71e1126afadeae8842dc57796d17318954bb2c662b3578be14`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-laughlin-exchange-phase_lean_mutation.json`

- file: [dag/research/campaign_fsp-laughlin-exchange-phase_lean_mutation.json](../../../dag/research/campaign_fsp-laughlin-exchange-phase_lean_mutation.json)
- sha256 (`lf-normalised`): `aa045a47dfbaa5964edbbfd3159f53b871cb2b11e1da1567402fdaf311495b16`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-laughlin-exchange-phase_lean_replay.json`

- file: [dag/research/campaign_fsp-laughlin-exchange-phase_lean_replay.json](../../../dag/research/campaign_fsp-laughlin-exchange-phase_lean_replay.json)
- sha256 (`lf-normalised`): `d7952b06f1b4fb2c67ffdc869ab06debbfaa4de2468198f3129cff71a42f9188`
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
