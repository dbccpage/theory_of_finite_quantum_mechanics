# Six-Chart Transition Pigeonhole Cover for Gauged MUB Candidates

Type: theorem
Confidence: high
Source: Candidates strategy_L00_N00, strategy_L00_N01, strategy_L00_N04, strategy_L00_N05, strategy_L00_N07 (Level 0)
Relevant to: Partitioning the candidate search space of complex Hadamard transition matrices into six compact charts away from degenerate neighborhoods.

## Statement
Let $W \in \mathbb{C}^{6 \times 6}$ be a transition matrix between two column-gauged complex Hadamard bases, satisfying:
$$\sum_{j=0}^5 \operatorname{Re}(W_{0j}) = 6.$$
Then there exists at least one index $k \in \{0, \dots, 5\}$ such that:
$$\operatorname{Re}(W_{0k}) \ge 1.$$
Since every entry of an unscaled complex Hadamard transition matrix satisfies $|W_{0k}|^2 \le 6 < 9$, every solution lies in the union of the six overlapping candidate charts:
$$\mathcal{C}_k = \left\{ x \in \mathcal{B} : \operatorname{Re}(W_{0k}) \in [1, 3] \right\} \qquad (k \in \{0, \dots, 5\}).$$

## Proof
Suppose for contradiction that $\operatorname{Re}(W_{0j}) < 1$ for all $j \in \{0, \dots, 5\}$. Summing these six strict inequalities:
$$\sum_{j=0}^5 \operatorname{Re}(W_{0j}) < \sum_{j=0}^5 1 = 6.$$
This contradicts the derived balance identity $\sum_{j=0}^5 \operatorname{Re}(W_{0j}) = 6$.
Therefore, at least one index $k$ satisfies $\operatorname{Re}(W_{0k}) \ge 1$.
Furthermore, because $|W_{0k}| \le \sqrt{6} \approx 2.4495 < 3$, $\operatorname{Re}(W_{0k}) \le 3$ is satisfied by all valid solutions. Hence the union $\bigcup_{k=0}^5 \mathcal{C}_k$ covers the entire candidate variety.

## Hypotheses / Conditions
1. The transition matrix $W = U^\dagger V$ is formed from two isometrically scaled bases $U, V$ satisfying top-row column gauge $(U)_{0j} = 1$ and $(V)_{0j} = 1$.
2. The balance identity $\sum_{j=0}^5 \operatorname{Re}(W_{0j}) = 6$ is satisfied.

## How It Applies
This theorem partitions the 440-variable candidate variety into six charts, each bounded away from zero in one transition coordinate ($\operatorname{Re}(W_{0k}) \ge 1$).
- What it supports: Supports an exhaustive partition of the candidate variety into six explicit charts.
- What it does not support: Does not by itself exclude any of the six charts without independent refutations.
- Narrowest defensible claim: Any matrix with row sum 6 has at least one real entry greater than or equal to 1.
- Next test needed: Test whether non-zero expansion centers within each chart achieve derivative contraction.

## Caveats
Mechanized in Lean 4 (`SzollosiGaugedCover.lean`, theorem `augmented_solution_chart_cover`). While each chart restricts one coordinate to $[1, 3]$, the remaining 439 coordinates retain their full boxes unless subdivided.
