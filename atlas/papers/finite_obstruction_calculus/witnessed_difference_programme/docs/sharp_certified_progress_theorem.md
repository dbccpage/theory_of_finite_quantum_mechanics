# Sharp certified progress for a finite PFP/Woland execution model

Self-contained corrected theorem, 2026-10-05. AuthorityEffect: None.
This extends the finite game theorem already integrated in Appendix S.
It does not claim a native Woland binding where no artifact is supplied.

## 1. Explicit assumptions and information states

A declared model consists of a finite concrete state set X, a finite action
alphabet A, an initial nonempty B₀⊆X, enabled actions En(x), nonempty
transition sets T(x,a), and finite post-state reports o(a,y). Proposals are
adversarial choices among **all** declared successors, with no helpfulness,
probability, or fairness assumption. A terminating task-specific checker
Check(P,r) is supplied independently. Its soundness for the original task P
is an explicit assumption or a separately established theorem. Checker
termination alone does not imply soundness. Transitions outside the tables
invalidate the model's guarantee.

After observed history h the information state is the set B(h) of concrete
states consistent with that history. It is nonempty. From B, action a is safe
to attempt only if a∈⋂_(x∈B)En(x). Its possible next information states are

\[
 \operatorname{Post}(B,a)=
 \{\{y\in\bigcup_{x\in B}T(x,a):o(a,y)=z\}:z\text{ attainable}\}.
\]

Explore these states from B₀. This terminates after at most 2^|X|−1 distinct
nonempty beliefs. Costs c(B,a) are declared positive rational numbers and
observable to the controller. A hidden outcome-dependent charge must be
made an observed part of the state/report or replaced by an explicitly
declared conservative price; it cannot silently use the exact-cost theorem.

Terminal beliefs carry supplied resolution IDs and their actual task witnesses.
Each proposed terminal resolution must pass its checker for every world still
possible. A target predicate F(B) means the controller can supply a **common**
checked resolution of the declared goal. For a positive mathematical question,
that means a checked original-task solution. For a negative question, it means
the original task's checked exhaustive or other sound negative certificate.
Safe refusal and budget exhaustion are different dispositions. Neither is
silently an existential solution or an impossibility proof. A policy objective
whose explicit goal is safe refusal may designate that disposition as its own
target, but this does not change the mathematical claim's status.

Authorization is an independently supplied predicate/binding on the permitted
operations and final use. A game certificate records it; it does not grant it.

## 2. Exact winning characterization and finite obstruction

On the finite reachable belief arena S define

\[
 W_0=F,\qquad
 W_{n+1}=W_n\cup\{B:\exists a\in En(B),\ \operatorname{Post}(B,a)\subseteq W_n\}.
\]

**Theorem P1.** W=⋃W_n is exactly the set of beliefs admitting safe,
finite, guaranteed resolution against every declared outcome.

**Proof.** For B entering at stage n+1 choose an action whose successors
entered earlier. The least entrance stage decreases strictly, so every
execution reaches a target in finitely many operations. Conversely consider
any strategy that resolves on every adversarial path. Its execution tree is
finitely branching. If it had no common finite depth bound, choosing an
unbounded-depth child at every node would construct an infinite path.
Thus the tree has finite height. Induction on its height places its root in
some W_n. The union is the least target-containing set closed under the
controllable predecessor rule. It stabilizes after at most |S| strict additions. ∎

Equal final endpoints do not replace this argument. An outcome branch may
stall forever, and an action available in only one possible world is unsafe.
The theorem also proves that a memoryless belief policy suffices; a history
dependent strategy cannot win from a belief outside W.
Every finite belief path has a compatible concrete path by the update rule.
An infinite belief path also has a compatible infinite concrete path by the
same finite-branching argument, so losing closure does not rely on switching
to an inconsistent hidden world at successive rounds.

