# MUB(6) claim ledger

AuthorityEffect: None.
Checkpoint: 2026-10-10. Classification and concrete semantic bridges remain open.

## Evidence boundary

The current package supports finite exact calculations and conditional Lean
statements. It does not establish `NoCompleteMUB6`, `MUB(6)=3`, or `MUB(6)<=3`
for concrete complex Hilbert bases without the remaining premises below.
A standard-axiom audit checks logical dependencies; it does not discharge arguments.

## Frontier gaps

The IDs G1-G5 here are planning IDs, distinct from the G1/G2/G3 predicates in
`Gluing.lean`. Each entry has the required four-part envelope.

| Gap | Status | Supported statement | Excluded interpretation | Narrow claim | Next required evidence |
|---|---|---|---|---|---|
| G1: full moduli classification | OPEN | Classification interfaces and finite parity/table lemmas exist. | No exhaustive classification of complex 6 by 6 Hadamard matrices. | `FullModuliClassification` still needs `FiveBranchRealizationHypothesis`; R6 and R7 remain `NOT_A_CERTIFICATE`. | A concrete exhaustive family/reconstruction argument, or an independently established alternative landing theorem. |
| G2: candidate representation | CONDITIONAL | `CurvatureWallCertifiedAtlas` and ZeroRel implications apply to supplied wall/representation data. | Catalog labels and fixed Gram matrices are not all candidate bases. | Results retain the actual representation, membership, and positivity arguments in their types. | A candidate-to-matrix map preserving the concrete MU equations and PSD. |
| G3: analytic parameter bounds | PARTIAL | Declared endpoint interpolations and scoped interval calculations. | No derivative bound over the full CHM moduli space. | Convex combinations of positive endpoint numbers stay positive. | Matrix-dependent rigorous derivative/remainder estimates, including singular collars. |
| G4: geometric cochains | CONDITIONAL | Exact circulation on a declared finite nerve and coboundary identities. | No derivation of that nerve or its weights from all complex charts. | Gauge invariance holds on the supplied complex. | Checked chart intersections, orientation and weights, with coverage. |
| G5: projector moments | OPEN; real positive-flat coordinate bridge checked | Normalized positive flat real coordinate moments with finite compatibility for all 180 residuals extract an actual unitary fourth-basis candidate. Actual solutions give rank-one evaluation moments. | No variety emptiness, positivity exclusion for arbitrary nonflat truncations, or full moduli exclusion. The separate noncommutative word route retains its dimension/rank-one/MU limits. | Commuting symmetric coordinate operators and a common real zero are constructed. Candidate existence is equivalent to existence of normalized positive flat compatible coordinate moments. Empty variety excludes positivity under those exact premises. | Establish the needed empty varieties and parameterized-family coverage; justify any use of the flat moment condition for proposed data. |

## Route C

- Supported: `fourier_count_ge_five`, `fourier_pairs_ge_ten`, and
  `fourier_landing_edges_lower_bound` are arithmetic consequences of a supplied
  `MUB6OrbitConfiguration`.
- Excluded: the structure contains no matrices or transition-edge membership
  map. The numerical expression `n_dita + pairCombinations n_dita >= 15` does
  not identify 15 actual Fourier transitions.
- Narrow claim: `no_complete_mub6_via_route_c` takes
  `h_landing : CompleteMUB6 -> RouteCCompleteMUBFamily`. The new
  `no_complete_mub6_of_fourier_triple_landing` needs a constituent triple with
  `InFourierDitaChart`, without the orbit-count fields.
- Next evidence: derive that certified membership from concrete complex MU
  data. `InFourierDitaChart` already carries analytic soundness through
  `CertifiedPointInGlobalDomain`; geometry alone is insufficient.

## Conjecture 2 and R6

`Conjecture2GeneralMechanization.lean` is tracked and contains integer parity,
anti-parallel cancellation, Tao phase-table evaluation, and a declared finite
class table. Its `AnalyticCubeSliceCertificate` supplies the row bound and
class/table compatibility as fields. The module is present; the old
artifact-missing description is stale. General matrix Conjecture 2 and the
matrix interpretation of Proposition 4.2 remain unestablished by this module.

The R6 receipt has raw SHA-256
`cf8442d8fe1397226d669fcea7bc038ef8d984a9bae741772b9d742fbe62eb59`
and status `NOT_A_CERTIFICATE`. Hash identity does not change that status.
The Matolcsi receipt has raw SHA-256
`598d73b4f7b6807d62fc8d5c7698fd7c00ca73634c24641e0f2a848c873fc6fa`.
Its internal digest is a separate field, not the file digest.

## Honesty addendum 2026-10-21: legacy receipts that are not certificates

No claim above is weakened. The following legacy receipts and modules are relabelled
`NOT_A_CERTIFICATE`, with the reason, in the receipts themselves
(`artifacts/*.json`, key `certificate_status`) and in `artifacts/manifest.json`.

| Receipt or module | Status | Reason |
|:---|:---|:---|
| `artifacts/mub6_szollosi_t5_cover_receipt.json`; `code/rust/src/mub/native/mub6_szollosi_t5_cover.rs` (the "T5 cover") | `NOT_A_CERTIFICATE: evaluates known roots only; no cover` | It evaluates only the 120 known root boxes loaded from `special_replay.json`; `excluded_leaves` is 0 and no complement leaf exists. `verified_sound` is the literal `true` in each receipt constructor. The dimension-3 control compares the literal `3 == 3`. The tests return silently when the replay file is missing. The 1e-10 radius cover uses an asserted sensitivity constant (8000). Only the exact interval pair-gap over the 120 boxes is genuine. Ray completeness at p0 is open. |
| `artifacts/mub_target_a10_global_cover_receipt.json` (28-cell A10 tree: F6 4, B6 8, S6 4, collar 4, Karlsson exterior 4, H6 4) | `NOT_A_CERTIFICATE` | The margins 37249/90000, 12133/30000 and 527/576 are literals. The deltoid-cover candidate box forces \|U00\|^2 >= 81/100 whereas every basis unbiased to the identity has \|U00\|^2 = 1/6, so the box contains no candidate (DAG `MUB6-DELTOID-COVER-BOX-DEFECT`). `certified:true` is a stored flag. |
| `artifacts/mub_target_a12_smale_sentry_receipt.json`; `TargetA12SmaleSentry.lean` `canonicalCell56` (56 cells) | `NOT_A_CERTIFICATE` | The 56 cells are scalar intervals [i/56,(i+1)/56] of one label with a stored depth constant 64; they do not cover the two-parameter Szollosi family. No per-cell boxes, Jacobians or Krawczyk images exist. `HasCurvatureCertificate` is a supplied premise. Conjecture 3 is OPEN. The receipt itself scans 28 cells. |
| `artifacts/mub_target_a2_deltoid_cusp_receipt.json` (A2 cusp blow-up, 24 leaf cells) | `NOT_A_CERTIFICATE` | Literal margins, formal angle labels and stored flags; no blow-up chart or collar data. |
| `artifacts/mub_target_a8_collar_boundary_receipt.json` (A1/A8 collar cover) | `NOT_A_CERTIFICATE` | Literal margins and stored flags. |
| `artifacts/mub_karlsson_volume_cover.json` | Not edited (the file carries its own internal digest). Treat as `NOT_A_CERTIFICATE`. | The minimum of the 104 stored per-box gaps equals the literal 37249/90000, `min_triad_defect_gap` is 0, and the margins are the same fixture literals. |
| `checkPartitionCover_sound` (`TargetA5FiniteCover.lean:237`) | Narrow | It quantifies only over rational points `x : Fin 5 -> Rat`, so it is not a cover of a real parameter domain. |

What does stand: the Lean soundness lemmas (`RectangularQuadraticExclusion`, `SparseRectangularExclusion`,
`SzollosiIntervalExclusion`, `MubQuadraticTransitionSeparation.close_columns_box_excluded`) are unchanged,
as is the general reduction chain to the 386/320-coordinate quadratic system.

## Conjecture 3 / 56-cell sentry

- Supported: positive stored rational margins and conditional implications in
  `TargetA12SmaleSentry.lean`.
- Excluded: the integer label `depth = 64` is not a subdivision computation;
  no 56-cell numerical replay follows from constructing that label.
- Narrow claim: `certified_point_in_cover56_iff` states that certified
  membership is geometric membership plus `HasCurvatureCertificate pt.triple`.
- Next evidence: actual rational domains, interval Jacobians, coverage of the
  continuous family and three cusp collars, per-cell Krawczyk exclusion bounds,
  and their soundness bridge into the concrete MU equations.

The square-quadratic contractor is the library at
`src/omega_native/mub6_smale_sentry.rs`. The new same-named `src/bin/` inspector
accepts `--inspect-system`; it does not supply the requested depth-64 run. The terminal receipt contains
aggregate counts and margins, with no per-cell bounding boxes or Krawczyk images.
Its current `CERTIFICATE` label has not been renewed by an independent full replay.
Strict Krawczyk inclusion is a root-existence condition; exclusion requires
Krawczyk disjointness or another justified infeasibility bound.

