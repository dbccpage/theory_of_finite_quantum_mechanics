# Karlsson Affine Family Minus-One Row Multiplicity and Invariant Vanishing

Type: observation
Confidence: high
Source: Candidates strategy_L00_N29, strategy_L00_N31 (Level 0 falser reports)
Relevant to: Auditing Proposition 4.2 moduli classification filters, row-count reduction criteria, and Lean table assumptions for MUB(6)

## Statement
In the displayed 2-parameter affine parametrization of the Karlsson complex Hadamard family $A_6(x, y)$ (for arbitrary continuous parameters $x, y \in \mathbb{T}$):
1. In column 1, entries in rows 1, 3, and 5 are identically equal to $-1$, giving at least 3 distinct rows containing $-1$ without requiring any parameter collapse (such as $y = x$).
2. The matrix satisfies the Laurent cubic and linear monomial vanishing conditions $G_{A_6}(\pi(\gamma_1)) = 0$ and $G_{A_6}(\pi(\gamma_2)) \cdot G_{A_6^*}(\pi(\gamma_2)) = 0$ identically across all 20 permutations $\pi \in S_6$.

Consequently, the Karlsson family evades exclusion by the proposed 3-row minus-one filter, refuting the claim that Conjecture 2 plus a 3-row criterion restricts candidate transitions strictly to $F(x, y) \cup B_6(\theta)$.

## Evidence
1. Symbolic matrix evaluation of the affine Karlsson ansatz $A_6(x, y)$ in SymPy and NumPy demonstrates that entries $(1, 1)$, $(3, 1)$, and $(5, 1)$ equal $-1$ identically for all $x, y \in \mathbb{T}$.
2. Evaluation of the column Laurent functional on $A_6(x, y)$ across all 20 permutations from $S_6$ yields maximum residual $< 10^{-15}$ (machine epsilon zero) for both $\gamma_1$ and $\gamma_2$.
3. Inspection of `Conjecture2GeneralMechanization.lean` revealed that the Lean file hardcoded `minMinusOneRows .KarlssonGeneric = 2` as a lookup table entry, which is refuted by the explicit matrix implementation in `MasterClassification.lean`.

## Implications
1. The premise that generic Karlsson matrices have only 2 rows with $-1$ (and only reach 3 rows by collapsing to Fourier-Diță $F(x, x)$) is refuted for the displayed affine ansatz.
2. Proposition 4.2 cannot reduce candidate MUB transitions to $F(x, y) \cup B_6(\theta)$ solely via the 3-row $-1$ criterion.
3. To exclude the 2-parameter Karlsson family from candidate MUB quartets, an independent obstruction (such as non-extendibility of $A_6(x, y)$ to four bases) is required.

## Claim Hygiene Summary
- **What it supports**: Supports that the affine Karlsson ansatz $A_6(x, y)$ has 3 distinct rows containing $-1$ for all $x, y \in \mathbb{T}$ and satisfies the 20-permutation Conjecture 2 vanishing identity.
- **What it does not support**: Does not support that $A_6(x, y)$ can be extended to an MUB quartet; independent geometric investigations suggest Karlsson matrices cannot complete to four bases.
- **Narrowest defensible claim**: The displayed affine Karlsson matrix $A_6(x, y)$ has entries equal to $-1$ in rows 1, 3, and 5 for all parameters $x, y \in \mathbb{T}$ and satisfies $G_{A_6}(\pi(\gamma_1)) = 0$ across all 20 permutations.
- **Next test needed**: Check whether an explicit polynomial refutation or certified vector exhaustion can exclude MUB quartets containing $A_6(x, y)$.
