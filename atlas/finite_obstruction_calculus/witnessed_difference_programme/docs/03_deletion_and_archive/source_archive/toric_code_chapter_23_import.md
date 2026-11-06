# Chapter 23 — Observer completion on a finite 2D toric-code carrier

**What this chapter does.** It instantiates the operational question of the previous session — *given what the observer already sees, which further observations are necessary and sufficient, and what is the cheapest way to obtain them?* — on a declared finite carrier with actual instruments and prices. The answer is a sharp threshold, an exact certificate, a replayable lower bound, a terminating procedure, and one honest negative result (worst-case adaptivity buys nothing here). The chapter is a **conditional result**: it presupposes a declared noise model, a declared schedule, and a declared precision, and it says nothing about any physical device.

---

## 23.1 The declaration packet

`WDP-CH23-D01` **Definition (toric-code completion packet).** A *completion packet* is a tuple

$$
\mathfrak T=\bigl(\Lambda,\ \mathcal{S},\ \mathcal{D},\ \mathcal{T},\ \mathcal{P},\ \mathcal{E},\ q,\ B\bigr)
$$

with the following fields, all finite and all declared:

1. **Carrier.** $\Lambda=\mathbb Z_L\times\mathbb Z_L$ with $L\ge 3$, horizontal qubits $h_{i,j}$ and vertical qubits $v_{i,j}$, $n=2L^{2}$ data qubits, and the Pauli carrier $\mathcal P=\mathbb F_2^{\,n}\oplus\mathbb F_2^{\,n}$ with $e=(e_X,e_Z)$ and weight $\mathrm{wt}(e)=|\mathrm{supp}e_X|+|\mathrm{supp}e_Z|$.
2. **Stabilizers.** $S=\langle\sigma^\star_v,\ \sigma^\square_f\rangle$, $\sigma^\star_v$ the $X$-star of site $v$, $\sigma^\square_f$ the $Z$-plaquette of face $f$.
3. **Detector locations.** A *detector* is a pair $d=(\sigma,k)$ with $\sigma$ a stabilizer generator and $k$ a round index. A schedule $D$ is a finite subset of $\mathcal S\times[R]$; the *dark windows* of $D$ are the maximal open intervals of $[R]$ containing no round whose full stabilizer set is in $D$.
4. **Classical communication.** Per round, a measurement duration $\tau_m$ and a link latency $\tau_c$; the syndrome of round $k$ is available to the policy at time $t_k=k(\tau_m+\tau_c)+\tau_c$.
5. **Precision.** Each detector returns one bit (exact readout), or — in the noisy branch of §23.9 — one bit subject to a declared independent flip with rational parameter $\varepsilon$, or no value at all (that is, the location is dark).
6. **Admissible errors.** $\mathcal E\subseteq\mathcal P$, declared; the standard instance is $\mathcal E_t=\{e:\mathrm{wt}(e)\le t\}$.
7. **Protected question.** A group homomorphism $q:\mathcal P\to A$ with $B=\ker q$ and $S\subseteq B$. The standard instance is $q(e)=[e]$ in $\mathcal P/S$, with $B=S$: *the recovery left a stabilizer, so the logical state is the prepared one.*
8. **Recovery.** A policy $\rho:\mathrm{im}\,Q_D\to\mathcal P$ applied to the accumulated detector record.

`WDP-CH23-D02` **Definition (effective detection map).** For a schedule $D\subseteq\mathcal S\times[R]$, let $D_k=\{\sigma:\ (\sigma,j)\in D,\ j\le k\}$ and define the **cumulative** detection map on error histories by
$$
Q_{D,k}(e^{(1..k)}) = \Bigl(\operatorname{syn}_{D_k}\bigl(e^{(k)}\bigr)\Bigr)\in\mathbb F_2^{\,2L^{2}},\qquad e^{(k)}=(e_X^{(k)},e_Z^{(k)}).
$$
Without measurement error the syndrome is exactly
$$
Q(e^{(k)})=\bigl(Ae^{(k)}_X,\ A_v e^{(k)}_Z\bigr),
$$
where $A\in\mathbb F_2^{\,L^{2}\times 2L^{2}}$ is the face–qubit incidence and $A_v$ the site–qubit incidence. When the whole of round $k$ is measured, $Q_{D,k}=Q_{D,k+1}$ and the map is the single-round map $Q$.

---

## 23.2 The exact structure of the kernel

`WDP-CH23-P01` **Finite proposition (kernel structure).** In the packet of CH23-D01, $\mathrm{rank}\,A=\mathrm{rank}\,A_v=L^{2}-1$, and with $\mathrm{Cyc}=\ker A$ (cycle space, dimension $L^{2}+1$), $\mathrm{Cut}=\ker A_v$ (cut space, dimension $L^{2}+1$), $\mathrm{Plaq}=\mathrm{row}(A)$ and $\mathrm{Star}=\mathrm{col}(A_v)$ (each of dimension $L^{2}-1$):

$$
\ker Q=\mathrm{Cyc}\oplus\mathrm{Cut},\qquad
S=\mathrm{Plaq}\oplus\mathrm{Star},\qquad
\mathrm{rank}\,Q=2L^{2}-2,\qquad
[\ker Q:S]=4 .
$$

*Proof.* Every qubit lies on exactly two faces and in exactly two stars, so $\sum_f A_{f,\cdot}=0$ and $\sum_v(A_v)_{v,\cdot}=0$; the left kernels of $A$ and $A_v$ are the constants on the connected dual and primal graphs respectively, giving rank $L^{2}-1$ each and $\dim\ker A=\dim\ker A_v=2L^{2}-(L^{2}-1)=L^{2}+1$. The orthogonal complement of the row space of an incidence matrix is the cut space and of the site–incidence is the cycle space, giving the two decompositions of $\mathbb F_2^{2L^{2}}$; rank-nullity on the direct sum gives $\mathrm{rank}\,Q=(L^{2}-1)+(L^{2}-1)$. Finally $2L^{2}-(2L^{2}-2)=2$. $\square$

