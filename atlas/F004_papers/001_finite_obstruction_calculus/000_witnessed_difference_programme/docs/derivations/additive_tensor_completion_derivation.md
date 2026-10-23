# Additive alternatives, signed completion, and universal tensor composition

**AuthorityEffect:** None.

**Status:** finite algebraic derivation with core-only Lean 4.33.1 proofs and
independent exact-integer Python replay.

**Dependency:**
[`generative_histories_contextual_compression_derivation.md`](generative_histories_contextual_compression_derivation.md).

This supplement closes the next dependency after typed histories and their
question-preserving contextual quotient:

\[
\text{typed histories}
\longrightarrow
\text{finite alternatives}
\longrightarrow
\text{signed differences}
\longrightarrow
\text{biadditive composition}
\longrightarrow
\text{algebraic tensor object}.
\]

The construction is exact and universal.  It is also deliberately narrower
than quantum theory.  It does not derive complex scalars, a dagger, positivity,
a norm, Hilbert completion, probabilities, or the Born rule.  The word
“tensor” below means the tensor product of free abelian groups with respect to
biadditive maps.

## 1. What is being added

Let $X$ be a declared type of admitted generators.  Depending on the adapter,
$X$ can be:

- primitive events;
- complete typed histories in a fixed hom-set;
- contextual-equivalence classes of histories;
- checked local witnesses; or
- any other explicitly admitted finite carrier.

The construction does not decide which of these carriers is intended.  In
particular, applying it to histories treats each history as one generator of a
formal alternative.  It does not erase the order *inside* that history.

Three operations are now admitted in sequence.

1. A finite collection of alternatives may be combined without ordering the
   alternatives.
2. Formal negatives may be introduced, so one combination can be subtracted
   from another.
3. Two independently supplied signed systems may be combined by a map required
   to be additive in each input.

Each operation introduces equations that were absent from the typed history
category.  Keeping those equations visible is the main point of the
derivation.

## 2. Free finite alternatives

Let $X^*$ be the finite words on $X$.  For a commutative monoid
$M=(M,0,+)$ and an interpretation $f:X\to M$, define

\[
\llbracket []\rrbracket_f=0,
\qquad
\llbracket x::w\rrbracket_f=f(x)+\llbracket w\rrbracket_f.
\]

**Definition AT1 (alternative equivalence).** For $u,v\in X^*$, put

\[
u\equiv_{\mathrm{alt}}v
\quad\Longleftrightarrow\quad
\forall(M,0,+)\ \forall f:X\to M,
\ \llbracket u\rrbracket_f=\llbracket v\rrbracket_f,
\tag{AT-1}
\]

where the first quantifier ranges over commutative monoids.

This relation is an equivalence.  Concatenation respects it in both arguments,
because evaluation sends concatenation to addition.  Define

\[
\mathsf{Alt}(X)=X^*/{\equiv_{\mathrm{alt}}},
\qquad
0=[[]],
\qquad
[u]+[v]=[u{+\!+}v],
\qquad
\eta_X(x)=[[x]].
\]

The quotient is a commutative monoid.  Commutativity is not a fact about list
concatenation; it holds because every interpreting target is commutative.

**Theorem AT2 (free-alternative theorem).** For every commutative monoid $M$
and map $f:X\to M$, there is a unique commutative-monoid homomorphism

\[
\widehat f:\mathsf{Alt}(X)\longrightarrow M
\]

such that $\widehat f\eta_X=f$.

*Proof.* Define $\widehat f([w])=\llbracket w\rrbracket_f$.  Equation (AT-1)
makes this independent of the representative.  Empty-word and concatenation
evaluation prove preservation of zero and addition.  For uniqueness, every
word is a finite sum of singleton words, so any zero/addition-preserving map
with the declared singleton values agrees with $\widehat f$ by induction. □

For finite $X$, or more generally for finite-support functions, this quotient
has the familiar concrete model

\[
\mathsf{Alt}(X)\cong\mathbb N^{(X)}.
\tag{AT-2}
\]

The isomorphism counts generator occurrences.  Equal counts imply equal
evaluation in every commutative monoid by permutation and associativity.
Conversely, evaluation in the count monoid itself separates unequal count
vectors.

### 2.1 The exact information loss

Alternative formation introduces precisely the commutative-monoid equations:

