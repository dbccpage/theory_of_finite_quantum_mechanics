# The topology of guarded remove/add schedules

Status: written derivation for the declared paired count-guard family.

This derivation classifies a family extending Appendix P.20's three-pair
counterexample. Its objects are actual legal schedules of tagged removals and
additions on one count key. The classification includes all dimensions of a
specified execution complex. In particular, it determines exactly when legal
swap proofs are connected by legal backtracks, squares and hexagons in this
family.

The argument uses finite posets, convex polytopes and the nerve theorem. These
are admitted mathematical tools. The comparison with a real subspace-arrangement
complement is a homotopy equivalence; it does not assign physical coordinates
to native states or derive a continuum from the count key.

## 1. Count semantics and the declared event presentation

Fix integers \(n\ge2\) and \(1\le c<n\). There are \(n\) tasks, with distinct
event tags

\[
E_n=\{r_1,a_1,\ldots,r_n,a_n\}.
\]

Every event occurs exactly once. The only compulsory precedences are

\[
r_i<a_i\qquad(1\le i\le n).
\]

All \(r_i\) act as a removal on the same count key; all \(a_i\) act as an
addition on that key. Starting at \(q=c\), a removal succeeds exactly when
\(q>0\), and then changes \(q\) to \(q-1\). An addition changes \(q\) to
\(q+1\). Task tags and the pair precedences are retained presentation data.
The native count update alone does not distinguish two removals with different
tags or impose their task precedences.

For a prefix \(u\) of a word satisfying the pair precedences, define its active
tasks by

\[
\operatorname{Act}(u)
=\{i:r_i\text{ occurs in }u\text{ and }a_i\text{ does not}\}.
\]

**Lemma 1 (exact count interpretation).** A pair-respecting word replays
successfully from \(c\) if and only if every prefix has at most \(c\) active
tasks. After every successful prefix,

\[
q=c-|\operatorname{Act}(u)|.
\tag{1}
\]

**Proof.** The empty prefix has count \(c\) and no active tasks. A removal
adds one new active task. It is admitted exactly when the old occupancy is
strictly less than \(c\), equivalently when the new occupancy is at most \(c\).
An addition closes its own active task, because its removal has already
occurred and neither event repeats. It therefore increases the count and
decreases the occupancy by one. Induction gives both assertions. At the full
word the active set is empty, so the count returns to \(c\). In particular,
the successful count never exceeds \(c\); a separate upper-count guard is not
being introduced. \(\square\)

This is the natural-number count kernel of the native five-edit model's
`Remove` and `AddAssertion` at one fixed valid address. Other counts, terms
and filled faces remain fixed. Native replay also requires representable
inputs and the implementation's ordinary resource bounds. The mathematical
statement quantifies over finite \(n,c\), independently of a machine integer
width or an enumeration budget.

## 2. The full execution complex

For a finite set \(E\) of \(m\) events, the permutohedron \(\Pi(E)\) has a vertex
for each ordering of \(E\). Its nonempty faces are ordered partitions

\[
B=(B_1\mid\cdots\mid B_k)
\]

into nonempty blocks. Its vertices are the words obtained by ordering each
block arbitrarily and then concatenating the blocks. A face has dimension
\(m-k\). Its subfaces refine blocks into consecutive ordered subblocks.

**Definition.** The full legal execution complex \(K(n,c)\) is the subcomplex
of \(\Pi(E_n)\) consisting of all faces whose every vertex satisfies the pair
precedences and replays successfully from \(c\). It is a subcomplex because
passing to a subface only removes vertex refinements.

The vertices retain complete tagged histories. An edge swaps two adjacent
events when both resulting words are legal. Two-dimensional faces are the
squares for two disjoint adjacent swaps and the hexagons for three events in
one block. These are precisely the square and braid faces used in Appendix
P.20 for this event family. Higher faces are now expressly included by the
same all-refinements rule.

The following test avoids quantifying over the vertices of an individual
face. Write \(b(e)\) for the block containing event \(e\).

**Lemma 2 (exact face test).** A face belongs to \(K(n,c)\) if and only if

\[
b(r_i)<b(a_i)\quad\text{for every }i,
\qquad
\max_{1\le t\le k}
\#\{i:b(r_i)\le t\le b(a_i)\}\le c.
\tag{2}
\]

