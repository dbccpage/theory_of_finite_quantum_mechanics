# Category: moore_penrose_least_squares_annihilation

Type: failed_approach_category
Pattern: Moore-Penrose pseudoinverses $R = (J^T J)^{-1} J^T$ annihilate residuals at least-squares stationary points ($J^T F = 0$), causing zero center displacement $R F(x_0) = 0$ and trapping overdetermined Krawczyk contractors.
Count: 2

## Entries
| # | Original File | One-line Summary |
|---|---------------|------------------|
| 1 | strategy_L00_N17 | Moore-Penrose preconditioner projects onto $\operatorname{im}(J_0)$ and has kernel $(\operatorname{im} J_0)^\perp$; at least-squares critical points where $J^T F = 0$, displacement $R_{\text{opt}} F(x_0) = 0$ vanishes, preventing coordinate separation. |
| 2 | strategy_L00_N23 | Regularized Moore-Penrose preconditioner maps the Jacobian left nullspace to zero, eliminating left-null residual displacement; setting preconditioner rows to left nullvectors leaves the identity diagonal term uncancelled, requiring first-order shifts $> 2\Delta_i$. |
