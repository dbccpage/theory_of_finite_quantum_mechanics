# Constructive Lower Bound N(6) >= 3 via Kronecker Products

Type: theorem
Confidence: high
Source: Candidates strategy_L02_N02, strategy_L02_N03, strategy_L02_N04, strategy_L02_N06 (Level 2); Candidates strategy_L03_N00, strategy_L03_N01 (Level 3); Candidate strategy_L04_N00 (Level 4)
Relevant to: Unconditional verification of Target B constructive lower bound N(6) >= 3 for MUB(6).

## Statement
There exists a triplet of pairwise mutually unbiased orthonormal bases in the complex Hilbert space $\mathbb{C}^6$, establishing unconditionally that:
$$N(6) \ge 3.$$

## Proof
We realize $\mathbb{C}^6$ as the Hilbert space tensor product $\mathbb{C}^2 \otimes \mathbb{C}^3 \cong \mathbb{C}^6$.

1. **Dimension 2 Triplet**:
In $\mathbb{C}^2$, define three $2 \times 2$ unitary matrices:
$$A_0 = I_2 = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}, \quad A_1 = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}, \quad A_2 = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & 1 \\ i & -i \end{pmatrix}.$$
Each $A_r$ is unitary ($A_r^\dagger A_r = I_2$). For any distinct pair $r \ne s \in \{0, 1, 2\}$, direct evaluation confirms that every entry of the transition matrix $A_r^\dagger A_s$ satisfies:
$$|(A_r^\dagger A_s)_{jk}|^2 = \frac{1}{2} \qquad \forall j, k \in \{0, 1\}.$$

2. **Dimension 3 Triplet**:
In $\mathbb{C}^3$, let $\omega = e^{2\pi i / 3}$ denote the primitive cube root of unity ($1 + \omega + \omega^2 = 0$). Define three $3 \times 3$ unitary matrices:
$$C_0 = I_3, \quad C_1 = \frac{1}{\sqrt{3}} \begin{pmatrix} 1 & 1 & 1 \\ 1 & \omega & \omega^2 \\ 1 & \omega^2 & \omega \end{pmatrix}, \quad C_2 = \operatorname{diag}(1, \omega, \omega) C_1.$$
Each $C_r$ is unitary ($C_r^\dagger C_r = I_3$). Mutual unbiasedness is verified as follows:
- For $r = 0$ and $s \in \{1, 2\}$, entries of $C_s$ have modulus $1/\sqrt{3}$, so $|(C_0^\dagger C_s)_{jl}|^2 = 1/3$.
- For $r = 1, s = 2$, the cross-product is $(C_1^\dagger C_2)_{jl} = \frac{1}{3} \sum_{x=0}^2 \omega^{x^2 + (l-j)x}$. For $l - j \equiv 0 \pmod 3$, the sum is $\frac{1}{3}(1 + 2\omega)$, with squared modulus $\frac{1}{9}|1 + 2\omega|^2 = \frac{1}{9}(3) = \frac{1}{3}$. For $l - j \in \{1, 2\} \pmod 3$, the sum is $\frac{1}{3}(2 + \omega^2)$, with squared modulus $\frac{1}{9}|2 + \omega^2|^2 = \frac{1}{9}(3) = \frac{1}{3}$.
Thus, for all $r \ne s \in \{0, 1, 2\}$, every entry satisfies $|(C_r^\dagger C_s)_{jl}|^2 = 1/3$.

3. **Composite Kronecker Product Construction**:
Define three $6 \times 6$ unitary matrices by the Kronecker product:
$$U_r = A_r \otimes C_r \in \mathbb{C}^{6 \times 6} \qquad (r \in \{0, 1, 2\}).$$
Unitarity is preserved by the Kronecker product: $U_r^\dagger U_r = (A_r^\dagger A_r) \otimes (C_r^\dagger C_r) = I_2 \otimes I_3 = I_6$.
For any distinct pair $r \ne s \in \{0, 1, 2\}$, the transition matrix factors as:
$$U_r^\dagger U_s = (A_r^\dagger A_s) \otimes (C_r^\dagger C_s).$$
Indexing rows by $(j, l)$ and columns by $(k, m)$ with $j, k \in \{0, 1\}$ and $l, m \in \{0, 1, 2\}$, every entry of $U_r^\dagger U_s$ satisfies:
$$|(U_r^\dagger U_s)_{(j,l), (k,m)}|^2 = |(A_r^\dagger A_s)_{jk}|^2 \cdot |(C_r^\dagger C_s)_{lm}|^2 = \frac{1}{2} \cdot \frac{1}{3} = \frac{1}{6}.$$
Therefore, the columns of $U_0, U_1, U_2$ form three pairwise mutually unbiased orthonormal bases in $\mathbb{C}^6$.

## Hypotheses / Conditions
None. This is an explicit, unconditional algebraic construction in standard Hilbert space $\mathbb{C}^6$.

## How It Applies
This result provides the exact mathematical justification for Target B's baseline lower bound $N(6) \ge 3$. To settle the maximum cardinality $N(6)$, research focuses on determining whether an additional fourth basis $U_3$ can exist (Target A: $N(6) = 3$ vs Target B: $N(6) \ge 4$).

## Caveats
- **What it supports**: Unconditionally supports $N(6) \ge 3$ in $\mathbb{C}^6$.
- **What it does not support**: Does not support existence or non-existence of a fourth basis ($N(6) \ge 4$ or $N(6) = 3$).
