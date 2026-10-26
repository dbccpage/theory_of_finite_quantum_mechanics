# Faithful representation and relative completeness

GEN-WDP-49–51. Written derivation, exact finite replay, and selected Lean
formalization. AuthorityEffect: None.

## 1. The question and the three distinct achievements

Can a machine change its representation while retaining a proof that every
certified success answers its original question? When does its search find a
success if one exists? This supplement answers those questions for a declared
effective certificate class and constructs a finite relational instance.

Certificate soundness, solution coverage, and search completeness are distinct.
A fourth property, the exclusive status coverage of Chapter 20.2–20.3, does
not imply any of them: an evaluator returning `Undetermined` everywhere could
have perfect status coverage. No existing definition or canonical claim ID
is strengthened by changing its name.

Composition of sound maps, finite constraint gluing, and exhaustive search
are standard mathematical mechanisms. The contribution here is their explicit
assembly with WDP's actual defect domain, original-goal decoding, admitted
presentation changes, and independently replayed continuation records.

## 2. Effective problems and witness systems

A problem instance P contains finite input data, its original answer carrier
A_P, assumptions H_P, authorization requirements J_P, and the semantic solution
predicate Sol_P on A_P. For the effective theorem, answers and certificates
have declared finite encodings. Adequacy of this formal problem for an informal
request is an input obligation; the theorem does not interpret arbitrary prose.

An effective encoder E constructs a witness system S_0 from P. A system S
has an effectively presented witness carrier W_S, a terminating local checker
C_S, and a decoding function d_S into A_P. Its accepted set is

$$
G_S=\{w\in W_S:C_S(w)=\mathsf{true}\}.
$$

Decoding need only be defined on accepted witnesses. One may equivalently
use an optional decoder and make successful decoding part of acceptance.
The Lean `System` uses a total decoder; the Python checker refuses undefined
or ill-typed candidates before decoding them.

The initial representation must satisfy two separately proved laws:

$$
w\in G_{S_0}\Longrightarrow d_{S_0}(w)\in\operatorname{Sol}(P),
\tag{S}
$$

and a supplied effective lifting function ell_0 satisfies

$$
x\in\operatorname{Sol}(P)\Longrightarrow
\ell_0(x)\in G_{S_0},\qquad d_{S_0}(\ell_0(x))=x.
\tag{C}
$$

Computing ell_0 from a *given* solution is different from finding a solution
while encoding P. Section 6 constructs E and ell_0 directly from input tables;
neither consumes a table of global solution bits.

## 3. Transport and the faithful representation theorem

An admitted change S to T supplies backward and forward witness maps b and f,
with checked laws

$$
b(G_T)\subseteq G_S,\qquad f(G_S)\subseteq G_T,
\tag{T1}
$$

$$
d_S(b(w))=d_T(w)\ (w\in G_T),\qquad
d_T(f(v))=d_S(v)\ (v\in G_S).
\tag{T2}
$$

The maps need not be inverse on arbitrary candidates or proof objects. They
preserve the decoded answer on accepted witnesses. A backward-only adapter
can establish soundness but cannot support transfer of exhaustive failure.

For a history S_0 to S_1 to ... to S_k, form

$$
b_h=b_1\circ\cdots\circ b_k,\qquad
f_h=f_k\circ\cdots\circ f_1.
$$

**Lemma 3.1 (composition).** These composites satisfy T1–T2.
For two consecutive changes, apply the inner map's validity law before the
outer map's law. Their decoding equations then telescope. Induction gives
the arbitrary finite history, including the identity history.

**Theorem 3.2 (GEN-WDP-49, faithful representation).** Under S, C and the
admitted transport laws, every accepted terminal witness w in G_Sk decodes
to a solution of P, and

$$
\operatorname{Sol}(P)\ne\varnothing
\quad\Longleftrightarrow\quad G_{S_k}\ne\varnothing.
\tag{FR}
$$

*Proof.* Backward validity gives b_h(w) in G_S0. S makes its decoded value a
solution; T2 identifies that value with d_Sk(w). Conversely, given a solution
x, the explicitly constructed f_h(ell_0(x)) is accepted by C and forward
validity, and decodes to x. These arguments establish soundness for every
accepted witness and coverage for every original solution, respectively.

A solving trace tau contains the root problem, admitted finite history, final
witness, and the checkable bindings between them. Its checker replays those
obligations. Thus, over the admitted trace language, FR yields

$$
\operatorname{Sol}(P)\ne\varnothing
\iff\exists\tau:\operatorname{Check}(E(P),\tau)=\mathsf{Solved}.
$$

