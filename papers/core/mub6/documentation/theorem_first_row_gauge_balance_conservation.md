# First-Row Column Gauge and Transition Balance Conservation

Type: theorem
Confidence: high
Source: Candidates strategy_L00_N00, strategy_L00_N01, strategy_L00_N04, strategy_L00_N05, strategy_L00_N07 (Level 0)
Relevant to: Reducing candidate basis search fibers and enforcing row/column sum constraints on transition matrices between column-gauged bases.

## Statement
Let $U, V \in \mathbb{C}^{6 \times 6}$ be two complex matrices satisfying $U^\dagger U = 6 I_6$ and $V^\dagger V = 6 I_6$, both normalized in the first-row column gauge:
$$(U)_{0j} = 1 \quad \text{and} \quad (V)_{0j} = 1 \qquad \text{for all } j \in \{0, \dots, 5\}.$$
Define the transition product matrix $W = U^\dagger V$. Then every row sum and every column sum of $W$ equals 6:
$$\sum_{j=0}^5 W_{ij} = 6 \quad \forall i \in \{0, \dots, 5\}, \qquad \sum_{i=0}^5 W_{ij} = 6 \quad \forall j \in \{0, \dots, 5\}.$$
Equivalently, in real and imaginary parts:
$$\sum_{j=0}^5 \operatorname{Re}(W_{ij}) = 6, \quad \sum_{j=0}^5 \operatorname{Im}(W_{ij}) = 0 \quad \forall i,$$
$$\sum_{i=0}^5 \operatorname{Re}(W_{ij}) = 6, \quad \sum_{i=0}^5 \operatorname{Im}(W_{ij}) = 0 \quad \forall j.$$

## Proof
Because $V$ is a finite square matrix over $\mathbb{C}$, the left isometry $V^\dagger V = 6 I_6$ implies the two-sided isometry $V V^\dagger = 6 I_6$.
Computing entry $(k, 0)$ of $V V^\dagger$:
$$(V V^\dagger)_{k0} = \sum_{j=0}^5 V_{kj} \overline{V_{0j}} = \sum_{j=0}^5 V_{kj} \cdot 1 = \sum_{j=0}^5 V_{kj}.$$
On the other hand, $V V^\dagger = 6 I_6$ implies $(V V^\dagger)_{k0} = 6 \delta_{k0}$. Thus:
$$\sum_{j=0}^5 V_{kj} = 6 \delta_{k0}.$$
Now evaluate the row sum of $W = U^\dagger V$ along row $i$:
$$\sum_{j=0}^5 W_{ij} = \sum_{j=0}^5 \sum_{k=0}^5 \overline{U_{ki}} V_{kj} = \sum_{k=0}^5 \overline{U_{ki}} \left(\sum_{j=0}^5 V_{kj}\right) = \sum_{k=0}^5 \overline{U_{ki}} (6 \delta_{k0}) = 6 \overline{U_{0i}}.$$
Since $U_{0i} = 1$ by the column gauge, we obtain $6 \cdot 1 = 6$.
By identical reasoning on the conjugate transpose $W^\dagger = V^\dagger U$, each column sum of $W$ evaluates to $6$.

## Hypotheses / Conditions
1. Both matrices $U$ and $V$ must satisfy isometric scaling $U^\dagger U = 6 I_6$ and $V^\dagger V = 6 I_6$.
2. Both matrices must be phased so that their first rows consist entirely of ones: $(U)_{0j} = 1$ and $(V)_{0j} = 1$ for all $j \in \{0, \dots, 5\}$.

## How It Applies
In the 440-coordinate formulation of candidate quartets extending a complex Hadamard matrix, candidate bases $U_2$ and $U_3$ can be column-rephased to have first rows equal to 1. This theorem derives 24 exact linear equations on the transition matrix $P_2 = H_1^\dagger H_2$, reducing the candidate solution variety.
- What it supports: Supports 24 exact linear balance relations on transition coordinates in column-gauged systems.
- What it does not support: Does not by itself exclude candidate quartets on boxes where the sum of transition real parts is consistent with 6.
- Narrowest defensible claim: Any pair of complex matrices satisfying $U^\dagger U = 6 I_6$, $V^\dagger V = 6 I_6$, and top row equal to 1 has transition row and column sums equal to 6.
- Next test needed: Test whether coupling these balance identities with higher-order polynomial constraints eliminates candidate leaves away from the symmetric slice.

## Caveats
The balance equations hold identically for all column-gauged pairs and thus cannot separate candidate boxes intersecting the feasible hyperplane $\sum_{j=0}^5 \operatorname{Re}(W_{0j}) = 6$. Lean formalization exists in `SzollosiGaugeBalance.lean` (`transition_row_sum`, `transition_column_sum`).
