# QM-226, QM-227, QM-228: Finite Rational Maps for Tree-Level QED (Klein–Nishina, Bhabha/Møller), Weak Chirality (Chiral Projectors, Muon Decay, $G_F$, CKM over $\mathbb{Q}(i)$), and Hadronic Identities (ABJ Colour Factor, Gell-Mann–Okubo)

**AuthorityEffect:** None.

**Goal IDs:** `QM-226-KLEIN-NISHINA-BHABHA-MOLLER-MAP`, `QM-227-CHIRAL-MUON-FERMI-CKM-MAP`, `QM-228-ABJ-GMO-HADRONIC-MAP`  
**Parent Milestone:** `MS-QUANTUM`  
**Status:** `DONE` (Rust, Python, and core Lean 4 `FiniteQFTAndGravity.lean` verified with exit code 0 and zero `sorryAx`)  
**Executable Rust Module:** [`external:sha256:b2756728a2444a8202ad7ab9078b63b94e2b41bb2addc311e7a2b1bebd8d9f44`](../../../../../omega_engine/crates_rs/omega_quantum_physics/src/qed_weak_hadronic_finite_maps.rs)  
**Executable Python Module:** [`python/finite_qm/use_cases/qed_weak_hadronic_control.py`](../python/finite_qm/use_cases/qed_weak_hadronic_control.py)  
**Lean 4 Mechanization:** [`lean4/FiniteQFTAndGravity.lean`](../../lean4/FiniteQFTAndGravity.lean) and [`lean4/FiniteQFTAndGravity.lean`](../../lean4/FiniteQFTAndGravity.lean) (sections QM-226, QM-227, QM-228)  
**E2E Verification Suite:** [`tests/e2e/test_e2e_qed_weak_hadronic_control.py`](../tests/e2e/test_e2e_qed_weak_hadronic_control.py)

## 1. Executive Summary

Goals 4, 5 and 6 of the Finite Quantum Mechanics roadmap are encoded as closed identities over $\mathbb{Q}$ and $\mathbb{Q}(i)$, with every transcendental constant ($\pi$, $\ln$, square roots) entering only as a rational interval enclosure whose endpoints are exact rationals. The three layers are:

1. **Exact algebraic spine.** The Klein–Nishina ratio $R(x, u) = \tfrac{1}{2}\eta^2\,(\eta + 1/\eta - (1 - u^2))$ with $\eta = 1/(1 + x(1 - u))$; the tree-level Bhabha and Møller reduced amplitudes and their crossing; the Weyl-basis Dirac matrices over $\mathbb{Q}(i)$ with $\gamma^5 = \operatorname{diag}(-1, -1, 1, 1)$ and the projectors $P_{L,R} = (I \mp \gamma^5)/2$; the muon phase-space polynomial $f_0(x) = 1 - 8x + 8x^3 - x^4$; a $3 \times 3$ CKM matrix over $\mathbb{Q}(i)$ built by the Cayley transform $V = (I - A)(I + A)^{-1}$ of a skew-Hermitian generator; the Adler–Bell–Jackiw colour factor $S(N_c) = N_c (Q_u^2 - Q_d^2)$; and the Gell-Mann–Okubo mass operator $M = M_0 + M_1 Y + M_2\,(I(I+1) - Y^2/4)$.
2. **Rational interval enclosures.** $\pi$ by the Machin series, $\ln x$ by the atanh series, square roots by integer square roots. These feed the muon-decay radiative term $-12 x^2 \ln x$, the one-loop bracket $\tfrac{\alpha}{2\pi}(\tfrac{25}{4} - \pi^2)$, the Fermi constant, the $\pi^0 \to \gamma\gamma$ rate and the GMO residuals.
3. **Lean 4 core-only theorems** for the scalar and $4 \times 4$ rational pieces (no Mathlib, no imports). The CKM Cayley transform, the $G_F$ enclosure and the interval helpers are checked in Rust and Python only.

### 1.0 One Gaussian-rational stack

Both executable modules reuse the existing exact types instead of carrying their own copies. In Rust the module uses the crate's `Qi`, `Mat4Qi`, `Vec4Qi` and `mat4_qi_*` helpers from `quantum_import_finite_maps` (with the added `mat4_qi_mul_vec`), the crate's Dirac-basis `dirac_gamma_matrices()`, and the BigRational `Mat3Qi` and `BigQi` of `qcd_beta0_wilson_confinement_control` for the CKM transform; the only new matrix operation is the $3 \times 3$ adjugate inverse. In Python the module uses `Qi` and the `qi_*` matrix helpers of `page_wootters_tsirelson_wigner_control`, the Dirac-basis gammas of `dirac_ward_takahashi_control`, and `RationalInterval` and `pi_interval` of `dressed_qed_g2_control`.

