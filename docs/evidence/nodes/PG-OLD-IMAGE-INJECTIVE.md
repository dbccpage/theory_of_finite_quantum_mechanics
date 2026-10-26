# PG-OLD-IMAGE-INJECTIVE

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> If a lift u : A -\> B has a typed recovery r : B -\> A + E with r(u a) = inl a for all a, then u is injective (all types); conversely, for E = Unit, every injective u has such a recovery, and for finite types there are (|A|+1)^(|B|-|A|) of them. Off-image rejection and observation preservation do not follow from the law (general statements). For obstruction repair only persistence of a Boolean predicate through the identity lift is shown; no repair notion is defined.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 15
- distinct cited Lean declarations covered by a current replay receipt: 15
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Off-image refusal is PG-SN-OFF-IMAGE-REFUSAL; a definition of obstruction repair for a lift is still missing, so the repair clause of the source statement is open.

## Source status

Proposition 4 / WDP-P001-005: typed old-image recovery implies injectivity of the lift

## Review

- PFP review: [dag/results/PG-OLD-IMAGE-INJECTIVE/reviews/20261021_batch01b_audit/delivery_review_result.json](../../../dag/results/PG-OLD-IMAGE-INJECTIVE/reviews/20261021_batch01b_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: A recovery r : B -\> A + Unit obeying r(u a) = inl a exists exactly when u is injective. For an injective lift it is determined only on the image: there are (\|A\|+1)^(\|B\|-\|A\|) of them, exactly one of which refuses every off-image point; when \|A\| \>= 1 and \|B\| \> \|A\| the others accept some off-image point as an old term, and for \|B\| = \|A\| or \|A\| = 0 the recovery is unique. The law fixes neither observations nor obstruction predicates (persistence through the identity lift only).
  - does not support: Off-image rejection as a property of the S(n) retraction (that is PG-SN-OFF-IMAGE-REFUSAL, which needs an added soundness hypothesis on r); the pinned SnCarrier lift and retraction; any definition of obstruction repair beyond persistence of a Boolean predicate through a lift (the source repair_not_implied instance uses the constant-true predicate and defines no repair); sets with more than four elements in the native census (the Lean count law_card is general for finite types); infinite types for the count; any physical or categorical reading.
  - next test: Define repair of an obstruction for a lift (a witness-count or chain criterion on the lifted pair) and decide for the identity embedding and for a non-identity injective lift whether the old obstruction count strictly drops, replacing the constant-predicate instance of repair_not_implied by a statement with a stated repair criterion.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/PreGenesisToMssn/Paper.lean`

- file: [lean4/Imported/PreGenesisToMssn/Paper.lean](../../../lean4/Imported/PreGenesisToMssn/Paper.lean)
- sha256 (`bytes`): `5f0ebfc1710b91ce84d4570d7653a3cb8396824adecfaba16fa59a96354b9e12`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.PreGenesisToMssn.Paper`): recorded sha256 `5f0ebfc1710b91ce84d4570d7653a3cb8396824adecfaba16fa59a96354b9e12` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/PreGenesisToMssn/Paper.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `old_image_injective` | yes | yes | yes | none | `#print axioms old_image_injective` |

- counts toward the grade: yes

### Lean: `lean4/Imported/SnMssn/Paper001.lean`

- file: [lean4/Imported/SnMssn/Paper001.lean](../../../lean4/Imported/SnMssn/Paper001.lean)
- sha256 (`bytes`): `1a79ddc7a70157834ee80ed3890124aadd149093336ac49776eab3c167b4fb07`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.SnMssn.Paper001`): recorded sha256 `1a79ddc7a70157834ee80ed3890124aadd149093336ac49776eab3c167b4fb07` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/SnMssn/Paper001.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `off_image_not_implied` | yes | yes | yes | Quot.sound, propext | `#print axioms off_image_not_implied` |
| `old_image_injective` | yes | yes | yes | none | `#print axioms old_image_injective` |

- counts toward the grade: yes

### Lean: `lean4/OldImageInjective.lean`

