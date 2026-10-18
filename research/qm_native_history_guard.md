# Native future guards: the exact finite-depth quotient

2026-10-11. Written proofs, constructive Lean and exact native checks.
`realizes: null`; `authority_effect: None`; `genesis_effect: None`.

The [history-price obstruction](qm_native_history_cost.md) leaves a
natural question: if accumulated price is no longer protected, can a finite
report preserve native future legality? For all continuations the answer is
still no, already on one Source-25 assertion cell. For continuations of a
declared bounded length there is an exact, minimal report. Its success does
not supply a native groupoid, a complex scalar field or a quantum state cone.

## 1. Source slice and the protected questions

Fix an existing pair of terms, one relation and every other field of a
validated raw Source-25 state. Let the chosen assertion's multiplicity be
$n\in\mathbb N$. The
[preserved seed](../../001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/prompt/twentyfifth/seed_prompt.md)
and the [native executor](../../../../../omega_engine/crates_rs/omega_wdp/src/genesis_source_execution.rs)
give the following slice:

$$a:n\mapsto n+1,\qquad b:n+1\mapsto n,$$

with $b$ refused at zero. Both moves leave the other raw fields fixed. This
uses an admitted nonempty carrier; assertions on the empty carrier are refused.
It does not prove that the bare presentation `<>` forces a term to be admitted.

For a word $w$ in $a,b$, let $L_n(w)$ be one if every successive native guard
allows execution, zero otherwise. The protected question family at depth $r$
contains **all** words of length at most $r$. Counts, costs, balance queries,
other cells, term identification, term addition and filling are not included
in this report's recovery contract. Refusing an out-of-alphabet query is not
evidence that the underlying native move is disabled.

## 2. Exact quotient and minimality

**NG1.** For every $r,m,n\in\mathbb N$,

$$[\forall |w|\le r,\ L_m(w)=L_n(w)]
\quad\Longleftrightarrow\quad \min(m,r)=\min(n,r).$$

For sufficiency, use induction on the word. At positive depth $r+1$, equal
clipped counts agree on whether the first removal is allowed. Following an
allowed move their clips at depth $r$ agree, because

$$\min(\min(n,r+1)+1,r)=\min(n+1,r),$$
$$\min(\min(n+1,r+1)-1,r)=\min(n,r).$$

The induction hypothesis applies to the remaining word. At depth zero only
the empty word is asked, and it is legal at every count.

For necessity, if the clips differ, interchange $m,n$ if needed so that
$m<n$ and $m<r$. Then $b^{m+1}$ has length at most $r$, fails at $m$ and
succeeds at $n$. This also supplies an explicit distinguishing context.

Thus the exact quotient is

$$Q_r=\{0,1,\ldots,r\},\qquad q_r(n)=\min(n,r).$$

Its last class means **at least $r$**, not exactly $r$. The representatives
$0,\ldots,r$ are pairwise distinguishable, so any sufficient report needs at
least $r+1$ labels. NG1 attains that bound. This is a label-count theorem; it
does not bound Hilbert-space dimension without an additional distinguishability
or orthogonality premise.

**NG2.** Protecting every finite continuation forces an injective report on
$\mathbb N$: every $m<n$ is separated by $b^{m+1}$. In particular, no finite
label set suffices on the unbounded rule closure, even after price is dropped.
This is distinct from the finite search horizon in the original seed.

Within that seed's 100-attempt horizon, one term followed by $m$ additions
reaches count $m$ after $1+m$ changes. A remaining context depth $r\le99$
allows this preparation family through $m=99-r$. Its exact number of guard
classes is $\min(r,99-r)+1$, by NG1 restricted to that interval. In particular,
counts $0,\ldots,49$ can all be prepared and distinguished with at most 49
further attempts inside the original horizon: **50 classes are already
necessary on this slice**. This is not a bound on the entire raw-state space.

## 3. Decreasing depth, composition and explicit boundaries

At depth $r>0$ and clipped count $c\le r$, the report transitions are

$$a:(r,c)\mapsto(r-1,\min(c+1,r-1)),$$
$$b:(r,c)\mapsto(r-1,\min(c-1,r-1))\quad(c>0).$$

At $c=0$, removal yields `GuardRefusal`. At $r=0$, any further event yields
`ContextExhausted`, which makes no claim about its native legality. For
example, after adding once from zero with budget one, removal is natively
legal but beyond the report's remaining scope. Evaluation returns the first
boundary encountered; a refusal already observed inside the budget remains
a refusal when an unexecuted suffix is appended.

Successful prefixes compose with their residual budget: the report after
$uv$ equals the report obtained after $u$ and then $v$. Keeping the same depth
would fail. For any $r\ge1$, counts $r$ and $r+1$ have equal $q_r$ reports,
but their legal removal successors $r-1,r$ have different $q_r$ reports.
Consequently this is a depth-indexed family of exact observers, not a single
finite congruence for unrestricted native continuation.

