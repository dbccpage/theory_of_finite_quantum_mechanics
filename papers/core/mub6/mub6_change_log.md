# MUB(6) research change log

AuthorityEffect: None.
Checkpoint: 2026-10-11. The three Option B frontiers remain open.

## Version 1.1.1 — 2026-10-16 publication preparation

- Moved all twelve former papers-directory files to the package root; renamed
  paper.md, paper.tex and paper.pdf to mub6.md, mub6.tex and mub6.pdf.
- Normalized the four-line header and narrowed release-level formal claims:
  historical scoped reports are not a complete current Lean replay.
- Replaced the manuscript's raw research-ledger table with an evidence-bound
  mechanism inventory. Retained the ledgers in the research checkout.
- Added Unicode description, bibliography, keywords, reproduction instructions,
  Zenodo metadata and separate full text/code licenses.
- Prepared a manuscript-only preprint archive, excluding historical receipts,
  prompts, ledgers and incomplete formal export files. Historical tarball bytes
  remain unchanged. No external deposit or DOI assignment is claimed.

## 2026-10-16: review on main and the next derivation

- Reviewed this package and the `omega_mub` crate at `main` `156c91d2f`
  (`research/mub6_review_and_next_derivation.md`).
- Withdrew the 2026-10-15 promotions of residuals R6, R7, R8 and R9 in the gap
  registry and the atlas. R6 rests on literal `true` flags and on receipts that
  score model answers; R7 on a separating polynomial built to equal −ε on the
  slice; R8 and R9 on literal `true` flags. R6 and R7 are back at
  `NOT_A_CERTIFICATE`, R8 at `BLOCKED` by R7, R9 at `OPEN`, as the paper and
  this ledger already said. Each registry entry keeps the withdrawn promotion in
  `promotion_withdrawn`.
- Corrected gap G1: the five-class list was quarantined on 2026-10-11, and
  Conjecture 3 and Prop 4.2 are cited from the published version
  (doi:10.1007/s10801-026-01506-x), not arXiv:2503.14752 v1.
- Marked the atlas's native gap solver row as fixture-based: its Φ1 values are
  fixtures and its 13/13 count cannot fail.
- Marked the registry's two discrete covers (Szöllősi deltoid, Karlsson
  volume) as fixture-based: their base term 37249/90000 is read, not computed.
  The Karlsson cover is no longer cited as evidence for R7.
- Reviewed the 19 `omega_mub` modules added on 2026-10-15: 15 return constant
  verdicts; of the four that compute, only the Tao norm (9 on all 20 sign
  patterns) bears on MUB(6). The crate is not edited.
- Added two rows to `research/superseded_notice.md` (G1 elimination receipt line
  14, synthesis line 132). Neither file is changed.
- Added claims MUB6-C40 (Szöllősi common-ray reduction, Lean, owner build) and
  MUB6-C41 (pair exclusion at the special point on the represented rays).
- Named one next derivation: a certified exact-rational cover of the phase
  torus T^5, calibrated at the special point and then at the generic sample,
  then widened to an explicit parameter box. It replaces the elimination step
  L2 of the 2026-10-15 plan, which that plan already named as its fallback.
- Added the two open goals to `plans/goal_dag.jsonl`: `MUB6-SZ-T5-COVER` (the
  certified cover) and `MUB6-SZ-CONJ2-TRIPLES` (the Conjecture 2 identities on
  arbitrary actual triples), both joined to `MS-IMPLEMENTATION-JOINS`, and the
  same two items to the remaining list of `MUB-CLM-001` in the math DAG.
- Recorded that the plans route `MUB6_PILOTS_31_50_ROUTE` names a function
  that returns PASS from constants. The route row is not edited.
- Custody pins left for the owner: receipts changed by `4a0b300ba` are still
  pinned at their old digests. N(6) = 3 remains open.

## 2026-10-16: prompt 05 campaign checks in Rust

- Rebuilt the balanced table in `omega_mub` from its definitions and compared
  it with `artifacts/balanced_quadratic_coefficients_20261011.jsonl` term by
  term over Q: all 648 rows agree. A changed coefficient is named by its row,
  and changed or truncated bytes are refused.
- Ran the negative controls from the campaign checkpoint. A third basis equal
  to the first or to the second makes exactly the 36 transition-modulus rows of
  that pair nonzero, with values in {-6, 30}; every other block vanishes.
