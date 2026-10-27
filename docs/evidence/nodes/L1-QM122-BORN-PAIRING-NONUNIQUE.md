# L1-QM122-BORN-PAIRING-NONUNIQUE

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A pairing exists (pairing_exists), a quartic rival to the quadratic pairing exists (quartic_rival), and uniqueness is not discharged (uniqueness_not_discharged, born_nonuniqueness_open). Under frame additivity the fourth power is excluded. Ordinary Gleason dimension is not matched by the two-label host (HilbertWalkGleason).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- Gleason: assumption

## Bottleneck

Lean exhibits the pairing on one state and an explicit quartic rival on one state (pairing_exists, quartic_rival), which settles the existence claims. Exclusion of the fourth power under frame additivity is not in the cited Lean. uniqueness_not_discharged and born_nonuniqueness_open evaluate a declared Boolean flag and carry no mathematical content.

## Source status

BornPairingBoundary: Candidate only. Not PROVEN. Kind: IMPORT BOUNDARY (file header)

## Review

- PFP review: [dag/results/L1-QM122-BORN-PAIRING-NONUNIQUE/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-QM122-BORN-PAIRING-NONUNIQUE/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Exact quadratic/quartic/swapped atom values, honest normalization contracts and Gaussian Hadamard/rotated frame countercontrols; literal unit and frame identities in Lean.
  - does not support: Formalize full source pairing refinement and the additional frame/POVM/Gleason uniqueness hypotheses. These rivals share only their stated weak contracts.
  - next test: Formalize full source pairing refinement and the additional frame/POVM/Gleason uniqueness hypotheses. These rivals share only their stated weak contracts.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BornPairingBoundary.lean`

- file: [lean4/BornPairingBoundary.lean](../../../lean4/BornPairingBoundary.lean)
- sha256 (`bytes`): `1a25c045a339b3b72e372dec8ea59683a40558820e302ab6f44bd0d8b518ee29`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `BornPairingBoundary`): recorded sha256 `1a25c045a339b3b72e372dec8ea59683a40558820e302ab6f44bd0d8b518ee29` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornPairingBoundary`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `born_nonuniqueness_open` | yes | yes | yes | none | `#print axioms born_nonuniqueness_open` |
| `pairing_exists` | yes | yes | yes | propext | `#print axioms pairing_exists` |
| `quartic_rival` | yes | yes | yes | propext | `#print axioms quartic_rival` |
| `uniqueness_not_discharged` | yes | yes | yes | none | `#print axioms uniqueness_not_discharged` |

- counts toward the grade: yes

### Lean: `lean4/FiniteQM.lean`

- file: [lean4/FiniteQM.lean](../../../lean4/FiniteQM.lean)
- sha256 (`bytes`): `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759`
- cited in: record TFQ-0306
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qcd.json](../../../dag/research/lean_replay_campaign_finite_qcd.json) (module `FiniteQM`): recorded sha256 `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteQM`
- counts toward the grade: yes

### Lean: `lean4/HilbertWalkGleason.lean`

- file: [lean4/HilbertWalkGleason.lean](../../../lean4/HilbertWalkGleason.lean)
- sha256 (`bytes`): `42c9d771c0f1c717bcf7673918fe0ee69046418ca70c1f6fd8ee9972977f9d30`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `HilbertWalkGleason`): recorded sha256 `42c9d771c0f1c717bcf7673918fe0ee69046418ca70c1f6fd8ee9972977f9d30` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build HilbertWalkGleason`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `two_label_host_not_gleason_dimension` | yes | yes | yes | none | `#print axioms two_label_host_not_gleason_dimension` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_0306_born_uniqueness_stays_an_imported_boundary.md`

- file: [dag/derivations/08_l1_to_l2/tfq_0306_born_uniqueness_stays_an_imported_boundary.md](../../../dag/derivations/08_l1_to_l2/tfq_0306_born_uniqueness_stays_an_imported_boundary.md)
- sha256 (`lf-normalised`): `cb5372ff39859e84f4b44fabf257bcf7f7aa28e390c21347623a4b0e3116e220`
- generated view: listed, not counted
- cited in: record TFQ-0306
- counts toward the grade: no

### Documents and data: `dag/derivations/09_finite_hilbert/tfq_0312_four_necessity_verdicts_stay_open_beside_the_matrix_gap.md`

- file: [dag/derivations/09_finite_hilbert/tfq_0312_four_necessity_verdicts_stay_open_beside_the_matrix_gap.md](../../../dag/derivations/09_finite_hilbert/tfq_0312_four_necessity_verdicts_stay_open_beside_the_matrix_gap.md)
- sha256 (`lf-normalised`): `7a88ebef332ac78cab8de69c4643d54ce5f272c58f21c8d24bd3396a68a9e0e9`
- generated view: listed, not counted
- cited in: record TFQ-0312 (shared)
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- `external:sha256:86710ba8ef7db719a42a2165e71d3bc72ac5db63d0b2a51e57f48f14e137754e`
- `external:sha256:c8f020f9abf33d6d86e8630fd8f9d3da0bb1db91835d6dfcbe56cfa4709cad7e`

## Absences recorded by the TFQ records

- TFQ-0306 rust: no local rust twin located for external:sha256:d58eb2c1f4ae2ac65cc7145554cd2a5c955e096776c1f6d9daafb2065b14450e
- TFQ-0312 python: no local python twin located for sources/atlas/papers/quantum_foundations/_code/qm_122/qm122_lib/qm122_dual.py

## Routes

Incoming (1):

- `L1-R-BORN-PAIRING-BOUNDARY` `COMPUTED`: [L1-QM020-THM6-P1-SCOPE-FENCE](L1-QM020-THM6-P1-SCOPE-FENCE.md) (COMPUTATIONALLY_CHECKED), [L1-IMP-ORTHOGONAL-ADDITIVITY](L1-IMP-ORTHOGONAL-ADDITIVITY.md) (CONDITIONAL)

Outgoing (1):

- `L1-R-MNC-LEFTOVER` `GAP_NO_DERIVATION`: [L1-QM122-LEFTOVER-MNC-NOT-RECOVERED](L1-QM122-LEFTOVER-MNC-NOT-RECOVERED.md) (OPEN)