\[
u+(v+w)=(u+v)+w,
\qquad
u+v=v+u,
\qquad
u+0=u.
\]

Thus the formal alternatives $[a,b,a]$ and $[a,a,b]$ are equal, while
$[a,b,a]$ and $[a,b]$ remain different.  If $a$ and $b$ are themselves
ordered histories, their internal order is untouched.

This is a new carrier, not a safe compression of histories for all questions.
A question about “which alternative was proposed first” does not descend to
$\mathsf{Alt}(X)$.  Such a question must either remain on the ordered proposal
history or be removed from the protected question family explicitly.

## 3. Signed completion

A signed word is a pair $(p,n)\in X^*\times X^*$.  In an abelian group
$G=(G,0,+,-)$ it evaluates as

\[
\llbracket(p,n)\rrbracket_f
=
\llbracket p\rrbracket_f-\llbracket n\rrbracket_f.
\]

**Definition AT3 (signed equivalence).** Put

\[
(p,n)\equiv_{\pm}(p',n')
\quad\Longleftrightarrow\quad
\forall G\ \forall f:X\to G,
\ \llbracket(p,n)\rrbracket_f=
\llbracket(p',n')\rrbracket_f,
\tag{AT-3}
\]

with $G$ ranging over abelian groups.  Set

\[
\mathsf{Diff}(X)
=(X^*\times X^*)/{\equiv_{\pm}}.
\]

Pairwise concatenation defines addition; swapping the pair defines negation:

\[
[(p,n)]+[(q,m)]=[(p{+\!+}q,n{+\!+}m)],
\qquad
-[(p,n)]=[(n,p)].
\]

The class of $([],[])$ is zero, and

\[
\iota_X:\mathsf{Alt}(X)\to\mathsf{Diff}(X),
\qquad
[p]\mapsto[(p,[])],
\tag{AT-4}
\]

preserves zero and addition.

**Theorem AT4 (free signed group).** $\mathsf{Diff}(X)$ is the free abelian
group on $X$.  Every map $f:X\to G$ into an abelian group has a unique group
homomorphism

\[
\widetilde f:\mathsf{Diff}(X)\to G,
\qquad
\widetilde f([(p,n)])=
\llbracket p\rrbracket_f-\llbracket n\rrbracket_f.
\]

*Proof.* Signed equivalence is defined to make the displayed map well defined.
Pairwise concatenation and pair swapping become addition and negation under
every group interpretation, which proves the group laws on the quotient.
Every signed class is

\[
[(p,n)]=\iota_X([p])-\iota_X([n]).
\tag{AT-5}
\]

A homomorphism is therefore determined by its values on positive singleton
classes, and induction over $p$ and $n$ proves uniqueness. □

**Theorem AT5 (Grothendieck extension).** If
$h:\mathsf{Alt}(X)\to G$ is a commutative-monoid homomorphism into the
underlying monoid of an abelian group $G$, there is a unique group
homomorphism $\overline h:\mathsf{Diff}(X)\to G$ satisfying

\[
\overline h\,\iota_X=h.
\tag{AT-6}
\]

*Proof.* Apply AT4 to $x\mapsto h(\eta_X(x))$.  AT2 shows that the restriction
of the resulting group map along $\iota_X$ equals $h$.  AT4 gives uniqueness. □

Equation (AT-6) is the universal property of the Grothendieck completion.  In
the concrete count model,

\[
\mathsf{Diff}(X)\cong\mathbb Z^{(X)}.
\tag{AT-7}
\]

For finite $X$ with decidable equality, $\iota_X$ is injective: a coordinate
map into $\mathbb Z$ separates any two distinct nonnegative count vectors.

### 3.1 What signing adds and what it does not

Signed completion adds additive inverses and hence cancellation:

\[
z+(-z)=0.
\]

It does not assert that a negative coefficient is an empirical probability, a
physical negative mass, or an executable reverse operation.  It is a formal
difference.  Turning a formal difference into a permitted repair still needs a
realization map and an authorization decision.

This distinction is essential for WDP: the group is a powerful obstruction
carrier precisely because it can record a difference that the native system
cannot necessarily execute.

## 4. Extending sequential composition

Let $\mathcal H_Q$ be the contextual history category constructed in the
previous supplement.  For every endpoint pair define the signed hom-group

\[
\mathbb Z\mathcal H_Q(x,y)
=\mathsf{Diff}(\mathcal H_Q(x,y)).
\]

