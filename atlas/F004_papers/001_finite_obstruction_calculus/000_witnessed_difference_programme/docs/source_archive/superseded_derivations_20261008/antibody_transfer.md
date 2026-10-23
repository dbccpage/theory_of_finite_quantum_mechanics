# Appendix Q — Antibody transfer: soundness, accumulation, and amortization

**New canonical rows.** The following are proposed rows for the unified ledger and require entry per §21.10 (claim identity: a reused ID must not absorb a strengthened quantifier). Nothing here enlarges the scope of the 154 existing rows; §Q.11 states the fences.

---

## Q.0 Which ingredients are standard, and what is actually new

Three of the four moves below are already in the monograph or are elementary, and I will not re-earn them:

- **(S1) Accumulation is set theory.** If $D_j\cap G=\varnothing$ for all $j$, then $\bigl(\bigcup_j D_j\bigr)\cap G=\varnothing$. This is the disjoint-union lemma; it is the whole content of the accumulation theorem's *safety* half, and it is standard.
- **(S2) The cost threshold is arithmetic.** $hv-Ng-C_0>0$ is one scalar comparison. No optimization is performed; the entire mathematical content of the threshold is the *model* in which $g,v,C_0,h$ are typed, not the inequality.
- **(S3) Image inclusion is fiber constancy.** The criterion "$\alpha(G_T)\subseteq G_S$" is the image-inclusion form of the lemma already proved as CH16-P02, §P.1, and Appendix K.1: a protected predicate descends through a map exactly when it is constant on the map's fibers, read one level up. Necessity is a one-line specialization.
- **(S4) Nonmembership certificates are already native.** CH04-P07 gives the weak duality $\langle y,\delta\rangle\le \Phi_{1,w}([\delta])$ for a circulation $y$ with $d_0^*y=0$ and $|y_e|\le w_e$. Every antibody in §Q.8 below is one line of that chain.

What is *not* standard and is contributed here: the typed binding discipline on $G_S$ and $G_T$ (§Q.1), the separation of the two quantifiers over rejections (§Q.2–Q.3), the repair-set failure inside the calculus itself (§Q.6.1), the four receipt kinds and their non-establishments (§Q.10), and the two-stage audit amortization (§Q.9.3). The calculus already insists that a diagnostic class is not a routing terminal (CH04-N01); an antibody is a *pre-filter*, and the transfer theorem below is a statement about typed sets, not about signatures or terminals.

---

## Q.1 Carriers: what $G_S$ and $G_T$ are

`WDP-CHQ-D01` **Definition (declared valid sets as evaluator data).** A *task* is a tuple
$$\mathfrak T=(\mathcal F,\ A,\ \mathbb F,\ \mathcal K,\ w,\ \varepsilon)$$
where $\mathcal F$ is the candidate carrier, $A\subseteq\mathcal F$ is the **declared admissible repair set** (the field $A_{\mathcal O}$ of CH10-D03), $\mathbb F$ the declared coefficient field, $\mathcal K$ the declared comparison family, $w$ the declared weight family, and $\varepsilon$ the declared terminalizer tolerance (CH10-N01). The **valid set** is
$$G_{\mathfrak T}:=\{x\in\mathcal F:\ x\text{ is accepted by the terminalizer of }\mathfrak T\}.$$

Two tasks $\mathfrak S,\mathfrak T$ with carriers $X$ and $Y$. The five fields are *task data*, and the binding list above is exactly the list the calculus already compiles in CH04-D01 and CH10-D03. Carriers are **realized images**: $G_S$ is the set of candidates that actually occur, not labels available to it. Appendix K.1's rule — unused target inputs destroy whole-target uniqueness — applies verbatim (§Q.4.2).

`WDP-CHQ-N01` **Nonclaim.** Nothing in this appendix identifies $G_S$ with a natural notion of correctness. $G_{\mathfrak T}$ is whatever the declared profile accepts; the transport question is entirely internal to the declared pair $(\mathfrak S,\mathfrak T,\alpha)$.

---

## Q.2 Antibodies, soundness, and the two quantifiers

`WDP-CHQ-D02` **Definition (antibody and transfer).** A **source antibody** is a pair $(D_S,\mathrm{cr}_S)$ with $D_S\subseteq X$ and a typed soundness certificate whose verdict is $D_S\subseteq X\setminus G_S$. For a declared adapter $\alpha:Y\to X$ the **transferred rejection** is
$$\alpha^{-1}(D_S)=\{y\in Y:\ \alpha(y)\in D_S\},\qquad\text{declared sound when } \alpha^{-1}(D_S)\cap G_T=\varnothing .$$

`WDP-CHQ-N02` **Typing fence.** A guard's verdict "reject" is a *pre-filter* result. It is not the evaluator's `Reject` status, not a `CounterexampleWitness` on the target, and not a routing decision (CH04-N01, CH04-O01). A target candidate that survives the guard still requires evaluation and terminalization by $\mathfrak T$'s own declared evaluator. Transfer of a *filter* is not transfer of a *terminal*.

