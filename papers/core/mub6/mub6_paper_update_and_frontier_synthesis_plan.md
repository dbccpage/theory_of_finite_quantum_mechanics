# MUB6 Option B synthesis and completion plan

AuthorityEffect: None. Updated 2026-10-10.
Status: active research; no unconditional MUB exclusion or publication clearance.

## Baseline and integrated changes

Baseline main: `4e4bb6ce92a64981d03861d25eae343164288432`.
PR #659 is merged at `3b981600217df0cbe960ae1a5c49234edf606959`
(2026-10-09 21:24 America/New_York). Its recorded scope includes deterministic
Rust collection repairs and non-tensor Conjecture 2 surveys.
PR #660 is merged at `0c9e95d326b90790a1e9363628ec667a1f61d014`
(2026-10-09 21:31 America/New_York). It adds odd-parity integer polynomial and
monomial identities. Their matrix interpretation remains a separate obligation.
Both merge states were checked through GitHub during this checkpoint.

The tracked `Conjecture2GeneralMechanization.lean` supersedes the old
artifact-missing description. Its presence and finite identities do not change
R6 from `NOT_A_CERTIFICATE` to a general matrix theorem. R7 also retains that
status. The package's abstract basis and operator interfaces require semantic
review alongside axiom auditing.

## Frontier 1: concrete Route C landing

Required result: derive certified Fourier-family constituent-triple membership
from a concrete complete complex MU family, or state the exact remaining
algebraic/analytic premise.

The existing bridge is
`CompleteMUB6 -> RouteCCompleteMUBFamily`.
The new `FourierTripleLandingPremise` drops orbit-count requirements from the
contradiction and retains only a constituent triple with certified chart
membership. It is an explicit premise, not a derived classification.

Next derivations:

1. Define Fourier-family equivalence for actual transition matrices, including
   unitary gauge, row/column phases and permutations.
2. Bind the abstract basis/MU relation and chart membership to those definitions.
3. Establish a landing statement without assuming exhaustive family counts.
   If a premise remains, give its formula, domain and independent evidence.
4. Instantiate the checked gluing implication with those concrete data.

The natural-number partition alone does not produce transition matrices.
The trace-based frame expression depends on column gauge; the entrywise MU
fourth-power sum is fixed at 84 for seven bases. Neither calculation alone
supplies a Fourier membership map. Integer Bianchi identities likewise need a
concrete transition/cochain interpretation.

Completion evidence: kernel-checked concrete bridge, all assumptions printed,
standard foundational dependencies, and a manuscript statement matching the type.

The exact Fourier cross-ratio fixture also rejects identifying Fourier-family
membership with an all-fourth-root entry condition. The proposed trace expression
is phase dependent; the entrywise MU fourth-power sum is constant. Neither route
currently supplies the missing landing derivation.

## Frontier 2: depth-64 56-cell and cusp contractor reflection

Required result: actual native execution for all 56 family cells and all three
cusp collars, rational domain/certificate emission, and a sound Lean derivation
without a caller-supplied curvature certificate.

Existing objects:

- The square-quadratic contractor is `src/omega_native/mub6_smale_sentry.rs`.
  The same-named `src/bin/` inspector now accepts `--inspect-system`; this mode
  supplies no depth-64 contractor or cell/cusp calculation.
- `CertifiedModuliPartitionCover56` carries counts, a depth label and margins.
- `certified_point_in_cover56_iff` exposes geometry plus the separately supplied
  curvature certificate.
- The Lean root-certificate structures already contain roots and uniqueness
  evidence; their projection lemmas do not establish contractor soundness.
- The persisted terminal receipt has aggregate labels but no 56-cell rational
  boxes or Krawczyk images.
- The deltoid-cover candidate box requires `|U[0,0]|^2 >= 81/100`, excluding
  every candidate unbiased to the standard basis (`|U[0,0]|^2 = 1/6`). Its
  `37249/90000` base margin does not supply the missing candidate coverage.

