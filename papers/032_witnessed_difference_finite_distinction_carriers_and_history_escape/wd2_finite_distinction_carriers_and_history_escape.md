# Finite Distinction Carriers and History Escape

**Subtitle:** Observational equivalence and minimal deterministic quotients

**Author:** Jeremy H. Carroll

**Date:** 2026-10-08

**Version:** 1.1.0

**Status:** Author-review prose preprint; not an external publication

**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)

**AuthorityEffect:** None

## Abstract

For a finite deterministic system with a fixed observation map, two states
may have the same present observation but different observations after a
sequence of updates. We characterize this history-dependent distinction by
a descending sequence of equivalence relations. The recursive refinement
equals comparison over all input words up to a given length. It stabilizes
within the number of states minus the number of initial observation classes;
every pair removed at a refinement step has a shortest separating word of
the corresponding length. The stabilized relation is the largest
observation-preserving update congruence, and its quotient is the smallest
deterministic quotient preserving every state's future observations. We also
give a sufficient report-factorization condition, its proof, and a
counterexample when reports introduce an additional observation. The
arguments, including empty-state and empty-alphabet cases, are written in
the text. In this package only Theorem WD2-T1 is a Lean 4 theorem. Lemma
WD2-L1 and records WD2-T2 through WD2-T6 are finite-instance checks or
prose arguments and are not labeled proved. The results are an exposition
of finite-state observational equivalence and classical state
minimization, not a new reconstruction of physical theory.

## 1. Question and relation to state minimization

An initially hidden state difference can become visible after specified
updates. This differs from processing an unchanged observation: the observer
is allowed to update the state and then observe it again. The question is
which initially indistinguishable pairs can be separated in this way, and
how long a shortest separating sequence can be.

The model is a finite deterministic Moore machine with a finite output
alphabet. Its refinement and quotient results belong to classical automata
theory [1,2]. We claim no novelty for partition refinement, observational
equivalence, or minimal deterministic quotients. The purpose is to state
their hypotheses, witness order, and observation boundary in one finite
formulation. The arguments below are self-contained; no unpublished
companion result or unavailable proof-assistant module is required.

**Package status (2026-10-09).** Theorem WD2-T1 is elaborated in Lean 4.
Reflexivity, symmetry, and transitivity are `Wd2.related_refl`,
`Wd2.related_symm`, and `Wd2.related_trans`. Inclusion and stability are
`Wd2.related_mono` and `Wd2.related_stable`. The five-state chain at
horizon 3 is `Wd2.sharp_m5_bound`. The general class-count bound, the
no-escape equivalence, the shortest-word construction, the quotient
mapping property, and the report-factorization argument are not Lean
theorems in this package. The Python checker evaluates the sharp chain,
the update-stable pair, and the factored report.

## 2. Finite model and word convention

Fix finite sets $S$ of states and $\Sigma$ of input symbols, an integer
$K\ge0$, maps
$$
 u:S\times\Sigma\longrightarrow S,\qquad
 p:S\longrightarrow\{0,1\}^K,
$$
and write $u_\sigma(s)=u(s,\sigma)$. The binary output representation is a
choice, not an assertion that binary distinctions are primitive. The proofs
also apply to a map into any finite output set.

Words are applied **left to right**. With $\varepsilon$ denoting the empty
word, define
$$
 u_\varepsilon=\operatorname{id}_S,\qquad
 u_{w\sigma}=u_\sigma\circ u_w.
$$
Induction on the length of $v$ gives
$u_{wv}=u_v\circ u_w$, and in particular
$u_{\sigma v}=u_v\circ u_\sigma$. This convention matters when updates do
not commute. No order on the alphabet is assumed.

For a map $f:S\to Y$, its kernel relation is
$\ker f=\{(s,t):f(s)=f(t)\}$. An *update congruence* is an equivalence
relation $E$ on $S$ such that
$sEt$ implies $u_\sigma(s)E u_\sigma(t)$ for every symbol $\sigma$.
It preserves the declared observation when $E\subseteq\ker p$.

## 3. Finite-horizon observations

Set $R_0=\ker p$ and, for integers $n\ge0$, define
$$
 R_{n+1}=R_0\cap\bigcap_{\sigma\in\Sigma}
              (u_\sigma\times u_\sigma)^{-1}(R_n).
