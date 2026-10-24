Status: AI-drafted, awaiting human review.

# Independent Derivation Note: `ADS-HAPPY-TOY-NOT-DUALITY-GAP` (`TFQ-2212`)

AuthorityEffect: None.

## Target & Outcome Class

- **Campaign Node**: `ADS-HAPPY-TOY-NOT-DUALITY-GAP` (`TFQ-2212`, stage `ADS_CFT`)
- **Outcome Class**: **Narrowed** (node status remains `OPEN`)
- **Primary Literature**:
  - F. Pastawski, B. Yoshida, D. Harlow, and J. Preskill, *Holographic quantum error-correcting codes: Toy models for the bulk/boundary correspondence*, JHEP **06** (2015) 149 [arXiv:1503.06237]
  - P. Calabrese and J. Cardy, *Entanglement entropy and quantum field theory*, J. Stat. Mech. **0406** (2004) P06002 [arXiv:hep-th/0405152]
  - S. Ryu and T. Takayanagi, *Holographic Derivation of Entanglement Entropy from AdS/CFT*, Phys. Rev. Lett. **96** (2006) 181602 [arXiv:hep-th/0603001]
- **Verification Artifacts**:
  - Lean 4 module: `lean4/CampaignAdsHappyToyNotDualityGap.lean`
  - Standalone zero-import Python checker: `checks/independent/ads-happy-toy-not-duality-gap.py`
  - Receipts: `dag/research/campaign_ads-happy-toy-not-duality-gap_lean_replay.json`, `dag/research/campaign_ads-happy-toy-not-duality-gap_lean_mutation.json`, `dag/research/campaign_ads-happy-toy-not-duality-gap_independent.json`

---

## 1. Flat Stabilizer Rényi Spectrum vs. Continuum CFT Rényi Scaling

In any stabilizer state—including the boundary state of a HaPPY perfect-tensor network—the reduced density matrix $\rho_A$ on a boundary region $A$ is proportional to an orthogonal projector of rank $2^{S(A)}$, so its normalized Rényi-$n$ to von Neumann entropy ratio is constant:
$$
\operatorname{stabilizerRenyiFactor}(n) := \frac{S_n^{\mathrm{stab}}(A)}{S_1^{\mathrm{stab}}(A)} = 1.
$$
By contrast, for a single interval of von Neumann entropy $S_1 > 0$ in a 2D conformal field theory (Calabrese-Cardy / Ryu-Takayanagi), the Rényi-$n$ entropy scales as:
$$
S_n^{\mathrm{CFT}}(A) = \frac{1 + 1/n}{2}\,S_1 = \operatorname{cftRenyiFactor}(n)\cdot S_1.
$$

Over $\mathbb{Q}$, `lean4/CampaignAdsHappyToyNotDualityGap.lean` establishes:
- `cftRenyiFactor_one`: $\operatorname{cftRenyiFactor}(1) = \operatorname{stabilizerRenyiFactor}(1) = 1$.
- `recorded_cft_vs_stabilizer_renyi_factors`: $\operatorname{cftRenyiFactor}(2) = 3/4$, $\operatorname{cftRenyiFactor}(3) = 2/3$, $\operatorname{cftRenyiFactor}(4) = 5/8$, with unit-entropy defects $1/4, 1/3, 3/8$.
- `cftRenyiFactor_sub_half`: $\operatorname{cftRenyiFactor}(n) - 1/2 = 1/(2n)$.
- `renyiSpectrumDefect_formula`: For $n \ne 0$, $\operatorname{renyiSpectrumDefect}(n, S_1) := S_n^{\mathrm{stab}}(S_1) - S_n^{\mathrm{CFT}}(S_1) = \frac{n - 1}{2n}\,S_1$.
- `renyiSpectrumDefect_pos_of_gt_one` and `cft_ne_stabilizer_renyi_of_gt_one`: For all $n > 1$ and $S_1 > 0$, $\operatorname{renyiSpectrumDefect}(n, S_1) > 0$, so $S_n^{\mathrm{CFT}}(S_1) \ne S_n^{\mathrm{stab}}(S_1)$.
- `cftRenyiFactor_strict_anti`: For $0 < m < n$, $\operatorname{cftRenyiFactor}(n) < \operatorname{cftRenyiFactor}(m)$.

---

## 2. Explicit Ryu-Takayanagi Minimal-Cut Deficit Witnesses & Complete Length Census on the HaPPY `{5,4}` Patch

