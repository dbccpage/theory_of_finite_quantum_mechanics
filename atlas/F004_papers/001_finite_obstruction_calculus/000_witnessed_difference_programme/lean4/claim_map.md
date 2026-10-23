# Claim-to-declaration map

This map is bound to the canonical claim inventory in
`../witnessed_difference_programme.md`. It covers all 154 unique claim IDs
exactly once. A Lean declaration is named only when its statement matches the
canonical claim at the stated finite scope.

## Exact theorem bindings

- `WDP-CH03-P01` maps to
  `WitnessedDifference.Symmetry.no_fully_invariant_point`.
- `WDP-CH07-P01` maps to
  `WitnessedDifference.FinitePath.duration_append`.
- `WDP-CH07-P02` maps to
  `WitnessedDifference.FinitePath.exact_duration_path_independent`;
  `duration_potential` is its telescoping lemma.
- `WDP-CH14-P01` maps to
  `WitnessedDifference.presentation_blind_spot`.
- `WDP-CH16-P01` maps to
  `WitnessedDifference.Descent.function_descends_iff_fiber_constant`.
  The theorem makes the quotient map's surjectivity explicit and applies to
  the manuscript by taking the target to be `q ∘ T`.
- `WDP-CH04-P07` maps to
  `WitnessedDifference.Obstruction.dual_certificate_lower_bound` and
  `matching_certificate_is_optimal`, over a finite edge list with ℚ weights,
  which is the row's stated scope.
  The bound is proved against every repair cost, which is the same as a bound
  on their infimum.
- `WDP-CH04-P08` maps to
  `WitnessedDifference.Obstruction.filled_triangle_signature`, over ℚ; its
  lower bound is derived from `dual_certificate_lower_bound`.
- `WDP-CH10-P02` maps to
  `WitnessedDifference.ObserverResolution.declared_family_order`, which bundles
  `observer_kernel_preorder`, `identity_observer_finest`, and
  `zero_observer_coarsest`. Kernels are equivalence kernels of report maps;
  for a linear report f they are determined by its linear zero kernel through f(x)=f(y) iff x−y belongs to ker(f). The equivalence relation and the linear subspace are distinct objects; this correspondence is not itself formalized here.
- `WDP-CH10-P03` maps to
  `WitnessedDifference.ObserverResolution.grammar_resolution_bound`, which
  bundles `visible_classes_le_grammar` (a map separating `k` classes needs at
  least `k` reports) and `pigeonhole_resolution_limit`. The bounded-length
  string count stated after the row in the manuscript is not mechanized.
- `WDP-CH01-P02` maps to
  `WitnessedDifference.PointedRelation.pointed_relation_independence_fin`,
  which exhibits the countermodels on `Fin 1` and `Fin 2`; the universe-general
  `pointed_relation_independence` states the same non-implications over all
  types.
- `WDP-CH16-P02` maps to
  `WitnessedDifference.Descent.obstruction_empty_iff_factors`,
  `factor_unique_of_surjective`, `section_factorization_iff`, and
  `section_factorization_all_sections` (bundled in
  `presentation_descent_signature`). The obstruction set is stated literally as
  the existence of a pair with equal presentation and unequal target.
- `WDP-CH18-P02` maps to
  `WitnessedDifference.ClassicalCorner.nonnegative_weights_force_permutations`,
  which bundles `preservesStates_iff_stochastic` and
  `reversible_iff_permutation` (proved through `perm_of_stochastic_inverse`)
  for a finite carrier and rational weights. Mathlib's `σ.permMatrix` is the
  prose's `P_{σ⁻¹}`, which does not affect the existential. The general-carrier
  preservation clauses `permutation_isometry_int` are a separate statement,
  mentioned in the prose.
- `WDP-CH18-P03` maps to
  `WitnessedDifference.ClassicalCorner.signed_weights_break_the_corner`.
- `WDP-CH18-P04` maps to
  `WitnessedDifference.ClassicalCorner.unitary_package_is_classical`, which
  states, with one permutation σ, the monomial form with entries 1, -1, i or -i
  (`gaussian_unitary_is_monomial`, `gaussian_unit_cases`), the readout moving by
  that σ (`readout_of_monomial`), and fibre preservation, over `GaussianInt` for
  any finite carrier. The run statement after the proof is
  `gaussian_run_readout`. The remark about signed permutation matrices over ℤ is
  prose only.
- `WDP-CH18-P05` maps to
  `WitnessedDifference.ClassicalCorner.classical_corner_ends`, which bundles
  `hadamard_similitude`, `hadamard_separates_fibre`, `hadamard_not_unitary`,
  `pythagorean_rotation_separates_fibre`, and `half_mixer_separates_fibre`.
  The rotation is stated over ℚ with its entries shown to lie in (1/5)ℤ. The
  half mixer is stated over `QuadraticAlgebra ℚ (-1) 0`, that is ℚ(i), with its
  entries shown to lie in (1/2)ℤ[i], and its square shown to be the toggle.
