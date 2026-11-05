# 006 Vector And Quantum Observer Geometries

## Gauge Relativity and Trace Metric Bounds

**Author:** Jeremy H. Carroll

**Date:** 2026-09-21

**Version:** v0.4

**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)  

## Abstract

Scalar-valued edge defects are not comprehensive. The local defect carrier may be vector- or operator-valued, while the declared observer gauge maps its residual class to a scalar magnitude. In finite obstruction calculus, the residual class may be algebraically fixed relative to the declared repair quotient while its measured scalar magnitude depends on the observer gauge used to measure local defects. A three-edge cycle already shows the split: coordinate-channel sensing gives $\Phi=2$ (scalar $\ell^1$), while Euclidean vector-displacement sensing gives $\Phi=\sqrt{2}$ ($\ell^1(E;\ell^2)$). This note develops two non-scalar observer geometries — the Euclidean vector gauge and a quantum trace-distance gauge — with explicit dual-witness theory and a shared $\Phi\Gamma R$ closure signature. All results are finite-dimensional and finite-graph.

**Why a researcher should care.** Anyone building a diagnostic over vector- or operator-valued bond data — mechanical/synchronization loops, or quantum state-comparison networks — needs to know that the *number* they report is not intrinsic to the defect: it is fixed by the gauge they declare. The same irreducible closure mismatch reads as $2$ to a coordinate-channel detector and $\sqrt2$ to a Euclidean-strain detector. This note also marks the honest line between a gauge that is *selected* by a symmetry theorem (the vector gauge) and one that is *chosen* or *conditionally selected* by an operational measurement axiom (the quantum gauge).

**Falsifiability.** The fork is empirical for a physical detector: a synchronization/strain loop with edge offsets $(1,0),(0,1),(0,0)$ forces a fork. A detector calibrated so that a unit Euclidean displacement has magnitude one must report $\sqrt2$; a detector calibrated to count independent unit coordinate-channel violations must report $2$. A device that measures vector strain yet reports $2$ (or counts channels yet reports $\sqrt2$) falsifies the gauge attribution for that device. The quantum analogue fails if a declared CPTP-compatible repair class makes the triangle quotient obstruction differ from $\tfrac12\lVert c\rVert_1$.

Positioning: Relation to Non-Scalar Observer Geometries and Operational Selection

In finite obstruction calculus on networks and cell complexes, the local defect carrier can be vector- or operator-valued rather than scalar. Beyond the standard scalar $\ell^1$ baseline:

> *vector-valued defects with rotational symmetry lead to $\ell^1(E;\ell^2)$, and quantum systems lead to $\ell^1(E;\text{trace norm})$ only after adding the operational assumptions that select trace distance, not from CPTP monotonicity alone.*
>
The two branches are **not symmetric in their justification**, and this note keeps that asymmetry explicit:

* **Vector branch — the $\ell^2$ stalk gauge is *selected* (proven).** Among faithful, absolutely homogeneous, convex edge gauges invariant under the rotation group $\mathrm{SO}(k)$ acting on the edge stalk $\mathbb R^k$, the only gauges are $j(x)=c\lVert x\rVert_2$. This is a proven theorem (*SO(k)-Invariant Gauge Classification and the $\ell^1(E;\ell^2)$ Obstruction Geometry*, Thm 3.1) — not a mere stipulation. The vector branch below therefore computes with a gauge that declared continuous rotation symmetry forces.
* **Quantum branch — the trace-distance stalk gauge is *conditionally selected* (proven under declared operational axioms).** Channel monotonicity under completely positive trace-preserving (CPTP) maps does **not** single out trace distance:
  $$ \big(\forall \Lambda \in \mathrm{CPTP},\; j(\Lambda(X)) \le j(X)\big) \;\not\Longrightarrow\; j(X) = \frac{1}{2}\|X\|_1. $$
  As mechanized in `QM.scale_monotone` and `QM.cptp_monotone_not_select`, monotonicity is scale-invariant, and a broad landscape of functionals (Petz monotone Riemannian metrics, relative entropies, fidelity-derived quantities) contract under CPTP maps. However, once the operational **single-shot binary discrimination axiom** (Holevo–Helstrom / classical total-variation reduction) is declared, the half-trace norm $j(X) = \frac{1}{2}\|X\|_1$ is uniquely selected on Hermitian trace-zero operators. This establishes trace distance as an exact conditional selection theorem.
