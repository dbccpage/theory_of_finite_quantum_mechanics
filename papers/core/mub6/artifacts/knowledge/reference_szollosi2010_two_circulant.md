# Szöllősi Two-Circulant Complex Hadamard Matrix Construction (Szöllősi 2010)

Type: reference
Confidence: high
Source: Candidates strategy_L00_N00, strategy_L00_N01, strategy_L00_N04, strategy_L00_N05, strategy_L00_N07, strategy_L00_N16, strategy_L00_N17, strategy_L00_N20 (Level 0)
Relevant to: Parameterizing and analyzing the continuous non-affine family of order-6 complex Hadamard matrices and their MUB triplet extensions.

## Bibliographic Info
- Authors: Ferenc Szöllősi
- Title: Complex Hadamard matrices of order 6: a complete parametrization / A property of complex Hadamard matrices of order 6
- Year: 2010
- ArXiv/DOI: arXiv:0811.3930 / Proc. Roy. Soc. Edinburgh Sect. A 140 (2010), 1281-1288; Proc. Amer. Math. Soc. 138 (2010), 1177-1184
- Theorem/Lemma Number: PRSE Theorem 2.1; PAMS Theorem 1.1
- Verified via web search: yes

## Key Result
1. **Parametrization**: Constructs the continuous family of $6 \times 6$ complex Hadamard matrices of two-circulant type:
$$H_6^{(2)}(a,b) = \begin{pmatrix} A & B \\ B^\dagger & -A^\dagger \end{pmatrix},$$
where $A = \operatorname{circ}(1, x, xy)$ and $B = \operatorname{circ}(1, u, uv)$ are $3 \times 3$ circulant matrices with unit complex phases $(x, y, u, v) \in \mathbb{T}^4$ satisfying the compatibility condition:
$$\phi(x, y) + \phi(u, v) = 0, \qquad \text{where } \phi(z, w) = z + w + \overline{z w}.$$
2. **Triplet Extension Theorem (PAMS 2010 Thm 1.1)**: Every member of the continuous two-circulant family $B_6(\theta)$ can be extended to a triplet of mutually unbiased bases $\{I_6, B_6(\theta), C_6(\theta)\}$, where $C_6(\theta)$ is also a two-circulant complex Hadamard matrix.

## Hypotheses / Conditions
1. Order $d = 6$.
2. Phases satisfy $|x|=|y|=|u|=|v|=1$ and $\phi(x,y)+\phi(u,v)=0$.

## How It Applies
This family represents the primary continuous candidate family in dimension 6 targeted by Route A (Conjecture 3 of Matolcsi et al.).
- What it supports: Supports an explicit block circulant parameterization and establishes that MUB triplets exist for all members of the family.
- What it does not support: Does not establish that any member of the family can extend to 4 MUBs (Conjecture 3 asserts none can).
- Narrowest defensible claim: $H_6^{(2)}(a,b)$ forms a continuous family of CHMs of order 6, and every member extends to at least one MUB triplet.
- Next test needed: Certify real variety emptiness of candidate fourth bases across all phase parameter fibers.

## Caveats
The phase parameter space forms a deltoid with 3 singular boundary cusps where phase roots collide and Jacobians drop rank.
Because every member extends to a triplet, attempts to refute existence of a single additional basis unbiased to $B_6(\theta)$ are mathematically false; exclusion requires targeting the joint quartet constraints on pairs of additional bases $(U, V)$.
