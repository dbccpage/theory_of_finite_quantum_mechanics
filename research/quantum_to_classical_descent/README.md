# Finite quantum-to-classical descent and observer completion

A self-contained research derivation with a standalone exact-arithmetic checker.
The conclusions are relative to the explicitly stated carriers, norms, dynamics,
measurement models, and analytic premises. **AuthorityEffect: None.**

Run from this directory with Python 3.10 or later; no third-party packages are required:

```console
python -I -B check_exact.py
```

The checker rejects `-O` and `-OO`, which would disable its certificate assertions.
The [replay receipt](replay.json) records one executed replay and the source pins.

**Theorem (Finite sufficient records and observer completion).** Exact autonomous records exist when the information discarded by the observer cannot affect any future report. On a full finite linear carrier, the minimum completion is the ordinary invariant row-space closure of the original observer. This algebraic completion does not, by itself, supply jointly sharp measurements, stochastic trajectories, or one realized outcome.

Here are the precise statements, their proofs, and the requested exact certificates.

Throughout, rational linear-algebra data are interpreted on their real extensions. Cochain norms are declared rational polyhedral norms. For quantum operators, $\|D\|_1=\operatorname{tr}|D|$ is the trace norm, and
$$
D_{\rm tr}(\rho,\sigma)=\tfrac12\|\rho-\sigma\|_1.
$$
The trace norm is not treated as polyhedral. Quantum input matrices in the fixtures belong to $\mathbb Q(i)$; continuous-time propagators are interpreted in finite-dimensional complex Hilbert space.

A **classical register** has a finite outcome alphabet and a commutative algebra of readouts. Its **probability distribution** is a point of a simplex. A vector of expectation values is numerical information, but need not itself be a probability distribution or describe jointly sharp observables. A **realized outcome** is one register value; it is different from its distribution.

For an admissible carrier $\mathcal S$, report $p:\mathcal S\to P$, and protected answer $q:\mathcal S\to Y$:

- $p$ is **sufficient for $q$** if equal reports imply equal protected answers.
- Reports are **autonomous** under $T_t$ if maps $F_t$ on $p(\mathcal S)$ satisfy $pT_t=F_tp$ and $F_{t+s}=F_tF_s$.
- A **linear completion** appends scalar linear statistics while retaining the original reports. The minimum below counts such statistics, without imposing a physical sensor menu or measurement-cost model.

The strongest linked conclusions are as follows.

1. **Static sufficiency.**
   $$
   q=\widehat q\,p
   \quad\Longleftrightarrow\quad
   p(x)=p(y)\Longrightarrow q(x)=q(y).
   $$
   The factor $\widehat q$ is unique on $p(\mathcal S)$.

   On $V$, let $B=\operatorname{im}d_0$, $K=\ker Q$, $k=\dim K$, and $h=\dim(B\cap K)$. When $B$ is also the carrier of realizable raw defects,
   $$
   \begin{array}{c|c|c}
   \text{Requirement}&\text{Criterion}&\text{Minimum added scalar rows}\\ \hline
   Qb=0\Rightarrow b=0,\ b\in B&B\cap K=0&h\\
   \operatorname{dist}(Qv,QB)=0\Rightarrow v\in B&K\subseteq B&k-h\\
   \text{Both}&K=0&k
   \end{array}
   $$
   The canonical sequence is
   $$
   0\longrightarrow B\cap K\longrightarrow K
   \longrightarrow(K+B)/B\longrightarrow0.
   $$

2. **Linear dynamical descent.** For $L\in\mathbb Q^{n\times n}$ and $Q\in\mathbb Q^{m\times n}$,
   $$
   \boxed{
   \exists M:\ Qe^{tL}=e^{tM}Q\ \forall t\ge0
   \iff L(\ker Q)\subseteq\ker Q
   \iff \exists M:\ QL=MQ .
   }
   $$
   Here $M$ is uniquely determined on $\operatorname{im}Q$, and is rational in rational coordinates. On failure there is a rational witness
   $$
   Qv=0,\qquad QLv\ne0.
   $$

3. **Minimum autonomous completion.** The unique smallest $L$-invariant row space containing the original reports is
   $$
   \boxed{
   \mathcal O_*=
   \operatorname{span}_{\mathbb Q}
   \{\operatorname{rows}(Q),\operatorname{rows}(QL),\ldots,
   \operatorname{rows}(QL^{n-1})\}.
   }
   $$
   The minimum number of additional unrestricted scalar linear statistics is
   $$
   \boxed{\dim\mathcal O_*-\operatorname{rank}Q.}
   $$
   Rational augmented rows $A$ and a rational $M$ with $AL=MA$ attain it.

   This minimum concerns autonomous evolution of the original reports. If a separate linear answer $Rv$ must also be recoverable, replace $Q$ in the generated row space by $\binom QR$, while subtracting the original $\operatorname{rank}Q$ when counting added rows.

4. **Repair-quotient dynamics.** Dynamics on $V/B$ exist precisely when
   $$
   L(B)\subseteq B.
   $$
   Under this hypothesis,
   $$
   \bar L[v]=[Lv],\qquad
   \bar Q[v]=[Qv]\in\operatorname{im}Q/QB
   $$
   are well defined, and
   $$
   \ker\bar Q=(K+B)/B.
   $$
   Autonomous quotient reports require
   $$
   L(K+B)\subseteq K+B.
   $$
   The same invariant-row-space construction applies on $V/B$, whose dimension is $n-\dim B$. Added scalar functions on this quotient correspond to rows on $V$ annihilating $B$.

5. **Exact closed-system classical autonomy.** Let $P_1,\ldots,P_k$ be nonzero orthogonal projectors summing to $I$, and let
   $$
   p_i(\rho)=\operatorname{tr}(P_i\rho),\qquad U_t=e^{-itH}.
   $$
   If, for every initial density matrix,
   $$
   p(U_t\rho U_t^\dagger)=K_t p(\rho)
   $$
   for a time-homogeneous classical Markov semigroup $K_t$, then
   $$
   \boxed{[H,P_i]=0\quad\text{for every }i,\qquad K_t=I.}
   $$
   Conversely, these commutators vanishing gives stationary autonomous probabilities. Nontrivial exact population dynamics are possible for supplied open-system channels.

