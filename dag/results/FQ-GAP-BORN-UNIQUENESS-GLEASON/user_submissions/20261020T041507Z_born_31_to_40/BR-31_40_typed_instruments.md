> REVIEWED DERIVATIVE. Original preserved in submission/. Written proof review and exact fixtures are separate from pending Lean verification. See review.md and corrections.md for the complete disposition.

# BR-31 – BR-40 — Typed instruments: branch states, Choi/effect duality, merge compatibility, carriers, PSD certification, qubit admission, Choi-level operad, padded unitary equivalence, parallel composition, rational dilation

Submission for `FQ-GAP-BORN-UNIQUENESS-GLEASON`, Born/tomography series (continues BR-21–BR-30; uses CC-21–CC-30 and their recorded corrections).
Exact-check script: `br31_40_checks.py` (sympy; 86 fixture checks, all pass; the PSD oracle used throughout is the BR-35 algorithm itself, with every certificate and witness re-verified).

## Standing conventions

- $K=\mathbb Q(i)$; $^*$ is conjugate transpose; dimensions are positive integers; "PSD" is over $\mathbb C$.
- Carriers are kept distinct: rational probes, instruments and Choi matrices live in $K$; probabilities live in $[0,1]\subset\mathbb R$; states live in $\{\rho\in\mathrm{Herm}_d(\mathbb C):\rho\succeq0,\ \mathrm{Tr}\rho=1\}$. Rationality of a state or probability is a property, never an assumption, unless stated.
- $E_{jk}=e_je_k^*$; $S_{jk}=E_{jk}+E_{kj}$, $T_{jk}=i(E_{jk}-E_{kj})$, $G_{jk}=\tfrac12(I+S_{jk})$, $H_{jk}=\tfrac12(I+T_{jk})$ (BR-21).
- Instruments as in BR-26: profile $(e_1,\dots,e_m;d)$, slot families $\{K_{i,a}\}_{a\in A_i}\subset K^{e_i\times d}$, $\sum_{i,a}K_{i,a}^*K_{i,a}=I_d$; $\Phi_i(X)=\sum_aK_{i,a}XK_{i,a}^*$; effect $A_i=\Phi_i^*(I)=\sum_aK_{i,a}^*K_{i,a}$.
- Input-first vectorization (BR-29): $\mathrm{vec}(X)=\sum_je_j\otimes Xe_j\in K^d\otimes K^e$; $C_\Phi=\sum_{jk}E_{jk}\otimes\Phi(E_{jk})$, so $C_\Phi[(j,a),(k,b)]=\Phi(E_{jk})_{ab}$ with row index $j\cdot e+a$. $\mathrm{Tr}_{\mathrm{out}}$ is the partial trace over the second (output) factor.
- Hilbert–Schmidt adjoint: $\mathrm{Tr}(\Phi(X)^*Y)=\mathrm{Tr}(X^*\Phi^*(Y))$; for Kraus maps $\Phi^*(Y)=\sum K^*YK$.
- Block embeddings: for $E=\sum_ie_i$, $J_i:K^{e_i}\to K^E$ is the $i$-th block injection, $J_i^*J_j=\delta_{ij}I$, $\sum_iJ_iJ_i^*=I_E$.

---

## BR-31 — Typed branch-state semantics

**Assumptions / domains.** Instrument $\mathcal K$ with profile $(e_1..e_m;d)$; $\rho$ a density on $\mathbb C^d$.

**Output state.** $\sigma_i:=\Phi_i(\rho)=\sum_{a\in A_i}K_{i,a}\rho K_{i,a}^*\in\mathrm{Herm}_{e_i}(\mathbb C)$. The output is the *tuple* $(\sigma_i)_{i=1}^m$, one matrix per slot, each in its own dimension.

*Positivity.* Each term is a congruence $K\rho K^*$ of $\rho\succeq0$ ($v^*K\rho K^*v=(K^*v)^*\rho(K^*v)\ge0$); PSD matrices of equal size add.
*Normalization.* $\sum_i\mathrm{Tr}\sigma_i=\mathrm{Tr}\big(\rho\sum_{i,a}K_{i,a}^*K_{i,a}\big)=\mathrm{Tr}\rho=1$. Each $\mathrm{Tr}\sigma_i=\mathrm{Tr}(\rho A_i)\ge0$ is a scalar; the tuple is never summed across slots. $\square$

**Tagged direct-sum embedding.** $\Sigma_{\mathcal K}(\rho):=\sum_iJ_i\sigma_iJ_i^*=\bigoplus_i\sigma_i\in M_E(\mathbb C)$, $E=\sum_ie_i$.
- $\Sigma\succeq0$ (sum of congruences), $\mathrm{Tr}\Sigma=\sum_i\mathrm{Tr}\sigma_i=1$: a density on $\mathbb C^E$.
- It is the output of the CPTP map $\Phi_\oplus(X)=\sum_iJ_i\Phi_i(X)J_i^*$ with Kraus family $\{J_iK_{i,a}\}$: $\sum(J_iK)^*(J_iK)=\sum K^*J_i^*J_iK=\sum K^*K=I_d$.
- The tag is recoverable: $\sigma_i=J_i^*\Sigma J_i$; the block projector $P_i=J_iJ_i^*$ gives the scalar marginal $p(i)=\mathrm{Tr}(\Sigma P_i)=\mathrm{Tr}\sigma_i$.
- Off-diagonal blocks $J_i^*\Sigma J_j$ ($i\ne j$) are zero by construction: the direct sum is an *incoherent* tag. This is the semantics; a coherent superposition of branches is a different object (the dilation of BR-40 before discarding the pointer).

**Nested instruments act by typed component maps.** Let $\mathcal L\in\mathrm{Ins}(g_1..g_n;e_i)$, $\Psi_l$ its slot maps, and $\mathcal K\circ_i\mathcal L$ with profile $(e_1..e_{i-1},g_1..g_n,e_{i+1}..e_m;d)$, $E'=E-e_i+\sum_lg_l$, injections $J'_j$ ($j\ne i$), $J'_{(i,l)}$. Define $\Lambda:M_E\to M_{E'}$,
$$\Lambda(Y)=\sum_{j\ne i}J'_j\,(J_j^*YJ_j)\,J_j'^*+\sum_lJ'_{(i,l)}\,\Psi_l(J_i^*YJ_i)\,J'^{*}_{(i,l)} .$$
$\Lambda$ has Kraus family $\{J'_jJ_j^*\}_{j\ne i}\cup\{J'_{(i,l)}L_{l,b}J_i^*\}_{l,b}$ and is TP: $\sum_{j\ne i}J_jJ_j^*+J_i(\sum_{l,b}L^*L)J_i^*=\sum_jJ_jJ_j^*=I_E$. Then
$$\Sigma_{\mathcal K\circ_i\mathcal L}(\rho)=\Lambda\big(\Sigma_{\mathcal K}(\rho)\big),$$
because block $(i,l)$ of the left side is $\sum_{a,b}L_{l,b}K_{i,a}\rho K_{i,a}^*L_{l,b}^*=\Psi_l(\sigma_i)$ (BR-28) and blocks $j\ne i$ are $\sigma_j$ (verified on an example). So the continuation acts on the tagged state by the identity on untouched blocks and by the typed map $\Psi_\oplus=\sum_lJ'_{(i,l)}\Psi_l(\cdot)J'^*_{(i,l)}$ on block $i$. $\square$

**Scalar marginals.** $p(i,l)=\mathrm{Tr}\,\Psi_l(\sigma_i)$; $\sum_lp(i,l)=\mathrm{Tr}\,\Psi(\sigma_i)=\mathrm{Tr}\sigma_i=p(i)$ since $\Psi=\sum_l\Psi_l$ is TP. Only scalars are summed; matrices of different sizes never are.