Composition of contextual-history classes is a map

\[
\mathcal H_Q(x,y)\times\mathcal H_Q(y,z)
\longrightarrow
\mathcal H_Q(x,z).
\]

AT4 extends it uniquely, one argument at a time, to a biadditive operation

\[
\mathbb Z\mathcal H_Q(x,y)\times
\mathbb Z\mathcal H_Q(y,z)
\longrightarrow
\mathbb Z\mathcal H_Q(x,z).
\tag{AT-8}
\]

For four generator histories its value is the expected distributive formula:

\[
([p]-[p']);([q]-[q'])
=[p;q]-[p;q']-[p';q]+[p';q'].
\]

Associativity holds because both sides of the associativity equation are
triadditive and agree on all triples of generators, where they reduce to
associativity in $\mathcal H_Q$.  The signed singleton of the empty history is
the identity.  Thus the construction gives the free preadditive category on
the contextual history category.

The Lean theorem `extendBinary_unit_unit` proves preservation of the declared
generator operation, and `extendBinary_add_left` and
`extendBinary_add_right` prove its canonical biadditive extension.  The current
Lean file does not package the endpoint-indexed hom-groups as a preadditive
category; the preceding associativity proof is the written dependent-family
argument.

## 5. Independent composition and the tensor object

Let $X$ and $Y$ be the generators of two signed systems.  Define

\[
\mathsf T(X,Y)=\mathsf{Diff}(X\times Y).
\tag{AT-9}
\]

The generator pairing $(x,y)\mapsto[(x,y)]$ extends uniquely in each argument
to

\[
\otimes:
\mathsf{Diff}(X)\times\mathsf{Diff}(Y)
\longrightarrow
\mathsf T(X,Y).
\]

For finite coordinates $a\in\mathbb Z^{(X)}$ and
$b\in\mathbb Z^{(Y)}$,

\[
(a\otimes b)_{x,y}=a_xb_y.
\tag{AT-10}
\]

**Theorem AT6 (universal biadditive factorization).** Let $G$ be an abelian
group and let

\[
B:\mathsf{Diff}(X)\times\mathsf{Diff}(Y)\to G
\]

be additive in each argument.  There is a unique group homomorphism

\[
\overline B:\mathsf T(X,Y)\to G
\]

such that

\[
\overline B(a\otimes b)=B(a,b)
\quad\text{for all }a,b.
\tag{AT-11}
\]

*Proof.* On a pair generator define

\[
(x,y)\longmapsto B(\iota_X\eta_X(x),\iota_Y\eta_Y(y)).
\]

AT4 gives a unique homomorphism $\overline B$ from
$\mathsf{Diff}(X\times Y)$.  For fixed generator $x$, both sides of (AT-11)
are group homomorphisms in $b$ and agree on every generator $y$, so AT4 makes
them equal.  Holding $b$ fixed and applying AT4 in the left argument proves
(AT-11) for all $a$.  Any competing factor agrees with $\overline B$ on every
pair generator and hence is equal to it by AT4. □

This proves

\[
\mathsf{Diff}(X)\otimes_{\mathbb Z}\mathsf{Diff}(Y)
\cong
\mathsf{Diff}(X\times Y)
\]

for the free signed carriers, by the defining universal property of the
algebraic tensor product.

### 5.1 Pure and non-pure tensors

The tensor carrier is generated by pure tensors but its elements need not be
pure.  With two left and two right generators, the coordinates

\[
T_{a,x}=1,
\qquad
T_{b,y}=1,
\qquad
T_{a,y}=T_{b,x}=0
\]

form the matrix

\[
\begin{pmatrix}1&0\\0&1\end{pmatrix}
\]

whose determinant is $1$.  Every pure $2\times2$ integer tensor has rank at
most one and determinant zero, so this element is not pure.  The Python replay
retains this exact witness.

This is algebraic non-factorability.  Calling it physical entanglement would
require states, allowed local operations, a positive readout, and the selected
physical composite carrier.

## 6. Relation to the cochain shadow

The occurrence-chain map from the previous supplement,

\[
n:\operatorname{Path}_\Sigma(x,y)\to\mathbb Z^{(E)},
\]

extends uniquely to a group homomorphism from signed formal combinations of
histories.  The boundary equation remains linear:

