# Reusing a rejection rule across finite representations

This example separates three questions: whether an emitted answer is correct,
whether every original solution remains obtainable, and whether a specified cost
bound is preserved. The first two concern actual emitted pairs, not a Boolean
report that some solution exists. The cost comparison uses the same task, initial
state, action menu and accounting boundary on both sides.

## 1. Exact carriers, inverses and task predicates

Let `D={-1,0,1}`, `X0=D²`, and `d∈{-1,0,1,2}`. A valid original answer
`(x,y)` satisfies `x+y=d`. Define

$$f_{01}(x,y)=(x+y,x-y),\quad
g_{10}(u,v)=((u+v)/2,(u-v)/2),$$
$$f_{12}(u,v)=(u,v+u),\quad g_{21}(r,t)=(r,t-r).$$

The other carriers are **exactly** `X1=f01(X0)` and `X2=f12(X1)`:

| `X0` | `X1` | `X2` |
|:---|:---|:---|
| (-1,-1) | (-2,0) | (-2,-2) |
| (-1,0) | (-1,-1) | (-1,-2) |
| (-1,1) | (0,-2) | (0,-2) |
| (0,-1) | (-1,1) | (-1,0) |
| (0,0) | (0,0) | (0,0) |
| (0,1) | (1,-1) | (1,0) |
| (1,-1) | (0,2) | (0,2) |
| (1,0) | (1,1) | (1,2) |
| (1,1) | (2,0) | (2,2) |

On these carriers, both pairs of maps are inverse bijections. For example,
`g10(f01(x,y))=(x,y)`, since the numerators are `2x,2y`; conversely
`f01(g10(u,v))=(u,v)` on `X1`. The second inverse pair follows by adding
and subtracting `u`. Hence

$$F=f_{12}\circ f_{01},\qquad H=g_{10}\circ g_{21},\qquad
H(r,t)=(t/2,r-t/2),\quad HF=1_{X_0},\quad FH=1_{X_2}.$$

Define `G0(d)={p∈X0:x+y=d}`, `G1(d)={q∈X1:u=d}` and
`G2(d)={z∈X2:r=d}`. Then `F(G0(d))=G2(d)` and `H(G2(d))=G0(d)`.
The solution counts for `d=-1,0,1,2` are respectively `2,3,2,1`.
For `d=1` the two complete paths are

$$ (0,1)\mapsto(1,-1)\mapsto(1,0)\mapsto(0,1),\qquad
(1,0)\mapsto(1,1)\mapsto(1,2)\mapsto(1,0).$$

The scalar report `u=1` does not distinguish these original pairs.
Also `(1,0)∉X1`, whose formal rational decoder is `(1/2,1/2)∉X0`,
although `(1,0)∈X2` and its level-2 decoder is the valid pair `(0,1)`.
Carrier admission and the representation level cannot be inferred from field names.

## 2. Necessary and sufficient soundness and coverage conditions

More generally let `f:X→Y` and `g:Y→X` be inverse bijections, and suppose
`y∈GY` iff `g(y)∈GX`. Let `E⊆Y` be the *actual set of emittable candidates*
under the installed menu and the declared fuel bound, if any. Then:

$$g(E)\subseteq G_X\quad\Longleftrightarrow\quad E\subseteq G_Y,
\qquad G_X\subseteq g(E)\quad\Longleftrightarrow\quad G_Y\subseteq E.$$

**Proof.** The first equivalence is the pointwise validity equivalence. For the
second, if `GX⊆g(E)` and `y∈GY`, there is `z∈E` with `g(z)=g(y)`; injectivity
of `g` gives `z=y`. Conversely, for `x∈GX`, validity transport puts `f(x)` in
`GY`, hence in `E`, and `g(f(x))=x`. This also shows why an accepted-answer
decoder alone cannot establish coverage: `E=∅` makes soundness vacuous.

