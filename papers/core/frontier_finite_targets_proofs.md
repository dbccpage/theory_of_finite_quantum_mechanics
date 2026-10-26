<div align="center">

# Finite Targets from Constructor Theory, Causal QFT, Stabilizer Holography, Spin Networks and Observer Presheaves: Proofs

**Author:** Jeremy H. Carroll

**Date:** 2026-10-26

**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)

</div>

## Introduction

The derivation DAG (`dag/derivation_dag.json`) has frontier branches in which a programme from the
literature is reduced to a finite statement that can be checked exactly. The record derivations are
in `dag/derivations/30_constructor_theory/`, `31_causal_qft/`, `32_ads_cft/` and
`33_loop_quantum_gravity/`, and the observer-presheaf results come from the LGGR note recorded
under `sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/`.
This note gives written proofs for the frontier nodes recorded as proved in Lean. Each section
states one result, proves it, and names the Lean declarations that check it. The DAG identifier
is on the line beginning *DAG node*.

Each result is a finite statement. None of them is a statement about the continuum theory it is
named after. Where the prose argument covers more than the Lean check, the text says which part is
checked in Lean and which part is proved only here. Where a step depends on an external theorem,
the theorem is named and is not claimed as proved in this repository.

Four frontier nodes recorded as proved in Lean have no section here, because their Lean content
is an exhaustive check over a finite table and there is no shorter argument to write down. They
are `ADS-HAPPY-ENTROPY-MINCUT-TARGET` (380 boundary intervals of a hand-entered stabilizer),
`LQG-6J-EXACT-AND-PENTAGON-TARGET` (Racah sums over admissible tuples), `LQG-PR-ALLOWED-REGION-TARGET`
(the sign of a Gram determinant on 13,691 tuples) and `LQG-TV-LEVEL2-PENTAGON-TARGET` (a transcribed
table at level 2). Their DAG statements list what the enumeration covers and what it does not.

---

## 1. Constructor theory

### 1.1 Separating two attributes through a report map

DAG node: `CT-FINITE-DISTINGUISHABILITY-REPORT-FIBERS`

**Proposition.** Let $X$ be a finite set, $q:X\to R$ a map, and $A,B\subseteq X$. There is a
function $f:R\to\{0,1\}$ with $f(q(a))=0$ for all $a\in A$ and $f(q(b))=1$ for all $b\in B$ if and
only if $q(A)\cap q(B)=\varnothing$. When this holds, the indicator of $B$ on $A\cup B$ is constant
on the fibres of $q$.

*Proof.* If such an $f$ exists and $r\in q(A)\cap q(B)$, then $r=q(a)=q(b)$ with $a\in A$, $b\in B$,
and $0=f(r)=1$, a contradiction. Conversely, if the images are disjoint, let $f$ be the indicator
of $q(B)$. Then $f(q(b))=1$ on $B$, and for $a\in A$ the value $q(a)$ is not in $q(B)$, so
$f(q(a))=0$. For the last claim, take $x,y\in A\cup B$ with $q(x)=q(y)$. Disjointness of the
images forbids $x\in A$, $y\in B$ and the reverse, so $x$ and $y$ lie in the same one of the two
sets and the indicator of $B$ takes the same value on both. $\square$

Lean checks both directions over `Finset` for arbitrary types with decidable equality on $R$, the
fibre-constancy statement, and an independent bitmask check of the equivalence for $|X|\le4$ and
$|R|\le3$. The proposition is the deterministic part of the constructor-theoretic notion of
distinguishable attributes. Accuracy, repeatability and the existence of a constructor are not
modelled.

Lean: `lean4/FrontierDistinguishability.lean::FrontierDistinguishability.separatedByTask_imp_disjoint_image`,
`lean4/FrontierDistinguishability.lean::FrontierDistinguishability.disjoint_image_imp_separatedByTask`,
`lean4/FrontierDistinguishability.lean::FrontierDistinguishability.separatedByTask_iff_disjoint_image`,
`lean4/FrontierDistinguishability.lean::FrontierDistinguishability.fiberConstant_indicator_of_disjoint_image`,
`lean4/FrontierDistinguishability.lean::FrontierDistinguishability.exhaustive_distinguishability_check_le4_le3`.

### 1.2 Which sets of Pauli eigenstates can be cloned

DAG node: `CT-QUBIT-NO-CLONING-FINITE-TARGET`

Write $|0\rangle,|1\rangle$, $|\pm\rangle$ and $|\pm i\rangle$ for the six eigenstates of $Z$, $X$
and $Y$, and $\psi$ for the projector onto $|\psi\rangle$. All entries lie in $\mathbb Q(i)$.

**Proposition.** (a) For each Pauli basis $\{e_0,e_1\}$ the measure-and-prepare map
$\rho\mapsto\operatorname{tr}(e_0\rho)\,e_0\otimes e_0+\operatorname{tr}(e_1\rho)\,e_1\otimes e_1$
sends $e_0$ and $e_1$ to their clones. (b) No additive map $\Phi$ on $2\times2$ matrices satisfies
$\Phi(\psi)=\psi\otimes\psi$ for all four of $|0\rangle,|1\rangle,|+\rangle,|-\rangle$. (c) The
squared overlap $|\langle s|t\rangle|^2$ of two of the six states is $1$, $0$ or $\tfrac12$
according as they are equal, antipodal or neither. A subset of the six states is pairwise equal or
orthogonal if and only if it is empty, a singleton or an antipodal pair, so there are exactly ten
such subsets and the maximal ones are the three bases.

