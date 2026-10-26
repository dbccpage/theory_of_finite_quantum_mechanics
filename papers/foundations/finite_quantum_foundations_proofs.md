<div align="center">

# Finite Quantum Foundations: Proofs of the Structure Results

**Author:** Jeremy H. Carroll

**Date:** 2026-10-26

**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)

</div>

## Introduction

This note gives written proofs of the results of the foundation papers `qm_060` to `qm_212` in this
folder that the derivation DAG (`dag/derivation_dag.json`) records as proved in Lean. Its companion
for the core paper is [finite_quantum_mechanics_proofs.md](../core/finite_quantum_mechanics_proofs.md),
cited below as *Core*. Each section states one result, proves it, and names the Lean declarations
that check it; the DAG identifier is on the line beginning *DAG node*.

Several of these DAG nodes carry a statement narrowed during review to what an exact computation
or a Lean declaration covers. Where a general theorem behind the narrowed statement has a short
proof, it is given here, and the closing remark says which part Lean checks. Nothing here changes a
DAG status.

**Notation.** As in *Core*: $w_v(q)=|v(q)|^2$ is the phase-blind weight of a report vector;
$\Delta$ is the diagonal pinching (dephasing) in a fixed basis; $\|\cdot\|_1$ is the trace norm, or
the $\ell^1$ norm on vectors; $X,Z$ are the Pauli matrices.

---

## 1. Superposition and interference

### 1.1 Phase lies in the fibre and returns as a cross term

DAG node: `DS-QM060-SUPERPOSITION-QUOTIENT-FIBER`

**Proposition.** Let $c_s=\sqrt{w_s}\,e^{i\theta_s}$ for $s=1,2$. Then $|c_s|^2=w_s$ does not depend
on $\theta_s$, and
$$|c_1+c_2|^2=w_1+w_2+2\sqrt{w_1w_2}\cos(\theta_2-\theta_1).$$
In particular $(1,1)$ and $(1,-1)$ have the same weights $(1,1)$ and the coherent sums $4$ and $0$.

*Proof.* $|c_s|^2=w_s|e^{i\theta_s}|^2=w_s$. Expanding,
$|c_1+c_2|^2=|c_1|^2+|c_2|^2+2\operatorname{Re}(\bar c_1c_2)$ and
$\bar c_1c_2=\sqrt{w_1w_2}\,e^{i(\theta_2-\theta_1)}$. $\square$

So the phase-blind map forgets exactly the phases, a global phase is invisible even in the coherent
sum, and the relative phase reappears in the cross term once two amplitudes are added. The
amplitude lift $c=\sqrt w\,e^{i\theta}$ is supplied.