$$
The intersection over an empty alphabet is $S\times S$.
An initially ambiguous pair $(s,t)\in R_0$ *escapes at depth* $n\ge1$
if $(s,t)\in R_{n-1}\setminus R_n$. A *separating word* satisfies
$p(u_w(s))\ne p(u_w(t))$; an *escape witness* is a separating word of
shortest length. “Shortest” does not mean a unique word. A tie-breaking
choice would require an additional order on $\Sigma$.

**Lemma WD2-L1 (word characterization).** For every integer $n\ge0$,
$$
 R_n=\bigcap_{|w|\le n}\ker(p\circ u_w).
$$

*Proof.* At $n=0$ the only word is $\varepsilon$, so the formula is the
definition of $R_0$. Every nonempty word of length at most $n+1$ has a first
symbol and a suffix: $w=\sigma v$, $|v|\le n$. By the induction hypothesis,
equality of all its readouts is equivalent to
$(u_\sigma(s),u_\sigma(t))\in R_n$ for every $\sigma$. The empty word
additionally requires $(s,t)\in R_0$. These are exactly the recursive
conditions for $R_{n+1}$. $\square$

## 4. Refinement and stabilization

**Theorem WD2-T1 (refinement and fixed-point law).** Every $R_n$ is an
equivalence relation and $R_{n+1}\subseteq R_n$. If $R_{n+1}=R_n$, then
$R_m=R_n$ for every $m\ge n$.

*Proof.* Kernels of maps are equivalence relations, and intersections preserve
that property. Lemma L1 therefore establishes equivalence. The set of words
of length at most $n$ is contained in the set for $n+1$, establishing the
inclusion. Define
$$
 F(E)=R_0\cap\bigcap_{\sigma\in\Sigma}
                     (u_\sigma\times u_\sigma)^{-1}(E).
$$
If $R_{n+1}=R_n$, then $F(R_n)=R_n$. Applying $F$ repeatedly gives the
claimed equality at all later indices. $\square$

**Classical record WD2-T2 (finite stabilization and a counting bound).** Not a theorem of this package. Put
$b_0=|S/R_0|$. There is a least integer $N\ge0$ such that
$R_N=R_{N+1}$, and
$$
 N\le |S|-b_0,\qquad R_\infty:=\bigcap_{n\ge0}R_n=R_N.
$$
The number $N$ counts strict refinement rounds. An implementation can need
one additional comparison to establish $R_N=R_{N+1}$.

*Proof.* A strict inclusion of finite equivalence relations splits at least
one class, increasing the number of classes by at least one. Starting with
$b_0$ classes, no more than $|S|-b_0$ consecutive strict inclusions can
occur. The first equality is permanent by T1. The descending intersection
is therefore its stabilized value. If $S$ is empty, both class counts and
$N$ are zero. If $\Sigma$ is empty, the recursion is constant and $N=0$.
$\square$

For sharpness when $m=|S|\ge2$, take
$S=\{0,\ldots,m-1\}$, a single symbol $a$,
$u_a(i)=\min(i+1,m-1)$, and $p(i)=1$ precisely for $i=m-1$.
At horizon $j\le m-2$, the lowest class is
$\{0,\ldots,m-2-j\}$ and all larger states are singleton classes.
Indeed state $i<m-1$ first reads one after exactly $m-1-i$ updates.
Thus $b_0=2$ and $N=m-2=|S|-b_0$ (including $N=0$ when $m=2$).

## 5. No escape and shortest witnesses

**Classical record WD2-T3 (no-escape criterion).** Not a theorem of this package. The following are equivalent:

1. $R_0$ is an update congruence;
2. $R_1=R_0$;
3. $R_n=R_0$ for every $n\ge0$;
4. no pair in $R_0$ has a separating word.

*Proof.* Since $R_1\subseteq R_0$, equality holds exactly when every pair
in $R_0$ is carried by every update back into $R_0$. This is condition 1.
Condition 2 implies 3 by T1, and 3 implies 2 by taking $n=1$. By L1,
condition 3 says that every initially equivalent pair has equal readouts
after every finite word, which is exactly condition 4. $\square$

**Classical record WD2-T4 (shortest separating-word construction).** Not a theorem of this package. If
$(s,t)\in R_n\setminus R_{n+1}$, then its shortest separating-word length
is $n+1$. Such a word can be constructed as a first symbol followed by a
length-$n$ suffix. Consequently every escaping pair has escape depth at
most $N\le |S|-b_0$.

