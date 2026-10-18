# Complex Hadamard Dimension 6 Catalog Crosswalk

**Packet**: Prompt 01 (Target & Premise Audit)  
**Deliverable**: `catalog_crosswalk.md`  
**Auditor**: `worker_prompt01`  
**Date**: 2026-09-22  
**AuthorityEffect**: None  
**Firewall Line**: `stated region only; mints no authority`  

---

## 1. Executive Summary

This crosswalk provides an item-by-item comparative analysis across four representations of $6 \times 6$ complex Hadamard matrices:
1. The user's/local definitions in `lean4/gluing/G1_Orbits.lean` ($F_6, D_6(\alpha), S_6, B_6(\theta)$).
2. The local unions in `G1_Orbits.lean` (`InKnownHadamardModuli`) and `TargetA11OrbitExhaustiveness.lean` (`InUnifiedCatalog`).
3. The classical primary literature:
   - Beauchamp–Nicoară (math/0609076) — self-adjoint subclass only.
   - Szöllősi (arXiv:0811.0854, arXiv:1008.0632) — four-parameter family $X_6$, defect 4.
   - Karlsson (arXiv:1003.4177) — two- and three-parameter families $K_6(x, y)$.
   - Tadej–Życzkowski (math/0512554) — comprehensive benchmark catalogue.
4. The contemporary computer-assisted classification:
   - Cárdenes Wuttig–Tindall (arXiv:2608.18053v2, August 2026) — finite-corner box cover.

**Key Rule**: Similar letters do not establish the same family. Parameter domains, equivalence groups, and mathematical definitions must be verified explicitly.

---

## 2. Catalog Crosswalk Matrix

