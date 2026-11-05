# Sources for claims_ledger.md

All paths are relative to the root of the theory_of_finite_quantum_mechanics repository.

| Ledger item | Source |
|---|---|
| Observer, four layers | `atlas/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md`, Chapter 10, WDP-CH10-D01 to D04 and the interpretive remark after D04 |
| Observation ladder | same file, Chapter 12, WDP-CH12-D01; §12.2 failure modes; WDP-CH12-P01 (observation is not authorization) |
| Measurement packet | same file, Chapter 13, WDP-CH13-D01 |
| Earlier observer tuples (six-component source packet, ten-component operational, five-component world observer, nine-component normalized) | same file, Appendix K.2 and K.3; Chapter 10.1 explains why they are layered rather than merged |
| Observer-packet validator | same file, Appendix G.4 and G.5 |
| Plain-language picture (rule card, block towers) | same file, Appendix R |
| Lean: `ObserverPacket` (presentation, memory, evaluator), `ObservationReceipt`, `AcceptedObservation`, `AuthorityPolicy` | `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/Observer.lean` |
| Lean: blind spot | `Observer.lean`, theorem `presentation_blind_spot` |
| Lean: resolution limit | `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/ObserverResolution.lean`, theorems `pigeonhole_resolution_limit` and `grammar_observer_not_finest` |
| Lean: original Genesis observer `(M,U,p,rho,G,T)` and its layered adapter `TypedLayers` (evaluator and policy optional) | `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/OriginalGenesisObserver.lean` |
| Lean: acceptance is not authority | `Observer.lean`, theorem `acceptance_does_not_entail_authority` |

Gap: the Lean `ObserverPacket` has three fields (presentation, memory, evaluator). Policy is not a field. The evaluator is reduced to `evaluate` and `accepts`, with no defect, repair, cost or terminalizer, and authority is the separate `AuthorityPolicy`. `OriginalGenesisObserver.TypedLayers` carries the policy and the evaluator, but as optional fields. No single Lean structure requires all four Chapter 10 layers together.

| Public definition | Jeremy Carroll, "What the Hell Is an Observer?", LinkedIn, 2026-05-23, https://www.linkedin.com/pulse/what-hell-observer-jeremy-carroll-tmyje/ (text kept in `observer_article_2026-05-23.md`). Formal anchor named there: Paper 000, Primitive Axiomatics of Finite Obstruction Calculus, doi:10.5281/zenodo.23114399. |
