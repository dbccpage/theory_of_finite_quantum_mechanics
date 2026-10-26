<div align="center">

# Mutually Unbiased Bases in Dimension Six: Proofs of the Reductions

**Author:** Jeremy H. Carroll

**Date:** 2026-10-26

**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)

</div>

## Introduction

This note gives written proofs of the results of [mub6.md](mub6/mub6.md) that the derivation DAG
(`dag/derivation_dag.json`) records as proved in Lean. Each section states one result, proves it,
and names the Lean declarations that check it. The DAG identifier is on the line beginning
*DAG node*.

None of these results decides whether $\mathbb C^6$ has four mutually unbiased bases. They are
reformulations of that question (as equivalent polynomial systems, moment problems or ray
problems), explicit complex Hadamard matrices, exclusions of particular boxes, and soundness
statements for exclusion methods. Each section says which of these it is.

**Notation.** $A^*$ is the conjugate transpose. A *raw Hadamard* matrix is $H\in\mathbb
C^{6\times6}$ with $|H_{ij}|=1$ and $H^*H=6I$ (equivalently $HH^*=6I$, since $H$ is square).
Raw matrices $A,B$ are *raw unbiased* if $|(A^*B)_{ij}|^2=6$ for all $i,j$. A *quartet* is four
orthonormal bases of $\mathbb C^6$, written as unitary matrices $B_0,\dots,B_3$, with
$|(B_a^*B_b)_{ij}|^2=1/6$ for $a\ne b$. A *monomial* matrix is a permutation matrix times a
diagonal matrix of unit phases; $H$ and $K$ are *Hadamard equivalent* if $K=PHQ$ with $P,Q$
monomial. $\omega=e^{2\pi i/3}$. All Lean paths are relative to the repository root.

---

## 1. Normal forms of the quartet problem

### 1.1 Quartets are raw quartets, and raw quartets are invariant under equivalence

DAG node: `MUB6-QUARTET-RAW-HADAMARD-TRANSPORT`

**Proposition.** Say $H$ has a *raw quartet* if $H$ is raw Hadamard and there are raw Hadamard
$U,V$ with $H,U$ and $H,V$ and $U,V$ pairwise raw unbiased.

1. A quartet exists if and only if some $H$ has a raw quartet.
2. If $K=PHQ$ with $P,Q$ monomial, then $H$ has a raw quartet if and only if $K$ has one.
3. Consequently, if a set $S$ contains a Hadamard-equivalent representative of every raw
   Hadamard matrix and no member of $S$ has a raw quartet, no quartet exists.

*Proof.* (1) Given a quartet, put $H=\sqrt6\,B_0^*B_1$, $U=\sqrt6\,B_0^*B_2$,
$V=\sqrt6\,B_0^*B_3$. Unbiasedness of $B_0$ with $B_a$ says $|H_{ij}|=|U_{ij}|=|V_{ij}|=1$;
unitarity gives $H^*H=6I$ and the same for $U,V$; and
$H^*U=6B_1^*B_0B_0^*B_2=6B_1^*B_2$ has squared entry moduli $36\cdot\frac16=6$, and likewise for
$H^*V$ and $U^*V$. Conversely, given a raw quartet $(H,U,V)$, the matrices
$I,\;H/\sqrt6,\;U/\sqrt6,\;V/\sqrt6$ are unitary and the same three computations, read
backwards, show they are pairwise unbiased.

(2) Write $P=\Pi D$ with $\Pi$ a permutation and $D$ diagonal unitary. Apply $P$ on the left to
all three matrices and independent monomials on the right: $H'=PHQ$, $U'=PUQ_2$, $V'=PVQ_3$ with
$Q_2=Q_3=I$ allowed. Entry moduli are permuted, so unit entries are preserved.
$H'^*H'=Q^*H^*P^*PHQ=6I$ because $P$ and $Q$ are unitary. Finally
$H'^*U'=Q^*(H^*U)Q_2$, whose entries are those of $H^*U$ permuted and multiplied by unit
phases, so the moduli $\sqrt6$ are kept. The inverse transformation is again monomial, giving
the converse.

(3) A quartet gives, by (1), a raw quartet for some $H$; by hypothesis $H$ is equivalent to some
$K\in S$; by (2) $K$ has a raw quartet, a contradiction. $\square$

The left factor must be a single monomial applied to all three matrices: it is the stabilizer of
the standard basis $B_0=I$ up to phases. Applying different row operations to one matrix only
does not preserve unbiasedness.

Lean: `lean4/MubQuartetTransportBridge.lean::exists_quartet_iff_exists_rawQuartet`,
`lean4/MubMonomialTransport.lean::hasRawQuartet_iff_of_monomialEquivalent`,
`lean4/MubQuartetTransportBridge.lean::no_quartet_of_concrete_representatives`.

### 1.2 A transition-balance identity

DAG node: `MUB6-TRANSITION-BALANCE-SYZYGY`

**Proposition.** Let $R$ be a commutative ring with an involution $z\mapsto\bar z$, let
$A,B\in R^{6\times6}$ and $W=A^*B$. Put
$g_{Aj}=A_{0j}-1$, $g_{Bk}=B_{0k}-1$ and $R_{Bm}=\sum_kB_{mk}\overline{B_{0k}}-6\delta_{m0}$.
Then, with no assumption on the residuals,

$$
\sum_kW_{jk}-6=\sum_m\overline{A_{mj}}\,R_{Bm}-\sum_{m,k}\overline{A_{mj}}B_{mk}\overline{g_{Bk}}
+6\,\overline{g_{Aj}},
$$

and the conjugate identity with the roles of rows and columns exchanged holds for
$\sum_jW_{jk}-6$. In particular, if $AA^*=BB^*=6I$ (so the row and column residuals vanish) and the first rows of $A$ and
$B$ are all ones, then every row sum and every column sum of $A^*B$ equals $6$.

*Proof.* Substitute $\overline{B_{0k}}=1+\overline{g_{Bk}}$ in $R_{Bm}$:
$\overline{A_{mj}}R_{Bm}=\sum_k\overline{A_{mj}}B_{mk}+\sum_k\overline{A_{mj}}B_{mk}\overline{g_{Bk}}
-6\delta_{m0}\overline{A_{mj}}$. Summing over $m$, the double sum cancels the second term on the
right, leaving $\sum_{m,k}\overline{A_{mj}}B_{mk}-6\overline{A_{0j}}+6(\overline{A_{0j}}-1)
=\sum_kW_{jk}-6$. For the column identity apply the row identity to the pair $(B,A)$, whose
transition is $W^*$, and conjugate. The last sentence follows because every term on the right
contains a vanishing residual. $\square$

The identity is an explicit ideal membership, so adding the balance equations to a polynomial
system with the Gram and gauge equations does not change its solution set.

Lean: `lean4/MubGaugeSyzygy.lean::row_balance_syzygy`,
`lean4/MubGaugeSyzygy.lean::column_balance_syzygy`,
`lean4/MubGaugeSyzygy.lean::balanceResidual_zero`.

### 1.3 A well-conditioned $3\times3$ minor

DAG node: `MUB6-CAUCHY-BINET-MINOR-BOUND`

**Proposition.** Let $H$ be raw Hadamard and let $A$ be its first three rows. Some $3\times3$
minor $B=A_{[:,S]}$ has $|\det B|^2\ge 54/5$. It is invertible and
$|(B^{-1})_{ij}|^2\le 10/27$ for all $i,j$.