*Proof.* Membership in $R_n$ excludes separation by any word of length at
most $n$, by L1. Failure of $R_{n+1}$, together with membership in $R_0$,
provides a symbol $\sigma$ for which the successor pair lies outside $R_n$.
For $n=0$, the empty suffix separates that successor pair. For $n\ge1$,
the recursion for membership of the original pair in $R_n$ also places
the successor pair in $R_{n-1}$. Induction supplies a shortest separating
suffix $v$ of length $n$. The word $\sigma v$ separates the original pair
because $u_{\sigma v}=u_v\circ u_\sigma$. Its length is $n+1$, which is
minimal by the first observation. No pair leaves the sequence after its
stabilization at $R_N$, giving the depth bound. $\square$

## 6. The complete finite behavioral quotient

**Classical record WD2-T6 (largest congruence and smallest deterministic quotient).** Not a theorem of this package.
The relation $R_\infty$ is the largest update congruence contained in
$\ker p$. The quotient $Q_*=S/R_\infty$ has well-defined updates and output
$$
 \bar u_\sigma([s])=[u_\sigma(s)],\qquad \bar p([s])=p(s).
$$
Let $q:S\twoheadrightarrow Q$ be any surjection with deterministic maps
$v_\sigma:Q\to Q$ and $o:Q\to\{0,1\}^K$ satisfying
$$
 q\circ u_\sigma=v_\sigma\circ q,\qquad p=o\circ q.
$$
There is a unique surjection $h:Q\twoheadrightarrow Q_*$ such that
$\pi=h\circ q$, where $\pi(s)=[s]$. It commutes with updates and preserves
output. In particular $|Q|\ge|Q_*|$. Equality makes $h$ an isomorphism of
the deterministic output systems.

*Proof.* Stabilization and the recursion show that $R_\infty$ is an
update congruence contained in $R_0$. If $E\subseteq R_0$ is any update
congruence, induction on word length shows that $sEt$ implies
$u_w(s)E u_w(t)$ for every word. Their observations agree, and L1 gives
$E\subseteq R_n$ for every $n$, hence $E\subseteq R_\infty$.
This establishes maximality and also makes the displayed quotient maps
well-defined.

For a specified quotient $q$, its kernel is an equivalence relation.
The update equation makes it an update congruence, and the output equation
places it inside $R_0$. Maximality yields $\ker q\subseteq R_\infty$.
Define $h(q(s))=[s]$. Kernel inclusion makes this independent of the choice
of $s$, and surjectivity of $q$ gives existence and uniqueness on all of
$Q$. Every class $[s]$ lies in the image, so $h$ is onto. Moreover,
$$
 h(v_\sigma(q(s)))=[u_\sigma(s)]
      =\bar u_\sigma(h(q(s))),
$$
and $o(q(s))=p(s)=\bar p(h(q(s)))$. This establishes compatibility.
Finite surjectivity gives the cardinal bound; at equality $h$ is bijective,
and its inverse also respects the maps. $\square$

Equivalently, the *behavior* of a state is the function
$\beta_s:\Sigma^*\to\{0,1\}^K$ given by
$\beta_s(w)=p(u_w(s))$. Lemma L1 identifies $R_\infty$ with equality of
behaviors. Thus $Q_*$ classifies every state by all its future readouts,
and the induced update sends a behavior $\beta_s$ to
$w\mapsto\beta_s(\sigma w)$. This completes the classification of
states for the specified finite model. It does not classify physical
theories or select quantum mechanics.

The cardinality assertion concerns quotients preserving readouts from
**every** state in $S$. A model restricted to the states reachable from one
initial state is a different minimization problem. If $S$ is empty, a
surjective $q$ has empty codomain, and the statement still holds.

## 7. Reports are additional observations unless constrained

Fix a set $\Lambda$ and a report $r:S\times\Sigma\to\Lambda$.
For a word $w=\sigma_1\cdots\sigma_m$, set $s_0=s$ and
$s_i=u_{\sigma_i}(s_{i-1})$. The report at step $i$ is
$r(s_{i-1},\sigma_i)$: it is attached to the update from $s_{i-1}$ to
$s_i$. This specifies the timing convention.

**Classical record WD2-T5 (sufficient report-factorization condition).** Not a theorem of this package. Suppose
there is a map $g:\{0,1\}^K\times\Sigma\times\{0,1\}^K\to\Lambda$
such that
$$
 r(s,\sigma)=g(p(s),\sigma,p(u_\sigma(s))).
$$
If $(s,t)\in R_n$, then their report sequences agree along every common
word of length at most $n$. Consequently adjoining these report sequences
to all profile histories through horizon $n$ leaves the relation $R_n$
unchanged.