6. **Conditional locality bound.** Let $O_j$ be finitely many Hermitian observables with $\|O_j\|_\infty\le1$. Suppose, as an analytic input,
   $$
   \|O_j(T)-O_j^{(r)}(T)\|_\infty
   \le \varepsilon_T,\qquad
   \varepsilon_T=C e^{-\mu(r-v_{\rm LR}T)},
   $$
   where $O_j^{(r)}(T)$ is supported in the declared radius-$r$ neighborhood. If $\rho_0,\rho_1$ agree on every such neighborhood, then
   $$
   \|Q_T(\rho_0)-Q_T(\rho_1)\|_{\ell^\infty}
   \le 2\varepsilon_T,
   \quad
   Q_T(\rho)_j=\operatorname{tr}(\rho O_j(T)).
   $$
   Supply a linear adapter $F$, repair space $B$, and fixed quotient norm, and suppose
   $$
   \delta=\operatorname{dist}(F(\rho_0-\rho_1),B)>0.
   $$
   Every exact reconstruction of $[F\rho]$ from these reports with finite Lipschitz constant $\kappa_T$ satisfies
   $$
   \boxed{
   \kappa_T\ge\frac{\delta}{2C}
   e^{\mu(r-v_{\rm LR}T)}.
   }
   $$
   If the reports coincide exactly, no such reconstruction exists.

   With additive adversarial report errors bounded by $\eta_0,\eta_1$ in the same norm, the two report balls overlap exactly when
   $$
   \boxed{
   \|Q_T(\rho_0)-Q_T(\rho_1)\|_{\ell^\infty}
   \le\eta_0+\eta_1.
   }
   $$
   In particular, equal error bounds $\eta\ge\varepsilon_T$ ensure overlap.

7. **Deterministic-label boundary.** There is no affine map from all density matrices into the vertices of a probability simplex that sends two distinct pointer eigenstates to two distinct vertices. This excludes that particular affine deterministic readout model. It does not exclude stochastic outcomes, conditional updates, or extensions with additional variables.

