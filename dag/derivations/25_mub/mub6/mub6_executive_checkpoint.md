# MUB(6) executive research checkpoint

AuthorityEffect: None. Date: 2026-10-10, America/New_York.
Verdict: NO-GO for the requested completed publication package.
The full Option B goal remains active and incomplete.

## Custody and scope

Worktree: `C:/Users/a343o/.codex/worktrees/main-sync/the_symbol_game`.
Branch: `codex/mub6-publication-closure`.
Starting remote-main SHA: `4e4bb6ce92a64981d03861d25eae343164288432`.
Remote main subsequently advanced to `25160b260b95d1e34781add75855320b43568c07`
and then `79fd9db728055deb001b7618e321f86e9ed4f97c` (observed 2026-10-10). The current experiment retains its starting source revision;
these results do not cover the later upstream Rust edits.
The commit containing this report is the revision receipt; source-byte bindings
are recorded in `artifacts/mub_option_b_checkpoint_receipt.json`.

Lean is pinned to `leanprover/lean4:v4.33.1` and mathlib to
`0df444a360eaa60ab8c11dca51a86af692955474`. The initial root-directory launch
selected the separate Lean 4.34.1 environment and was stopped. Current formal
commands run from `lean4/research_programs/mub6/` in the pinned environment.

## What is established in the checked formal setting

These are statements with their actual types, not a dimension-wide MUB theorem.
The printed dependencies for the changed results are within
`[propext, Classical.choice, Quot.sound]`. The transitive dependency audit also
passed for all 142 local modules and 14,752 owned declarations, with zero
violations.

| Result | Supported mathematical content | Boundary |
|---|---|---|
| `alpha2_is_odd`, parity cancellations, Tao norm calculation | Finite integer identities and the declared Tao phase-table norm of nine. | No general complex-matrix Conjecture 2 or Proposition 4.2. |
| `no_complete_mub6_of_fourier_triple_landing` | Abstract complete-family contradiction from a certified constituent-triple landing. | Landing and concrete matrix interpretation remain required. |
| `certified_point_in_cover56_iff` | Certified membership is geometric membership plus the separately supplied curvature certificate. | The certificate is not computed from the stored depth label. |
| `projector_interface_nonempty`, `not_universal_interface_exclusion` | The current incomplete projector interface has a zero-action model for every pair of size labels. These two results have no axiom dependencies. | This is an interface countermodel, not a concrete quantum configuration. |
| `rationalMomentMatrix_principal_submatrix`, `rationalMomentMatrix_rank_mono` | Word-preserving inclusion identifies an actual rational principal submatrix and gives rank monotonicity. | Actual rank equality, MUB relation compatibility and operator extraction are not obtained. |

`ConcreteMubProjectors.lean` now gives a forward construction of actual
complex projectors from `FiniteComplexMubFamily ι B ι`. Its seven checked results
establish self-adjointness, same-basis products, completeness, trace one, rank
at most one, rank one and the MU cross-trace equation. All printed dependencies
are in the permitted set. A supplied family is still required; no MUB family or
moment extraction is obtained from this construction.

`ConcreteMubMoments.lean` extends this forward construction to actual complex
word moments. Complete, nonduplicate degree-one/two words give Gram matrices,
positivity and principal inclusion. For a state chosen from one supplied basis
and a distinct MU basis, the singleton columns span the coordinate space.
Both moment matrix ranks equal its cardinality, and
`concrete_mub_moment_flatness` derives the equality. The family, basis labels,
state label and distinctness premise are explicit; rank equality is not an input.
No family is extracted from abstract moment data by this result.

`ConcreteMubPolynomials.lean` supplies an actual polynomial system in 72 real
candidate coordinates: 108 MU residuals and 72 real/imaginary orthonormality
residuals. The 180 constraints need not be independent. Exact evaluation
identities bind them to complex overlaps, candidate unitarity and projector
cross-traces. Their generated ideal is identified with the evaluation-kernel
condition. The actual real zero set is nonempty exactly when a unitary fourth
basis with those overlaps exists; a supplied complete family gives such a point
for its first three bases. No emptiness or reverse moment extraction follows.

