<div align="center">

# Finite Quantum Mechanics: Proofs of the Core Results

**Author:** Jeremy H. Carroll

**Date:** 2026-10-26

**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)

</div>

## Introduction

This note gives written proofs of the results of [Finite Quantum Mechanics](finite_quantum_mechanics.md)
that the derivation DAG (`dag/derivation_dag.json`) records as proved in Lean. Each section states
one result, proves it, and names the Lean declarations that check it. The DAG identifier of the
result is given on the line beginning *DAG node*.

Where a Lean declaration checks a special case (a fixed dimension, a fixed matrix, integer
entries), the proof below is written for the general statement when a general argument exists,
and the closing remark says what the Lean declaration covers. A proof here does not replace the
Lean check, and the Lean check does not replace the proof: the first is about the mathematics,
the second about a particular encoding of it.

**Notation.** $Q$ is a finite report set with $|Q|=n$. $\mathbb Z[i]$ is the ring of Gaussian
integers. A report vector is a function $v\colon Q\to\mathbb Z[i]$ and its phase-blind weight is
$w_v(q)=\overline{v(q)}\,v(q)=|v(q)|^2\in\mathbb Z_{\ge 0}$. Matrices act on the left;
$A^\dagger$ is the conjugate transpose. All Lean paths are relative to the repository root.

---

## 1. Report quotients and phase

### 1.1 The quotient of a primitive difference

DAG node: `FQ-PRIMDIFF-QUOTIENT-KERNEL`

**Proposition.** Let $\delta\colon A\times A\to B$ be a map and $Z\subseteq B$ a predicate such that
$Z(\delta(x,x))$; $Z(\delta(x,y))\Rightarrow Z(\delta(y,x))$; and
$Z(\delta(x,y))\wedge Z(\delta(y,z))\Rightarrow Z(\delta(x,z))$. Then $x\sim y :\Leftrightarrow
Z(\delta(x,y))$ is an equivalence relation, and the quotient $A/{\sim}$ exists. For a finite
presented carrier $\pi\colon X\to Q$ with $\delta_\pi(x,y)=(\pi x,\pi y)$ and $Z$ the diagonal,
$x\sim y$ if and only if $\pi x=\pi y$.

*Proof.* The three hypotheses are reflexivity, symmetry and transitivity of $\sim$ word for word,
so $\sim$ is an equivalence relation and $A/{\sim}$ is its set of classes. For the presented
carrier, $Z(\delta_\pi(x,y))$ says $(\pi x,\pi y)$ lies on the diagonal of $Q\times Q$, that is
$\pi x=\pi y$. Two distinct points with distinct reports, such as $(0,0)$ and $(1,0)$ under the
first-coordinate projection $\{0,1\}^2\to\{0,1\}$, are therefore not identified. $\square$

The content is the quotient construction only: $Z$ and $\pi$ are inputs, and no field, norm or
inner product is produced.

Lean: `lean4/PrimitiveDifference.lean::zeroRel_equivalence`,
`lean4/H000FinitePresentedCarrier.lean::sameReport_iff`,
`lean4/H000FinitePresentedCarrier.lean::presented_carrier_separates`.

### 1.2 The phase-blind fibre

DAG node: `FQ-PHASE-FIBER-QUOTIENT`

**Proposition.** For report vectors $u,v\colon Q\to\mathbb Z[i]$ put $u\sim v$ when $w_u=w_v$.
Then (i) $w_v(q)$ is a nonnegative integer; (ii) $u\sim v$ is the zero relation of the primitive
difference $\delta(u,v)=(w_u,w_v)$ with $Z$ the diagonal; (iii) $\zeta v\sim v$ for every unit
$\zeta\in\{\pm1,\pm i\}$; (iv) the fibre of $w$ is not a single orbit of global phases: on
$Q=\{0,1\}$ the vectors $\psi_1=(1,1)$ and $\psi_2=(1,-1)$ satisfy $\psi_1\sim\psi_2$ and
$\psi_2\neq\zeta\psi_1$ for every $\zeta\in\mathbb Z[i]$.

*Proof.* (i) For $z=a+bi$, $\bar z z=a^2+b^2\in\mathbb Z_{\ge0}$. (ii) is the definition of the
diagonal predicate, and §1.1 applies. (iii) $|\zeta z|^2=|\zeta|^2|z|^2=|z|^2$ because
$|\zeta|=1$. (iv) $w_{\psi_1}=w_{\psi_2}=(1,1)$. If $\psi_2=\zeta\psi_1$ then the first coordinate
gives $\zeta=1$ and the second gives $\zeta=-1$. $\square$

So the phase-blind fibre contains relative phases, not only global ones. Enumerating a fibre needs
a declared finite unit group; describing the fibre as an orbit of a group action on several
reports is not part of this result.

Lean: `lean4/H009PhaseFiber.lean::phasePD_zeroRel_iff`,
`lean4/H009PhaseFiber.lean::relative_phase_in_fiber`,
`lean4/H008PhaseBlindPresentation.lean::weight_nonneg`.

### 1.3 Interference does not descend to the phase-blind quotient

DAG node: `FQ-INTERFERENCE-NONDESCENT`

**Proposition.** Let $H(v)=(v_0+v_1,\;v_0-v_1)$ on $Q=\{0,1\}$ and let the readout be
$r(v)=w_{H(v)}$. There is no function $f$ with $r=f\circ w$.

*Proof.* With $\psi_1,\psi_2$ as in §1.2, $w_{\psi_1}=w_{\psi_2}$ but $H\psi_1=(2,0)$ and
$H\psi_2=(0,2)$, so $r(\psi_1)=(4,0)\neq(0,4)=r(\psi_2)$. A function of $w$ takes equal values on
$\psi_1$ and $\psi_2$. $\square$

Relative phase is thus invisible to $w$ and visible after a non-diagonal operation. The second
context $H$ is supplied, not derived.

Lean: `lean4/H010InterferenceNonDescent.lean::no_descent_through_fiber`,
`lean4/H010InterferenceNonDescent.lean::mix_separates`.

### 1.4 Which linear maps descend to populations

DAG node: `FQ-PHASE-BLIND-DESCENT-ZERO-RETAINED`

**Theorem.** Let $M$ be an $n\times n$ integer matrix. The following are equivalent:

1. for all integer vectors $u,v$, $u_j^2=v_j^2$ for every $j$ implies $(Mu)_i^2=(Mv)_i^2$ for
   every $i$ (the map $M$ descends to the population quotient);
2. every row of $M$ has at most one nonzero entry.

*Proof.* (2 ⇒ 1) If row $i$ is zero, $(Mu)_i=(Mv)_i=0$. If its only nonzero entry is $m_{ij}$,
then $(Mu)_i^2=m_{ij}^2u_j^2=m_{ij}^2v_j^2=(Mv)_i^2$.

(1 ⇒ 2) Suppose row $i$ has nonzero entries $m_{ij},m_{ik}$ with $j\neq k$. Take $u=e_j+e_k$ and
$v=e_j-e_k$; they have equal squared coordinates. Then
$$(Mu)_i^2-(Mv)_i^2=(m_{ij}+m_{ik})^2-(m_{ij}-m_{ik})^2=4\,m_{ij}m_{ik}\neq0,$$
contradicting (1). $\square$

The value $0$ has to be kept in the population quotient: a row with two nonzero entries can send
a vector with nonzero populations to population $0$, as $1\cdot1+1\cdot(-1)=0$ shows. The theorem
concerns integer populations; a normalized or projective version needs its own carrier and is not
claimed here.