| Row ID | Object Identifier | Source / Formal Reference | Parameter Domain | Type (Fixed vs Family) | Equivalence Convention | Established Inclusions / Relations | Missing / Unknown Mappings |
|---|---|---|---|---|---|---|---|
| **CAT-01** | **$F_6$ (Local Fourier)** | `G1_Orbits.lean:111-130` (`F6_concrete`, `F6_matrix`) | Discrete / None | Fixed matrix ($6 \times 6$) | Affine gauge in $\mathbb{N}$ (`PhaseGauge6`, `Permutation6`) | $[F_6]_{jk} = \omega_6^{jk}$. Proved dephased. Connects to $D_6(0)$ under hypothesis `D6_zero_is_fourier`. | `F6_concrete` is disconnected from `F6_matrix` (opaque). No link to Mathlib $\mathbb{C}$. |
| **CAT-02** | **$D_6(\alpha)$ (Local Diță)** | `G1_Orbits.lean:142-154` (`D6_family`) | `PhaseAngle` (in $\mathbb{N}$) | 1-parameter family | Affine gauge in $\mathbb{N}$ | Composite factorization $6 = 2 \times 3$. Subsumes $F_6$ at $\alpha = 0$. Included in `InKnownHadamardModuli`. | Parameter is typed as `Nat`, not $[0, \pi)$. Body is `opaque`. Modulo arithmetic missing. |
| **CAT-03** | **$S_6$ (Local Tao)** | `G1_Orbits.lean:165-206` (`Tao_S6_concrete`, `Tao_S6_matrix`) | Discrete / None | Fixed isolated matrix | Affine gauge in $\mathbb{N}$ | Entries in cubic phases $\{1, \omega_3, \omega_3^2\}$. Proved dephased. Included in `InKnownHadamardModuli`. | `Tao_S6_concrete` disconnected from `Tao_S6_matrix` (opaque). Exponent arithmetic unreduced. |
| **CAT-04** | **$B_6(\theta)$ (Local Szöllősi)** | `G1_Orbits.lean:207-220` (`Szollosi_B6_family`) | `PhaseAngle` (in $\mathbb{N}$) | 1-parameter family | Affine gauge in $\mathbb{N}$ | Self-adjoint non-affine family. Included in `InKnownHadamardModuli`. Intended to contain $H_6$ at $\theta = \pi/2$. | Parameter is typed as `Nat`, not $[0, \pi]$. Body is `opaque`. Connection to `SzollosiDeltoid.lean` is unproved. |
| **CAT-05** | **$H_6$ (Local Haagerup)** | `TargetA9Haagerup.lean:457`, `TargetA11.lean:87` (`haagerup_mat`) | Discrete / None | Fixed isolated matrix | Affine gauge in $\mathbb{N}$ | 2-circulant form over 4th roots $\{1, i, -1, -i\}$. Proved not equivalent to $F_6$ and $S_6$ via $\mathbb{N}$-inequalities. | `HaagerupInSzollosiFamily` is an unproved hypothesis parameter. |
| **CAT-06** | **`InKnownHadamardModuli`** | `G1_Orbits.lean:227` | Union of above | 4-term orbit disjunction ($F_6 \cup D_6 \cup S_6 \cup B_6$) | Affine gauge in $\mathbb{N}$ | Standard local target predicate for orbit coverage. | Omits $H_6$ unless basepoint hypothesis assumed. Omits Karlsson $K_6$ and Szöllősi $X_6$. |
| **CAT-07** | **`InUnifiedCatalog`** | `TargetA11.lean:114` | Union of above | 5-term orbit disjunction ($F_6 \cup D_6 \cup S_6 \cup B_6 \cup H_6$) | Affine gauge in $\mathbb{N}$ | Equivalent to `InKnownHadamardModuli` under `HaagerupInSzollosiFamily` and transitivity. | Omits Karlsson $K_6$ and Szöllősi $X_6$. Unlinked to continuous complex topology. |
| **CAT-08** | **Beauchamp–Nicoară (2006/2008)** | arXiv:math/0609076 | $\theta \in [0, \pi]$ | 1-parameter self-adjoint family + basepoints | Unitary Hadamard equivalence ($H \sim U H V$) | Classifies **strictly self-adjoint** CHMs ($H = H^\dagger$): $\{F_6\} \cup B_6(\theta) \cup \{H_6\}$. | **Does not classify all 6x6 CHMs**. Generic $D_6(\alpha)$ and $S_6$ are not self-adjoint. Scope mismatch. |
| **CAT-09** | **Szöllősi 4-Param ($X_6$)** | arXiv:1008.0632, arXiv:0811.0854 | $(a, b, c, d) \in [0, 2\pi)^4$ | 4-parameter continuous family | Affine gauge ($D_1 P_1 H P_2 D_2$) | Defect 4 family constructed via non-affine perturbations. Contains $F_6, D_6$ as subfamilies. | **Completely absent** from `InKnownHadamardModuli` and `InUnifiedCatalog`. |
| **CAT-10** | **Karlsson ($K_6$)** | arXiv:1003.4177 (2010), LAA 434 (2011) | 2D / 3D phase angles $(x, y) \in \mathbb{T}^2$ | 2- and 3-parameter continuous families | Affine gauge ($D_1 P_1 H P_2 D_2$) | Contains $F_6, D_6, B_6$ as boundary/sub-cases. | **Completely absent** from `InKnownHadamardModuli` and `InUnifiedCatalog`. |
| **CAT-11** | **Tadej–Życzkowski (2006)** | math/0512554 / OSID 13 (2006) | Defect 0 to 4 strata | Benchmark catalogue: $F_6, D_6, C_6, B_6, S_6, H_6, X_6, K_6$ | Extended affine gauge (+ transpose, conj) | Canonical reference taxonomy for 6x6 complex Hadamard matrices. | Confirms no complete classification existed in 2006–2010; catalog was known to be open. |
| **CAT-12** | **Cárdenes Wuttig–Tindall (2026)** | arXiv:2608.18053v2 (Aug 2026) | Finite subdivision of $\mathbb{T}^{25}$ | Finite box/corner certificate collection | Dephased representative box certificates | Proves computer-assisted finite-corner cover of order-6 CHMs. | Upstream trust boundary excludes bijective identification with literature names ($F_6, D_6, S_6, B_6$). |

---

## 3. Detailed Crosswalk Analysis

### 3.1 The Beauchamp–Nicoară Scope Error
In `TargetA11OrbitExhaustiveness.lean:15-18`, the classification premise is described as:
> `ClassificationExhaustivenessPremise`: Every 6x6 complex Hadamard matrix is Hadamard-equivalent to an element of the unified moduli atlas $\mathcal{M}_6$ (Fourier $F_6$, Diță $D_6(\alpha)$, Chernyavsky-Tao $S_6$, or Szöllősi $B_6(\theta)$). Cites Beauchamp–Nicoară 2006/2008 and Szöllősi 2010.