*Proof.* $AA^*=6I_3$ because the rows of $H$ are orthogonal of squared norm $6$. By the
Cauchy–Binet formula,
$\sum_{|S|=3}|\det A_{[:,S]}|^2=\det(AA^*)=216$. There are $\binom63=20$ subsets, so the
largest term is at least $216/20=54/5$. Each entry of $\operatorname{adj}B$ is, up to sign, a
$2\times2$ minor $xy-zw$ of unit-modulus numbers, so $|\operatorname{adj}(B)_{ij}|\le2$. Hence
$|(B^{-1})_{ij}|^2=|\operatorname{adj}(B)_{ij}|^2/|\det B|^2\le 4\cdot\frac5{54}=\frac{10}{27}$.
$\square$

Lean: `lean4/MubMinorChart.lean::exists_minor_norm_ge` (the averaging step, for any
$A$ with $AA^*=6I_3$), `lean4/MubMinorChart.lean::inverse_entry_normSq_le`,
`lean4/MubMinorChart.lean::exists_bounded_inverse_minor`.

### 1.4 A bounded block chart and division-free equations

DAG node: `MUB6-BOUNDED-BLOCK-QUARTET-EQUATIONS`

**Proposition.** Call $(E,B,C)\in(\mathbb C^{3\times3})^3$ *admissible* if $E,B,C$ have unit
entries, the first row and column of $E$, the first row of $B$ and the first column of $C$ are
all ones, $|\det B|^2\ge54/5$, $EE^*+BB^*=6I$, and the matrix $D=-CE^*(B^{-1})^*$ has unit
entries and satisfies $CC^*+DD^*=6I$. Then a quartet exists if and only if for some admissible
$(E,B,C)$ the matrix

$$
H=\begin{pmatrix}E&B\\C&D\end{pmatrix}
$$

has a raw quartet. Writing $d=\overline{\det B}$, $q=|d|^2$, $N=-CE^*(\operatorname{adj}B)^*$
and $S=\begin{pmatrix}dE&dB\\dC&N\end{pmatrix}$, this is equivalent to the solvability of the
division-free system: the unit-entry, gauge and $EE^*+BB^*=6I$ conditions on $E,B,C$;
$q\ge54/5$; $|N_{ij}|^2=q$; $qCC^*+NN^*=6qI$; raw Hadamard $U,V$ with first rows all ones; and

$$
|(S^*U)_{ij}|^2=6q,\qquad|(S^*V)_{ij}|^2=6q,\qquad|(U^*V)_{ij}|^2=6.
$$

*Proof.* Suppose $H_0$ has a raw quartet. By §1.3 three columns of its first three rows form a
minor with $|\det|^2\ge54/5$. Permute the columns so that these come last, and then dephase:
multiply rows and columns by unit phases so that the first row and the first column become all
ones. Column permutation and phase multiplication are monomial, so by §1.1 the result $H$ still
has a raw quartet; they change the minor's determinant only by a unit factor. Write $H$ in
$3+3$ blocks. The off-diagonal block of $HH^*=6I$ reads $CE^*+DB^*=0$, so
$D=-CE^*(B^*)^{-1}=-CE^*(B^{-1})^*$, and the diagonal blocks give the two Gram equations. So
$(E,B,C)$ is admissible. Conversely, for admissible data the formula for $D$ makes the
off-diagonal blocks of $HH^*$ vanish and the Gram equations make the diagonal blocks $6I$, so
$H$ is raw Hadamard; if it has a raw quartet, a quartet exists by §1.1.

For the second form, $B^{-1}=\operatorname{adj}B/\det B$ gives $dD=N$ and $dH=S$. Since $q>0$,
$|D_{ij}|=1\iff|N_{ij}|^2=q$, $CC^*+DD^*=6I\iff qCC^*+NN^*=6qI$, and
$|(H^*U)_{ij}|^2=6\iff|(S^*U)_{ij}|^2=|d|^2\cdot6=6q$. The first rows of $U$ and $V$ can be set
to ones by right multiplication with diagonal phases, which preserves all three unbiasedness
conditions. $\square$

The determinant bound is what makes the clearing of denominators reversible. In
`MubBoundedMUFactor.lean` the polynomial MU residuals are further divided by the factor $q$,
which is again reversible because $q\ge54/5$.

Lean: `lean4/MubBoundedBlockChart.lean::exists_quartet_iff_bounded_completion`,
`lean4/MubBoundedQuartetEquations.lean::exists_quartet_iff_equations`,
`lean4/MubBoundedMUFactor.lean::exists_quartet_iff_reduced`.

### 1.5 A quadratic system in 386 bounded coordinates

DAG node: `MUB6-QUADRATIC-LIFT-386`

**Proposition.** Introduce as unknowns the free entries of $E,B,C$ and of $U,V$ (after the
gauge constants of §1.4 are substituted: 76 complex entries), the nine entries of $D$, and three
transition matrices $W_0,W_1,W_2\in\mathbb C^{6\times6}$; in real and imaginary parts this is
$152+18+216=386$ real coordinates. Consider the 648 real equations

- $|z|^2=1$ for every entry $z$ of $H,U,V$ (108),
- $H^*H=U^*U=V^*V=6I$ (216 real components),
- $W_0=H^*U$, $W_1=H^*V$, $W_2=U^*V$ (216 real components),
- $|(W_a)_{ij}|^2=6$ (108).

Every equation has total degree at most two. A quartet exists if and only if this system has a
real solution in $[-1,1]^{170}\times[-3,3]^{216}$, and also if and only if it has one with the
216 transition coordinates in $[-10035/4096,\,10035/4096]$.

*Proof.* A solution is precisely a raw Hadamard $H$ in the form of §1.4 together with raw
Hadamard $U,V$ whose pairwise transitions have entries of squared modulus $6$, that is, a raw
quartet for $H$. By §1.4 and §1.1 such data exist if and only if a quartet exists; the reverse
direction does not use the determinant bound, since all three matrices are given in full. Each
equation is a sum of products of at most two unknowns. On a solution every entry of $H,U,V$ has
modulus one, so its real and imaginary parts lie in $[-1,1]$, and every transition entry has
modulus $\sqrt6$, so its parts lie in $[-\sqrt6,\sqrt6]$. Since
$\sqrt6<10035/4096<3$ (indeed $(10035/4096)^2=6.0023\ldots$), restricting to either box loses
no solution. $\square$

The Lean module carries the 648 rows as literal coefficient lists and checks by kernel
reduction that they equal the defining polynomials (`rows_match`).

Lean: `lean4/MubQuadraticLiftTable.lean::exists_quartet_iff_table`,
`lean4/MubQuadraticLiftTable.lean::rows_match`,
`lean4/MubQuadraticLiftNarrowBox.lean::exists_quartet_iff_narrow_table`.

### 1.6 Affine completion of the balanced transitions: 320 coordinates

DAG node: `MUB6-BALANCED-648-QUADRATIC`

**Proposition.** A $6\times6$ matrix $W$ over a commutative ring with all row and column sums
equal to $6$ is determined by its leading $5\times5$ block $A$:

$$
W_{i5}=6-\sum_{j<5}A_{ij},\qquad W_{5j}=6-\sum_{i<5}A_{ij},\qquad
W_{55}=\sum_{i,j<5}A_{ij}-24,
$$

