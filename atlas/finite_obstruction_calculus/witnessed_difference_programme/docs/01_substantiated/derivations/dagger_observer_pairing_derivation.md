# Dagger extension, positive observer pairings, and the radical of knowing

**AuthorityEffect:** None.

**Status:** finite algebraic derivation with core-only Lean 4.33.1 proofs and
independent exact-integer replay.

**Dependencies:**

- [`generative_histories_contextual_compression_derivation.md`](generative_histories_contextual_compression_derivation.md)
- [`additive_tensor_completion_derivation.md`](additive_tensor_completion_derivation.md)

This supplement advances the foundational chain by one controlled step:

\[
\text{contextual histories}
\longrightarrow
\text{signed additive envelope}
\longrightarrow
\text{declared dagger}
\longrightarrow
\text{observer Gram form}
\longrightarrow
\text{radical quotient}.
\]

It derives preservation consequences of supplied reversal and observation
data.  It does not derive those data from `<>`, select a unique positive form,
or construct complex Hilbert space or quantum probabilities.

## 1. Reversal on typed histories

Let $\Sigma=(O,E,s,t)$ be a typed generating signature.  A reversal structure
consists of a map

\[
e:x\to y\quad\longmapsto\quad e^\dagger:y\to x
\]

such that $(e^\dagger)^\dagger=e$.  Objects are fixed here.  A more general
object involution can be added, but it is extra data.

The free history reversal is forced recursively:

\[
1_x^\dagger=1_x,
\qquad
(e_1e_2\cdots e_n)^\dagger
=e_n^\dagger\cdots e_2^\dagger e_1^\dagger.
\tag{DP-1}
\]

Direct induction gives

\[
(p;q)^\dagger=q^\dagger;p^\dagger,
\qquad
(p^\dagger)^\dagger=p.
\tag{DP-2}
\]

These equations define a dagger on the free history category.  A native
transition system has this dagger only if every declared reverse event is
actually typed and admitted.  Merely reversing an event list is not enough
when guards or irreversible source edits refuse the reverse run.

### 1.1 Descent through contextual compression

Let $Q(x,y)$ be the protected question family used to form the contextual
history quotient. Reversal descends if and only if the induced contextual
equivalence is invariant under reversal. The following closure condition is
sufficient, but need not be necessary: for every $q\in Q(x,y)$ there is a reversed question
$q^\dagger\in Q(y,x)$ with the same answer type and

\[
\operatorname{ask}_{q^\dagger}(p^\dagger)
=\operatorname{ask}_q(p).
\tag{DP-3}
\]

**Theorem DP1 (dagger descent).** Under (DP-3),

