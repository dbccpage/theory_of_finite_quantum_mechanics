# Pointwise versus uniform ray continuity for frame functions on Q(i)^3

Assessment updated 2026-11-03 after independent review of PR #500 at
`45b0b093921aa0281969f92da18694e2e89c3cc4`. AuthorityEffect: None.

Full findings, independent rebuild evidence, and the handoff to Claude are in
[the review](pr500_review/review.md) and [its manifest](pr500_review/manifest.json).

## Distinct questions and statuses

- **TFQ-1055 / FQ-GLEASON-QI3-FRAME-FUNCTIONS:** the original statement has **no continuity
  hypothesis**. Its universal quadratic-rigidity assertion is REFUTED, even for nonnegative
  functions, by `exoticQi3_isNonnegFrameFunction` and `exoticQi3_not_quadratic`. The original
  decision question is retained verbatim; the zero-one and specified-extension alternatives
  have their separate negative answers. This is not an open pointwise-continuity statement.
- **TFQ-1056 / FQ-GLEASON-QI3-UNIFORM-RAY-CONTINUITY:** CONDITIONAL on uniform ray continuity.
- **TFQ-1057 / FQ-GLEASON-QI3-POINTWISE-TO-UNIFORM:** OPEN; signed and nonnegative cases separate.
- **TFQ-1058 / FQ-GLEASON-FRAME-CARRIERS:** the supplied carriers and frame definitions only.
- **TFQ-1059 / FQ-GLEASON-C3-CONTINUOUS-FRAME-FUNCTIONS:** the proved continuous signed C^3
  theorem, CONDITIONAL on continuity away from zero.
- **TFQ-1060 / FQ-BORN-QI3-CONTINUUM-COMPLETION:** OPEN packaging of the existing extension
  lemmas into a unique complex density-matrix extension and the general quadratic converse.

TFQ-0307 remains CONDITIONAL. Its broad Born-uniqueness/operational target is not the literal
pointwise statement either. None of these results derives the Hilbert carrier or regularity
premise from finite operational data.

## What is proved

`BornFinite.GleasonBridge.born_of_uniformlyRayContinuous` assumes:

- `IsFrameFunction f`: `f : GVec -> Q`, with sum one on every nonzero orthogonal triple in
  Q(i)^3. This is signed; no positivity is assumed.
- `IsUniformlyRayContinuous f`: for every rational epsilon > 0, a rational delta > 0 works
  for **all** nonzero u,v with `raySinSq u v < delta`, where
  `raySinSq u v = 1 - |<u,v>|^2 / (<u,u><v,v>)`.

It concludes `f v = quadRay (tomographyForm f) v` for every nonzero v. The tomography
trace-one and uniqueness results are already available separately. Nonnegative inputs are
a special case and imply nonnegativity of the rational quadratic numerator.

`raySinSq` is a squared ray distance; its square root is the metric on rays. The proof
extends f to a continuous frame function on C^3 and applies the continuous complex theorem.
The independent eight-module rebuild and 308-report axiom audit pass with only `propext`,
`Classical.choice`, and `Quot.sound`. Of the reports, 302 cover all named declarations in
the four new modules, four supporting results, and two review lemmas.

Uniform continuity is supplied, not derived. A finite instrument's resolution at one
tolerance gives one epsilon-delta pair, not the for-all-epsilon guarantee. The review
formally instantiates the hypothesis with the constant frame function 1/3. The general
instance for every Hermitian `quadRay rho` remains to be formalized. On paper, phase-aligning
unit representatives gives
`|q_rho(u)-q_rho(v)| <= 2 ||rho|| sqrt(2 raySinSq(u,v))`, hence a rational delta from a
rational coefficient bound. The constant instance does not replace this general converse.

## The remaining pointwise question

Does `IsArchimedeanContinuousEverywhere f` (pointwise epsilon-delta continuity at each
nonzero rational vector, using `distSqVec`) imply uniform ray continuity for a frame
function? The signed version implies the nonnegative version, which is enough for the
probability-valued target. Neither is settled by this review.

For arbitrary functions on a dense noncompact domain, no: on Q intersected with [0,1],
take h(q)=1 above sqrt(2)/2 and h(q)=0 below it. It is locally constant at every rational
point but not uniformly continuous. This is a topological illustration, not a frame function.

## What the near-maximum argument does and does not show

First restrict to a bounded-above frame function before choosing a rational p with
`f(p) > sup f - epsilon`. Nonnegative frame functions satisfy 0 <= f <= 1 by completion
of each ray to a frame. Such boundedness is not supplied for the general signed,
pointwise-continuous rational case.

The known near-maximum descent gives an epsilon loss per step. The constructed chains
lengthen near equal latitudes, and no argument controls the accumulated loss while the
rational near-maximizing pole changes with epsilon. This is a failure of the attempted
proof, not a lower bound on every possible argument. The uniform bridge avoids it by
extension and compactness: an actual maximum exists on the complex sphere and may be at
an irrational ray. Uniform continuity does not make a fixed rational pole a maximizer.

Two-step products `(1+ti)(1+si)=a+bi` obey `b^2+4(a-1)=(t-s)^2 >= 0`, even with real
parameters, so they are not dense in C. The earlier two-step density claim remains withdrawn.
However, this is not a new obstruction to arbitrary finite-chain approximation:
`GleasonReal.exists_chain_eq` expresses every m with |m|>1 as a finite real-parameter
product. For that fixed length N, the product is continuous in R^N and Q^N is dense, so
rational products approximate m. All factors have modulus >=1, and approximation from
outside reaches the unit circle in the closure. Thus the closure of **all finite** rational
products is exactly {|m|>=1}, not C. This paragraph is a paper deduction from the checked
real theorem, not a new Lean declaration. It gives neither a uniform length bound nor
the required accumulated-error control.

## Counterexamples and a constructive search target

A zero-weight residual supported in an angular cap of radius <45 degrees vanishes if
each ray completes to an admissible rational orthogonal frame: a frame can meet that cap
in at most one ray, and the frame identity forces its value to zero. This excludes that
support construction only. It proves neither that a counterexample must be a Zorn/Hamel
object nor that a finite description or finite search could never discover one.

The existing selective-oscillation results at `tomo_e1` rule out continuity everywhere
for the cited nonzero finite valuation combinations under their explicit prime/system
hypotheses. The cited declarations do not prove that every `sp` is discontinuous at every
ray; “nowhere continuous” is therefore not used as a formal result here.

For the nonnegative case, try fixed-ray oscillation propagation or exact rational frame
certificates which bound a residual value at x by values near the fixed tomography anchors
with coefficients bounded independently of the approximation tolerance. The full review
states a sufficient certificate inequality. Finite exact search can suggest and verify
individual certificates; a global theorem needs a symbolic family with the coefficient
bound proved. Projector linearity must not be silently assumed, since it already implies
the desired rigidity. The review also gives a separate effect-additive route and the
additional obligations for arbitrary complex states, higher finite dimensions, and
infinite-dimensional trace-class states.
