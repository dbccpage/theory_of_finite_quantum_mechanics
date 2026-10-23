# WDP-CHS-O01

Goal id: WDP-CHS-O01

Selected scope for WDP-CHS-O01 is recorded in this note.

## Selected scope

Five-belief alternating parity carrier `parity_alt_osc` only.

Beliefs and priorities: hi maps to 2, lo maps to 1, fork maps to 1, sink maps to 1, and bait maps to 2.

Actions and successor lists:

- hi/down goes to {lo}.
- lo/up goes to {hi}.
- lo/fall goes to {sink}.
- fork/risky goes to {hi, sink}.
- sink/stay goes to {sink}.
- bait/drop goes to {sink}.

No belief is a stopping target. The controller picks an admissible action. If the successor list has more than one belief, the adversary picks which one occurs. Plays are infinite. A play is a controller win exactly when the highest priority occurring infinitely often is even. Strategies may depend on history.

On this carrier only, the winning set is {hi, lo} and its cardinality is 2.

This carrier is not named by Appendix S, by `docs/five_outstanding_derivations.md`, or by the goal row. Those sources leave full parity objectives open and fence the reachability argument with WDP-CHS-N04. The calculation below is an inspection of this declared table. It does not discharge that open obligation.

## Hypotheses

H1. The carrier is exactly the five beliefs, priorities, and successor lists above. No successor is omitted, and no further action is enabled.

H2. Plays are infinite. There is no stopping target. A dead-end reading is not used, because every action in the table has a nonempty successor list. The positive-cost rank bounds of WDP-CHS-P15 are not part of this objective.

H3. The controller chooses the action. The adversary chooses the successor only when the list has more than one belief. A win is the existence of a controller strategy, which may depend on history, that forces an even highest infinitely often priority against every adversary reply. A loss means that some adversary reply forces an odd highest infinitely often priority against every controller strategy.

H4. WDP-CHS-N04 is in force. P01, P04, P07, P15, P16, the rational value V, the natural attractor rank, assumption A5, and the CertifiedProgress reachability certificate are not used as the parity proof.

H5. The goal row WDP-CHS-O01 has empty `depends_on` and fence WDP-CHS-N04. The fence does not cancel the open sentence in Appendix S. It forbids treating the reachability argument as the missing proof.

## Derivation

### Winning certificate

Submit W = {hi, lo}, σ(hi) = down, and σ(lo) = up. Both chosen successor lists are singletons and stay in W.

From hi the only play under σ is hi, lo, hi, lo, and so on. From lo it is lo, hi, lo, hi, and so on. In both plays the priorities occurring infinitely often are {1, 2}, so the maximum is 2, which is even. Thus the controller wins from hi and from lo. The adversary has no choice on these actions. The odd priority 1 occurs on every period, so the win is not absorption in an even terminal and not arrival at a target.

The action lo/fall is enabled and leads to sink. It is not the submitted strategy. Existence of a losing action at lo does not remove lo from the winning set.

### Losing certificate

Submit L = {fork, sink, bait} and the adversary reply τ(risky) = sink.

The sink action is unique and leads to sink. The only play from sink is sink, sink, and so on. The only priority occurring infinitely often is 1, which is odd.

The bait action is unique and leads to sink. The play is bait followed by that tail. The only priority occurring infinitely often is again 1.

From fork the only action is risky, and τ answers sink on the first step. The tail is the sink play. History cannot avoid τ, because fork has no other action.

The cooperative path fork, hi, lo, hi, and so on does win, because its priorities occurring infinitely often are {1, 2}. The adversary is not obliged to offer hi. Therefore fork, sink, and bait are losses against the submitted reply, for every controller strategy.

### Exact integer

The winning set has cardinality 2. That integer is the size of {hi, lo}. It is not the sum of the five priorities 2 + 1 + 1 + 1 + 2, and it is not a sum of progress-measure coordinates. No rational price is computed.

### Obstruction to the fenced reachability argument

WDP-CHS-N04, placed immediately after P01–P07, states that this reachability argument does not prove parity objectives. Appendix S.0 says that no parity-game theorem and no general Tarski theorem is used for the elementary finite proofs. Assumption A5 says that an infinite nonterminal play is losing for the reachability objective. The acceptance table's cost-two witness is a reachability optimum, not a parity quantity. The proof supplement says the review repairs leave parity objectives open. `docs/five_outstanding_derivations.md` lists full parity objectives together with source/world adequacy, physical scalar/readout choices, and the Q-continuum as separate open extensions, outside targets 1–5.

With the target set empty, P01 starts from W₀ = T ∩ B = ∅. No successor list in this table is contained in the empty set, so the attractor never adds a belief and reports 0 wins.

P04 applies to the set of all five beliefs: every successor remains inside that set, and the set contains no target, so it certifies hi as a reachability loss. The same hi is a parity win under σ. The two objectives disagree. P01 and P04 are not the certificate above.

If the even-priority set {hi, bait} is treated as a stopping target, the P01 attractor starts with those two beliefs, then adds lo because up lands in {hi}, and adds neither fork nor sink. Its size is 3, not 2. Bait has even priority, but its only continuation is the odd sink, so stopping on an even belief is a different objective. That attractor is not the winning set of this note.

P15's positive-price horizon and P16's rational Bellman certificate are one-dimensional reachability quantities. They are not evaluated here and are not reused as the parity answer.

### Boundary

Both directions were checked by inspecting every action on this five-belief carrier. No Python, Rust, or Lean checker was executed for this note. The argument does not prove memoryless determinacy, a general progress-measure theorem, or certificate completeness for an arbitrary finite parity game. The unbounded reading of WDP-CHS-O01 is not claimed. Appendix S still states that full parity and alternating objectives need their own certificate laws and proofs. A finite model does not establish a continuum limit, a physical law, or a closed theorem outside the selected scope.

## Claims this note does not make

- It does not claim that P01, P04, P07, P15, P16, A5, a natural attractor rank, a positive-price horizon, or the cost-two reachability witness proves a parity objective. WDP-CHS-N04 forbids that step, and that step was not used.
- It does not claim that the empty-target attractor, the five-belief trap, or the even-priority attractor of size 3 is the winning set. The winning set on this carrier is {hi, lo}, of cardinality 2.
- It does not claim that trap closure without reading the priorities that occur infinitely often decides the objective. The even oscillation and the odd sink are both closed under their selected actions; the integer maximum distinguishes them.
- It does not claim that dead-end attraction, or stopping on an even-priority belief, is a parity win.
- It does not claim memoryless determinacy, a progress-measure theorem, or that a positional witness covers every history-dependent strategy on an arbitrary finite parity game. Appendix S declines to import a parity-game theorem. On this carrier the loss side has no alternative action, so the inspection does not need that existence theorem.
- It does not derive the unbounded parity family, Zielonka recursion, quasipolynomial bounds, mean-payoff parity, stochastic almost-sure winning, alternating tree automata, or infinite arenas or infinite priority sets.
- It does not ignore an omitted successor. Every listed successor was used.
- It does not claim original-world soundness (WDP-CHS-O02), native binding (WDP-CHS-O03), physical readout, a continuum limit, a physical law, or authorization.
- It does not close WDP-CHS-O01 as stated in Appendix S. The open sentence remains. This note records only the five-belief certificate.