**Trace zero.** $\sigma_i\succeq0$, $\mathrm{Tr}\sigma_i=0\Rightarrow\sigma_i=0$ (Lemma Z). The zero block is retained in $\Sigma$ (it still occupies $e_i$ rows). Conditional normalization $\hat\sigma_i=\sigma_i/\mathrm{Tr}\sigma_i$ is *defined only when* $\mathrm{Tr}\sigma_i>0$; downstream, $\Psi_l(0)=0$ for every continuation, so nothing is normalized there either.

**Records.**
- *Zero cases:* $A_i=\emptyset$ gives $\sigma_i=0$ in dimension $e_i$, still a block; $d=1$: $\rho=(1)$, $\sigma_i=\sum_aK_{i,a}K_{i,a}^*$; all $e_i=1$: $\Sigma=\mathrm{diag}(p(1),\dots,p(m))$, the classical outcome distribution.
- *Operations / relations:* $\rho\mapsto(\sigma_i)_i\mapsto\Sigma$; block read-out $J_i^*(\cdot)J_i$; $\Lambda$ for $\circ_i$; merges add equal-size blocks through a CPTP tag-forgetting map, generally not an isometry. The typed algebra is $\bigoplus_i M_{e_i}$; the chosen extension of a component map to all of $M_E$ dephases inter-block coherences. Unit laws hold on the typed algebra, not as identities of these full-matrix extensions.
- *Admissible compositions:* $\Lambda_{\mathcal L}\circ\Phi^{\mathcal K}_\oplus=\Phi^{\mathcal K\circ_i\mathcal L}_\oplus$; $\Lambda$ composes along nested substitution; rationality: $\rho,\mathcal K$ rational $\Rightarrow\sigma_i,\Sigma$ rational.

---

## BR-32 — Choi/effect duality with every transpose explicit

**Assumptions / domains.** $\Phi:M_d(K)\to M_e(K)$ $K$-linear; $\Phi^*$ its HS adjoint (well defined because $K$ is conjugation-closed).

**Claim 1.** $\mathrm{Tr}_{\mathrm{out}}C_\Phi=\overline{\Phi^*(I_e)}$ (entrywise conjugate). If $\Phi^*(I_e)$ is Hermitian — true for every CP $\Phi$, where $\Phi^*(I)=\sum K^*K$ — this reads
$$\Phi^*(I_e)=\big(\mathrm{Tr}_{\mathrm{out}}C_\Phi\big)^{T}.$$
*Proof.* $\mathrm{Tr}_{\mathrm{out}}C_\Phi=\sum_{jk}E_{jk}\,\mathrm{Tr}\Phi(E_{jk})$, and $\mathrm{Tr}\Phi(E_{jk})=\mathrm{Tr}(I_e^*\Phi(E_{jk}))=\mathrm{Tr}(\Phi^*(I_e)^*E_{jk})=\big(\Phi^*(I_e)^*\big)_{kj}=\overline{\Phi^*(I_e)_{jk}}$. Hence $\mathrm{Tr}_{\mathrm{out}}C_\Phi=\overline{\Phi^*(I_e)}$, and $\overline{M}=M^T$ exactly when $M=M^*$. $\square$ (Kraus check: $\mathrm{Tr}(KE_{jk}K^*)=(K^*K)_{kj}$.)

**Claim 2 (scalar output).** $\Phi_A(X)=\mathrm{Tr}(AX)$, $A\in M_d(K)$. Then $C_{\Phi_A}=\sum_{jk}E_{jk}\,\mathrm{Tr}(AE_{jk})=\sum_{jk}A_{kj}E_{jk}=A^T$. And $\Phi_A^*(y)=yA^*$ for $y\in M_1$: $\mathrm{Tr}(\Phi_A(X)^*y)=y\,\overline{\mathrm{Tr}(AX)}=y\,\mathrm{Tr}(X^*A^*)=\mathrm{Tr}(X^*\,yA^*)$. So $\Phi_A^*(1)=A^*$, which equals $A$ exactly for Hermitian $A$ — in particular for every effect. $\square$

**Corrected identification.** A trace instrument (all $e_i=1$, $K_{i,a}=k_{i,a}^*\in K^{1\times d}$) has $\Phi_i(X)=\mathrm{Tr}(A_iX)$ with $A_i=\sum_ak_{i,a}k_{i,a}^*=\Phi_i^*(1)$ Hermitian PSD, and
$$C_i=A_i^{T}=\overline{A_i}\quad(\text{not }A_i).$$
The map $(C_i)_i\mapsto(C_i^T)_i$ is a bijection between rational Choi tuples with $\sum_iC_i=I_d$ and rational POVMs; BR-30's parenthetical "$C_i=A_i$" is to be read with this transpose.

**Example.** $A=H_{12}=\begin{pmatrix}\tfrac12&\tfrac i2\\-\tfrac i2&\tfrac12\end{pmatrix}$ is an effect; $C_{\Phi_A}=A^T=\begin{pmatrix}\tfrac12&-\tfrac i2\\\tfrac i2&\tfrac12\end{pmatrix}\ne A=\Phi_A^*(1)$ (verified). Real symmetric effects ($E_{jj}$, $G_{jk}$) are fixed by $T$; the discrepancy is exactly the imaginary off-diagonal part.

**Why normalization is unaffected.** $\sum_i\mathrm{Tr}_{\mathrm{out}}C_i=\sum_i\overline{\Phi_i^*(I)}=\overline{\sum_iA_i}=\overline{I_d}=I_d$: the identity is invariant under both conjugation and transpose, so $\sum_i\mathrm{Tr}_{e_i}C_i=I_d\iff\sum_iA_i=I_d$ regardless of which side carries the transpose. Moreover $C\mapsto C^T$ preserves PSD, trace, rationality and partial traces ($\mathrm{Tr}_{\mathrm{out}}(C^T)=(\mathrm{Tr}_{\mathrm{out}}C)^T$), so the convex set of BR-30 is stable under slotwise transpose.

**Records.**
- *Zero cases:* $\Phi=0$: both sides $0$; $d=1$: $C_\Phi=\Phi(1)$, $\Phi^*(I)=\mathrm{Tr}\Phi(1)$, no transpose visible; $e=1$ and $A$ real symmetric: $C=A$.
- *Operations / relations:* $\mathrm{Tr}_{\mathrm{out}}$, conjugation, transpose; $\mathrm{Tr}_{\mathrm{in}}C_\Phi=\Phi(I_d)$ needs no transpose (dual statement).
- *Admissible compositions:* $(\Psi\circ\Phi)^*(I)=\Phi^*(\Psi^*(I))$, so $\mathrm{Tr}_{\mathrm{out}}C_{\Psi\circ\Phi}=\overline{\Phi^*(\Psi^*(I))}$ — used in BR-37 for normalization transport.

---

## BR-33 — Precise merge/continuation compatibility

**Assumptions / domains.** $\mathcal K$ with slots $i<j$, $e_i=e_j=e$; $\mathcal L\in\mathrm{Ins}(g_1..g_n;e)$ with branch sets $B_l$.