**The generalization gap.** An antibody is normally *mined from a checked failure*. In the calculus the checked failure is a certificate pair $(f,y)$ with $\langle y,\delta\rangle=\|\delta-d_0f\|_{1,w}$ (CH04-P07); in the derivative demo it is one pair $(F,g)$ with $F'\ne g$. A **counterexample witness** (CH02 role 7) certifies a single inhabitant of a refuted universal claim. The antibody is a *closure* of that inhabitant under a declared predicate, and **the closure step is where soundness is lost.** The soundness certificate of an antibody must therefore be a `DualCertificateWitness` (CH02 role 5) — a separating functional — and not the `CounterexampleWitness` that motivated it. CH04-P07 is already in exactly this shape: one exhibited $\delta$ plus an annihilator certifies a whole family.

---

## Q.3 The sharp biconditional

`WDP-CHQ-P01` **Finite proposition (necessary and sufficient transfer condition).** For a total adapter $\alpha:Y\to X$,
$$\boxed{\ \Bigl[\ \forall D_S\subseteq X\setminus G_S:\ \alpha^{-1}(D_S)\cap G_T=\varnothing\ \Bigr]\ \iff\ \alpha(G_T)\subseteq G_S\ }$$

*Proof.* ($\Leftarrow$) Let $y\in\alpha^{-1}(D_S)\cap G_T$. Then $\alpha(y)\in D_S\subseteq X\setminus G_S$, while $\alpha(y)\in\alpha(G_T)\subseteq G_S$. Contradiction.
($\Rightarrow$) Suppose $\alpha(G_T)\not\subseteq G_S$; choose $y_0\in G_T$ with $x_0:=\alpha(y_0)\in X\setminus G_S$, and set $D_S=\{x_0\}$. This is a sound source rejection, and $\alpha^{-1}(D_S)\cap G_T\ni y_0$. $\square$

`WDP-CHQ-P02` **Finite proposition (per-antibody condition; the weaker statement).** For a *single* antibody $(D_S,\mathrm{cr}_S)$, transfer is sound exactly when
$$\alpha^{-1}(D_S)\cap G_T=\varnothing ,$$
which mentions $D_S$ and is implied by, but strictly weaker than, P01's condition.

`WDP-CHQ-P03` **Finite proposition (instance soundness certifies nothing about $\alpha$).** P02 does not imply P01's condition.

*Proof.* Work in the calculus; a symbolic instance is given in §Q.4.1. Fix the filled triangle of CH04-P08 over $\mathbb Q$ with $d_0f=(f_1-f_0,\ f_2-f_1,\ f_2-f_0)$ and $d_1x=x_{01}+x_{12}-x_{02}$. Let the **source** declare the repair set $A=\{0\}$, so $G_S=\{0\}$; let the **target** declare $A'=C^0(K;\mathbb Q)$, so $G_T=\operatorname{im}d_0$. Take $\alpha=\mathrm{id}$. Let $y=(1,1,-1)$ and $D_S=\{\delta:\ \langle y,\delta\rangle\ne0\}$.

$d_0^{*}y=0$: at vertex $0$ the net inflow is $-(y_{01}+y_{02})=-(1-1)=0$; at $1$ it is $y_{01}-y_{12}=0$; at $2$ it is $y_{12}+y_{02}=0$. So $y$ is a circulation and $D_S\subseteq X\setminus\{0\}=X\setminus G_S$ is sound. On the target, $\langle y,\delta\rangle=0$ iff $\delta\in(\mathbb Ry)^\perp=\operatorname{im}d_0=G_T$ — the annihilator of $\operatorname{im}d_0$ in $\mathbb Q^3$ is one-dimensional and is spanned by $(1,1,-1)$, so $\operatorname{im}d_0=(\mathbb Ry)^\perp$. Hence $\alpha^{-1}(D_S)\cap G_T=\varnothing$: this single antibody transfers soundly.

But $\alpha(G_T)=\operatorname{im}d_0\not\subseteq\{0\}=G_S$, so P01's condition fails. Concretely, $D_S'=\{(0,1,0)\}$ is a sound source rejection, and $(0,1,0)=d_0(0,1,0)\in G_T$ is rejected after transfer. $\square$

**Reading.** A guard is mined under pressure. The source in P03 rejects almost everything ($G_S$ is a point), so *any* rule — including the point rule above — is sound. The target rejects almost nothing. A certificate obtained under high rejection pressure carries no information about the target's valid set. **The repair set $A$ is a task binding, and it is the one most often dropped, because a guard is usually written as a predicate on fields and never as a predicate on fields-relative-to-a-declared-repair-space.** This failure is entirely internal to WDP's own typing: $A_{\mathcal O}$ is CH10-D03 profile data, and changing it is a *profile change*, not an evidential update (CH10-N01, §21.9).

