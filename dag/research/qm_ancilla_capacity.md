# Sharp purification bounds with limited ancilla capacity

2026-10-11. Written proofs and exact native implementations.
`realizes: null`; `authority_effect: None`; `genesis_effect: None`.

PO-000 [Proposition E.7](../../002_projection_obstruction/000_projection_obstruction/projection_obstruction.md#e7-a-sharp-quantitative-obstruction-from-central-weights)
bounds extension purity by the squared central weights and pure-marginal trace
distance by one minus the largest central weight. Attainment there needs a
sufficiently large available simple ancilla. This note removes that size
assumption and gives the exact answers for a specified finite ancilla algebra.
It also isolates a separate obstruction from restricting joint states to
separable preparations, even when the ancilla dimension is large enough.

## 1. Exact premises and notation

Supply finite complex matrix algebras

$$A=\bigoplus_s M_{n_s}(\mathbb C),\qquad
B=\bigoplus_t M_{m_t}(\mathbb C),\qquad m=\max_t m_t\ge1.$$

Assume the full positive trace-one state spaces, the standard block tensor
product, and admission of all the joint states used below. The trace is the
sum of ordinary matrix traces, not the regular representation trace. A state
on $A$ is $\rho=\bigoplus_s\rho_s$, with $p_s=\operatorname{Tr}\rho_s$ and
$\sum_s p_s=1$. Write its **unnormalized** sector spectra in decreasing order:

$$\lambda_{s,1}\ge\cdots\ge\lambda_{s,n_s}\ge0,\qquad
\sum_i\lambda_{s,i}=p_s.$$

Group consecutive entries into blocks of at most $m$, retaining zeros if
necessary, and set

$$v_{s,j}=\sum_{i=(j-1)m+1}^{\min(jm,n_s)}\lambda_{s,i},\qquad
w=\max_s v_{s,1}. \tag{AC1}$$

Let $\mathcal E_B(\rho)$ be the density states in $A\otimes B$ whose partial
trace is $\rho$. Let $\mathcal P_{A\otimes B}$ be the pure states of that full
algebra and $\mathcal R_B$ their marginals on $A$. In this setting a pure joint
state occupies one pair of central sectors and is a rank-one matrix there.
All minima/maxima below are attained:

$$
\begin{aligned}
\max_{\sigma\in\mathcal E_B(\rho)}\operatorname{Tr}\sigma^2
  &=\sum_{s,j}v_{s,j}^2,\\
\min_{\sigma\in\mathcal E_B(\rho)}\operatorname{rank}\sigma
  &=\sum_s\left\lceil\frac{\operatorname{rank}\rho_s}{m}\right\rceil,\\
\max_{\sigma\in\mathcal E_B(\rho)}\|\sigma\|_\infty &= w,\\
\min_{\eta\in\mathcal R_B}D(\rho,\eta)
  &=\min_{\substack{\sigma\in\mathcal E_B(\rho)\\\pi\in\mathcal P_{A\otimes B}}}
       D(\sigma,\pi)=1-w,
\end{aligned} \tag{AC2}
$$

Here $D(X,Y)=\tfrac12\|X-Y\|_1$ for states and matrix rank is summed over
central blocks. A zero-weight sector contributes zero. In particular, $\rho$
has a pure extension exactly when one system sector has weight one and its
rank is at most $m$.

These are conditional statements about the declared algebras and state cones.
They do not select complex scalars, establish a tensor rule, or certify that a
particular laboratory or native-history process can prepare the attaining state.

## 2. Spectral dominance: the upper bounds

Fix $s$ and diagonalize $\sigma_s=\bigoplus_t\sigma_{st}$ in an eigenbasis
adapted to the ancilla central blocks. Write its decreasing eigenvalues as
$\mu_1,\mu_2,\ldots$, including zeros. Retain the top $k$ eigenvectors with
their eigenvalues, producing $0\le\sigma_s^{(k)}\le\sigma_s$. Partial trace
preserves this order, so

$$0\le a_k:=\operatorname{Tr}_B\sigma_s^{(k)}\le\rho_s,
\qquad\operatorname{Tr}a_k=\sum_{j\le k}\mu_j.$$

Each eigenvector lies in a block $\mathbb C^{n_s}\otimes\mathbb C^{m_t}$.
Its reduced matrix has rank at most $m_t\le m$: its range is contained in
the span of its at most $m_t$ coefficient columns. The range of $a_k$ is
contained in the sum of these ranges, hence has dimension at most $km$.
Let $P$ project onto that range. Positivity and the finite spectral variational
bound give

$$\sum_{j\le k}\mu_j=\operatorname{Tr}(Pa_k)
\le\operatorname{Tr}(P\rho_s)
\le\sum_{i\le\min(km,n_s)}\lambda_{s,i}
=\sum_{j\le k}v_{s,j}. \tag{AC3}$$

For completeness, the variational bound uses no quantum reconstruction axiom.
In an eigenbasis of $\rho_s$, put $q_i=\langle i|P|i\rangle$. Then
$0\le q_i\le1$ and $\sum_iq_i=\operatorname{rank}P$. Moving any weight from
a smaller eigenvalue to an unfilled larger one cannot decrease
$\sum_i\lambda_{s,i}q_i$. Its maximum is the sum of the largest
$\operatorname{rank}P$ eigenvalues, which is at most the displayed sum.

Pad $v_s$ with zeros to the length of $\mu$. Both lists have total mass $p_s$,
and (AC3) says that $v_s$ majorizes $\mu$. Here is the required purity
inequality directly, rather than a computational assertion of it. Let
$d_k=\sum_{j\le k}(v_{s,j}-\mu_j)\ge0$ and $c_j=v_{s,j}+\mu_j$.
The list $c$ decreases and the final prefix difference is zero. Summation by
parts gives

$$\sum_j(v_{s,j}^2-\mu_j^2)
 =\sum_{k=1}^{L-1}d_k(c_k-c_{k+1})\ge0. \tag{AC4}$$

Summing over $s$ proves the purity ceiling. Taking $k=1$ in (AC3) proves the
operator-norm ceiling. If $r_s=\operatorname{rank}\sigma_s$, the same
coefficient-column argument gives $\operatorname{rank}\rho_s\le mr_s$,
which proves the rank lower bound. Degenerate eigenvalues cause no difficulty:
an eigenbasis adapted to the already block-diagonal operator always exists.

## 3. Simultaneous attainment

Choose any ancilla sector $t_*$ with dimension $m$. For each system sector,
choose an orthonormal eigenbasis $|i\rangle_s$ of $\rho_s$. For group $j$ put

$$|u_{s,j}\rangle=
\sum_{a=1}^{\min(m,n_s-(j-1)m)}
\sqrt{\lambda_{s,(j-1)m+a}}\,
|(j-1)m+a\rangle_s\otimes|a\rangle_{t_*}.$$

Set $\sigma_{s,t_*}=\sum_j|u_{s,j}\rangle\langle u_{s,j}|$ and all other
ancilla blocks to zero. Each partial trace is $\rho_s$. Different $j$ have
orthogonal system supports; thus the nonzero eigenvalues of $\sigma_{s,t_*}$
are exactly the positive $v_{s,j}$. This attains all three spectral bounds
in (AC2) at once, including the minimal rank. No separate ancilla sector is
needed for each group or each system sector.

If $m\ge\max_s\operatorname{rank}\rho_s$, every sector has only one positive
group sum, $p_s$. The maximum purity reduces to $\sum_s p_s^2$, exactly
PO-000 E.7. For $m=1$, it reduces to $\operatorname{Tr}\rho^2$.

## 4. Both sharp trace-distance statements

Every $\eta\in\mathcal R_B$ has trace one, is supported in a single system
sector $s$, and has rank at most $m$. If $P$ is its support projection then
the trace-distance variational bound and the same spectral argument yield

$$D(\rho,\eta)\ge\operatorname{Tr}P(\eta-\rho)
=1-\operatorname{Tr}(P\rho)\ge1-v_{s,1}\ge1-w.$$

For a trace-zero Hermitian difference $X$, the variational bound follows from
$X=X_+-X_-$ and $\operatorname{Tr}X_+=\tfrac12\|X\|_1$; it does not assume
that this projector is an operationally available measurement.

Select a maximizing sector and normalize its top-$m$ spectral truncation:
$\eta=\rho_s^{\mathrm{top}\,m}/w$, with zero blocks elsewhere. The retained
eigenvalues of $\rho-\eta$ are nonpositive and total $-(1-w)$; all the others
are nonnegative and total $1-w$. Hence $D(\rho,\eta)=1-w$. Its rank is at most
$m$, and the normalized vector $u_{s,1}/\sqrt w$ above purifies it.

For any joint pure state $\pi=|\psi\rangle\langle\psi|$ and any extension,

$$D(\sigma,\pi)\ge1-\langle\psi|\sigma|\psi\rangle
\ge1-\|\sigma\|_\infty\ge1-w.$$

The attaining extension from §3 has $u_{s,1}/\sqrt w$ as an eigenvector of
eigenvalue $w$; its other eigenvectors are orthogonal. Its distance to that
joint pure state is exactly $1-w$. Thus the two distance minima in (AC2)
agree, although their optimization domains are different.

## 5. Availability of joint states is a separate premise

Hold the same algebras, marginal and ancilla dimensions fixed, but admit only
separable joint states. Then the sharp maximum purity is

$$\max_{\substack{\sigma\text{ separable}\\\operatorname{Tr}_B\sigma=\rho}}
\operatorname{Tr}\sigma^2=\operatorname{Tr}\rho^2. \tag{AC5}$$

Indeed write $\sigma=\sum_a t_a\rho_a\otimes\tau_a$, with normalized positive
factors. Since $0\le\tau_a\le I_B$, we have
$0\le\sigma\le\rho\otimes I_B$. The trace of a product of positive matrices
is nonnegative, so

$$\operatorname{Tr}\sigma^2\le
\operatorname{Tr}\bigl(\sigma(\rho\otimes I_B)\bigr)=\operatorname{Tr}\rho^2.$$

The product $\rho\otimes|b\rangle\langle b|$ attains it for any pure ancilla
state. Pure separable joint states have pure marginals, so their closest
marginal distance is $1-\max_{s,i}\lambda_{s,i}$, irrespective of ancilla size.
This is an explicit state-availability alternative, not a claim to have
specified and certified every part of a rival operational theory.

For $\rho=\operatorname{diag}(9,4,1)/14$ and a two-level ancilla, full joint
states allow maximum purity $85/98$ and pure-marginal distance $1/14$; separable
joint states allow only purity $1/2$ and pure-marginal distance $5/14$. If a
WDP report omits this joint-state availability choice, the two possible purity
answers give a sharp two-model prediction floor $9/49$, and the two distance
answers give floor $1/7$. These are mathematical protected questions; their
operational measurement availability remains a separate premise.

## 6. Six-dimensional, native-history and sign consequences

For $\rho=I_6/6$, the
[projective-history algebras](qm_projective_history_algebra.md) furnish
the following possible *declared ancilla algebras*. Every row has complex
algebra dimension 36; their capacities nevertheless differ:

| Ancilla algebra | Largest simple block $m$ | Maximum extension purity | Minimum extension rank | Distance in (AC2) |
|---|---:|---:|---:|---:|
| $\mathbb C^{36}$ | 1 | $1/6$ | 6 | $5/6$ |
| $\bigoplus_{1}^{9}M_2(\mathbb C)$ | 2 | $1/3$ | 3 | $2/3$ |
| $\bigoplus_{1}^{4}M_3(\mathbb C)$ | 3 | $1/2$ | 2 | $1/2$ |
| $M_6(\mathbb C)$ | 6 | 1 | 1 | 0 |

An equally weighted orthonormal basis mixture, including any one of the checked
MUB6 bases, is $I_6/6$. Thus the table applies after that state and the ancilla
are admitted. It gives no bound on an arbitrary fourth mutually unbiased basis.
The family-limited MUB theorem remains separate from this extension theorem.

For the [native history-cost family](qm_native_history_cost.md), suppose
one additionally chooses $K$ orthogonal quantum labels and their uniform mixture
to encode a finite window. If $K=qm+r$, $0\le r<m$, (AC2) gives

$$P_{\max}=(qm^2+r^2)/K^2,\qquad
D_{\min}=1-\min(m,K)/K.$$

At fixed $m$ the purity ceiling tends to zero and the distance to one as the
declared orthogonal window grows. Native history distinction alone does not
force orthogonality, uniform probabilities, that density state, or this tensor
model. This conditional bridge respects the S(n)/MSS-N rule that a mathematical
realization cannot itself create a native stage or an available ancilla.

Likewise, two classical sign sectors have largest simple block one; merely
retaining an FSP sign label cannot provide the purification capacity of a
coherent two-level matrix ancilla. A declared projective algebra can have such
a matrix block, but an FSP-to-that-algebra map, its positivity and its usable
joint preparations still need proof. No efficient sampling result follows.

The single real-matrix version of the same spectral/Schmidt proof also works
over real Hilbert spaces. These capacity formulas do not discriminate real
from complex quantum theory and do not repair GAP-FQM-021 by dimension counting.

## 7. Native scope and reproduction

[`ancilla_capacity.rs`](../../../../../omega_engine/crates_rs/omega_quantum_physics/src/ancilla_capacity.rs)
uses the existing `RationalSpectrum`, exact operator spectrum, canonical
`BasicMatrix<GaussianRat>` and rational square-root owners. The spectrum-only
route takes validated normalized sector spectra and explicit central weights;
it does not assert a spectrum for a separately held matrix. The matrix-bound
route derives a density's rational eigenvalues and refuses irrational spectra.
The existing full/weighted purification owner remains the owner of those
different constructions; this module addresses fixed ancilla capacity.

The implementation returns exact purity, minimum rank, largest retained mass,
distance and separable-purity values. Its sorted-diagonal attainer requires
every within-group $\sqrt{\lambda_i\lambda_j}$ coefficient to be rational.
Failure refuses that Q(i) recipe, not the complex existence theorem and not
every possible same-field construction. A rotated marginal requires the
corresponding conjugation of the attainer; the tests check this explicitly.
Spectrum expansion and matrix allocation/work budgets fail closed.

Nine focused [native tests](../../../../../omega_engine/crates_rs/tests/omega_quantum_physics/ancilla_capacity.rs)
verify exact partial traces, positivity, purity, extension ranks, nearest
marginals and joint pure-state distance, a non-diagonal marginal, central
attainment, nondividing block sizes, all table rows, product-state controls,
canonical majorization comparison, zero weights and refusal paths. A cross-owner
test constructs all six $\mathbb Z_6^2$ twists, validates their cocycles with the
existing Lie-theory owner, and feeds its complex block profiles into the new
capacity owner; it does not substitute a dimension-compatible guessed algebra.

```console
cd omega_engine/crates_rs
cargo test -j 1 --offline --locked -p omega_quantum_physics --test ancilla_capacity
```

Use the shared target cache when running in a worktree. The
qualification receipt
records exact commands, outputs and source hashes. **AC1–AC5 are written proofs,
not new Lean theorems; finite test cases do not establish their unrestricted
quantifiers.** The finite spectral theorem and the usual matrix tensor/partial
trace structure are mathematical inputs. No F004 publication payload or
historical source archive is changed, and no new paper release is claimed.
