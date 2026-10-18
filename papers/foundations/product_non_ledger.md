Claim Ledger — Paper QM_070: Product Non-Factorization as a Bipartite Obstruction (OMEGA-QM-PROD-NONFACT-035)
=============================================================================================================

**Paper Key:** `003_quantum_foundations/070_product_non_factorization_as_a_bipartite_obstruction`  

Date: 2026-06-17
Version: v0.1 (Pre-Print)
Series: qm / QM ingredient ladder (rung 8A)
Companions: pub-001 (factorized states), pub-010 (phase-blind descent + voice), QM_071 (separability — next rung, planned)

Firewall note: QM is a realization spine. This paper mints no authority; the load-bearing
discipline is the green/red firewall — a finite structural fact about the declared carrier and
basis, never `IsAuth`. `StructureDerived(F,c) ⇏ IsAuth(t)`.

Paper character: a **finite obstruction-calculus derivation** with one mechanized theorem
(ENC-1123). The headline is honestly typed `[PROVEN]` (it is one-line elementary algebra,
mechanized), and the scope is fenced hard: this is non-product **correlation**, not
entanglement.

Claim index
-----------

| ID | Claim (abbreviated) | Status | Location |
|---|---|---|---|
| QM-070-C1 | Carrier = finite nonnegative joint weight table $w:A\times B\to\mathbb{Q}_{\ge0}$, $W>0$ | [DEFINITION] | §1 |
| QM-070-C2 | Descent QM→classical table via $w(a,b)=|\langle a,b|\psi\rangle|^2$ (phase-blind, basis-fixed) | [DEFINITION / SCOPE FENCE] | §1 |
| QM-070-C3 | Product defect $\delta_{\mathrm{prod}}(a,b)=w(a,b)-w_A(a)w_B(b)/W$ | [DEFINITION] | §2 |
| QM-070-C4 | ZeroRel: $\delta_{\mathrm{prod}}\equiv0$ identifies product carriers | [DEFINITION] | §3 |
| QM-070-C5 | **Theorem:** $\Phi(w)=0 \Leftrightarrow w$ factors through its marginals | [PROVEN] — mechanized `Phi_zero_iff_factors`, ENC-1123 | §5 |
| QM-070-C6 | Witnesses: `diagHalf` $\Phi=1>0$ (marginals uniform/green); `uniformQuarter` $\Phi=0$ | [PROVEN] — mechanized `diagHalf_Phi_pos`, `uniformQuarter_Phi_zero` | §8, §9 |
| QM-070-C7 | Bell $|\Phi^+\rangle$ and the classical mixture share the $(½,0,0,½)$ table ⇒ $\Phi$ does not see entanglement | [SCOPE FENCE] | §9, Abstract |
| QM-070-C8 | Local factorized maps send products to products, so a product carrier stays product and $\Phi=0$ is preserved; **general** monotonicity on non-product carriers NOT claimed | [PROVEN — elementary] + [SCOPE FENCE] | §10 |
| QM-070-C9 | $\Phi$ is basis-relative (product in one basis ≠ product in another) | [SCOPE FENCE] | §1, §12, non-claims |
| QM-070-C10 | Green/red firewall: $\Phi$ is structural; mints no authority | [SCOPE FENCE] | §11 |
| QM-070-C11 | Classical reading: independence ⇔ joint = product of marginals; $\Phi$ one $\ell^1$ dependence gauge (cf. TV-to-product, mutual information = KL to product; Cover & Thomas) | [INTERPRETIVE] — standard facts | §12 |
| QM-070-C12 | Falsifiability: a product carrier with $\Phi>0$ or a factorizable carrier with $\Phi=0$ | [SCOPE FENCE / FALSIFIABILITY] | Falsifiability |

Definition-as-theorem audit
---------------------------

PASSED. The single Theorem (C5) is genuinely a theorem (an exact zero-locus equivalence),
mechanized; its proof is one-line elementary algebra, and the paper says so. No definition is
dressed as a result. C1–C4 are explicitly typed `[DEFINITION]`.

Support ledger (Part C — upgrade paths)
---------------------------------------

| ID | What would upgrade / extend it | Difficulty | Lean/numerical? | Obligation? |
|---|---|---|---|---|
| QM-070-C7 → QM_071 | The separability obstruction proper: $\delta_{\mathrm{sep}}(w,\{\lambda_i,a_i,b_i\})=w-\sum_i\lambda_i(a_i\otimes b_i)$, ZeroRel = a finite convex product-decomposition witness exists. This is **entanglement**. | Hard — convex geometry; richer carrier (coherence) | Prose + Lean (later) | **No — separate paper (QM_071)**, not an obligation of QM_070 |
| QM-070-C11 | Citation resolved (Cover & Thomas, *Elements of Information Theory*) — standard dependence-measure facts; no further action | — | — | Resolved (adversary 2026-06-17) |

**No honesty-gating open obligations.** C5/C6 are mechanized (ENC-1123); C7/C9/C10 are scope
fences; C8/C11 are correctly typed interpretive. The separability rung (QM_071) is a *new
derivation*, deliberately out of scope here — recording it as an obligation of this paper would
misstate what this paper claims.
