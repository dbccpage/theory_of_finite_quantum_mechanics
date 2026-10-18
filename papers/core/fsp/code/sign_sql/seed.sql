-- ============================================================================
-- seed.sql — the actual walk as data.
--
-- AuthorityEffect: None.  Honesty fences:
--   * The toy three-path system below ILLUSTRATES the structure of the sign
--     problem; it does not simulate physics.  Weights are bare rationals, not
--     amplitudes; a declared sign range is a bit-shadow, not a qubit.
--   * priced = 1 rows are PURCHASES the sealed sources do not license.
--     Citing sealed-derivation-v1 @ 3100c4e on a priced row means "citable
--     only as the CONTRAST" (what the pre-purchase world provably lacks).
--   * The Wheeler-DeWitt row (rung 8) is DECLARED, not derived — a boundary
--     object citing the house DeWitt case study (PP/021, PO-021), which
--     itself REFUSES the continuum and works constraint-level only.
--   * Hardness statements are external literature: Cook 1971, Levin 1973,
--     Troyer & Wiese PRL 94, 170201 (2005).  Nothing here proves them.
-- ============================================================================

-- ---------------------------------------------------------------------------
-- The rungs: void (0) -> Troyer-Wiese presentation-dependence (7) -> the
-- Wheeler-DeWitt boundary row (8).  parent_rung_id is the walk itself.
-- ---------------------------------------------------------------------------
INSERT INTO rungs (rung_id, parent_rung_id, name, standing, claim_type, lay_sentence, source) VALUES
(0, NULL, 'void_point', 'licensed', 'PROVEN-MECHANIZED',
 'Before anything is deliberately taken on board, nothing happens and nothing can happen — even writing "this differs from itself" at the lone point is a sentence that changes nothing and proves nothing.',
 'sealed-derivation-v1 @ 3100c4e: lean4/Derivation/Inertia.lean (genesis_underivable, underivable_of_empty, supply_no_op); lean4/Derivation/PrimDiff.lean (selfdiff_consistent, symm_selfdiff_consistent, meta_diff_without_assertion, factors_through_point_iff); code/derivation/model.py (supply is a no-op)'),
(1, 0, 'primitive_difference', 'licensed', 'PROVEN-MECHANIZED (+ 4 OPEN locatedness cells)',
 'The first real thing is a witnessed difference under the rule "nothing differs from itself" — accept both and you have bought exactly two things and an arrow, and merging them back costs you the rule.',
 'sealed-derivation-v1 @ 3100c4e: lean4/Derivation/PrimDiff.lean (irrefl_witness_ne, no_witness_on_subsingleton, D2_initial_pointed, obstruction_under_irrefl); lean4/Derivation/PrimitiveCore.lean (72-cell matrix: 17 implications, 51 countermodels, 4 OPEN)'),
(2, 1, 'separability_observation', 'licensed', 'PROVEN-MECHANIZED + FINITE COMPUTATION',
 'Two things are genuinely different, from the inside, only when some admitted test tells them apart — visibly different things can remain internally identical until such a test is deliberately added.',
 'sealed-derivation-v1 @ 3100c4e: code/derivation/observe.py (contexts, profile, separable); lean4/Derivation/Inertia.lean (collapsed_of_no_insts, R2L_collapsed, R2F_collapsed, admission_without_expressive_increase)'),
(3, 2, 'composition_iteration', 'mixed', 'FINITE COMPUTATION / PROVEN-MECHANIZED (licensed half) + CONDITIONAL (import #1)',
 'Structure grows only the way it began — demand by demand, admission by admission, every state rebuildable from its diary — and "a string of symbols" is not free: gluing marks into sequences is itself a purchase.',
 'sealed-derivation-v1 @ 3100c4e: code/derivation/candidates.py (min_responses), iso.py (canonical), model.py (replay); import #1 must be proved fresh or stated CONDITIONAL'),
(4, 3, 'universal_machine', 'priced', 'CONDITIONAL on imports #1-#5 + external literature',
 'A computer is not found at the bottom of the walk — it is bought, in five named installments: symbols it can tell apart, endless room, a notion of next-to, permission to move itself, and one machine that imitates all the others.',
 'fresh proof or external literature (Turing 1936 universal machine); sealed-derivation-v1 @ 3100c4e citable ONLY as contrast (supply_no_op for externality of change; finite bounds; Challenge-2 opacity)'),
