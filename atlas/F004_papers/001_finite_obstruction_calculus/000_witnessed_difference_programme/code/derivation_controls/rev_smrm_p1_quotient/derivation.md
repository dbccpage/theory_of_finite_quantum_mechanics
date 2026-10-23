# REV-SMRM-P1-QUOTIENT

## Target
Implement the **Congruence Quotient & Observation Refinement Calculus** (`REV-SMRM-P1-QUOTIENT`, unblocking 3 downstream nodes in `goal_dag.jsonl`). Using `certified_progress.observation` and `certified_progress.structural`, we verify when an observation map $q : S \to Y$ forms a congruence on a finite relational model $M$, construct the exact quotient model $M / {\sim_q}$ when it is a congruence, and compute the minimal observation refinement (`refine_observation`) when non-congruence causes loss of information.

## Mathematical Formulation

Let $M = (S, O, Q, c, T)$ be a finite relational model and let $q : S \to Y$ be an observation map inducing the equivalence relation $s \sim_q s' \iff q(s) = q(s')$.
1. **Congruence Criterion (`is_congruence`)**: $q$ is a congruence for $M$ if and only if for all $s \sim_q s'$ and every action $a$:
   - $\forall o \in O,\; o(s) = o(s')$,
   - $\forall t \in T(s, a),\; \exists t' \in T(s', a)$ such that $q(t) = q(t')$ and $c(s, a, t) = c(s', a, t')$.
2. **Quotient Model (`quotient_model`)**: When `is_congruence(M, q)` holds, $M / {\sim_q}$ is well-defined on quotient classes $[s]_q$ and passes `check_quotient(M, q)`.
3. **Refinement Repair (`refine_observation`)**: When `is_congruence(M, q)` fails, iterative partition splitting refines $q \mapsto \widehat{q}$ until `is_congruence(M, \widehat{q})` holds and `check_refinement(M, q)` passes.

## Verification Summary
- Coarse non-congruent observation fails `is_congruence`.
- Refined observation $\widehat{q} = \mathrm{refine\_observation}(M, q)$ restores congruence and passes both `check_quotient` and `check_refinement`.
