<div align="center">

# The Dressing Field Method on Finite Graphs: Proofs of the Finite Results

**Author:** Jeremy H. Carroll

**Date:** 2026-10-26

**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)

</div>

## Introduction

This note gives written proofs of the results of the dressing-field material in
[ravera_dfm_dossier.md](../ravera_dfm_dossier.md) and of the two-stage Borel dressing (records
TFQ-0016, TFQ-0398, TFQ-0399, TFQ-0400) that the derivation DAG (`dag/derivation_dag.json`)
records as proved in Lean. Each section states one result, proves it, and names the Lean
declarations that check it. The DAG identifier is on the line beginning *DAG node*.

Section 1 is about graphs with edge labels in an arbitrary group. Section 2 is about
upper-triangular $2\times2$ labels. Section 3 collects exact rational identities from the
electroweak and flavour examples in the dossier. Those identities are algebra over $\mathbb Q$ or
$\mathbb Q(i)$. They are not derived from a Lagrangian, and they are not computations of
anomalies from triangle diagrams. Section 3 says this case by case.

**Conventions.** A graph has vertices $V$ and edges $E$, each edge $e$ with a source $s(e)$ and a
target $t(e)$. A connection is $U\colon E\to H$ for a group $H$. The transport of a walk is the
product of its edge labels, later edges on the left, with $U_e^{-1}$ for an edge traversed
backwards. A dressing is $u\colon V\to H$, and the dressed connection is
$U^u_e=u(t(e))\,U_e\,u(s(e))^{-1}$.

---

## 1. Dressing on a graph

### 1.1 Neutralization and closed walks

DAG nodes: `DFM-GENERAL-GRAPH-DRESSING` `DFM-TREE-CHANGE` `DFM-TREE-CHORD-COORDINATES`

**Theorem.** Let $U$ be a connection on a finite graph with values in a group $H$.

1. There is a dressing $u$ with $U^u_e=1$ for every edge if and only if every closed walk has
   transport $1$.
2. Fix in each component a root $r$ and a spanning tree, and let $T(v)$ be the transport along the
   tree path from $r$ to $v$. Then $u=T^{-1}$ neutralizes every tree edge, and $U^u_e$ on a chord
   $e$ is the transport around the closed walk "tree path to $s(e)$, then $e$, then tree path back
   from $t(e)$". So it suffices to test the chords.
