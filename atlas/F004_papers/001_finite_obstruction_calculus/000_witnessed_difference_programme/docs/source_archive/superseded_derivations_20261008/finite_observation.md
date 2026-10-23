# §14.6 — Minimum‑cost sufficient suites

*This section closes the operational question left open at the end of §14.4 ("a suite that is injective on $Y$ costs at least the sum of the $\dim Y$ cheapest probes") and at the nonclaim `WDP-CH14-N02` ("does not select, price, or authorize a sensor suite"). It prices; it does not license.*

**Scope of the new material.** Everything below is finite, exact, and conditional on a *declared* price function. It adds no physical instrument, no probability model, no authority, and no formalization credit. The starting points are §14.4 (capacity and recovery on a declared subspace), Appendix K.1 (the necessary‑and‑sufficient adapter criterion: fiber constancy), and Appendix P.1 (the factorization criterion $q=\bar q\circ p$ with uniqueness on the realized image). The new content is (i) the *cost* minimization, (ii) an *integer* optimality certificate, (iii) the *adaptive* recursion with its well‑foundedness, and (iv) the feasibility dichotomy with an explicit indistinguishable pair.

---

## 14.6.1 The priced instance

`WDP-CH14-D02` **Definition (priced instance).** A priced instance is a tuple

$$\mathfrak{P}=\bigl(X,\;p:X\to P,\;q:X\to A,\;\mathcal I=(m_i,c_i)_{i\in I},\;c_i\in\mathbb Q_{>0}\bigr),$$

with $X$ finite, $P,A,M_i$ finite, and $m_i:X\to M_i$. The index set $I$ is finite. The triple $(X,p,q)$ is the *question*; $\mathcal I$ is the *instrument shelf with prices*. $p$ is what the observer already sees. Prices are data: the calculus does not determine them (`CH15-N01`, `CH03-D01` injection ledger).

**Sufficiency.** A subset $S\subseteq I$ is **sufficient** when

$$p(x)=p(y),\quad m_i(x)=m_i(y)\ \forall i\in S\ \Longrightarrow\ q(x)=q(y).\tag{1}$$

**Unresolved pairs.** Put

$$\mathcal U=\bigl\{\{x,y\}:x,y\in X,\ p(x)=p(y),\ q(x)\ne q(y)\bigr\}.$$

Since $q(x)\ne q(y)$ forces $x\ne y$, every member of $\mathcal U$ is a genuine two‑element subset; no quotient by symmetry is needed. The *report* $p$ enters only here: it removes pairs that the observer has already settled.

---

## 14.6.2 Sufficiency is exactly coverage of $\mathcal U$

`WDP-CH14-P04` **Finite proposition (sufficiency = pair coverage; transversals).** For a subset $S\subseteq I$ define the *distinction set*

$$D_i=\bigl\{\{x,y\}\in\mathcal U:\ m_i(x)\ne m_i(y)\bigr\}.$$

Then (1) holds **iff** $\mathcal U\subseteq\bigcup_{i\in S}D_i$. Consequently:

1. $S$ is sufficient **iff** $S$ meets every $D_i$, i.e. **iff $S$ is a transversal (hitting set) of the hypergraph $\mathcal H=(I,\{D_i\})$**.
2. Sufficiency is monotone in $S$; the sufficient suites are exactly the transversals, and the *inclusion‑minimal* sufficient suites are exactly the minimal transversals.
3. The verification of (1) for a given $S$ is the finite computation $D(u)\ne\emptyset$ for all $u\in\mathcal U$, where $D(u)=\{i\in S:u\in D_i\}$.

*Proof.* ($\Rightarrow$) If $\mathcal U\not\subseteq\cup_{i\in S}D_i$, take $\{x,y\}\in\mathcal U$ outside the union. Then $p(x)=p(y)$ and $m_i(x)=m_i(y)$ for all $i\in S$, while $q(x)\ne q(y)$: (1) fails. ($\Leftarrow$) Suppose (1) fails. Then $p(x)=p(y)$, $m_i(x)=m_i(y)$ for all $i\in S$, $q(x)\ne q(y)$; so $\{x,y\}\in\mathcal U$ and $u\notin D_i$ for all $i\in S$, contradicting the covering. Item 2 is the elementary property of transversals. Item 3 is immediate. $\square$

