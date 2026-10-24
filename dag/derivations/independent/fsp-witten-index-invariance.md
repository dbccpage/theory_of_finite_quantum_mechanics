# Independent Verification Companion: `FSP-WITTEN-INDEX-INVARIANCE` (`FERMION_SIGN`)

- **DAG Node**: `FSP-WITTEN-INDEX-INVARIANCE` (`TFQ-1206`, `FSP-DERIV-042`)
- **Title**: `Witten index beta-independence under exact supersymmetry`
- **Independent Checker**: `checks/independent/fsp-witten-index-invariance.py`
- **Lean 4 Module**: `lean4/CampaignFspWittenIndexInvariance.lean`
- **Claim Class**: `L4D`
- **AuthorityEffect**: `None`

## 1. Purpose and Disjoint Verification Architecture

`checks/independent/fsp-witten-index-invariance.py` provides an independent, standard-library-only (`itertools`, `fractions.Fraction`) arithmetic audit of `FSP-WITTEN-INDEX-INVARIANCE` (`TFQ-1206`) without invoking Lean 4 or importing project modules:

1. **Block Power Factorization & Supertrace Vanishing of Positive Powers $H(A, B)^{k+1}$ (`supertrace=690`)**:
   - Evaluates the block intertwining identity $(BA)^{k+1} = B (AB)^k A$, iso-spectral trace identity $\mathrm{Tr}((BA)^{k+1}) = \mathrm{Tr}((AB)^{k+1})$, and supertrace vanishing $\mathrm{Tr}(\Gamma_F H(A, B)^{k+1}) = 0$ across dimensions $(n_B, n_F) \in \{(1,1), (2,1), (1,2), (2,2), (3,2), (2,3)\}$, 6 exact rational block seeds, and powers $k = 0 \dots 4$.
   - Evaluates truncated Boltzmann polynomials $P_\beta(H) = I - \beta H + \frac{\beta^2}{2} H^2 - \frac{\beta^3}{6} H^3$ across $\beta \in \{0, 1/4, 1, 5/2\}$, confirming $\mathrm{Tr}(\Gamma_F P_\beta(H(A, B))) = n_B - n_F$ independent of $\beta$.
2. **Paired Positive-Energy Doublets, $\beta$-Independence of $W(\beta)$, & Forced Zero Modes (`spectral=256`)**:
   - Evaluates `wittenIndexPaired` across $(n_B^{(0)}, n_F^{(0)}) \in \{0 \dots 3\}^2$ and 4 positive-energy Boltzmann weight sets, confirming $W(\beta) = n_B^{(0)} - n_F^{(0)}$ and that $W(\beta) \ne 0 \implies n_B^{(0)} + n_F^{(0)} > 0$ (unbroken supersymmetry ground energy $E = 0$).
   - Evaluates 36 rectangular $(n_B, n_F) = (2, 1)$ supercharges $A = [[a, b]]$, verifying $\mathrm{Tr}(A^T A) = \mathrm{Tr}(A A^T) = a^2 + b^2$, exact annihilation of the bosonic zero mode $[-b, a]^T$, and positive eigenvalue $a^2 + b^2$ on $[a, b]^T$ ($W = 2 - 1 = 1$).
3. **Scope & Non-Equivalence Fences (`fences=225`)**:
   - Verifies that while $W(\beta)$ cancels excited doublets ($w_i - w_i = 0$), the thermal partition function $Z(\beta) = n_B^{(0)} + n_F^{(0)} + 2 \sum_i w_i$ strictly varies with $\beta$ and has average Monte Carlo sign ratio $|W(\beta)| / Z(\beta) < 1$ decaying as excited states contribute.
   - Verifies that when a lattice discretization introduces a fermionic shift $H_F = A B + \Delta$ with $\mathrm{Tr}(\Delta) \ne 0$, $\mathrm{Tr}(\Gamma_F H_{\mathrm{broken}}) = -\mathrm{Tr}(\Delta) \ne 0$, breaking $\beta$-independence.

## 2. Execution Summary

- **Command**: `python -I -X utf8 checks/independent/fsp-witten-index-invariance.py`
- **Output**: `checks=1171 supertrace=690 spectral=256 fences=225 failures=0`
- **Exit Code**: `0`

## 3. Claim Hygiene Summary

1. **What it supports**: Supports exact finite-dimensional verification of block power intertwining $(BA)^{k+1} = B(AB)^k A$, supertrace vanishing $\mathrm{Tr}(\Gamma_F H(A,B)^{k+1}) = 0$, $\beta$-independence of the Witten index $W(\beta) = n_B^{(0)} - n_F^{(0)}$ under exact supersymmetry, forced zero modes when $W \ne 0$, and explicit fences showing that $W(\beta)$ does not yield sign-free sampling of $Z(\beta)$ and presupposes an exact lattice supercharge.
2. **What it does not support**: Does not support sign-free Monte Carlo sampling of the thermal partition function $Z(\beta)$, continuum path-integral measure construction, or automatic preservation of full lattice supersymmetry when nonlinear Leibniz defects are present (`FSP-LATTICE-WESS-ZUMINO-SUSY`).
3. **Narrowest defensible claim**: On a finite $\mathbb{Z}_2$-graded space with $H = \{Q(A), Q^\dagger(B)\} = \mathrm{diag}(B A, A B)$, every positive power $H^{k+1}$ has zero supertrace and paired positive-energy doublets cancel in $W(\beta) = n_B^{(0)} - n_F^{(0)}$, while $Z(\beta)$ remains $\beta$-dependent and lattice SUSY breaking $\Delta$ destroys supertrace cancellation by $-\mathrm{Tr}(\Delta)$.
4. **Next test needed**: Proceed to the next highest-ranked non-`TFQ` node in `dag/pfp/campaign/derivation_queue.json` (`FSP-KITAEV-HONEYCOMB-SOLUTION`, Rank 25).
