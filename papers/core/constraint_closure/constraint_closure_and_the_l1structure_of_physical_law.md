# A Constraint-Closure Toy Model for $\ell^1$ Residuals on Finite Complexes

## Linear Cochain Quotients, Exact Strong Duality, and Regge-Calculus Examples - With Quarantined High-Energy Speculations

**Author:** Jeremy H. Carroll
**Date:** 2026-09-10
**Version:** 1.2 Pre-Print
**Publication posture:** As-is continuation of an earlier toy model, written as an exploratory exercise and not as a claim to derive physical law.

---

## Author's Scope Note

This paper is a continuation of the original constraint-closure toy model. The original work was exploratory, but its public framing did not make the toy-model status clear enough. This version is therefore published as-is with the word "toy model" made explicit: it records how far finite $\ell^1$ residuals, quotient norms, dual certificates, and Regge-style examples can be pushed, and it records where the attempted extensions break.

The intended contribution is modest. The Python and Lean artifacts are included as best-effort executable evidence for finite, discrete, linear-algebraic statements and for falsification receipts around overextended high-energy analogies. The paper does not claim that $\ell^1$ methods derive continuous general relativity, the Standard Model gauge group $SU(3) \times SU(2) \times U(1)$, electroweak symmetry breaking, supersymmetry, the fine-structure constant, dark matter, or physical law. It is offered for the author's own mathematical interest and for any reader who may find the finite toy-model machinery, failure modes, or executable receipts useful.

---

## Mechanism Inventory

| Slot | Mathematical Binding | Exact Operational Definition |
| :----------------------- | :--------------------------------------- | :----------------------------------------------------------------------------------------------------------------- |
| **Primitive Differences** | Minimal non-sameness | Non-vanishing difference cochains on finite discrete carriers |
| **Carriers** | Simplicial complexes $K$ | Finite combinatorial cell complexes with canonical orientation |
| **Cochain Spaces** | $C^k(K, \mathbb{R})$ or $C^k(K, \mathbb{Q})$ | Chains and cochains with coboundary operators $d_k = \partial_{k+1}^T$ |
| **Curvature Cochain** | $\omega_R \in C^{D-2}(K)$ | Interior deficits $\varepsilon_h = 2\pi - \sum \theta_h$; boundary turning $\tau_h = \pi - \sum \theta_h$ |
| **$\ell^1$ Cochain Metric** | $\Vert \omega \Vert_1 = \sum_e \lvert \omega_e \rvert$ | Unweighted or area-weighted absolute sum of cochain coefficients |
| **Constraint Residual $\Phi$** | $\Phi_D([\omega]) = \min_{\alpha} \Vert \omega - D \alpha \Vert_1$ | Minimal $\ell^1$ distance on finite linear complex $C^1 / \operatorname{im} d_0$; proposed GR constraint model |
| **Joint Constraint System** | $C^1(K) \oplus C^0(K)$ | Direct-sum system with block coboundary $D_{\mathrm{joint}} = \begin{pmatrix} d_0 \\ 0 \end{pmatrix}$ avoiding Hamiltonian blind spots |
| **Dual Witness $w^*$** | $w^* \in C_1(K), \partial_1 w^* = 0, \Vert w^* \Vert_\infty \le 1$ | Certified divergence-free 1-cycle attaining exact LP duality gap |
| **Simplicial Bianchi** | $\sum_{w \sim v} \varepsilon_{vw} \hat{e}_{vw} = 0$, $d_2 \varepsilon = 0$ | Vertex gradient vanishing on stationary backgrounds; scalar coboundary on uniform/abelian models |
| **Ponzano--Regge Bound** | Schläfli path bound & fixed-angle bound | $\lvert \Delta S \rvert \le \Vert J' - J \Vert_1 \sup_t \Vert \theta(t) \Vert_\infty \le \pi \Vert J' - J \Vert_1$; fixed-angle linear functional bound |
| **Quarantine Register** | High Energy Quarantine Register | Five explicit falsification receipts fencing speculative particle physics analogies |
| **Executable Receipts** | Finite run and proof-script evidence | Receipts certify scoped finite computations and formal checks, not truth of continuous physics |

---

## 0. Why this toy-model continuation exists

In early developmental iterations of this repository, exploratory investigations attempted to traverse a speculative climb from primitive differences through Standard Model gauge groups ($SU(3) \times SU(2) \times U(1)$), an electroweak Higgs potential ($v = 246$ GeV), a fine-structure constant ($\alpha^{-1} \approx 137.036$), a supersymmetry threshold ($E_{\mathrm{sat}} \approx 85.6$ TeV), and cosmological dark sector analogies. Rigorous diagnostic evaluations demonstrated that these speculative extrapolations relied upon hand-tuned parameters, divergent lattice sums, or unmotivated category assignments.

Within its finite toy-model scope, this monograph establishes a rigorous linear-algebra layer for **finite linear $\ell^1$ constraint quotients, strong LP duality, and independently checkable certificates**, with examples from discrete Regge calculus and proposed models of discrete gravitational constraints. The rigor belongs to the finite quotient/certificate statements and explicit counterexamples; the physical interpretation remains illustrative and conditional.

### What is mathematically established