The reusable [category owner](../../../../../omega_engine/crates_rs/omega_category_theory/src/bounded_counter.rs)
implements clips, transitions and distinguishing removal lengths without
allocating raw count-sized data. It handles `usize::MAX` without increment
overflow. The [Source-25 adapter](../../../../../omega_engine/crates_rs/omega_wdp/src/genesis_guard_report.rs)
reads validated arbitrary-precision native counts, clips before any machine
conversion, and accepts only the chosen cell's add/remove events.

For testing, all successful graded states up to depth $R$ and two distinct
absorbing boundary labels form a total Moore machine. Its declared carrier
has $(R+1)(R+2)/2+2$ states. The canonical Moore owner checks its complete
transition table and behavioral quotient. The boundary labels are records
of observation outcomes, not extra successful native states or moves.

## 4. Coherent finite reports can add a non-native limit point

Depth restriction is $Q_{r+1}\to Q_r$, $c\mapsto\min(c,r)$, and native
profiles satisfy $q_r(n)=\min(q_{r+1}(n),r)$. The saturated profile $c_r=r$
also satisfies every restriction. Yet no finite $n$ represents it: at depth
$n+1$, $q_{n+1}(n)=n<n+1$.

**NG3 (written classification).** The inverse limit of these finite sets has
exactly the native finite-count profiles and one additional saturated profile.
Indeed, if a coherent profile has $c_R<R$, put $n=c_R$. For $k\ge R$,
$\min(c_k,R)=n<R$ forces $c_k=n$; for $k\le R$, coherence gives
$c_k=\min(n,k)$. If no such $R$ exists, every $c_r=r$.

This extra point would allow every finite removal word. It expresses the
quantifier distinction

$$\forall r\ \exists n\ \forall |w|\le r:\ L_n(w)=1,
\qquad
\neg\exists n\ \forall w:\ L_n(w)=1.$$

The first statement is witnessed by $n=r$; the second by testing
$b^{n+1}$. Lean verifies these two statements and nonrepresentability of the
saturated profile. The full inverse-limit classification is a written proof.
No infinite native multiplicity is admitted by completing the shadow models.

## 5. The groupoid and positive-algebra premises remain visible

The successful graded transition graph has strictly decreasing depth along
every nonidentity edge. Its finite path category therefore has no reverse
path for such an edge. Replacing a native add/remove pair by formal inverses
would discard the consumed context resource: even when counts return, depth
does not. The native test validates a two-object, one-edge category and checks
that all 27 proposed inverse assignments on its three arrows are refused by
the existing groupoid owner.

There is also an algebraic obstruction. In the complex path algebra write
$e_x$ for the identity at object $x$. For a nonzero path $h:x\to y$,
$h=e_yhe_x$. Suppose a conjugate-linear involutive anti-automorphism fixes
all $e_x$. Then $h^*=e_xh^*e_y$, a linear combination of paths $y\to x$.
There are none in this depth grading, so $h^*=0$, contradicting involutivity.
Thus the path algebra itself has no such object-preserving star operation
when it contains a nonidentity path. This written result is not inferred
from the three-arrow example.

A larger matrix star algebra may contain a faithful representation, with
adjoints that have no native history counterpart. The
[finite groupoid theorem](qm_finite_history_groupoid.md) consequently
cannot simply be applied to this successful quotient: supplying inverses,
adjoining adjoints or choosing a different quotient requires its own reflection
contract. Finite depth alone does not supply those operations.

## 6. An exact observer still does not select a quantum state space

Let $X$ be the finite total observer carrier of §3 and $f_e:X\to X$ its
deterministic event maps. Two explicit mathematical representations preserve
all its guard answers:

1. Classical probability distributions on $X$, with the deterministic
   stochastic channels $f_e$ and the three output-indicator effects.
2. Complex density matrices on $\mathbb C^X$, pointer states
   $|x\rangle\langle x|$, the same diagonal effects and channels
   $\Phi_e(\rho)=\sum_x K_{e,x}\rho K_{e,x}^*$, where
   $K_{e,x}=|f_e(x)\rangle\langle x|$.

Here $\sum_xK_{e,x}^*K_{e,x}=I$, and
$\Phi_e(|x\rangle\langle x|)=|f_e(x)\rangle\langle f_e(x)|$.
Induction on words proves equality of every observer answer, including the
distinct terminal flags. The second construction uses measure-and-prepare
channels; the guard data alone do not require coherent transformations.
This proves sufficiency for this question family, not equivalence on every
native or physical observable. Ordinary finite classical probability and
finite complex quantum mechanics supply the respective ambient state and
transformation structures; scalar choice, mixing and tensor composition are
declared inputs to that comparison.