Lean: `lean4/H009PhaseFiber.lean::phase_fiber` (global and relative phases lie in the fibre, and
$(1,-1)$ is not a unit multiple of $(1,1)$),
`lean4/H009PhaseFiber.lean::global_phase_in_fiber`,
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm060_061_phase_fiber_and_interference_non_descent`
(the sums $4$ and $0$ on one fibre point).

### 1.2 Total weight does not compute the interfered weight

DAG node: `DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE`

**Proposition.** For $v=(v_0,v_1)\in\mathbb Z[i]^2$ let $L(v)=|v_0|^2+|v_1|^2$ and
$I(v)=|v_0+v_1|^2$. Then $I(v)-L(v)=2\operatorname{Re}(\bar v_0v_1)$, and there is no function $f$ with
$I=f\circ L$; nor is there a function of the weight vector $w_v$ that gives $I$.

*Proof.* The identity is §1.1. The vectors $(1,1)$ and $(1,-1)$ have the same weight vector
$(1,1)$, hence the same $L=2$, but $I=4$ and $I=0$. $\square$

Lean: `lean4/InterferenceDeficit.lean::deficit_eq_cross_term`,
`lean4/InterferenceDeficit.lean::L1_cannot_compute_interference`,
`lean4/H010InterferenceNonDescent.lean::interference_non_descent`.

### 1.3 Holonomy and two-path intensity

DAG node: `DS-QM063-HOLONOMY-COHERENT-INTENSITY`

Let $G$ be a graph, $A$ an edge 1-cochain with values in an abelian group written additively (phases
$e^{iA}$ in the $U(1)$ case), and $(d\varphi)(u\to v)=\varphi(v)-\varphi(u)$ for a vertex function
$\varphi$. The holonomy of a path is the sum of $A$ along it.

**Proposition.** (i) A coboundary $d\varphi$ has zero holonomy around every closed path. (ii) If
some triangle has nonzero holonomy, $A$ is not a coboundary. (iii) On a tree every 1-cochain is a
coboundary. (iv) For two paths $p_1,p_2$ from $s$ to $t$ with amplitudes $z_k=r_ke^{iA(p_k)}$,
$$|z_1+z_2|^2=r_1^2+r_2^2+2r_1r_2\cos\big(A(p_2)-A(p_1)\big),$$
and both $A(p_2)-A(p_1)$ (the holonomy of the loop $p_2p_1^{-1}$) and the intensity are invariant
under the gauge change $A\mapsto A+d\varphi$ and under a common phase $z_k\mapsto uz_k$, $|u|=1$.

*Proof.* (i) Along $v_0\to v_1\to\dots\to v_n=v_0$ the sum $\sum(\varphi(v_{k+1})-\varphi(v_k))$
telescopes to $0$. (ii) is the contrapositive of (i). (iii) Fix a root $r$, put $\varphi(r)=0$, and
define $\varphi(v)$ as the holonomy of the unique path from $r$ to $v$; then $A=d\varphi$ on every
edge, since each edge lies on the root path of its far endpoint. (iv) The formula is §1.1 with
$\theta_k=A(p_k)$. A gauge change adds $\varphi(t)-\varphi(s)$ to both $A(p_1)$ and $A(p_2)$, so
their difference is unchanged; a common phase multiplies $\bar z_1z_2$ by $|u|^2=1$. $\square$

Intensity therefore does not factor through the weights $r_k^2$ when the holonomy varies.
Higher-form holonomy and matrix-valued (non-abelian) connections are outside this statement.

Lean: `lean4/CoboundaryHolonomy.lean::coboundary_closed_cycle_zero` (i),
`lean4/CoboundaryHolonomy.lean::flux_obstructs_coboundary` (ii),
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm063_tree_gauge_triviality_vertex_repair_and_l1_non_factorization`
((iii) on a three-edge tree, and the cross-term identity over $\mathbb Z[i]$),
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm063_holonomy_coherent_intensity_and_gauge_invariance`
((iv) over $\mathbb Z[i]$ with the common phase $i$).

### 1.4 Gauge invariance of triangle holonomy, and two annex identities

DAG node: `DS-QM064-074-083-ANNEX-REDIRECT-ROWS`

**Proposition.** (i) For a triangle with edge values $w_{01},w_{12},w_{20}$ and vertex gauge
$f_0,f_1,f_2$,
$(w_{01}+f_1-f_0)+(w_{12}+f_2-f_1)+(w_{20}+f_0-f_2)=w_{01}+w_{12}+w_{20}$. (ii) A column-stochastic
matrix does not increase the $\ell^1$ norm (§3.3).

*Proof.* (i) The gauge terms cancel in pairs. (ii) is proved in §3.3. $\square$

The no-signalling condition that this annex row also names is §2.4.

Lean: `lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm064_triangle_holonomy_gauge_invariant`,
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm081_stochastic_l1_contraction`.

### 1.5 Populations do not see coherence

DAG node: `DS-QM072-QUBIT-SUPERPOSITION-OBSTRUCTED`