- file: [lean4/OldImageInjective.lean](../../../lean4/OldImageInjective.lean)
- sha256 (`bytes`): `4f260c7c94cddf35ac4a372fabdfe8f07565dcd50672b382e6d2a3666ff8625d`
- cited in: node.lean, receipt dag/research/pfp_batch01_lean_replay.json (OldImageInjective)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `OldImageInjective`): recorded sha256 `4f260c7c94cddf35ac4a372fabdfe8f07565dcd50672b382e6d2a3666ff8625d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build OldImageInjective`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `OldImageInjective.injective_iff_exists_law` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms OldImageInjective.injective_iff_exists_law` |
| `OldImageInjective.law_card` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms OldImageInjective.law_card` |
| `OldImageInjective.law_card_le` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms OldImageInjective.law_card_le` |
| `OldImageInjective.law_freedom_off_image` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms OldImageInjective.law_freedom_off_image` |
| `OldImageInjective.observation_not_implied_general` | yes | yes | yes | none | `#print axioms OldImageInjective.observation_not_implied_general` |
| `OldImageInjective.observation_not_implied_instance` | yes | yes | yes | none | `#print axioms OldImageInjective.observation_not_implied_instance` |
| `OldImageInjective.observation_preserved_possible` | yes | yes | yes | none | `#print axioms OldImageInjective.observation_preserved_possible` |
| `OldImageInjective.off_image_not_implied_general` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms OldImageInjective.off_image_not_implied_general` |
| `OldImageInjective.off_image_not_implied_instance` | yes | yes | yes | propext | `#print axioms OldImageInjective.off_image_not_implied_instance` |
| `OldImageInjective.old_image_injective` | yes | yes | yes | none | `#print axioms OldImageInjective.old_image_injective` |
| `OldImageInjective.repair_not_implied_general` | yes | yes | yes | none | `#print axioms OldImageInjective.repair_not_implied_general` |
| `OldImageInjective.repair_not_implied_instance` | yes | yes | yes | propext | `#print axioms OldImageInjective.repair_not_implied_instance` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/01_pregenesis/tfq_0371_old_image_injective_lift.md`

- file: [dag/derivations/01_pregenesis/tfq_0371_old_image_injective_lift.md](../../../dag/derivations/01_pregenesis/tfq_0371_old_image_injective_lift.md)
- sha256 (`lf-normalised`): `9da6a29b27f35b0a97aabbee427c58348109c1abdc68c73004512a0318f9971d`
- generated view: listed, not counted
- cited in: record TFQ-0371
- counts toward the grade: no

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0335_from_typed_old_image_recovery_record_injectivity_of_the_lift_only_and_refuse.md`

- file: [dag/derivations/05_mssn_sn/tfq_0335_from_typed_old_image_recovery_record_injectivity_of_the_lift_only_and_refuse.md](../../../dag/derivations/05_mssn_sn/tfq_0335_from_typed_old_image_recovery_record_injectivity_of_the_lift_only_and_refuse.md)
- sha256 (`lf-normalised`): `8f89fd7a8a1e5586b501a9066cb2970205e03f31262fbe69b43061d36ff930a8`
- generated view: listed, not counted
- cited in: record TFQ-0335 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/paper_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/paper_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0335 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean
- TFQ-0335 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/code/sn_mssn_checks.py
- TFQ-0371 lean4: declaration obligation: old_image_injective, scoped to typed recovery on the old image
- TFQ-0371 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean
- TFQ-0371 python: missing obligation: an injectivity check for recover_word on the old alphabet that does not also claim off-image refusal
- TFQ-0371 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/preservation.py
- TFQ-0371 rust: missing obligation: old-image injectivity in crate pre_mssn_preservation, with the three negative boundaries as separate tests

## Routes

Incoming (1):

- `PG-R-OLD-IMAGE` `DERIVED_LEAN`: [PG-REFINE-SEPARATES](PG-REFINE-SEPARATES.md) (PROVED_LEAN)

Outgoing (4):

- `PG-R-OFF-IMAGE` `DERIVED_LEAN`: [PG-SN-OFF-IMAGE-REFUSAL](PG-SN-OFF-IMAGE-REFUSAL.md) (PROVED_LEAN)
- `PG-R-SN-CARRIER` `DERIVED_LEAN`: [PG-SN-CARRIER](PG-SN-CARRIER.md) (PROVED_LEAN)
- `PGW-R-SN-OFF-IMAGE-REFUSAL-PROPOSAL` `DERIVED_LEAN`: [PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL](PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL.md) (PROVED_LEAN)
- `PGW-R-SN-PROTECTED-ANSWER-TRANSPORT` `GAP_NO_DERIVATION`: [PGW-SN-PROTECTED-ANSWER-TRANSPORT](PGW-SN-PROTECTED-ANSWER-TRANSPORT.md) (OPEN)