The static results are existing quotient algebra, and the dynamical completion is standard finite observability. Repository attributions below are pinned to commit `0d55379635a98d0e2895fc5d89251b7205ba571f`, rather than the moving main branch. The static completion theorem is already stated in [WDP §10.6](https://github.com/dbccpage/the_symbol_game/blob/0d55379635a98d0e2895fc5d89251b7205ba571f/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md); the derivation below supplies its interfaces with dynamics, instruments, and the explicit quantum fixtures.

**Proof of static sufficiency and the row counts.** If $q=\widehat q p$, equal reports give equal answers. Conversely, define
$$
\widehat q(z)=q(x)\quad\text{for any }x\text{ with }p(x)=z.
$$
Fiber constancy makes this well defined, and every $z\in p(\mathcal S)$ has a representative, establishing uniqueness there. Values outside the actual report image are unconstrained.

For raw defects, the invisible realizable vectors are exactly $B\cap K$. For repair classes,
$$
Q^{-1}(QB)=B+K,
$$
because $Qv=Qb$ exactly when $v-b\in K$. Thus quotient soundness is $B+K=B$, equivalently $K\subseteq B$.

The map $K\to(K+B)/B$, $k\mapsto[k]$, is surjective and has kernel $B\cap K$, proving the displayed exact sequence.

Write an augmentation as $A=\binom QR$. Its kernel is $K\cap\ker R$. Therefore:

- Raw soundness requires $R|_{B\cap K}$ injective, requiring at least $h$ rows.
- Quotient soundness requires $\ker(R|_K)\subseteq B\cap K$, requiring at least $k-h$ rows.
- Both require $R|_K$ injective, requiring at least $k$ rows.

To attain these bounds, extend a rational basis of $B\cap K$ to one of $K$, then by the remaining directions of $B$, and finally to $V$. Select the corresponding dual coordinates: the first $h$, the next $k-h$, or all first $k$. This also shows that the dimensions are canonical but completion rows require choices.

For fixed sound $A$, the least constants in
$$
\|b\|_V\le C_{\rm raw}\|Ab\|,\qquad
\operatorname{dist}(v,B)
\le C_{\rm quo}\operatorname{dist}(Av,AB)
$$
are finite. Under rational polyhedral norms they are rational: they are operator norms of inverse maps on the relevant images, computed over rational polyhedral unit balls. An invisible nonzero vector makes the corresponding constant infinite. A zero-dimensional recovery domain has constant zero.

These statements must be adjusted to the actual carrier. For example, on $\mathcal S\subset V$, the answer $[v]$ is determined by the raw report $Qv$ exactly when
$$
(\mathcal S-\mathcal S)\cap K\subseteq B.
$$
If the report itself is taken modulo $QB$, replace $K$ by $K+B$.

Likewise, if a physical realization map $D_{\rm phys}$ has image $\mathcal R$, raw soundness is $\mathcal R\cap K=0$. The repair space remains $B=\operatorname{im}d_0$. The displayed “both iff $K=0$” statement assumes $\mathcal R=B$; it cannot be transferred unchanged to two different spaces.

**Proof of dynamical descent.** Suppose $L(K)\subseteq K$. Set
$$
M(Qv)=QLv.
$$
Changing $v$ by $k\in K$ changes $QLv$ by $QLk=0$, so $M$ is well defined. It satisfies $QL=MQ$, hence, by induction,
$$
QL^j=M^jQ.
$$
Summing the convergent finite-matrix exponential series gives $Qe^{tL}=e^{tM}Q$.

Conversely, differentiating this identity at $t=0$ gives $QL=MQ$, which immediately implies $QLk=0$ for $k\in K$.

An exact certificate is a rational kernel-basis matrix $N$ with
$$
QN=0,\qquad \operatorname{rank}N=n-\operatorname{rank}Q,
$$
together with $QLN=0$. If the last equality fails, one column of $N$ is the required rational failure witness.

A matrix-space witness becomes a density-state witness only after checking its type. Let $D\ne0$ be Hermitian and trace zero, with
$$
Q(D)=0,\qquad Q(\mathcal L D)\ne0,
$$
where $\mathcal L$ generates the supplied state-preserving dynamics. Choose a rational $R\ge\|D\|_\infty$, $R>0$, and
$$
0<\epsilon\le\frac1{2dR}.
$$
Then
$$
\rho_\pm=\frac Id\pm\epsilon D
$$
are admissible density matrices, have identical reports, and have different initial report derivatives. A rational bound $R$ can be obtained from the sum of the absolute real and imaginary entry components.

For density matrices the relevant difference space is the Hermitian trace-zero space. An arbitrary ambient matrix direction does not suffice. For nonunital dynamics, expectation equations can be affine; adjoining the known trace coordinate makes them homogeneous linear equations.

**Proof of minimum completion.** Start with
$$
\mathcal O_0=\operatorname{row}(Q),\qquad
\mathcal O_{j+1}=\mathcal O_j+\mathcal O_jL.
$$
If a step does not increase dimension, the space is invariant and all later steps agree. There can be at most $n-\operatorname{rank}Q$ strict increases. Cayley–Hamilton additionally expresses every $L^j$, $j\ge n$, in the span of $I,L,\ldots,L^{n-1}$, giving the stated finite formula.

Every invariant row space containing $Q$ contains $QL^j$ for every $j$, so it contains $\mathcal O_*$. Conversely, $\mathcal O_*$ is invariant by Cayley–Hamilton. This proves uniqueness and minimality.

Choose a rational row basis $A$ of $\mathcal O_*$ extending an independent basis of the original reports. Closure gives $AL=MA$. Explicitly, if $R_A$ is a rational right inverse of this full-row-rank $A$, then
$$
M=ALR_A.
$$
Because every row of $AL$ lies in $\operatorname{row}(A)$, this $M$ satisfies $MA=AL$. Redundant original reports can be retained afterward.

The exact information restored is characterized by
$$
\ker A=\bigcap_{j=0}^{n-1}\ker(QL^j).
$$
This is the largest $L$-invariant subspace contained in $\ker Q$. Directions left in $\ker A$ never influence any future original report. Thus completion need not reconstruct the whole state.

For a protected linear answer $Rv$, sufficiency requires $\operatorname{row}(R)\subseteq\operatorname{row}(A)$. Applying the same argument to $\binom QR$ proves the strengthened count stated above.

These are counts of linear statistics on the declared full carrier. They are not minimum numbers of physical measurements, samples, bits, or units of energy.

**Proof of repair-quotient dynamics.** Since $[b]=[0]$ for every $b\in B$, well-definedness of $[Lv]$ requires $[Lb]=0$. This is exactly $L(B)\subseteq B$, and it is also sufficient. Applying the preceding descent theorem to $\bar L,\bar Q$ gives the quotient criterion.

This prerequisite can fail even when static quotient observation works. On $B=\operatorname{span}(1,1)$, take the additional algebraic test
$$
L=\begin{pmatrix}1&0\\0&2\end{pmatrix}.
$$
Then $L(1,1)=(1,2)\notin B$. The zero repair class would acquire two different derivatives depending on its representative. No dynamics on $V/B$ have been defined.

**Proof of the closed-system classical statement.** Equality of expectations for every density matrix implies the operator identity
$$
U_t^\dagger P_iU_t=\sum_j(K_t)_{ij}P_j.
$$
The left side is a projector. Squaring the right side and using orthogonality gives
$$
(K_t)_{ij}^2=(K_t)_{ij}.
$$
Every coefficient is therefore $0$ or $1$. Since $K_0=I$ and $K_t$ is continuous, every coefficient remains equal to its initial value. Thus $U_t^\dagger P_iU_t=P_i$, and differentiation gives $[H,P_i]=0$.

The projectors being nonzero ensures that every simplex vertex is realizable, using the state $P_j/\operatorname{tr}P_j$. Consequently $K_t$ is determined on the full simplex.

The full-carrier hypothesis matters. With $H=X/2$, $Z$-pointer projectors, and the restricted carrier $\{I/2\}$, probabilities are stationary although $[H,P_i]\ne0$.

More generally, for supplied CPTP maps $\mathcal T_t$, exact closure of these PVM probabilities is equivalent to
$$
\mathcal T_t^\dagger(P_i)\in\operatorname{span}\{P_j\}.
$$
Positivity and unitality make the resulting coefficients a column-stochastic matrix. This permits nontrivial open-system dynamics.

**Proof of the locality and noise statements.** Neighborhood agreement implies
$$
\operatorname{tr}\bigl((\rho_0-\rho_1)O_j^{(r)}(T)\bigr)=0.
$$
Trace/operator-norm duality and $\|\rho_0-\rho_1\|_1\le2$ give
$$
\begin{aligned}
|Q_T(\rho_0)_j-Q_T(\rho_1)_j|
&=\left|\operatorname{tr}\bigl((\rho_0-\rho_1)
[O_j(T)-O_j^{(r)}(T)]\bigr)\right|\\
&\le2\varepsilon_T.
\end{aligned}
$$
If $R_T(Q_T(\rho))=[F\rho]$ is $\kappa_T$-Lipschitz,
$$
\delta
\le\kappa_T\|Q_T(\rho_0)-Q_T(\rho_1)\|_{\ell^\infty}
\le2\kappa_T\varepsilon_T.
$$
This proves the proposed bound. Normalization also gives a report separation at most $2$, so $2\min(1,\varepsilon_T)$ can replace $2\varepsilon_T$.

For $m$ detectors and an $\ell^1$ report norm, the corresponding denominator is $2mC$; for $\ell^2$, it is $2\sqrt m\,C$. The norm choice is essential.

Two norm balls with radii $\eta_0,\eta_1$ intersect iff the distance between their centers is at most $\eta_0+\eta_1$. Necessity is the triangle inequality; sufficiency follows by choosing the appropriately weighted point on the line segment between the centers. The locality estimate supplies a sufficient overlap condition, not a necessary one: reports may coincide even when $\eta<\varepsilon_T$.

For the analytic input, a typical supplied model is a finite subset of a lattice with finite-dimensional sites, finite-range Hamiltonian terms, uniform interaction-strength bounds, and bounded detector support sizes. The actual $C>0,\mu>0,v_{\rm LR}\ge0$ must account for the interaction range, strength, graph growth, and detector supports. Here the displayed approximation estimate is an explicit premise; no numerical values for those constants have been independently certified. This is the standard real-time locality input illustrated by [Bravyi–Hastings–Verstraete](https://arxiv.org/abs/quant-ph/0603121v1).

The conclusion concerns conditioning of a specified detector map. Preparation, encoding, and decoding lower bounds require further hypotheses, as in [König–Pastawski](https://arxiv.org/abs/1310.1037v1). There is no matching example here establishing sharpness. An exponential tail is not zero, and this real-time argument says nothing automatically about imaginary-time Monte Carlo weights.

All allowed joint measurements, feedback, and classical communication must be included before interpreting the bound as a restriction on a protocol. A bound for selected expectation values is not a bound for every measurement transcript.

**Proof of the deterministic-label statement.** Suppose an affine map $f$ sends pointer eigenstates $\rho_0,\rho_1$ to distinct vertices $e_0,e_1$. For $0<\lambda<1$,
$$
f(\lambda\rho_0+(1-\lambda)\rho_1)
=\lambda e_0+(1-\lambda)e_1,
$$
which is not a vertex. This contradicts the proposed codomain. The contradiction concerns affinity, deterministic labels, and the stated convex domain together.

Before applying these results, the retraction calculation needs its own distinction. For $m=\Pi(m)$, finite-dimensional $L$, and a $C^2$ retraction,
$$
e^{tL}m-\Pi(e^{tL}m)
=t(I-D\Pi_m)Lm+O(t^2).
$$
This follows by differentiating the two terms at zero.

For a linear projection $P$, the projected-family defect instead satisfies
$$
\begin{aligned}
S_{t+s}-S_tS_s
&=Pe^{tL}(I-P)e^{sL}\big|_{\operatorname{im}P}\\
&=ts\,PL(I-P)LP\big|_{\operatorname{im}P}
+O(ts(t+s)).
\end{aligned}
$$
Full-carrier observation descent through $P$ requires
$$
PL(I-P)=0.
$$
Normal leakage from the selected image is governed by the different block
$$
(I-P)LP.
$$

For example,
$$
P=\begin{pmatrix}1&0\\0&0\end{pmatrix},\qquad
L=\begin{pmatrix}0&0\\1&0\end{pmatrix}
$$
has nonzero normal leakage from $(1,0)$, but $S_t=I$ on $\operatorname{im}P$. Transposing $L$ gives a projected identity family again, while full-carrier observation descent fails. Testing only chosen representatives therefore does not establish descent.

For completeness, the mixed coefficient for a nonlinear $C^2$ retraction is
$$
S_{t+s}(m)-S_t(S_s(m))
=ts\left(
D\Pi_mL n_\Pi(m)+D^2\Pi_m[n_\Pi(m),Lm]
\right)+o(ts).
$$
It follows by differentiating $S_{t+s}$ and $S_t(S_s(m))$ once in each time variable. Thus normal leakage and semigroup failure are related through additional derivatives, not identical.

For $\Pi_{\rm prod}(\rho)=\rho_A\otimes\rho_B$, differentiating the tensor product gives, on trace-zero directions,
$$
D\Pi_m[Z]
=\operatorname{Tr}_B Z\otimes\rho_B
+\rho_A\otimes\operatorname{Tr}_A Z.
$$
The map $\Pi_{\rm prod}$ is nonlinear and generally nonaffine, so it is not a quantum channel on arbitrary states.

The supplied short-time bound can also be reproduced directly. For an observable supported on $k=1,2$ sites, support counting and $\|[A,B]\|_\infty\le2\|A\|_\infty\|B\|_\infty$ give
$$
\|[H,[H,O]]\|_\infty\le4k(k+1)g^2\|O\|_\infty.
$$
Hence
$$
\|\ddot\rho_{ab}\|_1\le24g^2,\quad
\|\ddot\rho_a\|_1,\|\ddot\rho_b\|_1\le8g^2,\quad
\|\dot\rho_a\|_1,\|\dot\rho_b\|_1\le2g.
$$
For $R_e(t)=\rho_{ab}(t)-\rho_a(t)\otimes\rho_b(t)$,
$$
\|R_e''(t)\|_1\le24g^2+8g^2+8g^2+8g^2=48g^2.
$$
The global product initial condition gives $R_e(0)=0$, $R_e'(0)=n_e$. Integral Taylor remainder yields
$$
\boxed{\|R_e(t)\|_1\ge\nu_et-24g^2t^2.}
$$
For $g>0,\nu_e>0$, this implies $\|R_e(t)\|_1\ge\nu_et/2$ on $0<t\le\nu_e/(48g^2)$. One-local fields contribute through the full $g$; the proof uses no Lieb–Robinson bound. This reproduces the scope and argument of [Paper 000 §5](https://github.com/dbccpage/the_symbol_game/blob/0d55379635a98d0e2895fc5d89251b7205ba571f/omega_engine_atlas/coda_atlas/F004_papers/002_projection_obstruction/000_projection_obstruction/projection_obstruction.md).

The following worked examples complete the finite calculations.

**The Paper 000 carrier.** With zero restrictions,
$$
\Delta(s_a,s_b,s_c)=(-s_a,-s_a),\qquad
d_0=\begin{pmatrix}-1&0&0\\-1&0&0\end{pmatrix}.
$$
Thus
$$
B=\operatorname{span}(1,1),\qquad
\ker d_0=\operatorname{span}\{(0,1,0),(0,0,1)\}.
$$
For $v=(x,y)$,
$$
\Phi(v)=\inf_t(|x-t|+|y-t|)=|x-y|.
$$
The lower bound is the triangle inequality; any $t$ between $x$ and $y$ attains it.

The newly chosen test observers are
$$
Q_+=(1,1),\qquad Q_-=(1,-1).
$$
Their complete comparison is
$$
\begin{array}{c|c|c}
&Q_+&Q_-\\ \hline
K&\operatorname{span}(1,-1)&\operatorname{span}(1,1)\\
QB&\mathbb R&0\\
\Phi_Q(Qv)&0&|x-y|\\
\text{Raw soundness}&\text{yes}&\text{no}\\
\text{Quotient soundness}&\text{no}&\text{yes}\\
\text{Added rows: raw, quotient, both}&(0,1,1)&(1,0,1)\\
C_{\rm raw},C_{\rm quo}&(1,\infty)&(\infty,1)
\end{array}
$$

For the required witnesses,
$$
b=(1,1)=d_0(-1,0,0),\qquad I(b)=2,\qquad\Phi(b)=0,
$$
while
$$
\omega=(1,-1),\qquad \Phi(\omega)=2.
$$
The observer values are
$$
Q_+b=2,\quad Q_-b=0,\qquad Q_+\omega=0,\quad Q_-\omega=2.
$$
Thus $Q_-$ hides a repairable raw defect, while $Q_+$ hides a nonrepairable cochain.

An exact dual certificate for $\omega$ is
$$
y=(1,-1),\qquad d_0^Ty=0,\qquad\|y\|_\infty=1,\qquad y^T\omega=2.
$$
The primal choice $\alpha=0$ has residual norm $2$, establishing optimality.

Every section defect has equal coordinates, so $\omega$ cannot equal $\Delta s$. It is a declared test cochain on the existing carrier.

For the completed observer
$$
A=\begin{pmatrix}1&1\\1&-1\end{pmatrix},
\qquad A^{-1}=\tfrac12A,
$$
use the required stacked $\ell^1$ report norm. For $b_t=(t,t)$,
$$
\|b_t\|_{\ell^1}=2|t|=\|Ab_t\|_{\ell^1}.
$$
Also,
$$
AB=\{(2t,0):t\in\mathbb R\},
\qquad
\operatorname{dist}_{\ell^1}(Av,AB)=|x-y|=\Phi(v).
$$
Consequently,
$$
\boxed{C_{\rm raw}(A)=C_{\rm quo}(A)=1,}
$$
with equality witnesses establishing sharpness.

This also supplies a restricted-carrier control: $Q_+$ is noninjective on $V$, yet determines every vector of the actual raw carrier $B$.

**Hidden coherence and a later record.** Write
$$
\rho=\tfrac12(I+xX+yY+zZ).
$$
For $H=X/2$, the von Neumann equation gives
$$
\dot x=0,\qquad\dot y=-z,\qquad\dot z=y,
$$
so
$$
L=\begin{pmatrix}
0&0&0\\
0&0&-1\\
0&1&0
\end{pmatrix}.
$$
The supplied states are
$$
\rho_\pm=
\begin{pmatrix}
\tfrac12&\mp\tfrac{3i}{10}\\
\pm\tfrac{3i}{10}&\tfrac12
\end{pmatrix}.
$$
Both have eigenvalues $4/5,1/5$, so they are admissible.

For $Q=(0,0,1)$,
$$
Q\rho_\pm=0,\qquad
\frac{d}{dt}\operatorname{tr}(Z\rho_\pm(t))\Big|_{t=0}
=\pm\frac35,
$$
and exactly
$$
\boxed{\operatorname{tr}(Z\rho_\pm(t))=\pm\tfrac35\sin t.}
$$
Their $Y$ expectations are $\pm(3/5)\cos t$.

The closure calculation is
$$
Q=(0,0,1),\quad QL=(0,1,0),\quad QL^2=-Q.
$$
Thus one added row suffices and is necessary:
$$
A=\begin{pmatrix}0&0&1\\0&1&0\end{pmatrix},\qquad
M=\begin{pmatrix}0&1\\-1&0\end{pmatrix},\qquad AL=MA.
$$
The rational failure witness is $v=(0,1,0)^T$, with $Qv=0$, $QLv=1$. The displayed $\rho_\pm$ realize that hidden-coherence direction physically.

For a diagonal initial state with probabilities $p=(p_0,p_1)^T$, evolution followed by $Z$-dephasing gives
$$
K(t)p,\qquad
K(t)=\frac12
\begin{pmatrix}
1+\cos t&1-\cos t\\
1-\cos t&1+\cos t
\end{pmatrix}.
$$
Although every $K(t)$ is stochastic,
$$
K(\pi/2)^2=
\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix},
\qquad
K(\pi)=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
$$
The semigroup law fails. In general it would require
$$
\cos(t+s)=\cos t\cos s,
$$
which misses the term $-\sin t\sin s$.

Dephasing only at the end preserves intermediate coherence until the final operation. Dephasing between steps deletes it and changes the dynamics. With a fixed step $\tau$, repeated dephasing produces the discrete stochastic chain $K(\tau)^n$, whose population difference is multiplied by $(\cos\tau)^n$. These are different protocols.

The completed expectation coordinates $(z,y)$ evolve autonomously, but
$$
[Y,Z]=2iX\ne0.
$$
They are not jointly sharp observables. Their possible values form the disk $y^2+z^2\le1$, not a simplex. Their expectations can be estimated through additional measurement arrangements on ensembles; that is not exact knowledge of a single unknown system.

For a sensor menu restricted to current-time observables in $\operatorname{span}\{I,Z\}$, with no additional controls, the required $Y$ row is unavailable. Repeating or recombining those rows cannot supply it. Allowing rotations or other protocols changes the sensor menu and requires a new attainability analysis.

Conversely, on the restricted carrier of diagonal qubit states, $z$ determines the entire state:
$$
\rho=\operatorname{diag}\bigl((1+z)/2,(1-z)/2\bigr).
$$
This observer is sufficient there despite its ambient coherence kernel.

**The open-system positive control.** For
$$
\rho=\begin{pmatrix}a&c\\c^*&d\end{pmatrix},
\qquad a+d=1,
$$
substitution into the supplied generator with $\alpha=1,\beta=2$ gives
$$
\mathcal L(\rho)=
\begin{pmatrix}
d-2a&-\tfrac32c\\
-\tfrac32c^*&2a-d
\end{pmatrix}.
$$
Therefore
$$
\boxed{
\frac d{dt}\binom{p_0}{p_1}
=
G\binom{p_0}{p_1},
\qquad
G=\begin{pmatrix}-2&1\\2&-1\end{pmatrix}.
}
$$
This holds for every initial density matrix, including coherent ones.

Let
$$
\pi=\binom{1/3}{2/3},\qquad
\Pi=\begin{pmatrix}1/3&1/3\\2/3&2/3\end{pmatrix}.
$$
Then
$$
G=-3(I-\Pi),\qquad
e^{tG}=\Pi+e^{-3t}(I-\Pi)
=e^{-3t}I+(1-e^{-3t})\Pi.
$$
This is a nontrivial stochastic semigroup. Coherences decay as $e^{-3t/2}$.

The supplied physical assumptions are a reduced qubit, continuous time, a time-homogeneous memoryless CPTP model with the displayed positive Lindblad rates, and Born probability readout. No microscopic reservoir derivation is being inferred from cochain algebra. The master equation specifies ensemble evolution. A monitored jump instrument, another unravelling, or a realized trajectory requires additional specification.

**The three-qubit measurement fixture.** Order the computational basis as $000,001,\ldots,111$, and apply the rightmost gate first. Then
$$
U|s,a,e\rangle=|s,a\oplus s,e\oplus a\oplus s\rangle.
$$
An explicit matrix specification is the permutation
$$
Ue_j=e_{f(j)},\qquad
f=(0,1,3,2,7,6,4,5).
$$
It immediately gives $U^\dagger U=I_8$.

The final state is
$$
|\Psi\rangle=\frac35|000\rangle+\frac45|111\rangle.
$$
Its density matrix has exactly four nonzero entries:
$$
\rho_{0,0}=\frac9{25},\quad
\rho_{7,7}=\frac{16}{25},\quad
\rho_{0,7}=\rho_{7,0}=\frac{12}{25}.
$$
It is positive because $\rho=|\Psi\rangle\langle\Psi|$, and has trace one.

The apparatus pointer projectors are
$$
J_i=I_S\otimes|i\rangle\langle i|_A\otimes I_E.
$$
The global pointer instrument is
$$
\mathcal J_i(\tau)=J_i\tau J_i,\qquad
\sum_iJ_i^\dagger J_i=I_8.
$$
Equivalently, from the initially prepared system to the three-qubit output, the outcome Kraus operators are
$$
K_0=|000\rangle\langle0|,\qquad
K_1=|111\rangle\langle1|,
\qquad
K_0^\dagger K_0+K_1^\dagger K_1=I_2.
$$
The induced system instrument is $\eta\mapsto P_i\eta P_i$.

Born readout now gives
$$
\boxed{p_0=9/25,\qquad p_1=16/25.}
$$
The reduced state is
$$
\rho_{SA}
=\frac9{25}|00\rangle\langle00|
+\frac{16}{25}|11\rangle\langle11|.
$$
Conditional on a supplied outcome $i$, the normalized global state is $|iii\rangle\langle iii|$. Since
$$
\mathcal J_j\mathcal J_i=\delta_{ij}\mathcal J_i,
$$
immediate repetition of this specified measurement returns the same label with probability one.

Now compare with
$$
\sigma=\frac9{25}|000\rangle\langle000|
+\frac{16}{25}|111\rangle\langle111|.
$$
For every proper subsystem, the reductions agree:

- On each of $S,A,E$, both reduce to $\operatorname{diag}(9/25,16/25)$.
- On each of $SA,SE,AE$, both reduce to
  $$
  \operatorname{diag}(9/25,0,0,16/25).
  $$
- On the empty subsystem, both have trace one.

Indeed, tracing out any qubit kills $|000\rangle\langle111|$, because $\langle1|0\rangle=0$.

Globally,
$$
\operatorname{tr}(\rho\,X\otimes X\otimes X)=\frac{24}{25},
\qquad
\operatorname{tr}(\sigma\,X\otimes X\otimes X)=0.
$$
The difference has nonzero eigenvalues $12/25,-12/25$, so
$$
\boxed{D_{\rm tr}(\rho,\sigma)=12/25.}
$$

Put $p=9/25$, $q=16/25$. The product of the $S,A$ marginals is
$$
\rho_S\otimes\rho_A=\operatorname{diag}(p^2,pq,pq,q^2),
$$
and hence
$$
\rho_{SA}-\rho_S\otimes\rho_A
=pq\,\operatorname{diag}(1,-1,-1,1).
$$
Therefore
$$
\boxed{
\|\rho_{SA}-\rho_S\otimes\rho_A\|_1
=4pq=\frac{576}{625}.
}
$$
The associated trace distance is $288/625$.

This positive residual occurs in a diagonal, explicitly separable state. It measures departure from a product, which includes ordinary classical correlation. It is not an entanglement or general “quantumness” certificate.

If a cochain presentation of this particular residual is desired, declare
$$
F_{\rm diag}(Z)=(Z_{00,00},Z_{01,01},Z_{10,10},Z_{11,11}),
\quad V=\mathbb R^4,\quad C^0=0,\quad B=0,
$$
with coordinate $\ell^1$. On this diagonal residual the adapter preserves the computed trace norm. Its only admitted repair is zero. No such norm equality is asserted for arbitrary nondiagonal operators.

The fixture establishes record probabilities and correlations. Persistence requires subsequent dynamics that preserve the pointer sectors—for example $[H_{\rm after},J_i]=0$, or a channel satisfying $\mathcal T^\dagger(J_i)=J_i$. Immediate repeatability alone supplies no persistence theorem under arbitrary later dynamics.

The four operations remain distinct:

- Tracing out $E$ produces a reduced state on $SA$.
- Nonselective pointer dephasing produces $\sigma$ on the full three-qubit space.
- Conditioning on an already supplied $i$ produces a normalized branch.
- Producing one $i$ requires a stochastic or ontological outcome rule.

The Born rule entered when the trace weights were interpreted as probabilities. Neither the unitary computation nor partial trace derived that interpretation.

A concrete stochastic completion adjoins $\lambda$, uniformly distributed on $[0,1]$, sets $i=0$ when $\lambda<9/25$, and applies the corresponding conditional update. A description retaining the unitary state and treating the same weights as branch-relative record weights gives the same displayed pointer statistics without adding that sampled actual-label variable. The supplied finite equations do not choose between those descriptions. Predictions for additional coherent access to an enlarged apparatus require the corresponding dynamics and accessible observables to be specified.

There is also a precise missing-premise formulation: the density matrix and instrument assign probabilities and conditional states, but the premises contain no axiom identifying one ontically actual label. The affine-to-vertices contradiction shows why that missing axiom cannot be replaced by an affine deterministic function of the density matrix alone.

For the locality theorem, an explicit alternative adapter is
$$
F(Z)=\operatorname{tr}(Z\,XXX),\qquad V=\mathbb R,\quad B=0.
$$
For $\rho,\sigma$, its protected separation is $\delta=24/25$, while all proper-subsystem observations coincide at $T=0$. However, local $X$ measurements followed by aggregation of their joint parity can access $XXX$. Thus equal individual or proper-subsystem reports do not imply equality of every allowed distributed transcript.

**The Bell fixture.** Write
$$
v=(1,0,0,1)^T,\qquad \rho_{\Phi^+}=\tfrac12vv^T.
$$
This is positive and trace one, with rational entries.

Because $XZ+ZX=0$,
$$
B_0^2=B_1^2
=\frac{16Z^2+9X^2}{25}=I.
$$
Also $A_0^2=A_1^2=I$. Thus all four observables have outcomes $\pm1$.

The Bell state has zero one-party expectations and
$$
\langle Z\otimes Z\rangle=\langle X\otimes X\rangle=1,\qquad
\langle Z\otimes X\rangle=\langle X\otimes Z\rangle=0.
$$
Consequently,
$$
(E_{00},E_{01},E_{10},E_{11})
=\left(\frac45,\frac45,\frac35,-\frac35\right),
$$
and
$$
p(a,b|x,y)=\frac14(1+abE_{xy}).
$$

In outcome order $++,+-,-+,--$, all four tables are
$$
\begin{array}{c|cccc}
(x,y)&++&+-&-+&--\\ \hline
(0,0)&9/20&1/20&1/20&9/20\\
(0,1)&9/20&1/20&1/20&9/20\\
(1,0)&2/5&1/10&1/10&2/5\\
(1,1)&1/10&2/5&2/5&1/10
\end{array}
$$
Every entry is positive, every row sums to one, and both parties’ marginals are $1/2,1/2$ in every context. Nevertheless,
$$
\boxed{S=E_{00}+E_{01}+E_{10}-E_{11}=14/5.}
$$

Let $\lambda=(a_0,a_1,b_0,b_1)\in\{\pm1\}^4$. Define the $16\times16$ marginal map
$$
\mathsf M_{(x,y,a,b),\lambda}
=\mathbf1\{a=a_x,\ b=b_y\}.
$$
A joint classical extension would be $w\ge0$ with
$$
\mathsf Mw=p.
$$
Its normalization follows by summing any one context.

Here is an explicit rational dual certificate. Set
$$
c_{00}=c_{01}=c_{10}=1,\qquad c_{11}=-1,
$$
and
$$
y_{xyab}=\frac12-c_{xy}ab.
$$
For every assignment,
$$
(\mathsf M^Ty)_\lambda
=2-\bigl[a_0(b_0+b_1)+a_1(b_0-b_1)\bigr]\in\{0,4\},
$$
since exactly one of $b_0+b_1,b_0-b_1$ vanishes and the other is $\pm2$. Thus $\mathsf M^Ty\ge0$. But
$$
y^Tp=2-S=-\frac45.
$$
If a nonnegative $w$ existed,
$$
-\frac45=y^Tp=y^T\mathsf Mw=(\mathsf M^Ty)^Tw\ge0,
$$
a contradiction.

The distinction from ordinary linear inconsistency is explicit. There is a signed joint extension:
$$
w_\lambda=\frac1{16}\left(
1+\frac45a_0b_0+\frac45a_0b_1
+\frac35a_1b_0-\frac35a_1b_1
\right).
$$
Summing over unused signs reproduces all four tables. Its minimum entry is $-3/80$. The obstruction is positivity-constrained marginal extension.

A Bell-local model supplies a setting-independent distribution of $\lambda$ and local response factorization
$$
p(a,b|x,y,\lambda)=p_A(a|x,\lambda)p_B(b|y,\lambda).
$$
Local stochastic responses can be made deterministic by adjoining local random seeds, producing the joint-assignment model above. Setting independence and local response dependence are therefore substantive premises. Compatible marginals alone do not supply them.

Each context has classical outcome records. Those records do not furnish a single nonnegative joint assignment to all four incompatible settings. Projection vocabulary does not remove this obstruction. No identification with an ordinary cochain exactness problem is made here.

The remaining carriers give short, explicit corollaries and boundaries.

For **FSP**, fix a configuration graph and
$$
(d_0g)_{uv}=g_u+g_v\quad\text{over }\mathbb F_2.
$$
Then
$$
\epsilon=d_0g
\quad\Longleftrightarrow\quad
\sum_{e\in C}\epsilon_e=0
\quad\text{for every cycle }C.
$$
Necessity follows because vertex values occur twice around a cycle. For sufficiency, choose a spanning forest, fix each root value, and propagate $g$ along tree edges. Every remaining edge agrees precisely when its fundamental-cycle parity vanishes.

For the stated star loop, additionally declare the usual CAR occupation basis ordered $0<1<2<3$, and hopping
$$
H=-\sum_{j=1}^3(c_0^\dagger c_j+c_j^\dagger c_0).
$$
The transfer signs of $-H$ along
$$
12\to02\to23\to03\to13\to01\to12
$$
have parity bits
$$
(0,1,0,0,1,1).
$$
Their sum is odd. The sign of a hop is $(-1)^N$, where $N$ is the number of occupied sites strictly between the two hopping sites in the declared ordering. Thus this sign-removal family fails.

The physical star is a tree, while its two-particle configuration graph has the displayed cycle. These are different graphs. General orbital transformations and meron regroupings are different transformation families. A cancelling pair with weights $+1,-1$ contributes zero to the partition sum but, for observable values $+1,-1$, contributes $2$ to its numerator. Partition preservation therefore does not imply observable preservation, and neither identity establishes efficient sampling. These are the scoped distinctions in the pinned [FSP §§13–16](https://github.com/dbccpage/the_symbol_game/blob/0d55379635a98d0e2895fc5d89251b7205ba571f/omega_engine_projects/fsp/the_problem_of_the_fermion_sign.md).

For **binary parity correction**, assume a finite complex with $d_1d_0=0$, put $Q=d_1$, $B=\operatorname{im}d_0$, and allow arbitrary additive corrections $c(s)$ indexed by syndrome. Success means
$$
e-c(Qe)\in B\qquad(e\in\mathcal E).
$$
Then exactly
$$
\boxed{
\exists c\text{ successful on }\mathcal E
\iff
(\mathcal E-\mathcal E)\cap\ker Q\subseteq B.
}
$$
If a decoder succeeds, two admitted errors with the same syndrome differ by two elements of $B$, hence by an element of $B$. Conversely, choose one admitted representative $e_s$ for each occurring syndrome and set $c(s)=e_s$. The condition makes every residual repairable.

A concrete example is
$$
V=\mathbb F_2^3,\qquad
d_0=\begin{pmatrix}1\\1\\0\end{pmatrix},\qquad
Q=(1,1,0).
$$
Here $\ker Q/B$ is one-dimensional, represented by $(0,0,1)$. The error set
$$
\mathcal E=\{0,(1,0,0)\}
$$
is correctable because its two syndromes differ. Replacing the second error by $(0,0,1)$ makes correction fail: the same syndrome hides a logical difference.

Thus nonzero $\ker d_1/B$ can carry logical information; detectable nontrivial errors can still be correctable. Requiring correction of every ambient error forces $\ker Q\subseteq B$, and, with $B\subseteq\ker Q$, eliminates that logical quotient.

The binary statement presupposes the admitted correction family. A physical quantum realization needs its own encoding, error, and recovery maps. The standard quantum comparison is the Knill–Laflamme condition
$$
P E_a^\dagger E_bP=c_{ab}P
$$
for a declared code projector and error family; it is not derived merely by naming a binary quotient. [Knill–Laflamme](https://arxiv.org/pdf/quant-ph/9604034v1)

Two hostile controls are necessary for physical error claims. If
$$
0\le E(T)\le U(T)=\frac14(T+T^{-1}),\qquad T>0,
$$
then
$$
U(T)-\frac12=\frac{(T-1)^2}{4T}\ge0,
$$
so $\min U=1/2$, while $E(T)\equiv0$ satisfies every inequality. A positive minimum of an upper budget gives no positive lower bound on actual error.

More specifically, the displayed lower estimate in the pinned [Majorana §8.1](https://github.com/dbccpage/the_symbol_game/blob/0d55379635a98d0e2895fc5d89251b7205ba571f/omega_engine_projects/ms_majorana/the_majorana_problem.md),
$$
\ell(T)=\max\!\left(0,\tfrac12(1-e^{-\Gamma T})-\frac{a}{2T^2}\right),
$$
vanishes for sufficiently small $T$. Taking $E(T)=\ell(T)$ satisfies both that lower estimate and its displayed upper estimate, but has infimum zero. The asserted positive uniform infimum does not follow from those estimates alone.

Also, every density-state trace distance is at most one. A proposed unrestricted lower bound
$$
D_{\rm tr}\ge a/T^2+bT^p
$$
fails whenever its right side exceeds one—for example $a=b=p=1,T=1$. Such a statement requires a justified restricted domain and an actual lower-bound derivation. Neither control decides hardware viability.

For **MUB6**, orient a cyclic triangle $0\to1\to2\to0$:
$$
d_0=
\begin{pmatrix}
-1&1&0\\
0&-1&1\\
1&0&-1
\end{pmatrix}.
$$
With $\omega=0$ and $\alpha=(0,1,0)$,
$$
d_0\alpha=(1,-1,0),\qquad
\omega-d_0\alpha=(-1,1,0).
$$
Its signed circulation is zero and its raw $\ell^1$ norm is $2$, while
$$
\Phi(\omega)=0
$$
by choosing the zero repair. A nonoptimal positive residual is an upper bound on the minimum, not a positive lower bound.

In fact, on this triangle,
$$
\Phi(v)=|v_1+v_2+v_3|.
$$
The cycle sum gives the dual lower bound; moving all residual mass to one edge attains it.

None of these linear identities supplies a nonlinear basis-extension certificate. Such a certificate must impose orthonormality and
$$
|\langle u_a^{(r)},u_b^{(s)}\rangle|^2=\frac16
$$
for every required pair of distinct bases. A regional exclusion becomes global only after a valid coverage and representation argument. The pinned [MUB6 synthesis](https://github.com/dbccpage/the_symbol_game/blob/0d55379635a98d0e2895fc5d89251b7205ba571f/omega_engine_projects/mub6/research/mub6_frontier_synthesis.md) explicitly retains that certification boundary.

**Certificate specification and replay.** The following data make the conclusions checkable without trusting a solver verdict.

| Certificate | Required inputs and independent checks |
|---|---|
| Cochain presentation | Field, coordinates, $d_0$, $Q$, norms, image/kernel bases; verify matrix identities and ranks. |
| Repairability | Supply $\alpha$ and check $v=d_0\alpha$. |
| Nonrepairability | Supply $y$ with $d_0^Ty=0$ and $y^Tv\ne0$. |
| Exact $\ell^1$ distance | Supply $\alpha,u,y$ with $-u\le v-d_0\alpha\le u$, $u\ge0$, $d_0^Ty=0$, $\|y\|_\infty\le1$, and $\sum u_i=y^Tv$. |
| Static completion | Supply added rows, augmented kernel checks, and the dimensions $h,k-h,k$ furnishing lower bounds. |
| Dynamic closure | Check $AL=MA$; replay row-space generation, or show both invariance/containment and that every row of $A$ is generated by $QL^j$, $j<n$. |
| Dynamic failure | Check $Qv=0,\ QLv\ne0$; for quantum use, also certify admissible density states realizing the direction. |
| Quantum fixture | Check Hermiticity, positivity, trace, unitary and Kraus completeness identities, partial traces, and explicit spectral or distinguishing-observable calculations. |
| Bell obstruction | Supply the tables, marginal matrix $\mathsf M$, and $y$ with $\mathsf M^Ty\ge0,\ y^Tp<0$. |
| Locality bridge | Supply geometry, dynamics, supports, $C,\mu,v_{\rm LR},r,T$, the assumed approximation estimate, adapter, repairs, and norms. Label the analytic estimate as supplied unless independently established. |

The distance certificate is sound directly: for every repair $\beta$,
$$
y^Tv=y^T(v-d_0\beta)
\le\|v-d_0\beta\|_{\ell^1}.
$$
A feasible primal vector with the same value attains this lower bound. Checking a matching pair does not require trusting an optimizer or invoking its success flag.

The standalone [exact checker](check_exact.py) was replayed with Python 3.12.14. It uses only the standard library, implements rational and Gaussian-rational arithmetic, and contains its inputs explicitly. It has no repository dependencies and refuses execution with assertions disabled.

The final execution exited **0** and checked:

- Cochain witnesses, ranks, observer values, and completion identities.
- The Bloch generator, failure witness, closure ranks $1,2,2$, and dephasing counterexample.
- The Lindblad population generator on a full matrix basis.
- The measurement unitary and instrument identities, positivity, every proper reduction, and both requested norm calculations.
- All Bell tables and the exact dual witness, including the signed extension.
- The triangle, binary-correction controls, and odd configuration-loop parity.

The [replay receipt](replay.json) records the portable command, output, checker and derivation SHA-256 digests, source commit, and source-file hashes. The source hashes bind the historical Git blobs; the checker itself needs no repository.

The general statements are established by the written proofs above; the program checks their displayed finite instances. No repository-wide test suite or Lean compilation was run. The outcome argument above is self-contained.

The requested adversarial controls have explicit witnesses:

| Control | Witness or result |
|---|---|
| Noninjective but sufficient on the actual carrier | $Q_+$ on $B$, or $Z$ expectation on diagonal qubit states |
| Invisible repairable versus nonrepairable vectors | $Q_-b=0$ versus $Q_+\omega=0$ |
| Positive residual in a classical correlated state | $\rho_{SA}$, residual $576/625$ |
| Same present, different future report | $\rho_\pm$, future values $\pm(3/5)\sin t$ |
| Autonomous coordinates without joint sharpness | $(z,y)$, with $[Y,Z]\ne0$ |
| Local mixture versus coherent global state | $\rho,\sigma$, all proper reductions equal, $XXX$ different |
| Positive minimum upper budget without actual lower bound | $E=0,\ U=(T+T^{-1})/4$ |
| Proposed trace-distance lower bound above one | $a/T^2+bT^p=2$ at the displayed parameters |
| Positive contextual probabilities without a joint extension | Bell dual objective $-4/5$ |
| Algebraic completion outside the sensor menu | Required $Y$ row absent from $\operatorname{span}\{I,Z\}$ |

The claim classifications are:

| Conclusion | Status |
|---|---|
| Static fiber criterion, exact sequence, and three minimum row counts | **Established here**, reproducing existing finite algebra |
| Kernel invariance, $QL=MQ$, and exponential descent equivalence | **Established here** |
| Canonical invariant row space and minimum autonomous completion | **Established here**, standard observability construction |
| Repair-quotient dynamics require $L(B)\subseteq B$ | **Established here** |
| Full-carrier finite unitary PVM autonomy forces stationary probabilities | **Established here** |
| Specified Lindblad model has exact nontrivial classical population dynamics | **Established here**; its use as a device model is **conditional on a stated physical premise** |
| Hilbert space, tensor composition, instruments, Born readout, and continuous time | **Standard imported structures/results** |
| Paper 000’s short-time raw correlation estimate | **Established here under its stated Hamiltonian hypotheses** |
| Positive product residual necessarily means entanglement or failed computation | **Refuted** |
| The Bell tables admit a nonnegative joint assignment | **Refuted** |
| Affine density-state readout can always return a distinct deterministic pointer label | **Refuted** |
| Locality reconstruction and noise-overlap bounds | **Established here conditional on the supplied analytic estimate** |
| A positive minimum of an upper error budget bounds actual error below | **Refuted** |
| These premises select one outcome ontology | **Not decided** |
| These finite certificates establish quantum-computing viability or nonviability | **Not decided** |

These results establish when declared records retain a protected answer, when their dynamics close, and exactly how many unrestricted linear statistics restore closure. They also establish that classical record distributions can coexist with hidden coherence, ordinary classical correlations, and Bell-contextual probabilities. The outcome problem remains at the step from a distribution and conditional instrument to one actual event; that step requires an additional premise. A quantum-computing viability claim would require a specified computational task, physical noise and control model, attainable measurements and corrections, resource bounds, and validated logical performance meeting the hypotheses of an applicable fault-tolerance result such as [Aharonov–Ben-Or](https://arxiv.org/abs/quant-ph/9906129v1). None of the finite certificates here supplies that evidence or authorizes an action.