These criteria apply to each actual image carrier in Section 1. They do not
identify `E` from a filter alone. Computing `E` must account for proposals,
full checks, emission gates, alternate routes and fuel. Under the particular
named-proposal menu below, each kept valid candidate is reachable at the same
price, so with sufficient fuel `E=Gℓ(d)\R`. In that menu, coverage is equivalent
to `R∩Gℓ(d)=∅`. An unavailable proposal or a removed emission action invalidates
that simplification even if the decoder remains correct.

For the parameterized source rule `R_d(u,v)≡u≠d`, the level-2 pullback is
`R_d∘g21`, namely `r≠d`. The level-0 pullback is `R_d∘f01`, namely `x+y≠d`.
Using `g10` for the latter has the wrong direction and domain. Each rule rejects
exactly the invalid elements on its own carrier. A concrete selection method is

$$M(-1)=(-1,-1),\ M(0)=(0,0),\ M(1)=(1,-1),\ M(2)=(2,0)\quad\text{in }X_1.$$

Each `M(d)` is valid; `f12(M(d))` is a level-2 witness. This method chooses one
answer, whereas full solution coverage additionally retains all valid proposals.
If `R,S` each avoid the full valid set, then `(R∪S)` avoids it: a valid element
in their union would lie in one of them. Auditing only the survivors of an
unverified earlier rejection does not establish that premise.

## 3. What the costs do, and do not, say

Prices are: proposal `1`, full check `2`, emission `1`, guard evaluation `1/2`
on every occurrence, adjacent transport `1`, and installation `3` in total
(`1` learning, `1` bundle check, `1` installation). The shared budget is `18`.
All execution actions have positive, outcome-independent prices. Carrier
admission, source hashing and checking the model tables are prerequisites to
this paid abstract arena, not additional free execution actions.

### Named proposals: the supplied profile

Retain every in-carrier named proposal, a full check, and valid-only emission.
Failed checks return to the root without an accepted answer. All tasks have a
valid candidate. A policy names one, checks it, and emits: cost `4`. Every
successful run includes these three operations, so its cost is at least `4`.
Thus the minimax value is exactly `4`; no adversary chooses a different named
candidate. These are finite public data, not a hidden-predicate search problem.

If a safe guard is made mandatory before every check, the same argument gives
operating value `9/2`; setup-inclusive value is `3+9/2=15/2`.
Every solution is still reachable individually at operating cost `9/2`.
This is a cost-only failure against a protected total bound of `4`.
Retaining an optional unguarded original route prevents a claim of global loss;
mandatory setup must still be charged. From level 2, an original fallback costs
two transports plus the original solution: `6`.

Consequently installation is not necessary to meet budget `18`, including at
`d=2`, where `(1,1)` is a direct original answer of cost `4`.
A guard-certified, carrier-admitted *check-free extension* would cost
`1+1/2+1=5/2`, not `2`. That extension is not the supplied check-retained menu
and is not used by the successful run or the optimality certificates here.

### A different problem: restricted blind scanning

For comparison, remove named selection, methods and alternate routes. The agent
must draw candidates without replacement, and an adversary chooses their order.
Stop at the first valid emission. There are `v` valid candidates among nine;
the guard soundly rejects `s` of the `9-v` invalid candidates. A draw costs `1`;
in a guarded scan the next action costs `1/2`, a nonrejected candidate is checked
for `2`, and a valid checked candidate is emitted for `1`.

An adversary places all invalid candidates first. The resulting exact values are

$$T_0(v)=3(9-v)+4=31-3v,$$
$$T_R(v,s)=\tfrac72(9-v-s)+\tfrac32s+\tfrac92
          =36-\tfrac72v-2s.$$

**Proof.** Every invalid candidate is visited at most once, and before the first
valid candidate there are at most all `9-v` invalid ones. Their charges are `3`
without a guard, `7/2` when guard-passed, and `3/2` when rejected. The final valid
candidate costs `4` or `9/2`. An order listing every invalid candidate first
attains the bounds. The finite arena records remaining counts of checked-invalid
and rejected-invalid candidates and exposes the draw's category. Merging the
identities of members of one category preserves these continuation costs and
success at the first valid emission; it is not an original-answer decoder.