Building on `FrontierHappyMincut` (the 20-qubit boundary state of the 6-pentagon `{5,4}` HaPPY star patch with all 6 bulk logical legs fixed in $|0_L\rangle$), `lean4/CampaignAdsHappyToyNotDualityGap.lean` resolves the exact structure of the 40 intervals where the naive Ryu-Takayanagi minimal-cut equality $S(A) = \operatorname{mincut}(A)$ fails:
- `happy_witness_start2_len8_deficit`: For the explicit 8-qubit contiguous interval `(start = 2, len = 8)` (qubits `2..9`, splitting outer pentagons `0` and `2` each `2|2` across outer pentagon `1`), `intervalEntropy 2 8 = 4 < 5 = intervalMincut 2 8`.
- `happy_witness_start2_len12_deficit`: For the complementary 12-qubit interval `(start = 2, len = 12)`, `intervalEntropy 2 12 = 4 < 5 = intervalMincut 2 12`.
- `happy_fivefold_rotational_deficit_orbit`: Across all five outer pentagons $k \in \{0, 1, 2, 3, 4\}$, the rotated 8-qubit interval `(4 * k + 2, 8)` satisfies `intervalEntropy (4 * k + 2) 8 = 4` and `intervalMincut (4 * k + 2) 8 = 5`.
- `happy_short_and_long_intervals_exact_mincut`: Every contiguous boundary interval of length $1 \le l \le 7$ or $13 \le l \le 19$ satisfies `S(A) = mincut(A)` (`20` exact equalities and `0` deficits per length across all $14 \times 20 = 280$ such intervals).
- `happy_deficit_distribution_by_length`: Across lengths $8, 9, 10, 11, 12$, the strict deficit counts (`S(A) + 1 = mincut(A)`) are $5, 10, 10, 10, 5$ respectively, summing to $5 + 10 + 10 + 10 + 5 = 40$.

---

## 3. General-Region Mutual Information Jumps & Bulk-to-Boundary Hilbert Codimension

- `happy_disconnected_mutual_information_witnesses`: On the 20-qubit HaPPY boundary state:
  - Separated single boundary qubits `[0]` and `[8]` have $S([0]) = 1$, $S([8]) = 1$, and $I([0] : [8]) = 0$.
  - Separated 4-qubit outer pentagons $P_0 = [0,1,2,3]$ and $P_2 = [8,9,10,11]$ have $S(P_0) = 1$, $S(P_2) = 1$, $S(P_0 \cup P_2) = 2$, and $I(P_0 : P_2) = 0$.
  - Two 2-qubit halves $[0,1]$ and $[2,3]$ of outer pentagon $P_0$ have $S([0,1]) = 2$, $S([2,3]) = 2$, $S(P_0) = 1$, and $I([0,1] : [2,3]) = 3$.
  - Two outer pentagons $P_0 \cup P_1 = [0..7]$ ($S = 2$) and $P_2 = [8..11]$ ($S = 1$) have joint entropy $S(P_0 \cup P_1 \cup P_2) = 2$ and $I(P_0 \cup P_1 : P_2) = 1$.
- `code_subspace_strict_codimension` and `recorded_happy_tiling_hilbert_codimensions`: Whenever $N_{\mathrm{bulk}} < N_{\mathrm{bdry}}$, $2^{N_{\mathrm{bulk}}} < 2^{N_{\mathrm{bdry}}}$ and the orthogonal complement has positive dimension $2^{N_{\mathrm{bdry}}} - 2^{N_{\mathrm{bulk}}} > 0$, taking values $32 - 2 = 30$ (1 pentagon), $1048576 - 64 = 1048512$ (6-pentagon star patch), and $33554432 - 2048 = 33552384$ (11-pentagon `{5,4}` 1-ring).

---

## What is proved

- **Rényi Spectrum Non-Equivalence**: `cftRenyiFactor_one`, `recorded_cft_vs_stabilizer_renyi_factors`, `cftRenyiFactor_sub_half`, `renyiSpectrumDefect_formula`, `renyiSpectrumDefect_pos_of_gt_one`, `cft_ne_stabilizer_renyi_of_gt_one`, and `cftRenyiFactor_strict_anti` in `lean4/CampaignAdsHappyToyNotDualityGap.lean`.
- **Explicit Ryu-Takayanagi Deficit Witnesses & Length Census on the HaPPY `{5,4}` Patch**: `happy_witness_start2_len8_deficit`, `happy_witness_start2_len12_deficit`, `happy_fivefold_rotational_deficit_orbit`, `happy_short_and_long_intervals_exact_mincut`, and `happy_deficit_distribution_by_length` in `lean4/CampaignAdsHappyToyNotDualityGap.lean`.
- **Disconnected Mutual Information Witnesses & Hilbert Codimension Fence**: `happy_disconnected_mutual_information_witnesses`, `code_subspace_strict_codimension`, and `recorded_happy_tiling_hilbert_codimensions` in `lean4/CampaignAdsHappyToyNotDualityGap.lean`.
- **Independent Verification & Mutation Killing**: 499 exact rational and GF(2) symplectic checks with 0 failures in `checks/independent/ads-happy-toy-not-duality-gap.py`, and 6 of 6 semantic Lean mutations killed in `dag/research/campaign_ads-happy-toy-not-duality-gap_lean_mutation.json`.

## What is assumed

- Nothing is imported by this node as a premise of a continuum claim; the continuum CFT Rényi scaling factor $(1 + 1/n)/2$ is compared solely as an algebraic expression over $\mathbb{Q}$.

## What is open

- Constructing a dynamical bulk-to-boundary theory with Lorentzian time evolution, non-flat entanglement spectra, sub-AdS locality, and continuum gravitational dynamics (`status: "OPEN"`).
