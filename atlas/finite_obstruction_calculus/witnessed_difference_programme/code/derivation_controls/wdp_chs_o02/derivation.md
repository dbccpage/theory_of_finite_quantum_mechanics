# WDP-CHS-O02

Goal id: WDP-CHS-O02

Selected scope for WDP-CHS-O02 is recorded in this note.

## Selected scope

The finite rejection-reuse profile already written in Appendix Q.6 and `docs/derivations/rejection_rule_reuse.md`, and inside it the `d=2` mandatory fixed-`R1` arena with no fallback. No new carrier is selected.

`D={-1,0,1}`, `X0=D²` (nine pairs), `X1=f01(X0)`, `X2=f12(X1)`. Tasks are `d` in `{-1,0,1,2}`. Maps: `f01(x,y)=(x+y,x-y)`, `f12(u,v)=(u,v+u)`, decoder `H(r,t)=(t/2,r-t/2)`, with `HF` the identity on `X0`. Prices, as stated there: proposal `1`, full check `2`, emission `1`, guard `1/2`, adjacent transport `1`, installation `3`, shared budget `18`.

On the `d=2` no-fallback arena the original solution set is `{(1,1)}`, so the solution count is `1`. Fixed `R1` rejects the level-1 image `(2,0)` and the level-2 image `(2,2)`. With that guard mandatory and no fallback, the emittable valid set is empty and the initial state lies in a target-disjoint loss trap, so the set of admissible winning strategies from that initial state is empty. Restoring the two-transport original route is a different arena, of exact value `6`. The witness read off those three stated quantities is `(original solutions, winning strategies from the initial state, restored value)=(1,0,6)`.

Appendix S names A1–A3 are assumptions on a declared vocabulary. They are not these maps. The named-proposal value `4`, the guarded costs `9/2` and `15/2`, the blind-scan figures, and the shared-ledger total `17` are other menus or one paid run on this same carrier. They are not the no-fallback strategy count, and they are not reused here as a discharge of the open sentence.

This note inspects that opened text. It does not execute a new checker, does not select a further carrier, and does not close WDP-CHS-O02.

## Hypotheses

H1. The carrier, inverses, and task predicates are exactly those in rejection-reuse §1 and Appendix Q.6. The nine printed rows are the whole of `X0`, `X1`, and `X2`. No further pair is admitted by field name.

H2. Prices, budget, and menu boundaries are exactly those in rejection-reuse §3. A named proposal, a mandatory safe guard, a restricted blind scan, a shared-ledger continuation, and the `d=2` no-fallback trap are different arenas. A number from one is not a number from another.

H3. A1 says accepted resolutions decode to valid original answers. A2 says the resolution vocabulary is finite and the table checks terminate. A3 says each supplied resolution is classified in both directions. In Appendix S.1.1 these are assumptions, not theorems. WDP-CHS-N03 is in force: an effective check is not a proof of A1 or of A3.

H4. C01 gives an original answer only by composing P01 target reachability with a sound decoder, and only when A1 holds. C04 gives source unsatisfiability from an arena loss only through an explicit map sending every original solution to an admissible winning strategy that preserves task and requirements. A3 classifies supplied resolutions and supplies no missing solution or enabled operation. GEN-WDP-49 and GEN-WDP-54 keep those §20.6 maps as hypotheses. A loss record and an authorization flag do not supply them. Theorem 3.2 and Corollary 3.3 separate the two directions: an empty accepted set can be vacuously sound and still say nothing about a nonempty source.

H5. The goal row WDP-CHS-O02 has empty `depends_on`, no acceptance field, and fence WDP-CHS-N03. Appendix S.0 leaves O01–O03 open. The fence does not cancel that open sentence. It forbids the step named in H3. That step is not taken.

## Derivation

### What the three duties are

The rejection-reuse note separates three questions: whether an emitted answer is correct, whether every original solution remains obtainable, and whether a specified cost bound is preserved. Appendix S.10 states the same separation as WDP-CHS-O02: original-world validation soundness, completeness, and constructive winning-strategy coverage remain profile-specific adapter duties, and declaring A1–A3 does not discharge them.

On this labelled profile those duties are three different pieces of data.

Soundness, when claimed, is the installed decoder together with inclusion of the actual emittable set in the valid set. It is not the label A1, and it is not a scalar acceptance bit.

Completeness, when claimed, is the other inclusion: every valid original has its valid preimage in the emittable set. Classification of a supplied proper subset does not restore an omitted original.

