# Qubit Odd-Parity Laurent Monomial Vanishing for Tensor-Product MUB Transitions

Type: theorem
Confidence: high
Source: Candidates strategy_L00_N29, strategy_L00_N30, strategy_L00_N31 (Level 0)
Relevant to: Analysis of Matolcsi-Weiner Conjecture 2 on tensor-product transitions and character sums on the Hadamard cube.

## Statement
Let $U(\phi) = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & 1 \\ e^{i\phi} & -e^{i\phi} \end{pmatrix}$ be any single-qubit mutually unbiased transition matrix with phase $\phi \in \mathbb{R}$, and let $V \in \mathbb{C}^{3 \times 3}$ be any entrywise-nonzero complex matrix. Let $H = U(\phi) \otimes V$ be the $6 \times 6$ Kronecker product matrix.
For any balanced ternary sign vector $s = \pi(\gamma_n) = (s_0, \dots, s_5) \in \{+n, -n\}^6$ with $n \in \{1, 3\}$, where $\pi \in S_6$ is an arbitrary permutation and $\sum_{r=0}^5 s_r = 0$ (so that exactly three components equal $+n$ and three equal $-n$), define the column Laurent monomial sum:
$$F_s(H) = \sum_{c=0}^5 \prod_{r=0}^5 H_{rc}^{s_r}.$$
Then $F_s(H) = 0$ identically across all $\binom{6}{3} = 20$ permutations $\pi \in S_6$, and consequently the quadratic functionals:
$$G_H(\pi(\gamma_1)) = |F_{\pi(\gamma_1)}(H)|^2 = 0 \quad \text{and} \quad G_H(\pi(\gamma_2)) \cdot G_{H^*}(\pi(\gamma_2)) = 0$$
vanish identically for all 20 permutations $\pi \in S_6$.

