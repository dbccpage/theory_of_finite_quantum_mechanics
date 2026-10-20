**Setup.** "Ordered rational vector space" means: $V$ is a $\mathbb Q$-vector space with a partial order $\le$ such that $A\le B \Rightarrow A+C\le B+C$ and $0\le A,\ r\in\mathbb Q\_{\ge0} \Rightarrow 0\le rA$. Write $E=[0,u]={A: 0\le A\le u}$.

**Lemma 0 (scaling stays in $E$).** If $A\in E$ and $r\in\mathbb Q$, $0\le r\le1$, then $rA\in E$.

*Proof.* $0\le A$ and $r\ge0$ give $0\le rA$. Also $u-rA=(u-A)+(1-r)A$, and both summands are $\ge0$ (since $A\le u$, and $1-r\ge0$ with $A\ge0$), so $rA\le u$. $\square$

**Lemma 1.** $p(0)=0$.

*Proof.* $0,0,0+0\in E$, so $p(0)=p(0+0)=2p(0)$. $\square$

**Lemma 2 (integer multiples).** If $B\in E$, $n\in\mathbb Z\_{\ge0}$, and $nB\in E$, then $p(kB)=k,p(B)$ for all $0\le k\le n$.

*Proof.* Induction on $k$. $k=0$ is Lemma 1. For $k\<n$: $kB=\tfrac kn(nB)\in E$ and $(k+1)B=\tfrac{k+1}{n}(nB)\in E$ by Lemma 0 applied to $nB$; and $B\in E$ by hypothesis. So additivity applies to $kB+B$, giving $p((k+1)B)=p(kB)+p(B)=(k+1)p(B)$. $\square$

**Theorem.** For $A\in E$ and rational $q=m/n$ with $0\le m\le n$, $n\ge1$: $p(qA)=q,p(A)$.

*Proof.* Let $B=\tfrac1n A$. Then $B\in E$ (Lemma 0, $r=1/n$) and $nB=A\in E$. Lemma 2 with $k=n$ gives $p(A)=n,p(B)$, i.e. $p(B)=p(A)/n$. Lemma 2 with $k=m\le n$ gives $p(mB)=m,p(B)$. Since $mB=qA$,\
&#x20;$$p(qA)=m,p(B)=\frac mn,p(A)=q,p(A).\qquad\square$$

**Why nothing leaves $E$.** Every point evaluated is of the form $\tfrac kn A$ with $0\le k\le n$, which is in $E$ by Lemma 0; and every additivity step $kB+B=(k+1)B$ has both summands and the sum of that form with $k+1\le n$. No $p$-value is ever requested outside $[0,u]$, and no extension of $p$ to $V$ is used.

**Remarks.**

- No order-preservation of $p$ is assumed or needed; only additivity on $E$ and the rational divisibility of $V$.
- $p(u)=1$ is not used here — it is the normalization that later pins down the scale, not part of the homogeneity argument.
- This is exactly the bounded-interval version of Cauchy's equation: additivity on a convex set forces $\mathbb Q$-homogeneity there. Extension to real $q$ requires an extra hypothesis (monotonicity or boundedness), which is where the genuine Born-rule content lives.
