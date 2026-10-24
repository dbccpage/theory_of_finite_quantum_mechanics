Status: AI-drafted, awaiting human review.

# Independent Derivation & Scope Audit: `FSP-DIRAC-KAHLER-SPINFOAM-CLAIM` (`TFQ-1216` / `FSP-DERIV-052`)

AuthorityEffect: None.

## 1. Audited Statement & Governing Obligation

- **Node**: `FSP-DIRAC-KAHLER-SPINFOAM-CLAIM` (`TFQ-1216`, stage `FERMION_SIGN`, source record `FSP-DERIV-052` in `papers/core/fsp/theory_of_finite_fsp.jsonl`).
- **Audited Statement**:
  > Claimed: Dirac-Kaehler fermions on simplicial lattices give 2^(D/2) flavors and EPRL-FK boundary contractions yield nonnegative spin-network weights; the only local content is the count 1+4+6+4+1 = 16 = 4 x 4 in D = 4, and no spinfoam amplitude is evaluated.
- **Governing Obligation**:
  > Evaluate EPRL-FK boundary contractions on a declared finite complex and determine their signs; the taste count is standard and carries no positivity.

---

## 2. Mathematical Derivation of the 4D Dirac-Kähler Bundle and Boundary Contraction Sign Dichotomy

### 2.1 Exterior Algebra Taste Decomposition and Orientifold Grading

In dimension $D = 4$, the graded exterior algebra $\Lambda^*(\mathbb{Q}^4) = \bigoplus_{p=0}^4 \Lambda^p(\mathbb{Q}^4)$ has binomial form-degree dimensions
$$\binom{4}{0} = 1, \quad \binom{4}{1} = 4, \quad \binom{4}{2} = 6, \quad \binom{4}{3} = 4, \quad \binom{4}{4} = 1,$$
with total dimension
$$\sum_{p=0}^4 \binom{4}{p} = 1 + 4 + 6 + 4 + 1 = 16 = 4 \times 2^{4/2}$$
(four $4$-component Dirac spinor tastes) and alternating Euler sum $\sum_{p=0}^4 (-1)^p \binom{4}{p} = 0$.

On $p$-forms, the orientifold involution sign $\omega(p) = (-1)^{p(p-1)/2}$ takes values $(+1, +1, -1, -1, +1)$ for $p = 0, 1, 2, 3, 4$ and satisfies $\omega(p)^2 = 1$ for every $p \in \mathbb{N}$. On the $6$-dimensional $2$-form sector $\Lambda^2(\mathbb{Q}^4)$, Hodge duality splits the space into $3$ self-dual ($+1$) and $3$ anti-self-dual ($-1$) components with zero net chirality trace $3(1) + 3(-1) = 0$. The diagonal single-taste spinor projector $P(t, s) = \delta_{t,0}$ on $\operatorname{Fin} 4 \times \operatorname{Fin} 4$ satisfies $P^2 = P$, $\operatorname{Tr}(P) = 4$, and $\operatorname{Tr}(I - P) = 12$.

### 2.2 Simplicial Coboundary Nilpotence and Curvature Obstruction to Taste Projection

On a finite 4-simplex $\Delta^4$ and on the 2-simplex CDT cluster (`CdtKahlerDiracEvaluator` in `code/python/src/fsp/cdt_kd_doubling_evaluator.py`), the oriented simplicial coboundary maps $d_p : C^p \to C^{p+1}$ satisfy $d_1 d_0 = 0$, $d_2 d_1 = 0$, and $d_3 d_2 = 0$ (and $d_0^T d_1^T = 0$).

On a flat block model where the discrete Dirac-Kähler operator $D_{\text{flat}} = I_2$ acts diagonally across tastes, the commutator with the single-taste projector $P_0 = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$ vanishes:
$$[D_{\text{flat}}, P_0] = D_{\text{flat}} P_0 - P_0 D_{\text{flat}} = 0 \quad (\text{MinimalSpinorRecovered}).$$
When curvature holonomy $c \ne 0$ mixes taste sectors via $D_{\text{curved}}(c) = \begin{pmatrix} 1 & c \\ -c & 1 \end{pmatrix}$, the commutator is non-zero:
$$[D_{\text{curved}}(c), P_0] = \begin{pmatrix} 0 & -c \\ -c & 0 \end{pmatrix}, \qquad \|[D_{\text{curved}}(c), P_0]\|_F^2 = 2c^2 > 0 \quad (\text{KahlerDiracIndexObstruction}).$$
Globally on $S^4 = \partial \Delta^5$ with face vector $(6, 15, 20, 15, 6)$, the Dirac-Kähler index equals the Euler characteristic $\chi(S^4) = 6 - 15 + 20 - 15 + 6 = 2$, whereas four copies of the single-spinor Dirac index $\hat{A}(S^4) = 0$ give $4 \hat{A}(S^4) = 0$, producing an index mismatch $\chi(S^4) - 4 \hat{A}(S^4) = 2 \ne 0$.

