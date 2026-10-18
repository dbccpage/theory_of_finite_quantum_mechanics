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
