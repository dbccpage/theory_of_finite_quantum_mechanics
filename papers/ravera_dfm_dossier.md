# The Dressing Field Method on Finite Graphs and Simplicial Complexes: Exact Cohomological Reduction, Gribov-Copy Elimination, and Rational Continuum Enclosures

**Authors:** A.O.
**Version:** v0.2.0
**Date:** October 2026
**Classification:** Mathematical Physics / Gauge Theory / Algebraic Graph Calculus / Discrete Differential Geometry

---

## Abstract

The Dressing Field Method (DFM), developed by François, Attard, Lazzarini, Masson, and Ravera, constructs gauge-invariant composite observables by extracting a field-dependent dressing map $u$ directly from the gauge-covariant degrees of freedom, avoiding the spontaneous symmetry breaking narrative and the global topological obstructions that afflict ad hoc gauge fixing. When translated from smooth principal bundles to finite combinatorial graphs, incidence posets, and simplicial complexes over $\mathbb{Q}$ and $\mathbb{Q}(i)$, the DFM becomes an exact, ghost-free algebraic retraction.

In this monograph we present a self-contained nine-pillar finite-to-continuum realization of the Dressing Field Method, accompanied by local machine-checked formalizations in Lean 4 (`lean4/RaveraDfmFiniteToContinuum.lean`), compiled exact-arithmetic verifiers in Rust (`rust/ravera_dfm_finite_to_continuum.rs`), and standalone rational replay scripts in Python (`code/ravera_dfm_dossier_replay.py`):

