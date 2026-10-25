# PGW-WDP-PHI-WELL-DEFINED-L1-DUALITY

Stage: [WDP](../stages/WDP.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On integer triples, the triangle coboundary is d0(f0, f1, f2) = (f1 - f0, f2 - f1, f2 - f0). For all integer vertex triples f and g, d0(f0 + g0, f1 + g1, f2 + g2) equals the componentwise sum of d0(f) and d0(g), and (delta + d0(g)) - d0(f + g) equals delta - d0(f). The sum of absolute residual entries is unchanged by that shift. For delta = (1, 1, 0), every integer repair has absolute residual sum at least 2, and the repair (0, 1, 0) has absolute residual sum 2. For every integer vertex triple g, delta + d0(g) has absolute residual sum at least 2 at every integer repair, and the repair (g0, 1 + g1, g2) has absolute residual sum 2.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 23
- distinct cited Lean declarations covered by a current replay receipt: 16
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Finite-dimensional convex (linear-programming) strong duality, REF-MATH-005 Rockafellar Convex Analysis, specialized to the declared weighted graph complex (assumption)
- Attainment hypothesis: repair space finite-dimensional over R or C and J a norm, not a seminorm (assumption)

## Bottleneck

Standing text is the integer triangle coboundary: linearity, residual identity under a vertex shift, and minimum absolute residual sum 2 for delta = (1, 1, 0) and for each integer coboundary shift of that one triple. Representative independence for a general cost, attainment on a real or complex repair space, weighted duality on an arbitrary complex, rational repairs, and a general coefficient field stay open. The weak direction of the duality is not imported (WDP-CH04-P07, TFQ-0348, Lean dual_certificate_lower_bound), and C01 is not shown for arbitrary coefficient spaces.

## Source status

WDP monograph §4.2-§4.3 WDP-CH04-P01, conditional P02 and C01 (imported LP duality)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean`

- file: [lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean](../../../lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean)
- sha256 (`bytes`): `e0b6759ce98df8fef7b96d569b6f5ca36c73d45b7f938670127412180eb6f094`
- cited in: node.lean, receipt dag/research/campaign_pgw-wdp-phi-well-defined-l1-duality_lean_replay.json (CampaignPgwWdpPhiWellDefinedL1Duality), receipt dag/research/pr_377_round2_replay.json (CampaignPgwWdpPhiWellDefinedL1Duality), record TFQ-0544
- replay: `verified`
  - receipt [dag/research/campaign_pgw-wdp-phi-well-defined-l1-duality_lean_replay.json](../../../dag/research/campaign_pgw-wdp-phi-well-defined-l1-duality_lean_replay.json) (module `CampaignPgwWdpPhiWellDefinedL1Duality`): recorded sha256 `e0b6759ce98df8fef7b96d569b6f5ca36c73d45b7f938670127412180eb6f094` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/pr_377_round2_replay.json](../../../dag/research/pr_377_round2_replay.json) (module `CampaignPgwWdpPhiWellDefinedL1Duality`): recorded sha256 `e0b6759ce98df8fef7b96d569b6f5ca36c73d45b7f938670127412180eb6f094` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignPgwWdpPhiWellDefinedL1Duality`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignPgwWdpPhiWellDefinedL1Duality.absSum` | yes | yes | yes | none | `#print axioms CampaignPgwWdpPhiWellDefinedL1Duality.absSum` |
| `CampaignPgwWdpPhiWellDefinedL1Duality.absSum_attained` | yes | yes | yes | propext | `#print axioms CampaignPgwWdpPhiWellDefinedL1Duality.absSum_attained` |
| `CampaignPgwWdpPhiWellDefinedL1Duality.absSum_ge_two` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignPgwWdpPhiWellDefinedL1Duality.absSum_ge_two` |
| `CampaignPgwWdpPhiWellDefinedL1Duality.absSum_shift` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignPgwWdpPhiWellDefinedL1Duality.absSum_shift` |
| `CampaignPgwWdpPhiWellDefinedL1Duality.add3` | yes | yes | yes | none | `#print axioms CampaignPgwWdpPhiWellDefinedL1Duality.add3` |
| `CampaignPgwWdpPhiWellDefinedL1Duality.d0` | yes | yes | yes | none | `#print axioms CampaignPgwWdpPhiWellDefinedL1Duality.d0` |
| `CampaignPgwWdpPhiWellDefinedL1Duality.d0_linear` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignPgwWdpPhiWellDefinedL1Duality.d0_linear` |
| `CampaignPgwWdpPhiWellDefinedL1Duality.natAbs_pair_le_absSum` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignPgwWdpPhiWellDefinedL1Duality.natAbs_pair_le_absSum` |
| `CampaignPgwWdpPhiWellDefinedL1Duality.pair110` | yes | yes | yes | none | `#print axioms CampaignPgwWdpPhiWellDefinedL1Duality.pair110` |
| `CampaignPgwWdpPhiWellDefinedL1Duality.pair_d0_zero` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignPgwWdpPhiWellDefinedL1Duality.pair_d0_zero` |
| `CampaignPgwWdpPhiWellDefinedL1Duality.pair_residual` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignPgwWdpPhiWellDefinedL1Duality.pair_residual` |
| `CampaignPgwWdpPhiWellDefinedL1Duality.residual_shift` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignPgwWdpPhiWellDefinedL1Duality.residual_shift` |
| `CampaignPgwWdpPhiWellDefinedL1Duality.shifted_attained` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignPgwWdpPhiWellDefinedL1Duality.shifted_attained` |
| `CampaignPgwWdpPhiWellDefinedL1Duality.shifted_ge` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignPgwWdpPhiWellDefinedL1Duality.shifted_ge` |
| `CampaignPgwWdpPhiWellDefinedL1Duality.sub3` | yes | yes | yes | none | `#print axioms CampaignPgwWdpPhiWellDefinedL1Duality.sub3` |
| `absSum_attained` | yes | yes | yes | propext | `#print axioms absSum_attained` |
| `absSum_ge_two` | yes | yes | yes | Quot.sound, propext | `#print axioms absSum_ge_two` |
| `absSum_shift` | yes | yes | yes | Quot.sound, propext | `#print axioms absSum_shift` |
| `d0_linear` | yes | yes | yes | Quot.sound, propext | `#print axioms d0_linear` |
| `residual_shift` | yes | yes | yes | Quot.sound, propext | `#print axioms residual_shift` |
| `shifted_attained` | yes | yes | yes | Quot.sound, propext | `#print axioms shifted_attained` |
| `shifted_ge` | yes | yes | yes | Quot.sound, propext | `#print axioms shifted_ge` |

- counts toward the grade: yes

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean)
- sha256 (`bytes`): `bef8623978d7c0735b4a02db686664b03b61e18bba0e5ef6bcce81ff4234dd0a`
- cited in: node.lean, record TFQ-0544
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_wdp.json](../../../dag/research/lean_replay_campaign_wdp.json) (module `Imported.WitnessedDifference.WitnessedDifference.Obstruction`): recorded sha256 `bef8623978d7c0735b4a02db686664b03b61e18bba0e5ef6bcce81ff4234dd0a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `dual_certificate_lower_bound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms dual_certificate_lower_bound` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_wdp/src/fenchel_duality.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/fenchel_duality.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0544_wdp_phi_well_defined_l1_duality.md`

- file: [dag/derivations/06_wdp/tfq_0544_wdp_phi_well_defined_l1_duality.md](../../../dag/derivations/06_wdp/tfq_0544_wdp_phi_well_defined_l1_duality.md)
- sha256 (`lf-normalised`): `048d5052f4687a6fbb459f6d8a78ff8ceb9ce6872cc29516bdd0e16f5d62618c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0544
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine/crates_rs/omega_wdp/src/fenchel_duality.rs::FenchelDualityReceipt`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/cochains.py::finite_quotient_l1`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/obstruction.py::exact_quotient_l1`

## Routes

Incoming (1):

- `PGW-R-WDP-PHI-WELL-DEFINED-L1-DUALITY` `CONDITIONAL_ON_IMPORT`: [PGW-WDP-GRAPH-COCHAIN-HOST](PGW-WDP-GRAPH-COCHAIN-HOST.md) (DEFINITION), [PGW-WDP-QUOTIENT-DEFECT-ROOT-P](PGW-WDP-QUOTIENT-DEFECT-ROOT-P.md) (DEFINITION), [PGW-SN-E08-WEIGHTED-L1-DUALITY](PGW-SN-E08-WEIGHTED-L1-DUALITY.md) (PROVED_LEAN)

Outgoing (0):