Here `Solved` denotes the verified positive existential claim, represented by
Chapter 20's `Proved` status. It is not a new operational authority status.
For a budgeted trace, the reverse implication requires enough admitted fuel
to construct and check that finite trace. A fixed inadequate budget is not
covered by the unbounded existence statement.

**Corollary 3.3 (negative-result transfer).** If forward coverage holds and
G_Sk is proved empty, Sol(P) is empty. A sound-only change cannot use this
corollary: let G_S={1} and G_T be empty. Every target success would decode
soundly, vacuously, while a negative target result says nothing about S.

## 4. Re-entry, evidence scope, and real repairs

Fix an anchor consisting of the original problem, assumptions, authorization
requirements, and witness interpretation. Each re-entry retains that anchor
and checks its parent representation and evidence. Changing assumptions
creates a new anchored problem. A result under an added premise may be reported
conditionally, but it becomes an unconditional answer to P only after that
premise is discharged in P. The reference implementation refuses such changes
inside an existing trace; a new problem requires a new encoding.

Let a frame carry spent count s and fixed ceiling B. A counted step preserves
the anchor and B, sets s'=s+1, and requires s'<=B before execution.

**Theorem 4.1 (GEN-WDP-51, finite re-entry).** After n admitted re-entries,
the anchor is unchanged, s_n=s_0+n, and s_0+n<=B. Proof: induction on the
history, adding the unit debit at each step. Hence a nonempty history cannot
reset its consumed fuel. With positive cost floor delta, the analogous
bound is floor(B/delta). A runtime bound additionally requires terminating
individual operations; this theorem does not bound their wall-clock cost.

The Python `fuel` argument is the *total cumulative ceiling*. A larger value
on resume is an explicit new grant recorded at the existing cursor; it does
not erase earlier spending. The fixed-ceiling theorem applies between grants,
and total spending never exceeds the last grant. A grant record declares an
input allowance; it does not authenticate an institution or account balance.
Encoding and verifier work are outside this unit search-cost model. Each
admitted transport and each candidate evaluation costs one search unit.

Observer compression imposes a further condition. Appendix K.1 requires
definedness, results and protected predicates to be constant on the relevant
fibers. When the compressed report becomes an execution state, future guarded
operations must also descend. A report sufficient for the current answer
need not preserve the search tree. This theorem keeps full witnesses unless
that stronger adapter is supplied.

Likewise, a quotient repair is not yet an action on a problem. For a defect
rho(c) and repair space B, the equality dist(rho(c),B)=0 establishes algebraic
repairability only under the declared attainment hypotheses. A usable repair
must supply a permitted operation c to c' and prove its residual equation,
candidate admissibility, and original-goal decoding. If zero residuals decode
soundly, such a realized zero-residual endpoint solves P. Setting B=V alone
supplies none of these witnesses. The inconsistent cycle below makes every
defect formally repairable under B=V while having no solving endpoint.

## 5. Relative search completeness and honest stopping

Assume a countable effective witness or trace grammar and a terminating
checker. A fair enumeration e is defined independently of success:

$$
\forall w\in W,\ \exists n\in\mathbb N:\ e(n)=w.
$$

**Theorem 5.1 (discovery).** If an admitted accepted finite witness exists,
fair enumeration eventually tests one. Choose its finite index n. Each of
the finitely many earlier checks terminates, so the prefix through n is
eventually checked. Its accepting member forces the prefix scanner to return
a success. Combined with Theorem 3.2, a solvable represented problem is
eventually solved, conditional on persistent admission and sufficient resources.

This proof does not grant an unsuccessful countable search a stopping time.
Finite resource exhaustion returns `Undetermined`; it does not refute P.
An admission policy that blocks all solving witnesses invalidates the
completeness premise. No assertion is made that every Prime/DDC policy meets
that premise. Proposals may fail or temporarily worsen a diagnostic without
changing the accepted mathematical state.

For a finite witness carrier, enumerate it completely and replay every
rejection. A negative result is valid exactly when this coverage is established.
Optional heuristic proposals may occupy at most one slot before each canonical
candidate; they cannot remove or postpone that candidate indefinitely. If the
canonical list has M members, at most 2M candidate checks are required, plus
k separately charged transport checks. Invalid proposals consume their slots.
No monotone-residual assumption is needed for this enumeration theorem.

## 6. A constructive finite class (GEN-WDP-50)