The source block family is now checked in `SzollosiTwoCirculant.lean`.
Its four unit phases and compatibility equation are equivalent to six scalar
real polynomial equations on eight coordinates. The Gram/normalization and
phase-sum image coverage are derived, including repeated-root parameters.
`SzollosiQuartetSystem.lean` retains arbitrary third and fourth bases, checks
the candidate-equation equivalence and bounds each of their 144 coordinates in
the rational half-unit box. The first two bases are the identity and the actual
normalized block matrix. `SzollosiQuadraticSystem.lean` adds 618 rational
quadratic equations in 440 real variables, with two-way quartet semantics both
globally and at each fixed admissible phase parameter. Every solution lies in a
rational box of radius one for phase/raw-basis coordinates and three for
auxiliary cross-product coordinates. `SzollosiExecutableSystem.lean` now exports
all equations as executable expression trees, with checked polynomial/evaluation
semantics and complete ordered IDs. Two exports were byte-identical. Native
inspection matched 1,854 rational probe values and emitted 618 exact full-box
intervals with status `UNRESOLVED_FULL_BOX`. The 5,128 sparse terms have degree
at most two. Finite probe agreement alone does not identify the polynomials.

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

`SzollosiIntervalExclusion.lean` supplies actual interval enclosure and
zero-exclusion soundness for the Lean AST. Its full-box Boolean reduces to false
inside the kernel. A kernel-reduced first-phase interior example excludes an off-domain
box containing no unit phase. The current emitted native interval data are
identified with sound sparse interval semantics above; no full exclusion follows.