- Recorded the box as stated in `def bounds`: [-1, 1] on 170 coordinates and
  ±10035/4096 on the 150 core coordinates, not [-1, 1]^320.
- Computed the Jacobian at the box centre: 1045 linear terms in 269 rows, exact
  rank 184 of 320. It is not zero, so the campaign's Krawczyk lemma (D4) rests
  on a false premise for this table.
- Checked the campaign's fixed-triple lemmas D1, D2, D3, D9, E.1, F.2 and G at
  exact values. D9's count shows 138 of its 180 rows independent of the
  Hermitian and diagonal identities, and lists no row-unitarity row. Statuses
  are recorded at what the code backs, not at the checkpoint's raised statuses
  (`research/prompt05_campaign_checks.md`).
- Added claims MUB6-C38 and MUB6-C39 (exact computation). The Lean equivalence
  `exists_quartet_iff_table` was not elaborated: Mathlib is not reachable in
  this environment. N(6) = 3 remains open.

## 2026-10-11: concrete quartet transport and complex Tao semantics

- Derived simultaneous monomial transport directly from complex matrix Gram
  identities, including normalization of any actual quartet and a bridge to
  the existing concrete quartet predicates. Complete representative coverage
  and exclusion remain explicit inputs to the global reduction.
- Checked both balance residual identities over commutative star rings and
  their ideal-membership corollaries. No Jacobian rank claim follows.
- Connected the integer Tao evaluator to complex column products and integer
  Laurent powers. All twenty balanced masks have squared norm nine.
- Replayed the three scoped targets and 23 local source modules under the
  project pins. All 31 new displayed endpoints use only standard Lean axioms;
  the finite integer-pair comparison uses none. False coefficient and norm
  mutations were rejected. The flat-moment and joint polynomial equivalences
  also passed as dependencies; the complete MUB6 import surface was not rebuilt.
- Pinned the external classification source and checked its public definitions
  and source audit. An out-of-memory failure prevented a complete endpoint
  replay; the failed module subsequently passed with one worker. The resumed
  public target is still pending. This does not discharge classification
  integration or nonextension.
- Added an acyclic 25-node derivation graph covering branches A-F, with six
  explicit routes and open decisive outcomes. Recovered dependency Git custody
  in an owned scratch pool and checked all eighteen pinned source trees.

## 2026-10-11: exhaustive Tao sign patterns and corrected derivation boundary

- Added kernel-checked integer phase-table evaluations for all twenty balanced
  sign masks and for every choice of three distinct positive row indices.
  The four new theorems have no axiom dependencies under Lean 4.33.1.
- Distinguished the twelve-dimensional column-phase group from twenty-four
  prescribed real coordinates and the remaining 120 ambient coordinates for
  a fixed first Hadamard. Added an explicit polynomial balance-residual identity.
- Quarantined the inherited five-family classification and unspecified Haagerup
  ceiling. Pinned primary sources distinguish the full three-parameter Karlsson
  family, a reported 2026 finite-corner classification, and open quartet exclusion.
- Added a derivation checkpoint and dependency graph under `research/`, with
  the operational recommendation CONTINUE TARGETED SOLVE. No global upper bound,
  external formalization replay, or publication readiness follows.

## 2026-10-09: manuscript reconciliation and premise audit

The current manuscript, ledger and synchronized synthesis plans replace the
conflicted manuscript and earlier unconditional Route C interpretation. The
baseline for this revision is commit
`4e4bb6ce92a64981d03861d25eae343164288432`. Detailed earlier campaign entries
remain available in Git history; the bounded record below supersedes their
mathematical and publication interpretations.

- Removed committed conflict markers and unsupported claims of dimension-wide
  closure. The current manuscript distinguishes finite arithmetic, abstract
  implications, concrete mathematical interpretations, and publication custody.
- Reconciled G1-G5: G1 open, G2/G4 conditional, G3 partial, and G5 open with a
  countermodel to its present interface. The four-part envelopes state supported
  statements, excluded interpretations, narrow claims and next required evidence.
- Added `FourierTripleLandingPremise` and its conditional obstruction theorem.
  This removes orbit counts from the needed certificate interface; certified
  constituent-triple landing remains an explicit premise.
