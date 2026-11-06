# Hypothesis Ledger for Pure Mathematics, Category Theory & Homological Algebra

**Domain Key:** `mathematics`  
**AuthorityEffect:** `None`  

Statuses below refer to the stated models, not to the frozen Genesis source or a Python/Lean equivalence. See the [publication review](../../publication_review.md) for current executions.

| hypothesis_id | statement | verification_method | invalidation_criterion | status |
| --- | --- | --- | --- | :---: |
| `hyp_mathematics_germ_distinctness` | The primitive difference pair $(a, b)$ with $r a b$ and $\neg r a a$ strictly separates $a \neq b$. | Lean 4 proof (`irrefl_distinct`) and Python assertion. | An instance where $a = b$ satisfies $r a b \wedge \neg r a a$. | `VERIFIED` |
| `hyp_mathematics_boundary_closure` | Discrete boundary operators over simplicial complexes satisfy $d_1 \circ d_2 = 0$ represented by exact integer matrix product $B_1 B_2 = \mathbf{0}$. | Exact integer matrix multiplication in `SimplicialComplex.compute_boundary_nilpotency` and Lean 4 `SimplicialMorphism.boundary_nilpotence`. | Any complex where $B_1 B_2 \neq \mathbf{0}$. | `VERIFIED` |
| `hyp_mathematics_gap_obstruction` | `UncountableContinuumObstruction` is a legacy scenario label, not a proved impossibility result. | The former fixed-root predicate is now characterized exactly by `every_endomap_fixes_root_iff`. | A verified domain-specific theorem would need explicit assumptions and a faithful model bridge. | `WITHDRAWN_AS_THEOREM` |
