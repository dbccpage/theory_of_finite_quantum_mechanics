# QM-229, QM-230, QM-231: Finite Rational Maps for Post-Newtonian Gravity (Light Deflection, Mercury Perihelion), Three-Qubit GHZ/Mermin over $\mathbb{Q}(i)$, Page–Wootters Four-Tick History, Pythagorean Phase Damping, and QWZ/Haldane Chern Parity

**AuthorityEffect:** None.

**Goal IDs:** `QM-229-PPN-DEFLECTION-PERIHELION-MAP`, `QM-230-GHZ-MERMIN-PAGE-WOOTTERS-KRAUS-MAP`, `QM-231-QWZ-HALDANE-CHERN-PARITY-MAP`  
**Parent Milestone:** `MS-QUANTUM`  
**Status:** `DONE` (Rust, Python, and core Lean 4 `FiniteQFTAndGravity.lean` verified with exit code 0 and zero `sorryAx`)  
**Executable Rust Module:** `external:sha256:c5ad48d5c22ea89b1e481b44062e0de0f36728afa54ea6439e12e592c239f77a`  
**Executable Python Module:** [`python/finite_qm/use_cases/regge_gravity_ghz_chern_control.py`](../python/finite_qm/use_cases/regge_gravity_ghz_chern_control.py)  
**Lean 4 Mechanization:** [`lean4/FiniteQFTAndGravity.lean`](../../lean4/FiniteQFTAndGravity.lean) and [`lean4/FiniteQFTAndGravity.lean`](../../lean4/FiniteQFTAndGravity.lean) (sections QM-229, QM-230, QM-231)  
**E2E Verification Suite:** [`tests/e2e/test_e2e_regge_gravity_ghz_chern_control.py`](../tests/e2e/test_e2e_regge_gravity_ghz_chern_control.py)

## 1. Executive Summary

Goals 7, 8 and 9 of the Finite Quantum Mechanics roadmap are encoded as closed identities over $\mathbb{Q}$, $\mathbb{Q}(i)$ and $\mathbb{Z}$, with $\pi$ entering only as the Machin rational interval enclosure. The three layers are:

1. **Exact algebraic spine.** The PPN factors $(1 + \gamma)/2$ and $(2 + 2\gamma - \beta)/3$; the Minkowski trace of the constructed flow tensor $e\,k^\mu k^\nu$ (a null probe with $k = (1, 1, 0, 0)$ and dust at rest with $u = (1, 0, 0, 0)$); the exact rational deflection $4GM/(c^2 b)$ and the Mercury advance $6\pi GM/(a(1 - e^2)c^2)$ per orbit; the $8 \times 8$ Gaussian-rational operators $A_1 = X\otimes Y\otimes Y$, $A_2 = Y\otimes X\otimes Y$, $A_3 = Y\otimes Y\otimes X$, $B = X\otimes X\otimes X$ on the GHZ state; the cyclic clock shift $S$ and the rational-Gaussian step unitary $U = \tfrac{1}{25}\begin{pmatrix} 9 + 16i & -12 - 12i \\ 12 + 12i & 16 + 9i\end{pmatrix}$; the Pythagorean Kraus pair $K_0 = \operatorname{diag}(1, p/q)$, $K_1 = \operatorname{diag}(0, r/q)$; and the signed sum $\sum (-1)^{n_x + n_y}\operatorname{sgn}(m + \cos k_x + \cos k_y)$ over the four Dirac points of the QWZ model.
2. **Rational interval enclosures.** Only $\pi$ is needed, for the radian-to-arcsecond conversion of the deflection; the Mercury advance in arcseconds is $\pi$-free because $6\pi$ radians times $648000/\pi$ arcseconds per radian is $6 \cdot 648000 = 3888000$ arcseconds.
3. **Lean 4 core-only theorems** for the scalar, $2 \times 2$ Gaussian-rational and $4 \times 4$ rational pieces, including the Mermin bound over all 64 deterministic assignments by case split. The $8 \times 8$ GHZ eigenvector checks and the history-state constraint are checked in Rust and Python only.

### 1.0 Shared exact types, stored values, typed refusals

The Rust module uses the crate's `Qi` and the dynamic Gaussian-rational matrices of `cyclotomic_rings` (`qi_dyn_*`, now `pub(crate)`); the Python module uses `Qi` and the `qi_*` helpers of `page_wootters_tsirelson_wigner_control` and `RationalInterval` and `pi_interval` of `dressed_qed_g2_control`. Neither carries a private Gaussian-rational type.