**Proof.** Every vertex respects \(r_i<a_i\) exactly when the events occupy
strictly ordered blocks. Equal blocks would allow the opposite ordering.
Assume these strict inequalities. During block \(t\), every active task
belongs to

\[
I_t=\{i:b(r_i)\le t\le b(a_i)\}.
\]

This includes tasks closing in the block, tasks opening in it, and tasks
remaining active across it. Conversely, order all removals in block \(t\)
before all additions in that block. Just after those removals, the active
set is exactly \(I_t\). No task has both events in the block, so this is a
permitted vertex refinement. Hence the maximum occupancy over all prefixes
of all vertex refinements is exactly \(\max_t|I_t|\). Apply Lemma 1.
The endpoints in (2) must be inclusive: a task closing in a block can
overlap a task opening in that same block. \(\square\)

## 3. Contractibility of a full linear-extension complex

For any strict partial order \(Q\) on a finite nonempty set \(E\), let
\(L(Q)\subseteq\Pi(E)\) consist of the faces all of whose vertices are linear
extensions of \(Q\). Equivalently, each relation \(x<_Qy\) must place \(x\)
in a strictly earlier block than \(y\). The poset is finite and acyclic, so
\(L(Q)\) has at least one vertex.

**Lemma 3.** The full complex \(L(Q)\) is contractible.

**Proof.** Fix a linear extension \(e_0\). The rank of any other linear
extension \(v\) is its number of inversions relative to \(e_0\). Within any
face, the order of events in different blocks is fixed. Ordering every block
in reverse \(e_0\)-order gives its unique maximum-rank vertex. Every other
vertex has strictly smaller rank.

For a vertex \(v=(v_1,\ldots,v_m)\), mark the adjacent positions at which
the \(e_0\)-position of \(v_i\) exceeds that of \(v_{i+1}\). Partition \(v\)
into its maximal consecutive decreasing runs relative to \(e_0\), and let
\(F_v\) be the face whose blocks are those runs. Two events in one run occur
in opposite orders in \(v\) and \(e_0\). Since both words extend \(Q\), those
events are incomparable in \(Q\). Thus every refinement of every block is
still a linear extension, and \(F_v\subseteq L(Q)\).

The faces with maximum vertex \(v\) are exactly the faces of \(F_v\) that
contain \(v\). Indeed, each block of such a face must decrease relative to
\(e_0\); it therefore lies within one of the maximal decreasing runs. The
converse follows from the description of the maximum of a face.

Build \(L(Q)\) by adding vertices in increasing inversion rank together
with all faces for which they are the maximum. The first stage is the point
\(e_0\). For \(v\ne e_0\), there is an adjacent inversion, so \(F_v\) has
positive dimension. The new stage is the preceding stage union \(F_v\),
and their intersection is

\[
A_v=\bigcup\{F:F\text{ is a facet of }F_v\text{ and }v\notin F\}.
\tag{3}
\]

Every face of \(F_v\) not containing \(v\) has already been added, whereas
every face containing \(v\) is new. This also shows that an arbitrary order
among vertices of equal rank is harmless.

For completeness, \(A_v\) is contractible in every dimension. Translate
\(v\) to the origin in the affine span of the convex polytope \(F_v\), and
let \(C_v\) be its pointed tangent cone. Choose a linear functional
\(\ell>0\) on \(C_v\setminus\{0\}\). The section

\[
D_v=C_v\cap\{\ell=1\}
\]

is a nonempty compact convex polytope. Each ray through a point of \(D_v\)
meets \(A_v\) at its last point in \(F_v\). The meeting point is unique:
facets through the origin constrain the ray's direction, while the facets
not through the origin impose its finite upper length. To check continuity,
write the latter inequalities as \(f_j(x)\le b_j\), with \(b_j>0\). For
\(u\in D_v\), the final radius is

\[
r(u)=\frac{1}{\max_j\max(f_j(u)/b_j,0)}.
\]

The denominator is positive because \(F_v\) is bounded. Thus
\(u\mapsto r(u)u\) is a continuous bijection with continuous inverse
\(x\mapsto x/\ell(x)\). Consequently \(A_v\cong D_v\), a closed ball
of dimension \(\dim F_v-1\).