*Proof.* (a) $\operatorname{tr}(e_ie_j)=\delta_{ij}$, so the map sends $e_i$ to $e_i\otimes e_i$.
(b) Both bases resolve the identity: $|0\rangle\langle0|+|1\rangle\langle1|=I=|+\rangle\langle+|+|-\rangle\langle-|$.
An additive cloner would give
$|00\rangle\langle00|+|11\rangle\langle11|=\Phi(I)=|{+}{+}\rangle\langle{+}{+}|+|{-}{-}\rangle\langle{-}{-}|$.
The left side has entry $0$ in position $(00,11)$. On the right, $|{+}{+}\rangle=\tfrac12(1,1,1,1)$
and $|{-}{-}\rangle=\tfrac12(1,-1,-1,1)$ each contribute $\tfrac14$ there, giving $\tfrac12$.
(c) The overlaps follow from the coordinates: states in the same basis have overlap $1$ or $0$,
and states in different bases have amplitudes of modulus $1/\sqrt2$ against each other. A subset
that contains two distinct non-antipodal states has a pair with overlap $\tfrac12$. Any three of
the six states contain such a pair, because each state has only one antipode. So the admissible
subsets are $\varnothing$, the six singletons and the three antipodal pairs, ten in all. $\square$

The connection with cloning goes through one inequality. If a channel $\Phi$ clones pure states
$\psi$ and $\varphi$ with overlap $x=\operatorname{tr}(\psi\varphi)\in[0,1]$, the output overlap is
$x^2$, and monotonicity of fidelity under channels would give $x\le x^2$, so $x(x-1)\ge0$ and
$x\in\{0,1\}$. Lean checks this last step of arithmetic. Monotonicity of fidelity is an external
theorem and is a hypothesis of the Lean lemma.

Not proved in Lean, and not proved here: complete positivity of the three measure-and-prepare maps
(they are entanglement-breaking channels in the standard sense) and trace preservation of the
$X$ and $Y$ maps (only the $Z$ map is checked). In Lean "cloneable" in (c) is defined as pairwise
equal or orthogonal. The equivalence with "some channel clones every state of the subset" uses (a)
in one direction and fidelity monotonicity in the other, and is not a Lean theorem.

Lean: `lean4/FrontierNoCloning.lean::FrontierNoCloning.cloneZ_trace_preserving`,
`lean4/FrontierNoCloning.lean::FrontierNoCloning.cloneZ_clones_Z_attribute`,
`lean4/FrontierNoCloning.lean::FrontierNoCloning.cloneX_clones_X_attribute`,
`lean4/FrontierNoCloning.lean::FrontierNoCloning.cloneY_clones_Y_attribute`,
`lean4/FrontierNoCloning.lean::FrontierNoCloning.pauli_Z_X_completeness_identity`,
`lean4/FrontierNoCloning.lean::FrontierNoCloning.cloning_defect_ZX_off_diagonal_half`,
`lean4/FrontierNoCloning.lean::FrontierNoCloning.no_additive_cloner_for_Z_union_X`,
`lean4/FrontierNoCloning.lean::FrontierNoCloning.fidelity_monotonicity_forces_zero_or_one`,
`lean4/FrontierNoCloning.lean::FrontierNoCloning.pauli_overlap_idempotent_iff_equal_or_antipodal`,
`lean4/FrontierNoCloning.lean::FrontierNoCloning.exhaustive_64_subsets_clonability_classification`.

### 1.3 A diagonal phase that entangles

DAG node: `CT-ENTANGLING-PHASE-FINITE-TARGET`

For $u\in\mathbb Q(i)$ let $\psi_u=\tfrac12(1,1,1,u)$ in the basis $|00\rangle,|01\rangle,|10\rangle,|11\rangle$,
with coefficient matrix $M_u=\tfrac12\begin{pmatrix}1&1\\1&u\end{pmatrix}$. A two-qubit vector is a
product when its coefficient matrix is $(a_ib_j)$.

**Proposition.** (a) $\det M_u=(u-1)/4$, and $\psi_u$ is a product if and only if $u=1$. (b) With
the squared concurrence defined as $4|\det M|^2$, $\psi_u$ has squared concurrence $|u-1|^2/4$; at
$u=(3+4i)/5$, which has modulus $1$, the value is $1/5$. (c) For all $2\times2$ matrices $A,B$,
$\det(AMB^{\mathsf T})=\det A\,\det M\,\det B$, so local operations map a product vector to a
product vector. The phase gate $\operatorname{diag}(1,1,1,u)$ maps the product vector $\psi_1$ to
$\psi_u$.

*Proof.* (a) $\det M_u=\tfrac14(u-1)$. A product matrix $(a_ib_j)$ has determinant
$a_0b_0a_1b_1-a_0b_1a_1b_0=0$, so a product $\psi_u$ forces $u=1$. At $u=1$, $M_1=(a_ib_j)$ with
$a=(1,1)$ and $b=(\tfrac12,\tfrac12)$.
(b) $4|\det M_u|^2=4|u-1|^2/16$. At $u=(3+4i)/5$, $u-1=(-2+4i)/5$ and $|u-1|^2=20/25=4/5$.
(c) $AMB^{\mathsf T}$ is the coefficient matrix of $(A\otimes B)\psi$, and the determinant is
multiplicative, so $\det M=0$ is preserved. The phase gate multiplies the last coordinate of
$\psi_1$ by $u$. $\square$