**Proposition.** The states $\rho_\pm=\frac12\begin{pmatrix}1&\pm1\\\pm1&1\end{pmatrix}$ and their
dephased mixture $\frac12(\rho_++\rho_-)=\frac12I$ have the same populations $(\frac12,\frac12)$.
The coherent readout $\langle+|\rho|+\rangle$, with $|+\rangle=(|0\rangle+|1\rangle)/\sqrt2$, takes
the values $1$, $0$ and $\frac12$ on them, and the purities $\operatorname{tr}\rho^2$ are $1,1,\frac12$.

*Proof.* $\langle+|\rho|+\rangle=\frac12\sum_{ij}\rho_{ij}=\frac12(1\pm1)$ for $\rho_\pm$, and
$\frac12$ for $\frac12I$. $\operatorname{tr}\rho_\pm^2=\sum_{ij}|\rho_{ij}|^2=1$ and
$\operatorname{tr}(\frac14I)=\frac12$. $\square$

The bit (the population vector) is recoverable from the qubit; superposition is not recoverable
from the bit. The coherent readout is supplied.

Lean: `lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates`
(equal diagonals of $2\rho_\pm$),
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm072_and_c10_hadamard_coherence_separation_vs_pinched_mixture`
and
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm072_bit_shadow_q1_q4_obstruction_and_p7_c10_bloch_refutation`
(the scaled readouts $2,-2,0$ are pairwise distinct).

---

## 2. Composition, correlation and contextuality

### 2.1 Product tables

DAG node: `DS-QM070-PRODUCT-NONFACTORIZATION`

**Proposition.** Let $w\colon A\times B\to\mathbb Q_{\ge0}$ be finite with total $W>0$ and marginals
$w_A(a)=\sum_bw(a,b)$, $w_B(b)=\sum_aw(a,b)$. Then $w=w_A\,w_B^{\mathsf T}/W$ if and only if
$w=xy^{\mathsf T}$ for some vectors $x,y$, i.e. iff the matrix $w$ has rank 1. For $|A|=|B|=2$ this
holds iff $\det w=0$. The table $\frac12\begin{pmatrix}1&0\\0&1\end{pmatrix}$ is not a product.

*Proof.* If $w=xy^{\mathsf T}$ then $w_A=x\,\sigma(y)$, $w_B=y\,\sigma(x)$ and $W=\sigma(x)\sigma(y)$,
where $\sigma$ is the coordinate sum, so $w_Aw_B^{\mathsf T}/W=xy^{\mathsf T}$. The converse is
immediate. A nonzero $2\times2$ matrix has rank 1 iff its determinant vanishes. The given table has
determinant $\frac14$. $\square$

The defect is basis-relative and does not detect entanglement: the Bell state
$(|00\rangle+|11\rangle)/\sqrt2$ and the classical mixture of $|00\rangle,|11\rangle$ give the same
table in the computational basis.

Lean: `lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm070_071_product_nonfactorization_and_entanglement_witness`
(the determinant of $(a_ib_j)$ vanishes for all integers; the identity table is not of that form),
`lean4/H014TensorCompositionBoundary.lean::tensor_not_forced_open` (records that tensor
composition is not derived).

### 2.2 Entanglement witnesses are sound

DAG node: `DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS`

**Proposition.** (i) Let $P_1,\dots,P_m$ be points of a real vector space, $\varphi$ linear, and
$\varphi(P_k)\ge t$ for all $k$. If $\varphi(w)<t$ then $w\notin\operatorname{conv}\{P_k\}$. (ii) For a
two-qubit vector $\psi=\sum c_{ij}|ij\rangle$, $\psi$ is a product vector iff
$c_{00}c_{11}-c_{01}c_{10}=0$; for $|00\rangle+|11\rangle$ this minor is $1$. (iii) For vectors
$w,d$ with $|w_i|\le1$, $|\langle w,d\rangle|\le\|d\|_1$.

