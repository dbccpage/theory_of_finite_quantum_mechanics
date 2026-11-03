# PR #500: independent proof, statement, and dependency review

AuthorityEffect: None.

Reviewed source: `45b0b093921aa0281969f92da18694e2e89c3cc4`, PR #500,
`claude/project-thread-mgyaz1`. This report concerns that exact source, not a later moving head.
The original analytic receipt is retained unchanged. The independent replay is in
`manifest.json`, `Audit.lean`, `Audit.txt`, and the eight module outputs in this directory.

**Verdict:** no proof-level error was found in the stated uniform-continuity implication.
All 3,430 lines of the four new Lean modules were read, and all eight project modules in
their import closure were independently rebuilt. All 302 named declarations in the four
new modules were audited with `#print axioms`; only `propext`, `Classical.choice`, and
`Quot.sound` occurred. Four supporting declarations and two review lemmas passed the same
audit. This establishes the conditional result; it does not establish its regularity premise.
There are eleven actionable statement, provenance, documentation, and verification findings below.

## Scope and independent checks

| Module read in full | Lines | What was checked against its proof |
| --- | ---: | --- |
| `BornGaussianParallelogramRigidity.lean` | 444 | Zero-weight and nine-ray hypotheses; zero-vector cases; scalar invariance; three plane reflections; coordinate permutations; propagation off the planes; application to the tomography residual. |
| `GleasonRealSphere.lean` | 1,552 | Frame and scale definitions; meridian descent; finite real multiplier factorization; latitude constancy under continuity; maxima/minima on compact sets; orthonormal changes of coordinates; six-circle identities and elimination; final continuous signed theorem in dimension three. |
| `GleasonComplexSphere.lean` | 586 | Hermitian convention and conjugated cross product; fully real pullbacks; two-dimensional restriction argument; compact maximum and perpendicular maximum; orthonormal decomposition; exact continuous signed theorem on C^3. |
| `GleasonGaussianBridge.lean` | 848 | Faithful Q(i) embedding; cross-product norm identity; squared ray distance; rational density; well-defined pushforward; uniform extension; passage of scale invariance and the frame identity by density of admissible pairs; complex Gleason; residual parallelogram law; final quantified conclusion. |

The four older project dependencies were rebuilt too: `BornGaussRat`,
`BornGaussianRationalFrameObstruction`, `BornGaussianFrameRays`, and
`BornGaussianTomographyReduction`. Their used carrier/frame/tomography/continuity/residual
definitions and theorem statements were inspected. This is not a claim to have manually
re-reviewed every line of the older 8,595-line tomography module or of Mathlib.

Rebuild: Lean 4.35.0, commit `eb6cafb7290e8bd5f2937522d8d804f58f02bafc`, Windows;
Mathlib `56a005855ea17e0b0958f73ec801ae140b0a1679`, existing clean checkout and cached
Mathlib oleans. Fresh project oleans were placed in an isolated audit build directory.
The project sources were hashed before and after compilation. All eight compiled unchanged.
This is a source rebuild of the project closure, not a fresh build of Mathlib or a replay
of every library in the repository. No hosted Lean replay was found in the PR workflows.

To reproduce with a configured checkout, from `lean4` run
`lake build BornGaussianParallelogramRigidity GleasonRealSphere GleasonComplexSphere GleasonGaussianBridge`,
then `lake env lean ../dag/research/pr500_review/Audit.lean` and compare the complete output
with the retained names and axiom allowlist. The independent Windows run used the same
pinned Lean binary directly with `LEAN_PATH` containing the fresh project build directory
and existing package library directories, compiling each module in manifest order with
`lean -o <fresh-build>/<module>.olean <source>`. Check source hashes before interpreting
an old audit as evidence for a new tree.

PR #500 was merged during this review as `e30671f8c566b2653de08a8d5cef0719b95f7dc0`.
Its tree is identical to the reviewed head. These corrections are published as a follow-up,
not as a claim that the original merge awaited this audit.

The independent audit also checks:

- A genuine instance: the constant function `f = 1/3` is both a frame function and uniformly
  ray continuous (`PR500Review.uniform_input_nonvacuous`).
- The exported theorem has the advertised signed hypotheses, with no hidden positivity input.
- A nonnegative input makes `quadNum (tomographyForm f) v >= 0` for every nonzero rational
  vector (`PR500Review.rational_numerator_nonneg`). This is not yet the complex PSD wrapper.
- Existing `exoticQi3_isNonnegFrameFunction`, `exoticQi3_not_quadratic`,
  `tomography_trace_one`, and `tomography_unique` have only the standard listed axioms.

An initial version of the review-only nonnegativity check used a nonexistent lemma name,
`div_nonneg_iff_of_pos_right`; it failed elaboration. Replacing that step with multiplication
by the positive squared norm made the check pass. This was a review-harness error, not a
PR proof error. The manifest records this failed attempt; the retained final audit has no
`sorryAx`, unknown identifier, or other elaboration error.