**Theorem P2 (sharp finite certificates).** A winner certificate is a policy
π on W\F with a natural rank r, zero on F, such that every chosen action is
enabled and every successor is in W with smaller rank. A loser certificate
is a target-disjoint L containing the initial belief, plus, for **every**
available action at every B∈L, a listed successor in L. Dead ends have no
action rows and are explicitly retained as stalled, nonterminal states.

**Proof.** A rank proves termination by descent. For L, the adversary follows
the supplied closure successor forever or reaches a nonterminal dead end.
The complement of the least attractor supplies such witnesses because no
action there has all successors inside W. Thus both certificates exist
exactly at the corresponding beliefs. ∎

A complete W/L partition with winner ranks and all-action loser witnesses
lets a checker validate the classification without running attractor search.
A losing game certificate says “no guaranteed strategy in this declared
operation menu.” It is not an unsatisfiability certificate for P. Turning it
into that claim requires faithful source coverage and an independently sound
original-task negative checker.

## 3. Exact operation-preserving observation quotient

Let p:S→C be the surjection determined by a supplied presentation partition.
An **exact operation quotient** means a quotient with the same action names,
preserved and reflected enablement, identical prices on enabled actions,
preserved terminal truth and declared report labels, and exact equality of
successor class sets. No probabilities or outcome multiplicities are used.
Report labels include the resolution-ID sets, claim/disposition type, and any
state-dependent authorization information the presentation purports to retain.

**Theorem P3 (necessary and sufficient structural criterion).** Such a
quotient exists if and only if whenever p(B)=p(C):

1. F(B)=F(C) and the declared report labels agree.
2. En(B)=En(C).
3. c(B,a)=c(C,a) for every enabled a.
4. {p(D):D∈Post(B,a)}={p(D):D∈Post(C,a)} for every enabled a.

**Proof.** Necessity follows by comparing the two states to their common
quotient image. For sufficiency choose any representative of each nonempty
class. Define terminal truth, reports, enabled actions, prices and successor
class sets using that representative. The four laws make every definition
independent of the choice. They give forward and backward successor matching,
not merely a forward simulation. This constructs the quotient. ∎

Winning and each finite-horizon achievable budget are preserved and reflected:
induct on the horizon, using forward matching in one direction and backward
matching in the other. Hence exact optimal cost is preserved. A quotient
policy lifts. A particular fine policy descends literally only if its choices
are constant on presentation fibers. Common checked terminal payloads still
need their actual checker binding; a table of equal booleans cannot create one.

The criterion is necessary for **this structural definition**, not for a
particular task accidentally having the same value. For example two pending
states may both have a direct route of cost 2, while only one also enables
an action of cost 7. Their optimal values agree; their operation sets do not.
Likewise a presentation can preserve today's output “pending” while forgetting
that one state's only completion costs 2 and another's costs 9.

**Theorem P4 (coarsest stable refinement).** Starting from a supplied seed
partition, split each block by the signature
(terminal truth, report label, enabled actions, their prices and successor
block sets). Repeat until unchanged. The result is the coarsest exact
operation partition refining the seed.

**Proof.** Each strict step increases the number of blocks, so there are at
most |S|−|seed| strict steps. The fixed point satisfies P3. Suppose another
exact partition refines the seed. Inductively it refines every intermediate
partition: equivalent states agree in terminal/report/action/cost data, and
successor matching in its own blocks implies agreement in every coarser
intermediate block. Such states are therefore never split by an intermediate
signature. This proves maximal coarseness at stabilization. ∎

`ExactProgressQuotient.lean` proves the iff construction with an explicit
section of p and arbitrary report labels. The existing `BeliefGameQuotient`
proves achievable-budget equivalence and the constructive finite relation
refinement. The Python refinement receipt lists every exact split plus the
final unchanged step; a separate table checker validates that receipt.

## 4. Exact minimum worst-case price, including cycles

For B∈W, let V(B) be the minimum worst-case sum of operation prices among
guaranteed resolving strategies; V=∞ off W and V=0 on F.

