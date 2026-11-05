# G3 & G4 Meron Chain Field Theorems & Finite-M Analysis

**AuthorityEffect:** None.

This folder contains the complete mathematical artifacts, prompts, model responses, exact rational verification scripts, and master synthesis dossier for the periodic full-Fock $U=t$ Meron chain research program.

---

## Directory Organization

- [`meron_spacetime_field_theorems.md`](meron_spacetime_field_theorems.md): Definitive peer-review synthesis of Theorems A and B, G3 and G4 resolutions, Gate E refutation, Gate D polymer closure, and emergent positivity for OpenAI / Codex review.
- [`g3_g4_research_dossier_and_next_targets.md`](g3_g4_research_dossier_and_next_targets.md): Research dossier. Its scorecard and section 3 both mark Gate D, Gate F, and Theorem B closed; they do not draw those items as open. Gate G's extinction claim is marked as not in the Gate E receipt. Gate E is the one-point receipt.
- [`gate_e_exact_refutation.md`](gate_e_exact_refutation.md): Exact rational witness that $G^{(2)}_{4,1}$ is not positive semidefinite at $L=4$, $M=1$, $r=1/10$.

### Subdirectories

1. [`prompts/`](prompts/):
   - [`codex_peer_review_prompt.md`](prompts/codex_peer_review_prompt.md): Executive peer-review protocol for OpenAI Codex to audit the monograph and propose the next research targets.
   - [`deepseek_sprint6_prompt.md`](prompts/deepseek_sprint6_prompt.md): Sprint 6 prompt targeting final closure of G3 (boundary CAR string and MIMO constant A).
   - [`deepseek_sprint5_prompt.md`](prompts/deepseek_sprint5_prompt.md): Sprint 5 prompt targeting the discrete-to-continuum Trotter passage, emergent positivity, and Theorem B.
   - [`deepseek_sprint4_prompt.md`](prompts/deepseek_sprint4_prompt.md): Sprint 4 prompt targeting Gate D (complex winding phases and Lee-Yang zero obstruction).
   - [`g3_prompt.md`](prompts/g3_prompt.md): Volume- and time-slice-uniform mixed-cumulant prompt.
   - [`g4_prompt.md`](prompts/g4_prompt.md): Time-resolved spacetime covariance limit prompt.
   - [`fugu_prompt_3.md`](prompts/fugu_prompt_3.md): Strongest defensible spacetime field theorem prompt.
   - [`fugu_prompt_4.md`](prompts/fugu_prompt_4.md): Infinite-family time-resolved covariance limit prompt.

2. [`responses/`](responses/):
   - [`deepseek_sprint6_g3_closure.md`](responses/deepseek_sprint6_g3_closure.md): DeepSeek Sprint 6 response delivering the final, definitive mathematical closure of G3.
   - [`deepseek_sprint5_theorem_b.md`](responses/deepseek_sprint5_theorem_b.md): DeepSeek Sprint 5 response establishing the Trotter error bounds, negative mode extinction ($O(M^{-6})$), and Theorem B.
   - [`deepseek_sprint4_gate_d.md`](responses/deepseek_sprint4_gate_d.md): DeepSeek Sprint 4 response establishing bulk KP polymer convergence and Gate D zero-freeness.
   - [`deepseek_sprint3_spatial_clt.md`](responses/deepseek_sprint3_spatial_clt.md): DeepSeek's Sprint 3 proof of Theorem A via unequal-time spatial clustering and MIMO's Lemma A.
   - [`deepseek_sprint2_zero_mode.md`](responses/deepseek_sprint2_zero_mode.md): DeepSeek's Sprint 2 analysis of the $r=0$ flat zero mode.
   - [`deepseek_sprint1_exact_cusp.md`](responses/deepseek_sprint1_exact_cusp.md): DeepSeek's Sprint 1 exact rational cusp derivation ($\gamma = \theta^2/4$).
   - [`mimo_v2_6_pro_g3_response.md`](responses/mimo_v2_6_pro_g3_response.md): MIMO-V2.6-PRO's analytical proof reducing G3 to Lemma A (spacetime Ursell bound) and proving that analyticity alone fails by $(2M)^n L^n$.
   - [`deepseek_g3_gate3_exact_proof.md`](responses/deepseek_g3_gate3_exact_proof.md): Gate 3 proof of infinite temperature and mode activation.
   - [`deepseek_g4_covariance_response.md`](responses/deepseek_g4_covariance_response.md): DeepSeek's initial G4 covariance response.
   - [`deepseek_g4_followup_response.md`](responses/deepseek_g4_followup_response.md): DeepSeek's follow-up corrections.
   - [`g4_sakana_fugu_ultra_v2_response.md`](responses/g4_sakana_fugu_ultra_v2_response.md): Raw Fugu Ultra v2 generation response.
   - [`g4_sakana_fugu_ultra_v2_receipt.json`](responses/g4_sakana_fugu_ultra_v2_receipt.json): Billing and token receipt for Fugu Ultra v2.

3. [`code/`](code/):
   - [`gate_e_exact_counterexample.py`](code/gate_e_exact_counterexample.py): Sympy/Python script computing the exact rational characteristic polynomial and negative eigenvalue $\lambda_{\min} = -1/706440$ on the 16-dimensional CAR Fock space.
   - [`gate_e_exact_counterexample_receipt.json`](code/gate_e_exact_counterexample_receipt.json): Numerical receipt of the exact roots and negative quadratic form $v^\top G v = -1/88305 < 0$.
   - [`run_sakana_prompt1.py`](code/run_sakana_prompt1.py): Provider execution runner connecting to Sakana AI / OpenRouter.