`FlatMomentProjectorExtraction.lean` gives a finite reverse construction from
normalized complex word values, actual degree-two positivity, actual flat rank
equality, and contextual idempotence equations for every generator. It derives
nullspace stability and uses the quotient/range equivalence to construct linear
actions. A common Gram factor yields one finite complex space, one normalized
state and linear idempotents symmetric for the explicit finite Hermitian
pairing. `extract_word_projectors` reproduces every complete degree-two
word-matrix entry. The dimension equals the degree-one matrix rank. Operators
and a state are outputs, with no preconstructed operator input fields.
`concrete_moment_extraction_inputs` checks compatibility with the forward
moments of a supplied MUB family.

`FlatMomentBasisRelations.lean` adds contextual same-basis product and
completeness equations for every pair of words of length at most one.
`extract_word_basis` derives the complete orthogonal product rule and each
basis's identity sum on the same common space, while retaining symmetry,
normalization and every degree-two entry. The equations remain explicit inputs;
positivity and flatness alone do not supply them. Supplied concrete-family
moments satisfy all of them through `concrete_moment_basis_inputs`. The
normalized assignment that is zero on nonempty words fails completeness.
Dimension six, nonzero rank-one outcomes, cross-basis MU, full star-algebra
extension and coordinate-variety transport remain open for arbitrary word data.

`CommutativeFlatMoments.lean` supplies a separate direct real-coordinate
construction. The lower matrix indexes the constant and all coordinates; the
upper matrix also indexes every ordered quadratic product. Repeated monomials
are retained. From a normalized real linear functional, actual positive
semidefiniteness and actual rank equality, it constructs symmetric commuting
multiplication operators on the finite lower-column space, a normalized state,
and one common real point. A visible joint eigenvector supplies that point.
Every quadratic polynomial whose square has zero moment vanishes there.
Operators, the state and the point are derived from the Gram/rank data.

`ConcreteMubFlatExtension.lean` checks that all 180 residuals are quadratic.
The finite relation equations imply square-annihilation of every residual;
therefore one extracted point annihilates them all. The exact hypotheses are:

```lean
Λ : Poly →ₗ[ℝ] ℝ
hnorm : Λ 1 = 1
hflat : (momentTwo Λ).rank = (momentOne Λ).rank
hrel : ∀ e : EquationIndex, ∀ i : Two (σ := Coord),
  Λ (twoPolynomial i * equationPolynomial T e) = 0
hM : (momentTwo Λ).PosSemidef
```

`fourth_basis_of_positive_flat` outputs an actual complex unitary candidate
with all 108 MU overlap conditions for the fixed triple. Evaluation at any
actual solution supplies normalized positive flat moments with both ranks one,
and satisfies the finite relation equations. Thus
`fourth_basis_iff_positive_flat_moments` gives a two-way existence equivalence.
`moment_nonpositive_of_empty_variety` excludes positive semidefiniteness when
the fixed real variety is empty, retaining normalization, rank equality and
finite relation compatibility. The conclusion concerns those compatible flat
coordinate moments. No identification with the rational or noncommutative word
APIs, arbitrary-nonflat exclusion, or variety emptiness is asserted.

The exact cyclotomic Python fixture also checks a concrete obstruction to the
proposed trace frame potential: column rephasing preserves orthonormality/MU and
changes the normalized trace fourth power from zero to 36. It is an exact
arithmetic test, rather than a Lean theorem about all basis families. A second
fixture exhibits a Fourier $2\times2$ cross ratio whose fourth power is not one;
the fourth-root entry condition proposed in the briefing does not define the
ordinary Fourier family.

## Remaining premises and frontiers

### Route C

The old theorem still takes

```lean
h_landing : CompleteMUB6 → RouteCCompleteMUBFamily
```

The smaller premise is

```lean
∀ (B : Fin 7 → Basis), PairwiseMU B →
  ∃ (T : MUTriple), InConfig T B ∧ InFourierDitaChart T
```

It removes unneeded orbit counts from the contradiction. `InFourierDitaChart`
already requires certified analytic membership. No derivation of that membership
from arbitrary concrete complex MU matrices is available here. The count
`n_dita + pairCombinations n_dita ≥ 15` is a consequence of a supplied
natural-number partition, without a transition-matrix membership map.