and every $5\times5$ block $A$ arises this way. Substituting these formulas for $W_0,W_1,W_2$
in the system of §1.5 gives 648 rational equations of degree at most two in $386-66=320$
coordinates, and a quartet exists if and only if this system has a solution in
$[-1,1]^{170}\times[-10035/4096,10035/4096]^{150}$.

*Proof.* The formulas for the last column and last row are the row and column sum conditions.
For the corner, the last row sums to six:
$W_{55}=6-\sum_{j<5}W_{5j}=6-\sum_{j<5}\bigl(6-\sum_{i<5}A_{ij}\bigr)=\sum_{i,j}A_{ij}-24$.
Conversely, the completed matrix has row and column sums six by construction (the corner
formula makes the last row and the last column consistent). On a solution of §1.5, $H,U,V$ have
first rows all ones and Gram matrix $6I$, so by §1.2 each transition $W_a$ has all row and column
sums six; hence each $W_a$ equals the completion of its block. Conversely a solution of the
reduced system completes to a solution of §1.5. The substitution is affine, so degrees do not
increase. The box condition on the 150 retained transition coordinates follows from §1.5. $\square$

The recovered last row and column of a point in the reduced box need not lie in the old box:
the all-zero block completes to a corner entry $-24$. The equivalence is between solution sets,
not between boxes.

Lean: `lean4/MubBalancedCompletion.lean::complete_restrict`,
`lean4/MubBalancedCompletion.lean::restrict_complete`,
`lean4/MubBalancedQuadraticPolynomials.lean::exists_quartet_iff_balanced_polynomials`,
`lean4/MubBalancedQuadraticPolynomials.lean::equation_degree`.

### 1.7 Two transition columns cannot be close

DAG node: `MUB6-CLOSE-COLUMNS-EXCLUSION`

**Proposition.** On every solution of §1.5 and every pair $i,j$,

$$
\sum_k\bigl|(W_0)_{ki}-(W_1)_{kj}\bigr|^2=72-12\operatorname{Re}(W_2)_{ij}\ge
72-12\sqrt6>\frac{43623}{1024}.
$$

Hence no solution has a column $i$ of $W_0$ and a column $j$ of $W_1$ whose real parts all lie
in $[9/10,11/10]$ and whose imaginary parts lie within $1/20$ of common centres $c_k$.

*Proof.* $W_0^*W_0=U^*HH^*U=36I$, so each column of $W_0$ has squared norm $36$, and likewise for
$W_1$. Also $W_0^*W_1=U^*HH^*V=6U^*V=6W_2$. Expanding,
$\sum_k|(W_0)_{ki}-(W_1)_{kj}|^2=36+36-2\operatorname{Re}(W_0^*W_1)_{ij}=72-12\operatorname{Re}(W_2)_{ij}$.
Since $|(W_2)_{ij}|=\sqrt6$, this is at least $72-12\sqrt6=42.606\ldots$, and
$43623/1024=42.6006\ldots$. In the stated region each real difference has modulus at most
$1/5$ and each imaginary difference at most $1/10$, so the left side is at most
$6\bigl(\frac1{25}+\frac1{100}\bigr)=\frac3{10}$. $\square$

This excludes one family of regions. It is not a cover of the solution box.

Lean: `lean4/MubQuadraticTransitionSeparation.lean::close_columns_box_excluded`.

---

## 2. Explicit complex Hadamard matrices

Each matrix below has unit-modulus entries by inspection ($\omega$, $i$ and the parameters are
unit complex numbers), so only $HH^*=6I$ needs proof. The names follow the Lean module; this
note does not prove that a matrix is equivalent to the matrix of the same name in the literature.

### 2.1 The Fourier–Diţă matrix

DAG node: `MUB6-FOURIER-DITA-FAMILY-CHM`

**Proposition.** Let $F=(\omega^{jk})_{j,k=0}^2$ and $\Delta=\operatorname{diag}(a,b,c)$ with
$|a|=|b|=|c|=1$. The matrix
$H=\begin{pmatrix}F&\Delta F\\F&-\Delta F\end{pmatrix}$ satisfies $HH^*=6I$.

*Proof.* $FF^*=3I$ and $\Delta\Delta^*=I$, so
$HH^*=\begin{pmatrix}FF^*+\Delta FF^*\Delta^*&FF^*-\Delta FF^*\Delta^*\\
FF^*-\Delta FF^*\Delta^*&FF^*+\Delta FF^*\Delta^*\end{pmatrix}
=\begin{pmatrix}6I&0\\0&6I\end{pmatrix}$. $\square$

The Lean matrix `fourierDitaMatrix` is this $H$ written out entry by entry.

Lean: `lean4/MasterClassification.lean::fourierDitaMatrix_isCH6`.

### 2.2 The two-phase affine (Karlsson) matrix

DAG node: `MUB6-KARLSSON-AFFINE-ANSATZ`

**Proposition.** Index rows by $(k,s)$ and columns by $(m,t)$ with $k,m\in\{0,1,2\}$ and
$s,t\in\{0,1\}$ (row $2k+s$, column $2m+t$). Let $\varphi_0=(1,1,1)$ and $\varphi_1=(1,x,y)$
with $|x|=|y|=1$. The matrix
$H_{(k,s),(m,t)}=\omega^{km}\,(\varphi_s)_m\,(-1)^{st}$ satisfies $HH^*=6I$.