So the syndrome map has a **two-dimensional logical kernel**:
$$
\ker Q/S\;\cong\;\mathrm{Cyc}/\mathrm{Plaq}\oplus\mathrm{Cut}/\mathrm{Star}\;\cong\;\mathbb F_2^{\,2}\oplus\mathbb F_2^{\,2}.
$$
A **logical operator** is a row or column of the lattice: $\bar X=\prod_j X_{h_{i,j}}$ (a cycle of weight $L$ not a plaquette sum) and $\bar Z=\prod_i Z_{v_{i,j}}$ (a cut of weight $L$ not a star union).

`WDP-CH23-P02` **Finite proposition (distance).** $\min\{\mathrm{wt}(e): e\in\ker Q\setminus S\}=L$, and a weight-$L$ element exists in each sector.

*Proof sketch.* Let $u\in\mathrm{Cyc}$ with $\mathrm{wt}(u)<L$. Decompose $u$ into simple cycles. A simple cycle of weight $\ge 5$ on the torus bounds a disk and is a sum of plaquette boundaries; a simple cycle of weight $4$ is a single plaquette, or (only when $L=4$) a full row, which has weight $L$ and so is not of weight $<L$. Hence $\mathrm{wt}(u)<L\Rightarrow u\in\mathrm{Plaq}$. Dually $\mathrm{wt}(v)<L\Rightarrow v\in\mathrm{Star}$. Therefore $\mathrm{wt}(e)<L$ forces $e\in S$. The row $\bar X$ has weight $L$ and lies in $\mathrm{Cyc}\setminus\mathrm{Plaq}$: a row cycle does not bound a disk, and any plaquette decomposition of it would have to cancel $L$ of its $L$ edges, forcing $L\le 4$ plaquettes with pairwise disjoint edge sets, which cannot occur for a cycle that meets each face in at most two consecutive edges. $\square$

`WDP-CH23-P01`–`P02` are the standard toric-code facts (distance $L$, two logical qubits, $2L^{2}-2$ independent stabilizers on $2L^{2}$ qubits). They are re-derived here so that every later row is checkable from this chapter alone, not imported from the literature. `WDP-CH23-N01` **Imported standard.** The mathematical content is textbook stabilizer-code theory; the contributions claimed are the *declared* $B$-spectrum, the certificate calculus of §23.7, the time envelope of §23.8, and the negative result of §23.10.

---

## 23.3 The criterion is the report–question factorization

`WDP-CH23-P03` **Finite proposition (the criterion, in general).** Let $Q:\mathcal P\to Y$ be a homomorphism, $q:\mathcal P\to A$ a homomorphism, $B=\ker q$, and $\mathcal E\subseteq\mathcal P$. Then

$$
q|_{\mathcal E}\ \text{is a function of }Q|_{\mathcal E}\quad\Longleftrightarrow\quad
(\mathcal E-\mathcal E)\cap\ker Q\;\subseteq\;B .
$$

*Proof.* ($\Rightarrow$) If $Qe_1=Qe_2$ then $e_1-e_2\in\ker Q\subseteq B$, so $qe_1=qe_2$ because $q$ factors through $\mathcal P/B$. ($\Leftarrow$) Define $\bar q(\sigma)=qe$ for any $e\in\mathcal E$ with $Qe=\sigma$; the inclusion makes this independent of the choice. $\square$

This is Appendix P.1's factorization criterion specialised to the subgroup $B$, and it is the reason the question must be *stated* before it can be *priced*. Note the quantifier: the condition is about the **set of unresolved pairs** $\{(e_1,e_2)\in\mathcal E^2: Qe_1=Qe_2\}$, exactly as in the previous session; here the pairs are grouped into the fibres of one finite map.

`WDP-CH23-P04` **Finite proposition (the recovery, exactly).** With $D$ the full schedule, $q$ and $B$ as in CH23-D01, there is a policy $\rho:\mathrm{im}\,Q\to\mathcal P$ with
$$
e+\rho(Qe)\in B\quad\text{for all }e\in\mathcal E
\qquad\Longleftrightarrow\qquad
(\mathcal E-\mathcal E)\cap\ker Q\subseteq B .
$$

*Proof.* ($\Leftarrow$) For each realized $\sigma$ pick $e_\sigma\in\mathcal E\cap Q^{-1}\sigma$ and set $\rho(\sigma)=e_\sigma$; then $e+e_\sigma\in B$ for every $e$ in that fibre by CH23-P03. ($\Rightarrow$) If $Qe_1=Qe_2=\sigma$ then $e_1+\rho\sigma,\,e_2+\rho\sigma\in B$, so $e_1-e_2\in B$. $\square$

`WDP-CH23-P05` **Finite proposition (the sharp failure witness).** If the condition fails, the procedure of §23.11 returns $e_1,e_2\in\mathcal E$ with
$$
Qe_1=Qe_2,\qquad e_1-e_2\in\ker Q\setminus B .
$$
Such a pair is an **indistinguishable pair with different protected answers**: $qe_1-qe_2=q(e_1-e_2)\ne 0$, and no policy of the form above can place both residuals in $B$, because $Q(e_1+\rho\sigma)=Q(e_2+\rho\sigma)=0$ forces the two residuals to differ by $e_1-e_2$.

---

## 23.4 The threshold, and the tolerance spectrum over $B$

`WDP-CH23-P06` **Finite proposition (the threshold).** For $\mathcal E=\mathcal E_t$ and $B=S$,
$$
(\mathcal E_t-\mathcal E_t)\cap\ker Q\subseteq S
\qquad\Longleftrightarrow\qquad
2t<L .
$$

*Proof.* Every Pauli of weight $\le 2t$ is a sum of two of weight $\le t$ whenever $2t\le n$ (split the support), so $\mathcal E_t-\mathcal E_t=\mathcal E_{2t}$. By CH23-P02, $\mathcal E_{2t}\cap(\ker Q\setminus S)\ne\emptyset$ exactly when $2t\ge L$. $\square$

So for the protected question "is the logical state the prepared one?", the answer is: **the lattice and the noise model already settle it; the observer buys nothing.** The sufficiency condition $L>2t$ is a property of the declared carrier, not a purchase.