**Same-continuation identity, all reindexing explicit.**
*Left side* $\mathrm{merge}_{i,j}(\mathcal K)\circ_i\mathcal L$: profile $(e_1..e_{i-1},g_1..g_n,e_{i+1}..e_{j-1},e_{j+1}..e_m;d)$; positions $i..i+n-1$ carry slot $(i,l)$ with index set $(A_i\sqcup A_j)\times B_l$ and operators $L_{l,b}K_{i,a}$ ($a\in A_i$), $L_{l,b}K_{j,c}$ ($c\in A_j$).
*Right side:* in $\mathcal K\circ_i\mathcal L$ slot $j$ sits at position $j'=j+n-1$; $(\mathcal K\circ_i\mathcal L)\circ_{j'}\mathcal L$ places $n$ slots at positions $j'..j'+n-1$ with index sets $A_j\times B_l$ and operators $L_{l,b}K_{j,c}$. The slotwise merge is the simultaneous merge along the position pairing $\beta(l)=(i+l-1,\ j'+l-1)$, $l=1..n$ (performed for $l=n,n-1,\dots,1$ so earlier positions are undisturbed, or defined at once on position sets). The merged slot $l$ has index set $(A_i\times B_l)\sqcup(A_j\times B_l)$.
*Identity:* the canonical bijection $(A_i\sqcup A_j)\times B_l\to(A_i\times B_l)\sqcup(A_j\times B_l)$, $(\iota_1a,b)\mapsto\iota_1(a,b)$, $(\iota_2c,b)\mapsto\iota_2(c,b)$, carries operators to equal operators; untouched slots coincide position by position. So both sides are the same element of $\mathrm{Ins}$ (BR-26 $\sim$). $\square$

**Sufficient uniformly, not necessary.** The identity holds for *every* $\mathcal K$ and $\mathcal L$ (uniform). It is not necessary for a fixed instrument: outer slots $\{E_{11}\},\{E_{22}\}$, continuations $I$ on slot 1 and $D=\mathrm{diag}(-1,1)$ on slot 2. Merge-after-continuations: $\{IE_{11},\ DE_{22}\}=\{E_{11},E_{22}\}$, which equals merge-first followed by the single continuation $I$ — as representatives, not merely as classes (verified). (With $D$ as the common continuation, $\{DE_{11},DE_{22}\}=\{-E_{11},E_{22}\}$: a different representative, the same CP map; so at the BR-30 level both $I$ and $D$ are merge-first continuations.) The reason: $DE_{22}=E_{22}$ — the two continuations agree on the output support of slot 2.

**CP-level exact condition.** Let $\Psi=(\Psi_l)_l,\Psi'=(\Psi'_l)_l$ be CP tuples (continuations) with $\sum_l\Psi_l,\sum_l\Psi'_l$ TP, and $M_l:=\Psi_l\circ\Phi_i+\Psi'_l\circ\Phi_j$ (merge after continuations). A *common merge-first continuation* is a CP tuple $\Theta=(\Theta_l)_l$ with $\sum_l\Theta_l$ TP and
$$\Theta_l\circ(\Phi_i+\Phi_j)=M_l\quad\forall l.\tag{F}$$
Exactly: (F) holds iff the linear system $\mathrm{link}\big(C_{\Phi_i}+C_{\Phi_j},\,C_{\Theta_l}\big)=C_{M_l}$ (BR-37) has a solution with every $C_{\Theta_l}\succeq0$ rational and $\sum_l\mathrm{Tr}_{g_l}C_{\Theta_l}=I_e$. Three consequences:
- *Necessary (linear):* $\ker(\Phi_i+\Phi_j)\subseteq\ker M_l$ for all $l$.
- *Sufficient:* termwise agreement $\Theta_l\circ\Phi_i=\Psi_l\circ\Phi_i$ and $\Theta_l\circ\Phi_j=\Psi'_l\circ\Phi_j$ for some $\Theta$ (uniform case $\Psi=\Psi'$ included). Not necessary: slots $\tfrac35I,\tfrac45I$ ($\Phi_1+\Phi_2=\mathrm{Id}$), continuations $\mathrm{Id}$ and $\mathrm{Ad}_Z$: $\Theta=\tfrac9{25}\mathrm{Id}+\tfrac{16}{25}\mathrm{Ad}_Z$ satisfies (F) and is CP, but $\Theta\circ\Phi_1\ne\mathrm{Id}\circ\Phi_1$ (verified).
- *Decidable regime:* if $\Phi_i+\Phi_j$ is surjective onto $M_e$, (F) determines $\Theta_l=M_l\circ R$ uniquely on $M_e$ for any linear right inverse $R$ (after the kernel condition), and the exact test is "each $C_{\Theta_l}$ PSD" — BR-35. Trace preservation of $\sum_l\Theta_l$ is then automatic: $\mathrm{Tr}\sum_lM_l(X)=\mathrm{Tr}\Phi_i(X)+\mathrm{Tr}\Phi_j(X)=\mathrm{Tr}(\Phi_i+\Phi_j)(X)$. When $\Phi_i+\Phi_j$ is not surjective the kernel condition fixes $\Theta_l$ only on $\mathrm{Im}(\Phi_i+\Phi_j)$, and (F) is a CP-extension problem from that subspace; it is not reducible to kernel conditions, which is why the exact statement is the PSD-feasibility system above.

*Non-existence example (fails already at the linear level).* Slots $\{E_{11}\},\{E_{12}\}$ (normalized: $E_{11}+E_{22}=I$), so $\Phi_1(X)=X_{11}E_{11}$, $\Phi_2(X)=X_{22}E_{11}$, $\Phi_1+\Phi_2=\mathrm{Tr}(\cdot)E_{11}$. Continuations $\mathrm{Id}$ and $\mathrm{Ad}_X$ ($X$ the flip): $M=\Delta$. $E_{11}-E_{22}\in\ker(\Phi_1+\Phi_2)\setminus\ker\Delta$. The merge-after representative $\{E_{11},XE_{12}\}=\{E_{11},E_{22}\}$ is a perfectly good instrument with no merge-first form (verified).

**Separations.**
- *Disjoint merges* $\mathrm{merge}_{i,j}$, $\mathrm{merge}_{k,l}$ with $\{i,j\}\cap\{k,l\}=\emptyset$ commute exactly (disjoint index unions; positions shift predictably).
- *Overlapping coarsenings* $\mathrm{merge}_{i,j}$ then $\mathrm{merge}_{i,k}$: one slot with $A_i\sqcup A_j\sqcup A_k$; order-independent up to the associativity bijection of $\sqcup$; effects add.
- *Zero-slot profile changes:* $\mathrm{merge}_{i,j}$ with $A_j=\emptyset$ leaves every operator and effect unchanged ($A_i\sqcup\emptyset\cong A_i$) but lowers the arity, changes the $\Sigma_m$ component and which $\circ_k$ exist; it is a profile change, not a coarsening of information, and is unavailable when no slot shares $e_j$.