- `WDP-CH19-P02` maps to
  `WitnessedDifference.PacketAdapter.measurement_packet_adapter`, which states
  `Empirical.adapt_eq_inr_iff` and `Empirical.adapt_succeeds_iff` for tables of
  `MeasurementPacket`s under a declared profile. The adapter is
  `Empirical.adapt`; its refusals carry their evidence in the type
  `Empirical.Refusal`. It is defined with classical choice, so the statements
  describe its values rather than a Lean evaluation.
- `WDP-CH19-P03` maps to
  `WitnessedDifference.PacketAdapter.what_survives_the_adapter`, which bundles
  `support_is_backed_by_accepted_packets` (through `backs_iff` and
  `Empirical.adapt_support`), `Empirical.freq_eq_of_outcomes`, and
  `Empirical.freq_eq_freq_iff`. The evidence in `Backs` holds for every
  admissible packet by its type, so the support clause adds nothing that the
  image records. The two examples in the prose are
  `recalibration_is_invisible` and `evaluator_is_lost`; the latter exhibits one
  concrete pair of packets.
- `WDP-CH19-P04` maps to
  `WitnessedDifference.PacketAdapter.every_model_is_a_packet_image`, an
  instance of `Empirical.exists_table`; `toy_realizes` shows that its
  outcome-availability hypothesis holds for a concrete CHSH profile.
  `Empirical.Run` is an arbitrary tuple of individually admissible packets,
  and the table type is `List`, so free tuple formation and arbitrary finite
  repetition are built into the formal domain. The declaration does not
  establish joint experimental availability in a theory with additional
  restrictions on allowed runs.
- `WDP-CH19-P05` maps to
  `WitnessedDifference.PacketAdapter.contextuality_is_a_missing_global_table`.
  It bundles `Empirical.noncontextual_iff_global_table` for any cover and any
  profile under the hypothesis and free table domain of CH19-P04,
  `Empirical.chsh_le_two_of_global_table`
  (through `chsh_le_two_of_noncontextual`) for any profile on the CHSH cover,
  `Empirical.prBox_signed_not_nonneg`, and `Empirical.pr_box_packet_table` for
  the concrete profile `toyProfile`. `Empirical.GlobalRun` likewise permits
  arbitrary tuples over all measurements, with repetition supplied by `List`.
  Global sections have rational weights. The manuscript's rational
  feasible-point argument that a real nonnegative section of a rational model
  yields a rational one is a written extension, not part of this Lean binding.

- `WDP-CH18-P07` maps to
  `WitnessedDifference.ClassicalPackage.stochastic_updates_are_mixtures_of_functions`,
  which bundles closure under composition and the identity, the
  characterization of deterministic updates as function updates, and the
  mixture decomposition with weights `funWeight`, together with
  `ClassicalCorner.nonnegative_weights_force_permutations` for the
  characterization of state-preserving updates as column-stochastic matrices
  and of the units as permutations. A presentation map is a function, so it is
  a function update. Everything is over ℚ.
- `WDP-CH18-P08` maps to
  `WitnessedDifference.ClassicalPackage.classical_package_and_sharpness`. It
  bundles the nonnegativity, consistency and normalization of the outcome law
  of a classical instrument (`Instrument.law_nonneg`, `law_consistent`,
  `law_total`), `Empirical.chsh_le_two_of_noncontextual`, the PR-box values
  `prBox_signed_not_nonneg` and `chsh_prBox`, and the signed shear of
  `ClassicalCorner.signed_weights_break_the_corner`. The reading of the package
  S in the vocabulary of §19.10 is prose and is not part of the row.
- `WDP-CH19-P06` maps to
  `WitnessedDifference.ToleranceAdapter.tolerant_adapter_signature`, which
  bundles `adaptTol_zero_iff_adapt`, `adaptTol_mono` and `tolerant_of_within`.
  The typed refusals are `TolRefusal`; `adaptTol_eq_inr_iff` (with
  `Empirical.adapt_eq_inr_iff` for the equality of frequencies at `ε = 0`) and
  `adaptTol_succeeds_iff` characterize acceptance.
- `WDP-CH19-P07` maps to
  `WitnessedDifference.ToleranceAdapter.two_context_tolerance_iff`, through
  `exists_repair` (the repair `repair2` is at `ℓ¹` distance exactly `D/2` from
  each table) and `tolerant_of_within`. The cover has two contexts indexed by
  `Bool`, and the outcome set is nonempty. That the sampling tolerance follows
  from a trial protocol is not formalized.
- `WDP-CH19-P08` maps to
  `WitnessedDifference.Composition.locallyRecoverable_iff_injective` and
  `dumpRight_not_recoverable`.
- `WDP-CH19-P09` maps to
  `WitnessedDifference.Composition.noSignalling_right` and `noSignalling_left`
  (the complete local instrument sums the Kronecker updates `1 ⊗ K_o` over all outcomes),
  `marginal_independent_of_choice` and
  `presentation_commutes_with_marginal`.
- `WDP-CH19-P10` maps to
  `WitnessedDifference.Composition.composite_state_iff_joint_distribution` and
  `joint_unique`, and, for the CHSH product cover,
  `no_signalling_does_not_force_the_local_composite` (which cites
  `Empirical.prBox`, `prBox_signed_not_nonneg` and `chsh_prBox`).
