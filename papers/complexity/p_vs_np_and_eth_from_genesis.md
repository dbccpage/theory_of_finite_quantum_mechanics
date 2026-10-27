<div align="center">

# P, NP and the Exponential Time Hypothesis from Genesis: Search, Signs and Presentations

**Author:** Jeremy H. Carroll

**Date:** 2026-10-27

**Status:** Unpublished exploratory draft. Not reviewed. Temporary: its results are to be moved into
the computation and fermion-sign papers or dropped.

**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)

</div>

## Introduction

The computation stage of the derivation DAG (`dag/derivation_dag.json`) proves in Lean that word
rewriting over admitted marks simulates Turing machines step for step, that one finite alphabet of
marks carries a universal machine, and that halting and normal-form reach are undecidable
([computation proofs](../computation/computation_proofs.md), §1). The fermion-sign stage records
signed sums, switching normal forms and an imported NP-hardness reduction
([fermion sign proofs](../core/fermion_sign_and_majorana_proofs.md)). This note asks what lies
between those two facts: where, in the passage from the empty mark $\langle\rangle$ to a universal
machine, the gap between finding and checking appears, why a sign appears as early as it does, and
what the reported refutation of the Exponential Time Hypothesis would and would not change.

Four questions are taken in turn.

1. Where does exponential search enter the Genesis regimes, and is the P/NP boundary visible in
   the regimes' own operations? (§§2–3)
2. Why does a sign appear so early, and why is the sign problem hard? (§4)
3. What would a subexponential algorithm for $k$-SAT do to signed sums, and to this programme? (§5)
4. Are P and NP properties of the world or of a family of presentations, and does any of this bear
   on computational irreducibility? (§§6–7)

**Labels.** Every result carries one of these labels, and nothing in this note changes a DAG
status.

| Label | Meaning |
|---|---|
| *Lean* | Proved in this repository's Lean; the DAG node and declarations are named. |
| *Mathlib* | A theorem of Mathlib, not exercised by this repository's Lean. |
| *Prose* | Proved here in writing, not in Lean. Small cases are checked by `papers/complexity/checks/complexity_checks.py`. |
| *Imported* | A published theorem, cited and not proved here. |
| *Reported* | A claim announced by others and not checked by us. |
| *Conditional* | Follows from an imported or reported result by an argument given here. |
| *Conjecture* | A precise statement we believe and have not proved. |
| *Reading* | An interpretation. It is not a theorem and is not evidence. |

The checks run with `python -I papers/complexity/checks/complexity_checks.py` from the repository
root (standard library only, under a second).

## 1. From $\langle\rangle$ to a universal machine

This section only collects what is already proved, so that later sections can cite it.

- *Lean.* $n$ marks can be admitted and pairwise separated with $n-1$ unary forms
  (`COMP-C1-CANONICAL-SEPARATED-ALPHABET`), and two marks suffice to code any finite alphabet
  injectively (`COMP-C8-BINARY-CODING`).
- *Lean.* Rewriting over the marks $\Gamma\sqcup\Lambda\sqcup\{\vdash,\dashv\}$ simulates a TM0
  machine one step for one step, forward and backward, and the machine halts exactly when a
  reachable word is irreducible (`COMP-C5-TM0-STEP-SIMULATION`, `COMP-C5-CLOSURES-HALTING`).
- *Lean.* A fixed machine $M_0$, compiled from Kleene's universal function, runs every program
  over one finite mark set ($1250$ tape marks plus finitely many state marks)
  (`COMP-C6-EVAL-HAS-A-CODE`, `COMP-C6-FINITE-MARKS`), and both its halting and its normal-form reach
  are not computable (`COMP-C7-MACHINE-HALTING-UNDECIDABLE`, `COMP-C7-NF-REACH-UNDECIDABLE`).
- *Lean.* Under a length bound $L$ reach is decidable by iterating successors over the
  $\sum_{i\le L}k^i$ words of length at most $L$ (`COMP-C3-BOUNDED-REACH-DECIDABLE`).

What is *not* derived matters as much. The universal machine needs words of unbounded length, and
in Genesis terms every new blank is an admitted datum, a host event. The closed Genesis system
saturates after at most $n(n-1)/2$ rounds (`PGW-ENDOGENOUS-DEMANDS-EXOGENOUS-PAYMENTS`, *Lean*),
and unbounded supply is an imported assumption, not a theorem (`COMP-C4-UNBOUNDED-SUPPLY-IMPORT`).
So the route $\langle\rangle\to$ UTM is proved *given* an exogenous supply of fresh marks and a
declared rule list. Everything below inherits that hypothesis.