1. **Abelian Spanning-Tree Dressing and Symanzik Graph Polynomials (Theorem 3.1):** On any connected graph $G = (V, E)$, a spanning tree $T \subset E$ defines a field-dependent dressing map $u_T(v) = \mathrm{Hol}_T(v_0 \to v)$ that neutralizes all $|V|-1$ tree edges and projects the discrete gauge connection onto $H^1(G) \cong \mathbb{Q}^{b_1(G)}$. Residual ambiguity of the second kind ($T \to T'$) acts by unimodular matrices in $\mathrm{GL}(b_1(G), \mathbb{Z})$, leaving the first Symanzik spanning-tree polynomial $U_G(\alpha)$ invariant.
2. **Non-Abelian Two-Stage Borel Normal-Subgroup Dressing and Artificial vs. Substantial Cohomology (Theorem 3.2):** For the solvable Borel gauge group $B_2(\mathbb{Q}) = N \rtimes T_2(\mathbb{Q})$, sequential dressing first by the unipotent normal subgroup $N$ and then by the residual diagonal torus $T_2(\mathbb{Q})$ factorizes the full non-Abelian tree dressing while preserving the discrete Bianchi identity $D_{A^u} K(A^u) = 0$ on the incidence poset algebra. Vanishing dressed cycle holonomy separates artificial pure-gauge symmetries from substantial physical holonomy.
3. **Spanning-Tree Momentum Routing, Second Symanzik 2-Forest Polynomial $F_G$, and Zimmermann BPHZ Forest Subtraction (Theorem 3.3):** Spanning-tree dressing routes external vertex momenta $q_v$ uniquely along tree edges $T$, decoupling the $b_1(G)$ independent loop momenta and reproducing the second Symanzik spanning 2-forest polynomial $F_G(\alpha; q, m^2)$ identically across all spanning trees. Combined with Zimmermann's forest formula, nested and overlapping ultraviolet boundary poles cancel algebraically inside the rational integrand prior to integration.
4. **Dressed Dirac Fermion Propagators and the Exact Clifford Ward–Takahashi Identity $Z_1 = Z_2$ (Theorem 3.4):** Pairing lattice spinors $\psi_v$ with their spanning-tree holonomy tails $\psi_v^{(T)} = u_T(v)^{-1}\psi_v$ yields strictly gauge-invariant two-point correlators across all spanning trees. In the exact Gaussian-rational Clifford algebra $\mathrm{Cl}_{1,3}(\mathbb{Q}(i))$, the discrete Ward–Takahashi identity $(\not{p}+\not{q}-m) - (\not{p}-m) = \not{q}$ forces equality of the 1-loop vertex and wave-function ultraviolet counterterms ($Z_1 / Z_2 = 1$).
5. **Relational Page–Wootters Clock Dressing on Static History Kernels (Theorem 3.5):** Treating the discrete time-reparameterization shift on a periodic clock space $\mathcal{H}_C \otimes \mathcal{H}_S$ as a relational gauge symmetry, the conditional clock-dressing unitary $D = \sum_t |t\rangle\langle t| \otimes U_S^t$ intertwines the static Wheeler–DeWitt history operator ($D^\dagger W D = S_C \otimes I_S$), so unitary step evolution emerges as a gauge-invariant relational observable on $\ker(I - W)$.
6. **Electroweak $SU(2)_L \times U(1)_Y \to U(1)_{\mathrm{EM}}$ Doublet Dressing and Rational Weinberg Projectors (Theorem 3.6):** Extracting the $SU(2)_L$ dressing matrix $u(\Phi) \in SU(2)$ algebraically from the scalar doublet $\Phi$ reduces $\Phi^u = (0, v)^T$ without invoking spontaneous symmetry breaking, yields orthogonal rational Weinberg projectors ($P_\gamma + P_Z = I_2, P_\gamma P_Z = 0$) and the tree-level custodial identity $\rho_{\mathrm{EW}} = 1$, and links residual $U(1)_{\mathrm{EM}}$ consistency to cubic hypercharge anomaly cancellation at $N_c = 3$.
7. **Complete Bipartite Flavor Graph $K_{N_g,N_g}$ Rephasing Dressing and Jarlskog Cycle Holonomy (Theorem 3.7):** Quark-field phase redefinitions in $U(1)_L^{N_g} \times U(1)_R^{N_g}$ act as vertex coboundaries on the complete bipartite flavor graph $K_{N_g,N_g}$. Spanning-tree dressing eliminates $2N_g - 1$ artificial phases and projects the CKM matrix onto $b_1(K_{N_g,N_g}) = (N_g - 1)^2$ fundamental 4-cycles (Jarlskog plaquettes), explaining why $N_g = 2$ has zero physical CP phases ($J_{\mathrm{CP}} = 0$) whereas $N_g = 3$ carries a non-zero dressed cycle holonomy ($J_{\mathrm{CP}} = 5184/78125$ on an explicit Pythagorean $SU(3, \mathbb{Q}(i))$ witness).
8. **Non-Abelian $SU(3)_c$ Spanning-Tree Dressing Uniqueness vs. Discrete Landau Gauge Gribov Copies (Theorem 3.8):** On a finite lattice graph $G$, the differential Landau gauge condition $\partial^* A^g = 0$ admits $4^{|V|-1}$ anchored Gribov copies generated by the diagonal Klein 4-group $\mathcal{K}_4 = \{I_3, \Omega_1, \Omega_2, \Omega_3\} \subset SU(3, \mathbb{Q})$ ($\Omega_a^2 = I_3, \det \Omega_a = +1$), which flip the Faddeev–Popov Hessian edge weight from $+1$ inside the Gribov horizon to $-1 < 0$ outside the horizon. In contrast, the algebraic spanning-tree dressing projector $\Pi_{\mathrm{dress}}^{(T)}$ collapses all $4^{|V|-1} = 64$ Gribov copies on the diamond graph to a single unique dressed state without Faddeev–Popov ghosts.
9. **Discrete Cartan–Regge Lorentz Frame/Tetrad Dressing Around Simplicial 2-Hinges over $\mathbb{Q}$ (Theorem 3.9):** On a 4-dimensional piecewise-flat simplicial manifold, the local tetrad $e_\sigma \in \mathrm{GL}(4, \mathbb{Q})$ acts as an $SO^+(1,3;\mathbb{Q})$-dressing field. Dressing the internal spin connection $\Omega_{\sigma\sigma'} \in SO^+(1,3;\mathbb{Q})$ produces the Lorentz-invariant, metric-compatible affine transport $\Gamma_{\sigma\sigma'} = e_\sigma^{-1}\Omega_{\sigma\sigma'} e_{\sigma'}$ ($\Gamma_{\sigma\sigma'}^T g_\sigma \Gamma_{\sigma\sigma'} = g_{\sigma'}$ for $g_\sigma = e_\sigma^T \eta e_\sigma$), distinguishes artificial frame rotations from substantial deficit-angle hinge holonomy ($\mathrm{Tr}(H_h^{\mathrm{dress}}) = 16/3 \neq 4$ in 4D, $10/3 \neq 2$ in the boost plane), and satisfies the non-Abelian discrete Bianchi identity $\prod_{f \in \partial c} H_f^{\mathrm{dress}} = I_4$ around every closed 3-cell boundary.

---

## 1. Introduction: Why the Dressing Field Method Needs a Finite Combinatorial Spine

In continuum gauge field theory and general relativity, standard textbook quantization and symmetry reduction rely on three recurring operations that introduce technical or conceptual artifacts:

1. **Differential Gauge Fixing and Gribov Ambiguities:** Imposing a differential gauge condition such as Lorenz/Landau gauge $\partial^\mu A_\mu = 0$ or Coulomb gauge $\nabla \cdot \mathbf{A} = 0$ selects a slice across gauge orbits only locally. Globally, as shown by Gribov (1978) and Singer (1978), multiple gauge-equivalent configurations satisfy the same differential condition (Gribov copies), the Faddeev–Popov determinant changes sign across the Gribov horizon, and artificial Faddeev–Popov ghost fields must be introduced to restore unitarity.
2. **Spontaneous Symmetry Breaking (SSB) Narratives in Gauge Theories:** In the textbook presentation of the electroweak model, gauge-variant fields are assigned non-zero vacuum expectation values $\langle \Phi \rangle \neq 0$, despite Elitzur's theorem (1975) demonstrating that a local gauge symmetry cannot be spontaneously broken in a gauge-invariant non-perturbative formulation.
3. **Divergent Intermediate Continuum Integrals:** Perturbative loop calculations evaluate continuum momentum integrals that diverge in the ultraviolet and infrared, subtracting formal infinities via regularization parameters ($\epsilon = 4 - d$ or ad hoc cutoffs) before taking continuum limits.

The **Dressing Field Method (DFM)** (François 2014, Attard et al. 2018, François 2019, Berghofer et al. 2023, François & Ravera 2024–2025) resolves the second problem at the level of differential geometry by defining a **dressing field** $u: \mathcal{P} \to K \subseteq H$ that transforms covariance-wise as $u^g = g^{-1} u$ under a subgroup $K$ of the structure group $H$. Given a connection 1-form $A$ and matter field $\phi$, the **dressed fields**

$$A^u := u^{-1} A u + u^{-1} du, \qquad \phi^u := \rho(u^{-1})\phi$$

are strictly $K$-invariant composite variables. They are not gauge-fixed coordinates on a slice; rather, they are coordinatizations of the $K$-orbit quotient.

However, on a smooth continuum manifold $\mathcal{M}$, constructing $u$ for a propagating gauge connection typically requires solving a differential equation or evaluating a non-local path-ordered continuum integral (such as the Coulomb radiative dressing tail $u(A) = \exp(\nabla^{-2}\partial^i A_i)$), which re-encounters analytical boundary obstructions and Gribov horizons.

This monograph demonstrates that when the carrier is a **finite combinatorial graph, incidence poset, or simplicial complex** over $\mathbb{Q}$ and $\mathbb{Q}(i)$, the Dressing Field Method becomes **purely algebraic, finite, and constructive**:

- Path-ordered continuum Wilson lines are replaced by finite products along a **spanning tree** $T \subset E$, requiring zero differential equations and zero continuum limits.
- The separation between **artificial** (gauge-redundant) and **substantial** (physically observable) degrees of freedom becomes an exact cohomological decomposition $C^1(G) \cong B^1(G) \oplus H^1(G)$ into $|V|-1$ tree edges and $b_1(G) = |E| - |V| + c(G)$ fundamental cycles.
- Irrational or transcendental continuum period integrals (such as multi-loop QED anomalous magnetic moments, vacuum polarization, and Bloch–Nordsieck soft-photon attenuation) are represented without floating-point approximation as **certified rational interval enclosures** $[q_{\mathrm{lo}}, q_{\mathrm{hi}}] \subset \mathbb{Q}$ constructed from the dressed graph polynomials $U_G(\alpha)$ and $F_G(\alpha; q, m^2)$.

---

## 2. Preliminaries: Discrete Gauge Connections and Spanning-Tree Dressing

Let $G = (V, E)$ be a finite connected directed graph with $|V|$ vertices, $|E|$ directed edges $e = (u, v)$, and first Betti number $b_1(G) = |E| - |V| + 1$. Throughout our canonical benchmarks we use the **diamond graph** $G_{\mathrm{diam}}$ with $|V| = 4$ vertices $\{0, 1, 2, 3\}$, $|E| = 5$ directed edges

$$E(G_{\mathrm{diam}}) = \{e_0=(0,1),\; e_1=(1,3),\; e_2=(0,2),\; e_3=(2,3),\; e_4=(1,2)\},$$

and $b_1(G_{\mathrm{diam}}) = 5 - 4 + 1 = 2$ independent cycles. By Kirchhoff's matrix-tree theorem, $G_{\mathrm{diam}}$ possesses $|\mathcal{T}(G_{\mathrm{diam}})| = 8$ spanning trees and $|\mathcal{T}_2(G_{\mathrm{diam}})| = 10$ spanning 2-forests.

### Definition 2.1 (Discrete Gauge Connection and Gauge Group Action)
Let $H$ be a group (such as $(\mathbb{Q}, +)$, $U(1, \mathbb{Q}(i))$, $B_2(\mathbb{Q})$, $SU(2, \mathbb{Q}(i))$, $SU(3, \mathbb{Q}(i))$, or $SO^+(1,3;\mathbb{Q})$).
1. A **discrete $H$-connection** assigns to each directed edge $e = (u, v) \in E$ a parallel-transport group element $U_e \in H$ (or, in the additive Abelian case, a 1-cochain $A_e \in \mathbb{Q}$).
2. A **local vertex gauge transformation** is a 0-cochain $g: V \to H$ acting on edge links and vertex matter fields $\psi_v$ via

$$U_{(u,v)}^g = g(v)\, U_{(u,v)}\, g(u)^{-1}, \qquad \psi_v^g = \rho(g(v))\,\psi_v.$$

### Definition 2.2 (Spanning-Tree Dressing Field and General Rooted-Tree Factorization)
Fix a root vertex $v_0 \in V$ and a spanning tree $T \subset E$ of $G$. For every vertex $v \in V$, let $\gamma_T(v_0 \to v)$ be the unique simple path in $T$ from $v_0$ to $v$. The **spanning-tree dressing field** $u_T: V \to H$ is defined algebraically by the path-ordered tree holonomy

$$u_T(v) := \mathrm{Hol}_T(v_0 \to v) = \prod_{e \in \gamma_T(v_0 \to v)}^{\longleftarrow} U_e^{\pm 1}.$$

Under any local gauge transformation $g: V \to H$, the tree holonomy transforms as

$$u_T(v)^g = g(v)\, u_T(v)\, g(v_0)^{-1}.$$

Consequently, for every anchored gauge transformation ($g(v_0) = 1_H$), $u_T(v)$ satisfies the defining DFM covariance law $(u_T(v)^{-1})^g = u_T(v)^{-1} g(v)^{-1}$, and the **dressed connection** and **dressed matter field**

$$U_{(u,v)}^{\mathrm{dress},(T)} := u_T(v)^{-1} U_{(u,v)} u_T(u), \qquad \psi_v^{\mathrm{dress},(T)} := \rho(u_T(v)^{-1})\psi_v$$

are strictly invariant under all anchored vertex gauge transformations, satisfy $U_e^{\mathrm{dress},(T)} = 1_H$ on all $|V|-1$ tree edges $e \in T$, and equal the rooted fundamental-cycle holonomies on the $b_1(G) = |E| - |V| + 1$ cotree chords $c \in E \setminus T$, while an unanchored constant shift $g(v_0) \in H$ acts globally by conjugation $U_e^{\mathrm{dress},(T)} \mapsto g(v_0)^{-1} U_e^{\mathrm{dress},(T)} g(v_0)$. This provides a bijection $(u_T|_{V\setminus\{v_0\}},\, U^{\mathrm{dress},(T)}|_{E\setminus T}) \in H^{|V|-1} \times H^{b_1(G)} \cong H^{|E|}$ for any group $H$ (mechanized for non-commuting $2 \times 2$ matrices in `spanning_tree_nonabelian_mat2_factorization` in `lean4/RaveraDfmFiniteToContinuum.lean`).

---

## 3. The Nine Finite-to-Continuum Pillars of the Dressing Field Method

### 3.1 Abelian Spanning-Tree Dressing, First Symanzik Polynomial $U_G(\alpha)$, and $\mathrm{GL}(b_1(G), \mathbb{Z})$ Tree Ambiguity

**Theorem 3.1 (Abelian Tree-Dressing Retraction and Unimodular Tree-Change Invariance).**
*Let $G = (V, E)$ be a finite connected graph with coboundary operator $d_0: C^0(G; \mathbb{Q}) \to C^1(G; \mathbb{Q})$, $(d_0 \lambda)_{(u,v)} = \lambda(v) - \lambda(u)$. For any spanning tree $T \subset E$ rooted at $v_0$, let $u_T[A](v) = \sum_{e \in \gamma_T(v_0 \to v)} \pm A_e$ and $\Pi_{\mathrm{dress}}^{(T)}(A) = A - d_0 u_T[A]$. Then:*
1. *(Idempotent Gauge-Invariant Retraction):* $\Pi_{\mathrm{dress}}^{(T)} \circ \Pi_{\mathrm{dress}}^{(T)} = \Pi_{\mathrm{dress}}^{(T)}$, $\Pi_{\mathrm{dress}}^{(T)}(A + d_0\lambda) = \Pi_{\mathrm{dress}}^{(T)}(A)$, and $\Pi_{\mathrm{dress}}^{(T)}(A)_e = 0$ for all $|V|-1$ tree edges $e \in T$, whereas for each of the $b_1(G)$ cotree chords $c \in E \setminus T$, $\Pi_{\mathrm{dress}}^{(T)}(A)_c = \oint_{\gamma_T(c)} A$ equals the fundamental cycle holonomy.
2. *(Residual Ambiguity of the Second Kind):* *Changing the spanning tree $T \to T'$ shifts the dressing field by a connection-dependent 0-cochain $\xi_{T \to T'}[A] = u_{T'}[A] - u_T[A]$ and transforms the $b_1(G)$-tuple of dressed chord holonomies by an integer matrix $M_{T \to T'} \in \mathrm{GL}(b_1(G), \mathbb{Z})$ with $\det(M_{T \to T'}) = \pm 1$.*
3. *(Symanzik Cycle-Intersection Invariance):* *For any edge Schwinger weights $\alpha \in (\mathbb{Q}_{>0})^{|E|}$, the determinant of the $b_1(G) \times b_1(G)$ cycle-intersection matrix $L_T(\alpha) = C_T \mathrm{diag}(\alpha) C_T^T$ is independent of the choice of spanning tree $T$ and equals the first Symanzik spanning-tree polynomial:*

$$\det L_T(\alpha) = \det\bigl(M_{T \to T'} L_{T'}(\alpha) M_{T \to T'}^T\bigr) = \sum_{T \in \mathcal{T}(G)} \prod_{e \notin T} \alpha_e =: U_G(\alpha).$$

*Verification:* Checked across all 8 spanning trees of $G_{\mathrm{diam}}$ in `code/ravera_dfm_dossier_replay.py` (`verify_pillar1_abelian_tree_dfm_and_symanzik_u`), with $U_{G_{\mathrm{diam}}}(1,\dots,1) = 8$, $U_{G_{\mathrm{diam}}}(2,3,5,7,11) = 247$, and certified rational interval enclosures in $\mathbb{Q}$ bracketing the imported 1-to-4-loop QED electron anomalous magnetic moment series $a_e$ to 12 decimal places.

---

### 3.2 Non-Abelian Two-Stage Borel Normal-Subgroup Dressing and Artificial vs. Substantial Cohomology

In François (2014) and Attard et al. (2018), when a gauge group $H$ contains a normal subgroup $N \triangleleft H$ with quotient $Q_H = H / N$, dressing proceeds sequentially: Stage 1 uses an $N$-valued dressing field $u_N: V \to N$ to eliminate the $N$-symmetry, leaving a residual connection with genuine gauge covariance under $Q_H = H / N$; Stage 2 dresses the residual $Q_H$-symmetry.

**Theorem 3.2 (Two-Stage Borel $B_2(\mathbb{Q}) = N \rtimes T_2(\mathbb{Q})$ Dressing and Cohomological Separation).**
*Let $B_2(\mathbb{Q}) = \left\{\begin{pmatrix} a & b \\ 0 & d \end{pmatrix} : a, d \in \mathbb{Q}^\times,\, b \in \mathbb{Q}\right\}$ be the upper-triangular Borel group, with normal unipotent subgroup $N = \left\{\begin{pmatrix} 1 & x \\ 0 & 1 \end{pmatrix}\right\} \triangleleft B_2(\mathbb{Q})$ and diagonal torus quotient $T_2(\mathbb{Q}) \cong B_2(\mathbb{Q})/N$. For any $B_2(\mathbb{Q})$-connection $U$ on $G_{\mathrm{diam}}$ and spanning tree $T$ with rooted tree holonomy $u_T(v) = \mathrm{Hol}_T(v_0 \to v)$ satisfying $U_e = u_T(v)\,u_T(u)^{-1}$ for $e=(u,v) \in T$:*
1. *(Unique Levi Decomposition of the Tree Dressing):* *The full tree holonomy $u_T(v) = \begin{pmatrix} a_v & b_v \\ 0 & d_v \end{pmatrix} \in B_2(\mathbb{Q})$ factors uniquely as $u_T(v) = u_{N,T}(v)\, t_T(v)$ with unipotent $u_{N,T}(v) = \begin{pmatrix} 1 & b_v/d_v \\ 0 & 1 \end{pmatrix} \in N$ and diagonal $t_T(v) = \mathrm{diag}(a_v, d_v) \in T_2(\mathbb{Q})$.*
2. *(Two-Stage Sequential Reduction):* *Stage-1 dressing by $u_{N,T} \in N$, $U_{(u,v)}^{(1)} := u_{N,T}(v)^{-1} U_{(u,v)} u_{N,T}(u)$, reduces all tree edges $e \in T$ to the diagonal torus $U_e^{(1)} = t_T(v)\,t_T(u)^{-1} \in T_2(\mathbb{Q})$ while leaving the quotient projection $\pi_{B/N}(U_e^{(1)}) = \mathrm{diag}(a_e, d_e) = \pi_{B/N}(U_e)$ untouched on every edge $e \in E$. Subsequent Stage-2 dressing by $t_T \in T_2(\mathbb{Q})$ satisfies $(U^{(1)})^{t_T}_{(u,v)} = t_T(v)^{-1} u_{N,T}(v)^{-1} U_{(u,v)} u_{N,T}(u) t_T(u) = u_T(v)^{-1} U_{(u,v)} u_T(u) = U_{(u,v)}^{u_T}$, neutralizing all tree edges to $I_2$ and reproducing the one-shot dressed connection identically.*
3. *(Artificial vs. Substantial Separation):* *The dressed connection satisfies $U_e^{u_T} = I_2$ on all cotree chords $e \in E \setminus T$ if and only if $U$ is an **artificial** pure-gauge coboundary $U_{(u,v)} = g(v)g(u)^{-1}$. When $U$ has non-identity dressed chord holonomy $U_c^{u_T} \neq I_2$, the connection carries a **substantial** global obstruction in $H^1(G; B_2(\mathbb{Q}))$, and both stages preserve the discrete Bianchi identity around the 2-plaquette prism.*

*Verification:* Two-stage Borel factorization, artificial vs. substantial chord holonomy on $G_{\mathrm{diam}}$, and the discrete Bianchi identity are checked in `code/ravera_dfm_dossier_replay.py` (`verify_pillar2_nonabelian_borel_two_stage_dfm`), and non-Abelian $2\times 2$ spanning-tree/chord reconstruction is mechanized in `lean4/RaveraDfmFiniteToContinuum.lean` (`spanning_tree_nonabelian_mat2_factorization`).

---

### 3.3 Spanning-Tree Momentum Routing, Second Symanzik 2-Forest Polynomial $F_G$, and Zimmermann BPHZ Forest Subtraction

**Theorem 3.3 (Spanning-Tree Momentum Routing and Algebraic BPHZ Forest Pole Cancellation).**
*Let $G = (V, E)$ be a connected graph with external momenta $q_v \in \mathbb{Q}^d$ satisfying overall momentum conservation $\sum_{v \in V} q_v = 0$.*
1. *(Tree Momentum Routing as a DFM Projection):* *For each spanning tree $T \in \mathcal{T}(G)$, removing any tree edge $e \in T$ partitions $V$ into two connected components $V = V_1(T, e) \sqcup V_2(T, e)$. The tree-supported edge flow $p_T(e) = -\sum_{v \in V_1(T,e)} q_v$ for $e \in T$ and $p_T(c) = 0$ for $c \notin T$ is the unique 1-chain supported on $T$ satisfying $(d_0^T p_T)(v) = q_v$ at every vertex. Completing the square over the $b_1(G)$ independent loop momenta yields the second Symanzik 2-forest polynomial independently of $T$:*

$$F_0(\alpha; q) = U_G(\alpha)\Biggl(\sum_{e \in T} \alpha_e \|p_T(e)\|^2 - \sum_{\mu=1}^d r_{T,\mu}^T L_T(\alpha)^{-1} r_{T,\mu}\Biggr) = \sum_{(F, V_1, V_2) \in \mathcal{T}_2(G)} \biggl(\prod_{e \notin F} \alpha_e\biggr)\biggl\|\sum_{v \in V_1} q_v\biggr\|^2.$$

2. *(Algebraic BPHZ Forest Subtraction on Rational Sector Kernels):* *On nested two-parameter UV sector kernels $K_1(z;\lambda_1)K_2(z;\lambda_2)$ with boundary poles $\lambda_1^{-1}\lambda_2^{-1}$, Zimmermann's four-forest sum $\mathcal{R}_G = \sum_{\mathcal{F}} \prod_{\gamma \in \mathcal{F}} (-T^{\omega(\gamma)})$ factors as $(K_1(z) - K_1(0))(K_2(z) - K_2(0))$, cancelling the $1/\lambda_i$ boundary poles identically over $\mathbb{Q}$ prior to integration.*

*Verification:* Checked across all 8 spanning trees and all 10 spanning 2-forests of $G_{\mathrm{diam}}$ in `code/ravera_dfm_dossier_replay.py` (`verify_pillar3_symanzik_two_forest_and_bphz`), with $U_{G_{\mathrm{diam}}} = 247$, $F_0(G_{\mathrm{diam}}) = 31153$, and exact boundary pole cancellation on the rational 2-loop sector model (reaching regular value $9/25$ at $(\lambda_1, \lambda_2) \to (0, 0)$).

---

### 3.4 Dressed Dirac Fermion Propagator Invariance and the Exact Clifford Ward–Takahashi Identity

In QED, bare electron fields $\psi(x)$ are not gauge-invariant; Dirac (1955) and Kulish & Faddeev (1970) showed that physical charged particles must be dressed by their electromagnetic phase cloud.

**Theorem 3.4 (Spanning-Tree Dressed Dirac Propagator and Exact $\mathrm{Cl}_{1,3}(\mathbb{Q}(i))$ Ward–Takahashi Matrix Identity).**
*Let $\gamma^0, \gamma^1, \gamma^2, \gamma^3 \in M_4(\mathbb{Q}(i))$ be the Dirac matrices satisfying $\{\gamma^\mu, \gamma^\nu\} = 2\eta^{\mu\nu} I_4$ with $\eta = \mathrm{diag}(1,-1,-1,-1)$, and let $S_F(p) = (\not{p} - m I_4)^{-1} = (p^2 - m^2)^{-1}(\not{p} + m I_4)$ for $p \in \mathbb{Q}^4, m \in \mathbb{Q}$ with $p^2 \neq m^2$.*
1. *(Dressed Correlator Gauge Invariance):* *Whereas the bare two-point spinor correlator $\bar{\psi}_y \psi_x = \psi_y^\dagger \gamma^0 \psi_x$ changes under local $U(1, \mathbb{Q}(i))$ vertex gauge transformations, the spanning-tree dressed correlator $\overline{\psi_y^{(T)}} \psi_x^{(T)}$ with $\psi_v^{(T)} = u_T(v)^{-1}\psi_v$ is strictly gauge-invariant for every spanning tree $T \in \mathcal{T}(G)$, and changing $T \to T'$ multiplies the correlator by the gauge-invariant fundamental-cycle holonomy factor.*
2. *(Exact Algebraic Ward–Takahashi Propagator Difference):* *In $M_4(\mathbb{Q}(i))$, the exact matrix identity*

$$S_F^{-1}(p+q) - S_F^{-1}(p) = \not{q} \implies S_F(p+q)\,\not{q}\,S_F(p) = S_F(p) - S_F(p+q)$$

*holds identically at all non-singular rational momenta $(p, q) \in (\mathbb{Q}^4)^2$. At the 1-loop integrand level, contracting the bare QED vertex integrand $\mathcal{I}_\Lambda^\mu(p+q, p; k) = \gamma^\nu S_F(p+q-k)\gamma^\mu S_F(p-k)\gamma_\nu$ with $q_\mu$ gives $q_\mu \mathcal{I}_\Lambda^\mu(p+q, p; k) = \mathcal{I}_\Sigma(p; k) - \mathcal{I}_\Sigma(p+q; k)$, which under any gauge-invariant BPHZ subtraction scheme equates the vertex and self-energy counterterms ($Z_1 / Z_2 = 1$).*

*Verification:* Tree-dressed spinor correlator invariance across all 8 diamond trees, the $4 \times 4$ matrix identity $S_F(p+q)\not{q}S_F(p) = S_F(p) - S_F(p+q)$ in $M_4(\mathbb{Q}(i))$, and the $4 \times 4$ Dirac trace contraction identity are checked in `code/ravera_dfm_dossier_replay.py` (`verify_pillar4_dressed_dirac_and_ward_takahashi`).

---

### 3.5 Discrete Relational Page–Wootters Clock Dressing on Static History Kernels

In reparameterization-invariant systems where the total Hamiltonian constraint $H_{\mathrm{total}}|\Psi\rangle\rangle = 0$ freezes external coordinate time, Page & Wootters (1983) proposed that time evolution is a relational correlation between an internal clock $C$ and system $S$. Within the DFM framework, discrete time-shift reparameterization is a gauge symmetry and the clock-conditioned evolution operator is the dressing map.

**Theorem 3.5 (Page–Wootters Relational Clock Dressing Intertwiner).**
*Let $\mathcal{H}_C \otimes \mathcal{H}_S = \mathbb{Q}(i)^N \otimes \mathbb{Q}(i)^d$ carry the cyclic clock shift $S_C = \sum_{t=0}^{N-1} |t+1 \bmod N\rangle\langle t|$ (with adjoint $S_C^\dagger = \sum_{t=0}^{N-1} |t-1 \bmod N\rangle\langle t|$) and a unitary system step $U_S \in U(d, \mathbb{Q}(i))$ satisfying $U_S^N = I_d$. Define the discrete Wheeler–DeWitt history shift $W := S_C \otimes U_S$ (so $(I - W)|\Psi\rangle\rangle = 0 \iff |\psi(t+1 \bmod N)\rangle = U_S |\psi(t)\rangle$) and the relational clock-dressing unitary*

$$D := \sum_{t=0}^{N-1} |t\rangle\langle t| \otimes U_S^t.$$

*Then $D$ satisfies the exact operator intertwining identity*

$$D^\dagger W D = \sum_{t=0}^{N-1} |t+1 \bmod N\rangle\langle t| \otimes \bigl((U_S^{t+1})^\dagger U_S U_S^t\bigr) = S_C \otimes I_S.$$

*Consequently, dressing any static history state $|\Psi\rangle\rangle = \sum_{t=0}^{N-1} |t\rangle \otimes U_S^t |\psi(0)\rangle \in \ker(I - W)$ yields $D^\dagger |\Psi\rangle\rangle = \bigl(\sum_{t=0}^{N-1} |t\rangle\bigr) \otimes |\psi(0)\rangle$, and the relational conditional projection $|\psi(t)\rangle = U_S^t |\psi(0)\rangle$ obeys exact unitary step evolution without any external continuum time parameter.*

*Verification:* Checked in `code/ravera_dfm_dossier_replay.py` (`verify_pillar5_page_wootters_clock_dressing`).

---

### 3.6 Electroweak $SU(2)_L \times U(1)_Y \to U(1)_{\mathrm{EM}}$ Doublet Dressing, Rational Weinberg Projectors, and Anomaly Cancellation

A flagship application of the DFM highlighted by François (2014), Masson & Wallet (2010), and Berghofer et al. (2023) is the **gauge-invariant formulation of the electroweak model without spontaneous symmetry breaking**.

**Theorem 3.6 (Electroweak $SU(2)_L$ Scalar Doublet Dressing and Rational Weinberg Projectors).**
*Let $\Phi = (\phi_1, \phi_2)^T \in \mathbb{Q}(i)^2$ be an $SU(2)_L \times U(1)_Y$ scalar doublet with non-vanishing norm $\Phi^\dagger \Phi = v^2 > 0$ ($v \in \mathbb{Q}_{>0}$). Define the algebraic $SU(2)_L$ dressing matrix*

$$u(\Phi) := \frac{1}{v}\begin{pmatrix} \phi_2^* & \phi_1 \\ -\phi_1^* & \phi_2 \end{pmatrix} \in SU(2, \mathbb{Q}(i)).$$

1. *(Exact $SU(2)_L$ Dressing Reduction):* $u(\Phi)^\dagger u(\Phi) = I_2$, $\det u(\Phi) = 1$, and $u(\Phi)^\dagger \Phi = (0, v)^T$. Under any $g_L \in SU(2)_L$, $u(g_L \Phi) = g_L u(\Phi)$, so the dressed doublet $\Phi^u = u(\Phi)^\dagger \Phi = (0, v)^T$ and the dressed weak gauge bosons $W_\mu^u = u(\Phi)^\dagger W_\mu u(\Phi) + \frac{i}{g} u(\Phi)^\dagger \partial_\mu u(\Phi)$ are strictly $SU(2)_L$-invariant composite fields.
2. *(Residual $U(1)_Y$ Covariance and Rational Weinberg Projectors):* *Under $U(1)_Y$ hypercharge multiplication $\Phi \mapsto e^{i\alpha/2}\Phi$, the conjugate first column of $u(\Phi)$ acquires $e^{-i\alpha/2}$ and the second column acquires $e^{+i\alpha/2}$, so $u(e^{i\alpha/2}\Phi) = u(\Phi)\,\mathrm{diag}(e^{-i\alpha/2}, e^{i\alpha/2})$, and the dressed doublet $\Phi^u = (0, v)^T$ is annihilated by the unbroken electric-charge generator $Q_{\mathrm{EM}} = T_3 + Y I_2 = \mathrm{diag}(1, 0)$ ($Q_{\mathrm{EM}}\Phi^u = (0,0)^T$). For any rational couplings $(g, g') \in \mathbb{Q}_{>0}^2$ with $\cos^2\theta_W = g^2/(g^2+g'^2)$ and $\sin^2\theta_W = g'^2/(g^2+g'^2)$, the neutral-current mass matrix $M_{\mathrm{neutral}}^2 = \frac{v^2}{4}\begin{pmatrix} g^2 & -gg' \\ -gg' & g'^2 \end{pmatrix}$ decomposes into orthogonal rational Weinberg projectors $P_\gamma + P_Z = I_2$, $P_\gamma P_Z = 0$ with $M_\gamma^2 = 0$, $M_Z^2 = (g^2+g'^2)v^2/4$, $M_W^2 = g^2 v^2/4$, and exact custodial ratio*

$$\rho_{\mathrm{EW}} := \frac{M_W^2}{M_Z^2 \cos^2\theta_W} = 1.$$

3. *(Anomaly Cancellation at $N_c = 3$):* *For a Standard Model chiral fermion generation with $N_c$ colors ($Y_Q = 1/6, Y_u = 2/3, Y_d = -1/3, Y_L = -1/2, Y_e = -1$), the four one-generation anomaly traces over $\mathbb{Q}$ are:*
   - $[\mathrm{SU}(3)_c]^2 \mathrm{U}(1)_Y$: $\mathcal{A}_{331}(N_c) = 2 Y_Q - Y_u - Y_d = 0$ *(identically for all $N_c$)*,
   - $[\mathrm{grav}]^2 \mathrm{U}(1)_Y$: $\mathcal{A}_{\mathrm{grav}}(N_c) = N_c(2Y_Q - Y_u - Y_d) + (2Y_L - Y_e) = 0$ *(identically for all $N_c$)*,
   - $[\mathrm{SU}(2)_L]^2 \mathrm{U}(1)_Y$: $\mathcal{A}_{221}(N_c) = N_c Y_Q + Y_L = \frac{1}{6}(N_c - 3)$,
   - $[\mathrm{U}(1)_Y]^3$: $\mathcal{A}_{111}(N_c) = N_c(2Y_Q^3 - Y_u^3 - Y_d^3) + (2Y_L^3 - Y_e^3) = \frac{3}{4}(3 - N_c)$,
   *which jointly vanish over $\mathbb{Q}$ if and only if $N_c = 3$.*

*Verification:* Mechanized in `lean4/RaveraDfmFiniteToContinuum.lean` (`electroweak_su2_dressing_unitary_and_reduces_doublet`, `weinberg_rational_projectors_and_custodial_rho_one`, `sm_anomaly_polynomials_vanish_iff_nc_eq_three`, `sm_anomaly_polynomials_general_nc`) and checked in `code/ravera_dfm_dossier_replay.py` (`verify_pillar6_electroweak_doublet_dfm`).

---

### 3.7 Complete Bipartite Flavor Graph $K_{N_g,N_g}$ Rephasing Dressing and Jarlskog Cycle Holonomy

When the electroweak scalar doublet is dressed via Theorem 3.6, the Yukawa couplings between $N_g$ generations of up-type and down-type quarks induce a unitary Cabibbo–Kobayashi–Maskawa (CKM) mixing matrix $V \in U(N_g)$. Independent phase redefinitions of the left-handed mass eigenstates $u_{L,\alpha} \mapsto e^{i\phi_\alpha^u} u_{L,\alpha}$ and $d_{L,j} \mapsto e^{i\phi_j^d} d_{L,j}$ transform $V$ as

$$V_{\alpha j} \longmapsto e^{i\phi_\alpha^u}\, V_{\alpha j}\, e^{-i\phi_j^d}.$$

Graph-theoretically, this transformation is an exact **Abelian $U(1)$ vertex coboundary** on the **complete bipartite flavor graph** $K_{N_g,N_g}$ with $|V| = 2N_g$ vertices ($N_g$ up-type and $N_g$ down-type) and $|E| = N_g^2$ directed flavor edges $(\alpha, j)$.

**Theorem 3.7 (Bipartite Flavor Graph Rephasing Dressing and Jarlskog 4-Cycle Holonomy).**
*Let $K_{N_g,N_g}$ be the complete bipartite flavor graph for $N_g \ge 1$ quark generations.*
1. *(Spanning-Tree Phase Elimination):* *Every spanning tree $T \subset E(K_{N_g,N_g})$ has $|E(T)| = 2N_g - 1$ edges, corresponding to the $2N_g - 1$ relative vertex phases removed by a spanning-tree rephasing dressing field $u_T: V(K_{N_g,N_g}) \to U(1)$ (while the overall diagonal baryon-number phase $e^{i\phi_0}$ acts trivially on all edges). The number of independent rephasing-invariant fundamental 4-cycles is the first Betti number*

$$b_1(K_{N_g,N_g}) = |E(K_{N_g,N_g})| - |V(K_{N_g,N_g})| + 1 = N_g^2 - 2N_g + 1 = (N_g - 1)^2.$$

2. *(Unitarity Triangle Reduction and Vanishing 2-Generation CP Phase):* *Imposing the $(N_g - 1)(N_g - 2)/2 + (N_g - 1) = (N_g - 1)N_g / 2$ independent off-diagonal unitarity triangle constraints reduces the $(N_g - 1)^2$ cycle phases to $N_{\mathrm{CP}}(N_g) = (N_g - 1)(N_g - 2)/2$ independent CP-violating phases. For $N_g = 2$, $2N_g - 1 = 3$ artificial phases are removed by spanning-tree dressing on $K_{2,2}$, $N_{\mathrm{CP}}(2) = 0$, and the single fundamental 4-cycle has real trace and vanishing Jarlskog invariant $J_{\mathrm{CP}}^{(2)} = \mathrm{Im}(V_{11}V_{22}V_{12}^*V_{21}^*) = 0$.*
3. *(3-Generation Substantial Jarlskog Holonomy):* *For $N_g = 3$, spanning-tree dressing removes $2N_g - 1 = 5$ artificial phases on $K_{3,3}$, leaving $b_1(K_{3,3}) = 4$ fundamental 4-cycles and $N_{\mathrm{CP}}(3) = 1$ physical CP phase. Each elementary 4-cycle plaquette $Q_{\alpha\beta j k}(V) := V_{\alpha j} V_{\beta k} V_{\alpha k}^* V_{\beta j}^*$ is strictly invariant under all $U(1)_L^3 \times U(1)_R^3$ vertex rephasings. On the exact Pythagorean $SU(3, \mathbb{Q}(i))$ CKM witness with $(c_i, s_i) = (3/5, 4/5)$ ($i=1,2,3$) and $\delta = \pi/2$ ($e^{i\delta} = i \in \mathbb{Q}(i)$), all 9 plaquettes satisfy $\mathrm{Im}\,Q_{\alpha\beta j k}(V) = \pm J_{\mathrm{CP}}$ with non-zero substantial CP-violating cycle holonomy*

$$J_{\mathrm{CP}} = c_1 s_1 c_2^2 s_2 c_3 s_3 = \frac{5184}{78125} \neq 0.$$

*Verification:* Mechanized in `lean4/RaveraDfmFiniteToContinuum.lean` (`ckm_bipartite_dfm_parameter_count`, `jarlskog_quartet_rephasing_dressing_invariance`, `two_gen_cabibbo_artificial_cp_phase_zero`, `three_gen_ckm_substantial_jarlskog_witness`), compiled in `rust/ravera_dfm_finite_to_continuum.rs` (`evaluate_ckm_jarlskog_bipartite_dfm_control`), and checked in `code/ravera_dfm_dossier_replay.py` (`verify_pillar7_ckm_jarlskog_bipartite_dfm`).

---

### 3.8 Non-Abelian $SU(3)_c$ Spanning-Tree Dressing Uniqueness vs. Discrete Landau Gauge Gribov Copies

A central physical question in non-Abelian Yang–Mills theory is how the algebraic Dressing Field Method compares against differential gauge fixing ($\partial^\mu A_\mu = 0$) in the presence of **Gribov copies** (Gribov 1978, Singer 1978). On a finite connected lattice graph $G = (V, E)$, we can make this comparison exact over $\mathbb{Q}$ and $\mathbb{Q}(i)$.

Given a lattice $SU(3)$ link configuration $U_e \in SU(3, \mathbb{Q}(i))$, the standard lattice **Landau gauge condition** extremizes the link-trace functional $\mathcal{F}_U[g] = \sum_{e=(u,v) \in E} \mathrm{Re}\,\mathrm{Tr}(U_e^g)$, which imposes the discrete divergence equation

$$(\partial^* A^g)(v) = \sum_{e \ni v} \pm \Bigl(U_e^g - (U_e^g)^\dagger - \frac{1}{3}\mathrm{Tr}\bigl(U_e^g - (U_e^g)^\dagger\bigr)I_3\Bigr) = 0,$$

and restricts to the **first Gribov region** $\Omega_{\mathrm{Gribov}}$ where the Faddeev–Popov Hessian $-\Delta_{\mathrm{FP}}(U^g)$ is positive semi-definite.

**Theorem 3.8 (Non-Abelian $SU(3)_c$ Spanning-Tree Dressing Uniqueness vs. Discrete Landau Gribov Copies).**
*Let $G = (V, E)$ be a finite connected graph with rooted spanning tree $T \subset E$, and let $\mathcal{K}_4 = \{I_3, \Omega_1, \Omega_2, \Omega_3\} \subset SU(3, \mathbb{Q})$ be the diagonal Klein 4-group of involutory matrices*

$$\Omega_1 = \mathrm{diag}(1, -1, -1), \qquad \Omega_2 = \mathrm{diag}(-1, 1, -1), \qquad \Omega_3 = \mathrm{diag}(-1, -1, 1).$$

1. *(Discrete Landau Gribov Multiplicity and Faddeev–Popov Hessian Negative Mode):* *Every $\Omega_a \in \mathcal{K}_4$ satisfies $\Omega_a^T \Omega_a = I_3$, $\det(\Omega_a) = +1$, and $\Omega_a^2 = I_3$. Acting on the trivial vacuum connection $U_e = I_3$ by any anchored vertex map $g: V \to \mathcal{K}_4$ with $g(v_0) = I_3$ yields $4^{|V|-1}$ gauge-equivalent link configurations $U_{(u,v)}^g = g(v)g(u)^{-1} \in \mathcal{K}_4$ (giving $4^3 = 64$ anchored copies—$1$ identity and $63$ non-trivial Gribov copies—on $G_{\mathrm{diam}}$). Because every $\Omega_a$ is real symmetric ($\Omega_a^\dagger = \Omega_a$), every one of the $4^{|V|-1}$ copies satisfies the exact discrete Landau divergence condition $\partial^* A^g = 0$, while on any edge with $U_e^g = \Omega_1 \neq I_3$ the link trace drops from $\mathrm{Tr}(I_3) = +3$ to $\mathrm{Tr}(\Omega_1) = -1 < 0$ and the Faddeev–Popov Hessian quadratic form along the traceless generator $H^{(23)} = E_{23} + E_{32} \in \mathfrak{su}(3)$ flips from $\mathrm{Tr}(I_3 (H^{(23)})^2) = +2 > 0$ (inside the Gribov horizon) to $\mathrm{Tr}(\Omega_1 (H^{(23)})^2) = (-1) + (-1) = -2 < 0$ (outside the Gribov horizon).*
2. *(Ghost-Free Algebraic DFM Uniqueness):* *For any non-Abelian $SU(3, \mathbb{Q}(i))$ connection $U$ on $G$ and fixed rooted spanning tree $T$, the spanning-tree dressing field $u_T[U](v) = \mathrm{Hol}_T(v_0 \to v) \in SU(3, \mathbb{Q}(i))$ satisfies $u_T[U^g](v) = g(v)\,u_T[U](v)$ for every anchored gauge transformation $g: V \to SU(3, \mathbb{Q}(i))$ ($g(v_0) = I_3$). Consequently, the dressed connection $\Pi_{\mathrm{dress}}^{(T)}(U^g)_e = u_T[U^g](v)^{-1} U_e^g u_T[U^g](u) = \Pi_{\mathrm{dress}}^{(T)}(U)_e$ has **unique** representative along the entire anchored gauge orbit, neutralizes all $|V|-1$ tree edges to $I_3$, and collapses all $4^{|V|-1} = 64$ Landau Gribov copies on $G_{\mathrm{diam}}$ to the single dressed configuration $(I_3, \dots, I_3)$ with unit Jacobian and zero Faddeev–Popov ghosts.*

*Verification:* Mechanized in `lean4/RaveraDfmFiniteToContinuum.lean` (`su3_diagonal_klein_four_landau_gribov_copies`, `spanning_tree_dfm_eliminates_gribov_copies`, `spanning_tree_nonabelian_mat2_factorization`), compiled in `rust/ravera_dfm_finite_to_continuum.rs` (`evaluate_su3_spanning_tree_vs_landau_gribov_control`), and checked in `code/ravera_dfm_dossier_replay.py` (`verify_pillar8_su3_spanning_tree_vs_landau_gribov`).

---

### 3.9 Discrete Cartan–Regge Lorentz Frame/Tetrad Dressing Around Simplicial 2-Hinges over $\mathbb{Q}$

In four-dimensional Cartan–Palatini gravity and its relational DFM formulation (François 2014, Attard et al. 2018, François & Ravera 2024–2025), the solder-form / tetrad $e = e_\mu^a dx^\mu$ acts as a **frame-dressing field** for the local Lorentz structure group $SO^+(1, 3)$: dressing the internal Lorentz spin connection $\omega^a{}_b$ by $e$ yields the Lorentz-invariant spacetime metric $g = e^T \eta e$ and the affine Levi-Civita connection $\Gamma = e^{-1}\omega e + e^{-1}de$.

On a 4-dimensional piecewise-flat Regge simplicial complex $\mathcal{K}$, each 4-simplex $\sigma$ carries a flat Minkowski frame $e_\sigma \in \mathrm{GL}(4, \mathbb{Q})$, each shared tetrahedron $\tau = (\sigma, \sigma')$ carries a discrete Lorentz spin transport $\Omega_{\sigma\sigma'} \in SO^+(1, 3; \mathbb{Q})$, and curvature is concentrated on codimension-2 **simplicial 2-hinges** (triangles) $h$.

**Theorem 3.9 (Discrete Cartan–Regge Lorentz Tetrad Dressing and Simplicial Hinge Holonomy over $\mathbb{Q}$).**
*Let $\eta = \mathrm{diag}(1, -1, -1, -1)$ be the 4D Minkowski metric, and for every rational velocity parameter $\beta \in (-1, 1) \cap \mathbb{Q}$ define the exact rational Lorentz boost matrix in $SO^+(1, 3; \mathbb{Q})$:*

$$\Lambda(\beta) := \begin{pmatrix} \frac{1+\beta^2}{1-\beta^2} & \frac{2\beta}{1-\beta^2} & 0 & 0 \\ \frac{2\beta}{1-\beta^2} & \frac{1+\beta^2}{1-\beta^2} & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}, \qquad \Lambda(\beta)^T \eta \Lambda(\beta) = \eta, \qquad \det \Lambda(\beta) = +1.$$

1. *(Rational Boost Group Law and Local Tetrad Metric Invariance):* *For any $\beta_1, \beta_2 \in (-1, 1) \cap \mathbb{Q}$, $\Lambda(\beta_1)\Lambda(\beta_2) = \Lambda\bigl(\frac{\beta_1+\beta_2}{1+\beta_1\beta_2}\bigr)$. Under any local Lorentz frame rotations $L_\sigma \in SO^+(1, 3; \mathbb{Q})$ acting on the simplex tetrads as $e_\sigma \mapsto L_\sigma e_\sigma$ and on the spin connection as $\Omega_{\sigma\sigma'} \mapsto L_\sigma \Omega_{\sigma\sigma'} L_{\sigma'}^{-1}$, the induced simplex metric*

$$g_\sigma := e_\sigma^T \eta e_\sigma$$

*is strictly $SO^+(1, 3; \mathbb{Q})$-invariant: $(L_\sigma e_\sigma)^T \eta (L_\sigma e_\sigma) = e_\sigma^T (L_\sigma^T \eta L_\sigma) e_\sigma = g_\sigma$.*
2. *(Dressed Discrete Affine Transport and Metric Compatibility):* *Dressing the inter-simplex spin transport $\Omega_{\sigma\sigma'} \in SO^+(1, 3; \mathbb{Q})$ by the local invertible tetrads $(e_\sigma, e_{\sigma'}) \in \mathrm{GL}(4,\mathbb{Q})^2$ defines the discrete frame-dressed affine transport (the finite simplicial analogue of $e^{-1}\omega e + e^{-1}de$)*

$$\Gamma_{\sigma\sigma'} := e_\sigma^{-1} \Omega_{\sigma\sigma'} e_{\sigma'} \in \mathrm{GL}(4, \mathbb{Q}),$$

*which is strictly invariant under independent local Lorentz transformations $(L_\sigma, L_{\sigma'}) \in SO^+(1,3;\mathbb{Q})^2$ and satisfies exact discrete metric compatibility:*

$$\Gamma_{\sigma\sigma'}^T\, g_\sigma\, \Gamma_{\sigma\sigma'} = e_{\sigma'}^T \Omega_{\sigma\sigma'}^T (e_\sigma^{-1})^T (e_\sigma^T \eta e_\sigma) e_\sigma^{-1} \Omega_{\sigma\sigma'} e_{\sigma'} = e_{\sigma'}^T (\Omega_{\sigma\sigma'}^T \eta \Omega_{\sigma\sigma'}) e_{\sigma'} = g_{\sigma'}.$$

3. *(Artificial vs. Substantial Hinge Curvature and Discrete Bianchi Identity):* *Around a simplicial 2-hinge $h$ shared cyclically by 4-simplices $(\sigma_0, \sigma_1, \dots, \sigma_{k-1})$, the dressed hinge holonomy $H_h^{\mathrm{dress}} := \Gamma_{\sigma_0\sigma_1}\Gamma_{\sigma_1\sigma_2}\cdots\Gamma_{\sigma_{k-1}\sigma_0} = e_{\sigma_0}^{-1} H_h^{\mathrm{spin}} e_{\sigma_0}$ is strictly invariant under all local Lorentz transformations at every simplex. An **artificial** pure-gauge spin connection $\Omega_{\sigma_i\sigma_{i+1}} = L_{\sigma_i} L_{\sigma_{i+1}}^{-1}$ has $H_h^{\mathrm{dress}} = I_4$ ($\mathrm{Tr}(H_h^{\mathrm{dress}}) = 4$), whereas a **substantial** curved hinge with net boost parameter $\beta_{\mathrm{net}} = 1/2$ has gauge-invariant trace $\mathrm{Tr}(H_h^{\mathrm{dress}}) = 16/3 \neq 4$ ($10/3 \neq 2$ in the 2D boost plane). Around any closed 3-cell boundary composed of hinges $(h_1, h_2, h_3)$ rooted at $\sigma_0$, the dressed holonomies satisfy the exact non-Abelian discrete Bianchi identity $H_{h_1}^{\mathrm{dress}} H_{h_2}^{\mathrm{dress}} H_{h_3}^{\mathrm{dress}} = I_4$.*

*Verification:* Mechanized in `lean4/RaveraDfmFiniteToContinuum.lean` (`lorentz_boost_preserves_minkowski_and_det_one`, `cartan_regge_tetrad_dressed_metric_invariance`, `cartan_regge_hinge_holonomy_and_bianchi_witness`), compiled in `rust/ravera_dfm_finite_to_continuum.rs` (`evaluate_cartan_regge_lorentz_tetrad_dfm_control`), and checked in `code/ravera_dfm_dossier_replay.py` (`verify_pillar9_cartan_regge_lorentz_tetrad_dfm`).

---

## 4. Summary Table of Local Verification Artifacts

Every mathematical result in this dossier is verified by local executable code and formal proofs inside this self-contained package directory:

| Section & Theorem | Mathematical Claim | Local Lean 4 Theorem (`lean4/RaveraDfmFiniteToContinuum.lean`) | Local Rust Verifier (`rust/ravera_dfm_finite_to_continuum.rs`) | Local Python Verifier (`code/ravera_dfm_dossier_replay.py`) |
|---|---|---|---|---|
| **§3.1 (Theorem 3.1)** | Abelian spanning-tree dressing, Symanzik $U_G(\alpha)$, and $\mathrm{GL}(2,\mathbb{Z})$ tree-change unimodularity on $G_{\mathrm{diam}}$ | — | — | `verify_pillar1_abelian_tree_dfm_and_symanzik_u` |
| **§3.2 (Theorem 3.2)** | Two-stage Borel $B_2(\mathbb{Q}) = N \rtimes T_2(\mathbb{Q})$ dressing and artificial vs. substantial cohomology | `spanning_tree_nonabelian_mat2_factorization` | — | `verify_pillar2_nonabelian_borel_two_stage_dfm` |
| **§3.3 (Theorem 3.3)** | Spanning-tree momentum routing $p_T$, second Symanzik 2-forest polynomial $F_G$, and BPHZ forest pole cancellation | — | — | `verify_pillar3_symanzik_two_forest_and_bphz` |
| **§3.4 (Theorem 3.4)** | Dressed Dirac propagator gauge invariance and exact $\mathrm{Cl}_{1,3}(\mathbb{Q}(i))$ Ward–Takahashi matrix identity | — | — | `verify_pillar4_dressed_dirac_and_ward_takahashi` |
| **§3.5 (Theorem 3.5)** | Relational Page–Wootters clock dressing $D^\dagger W D = S_C \otimes I_S$ on static history kernels | — | — | `verify_pillar5_page_wootters_clock_dressing` |
| **§3.6 (Theorem 3.6)** | Electroweak $SU(2)_L \times U(1)_Y \to U(1)_{\mathrm{EM}}$ doublet dressing, Weinberg projectors, $\rho_{\mathrm{EW}} = 1$, and $N_c = 3$ 4-condition anomalies | `electroweak_su2_dressing_unitary_and_reduces_doublet`, `weinberg_rational_projectors_and_custodial_rho_one`, `sm_anomaly_polynomials_vanish_iff_nc_eq_three`, `sm_anomaly_polynomials_general_nc` | — | `verify_pillar6_electroweak_doublet_dfm` |
| **§3.7 (Theorem 3.7)** | Bipartite flavor graph $K_{N_g,N_g}$ CKM rephasing dressing and Jarlskog 4-cycle holonomy ($J_{\mathrm{CP}} = 5184/78125$) | `ckm_bipartite_dfm_parameter_count`, `jarlskog_quartet_rephasing_dressing_invariance`, `two_gen_cabibbo_artificial_cp_phase_zero`, `three_gen_ckm_substantial_jarlskog_witness` | `evaluate_ckm_jarlskog_bipartite_dfm_control` | `verify_pillar7_ckm_jarlskog_bipartite_dfm` |
| **§3.8 (Theorem 3.8)** | Non-Abelian $SU(3)_c$ spanning-tree dressing uniqueness vs. $4^{|V|-1}=64$ discrete Landau Gribov copies and FP Hessian quadratic form $-2 < 0$ | `su3_diagonal_klein_four_landau_gribov_copies`, `spanning_tree_dfm_eliminates_gribov_copies`, `spanning_tree_nonabelian_mat2_factorization` | `evaluate_su3_spanning_tree_vs_landau_gribov_control` | `verify_pillar8_su3_spanning_tree_vs_landau_gribov` |
| **§3.9 (Theorem 3.9)** | Discrete Cartan–Regge Lorentz tetrad dressing $g_\sigma = e_\sigma^T \eta e_\sigma$, $\Gamma_{\sigma\sigma'} = e_\sigma^{-1}\Omega_{\sigma\sigma'} e_{\sigma'}$, and simplicial hinge Bianchi identity | `lorentz_boost_preserves_minkowski_and_det_one`, `cartan_regge_tetrad_dressed_metric_invariance`, `cartan_regge_hinge_holonomy_and_bianchi_witness` | `evaluate_cartan_regge_lorentz_tetrad_dfm_control` | `verify_pillar9_cartan_regge_lorentz_tetrad_dfm` |

---

## 5. Claim-Discipline Scope Statement

1. **What this dossier supports:**
   - Supports the exact algebraic realization of the Dressing Field Method on finite connected graphs, incidence posets, complete bipartite flavor graphs, and 4D Regge simplicial complexes over $\mathbb{Q}$ and $\mathbb{Q}(i)$.
   - Demonstrates in these finite combinatorial settings that spanning-tree dressing eliminates local vertex gauge redundancy without differential gauge-fixing equations or Faddeev–Popov ghosts, collapses the $4^{|V|-1} = 64$ discrete Landau-gauge Klein 4-group Gribov copies on $G_{\mathrm{diam}}$ (where the Faddeev–Popov Hessian quadratic form on $H^{(23)} \in \mathfrak{su}(3)$ flips from $+2$ to $-2 < 0$) to a single unique dressed configuration, reduces the electroweak scalar doublet to $(0, v)^T$ with $\rho_{\mathrm{EW}} = 1$ and four-condition $N_c = 3$ anomaly cancellation, extracts the Jarlskog CP-violating invariant $J_{\mathrm{CP}} = 5184/78125$ as a fundamental 4-cycle holonomy on $K_{3,3}$, and dresses simplicial Lorentz spin connections into metric-compatible discrete affine transports $\Gamma_{\sigma\sigma'} = e_\sigma^{-1}\Omega_{\sigma\sigma'} e_{\sigma'}$ satisfying the discrete Bianchi identity.
2. **What this dossier does not support:**
   - Does not claim a non-perturbative continuum existence proof or mass-gap proof for four-dimensional continuum $SU(3)_c$ Yang–Mills theory, nor a UV-complete quantum theory of continuum four-dimensional gravity.
   - Does not claim that choosing a fixed spanning tree $T$ removes the residual global conjugation action at the root vertex $v_0$ or eliminates the unimodular tree-change ambiguity $M_{T \to T'} \in \mathrm{GL}(b_1(G), \mathbb{Z})$ between distinct spanning trees; rather, it characterizes both explicitly as residual symmetries of the first and second kind.
3. **The narrowest defensible claim:**
   - On finite graphs and simplicial complexes over $\mathbb{Q}$ and $\mathbb{Q}(i)$, the Dressing Field Method provides an exact, ghost-free cohomological retraction that separates artificial vertex coboundaries from substantial cycle/hinge holonomies across Abelian QED, solvable Borel $B_2(\mathbb{Q})$, non-Abelian $SU(3)_c$ lattice connections, electroweak $SU(2)_L \times U(1)_Y$, bipartite $K_{N_g,N_g}$ CKM flavor mixing, Page–Wootters relational clocks, and discrete Cartan–Regge Lorentz tetrads, verified by 16 zero-sorry Lean 4 theorems, compiled Rust unit tests, and standalone Python rational replays.
4. **The next test needed:**
   - Extend the discrete Cartan–Regge tetrad dressing of Section 3.9 to coupled Dirac spinor fields on a 4D simplicial complex by constructing a rational $\mathrm{Spin}^+(1,3;\mathbb{Q}(i))$ spin-frame dressing field that pairs each simplex spinor with its local tetrad while preserving the discrete Dirac action around curved 2-hinges.