- `WDP-CH19-P11` maps to
  `WitnessedDifference.AmplitudeBridge.common_phase_iff`,
  `phaseBlind_readout_factors`, `holonomy_gauge_invariant`,
  `cross_eq_holonomy`, `readout_depends_on_cochain_class` and
  `gauge_invariance_does_not_select_the_readout`. Walks are lists of
  vertices, amplitudes are in the unit-norm group of `ℚ(i)`, and the
  cochain is any function `V → V → ℤ`; antisymmetry is not used.
- `WDP-CH19-P12` maps to
  `WitnessedDifference.AmplitudeBridge.exponentiation_obstruction`, which
  bundles `phaseU_no_square_root`, `no_rational_exponentiation`, composition
  of integer exponents and `phaseU_zpow_ne_one`; that coboundaries go to gauge
  transformations is `amp_gauge`.
- `WDP-CH19-P14` maps to
  `WitnessedDifference.InstrumentAdapter.povm_does_not_determine_the_instrument`,
  which bundles `ludersK_complete`, `prepareK_complete`, `same_effects`,
  equality of the probabilities through `prob_eq_effect`, and
  `post_vectors_differ`.

## Exact definition binding

- `WDP-CH07-D01` maps to `WitnessedDifference.FinitePath`,
  `FinitePath.duration`, and their declared edge-weight and `AddMonoid`
  parameters. This is a definition binding, not a theorem promotion.

## Prose-only or narrower-than-claim rows

The following theorem-bearing rows have no exact declaration in this package:

- `WDP-CH01-P01`
- `WDP-CH02-P01`
- `WDP-CH03-P02`
- `WDP-CH03-P03` — no declaration in this package. The absorbed genesis-alpha
  source 006 proved the lower bound, the arity family for two data, and the
  refined uniqueness for two and three data in vendored copies of the external
  Genesis Lean modules; they were not ported and carry no credit here.
- `WDP-CH04-P01`
- `WDP-CH04-P02` — `WitnessedDifference.EmpiricalRepair.matching_objective_lower_bound` proves the lower bound over `Int` for all feasible `z` given dual feasibility and matching cost. Candidate feasibility (nonnegativity `x ≥ 0` and `Ax = b` for `x`) is required by `matching_certificate_optimal`. Rational polyhedral minimizer attainment is proved in the prose by finite rational linear programming, but is not formalized by this declaration. An irrational minimizer for a nonpolyhedral norm is outside that theorem's assumptions.
- `WDP-CH04-C01`
- `WDP-CH04-P03` — `WitnessedDifference.Obstruction.kappa_exact_sequence`,
  with `kappa_mk` and `kappa_well_defined`, proves well-definedness of the
  closure map and a set-level exactness on the quotient by the repair relation.
  The quotient carries no additive structure in the package, additivity of the
  closure map is not proved, and the splitting remark is not formalized.
  Narrower than the row.
- `WDP-CH04-P04`
- `WDP-CH04-P06` — `WitnessedDifference.Obstruction.closure_ratio_signature`
  bundles `closure_ratio_nonneg` and `closure_ratio_bound_of_infimum` for
  ℚ-valued costs, so it covers only windows whose residual and closure masses
  are rational (for example weighted `L¹` over ℚ), not the row's real-valued
  norms. The operator norm enters as any constant `c` satisfying the operator
  bound, and `Φ` through the half of the infimum property saying that `Φ` is at
  least every lower bound of the repair costs. Narrower than the row.
- `WDP-CH04-P09` — `WitnessedDifference.ComplexGrowth.restriction_phi_le`,
  `subdivision_residual_eq`, and `subdivision_phi_eq` prove the restriction and
  one-edge subdivision statements from the lower-bound and greatest-lower-bound
  halves of the infima, which enter as hypotheses; face attachment and
  arbitrary complexes are not formalized. Narrower than the row.
- `WDP-CH04-P10`
- `WDP-CH04-P11`
- `WDP-CH04-P05` — `WitnessedDifference.Obstruction.closure_charge_le_opnorm_mul_phi`
  proves only item 4 (the operator bound), from the infimum property.
- `WDP-CH05-P01`
- `WDP-CH05-P02`
- `WDP-CH05-P03`
- `WDP-CH05-P04`
- `WDP-CH05-P05`
- `WDP-CH05-P06`
- `WDP-CH05-C01`
- `WDP-CH05-P07`
- `WDP-CH05-P08` — no declaration in this package. The absorbed genesis-alpha
  source 004 cited an external Lean proof for integer matrices only; not
  ported, no credit.
- `WDP-CH05-P09`
- `WDP-CH05-P10` — no declaration in this package. The absorbed source 004
  cited an external Lean check of orthogonality and unbiasedness for the
  unnormalized vectors; the reconstruction identity had no Lean. Not ported,
  no credit.
- `WDP-CH05-P11`
- `WDP-CH05-P12` — no declaration in this package. The Lean that the absorbed
  source 005 cites defines the value -1/N as a constant; not ported, no credit.
- `WDP-CH06-P01`
- `WDP-CH07-P03`
- `WDP-CH08-P01` — `Probability.sum_normalizedMultiplicity` proves only
  the narrower natural-multiplicity instance with an explicit nonzero
  denominator.