`SmalePointCertificate` and `KrawczykContractor` already contain root and
uniqueness evidence. Their existence lemmas project those fields. An analytic
root theorem is not obtained from the stored inclusion field alone.

The deltoid-cover implementation uses a candidate box with
`|U[0,0]|^2 >= 81/100`. Its margin `37249/90000` comes from the standard-basis
residual alone. An unbiased candidate has `|U[0,0]|^2 = 1/6` and lies outside
this box. Family-parameter coverage does not establish candidate coverage.

The continuous two-circulant construction is now checked in
`SzollosiTwoCirculant.lean`: unit phases and one complex compatibility equation
yield the actual Gram identity, normalized unitarity and one-sixth entry moduli.
The six real parameter equations cover every preimage in the two phase-sum
images, lie in the rational unit box, and retain boundary/repeated-root points.
This is a construction, without classification or dephased equivalence transport.

`SzollosiQuartetSystem.lean` checks the equivalence between actual quadruplets
with the identity and the family matrix as the first two bases and candidate
equations with both additional bases arbitrary. All 144 candidate coordinates
are retained. Standard-basis unbiasedness bounds each coordinate by one half.
The empty-variety obligation ranges over every admissible third basis; selecting
one Zauner triplet does not meet that obligation.

Joint rational specification envelope (`SzollosiQuadraticSystem.lean`):

- Supported claim: 618 rational equations in 440 real variables have total degree
  at most two. Actual quartets and equation solutions correspond in both directions,
  also at each fixed admissible phase parameter; both additional bases are arbitrary.
- Evidence: `equation_degree`, `exists_solution_with_parameters_iff`,
  `exists_solution_iff_quartet`, `solution_in_full_box` and
  `exists_bounded_solution_iff_quartet`, under the package build and transitive
  axiom audit bound in `mub_option_b_checkpoint_receipt.json`.
- Conditions: the identity and the constructed normalized block-family matrix
  are the first two bases. Raw matrices scale by sqrt 6; auxiliary cross-product
  entry norms squared equal six. The rational containing box has radius one for
  phase/raw-basis coordinates and three for cross-product coordinates.
- Remaining obligation: establish the real solution set empty. The executable
  expression export and native full-box inspection below now exist. Generic
  runtime/decoder qualification for later inputs and further equivalence
  transport, complete parameter/candidate cover, cusp analysis and the requested
  complete reflected exclusion remain open.

Rectangular quadratic exclusion envelope (`RectangularQuadraticExclusion.lean`,
`SzollosiRectangularExclusion.lean`):

- Supported claim: the exact midpoint secant identity and sound derivative
  intervals enclose every zero in the rational rectangular image. Strict
  coordinate separation excludes zeros. The actual quartet coefficient shape
  and polynomial semantics are derived from the checked table, retaining all
  618 equations and 440 coordinates.
- Evidence: `list_derivative_polynomial`, `list_secant_identity`, `root_in_image`,
  `exclusion_sound`, `rows_shape`, `derivative_enclosed`,
  `no_solution_in_box_of_check` and `no_quartet_of_check`. Kernel examples check
  exclusion beyond residual intervals, retained endpoint contact and failure of
  overdetermined root inference from strict inclusion alone.
- Conditions: finite quadratic terms with valid coordinate indices, an actual
  containing box, a center in that box and the actual successful separation
  Boolean. The rational preconditioner is arbitrary; invertibility is not an input.
- Remaining obligation: useful preconditioners, complete parameter/candidate
  leaves and cusp collars, coverage and successful checks. No actual
  quartet-domain exclusion or complete curvature certificate is supplied.

Column-gauge reduction envelope (`SzollosiColumnGauge.lean`):

- Supported statement: for each admissible family parameter, quartet existence
  is equivalent to a solution of all 618 equations in the explicit gauge box.
  The two arbitrary additional bases are retained up to independent column phases.
- Excluded interpretation: original matrices need not have first rows equal to
  one. This is an existence-preserving representative reduction, without a
  classification or family-matrix dephasing theorem.
- Narrow claim: the reduction prescribes 24 real wire coordinates, with their
  ordered IDs and values checked by `gaugePointCodes_checked` using `by rfl`.
  `gauge_box_firstRow` derives the equalities from actual point bounds.
- Remaining obligation: useful further contraction, full parameter/candidate
  coverage, actual cell/cusp exclusions and the curvature bridge. The new native
  gauge-box replay is unresolved and its output images are not kernel-reflected.

Current native rectangular data envelope (`SparseRectangularExclusion.lean`,
`SzollosiRectangularReflection.lean`):

- Supported claim: all 618 sparse Jacobian rows (9,000 entries), 440 images and
  intersections match sound actual-system semantics. Every actual solution is
  retained. Exactly 24 coordinates of the constructed family matrix contract; none separates. The 144 raw coordinates of the additional bases are unchanged.
- Evidence: `native_jacobian_eq`, `native_jacobian_entry_enclosed`,
  `native_images_eq`, `solution_in_native_retained`,
  `native_contracted_coordinates_checked`, `native_images_have_no_separation`
  and `mub_szollosi_rectangular_native_receipt.json`, bound by the checkpoint.
- Conditions: this exact full containing box, zero center, actual coefficient
  table and 28-entry rational preconditioner. Kernel reduction checks the emitted
  data; generic Rust/JSON implementation verification is not a consequence.
- Remaining obligation: successful quartet-domain separation, useful further
  contraction/subdivision, further transport, complete 56-cell/cusp coverage and
  actual curvature. Status is `CONTRACTED_UNRESOLVED_BOX`; no root is obtained.

Executable and interval envelope (`SzollosiExecutableSystem.lean`,
`SzollosiIntervalExclusion.lean`):

- Supported claim: every executable expression represents its checked rational
  polynomial for all real assignments. Ordered IDs cover every coordinate and
  equation. Rational AST interval evaluation encloses those values, and a
  successful zero-exclusion check excludes actual zeros in that box. Every current
  emitted coefficient row is identified with its actual polynomial for all real
  assignments; every emitted native interval encloses those values for assignments
  in the full containing box.
- Evidence: `expression_polynomial`, `equation_eval`, `variable_codes`,
  `equation_codes`, `equation_enclosed`, `exclusion_check_sound`,
  `normalized_equation_polynomial`, `native_coefficients_polynomial`,
  `native_interval_enclosed` and the current package build/axiom audit. The exported input has raw SHA-256
  `1367d390da36e5ccf65abbc8fbf529ff07f9e154c277bb14c1cd8c36ba24c947`.
- Conditions: a successful exclusion check and actual containment are required.
  The native sparse compiler matched 1,854 rational probe values, which is finite
  evidence. The current emitted tables have the stronger identity and enclosure
  semantics recorded below. Generic compiler/decoder verification remains open.

`SzollosiTermExpansion.lean` derives complete sparse normalization semantics.
The native inspector now compares all 618 rows and 5,128 nonzero terms against
the independently exported Lean coefficient table, raw SHA-256
`44656965bb72e735febfc69c1bcd599adbeea2e8512ebd6141025f8524e5d2df`.
`SzollosiNativeReflection.lean` checks the actual emitted coefficient table by
kernel reduction (`native_terms_match`); `native_coefficients_polynomial`
identifies every row with the actual rational polynomial under injective coding.
`SzollosiNativeInterval.lean` derives sparse interval enclosure with square
refinement and ordered accumulation. Kernel reduction checks all 618 actual
emitted intervals (`native_ranges_match`); `native_interval_enclosed` binds
each to all actual real assignments in the full containing box. The native
receipt raw SHA-256 is
`17b31a7eec56d0129b0b4b8a837f55d71b37ee0be0d0a91ad6fbb106949633dc`.
These identities concern the current emitted data, without generic verification
of every Rust compiler or JSON decoder input. Every emitted interval still
contains zero (`native_full_box_unresolved`). No variety emptiness or root
existence follows. Coefficient and interval literal mutations are rejected by
their kernel checks; a quadratic perturbation invisible to all three old probes
is rejected by the complete native coefficient comparison.
- Remaining obligation: both full-box checks are unresolved; the Lean Boolean
  reduces to false. `phase_interior_excluded` is a kernel-reduced off-domain example
  containing no admissible unit phase. The native receipt records
  `UNRESOLVED_FULL_BOX`, all 618 residual intervals, no Krawczyk run and no full
  56-cell/cusp calculation. These results supply no quartet-variety emptiness.

## Moment bridge