---

## Q.4 The two quantifiers, and partial adapters

### Q.4.1 The quantified object differs

P01's left side ranges over **all** $2^{|X\setminus G_S|}$ subsets of the invalid source pool. Its right side mentions only $\alpha$, $G_S$, $G_T$ — no $D_S$ at all. The universal statement is therefore a property of the **adapter pair** and is *content-independent*: it certifies every antibody already mined and every antibody not yet conceived. The instance statement P02 is a property of the **antibody** and is content-specific. This is the whole reason the two must be kept apart:

- If you will reuse **one** antibody **once**, P02 is the cheaper and sufficient check.
- If you will reuse antibodies **repeatedly, or add more later**, P02 gives you no cumulative guarantee. Adding a second antibody requires a fresh P02 check whose difficulty is the same as the first, and a fresh certificate that composes with nothing.
- P01's certificate is *monotone in the antibody family*: it never expires as antibodies accumulate. This is the only artifact in the transfer calculus that amortizes over the antibody family.

### Q.4.2 Partial adapters: three obligations, not one

WDP adapters are partial (Appendix K.1), so let $\mathrm{dom}\,\alpha\subseteq Y$ be the declared domain. $\alpha^{-1}(D_S)=\{y\in\mathrm{dom}\,\alpha:\alpha(y)\in D_S\}$.

`WDP-CHQ-P04` **Finite proposition (three separate partial-adapter obligations).** For partial $\alpha$:

1. **Safety.** P01's condition $\alpha(G_T\cap\mathrm{dom}\,\alpha)\subseteq G_S$ and P02's condition $\alpha^{-1}(D_S)\cap G_T=\varnothing$ are stated on the domain and require no totality.
2. **Typing.** The transferred guard is well typed on all of $Y$ only if $G_T\subseteq\mathrm{dom}\,\alpha$, or if the complement is declared as a separate *unguarded stratum* with its own cost and its own audit.
3. **Economy.** A target candidate outside $\mathrm{dom}\,\alpha$ is never filtered, so $|Y_{\mathrm{pool}}\cap\mathrm{dom}\,\alpha|$ is an upper bound on the reachable kill count.

*Proof.* (1) is P01 with $G_T$ replaced by $G_T\cap\mathrm{dom}\,\alpha$. (2) and (3) are the definition of the preimage. $\square$

The point of separating (2) is that a guard which is *safe* on an ill-typed stratum is a trap: it returns "no rejection" for a candidate the pipeline has no way to interpret. This is Appendix K.1's "unused target inputs destroy whole-target uniqueness" in a new dress — a partial guard is a partial adapter, and the domain predicate is part of the certificate, not a footnote.

---

## Q.5 The calculus demo: $5x$, and what the transferable obligation actually is

### Q.5.1 The counterexample

Carrier $\mathcal F=\mathbb Q[x]$, validation functional $\partial = \mathrm{d}/\mathrm{d}x$ (total). Source task: declared integrand $g_S(x)=x$, $G_S=\{F:\partial F=x\}$. Target task: declared integrand $g_T=5$, $G_T=\{F:\partial F=5\}$. Adapter $\alpha=\mathrm{id}_{\mathcal F}$, task-data adapter $\bar\alpha=\mathrm{id}_{\mathbb Q}$.