- `WDP-CH08-P02`
- `WDP-CH08-C01`
- `WDP-CH10-P01` — `WitnessedDifference.Obstruction.observer_passivity_of_infimum`
  takes the fiber-wise lower bound as a hypothesis, which at `y = O q` is the
  inequality itself; `observer_exact_class_stays_exact` derives the exact-class
  corollary from both halves of the infimum property. The clause that states
  identified by the core profile stay identified holds for any function O
  (linearity is not needed) and is not formalized. Narrower than the row.
- `WDP-CH11-P01`
- `WDP-CH11-P02` — no declaration in this package. The absorbed genesis-alpha
  source 011 proved the triangle case of clause 1 and the non-exactness of its
  example over the integers; its Lean evaluates one candidate for clause 3 and
  does not prove the minimum. Not ported; no credit here.
- `WDP-CH14-P02`
- `WDP-CH14-P03`
- `WDP-CH16-P03` — `WitnessedDifference.Descent.retraction_defect_commutes`,
  `retraction_defect_comp_eq`, and `ir_idempotent` prove only that the
  retraction defect commutes with the differential and that `i r` is
  idempotent; the endomorphism-complex reading, the criterion that `ker r` be
  acyclic, the normalization step, and the exclusion of
  `ActiveClosureFailure` are not formalized.
- `WDP-CH16-P04`
- `WDP-CH16-P05` — no declaration in this package. The absorbed genesis-alpha
  source 009 proved the first identity and the flat equivalence for a single
  triple of maps on one carrier type, and the case g = d0 s of the second
  identity for a single quadruple; not ported, no credit.
- `WDP-CH16-C01`
- `WDP-CH18-P01` — W1–W6 are admitted specializations under declared reversible, Gaussian-integer, pairing, or quadratic readout structure. Generic primitive packets do not force these choices; state additional inputs explicitly.
- `WDP-CH18-P06` — no declaration in this package. The absorbed genesis-alpha
  source 004 cited an external Lean check of an equivalent table; read, not
  built or ported, no credit. The current Python `H020` checks the supplied
  eighteen rays, all orthogonality products and incidences before parity;
  this adds executable instance evidence, not a Lean declaration.
- `WDP-CH19-P13` — `WitnessedDifference.InstrumentAdapter.sum_prob`,
  `prob_eq_effect`, `prob_nonneg`, `post` and `instrumentModel` prove the
  probabilities, the trace formula, the post-measurement state and the
  empirical model on the one-measurement cover for a qubit over `ℚ(i)`. The
  application of CH19-P04 to that model and the replay of the receipts through
  the packet of CH13-D01 are prose: `InstrumentAdapter` does not import
  `PacketAdapter`, whose core-only imports clash with Mathlib's notation. The
  probabilities `prob` are declared by the adapter; `prob_eq_effect` proves the
  trace formula over the mixture, not a matrix trace.
- `WDP-CH19-P01` — `WitnessedDifference.Interference.sorkin_I2_cross` and
  `sorkin_I3_biadditive` prove the identity for two and three alternatives
  only, for any additive operation and biadditive ℚ-valued readout (so the
  complex readout of §19.8 is outside it) and without the empty-set term; the
  row's statement for every k at least three is not formalized.
- `WDP-CH09-P01`
- `WDP-CH12-P01` —
  `AcceptedObservation.status_ne_refuse`, `.status_ne_reject`, and
  `acceptance_does_not_entail_authority` are narrower typing/countermodel
  results, not a mechanization of the manuscript's full non-coercion assertion.
  Lean's `EvaluationStatus` has `accept`, `refuse`, and `reject` only; the
  `Undetermined` status of §10.2 and §12.2 is not represented.
- `WDP-CH13-C01` — the package does not formalize interval-order transport.
  `MeasurementPacket.uncertainty_fields_nonnegative` proves only the narrower
  nonnegativity obligations carried by its finite packet.
- `WDP-CH17-P01`
- `WDP-CH17-P02`
- `WDP-CH17-P03`
- `WDP-CH22-C01`

## Definition rows without an exact declaration

These remain definitions in the manuscript. Related Lean structures are
strictly smaller packets and are not asserted to implement the canonical row:

- `WDP-CH01-D01`
- `WDP-CH02-D01`
- `WDP-CH03-D01`
- `WDP-CH04-D01`
- `WDP-CH04-D02` — `WitnessedDifference.Obstruction.Repair`, `Q1`, `kappa`,
  and `H1` model the quotient and closure data abstractly; the norms and the
  diagnostic classes are not formalized.
- `WDP-CH05-D01`
- `WDP-CH06-D01`
- `WDP-CH06-D02`
- `WDP-CH07-D02`
- `WDP-CH08-D01`
- `WDP-CH10-D01`
- `WDP-CH10-D02`
- `WDP-CH10-D03`
- `WDP-CH10-D04`
- `WDP-CH10-D05`
- `WDP-CH10-D06`
- `WDP-CH11-D02`
- `WDP-CH16-D02` — `WitnessedDifference.Descent.retractionDefect` models only
  the defect map, not the contraction data.
- `WDP-CH11-D01`
- `WDP-CH12-D01` — `ObservationReceipt` and `AcceptedObservation` are narrower
  packet types. The former permits every evaluator result; the latter requires
  the result `accept`, so refusal and rejection receipts cannot inhabit it.