Both \(A_v\) and \(F_v\) are nonempty contractible spaces. The inclusion
is an inclusion of finite polyhedral subcomplexes, hence a cofibration, and
it is a homotopy equivalence. The gluing property for a cofibration that is
a homotopy equivalence shows that adjoining \(F_v\) along \(A_v\) preserves
the preceding stage's homotopy type. Induction proves that \(L(Q)\) is
homotopy equivalent to its initial point. \(\square\)

This proof uses the full faces \(F_v\). Connected descending links in a
graph would not establish the asserted all-dimensional contractibility.

## 4. A common cover by task orders

Let \(\mathcal P_{n,c}\) be the finite set of strict partial orders on
\([n]=\{1,\ldots,n\}\) whose width is at most \(c\). Width means the
largest size of an antichain.

For \(P\in\mathcal P_{n,c}\), form the event order \(Q_P\) generated by

\[
r_i<a_i,
\qquad
a_i<r_j\quad\text{whenever }i<_Pj.
\tag{4}
\]

Let \(U_P=L(Q_P)\). The order \(Q_P\) is acyclic: concatenate the two
events of each task in any linear extension of \(P\).

**Lemma 4 (the execution cover).** The subcomplexes \(U_P\) cover
\(K(n,c)\). An intersection

\[
U_{P_1}\cap\cdots\cap U_{P_s}
\]

is nonempty if and only if the directed relation
\(P_1\cup\cdots\cup P_s\) is acyclic. Every nonempty intersection is
contractible.

**Proof.** In any vertex of \(U_P\), simultaneously active tasks are
pairwise incomparable in \(P\). If \(i<_Pj\), task \(i\) has completed
before task \(j\) starts. Hence each occupancy is at most \(c\), proving
\(U_P\subseteq K(n,c)\).

For the converse, take a face \(B\in K(n,c)\), and give task \(i\) the
closed interval

\[
J_i=[b(r_i),b(a_i)].
\]

Define the interval order

\[
i<_{P_B}j\quad\Longleftrightarrow\quad b(a_i)<b(r_j).
\tag{5}
\]

It is irreflexive and transitive. Tasks form an antichain in \(P_B\)
exactly when their intervals overlap pairwise. For closed intervals on a
line, pairwise overlap implies common overlap: the largest left endpoint
is no greater than the smallest right endpoint. Here these endpoints are
integers, so the common point can be chosen at a block index. Conversely,
intervals sharing a point form an antichain. Therefore

\[
\operatorname{width}(P_B)=\max_t\#\{i:b(r_i)\le t\le b(a_i)\}\le c
\]

by Lemma 2. Every vertex of \(B\) respects (4) for \(P_B\), so
\(B\subseteq U_{P_B}\). This proves cover of every cell, not just every
vertex.

For an intersection, combine all the task relations. A directed task cycle
would require a cycle of strict event precedences

\[
a_{i_1}<r_{i_2}<a_{i_2}<\cdots<r_{i_1}<a_{i_1},
\]

so the intersection would be empty. Conversely, if the union is acyclic,
its transitive closure is a strict partial order. A topological ordering of
the tasks gives an event extension by placing each \(r_i,a_i\) consecutively.
The intersection is exactly the full linear-extension complex of the
combined event order. It is contractible by Lemma 3. \(\square\)

## 5. A smaller finite complex with the same nerve

**Definition.** Let \(T(n,c)\subseteq\Pi([n])\) consist of the ordered
partitions of the \(n\) tasks with every block of size at most \(c\).
This is a finite subcomplex of the task permutohedron. It has \(n!\)
vertices, independently of \(c\ge1\).

For \(P\in\mathcal P_{n,c}\), put \(W_P=L(P)\subseteq\Pi([n])\).
Every block of a face of \(W_P\) is an antichain in \(P\), hence has size
at most \(c\). Thus \(W_P\subseteq T(n,c)\).

Conversely, for a face \(B_1|\cdots|B_k\) of \(T(n,c)\), order every
element of an earlier block before every element of a later block and leave
each block unordered. This strict partial order has width
\(\max_j|B_j|\le c\), and its linear-extension complex contains the
face. Hence the \(W_P\) cover \(T(n,c)\).

As in Lemma 4, an intersection of the \(W_P\) is nonempty exactly when
the union of the task relations is acyclic. In that case the intersection
is \(L(Q)\) for the union's transitive closure and is contractible by
Lemma 3. The \(U_P\) and \(W_P\) covers therefore have the same nerve.

## 6. The arrangement complement

Define

