GLM5.3's VERSION TO THE FIRST LEMMA U GAVE ME:
## Theorem

Let $V$ be an ordered $\mathbb Q$-vector space, $u\ge 0$, $E=[0,u]:=\{X\in V: 0\le X\le u\}$, and $p:E\to\mathbb Q_{\ge 0}$ additive in the sense that $p(A+B)=p(A)+p(B)$ whenever $A,B,A+B\in E$. Then for every $A\in E$ and $q\in\mathbb Q\cap[0,1]$ we have $qA\in E$ and
$$p(qA)=q\,p(A).$$

**What is used.** Only the order axioms of an ordered $\mathbb Q$-vector space,
- (T) $X\le Y\Rightarrow X+Z\le Y+Z$,
- (S) $X\le Y,\ \mu\in\mathbb Q_{\ge0}\Rightarrow \mu X\le\mu Y$,

the stated additivity of $p$, and arithmetic in $\mathbb Q$. No linearity, monotonicity, or continuity of $p$ is assumed (in fact $p(u)=1$ and $p\ge0$ are never used). Since $u\ge0$, reflexivity gives $0,u\in E$.

**Lemma (everything stays in $E$).** *If $X\in E$ and $\lambda\in\mathbb Q\cap[0,1]$, then $\lambda X\in E$.*

*Proof.* From $0\le X$ and $\lambda\ge0$, (S) gives $0=\lambda\cdot 0\le\lambda X$. From $0\le X$ and $1-\lambda\ge0$, (S) gives $0\le(1-\lambda)X$; adding $\lambda X$ via (T) gives $\lambda X\le\lambda X+(1-\lambda)X=X$. By transitivity, $0\le\lambda X\le X\le u$. $\square$

**Step 1: $p(0)=0$.** Since $0\in E$ and $0+0=0\in E$, additivity applied to $(0,0)$ gives $p(0)=p(0)+p(0)$; cancel in $\mathbb Q$.

**Step 2: equal subdivision.** Fix $X\in E$ and $n\in\mathbb Z_{\ge1}$. Set
$$B:=\tfrac1nX,\qquad X_k:=kB=\tfrac{k}{n}X\quad(0\le k\le n),$$
so $X_0=0$ and $X_n=X$ (vector-space arithmetic over $\mathbb Q$). By the Lemma ($\lambda=\tfrac1n$ and $\lambda=\tfrac kn\in[0,1]$), $B\in E$ and every $X_k\in E$ — hence $p$ is defined on all of them. For each $1\le k\le n$,
$$X_{k-1}+B=\tfrac{k-1}{n}X+\tfrac1nX=X_k,$$
so the triple $(X_{k-1},\,B,\,X_k)$ lies in $E^3$ and additivity applies:
$$p(X_k)=p(X_{k-1})+p(B).$$
Induction on $k$, with base $p(X_0)=p(0)=0$ (Step 1), yields
$$p(X_k)=k\,p(B)\qquad(0\le k\le n).\tag{$*$}$$

**Step 3: homogeneity.** Taking $k=n$ in ($*$): $p(X)=n\,p(B)$, hence $p(B)=p(X)/n$ (division in $\mathbb Q$; $n\ne0$). Substituting into ($*$):
$$p\Big(\tfrac{k}{n}X\Big)=\tfrac{k}{n}\,p(X)\qquad(0\le k\le n).\tag{$**$}$$
Now let $A\in E$, $q\in\mathbb Q\cap[0,1]$, and write $q=\tfrac mn$ with integers $0\le m\le n$, $n\ge1$. By the Lemma, $qA=\tfrac mnA\in E$, so $p(qA)$ is defined, and ($**$) with $X=A,\ k=m$ gives
$$p(qA)=p\Big(\tfrac mnA\Big)=\tfrac mn\,p(A)=q\,p(A).\qquad\blacksquare$$

**Remarks (where each hypothesis enters).**

1. *Staying in $E$:* the order axioms are used only in the Lemma, which certifies — before $p$ is ever applied — that each of $0$, $B$, $X_0,\dots,X_n$, and $qA$ lies in $E$. Additivity is invoked only for the triples $(X_{k-1},B,X_k)\in E^3$, checked elementwise.
2. *Rational structure:* $\mathbb Q$-scalar multiplication in $V$ produces the subdivision points $B,\frac{k}{n}X$ (in a mere ordered abelian group these need not exist); $\mathbb Q$-valuedness of $p$ lets us divide $p(X)=np(B)$ by $n$.
3. *What is not used:* $p(u)=1$ and $p\ge0$ (and the monotonicity they imply) play no role — the lemma is a pure consequence of effect-additivity. Accordingly, it establishes homogeneity on $[0,1]A$ only: an effect-additivity lemma, not linearity on $V$ or Born-rule uniqueness, which would require extra assumptions (e.g., that $E$ order-generates $V$).
