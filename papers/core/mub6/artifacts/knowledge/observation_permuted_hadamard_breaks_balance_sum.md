# Row Permutations in Hadamard Equivalence Orbits Break Transition Balance Identities

Type: observation
Confidence: high
Source: Candidate strategy_L01_N00 (Level 1 falser report)
Relevant to: Column gauge reductions, 24 linear transition balance equations, and the 518,400 permutation orbits in Route A and Route D.

## Statement
Let $H \in \mathbb{C}^{6 \times 6}$ be a complex Hadamard matrix with $H^\dagger H = 6 I_6$, and let $B \in \mathbb{C}^{6 \times 6}$ be a column-gauged candidate basis matrix ($B^\dagger B = 6 I_6$ with $B_{0k} = 1$ for all $k \in \{0, \dots, 5\}$).
The 24 linear transition balance equations:
$$\sum_{k=0}^5 \operatorname{Re}(W_{jk}) = 6, \qquad \sum_{k=0}^5 \operatorname{Im}(W_{jk}) = 0$$
for $W = H^\dagger B$ hold identically if and only if row 0 of $H$ is identically equal to 1 ($H_{0k} = 1$ for all $k$).
If an essential row permutation $P$ from the $518,400$ Hadamard equivalence orbits is applied to $H$ (for example, swapping rows 0 and 1 of $F_6$), the row sums of $W = (P H)^\dagger B$ deviate sharply from 6, evaluating to non-constant values such as $\{6, 3 \pm 5.2i, -6, -3 \pm 5.2i\} \ne 6$.
Consequently, the 24 transition balance identities cannot be asserted under general unitary equivalence without explicitly fixing the row permutation gauge of all constituent Hadamard matrices.

## Evidence
1. The analytical expansion of the row sum of $W = H^\dagger B$ is:
   $$\sum_{k=0}^5 W_{jk} = \sum_{m=0}^5 \overline{H_{mj}} \left( \sum_{k=0}^5 B_{mk} \right) = \sum_{m=0}^5 \overline{H_{mj}} (6 \delta_{m0}) = 6 \overline{H_{0j}}.$$
   This equals 6 if and only if $H_{0j} = 1$ for all columns $j$.
2. In the numerical code probe executed for strategy_L01_N00_falser, evaluating $W = (P F_6)^\dagger B$ where $P$ swaps rows 0 and 1 yielded row sums:
   $$[6.0, 3.0 - 5.20j, -3.0 - 5.20j, -6.0, -3.0 + 5.20j, 3.0 + 5.20j].$$
   The real parts include $3.0$ and $-6.0$, deviating from $6.0$ by up to $12.0$.

## Implications
- **What it supports**: Proves that the transition balance identities are gauge-dependent and require both $H$ and $B$ to have their first rows normalized to all ones.
- **What it does not support**: Does not mean that column gauge is invalid; rather, global unitary equivalence $U_0 = I_6$ fixes the basis frame, and subsequent bases $U_1, U_2, U_3$ cannot have their rows permuted independently without breaking the standard basis gauge.
- **Narrowest defensible claim**: The 24 transition balance equations $\sum_k W_{jk} = 6$ fail on row-permuted complex Hadamard matrices whose first row is not all ones.
- **Next test needed**: In any formulation deploying the 24 balance identities, ensure that the row permutation of the second and third bases is explicitly tracked or fixed.

## Caveats
Column permutations and column phase multiplications of $B$ can be absorbed, but row permutations of $H$ change the first row and destroy the identity $\sum_k W_{jk} = 6$.