- `WDP-CH13-D01` — `MeasurementPacket` is a strictly narrower typed packet,
  not an exact binding. It separates a measurand specification from the result
  carrier, metrological traceability from provenance/re-access, and encodes an
  unbroken nonempty calibration chain with uncertainty at every step.
- `WDP-CH14-D01`
- `WDP-CH15-D01`
- `WDP-CH16-D01`
- `WDP-CH18-D01`
- `WDP-CH20-D01`

## Expert supplement: finite and conditional rows

These source-bound standalone milestones compile with Lean 4.33.1; each is partial coverage of its canonical row. They do not extend the historical Mathlib census or claim analytic/probability/matrix theorem coverage beyond their statements. Reproduce them with scripts/verify_finite_derivations.py.

- `WDP-CH03-O02` — OPEN_CLAIM; partial modules RetentionChoices, FunctionalClassification. Canonical scope and full proofs: Appendix J and docs/derivation_review.md.

- `WDP-CH04-O01` — OPEN_CLAIM; partial modules ContextReflection and FiniteRouting. Canonical scope and full proofs: Appendix J and docs/derivation_review.md.

- `WDP-CH06-O01` — OPEN_CLAIM; partial modules RelationalRetention. Canonical scope and full proofs: Appendix J and docs/derivation_review.md.

- `WDP-CH11-O01` — OPEN_CLAIM; partial modules ObserverDescent. Canonical scope and full proofs: Appendix J and docs/derivation_review.md.

- `WDP-CH14-O01` — OPEN_CLAIM; partial modules FunctionalClassification, SelfReferenceBridges. Canonical scope and full proofs: Appendix J and docs/derivation_review.md.

- `WDP-CH18-O01` — OPEN_CLAIM; partial modules ReconstructionClassification. Canonical scope and full proofs: Appendix J and docs/derivation_review.md.

- `WDP-CH19-O01` — OPEN_CLAIM; partial modules EmpiricalRepair. Canonical scope and full proofs: Appendix J and docs/derivation_review.md.

- `WDP-CH19-O02` — OPEN_CLAIM; partial modules ReconstructionClassification. Canonical scope and full proofs: Appendix J and docs/derivation_review.md.

- `WDP-CH19-O03` — OPEN_CLAIM; partial modules RationalPhaseBoundary. Canonical scope and full proofs: Appendix J and docs/derivation_review.md.

- `WDP-CH19-O04` — OPEN_CLAIM; partial modules InstrumentRepeatability. Canonical scope and full proofs: Appendix J and docs/derivation_review.md.


## Source-bound adapter result

- `WDP-CH10-O01` — OPEN_CLAIM; partial corpus coverage through ObserverAdapterCompleteness, OriginalGenesisObserver, LegacyObserverAdapters and PolicyObserverAdapter. The universal operation/predicate and faithful-completion iff criteria, all-history free extension, faithful original-six adapter, reached-state context quotient iff, G/T classification independence and declared gauge reindexing are proved at their exact scopes. All original source bytes are recovered. The source inventory, transducer algorithm and complete matrix/analysis arguments are separately checked; no single all-corpus Lean theorem is claimed. Appendix K and docs/observer_adapter_completion.md give the full reconciliation.

## Nonclaim rows

These remain scope fences. They have no theorem declaration:

- `WDP-CH00-N01`
- `WDP-CH00-N02`
- `WDP-CH00-N03`
- `WDP-CH01-N01`
- `WDP-CH02-N01`
- `WDP-CH03-N01`
- `WDP-CH04-N01`
- `WDP-CH04-N02`
- `WDP-CH05-N01`
- `WDP-CH05-N02`
- `WDP-CH05-N03`
- `WDP-CH14-N02`
- `WDP-CH16-N02`
- `WDP-CH06-N01`
- `WDP-CH07-N01`
- `WDP-CH09-N01`
- `WDP-CH09-N02`
- `WDP-CH10-N01`
- `WDP-CH13-N01`
- `WDP-CH14-N01`
- `WDP-CH15-N01`
- `WDP-CH16-N01`
- `WDP-CH17-N01`
- `WDP-CH18-N01`
- `WDP-CH19-N01`
- `WDP-CH19-N02`
- `WDP-CH20-N01`

The `WitnessedDifference.OPEN` and `WitnessedDifference.NONCLAIM`
namespaces are documentation registries only. Their constructors are labels,
not propositions or surrogate proofs.

## Resolved finite targets and separate formal milestones

- `WDP-CH03-O01` — BehavioralQuotient.lean proves greatest behavioral equivalence and universal quotient comparison; finite stabilization bound is prose/native, not a Lean termination theorem.
- `WDP-CH05-O01` — Resolved at the declared finite scope in Appendix I; no exact full-row Lean credit.
- `WDP-CH07-O01` — Resolved at the declared finite scope in Appendix I; no exact full-row Lean credit.
- `WDP-CH08-O01` — Resolved at the declared finite scope in Appendix I; no exact full-row Lean credit.
- `WDP-CH13-O01` — Resolved at the declared finite scope in Appendix I; no exact full-row Lean credit.
- `WDP-CH13-O02` — Resolved at the declared finite scope in Appendix I; no exact full-row Lean credit.
- `WDP-CH17-O01` — SemiringCoarseGraining.lean proves power intertwining iff length-one intertwining under algebra laws; matrix partition construction remains prose/native.
- `WDP-CH20-O01` — Resolved at the declared finite scope in Appendix I; no exact full-row Lean credit.

