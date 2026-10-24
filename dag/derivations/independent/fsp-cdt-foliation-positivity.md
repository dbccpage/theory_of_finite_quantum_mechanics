# Independent Derivation & Scope Audit: `FSP-CDT-FOLIATION-POSITIVITY` (`TFQ-1215` / `FSP-DERIV-051`)

AuthorityEffect: None.

## 1. Audited Statement & Governing Obligation

- **Node**: `FSP-CDT-FOLIATION-POSITIVITY` (`TFQ-1215`, stage `FERMION_SIGN`, source record `FSP-DERIV-051` in `papers/core/fsp/theory_of_finite_fsp.jsonl`).
- **Audited Statement**:
  > Claimed: a global proper-time foliation in CDT forbids spatial branching, removes Lorentzian cancellations, yields a sign-free positive transfer matrix and a 4D de Sitter universe; the de Sitter phase is numerical literature and the checkout has no transfer-matrix or positivity computation.
- **Governing Obligation**:
  > Positivity in CDT uses a Wick rotation of a declared action; derive it for a declared finite model and keep numerical phase results as external evidence.

---

## 2. Mathematical Derivation of the Finite CDT Transfer Matrix & Positivity Model

### 2.1 Global Proper-Time Foliation and Causal Simplex Classification

Let $(V, \tau)$ be a finite vertex set equipped with a global proper-time slicing $\tau : V \to \mathbb{N}$. Define the single-step causal link relation
$$u \to_1 v \iff \tau(u) + 1 = \tau(v)$$
and the strict causal precedence relation
$$u \prec v \iff \tau(u) < \tau(v).$$
Because $(\mathbb{N}, <)$ is a strict linear order, $\prec$ is irreflexive, asymmetric, and transitive, extends every single-step link $u \to_1 v \implies u \prec v$, and forbids all closed causal $2$-cycles ($u \prec v \land v \prec u$) and $3$-cycles ($u \prec v \land v \prec w \land w \prec u$).

In 4D Causal Dynamical Triangulations (Ambjørn, Jurkiewicz, and Loll), every 4-simplex $\sigma$ spans two adjacent proper-time slices $t$ and $t+1$ with vertex partition $(n_t, n_{t+1}) \in \mathbb{N}^2$ satisfying:
$$n_t + n_{t+1} = 5, \qquad n_t \ge 1, \qquad n_{t+1} \ge 1.$$
The admissible pairs $(n_t, n_{t+1})$ are therefore restricted to the four causal simplex types
$$(n_t, n_{t+1}) \in \{(4,1),\, (3,2),\, (2,3),\, (1,4)\},$$
excluding purely spatial 4-simplices of type $(5,0)$ or $(0,5)$. Within a single slab $[t, t+1]$ composed of $(n_{41}, n_{32}, n_{23}, n_{14})$ causal 4-simplices, each $(4,1)$ simplex intersects slice $t$ in a spatial tetrahedron $(4,0)$ and each $(1,4)$ simplex intersects slice $t+1$ in a spatial tetrahedron $(0,4)$, so the boundary tetrahedral counts are $N_3(\Sigma_t) = n_{41}$ and $N_3(\Sigma_{t+1}) = n_{14}$. Requiring connected spatial slice topology ($c_t = c_{t+1} = 1$) excludes baby-universe spatial branching ($c_{t+1} \ge 2$).

### 2.2 Wick-Rotated Euclidean Action and Reflection-Positive Transfer Matrix

Under the CDT Wick rotation from Lorentzian edge-length parameter $\alpha < 0$ to Euclidean $\alpha > 0$, the Euclidean Regge-CDT action on a finite causal triangulation with $N_0$ vertices, $N_{41}$ simplices of type $(4,1)/(1,4)$, and $N_{32}$ simplices of type $(3,2)/(2,3)$ is linear in the simplex counts:
$$S_E(N_0, N_{41}, N_{32}) = -\kappa_0 N_0 + \Delta (N_{41} + N_{32}) + \kappa_4 (N_{41} + N_{32}).$$
Setting the monomer fugacities $w_0 = e^{\kappa_0} > 0$, $w_{41} = e^{-(\Delta + \kappa_4)} > 0$, and $w_{32} > 0$ over $\mathbb{Q}$, the Wick-rotated configuration weight is
$$W_{\text{CDT}}(N_0, N_{41}, N_{32}) = w_0^{N_0} w_{41}^{N_{41}} w_{32}^{N_{32}} > 0.$$

