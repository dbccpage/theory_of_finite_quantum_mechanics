# Feasible Balance Hyperplane Configurations Admit Zero Residual within Candidate Charts

Type: observation
Confidence: high
Source: Candidates strategy_L01_N04, strategy_L01_N06 (Level 1 falser reports)
Relevant to: Evaluating the true exclusion power of the 24 linear balance equations on the candidate solution variety in Route A and Route D.

## Statement
The 24 linear balance equations $\sum_{k=0}^5 \operatorname{Re}(P_{jk}) = 6$ and chart inequalities $\operatorname{Re}(P_{0j}) \ge 1$ provide zero algebraic contradiction or refutation power on the candidate variety within the candidate charts $\mathcal{C}_j = \{ x \in \mathbb{R}^{440} : \operatorname{Re}(P_{0j}) \ge 1 \}$.
Specifically:
1. There exist explicit complex coordinate configurations lying strictly within Chart $\mathcal{C}_0$ that satisfy all entry unimodularity bounds $|z_j|^2 = 6$, chart inequalities $\operatorname{Re}(z_0) \ge 1$, and linear balance equations $\sum_{j=0}^5 z_j = 6$ with zero residual. For example:
   $$z = (1 + i\sqrt{5}, \; 1 - i\sqrt{5}, \; 1 + i\sqrt{5}, \; 1 - i\sqrt{5}, \; 1 + i\sqrt{5}, \; 1 - i\sqrt{5})$$
   satisfies $\operatorname{Re}(z_0) = 1 \ge 1$, $|z_j|^2 = 1^2 + 5 = 6$ for all $j$, and $\sum_{j=0}^5 z_j = 6 + 0i = 6$.
2. The linear balance threshold condition (five entries $x_j \le 71/100$) prunes exactly $0.0000\%$ of feasible points in Chart $\mathcal{C}_0$ (tested across 77,030 feasible points on the hyperplane $\sum x_j = 6$ with $x_0 \in [1, \sqrt{6}]$).
3. The coordinate-368 separation verified in Lean 4 (`low_row_box_empty`) is an artifact of evaluating an off-domain test box $[-1/2, 1/2]^6$ where the maximum possible coordinate sum is $6 \times 0.5 = 3 < 6$. On any box intersecting the true balance hyperplane, the balance equations provide zero coordinate separation.

## Evidence
1. Evaluated in strategy_L01_N04_falser: candidate vector $z = (1+i\sqrt{5}, 1-i\sqrt{5}, \dots)$ satisfies $\operatorname{Re}(z_0) = 1.0 \ge 1$, $\sum_{j=0}^5 z_j = 6.0 + 0.0j$ (residual $0.00$), and all $|z_j|^2 = 6.0$ (residuals $\le 8.88 \times 10^{-16}$).
2. Evaluated in strategy_L01_N06_falser: Monte Carlo sampling of $1,000,000$ points on the balance hyperplane in Chart $\mathcal{C}_0$ found $77,030$ feasible points; exactly $0$ out of $77,030$ satisfied five coordinates $\le 0.71$ ($0.0000\%$ pruned).

## Implications
- **What it supports**: Proves that the 24 balance equations cannot by themselves refute the candidate variety or substitute for high-dimensional coordinate subdivision.
- **What it does not support**: Does not mean the balance equations are false; they are exact algebraic consequences of column gauge and unitarity, but they define a non-empty affine slice that intersects the variety.
- **Narrowest defensible claim**: The 24 balance equations admit exact solutions on the boundary of Chart $\mathcal{C}_j$ with entry moduli equal to $\sqrt{6}$, and prune $0\%$ of interior feasible points.
- **Next test needed**: In Route A, branch-and-prune cannot rely on balance filtering to eliminate the 120 unconstrained candidate coordinates; non-balance relations must be deployed.

## Caveats
The balance equations are valid as linear constraints in an SDP or Krawczyk system, but strategies that claim balance equations alone prove variety emptiness commit an off-domain fallacy.
