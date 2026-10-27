<div align="center">

# The Fermion Sign and Majorana Carriers: Proofs of the Finite Results

**Author:** Jeremy H. Carroll

**Date:** 2026-10-26

**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)

</div>

## Introduction

This note gives written proofs of the finite results of
[the_problem_of_the_fermion_sign.md](fsp/the_problem_of_the_fermion_sign.md),
[theory_of_finite_fsp.md](fsp/theory_of_finite_fsp.md) and
[the_majorana_problem.md](majorana/the_majorana_problem.md) that the derivation DAG
(`dag/derivation_dag.json`) records as proved in Lean. Each section states one result, proves it,
and names the Lean declarations that check it. The DAG identifier is on the line beginning
*DAG node*.

None of these results removes a sign problem, gives an efficient sampler, or establishes a
topological phase. They are exact statements about signed sums, sign switching, gauge-invariant
actions and cochain labels on declared finite carriers. Each section says what is not claimed.

---

## 1. Signed sums and sign switching

### 1.1 The switching normal form of an edge signing

DAG nodes: `FSP-SWITCHING-NORMAL-FORM` `IMPL-FSP-SWITCHING-NORMAL-FORM-NF002`

Let $G$ be a finite graph with vertex set $V$ and labelled edges $E$ (loops and parallel edges
allowed), with $c$ connected components. An edge signing is $s\colon E\to\mathbb F_2$. Switching
by $a\colon V\to\mathbb F_2$ sends $s$ to $s+\delta a$, where $(\delta a)(e)=a(u)+a(v)$ for
$e=\{u,v\}$. Fix a spanning forest $F$ with one root in each component; the edges of $E\setminus F$
are the chords.

**Theorem.** Let $p_s(v)$ be the sum of $s$ along the forest path from $v$ to its root, and
$N(s)=s+\delta p_s$. Then (i) $N(s)$ is switching equivalent to $s$ and vanishes on $F$;
(ii) $s$ and $t$ are switching equivalent if and only if $N(s)=N(t)$; (iii) the classes are in
bijection with $\mathbb F_2^{\,\text{chords}}$, so there are $2^{|E|-|V|+c}$ of them.

*Proof.* (i) $N(s)$ is a switch of $s$ by definition. For a forest edge $e$ from $v$ to its parent
$u$, $p_s(v)=p_s(u)+s(e)$, so $N(s)(e)=s(e)+p_s(u)+p_s(v)=0$. (ii) If $t=s+\delta a$, then along
each forest path $p_t(v)=p_s(v)+a(v)+a(r)$ with $r$ the root, and $\delta$ of the function
$v\mapsto a(v)+a(r_v)$ is $\delta a$ (the root term is constant on each component, and every edge
lies in one component). Hence $N(t)=t+\delta p_t=s+\delta a+\delta p_s+\delta a=N(s)$. Conversely,
$N(s)=N(t)$ makes $s$ and $t$ equivalent to a common signing. (iii) By (i) and (ii) a class is
determined by the values of its normal form on the chords. Every chord assignment occurs: extend it
by $0$ on $F$, and that signing is its own normal form because $p=0$. A spanning forest of a graph
with $c$ components has $|V|-c$ edges, so there are $|E|-|V|+c$ chords. $\square$

The value of $N(s)$ on a chord is the sum of $s$ around the chord's fundamental cycle, a
switching invariant. The normal form depends on the labelled graph and the chosen forest. It is
not a canonical form under graph isomorphism or under many-body basis changes, and nothing here
bears on sampling cost.

Lean: `lean4/SwitchingNormalForm.lean::normal_sound`, `lean4/SwitchingNormalForm.lean::same_class_iff`,
`lean4/SwitchingNormalForm.lean::numChord_identity`, `lean4/SwitchingNormalForm.lean::normalForms_length`,
`lean4/SwitchingNormalForm.lean::normalForms_nodup`, `lean4/SwitchingNormalForm.lean::mem_normalForms_iff`.
The development is in core Lean 4 without `Classical.choice`. The forest is given as a witness with
a depth function. `normalForms` lists the $2^{\text{chords}}$ normal forms without duplicates.

### 1.2 Meron flips: the orbit sign sum

DAG node: `FSP-MERON-CHARACTER-CANCELLATION`

**Proposition.** Let a configuration have $k$ clusters, each flagged as a meron or not, and let
flipping a set $S$ of clusters multiply the sign by $(-1)^{|S\cap M|}$, where $M$ is the set of
merons. Then $\sum_{S\subseteq[k]}(-1)^{|S\cap M|}$ is $0$ if $M\neq\emptyset$ and $2^k$ if
$M=\emptyset$.

