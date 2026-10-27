# TFQ-0119: `cdx2.pontryagin_completion_classification` Stays Open — Dyadic Direct Limit Is Not the Completed Circle

- **Node ID**: `TFQ-0119`
- **Stage**: `CONTINUUM_INTERFACE`
- **Status**: `OPEN`
- **Claim Class**: `L4D`
- **Lean 4 Module**: `lean4/DyadicDirectLimitCircle.lean`
- **Independent Checker**: `checks/independent/tfq-0119.py`
- **AuthorityEffect**: `None`

## 1. Statement & Scope

> `circle_haar.lean` imports a normalized Haar measure and states an injective cyclic inclusion. Its header says the dyadic direct limit is not asserted to equal the completed circle. The package README treats those as different objects. What is finite is the cyclic inclusion and the character identity the ledger can mark mechanized. What is not discharged is metric completion for every continuous observable, Pontryagin completion classification, and the continuum limit. A circle integral is not the Einstein equation and not quantum gravity.

## 2. Formalized Finite Surface & Non-Equivalence Fences (`lean4/DyadicDirectLimitCircle.lean`)

1. **Dyadic Direct-System Compatibility & Finite Haar Partition (`dyadicRatVal`)**:
   - `dyadic_direct_limit_step_invariant`: proves single-step compatibility `dyadicRatVal (k + 1) (2 * m) = dyadicRatVal k m` for `dyadicRatVal k m = m / 2^k`.
   - `dyadic_direct_limit_multi_step_invariant`: proves multi-step compatibility `dyadicRatVal (k + d) (2^d * m) = dyadicRatVal k m`.
   - `dyadic_haar_uniform_sum_one`: proves `(2^k) * dyadicRatVal k 1 = 1` at every finite dyadic level $k$.
2. **Dyadic Direct Limit Is Not the Completed Circle (`1/3 ∉ Z[1/2]`)**:
   - `two_pow_mod_three_nonzero`: proves by induction on $k$ that $(2^k) \bmod 3 \in \{1, 2\}$ and $(2^k) \bmod 3 \ne 0$.
   - `three_mul_ne_two_pow`: proves $3m \ne 2^k$ for all $k, m \in \mathbb{N}$.
   - `one_third_not_dyadic_fraction`: proves `dyadicRatVal k m ≠ 1 / 3` for all $k, m \in \mathbb{N}$, establishing that the rational 3-torsion circle point $1/3 \in \mathbb{R}/\mathbb{Z}$ is omitted from the uncompleted dyadic direct limit $\mathbb{Z}[1/2]/\mathbb{Z}$.
3. **Uncompleted Dyadic Cauchy Sequence Approximating $1/3$ (`cdx2.pontryagin_completion_classification` Fence)**:
   - `four_pow_sub_one_mod_three_zero`: proves $(4^n) \bmod 3 = 1$ and $(4^n - 1) \bmod 3 = 0$, so $(4^n - 1)/3$ is an exact integer numerator over $4^n = 2^{2n}$.
   - `dyadic_cauchy_approx_one_third_residual`: proves that `dyadicOneThirdResidual n = 1 / 3 - dyadicOneThirdApprox n` equals $1 / (3 \cdot 4^n)$ and satisfies `dyadicOneThirdResidual (n + 1) = (1 / 4) * dyadicOneThirdResidual n`.
   - `dyadic_cauchy_approx_strictly_below_one_third`: proves `0 < dyadicOneThirdResidual n`, `dyadicOneThirdApprox n < 1 / 3`, and `dyadicOneThirdApprox n ≠ 1 / 3` at every finite stage $n$.
   - `dyadic_cauchy_approx_table`: verifies the stage-$1..4$ dyadic approximations $(1/4, 5/16, 21/64, 85/256)$ and residuals $(1/12, 1/48, 1/192, 1/768)$.

## 3. Independent Verification & Mutation Receipts

- **Independent Checker (`checks/independent/tfq-0119.py`)**: `checks=892 direct_limit=298 non_dyadic=516 cauchy_fence=78 failures=0`.
- **Lean Mutation Gate (`dag/research/campaign_tfq-0119_lean_mutation.json`)**: 6/6 semantic mutations killed (`all_killed=true`).

## 4. Claim Hygiene Summary

1. **What it supports**: Supports exact rational verification of dyadic direct-system inclusion compatibility, finite level-$k$ Haar partition normalization, and the explicit non-equivalence fence (`1/3` omitted from $\mathbb{Z}[1/2]$ and approached by an uncompleted dyadic Cauchy sequence) keeping `cdx2.pontryagin_completion_classification` open.
2. **What it does not support**: Does not support metric completion for continuous observables, Pontryagin completion classification, a continuum limit, the Einstein equations, or quantum gravity.
3. **Narrowest defensible claim**: The finite dyadic direct-system compatibility and Haar partition identities hold over $\mathbb{Q}$, while the uncompleted dyadic direct limit is strictly narrower than the completed circle (`cdx2.pontryagin_completion_classification`).
4. **Next test needed**: Proceed to `TFQ-0123`.
