Status: AI-drafted, awaiting human review.

# FSP-U1-WILSON-ACTION

AuthorityEffect: None.

The node statement is narrowed in two places: the coupling condition `beta_g >= 0` is written explicitly, and links are taken to be functions of ordered vertex pairs on a finite family of closed oriented paths. The Lean module `lean4/CampaignFspU1WilsonAction.lean` states the narrowed claim as `fsp_u1_wilson_action`.

## Setting

Let `V` be any set of vertices. A `U(1)` link field is a function `U : V × V → U(1)`, where `U(1) = {z ∈ ℂ : |z| = 1}`. A closed oriented path is a base vertex `v_0` and a vertex list `v_1, ..., v_n` with `v_n = v_0`. Its holonomy is the ordered product

```
U_p = U(v_0, v_1) U(v_1, v_2) ... U(v_{n-1}, v_n).
```

A plaquette family is a finite index set `P` with a closed path `p` for each index. The Wilson action at coupling `β ∈ ℝ` is

```
S_β(U) = β Σ_{p ∈ P} (1 - Re U_p).
```

A local gauge transformation is any `g : V → U(1)`. It acts by `(gU)(a, b) = g(a) U(a, b) g(b)^{-1}`. In angle form, `U(a, b) = exp(i A(a, b))` with `A(a, b)` real, `g(v) = exp(i θ(v))`, and the action is `A(a, b) ↦ A(a, b) + θ(a) - θ(b)`.

On the periodic hypercubic lattice `(ℤ/L)^d`, the plaquette at site `x` in the plane `μ < ν` is the closed path `x → x+μ̂ → x+μ̂+ν̂ → x+ν̂ → x`. With the orientation convention `U(b, a) = U(a, b)^{-1}` its holonomy is the familiar `U_μ(x) U_ν(x+μ̂) U_μ(x+ν̂)^{-1} U_ν(x)^{-1}`.

## Derivation

**Step 1 (holonomy covariance, any group).** For a path `a = v_0, v_1, ..., v_n`,

```
(gU)-holonomy = g(v_0) U(v_0,v_1) g(v_1)^{-1} g(v_1) U(v_1,v_2) g(v_2)^{-1} ... g(v_n)^{-1}
              = g(v_0) · U-holonomy · g(v_n)^{-1}.
```

The inner factors `g(v_k)^{-1} g(v_k)` cancel. The argument is induction on the length of the list. It uses only associativity and inverses, so it holds in every group (`holonomy_gaugeAct`).

**Step 2 (closed paths).** For a closed path `v_n = v_0`, Step 1 gives `(gU)_p = g(v_0) U_p g(v_0)^{-1}` in any group (`loopHolonomy_gaugeAct_conj`). In a commutative group such as `U(1)` this equals `U_p` (`loopHolonomy_gaugeAct`).

**Step 3 (gauge invariance of the action).** Every term of `S_β(gU)` equals the matching term of `S_β(U)` by Step 2, so `S_β(gU) = S_β(U)` for every `β`, every finite plaquette family and every `g` (`wilsonAction_gauge_invariant`).

**Step 4 (angle form).** `exp(i(A + θ(a) - θ(b))) = exp(iθ(a)) exp(iA) exp(iθ(b))^{-1}`, so the angle shift is the gauge action of `g = exp(iθ)` (`linkOfAngle_gaugeAngle`). The holonomy of angle links is `exp(i Σ A)` along the path (`holonomy_linkOfAngle`), so `Re U_p = cos(Σ_p A)` and `S_β = β Σ_p (1 - cos Σ_p A)` (`wilsonAction_linkOfAngle`).

**Step 5 (nonnegativity).** For `|z| = 1`, `Re z ≤ |z| = 1`, so `1 - Re z ≥ 0` (`one_sub_re_nonneg`). A sum of nonnegative terms times `β ≥ 0` is nonnegative (`wilsonAction_nonneg`).

**Step 6 (equality case).** For `|z| = 1`, `Re z = 1` forces `(Im z)^2 = 1 - 1 = 0`, so `z = 1`. Hence for `β > 0`, `S_β(U) = 0` exactly when every plaquette holonomy is `1` (`wilsonAction_eq_zero_iff`).