## 2. Where exponential search enters

### 2.1 The brute-force bound is the size of the bounded word space

The decision procedure of §1 for bounded reach explores up to $\sum_{i\le L}k^i$ words, exponential
in $L$. That is the generic cost of *search* in these regimes: a question whose answer is a
witness word, or a path of rewriting steps, is settled by enumerating the space in which the
witness lives.

**Proposition 2.1** (*Prose*). Fix a finite rule list over $k$ marks. The problem "given words
$a,b$ and a number $t$ written in unary, does $a$ reach $b$ in at most $t$ steps?" is in NP.

*Proof.* A certificate is the list of at most $t$ intermediate words together with, for each step,
the rule used and the position of its left side. Each word has length at most
$|a|+t\cdot\max_{(l,r)}|r|$, so the certificate has size polynomial in $|a|+|b|+t$, and each step
is checked by comparing the words around the stated position. $\square$

**Proposition 2.2** (*Imported*). For suitable fixed rule lists this problem is NP-complete.
String rewriting with a step bound simulates nondeterministic Turing machines with a step bound,
and Cook–Levin then applies (Cook 1971; Book and Otto 1993 for semi-Thue systems). The Lean
simulation of §1 is for deterministic machines (Mathlib's TM0); the nondeterministic version is not
formalized here.

When $t$ is not bounded, or is written in binary, the problem leaves NP: bounded-length reach is
PSPACE-complete for suitable rule lists (the linear-bounded-automaton acceptance problem), and
unbounded reach is undecidable (§1, *Lean*).

### 2.2 The certificate is the payment

**Reading.** NP is the class of questions whose positive answers have a short *exogenous*
witness and a polynomial-time *endogenous* check. In the Genesis vocabulary the witness is a
payment (a supplied tag, an admitted mark, a chosen path) and the check is replay. The proved
Genesis facts say that payments are not generated by the closed system
(`PGW-ENDOGENOUS-DEMANDS-EXOGENOUS-PAYMENTS`), and that when a refinement is needed its choice is
not determined by the regime (`PGW-FORCED-SEPARATION-LIFT-NOT-UNIQUE`,
[Genesis proofs](../genesis/genesis_proofs.md) §1.1). P versus NP asks, in this reading, whether
every short payment that replay can verify can also be produced by a polynomial-time procedure.
This is a description of the question and does not bear on its answer.

## 3. The P/NP boundary inside a Genesis operation

The Genesis refinement step adds a tag to a report to resolve conflicting pairs
([Genesis proofs](../genesis/genesis_proofs.md) §1.4, `PG-REFINE-SEPARATES`, *Lean* for the
separation; the colouring criterion is *Prose* there). A tag with values in $\{0,1\}^b$ resolves a
conflict set $C$ exactly when the conflict graph $(A,C)$ has a proper colouring with $2^b$ colours.

**Proposition 3.1** (*Prose* + *Imported*). Let the conflict graph have $n$ vertices and $m$ edges.

1. Deciding whether a one-bit tag exists is bipartiteness, decidable in $O(n+m)$ time by
   breadth-first two-colouring.
2. Deciding whether a two-bit tag exists is 4-colourability, which is NP-complete.
3. For every fixed $b\ge2$ deciding whether a $b$-bit tag exists is NP-complete.

*Proof.* (1) The colouring criterion of §1.4 with $2^1=2$ colours, and the standard
breadth-first test: colour a vertex, give each neighbour the other colour, and report failure on
an edge whose ends share a colour; an odd cycle is the only obstruction. (2), (3) $3$-colourability
is NP-complete (*Imported*: Karp 1972; Garey, Johnson and Stockmeyer 1976). Adding $q-3$ new
vertices adjacent to everything and to each other turns a $3$-colouring question into a
$q$-colouring question, so $q$-colourability is NP-hard for every fixed $q\ge3$, in particular for
$q=2^b$ with $b\ge2$. Membership in NP is the tag itself. $\square$

The checks confirm on 150 random graphs with at most six vertices that a one-bit tag exists exactly
when the graph is bipartite and a two-bit tag exactly when it is 4-colourable (computed by
exhaustive search).

So the boundary between polynomial time and NP-completeness (assuming P $\neq$ NP) is crossed
inside a single Genesis operation, between one and two bits of supplied tag. The odd-cycle
obstruction to a one-bit tag is the same obstruction as the odd frustrated cycle of §4: both are
the failure of a $\mathbb Z/2$-valued potential to exist around a cycle.

**Conditional 3.2.** Under ETH, no algorithm decides the existence of a two-bit tag in time
$2^{o(n)}$ on conflict graphs with $O(n)$ edges. (ETH implies that $3$-colouring of graphs with
$O(n)$ edges needs $2^{\Omega(n)}$ time; *Imported*: Impagliazzo, Paturi and Zane 2001; Cygan
et al. 2015, Chapter 14. The apex construction above with one apex vertex adds $n$ edges.)

## 4. The sign

### 4.1 Three places the sign appears, each forced by a minimal structure

In the proved Genesis material the sign appears three times, from three different minimal structures, none of them physical.

**(a) Orientation.** A relation $arb$ that is irreflexive need not be symmetric: the relation
$\{(0,1)\}$ on $\{0,1\}$ contains $arb$ and not $bra$ (`PG-GEN-IRREFLEXIVE-DISTINCT`, *Lean*,
[Genesis proofs](../genesis/genesis_proofs.md) §2.1(4)). Once edge data are compared with potentials,
the coboundary of the triangle is $d_0g=(g_b-g_a,\ g_c-g_b,\ g_a-g_c)$, and traversing an edge
backwards contributes the negative of its value; the circulation $I(x)=x_{ab}+x_{bc}+x_{ca}$ is an
obstruction with values in $\mathbb Z$ (`PGW-SN-E12-CIRCULATION-FUNCTIONAL`, *Lean*, §6.1 there).
The sign here is the cost of reversing an oriented edge.

**(b) Cancellation.** In the twenty-second Genesis Ongoing seed an assertion $xry$ and an
assertion $xsy$ cancel. The multiplicity tables, which were natural numbers and could only rise,
are replaced by the excess $e_G(x,y)=M_r(x,y)-M_s(x,y)\in\mathbb Z$, and sameness of results is
equality of excess (`PGW-GO-H1-CANCELLATION-EXCESS`, *Lean*, §4.8 there). This is the
Grothendieck completion of the multiplicity monoid: the first seed in which an addition can undo an
addition is the first seed with signed weights, and the earlier no-return property for additions
fails there. The next two seeds add the gauge $e\mapsto e+g(x)-g(y)$
(`PGW-GO-H2-STATE-RAISING-GAUGE`) and holonomy around filled triples
(`PGW-GO-H3-TWIN-FILLS-HOLONOMY`), both *Lean*. Signed weights, a gauge and holonomy are exactly the
data of a signed graph modulo switching.

**(c) Exchange.** Once there are $n\ge2$ marks that the regime does not tell apart, the symmetric
group acts on them, and no point is fixed by every permutation (`PG-WDP-PROTECTED-QUESTIONS`,
*Lean*, §2.3 there).

**Proposition 4.1** (*Mathlib* + *Prose*). For $n\ge2$ the symmetric group $S_n$ has exactly two
homomorphisms to the multiplicative group $\mathbb C^\times$: the trivial one and the sign.

*Proof.* A homomorphism to an abelian group is constant on conjugacy classes, and all
transpositions are conjugate, so it sends every transposition to one value $\varepsilon$ with
$\varepsilon^2=1$. Transpositions generate $S_n$, so $\varepsilon=1$ gives the trivial
homomorphism and $\varepsilon=-1$ gives the sign. Mathlib's
`Equiv.Perm.eq_sign_of_surjective_hom` states the uniqueness of the sign among surjective
homomorphisms to $\mathbb Z^\times$. $\square$

The checks compute the commutator subgroup of $S_n$ for $n=2,\dots,5$ and find the alternating
group in each case, which is the same statement.

**Reading.** If exchanging two indistinguishable marks is recorded by a single scalar factor,
that factor is $+1$ for every exchange or the sign of the permutation; there is no third
one-dimensional option. Bosonic and fermionic bookkeeping are the two characters of $S_n$, and the
fermionic one is available as soon as a regime has two exchangeable marks. Nothing here explains
why nature uses the sign character for some particles; it explains why, once a scalar exchange
rule is wanted, the sign is one of only two candidates. The Fock-space realization of the sign
character and the Jordan–Wigner hop sign are recorded separately (`FSP-CAR-EXTERIOR-FOCK`, *Prose*;
`FSP-JORDAN-WIGNER-HOP-SIGN`, computationally checked on six modes).

So the answer offered here to "why so early" is that the sign is the smallest structure that
records each of orientation, cancellation and exchange. It is cheap to introduce and appears at
the first stage that has any of the three.

### 4.2 Balance is easy, the frustration index is hard

Write a sign on each edge of a finite graph additively, $x_e\in\mathbb Z/2$ ($1$ for negative).
Switching at a vertex set $s$ replaces $x$ by $x+d_0s$. A signing is *balanced* when it switches to
all-positive.

**Proposition 4.2** (*Lean*: `FSP-SWITCHING-NORMAL-FORM`). For a supplied spanning forest, every
switching class has a unique representative that vanishes on the forest, determined by the chord
signs; there are $2^{|E|-|V|+c}$ classes. In particular balance is decided in polynomial time: it
holds exactly when every chord closes a positive fundamental cycle.

The checks confirm on 200 random signed graphs with at most seven vertices that the chord test
agrees with exhaustive search over switchings.

The hard question is not membership in the balanced class but distance to it. Define the
*frustration index* $\Phi_1^{\mathbb F_2}(x)=\min_s\operatorname{wt}(x+d_0s)$, the fewest negative
edges in the switching class. This is the weighted $\ell^1$ obstruction $\Phi_1$ of the Genesis
cochain calculus ([Genesis proofs](../genesis/genesis_proofs.md) §6) with unit weights and
coefficients $\mathbb F_2$, and it is the coset-leader weight of $x$ for the binary code
$\operatorname{im}d_0$ (`MAJ-PHI1-SYNDROME-DECODING`, *Conditional*).

**Proposition 4.3** (*Prose*). For the all-negative signing $x=\mathbf 1$ of a graph $G$,
$\Phi_1^{\mathbb F_2}(\mathbf 1)=|E|-\operatorname{maxcut}(G)$. Hence computing the frustration
index of signed graphs is NP-hard.

*Proof.* After switching at $s$, an edge $uv$ is negative exactly when $1+s_u+s_v=1$, that is, when
$s_u=s_v$, which is when the cut defined by $s$ does not separate $u$ and $v$. So the number of
negative edges is $|E|$ minus the size of that cut, and minimizing over $s$ gives the claim.
MAX-CUT is NP-hard (*Imported*: Karp 1972). $\square$

The checks confirm the identity on 200 random graphs with at most seven vertices. The frustration
index is the ground-state energy (up to an affine change) of the $\pm J$ Ising spin glass on $G$;
Barahona (1982, *Imported*) proved it NP-hard on three-dimensional grids and on planar graphs in a
field, and polynomial on planar graphs without a field.

### 4.3 The coefficient dichotomy

The same functional $\Phi_1$ with ordered coefficients is easy.

**Proposition 4.4** (*Lean* + *Imported*). Over $\mathbb Q$, $\Phi_1(c)=\min_g\sum_e\omega_e
|c_e-(d_0g)_e|$ equals the maximum of $c^{\mathsf T}y$ over circulations $y$ with $|y_e|\le\omega_e$,
both attained (`PGW-SN-E08-WEIGHTED-L1-DUALITY`, `L1-FRAMEWORK-KKT-CERT`, *Lean*), so it is a linear
programme and is computed in polynomial time (*Imported*: Khachiyan 1979). When $d_0$ is the
incidence matrix of a graph it is totally unimodular, so for integer $c$ and $\omega$ the optimum is
attained at an integer potential (*Imported*: Schrijver 1986, §19), and the problem is the dual of
a minimum-cost flow problem.

The checks confirm on random small graphs, with integer $c\in[-2,2]^E$ and unit weights, that the
best integer potential and the best integer circulation $y\in\{-1,0,1\}^E$ have equal value; by weak
duality this pins the rational optimum to the integer one on those instances.

**Reading.** On the same graph and the same cochain, $\Phi_1$ is a polynomial-time linear programme
when the coefficients are $\mathbb Z$ or $\mathbb Q$ and NP-hard when they are $\mathbb Z/2$. The
difference is convexity: an ordered group has a convex relaxation whose optimum is exact (duality
plus total unimodularity), and $\mathbb Z/2$ has no order and no such relaxation. The cancellation
of §4.1(b) lives in $\mathbb Z$; the sign of §4.1(c) lives in $\mathbb Z/2$. The proposal of this
note is that the sign problem is hard where the bookkeeping passes from $\mathbb Z$ to
$\mathbb Z/2$, and not before.

**Conjecture 4.5.** For the families of finite cochain windows of the Genesis calculus (graph and
2-complex incidence matrices with integer weights), exact $\Phi_1$ over $\mathbb Z$ or $\mathbb Q$
is in P, and exact $\Phi_1$ over $\mathbb Z/p$ for any prime $p$ is NP-hard on the family of
2-complexes. The first half follows from Proposition 4.4 for graphs and from linear programming in
general; the second is proved above only for $p=2$ on graphs.

### 4.4 The sign problem proper

The fermion sign problem is a statement about estimators, not about a single number. For a path
representation with weights $W(c)$, the average sign is $\langle\mathrm{Sign}\rangle=Z/Z_{\mathrm{abs}}$
(`FSP-AVERAGE-SIGN-DEFINITION`), and a relative error $\epsilon$ needs about
$(1-\langle\mathrm{Sign}\rangle^2)/(\epsilon^2\langle\mathrm{Sign}\rangle^2)$ samples
(`FSP-SIGN-ESTIMATOR-VARIANCE`, *Prose*). The repository's sign results fit the dichotomy above.

- *Lean.* A sign-reversing, weight-preserving involution cancels in pairs; zero signed mass does
  not require one (`FSP-INVOLUTION-PAIR-CANCELLATION`). This is the $\mathbb Z$-level, convex
  mechanism: cancellation by an explicit matching.
- *Imported.* Troyer and Wiese (2005): a polynomial-time estimator for the frustrated quantum
  model $-\sum J_{ij}\sigma^x_i\sigma^x_j$ at the stated temperature would give P $=$ NP
  (`FSP-TROYER-WIESE-REDUCTION`). The hard instances are exactly the frustrated $\pm J$ signings of
  §4.2.
- *Lean* (a refutation). The claimed dichotomy "every finite system either has a polynomial-time
  sign-eliminating involution or is NP-hard" is refuted: NP-hardness belongs to input families, and
  the free triangle has no equal-weight involution in its declared basis yet is solved by one-body
  diagonalization (`FSP-MASTER-DICHOTOMY-REFUTED`).
- *Imported.* Whether a local Hamiltonian can be made sign-free (stoquastic) by a local basis
  change is itself NP-hard to decide in general (Marvian, Lidar and Hen 2019; Klassen and Terhal
  2019 for two-local qubit Hamiltonians).
- *Open.* No efficient sampler or general solution is established here
  (`FSP-EFFICIENT-SAMPLING-OBLIGATIONS`).

**Reading.** The sign problem is a property of a presentation (a basis and a path expansion) of a
system, as the free triangle shows; finding a better presentation can itself be NP-hard. This
supports the view in §6 that hardness belongs to families of presentations and the translations
between them, and not to a single physical system.

## 5. Signed sums, counting, and the reported refutation of ETH

### 5.1 The hypothesis

**Definition.** The Exponential Time Hypothesis (Impagliazzo and Paturi 2001) states that there is
$\delta>0$ such that no algorithm decides $3$-SAT on $n$ variables in time $2^{\delta n}$. By the
sparsification lemma (Impagliazzo, Paturi and Zane 2001) it is equivalent to the statement that
$3$-SAT has no $2^{o(n)}$ algorithm, and it may be stated with $n$ the number of clauses instead.
ETH implies P $\neq$ NP; its failure does not imply P $=$ NP.

### 5.2 The report

*Reported.* On 2026-10-25 OpenAI announced that one of its systems had proved ETH false, with a
natural-language manuscript dated 2026-10-16 and a Lean formalization dated 2026-10-17, and that a
group including Russell Impagliazzo, Ramamohan Paturi and Ryan Williams would examine and explain
it (OpenAI 2026). As described in a public issue of the `complexitylib` project (cslib-community
2026), the formal statement gives, for each fixed $k\ge2$, one deterministic multi-tape machine that
outputs the exact number of satisfying assignments of a width-$k$ CNF on $n$ declared variables,
together with the satisfiability bit, in

$$C\,(L+1)^d\;2^{A\,n\,(\log\log(n+16))^2/\sqrt{\log(n+16)}}$$

steps, $L$ the encoding length, with polynomially bounded space. The listed technique is rational
interpolation over shared linear summaries, low-degree replacement forms, and counting common
zeros of sparse $\mathbb F_2$ polynomial systems lifted to $\mathbb Z$.

We have not read the manuscript in full, built the Lean, or checked that the formal statement is
ETH. Three cautions are on record. The `complexitylib` issue notes that the formal statement counts
declared rather than occurring variables, so a bridge to the standard parameter is still open, and
that the strongest form of the bound needs fixed clause density. The announcement mentions no peer
review. A Lean proof certifies the formal statement, not its match with the intended one.

Everything below about the reported theorem is labelled *Conditional* on it.

### 5.3 Signed sums are model counts

The cleanest form of a signed sum over $n$ binary choices is $S(p)=\sum_{x\in\{0,1\}^n}(-1)^{p(x)}$
for a polynomial $p$ over $\mathbb F_2$. For degree $2$ it is computed in polynomial time
(*Imported*: Dickson's normal form of quadratic forms; Ehrenfeucht and Karpinski 1990), which is
the counting core of the Gottesman–Knill theorem. For degree $3$ it is $\#\mathrm P$-hard, and it
equals, up to a power of $\sqrt2$, an amplitude of a circuit of Hadamard and controlled-controlled-$Z$
gates with $n$ Hadamard variables (*Imported*: Dawson et al. 2005; Montanaro 2017). Degree three is
therefore where the sign becomes a universal quantum amplitude.

**Proposition 5.1** (*Prose*). Let $p$ have degree at most $3$, no constant term and $m$ monomials
over $n$ variables (a constant term only changes the sign of $S(p)$). There is a CNF with clauses of width at most $4$, $n+2m$ variables and at most $8m+1$
clauses whose models are in bijection with $\{x:p(x)=0\}$. Hence
$S(p)=2\,\#\mathrm{models}-2^n$.

*Proof.* Introduce $y_j$ for the $j$-th monomial with clauses $\neg y_j\vee x_i$ for each of its
variables and $y_j\vee\bigvee_i\neg x_i$, which force $y_j=\prod_ix_i$. Introduce $z_1=y_1$ and
$z_j=z_{j-1}\oplus y_j$ by the four width-3 clauses of an exclusive or, and add the unit clause
$\neg z_m$. Every $x$ determines all $y$ and $z$, and the formula is satisfied exactly when
$z_m=p(x)=0$. Then $S(p)=\#\{p=0\}-\#\{p=1\}=2\#\{p=0\}-2^n$. $\square$

The checks confirm the identity, and the width bound, on 80 random polynomials with at most four
variables and three monomials.

**Conditional 5.2.** If the reported theorem holds for $\#4$-SAT at bounded clause density, then
$S(p)$ for degree-$3$ polynomials with $m=O(n)$ monomials is computed exactly in time
$2^{O(n(\log\log n)^2/\sqrt{\log n})}$, that is, in $2^{o(n)}$. Equivalently, exact amplitudes of
Hadamard–CCZ circuits with $h$ Hadamard gates and $O(h)$ CCZ gates would be computable in
$2^{o(h)}$ time, against the $2^h$ of the direct path sum.

*Argument.* Proposition 5.1 produces $n+2m=O(n)$ variables and $O(n)$ clauses of width at most $4$,
so the clause density is bounded. $\square$

What Conditional 5.2 would and would not do:

- It would falsify the counting versions of ETH and SETH, which some conditional lower bounds for
  strong classical simulation of quantum circuits assume (see Huang, Newman and Szegedy 2018), at
  least for circuits of linear size.
- It would not give a polynomial-time algorithm, would not make the sign problem tractable, and
  would not touch the estimator variance of §4.4. The bound is $2^{n^{1-o(1)}}$.
- It does not transfer directly to the frustration index of §4.2. Encoding "at most $K$ negative
  edges" as a bounded-width CNF needs a counting circuit with $\Theta(m\log m)$ auxiliary variables,
  which loses the $o(n)$ in the exponent. Whether MAX-CUT on bounded-degree graphs would also
  fall below $2^{\Omega(n)}$ is left open here.

### 5.4 What it would do to this programme

**Reading.** Most of this repository's statements are exact finite certificates (Lean proofs, exact
rational arithmetic, exhaustive enumeration), and none is conditional on ETH. The conditional
statements that cite hardness (`MAJ-PHI1-SYNDROME-DECODING`, `FSP-TROYER-WIESE-REDUCTION`) cite
NP-hardness, which a refutation of ETH does not affect. A search of the DAG for statements that
assume ETH or SETH finds none. So the reported result changes no DAG status. Its relevance is
direct only for §5.3: the signed sums that the fermion-sign stage studies are model counts, and the
reported technique is a model-counting technique over $\mathbb F_2$, the same coefficients as the
hard half of §4.3.

## 6. Intrinsic or a perspective of the presentation family?

**Proposition 6.1** (*Prose*, using *Lean* §1.6 of the Genesis proofs). Let presentations $P,Q$ of
the same finite objects be related by translations $f:P\to Q$ and $g:Q\to P$ that are computable in
polynomial time, change size polynomially, and satisfy $g\circ f=\mathrm{id}$ and
$f\circ g=\mathrm{id}$. Then a family of questions is in P (respectively NP) in presentation $P$ if
and only if the translated family is in P (respectively NP) in presentation $Q$.

*Proof.* Compose a decider (respectively a verifier) for one side with the translation. The round
trips are what make the two families the same questions (`PGW-FAITHFUL-DESCENT-ROUND-TRIP`, *Lean*:
a faithful common carrier exists exactly when the round trips close). $\square$

So within a family of presentations closed under polynomial-time faithful translation, P and NP
are invariants, not perspectives. Three things are not invariant.

1. **Finer exponents.** ETH and its relatives depend on the size measure: number of variables,
   number of clauses, or encoding length. The sparsification lemma makes the first two equivalent
   for $3$-SAT; the declared-versus-occurring variable caveat of §5.2 is a concrete case where the
   measure is the open point.
2. **The basis.** The sign problem depends on the basis and the path expansion (§4.4).
3. **The machine model.** The extended Church–Turing thesis, that every physically realizable
   computation is simulated with polynomial overhead by a probabilistic Turing machine, is a
   physical hypothesis. Quantum computation is the standard reason to doubt it: BQP contains
   factoring (Shor 1994), which is not known to be in BPP.

**Reading.** The question "why does the universe contain NP and P" splits in two. P and NP are
classes of question families about finite presentations, robust under every polynomial-time
change of presentation (Proposition 6.1), so they are not artefacts of one presentation. NP-hard
families appear in any setting that supplies, without bound, independent binary choices and local
checks on them. In Genesis these are exactly the exogenous payments of §2.2 and the tags of §3; the
closed system does not supply them, and the regimes with external supply do. Which side of the P/NP
line a *physical* question falls on depends on the third point above, which is a question about
physics and not about presentations.

## 7. Computational irreducibility

Computational irreducibility (Wolfram 2002) is the informal thesis that for many systems there is
no way to predict the state after $t$ steps substantially faster than running the $t$ steps. It is
not a single mathematical statement, so it cannot be refuted outright; specific formalizations can
be proved or refuted.

- *Lean.* For the universal regime of §1 there is no total computable predictor of normal-form
  reach (`COMP-C7-NF-REACH-UNDECIDABLE`). This is a proved form of irreducibility for long-run
  questions about universal systems.
- *Imported.* The time hierarchy theorem (Hartmanis and Stearns 1965) gives, unconditionally,
  problems decidable in time $t(n)$ and not in time $o(t(n)/\log t(n))$ on multitape machines: some
  computations have no substantial shortcut.
- *Imported.* The Blum speedup theorem (1967) gives computable functions with no fastest program,
  so "the irreducible computation" of such a function is not well defined.
- *Imported.* Some rules do have shortcuts: additive cellular automata such as rule 90 have closed
  forms by Lucas' theorem, giving the state at step $t$ in time polynomial in $\log t$ per cell.

**Reading.** A refutation of ETH concerns *search* over an exponential certificate space; it says
that one specific belief, that exhaustive search over $n$ binary choices cannot be beaten by much,
is wrong. Computational irreducibility concerns *simulation* of a given run. These are different
quantities, and an algorithm that beats brute-force search does not by that fact shortcut the
simulation of any system. Nothing proved or reported here refutes computational irreducibility, and
the first two items above prove weak forms of it. A real argument against the thesis would be a
theorem of the form "for a natural class of systems $X$, the state after $t$ steps is computable in
time $o(t)$", together with evidence that physical systems belong to $X$. The repository has no
such theorem; this is recorded as an open target.

**Conjecture 7.1** (a presentation-relative form). For the rewriting regimes of §1, whether the
$t$-step state of a family of runs has a shortcut depends on the presentation only up to
polynomial-time faithful translation (Proposition 6.1), so "irreducible" is meaningful for a family
of runs, not for a single run. A single finite run is always reducible: its result can be stored.

## 8. Ledger

| Claim | Label | Evidence |
|---|---|---|
| Rewriting over admitted marks is Turing-universal; halting and NF reach undecidable | Lean | `COMP-C5-*`, `COMP-C6-*`, `COMP-C7-*` |
| Unbounded supply of fresh marks | Imported assumption | `COMP-C4-UNBOUNDED-SUPPLY-IMPORT` |
| Step-bounded reach (unary $t$) in NP | Prose | Prop. 2.1 |
| Step-bounded reach NP-complete for some rule lists | Imported | Prop. 2.2 |
| One-bit tag in linear time, $b\ge2$-bit tag NP-complete | Prose + Imported | Prop. 3.1; checks |
| Signs from orientation, cancellation and exchange | Lean (a), (b); Mathlib + Prose (c) | §4.1; checks |
| Balance decided by chord signs | Lean | `FSP-SWITCHING-NORMAL-FORM` |
| Frustration index of the all-negative signing is $\lvert E\rvert-\mathrm{maxcut}$, so NP-hard | Prose + Imported | Prop. 4.3; checks |
| $\Phi_1$ over $\mathbb Q$ is an LP; integral on graphs | Lean + Imported | Prop. 4.4; checks |
| $\Phi_1$ over $\mathbb Z/p$ NP-hard on 2-complexes, every prime $p$ | Conjecture | Conj. 4.5 |
| ETH is false | Reported, unchecked | §5.2 |
| Degree-3 signed sums are $\#4$-SAT counts with $n+2m$ variables | Prose | Prop. 5.1; checks |
| Subexponential exact Hadamard–CCZ amplitudes at linear size | Conditional on the report | Cond. 5.2 |
| P and NP invariant under polynomial-time faithful translations | Prose | Prop. 6.1 |
| Computational irreducibility refuted | Not claimed | §7 |

**Candidate DAG nodes.** Propositions 3.1, 4.3, 5.1 and 6.1 and Conjecture 4.5 are candidates for
new nodes in the COMPUTATION and FERMION_SIGN stages, with Lean formalization of 3.1(1), 4.3 and 5.1
as the natural next step (each is a finite combinatorial statement). They are not added to the DAG
by this note.

## References

- R. V. Book and F. Otto, *String-Rewriting Systems*, Springer, 1993.
- F. Barahona, On the computational complexity of Ising spin glass models, *J. Phys. A* 15 (1982)
  3241–3253.
- M. Blum, A machine-independent theory of the complexity of recursive functions, *J. ACM* 14
  (1967) 322–336.
- S. A. Cook, The complexity of theorem-proving procedures, *STOC* 1971, 151–158.
- cslib-community, Port OpenAI's ETH refutation (subexponential #k-SAT) natively into complexitylib,
  issue 1226, https://github.com/cslib-community/complexitylib/issues/1226 (read 2026-10-27).
- M. Cygan et al., *Parameterized Algorithms*, Springer, 2015, Chapter 14.
- C. M. Dawson, H. L. Haselgrove, A. P. Hines, D. Mortimer, M. A. Nielsen and T. J. Osborne,
  Quantum computing and polynomial equations over the finite field $\mathbb Z_2$, *Quantum Inf.
  Comput.* 5 (2005).
- A. Ehrenfeucht and M. Karpinski, The computational complexity of (XOR, AND)-counting problems,
  ICSI technical report, Berkeley, 1990.
- M. R. Garey, D. S. Johnson and L. Stockmeyer, Some simplified NP-complete graph problems,
  *Theoret. Comput. Sci.* 1 (1976) 237–267.
- J. Hartmanis and R. E. Stearns, On the computational complexity of algorithms, *Trans. AMS* 117
  (1965) 285–306.
- C. Huang, M. Newman and M. Szegedy, Explicit lower bounds on strong quantum simulation,
  arXiv:1804.10368, 2018.
- R. Impagliazzo and R. Paturi, On the complexity of $k$-SAT, *J. Comput. Syst. Sci.* 62 (2001)
  367–375.
- R. Impagliazzo, R. Paturi and F. Zane, Which problems have strongly exponential complexity?,
  *J. Comput. Syst. Sci.* 63 (2001) 512–530.
- R. M. Karp, Reducibility among combinatorial problems, in *Complexity of Computer Computations*,
  1972, 85–103.
- L. G. Khachiyan, A polynomial algorithm in linear programming, *Soviet Math. Dokl.* 20 (1979)
  191–194.
- J. Klassen and B. M. Terhal, Two-local qubit Hamiltonians: when are they stoquastic?, *Quantum* 3
  (2019) 139.
- M. Marvian, D. A. Lidar and I. Hen, On the computational complexity of curing non-stoquastic
  Hamiltonians, *Nature Commun.* 10 (2019) 1571.
- A. Montanaro, Quantum circuits and low-degree polynomials over $\mathbb F_2$, *J. Phys. A* 50
  (2017) 084002.
- OpenAI, Building scientific understanding with academic communities,
  https://openai.com/index/building-scientific-understanding-with-academic-communities/ (read
  2026-10-27).
- A. Schrijver, *Theory of Linear and Integer Programming*, Wiley, 1986.
- P. W. Shor, Algorithms for quantum computation: discrete logarithms and factoring, *FOCS* 1994,
  124–134.
- M. Troyer and U.-J. Wiese, Computational complexity and fundamental limitations to fermionic
  quantum Monte Carlo simulations, *Phys. Rev. Lett.* 94 (2005) 170201.
- S. Wolfram, *A New Kind of Science*, Wolfram Media, 2002.