`CurtoFialkowFlatExtension` supplies rank labels, operators, a normalized state,
self-adjointness, idempotence, and orthogonality. `gns_extraction_theorem`
repackages those supplied operators. It does not derive them from `M2` and `M1`.
`sound_universal_exclusion_via_rank_loop` also takes `h_gns_exhaust`.
The emptiness variants take `h_sound`, `h_contra`, or physical nonnegative/negative
trace hypotheses. These arguments remain required.

`rationalMomentMatrix`, `MomentPrincipalEmbedding`, and
`FlatMomentRankCondition` now bind the proposed rank equality to actual rational
word-moment matrices with complete, nonduplicate word indexing. The
principal-submatrix identity and rank monotonicity are
formal consequences of the supplied embedding. The equality, positivity,
MUB-relation compatibility, and extraction remain separate obligations.

`zeroActionInterfaceModel` inhabits `PhysicalProjectorRealization numBases dim Bool`
for arbitrary size labels. The current structure lacks completeness, rank-one,
concrete dimension, inner-product linearity, and cross-basis MU constraints.
The checked theorem `not_universal_interface_exclusion` has no axiom dependencies.
This is a countermodel to the interface, not a concrete MUB configuration.

`ConcreteMubProjectors.lean` now constructs actual complex rank-one projector
matrices from `FiniteComplexMubFamily ι B ι`. Self-adjointness, same-basis products,
completeness, trace one, rank one and the MU cross-trace equation are checked
with standard axiom dependencies. This is a forward construction from a supplied
complex family. It does not establish that family or perform GNS extraction.

`ConcreteMubMoments.lean` constructs the corresponding complex word functional.
For a state from one supplied basis and a distinct MU basis, its complete,
nonduplicate degree-one/two word lists give positive semidefinite Gram moment
matrices, an actual principal inclusion, and ranks equal to the coordinate
cardinality. `concrete_mub_moment_flatness` derives the rank equality. The exact
premises are the supplied `FiniteComplexMubFamily`, labels `b₀`, `b₁`, `l₀`, and
`b₁ ≠ b₀`; no rank equality is an input. This forward result does not extract
operators from arbitrary positive flat data.

`ConcreteMubPolynomials.lean` gives 108 actual MU polynomials over 72 real
candidate coordinates, together with 72 real/imaginary orthonormality residuals.
The coordinate encoding/decoding, exact evaluations, polynomial ideal and
real-zero-set/fourth-basis equivalence are checked. Each MU residual agrees with
the actual complex projector cross-trace minus one sixth. A supplied complete
family gives a zero-set point for its first three bases. This does not supply
emptiness, interval certificates for a parameterized family, or extraction from
arbitrary positive flat moment data.

`FlatMomentProjectorExtraction.lean` now constructs a finite reverse word
representation from `L [] = 1`, a positive semidefinite `wordMomentTwo L`, actual
rank equality with `wordMomentOne L`, and `ContextualProjection L g` for every
generator. These contextual equations state idempotence inside all lower-word
contexts. `extract_word_projectors` outputs a Gram factor, common range,
normalized state and complex linear idempotents symmetric for the explicit
finite Hermitian pairing. All complete degree-two word-matrix entries are
represented. The space dimension equals the lower matrix rank; it is not
assumed or concluded to be six. `concrete_moment_extraction_inputs` connects the
forward supplied-family moments to these premises.

`FlatMomentBasisRelations.lean` strengthens the finite extraction with
`ContextualSameBasis` and `ContextualCompleteness`. For every pair of lower
words, these input equations impose the same-basis Kronecker product rule and
sum-to-identity relation. `extract_word_basis` derives complete orthogonal
basis actions, symmetry, and the same normalized degree-two representation.
`concrete_moment_basis_inputs` checks these stronger premises for supplied
concrete-family moments. `zero_action_moments_reject_completeness` rejects the
normalized word assignment that vanishes on all nonempty words.
Dimension six, nonzero rank-one outcomes, cross-basis MU conclusions, full
star-algebra extension and coordinate-variety transport for arbitrary input
data remain required for the full MUB bridge.

`CommutativeFlatMoments.lean` now derives a common real point from normalized
positive flat real coordinate moments. Actual Gram factors, nullspace stability,
symmetric commuting multiplication operators and a visible joint eigenvector
supply the construction. `ConcreteMubFlatExtension.lean` checks membership of
all 180 residuals in the quadratic span. Its finite compatibility equations
annihilate each residual times every upper-list monomial, hence each residual
square. The extracted point gives an actual unitary candidate with the 108 MU
overlap conditions. Evaluation at any solution supplies positive flat rank-one
moments, yielding `fourth_basis_iff_positive_flat_moments`.

The exact remaining hypotheses in `moment_nonpositive_of_empty_variety` are
fixed-variety emptiness, real-linearity of the moment functional, normalization,
actual lower/upper rank equality, and `FiniteRelationCompatibility`. No
preconstructed operator family or point is an input. The conclusion is failure
of positive semidefiniteness for that functional. Emptiness itself, full
parameter coverage and rejection of arbitrary nonflat truncations are not
established. The separate word route has not been identified with these real
coordinate moments.

## Derived balance, exact candidate charts and one separated box

- Supported statement: `augmented_exists_with_parameters_iff` retains quartet
  existence at each admissible family parameter in all 666 equations.
  `native_chart_quartet_iff` retains that equivalence with membership in one of
  six actual native candidate charts. `native_box_exclusion` excludes the
  recorded candidate box; `native_box_has_admissible_phase_point` supplies a
  phase-admissible point in that box without asserting it is a quartet.
- Evidence: `SzollosiGaugeBalance.lean`, `SzollosiGaugedExecutable.lean`,
  `SzollosiGaugedCover.lean`, `SzollosiGaugedReflection.lean`, the gauged AST and
  coefficient exports, root/exclusion receipts, and the checkpoint's bound
  native chart replays and complete validation logs.
- Exact premises: an admissible parameter for the fixed-parameter equivalence;
  all 666 equations and membership in the recorded box for its contradiction.
  The 24 balance equations are derived from original equations and first-row
  gauge, whose existence reduction was established earlier. The native image
  semantics concern coordinate 368 and use the actual row balance identity.
- Scope ceiling: six overlapping candidate charts remain unresolved. The
  separated box does not contain every candidate at any specified parameter.
  It does not complete the 56 family cells/three cusp collars, remove curvature,
  establish global quartet absence, or verify all images/generic Rust decoding.

## Prompt 05 campaign checks in Rust

- Supported statement: the 648-row, 320-coordinate balanced table
  `artifacts/balanced_quadratic_coefficients_20261011.jsonl` equals its
  regeneration from the definitions, term by term over Q. A third basis equal
  to the first or to the second makes exactly the 36 transition-modulus rows of
  that pair nonzero, with values in {-6, 30}. The Jacobian at the centre of the
  box has 1045 linear terms in 269 rows and exact rank 184 of 320. The
  campaign's fixed-triple lemmas D1, D2, D3, D9, E.1, F.2 and G hold at the
  values the receipt records.
- Evidence: `omega_mub::omega_native::mub6_balanced_table_replay`
  (`regenerate_equations`) and `mub6_prompt05_campaign_checks`
  (`run_campaign_checks`) in `omega_engine/crates_rs/omega_mub`; the 8 tests in
  `omega_engine/crates_rs/tests/omega_mub/test_mub6_prompt05_campaign_checks.rs`;
  the receipt `artifacts/mub6_prompt05_campaign_receipt.json`; the note
  `research/prompt05_campaign_checks.md`.
- Exact premises: the table bytes pinned by SHA-256; points in Q(ζ24); the box
  [-1, 1] on the 170 slot and D-block coordinates and ±10035/4096 on the 150
  core coordinates (`def bounds` in `MubBalancedTable.lean`).
- Scope ceiling: the Rust table identity is not the Lean equivalence
  `exists_quartet_iff_table`, which has not been elaborated here. `Quartet` is
  global; that bridge is source only. D9's count refutes its stated premise:
  138 of the 180 rows are independent of the Hermitian and diagonal identities,
  and no row-unitarity row is listed. E.1 covers multipliers of degree at most
  one on the fixed triple. F.2 is a commutative model at trace level. D4 is a
  hand lemma whose premise J(0) = 0 is false for this table. None of this
  excludes a quartet or bounds MUB(6) above 3.

## Publication disposition

NO-GO for the current arXiv manuscript and for a new Zenodo release asserting
mathematical closure. The existing archive is historical: its manifest has 495
entries and its extraction test checks 492 file members. Neither count is a theorem.
Current execution results and pending gates are recorded in the executive
checkpoint. A new scoped deposit still needs current-source packaging, review,
and deterministic archive re-certification.

## Formal Claims Register

