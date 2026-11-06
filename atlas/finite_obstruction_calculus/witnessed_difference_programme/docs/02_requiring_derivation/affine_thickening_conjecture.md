# Active Derivation Target: Affine Support Noise Thickening

**Status:** OPEN / REQUIRING_DERIVATION  
**Origin:** Monograph Appendix Y & README §"Scope and next question"  
**Target ID:** `WDP-AFFINE-THICKENED-MEASUREMENT-REDUCTION` / `TFQ-0577`

---

## 1. Problem Statement

In Appendix Y, the Witnessed Difference Programme derives exact observation and recovery costs from joint report supports:
- It establishes the existence of finite cost witnesses.
- It constructs such witnesses explicitly for finite unions of rational affine segments where the fiber of any single observation coordinate over the latent state space is finite.

The open mathematical challenge is to construct a **finite reduction for affine supports thickened by bounded independent measurement error**:
$$\text{Supp}_\varepsilon(S) = \{ x + e : x \in S, \|e\|_\infty \le \varepsilon \}$$
where $S \subset \mathbb{R}^k$ is a finite union of rational affine segments, and $\varepsilon > 0$ represents independent measurement noise.

---

## 2. Mathematical Obstruction

When affine supports are thickened by non-zero noise $\varepsilon > 0$:
1. A single observation reading no longer corresponds to a discrete set of latent state points; it leaves a continuum or broad interval of latent parameters.
2. The discrete finite-fiber argument of Appendix Y (which counts points in the preimage of projection maps) breaks down because preimages are infinite sets (non-trivial intervals).
3. Therefore, finite cost witness construction requires a replacement based on:
   - Covering numbers or dyadic cell partitions.
   - Robust cell-boundary disambiguation with sound abstention tokens (`NO_RULE`).
   - Finite witness certificates that bound the worst-case recovery cost uniformly over all noise realizations.

---

## 3. Claim Boundaries & Finite Reduction Status (`TFQ-0581`)

- **Discharged Finite 1D Rational Interval Reduction (`WdpBatch6.lean`, `TFQ-0581`):** `lean4/WitnessedDifference/WdpBatch6.lean` formalizes the 1D rational interval cell partition `classifyThickenedAffine` around $[a, b]$ with measurement margin $\varepsilon \ge 0$, proving:
  1. `thickened_affine_cell_soundness` and `thickened_affine_no_false_verdict`: every noise realization $\delta \in [-\varepsilon, \varepsilon]$ preserves true membership on `CertifiedInside` ($[a + \varepsilon, b - \varepsilon]$) and true non-membership on `CertifiedOutside`.
  2. `thickened_affine_boundary_abstains`: every point in the boundary uncertainty collars $[a - \varepsilon, a + \varepsilon)$ and $(b - \varepsilon, b + \varepsilon]$ returns `AbstainBoundary` (`ABSTAIN_NO_RULE`).
  3. `thickened_affine_dyadic_covering_bound`: dyadic cell covering bound for rational intervals.
- **What remains open:** Higher-dimensional polyhedral cell complexes ($k > 1$) and continuum Lebesgue/Gaussian measure extensions beyond the 1D rational interval reduction.