`WDP-CH23-P07` **Finite proposition (the $B$-spectrum).** Write $B_W=S\vee\langle\bar X^{\alpha}\bar Z^{\beta}:(\alpha,\beta)\in W\rangle$ for $W\le\mathbb F_2^{2}$, and
$$
d_W:=\min\{\mathrm{wt}(e): e\in\ker Q\setminus S,\ [e]\bmod S\in W\setminus\{0\}\}.
$$
Then $(\mathcal E_t-\mathcal E_t)\cap\ker Q\subseteq B_W$ iff $2t<d_W$, and

$$
d_{\{0\}}=d_{\langle\bar X\rangle}=d_{\langle\bar Z\rangle}=d_{\mathbb F_2^{2}}=L,
\qquad d_{\langle\bar X\bar Z\rangle}=2L-1 .
$$

*Proof.* The first equivalence is CH23-P03 with $\ker q=B_W$ and the weight argument of CH23-P06, using $d_W$ as the effective distance of the code with stabilizer group $B_W$. For the values: any element of $\mathrm{Cyc}\setminus\mathrm{Plaq}$ has weight $\ge L$ (CH23-P02) and likewise in the cut sector, so every $W$ containing a nonzero homology class in one sector has $d_W=L$. For $W=\langle\bar X\bar Z\rangle$ the class is $\bar X\bar Z$ with support the union of a row and a column, of size $L+L-1=2L-1$; adding stabilizers cannot reduce it, because the $X$-part of any element of $\mathrm{Cyc}\setminus\mathrm{Plaq}$ has weight $\ge L$ and the $Z$-part has weight $\ge L$, and two weight-$L$ supports overlap in at most one qubit. $\square$

`WDP-CH23-P08` **Corollary (query-relative tolerance).** Protecting the coarser question *"neither of the two logical bits has flipped"* ($W=\langle\bar X\bar Z\rangle$) tolerates $t\le L-1$ where $B=S$ tolerates $t\le (L-1)/2$. **A halving of the required lattice size.** This is §9.8 ("sufficiency is query-relative") with a price attached: a coarser protected question is exponentially — here factorially — cheaper in carrier.

---

## 23.5 Partial schedules and the exact unresolved subgroup

The full-schedule discussion in §23.3 concerns the one-round syndrome map. A partial schedule requires a cumulative detector record. The following definitions make “dark” and “omitted” precise.

`WDP-CH23-D03` **Definition (partial cumulative syndrome).**  
Let \(D\subseteq\mathcal S\times[R]\). For \(e=(e^{(1)},\ldots,e^{(R)})\) and \(k\in[R]\), define

\[
Q_{D,k}(e^{(1,\ldots,k)})
 =
\sum_{j=1}^{k}Q_{D_j}(e^{(j)}),
\]

where

\[
D_j=\{\sigma\in\mathcal S:(\sigma,j)\in D\}
\]

and \(Q_{D_j}\) is the sum of the syndrome columns assigned to the stabilizers in \(D_j\). Equivalently, if \(H_D\in\mathbb F_2^{|D|\times n}\) has one column for each detected Pauli component, then

\[
Q_{D,k}(e^{(1,\ldots,k)})
 =
\sum_{j=1}^{k}H_{D_j}(e^{(j)}).
\]

For a single spatial Pauli \(e\), write

\[
\ker Q_D
 =
 \{z\in\mathbb F_2^n:H_Dz=0\}.
\]

All additions below are in \(\mathbb F_2\).

A dark round is a \(j\) for which \(D_j=\varnothing\). An omitted stabilizer is a stabilizer generator \(\sigma\notin D_j\). The cumulative definition does not discard the earlier rounds: a detector omission changes the information available after that round, while prior accumulated syndrome remains part of the record.

`WDP-CH23-P09` **Finite proposition (partial-schedule criterion).**  
For a partial schedule \(D\), the terminal detector record is

\[
Q_{D,R}:\mathcal E^R\longrightarrow \mathbb F_2^{|D|}.
\]

A recovery policy

\[
\rho:\operatorname{im}Q_{D,R}\longrightarrow\mathcal P
\]

satisfying

\[
e^{(R)}+\rho(Q_{D,R}e)\in B
\qquad
\text{for every }e\in\mathcal E
\]

depends on whether the question is attached to the terminal error alone or to the complete spacetime history. For the terminal-error convention, the exact condition is

\[
(\mathcal E-\mathcal E)\cap\ker Q_D\subseteq B,
\]

where

\[
H_D=\sum_{j=1}^R H_{D_j}
\]

is the accumulated detector matrix. For the spacetime-history convention, the corresponding condition is

\[
\bigl(\mathcal E^R-\mathcal E^R\bigr)
 \cap \ker Q_{D,R}\subseteq B^R.
\]

In particular, for a single-round error model, \(D\) is sufficient for \((\mathcal E,B)\) in the sense of §23.3 exactly when

\[
\boxed{
(\mathcal E-\mathcal E)\cap\ker Q_D\subseteq B.
}
\]

*Proof.* The terminal-error convention asks whether two admissible terminal errors with equal accumulated syndrome have the same protected answer. This is the factorization criterion from CH23-P03 applied to \(Q_D\). The recovery construction is the same: choose one representative \(e_\sigma\) from each nonempty fibre and set \(\rho(\sigma)=e_\sigma\).

For the spacetime convention, \(Q_{D,R}\) acts on the block vector

\[
e^{(1)},\ldots,e^{(R)}.
\]

If two histories have the same record, their difference lies in \(\ker Q_{D,R}\). Their protected questions agree exactly when that difference lies in \(B^R\). Applying CH23-P03 gives the stated condition. \(\square\)

#### Omitted stabilizers and homological expansion

`WDP-CH23-D04` **Definition (effective stabilizer row space and omitted-dual basis).**  
For \(D\), let

\[
R_D=\operatorname{row}_{\mathbb F_2}(H_D)\subseteq(\mathbb F_2^n)^*
\]

and let \(N_D=R_D^\perp\) be the omitted-dual space. When all independent stabilizer rows are measured, \(R_D=S^*\) up to an invertible change of basis and \(\ker Q_D=S\). If one independent row is removed, then