- $(5x)'=5\ne x$, so $5x\notin G_S$; the checked failure is certified.
- $(5x)'=5=g_T$, so $5x\in G_T$.
- Hence $\alpha(G_T)=\{5x+c\}\not\subseteq G_S$: P01 fails, correctly.
- $D_S=\{5x\}$ is sound, and $\alpha^{-1}(D_S)\cap G_T=\{5x\}\ne\varnothing$: unsafe.
- $D_S=\{F:\ F'\ne x\}$ is *also* sound, and its transfer contains $5x$ since $(5x)'=5\ne x$: **also unsafe.**

### Q.5.2 The parameterized rule and its certificate

`WDP-CHQ-P05` **Finite proposition (task-parameterized transfer).** Let $\mathsf D_S,\mathsf D_T$ be the spaces of declared task data with valid families $G_S(d),G_T(e)$, and let $\bar\alpha:\mathsf D_T\to\mathsf D_S$. For each $e$,
$$\forall d:=\bar\alpha(e)\ \forall D_S\subseteq X\setminus G_S(d):\ \alpha^{-1}(D_S)\cap G_T(e)=\varnothing\ \iff\ \alpha(G_T(e))\subseteq G_S(d).$$

*Proof.* P01 applied pointwise in $e$ with the valid family held fixed at $G_T(e)$ and $G_S(\bar\alpha e)$. $\square$

The rule "$F'\ne g$" is a *predicate on (candidate, task-data) pairs*:
$$P_S(F,d):=[\ \partial F\ne d\ ].$$
Its transfer is $P_T(F,e):=[\ \partial(\alpha F)\ne\bar\alpha(e)\ ]$, and by P05 it is sound at $e$ **iff**
$$\forall F\in G_T(e):\quad \partial(\alpha F)=\bar\alpha(\partial F). \tag{$\star$}$$

`WDP-CHQ-D03` **Definition (adapter certificate / commutation law).** $(\star)$ is the **adapter certificate**: the declared adapter $\alpha$, together with the task-data adapter $\bar\alpha$, commutes with the declared validation functional on the realized image of $\partial$.

For $\alpha=\bar\alpha=\mathrm{id}$ on $\mathbb Q[x]$, $(\star)$ is $\partial F=\partial F$, discharged by uniqueness of the derivative — a single symbolic check, not a per-candidate computation. This is the structural payoff: **one commutation law, checked once, discharges the transfer obligation for every valid target candidate simultaneously, and simultaneously for every source guard invariant in the right way.** Compare P02, which requires a fresh certificate per antibody and can never be discharged once and for all.

### Q.5.3 The rule that is more transferable is the more fragile one

`WDP-CHQ-X01` **Counterexample (the certificate is checkable and still fails).** Let $\alpha=\pi_{\le k}$ be projection onto polynomials of degree $\le k$ (a declared adapter to a lower-degree source carrier) and $\bar\alpha=\mathrm{id}$. Then $(\star)$ reads $\pi_{\le k-1}\,\partial F=\partial F$ on the realized image, which fails for any $F$ with $\partial F$ of degree $k$ and nonzero top coefficient. So the sophisticated parameterized rule *fails the audit* on a degree-restricted target, while the crude point rule $\{5x\}$ passes the audit on the same carrier (it is a point and its image is itself).

*Proof.* Take $F=x^{k+1}$ with $k\ge1$ and target declared pool of degree $\le k+1$. Then $\partial(\pi_{\le k}F)=k\,x^{k}\cdot[\,k\le k\,]=kx^{k}$, wait — $\pi_{\le k}(x^{k+1})=0$, so $\partial(\pi_{\le k}F)=0$, while $\bar\alpha(\partial F)=(k+1)x^{k}\ne0$. So $(\star)$ fails at $F=x^{k+1}$, which lies in $G_T$ only if $g_T=(k+1)x^k$ is the declared integrand. Fix the declared integrand to $g_T=(k+1)x^{k}$ and the pool to degree $\le k+1$: then $x^{k+1}\in G_T$ and the rule "$F'\ne g_T$" would fire on it after transfer, while $5x$-style point rules are unaffected. $\square$

**Correction, stated explicitly.** The displayed calculation has $\pi_{\le k}(x^{k+1})=0$; a cleaner witness for $k\ge2$ is $F=x^{k}$ with declared integrand $g_T=kx^{k-1}$: $\pi_{\le k}F=x^{k}$ so $\partial(\pi_{\le k}F)=kx^{k-1}=\partial F$, and $(\star)$ *holds*. So the exact statement is: $(\star)$ fails exactly when the realized image of $\partial$ on the declared target pool meets degree $>k$, i.e. when $\max\deg(\partial F)>k$ over the declared pool. The repair is a **pool declaration** (declare the target pool to have degree $\le k+1$ or restrict $\mathfrak T$ so that $\partial F$ stays in range) — and that same declaration is already an input to the cost model in §Q.9. The honest moral is not "the rule is safe" but "**the rule's certificate is a joint statement about the adapter and the declared pool, and the pool declaration is load-bearing for safety and for cost alike.**"

`WDP-CHQ-N03` **Nonclaim.** Generalization strictly improves coverage and strictly increases transfer fragility. The audit detects the trade; it does not eliminate it. Neither the point rule nor the parameterized rule is universally preferable.

---

## Q.6 The counterexample families

### Q.6.1 Omitted task bindings (safety failures)

| Binding omitted | Instance | Binding that would have caught it | Certificate field |
|---|---|---|---|
| **Admissible repair set $A$** | Q-P03: $A=\{0\}$ vs. $A'=C^0$ on the same $d_0$ | $A$ recorded on both sides; audit run on $d_0A$ vs. $d_0A'$, not on $\operatorname{im}d_0$ twice | CH10-D03 field $A_{\mathcal O}$ |
| **$d_1d_0=0$ certificate** | Restriction system of CH16-P05 with $K\ne0$ | $d_1d_0=0$; without it $d_1$ is not class-invariant, so "reject $d_1\delta\ne0$" is a rule on no well-defined object | CH04-D01 certificate |
| **Coefficient field $\mathbb F$** | CH05-P06: $H^2(K;\mathbb Q)=0$, $H^2(K;\mathbb F_2)\ne0$ | declared field on both sides | CH04-D01 norm/field hypothesis |
| **Declared weights $w$** | CH04-P10: $\Phi_{1,w}$ and the saturated circulation depend on $w$ | $w$ and the capacity bounds $|y_e|\le w_e$ | CH04-P07 |
| **Task-data binding** | Q.5.1: "$F'\ne x$" bound to the source integrand | P05 / $(\star)$ | Q-D03 |
| **Adapter domain** | Q-P04(2) | $\mathrm{dom}\,\alpha\supseteq G_T$ or a declared unguarded stratum | Appendix K.1 domain predicate |
| **Terminalizer tolerance** | CH10-N01: a residual below $\varepsilon$ is accepted at one tolerance and rejected at another | $\varepsilon$ on both sides | CH10-D03 terminalizer |

The pattern is uniform: the calculus already types every one of these fields, and the transfer failure is a *silent substitution of defaults* rather than an illegitimate construction. The audit is therefore computable — it is a conjunction of seven recorded fields being present and matching.

### Q.6.2 Overly broad rules

`WDP-CHQ-X02` **Counterexample (unbound point rule).** "$D_S=\{5x\}$" is sound on $\mathfrak S$ and unsound on $\mathfrak T$ (Q.5.1). It fails P01, fails P02, and — independently — fails the cost threshold for every pool on which $h\le1$ (§Q.9.4). Safety and economy refute it for unrelated reasons, and per §D.3 the two refutations must be recorded in separate rows: a sound-but-uneconomic guard is not a refuted guard.

`WDP-CHQ-X03` **Counterexample (sound but vacuous — the efficiency face of "broad").** On $K$ the six-vertex projective-plane triangulation, the guard "reject any 2-cochain that is not a coboundary" is sound over both fields. Over $\mathbb Q$, $\operatorname{rank}_{\mathbb Q}\delta^1=10$ and $C^2$ has dimension 10, so $B^2=C^2$ and the guard rejects **nothing**: $h=0$, saving $=-Ng-C_0<0$. Over $\mathbb F_2$, $\operatorname{rank}=9$ and the single-triangle indicator is rejected: $h=1$. **Same guard, same declared configuration, $h=0$ or $h=1$ according to an undeclared field.** Safety is robust to the omission; economics is not.

`WDP-CHQ-X04` **Counterexample (rejecting a non-element).** CH04-N02: orthogonal projection of $\delta=(1,1,0)$ onto $\ker d_1$ returns the closed field $(1/3,1/3,2/3)$. A guard of the form "reject $\delta$ unless it is closed" is sound as a *detector of active closure failure*, but a rule "replace then check closedness" is not a repair and does not lower $\Phi_1$ from 2. Antibody rules, like repairs, must act on members of the declared carrier; a projection produces a different object and transfers nothing.

---

## Q.7 Safe accumulation

`WDP-CHQ-P06` **Finite proposition (conservative accumulation).** Let $(D_j,\mathrm{cr}_j)_{j\le k}$ be source antibodies each certified $D_j\subseteq X\setminus G_S$, and $\alpha$ declared. Then
$$G_T\cap\bigcup_{j=1}^{k}\alpha^{-1}(D_j)=\varnothing ,\qquad\text{hence}\qquad
G_T\ \subseteq\ Y\setminus\bigcup_{j=1}^{k}\alpha^{-1}(D_j)=:Y_{\mathrm{ret}} .$$
The retained set is the pool actually searched; every valid candidate survives.

*Proof.* (S1) applied with $G:=G_T$ to the soundly-transferred family: P02 gives $\alpha^{-1}(D_j)\cap G_T=\varnothing$ for each $j$; a union of sets disjoint from $G_T$ is disjoint from $G_T$. $\square$

`WDP-CHQ-P07` **Finite proposition (what accumulation does and does not deliver).** With $Y_{\mathrm{pool}}$ the declared candidate pool,
$$h=\Bigl|\Bigl(\bigcup_{j\le k}\alpha^{-1}(D_j)\Bigr)\cap Y_{\mathrm{pool}}\Bigr|\ \le\ \min\Bigl(|Y_{\mathrm{pool}}\setminus G_T|,\ \sum_{j\le k}|\alpha^{-1}(D_j)\cap Y_{\mathrm{pool}}|\Bigr).$$

*Proof.* The first bound: under P06 every element of the union is outside $G_T$. The second: $|\bigcup|\le\sum| |$ for finite families. $\square$

Three fences, stated as the theorem's conservatism:

- **Completeness is not delivered.** $Y_{\mathrm{ret}}$ is a superset of $G_T$ with no upper bound tighter than $Y$. Accumulation is a *soundness* theorem about a set.
- **Cheap search is not delivered.** $|Y_{\mathrm{ret}}|<|Y|$ is a cardinality statement. Turning it into a cheaper search requires a declared policy consuming the operation, witness, budget and stabilization evidence of CH04-O01. A guard is not a policy.
- **Per-antibody certificates must be checked against $G_S$, never against the running filter.**

`WDP-CHQ-N04` **Operational prohibition (incremental-check laundering).** Checking "$D_j$ contains no candidate surviving the filters $1,\dots,j-1$" is *strictly weaker* than $D_j\cap G_S=\varnothing$, and it launders the unsoundness of any earlier $D_i$ that already killed a valid candidate. Every certificate is checked against the **full** source valid set. This is the same discipline as CH04-P10 ("each pair is checked against CH04-P07 on its own") and §D.2, applied to guards.

---

## Q.8 Accumulation inside the calculus

`WDP-CHQ-D04` **Definition (calculus antibody).** In a window $\mathcal W$ with $d_1d_0=0$ and weighted $L^1$ (CH04-D02), a *circulation antibody* is a triple $(y,\ w,\ \mathrm{cr})$ with $y\in C^1$, $d_0^{*}y=0$, $|y_e|\le w_e$, and guard
$$G_y(\delta):=[\ \langle y,\delta\rangle\ne0\ ].$$

`WDP-CHQ-P08` **Finite proposition (soundness of the calculus antibody).** $G_y$ is sound on the task "is $\delta$ exact?", for the declared window, field and weights, and for the declared repair set $A$ — in particular for $A=C^0$ and for any $A$ whatever, since the argument never uses $A$.

*Proof.* For every admissible repair $f$, $\langle y,\delta\rangle=\langle y,\delta-d_0f\rangle$ because $\langle d_0^{*}y,f\rangle=0$. So $\langle y,\delta\rangle\ne0$ forces $\delta-d_0f\ne0$ for all $f\in A$, hence $\delta\notin d_0A=G$. $\square$

The certificate is precisely the pair $(d_0^{*}y=0,\ |y_e|\le w_e)$ — i.e. a `DualCertificateWitness` of the family, of the same type as the $(f,y)$ pair that CH04-P07 uses to certify $\Phi_1$. Worked instance, CH04-P08: $y=(1,1,-1)$ on the filled triangle with unit weights, $d_0^*y=0$, $\langle y,(1,1,0)\rangle=2\ne0$, guard fires; $d_0^*y=0$ and the capacity bounds are two three-term checks, against an evaluation that is a rational linear programme (CH04-C01) with slack variables, a two-phase simplex solve, and a dual replay. **$g\ll v$ by construction, and $h$ is a nonzero inner product rather than an LP optimum.**

Two observations that the calculus supplies for free and that the general theory must buy:

1. **Guard transfer and signature transfer are different claims.** The circulation guard transfers between the hollow and the filled triangle unchanged ($d_0$, $d_0^*$, and the weights are untouched), while the signature does not: $\Gamma_2$ goes $0\mapsto3$ and $R_{cl}$ is undefined in the hollow case. P01 is about sets; CH04-P05's bounds are about numbers; CH04-P12 is about implementations. Do not conflate them.
2. **The projection fallacy is an antibody fallacy.** CH04-N02's projection "repairs" a field by leaving its class; the analogous guard "reject unless projected-closed" is a rule about a non-element. P06's proof needs $\alpha^{-1}(D_j)\subseteq Y$; it breaks if the guard's output is manufactured.

---

## Q.9 Amortized benefit

### Q.9.1 The model

`WDP-CHQ-D05` **Definition (declared amortization model).** For a declared guard: setup cost $C_0\ge0$ covering mining (generalizing a checked failure into a predicate), certification (the `DualCertificateWitness`), adaptation (the adapter and the domain predicate), and lookup (indexing the guard); guard cost $g$ on each of $N$ declared candidates; evaluation cost $v$ on each surviving candidate; and $h$ sound early rejections, i.e. candidates removed before evaluation. The guard is assumed total and deterministic on the pool, so $g$ is paid $N$ times.

$$T_{\mathrm{bare}}=Nv,\qquad T_{\mathrm{guard}}=C_0+Ng+(N-h)v,\qquad \boxed{\ \mathrm{saving}=hv-Ng-C_0\ }$$

### Q.9.2 The exact threshold

`WDP-CHQ-P09` **Finite proposition (threshold, and its design corollaries).** Under D05, the guard pays its own way and more iff $h>h^{\star}$, where
$$h^{\star}=\frac{Ng+C_0}{v},\qquad\text{equivalently}\qquad \frac{h}{N}>\gamma:=\frac{g}{v}+\frac{C_0}{Nv}.$$

1. **$g<v$ is necessary.** If $g\ge v$ then $hv\le Nv\le Ng$ and $\mathrm{saving}\le-C_0<0$ for every $h$. A guard that costs at least as much as the evaluation it replaces can never amortize at any pool size.
2. **$C_0$ is amortized away.** For fixed $C_0$ and $g<v$, $\gamma\downarrow g/v$ as $N\to\infty$; a positive fraction of hits above $g/v$ suffices in the limit.
3. **The degenerate free case.** $C_0=g=0$ gives $\mathrm{saving}=hv>0$ for $h\ge1$. Cost, not soundness, is the scarce resource.
4. **The pool floor.** By P07, $h\le|Y_{\mathrm{pool}}\setminus G_T|$, so a *necessary* condition for a positive saving on a single antibody is $|Y_{\mathrm{pool}}\setminus G_T|\cdot v>Ng+C_0$. **A sound guard cannot pay for itself on a pool with too few invalids**, no matter how good the rule.
5. **Soundness is a feasibility condition, not a term in the objective.** Completeness loss is unpriced in D05. A cheap unsound guard minimizes $hv-Ng-C_0$ perfectly well and is worthless.

*Proof.* (1)–(3) are rearrangements. (4) is P07's first bound. (5) is the observation that D05's $h$ counts only candidates that *may* be rejected; an unsound transfer inflates the count with valid candidates at zero marginal cost. $\square$

### Q.9.3 Two-stage audit, and what to trust about $h$

`WDP-CHQ-P10` **Finite proposition (audit amortization and the asymmetry of $h$ estimates).** Let $c$ be the cost of a source soundness check ($D_j\cap G_S=\varnothing$) and $c'\ge c$ the cost of a transfer check ($\alpha^{-1}(D_j)\cap G_T=\varnothing$, which reads $D_j$, $\alpha$ and $G_T$). Let $C_{\alpha}$ be the cost of one adapter audit, whose certificate $\alpha(G_T)\subseteq G_S$ mentions no antibody. Then
$$C_{\alpha}+kc\le kc'\quad\iff\quad k\ \ge\ \frac{C_{\alpha}}{c'-c}.$$
Above that threshold, audit first; below it, per-antibody checking is cheaper.