3. For any two dressings $u,u'$, the field $C(v)=u'(v)u(v)^{-1}$ satisfies
   $U^{u'}_e=C(t(e))\,U^u_e\,C(s(e))^{-1}$. If $u$ and $u'$ both neutralize $U$, then $C$ is
   constant on each component.

*Proof.* Every claim follows from the telescoping identity: for a walk $p$ from $a$ to $b$, the
transport of $U^u$ along $p$ is $u(b)\,\mathrm{tr}_U(p)\,u(a)^{-1}$. This holds for a single edge
by definition and is preserved by concatenation and reversal.

(1) If $U^u=1$, a closed walk at $a$ has $\mathrm{tr}_U(p)=u(a)^{-1}\cdot1\cdot u(a)=1$.
Conversely, if every closed walk has transport $1$, the transport from the root of a component to
$v$ does not depend on the walk. Call it $T(v)$ and put $u=T^{-1}$. For any edge $e$, going to
$s(e)$ and then along $e$ is a walk to $t(e)$, so $U_eT(s(e))=T(t(e))$. Hence
$U^u_e=T(t(e))^{-1}U_eT(s(e))=1$.

(2) For a tree edge, $U_eT(s(e))=T(t(e))$ holds by the definition of $T$, so $U^u_e=1$. For a chord,
$U^u_e=T(t(e))^{-1}U_eT(s(e))$ is the transport of the closed walk described, read from the root.
Every closed walk is a product of conjugates of these chord loops, since the tree carries no loops.
So all closed walks have transport $1$ exactly when all chords are neutralized.

(3) $C(t)U^u_eC(s)^{-1}=u'(t)u(t)^{-1}\,u(t)U_eu(s)^{-1}\,u(s)u'(s)^{-1}=U^{u'}_e$. If both
dressings neutralize $U$, then $C(t(e))=C(s(e))$ for every edge, so $C$ is constant along walks.
$\square$

For a non-abelian $H$ the chord values $U^u_e$ are not gauge invariant by themselves: changing the
tree, or the dressing, conjugates them as in (3). The conjugacy classes of closed-loop transports
are invariant. The dossier uses the mirror convention, in which a gauge acts as
$U_{ij}\mapsto G_i^{-1}U_{ij}G_j$. In that convention, on the triangle with tree edges $01,12$ and
chord $02$, the rooted tree dressing sends both tree links to $1$ and the chord to
$U_{02}U_{12}^{-1}U_{01}^{-1}$, the holonomy around the triangle. This holds whatever anchored gauge
$(1,G_1,G_2)$ was applied first. The
counting statement that dressed chords give coordinates $H^{|E|-|V|+1}$ on connections modulo
gauge for every connected graph is in the dossier. It follows from (2) and (3), but it is not in
Lean.

Lean: `lean4/FiniteGraphDressing.lean::neutralizable_iff_closed_walks_forest` (1) and (2) for a
rooted forest given by root paths, `lean4/FiniteGraphDressing.lean::tree_dressing_iff`,
`lean4/FiniteGraphDressing.lean::change_dressing` and
`lean4/FiniteGraphDressing.lean::neutralizers_constant` (3), for an arbitrary group.
`lean4/RaveraDfmFiniteToContinuum.lean::spanning_tree_nonabelian_mat2_factorization` checks the
triangle for rational $2\times2$ matrices with right inverses, using
`lean4/RaveraDfmFiniteToContinuum.lean::mat2_mul_assoc`.

---

## 2. Two-stage dressing for upper-triangular labels

### 2.1 The Borel factorization and the two-stage dressing

DAG nodes: `DFM-HIERARCHICAL-BOREL` `TFQ-0016`

Let $B$ be the group of invertible upper-triangular $2\times2$ matrices over $\mathbb Q$,
$x=\begin{pmatrix}d_1&b\\0&d_2\end{pmatrix}$ with $d_1d_2\neq0$. Let $T\subset B$ be the diagonal
matrices and $N\subset B$ the unit upper-triangular ones. Let $\pi(x)=\operatorname{diag}(d_1,d_2)$.

**Theorem.** (i) $\pi\colon B\to T$ is a homomorphism with kernel $N$. So $N$ is normal, and every
$x\in B$ factors uniquely as $x=\pi(x)\,n(x)$ with $n(x)=\pi(x)^{-1}x\in N$.

(ii) Let $V$ be the vertices of a rooted tree, given by a parent map and a depth that decreases
toward the root. Give each non-root vertex $v$ a label $U(v)\in B$ on the edge from its parent
$p(v)$, and put $T(r)=I$ and $T(v)=U(v)T(p(v))$. A vertex field $g$ with $g(r)=I$ and
$U(v)=g(v)g(p(v))^{-1}$ off the root equals $T$. Write $T(v)=D(v)n(v)$ as in (i).

(iii) The stage-one field $u_N(v)=D(v)n(v)^{-1}D(v)^{-1}$ lies in $N$. Writing
$D(v)=\operatorname{diag}(d_1,d_2)$ and $T(v)=\begin{pmatrix}d_1&b\\0&d_2\end{pmatrix}$, it equals
$\begin{pmatrix}1&-b/d_2\\0&1\end{pmatrix}$. Dressing by $u_N$ makes each tree edge diagonal,
$u_N(v)U(v)u_N(p(v))^{-1}=D(v)D(p(v))^{-1}$, and leaves $\pi$ of every label unchanged,
$\pi(u_N(a)\,g\,u_N(c)^{-1})=\pi(g)$.

(iv) The stage-two field $u_T(v)=D(v)^{-1}$ satisfies $u_T(v)u_N(v)=T(v)^{-1}$. So the composite
dressing sends a label $g$ from $c$ to $a$ to $T(a)^{-1}gT(c)$, which is $I$ exactly when
$g=T(a)T(c)^{-1}$.

*Proof.* (i) The diagonal of a product of upper-triangular matrices is the product of the
diagonals, so $\pi$ is a homomorphism. Its kernel is $N$ by definition. Uniqueness: if
$Dn=D'n'$ then $D'^{-1}D=n'n^{-1}\in T\cap N=\{I\}$.

(ii) Induction on depth: $g(r)=I=T(r)$, and $g(v)=U(v)g(p(v))=U(v)T(p(v))=T(v)$.

(iii) $u_N(v)$ is a conjugate of $n(v)^{-1}\in N$, and $N$ is normal. Explicitly,
$n(v)=\begin{pmatrix}1&b/d_1\\0&1\end{pmatrix}$, and conjugating its inverse by $D(v)$ multiplies the
corner by $d_1/d_2$, which gives $-b/d_2$. Next, $u_N(v)T(v)=Dn^{-1}D^{-1}Dn=D(v)$. Since
$U(v)=T(v)T(p(v))^{-1}$,
$$u_N(v)U(v)u_N(p(v))^{-1}=\big(u_N(v)T(v)\big)\big(u_N(p(v))T(p(v))\big)^{-1}=D(v)D(p(v))^{-1}.$$
Finally, $\pi(u_N)=I$ and $\pi$ is a homomorphism.

(iv) $u_T(v)u_N(v)=D^{-1}Dn^{-1}D^{-1}=n^{-1}D^{-1}=T(v)^{-1}$, and the composite dressing is
$g\mapsto(u_Tu_N)(a)\,g\,(u_Tu_N)(c)^{-1}=T(a)^{-1}gT(c)$. $\square$

Invertibility matters. $\begin{pmatrix}0&1\\0&1\end{pmatrix}$ has no factorization of the form in
(i). The map that keeps $d_1$ and $b$ and sets $d_2=1$ is not a homomorphism: for
$x=\begin{pmatrix}2&1\\0&3\end{pmatrix}$ the corner of the image of $x^2$ is $5$, while the corner of
the square of the image of $x$ is $3$.

Record TFQ-0016 states the same factorization for a separate model of $B$ as triples
$(d_1,b,d_2)$. It also applies stages one and two to a fixed graph with vertices $0,\dots,3$,
edges $01,12,02,23,13$ and tree $01,02,23$, where stage two reproduces
$T(t(e))^{-1}U_eT(s(e))$ on all five edges. That is (iv) for this graph. Neither record identifies
the triple model with the map of record QM-213, and neither contains a colour-transport
statement.

Lean: `lean4/CampaignDfmHierarchicalBorel.lean::b2_semidirect_factorization`,
`lean4/CampaignDfmHierarchicalBorel.lean::b2_factorization_unique`,
`lean4/CampaignDfmHierarchicalBorel.lean::unipotent_subgroup_normal`,
`lean4/CampaignDfmHierarchicalBorel.lean::torusProj_mul`,
`lean4/CampaignDfmHierarchicalBorel.lean::u_N_eq_conjugate`,
`lean4/CampaignDfmHierarchicalBorel.lean::stage1_tree_edge`,
`lean4/CampaignDfmHierarchicalBorel.lean::stage1_preserves_quotient`,
`lean4/CampaignDfmHierarchicalBorel.lean::two_stage_factorization`,
`lean4/CampaignDfmHierarchicalBorel.lean::stage2_reproduces`,
`lean4/CampaignDfmHierarchicalBorel.lean::dressed_one_iff`,
`lean4/CampaignDfmHierarchicalBorel.lean::anchored_transport_unique`,
`lean4/CampaignDfmHierarchicalBorel.lean::factorization_fails_if_singular`,
`lean4/CampaignDfmHierarchicalBorel.lean::badProj_not_homomorphism`;
for TFQ-0016, `lean4/CampaignTfq0016B2Dressing.lean::CampaignTfq0016.UpperTri2.b2_semidirect_factorization`,
`lean4/CampaignTfq0016B2Dressing.lean::CampaignTfq0016.UpperTri2.b2_factorization_unique`,
`lean4/CampaignTfq0016B2Dressing.lean::CampaignTfq0016.UpperTri2.unipotent_subgroup_normal`,
`lean4/CampaignTfq0016B2Dressing.lean::CampaignTfq0016.stage1_tree_edges_diagonal`,
`lean4/CampaignTfq0016B2Dressing.lean::CampaignTfq0016.stage1_preserves_quotient_projection`,
`lean4/CampaignTfq0016B2Dressing.lean::CampaignTfq0016.stage2_reproduces_residual`,
`lean4/CampaignTfq0016B2Dressing.lean::CampaignTfq0016.two_stage_factorization`.

### 2.2 Discrete curvature and the Bianchi identity

DAG nodes: `DFM-HIERARCHICAL-BOREL` `TFQ-0016`

Let $R$ be a ring and $A\colon R\times R\to R$ a 1-cochain. Put $(bA)(u,v,w)=-A(u,w)$,
$(A\smile A)(u,v,w)=A(u,v)A(v,w)$, and $K=bA+A\smile A$, so $K(u,v,w)=A(u,v)A(v,w)-A(u,w)$. For a
2-cochain $L$ put $(bL)(u,v,w,z)=-L(u,w,z)+L(u,v,z)$, $(A\smile L)(u,v,w,z)=A(u,v)L(v,w,z)$ and
$(L\smile A)(u,v,w,z)=L(u,v,w)A(w,z)$.

**Proposition.** (i) $b(bA)=0$. (ii) $bK+A\smile K-K\smile A=0$. (iii) If $g,\bar g\colon R\to R$
satisfy $g(x)\bar g(x)=1$ and $A^g(x,y)=g(x)A(x,y)\bar g(y)$, then
$K(A^g)(u,v,w)=g(u)K(A)(u,v,w)\bar g(w)$.

*Proof.* (i) $b(bA)(u,v,w,z)=-(bA)(u,w,z)+(bA)(u,v,z)=A(u,z)-A(u,z)=0$.
(ii) Write $A_{uv}$ for $A(u,v)$. Then $bK=A_{uz}-A_{uw}A_{wz}-A_{uz}+A_{uv}A_{vz}$,
$A\smile K=A_{uv}A_{vw}A_{wz}-A_{uv}A_{vz}$ and $K\smile A=A_{uv}A_{vw}A_{wz}-A_{uw}A_{wz}$. In
$bK+A\smile K-K\smile A$ every term cancels against another.
(iii) $A^g_{uv}A^g_{vw}=g(u)A_{uv}\bar g(v)g(v)A_{vw}\bar g(w)=g(u)A_{uv}A_{vw}\bar g(w)$, and
$A^g_{uw}=g(u)A_{uw}\bar g(w)$. Subtracting gives the claim. $\square$

The computations in (ii) and (iii) never swap two factors, so they hold verbatim for
non-commutative coefficients. Lean states them for commutative $R$. Dressing only at the source
end does not give covariance: with $A_{01}=A_{12}=1$, $A_{02}=0$, $g(0)=1$ and $g(1)=2$, the
source-dressed curvature is $1\cdot2-0=2$, while $g(0)K(0,1,2)=1$. With the same values, dressing
at both ends, with $g(2)=1$ and $\bar g(1)=1/2$, satisfies (iii).

Lean: `lean4/CampaignDfmHierarchicalBorel.lean::b_squared_zero`,
`lean4/CampaignDfmHierarchicalBorel.lean::discrete_bianchi_identity`,
`lean4/CampaignDfmHierarchicalBorel.lean::curvature_gauge_covariance`,
`lean4/CampaignDfmHierarchicalBorel.lean::source_only_dressing_breaks_curvature`,
`lean4/CampaignDfmHierarchicalBorel.lean::endpoint_dressing_matches_curvature`;
`lean4/CampaignTfq0016B2Dressing.lean::CampaignTfq0016.b_squared_zero`,
`lean4/CampaignTfq0016B2Dressing.lean::CampaignTfq0016.discrete_bianchi_identity`,
`lean4/CampaignTfq0016B2Dressing.lean::CampaignTfq0016.curvature_gauge_covariance`.

---

## 3. Rational identities in the electroweak and flavour examples

### 3.1 Dressing a Higgs doublet on a rational sphere

DAG node: `DFM-EW-DOUBLET-REDUCTION`

**Proposition.** Let $\Phi=(\phi_+,\phi_0)=(a+ib,\;c+id)$ with $a,b,c,d,r\in\mathbb Q$, $r\neq0$ and
$a^2+b^2+c^2+d^2=r^2$, and put
$$u(\Phi)=\frac1r\begin{pmatrix}\bar\phi_0&\phi_+\\-\bar\phi_+&\phi_0\end{pmatrix}.$$
Then $u(\Phi)\in SU(2)$ and $u(\Phi)^\dagger\Phi=(0,r)$. For a real doublet ($b=d=0$), $u(\Phi)$ is a
rotation of determinant $1$.

*Proof.* $u$ has the form $\begin{pmatrix}\alpha&\beta\\-\bar\beta&\bar\alpha\end{pmatrix}$ with
$|\alpha|^2+|\beta|^2=(|\phi_0|^2+|\phi_+|^2)/r^2=1$, and every such matrix is unitary with
determinant $|\alpha|^2+|\beta|^2=1$. Then
$u^\dagger\Phi=\frac1r(\phi_0\phi_+-\phi_+\phi_0,\;\bar\phi_+\phi_++\bar\phi_0\phi_0)=(0,r)$. $\square$

So the three Goldstone directions are removed by a field-dependent $SU(2)$ element, and the
remaining component is the radius.

Lean: `lean4/RaveraDfmFiniteToContinuum.lean::ew_gaussian_4d_goldstone_elimination` checks the four
real components of $u^\dagger\Phi=(0,r)$.
`lean4/RaveraDfmFiniteToContinuum.lean::ew_dfm_goldstone_elimination_on_sphere` checks the real
case: determinant $1$, $u^{\mathsf T}u=I$ and the image $(0,r)$. Unitarity and $\det=1$ of the
complex $u$, as proved above, are not in Lean. Neither is the covariance $u(g\Phi)=g\,u(\Phi)$.

### 3.2 Weinberg projectors and $\rho=1$

DAG node: `DFM-WEINBERG-PROJECTORS-RHO`

**Proposition.** Let $g,g',v\in\mathbb Q$ with $\Delta=g^2+g'^2\neq0$, and set
$P_\gamma=\Delta^{-1}\begin{pmatrix}g'^2&gg'\\gg'&g^2\end{pmatrix}$,
$P_Z=\Delta^{-1}\begin{pmatrix}g^2&-gg'\\-gg'&g'^2\end{pmatrix}$ and
$M^2=\frac{v^2}4\begin{pmatrix}g^2&-gg'\\-gg'&g'^2\end{pmatrix}$. Then $P_\gamma,P_Z$ are
complementary orthogonal idempotents, $M^2P_\gamma=0$, and
$\sin^2\theta_W+\cos^2\theta_W=1$ for $\sin^2\theta_W=g'^2/\Delta$ and $\cos^2\theta_W=g^2/\Delta$.
If also $g\neq0\neq v$, then $M_W^2/(M_Z^2\cos^2\theta_W)=1$ with $M_W^2=v^2g^2/4$ and
$M_Z^2=v^2\Delta/4$.

*Proof.* Let $n=(g',g)$ and $m=(g,-g')$. Then $n\cdot m=0$, $n\cdot n=m\cdot m=\Delta$,
$P_\gamma=nn^{\mathsf T}/\Delta$, $P_Z=mm^{\mathsf T}/\Delta$ and $M^2=\frac{v^2}4mm^{\mathsf T}$. A
matrix $xx^{\mathsf T}/(x\cdot x)$ is idempotent. The products $P_\gamma P_Z$, $P_ZP_\gamma$ and
$M^2P_\gamma$ contain the factor $m\cdot n=0$. $P_\gamma+P_Z=I$ because $n/\sqrt\Delta$ and
$m/\sqrt\Delta$ form an orthonormal basis. Over $\mathbb Q$ one can also check the four entries
directly. Finally $M_Z^2\cos^2\theta_W=\frac{v^2\Delta}{4}\cdot\frac{g^2}{\Delta}=M_W^2$. $\square$

Here $M_Z^2$, $M_W^2$ and $\rho$ are defined by these formulas. They are not derived from a
Lagrangian.

Lean: `lean4/RaveraDfmFiniteToContinuum.lean::weinberg_projectors_complete_orthogonal_idempotent`,
`lean4/RaveraDfmFiniteToContinuum.lean::ew_custodial_rho_eq_one`.

### 3.3 Anomaly polynomials as functions of the number of colours

DAG node: `DFM-SM-ANOMALY-NC-THREE`

**Proposition.** With one generation of hypercharges $Y_Q=\frac16$, $Y_u=\frac23$, $Y_d=-\frac13$,
$Y_L=-\frac12$, $Y_e=-1$ and $N_c$ colours (left-handed doublets counted twice, right-handed fields
with a minus sign):
$$\begin{aligned}
SU(3)^2U(1):&\quad 2Y_Q-Y_u-Y_d=0,\\
\text{grav}^2U(1):&\quad N_c(2Y_Q-Y_u-Y_d)+2Y_L-Y_e=0,\\
SU(2)^2U(1):&\quad N_cY_Q+Y_L=\tfrac{N_c-3}6,\\
U(1)^3:&\quad N_c(2Y_Q^3-Y_u^3-Y_d^3)+2Y_L^3-Y_e^3=\tfrac{3-N_c}4 .
\end{aligned}$$
The last two vanish exactly when $N_c=3$.

*Proof.* $2Y_Q-Y_u-Y_d=\frac13-\frac23+\frac13=0$, and $2Y_L-Y_e=-1+1=0$. Next,
$N_c/6-1/2=(N_c-3)/6$. For the cubic,
$2Y_Q^3-Y_u^3-Y_d^3=\frac1{108}-\frac8{27}+\frac1{27}=-\frac14$ and $2Y_L^3-Y_e^3=-\frac14+1=\frac34$,
so the total is $\frac{3-N_c}4$. $\square$

These are polynomial identities in the stated charges. The anomaly coefficients themselves come
from the standard triangle-diagram computation, which is not reproduced. The dossier prints the
cubic trace as $\frac34(3-N_c)$, which disagrees with the computation above; the value
$\frac{3-N_c}4$ is the correct one.

Lean: `lean4/RaveraDfmFiniteToContinuum.lean::sm_anomaly_polynomials_general_nc`,
`lean4/RaveraDfmFiniteToContinuum.lean::sm_all_four_anomalies_cancel_at_nc3_and_fail_at_nc1`.

### 3.4 Quark mixing: cycle count, rephasing invariance and two generations

DAG nodes: `DFM-CKM-CYCLE-COUNT` `DFM-JARLSKOG-QUARTET-INVARIANCE` `DFM-CABIBBO-CP-PHASE-ZERO`

Treat an $n\times n$ mixing matrix $v$ as a connection on the complete bipartite graph $K_{n,n}$,
with up-type and down-type quarks as vertices and $v_{ij}$ on the edge $ij$. Rephasing the
quark fields by unit complex numbers is a vertex dressing: $v_{ij}\mapsto u_iv_{ij}\bar d_j$.

**Proposition.** (i) $K_{n,n}$ has $n^2$ edges, a spanning tree has $2n-1$ of them, and the number
of independent cycles is $n^2-(2n-1)=(n-1)^2$. (ii) For $|u_i|=|d_j|=1$, the products
$v_{ij}\bar v_{il}$ and $v_{ij}\bar v_{kj}$ are invariant under rephasing row $i$ and column $j$
respectively. So the quartet $Q=v_{ij}v_{kl}\bar v_{il}\bar v_{kj}$ is invariant under every
rephasing. (iii) If $n=2$ and $v_{11}\bar v_{21}+v_{12}\bar v_{22}=0$ (orthogonal rows), then
$v_{11}v_{22}\bar v_{12}\bar v_{21}=-|v_{12}|^2|v_{22}|^2$ is real.

*Proof.* (i) A spanning tree of a connected graph on $V$ vertices has $V-1$ edges, here $2n-1$, and
each remaining edge closes one independent cycle. (ii) Rephasing row $i$ multiplies $v_{ij}$ and
$v_{il}$ by $u_i$, so $v_{ij}\bar v_{il}$ gains $u_i\bar u_i=1$. Columns are the same. In $Q$,
each row index and each column index occurs once unconjugated and once conjugated, so every
single-vertex rephasing cancels, and a general rephasing is a composite of these. (iii)
$v_{11}\bar v_{21}=-v_{12}\bar v_{22}$, so
$v_{11}v_{22}\bar v_{12}\bar v_{21}=(v_{11}\bar v_{21})(v_{22}\bar v_{12})=-v_{12}\bar v_{22}v_{22}\bar
v_{12}=-|v_{12}|^2|v_{22}|^2$. $\square$

$\operatorname{Im}Q$ is the Jarlskog invariant, and (iii) says it vanishes for two generations. The
further count, that unitarity leaves $(n-1)(n-2)/2$ CP phases among the $(n-1)^2$ cycle phases
($0,0,1,3$ for $n=1,2,3,4$), is the standard result and is not proved here.

Lean: `lean4/RaveraDfmFiniteToContinuum.lean::ckm_bipartite_dfm_parameter_count` (the identity
$n^2-(2n-1)=(n-1)^2$ and the four values),
`lean4/RaveraDfmFiniteToContinuum.lean::jarlskog_quartet_rephasing_dressing_invariance`
(single-vertex steps over $\mathbb Q(i)$),
`lean4/RaveraDfmFiniteToContinuum.lean::two_gen_cabibbo_artificial_cp_phase_zero`.

### 3.5 Boosts of the Minkowski plane

DAG node: `DFM-BOOST-PLANE-LEAN`

**Proposition.** For $\beta\in\mathbb Q$ with $\beta^2\neq1$, let
$\Lambda(\beta)=\frac1{1-\beta^2}\begin{pmatrix}1+\beta^2&2\beta\\2\beta&1+\beta^2\end{pmatrix}$ and
$\eta=\operatorname{diag}(1,-1)$. Then $\det\Lambda(\beta)=1$, $\Lambda(\beta)\Lambda(-\beta)=I$,
$\Lambda^{\mathsf T}\eta\Lambda=\eta$, and $e^{\mathsf T}\eta e$ is unchanged when a frame $e$ is
replaced by $\Lambda(-\beta)e$.

*Proof.* Write $\Lambda=\begin{pmatrix}p&q\\q&p\end{pmatrix}$ with $p=\frac{1+\beta^2}{1-\beta^2}$
and $q=\frac{2\beta}{1-\beta^2}$. Then $p^2-q^2=\frac{(1+\beta^2)^2-4\beta^2}{(1-\beta^2)^2}=1$.
This is $\det\Lambda$. It is also the diagonal of $\Lambda(\beta)\Lambda(-\beta)$, whose
off-diagonal entries are $-pq+qp=0$. Finally
$\Lambda^{\mathsf T}\eta\Lambda=\begin{pmatrix}p^2-q^2&0\\0&q^2-p^2\end{pmatrix}=\eta$, and
$(\Lambda e)^{\mathsf T}\eta(\Lambda e)=e^{\mathsf T}(\Lambda^{\mathsf T}\eta\Lambda)e$. $\square$

With $\beta=\tanh(\chi/2)$ this is the boost of rapidity $\chi$. The rational parametrization
reaches every boost with rational $\cosh\chi$ and $\sinh\chi$. The four-dimensional statements and
the velocity-addition law are not in Lean.

Lean: `lean4/RaveraDfmFiniteToContinuum.lean::lorentz_boost_preserves_minkowski_and_det_one`,
`lean4/RaveraDfmFiniteToContinuum.lean::cartan_regge_tetrad_dressed_metric_invariance`.