- Added `certified_point_in_cover56_iff`. The current certified membership
  predicate is geometry plus the separately supplied curvature certificate.
  The depth label and aggregate historical receipt are not a native 56-cell run.
- Added an exact cyclotomic gauge counterexample to the proposed trace-based
  frame potential. Column rephasing preserves MU and changes the normalized
  trace fourth power from $0$ to $36$. A second fixture exhibits a Fourier
  cross ratio outside fourth roots. The entrywise MU sum does not identify
  Fourier-family transition matrices.
- Added `zeroActionInterfaceModel` and the axiom-free interface non-exclusion
  theorem. The weak projector structure omits completeness, rank one, concrete
  dimension, linearity and cross-basis MU constraints.
- Added actual rational word-moment matrices, a word-preserving principal
  embedding, the principal-submatrix identity and rank monotonicity.
  `FlatMomentRankCondition` requires complete, nonduplicate word indexing and
  equality of actual ranks; empty lists cannot satisfy it. A compatible
  positive MUB moment sequence and operator extraction remain open.
- Added the aggregate `Mub6` target importing all 110 local Lean modules, and an
  all-declaration transitive axiom auditor with an explicit foundational allowlist.
  Build completion and axiom-audit results belong to the execution report.
- Reconciled R6 with the tracked mechanization. Its receipt retains
  `NOT_A_CERTIFICATE` and raw SHA-256
  `cf8442d8fe1397226d669fcea7bc038ef8d984a9bae741772b9d742fbe62eb59`.
- Withdrew release approval metadata. The refreshed legacy archive has 474 file
  members and 477 manifest entries. Its layout excludes the current manuscript
  and canonical Lean source tree; integrity checks do not complete the requested
  publication package. No external submission or deposit has been made.

## 2026-10-09 merges: deterministic Rust review and parity lemmas

PR #659 merged at `3b981600217df0cbe960ae1a5c49234edf606959` on
2026-10-09 21:24 EDT. Its Rust review includes deterministic `BTreeSet`/`BTreeMap`
collections and anti-pattern remediation, plus non-tensor family survey work.
Those changes are integrated in the baseline; the current full-suite run is
independent validation, not an inference from the merge.

PR #660 merged at `0c9e95d326b90790a1e9363628ec667a1f61d014` on
2026-10-09 21:31 EDT. Its odd-parity polynomial and monomial lemmas are finite
integer identities. A matrix interpretation is still needed before applying
them to arbitrary Hadamard cube slices.

The later removal of the warning banner changes prose. It discharges no
classification, landing, analytic or moment premise. The former Phase 6K
statement of unconditional complete-family exclusion is withdrawn.

## 2026-10-01: R6 and R7 receipt status

`Conjecture2GeneralMechanization.lean` is present and tracked. Its parity,
anti-parallel cancellation, Tao phase-table and finite class-table statements
must be read with their actual types. `AnalyticCubeSliceCertificate` supplies row
bounds and compatibility fields. General matrix Conjecture 2 and Proposition 4.2
are not established by naming the module or evaluating its finite table.

R6 and R7 retain `NOT_A_CERTIFICATE`; G1 remains open and R8 depends on R7.
The R6 receipt generator refuses to overwrite the committed receipt. The earlier
Phase 6I description of an accepted singular-Segre certificate is withdrawn.

## 2026-09-23 to 2026-09-27: conditional assembly and archive custody

The earlier SDP, cochain, interval and gluing campaigns supplied scoped routines
and conditional interfaces. Input rank labels, certificate Booleans, endpoint
interpolations and chart membership do not supply their missing concrete
mathematical bridges. The former release approval label is withdrawn.

## 2026-06 to 2026-09-18: finite fixtures and regional calculations

The historical Diță, Szöllősi, Karlsson and discrete-family work remains regional
or finite evidence at this checkpoint. No exhaustive complex Hadamard
classification or complete continuum cover is inferred from those campaign
names. Exact source and receipt dependencies are recorded in the current ledger
and synthesis plan.

The candidate-domain audit identifies that the deltoid cover uses a box with
`|U[0,0]|^2 >= 81/100`; unbiased candidates have `|U[0,0]|^2 = 1/6` and lie
outside it. The fixed `37249/90000` margin does not address that coverage gap.

## 2026-10-10: concrete projector forward construction

