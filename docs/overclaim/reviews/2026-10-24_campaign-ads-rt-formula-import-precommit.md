Status: AI-drafted, awaiting human review.

# Pre-Commit Overclaim & Falsification Review: `ADS-RT-FORMULA-IMPORT` (`TFQ-2204`)

**Date:** 2026-10-24  
**Campaign Node:** `ADS-RT-FORMULA-IMPORT` (`TFQ-2204`, stage `ADS_CFT`)  
**Outcome:** `Narrowed` (`IMPORTED_ASSUMPTION` status preserved; narrowed to exact rational Ryu-Takayanagi / Brown-Henneaux coupling elimination, cut-pasting Strong Subadditivity and 380-interval HaPPY complement symmetry, von Neumann entropy dichotomy fence against rational RT areas, and exact rational Regge action proxy vs. minimal-surface area fences in Lean 4 and an independent Python verifier)  
**AuthorityEffect:** `None`

---

## 1. Falsification & Boundary Audit

1. **Ryu-Takayanagi / Brown-Henneaux Coupling Elimination & Minimal-Cut Submodularity**:
   - In `lean4/CampaignAdsRtFormulaImport.lean`, `rt_ads3_reproduces_calabrese_cardy` and `rt_over_brown_henneaux_eliminates_couplings` show over $\mathbb{Q}$ that substituting the regulated $\mathrm{AdS}_3$ geodesic length $2 R_{\mathrm{AdS}} \Lambda_{\log}$ into $\mathrm{Area}/(4 G_N^{(3)})$ reproduces $(c/3)\Lambda_{\log}$ under $c = 3 R_{\mathrm{AdS}} / (2 G_N^{(3)})$ and eliminates both $R_{\mathrm{AdS}}$ and $G_N^{(3)}$ from the ratio $S_A / c = \Lambda_{\log} / 3$.
   - `cut_pasting_strong_subadditivity_from_submodularity` establishes the surface-reconnection Strong Subadditivity inequality $S(ABC) + S(B) \le S(AB) + S(BC)$ from submodularity and minimality at $G_N > 0$, while `happy_mincut_and_entropy_complement_symmetry_all_380` verifies exact complement symmetry $A \leftrightarrow A^c$ across all $380$ proper contiguous boundary intervals of the 20-qubit 6-pentagon HaPPY patch.

2. **Von Neumann Entropy Dichotomy Fence (`FQ-ENTROPY-DICHOTOMY-BAKER`)**:
   - Importing `EntropyDichotomy`, `rtLeadingEntropy_realCast_isAlgebraic`, `no_rational_rt_area_for_mixed_algebraic_spectrum`, and `rational_rt_match_iff_pure_and_zero_area` show under `BakerCitedInput` that no mixed finite state with algebraic eigenvalues can have natural-log von Neumann entropy equal to a rational ratio $\mathrm{area}/(4 G_N)$, and that equality holds at $G_N > 0$ if and only if the state is pure and $\mathrm{area} = 0$.
   - `stabilizer_bits_to_nats_transcendental_conversion` shows that integer stabilizer bond counts $k$ are recovered from natural-log entropy $k \ln 2$ only after dividing by $\ln 2 \neq 0$.

3. **Exact Rational Regge Proxy (`TFQ-0100`) vs. Minimal-Surface Area & HaPPY Bond-Cut Fence**:
   - `orthogonal_pentatope_hinge_areas_sq`, `nat_dvd_three_of_sq_mul_four_eq_three_mul_sq`, and `no_rational_linear_area_for_equilateral_pentatope_hinge` show that on the `orthogonal_pentatope` chart of `TFQ-0100`, the 6 right-triangle hinges have Cayley-Menger squared area $1/4$ and the 4 equilateral-triangle hinges have squared area $3/4$ (summing to $9/2$), with no rational linear area $A \in \mathbb{Q}$ satisfying $A^2 = 3/4$.
   - `reggeProxy_zero_on_flat_chart`, `happy_all_380_intervals_pos_entropy_and_mincut`, `cayleyMengerTriangleAreaSq_homogeneous_deg4_in_length`, and `no_scale_invariant_regge_to_rt_dictionary` separate the flat-chart vanishing and $\lambda^4$ scaling of the rational Regge proxy from the strictly positive cuts ($1 \le S(A) \le \mathrm{mincut}(A)$ on all 380 intervals) and $\lambda^2$ / $\lambda^0$ scaling of minimal surfaces and bond counts.

---

## 2. Claim Hygiene Summary

1. **What it supports**:
   - In `lean4/CampaignAdsRtFormulaImport.lean` (`L4D`), the 16 declarations formalize the exact rational Ryu-Takayanagi / Brown-Henneaux algebra, Strong Subadditivity from submodular surface pasting, 380-interval complement symmetry on the 6-pentagon HaPPY patch, the `BakerCitedInput` entropy dichotomy fence against rational RT ratios for mixed algebraic spectra, and the non-equivalence fences separating the `TFQ-0100` rational Regge proxy ($A_h^2 \kappa_h$) from continuum minimal-surface areas and discrete HaPPY bond counts.
   - In `checks/independent/ads-rt-formula-import.py`, 545 exact rational and GF(2) symplectic checks pass with 0 failures, and 6 of 6 semantic Lean mutations are killed in `dag/research/campaign_ads-rt-formula-import_lean_mutation.json`.
2. **What it does not support**:
   - A derivation of the continuum Ryu-Takayanagi formula $S(A) = \mathrm{Area}(\gamma_A)/(4 G_N)$ from finite quantum mechanics, or a dictionary equating the repository's rational Regge proxy (`TFQ-0100`) with minimal-surface areas in a smooth bulk geometry.
3. **Narrowest defensible claim**:
   - While the continuum Ryu-Takayanagi formula remains an `IMPORTED_ASSUMPTION`, its rational $\mathrm{AdS}_3 / \mathrm{CFT}_2$ Brown-Henneaux coupling elimination, submodular cut-pasting inequality, `BakerCitedInput` transcendental separation from rational areas on mixed algebraic spectra, and structural non-equivalence with the $\lambda^4$-scaling `TFQ-0100` rational Regge proxy are machine-checked in Lean 4 and cross-checked in Python.
4. **Next test needed**:
   - Proceed to the next available AdS/CFT derivation in `dag/pfp/campaign/derivation_queue.json` (`ADS-REGGE-AREA-RT-GAP`, `TFQ-2211`).