*Proof.* (i) For $\lambda_k\ge0$ with $\sum\lambda_k=1$,
$\varphi(\sum\lambda_kP_k)=\sum\lambda_k\varphi(P_k)\ge t$. (ii) $\psi$ is a product iff the
coefficient matrix $(c_{ij})$ has rank at most 1, iff its determinant vanishes. (iii)
$|\sum w_id_i|\le\sum|w_i||d_i|\le\sum|d_i|$. $\square$

Only soundness is claimed: a witness certifies non-membership, and not every entangled state is
shown to have a witness from a given family.

Lean: `lean4/Entanglement.lean::bell_state_is_entangled` (ii),
`lean4/DualWitness.lean::dual_witness_certifies_trace_distance` ((iii) in two coordinates),
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm070_071_product_nonfactorization_and_entanglement_witness`.
Part (i) is the linearity argument above.

### 2.3 Bare tables, CHSH and the PR box

DAG node: `DS-QM073-FINITE-CHSH-AND-PR-BOX`

**Proposition.** (i) Every normalized table $w$ on $A\times B$ is a convex combination of point
product tables $\delta_a\otimes\delta_b$. (ii) If four $\pm1$ variables have one joint law, the CHSH
expression satisfies $|S|\le2$ (*Core* §3.1). (iii) The PR box, $P(a,b\mid x,y)=\frac12$ when
$a\oplus b=xy$ and $0$ otherwise, has correlations $E(x,y)=(-1)^{xy}$, $S=4$, and no joint law.

*Proof.* (i) $w=\sum_{a,b}w(a,b)\,\delta_{(a,b)}$ and $\delta_{(a,b)}=\delta_a\otimes\delta_b$. (ii) is
*Core* §3.1; pointwise $S=A_0(B_0+B_1)+A_1(B_0-B_1)$ and $S^2=4$. (iii)
$E(x,y)=P(a=b)-P(a\neq b)=(-1)^{xy}$, so $S=E(0,0)+E(0,1)+E(1,0)-E(1,1)=4$, and by (ii) no joint law
exists. $\square$

So correlation alone is never entanglement at the level of a single table, and the CHSH bound rests
on one hypothesis: a single global joint law. The Tsirelson ceiling $2\sqrt2$ is a separate result
(*Core* §3.3) and needs the quantum model.

Lean: `lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm073_074_chsh_pr_box_and_no_signaling_marginal`
($S^2=4$ on every deterministic assignment, PR value 4),
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm073_bare_table_separability_single_joint_bound_and_pr_box_obstruction`
((i) in the $2\times2$ case),
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm073_bell_chsh_pythagorean_tsirelson_vs_pr_box_and_local_bound`,
`lean4/ContextualityObstruction.lean::x1_has_no_global_section`.

### 2.4 Local operations do not signal

DAG node: `DS-QM074-NO-SIGNALING-MARGINAL`

**Proposition.** (i) For a state $\rho$ on $\mathcal H_A\otimes\mathcal H_B$ and a unitary $U$ on
$\mathcal H_A$, $\operatorname{tr}_A[(U\otimes I)\rho(U^\dagger\otimes I)]=\operatorname{tr}_A\rho$.
(ii) Equal local marginals do not force a product table: the PR box and the table
$\frac12(\delta_{00}+\delta_{11})$ have uniform marginals and are not products.

*Proof.* (i) In components,
$\big(\operatorname{tr}_A[(U\otimes I)\rho(U^\dagger\otimes I)]\big)_{bb'}=\sum_{a,a_1,a_2}U_{aa_1}\rho_{a_1b,a_2b'}\overline{U_{aa_2}}
=\sum_{a_1,a_2}(U^\dagger U)_{a_2a_1}\rho_{a_1b,a_2b'}=\sum_{a_1}\rho_{a_1b,a_1b'}$.
(ii) For the second table see §2.1. For the PR box, each conditional table $P(\cdot,\cdot\mid x,y)$ is $\frac12$ times a
permutation matrix, whose determinant is $\pm\frac14\neq0$. $\square$

This is a statement about admitted tensor composition, not about relativistic causality.

Lean: `lean4/NoSignalling.lean::no_signalling_under_admitted_composition` ((i) for two qubits with
integer entries), `lean4/Entanglement.lean::non_signaling_under_local_b_flip`,
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm073_074_chsh_pr_box_and_no_signaling_marginal`.

