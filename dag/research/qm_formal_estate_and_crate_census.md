# Finite-QM source review, Weyl transport and Gleason boundaries

Review date: 2026-10-12. Initial base: remote main `c8201a757` (PR #818).
Synced again to `5452a476d` (PR #821); those intervening changes do not alter
the reviewed math owners, Lean project or finite-QM paper.
AuthorityEffect: None. This supersedes the 2026-10-11 census's unsupported
blanket certification claims; Git retains that revision and historical source
archives and receipts remain intact.

Edition 0.51.0 adds the manuscript's carrier/observer/measurement synthesis.
Its focused instrument, conditioning and exact record checks do not replay
this entire review. The inventory below remains the snapshot of the reviewed
sources, while the paper file catalog is refreshed separately. Later crate
additions do not inherit this review's test or Lean-build verdicts.

## Coverage and reproduction

The [reproducible inventory](qm_weyl_gleason_source_inventory.json) records every
canonical QM Lean module and every Rust file in all 17 requested owners, with
path, hash and line count. Generate or check it with
`python python/finite_qm/entrypoints/review_estate.py --write` or `--check` from
this paper directory. After staging new paper files, add `--manifest` to
refresh/check the current paper manifest as well. Inventory coverage is not a claim of exhaustive semantic
review of 1,413 Rust files. Detailed proof and contract review in this change
covers the Weyl/Gleason, projector, transport, tensor, tomography and evidence
paths below; other Rust modules received ownership/interface review.

- **Lean:** 185 source modules, excluding `lakefile.lean`. All 184 core modules
  build through the repaired Lake project with pinned Lean 4.33.1 (193 jobs,
  including eight source-owned primitive-difference dependencies). Twelve
  previously unlisted modules are now registered; renamed H-series and C750
  imports resolve. No source dependency was copied out of its owner.
- **Entropy module:** the pinned Mathlib cache request received proxy HTTP 403
  from `lakecache.blob.core.windows.net`. `EntropyDichotomy.lean` separately
  typechecks against the available Lean/Mathlib 4.34.0 cache. This is a distinct
  reproduction result, not a successful pinned full-project build. Baker's
  theorem remains a supplied hypothesis in the reduction.
- **Axioms:** the new proofs print their dependencies. The rational-plane and
  commutant proofs use `propext`, `Classical.choice`, and `Quot.sound`; Cabello
  parity uses the standard arithmetic proof dependencies. No new custom axiom
  or `sorry` was introduced. Absence of a custom `axiom` declaration does not
  discharge theorem arguments or fields of an assumed structure.
- **Rust:** focused exact regressions passed: seven falser unit tests, three
  falser integration tests, the existing Weyl-triad integration, two carrier/
  tensor mutation tests, two Weyl-intertwiner tests, and the Cabello positivity
  integration. These do not constitute all-crate or all-feature testing.
- **Application:** a development wheel built from the changed Rust owners and
  live Python host was installed in an isolated virtual environment; both
  integration files passed (49 tests), including native exact boundaries and
  revision-bound receipt corruption controls. This is development-wheel
  reproduction, not a release-profile or cross-platform certification.
- **Finite search:** 720 unphased Tao row permutations and 144 points of the
  specified two-circulant ansatz were rejected exactly. The debug integration
  search took about two minutes after candidate projector validation. No
  row-phase orbit or continuous Hadamard family was exhausted.

The [validation record](qm_weyl_gleason_validation.json) records commands,
source-inventory binding, toolchain revisions and the development wheel digest.
Default-library `cargo check` also passes for `omega_mub` and `omega_sheaf_theory`;
no claim of all-feature or all-test coverage follows.

The paper tree was inventoried separately through its refreshed file manifest.
The total claim/file matrix retains its 2026-10-11 name/citation scan as
historical data, with the current review and inventory explicitly superseding
its counts and suggested proof promotions. Historical campaigns, archived
Python copies and source pins are retained;
old success receipts are not promoted to current reproduction results.

## Corrections supported by counterexamples

| Finding | Repair and scope |
| --- | --- |
| Six copies of I/6 pass all 108 cross-overlap equations | Both attack methods now run the canonical projector-algebra checker. The regression demonstrates all 108 passing overlaps and then rejection of the invalid candidate. The reference triad is also verified. |
| HH*=6I does not imply complex Hadamard | Require every entry times its conjugate to equal one. The exact sqrt(3)(1+i)I counterexample is rejected; all 144 selected two-circulant matrices pass both conditions. |
| Tao row phases were advertised but never enumerated | Scope is narrowed explicitly to unphased row permutations. Each shares the uniform first column with the X basis, so these failures are a simple shared-ray obstruction. The conclusion depends on actual counts and does not hard-code 100%. |
| A transport report can change carrier labels without changing counts | Board, spectral, algebra and Hilbert dimensions agree; available exponents agree and d=2^e is checked. Count arithmetic is checked for overflow. Seven independent label mutations are rejected. This aligns reports, not independently supplied proofs. |
| Empty/malformed factor reports panic or pass | Require at least two distinct prime-power factors, checked product dimension, q+1 factor basis counts, and matching reported minimum/complete counts. Ten malformed-report mutations are refused. Factor-control flags remain caller-supplied premises. |
| Finite tomography can return a non-PSD matrix | `FrameSystem::density_state_of` supplements unique symmetric reconstruction with the linear-algebra owner's exact inertia test. The Cabello non-PSD reconstruction is refused and I/4 is admitted. |
| Relocation invalidates current-path checks of historical receipts | The repository marker is the canonical Cargo workspace; integration tests compare claim bytes/hashes at the recorded source revision, rather than requiring historical paths to exist in today's tree. Source pins are unchanged. |

## Weyl: constructive equivalence and its exact price

The reusable implementation is
`omega_lie_theory::heisenberg::WeylHeisenberg::intertwiner_from_clock_seed`.
Given a primitive d-th root omega, exact unitary d-by-d matrices X', Z' with
Z'X'=omega X'Z', X'^d=I, and a supplied v with Z'v=v and v* v=1, set

    U = [v, X'v, ..., X'^(d-1)v].

Induction gives Z'X'^j v=omega^j X'^j v. Distinct eigenvalues of the unitary
clock give orthogonal columns; unitarity of X' gives norm one. The cyclic
shift and eigenvalue equations give X'U=UX and Z'U=UZ. The implementation
checks every input identity and both U*U=UU*=I and the two output intertwining
identities before returning U. Tests use d=3 and a non-monomial rational
change of basis in d=6, plus wrong norms, eigenvectors, relations, shape and
period controls. The construction is not restricted to prime dimension.

`WeylCommutant.lean` proves the complementary dimension-independent statement:
over a field, an operator commuting entrywise with a diagonal clock with
pairwise distinct eigenvalues has no off-diagonal entries; equality of adjacent
diagonal entries forced by the cyclic shift then makes it scalar. The clock
spectrum and shift-entry premise are explicit. This is not a formal proof that
all abstract representations have those premises.

Remaining prices: finding the eigenvector, admitting any scalar extension
needed to normalize it, deriving the primitive phase and X/Z relations from
native histories, treating other dimensions/multiplicities and central
characters, and transporting operationally available states/effects. The
existing Stone-von Neumann census is a dimension table; its sum of squares does
not prove representation classification. Finite characteristic-zero CCR still
fails by trace; a finite Weyl relation is a different algebraic statement.

## Gleason: stronger finite results without a false uniqueness claim

`GleasonRationalPlane.lean` defines f(x,y)=1 when xy>0, f=0 when xy<0,
and selects the horizontal axis at xy=0. On nonzero rational vectors it:

1. takes only 0 or 1;
2. is invariant under every nonzero rational rescaling;
3. satisfies f(x,y)+f(u,v)=1 for every nonzero orthogonal pair;
4. has no representation (a*x*x+2*b*x*y+c*y*y)/(x*x+y*y) with rational a,b,c.

For the last claim the axes force a=1,c=0, the ray (1,1) forces b=1/2,
and (1,2) would require 3=5. This replaces the old file's integer-parity
argument with an actual frame-function construction on the declared domain.
The existing `GleasonTheorem.lean` names are retained with accurate comments;
its oddness proof alone never ruled out b=1/2.

`H054GleasonCyclotomicObstruction.lean` now proves that no integer assignment
has sum one on each of the nine Cabello contexts: every one of the 18 rays
occurs twice, whereas the total demanded by the contexts is nine. This rules
out binary noncontextual assignments on that finite projective configuration.
It does not prove uniqueness of general probability-valued frame functions.
The same file now bundles every sampled bound and frame sum for M_bad/2 with
its negative witness. The witness's Rayleigh quotient is -1/2, which is not
an assertion that the least eigenvalue equals -1/2.

`H058EffectFrameBusch.lean` proves the four probes D0,D1,P_plus,P_R are
actual effects, that their trace readouts determine a Hermitian qubit matrix,
and that the tomographic candidate reproduces those readouts. Positivity on
all effects and representation of the entire function remain separate.
Its rational homogeneity witness supplies the subdivision equalities; its
squeeze lemma ranges over Rat; its old non-extension theorem assumes a
midpoint identity. None is silently upgraded into a proof of Busch's theorem.

The missing general bridge remains substantial: specify the ray/effect domain,
noncontextuality and additivity law, normalization, positivity, dimension,
and any regularity/extension assumptions, then derive a positive trace-one
representation on that full domain. A rational unit sphere and all rational
projective rays are different domains because normalization can require square
roots. Countability or density alone proves neither a countermodel nor Born
uniqueness. Real quantum theory has purification; quaternion multiplication is
associative; dimension counts alone do not certify an operational theory.

## Ownership map for the requested math crates

These are inspected implementation entry points and useful integration routes,
not claims that every listed crate has been fully tested in this review.

| Owner | Existing route into finite QM | Obligation at the boundary |
| --- | --- | --- |
| omega_number_theory | Cyclotomic fields, finite fields, character sums, ordered real embeddings | Specify conductor, conjugation, embeddings and scalar extensions. Q(zeta_n) is generally not ordered. |
| omega_linear_algebra | Exact field matrices, elimination, commutants and Hermitian inertia | Distinguish matrix identities, positivity and state admission. |
| omega_lie_theory | Weyl systems, intertwiners, finite path and twisted groupoid algebras | Prove the native history presentation and faithful quotient/phase transport. |
| omega_quantum_physics | Projector checks, frame polytopes, tomography, channels | State/effect availability and composition remain model inputs. |
| omega_sheaf_theory | `finite_report_gluing`, covers and sections | A compatible report section need not be a physical global state. |
| omega_mub | Search/obstruction orchestration over the physics owner | Exhaustion is relative to a declared carrier and search region. |
| omega_finite_probability | Simplexes, marginal compatibility, signed representations | Classical probabilities do not by themselves select a Born pairing. |
| omega_category_theory | Finite histories, groupoids, dagger and report descent | Identify relations, invertibility, composition and faithfulness. |
| omega_combinatorics | Budgeted Cartesian-word and finite enumeration | Termination under a budget is not unbounded completeness. |
| omega_fusion_categories | Exact fusion rings, pentagon/hexagon and braid data | Validate each model and its field; no blanket classification follows. |
| omega_functional | Exact residual, norm and feasibility functionals | Bind a functional to its supplied norm, carrier and operational meaning. |
| omega_general_relativity | Finite Regge, causal and simplicial models | Toy amplitudes or integer area formulae do not establish quantum gravity. |
| omega_homology | Chain/cochain complexes, F2 and rational cohomology | An obstruction class has meaning relative to its declared complex. |
| omega_holonomy | `signed_transport`, connections and discrete loop products | FSP sign transport is not automatically a full complex phase group. |
| omega_homotopy_type_theory | Finite paths, transport and presentation differences | Runtime records are not themselves a proof of a HoTT foundation. |
| omega_solvers | Exact rational feasibility and Boolean constraints | Require a replayable witness/refutation within the declared bounds. |
| omega_wdp | Genesis histories, question-preserving encodings and observer adapters | Preserve protected questions across each quotient and representation. |

The useful combined route is native histories -> checked relations/groupoid ->
declared exact *-algebra -> positive state/effect model -> faithful operational
readout. The Weyl and tomography additions strengthen the middle of this route;
GAP-FQM-021 still concerns the missing derivation of its premises from the
primitive construction. They do not solve unrestricted MUB6, FSP composition,
or the entire <>-to-QM reconstruction.

## Corrections to the previous census

The former claims of 188 modules compiled on Lean 4.34.1, universal axiom purity,
fully tested crates, zero-allocation arithmetic, dense-field Gleason from H017,
and complete quantum-gravity/topological-computing foundations were not backed
by the stated source. H017 is a cardinality surrogate; H022 uses stipulated
area/entropy formulae; H023-H027 prove finite declared amplitude and parity
models. The previously cited `TsirelsonCHSH.lean` path does not exist in this
canonical tree, and Tsirelson's bound would not exclude superquantum
no-signalling boxes in any case. `U1TorsionExclusion.lean` explicitly proves
that the quarter-turn has order four: unbounded integer labels do not imply
infinitely many distinct represented elements. These are scope corrections,
not deletions of the valid underlying finite theorems.
