# Positive Semidefiniteness and Spectrum of the 24x24 MUB Quartet Projector Gram Matrix

Type: theorem
Confidence: high
Source: Candidate strategy_L01_N00 (Level 1); Candidate strategy_L03_N04 (Level 3); Candidate strategy_L04_N00 (Level 4)
Relevant to: Linear operator bounds, Welch frame bounds, and explaining why degree-2 polynomial/linear operator methods cannot detect the non-existence of 4 MUBs in C^6.

## Statement
Let $\{U_0, U_1, U_2, U_3\}$ be an ideal quartet of mutually unbiased orthonormal bases in $\mathbb{C}^6$. Let $P_{a, i} = u_{a, i} u_{a, i}^\dagger$ denote the 24 rank-1 projection operators ($a \in \{0, 1, 2, 3\}$, $i \in \{0, \dots, 5\}$).
The $24 \times 24$ Projector Gram matrix $\mathcal{G} \in \mathbb{C}^{24 \times 24}$ with entries:
$$\mathcal{G}_{(a,i), (b,j)} = \operatorname{Tr}(P_{a,i} P_{b,j}) = |\langle u_{a,i}, u_{b,j} \rangle|^2$$
(where $\mathcal{G}_{(a,i), (a,j)} = \delta_{ij}$ and $\mathcal{G}_{(a,i), (b,j)} = 1/6$ for $a \ne b$) is positive semidefinite with rank 21 and spectrum:
$$\operatorname{spec}(\mathcal{G}) = \{ 4 \text{ (multiplicity 1)}, \; 1 \text{ (multiplicity 20)}, \; 0 \text{ (multiplicity 3)} \}.$$

## Proof
The matrix $\mathcal{G}$ can be expressed in Kronecker block form as:
$$\mathcal{G} = I_4 \otimes I_6 + \frac{1}{6} (J_4 - I_4) \otimes J_6,$$
where $J_n$ denotes the $n \times n$ all-ones matrix.
The eigenvalues of $J_4$ are $4$ (multiplicity 1) and $0$ (multiplicity 3), so $J_4 - I_4$ has eigenvalues:
- $\lambda_1 = 3$ (multiplicity 1, eigenvector $\mathbf{1}_4$),
- $\lambda_2 = -1$ (multiplicity 3, orthogonal to $\mathbf{1}_4$).

The eigenvalues of $J_6$ are $6$ (multiplicity 1, eigenvector $\mathbf{1}_6$) and $0$ (multiplicity 5).
Taking the Kronecker sum/product eigenvalues:
1. For the common all-ones eigenvector $\mathbf{1}_4 \otimes \mathbf{1}_6$:
   $$1 + \frac{1}{6} (3)(6) = 1 + 3 = 4 \quad (\text{multiplicity } 1 \times 1 = 1).$$
2. For eigenvectors in $\mathbb{C}^4 \otimes \ker(J_6)$:
   $$1 + \frac{1}{6} (\lambda)(0) = 1 \quad (\text{multiplicity } 4 \times 5 = 20).$$
3. For eigenvectors in $(\ker(J_4 - I_4 - 3 I_4))^\perp \otimes \mathbf{1}_6$:
   $$1 + \frac{1}{6} (-1)(6) = 1 - 1 = 0 \quad (\text{multiplicity } 3 \times 1 = 3).$$

All eigenvalues are non-negative ($4 \ge 0, 1 \ge 0, 0 \ge 0$), so $\mathcal{G} \succeq 0$. The rank is $\operatorname{rank}(\mathcal{G}) = 1 + 20 = 21 \le 36$.

## Hypotheses / Conditions
1. Dimension $d = 6$, number of bases $m = 4$.
2. Pairwise transition probabilities satisfy $|\langle u_{a,i}, u_{b,j} \rangle|^2 = 1/6$ for $a \ne b$, and $\langle u_{a,i}, u_{a,j} \rangle = \delta_{ij}$.

## How It Applies
This result provides an exact structural explanation for why linear operator methods fail:
- Because $\mathcal{G} \succeq 0$, all pairwise linear operator inequalities, frame potentials, and Welch bounds are identically satisfied by the ideal 4-MUB rank-1 projector system in $\mathbb{C}^6$.
- Consequently, linear operator methods and degree-2 polynomial bounds cannot detect the dimension-6 obstruction.
- The obstruction to 4 MUBs in $\mathbb{C}^6$ enters strictly at degree 4 or higher in the polynomial algebra, where candidate basis unitarity $B^\dagger B = 6 I_6$ couples with mutual unbiasedness cross-terms.

## Caveats
This theorem describes the ideal Gram matrix of rank-1 projectors. It shows the limitation of unconstrained linear operator relaxations; it does not rule out higher-order algebraic obstructions.