Audit records store computed values: the stress tensors, the deflection and perihelion values and their arcsecond enclosures, the $8 \times 8$ operators and the GHZ eigenvalues, the history state and both shift residuals, the channel outputs $\rho_0, \dots, \rho_3$, and the Chern samples. Every check is a property (Python) or method (Rust) that recomputes its verdict from those values.

An eigenvalue is exact or refused. `exact_eigenvalue` takes the Rayleigh quotient $\lambda = \langle v, Av\rangle / \langle v, v\rangle$ and then requires $Av = \lambda v$ entry by entry; a vector that is not an eigenvector, and the zero vector, raise `ReggeGravityGhzChernRefusal` (a typed error in both languages). No sentinel value stands in for a missing eigenvalue. The tests check the refusal on $Z \otimes X \otimes X$ applied to GHZ and on the zero vector. Likewise $b \le 0$, $c \le 0$, $a \le 0$, $e \notin [0, 1)$ and a non-Pythagorean triple are refused.

### 1.1 Encoding choices recorded during the work

* **Page–Wootters uses the cyclic lowering shift.** With $S|t\rangle = |t - 1 \bmod 4\rangle$ (rows $[[0,1,0,0],[0,0,1,0],[0,0,0,1],[1,0,0,0]]$) and $U^4 = I$, the history $|\Psi\rangle = \sum_t |t\rangle \otimes U^t|\psi_0\rangle$ satisfies $(I_C \otimes U - S \otimes I_S)|\Psi\rangle = 0$; the raising shift fails on the same history. The initial state must not be an eigenvector of $U$ for the raising check to be a genuine negative control: $\psi_0 = (1, 0)$ is used, since $(3/5, 4i/5)$ is an eigenvector of $U$.
* **Haldane sign.** $C = \tfrac12[\operatorname{sgn}(M - D) - \operatorname{sgn}(M + D)]$ with $D = 3\sqrt{3}\, t_2 \sin\phi$; for $|M| < |D|$ this is $-\operatorname{sgn}(t_2 \sin\phi)$. The module takes a declared rational $s$ standing for $\sin\phi$ and decides the regime exactly by comparing $M^2$ with $27\,t_2^2 s^2$, so no square root is taken; the gap closing $M^2 = 27\,t_2^2 s^2$ returns no Chern number.
* **QWZ as a parity table.** Twice the Chern number is $\operatorname{sgn}(m + 2) - 2\operatorname{sgn}(m) + \operatorname{sgn}(m - 2)$; it is $2, -2, 0, 0$ at $m = -1, 1, 3, -3$, odd at the gap closings $m = \pm 2$, and even elsewhere, so an integer $C_1(m)$ exists exactly away from the closings (`chern_table`, `chern_gap_closings_odd`, `chern_parity`).

## 2. Claim Hygiene Summary

1. **What it supports:**
   * Checked by `regge_gravity_ghz_chern_finite_maps.rs` (`external:sha256:c5ad48d5c22ea89b1e481b44062e0de0f36728afa54ea6439e12e592c239f77a`) (6 inline tests), [`regge_gravity_ghz_chern_control.py`](../python/finite_qm/use_cases/regge_gravity_ghz_chern_control.py) (13 e2e tests) and the Lean theorems `deflection_factor_values` through `chern_parity` in [`FiniteQFTAndGravity.lean`](../../lean4/FiniteQFTAndGravity.lean): the PPN factors at $(\gamma, \beta) = (1, 1)$ and $\gamma = 0$; $\delta\varphi_{\mathrm{GR}} = 2\,\delta\varphi_{\mathrm{Newton}}$; the Minkowski trace $e\,\eta(k, k)$ of the flow tensor $e\,k k$ for every $e$ and $k$, which vanishes for the null probe and is $\rho$ for dust; the Pauli single-site identities $XYY = X$, $YXY = -X$, $YYX = X$ behind $A_1A_2A_3 = -B$; the Mermin bound $|x_1x_2x_3 - x_1y_2y_3 - y_1x_2y_3 - y_1y_2x_3| \le 2$ over all 64 assignments; $U = W\operatorname{diag}(1, i)W^\dagger$ with $W = \tfrac15\begin{pmatrix}3 & 4i \\ 4i & 3\end{pmatrix}$, $UU^\dagger = I$ and $U^4 = I$; $S^4 = I$; Kraus completeness, three applications of the $(3, 4, 5)$ channel to $\rho_+$ ending at off-diagonal entry $27/250$, and the coherence $(3/5)^3$ read off that output; the QWZ parity table.
   * Checked in Rust and Python only: the solar-limb deflection $1.751190''$ inside $[1.750, 1.752]''$ and the Newtonian half $0.875595''$ inside $[0.875, 0.876]''$; Mercury $42.980654''$ per century inside $[42.97, 42.99]''$; the $8 \times 8$ operators commute, are Hermitian and involutive, $A_1A_2A_3 = -B$ on $\mathbb{Q}(i)^8$, GHZ is an eigenvector of each with exact eigenvalues $(-1, -1, -1, +1)$, and of $M = B - A_1 - A_2 - A_3$ with eigenvalue $4$; the four-tick history constraint; the Haldane sign decisions.