\[
\partial_1\!\left(\sum_i k_i n(p_i)\right)
=
\sum_i k_i\bigl([t(p_i)]-[s(p_i)]\bigr).
\]

This exposes two different commutativizations:

1. $\mathsf{Diff}(\mathcal H_Q(x,y))$ forms signed sums of whole contextual
   histories.  It retains the internal ordered history represented by each
   basis generator.
2. The occurrence map sends each history to an edge-count vector.  It can
   identify internally different histories such as $ab$ and $ba$.

The second map therefore has a potentially large kernel.  A vanishing image in
the cochain shadow remains an obstruction statement; it does not reconstruct
an ordered comparison or executable repair.

## 7. What ties WDP, CODA, LGGR, and projection obstruction together here

The shared mathematical object is a typed map between explicitly presented
carriers, together with the kernel information created when the map forgets
structure.

- **WDP:** signed completion supplies the canonical finite difference group.
  An additive observer is a group homomorphism, and an invisible difference is
  an element of its kernel.
- **CODA:** proposals can live in the positive alternative monoid; evaluation
  can pass through signed differences; authorization remains a separate input
  deciding which formal operations may become native transitions.
- **LGGR:** local contributions can be added and paired, while global
  compatibility remains a distinct gluing obligation.  Tensoring local
  carriers does not prove that local sections glue.
- **Projection obstruction:** every additive report factors through the free
  signed carrier.  Its kernel states exactly which formal differences the
  report cannot see.  A sufficient observer is one whose kernel avoids the
  protected difference class, under the declared task.
- **DDC:** a formal signed repair is not automatically realizable.  DDC still
  needs an admissible transition witnessing that the algebraic correction can
  be performed on the source carrier.

These are substantive connections, not a common checker.  Each subsystem
retains its own admission and validity rules.

## 8. The precise quantum boundary

AT1–AT6 derive an additive tensor calculus over $\mathbb Z$.  They do not
select the Hilbert tensor product used by quantum mechanics.  The following
data remain absent:

1. a scalar extension, such as $\mathbb Q$, $\mathbb R$, or $\mathbb C$;
2. a conjugate-linear involution or dagger;
3. a positive pairing or positive cone compatible with composition;
4. a null-space quotient and norm completion;
5. normalized states and effects;
6. a probability readout;
7. a physical independence or locality interpretation;
8. a completeness theorem for a quantum circuit language.

The existing `ComplexTensorBalancing` result begins after a particular
two-component complex balance has been declared.  AT6 now supplies the earlier
algebraic tensor universal property that result explicitly lacked.  It still
does not force the declared complex balance or its physical interpretation.

## 9. Machine evidence

Written, mechanized, and executable claims remain distinct.

- Lean source:
  `lean4/WitnessedDifference/AdditiveTensorCompletion.lean`
- Lean receipt:
  `lean4/additive_tensor_completion_axioms.txt`
- exact finite model and independent replay:
  `code/additive_tensor/model.py` and `code/additive_tensor/replay.py`
- retained receipt:
  `code/additive_tensor/reference_receipt.json`
- adversarial tests:
  `code/unit_tests/test_additive_tensor_completion.py`

The Lean module proves the free-alternative fold and uniqueness, the signed
group and Grothendieck extension, canonical biadditive extension, and the
tensor factorization and uniqueness theorems.  Its selected declarations use
only `{propext, Quot.sound}`.  It has no `sorry` and introduces no custom axiom.

The Python checker uses exact integers, binds the receipt to its input problem,
replays the submitted coordinates, rejects non-integer coefficients, and
retains both an order-loss example and a non-pure tensor witness.  It makes no
model calls.

## 10. Next dependency

The next derivation should not jump directly to amplitudes.  It should state
and solve the exact selection problem for a dagger and a positive pairing:

1. declare which history generators admit reversal and prove that reversal
   extends to a contravariant involution on the additive envelope;
2. characterize finite pairings that descend through the contextual quotient
   and compose with the tensor object;
3. quotient by the pairing’s radical and separate positive semidefiniteness
   from faithfulness;
4. show exactly what additional law is required to adjoin an operator
   $J$ with $J^2=-1$ and obtain a complex branch;
5. retain countermodels showing that the additive tensor calculus alone does
   not choose positivity, complex scalars, or Born readout.

Only after this step can a finite GNS-style carrier or exact circuit calculus
be derived without hiding the imports that make it quantum.