\[
p\equiv_Qp'\quad\Longrightarrow\quad
p^\dagger\equiv_Q(p')^\dagger.
\]

*Proof.* A compatible context around $p^\dagger$ has the form
$u;p^\dagger;v$.  Reversing it gives
$v^\dagger;p;u^\dagger$.  Contextual equivalence of $p$ and $p'$ equates the
answers to the reversed protected question in that reversed context.  Equation
(DP-3) transports the equality back to the original context. □

If the protected questions are not closed this way, the history dagger still
exists before quotienting but need not be well defined on compressed classes.
That failure is a precise presentation obstruction.

## 2. Additive dagger extension

Let $X$ be any generator carrier equipped with an involution
$x\mapsto x^\dagger$.  By the free signed-group theorem, the generator map

\[
x\longmapsto [x^\dagger]
\]

has a unique additive extension

\[
D:\mathsf{Diff}(X)\to\mathsf{Diff}(X).
\tag{DP-4}
\]

**Theorem DP2 (free additive dagger).** The extension satisfies

\[
D(a+b)=D(a)+D(b),
\qquad
D(-a)=-D(a),
\qquad
D^2(a)=a.
\tag{DP-5}
\]

*Proof.* The first two equations are homomorphism laws.  Both $D^2$ and the
identity are group homomorphisms.  On each generator,

\[
D^2([x])=[(x^\dagger)^\dagger]=[x].
\]

Free-group uniqueness makes the two homomorphisms equal everywhere. □

When $X=\mathcal H_Q(x,y)$ and DP1 holds, $D$ sends the signed hom-group from
$x$ to $y$ to the signed hom-group from $y$ to $x$.  Together with (DP-2),
this makes the preadditive history envelope a dagger category.

The Lean module proves the untyped free signed form of DP2.  The typed
endpoint-indexed packaging and DP1 are written proofs because the prior Lean
question family has not yet been extended with a reversed-question operator.

## 3. Dagger on independent composition

Let $X$ and $Y$ carry involutions.  Their product carrier has the componentwise
involution

\[
(x,y)^\dagger=(x^\dagger,y^\dagger).
\]

**Theorem DP3 (tensor-dagger compatibility).** On the universal algebraic
tensor object,

\[
(a\otimes b)^\dagger=a^\dagger\otimes b^\dagger.
\tag{DP-6}
\]

*Proof.* Both sides are biadditive in $a$ and $b$.  On generator units they
both equal $[(x^\dagger,y^\dagger)]$.  Apply free-group uniqueness first in
the right input and then in the left input. □

This is a genuine theorem about the algebraic tensor construction.  It still
does not say that the supplied dagger is an adjoint for a positive pairing.
Reversal and positivity are independent interfaces until compatibility is
proved.

## 4. Observation induces a positive semidefinite form

Let

\[
A=\mathsf{Diff}(X)\cong\mathbb Z^{(X)}
\]

and supply an additive observer

\[
L:A\longrightarrow\mathbb Z^m.
\tag{DP-7}
\]

The coordinate dot product defines the observer Gram form

\[
g_L(a,b)=L(a)^T L(b)
=\sum_{i=1}^mL(a)_iL(b)_i.
\tag{DP-8}
\]

**Theorem DP4 (observer Gram theorem).** The form $g_L$ is symmetric and
biadditive, and

\[
g_L(a,a)=\sum_iL(a)_i^2\ge0.
\tag{DP-9}
\]

Its radical is exactly the observer kernel:

\[
\operatorname{Rad}(g_L)
:=\{a\mid \forall b,\ g_L(a,b)=0\}
=\ker L.
\tag{DP-10}
\]

*Proof.* Symmetry and biadditivity follow from the integer dot product and
additivity of $L$.  Equation (DP-9) is a sum of nonnegative integer squares.
If $L(a)=0$, then $g_L(a,b)=0$ for every $b$.  Conversely, if $a$ is in the
radical, choose $b=a$.  The sum of squares is zero, so every coordinate of
$L(a)$ is zero. □

The same proof shows that the self-null set

\[
\{a\mid g_L(a,a)=0\}
\]

already equals $\ker L$.  Hence, for source states or histories $u,v$,

\[
L(u)=L(v)
\quad\Longleftrightarrow\quad
u-v\in\operatorname{Rad}(g_L)
\quad\Longleftrightarrow\quad
g_L(u-v,u-v)=0.
\tag{DP-11}
\]

Equation (DP-11) is a precise finite connection between observation and
knowing: the presentation knows exactly the signed differences outside its
Gram radical.  The claim is relative to the supplied observer and protected
carrier.  It is not an absolute epistemic assertion.

### 4.1 The radical quotient

The quotient

\[
A_L=A/\ker L
\]

is canonically isomorphic to $\operatorname{im}L$.  The Gram form descends to
$A_L$ and is positive definite there:

\[
[a]\ne0\quad\Longrightarrow\quad g_L([a],[a])>0.
\tag{DP-12}
\]

*Proof.* The first isomorphism theorem gives
$A/\ker L\cong\operatorname{im}L$.  If the descended square norm is zero,
DP4 gives $a\in\ker L$, so $[a]=0$.  Over integers a nonzero sum of squares is
a positive integer. □

This quotient is sharp observer completion for the declared finite linear
report: it removes exactly invisible signed differences and no visible one.
It does not reconstruct source representatives discarded by $L$.

## 5. Dagger-compatible observation

To make the dagger an adjoint symmetry of the Gram geometry, additional data
are required.  Suppose the report carrier has an orthogonal involution $U$ and

\[
L(a^\dagger)=U L(a),
\qquad
U^TU=I.
\tag{DP-13}
\]

Then

\[
g_L(a^\dagger,b^\dagger)
=L(a)^TU^TUL(b)
=g_L(a,b).
\tag{DP-14}
\]

Thus the dagger preserves the pairing and its radical.  Without (DP-13), an
involutive history reversal can change what the observer sees and need not
descend to an isometry of the observer quotient.

For two observer maps $L:A\to\mathbb Z^m$ and
$M:B\to\mathbb Z^n$, the product observer on pure tensors is

\[
(L\otimes M)(a\otimes b)=L(a)\otimes M(b).
\]

The coordinate identity

\[
\|L(a)\otimes M(b)\|^2
=\|L(a)\|^2\,\|M(b)\|^2
\]

gives a positive product form.  It is an admitted choice of product observer;
the algebraic tensor theorem alone does not select it.

## 6. Two nonselection theorems

### 6.1 Positivity is not unique

On the rank-one carrier $\mathbb Z$, both

\[
g_1(x,y)=xy,
\qquad
g_2(x,y)=2xy
\]

are symmetric positive definite integer forms, but $g_1\ne g_2$.  Therefore
the conditions “symmetric” and “positive” do not select a scale, observer, or
readout.

More generally, replacing the Euclidean report product in (DP-8) by any
positive definite integer matrix $W$ gives

\[
g_{L,W}(a,b)=L(a)^TWL(b).
\]

The kernel may remain the same while distances and costs change.

### 6.2 A dagger and positive form do not force complex structure

On rank-one $\mathbb Z$, the identity dagger and $g_1$ exist.  A complex
structure would require an integer endomorphism $J(x)=jx$ with

\[
J^2=-I,
\qquad\text{hence}\qquad j^2=-1.
\]

No integer square is negative.  Thus no such $J$ exists.  The Lean theorem
`no_rank_one_integer_complex_structure` proves this without enumeration.

The additive tensor carrier, dagger, and positive pairing therefore still do
not force complex amplitudes.

## 7. Relationship to WDP, CODA, LGGR, and Projection Obstruction

- **WDP:** the signed difference $u-v$ is visible exactly when it has nonzero
  observer Gram norm.  The radical is a task-relative blind-difference space.
- **Projection Obstruction:** (DP-11) turns report-fiber collisions into a
  kernel/radical equality.  Enlarging an observer removes a blind difference
  exactly when the augmented map sends it to a nonzero report.
- **LGGR:** direct-sum local observers produce a sum of local squares.  Local
  green means every observed local component vanishes; a global conclusion
  still needs the supplied local family to be jointly sufficient for the
  protected defect carrier.
- **CODA:** an evaluation layer may retain the Gram certificate and its bound
  source task.  Authorization still decides whether any proposed quotient,
  repair, or additional observation is permitted.
- **DDC:** zero Gram norm establishes invisibility to $L$, not realizability of
  a corrective transition.  A native repair witness remains separate.

The observer Gram construction is one clean mathematical meeting point.  The
subsystems retain different checker and policy obligations.

## 8. Machine evidence

- Lean source:
  `lean4/WitnessedDifference/DaggerObserverPairing.lean`
- Lean receipt:
  `lean4/dagger_observer_pairing_axioms.txt`
- finite exact model and replay:
  `code/dagger_pairing/model.py` and `code/dagger_pairing/replay.py`
- retained receipt:
  `code/dagger_pairing/reference_receipt.json`
- adversarial tests:
  `code/unit_tests/test_dagger_observer_pairing.py`

The Lean module proves additive dagger extension and involution, componentwise
tensor dagger, exact two-coordinate Gram positivity, radical/kernel equality,
equal-report/null-difference equivalence, nonunique positive forms, and the
rank-one obstruction to an integer complex structure.  Its selected
declarations use only `{propext, Quot.sound}` and contain no admitted proof or
custom axiom.

The Python replay checks an involutive coordinate permutation, tensor-dagger
compatibility, a nonzero blind difference, a visible difference of norm square
$5$, and radical/kernel equivalence on all $5^3=125$ vectors in the declared
box.  This exhaustive box is regression evidence for the general Lean theorem,
not the theorem’s proof.

## 9. Next dependency: finite Hermitianization

The next derivation must state the additional data that turns the real or
rational radical quotient into a complex pre-Hilbert carrier:

1. choose a coefficient extension on which division and normalization claims
   are actually defined;
2. supply an endomorphism $J$ with $J^2=-I$;
3. require $J$ to preserve the positive form and satisfy the appropriate
   skew-adjoint law;
4. construct the resulting Hermitian form and prove its radical and tensor
   laws;
5. separate algebraic complexification from analytic completion;
6. retain finite countermodels showing that dagger plus positivity does not
   select $J$, normalization, states, effects, or Born readout.

Only then is there a justified carrier on which exact finite quantum gates can
be defined and audited.