\[
M(n,c+1)=\mathbb R^n\setminus
\bigcup_{\substack{S\subseteq[n]\\|S|=c+1}}
\{x\in\mathbb R^n:x_i=x_j\text{ for every }i,j\in S\}.
\tag{6}
\]

For \(P\in\mathcal P_{n,c}\), let

\[
V_P=\{x\in\mathbb R^n:x_i<x_j\text{ whenever }i<_Pj\}.
\tag{7}
\]

**Lemma 5 (the convex cover).** The \(V_P\) form an open cover of
\(M(n,c+1)\). Their nerve is the common nerve of the covers in §§4–5.
All their nonempty finite intersections are convex, hence contractible.

**Proof.** If \(x\in V_P\), coordinates having one common value must
index an antichain in \(P\). There are at most \(c\) of them. Thus
\(V_P\subseteq M(n,c+1)\).

Conversely, for \(x\in M(n,c+1)\), define \(i<_{P_x}j\) exactly when
\(x_i<x_j\). Its antichains are subsets of coordinate tie classes, each
of size at most \(c\). It follows that
\(P_x\in\mathcal P_{n,c}\) and \(x\in V_{P_x}\), proving coverage.

An intersection imposes all the strict inequalities from a union of task
relations. A directed cycle makes those inequalities inconsistent. If the
union is acyclic, assign increasing integer coordinates along a topological
order of the tasks; this satisfies every inequality. The intersection is
then an open convex set defined by finitely many strict linear inequalities.
These are exactly the nonemptiness conditions in Lemma 4 and §5. \(\square\)

## 7. Classification theorem

**Theorem 6 (guarded schedule topology).** For all integers
\(n\ge2\) and \(1\le c<n\), there are homotopy equivalences

\[
K(n,c)\simeq T(n,c)\simeq M(n,c+1).
\tag{8}
\]

**Proof.** Let \(N_{n,c}\) be the finite simplicial complex with vertex
set \(\mathcal P_{n,c}\), in which a nonempty collection is a simplex
exactly when the union of its task relations is acyclic. Lemma 4 and §5
give covers of the finite polyhedral complexes \(K(n,c)\) and \(T(n,c)\)
by subcomplexes with all nonempty intersections contractible. The finite
subcomplex form of the nerve theorem gives

\[
K(n,c)\simeq|N_{n,c}|\simeq T(n,c).
\]

Lemma 5 supplies an open convex cover of \(M(n,c+1)\) with this same
nerve. The open-cover form of the nerve theorem gives
\(M(n,c+1)\simeq|N_{n,c}|\), proving (8). The cover indices, intersections,
and their nonemptiness tests are the same in all three applications.
\(\square\)

The nerve theorem is used in its usual finite good-cover forms: an open
cover with contractible nonempty finite intersections, or a cover of a
finite polyhedral complex by subcomplexes with that property, has the
homotopy type of its nerve. Lemmas 3–5 establish the hypotheses; the theorem
does not assume contractibility merely because intersections are connected.
For precise versions, see Bauer, Kerber, Roll and Rolle, Proposition 4.2
for good subcomplex covers after barycentric subdivision, and Theorem
5.9(1a, 2a) for the open good cover of the paracompact Hausdorff space
\(M(n,c+1)\). Those references are to the reviewed arXiv version 6.

## 8. Exact coherence thresholds and the higher obstruction

**Corollary 7 (components and swap-proof coherence).** Within
\(1\le c<n\):

1. If \(c=1\), \(K(n,1)\) has exactly \(n!\) components, each contractible.
2. \(K(n,c)\) is connected if and only if \(c\ge2\).
3. A connected \(K(n,c)\) is simply connected if and only if \(c\ge3\).

Consequently, for \(c\ge3\), all parallel legal swap proofs in this family
are related by legal backtracks, squares and hexagons. For \(c=2\), some
parallel legal swap proofs are not related by these moves.

**Proof.** For \(c=1\), every block of \(T(n,1)\) is a singleton, so it is
a discrete space of \(n!\) points. Equivalently, a successful capacity-one
schedule must finish each task before starting another; the \(n!\) resulting
vertices of \(K(n,1)\) are isolated.