### 2.3 Evaluation of Finite Spin-Network Boundary Contractions and Their Signs

For a boundary spin-network state $\psi \in \mathbb{Q}^n$ and a vertex or recoupling kernel $W \in M_n(\mathbb{Q})$, the boundary contraction amplitude is
$$\langle \psi | W | \psi \rangle = \sum_{i,j} \psi_i W_{ij} \psi_j.$$
1. **Mirror-Glued Double-Vertex Contractions Are Nonnegative**: When two 4-simplices are glued with conjugate/transposed real vertex amplitude matrix $V \in M_2(\mathbb{Q})$ so $W_{\text{glued}} = V^T V$, the contraction factors into a sum of squares:
   $$\langle \psi | V^T V | \psi \rangle = \sum_{k=0}^{1} \left(\sum_{i=0}^{1} V_{ki} \psi_i\right)^2 \ge 0.$$
2. **Single-Vertex Spin-1 Racah $6j$ Contractions Are Indefinite**: For the single-vertex spin-$1$ tetrahedral Racah $6j$ recoupling kernel
   $$W_{6j} = \begin{pmatrix} 1/6 & -1/3 \\ -1/3 & 1/6 \end{pmatrix},$$
   whose entries $\left\{\begin{smallmatrix} 1 & 1 & 1 \\ 1 & 1 & 1 \end{smallmatrix}\right\} = \frac{1}{6}$ and $\left\{\begin{smallmatrix} 1 & 1 & 1 \\ 1 & 1 & 2 \end{smallmatrix}\right\}_{\text{off}} = -\frac{1}{3}$ are exact rational $SU(2)$ recoupling coefficients, the symmetric boundary state $\psi_+ = (1, 1)^T$ gives a strictly negative contraction
   $$\langle \psi_+ | W_{6j} | \psi_+ \rangle = \frac{1}{6} - \frac{1}{3} - \frac{1}{3} + \frac{1}{6} = -\frac{1}{3} < 0,$$
   while the antisymmetric boundary state $\psi_- = (1, -1)^T$ gives a strictly positive contraction
   $$\langle \psi_- | W_{6j} | \psi_- \rangle = \frac{1}{6} + \frac{1}{3} + \frac{1}{3} + \frac{1}{6} = 1 > 0.$$
   Thus boundary spin-network contractions are not nonnegative in general unless restricted to mirror-glued norm-squared pairings $W = V^T V$.

---

## 3. Explicit Scope Fences

1. **Taste Count Carries No Positivity (`taste_count_carries_no_positivity_fence`)**:
   The exterior-algebra dimension identity $1+4+6+4+1 = 16 = 4 \times 4$ fixes the vector-space rank of $\Lambda^*(\mathbb{Q}^4)$ only; diagonal $16 \times 16$ fermion operators with an odd number of negative eigenvalues have determinant $-1 < 0$.
2. **EPRL Simplicity Spin Sublattice Restriction (`eprl_simplicity_spin_embedding_sublattice_fence`)**:
   The Euclidean EPRL simplicity relation $j^\pm = \frac{1 \pm \gamma}{2} k$ satisfies $j^+ + j^- = k$ and $j^+ - j^- = \gamma k$, and at Barbero-Immirzi parameter $\gamma = 1/2$ and boundary spin $k = 1$ gives $2 j^+ = 3/2 \notin \mathbb{Z}$, requiring $k$ to lie on the denominator sublattice of $\gamma$.
3. **Berezin Orientation-Reversal Sign (`fermionic_cochain_orientation_reversal_sign_fence`)**:
   Reversing the orientation of an odd number $2m+1$ of oriented simplices multiplies a positive spinfoam weight $w > 0$ by $(-1)^{2m+1} = -1$, yielding $-w < 0$.

---

## 4. Verification Summary

- **Lean 4 Module**: [`lean4/CampaignFspDiracKahlerSpinfoamClaim.lean`](../../../lean4/CampaignFspDiracKahlerSpinfoamClaim.lean) — 10 theorems, 0 `sorry`, standard axioms only, 6/6 semantic mutations killed.
- **Independent Python Check**: [`checks/independent/fsp-dirac-kahler-spinfoam-claim.py`](../../../checks/independent/fsp-dirac-kahler-spinfoam-claim.py) — `checks=16242 exterior_taste=44 coboundary_comm=449 spinfoam_fences=15749 failures=0`.
