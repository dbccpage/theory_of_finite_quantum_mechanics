# Paper 001 — Claim ledger

AuthorityEffect: None. Author-review draft, 2026-10-09. Every row has one status: definition, proved, negative boundary, or withdrawn. A proved row is elaborated in `lean4/Paper001.lean` and evaluated by `code/sn_mssn_checks.py`.

| ID | Status | Claim | Evidence and limit |
| --- | --- | --- | --- |
| WDP-P001-001 | definition | Native stages, alphabet indices, profiles, atlas rows and homological degrees differ. | §§1–3; crosswalk does not derive every row. |
| WDP-P001-002 | proved | Finite demand cardinality obeys s_next=s−d+b. | Proposition 001.1. Lean `demand_accounting`. Python `demand_account`. Discharged subset and disjoint births are required. |
| WDP-P001-003 | negative boundary | The displayed seven-entry survivor sequence is a chosen ledger example. | §4; it is not a universal native law or physical pressure. |
| WDP-P001-004 | proved | A supplied binary tag can separate one collapsed pair and retain the old report. | §5. Lean `supplied_tag_separates`. Python `supplied_tag_separates`. Finding tags and satisfying many conflicts are separate questions. |
| WDP-P001-005 | proved | Typed old-image recovery implies injectivity of the lift. | Proposition 001.2. Lean `old_image_injective`. Python `old_image_injective`. Off-image rejection is not this theorem. |
| WDP-P001-006 | negative boundary | Term recovery alone implies neither off-image rejection, observation preservation, nor obstruction repair. | §6. Lean `off_image_not_implied`, `observation_not_implied`, `repair_not_implied`. Python `recovery_counterexamples`. |
| WDP-P001-007 | proved | Free monoids on different finite alphabet sizes are nonisomorphic. | Theorem 001.3. Lean `no_free_monoid_iso`. Python `free_monoids_nonisomorphic`. |
| WDP-P001-008 | proved | Discrete categories of different finite object counts are inequivalent. | §7.1. Lean `no_discrete_equivalence`. Python `discrete_categories_inequivalent`. Isomorphism classes are singletons. |
| WDP-P001-009 | proved | Language restriction, partial word recovery and total erasure have different types. | §7.2. Lean `three_contracts_differ_on_a_new_letter`. Python `three_recovery_contracts`. No Ext calculation. |
| WDP-P001-010 | negative boundary | Noninjective codes collapse words; edge traversal transformations preserve different data. | §8. Lean `code_collapses_aa_and_b`. Python `code_collapse_witness` and `edge_multiset_witness`. Decoded edges are not raw bytes or ordered histories. |
| WDP-P001-011 | proved | On the two-point graph, H0 counts undirected components and loops do not lower that count. | §9. Lean `loop_does_not_lower_component_count`, `loops_do_not_lower`, `reduced_h0_of_nonempty`. Python `graph_component_report`. Nonempty vertex set for the displayed reduced-H0 formula. |
| WDP-P001-012 | proved | A chain-map retraction forces homology injectivity. The two-point edge and the filled triangle admit no chain-map retraction fixing the original complex. | Theorem 001.4 and §§9.2–9.3. Lean `homology_injective_of_chain_retraction`, `two_point_retraction_impossible`, `triangle_retraction_impossible`. Python `retraction_recovers_cycle`, `two_point_obstruction`, `triangle_obstruction`. |
| WDP-P001-013 | definition | Chains, cochains, homology, homotopy and directed reachability are distinct. | §9.3; a vanishing homology class is not a homotopy contraction. |
| WDP-P001-014 | definition | MSS grammar has the 22 listed public starts and the declared profile examples. | §10, Appendix A, source grammar. Python `grammar_inventory_matches` compares the appendix with `mssn.ebnf`. Not 22 completed semantic adapters. |
| WDP-P001-015 | definition | Necessary/minimal lifts require a specified repair class, cost and evidence of failure/success. | §11; budget exhaustion is not an impossibility proof. |
| WDP-P001-016 | negative boundary | One selected CHSH expression misses another violated orientation. | §12. Lean `chsh_missed_orientation`. Python `chsh_missed_orientation`. Pairwise signs (1,1,−1,1). Not a physical theory. |
| WDP-P001-017 | withdrawn | Univalence, automatic Postnikov structure, pentagon coherence and universal physics/bisimulation claims do not follow from the cited finite checks. | §12 and the prior physics cleanup record. Withdrawn claims are not reactivated. |
| WDP-P001-018 | proved | A question descends uniquely to the realized report image exactly when it is constant on report fibers. | §13. Lean `exists_descent_of_constant` and `descent_unique`. Python `fiber_descent`. Paper 002 develops the calculus. No automatic cross-repository derivation. |
| WDP-P001-019 | negative boundary | The pinned SnCarrier implementation does not establish unrestricted old-image recovery or its advertised carrier cardinalities. | §6. Lean `refusal_token_round_trip_changes_input` and `carrier_card_table_disagrees_with_higher` in `SnCarrierDischarge.lean`, importing the education `SnCarrier` module. Domain restriction and a corrected cardinality theorem remain open. |

Original CLAIM-MSSN, S(n), and PGM ledgers remain in the source archive. The source map explains their use and supersession; none is merged into a larger count of verified results.