| ID | Name | Claim Type | Statement | Evidence / Reference |
|:---|:---|:---|:---|:---|
| MUB6-C01 | Orbit Configuration Fourier Count Lower Bound | FormalLeanTheorem | Orbit configuration lower bound on Fourier count (n_dita >= 5) in MUB6OrbitConfiguration. | Lean 4: RouteCFourierLandingBypass (fourier_count_ge_five) |
| MUB6-C02 | Orbit Configuration Fourier Transition Pairs Lower Bound | FormalLeanTheorem | Orbit configuration Fourier transition pairs lower bound (pairCombinations n_dita >= 10). | Lean 4: RouteCFourierLandingBypass (fourier_pairs_ge_ten) |
| MUB6-C03 | Orbit Configuration Fourier Landing Edges Lower Bound | FormalLeanTheorem | Lower bound of at least 15 Fourier transition edges in orbit configuration. | Lean 4: RouteCFourierLandingBypass (fourier_landing_edges_lower_bound) |
| MUB6-C04 | Conditional Non-Existence of Complete MUB(6) via Route C | FormalLeanTheoremConditional | Conditional non-existence of complete MUB(6) via Route C given landing hypothesis h_landing : CompleteMUB6 -> RouteCCompleteMUBFamily. | Lean 4: RouteCFourierLandingBypass (no_complete_mub6_via_route_c) |
| MUB6-C05 | Non-Existence under Fourier Triple Landing Bypass | FormalLeanTheoremConditional | Non-existence of complete MUB(6) under the supplied premise FourierTripleLandingPremise (a constituent triple in InFourierDitaChart), without orbit-count fields. | Lean 4: RouteCFourierLandingBypass (no_complete_mub6_of_fourier_triple_landing) |
| MUB6-C06 | Analytic Cube Slice Certificate for Conjecture 2 | LeanDefinition | Analytic cube slice certificate supplying row bounds, integer parity, and class/table compatibility. | Lean 4: Conjecture2GeneralMechanization (AnalyticCubeSliceCertificate); Tests: tests/test_conj2_all_slice_configurations.py |
| MUB6-C07 | Tao Phase-Table All-Slice Evaluation | FormalLeanTheorem | Kernel-checked evaluation of the Tao phase table across all 20 balanced three-positive/three-negative sign patterns, each with Eisenstein norm 9. | Lean 4: Conjecture2GeneralMechanization (balanced_mask_count, tao_all_balanced_masks) |
| MUB6-C08 | R6 Moduli Classification Receipt Status | CustodyVerification | R6 classification receipt with SHA-256 cf8442d8fe1397226d669fcea7bc038ef8d984a9bae741772b9d742fbe62eb59 retains NOT_A_CERTIFICATE status. | Tests: tests/test_option_b_premises.py |
| MUB6-C09 | Matolcsi Moduli Receipt Verification | CustodyVerification | Matolcsi receipt verification with internal digest separation and custody verification. | Tests: tests/test_option_b_premises.py |
| MUB6-C10 | Cauchy-Binet Invertible Minor Quantitative Bound | FormalLeanTheorem | Every raw 6x6 complex Hadamard has a minor with squared determinant >= 54/5 and inverse-entry squared moduli <= 10/27. | Lean 4: MubMinorChart (exists_minor_norm_ge, inverse_entry_normSq_le, exists_bounded_inverse_minor); Tests: tests/test_remediation_b1_b11.py |
| MUB6-C11 | Complete Block Reconstruction Chart | FormalLeanTheorem | Bounded minor supplies complete block reconstruction chart for quartet existence. | Lean 4: MubBoundedBlockChart (chart_hadamard, chart_hasRawQuartet_iff); Tests: tests/test_remediation_b1_b11.py |
| MUB6-C12 | Division-Free Quartet Matrix Equations | FormalLeanTheorem | Clearing nonzero determinant denominator yields explicit division-free matrix equations equivalent to quartet existence. | Lean 4: MubBoundedQuartetEquations (exists_quartet_iff_equations); Tests: tests/test_remediation_b1_b11.py |
| MUB6-C13 | Standard-Basis Unbiasedness Coordinate Bounds | FormalLeanTheorem | Standard-basis unbiasedness bounds all real candidate coordinates by 1/2 in absolute value. | Lean 4: SzollosiQuartetSystem (mu_identity_coordinates_bounded); Tests: tests/test_remediation_b1_b11.py |
| MUB6-C14 | Rational Affine Completion System | FormalLeanTheorem | Checked affine completion of balanced transition matrices gives an equivalent system of rational polynomial equations. | Lean 4: MubBalancedCompletion (complete_restrict, restrict_complete, complete_row_sum, complete_column_sum); Tests: tests/test_remediation_b1_b11.py |
| MUB6-C15 | Balanced Quadratic System Degree and Equivalence | FormalLeanTheorem | 648 rational polynomial equations of degree at most two in 320 bounded real coordinates whose common zeros are equivalent to quartet existence. The counts are equation and coordinate counts, not dimension or independence claims. | Lean 4: MubBalancedQuadraticPolynomials (equation_degree, exists_quartet_iff_balanced_polynomials); Tests: tests/test_remediation_b1_b11.py |
| MUB6-C16 | Quadratic Lift Equivalence | FormalLeanTheorem | Quadratic lifting yields equivalent quadratic equations preserving all candidate solutions. | Lean 4: SzollosiQuadraticSystem (exists_solution_iff_quartet); Tests: tests/test_remediation_b1_b11.py |
| MUB6-C17 | Rational Containing Box Radius Bounds | FormalLeanTheorem | Rational containing box has radius 1 for phase/raw-basis coordinates and 3 for cross-product coordinates. | Lean 4: SzollosiQuadraticSystem (solution_in_full_box); Tests: tests/test_remediation_b1_b11.py |
| MUB6-C18 | Bounded Solution Quartet Equivalence | FormalLeanTheorem | Bounded solution existence in full box is equivalent to actual quartet existence. | Lean 4: SzollosiQuadraticSystem (exists_bounded_solution_iff_quartet); Tests: tests/test_remediation_b1_b11.py |
| MUB6-C19 | Deltoid Cover Standard-Basis Margin Disjointness | ExactComputation | Deltoid candidate box residual margin 37249/90000 separates standard-basis residual outside unbiased candidate box (\|U[0,0]\|^2 = 1/6). | Tests: tests/test_remediation_b1_b11.py |
| MUB6-C20 | Augmented 666-Equation System Parameter Equivalence | FormalLeanTheorem | Quartet existence is equivalent to augmented 666-equation solution at each admissible family parameter. | Lean 4: SzollosiGaugedExecutable (augmented_exists_with_parameters_iff); Tests: tests/test_gauged_reflection_wire.py |
| MUB6-C21 | Native Six-Chart Candidate Cover Equivalence | FormalLeanTheorem | Quartet existence is equivalent to an augmented-system solution in at least one of six overlapping native candidate charts. | Lean 4: SzollosiGaugedReflection (native_chart_quartet_iff); Tests: tests/test_gauged_reflection_wire.py |
| MUB6-C22 | Szöllősi Continuous Two-Circulant Construction | FormalLeanTheorem | Unit phases and complex compatibility equation yield Gram identity, normalized unitarity, and 1/6 entry moduli. | Lean 4: SzollosiTwoCirculant (rawSix_gram, normalized_unitary, normalized_entry_modulus); Tests: tests/test_remediation_b1_b11.py |
| MUB6-C23 | Szöllősi Quartet Equivalence with Arbitrary Additional Bases | FormalLeanTheorem | Quartet existence with identity and family matrix equivalent to candidate equations with 144 retained coordinates. | Lean 4: SzollosiQuartetSystem (quartet_iff_candidate_equations); Tests: tests/test_remediation_b1_b11.py |
| MUB6-C24 | 618 Rational Equations Degree at Most Two | FormalLeanTheorem | 618 rational equations in 440 real variables have total degree at most two, with solutions corresponding to actual quartets. | Lean 4: SzollosiQuadraticSystem (equation_degree, exists_solution_with_parameters_iff); Tests: tests/test_remediation_b1_b11.py |
| MUB6-C25 | Midpoint Secant Identity and Exclusion Soundness | FormalLeanTheorem | Exact midpoint secant identity and derivative intervals enclose zeros; strict coordinate separation excludes roots. | Lean 4: RectangularQuadraticExclusion (list_secant_identity, exclusion_sound); Tests: tests/test_rectangular_reflection_wire.py |
| MUB6-C26 | Column-Gauge Reduction First-Row Equality | FormalLeanTheorem | 24 real wire coordinates prescribed with ordered IDs and values checked by kernel reduction (by rfl). | Lean 4: SzollosiColumnGauge (gaugePointCodes_checked, gauge_box_firstRow); Tests: tests/test_gauged_reflection_wire.py |
| MUB6-C27 | Native Sparse Jacobian Row Reflection | FormalLeanTheorem | All 618 sparse Jacobian rows (9,000 entries) and 440 images match sound actual-system semantics. | Lean 4: SzollosiRectangularReflection (native_jacobian_eq, native_images_eq); Tests: tests/test_rectangular_reflection_wire.py::test_formatter_reproduces_the_kernel_checked_source |
| MUB6-C28 | Native Candidate Box Exclusion on Coordinate 368 | FormalLeanTheorem | Native box exclusion excludes recorded candidate box via row balance coordinate 368 without global quartet absence. | Lean 4: SzollosiGaugedReflection (native_box_exclusion, native_box_has_admissible_phase_point); Tests: tests/test_gauged_reflection_wire.py::test_formatter_reproduces_checked_candidate_box_source |
| MUB6-C29 | Concrete Complex Rank-One Projector Matrix Construction | FormalLeanTheorem | Construction of complex rank-one projector matrices from FiniteComplexMubFamily with self-adjointness and trace one. | Lean 4: ConcreteMubProjectors (concreteProjector_self_adjoint, concreteProjector_trace_one); Tests: tests/test_remediation_m1_m4.py |
| MUB6-C30 | Concrete MUB Word Moment Flatness | FormalLeanTheorem | Degree-one and two word Gram moment matrices are PSD with rank equality to coordinate cardinality. | Lean 4: ConcreteMubMoments (concrete_mub_moment_flatness); Tests: tests/test_remediation_m1_m4.py |
| MUB6-C31 | Concrete MUB Orthonormality and Overlap Polynomials | FormalLeanTheorem | 108 MU residuals in 72 real coordinates agree with projector cross-trace minus 1/6; 72 further residuals encode candidate orthonormality U*U = I. | Lean 4: ConcreteMubPolynomials (muPolynomial_eval_projector_trace); Tests: tests/test_remediation_m1_m4.py |
| MUB6-C32 | Finite Reverse Word Projector Extraction | FormalLeanTheorem | Extraction of Gram factor, common range, normalized state, and complex linear idempotents from positive flat data. | Lean 4: FlatMomentProjectorExtraction (extract_word_projectors); Tests: tests/test_remediation_m1_m4.py |
| MUB6-C33 | Contextual Basis Word Relations Extraction | FormalLeanTheorem | Extraction of orthogonal basis actions and normalized degree-two representation from contextual same-basis data. | Lean 4: FlatMomentBasisRelations (extract_word_basis); Tests: tests/test_remediation_m1_m4.py |
| MUB6-C34 | Zero-Action Interface Countermodel Inhabitation | FormalLeanTheorem | Unconstrained projector interface admits trivial countermodel lacking completeness and cross-basis constraints. | Lean 4: MomentPositivityObligation (not_universal_interface_exclusion); Tests: tests/test_remediation_m1_m4.py |
| MUB6-C35 | Commutative Flat Real Moments Zero Extraction | FormalLeanTheorem | Construction of common real point from normalized positive flat real coordinate moments via commuting operators. | Lean 4: CommutativeFlatMoments (real_point_of_positive_flat); Tests: tests/test_remediation_m1_m4.py |
| MUB6-C36 | Fourth-Basis Existence Equivalence to Positive Flat Moments | FormalLeanTheorem | Existence of unitary fourth-basis candidate is equivalent to normalized positive flat compatible coordinate moments. | Lean 4: ConcreteMubFlatExtension (fourth_basis_iff_positive_flat_moments); Tests: tests/test_remediation_m1_m4.py |
| MUB6-C37 | Moment Functional Nonpositivity from Empty Variety | FormalLeanTheorem | Fixed-variety emptiness and finite relation compatibility imply failure of positive semidefiniteness for moment functional. | Lean 4: ConcreteMubFlatExtension (moment_nonpositive_of_empty_variety); Tests: tests/test_remediation_m1_m4.py |
| MUB6-C38 | Balanced Table Regeneration, Negative Controls and Centre Jacobian | ExactComputation | The 648-row, 320-coordinate balanced table equals its regeneration from the definitions over Q; a third basis equal to the first or second makes exactly 36 transition-modulus rows nonzero; the Jacobian at the box centre has exact rank 184 of 320. Not the Lean equivalence exists_quartet_iff_table, which is not elaborated. | Rust: omega_mub mub6_balanced_table_replay (regenerate_equations), mub6_prompt05_campaign_checks (run_campaign_checks); Tests: omega_engine/crates_rs/tests/omega_mub/test_mub6_prompt05_campaign_checks.rs; Receipt: artifacts/mub6_prompt05_campaign_receipt.json |
| MUB6-C39 | Prompt 05 Fixed-Triple Local Lemma Checks | ExactComputation | Fixed-triple checks D1 (product triple, overlaps 1/6), D2 (decoy overlaps), D3 (Gram multiplicities 4^1, 1^20, 0^3), D9 (180 = 108 + 72 rows, 138 not implied, no row-unitarity rows), E.1 (252 x 73 affine-multiplier expectations zero under a four-point design), F.2 (commutative trace model, sandwich identity fails in 432 of 432 cases) and G (320 = 152 + 18 + 150). Scope: the fixed triple; no quartet exclusion. | Rust: omega_mub mub6_prompt05_campaign_checks (run_campaign_checks); Tests: omega_engine/crates_rs/tests/omega_mub/test_mub6_prompt05_campaign_checks.rs; Receipt: artifacts/mub6_prompt05_campaign_receipt.json |
| MUB6-C40 | Szöllősi Common-Ray Reduction | FormalLeanTheorem | For a raw complex Hadamard H, H lies in a quartet with I iff two orthonormal bases of common rays of I and H are mutually unbiased; so if no two common rays are unbiased, H is in no quartet. Owner build of 2026-10-15: lake exit 0, axioms propext, Classical.choice, Quot.sound, source sha256 830f5016… unchanged on main; not rebuilt on 2026-10-16. | Lean 4: SzollosiCommonRays (quartet_iff_ray_bases, no_quartet_of_no_unbiased_ray_pair); Receipt: research/five_derivations_20261015/execution_receipt.json |
| MUB6-C41 | Pair Exclusion at the Special Szöllősi Point, Represented Rays | ExactComputation | At (x, y, u, v) = (1, -1, 1, i), the 120 real rays represented by the rational parametrization are nonsingular, and all 7,140 pairs satisfy ||z*w|^2 - 6| > 47/100. Status PASS_FOR_REPRESENTED_SOLUTIONS: completeness of the ray set needs an independent bound on the number of complex solutions. Not replayed on 2026-10-16 (needs python-flint and PARI/GP). | Script: research/five_derivations_20261015/replay_rur.py; Tests: research/five_derivations_20261015/test_rur.py; Receipt: research/five_derivations_20261015/special_replay.json |

