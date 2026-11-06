# Brierley-Weigert MUB Extension Ceilings for Dimension Six

Type: reference
Confidence: high
Source: Aggregator Nodes strategy_L02_N01, strategy_L02_N03, strategy_L02_N07 (Level 2); Candidate strategy_L04_N00 (Level 4)
Relevant to: MUB extension ceilings, Hadamard equivalence classes, isolating candidate Hadamard matrices that could admit 4 or more MUBs

## Bibliographic Info
- Authors: Stephen Brierley, Stefan Weigert (2010); Dardo Goyeneche et al. (2014)
- Title: Maximal sets of mutually unbiased quantum states in dimension six
- Year: 2010 (Brierley & Weigert); 2014 (Goyeneche et al.)
- Journal: Physical Review A, 81(5), 052327 (2010); Physical Review A, 89, 012301 (2014)
- ArXiv/DOI: arXiv:0909.4484 [quant-ph] / doi:10.1103/PhysRevA.81.052327; arXiv:1309.4324
- Verified via web search: yes

## Key Result
Brierley and Weigert investigated whether known complex Hadamard matrices in dimension 6 can belong to maximal sets of mutually unbiased bases (with independent confirmation of Haagerup ceilings by Goyeneche et al. 2014):
1. **Tao Matrix ($S_6$)**: The isolated Fourier matrix on $\mathbb{Z}_2 \times \mathbb{Z}_3$, $S_6$, belongs to a maximal set of at most 2 MUBs. That is, no third basis exists mutually unbiased to both the standard basis $I$ and $S_6$.
2. **Haagerup Matrix ($H_6$)**: Any set of MUBs containing the Haagerup matrix $H_6$ (and the identity $I$) can be extended to at most 3 MUBs. That is, a triplet $\{I, H_6, B\}$ exists, but cannot be extended to 4 MUBs.
3. **General Consequence**: Any hypothetical system of 4 or more MUBs in dimension 6 cannot contain the Tao matrix $S_6$ or the Haagerup matrix $H_6$. A 4-MUB system must therefore arise from candidates in other equivalence classes (such as the two-circulant family $B_6(\theta)$ or non-equivalent components).

## Hypotheses / Conditions
- Dimension $d = 6$.
- Unbiasedness defined by $|\langle \psi_j | \phi_k \rangle|^2 = 1/6$ for all basis vectors across different bases.
- Matrices $S_6$ and $H_6$ are evaluated up to standard Hadamard equivalence (row/column permutations and diagonal phase shifts).

## How It Applies
- Restricts the search space for $N(6) \ge 4$: eliminates $S_6$ and $H_6$ as candidate seeds for 4-MUB systems.
- Confirms why attempts to build 4 MUBs starting from the Tao matrix or Haagerup matrix inevitably stall at 2 or 3 MUBs.
- Directs search efforts toward the one-parameter two-circulant family $B_6(\theta)$ or other orbits.

## Caveats
- The result establishes ceilings for specific known complex Hadamard matrices; it does not rule out the existence of 4 MUBs constructed from other families of Hadamard matrices (such as $B_6(\theta)$ for specific $\theta$).
