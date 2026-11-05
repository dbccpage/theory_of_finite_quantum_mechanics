# PROD-P4

## Target
Bind the **P4 Observation-Budget Planner** (`PROD-P4`) to `omega_engine_cognitive_operations` via `plan_observation_budget` and `WdpObservationBudgetAdapter`. Given an instrument menu with exact rational prices and a set of target state pairs to separate (`PROD-P4-NEXT-1`, `PROD-P4-KILL`), the planner computes and independently verifies the minimum-cost separating suite and synthesizes the least-cost adaptive procedure preserving enabled future operations (`REV-SMRM-P4-FUTURE`).

## Mathematical Formulation

Let $\mathcal{I}$ be a finite instrument menu with prices $c : \mathcal{I} \to \mathbb{Q}_{>0}$ and outcome maps $o_I : S \to Y_I$, and let $\mathcal{P} \subseteq S \times S$ be the target pairs to separate.
1. **Minimum-Cost Separating Suite (`WdpObservationPlanner`)**: Finds $\Sigma^* \in \arg\min_{\Sigma \subseteq \mathcal{I}} \sum_{I \in \Sigma} c(I)$ subject to $\forall (s, s') \in \mathcal{P},\; \exists I \in \Sigma,\; o_I(s) \ne o_I(s')$.
2. **Future-Operation Preservation (`realizable_observation.construct`)**: Synthesizes and verifies an adaptive observation-and-restore procedure of cost `15/4`, strictly below the static non-disturbing suite cost `6`.

## Verification Summary
- `plan_observation_budget` in `omega_engine_cognitive_operations` selects `("I_pair01", "I_pair12")` at cost `"7/2"` (strictly beating the monolithic instrument at cost `"5"`), verifies future-operation preservation at cost `"15/4" < "6"`, and refuses infeasible pair requests.
