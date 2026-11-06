# What this repository holds for Pre-Genesis, Genesis, and S(n) / MSS-N

AuthorityEffect: None. This note inventories records already in `theory_of_finite_quantum_mechanics`. It adds no theorem. Another note covers the external repositories 19L57G1 and H3V7N5QF; those trees were not cloned.

Citations use `theory_of_finite_quantum_mechanics:path::declaration`. A Lean name is the declaration in that file. A markdown name is a heading, or the node-page heading `Statement`.

## How a line is marked

Four marks, exactly one per claim this checkout itself carries:

- **proved in Lean** — a declaration in this checkout, with the axiom list recorded by an existing `#print axioms` receipt. Lean was not rebuilt for this note.
- **computed (exact)** — an exact finite check in this checkout, not a general theorem.
- **stated in prose only** — the text is in this checkout and no in-repo Lean declaration is marked here as proving it.
- **imported** — admitted, or taken in as a premise, and not derived here.

Batch receipt for the sixteen modules below: `theory_of_finite_quantum_mechanics:dag/research/pfp_batch01_lean_replay.json::lean_replay`. Lean 4.35.0, Mathlib `56a005855ea17e0b0958f73ec801ae140b0a1679`, library `PfpBatch01`, exit code 0, axiom audit passed. Allowed axioms named there: `propext`, `Classical.choice`, `Quot.sound`. The receipt's `proof_boundary` says it does not change DAG status. Evidence grades are defined in `theory_of_finite_quantum_mechanics:docs/evidence/README.md::Evidence grades`. E3 requires a matching sha256, exit code 0, a passed axiom audit, and only those standard axioms. E4 is not claimed for these nodes. The honesty gate in `theory_of_finite_quantum_mechanics:dag/pfp/campaign/README.md::The honesty gate (non-negotiable)` is why a DAG status `PROVED_LEAN` whose Lean path is `external_unresolved` is not marked proved in Lean here.

`theory_of_finite_quantum_mechanics:lean4/DerivationDagQMClosure.lean::pg_root_coproduct_inert_diamond_and_six_operation_separation` and the neighbouring `pg_*` theorems in that file are integer and `Fin` identities (for the coproduct one: `(0 : Nat) ≠ 1`, `d + 0 = d`, and a `Fin 6` index test). `theory_of_finite_quantum_mechanics:lean4/RootDiffStructure.lean` says that bridge does not state a coproduct. Those closure theorems have no itemised axiom receipt in `dag/research/`. They are not marked proved in Lean in this note, and they are not treated as proofs of the node statements that cite them.

Stage sizes used below are the tables `theory_of_finite_quantum_mechanics:docs/evidence/stages/PREGENESIS.md`, `theory_of_finite_quantum_mechanics:docs/evidence/stages/GENESIS.md`, and `theory_of_finite_quantum_mechanics:docs/evidence/stages/MSSN_SN.md` (31, 89, and 28 nodes). The map is generated from the DAG and does not by itself prove a statement (`theory_of_finite_quantum_mechanics:docs/evidence/README.md::What this map does not do`).

## Pre-Genesis

Scope of the segment, including the gap from the inscription to the admitted root: `theory_of_finite_quantum_mechanics:dag/derivation_dag_reading_note.md::Segments` and `theory_of_finite_quantum_mechanics:dag/derivation_dag_reading_note.md::Gaps on the path from <>`.

### Data types

Each of these is a definition in a module whose batch replay exited 0. It is not a propositional theorem, so it has no `#print axioms` line. Mark for each: **proved in Lean** only in the sense that the definition type-checks inside that replayed module. Axiom bill: none recorded, because none was printed. Counted below as definitions, not as theorems.

- `theory_of_finite_quantum_mechanics:lean4/RootDiffStructure.lean::RootDiffStructure.Real0` — two constructors, `primitiveDifference` and `structureChannel`. Payload types are arbitrary. The file says this is the constructor shape of `OntologyBasic.Real0` and that that file is not imported.
- `theory_of_finite_quantum_mechanics:lean4/AdmissionFloor.lean::AdmissionFloor.ExhibitedCut` — a relation, two endpoints, an exhibited pair, and an irreflexive law.
- `theory_of_finite_quantum_mechanics:lean4/InertDiamond.lean::InertDiamond.Ev` — `supply`, `admit`, `form`. Instance, rule, and imposition events are not in this type.
- `theory_of_finite_quantum_mechanics:lean4/InertDiamond.lean::InertDiamond.St` — admitted data as a list, and form arities as a list. `init` is both empty.
- `theory_of_finite_quantum_mechanics:lean4/InertDiamond.lean::InertDiamond.Chan` — two labels used only for the predicate `HasCoproduct`.
- `theory_of_finite_quantum_mechanics:lean4/SixOperations.lean::SixOperations.Op` — `mention`, `supply`, `designate`, `admit`, `retain`, `operate`.
- `theory_of_finite_quantum_mechanics:lean4/SixOperations.lean::SixOperations.St` — six `Finset` fields, one per operation.
- `theory_of_finite_quantum_mechanics:lean4/PrimdiffAxioms.lean::PrimdiffAxioms.Kernel` — a finite carrier and a list of triples `(N × N × T)`.
- `theory_of_finite_quantum_mechanics:lean4/PrimdiffAxioms.lean::PrimdiffAxioms.KErr` — `a1` or `carrier`.
- `theory_of_finite_quantum_mechanics:lean4/HistoryReport.lean::HistoryReport.ReportImage` — subtype of reports that some history hits.
- `theory_of_finite_quantum_mechanics:lean4/HistoryReport.lean::HistoryReport.FiberConstant` — equal reports imply equal answers.
- `theory_of_finite_quantum_mechanics:lean4/PregenConstructive.lean::PregenConstructive.recon` — first-match reconstruction on an explicit list, requiring `DecidableEq` on the report type.
- `theory_of_finite_quantum_mechanics:lean4/CollapseBarrier.lean::CollapseBarrier.Factors` — existence of a post-composition through the whole codomain.
- `theory_of_finite_quantum_mechanics:lean4/DemandAccounting.lean::DemandAccounting.next` — `(W \ D) ∪ B`.
- `theory_of_finite_quantum_mechanics:lean4/OldImageInjective.lean::OldImageInjective.OldImageLaw` — `r (u a) = inl a`.
- `theory_of_finite_quantum_mechanics:lean4/RefineSeparates.lean::RefineSeparates.refine` — `a ↦ (q a, t a)`. The tag `t` is an input.
- `theory_of_finite_quantum_mechanics:lean4/FreeMonoidNoniso.lean::FreeMonoidNoniso.IsAtom` — not the unit, and every factorisation has a unit factor.
- `theory_of_finite_quantum_mechanics:lean4/FreeMonoidNoniso.lean::FreeMonoidNoniso.WordIso` — the source's word-isomorphism record; `WordIso.toMulEquiv` sends it to a monoid equivalence.
- `theory_of_finite_quantum_mechanics:lean4/ChainRetraction.lean::ChainRetraction.Hom` — `ker d` quotiented by the boundaries from the previous map. One degree of an `R`-module complex.