**Audit Finding**:
- The paper by Beauchamp and Nicoară (*Self-adjoint complex Hadamard matrices of order 6*, math/0609076) explicitly and exclusively classifies the **self-adjoint subclass** ($H = H^\dagger$).
- A generic complex Hadamard matrix is **not** self-adjoint. In particular, the Diță family $D_6(\alpha)$ is not self-adjoint for generic $\alpha$, and Tao's matrix $S_6$ is not self-adjoint.
- Citing Beauchamp–Nicoară as the foundation for the classification of *all* $6 \times 6$ complex Hadamard matrices is a mathematical scope error.

### 3.2 The Missing Higher-Dimensional Families ($X_6$ and $K_6$)
- In 2010, Ferenc Szöllősi constructed an explicit **four-parameter family** $X_6(a, b, c, d)$ (arXiv:1008.0632).
- In 2010, B. R. Karlsson constructed explicit **two-parameter and three-parameter families** $K_6(x, y)$ (arXiv:1003.4177).
- However, the predicate `InKnownHadamardModuli` in `G1_Orbits.lean` contains only:
  - 0-parameter: $F_6$, $S_6$
  - 1-parameter: $D_6(\alpha)$, $B_6(\theta)$
- **Omission**: If the true classification requires higher-dimensional defect strata (such as $X_6$ or $K_6$), the predicate `InKnownHadamardModuli` is **under-specified**. Any theorem attempting to prove `∀ H, is_complex_hadamard H → InKnownHadamardModuli H` would fail if $H$ were instantiated with a generic member of $X_6$ or $K_6$ that is not equivalent to a member of $F_6, D_6, S_6, B_6$.

### 3.3 The Cárdenes Wuttig–Tindall Trust Boundary
The recent work by Cárdenes Wuttig and Tindall (arXiv:2608.18053v2, August 2026) provides an interval-arithmetic finite-corner classification. However, inspecting their formal trust boundary (`LEAN_ASSUMES_AND_PROVES.md`) demonstrates:
1. **Verified Upstream**: The Lean formalization verifies that every $6 \times 6$ complex Hadamard matrix falls into a certified finite collection of semi-algebraic boxes (`paper_finite_corner_theorem`).
2. **Excluded from Formal Boundary**: Upstream explicitly excludes the bijective mapping between these certified boxes and the named continuous literature families ($F_6, D_6(\alpha), S_6, B_6(\theta)$).
3. **Implication for MUB(6)**: Importing the Cárdenes Wuttig–Tindall theorem directly will **not** discharge `InKnownHadamardModuli` as defined in `G1_Orbits.lean`. It would instead supply a finite collection of certified boxes $\bigcup_{i=1}^N \mathcal{B}_i$, requiring an explicit bridge from each box to the MUB(6) extension obstruction.

---

## 4. Crosswalk Summary Table: Catalog Concordance

| Moduli Component | In User Local `InKnownHadamardModuli` | In Local `InUnifiedCatalog` | In Beauchamp–Nicoară | In Szöllősi (2010) | In Karlsson (2010) | In Cárdenes Wuttig–Tindall (2026) |
|---|---|---|---|---|---|---|
| $F_6$ (Fourier) | Yes | Yes | Yes (Self-adj) | Yes | Yes | Certified in box |
| $D_6(\alpha)$ (Diță 1D) | Yes (as `Nat`) | Yes (as `Nat`) | No (Not self-adj) | Yes | Yes | Certified in boxes |
| $S_6$ (Tao isolated) | Yes | Yes | No (Not self-adj) | Yes | Yes | Certified in box |
| $B_6(\theta)$ (Szöllősi 1D) | Yes (as `Nat`) | Yes (as `Nat`) | Yes (Self-adj) | Yes | Yes | Certified in boxes |
| $H_6$ (Haagerup isolated) | Conditional (`theta_0`) | Yes | Yes (at $\pi/2$) | Yes | Yes | Certified in box |
| $X_6(a, b, c, d)$ (Szöllősi 4D) | **NO** | **NO** | **NO** | Yes (Defect 4) | Yes | Certified in boxes |
| $K_6(x, y)$ (Karlsson 2D/3D) | **NO** | **NO** | **NO** | Yes | Yes | Certified in boxes |
| Finite-corner box cover | **NO** | **NO** | **NO** | **NO** | **NO** | **Primary target** |

---
**Crosswalk Recommendation**: The catalog predicate must be semantically redefined to align with an audited mathematical atlas (either the full continuous strata $\{F_6, D_6, S_6, B_6, H_6, K_6, X_6\}$ or the upstream finite-corner box cover).