Added `ConcreteMubProjectors.lean`: actual outer-product matrices of a supplied
finite complex MUB family satisfy self-adjointness, same-basis products,
completeness, trace one, rank one and the MU cross-trace equation. All seven
printed theorem dependencies lie in the standard foundational set. This does
not establish a family or extract it from truncated moments. The remaining
moment bridge needs complex Hermitian moments or a justified realification;
the current rational API covers rational fixtures.

## 2026-10-10: forward complex moment rank equality

Added `ConcreteMubMoments.lean` to the full aggregate. From a supplied complex
MUB family, a state label in one basis and a distinct basis, the module derives
normalized complex word moments, their Gram identity and positivity, complete
nonduplicate degree-one/two word lists, principal inclusion, full column ranks,
and `concrete_mub_moment_flatness`. No rank-equality field is assumed. The
reverse extraction and the 108-polynomial variety bridge remain open.

The 110-module axiom audit completed with 10,884 declarations and zero
violations. After adding the moment module, the 111-module aggregate and
transitive axiom audit passed: 8,817 dependency jobs and 10,936 declarations,
with zero disallowed dependencies. The audit now caches the import-name array and flushes progress;
its allowlist and transitive dependency scope are unchanged. The full Rust
command completed with 317 passed, zero failed and 18 ignored in 2,493.52 seconds.
The execution receipt retains the ignored tests and earlier failed-attempt history.

The uncaptured full Rust log included one expected panic from the existing
negative widening-radius test. That harness pass does not meet the literal
zero-panics requirement. `widening_error_bounds` now returns
`Result<WideningScopeBounds, WideningBoundsError>` with typed `NegativeDelta`.
The negative-input test checks that refusal and the added zero-radius test
checks the boundary. This change requires a fresh full Rust run; its completed
pre-repair log remains bound in the checkpoint receipt.

The focused seven cover tests passed with zero panic events in 0.50 seconds.
The repaired-source full Rust run is active; the zero-panics gate remains pending
until its terminal result is recorded. The refreshed Python suite passed all
71 tests in 18.26 seconds. The current quartet renders under strict KaTeX:
43 main-manuscript expressions and two change-log expressions.

## 2026-10-10: concrete coordinate-polynomial and variety bridge

Added `ConcreteMubPolynomials.lean`: 72 real coordinates for an actual complex
candidate matrix, 108 MU polynomials, 72 candidate-orthonormality polynomials,
their generated ideal, exact evaluation and projector-trace identities, and the
real-zero-set/fourth-basis equivalence. A supplied complete family gives a point
in that zero set for its first three bases. The 180 indexed constraints are not
asserted independent. Emptiness and reverse extraction from abstract positive
flat moments remain open.

The expanded full Lean build passed with 112 local modules and 8,818 dependency
jobs. Its transitive axiom audit checked 10,998 declarations with zero violations.
The dependency cache's missing empty Git refs directories were restored, and
all nine dependency HEADs and tracked trees were revalidated against the pins.
The repaired-source full Rust run remains active.

The manuscript distinguishes the one-parameter B6 subfamily from the full
two-parameter deltoid-intersection family using arXiv:0811.3930v2. The current
56 scalar intervals have no coverage map for the latter. The plan also records
the pinned mathlib GNS theorem's full-positive-functional requirements; it
cannot be used as a truncated degree-two extension by its name alone.

Three semantic mutation checks rejected modified scratch copies at the expected
Lean obligations: changing the MU target from one sixth to one fifth, reversing
the conjugate-overlap imaginary sign, and omitting candidate unitarity. Their
modified source bytes, diagnostics and runner are bound separately from the
successful canonical build and axiom audit. The refreshed Python suite passed
71 tests in 15.62 seconds. Strict rendering passed with 48 main-manuscript and
two change-log expressions; the new polynomial and moment sections were also
inspected visually with local fonts.

The repaired-source full Rust command completed at 2026-10-10 06:05:41 UTC:
318 passed, zero failed, 18 ignored, zero measured, zero filtered, 2,406.33
seconds, exit zero. The uncaptured log has zero panic events. The 18 ignored
tests did not execute; their names and recorded external-input, large-cover,
or diagnostic reasons are retained in the receipt. The default full library
command's passing result does not supply the missing 56-cell/cusp certificates.

