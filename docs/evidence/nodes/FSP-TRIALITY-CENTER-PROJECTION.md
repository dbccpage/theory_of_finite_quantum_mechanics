# FSP-TRIALITY-CENTER-PROJECTION

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claimed: averaging over Z3 center phases cancels the signs of fractional-triality quark paths and leaves color-singlet zero-triality contributions; no model, projection identity or computation for this exists in this checkout.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 10
- cited Lean, Rust or Python symbols found in their in-repo files: 13
- cited Lean declarations covered by a current replay receipt: 10
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

State the canonical-ensemble center projection as an identity on a declared lattice model and show which signs it removes; ledger GIN-C10 and GIN-C11 withdraw the fixture reading. Narrowed in lean4/CampaignFspTrialityCenterProjection.lean and checks/independent/fsp-triality-center-projection.py while keeping status OPEN to: (1) Eisenstein-cyclotomic ring Z\[omega\] (omega^2 + omega + 1 = 0, omega^3 = 1) canonical-ensemble Z3 center projector Pi_Z3(q) = sum_{k=0}^2 omega^{q k}, proving Pi_Z3(q) = 3 for q = 0 (mod 3) and Pi_Z3(q) = 0 for q = 1, 2 (mod 3), with idempotence Pi_Z3(q)^2 = 3 Pi_Z3(q); (2) grand-canonical Fourier isolation sum_{k=0}^2 (Z_0 + omega^k Z_1 + omega^{2k} Z_2) = 3 Z_0 showing that Z3 center averaging removes fractional-triality amplitudes Z_1, Z_2 while preserving intra-sector zero-triality baryon sign differences 3(w_{B,+} - w_{B,-}) \< 0 when w_{B,-} \> w_{B,+} \> 0; (3) 4-vertex simplicial Y-junction coboundary nilpotence d1(d0(v)) = (0,0,0), closed uniform meson spoke cochains vs non-zero 2-cochain coboundary (1, 4, -5) (L1 norm 10 \> 0) for color-singlet 3-spoke baryon fluxes (2, 1, -3), and Polyakov-loop sector action sum S_F(0)+S_F(1)+S_F(2)=0 with gap 18 h P \> 0; and (4) explicit GIN-C10 and GIN-C11 scope fences for confined 1-vs-2 sector multiplicity imbalance w - 2w = -w \< 0 and non-injectivity with respect to dense lattice QCD sign-problem solvers.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-038 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspTrialityCenterProjection.lean`

- file: [lean4/CampaignFspTrialityCenterProjection.lean](../../../lean4/CampaignFspTrialityCenterProjection.lean)
- sha256 (`bytes`): `f5fe2d825c3ae09dd62e6377b6b92d060a97ae02223cd11c034f9605b67d1dec`
- cited in: node.lean, receipt dag/research/campaign_fsp-triality-center-projection_lean_replay.json (CampaignFspTrialityCenterProjection), record TFQ-1202
- replay: `verified`
  - receipt [dag/research/campaign_fsp-triality-center-projection_lean_replay.json](../../../dag/research/campaign_fsp-triality-center-projection_lean_replay.json) (module `CampaignFspTrialityCenterProjection`): recorded sha256 `f5fe2d825c3ae09dd62e6377b6b92d060a97ae02223cd11c034f9605b67d1dec` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspTrialityCenterProjection`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspTrialityCenterProjection.canonical_z3_center_projection_identity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspTrialityCenterProjection.canonical_z3_center_projection_identity` |
| `CampaignFspTrialityCenterProjection.canonical_z3_sector_fourier_isolation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspTrialityCenterProjection.canonical_z3_sector_fourier_isolation` |
| `CampaignFspTrialityCenterProjection.gin_c10_c11_historical_fixture_scope_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspTrialityCenterProjection.gin_c10_c11_historical_fixture_scope_fence` |
| `CampaignFspTrialityCenterProjection.gin_c11_confined_sector_multiplicity_imbalance` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspTrialityCenterProjection.gin_c11_confined_sector_multiplicity_imbalance` |
| `CampaignFspTrialityCenterProjection.polyakov_center_sector_action_sum_and_gap` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspTrialityCenterProjection.polyakov_center_sector_action_sum_and_gap` |
| `CampaignFspTrialityCenterProjection.su3_cartan_singlet_y_junction_curvature` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspTrialityCenterProjection.su3_cartan_singlet_y_junction_curvature` |
| `CampaignFspTrialityCenterProjection.y_junction_simplicial_nilpotence_d1_d0` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspTrialityCenterProjection.y_junction_simplicial_nilpotence_d1_d0` |
| `CampaignFspTrialityCenterProjection.z3_center_projector_idempotence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspTrialityCenterProjection.z3_center_projector_idempotence` |
| `CampaignFspTrialityCenterProjection.z3_roots_of_unity_group_law` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspTrialityCenterProjection.z3_roots_of_unity_group_law` |
| `CampaignFspTrialityCenterProjection.zero_triality_baryon_sector_sign_persistence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspTrialityCenterProjection.zero_triality_baryon_sector_sign_persistence` |
- counts toward the grade: yes