## Proof
Index rows and columns of $H$ by pairs $(i, j)$ and $(k, l)$ where $i, k \in \{0, 1\}$ are qubit indices and $j, l \in \{0, 1, 2\}$ are qutrit indices. The flat indices are $r = 3i + j$ and $c = 3k + l$ for $r, c \in \{0, \dots, 5\}$.
By the definition of the Kronecker product, the matrix entries factorize as:
$$H_{rc} = H_{(i,j),(k,l)} = U_{ik} V_{jl}.$$
The column Laurent monomial sum evaluates to:
$$F_s = \sum_{c=0}^5 \prod_{r=0}^5 H_{rc}^{s_r} = \sum_{k=0}^1 \sum_{l=0}^2 \prod_{i=0}^1 \prod_{j=0}^2 (U_{ik} V_{jl})^{s_{3i+j}}.$$
Separating the qubit factors $U_{0k}$ (block $i=0$, indices $r \in \{0, 1, 2\}$) and $U_{1k}$ (block $i=1$, indices $r \in \{3, 4, 5\}$):
$$F_s = \sum_{k=0}^1 \sum_{l=0}^2 U_{0k}^{s_0 + s_1 + s_2} U_{1k}^{s_3 + s_4 + s_5} \prod_{j=0}^2 V_{jl}^{s_j + s_{3+j}}.$$
Define the block exponent sums:
$$\alpha = s_0 + s_1 + s_2, \qquad \beta = s_3 + s_4 + s_5.$$
Because the sign vector $s$ has three $+n$ and three $-n$ entries, the total sum of all exponents vanishes:
$$\alpha + \beta = \sum_{r=0}^5 s_r = 3(+n) + 3(-n) = 0 \implies \beta = -\alpha.$$
For each qutrit column index $l \in \{0, 1, 2\}$, define the column weight:
$$W_l(s) = \prod_{j=0}^2 V_{jl}^{s_j + s_{3+j}}.$$
The weight $W_l(s)$ depends on $l$ and $s$, but does not depend on the qubit column index $k$.
Consequently, the double summation factors into a product of two independent sums:
$$F_s = \left( \sum_{k=0}^1 \left( \frac{U_{0k}}{U_{1k}} \right)^\alpha \right) \left( \sum_{l=0}^2 W_l(s) \right).$$
Evaluating the qubit column ratio for $U(\phi)$:
- For column $k=0$: $\frac{U_{00}}{U_{10}} = \frac{1/\sqrt{2}}{e^{i\phi}/\sqrt{2}} = e^{-i\phi}$.
- For column $k=1$: $\frac{U_{01}}{U_{11}} = \frac{1/\sqrt{2}}{-e^{i\phi}/\sqrt{2}} = -e^{-i\phi}$.
Substituting these ratios yields:
$$\sum_{k=0}^1 \left( \frac{U_{0k}}{U_{1k}} \right)^\alpha = (e^{-i\phi})^\alpha + (-e^{-i\phi})^\alpha = e^{-i\alpha\phi} (1 + (-1)^\alpha).$$
Now consider the arithmetic parity of the integer exponent $\alpha$.
Let $m \in \{0, 1, 2, 3\}$ denote the number of positive signs $+n$ that fall into the first block $\{0, 1, 2\}$.
Then exactly $3 - m$ negative signs $-n$ fall into the first block, so:
$$\alpha = m(+n) + (3 - m)(-n) = n(2m - 3).$$
Evaluating across all possible values $m \in \{0, 1, 2, 3\}$:
- For linear signs ($n = 1$): $\alpha_1 \in \{2(0)-3, 2(1)-3, 2(2)-3, 2(3)-3\} = \{-3, -1, 1, 3\}$.
- For cubic signs ($n = 3$): $\alpha_2 \in \{3(-3), 3(-1), 3(1), 3(3)\} = \{-9, -3, 3, 9\}$.
In every case, $2m - 3$ is an odd integer, and $n \in \{1, 3\}$ is odd, so the product $\alpha = n(2m - 3)$ is strictly an odd integer.
Therefore:
$$(-1)^\alpha = -1 \quad \forall m \in \{0, 1, 2, 3\}.$$
It follows that:
$$1 + (-1)^\alpha = 1 - 1 = 0.$$
Hence the qubit factor vanishes:
$$\sum_{k=0}^1 \left( \frac{U_{0k}}{U_{1k}} \right)^\alpha = e^{-i\alpha\phi} \cdot 0 = 0.$$
Therefore $F_s = 0$, which yields $G_H(\pi(\gamma_1)) = 0$ and $G_H(\pi(\gamma_2)) = 0$ for all 20 permutations $\pi \in S_6$. An identical computation on $H^*$ yields column ratios $1$ and $-1$, so $1^\alpha + (-1)^\alpha = 0$, confirming $G_{H^*}(\pi(\gamma_2)) = 0$.

## Hypotheses / Conditions
1. The matrix $H$ must possess a Kronecker product factorization $H = U(\phi) \otimes V$ with $U(\phi)$ having column phase ratios $e^{-i\phi}$ and $-e^{-i\phi}$.
2. The sign vector $s$ must partition into three $+n$ and three $-n$ entries for odd integer $n \in \{1, 3\}$.

## How It Applies
This result provides the exact algebraic mechanism behind Matolcsi-Weiner Conjecture 2 on all tensor-product candidate transitions. In Lean 4, this is mechanized in `Conjecture2GeneralMechanization.lean` under lemmas `alpha2_is_odd` and `qubit_parity_sum_zero`.

## Caveats
- **What it supports**: Supports that all $2 \times 3$ tensor-product transitions in $\mathbb{C}^6$ satisfy Conjecture 2 with zero residual.
- **What it does not support**: Does not support Conjecture 2 for general non-tensor complex Hadamard matrices. In particular, the isolated Tao matrix $S_6$ has non-tensor structure and yields $G_{S_6}(\gamma_1) = 9 \ne 0$.
- **Narrowest defensible claim**: For any $6 \times 6$ Kronecker product matrix $U(\phi) \otimes V$ with qubit MUB factor $U(\phi)$, the Laurent monomial functional $G_H(\pi(\gamma_n))$ vanishes identically across all 20 permutations of $\gamma_n$ for $n \in \{1, 3\}$.
- **Next test needed**: Check whether an algebraic derivation of Conjecture 2 can be established for non-tensor Hadamard cube slices from the 3-basis mutual unbiasedness ideal.