### 2.5 Mermin–Peres: locally satisfiable, globally not

DAG node: `DS-QM120-MERMIN-PERES-F2-OBSTRUCTION`

Write the nine entries of the Mermin–Peres square as $s_0,\dots,s_8\in\mathbb F_2$ ($s=0$ for $+1$),
row-major. The six contexts are the three rows and three columns; the declared parities are $0$
for every row and for the first two columns, and $1$ for the third column.

**Proposition.** (i) No assignment satisfies all six parities. (ii) Every five of the six are
simultaneously satisfiable. (iii) If a global section $g$ exists, the 0-cochain it induces has
$d^0g=0$.

*Proof.* (i) The sum of the three row equations and the sum of the three column equations have the
same left side $\sum_is_i$ and the right sides $0$ and $1$. (ii) The six linear forms are the
incidence vectors of the edges of $K_{3,3}$ at its six vertices (an entry is the edge joining its
row and its column). The incidence matrix of a connected bipartite graph on six vertices has rank
$6-1=5$; over $\mathbb F_2$ the only relation is that the sum of all six forms is zero. Five of the six forms are therefore
independent, and any right-hand side is attained. (iii) $(d^0g)_{ij}=g-g=0$. $\square$

Lean: `lean4/DualWitness.lean::mermin_peres_parity_obstruction` and
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm120_mermin_peres_f2_no_global_section`
(i), `lean4/ContextualityObstruction.lean::d0_of_global_section` (iii). Part (ii) is the rank
argument above; the DAG records the five-context solutions as exact computations.

---

## 3. Distinguishability and channels

### 3.1 The $\ell^1$ core of trace distance

DAG node: `DS-QM080-IMPORT-FREE-TRACE-NORM-CORE`

**Proposition.** On $\mathbb Q^n$: (i) $\|x-y\|_1$ is unchanged when the same vector is added to
$x$ and $y$; (ii) $|\langle w,d\rangle|\le\|d\|_1$ whenever $\|w\|_\infty\le1$; (iii) the bound is
attained by the rational witness $w_i=\operatorname{sgn}d_i$, so
$\|d\|_1=\max_{\|w\|_\infty\le1}\langle w,d\rangle$.

*Proof.* (i) $(x+c)-(y+c)=x-y$. (ii) is §2.2 (iii). (iii)
$\sum_i\operatorname{sgn}(d_i)d_i=\sum_i|d_i|$. $\square$

For matrices, identifying the dual ball with the trace-zero operator-norm ball uses the spectral
theorem; that step is *Core* §2.5.

Lean: `lean4/DualWitness.lean::dual_witness_certifies_trace_distance`,
`lean4/TraceZeroDuality.lean::trace_zero_duality_gap_zero`,
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.trace_zero_pinching_contraction`.

### 3.2 Half trace norm on diagonal states, and its scale

DAG nodes: `DS-QM080-081-TRACE-NORM-CONDITIONAL-SELECTION`, `DS-QM081-CPTP-MONOTONE-NOT-SELECTING`

**Proposition.** (i) For diagonal states $\rho=\operatorname{diag}(p)$ and
$\sigma=\operatorname{diag}(q)$, $\frac12\|\rho-\sigma\|_1=\frac12\sum_i|p_i-q_i|$, the total
variation distance. (ii) If a distance $D$ is contracted by a map $T$, so is $cD$ for every
$c\ge0$; if $D(x,y)>0$, distinct $c$ give distinct values $cD(x,y)$.