*Proof.* Direct rearrangement. $c'\ge c$ because the transfer certificate is a conjunction containing the source certificate. $\square$

`WDP-CHQ-N05` **Falsifier for source-side measurement.** A hit rate measured on the source pool does not estimate the target's. In Q-P03 the source's invalid fraction tends to $1$ while the target's is $1/\mathbb Q^3$ complement of a 2-plane, i.e. $1/3$; the source overstates the target's kill rate by a factor of 3, and P01's audit — being a *safety* certificate — does not notice. A declared **lower** bound on $h$ justifies installing the guard; an upper bound on $h$ only bounds the loss from having installed it wrongly. The two are not interchangeable, and pessimistic-in-the-safe-direction here means *under*-estimating the kill count. A transport of hit rates from $\mathfrak S$ to $\mathfrak T$ is a separate declared obligation, of the same family as the finite-sample tolerance of Appendix J.5 and the trial-protocol requirements of §9.9 — a declared distributional bridge, not a corollary of the audit.

### Q.9.4 A worked threshold

$N=10^{4}$ candidates, $v=1$ (one full verification pass), $g=10^{-3}$ (one differentiation or one inner product), $C_0=2$. Then $\gamma=1.2\times10^{-3}$: **the guard pays once it fires on more than 12 of 10,000 candidates.**

