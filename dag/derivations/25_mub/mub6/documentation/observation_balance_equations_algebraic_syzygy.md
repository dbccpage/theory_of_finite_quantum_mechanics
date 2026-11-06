# Algebraic Syzygy Status and Preconditioner Norm Inflation of Balance Equations

Type: observation
Confidence: high
Source: Candidates L01_N10, L01_N04, L01_N06, L00_N28
Relevant to: Route A balance filtering, rectangular Krawczyk preconditioning, variety codimension

## Statement
The 24 linear balance equations:
$$\sum_{k=0}^5 W_{jk} = 6, \quad \sum_{j=0}^5 W_{jk} = 6$$
are algebraic syzygies of row-1 gauge normalization and column unitarity ($V V^\dagger = 6 I_6$). They add zero codimension to the candidate variety, and appending them to rectangular Krawczyk preconditioning systems empirically increases the operator error norm $\|I - A J\|$ by $31.7\%$.

## Evidence
Let $V$ be a $6 \times 6$ matrix with $V_{0k} = 1$ for all $k \in \{0, \dots, 5\}$. The sum of entries in row $j$ satisfies:
$$\sum_{k=0}^5 V_{jk} = \sum_{k=0}^5 V_{0k}^* V_{jk} = (V V^\dagger)_{0j}$$
Under the unitarity condition $V V^\dagger = 6 I_6$, this product is $6 \delta_{0j}$, giving 6 for $j=0$ and 0 for $j > 0$. Similarly, for the transition matrix $W = V_C^\dagger D V_B$, row and column sums are constrained identically by the boundary conditions.
Empirical evaluation in candidate solvers shows that adding these 24 redundant equations expands the equation count to 440 without increasing the Jacobian rank, increasing the condition number of the normal equations and worsening interval error bounds.

## Implications
Retaining the balance equations does not improve chart separation or variety pruning, but instead degrades numerical conditioning in least-squares preconditioning. Efficient contractor formulations should eliminate balance equations and operate directly on independent coordinates.

## Caveats
The balance equations hold identically on the true candidate variety; the obstruction is purely one of algebraic redundancy and adverse impact on rectangular preconditioning condition numbers.
