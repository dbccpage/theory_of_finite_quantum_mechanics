# Original Genesis observer: all-history adapter and source corrections

The recovered original source `001_from_primitive_difference_to_cochain_systems/manuscript.md` (lines 983–1004) declares `(M,U,p,rho,G,T)`, an initial memory, distinction histories in `D*`, and total `rho : C × D* → D*`. `OriginalGenesisObserver.lean` formalizes these signatures directly. Its terminal alphabet is exactly `Proved`, `Refuted`, `Unresolved`, `Outside`, `Refused`. The formal results hold for arbitrary typed carriers and consequently for the original finite carriers; they do not replace `D*` with sampled words.

## Free extension and faithful typed layers

`historyUpdate` processes words in input order. Empty, append and snoc laws are proved. `history_extension_unique` proves that any extension satisfying the empty and snoc equations equals this extension on every word. Thus the induced report is exactly `p(U*(m0,w))`.

The typed adapter preserves memory initial state, update, readout, history reaccess, all-history report, input contexts and grammar terminalization. Recovering the original fields after adaptation is literally the identity. Optional evaluator and policy layers are absent. No encoder from reports or memories into grammar terms is provided by the recovered six, and none is invented by this adapter. Adding such a layer requires declared extra data or the separate necessary/sufficient descent theorem.

## Exact state-context descent

Let `q(w)=U*(m0,w)` with codomain the subtype of reachable states. This presentation is onto by construction. There is a unique context action on reachable states commuting with every original history context if and only if

```
q(v) = q(w) implies q(rho(c,v)) = q(rho(c,w)), for every c,v,w.
```

Necessity follows by applying the adapted action to equal presentations. Sufficiency chooses one representing word for each reachable state; the displayed condition makes its transformed state independent of this choice. Onto presentation proves uniqueness. This is a quotient/factorization theorem about sets. It asserts neither a HoTT equivalence nor Kan fibrancy. Finiteness is unnecessary for the theorem; a finite-state transducer can supply a separate executable all-word decision procedure for its own declared representation class.

Total context functions do not automatically satisfy this condition. The checked counterexample toggles Boolean memory on every input. Empty and length-two histories both reach `false`; the context maps the empty history to a singleton and every nonempty history to empty. Their context images reach `true` and `false`. The function is total on all words but cannot descend to memory states.

## Original classification claims corrected

The formal `O1Criterion` is nonconstancy of the induced history report. `O2Criterion` is a pair of equal-report histories separated by one context. These are the stated original source criteria, not an independent claim about physical consciousness.

Both criteria are invariant under replacing grammar and terminalization, even when the grammar carrier changes. They depend only on `(m0,U,p,rho)`. `full_six_classification_independence_fails` therefore refutes the historical T1 assertion that changing each of all six fields in isolation can change these criteria. This does not make grammar or terminalization dispensable for any separately declared proof/status semantics.

The archived T2 corollary that input-independent updates force O0 is also false: a Boolean memory toggling on every step ignores the input label yet has different empty and singleton reports. The formal counterexample uses two distinct Boolean input labels, so it does not rely on a singleton alphabet. Identity updates do force constant history reports, and a constant profile also refutes O1; both correct sufficient conditions are proved. Identity contexts on the parity observer refute O2, whereas the total non-descending context above satisfies O2.

## Checked evidence and boundaries

Standalone Lean 4.33.1 compilation passed with 18 theorem proofs. The source-bound receipt `lean4/original_genesis_observer_axioms.txt` audits 54 explicit declarations, constructors and fields; its axiom union is only `Classical.choice`, `Quot.sound`, `propext`. There are no `sorry` proofs or added axioms. The receipt contains the exact source SHA-256 and complete compiler output.

The arbitrary-history theorem does not certify arbitrary source contexts by finite sampling. The source phrase “decidable finite question” requires an explicit finite presentation/decision argument for the chosen contexts; finite memory and finite context names alone do not provide a context table over the infinite history domain. The separate native transducer owner supplies a checked finite product-state procedure for represented total finite transducers. Universal finite-table observer descent and this all-history adapter must retain their distinct domains.