The phase gate is a single nonlocal diagonal unitary, so (a) to (c) show that it creates
entanglement which no local operation can create from a product vector. Not proved: statement (d)
of the record, a linear functional on density matrices that separates $\psi_u$ from all mixtures of
products. The Lean quantity $|\det M|^2$ vanishes on product vectors, but it is quadratic in the
amplitudes and is not shown to vanish on mixtures. The physical inference from entanglement of two
probes to a non-classical mediator is imported and is not part of this node.

Lean: `lean4/FrontierEntanglingPhase.lean::FrontierEntanglingPhase.det_M_u`,
`lean4/FrontierEntanglingPhase.lean::FrontierEntanglingPhase.productState2_det_zero`,
`lean4/FrontierEntanglingPhase.lean::FrontierEntanglingPhase.psi_u_isProduct_iff`,
`lean4/FrontierEntanglingPhase.lean::FrontierEntanglingPhase.concurrenceSq_M_u`,
`lean4/FrontierEntanglingPhase.lean::FrontierEntanglingPhase.u_pythagorean_unit_and_concurrence`,
`lean4/FrontierEntanglingPhase.lean::FrontierEntanglingPhase.det2_local_action`,
`lean4/FrontierEntanglingPhase.lean::FrontierEntanglingPhase.local_op_cannot_raise_product_rank`,
`lean4/FrontierEntanglingPhase.lean::FrontierEntanglingPhase.diag_phase_maps_psi1_to_psiu`.

---

## 2. Causal order and local algebras

Throughout, $P$ is a finite strict partial order on $\{0,\dots,n-1\}$ (an irreflexive transitive
relation $<$). Two points are *spacelike* when they are distinct and neither precedes the other.

### 2.1 The spacelike relation

DAG node: `CQFT-FINITE-STRICT-POSET-SPACELIKE`

**Proposition.** Spacelike separation is symmetric and irreflexive and need not be transitive. On
the poset $N_4$ with relations $0<2$, $1<2$, $1<3$, the points $0$ and $3$ are spacelike, $3$ and $2$
are spacelike, and $0<2$.

*Proof.* The definition is symmetric in the two points and requires them to be distinct. In $N_4$
no relation involves both $0$ and $3$, or both $3$ and $2$. $\square$

Lean also decides the small examples $C_1$ ($0<1$, $0<2$) and the diamond $C_2$, shows that $C_1$
and its dual are different orders, and checks two entries of the Möbius function: $\mu(1,2)=0$ on
$C_1$, since $\mu$ vanishes off comparable pairs, and $\mu(0,3)=1$ on $C_2$, since
$\mu(0,3)=-(\mu(0,0)+\mu(0,1)+\mu(0,2))=-(1-1-1)$. In this file the Möbius table for $C_2$ is
checked entry by entry; the recursion is stated in §2.6.

Lean: `lean4/CausalOrder.lean::spacelike_symm`, `lean4/CausalOrder.lean::spacelike_irrefl`,
`lean4/CausalOrder.lean::c1_spacelike_1_2`, `lean4/CausalOrder.lean::c1_spacelike_symm_irrefl`,
`lean4/CausalOrder.lean::c2_causal_0_3`, `lean4/CausalOrder.lean::n4_spacelike_not_transitive`,
`lean4/CausalOrder.lean::spacelike_not_transitive`, `lean4/CausalOrder.lean::order_independence_witness`,
`lean4/CausalOrder.lean::c1_mu_spacelike_vanishes`, `lean4/CausalOrder.lean::c2_mu_top_bottom`.

### 2.2 Isotony and locality for site-factorized operators

DAG node: `CQFT-FINITE-POSET-NET-TARGET`

Put a copy of a monoid $M$ at each point of $P$ (for qubits, $M$ is the $2\times2$ matrices). A
site-factorized operator is a function $A:P\to M$, multiplied sitewise. It is *localized* in
$O\subseteq P$ when $A_x=1$ for every $x\notin O$.

**Proposition.** (a) If $O_1\subseteq O_2$, an operator localized in $O_1$ is localized in $O_2$.
(b) If every point of $O_1$ is spacelike to every point of $O_2$, then $O_1\cap O_2=\varnothing$ and
any $A$ localized in $O_1$ commutes with any $B$ localized in $O_2$.

*Proof.* (a) A point outside $O_2$ is outside $O_1$. (b) A common point $x$ would be spacelike to
itself, which irreflexivity forbids. At each site $x$, at least one of $A_x$, $B_x$ is $1$, so
$A_xB_x=B_xA_x$. $\square$

The Lean statement is for elementary tensors only, with $M$ an arbitrary monoid. Not proved in
Lean: the extension to the full matrix algebras $\mathcal A(O)$, which follows by bilinearity of the
product because $\mathcal A(O)$ is spanned by elementary tensors localized in $O$, and the
instantiation at $2\times2$ matrices. The net has no dynamics, so the commutation in (b) comes from
disjoint supports and not from causal propagation. This is the finite form of the isotony and
locality axioms of Haag and Kastler, and nothing more.

