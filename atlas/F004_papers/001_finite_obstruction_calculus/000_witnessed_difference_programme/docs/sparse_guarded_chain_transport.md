# Sparse integral transport for guarded schedules

This supplement constructs and bounds the chain maps left implicit in
[Appendix P.22](../witnessed_difference_programme.md#p22-exact-topology-and-coherence-thresholds-for-paired-count-guards).
Its input consists of ordered-partition cells with integer coefficients.
Neither the definition nor the evaluation algorithm requires a list of all
legal execution cells or the matrices of the full execution complex.

The minimum-sweep version below has polynomial computation and certificate-size
bounds at every fixed chain degree. The earlier first-descent version is
retained separately: its proved general bound remains exponential. The two
versions use the same carriers and satisfy the same identities, but need not
return the same chains. A polynomial bound is not a measured speed advantage
over a direct checker.

## 1. Cells and their local differential

Fix integers \(n\ge2\), \(1\le c<n\). Use exactly P.22's full legal event
complex \(K=K(n,c)\) and bounded-block task complex \(T=T(n,c)\). Write
\(C_*(-)\) for their ordinary integral cellular chains. A cell on \(m\)
labels is an ordered partition \(F=(B_1|\cdots|B_t)\), with nonempty blocks,
degree \(m-t\), and labels sorted within each block. All labels occur once.

Orient a block \(b_1<\cdots<b_s\) by
\((e_{b_1}-e_{b_s},\ldots,e_{b_{s-1}}-e_{b_s})\), and use the block order
for product orientation. Splitting block \(B_j=L\sqcup R\) into the ordered
pair \(L|R\) has incidence

\[
(-1)^{\sum_{a<j}(|B_a|-1)+|L|+\#\{(x,y)\in L\times R:x>y\}}.
\tag{1}
\]

Sum (1) over every nonempty proper \(L\subset B_j\), with
\(R=B_j\setminus L\), and every nonsingleton block. This is the ordinary
oriented cellular boundary \(\partial\), so \(\partial^2=0\).

Put \(B_q=2^{q+1}-2\) for \(q\ge0\). A degree-\(q\) cell has at most
\(B_q\) facets. Indeed, set \(x_j=|B_j|-1\), so \(\sum_jx_j=q\).
The number of facets is \(\sum_j(2^{x_j+1}-2)\). For nonnegative integers,

\[
(2^{x+y+1}-2)-(2^{x+1}-2)-(2^{y+1}-2)
=2(2^x-1)(2^y-1)\ge0.
\]

Induction gives the bound. It includes \(B_0=0\). Thus computing a boundary
uses subsets of individual supplied blocks, not all ordered partitions.

An event cell is legal precisely when its block indices satisfy

\[
b(r_i)<b(a_i),\qquad
\max_t\#\{i:b(r_i)\le t\le b(a_i)\}\le c.
\tag{2}
\]

This local test was proved in P.22. It checks all vertex refinements without
enumerating those vertices. A task cell is legal when its largest block has
size at most \(c\). Both tests take \(O(n^2)\) elementary operations by a
direct implementation.

## 2. A contraction evaluated on demand

For a strict partial order \(Q\) on \(m\) labels, let \(L(Q)\) contain the
ordered partitions whose every vertex extends \(Q\). Equivalently, every
relation of \(Q\) is strict between blocks. Choose the lexicographically
least linear extension \(w_0\). It can be found by repeatedly selecting the
least remaining minimal label, without enumerating extensions.

The maximum-inversion vertex \(v(F)\) of a cell \(F\), relative to \(w_0\),
sorts each block in decreasing reference rank. For a vertex \(v\), its
maximal decreasing runs are antichains in \(Q\): comparable labels cannot
appear in opposite orders in two linear extensions. The cells with maximum
vertex \(v\) are therefore indexed by subsets \(S\) of its adjacent descent
positions. A position in \(S\) is merged; a position outside it is a cut.

For \(v\ne w_0\), let \(a(v)\) be the first descent. Match the cell
\(\alpha\) indexed by \(S\), with \(a(v)\notin S\), to the cell \(\beta\)
indexed by \(S\cup\{a(v)\}\). Set

\[
V(\alpha)=[\alpha:\partial\beta]\,\beta,
\qquad V(\beta)=0,\qquad V(w_0)=0,
\qquad F_Q=1-\partial V-V\partial.
\tag{3}
\]

Here \([\alpha:\partial\beta]\in\{-1,1\}\) is (1). Every term stays in
\(L(Q)\). The symbol \(F_Q\) denotes a chain operator; it is not one of
the engine's defect functionals.

**Lemma 1 (strict descent).** Apart from the fixed root vertex, every term
of \(F_Q(F)\) has strictly smaller maximum-vertex inversion number than
\(F\).

**Proof.** For an upper matched cell \(\beta\), its only lower matched
facet in the same maximum-vertex fiber is \(\alpha\). The coefficient of
\(\beta\) in \(V\partial\beta\) is one and cancels the identity term.
For a lower cell \(\alpha\), \(\partial V\alpha\) similarly cancels
\(\alpha\). Every remaining same-fiber term corresponds to toggling one
other descent and the distinguished descent in the two possible orders.
The coefficient of their common codimension-two face in
\(\partial^2\beta\) is zero; because both incidences are units, the two
contributions in \(\partial V+V\partial\) cancel. All other facets have
strictly smaller maximum inversion number. Applying \(V\) preserves the
maximum vertex wherever it is nonzero. This proves the assertion. \(\square\)

Let \(R_m=\binom m2\). The chain map \(F_Q\) preserves augmentation,
and the only cell with inversion number zero is \(w_0\). Consequently
\(F_Q^{R_m}=r\epsilon\), where \(r(1)=w_0\) and augmentation is zero in
positive degrees. Define

\[
h_Q=V\sum_{j=0}^{R_m-1}F_Q^j.
\qquad
\partial h_Q+h_Q\partial=1-r\epsilon.
\tag{4}
\]

The identity follows by telescoping, since \(F_Q\partial=\partial F_Q\).
The empty sum at \(m=1\) is zero. Operationally use
\(h_Q(F)=V(F)+h_Q(F_Q(F))\), with \(h_Q(w_0)=0\). Lemma 1 makes this a
terminating evaluation on encountered cells, with no ambient cell list.
Only positive-degree cycles or augmentation-zero zero-cycles are filled.

## 3. The maps and their legal carriers

The following construction applies to either local contraction. For the
polynomial result, use the minimum-sweep contraction now defined, rather than
the first-descent contraction (4).

**Lemma 2 (minimum sweep).** Every \(L(Q)\) has an explicit integral
contraction \(h_Q^{\mathrm{sw}}\) to the same root such that a basis cell
has at most \(R_m=\binom m2\) output cells, each with coefficient \(1\)
or \(-1\). It can be materialized in \(O(m^3)\) label operations.

**Proof.** Choose the first reference label \(x\), which is minimal in
\(Q\). Let \(D_x\) delete the singleton block \(\{x\}\), and be zero
when \(x\) belongs to a nonsingleton block. Let \(I_x\) prepend the
singleton \(\{x\}\). If \(x\) is a singleton in position \(k\), define

\[
s_x(F)=\sum_{j<k}
(-1)^{a_j+|B_j|+t_j}G_j,
\quad a_j=\sum_{h<j}(|B_h|-1),
\quad t_j=\#\{b\in B_j:b>x\},
\tag{4a}
\]

where \(G_j\) deletes the singleton \(x\) and merges it into \(B_j\).
If \(x\) is in a nonsingleton block, set \(s_x(F)=0\). Every crossed
label is incomparable with \(x\): it cannot precede a minimal label, and
if it followed \(x\) in \(Q\), its earlier block in \(F\) would be
illegal. Thus all displayed cells are in \(L(Q)\).

We verify the signed identity

\[
\partial s_x+s_x\partial=1-I_xD_x.
\tag{4b}
\]

When \(x\) is a singleton, splitting \(B_j\cup\{x\}\) as
\(B_j|\{x\}\) or \(\{x\}|B_j\) contributes respectively \(+1\)
and \(-1\). Summing these adjacent positions telescopes to
\(F-I_xD_x(F)\). Splitting any other block cancels between the two
orders of operations: the product-boundary prefix degree changes by one.
For completeness, split the crossed block \(B=A\sqcup C\), write
\(a=|A|\), \(b=|B|\), \(s\) for its prefix degree,
\(u=\operatorname{inv}(A,C)\), and \(t_A,t_C\) for the numbers of
labels exceeding \(x\) in those sets. For the face
\((A\cup\{x\})|C\), the exponents in \(s_x\partial\) and
\(\partial s_x\) differ by one: the first is \(u+t_A\) modulo two,
and \(\operatorname{inv}(A\cup\{x\},C)=u+|C|-t_C\) gives its
opposite in the second. For \(A|(C\cup\{x\})\), the exponents are
\(2s+a+b-1+u+t_C\) and \(2s+a+b+u+t_C\). These also cancel.

If \(x\) lies in a nonsingleton block \(S\cup\{x\}\), only its two
facets \(\{x\}|S\) and \(S|\{x\}\) can contribute to
\(s_x\partial F\). Their terms crossing earlier blocks cancel. The
one additional term that remerges \(S\) and \(x\) has coefficient the
square of its incidence, hence one. Both \(s_x(F)\) and \(D_x(F)\)
are zero, proving (4b) in this case too.

Prepending a singleton is an injective chain map. Commuting (4b) with
\(\partial\) therefore proves that \(D_x\) is a chain map. Recursively
define

\[
h_Q^{\mathrm{sw}}=s_x+I_xh_{Q\setminus\{x\}}^{\mathrm{sw}}D_x,
\qquad
\partial h_Q^{\mathrm{sw}}+h_Q^{\mathrm{sw}}\partial=1-r\epsilon.
\tag{4c}
\]

The second identity follows from (4b) and induction. Use zero contraction
on the one-label complex. A degree-zero input reduces to the chosen root;
a positive-dimensional cell eventually meets a reference label in a
nonsingleton block, where its continuation vanishes.

At a stage with \(r\) remaining labels, at most \(r-1\) terms are
produced. Within a stage they cross different blocks and are distinct.
Between stages, the earlier distinguished label belongs to a nonsingleton
block in the earlier outputs but to a fixed initial singleton in every
later output. Thus their supports are disjoint, their coefficients are units,
and there are at most \(\sum_{r=1}^m(r-1)=R_m\) terms. Writing an unsorted
list of that many cells of length \(m\), computing their prefix signs, and
selecting the reference extension costs \(O(m^3)\) label operations. Ordered
dictionary insertion has an additional comparison cost, included in (12h).
No boundary expansion or list of linear extensions is used. \(\square\)

For an event cell \(A\), define its interval order on tasks by
\(i<_{P_A}j\) iff \(b_A(a_i)<b_A(r_j)\). Its width is at most \(c\):
antichains correspond to pairwise intersecting closed task intervals, which
share a block index, and (2) bounds that overlap. Refining \(A\) adds order
relations, so the task carriers \(L(P_A)\subseteq T\) shrink under faces.

For a task cell \(B\), let \(P_B\) order earlier blocks before later
blocks. For any task order \(P\), form the event order \(Q_P\) generated
by \(r_i<a_i\) and \(a_i<r_j\) whenever \(i<_Pj\). Its linear-extension
complex is legal when \(P\) has width at most \(c\): active tasks are a
\(P\)-antichain. These event carriers also shrink under faces.

Define \(p\) on an event vertex as the root of \(L(P_A)\), and define
\(i\) on a task vertex as its sequential paired event word. In positive
degree put

\[
p(A)=h_{P_A}\bigl(p(\partial A)\bigr),\qquad
i(B)=h_{Q_{P_B}}\bigl(i(\partial B)\bigr).
\tag{5}
\]

Every recursive call in (5) has smaller cell degree. The right-hand side is
a cycle by the lower-degree chain-map identity and \(\partial^2=0\).
At degree zero it has augmentation zero. Nested carriers put the whole
right-hand side inside the displayed contraction's domain. Equation (4)
therefore proves \(\partial p=p\partial\) and
\(\partial i=i\partial\), inductively.

Two carrier containments are essential. If \(B\) occurs in \(p(A)\),
then \(P_A\subseteq P_B\), so \(i(B)\) lies in \(L(Q_{P_A})\).
If \(A\) occurs in \(i(B)\), then \(P_B\subseteq P_A\), so
\(p(A)\) lies in \(L(P_B)\), exactly the closed face \(B\).

Thus \(pi(B)\), in degree \(\dim B\), is a multiple of \(B\). It fixes
vertices. If it fixes all proper faces, the chain-map identity gives
\(\partial(pi(B)-B)=0\); the nonzero boundary of a positive-dimensional
polytope cell forces that multiple to be one. Hence

\[
pi=1.
\tag{6}
\]

Set \(H=0\) in degree minus one and recursively define

\[
H(A)=h_{Q_{P_A}}\bigl(ip(A)-A-H(\partial A)\bigr).
\tag{7}
\]

The cross-containments put every term in the indicated legal event carrier.
The lower-degree homotopy identity makes the argument a cycle; for vertices
its augmentation is zero. Applying (4) proves

\[
ip-1=\partial H+H\partial.
\tag{8}
\]

No agreement of contractions for different posets is assumed. A fixed cell's
carrier and choices are independent of capacity. Thus \(p,i,H\) commute
strictly with the inclusions obtained by increasing \(c\). Equations
(5)–(7) request only individual cells and their boundaries; an implementation
can memoize them but does not need to enumerate \(K\), \(T\), or a cover.

## 4. Explicit size bounds

Use coefficient mass \(\|x\|_1=\sum_F|x_F|\) for estimating the expansion
of a chain. This is a proof estimate for these operators, not a new engine
defect evaluator. Set

\[
D_q=1+B_{q+1}+B_q,
\qquad L_{m,q}=\sum_{j=0}^{R_m-1}D_q^j.
\tag{9}
\]

The columns of \(V\) have mass at most one, while the columns of the two
differentials in (3) have mass at most \(B_{q+1}\) and \(B_q\).
Thus \(\|F_Qx\|_1\le D_q\|x\|_1\) and
\(\|h_Qx\|_1\le L_{m,q}\|x\|_1\). The same geometric sum bounds the
number of signed unit terms in the uncollected expansion tree. Cancellations
and memoization can reduce the actual support.

For the first-descent version use \(L_{m,q}\) from (9). For the
minimum-sweep version, set \(L_{m,q}=R_m\) in every degree instead:
Lemma 2 proves that bound directly. Define \(P_0=I_0=1\),
\(J_{-1}=0\), and, for \(q\ge1\),

\[
P_q=L_{n,q-1}B_qP_{q-1},\qquad
I_q=L_{2n,q-1}B_qI_{q-1}.
\tag{10}
\]

For \(q\ge0\), set

\[
J_q=L_{2n,q}\bigl(I_qP_q+1+B_qJ_{q-1}\bigr).
\tag{11}
\]

**Theorem 3 (sparse transport).** The algorithms (5)–(7) evaluate a
degree-\(q\) chain with \(s\) nonzero coefficients by requesting cells
only in their recursive expansions. The resulting supports have sizes at
most \(sP_q,sI_q,sJ_q\), respectively, and their coefficient masses are
at most \(P_q\|x\|_1,I_q\|x\|_1,J_q\|x\|_1\). These conclusions hold
for all \(n,c\) in the stated range over unbounded integers.

**Proof.** Apply (9) to (5) and induct on degree to obtain (10). In (7),
the composite contributes at most \(I_qP_q\), the input cell contributes
one, and the boundary term contributes at most \(B_qJ_{q-1}\). This gives
(11). Evaluate each of the \(s\) basis-cell images once, multiply by its
original coefficient in binary, and collect equal cells. Every nonzero
integer term has absolute value at least one; the unit-input mass bounds
therefore bound the number of output cells. This algorithm never expands a
binary input coefficient into that many separate copies. \(\square\)

If every input coefficient has magnitude less than \(2^b\), and \(M\)
is the applicable bound \(P_q,I_q,J_q\), each output coefficient needs at
most
\(1+b+\lceil\log_2(sM+1)\rceil\) signed bits. Encoding a cell by its
label list and block breaks needs at most
\(m(\lceil\log_2m\rceil+1)\) bits, with \(m=n\) or \(2n\).
Consequently an explicit output chain can be encoded using

\[
O\!\left(sM\left[n\log(n+1)+b+\log(sM+1)\right]\right)
\tag{12}
\]

bits. No ambient cell indices or full boundary matrix are part of this format.
Zero chains have empty support and are encoded separately.

For a simpler bound on the sweep version through degree \(d\), put

\[
R=\binom{2n}{2},\quad B=2^{d+2}-2,\quad C=\max(2,RB).
\tag{12a}
\]

For \(0\le q\le d\), equations (10)–(11) give

\[
P_q,I_q\le C^q,\qquad J_q\le2R(q+1)C^{2q}.
\tag{12b}
\]

For the last inequality, the base case is \(J_0\le2R\). If it holds at
\(q-1\), then
\(R(C^{2q}+1)\le2RC^{2q}\), and the remaining term is at most
\(2RqC^{2q-1}\le2RqC^{2q}\). This proves (12b). At fixed degree,
\(p\) and \(i\) therefore have \(O(n^{2q})\) unit-column mass and
\(H\) has \(O(n^{4q+2})\). The degree can grow with \(n\), but the
fixed-degree polynomial assertion does not cover that regime.

**Explicit computation bound.** Count cell emissions, coefficient operations
and local structural checks first. A structural check works on at most
\(m=2n\) labels and \(m^2\) order pairs, and can be implemented in
\(O(m^3)\) label operations. Set

\[
U=4(R+1)(B+1).
\tag{12c}
\]

This bounds the term/check operations for one sweep column, collecting its
output and checking its differential: there are at most \(R\) emissions,
\(B\) input facets and \(RB\) output facets, with separate charges for
coefficient accumulation and structural setup. This is an algorithmic
operation model, not a count of CPU instructions.

Let \(W_p(q),W_i(q),W_H(q)\) bound work for a requested basis column,
without assuming any cache hits. The following finite recurrences suffice:

\[
\begin{aligned}
W_p(0),W_i(0)&\le U,\\
W_p(q)&\le B W_p(q-1)+U(1+BC^{q-1}),\\
W_i(q)&\le B W_i(q-1)+U(1+BC^{q-1}),\\
W_H(q)&\le W_p(q)+C^qW_i(q)+BW_H(q-1)\\
&\hspace{1cm}+U(1+C^{2q}+BJ_{q-1}),
\qquad W_H(-1)=0.
\end{aligned}
\tag{12d}
\]

The first two recurrences charge every recursive boundary column, collect
their at most \(BC^{q-1}\) terms, and sweep the result. The last computes
\(p(A)\), requests \(i\) on each of its at most \(C^q\) cells, requests
\(H\) on each boundary facet, then collects and sweeps the residual.
All requests are charged even when a memoized implementation can reuse them.
These are finite expansions of local formulas, not calls to an ambient
enumerator or to an unspecified filling oracle.

Induction, using \(B\le C\), gives
\(W_p(q),W_i(q)\le U(2q+1)C^q\). In the last recurrence, the
nonrecursive terms are bounded by \(8U(q+1)C^{2q}\). Sum the recurrence
using \(B\le C^2\) to obtain

\[
W_H(q)\le8U(q+1)^2C^{2q}.
\tag{12e}
\]

For \(s\) input cells allow a further factor two for binary coefficient
scaling and final collection. A common work bound through degree \(d\) is

\[
T=16sU(d+1)^2C^{2d}.
\tag{12f}
\]

No input coefficient is expanded into repeated unit copies. Set
\(F_d=2R(d+1)C^{2d}\) and
\[
\ell=2+b+\lceil\log_2\max(1,s)\rceil
             +\lceil\log_2((B+1)F_d)\rceil.
\tag{12g}
\]
This bounds signed intermediate coefficient lengths, including uncancelled
boundary terms used in internal checking. The bounds were taken before
cancellation at each stage, so they cover the residual and composite as well
as the final output. With ordinary binary arithmetic and balanced sparse
dictionaries, the bit-operation bound is

\[
O\!\left(T\left[
m^3\log(m+1)+m\log(m+1)\log(T+2)+\ell^2
\right]\right).
\tag{12h}
\]

The three terms account for local carrier/cell work, dictionary comparisons,
and schoolbook coefficient multiplication. At fixed \(d\),
\(T=O_d(s n^{4d+2})\) and
\(\ell=O_d(b+\log(s+1)+\log(n+1))\). This proves polynomial bit
complexity in the sparse input parameters. It is deliberately a loose upper
bound. A full matrix still has a column for every basis cell and is outside
this sparse-input statement.

## 5. Checking a supplied certificate locally

For a legal degree-\(q\) cycle \(z\), equations (5) and (8) give

\[
z\in\operatorname{im}\partial
\quad\Longleftrightarrow\quad
p(z)\in\operatorname{im}\partial.
\tag{13}
\]

If a supplied reduced filling \(b\) satisfies \(\partial b=p(z)\), then

\[
a=i(b)-H(z),\qquad \partial a=z.
\tag{14}
\]

For input supports \(s_b,s_z\), the reconstructed certificate has support
at most \(s_bI_{q+1}+s_zJ_q\). Its mass is at most
\(I_{q+1}\|b\|_1+J_q\|z\|_1\). The checker independently validates
the labels, degree and legality of every supplied cell, computes the boundary
of each cell in \(a\), and compares the resulting sparse chain with \(z\).
It need not trust \(p,i,H\), the producer, or any proposed ambient matrix.

For certificate support \(t\), at most \(tB_{q+1}\) signed incidences
are generated. With sorted cell keys, verification takes

\[
O\!\left((s_z+t+tB_{q+1})
\left[n^2\log(n+1)+n\log(n+1)\log(s_z+tB_{q+1}+2)+b'\right]\right)
\tag{15}
\]

bit operations under ordinary binary addition and a direct cell comparison,
where \(b'\) bounds the bit lengths of coefficients and their accumulated
sums. The quadratic label term includes pairwise comparisons for incidence
signs. This is a bound in the actual certificate size; it requires no
enumeration of other cells.

A nonboundary certificate is a legal cycle \(z\) and a genuinely closed
integer cochain \(\varphi\) with \(\varphi(z)\ne0\). Arbitrary input
cochains are not assumed closed. If a cochain is supplied with finite support
\(S\), every possible nonzero entry of \(\delta\varphi\) belongs to a
coface of a member of \(S\). A codimension-one coface of an ordered partition
merges two adjacent blocks, so there are at most \((m-1)|S|\) candidates.
Generate all these candidates, retain the legal ones, and evaluate
\(\varphi(\partial A)\) on each. This proves closure on the entire complex:
every unlisted cell has no facet in the support and hence evaluation zero.
It is insufficient to check only cells encountered while transporting \(z\).

For a closed task cochain \(\psi\), the pullback \(\psi\circ p\) is a
closed native cochain, and
\((\psi\circ p)(i(y))=\psi(y)\) by (6). Its values on requested chains
can be evaluated sparsely. Its complete coordinate support need not be sparse;
the theorem does not promise a short explicit listing of every nonzero entry
of the transpose map. A claimed global closure certificate must use the
universal chain-map theorem or the complete coface check just described.

## 6. Evidence scope

The all-size statements above are written proofs. Lean's chain-transport
module verifies algebraic consequences of checked linear-map identities;
the separate bound module verifies declared finite arithmetic recurrences.
Neither is a formalization of the complete permutohedral construction or of
the Rust implementation. Fresh build and execution results are recorded in
the companion verification record when available.

The native implementation uses checked integer coefficients and explicit
resource limits. A result accepted within those limits is exact; exceeding
them returns a refusal. The unbounded-integer theorem is not a promise that
every input fits a machine integer or the configured budget. This construction
answers integral boundary questions for the declared full legal-cell model.
It does not identify arbitrary native histories, preserve authorization, or
prove that an obstruction search terminates within a practical budget.