## Additional Genesis bridge register

The new `ProposalAdmissionBridge` module proves sixteen abstract report/decision, guarded admission and ordered replay theorems. Its image-domain scope and executable specializations are recorded in [the separate Genesis bridge ledger](../docs/genesis_bridge_register.md). These entries are additional to the canonical 154-row register; they do not mechanically upgrade broader source-refinement or institutional claims. The current standalone import spine audits forty-two modules and 601 selected declarations. The earlier twenty-seven-module, 379-declaration count was a 2026-10-02 milestone. The spine includes eighteen selected declarations in `FoundationalBridges`, twelve in the later admission/transport supplement, ten in `Source25PairTransport`, twelve aggregate COUNT declarations in `AdmissionCount` and eleven context/cover declarations in `PrimitiveContextFloor`; each current receipt is source-bound and replayed by `verify_finite_derivations.py`.

The latter ten declarations establish the all-finite-sum matrix/fiber
identity and preservation/reflection of the declared partial-run formulas.
They do not supply full-row formal credit for GEN-WDP-O02/O03 or verify the
concrete original/native programs. Their source correspondence and finite
oracle are documented in [the execution supplement](../docs/source_execution_refinement.md).

The eleven `PrimitiveContextFloor` declarations prove one-instance profile
inhabitation, distinct-datum reflection and persistent separation iff the
mentioned tuple covers every proper requirement edge. The carrier type and
finite arity are arbitrary. They do not verify the source/native programs,
classify all delta item shapes or mechanize minimum vertex-cover optimization.
Those arguments and the finite program oracle are stated in
[the primitive execution supplement](../docs/primitive_execution_refinement.md).

The sixteen `RootGaugeNormalization` declarations prove table-level
gradient classification, the complete loop/two-way/ascending-triangle
criterion, raising invariance and pullback/re-normalization at arbitrary
types or finite carrier sizes as stated. The source-bound
[`root_gauge_normalization_axioms.txt`](root_gauge_normalization_axioms.txt)
records `propext` and `Quot.sound` with no admitted proofs. Renaming-orbit
completeness and concrete source/native correspondence are written proofs
with separate finite differential evidence, not full-row formal credit
for GEN-WDP-O02/O03.

The nineteen `MarkedGaugeTransport` declarations prove fixed-writing
gradient classification with retained markings, cyclic/raising/normalization
diagnostic laws and explicit carrier-changing non-descent. The source-step
equalities use the existing `Source25PairTransport` definitions; exact
term-addition and identification countermodels have nonzero target cycles.
The [`marked_gauge_transport_axioms.txt`](marked_gauge_transport_axioms.txt)
receipt binds all proof bytes, with propext and Quot.sound and no admitted
proofs. Joint orbit completeness and concrete program correspondence have
separate written and differential evidence. These statements advance the
source-specific O02/O03 branch without granting whole-obligation credit.

## Faithful representation and the constructive constraint profile

GEN-WDP-49–51 are postcanonical bridge claims, not replacements for
Chapter 20.2's status-coverage definition. `FaithfulRepresentation` has 20
audited declarations for sound transport, finite history composition,
constructive coverage, fair-prefix discovery, exhaustive rejection,
nonstarving interleaving, and anchor/shared-fuel invariants.
`FiniteConstraintRepresentation` has 26 audited declarations for restriction
and gluing, actual system soundness and coverage through admitted histories,
integer indicator defects, uncovered-variable augmentation, exact Cartesian
enumeration, relational transport laws and empty-domain/table boundaries.

The [faithful-representation axiom receipt](faithful_representation_axioms.txt)
and [finite-constraint axiom receipt](finite_constraint_representation_axioms.txt)
bind the compiled sources. The second module's arbitrary-index augmentation
uses Classical.choice; the finite Python encoder scans its explicit scopes.
The effective finite construction and four concrete table transformations have
full written proofs in the [supplement](../docs/faithful_representation_and_relative_completeness.md).
The formal models do not prove JSON admission, hashing, the concrete Python
implementation, arbitrary engine adapters, or institutional authorization.

## Certified progress and observation refinement

GEN-WDP-52–54 / §20.9 and Appendix S add two mathematical modules.
`CertifiedProgress` contributes 23 audited declarations for finite
reachability, losing traps, ranked termination and exact rational upper/lower
certificate laws. `BeliefGameQuotient` contributes 16 for two-sided quotient
transport, budget equality, optional-action monotonicity and the greatest
stable finite relation below a seed. An equivalence seed gives an equivalence
result. Its constructive stabilization bound is the number of listed seed
pairs; the sharper partition-round bound is proved in the manuscript.