Lean: `lean4/FrontierPosetNet.lean::FrontierPosetNet.isotony`,
`lean4/FrontierPosetNet.lean::FrontierPosetNet.disjoint_of_all_spacelike`,
`lean4/FrontierPosetNet.lean::FrontierPosetNet.locality_commute_of_spacelike`,
`lean4/FrontierPosetNet.lean::FrontierPosetNet.spacelike_not_transitive_on_posetN`,
`lean4/CausalOrder.lean::spacelike_symm`, `lean4/CausalOrder.lean::spacelike_irrefl`.

### 2.3 Product tables do not signal

DAG node: `CQFT-NO-SIGNALLING-PRODUCT-LEAN`

**Proposition.** Let $P(a,b\mid x,y)=P_A(a\mid x)\,P_B(b\mid y)$ with $\sum_bP_B(b\mid y)=1$ for each
$y$. Then $\sum_bP(a,b\mid x,y)=P_A(a\mid x)$ for every $y$. The table with one outcome $a$ for the
first party, $a=y$, has a marginal that depends on $y$.

*Proof.* $\sum_bP_A(a\mid x)P_B(b\mid y)=P_A(a\mid x)\sum_bP_B(b\mid y)=P_A(a\mid x)$. In the second
table the probability of $a=\text{true}$ is $1$ at $y=\text{true}$ and $0$ at $y=\text{false}$. $\square$

Lean states this for natural-number weights over a listed outcome set. The quantum statement, that
commuting local measurements give setting-independent marginals, is not in this file.

Lean: `lean4/NoSignallingCore.lean::product_noSignalling`, `lean4/NoSignallingCore.lean::marginalA_product`,
`lean4/NoSignallingCore.lean::sig_signals`.

### 2.4 Cyclic and separating vectors in finite dimension

DAG node: `CQFT-RS-FINITE-CYCLICITY-TARGET`

A vector of $\mathcal H_A\otimes\mathcal H_{A^c}$ is a $d_A\times d_B$ amplitude matrix $\Omega$ over
a semiring. Operators on $\mathcal H_A$ act by $\Omega\mapsto X\Omega$ and operators on
$\mathcal H_{A^c}$ by $\Omega\mapsto\Omega Y$. $\Omega$ is *cyclic* for the $A$ operators when every
$d_A\times d_B$ matrix is some $X\Omega$, and *separating* for the $A^c$ operators when $\Omega Y=0$
implies $Y=0$.

**Proposition.** (a) If $L\Omega=I_{d_B}$ for some $L$, then $\Omega$ is cyclic and separating.
(b) If $d_B\le d_A$ and $\Omega$ is cyclic, such an $L$ exists. (c) If $\Omega v=0$ for a nonzero
vector $v$, then $\Omega$ is not separating.

*Proof.* (a) Given $\Psi$, take $X=\Psi L$; then $X\Omega=\Psi(L\Omega)=\Psi$. If $\Omega Y=0$, then
$Y=L\Omega Y=0$. (b) Choose an injection $e:\{1..d_B\}\to\{1..d_A\}$ and let $T$ be the matrix with
$T_{e(j),j}=1$ and zeros elsewhere. Cyclicity gives $X$ with $X\Omega=T$. The rows $e(1),\dots,e(d_B)$
of $X$ form $L$, and $(L\Omega)_{kj}=T_{e(k),j}=\delta_{kj}$ by injectivity. (c) Let $Y$ have every
column equal to $v$. Then $\Omega Y=0$ and $Y\ne0$. $\square$

On three qubits Lean exhibits, for $|000\rangle$, GHZ and W, a nonzero kernel vector of every
single-site unfolding ($2\times4$), so none of them is separating for the two-site complement, and
integer left inverses of every two-site unfolding ($4\times2$) of GHZ and W, so these are cyclic for
each pair of sites. Not proved in Lean: separating implies a left inverse, so the three conditions
are not shown equivalent; the identification of a left inverse with full rank of the reduced state;
"not cyclic" for the single-site cases, where (b) does not apply because $d_A=2<d_B=4$; and "not
cyclic" for $|000\rangle$ on pairs, where Lean exhibits a zero column but does not derive the
conclusion. The relation to the Reeh–Schlieder theorem is an analogy. Finite dimension has no
translations and no spectrum condition.

Lean: `lean4/FrontierRsCyclicity.lean::FrontierRsCyclicity.cyclic_of_fullComplementaryRank`,
`lean4/FrontierRsCyclicity.lean::FrontierRsCyclicity.fullComplementaryRank_of_cyclic`,
`lean4/FrontierRsCyclicity.lean::FrontierRsCyclicity.separating_of_fullComplementaryRank`,
`lean4/FrontierRsCyclicity.lean::FrontierRsCyclicity.not_separating_of_right_kernel`,
`lean4/FrontierRsCyclicity.lean::FrontierRsCyclicity.single_site_not_cyclic_prod_ghz_w`,
`lean4/FrontierRsCyclicity.lean::FrontierRsCyclicity.pair_of_sites_cyclic_for_GHZ3_and_W3_not_prod3`.

### 2.5 Ordered products along linear extensions