*Proof.* The sum factorizes over clusters: $\prod_{i=1}^k(1+\varepsilon_i)$ with $\varepsilon_i=-1$
for a meron and $+1$ otherwise. A factor is $0$ exactly for a meron, and every factor is $2$ when
there is none. $\square$

This is the sign identity alone. Using it to drop meron sectors from a partition function also
requires every configuration in a flip orbit to have the same weight magnitude, and requires
observables to be orbit compatible. Those are separate hypotheses on the model.

Lean: `lean4/MeronCharacter.lean::meron_orbit_cancels`,
`lean4/MeronCharacter.lean::zero_meron_orbit_positive` and
`lean4/MeronCharacter.lean::compression_preserves_partition`, by induction on the
flag list with the orbit built by doubling, which is the same factorization.

### 1.3 Sign-reversing involutions

DAG nodes: `FSP-INVOLUTION-PAIR-CANCELLATION` `MAJ-GIN-INVOLUTION-PAIR-CANCEL`

**Proposition.** Let $C$ be a finite set with weights $w\colon C\to\mathbb N$ and signs
$\sigma\colon C\to\{\pm1\}$, and let $\tau$ be an involution of $C$ with $w\circ\tau=w$ and
$\sigma\circ\tau=-\sigma$. Then $\tau$ has no fixed point,
$w(c)\sigma(c)+w(\tau c)\sigma(\tau c)=0$ for every $c$, and $\sum_{c\in C}w(c)\sigma(c)=0$. The
converse fails: a zero signed sum need not come from such a pairing.

*Proof.* A fixed point would have $\sigma(c)=-\sigma(c)$, which is impossible for $\sigma(c)=\pm1$.
For each $c$, $w(\tau c)\sigma(\tau c)=w(c)(-\sigma(c))$, so the pair sum is $0$. Since $\tau$ is a
fixed-point-free involution, $C$ is the disjoint union of the two-element orbits $\{c,\tau c\}$, and
the total is a sum of zero pair sums. For the converse, three configurations with signed weights
$2,-1,-1$ sum to $0$, but no weight-preserving pairing matches the weight $2$. $\square$

An observable numerator $\sum_cw(c)\sigma(c)A(c)$ cancels in the same way only if $A\circ\tau=A$.
Without that condition a cancelling doublet can carry a nonzero numerator: signs $1,-1$ with
$A=1,-1$ give $1\cdot1+(-1)(-1)=2$.

Lean: `papers/core/fsp/lean4/MeronClusterInvolution.lean::meron_pair_exact_cancellation`,
`papers/core/fsp/lean4/MeronClusterInvolution.lean::fixed_point_contradiction`,
`papers/core/fsp/lean4/FrustratedSpectrumObstruction.lean::bipartite_pair_exact_cancellation`
(the same pair identity for a bipartite Trotter-path involution),
`papers/core/fsp/lean4/MeronCharacter.lean::unequal_three_term_cancellation`,
`papers/core/fsp/lean4/MeronCharacter.lean::observable_doublet_counterexample`, and
`papers/core/majorana/lean4/MajoranaGinCore.lean::involution_pair_cancels_sign` (the pair identity
$ws_1+ws_2=w(s_1+s_2)=0$). The step from pair sums to the total over $C$ is not in Lean.

### 1.4 The U(1) Wilson action

DAG node: `FSP-U1-WILSON-ACTION`

**Proposition.** Let $V$ be a set of vertices, $U\colon V\times V\to U(1)$ a link field, and
$(\gamma_p)_{p\in P}$ a finite family of closed vertex paths, with holonomy $U_p$ the ordered
product of the link values along $\gamma_p$. For $\beta\in\mathbb R$ put
$S(U)=\beta\sum_{p}(1-\operatorname{Re}U_p)$. Then (i) $S$ is invariant under
$U_{ab}\mapsto g_aU_{ab}g_b^{-1}$ for every $g\colon V\to U(1)$, equivalently under
$A_{ab}\mapsto A_{ab}+\theta_a-\theta_b$ for $U=e^{iA}$; (ii) if $\beta\ge0$ then $S\ge0$, and if
$\beta>0$ then $S=0$ exactly when every $U_p=1$; (iii) without $\beta\ge0$, nonnegativity fails.