## 2026-10-10: finite reverse word-moment extraction

Added `FlatMomentProjectorExtraction.lean`. Its input is normalized complex word
values, the actual positive semidefinite degree-two matrix, actual flat rank
equality, and contextual generator idempotence. It constructs a Gram factor,
a common finite complex range, a normalized state and linear idempotents
symmetric for the finite Hermitian pairing. Every complete degree-two word
matrix entry is represented, and the dimension equals the lower matrix rank.
No operator or state is an input field. The concrete supplied-family moments
are checked to satisfy these premises. The targeted build passed with 8,718
dependency jobs and only the permitted foundational dependencies.

This finite reverse construction does not discharge dimension-six, rank-one,
completeness, orthogonality, MU, full star-algebra extension or coordinate-variety
transport for arbitrary moment data. The 56-cell/cusp reflection and the
remaining Route C premise remain open.

The expanded full aggregate passed for all 113 local modules, with 8,819
dependency jobs. The full transitive audit checked 11,048 declarations with
zero disallowed dependencies. Earlier 112-module logs remain preserved. The
repaired Rust full-library command is complete with zero failures and zero
panic events; its 18 ignored tests remain disclosed.

The final Python suite passed all 71 tests in 10.40 seconds after the final
archive refresh. Strict KaTeX rendering passed with 51 main-manuscript and two
change-log expressions. The source scan covers 113 local Lean modules with
zero active placeholders or custom axiom declarations, and the two synthesis
plan copies are byte-identical.

## 2026-10-10: complete orthogonal actions from flat moments

Added `FlatMomentBasisRelations.lean`. Explicit contextual same-basis product
and completeness equations, together with normalized positive flat complex
word data, yield complete orthogonal symmetric basis actions on the common
extracted space. The normalized state and every degree-two matrix entry are
retained. The space dimension equals the lower matrix rank. Operators and a
state are constructed; the contextual relations remain explicit input premises.

`concrete_moment_basis_inputs` checks those premises for supplied concrete-family
moments. `zero_action_moments_reject_completeness` rejects the normalized word
assignment that is zero on every nonempty word. The existing exact word-state
coordinate proof was factored into reusable lemmas without changing the prior
extraction statement. Dimension six, nonzero rank-one outcomes, cross-basis MU,
full star-algebra extension and transport to the coordinate variety remain open.
The Route C landing and complete 56-cell/cusp reflection also remain open.

The canonical targeted build passed with 8,719 dependency jobs. All printed
dependencies are in the permitted foundational set. The full build, transitive
audit and refreshed execution totals are recorded in the executive checkpoint
and byte-bound receipt for this revision.

The full build passed for all 114 local modules, with 8,820 dependency jobs.
The transitive audit checked 11,065 declarations with zero disallowed axioms;
the source scan found zero active placeholders or custom axiom declarations.
All nine dependency pins and tracked trees were revalidated. Prior 113-module
logs remain preserved. The refreshed Python suite passed 71 tests in 18.02
seconds. Strict rendering passed with 55 main-manuscript and two changelog
expressions; the plan copies remain byte-identical. The unchanged Rust sources
retain the completed full result: 318 passed, zero failures, zero panic events,
and 18 ignored tests. No new full Rust execution is claimed for this revision.

## 2026-10-10: real positive-flat moments reach the candidate variety

Added `CommutativeFlatMoments.lean` and `ConcreteMubFlatExtension.lean`.
The construction starts with a real linear functional and actual constant/linear
and constant/linear/ordered-quadratic moment matrices. Normalization, positivity
and actual rank equality yield well-defined symmetric commuting multiplication
operators and a normalized state on the lower-column space. A visible joint
real eigenvector gives one common point annihilating every quadratic polynomial
whose square has zero moment.

All 180 concrete residuals are in the quadratic span. The finite equations
annihilating each residual times every upper monomial imply zero square moment.
The same extracted point satisfies all residuals, hence gives an actual complex
unitary candidate with all 108 MU overlaps. Evaluation at any solution supplies
normalized positive flat rank-one moments, yielding a two-way existence
equivalence. The empty-variety consequence excludes positive semidefiniteness
under normalization, actual flatness and finite relation compatibility.
No operator family or coordinate point is an extraction input.