(5, 4, 'np_hardness_search', 'external', 'external literature (Cook-Levin) + OPEN-or-fresh for native hardness',
 'Hard problems are the ordinary situation of this walk scaled up — checking one admitted answer is easy, while hunting through the space of possible admissions is what costs.',
 'external literature: Cook 1971, Levin 1973; sealed-derivation-v1 @ 3100c4e code/derivation/candidates.py + iso.py citable as the finite, licensed prototype of presentation-search'),
(6, 5, 'signed_sums_cancellation', 'priced', 'fresh bridge lemma + import #6 + external literature (Troyer-Wiese)',
 'Adding things up is an act of forgetting — and when the things carry signs, the forgetting is vicious, because huge crowds of paths can cancel to a whisper that no amount of fair sampling of the crowd can hear.',
 'sealed-derivation-v1 @ 3100c4e: lean4/Derivation/PrimDiff.lean (Push, CollapseCollision, FidelityObstruction — the collapse grammar, cited as ancestor ONLY); hardness: Troyer & Wiese PRL 94, 170201 (2005), external literature'),
(7, 6, 'sign_problem_presentation_dependence', 'mixed', 'CONDITIONAL/positioning (fresh toy theorem recommended) + external literature',
 'Whether a sum "has minus signs in it" is a fact about how you wrote the sum, not about what the sum equals — mistaking the first for the second is the same error as thinking two things differ because their names do.',
 'sealed-derivation-v1 @ 3100c4e: code/derivation/iso.py (canonical forgets presentation tokens) + prompt/seed_prompt.md section 6 (presentation identity vs internal identity discipline); Troyer & Wiese PRL 94, 170201 (2005) for physics-scale statements'),
(8, 7, 'wheeler_dewitt_boundary', 'declared_boundary', 'DECLARED (not derived); cites FRONTIER CASE STUDY PP/021',
 'The Wheeler-DeWitt equation enters this walk as a declared boundary row, not a derived rung: constraint-level problem mathematics, not root ontology — the quotient exists, and that never buys a canonical section (quotient descent, choice of representative, and orthogonal splitting are three different purchases).',
 'DECLARED here, citing PP/021_dewitt_superspace_case_study (PO-021): DeWitt supermetric indefinite per point, canonical orthogonal projection fails globally; continuum superspace REFUSED there; DeWitt Phys. Rev. 160, 1113 (1967); Giulini arXiv:0902.3923');

-- ---------------------------------------------------------------------------
-- Carriers per rung.  NULL size = unbounded or refused.
-- ---------------------------------------------------------------------------
INSERT INTO carriers (carrier_id, rung_id, name, size, description) VALUES
(1, 0, 'one_point', 1,
 'The lone point.  Can consistently host a self-difference assertion (selfdiff_consistent) and that assertion buys nothing: factoring through this carrier is exactly identity (factors_through_point_iff).'),
(2, 1, 'oriented_two_point', 2,
 'Two points and one arrow — initial among pointed witnessed structures (D2_initial_pointed).  Minimal but not the only home: witnessed irreflexive structures exist on every carrier of size >= 2.'),
(3, 2, 'admitted_data_pool', NULL,
 'The admitted data of a regime, distinguishable only by profile — the object language never sees token identity.  Size varies with the admission history; unbounded here means "not fixed", not "infinite".'),
(4, 6, 'toy_path_space', 3,
 'The three paths of the toy signed-sum system.  ILLUSTRATION ONLY: a finite stand-in for a path ensemble; not a physical configuration space.'),
(5, 8, 'superspace_riem_mod_diff', NULL,
 'REFUSED as a carrier: the continuum superspace of PP/021 is a declared boundary object; the case study itself refuses continuum fundamentalism and works on finite toys.  This row exists so the refusal is a row, not an omission.');