*Proof.* (i) Along a closed path $v_0v_1\cdots v_n=v_0$ the gauge factors telescope:
$\prod_j g_{v_j}U_{v_jv_{j+1}}g_{v_{j+1}}^{-1}=g_{v_0}U_pg_{v_0}^{-1}=U_p$, since $U(1)$ is
abelian. So every $U_p$, and hence $S$, is unchanged. With $g_a=e^{i\theta_a}$ the angle shift is
the same transformation. (ii) $|U_p|=1$ gives $\operatorname{Re}U_p\le1$, so every term is
nonnegative. A sum of nonnegative terms is zero only if each term is, and $1-\operatorname{Re}U_p=0$
with $|U_p|=1$ forces $U_p=1$. (iii) One self-loop plaquette with $U_p=-1$ and $\beta=-1$ gives
$S=-2$. $\square$

The periodic hypercubic lattice $(\mathbb Z/L)^d$ with its elementary plaquettes is one instance.
Because links are functions of ordered vertex pairs, for $L\le2$ the two parallel links between
neighbours coincide. Nothing is claimed about a fermion sign, a continuum limit, reflection
positivity, a transfer matrix or a non-abelian action.

Lean: `lean4/FermionSignU1WilsonAction.lean::FermionSignU1WilsonAction.fsp_u1_wilson_action`
states (i) and the first part of (ii) for any vertex type and finite path family;
`lean4/FermionSignU1WilsonAction.lean::FermionSignU1WilsonAction.loopHolonomy_gaugeAct`,
`lean4/FermionSignU1WilsonAction.lean::FermionSignU1WilsonAction.wilsonAction_eq_zero_iff`,
`lean4/FermionSignU1WilsonAction.lean::FermionSignU1WilsonAction.wilsonAction_nonneg_needs_beta`,
`lean4/FermionSignU1WilsonAction.lean::FermionSignU1WilsonAction.hypercubicWilson_gauge_invariant`,
`lean4/FermionSignU1WilsonAction.lean::FermionSignU1WilsonAction.hypercubicWilson_nonneg`.

### 1.5 Flat-connection counts under the 4D Pachner moves

DAG node: `FSP-PACHNER-INVARIANCE-CLAIM`

Let $G$ be a finite group. A $G$-connection on a simplicial complex assigns $c_{ij}\in G$ to each
oriented edge with $c_{ji}=c_{ij}^{-1}$. It is flat if $c_{ij}c_{jk}=c_{ik}$ on every triangle.

**Theorem.** Let $B$ be a simplicial complex that is a combinatorial ball with simply connected
boundary $\partial B$, and let $n_B$ be the number of vertices of $B$ not in $\partial B$. For a
connection $b$ on $\partial B$ let $Z_B(b)$ be the number of flat connections on $B$ that restrict
to $b$. Then $Z_B(b)=0$ if $b$ is not flat, and $Z_B(b)=|G|^{n_B}$ if $b$ is flat. Consequently, for
the two sides $B,B'$ of a 1–5, 2–4 or 3–3 Pachner move in dimension 4, which share their boundary,
$Z_B(b)/|G|^{n_B}=Z_{B'}(b)/|G|^{n_{B'}}$ for every boundary connection $b$.

*Proof.* A non-flat $b$ has a boundary triangle on which flatness fails, and that triangle is also a
triangle of $B$, so no flat extension exists. Let $b$ be flat. On a connected, simply connected
complex every flat connection is a gauge transform of the trivial one: fix a base vertex $o$ and set
$g_v$ to the product of $c$ along any edge path from $o$ to $v$. Flatness on triangles makes this
independent of the path, because simple connectivity means any two paths differ by moves across
triangles. Then $c_{uv}=g_u^{-1}g_v$. The potential $g$ is unique up to left multiplication by one
element of $G$.

Apply this to $b$ on $\partial B$: $b$ has a potential $h$ on the boundary vertices, unique up to
that constant. A flat connection on $B$ restricting to $b$ has a potential $g$ on all vertices of
$B$ whose restriction to $\partial B$ is a potential of $b$, that is, $g|_{\partial B}=ah$ for some
$a\in G$. Conversely, every choice of $a\in G$ and of $g$ at the $n_B$ interior vertices defines a
flat connection extending $b$. Two choices give the same connection exactly when one is obtained
from the other by left multiplication by some $k\in G$ at every vertex, so each extension arises
from exactly $|G|$ of the $|G|\cdot|G|^{n_B}$ choices, and $Z_B(b)=|G|^{n_B}$. The two sides of a Pachner move are balls with the same boundary sphere,
so both normalized counts are $1$ for flat $b$ and $0$ otherwise. $\square$