DAG node: `CQFT-ORDERED-PRODUCT-LINEAR-EXTENSION-TARGET`

Let $A_x$ ($x\in P$) be elements of a monoid with $A_xA_y=A_yA_x$ whenever $x$ and $y$ are
spacelike. For a listing $L=(x_1,\dots,x_n)$ put $\prod_LA=A_{x_1}\cdots A_{x_n}$.

**Proposition.** (a) Swapping two adjacent spacelike entries of $L$ does not change $\prod_LA$,
and neither does any chain of such swaps. (b) Any two linear extensions of $P$ are joined by a
chain of adjacent spacelike swaps through linear extensions. Hence $\prod_LA$ is the same for all
linear extensions $L$.

*Proof.* (a) $\prod_{p\,xy\,q}A=(\prod_pA)A_xA_y(\prod_qA)=(\prod_pA)A_yA_x(\prod_qA)$, and a chain
is handled by induction on its length. (b) Let $L$ and $L'$ be linear extensions and let $y$ be the
first entry of $L'$. Nothing precedes $y$ in $P$, since $L'$ is a linear extension. Let $z$ be an
entry before $y$ in $L$. Then $y<z$ is excluded because $L$ is a linear extension, and $z<y$ is
excluded because $y$ is minimal, so $z$ and $y$ are spacelike. Moving $y$ to the front of $L$ by
adjacent swaps therefore uses only spacelike swaps, and each intermediate listing is still a
linear extension. Both listings now start with $y$. Removing $y$ leaves two linear extensions of
$P\setminus\{y\}$, and induction on $|P|$ finishes the argument. $\square$

Lean checks (a) in general. Part (b) is proved here and is not a Lean theorem. Lean exhibits the
connecting swap only for the diamond $C_2$, whose two linear extensions $[0,1,2,3]$ and $[0,2,1,3]$
differ by swapping $1$ and $2$, and counts the five linear extensions of $N_4$. With Pauli matrices
at the spacelike points $1,2$ of $C_2$, the two ordered products agree for $Z,Z$ and differ by the
sign $-1$ for $X,Z$, which shows that the commutation hypothesis is needed. The relation to the
Epstein–Glaser construction is an analogy.

Lean: `lean4/FrontierLinearExtension.lean::FrontierLinearExtension.orderedProd_append`,
`lean4/FrontierLinearExtension.lean::FrontierLinearExtension.orderedProd_eq_of_adjSpacelikeSwap`,
`lean4/FrontierLinearExtension.lean::FrontierLinearExtension.orderedProd_eq_of_spacelikeSwapChain`,
`lean4/FrontierLinearExtension.lean::FrontierLinearExtension.linear_extensions_of_C2_and_N`,
`lean4/FrontierLinearExtension.lean::FrontierLinearExtension.c2_extensions_connected_by_swap`,
`lean4/FrontierLinearExtension.lean::FrontierLinearExtension.c2_pauli_commuting_and_anticommuting_products`.

### 2.6 Ordering fractions, the grid, and covering relations

DAG node: `CQFT-MYRHEIM-MEYER-ORDERING-FRACTION-TARGET`

The ordering fraction of a poset with $N$ points and $R$ related pairs is $r=2R/(N(N-1))$.

**Proposition.** (i) The $n\times n$ grid with the componentwise order has
$R(n)=\bigl(n(n+1)/2\bigr)^2-n^2$ related pairs, $4R(n)=n^2(n-1)(n+3)$, and
$r=(n+3)/(2(n+1))=\tfrac12+1/(n+1)$ for $n\ge2$. (ii) If $E$ is a subrelation of $<$ such that every
related pair is in $E$ or has an element strictly between, then every covering pair is in $E$.

*Proof.* (i) A pair $(a,b)\le(c,d)$ in the grid is a choice of $a\le c$ and of $b\le d$
independently, and each coordinate has $n(n+1)/2$ choices. Removing the $n^2$ equal pairs leaves
$R(n)$. Then $4R(n)=n^2(n+1)^2-4n^2=n^2\bigl((n+1)^2-4\bigr)=n^2(n-1)(n+3)$, and with $N=n^2$,
$r=\dfrac{n^2(n-1)(n+3)/2}{n^2(n^2-1)}=\dfrac{n+3}{2(n+1)}$. (ii) A covering pair $x\lessdot y$ is
related and has nothing strictly between, so it must lie in $E$. $\square$

Lean checks the algebra of (i) on the count $R(n)$, which in Lean is a definition and not derived
from a poset. The counting argument above is proved here and not in Lean. At $n=2$ the grid is the
diamond, and $r=5/6$ agrees with the value Lean computes from the relation table of $C_2$ (five
related pairs among four points). Lean also checks (ii), the link counts $2$ for $C_1$ and $4$ for
$C_2$, the Möbius recursions on both, and a nearest-dimension selector against the Myrheim–Meyer
values $f(1),\dots,f(4)=1,\tfrac12,\tfrac8{35},\tfrac1{10}$ on six inputs. Those four values are
entered as a table; their derivation from the Gamma-function formula of Myrheim and Meyer (see
Sorkin, arXiv:gr-qc/0309009, §7) is external. The grid is a lattice, not a sprinkling, and a
dimension estimate on a small poset carries no statement about a manifold. Not proved: that the
covering relation generates the order and is the smallest such relation.