- The parameterized guard "$F'\ne g$" on a calculus pool of degree-$\le4$ rational fields with random-ish rational integrands: $h/N$ is of order $1$; $\mathrm{saving}\approx10^{4}-12\gg0$.
- The point rule $\{5x\}$: $h\le1$ always, so $\mathrm{saving}\le1-12=-11<0$ on *every* pool. It never pays, independent of the transfer failure in Q.5.1.
- The vacuous $\mathbb Q$-exactness guard of Q-X03: $h=0$, $\mathrm{saving}=-12$. It is sound and worthless, and the two facts belong in separate ledger rows.

---

## Q.10 Receipts

Following §15.6 and §D.3 (eight distinct pointers, none standing in for another), transfer uses four receipt kinds:

1. **Source soundness receipt** — subject $(X, D_j)$; declared $\mathfrak S$ with all five bindings of Q-D01; verdict $D_j\subseteq X\setminus G_S$; verifier. *Does not establish:* anything about $\mathfrak T$, $\alpha$, or cost.
2. **Adapter audit receipt** — subject $(\mathfrak S, \mathfrak T, \alpha)$; verdict $\alpha(G_T)\subseteq G_S$; verifier by finite exhaustion over $G_T$ when $G_T$ is finitely enumerable, or by a *generator plus generation law* when $G_T$ is declared generated (e.g. "$H+c$ for $H$ an antiderivative of $g$": check the generator, then the transport equivariance law). *Does not establish:* that any particular antibody is a source-validity rule, or that any particular rejection fires.
3. **Binding receipt** — subject $(\partial,\alpha,\bar\alpha, Y_{\mathrm{pool}})$; verdict $(\star)$ on the realized image; verifier by exact symbolic computation. *Does not establish:* that the pool is the pool the guard will meet in production, nor that the target-side integrator is the declared $\partial$.
4. **Accumulation receipt** — verdict $G_T\subseteq Y_{\mathrm{ret}}$, *re-derived* from the constituent source receipts against the full $G_S$ (N04 forbids incremental re-checking). *Does not establish:* completeness, search efficiency, or a routing policy.
5. **Cost receipt** — the five numbers of D05 with $h$ measured on a *named* pool or bounded by a declared argument, plus the inequality of P09. *Does not establish:* that the model is the right model, that $h$ transports to another pool (N05), or that the guard is sound.