## Findings and corrections

### 1. P1: TFQ-1055 is mislabeled as an open pointwise-continuity target

At the reviewed head, the note (lines 6-7 and 92-93), uniform node, bridge contract, analytic
receipt, and PR description describe TFQ-1055 and TFQ-0307 as original pointwise targets.
TFQ-1055's literal statement is instead:

> Let V = Q(i)^3 with the standard Hermitian form. Decide whether every function f from the
> nonzero vectors of V to Q with f(u) + f(v) + f(w) = 1 for every orthogonal triple of nonzero
> vectors has the form f(v) = <v, rho v>/<v, v> for a Hermitian trace-one 3 x 3 matrix rho over
> Q(i), or exhibit one that does not; state separately the signed, nonnegative and {0,1}-valued
> variants, and whether the non-quadratic Q^3 frame function extends to Q(i)^3.

There is no continuity premise. `exoticQi3` already refutes the universal assertion, even
with nonnegativity. The zero-one and specified-extension subquestions have separate negative
answers. Leaving the node OPEN for a different, unstated regularity problem misdirects work.

**Correction made:** keep the original question verbatim; mark REFUTED explicitly for its
unrestricted quadratic-rigidity assertion, record the resolved decision alternatives, and
put the new continuity question in TFQ-1057. Remove the stale route claim that the uniform
prime-indexed residual construction is still unwritten. TFQ-0307 remains CONDITIONAL: its
broad operational/projection-lattice target is not the literal pointwise statement either.
Historical receipts and old contract history are not silently rewritten. Claude should
append corrected current contract boundaries and update the PR description.

### 2. P1: the Born route imports a package that already assumes the Born pairing

`FQ-R-GLEASON-QI3-UNIFORM-RAY-CONTINUITY` takes
`FQ-DECLARED-QUANTUM-INTERFACE` as its sole input. That bundle includes the trace/Born pairing,
as well as dynamics and tensor structure not used by these proofs. This is a misleading
provenance dependency, although the Lean proof itself is not circular.

**Correction made:** introduce a narrow Q(i)^3 carrier/frame-definition node and use it for
the uniform theorem and rational obstruction routes. State uniform continuity as a separate
declared hypothesis. Add a distinct continuous-C^3 theorem node and an OPEN completion
packaging target. The abstract carrier is still supplied; this does not derive it from
the finite system's operational rules.

### 3. P2: the near-supremum argument silently needs boundedness

The note's epsilon-descent paragraph starts from `f(p) > sup f - epsilon` while discussing
both signed and nonnegative pointwise-continuous rational frame functions. Pointwise
continuity on this noncompact rational domain has not established a finite supremum for
the signed case. For nonnegative frame functions, frame completion gives `0 <= f <= 1`.

**Correction made:** restrict that attempted argument to bounded-above functions, in
particular the nonnegative case. Do not treat a bounded signed reduction as already proved.

### 4. P2: uniform continuity does not produce a fixed rational maximizing pole

The note says uniform continuity lets epsilon tend to zero with the pole fixed (line 62).
The actual bridge instead extends to a continuous function on complex rays; compactness
then supplies a maximum, potentially at an irrational ray. Even a rational-coefficient
Hermitian matrix need not have a rational maximizing eigenray.

**Correction made:** describe the extension/compactness mechanism. The moving rational
near-maximizer problem is precisely not solved by pretending the maximum is rational.

### 5. P2: two-step nondensity is overinterpreted as a further reachability obstruction

The corrected two-step calculation is right: writing `(1+ti)(1+si)=a+bi` gives
`b^2 + 4(a-1) = (t-s)^2 >= 0`. It does not decide the closure of arbitrary finite chains.
`GleasonReal.exists_chain_eq` (lines 258-337) proves every complex multiplier of modulus
greater than one is a finite product of real-parameter factors. For that fixed finite
length, the product is a continuous polynomial in the parameters and Q^N is dense in R^N.
Hence rational finite products approximate every such multiplier. Their full closure is
`{m : |m| >= 1}`: factors all have modulus at least one, and the unit circle is approached
from outside. The original claim of density in all of C remains false.

**Correction made:** supply this paper argument, explicitly not yet a new Lean theorem.
It restores approximation in the outward multiplier region only. It gives no uniform
bound on chain length, no control of a changing near-maximizer, and no solution to the
accumulating-error problem. The asserted inverse-latitude scaling is a feature of the
known construction, not a proved lower bound for every possible proof strategy.

### 6. P2: “nowhere continuous” exceeds the cited formal evidence