*Proof.* (i) The eigenvalues of the diagonal matrix $\rho-\sigma$ are $p_i-q_i$. (ii)
$cD(Tx,Ty)\le cD(x,y)$, and $c_1D=c_2D$ at a point with $D>0$ forces $c_1=c_2$. $\square$

Monotonicity under CPTP maps therefore fixes a distinguishability measure at most up to the
normalization, and the half trace norm is singled out only with further axioms (classical
total-variation reduction among them). Other monotone measures, such as relative entropy, also
exist.

Lean: `lean4/TraceZeroDuality.lean::scaleMetric_monotone`,
`lean4/TraceZeroDuality.lean::monotone_metric_distinct`,
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds`
(the inequality $c|a|\le c(|a|+|b|)$ behind dropping off-diagonal mass).

### 3.3 Stochastic matrices contract $\ell^1$

DAG node: `DS-QM081-STOCHASTIC-L1-CONTRACTION`

**Proposition.** If $S$ is column-stochastic ($S_{ij}\ge0$, $\sum_iS_{ij}=1$) then
$\|Sx\|_1\le\|x\|_1$ for every real vector $x$.

*Proof.* $\|Sx\|_1=\sum_i|\sum_jS_{ij}x_j|\le\sum_j|x_j|\sum_iS_{ij}=\sum_j|x_j|$. $\square$

Lean: `lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm081_stochastic_l1_contraction`
proves the $2\times2$ case with column sums $S$ (giving $\|Sx\|_1\le|S|\,\|x\|_1$).

### 3.4 The population shadow of a channel

DAG node: `DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL`

**Proposition.** Let $\Phi(\rho)=\sum_kK_k\rho K_k^\dagger$ with $\sum_kK_k^\dagger K_k=I$, and
$T_{ij}=\sum_k|\langle i|K_k|j\rangle|^2$. Then $T$ is column-stochastic and
$\operatorname{diag}\Phi(\operatorname{diag}p)=Tp$. The shadow does not determine $\Phi$: the
unitary channel of $H=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$ and the channel
$\rho\mapsto\frac12(\operatorname{tr}\rho)I$ have the same $T$ but send $|0\rangle\langle0|$ to
different states.

*Proof.* $\sum_iT_{ij}=\sum_k\langle j|K_k^\dagger K_k|j\rangle=1$ and $T_{ij}\ge0$. For
$\rho=\operatorname{diag}p$,
$\langle i|\Phi(\rho)|i\rangle=\sum_{k,j}p_j|\langle i|K_k|j\rangle|^2=(Tp)_i$. Both channels have
$T=\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix}$, but $H|0\rangle\langle0|H^\dagger=\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix}\neq\frac12I$.
$\square$

The kernel depends on the basis chosen for the diagonal read.

Lean: `lean4/H018Channel.lean::diagonal_shadow_does_not_fix_channel` (with the unnormalized
$H$: the image of $|0\rangle\langle0|$ dephases to the identity but has a nonzero off-diagonal
entry), `lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm081_082_090_093_stochastic_contraction_channel_shadow_firewall_and_cochain`.

### 3.5 Cochains on quantum packets

DAG node: `DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO`

**Proposition.** (i) For any abelian-group valued 0-cochain $f$ on contexts,
$(d^1d^0f)_{ijk}=(f_j-f_i)+(f_k-f_j)-(f_k-f_i)=0$. (ii) If contexts are related by unitaries
$U_{ij}$ and states and effects are transported by conjugation, the Born pairing
$\operatorname{tr}(\rho E)$ is unchanged: $\operatorname{tr}(U\rho U^\dagger\,UEU^\dagger)=\operatorname{tr}(\rho E)$.

*Proof.* (i) The terms cancel. (ii) $U^\dagger U=I$ and cyclicity of the trace. $\square$

The Born pairing is thus gauge-invariant; invariance does not select it.

Lean: `lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm093_cochain_d1_d0_zero`,
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm081_082_090_093_stochastic_contraction_channel_shadow_firewall_and_cochain`
(the commutator terms of diagonal $\pm1$ matrices vanish).