Constructive winning-strategy coverage, when claimed, is an explicit admissible winning strategy for each original solution, preserving task and requirements, together with the cost bound that the declared arena actually protects. A loss trap on a different menu is not that map.

### Soundness is the decoder, not the label

For `d=1` the printed paths are `(0,1)→(1,-1)→(1,0)` and `(1,0)→(1,1)→(1,2)`. `H` sends `(1,0)` back to `(0,1)` and `(1,2)` back to `(1,0)`. The scalar report `u=1` does not distinguish those pairs. Q.6 states that reporting the first coordinate alone does not decode the pair.

The off-carrier name `(1,0)` at level 1 is not an element of `X1`. Its formal level-1 decoder is `(1/2,1/2)`, which is not in `X0`. The same field name at level 2 is in `X2` and decodes to the valid pair `(0,1)`. Field-name admission is not `H`.

A checker that admits sums in `{d-1,d}` accepts the invalid original `(0,0)` at `d=1`. Declaring A1 does not install `H`, and it does not install that checker's predicate. The nine-row table, the subset replays, and the arena certificates are effective checks of this finite example. WDP-CHS-N03 forbids reading them as proofs of A1. They are not so read. Q.6 says those checks complete this finite example, not a general correspondence between recursive engine execution and external tasks.

### Completeness is the second inclusion

For inverse bijections, rejection-reuse §2 states

`g(E)⊆G_X` if and only if `E⊆G_Y`,

and

`G_X⊆g(E)` if and only if `G_Y⊆E`.

These are not the same claim. `E` empty makes the first inclusion vacuous. At `d=1` the stated solution count is `2`, so the empty emittable set omits both solutions. The one-point method `M(d)` in `X1` chooses one valid answer. The text says full solution coverage additionally retains every valid proposal. A3, applied to a supplied proper subset, checks that subset. C04 says it supplies no missing solution.

The stated solution counts on `X0` are `2,3,2,1` for `d=-1,0,1,2`. The printed nine-row table agrees: only `(1,1)` has coordinate sum `2`. `H(2,2)=(1,1)` and `F(1,1)=(2,2)`, so that solution has one level-2 preimage. Retaining that one preimage is a coverage fact about an emittable set. It is not settled by writing the name A3.

The certified-progress evidence note states the matching boundary for A2: checker completeness on a finite listed vocabulary does not provide original-solution strategy coverage.

### The d=2 no-fallback witness

Fixed `R1` is the predicate `u≠1`, not the parameterized rule `R_d`. Q.6 and rejection-reuse §5.1 state that at `d=2` it rejects the unique valid level-1 candidate `(2,0)` and the unique valid level-2 candidate `(2,2)`. The same assumption names A1–A3 do not transport the `d=1` rule onto this task. Target 4 of `docs/five_outstanding_derivations.md` says that repeating conditional map axioms without constructing the selected adapter does not close that target.

In the menu where that guard is mandatory and no fallback exists, the text states that the check-retained menu remains sound but loses coverage, and that every reachable nontarget state is a loss trap: rejected valid proposals and checked-invalid proposals return to the root. The certificate includes the initial state. By the stated trap, the winning region does not contain the initial state, so the set of admissible winning strategies from that initial state is empty.

`Sol` on this task is nonempty: its count is `1`. Vacuous decoding of the empty accepted set is the Corollary 3.3 situation, not an installed proof of A1, and not the GEN-WDP-49 biconditional. The rejection row is not a proof of A3. N03 forbids both readings. Neither is used. C04's coverage map is absent while `Sol` is nonempty. GEN-WDP-54 says neither the loss verification record nor an authorization flag supplies that map. WDP-CHS-N02 keeps the loss relative to the declared arena. The trap does not say that `x+y=2` has no original solution.

The text states that restoring the two-transport original route gives exact value `6`, not loss. From level 2 that fallback is two transports plus the original solution. That restored arena is a different profile. The unguarded named-proposal menu solves `(1,1)` at cost `4`. That is also a different profile. The labels A1–A3 construct neither `H`, nor the emittable set, nor the route of value `6`.

### Other stated costs are not this strategy count

On the named-proposal menu every success pays proposal, check, and emission, and that policy attains the value, so the minimax value is exactly `4`. Forcing the safe guard, which the text says preserves individual reachability, raises the operating value to `9/2` and the setup-inclusive value to `15/2`. The protected total bound `4` fails while coverage of each single solution survives. That is a cost-only separation on a menu that still emits.

