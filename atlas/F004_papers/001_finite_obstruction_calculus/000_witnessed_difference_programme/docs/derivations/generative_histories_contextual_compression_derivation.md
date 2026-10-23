# Generative histories, contextual compression, and the derived cochain law

**AuthorityEffect:** None.

**Status:** finite mathematical derivation with core-only Lean 4.33.1 proofs and
independent Python replay.

**Source baseline:** repository commit
`e2cd90471b89c543f2c240293a971f0ef61d98a1`.

This supplement closes a specific missing dependency in the foundational chain:

\[
\text{presentation}\longrightarrow
\text{admitted generators}\longrightarrow
\text{typed histories}\longrightarrow
\text{contextual compression}\longrightarrow
\text{chain/cochain shadow}.
\]

It does not derive the admitted generators from the glyph `<>`, identify every
Genesis history with a WDP path without an adapter, or derive additive,
probabilistic, complex, tensor, or quantum structure.  Those are later and
separate obligations.

## 1. The seed boundary

The presentation mark `<>` is an external framing convention.  In the actual
Genesis Level 00 contract, presenting a token is inert: `Supply` leaves the
internal regime unchanged.  A datum, form, instance, rule, separation demand,
or transition is present internally only after the corresponding admission.

Consequently, the first object used below is declared data rather than a theorem
about the mark.

**Definition H1 (generating signature).** A typed generating signature is

\[
\Sigma=(O,E,s,t),
\]

where $O$ is a type of objects, $E$ is a type of generators, and
$s,t:E\to O$ give their endpoints.  Equivalently, use a dependent generator
family $E(x,y)$.

This records the exact price of moving beyond the inert seed: objects and
well-typed generating steps have been admitted.  Finiteness, decidable equality,
costs, questions, and equations are not implicit.

For a deterministic partial transition rule

\[
\operatorname{step}:S\times A\longrightarrow S+\{\mathsf{refuse}\},
\]

there is a canonical signature with objects $S$ and

\[
E(x,y)=\{a\in A\mid \operatorname{step}(x,a)=y\}.
\]

Thus a native Genesis transition table enters this theory by supplying its
actual state type, event type, and guarded step function.  It does not enter by
matching names or diagrams.

## 2. Free typed histories

**Definition H2 (history).** Histories are generated inductively:

- $1_x:x\to x$ is the empty history;
- if $e\in E(x,y)$ and $p:y\to z$, then $e;p:x\to z$.

Compatible histories concatenate.  Direct induction gives

\[
1_x;p=p,
\qquad
p;1_y=p,
\qquad
(p;q);r=p;(q;r).
\tag{H-1}
\]

The endpoints are part of the type.  A malformed event list is therefore not a
history with a bad value; it fails to inhabit the requested hom-set.

**Theorem H3 (transition replay).** For the signature constructed from a partial
transition rule, forgetting the endpoint proofs of a typed history produces an
ordered event list whose replay terminates at the history's target.

*Proof.* Induct on the history.  The empty history replays to its source.  For
$e;p$, the subtype carried by $e$ proves that the first transition reaches
the source of $p$; the induction hypothesis completes the replay.  The same
induction proves that event extraction sends typed concatenation to list
append. □

This is the precise generic adapter needed by Genesis.  Applying it to a native
system still requires the real source transition function and its refusal
semantics.

### 2.1 Universal property

Let $\mathcal C$ supply objects $O$, typed arrows, identities, associative
composition, and an interpretation $\llbracket e\rrbracket$ of every generator.
Define

\[
\begin{aligned}
F(1_x)&=1_x,\\
F(e;p)&=\llbracket e\rrbracket;F(p).
\end{aligned}
\]

**Theorem H4 (free-history fold).** The map $F$ preserves concatenation and is
the unique map satisfying the two displayed recursion equations.

*Proof.* Both claims are inductions on the first history.  The empty case uses
the left identity law.  The generating case uses associativity and the
induction hypothesis.  Any competing map obeying the same recursion is equal to
$F$ constructor by constructor. □

This is the universal property that Chapter 17's path carrier needs.  A path
semiring weight, a replay evaluator, or a matrix interpretation is an instance
only after its identities, compositions, and generator map are supplied.

## 3. Questions and two-sided contextual equivalence

For every endpoint pair $x,y$, declare a type of protected questions
$Q(x,y)$.  A question $q\in Q(x,y)$ has an answer type $A_q$ and an
evaluator

\[
\operatorname{ask}_q:\operatorname{Path}_\Sigma(x,y)\to A_q.
\]

