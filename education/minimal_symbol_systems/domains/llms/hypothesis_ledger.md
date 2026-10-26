# Hypothesis Ledger for Machine Learning, LLMs & Transformer Token Dynamics

**Domain Key:** `llms`  
**AuthorityEffect:** `None`  

Statuses below refer to the stated models, not to the frozen Genesis source or a Python/Lean equivalence. See the [publication review](../../publication_review.md) for current executions.

| hypothesis_id | statement | verification_method | invalidation_criterion | status |
| --- | --- | --- | --- | :---: |
| `hyp_llms_germ_distinctness` | The primitive difference pair $(a, b)$ with $r a b$ and $\neg r a a$ strictly separates $a \neq b$. | Lean 4 proof (`irrefl_distinct`) and Python assertion. | An instance where $a = b$ satisfies $r a b \wedge \neg r a a$. | `VERIFIED` |
| `hyp_llms_boundary_closure` | Discrete simplicial boundary operators over token 2-complexes satisfy $B_1 B_2 = \mathbf{0}$. | Python exact integer matrix product computation. | Any non-vanishing matrix entry in $B_1 B_2$. | `VERIFIED` |
| `hyp_llms_causal_acyclicity` | Causal self-attention directed graphs enforce strict acyclicity and lower-triangular precedence ($j < i$). | Python topological sort and acyclicity verification. | An attention edge directing from future token to past token. | `VERIFIED` |
| `hyp_llms_gap_obstruction` | `ContinuousGradientObstruction` is a legacy scenario label, not a proved impossibility result. | The former fixed-root predicate is now characterized exactly by `every_endomap_fixes_root_iff`. | A verified domain-specific theorem would need explicit assumptions and a faithful model bridge. | `WITHDRAWN_AS_THEOREM` |
