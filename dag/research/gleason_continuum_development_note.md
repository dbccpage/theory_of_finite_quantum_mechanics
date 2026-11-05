# Phase 4 Research Note: Full Continuum Gleason Development across Dimensions

## 1. Scope and Architecture

This note records the Phase 4 mathematical formalization in `lean4/GleasonContinuumDevelopment.lean` and its exact-arithmetic verification suite (`scripts/verify_gleason_continuum_development.py`, `scripts/test_gleason_continuum_development.py`, `dag/research/gleason_continuum_development_receipt.json`).

Building directly on the Phase 2 finite and exact-arithmetic Gleason model (`lean4/BornGaussianFiniteModel.lean`) and the Phase 3 continuum shadow and bridge (`lean4/GleasonContinuumShadow.lean`), Phase 4 organizes the continuum Gleason development across four parts:

1. **Part A ($d = 3$ Complex States, Gram-Factorized Density Operators, and Rayleigh Stability)**:
   - Formalizes $3 \times 3$ Gaussian-rational matrices `GaussMatrix3`, the Gram Hermitian form `gramHermForm3 B` representing $B B^*$, the squared Frobenius norm `frobNormSq B` representing $\operatorname{tr}(B B^*)$, and the normalized factorized state `factorizedState3 B` representing $\rho(B) = B B^* / \operatorname{tr}(B B^*)$.
   - Establishes the exact Gram identity `quadNum_gramHermForm3`: for every vector $v \in \mathbb{Q}(i)^3$, the quadratic numerator of `gramHermForm3 B` equals the squared norm $\|B^* v\|^2 \ge 0$ (`normSqVec (mulConjTransposeVec B v)`).
   - Connects `factorizedState3 B` directly to the complex density-matrix interface `IsComplex3DensityMatrix (toMatrix (factorizedState3 B))` via `toMatrix_factorizedState3_posSemidef_and_trace_one`.
   - Defines the continuum Rayleigh quotient `complexRayleigh A v` on $\mathbb{C}^3 \setminus \{0\}$ and the matrix entry $\ell_1$ norm `matEntryL1Norm A`, establishing the uniform Rayleigh stability bound `abs_complexRayleigh_sub_le`:
     $$|\operatorname{complexRayleigh}(A, v) - \operatorname{complexRayleigh}(B, v)| \le \|A - B\|_1$$
     for all nonzero $v \in \mathbb{C}^3$, together with the factorized Born-probability approximation theorem `factorizedState3_born_prob_error_le` and complex Hermitian uniqueness `complex_hermitian_unique_of_rayleigh_eq`.

2. **Part B (All Finite Dimensions $d = 0, 1, 2$ and $d \ge 3$)**:
   - **Dimension $d = 0$**: `dim0_no_nonzero_vectors` and `dim0_frameValuation_vacuously_unique` show that `Fin 0 → ℂ` admits no nonzero vectors and any two ray valuations agree vacuously.
   - **Dimension $d = 1$**: `dim1_frameValuation_eq_one` shows that any 1D frame valuation (`IsDim1FrameValuation`) equals $1$ on every nonzero vector and coincides with the trace-$1$ Born rule in $d = 1$.
   - **Dimension $d = 2$**: Formalizes `GVec2`, `IsFrame2`, `IsFrameFunction2`, `IsNonnegFrameFunction2`, and `HermForm2` over $\mathbb{Q}(i)^2$, and constructs the explicit $\{0, 1/2, 1\}$-valued non-quadratic frame function `dim2AxisCounterexample`:
     $$f(x, y) = \begin{cases} 1 & \text{if } y = 0, \\ 0 & \text{if } x = 0, \\ 1/2 & \text{if } x \ne 0 \text{ and } y \ne 0. \end{cases}$$
     `dim2AxisCounterexample_isNonnegFrameFunction2` shows that $f$ is a nonnegative 2D frame function on $\mathbb{Q}(i)^2$, while `dim2_projection_measure_obstruction` shows that no $2 \times 2$ Hermitian form `ρ : HermForm2` represents $f$ on $\mathbb{Q}(i)^2 \setminus \{0\}$ (matching the 6 standard axes and phase vectors forces $\rho = \operatorname{diag}(1, 0)$, which evaluates to $4/5 \ne 1/2$ at $u = (2, 1)$).
   - **Dimensions $d \ge 3$**: Formalizes 3D coordinate subspace embeddings `embed3D`, 3D restricted submatrices `submatrix3D M emb`, Hermiticity preservation `submatrix3D_isHermitian`, subspace weight preservation `submatrix3D_trace_eq_subspace_weight`, compatibility on shared 1D/2D coordinate intersections `compat_submatrix3D_overlap`, and global $d \times d$ Hermitian uniqueness `eq_of_complexQuadFormD_eq` across all finite dimensions $d$.

