# Mathematical review and boundaries

AuthorityEffect: None.

## What is specified

- **Continuity.** The finite carrier (rational matrices, Gaussian-rational or cyclotomic entries)
  carries no topology, so "strong continuity" has no finite meaning. The strongest finite notion of
  continuous time is a ℚ-parameter group: `U : ℚ → G` with `U 0 = 1` and `U (s + t) = U s * U t`.
  Any real one-parameter group restricts to one, so every obstruction to a ℚ-parameter group is an
  obstruction to continuous time.
- **Discrete evolution.** One reversible step `u` generates the ℤ-action `k ↦ u ^ k`.
- **Generator selection.** A "generator" at the finite level is a half-step (or, more generally, an
  m-th root) of the step. Half-steps are never unique: `−V` squares to the same matrix.

## What is derived

1. A ℚ-parameter group is determined on ℤ by its unit step (`U k = U 1 ^ k`) and requires an m-th root
   of the unit step for every m (`U (1/m) ^ m = U 1`).
2. The rational 2×2 Pythagorean rotation is a reversible ℤ-action over ℚ (all powers orthogonal) but
   has no rational half-step: a square root commutes with it, so it has the form `p·1 + r·J`, and the
   equations `p² − r² = 3/5`, `2pr = 4/5` force `p² = 4/5`, which is not a rational square because
   `Rat.mul_self_den` would make 5 a perfect square. Hence no ℚ-parameter group of invertible rational
   2×2 matrices passes through it. Continuous time through this step needs the carrier extension
   ℚ(√5) (the half-angle has cosine 2/√5).
3. Generator non-uniqueness holds in any ring with a ℚ-module structure, in particular on rational
   n×n matrices.

## What is not derived

- Topology, real completion, exponentials and logarithms are not constructed; the Stone theorem is
  not used or proved.
- The general statement "every ℚ-parameter group of matrices over ℚ(i) is trivial" is not proved. Its
  natural proof uses unique factorisation in ℤ[i] (norms along the group are perfect m-th powers for
  every m, and the unit-circle group of ℚ(i) is torsion times free abelian). It is recorded as the
  open obligation of this node.
- Causal order between events remains an external datum (unchanged).

## Relation to existing material

`H055DiscreteDynamicsStone` (no Bool half-step; two scaled ℚ(i) interpolants of the swap),
`H016ContinuousDynamicsFork`, `H061DynamicsDichotomy` (Pythagorean residues) and `PromptDynamics`
(aliasing) remain as they are. The uncommitted working-copy modules `U1PythagoreanObstruction.lean`
and `U1PowerMapInjectivity.lean` establish the scalar facts on the rational circle; this run does not
import them and proves its 2×2 statement independently.

## Mechanical notes

Lean 4.33.1, pinned Mathlib cache, targeted imports; `tools/replay.py` receipt
`discrete_time_spec_01`; `tools/seal.py receipts` checks exit codes, custody digests, absence of
`sorry`/`axiom`/`opaque`/`unsafe`, absence of diagnostics, and that every printed axiom list is within
`{propext, Classical.choice, Quot.sound}`.
