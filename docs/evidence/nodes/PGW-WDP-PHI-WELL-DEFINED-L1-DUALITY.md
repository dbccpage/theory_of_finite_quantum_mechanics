# PGW-WDP-PHI-WELL-DEFINED-L1-DUALITY

Stage: [WDP](../stages/WDP.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> WDP-CH04-P01: Φ_J(\[δ\]) = inf_f J(δ − d₀f) is independent of the representative, because δ' = δ + d₀g turns the infimum into one over h = f − g, a bijection of C⁰. WDP-CH04-P02 (conditional): when the repair space is finite-dimensional over ℝ or ℂ and J is a norm, the infimum is attained after quotienting ker d₀; the hypotheses cannot be dropped silently for seminorms or infinite carriers. WDP-CH04-C01 (conditional): with positive weights w, Φ_{1,w}(\[δ\]) = max{⟨y, δ⟩ : d₀*y = 0, |y_e| ≤ w_e}, an imported finite-dimensional convex-duality result (REF-MATH-005, Rockafellar, Convex Analysis) specialized to the declared weighted graph complex. In code, finite_quotient_l1 minimizes over an explicit candidate list, and exact_quotient_l1 solves the weighted ℓ¹ programme over Fraction and reports a value only after an independent certificate check.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 8
- cited Lean declarations covered by a current replay receipt: 8
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `receipt_names_uncited_module`: a replay receipt names this node for lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean, but the node's lean, rust and source fields do not cite it. A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence).

## Imported structure

- Finite-dimensional convex (linear-programming) strong duality, REF-MATH-005 Rockafellar Convex Analysis, specialized to the declared weighted graph complex (assumption)
- Attainment hypothesis: repair space finite-dimensional over R or C and J a norm, not a seminorm (assumption)

## Bottleneck

Representative independence is unconditional; the weak direction of the duality is not imported (WDP-CH04-P07, TFQ-0348, Lean dual_certificate_lower_bound), and C01 is not shown for arbitrary coefficient spaces.

## Source status

WDP monograph §4.2-§4.3 WDP-CH04-P01, conditional P02 and C01 (imported LP duality)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean`

- file: [lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean](../../../lean4/CampaignPgwWdpPhiWellDefinedL1Duality.lean)
- sha256 (`bytes`): `ad360df138896aa08a749c4f5db0df98b8b46ba7ff7a3554477b3266f3d1d7fb`
- cited in: receipt dag/research/campaign_pgw-wdp-phi-well-defined-l1-duality_lean_replay.json (CampaignPgwWdpPhiWellDefinedL1Duality)
- replay: `verified`
  - receipt [dag/research/campaign_pgw-wdp-phi-well-defined-l1-duality_lean_replay.json](../../../dag/research/campaign_pgw-wdp-phi-well-defined-l1-duality_lean_replay.json) (module `CampaignPgwWdpPhiWellDefinedL1Duality`): recorded sha256 `ad360df138896aa08a749c4f5db0df98b8b46ba7ff7a3554477b3266f3d1d7fb` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignPgwWdpPhiWellDefinedL1Duality`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
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
- sha256 (`lf-normalised`): `819551ed358cf7a8fe9ee7aae58d820381530aedb06b69c20c8232af51c92626`
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

