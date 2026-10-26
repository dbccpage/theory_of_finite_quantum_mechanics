# FQ-SORKIN-READOUT-CLASS-QM208

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Inside the phase-blind family alpha|c|^2 + beta|c|^4, third-order Sorkin I3 vanishes identically iff beta = 0; over Z\[zeta_12\] the I3 = 0 rational readout cone R_{A,B} is classified and Galois-invariance selects equal embedding weights alpha = beta. Does not hold outside the polynomial family.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- add-then-square amplitude composition rule (assumption)
- restriction to polynomial readout family (assumption)

## Bottleneck

Lean checks rational identities for the declared Z\[zeta_12\] readout family R_{A,B} (vanishing iff B = 0 on the two test vectors) and fixed positive minors. The full classification of the I3 = 0 cone and the Galois selection alpha = beta are not in Lean.

## Source status

QM-208 table row: exact finite invariant; residual "add-then-square composition and restriction to the polynomial readout family"

## Review

- PFP review: [dag/results/FQ-SORKIN-READOUT-CLASS-QM208/reviews/20261019_structure_audit/review_result.json](../../../dag/results/FQ-SORKIN-READOUT-CLASS-QM208/reviews/20261019_structure_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: general I3(alpha*t²+beta*t⁴)=12*beta*abc(a+b+c), hence general vanishing iff beta=0. Exact Q(zeta12) control norms (7,±4) give R_AB invariance iff B=0; no full positivity-cone classification is inferred.
  - does not support: Formalize the embedding-weight/basis-coordinate conversion and full rational readout positivity cone. Polynomial restriction and amplitude addition are admitted, and this is not a classification of all readouts.
  - next test: Formalize the embedding-weight/basis-coordinate conversion and full rational readout positivity cone. Polynomial restriction and amplitude addition are admitted, and this is not a classification of all readouts.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FiniteQM.lean`

- file: [lean4/FiniteQM.lean](../../../lean4/FiniteQM.lean)
- sha256 (`bytes`): `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759`
- cited in: node.lean, record TFQ-1011
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qcd.json](../../../dag/research/lean_replay_campaign_finite_qcd.json) (module `FiniteQM`): recorded sha256 `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteQM`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `born_trace_vs_quartic_readout_and_three_ray_positivity_gap` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms born_trace_vs_quartic_readout_and_three_ray_positivity_gap` |
| `qzeta12_rational_readout_cone_and_galois_selection` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms qzeta12_rational_readout_cone_and_galois_selection` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/everett.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/everett.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1011
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1011
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1011
- counts toward the grade: no

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1011_fq_sorkin_readout_class_qm208.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1011_fq_sorkin_readout_class_qm208.md](../../../dag/derivations/10_finite_qm_core/tfq_1011_fq_sorkin_readout_class_qm208.md)
- sha256 (`lf-normalised`): `434977606178e52bd90ca63d34538b8ee42faa035b9fdccb4076e3090d0dd327`
- generated view: listed, not counted
- cited in: record TFQ-1011
- counts toward the grade: no

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md`

- file: [sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md](../../../sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `85ca7b22b1c1e360a4c17ad8a9e0bddae03433592585b01d23a74cd09c82929e`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics_claim_ledger.md`

- file: [sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics_claim_ledger.md](../../../sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics_claim_ledger.md)
- sha256 (`lf-normalised`): `259e971c72c485503b9c9f157bec6ec9412fe24b8c4cc266e1d0ab6aa7e2d1e0`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FQ-R-SORKIN-CLASS` `COMPUTED`: [FQ-PHASE-FIBER-QUOTIENT](FQ-PHASE-FIBER-QUOTIENT.md) (PROVED_LEAN), [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION)

Outgoing (1):

- `FQ-R-GAP-BORN-UNIQUENESS` `CONDITIONAL_ON_IMPORT`: [FQ-GAP-BORN-UNIQUENESS-GLEASON](FQ-GAP-BORN-UNIQUENESS-GLEASON.md) (CONDITIONAL)
