# CODA-CS-Q Lean claim map

The formal statement, carrier, and assumptions determine the scope. Build and axiom evidence comes from a fresh run with `lean4/lean-toolchain`; this map does not assert current execution success.

| Claim | Declaration | File | Formal scope |
|---|---|---|---|
| CSQ-T1 | `Coda.CSQ.exact_on_image` | `Algebra.lean` | Arbitrary types with explicit witness image carrier; runtime checks Prof(D) only |
| CSQ-T1-UNIQUE | `Coda.CSQ.image_factor_unique` | `Algebra.lean` | Both factors recover q and are invariant under equal profile values |
| CSQ-T2 | `Coda.CSQ.approximate_collision_bound` | `Algebra.lean` | Abstract additive ordered distance carrier with stated symmetry and triangle assumptions |
| CSQ-T2-COR | `Coda.CSQ.metric_zero_error_implies_equality` | `Algebra.lean` | Requires separation and the explicit MetricSpace fields |
| CSQ-T2-CNT | `Coda.CSQ.pseudometric_zero_error_does_not_imply_equality` | `Algebra.lean` | Boolean indiscrete countermodel |
| CSQ-T3 | `Coda.CSQ.lipschitz_access` | `Algebra.lean` | Abstract ordered-carrier theorem; real K-Lipschitz specialization is prose, not instantiated in Lean |
| CSQ-T4 | `Coda.CSQ.samples_not_query` | `Algebra.lean` | Boolean Point3 analogue only; real quadratic theorem is prose plus rational tests |
| CSQ-T5 | `Coda.CSQ.whole_codomain_needs_extension` | `Algebra.lean` | Empty-domain theorem; runtime separately refuses empty evaluation domain |
| CSQ-T5-INHABITED | `Coda.CSQ.total_factor_of_inhabited` | `Algebra.lean` | Uses Classical choice and an inhabited default; finite runtime does not construct arbitrary total extensions |
| CSQ-SCH-01 | `CodaCsQ.admissible_implies_all_eight` | `T02BridgeAdmissibility.lean` | Projection of recorded hypotheses; no continuum existence certificate |
| CSQ-TRM-01 | `CodaCsQ.factorization_implies_named_terminalizers_agree` | `T03NamedTerminalizers.lean` | Named maps q and factor composed with profile |
| CSQ-TAX-01 | None | — | Runtime diagnostic taxonomy, not a Lean seven-class theorem |
| BRIDGE-002 | `CodaCsQ.query_family_factorization_implies_fiber_constant` | `T01FactorizationFiberConstancy.lean` | Assumes family factorization; degree metadata is not a polynomial certificate |
| BRIDGE-004 | `CodaCsQ.TranslationSemigroup` | `D01D02Records.lean` | Definition only; Python computes f(x+h); no exponential generator theorem |
| BRIDGE-005 | `CodaCsQ.ActionCompositionSemigroup` | `D01D02Records.lean` | Definition only; Python adds s_h+s_k; no variational action theorem |
| CSQ-AUT-01 | `CodaCsQ.terminalizers_not_automatic_from_flags` | `T03NamedTerminalizers.lean` | Diagnostic model only; no operational permission |

The alternate `CodaCsQ` carrier has `factorization_implies_fiber_constancy`, `q_bar_on_image_well_defined`, `fiber_constancy_implies_image_factorization`, and `factorization_iff_fiber_constancy_on_image` in `T01FactorizationFiberConstancy.lean`. These are standalone declarations, not aliases to absent `Coda.imageFactor` helpers.

`CodaCsQ.BridgePacket14.field_count_eq_fourteen` records the declared field count. It does not validate the analytic interpretation of those slots. `CodaCsQ.terminalizers_not_automatic_from_flags` separately exhibits disagreeing named maps.