\[
\dim(\ker Q_D/S)=1.
\]

More generally, if \(r_D=\operatorname{rank}H_D\), then

\[
\dim\ker Q_D=n-r_D
\]

and the quotient by the full stabilizer group, when \(S\subseteq\ker Q_D\), has dimension

\[
\dim\bigl(\ker Q_D/S\bigr)
 =
 2L^2-2-r_D.
\]

`WDP-CH23-P10` **Finite proposition (the cost of omission).**  
Suppose the full independent stabilizer set is measured except for an independent row \(s\). Then the new kernel is

\[
\ker Q_{\mathrm{partial}}
 =
 S\vee\langle z\rangle,
\]

where \(z\in\ker Q\setminus S\) is a dual logical representative satisfying \(s(z)=1\). Thus an omitted independent detector leaves a logical element invisible.

If the omitted row is an independent plaquette row, \(z\) has a nontrivial cycle homology class. If it is an independent star row, \(z\) has a nontrivial cut homology class. For the standard local-error set \(\mathcal E_t\), the resulting sufficient threshold can drop from

\[
2t<L
\]

to the smallest weight of a nonzero class in the omitted-dual direction.

*Proof.* Since \(Q_{\mathrm{full}}\) has row space \(S^*\), deleting a basis row \(s\) changes the row space to a codimension-one subspace of \(S^*\). Therefore its orthogonal complement is

\[
\ker Q_{\mathrm{partial}}
 =
 (S^*\setminus s)^\perp
 =
 S\vee\langle z\rangle
\]

for an element \(z\) representing the dual generator. If \(s\) is a face row, choose a primal cycle crossing that face; then \(s(z)=1\) because the cycle meets the face boundary in one edge. If \(s\) is a star row, choose the dual cut crossing that star.

The standard basis of primal and dual logical operators is detected by every independent stabilizer row. After omission, the corresponding logical direction is no longer detected. For local Pauli errors, the minimum surviving weight depends on the chosen representative of the homological direction; the exact value must be computed from that representative. \(\square\)

For the usual logical rows and columns, the omitted direction can contain a representative of weight \(L\). If the detector omission is combined with a boundary deformation, the representative may have weight \(1\) or \(2\). The exact small-weight statement is therefore:

\[
d_{\mathrm{omitted}}
 :=
 \min\{\mathrm{wt}(z):z\in\ker Q_{\mathrm{partial}}\setminus S\}
\]

and

\[
(\mathcal E_t-\mathcal E_t)
 \cap\ker Q_{\mathrm{partial}}\subseteq S
 \quad\Longleftrightarrow\quad
 2t<d_{\mathrm{omitted}}.
\]

Thus a dark window is not, by itself, a general failure statement. It is fatal for the protected question exactly when it creates an unresolved pair in the relevant kernel.

`WDP-CH23-N02` **Note (negative fence for dark-window language).**  
The phrase “dark windows are fatal” means that a dark window is fatal whenever it introduces a nonzero element of \((\mathcal E-\mathcal E)\cap\ker Q_D\setminus B\). It does not mean that every dark window is harmful for every \(\mathcal E\). A single dark round can leave the accumulated syndrome sufficient for a restricted error set, while a complete dark interval can be harmful for a spatially local model once the admissible spacetime weight is large enough.

---

## 23.6 The minimum-cost sufficient detector set

`WDP-CH23-D05` **Definition (instrument prices).**  
Assign to every detector location \(d=(\sigma,k)\in\mathcal S\times[R]\) a rational price

\[
c(d)\in\mathbb Q_{\ge0}.
\]

For \(D\subseteq\mathcal S\times[R]\), define

\[
c(D)=\sum_{d\in D}c(d).
\]

Prices are instrument costs only. They do not represent a claim about physical implementation time.

For the single-round terminal convention, define the detector matrix

\[
H_D=(H_{D_j})_{j=1}^{R}.
\]

If the admissible set is \(\mathcal E_t\), the sufficient schedules are exactly those satisfying

\[
(\mathcal E_t-\mathcal E_t)\cap\ker H_D\subseteq S.
\]

`WDP-CH23-P11` **Finite proposition (integer optimization).**  
For the full question \(B=S\) and the standard threshold \(2t<L\), define

\[
\mathcal F_D
 =
 \{D\subseteq\mathcal S\times[R]:
    H_D\text{ has full stabilizer rank }2L^2-2\}.
\]

Then

\[
D^*\in\arg\min_{D\in\mathcal F_D}c(D)
\]

is a cheapest sufficient detector set. If the question is restricted by a set \(B\) or by a nonstandard \(\mathcal E\), replace \(\mathcal F_D\) by the exact family

\[
\mathcal F_D(\mathcal E,B)
 =
 \{D:
  (\mathcal E-\mathcal E)\cap\ker H_D\subseteq B
 \}.
\]

*Proof.* For \(2t<L\), CH23-P06 says that sufficiency is equivalent to every nontrivial kernel element belonging to \(S\). The full stabilizer syndrome has kernel \(S\). Hence

\[
\ker H_D\subseteq S
\]

is equivalent to equality of the row spaces \(R_D=S^*\), which is equivalent to

\[
\operatorname{rank}H_D=2L^2-2.
\]

The weighted subset problem is therefore the stated integer optimization problem. The same argument after replacing \(S\) by \(B\) applies to the restricted family. \(\square\)

### Matroid and covering formulations

`WDP-CH23-D06` **Definition (detector matroid).**  
Let

\[
\mathcal A=\mathcal S\times[R]
\]

and assign to each \(a\in\mathcal A\) its detector column \(h_a\in\mathbb F_2^n\), with the appropriate \(X\)- and \(Z\)-sector interpretation. Define the linear matroid

\[
\mathcal M_D=(V,\mathcal I),
\qquad
I\subseteq\mathcal A,\quad I\in\mathcal I
 \Longleftrightarrow
 \{h_a:a\in I\}\text{ is linearly independent}.
\]