Let V be a finite set of variables, each with an explicitly listed finite
domain D_v. Each constraint i supplies a scope S_i contained in V and a finite
relation R_i contained in the product of D_v over v in S_i. Values use exact
equality. The original solutions are

$$
\operatorname{Sol}(P)=
\{x\in\prod_{v\in V}D_v:\ x|_{S_i}\in R_i\text{ for every }i\}.
$$

For every uncovered variable add the full-domain unary relation D_v. This
uses only scope incidence and input domains. It changes no solution. A local
candidate chooses one row r_i from every relation; its carrier is the finite
product C=product_i R_i. Encoding records these tables without computing Sol(P).

Choose the first occurrence i(v) of each variable in the retained table order.
For every other occurrence i and each a in D_v, define the integer coordinate

$$
\rho(r)_{i,v,a}=\mathbf1_{r_i(v)=a}-\mathbf1_{r_{i(v)}(v)=a}.
$$

**Lemma 6.1 (actual defect).** rho(r)=0 iff every two occurrences of each
variable agree. Equality implies every displayed coordinate is zero. Conversely,
if two values differ, testing the indicator at the first value gives a nonzero
coordinate. Agreement with the selected occurrence gives pairwise agreement.

**Theorem 6.2 (constructive bijection).** Global solutions correspond
bijectively to zero-defect local candidates. Send x to its restrictions. In
the other direction, set $x(v)=r_{i(v)}(v)$. Lemma 6.1 makes this independent of
the occurrence. Each selected row is in its input relation, so the reconstructed
x satisfies every original constraint. Restriction after reconstruction
recovers every row; reconstruction after restriction recovers every value.

This proves S and C for the actual encoder. It also proves that the decoded
answer is unique for a compatible local family; it does not assert that a
problem has only one global solution.

The quantity I(r)=sum abs(rho(r)) is an exact raw inconsistency diagnostic.
Its zero set is precisely the solving local families. The set D=rho(C) of
realizable defects is finite and generally is not a vector space. A proposed
linear observer Q is adequate for zero detection exactly when

$$
D\cap\ker Q\subseteq\{0\}.
$$

Full residual reconstruction instead requires Q to be injective on D, or
(D-D) intersect ker Q contained in {0}. Both conditions refer to actual
realizable defects. A linear-span condition can be sufficient without being
necessary on this constrained domain. The replay uses the complete defect;
it grants no automatic soundness to arbitrary compressed observers.

**Boundary cases.** An empty domain makes the original product empty. If its
variable was uncovered, the added unary relation is empty too. An empty
relation makes C empty. A nullary constraint has the unique empty tuple as
its only possible row, and is false precisely when its row table is empty.
With no variables and no false nullary constraints, there is one empty global
assignment and one compatible local family. Empty products therefore have
size one, not zero.

Canonical mixed-radix row-index enumeration has M=product_i size(R_i)
candidates. The identity history and this enumeration make Theorem 5.1 a
terminating decision procedure, with the stated finite search-unit bound.
The bound is not polynomial in the input size.

## 7. Four constructive presentation changes

All four operations leave the original goal and its anchor fixed. Transport
maps on compatible local families are obtained by gluing, applying the
following assignment maps, and restricting to the new tables.

1. **Variable and value renaming.** Use a bijection on variable names and a
   bijection on each listed value domain. Rename every scope and every row
   with those same maps. Forward assignment applies these maps; backward
   assignment applies their inverses. Table membership is preserved and
   reflected because the maps are bijective. Both assignment round trips are
   identities, so Theorem 6.2 gives both witness maps and their decoding laws.
2. **Exact join.** Replace two relations by their natural join on the union
   scope. A union tuple is in this join iff both restrictions are in the
   original relations. Therefore an assignment satisfies the joined constraint
   iff it satisfies both originals. Both assignment maps are identities.
   This remains true for disjoint scopes, empty tables, and nullary relations.
3. **Checked lossless decomposition.** Replace R on S by its projections on
   S_1,S_2, where the scopes cover S, only after checking
   R=projection_1(R) join projection_2(R). Every original row always survives;
   the extra check excludes spurious rows. The equality gives the reverse
   membership implication and hence identity maps on global solutions.
   This is a theorem about the supplied relation. Universal schema losslessness
   requires the separate FD theorem in Appendix O.6. Later independent edits
   require fresh checking.
4. **Deterministic auxiliary variable.** Supply a new domain and a graph of
   a total function f on the complete product of its declared input domains.
   Add the constraint y=f(x|_S). Extend a solution by that value, and decode
   by dropping y. Every target solution has the required graph value, so both
   round trips hold on solutions. Totality is checked on domain tuples, not
   merely on tuples already known to extend to global solutions.