The separate noncommutative word route retains its dimension-six/rank-one/MU
and full star-algebra limits. Variety emptiness, the Route C landing premise,
and complete 56-cell/three-cusp semantic reflection remain open. The manuscript,
claim ledger, mirrored synthesis plan, registry and executive checkpoint now
state the direct real coordinate bridge and its exact premises.

The targeted canonical build passed with 8,720 dependency jobs and no warnings
in the two new modules. All printed dependencies are in the permitted set.
Expanded aggregate build/audit, current Python and rendering results, archive
custody and the unchanged-source Rust result are recorded in the executive
checkpoint and byte-bound receipt for this revision.

The full aggregate build passed for 116 local modules, with 8,822 dependency
jobs. The transitive audit checked 11,163 owned declarations with zero
disallowed dependencies. The source scan found zero active placeholders or
custom axiom declarations. All nine pinned dependency revisions and tracked
trees were revalidated; prior 114-module logs are preserved. The final Python
suite passed 71 tests in 8.91 seconds. Strict KaTeX rendering passed for 64
main-manuscript and two changelog expressions, with byte-identical plan copies.
The historical archive has 474 members and 477 checked manifest entries;
independent rebuilds agree. Release metadata recognizes the real coordinate
bridge while retaining the unresolved emptiness, flatness-use and coverage
gates. Rust sources are unchanged; the completed full-library result remains
318 passed, zero failed, zero panic events and 18 ignored tests. No new full
Rust execution is claimed for this revision.

## 2026-10-10: continuous phase family and arbitrary additional bases

Added `SzollosiTwoCirculant.lean` and `SzollosiQuartetSystem.lean`.
The first derives the actual six-phase block Gram identity and normalization,
then checks the four-phase construction and six scalar real parameter equations
in eight coordinates. Every phase-sum intersection point has an encoding in
that system; all solutions lie in the rational unit box. Cubic identities and
a concrete boundary parameter point are checked without a distinct-root premise.
No classification or equivalence transport is inferred.

The quartet formulation leaves both additional bases arbitrary, retaining all
144 real coordinates. Standard-basis unbiasedness gives a rational half-unit
containing box. Absence of a quartet is equivalent to emptiness for every
admissible third-basis variety in the constructed block gauge. This identifies
the required quantifier; no variety emptiness is supplied. A selected Zauner
triplet cannot stand in for that quantifier. Joint rational encoding, the
square-system reduction, full 56-cell/cusp exclusion and semantic reflection
remain open, along with the concrete Route C landing.

The targeted build passed with 8,721 dependency jobs and no new-module warnings.
The full aggregate build passed for 118 local modules with 8,824 dependency jobs.
The transitive audit checked 11,253 owned declarations with zero disallowed
axioms. All nine pinned dependency revisions and tracked trees were revalidated;
prior 116-module logs are preserved. Current Python, rendering and archive
results are recorded in the executive checkpoint and byte-bound receipt.
Rust sources are unchanged; the retained completed full command has 318 passed,
zero failed, zero panic events and 18 ignored tests. No new full Rust execution
is claimed for this revision.

The refreshed Python suite passed all 71 tests in 12.25 seconds. Strict KaTeX
rendering passed for 73 main-manuscript and two changelog expressions. The plan
copies remain byte-identical. Two independent historical-archive rebuilds agree
on raw bytes; all 474 members and 477 manifest entries match. The archive still
excludes the current manuscript and canonical Lean tree. Publication remains
NO-GO for the requested complete package, and the full Option B goal remains active.


## 2026-10-10: joint rational quadratic quartet specification

Added `SzollosiQuadraticSystem.lean`: 440 real coordinates and 618 rational
polynomials, every total degree at most two. The system retains eight phase
coordinates, three raw complex basis matrices and three auxiliary cross-product
matrices. Raw scaling is sqrt six; the cross-product norm-square target is six.
The actual quartet/solution correspondence is checked in both directions,
including at each fixed admissible phase parameter. Both additional bases remain
arbitrary. Every solution lies in a rational containing box of radius one for
phase/raw-basis coordinates and three for cross-product coordinates.

The full aggregate build passed for 119 local modules, 8,825 dependency jobs.
The all-declaration audit checked 11,448 owned declarations, zero disallowed
axiom dependencies. The targeted new-module build passed, 8,722 dependency jobs,
with no compiler warnings in that module. Two modified scratch models were
rejected: raw overlap target one in place of six and omitted complex conjugation.
The previous 118-module build/audit logs remain retained and byte-bound.