For nonuniform costs, a minimum-cost full-rank detector set is a minimum-weight basis of this binary matroid, provided that sufficiency is equivalent to full detector rank.

For a restricted error set, the exact condition is a covering condition:

\[
\forall z\in(\mathcal E-\mathcal E)\setminus B,\qquad
H_Dz\ne0.
\]

Equivalently, for every admissible unresolved direction

\[
z\in(\mathcal E-\mathcal E)\setminus B,
\]

the chosen detector set must contain a collection of columns whose common kernel does not contain \(z\).

`WDP-CH23-P12` **Finite proposition (matroid structure and greedy algorithm).**  
Under full-rank sufficiency, the family of sufficient detector sets is the family of spanning sets of \(\mathcal M_D\). Consequently, a minimum-cost sufficient set is a minimum-weight basis. The standard greedy algorithm for a linear matroid returns such a basis:

1. Start with \(I=\varnothing\).
2. Among all \(a\notin I\) for which \(I\cup\{a\}\) remains independent, choose one minimizing \(c(a)/(c(a)-0)\), or directly minimizing \(c(a)\) when the prices are the declared additive weights.
3. Add \(a\) to \(I\).
4. Stop when \(\operatorname{rank}I=2L^2-2\).

The precise weighted greedy procedure uses the usual matroid weight comparison. If the prices are interpreted as additive nonnegative costs, it returns a minimum-weight basis among all bases of the linear matroid.

*Proof.* The rank function of a linear matroid is

\[
r(I)=\dim\operatorname{span}\{h_a:a\in I\}.
\]

A detector set is full rank exactly when \(r(I)=2L^2-2\). Such sets are precisely the spanning sets. Every spanning set contains a basis, and deleting an element outside a basis cannot change the rank. Minimum-weight sufficient sets can therefore be taken to be bases. The weighted greedy theorem for matroids then gives optimality. \(\square\)

For general \((\mathcal E,B)\), the condition is not always a matroid basis condition. It can be represented as a covering problem over the finite set

\[
\mathcal U=(\mathcal E-\mathcal E)\setminus B.
\]

The restriction to a finite declared family permits exhaustive integer optimization, while the full-rank toric-code instance has the matroid form above.

### Uniform costs and the degree-one spine

`WDP-CH23-D07` **Definition (uniform detector price).**  
Assume

\[
c(a)=1
\]

for every \(a\in\mathcal A\). A **degree-one spine** is a detector set containing one representative of every independent stabilizer row, with no duplicate or linearly dependent detector column.

`WDP-CH23-P13` **Finite proposition (uniform-cost threshold).**  
If \(2t<L\), every sufficient single-round schedule has

\[
|D|\ge 2L^2-2.
\]

There is a sufficient schedule with exactly \(2L^2-2\) detectors. In such a schedule, every detector is essential: deleting any one lowers the detector rank and enlarges the kernel beyond \(S\).

*Proof.* A rank-\((2L^2-2)\) matrix over \(\mathbb F_2\) has at least \(2L^2-2\) columns. The full stabilizer generator set supplies a matrix of that rank. If a schedule has exactly \(2L^2-2\) independent columns, deleting one column lowers the rank by one, so the new kernel has dimension at least three beyond the two-dimensional quotient \(\ker Q/S\). Therefore a logical class is no longer excluded. \(\square\)

The exact spine is consequently any basis of the stabilizer row matroid:

\[
\boxed{
\min_{\text{uniform }c}|D|=2L^2-2
}
\]

for the standard full logical question. Redundant checks can be removed without changing the kernel. The phrase “degree-one spine” refers to the rank-\(2L^2-2\) basis of the detector row space, not to a graph-theoretic degree condition.

---

## 23.7 Primal and dual certificate calculus

`WDP-CH23-D08` **Definition (primal certificate).**  
A primal certificate for \(D\) is a map

\[
\rho:\operatorname{im}Q_D\to\mathcal P
\]

such that

\[
e+\rho(Q_D e)\in B
\qquad
\forall e\in\mathcal E.
\]

The map is finite because \(\operatorname{im}Q_D\subseteq\mathbb F_2^{|D|}\) is finite. It may be stored as a dictionary with one recovered representative for each realized syndrome.

A homological decoder table is an alternative presentation. It records, for each syndrome, a representative \(e_\sigma\) chosen from one of the relevant homology classes.

`WDP-CH23-D09` **Definition (dual certificate).**  
A dual certificate of failure is a pair

\[
(e_1,e_2)\in\mathcal E\times\mathcal E
\]

such that

\[
Q_D e_1=Q_D e_2
\]

and

\[
e_1-e_2\in\ker Q_D\setminus B.
\]

Equivalently,

\[
Q_D(e_1-e_2)=0,
\qquad
q(e_1)\ne q(e_2).
\]

The pair is an explicit indistinguishable pair with unequal protected answers.

`WDP-CH23-P14` **Finite proposition (exact primal–dual certificate dichotomy).**  
For every finite declared instance \((D,\mathcal E,B)\), exactly one of the following holds:

1. a primal certificate \(\rho\) exists; or
2. a dual certificate \((e_1,e_2)\) exists.

Moreover,

\[
\text{a primal certificate exists}
\Longleftrightarrow
(\mathcal E-\mathcal E)\cap\ker Q_D\subseteq B.
\]

*Proof.* If the primal certificate exists and \(Q_D e_1=Q_D e_2\), then

\[
e_1-e_2
 =
(e_1+\rho(Q_D e_1))
 +(e_2+\rho(Q_D e_2))
 \in B.
\]

Thus the kernel inclusion holds.

Conversely, suppose the kernel inclusion holds. For each realized syndrome \(\sigma\), choose \(e_\sigma\in\mathcal E\) with \(Q_De_\sigma=\sigma\). For every \(e\in\mathcal E\) with \(Q_De=\sigma\),

\[
e-e_\sigma\in
(\mathcal E-\mathcal E)\cap\ker Q_D\subseteq B.
\]

Hence

\[
e+\rho(\sigma)
 =
 e+e_\sigma
 \in B
\]

over \(\mathbb F_2\), defining a valid primal certificate.