All five are `Mechanized elsewhere` or `finite proposition` rows at their own scopes. None is `Proved` about $\mathfrak T$'s mathematics, and none confers standing (CH15-N01, CH00-N03).

---

## Q.11 Falsifiers, nonclaims, and the session map

**Falsifiers for this appendix.** Q-P01 fails if a sound $D_S\subseteq X\setminus G_S$ is exhibited with $\alpha^{-1}(D_S)\cap G_T\ne\varnothing$ while $\alpha(G_T)\subseteq G_S$ is claimed. Q-P06 fails if a $y\in G_T$ is exhibited in $\bigcup_j\alpha^{-1}(D_j)$ from certificates each verified against the full $G_S$. Q-P08 fails if a field $\delta\in d_0A$ is exhibited with $\langle y,\delta\rangle\ne0$ under a verified $d_0^*y=0$ and $|y_e|\le w_e$. P09(1) fails if a guard with $g\ge v$ exhibits positive saving.

**Nonclaims.** (N01) $G_{\mathfrak T}$ is not a natural notion of truth. (N02) A guard's "reject" is not an evaluator status, a target counterexample, or a routing decision. (N03) Generalization is not free: better coverage, worse transfer fragility. (N04) Incremental checking is not sound. (N05) Source-side hit rates do not transport. (N06) A transfer certificate says nothing about whether a rule *helps*; soundness and amortization are independent rows and are reported separately. (N07) Nothing here supplies authority, or selects a mathemophysics.