Audit records store computed values (matrices, enclosures, amplitudes). Every check is a property that recomputes its verdict from those values, so a test reads a value and recomputes, rather than reading a stored flag.

### 1.1 Formula corrections recorded during encoding

* **Bhabha/Møller crossing is $s \leftrightarrow u$, not $s \leftrightarrow t$.** With $M_{\mathrm{Bhabha}}(s,t,u) = 2\big((s^2+u^2)/t^2 + 2u^2/(st) + (t^2+u^2)/s^2\big)$ and $M_{\mathrm{M\o ller}}(s,t,u) = 2\big((s^2+u^2)/t^2 + 2s^2/(tu) + (s^2+t^2)/u^2\big)$, the identity $M_{\mathrm{M\o ller}}(s,t,u) = M_{\mathrm{Bhabha}}(u,t,s)$ holds for all nonzero $s, t, u$. The $s \leftrightarrow t$ exchange fails at the witness $(s,t,u) = (5,-2,-3)$: $M_{\mathrm{Bhabha}}(5,-2,-3) = 361/25$ while $M_{\mathrm{M\o ller}}(-2,5,-3) = 1444/225$. Both the identity and the witness are Lean theorems (`moller_eq_bhabha_su`, `crossing_st_witness`).
* **The $\pi^0$ window is read as an experimental band.** The computed $N_c = 3$ enclosure of $\Gamma = \alpha^2 m_\pi^3 S^2/(64\pi^3 f_\pi^2)$ is $[7.690, 7.882]$ eV, which contains the central value $7.72$ eV and overlaps the band $[7.60, 7.85]$ eV; the $N_c = 1$ enclosure $[0.854, 0.875]$ eV lies below it. The factor between the two is exactly 9.
* **The CKM triangle is the $d$–$b$ column triangle** $z_k = V_{kd} V_{kb}^{*}$ summed over the three up-type rows; closure $z_1 + z_2 + z_3 = 0$ is exact in $\mathbb{Q}(i)$ because it is a column of $V^\dagger V = I$.

## 2. Claim Hygiene Summary

1. **What it supports:**
   * Checked by [`qed_weak_hadronic_finite_maps.rs`](../../../../../omega_engine/crates_rs/omega_quantum_physics/src/qed_weak_hadronic_finite_maps.rs) (5 inline tests), [`qed_weak_hadronic_control.py`](../python/finite_qm/use_cases/qed_weak_hadronic_control.py) (9 e2e tests) and the Lean theorems `kn_forward` through `gmo_omega_from_spacing` in [`FiniteQFTAndGravity.lean`](../../lean4/FiniteQFTAndGravity.lean): the Klein–Nishina forward value, Thomson limit and normalization; the $s \leftrightarrow u$ crossing; the chiral projector algebra; the factorization of $f_0$; the sign of the one-loop muon bracket; the ABJ factor and the factor 9; the octet and decuplet GMO identities as polynomial identities in $(M_0, M_1, M_2)$.
   * Checked in Rust and Python only: the Fermi-constant enclosure $G_F/(\hbar c)^3 \in [1.16638176 \times 10^{-5}, 1.16638177 \times 10^{-5}]\ \mathrm{GeV}^{-2}$ inside the requested window $[1.1663 \times 10^{-5}, 1.1665 \times 10^{-5}]$; the CKM matrix with exact $V^\dagger V = V V^\dagger = I$, exact triangle closure and Jarlskog $J \neq 0$ with $|V_{us}|^2$ and $|V_{cb}|^2$ within ten percent of $\lambda^2$ and $A^2\lambda^4$ at $\lambda = 9/40$, $A = 4/5$; the octet residual $5.7 \times 10^{-3}$ (within $0.6\%$) and the decuplet $\Omega^-$ prediction $1682.2$ MeV against $1672.45$ MeV (residual $0.58\%$, within $1\%$).
2. **What it does not support:**
   * The enclosures use the toy inputs declared in the modules (PDG-style masses and couplings as exact rationals) and do not compute radiative corrections beyond the one-loop bracket quoted, nor QCD corrections to the pion rate, nor the full Wolfenstein hierarchy of the CKM matrix. The Lean file does not elaborate the CKM, $G_F$ or interval claims.
   * `FiniteQFTAndGravity.lean` elaborates cleanly with core Lean 4 (`lean lean4/FiniteQFTAndGravity.lean`, no imports, zero warnings, zero `sorryAx`). A full `lake build` of the `quantum_mechanics` package requires Mathlib in an environment with network or cached Mathlib artifacts.
3. **The narrowest defensible claim:**
   * Within the implemented code and at the listed inputs, the stated rational and Gaussian-rational identities hold, the stated interval enclosures contain the stated values, and the stated windows contain the enclosures. No statement about nature beyond those identities is made.
