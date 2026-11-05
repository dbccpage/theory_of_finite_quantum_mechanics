# The outside mathematical examination, checked

**Input.** A 10-page "Mathematical examination of the holographic-brain paper" (dated 2026-11-05), forwarded by Jeremy on 2026-11-05 from another reviewer, kept here as [holographic_brain_math_exam.pdf](holographic_brain_math_exam.pdf). Its LaTeX source was offered through a link that does not resolve, so only the PDF is on file. It is another review: say-so until checked.

**Method.** Each of its fourteen sections is read against the paper's text and against this folder's own checks. Every line below says one of three things and what it rests on:

- **agrees**: this folder already has the finding, with its own evidence named;
- **adds**: new to this folder, re-derived here (arithmetic or a short symbolic check) before being accepted;
- **differs**: the examination and this folder read the same equations differently, with the difference stated.

Agreement between the examination and this folder is two readings of the same equations. It is not two pieces of evidence. The evidence is the named check in each row.

---

## 1. Section by section

| Exam § | Finding (the examination's) | Verdict | What it rests on |
|---|---|---|---|
| 0 | The model is a chosen nonrelativistic charged scalar coupled to A_μ; "water" and "microtubule" are names, not derivations. | agrees | Mutation audit rows J, L, Y, Z. |
| 1 | A⁰ = 0 with ∇·A = 0 gives ∇·E = 0, while (A6)–(A7) require ∇·E = −e\|φ\|². Contradiction for N > 0. Possible repair: keep ∇·A = 0, let A⁰ obey ∇²A⁰ = −ρ. A neutralizing background forces a static ρ. | agrees | Check 1 (sympy). The repair is mutation audit row D1; the static-background remark is row F1 (frozen density). |
| 2 | The eigenoperator in (A9) contains e²A²/2m, so a fixed basis φ_n(x) under a time-dependent A is an approximation with ⟨φ_m\|∂_tφ_n⟩ terms not shown. | **adds** | (A9) as printed carries the A² term: witnessed in the transcript. The point is correct and this folder had not made it. Ledger row G1 is narrowed accordingly. |
| 2 | (A11) has A₃ independent of x³ while its source may depend on x³; a longitudinal average or projector is used later but not defined. | **adds** | (A11) and (A13): the operator has no ∂₃ and k³ = 0 (mutation audit row M1). The missing projector is new here. |
| 3 | (A31) prints χ₁ where (A34) needs χ₀. | agrees | The transcript's note at (A31); earlier typo list in the paper transcript. |
| 4 | Z² + R² = N² only when Im(χ₀*χ₁) = 0; the substitution Z = N cos θ, R = N sin θ selects the real-coherence sector. Counterexample χ₀ = √(N/2), χ₁ = i√(N/2). | **adds**, with one addition | The identity is arithmetic. Re-derived here: under (A33)–(A34) with 𝒜 real, d/dt(χ₀*χ₁) = g𝒜(\|χ₁\|² − \|χ₀\|²) is real, so Im(χ₀*χ₁) is conserved. The condition is on the initial data only; the flow preserves it. The examination's "owed: preserve it under the dynamics" is therefore already discharged by (A33)–(A34). |
| 5 | The sech pulse (A45)–(A47) follows from (A42)–(A43); τ_R = 2π/(g²ΩN), τ₀ = −τ_R ln tan(θ₀/2). | agrees | Self-audit checks S1c, S1d. |
| 5 | With θ₀ = 0 and 𝒜(0) = 0 the solution stays θ ≡ 0, 𝒜 ≡ 0; the burst needs a seed, and none is propagated. | agrees | Mutation audit row T1 (τ₀ → ∞ as θ₀ → 0). |
| 5 | Adiabatic self-consistency: \|𝒜̇\|/(\|𝒜\|/L₃) = (L₃/τ_R)\|tanh\| requires g²ΩNL₃/2π ≪ 1, i.e. L₃ ≪ τ_R; the formal N → ∞ limit violates it. | agrees, sharper | Check 2 found the sech within 1 % at L₃ = 0.005/Ω and off by 24 % at 0.5/Ω; the examination's closed-form condition L₃ ≪ τ_R says the same thing in one line and adds the N → ∞ remark. |
| 6 | The particular solution of (A48) for a plane-wave drive is C = M²b/(M² + μ² + \|k\|² − ω²); (A49) needs ω² = \|k\|² (on-shell drive) and \|μ²\| ≪ M². | agrees, with a detail added | Check 5 has the screening series in μ²/M² = 0.045. The on-shell condition ω² = \|k\|² is new here and correct: the paper's (A49) silently drops the □ contribution. |
| 6 | (A52) contains the twin image r²o* and other orders; no readout selects the image. | agrees | Mutation audit rows B2, P. |
| 6 | (A52) prints Ã_i (the input) where the algebra gives A_i (the response). | agrees | The transcript's note at (A52). |
| 7 | 2.60 PB and 31.25 TB unrounded; the paper's 2.5 PB and 30 TB are consistent. | agrees | Self-audit S3f–g; mutation audit §1 row H2. |
| 7 | λ = 500 nm is chosen, not derived from Ω; λ_emit = 2π/Ω is never computed. | agrees | Mutation audit rows K1, U1; check 9. |
| 7 | Sensitivity: a 4 meV mode gives λ ≈ 310 µm and the same formula gives ≈ 11 MB. | **adds** | Re-derived: λ = 1239.84 eV·nm / 0.004 eV = 310 µm; 2.6 PB × (500 nm / 310 µm)³ = 10.9 MB. The examination marks this as an illustration, not a claim about the paper's intent; so does this folder. |
| 8 | (6)–(9) are a supplied binary-encoding algorithm, not a derivation of the image from neural dynamics. | agrees | Mutation audit row D2. |
| 9 | The 2PI machinery is genuine; Γ₂ and the propagators are never evaluated; (A75) replaces them by M² and γ as parameters, so the output equations are effective mean-field equations. | agrees | Check 3; mutation audit rows J2, K2, L2. |
| 10 | (A70) prints a minus on the squared phase-gradient term; the correct sign is plus; (A81) has the plus. Counterexample: the free plane wave β = k·x − k²t/2m, R constant, A = A₀ = 0. | agrees | Check 3 (sympy) found the same misprint and the same correct sign. The plane-wave counterexample is re-done here: left side k²/(2me); right side with plus k²/(2me), with minus −k²/(2me). It is a cleaner demonstration than check 3's and is adopted. |
| 11 | The reduced 2D system (A76)–(A81) and the layer coupling u^{(n)} = A^{(n−1)} + A^{(n+1)}; no z-dependent Maxwell problem is solved between layers. | agrees | Mutation audit rows M2, O2, P2. |
| 11 | The static inversion (A88)–(A89) neglects Ė, γ(E + ∂A₀) and e²ρA/m; at the paper's values e²ρ/m = 0.09 and (e²ρ/m)/M² = 4.5 %. | agrees | Check 5 (0.045); mutation audit row W2. |
| 11 | The target (10) is piecewise linear, so its second difference is a delta at the corners: Δs = 0.1(1/30 + 1/34) = 0.00627; the paper's claim that ∂₂²u₁ and ∂₁∂₂u₂ vanish for the target holds only between corners. | **adds** | Re-derived on the paper's grid (N_s = 64, N₁ = 30): nonzero second differences at n = ±30, magnitude 0.006275. Relative to the M²u₁ term in (A88) at the corner cells (2 × 0.1) that is 3.1 %. The paper's sentence after Figure 4 says the terms are zero; on the grid they are not, at two cells. Small, but as stated it is wrong. |
| 11 | Input amplification 0.1·(2/0.8)⁴ = 3.90625; the 21 % at m x⁰ = 200 is a numerical output for chosen inputs and boundary conditions. | agrees | Check 11 (3.9); mutation audit rows Q2, Y2, U2. |
| 12 | No coil current, geometry, tissue ε, μ, σ or Maxwell boundary problem connects a physical driver to the prescribed A^{(0)}; the link is not calculated. | agrees, stated more fully | Mutation audit row P ("headset" external) and row Z2. The chain J_coil → Maxwell + tissue → A^{(0)} → A^{(4)} with its first two boxes empty is the examination's framing and is adopted. |
| 12 | The conserved energy (A73)–(A74) does not apply unchanged to the damped, driven sector; Ḣ = −γ∫Ȧ² + ∫fȦ. | agrees | Mutation audit rows K2, L2 (the relaxation terms are the Gauss-breaking terms); this folder had not written the energy balance out, and now has it. |
| 13 | Verdict table by equation range. | agrees in every row | Each row maps onto a check or a mutation-audit row above. |
| 14 | Residual requests R1–R9. | agrees | R8 (matched classical driven-field model) is the mutation audit's §6; R9 (one measured write/store/read/retention result) is its row C2; R6 (correct (A31), (A70), (A52)) is the transcript's typo list. |

**Differs:** none found. One place where this folder says more than the examination: its §1 reads (A7) as 0 = J₀ only; with the integration constant kept, (A7) reads ∂₀J₀ = 0, a frozen nonzero density, and either reading removes the oscillating coherence (mutation audit §1, row F1). One place where the examination says more than this folder: §4's phase condition, now adopted with the proof that the flow preserves it.

---

## 2. What is new to this folder, and now checked

1. **(A9) is not a fixed eigenproblem.** Its operator carries e²A²/2m, so a time-independent basis φ_n(x) is an approximation once A moves. Rests on the printed (A9).
2. **(A11) needs a projector onto x³-independent fields.** The paper averages later without defining the average. Rests on (A11), (A13).
3. **The Bloch identity needs Im(χ₀*χ₁) = 0 at t = 0,** and (A33)–(A34) with real 𝒜 then keep it zero. Rests on the arithmetic above.
4. **(A49) is on-shell only:** ω² = \|k\|² for the drive, or the □ term enters the denominator. Rests on the particular solution of (A48).
5. **The polygonal target has corner second differences** of 0.00627, 3 % of the M² term at two cells; the paper's "vanish" is wrong at those cells. Rests on the grid arithmetic.
6. **A plane-wave counterexample fixes the (A70) sign** in two lines. Rests on the substitution shown in the examination and redone here.
7. **The energy balance of the damped sector** is written: Ḣ = −γ∫Ȧ² + ∫fȦ. Rests on the reduced equation.

Items 1 to 7 are added to the claims ledger of this folder's critique as new rows (status: derived, from the examination, re-derived here).

---

## 3. Three findings Jeremy asked to see first

- **Gauss's law, Appendix A.** Confirmed by this folder's check 1 before the examination arrived. The repair the examination names (A⁰ from Poisson) is the mutation audit's row D1, with the price stated there: a Coulomb term the paper would have to bound.
- **The (A70) sign.** Confirmed by check 3 before the examination arrived; the examination's plane-wave counterexample is independent of check 3 and is now the shorter demonstration.
- **Zero-seed superradiance.** Confirmed by the mutation audit's row T1: θ₀ = 0 gives τ₀ = ∞, no pulse. The examination adds that no stochastic source is propagated through (A33)–(A47), which is correct and is what row T1 calls the missing seed.

Both documents reach these three findings from the same printed equations. That is the expected outcome when two readers compute the same thing, and it carries no weight beyond the computations themselves.

---

## 4. Companion references

Checks 1, 2, 3, 5, 9, 11 are in `../code/critique_checks.py`; S1, S3 in `../code/self_audit_checks.py`; the mutation audit is `assumptions_mutation_audit.md`; the paper transcript with its typo notes is `../02_paper/ijms-25-02399.md`. The short re-derivations in this file (A70 plane wave, the Im(χ₀*χ₁) conservation, the 310 µm / 11 MB figure, the corner differences) were run with sympy and numpy and are reproduced in `../code/math_exam_checks.py`.
