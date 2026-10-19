# QM-214 Second Symanzik 2-Forest Polynomial, DFM Momentum Routing, and BPHZ Forest Renormalization: the Finite Map

## 1. Three-Layer Decomposition

- **COMPUTED (exact over $\mathbb{Q}$):**
  - **Part (a) — Second Symanzik 2-Forest Polynomial $\mathcal{F}_G(\alpha; q, m^2)$ and Kirchhoff-Schur Duality:**
    On a connected multigraph $G = (V, E)$ with conserved external vertex momenta $q_v \in \mathbb{Q}^d$ ($\sum_{v \in V} q_v = 0$), rational Schwinger parameters $\alpha_e \in \mathbb{Q}_{>0}$, and squared masses $m_e^2 \in \mathbb{Q}_{\ge 0}$, the massless second Symanzik polynomial sums over all spanning 2-forests $F = (T_1, T_2) \in \mathcal{T}_2(G)$ ($|F| = |V| - 2$, acyclic, partitioning $V = V_1 \sqcup V_2$):
    $$\mathcal{F}_0(\alpha; q) = \sum_{(F, V_1, V_2) \in \mathcal{T}_2(G)} \left(\prod_{e \notin F} \alpha_e\right) \left\|\sum_{v \in V_1} q_v\right\|^2, \qquad \mathcal{F}_G(\alpha; q, m^2) = \mathcal{F}_0(\alpha; q) + \mathcal{U}_G(\alpha) \sum_{e \in E} \alpha_e m_e^2.$$
    Across the 1-loop bubble ($|\mathcal{T}_1|=2, |\mathcal{T}_2|=1$), 1-loop triangle vertex ($|\mathcal{T}_1|=3, |\mathcal{T}_2|=3$), and 2-loop diamond ($|\mathcal{T}_1|=8, |\mathcal{T}_2|=10$) graphs, $\mathcal{F}_0(\alpha; q)$ equals the dual Kirchhoff-Schur complement $\mathcal{U}_G(\alpha) \sum_{\mu=1}^d \tilde{q}_\mu^T \tilde{L}_G^{(0)}(1/\alpha)^{-1} \tilde{q}_\mu$ identically over $\mathbb{Q}$.
  - **Part (b) — DFM Spanning-Tree Momentum Routing and Loop-Intersection Invariance:**
    Choosing a spanning tree $T \in \mathcal{T}_1(G)$ defines a unique tree-supported momentum routing $p_T \in C_1(G; \mathbb{Q}^d)$ satisfying $d_0^T p_T = q$ and $p_T(e) = 0$ on all cotree chords $e \notin T$. Under a spanning-tree change $T_1 \to T_2$ (DFM ambiguity of the second kind), the difference $p_{T_2} - p_{T_1} \in Z_1(G; \mathbb{Q}^d) = \ker d_0^T$ is a pure loop-momentum cycle shift, and completing the square against the $b_1 \times b_1$ loop intersection matrix $M_T(\alpha) = C_T \operatorname{diag}(\alpha) C_T^T$ yields $\det M_T(\alpha) = \mathcal{U}_G(\alpha)$ and
    $$\mathcal{U}_G(\alpha)\!\left(\sum_{e \in E} \alpha_e \|p_T(e)\|^2 - \sum_{\mu=1}^d (C_T R p_{T,\mu})^T M_T(\alpha)^{-1} (C_T R p_{T,\mu})\right) = \mathcal{F}_0(\alpha; q)$$
    identically for every spanning tree $T \in \mathcal{T}_1(G)$.
  - **Part (c) — Zimmermann BPHZ Forest Enumeration and Algebraic UV Boundary-Pole Cancellation:**
    Pairwise compatibility of 1PI divergent subgraphs ($\gamma_1 \subseteq \gamma_2$, $\gamma_2 \subseteq \gamma_1$, or $E(\gamma_1) \cap E(\gamma_2) = \emptyset$) enumerates the 4 Zimmermann forests on the 2-loop nested self-energy graph and 6 non-overlapping forests when two subgraphs share an internal edge. On the 2-loop nested Hepp sector integrand $I_{\mathrm{bare}}(\lambda_1, \lambda_2; z)$, the 4-forest BPHZ subtraction $\mathcal{R}_{G_2} = (1 - T_{G_2}^0)(1 - T_{\gamma_1}^0) I_{\mathrm{bare}}$ cancels both the subdivergence pole at $\lambda_2 \to 0$ and the overall UV pole at $\lambda_1 \to 0$ algebraically over $\mathbb{Q}$, reducing to the regular rational kernel $\frac{z}{1+\lambda_1}\frac{z}{1+\lambda_2}$ with finite boundary value $z^2$ at $(\lambda_1, \lambda_2) = (0, 0)$.
- **COMPLETION:**
  - Certified rational interval quadrature (`BigInterval` over `BigRational`) over the $[0, 1]^L$ Feynman-Hepp parameter cube for the BPHZ-subtracted integrand $\mathcal{R}_G$.
- **RESIDUAL IMPORT:**
  - External renormalization subtraction point $\mu^2$, spacetime dimension $D = 4$ in the superficial divergence degree $\omega(\gamma)$, and physical particle masses $m_e^2$.

## 2. Claim Hygiene Summary

1. **What it supports:**
   - Supports in this finite model over $\mathbb{Q}$ that the second Symanzik 2-forest polynomial $\mathcal{F}_G(\alpha; q, m^2)$, its Kirchhoff-Schur complement dual, the DFM spanning-tree momentum-routing loop completion, and Zimmermann's BPHZ forest UV pole cancellation are exact finite combinatorial and linear-algebraic identities.
2. **What it does not support:**
   - Does not support non-perturbative convergence of the summed perturbative series or derive the external spacetime dimension $D = 4$ or physical mass scale $m_e$ from bare graph topology.
3. **The narrowest defensible claim:**
   - On the 1-loop bubble, 1-loop triangle, and 2-loop diamond multigraphs over $\mathbb{Q}$, the combinatorial 2-forest sum $\mathcal{F}_0(\alpha; q)$, the Kirchhoff-Schur complement $\mathcal{U}_G(\alpha)\tilde{q}^T \tilde{L}_G^{(0)}(1/\alpha)^{-1}\tilde{q}$, and the DFM loop-intersection completion across all 8 spanning trees agree identically, and the 4-forest Zimmermann BPHZ subtraction cancels the $(\lambda_1, \lambda_2) \to (0, 0)$ UV boundary poles of the 2-loop nested sector integrand over $\mathbb{Q}$.
4. **The next test needed:**
   - Couple `QM-214` to `CliffordFamily::dirac` and `U1GraphConnection` in Step 2 (`QM-215`) to check the dressed fermion propagator and the exact $4 \times 4$ matrix Ward-Takahashi identity $q_\mu \Gamma^\mu = S_0^{-1}(p+q) - S_0^{-1}(p)$ ($Z_1 = Z_2$) over $\mathbb{Q}(i)$.