Lean: `lean4/FrontierMyrheimMeyer.lean::FrontierMyrheimMeyer.gridStrictPairs_factorization`,
`lean4/FrontierMyrheimMeyer.lean::FrontierMyrheimMeyer.grid_ordering_fraction_closed_form`,
`lean4/FrontierMyrheimMeyer.lean::FrontierMyrheimMeyer.grid_ordering_fraction_minus_half`,
`lean4/FrontierMyrheimMeyer.lean::FrontierMyrheimMeyer.grid_values_2_to_6_and_c2_agreement`,
`lean4/FrontierMyrheimMeyer.lean::FrontierMyrheimMeyer.myrheim_meyer_nearest_dimension_checks`,
`lean4/FrontierMyrheimMeyer.lean::FrontierMyrheimMeyer.covers_subset_of_generating_subrelation`,
`lean4/FrontierMyrheimMeyer.lean::FrontierMyrheimMeyer.hasse_links_and_mobius_recursions_C1_C2`.

---

## 3. The five-qubit code

Pauli operators are taken modulo phase, so an $n$-qubit Pauli operator is a vector in
$\mathbb F_2^{2n}$ and commutation is the symplectic form. The $[[5,1,3]]$ code of Laflamme, Miquel,
Paz and Zurek has stabilizer $S$ generated by $XZZXI$ and its cyclic shifts $IXZZX$, $XIXZZ$,
$ZXIXZ$, with logical operators $\bar X=XXXXX$ and $\bar Z=ZZZZZ$. The normalizer $N(S)$ is
$S\cup\bar XS\cup\bar ZS\cup\bar YS$, of order $64$.

We use the standard stabilizer dictionary. For a stabilizer state on $n$ qubits with stabilizer
group $G$ of order $2^n$, the state is $\rho=2^{-n}\sum_{g\in G}g$. Partial trace over the complement
of $A$ kills every non-identity Pauli factor there, so
$\rho_A=2^{-|A|}\sum_{g\in G_A}g|_A$, where $G_A$ is the subgroup supported in $A$, and
$S(\rho_A)=|A|-\log_2|G_A|$. This dictionary is textbook material and is not formalised on density
matrices in this repository.

### 3.1 The six-qubit perfect tensor

DAG node: `ADS-FIVE-QUBIT-PERFECT-TENSOR-TARGET`

The Choi state of the code is the six-qubit stabilizer state $G$ generated by $g\otimes I$ for the
four generators $g$, and by $\bar X\otimes X$ and $\bar Z\otimes Z$.

**Proposition.** (i) The six generators commute and generate $64$ elements, with weight
distribution $1,45,18$ in weights $0,4,6$. (ii) Hence every marginal on at most three legs is
maximally mixed, and every $3|3$ cut has entropy $3$ bits. (iii) Every nontrivial logical operator
of the code has weight at least $3$.

*Proof.* (i) is a finite check, carried out in Lean. (ii) If $|A|\le3$, a non-identity element of
$G$ supported in $A$ would have weight at most $3$, which (i) excludes. So $G_A=\{I\}$ and
$\rho_A=2^{-|A|}I$; for $|A|=3$ this gives $S(A)=3$. (iii) A nontrivial logical operator $L$ lies in
one of the cosets $\bar XS$, $\bar ZS$, $\bar YS$, and then $L\otimes P\in G$ for the corresponding
reference Pauli $P\in\{X,Z,Y\}$. That element has weight $\operatorname{wt}(L)+1\ge4$, so
$\operatorname{wt}(L)\ge3$. $\square$

Lean checks (i) by enumeration, the triviality of $G_A$ on all twenty $3|3$ cuts, and the minimum
weight $3$ of the $48$ nontrivial logical operators by enumeration of the normalizer. The argument in
(iii) derives the lower bound from (i) without that enumeration. The reading of weights and local
subgroups as marginals and entropies is the dictionary above. A stabilizer computation on six qubits
is not a statement about AdS/CFT.

Lean: `lean4/FrontierFiveQubitPerfectTensor.lean::FrontierFiveQubitPerfectTensor.choi_generators_commute_and_group_order_64`,
`lean4/FrontierFiveQubitPerfectTensor.lean::FrontierFiveQubitPerfectTensor.choi_perfect_tensor_weight_distribution`,
`lean4/FrontierFiveQubitPerfectTensor.lean::FrontierFiveQubitPerfectTensor.all_twenty_3_3_bipartitions_maximal_entropy`,
`lean4/FrontierFiveQubitPerfectTensor.lean::FrontierFiveQubitPerfectTensor.five_qubit_logical_minimum_weight_3`.

### 3.2 Reconstruction of logical operators on three qubits

DAG node: `ADS-LOGICAL-RECONSTRUCTION-TARGET`

**Proposition.** (a) No nontrivial logical operator is supported on two qubits, and every
non-identity Pauli operator of weight at most $2$ anticommutes with some generator of $S$. (b) Each
of the ten three-qubit subsets $T$ supports a representative of each of the three nontrivial logical
classes.