### The 56-cell and cusp calculation

The exact remaining premise is

```lean
CertifiedPointInCover56 cover pt ↔
  GeometricPointInCover56 cover pt ∧ HasCurvatureCertificate pt.triple
```

No current run has emitted the required 56 rational domain/Jacobian/Krawczyk
records or the three cusp-collar records. The same-named binary now supplies `--inspect-system` for the exported joint
system. This is an interval inspection mode, without a depth-64 contractor or
complete cell/cusp run; the square-quadratic contractor remains a library module. The
historical terminal receipt has aggregate labels, not those missing per-cell
data. A concrete system/chart encoding, complete candidate coverage and sound
exclusion reflection must precede removal of the curvature premise. Strict
Krawczyk inclusion requires an applicable existence theorem for a root conclusion;
overdetermined inclusion alone is insufficient. Exclusion requires a sound
disjointness or infeasibility argument.

The Lean root-certificate structures already contain a root and uniqueness
proof. Their existence lemmas project those fields; no analytic contractor
soundness is derived from the inclusion field alone. The separate native deltoid
cover restricts candidates to `|U[0,0]|^2 >= 81/100`. Every candidate unbiased to
the standard basis has `|U[0,0]|^2 = 1/6`, outside that box. Its `37249/90000`
margin does not address the required candidate coverage.

