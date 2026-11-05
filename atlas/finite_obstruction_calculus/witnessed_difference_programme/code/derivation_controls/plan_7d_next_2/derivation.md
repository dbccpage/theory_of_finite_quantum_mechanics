# Derivation Control: PLAN-7D-NEXT-2

**AuthorityEffect:** None.

## Scope and Claim

This finite control (`PLAN-7D-NEXT-2`) binds the accepted Lane B (`realizable_observation`) and Lane C (`rejection_reuse` and `antibody_transfer`) finite models to their native owners and verifies their exact rational invariants and hostile controls:

1. **Lane B (`code/realizable_observation`)**:
   - The eight-state Appendix-S realizable-observation replay (`finite_replay_v3.json`) has disturbance/repair optimum $15/4$, adaptive nondisturbing optimum $4$, static `read_all` cost $6$, and original-class-only cost $7/2$, with $5$ replayed instances and $12$ hostile controls rejected.
2. **Lane C (`code/rejection_reuse` and `code/antibody_transfer`)**:
   - The three $9$-element image carriers $X_0 = \{-1,0,1\}^2$, $X_1 = f_{01}(X_0)$, and $X_2 = f_{12}(X_1)$ under $f_{01}(x,y)=(x+y,x-y)$ and $f_{12}(u,v)=(u,v+u)$ with composite inverse $H(r,t)=(t/2, r-t/2)$ yield exact solution counts $(2, 3, 2, 1)$ for $d \in (-1, 0, 1, 2)$, reject the off-image probe $(1,0) \notin X_1$ while admitting $(1,0) \in X_2 \mapsto (0,1) \in X_0$, and verify the named-proposal optimum $4$, mandatory-guard setup-inclusive optimum $15/2$, and nonreset shared fuel budget $18$ ($5$ spent leaves $13$, whereas resetting to $18$ permits $23 > 18$).

## Non-Claims

- This finite control does not claim empirical LLM behavior or unbounded domain transfer.
