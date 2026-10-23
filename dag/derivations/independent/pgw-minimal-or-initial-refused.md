Status: AI-drafted, awaiting human review.

AuthorityEffect: None.

This declares comparison classes and proves their consequences. It does not
identify the sealed Alpha process with a newly chosen abstract category or
claim that repeated artifact agreement proves engine determinism.

A labelled process has a root, an action for each letter and a readout. A
morphism preserves the root, every action and the readout. Two processes meet
the same observed challenges here when every finite action word gives the same
rooted readout. These are explicit choices. The class permits additional
unobserved finite internal state, including a clock. It does not impose a
budget on declarations, program text or all hidden states through the readout.

For any process, form its product with a finite cyclic clock. Every action
advances the clock; the readout projects to the original process. Induction
proves equality of every finite-word readout, with no horizon cutoff. For a
finite carrier of size n, a root/action-preserving map into the product with
an (n+1)-clock would map the first n+1 iterates of any chosen action onto every
clock value. Its clock component would be a surjection from n states to n+1,
contradicting finite cardinality. Therefore no finite-state process is initial
in this clock-closed comparison class with a nonempty action alphabet.

A second obstruction does not require a finite state type. If any admitted
action is a self-loop at a state, a morphism into the invisible two-clock lift
would send that state to a fixed point of the clock toggle. There is no such
fixed point. This applies directly to the actual source interpreter: supply
is a self-loop. The Lean sourceModel is its optional regime state with an
absorbing failure state, source event alphabet and whole optional-regime
readout. A general replay theorem proves that its runs are exactly the actual
source replayE, including failure. Thus the actual regime-history interpreter
also has no morphism into its invisible two-clock lift, while all its observed
finite histories agree. This is a source-grounded obstruction under the stated
comparison rules, not a claim about an unspecified category of Alpha engines.

The clock argument concerns initiality. Minimum state count has a separate
criterion. Suppose a finite process p is reachable (every state is reached by
some finite word) and behaviorally reduced (agreement of all future-word
readouts implies equality of states). For any finite q with the same rooted
challenge answers, choose a reaching word for each p-state and run that word
in q. Equality of the resulting q-states would force all future observations
of the p-states to agree, hence the p-states are equal. This gives an injection
from p into q and therefore card(p) ≤ card(q). No corresponding reachability
or reduction premise is required for q.

Adequacy alone does not imply that criterion. A toggling two-state process
with constant readout and a one-state constant-readout process have the same
challenge answers. The former is reachable and is not reduced; it is larger.
A separate reduced example with an unreachable state shows why reachability
cannot simply be omitted. These are counterexamples to missing hypotheses,
not counterexamples to a specific sealed engine's minimum declaration cost.

The independent checker imports no repository code. It enumerates all 682
unary Boolean-readout processes with carrier sizes through three. Exact finite
pair-orbit closure decides all-time behavioral agreement for that declared
universe; it is not merely agreement through a chosen trace horizon. It checks
41,764 possible clock-component maps and all 98,346 behavior-equal pairs.
The 1,230 comparisons whose source is reachable and reduced satisfy the state
count bound. A supply-loop model checks all sixteen maps into its explicit
four-state invisible-clock target. SymPy verifies the process census and the
target's zero fixed-point trace. Three exact missing-premise/morphism controls
are checked. Normal/optimized output agrees and strict mypy passes. The general
Lean theorems allow arbitrary action alphabets and observation types; only the
independent census has these finite bounds.

What is proved

All-word clock readout agreement, no finite-state initial object in the stated
clock-closed class, the self-loop obstruction without a finiteness premise,
its exact actual-source replay instance, the reachable/reduced minimum-cardinality
criterion, and concrete controls showing the hypotheses cannot be dropped.

What is assumed

The explicit comparison class, observation interface and strict morphisms.
The source instance uses actual pinned Basic definitions and their supply rule.
All sixteen theorem audits use only the permitted kernel axioms. Independent batch review assesses the proof L4D, the bounded regression
checker L3D under the support exception, and Lake registration L1D. The three
fixed controls are not mutations. A separate actual root-only-equivalence
source mutant is rejected in both Python modes; broad mutation coverage is
not established. Human review is pending.

What is open

Membership and reduction/reachability obligations for the actual full Alpha
engine, a minimum program/declaration-cost theorem, and any initiality claim
under different morphisms or classes excluding hidden clocks. The source-regime
interpreter result is not an Alpha responder/runtime/license refinement. The
historical refusal record keeps its existing status. This is a provisional
narrowed comparison result, not an unconditional whole-engine minimum theorem.