The note (line 84) and TFQ-1057 say `s3`, `s7`, and `sp` are nowhere Archimedean continuous.
The cited elimination statements concern `tomo_e1`, selected witnesses, and finite residual
systems under their stated hypotheses. They do not prove discontinuity at every ray for
every parameter. The stronger statement may be true; it is not established by these citations.

**Correction made:** state the proved discontinuity/oscillation at `tomo_e1`, with the
finite-system hypotheses retained. One discontinuity already excludes continuity everywhere.

### 7. P3: the algebraic module claims three unequal poles have equal norms

`BornGaussianParallelogramRigidity.lean:21` calls `e2`, `e2+e3`, and `e2+i e3` three zero
poles with equal norms. Their squared norms are 1, 2, and 2. The proof only needs the equal
norms within each pole/orthogonal-partner pair, which it establishes correctly.

**Suggested correction:** replace “three zero poles with equal norms” by “three zero poles,
each paired with an orthogonal zero partner of the same norm.” No proof change is needed.
Left for the author so this review does not change the audited Lean source or its receipt pins.

### 8. P3: the module header advertises nonexistent exported theorems

`BornGaussianParallelogramRigidity.lean:44-47` advertises plural
`signed_rigidity_of_orthoParallelogramZero_residuals` and
`nonneg_rigidity_of_orthoParallelogramZero_residuals`. Neither declaration exists.
The exported theorem at line 425 is singular
`signed_rigidity_of_orthoParallelogramZero_residual`; nonnegative inputs are a specialization.

**Suggested correction:** cite the actual singular name and state the specialization, or
add and check an explicitly named nonnegative wrapper. Left for the author.

### 9. P2: source-bound replay and hosted Lean coverage are incomplete

The original analytic receipt hashes the four new sources and lakefile and lists successful
commands/axiom summaries. It omits raw audit input/output and source hashes for the four
project dependencies. The listed build commands alone do not reproduce the complete axiom
tables; the real/complex modules do not contain those `#print axioms` commands. The hosted
governance job verifies other campaigns' receipts, not this one. Merely declaring four
non-default `lean_lib` targets does not cause CI to compile them.

**Correction partly made:** retain an independent eight-module source manifest, toolchain
and manifest hashes, exact audit input, raw outputs, and complete axiom coverage. No contrary
proof result was found. **Still required for regression protection:** a fail-closed verifier
and hosted job that explicitly builds these targets, checks all expected audit reports,
rejects unexpected axioms (including `sorryAx`), and invalidates evidence when any project
dependency or toolchain pin changes. Test missing-report, stale-source, and unexpected-axiom
failure cases. Do not equate the currently green governance job with a Lean build.

### 10. P2: contract symbol inventories truncate Unicode Lean identifiers

`GleasonGaussianBridge.contract.score.yaml` contains `nonZero_of_`, `dotC_`, `nsq_`,
`exists_`, duplicate `f`, `uniformContinuous_f`, `C`, `R`, and `F_` in place of names involving
`ι`, `₀`, or `₁`. For example, the source declares `nonZero_of_ι_ne_zero`, `f₀`, and `F_ι`.
The file-content hash is correct, but the advertised symbol inventory is not an exact binding.
Its current claim also still calls `raySinSq` a metric rather than a squared distance.

**Suggested correction:** use Unicode-preserving declaration extraction, check each advertised
name against Lean, reject truncations/duplicates, and append corrected contract history with
the accurate DAG boundary. Do not rewrite past records. The independent audit in this review
uses the complete Unicode identifiers and successfully checks all of them.

### 11. P2: the published README embeds a failed contract-check invocation

At line 72 the contract row reads `could not parse output (exit 1)`. This is a failed generator
observation, not a useful current contract result. The independent whole-tree check passed
for all 3,703 governed source companions before these documentation updates.

**Correction made:** regenerate README facts with the working Python/PyYAML environment;
retain the real check result. Do not paper over a nonzero checker exit with a success string.

## What is proved, and what is still missing

The exact rational result is

`IsFrameFunction f -> IsUniformlyRayContinuous f ->`
`forall v != 0, f v = quadRay (tomographyForm f) v`.

It is signed, fixed to dimension three and rational-valued inputs. Trace one and uniqueness
are available from the existing tomography results, rather than extra conclusions syntactically
bundled into the exported bridge theorem. Nonnegativity is needed to conclude a density matrix.

There is already a continuum theorem in this PR: `GleasonComplex.gleason_complex` proves
quadratic representation for real-valued **continuous** frame functions on all of C^3, with
complex scale invariance and weight W supplied. It is not yet the classical theorem which
derives continuity from nonnegativity, nor an arbitrary-dimension or infinite-dimensional result.

Q(i)^3 is finite-dimensional but has infinitely many vectors/rays and infinitely many frame
constraints. The bridge uses real/complex completeness and compactness. Thus this is not
an inference from finitely many measured frames alone, or a construction of the continuum
from a finite carrier. A physical instrument's one tolerance/resolution pair cannot discharge
`forall epsilon > 0, exists delta > 0`.

