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

## 3. Claim Boundaries

- **What would support completion:** An explicit finite algorithm that takes $(S, \varepsilon)$, produces a finite family of test questions, and proves that if a state can be distinguished under noise $\varepsilon$, the family of questions achieves minimum or bounded cost with guaranteed error control.
- **What this document does NOT support:** It does not assert that the problem is solved, nor that heuristic sampling provides a valid mathematical proof.