*Proof.*
$(HH^*)_{(k,s),(k',s')}=\sum_m\omega^{(k-k')m}(\varphi_s)_m\overline{(\varphi_{s'})_m}\sum_t(-1)^{(s-s')t}$.
The inner sum is $2\delta_{ss'}$. When $s=s'$, $|(\varphi_s)_m|=1$ and the outer sum is
$\sum_m\omega^{(k-k')m}=3\delta_{kk'}$. $\square$

Lean: `lean4/MasterClassification.lean::karlssonMatrix_isCH6`.

### 2.3 The Tao matrix

DAG node: `MUB6-TAO-MATRIX-CHM`

**Proposition.** Let $S_{rj}=\omega^{e_{rj}}$ with exponent table

$$
e=\begin{pmatrix}
0&0&0&0&0&0\\0&0&1&1&2&2\\0&1&0&2&2&1\\0&1&2&0&1&2\\0&2&2&1&0&1\\0&2&1&2&1&0
\end{pmatrix}.
$$

Then $SS^*=6I$.

*Proof.* For rows $r\ne r'$, $(SS^*)_{rr'}=\sum_j\omega^{e_{rj}-e_{r'j}}$. For each of the
fifteen pairs, the six differences $e_{rj}-e_{r'j}$ take each residue modulo $3$ exactly twice
(row $0$ against row $r$: each nonzero row contains each residue twice; the ten pairs of nonzero
rows are checked from the table). So the sum is $2(1+\omega+\omega^2)=0$. $\square$

Lean: `lean4/MasterClassification.lean::taoMatrix_isCH6`.

### 2.4 A $\{1,-1,i\}$ matrix

DAG node: `MUB6-HAAGERUP-MATRIX-CHM`

**Proposition.** The matrix

$$
H=\begin{pmatrix}
1&1&i&1&1&-1\\ i&1&1&-1&1&1\\ 1&i&1&1&-1&1\\
1&-1&1&-1&i&-1\\ 1&1&-1&-1&-1&i\\ -1&1&1&i&-1&-1
\end{pmatrix}
$$

satisfies $HH^*=6I$.

*Proof.* For each of the fifteen pairs of distinct rows $r,r'$, the six products
$H_{rj}\overline{H_{r'j}}$ consist of $i$, $-i$, $1$, $1$, $-1$, $-1$ in some order (direct
inspection of the table), so they sum to zero. $\square$

Lean: `lean4/MasterClassification.lean::haagerupMatrix_isCH6`.

### 2.5 The two-circulant family

DAG node: `MUB6-SZOLLOSI-TWO-CIRCULANT`

**Proposition.** Let $A,B$ be $3\times3$ circulants with first rows $(a_0,a_1,a_2)$,
$(b_0,b_1,b_2)$ of unit phases, and put
$z(a)=a_0\bar a_2+a_1\bar a_0+a_2\bar a_1$. If $z(a)+z(b)=0$ then
$H=\begin{pmatrix}A&B\\B^*&-A^*\end{pmatrix}$ satisfies $HH^*=6I$; so $H/\sqrt6$ is unitary and
its entries have squared modulus $1/6$. With $\phi(x,y)=x+y+\overline{xy}$ and phase rows
$(1,x,xy)$, $(1,u,uv)$, one has $z=\phi(x,y)$ and $z=\phi(u,v)$, so the admissible parameters
are the real solutions of six equations in eight real unknowns:
$|x|=|y|=|u|=|v|=1$ and $\phi(x,y)+\phi(u,v)=0$. A number $\alpha$ lies in both
$\phi(\mathbb T^2)$ and $-\phi(\mathbb T^2)$ if and only if some admissible parameter has
$\phi(x,y)=\alpha$.

*Proof.* Circulants commute with each other and with their adjoints. Hence
$HH^*=\begin{pmatrix}AA^*+BB^*&AB-BA\\B^*A^*-A^*B^*&B^*B+A^*A\end{pmatrix}
=\begin{pmatrix}AA^*+BB^*&0\\0&AA^*+BB^*\end{pmatrix}$. The matrix $AA^*$ is circulant with
diagonal $\sum|a_k|^2=3$ and off-diagonal entries $z(a)$ and $\overline{z(a)}$; similarly for
$B$. So $AA^*+BB^*=6I$ exactly when $z(a)+z(b)=0$. For $(a_0,a_1,a_2)=(1,x,xy)$,
$z=\overline{xy}+x+xy\bar x=\phi(x,y)$. The last statement is a restatement: $\alpha=\phi(x,y)$
and $-\alpha=\phi(u,v)$ is the same as $\phi(x,y)+\phi(u,v)=0$ with $\phi(x,y)=\alpha$. $\square$

Lean: `lean4/SzollosiTwoCirculant.lean::rawSix_gram`,
`lean4/SzollosiTwoCirculant.lean::normalized_unitary`,
`lean4/SzollosiTwoCirculant.lean::normalized_entry_modulus`,
`lean4/SzollosiTwoCirculant.lean::parameter_covers_intersection`,
`lean4/MasterClassification.lean::szollosiMatrix_isCH6` (the same block form with six free
phases).

### 2.6 Dephasing and the corner split

DAG node: `MUB6-CORNER-ROUTING-DEPHASING`

**Proposition.** Every raw Hadamard $H$ is Hadamard equivalent to a raw Hadamard $D$ whose first
row and first column are all ones, and either $\det D_{[0..2],[0..2]}=0$ or it is nonzero.

*Proof.* Put $D=\operatorname{diag}(\overline{H_{i0}})\,H\,\operatorname{diag}(H_{00}\overline{H_{0j}})$.
Then $D_{i0}=\overline{H_{i0}}H_{i0}H_{00}\overline{H_{00}}=1$ and
$D_{0j}=\overline{H_{00}}H_{0j}H_{00}\overline{H_{0j}}=1$; $D$ is equivalent to $H$ and raw
Hadamard by §1.1. With first row and column ones, the leading $3\times3$ determinant is
$ad-bc-a+b+c-d$ in the entries $a=D_{11},b=D_{12},c=D_{21},d=D_{22}$; it is zero or not. $\square$

The Lean theorem attaches a family label to each case. The label is a name: no parametrization of
either case by a known family is proved.

Lean: `lean4/MasterClassification.lean::dephase_and_route_corner`,
`lean4/MasterClassification.lean::corner_routing_classification`.

---

## 3. The two-circulant quartet problem

Throughout this part, $H$ is the two-circulant matrix of §2.5 at an admissible parameter, and the
quartet in question is $(I,\,H/\sqrt6,\,U/\sqrt6,\,V/\sqrt6)$ with $U,V$ arbitrary.

### 3.1 Common rays

DAG node: `MUB6-SZOLLOSI-COMMON-RAYS`

**Proposition.** For raw Hadamard $H$ call $z\in\mathbb C^6$ a *common ray* if $z_0=1$,
$|z_i|=1$ for all $i$, and $|\langle H_{\cdot k},z\rangle|^2=6$ for every column $k$ of $H$.
Then $H$ has a raw quartet if and only if there are raw Hadamard $U,V$, all of whose columns are
common rays, with $U,V$ raw unbiased. In particular, if no two common rays $z,w$ satisfy
$|\langle z,w\rangle|^2=6$, then $H$ has no raw quartet.

*Proof.* If $(H,U,V)$ is a raw quartet, multiply each column of $U$ and of $V$ by the conjugate
of its first entry. This is a right diagonal phase, which preserves raw Hadamard and all three
unbiasedness conditions (§1.1), and it makes every column a common ray: unit entries express
unbiasedness with $I$, and the overlaps with columns of $H$ are the entries of $H^*U$. The
converse reads the same facts backwards. For the corollary, the first columns of $U$ and $V$
would be common rays with $|\langle z,w\rangle|^2=|(U^*V)_{00}|^2=6$. $\square$

No finiteness of the set of common rays is used.

Lean: `lean4/SzollosiCommonRays.lean::quartet_iff_ray_bases`,
`lean4/SzollosiCommonRays.lean::no_quartet_of_no_unbiased_ray_pair`.

### 3.2 A quadratic system with 618 equations in 440 unknowns

DAG node: `MUB6-SZOLLOSI-618-SYSTEM`

**Proposition.** Take as unknowns the eight real phase coordinates $(x,y,u,v)$, the 36 complex
entries of the family matrix, the entries of raw $U,V$, and three auxiliary matrices
$X_{HU},X_{HV},X_{UV}$ (440 real unknowns). Impose: the six parameter equations of §2.5; the
72 real ties of the family-matrix entries to the phases; $U^*U=V^*V=6I$ (144); unit entries of
$U,V$ (72); $X_{HU}=H^*U$, $X_{HV}=H^*V$, $X_{UV}=U^*V$ (216); and $|X_{ij}|^2=6$ for all three
(108). Every equation has rational coefficients and total degree at most two. The system has a
real solution if and only if some admissible parameter admits a quartet of the stated form;
for each fixed admissible parameter the same holds with the phase coordinates fixed. Every
solution lies in the box with radius $1$ for the phase, family and $U,V$ coordinates and radius
$3$ for the auxiliary coordinates. Every matrix unbiased to $I$ after normalization has all real
and imaginary parts in $[-1/2,1/2]$.

*Proof.* The ties $(1,x,xy)$ involve products of two phases, which is why the family entries
are separate unknowns; with them all equations are of degree at most two. A solution is exactly
an admissible parameter, the matrix $H$ of §2.5, and raw Hadamard $U,V$ unbiased to $I$ (unit
entries), to $H$ and to each other ($|X|^2=6$), i.e. a raw quartet $(H,U,V)$, which is a quartet
of the stated form by §1.1. The box bounds come from unit modulus and modulus $\sqrt6<3$. A
normalized matrix unbiased to $I$ has $|U_{ij}|^2=1/6$, so its parts are at most
$1/\sqrt6<1/2$ in modulus. $\square$

Lean: `lean4/SzollosiQuartetSystem.lean::quartet_iff_candidate_equations`,
`lean4/SzollosiQuartetSystem.lean::mu_identity_coordinates_bounded`,
`lean4/SzollosiQuadraticSystem.lean::equation_degree`,
`lean4/SzollosiQuadraticSystem.lean::exists_solution_iff_quartet`,
`lean4/SzollosiQuadraticSystem.lean::exists_solution_with_parameters_iff`,
`lean4/SzollosiQuadraticSystem.lean::solution_in_full_box`,
`lean4/SzollosiQuadraticSystem.lean::exists_bounded_solution_iff_quartet`.

### 3.3 Gauge, balance and six charts: 666 equations

DAG node: `MUB6-SZOLLOSI-GAUGED-666`

**Proposition.** At each admissible parameter, adding to the system of §3.2 the 24 real
equations "the first rows of $U$ and $V$ are all ones" and the 24 real equations "every row and
column sum of $X_{UV}$ equals $6$" does not change whether a quartet of the stated form exists.
Every solution of the 666 equations lies in one of six charts $\{\operatorname{Re}(X_{UV})_{0j}\ge1\}$,
$j=0,\dots,5$.

*Proof.* Right multiplication of $U$ and $V$ by diagonal phases sets their first rows to ones and
preserves every equation of §3.2 (§1.1), so the gauge loses no quartet. Given the gauge and
$UU^*=VV^*=6I$, §1.2 shows that all row and column sums of $U^*V$ equal $6$, so the balance
equations hold on every gauged solution. For the charts, the six real parts of the first row of
$X_{UV}$ sum to $6$, so at least one is at least $1$. $\square$

Lean: `lean4/SzollosiColumnGauge.lean::exists_gauge_box_solution_with_parameters_iff`,
`lean4/SzollosiGaugeBalance.lean::solution_balance_equations`,
`lean4/SzollosiGaugedExecutable.lean::augmented_exists_with_parameters_iff`,
`lean4/SzollosiGaugedCover.lean::augmented_solution_chart_cover`,
`lean4/SzollosiGaugedReflection.lean::native_chart_quartet_iff`.

### 3.4 A candidate box excluded by balance

DAG node: `MUB6-SZOLLOSI-BOX-368-EXCLUSION`

**Proposition.** No solution of the 666 equations has all six real parts
$\operatorname{Re}(X_{UV})_{0j}$ in $[-1/2,1/2]$. The box in which these six coordinates are so
restricted (and the others are as in §3.2) contains points with admissible phases, for example
$(x,y,u,v)=(1,-1,1,i)$.

*Proof.* The balance equation gives
$\operatorname{Re}(X_{UV})_{00}=6-\sum_{j=1}^5\operatorname{Re}(X_{UV})_{0j}\in[6-\tfrac52,6+\tfrac52]=[\tfrac72,\tfrac{17}2]$,
which is disjoint from $[-1/2,1/2]$. For the phase point, $\phi(1,-1)=1-1-1=-1$ and
$\phi(1,i)=1+i-i=1$, so $\phi(x,y)+\phi(u,v)=0$. $\square$

In the formal coordinate numbering, $\operatorname{Re}(X_{UV})_{00}$ is coordinate 368. The phase
point is not a quartet; it shows only that the box is not excluded for the trivial reason of
containing no admissible parameter.

Lean: `lean4/SzollosiGaugedReflection.lean::native_box_exclusion`,
`lean4/SzollosiGaugedReflection.lean::native_box_has_admissible_phase_point`.

### 3.5 Soundness of rectangular Krawczyk exclusion for quadratic systems

DAG node: `MUB6-RECTANGULAR-KRAWCZYK-SOUNDNESS`

**Proposition.** Let $f_1,\dots,f_m$ be real polynomials of degree at most two in
$r\in\mathbb R^n$, let $X=\prod_k[\ell_k,u_k]$ be a box, $c\in X$ a rational point and
$C\in\mathbb Q^{n\times m}$ any matrix. Let $J$ be an interval enclosure of the Jacobian
$\partial f_e/\partial r_k$ over $X$, and

$$
K_i=c_i-\sum_eC_{ie}f_e(c)+\sum_k\Bigl(\delta_{ik}-\sum_eC_{ie}J_{ek}\Bigr)\,(X_k-c_k)
$$

in interval arithmetic. Every zero $r\in X$ of all $f_e$ satisfies $r_i\in K_i$. Hence if
$K_i\cap[\ell_i,u_i]=\emptyset$ for some $i$, the system has no zero in $X$.

*Proof.* For a polynomial of degree at most two, the midpoint rule is exact:
$f(r)-f(c)=\nabla f\bigl(\tfrac{r+c}2\bigr)\cdot(r-c)$. It suffices to check monomials: it is
trivial for constants and linear terms, and
$r_kr_l-c_kc_l=\tfrac{r_l+c_l}2(r_k-c_k)+\tfrac{r_k+c_k}2(r_l-c_l)$ (including $k=l$). If $r$ is
a zero, then
$0=\sum_eC_{ie}f_e(r)=\sum_eC_{ie}f_e(c)+\sum_k\sum_eC_{ie}\,\partial_kf_e(\tfrac{r+c}2)(r_k-c_k)$,
so
$r_i=c_i-\sum_eC_{ie}f_e(c)+\sum_k\bigl(\delta_{ik}-\sum_eC_{ie}\partial_kf_e(\tfrac{r+c}2)\bigr)(r_k-c_k)$.
The midpoint lies in $X$ because $X$ is convex, so each derivative lies in $J_{ek}$, and
$r_k-c_k\in X_k-c_k$. Interval arithmetic is inclusion-monotone, so $r_i\in K_i$. If
$K_i$ misses $[\ell_i,u_i]$, no such $r$ exists. $\square$

No inverse of $C$, no squareness ($m=n$) and no particular choice of $C$ is needed for
exclusion. Square-system existence versions require their stated hypotheses, including an invertible preconditioner. Strict inclusion of $K$ in $X$ alone does not establish a zero for an overdetermined system; only separation is used here. Applied to the 618-equation system of
§3.2 on its containing box, a successful separation check would exclude every quartet of that
form. No such successful check is recorded.

Lean: `lean4/RectangularQuadraticExclusion.lean::list_secant_identity`,
`lean4/RectangularQuadraticExclusion.lean::root_in_image`,
`lean4/RectangularQuadraticExclusion.lean::exclusion_sound`,
`lean4/SzollosiRectangularExclusion.lean::no_quartet_of_check`.

### 3.6 What certified membership in the 56-cell cover means

DAG node: `MUB6-COVER56-CURVATURE-PREMISE`

**Proposition.** For the stored 56-cell cover and a point $p$, certified membership holds if and
only if $p$ lies in some cell and $p$'s triple carries a curvature certificate.

*Proof.* Certified membership is defined as: there is a cell $i$ with $p\in i$ such that
$p\in i$ implies a curvature certificate for $p$'s triple. From this, $p$ lies in a cell and the
certificate follows by applying the implication. Conversely, given a cell containing $p$ and a
certificate, the implication holds trivially. $\square$

The point of the statement is negative: the 56 stored interval cells and their margins do not
produce the curvature certificate; any theorem using certified membership assumes it.

Lean: `lean4/TargetA12SmaleSentry.lean::certified_point_in_cover56_iff`.

---

## 4. Fixed triples, moments and extraction

In this part $T=(T_0,T_1,T_2)$ is a fixed triple of complex $6\times6$ matrices and a *fourth
basis* for $T$ is a unitary $U$ with $|\langle(T_a)_{\cdot i},U_{\cdot j}\rangle|^2=1/6$ for all
$a,i,j$. A candidate $U$ is encoded by its 72 real and imaginary parts.

### 4.1 The fixed-triple variety

DAG node: `MUB6-FIXED-TRIPLE-VARIETY`

**Proposition.** Let $r_{a,i,j}(U)=|\langle(T_a)_{\cdot i},U_{\cdot j}\rangle|^2-1/6$ and let
$s(U)$ be the 72 real and imaginary parts of $U^*U-I$. Then
(i) $r_{a,i,j}(U)=\operatorname{tr}(P_{T_a,i}P_{U,j})-1/6$, where $P_{M,i}=M_{\cdot i}M_{\cdot i}^*$ is the column outer product (a projector when the column has unit norm);
(ii) a real point $x$ is a common zero of the ideal generated by all $r$ and $s$ if and only if
every generator vanishes at $x$;
(iii) the real zero set is empty if and only if $T$ has no fourth basis;
(iv) if $T$ consists of three bases of a family of four or more mutually unbiased bases, the
zero set is nonempty.

*Proof.* (i) $\operatorname{tr}(vv^*ww^*)=(v^*w)(w^*v)=|\langle v,w\rangle|^2$. (ii) An ideal is
contained in the kernel of evaluation at $x$ if and only if its generators are. (iii) The
coordinate map is a bijection between $\mathbb C^{6\times6}$ and $\mathbb R^{72}$, and the
vanishing of $s$ and $r$ at the coordinates of $U$ says exactly that $U$ is a fourth basis.
(iv) Take $U$ to be the fourth basis of the family. $\square$

Lean: `lean4/ConcreteMubPolynomials.lean::muPolynomial_eval_projector_trace`,
`lean4/ConcreteMubPolynomials.lean::polynomialIdeal_le_eval_kernel_iff`,
`lean4/ConcreteMubPolynomials.lean::polynomialVariety_eq_empty_iff`,
`lean4/ConcreteMubPolynomials.lean::family_triple_variety_nonempty`.

### 4.2 The count of constraints

DAG node: `MUB6-180-RESIDUAL-COUNT`

**Proposition.** The system of §4.1 has $3\cdot6\cdot6=108$ MU residuals and
$2\cdot36=72$ orthonormality residuals, 180 in all, in $2\cdot36=72$ real coordinates.

*Proof.* Count the index sets. $\square$

This is a count of indexed equations only. It says nothing about their independence or the
dimension of the zero set.

Lean: `lean4/ConcreteMubPolynomials.lean::mu_equation_count`,
`lean4/ConcreteMubPolynomials.lean::total_equation_count`,
`lean4/ConcreteMubPolynomials.lean::coordinate_count`.

### 4.3 Evaluation functionals are positive and flat

DAG node: `MUB6-MOMENT-EVALUATION-FLAT`

Fix variables $x_1,\dots,x_n$. The *lower list* consists of $1,x_1,\dots,x_n$; the *upper list*
adds every ordered product $x_kx_l$ (repetitions kept). For a linear functional $\Lambda$ on
$\mathbb R[x]$, $M_2(\Lambda)_{u,v}=\Lambda(uv)$ for $u,v$ in the upper list, and $M_1(\Lambda)$
is the principal submatrix on the lower list.

**Proposition.** For $\chi\in\mathbb R^n$ and $\Lambda_\chi(p)=p(\chi)$: $\Lambda_\chi(1)=1$,
$M_2(\Lambda_\chi)$ is positive semidefinite, and $\operatorname{rank}M_2=\operatorname{rank}M_1$.

*Proof.* $M_2=ww^{\mathsf T}$ with $w_u=u(\chi)$, which is positive semidefinite of rank one
because $w_1=1\ne0$; likewise $M_1$ has rank one. $\square$

Lean: `lean4/CommutativeFlatMoments.lean::evaluation_moment_positive_flat`.

### 4.4 Positive flat moments have a real point

DAG node: `MUB6-COMMUTATIVE-FLAT-REAL-POINT`

**Proposition.** Let $\Lambda$ be a linear functional on $\mathbb R[x_1,\dots,x_n]$ with
$\Lambda(1)=1$, $M_2(\Lambda)\succeq0$ and $\operatorname{rank}M_2=\operatorname{rank}M_1$.
There is $\chi\in\mathbb R^n$ such that every $p$ in the span of the upper list with
$\Lambda(p^2)=0$ satisfies $p(\chi)=0$.

*Proof.* Write $M_2=A^{\mathsf T}A$ and let $a_u$ be the column of $A$ for the upper-list
monomial $u$, so $\langle a_u,a_v\rangle=\Lambda(uv)$. Let $V$ be the span of all $a_u$. The
lower columns span a space of dimension $\operatorname{rank}M_1=\operatorname{rank}M_2=\dim V$,
so they span $V$.

Define $X_k$ on $V$ by $X_ka_m=a_{x_km}$ for $m$ in the lower list. It is well defined: if
$\sum c_ma_m=0$ then for every lower $u$,
$\langle a_u,\sum c_ma_{x_km}\rangle=\sum c_m\Lambda(ux_km)=\langle a_{x_ku},\sum c_ma_m\rangle=0$,
and since $\sum c_ma_{x_km}\in V$ is orthogonal to a spanning set it is zero. The same computation
shows $\langle X_ka_u,a_m\rangle=\Lambda(x_kum)=\langle a_u,X_ka_m\rangle$, so $X_k$ is
symmetric. They commute:
$\langle X_kX_la_u,a_m\rangle=\langle a_{x_lu},a_{x_km}\rangle=\Lambda(x_lux_km)$ is symmetric in
$k,l$, because $\mathbb R[x]$ is commutative.

Commuting symmetric operators on a finite-dimensional real inner-product space have an
orthonormal basis of joint eigenvectors. The vector $\psi=a_1$ has $\|\psi\|^2=\Lambda(1)=1$, so
some joint eigenvector $v$ has $\langle v,\psi\rangle\ne0$; let $X_kv=\chi_kv$. For an upper
monomial $u$, $a_u=u(X)\psi$, so for $p=\sum c_uu$ in the span of the upper list,
$\hat p:=\sum c_ua_u=p(X)\psi$ and $\|\hat p\|^2=\Lambda(p^2)$. If $\Lambda(p^2)=0$ then
$\hat p=0$ and
$0=\langle v,p(X)\psi\rangle=\langle p(X)v,\psi\rangle=p(\chi)\langle v,\psi\rangle$, so
$p(\chi)=0$. $\square$

This is the degree-two case of the flat-extension theorem of Curto and Fialkow, in the form of
Laurent and Mourrain (arXiv:0812.2563), proved here directly for the lists used.

Lean: `lean4/CommutativeFlatMoments.lean::operators_commute`,
`lean4/CommutativeFlatMoments.lean::real_point_of_positive_flat`.

### 4.5 Fourth bases and flat moments

DAG nodes: `MUB6-FOURTH-BASIS-FLAT-MOMENTS`, `MUB6-EMPTY-VARIETY-MOMENT-NONPSD`

**Proposition.** Say $\Lambda$ is *compatible* with $T$ if $\Lambda(u\,r)=0$ for every upper-list
monomial $u$ and every one of the 180 residuals $r$ of §4.1. Then $T$ has a fourth basis if and
only if some $\Lambda$ with $\Lambda(1)=1$, $M_2(\Lambda)\succeq0$ and
$\operatorname{rank}M_2=\operatorname{rank}M_1$ is compatible with $T$. Consequently, if the
fixed-triple variety is empty, every normalized, flat, compatible $\Lambda$ has $M_2(\Lambda)$
not positive semidefinite.

*Proof.* If $U$ is a fourth basis, the evaluation functional at its coordinates is normalized,
positive and flat by §4.3, and $\Lambda(ur)=u(x)r(x)=0$. Conversely, every residual has degree at
most two, so $r=\sum_uc_uu$ lies in the span of the upper list, and
$\Lambda(r^2)=\sum_uc_u\Lambda(ur)=0$. By §4.4 there is a real point at which all 180 residuals
vanish, and by §4.1 it is the coordinate vector of a fourth basis. The second statement is the
contrapositive. $\square$

It does not follow that a nonflat truncation, or a functional that fails compatibility, is
excluded by emptiness of the variety.

Lean: `lean4/ConcreteMubFlatExtension.lean::fourth_basis_of_positive_flat`,
`lean4/ConcreteMubFlatExtension.lean::fourth_basis_iff_positive_flat_moments`,
`lean4/ConcreteMubFlatExtension.lean::moment_nonpositive_of_empty_variety`.

### 4.6 Projectors of a given MUB family

DAG node: `MUB6-CONCRETE-PROJECTORS`

**Proposition.** Let $d\ge1$ and let $\{v_{b,l}\}$ be a family of orthonormal bases of $\mathbb C^d$, indexed by
bases $b$ and $l=1,\dots,d$, pairwise mutually unbiased. Then $P_{b,l}=v_{b,l}v_{b,l}^*$ is
self-adjoint, $\sum_lP_{b,l}=I$, $\operatorname{tr}P_{b,l}=1$, $\operatorname{rank}P_{b,l}=1$, and
$\operatorname{tr}(P_{b,l}P_{c,k})=1/d$ for $b\ne c$.

*Proof.* Self-adjointness is $(vv^*)^*=vv^*$. If $U_b$ has columns $v_{b,l}$ then $U_b^*U_b=I$,
so $U_bU_b^*=I$ as $U_b$ is square, and $U_bU_b^*=\sum_lP_{b,l}$. The trace is $\|v\|^2=1$.
$P_{b,l}v_{b,l}=v_{b,l}\ne0$ and the range lies in $\mathbb Cv_{b,l}$, so the rank is one.
Finally $\operatorname{tr}(P_{b,l}P_{c,k})=|\langle v_{b,l},v_{c,k}\rangle|^2=1/d$. $\square$

Lean: `lean4/ConcreteMubProjectors.lean::concreteProjector_self_adjoint`,
`lean4/ConcreteMubProjectors.lean::concreteProjector_complete`,
`lean4/ConcreteMubProjectors.lean::concreteProjector_trace_one`,
`lean4/ConcreteMubProjectors.lean::concreteProjector_rank_one`,
`lean4/ConcreteMubProjectors.lean::concreteProjector_cross_basis_trace`.

### 4.7 Word moments of a given MUB family are flat

DAG node: `MUB6-CONCRETE-MOMENT-FLATNESS`

**Proposition.** In the setting of §4.6, fix a state $\psi=v_{b_0,l_0}$ and another basis
$b_1\ne b_0$. For a word $w=g_1\cdots g_t$ in the symbols $g=(b,l)$ put $P_w=P_{g_1}\cdots P_{g_t}$
and $L(w)=\langle\psi,P_w\psi\rangle$. For words of length at most one (resp. two) let $M_1$
(resp. $M_2$) be the matrix $L(u^{\mathrm{rev}}v)$. Then $M_1$ and $M_2$ are Gram matrices,
hence positive semidefinite, and $\operatorname{rank}M_2=\operatorname{rank}M_1=d$.

*Proof.* Since each $P_g$ is self-adjoint, $L(u^{\mathrm{rev}}v)=\langle P_u\psi,P_v\psi\rangle$,
so $M_k$ is the Gram matrix of the vectors $P_w\psi$, $|w|\le k$. These lie in $\mathbb C^d$, so
$\operatorname{rank}M_1\le\operatorname{rank}M_2\le d$ ($M_1$ is a principal submatrix of $M_2$).
Among the vectors for $M_1$ are
$P_{(b_1,l)}\psi=\langle v_{b_1,l},\psi\rangle\,v_{b_1,l}$, $l=1,\dots,d$, whose coefficients have
squared modulus $1/d\ne0$; they span $\mathbb C^d$. So $\operatorname{rank}M_1=d$. $\square$

Lean: `lean4/ConcreteMubMoments.lean::complexMomentMatrix_eq_gram`,
`lean4/ConcreteMubMoments.lean::complexMomentMatrix_posSemidef`,
`lean4/ConcreteMubMoments.lean::concrete_mub_moment_flatness`.

### 4.8 Extracting projectors from flat word moments

DAG node: `MUB6-WORD-PROJECTOR-EXTRACTION`

**Proposition.** Let $L$ assign a complex number to every word of length at most four in the
symbols $g=(b,l)$, with $L(\varnothing)=1$, $M_2\succeq0$ and $\operatorname{rank}M_2=\operatorname{rank}M_1$,
and suppose $L(u^{\mathrm{rev}}ggv)=L(u^{\mathrm{rev}}gv)$ for every symbol and all words $u,v$ of
length at most one. Then there are a complex inner-product space $V$ of dimension
$\operatorname{rank}M_1$, a unit vector $\psi\in V$ and self-adjoint idempotents $P_g$ on $V$
with $\langle P_u\psi,P_v\psi\rangle=L(u^{\mathrm{rev}}v)$ for all words $u,v$ of length at most
two. If moreover $L(u^{\mathrm{rev}}g_{b,l}g_{b,k}v)=\delta_{lk}L(u^{\mathrm{rev}}g_{b,l}v)$ and
$\sum_lL(u^{\mathrm{rev}}g_{b,l}v)=L(u^{\mathrm{rev}}v)$, then
$P_{b,l}P_{b,k}=\delta_{lk}P_{b,l}$ and $\sum_lP_{b,l}=I$. The functional with $L(\varnothing)=1$
and $L(w)=0$ for $w\ne\varnothing$ satisfies the first set of hypotheses and fails completeness.

*Proof.* Factor $M_2=A^*A$ and let $a_w$ be the column for the word $w$, so
$\langle a_u,a_v\rangle=L(u^{\mathrm{rev}}v)$. As in §4.4, flatness implies that the columns for
$|w|\le1$ span the column space $V$, of dimension $\operatorname{rank}M_1$. Fix $g$ and let
$W_g\subseteq V$ be the span of $a_{gv}$, $|v|\le1$. The idempotence relation says
$\langle a_{gu},a_{gv}-a_v\rangle=0$, so $a_{gv}\in W_g$ and $a_v-a_{gv}\perp W_g$: $a_{gv}$ is
the orthogonal projection of $a_v$ onto $W_g$. Let $P_g$ be that orthogonal projection; it is a
self-adjoint idempotent with $P_ga_v=a_{gv}$ for $|v|\le1$. Put $\psi=a_\varnothing$, so
$\|\psi\|^2=L(\varnothing)=1$, $P_g\psi=a_g$ and $P_{g}P_{h}\psi=a_{gh}$; hence
$\langle P_u\psi,P_v\psi\rangle=\langle a_u,a_v\rangle$.

Under the same-basis relation with $l\ne k$, $\langle a_{g_{b,l}u},a_{g_{b,k}v}\rangle=0$, so
$W_{b,l}\perp W_{b,k}$ and $P_{b,l}P_{b,k}=0$ (the case $l=k$ is idempotence). Under completeness,
$\langle a_u,\sum_la_{g_{b,l}v}-a_v\rangle=0$ for all $|u|\le1$; the vector lies in $V$, so it is
zero, i.e. $\sum_lP_{b,l}$ fixes a spanning set and equals $I$. For the last statement,
completeness at $u=v=\varnothing$ would read $0=\sum_lL(g_{b,l})=L(\varnothing)=1$. $\square$

The extracted space need not have dimension six, and the ranges need not be one-dimensional or
mutually unbiased; those require further relations.

Lean: `lean4/FlatMomentProjectorExtraction.lean::extract_word_projectors`,
`lean4/FlatMomentBasisRelations.lean::extract_word_basis`,
`lean4/FlatMomentBasisRelations.lean::zero_action_moments_reject_completeness`.

### 4.9 The legacy projector interface has a trivial model

DAG node: `MUB6-INTERFACE-COUNTERMODEL`

**Proposition.** The structure `PhysicalProjectorRealization` (an inner-product function, a
designated normalized state, idempotent self-adjoint actions of the generators, and
orthogonality of distinct outcomes within a basis) has a model for every number of bases and
every dimension label. Hence the statement that it has no model is false for all sizes.

*Proof.* Take the carrier $\{\mathrm{true},\mathrm{false}\}$, inner product $1$ on
$(\mathrm{true},\mathrm{true})$ and $0$ otherwise, state $\mathrm{true}$, and every action and
every linear combination constantly $\mathrm{false}$. The state has inner product $1$ with
itself. Every action is idempotent and self-adjoint, and products of distinct outcomes are
zero, because all actions return the zero vector $\mathrm{false}$, whose inner product with
anything is $0$. $\square$

The structure does not require completeness, rank one, dimension six or unbiasedness, so an
exclusion stated over it cannot be the intended theorem. §4.8 shows that completeness alone
already rules out this model.

Lean: `lean4/MomentPositivityObligation.lean::zeroActionInterfaceModel`,
`lean4/MomentPositivityObligation.lean::not_universal_interface_exclusion`.

---

## 5. Abstract gluing and label arithmetic

### 5.1 Fourth bases inside a seven-basis family

DAG node: `MUB6-GLUING-G3-OPAQUE`

**Proposition.** Let a type of "bases" carry any symmetric relation "MU". If $B_0,\dots,B_6$ are
pairwise MU, then every triple $B_i,B_j,B_k$ of distinct members has a fourth member MU to all
three. If no MU triple has a fourth MU basis, no four pairwise MU bases exist.

*Proof.* Seven indices leave at least four outside any three; pick one. For the second
statement, four pairwise MU bases contain an MU triple with a fourth. $\square$

The relation is opaque in this statement: nothing about coordinates or unitary matrices is
used, and applying the result to Hilbert-space bases needs a separate interpretation.

Lean: `lean4/Gluing.lean::g3_theorem`,
`lean4/Gluing.lean::no_four_mub6_of_no_triple_extension`.

### 5.2 Route C label arithmetic

DAG node: `MUB6-ROUTE-C-LABEL-ARITHMETIC`

**Proposition.** If natural numbers satisfy $6=n_D+n_T+n_S+n_H$, $n_T+n_S\le1$ and $n_H\le0$,
then $n_D\ge5$, $\binom{n_D}2\ge10$ and $n_D+\binom{n_D}2\ge15$.

*Proof.* $n_H=0$, so $n_D=6-(n_T+n_S)\ge5$; $\binom n2$ is increasing in $n$ and $\binom52=10$;
add. $\square$

The numbers are labels in a configuration record. No map from them to transition matrices in the
Fourier family is part of the statement.

Lean: `lean4/RouteCFourierLandingBypass.lean::fourier_count_ge_five`,
`lean4/RouteCFourierLandingBypass.lean::fourier_pairs_ge_ten`,
`lean4/RouteCFourierLandingBypass.lean::fourier_landing_edges_lower_bound`.

### 5.3 Balanced Laurent sums of the Tao matrix

DAG node: `MUB6-TAO-LAURENT-NORM-NINE`

**Proposition.** Let $S$ be the Tao matrix of §2.3. There are $\binom63=20$ sign vectors
$g\in\{\pm1\}^6$ with three entries $+1$, and for each of them

$$
\Bigl|\sum_{j=0}^5\prod_{r=0}^5S_{rj}^{\,g_r}\Bigr|^2=9.
$$

*Proof.* The product is $\omega^{t_j}$ with $t_j=\sum_rg_re_{rj}\bmod3$. Every column of the
exponent table $e$ sums to $0\bmod3$ (column $0$ is zero and each other column contains each
residue twice), and $g_r\equiv2\cdot[r\in P]-1\pmod 3$ where $P$ is the set of positive entries,
so $t\equiv-\sum_{r\in P}e_r$. Replacing $P$ by its complement replaces $t$ by $-t$ and leaves
$|\sum_j\omega^{t_j}|$ unchanged, so it is enough to take the ten sets $P$ containing $0$:

| $P$ | $t$ | | $P$ | $t$ |
|---|---|---|---|---|
| 012 | 0 2 2 0 2 0 | | 024 | 0 0 1 0 1 1 |
| 013 | 0 2 0 2 0 2 | | 025 | 0 0 2 2 0 2 |
| 014 | 0 1 0 1 1 0 | | 034 | 0 0 2 2 2 0 |
| 015 | 0 1 1 0 0 1 | | 035 | 0 0 0 1 1 1 |
| 023 | 0 1 1 1 0 0 | | 045 | 0 2 0 0 2 2 |

In every row two residues occur three times each and the third not at all. So the sum is
$3(\omega^a+\omega^b)=-3\omega^c$ with $\{a,b,c\}=\{0,1,2\}$, of squared modulus $9$. $\square$

Lean checks the 20 cases by evaluation over the Eisenstein integers and transfers the result to
$\mathbb C$ with $\omega=-\frac12+\frac{\sqrt3}2i$.

Lean: `lean4/Conjecture2GeneralMechanization.lean::balanced_mask_count`,
`lean4/Conjecture2GeneralMechanization.lean::tao_all_balanced_masks`,
`lean4/MubTaoLaurent.lean::tao_all_balanced_laurent`.
