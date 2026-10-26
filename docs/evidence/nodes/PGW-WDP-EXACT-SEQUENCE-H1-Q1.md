# PGW-WDP-EXACT-SEQUENCE-H1-Q1

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> WDP-CH04-P03: in a window with d₁d₀ = 0, κ¹(\[h\]) = d₁h is well defined on Q¹ because d₁(h + d₀α) = d₁h + d₁d₀α = d₁h, and 0 → H¹ → Q¹ → im d₁ → 0 is exact with H¹ = ker κ¹; closedness of a class does not depend on the representative, so H¹ is the usual Z¹/B¹ of the window. The sequence is an extension: in finite dimension it splits, but a splitting Q¹ ≅ H¹ ⊕ im d₁ requires a chosen section and is not canonical. Lean kappa_exact_sequence, with kappa_well_defined and kappa_mk, establishes on the literal quotient Quot (Repair d₀), for an additive d₁ with d₁ ∘ d₀ = 0, that the inclusion of H¹ is injective, its image is the kernel of κ, a class has zero charge exactly when every representative is closed, and κ maps onto the image of d₁; these three declarations use no axioms.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared window with additive d₁ and a d₁d₀ = 0 certificate (assumption)

## Bottleneck

The Lean statement is narrower than the row: set-level exactness on the literal quotient, without additive structure on Q¹, additivity of κ¹ or the splitting remark; it takes the window as declared and is not a Genesis derivation of it (TFQ-0344).

## Source status

WDP monograph §4.8 WDP-CH04-P03; Lean Obstruction.kappa_exact_sequence (narrower set-level statement)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean)
- sha256 (`bytes`): `bef8623978d7c0735b4a02db686664b03b61e18bba0e5ef6bcce81ff4234dd0a`
- cited in: node.lean, node.source, record TFQ-0546
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_wdp.json](../../../dag/research/lean_replay_campaign_wdp.json) (module `Imported.WitnessedDifference.WitnessedDifference.Obstruction`): recorded sha256 `bef8623978d7c0735b4a02db686664b03b61e18bba0e5ef6bcce81ff4234dd0a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `kappa_exact_sequence` | yes | yes | yes | none | `#print axioms kappa_exact_sequence` |
| `kappa_mk` | yes | yes | yes | none | `#print axioms kappa_mk` |
| `kappa_well_defined` | yes | yes | yes | none | `#print axioms kappa_well_defined` |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md)
- sha256 (`lf-normalised`): `753d1c99c799f84f9a71912b98082d590c89c531f980c112b62ee2a86ab2726b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0546_wdp_exact_sequence_h1_q1.md`

- file: [dag/derivations/06_wdp/tfq_0546_wdp_exact_sequence_h1_q1.md](../../../dag/derivations/06_wdp/tfq_0546_wdp_exact_sequence_h1_q1.md)
- sha256 (`lf-normalised`): `8ecaf8bf42477d4f935786ebf92b718884c997966ffa2aee1fd5eee753abb54c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0546
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/006_oewdp/levels/level_03_discrete_complex_cochains.md`

- file: `omega_engine_education/documentation/006_oewdp/levels/level_03_discrete_complex_cochains.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0546 python: the ledger binds WDP-CH04-P03 to no executable; obstruction.py computes signatures, not the sequence
- TFQ-0546 rust: no Rust statement of the degree-1 exact sequence

## Routes

Incoming (1):

- `PGW-R-WDP-EXACT-SEQUENCE-H1-Q1` `DERIVED_LEAN`: [PG-WDP-DEGREE1-WINDOW](PG-WDP-DEGREE1-WINDOW.md) (DEFINITION), [PG-WDP-QUOTIENT-EXACT-SEQUENCE](PG-WDP-QUOTIENT-EXACT-SEQUENCE.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-TRICHOTOMY-BOUNDS` `DERIVED_PROSE`: [PGW-WDP-TRICHOTOMY-BOUNDS](PGW-WDP-TRICHOTOMY-BOUNDS.md) (PROVED_PROSE)