The source two-circulant construction is now checked in
`SzollosiTwoCirculant.lean`. The actual block Gram identity and normalization
yield a complex unitary matrix whose entry moduli squared are one sixth.
Four unit phases with one complex compatibility equation are equivalent to
six scalar real polynomial equations in eight coordinates. Every solution lies
in the rational unit box. `parameter_covers_intersection` connects all phase-sum
image preimages to those equations, without a distinct-root selection premise.
The source is [Szöllősi, arXiv:0811.3930v2](https://arxiv.org/pdf/0811.3930v2).

`SzollosiQuartetSystem.lean` retains both additional bases as arbitrary complex
matrices. Its checked candidate-equation equivalence retains all 144 real
coordinates; standard-basis unbiasedness bounds every coordinate in the rational
half-unit box. Conjecture 3 concerns arbitrary quadruplets containing a family
member, as stated in [Matolcsi et al., arXiv:2503.14752](https://arxiv.org/pdf/2503.14752).
A chosen Zauner triplet does not supply coverage of arbitrary third bases.
The exact remaining empty-variety target in the constructed block gauge is:

```lean
∀ r, (∀ e, MvPolynomial.eval r (parameterPolynomial e) = 0) →
  ∀ U, U.conjTranspose * U = 1 → PairMU 1 U → PairMU (parameterMatrix r) U →
    polynomialVariety (triple (parameterMatrix r) U) = ∅
```

`no_quartet_iff_all_varieties_empty` checks the fixed-parameter equivalence.
No such variety emptiness is supplied. The 56 stored scalar intervals still
have no map covering the full phase domain and all candidate bases.

`SzollosiQuadraticSystem.lean` now specifies 618 rational equations on 440 real
coordinates. Its `equation_degree` bounds every total degree by two.
`exists_solution_with_parameters_iff` gives the actual quartet/solution
correspondence at each admissible phase parameter, while
`exists_solution_iff_quartet` gives the full existence equivalence. Three raw
basis matrices and three auxiliary cross-product matrices retain both additional
bases without choosing a third basis. Cross-product norm-square target six is
consistent with the raw sqrt-six scaling.

`solution_in_full_box` and `exists_bounded_solution_iff_quartet` check a containing
rational box: phase and raw-basis coordinates have radius one, auxiliary
cross-product coordinates have radius three. The exact remaining algebraic
condition in this constructed block gauge can therefore also be written:

```lean
¬ ∃ r : MUB.SzollosiQuadraticSystem.Variable → ℝ,
  ∀ e, MUB.SzollosiQuadraticSystem.realEval r
    (MUB.SzollosiQuadraticSystem.equationPolynomial e) = 0
```

No such emptiness is established. `SzollosiExecutableSystem.lean` now supplies
all 618 executable expressions with checked polynomial/evaluation semantics and
complete ordered IDs for the 440 coordinates. Independent JSON exports match
byte for byte; the input raw SHA-256 is
`1367d390da36e5ccf65abbc8fbf529ff07f9e154c277bb14c1cd8c36ba24c947`.
Native inspection compiled 5,128 sparse terms of degree at most two, matched
1,854 rational probe values and emitted all 618 residual intervals with status
`UNRESOLVED_FULL_BOX`. Its receipt reproduced byte for byte. Finite probes do
not establish native symbolic parity for every real assignment.

`SzollosiIntervalExclusion.lean` derives rational AST interval enclosure for
all contained real assignments and connects successful residual zero-exclusion
to absence of actual polynomial solutions in a box. The full-box Boolean
reduces to false inside the kernel. Its computed phase-interior example excludes
an off-domain box with no admissible unit phase; it excludes no admissible
quartet.

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

`RectangularQuadraticExclusion.lean` now supplies a rational rectangular
Krawczyk exclusion method. `list_derivative_polynomial` identifies the computed
derivative expressions with formal partial derivatives. The exact quadratic
midpoint secant identity yields `root_in_image`: every zero in the input box lies
in its image for any rational preconditioner. No inverse or square projection is
required. Strict separation in one coordinate gives `exclusion_sound`; endpoint
contact is retained. A checked three-equation, two-coordinate example separates
a coordinate even though every natural residual interval contains zero.
A second checked example has strict image inclusion and no common root, so
strict inclusion alone supplies no root conclusion for an overdetermined system.

`SzollosiRectangularExclusion.lean` derives coefficient shape from the checked
native table and retains all 618 equations and 440 coordinates.
`derivative_enclosed` encloses formal derivatives of the actual coded quartet
polynomials. `no_solution_in_box_of_check` applies each successful leaf check to
actual polynomial solutions; `no_quartet_of_check` applies a successful containing-
box check to actual quartets. Both require an actual successful rational check
and a center inside the box. No successful quartet-domain exclusion or complete
56-cell/cusp run is supplied.

The native rectangular command now emits the full containing-box request,
all 618 sparse Jacobian rows (9,000 entries), 440 images and intersections.
Its deterministic preconditioner has 28 nonzero rational entries. The zero
center lies in the containing box and need not satisfy the phase equations.
The output in `artifacts/mub_szollosi_rectangular_native_receipt.json`
(raw SHA-256 `eccd3b1c075d0058cf729e2aa0af5e210860da93d2178ea09a9d5cfb3b820a76`)
is `CONTRACTED_UNRESOLVED_BOX`: 24 coordinates contract and none
separates. These contractions restore constant entries of the constructed family
matrix; none of the 144 raw coordinates of the two additional bases is narrowed
by this run, as checked by `native_additional_bases_unchanged`. The saved request
reproduces the receipt byte for byte.

`SparseRectangularExclusion.lean` derives finite-support image soundness.
`SzollosiRectangularReflection.lean` identifies every emitted derivative
interval and image with the actual polynomial definitions, using bounded row
checks evaluated inside the Lean kernel. `native_jacobian_entry_enclosed`
bounds actual formal derivatives. `solution_in_native_retained` retains every
actual polynomial solution in every recorded intersection. The input box,
zero center, center residuals, contracted-coordinate list and non-separation
are also kernel checked. These checks apply to the current emitted data;
generic Rust/JSON verification is not supplied. No root existence follows.
`SzollosiColumnGauge.lean` now derives an independent column-phase reduction
for both additional bases. It leaves the constructed family matrix and all eight
phase coordinates fixed, and preserves the raw unitary, unit-entry and all three
MU Gram-norm equations. Conjugating each additional basis's first-row entries
sets that row to one. The same 618-equation system therefore has a representative
with 24 prescribed real coordinates whenever a quartet exists, also at every
fixed admissible family parameter. These coordinates are wire IDs 80-91 and
152-163, with alternating real value one and imaginary value zero; their complete
ordered list is checked by `gaugePointCodes_checked` using `by rfl`.
`gauge_box_firstRow` derives the first-row equalities from point-box membership;
`exists_gauge_box_solution_with_parameters_iff` gives the exact existence
reduction with no separate gauge premise. The bounds are exported in
`artifacts/mub_szollosi_column_gauge_box.json`. This normalizes columns of the
two variable bases; it does not classify or fully dephase the family matrix.
The earlier full-box contractor receipt is unchanged. No quartet-domain
exclusion or complete cell/cusp coverage follows from this reduction.

`SzollosiGaugeBalance.lean` derives row and column sums of six for the
raw transition between the two additional bases after the column gauge.
`SzollosiGaugedExecutable.lean` retains all 618 original equations and appends
24 gauge equations and 24 derived balance equations. The resulting 666
quadratics use the same 440 coordinates and preserve quartet existence at
every fixed admissible family parameter. The balance equations are conclusions
of the original equations and gauge, rather than new assumptions on quartets.
The Lean export and native replay agree on all 666 coefficient rows, 5,320
sparse terms and 1,998 rational probe values; the first 618 rows are unchanged.

`SzollosiGaugedCover.lean` checks a six-chart solution cover: at least one
real entry in the first transition row is at least one, since that row sums
to six. The six charts overlap. `SzollosiGaugedReflection.lean` connects the
actual native chart bounds to every augmented-system solution, also at each
admissible family parameter, using the earlier checked retained-box theorem.
Both additional bases remain variable. Duplicate native runs on all six
charts return `UNRESOLVED_BOX`; none of these charts has been excluded.

A separate candidate box restricts all six real entries of that transition row
to [-1/2,1/2]. Its balance equation forces the first real entry into [7/2,17/2],
separated from its own input interval. The native receipt
`artifacts/mub_szollosi_balance_exclusion_receipt.json` records this image
at coordinate 368. Kernel checks bind the 48 added coefficient rows and all
440 input bounds; the selected image has independent real semantics from the
balance identity. A contained point has admissible phases (1,-1,1,i), so this
box's exclusion is not an off-phase-domain example. That point is not a
quartet. The result excludes this candidate box, without excluding all
candidates at any family parameter. Other newly emitted images and the generic
Rust/JSON runtime are not verified by this selected-image result. The new
root replay fixes 48 coordinates (24 constructed-family constants and the 24
column gauges) with 74 nonzero preconditioner entries. It remains unresolved.
Six candidate charts do not replace the required 56 family cells and three
cusp collars, and `HasCurvatureCertificate` remains an explicit premise.

Useful preconditioners, further subdivision, further equivalence transports,
complete parameter/candidate coverage, cusp analysis and curvature remain open.
The native runtime receipt retains its `kernel_reflection_complete: false`
field; the separate checkpoint binds the subsequent Lean checks without
altering the native output.

### Moment positivity and flat extension

`FlatMomentRankCondition E S1 S2` now requires a word-preserving principal
embedding, complete nonduplicate indexing at both degrees, and equality of the
actual rational degree-two/degree-one matrix ranks. Empty index lists cannot
satisfy this condition.
It is a condition to establish, not a flat-extension theorem. The legacy
`CurtoFialkowFlatExtension` supplies operators and a state; `gns_extraction_theorem`
repackages them. The rank-loop consequence still takes `h_gns_exhaust`, and the
emptiness variants retain their soundness or contradiction arguments.

The zero-action countermodel shows that the legacy exclusion path must use
an adequate complex Hilbert/operator domain with completeness, rank one,
dimension and MU relations. The new concrete projector construction provides a forward target for that
bridge. The new `ConcreteMubMoments` construction now establishes normalized
Hermitian word moments, positivity and actual flatness in the forward direction
from a supplied family. The rational API remains separate. The new finite
reverse construction handles normalized complex positive flat word values with
contextual idempotence, and reproduces their complete degree-two matrix through
a normalized state and symmetric linear idempotents. With the added contextual
same-basis and completeness equations, the extracted actions now satisfy
complete orthogonal basis relations. Dimension-six, nonzero rank-one outcomes,
cross-basis MU and full star-algebra extension for arbitrary input data remain
open on the noncommutative word route. The direct real coordinate route now
constructs an actual unitary fourth-basis candidate from normalized positive
flat moments and finite compatibility with all 180 residuals. Its empty-variety
consequence is checked without preconstructed operator or point fields. The
remaining mathematical work includes the required variety emptiness and full
parameterized-family coverage. Algebraic variety emptiness alone does not
establish nonpositivity of an arbitrary nonflat truncation; actual flatness,
normalization and finite relation compatibility remain explicit premises.

## Validation checkpoint

| Gate | Current result |
|---|---|
| Python suite | All 103 tests passed in 73.30 seconds with a fresh writable temporary directory. |
| Changed moment module | `lake build +MomentPositivityObligation` passed, 1840 dependency jobs; new theorem axiom lists checked; focused all-declaration audit passed for 454 declarations. |
| Continuous phase family and variable quartet | Targeted build passed, 8721 dependency jobs, with no warnings in the two new modules. The actual block Gram/normalization, six real parameter equations, phase-sum image coverage, variable-basis equivalence and rational candidate bounds have permitted foundational dependencies. No variety emptiness or native full-domain exclusion is claimed. |
| Joint rational quadratic specification | Targeted build passed, 8722 dependency jobs. The 440-variable, 618-equation specification has checked two-way quartet semantics and a containing rational box; its executable representation and interval scope are recorded below. |
| Executable quartet replay | Targeted Lean build passed, 8723 dependency jobs. Every expression has checked real polynomial semantics; native replay matched 1854 rational probe values and returned `UNRESOLVED_FULL_BOX`. Export and native receipt reproduced byte for byte. |
| Complete native data reflection | All 618 coefficient rows, 5,128 terms and 618 interval rows have kernel-checked identity and real enclosure semantics. Two literal mutations were rejected. Full-box status remains unresolved. Generic Rust/decoder verification and the complete frontier calculation remain open. |
| Rational interval soundness | Targeted build passed, 8724 dependency jobs. Real AST interval enclosure and zero-exclusion soundness are checked. Full-box exclusion reduces to false; the computed phase-interior example is off domain. Two semantic mutations were rejected. |
| Real coordinate flat-extension bridge | Targeted build passed, 8720 dependency jobs. Symmetric commuting multiplication operators, common real-point extraction, the 180-residual bridge, fourth-basis equivalence and empty-variety positivity exclusion have permitted foundational dependencies. The new modules emit no compiler warnings. |
| Changed Route C / A12 / synthesis modules | Combined targeted build passed, 2109 dependency jobs; printed dependencies within the permitted set. |
| Full `lake build Mub6` | Passed for all 142 local modules, 8848 dependency jobs. |
| All-declaration axiom audit | Passed for 142 local modules and 14,752 owned declarations; zero disallowed dependencies. Prior audits, including the 137-module checkpoint, remain byte-bound. |
| Active source-token scan | 142 local modules scanned; zero active `sorry`, `admit`, or custom axiom declarations. |
| Full Rust suite | Fresh full serial command: 335 passed, zero failed, 18 ignored, zero filtered, 2211.19 seconds, exit zero. The uncaptured log has zero observed panic events. Seventeen focused native tests and nineteen new adversarial wire-boundary tests passed. The latter include complete generated-source reproduction. All 2,507 frozen native source/fixture inputs were rechecked; historical Rust logs remain byte-bound. |
| Manuscript quartet rendering | Strict KaTeX 0.16.47 passed: 77 main-manuscript and two changelog expressions; ledger/plan have no math delimiters. The polynomial and forward-moment sections were also inspected visually with local fonts. |
| Renderer rejection checks | Invalid TeX, unmatched math, conflict markers and unescaped currency were rejected. |
| Polynomial semantic mutation checks | Three modified scratch copies were rejected at the expected Lean obligations: MU target one fifth instead of one sixth, the conjugate-overlap sign reversed, and candidate unitarity omitted. Canonical source passed its build and axiom audit. Two additional joint-model mutations (raw overlap target one instead of six, missing conjugation) were rejected at their semantic obligations. |
| Rectangular exclusion | Exact quadratic midpoint identity, formal derivative bounds and zero retention in the rectangular image checked. All 618 equations and 440 coordinates retained in the actual-system bridge. Three core semantic mutations and two endpoint mutations rejected. Independent kernel controls check the changed endpoint comparisons equal false. Current native Jacobian/image identity and solution retention are checked; no successful quartet-domain exclusion is asserted. |
| Column gauge reduction | Both additional first rows fixed by independent unit column phases, with every family parameter and all 618 equations retained. Exact 24 wire coordinates checked by `rfl`. Duplicate native gauge-box replays match and remain unresolved; these new images are not kernel-reflected. Two nonunit-input boundary controls pass and their false unit-norm conclusions are rejected. |
| Derived balance and candidate charts | All 666 coefficient rows retain the original 618-row system. Six actual native chart boxes retain quartet existence at each admissible parameter; each native replay remains unresolved. The selected phase-admissible candidate box has a checked real balance-image exclusion. Three coefficient/bound/contact acceptance mutations were rejected. Full new Jacobian/image reflection and full family/cusp coverage remain open. |
| Vocabulary | Current quartet prose passes the requested vocabulary scan, excluding literal code identifiers. |
| Historical archive | 474 extracted members match raw hashes; 477 manifest entries match; independent rebuilds reproduce the archive digest. |

The completed pre-repair Rust command had 317 passed, zero failed and 18
ignored in 2,493.52 seconds, with one expected panic. The typed `NegativeDelta`
repair retains the negative-radius test and adds a zero-radius boundary check.
An earlier interrupted run observed a deep-run failure whose cause remains
unknown; another retry ended without a terminal summary. Those outcomes and
raw logs remain bound in the receipt, separate from the current rerun.

Runtime logs remain under ignored `scratch/mub6-2026-10-09/`. The tracked checkpoint
receipt binds completed log hashes and source bytes, including the fresh full
Rust result. All 2,507 frozen inputs (2,503 tracked Cargo-workspace Rust source/manifest
files and four system fixtures) match their pre-run raw hashes. This freezes the native source surface;
other imported runtime data remain subject to their own artifact bindings. The 18 ignored tests
did not execute: they require absent external receipts, dedicated large-cover computation, or diagnostic runs. Their exact names and reasons are retained in the receipt. Dependency-job counts are not counts of local modules.

## Receipt and package disposition

R6 raw SHA-256:
`cf8442d8fe1397226d669fcea7bc038ef8d984a9bae741772b9d742fbe62eb59`.
Its status remains `NOT_A_CERTIFICATE`.

Matolcsi receipt raw SHA-256:
`598d73b4f7b6807d62fc8d5c7698fd7c00ca73634c24641e0f2a848c873fc6fa`.
Its internal digest is a different commitment.

Refreshed historical archive SHA-256:
`69c85da557191af915b4cd2298e109adad9f1fd46ed63eb3b807deb718f87c85`.
The archive is 2,132,303 bytes. Its legacy layout excludes the current manuscript
and canonical Lean sources. Its metadata now states `publication_ready: false`.

An arXiv submission claiming completed Option B closure is not supported. A new
Zenodo deposit of the requested complete package is not ready either: the
mathematical frontiers and current-source archive layout remain unresolved.
Execution success does not discharge the remaining mathematical premises. A scoped conditional or negative research checkpoint could be
archived after its own review and packaging gates; open mathematics does not
itself forbid such a deposit. No submission, DOI registration or external deposit
has been performed.

## Next execution and research work

1. Retain the completed full library command and its raw log. All 353 tests were
   indexed; 335 executed and passed, and 18 were ignored. The latter were not
   substituted for the requested 56-cell/cusp research calculation.
2. Retain the completed 142-module all-declaration audit with the source bindings.
   Its command is `lake env lean ../../../omega_engine_projects/mub6/scripts/audit_mub6_axioms.lean`.
3. Improve exact preconditioners and subdivide unresolved boxes, retaining
   every leaf until separation or a justified root branch. The current root run
   restores fixed family entries and derives both additional first-row gauges;
   the six covering candidate chart runs remain unresolved.
   Continue the concrete landing, full analytic cover/reflection and adequate
   operator/flat-extension derivations in the synchronized synthesis plan.
4. Package the actual current sources and manuscript, reconcile metadata, and
   repeat byte/semantic review before any deposit decision.

The derived-balance revision has a fresh full serial Rust run, aggregate Lean build and owned-declaration axiom audit. Their logs, the new kernel controls and the fresh complete Python suite are bound in the checkpoint receipt.