Thus every finite composition of these operations satisfies Theorem 3.2.
The implementation recomputes every target from its source and operation;
a stored target hash or an asserted preservation flag is insufficient.

## 8. Counterexamples and cross-system interpretation

On Boolean variables x,y,z, the relations x=y, y=z, x=z have two global
solutions. Replacing the last relation by x!=z leaves every local relation
nonempty and produces eight locally admitted row families, but no global
solution. Every family has nonzero raw defect. Q=0 hides all eight failures;
B=V declares every defect algebraically repairable without supplying any
permitted solving endpoint. These are concrete LGGR and WDP distinctions.

A completion-only control solves 3x+1=0 in Q with x=-1/3. No integer solution
exists, since 3 does not divide -1. An embedding of Z in Q therefore supplies
no backward map for that witness. This is the finite-certificate analogue of
LGGR IV's stronger inverse-limit example; it does not replace that example.

For the calculus control, f(x)=x and
g(x)=x+product_(k=0)^10 (x-k)^2 agree at every integer sample 0,...,10.
The added polynomial is nonnegative and positive on an interval, so its
integral is strictly positive. The retained exact coefficient calculation
also computes that positive rational integral. Hence samples alone do not
determine 50. The exact formula f=x has antiderivative x^2/2 and integral 50.
With a declared affine-function assumption, samples at 0 and 1 force slope
one and intercept zero, conditionally giving 50. A collision proves a
separate non-identifiability claim; the original numerical query remains
`Undetermined`. Fuel exhaustion has the same primary status but a different
reason and no collision claim.

CODA/Prime admission and continuation fit the typed history interface only
when their actual implementations discharge its laws. DDC's raw closure
norm and CODA's potentially repair-quotiented closure charge stay distinct.
Their equality is not assumed or required by this construction. Mathematical
proposal, evaluation and authorization retain their separate meanings.

## 9. Executable and formal evidence

The [reference implementation](../code/faithful_representation/core.py) exposes
`encode`, `search`, `check`, and `replay`. `check` validates the submitted
history and witness; it never searches for a replacement candidate. The root
constraint predicate is checked again after decoding. `Refuted` requires full
canonical coverage. Malformed inputs raise admission errors or yield rejected
certificates, never an unsatisfiability claim.

Checkpoint replay recomputes the transport cursor, enumeration cursor, pending
proposal/canonical phase, spent fuel, and parent hashes. Recorded increases
in the total ceiling are separate from re-entry. Changed roots, assumptions,
permissions, witnesses, parents or resource counts refuse. Replay has no model
or network dependency.

The [retained evidence](../code/faithful_representation/evidence/summary.json)
binds the Python sources and eight runs. Independent original-assignment
enumeration checks all **4,096** triples of Boolean binary relations: **2,397**
are satisfiable, and **32,768** local families are compared in total. These
finite counts support the implementation; the written and Lean arguments
establish the general mathematical statements at their declared types.

The two new Lean modules are
[FaithfulRepresentation](../lean4/WitnessedDifference/FaithfulRepresentation.lean)
and [FiniteConstraintRepresentation](../lean4/WitnessedDifference/FiniteConstraintRepresentation.lean).
They prove the witness-system theorem, finite-history composition, forward
coverage requirements, enumeration/discovery laws, fuel/anchor preservation,
constraint gluing, exact indicator defects, unary augmentation, Cartesian
enumeration, and the stated relational transport lemmas. The augmentation
existence proof allows arbitrary index types and uses Classical.choice; the
finite reference algorithm instead scans the supplied scopes. Neither proof
assumes a global solution. The Lean models do not verify Python parsing,
hash implementation, storage, or the full native engine.

Run from the paper's code directory:

```powershell
python -B -m faithful_representation verify
python -B -m faithful_representation replay --directory faithful_representation/evidence/four_transports
```

The test suite is [test_faithful_representation.py](../code/tests/unit_tests/test_faithful_representation.py).
The existing standalone [Lean harness](../scripts/verify_finite_derivations.py)
compiles the new modules and checks source-bound axiom reports. `--write`
refreshes those reports only after successful compilation; ordinary checking
refuses changed sources. The 154 canonical rows retain their original scope.

The completed target is this theorem family and finite realization. It does
not decide every mathematical problem, prove every engine adapter faithful,
close arbitrary guarded-history coherence, or establish physical/continuum
reconstruction. Those remain separate source and mathematical obligations.