The [progress audit](certified_progress_axioms.txt) and
[quotient audit](belief_game_quotient_axioms.txt) bind source hashes.
The [proof supplement](../docs/certified_progress_proof_and_evidence.md)
keeps the mathematical model separate from the concrete Python checker,
producer horizon, JSON admission and institutional authorization. Neither
module promotes a game loss to source unsatisfiability without coverage.

## Foundational histories and additive tensor completion

`GenerativeHistoryCompression` supplies 16 audited declarations underlying
the R7 theorem-map entry: free typed paths, transition replay, the greatest
two-sided contextual congruence, quotient composition and the telescoping
endpoint boundary. It does not choose the generating signature or protected
questions and does not claim the quotient is finite.

`AdditiveTensorCompletion` supplies 12 audited declarations binding
GEN-WDP-58/59: the free-alternative uniqueness theorem, signed difference
decomposition, the Grothendieck extension, generic biadditive operation
extension and the universal factor/uniqueness property of the free group on
generator pairs. The [derivation](../docs/derivations/additive_tensor_completion_derivation.md)
and [axiom receipt](additive_tensor_completion_axioms.txt) keep this algebraic
integer tensor object separate from Hilbert tensor selection, dagger,
positivity, norm completion and Born readout.

`DaggerObserverPairing` supplies 12 audited declarations binding
GEN-WDP-60/61. A declared generator involution extends additively, remains
involutive and acts componentwise on the algebraic tensor. A supplied
two-coordinate integer observer induces a symmetric positive semidefinite
Gram form whose self-null space equals the observer kernel; equal reports are
exactly null signed differences. The [derivation](../docs/derivations/dagger_observer_pairing_derivation.md)
and [receipt](dagger_observer_pairing_axioms.txt) retain the nonuniqueness of
positive forms and the rank-one obstruction to integer complex structure.

`FiniteHermitianization` supplies 17 audited declarations binding
GEN-WDP-62/63. The module constructs exact Gaussian-rational multiplication
and a scalar action from a supplied rational-linear complex structure. A
compatible symmetric positive-semidefinite form produces a conjugate-symmetric
sesquilinear pairing whose diagonal is nonnegative real and whose radical is
the original form radical. The rational-plane instance proves the hypotheses
are constructive; the opposite-orientation instance proves that positivity
does not select $J$. The [derivation](../docs/derivations/finite_hermitianization_derivation.md)
and [receipt](finite_hermitianization_axioms.txt) do not claim scalar
completion, state/effect cones, Born readout or physical reconstruction.

`FiniteStateEffectReadout` supplies 13 audited declarations for the
constructive side of GEN-WDP-64/65. A nonzero two-by-two Gaussian-rational
Gram factor presents a normalized positive state; a complete pair of Gram
factors presents a binary effect and complement. The formal trace numerator
is an exact Frobenius sum of squares, so accepted and rejected rational values
are nonnegative and sum to one. The [derivation](../docs/derivations/finite_state_effect_readout_derivation.md)
and [receipt](finite_state_effect_readout_axioms.txt) restrict coverage to the
declared Gram-factorable class and do not claim that positivity, normalization
or phase invariance uniquely selects the admitted trace readout.

`FiniteProcessComposition` adds 12 selected declarations binding the
constructive side of GEN-WDP-66–68. It proves dagger reversal of multiplication,
matrix associativity, equality of branch mass with the earlier readout
numerator, mass partition for a complete binary process, sequential factor
composition, and mass preservation and reversibility for a supplied unitary.
The exact bit-flip fixture proves unitarity, basis transport and round trip.
The [derivation](../docs/derivations/finite_process_composition_derivation.md) and
[receipt](finite_process_composition_axioms.txt) distinguish this finite
two-dimensional model from physical process selection, the instrument/channel
nonselection countermodel in Python, approximate synthesis and universal
quantum computation.

## Preserver supplement bindings