Lean: `lean4/BornRedundancy.lean::descent_compatible_iff_row_sparse` proves the theorem for
$n=2$. `lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_phase_blind_descent_general_n_row_sparsity`
checks the two identities used above for arbitrary integers: the cross term $4ab$ and the
row-sparse direction $(au)^2=(av)^2$ when $u^2=v^2$.

### 1.5 Normalization is redundant after the ray quotient

DAG node: `FQ-BORN-NORMALIZATION-REDUNDANCY`

**Proposition.** For a finite list $w$ of rationals with $s(w)=\sum_k w_k\neq0$, let
$N(w)=w/s(w)$. Then $N(N(w))=N(w)$. If $s(w_1)>0$ and $s(w_2)>0$, then $N(w_1)=N(w_2)$ if and only
if $w_2=c\,w_1$ for some rational $c>0$.

*Proof.* $s(N(w))=s(w)/s(w)=1$, so $N(N(w))=N(w)/1$. If $w_2=cw_1$ with $c>0$ then
$s(w_2)=cs(w_1)$ and $N(w_2)=cw_1/(cs(w_1))=N(w_1)$. Conversely, if $N(w_1)=N(w_2)$ then
$w_2=s(w_2)N(w_2)=s(w_2)N(w_1)=\frac{s(w_2)}{s(w_1)}\,w_1$ and $c=s(w_2)/s(w_1)>0$. $\square$

So normalizing and then passing to positive rays gives the same classes as passing to rays
directly: a normalized weight vector is a canonical representative of its ray, nothing more.

Lean: `lean4/BornRedundancy.lean::normalize_idempotent`,
`lean4/BornRedundancy.lean::ray_quotient_classification`.

### 1.6 Linear maps on Gaussian report vectors are Gaussian matrices

DAG node: `GP-FIN-GAUSS-MATRIX-ALGEBRA`

**Proposition.** Let $V=\mathbb Z[i]^Q$ with the sesquilinear pairing
$\langle u,v\rangle=\sum_q\overline{u(q)}\,v(q)$. Every additive map $T\colon V\to V$ commuting
with multiplication by $\mathbb Z[i]$ is $v\mapsto Av$ for a unique matrix
$A\in M_n(\mathbb Z[i])$, namely $A_{ij}=T(e_j)_i$. Matrix product corresponds to composition, and
$\langle Au,v\rangle=\langle u,A^\dagger v\rangle$.

*Proof.* Every $v$ is $\sum_j v(j)e_j$, a finite sum, so linearity gives
$T(v)_i=\sum_j v(j)T(e_j)_i=(Av)_i$. If $B$ also represents $T$, then $B_{ij}=(Be_j)_i=T(e_j)_i=A_{ij}$.
$(AB)v=A(Bv)$ is associativity of finite sums. Finally
$\langle Au,v\rangle=\sum_{i,j}\overline{A_{ij}u_j}\,v_i=\sum_j\overline{u_j}\sum_i\overline{A_{ij}}v_i
=\langle u,A^\dagger v\rangle$. $\square$

This is $M_n(\mathbb Z[i])$, not $M_n(\mathbb C)$: there are no inverses of non-units and, as §7
shows, Hermitian matrices need not have eigenvalues in $\mathbb Z[i]$.

Lean: `lean4/H017Fin.lean::finite_gauss_matrix_algebra`.

---

## 2. Readout rules

### 2.1 The Sorkin term of a polynomial readout

DAG node: `FQ-SORKIN-READOUT-CLASS-QM208`

For a readout $R$ of real amplitudes put
$$I_3(R;a,b,c)=R(a+b+c)-R(a+b)-R(a+c)-R(b+c)+R(a)+R(b)+R(c)-R(0).$$

**Theorem.** (i) For $R(t)=\alpha t^2+\beta t^4$,
$I_3(R;a,b,c)=12\,\beta\,abc\,(a+b+c)$; hence $I_3$ vanishes identically if and only if
$\beta=0$. (ii) Write the Born weight of $x\in\mathbb Q(\zeta_{12})$ as
$x\bar x=N_0(x)+N_1(x)\sqrt3$ with $N_0,N_1\in\mathbb Q$, and let
$R_{A,B}(x)=A\,N_0(x)+B\,N_1(x)$. Then $R_{A,B}$ is invariant under the conjugation
$\sqrt3\mapsto-\sqrt3$ of the Born weight if and only if $B=0$.

*Proof.* (i) $I_3$ is linear in $R$, and for a polynomial $R$ the alternating sum over the subsets
of $\{a,b,c\}$ kills every monomial of $R(a+b+c)$ that omits one of the variables. For $t^2$ no
monomial of degree 2 contains all three variables, so $I_3(t^2)=0$. The monomials of $(a+b+c)^4$
containing all three variables are $a^2bc$, $ab^2c$, $abc^2$, each with multinomial coefficient
$4!/(2!\,1!\,1!)=12$. Hence $I_3(t^4)=12abc(a+b+c)$ and $I_3(R)=12\beta abc(a+b+c)$. Taking
$a=b=c=1$ gives $36\beta$, so vanishing forces $\beta=0$.

(ii) $\sqrt3=\zeta_{12}+\zeta_{12}^{-1}$ generates the real subfield $\mathbb Q(\sqrt3)$ of
$\mathbb Q(\zeta_{12})$, and $x\bar x$ is real, so $N_0,N_1$ are defined. Conjugation replaces
$(N_0,N_1)$ by $(N_0,-N_1)$, which changes $R_{A,B}$ by $-2BN_1$. The element
$v_+=2+2\zeta_{12}-\zeta_{12}^3$ has $v_+\bar v_+=7+4\sqrt3=(2+\sqrt3)^2$, and its conjugate
weight $7-4\sqrt3$ is the weight of $v_-=2-2\zeta_{12}+\zeta_{12}^3$. Then
$R_{A,B}(v_+)-R_{A,B}(v_-)=8B$, which vanishes only for $B=0$. Conversely $B=0$ gives a readout of
$N_0$ alone, which conjugation fixes. $\square$

This is not a classification of all readouts or of the positive cone of rational readouts.

Lean: `lean4/FiniteQM.lean::qzeta12_rational_readout_cone_and_galois_selection` checks (ii) and
the values $R_{1,1}(v_\pm)=11,3$. `lean4/FiniteQM.lean::born_trace_vs_quartic_readout_and_three_ray_positivity_gap`
checks that the quartic rule disagrees with the quadratic one on the context $(3/5,4/5)$ and that a
trace-one symmetric matrix with negative determinant gives a negative weight. Part (i) is checked
in Lean at $a=b=c=1$ (`lean4/FiniteQM.lean::sym_deg4_sorkin_i3_at_unit_triple`); the general
identity is the argument above.

### 2.2 The power rule on a Pythagorean context selects $p=2$

DAG node: `FQ-POWER-RULE-P2-SELECTION`

**Proposition.** For real $p$, $(3/5)^p+(4/5)^p=1$ if and only if $p=2$.

*Proof.* $f(p)=(3/5)^p+(4/5)^p$ is a sum of two strictly decreasing functions of $p$, since both
bases lie in $(0,1)$. So $f$ is injective, and $f(2)=9/25+16/25=1$. $\square$

The orthonormal context $\{(3/5,4/5),(-4/5,3/5)\}$ is real and rational, so a power rule
$|c|^p$ that is to give a probability distribution on it must have $p=2$. The power family and the
context are supplied; this is not a uniqueness theorem for readouts in general.

