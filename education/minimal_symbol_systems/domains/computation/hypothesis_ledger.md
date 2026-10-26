# Hypothesis Ledger for Theoretical Computer Science & Automata Theory

**Domain Key:** `computation`  
**AuthorityEffect:** `None`  

Statuses below refer to the stated models, not to the frozen Genesis source or a Python/Lean equivalence. See the [publication review](../../publication_review.md) for current executions.

| hypothesis_id | statement | verification_method | invalidation_criterion | status |
| --- | --- | --- | --- | :---: |
| `hyp_computation_germ_distinctness` | The primitive difference pair $(a, b)$ with $r a b$ and $\neg r a a$ strictly separates $a \neq b$. | Lean 4 proof (`irrefl_distinct`) and Python assertion. | An instance where $a = b$ satisfies $r a b \wedge \neg r a a$. | `VERIFIED` |
| `hyp_computation_transposition_sign` | Transposition operator $\sigma(a, b) = (b, a)$ satisfies boundary sign inversion $\partial_1(\sigma(e)) = -\partial_1(e)$. | Python exact integer boundary evaluation. | Any directed edge where $\partial_1(\sigma(e)) \neq -\partial_1(e)$. | `VERIFIED` |
| `hyp_computation_boundary_closure` | Discrete boundary operators over simplicial computational chains satisfy $B_1 B_2 = 0$. | Python integer matrix multiplication. | Any non-vanishing entry in $B_1 B_2$. | `VERIFIED` |
| `hyp_computation_fuel_monotonicity` | In non-halting deterministic Turing execution, remaining fuel strictly decreases monotonically by 1 per step. | Python step receipts and Lean 4 `fuel_strictly_decreases`. | A transition where fuel does not decrease by exactly 1. | `VERIFIED` |
| `hyp_computation_cycle_detection` | A deterministic Turing or graph reduction machine entering a previously visited configuration enters a periodic cycle and will not halt. | Python hash/index cycle detector emitting `FuelStatus.CYCLE_DETECTED`. | A deterministic machine reaching a halting state after repeating an identical configuration without perturbation. | `VERIFIED` |
| `hyp_computation_gap_obstruction` | `HaltingIncompletenessObstruction` is a legacy scenario label, not a proved impossibility result. | The former fixed-root predicate is now characterized exactly by `every_endomap_fixes_root_iff`. | A verified domain-specific theorem would need explicit assumptions and a faithful model bridge. | `WITHDRAWN_AS_THEOREM` |
