# Two-Circulant Parity Pairing and Laurent Monomial Cancellation

Type: theorem
Confidence: high
Source: Candidates strategy_L02_N04, strategy_L02_N06 (Level 2)
Relevant to: Evaluation of Matolcsi-Weiner Conjecture 2 on two-circulant Hadamard families B_6(theta) and Haagerup H_6.

## Statement
Let $A = \operatorname{circ}(1, b, c)$ and $B = \operatorname{circ}(1, e, f)$ be $3 \times 3$ circulant matrices with unimodular entries ($|b|=|c|=|e|=|f|=1$). Let:
$$H = \begin{pmatrix} A & B \\ B^\dagger & -A^\dagger \end{pmatrix} \in \mathbb{C}^{6 \times 6}.$$
Then for both the linear balanced sign vector $\gamma_1 = (1, 1, 1, -1, -1, -1)$ and the cubic balanced sign vector $\gamma_2 = (3, 3, 3, -3, -3, -3)$, the column Laurent monomial sum:
$$F_s(H) = \sum_{c=0}^5 \prod_{r=0}^5 H_{rc}^{s_r}$$
vanishes identically across all $\binom{6}{3} = 20$ permutations $\pi \in S_6$, forcing:
$$G_H(\pi(\gamma_1)) = |F_{\pi(\gamma_1)}(H)|^2 = 0 \quad \text{and} \quad G_H(\pi(\gamma_2)) = |F_{\pi(\gamma_2)}(H)|^2 = 0.$$

## Proof
Let $s = \pi(\gamma_n) \in \{+n, -n\}^6$ with $n \in \{1, 3\}$, where $\sum_{r=0}^5 s_r = 0$.
The column sum splits across the two $3 \times 3$ blocks:
$$F_s(H) = \sum_{j=0}^2 P_j(s) + \sum_{j=0}^2 P_{3+j}(s),$$
where $P_c(s) = \prod_{r=0}^5 H_{rc}^{s_r}$.

1. **Minus Sign Extraction**:
For columns in the right block $c = 3 + j$ ($j \in \{0, 1, 2\}$):
- For row indices $k \in \{0, 1, 2\}$, $H_{k, 3+j} = B_{kj}$.
- For row indices $3+k \in \{3, 4, 5\}$, $H_{3+k, 3+j} = -(A^\dagger)_{kj} = -\overline{A_{jk}}$.
Factoring the $-1$ signs out of the bottom-right block yields:
$$P_{3+j}(s) = \left( \prod_{k=0}^2 (-1)^{s_{3+k}} \right) \cdot \left( \prod_{k=0}^2 B_{kj}^{s_k} \right) \cdot \left( \prod_{k=0}^2 (A^\dagger)_{kj}^{s_{3+k}} \right).$$

2. **Exponent Parity**:
Let $m \in \{0, 1, 2, 3\}$ denote the number of $+n$ signs in the first block $\{0, 1, 2\}$.
Then exactly $3 - m$ signs equal $-n$ in the first block, so the second block contains $3 - m$ entries of $+n$ and $m$ entries of $-n$.
The sum of exponents in the second block is:
$$\beta_n = \sum_{k=0}^2 s_{3+k} = (3 - m)(+n) + m(-n) = n(3 - 2m) = -n(2m - 3).$$
Since $n \in \{1, 3\}$ is odd and $2m - 3$ is odd for all $m \in \{0, 1, 2, 3\}$, $\beta_n$ is strictly an odd integer.
Therefore:
$$\prod_{k=0}^2 (-1)^{s_{3+k}} = (-1)^{\beta_n} = -1 \qquad \forall \pi \in S_6.$$

3. **Circulant Shift Symmetry**:
Because $A$ and $B$ are circulant matrices, cyclic shifts of rows correspond to cyclic shifts of columns. Across the three columns $j \in \{0, 1, 2\}$, the multiset of column products in the right block matches the multiset of column products in the left block up to a cyclic permutation $\sigma \in S_3$.
Therefore:
$$P_{3+j}(s) = - P_{\sigma(j)}(s).$$
Summing across all three columns of the right block:
$$\sum_{j=0}^2 P_{3+j}(s) = - \sum_{j=0}^2 P_{\sigma(j)}(s) = - \sum_{j=0}^2 P_j(s).$$
Adding the left and right blocks gives:
$$F_s(H) = \sum_{j=0}^2 P_j(s) + \sum_{j=0}^2 P_{3+j}(s) = \sum_{j=0}^2 P_j(s) - \sum_{j=0}^2 P_j(s) = 0.$$
Taking squared modulus establishes $G_H(\pi(\gamma_n)) = 0$ for all 20 permutations $\pi \in S_6$.

## Hypotheses / Conditions
1. $H$ must have the two-circulant block form $\begin{pmatrix} A & B \\ B^\dagger & -A^\dagger \end{pmatrix}$.
2. Blocks $A$ and $B$ must be $3 \times 3$ circulant matrices with unimodular entries.
3. The sign vector $s$ must have three components $+n$ and three components $-n$ for odd integer $n \in \{1, 3\}$.

## How It Applies
This theorem establishes that all members of the continuous Szöllősi family $B_6(\theta)$ and the isolated Haagerup complex Hadamard matrix $H_6$ satisfy the Matolcsi-Weiner Conjecture 2 parity vanishing conditions identically with zero residual across all 20 permutations.

## Caveats
- **What it supports**: Supports that all 2-circulant matrices (including $B_6(\theta)$ and $H_6$) evaluate to $G_H = 0$ on all 20 permutations.
- **What it does not support**: Does not support that $G_H = 0$ confines complex Hadamard matrices to $F_6(x, y) \cup B_6(\theta)$; in particular, the isolated Haagerup matrix $H_6$ is a two-circulant that satisfies $G_H = 0$ while lying strictly outside $F_6(x, y) \cup B_6(\theta)$.