This is precisely the fiber‑constancy criterion of `WDP-CH16-P02` / Appendix K.1 §K.1 / Appendix P.1 §P.1, applied to the **augmented report** $r_S:=(p,(m_i)_{i\in S})$: a decoder $\bar q$ on the realized image of $r_S$ exists exactly when $r_S$ is constant‑on‑$q$‑fibers. The proof of the "only if" direction is the one‑line substitution; the "if" direction assigns each realized joint report the value of any preimage. Uniqueness on the realized image is P.1's, and is not needed below.

**This answers the "necessary and sufficient" half of the operational question exactly:** the additional observations that are both necessary and sufficient are the transversals of $\mathcal H$; the cheap ones are its minimal transversals, priced.

`WDP-CH14-P04b` **Finite proposition (monotonicity in the visible report).** If $p'$ is a coarsening of $p$ ($p'(x)=p'(y)\Rightarrow p(x)=p(y)$), then $\mathcal U(p)\subseteq\mathcal U(p')$, so every $p$‑sufficient suite is $p'$‑sufficient. Hence the optimum value is non‑decreasing under coarsening of $p$ and non‑increasing under refinement.

*Proof.* Inclusion of the pair sets, then $\mathcal H$ for $p'$ has the same vertices and a family of $D_i$'s each containing the $p$‑one; a transversal of the smaller hypergraph family may miss a larger $D_i$. Sufficiency for $p$ implies sufficiency for $p'$ by (1) directly. $\square$

