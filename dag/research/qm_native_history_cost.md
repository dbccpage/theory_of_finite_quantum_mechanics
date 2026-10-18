# Native history costs and the finite algebra boundary

2026-10-11. Source-backed mathematical proofs, a focused Lean module and exact
native controls. `realizes: null`; `authority_effect: None`; `genesis_effect: None`.

The repeatable positive-cost loop required by the
[projective-history obstruction](qm_projective_history_algebra.md#6-native-history-and-fsp-obligations)
actually occurs in the declared Source-25 transition system. Add one assertion,
then remove it. The complete raw state returns, but the ordered run retains two
events and one assertion addition. This supplies a concrete obstruction to
recovering all native history information from a finite groupoid label.

## 1. Source, admission and horizon

The preserved [twenty-fifth seed](../../001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/prompt/twentyfifth/seed_prompt.md)
defines addition/removal of an assertion as increment/decrement of its
multiplicity. It explicitly asks for **100 changes along each alternative**.
Its chosen readings and source functions are in
[`twentyfifth/state.py`](../../001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/twentyfifth/state.py),
which imports the four assertion changes through
[`ninth/changes.py`](../../001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/ninth/changes.py)
from [`eighth/changes.py`](../../001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/eighth/changes.py).
Removal is enabled only when the selected multiplicity is positive. Diagonal
assertions are allowed. Filling data is carried unchanged by these two events.

The existing native owner
[`genesis_source_execution.rs`](../../../../../omega_engine/crates_rs/omega_wdp/src/genesis_source_execution.rs)
implements those guards, arbitrary-precision multiplicities, every intermediate
raw state, the ordered events and the two addition prices. `Source25Run::then`
requires equality of the complete intermediate raw states and adds prices.
The guarded-schedule owner calls this same replay implementation; it does not
silently admit a refused change as an identity.

All results below concern this **declared** transition system, after a term has
been admitted. In its empty state an assertion is disabled; `AddTerm` is enabled.
That supplied transition rule is not a derivation that an opaque `<>` inscription
forces carrier admission. Nor is this a claim about every Genesis regime.

We distinguish (a) the seed's 100-step request from (b) the mathematical category
of all finite legal histories obtained by allowing repeated application of the
same rules. The infinite conclusions use (b). They do not assert that the source
enumerated an infinite frontier, or change its original 100-step task.

## 2. The native loop and the protected questions

Fix any nonempty validated raw state $x$, a relation $r$ or $s$, and a pair of
existing term indices. Write $a$ for adding at that cell and $b$ for removing
there. If its original multiplicity is $m\ge0$, then

$$m\xrightarrow{a}m+1\xrightarrow{b}m.$$

Both events are enabled in this order. Every other multiplicity, term and filled
triple is unchanged. Let $h=ab:x\to x$, and let $c$ count assertion additions.
Induction gives, for every $k\in\mathbb N$,

$$\operatorname{end}(h^k)=x,\qquad c(h^k)=k,\qquad |h^k|=2k. \tag{NHC1}$$

Thus the histories are distinct even though their complete endpoint states and
all questions about those states agree. The old native tests already checked a
single endpoint/price collision. The advance here is its explicit unbounded
family, the algebraic and quantitative consequences below, and a formal proof
of the one-cell rule rather than inference from the finite checks.

Here $c$ is the **accumulated history addition price** already retained by the
WDP native run. It is not the endpoint's source size, plain-state cost, or
minimum cost of reaching its result class. Those endpoint/minimum questions
stay unchanged on this loop family; the infinite-range conclusion does not
apply to them merely because the same word "cost" is used.

**Future boundary.** For any legal suffix $u$ from $x$, replay from the common
endpoint is identical, while $c(h^ku)=k+c(u)$. Endpoint equality therefore
preserves future admission and future endpoint answers for this deterministic
raw-state interpreter. It does not preserve accumulated prices or past event
occurrences. An exact sufficient report for the protected future-state and
total-price questions can retain the endpoint and the two accumulated prices;
that report has unbounded range and still forgets the ordered past word.
These claims follow directly by induction on the suffix, not from a finite
test's coverage of all future programs.

**Contextual quotient boundary.** If price is among the protected questions,
even the empty two-sided context distinguishes every pair $h^j,h^k$, $j\ne k$.
Consequently the greatest question-preserving contextual congruence in
[GEN-WDP-72](../../001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/derivations/generative_histories_contextual_compression_derivation.md)
has infinitely many classes on this one hom-set in the unbounded closure. This
is a concrete failure of the finite-index premise, not a failure of that
congruence theorem. The WDP source-reflection obligation O02 must name which
questions are being retained.

## 3. Finite reports and a sharp finite-window bound

No finite-valued report $q$ can recover $c(h^k)=k$ for all $k$: exact recovery
would inject the natural numbers into its finite image. More strongly, every
real decoder on a finite report has unbounded absolute price error, because its
finite set of decoded values is bounded above while $k$ is not. If the report
is a functor into a finite groupoid, $q(h)$ has finite order $m\ge1$, yielding
the explicit collision $q(h^m)=q(1_x)$ with prices $m$ and zero. The same label
receives the sharp two-input minimax error floor $m/2$.

For a bounded question set $h^0,\ldots,h^N$ and a budget $K\ge1$ of labels,
the best possible worst absolute error, over **all** reports and real decoders,
is

$$\epsilon^*(N,K)=\frac{\lceil(N+1)/K\rceil-1}{2}. \tag{NHC2}$$

**Lower bound.** Some fiber contains at least $w=\lceil(N+1)/K\rceil$
distinct integers, so its diameter is at least $w-1$. Any single prediction
for its smallest and largest costs has error at least half that diameter.

**Attainment.** Partition $0,\ldots,N$ into consecutive blocks of width $w$,
with a possibly shorter final block. This uses at most $K$ labels. Decode each
block by the midpoint of its endpoints; every error is at most $(w-1)/2$ and
the first full block attains it. For $K>N+1$, $w=1$ and the error is zero.

[`FiniteCostReport`](../../../../../omega_engine/crates_rs/omega_wdp/src/finite_cost_report.rs)
implements this construction with `BigUint`/`BigRational`, no floating point
and no allocation proportional to $N$ or $K$. Zero labels, costs outside the
window and unused labels are refused. It is a static report: with $N=3,K=2$,
costs zero and one share a label, but their $+1$ continuations do not. Hence it
does not certify a congruence or a compositional history quotient.

Within the original 100-step horizon from the empty Source-25 state, first add
one term, then perform $k$ diagonal assertion excursions. For $0\le k\le49$,
the histories have $1+2k\le99$ steps and 50 different assertion prices.
Preserving those prices exactly needs at least 50 **report labels**; six labels
have best error 4, and seven have best error $7/2$. This is not a Hilbert-space
dimension lower bound: finite-dimensional spaces have infinitely many values,
and no perfectly distinguishable operational encoding has been supplied.

## 4. State return, inverses and faithful linearization

Although $b$ undoes $a$ on the selected multiplicity, their recorded composite
$ab$ is not the empty history. In the free history category, concatenation
does not cancel admitted events. Replacing $b$ by an algebraic inverse of $a$
would identify $h$ with the identity and lose both its price and occurrence
questions. The *free groupoid completion* of the history graph instead adjoins
formal inverses of its generators; it does not identify the already separate
native generator $b$ with $a^{-1}$ without another imposed relation.

There is a second, independent obstruction. If an additive cost on a groupoid
takes values in $\mathbb N$ and has identity cost zero, then

$$0=c(gg^{-1})=c(g)+c(g^{-1})\quad\Longrightarrow\quad c(g)=0. \tag{NHC3}$$

So positive native prices cannot extend as a nonnegative additive cost on all
formal inverse arrows. Allowing signed prices may remove this obstruction,
but the negative-cost inverses are then extra operations, not native witnesses.
A groupoid embedding need not be full; no claim here forbids an embedding that
keeps $a,b$ distinct and gives up this nonnegative-cost extension.

Now freely linearize the one-object subcategory generated by $h$. Its algebra
over any supplied field $F$ is $F[t]$, with $h^k$ corresponding to $t^k$.
Its independent basis is infinite. A linear map into a $D$-dimensional algebra
cannot be injective: the images of $1,t,\ldots,t^D$ are linearly dependent.
In particular **no finite-dimensional representation is faithful on this full
free history algebra**, even if it distinguishes individual histories.
For a representation into $M_d(F)$, Cayley-Hamilton strengthens the witness to
a nonzero polynomial of degree at most $d$ in the image of $t$.

Two exact controls separate these notions:

* $T=\left(\begin{smallmatrix}1&1\\0&1\end{smallmatrix}\right)$ has
  $T^k=\left(\begin{smallmatrix}1&k\\0&1\end{smallmatrix}\right)$, so the
  matrix entry recovers every integer $k$, yet $T^2-2T+I=0$.
* The rational orthogonal matrix
  $R=\frac15\left(\begin{smallmatrix}3&-4\\4&3\end{smallmatrix}\right)$
  has infinite order, yet $R^2-\frac65R+I=0$. For the order claim, its
  eigenvalue $z=(3+4i)/5$ cannot be a root of unity: otherwise $z+z^{-1}=6/5$
  would be a rational algebraic integer and hence an integer, a contradiction.
  Thus even an injective unitary encoding of the loop monoid need not be a
  faithful encoding of its free algebra. Infinite order is a written proof;
  the native test checks the exact inverse and polynomial identities.

For the first control, the nonzero free coefficient vector $(1,-2,1)$ has
squared coefficient norm 6 and maps to zero; for the second, $(1,-6/5,1)$ has
norm squared $86/25$ and maps to zero. Protecting this *additional formal*
coefficient norm gives WDP two-input error floors 3 and $43/25$, respectively.
These norms are questions on the declared linearization, not a claim that
Genesis itself has amplitudes or a Born rule.

One may quotient $F[t]$ by a polynomial relation, restrict to a finite window,
or move to an infinite-dimensional algebra. Each is a different premise. A
finite list of histories with a length cutoff is generally not closed under
concatenation; overflow, partial composition or truncation relations must be
declared and their protected questions checked. The earlier finite groupoid
and twisted-algebra theorems remain valid for their declared finite inputs;
they cannot automatically be faithful linearizations of all Source-25 histories.

## 5. Genesis/S(n), FSP and MUB6 consequences

For the [S(n)/MSS-N bridge](../../001_finite_obstruction_calculus/001_sn_mssn/README.md),
this makes the choice of recovery contract concrete. A finite label cannot
have a retraction recovering every protected historical price in this family.
That does not disprove a retraction on a finite declared stage, and a formal
shadow cannot create a new native stage to repair its own lost information.

An FSP sign assigns at most two values to loop powers: if $\sigma(h)=-1$,
$\sigma(h^2)=+1$ already collides with the identity's sign while native prices
are two and zero. If $\sigma(h)=+1$, the first loop already collides. This
conditional diagnostic assumes a declared functorial sign map from the native
histories; none is supplied by a numerical resemblance to an FSP loop. The sign
can faithfully answer its parity question without answering cost questions.

For MUB6, the faithful algebra of the finite projective $\mathbb Z_6^2$ model
is still $M_6(\mathbb C)$ for a nondegenerate twist. A map from these native
histories into that finite label set must lose unbounded exact cost; a matrix
encoding into $M_6(\mathbb C)$ cannot faithfully represent their entire free
linearized loop algebra. Neither fact constrains an arbitrary fourth MUB or
invalidates a restricted operational quotient whose protection contract is
weaker and explicitly justified. Scalar choice, positivity, tensor composition
and available preparations/effects still require independent premises.

## 6. Formal, native and reproduction scope

[`NativeHistoryCost.lean`](../../../../../lean4/NativeHistoryCost.lean), registered
in the existing root Lake package, proves the one-cell loop endpoint, price,
length, distinctness, price additivity, lack of a zero-price continuation,
finite natural-number decoder obstruction and unbounded underestimation, and
the nonnegative-cost inverse obstruction. The hypothesis package has an
explicit Boolean XOR/zero-cost inhabitant. Its 12 printed theorem reports use
only `propext` and `Quot.sound`; the module builds on Lean 4.34.0 without mathlib.
It does not formalize the full Source-25 interpreter, NHC2, Cayley-Hamilton or
the infinite-order rotation argument. NHC2 and the algebra results are written
proofs with the native controls above.

[`native_history_cost.rs`](../../../../../omega_engine/crates_rs/tests/omega_wdp/native_history_cost.rs)
checks actual source replay on zero/large multiplicities and marked states,
prices and occurrences through eight repetitions, refusal before term admission,
finite cyclic collisions, exact matrix identities, all partitions on integer
windows with at most eight costs, and arbitrary-precision/refusal controls.
The independent [source replay driver](../tests/oracles/native_history_cost_replay.py)
calls the preserved Python functions on four excursions with three repetitions
each. Its fixture retains all 28 intermediate states and hashes the imported
source modules; native replay checks those states and enabled-event counts.
This is bounded source/native correspondence, not a universal equivalence proof.

Focused reproduction (from repository root, unless a `cd` is shown):

```console
python omega_engine_projects/finite_qm/tests/oracles/native_history_cost_replay.py --check
cd lean4
lake build +NativeHistoryCost
cd ../omega_engine/crates_rs
cargo test -j 1 --offline --locked -p omega_wdp --test native_history_cost
```

Use the configured shared Cargo target in a worktree. The
[qualification receipt](https://github.com/dbccpage/the_symbol_game/blob/cd6205a801c4fa2e640e805ac556e704b6b51054/_intelligence/primitive_qm_eight_hour/native_history_cost_2026-10-11.json)
records exact commands, versions, exits, warnings, source hashes and scopes.
This block changes research notes, root Lean and native code; it does not alter
the PO-000 release payload or any preserved source archive.