Operating-cost nonincrease is equivalent to `4s≥10-v`; including installation
on the guarded side makes the criterion `4s≥16-v`. Maximal rejection has
`s=9-v` and operating value `18-3v/2`:

| Task `d` | Valid count `v` | Bare scan | Maximal-guard scan | Guard scan + setup |
|:---|---:|---:|---:|---:|
| -1 | 2 | 25 | 15 | 18 |
| 0 | 3 | 22 | 27/2 | 33/2 |
| 1 | 2 | 25 | 15 | 18 |
| 2 | 1 | 28 | 33/2 | 39/2 |

In particular `39/2>18` at `d=2`. These are exact values of the stated restricted
scan arenas, not optima of the supplied named-proposal profile. A safe do-nothing
guard (`s=0`) only adds cost; soundness by itself is not an efficiency theorem.

For any other finite installed arena, budget preservation against a reference
`b` means its actual minimax value is at most `b`, with the same setup boundary.
A rank-decreasing policy supplies an upper bound. Lower inequalities must cover
every admissible action, and omitted finite values require a checked loss trap.
The accompanying certificate checker checks these duties for the supplied finite
models; scanning arithmetic alone cannot replace them.

## 4. One compositional run on one ledger

The initial parent is at level 1. At `d=1` it names and checks `(1,-1)`, then
emits decoded original answer `(0,1)` for `4`. Learning, bundle
checking and installation cost `3`, bringing spent fuel to `7`. Transport
`X1→X2` costs `1`. The child proposes `(1,0)`, evaluates the guard, checks and
emits decoded `(0,1)` for `9/2`; then does the same with `(1,2)`, emitting
decoded `(1,0)` for another `9/2`. Thus

$$4+3+1+\tfrac92+\tfrac92=17\le18.$$

The child emits both original solutions and leaves fuel `1`. Before transport,
the child's incremental cost is `1+9=10`, not `9`. This is a constructed
successful paid run, not a globally optimal way to find the answers.
The Python replay retains all fifteen operation/charge/cumulative-spent rows,
with fixed parent identity and task. Repeated guard occurrences are each charged.

This is a multi-episode continuation, not one policy in the first-answer arenas
of Section 3: those arenas terminate at an emission. The separately declared
outer wrapper starts at level 1, receives the parent's completed answer, then
permits learning, bundle checking, installation and transport in that order.
At level 2 it permits proposal, guard, full check and decoded emission, returning
to the wrapper after each answer until both child solutions have been emitted.
It never resets the shared ledger. The
[trace checker](../../code/rejection_reuse/trace_checker.py) validates every
transition, carrier/decoder/check outcome, task/parent binding and exact charge.
It refuses skipped checks, installation or transport, changed binding, a reset,
an undercharged repeated guard and a wrong decoded emission. Repeating a child
episode costs another `9/2`: total `43/2`, refused at budget `18` but accepted
at an independently supplied budget `22`. No optimality claim is made for this
outer wrapper, and no recursive call can select a larger budget.

## 5. Changes and hostile controls

1. **Changed task.** At `d=2`, fixed `R1` rejects the unique valid level-1
   candidate `(2,0)` and level-2 candidate `(2,2)`. A check-retained menu remains
   sound but loses coverage. In the menu where that guard is mandatory and no
   fallback exists, every reachable nontarget state is a loss trap: rejected
   valid proposals and checked-invalid proposals return to the root. The
   certificate includes the initial state and a closed target-disjoint region.
   Restoring the two-transport original route gives exact value `6`, not loss.

2. **Stale parent.** The executable example hashes a canonical parent packet
   containing task, level, exact carrier, checker verdicts and prices, and binds
   the bundle to that digest. A different parent is refused even with unchanged
   acceptance semantics. This custody mismatch is not a mathematical
   counterexample. A task change separately supplies the counterexample above.