3. **Part C (Continuum Automatic Regularity in $d \ge 3$)**:
   - Formalizes `IsContinuumFrame3`, `IsContinuumFrameFunction3`, and `IsNonnegContinuumFrameFunction3` on $\mathbb{C}^3$.
   - Establishes `exists_continuumFrame3_completion` (every orthogonal pair of unit vectors in $\mathbb{C}^3$ completes to an orthonormal 3-frame via the normalized cross product), `nonneg_continuum_frameFunction_bounds` ($0 \le f(u) \le 1$ on unit vectors), `continuum_piron_subadditivity` (Piron's planar subadditivity $f(u) + f(v) \le 1$ for orthogonal unit vectors $u \perp v$), and `continuum_eq_zero_on_perp_of_pole_one` ($f(p) = 1 \implies f(u) = 0$ for all unit vectors $u \perp p$).
   - Documents the relationship between these continuum frame-completion regularity lemmas and `gleason_complex_three_dim_continuous` in `lean4/GleasonComplexSphere.lean`.

4. **Part D (Infinite-Dimensional Separable Hilbert Spaces and Trace Escape)**:
   - Formalizes finite-dimensional Hilbert-basis compressions `compressionTrace w N = ∑ n ∈ Finset.range N, w n`, monotonicity `compressionTrace_mono`, tightness modulus `IsTightState w B`, and the uniform tail-weight bound `tail_weight_le_of_tight`:
     $$\sum_{k < M} w(N + k) \le \varepsilon \quad \text{for all } N \ge B(\varepsilon).$$
   - Constructs the explicit moving-bump sequence `basisEscapeState k` ($w_k(n) = \delta_{n, k}$), establishing `basisEscapeState_normalized_at_stage` ($\sum_{n < N} w_k(n) = 1$ for $N > k$), `basisEscapeState_compression_eq_zero_of_ge` ($\sum_{n < N} w_k(n) = 0$ for $k \ge N$), and `basisEscapeState_escapes_to_zero_without_tightness`: without a uniform tightness modulus ($\sigma$-additivity / normal-state condition), a sequence of normalized states can converge pointwise to $0$ on every fixed finite-dimensional subspace while carrying total weight $1$.

---

## 2. Claim Hygiene Summary

1. **What it supports**:
   - Supports in Lean 4 (using only the standard axioms `propext`, `Classical.choice`, `Quot.sound`) that Gram-factorized Gaussian-rational states `factorizedState3 B` map into the complex density-matrix cone with exact trace $1$ and uniform Rayleigh quotient stability $|\operatorname{complexRayleigh}(A, v) - \operatorname{complexRayleigh}(B, v)| \le \|A - B\|_1$.
   - Supports the dimension dichotomy across $d = 0, 1, 2$ and $d \ge 3$: vacuous/trivial uniqueness in $d = 0, 1$, an explicit non-quadratic nonnegative 2D frame function obstruction `dim2AxisCounterexample` in $d = 2$, and 3D coordinate subspace compatibility plus global $d \times d$ Hermitian polarization uniqueness in $d \ge 3$.
   - Supports the continuum frame-completion regularity lemmas in $d = 3$ (`exists_continuumFrame3_completion`, `nonneg_continuum_frameFunction_bounds`, `continuum_piron_subadditivity`, `continuum_eq_zero_on_perp_of_pole_one`) and the infinite-dimensional tightness versus moving-bump trace-escape theorem (`tail_weight_le_of_tight`, `basisEscapeState_escapes_to_zero_without_tightness`).
2. **What it does not support**:
   - Does not claim that finitely additive frame functions on an infinite-dimensional Hilbert space are represented by trace-class density operators without $\sigma$-additivity or uniform tightness (`basisEscapeState_escapes_to_zero_without_tightness` exhibits the moving-bump obstruction).
   - Does not claim that 2D projection-valued frame functions must be quadratic (`dim2_projection_measure_obstruction` refutes this in $d = 2$ without effect-level additivity).
3. **The narrowest defensible claim**:
   - Every theorem in `lean4/GleasonContinuumDevelopment.lean` is kernel-checked with standard axioms (`propext`, `Classical.choice`, `Quot.sound`), and all finite-arithmetic witnesses in `dag/research/gleason_continuum_development_receipt.json` are independently verified by `scripts/verify_gleason_continuum_development.py`.
4. **The next test needed**:
   - Proceed to Phase 5 to connect the finite/shadow/continuum Gleason chain to the 8-stage inherited continuum derivation spine across scalar fields, inner products, state/effect cones, tensor products, Wigner/Stone dynamics, CPTP/Stinespring measurement updates, directed continuum limits, and field-theoretic/geometric endpoints.