**Step 7 (the coupling condition is needed).** Take one vertex, one self-link plaquette `v_0 → v_0`, link phase `-1` and `β = -1`. Then `U_p = -1` and `S = -1 · (1 - (-1)) = -2 < 0` (`wilsonAction_negative_beta_witness`, `wilsonAction_nonneg_needs_beta`). So nonnegativity does not hold without `β ≥ 0`.

**Step 8 (lattice instance).** The hypercubic plaquettes above are closed paths, so Steps 3 and 5 apply to `hypercubicWilson` (`hypercubicWilson_gauge_invariant`, `hypercubicWilson_nonneg`).

## Lean evidence

Module `CampaignFspU1WilsonAction`, built with `lake build CampaignFspU1WilsonAction` (Lean 4.35.0, Mathlib `56a005855ea17e0b0958f73ec801ae140b0a1679`). The twelve `#print axioms` lines at the end of the file report only `propext`, `Classical.choice` and `Quot.sound`. The receipt is `dag/research/campaign_fsp-u1-wilson-action_lean_replay.json`. A mutation run (`dag/research/campaign_fsp-u1-wilson-action_lean_mutation.json`) changes one ingredient at a time (the inverse in the gauge rule, the sign of `Re U_p`, the hypothesis `β ≥ 0`, the closing vertex of the plaquette, the sign of `θ(b)`, the link factor in the holonomy) and records whether Lean rejects each mutant.

## Independent check

`checks/independent/fsp-u1-wilson-action.py` imports no repository code. It uses unit complex numbers with rational coordinates, `((1 - t^2) + 2ti)/(1 + t^2)`, held as exact fractions, on periodic lattices `(d, L) = (2,3), (2,4), (3,2), (3,3), (4,2)`. It recomputes gauge invariance of every plaquette holonomy and of `S` at `β = 0, 1, 7/2`, nonnegativity, the plaquette count `L^d d(d-1)/2`, open-path covariance, the composition law of gauge transformations, preservation of `U(b,a) = conj U(a,b)`, the equality case on pure-gauge and random fields, the one-plaquette value `-2` at `β = -1`, and negative `S` at `β = -1` on a non-flat field. It confirms that 20 single-link non-gauge rotations and one wrong gauge rule each change some plaquette. A SymPy part checks `Re Π exp(iA) = cos Σ A` and `S(A + dθ) = S(A)` exactly for angles in `(π/6)ℤ` and `(π/4)ℤ`. The last run reported `checks=6159 distinct=21 failures=0`. These are finite checks; they are not a proof.

## What is proved

For every vertex type, every finite family of closed oriented paths, every real `β`, every `U(1)` link field and every gauge function, the Wilson action is gauge invariant, both for `g : V → U(1)` and for angle shifts. It is nonnegative when `β ≥ 0`. For `β > 0` it is zero exactly on fields whose plaquette holonomies are all `1`. The hypothesis `β ≥ 0` cannot be dropped. Holonomy covariance and closed-path conjugation hold over any group.

## What is assumed

Links are functions of ordered vertex pairs. On a periodic lattice with `L ≤ 2` this identifies the two parallel links between neighbouring sites, so the lattice instance is the vertex-pair model there; for `L ≥ 3` each ordered neighbour pair is one link. The orientation convention `U(b, a) = U(a, b)^{-1}` is not needed for the theorems; it is preserved by gauge transformations (`gaugeAct_reversal`). The coupling `β_g` is a real parameter with `β_g ≥ 0` for the nonnegativity part. Mathlib's `Circle`, `Complex.exp` and `Real.cos` are the definitions of `U(1)`, `exp(i·)` and `cos`.

## What is open

The source supplies no fermion-sign consequence of this fact, and none is claimed. Not addressed: the non-abelian Wilson action (Step 2 gives only conjugation of `U_p`, so invariance there needs a class function such as the trace), reflection positivity, a transfer matrix, gauge fixing, the continuum limit, and the multigraph lattice with distinct parallel links for `L ≤ 2`. The downstream nodes `FSP-WILSON-DIRAC-GAMMA5`, `FSP-THETA-TERM-COMPLEX-WEIGHT` and `FSP-SU2-ADJOINT-REAL-DET` keep their own obligations.