### Python: `checks/independent/fsp-triality-center-projection.py`

- file: [checks/independent/fsp-triality-center-projection.py](../../../checks/independent/fsp-triality-center-projection.py)
- sha256 (`bytes`): `0a76315ba99179324fdcf9e69e9e8a181915200dc5829918143e687e28c4a77a`
- cited in: record TFQ-1202

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `code/python/src/fsp/su3_baryon_triality.py`

- file: [code/python/src/fsp/su3_baryon_triality.py](../../../code/python/src/fsp/su3_baryon_triality.py)
- sha256 (`bytes`): `418089ee35f2e4088c8a2f2073c8ef572d9ca2bd3468d8bbf1c4a70ccf47f769`
- cited in: record TFQ-1202

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `SU3BaryonGinEngine` (python_symbol) | yes | yes | yes | - | - |
| `SU3SimplicialYJunction` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1202_fsp_triality_center_projection.md`

- file: [dag/derivations/26_fsp/tfq_1202_fsp_triality_center_projection.md](../../../dag/derivations/26_fsp/tfq_1202_fsp_triality_center_projection.md)
- sha256 (`lf-normalised`): `f1bd9f144dfc8365bbf1c620390782659c0148ba9780a10c073d36d2eeacd9f6`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1202
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-triality-center-projection.md`

- file: [dag/derivations/independent/fsp-triality-center-projection.md](../../../dag/derivations/independent/fsp-triality-center-projection.md)
- sha256 (`lf-normalised`): `a9ca45e448a58650517768dc8e1bb204f4b2d5522e0d6b28db4e8555e1da0686`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-triality-center-projection_independent.json`

- file: [dag/research/campaign_fsp-triality-center-projection_independent.json](../../../dag/research/campaign_fsp-triality-center-projection_independent.json)
- sha256 (`lf-normalised`): `da681c4e7ad8d3312be91fafbb000b36fe2b96d98672eebbba75415aa0146b0e`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-triality-center-projection_lean_mutation.json`

- file: [dag/research/campaign_fsp-triality-center-projection_lean_mutation.json](../../../dag/research/campaign_fsp-triality-center-projection_lean_mutation.json)
- sha256 (`lf-normalised`): `75892f268445ffd8daef00a8935cea0e55697144a63bcbe823bb1649e8674003`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-triality-center-projection_lean_replay.json`

- file: [dag/research/campaign_fsp-triality-center-projection_lean_replay.json](../../../dag/research/campaign_fsp-triality-center-projection_lean_replay.json)
- sha256 (`lf-normalised`): `cb3a3c535c8ed95eeb1c9a9d625a923ca9f94223b037d99e4bb3e0e272c13f38`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign.md)
- sha256 (`lf-normalised`): `f894f295fb17dc831f4e961602bea56223bf79ae6b34c3350cfa6fe358789808`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md)
- sha256 (`lf-normalised`): `0a97b32d187a99450605943866d6d4285f0bfd73dcc021c2b69911243066f2f3`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-TRIALITY-CENTER-PROJECTION` `GAP_NO_DERIVATION`: [FSP-QCD-CHEMICAL-POTENTIAL-DET](FSP-QCD-CHEMICAL-POTENTIAL-DET.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