* **Classical population shadows and $\ell^1$ contraction.** For any finite CPTP channel $\mathcal{E}(\rho) = \sum_k A_k \rho A_k^\dagger$ with $\sum_k A_k^\dagger A_k = I$, choosing an orthonormal basis and reading only the output diagonal yields a column-stochastic Markov population shadow $K(\gamma'\mid\gamma) = \sum_k |\langle\gamma'|A_k|\gamma\rangle|^2$ (`QM.StochasticChannel`). Column-stochastic kernels contract the classical $\ell^1$ norm, $\|S x\|_1 \le \|x\|_1$ (`QM.stochastic_l1_contraction`), providing the elementary commutative shadow of the quantum data-processing inequality. Complete positivity and coherence transport constitute the non-commutative lift.
* **Trace-norm operator duality.** Full graph-level quotient duality ($d_0^*\varphi = 0$, Helstrom effects) and operator-level trace-norm geometry are developed in companion work on CPTP-compatible obstruction theory (*CPTP-Compatible Obstruction Theory: Trace-Norm Geometry and Quantum Dual Witnesses*, Carroll, 2026, Zenodo DOI: `10.5281/zenodo.20550459`).

The shared machinery — quotient norm $\Phi$, dual witnesses, the closure invariant $\Gamma_2$ and ratio $R_{cl}$ — specializes general obstruction calculus to two non-scalar stalks. **Notation** ($\Phi$, $d_0$, $d_1$, $Q^1$, cycle circulation $c$, coboundary $\delta_e$) follows standard obstruction complexes; trace distance $\tfrac12\lVert\cdot\rVert_1$, CPTP contractivity, and Helstrom duality are standard quantum-information facts.

Explicit Vector Carrier

Let the underlying graph be $P = (V,E)$. The general vector cochain carriers are explicitly declared as:
$$
C^0=(\mathbb R^k)^V,\qquad
C^1=(\mathbb R^k)^E,
$$
with observed 1-cochain defect datum $\omega\in C^1$, repair boundary $d_0:C^0\to C^1$, and the explicit equivalence relation:
$$
\omega\sim_{\mathrm{ZeroRel}}\omega'
\iff
\omega-\omega'\in\operatorname{im}(d_0).
$$
The vector repair quotient is thus structurally defined as:
$$
Q^1_{\mathrm{vec}}=C^1/\operatorname{im}(d_0).
$$

The Triangle Fixture

Consider a 3-cycle $V=\{0,1,2\}$ with directed edges $E=\{(0,1),(1,2),(2,0)\}$.
The required (target) displacements over the edges are:

* $\omega_{01} = (1, 0)$
* $\omega_{12} = (0, 1)$
* $\omega_{20} = (0, 0)$

The net cycle circulation is $c = (1, 1)$.

For any repair $\alpha$, the exact component $d_0\alpha$ has zero cycle circulation, so the class keeps the same circulation:
$$
\sum_{\text{cycle}}(\omega-d_0\alpha)=\sum_{\text{cycle}}\omega=c.
$$

The quotient minimization reduces to:
$$
\min_{r_1+r_2+r_3=c}\sum_e j(r_e).
$$

Two Observers, Two Magnitudes

We compare two local observer gauge systems $j(x,y)$:

1. **Coordinate-channel observer:** $j_{1,1}(x,y)=|x|+|y|$
   Treats $x$ and $y$ as separable additive channels. This yields an $\ell^1$ magnitude:
   $$
   \Phi_{1,1}=|(1,1)|_1=2.
   $$

2. **Vector-displacement observer:** $j_{2,1}(x,y)=\sqrt{x^2+y^2}$
   Yields an $\ell^1(E;\ell^2)$ geometry: additive over edges, Euclidean within each edge stalk.
   $$
   \Phi_{2,1}=|(1,1)|_2=\sqrt{2}.
   $$

Same graph. Same edge signal. Same residual class. Different observer gauge. Different obstruction magnitude.

Why the Class Is the Same

Cycle circulation is preserved modulo repair. For any repair cochain $\alpha$, the coboundary $d_0\alpha$ telescopes around the cycle to zero. So the quotient class always carries the full circulation $c = (1,1)$, regardless of which gauge is used.

Why the Magnitude Changes

The local gauge changes from $\ell^1$ to $\ell^2$.

Scalar $\ell^1$ says: *x-error and y-error are independent failures.*
Vector $J_{2,1}$ says: *(x,y) is one physical displacement error.*

A mechanical/synchronization system with true vector-valued bond defects should measure $\sqrt{2}$, not $2$. A system that independently counts coordinate-channel violations should measure $2$, not $\sqrt{2}$. That is a concrete falsifiable fork: same topology, same signal, different gauge, different obstruction.

Analytic Proof

**[PROVEN — single-cycle fixture].** The proof of magnitude is a direct application of the triangle inequality (subadditivity of the gauge $j$, with $j(0)=0$). It is stated for the single 3-cycle above; on a general finite graph the magnitude is characterized *dually* by the Mixed Vector Obstruction Duality theorem below, not by this single-edge reduction.
$$
\sum_e j(r_e)\ge j\left(\sum_e r_e\right)=j(c).
$$

Equality is attained by putting all residual on one edge:
$$
r_{01}=c,\quad r_{12}=0,\quad r_{20}=0.
$$

Therefore:
$$
\Phi_J([\omega])=j(c).
$$

Then the two observer choices give:
$$
\Phi_{1,1}=j_{1,1}(1,1)=2,
$$
$$
\Phi_{2,1}=j_{2,1}(1,1)=\sqrt{2}.
$$

**Weighting note.** With positive edge weights $w_e$ on a single cycle, routing all residual onto the lightest edge gives quotient value $(\min_e w_e)\,j(c)$; the clean $2$-versus-$\sqrt2$ comparison above is the normalized equal-weight case ($w_e\equiv 1$), matching the convention of the $SO(k)$-invariant gauge classification.

Executable Sanity Check

**[PROVEN, NUMERICAL / DIRECT COMPUTATION]** (self-contained replay; no external certificate claimed). As a numerical sanity check, we approximate the quotient obstruction by minimizing the residual over local repair cochains $\alpha$; the analytic proof above is the exact statement.

```python
import numpy as np
from scipy.optimize import minimize

delta = np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]])

def d0(alpha):
    return np.array([alpha[1] - alpha[0], alpha[2] - alpha[1], alpha[0] - alpha[2]])

def objective_L1_L1(x):
    alpha = x.reshape(3, 2)
    return np.sum(np.abs(delta - d0(alpha)))

def objective_L1_L2(x):
    alpha = x.reshape(3, 2)
    return np.sum(np.linalg.norm(delta - d0(alpha), axis=1))

x0 = np.zeros(6)
res_L1 = minimize(objective_L1_L1, x0, method='Nelder-Mead', options={'maxiter':10000, 'xatol':1e-8, 'fatol':1e-8})
res_L2 = minimize(objective_L1_L2, x0, method='Nelder-Mead', options={'maxiter':10000, 'xatol':1e-8, 'fatol':1e-8})

print(f'L1-L1 minimum: {res_L1.fun:.6f}')
print(f'L1-L2 minimum: {res_L2.fun:.6f}')
```

Results:

```text
L1-L1 minimum: 2.000000
L1-L2 minimum: 1.414214
```

The numerical optimization matches the analytic values to displayed precision.

Physical Interpretation

Build a 3-node mechanical/synchronization loop where the preferred edge offsets are:

* $0\to1$ requires displacement $(1,0)$
* $1\to2$ requires displacement $(0,1)$
* $2\to0$ requires displacement $(0,0)$

Then measure total irreducible closure mismatch.
Expected result:

* component-counting detector: 2
* Euclidean vector detector: $\sqrt{2}$

If the declared detector response is Euclidean per-bond magnitude, the $J_{2,1}$ attribution is the matching observer model. If the detector independently counts coordinate-channel violations, the scalar $\ell^1$ attribution is the matching observer model.

Generalization: Mixed Vector Obstruction

> **[PROVEN — finite-dimensional convex (Fenchel) duality] Theorem — Mixed Vector Obstruction Duality**
> Let $P$ be a finite directed graph and let edge defects lie in $\mathbb{R}^k$. Define
> $$
> \Phi_{2,1}([\omega])=\inf_\alpha\sum_e\|\omega_e-(d_0\alpha)_e\|_2 .
> $$
> Then
> $$
> \Phi_{2,1}([\omega])
> =
> \max_{\varphi}
> \sum_e \langle \varphi_e,\omega_e\rangle
> $$
> subject to
> $$
> d_0^*\varphi=0,\qquad \|\varphi_e\|_2\le 1\quad\text{for every edge }e.
> $$
> Thus the dual witnesses are Euclidean-unit-bounded divergence-free vector circulations.
> *(Lean: weak vector duality in `mixed_vector_duality.lean` [`weak_vector_duality_pointwise`, `weak_vector_duality_quotient`, `duality_gap_zero_certificate`]; strong duality, complementary slackness, and Hahn–Banach separation in `strong_vector_duality.lean` [`subgradient_attainment`, `dual_witness_is_maximizer`, `strong_duality_minimax_identity`, `complementary_slackness_edge_alignment`, `strong_vector_duality_of_stationary_subgradient`, `hahn_banach_separation_existence`]; lake build green, axioms `[propext, Classical.choice, Quot.sound]`)*
>
> *Proof.* This is finite-dimensional convex duality. The primal minimizes the convex function $\sum_e\|r_e\|_2$ over the affine space $r=\omega-d_0\alpha$. The convex conjugate of $\|\cdot\|_2$ is the indicator of the Euclidean unit ball, and minimizing over $\alpha$ imposes the stationarity constraint $d_0^*\varphi=0$. Weak duality ($\sum_e \langle \varphi_e, \omega_e \rangle \le \sum_e \|\omega_e - (d_0 \alpha)_e\|_2$) follows pointwise from Cauchy–Schwarz and divergence-free orthogonality; strong duality holds by finite-dimensional Fenchel–Rockafellar duality with subgradient alignment $\varphi_e^* = r_e^* / \|r_e^*\|_2$ on active defect edges. $\square$
>
> **[PROVEN, CONDITIONAL + declared 2-cell $d_1$ with $d_1d_0=0$] Theorem — Mixed Closure Bound**
> Suppose a finite 2-cell operator $d_1$ is declared with $d_1d_0=0$, and define
> $$
> \Gamma_2([h])=\sum_f\|(d_1h)_f\|_2 .
> $$
> Then
> $$
> \Gamma_2([h])\le \|d_1\|_{(2,1\to 2,1)}\,\Phi_{2,1}([h]).
> $$
>
> *Proof.* For every repair $\alpha$, $d_1(h-d_0\alpha)=d_1h$ because $d_1d_0=0$. Hence
> $$
> \Gamma_2([h])
> =
> \|d_1(h-d_0\alpha)\|_{2,1}
> \le
> \|d_1\|_{(2,1\to2,1)}\|h-d_0\alpha\|_{2,1}.
> $$
> Taking the infimum over $\alpha$ gives the claimed bound. $\square$
>
**[PROVEN, CONDITIONAL + declared 2-cell].** In the separately declared filled-triangle carrier, the same edge datum has nonzero closure charge and $R_{cl}=1$. Relating this classification to the unfilled-cycle carrier requires an explicit carrier-change transport. The closure invariant $\Gamma_2$ detects whether the residual is a true cycle obstruction or a filled-cell closure failure uniformly under this Euclidean metric.

Continuous Gauge Action and Spectral Invariance of the Obstruction Operator

**Authority:** finite-dimensional, finite-graph structural results under the declared observer gauge and the declared Hilbertization below. No physical, dynamical, or empirical claims. No spectral quantity computed here mints authority; observers reveal or erase, they do not create obstruction.

### G.1 Hilbertized finite truncation (declared structure)

**Definition G.1 (Hilbertization).** Equip the declared carriers with inner products: on $C^1=(\mathbb R^k)^E$,
$$\langle\omega,\omega'\rangle \;:=\; \sum_{e\in E}\langle\omega_e,\omega'_e\rangle_{\mathbb R^k},$$
with edge weights $w_e\equiv1$ (the normalized equal-weight convention of the paper's Weighting note), and analogously on $C^0$ and, when a 2-cell layer is declared, on $C^2$. On the quantum carriers $C^p_Q$ use the trace pairing $\langle\varphi,\delta\rangle=\sum\operatorname{Tr}(\varphi\,\delta)$ already used by the Quantum Trace-Norm Obstruction Duality theorem. The complex model is $C^p_{\mathbb C}:=C^p\otimes_{\mathbb R}\mathbb C$ with the Hermitian extension.

Three fences are declared up front and are load-bearing:

1. **This is an added structure, not an identification.** The paper's observer gauges $\Phi_{1,1}$, $\Phi_{2,1}$, $\Phi_Q$ are $\ell^1$-type edge-additive quantities; the Hilbert ($\ell^2$) structure above is a *distinct* declared observer geometry. The only licensed passage between them is the explicit stalkwise norm comparison $\|x\|_2\le\|x\|_1\le\sqrt{k}\,\|x\|_2$ and the edge-count comparison in Proposition G.3. No silent identification of $\ell^1$ defect norms with $\ell^2$ spectral quantities is made anywhere in this section.
2. **Finite truncation only.** Continuous Hilbert cochain spaces $H_Q$ are Q-layer (continuum) objects, and continuum membership mints no authority ($\Omega_\kappa$ rule). Everything below is computed on the finite-dimensional truncations declared in the paper's carriers; any completion step to a continuum $H_Q$ is out of scope here and is logged as obligation OB-E19-5.
3. **Represented, not cohomological.** All magnitudes below are represented compatibility defect norms measured on the paper's declared quotient $Q^1=C^1/\operatorname{im}(d_0)$. In particular $\|d_0\alpha\|$-type quantities are never treated as $H^1$ classes; the Hodge-style identification in Proposition G.3(b) is available only because the paper's quotient is explicitly constructed, and its cohomological reading additionally needs the declared 2-cell $d_1$ with $d_1d_0=0$.

### G.2 The obstruction operator

**Definition G.2 (sheaf Laplacian; notation fences).** With $d_0^*$ the adjoint under Definition G.1 (the same adjoint that appears in the constraint $d_0^*\varphi=0$ of the Mixed Vector Obstruction Duality theorem), define
$$L_0 \;:=\; d_0^*d_0 \ \text{ on } C^0, \qquad
H^{(1)}_{\mathrm{obstr}} \;:=\; L_1 \;:=\; d_0d_0^* + d_1^*d_1 \ \text{ on } C^1,$$
the second form only when a 2-cell operator $d_1$ with $d_1d_0=0$ is declared (the same conditional convention as the Mixed Closure Bound and Quantum $\Phi\Gamma R$ Signature theorems); with no declared $d_1$, set $H^{(1)}_{\mathrm{obstr}}:=d_0d_0^*$. **Notation fence (primitive distinction):** in this corpus the symbol $\Delta_0$ names the primitive distinction operator; the sheaf Laplacian is therefore always written $L_0:=d_0^*d_0$ and never shares the symbol $\Delta_0$. Both $L_0$ and $L_1$ are real-symmetric positive semidefinite in the real model and self-adjoint positive semidefinite in the complex model.

**Notation fence (two obstruction operators; no shared symbol).** The Rust conformance target of G.9 realizes a **distinct** operator: per its module docs it computes the degree-0 operator
$$H^{(0)}_{\mathrm{obstr}} \;:=\; L_0 + V_{\mathrm{defect}} \;=\; \delta^\top\delta + V_{\mathrm{defect}} \ \text{ on } C^0,$$
where $V_{\mathrm{defect}}$ is a disclosed symmetric defect potential — not this section's degree-1 operator $H^{(1)}_{\mathrm{obstr}}=L_1$ on $C^1$, which carries no potential term. The bare symbol $H_{\mathrm{obstr}}$ is therefore not used in this section: the superscript always discloses the cochain degree, and one symbol never names both operators. Extending the solver with an $L_1$-side ($C^1$/$d_1$) entry point is typed obligation OB-E19-8. Wherever an $L_1$-side conclusion is wanted from an $L_0$-side replay, the declared bridge is the one-line SVD fact — declared here, never silently assumed — that $\operatorname{spec}(d_0d_0^*)$ and $\operatorname{spec}(d_0^*d_0)$ agree away from $0$.

The smallest nonzero eigenvalue of $L_0$ measures spectral conditioning and connectivity of the declared carrier. It does **not** measure semantic agreement hardness, and no such reading is proposed.

### G.3 The $\ell^2$ quotient realization and its comparison to $\Phi_{2,1}$

**Proposition G.3.** Let $\Pi^\perp$ be the orthogonal projection of $C^1$ onto $\ker d_0^*=\operatorname{im}(d_0)^\perp$.
(a) The map $\operatorname{im}(d_0)^\perp\to Q^1$, $h\mapsto[h]$, is a linear bijection, and the $\ell^2$ quotient magnitude satisfies
$$\Phi_{2,2}([\omega]) \;:=\; \min_{\alpha}\ \|\omega-d_0\alpha\|_2 \;=\; \|\Pi^\perp\omega\|_2 .$$
(b) When $d_1$ with $d_1d_0=0$ is declared, $\ker L_1=\ker d_0^*\cap\ker d_1$, and this harmonic space is linearly bijective with the subquotient $\ker d_1/\operatorname{im} d_0$ (the cohomological reading licensed by fence G.1.3).
(c) Comparison with the paper's mixed gauge:
$$\Phi_{2,2}([\omega])\ \le\ \Phi_{2,1}([\omega])\ \le\ \sqrt{|E|}\;\Phi_{2,2}([\omega]).$$

*Proof.* (a) is the finite-dimensional orthogonal decomposition $C^1=\operatorname{im}(d_0)\oplus\operatorname{im}(d_0)^\perp$; the minimum over the affine space $\omega-\operatorname{im}(d_0)$ of the $\ell^2$ norm is attained at the orthogonal projection. (b) $L_1h=0$ iff $\langle L_1h,h\rangle=\|d_0^*h\|_2^2+\|d_1h\|_2^2=0$; the bijection with the subquotient is the standard finite-dimensional Hodge decomposition for $d_1d_0=0$. (c) For any residual $r=\omega-d_0\alpha$: $\|r\|_2=(\sum_e\|r_e\|_2^2)^{1/2}\le\sum_e\|r_e\|_2=\|r\|_{2,1}$, and by Cauchy–Schwarz $\|r\|_{2,1}\le\sqrt{|E|}\,\|r\|_2$; minimize each side over $\alpha$. $\square$

This shows in this model that the spectral object $L_1$ and the paper's $\Phi_{2,1}$ live on the same declared quotient but read it through different gauges, with explicit constants — the assumption-carrying bridge demanded by fence G.1.1.

### G.4 The continuous gauge action

**Definition G.4 (one-parameter gauge groups; real and complex forms).**

* **Complex model:** for $G=G^*$ self-adjoint on a finite truncation, set $U(\lambda):=\exp(i\lambda G)$, $\lambda\in\mathbb R$. Then $U(\lambda)^*U(\lambda)=I$ and $U(\lambda+\mu)=U(\lambda)U(\mu)$ (finite-dimensional matrix exponential; no Stone-theorem subtlety at this truncation). On a quantum edge stalk the action is conjugation $X\mapsto U X U^*$, which preserves Hermiticity, tracelessness — hence the carrier $\operatorname{Herm}_0(H_e)$ of Model II §1 — and the trace norm.
* **Real form:** for $A^\top=-A$ skew-symmetric, set $O(\lambda):=\exp(\lambda A)\in SO(n)$. This is the form acting on the vector stalks $\mathbb R^k$ of the Explicit Vector Carrier. **The Rust conformance target implements the real form only** (see G.9).

A *gauge action on the complex* is a degreewise family $(U_0,U_1)$ (and $U_2$ when $d_1$ is declared) of unitaries/orthogonals. It is **transport-licensed** when the intertwining witness
$$U_1 d_0 \;=\; d_0 U_0 \qquad(\text{and } U_2 d_1 = d_1 U_1 \text{ when declared})$$
holds — deliberately the same shape as the typed cochain transformation $\Lambda^1d_0=d_0'\Lambda^0$ in the paper's Theorem — CPTP Monotonicity. Without the witness the correct verdict is `NoRule` or `TransportLicenseNeeded`, exactly as there.

**Remark G.4.1 (two different actions; do not conflate).** The paper's repair action $\omega\mapsto\omega-d_0\alpha$ moves a representative *within* the class $[\omega]$ (Why the Class Is the Same). The conjugation action above moves the *observer frame* and, when transport-licensed, acts *on* classes. In the abelian limit of the deformation-theoretic gauge action of G.7 (bracket $\equiv0$), that action degenerates precisely to $\tau\mapsto\tau-dx$, i.e. to the paper's repair action. The two coincide only in that degenerate case.

### G.5 Spectral invariance under conjugation

**Proposition G.5 (spectral invariance).** Let $H$ be self-adjoint (real-symmetric in the real model) and $U$ unitary (orthogonal) on the finite truncation. Then $UHU^*$ has the same spectrum as $H$, with multiplicities. Consequently $\lambda_0(H)$, the spectral gap $\gamma:=\lambda_1-\lambda_0$, and every decay rate of the imaginary-time semigroup $t\mapsto e^{-tH}$ are invariant under conjugation.

*Proof (two lines).* $UHU^*-\mu I=U(H-\mu I)U^*$, so $\det(UHU^*-\mu I)=\det(H-\mu I)$ for all $\mu$: the characteristic polynomials coincide, hence spectra and multiplicities coincide. For the semigroup, $e^{-t\,UHU^*}=U e^{-tH}U^*$ termwise in the exponential series, so each eigenmode $Hv=\lambda v$ transports to $UHU^*(Uv)=\lambda\,Uv$ with decay $e^{-\lambda t}$ unchanged. $\square$

**Domain restriction (declared).** The ground-state decay $e^{-tH^{(1)}_{\mathrm{obstr}}}$ (and the solver's $e^{-tH^{(0)}_{\mathrm{obstr}}}$) is a mathematical analogy inside the declared finite model. It is not physical quantum mechanics, not quantum gravity, and not an empirical claim of any kind; this repeats the paper's "No physical quantum substrate" fence at the continuous-action level.

**Corollary G.5.1 (Laplacian transport: three cases, kept separate).**
(i) *Unconditional conjugation algebra — no license involved.* For arbitrary unitaries (orthogonals) $U_0,U_1$ (and $U_2$ when $d_1$ is declared), if one *defines* $d_0':=U_1d_0U_0^*$ (and $d_1':=U_2d_1U_1^*$), then $L_0'=U_0L_0U_0^*$ and $H^{(1)\prime}_{\mathrm{obstr}}=U_1H^{(1)}_{\mathrm{obstr}}U_1^*$ by conjugation algebra alone, and Proposition G.5 gives spectral equality unconditionally: a conjugation-defined presentation carries the same spectral data by construction, whether or not any intertwining witness holds.
(ii) *Licensed action on a fixed complex.* When the (unprimed) witness $U_1d_0=d_0U_0$ of G.4 holds, then $d_0'=U_1d_0U_0^*=d_0U_0U_0^*=d_0$: the action is an automorphism of the **same** complex, and the spectral conditioning data — $\lambda_0$, the smallest nonzero eigenvalue of $L_0$, the gap, the decay rates — are fixed points of the gauge action on that complex.
(iii) *Independently given second presentation.* When a second presentation $(C'^\bullet,d_0')$ is **given** (not defined by conjugation from the first) and no cross-presentation witness $U_1d_0=d_0'U_0$ is exhibited — the primed shape of the paper's Theorem — CPTP Monotonicity — no relation between $\operatorname{spec}(L_0)$ and $\operatorname{spec}(L_0')$ is asserted: `NoRule`, matching G.7(c). The verdict `NoRule` is reserved for this case only; it does not apply to case (i), whose spectral equality is definitional.

### G.6 A licensed action under a declared assumption: shared stalkwise $SO(k)$ on the vector carrier

**Proposition G.6.** **Declared assumption (identity stalk restrictions).** Declare — consistently with the paper's telescoping convention in Why the Class Is the Same and its Executable Sanity Check, both of which use identity stalk restrictions — that on the Explicit Vector Carrier $d_0=B\otimes I_k$, where $B$ is the signed incidence operator of $P$ and $I_k$ the stalk identity. The anchor's Explicit Vector Carrier section declares $d_0:C^0\to C^1$ abstractly and does not state this tensor form; Proposition G.6 is conditional on this declaration, and vector carriers with nontrivial edge restriction maps (the vector analogue of the quantum branch's $r_{b,a}$) are out of its scope and receive `TransportLicenseNeeded`.

Under the declaration, for every $R\in SO(k)$ the shared stalkwise action $U_0:=I_V\otimes R$, $U_1:=I_E\otimes R$ satisfies the intertwining witness:
$$U_1d_0=(I_E\otimes R)(B\otimes I_k)=B\otimes R=(B\otimes I_k)(I_V\otimes R)=d_0U_0 .$$
The shared stalkwise $SO(k)$ action is therefore transport-licensed under the declared assumption, descends to $Q^1$, and:
(a) $\Phi_{2,1}([R\omega])=\Phi_{2,1}([\omega])$ — if $\varphi$ is an optimal dual witness in the sense of the Mixed Vector Obstruction Duality theorem, then $R\varphi$ is again feasible ($d_0^*(R\varphi)=R\,d_0^*\varphi=0$ and $\|R\varphi_e\|_2=\|\varphi_e\|_2\le1$) and attains the same value against $R\omega$, which — the dual being a maximum — gives $\Phi_{2,1}([R\omega])\ge\Phi_{2,1}([\omega])$; applying the same argument with $R^{-1}=R^\top\in SO(k)$ to the datum $R\omega$ gives $\Phi_{2,1}([\omega])\ge\Phi_{2,1}([R\omega])$, hence equality;
(b) $\Phi_{2,2}$ and $\operatorname{spec}(H^{(1)}_{\mathrm{obstr}})$ are invariant (Cor. G.5.1(ii) via Prop. G.5);
(c) $\Phi_{1,1}$ is **not** invariant in general — see G.7(b).

Edgewise-independent rotations $(R_e)_{e\in E}$ generally fail the witness unless additional structure is declared; for them the verdict is `TransportLicenseNeeded`.

On the quantum carrier of Model II with identity restrictions, the vertexwise conjugation family $\rho_v\mapsto U\rho_vU^*$ (shared $U$) is likewise licensed; for general CPTP restriction maps $r_{b,a}$ the witness $U\,r_{b,a}=r_{b,a}'\,U$ must be exhibited per edge, or the verdict is again `TransportLicenseNeeded`.

### G.7 What gauge freedom does not do

**(a) It does not remove a Maurer–Cartan defect.** Declare a finite-dimensional differential graded Lie algebra $(L^\bullet,d,[\cdot,\cdot])$ with typing $\tau\in L^1$, gauge parameters $x\in L^0$, and a pronilpotence assumption ($L^0$ nilpotent, or the filtration-complete setting) so that $e^{\operatorname{ad}_x}$ and the gauge action
$$x\cdot\tau \;:=\; e^{\operatorname{ad}_x}(\tau)\;-\;\frac{e^{\operatorname{ad}_x}-\mathrm{id}}{\operatorname{ad}_x}(dx)$$
converge (sign convention declared here; the statement below is convention-independent). Write the curvature
$$F(\tau)\;:=\;d\tau+\tfrac12[\tau,\tau].$$
An element with $F(\tau)\neq0$ is a **Maurer–Cartan defect** carrier — it is at no point called a Maurer–Cartan element. The standard equivariance identity of deformation theory,
$$F(x\cdot\tau)\;=\;e^{\operatorname{ad}_x}\,F(\tau)
\qquad\text{[STANDARD — imported; declared assumptions: dgLa, typing }x\in L^0,\tau\in L^1\text{, pronilpotence]},$$
shows in this model that, since $e^{\operatorname{ad}_x}$ is invertible, $F(\tau)\neq0$ implies $F(x\cdot\tau)\neq0$: the gauge orbit of a nonzero Maurer–Cartan defect contains no flat element. **Without** the pronilpotence and typing assumptions the action itself is undefined and the verdict is `NoRule`. Corpus-local verification of the imported identity is obligation OB-E19-2; it is not re-derived here.

**(b) It does not fix the coordinate-channel reading.** With $k=2$, $A=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$, the rotation $O(\tfrac\pi4)=\exp(\tfrac\pi4A)$ applied stalkwise to the triangle-fixture circulation $c=(1,1)$ gives $O(\tfrac\pi4)c=(0,\sqrt2)$. The coordinate-channel gauge of Two Observers, Two Magnitudes therefore reads $j_{1,1}(c)=2$ before and $j_{1,1}(O(\tfrac\pi4)c)=\sqrt2$ after, while $j_{2,1}$ reads $\sqrt2$ at both points. The $\ell^2$ reading is constant on the licensed gauge orbit; the $\ell^1$ coordinate reading is a function *on* the orbit, not a function *of* the orbit. This is the continuous-orbit restatement of the paper's discrete fork and supports, rather than replaces, its falsifiability reading. (The quantum stalk gauge $\tfrac12\|\cdot\|_1$ **is** invariant under the conjugation action, since the trace norm is unitarily invariant — a standard fact in the sense of the Helstrom and Watrous literature. Invariance is an admissibility-strengthening observation only; it does not select the gauge without operational discrimination axioms.)

**(c) It does not transport represented defect-norm classes without a witness.** Given two presentations $(C^\bullet,d_0)$ and $(C'^\bullet,d_0')$ and a unitary $U_1:C^1\to C'^1$ with $\omega'=U_1\omega$ but **no** intertwining witness $U_1d_0=d_0'U_0$, the image $U_1(\operatorname{im} d_0)$ bears no declared relation to $\operatorname{im} d_0'$, so neither $\Phi'([\omega'])\le\Phi([\omega])$ nor the reverse follows for any of the gauges $\Phi_{1,1},\Phi_{2,1},\Phi_{2,2},\Phi_Q$. Typed verdict: `NoRule` / `TransportLicenseNeeded` — the same discipline the paper already imposes on the quotient part of Theorem — CPTP Monotonicity. With the witness, $U_1$ descends to a bijection of quotients and transports the $\ell^2$ magnitude isometrically; the $\ell^1$-type magnitudes transport under the additional declared assumption that the stalk gauge is orbit-invariant; without that assumption transport can fail — explicit witness in (b) (trace distance: invariant under conjugation; coordinate $\ell^1$: fails at $\lambda=\pi/4$).

### G.8 The discrete shadow: recovering the $SO(k)$ classification

**Proposition G.8.** A stalk gauge $j$ on $\mathbb R^k$ is invariant under every one-parameter flow $\{\exp(\lambda A):\lambda\in\mathbb R\}$, $A^\top=-A$, if and only if it is $SO(k)$-invariant.

*Proof.* One direction is immediate ($\exp(\lambda A)\in SO(k)$). For the converse, $\exp:\mathfrak{so}(k)\to SO(k)$ is surjective ($SO(k)$ compact connected; standard — logged as obligation OB-E19-6 for corpus-local citation or formalization), so every $R\in SO(k)$ lies on some one-parameter flow. $\square$

Combining with the classification theorem for rotation-invariant gauges (among faithful, absolutely homogeneous, convex edge gauges invariant under $\mathrm{SO}(k)$, the only gauges are $j(x)=c\|x\|_2$): **invariance under the continuous gauge action of G.4 forces the $\ell^2$ stalk gauge, up to scale, within that declared class.** The discrete classification is in this precise sense the discrete shadow — the orbit-level invariant theory — of the continuous action introduced here. The vector branch's *selected* status is thereby re-derived from a continuous symmetry demand; the quantum branch's *conditionally selected* status requires the operational binary discrimination axiom.

### G.9 Rust conformance target (not evidence)

The computational counterpart is `omega_engine/crates_rs/omega_solvers/src/solver_spectrum_laplacian.rs`: a finite-truncation solver in the **real-symmetric model** — the real form $O(\lambda)=\exp(\lambda A)$ of G.4 only, not the complex model — with deterministic eigendecomposition (cyclic Jacobi) and disclosed residual certificates emitted as `QSpectralReceipt` values (schema `omega.q-spectral-receipt.v1`). It is referenced as a **conformance target, not as evidence**: no claim in this section rests on it.

**Disclosure:** the solver is maintained in the canonical Rust workspace at `omega_engine/crates_rs/omega_solvers/src/solver_spectrum_laplacian.rs` — module `omega_solvers::solver_spectrum_laplacian` (with alias `omega_solvers::q_obstruction_solver` exported in `omega_solvers/src/lib.rs`), tested by conformance tests in `omega_solvers/tests/q_solver_conformance.rs` under `PKT-20260722-RES-EPOCH19`. Admission through repository gates is completed (discharging obligation OB-E19-7). **Operator reconciliation:** the solver implements both the degree-0 operator $H^{(0)}_{\mathrm{obstr}}=L_0+V_{\mathrm{defect}}=\delta^\top\delta+V_{\mathrm{defect}}$ on the $C^0$ truncation and the degree-1 operator $H^{(1)}_{\mathrm{obstr}}=L_1=\delta\delta^\top$ on $C^1$ via `solve_degree1` (discharging obligation OB-E19-8). Conformance requires: (1) disclosed orthogonality residual $\|O^\top O-I\|$; (2) eigenvalue-invariance replay $\operatorname{spec}(O(L_0+V_{\mathrm{defect}})O^\top)$ vs $\operatorname{spec}(L_0+V_{\mathrm{defect}})$ within disclosed tolerance; (3) determinism (no hidden randomness); (4) diagnostic output only — per repository governance, no spectral quantity, certificate, test result, or signature mints authority.

Architectural Lesson

The overarching structural lesson is clear: obstruction is not a single scalar primitive detached from observation. The quotient class is structural, but the gauge that measures it is part of the declared observer geometry.

What This Does Not Claim

```{=latex}
\begin{nonclaim}
\begin{itemize}
\item No exclusive $\ell^1$. The scalar $\ell^1$ baseline is one observer geometry, not the only one.
\item \textbf{Metric Non-Selection Firewall.} Monotonicity under quantum channels (CPTP maps) does \emph{not} uniquely select the trace-distance gauge: contractivity under all CPTP maps, $j(\Lambda(X)) \le j(X)$, does not imply $j(X) = \frac{1}{2}\|X\|_1$ (formalized in Lean module \texttt{QM.cptp\_monotone\_not\_select}). Monotonicity is scale-invariant (\texttt{QM.scale\_monotone}), and families of distinguishability measures (Petz monotone metrics, relative entropies) contract under CPTP maps. Selecting $\tfrac12\lVert\cdot\rVert_1$ requires an additional operational distinguishability axiom (Holevo--Helstrom / classical total-variation reduction).
\item \textbf{Scope of classical population shadows.} A CPTP channel induces a column-stochastic population shadow $K(\gamma'\mid\gamma) = \sum_k |\langle\gamma'|A_k|\gamma\rangle|^2$ on populations only after choosing an orthonormal basis and reading the output diagonal (Lean \texttt{QM.StochasticChannel}). The classical kernel captures population transport only and does \emph{not} fix off-diagonal coherences or determine the full channel. Complete positivity and coherence transport constitute the non-commutative lift, not forced by the classical kernel alone.
\item \textbf{No general-graph closed form from the single-edge reduction.} The boxed $\Phi_J=j(c)$ is the single-cycle fixture; general finite graphs are characterized \emph{dually} (Mixed Vector Obstruction Duality), not by ``all residual on one edge.''
\item No physical quantum substrate or ontology. The quantum branch below is a mathematical instantiation of operator-valued observer geometry, not an empirical assertion about nature or a derivation of CPTP dynamics.
\item No Born rule derivation.
\item No observer-independent authority.
\end{itemize}
\end{nonclaim}
```

Bottom Line

$$
\boxed{
\Phi_J([\omega])=\min_{\alpha}J(\omega-d_0\alpha)=j(c)
}
$$

where $c$ is the cycle circulation and $j$ is the declared local gauge (**single-cycle fixture**; general finite graphs are handled by the duality theorem above). For $c=(1,1)$:
$$
j=\ell^1 \Rightarrow \Phi=2,
\qquad
j=\ell^2 \Rightarrow \Phi=\sqrt{2}.
$$

Same topology, same signal, different observer gauge, different obstruction magnitude.

## Supplement: Trace-Norm Quantum Observer Geometry

**Authority:** Supplementary. Not primitive axiomatics.

**Status:** Supplementary observer-geometry branch. Not primitive axiomatics.

Model II: Explicit Quantum Carrier & Trace-Norm Observer Geometry

**1. Carrier**
Let $P = (V,E)$. Each vertex carries a finite-dimensional Hilbert space $H_v$. For a coherent finite operator-valued carrier, we declare the explicit cochain groups:
$$
C^0_Q=\bigoplus_v\operatorname{Herm}_0(H_v),
\qquad
C^1_Q=\bigoplus_e\operatorname{Herm}_0(H_e),
$$
where $\operatorname{Herm}_0$ denotes traceless Hermitian operators. The CPTP restriction maps must be understood through their linear extensions to Hermitian operators.

Edge defects are Hermitian differences of compared states. For an edge $e=(a\to b)$, choose a CPTP restriction/comparison map $r_{b,a}: \operatorname{Herm}_0(H_b) \to \operatorname{Herm}_0(H_a)$. For a section $\rho=(\rho_v)_v$, define the edge defect $\delta_e(\rho) := r_{b,a}(\rho_b) - \rho_a$.
The explicit zero relation is:
$$
\delta\sim_{\mathrm{ZeroRel}_Q}\delta'
\iff
\delta-\delta'\in\operatorname{im}(d_0^Q).
$$
A $(C^2_Q,d_1^Q)$ layer exists only after coherent 2-cell comparison data and a verified $d_1^Qd_0^Q=0$ witness are supplied.

**2. Local Gauge & The CPTP Non-Selection Firewall**

To audit trace-norm transport, we explicitly separate imported formal structure from the resulting operational metric. The audit rests on four declared imports:
1. *Quantum Interface:* The carrier is explicitly declared as $M_n(\mathbb{C})$ with Hermitian density operators ($\rho \ge 0$, $\operatorname{Tr}(\rho)=1$).
2. *Binary Single-Shot Discrimination Axiom:* The distinguishability functional must reproduce optimal binary state-discrimination advantage (Helstrom operational axiom).
3. *CPTP Compatibility:* Operational channel dynamics are Completely Positive Trace-Preserving (CPTP) maps over the quantum interface.
4. *Edge Additivity:* Orthogonal states sum additively in the distinguishing metric across independent edges.

*Firewall Theorem (Metric Non-Selection).* Monotonicity under quantum channels (CPTP maps) does **not** uniquely select the trace-distance gauge:
$$ \big(\forall \Lambda \in \mathrm{CPTP},\; j(\Lambda(X)) \le j(X)\big) \;\not\Longrightarrow\; j(X) = \frac{1}{2}\|X\|_1. $$
Mechanized in `QM.scale_monotone`, `QM.cptp_monotone_not_select`, and `QM.cptp_monotone_not_select_traceNorm`. The core mechanism is **scaling invariance**: if $j$ is CPTP-monotone ($j(\Lambda X) \le j(X)$ for all CPTP $\Lambda$), then so is $c \cdot j$ for any positive constant $c > 0$. Hence, monotonicity under data processing cannot fix the scalar normalization, nor does it single out trace distance among the broad landscape of CPTP-contractive functionals (e.g. Petz monotone Riemannian metrics, quantum relative entropies, and fidelity-derived distances). Monotonicity is *necessary* for an operational metric, but *not sufficient* to select it. The counterexample is non-vacuous under genuine contractions (`QM.id_cptpMonotone_halving`).

**2.1 Classical Population Shadows & Stochastic $\ell^1$ Contraction**

*Markov Population Shadows.* Let $\mathcal{E}: M_n(\mathbb{C}) \to M_m(\mathbb{C})$ be a CPTP channel in Kraus form $\mathcal{E}(\rho) = \sum_k A_k \rho A_k^\dagger$ with $\sum_k A_k^\dagger A_k = I_n$. Once input and output orthonormal bases $\{|\gamma\rangle\}$ and $\{|\gamma'\rangle\}$ are declared, reading only the output diagonal induces the population transition kernel:
$$ K(\gamma' \mid \gamma) := \langle\gamma'|\mathcal{E}(|\gamma\rangle\langle\gamma|)|\gamma'\rangle = \sum_k |\langle\gamma'|A_k|\gamma\rangle|^2. $$
Because $\sum_{\gamma'} |\gamma'\rangle\langle\gamma'| = I_m$ and $\sum_k A_k^\dagger A_k = I_n$, the column sums are identically 1:
$$ \sum_{\gamma'} K(\gamma' \mid \gamma) = \sum_k \langle\gamma|A_k^\dagger \Big(\sum_{\gamma'} |\gamma'\rangle\langle\gamma'|\Big) A_k|\gamma\rangle = \langle\gamma|\Big(\sum_k A_k^\dagger A_k\Big)|\gamma\rangle = \langle\gamma|I_n|\gamma\rangle = 1. $$
Thus $K$ is a column-stochastic Markov transition matrix (`QM.StochasticChannel`).

*Scope Fence / The Quantum Lift.* The matrix $K$ records **population transport only**: it does *not* mean the channel preserves diagonality (a CPTP map may generate output coherences even from a diagonal input), and it does *not* determine the full channel $\mathcal{E}$. Complete positivity and coherence transport constitute the licensed non-commutative lift, not implied by the classical kernel.

*Classical $\ell^1$ Contraction Shadow.* On diagonal trace-zero operators $X = \operatorname{diag}(r)$ with $\sum_i r_i = 0$, trace distance reduces to classical total variation: $\frac{1}{2}\|X\|_1 = \frac{1}{2}\|r\|_1$. Any column-stochastic kernel $S$ contracts the classical $\ell^1$ norm:
$$ \|Sx\|_1 = \sum_i \Big|\sum_j S_{ij} x_j\Big| \le \sum_i \sum_j S_{ij} |x_j| = \sum_j \Big(\sum_i S_{ij}\Big) |x_j| = \sum_j |x_j| = \|x\|_1. $$
Mechanized in `QM.stochastic_l1_contraction` over $\mathbb{Q}$. This provides the elementary, division-algebra-free classical shadow of the quantum data-processing inequality.

**2.2 Operational Trace-Distance Selection**

*Theorem (Holevo–Helstrom / Spectral Selection).* Let $j_n$ be a family of norms on Hermitian trace-zero operators satisfying:
1. *Unitary Invariance:* $j_n(U X U^\dagger) = j_n(X)$ for all unitary $U$;
2. *Classical Total-Variation Reduction:* For every diagonal trace-zero operator $X = \operatorname{diag}(r)$ with $\sum_i r_i = 0$, $j_n(X) = \frac{1}{2}\|r\|_1$.

Then $j_n(X) = \frac{1}{2}\|X\|_1$ for every Hermitian trace-zero operator $X$.

*Proof.* For any Hermitian $X$, the spectral theorem yields $X = U \operatorname{diag}(\lambda) U^\dagger$ with real eigenvalues $\lambda = (\lambda_1, \ldots, \lambda_n)$ summing to $\operatorname{Tr}(X) = 0$. By unitary invariance, $j_n(X) = j_n(\operatorname{diag}(\lambda))$. By classical total-variation reduction (the operational Helstrom requirement that maximal distinguishability under equal priors reproduces the total-variation distance on probability distributions), $j_n(\operatorname{diag}(\lambda)) = \frac{1}{2}\|\lambda\|_1$. Since for Hermitian $X$ the Schatten 1-norm equals the $\ell^1$-norm of its eigenvalues, $\|X\|_1 = \|\lambda\|_1$, we have:
$$ j_n(X) = \frac{1}{2}\|\lambda\|_1 = \frac{1}{2}\|X\|_1. \quad \square $$
Trace distance is uniquely selected *conditioned* on operational single-shot binary discrimination, establishing the exact boundary between channel monotonicity (which does not select) and operational measurement advantage (which does select).

**2.3 Global Raw Quantum Defect Load**
Use the conditionally selected trace distance $j_e(\delta_e) := \frac{1}{2} \|\delta_e\|_1$. This gauge is CPTP-compatible: $j_e(\Lambda\delta_e) \le j_e(\delta_e)$ for any CPTP map $\Lambda$.
The global raw quantum defect load is $J_Q(\delta) := \sum_e \frac{1}{2} \|\delta_e\|_1$, representing edge-additive quantum obstruction under the operational trace-distance gauge. Companion work on CPTP-compatible obstruction theory develops the operator-level graph quotient duality ($d_0^*\varphi = 0$, Helstrom effects) in full generality.

**3. Quotient Obstruction**
Let $d_0\alpha$ represent admissible local quantum repair: $(d_0\alpha)_e := r_{b,a}(\alpha_b) - \alpha_a$. The repair cochains $\alpha$ are **not** required to be density states: they live in the declared real vector space of admissible Hermitian perturbations (repair fields). When the comparisons preserve trace, the edge defects and admissible repairs are taken in the traceless Hermitian subspace.
Then $\Phi_Q([\delta]) := \inf_\alpha \sum_e \frac{1}{2} \|\delta_e - (d_0\alpha)_e\|_1$.
With residual $h_e := \delta_e - (d_0\alpha^*)_e$, we have $\Phi_Q = \sum_e \frac{1}{2} \|h_e\|_1$.

**4. Dual Witness Theory**
The dual norm of $\frac{1}{2}\|X\|_1$ on Hermitian operators is $2\|Y\|_\infty$, meaning $\frac{1}{2}\|X\|_1 = \max_{\|\varphi\|_\infty \le 1/2} \text{Tr}(\varphi X)$.
Therefore, $\Phi_Q([\delta]) = \max_\varphi \sum_e \text{Tr}(\varphi_e \delta_e)$
subject to $d_0^*\varphi = 0$, $\|\varphi_e\|_\infty \le 1/2$, and $\varphi_e = \varphi_e^\dagger$.
Here $\varphi_e$ is a bounded Hermitian observable/effect-difference on the edge stalk.
*Primal:* remove quantum-gauge repair. *Dual:* maximize distinguishable residual using bounded admissible observables. *Constraint:* $d_0^*\varphi = 0$ means the probe is gauge-invariant/divergence-free.

**5. Effect-Operator Form**
Trace distance satisfies Helstrom duality: $\frac{1}{2}\|X\|_1 = \max_{0 \le E \le I} \text{Tr}(E X)$ for traceless Hermitian $X$.
For traceless residuals, each dual edge witness may be written as an effect operator $0 \le E_e \le I$ with centered observable $\varphi_e := E_e - \frac{1}{2} I$.
Then $\|\varphi_e\|_\infty \le 1/2$ and $\text{Tr}(\varphi_e h_e) = \text{Tr}(E_e h_e)$ when $\text{Tr}(h_e)=0$. So the quantum dual witness is a divergence-free family of local Helstrom measurement effects.

**6. Quantum Closure Invariant**
If a 2-cell structure exists $d_1 : C^1(P,\mathcal{F}) \to C^2(P,\mathcal{F})$, define:
$\Omega_2^Q([h]) := d_1 h$
$\Gamma_2^Q([h]) := \sum_f \frac{1}{2} \|(d_1 h)_f\|_1$
$R_{cl}^Q := \Gamma_2^Q / \Phi_Q$
Bound: $\Gamma_2^Q \le \|d_1\|_{J_Q^{(1)}\to J_Q^{(2)}} \Phi_Q$ (with $R_{cl}^Q$ defined only when $\Phi_Q>0$).
So the quotient-duality and closure-bound fragment of the $\Phi\Gamma R$ calculus survives under the declared vector or trace-distance gauge.

**7. Minimal Triangle Example** **[PROVEN, NUMERICAL / DIRECT COMPUTATION]**
Let all vertex Hilbert spaces be qubits and restrictions be identity. $V=\{A,B,C\}$, $E=\{(A,B),(B,C),(C,A)\}$.
States: $\rho_A = |0\rangle\langle0|$, $\rho_B = |+\rangle\langle+|$, $\rho_C = |1\rangle\langle1|$.
Edge defects: $\delta_{AB} = \rho_B-\rho_A$, $\delta_{BC} = \rho_C-\rho_B$, $\delta_{CA} = \rho_A-\rho_C$.
Raw quantum defect load: $J_Q = D(\rho_A,\rho_B)+D(\rho_B,\rho_C)+D(\rho_C,\rho_A) = 1/\sqrt{2} + 1/\sqrt{2} + 1 = \sqrt{2} + 1$.
For identity restrictions on a closed cycle, the irreducible circulation is governed by $c := \delta_{AB} + \delta_{BC} + \delta_{CA} = 0$. This particular marginal loop is exact as an edge coboundary: explicitly, the repair witness $\alpha_A = \rho_A - I/2, \alpha_B = \rho_B - I/2, \alpha_C = \rho_C - I/2$ satisfies $d_0\alpha = (\rho_B-\rho_A, \rho_C-\rho_B, \rho_A-\rho_C) = \delta$, proving $\Phi_Q = 0$ directly in the traceless repair space.

*Positive Quotient Obstruction:* To get positive quotient obstruction, use a non-telescoping operator-valued edge signal.
Example: $\omega_{AB} = \omega_{BC} = \omega_{CA} = |0\rangle\langle0| - \frac{I}{2}$.
Then $c = 3(|0\rangle\langle0| - \frac{I}{2}) \ne 0$ and $\Phi_Q > 0$.
For a single cycle with uniform operator circulation, $\Phi_Q = \frac{1}{2}\|c\|_1$.
Here $|0\rangle\langle0| - \frac{I}{2} = \text{diag}(1/2, -1/2)$ has trace norm $1$, so $c = \text{diag}(3/2, -3/2)$ gives $\|c\|_1=3 \implies \Phi_Q = 3/2$.

**8. Dual Witness for the Positive Case**
Let $A = \text{diag}(1/2, -1/2)$. $\omega_e = A$ for all edges. $c = 3A$.
Optimal edge dual witness: $\varphi_e = \frac{1}{2}\text{sign}(A) = \frac{1}{2}\text{diag}(1, -1)$.
Then $\|\varphi_e\|_\infty = 1/2$, and it is divergence-free on the directed cycle (same flows everywhere).
Dual value: $\sum_e \text{Tr}(\varphi_e \omega_e) = 3 \cdot \text{Tr}( (\frac{1}{2}\text{diag}(1,-1))\text{diag}(1/2,-1/2) ) = 3 \cdot 1/2 = 3/2 = \Phi_Q$.
The dual witness attains the quotient obstruction exactly in this finite example.

### Technical Appendix: Proofs

> **[PROVEN — finite-dimensional Fenchel duality] Theorem — Quantum Trace-Norm Obstruction Duality**
> Let $P$ be a finite directed graph with Hermitian trace-class edge defects. Define $\Phi_Q([\delta]) = \inf_\alpha \sum_e \frac{1}{2} \|\delta_e - (d_0\alpha)_e\|_1$.
> Then $\Phi_Q([\delta]) = \max_\varphi \sum_e \text{Tr}(\varphi_e \delta_e)$ subject to $d_0^*\varphi = 0$, $\varphi_e = \varphi_e^\dagger$, and $\|\varphi_e\|_\infty \le 1/2$. Thus quantum dual witnesses are bounded divergence-free observable fields. For traceless residuals, the witnesses are equivalently centered Helstrom effects.
> *(Lean: quantum trace-norm obstruction duality, Helstrom POVM decision observables, subgradient alignment, and strong minimax identity in `quantum_trace_duality.lean` [`helstromStalkObservable_specNorm_le`, `helstromStalkObservable_inner_eq`, `helstrom_slack_nonneg`, `canonicalHelstromCochain_bounded`, `canonicalHelstromCochain_pairing_eq`, `dualPairing_Q_sub`, `dualPairing_Q_repair_invariance`, `weak_quantum_duality_pointwise`, `weak_quantum_duality_quotient`, `helstrom_attainment`, `quantum_dual_witness_is_maximizer`, `quantum_strong_duality_minimax_identity`, `quantum_complementary_slackness`, `strong_quantum_duality_of_stationary_helstrom`, `single_cycle_qubit_fixture_exact`]; lake build green, axioms `[propext, Classical.choice, Quot.sound]`)*
>
> *Proof.* We apply Fenchel duality on the finite-dimensional space of Hermitian operator cochains.
>
> 1. Let $V_e$ be the space of Hermitian trace-class operators on $H_e$, equipped with the norm $\|\cdot\|_e = \frac{1}{2} \|\cdot\|_1$.
>
> 2. The dual space of Hermitian operators under the trace pairing $\langle \varphi_e, \delta_e \rangle = \text{Tr}(\varphi_e \delta_e)$ is equipped with the dual norm, which is the operator norm (Schatten $\infty$-norm) scaled by the reciprocal factor: $\|\varphi_e\|_{e, *} = 2 \|\varphi_e\|_\infty$.
>
> 3. The conjugate function of the local norm $\|\cdot\|_e$ is the indicator function of the dual unit ball:
>    $$(\|\cdot\|_e)^*(\varphi_e) = \begin{cases} 0 & 2 \|\varphi_e\|_\infty \le 1 \\ +\infty & \text{otherwise} \end{cases} = \begin{cases} 0 & \|\varphi_e\|_\infty \le 1/2 \\ +\infty & \text{otherwise} \end{cases}$$
>
> 4. Min-max duality (strong duality) holds because the optimization is convex over finite-dimensional spaces and the primal problem is bounded. This gives:
>    $$\Phi_Q([\delta]) = \max_{\varphi} \sum_e \text{Tr}(\varphi_e \delta_e)$$
>    subject to the dual constraint $d_0^*\varphi = 0$ (divergence-free) and $\|\varphi_e\|_\infty \le 1/2$. $\square$
>
> **[PROVEN; raw part unconditional, quotient part CONDITIONAL + typed cochain transformation] Theorem — CPTP Monotonicity**
> If $\Lambda_e$ are CPTP maps acting locally on edge defects, then $J_Q(\Lambda\delta) \le J_Q(\delta)$ and hence CPTP coarse-graining cannot increase raw quantum defect load. For quotient monotonicity, require a typed cochain transformation $\Lambda^0:C^0_Q\to C^{0\prime}_Q$ and $\Lambda^1:C^1_Q\to C^{1\prime}_Q$ satisfying $\Lambda^1d_0=d_0'\Lambda^0$. (For closure transport, additionally require $\Lambda^2d_1=d_1'\Lambda^1$.) Then $\Phi'_Q([\Lambda^1\delta]) \le \Phi_Q([\delta])$. Without that cochain-map witness, the correct result is `NoRule` or `TransportLicenseNeeded`.
>
> *Proof.*
>
> 1. For Hermitian trace-zero differences of states, CPTP maps are contractive under the trace norm (Schatten 1-norm): $\|\Lambda_e(X)\|_1 \le \|X\|_1$; equivalently, trace distance between density states is monotone under CPTP maps. This is exactly the domain the carrier uses — edge defects are traceless Hermitian (Model II §1).
>
> 2. By definition, the raw quantum defect load is $J_Q(\delta) = \sum_e \frac{1}{2} \|\delta_e\|_1$. Applying the local contractivity:
>    $$J'_Q(\Lambda^1\delta) = \sum_e \frac{1}{2} \|\Lambda^1_e(\delta_e)\|_1 \le \sum_e \frac{1}{2} \|\delta_e\|_1 = J_Q(\delta).$$
>
> 3. For the quotient obstruction magnitude, $\Phi_Q([\delta]) = \inf_{\alpha} J_Q(\delta - d_0 \alpha)$. Fix any admissible repair $\alpha$. The cochain transformation condition $\Lambda^1 d_0 = d_0' \Lambda^0$ gives $d_0'(\Lambda^0\alpha)=\Lambda^1(d_0\alpha)$. Hence
>    $$\Phi'_Q([\Lambda^1\delta]) \le J'_Q\big(\Lambda^1\delta - d_0'(\Lambda^0\alpha)\big) = J'_Q\big(\Lambda^1(\delta-d_0\alpha)\big) \le J_Q(\delta-d_0\alpha),$$
>    the last inequality by the raw contractivity of steps 1–2. Taking the infimum over admissible $\alpha$ gives $\Phi'_Q([\Lambda^1\delta]) \le \Phi_Q([\delta])$. $\square$
>
> **[PROVEN, CONDITIONAL + declared 2-cell $d_1$ with $d_1d_0=0$] Theorem — Quantum $\Phi\Gamma R$ Signature**
> When $d_1$ exists, let $J_Q^{(1)}$ be the edge trace-distance cochain gauge ($J_Q^{(1)}(\cdot)=\sum_e\tfrac12\|\cdot_e\|_1$) and $J_Q^{(2)}$ the corresponding $C^2$ gauge ($\sum_f\tfrac12\|\cdot_f\|_1$). Then $\Gamma_2^Q([h]) = J_Q^{(2)}(d_1 h)$ and $R_{cl}^Q = \Gamma_2^Q / \Phi_Q$ satisfy $\Gamma_2^Q \le \|d_1\|_{J_Q^{(1)}\to J_Q^{(2)}}\, \Phi_Q$, with $R_{cl}^Q$ defined only when $\Phi_Q([h])>0$. Thus the full $\Phi\Gamma R$ obstruction signature survives in the CPTP-compatible quantum carrier.
>
> *Proof.* Let $\|d_1\|_{J_Q^{(1)}\to J_Q^{(2)}}$ be the operator norm of $d_1$ from the $J_Q^{(1)}$ to the $J_Q^{(2)}$ gauge.
>
> 1. Since $d_1 d_0 = 0$, $d_1(h - d_0 \alpha) = d_1 h$ for any 0-cochain $\alpha$.
> 2. Hence, for any $\alpha$,
>    $$\Gamma_2^Q([h]) = J_Q^{(2)}(d_1 h) = J_Q^{(2)}\big(d_1(h - d_0 \alpha)\big) \le \|d_1\|_{J_Q^{(1)}\to J_Q^{(2)}}\, J_Q^{(1)}(h - d_0 \alpha).$$
> 3. Taking the infimum over $\alpha$ yields $\Gamma_2^Q([h]) \le \|d_1\|_{J_Q^{(1)}\to J_Q^{(2)}}\, \Phi_Q([h])$.
>
> **[PROVEN — abstract finite monotone-functional model] Theorem — Metric Non-Selection Firewall**
> Channel monotonicity under completely positive trace-preserving (CPTP) maps does not uniquely select the trace-distance gauge:
> $$\big(\forall \Lambda \in \mathrm{CPTP},\; j(\Lambda(X)) \le j(X)\big) \;\not\Longrightarrow\; j(X) = \frac{1}{2}\|X\|_1.$$
> *(Lean: `QM.cptp_monotone_not_select`, `QM.cptp_monotone_not_select_traceNorm`, `QM.scale_monotone`)*
>
> *Proof.*
> 1. Let $V$ be a finite-dimensional real vector space of traceless Hermitian operators. Let $\mathcal{T}$ be a declared family of CPTP channel maps $\Lambda: V \to V$. A functional $j: V \to \mathbb{R}_{\ge 0}$ is CPTP-monotone if $j(\Lambda X) \le j(X)$ for all $\Lambda \in \mathcal{T}$ and $X \in V$.
> 2. By linearity of scalar multiplication, for any constant $c > 0$, $(c \cdot j)(\Lambda X) = c \cdot j(\Lambda X) \le c \cdot j(X) = (c \cdot j)(X)$ (`QM.scale_monotone`).
> 3. Given any non-trivial CPTP-monotone functional $j_0$ (such as $j_0(X) = \frac{1}{2}\|X\|_1$), the distinct functional $j_1(X) = 2 j_0(X) = \|X\|_1$ is also CPTP-monotone (`QM.cptp_monotone_not_select`).
> 4. Over $\mathbb{N}$ differences, the halving map $x \mapsto \lfloor x/2 \rfloor$ is non-increasing, demonstrating non-vacuous contraction (`QM.id_cptpMonotone_halving`).
> 5. Furthermore, in the wider matrix landscape, infinitely many contractive distinguishability functionals exist that are not scalar multiples of trace distance, including Petz monotone Riemannian metrics, quantum relative entropies, and fidelity distances. Thus CPTP monotonicity underdetermines the metric. $\square$
>
> **[PROVEN — algebraic & finite classical shadow] Theorem — CPTP Population Shadow & Classical $\ell^1$ Contraction**
> Let $\mathcal{E}: M_n(\mathbb{C}) \to M_m(\mathbb{C})$ be a CPTP channel with Kraus representation $\mathcal{E}(\rho) = \sum_k A_k \rho A_k^\dagger$, $\sum_k A_k^\dagger A_k = I_n$.
> 1. In any declared orthonormal bases $\{|\gamma\rangle\}_{j=1}^n$ and $\{|\gamma'\rangle\}_{i=1}^m$, the output-diagonal readout on pure states induces a column-stochastic Markov kernel $K(\gamma'\mid\gamma) = \sum_k |\langle\gamma'|A_k|\gamma\rangle|^2$, satisfying $\sum_{\gamma'} K(\gamma'\mid\gamma) = 1$ and preserving probability distributions (`QM.StochasticChannel`).
> 2. Any column-stochastic kernel $S \in \mathbb{Q}^{m \times n}$ contracts the classical $\ell^1$ norm: $\|Sx\|_1 \le \|x\|_1$ for all $x \in \mathbb{Q}^n$ (`QM.stochastic_l1_contraction`).
>
> *Proof.*
> 1. Column sum: $\sum_{\gamma'} K(\gamma'\mid\gamma) = \sum_k \langle\gamma|A_k^\dagger \Big(\sum_{\gamma'} |\gamma'\rangle\langle\gamma'|\Big) A_k|\gamma\rangle = \langle\gamma|\Big(\sum_k A_k^\dagger A_k\Big)|\gamma\rangle = \langle\gamma|I_n|\gamma\rangle = 1$.
> 2. Nonnegativity: $K(\gamma'\mid\gamma) \ge 0$ by definition. If $p \ge 0$ with $\sum_\gamma p_\gamma = 1$, $(Kp)_{\gamma'} = \sum_\gamma K(\gamma'\mid\gamma) p_\gamma \ge 0$ and $\sum_{\gamma'} (Kp)_{\gamma'} = \sum_\gamma p_\gamma \sum_{\gamma'} K(\gamma'\mid\gamma) = \sum_\gamma p_\gamma = 1$.
> 3. Classical $\ell^1$ contraction: By the triangle inequality and nonnegativity of $S_{ij}$,
>    $$\|Sx\|_1 = \sum_i \Big|\sum_j S_{ij} x_j\Big| \le \sum_i \sum_j S_{ij} |x_j| = \sum_j \Big(\sum_i S_{ij}\Big) |x_j| = \sum_j |x_j| = \|x\|_1. \quad \square$$
>
> **[PROVEN, CONDITIONAL + unitary invariance & classical total-variation reduction] Theorem — Conditional Trace-Distance Selection**
> Let $j_n: \operatorname{Herm}_0(H_n) \to \mathbb{R}_{\ge 0}$ be a family of norms on finite-dimensional Hermitian trace-zero operators. If:
> 1. $j_n(U X U^\dagger) = j_n(X)$ for all unitary $U$ (unitary invariance);
> 2. $j_n(\operatorname{diag}(r)) = \frac{1}{2}\|r\|_1$ for all diagonal trace-zero $r$ (classical total-variation reduction / Helstrom binary discrimination under equal priors);
>
> then $j_n(X) = \frac{1}{2}\|X\|_1$ for all $X \in \operatorname{Herm}_0(H_n)$.
>
> *Proof.*
> Every Hermitian operator $X$ admits a spectral decomposition $X = U \operatorname{diag}(\lambda) U^\dagger$ with real eigenvalues $\lambda = (\lambda_1, \ldots, \lambda_n)$ satisfying $\sum_i \lambda_i = \operatorname{Tr}(X) = 0$. By unitary invariance, $j_n(X) = j_n(\operatorname{diag}(\lambda))$. By classical total-variation reduction, $j_n(\operatorname{diag}(\lambda)) = \frac{1}{2}\|\lambda\|_1$. For Hermitian $X$, the Schatten 1-norm equals the $\ell^1$-norm of its eigenvalues: $\|X\|_1 = \|\lambda\|_1$. Hence $j_n(X) = \frac{1}{2}\|X\|_1$. $\square$
>
**Bottom line:** Under the trace-distance observer gauge, quantum obstruction is not scalar $\ell^1$: it is replica-extensive $\ell^1$ over independent edges, with trace-distance geometry inside each operator-valued edge stalk — conditionally selected by the operational single-shot binary discrimination axiom, not forced by CPTP channel monotonicity alone. Primal: remove CPTP-compatible gauge repair. Dual: bounded divergence-free observable witnesses. Closure: trace-norm $d_1$ residual. Dynamics: CPTP maps contract raw quantum defect load and contract quotient obstruction magnitude when compatible with repair.

References

- Carroll, J. H. *Primitive Axiomatics of Finite Obstruction Calculus*, Research Notes in Mathematical Physics, 2026.
- Carroll, J. H. *SO(k)-Invariant Gauge Classification and the $\ell^1(E;\ell^2)$ Obstruction Geometry*, Research Notes in Mathematical Physics, 2026.
- Carroll, J. H. *CPTP-Compatible Obstruction Theory: Trace-Norm Geometry and Quantum Dual Witnesses*, Zenodo DOI: 10.5281/zenodo.20550459, 2026.
- Helstrom, C. W. (1976). *Quantum Detection and Estimation Theory*. Academic Press.
- Holevo, A. S. (1973). *Statistical decision theory for quantum systems*. Journal of Multivariate Analysis, 3(4), 337–394.
- Morozova, E. A., & Chentsov, N. N. (1990). *Markov invariant geometry on state manifolds*. Journal of Soviet Mathematics, 56(6), 2648–2669.
- Nielsen, M. A., & Chuang, I. L. (2010). *Quantum Computation and Quantum Information* (10th Anniversary ed.). Cambridge University Press.
- Pérez-García, D., Wolf, M. M., Petz, D., & Ruskai, M. B. (2006). *Contractivity of positive and trace-preserving maps under $L_p$ norms*. Journal of Mathematical Physics, 47, 083506. arXiv:math-ph/0601063.
- Petz, D. (1996). *Monotone metrics on matrix spaces*. Linear Algebra and its Applications, 244, 81–96.
- Rockafellar, R. T. (1970). *Convex Analysis*. Princeton University Press.
- Watrous, J. (2018). *The Theory of Quantum Information*. Cambridge University Press.
- Wilde, M. M. (2013). *Quantum Information Theory*. Cambridge University Press.