No common answer type is required.

**Definition H5 (contextual equivalence).** For parallel histories
$p,p':x\to y$, put

\[
p\equiv_Qp'
\quad\Longleftrightarrow\quad
\operatorname{ask}_q(u;p;v)=\operatorname{ask}_q(u;p';v)
\tag{H-2}
\]

for every compatible prefix $u:a\to x$, suffix $v:y\to b$, and question
$q\in Q(a,b)$.

Including both sides matters.  A history may be exposed by what preceded it,
what follows it, or their interaction.

**Theorem H6 (greatest protected contextual congruence).** The relation
$\equiv_Q$:

1. is an equivalence relation on each hom-set;
2. preserves every current question;
3. is stable under every compatible prefix and suffix;
4. contains every other relation with properties 2 and 3.

Hence it is the greatest two-sided, question-preserving congruence.

*Proof.* Reflexivity, symmetry, and transitivity follow pointwise from equality
in each $A_q$.  Current-question preservation uses empty contexts.  Prefix or
suffix closure follows by absorbing the additional history into the quantified
context and using associativity.

For greatestness, let $R$ preserve current questions and be closed under
prefixes and suffixes.  If $R(p,p')$, prefix closure gives
$R(u;p,u;p')$, suffix closure gives
$R(u;p;v,u;p';v)$, and question preservation gives (H-2).  Thus
$R\subseteq\equiv_Q$. □

This theorem unifies two different requirements in the manuscript:

- a report must preserve the question asked now;
- a compression must preserve every declared future use.

The first alone is insufficient.

### 3.1 The sharp counterexample to current-answer compression

Take one object with loop generators $a,b$.  Let the protected question be

\[
q(p)=[p\text{ is exactly the one-letter word }b].
\]

For $p=1$ and $p'=a$, both current answers are false.  With suffix $b$,

\[
q(1;b)=q(b)=\mathsf{true},
\qquad
q(a;b)=q(ab)=\mathsf{false}.
\]

Thus equal current reports do not imply contextual equivalence.  The executable
receipt retains this exact collision.

## 4. The compressed history category

Let

\[
\mathcal H_Q(x,y)=\operatorname{Path}_\Sigma(x,y)/{\equiv_Q}.
\]

**Theorem H7 (quotient composition).** The rule

\[
[p]_Q;[q]_Q=[p;q]_Q

\]

is well defined.  The empty-history classes are identities, composition is
associative, and each protected question descends uniquely to its corresponding
quotient hom-set.

*Proof.* If $p\equiv_Qp'$, suffix closure gives
$p;q\equiv_Qp';q$.  If $q\equiv_Qq'$, prefix closure gives
$p';q\equiv_Qp';q'$.  Transitivity proves independence of both
representatives.  The category laws descend from (H-1), and question descent is
the empty-context instance of (H-2). □

Because $\equiv_Q$ is greatest, this is the coarsest quotient retaining every
declared question under every declared composition.  It is relative to $Q$:
changing the protected questions changes the quotient.

### 4.1 Finiteness and decidability boundary

A finite signature can generate infinitely many histories whenever it contains
a directed cycle.  The theorem therefore does not imply a finite quotient or a
terminating decision procedure.

Finite procedures are exact under an additional bound or finite semantic
presentation:

- a declared length bound gives a finite, explicitly bounded comparison;
- a finite acyclic graph has no path longer than $|O|-1$;
- a finite transducer semantics can admit partition refinement on its finite
  semantic states, provided the questions and continuation operations factor
  through those states.

The Python procedure reports `max_context_length` in its input and receipt.  It
does not rename bounded search as the unbounded theorem.

## 5. Deriving the boundary law from histories

The cochain complex is a derived abelian shadow of the typed history theory.
It is not present in `<>` and is not required to define (H-2).

For any set $X$, let $\mathbb N^{(X)}$ be the free commutative monoid of finite
multisets.  Its signed completion is

\[
\mathbb Z^{(X)}=
\bigl(\mathbb N^{(X)}\times\mathbb N^{(X)}\bigr)/\sim,

\]

where

\[
(A,B)\sim(A',B')
\quad\Longleftrightarrow\quad
A+B'=A'+B.

\]

The relation is an equivalence because the free commutative monoid is
cancellative.  Pairwise multiset addition supplies group addition, swapping
the pair supplies inverse, and $(0,0)$ supplies zero.  This constructs the
free abelian group without presupposing a real vector space.

Set

\[
C_0=\mathbb Z^{(O)},
\qquad
C_1=\mathbb Z^{(E)}.

\]

For a generator $e:x\to y$, define

\[
\partial_1[e]=[y]-[x].

\]

For a history $p=e_1\cdots e_n:x\to y$, let $n(p)\in C_1$ be its
signed occurrence chain.  Intermediate endpoints cancel, giving

\[
\boxed{\partial_1n(p)=[y]-[x].}
\tag{H-3}

\]

This telescoping identity is proved independently in Lean and checked on all
enumerated small Python histories.

Now declare a set $R$ of proposed comparisons $r:p\Rightarrow q$ between
parallel histories and put $C_2=\mathbb Z^{(R)}$.  Define

\[
\partial_2[r]=n(q)-n(p).

\]

Since $p$ and $q$ have the same endpoints, (H-3) gives

\[
\boxed{\partial_1\partial_2=0.}
\tag{H-4}

\]

For any abelian coefficient group $A$, set
$C^k=\operatorname{Hom}(C_k,A)$ and
$d^kf=f\circ\partial_{k+1}$.  Then

\[
d^1d^0f=f\circ\partial_1\circ\partial_2=0.

\]

The cochain law has therefore been derived from typed composition and matched
comparison boundaries.

### 5.1 What linearization forgets

With one object and loops $a,b$, the histories $ab$ and $ba$ have the
same occurrence chain:

\[
n(ab)=[a]+[b]=n(ba).

\]

They remain distinct ordered histories and can be separated by the exact-word
question.  Therefore the map $p\mapsto n(p)$ is generally not faithful.

Similarly, a proposed comparison $p\Rightarrow q$ contributes a 2-chain
whose boundary closes.  It does not automatically impose the equation $p=q$.
Imposing an equation requires quotienting by the generated congruence; retaining
the comparison as a defect or candidate leaves the histories distinct.

Consequently:

- vanishing abelian obstruction does not construct a rewrite;
- equal edge counts do not reconstruct order;
- a homological certificate and an operational comparison have different
  types;
- recovering an actual comparison from the chain shadow needs a separate
  lifting or completeness theorem.

These are the exact limits needed before WDP uses cohomology as an obstruction
calculus.

## 6. Relation to the existing WDP results

The existing `BehavioralQuotient` theorem handles total actions on states and
finite context words.  H6 generalizes the preservation principle to typed
parallel histories, two-sided contexts, and endpoint-indexed question families.
Neither theorem replaces the other:

- state-action quotients are efficient when histories factor through a finite
  state;
- typed path quotients retain source, target, and surrounding composition;
- an adapter between them requires a proved factorization through the chosen
  state presentation.

The derivation also explains the dependency order of later WDP chapters:

1. Genesis supplies admitted guarded transitions.
2. H2–H4 freely generate typed histories and their interpretations.
3. H5–H7 construct the maximum safe compression relative to declared
   questions.
4. Section 5 adds signed commutative completion and derives the cochain law.
5. Obstruction theory can then evaluate the resulting abelian shadow.
6. Additive alternatives, tensor composition, involution, positivity, and
   quantum readout still require further constructions.

## 7. Evidence and replay

Written claims and their machine evidence remain separate:

- Lean source:
  `lean4/WitnessedDifference/GenerativeHistoryCompression.lean`
- Lean receipt:
  `lean4/generative_history_compression_axioms.txt`
- finite model and checker:
  `code/generative_history/model.py` and
  `code/generative_history/replay.py`
- retained receipt:
  `code/generative_history/reference_receipt.json`
- adversarial tests:
  `code/unit_tests/test_generative_history.py`

The Lean module proves 16 selected declarations using only the admitted core
axioms `{propext, Quot.sound}`.  It contains no `sorry` and no custom axiom.
The executable receipt is source-problem bound and independently recomputed.

Verification commands:

```text
python scripts/verify_finite_derivations.py --lean PATH_TO_LEAN_4_33_1
python -m pytest code/unit_tests/test_generative_history.py -q
python -m generative_history.replay check \
  --receipt code/generative_history/reference_receipt.json
```

## 8. Next dependency

The next foundational theorem should start from the history category just
constructed and derive, with universal properties kept explicit:

1. finite alternative formation as a free commutative monoid;
2. signed completion as its Grothendieck group;
3. sequential bilinearity and the tensor product for independent composition;
4. the exact equations each completion introduces and the distinctions each
   one erases.

Only after those steps is it meaningful to ask which involution, positive
pairing, scalar extension, and readout principles admit a quantum branch.
