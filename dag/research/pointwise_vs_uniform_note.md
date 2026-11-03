# Pointwise versus uniform ray continuity for frame functions on ℚ(i)³

Bounded-time assessment, 2026-11-03, corrected the same day after maintainer review. AuthorityEffect: None.

Companion to the DAG nodes `FQ-GLEASON-QI3-UNIFORM-RAY-CONTINUITY` (CONDITIONAL) and
`FQ-GLEASON-QI3-POINTWISE-TO-UNIFORM` (OPEN). The original pointwise-continuity targets and their statuses on
`TFQ-0307` / `FQ-GAP-BORN-UNIQUENESS-GLEASON` and `TFQ-1055` / `FQ-GLEASON-QI3-FRAME-FUNCTIONS` are unchanged.

## What is proved (PR #500)

`BornFinite.GleasonBridge.born_of_uniformlyRayContinuous` in `lean4/GleasonGaussianBridge.lean`.
Kernel-checked, 0 sorry, axioms `propext`, `Classical.choice`, `Quot.sound`. Hypotheses, recorded literally:

- `IsFrameFunction f`: `f : GVec → ℚ` with `f u + f v + f w = 1` for every triple `u, v, w` of nonzero,
  pairwise orthogonal vectors of ℚ(i)³. This is the **signed** version: no sign condition on `f`.
- `IsUniformlyRayContinuous f`: for every rational `ε > 0` there is a rational `δ > 0` such that
  `|f u − f v| < ε` for all nonzero `u, v` with `raySinSq u v < δ`, where
  `raySinSq u v = 1 − |⟨u,v⟩|² / (⟨u,u⟩⟨v,v⟩)`. `raySinSq` is a **squared ray distance** (phase and scale
  invariant, rational-valued); its square root is the corresponding metric on rays.

Conclusion: `f v = quadRay (tomographyForm f) v` for every nonzero `v`, that is `f(v) = ⟨v, ρ v⟩ / ⟨v, v⟩` with
`ρ` the Hermitian trace-one matrix reconstructed from the nine tomography rays.

The **nonnegative** version (`IsNonnegFrameFunction f`, the one the original targets need) is the special case
of a nonnegative `f`; the theorem as proved covers all signed frame functions.

## Uniform continuity is a declared input

`IsUniformlyRayContinuous f` is not derived from anything in the repository. It is a mathematical input that
requires justification before the theorem applies to a given `f`. In particular, a finite instrument whose
resolution is known at one tolerance supplies one `(ε, δ)` pair; it does not by itself supply the `∀ε ∃δ`
guarantee the hypothesis demands.

The hypothesis is not vacuous: on paper, every `quadRay ρ` (any Hermitian `ρ`) is uniformly ray continuous, since
with unit representatives `|⟨û,ρû⟩ − ⟨v̂,ρv̂⟩| ≤ 2‖ρ‖·√(2·raySinSq u v)`, which gives a rational `δ` from the
coefficient bound of `ρ`. This instance is not formalized in the repository; no Lean declaration instantiates
`IsUniformlyRayContinuous` (noted by the 2026-11-03 review, left for later work).

## The remaining question (`FQ-GLEASON-QI3-POINTWISE-TO-UNIFORM`)

Does Archimedean continuity at every nonzero rational vector (`IsArchimedeanContinuousEverywhere f`: for each
nonzero `v₀` and each `ε > 0` some `δ > 0` with `|f v − f v₀| < ε` whenever `distSqVec v v₀ < δ`) imply
`IsUniformlyRayContinuous f` when `f` is a frame function? Two versions are to be distinguished:

- for all signed frame functions (`IsFrameFunction f`);
- for nonnegative frame functions only (`IsNonnegFrameFunction f`), which is what the original targets need.

The signed version implies the nonnegative one. Neither is settled.

For arbitrary functions on a dense, non-compact domain the implication fails. A topological illustration only,
not a frame function: `h(q) = 1` if `q > √2/2` and `h(q) = 0` otherwise, on `q ∈ ℚ ∩ [0,1]`. Since `√2/2` is
irrational, `h` is constant near every point of its domain, so it is continuous at every point, and it is not
uniformly continuous because rationals on both sides of `√2/2` come arbitrarily close.

## Why the ε-version of Cooke–Keane–Moran did not close

With pointwise continuity the maximiser of `f` cannot be placed at a rational ray; one works with a rational
pole `p` where `f(p) > sup f − ε`. The descent lemma along slope circles then only gives `f(a) ≥ f(b) − ε` per
step. The latitude-constancy proposition needs chains of Piron steps from latitude `l(a)` down to latitude
`l(b)`, and the number of steps grows like `1 / (l(a)/l(b) − 1)`: comparing two rays of nearly equal latitude
costs unboundedly many steps, each losing `ε`. The accumulated error `n·ε` is therefore not small exactly where
latitude constancy is needed. Uniform continuity lets `ε → 0` with the pole fixed; pointwise continuity at
rational rays does not pin the pole. Several variants of this route were tried on 2026-11-02 and 2026-11-03 with
the same outcome.

A separate obstruction remains in the rational chains themselves. Two-step Piron multiplier products
`(1 + ti)(1 + si)` with `t, s` real (so in particular rational) are **not** dense in ℂ: writing
`(1 + ti)(1 + si) = a + bi` gives `a = 1 − ts`, `b = t + s`, hence `b² + 4(a − 1) = (t − s)² ≥ 0`, so every such
product lies in the closed region `a ≥ 1 − b²/4`, which excludes a neighbourhood of `0`. An earlier draft of
this note claimed these products were dense and that this bridged the reachability gap; that claim was false and
is withdrawn. No multiplier result that restores reachability is established here. This observation does not
affect the uniform-continuity theorem above, which does not use rational Piron chains.

## What is known about counterexamples

Cap argument. A zero-weight residual `g` (frame sum `0`) supported inside a cap of angular radius below 45°
vanishes on the cap, provided each ray of the cap can be completed to an admissible rational orthogonal frame:
such a frame has pairwise orthogonal members, so it meets the cap in at most one ray, and the frame identity
forces `g = 0` there. This rules out that particular localized construction, a perturbation of a Born form
supported in a small cap. It does not show that every counterexample must be global, that one would need
Zorn/Hamel methods, that it would lack a finite description, or that it could not be found by finite
computation. No global counterexample has been established, and none has been excluded.

The known residuals `s3`, `s7`, `sp` are valuation-defined and nowhere Archimedean continuous, so they are not
candidates.

## Record

- Conditional theorem: `FQ-GLEASON-QI3-UNIFORM-RAY-CONTINUITY` (CONDITIONAL), hypotheses as listed above.
- Open sub-question: `FQ-GLEASON-QI3-POINTWISE-TO-UNIFORM` (OPEN). What would settle it: an `ε`-free rigidity
  argument that fixes a pole, or a pointwise-continuous non-quadratic frame function.
- The pointwise targets in `TFQ-0307` / `TFQ-1055` remain unresolved. Neither the unsuccessful proof attempts
  nor the conditional theorem settle them.