-- ---------------------------------------------------------------------------
-- Admissions with the priced/derived flag.  THE PRICE LIST IS THIS TABLE.
-- priced = 0: licensed by sealed-derivation-v1 @ 3100c4e.
-- priced = 1: a purchase (imports #1..#6; the asymptotic frame).
-- ---------------------------------------------------------------------------
INSERT INTO admissions (admission_id, rung_id, name, kind, priced, price_tag, source, description) VALUES
-- rung 1: the first witnessed difference (all licensed)
(1, 1, 'binary_relation_symbol', 'relation', 0, NULL,
 'sealed-derivation-v1 @ 3100c4e: lean4/Derivation/PrimDiff.lean',
 'One binary relation symbol r — the difference vocabulary itself.'),
(2, 1, 'witnessed_instance', 'instance', 0, NULL,
 'sealed-derivation-v1 @ 3100c4e: lean4/Derivation/PrimDiff.lean (irrefl_witness_ne)',
 'A concrete asserted instance r a b — a difference someone has actually pointed at, not merely the possibility of one.'),
(3, 1, 'irreflexivity_law', 'law', 0, NULL,
 'sealed-derivation-v1 @ 3100c4e: lean4/Derivation/PrimDiff.lean (no_witness_on_subsingleton)',
 'The law that nothing differs from itself.  This is the purchase that makes difference cost something: with it, a witnessed pair forces distinctness and a two-element carrier.'),
-- rung 2: separability and observation (all licensed)
(4, 2, 'judgment_forms', 'form', 0, NULL,
 'sealed-derivation-v1 @ 3100c4e: code/derivation/observe.py',
 'Slot patterns of fixed arity — the shapes of admissible tests.'),
(5, 2, 'judgment_instances', 'instance', 0, NULL,
 'sealed-derivation-v1 @ 3100c4e: code/derivation/observe.py',
 'Forms with slots filled by admitted data — actual admitted judgments.'),
(6, 2, 'profile_separability_definition', 'definition', 0, NULL,
 'sealed-derivation-v1 @ 3100c4e: code/derivation/observe.py (profile, separable)',
 'The declared meaning of internal separability: two data differ from inside exactly when their context-profiles differ.'),
(7, 2, 'impose_separation_requirement', 'external_event', 0, NULL,
 'sealed-derivation-v1 @ 3100c4e: code/derivation/model.py (Impose)',
 'The external act of DEMANDING a separation — a demand, not a solution.'),
-- rung 3: composition and iteration (licensed core + priced import #1)
(8, 3, 'demand_respond_admit_loop', 'iteration', 0, NULL,
 'sealed-derivation-v1 @ 3100c4e: code/derivation/model.py (replay), engine',
 'The repeated game: demand, enumerate responses, admit one, replay from genesis.'),
(9, 3, 'candidate_space_and_costs', 'enumeration', 0, NULL,
 'sealed-derivation-v1 @ 3100c4e: code/derivation/candidates.py (min_responses, Bounds)',
 'A declared finite space of one-step augmentations with two declared cost measures; minima enumerated exhaustively, ties retained.'),
(10, 3, 'isomorphism_quotient', 'quotient', 0, NULL,
 'sealed-derivation-v1 @ 3100c4e: code/derivation/iso.py (canonical, cross-checked against brute force)',
 'The implemented relation under which branches may be identified — it deliberately forgets presentation tokens.'),
(11, 3, 'internal_composition_adjacency', 'operation', 1, '#1',
 'PRICED: fresh proof or CONDITIONAL.  Sealed Challenge-2 opacity is the citable contrast: concatenation, substrings, glyph identity, order, multiplicity are never licensed there.',
 'Gluing marks into sequences: an internal successor/adjacency relation and an internal composition operation.  The walk''s first purchase.'),
-- rung 4: the universal machine (all priced)
(12, 4, 'internal_token_identity', 'alphabet', 1, '#2',
 'PRICED: fresh.  Sealed rung-2 machinery prices what it costs to fake symbol equality with profiles; the admission itself is new.',
 'A finite alphabet whose members the process can compare for equality — a machine that reads a symbol needs decidable internal equality on symbols.'),
(13, 4, 'unbounded_workspace', 'resource', 1, '#3',
 'PRICED: fresh commitment.  The sealed derivation is finite everywhere, with declared bounds and exported frontiers.',
 'An inexhaustible supply of fresh cells.  Unboundedness is a genuinely new commitment, not a limit of the old ones.'),
(14, 4, 'self_driven_transition', 'authority', 1, '#4',
 'PRICED: fresh, and directly against the sealed external-events-only invariant (model.py step; supply_no_op).  Must be named loudly.',
 'Permission for the process to issue its own admission events according to an admitted finite rule table — a machine''s transition function is precisely this license.'),
(15, 4, 'universality', 'machine', 1, '#5',
 'PRICED: external literature (Turing 1936 and standard constructions) or fresh small-UTM proof.  Not derivable from the sealed sources.',
 'One admitted machine that simulates every machine when handed a description; needs encoding (imports #1-#3) plus an interpretation theorem.'),
-- rung 5: the asymptotic frame (priced, un-numbered: rides on #3-#5)
(16, 5, 'asymptotic_frame', 'frame', 1, NULL,
 'PRICED (rides on imports #3-#5); hardness anchor is external literature: Cook 1971, Levin 1973.  No hardness claim may be back-attributed to the sealed finite instance (max 2 items, arity <= 2 — trivially finite).',
 'Families of instances indexed by size, so that "polynomial" and "exponential" are sayable.  Complexity classes, reductions, and asymptotics all live here.'),
-- rung 6: signed arithmetic and the sum-observation (priced import #6)
(17, 6, 'signed_arithmetic_and_sum_observation', 'arithmetic', 1, '#6',
 'PRICED: fresh admission.  The sealed collapse grammar (PrimDiff.lean) prices what summation forgets but does not supply numbers, negatives, or cancellation.',
 'Numbers as weights on paths, and SUMMATION as an observation — a collapse map from many paths to one total.  With signs, distinct path-sets can produce the same total by cancellation; the gross (L1) and net (signed) observations come apart.');
-- rung 7 admits nothing new: it is a reclassification (non-negativity moves
-- from the object column to the presentation column).  rung 8 admits nothing:
-- it is a declared boundary row, not an admission on the walk.

-- ---------------------------------------------------------------------------
-- Observers: the two aggregations the queries perform.
-- ---------------------------------------------------------------------------
INSERT INTO observers (observer_id, name, kind, description) VALUES
(1, 'net_signed_sum', 'signed_sum',
 'The partition-sum observation: SUM of signed weights.  Many-to-one; forgets path identity entirely — the fibers of this map are the cancelling path-sets.  This is the observation a downstream reader actually receives.'),
(2, 'gross_l1_mass', 'l1_sum',
 'The L1 observation: SUM of absolute weights — total magnitude of activity.  A DIFFERENT observation of the same rows; the ratio net/gross is the sign-problem severity, and sampling the gross to estimate the net pays that ratio.');

-- ---------------------------------------------------------------------------
-- The toy signed-sum system: 3 paths, 2 presentations of ONE system.
-- ILLUSTRATION ONLY — this is the structure of the sign problem, not physics.
--
-- Presentation A (frustrated basis): weights 1/2, 7/2, -7/2.
--   net = 1/2, gross L1 = 15/2, severity |net|/gross = 1/15.
-- Presentation B (meron-style re-presentation): weights 1/2, 0/2, 0/2.
--   The cancelling pair (p2, p3) is discharged by a sign-inverting,
--   weight-preserving involution pairing p2 <-> p3 (the meron-cluster move of
--   Chandrasekharan-Wiese 1999, cited as external literature); the surviving
--   zero-meron cluster carries the whole net weight.  net = 1/2, L1 = 1/2,
--   severity = 1.  All weights non-negative.
-- Same net total in both — the re-presentation changed the writing, not the
-- thing written.  Fence: B keeps the SAME path labels for comparability; in a
-- genuine meron-cluster move the carrier itself is re-clustered, and that
-- re-clustering is a purchase (an admitted witness), not a free relabeling.
-- ---------------------------------------------------------------------------
INSERT INTO systems (system_id, name, description) VALUES
(1, 'toy_three_path_signed_sum',
 'A three-path signed-sum object.  ILLUSTRATES sign-problem structure (cancellation vs re-presentation); does NOT simulate physics.  Weights are bare rationals, not amplitudes; the sign range is a bit-shadow, not a qubit.');

INSERT INTO paths (path_id, system_id, label, description) VALUES
(1, 1, 'p1_zero_meron_cluster', 'The surviving configuration: carries the entire net weight in both presentations.'),
(2, 1, 'p2_meron_plus',  'One half of the cancelling pair: large positive weight in the frustrated basis.'),
(3, 1, 'p3_meron_minus', 'The other half: equal magnitude, opposite sign — the involution partner of p2.');

INSERT INTO presentations (presentation_id, system_id, label, basis_note, description) VALUES
(1, 1, 'A_frustrated',
 'Naive path basis: signs frustrated, cancellation live between p2 and p3.',
 'The presentation in which the sign problem is visible: gross mass 15/2 collapses to net 1/2.'),
(2, 1, 'B_meron_repaired',
 'Meron-style re-presentation: the sign-inverting, weight-preserving involution p2 <-> p3 discharges the cancelling pair; net weight sits on the zero-meron cluster p1.  Witness is an admitted object, not cohomology alone.',
 'The presentation in which the same system is sign-free.  Same net total as A; the sign problem was a property of presentation A, not of the system.');

-- Weights: common denominator 2 in every presentation (the in-query exactness
-- guard COUNT(DISTINCT den) = 1 depends on seeds honoring this).
INSERT INTO path_weights (path_id, presentation_id, num, den) VALUES
-- Presentation A (frustrated): 1/2, 7/2, -7/2
(1, 1,  1, 2),
(2, 1,  7, 2),
(3, 1, -7, 2),
-- Presentation B (meron-repaired): 1/2, 0/2, 0/2 — all non-negative
(1, 2,  1, 2),
(2, 2,  0, 2),
(3, 2,  0, 2);

-- ---------------------------------------------------------------------------
-- Obstructions: what blocks the naive continuation at each rung.
-- ---------------------------------------------------------------------------
INSERT INTO obstructions (obstruction_id, rung_id, obstruction_type, name, description, terminal, source) VALUES
(1, 0, 'inertia', 'genesis_inertia',
 'Nothing is derivable at genesis, nothing is derivable in any empty-rule state, and showing the process a new inscription changes its state not at all.  The void does not continue by itself.',
 'full stop until something is deliberately admitted',
 'sealed-derivation-v1 @ 3100c4e: Inertia.lean (genesis_underivable, underivable_of_empty, supply_no_op)'),
(2, 1, 'collision', 'collapse_collision',
 'Merging the two endpoints of a witnessed pair always produces a self-relating point; under the protected irreflexivity law that collision is an obstruction.  Without the protected law, collapse is admissible and the difference silently dies.',
 'collapse refused while irreflexivity is protected; otherwise silent loss',
 'sealed-derivation-v1 @ 3100c4e: PrimDiff.lean (obstruction_under_irrefl, collision_not_irrefl, bare_collapse_admissible)'),
(3, 2, 'collapse', 'observational_collapse',
 'Externally different admitted data can stay internally identical: after admitting two visibly different marks, the pair is still collapsed under both admission readings.  Admission does not necessarily increase expressive power.',
 'internal indistinguishability persists until a separating test is admitted',
 'sealed-derivation-v1 @ 3100c4e: Inertia.lean (R2L_collapsed, R2F_collapsed, admission_without_expressive_increase)'),
(4, 3, 'unlicensed_structure', 'string_smuggle_block',
 'Concatenation, substrings, glyph identity, order, and multiplicity are never licensed by the sealed sources; a walk that wants sequences must buy import #1 openly.',
 'loud stop: purchase (#1) required before sequences exist',
 'sealed-derivation-v1 @ 3100c4e: prompt/seed_prompt.md Challenge 2 (opacity of <ab>)'),
(5, 4, 'authority', 'external_events_only',
 'In the sealed model every state change is caused by an external event; the process never authors its own admissions.  A transition function is a new authority and must be admitted as one (#4).',
 'loud stop: self-driven change requires the priced authority admission',
 'sealed-derivation-v1 @ 3100c4e: model.py (step is the only mutator), Inertia.lean (supply_no_op)'),
(6, 5, 'complexity', 'search_over_presentations',
 'Verification of one admitted presentation is cheap; search over the space of presentations is the expensive act.  The canonical hardness anchor is external literature; any hardness claim about the walk''s own objects is a fresh theorem or an OPEN.',
 'no polynomial search guarantee; hardness cited, never derived here',
 'external literature: Cook 1971, Levin 1973; sealed candidates.py/iso.py as the finite licensed prototype'),
(7, 6, 'cancellation', 'signed_sum_cancellation',
 'A signed sum is a collapse map whose fibers are the cancelling path-sets.  Two ensembles can agree in gross (L1) mass and cancel to a whisper in net; any procedure that estimates the net by sampling the gross pays the ratio.  Generic stochastic curing is NP-hard.',
 'exponential estimator cost in the frustrated presentation; hardness external (Troyer-Wiese)',
 'external literature: Troyer & Wiese PRL 94, 170201 (2005); sealed PrimDiff.lean collapse grammar as ancestor vocabulary only'),
(8, 7, 'misclassification', 'presentation_object_conflation',
 'Treating "this model has no sign problem" as a property of the model rather than of the model-plus-basis conflates presentation identity with internal identity — exactly the conflation the sealed discipline forbids.  Non-negativity is not isomorphism-invariant data of the computed quantity.',
 'diagnosis: reclassify non-negativity to the presentation column; no theorem claimed without a fresh proof',
 'sealed-derivation-v1 @ 3100c4e: iso.py (canonical forgets presentation tokens); prompt/seed_prompt.md section 6'),
(9, 8, 'no_section', 'quotient_without_canonical_section',
 'The quotient exists, and that never buys a canonical section or retraction: the DeWitt supermetric is indefinite per point, so horizontal/vertical directions can intersect null vectors and canonical orthogonal projection fails globally.  Quotient descent, choice of representative, and orthogonal splitting are three different purchases.',
 'boundary: declared constraint-level row; continuum REFUSED; walk ends here',
 'PP/021_dewitt_superspace_case_study (PO-021); DeWitt Phys. Rev. 160, 1113 (1967); Giulini arXiv:0902.3923');