**Theorem P5.** The minimum exists, is rational on W, equals zero on F,
and for each B∈W∖F satisfies

\[
 V(B)=\min_{a\in En(B)}\bigl(c(B,a)+\max_{D\in Post(B,a)}V(D)\bigr).
\]

An action with a losing successor has value ∞. This is the terminating-game
solution of the equation; an unsupported fixed-point guess is not a proof.

**Proof and terminating producer.** If W∖F is empty, every winning state is
already terminal, so the zero values and empty policy give the result.
Otherwise at least one operation is enabled. Let ε be the smallest cost among
enabled operations, c_max the largest, and R the greatest attractor rank. The attractor policy
costs at most U=Rc_max from every winner. Every path costing at most U has
at most H=floor(U/ε) operations. There are finitely many bounded strategy
trees, so their exact rational costs have a minimum. Synchronous dynamic
programming initialized at 0 on F and ∞ elsewhere computes these costs up
to horizon H. It therefore attains the global optimum at every winner.
The optimal next-action principle gives the displayed Bellman identity.
For an optimal action chosen at B∈W∖F, positivity gives V(D)<V(B) at every successor.
Order states by increasing finite V and assign a natural rank to obtain a
memoryless terminating optimal policy. ∎

Cycles remain in the source arena. A successful strategy cannot rely on an
adversary-controlled self-loop; such a loop provides a losing closure unless
another controller action avoids it. A loop in a finite-cost optimal policy
would force strictly decreasing values around a cycle, which is impossible.
Positive prices are essential to the finite cost/horizon argument.

**Independent upper/lower certificate.** Supply the complete W/L partition,
terminal value zero, a rational v on W, policy and decreasing ranks.
At each B∈W∖F, for the selected action require all successors in W and
c(B,π(B))+v(D)≤v(B) for every successor D. This is an upper bound by
telescoping. At each B∈W∖F, for **every** enabled action either exhibit a successor in L,
or require v(B)≤c(B,a)+max_D v(D). The complete finite successor/value table
lets the checker identify a maximizing successor without strategy search.
The adversary then enforces the lower bound along any guaranteed strategy;
at termination its remaining value is zero. The matching bounds prove
v=V. All comparisons are exact rational arithmetic. The checker never
silently swaps in a separately found strategy when the submitted one fails.

Model resource limits may stop this computation before H. The producer then
returns `Undetermined` with the missing horizon. A previously checked feasible
strategy supplies an upper cost only. Budget b<V is a budget obstruction,
distinct from V=∞ and from original-task impossibility.

## 5. Optional certified shortcuts and transfer

**Theorem P6.** If new operations are optional, old operations and costs
are retained, and a shortcut's emitted resolution passes the original task
checker, then V_new≤V_old. The old strategy is still available.
This comparison concerns operating cost only.

Let setup C=C_learning+C_checking+C_installation be separately accounted.
For repeated episodes with saving Δ>0, payback requires nΔ≥C; strict savings
require nΔ>C. Nothing in P6 implies one-use payback. For V_old=3,
V_new=1/2,C=8, one use costs 17/2>3, while four uses cost 10<12.

A source-sound antibody can fail after transfer. For the source task
f(x)=x, the candidate F(x)=5x has the correct endpoint difference 50 but
fails the derivative check. Rejecting it is sound there. For the target task
f(x)=5 on the same interval, that same primitive is valid. An antibody that
rejects the formula regardless of task identity destroys target validity.
Scope it to the original input/assumptions, or supply a checked preservation
map proving its predicate remains sound. A restrictive guard is not an
optional shortcut: removing old actions can raise cost or destroy winning.

## 6. Actual bounded calculus/PFP reconstruction

