# Minimum-cost observation that preserves future operations

This completes a declared finite instance of target 3 in the WDP derivation
plan. It also gives a full written reduction for the finite model below.
“Instrument” means a specified measurement action with a transition, report,
admissibility condition and cost; physical realization is a separate question.
No new standard, protocol or terminology is needed.

## 1. Inputs and the exact preservation question

Let X be a finite information-state carrier, such as the reachable beliefs
of Appendix S. Fix a partition map k:X→K. States in one block must have the
same protected current answers, target truth, enabled future-action labels,
prices, and sets of successor blocks for each such action. These are the
future-operation congruence conditions of S.5. They preserve and reflect
declared future paths and their prices by induction on path length. They do
not preserve an unlisted outcome label or probability distribution.

Supply a finite measurement family I. Action i has domain D_i⊆X, a nonempty
successor set T_i(y) for y∈D_i, and a post-state report λ_i(y'). Prices are
positive rational numbers c(z,i), known from the observer's information z.
For state-priced tables this requires equal prices on all possible current
states. Every listed outcome is adversarially realizable. Infinite
nonterminating execution is unsuccessful. There is no implicit permission,
hidden free measurement, or physical apparatus assumption.

The original state x is fixed while the current state y changes. A policy
must, on every observation branch, terminate with a decoded **original**
class k(x) and a current state with that same future class. A more detailed
report may refine this class: the minimum concerns cost of a sufficient
report, not an exact prescribed encoding or minimum number of bits.

The default preservation boundary is the **handoff after measurement**:
temporary disturbance may be repaired before the future procedure resumes.
If future operations must remain available throughout measurement, impose
the stronger prefix condition k(x)=k(y) after every step. Section 7 gives
that variant. Neither convention should be substituted for the other.

The free initial report p gives one initial relation
z_o={(x,x):p(x)=o} for each realized o. Empty fibers are ignored.

## 2. The required information is a relation, not a current-state set

At an observation history retain the nonempty relation z⊆X×X of possible
(original,current) pairs. Action i is admissible exactly when every second
coordinate lies in D_i. Its observed successor is

\[
 z_{i,o}=\{(x,y'):\exists y\ ((x,y)\in z,\ y'\in T_i(y),
                    \lambda_i(y')=o)\}.
\]

Retain only nonempty successors. This relation is finite, publicly
computable from the known history and model, and never drops the first
coordinate. It can grow after a nondeterministic action. A non-splitting
action can be useful because it changes the current state.

**Lemma (exact history correspondence).** The displayed relation contains
exactly the possible original/current pairs after that history.

*Proof.* At the empty history the original and current states coincide
and the initial report restricts exactly the diagonal pairs. If the
statement holds at a prefix, executing i gives exactly the supplied
T_i-successors of its current states. Selecting report o then retains
exactly the successors satisfying λ_i(y')=o. The displayed existential
keeps their original coordinates. This establishes the next prefix in both
directions. Induction covers every finite history. ∎

Discarding the original coordinate is unsound. Relations
{(a,a)} and {(a,a),(b,a)} have the same current-state set {a}. If k(a)≠k(b),
only the former supplies a decoder for the original class. This is a
direct collision, not a failure of the ordinary Appendix-S posterior for
its different current-state question.

## 3. Necessary and sufficient stopping condition

A relation z admits a successful handoff exactly when

\[
 \exists C\in K\quad \forall(x,y)\in z:
              k(x)=C=k(y).                                      \tag{1}
\]

**Proposition.** Condition (1) is equivalent to a unique class decoder on
that realized observation history together with preservation of the
declared future contract for every possible actual execution.

*Proof.* If (1) holds, output C. Nonemptiness makes C unique. Every possible
original pair has the reported class, and its current state has that
class. The congruence assumptions make the quotient future steps
well-defined. Each current step maps to a quotient step; every quotient
successor block has an actual current successor. Induction lifts any
finite quotient path from the current state with the same labels and
prices, and compares it to a path from the original state. Thus the
preservation and reflection assertions concern the supplied block-level
future semantics, not identity of raw histories.

Conversely a decoder for the original class must give the same C on every
pair compatible with the history. The required handoff preservation
forces k(y)=k(x) for each such pair. These are precisely (1). ∎

Knowing a current answer, knowing the original class, and preserving the
original class are three different tests. The instance below separates them.

## 4. Sharp finite policy and cost theorem

Explore the relations reachable by the update in §2, stopping at (1).
There are at most 2^(|X|²)−1 nonempty relations. This is a finite
reachability arena whose actions, adversarial outcomes and positive prices
are derived from the measurement tables; they are not arbitrary linear rows.

**Theorem.** A future-preserving observation policy exists if and only if
every realized initial relation belongs to the reachability attractor of
the relations satisfying (1). Its least worst-case cost is the exact
finite minimax value in that arena, maximized over the free-report fibers.
It is attained by a policy depending only on the current relation. An
initial-containing target-disjoint trap certifies nonrealizability. A
rank-decreasing policy with all-action lower inequalities certifies an
attained minimum independently of the search that produced it.

*Proof.* By the history lemma, an action is executable on every possible
current state precisely when it is admissible at its relation; the update
lists all and only its possible observed successors. Policy choices based
on the observation history therefore correspond to contingent plans in
this relation arena. The stopping proposition identifies their successful
leaves exactly, and every charged edge retains its original price.

Apply the elementary finite attractor argument of S.3: targets have rank
zero; add a relation when one action has all successors at earlier ranks.
The process stabilizes after at most the number of reachable relations.
A witnessing action strictly decreases rank, hence realizes a finite
successful policy. Outside the attractor every admissible action has a
successor outside it, so an adversary can stay in the target-disjoint
complement or terminate at a non-target dead end. This covers
history-dependent policies as well as relation-dependent ones.

For the cost assertion let ε>0 be the minimum reachable price, c_max
the maximum, and R the maximum attractor rank. An attractor policy costs
at most M=c_max R from every winner. A policy with worst-case cost at
most M takes at most H=⌊M/ε⌋ actions on every branch. There are finitely
many contingent plans of that depth. Backward minimax recursion with
terminal zero therefore attains an optimum; any cheaper policy would
also lie in that finite family. A minimizing action decreases value by
at least ε at every successor and consequently has a terminating rank.

To check a submitted optimum v, replay the target/trap partition and the
selected ranks. On winners require terminal zero, selected-action
equality, and for **every** admissible action

\[
 v(z)\le c(z,i)+\max_{z'\in\operatorname{Succ}(z,i)}v(z').
\]

A losing successor makes that alternative infinite only after its trap
has been checked. Rank induction gives a selected-policy upper bound.
Induction on a successful contingent plan gives the lower bound by taking
a maximizing child. Every finitely branching policy all of whose maximal
plays terminate has bounded depth, since otherwise its tree has an infinite
branch. Thus the lower argument covers every successful policy. These
are the S.6 certificate laws on the newly constructed relation arena. ∎

The procedure is exponential in the supplied finite carrier. A cost above
the available budget is a budget obstruction, not nonrealizability.

## 5. A complete instance, with restoration charged

The source model is an actual Appendix-S table, constructed by
`future_model()` in [core.py](../../code/realizable_observation/core.py).
A preparation state has an action leading to any of the eight states
(b,v,m), where b∈{A,B}, v∈{0,1}, m∈{0,1}, observed by its full name.
The successful state is t. At (b,v,m), the future action `resolve_b`
costs 1+v and leads to t; `wait` costs 1 and returns to the same state.
All other resolution labels are disabled. Future reports depend on b,v,
not m. Accordingly the congruence class of a singleton information state
is (b,v), independent of m. The initial measurement possibilities are the
four singleton information states with m=0, with constant free report.

All of them have the same current nonterminal status. Branch enablement
and resolution price nevertheless force four distinct future classes.

| Measurement action | Admissibility and actual post-state | Report | Cost |
|---|---|---|---|
| `read_branch` | All eight states; unchanged | b | 1 |
| `read_A` | All states; unchanged | v if b=A, otherwise 0 | 3 |
| `read_B` | All states; unchanged | v if b=B, otherwise 0 | 3 |
| `read_all` | All states; unchanged | (b,v) | 6 |
| `flip_read` | m=0 only; (b,v,0)→(opposite b,v,1) | Post-state branch | 1/2 |
| `restore` | m=1 only; (b,v,1)→(opposite b,v,0) | Constant | 1/4 |

The optimum is **15/4**. Ask `flip_read`, ask `read_A` or `read_B`
according to the observed current branch, and restore. The decoder uses
the recorded original branch and measured v. Every actual endpoint is
the exact starting state. Restoration makes no new distinction but is
required for the declared future handoff.

For a direct lower bound follow the execution starting at (A,0,0).
To distinguish it from (B,0,0), the policy must use `read_branch`,
`read_all`, or `flip_read`: both conditional measurements report 0 at
both states. To distinguish it from (A,1,0), it must use a conditional
value measurement or `read_all`; branch-changing actions do not depend
on v. If `read_all` occurs, its cost is already 6. Otherwise a path
using `read_branch` but no flip costs at least 1+3=4. A path using
`flip_read` costs at least 1/2+3 and must restore, adding at least 1/4:
`flip_read` is disabled in mode 1 and no other action returns to mode 0.
Additional operations have positive cost. Hence every successful policy
has a path costing at least 15/4. The displayed policy attains it.

If only original-class information is required, the optimum is 7/2;
the cheaper stopping point leaves the wrong resolution label enabled.
If restoration costs 4, the optimum becomes 4 via non-disturbing adaptive
measurement. If the non-disturbing branch/all measurements and restoration
are removed, no sufficient future-preserving policy exists: the two
zero-valued branches cannot be distinguished before the flip, and every
flipped execution is permanently in the wrong future class. The replay
contains an initial-containing trap, not just an information collision.

## 6. Exactly when static sufficient measurement is enough

With only nondisturbing, total, history-independent measurements and fixed
positive prices, the relation remains diagonal. Condition (1) reduces
to constancy of k on the posterior. The construction is then exactly the
adaptive recursion of §14.6; a sufficient fixed measurement family is
a feasible policy, so dynamic cost is at most its cost.

For any such instance with a finite static optimum C, equality is
equivalent to a matching dynamic lower certificate of value C at an
initial worst-case fiber. Sufficiency follows from that lower bound and
the static upper policy; necessity follows from the complete finite
certificate theorem in §4. This is an exact checkable characterization,
not a claim that static coverage itself supplies a dynamic lower bound.

A useful structural sufficient condition is a full Cartesian product of
independent finite coordinate sets, each with at least two values; the
protected class is the complete coordinate tuple; the free report is
constant; and every permitted action returns a fixed subset of coordinates
without changing state. A successful branch must have observed every
coordinate: otherwise changing one unobserved coordinate yields another
compatible original class. Thus the set of actions on every successful
branch covers all coordinates, and its path cost is at least the minimum
weighted set-cover cost. An attaining static cover gives the matching
upper policy. Static and adaptive minima therefore agree. The two-bit
coordinate fixture has price 1+2=3 in both calculations.

The main instance violates this coordinate condition: the conditional
measurements reveal a value only on one branch. Its cheapest fixed
nondisturbing family is `read_all` at cost 6; its adaptive nondisturbing
optimum is 4; and the disturbance/repair family attains 15/4. Thus static
sufficiency, adaptive sufficiency and realizable cost need separate checks.

## 7. Preservation throughout measurement

If the contract protects future availability at every prefix, admit an
action at z only when every pair in every observed successor satisfies
k(x)=k(y'). Apply the same finite theorem to this restricted arena.
The exact update, decoder and cost arguments are unchanged; the action
filter encodes the stronger requirement. In this instance `flip_read`
is excluded initially, and the remaining optimum is 4. A terminal-only
certificate of 15/4 must not be used for that stronger contract.

## 8. Evidence and remaining scope

[replay.py](../../code/realizable_observation/replay.py) retains original
inputs and search certificates; the separate
[construction checker](../../code/realizable_observation/checker.py)
recomputes all pair updates, domains, terminal decoders and prices without
importing the construction/search implementation. The established
`certified_progress.checker` replays submitted policies, lower bounds and
loss traps without strategy search. These checkers share the original
future model and partition-refinement dependency, which is explicit.

[finite_replay_v3.json](../../code/realizable_observation/finite_replay_v3.json)
records five independently replayed instances and twelve hostile controls:
changed prices/reports/guards, fabricated future classes, forged lower
bounds, shifted terminal cost, omitted original state, loss of the original
anchor, original information without future preservation, the useful
non-splitting restoration, static/adaptive separation, and coordinate equality.
The first draft accidentally reported a special symbol on the inactive
branch of a conditional measurement, making that action disclose the branch.
The failed nonrealizability test exposed this; the corrected inactive
report is 0, and that failed result is retained in the research audit.

[RelationLaws.lean](../../code/realizable_observation/RelationLaws.lean)
also checks five selected relation laws with Lean 4.34.1 and no axioms:
retention of the original coordinate, two-step update, decoded original
and current classes, decoder uniqueness on a nonempty relation, and the
current-set collision. [The compiler record](../../code/realizable_observation/lean_check.txt)
states the exact command and scope; these laws do not formalize the minimax theorem.

The general result above is a complete written argument. Finite execution
checks the stated tables and certificates, not every possible finite model.
No whole-theorem Lean proof, actual hardware sensor, engine deployment,
unbounded world reconstruction, or new publication is claimed. This closes
the selected finite observation-model question and advances the observer
realization obligation of S.5; the broader source/world correspondence
and physical realization obligations remain open.
