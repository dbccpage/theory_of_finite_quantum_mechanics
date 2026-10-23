# Review of the declared Genesis process comparison

AuthorityEffect: None. AI self-review, awaiting human review.

Scope: PGW-MINIMAL-OR-INITIAL-REFUSED on main 4d50f22373578df83989dc8ec09fdface91289c2.
Method: inspect the defined process objects, morphisms, complete finite-word
readouts, cardinality proof, actual-source replay relation and independent
exact finite orbit audit. Not rebuilt by this review; the authoring campaign
receipt supplies the successful target replay.

Result: 0 FULL, 1 NARROWED, 0 OVERCLAIM for the requested whole-process question.
The declared comparison results below compile; they do not certify the full
Alpha engine's class membership or minimum program/declaration cost. The
historical refusal record and its PROVED_PROSE status remain unchanged.

| Atomic claim | Declaration and exact line | Verdict |
|---|---|---|
| Every finite action word has the same readout after an invisible clock extension | `all_words_agree` (`lean4/CampaignGenesisProcessComparison.lean:164`) | FULL in the declared class |
| No finite-state process maps to its period-(card+1) lift | `no_initial_in_clock_closed_class` (`lean4/CampaignGenesisProcessComparison.lean:175`) | FULL with a chosen action |
| Any self-loop forbids a map to the invisible two-clock lift, without state finiteness | `no_clock_hom_of_self_loop` (`lean4/CampaignGenesisProcessComparison.lean:210`) | FULL |
| Actual optional source runs agree with source replay, including failure | `source_advance_matches` (`lean4/CampaignGenesisProcessComparison.lean:230`), `source_run_matches` (`lean4/CampaignGenesisProcessComparison.lean:243`) | FULL |
| Actual source supply is a self-loop and gives the clock obstruction | `source_supply_self_loop` (`lean4/CampaignGenesisProcessComparison.lean:248`), `no_source_initial_in_clock_closed_class` (`lean4/CampaignGenesisProcessComparison.lean:251`) | FULL for the regime-history interpreter |
| A reachable, behaviorally reduced finite process has minimum state count among same-answer finite models | `all_words_minimum_size` (`lean4/CampaignGenesisProcessComparison.lean:183`) | FULL with explicit reachability/reduction premises |
| Adequacy alone forces minimum state count | `nonminimal_adequate_process` (`lean4/CampaignGenesisProcessComparison.lean:120`) | REFUSED by the concrete control |
| Whole Alpha engine minimum or initiality in an unspecified class | not proved | NOT PROVED; original boundary retained |

The class admits additional unobserved internal state. Morphisms preserve
actual roots, actions and readouts. The finite-state theorem uses a nonempty
action alphabet (a chosen action is explicit). The self-loop theorem drops
state finiteness and applies to the exact actual-source regime interpreter.
Source failure is absorbing, not a no-op. Finite state-cardinality minimality
is a different resource claim from program size, declaration count or the
engine input floor. No conclusion about Alpha runtime/license behavior follows.

Numbers recomputed: 682 unary Boolean-readout processes, 41,764 clock-component
candidate maps, 98,346 exactly behavior-equal pairs, 1,230 valid minimum-size
comparisons, and all sixteen maps into the supply-loop clock countermodel.
SymPy checks the census and the clock target's zero fixed-point trace. Three
explicit missing-premise/morphism controls are checked. Sixteen terminal
axiom audits match the successful replay; no new kernel axiom is introduced.
The general Lean results have no independent-check state bound.

What the scanner cannot decide: which challenge interface and morphisms are
appropriate for the full historical engine, whether it satisfies reduction and
reachability in a finite model, or whether a human accepts the selected class.
The declared class choices are not inferred from a frozen tag or repeated runs.