Lean: `lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_power_p2_cabello_146_and_weyl_commutant_irreducibility`
checks $3^p+4^p=5^p$ for $p=2$ and its failure for $p=1,3,4,5,6$.
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.power_rule_p2_unique_even_exponent`
checks the analogous selection $1^{2k}+1^{2k}=2^k\iff k=1$ on the context $(1,1)/\sqrt2$. The
statement for real $p$ is the monotonicity argument above; Lean does not check it.

### 2.3 Gleason fails on the rational plane

DAG node: `FQ-GLEASON-D2-RATIONAL-PLANE-OBSTRUCTION`

**Proposition.** On nonzero $(x,y)\in\mathbb Q^2$ let
$$f(x,y)=\begin{cases}1 & xy>0 \text{ or } y=0,\\ 0 & xy<0 \text{ or } x=0.\end{cases}$$
Then $f$ takes values in $\{0,1\}$, is invariant under nonzero scaling, and sums to $1$ on every
orthogonal pair $\{(x,y),(-y,x)\}$. There are no rationals $a,b,c$ with
$ax^2+2bxy+cy^2=f(x,y)\,(x^2+y^2)$ for all nonzero $(x,y)$.

*Proof.* Scaling by $\lambda\neq0$ multiplies $xy$ by $\lambda^2>0$ and preserves which coordinate
vanishes. On an orthogonal pair with $xy\neq0$ the products $xy$ and $-yx$ have opposite signs, so
exactly one vector gets value 1; if $xy=0$ the pair is $\{$horizontal, vertical$\}$, with values
$1$ and $0$. Suppose $a,b,c$ exist. At $(1,0)$: $a=1$. At $(0,1)$: $c=0$. At $(1,1)$:
$1+2b=2$, so $b=1/2$. At $(1,2)$ the left side is $1+2\cdot\frac12\cdot2=3$ and the right side is
$1\cdot5=5$. $\square$

Gleason's theorem needs dimension at least 3; in dimension 2 frame functions are unconstrained
beyond the pair condition, and this one is not quadratic. The statement says nothing for
$d\ge3$.

Lean: `lean4/GleasonRationalPlane.lean::no_quadratic_representation`,
`lean4/GleasonRationalPlane.lean::binary_values`,
`lean4/GleasonTheorem.lean::d2_binary_non_bornian_obstruction`.

### 2.4 No integer frame function on the Cabello rays

DAG node: `FQ-CABELLO-NO-INTEGER-FRAME`

Let $v_0,\dots,v_{17}\in\mathbb Z^4$ be the 18 Cabello rays and $C_1,\dots,C_9$ the nine
orthogonal tetrads (listed in `lean4/H054GleasonCyclotomicObstruction.lean`). Each ray lies in
exactly two tetrads.

**Proposition.** (i) There is no $f\colon\{v_0,\dots,v_{17}\}\to\mathbb Z$ with
$\sum_{v\in C_k}f(v)=1$ for all nine tetrads. (ii) There is a symmetric integer matrix $M$ whose
quadratic form is nonnegative and bounded by $2\|v\|^2$ on all 18 rays and whose normalized
values $4\,v^{\mathsf T}Mv/\|v\|^2$ sum to 8 on every tetrad, while $M$ is not positive
semidefinite.

*Proof.* (i) Summing the nine equations counts every ray twice, so $2\sum_v f(v)=9$, which has no
integer solution. (ii) Index coordinates by $0,\dots,3$ and take $M$ symmetric with $m_{11}=2$, $m_{12}=1$,
$m_{13}=-1$, $m_{23}=-1$ and all other entries on or above the diagonal zero. For $w=(0,0,1,1)$,
$w^{\mathsf T}Mw=2m_{23}=-2<0$. The nonnegativity, the bound and the tetrad sums are a finite
evaluation on the 18 listed rays. $\square$

Part (i) does not need $f$ to take values in $\{0,1\}$; any integer-valued assignment fails.
Part (ii) shows that frame additivity with nonnegativity on a finite set of rays does not force a
positive semidefinite representative. The scope is this real system, not complex Hermitian
matrices in general.

Lean: `lean4/H054GleasonCyclotomicObstruction.lean::cabello_no_integer_frame_assignment`,
`lean4/H054GleasonCyclotomicObstruction.lean::frame_additivity_not_force_psd`,
`lean4/H053EverettForkingTree.lean::cabello_parity_obstruction`.

### 2.5 The trace norm on trace-zero differences

DAG node: `FQ-TRACE-NORM-FROM-CPTP-MONOTONICITY`

**Theorem.** (i) Let $d\ge1$ and let $L$ be Hermitian on $\mathbb C^d$ with extreme eigenvalues
$\lambda_{\max},\lambda_{\min}$. Then
$$\sup\{\operatorname{tr}(LX): X=X^\dagger,\ \operatorname{tr}X=0,\ \|X\|_1\le2\}
=\lambda_{\max}-\lambda_{\min}=2\min_{c\in\mathbb R}\|L-c\,I\|_\infty .$$
(ii) For the trace-zero Hermitian $X=\begin{pmatrix}a&b\\\bar b&-a\end{pmatrix}$ and the diagonal
pinching $\Delta(X)=\operatorname{diag}(a,-a)$, $\|\Delta X\|_1\le\|X\|_1$ with equality if and
only if $b=0$.

*Proof.* (i) Write $X=P-N$ with $P,N\ge0$ of orthogonal supports. Then
$\operatorname{tr}P=\operatorname{tr}N=t$ and $\|X\|_1=2t\le2$, so
$\operatorname{tr}(LX)\le\lambda_{\max}t-\lambda_{\min}t\le\lambda_{\max}-\lambda_{\min}$. The
value is attained by $X=|e_{\max}\rangle\langle e_{\max}|-|e_{\min}\rangle\langle e_{\min}|$. For
the second equality, $\|L-cI\|_\infty=\max(\lambda_{\max}-c,\;c-\lambda_{\min})\ge
\frac12(\lambda_{\max}-\lambda_{\min})$, with equality at $c=\frac12(\lambda_{\max}+\lambda_{\min})$.

(ii) $X$ has eigenvalues $\pm\sqrt{a^2+|b|^2}$, so $\|X\|_1^2=4(a^2+|b|^2)\ge4a^2=\|\Delta X\|_1^2$,
with equality exactly when $b=0$. $\square$

Part (i) is the duality between the trace norm on trace-zero matrices and the operator norm
modulo scalars. Part (ii) is one CPTP map contracting the trace norm. That the trace norm is the
only norm family contracted by every CPTP map, in every dimension, is not claimed here.

Lean: `lean4/TraceZeroDuality.lean::trace_zero_duality_gap_zero` checks (i) for diagonal $2\times2$
integer $L$, with the factor 2 absorbed into the scaling.
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.trace_zero_pinching_contraction`
checks (ii) for real integer $a,b$ in the squared form $a^2\le a^2+b^2$.

---

## 3. Correlations and contextuality

### 3.1 A common joint law bounds CHSH by 2

DAG node: `FQ-BELL-CLASSICAL-JOINT-EXTENSION`

**Proposition.** Let $A_0,A_1,B_0,B_1$ be $\pm1$-valued random variables on one probability space
and $S=A_0B_0+A_0B_1-A_1B_0+A_1B_1$. Then every outcome of $S$ is $\pm2$ and
$|\mathbb E S|\le2$.

*Proof.* $S=A_0(B_0+B_1)+A_1(B_1-B_0)$. Since $B_0,B_1\in\{\pm1\}$, one of $B_0+B_1$,
$B_1-B_0$ is $0$ and the other is $\pm2$, so $S=\pm2$ pointwise. Expectation is a convex
combination, hence $|\mathbb ES|\le2$. $\square$