### Primitives and admission rules

- **imported.** `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PG-ROOT-DIFF-STRUCTURE.md::Statement`. The node status is `ADMITTED_PRIMITIVE`. The two channels are posits. The review's narrowest claim is only the typed coproduct of arbitrary payloads. The route from the inscription `<>` to this root is `GAP_NO_DERIVATION` (`theory_of_finite_quantum_mechanics:dag/derivation_dag_reading_note.md::Gaps on the path from <>`).
- **imported.** `theory_of_finite_quantum_mechanics:code/rust/src/wdp/primitive_axiomatics.rs::PrimitiveDifferenceAxiom` — ten names `A01NonIdentification` through `A10AntiReificationFirewall`, with no predicate on the enum. `theory_of_finite_quantum_mechanics:lean4/PrimdiffAxioms.lean` records the same list as underived. Node `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PG-PRIMDIFF-AXIOMS.md::Statement` is status `DEFINITION`.
- **proved in Lean** (the kernel's accept/refuse behaviour, not a derivation of A1–A10). `theory_of_finite_quantum_mechanics:code/rust/src/wdp/primitive_axiomatics.rs::GenesisAdmissionKernel::admit_difference` refuses `a = b` and refuses endpoints outside the carrier, then stores the triple. The Lean statements of that behaviour are the `admit_*` theorems in the PrimdiffAxioms list below. The Rust function is the same rule as code, not a second proof.
- **proved in Lean.** Supply does not change the admitted set; only `admit` does. Theorems `SixOperations.supply_keeps_admitted`, `step_changes_admitted_iff`, `run_changes_admitted_iff` below. This is a model. It does not derive Reading L versus Reading F.
- **proved in Lean.** In `InertDiamond`, unrooted `step` on `supply` returns the same state (`step_supply` is `rfl`; the replay theorems are below). Rooted replay treats the first supply of the root token as an admission precondition (`rooted_root_supply_is_precondition`). A rival step that admits on supply is exhibited (`rival_supply_not_inert`), so inertness is a rule of the model, not a consequence of the spelling `<>`.
- **stated in prose only.** `theory_of_finite_quantum_mechanics:dag/derivations/01_pregenesis/tfq_0417_pregenesis_grammar.md::1. Abstract & Formal Statement`. Alphabet `{<, >, a, b}`, three public starts, no event productions. The note says there is no Lean statement of the grammar. The `.ebnf` file is not in this checkout (`theory_of_finite_quantum_mechanics:dag/fragments/pregenesis_to_wdp.json::segment_note` places unprefixed grammar paths in `the_symbol_game`).
- **stated in prose only.** `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-NO-TRANSITION-QUIESCENCE.md::Statement`. Empty transition relation means no successor. Node status `DEFINITION`.
- **stated in prose only.** `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-OBSERVATIONAL-EQUIVALENCE.md::Statement`. `x ≈ₙ y` means every observation in the stage family `Oₙ` agrees. Node status `DEFINITION`.
- **stated in prose only.** `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-ADMISSION-BEFORE-DISTINCTION.md::Statement`. Distinguishability of `<a>` and `<ab>` is not evaluated before admission. Node status `DEFINITION`.
- **stated in prose only.** `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-ABSENCE-OF-RULE-NOT-IDENTIFICATION.md::Statement`. Absence of a distinguishing rule is not itself an identification. Node status `DEFINITION`.
- **imported.** `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-IDENTITY-CONVENTION-UNDECIDABLE.md::Statement`, and the later node `theory_of_finite_quantum_mechanics:docs/evidence/nodes/COMP-C1-IDENTITY-CONVENTION-INPUT.md::Statement` (status `IMPORTED_ASSUMPTION`). The Lean carrier is `theory_of_finite_quantum_mechanics:lean4/GenesisComputation.lean::GenesisComputation.IdentityConvention` (`opaqueConv`, `exactInscription`). The module header says the convention is never derived.

### Invariants and boundary statements proved in Lean

Receipt module sha256 values are the `sha256` fields of `pfp_batch01_lean_replay.json`. "Axioms: none" means the receipt list for that declaration is empty.

`RootDiffStructure` (sha256 `63a62b1dcd98373ab6a5019b54e567ad7d55894f6eca73a95a19e6f5af305084`), node `PG-ROOT-DIFF-STRUCTURE`. These do not prove that either real channel exists or that either is irreducible for the inhabited record types. The file says both emptiness directions of retraction exist when both channels are inhabited.

- Axioms: none. `pd_injective`, `st_injective`, `pd_ne_st`, `exhaustive`, `no_identification`, `real0_empty_of_both_empty`, `posits_independent`.
- Axioms: `Quot.sound`. `universal`.
- Axioms: `Classical.choice`. `nonempty_real0_iff`.
- Axioms: `Classical.choice`, `Quot.sound`, `propext`. `card_real0`, `card_maps_out`, `card_maps_out_pow`, `retracts_to_pd_iff`, `retracts_to_s_iff`, `no_reduction_to_pd`, `no_reduction_to_s`, `retractions_both_ways_of_nonempty`.

`AdmissionFloor` (sha256 `6974f4c9df701c53aac00d5831e99669b5f2810c7a2e1587763cc6ed1324a717`), node `PG-ADMISSION-FLOOR`. The law is supplied data.

- Axioms: none. `endpoints_apart`, `no_cut_on_subsingleton`, `identification_breaks_law`, `cut_exists_iff_nontrivial`, `exists_law_target_iff`, `instance_without_law`, `law_without_instance`, `law_not_derived_from_distinctness`, `pointed_relation_independence`.
- Axioms: `Classical.choice`, `Quot.sound`, `propext`. `two_point_cut_count`, `one_point_cut_count` (counts of relations on `Fin 2` and `Fin 1`).

`InertDiamond` (sha256 `3981d4df4b464251865c5b3553c96467f64024927f11710f0769f1bef4880dd7`), node `PG-INERT-DIAMOND` (status `DEFINITION`; the theorems are about the model).

- Axioms: none. `no_coproduct_of_single_token`.
- Axioms: `Quot.sound`, `propext`. `admit_changes_state`.
- Axioms: `propext`. `replay_filter_supply`, `replay_eq_of_same_admissions`, `mention_count_irrelevant`, `step_changes_only_by_admission`, `supply_then_admit_root`, `rooted_refuses_without_root`, `rooted_root_supply_is_precondition`, `rooted_later_supply_inert`, `root_only_no_coproduct`, `rooted_with_coproduct`, `coproduct_without_inscription`, `inscription_without_coproduct`, `inscription_does_not_determine_coproduct`, `rival_supply_not_inert`.

`SixOperations` (sha256 `a05c568c76bd1e1a4b574171bf80fb2980e661d7f5d1f42d4f9ea826c1a849a1`), node `PG-SIX-OPERATIONS` (status `DEFINITION`).

- Axioms: `Classical.choice`, `Quot.sound`, `propext`. `supply_keeps_admitted`, `step_admitted_of_ne_admit`, `step_changes_admitted_iff`, `run_admitted`, `run_changes_admitted_iff`, `run_without_admit`, `six_results_pairwise_distinct`, `readings_separated_six_ops`, `readings_collapse_when_supply_admits`, `supply_admits_conflation_separates`, `designate_retains_conflation_separates`, `designation_is_overwritten`, `repeated_admit_does_not_grow_set`.

`PrimdiffAxioms` (sha256 `f41974512bd2143da41aa286cf55a45b2169c2e6690996bc01945cbea4ad8e16`). Proved about the defined kernel and about a small cochain reading. Not a derivation of A1–A10. The file says the rational-valued `Φ₁` of the source is not covered, and that `A7` read as "`d₁` vanishes on `im d₀`" is `A5` again.

- Axioms: none. `rtc_preorder`, `rtc_least`.
- Axioms: `propext`. `d1_d0`, `a1_a4_a5_independent_on_three_vertices`, `empty_structure_is_a_model`.
- Axioms: `Quot.sound`, `propext`. `exact_closed`.
- Axioms: `Classical.choice`, `Quot.sound`, `propext`. `admit_error_a1`, `admit_ok_iff`, `admit_token_irrelevant`, `admit_preserves_inv`, `duplicates_stored`, `reverse_orientation_accepted`, `face_nilpotent_iff`, `descends_iff`, `defect_gauge_invariant`, `exact_not_closed`, `trichotomy`, `rcl_eq_none_iff`, `rcl_defined_of_nilpotent`, `rcl_refuses_zero_one`, `a5_iff_nilpotent`.

`CollapseBarrier` (sha256 `2e19515baccbf10fe7fb8b82c5c58490ba6808cd877924acdef7eb56606e7561`), node `PG-COLLAPSE-BARRIER`.

- Axioms: none. `barrier`, `factors_iff_fails_without_nonempty`, `refine_separates`, `two_point_one_bit`, `two_point_no_factor`.
- Axioms: `Classical.choice`. `factorsImage_iff`.
- Axioms: `Classical.choice`, `Quot.sound`, `propext`. `factors_iff_of_nonempty`, `factors_iff_exact`, `tag_separates`, `tag_card_lower_bound`, `tag_exists`, `tag_alphabet_iff`.

`HistoryReport` (sha256 `420e89ea7590479d90d1a16e9cea9b70f634e5dfc18d283397143f8c06773c0f`), node `PG-HISTORY-REPORT-CRITERION`. The file separates the choice-free directions from `selector_exists`.

- Axioms: none. `fiberConstant_of_factors`, `factors_of_fiberConstant_of_selector`, `not_factors_of_split`, `off_image_not_unique`.
- Axioms: `Classical.choice`. `selector_exists`, `history_report_criterion`.
- Axioms: `Quot.sound`. `factor_unique_on_image`, `extension_unique_of_surjective`.
- Axioms: `propext`. `instance_split`.

`PregenConstructive` (sha256 `6b600af885a14319d1f3cca3afa4631bb388eb8b88aa9b4993d31643538d28d9`), node `PG-PREGEN-CONSTRUCTIVE-SUMMARY`. The node's own `lean` field is flagged `proved_lean_external_only`; the receipt names this in-repo file, and the sha256 matches. The choice-free theorems do not use `Classical.choice`. The classical variant does.

- Axioms: none. `recon_of_fiberConstant`, `fiberConstantOn_of_recon`, `listed_history_report_criterion`, `recon_eq_none_iff`, `recon_unique`, `recon_wrong_off_list`, `listed_factor_exists`, `instance_reconstructs`.
- Axioms: `propext`. `instance_not_fiberConstant`, `instance_wrong_off_list`.
- Axioms: `Classical.choice`, `Quot.sound`, `propext`. `listed_history_report_criterion_classical`.

`DemandAccounting` (sha256 `caa7cae003a1790f98cbc16d56af7ee2d50116c8d2b56b3c5d734da5185ec14c`), node `PG-DEMAND-ACCOUNTING`. Identity `|next| = |W| - |D| + |B|` needs `D ⊆ W` and `Disjoint (W \ D) B`.

- Axioms: none. `list_overlap_not_nodup`.
- Axioms: `Quot.sound`, `propext`. `list_register_nodup_iff`, `list_length_no_disjointness`.
- Axioms: `Classical.choice`, `Quot.sound`, `propext`. `demand_accounting`, `card_next_exact`, `formula_iff`, `fails_without_subset`, `fails_without_disjoint`, `holds_accidentally_without_hypotheses`, `fails_of_excess_without_overlap`, `single_violation_fails`, `nat_truncation_masks_subset_violation`, `every_step_is_an_accounting`, `split_not_determined`.

`RefineSeparates` (sha256 `27eb996394f29091540847f284ccfb33e220f0e6d25974810e9888ff4223a5ea`), node `PG-REFINE-SEPARATES`.

- Axioms: none. `refine_retains`, `refine_separates`, `refine_keeps_old_separation`, `proper_union`.
- Axioms: `propext`. `refine_separates_iff`, `resolves_iff_proper`.
- Axioms: `Quot.sound`, `propext`. `no_one_bit_of_odd_cycle`, `triangle_no_one_bit`.
- Axioms: `Classical.choice`, `Quot.sound`, `propext`. `card_bits`, `bits_iff_colours`, `fibre_bits_iff`, `fibre_one_bit_iff`, `fibre_report_bits_iff`, `refine_separates_many`.

`OldImageInjective` (sha256 `4f260c7c94cddf35ac4a372fabdfe8f07565dcd50672b382e6d2a3666ff8625d`), node `PG-OLD-IMAGE-INJECTIVE`. The law is exactly injectivity of `u`. Off-image refusal, observations, and repair are not implied.

- Axioms: none. `old_image_injective`, `observation_not_implied_general`, `observation_preserved_possible`, `observation_not_implied_instance`, `repair_not_implied_general`.
- Axioms: `propext`. `off_image_not_implied_instance`, `repair_not_implied_instance`.
- Axioms: `Classical.choice`, `Quot.sound`, `propext`. `injective_iff_exists_law`, `law_freedom_off_image`, `off_image_not_implied_general`, `law_card_le`, `law_card`.

`FreeMonoidNoniso` (sha256 `97453073da4c402585e900368fd9f71837da6621bc43bd43d9cd409b67027990`), node `PG-FREE-MONOID-NONISO`. Unequal finite alphabets give non-isomorphic free monoids. For `n, m ≥ 1` the underlying sets are both countably infinite, so the obstruction is multiplicative, not a difference of set-cardinalities (`bijection_but_not_isomorphic`). `Discrete` here is the discrete category, not a path space.

- Axioms: `Quot.sound`. `isAtom_map_iff`, `free_monoid_zero_subsingleton`.
- Axioms: `Quot.sound`, `propext`. `isAtom_iff`.
- Axioms: `Classical.choice`, `Quot.sound`, `propext`. `alphabetEquiv`, `no_free_monoid_iso`, `freeMonoid_iso_iff_equiv`, `discrete_equivalence_card`, `no_discrete_equivalence`, `discrete_equivalence_iff`, `set_bijection_exists`, `bijection_but_not_isomorphic`, `card_words_of_length`, `card_atoms`, `unequal_finite_alphabets_not_wordiso`.

`ChainRetraction` (sha256 `94f50b9df3ae5fa4f31c1461289535ce947ac7d769e9aece38acd2556451ed26`), node `PG-CHAIN-RETRACTION`. If `r ∘ i = id` on the middle module and `r` commutes with the incoming boundary, the induced map on that homology is injective (`Hmap_injective`), so a chain retraction cannot kill a nonzero old class (`cannot_kill`). The file says the argument is degree by degree and is not restricted to finite modules. The converse fails for multiplication by 2 on `ℤ` (`TimesTwo.converse_fails_over_int`). Two named non-examples: two points, and a triangle boundary.

- Axioms: none. `cannot_kill`.
- Axioms: `Classical.choice`, `Quot.sound`, `propext`. `Hmap_injective`, `kernel_trivial`, `no_retraction_of_killed`, `TwoPoints.cls_ne_zero`, `TwoPoints.cls_killed`, `TwoPoints.no_chain_retraction`, `Triangle.square_zero`, `Triangle.cls_ne_zero`, `Triangle.cls_killed`, `Triangle.no_chain_retraction`, `TimesTwo.converse_fails_over_int`.

### Pre-Genesis claims only in prose, or only as external records

- **stated in prose only.** `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT.md::Statement`. Supplying `<a>` changes the presented inscriptions and leaves the internal observations fixed. Node status `CONDITIONAL`.
- **imported.** Five `SOURCE_RECORD` nodes, none with an in-repo evidence file: `theory_of_finite_quantum_mechanics:docs/evidence/nodes/TFQ-0364.md::Statement`, `theory_of_finite_quantum_mechanics:docs/evidence/nodes/TFQ-0368.md::Statement`, `theory_of_finite_quantum_mechanics:docs/evidence/nodes/TFQ-0419.md::Statement`, `theory_of_finite_quantum_mechanics:docs/evidence/nodes/TFQ-0420.md::Statement`, `theory_of_finite_quantum_mechanics:docs/evidence/nodes/TFQ-0429.md::Statement`.

Theorem count in this section, from the `#print axioms` lines of the thirteen modules (the batch receipt lists 173 anchors: it omits one theorem each in PrimdiffAxioms, PregenConstructive and RefineSeparates): RootDiffStructure 17, AdmissionFloor 11, InertDiamond 16, SixOperations 13, PrimdiffAxioms 21, CollapseBarrier 12, HistoryReport 9, PregenConstructive 11, DemandAccounting 14, RefineSeparates 14, OldImageInjective 12, FreeMonoidNoniso 14, ChainRetraction 12. Total 176. Definitions listed above: 19.

## Genesis stage

The DAG stage `GENESIS` has 89 nodes (`theory_of_finite_quantum_mechanics:docs/evidence/stages/GENESIS.md`). Of the 36 with status `PROVED_LEAN`, 35 are grade E0 with flag `proved_lean_external_only`: every cited Lean path is `external_unresolved`. They are listed under **Not available**, not as proved in Lean. The remaining one, `PG-GEN-REWRITING-COMMUTATION`, is grade E2 because `theory_of_finite_quantum_mechanics:lean4/DerivationDagQMClosure.lean::pg_gen_rewriting_commutation_and_obstruction_persistence` is in this checkout. That declaration says: an injective `Nat → Nat` preserves inequality of two numbers, and a true `pairInList` membership stays true after consing pairs. It does not mention `Step.rename`, `Reach.rename`, or the Genesis state `(T, A, a, b)`. No receipt itemises its axioms. It is not marked proved in Lean here.

What this checkout does prove about a Genesis-shaped event semantics is in `theory_of_finite_quantum_mechanics:lean4/GenesisComputation.lean`, DAG stage `COMPUTATION`, not `GENESIS`. The header says `Regime`, `Event`, `stepE`, and `replayE` are a byte copy of a staged `SupplyErasure.lean` block, itself from the sealed derivation, and that no embedding of Genesis `Step3` into word rewriting is proved. Axiom lines are the recorded output `theory_of_finite_quantum_mechanics:dag/research/genesis_to_universal_computation.axioms.txt` (Lean 4.35.0, Mathlib v4.35.0, 81 declarations, none outside `propext`, `Classical.choice`, `Quot.sound`). That file is not an evidence-map sha256 receipt: `theory_of_finite_quantum_mechanics:docs/evidence/README.md::What this map does not do` says `*.axioms.txt` is not used for grading, and the computation nodes that cite this module are below E3 (`proved_lean_below_e3`). The names and axiom lists below are taken from that file, whose line numbers match the `#print axioms` block at the end of `GenesisComputation.lean`.

### Data types in the copied event semantics

Definitions, not theorems. Mark: defined in `lean4/GenesisComputation.lean` (not given a theorem axiom bill).

- `theory_of_finite_quantum_mechanics:lean4/GenesisComputation.lean::GenesisComputation.GenesisCopy.Regime` — fields `data : Nat`, `forms`, `insts`, `rules`, `reqs`.
- `theory_of_finite_quantum_mechanics:lean4/GenesisComputation.lean::GenesisComputation.GenesisCopy.Event` — `supply`, `admitDatum`, `admitForm`, `admitInst`, `admitRuleAll`, `impose`.
- `theory_of_finite_quantum_mechanics:lean4/GenesisComputation.lean::GenesisComputation.GenesisCopy.stepE` — `supply` returns `some r` unchanged; `admitDatum` increments `data` with no upper bound in the match.
- `theory_of_finite_quantum_mechanics:lean4/GenesisComputation.lean::GenesisComputation.GenesisCopy.replayE` — `foldlM stepE`.
- `theory_of_finite_quantum_mechanics:lean4/GenesisComputation.lean::GenesisComputation.UnarySep` — mirror of hole-only unary separation by instance membership. Not the external `separable`.
- `theory_of_finite_quantum_mechanics:lean4/GenesisComputation.lean::GenesisComputation.Step` — one word step under a one-hole context.
- `theory_of_finite_quantum_mechanics:lean4/GenesisComputation.lean::GenesisComputation.Reach` — reflexive-transitive closure of `Step`.
- `theory_of_finite_quantum_mechanics:lean4/GenesisComputation.lean::GenesisComputation.GCtx` — slot tuple of `Option`, the mirror of a Genesis context.

### Theorems about that copy

All of the following are **proved in Lean**, axioms as recorded in `genesis_to_universal_computation.axioms.txt`.

- Axioms: none. `genesis_context_count_n2_a3`, `genesis_one_hole_count_n2_a3`. These are `decide` on one pair `(n, a) = (2, 3)`: 19 contexts with a hole and 12 with exactly one hole. The general rectangle is the computed check below, not these two theorems.
- Axioms: `propext`. `first_separation_replay`, `separated_marks_not_collapsed`, `Step.context`, `Reach.context`, `Reach.map`, `ofSplit_injective`, `replay_admitDatum_replicate`, `genesis_unbounded_admission`.
- Axioms: `propext`, `Quot.sound`. `first_separation_pairwise`, `canonicalRegime_pairwise`, `Mark2.toDatum_bijective`, `unarySep_iff`, `pairwiseSeparated_iff`, `canonicalRegime_four_pairwise_decide`, `two_marks_without_forms_collapsed`, `Reach.of_map`, `Step.exists_of_map`, `plug1_ofSplit`, `supply_growth`.
- Axioms: `propext`, `Classical.choice`, `Quot.sound`. `holes_ofSplit`, `oneHole_iff_split`, `rtg_iff_mem_reachN_card`, `card_wordsLE`, `mem_succList`, `reachB_iff`, `decideReachB_iff`, `reachSet_card_le`, `ReachB.reach`, `Reach.exists_bound`, `reach_iff_reachB_of_closed`, `verdict_reachable_sound`, `verdict_unreachable_sound`, `verdict_boundExceeded_witness`, `not_closed_of_unbounded`, `closed_bounds_reach`, `stepE_data_mono`, `decode_encode`, `encodeWord_injective`, `decodeMarks_encodeMarks`, `encodeMarks_injective`, `encodeMarks_append`.

That is 43 theorems. `first_separation_replay` checks one history of two data, one unary form, one instance, and one demand. The module says the cost-two minimum itself is not in this checkout. `canonicalRegime_pairwise` is pairwise separation for the mirror `UnarySep` on the canonical regime of every `n`, at item cost `2(n - 1)`, not a theorem about the sealed responder. `replay_admitDatum_replicate` and `genesis_unbounded_admission` show that this `stepE` has no cap on `admitDatum`. They do not derive an unbounded supply of marks.

- **imported.** `theory_of_finite_quantum_mechanics:lean4/GenesisComputation.lean::GenesisComputation.UnboundedSupply` and `theory_of_finite_quantum_mechanics:docs/evidence/nodes/COMP-C4-UNBOUNDED-SUPPLY-IMPORT.md::Statement`. Status `IMPORTED_ASSUMPTION`. `not_closed_of_unbounded` is the proved implication from that hypothesis; the supply is not derived.
- **computed (exact).** `theory_of_finite_quantum_mechanics:code/rust/src/wdp/genesis_tm.rs::context_count_formula_and_one_hole_splits`. For each `n` from 0 through 4 and each arity `a` from 1 through 5, the enumerated context list has length `(n + 1)^a - n^a`, and the one-hole subcount is `a * n^(a - 1)` when `n ≠ 0` (and the `n = 0` cases written in the test). Integer arithmetic only. This is not a proof for every `n` and `a`. The general formula node `PGW-CONTEXT-COUNT-FORMULA` is external and is not marked proved in Lean.

### Genesis-stage text in this checkout, with no in-repo proof

Each line is **stated in prose only**. The evidence map flags the four `PROVED_PROSE` nodes `proved_prose_no_in_repo_document`. The derivation papers restate the DAG; `theory_of_finite_quantum_mechanics:docs/evidence/README.md::Evidence grades` does not count those generated papers as evidence.

Definitions (node status `DEFINITION`), except the freeze ledger, which is imported below:

- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PG-MSS0-ONLY-DIAMOND.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PG-GEN-REGIME-EVENTS.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-METATHEORY-OBJECT-LANGUAGE-SPLIT.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-REGIME-ISOMORPHISM-UNORDERED-PAIRS.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-CONTEXTS-PLUGGING-PROFILES.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-RESPONSES-COSTS-MU1-MU2.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-CHALLENGE-SOURCE-POLICIES.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-FIVE-PRESENTATION-QUESTIONS.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-GO-ADMISSION-GATE.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-DECLARED-CHALLENGE-IMPORT-PER-LEVEL.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-TYPED-REQUIREMENT-KINDS.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-CAPABILITY-STAGE-COUNTER.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-CANDIDATE-EXTENSION-GENERATOR.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-FOUR-GATE-ACTIVE-OBSTRUCTION.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-GENESIS-TO-SN-CROSSWALK.md::Statement`

Prose proofs (status `PROVED_PROSE`):

- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-NO-ENDOGENOUS-DEMAND-GENERATOR.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-IDENTITY-IS-INDEX-NOT-PROFILE.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-MINIMAL-OR-INITIAL-REFUSED.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-SEALED-TERMINAL-STATEMENT.md::Statement`

Conditional (status `CONDITIONAL`; hypotheses not derived here):

- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-RUNG2A-STAKE-DECLARED-LABEL.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-RUNG3-FIRST-DEMAND-INDEX.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-RUNG4-INDEX-UP-TO-ISOMORPHISM.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-RUNG5-SYMMETRY-ALONG-HISTORY.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-RUNG6-SUCCESSION-ELEMENT-COUNT.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-RUNG7-DURATION-UNDER-CHANGING.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-RUNG8-ELEMENT-COUNT-ACROSS-ISO.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-RUNG9-TWO-NESS-OBSERVATIONAL-CLASSES.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-RUNG10-RESPONDER-ADJACENCY-REACH.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-C1-ENGINE-CLASS-144.md::Statement`

Imported records of external Genesis bookkeeping:

- **imported.** `theory_of_finite_quantum_mechanics:docs/evidence/nodes/TFQ-0383.md::Statement` (status `SOURCE_RECORD`; the counted file is `code/rust/src/general_relativity/exact_regge/closure.rs`, which is not a derivation of the ledger row).
- **imported.** `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md::Statement`. The text reports a closeout of 19L57G1. This checkout does not prove that closeout.

`GenesisCompTM.lean` and `GenesisCompUniv.lean` are in this checkout and are named in the same axioms file. They are DAG stage `COMPUTATION` (Turing machines and a Mathlib evaluator). They are not Genesis-stage object language and are not itemised here. The paper `theory_of_finite_quantum_mechanics:dag/research/genesis_to_universal_computation.md::1. Where Genesis ends` says Mathlib's computability theory is imported infrastructure.

## S(n) and MSS-N

Segment statement: `theory_of_finite_quantum_mechanics:dag/derivation_dag_reading_note.md::Segments` (S(n) presentation carrier and the Witnessed Difference Programme window). MSS-N is recorded as an external atlas, not the next stage after Genesis: `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-MSSN-ATLAS-NOT-DERIVATION.md::Statement`.

The off-image module is DAG stage `PREGENESIS` (`PG-SN-OFF-IMAGE-REFUSAL`) and is listed here because it is the S(n) retraction law proved in this checkout. Its theorems are not counted again in the Pre-Genesis total.

### Data types

Definitions in replayed modules. Same mark as the Pre-Genesis definitions: type-checked in a module whose batch replay exited 0; not propositional theorems.

- `theory_of_finite_quantum_mechanics:lean4/SnCarrierPfp.lean::SnCarrierPfp.Base` — `ground`, `supplied`, `relation` of `Rel` (`pair`, `cut`, `simplex`).
- `theory_of_finite_quantum_mechanics:lean4/SnCarrierPfp.lean::SnCarrierPfp.Pres` — those three, plus `lift`, `retraction`, and `nonDescent`.
- `theory_of_finite_quantum_mechanics:lean4/SnCarrierPfp.lean::SnCarrierPfp.sectionLift` — section on base presentations at a stage index.
- `theory_of_finite_quantum_mechanics:lean4/SnCarrierPfp.lean::SnCarrierPfp.retr` — retraction down-map; off the five base shapes, or at the wrong stage, it returns `nonDescent`.
- `theory_of_finite_quantum_mechanics:lean4/SnCarrierPfp.lean::SnCarrierPfp.carrierCard` — the table `0,1,2,2,4,5,6` and then `n ↦ n`. The file says the source calls this declared, not derived. `Carrier n` is `Fin (carrierCard n)`.
- `theory_of_finite_quantum_mechanics:lean4/SnCarrierPfp.lean::SnCarrierPfp.baseCard` — `1 + g + 3 g²`.
- `theory_of_finite_quantum_mechanics:lean4/SnOffImageRefusal.lean::SnOffImageRefusal.SectionRetraction` — old-image law plus soundness (`r y = inl x` implies `s x = y`).
- `theory_of_finite_quantum_mechanics:lean4/ObligationMonoid.lean::ObligationMonoid.Ob` — `Fin k → Nat`, pointwise sum. The file says this is the free commutative monoid on `k` ids and that Genesis events and S(n) maps are not shown to be morphisms into it.
- `theory_of_finite_quantum_mechanics:lean4/ObligationMonoid.lean::ObligationMonoid.Ev` — `declareTerm`, `assertDiff`, `removeDiff`, `identifyTerms`. The table `evOb` is copied, not derived. `removeDiff` and `identifyTerms` are sent to the same counter (`event_table_not_injective`).
- `theory_of_finite_quantum_mechanics:lean4/ObligationMonoid.lean::ObligationMonoid.Ledger` — `gen` and `dis` counters. `Valid` means `dis i ≤ gen i` at every id.

### Theorems proved in Lean

`SnCarrierPfp` (sha256 `f55efb45cdedf884efc81d7dd16fd0f2f8bf04fc5e44b2d41f0b2fc36762ec2f`), node `PG-SN-CARRIER`. The review's narrowest claim is this restatement (glyph alphabet abstracted, wrappers flattened). It does not derive `carrierCard` from `Base`, and it does not identify the restatement with a 36-glyph `Glyph` type except for the one arithmetic instance `baseCard 36 = 3925`.

- Axioms: none. `ground_carrier_empty` (`Carrier 0` has no inhabitant, because `carrierCard 0 = 0`).
- Axioms: `propext`. `old_image_base`, `sectionLift_injective`, `unrestricted_lift_not_injective`, `no_recovery_for_unrestricted_lift`, `refusal_token_round_trip_changes_input`, `baseCard_36`.
- Axioms: `Quot.sound`, `propext`. `table_ne_base_stage_zero`, `no_alphabet_matches_stages_one_two`.
- Axioms: `Classical.choice`, `Quot.sound`, `propext`. `card_base`, `card_image_sectionLift`, `table_ne_base_stage_two`, `table_ne_base_stage_three`, `table_eq_base_stage_one_iff`.

`SnOffImageRefusal` (sha256 `fd9d0acd0e1a3985cc23bc94ceff041a7e80a5ae6c1845c3d6ff9a252629d972`), node `PG-SN-OFF-IMAGE-REFUSAL`. The law alone does not refuse; soundness does (`lax_retraction_obeys_law_but_accepts_off_image`). The pinned half is for every alphabet `G`, not only 36 glyphs. The node's own `lean` field is flagged external; the receipt names this file.

- Axioms: none. `SectionRetraction.injective`, `refused_iff_off_image`, `roundtrip_iff_in_image`, `roundtrip_fails_off_image`.
- Axioms: `Quot.sound`, `propext`. `toy_refused_iff_odd`.
- Axioms: `propext`. `refuseOffImage_isSectionRetraction`, `lax_retraction_obeys_law_but_accepts_off_image`, `sn_is_section_retraction`, `sn_refused_iff_off_image`, `sectionLift_injective`, `old_image_base`, `accepted_only_from_section`, `accepted_iff`, `nonDescent_iff_off_image`, `retraction_stage_strict`, `inImage_iff`, `lax_breaks_refusal_characterisation`, `instance_refusals`.

`ObligationMonoid` (sha256 `b5afec8bddd5021a809a91368fa00e26538962fce7a27f1e1acd08f3e79ac1c5`), node `PG-OBLIGATION-MONOID`.

- Axioms: `propext`. `valid_fresh_order_blind`, `event_table_not_injective`.
- Axioms: `Quot.sound`, `propext`. `combine_assoc`, `combine_comm`, `combine_empty`, `combine_cancel`, `no_inverse`, `trace_append`, `trace_total`, `trace_terms`, `trace_assertions`, `trace_destructive`, `cost_floor`, `combineB_assoc`, `discharge_valid`, `discharge_ok_iff`, `discharge_never_generated`, `over_discharge_needs_generated`, `run_valid`, `run_from_empty_valid`, `genB_valid`, `overdischarge_instance`.
- Axioms: `Classical.choice`, `Quot.sound`, `propext`. `lift_single`, `lift_unique`, `trace_swap`, `genB_none_iff`.

Theorem count in this section: SnCarrierPfp 14, SnOffImageRefusal 18, ObligationMonoid 26. Total 58. Definitions listed: 10.

### S(n) / MSS-N text in this checkout, with no in-repo proof

Each line is **stated in prose only**.

- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-SN-TWO-BOXED-LAWS.md::Statement` — two design rules. The derivation `theory_of_finite_quantum_mechanics:dag/derivations/05_mssn_sn/tfq_0510_sn_two_boxed_laws.md::1. Abstract & Formal Statement` says no checker enforces them. Status `DEFINITION`.
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-SN5-CONTINUATION-RECORDED-REQUEST.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-MSSN-ATLAS-NOT-DERIVATION.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-MSSN-ASCENT-TRIAD.md::Statement` — declared successor, candidate lift, and licensed lift are three statuses.
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-MSSN-ALPHABET-DECLARATIONS.md::Statement` — `Γ38` and `Σ36` as declared alphabets. The grammar file is not in this checkout.
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-MSSN-MANY-READINGS.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-MSSN-SYNTAX-NOT-DECODING.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-MSSN-ROWS-1-TO-6-SPECIFIED.md::Statement` — rows MSS-1 to MSS-6 unlicensed.
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-MSSN-L1-CUTS-HODGE-ROWS.md::Statement` — row MSS-8 as a specified target. Not the proved `ObligationMonoid`.
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-SN4-POLICY-CLOSURE-CYCLE-SPACE.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-SN-POSTNIKOV-REFUSAL.md::Statement` — the index `n` is not Postnikov depth. This is prose. No homotopy group is defined.
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-SN-E18-L1-TIES-L2-CENTER.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-SN-E19-TORSION-ERASED-OVER-Q.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-SN-E20-OBSERVER-COMPLETION.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-SN-E21-REPAIR-RANK.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-SN-E08-WEIGHTED-L1-DUALITY.md::Statement` — status `CONDITIONAL`.

## Counts

Marks on claims this checkout carries, counted from the lists above:

| Mark | Count | What is included |
|---|---|---|
| proved in Lean | 277 theorems | Pre-Genesis `#print axioms` lines 176 (the batch receipt lists 173 anchors), GenesisComputation anchors 43, S(n) receipt anchors 58 |
| proved in Lean | 29 definitions | 19 Pre-Genesis carriers, 0 extra Genesis theorem-definitions in that 43, 10 S(n) carriers. The 8 Genesis copy types are listed and are not in this 29, because their module has an axioms file rather than a sha256 batch receipt. They are definitions in `lean4/GenesisComputation.lean`, not theorem marks. |
| computed (exact) | 1 | the Rust context-count rectangle |
| stated in prose only | 51 | Pre-Genesis 6 (grammar, quiescence, observational equivalence, admission-before-distinction, absence-of-rule, presentation-not-expressive-lift), Genesis 29 (15 definitions, 4 prose proofs, 10 conditionals), MSS-N 16 |
| imported | 11 | Real_0 posit, A1–A10 names, identity convention, five Pre-Genesis source records, unbounded supply, TFQ-0383, Genesis freeze ledger |

The 29 definition lines are not theorems. If a count of theorem marks only is wanted, use 277. The 8 Genesis copy types are additional definitions without a batch-receipt axiom line.

## Not available in this repository

### No infinite object of these stages

No infinite carrier is admitted as a Pre-Genesis inscription, a Genesis regime, or an S(n) presentation. `ChainRetraction` states its one-degree lemma for arbitrary modules, finite or not; that is not an infinite Genesis object. `FreeMonoidNoniso.bijection_but_not_isomorphic` records that the underlying sets of `FreeMonoid (Fin n)` and `FreeMonoid (Fin m)` for `n, m ≥ 1` are countably infinite and still not monoid-isomorphic. No infinite colimit, no infinite ordinal stage, and no continuum Hilbert space is constructed in the three stages. The reading note lists the continuum Hilbert lift, Stone's theorem, and the U(1) circle as open imports outside this fragment (`theory_of_finite_quantum_mechanics:dag/derivation_dag_reading_note.md::Gaps on the path from <>`).

### No path space and no homotopy

`PGW-SN-POSTNIKOV-REFUSAL` is prose that the construction index `n` is not a Postnikov truncation depth. This checkout does not define a path object, a path concatenation, a homotopy, or a homotopy group for `<>`, for a Genesis regime, or for S(n). `FreeMonoidNoniso.discrete_equivalence_iff` is an equivalence of discrete categories. `ChainRetraction.Hom` is a module homology at one degree, not a homotopy type of a space.

### No composition of higher cells

No 2-cell, 3-cell, or higher cell is composed in these stages. `theory_of_finite_quantum_mechanics:lean4/DerivationDagQMClosure.lean::master_operad_25_family_composition_and_end_to_end_chain_closure` is a block of arithmetic identities and a `Fin 25` inequality test. It is not an operad composition. The obligation monoid's `combine` is pointwise addition of counters on `Fin k`, not composition of cells. MSS-N rows that mention circulation or Hodge data are prose targets (`PGW-MSSN-L1-CUTS-HODGE-ROWS`, `PGW-SN-E08-WEIGHTED-L1-DUALITY`), not proved higher-cell calculus.

### Gap from the inscription to the admitted root

`theory_of_finite_quantum_mechanics:dag/derivation_dag_reading_note.md::Gaps on the path from <>`: no derivation in the sources read there joins the inscription `<>` to `Real_0 = PrimitiveDifference ⊔ Structure`. `InertDiamond.inscription_does_not_determine_coproduct` is a theorem that one model does not force the other. It is not that missing derivation.

### Genesis object-language items this checkout does not prove

External Lean paths cited by these nodes resolve as `external_unresolved` on the node pages (sibling trees `omega_engine_atlas/.../genesis` or `omega_engine_education/...`, not files in this checkout). DAG status `PROVED_LEAN` is not a proof in this repository. The fragment note `theory_of_finite_quantum_mechanics:dag/fragments/pregenesis_to_wdp.json::segment_note` says Lean paths prefixed for 19L57G1 at commit `85a83ae7ce64dc2123ff218568a4ecd37e566d33` are not in this checkout.

Status `PROVED_LEAN`, Lean not in this checkout (36 Genesis nodes, plus two Pre-Genesis nodes and nine MSS-N nodes):

- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PG-GEN-SUPPLY-NO-OP.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PG-GEN-SUPPLY-ERASURE.md::Statement` — the byte copy of `stepE` proves supply is a no-op on that copy; the node also asks for both Reading L and Reading F, which the review says the copy does not settle.
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PG-GEN-NO-RETURN.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PG-GEN-IRREFLEXIVE-DISTINCT.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PG-GEN-ONGOING-OBSTRUCTION.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PG-GEN-ONGOING-FEWEST-CHANGES.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PG-GEN-REWRITING-COMMUTATION.md::Statement` — sealed `Step.rename` / `Reach.rename`. The in-repo `Nat` lemma and the word-renaming theorems are not that statement.
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-CHALLENGE0-INERTIA-SECOND-TOKEN.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-COLLAPSE-WITHOUT-INSTANCES.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-CHALLENGE2-ADMITTED-BUT-COLLAPSED.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-CONTEXT-COUNT-FORMULA.md::Statement` — the general count `(n+1)^a - n^a` for every regime. Only the Rust rectangle and one Lean `decide` are in this checkout.
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-COLLECTION-EXTENSIONALITY.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-CHALLENGE3-CURRENT-REGIME-FAILS.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-MU1-MINIMUM-NOT-UNIQUE-L.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-MU1-ARITY-INDEXED-TIE-FAMILY.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-ORBIT-BRANCHING-REPAIRS-LEAST-PAIR.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-RESPONSE-EXISTENCE-MARK-PROGRESS.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-PRUNING-LEMMAS-COST-TWO.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-COUNT-INVARIANCE-TRANSPORT.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-POLICY-ENDPOINT-ALL-SEPARATED.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-D2-INITIAL-POINTED.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-QUOTIENT-RETENTION.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-FAITHFUL-DESCENT-ROUND-TRIP.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-CANONICAL-KEY-CLASSIFICATION.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-INCIDENCE-CONSTRUCTION-BETTI.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-C2-RUN-FORWARD-EVERY-HISTORY.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-GO-REACH-CEILING.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-GO-CONTRACTION-STEP2-STEP3.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-GO-MULTIPLICITY-MONOTONE.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-GO-TWO-RELATIONS-SWAP.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-GO-LEFTOVER-UNBOUNDEDNESS.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-GO-H1-CANCELLATION-EXCESS.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-GO-H2-STATE-RAISING-GAUGE.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-GO-H3-TWIN-FILLS-HOLONOMY.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-ENDOGENOUS-DEMANDS-EXOGENOUS-PAYMENTS.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-STAGE-CHANGE-CONTRACT-PROPOSAL-RECORD.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-FORCED-SEPARATION-LIFT-NOT-UNIQUE.md::Statement` (stage `PREGENESIS`)
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-REPLAY-NECESSITY.md::Statement` (stage `PREGENESIS`)
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-SN0-GROUND-INERTIA.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-SN1-SUPPLY-NOT-ADMISSION.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-SN2-OPAQUE-COLLAPSE.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-SN3-COST-TWO-UNARY-MARK.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-SN-ENDPOINT-LEMMA.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL.md::Statement` — cites external `SnOffImage.lean`. The in-repo proof is `SnOffImageRefusal`, already marked above, and is not this node's external file.
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-SN-REPRESENTATION-QUOTIENT.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-SN-E12-CIRCULATION-FUNCTIONAL.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-MSSN-CIRCULATION-OBSTRUCTION.md::Statement`

Status `COMPUTATIONALLY_CHECKED` with flag `computational_no_runnable_test` and no counted in-repo evidence file. The numbers in the node statements are not recomputed here:

- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PG-GEN-COLLAPSE-AND-FIRST-SEPARATION.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PG-GEN-SAMENESS-REFINEMENTS.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-BOUNDED-TIE-CENSUS.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-BRANCH-TREES-AND-ROLES.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-CLOSED-BASELINE-TERMINATES.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-GENESIS-THREE-AXIS-VERDICT.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-RUNG0-INHERITANCE-REPLAY.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-RUNG2B-STAKE-MENU.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-FORCED-CENSUS-COLUMN.md::Statement`

Status `OPEN` (no derivation recorded in the node):

- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/TFQ-0374.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/TFQ-0376.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-CONTEXT-FIDELITY.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/TFQ-0385.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/TFQ-0396.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-RUNG1-STREAM-AS-RESPONSE.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-K-ITEM-DELTA-GRAMMAR.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-RESPONDER-IN-LEAN.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-CONTEXT-DECISION-PROCEDURE.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-DECLARED-INPUT-FLOOR.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-PYTHON-LEAN-CARRIER-BRIDGE.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-ISOMORPHISM-SOUNDNESS-IN-LEAN.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-RUNS-PAST-DECLARED-BOUNDS.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-STREAM-AT-FOUR-ITEMS.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-DRIVER-B-SEVENTH-EVENT.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-ENDOGENOUS-DEMAND-OB1.md::Statement`
- `theory_of_finite_quantum_mechanics:docs/evidence/nodes/PGW-SN-PROTECTED-ANSWER-TRANSPORT.md::Statement`

Also absent, as named by the module headers rather than by a second proof:

- Reading L and Reading F as a sealed pair of regimes, beyond the two machines compared in `SixOperations.readings_separated_six_ops`.
- The sealed responder that minimises the cost-at-most-two candidate space (`PGW-RESPONDER-IN-LEAN`).
- A theorem that `carrierCard` equals the cardinality of a derived `Carrier n` (`SnCarrierPfp` header).
- Any theorem that Genesis events or S(n) maps are homomorphisms into `ObligationMonoid.Ob` (`ObligationMonoid` header; node text of the gap is the MSS-N record that events are not yet monoid morphisms).
- The host grammars `pre_genesis.ebnf` and `mssn.ebnf` as runnable checkers.
- The rational weighted primal-dual programme stated as MSS-8 / E08.
- An identification of `RootDiffStructure.Real0` with `OntologyBasic.Real0` beyond constructor shape.