**Records.**
- *Zero cases:* $n=1$ (a channel continuation): identity reduces to $\Phi_{i\sqcup j}\mapsto\Psi\circ(\Phi_i+\Phi_j)$; a zero slot merged after any continuation is still zero.
- *Operations / relations:* $\sqcup$ of index sets; position pairing $\beta$; link product; kernel inclusion; PSD feasibility.
- *Admissible compositions:* merge $\circ_i$ (same $\mathcal L$) $=$ $\circ_i,\circ_{j'}$ then slotwise merge; merge after distinct continuations is always admissible as an instrument, has a merge-first form iff (F) is feasible.

---

## BR-34 — Rational mixing and carrier scope

**Assumptions / domains.** Choi tuples $\mathcal C(e_1..e_m;d)=\{(C_i)_i:\ C_i\in M_{de_i}(K),\ C_i\succeq0,\ \sum_i\mathrm{Tr}_{e_i}C_i=I_d\}$ (BR-30).

**Closure under rational convex weights.** For $\lambda_t\in\mathbb Q_{\ge0}$, $\sum_t\lambda_t=1$, tuples $C^{(t)}\in\mathcal C$: $\sum_t\lambda_tC^{(t)}_i$ has entries in $K$ ($\mathbb Q\subset K$), is PSD (cone), and $\sum_i\mathrm{Tr}_{e_i}\sum_t\lambda_tC^{(t)}_i=\sum_t\lambda_tI_d=I_d$. $\square$ So $\mathcal C$ is $\mathbb Q$-convex. It is not $\mathbb R$-convex *as a subset of $K$-matrices*: with $C^{(1)}$ the trace instrument $(E_{11}^T,E_{22}^T)$ and $C^{(2)}=(G_{12}^T,(I-G_{12})^T)$ and $\lambda=1/\sqrt2$, the mixture's $(1,1)$ entry is $\tfrac12(1+\tfrac1{\sqrt2})\notin K$ (verified). The ambient complex-Choi instrument set is real-convex and its $K$-points are $\mathcal C$. Its finite real convex hull of $K$-points need not equal the ambient set: irrational projective effects are extreme. The norm closure does equal the ambient set, by exact rational-unitary approximation of stacked Kraus isometries; see corrections.md.

**Rational Kraus realization of a rational mixture.** Given rational instruments $\mathcal K^{(t)}$ and $\lambda_t=p_t/q_t$, write $p_tq_t=\sum_{s=1}^4a_{t,s}^2$ (Lagrange) so $\lambda_t=\sum_sr_{t,s}^2$, $r_{t,s}=a_{t,s}/q_t\in\mathbb Q$. The family $\{r_{t,s}K^{(t)}_{i,a}\}_{t,s,a}$ in slot $i$ is rational and normalized: $\sum_{t,s,a}r_{t,s}^2K^*K=\sum_t\lambda_tI_d=I_d$; its slot map is $\sum_t\lambda_t\Phi^{(t)}_i$, i.e. its Choi tuple is the mixture. No $\sqrt{\lambda_t}$ is used (verified with weights $\tfrac27,\tfrac57$). A single Gaussian norm sometimes suffices (for example $1/2=|(1+i)/2|^2$), but not always ($1/3$ is not a Gaussian-rational norm). TWO Gaussian norms always suffice by grouping four rational squares in pairs; this gives the optional $2\,\mathrm{rank}$ Gram bound proved in corrections.md.

**Carrier scope — exact statements.**
1. If $\rho\in M_d(K)$ and $\mathcal K$ is rational, then every $\sigma_i\in M_{e_i}(K)$, $\mathrm{Tr}\sigma_i\in\mathbb Q$ (real element of $K$), every probability $\mathrm{Tr}(\rho A_i)\in\mathbb Q$, and every normalized conditional state $\sigma_i/\mathrm{Tr}\sigma_i$ (when defined) is in $M_{e_i}(K)$. Rationality propagates forward.
2. Conversely, by BR-21/23, $\rho\in M_d(K)$ iff all probe values $p(E_{jj}),p(G_{jk}),p(H_{jk})$ are rational; $\rho$ is real symmetric iff all $p(H_{jk})=\tfrac12$; $\rho\in M_d(\mathbb Q)$ iff both.
3. Arbitrary real probe values require complex entries whenever some $p(H_{jk})\ne\tfrac12$ (nonzero imaginary part) and leave $K$ whenever some value is irrational. Example: $\rho=\tfrac12(I+\tfrac1{\sqrt2}S_{12})$ is a density (eigenvalues $\tfrac12(1\pm\tfrac1{\sqrt2})$) with $p(G_{12})=\tfrac12+\tfrac1{2\sqrt2}\notin\mathbb Q$ (verified). Its statistics are real and need not be rational; some remain rational, for example the identity probability 1.
4. Therefore: the instrument carrier is $K$; the state carrier is complex PSD trace one; the probability carrier is $[0,1]$. "All probabilities and states lie in $K$" is false and is not asserted; what holds is closure of $K$-data under $K$-instruments and the exact characterization in 2.

**Records.**
- *Zero cases:* $\lambda_t=0$ contributes no Kraus operators; a weight that is a rational square needs one copy; $\mathrm{Tr}\sigma_i=0$: no conditional state, rational or otherwise.
- *Operations / relations:* $\mathbb Q$-convex combination; four-square splitting; probe inversion.
- *Admissible compositions:* normalized convex mixtures commute with $\circ_i$ affinely in each argument (the second argument leaves untouched slots fixed) ($(\sum\lambda_t\mathcal K^{(t)})\circ_i\mathcal L=\sum\lambda_t(\mathcal K^{(t)}\circ_i\mathcal L)$ at the CP level); rationality closure is preserved by $\circ_i$, merge and $\boxtimes$ (BR-39).

---

## BR-35 — Certifying rational PSD admission algorithm

**Assumptions / domains.** $A\in\mathrm{Herm}_d(K)$, $K=\mathbb Q(i)$: diagonal entries in $\mathbb Q$, off-diagonal in $K$; exact arithmetic and exact sign tests on $\mathbb Q$ available.

**Algorithm $\mathrm{PSD}(A)$.**
1. $d=0$: return PSD, empty certificate.
2. If some $a_{jj}<0$: return witness $v=e_j$ ($v^*Av=a_{jj}<0$).
3. If all $a_{jj}=0$: if $A=0$ return PSD with $L=I$, $D=0$; else pick $a_{jk}\ne0$, $j\ne k$, return witness $v=e_j-\overline{a_{jk}}\,e_k$ (then $v^*Av=2\,\mathrm{Re}(-\overline{a_{jk}}a_{jk})=-2|a_{jk}|^2<0$; this is Lemma Z made constructive).
4. Otherwise pick $j_0$ with $\pi:=a_{j_0j_0}>0$; let $P$ be the permutation moving $j_0$ to the front, $B=PAP^T=\begin{pmatrix}\pi&c^*\\c&B_{22}\end{pmatrix}$; form the Schur complement $A'=B_{22}-cc^*/\pi\in\mathrm{Herm}_{d-1}(K)$; recurse on $A'$.
   - If $A'=L'D'L'^*$: return $L=P^T\begin{pmatrix}1&0\\c/\pi&L'\end{pmatrix}$, $D=\mathrm{diag}(\pi,D')$.
   - If $A'$ has witness $v'$: return $v=P^T\begin{pmatrix}-c^*v'/\pi\\v'\end{pmatrix}$.

**Termination.** Each pass through step 4 reduces $d$ by one; steps 1–3 return. All operations are $+,-,\times,\div$ and conjugation in $K$ plus sign tests of elements of $\mathbb Q$.

**Correctness.** (a) Witnesses: step 2 and 3 computed above. Step 4: for $v=\binom{x}{v'}$, $v^*Bv=\pi|x|^2+2\mathrm{Re}(\bar x\,c^*v')+v'^*B_{22}v'$; with $x=-c^*v'/\pi$ the first two terms give $-|c^*v'|^2/\pi$, so $v^*Bv=v'^*(B_{22}-cc^*/\pi)v'=v'^*A'v'<0$, and $v\ne0$ since $v'\ne0$; $v^*Av=(Pv)^*B(Pv)$ transports it. (b) Certificates: $B=\begin{pmatrix}1&0\\c/\pi&I\end{pmatrix}\begin{pmatrix}\pi&0\\0&A'\end{pmatrix}\begin{pmatrix}1&c^*/\pi\\0&I\end{pmatrix}$ is an identity of rational matrices; composing with $A'=L'D'L'^*$ gives $A=LDL^*$ with $D\ge0$ diagonal rational, hence $v^*Av=\sum_kD_{kk}|(L^*v)_k|^2\ge0$ for all $v\in\mathbb C^d$: $A$ is PSD over $\mathbb C$, not just over $K$. (c) Exactly one of the two outputs occurs, so the verdict is a decision. $\square$

**Witness transport through congruences.** If $A=MBM^*$ with $M$ invertible and $w^*Bw<0$, then $v=M^{-*}w$ gives $v^*Av=w^*Bw<0$ (verified). The recursion is this transport applied to $M=P^T\begin{pmatrix}1&0\\c/\pi&I\end{pmatrix}$.