For \(c\ge2\), \(T(n,c)\) contains the whole one-skeleton of the task
permutohedron: an edge has one block of size two and all other blocks
singletons. That graph is connected. For \(c\ge3\), \(T(n,c)\) also
contains its whole two-skeleton. A two-face has either one block of size
three or two blocks of size two. The two-skeleton of a convex polytope is
simply connected whenever its dimension is at least two: attaching cells
of dimension at least three does not change the fundamental group, and
the full polytope is contractible. The same fact applied to the higher
cells of \(T(n,c)\) shows \(\pi_1(T(n,c))=0\).

For \(c=2\), necessarily \(n\ge3\). Projection onto the first three
coordinates defines

\[
p:M(n,3)\longrightarrow M(3,3).
\]

It has a continuous section. For \(y=(y_1,y_2,y_3)\), set
\(m=\max(y_1,y_2,y_3)\) and put

\[
s(y)=(y_1,y_2,y_3,m+1,m+2,\ldots,m+n-3).
\]

The added coordinates are distinct and exceed the first three, so the
image remains in \(M(n,3)\); \(p\circ s=\operatorname{id}\).
The space \(M(3,3)\) is \(\mathbb R^3\) minus its diagonal line and has
homotopy type \(S^1\). Therefore its nontrivial fundamental group injects
into that of \(M(n,3)\), which cannot be simply connected. Apply (8).

Finally, the two-skeleton of \(K(n,c)\) is its legal swap graph with the
declared squares and hexagons attached. Combinatorial homotopy of paths is
generated by edge backtracks and face-boundary replacements. Higher cells
do not affect the fundamental group. This gives the assertions about legal
swap proofs, with every intermediate schedule still legal. \(\square\)

**Corollary 8 (exact first obstruction degree).** For \(2\le c<n\),
\(K(n,c)\) is \((c-2)\)-connected and is not \((c-1)\)-connected.
Its group \(\pi_{c-1}\) has \(\mathbb Z\) as a retract, and its integral
homology group \(H_{c-1}\) has \(\mathbb Z\) as a direct summand. All its
reduced homology below degree \(c-1\) vanishes.

**Proof.** A \(d\)-face of the task permutohedron, represented by blocks
\(B_1,\ldots,B_k\), satisfies

\[
d=\sum_j(|B_j|-1).
\]

Every block therefore has size at most \(d+1\). In particular, \(T(n,c)\)
contains the entire \((c-1)\)-skeleton of the task permutohedron. Adjoining
all omitted cells to \(T(n,c)\) reconstructs that contractible polytope,
and every such cell has dimension at least \(c\). Cellular approximation,
or the relative homotopy groups of this CW pair, shows that these
attachments do not change components or \(\pi_j\) for \(1\le j\le c-2\).
Thus \(T(n,c)\), and hence \(K(n,c)\), is \((c-2)\)-connected. For \(c=2\)
this assertion means connectedness.

For the lower bound, projection onto the first \(c+1\) coordinates gives
\(p:M(n,c+1)\to M(c+1,c+1)\). For a point \(y\) of the latter space, let
\(m=\max(y_1,\ldots,y_{c+1})\) and append the distinct coordinates
\(m+1,\ldots,m+n-c-1\). This is a continuous section \(s\) of \(p\).
The space \(M(c+1,c+1)\) is a Euclidean space minus its full diagonal,
and has homotopy type \(S^{c-1}\). With a base point and its image under
\(s\), the induced maps on \(\pi_{c-1}\) split the identity of
\(\mathbb Z\). The induced maps on \(H_{c-1}(-;\mathbb Z)\) do the same.
This proves nonvanishing and the stated retractions. For \(c=2\), no
assertion that \(\pi_1\) is abelian or that this retract is a direct-product
factor is needed. Reduced homology below degree \(c-1\) vanishes by
connectedness and the homological consequence of \((c-2)\)-connectivity.
\(\square\)

Capacity therefore fixes the degree of the first possible coherence
obstruction in this family, and the retraction proves that this obstruction
is actually present. The conclusion uses the full complex.

**Corollary 9 (maximal-capacity sphere).** For every \(n\ge2\),

\[
K(n,n-1)\simeq S^{n-2}.
\tag{9}
\]

Its reduced integral homology is \(\mathbb Z\) in degree \(n-2\) and zero
in every other degree.

**Proof.** The only face of the task permutohedron excluded by the block
bound \(n-1\) is its full face, indexed by the single block \([n]\).
Thus \(T(n,n-1)=\partial\Pi([n])\), the boundary of a convex polytope of
dimension \(n-1\). Its boundary is \(S^{n-2}\). As a second description,
\(M(n,n)\) removes only the diagonal line from \(\mathbb R^n\). Orthogonal
splitting into that line and its complement gives