The restricted blind scan is a different menu. At `d=2` its maximal-guard-plus-setup value is `39/2`, which exceeds budget `18`, and the text says this is not the named-proposal optimum. The bare scan value `28` and the maximal-guard operating value `33/2` belong to that scan family. One shared-ledger run totals `17`, which is at most `18`, and the text says no optimality claim is made for that wrapper.

None of `4`, `9/2`, `15/2`, `6`, `17`, `28`, `33/2`, or `39/2` is the number of winning strategies from the initial state of the no-fallback arena. That number, read from the stated trap, is `0`. The solution count on the same task is `1`. The restored value `6` is the other arena.

### Boundary

Writing down A1–A3 on this profile does not discharge original-world validation soundness (the map `H` and accepted-set inclusion), completeness (`G_Y⊆E`, equivalently retention of every valid original), or constructive winning-strategy coverage (a task-and-requirement-preserving map from each original solution to an admissible winning strategy, with the bound the declared arena protects). On the no-fallback arena those three data are: a decoder that is not installed by the assumption label, an empty emittable valid set against one original solution, and no winning strategy from the initial state. The triple `(1,0,6)` records that gap and the value of a different, restored arena. It does not fill the gap.

The opened sources do not name a further carrier together with quantities an exact test has not already been said to check. This note therefore does not assign a new numerical obligation. It does not reuse X05's reachability optimum `2`, the named-proposal optimum `4`, target 3's optimum `15/4`, or the class count `29,771` as a calculation that would close WDP-CHS-O02. Target 4 leaves general engine adapters open. Target 3 leaves unrestricted source/world correspondence outside its table. Target 5 says the full O02/O03 obligations retain a separate open scope. The reading-order paragraph of `docs/five_outstanding_derivations.md` leaves source/world adequacy, physical scalar and readout choices, and the Q-continuum as separate open extensions.

No Python, Rust, or Lean checker was executed for this note. The argument does not prove A1 or A3, does not construct a missing coverage map for an arbitrary profile, and does not close WDP-CHS-O02. Appendix S still states the open sentence. A finite model does not establish a continuum limit, a physical law, or a closed theorem outside the selected scope.

## Claims this note does not make

- It does not claim that the nine-row table, the emission or rejection subsets, the arena certificates, or the `d=2` rejection row proves A1 or A3. WDP-CHS-N03 forbids that step, and that step was not used.
- It does not claim that declaring A1 installs `H`, that declaring A2 installs original-solution strategy coverage, or that declaring A3 supplies a missing solution or an enabled operation.
- It does not claim that vacuous soundness of an empty accepted set is coverage, or that it is the GEN-WDP-49 biconditional. Corollary 3.3 separates those readings. At `d=1` the empty set omits both stated solutions. At `d=2` it omits `(1,1)`.
- It does not claim that the no-fallback loss trap shows `x+y=2` has no original solution. The opened text states that `(1,1)` is an original answer, and that restoring the two-transport route gives value `6`, not loss. Loss stays relative to the declared arena.
- It does not claim that `4`, `9/2`, `15/2`, `6`, `17`, `28`, `33/2`, or `39/2` is the number of winning strategies from the initial state of the no-fallback arena. That number is `0`. The value `6` is a different arena. The value `4` is the unguarded named-proposal menu. The values `9/2` and `15/2` are the mandatory-guard named-proposal menu. The scan figures are the restricted blind-scan menu. The total `17` is one shared-ledger run and is not claimed optimal.
- It does not claim that field-name admission of level-1 `(1,0)`, whose formal decoder is `(1/2,1/2)` outside `X0`, is an original solution.
- It does not claim that a loss verification record or an authorization flag supplies the §20.6 maps. GEN-WDP-54 says they do not.
- It does not reuse a completed one-dimensional value from another target — X05's optimum `2`, target 3's optimum `15/4`, or the class count `29,771` — as the witness for this profile.
- It does not claim that this profile discharges every original-world adapter, source/world adequacy, native repair realization, instrument realization, guarded-history coherence, parity (WDP-CHS-O01), native binding (WDP-CHS-O03), authorization, a physical law, or a Q-continuum limit.
- It does not claim that Appendix S withdraws the open sentence. The goal row remains open. This note records only the stated separation on the selected finite profile.