### 3.6 Relative states with orthogonal records

DAG node: `DS-QM094-EVERETT-RELATIVE-STATE-CONTACT`

**Proposition.** Let $\Psi=\sum_ic_i|i\rangle\otimes|r_i\rangle$ with orthonormal records $r_i$.
(i) $\operatorname{tr}_R|\Psi\rangle\langle\Psi|=\sum_i|c_i|^2|i\rangle\langle i|$. (ii) For any state
$\rho$ and observable $A$,
$|\operatorname{tr}(\rho A)-\operatorname{tr}(\Delta(\rho)A)|\le\max_{i\neq j}|A_{ji}|\cdot\sum_{i\neq j}|\rho_{ij}|$.
(iii) For a qubit, $\Delta(\rho)=\frac12(\rho+Z\rho Z)$.

*Proof.* (i) The $(i,j)$ entry of the reduced state is $c_i\bar c_j\langle r_j|r_i\rangle=|c_i|^2\delta_{ij}$.
(ii) $\operatorname{tr}(\rho A)-\operatorname{tr}(\Delta(\rho)A)=\sum_{i\neq j}\rho_{ij}A_{ji}$.
(iii) $Z\rho Z$ flips the sign of the off-diagonal entries. $\square$

Equal local populations can hide distinguishable coherent states (§1.5). The relative-state
decomposition does not select a branch basis and carries no probability rule.