**Three levels of "reuse," with three distinct certificates.** Across candidates: $D\cap G=\varnothing$, one check, no adapter. Across tasks: the audit of P01 plus the source receipt. Across implementations: a **port** certificate on the exact predicate *including its parameter binding* — porting rule *text* is not porting the *guard*, and the omission-of-binding failure recurs — plus a **re-price** of $g$, since guard cost is implementation-dependent. A port to a different carrier is a new adapter and therefore a new audit. And a port may be sound while being uneconomic.

**Audit reuse is monotone, and only in one direction.** If $G_T'\subseteq G_T$ (a declared restriction of the audited target) or $G_S'\supseteq G_S$ (an enlargement of the source valid set, e.g. a more permissive declared repair set), then $\alpha(G_T')\subseteq G_S\subseteq G_S'$ and the audit carries. This is the one genuinely conservative reuse rule for the *audit artifact* itself, and it is a one-line check against the seven binding fields. Arbitrary adaptation of the task in any other direction requires a fresh audit. Note the tension with Q-P03: the target there has a *larger* valid set, so the audit cannot be reused, while the single parameterized guard happens to remain sound — generalization bought coverage with fragility, as in Q-N03.

**Session acceptance map.** Necessary-and-sufficient transfer conditions: Q-P01 (total, sharp), Q-P05 (task-parameterized), Q-P04 (partial, three obligations); per-antibody weakness isolated in Q-P02 and refuted as a transfer guarantee in Q-P03. Conservative accumulation: Q-P06 with the three fences of Q-P07, the incremental-check prohibition N04, and the calculus instantiation Q-P08. Exact cost threshold: Q-P09 with the threshold $h^{\star}=(Ng+C_0)/v$, the four corollaries, the two-stage audit bound Q-P10, and the mis-estimated-$h$ prohibition N05. Counterexamples for omitted task bindings: Q-X01 and the seven-row table in Q.6.1, anchored on the repair-set instance Q-P03 and the calculus instances CH16-P05, CH05-P06, CH04-P08, CH04-N02. Counterexamples for overly broad rules: Q-X02 (unbound point rule, refuted twice for unrelated reasons), Q-X03 (sound but vacuous), Q-X04 (rejecting a non-element).

**What is not established.** Q-X01's degree calculation in its first form was wrong and is corrected in place; the corrected statement still exhibits a real failure, and the correction is the more useful lesson — the certificate is a joint statement about adapter *and* declared pool. No claim is made that the audit is computable in general: it is computable when $G_T$ is finitely enumerable or finitely generated with a checkable law, and *not* otherwise. No claim is made that the retained set is cheaply searchable, that a rejected field is repaired, or that any of these certificates survive a change of profile beyond the monotone direction above.