1. **Simplicial Geometry & Cochain Nilpotency:** Exact boundary and coboundary operators on finite simplicial complexes in 2D, 3D, and 4D, with verified nilpotency $\partial^2 = 0$ and $d^2 = 0$ (Theorem 1.1).
2. **Finite $\ell^1$ Quotient Invariance and Strong LP Duality:** For any finite linear coboundary matrix $D$, the quotient norm $\Phi_D([\omega]) = \min_\alpha \|\omega - D\alpha\|_1$ is invariant under gauge shifts (Theorem 4.1), satisfies $0 \le \Phi_D([\omega]) \le \|\omega\|_1$, and attains exact strong duality with zero duality gap against a bounded divergence-free dual circulation witness (Theorem 5.1).
3. **Independently Checkable Dual Certificates:** When $\Phi_D([\omega]) > 0$, an auditor can check $D^T w^* = 0$, $\|w^*\|_\infty \le 1$, and $\langle w^*, \omega \rangle = \Phi_D([\omega])$ by direct arithmetic without trusting an external optimizer (Theorem 5.2).
4. **Ponzano--Regge Semiclassical Bounds:** The discrete Regge action phase satisfies a fixed-angle linear functional bound and a geometric Schläfli path bound $|S(J') - S(J)| \le \|J' - J\|_1 \sup_{t} \|\theta(J(t))\|_\infty \le \pi \|J' - J\|_1$ along nondegenerate deformation trajectories (Theorem 6.1).
5. **Direct-Sum Joint Constraint Formulation:** Formulating joint momentum and scalar constraint diagnostics in $C^1 \oplus C^0$ with block operator $D_{\mathrm{joint}} = \begin{pmatrix} d_0 \\ 0 \end{pmatrix}$ strictly preserves scalar Hamiltonian violations ($\Phi_{\mathrm{joint}} = \Phi_{d_0}(p) + \|H_\perp\|_1$), eliminating the blind spot of naive coboundary encodings.
6. **Complete Quarantine of High-Energy Speculations:** Five formal falsification receipts documenting why the speculative high-energy claims are non-sequiturs, category errors, or dimensional inconsistencies within this framework.

### What is scoped or illustrative

- **3D Contracted Bianchi Gradient:** The vanishing of the vertex action gradient $-\sum \varepsilon_e \hat{e} = 0$ is established for interior vertices in stationary or flat-background regimes where vertex variation corresponds to an exact diffeomorphism gauge symmetry (Theorem 3.1).
- **4D Simplicial Bianchi Identity:** The scalar deficit cochain satisfies $d_2 \varepsilon = 0$ on uniform/symmetric complexes (such as regular boundaries where deficits are equal and cancel by alternating signs) and in abelian gauge models ($F = dA$). On generic curved 4-manifolds, the exact Regge Bianchi identity is non-abelian ($\prod U_t = \mathbb{I}$ in $SO(4)$) and does not reduce to scalar cochain coboundary vanishing ($d_2 \varepsilon \ne 0$, Theorem 3.2).
- **Implemented Gravitational Quantities:** In the computational implementation, momentum constraints return edge momenta directly, and Hamiltonian constraints evaluate an unweighted sum of momentum squares minus discrete Ricci scalar curvature with unit dual cell volume. These are chosen toy quantities demonstrating linear algebraic quotient mechanics, rather than an asserted full continuous gravitational correspondence.

### What is a proposed physical application (and explicitly not derived)

- **Continuous Wheeler--DeWitt Constraint Closure:** The physical correspondence mapping continuous 3+1 ADM phase-space variables $(q_{ab}, \pi^{ab})$ and the DeWitt supermetric $G_{ee'}$ to the edge cochain $\omega$, and deriving the coboundary action $\omega \mapsto \omega - d_0 \alpha$ from spatial diffeomorphisms, is a proposed discrete model rather than an established derivation. Minimizing $\Phi_D(\omega)$ evaluates linear gauge-orthogonality; it does not compute Poisson brackets of constraints, verify constraint algebra closure, or construct a quantum Wheeler--DeWitt operator.
- **Topological Cohomology vs Cochain Quotient:** For general cochains $\omega \in C^1$, the quotient space is $C^1 / \operatorname{im} d_0$. It represents cohomology $H^1 = \ker(d_1) / \operatorname{im}(d_0)$ only when $\omega$ is a cocycle ($d_1 \omega = 0$).

### What is explicitly not claimed

- That physical spacetime is a discrete lattice.
- That the scalar identity $d_2 \varepsilon = 0$ holds on arbitrary curved 4D simplicial manifolds.
- That the naive encoding $\omega = p + d_0 H_\perp$ detects Hamiltonian constraint violations.
- That phase stability alone guarantees path-integral amplitude stability (volume prefactors and degeneracies remain uncontrolled).
- That the Standard Model gauge group, Higgs VEV, or Yukawa couplings are derived from simplicial boundaries.
- That supersymmetry exists at 85.6 TeV or any other scale.
- That cold dark matter consists of isolated cochain edges.
- That the fine-structure constant $\alpha$ is determined by hexagonal Regge lattices.

---

## 1. Foundational Geometry: Simplicial Complexes and $\ell^1$ Cochains

### 1.1 Simplicial Complexes and Cayley--Menger Geometry

Let $K$ be a finite simplicial complex of dimension $D$. A $k$-simplex $\sigma^k \in K^{(k)}$ is determined by an ordered set of $k+1$ vertices $(v_0, v_1, \dots, v_k)$. The geometry of each simplex is specified by the matrix of squared edge lengths $s_{ij} = \ell(v_i, v_j)^2 = s_{ji} \ge 0$.

**Definition 1.1 (Cayley--Menger Determinant).**
For a $d$-simplex $\sigma^d$, the Cayley--Menger matrix $CM(\sigma^d) \in \mathbb{R}^{(d+2) \times (d+2)}$ is defined by:
$$
CM(\sigma^d) = \begin{pmatrix}
0 & 1 & 1 & \dots & 1 \\
1 & 0 & s_{01} & \dots & s_{0d} \\
1 & s_{10} & 0 & \dots & s_{1d} \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
1 & s_{d0} & s_{d1} & \dots & 0
\end{pmatrix}
$$
The $d$-dimensional volume $V(\sigma^d)$ satisfies:
$$
V^2(\sigma^d) = \frac{(-1)^{d+1}}{2^d (d!)^2} \det CM(\sigma^d)
$$

A configuration of edge lengths is geometrically realizable in Euclidean space $\mathbb{R}^d$ if and only if $V^2(\tau) > 0$ for all sub-simplices $\tau \subseteq \sigma^d$.

### 1.2 Boundary and Coboundary Operators

Let $C_k(K, \mathbb{R})$ denote the vector space of formal real linear combinations of oriented $k$-simplices, and let $C^k(K, \mathbb{R}) = \mathrm{Hom}(C_k, \mathbb{R})$ denote the dual space of $k$-cochains.

The boundary operator $\partial_k: C_k \to C_{k-1}$ is defined on basis simplices by:
$$
\partial_k (v_0, v_1, \dots, v_k) = \sum_{i=0}^k (-1)^i (v_0, \dots, \hat{v}_i, \dots, v_k)
$$
The coboundary operator $d_{k-1}: C^{k-1} \to C^k$ is the adjoint of $\partial_k$:
$$
\langle d_{k-1} \omega, c \rangle = \langle \omega, \partial_k c \rangle \quad \forall \omega \in C^{k-1}, c \in C_k
$$
In matrix representation with respect to the canonical ordered bases, $d_{k-1} = \partial_k^T$.

**Theorem 1.1 (Simplicial Operator Nilpotency).**
For every dimension $k \ge 1$:
$$
\partial_{k-1} \circ \partial_k = 0 \quad \text{and} \quad d_k \circ d_{k-1} = 0
$$

*Proof.*
For any simplex $\sigma = (v_0, \dots, v_k)$:
$$
(\partial_{k-1} \circ \partial_k) \sigma = \sum_{i=0}^k (-1)^i \partial_{k-1} (v_0, \dots, \hat{v}_i, \dots, v_k)
$$
Expanding the inner boundary splits into indices $j < i$ and $j > i$:
$$
\sum_{i=0}^k (-1)^i \left[ \sum_{j < i} (-1)^j (v_0, \dots, \hat{v}_j, \dots, \hat{v}_i, \dots, v_k) + \sum_{j > i} (-1)^{j-1} (v_0, \dots, \hat{v}_i, \dots, \hat{v}_j, \dots, v_k) \right]
$$
Relabeling indices shows that each pair of omitted vertices appears exactly twice with opposite signs $(-1)^{i+j}$ and $(-1)^{i+j-1}$, canceling identically to zero. Transposition gives $d_k \circ d_{k-1} = \partial_{k+1}^T \circ \partial_k^T = (\partial_k \circ \partial_{k+1})^T = 0$. $\square$

---

## 2. Discrete Regge Action and Curvature Deficit Cochains

In Regge calculus (Regge 1961), curved Riemannian manifolds are approximated by piece-wise flat simplicial complexes. Curvature is concentrated entirely on codimension-2 simplices, termed **hinges** ($h \in K^{(D-2)}$).
- In $D=2$: hinges are vertices $v$ ($D-2 = 0$).
- In $D=3$: hinges are edges $e$ ($D-2 = 1$).
- In $D=4$: hinges are triangles $t$ ($D-2 = 2$).

### 2.1 Dihedral Angles and Deficit Angles

**Definition 2.1 (Simplex Dihedral Angle).**
Let $\sigma^D$ be a $D$-simplex, and let $h \subset \sigma^D$ be a codimension-2 hinge. The hinge $h$ is shared by exactly two codimension-1 faces (hyperfaces) $f_1, f_2 \subset \sigma^D$. The dihedral angle $\theta(\sigma^D, h)$ is the angle between the inward unit normals $n_1, n_2$ of $f_1$ and $f_2$:
$$
\cos \theta(\sigma^D, h) = - n_1 \cdot n_2
$$
For regular $D$-simplices where all edge lengths are equal:
$$
\theta_{\mathrm{reg}}(D) = \arccos\left(\frac{1}{D}\right)
$$
Specifically:
- $D=2$ (equilateral triangle at vertex): $\arccos(1/2) = \pi/3 \approx 1.047198$ rad.
- $D=3$ (regular tetrahedron along edge): $\arccos(1/3) \approx 1.230959$ rad.
- $D=4$ (regular 4-simplex along triangle): $\arccos(1/4) \approx 1.318116$ rad.

**Definition 2.2 (Regge Deficit and Boundary Turning Angles).**
For an interior hinge $h \in \mathrm{int}(K)$, the **interior deficit angle** $\varepsilon_h$ measures local intrinsic curvature:
$$
\varepsilon_h = 2\pi - \sum_{\sigma^D \supset h} \theta(\sigma^D, h), \quad h \in \mathrm{int}(K)
$$
For a boundary hinge $h \in \partial K$, the **boundary turning angle** $\tau_h$ measures discrete extrinsic boundary turning:
$$
\tau_h = \pi - \sum_{\sigma^D \supset h} \theta(\sigma^D, h), \quad h \in \partial K
$$

### 2.2 The Discrete Regge Action and $\ell^1$ Curvature Metric

The discrete Regge action on a manifold with boundary decomposes into interior and boundary terms, mirroring the Einstein--Hilbert action with Gibbons--Hawking--York boundary term $S = \frac{1}{16\pi G} \left( \int_M R \sqrt{g} \, d^D x + 2 \int_{\partial M} K \sqrt{h} \, d^{D-1} x \right)$:
$$
S_{\mathrm{Regge}} = \sum_{h \in \mathrm{int}(K)} A_h \, \varepsilon_h + \sum_{h \in \partial K} A_h \, \tau_h
$$
where $A_h$ is the volume of the hinge ($A_v = 1$ in 2D, $A_e = \ell_e$ in 3D, and $A_t = \mathrm{Area}(t)$ in 4D).

**Definition 2.3 (Interior Curvature $\ell^1$ Norm).**
Let $\omega_R \in C^{D-2}(\mathrm{int}(K), \mathbb{R})$ be the interior curvature cochain assigning $\varepsilon_h$ to each interior hinge $h \in \mathrm{int}(K)$. The $\ell^1$ norm of interior curvature is:
$$
\|\omega_R\|_{\mathrm{int}, 1} = \sum_{h \in \mathrm{int}(K)} A_h |\varepsilon_h|
$$
The total boundary turning is tracked separately as $\mathcal{T}_{\partial K} = \sum_{h \in \partial K} A_h |\tau_h|$.

**Theorem 2.1 (Local Flatness Invariant).**
A triangulated piecewise-linear manifold complex $K$ is locally flat (locally isometric to Euclidean space $\mathbb{R}^D$ away from the boundary) if and only if the interior curvature norm vanishes:
$$
\|\omega_R\|_{\mathrm{int}, 1} = 0 \quad \Longleftrightarrow \quad \varepsilon_h = 0 \quad \forall h \in \mathrm{int}(K)
$$

*Proof & Scope Clarification:*
If $K$ is locally isometric to $\mathbb{R}^D$, the sum of dihedral angles of simplices meeting around any interior codimension-2 hinge completes a full rotation of $2\pi$ radians around the hinge axis in the transverse 2-plane. Thus $\sum \theta = 2\pi \implies \varepsilon_h = 0$. Conversely, if $\varepsilon_h = 0$ at all interior hinges, parallel transport around any contractible loop of simplices has trivial holonomy ($U = \mathbb{I}$), ensuring local Euclidean metric recovery.

*Separation of Boundary Turning:* Treating boundary hinges as carrying interior curvature leads to contradictions. For example, a single flat equilateral triangle in 2D has no interior hinges. At each of its three boundary vertices, the single triangle provides angle $\theta = \pi/3$, giving boundary turning $\tau_v = \pi - \pi/3 = 2\pi/3$. Summing over the three vertices yields total boundary turning $\sum \tau_v = 3 \times (2\pi/3) = 2\pi$, which is the topological Gauss-Bonnet turning of a closed planar curve ($\int \kappa_g ds = 2\pi$), not local interior curvature.

*Local Flatness vs Global Embedding:* Local Euclidean flatness ($\|\omega_R\|_{\mathrm{int}, 1} = 0$) does not imply global isometric embedding in $\mathbb{R}^D$. For instance, a triangulated flat torus $T^D$ is locally Euclidean and satisfies $\|\omega_R\|_{\mathrm{int}, 1} = 0$ everywhere, but cannot be embedded isometrically in $\mathbb{R}^D$ without metric distortion. $\square$

---

## 3. Simplicial Bianchi Identities in 3D and 4D

In continuum differential geometry, the contracted Bianchi identity $\nabla_\mu G^{\mu\nu} = 0$ ensures diffeomorphism invariance and the conservation of energy-momentum. In discrete Regge calculus, this identity manifests through geometric variations on simplicial complexes, though its exact non-abelian structure requires careful scoping.

### 3.1 3D Contracted Bianchi Identity at Vertices

In 3D simplicial gravity, hinges are edges $e = (v, w)$, and the discrete action is $S = \sum_e \ell_e \varepsilon_e$.

**Theorem 3.1 (3D Contracted Bianchi Identity in Stationary / Flat Backgrounds).**
For any interior vertex $v \in K^{(0)}$ of a 3D simplicial complex in a stationary background configuration, the variation of the discrete Regge action with respect to vertex coordinates $x_v \in \mathbb{R}^3$ satisfies:
$$
\frac{\partial S_{\mathrm{Regge}}}{\partial x_v} = -\sum_{w \sim v} \varepsilon_{vw} \, \hat{e}_{vw} = 0
$$
where $\hat{e}_{vw} = \frac{x_w - x_v}{\|x_w - x_v\|}$ is the unit tangent vector directed along edge $(v, w)$.

*Proof & Physical Scope:*
Under an infinitesimal vertex coordinate shift $x_v \mapsto x_v + \delta x_v$, the variation of the Regge action is:
$$
\delta S = \sum_{e} \left( \delta \ell_e \, \varepsilon_e + \ell_e \, \delta \varepsilon_e \right)
$$
By the Schläfli identity for polyhedra (Regge 1961), the second term vanishes identically: $\sum_e \ell_e \delta \varepsilon_e = 0$.
The variation of the edge length $\ell_{vw} = \|x_w - x_v\|$ with respect to $x_v$ is:
$$
\delta \ell_{vw} = -\hat{e}_{vw} \cdot \delta x_v
$$
Substituting this yields:
$$
\delta S = -\left( \sum_{w \sim v} \varepsilon_{vw} \, \hat{e}_{vw} \right) \cdot \delta x_v \implies \frac{\partial S}{\partial x_v} = -\sum_{w \sim v} \varepsilon_{vw} \, \hat{e}_{vw}
$$
When the triangulation is stationary under coordinate relocations (such as on flat backgrounds where interior vertex displacement is a pure diffeomorphism gauge symmetry), $\delta S / \delta x_v = 0$, forcing $\sum_{w \sim v} \varepsilon_{vw} \hat{e}_{vw} = 0$.

*Limitation on Generic Curved Complexes:* On generic curved 4D or 3D Regge triangulations without stationarity, shifting an interior vertex changes the surrounding geometry and deficit angles; exact vertex gauge invariance is broken at finite lattice spacing and is recovered only in the continuum or on-shell limit (Bahr & Dittrich 2009). $\square$

### 3.2 4D Discrete Bianchi Identity: Holonomy Obstruction and Scoped Regimes

In 4D spacetime, hinges are triangles $t \in K^{(2)}$. In early versions of this monograph, it was asserted that the scalar deficit cochain $\varepsilon \in C^2(K)$ satisfies $d_2 \varepsilon = 0$ universally on all closed triangulated 4-manifolds. That unrestricted claim is false and is formally withdrawn.

**Withdrawal of Unrestricted Scalar Claim:**
In 4D discrete gravity, curvature is fundamentally encoded in parallel transport holonomy matrices $U_t \in SO(4)$ associated with triangular hinges. The exact geometric Bianchi identity around any 3-cell (tetrahedron $\tau^3$) is the non-abelian path-ordered loop product (Hamber & Kagel 2001):
$$
\prod_{t \subset \partial \tau^3} U_t = \mathbb{I} \in SO(4)
$$
Because $SO(4)$ is non-abelian, the logarithm of a product of non-commuting rotation matrices does not equal the sum of their logarithms ($\log \prod U_i \ne \sum \log U_i$). Projecting holonomies onto scalar deficit angles $\varepsilon_t = \theta(U_t)$ discards rotation planes and transport information. Consequently, the linear scalar coboundary $(d_2 \varepsilon)(\tau^3) = \sum_{t \subset \tau^3} (-1)^i \varepsilon_{t_i}$ does not vanish on generic curved complexes.

**Concrete Counterexample on $\partial \Delta^5 \cong S^4$:**
Consider the boundary of a standard 5-simplex $\partial \Delta^5$ with 6 vertices $0, \dots, 5$, 15 edges, 20 triangles, 15 tetrahedra, and 6 4-simplices.
1. Set 14 edge lengths to $\ell_{ij} = 1.0$, and perturb only a single edge $\ell_{01} = 1.1$.
2. Every 4-simplex remains strictly Euclidean and nondegenerate (smallest Gram matrix eigenvalue $\approx 0.4851$).
3. Simplicial operator nilpotency holds identically: $\partial_2 \circ \partial_3 = 0$ and $d_2 \circ d_1 = 0$.
4. Recomputing the dihedral angles of all six 4-simplices and deficit angles of all twenty triangular hinges yields:
$$
\|d_2 \varepsilon\|_1 \approx 1.956565, \quad \|d_2 \varepsilon\|_\infty \approx 0.244571, \quad (d_2 \varepsilon)(0,2,3,4) \approx -0.244571
$$
Thus, even on the paper's own topology, the scalar deficit cochain fails to be closed under $d_2$.

**Theorem 3.2 (Simplicial Bianchi Identity: Scoped Regimes).**
The linear scalar coboundary identity $d_2 \varepsilon = 0$ holds strictly under the following declared conditions:
1. *Uniform and symmetric complexes:* on regular boundary complexes where all deficit angles are identical ($\varepsilon_t = c$), the alternating face sum across every tetrahedron vanishes identically:
   $$
   (d_2 \varepsilon)(\tau^3) = c - c + c - c = 0
   $$
   *(Incidence count correction:* In $\partial \Delta^5$, each triangle belongs to exactly $6 - 3 = 3$ (not 5) 4-simplices. Its regular deficit angle is $\varepsilon_{\mathrm{reg}} = 2\pi - 3\arccos(1/4) \approx 2.328837$ rad, rather than $-0.307395$ rad).*
2. *Discrete abelian gauge models:* for an abelian connection $A \in C^1(K, \mathbb{R})$ with curvature 2-form $F = d_1 A$, the operator nilpotency Theorem 1.1 guarantees $d_2 F = d_2 d_1 A = 0$ identically.
3. *Linearized Regge calculus:* around flat Euclidean space where deficit angles are infinitesimal ($\varepsilon = O(\delta)$), so non-abelian commutator terms $[U_i, U_j] = O(\varepsilon^2)$ are neglected. $\square$

---

## 4. Finite Linear $\ell^1$ Constraint Quotients and Proposed Discrete Gravitational Models

### 4.1 Canonical 3+1 Cauchy Slices and Proposed Constraint Models

In continuous general relativity, the 3+1 ADM formulation describes gravity as a constrained Hamiltonian system on a spatial hypersurface $\Sigma$, governed by spatial diffeomorphism constraints $\mathcal{H}_a$ and the scalar Wheeler--DeWitt Hamiltonian constraint $\mathcal{H}_\perp$.

In a discrete simplicial setting on a 3-complex $\Sigma$, one considers:
1. Spatial metric edge lengths: $q_e = \ell_e > 0$ for $e \in \Sigma^{(1)}$.
2. Conjugate momentum cochain: $\pi \in C^1(\Sigma, \mathbb{R})$, representing discrete extrinsic curvature.

A proposed discrete model assigns constraint violations to edges or vertices:
- **Spatial Momentum Violation:** $\mathcal{H}_a(v) = \sum_{e \supset v} \pi_e \, \hat{e}_a$.
- **Hamiltonian Scalar Violation:** $\mathcal{H}_\perp(v) = \frac{1}{\sqrt{q_v}} \sum_{e, e' \supset v} G_{ee'} \pi_e \pi_{e'} - \sqrt{q_v} R(v)$, where $G_{ee'}$ is a discrete DeWitt supermetric.

*Important Mathematical Scope Note:* The mapping from continuous canonical fields $(q_{ab}, \pi^{ab})$ to a discrete cochain $\omega \in C^1(\Sigma)$, the definition of the discrete supermetric $G_{ee'}$, and the identification of spatial coordinate reparametrizations with coboundaries $\omega \mapsto \omega - d_0 \alpha$ constitute a **proposed discrete model** rather than an established mathematical derivation from continuous Einstein gravity. Minimizing an $\ell^1$ residual $\Phi$ evaluates linear gauge-orthogonality on the discrete complex; it does not compute Poisson brackets of constraints, verify structure functions, or construct a quantum Wheeler--DeWitt operator acting on wave functionals $\Psi[q]$.

### 4.2 Linear Cochain Quotients: $C^1 / \mathrm{im}(d_0)$ vs Cohomology $H^1$

Let $D: C^0(\Sigma) \to C^1(\Sigma)$ be any finite linear coboundary operator (such as the simplicial coboundary $d_0 = \partial_1^T$). Given an arbitrary constraint cochain $\omega \in C^1(\Sigma)$, gauge transformations act as translations by pure coboundaries:
$$
\omega \mapsto \omega - D \alpha, \quad \alpha \in C^0(\Sigma)
$$
The gauge-invariant measure of constraint violation is the quotient norm on the quotient vector space $C^1(\Sigma) / \mathrm{im}(D)$:

**Definition 4.1 ($\ell^1$ Constraint Quotient Norm).**
For any finite linear operator $D: \mathbb{R}^{|V|} \to \mathbb{R}^{|E|}$ and cochain $\omega \in \mathbb{R}^{|E|}$:
$$
\Phi_D([\omega]) = \min_{\alpha \in \mathbb{R}^{|V|}} \|\omega - D \alpha\|_1
$$

*Distinction Between Cochain Quotient and Cohomology:*
For an arbitrary cochain $\omega$, the quotient space is $C^1 / \mathrm{im}(d_0)$. It is **not necessarily cohomology** $H^1 = \ker(d_1) / \mathrm{im}(d_0)$. The quotient class $[\omega]$ belongs to cohomology if and only if $\omega$ is a cocycle ($d_1 \omega = 0$).
For example, on a single filled triangle with edges $(0,1), (1,2), (2,0)$ and face $(0,1,2)$, the circulation cochain $\omega = (1, 1, 1)^T$ satisfies $(d_1 \omega)(0,1,2) = 1 + 1 + 1 = 3 \ne 0$. Thus $\omega$ is not a cocycle and carries no non-trivial class in $H^1$, yet its quotient distance $\Phi([\omega]) = 3$ is strictly positive.

**Theorem 4.1 (Gauge Invariance of $\Phi_D$).**
For any pure gauge vector $\gamma \in \mathbb{R}^{|V|}$:
$$
\Phi_D([\omega + D \gamma]) = \Phi_D([\omega])
$$

*Proof.*
By definition:
$$
\Phi_D([\omega + D \gamma]) = \min_{\alpha} \|\omega + D \gamma - D \alpha\|_1 = \min_{\alpha} \|\omega - D (\alpha - \gamma)\|_1
$$
Substituting $\beta = \alpha - \gamma$ establishes that the set of vectors over which the minimum is taken is identical, hence $\Phi_D([\omega + D \gamma]) = \Phi_D([\omega])$. $\square$

**Definition 4.2 (Exact Linear Constraint Closure).**
A discrete state satisfies **exact constraint closure** if and only if $\Phi_D([\omega]) = 0$. Because $\mathrm{im}(D)$ is a closed subspace in finite dimensions, this condition holds if and only if $\omega \in \mathrm{im}(D)$ (i.e. the violation is entirely removable by gauge choice).

### 4.3 The Hamiltonian Blind Spot and the Joint Direct-Sum System

In early drafts of this discrete constraint model, it was suggested that a total constraint cochain could be assembled by encoding the scalar Hamiltonian violation $H_\perp \in C^0(\Sigma)$ directly into $C^1(\Sigma)$ via the coboundary:
$$
\omega = p + d_0 H_\perp
$$
where $p \in C^1(\Sigma)$ represents spatial momentum violations. However, as identified in peer review (Jeremy H. Carroll, Sept 2026), this encoding suffers from an exact **Hamiltonian blind spot**:
$$
\Phi_{d_0}(p + d_0 H_\perp) = \min_{\alpha \in C^0} \|p + d_0 H_\perp - d_0 \alpha\|_1 = \min_{\alpha' \in C^0} \|p - d_0 \alpha'\|_1 = \Phi_{d_0}(p)
$$
where $\alpha' = \alpha - H_\perp$. Consequently:

1. The quotient distance $\Phi_{d_0}(\omega)$ is mathematically independent of every Hamiltonian cochain $H_\perp$, whether constant or non-constant.
2. For any state with zero spatial momentum ($p = 0$), $\Phi_{d_0}(d_0 H_\perp) = 0$ identically, reporting false "exact closure" (`is_closed = True`) regardless of how severely the Hamiltonian constraint is violated.
3. On a regular triangulated 3-sphere $\partial\Delta^4$ with all edge lengths 1.0 and zero momenta, each edge deficit is $2\pi - 3\arccos(1/3) \approx 2.590307$ rad, producing a large negative Hamiltonian defect $H_\perp(v) \approx -20.722456$ at every vertex. Under the naive encoding $\omega = d_0 H_\perp$, the solver reports $\Phi = 0$ and `is_closed = True`, completely laundering away the scalar curvature violation.

**The Direct-Sum Joint Formulation:**
To prevent scalar violations from disappearing into the spatial gauge orbit, the joint constraint system is defined on the direct-sum space $C^1(\Sigma) \oplus C^0(\Sigma)$:
$$
\Omega_{\mathrm{joint}} = \begin{pmatrix} p \\ H_\perp \end{pmatrix}, \quad D_{\mathrm{joint}} = \begin{pmatrix} d_0 \\ 0 \end{pmatrix} : C^0(\Sigma) \to C^1(\Sigma) \oplus C^0(\Sigma)
$$
Because the spatial gauge correction operator acts only on the momentum component, the joint $\ell^1$ quotient separates additively:
$$
\Phi_{D_{\mathrm{joint}}}(\Omega_{\mathrm{joint}}) = \min_{\alpha \in C^0} \left( \|p - d_0 \alpha\|_1 + \|H_\perp - 0\|_1 \right) = \Phi_{d_0}(p) + \|H_\perp\|_1
$$
This ensures that both momentum and Hamiltonian violations are strictly observable: a state achieves joint closure if and only if spatial momentum is pure gauge ($\Phi_{d_0}(p) = 0$) AND scalar Hamiltonian curvature vanishes identically ($\|H_\perp\|_1 = 0$).

---

## 5. Exact Strong Duality and Independently Checkable Dual Certificates

When a discrete constraint cochain fails exact closure ($\Phi_D([\omega]) > 0$), linear programming duality provides an independently checkable certificate that the violation cannot be removed by any coordinate choice.

### 5.1 Primal and Dual Linear Programs

The primal minimization problem:
$$
\Phi_D([\omega]) = \min_{\alpha \in \mathbb{R}^{|V|}, u \in \mathbb{R}^{|E|}} \sum_{e \in E} u_e
$$
subject to:
$$
-u_e \le \omega_e - (D \alpha)_e \le u_e, \quad u_e \ge 0
$$

The dual maximization problem:
$$
\Psi_D(\omega) = \max_{w \in \mathbb{R}^{|E|}} \sum_{e \in E} w_e \, \omega_e
$$
subject to:
$$
D^T w = 0, \quad -1 \le w_e \le 1
$$

**Theorem 5.1 (Exact Strong Duality and A Priori Bounds).**
For any finite matrix $D$ and vector $\omega$:
1. Both primal and dual problems are feasible.
2. The optimal value satisfies the elementary bounds:
   $$
   0 \le \Phi_D([\omega]) \le \|\omega\|_1
   $$
3. The optimal primal objective equals the optimal dual objective with **identically zero duality gap**:
   $$
   \Phi_D([\omega]) = \Psi_D(\omega) = \max_{\substack{w \in \mathbb{R}^{|E|} \\ D^T w = 0 \\ \|w\|_\infty \le 1}} \langle w, \omega \rangle
   $$

*Proof.*
Feasibility: setting $\alpha = 0$ and $u = |\omega|$ is primal feasible, establishing $\Phi_D([\omega]) \le \|\omega\|_1$. Setting $w = 0$ is dual feasible with value $0$, establishing $\Psi_D(\omega) \ge 0$.
Since the feasible regions are non-empty polyhedra and the primal objective is bounded below by $0$ (by non-negativity of norms), both optima exist and are attained at finite values. By the Strong Duality Theorem of Linear Programming (Schrijver 1986), the optimal values coincide: $\Phi_D([\omega]) = \Psi_D(\omega)$. $\square$

**Theorem 5.2 (Independently Checkable Dual Circulation Witness).**
Let $\alpha^*$ be an optimal primal gauge fix, and let $r^* = \omega - D \alpha^*$ be the optimal residual. If $\Phi_D([\omega]) > 0$, the dual optimizer $w^*$ is an **independently checkable certificate**:
1. *Divergence-free:* $D^T w^* = 0$ (a 1-cycle in homology $Z_1$ when $D = d_0$).
2. *Bounded:* $\|w^*\|_\infty \le 1$.
3. *Residual saturation:* $\langle w^*, r^* \rangle = \|r^*\|_1 = \Phi_D([\omega])$.
4. *Complementary slackness:*
   $$
   w_e^* = \begin{cases}
   +1, & r_e^* > 0 \\
   -1, & r_e^* < 0 \\
   \in [-1, 1], & r_e^* = 0
   \end{cases}
   $$

*Mathematical Significance:*
Weak duality establishes that for any dual feasible $w$ ($D^T w = 0, \|w\|_\infty \le 1$) and any gauge vector $\alpha$:
$$
\langle w, \omega \rangle = \langle w, \omega - D\alpha \rangle \le \|w\|_\infty \|\omega - D\alpha\|_1 \le \|\omega - D\alpha\|_1
$$
Taking the infimum over $\alpha$ yields $\langle w, \omega \rangle \le \Phi_D([\omega])$. Therefore, an external auditor can directly certify a lower bound on the constraint violation by evaluating $\langle w^*, \omega \rangle > 0$ and checking $D^T w^* = 0$ and $\|w^*\|_\infty \le 1$ via elementary matrix-vector multiplication, without needing to trust or rerun an optimizer. When primal and dual objectives match, optimality is certified unconditionally.

---

## 6. Ponzano--Regge Asymptotics and $\ell^1$ Phase Envelopes

The Ponzano--Regge model (Ponzano & Regge 1968) provides the canonical state sum for 3D quantum gravity, defined on a simplicial triangulation with spins $j_e \in \frac{1}{2}\mathbb{N}$ attached to edges.

### 6.1 Wigner 6j Symbol, Racah Formula, and Algebraic Radicals

The amplitude for a single tetrahedron is given by the Wigner 6j symbol:
$$
\left\{ \begin{matrix} j_1 & j_2 & j_3 \\ j_4 & j_5 & j_6 \end{matrix} \right\}
$$
Using the Racah single-sum formula, this amplitude evaluates to:
$$
\{6j\} = \Delta(j_1, j_2, j_3)\Delta(j_1, j_5, j_6)\Delta(j_4, j_2, j_6)\Delta(j_4, j_5, j_3) \sum_z \frac{(-1)^z (z+1)!}{\prod_i (z - p_i)! \prod_k (q_k - z)!}
$$
where each triangle coefficient $\Delta(a, b, c) = \sqrt{\frac{(a+b-c)!(a-b+c)!(-a+b+c)!}{(a+b+c+1)!}}$ contains a square-root radical.

*Radical vs Rational Structure:*
While symmetric configurations with identical spins can produce rational values (such as the regular all-spin-1 tetrahedron where $\{6j\} = 1/6$), general 6j symbols lie in quadratic field extensions due to triangle square roots. For example, for spins $(j_1, j_2, j_3; j_4, j_5, j_6) = (1, 1, 1; 1, 2, 2)$:
$$
\left\{ \begin{matrix} 1 & 1 & 1 \\ 1 & 2 & 2 \end{matrix} \right\} = -\frac{1}{\sqrt{20}}
$$
Its square is rational ($1/20$), but the symbol itself requires radical arithmetic.

### 6.2 Semiclassical Asymptotics and $\ell^1$ Geometric Bounds

In the semiclassical limit where edge spins are scaled by a large integer $k \to \infty$ ($j_e \mapsto k j_e$), Roberts (1999) established the asymptotic formula:
$$
\{k j_e\} \sim \frac{1}{\sqrt{12\pi V(j)}} \, k^{-3/2} \cos\left( k \, S_{\mathrm{Regge}} + \frac{\pi}{4} \right)
$$
where $V(j)$ is the volume of the unscaled tetrahedron (necessitating the $k^{-3/2}$ prefactor), and $S_{\mathrm{Regge}} = \sum_{e=1}^6 \left(j_e + \frac{1}{2k}\right) \theta_e$.

**Theorem 6.1 (Ponzano--Regge Phase Bounds).**
1. *Fixed-Angle Linear Phase Bound:* For fixed dihedral angles $\theta \in \mathbb{R}^6$ and arbitrary spin variations $j, j' \in \mathbb{R}^6$:
   $$
   |S_\theta(j) - S_\theta(j')| \le \|j - j'\|_1 \, \|\theta\|_\infty
   $$
2. *Schläfli Geometric Path Bound:* For two geometric tetrahedra with edge length vectors $J, J' \in \mathbb{R}_{>0}^6$ (where $J_e = j_e + 1/2$) connected by a smooth path $J(t)$ ($t \in [0, 1]$) along which every intermediate configuration remains a nondegenerate Euclidean tetrahedron:
   $$
   |S_{\mathrm{Regge}}(J') - S_{\mathrm{Regge}}(J)| \le \|J' - J\|_1 \sup_{0 \le t \le 1} \|\theta(J(t))\|_\infty \le \pi \|J' - J\|_1
   $$

*Proof & Counterexample to Naive Angle-Freezing:*
The proof of the fixed-angle bound follows directly from Hölder's inequality on $\mathbb{R}^6$:
$$
|S_\theta(j) - S_\theta(j')| = \left| \sum_{e=1}^6 (j_e - j'_e) \theta_e \right| \le \sum_{e=1}^6 |j_e - j'_e| |\theta_e| \le \|j - j'\|_1 \|\theta\|_\infty
$$
When edge lengths vary, however, dihedral angles $\theta_e = \theta_e(J)$ also vary. Recomputing angles produces a counterexample to the naive endpoint bound $|\Delta S| \le \|\Delta j\|_1 \|\theta(j)\|_\infty$:
- Start with all six spins $j_e = 2$ ($J_e = 2.5$), where $\theta_e = \arccos(1/3) \approx 1.230959$ rad.
- Increase only spin $(0, 1)$ to $j_{01} = 3$ ($J_{01} = 3.5$), leaving other five spins at 2.
- Both configurations are strictly nondegenerate Euclidean tetrahedra. Recomputing exact dihedral angles yields:
  $$
  |\Delta S| \approx 1.363496 > \|\Delta j\|_1 \|\theta(j)\|_\infty = 1.0 \times 1.230959 = 1.230959
  $$
To obtain a sound geometric bound, we apply the Schläfli differential identity $dS = \sum_{e=1}^6 \theta_e dJ_e$ (since $\sum J_e d\theta_e = 0$). Integrating along the path $J(t)$:
$$
|S(J') - S(J)| = \left| \int_0^1 \sum_{e=1}^6 \theta_e(J(t)) \frac{dJ_e}{dt} \, dt \right| \le \int_0^1 \sum_{e=1}^6 |\theta_e(t)| \left| \frac{dJ_e}{dt} \right| dt \le \|J' - J\|_1 \sup_{0 \le t \le 1} \|\theta(J(t))\|_\infty
$$
Because every dihedral angle in a nondegenerate Euclidean tetrahedron satisfies $0 < \theta_e < \pi$, the universal geometric bound $\pi \|J' - J\|_1$ holds unconditionally along any straight path that avoids degenerate configurations. $\square$

---

## 7. Quarantined High-Energy Speculative Analogies and Explicit Falsification Receipts

To preserve strict claim discipline, early speculative analogies are quarantined. The receipts below demonstrate that these speculative ideas fail due to missing derivations, category errors, or dimensional inconsistencies within this discrete framework, rather than constituting empirical refutations of continuous physical theories.

### 7.1 Receipt: Simplicial Gauge Group Uniqueness Falsified
- **Target Observable:** $SU(3) \times SU(2) \times U(1)$ Standard Model gauge group.
- **Speculative Ansatz:** Matching 2-simplices to $SU(3)$, 1-simplices to $SU(2)$, and 0-simplices to $U(1)$.
- **Obstruction Type:** Category error; absence of Lie algebra representations.
- **Proof of Failure:** Simplicial boundary operators $\partial_k: C_k \to C_{k-1}$ are abelian group homomorphisms over $\mathbb{Z}$ or $\mathbb{R}$. They do not encode Lie brackets, non-abelian structure constants $[T_a, T_b] = i f_{abc} T_c$, or gauge field representations. Any Lie group (e.g. $SO(N), Sp(N), E_8$) can be assigned to simplices with equal formal validity. The 3-2-1 hierarchy is mnemonic, not derived.

### 7.2 Receipt: Electroweak Higgs VEV Derivation Falsified
- **Target Observable:** Electroweak symmetry breaking VEV $v = 246.22$ GeV.
- **Speculative Ansatz:** $V(\Phi) = -\mu^2 |\Phi|^2 + \lambda |\Phi|^4$ with $v = \sqrt{\mu^2 / \lambda}$.
- **Obstruction Type:** Injected parameter scale.
- **Proof of Failure:** The scalar potential $V(\Phi)$ is not derived from discrete constraint closure; it is injected by hand. The value $v = 246$ GeV is supplied as an empirical boundary datum, not a mathematical consequence of primitive difference or $\ell^1$ cochain geometry.

### 7.3 Receipt: Topological SUSY Saturation Scale Falsified
- **Target Observable:** MSSM sparticle mass threshold at $E_{\mathrm{sat}} \approx 85.6 - 88.56$ TeV.
- **Speculative Ansatz:** $E_{\mathrm{sat}} = v_{\mathrm{EW}} \times 360^\circ$.
- **Obstruction Type:** Dimensional inconsistency and angle-unit numerology.
- **Proof of Failure:** The degree is an arbitrary human convention ($1/360$ of a circle). Multiplying an energy ($v_{\mathrm{EW}} = 246$ GeV) by the dimensionless number 360 has no gauge-invariant physical meaning. In radians, $v_{\mathrm{EW}} \times 2\pi \approx 1.55$ TeV, which differs by a factor of 57. No superspace, supersymmetry algebra $\{Q_\alpha, \bar{Q}_{\dot{\beta}}\} = 2 \sigma^\mu_{\alpha\dot{\beta}} P_\mu$, or supermultiplet is constructed.

### 7.4 Receipt: Hexagonal Wall Fine-Structure Constant Falsified
- **Target Observable:** QED fine-structure constant $\alpha^{-1} = 137.035999...$
- **Speculative Ansatz:** $4\pi^3 + \pi^2 + \pi \approx 137.036304$ via hexagonal Regge deficit lattice.
- **Obstruction Type:** Boundary convention artifact and post-hoc numerical coincidence.
- **Proof of Failure:** The formula $2\pi + 6\pi R$ reported in early notes charged boundary vertices with full $2\pi - \sum \theta$ rotations rather than the extrinsic boundary turning angle $\tau = \pi - \sum \theta$. Under the boundary turning convention $\tau$, the six corner vertices contribute $\pi/3$ each and the straight boundary vertices contribute zero, yielding total boundary turning $\sum \tau = 2\pi$ for every radius $R$, exactly matching the Gauss-Bonnet theorem ($\int \kappa_g ds = 2\pi$). Interior vertices have deficit 0. The expression $4\pi^3 + \pi^2 + \pi$ is an unmotivated algebraic combination selected post-hoc to approximate the CODATA value.

### 7.5 Receipt: Isolated Cochain Edge Dark Matter Analogy Falsified
- **Target Observable:** Cosmological cold dark matter density $\Omega_c$.
- **Speculative Ansatz:** An isolated 1-simplex with raw norm 2 represents dark matter.
- **Obstruction Type:** Missing dynamical stress-energy tensor and quotient gauge triviality.
- **Proof of Failure:** Under the unrestricted coboundary $d_0$, an isolated edge has quotient residual $\Phi_{d_0} = 0$, because assigning potential $\alpha_0 = 0, \alpha_1 = 2$ cancels the edge cochain completely. Raw cochain values do not represent surviving topological obstructions. Furthermore, an isolated edge possesses no stress-energy tensor $T_{\mu\nu}$, no gravitational clustering dynamics, and no cosmological equation of state $w = 0$.

---

## 8. Worked Computational Examples & Test Invariants

### 8.1 Minimal 2-Simplex Triangle Loop
Consider a single 2-simplex triangle with 3 vertices and 3 directed edges $(0,1), (1,2), (2,0)$. The coboundary matrix $d_0: C^0 \to C^1$ is:
$$
d_0 = \begin{pmatrix} -1 & 1 & 0 \\ 0 & -1 & 1 \\ 1 & 0 & -1 \end{pmatrix}
$$
1. **Exact Coboundary (Pure Gauge):** Let $\omega = d_0 [1, 2, 0]^T = [1, -2, 1]^T$.
   The solver yields $\Phi([\omega]) = 0.0$, duality gap $< 10^{-14}$, and `is_closed = True`.
2. **Circulation Loop (Obstruction in $C^1 / \mathrm{im} d_0$):** Let $\omega = [1, 1, 1]^T$.
   The solver yields $\Phi([\omega]) = 3.0$, optimal gauge fix $\alpha^* = [0, 0, 0]^T$, and dual witness $w^* = [1, 1, 1]^T$.
   Notice that $\partial_1 w^* = d_0^T w^* = [-1+1, 1-1, 1-1]^T = [0, 0, 0]^T$, and $\|w^*\|_\infty = 1 \le 1$.
   The duality gap is $\Phi - \langle w^*, \omega \rangle = 3.0 - 3.0 = 0.0$.
   *Note on Cohomology:* On a filled triangle with face $(0,1,2)$, $(d_1 \omega)(0,1,2) = 3 \ne 0$. Thus $\omega$ is not a cocycle and does not represent an element of $H^1(K)$, but rather a non-vanishing quotient residual in $C^1(K) / \mathrm{im}(d_0)$.

### 8.2 Closed 4-Sphere Simplicial Bianchi Verification & Perturbation

Consider the boundary of a 5-simplex $\partial \Delta^5 \cong S^4$, comprising 6 vertices, 15 edges, 20 triangles, 15 tetrahedra, and 6 4-simplices.

1. **Regular Symmetric Complex:** Each triangle belongs to exactly $6 - 3 = 3$ 4-simplices. Assigning the regular deficit angle $\varepsilon_{\mathrm{reg}} = 2\pi - 3\arccos(1/4) \approx 2.328837$ rad to all 20 triangular hinges:
   $$
   d_2 \varepsilon = \partial_3^T \varepsilon = 0 \quad (\|d_2 \varepsilon\|_1 = 0.0)
   $$
   Alternating signs cancel identically on every tetrahedron: $c - c + c - c = 0$.
2. **Perturbed Complex (Non-Abelian Failure):** Setting $\ell_{01} = 1.1$ while keeping all other edges at $1.0$ preserves Euclidean nondegeneracy (smallest Gram eigenvalue $\approx 0.4851$) but yields:
   $$
   \|d_2 \varepsilon\|_1 \approx 1.956565, \quad \|d_2 \varepsilon\|_\infty \approx 0.244571
   $$
   confirming that generic curved 4-manifolds do not satisfy scalar Bianchi coboundary closure.

### 8.3 Hamiltonian Blind Spot and Direct-Sum Resolution on Regular $\partial\Delta^4$

Consider the boundary complex of a regular 4-simplex $\partial\Delta^4$ (homeomorphic to the 3-sphere $S^3$), comprising 5 vertices, 10 edges, 10 triangles, and 5 tetrahedra, with all edge lengths set to $\ell_e = 1.0$.

1. **Geometry and Deficit Angles:**
   Each interior edge belongs to exactly $5 - 2 = 3$ regular tetrahedra. The dihedral angle of a regular tetrahedron is $\theta_{\mathrm{tet}} = \arccos(1/3) \approx 1.230959$ rad.
   The deficit angle on every edge is:
   $$
   \varepsilon_e = 2\pi - 3\arccos(1/3) \approx 2.590307 \text{ rad}
   $$
2. **Scalar Curvature and Hamiltonian Value:**
   Under the toy discrete Hamiltonian formulation, with zero momentum ($p_e = 0$ for all edges) and unit dual volume $V_v^* = 1.0$, the scalar constraint at vertex $v$ evaluates:
   $$
   H_\perp(v) = \sum_{e \sim v} p_e^2 - R(v) = 0 - \sum_{e \sim v} \varepsilon_e \approx -20.722456
   $$
   This yields a total $\ell^1$ Hamiltonian violation of $\|H_\perp\|_1 = \sum_{v=0}^4 |H_\perp(v)| = 5 \times 20.722456 \approx 103.612282$.
3. **Failure of Naive Coboundary Encoding:**
   In the naive formulation where constraints are mapped into a single 1-cochain $\omega_{\mathrm{naive}} = p + d_0 H_\perp$, when $p = 0$, $\omega_{\mathrm{naive}} = d_0 H_\perp$ is by definition an exact coboundary in $\operatorname{im}(d_0)$.
   Solving the linear program $\Phi_{d_0}([\omega_{\mathrm{naive}}]) = \min_\alpha \|\omega_{\mathrm{naive}} - d_0 \alpha\|_1$ sets $\alpha^* = H_\perp$ and yields:
   $$
   \Phi_{d_0}([\omega_{\mathrm{naive}}]) = 0.0, \quad \text{reporting } \texttt{is\_closed = True}
   $$
   The solver is completely blind to the scalar Hamiltonian violation of $> 103.61$.
4. **Direct-Sum Joint Resolution:**
   Under the joint direct-sum system $C^1(K) \oplus C^0(K)$ with block coboundary operator $D_{\mathrm{joint}} = \begin{pmatrix} d_0 \\ 0 \end{pmatrix}$:
   $$
   \Phi_{\mathrm{joint}}([\omega_{\mathrm{joint}}]) = \min_\alpha \left( \|p - d_0 \alpha\|_1 + \|H_\perp - 0 \alpha\|_1 \right) = \Phi_{d_0}([p]) + \|H_\perp\|_1
   $$
   For $p = 0$, $\Phi_{\mathrm{joint}} = 0 + 103.612282 = 103.612282 > 0$, correctly diagnosing the non-closure (`is_closed = False`).
   The certified dual witness is $w^*_{\mathrm{joint}} = (0, \operatorname{sgn}(H_\perp)) \in C_1 \oplus C_0$, satisfying $D_{\mathrm{joint}}^T w^*_{\mathrm{joint}} = d_0^T 0 = 0$, $\|w^*_{\mathrm{joint}}\|_\infty = 1$, and attaining exact strong duality with gap $0.0$.

### 8.4 Exact Rational Basis Reconstruction on Carroll's Regression Case

Floating-point linear programming solvers operating near machine precision or ill-conditioned geometry can report non-zero residuals or fail certification on tiny non-zero cochains. The exact rational solver `exact_rational_l1_quotient` operates strictly over $\mathbb{Q}$ using Python's `fractions.Fraction` and certified Gauss--Jordan elimination.

Consider the regression case identified by J. H. Carroll:
$$
\omega = \left[ \frac{1}{1000001} \right] \in C^1, \quad D = \begin{pmatrix} -1 & 1 \end{pmatrix}: C^0 \to C^1
$$
where $C^0 \cong \mathbb{Q}^2$ and $C^1 \cong \mathbb{Q}^1$.

1. **Primal Resolution:**
   The gauge condition is $D \alpha = -\alpha_0 + \alpha_1 = 1/1000001$.
   Setting $\alpha_0 = 0$ and $\alpha_1 = 1/1000001$ yields an exact cancellation $\omega - D\alpha = [0]$.
   The solver reconstructs the primal gauge potential $\alpha^* = [0, 1/1000001]^T$, yielding exact primal objective:
   $$
   \Phi_D([\omega]) = \frac{0}{1}, \quad \Psi_D(\omega) = \frac{0}{1}, \quad \text{Gap} = \frac{0}{1}, \quad \texttt{is\_closed = True, is\_certified = True}
   $$
2. **Dual Nullspace Certification:**
   The dual constraint requires $D^T w = \begin{pmatrix} -1 \\ 1 \end{pmatrix} w = \begin{pmatrix} 0 \\ 0 \end{pmatrix}$, which forces $w = [0]$.
   Since $w = 0$, the dual objective is $\langle w, \omega \rangle = 0$, which matches the primal value $0$ identically.
3. **Comparison on Non-Zero Cycle:**
   Conversely, on the directed triangle cycle $\omega = [1, 1, 1]^T$ with incidence $d_0$, the exact solver identifies the nullspace witness $w^* = [1, 1, 1]^T$, verifies $d_0^T w^* = [0, 0, 0]^T$, $\|w^*\|_\infty = 1$, and produces $\Phi = 3/1, \Psi = 3/1, \text{Gap} = 0/1, \texttt{is\_closed = False, is\_certified = True}$.

### 8.5 Finite Hodge--Dirac Graded Algebra on Simplicial Complexes

On finite simplicial complexes, discrete differential operators form a graded cochain complex $C^0 \xrightarrow{d_0} C^1 \xrightarrow{d_1} C^2 \dots$ with nilpotency $d_{k+1} d_k = 0$. The finite Hodge--Dirac operator $D = d + d^*$ on $C = \bigoplus_k C^k$ satisfies $D^2 = \Delta = d d^* + d^* d$.

1. **Single-Triangle Delta Matrix Identity:**
   On a single oriented 2-simplex $\Delta^2$ with 3 vertices, 3 edges, and 1 face, with $d_0: C^0 \to C^1$ and $d_1: C^1 \to C^2$:
   $$
   \Delta_1 = d_0 d_0^T + d_1^T d_1 = 3 I_3
   $$
   This is verified as a coordinate identity in `hodge_dirac_susy.py` and formalized in Lean 4 (`delta1_is_3_identity` in `GR002/HodgeDiracSUSY.lean`).
2. **Witten Index and Spectrum:**
   The finite Hodge Laplacian $\Delta$ decomposes into even and odd subspaces $C^{\mathrm{even}} = C^0 \oplus C^2$ ($\dim = 3 + 1 = 4$) and $C^{\mathrm{odd}} = C^1$ ($\dim = 3$). The finite Witten index evaluates:
   $$
   W = \dim \ker(\Delta_{\mathrm{even}}) - \dim \ker(\Delta_{\mathrm{odd}}) = \beta_0 + \beta_2 - \beta_1 = 1 + 0 - 0 = 1
   $$
   matching the Euler characteristic $\chi(\Delta^2) = 1$.
   On two triangles glued along an edge (4 vertices, 5 edges, 2 faces), the Hodge--Laplacian spectrum on 1-forms evaluates to $\{2, 2, 4, 4, 4\}$, with trace $\operatorname{Tr}(\Delta_1) = 16$.
3. **Physical Interpretation Boundary:**
   These properties represent standard theorems in finite-dimensional graded exterior algebra and discrete differential geometry. They do not construct a continuous spacetime supersymmetry, a gravitino superpartner, or a spontaneous supersymmetry breaking scale.

### 8.6 Fixed-Carrier Quotient Homogeneity and the No-Double-Well Invariant

A central question in discrete field theories is whether non-trivial symmetry-breaking effective potentials (such as the Higgs Mexican-hat double well) can emerge from pure $\ell^1$ metric minimization without injected polynomial interactions.

1. **Quotient Absolute Homogeneity Theorem:**
   Let $K$ be a fixed finite cell carrier, $D: C^{k-1} \to C^k$ a linear coboundary operator, and $\omega \in C^k$. The quotient residual along a fixed ray $t \mapsto t\omega$ ($t \in \mathbb{R}$) satisfies:
   $$
   \Phi_D([t\omega]) = \min_\alpha \|t\omega - D\alpha\|_1 = |t| \min_{\alpha'} \|\omega - D\alpha'\|_1 = |t| \Phi_D([\omega])
   $$
   where $\alpha' = \alpha / t$ for $t \ne 0$, and the case $t = 0$ is trivial.
2. **Formalization and Numerical Verification:**
   This identity is formalized in Lean 4 (declarations `fixed_carrier_quotient_homogeneity`
   and `quotient_candidate_homogeneity` in module `GR002/LinearEnergy.lean`).
   In numerical simulations (`higgs_pure_linear_certificate.py`), sampling $E(\phi) = \Phi_D([\phi \omega_0])$
   across $\phi \in [0.1, 5.0]$ confirms that a linear fit achieves $R^2 = 1.000000$, whereas a quartic
   double-well ansatz achieves only $R^2 = 0.985563$.
3. **Absence of Spontaneous Symmetry Breaking:**
   Because $t \mapsto |t| \Phi_D([\omega])$ is strictly convex (or identically zero) with its global minimum
   uniquely at the origin $t = 0$ (formalized as `linear_energy_has_origin_minimum`), pure linear
   $\ell^1$ topology along fixed rays cannot produce a non-zero vacuum expectation value ($v > 0$)
   or double-well symmetry breaking. Any reported Higgs potential must be an explicit polynomial injection.

### 8.7 Discrete Descent Dynamics on Non-Manifold Complexes

The Discrete Descent Algorithm (DDA) iterates local coexact updates to reduce curvature mass $\gamma_{k+1} = \|d_k \omega\|_1$. While uncoupled local updates descend monotonically on planar duals and trees, they do not possess a universal descent guarantee on generic complexes.

1. **Five-Triangle Shared-Edge Counterexample:**
   Consider five triangles $(0, 1, i)$ ($i = 2, \dots, 6$) meeting at a single shared interior edge $(0, 1)$ (a non-manifold 2-complex). Let the cochain have value $1.0$ on the common edge $(0, 1)$ and $0.0$ on all outer edges.
   The initial curl magnitude on each face is $1.0$, giving initial curvature mass $\gamma_{\mathrm{before}} = 5.0$.
   An uncoupled coexact update applies a boundary subtraction of $-1/3$ from each of the five triangles onto edge $(0, 1)$, over-correcting it to $1.0 - 5(1/3) = -2/3$. The updated curvature mass evaluates:
   $$
   \gamma_{\mathrm{after}} = \frac{20}{3} \approx 6.6667 > 5.0
   $$
2. **Loss Ledger Honesty & Prior-Degree Guards:**
   Rather than recording the initial mass of $5.0$ as canceled, the repaired DDA engine
   (`discrete_descent_engine.py`) explicitly evaluates the candidate complex, records $\Delta \gamma = +5/3$,
   and sets `curl_mass_canceled = 0.0`.
   Furthermore, when higher-degree lifts encounter zero residual at degree $k+1$ while obligations at degree $k$ remain unresolved, the engine returns `status = TYPED_OBSTRUCTION`, preventing a trivial higher-dimensional zero from declaring the global problem solved.

---

## 9. Falsifiability and Reproducibility

Every mathematical theorem and numerical claim in this monograph is falsifiable by executing the verified test suite under Python 3.14:
```bash
python -m pytest code/tests -n 8
```

### Reproducibility Criteria:
1. If any regular boundary complex where all deficit angles are uniform exhibits non-zero scalar Bianchi flux $\|d_2 \varepsilon\|_1 > 10^{-10}$, Theorem 3.2(1) is falsified.
2. If any constraint cochain $\omega$ produces a duality gap $|\Phi_D([\omega]) - \Psi_D(\omega)| > 10^{-8}$ between primal and dual LP solvers, Theorem 5.1 is falsified.
3. If any two spin configurations along an admissible Euclidean path violate $|S(J') - S(J)| \le \pi \|J' - J\|_1$, Theorem 6.1(2) is falsified.
4. If any pure gauge shift $\omega \mapsto \omega + D \gamma$ changes the quotient norm $\Phi_D$, Theorem 4.1 is falsified.

---

## 10. Canonical References

1. **Regge, T.** (1961). *General relativity without coordinates*. Il Nuovo Cimento, 19(3), 558--571.
2. **Hamber, H. W., & Kagel, G.** (2001). *Exact Bianchi identity in Regge gravity*. Nuclear Physics B, 608(1-2), 435--452. arXiv:gr-qc/0107031.
3. **Ponzano, G., & Regge, T.** (1968). *Semiclassical limit of Racah coefficients*. Spectroscopic and group theoretical methods in physics, 1--58.
4. **Wheeler, J. A.** (1968). *Superspace and the nature of quantum geometrodynamics*. Battelle Rencontres, 242--307.
5. **DeWitt, B. S.** (1967). *Quantum theory of gravity. I. The canonical theory*. Physical Review, 160(5), 1113.
6. **Misner, C. W., Thorne, K. S., & Wheeler, J. A.** (1973). *Gravitation*. W. H. Freeman and Company, San Francisco.
7. **Friedberg, R., & Lee, T. D.** (1984). *Derivation of Regge's action from Einstein's theory of general relativity*. Nuclear Physics B, 242(1), 145--166.
8. **Hamber, H. W.** (2009). *Quantum Gravitation: The Feynman Path Integral Approach*. Springer Science & Business Media.
9. **Bahr, B., & Dittrich, B.** (2009). *Regge calculus from a new perspective: Towards consistent approximations of quantum gravity*. Physical Review D, 80(12), 124030. arXiv:0905.1670.
10. **Freidel, L., & Louapre, D.** (2003). *Non-perturbative summation over 3D discrete geometries*. Nuclear Physics B, 662(1-2), 279--298.
11. **Roberts, J.** (1999). *Classical 6j-symbols and the tetrahedron*. Geometry & Topology, 3(1), 21--66. arXiv:math-ph/9812013.
12. **Schrijver, A.** (1986). *Theory of Linear and Integer Programming*. John Wiley & Sons.