*Proof.* For each prefix of length $i\le n$, L1 gives equality of the
profile values reached from $s$ and $t$. In particular the profiles before
and after step $i$ agree, and the input symbol is the same. Applying $g$
therefore gives equal reports at that step. This holds at every step of
every such word. The profile comparisons already impose $R_n$; the equal
reports impose no further condition. $\square$

This is sufficient, not a necessary characterization. At horizon infinity
a report constant on $R_\infty$-classes for each input can also preserve
behavioral equivalence without factoring through just the two endpoint
profiles. For example, let states $x,y,z$ have profiles $0,0,1$, let $a$
act identically, and let $b$ send $x$ to $x$ and both $y,z$ to $z$.
Here $R_\infty$ is equality. A report distinguishing $x,y$ on input $a$
preserves that equality relation but cannot factor through the identical
endpoint profile pair $(0,0)$ for $a$.

Without any report restriction even the one-step conclusion fails. Take
$S=\{0,1\}$, one identity update $a$, constant profile $p=0$, and
$r(s,a)=s$. Every profile history agrees, but the first reports differ.
The report has supplied an additional observation, not recovered a
difference from the unchanged profile.

## 8. Worked witnesses and boundary cases

**Three-state escape.** Let $S=\{x,y,z\}$, $\Sigma=\{a\}$,
$p(x)=p(y)=0$, $p(z)=1$, and
$u_a(x)=x$, $u_a(y)=u_a(z)=z$. Initially the classes are
$\{x,y\}$ and $\{z\}$. One refinement makes every state a singleton;
$a$ is a shortest witness for $x,y$. Thus $N=1=3-2$.

**Noncommuting updates.** Let $S=\{0,1,2,3\}$, profiles $(0,0,0,1)$,
and specify the update values in state order by
$$
 u_a=(1,2,2,3),\qquad u_b=(0,0,3,3).
$$
States $0,1$ have equal readouts at the empty word and after either one-letter
word. Under $ab$ they reach $0,3$, whose profiles differ. Under $ba$ they
both reach $1$. Thus $ab$ is a shortest separating word of length two,
and reversing the word destroys this witness. In fact $R_1$ has classes
$\{0,1\},\{2\},\{3\}$ and $R_2$ is equality.

**No symbols or no output bits.** If $\Sigma$ is empty, the only word is
$\varepsilon$ and no initially ambiguous pair escapes. If $K=0$, the
output set is a singleton, so all pairs have equal profiles forever,
regardless of the updates. For empty $S$, every relation and quotient is
empty and every assertion about a state pair is vacuous.

## Mechanism inventory

| Object | Mathematical role |
|---|---|
| Finite $S$ | States being compared |
| Finite $\Sigma$ and $u_\sigma:S\to S$ | Permitted deterministic updates |
| Finite profile $p:S\to\{0,1\}^K$ | Declared observation |
| Equivalence relations $R_n$ | Equality of readouts through horizon $n$ |
| Separating word | Finite witness of observable difference |
| $S/R_\infty$ | Smallest deterministic quotient preserving all states' future readouts |
| Optional report $r$ | Additional observation with explicit timing and factorization hypothesis |
| **AuthorityEffect** | None |

## Verification scope

Theorem WD2-T1 is elaborated in Lean 4 with no `sorry`. Lemma WD2-L1 and
records WD2-T2 through WD2-T6 have prose arguments above. The Python
checker evaluates finite instances of those statements; their general
forms are not Lean theorems in this package. From the package root, this
command checks pinned files, those finite tests, and the Lean build:

```bash
py -3.12 verify_deposit.py --lean --test code/tests/test_proved_rows.py
```

The reading notebook contains prose only and requires no kernel execution.

No cochain complex, Hilbert space, repair norm or physical probability rule
is defined here. A quotient by behavioral equivalence is a quotient of a
finite set, not a Banach quotient. Nothing here derives memory, agency,
consciousness, or quantum theory from a deterministic update system.

## References

1. L. Trevisan, *CS103: Mathematical Foundations of Computing*, Lecture 16,
   state minimization, Stanford University (2010).
   <https://theory.stanford.edu/~trevisan/cs103-10/lecture16.pdf>.
2. J. E. Hopcroft, R. Motwani, and J. D. Ullman, *Introduction to Automata
   Theory, Languages, and Computation*, third edition, Pearson (2007),
   Chapter 4. ISBN 978-0-321-45536-9.
