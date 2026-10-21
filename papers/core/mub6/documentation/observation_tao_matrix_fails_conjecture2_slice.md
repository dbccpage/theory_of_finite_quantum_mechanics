# Tao Matrix Obstruction to Conjecture 2 Hadamard Slice Reduction

Type: observation
Confidence: high
Source: Candidate strategy_L00_N01 (Level 0 falser report), strategy_L00_N07
Relevant to: Auditing Route B (Hadamard cube slice Laurent parity transport) and global classification bridges to N(6) = 3.

## Statement
The order-6 Tao complex Hadamard matrix $S_6$ (whose entries belong strictly to the 3rd roots of unity $\{1, \omega, \omega^2\}$ with $\omega = e^{2\pi i / 3}$) cannot have any entry equal to $-1$ under any row or column dephasing. Furthermore, its Laurent cubic invariant sum evaluates to a norm of 9 rather than 0. Consequently, $S_6$ violates the three $-1$ rows condition and fails Conjecture 2 of Matolcsi et al. (2025).

## Evidence
1. Entry phase group: The entries of $S_6$ are powers of $\omega$. Multiplying rows or columns by unit phases to dephase the first row and column leaves all entries in $\mathbb{Z}_3$ phases; no phase rotation can produce $-1$ since $-1 = e^{i \pi} \notin \{1, \omega, \omega^2\}$.
2. Algebraic calculation: The 20-permutation action on cubic Laurent monomial sums $G_H(\pi(\gamma_2))$ evaluated on $S_6$ yields a non-zero residual of norm 9.
3. Code probe executed in `strategy_L00_N01_falser`: verified exact phase group closure and non-zero Laurent sum in Python.

## Implications
- What it supports: Supports that $S_6$ cannot arise as a Hadamard cube slice with three $-1$ rows under Conjecture 2.
- What it does not support: Does not support that $S_6$ can participate in a MUB quartet; $S_6$ is an isolated matrix known not to extend to a quartet by discrete searches.
- Narrowest defensible claim: Route B's Laurent parity transport cannot bridge local family exclusions to $N(6) = 3$ without an independent theorem excluding $S_6$ from MUB triads.
- Next test needed: Check whether $S_6$ can be excluded from MUB triads via exact rational polynomial ideals in low dimension.

## Caveats
This obstruction targets the general transport bridge (Route B). It does not imply that $S_6$ extends to 4 MUBs; it demonstrates that Conjecture 2 cannot be assumed for general complex Hadamard matrices without an independent classification.