\[
M(n,n)\cong\mathbb R\times(\mathbb R^{n-1}\setminus\{0\})
\simeq S^{n-2}.
\]

Apply (8) and the integral homology of a sphere. \(\square\)

**Explicit chain and cochain witness.** For \(n\ge3\), orient the top cell
of \(\Pi([n])\) and give all its faces compatible cellular orientations.
In the integral cellular chain complex of
\(T(n,n-1)=\partial\Pi([n])\), put

\[
z=\partial[\Pi([n])]\in C_{n-2}(T(n,n-1);\mathbb Z).
\]

Every facet has coefficient \(+1\) or \(-1\), so \(z\ne0\).
The identity \(\partial^2=0\) gives \(\partial z=0\), and
\(C_{n-1}(T(n,n-1);\mathbb Z)=0\) makes \(z\) a nonboundary.
Choose one facet \(F\), and let \(\varphi\) be its coefficient functional
on \(C_{n-2}\). For the actual cellular coboundary
\(\delta\alpha=\alpha\circ\partial\), one has
\(\delta\varphi=0\), because the next chain group is zero, and
\(\varphi(z)=\pm1\). If \(\varphi=\delta\alpha\), then
\(\varphi(z)=\alpha(\partial z)=0\), a contradiction. This is a closed,
non-exact cochain with a specified differential and an explicit separating
cycle.

The displayed coordinates are those of the smaller task complex \(T\).
Theorem 6 transports the nonzero homology and cohomology classes to \(K\);
using the same numerical cochain on native execution cells would additionally
require an explicit corresponding chain map.

The first cases recover and extend the native example. For two tasks at
capacity one, the two complete histories are disconnected. For three tasks
at capacity two, the full execution complex has the homotopy type of a
circle, agreeing with P.20's 54 vertices, 84 edges and 30 squares. For four
tasks at capacity three, ordinary path-proof coherence holds, but the full
complex has \(H_2\cong\mathbb Z\). More generally the maximal-capacity
family has its first nonzero reduced homology in degree \(n-2\).

**Example (four tasks at capacity two).** The task permutohedron
\(\Pi([4])\) is a truncated octahedron. Its boundary has six squares
and eight hexagons. \(T(4,2)\) retains all 24 vertices, all 36 edges and
the six squares; it deletes the interiors of the eight hexagons and the
three-cell. To obtain its homotopy type, remove one interior point from
each of the eight hexagons in the boundary sphere. Radial retraction of
each punctured hexagonal face onto its boundary, fixing that boundary,
gives a deformation retraction of this eight-punctured sphere onto
\(T(4,2)\). Thus \(T(4,2)\) is homotopy equivalent to a wedge of seven
circles. It need not itself be a surface: different removed hexagons can
share an edge. Therefore

\[
H_1(K(4,2);\mathbb Z)\cong\mathbb Z^7,
\qquad H_j(K(4,2);\mathbb Z)=0\quad(j\ge2).
\]

This example also prevents replacing the general-capacity theorem by the
claim that every connected guarded complex has only one hole.

## 9. What the construction preserves

The complex \(K(n,c)\) retains the declared tagged schedules and their
legal local comparisons. The full higher faces are a specified mathematical
extension of the existing two-dimensional swap complex. The theorem does
not assert that the native engine already stores a canonical higher-cell
representation.

The smaller complex \(T(n,c)\) is a finite homotopy model. Equation (8)
does not make it a quotient preserving every native answer, cost or future
continuation. Its vertices are task orders, while those of \(K(n,c)\) are
complete event histories. A behavioral compression would require the
separate preservation and reflection conditions used elsewhere in WDP.

For questions about parallel paths, the two-skeleton suffices. For the
homology and higher homotopy statements in Corollaries 8–9, the full complex is
essential. Discarding its three- and higher-dimensional cells may introduce
additional homology in degree two and above. A rational first-homology
calculation alone is not a proof of simple connectivity.

The proof covers one count key, one removal and addition per task, and the
declared pair precedences. Additional precedence constraints, multiple count
keys, repeated task loops, term creation, identification or filling can change
the cover and its nerve. Theorem 6 supplies an exact classification for this
family; it does not classify all guarded presentations in O03.