This is a noncomputable Mathlib specification, with no executable native
coefficient export or empty solution set derived. A valid square/gauge reduction
or rectangular exclusion method, dephased equivalence transport, complete cover,
cusp treatment, analytic soundness and semantic reflection remain open. Route C
landing and the remaining flatness/variety-emptiness obligations are unchanged.
The requested completed publication package remains NO-GO; the goal stays active.


Checkpoint validation also passed all 71 Python tests in 13.01 seconds and strict
KaTeX rendering (76 main-manuscript expressions and two changelog expressions).
The source-bound Rust result is retained: 318 passed, zero failures, zero panic
events, 18 ignored. Rust sources are unchanged. Independent archive rebuilds and
raw-byte comparison passed for 474 members and 477 manifest entries; the archive
still excludes the current papers and canonical Lean tree.


## 2026-10-10: executable quartet expressions and interval semantics

Added `SzollosiExecutableSystem.lean`, an executable representation of all 618
checked rational equations on 440 coordinates. The expression/polynomial and
real-evaluation identities hold for every assignment; ordered IDs cover all
variables and equations. The checked rational containing box is exported with
three rational probes. Independent exports are byte-identical, raw SHA-256
`1367d390da36e5ccf65abbc8fbf529ff07f9e154c277bb14c1cd8c36ba24c947`.

The new native inspector compiles 5,128 sparse terms of degree at most two,
checks all 1,854 probe values and emits 618 rational residual intervals. The
observed status is `UNRESOLVED_FULL_BOX`; the receipt reproduces byte for byte.
Five focused tests passed, including equation/box/parity mutations, malformed
rational refusal, point enclosure and exact quadratic derivative identities.
The binary provides `--inspect-system`, without a depth-64 contractor run.

Added `SzollosiIntervalExclusion.lean`. Rational AST intervals enclose the actual
polynomial values for every contained real assignment. A successful residual
zero-exclusion check excludes actual zeros in that box. The complete containing
box reduces to false inside the kernel. A computed first-phase interior box
contains no admissible unit phase and is excluded. This off-domain example
supplies no exclusion of admissible quartets. A reversed product lower bound
and a widened example radius were rejected by the expected Lean obligations.

The full Lean build passed for 121 local modules, 8827 dependency jobs;
the full audit checked 11,748 owned declarations with zero disallowed
axiom dependencies. All 71 Python tests passed in 16.23 seconds. The fresh full
Rust command passed 323 tests, zero failures, zero observed panic events,
18 ignored and zero filtered, 2165.43 seconds. Ignored tests did not
execute. Prior 318-test and 119-/120-module logs remain byte-bound.

Native sparse compilation/interval semantics are not kernel-identified with the
Lean AST by finite probe agreement. No real solution set is established empty.
A valid system reduction or rectangular exclusion method, dephased transport,
complete coverage, three cusp collars and full analytic reflection remain open.
The manuscript, claim ledger, mirrored plan and release blockers were reconciled.
The requested completed publication package remains NO-GO; the goal stays active.


## 2026-10-10: complete native coefficient and interval data reflection

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

The full Rust run passed 324 tests, zero failures, zero observed panic
events, 18 ignored, zero filtered, 2357.06 seconds. All 71 Python tests
passed in 9.09 seconds. The complete Lean build covers 124 local modules
and 8830 dependency jobs; the all-declaration audit covers 12,544 owned
declarations with zero disallowed dependencies. Earlier 323-test and 121-module
gates remain byte-bound. Independent receipt and Lean source generation are
byte-identical. The formatter performs wire validation and byte custody only.
The generated literals are split by equation row after an observed pending-MVars
elaboration timeout. Closed data checks use `decide +kernel`; earlier `rfl`
attempts did not close. Failed and interrupted logs remain byte-bound.
Two redundant scratch Lean checks were interrupted after observed memory/disk
exhaustion; neither has a mathematical pass/fail verdict. The retained canonical
build supplies the successful proof evidence.

Valid reduction or rectangular exclusion, dephased transport, complete 56-cell
coverage, three cusp collars and analytic contractor reflection remain open.
The Route C landing and flat-extension scope limits remain. The requested
publication package remains NO-GO; the full goal stays active.

