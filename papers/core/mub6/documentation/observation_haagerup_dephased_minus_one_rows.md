# Haagerup Complex Hadamard Matrix Dephased Row Sign Multiplicity

Type: observation
Confidence: high
Source: Candidate strategy_L00_N22 (Level 0)
Relevant to: Auditing Proposition 4.2 moduli classification filters and row-count exclusion criteria for MUB triplets

## Statement
In any dephased representation of the order-6 Haagerup complex Hadamard matrix $H_6$ (where row $r_0$ and column $c_0$ are dephased to all-ones for any choice of base cell $(r_0, c_0) \in \{0, \dots, 5\}^2$), the dephased matrix contains entries equal to $-1$ in exactly 5 distinct rows. Consequently, the Haagerup matrix cannot be excluded by the criterion of containing strictly fewer than 3 rows with entry $-1$.

## Evidence
The Haagerup matrix $H_6$ can be represented in two-circulant block form:
$$H_6 = \begin{pmatrix} A & B \\ B^\dagger & -A^\dagger \end{pmatrix},$$
where $A = \operatorname{circ}(1, 1, i)$ and $B = \operatorname{circ}(1, 1, -1)$.
Numerical and symbolic enumeration across all 36 choices of base cell $(r_0, c_0) \in \{0, \dots, 5\}^2$ performed during the adversarial audit of Candidate 22 verified that:
1. Every dephased representation has exactly 5 distinct rows containing at least one entry equal to $-1$.
2. Because $H_6$ is a two-circulant block matrix, it satisfies the Laurent cubic monomial parity identity $G_{H_6}(\pi(\gamma_1)) = 0$ identically across all 20 permutations $\pi \in S_6$.

## Implications
1. The heuristic premise that Haagerup $H_6$ has at most 1 row with entry $-1$ (which was encoded in some preliminary classification tables) is factually incorrect.
2. Filtering candidate transition matrices by requiring $\ge 3$ rows containing $-1$ does not exclude Haagerup $H_6$.
3. Excluding $H_6$ from participating in a MUB quartet requires dedicated orbit-level algebraic obstruction analysis (e.g. non-extendibility of $H_6$ to 4 MUBs) rather than row-count filtering.

## Claim Hygiene Summary
- **What it supports**: Supports that all 36 dephasings of Haagerup $H_6$ contain entries of $-1$ in 5 distinct rows, and that $H_6$ satisfies $G_{H_6}(\pi(\gamma_1)) = 0$.
- **What it does not support**: Does not support that Haagerup $H_6$ can be extended to 4 MUBs; independent literature results indicate that $H_6$ cannot extend to a quartet.
- **Narrowest defensible claim**: The Haagerup matrix $H_6$ in any dephased form has 5 distinct rows containing $-1$.
- **Next test needed**: Verify formal Lean 4 theorem excluding quartet extensions containing the isolated Haagerup matrix $H_6$.