If the inclusion fails, there are \(e_1,e_2\in\mathcal E\) with

\[
e_1-e_2\in(\mathcal E-\mathcal E)\cap\ker Q_D\setminus B.
\]

This is a dual certificate. \(\square\)

This is a finite algebraic dichotomy, not a numerical approximation. The primal object certifies success for every admissible error; the dual object identifies one concrete failure witness.

`WDP-CH23-N03` **Note (zero-duality-gap boundary).**  
The dichotomy concerns the exact finite instance. It does not assign a computational price to finding the certificate and does not assert that an approximate solver produces the same result.

---

## 23.8 Time resources and local causal cones

`WDP-CH23-D10` **Definition (time envelope).**  
Suppose a round consists of measurement duration \(\tau_m\), communication latency \(\tau_c\), and decoder latency

\[
\tau_{\mathrm{dec}}\ge0.
\]

The terminal decoder is available at

\[
T_R
 =
 R(\tau_m+\tau_c)+\tau_c+\tau_{\mathrm{dec}}.
\]

A detector acquired in round \(k\) is available at

\[
t_k^{\mathrm{dec}}
 =
 k(\tau_m+\tau_c)+\tau_c+\tau_{\mathrm{dec}}.
\]

Define the dark-window length between consecutive usable detector times by

\[
\delta_k=t_{k+1}^{\mathrm{dec}}-t_k^{\mathrm{dec}}
 =
 \tau_m+\tau_c.
\]

The elapsed time from the start of a dark interval to the next detector record is therefore bounded by the schedule envelope and is enlarged by the decoder latency when the next decision requires the decoded record.

`WDP-CH23-D11` **Definition (declared causal cone).**  
Fix a Lieb–Robinson velocity \(v_{\mathrm{LR}}\), measured in lattice sites per unit time. For an event at location \(x\) at time \(t_0\), the declared causal cone is

\[
\mathcal C_{v_{\mathrm{LR}}}(x,t_0)
 =
 \{y:d_{\mathrm{lat}}(x,y)\le v_{\mathrm{LR}}(t-t_0)\}.
\]

The set of lattice locations that can be affected inside a dark interval of length \(\Delta t\) is

\[
C(x,\Delta t)
 =
 \{y:d_{\mathrm{lat}}(x,y)\le v_{\mathrm{LR}}\Delta t\}.
\]

`WDP-CH23-P15` **Finite proposition (causal-cone lower bound).**  
If the local error model permits one error to be placed independently in every unobserved site of a causal cone, then the set of spacetime locations reachable during a dark interval of length \(\Delta t\) has lattice radius at most

\[
\left\lceil v_{\mathrm{LR}}\Delta t\right\rceil.
\]

Therefore, if

\[
\left\lceil v_{\mathrm{LR}}\Delta t\right\rceil\ge
\left\lfloor\frac L2\right\rfloor,
\]

the cone reaches the declared half-distance scale of the logical cycle or cut.

*Proof.* The cone definition gives the integer radius directly. The half-distance statement follows by comparing the radius with \(\lfloor L/2\rfloor\). On the square torus, an unobserved connected region spanning a strip of width \(\lfloor L/2\rfloor\) can contain a path from one side of the logical cycle or cut to the other. \(\square\)

`WDP-CH23-N04` **Note (negative fence for the time envelope).**  
The cone statement establishes geometric reachability under the declared local-error premise. It does not by itself establish that a syndrome-extraction schedule fails. A logical path remains detectable if the stabilizers crossing it are read correctly before the protected decision. The time envelope becomes a failure certificate only when the causal path also lies in the relevant unresolved kernel and the pair lies in \((\mathcal E^R-\mathcal E^R)\setminus B^R\).

In particular, the informal statement

\[
\Delta t\,v_{\mathrm{LR}}\ge L/2
\]

should be read as the threshold at which the causal cone reaches the half-distance scale, not as a threshold that is sufficient for every detector layout. Exact failure remains governed by

\[
(\mathcal E^R-\mathcal E^R)\cap\ker Q_{D,R}\subseteq B^R.
\]

The time resources therefore affect which information is available when, while the finite kernel calculation determines whether the protected question is factorized at the decision time.

---

## 23.9 Noisy detector readout: the \(\varepsilon\)-branch

`WDP-CH23-D12` **Definition (noisy detector record).**  
In the noisy branch, each observed syndrome bit is modified by an independent flip with probability

\[
\varepsilon\in(0,\tfrac12)\cap\mathbb Q.
\]

For a cumulative syndrome \(s\in\mathbb F_2^{|D|}\), the observed record is

\[
\widetilde s=s+m,
\]

where

\[
m\sim \operatorname{Bernoulli}(\varepsilon)^{|D|}
\]

has coordinatewise independent bits.

The protected question is now a statistical decoding question unless the error event is included in the equivalence relation. A deterministic exact recovery is possible for all detector-noise realizations only under a stronger condition than the noiseless criterion.

### Spacetime detector graph

`WDP-CH23-D13` **Definition (spacetime detector graph).**  
Construct a graph whose vertices are detector events, data events, and relevant lattice cells. Attach:

1. a time edge for each detector readout error;
2. a space edge for each data-qubit error propagation between rounds;
3. a syndrome incidence edge from a data error to each stabilizer that detects it.

The corresponding binary chain complex is

\[
C_3
 \xrightarrow{\partial_3}
 C_2
 \xrightarrow{\partial_2}
 C_1
 \xrightarrow{\partial_1}
 C_0.
\]

Data errors, detector flips, and syndrome defects are represented by binary chains of the corresponding degrees. A syndrome history is consistent with a data history precisely when their boundaries agree:

\[
\partial_1 m
 =
 \partial_2 c
 +
 \partial_3 d
\]

under the chosen convention that \(c\) is the data-error chain, \(d\) is the syndrome-defect chain, and \(m\) is the measurement-error chain.

The exact logical question is well posed when the map from admissible joint error chains to the observed syndrome has a well-defined protected-answer factorization.

`WDP-CH23-P16` **Finite proposition (space–time consistency condition).**  
Let