*Proof.* (a) A logical operator supported on two qubits has weight at most $2$, which §3.1 (iii)
excludes. Every non-identity element of $S$ has weight $4$ (it is $g\otimes I$ in the Choi group of
§3.1), so a non-identity Pauli $E$ of weight at most $2$ is not in $S$ and, by the first claim, not
in $N(S)$. Not lying in the normalizer means anticommuting with some element of $S$, hence with some
generator. (b) Let $Q$ be the complementary pair, and restrict $S$ to $Q$: the map
$s\mapsto s|_Q$ lands in the $16$-element Pauli group of $Q$, a symplectic space of dimension $4$.
If a Pauli operator $E$ on $Q$ commuted with every $s|_Q$, then $E\otimes I_T$ would commute with
all of $S$ and lie in $N(S)$ with weight at most $2$, so $E=I$ by (a). The symplectic complement of
the image $S|_Q$ is therefore zero, so $S|_Q$ is the whole Pauli group of $Q$. Given a logical
operator $L$, choose $s\in S$ with $s|_Q=L|_Q$. Then $Ls$ is in the same logical class and acts as
the identity on $Q$, so it is supported on $T$. $\square$

This is the cleaning lemma for a code of distance $3$. Lean checks (a) on all $105$ low-weight
errors and all ten pairs, and (b) on all ten triples and three classes, by enumeration. Part (a) is
the Knill–Laflamme condition for erasure of two qubits. The identification with bulk operator
reconstruction in AdS/CFT (Almheiri, Dong and Harlow, arXiv:1411.7041) is the imported picture of
the source.

Lean: `lean4/FrontierLogicalReconstruction.lean::FrontierLogicalReconstruction.every_triple_reconstructs_all_three_logical_classes`,
`lean4/FrontierLogicalReconstruction.lean::FrontierLogicalReconstruction.no_pair_supports_any_nontrivial_logical_class`,
`lean4/FrontierLogicalReconstruction.lean::FrontierLogicalReconstruction.two_qubit_erasure_detectable_all_105`.

---

## 4. Spin-network area

### 4.1 Degeneracy of the area spectrum for small puncture sets

DAG node: `LQG-AREA-SPECTRUM-EXACT-TARGET`

The dimensionless area of a set of punctures with spins $j$ is $\sum\sqrt{j(j+1)}$. With twice-spin
$k=2j$, $j(j+1)=k(k+2)/4$. For $k=1,\dots,6$ the terms are $\tfrac{\sqrt3}2$, $\sqrt2$,
$\tfrac{\sqrt{15}}2$, $\sqrt6$, $\tfrac{\sqrt{35}}2$, $2\sqrt3$, since
$k(k+2)=3,8,15,24,35,48=3,\,2^2\cdot2,\,15,\,2^2\cdot6,\,35,\,4^2\cdot3$. In the formal
$\mathbb Q$-module with basis $\tfrac12(\sqrt2,\sqrt3,\sqrt6,\sqrt{15},\sqrt{35})$, a multiset with
$n_k$ punctures of twice-spin $k$ has the vector
$v=(2n_2,\ n_1+4n_6,\ 2n_4,\ n_3,\ n_5)$.

**Proposition.** (i) Among the $210$ multisets of at most four punctures with $k\le6$, the vectors
take $209$ distinct values, $208$ of them nonzero. (ii) The only collision is four punctures of spin
$\tfrac12$ against one puncture of spin $3$. (iii) For a single puncture the squared area
$k(k+2)/4$ is strictly increasing in $k$, with minimum $\tfrac34$ at $j=\tfrac12$.

*Proof.* The count of multisets of size at most $4$ from six labels is $\binom{6+4}{4}=210$. Two
multisets $n,n'$ with $v(n)=v(n')$ have $n_k=n'_k$ for $k=2,3,4,5$ and $n_1+4n_6=n'_1+4n'_6$. If
$n_6\ne n'_6$, say $n'_6=n_6+t$ with $t\ge1$, then $n_1=n'_1+4t\ge4$. The multiset $n$ has at most
four elements, so $n_1=4$, $t=1$, $n'_1=0$ and every other count of $n$ is $0$. Then $n'_6=1$ and the
shared counts are $0$, so $n=\{\tfrac12,\tfrac12,\tfrac12,\tfrac12\}$ and $n'=\{3\}$. If
$n_6=n'_6$, then $n=n'$. This gives (ii), and (i) follows: $210-1=209$ values. All coordinates are
non-negative and vanish only when every $n_k=0$, so only the empty multiset has the zero vector.
(iii) $k(k+2)$ is increasing for $k\ge1$ and equals $3$ at $k=1$. $\square$

The proof above is a general argument for the statement that Lean checks by enumeration. To pass
from the formal vectors to real areas one needs that $\sqrt2,\sqrt3,\sqrt6,\sqrt{15},\sqrt{35}$ are
linearly independent over $\mathbb Q$. That is a classical theorem on square roots of distinct
squarefree integers (Besicovitch, 1940) and is not a Lean theorem here. Also not proved: the minimum
area over sets of several punctures. The Immirzi parameter, the physical constant and the
gauge-invariance constraint on puncture lists are not part of the node.

Lean: `lean4/FrontierAreaSpectrum.lean::FrontierAreaSpectrum.casimir_squarefree_factorizations`,
`lean4/FrontierAreaSpectrum.lean::FrontierAreaSpectrum.spin3_equals_four_spin_half`,
`lean4/FrontierAreaSpectrum.lean::FrontierAreaSpectrum.area_spectrum_table_and_unique_degeneracy`,
`lean4/FrontierAreaSpectrum.lean::FrontierAreaSpectrum.smallest_nonzero_area_level_is_spin_half`,
`lean4/FrontierAreaSpectrum.lean::FrontierAreaSpectrum.single_puncture_area_sq_strictly_increasing`.