4. **The next test needed:**
   * Extend the Lean 4 mechanization to cover the $3 \times 3$ Gaussian-rational CKM Cayley transform and rational interval enclosures, or run `lake build` in an environment with cached Mathlib artifacts.

## 3. QM-226: Klein–Nishina, Thomson Limit, Bhabha/Møller Crossing

### 3.1 Klein–Nishina ratio over $\mathbb{Q}$

With $x = \hbar\omega / (m_e c^2)$ and $u = \cos\theta$, the frequency ratio is $\eta(x, u) = 1/(1 + x(1 - u))$ and

$$R(x, u) = \tfrac{1}{2}\,\eta^2\,\big(\eta + \eta^{-1} - (1 - u^2)\big).$$

Forward scattering gives $\eta(x, 1) = 1$ and $R(x, 1) = 1$ for every $x$; the Thomson limit $x = 0$ gives $R(0, u) = \tfrac{1}{2}(1 + u^2)$, and the normalized weight $\tfrac{3}{8}(1 + u^2)$ integrates to exactly 1 over $u \in [-1, 1]$ through the antiderivative $F(u) = \tfrac{3}{8}(u + u^3/3)$, $F(1) - F(-1) = 1$. Sample values at $x \in \{1/10, 1, 2\}$ and $u \in \{-1, 0, 1\}$:

| $x$ | $u = -1$ | $u = 0$ | $u = 1$ |
| --- | --- | --- | --- |
| $1/10$ | $305/432$ | $555/1331$ | $1$ |
| $1$ | $5/27$ | $3/16$ | $1$ |
| $2$ | $13/125$ | $7/54$ | $1$ |

The Lean theorems `kn_forward`, `kn_thomson`, `kn_samples`, `kn_sample_etas` and `thomson_normalized` state these in a division-free form where $\eta^{-1}$ enters as the polynomial $1 + x(1 - u)$; `kn_textbook_form` ties that form to the expression with $1/\eta$ under the hypothesis $\eta\,(1 + x(1-u)) = 1$.

### 3.2 Bhabha and Møller

The reduced tree-level amplitudes (spin-averaged, massless, units of $2e^4$) are as in section 1.1, with $s + t + u = 0$. The crossing $M_{\mathrm{M\o ller}}(s,t,u) = M_{\mathrm{Bhabha}}(u,t,s)$ and the $t \leftrightarrow u$ symmetry of Møller are proved for all nonzero arguments by `moller_eq_bhabha_su` and `moller_tu_symmetric`; the Python audit stores the amplitudes and recomputes the checks `crossing_s_u_holds`, `moller_t_u_symmetric` and `s_t_swap_fails` (the $s \leftrightarrow t$ counterexample) from them; a Mandelstam triple with $s + t + u \neq 0$ is refused.

## 4. QM-227: Chiral Projectors, Muon Decay, $G_F$, CKM

### 4.1 Chiral projectors in the Weyl basis

The Python and Rust modules take the existing Dirac-basis gammas $\gamma_D^\mu$ over $\mathbb{Q}(i)$ and move them to the Weyl basis by $\gamma_W^\mu = \tfrac{1}{2} V \gamma_D^\mu V^{T}$ with $V = \begin{pmatrix} I & -I \\ I & I \end{pmatrix}$, $V V^{T} = 2I$; the two factors $1/\sqrt{2}$ of the orthogonal change of basis multiply to $1/2$, so the change stays inside $\mathbb{Q}(i)$. They check the Clifford relations $\{\gamma^\mu, \gamma^\nu\} = 2\eta^{\mu\nu}$, form $\gamma^5 = i\gamma^0\gamma^1\gamma^2\gamma^3 = \operatorname{diag}(-1,-1,1,1)$, and check that it squares to $I$ and anticommutes with each $\gamma^\mu$. The Lean file takes $\gamma^5$ in its diagonal form over a rational $4 \times 4$ structure `Mat4Rat` and states as theorems (`chiral_projectors`, `chiral_projectors_explicit`, `projL_projR_vec`):

* $P_L^2 = P_L$, $P_R^2 = P_R$, $P_L P_R = P_R P_L = 0$, $P_L + P_R = I$, $\operatorname{tr} P_L = \operatorname{tr} P_R = 2$;
* $P_L = \operatorname{diag}(1,1,0,0)$, $P_R = \operatorname{diag}(0,0,1,1)$;
* $P_L (P_R v) = 0$ for every rational 4-vector $v$.

The executable audits also apply $P_R$ to a fixed Gaussian-rational test spinor and check that the $V - A$ projector $P_L$ annihilates the result (`v_minus_a_current_kills_right_handed`).

### 4.2 Muon decay and the Fermi constant

