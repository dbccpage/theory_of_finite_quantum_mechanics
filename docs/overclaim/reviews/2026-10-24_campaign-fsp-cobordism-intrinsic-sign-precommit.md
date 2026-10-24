# Pre-Commit Claim Hygiene & Scope Review: `FSP-COBORDISM-INTRINSIC-SIGN` (`TFQ-1211`)

- **Date**: 2026-10-24
- **Branch**: `campaign/fsp-cobordism-intrinsic-sign`
- **Target Node**: `FSP-COBORDISM-INTRINSIC-SIGN` (`TFQ-1211` / `FSP-DERIV-047`, `FERMION_SIGN`)
- **Status**: `OPEN` (narrowed to exact finite spectral-asymmetry, mapping-torus determinant, Arf Gaussian sign-sum, mod-2 cobordism pairing, and class-specific representation no-go/scope-fence theorems, `E1 -> E3`)

## 1. What It Supports
- Formalizes in [`lean4/CampaignFspCobordismIntrinsicSign.lean`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignFspCobordismIntrinsicSign.lean) (`L4D`, 10 theorems, 0 `sorry`, standard axioms only, 6/6 semantic mutations killed) and [`checks/independent/fsp-cobordism-intrinsic-sign.py`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/checks/independent/fsp-cobordism-intrinsic-sign.py) (`checks=1230`, `failures=0`) the finite algebraic prototypes and class-specific scope boundaries of `TFQ-1211`:
  1. Discrete spectral asymmetry oddness, particle-hole doublet cancellation, and single-mode zero-crossing jump $\Delta\eta = +2$ ($\Delta(\eta/2) = 1$) flipping $(-1)^k$.
  2. Finite $2 \times 2$ mapping-torus Dirac block $\det(\mathrm{diracMappingBlock}(m, s)) = m^2 - s$ reversing sign between untwisted antiperiodic ($s = -1, \det = +1$) and $\mathbb{Z}_2$-twisted periodic ($s = +1, \det = -1$) sectors at $m = 0$.
  3. Arf-0 ($+2$) vs Arf-1 ($-2$) Gaussian sign sums on $(\mathrm{Fin}\ 2)^2$ and the mod-2 5D Spin cobordism pairing $\nu_5 = a_3 \cdot \mathrm{Arf} + w_1 \cdot (\sigma/16) \in \mathbb{Z}_2$ across $T^4$, $K3$, and Postnikov-Arf sectors.
  4. Class-specific representation no-go under an odd anomaly Ward identity $Z = -Z$ for nonnegative weights $w_i \ge 0$, and 5D bulk topological inflow cancellation $\nu_5 + (-\nu_5) = 0$ with $(-1)^{\nu_5}(-1)^{\nu_5} = +1$.
  5. Explicit class-specificity, $\mathrm{Pin}^-$ $\mathbb{Z}_{16}$, and thermal weight asymmetry scope fences (`GIN-C22`).

## 2. What It Does Not Support
- Does not compute smooth continuum Atiyah-Patodi-Singer $\eta$-invariants on 5-manifolds or claim a representation-independent sign no-go outside the declared symmetry-preserving representation class (`GIN-C22`).

## 3. Narrowest Defensible Claim
- Within any representation class whose nonnegative weights $w_i \ge 0$ preserve an odd anomaly Ward identity $Z = -Z$ (induced in the finite prototype by an odd zero-mode crossing, Arf-1 quadratic refinement, or $\nu_5 = 1$ mod-2 cobordism pairing), no positive partition sum $Z > 0$ exists without either coupling to a compensating 5D bulk counterterm $-\nu_5$ or leaving the symmetry-constrained representation class.

## 4. Next Test Needed
- Narrow `PGW-IDENTITY-CONVENTION-UNDECIDABLE` in the frontier derivation queue.