---

## 5. Observer presheaf

A finitely supported measure with natural-number weights is a list of (value, weight) pairs. Its
mass is the sum of the weights, and the pushforward along $f$ replaces each value $a$ by $f(a)$.

### 5.1 Pushforward is functorial

DAG node: `OPS-PUSHFORWARD-FUNCTOR-LEAN`

**Proposition.** $f_*$ satisfies $\mathrm{id}_*=\mathrm{id}$ and $(g\circ f)_*=g_*\circ f_*$, preserves
mass, and the weight of $f_*p$ at $b$ is the total weight of the entries of $p$ with $f(a)=b$.

*Proof.* Pushforward maps the list entrywise and leaves weights alone, so the first two identities
are the identity and composition laws of mapping a list, and mass, a sum of weights, is unchanged.
An entry of $f_*p$ has value $b$ exactly when the corresponding entry of $p$ has $f(a)=b$, which
gives the weight formula. $\square$

The LGGR note reads marginalisation of a context distribution as pushforward along a restriction
map, so these are the functor laws for the presheaf of distributions on the context poset (its
Lemma B2). That reading, rational weights, normalisation and the context poset are not Lean
statements.

Lean: `lean4/LggrFiniteResults.lean::LggrFiniteResults.push_id`,
`lean4/LggrFiniteResults.lean::LggrFiniteResults.push_comp`,
`lean4/LggrFiniteResults.lean::LggrFiniteResults.mass_push`,
`lean4/LggrFiniteResults.lean::LggrFiniteResults.weightAt_push`.

### 5.2 Parity cycles: holonomy, sections and joint measures

DAG nodes: `OPS-PARITY-HOLONOMY-LEAN` `IMPL-LGGR-FINITE-RESULTS-LEAN`

Take a cycle of length $n\ge1$ with edge parities $b_0,\dots,b_{n-1}\in\mathbb F_2$, and let
$h=b_0\oplus\cdots\oplus b_{n-1}$ be its holonomy. A *section* is an assignment
$g:\{0,\dots,n-1\}\to\mathbb F_2$ with $g_i\oplus g_{i+1}=b_i$ for every $i$, indices mod $n$.

**Proposition.** (a) A section exists if and only if $h=0$. (b) If $h=1$, no measure of positive
mass on assignments has every edge marginal supported on the pairs of parity $b_i$. (c) On the
triangle with all parities $1$, every assignment satisfies at most two of the three edge
constraints, so a measure of mass $m>0$ has total satisfied weight at most $2m<3m$. (d) The cycle
gate, which admits a pair (cycle, mass $M$) when $M=0$ or $h=0$, admits exactly when $M=0$ or a
section exists.

*Proof.* (a) If $g$ is a section, the sum of $g_i\oplus g_{i+1}$ around the cycle counts each $g_i$
twice, so $h=0$. Conversely, if $h=0$, set $g_0=0$ and $g_k=b_0\oplus\cdots\oplus b_{k-1}$ for
$0<k<n$. The constraints for $i<n-1$ hold by construction, and the last one reads
$g_{n-1}\oplus g_0=b_0\oplus\cdots\oplus b_{n-2}$, which equals $b_{n-1}$ because $h=0$. (b) A
positive-mass measure has an entry $g$ of positive weight. Its restriction to edge $i$ is a pair of
positive weight in the marginal, so the pair has parity $b_i$, and $g$ is a section, contradicting
(a). (c) For any $g$, the three parities $g_0\oplus g_1$, $g_1\oplus g_2$, $g_2\oplus g_0$ sum to $0$,
so an even number of them equal $1$, at most two. Summing over the entries of the measure gives the
bound. (d) Substitute (a) in the definition of the gate. $\square$

Part (c) is the dual certificate for the odd triangle: it bounds the satisfiable fraction by
$\tfrac23$. (a) and (b) are the clauses "a global section exists if and only if the holonomy is $0$"
and "holonomy $1$ forbids a positive-mass joint measure with parity-supported marginals" of
Proposition B6 of the LGGR note. Not in Lean: the arc-cover clause, the noncontextual fraction and
the Čech-cohomology reading of $h$. The node `IMPL-LGGR-FINITE-RESULTS-LEAN` records the whole Lean
file; its listed gaps (the $\ell^1$ defect and the LP dual in Rust, the link between the Lean gate and
the Rust gate, and Proposition II-open) are not covered by this section and remain open.

Lean: `lean4/LggrFiniteResults.lean::LggrFiniteResults.section_exists_iff_holonomy_zero`,
`lean4/LggrFiniteResults.lean::LggrFiniteResults.no_joint_measure_when_holonomy_one`,
`lean4/LggrFiniteResults.lean::LggrFiniteResults.totalSatWeight3_le_two_mul_mass`,
`lean4/LggrFiniteResults.lean::LggrFiniteResults.odd_triangle_lp_dual_defect_pos`,
`lean4/LggrFiniteResults.lean::LggrFiniteResults.lggrCycleGateAdmits_iff_section_or_zero_mass`.
