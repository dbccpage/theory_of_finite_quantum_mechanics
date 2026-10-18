# Laurent Monomial Vanishing and MUB Conjectures (Matolcsi et al. 2025)

Type: reference
Confidence: medium
Source: Candidates strategy_L00_N01, strategy_L00_N05, strategy_L00_N07, strategy_L00_N16, strategy_L00_N19, strategy_L00_N21, strategy_L00_N22 (Level 0)
Relevant to: Auditing Route B (Conjecture 2 and Proposition 4.2 transport) and the formulation of Conjecture 3.

## Bibliographic Info
- Authors: Maté Matolcsi, Dániel Matszangosz, Péter E. Varga, Mihály Weiner
- Title: On the maximum number of mutually unbiased bases in dimension 6
- Year: 2025
- ArXiv/DOI: arXiv:2503.14752
- Theorem/Lemma Number: Conjecture 2, Proposition 4.2, Conjecture 3
- Verified via web search: yes

## Key Result
1. **Conjecture 2(a) and 2(b)**: Proposes that Laurent monomial sums $G_H(\pi(\gamma_1))$ and $G_H(\pi(\gamma_2)) G_{H^*}(\pi(\gamma_2))$ vanish across all 20 permutations $\pi \in S_6$ of sign vectors $\gamma_1 = (1,1,1,-1,-1,-1)$ and $\gamma_2 = (3,3,3,-3,-3,-3)$ for any complex Hadamard matrix $H$ appearing in an MUB triplet.
   - Proved algebraically for all qubit $\otimes$ qutrit tensor product transitions $U(\phi) \otimes V$ due to odd block exponent parity $\alpha_n = n(2m-3) \in \{-9, -3, 3, 9\}$ forcing $1 + (-1)^{\alpha_n} = 0$.
   - Proved algebraically for all two-circulant block matrices $B_6(\theta)$ due to circulant multiset cancellation between left and right blocks.
2. **Proposition 4.2**: Asserts that any transition matrix in a putative MUB triplet must contain at least three rows of $-1$ and is equivalent to a member of $F_6(x, y) \cup B_6(\theta)$.
3. **Conjecture 3**: Asserts that no quartet of mutually unbiased bases in $\mathbb{C}^6$ contains a member of the Szöllősi two-circulant family $B_6(\theta)$.

## Hypotheses / Conditions
1. Order $d = 6$ complex Hadamard matrices.
2. Transition matrices between MUB bases.

## How It Applies
This paper forms the theoretical backbone for Route B and Route A:
- What it supports: Supports framing Conjecture 3 as the central remaining continuous obstacle to $N(6) = 3$, and establishes algebraic parity cancellation on tensor products and two-circulants.
- What it does not support: Does not establish Conjecture 2 for arbitrary abstract MUB triplet faces (the Gram equations do not algebraically imply Laurent functional vanishing); does not prove Proposition 4.2 for general complex matrices (Mann's theorem does not apply to continuous phases on $\mathbb{T}$).
- Narrowest defensible claim: If Conjecture 2 holds, any MUB triad transition matrix belongs to $F(x,y) \cup B_6(\theta) \cup \{H_6\}$.
- Next test needed: Mechanize the deduction from 20-permutation cancellation to three $-1$ rows in Lean 4 without custom axioms.

## Caveats
1. Conjecture 2 is unproved for general complex matrices and is contradicted by the Tao matrix $S_6$ (norm 9, zero $-1$ entries).
2. The deduction of Proposition 4.2 via Mann's theorem fails on continuous circle phases, where 6-bar equilateral linkages admit continuous zero-sums with zero opposite pairs and zero triangles.
3. Dephased Haagerup matrix $H_6$ satisfies $G_{H_6} = 0$ on all 20 permutations and has 5 distinct rows with $-1$, surviving the 3-row filter.