3. **Valid but blocked.** Removing all valid proposals or emissions can give
   `E=∅` while all accepted-witness decoder claims remain sound. Loss is established
   by the explicit trap above, not by soundness alone. A retained alternate route
   changes the arena and the conclusion.

4. **Fuel reset.** Two transports and installation spend `5`, leaving `13`.
   Resetting spent to zero and then using a fresh `18` exposes `23`, exceeding the
   original limit by `5`. Re-entry carries spent unchanged; a step with charge
   `c≥0` is admitted only if `spent+c≤18`. Neither a method nor a proof creates fuel.

5. **Cost only.** The safe mandatory guard keeps every original solution but
   raises the named-route setup-inclusive value from `4` to `15/2`.
   An efficiency claim needs a cost certificate, not just a sound filter.

6. **Checker change.** A refactoring with the same finite truth table preserves
   acceptance on these carriers. If prices, action menus, targets and reports
   also agree, the same mathematical bounds apply, although a byte-bound
   certificate must be rebound or regenerated. A checker accepting sums in
   `{d-1,d}` instead accepts invalid original `(0,0)` at `d=1` on an unguarded
   route. A correct maximal guard can mask this error on one guarded route;
   it does not validate the changed checker generally.

The smallest justified revalidation follows the dependencies of each claim:
soundness needs actual emitted sets, domains, decoder and acceptance; coverage
also needs forward maps and reachable proposals/emissions; budget bounds need
all admissible actions, successors, observations, targets, prices and setup.
Task and parent binding are additional custody conditions. If a changed
dependency has a checked equivalence certificate, its unchanged consequences can
be reused. An upper-bound policy need not be discarded because an unused action
was added; optimality still requires checking the new action's lower inequality.
The replay adds an unused cost-100 loop: the optimum stays `4` although the old
byte-bound certificate is refused. Dependency change therefore does **not** mean
semantic failure iff that dependency changed. Without justified equivalence, the
affected claim is unverified, not automatically false.

## 6. Mechanical scope and reproduction

From this paper's `code` directory:

```text
python -m rejection_reuse.replay --output <new-record.json>
lean rejection_reuse/rejection_reuse.lean
```

Python uses exact `Fraction` arithmetic, enumerates all nine elements at each
level, checks 6,144 emission subsets and 6,144 rejection subsets across the four
tasks, and submits 46 finite arena certificates to the existing search-free
`certified_progress.checker`. The producer is not imported by that checker.
Twenty-two controls include the six cases above, wrong map direction, off-image
inputs, a forged value, changed task/price bindings and the check-free price error.
The separate continuation checker accepts the fifteen-step trace and refuses
ten hostile traces, including an over-budget repeated episode; a budget-22 replay
of that same repeated episode confirms its full charge rather than treating it
as free. These trace checks do not extend the first-answer arena certificates.
Generated output records source hashes, all models/certificates and the ledger.
The canonical parent-packet digest is an example binding, not a signature or
authorization credential. Earlier source responses and development failures are
retained separately in the internal research record.

[Lean source](../../code/rejection_reuse/rejection_reuse.lean) formalizes the
integer image maps and inverse laws, validity transport, generic soundness and
coverage equivalences (instantiated at level 2), safe union, guard coverage,
pullback direction, scan cost algebra and both thresholds, the successful trace,
nonreset accounting and two finite counterexample witnesses. On image carriers
the integer divisions exactly represent the rational decoder; the off-image
rational control belongs to Python, not that integer decoder's formal scope.
Lean 4.34.1 compiles it without `sorry` or custom axioms. Printed dependencies
include the standard `propext`, `Quot.sound` and, for some arithmetic proofs,
`Classical.choice`; it is not advertised as axiom-free.

Lean does not certify the Python interpreter, the full general arena solver or
the complete software-to-engine correspondence. The Python results are finite
replays, not measured search performance. This completes the specified finite
reuse example; generic recursive re-entry and external authorization remain
separate questions.