**Coverage.** Negative diagonal (step 2); positive pivots (step 4, pivot chosen among positive diagonal entries only, never zero); zero-diagonal nonzero block (step 3, including purely imaginary off-diagonals: $A=\begin{pmatrix}0&i\\-i&0\end{pmatrix}$, $v=e_1+ie_2$, $v^*Av=-2$); singular PSD inputs (zeros in $D$: $\begin{pmatrix}1&1\\1&1\end{pmatrix}\mapsto D=\mathrm{diag}(1,0)$); hidden negativity exposed only after pivoting ($\begin{pmatrix}1&1\\1&0\end{pmatrix}$: $A'=-1$). All eleven test matrices in the script return a certificate that reproduces $A$ or a witness with $v^*Av<0$ re-verified independently.

**Real-algebraic inputs.** The algorithm uses exactly: field operations, conjugation, equality test with $0$, and the sign of a real element. For entries in a real-algebraic (or real-closed) field one additionally needs (i) a representation of elements (e.g. $\mathbb Q(\alpha)$ with a minimal polynomial and isolating interval, or Thom encodings), (ii) exact arithmetic in that representation, and (iii) an exact sign procedure (Sturm sequences / interval refinement, which terminates because the number is algebraic and nonzero-ness is decidable). With these the same algorithm decides PSD. For reals given only by approximation oracles none of this holds: "$a_{jj}=0$" vs "$a_{jj}=10^{-100}$" is not decidable from finitely many approximations, so step 3 cannot be entered exactly and the procedure is not automatically computable.

**Records.**
- *Zero cases:* $A=0$; $d=1$ ($A=(a)$: PSD iff $a\ge0$); zero rows/columns pass through as zero pivots in $D$.
- *Operations / relations:* permutation, Schur complement, congruence, $LDL^*$.
- *Admissible compositions:* $A\succeq0\Rightarrow M^*AM\succeq0$ for any rational $M$, with certificate $(M^*L)\,D\,(M^*L)^*$ — sufficiency of a certificate never needs $L$ invertible; direct sums certify blockwise; a witness of a block, zero-padded, is a witness of the direct sum.

---

## BR-36 — Explicit qubit probability-admission region

**Setting (BR-25, $d=2$).** $\lambda=\tfrac13$, $M_1=\tfrac13E_{11}$, $M_2=\tfrac13G_{12}$, $M_3=\tfrac13H_{12}$,
$$M_0=I-M_1-M_2-M_3=\begin{pmatrix}\tfrac13&-\tfrac{1+i}6\\-\tfrac{1-i}6&\tfrac23\end{pmatrix},\qquad\det M_0=\tfrac16,\qquad \mathrm{eig}\,M_0=\tfrac{3\mp\sqrt3}{6}.$$
$M_0\succ0$ (BR-35 certificate), so this is a rational POVM with four outcomes and $q_i=\mathrm{Tr}(\rho M_i)$.

**Inverse.** From $q_1,q_2,q_3$ (BR-21):
$$\rho_{11}=3q_1,\quad\rho_{22}=1-3q_1,\quad\rho_{12}=(3q_2-\tfrac12)+i(3q_3-\tfrac12),\quad\rho_{21}=\overline{\rho_{12}},$$
and $q_0$ is not free: $q_0=1-q_1-q_2-q_3$ (verified symbolically).

**Admission (necessary and sufficient).** $(q_0,q_1,q_2,q_3)$ are the statistics of a density iff
$$q_0=1-q_1-q_2-q_3\qquad\text{and}\qquad(6q_1-1)^2+(6q_2-1)^2+(6q_3-1)^2\le1 .$$
*Proof.* A $2\times2$ Hermitian matrix with trace $1$ is PSD iff $\det\ge0$ (eigenvalues sum to $1$; nonnegative product then forces both $\ge0$; also $\rho_{11}\rho_{22}\ge|\rho_{12}|^2\ge0$ with $\rho_{11}+\rho_{22}=1$ forces both diagonal entries $\ge0$). With the inverse, $4\det\rho=1-\sum_{i=1}^3(6q_i-1)^2$ (verified: $4\det\rho+\text{ball}=0$). $\square$
So the admissible region is the affine image of the Bloch ball: a Euclidean ball of radius $\tfrac16$ centred at $(\tfrac16,\tfrac16,\tfrac16)$ in $(q_1,q_2,q_3)$, with $q_0$ determined. In Bloch coordinates $\rho=\tfrac12(I+x\sigma_x+y\sigma_y+z\sigma_z)$: $q_1=\tfrac{1+z}6$, $q_2=\tfrac{1+x}6$, $q_3=\tfrac{1-y}6$, $q_0=\tfrac{3-x+y-z}6$.

**Bounds and boundary.**
- $0\le q_i\le\tfrac13$ for $i=1,2,3$; equality at the six axis points.
- $q_0\in\big[\tfrac{3-\sqrt3}6,\ \tfrac{3+\sqrt3}6\big]$: since $\sum_iq_i=\tfrac12+\tfrac16\sum_iu_i$ with $\|u\|\le1$, and $\max\sum u_i=\sqrt3$. The nonzero lower bound $q_0\ge\tfrac{3-\sqrt3}6=\lambda_{\min}(M_0)\approx0.2113$ is attained only at the pure state $q_1=q_2=q_3=\tfrac{1+1/\sqrt3}6$ (verified: on the sphere). It is irrational, so no rational data attain it; rational admissible data satisfy $q_0>\tfrac{3-\sqrt3}6$ strictly.
- Boundary of the ball $\iff\det\rho=0\iff\rho$ pure. Interior $\iff$ mixed.
- Zero cases: $q_1=0\Rightarrow q_2=q_3=\tfrac16$, $q_0=\tfrac23$, $\rho=E_{22}$ (Lemma Z forces $\rho_{12}=0$); $q_1=\tfrac13\Rightarrow\rho=E_{11}$, $q_0=\tfrac13$; $q_2=0\Rightarrow\rho$ the projector onto $e_1-e_2$; $q_3=0\Rightarrow\rho$ the projector onto $e_1+ie_2$; $q_0$ is never $0$. Maximally mixed: $q=(\tfrac12,\tfrac16,\tfrac16,\tfrac16)$. A rational point outside: $(q_1,q_2,q_3)=(\tfrac13,\tfrac13,\tfrac16)$ gives $\rho$ with $\det<0$ (verified).

No tolerances: the test is one equality and one polynomial inequality; for rational data both are exact in $\mathbb Q$, and the certificate is BR-35 on the reconstructed $\rho$.

**Records.**
- *Operations / relations:* affine inverse $q\mapsto\rho$; the single inequality $\det\rho\ge0$; Bloch change of variables.
- *Admissible compositions:* unitary conjugation of the probe basis by a rational unitary moves the ball by an affine map; coarse-graining two outcomes projects the ball and loses injectivity (BR-25).

---

## BR-37 — Operadic composition directly in Choi coordinates

**Assumptions / domains.** $\Phi:M_d\to M_e$, $\Psi:M_e\to M_g$ $K$-linear; $A=C_\Phi\in M_d\otimes M_e$, $B=C_\Psi\in M_e\otimes M_g$; all tensor orders are (input, output) and for triples $(d,e,g)$.

**Index formula.** $\Psi(\Phi(E_{jk}))=\Psi\big(\sum_{ab}\Phi(E_{jk})_{ab}E_{ab}\big)=\sum_{ab}A[(j,a),(k,b)]\,\Psi(E_{ab})$; taking entry $(\alpha,\beta)$,
$$C_{\Psi\circ\Phi}[(j,\alpha),(k,\beta)]=\sum_{a,b}A[(j,a),(k,b)]\;B[(a,\alpha),(b,\beta)].\qquad\square$$

**Link-product form.** With $B^{T_e}$ the partial transpose on the $e$ factor, $B^{T_e}[(a,\alpha),(b,\beta)]=B[(b,\alpha),(a,\beta)]$, and $\mathrm{Tr}_e$ the trace over the middle factor of $M_d\otimes M_e\otimes M_g$:
$$C_{\Psi\circ\Phi}=\mathrm{Tr}_e\big[(A\otimes I_g)(I_d\otimes B^{T_e})\big].$$
*Proof.* $(A\otimes I_g)[(j,a,\alpha),(k,b,\beta)]=A[(j,a),(k,b)]\delta_{\alpha\beta}$ and $(I_d\otimes B^{T_e})[(k,b,\beta),(k',b',\beta')]=\delta_{kk'}B[(b',\beta),(b,\beta')]$. Their product has entry $\sum_bA[(j,a),(k',b)]\,B[(b',\alpha),(b,\beta')]$ at $[(j,a,\alpha),(k',b',\beta')]$; $\mathrm{Tr}_e$ sets $a=b'$ and sums, giving the index formula. $\square$ (Verified on a $2\to3\to2$ example with complex entries.)

**Slot composition without Kraus representatives.** In BR-30, slot $(i,l)$ of $\mathcal K\circ_i\mathcal L$ has $C_{(i,l)}=C_{\Psi_l\circ\Phi_i}=\mathrm{link}(C_i,C'_l)$ — a function of the Choi matrices alone; no representative is chosen, so the descent of $\circ_i$ to $\mathrm{Ins}^{\mathrm{op}}$ is given by an explicit formula rather than by "compute from any Kraus pair". Positivity: $\mathrm{link}(C_\Phi,C_\Psi)=(\mathrm{id}_d\otimes\Psi)(C_\Phi)$ is PSD because $\Psi$ is CP (BR-29) — a statement about $\Psi$, not about a representative.

**Normalization preserved, in Choi coordinates.** $\mathrm{Tr}_g\,\mathrm{link}(A,B)[j,k]=\sum_{a,b}A[(j,a),(k,b)]\,(\mathrm{Tr}_gB)[a,b]$. For a continuation instrument $(B_l)_l$ with $\sum_l\mathrm{Tr}_{g_l}B_l=I_e$:
$$\sum_l\mathrm{Tr}_{g_l}C_{(i,l)}[j,k]=\sum_{a,b}A[(j,a),(k,b)]\,\delta_{ab}=(\mathrm{Tr}_eC_i)[j,k],$$
so $\sum_{j\ne i}\mathrm{Tr}_{e_j}C_j+\sum_l\mathrm{Tr}_{g_l}C_{(i,l)}=\sum_j\mathrm{Tr}_{e_j}C_j=I_d$ (verified). This is BR-32's $(\Psi\circ\Phi)^*(I)=\Phi^*(\Psi^*(I))$ read in coordinates; no transpose appears because the identity is transpose-invariant.

**Records.**
- *Zero cases:* $A=0$ or $B=0$: link $=0$; $e=1$: $A=A_\Phi^T$ is $d\times d$, $B=\Psi(1)$, link $=A\otimes\Psi(1)$ (prepare after measure); $g=1$: link $=\sum_{ab}A[(j,a),(k,b)]B_{ab}=\big(\mathrm{Tr}(B^T\Phi(E_{jk}))\big)_{jk}$.
- *Operations / relations:* partial transpose on the middle factor, middle partial trace; bilinearity in $(A,B)$.
- *Admissible compositions:* associativity $\mathrm{link}(\mathrm{link}(A,B),C)=\mathrm{link}(A,\mathrm{link}(B,C))$ (both are $C_{\Xi\circ\Psi\circ\Phi}$); output dimension of $A$ must equal input dimension of $B$; tensor: $C_{\Phi\otimes\Psi}=P(C_\Phi\otimes C_\Psi)P^T$ with the leg permutation $(d,e,d',e')\to(d,d',e,e')$ (BR-39).

---

## BR-38 — Rational unitary equivalence after zero padding

**Assumptions / domains.** $A\in K^{N\times r}$, $B\in K^{N\times s}$, $AA^*=BB^*$. $R=\max(r,s)$; $A_p,B_p\in K^{N\times R}$ zero-padded. Convention: $a_m:=A_p^*e_m\in K^R$ (the conjugate of row $m$), $b_m:=B_p^*e_m$; then $a_m^*a_n=(A_pA_p^*)_{mn}=(B_pB_p^*)_{mn}=b_m^*b_n$: equal Gram matrices $\Gamma$. The target $B_p=A_pU$ is equivalent to $B_p^*=U^*A_p^*$, i.e. $Va_m=b_m$ for all $m$ with $V:=U^*$.

**One reflection.** For $a\ne b$ with $\|a\|=\|b\|$: $w=a-b$, $c=w^*a$, $U_w=I-ww^*/c$.
- $c\ne0$: if $c=0$ then $b^*a=\|a\|^2=\|a\|\|b\|$, Cauchy–Schwarz equality forces $b=\mu a$ with $\bar\mu\|a\|^2=\|a\|^2$, so $b=a$, contradiction ($a=b=0$ is the excluded case $a=b$).
- $w^*w=\|a\|^2-a^*b-b^*a+\|b\|^2=c+\bar c$ (using $\bar c=a^*w=\|a\|^2-a^*b$). Hence $U_w^*U_w=I-ww^*(\tfrac1c+\tfrac1{\bar c})+ww^*\tfrac{c+\bar c}{c\bar c}=I$.
- $U_wa=a-w\,(w^*a)/c=a-w=b$.
- $U_wx=x$ for every $x\perp w$.
All entries in $K$ (one division by $c\in K\setminus0$). CC-30 is the case $a=e_1$.

**Matching one by one, fixing the matched.** Set $V_0=I_R$. For $m=1..N$: let $a'=V_{m-1}a_m$. If $a'=b_m$, set $V_m=V_{m-1}$. Otherwise $\|a'\|=\|a_m\|=\|b_m\|$ (Gram) and for $n<m$:
$$b_n^*a'=(V_{m-1}a_n)^*V_{m-1}a_m=a_n^*a_m=b_n^*b_m,$$
so $w=a'-b_m\perp b_n$ for all $n<m$; $U_w$ fixes every $b_n$ and maps $a'\mapsto b_m$. Set $V_m=U_wV_{m-1}$; the invariant $V_ma_n=b_n$ ($n\le m$) holds. After $N$ steps $V=V_N$ is a product of rational unitaries with $Va_m=b_m$ for all $m$; $U=V^*$ gives $B_p=A_pU$. $\square$ (Verified: $\{I\}$ vs $\{\tfrac35I,\tfrac45I\}$ gives $U=\begin{pmatrix}\tfrac35&\tfrac45\\\tfrac45&-\tfrac35\end{pmatrix}$; $\{\tfrac35,\tfrac45\}$ vs $\{\tfrac13,\tfrac23,\tfrac23\}$; a complex $4\times2$ example with a zero row and a dependent row.)

**Zero and dependent vectors.** $a_m=0\Rightarrow\|b_m\|=0\Rightarrow b_m=0$: the step is skipped. If $a_m=\sum_{n<m}\gamma_na_n$ then $\|b_m-\sum\gamma_nb_n\|^2=\|a_m-\sum\gamma_na_n\|^2=0$ (Gram), so $b_m=\sum\gamma_nb_n=V_{m-1}a_m$ and the step is again skipped — no separate case is needed; the invariant handles it.

**Conjugation conventions.** Rows of $A$ enter as $a_m=A^*e_m$ (conjugated); $\Gamma_{mn}=a_m^*a_n$ is the $(m,n)$ entry of $AA^*$; $B=AU$ means each row of $B$ is the corresponding row of $A$ times $U$, i.e. $b_m=U^*a_m$. With the other convention (rows unconjugated, $r_m=A^Te_m$, $\Gamma'=\overline{AA^*}$) one obtains $\overline U$ instead; both are rational unitaries.

**Application to Kraus vectorizations.** Kraus families $\{K_i\}_{i\le r},\{L_j\}_{j\le s}$ of one channel have $A=[\mathrm{vec}K_1\cdots\mathrm{vec}K_r]$, $B=[\mathrm{vec}L_1\cdots\mathrm{vec}L_s]$ with $AA^*=C_\Phi=BB^*$ ($N=de$). Hence after zero-padding, $L_j=\sum_{i=1}^RU_{ij}K_i$ with $U$ a rational unitary on $K^R$ (verified on $\{E_{11},E_{22}\}$ vs its $3$-$4$-$5$ rotation). Nothing assumes $r$ or $s$ equals $\mathrm{rank}\,C_\Phi$; the minimal *rational* count can exceed the rank: the rank-one effect $\tfrac13E_{11}$ (slot $M_1$ of BR-36) is $kk^*$ for no $k\in K^2$, because $\tfrac13$ is not a norm from $\mathbb Q(i)$ (the full primitive-denominator descent proof is in corrections.md; the submitted finite integer search alone does not prove this), while $\tfrac13=|\tfrac{1+i}3|^2+|\tfrac13|^2$ gives a two-vector rational Gram decomposition (verified). Step 12's bound $4\,\mathrm{rank}$ is the general ceiling; the padding theorem compares any two counts below it.

**Records.**
- *Zero cases:* $A=B=0$: $U=I$; $r=s=1$: $b=\mu a$ with $|\mu|=1$, $U=(\mu)$; $N=1$.
- *Operations / relations:* padding; Gram equality; reflections $U_w$; product of reflections; $U=V^*$.
- *Admissible compositions:* if $B_p=A_pU$ and $C_p=B_pU'$ then $C_p=A_p(UU')$ (after padding to the common $R$); the completion is unique up to a unitary of the orthogonal complement of $\mathrm{span}\{a_m\}$; tensor and composition of Kraus families transport $U\otimes U'$ and $U\otimes U'$ on index pairs (BR-39, CC-29).

---

## BR-39 — Parallel composition compatible with the operad

**Assumptions / domains.** $\mathcal K\in\mathrm{Ins}(e_1..e_m;d)$, $\mathcal L\in\mathrm{Ins}(f_1..f_n;d')$. Kronecker convention: $K^d\otimes K^{d'}\cong K^{dd'}$ with index $(x,y)\mapsto xd'+y$ (first factor outer). **Physical input, stated explicitly:** two subsystems with no interaction and no shared randomness, both outcomes recorded jointly; the identification of the composite with $K^{dd'}$ by this Kronecker map is a labeling choice.

**Definition.** $\mathcal K\boxtimes\mathcal L\in\mathrm{Ins}\big((e_if_j)_{(i,j)};dd'\big)$: slots are ordered pairs $(i,j)$ in lexicographic order, slot $(i,j)$ carries $\{K_{i,a}\otimes L_{j,b}\}_{(a,b)\in A_i\times B_j}\subset K^{e_if_j\times dd'}$.
- *Normalization:* $\sum_{i,j,a,b}(K\otimes L)^*(K\otimes L)=\big(\sum K^*K\big)\otimes\big(\sum L^*L\big)=I_d\otimes I_{d'}=I_{dd'}$ (mixed-product).
- *Well defined on $\sim$:* bijections $\pi_i\times\sigma_j$ on $A_i\times B_j$.
- *Slot maps:* $\Phi_{(i,j)}=\Phi_i\otimes\Psi_j$ on $M_d\otimes M_{d'}\cong M_{dd'}$.

**Unit.** $\mathbf 1\in\mathrm{Ins}(1;1)$: one slot, one branch $(1)$. $\mathcal K\boxtimes\mathbf 1=\mathcal K$ exactly: $e_i\cdot1=e_i$, $K\otimes(1)=K$, $A_i\times\{*\}\cong A_i$, slot $(i,1)\mapsto i$ (verified).

**Swap law.** With $S_{p,q}$ the permutation matrix $K^p\otimes K^q\to K^q\otimes K^p$ (rational unitary):
$$L_{j,b}\otimes K_{i,a}=S_{e_i,f_j}\,(K_{i,a}\otimes L_{j,b})\,S_{d,d'}^{*},$$
so $\mathcal L\boxtimes\mathcal K=\tau\cdot\big(S^{\mathrm{out}}\,(\mathcal K\boxtimes\mathcal L)\,S^{\mathrm{in}*}\big)$ with $\tau$ the slot bijection $(i,j)\mapsto(j,i)$ (an element of $\Sigma_{mn}$) and $S^{\mathrm{out}}$ acting slotwise by $S_{e_i,f_j}$ (verified). The swap is an isomorphism of the operad extended by rational unitary change of colors; it is not an identity of representatives, since the two sides are instruments on differently labeled copies of $K^{dd'}$.


**Corrected full-grid interchange.** The originally displayed single-pair global equation is false. Its left side has $(m+p-1)(n+q-1)$ outcomes; its right side has $mn-1+pq$. The difference is $(m-1)(q-1)+(n-1)(p-1)$, positive in general. At $m=n=p=q=2$ the counts are 9 and 7, so no outcome permutation can identify them. Zero outcomes remain outcomes.

For every original pair $(r,s)$, simultaneously substitute the continuation
\[
\mathcal D_{rs}=\begin{cases}
\mathcal K'\boxtimes\mathcal L'&r=i,\ s=j,\\
\mathcal K'\boxtimes\mathrm{id}_{f_s}&r=i,\ s\ne j,\\
\mathrm{id}_{e_r}\boxtimes\mathcal L'&r\ne i,\ s=j,\\
\mathrm{id}_{e_rf_s}&r\ne i,\ s\ne j.
\end{cases}
\]
Then the resulting instrument agrees with $(\mathcal K\circ_i\mathcal K')\boxtimes(\mathcal L\circ_j\mathcal L')$ up to the explicit flattening permutation of outcomes and branch indices. The outcome bijection expands each original $r$ to $r$ or $(i,l)$ and each original $s$ to $s$ or $(j,l')$, then orders their pairs lexicographically. It is a bijection region by region, with
\[
(m-1)(n-1)+p(n-1)+q(m-1)+pq=(m+p-1)(n+q-1)
\]
outcomes on both sides. In each region the operator equality is the mixed-product law, with identity continuations in the untouched factor. Branch products are related by the canonical bijection $(a,c,b,c')\leftrightarrow(a,b,c,c')$. This proves the representative law modulo branch relabeling and the CP-map law. The one-selected-pair matrix identity in the submitted script is valid but does not prove the original global equation. One-sided refinement likewise requires one substitution at every affected pair.

**Descent to the CP quotient.** $\Phi_{(i,j)}=\Phi_i\otimes\Psi_j$ depends only on the classes of $\mathcal K,\mathcal L$; in Choi data $C_{(i,j)}=P\,(C_i\otimes C'_j)\,P^T$ with $P$ the leg permutation $(d,e_i,d',f_j)\to(d,d',e_i,f_j)$ (verified). Unit, swap and interchange are identities of CP maps, hence hold in $\mathrm{Ins}^{\mathrm{op}}$; normalization $\sum_{(i,j)}\mathrm{Tr}_{e_if_j}C_{(i,j)}=\big(\sum_i\mathrm{Tr}_{e_i}C_i\big)\otimes\big(\sum_j\mathrm{Tr}_{f_j}C'_j\big)=I_{dd'}$.

**Records.**
- *Zero cases:* a zero slot tensored with anything is a zero slot (and still a slot); $d'=1$, $\mathcal L=\mathbf 1$ recovers $\mathcal K$; trace instruments: $\boxtimes$ is the product POVM $(A_i\otimes B_j)$.
- *Operations / relations:* $\boxtimes$, $S_{p,q}$, $\tau$, $\beta$, leg permutation $P$.
- *Admissible compositions:* $\boxtimes$ is defined for any two profiles (no dimension constraint); $\circ_{(i,j)}$ requires a continuation with input colour $e_if_j$, and a *product* continuation is what the interchange law concerns — a non-product continuation on $K^{e_if_j}$ is admissible in the operad but is not a tensor of continuations (this is where interaction enters, and it is not covered by the law).

---

## BR-40 — Rational dilation of a full typed instrument

**Assumptions / domains.** Normalized rational slots $K_{i,a}:K^d\to K^{e_i}$, $a\in A_i$ (possibly empty). $E=\sum_ie_i$, $R=\sum_i|A_i|$. Branches enumerated $t=t(i,a)\in\{1..R\}$, slot-major. $\varepsilon_t$ the standard basis of $K^R$ (environment pointer). $R\ge1$: $\sum K^*K=I_d\ne0$ needs at least one operator.

**Construction.**
$$V=\sum_{(i,a)}\big(J_iK_{i,a}\big)\otimes\varepsilon_{t(i,a)}:\ K^d\to K^E\otimes K^R,\qquad Q_i=I_E\otimes P_i,\quad P_i=\sum_{a\in A_i}\varepsilon_{t(i,a)}\varepsilon_{t(i,a)}^* .$$
- $V$ is a rational isometry: $V^*V=\sum_{t,t'}K^*J_i^*J_{i'}K'\,(\varepsilon_t^*\varepsilon_{t'})=\sum_{(i,a)}K_{i,a}^*K_{i,a}=I_d$.
- $Q_i$ are orthogonal projections ($P_i$ diagonal $0/1$), mutually orthogonal (branch sets disjoint), $\sum_iQ_i=I_E\otimes I_R$ (every $t$ belongs to one slot). A zero slot $A_i=\emptyset$ has $P_i=0$, $Q_i=0$: the outcome label is retained with probability identically $0$.

**State-update identity.** For a density $\rho$ on $\mathbb C^d$ and $\mathrm{Tr}_R$ the partial trace over the pointer:
$$\mathrm{Tr}_R\big[Q_iV\rho V^*Q_i\big]=J_i\,\Phi_i(\rho)\,J_i^* .$$
*Proof.* $Q_iV=\sum_{(i',a')}(J_{i'}K_{i',a'})\otimes P_i\varepsilon_{t(i',a')}=\sum_{a\in A_i}(J_iK_{i,a})\otimes\varepsilon_{t(i,a)}$. Hence $Q_iV\rho V^*Q_i=\sum_{a,a'\in A_i}\big(J_iK_{i,a}\rho K_{i,a'}^*J_i^*\big)\otimes\varepsilon_{t(i,a)}\varepsilon_{t(i,a')}^*$, and $\mathrm{Tr}_R$ keeps the terms $a=a'$: $\sum_aJ_iK_{i,a}\rho K_{i,a}^*J_i^*=J_i\Phi_i(\rho)J_i^*$. $\square$ (Verified on a three-slot example with a zero slot.)
Consequences: the probability $\mathrm{Tr}(Q_iV\rho V^*)=\mathrm{Tr}\Phi_i(\rho)=\mathrm{Tr}(\rho A_i)$ (effect form) is the trace of the identity, not an independent fact; $\mathrm{Tr}_R[V\rho V^*]=\sum_iJ_i\Phi_i(\rho)J_i^*=\Sigma_{\mathcal K}(\rho)$, the typed output of BR-31; and on $\mathrm{ran}\,V$ the pointer projection coincides with the system block projection, $Q_iV=(J_iJ_i^*\otimes I_R)V$ (verified) — the outcome can be read from the environment pointer or from the type tag, with the same post-measurement state.

What the environment keeps before discarding: $\mathrm{Tr}_E[Q_iV\rho V^*Q_i]=\sum_{a,a'}\mathrm{Tr}(K_{i,a}\rho K_{i,a'}^*)\,\varepsilon_t\varepsilon_{t'}^*$ — coherence between branches *within* a slot. Discarding it is what makes distinct branches of one slot indistinguishable, consistent with BR-26's $\sim$ (branch relabeling) and BR-30's Kraus mixing.

**Finite size bounds.** Dilation space $K^E\otimes K^R$, dimension $E\cdot R$. $R\le\sum_i|A_i|$ as given; replacing each slot by a Step-12 family gives $R\le4\sum_i\mathrm{rank}\,C_i\le4dE$. Lower bound: $R\ge\sum_i r_i$ with $r_i$ the minimal rational Kraus count of $\Phi_i$, and $r_i\ge\mathrm{rank}\,C_i$ with strict inequality possible over $K$ (BR-38). The isometry extends to a rational unitary $U_0$ on $K^{ER}$ with $V=U_0B_0$, where $B_0:K^d\to K^{ER}$ is the first-$d$-coordinate injection. The expression $U_0(x\otimes\varepsilon_1)$ is not generally typed when $E\ne d$. For a literal product-ancilla implementation, put $D=\operatorname{lcm}(d,ER)$, $s=D/(ER)$ and $a=D/d$. Let $\widetilde V=V\otimes\eta_1^{(s)}:K^d\to K^E\otimes K^R\otimes K^s$ and $B_{\rm in}(x)=x\otimes\eta_1^{(a)}\in K^D$. Both are rational isometries with $d$ columns. Rational unitary matching gives $U B_{\rm in}=\widetilde V$. The pointer is $Q_i\otimes I_s$, and discarding $R s$ environmental dimensions recovers the same typed states. Bounds on the sum of per-slot rational Kraus counts apply to this disjoint-coordinate pointer construction, not to every conceivable dilation encoding.

**Physical assumptions, stated separately.** (P1) A composite $K^E\otimes K^R$ exists with the Kronecker labeling, and the declared input encoding can be realized; for a product ancilla use the common-$D$ construction above with its fixed initial ancilla, and assume the resulting rational unitary interaction is available (this is what turns the isometry into a dynamics). (P2) The pointer admits the projective measurement $\{Q_i\}$ — a coarse measurement that reads the slot but not the branch. (P3) The environment is then inaccessible: "discard" means partial trace, which is where probabilities become irreversible and branch coherence is lost. (P4) The system's output type is the direct-sum tag $K^E=\bigoplus K^{e_i}$ of BR-31; interpreting the block index as "which outcome occurred" is the same input as in BR-31. None of P1–P4 is derived here; the theorem is that *given* them, the Kraus instrument is exactly the observable statistics and state updates of this one rational isometry.

**Records.**
- *Zero cases:* $m=1$: ordinary Stinespring, $Q_1=I$; $d=1$: $V$ is a unit vector in $K^{ER}$; all $e_i=1$: $E=m$ and $J_i\Phi_i(\rho)J_i^*=\mathrm{Tr}(\rho A_i)E_{ii}$, a classical register; zero slot: $Q_i=0$, update $=0$, no normalization.
- *Operations / relations:* $V$, $Q_i$, $\mathrm{Tr}_R$, block read-out $J_i^*(\cdot)J_i$; unitary completion of $V$.
- *Admissible compositions:* nesting uses a controlled isometry on the selected system block and initializes a fixed auxiliary pointer state on every untouched block. If the outer branch count is $R$, the selected slot has $r_i$ branches and the continuation has $R'$ branches, the direct nested presentation has $(R-r_i)+r_iR'$ branch labels. The sequential dilation has pointer size $RR'$. These are related by an explicit isometric environment embedding: send affected labels $(a,b)$ to their product labels and untouched $a$ to $(a,1)$. Equality is after this embedding and re-tagging, not literal equality of different-dimensional isometries. Parallel dilation similarly requires reordering system and pointer tensor legs. All maps stay rational.

---

## Exact checks

The submitted `submission/br31_40_checks.py` produces 86 PASS labels in both replay modes. Those fixtures do not prove the rejected global interchange or the original unitary-embedding expression. The reviewed derivative and independent controls have separate receipts. The PSD oracle is the BR-35 procedure itself; every "PSD" verdict is re-verified by multiplying out $LDL^*$ and every "not PSD" verdict by evaluating $v^*Av$. Highlights: BR-33's three examples (equal-representative, CP-but-not-termwise, kernel obstruction); BR-34's irrational mixture, four-square rational mixture and irrational density; BR-36's $M_0$, eigenvalues $\tfrac{3\mp\sqrt3}6$, the ball identity $4\det\rho=1-\sum(6q_i-1)^2$ and five boundary points; BR-37's index formula, link product and Kraus-free normalization transport on a $2\to3\to3$ chain; BR-38's padded unitaries ($1\to2$, $2\to3$, complex with zero and dependent rows) and the $\tfrac13$-is-not-a-norm fact; BR-39's unit, swap, interchange and Choi descent; BR-40's isometry, pointer projections, state-update identity with a zero slot, and the pointer/block-projection coincidence.

Lean verification remains pending for all items.