## 10. Proof and evidence boundaries

The classification for all sizes and capacities is the written proof in
§§1–8. Its topology
uses the standard nerve theorem, elementary convex-polytope topology and the
ordinary fundamental-group and homology consequences stated above.

The finite Python implementation, formal Lean declarations and their fresh
verification results are recorded separately in the derivation evidence map.
The formal source is
[GuardedScheduleTopology.lean](../lean4/WitnessedDifference/GuardedScheduleTopology.lean).
Its statements concern exact replay and prefix counts, actual tagged block
permutations, the extremal-capacity ordering witness, endpoint constraints,
antichains and a ranked endpoint construction. It does not state the nerve
theorem or the homotopy equivalence (8).
Only the actual declarations and checked finite instances may be described
as mechanized or executed. In particular, a bounded homology replay does not
establish the infinite quantifiers in Theorem 6, and formalizing the block
occupancy criterion alone does not formalize its topological conclusion.

The comparison with the no-\(k\)-equal arrangement belongs to established
arrangement and concurrency mathematics. The contribution here is the
explicit proof connecting the stated WDP native count kernel, its tagged
event presentation, the complete legal face rule and the common finite
cover. It is not a claim to have introduced arrangement complements or the
use of topology in concurrency.

## 11. Prior mathematics and references

The definitions of a \(k\)-equal arrangement and its real complement in
Baryshnikov, Klivans and Kosar, Definitions 2–3, coincide with (6) when
\(k=c+1\). Their Theorem 2.1 attributes the classical homology calculation
to Björner and Welker. The proof here needs none of that general Betti-number
formula: the common cover, finite task model and coordinate retraction
establish the stated consequences directly.

Panov and Tril give a direct prior construction of the task model. Take
\(\mathcal S_c=\{I\subseteq[n]:|I|\le c\}\), with \(1\le c<n\).
Their Construction 4.5 retains exactly the permutohedral faces whose blocks
belong to \(\mathcal S_c\), so \(\operatorname{Perm}(\mathcal S_c)=T(n,c)\).
The diagonal subspaces for larger nonfaces lie inside those for nonfaces of
size \(c+1\), hence their complement \(D_{\mathbb R}(\mathcal S_c)\) is
\(M(n,c+1)\). Their Theorem 4.6 gives a deformation retraction from this
complement to the task complex. The present common-cover proof also derives
this equivalence; the additional WDP statement identifies the declared native
event complex \(K(n,c)\) with that homotopy type.

Execution-space topology for programs sharing capacity-constrained
semaphores is established prior work. Ziemiański's §2 supplies the relevant
programming context. Its state-space convention and the present
all-refinements face convention must be kept distinct; that paper is not
being cited as an unproved identification of the two models.

- Yuliy Baryshnikov, Caroline Klivans and Nicholas Kosar, “On the topology
  of no \(k\)-equal spaces,” 2017,
  [arXiv:1708.00032](https://arxiv.org/abs/1708.00032), Definitions 2–3 and
  Theorem 2.1.
- Anders Björner and Volkmar Welker, “The homology of ‘\(k\)-equal’
  manifolds and related partition lattices,” *Advances in Mathematics*
  110(2), 277–313, 1995. Bibliographic details verified in the preceding
  paper's bibliography; the original article is not needed for this proof.
- Ulrich Bauer, Michael Kerber, Fabian Roll and Alexander Rolle,
  “A Unified View on the Functorial Nerve Theorem and its Variations,”
  *Expositiones Mathematicae* 41(4), 125503, 2023,
  [doi:10.1016/j.exmath.2023.04.005](https://doi.org/10.1016/j.exmath.2023.04.005).
  The statements used above were checked in
  [arXiv:2203.03571v6](https://arxiv.org/abs/2203.03571v6), Proposition 4.2
  and Theorem 5.9.
- Krzysztof Ziemiański, “On execution spaces of PV-programs,” 2015,
  [arXiv:1502.04498](https://arxiv.org/abs/1502.04498), §2.
- Taras Panov and Vsevolod Tril, “Permutohedral complex and complements of
  diagonal subspace arrangements,” 2025,
  [arXiv:2504.04183v1](https://arxiv.org/html/2504.04183v1), Construction 4.5
  and Theorem 4.6. These statements and the arrangement convention in §2
  were checked in the linked source.