With $x = (m_e/m_\mu)^2$, $f_0(x) = 1 - 8x + 8x^3 - x^4$ factors as $(1 - x)(1 - 7x - 7x^2 + x^3)$ (`muonF0_factor`), with $f_0(0) = 1$ and $f_0(1) = 0$. The radiative term $-12x^2 \ln x$ is enclosed through the atanh-series enclosure of $\ln x$, and the one-loop bracket $\tfrac{\alpha}{2\pi}(\tfrac{25}{4} - \pi^2)$ is negative because any rational lower bound $p > 5/2$ of $\pi$ already gives $25/4 - p^2 < 0$ (`muon_qed_correction_negative`; the Machin enclosure gives $p > 3$). Inverting $\tau_\mu^{-1} = G_F^2 m_\mu^5 f(x)(1 + \Delta q)/(192\pi^3)$ with interval arithmetic and an isqrt-based square-root enclosure yields $G_F/(\hbar c)^3 \in [1.16638176, 1.16638177] \times 10^{-5}\ \mathrm{GeV}^{-2}$, inside the requested window.

### 4.3 CKM over $\mathbb{Q}(i)$

A skew-Hermitian generator $A \in M_3(\mathbb{Q}(i))$ with entries chosen near $\lambda = 9/40$ and $A_W = 4/5$ gives $V = (I - A)(I + A)^{-1}$ by an exact Gaussian-rational $3 \times 3$ inverse. The audit checks $V^\dagger V = V V^\dagger = I$ exactly, the $d$–$b$ column triangle $z_1 + z_2 + z_3 = 0$ exactly, the Jarlskog invariant $J = \operatorname{Im}(V_{ud} V_{cs} V_{us}^* V_{cd}^*) \neq 0$ with consistency across quartets, and that $|V_{us}|^2$ and $|V_{cb}|^2$ sit within ten percent of $\lambda^2 = 81/1600$ and $A^2\lambda^4 = 6561/4000000$. This part has no Lean counterpart in this file.

## 5. QM-228: ABJ Colour Factor and Gell-Mann–Okubo

### 5.1 $\pi^0 \to \gamma\gamma$

$S(N_c) = N_c\,(Q_u^2 - Q_d^2) = N_c/3$, so $S(3) = 1$, $S(1) = 1/3$, and the rate ratio is $S(3)^2/S(1)^2 = 9$ (`abj_factor_closed`, `abj_factor_values`, `abj_rate_ratio`). The rate $\Gamma = \alpha^2 m_\pi^3 S^2/(64\pi^3 f_\pi^2)$ with the Machin $\pi$ enclosure gives the enclosures of section 1.1.

### 5.2 Gell-Mann–Okubo

For $M = M_0 + M_1 Y + M_2\,(I(I+1) - Y^2/4)$ the octet relation $2(M_N + M_\Xi) = 3M_\Lambda + M_\Sigma$ at $(I, Y) = (\tfrac12, 1), (\tfrac12, -1), (0, 0), (1, 0)$ and the decuplet equal spacing at $(\tfrac32, 1), (1, 0), (\tfrac12, -1), (0, -2)$ are polynomial identities in $(M_0, M_1, M_2)$. The Python module computes them as coefficient vectors: `su3_mass_coefficients` gives the coefficients of $(M_0, M_1, M_2)$ for each $(I, Y)$, `gmo_octet_relation_coefficients` gives the octet combination (the zero vector), and `gmo_decuplet_second_differences` gives the two second differences of the decuplet (both zero). The common spacing is $-(M_1 + \tfrac32 M_2)$ and $M_\Omega = 2M_{\Xi^*} - M_{\Sigma^*}$ (`gmo_octet`, `gmo_decuplet_equal_spacing`, `gmo_decuplet_spacing_value`, `gmo_omega_from_spacing`). On the PDG-style rational inputs declared in the Python module the octet fractional residual is $1934636849/340515200000 \approx 5.7 \times 10^{-3}$ and the $\Omega^-$ equal-spacing prediction is $504667/300 \approx 1682.2$ MeV against $1672.45$ MeV.

## 6. Reproduction

From the repository root:

```text
cd sources/atlas/papers/finite_quantum_mechanics
python3 -m pytest tests/e2e/test_e2e_qed_weak_hadronic_control.py -q
cd ../../../../../omega_engine/crates_rs
cargo test -j 1 -p omega_quantum_physics --lib -- qed_weak_hadronic
cd ../../lean4/quantum_mechanics
lean FiniteQFTAndGravity.lean
```

The Lean file has no imports, so `lean FiniteQFTAndGravity.lean` from `lean4/quantum_mechanics` elaborates it with the core toolchain pinned by `lean4/lean-toolchain`; `lake build` of the whole package also needs Mathlib.