2. **What it does not support:**
   * The deflection and perihelion numbers are evaluated at the declared rational inputs ($GM_\odot$, $c$, $R_\odot$, Mercury's $a$ and $e$, orbits per century) and are not fits to data; the PPN factors are the standard parameterized forms, not derivations from a field equation. The Regge-calculus discretization named in the goal title is not implemented here; only the PPN endpoint checks are.
   * `FiniteQFTAndGravity.lean` elaborates cleanly with core Lean 4 (`lean lean4/FiniteQFTAndGravity.lean`, no imports, zero warnings, zero `sorryAx`). A full `lake build` of the `quantum_mechanics` package requires Mathlib in an environment with network or cached Mathlib artifacts.
3. **The narrowest defensible claim:**
   * Within the implemented code and at the listed inputs, the stated rational, Gaussian-rational and integer identities hold, the stated enclosures contain the stated values, and the stated windows contain the enclosures. The Mermin bound is a finite case analysis over 64 sign assignments, not a theorem about hidden-variable theories in general.
4. **The next test needed:**
   * Extend the Lean 4 mechanization to cover the $8 \times 8$ GHZ eigenvector relations and four-tick Page–Wootters history constraint, or run `lake build` in an environment with cached Mathlib artifacts.

## 3. QM-229: Deflection and Perihelion

The stress tensors are built, not typed in: a null probe is $E\,k^\mu k^\nu$ with $k = (1, 1, 0, 0)$, so $T^{00} = T^{11} = E$, and dust at rest is $\rho\,u^\mu u^\nu$ with $u = (1, 0, 0, 0)$. The Minkowski trace of $e\,k k$ is $e\,\eta(k, k)$ for every $e$ and $k$ (`flow_tensor_trace`), so the null probe is traceless for every $E$ and dust has trace $\rho$ (`null_probe_traceless`, `dust_trace`). The executable audits use energy $7/3$ and density $5/2$. The deflection factor $(1 + \gamma)/2$ is $1$ at $\gamma = 1$ and $1/2$ at $\gamma = 0$, so $\delta\varphi_{\mathrm{GR}} = 4GM/(c^2 b) = 2\,\delta\varphi_{\mathrm{Newton}}$ (`deflection_factor_values`, `gr_deflection_twice_newton`). At the solar limb the exact rational radian values are converted to arcseconds through the $\pi$ enclosure, giving $1.751190''$ and $0.875595''$. The perihelion factor $(2 + 2\gamma - \beta)/3$ is $1$ at $(1, 1)$ (`perihelion_factor_gr`; the Brans–Dicke $\omega = 40$ value $62/63$ is recorded beside it). Mercury's advance per orbit is $6 \cdot 648000\,GM/(a(1 - e^2)c^2) = 3888000\,GM/(a(1 - e^2)c^2)$ arcseconds, an exact rational (`mercury_per_orbit_arcsec`), and $42.980654''$ per century at the declared inputs.

## 4. QM-230: GHZ/Mermin, Page–Wootters, Phase Damping

### 4.1 GHZ and Mermin

Over $\mathbb{Q}(i)$ with $X = \begin{pmatrix}0&1\\1&0\end{pmatrix}$, $Y = \begin{pmatrix}0&-i\\i&0\end{pmatrix}$, the three-fold Kronecker products $A_1, A_2, A_3, B$ are Hermitian, involutive and pairwise commuting, and $A_1A_2A_3 = -B$, which follows site by site from $XYY = X$, $YXY = -X$, $YYX = X$ (`pauli_ghz_sites`). On the unnormalized GHZ vector $(1, 0, 0, 0, 0, 0, 0, 1)$ each operator acts as a scalar: $A_k v = -v$ and $B v = v$, checked entry by entry by `exact_eigenvalue`. The Mermin operator $M = B - A_1 - A_2 - A_3$ then has GHZ as an eigenvector with eigenvalue $1 + 3 = 4$, also checked as $Mv = 4v$. The audit stores the 64 deterministic values and recomputes their largest absolute value, $2$. The Lean theorem `mermin_deterministic_bound` shows by exhaustive case split that every assignment of $\pm 1$ to $x_1, x_2, x_3, y_1, y_2, y_3$ gives a value in $[-2, 2]$, and `mermin_bound_attained` exhibits both endpoints. The comparison $4 > 2$ is made on the stored values in Rust and Python; the former Lean line $2 < 4$ on bare numerals was removed.

### 4.2 Page–Wootters four-tick history

$U = W\operatorname{diag}(1, i)W^\dagger$ with $W = \tfrac15\begin{pmatrix}3 & 4i\\ 4i & 3\end{pmatrix}$ is a non-diagonal unitary over $\mathbb{Q}(i)$ with $U^4 = I$ (`pw_frame_unitary`, `step_unitary_factorization`, `step_unitary_unitary`, `step_unitary_order_four`). With the lowering shift $S$ ($S^4 = I$, `clock_shift_order_four`) the history $|\Psi\rangle = \sum_{t=0}^{3}|t\rangle\otimes U^t|\psi_0\rangle$ is annihilated by $I_C\otimes U - S\otimes I_S$, the raising constraint fails on it, the conditional states are the powers $U^t|\psi_0\rangle$, and $\|\Psi\|^2 = 4\|\psi_0\|^2$ (Rust and Python).

### 4.3 Pythagorean phase damping

For a triple $p^2 + r^2 = q^2$ set $1 - \lambda = p^2/q^2$ and $\lambda = r^2/q^2$; then $K_0 = \operatorname{diag}(1, p/q)$ and $K_1 = \operatorname{diag}(0, r/q)$ satisfy $K_0^\dagger K_0 + K_1^\dagger K_1 = I$ (`phase_damping_trace_preserving`, `kraus_completeness`), the channel keeps the populations and multiplies the coherence by $p/q$ per step (`phase_damping_channel_step`). For $(3, 4, 5)$ the Lean file applies the channel three times to $\rho_+$, one step per theorem (`phase_damping_step_one`, `phase_damping_step_two`, `phase_damping_step_three`), composes them (`phase_damping_three_applications`), and reads the coherence $2\operatorname{Re}\rho_{01} = (3/5)^3 = 27/125$ off the output (`phase_damping_coherence_three_steps`). The executable audits store $\rho_0, \dots, \rho_3$ for each of the triples $(3,4,5)$, $(5,12,13)$, $(8,15,17)$ and check that each state is the channel applied to the previous one.

## 5. QM-231: QWZ and Haldane Chern Parity

With $d_z(k) = m + \cos k_x + \cos k_y$ at the four Dirac points $k \in \{0, \pi\}^2$ the signed sum $2C_1(m) = \operatorname{sgn}(m + 2) - 2\operatorname{sgn}(m) + \operatorname{sgn}(m - 2)$ gives $C_1(-1) = +1$, $C_1(+1) = -1$, $C_1(\pm 3) = 0$, with jumps $1, 2, 1$ across the closings $m = -2, 0, 2$ matching the number of Dirac points closing at each. The Lean theorems `chern_table`, `chern_gap_closings_odd` and `chern_parity` state the table, the odd values at $m = \pm 2$ and the evenness elsewhere. The Haldane audit returns $0$ for $|M| > |D|$ and $\mp 1$ for $\sin\phi = \pm 1/2$ inside the gap, with an exact rational grid check that the gap never closes at rational sample points away from the degenerate line and that it does close at $M = D = 0$.

## 6. Reproduction

From the repository root:

```text
cd sources/atlas/papers/finite_quantum_mechanics
python3 -m pytest tests/e2e/test_e2e_regge_gravity_ghz_chern_control.py -q
cd external:git-tree:ac1f6d647c3ecc2bf45f6fc4922213ac752e71a3
cargo test -j 1 -p quantum_physics --lib -- regge_gravity
cd ../../lean4/quantum_mechanics
lean FiniteQFTAndGravity.lean
```

The Lean file has no imports, so `lean FiniteQFTAndGravity.lean` from `lean4/quantum_mechanics` elaborates it with the core toolchain pinned by `lean4/lean-toolchain`; `lake build` of the whole package also needs Mathlib.