In the 1–5 move, one side has no interior vertex and the other has one, so the raw counts are $1$
and $|G|$. The raw counts agree only when $G$ is trivial, which is why the normalization is
needed. Summing over a finite family of exterior configurations, with the same number of outside
vertices on both sides, preserves the equality term by term.

Lean: `lean4/FiniteGroupPachner.lean::FiniteGroupPachner.pachner_one_five`,
`lean4/FiniteGroupPachner.lean::FiniteGroupPachner.pachner_two_four`,
`lean4/FiniteGroupPachner.lean::FiniteGroupPachner.pachner_three_three`,
`lean4/FiniteGroupPachner.lean::FiniteGroupPachner.nonflat_boundary_has_no_extension`,
`lean4/FiniteGroupPachner.lean::FiniteGroupPachner.oneFillingEquiv`,
`lean4/FiniteGroupPachner.lean::FiniteGroupPachner.unnormalized_one_five_iff`,
`lean4/FiniteGroupPachner.lean::FiniteGroupPachner.glued_one_five`,
`lean4/FiniteGroupPachner.lean::FiniteGroupPachner.glued_two_four`,
`lean4/FiniteGroupPachner.lean::FiniteGroupPachner.glued_three_three`.
Lean checks the three canonical local complexes directly, by constructing the fillings and counting
them. It does not contain the general ball argument above, a gluing or PL-homeomorphism library, or
twisted (Dijkgraaf–Witten, Crane–Yetter) weights.

---

## 2. Majorana carriers

### 2.1 The residual trichotomy

DAG nodes: `MAJ-TRICHOTOMY-PAIRWISE-EXCLUSION` `MAJ-TRIVIAL-H1-NO-CLOSED`

Let $C^0\xrightarrow{d_0}C^1\xrightarrow{d_1}C^2$ be linear maps of $\mathbb F_2$-vector spaces with
$d_1d_0=0$. Call $w\in C^1$ *exact* if $w\in\operatorname{im}d_0$, a *closed residual* if $d_1w=0$
and $w\notin\operatorname{im}d_0$, and an *open obstruction* if $d_1w\neq0$.

**Proposition.** (i) Every exact $w$ is a cocycle, and no $w$ has two of the three labels.
(ii) If every cocycle is exact ($H^1=0$), no $w$ is a closed residual.

*Proof.* (i) If $w=d_0g$ then $d_1w=d_1d_0g=0$, so $w$ is neither an open obstruction nor, by
definition, a closed residual. A closed residual has $d_1w=0$ and so is not an open obstruction.
(ii) A closed residual would be a cocycle that is not exact. $\square$

Every $w$ also has at least one label, by cases on $d_1w=0$ and on $w\in\operatorname{im}d_0$. That
half is not in Lean. Using (ii) on the legacy carrier needs the separate computation that its
$H^1$ vanishes.

Lean: `papers/core/majorana/lean4/MajoranaCore.lean::coboundary_is_cocycle`,
`papers/core/majorana/lean4/MajoranaCore.lean::exact_not_open`,
`papers/core/majorana/lean4/MajoranaCore.lean::exact_not_closed_residual`,
`papers/core/majorana/lean4/MajoranaCore.lean::closed_residual_not_open`,
`papers/core/majorana/lean4/MajoranaCore.lean::trichotomy_pairwise_disjoint`,
`papers/core/majorana/lean4/MajoranaCore.lean::legacy_carrier_obstruction`.

### 2.2 Edge Majorana indices of the Kitaev chain

DAG node: `MAJ-KITAEV-EDGE-INDEX-DISJOINT`

**Proposition.** Number the $2L$ Majorana operators of an $L$-site chain $1,\dots,2L$. For
$1\le j<L$, the inter-site bond $(2j,2j+1)$ contains neither $1$ nor $2L$.

*Proof.* $2j\ge2$ and $2j+1\ge3$, and $2j+1\le2L-1<2L$. $\square$

At the sweet spot the Hamiltonian is a sum over these bonds, so $\gamma_1$ and $\gamma_{2L}$ appear
in no term. That operator statement is a separate exact instance and is not proved here.

Lean: `papers/core/majorana/lean4/MajoranaGinCore.lean::is_bulk_kitaev_bond`,
`papers/core/majorana/lean4/MajoranaGinCore.lean::edge_mode_1_not_in_bulk`,
`papers/core/majorana/lean4/MajoranaGinCore.lean::edge_mode_2L_not_in_bulk`.