The supplied archived task is “Integrate f(x)=x from 0 to 10; give one exact
numerical result,” with declared real interval, Riemann measure and rational
polynomial witness profile. The retained proposal is F(x)=x²/2, answer 50.
The unchanged supplied `pfp_calculus/source/calculus_reference_check.py`
checks its input hash, coefficient profile, exact polynomial derivative and
endpoint evaluation. The result is independently replayed, not assumed from
the answer 50. The malformed alternative F=5x, also claiming 50, is refused.

The bounded operation table is:

| state | controller action | all declared successors | cost |
|---|---|---|---|
| ready | propose | ready, good, bad | 1 |
| ready | retrieve_archived | good | 1 |
| good | check | verified | 1 |
| bad | check | refused | 1 |
| refused | retrieve_archived | good | 1 |
| verified | record_resolution | resolved | 1 |

Reports identify the listed next states. `resolved` is terminal only with
the bound checked answer-50 payload. The supplied-checker hash, original
task hash, actual retained proposal hash and replayed receipt are retained.
The actual local episode executes retrieve → check → local record, cost 3.
The adversarial `propose` row is a declared possible behavior; it is not a
native provider binding or evidence of a new model call. Its forever-ready
outcome cannot defeat the guaranteed archive route. Removing the archive
route gives a genuine losing trap {ready,bad,refused}, despite the existence
of a valid mathematical answer. That is game loss, not impossibility.

At ready the exact minimum is 3: retrieve costs 1, checking 1 and recording 1;
proposal can remain ready forever. A certified optional direct resolution
at declared cost 1/2 reduces the operating optimum to 1/2, after its separately
declared setup/checking cost. These prices are abstract operation units,
not model billing or measured runtime.

Only the supplied retrieval/check/local-record operations are reconstructed.
Missing host stages, full campaigns and Woland runtime integration are not
invented. The actual checker demonstrates the polynomial claim, not source
quote truth or every surrounding audit statement. Those need separate checks.

## 7. Formats, rejection tests and provenance

The arena schema `wdp-finite-belief-model-v1` lists concrete states, action
enablement, transitions, reports, initial belief, terminal beliefs, resolution
IDs, validity tables, emissions, positive rational prices, assumptions and
authorization. Resolution tables alone are declared assumptions until the
task adapter replays the corresponding actual checker.

The progress schema `wdp-progress-certificate-v1` binds the model digest and
task ID; it supplies W,L, stalls, all-action closure rows, strategy, natural
ranks, exact values, resolution IDs and the precise optimality flag.
The separate quotient table lists terminal truth, resolution IDs, enabled
action names, prices and successor class sets for every class. Its refinement
receipt binds the original model digest and all successive split partitions.
The calculus episode adds original checker/proposal hashes and the submitted
payload and actual mathematical receipt. Wrong witnesses, task changes,
stale source hashes and authorization changes must be refused.

Retained rejection tests cover indistinguishable states requiring left/right
actions; a forever-unhelpful proposer; the cost-2 two-step route versus the
cost-5 direct route; equal current reports with unequal actions/costs; the
F=5x antibody transplant; and resource cutoff presented as `Undetermined`.
Existing Appendix S tests additionally cover invented terminal truth,
omitted cheaper actions, fake infinity, missing closure rows and malformed
JSON. Replay requires zero provider calls.

The attractor, memoryless reachability, adversarial shortest-path reasoning,
bisimulation and partition refinement are imported standard game-theoretic
constructions, reproved here for the precise finite semantics. The WDP
contribution is their binding to original-task evidence, observer adequacy,
explicit information loss, typed refusal, repair/transfer scope, source custody
and independent authorization. This is an application and synthesis, not a
claim to have invented controllable predecessors or minimax search.
For the standard refinement background see
[Paige–Tarjan, Three Partition Refinement Algorithms](https://epubs.siam.org/doi/10.1137/0216062).
This theorem uses sure resolution against every path. Almost-sure stochastic
winning has different memory requirements; no such conclusion is imported
from the belief construction (compare the distinct setting in
[Chatterjee–Doyen](https://arxiv.org/abs/1107.2141)).