## 2026-10-10 — rectangular quadratic exclusion and actual quartet bridge

- Added the exact quadratic midpoint secant identity, formal partial-derivative
  identification, rational derivative interval soundness and rectangular image
  enclosure of every zero. A rational preconditioner may be rectangular and need
  not be an inverse. Strict coordinate separation is the exclusion criterion.
- Connected the checked native coefficient table to the contractor without
  dropping any of the 618 equations or 440 coordinates. Leaf checks now imply
  absence of actual polynomial solutions; a successful full containing-box
  check would exclude actual quartets in the constructed block gauge.
- Added kernel examples where residual intervals include zero but the image
  excludes the box, where endpoint contact must be retained, and where strict
  overdetermined inclusion occurs without a common root. Updated the root-branch
  wording in the synthesis plan and executive report accordingly.
- Retained scratch attempts with cast, binder and coordinate-indicator proof
  errors. The canonical modules contain the repaired proofs; failed scratch
  elaborations are excluded from their successful build and axiom scope.
- No successful quartet-domain exclusion, native rectangular image parity,
  complete 56-cell/cusp computation, curvature certificate or publication
  completion is asserted. The full Option B goal remains active.


## 2026-10-10 — native rectangular calculation and kernel reflection

- Added strict native rectangular requests for the full 618-equation,
  440-coordinate system, exact sparse Jacobians, arbitrary rational weights,
  images, intersections and typed malformed-input refusals. Existing inspection
  output remains byte identical. Alias checks preserve all input bytes.
- The full-box run uses 28 nonzero weights, emits all 9,000 Jacobian support
  entries and narrows 24 coordinates. None separates. The preserved request and
  default calculation reproduce the same `CONTRACTED_UNRESOLVED_BOX` receipt.
- Added finite-support quadratic image soundness and kernel reflection of every
  emitted derivative interval, image, intersection and contracted-coordinate
  index. Every actual system zero is retained. A monolithic reduction approached
  the machine memory limit and was stopped; bounded row checks replace it.
  Failed scratch attempts and resource diagnostics remain outside the
  successful canonical build.
- Current-data reflection supplies no generic Rust/decoder verification, root
  existence, complete 56-cell/cusp cover, successful quartet-domain exclusion or
  curvature conclusion. The full goal remains active.


- Final validation: full serial Rust command, 330 passed, zero failed,
  18 ignored, zero observed panic events; Python, 84 passed; Lean build,
  137 local modules and 8843 dependency jobs; owned-declaration audit,
  14,559 declarations and zero disallowed dependencies. Independent
  kernel controls evaluate both altered endpoint comparisons to false before
  rejecting acceptance. Initial list-update and type-failure diagnostics are
  retained as superseded probe attempts.

## 2026-10-10: existence-preserving column gauge for both additional bases

- Added exact Gram transport under independent unit column phases and preserved
  all raw quartet equations with the family matrix and phase parameters fixed.
- Derived first-row normalization for both additional bases, prescribing 24 real
  coordinates. The wire list at IDs 80-91 and 152-163 reduces by `rfl`.
- Added the explicit rational point box, derived first-row equalities from box
  membership, and checked quartet/boxed-solution existence at each parameter.
- Exported the box twice with equal bytes. The native replay retains an unresolved
  domain; its new output images are not kernel-reflected and give no exclusion.
- Refreshed the complete Lean build, all-owned-declaration axiom audit, source
  scan, Python suite and strict math rendering. The completed Rust run remains
  bound to unchanged Rust sources. The full Option B goal remains open.

## 2026-10-10 — Derived balance equations and candidate-box exclusion

Retained every original quartet equation and appended 24 gauge and 24 derived
transition-balance equations, preserving existence at each admissible parameter.
The 666-row Lean/native export has 5,320 terms and 1,998 probe comparisons.
Added six overlapping candidate charts and a semantic bridge to their actual
native bounds. All six native chart runs remain unresolved. A separate box,
whose phase projection meets the admissible domain, is excluded by the exact
row balance image [7/2,17/2] against input [-1/2,1/2]. Added coefficient/input
literal checks, selected-image real semantics, strict native shape handling,
and adversarial formatter controls. Full family/cusp coverage, curvature
closure, global landing and the remaining moment premises are still open.