Now admit the uniform mixture of the $K=r+1$ initial-depth pointer states.
As a state of the classical algebra $\mathbb C^X$, it has $K$ central weights
$1/K$, so [PO-000 E.7](../../002_projection_obstruction/000_projection_obstruction/projection_obstruction.md#e7-a-sharp-quantitative-obstruction-from-central-weights)
bounds every extension's purity by $1/K$. This remains true even if a full
matrix ancilla is allowed. As a state in the single algebra $M_{|X|}(\mathbb C)$,
it has rank $K$ and an available $M_K$ ancilla can purify it, giving purity one.
The [capacity theorem](qm_ancilla_capacity.md) gives pure-marginal
distances $1-1/K$ and zero, respectively.

For $K\ge2$, any shared guard-only report predicting either of those extension
questions across these two supplied structures has worst-case absolute error
at least $(1-1/K)/2$. The midpoint attains this two-alternative bound. The
native test checks both event channels on every pointer projector for the
eight-state depth-two observer and uses the canonical capacity owner to
obtain purity $1/3$ versus $1$, and distance $2/3$ versus zero. These are finite
exact witnesses plus the written general construction, not dimension counts
offered as certification of an entire operational theory.

For WDP's greatest question-preserving contextual quotient, this supplies an
explicit instance: unrestricted legality has infinitely many classes, while
the bounded context contract has exactly $r+1$. For the
[S(n)/MSSN bridge](../../001_finite_obstruction_calculus/001_sn_mssn/README.md),
the report reflects this one native question family; the saturated profile,
adjoint completion and quantum enlargement have no authority to create a new
native stage. Other native moves can couple cells or change carriers and need
new reflection proofs.

An FSP sign/parity report can omit this distinction: counts one and three
have the same parity but disagree on two removals. A finite cyclic clock,
including a mod-six label, likewise need not preserve these native guards.
No FSP-to-Source-25 identification is assumed. The earlier MUB6 Weyl-family
results keep their restricted scope; neither this quotient nor its quantum
embedding rules out an arbitrary fourth mutually unbiased basis.

## 7. Verified scope and reproduction

[`NativeHistoryGuard.lean`](../../../../../lean4/NativeHistoryGuard.lean) imports
the existing one-cell transition definitions and proves NG1, separating words,
injection of the canonical $r+1$ representatives into any sufficient report,
unrestricted report injectivity, decreasing-depth transition laws, fixed-depth
failure, coherent truncation and the finite-versus-unrestricted quantifier
distinction. All **17** new reports use only `propext` and `Quot.sound` (some
use fewer). The finite cardinal consequences use the written pigeonhole
argument; there is no full Source-25 interpreter equivalence proof, formal
inverse-limit classification or formal category-algebra reconstruction here.

The [category tests](../../../../../omega_engine/crates_rs/tests/omega_category_theory/bounded_counter.rs)
check all words through depth eight, exact behavior partitions, the canonical
Moore quotient, composition, boundary distinctions and machine-integer limits.
The [native tests](../../../../../omega_engine/crates_rs/tests/omega_wdp/native_history_guard.rs)
check every cell of one-to-three-term marked states for both relations, counts
$0,1,3,2^{140}$ and all words through depth five. They compare complete raw
state updates along allowed prefixes and test the refusal, 100-attempt,
groupoid and declared quantum-channel controls above.

The [source driver](../tests/oracles/native_history_guard_replay.py) calls
the preserved Python `changes` and `perform` functions for eight inputs and
all 31 words through depth four. Its 248 first-refusal/final-count answers
reproduce byte for byte and are consumed by the native integration test.
The fixture hashes the imported source files. This is bounded reproduction,
not a universal source-language correctness claim.

```console
python omega_engine_projects/finite_qm/tests/oracles/native_history_guard_replay.py --check
cd lean4
lake build +NativeHistoryGuard
cd ../omega_engine/crates_rs
cargo test -j 1 --offline --locked -p omega_category_theory --test bounded_counter
cargo test -j 1 --offline --locked -p omega_wdp --test native_history_guard
```

Use the configured shared Cargo target in a worktree. The
[qualification receipt](https://github.com/dbccpage/the_symbol_game/blob/cd6205a801c4fa2e640e805ac556e704b6b51054/_intelligence/primitive_qm_eight_hour/native_history_guard_2026-10-11.json)
records exact commands, versions, exits, dependency warnings and source hashes.
No F004 release artifact or historical source archive is changed. The remaining
primitive-to-QM obligations include native admission, wider context reflection,
scalar choice, positive state/effect cones, tensor structure and operational
availability. GAP-FQM-021 remains open.