So the drop $c^*_{fix}(p)-c^*_{fix}(p')$ is the **exact price of the extra visible report** $p'$ over $p$ — an exactly computable, non‑speculative quantity.

---

## 14.6.3 The fixed price, and why an LP relaxation does not certify it

Define

$$c^*_{fix}(\mathfrak P)=\min\bigl\{c(S):=\textstyle\sum_{i\in S}c_i:\ S \text{ sufficient}\bigr\}.\tag{2}$$

`WDP-CH14-P05` **Finite proposition (the value is a minimum-weight transversal; the LP is only a lower bound).** Let $A\in\{0,1\}^{\mathcal U\times I}$ be the incidence matrix of the $D_i$. The set‑cover relaxation

$$\tau=\min\{\,c^\top z:\ Az\ge\mathbf 1,\ z\ge0\,\}\qquad\text{dual}\qquad
\max\{\ \mathbf 1^\top y:\ A^\top y\le c,\ y\ge0\ \}$$

satisfies $\tau\le c^*_{fix}$, with strict inequality possible; and $c^*_{fix}$ is attained, is a nonnegative rational, and is not characterized by $\tau$ in general.

*Proof.* A feasible $z$ of value $\tau$ randomized round gives $\tau\le c^*_{fix}$; equivalently, for any sufficient $S$ take $z=\mathbf 1_S$. Attainment and rationality: $2^{|I|}$ subsets, finitely many, costs rational. Strictness: see the Fano instance of §14.6.4 below, where $\tau=7/3$ and $c^*_{fix}=3$. $\square$

The operational rule this licenses is narrow and worth stating bluntly: **a primal–dual LP pair certifies the integer optimum only when its common value equals the certified value of a feasible integer suite.** A dual vector $y$ is a certificate for $c^*_{fix}$ exactly when $\mathbf 1^\top y = c(S)$ for a verified feasible $S$.

### An integral lower‑bound object that does certify

`WDP-CH14-P05b` **Finite proposition (integral packing certificate).** Let $u_1,\dots,u_r\in\mathcal U$ be such that the index families $\{i\in I: u_j\in D_i\}$ are pairwise disjoint over $j$. Then every sufficient suite contains $r$ distinct measurements and

$$c^*_{fix}\ \ge\ \sum_{j=1}^{r}\ \min\{c_i:\ u_j\in D_i\}.$$

*Proof.* A sufficient suite meets each $D_i$‑of‑$u_j$ (that is, contains some index covering $u_j$). If one index covered $u_j$ and $u_\ell$ with $j\ne\ell$, the two families would meet; so the $r$ chosen indices are distinct. Minimizing each term independently gives the bound. $\square$

This is the integer dual of (2) restricted to disjointly‑supported packings. It is a genuine replayable certificate — and it, too, is not universally tight (the 3‑edge star: universe $\{a,b,c\}$ (centre $c$), sets $\{c,a\},\{c,b\}$; the integer optimum is $2$, the best packing bound is $1$). Neither object dominates the other.

### A self-contained family with a persistent gap

`WDP-CH14-P05c` **Finite proposition (complete‑graph family).** Let $\mathcal U$ be the edge set of $K_n$ ($n\ge3$) and let $D_v$ be the $n-1$ edges at vertex $v$, with all costs $1$. Then $c^*_{fix}=n-1$ while $\tau\le n/2$, so $c^*_{fix}/\tau\ge 2(n-1)/n\to2$.

*Proof.* A transversal is a vertex cover. If $|S|\le n-2$ two vertices lie outside $S$, and the edge between them is uncovered; the $n-1$ vertices other than one form a cover. For the relaxation, $z_v=\tfrac12$ satisfies every edge constraint with equality and has value $n/2$. $\square$

We prove no general gap theorem and claim no constant‑factor relation: the exact integer value is obtained by the declared procedure below.

### Certificate bundle and terminating procedure

`WDP-CH14-D03` **Definition (price certificate).** A price certificate for a claim $\widehat c = c^*_{fix}(\mathfrak P)$ is a pair $(S,\Lambda)$ where $S\subseteq I$ is a **cover witness** and $\Lambda$ is a **lower‑bound witness** of one of four types:

* **(P) cover map** $w:\mathcal U\to S$ with $u\in D_{w(u)}$ for all $u$ — a finite object of size $|\mathcal U|$, verified by lookup;
* **(D1) integral packing** $u_1,\dots,u_r$ with pairwise‑disjoint index families, plus the per‑element minimum costs;
* **(D2) residual‑counting prune**: at a node of a branch‑and‑bound search, $n$ pairs remain uncovered and every unselected measurement covers at most $k$ of them, so at least $\lceil n/k\rceil$ further measurements are required, at total cost at least the sum of the $\lceil n/k\rceil$ cheapest unselected prices;
* **(D3) matching LP pair** $z,y\ge0$ with $Az\ge\mathbf 1$, $A^\top y\le c$, $c^\top z=\mathbf 1^\top y=\widehat c$ (weak duality verified line by line, as in Appendix J.5).

`WDP-CH14-P05d` **Finite proposition (acceptance rule, terminating procedure).** The reference procedure *BuildCover–Decide* is:

1. compute $D_i$ for every $i\in I$ and $\mathcal U$ (time $O(|\mathcal U|\sum_i|M_i|)$, all exact);
2. if $\mathcal U=\emptyset$, return $S=\emptyset$, $\widehat c=0$ — done;
3. run branch‑and‑bound over subsets of $I$ with prunes (D2) and the packing bound (D1), emitting at each prune the two integers $n,k$ used;
4. return $(S^*,\Lambda^*)$ with $c(S^*)=\Lambda^*$.

It terminates, because the search space is $2^{|I|}$ and each node either is expanded or is pruned by a check that is pure finite arithmetic. The procedure is auditable: a replayed run needs only the instance, $S^*$, $\Lambda^*$, and a verifier of items (P) and (D1)–(D3).

**Acceptance.** $(S,\Lambda)$ is accepted iff the cover check passes on every $u\in\mathcal U$, $\Lambda$ verifies, and $c(S)=\Lambda$'s value. Rejection is structured, never a bare `false`: `NotSufficient` (with a witness $u$ having $D(u)=\emptyset$), `UpperLowerMismatch` (with both values), or `CertificateInvalid` (with the failing field). This mirrors the validation discipline of §G.5 and the tamper‑test discipline of §D.2.

`WDP-CH14-P05e` **Finite proposition (realization).** Every finite set system $(\mathcal U,\{D_i\}_{i\in I})$ of positive‑rational costs is the distinction system of a priced instance with a constant report and a two‑valued question. Specifically: let $X=\{*\}\sqcup\mathcal U$, $p\equiv*$, $q(*)=0$, $q(u)=1$, and $m_i(*)=0$, $m_i(u)=\mathbf 1_{D_i}(u)$. Then $\mathcal U(\mathfrak P)=\{\{*\,,u\}:u\in\mathcal U\}$ and $D_i$ as given.

*Proof.* Pairs inside $\mathcal U$ have $q=1=1$; $*\,,*$ is diagonal; $\{*\,,u\}$ is the only kind with $q$ unequal; and $m_i$ separates it iff $u\in D_i$. $\square$

This is a reduction of (2) *to* minimum‑weight set cover. We do **not** claim hardness, and we claim no polynomial‑time exact procedure; `CH21-F` style: any efficiency claim requires its own evidence.

---

## 14.6.4 Worked fixed instance: the Fano plane, where the LP fails

Let $F$ be the seven points and $\ell_1,\dots,\ell_7$ the seven lines of the Fano plane. Set $\mathfrak P=\bigl(\{*\}\cup F,\ p\equiv*,\ q(*)=0,\ q(f)=1,\ (m_\ell,\ 1)_\ell\bigr)$ with $m_\ell(*)=0$, $m_\ell(f)=\mathbf 1_{\{f\in\ell\}}$ (CH14‑P05e). Then $|\mathcal U|=7$ and $D_\ell=\{\{*\,,f\}:f\in\ell\}$.

**Optimal suite.** Three concurrent lines $\ell_1,\ell_2,\ell_3$ through a point $P$. By inclusion–exclusion on the three pairwise intersections (all equal to $P$),

$$|\ell_1\cup\ell_2\cup\ell_3|=9-3+1=7=\lvert F\rvert ,$$

so $\mathcal U\subseteq D_{\ell_1}\cup D_{\ell_2}\cup D_{\ell_3}$: $c^*_{fix}\le 3$.

**Optimality certificate.** (D2) at the root: $n=7$ uncovered, every line meets $F$ in exactly $3$ points, so $k=3$ and

$$c^*_{fix}\ \ge\ \lceil 7/3\rceil\cdot 1=3 .$$

Combined: $c^*_{fix}=3$. Both halves are one‑line checks. Two natural relaxations, by contrast, both fail here:

* **LP:** each point lies on $3$ lines, so $z\equiv\tfrac13$ is feasible and $y\equiv\tfrac13$ is dual feasible, both with value $7/3<3$.
* **Integral packing (D1):** in the Fano plane any two points lie on a common line, so no two‑element packing exists; the bound is $1$.

So in this instance neither relaxation certifies the integer optimum, and a *two‑line counting argument* is required. That is the precise content of "an LP relaxation alone does not certify the integer optimum."

---

## 14.6.5 Adaptive observation: the exact recursion

A **strategy** $\sigma$ for a candidate set $C\subseteq X$ (always $C\subseteq p^{-1}(p(x))$ for some $x$) is a decision tree whose nodes are labelled by pairs $(i,a)$ with $a\in m_i(C)$ and whose leaf sets are the reached $C$‑fibers. It is **correct on $C$** if $q$ is constant on every leaf set. Its cost at $x$ is $c(\sigma)=\sum_{i\ \text{asked on }x\text{'s path}}c_i$, and its worst case is $W(\sigma)=\max_{x\in C}c(\sigma(x))$.

For $C\subseteq X$ let

$$U_C=\bigl\{\{x,y\}\subseteq C:\ q(x)\ne q(y)\bigr\},\qquad
J(C)=\bigl\{i\in I:\ |m_i(C)|\ge2\bigr\},\qquad
J^*(C)=\bigl\{i\in I:\ D_i\cap U_C\ne\emptyset\bigr\}.$$

Note $J^*(C)\subseteq J(C)$: a measurement that separates some $q$‑different pair certainly splits $C$.

`WDP-CH14-P06` **Finite proposition (the exact worst‑case recursion).** With $V(C)=0$ when $q$ is constant on $C$ and

$$V(C)=\min_{i\in J^{*}(C)}\ \Bigl[\ c_i+\max_{a\in m_i(C)}V\bigl(C\cap m_i^{-1}(a)\bigr)\ \Bigr] \tag{3}$$

when $q$ is not constant on $C$, and with $V(C)=+\infty$ when $q$ is not constant on $C$ and $J(C)=\emptyset$:

1. **(3) is the true optimum.** $V$ is the infimum of $W(\sigma)$ over correct strategies.
2. **Well‑foundedness.** Every argument of $V$ on the right is a proper subset of $C$, so the recursion terminates. Depth is at most $\min(|C|-1,\,|I|)$, since a measurement is never usefully repeated.
3. **Why the minimum runs over $J^*(C)$** (the "only splitting measurements" restriction, and something stronger than it). Let $\sigma$ be an optimal strategy and let $i$ be its first measurement.
 * If $i\notin J(C)$, then $C$ reaches a single branch whose remaining candidate set is again $C$; deleting the step leaves a correct strategy, so $\sigma$ was not optimal because $c_i>0$. **This is exactly where $c_i>0$ is load‑bearing.**
 * If $i\in J(C)\setminus J^*(C)$, then $D_i\cap U_C=\emptyset$, so the step resolves no $q$‑different pair; again deletion is strictly cheaper. Hence $i\in J^*(C)$.
 * If $i\in J^*(C)$, the branch strategy on $C\cap m_i^{-1}(a)$ must itself be optimal, or the whole strategy improves.
4. **A typing warning on the unrestricted form.** The recursion with $\min$ over *all* $i$ is **not well‑founded in $|C|$**: a non‑splitting $i$ re‑enters the same subproblem. It is nevertheless *equivalent*, because the term for such an $i$ is $c_i+V(C)\ge V(C)$, and item 1 already exhibits a strategy of value $V(C)$ using only splitting measurements. The correct published form is (3) (or the split‑only form); the all‑$i$ form should not be quoted as a recursive definition.
5. **Monotonicity.** $C'\subseteq C\Rightarrow V(C')\le V(C)$ whenever $V(C)<\infty$, by restricting an optimal strategy on $C$.
6. **Rationality and computability.** $V(X)\in\mathbb Q_{\ge0}$ when finite, and $V$ is computed by memoization over subsets of $X$ in time $O(2^{|X|}\cdot|I|\cdot|X|)$.

*Proof.* (1),(3) by induction on $|C|$: the base case is $q$ constant. (2) Immediate from (1): $i\in J^*(C)$ means $C\cap m_i^{-1}(a)$ is a proper subset for every $a\in m_i(C)$, and a repeated measurement yields the same $C$‑fiber as before, so an optimal tree is simple. (5) Run $\sigma$ on $C'$; each node's candidate set is a subset of the corresponding $C$‑set, leaves stay $q$‑constant, and the cost is not increased. (6) Finitely many strategies with rational costs; the min is attained. The $V(C)=+\infty$ case is handled in P07 below. $\square$

**Comparison with the fixed price.**

`WDP-CH14-P06b` **Finite proposition ($V\le c^*_{fix}$; the gap is the price of non‑adaptivity).** If $\mathcal U\ne\emptyset$ and $c^*_{fix}<\infty$, then $V(X)\le c^*_{fix}$. Hence

$$\underbrace{c^*_{fix}-V(X)}_{\text{price of committing to a non-adaptive suite}}\ \ge 0 ,$$

and the *adaptive* answer is never more expensive than the best *fixed* answer.

*Proof.* Take an optimal sufficient suite $S^*$. The strategy "ask the members of $S^*$ in any order, stopping as soon as $q$ is constant on the current $C$" is correct on $X$ and costs at most $c(S^*)$. $\square$

**The operational "what next?" rule.** Once the memo table $\{V(C)\}$ over reachable $C$ is filled, the exact cheapest next inspection from a candidate set $C$ is

$$\arg\min_{i\in J^*(C)}\Bigl[\,c_i+\max_{a\in m_i(C)}V\bigl(C\cap m_i^{-1}(a)\bigr)\,\Bigr],\qquad \text{price }V(C).\tag{4}$$

This is a decision procedure, not a heuristic. A greedy "buy the measurement with the best immediate reduction per unit price" rule is **not** claimed optimal — the source audit (§Appendix C) explicitly rejects 035's greedy‑optimality claim — and (4) supersedes it.

*Scope fence.* If a declared prior on $C$ replaces the max by a $\sum_a \Pr(a\mid C)$, the recursion becomes an expected‑cost value. That requires a declared stochastic model and inherits every fence of §9.1 and §9.10; nothing in this section selects a probability reading of the finite carrier.

---

## 14.6.6 Feasibility, and the explicit indistinguishable pair

`WDP-CH14-P07` **Finite proposition (resolvability, and the witness pair).** Define the joint indistinguishability

$$x\equiv y \iff p(x)=p(y)\ \text{and}\ m_i(x)=m_i(y)\ \ \forall i\in I .$$

Then:

1. $q$ is resolvable on $X$ by *some* strategy (equivalently, $\exists S$ sufficient, equivalently, $c^*_{fin}<\infty$, equivalently, $V(X)<\infty$) **iff** $q$ is constant on every $\equiv$‑class, **iff** $\mathcal U=\emptyset$ is false precisely when $\bigcup_{i\in I}D_i=\mathcal U$.
2. If not resolvable, the procedure *Classify* returns an explicit pair: compute the join partition of $\{p,m_i\}_{i\in I}$ on $X$, and on any class on which $q$ is not constant return the first two members. That pair $(x,y)$ satisfies $m_i(x)=m_i(y)$ for all $i$ and $q(x)\ne q(y)$.
3. **Adaptivity buys cost, never feasibility:** a strategy resolves the question iff the *whole shelf* $\mathcal I$ is sufficient.

*Proof.* (1) ($\Leftarrow$) The full family is sufficient, so the fixed strategy "ask all" resolves. ($\Rightarrow$) Suppose some strategy $\sigma$ resolves $X$. Fix $x$ and let $C$ be its leaf set; $C$ lies inside a $\equiv$‑class $E$ (a leaf is an intersection of $p$‑fibers and $m_i$‑fibers). $q$ is constant on $C$ by correctness; and $q$ is constant on $C\subseteq E$ forces $q$ to take at most one value on $E$ only if $E=C$… in general, take any $\equiv$‑pair $(y,z)$: both lie in the same fiber of every measurement ever asked, hence in the same leaf, hence $q(y)=q(z)$. So $q$ is constant on $E$. (2) is the algorithm. (3) is (1). $\square$

*Miniature unresolvable instance.* $X=\{1,2,3\}$, $p\equiv*$, $q(1)=0$, $q(2)=1$, $q(3)=0$; shelf $\{m_1,m_2\}$ with $m_1=m_2=(0,0,1)$, costs $1,1$. Then $D_1=D_2=\emptyset$, $\mathcal U=\{\{1,2\}\}$, $\equiv$ has a non‑$q$‑constant class, and the procedure returns the witness pair $(1,2)$ with $m_i(1)=m_i(2)$ for all $i$ and $q(1)\ne q(2)$. The reported price is $+\infty$, not a large number: a refusal is not a quantity.

---

## 14.6.7 Worked adaptive instance: adaptation is strictly cheaper

Take the priced instance below (all values exact; $q(x)=\lceil x/2\rceil$; $p\equiv*$; $U=\{*\}$).

| $i$ | $m_i(1)$ | $m_i(2)$ | $m_i(3)$ | $m_i(4)$ | $m_i(5)$ | $m_i(6)$ | $m_i(7)$ | $m_i(8)$ | $c_i$ | $D_i\cap\mathcal U$ |
|---|---|---|---|---|---|---|---|---|---|---|
| $A$ | 0 | 1 | 0 | 1 | 0 | 0 | 1 | 1 | $1$ | $\{G_1G_3,\,G_1G_4,\,G_2G_3,\,G_2G_4\}$ (16) |
| $B$ | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | $3$ | $\{G_1G_2,\,G_3G_2,\,G_4G_2\}$ (12) |
| $C$ | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | $3$ | $\{G_1G_4,\,G_2G_4,\,G_3G_4\}$ (12) |

Here $G_k=\{2k-1,2k\}$, $\lvert\mathcal U\rvert=24$.

**(i) $c^*_{fix}=7$, with a three‑witness certificate.** $A,B,C$ together cover all $24$ (16 from $A$, 4 from $B$, 4 from $C$). For the lower bound, three **forcing pairs**:

* $\{1,3\}\in D_B$ and $\{1,3\}\notin D_A\cup D_C\Rightarrow$ every sufficient suite contains $B$;
* $\{1,5\}\in D_A$ and $\notin D_B\cup D_C\Rightarrow$ contains $A$;
* $\{5,7\}\in D_C$ and $\notin D_A\cup D_B\Rightarrow$ contains $C$.

So $c^*_{fix}\ge 1+3+3=7$ — an integral packing‑of‑singletons certificate, i.e. a "forcing set". A replay consists of three $2\times2$ table lookups.

**(ii) $V(X)=4$.** *Upper:* ask $A$ (cost $1$). On outcome $0$ the candidate set is $\{1,2,3,4\}$ and the residual unresolved pairs are $\{G_1\times G_2\}$; $B$ resolves them. On outcome $1$ the candidate set is $\{5,6,7,8\}$ and the residual is $\{G_3\times G_4\}$; $C$ resolves them. Worst case $1+3=4$.

*Lower (replayable):* consider state $1$. A correct strategy must, on $1$'s path, separate $1$ from $3$ and $1$ from $5$. Among $\{A,B,C\}$ the only measurement separating $1$ from $3$ is $B$ and the only one separating $1$ from $5$ is $A$. Hence $\{A,B\}\subseteq\mathrm{Path}(1)$ and $V(X)\ge c_A+c_B=4$. $\square$

Therefore

$$V(X)=4\ <\ 7=c^*_{fix}(\mathfrak P).$$

**Mechanism (stated, not generalized).** $A$ is a *splitter that resolves nothing by itself* ($D_A$ misses $G_1\times G_2$ and $G_3\times G_4$); the two branch residuals are covered by *disjoint* expensive instruments $B$ and $C$. A fixed suite must buy both; an adaptive strategy buys one. We do not claim a general characterization of when the gap is positive.

---

## 14.6.8 Graceful degradation, via P.1's pseudometric bound

`WDP-CH14-P08` **Finite proposition (what a failed cover still buys you).** Let $A$ carry a pseudometric $d_A$, let $r_S$ be valued in a pseudometric space, and suppose some $\widehat q$ satisfies $d_A\bigl(q(x),\widehat q(r_S(x))\bigr)\le\varepsilon$ for all $x$. Then on every fiber of $r_S$ (inside a fiber of $p$) any two states $x,y$ satisfy

$$d_A\bigl(q(x),q(y)\bigr)\le 2\varepsilon .$$

*Proof.* Triangle inequality through the common decoded value $\widehat q(r_S(x))=\widehat q(r_S(y))$. $\square$

So when no suite is sufficient, the cheapest suite still certifies *how far apart the answers are on every unresolved pair*: either some pair is $>2\varepsilon$ apart (a quantitative impossibility result for the shelf, in the declared metric), or $d_A$ is zero between distinct values and nothing follows. The bound is necessary, not sufficient (P.1's three‑point countermodel), and at $\varepsilon=0$ one needs separation on $A$ itself. This is the honest fallback: the price problem degrades to a *bound* problem rather than returning a bare $\infty$.

---

## 14.6.9 Nonclaims, falsifiers, ledger, and the answer

`WDP-CH14-N03` **Nonclaim block.**
1. Nothing here derives a price. $c_i$ is declared data (`CH03-D01`).
2. Nothing here authorizes a purchase or an action. Evaluation standing and authority stay separate layers (`CH12-P01`, `CH15-N01`, `CH13-N01`).
3. No polynomial‑time exact procedure, no hardness theorem, and no constant‑factor gap bound is claimed (P05e is a reduction *to* a named problem; P05c proves only the displayed limit).
4. No claim that the minimal sufficient suites are unique, few, or canonical. Minimal transversals of a hypergraph carry none of that.
5. The recursion is worst case. Expected‑cost, minimax‑regret, and average‑case variants require their own declared models and are not derived here.
6. No continuum, no instrument physics, no measurement uncertainty semantics (the $2\varepsilon$ bound of P08 is a declared‑metric statement, not a VIM/GUM claim).
7. $X$ finite is essential to termination. Nothing extends to infinite carriers.
8. No formalization or executable credit is taken by this section.

**Falsifiers (§21 register).**

* *CH14‑P04* fails if a proposed suite passes the $D(u)\ne\emptyset$ test on all $u\in\mathcal U$ and (1) nevertheless fails — search over $\mathcal U$ is exhaustive, so this refutes an implementation.
* *CH14‑P05* ("LP is a lower bound") is refuted by a primal–dual LP pair of value $v$ with a verified sufficient suite of cost $<v$. *CH14‑P05*'s sharpness claim is refuted by an instance with $c^*_{fix}=\tau$; the Fano instance (§14.6.4) is the standing counterexample, and any instance where $\tau<c^*$ refutes "LP certifies".
* *CH14‑P05b* is refuted by an instance with $c^*_{fix}<\sum_j\min\{c_i:u_j\in D_i\}$; the 3‑edge star ($2<2$? no: $2 < 2$ holds, so use the four‑element star with three edges: optimum $3$, best packing $2$) is the standing counterexample to packing‑tightness.
* *CH14‑P06* item 3 is refuted by a strategy of worst case $<V(X)$, or by a cheapest first move lying outside $J^*(C)$.
* *CH14‑P06b* is refuted by an instance with $V(X)>c^*_{fix}$ — a direct check of the "ask $S^*$ and stop early" strategy.
* *CH14‑P07* is refuted by a correct strategy on an instance where some $\equiv$‑pair has different $q$ values.

**Candidate formal and executable targets (proposals only; no credit).** For CH14‑P04/P05b: the coverage↔transversal equivalence and the packing bound over a finite table. For CH14‑P05d: `BuildCover–Decide` with an independent re‑checker for (P) and (D1)–(D3), plus tamper tests on every certificate field — the architecture of §D.2, not an instance of it. For CH14‑P06: well‑foundedness of (3) in $|C|$ and the $J^*$ restriction. For CH14‑P07: the $\equiv$‑criterion. For the two worked instances: exact rational table checks. Nothing above is `Mechanized elsewhere`.

**Ledger rows to add** (with `formal_anchor: not present`, `executable_anchor: not present`, `source_revision: this text`): `WDP-CH14-D02`, `D03`, `P04`, `P04b`, `P05`, `P05b`, `P05c`, `P05d`, `P05e`, `P06`, `P06b`, `P07`, `P08`, `N03`.

---

## The operational answer, in one paragraph

Given the visible report $p$, the additional observations that are **necessary and sufficient** are exactly the transversals of the hypergraph whose edges are the pairs each instrument distinguishes inside $\mathcal U=\{\{x,y\}:p(x)=p(y),\,q(x)\ne q(y)\}$; the **cheapest fixed** completion is the minimum‑weight transversal $c^*_{fix}$, and it is certified by a cover map together with an *integer* lower‑bound object (forcing pairs, residual counting, an integral packing, or an LP pair that meets the integral value) — never by the relaxation alone, as the Fano instance ($7/3$ versus $3$) shows. The **cheapest adaptive** completion is the exact recursion (3), restricted to measurements that actually separate some unresolved pair, terminating because the candidate set strictly shrinks, and it is never more expensive than the fixed answer and sometimes strictly cheaper, as $V=4<7$ above shows. When the shelf cannot resolve the question, the procedure returns an indistinguishable pair with different answers, together with the $2\varepsilon$ separation bound that the best available suite still certifies. And having bought the information confers no standing whatever: `CH12-P01` and `CH15-N01` are untouched by any of it.