These bindings are separate from the 154 canonical WDP-CH rows and the
historical Mathlib census. The complete statements and corrections are in
[Chapter 19A](../witnessed_difference_programme.md#chapter-19a) and its
[proof supplement](../docs/derivations/certified_preserver_derivation.md).

| Supplement | Lean declarations | Exact scope |
|---|---|---|
| WDP-R12-P01 | `CertifiedPreservers.transition_representative_independent`, `transition_bounds`, `table_injective_iff_same_ray` | General supplied R9 complex structure and positive definite compatible form; full-table separation. No mechanized finite tomography count. |
| WDP-R12-P02 | `unit_norm_phase_classification`, `phase_injective`, `phase_inverse`, `phase_counterexample`, `equal_multiplier_iff_unit_phase` in `CertifiedPreservers` | Exact rational circle and scalar multiplier law; the separate torsion-subgroup proof is written only. |
| WDP-R12-P03 | `RationalUnitaryReachability.gaussian_norm_iff_prime_parity` | Defines primality and even numerator/denominator valuations. The rational two-squares equivalence is an explicit premise, not a custom axiom or a newly proved prime theorem. |
| WDP-R12-O02 | `equal_norm_unitary`, `ray_reachable_iff_gaussian_norm`, `reachability_from_two_squares` in `RationalUnitaryReachability` | Constructs a linear isometry and two-sided inverse; only the parity corollary imports arithmetic as a premise. |
| WDP-R12-P04 | `projection_idempotent`, `projection_selfadjoint`, `projection_probability`, `projection_zero_iff_zero_probability`, `projection_same_ray_at_positive_probability`, `projection_complement_mass` in `CertifiedPreservers` | Exact named rank-one branch, positive-probability target ray and complement; no optimal cost or physical measurement theorem. |
| WDP-R12-O01, partial | `rational_scalar_hom_two_branches` and `ProjectiveFrameRigidity.frame_scalars_equal` / `mixed_ray_branch_rigidity` | Rational-fixing scalar homomorphisms and the coordinate-frame steps of projective uniqueness. Existence of a semilinear representative for a global preserver remains a written coordinate proof. |

WDP-R12-P05, the bicommutant portion of WDP-R12-O03, and WDP-R13-P01
are not represented as fully mechanized by these bindings. Python/Rust
implementations have separate tests; the Lean model does not verify their
machine arithmetic or implementation semantics.

## Derivation-audit bindings (DP-1 to DP-9, 2026-10-06)

These rows bind the finite parts of the `coda_wdp_derivations_20261006`
proposals to new Lean-core modules (only `Init` imported). They are separate
from the canonical WDP-CH rows and from the sealed release. Every listed
declaration reports axioms within `propext`, `Quot.sound`, `Classical.choice`.

| Proposal | Lean declarations | Exact scope |
|---|---|---|
| DP-1 | `decoder_exists_iff_fiber_constant`, `decoder_unique`, `not_fiber_constant_iff_collision`, `decoder_xor_collision`, `empty_source_has_decoder`, `refinement_transfers`, `refinement_converse_fails`, `fixture_factorable`, `constant_report_collides`, `decoder_off_image_not_unique` in `ComponentReports` | Arbitrary types; decoder on the realized image. Codomain membership is part of the type, not a separate premise. |
| DP-6 | `glue_exists_unique`, `compatible_of_restricts`, `not_compatible_iff_witness`, `empty_cover_glues`, `CoverPresheaf.restriction_matches`, `existence_failure_zero_extensions`, `uniqueness_failure_two_extensions`, `CoverPresheaf.every_matching_extends_iff` in `ComponentReports` | Total functions on a family of subsets; presheaf controls only on the two-set cover of a two-point carrier. |
| DP-2 | `Pseudometric.zero_equivalence`, `Pseudometric.well_defined_iff`, `Pseudometric.separated_iff`, `indiscrete_quotient_singleton`, `fiber_diameter_le`, `strict_gap_forces_equivalence`, `equality_threshold_countermodel`, `worked_example_distances` in `ComponentReports` | Rational pseudometrics on arbitrary carriers; the gap hypothesis is supplied, not computed. |
| DP-3 | `lower_bound_le_raw`, `quot_le_raw`, `countermodel_raw`, `countermodel_quot`, `countermodel_zero_tests`, `countermodel_values_differ`, `weighted_countermodel` in `ComponentRepair` | General weak duality from admissibility of `u = 0`; the one-dimensional countermodel and the `(2,3)` weights. |
| DP-4 | `colNorm_ge`, `some_column_ge_four_thirds`, `uniform_column_norm`, `repaired_example_norm`, `example_distance_to_R`, `example_ratio`, `planar_control` in `ComponentRepair` | Rank-one projectors `e aᵀ` on `ℓ¹³` only; operator norm read as maximum column norm (not formalized). |
| DP-5 | `inv_start`, `inv_step`, `inv_iter`, `width_step`, `step_nested`, `width_iter`, `root_in_bracket`, `mid_close`, `negative_endpoint_control`, `table_row1`..`table_row6`, `table_iter6`, `start_two`, `nat_sq_two_descent`, `no_rational_sqrt_two` in `ComponentCompletion` | Rational bisection. Empty rational intersection of the nested brackets needs an Archimedean step that is not formalized. |
| DP-9 | `pauli_relations`, `single_qubit_minus_x`, `single_qubit_plus_x`, `single_qubit_minus_x_not_symmetric`, `sos_identity`, `sos_factors_symmetric`, `chshBs_table`, `bs_quad_le`, `bs_quad_bell`, `deterministic_chsh`, `pr_box_not_deterministic` in `ComponentQuantum` | Integer tables and the quadratic form of `Z⊗Z + X⊗X` on `Rat⁴`; the scale `√2` and the complex expectation `2 + 2i` are not formalized. |
| DP-8 | `choi_transpose_negative`, `choi_transpose_tp`, `leading_minor_trap`, `kraus_h_orthogonal`, `three_copies_complete`, `mod_three_descent` in `ComponentQuantum` | Separating controls only; the PSD/principal-minor/LDL equivalence and Choi–Kraus equivalence are not formalized. |
| DP-7 | `coefficient_relax`, `coefficient_relax_iff`, `coefficient_relax_fails_at_one`, `half_slope_window`, `envelope_monotone`, `vertex_value`, `envelope_relax`, `replay_k2`, `replay_k3`, `sine_enclosure_comparison`, `field_control_square`, `correlated_control_normalization`, `time_dependent_control` in `ComponentQuantum` | Exact envelope algebra and integer controls. Commutator support counting, trace-norm duality, the Taylor remainder and the sine enclosure itself are analytic residuals. |