<!-- BEGIN UNIFIED-DAG-BACKLINKS -->
<!-- Generated by papers/core/tools/build_corpus_dag_backlinks.py; edit the tool, not this region. -->

## Unified DAG

Audit of 2026-10-21. The unified derivation DAG (`dag/fragments/unified_dag.json`) folds the records of this corpus into one graph: a record with no trunk counterpart is a NEW application-branch node with its own TFQ record; a restatement of a trunk step is an ALIAS row that points to the trunk node. *Source claimed* is the status the source asserted; *Audited* is the status the audit assigned against what is actually in this checkout (Lean declarations resolved, replays rerun, statements compared). The original claims, labels and text of this document are kept unchanged. A status below the source claim means the claim is not established as stated; it does not mean the underlying mathematics is false (only REFUTED means that). For an ALIAS row the audited column is the status of the trunk node, which is the authority for the restated step. Regenerate with `python -I -X utf8 papers/core/tools/build_corpus_dag_backlinks.py`. The MUB6 register has no status field; the claimed status of its records is PROVED_LEAN because each cites a Lean name. Rows whose id is not a `MUB6-DERIV-*` id come from the claim ledger, the paper or the atlas.

63 NEW records and 51 ALIAS rows; 35 same, 26 lowered, 1 raised, 1 reclassified. REFUTED: `MUB6-DERIV-062`.