## Handoff to Claude: a concrete route forward

### A. Finish the available C^3 completion result first

Package the existing `F_ι`, `F_smul`, `continuousOn_F`, `isFrameFunctionC_F`,
`born_of_uniformlyRayContinuous`, `tomography_trace_one`, and `tomography_unique` into one
theorem: a uniformly ray-continuous nonnegative rational frame function has a unique
continuous extension to complex rays, represented by the embedded tomography density matrix.
Use density to extend rational quadratic-form nonnegativity to complex PSD and to identify
the extension everywhere. This is a bounded formalization task, not the open regularity hinge.

Prove the general converse instance `IsUniformlyRayContinuous (quadRay rho)` as well.
For a Hermitian matrix, phase-align unit representatives and use

`|q_rho(u) - q_rho(v)| <= 2 ||rho|| sqrt(2 raySinSq(u,v))`.

Choose a rational bound for the coefficients/operator norm to obtain a rational delta.
The constant-instance review check establishes nonvacuity; it does not replace this converse.

### B. Attack the nonnegative pointwise question before the signed version

This gives the useful a priori bound `0 <= f <= 1`, hence a bounded tomography residual.
Try to propagate oscillation to one fixed rational ray, or construct exact finite frame
certificates that avoid choosing a changing near-maximizer.

A precise search target is the following sufficient condition. For each fixed rational x,
find finite rational-frame consequences, for eta tending to zero, of the form

`|g(x)| <= A(x) max_j |g(y_(eta,j))| + B r_eta`,

where g is a bounded zero-weight residual vanishing at the nine tomography anchors,
`|g| <= B`, all the y's approach those fixed anchors uniformly over the finite list,
`r_eta -> 0`, and A(x) is independent of eta and of g. Pointwise continuity at those finitely
many fixed anchors then forces g(x)=0. The uniformly bounded certificate coefficients are
the difficult requirement; allowing them to grow like the inverse tolerance recreates the
original problem.

Exact-rational linear programming/dual certificates can search for this mechanism, followed
by an independent exact checker and a symbolic theorem for the family. A failed finite
search proves no impossibility, and one finite certificate proves no global theorem. Formalize
the arbitrary-chain rational approximation lemma if it helps, but do not mistake it for the
needed error bound. Do not assume projector linearity: the existing equivalence already makes
that essentially the desired rigidity conclusion. This review did not settle the pointwise
question or establish that it is an open problem throughout the literature.

### C. Keep the effect-additive route separate

The repository's positive, normalized effect-additive valuation route is another route to
Born representation over rational fields. An operational account of coarse-graining and
randomization could justify that stronger premise. Orthogonal projection frame additivity
alone does not imply it here, as the explicit rational counterexamples show. This distinction
also appears in [Caves, Fuchs, Manne, and Renes](https://arxiv.org/abs/quant-ph/0306179).
Do not import the already-defined Born pairing to justify the premise.

### D. Separate continuous coordinates, all finite dimensions, and infinite dimension

1. **All complex states in dimension three:** rational-valued tomography only reconstructs
   Gaussian-rational coefficients. General complex density matrices require real-valued
   data on rational rays, or an approximation/completion theorem. One constructive density
   route is to approximate a matrix factor B by Gaussian-rational B_k and normalize
   `B_k B_k* / trace(B_k B_k*)`; positivity and trace one are exact at each nonzero step.
   Prove convergence and probability error bounds explicitly.
2. **C^n, n >= 3:** glue compatible three-dimensional restrictions into a global Hermitian
   quadratic form. Prove subspace weight independence, compatibility, PSD, trace, and uniqueness.
   It is not enough to say dimension three is representative. For the full nonnegative
   continuum Gleason theorem, formalize the automatic-continuity step as well; the
   [Cooke-Keane-Moran proof](https://rogermcooke.net/rogermcooke_files/Elementary%20Proof%20of%20Gleasons%20Theorem.pdf)
   is relevant classical source material, not a discharged local dependency.
3. **A separable infinite-dimensional Hilbert space:** require compatible finite compressions,
   a bounded positive form, and the normalization/normality or countable-additivity hypotheses
   that yield a trace-class state. If using a sequence of finite states, prevent escape of
   trace, for example by uniform tightness on finite-rank projections. The states
   `|e_n><e_n|` have trace one but converge weakly to zero, so finite-dimensional positivity
   and normalization alone do not preserve trace one in a limit. Compressing a state does
   not in general leave every finite block normalized; do not silently renormalize them.

The recommended order is A, the nonnegative version of B, and then the precise dimension/completion
targets in D. C is an explicitly stronger operational route that can proceed independently.
The DAG records these boundaries; none of these proposed steps is labeled as a completed theorem.