Decomposing the slab transition $t \to t+1$ across the mid-slice $t + 1/2$ (formed by the spatial tetrahedral cross-sections of the $(3,2)$ and $(2,3)$ simplices) with half-step transition matrix $B \in M_{m \times n}(\mathbb{Q})$ and positive intermediate bulk weights $d_k \ge 0$ ($k \in \{0, \dots, m-1\}$) yields the symmetric slice transfer matrix
$$T_{ij} = (B^T D B)_{ij} = \sum_{k=0}^{m-1} d_k B_{ki} B_{kj}.$$
For every boundary state vector $\psi \in \mathbb{Q}^n$, the quadratic expectation value factors into a weighted sum of squares (reflection positivity):
$$\langle \psi, T \psi \rangle = \sum_{i,j} \psi_i T_{ij} \psi_j = \sum_{k=0}^{m-1} d_k \left(\sum_{i=0}^{n-1} B_{ki} \psi_i\right)^2 \ge 0.$$
On the explicit 2-state finite CDT slice transfer witness with $B_{\text{cdt}} = \begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}$ and $d = (1, 1)$,
$$T_{\text{cdt}} = B_{\text{cdt}}^T B_{\text{cdt}} = \begin{pmatrix} 5 & 3 \\ 3 & 2 \end{pmatrix},$$
which has strictly positive entries, $\operatorname{Tr}(T_{\text{cdt}}) = 7 > 0$, $\det(T_{\text{cdt}}) = 1 > 0$, and strictly positive multi-slice periodic partition functions
$$Z_1 = \operatorname{Tr}(T_{\text{cdt}}) = 7 > 0, \qquad Z_2 = \operatorname{Tr}(T_{\text{cdt}}^2) = 47 > 0, \qquad Z_3 = \operatorname{Tr}(T_{\text{cdt}}^3) = 322 > 0.$$

### 2.3 BQNF Sign-Reversing Involution vs Chiral Frustration Obstruction

In `code/python/src/fsp/cdt_fermion_sign_evaluator.py` (`CdtFermionSignEvaluator`), a signed ensemble $(C, s, w)$ admits pairwise cancellation of its negative sector when a fixed-point-free involution $\Xi : C \to C$ reverses signs ($s(\Xi(c)) = -s(c)$) and preserves weights ($w(\Xi(c)) = w(c)$), giving
$$s(c) w(c) + s(\Xi(c)) w(\Xi(c)) = 0.$$
By contrast, in the 3-configuration frustrated chiral ensemble with weights $(w_0, w_1, w_2) = (2, 3, 5)$ and signs $(s_0, s_1, s_2) = (+1, +1, -1)$, no positive-sector configuration matches the negative-sector weight $w_2 = 5$, obstructing any weight-preserving sign-reversing involution on the negative configuration.

---

## 3. Explicit Scope Fences

1. **Wick Rotation Is Required for Positivity (`lorentzian_vs_euclidean_wick_rotation_fence`)**:
   Proper-time foliation and restriction to causal $(4,1)$ simplices do not by themselves remove Lorentzian phase oscillations: two causally admissible $(4,1)$ configurations with equal weight $w > 0$ and opposite Lorentzian phase factors $+1$ and $-1$ sum to $(+1)w + (-1)w = 0$ before Wick rotation, whereas their Euclidean Wick-rotated sum is $2w > 0$.
2. **Finite-Complex Spectral Dimension Saturation vs 4D de Sitter Literature Import (`finite_complex_stationary_return_probability_saturates_fence`)**:
   The emergence of a macroscopic 4D de Sitter background and spectral dimension $d_s(\tau) \to 4$ at large diffusion times in CDT (Ambjørn, Jurkiewicz, and Loll) is a numerical Monte Carlo result in the infinite-volume limit $N_4 \to \infty$. On any finite connected complex of $N \ge 1$ vertices, the stationary random-walk return probability saturates at $P_\infty = 1/N > 0$ with zero step increment $P_\infty(\tau+1) - P_\infty(\tau) = 0$, corresponding to asymptotic spectral dimension $0 \ne 4$.
3. **Bosonic CDT Transfer Positivity vs Fermion Determinant Sign (`bosonic_cdt_positivity_independent_of_fermion_determinant_sign_fence`)**:
   Strict positivity of the bosonic CDT geometric weight $w_{\text{geom}} > 0$ does not make a coupled fermion-gravity path integral sign-free when the fermionic Grassmann determinant is negative ($\det D < 0$), since $w_{\text{geom}} \cdot \det D < 0$.

---

## 4. Verification Summary

- **Lean 4 Module**: [`lean4/CampaignFspCdtFoliationPositivity.lean`](../../../lean4/CampaignFspCdtFoliationPositivity.lean) — 10 theorems, 0 `sorry`, standard axioms only (`propext`, `Classical.choice`, `Quot.sound`), 6/6 semantic mutations killed.
- **Independent Python Check**: [`checks/independent/fsp-cdt-foliation-positivity.py`](../../../checks/independent/fsp-cdt-foliation-positivity.py) — `checks=52525 foliation=16384 simplex_branching=684 transfer_pos=35351 bqnf_fences=106 failures=0`.