| Source id | Kind | TFQ record | DAG node | Source claimed | Audited | Reconciliation |
|---|---|---|---|---|---|---|
| `MUB6-ATLAS-CORNER-ROUTING` | NEW | [TFQ-1266](../../../dag/derivations/25_mub/tfq_1266_mub6_corner_routing_dephasing.md) | `MUB6-CORNER-ROUTING-DEPHASING` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C01` | NEW | [TFQ-1256](../../../dag/derivations/25_mub/tfq_1256_mub6_route_c_label_arithmetic.md) | `MUB6-ROUTE-C-LABEL-ARITHMETIC` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C05` | NEW | [TFQ-1257](../../../dag/derivations/25_mub/tfq_1257_mub6_route_c_conditional.md) | `MUB6-ROUTE-C-CONDITIONAL` | CONDITIONAL | **CONDITIONAL** | same |
| `MUB6-C10` | NEW | [TFQ-1259](../../../dag/derivations/25_mub/tfq_1259_mub6_cauchy_binet_minor_bound.md) | `MUB6-CAUCHY-BINET-MINOR-BOUND` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C12` | NEW | [TFQ-1260](../../../dag/derivations/25_mub/tfq_1260_mub6_bounded_block_quartet_equations.md) | `MUB6-BOUNDED-BLOCK-QUARTET-EQUATIONS` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C15` | NEW | [TFQ-1264](../../../dag/derivations/25_mub/tfq_1264_mub6_balanced_648_quadratic.md) | `MUB6-BALANCED-648-QUADRATIC` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C19` | NEW | [TFQ-1267](../../../dag/derivations/25_mub/tfq_1267_mub6_deltoid_cover_box_defect.md) | `MUB6-DELTOID-COVER-BOX-DEFECT` | COMPUTATIONALLY_CHECKED | **PROVED_PROSE** | raised |
| `MUB6-C20` | NEW | [TFQ-1269](../../../dag/derivations/25_mub/tfq_1269_mub6_szollosi_gauged_666.md) | `MUB6-SZOLLOSI-GAUGED-666` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C24` | NEW | [TFQ-1268](../../../dag/derivations/25_mub/tfq_1268_mub6_szollosi_618_system.md) | `MUB6-SZOLLOSI-618-SYSTEM` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C25` | NEW | [TFQ-1271](../../../dag/derivations/25_mub/tfq_1271_mub6_rectangular_krawczyk_soundness.md) | `MUB6-RECTANGULAR-KRAWCZYK-SOUNDNESS` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C27` | NEW | [TFQ-1272](../../../dag/derivations/25_mub/tfq_1272_mub6_szollosi_fullbox_unresolved.md) | `MUB6-SZOLLOSI-FULLBOX-UNRESOLVED` | PROVED_LEAN | **COMPUTATIONALLY_CHECKED** | lowered |
| `MUB6-C28` | NEW | [TFQ-1270](../../../dag/derivations/25_mub/tfq_1270_mub6_szollosi_box_368_exclusion.md) | `MUB6-SZOLLOSI-BOX-368-EXCLUSION` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C29` | NEW | [TFQ-1276](../../../dag/derivations/25_mub/tfq_1276_mub6_concrete_projectors.md) | `MUB6-CONCRETE-PROJECTORS` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C30` | NEW | [TFQ-1277](../../../dag/derivations/25_mub/tfq_1277_mub6_concrete_moment_flatness.md) | `MUB6-CONCRETE-MOMENT-FLATNESS` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C32` | NEW | [TFQ-1278](../../../dag/derivations/25_mub/tfq_1278_mub6_word_projector_extraction.md) | `MUB6-WORD-PROJECTOR-EXTRACTION` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C34` | NEW | [TFQ-1279](../../../dag/derivations/25_mub/tfq_1279_mub6_interface_countermodel.md) | `MUB6-INTERFACE-COUNTERMODEL` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C35` | NEW | [TFQ-1280](../../../dag/derivations/25_mub/tfq_1280_mub6_commutative_flat_real_point.md) | `MUB6-COMMUTATIVE-FLAT-REAL-POINT` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C36` | NEW | [TFQ-1281](../../../dag/derivations/25_mub/tfq_1281_mub6_fourth_basis_flat_moments.md) | `MUB6-FOURTH-BASIS-FLAT-MOMENTS` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C37` | NEW | [TFQ-1282](../../../dag/derivations/25_mub/tfq_1282_mub6_empty_variety_moment_nonpsd.md) | `MUB6-EMPTY-VARIETY-MOMENT-NONPSD` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C40` | NEW | [TFQ-1274](../../../dag/derivations/25_mub/tfq_1274_mub6_szollosi_common_rays.md) | `MUB6-SZOLLOSI-COMMON-RAYS` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C41` | NEW | [TFQ-1275](../../../dag/derivations/25_mub/tfq_1275_mub6_szollosi_special_point_pairs.md) | `MUB6-SZOLLOSI-SPECIAL-POINT-PAIRS` | COMPUTATIONALLY_CHECKED | **COMPUTATIONALLY_CHECKED** | same |
| `MUB6-DERIV-001` | ALIAS | - | `PG-INERT-DIAMOND` | PROVED_LEAN | **DEFINITION** | restated in trunk |
| `MUB6-DERIV-002` | ALIAS | - | `PG-ADMISSION-FLOOR` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-003` | ALIAS | - | `L1-QM002-O022A-PHI1-QUOTIENT` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-004` | ALIAS | - | `PG-GEN-REWRITING-COMMUTATION` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-005` | ALIAS | [TFQ-0003](../../../dag/derivations/03_finite_obstruction/tfq_0003_finite_obstruction_calculus_on_a_declared_carrier.md) | `TFQ-0003` | PROVED_LEAN | **OPEN** | restated in trunk |
| `MUB6-DERIV-006` | ALIAS | [TFQ-0455](../../../dag/derivations/02_genesis/tfq_0455_d2_initial_pointed.md) | `PGW-D2-INITIAL-POINTED` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-007` | ALIAS | [TFQ-0499](../../../dag/derivations/02_genesis/tfq_0499_python_lean_carrier_bridge.md) | `PGW-PYTHON-LEAN-CARRIER-BRIDGE` | PROVED_LEAN | **OPEN** | restated in trunk |
| `MUB6-DERIV-008` | ALIAS | [TFQ-0459](../../../dag/derivations/02_genesis/tfq_0459_canonical_key_classification.md) | `PGW-CANONICAL-KEY-CLASSIFICATION` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-009` | ALIAS | [TFQ-0447](../../../dag/derivations/02_genesis/tfq_0447_count_invariance_transport.md) | `PGW-COUNT-INVARIANCE-TRANSPORT` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-010` | ALIAS | [TFQ-0549](../../../dag/derivations/06_wdp/tfq_0549_wdp_degree_k_torsion_balance.md) | `PGW-WDP-DEGREE-K-TORSION-BALANCE` | PROVED_LEAN | **PROVED_PROSE** | restated in trunk |
| `MUB6-DERIV-011` | ALIAS | [TFQ-0553](../../../dag/derivations/06_wdp/tfq_0553_wdp_observer_quotient_passivity.md) | `PGW-WDP-OBSERVER-QUOTIENT-PASSIVITY` | PROVED_LEAN | **DEFINITION** | restated in trunk |
| `MUB6-DERIV-012` | ALIAS | - | `PG-WDP-DIAGNOSTIC-NOT-ROUTING` | PROVED_LEAN | **DEFINITION** | restated in trunk |
| `MUB6-DERIV-013` | ALIAS | - | `DS-QM090-092-AUTHORITY-FIREWALL` | PROVED_LEAN | **COMPUTATIONALLY_CHECKED** | restated in trunk |
| `MUB6-DERIV-014` | ALIAS | - | `DS-QM103-SHOW-THE-PACKET-PROTOCOL` | PROVED_LEAN | **DEFINITION** | restated in trunk |
| `MUB6-DERIV-015` | ALIAS | - | `PG-WDP-DIAGNOSTIC-NOT-ROUTING` | PROVED_LEAN | **DEFINITION** | restated in trunk |
| `MUB6-DERIV-016` | ALIAS | - | `L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED` | PROVED_LEAN | **CONDITIONAL** | restated in trunk |
| `MUB6-DERIV-017` | ALIAS | - | `L1-WDP-WITNESS-MASS` | PROVED_LEAN | **DEFINITION** | restated in trunk |
| `MUB6-DERIV-018` | ALIAS | - | `DS-QM081-STOCHASTIC-L1-CONTRACTION` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-019` | ALIAS | - | `L1-QM121-LADDER-RUNGS-2-6` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-020` | ALIAS | [TFQ-0170](../../../dag/derivations/22_implementation_sibling/tfq_0170_keep_majorization_finite_markov_laws_and_row_stochastic_maps_on_exact_rational_kernels.md) | `TFQ-0170` | PROVED_LEAN | **COMPUTATIONALLY_CHECKED** | restated in trunk |
| `MUB6-DERIV-021` | ALIAS | - | `L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-022` | ALIAS | - | `L1-IMP-U1-PHASES` | PROVED_LEAN | **IMPORTED_ASSUMPTION** | restated in trunk |
| `MUB6-DERIV-023` | ALIAS | - | `FQ-BORN-NORMALIZATION-REDUNDANCY` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-024` | ALIAS | - | `GP-IMPORT-GLEASON` | PROVED_LEAN | **IMPORTED_ASSUMPTION** | restated in trunk |
| `MUB6-DERIV-025` | ALIAS | - | `DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-026` | ALIAS | - | `L1-IMP-HILBERT-INNER-PRODUCT` | PROVED_LEAN | **CONDITIONAL** | restated in trunk |
| `MUB6-DERIV-027` | ALIAS | [TFQ-0315](../../../dag/derivations/09_finite_hilbert/tfq_0315_exact_density_ray_and_population_shadow.md) | `TFQ-0315` | PROVED_LEAN | **SOURCE_RECORD** | restated in trunk |
| `MUB6-DERIV-028` | ALIAS | - | `DS-QM030-PROJECTION-POSTULATE-AND-BORN-PAIRING-IMPORT` | PROVED_LEAN | **IMPORTED_ASSUMPTION** | restated in trunk |
| `MUB6-DERIV-029` | ALIAS | [TFQ-0416](../../../dag/derivations/27_tensor_composition/tfq_0416_tensor_finite_povm_availability.md) | `TENSOR-FINITE-POVM-AVAILABILITY` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-030` | ALIAS | - | `FQ-CPTP-CLASS-DEFINITION` | PROVED_LEAN | **DEFINITION** | restated in trunk |
| `MUB6-DERIV-031` | ALIAS | [TFQ-0138](../../../dag/derivations/21_implementation_core/tfq_0138_heisenberg_picture_and_cayley_jet.md) | `TFQ-0138` | PROVED_LEAN | **COMPUTATIONALLY_CHECKED** | restated in trunk |
| `MUB6-DERIV-032` | ALIAS | - | `DS-QM030-GRADED-PATHSUM` | PROVED_LEAN | **COMPUTATIONALLY_CHECKED** | restated in trunk |
| `MUB6-DERIV-033` | ALIAS | - | `FQ-DISCRETE-DYNAMICS-DICHOTOMY` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-034` | ALIAS | - | `DS-QM041-HEISENBERG-PICTURE-FINITE` | PROVED_LEAN | **COMPUTATIONALLY_CHECKED** | restated in trunk |
| `MUB6-DERIV-035` | ALIAS | - | `DS-QM043-DECOHERENCE-FUNCTIONAL-IMPORT` | PROVED_LEAN | **IMPORTED_ASSUMPTION** | restated in trunk |
| `MUB6-DERIV-036` | ALIAS | - | `FQ-U1-TRANSPORT-N-TORSION` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-037` | ALIAS | - | `DS-QM064-074-083-ANNEX-REDIRECT-ROWS` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-038` | ALIAS | - | `DS-QM063-HOLONOMY-COHERENT-INTENSITY` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-039` | ALIAS | - | `FQ-QM207-231-FINITE-MAP-CONTROLS` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-040` | ALIAS | - | `FQ-U1-TRANSPORT-N-TORSION` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-041` | ALIAS | [TFQ-0018](../../../dag/derivations/17_finite_qcd/tfq_0018_treat_c_n_as_a_declared_label_space_before_any_graph_attachment.md) | `TFQ-0018` | PROVED_LEAN | **COMPUTATIONALLY_CHECKED** | restated in trunk |
| `MUB6-DERIV-042` | ALIAS | [TFQ-0011](../../../dag/derivations/17_finite_qcd/tfq_0011_finite_qcd_shadow.md) | `TFQ-0011` | PROVED_LEAN | **OPEN** | restated in trunk |
| `MUB6-DERIV-043` | ALIAS | [TFQ-0033](../../../dag/derivations/17_finite_qcd/tfq_0033_construct_an_explicit_three_index_color_contraction_before_using_a_baryon_singlet_label.md) | `TFQ-0033` | PROVED_LEAN | **OPEN** | restated in trunk |
| `MUB6-DERIV-044` | ALIAS | - | `DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-045` | ALIAS | [TFQ-0021](../../../dag/derivations/17_finite_qcd/tfq_0021_record_channel_factors_as_casimir_arithmetic_not_as_composites.md) | `TFQ-0021` | PROVED_LEAN | **COMPUTATIONALLY_CHECKED** | restated in trunk |
| `MUB6-DERIV-046` | ALIAS | [TFQ-0084](../../../dag/derivations/19_finite_qg/tfq_0084_finite_quantum_gravity_shadow.md) | `TFQ-0084` | PROVED_LEAN | **OPEN** | restated in trunk |
| `MUB6-DERIV-047` | ALIAS | [TFQ-0107](../../../dag/derivations/19_finite_qg/tfq_0107_gap_einstein_equation_and_physical_cosmological_constant_stay_unpaid_deficit_is_not.md) | `TFQ-0107` | PROVED_LEAN | **OPEN** | restated in trunk |
| `MUB6-DERIV-048` | ALIAS | - | `DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-049` | ALIAS | - | `DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-050` | ALIAS | - | `DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-051` | NEW | [TFQ-1221](../../../dag/derivations/25_mub/tfq_1221_mub6_quhex_tensor_carrier.md) | `MUB6-QUHEX-TENSOR-CARRIER` | PROVED_LEAN | **DEFINITION** | reclassified |
| `MUB6-DERIV-052` | NEW | [TFQ-1222](../../../dag/derivations/25_mub/tfq_1222_mub6_no_field_of_order_six.md) | `MUB6-NO-FIELD-OF-ORDER-SIX` | PROVED_LEAN | **IMPORTED_ASSUMPTION** | lowered |
| `MUB6-DERIV-053` | NEW | [TFQ-1223](../../../dag/derivations/25_mub/tfq_1223_mub6_weyl_heisenberg_d6.md) | `MUB6-WEYL-HEISENBERG-D6` | PROVED_LEAN | **IMPORTED_ASSUMPTION** | lowered |
| `MUB6-DERIV-054` | NEW | [TFQ-1224](../../../dag/derivations/25_mub/tfq_1224_mub6_weyl_stabilizer_bound.md) | `MUB6-WEYL-STABILIZER-BOUND` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-055` | ALIAS | [TFQ-0402](../../../dag/derivations/25_mub/tfq_0402_mub_exact_projectors.md) | `MUB-EXACT-PROJECTORS` | PROVED_LEAN | **DEFINITION** | restated in trunk |
| `MUB6-DERIV-056` | NEW | [TFQ-1225](../../../dag/derivations/25_mub/tfq_1225_mub6_quartet_raw_hadamard_transport.md) | `MUB6-QUARTET-RAW-HADAMARD-TRANSPORT` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-DERIV-057` | NEW | [TFQ-1226](../../../dag/derivations/25_mub/tfq_1226_mub6_fourier_dita_family_chm.md) | `MUB6-FOURIER-DITA-FAMILY-CHM` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-DERIV-058` | NEW | [TFQ-1227](../../../dag/derivations/25_mub/tfq_1227_mub6_haagerup_matrix_chm.md) | `MUB6-HAAGERUP-MATRIX-CHM` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-DERIV-059` | NEW | [TFQ-1228](../../../dag/derivations/25_mub/tfq_1228_mub6_szollosi_two_circulant.md) | `MUB6-SZOLLOSI-TWO-CIRCULANT` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-DERIV-060` | NEW | [TFQ-1229](../../../dag/derivations/25_mub/tfq_1229_mub6_karlsson_affine_ansatz.md) | `MUB6-KARLSSON-AFFINE-ANSATZ` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-DERIV-061` | NEW | [TFQ-1230](../../../dag/derivations/25_mub/tfq_1230_mub6_tao_matrix_chm.md) | `MUB6-TAO-MATRIX-CHM` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-DERIV-062` | NEW | [TFQ-1231](../../../dag/derivations/25_mub/tfq_1231_mub6_affine_fiber_third_basis.md) | `MUB6-AFFINE-FIBER-THIRD-BASIS` | PROVED_LEAN | **REFUTED** | lowered |
| `MUB6-DERIV-063` | NEW | [TFQ-1232](../../../dag/derivations/25_mub/tfq_1232_mub6_product_triple_lower_bound.md) | `MUB6-PRODUCT-TRIPLE-LOWER-BOUND` | PROVED_LEAN | **COMPUTATIONALLY_CHECKED** | lowered |
| `MUB6-DERIV-064` | NEW | [TFQ-1233](../../../dag/derivations/25_mub/tfq_1233_mub6_fixed_triple_variety.md) | `MUB6-FIXED-TRIPLE-VARIETY` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-DERIV-065` | NEW | [TFQ-1234](../../../dag/derivations/25_mub/tfq_1234_mub6_180_residual_count.md) | `MUB6-180-RESIDUAL-COUNT` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-DERIV-066` | NEW | [TFQ-1235](../../../dag/derivations/25_mub/tfq_1235_mub6_gram_nullstellensatz_claim.md) | `MUB6-GRAM-NULLSTELLENSATZ-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-067` | NEW | [TFQ-1236](../../../dag/derivations/25_mub/tfq_1236_mub6_groebner_elimination_claim.md) | `MUB6-GROEBNER-ELIMINATION-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-068` | NEW | [TFQ-1237](../../../dag/derivations/25_mub/tfq_1237_mub6_torus_cad_emptiness_claim.md) | `MUB6-TORUS-CAD-EMPTINESS-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-069` | NEW | [TFQ-1251](../../../dag/derivations/25_mub/tfq_1251_mub6_moment_evaluation_flat.md) | `MUB6-MOMENT-EVALUATION-FLAT` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-DERIV-070` | NEW | [TFQ-1238](../../../dag/derivations/25_mub/tfq_1238_mub6_degree2_sdp_gap_claim.md) | `MUB6-DEGREE2-SDP-GAP-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-071` | NEW | [TFQ-1239](../../../dag/derivations/25_mub/tfq_1239_mub6_flat_extension_failure_claim.md) | `MUB6-FLAT-EXTENSION-FAILURE-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-072` | NEW | [TFQ-1240](../../../dag/derivations/25_mub/tfq_1240_mub6_commutativity_defect_claim.md) | `MUB6-COMMUTATIVITY-DEFECT-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-073` | NEW | [TFQ-1241](../../../dag/derivations/25_mub/tfq_1241_mub6_positivstellensatz_claim.md) | `MUB6-POSITIVSTELLENSATZ-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-074` | NEW | [TFQ-1242](../../../dag/derivations/25_mub/tfq_1242_mub6_rational_ldl_claim.md) | `MUB6-RATIONAL-LDL-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-075` | NEW | [TFQ-1252](../../../dag/derivations/25_mub/tfq_1252_mub6_conjecture2_premise.md) | `MUB6-CONJECTURE2-PREMISE` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-076` | NEW | [TFQ-1253](../../../dag/derivations/25_mub/tfq_1253_mub6_tao_laurent_norm_nine.md) | `MUB6-TAO-LAURENT-NORM-NINE` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-DERIV-077` | NEW | [TFQ-1243](../../../dag/derivations/25_mub/tfq_1243_mub6_krawczyk_global_cover_claim.md) | `MUB6-KRAWCZYK-GLOBAL-COVER-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-078` | NEW | [TFQ-1244](../../../dag/derivations/25_mub/tfq_1244_mub6_smale_alpha_claim.md) | `MUB6-SMALE-ALPHA-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-079` | NEW | [TFQ-1245](../../../dag/derivations/25_mub/tfq_1245_mub6_residual_fence_claim.md) | `MUB6-RESIDUAL-FENCE-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-080` | NEW | [TFQ-1246](../../../dag/derivations/25_mub/tfq_1246_mub6_cusp_puiseux_claim.md) | `MUB6-CUSP-PUISEUX-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-081` | NEW | [TFQ-1247](../../../dag/derivations/25_mub/tfq_1247_mub6_psi_gluing_claim.md) | `MUB6-PSI-GLUING-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-082` | NEW | [TFQ-1248](../../../dag/derivations/25_mub/tfq_1248_mub6_phi1_circulation_claim.md) | `MUB6-PHI1-CIRCULATION-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-083` | NEW | [TFQ-1249](../../../dag/derivations/25_mub/tfq_1249_mub6_route_c_landing_claim.md) | `MUB6-ROUTE-C-LANDING-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-084` | NEW | [TFQ-1250](../../../dag/derivations/25_mub/tfq_1250_mub6_five_branch_routing_claim.md) | `MUB6-FIVE-BRANCH-ROUTING-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-085` | NEW | [TFQ-1254](../../../dag/derivations/25_mub/tfq_1254_mub6_no_quartet_d6.md) | `MUB6-NO-QUARTET-D6` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-086` | NEW | [TFQ-1255](../../../dag/derivations/25_mub/tfq_1255_mub6_max_mub_six_equals_three.md) | `MUB6-MAX-MUB-SIX-EQUALS-THREE` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-IMPORT-OPENAI-LE5` | NEW | [TFQ-1365](../../../dag/derivations/25_mub/tfq_1365_mub6_openai_family_le_five.md) | `MUB6-OPENAI-FAMILY-LE-FIVE` | IMPORTED_ASSUMPTION | **IMPORTED_ASSUMPTION** | same |
| `MUB6-LEDGER-COVER56` | NEW | [TFQ-1273](../../../dag/derivations/25_mub/tfq_1273_mub6_cover56_curvature_premise.md) | `MUB6-COVER56-CURVATURE-PREMISE` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-LEDGER-G3-GLUING` | NEW | [TFQ-1258](../../../dag/derivations/25_mub/tfq_1258_mub6_gluing_g3_opaque.md) | `MUB6-GLUING-G3-OPAQUE` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-PAPER-BALANCE-SYZYGY` | NEW | [TFQ-1265](../../../dag/derivations/25_mub/tfq_1265_mub6_transition_balance_syzygy.md) | `MUB6-TRANSITION-BALANCE-SYZYGY` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-PAPER-CLOSE-COLUMNS` | NEW | [TFQ-1263](../../../dag/derivations/25_mub/tfq_1263_mub6_close_columns_exclusion.md) | `MUB6-CLOSE-COLUMNS-EXCLUSION` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-PAPER-FINITE-CORNER` | NEW | [TFQ-1261](../../../dag/derivations/25_mub/tfq_1261_mub6_finite_corner_reduction.md) | `MUB6-FINITE-CORNER-REDUCTION` | PROVED_LEAN | **IMPORTED_ASSUMPTION** | lowered |
| `MUB6-PAPER-QUADRATIC-LIFT` | NEW | [TFQ-1262](../../../dag/derivations/25_mub/tfq_1262_mub6_quadratic_lift_386.md) | `MUB6-QUADRATIC-LIFT-386` | PROVED_LEAN | **PROVED_LEAN** | same |

### Audit errata (2026-10-21)

- 2026-10-21 ERRATUM (MUB6-DERIV-062, TFQ-1231): REFUTED. The register claims that no affine family through F_2 (x) F_3 contains a third basis unbiased to both the identity and the base matrix. The product triple I_6, F_2 (x) F_3 / sqrt 6, A_2 (x) C_2 (itself row-phase equivalent to F_2 (x) F_3) is pairwise unbiased (exact check `verify_three_bases`, squared overlaps 1/6; Jaming et al., arXiv:0902.0882, give an infinite family of such triplets from the Fourier family).
- 2026-10-21 ERRATUM (MUB6-DERIV-064/065, TFQ-1233/TFQ-1234): The total of 180 real constraints in 72 coordinates is correct, but the split '36 normalization, 36 against I_6, 108 against F_6 and B_3' is not the one in Lean. The Lean indexing (`total_equation_count`, `mu_equation_count`, `coordinate_count`) is 108 MU residuals (36 per basis of the fixed triple) plus 72 real and imaginary components of U*U - I. The count is not an independence, rank or overdetermination statement.
- 2026-10-21 ERRATUM (MUB6-DERIV-053, TFQ-1223): With X|j> = |j+1 mod 6> and Z|j> = w^j|j> one has Z X = w X Z, equivalently X Z = w^{-1} Z X. The register writes X Z = w Z X, which holds only under the opposite clock convention. There is no d = 6 Lean declaration for it, and no MUB count follows from the relation.
- 2026-10-21 ERRATUM (MUB6-DERIV-075, TFQ-1252): The register summary states Conjecture 2 as: no 6x6 complex Hadamard matrix has all 20 balanced 3x3 submatrices with determinant zero, and that it implies no fourth basis unbiased to F_6. Neither is the conjecture. Matolcsi, Matszangosz, Varga and Weiner (arXiv:2503.14752) conjecture Laurent (character) vanishing g_H(pi a) = 0 for every coordinate permutation pi of a = (1,1,1,-1,-1,-1), plus a condition coupling the characters at 3a, for transitions of a MUB triplet; with Conjecture 3 and Proposition 4.2 it would give at most three MUBs. Corrected in the register (original wording in summary_original) on 2026-10-21.
- 2026-10-21 ERRATUM (MUB6-DERIV-076, TFQ-1253): The register calls the quantity an l1 operator norm ||P S_6 P||_1 = 9. The computed (and Lean) quantity is |sum_j prod_r S_rj^{g_r}|^2 = 9 for each of the 20 balanced sign vectors g (`tao_all_balanced_masks`, `tao_all_balanced_laurent`). This is a finite evaluation for one matrix and gives no nonextension statement without Conjecture 2.
- 2026-10-21 ERRATUM (MUB6-DERIV-085/086, TFQ-1254/TFQ-1255): Both records carry PROVED_LEAN. DERIV-085 (no quartet in dimension six) and DERIV-086 (max MUB(6) = 3) are OPEN: no such declaration exists under `lean4/`, and the package itself states that N(6) = 3 remains open.
- 2026-10-21 ERRATUM (MUB6-LEAN-CENSUS): None of the 86 Lean names in the register's `languages.lean4` fields exists. The Lean that actually backs the audited records lives in the repository-root `lean4/` (ConcreteMub*, Szollosi*, MubTaoLaurent, Conjecture2GeneralMechanization, ...).

<!-- END UNIFIED-DAG-BACKLINKS -->