The required quantified target covers all admissible third bases, as stated by
`no_quartet_iff_all_varieties_empty`. Checking one Zauner triplet leaves this
quantifier unresolved. The literature formulation is Conjecture 3 of
[Matolcsi et al., arXiv:2503.14752](https://arxiv.org/pdf/2503.14752), using the
family constructed in [Szöllősi, arXiv:0811.3930v2](https://arxiv.org/pdf/0811.3930v2).

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

Next derivations:

1. Retain the checked complete coefficient identity and interval enclosure for
   the current emitted data. Qualify the generic runtime/decoder boundary as
   needed for later inputs. Retain all third/fourth bases and establish the needed
   further gauge and equivalence transports.
2. Use the now-checked rectangular exclusion method in
   `RectangularQuadraticExclusion.lean` and its actual-system bridge in
   `SzollosiRectangularExclusion.lean`. The exact quadratic midpoint identity and
   formal derivative bounds retain every zero without an inverse or square
   projection. All 618 equations and 440 coordinates are retained. The actual
   full-box native run now has kernel-checked Jacobian and image parity in
   `SzollosiRectangularReflection.lean`. It narrows 24 coordinates with 28
   nonzero weights and excludes none. Every actual solution is retained.
3. Generate useful further exact boxes, interval Jacobians, preconditioners and images.
   Exclusion uses strict coordinate separation. Endpoint contact is retained.
   A checked overdetermined example has strict inclusion but no common root;
   any root branch needs the applicable existence theorem and every residual.
4. Check complete parameter/candidate coverage, interfaces and three cusp collars.
5. Reflect the actual rational inequalities and derive their concrete analytic
   meaning in Lean. Boolean reduction alone does not establish this meaning.
6. Replace the abstract `HasCurvatureCertificate` input only after this bridge is
   established. Retain counterexample/root branches when the calculation finds one.

Completion evidence: reproducible native command and exit status, every leaf's
input/output data, full coverage receipt, kernel reflection and soundness theorem.

## Frontier 3: adequate operator domain and flat extension

Required result: actual structured moment matrices for the MUB relations,
positive flat extension and operator extraction, connected to the concrete
variety or to a justified noncommutative SOS emptiness certificate.

The checked zero-action interface countermodel is the first obstruction:
`not_universal_interface_exclusion` has no axiom dependencies. Current
`PhysicalProjectorRealization` omits completeness, rank one, dimension, linearity
and cross-basis unbiasedness. Its exclusion predicate cannot be the desired
concrete MUB conclusion.

The checked `ConcreteMubProjectors` forward construction supplies actual
complex rank-one projectors, completeness and MU trace relations from the existing
complex-family definition. It does not supply a family or extract operators.

The forward rank construction is now checked in `ConcreteMubMoments.lean`.
Actual complex word moments from a supplied family are Gram matrices, hence
positive semidefinite. The normalized state is a vector from one supplied
basis. Every singleton projector from a distinct MU basis produces a nonzero
multiple of that basis vector. These columns span the coordinate space, so
both complete degree-one/two moment matrices have rank equal to its dimension.
The word lists are nonduplicate and complete at both degrees, and the lower
matrix is the declared principal submatrix. `concrete_mub_moment_flatness`
derives the rank equality with no rank-equality input. The rational API remains
separate; no unsupported realification is used.

Next derivations:

1. The coordinate-polynomial and projector-trace bridge is now checked in
   `ConcreteMubPolynomials.lean`: 108 MU residuals plus 72 orthonormality
   residuals in 72 real candidate coordinates. The actual ideal and real zero
   set agree with unitary fourth-basis solutions, and a supplied complete
   family gives a zero-set point. The real coordinate moments below now bind
   all these residuals to a common extracted point. Arbitrary noncommutative
   word data remains a separate model.
2. The finite nullspace/range construction is now checked in
   `FlatMomentProjectorExtraction.lean`. Normalization, positivity, actual
   flatness and contextual idempotence yield a common finite complex space,
   normalized state and linear idempotents symmetric for the finite Hermitian
   pairing. Every degree-two word-matrix entry is reproduced; the dimension is
   the lower moment rank. `FlatMomentBasisRelations.lean` now derives
   same-basis orthogonality and completeness from `ContextualSameBasis` and
   `ContextualCompleteness`, with the normalized representation on the same
   common space. `concrete_moment_basis_inputs` checks both premises for
   supplied-family moments; the zero-action assignment fails completeness.
   Dimension six, nonzero rank-one outcomes, cross-basis MU and transport of
   arbitrary word data remain open on this route. Full star-algebra extension
   is not supplied here. These are not hidden premises of the separate real
   coordinate extraction below.
3. The direct commutative construction is now checked in
   `CommutativeFlatMoments.lean`. Normalized positive real moments and actual
   rank equality give well-defined symmetric commuting multiplication
   operators, a normalized state, and a common real point annihilating every
   quadratic relation whose square has zero moment. The point and operators
   are constructed. Only products of degree at most four enter the argument.
4. `ConcreteMubFlatExtension.lean` checks that the 180 residuals are quadratic.
   `FiniteRelationCompatibility` annihilates every residual times every upper
   monomial, so each residual square has zero moment. The extracted point is
   an actual unitary candidate with all 108 MU overlaps. Evaluation at any
   solution gives normalized positive flat moments; candidate existence and
   existence of such compatible moments are equivalent.
5. The appropriate emptiness consequence is checked:
   `moment_nonpositive_of_empty_variety` retains normalization, actual flatness
   and finite relation compatibility. Establish emptiness for the needed fixed
   triples with complete parameterized-family coverage. Positivity exclusion
   for arbitrary nonflat truncations needs a separate argument; flatness is
   not inferred from a depth label or from positivity alone.
6. A full noncommutative star-algebra extension would be additional research.
   It is not required to apply the checked real coordinate theorem and is not
   inferred from the pinned full-C-star-algebra GNS construction.

Completion evidence: actual matrix/rank construction, checked extraction and
soundness, no custom axioms or placeholders, and no unbound operator fields.

## Publication and execution gates

- Rust: `cargo test -p omega_mub --lib -j 1 -- --test-threads=1`.
- Python: `python -m pytest omega_engine_projects/mub6/tests/`.
- Lean, from the pinned package directory: `lake build Mub6`.
- Source audit: no active proof placeholders/custom axiom declarations.
- Environment audit: every local declaration's transitive dependencies are in
  `[propext, Classical.choice, Quot.sound]`; imports cover all local modules.
- Manuscript: consistent current claims, no conflict markers/placeholders, valid
  rendered math, linked receipts and verified hashes.
- Package: current metadata, licensing, deterministic archive, manifest and
  semantic receipt replay. Existing archive integrity is historical evidence.
- Closeout: executive report, explicit branch/commit/status, and a clean tree.

The executive checkpoint must give a frank NO-GO while any required mathematical,
validation, rendering or package gate is unresolved. Completing a scoped repair
does not complete the full Option B objective.

## 2026-10-10 derived-balance checkpoint

The gauge reduction now has derived transition row/column balance equations.
All original 618 equations are retained in a 666-equation, 440-coordinate system.
At each admissible parameter, the exact native six-chart candidate cover retains
every quartet representative. Duplicate native replays leave every chart
unresolved. One candidate box meeting the admissible phase domain has a checked
balance-image separation; this is not a parameter-fiber exclusion. Full new
Jacobian/image reflection and the 56 family-cell/three-cusp calculation remain
required. Next, improve contraction within these retained charts and subdivide
without discarding unresolved leaves; the actual curvature premise remains open.