Lean: `lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_phase_averaged_shadow_and_c10_pinching`
((iii) as $A+ZAZ=2\Delta(A)$, and the phase average
$\frac14\sum_{\pm,\pm}|\pm a_1\pm a_2|^2=|a_1|^2+|a_2|^2$),
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm094_everett_reduced_state_overlap_isometric_refinement_and_collapse_refutation`
((i) for two branches).

---

## 4. Error correction, lattice gauge shadows and Majorana algebra

### 4.1 Syndromes and the correctable weight

DAG node: `DS-QM102-SYNDROME-CAPACITY-BOUND`

**Proposition.** (i) Let $C\subseteq\mathbb F_2^n$ be a linear code of minimum distance $d$ with
parity-check matrix $H$, and $t=\lfloor(d-1)/2\rfloor$. Distinct error patterns of weight at most
$t$ have distinct syndromes $He$. (ii) A nondegenerate quantum code $[[n,1,3]]$ needs
$2(1+3n)\le2^n$; this holds with equality at $n=5$ and fails at $n=4$.

*Proof.* (i) If $He=He'$ then $e-e'\in C$ and $\operatorname{wt}(e-e')\le2t<d$, so $e=e'$. (ii) A
nondegenerate code assigns orthogonal syndrome spaces to the identity and to the $3n$ single-qubit
Pauli errors, each of dimension $2^k=2$, inside a space of dimension $2^n$. $1+3\cdot5=16=2^4$, and
$1+3\cdot4=13>8=2^3$. $\square$

This is the guaranteed-correction direction only. For the three-bit repetition code the syndromes
$(x_1\oplus x_2,x_2\oplus x_3)$ distinguish the four patterns of weight at most one.

Lean: `lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm102_110_111_212_syndrome_hamming_lqg_wilson_and_majorana_braid`
(the Hamming counts), `lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds`.

### 4.2 Kinematical shadows of lattice gauge theory and Regge calculus

DAG node: `DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS`

**Proposition.** (i) In any group, a pure-gauge connection $g_{uv}=h_uh_v^{-1}$ has trivial holonomy
around every closed path. (ii) In the quaternion group $Q_8$, a plaquette with links $i,j,i^{-1},j^{-1}$
has holonomy $iji^{-1}j^{-1}=-1$. (iii) With $a=2j_1$, $b=2j_2$, $c=2j_3$, a trivalent spin-network
vertex is admissible iff $a\le b+c$, $b\le c+a$, $c\le a+b$ and $a+b+c$ is even; so
$(\frac12,\frac12,1)$ is admissible and $(\frac12,\frac12,\frac12)$ is not. (iv) Six equilateral
triangles around a vertex have deficit angle $0$; five have deficit $60^\circ$.

*Proof.* (i) $g_{v_0v_1}g_{v_1v_2}\cdots g_{v_{n-1}v_0}=h_{v_0}h_{v_0}^{-1}=1$ by telescoping.
(ii) $ij=k$ and $i^{-1}j^{-1}=(-i)(-j)=k$, so the product is $k^2=-1$. (iii) These are the
Clebsch–Gordan conditions for $j_3\in j_1\otimes j_2$: $|j_1-j_2|\le j_3\le j_1+j_2$ and
$j_1+j_2+j_3\in\mathbb Z$. For $(1,1,2)$ the sum is $4$; for $(1,1,1)$ it is $3$. (iv)
$360^\circ-6\cdot60^\circ=0$ and $360^\circ-5\cdot60^\circ=60^\circ$. $\square$

These are toy carriers: $Q_8$ is not $SU(2)$, and the continuum connection, the spin-network
Hilbert space and the Einstein equation are outside the statement.

Lean: `lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm110_111_lqg_gr_kinematical_witness`
((iii) and the flat case of (iv)),
`lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm102_110_111_212_syndrome_hamming_lqg_wilson_and_majorana_braid`
((i) for $\mathbb Z_2$ link signs on a square, and (iv)). The $Q_8$ computation (ii) is recorded in
the DAG as an exact computation; the cited Lean declarations do not contain it.

### 4.3 Majorana operators

DAG node: `DS-QM212-MAJORANA-PROBLEM`

**Proposition.** Let $\gamma_1=Z$, $\gamma_2=X$, $P=\gamma_1\gamma_2$ and $B=\frac1{\sqrt2}(I+P)$.
Then $\gamma_1^2=\gamma_2^2=I$, $\gamma_1\gamma_2+\gamma_2\gamma_1=0$, $P^2=-I$, $B^2=P$, and
$B\gamma_1B^{-1}=-\gamma_2$, $B\gamma_2B^{-1}=\gamma_1$ (the braid exchanges the two Majorana
operators up to sign).

*Proof.* $Z^2=X^2=I$ and $ZX=-XZ$ by direct multiplication. $P^2=ZXZX=-ZZXX=-I$.
$(I+P)^2=I+2P+P^2=2P$, so $B^2=P$. $B^{-1}=\frac1{\sqrt2}(I-P)$ since $(I+P)(I-P)=I-P^2=2I$.
Using $P\gamma_1=-\gamma_1P=-\gamma_2$ (as $\gamma_1P=\gamma_1^2\gamma_2=\gamma_2$) and
$P\gamma_2=\gamma_1$, we get
$B\gamma_1B^{-1}=\frac12(I+P)\gamma_1(I-P)=\frac12(\gamma_1+P\gamma_1)(I-P)=\frac12(\gamma_1-\gamma_2)(I-P)$,
and $(\gamma_1-\gamma_2)(I-P)=\gamma_1-\gamma_1P-\gamma_2+\gamma_2P=\gamma_1-\gamma_2-\gamma_2-\gamma_1=-2\gamma_2$,
using $\gamma_2P=\gamma_2\gamma_1\gamma_2=-\gamma_1$. The second identity is the same computation. $\square$

Lean: `lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm212_majorana_clifford_relations`
(the three Clifford relations), `lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm102_110_111_212_syndrome_hamming_lqg_wilson_and_majorana_braid`.
$P^2=-I$ and the braid identities are the computation above.