\[
\Phi_{\varepsilon,D}:\mathcal C_{\mathrm{adm}}
 \longrightarrow \mathbb F_2^{|D|}
\]

be the map from an admissible joint data–measurement error chain to its noisy detector record. Let \(B_{\mathrm{sp}}\) be the protected subspace for the full data history. Exact factorization of the protected question on every admissible joint error is equivalent to

\[
(\mathcal C_{\mathrm{adm}}-\mathcal C_{\mathrm{adm}})
 \cap\ker\Phi_{\varepsilon,D}
 \subseteq B_{\mathrm{sp}}.
\]

If the intended criterion is recovery after marginalizing detector flips, then the relevant condition is instead the likelihood-based condition

\[
\Pr_{\varepsilon}\!\left[
 \widetilde Q_D(e)\ne \widetilde Q_D(e')
 \,\middle|\,
 Q_D(e)=Q_D(e'),\ q(e)\ne q(e')
 \right]>0
\]

for every such pair. This is a separation condition, not a deterministic factorization condition.

*Proof.* The deterministic statement is CH23-P03 applied to the joint chain space and the full spacetime protected map. For the probabilistic statement, if two histories have different protected answers but can generate the same observed record with positive probability, no decoder based only on that record can assign one protected answer to both with certainty. \(\square\)

### Temporal repetition

`WDP-CH23-D14` **Definition (temporal repetition requirement).**  
Suppose a temporal measurement-flip pattern is distinguished from a data-error pattern by requiring a connected space–time error graph to have a minimum homological separation

\[
d_{\mathrm{st}}.
\]

The exact repetition threshold is

\[
R\ge d_{\mathrm{st}}
\]

under the declared convention that one independent detector sample is acquired per round and that the relevant temporal boundary has unit length per round.

For a repetition code in time with adjacent-round syndrome comparisons, \(d_{\mathrm{st}}=L\) gives

\[
R\ge L.
\]

*Proof.* A temporal chain of fewer than \(d_{\mathrm{st}}\) edges cannot meet the declared separation threshold. A chain of length \(d_{\mathrm{st}}\) can meet it, and the chosen space–time boundary then distinguishes the corresponding alternatives. \(\square\)

`WDP-CH23-N05` **Note (dependence of \(R\ge L\) on the premise).**  
The value \(R=L\) follows for the specified temporal repetition model with minimum temporal chain length \(L\). It is not a parameter-free consequence of the toric-code distance alone. If detector errors have a different graph, if samples are reused under a code with a different temporal distance, or if the decision permits probabilistic decoding, the exact threshold must be recomputed from the space–time chain complex.

For rational \(\varepsilon<1/2\), majority repetition of \(R\) independent samples has detector-flip probability

\[
p_R(\varepsilon)
 =
 \sum_{j=\lceil R/2\rceil}^{R}
 \binom Rj\varepsilon^j(1-\varepsilon)^{R-j}.
\]

Thus \(R=L\) is a chain-complex threshold under the declared repetition criterion; it is not an assertion about the smallest number of noisy samples for every error-probability target.

---

## 23.10 Worst-case adaptivity

`WDP-CH23-D15` **Definition (adaptive stabilizer policy).**  
An adaptive policy is a collection of detector sets

\[
D_k:\operatorname{im}Q_{<k}\longrightarrow
 2^{\mathcal S\times\{k\}},
\]

where the set selected in round \(k\) may depend on the observed or noiseless syndrome record from earlier rounds. The accumulated noiseless detector action is

\[
Q_D(e)
 =
 Q_{D_1}(e)+\cdots+Q_{D_R}(e).
\]

In the worst-case noiseless branch, a policy is evaluated on the complete transcript

\[
\mathcal T=(D_1,\ldots,D_R,Q_{<R}).
\]

`WDP-CH23-P17` **Finite proposition (worst-case adaptive non-improvement).**  
Assume:

1. the carrier is \(\mathcal P=\mathbb F_2^n\oplus\mathbb F_2^n\);
2. the protected question is represented by a subgroup \(B\);
3. the worst-case admissible error may be selected after the policy is fixed;
4. the policy receives no prior information identifying the error; and
5. success is required for every \(e\in\mathcal E_t\).

Then an adaptive stabilizer policy cannot increase the worst-case tolerable weight beyond the nonadaptive threshold, and a policy that must distinguish the full logical stabilizer quotient requires at least

\[
2L^2-2
\]

independent stabilizer checks along every worst-case transcript.

*Proof.* The Pauli group modulo phase is an \(\mathbb F_2\)-vector space. Stabilizer measurement acts by a linear syndrome map. If fewer than \(2L^2-2\) independent stabilizer directions are accumulated, the resulting map has a kernel containing a nonzero element

\[
z\in\ker Q_D\setminus B.
\]

The adversary may choose a low-weight representative of the corresponding logical class, subject to the declared weight bound, or a permissible logical cycle. Along the fixed transcript, the two errors \(e\) and \(e+z\) have the same measurements:

\[
Q_D(e+z)
 =
 Q_D(e)+Q_Dz
 =
 Q_D(e).
\]

Their protected answers differ by

\[
q(e+z)+q(e)=q(z)\ne0.
\]

The feedback history does not remove the indistinguishability, because the two histories produce the same transcript along that branch. The adaptive choices on the other branch do not change the worst-case requirement. \(\square\)

`WDP-CH23-P18` **Corollary (full-rank cost).**  
For the standard threshold \(2t<L\), any worst-case adaptive policy that must solve the protected stabilizer question on every error of weight at most \(t\) must accumulate rank

\[
2L^2-2
\]

in the stabilizer measurement matroid. Uniform cost therefore gives the lower bound

\[
|D_{\mathrm{adaptive}}|\ge 2L^2-2
\]

when each measured location counts as one unit.

*Proof.* CH23-P06 gives the full-rank requirement for deterministic separation from the stabilizer group. If the accumulated rank is smaller, a nonzero logical kernel direction remains. The adaptive argument in CH23-P17 places the adversarial pair on that transcript. \(\square\)

`WDP-CH23-N06` **Negative fence.**  
This result concerns worst-case unrestricted Pauli placement and deterministic recovery of the declared protected quotient. It does not exclude adaptive policies for a known error support, a Bayesian noise model, a restricted error family, or a task that accepts a nonzero failure probability. Those cases require a different error class and a different objective.

---

## 23.11 Terminating observer-completion procedure

`WDP-CH23-D16` **Definition (`ToricObserverCompletion`).**  
Given \((\Lambda,\mathcal S,D,\mathcal E,B)\), the procedure is:

1. enumerate the Pauli coordinates appearing in the declared carrier;
2. construct \(H_D\);
3. compute a basis of \(\ker H_D\);
4. enumerate \(\mathcal E-\mathcal E\);
5. test whether
   \[
   (\mathcal E-\mathcal E)\cap\ker H_D\subseteq B;
   \]
6. if the inclusion holds, construct a recovery table;
7. if the inclusion fails, return a pair \(e_1,e_2\) realizing the failed inclusion.

The procedure must distinguish the single-error and spacetime-history versions. For the latter, the same steps are applied to the block history space.

`WDP-CH23-P19` **Finite proposition (termination and correctness).**  
The procedure terminates for every finite declared instance and returns one of the two certificates from CH23-P14.

*Proof.* The carrier, detector set, and admissible set are finite. Matrix construction and Gaussian elimination terminate. The set \(\mathcal E-\mathcal E\) is finite and can be enumerated. The kernel test is a finite sequence of linear-algebra operations.

If the test succeeds, choose one representative \(e_\sigma\) from every nonempty fibre and output the dictionary

\[
\rho(\sigma)=e_\sigma.
\]

By CH23-P03, every error in the fibre differs from \(e_\sigma\) by an element of \(B\), so the dictionary is valid.

If the test fails, select

\[
z\in(\mathcal E-\mathcal E)\cap\ker H_D\setminus B.
\]

By the definition of \(\mathcal E-\mathcal E\), there are \(e_1,e_2\in\mathcal E\) with

\[
z=e_1-e_2.
\]

Then

\[
Q_D e_1=Q_D e_2,
\qquad
q(e_1)\ne q(e_2),
\]

so the returned pair is a dual certificate. \(\square\)

`WDP-CH23-P20` **Finite proposition (complexity statement).**  
Let \(m=|\mathcal E|\), \(d=n=2L^2\), \(r=|D|\), and let \(\mathcal B\) be a basis matrix for \(B\). Kernel computation has arithmetic complexity

\[
O(d^3+d^2r)
\]

over \(\mathbb F_2\), using standard Gaussian elimination. Membership in \(B\) can be tested by reduction modulo a basis, at cost polynomial in \(d\) per candidate.

The direct criterion test has an enumeration cost polynomial in \(m\) and in the representation size of the declared lattice family. For explicit low-weight \(\mathcal E_t\), membership in \(\mathcal E_t\) and enumeration can be bounded in terms of the binomial sum

\[
\sum_{j=0}^t\binom dj.
\]

*Proof.* Gaussian elimination and nullspace computation use a polynomial number of bit operations over \(\mathbb F_2\). The finite difference set has cardinality at most \(m^2\). Testing each difference against a basis of \(B\) is a linear-system operation. The displayed bounds follow from the standard dimensions of the matrices. \(\square\)

The algorithm is exact for finite inputs. Its practical cost may still be substantial when \(t\), \(L\), or the spacetime history space is large.

---

## 23.12 Claim hygiene and boundaries

### 1. What this chapter supports

This chapter supports the following statements under the declared finite carrier, schedule, error set, precision, and protected subgroup:

- The full one-round stabilizer syndrome has kernel \(S\) and logical quotient of dimension \(4\).
- The exact completion condition is
  \[
  (\mathcal E-\mathcal E)\cap\ker Q_D\subseteq B.
  \]
- For \(\mathcal E_t\), \(B=S\), and \(2t<L\), a full independent stabilizer rank of \(2L^2-2\) is sufficient.
- A partial schedule is sufficient exactly when its unresolved subgroup remains inside \(B\).
- Full-rank uniform-cost detector optimization is a binary-matroid basis problem.
- Every finite instance admits either an exact primal recovery certificate or an exact dual failure pair.
- Under the stated unrestricted worst-case assumptions, adaptive stabilizer selection does not improve the full-rank threshold or the full independent-check count.
- Under the declared temporal-chain premise, a minimum temporal separation \(L\) gives \(R\ge L\).

### 2. What this chapter does not support

This chapter does not support claims about:

- a physical toric-code device, its fabrication, calibration, or noise spectrum;
- detector or decoder performance under undeclared stochastic or adversarial noise;
- the sufficiency of \(R\ge L\) for temporal sampling outside the declared chain-complex model;
- a dark window being harmful for every schedule or every restricted error set;
- adaptive policies for restricted supports, Bayesian noise, or probabilistic success criteria;
- a reduction below \(2L^2-2\) measurements for those restricted or probabilistic tasks;
- a general causal-cone statement without the declared local-error model;
- computational practicality for large lattices, large \(t\), or large spacetime histories;
- any statement about consciousness, intelligence, or cognition.

### 3. Narrowest defensible claim

Under the exact finite assumptions declared in this chapter, observer completion is a question of unresolved stabilizer homology. A schedule supports the protected answer precisely when

\[
(\mathcal E-\mathcal E)\cap\ker Q_D\subseteq B.
\]

For the standard \(B=S\) instance with \(2t<L\), full independent stabilizer rank is sufficient, and worst-case unrestricted adaptivity does not lower the independent-check requirement.

### 4. Next test needed

The next test is a calibrated instance study in which:

1. the lattice dimensions and detector-readout error law are measured;
2. the admissible data-error family is estimated from observed fault statistics;
3. the resulting \(\mathcal E\), \(B\), and detector chain are inserted into the exact kernel test;
4. the primal recovery table or dual failure pair is checked on the complete declared finite instance; and
5. the predicted threshold is compared with held-out fault data.

This test would connect the finite algebra to a declared experimental regime. It would not by itself extend the theorem beyond that regime.