The same bound holds for any finite mixture with natural-number weights $w_k$ and values
$s_k\in[-2,2]$: $|\sum_kw_ks_k|\le2\sum_kw_k$. The converse (a common joint law exists whenever all
CHSH inequalities hold, Fine's theorem) is not proved here over the rationals. A physical
conclusion needs locality and setting independence in addition.

Lean: `lean4/QuantumCorrelation.lean::classical_chsh_bound`,
`lean4/H053EverettForkingTree.lean::chsh_classical_bound`,
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_bell_classical_joint_extension_convex_bound`.

### 3.2 A rational quantum model with $S=14/5$

DAG node: `FQ-BELL-RATIONAL-VIOLATION-14-5`

**Proposition.** Take the real maximally entangled two-qubit state and observables
$\sigma(u)=u_1Z+u_2X$ for unit $u\in\mathbb R^2$, so that $E(a,b)=a\cdot b$. With
$a_1=(1,0)$, $a_2=(0,1)$, $b_1=(4/5,3/5)$, $b_2=(3/5,-4/5)$,
$$S=E(a_1,b_1)+E(a_1,b_2)+E(a_2,b_1)-E(a_2,b_2)=\tfrac{14}{5}>2 .$$
Consequently the four correlations have no common joint law.

*Proof.* For $|\Phi^+\rangle=(|00\rangle+|11\rangle)/\sqrt2$ and real symmetric $A,B$,
$\langle\Phi^+|A\otimes B|\Phi^+\rangle=\frac12\operatorname{tr}(A^{\mathsf T}B)=\frac12\operatorname{tr}(AB)$,
and $\frac12\operatorname{tr}(\sigma(a)\sigma(b))=a\cdot b$. The four dot products are
$\frac45,\frac35,\frac35,-\frac45$, so $S=\frac{14}{5}$. By §3.1 a common joint law would give
$|S|\le2$. $\square$

All entries are rational; $14/5<2\sqrt2$, so this is not the Tsirelson value. The state, the
tensor product and the Born pairing are supplied.

Lean: `lean4/QuantumCorrelation.lean::q1_violates_classical_bound` checks the scaled value
$70>50$ for the vectors scaled by 5. `lean4/H053EverettForkingTree.lean::chsh_pythagorean_quantum_value`
checks the same value for a second presentation.
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_bell_rational_violation_14_5_no_joint_law`
checks that no natural-weighted list of deterministic values with total weight 25 sums to 70.

### 3.3 Tsirelson's bound and its attainment over $\mathbb Q(\sqrt2)$

DAG node: `FQ-TSIRELSON-SOS-Q-SQRT2`

**Theorem.** (i) Let $A_0,A_1,B_0,B_1$ be Hermitian with $A_x^2=B_y^2=I$ and $[A_x,B_y]=0$, and
$\mathcal B=A_0B_0+A_0B_1+A_1B_0-A_1B_1$. Then
$$2\sqrt2\,I-\mathcal B=\tfrac{1}{\sqrt2}\Big[\big(A_0-\tfrac{B_0+B_1}{\sqrt2}\big)^2+\big(A_1-\tfrac{B_0-B_1}{\sqrt2}\big)^2\Big]\ \ge0,$$
so $\langle\mathcal B\rangle\le2\sqrt2$ in every state. (ii) The value $2\sqrt2$ is attained by the
model of §3.2 with $a_1=(1,0)$, $a_2=(0,1)$, $b_{1,2}=(1,\pm1)/\sqrt2$, all of whose entries lie
in $\mathbb Q(\sqrt2)$.

*Proof.* (i) Expand, using $A_x^2=I$, $B_y^2=I$ and commutation:
$(A_0-\frac{B_0+B_1}{\sqrt2})^2=I-\sqrt2A_0(B_0+B_1)+\frac12(B_0+B_1)^2$ and
$(A_1-\frac{B_0-B_1}{\sqrt2})^2=I-\sqrt2A_1(B_0-B_1)+\frac12(B_0-B_1)^2$. The two $B$ terms add to
$\frac12(2B_0^2+2B_1^2)=2I$. The sum is $4I-\sqrt2\,\mathcal B$, and dividing by $\sqrt2$ gives the
identity. A sum of squares of Hermitian operators is positive semidefinite.

(ii) $a_1\cdot b_1=a_1\cdot b_2=a_2\cdot b_1=\frac1{\sqrt2}$ and $a_2\cdot b_2=-\frac1{\sqrt2}$, so
$S=4/\sqrt2=2\sqrt2$. $\square$

The vectors scaled to squared norm 4, namely $(2,0)$, $(0,2)$, $(\sqrt2,\pm\sqrt2)$, have
$\mathbb Z[\sqrt2]$ entries and scaled value $8\sqrt2$. Since $\sqrt2=\zeta_8+\zeta_8^{-1}$ lies in
$\mathbb Q(\zeta_8)\subset\mathbb Q(\zeta_{24})$, the construction lives in the conductor-24 field.
Observables beyond the four supplied ones, the tensor structure and the Born pairing are not
derived.

Lean: `lean4/QuantumCorrelation.lean::q2_tsirelson_attainment` checks (ii) in
$\mathbb Z[\sqrt2]$ (the scaled sum is $0+8\sqrt2$).
`lean4/H064ContextualityThresholds.lean::conductor_24_contains_sqrt2` records that the conductor of
$\mathbb Q(\sqrt2)$ divides 24. The operator identity (i) is the computation above; the DAG
records the explicit $\mathbb Q(\sqrt2)$ matrix certificates as checked by exact computation.

### 3.4 Contextuality as a degree-one obstruction over $\mathbb F_2$

DAG node: `FQ-CONTEXTUALITY-CECH-F2`

Let $\mathcal C=\{C_1,\dots,C_m\}$ be a cover of a set of observables by contexts. A 0-cochain
assigns to each context a value in $\mathbb F_2$ (per observable), and
$(d^0s)_{ij}=s_j-s_i$, $(d^1w)_{ijk}=w_{jk}-w_{ik}+w_{ij}$.

**Proposition.** (i) $d^1d^0=0$. (ii) The Cabello system (§2.4) has no global section: there is no
$g\colon\{v_0,\dots,v_{17}\}\to\mathbb F_2$ whose sum over every tetrad is $1$. (iii) In the
Mermin–Peres square there is no assignment of $\pm1$ to the nine entries with row products
$+1,+1,+1$ and column products $+1,+1,-1$.

*Proof.* (i) $(d^1d^0s)_{ijk}=(s_k-s_j)-(s_k-s_i)+(s_j-s_i)=0$. (ii) Summing the nine tetrad
equations in $\mathbb F_2$ gives $2\sum_vg(v)=9$, i.e. $0=1$. (iii) The product of all row
products and the product of all column products are both the product of the nine entries, but
they are $+1$ and $-1$. $\square$

In (ii) and (iii) the local constraints are satisfiable context by context and fail globally; the
parity class is the obstruction. Rank computations of the incidence matrices, and any equivalence
with sheaf cohomology in general, are separate statements.

Lean: `lean4/ContextualityObstruction.lean::differential_squares_to_zero`,
`lean4/ContextualityObstruction.lean::x1_has_no_global_section`,
`lean4/DualWitness.lean::mermin_peres_parity_obstruction`.

---

## 4. Dynamics

### 4.1 No finite-dimensional canonical commutation relation

DAG node: `FQ-COMMUTATOR-TRACE-OBSTRUCTION`

**Proposition.** Let $K$ be a field of characteristic 0 and $n\ge1$. If $A,B\in M_n(K)$ and
$AB-BA=\lambda I$, then $\lambda=0$. In particular $[X,P]=i\hbar I$ has no solution in
$M_n(\mathbb C)$ when $\hbar\ne0$.

*Proof.* $\operatorname{tr}(AB)=\sum_{i,j}A_{ij}B_{ji}=\operatorname{tr}(BA)$, so
$\operatorname{tr}(AB-BA)=0$, while $\operatorname{tr}(\lambda I)=n\lambda$. Since $n\neq0$ in $K$,
$\lambda=0$. $\square$

The same argument works over any commutative ring in which $n$ is not a zero divisor. In
characteristic $p$ with $p\mid n$ the relation can hold: on $\mathbb F_p[x]/(x^p)$, of dimension
$p$, differentiation $D$ and multiplication by $x$ satisfy $[D,x]=I$. That is why the hypothesis on
$K$ is needed.

Lean: `lean4/H056ContinuumLiftBoundary.lean::wintner_wielandt_dim2_obstruction` proves the
proposition for $2\times2$ integer matrices; `lean4/H068WeylCcrResidual.lean::tr_comm2_vanishes` and
`lean4/FiniteQM.lean::weyl_heisenberg_finite_trace_obstruction` check the trace identity for
$2\times2$ matrices. The general $n$ is the argument above.

### 4.2 The Pythagorean rotation has infinite order

DAG node: `FQ-DISCRETE-DYNAMICS-DICHOTOMY`

**Proposition.** The rotation $R=\frac15\begin{pmatrix}3&-4\\4&3\end{pmatrix}$ satisfies
$R^n\neq I$ for every $n\ge1$.

*Proof.* Identify $R$ with multiplication by $z=(3+4i)/5$. Then $R^n=I$ iff $(3+4i)^n=5^n$. Modulo
5, $(3+4i)^2=-7+24i\equiv3+4i$, so $(3+4i)^n\equiv3+4i\pmod5$ for all $n\ge1$, and the imaginary
part of $(3+4i)^n$ is $\equiv4\pmod5$, never $0$. $\square$

So a normalized rational unitary need not be periodic, while a periodic sector (a root of unity)
has to be declared. The DAG statement records only this half; a dichotomy for all finite
unitaries, and any closure or topology on the orbit, are not claimed.

Lean: `lean4/H061DynamicsDichotomy.lean::pythagorean_rotation_order_infinite` proves that the
imaginary part of $(3+4i)^{n+1}$ is never zero, by the residue argument above;
`lean4/H061DynamicsDichotomy.lean::periodic_sector_requires_declaration` records the declared
periodic sector.

### 4.3 Discrete time does not determine a generator

DAG node: `FQ-DISCRETE-TIME-STONE-AMBIGUITY`

**Proposition.** (i) There is no map $\sigma\colon\{0,1\}\to\{0,1\}$ with $\sigma\circ\sigma$ the
transposition. (ii) The Pauli matrix $X$ has the two distinct square roots
$\pm\frac12\begin{pmatrix}1+i&1-i\\1-i&1+i\end{pmatrix}$ in $M_2(\mathbb Q(i))$. (iii) The
Hermitian $H$ with $e^{-iH}=X$ are exactly those diagonal in the eigenbasis of $X$ with eigenvalues
$2\pi k$ on the $+1$ eigenspace and $\pi(2k'+1)$ on the $-1$ eigenspace, $k,k'\in\mathbb Z$;
distinct $k'$ give distinct generators.

*Proof.* (i) If $\sigma^2$ is a bijection then $\sigma$ is injective, hence a permutation of a
two-element set, and the square of a permutation is even while a transposition is odd. (ii)
$M=\begin{pmatrix}1+i&1-i\\1-i&1+i\end{pmatrix}$ has
$M^2=\begin{pmatrix}(1+i)^2+(1-i)^2&2(1+i)(1-i)\\2(1+i)(1-i)&(1+i)^2+(1-i)^2\end{pmatrix}
=\begin{pmatrix}0&4\\4&0\end{pmatrix}$, so $(\pm M/2)^2=X$. (iii) $e^{-iH}$ commutes with $H$, so
$H$ preserves the eigenspaces of $X$; on each (one-dimensional) eigenspace $e^{-ih}=\pm1$ fixes $h$
modulo $2\pi$ and nothing more. $\square$

A unitary step on a finite carrier admits square roots and logarithms over a suitable field, but
not uniquely; the report-level toggle in (i) has no square root. Selecting a continuous one-parameter group
requires a branch choice that the discrete data do not supply.

Lean: `lean4/H055DiscreteDynamicsStone.lean::no_bool_half_step` proves (i);
`lean4/H055DiscreteDynamicsStone.lean::interpolant_not_unique` checks (ii) as
$M^2=4X$; `lean4/H055DiscreteDynamicsStone.lean::stone_discrete_generator_ambiguity` records that
the odd branches $2k'+1$ are pairwise distinct.

### 4.4 The off-diagonal term of a global weight

DAG node: `DS-QM043-OFFDIAG-GLOBAL-WEIGHT-IDENTITY`

**Proposition.** For a symmetric $D=\begin{pmatrix}d_{11}&d_{12}\\d_{12}&d_{22}\end{pmatrix}$ with
integer entries, $\mathbf 1^{\mathsf T}D\mathbf 1-\operatorname{tr}D=2d_{12}$.

*Proof.* $\mathbf 1^{\mathsf T}D\mathbf1=d_{11}+2d_{12}+d_{22}$. $\square$

The global weight of the coherent sum differs from the sum of local weights by exactly the
interference term. Phase-class descent of this term to a $U(1)$ cohomology class is not part of
the statement.

Lean: `lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm021_040_041_043_commutator_heisenberg_global_weight_and_conditioning`,
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality`.

### 4.5 Branch counting reproduces only rational weights

DAG node: `FQ-EVERETT-RATIONAL-SECTOR-BOUNDARY`

**Proposition.** (i) Natural weights $p_0+p_1=D>0$ are reproduced by an equal-weight fine graining
into $D$ branches, $p_0$ of them labelled 0. (ii) The Born weights $\frac{5\pm\sqrt5}{10}$, the
roots of $5x^2-5x+1$, are irrational, so no equal-weight fine graining into finitely many branches
reproduces them.

*Proof.* (i) is immediate: the fraction of branches labelled $j$ is $p_j/D$. (ii) By the rational
root theorem a rational root of $5x^2-5x+1$ is one of $\pm1,\pm\frac15$; the polynomial takes the
values $1,11,\frac15,\frac{11}5$ there. A fine graining into $D$ equal branches gives weights in
$\frac1D\mathbb Z$. $\square$

Counting branches therefore reproduces the Born rule exactly on rational-weight sectors and fails
on sectors with irrational weights such as these. Reading branch counts as probabilities is an interpretive input.

Lean: `lean4/H059RationalSector.lean::rational_finegraining_exists`,
`lean4/H059RationalSector.lean::conductors_with_real_q_yield_rational_finegraining`,
`lean4/H059RationalSector.lean::witness_poly_has_no_candidate_rational_root` (the four candidate
values, cleared of denominators).

---

## 5. Entropy

### 5.1 Purity and transcendence of von Neumann entropy

DAG node: `FQ-ENTROPY-DICHOTOMY-BAKER`

**Theorem.** Let $p_1,\dots,p_d$ be the spectrum of a density matrix, all $p_i$ algebraic, and
$S=-\sum_ip_i\log p_i$ (with $0\log0=0$). Then (i) $S=0$ if and only if some $p_j=1$ (the state is
pure); (ii) $S>0$ otherwise; (iii) if the state is mixed, $S$ is transcendental.

*Proof.* (i) Each term $-p\log p$ is $\ge0$ on $[0,1]$ and vanishes only at $p\in\{0,1\}$. So
$S=0$ iff every $p_i\in\{0,1\}$, and with $\sum p_i=1$ that means exactly one $p_j=1$. (ii)
follows from (i) and nonnegativity. (iii) Write $S=\sum_{p_i>0}p_i\log(1/p_i)$, a linear form in
logarithms of the algebraic numbers $1/p_i$ with algebraic coefficients $p_i$. By Baker's theorem
such a form is either $0$ or transcendental, and by (ii) it is not $0$. $\square$

Baker's theorem enters (iii) as a cited result; in Lean it is a hypothesis of the theorem. The
integer identity $(p+q)^2=p^2+q^2+2pq$ gives the corresponding Rényi-2 statement for a
two-level spectrum $(p,q)/(p+q)$: the purity deficit $2pq$ vanishes iff $p=0$ or $q=0$.

Lean: `lean4/EntropyDichotomy.lean::entropy_zero_iff_pure`,
`lean4/EntropyDichotomy.lean::mixed_entropy_positive`,
`lean4/EntropyPurity.lean::mixed_entropy_is_transcendental` (with Baker as the hypothesis
`BakerHypothesis`),
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_entropy_renyi_purity_dichotomy_and_qm122_six_import_drop_one_census`.

---

## 6. The Hilbert lift of the exact carriers

DAG node: `FQ-CONTINUUM-HILBERT-LIFT-CONSTRUCTION`

This section states what follows once two inputs are supplied: a scalar field
$\mathbb K\in\{\mathbb R,\mathbb C\}$ and the $\ell^2$ uniformity. Their selection from finite
primitives is a separate, open question.

Let $F_n=\mathbb Q^n$ with $\langle x,y\rangle=\sum x_iy_i$, and
$\iota_{n,m}\colon F_n\to F_m$ ($n\le m$) zero padding. Let $c_{00}(\mathbb K)$ be the finitely
supported sequences $\mathbb N\to\mathbb K$ with $\langle f,g\rangle=\sum\overline{f_i}g_i$, and
$\mathcal H_{\mathbb K}$ its Hausdorff completion. Write
$h_N=\sum_{i<N}\frac1{i+1}e_i\in c_{00}(\mathbb Q)$.

**Theorem.**

1. The $F_n$ with the maps $\iota_{n,m}$ form a directed system of injective isometries whose
   colimit is $c_{00}(\mathbb Q)$; every element of $c_{00}(\mathbb Q)$ lies in the image of
   some $F_n$.
2. $\mathcal H_{\mathbb K}$ is a Hilbert space, and the map
   $\lambda\colon c_{00}(\mathbb Q)\to\mathcal H_{\mathbb K}$ is injective, preserves inner
   products and is compatible with the $\iota_{n,m}$.
3. A sequence $(f_k)$ in $c_{00}(\mathbb Q)$ has $(\lambda f_k)$ Cauchy if and only if for every
   rational $\varepsilon>0$ there is $K$ with $\|f_k-f_l\|^2<\varepsilon$ for $k,l\ge K$; every
   such sequence converges in $\mathcal H_{\mathbb K}$.
4. For $\mathbb K=\mathbb R$: $\lambda$ has dense image, continuous maps from
   $\mathcal H_{\mathbb R}$ into a Hausdorff space are determined by their values on $\lambda(c_{00}(\mathbb Q))$, and
   $\lambda$ is not surjective.
5. For $\mathbb K=\mathbb C$: pairs $(a,b)$ of rational sequences, read as $a+ib$, are dense, and
   $\langle a+ib,c+id\rangle=(\langle a,c\rangle+\langle b,d\rangle)+i(\langle a,d\rangle-\langle b,c\rangle)$.
6. The uniformity on $c_{00}(\mathbb Q)$ induced from $\mathcal H_{\mathbb R}$ has the rational
   balls $\{(f,g):\|f-g\|^2<\varepsilon\}$, $\varepsilon\in\mathbb Q_{>0}$, as a basis, and the
   completion of $c_{00}(\mathbb Q)$ for it is uniformly isomorphic to $\mathcal H_{\mathbb R}$.
7. $\mathcal H_{\mathbb K}$ is isometrically isomorphic to $\ell^2(\mathbb N,\mathbb K)$, with
   $\lambda f$ corresponding to the sequence $f$.
8. A $\mathbb Q$-linear $A$ on $c_{00}(\mathbb Q)$ with $\|Af\|^2\le C\|f\|^2$ for a rational
   $C\ge0$ extends uniquely to a continuous $\mathbb R$-linear operator $T$ on
   $\mathcal H_{\mathbb R}$ with $\|T\|\le\sqrt C$; the unilateral shift extends to an isometry.
   The $\mathbb Q$-linear functional $\sigma(f)=\sum_if_i$ has no continuous extension.

*Proof.* (1) Zero padding is linear, injective and preserves the sum of products; it is
functorial, $\iota_{m,k}\iota_{n,m}=\iota_{n,k}$. An element of $c_{00}(\mathbb Q)$ with support in
$\{0,\dots,n-1\}$ is the image of its truncation in $F_n$, and these images are compatible, which
is the colimit property.

(2) $c_{00}(\mathbb K)$ is an inner product space. The inner product is uniformly continuous on
bounded sets, so it extends to the completion, where it still satisfies the inner-product axioms
by continuity; the completion is complete by construction. The rational inner product of
$f,g\in c_{00}(\mathbb Q)$ equals the $\mathbb K$ inner product of their images, so $\lambda$
preserves inner products, hence norms, hence is injective. Compatibility with padding holds
because padding does not change the sequence.

(3) $\lambda$ is isometric, so $(\lambda f_k)$ is Cauchy iff $\|f_k-f_l\|\to0$. Because rationals are
dense in $(0,\infty)$, it suffices to test squared distances against rational $\varepsilon$.
Convergence follows from completeness.

(4) Given $x\in\mathcal H_{\mathbb R}$ and $\varepsilon>0$, choose $f\in c_{00}(\mathbb R)$ with
$\|x-f\|<\varepsilon/2$, then round each of the finitely many nonzero coordinates of $f$ to a
rational within $\varepsilon/(2\sqrt{N})$, where $N>0$ is the support size (if the support is empty, take the zero rational sequence). Two continuous maps into a
Hausdorff space that agree on a dense set agree. The sequence $h_N$ is Cauchy, since, for $M>N\ge1$,
$\|h_M-h_N\|^2=\sum_{N\le i<M}(i+1)^{-2}<1/N$; its limit has coordinate $1/(i+1)$ at every $i$, so it
is not $\lambda f$ for any finitely supported $f$.

(5) Approximate the real and imaginary parts separately as in (4). The identity is the expansion
$\overline{(a_j+ib_j)}(c_j+id_j)=a_jc_j+b_jd_j+i(a_jd_j-b_jc_j)$, summed over $j$.

(6) The induced uniformity is generated by $\{(f,g):\|f-g\|<r\}$, $r>0$ real. Each such set
contains a rational ball (take rational $0<\varepsilon<r^2$) and each rational ball is one of them
($r=\sqrt\varepsilon$). The embedding $c_{00}(\mathbb Q)\to\mathcal H_{\mathbb R}$ is uniformly
inducing with dense image into a complete Hausdorff space, which characterizes the completion up to
unique uniform isomorphism.

(7) The coordinate map $c_{00}(\mathbb K)\to\ell^2$ is a linear isometry with dense image, because
finitely supported sequences are dense in $\ell^2$. It extends to a linear isometry
$\mathcal H_{\mathbb K}\to\ell^2$, whose image is complete, hence closed, and dense, hence
everything.

(8) $\|Af-Ag\|\le\sqrt C\|f-g\|$, so $A$ is uniformly continuous and extends uniquely to a
uniformly continuous $T$ on the completion. $T$ is additive and $\mathbb Q$-homogeneous by
continuity, hence $\mathbb R$-homogeneous by density of $\mathbb Q$ in $\mathbb R$ and continuity of
scalar multiplication, and $\|Tx\|^2\le C\|x\|^2$ passes to limits. The shift preserves
$\|f\|^2$, so $C=1$ and $T$ is an isometry. If $\sigma$ had a continuous extension $\bar\sigma$, then
$\bar\sigma(\lambda h_N)$ would converge, because $(\lambda h_N)$ converges; but
$\sigma(h_N)=\sum_{i=1}^N\frac1i$ diverges, although $\|h_N\|^2\le\sum_i i^{-2}<2$. $\square$

Dynamics and generators are not lifted here, and which exact operators satisfy a rational bound is
a hypothesis on the operator.

Lean: `lean4/HilbertLiftFiniteTower.lean::HilbertLift.exhaustion` (1);
`lean4/HilbertLiftCompletion.lean::HilbertLift.controlled_completion` (2–4);
`lean4/HilbertLiftComplexCarrier.lean::HilbertLift.controlled_completion_complex` (5);
`lean4/HilbertLiftIntrinsicUniformity.lean::HilbertLift.uniformity_eq_iInf_sqdist` and
`lean4/HilbertLiftIntrinsicUniformity.lean::HilbertLift.intrinsic_completion` (6);
`lean4/HilbertLiftL2Model.lean::HilbertLift.l2_model_summary` (7);
`lean4/HilbertLiftOperators.lean::HilbertLift.operator_lift_summary` and
`lean4/HilbertLiftOperators.lean::HilbertLift.no_continuous_extension_coordSum` (8);
`lean4/HilbertLiftRationalUniformity.lean::HilbertLift.harmonic_separates_uniformities` (the
harmonic sequence is $\ell^2$-Cauchy but not $\ell^1$-Cauchy).

---

## 7. Three supplied structures that the Gaussian carrier lacks

DAG node: `GP-DROP-ONE-CENSUS`

The census lists eight structures supplied beyond the finite Gaussian carrier: the field
$\mathbb C$, the spectral theorem, Gleason's theorem for $n\ge3$, the CPTP class, uniqueness of the
tensor product, the circle group, continuous time and a dual certificate checked outside Lean. It
records three as lost when dropped and leaves the necessity of the other five open. The
mathematical content of the three verdicts is the following.

**Proposition.** (i) $\mathbb Z[i]$ is not a field: $1+i$ has no inverse. (ii) The Hermitian
matrix $\begin{pmatrix}0&1+i\\1-i&0\end{pmatrix}\in M_2(\mathbb Z[i])$ has no eigenvalue in
$\mathbb Z[i]$. (iii) On the two-element report set the toggle has no square root (§4.3 (i)).

*Proof.* (i) The norm $N(a+bi)=a^2+b^2$ is multiplicative, $N(1+i)=2$ and $N(1)=1$, and no Gaussian
integer has norm $\frac12$. (ii) The characteristic polynomial is $\lambda^2-|1+i|^2=\lambda^2-2$,
whose roots $\pm\sqrt2$ are not in $\mathbb Q(i)$. (iii) was proved in §4.3. $\square$

This is a census of eight items with three verdicts, not a necessity theorem for the remaining
five.

Lean: `lean4/H017ExtrasDropone.lean::drop_one_count`,
`lean4/H017Finish.lean::remaining_import_list`.

---

## 8. Structure of the finite carrier

### 8.1 The clock-and-shift representation is irreducible

DAG node: `FQ-WEYL-FINITE-SCHRODINGER-IRREDUCIBILITY`

Let $d\ge2$, $\omega$ a primitive $d$-th root of unity in a field $K$, and on $K^d$ with basis
$e_0,\dots,e_{d-1}$ (indices mod $d$) let $Ze_k=\omega^ke_k$ and $Xe_k=e_{k+1}$.

**Theorem.** (i) $ZX=\omega XZ$, hence $X^aZ^bX^{-a}Z^{-b}=\omega^{-ab}I$. (ii) A matrix commuting
with $Z$ and $X$ is scalar. (iii) The $d^2$ products $X^aZ^b$ span $M_d(K)$, so the representation
generated by $X$ and $Z$ is irreducible.

*Proof.* (i) $ZXe_k=\omega^{k+1}e_{k+1}=\omega XZe_k$. Moving $Z^b$ past $X^a$ one factor at a time
gives $Z^bX^a=\omega^{ab}X^aZ^b$, so $X^aZ^b=\omega^{-ab}Z^bX^a$ and
$X^aZ^bX^{-a}Z^{-b}=\omega^{-ab}Z^bX^aX^{-a}Z^{-b}=\omega^{-ab}I$. (ii) If $AZ=ZA$ then
$\omega^iA_{ij}=A_{ij}\omega^j$, and the eigenvalues $\omega^i$ are distinct, so $A$ is diagonal. If
also $AX=XA$ then $A_{k+1,k+1}=A_{kk}$ for all $k$, so $A$ is scalar. (iii) $X^aZ^b$ has its nonzero
entries $\omega^{bk}$ at the positions $(k+a,k)$. For fixed $a$, the vectors $(\omega^{bk})_k$,
$b=0,\dots,d-1$, are the rows of a Vandermonde matrix with distinct nodes $\omega^k$, so they span
$K^d$; hence the $X^aZ^b$ span every matrix supported on the $a$-th cyclic diagonal, and all $a$
together span $M_d(K)$. An invariant subspace of the generated algebra is invariant under all
matrices, so it is $0$ or $K^d$. $\square$

The statement is finite and exact; nothing is claimed in infinite dimension.

Lean: `lean4/WeylCommutant.lean::clock_shift_commutant_scalar` proves (ii) for any $n+1$, any field
and any distinct clock eigenvalues.
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_power_p2_cabello_146_and_weyl_commutant_irreducibility`
checks the $2\times2$ case of (ii): $\begin{pmatrix}a&b\\c&d\end{pmatrix}$ commutes with $Z$ and $X$
iff $b=c=0$ and $a=d$. Parts (i) and (iii) are the computations above; the DAG records the $d=3$
case as an exact computation.

### 8.2 $\mu_N$-valued gauge fields on a finite graph

DAG node: `FQ-U1-TRANSPORT-N-TORSION`

Let $N\ge1$ and let $G$ be a finite connected graph with at least one vertex, $V$ vertices, $E$ edges and $\beta_1=E-V+1$, and
$\mu_N\subset\mathbb Q(\zeta_N)^\times$ the $N$-th roots of unity. An edge cochain
$\tau\colon\vec E\to\mu_N$ ($\tau(\bar e)=\tau(e)^{-1}$) is gauge-equivalent to $\tau'$ when
$\tau'(u\to v)=g(u)\tau(u\to v)g(v)^{-1}$ for some $g\colon V\to\mu_N$.

**Theorem.** (i) There are exactly $N^{\beta_1}$ gauge classes, and the holonomy map identifies them
with $\operatorname{Hom}(H_1(G,\mathbb Z),\mu_N)$. (ii) For two paths $p_1,p_2$ with the same ends,
the relative phase $\tau(p_1)\tau(p_2)^{-1}$ is the holonomy of the loop $p_1p_2^{-1}$ and is gauge
invariant. (iii) In the sign group $\{\pm1\}$ every element squares to $1$; in the Gaussian units
$i^2=-1\neq1$, and in $\mu_3$, $\zeta_3^2\neq1$.

*Proof.* (i) The gauge group $\mu_N^V$ acts on $\mu_N^E$; the stabilizer of any $\tau$ is the
constant functions, because $G$ is connected. So every orbit has $N^{V}/N=N^{V-1}$ elements and
there are $N^E/N^{V-1}=N^{\beta_1}$ orbits. Holonomy around closed paths is gauge invariant (the
$g$ factors cancel at each vertex) and defines a homomorphism $H_1(G,\mathbb Z)\to\mu_N$. It is
injective on classes: if all holonomies are trivial, fix a spanning tree $T$ and a root $r$, put
$g(v)=\tau(\text{tree path } r\to v)$; then $g$ gauges $\tau$ to $1$ on $T$, and on each remaining
edge to the holonomy of its fundamental cycle, which is $1$. Apply this to the ratio of two cochains with equal holonomies to obtain injectivity. Since $H_1(G,\mathbb Z)\cong\mathbb Z^{\beta_1}$,
$|\operatorname{Hom}(H_1,\mu_N)|=N^{\beta_1}$, so the injection is a bijection. (ii) Gauge factors at
the interior vertices cancel and those at the common ends cancel between $p_1$ and $p_2^{-1}$.
(iii) is immediate. $\square$

So the sign group cannot carry a phase whose square is nontrivial, while $\mathbb Z[i]^\times$ and
$\mu_3$ can.

Lean: `lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_u1_transport_n_torsion_and_sign_separation`
(gauge invariance of triangle holonomy modulo $N$, written additively),
`lean4/H011Circle.lean::sign_fails_connectedness_shadow` (iii),
`lean4/H011U1SelectorBoundary.lean::u1_selector_boundary` (the selector is not derived, and the
integer realization of §1.3 separates two points of one fibre). The count $N^{\beta_1}$ is the
argument above; the DAG records it as an exact enumeration on small graphs.

### 8.3 Tensor product versus a bilinear rival

DAG node: `FQ-TENSOR-LU-RIVAL-EXCLUSION`

**Proposition.** (i) Let $\boxtimes\colon\mathbb Z^2\times\mathbb Z^2\to\mathbb Z^{2\times2}$ be
bi-additive, $\mathbb Z$-homogeneous in each argument, and Kronecker-normalized,
$e_i\boxtimes e_j=e_{(i,j)}$. Then $u\boxtimes v=u\otimes v$, i.e.
$(u\boxtimes v)_{(i,j)}=u_iv_j$. (ii) Without the normalization, the bilinear rule
$u\boxtimes' v=(v_0+v_1)\,u$ (into $\mathbb Z^2$) is not covariant under the local unitary $Z$ on
the second factor: there is no $W$ with $u\boxtimes'(Zv)=W(u\boxtimes'v)$ for all $u,v$.

*Proof.* (i) $u\boxtimes v=\sum_{i,j}u_iv_j\,e_i\boxtimes e_j=\sum_{i,j}u_iv_je_{(i,j)}$. (ii)
$e_0\boxtimes'Ze_0=e_0\boxtimes'e_0=e_0$ forces $We_0=e_0$, but
$e_0\boxtimes'Ze_1=e_0\boxtimes'(-e_1)=-e_0$ while $W(e_0\boxtimes'e_1)=We_0=e_0$. $\square$

The normalization or a covariance requirement is what excludes the rival; neither is derived here.

Lean: `lean4/H014BilinearProduct.lean::bilinear_product_unique_on_bool_prod` (i),
`lean4/H014Interface.lean::dumpRight_not_tensor` (the rival into $\mathbb Z^{2\times2}$ differs from
$\otimes$), `lean4/H062CompositionTensorMub.lean::rival_fails_local_unitary_covariance` (the two
values $e_0$ and $-e_0$ in (ii)).

### 8.4 An informationally complete four-outcome POVM, and positivity at real places

DAG node: `FQ-BUSCH-EFFECT-FRAME`

**Proposition.** (i) With Bloch vectors $r_1=(\frac35,0,\frac45)$, $r_2=(-\frac35,0,\frac45)$,
$r_3=(0,\frac35,-\frac45)$, $r_4=(0,-\frac35,-\frac45)$, the operators
$E_k=\frac14(I+r_k\cdot\sigma)$ are rank-one effects summing to $I$, and they are linearly
independent, so the outcome probabilities $\operatorname{tr}(\rho E_k)$ determine $\rho$. (ii) In
$\mathbb Q(\sqrt5)$, $\alpha=-\frac18+\frac18\sqrt5$ is positive at the embedding $\sqrt5>0$ and
negative at the other, while a sum of squares $\sum\beta_i^2$ is nonnegative at both.

*Proof.* (i) $|r_k|^2=\frac9{25}+\frac{16}{25}=1$, so $E_k$ has eigenvalues $\frac12$ and $0$.
$\sum_kr_k=0$ gives $\sum E_k=I$. Writing $E_k$ in the basis $(I,\sigma_x,\sigma_y,\sigma_z)$, the
coefficient matrix has rows $\frac14(1,r_k)$ and
$\det\begin{pmatrix}1&r_1\\\vdots&\vdots\\1&r_4\end{pmatrix}=\frac{288}{125}=(\frac65)^2\cdot\frac85\neq0$.
So the map $\rho\mapsto(\operatorname{tr}\rho E_k)_k$ is injective on Hermitian matrices. (ii)
$\alpha$'s norm is $\frac1{64}-\frac5{64}=-\frac1{16}<0$, so its two conjugates have opposite signs,
and $\alpha>0$ since $\sqrt5>1$. Each real embedding $\sigma$ is a ring homomorphism, so
$\sigma(\sum\beta_i^2)=\sum\sigma(\beta_i)^2\ge0$. $\square$

Positivity checked at one real place is not total positivity; a sum-of-squares certificate is.
Frame additivity on finitely many rays also does not give positivity (§2.4 (ii)).

Lean: `lean4/FiniteQM.lean::busch_ic_povm_vs_polyhedral_frame_cone` (traces, determinants, Bloch
sums and the reconstruction determinant),
`lean4/FiniteQM.lean::galois_conjugate_negativity_vs_sos_total_positivity` (ii),
`lean4/H058EffectFrameBusch.lean::two_mul_half`.

### 8.5 The helium variational bound

DAG node: `FQ-QM207-231-FINITE-MAP-CONTROLS`

This node collects twenty-five finite controls. The part with a general mathematical statement is
the helium ground-state estimate with an effective nuclear charge.

**Proposition.** In atomic units, with the trial state a product of hydrogenic $1s$ orbitals of
charge $Z>0$ for nuclear charge 2, $E(Z)=Z^2-\frac{27}8Z$. Its minimum over $Z$ is at
$Z^\ast=\frac{27}{16}$ with $E(Z^\ast)=-\frac{729}{256}$, and $E(Z)-E(Z^\ast)=(Z-Z^\ast)^2$. At $Z^\ast$
the virial relation $2T+V=0$ holds, and $E(Z^\ast)<-\frac{11}4$, the first-order perturbative value.

*Proof.* The kinetic energy is $T=Z^2$, the electron-nucleus energy $-2\cdot2Z=-4Z$ and the
electron-electron energy $\frac58Z$, so $V=-\frac{27}8Z$ and $E=Z^2-\frac{27}8Z$. Completing the
square, $E=(Z-\frac{27}{16})^2-\frac{729}{256}$. At $Z^\ast$, $2T+V=Z^\ast(2Z^\ast-\frac{27}8)=0$.
Finally $-\frac{729}{256}<-\frac{704}{256}=-\frac{11}4$. $\square$

The orbital integrals ($T$, $\frac58Z$) are the standard hydrogenic values and are taken as input.

Lean: `lean4/FiniteQM.lean::helium_kellner_variational_bound_and_virial_identity` (the identities
above for every rational $Z$, and a four-term Hylleraas value below $E(Z^\ast)$),
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_qm207_231_finite_map_controls_master_certificate`.
