# Retest log: claim → counterexample → repair → retest → residual obligation

Date: 2026-11-05. This answers ChatGPT's second-round review. That review confirmed parts of [adversarial_review.md](adversarial_review.md) and named new overclaims in the recovered arguments. Each item below runs the full cycle, ending with what is still owed. Checks are in [code/retest_checks.py](code/retest_checks.py). R1 is a floating-point numerical rerun. R2 to R4 are exact.

**Standing caution.** Agreement between ChatGPT and Claude is not evidence that something is true. Two language models agreeing after an exchange is a fact about the exchange, not about the physics. In this log only three things count as evidence: an exact computation, the rerun of the paper's own equations, and quoted text from the paper. Every result carries its tag: **Witnessed** (a record exists), **Derived** (an exact check here), **Numerical** (a floating-point rerun), **Supplied** (an assumption), or **Open**. Nothing here has had human review. The unchecked list is at the end.

Two of the claims ChatGPT audits were not in `adversarial_review.md`. The roughly $4\times10^9$ molecular count and the "public opener" critique came from a different adversary pass. They are still audited below, because the board relied on that material.

## R1. Gauge: does the repair satisfy Gauss's law with charged matter?

**Claim (ChatGPT, round 2).** Appendix A is inconsistent as written: $A^0 = 0$ and $\nabla\cdot\mathbf A = 0$ force $e|\varphi|^2 = 0$, against $\int|\varphi|^2 = N$. The objection does not reach Appendix C.

**Counterexample to the claim as worded.** (A7) is an integral in time. The paper drops the time-independent constant "that might represent boundary conditions". Keep that constant as a static background, and the static part of the charge no longer contradicts anything. So the precise statement is this: Appendix A is inconsistent **as printed, with the constant set to zero**. With the constant kept, the remaining problem is the time-dependent charge. That includes the slow change of the diagonal density as the populations move ($\theta \to \pi$ in (A44)), not only the oscillation at $\Omega$. So Appendix A is consistent only for stationary states ([self_review.md](self_review.md) A1). ChatGPT's round-2 text agrees that a fixed background cannot absorb a charge that changes in time.

**Retest A: does the modeled emission need a changing charge?** ChatGPT notes that a static density does not forbid every radiating transverse current, and that is true. The question is whether *this* current is one of those. For real eigenstates of $-\nabla^2/2m + U$, the transition current $j = \phi_0\partial_3\phi_1 - \phi_1\partial_3\phi_0$ has

$$\partial_3 j = \phi_0\phi_1'' - \phi_1\phi_0'' = -2m(E_1 - E_0)\,\phi_0\phi_1 \neq 0 .$$

Checked symbolically for oscillator states ([R2](code/retest_checks.py)): $\partial_x j = -2m\omega\,\psi_0\psi_1$. So the Appendix A source current is not divergence-free. By continuity it needs a density oscillating at $\Omega$, which is exactly the part that $A^0 = 0$ drops. *Derived.* ChatGPT's general caveat is correct but does not apply to this mechanism.

**Retest B: Appendix C, by rerunning the simulation.** In round 1, `adversarial_review.md` showed symbolically that the $M^2$, $\gamma$ and $v$ terms break Gauss's law, and left the size of the violation **Open**. I reran Section 4 at the paper's parameters: $N = 4$ layers, a $128^2$ periodic lattice, $e = 0.3$, $v = 0.8$, $\gamma = 0.2$, $M^2 = 2$, $\gamma_2 = 0.01$, $dt = 0.001$, RK4. I then measured $G = \nabla\cdot\mathbf E - J^0 - e$ on the output layer, with $\mathbf E$ taken from the paper's own (A83).

**Reproduction check (Numerical).** With the input scaled to the paper's stated amplitude, about 3:

| $mx^0$ | density dip in the target box, rerun | paper (Fig. 6 text) | max \|G\| | max \|e δρ\| | rms G / rms e δρ |
|---|---|---|---|---|---|
| 5 | 1.44% | 1.3% | 1.2e-2 | 4.5e-3 | 2.3 |
| 20 | 4.98% | 4.5% | 3.4e-2 | 1.6e-2 | 1.14 |
| 40 | 9.07% | 9.1% | 7.3e-2 | 2.9e-2 | 1.12 |

With the input amplitude from my own (A88)–(A89) recursion (2.13), the dip at $mx^0 = 5$ is 1.03%, with the same rms ratio of 2.3. Total charge is conserved to about 1e-15 in every run. The rerun matches the paper's dips to within about 10% and lands on 9.1% at $mx^0 = 40$. So it is very likely the same simulation, though nobody has compared it against the authors' code.

**Result (Numerical).** The Gauss-law residual is **as large as the charge change itself**, or larger. The rms ratio runs from 1.1 to 2.3 over the whole run. The violation is order one, not a rounding effect.

**Is it a stencil artefact? (Numerical).** At $mx^0 = 5$ I split the residual rate $\partial_t G$ into its terms (rms over the output layer):

| term | rms contribution to $\partial_t G$ |
|---|---|
| discrete curl–curl (zero in the continuum) | 3.1e-7 |
| discrete current against $\partial_t J^0$ (zero in the continuum) | 1.5e-18 |
| $-M^2\nabla\cdot\mathbf A$ | 3.2e-2 |
| $v\,\nabla\cdot\mathbf A^{(n\pm1)}$ | 1.8e-2 |
| $-\gamma\,\partial_t\nabla\cdot\mathbf A$ | 4.5e-4 |

The stencil contributes about five orders of magnitude less than the paper's added terms. The violation is the paper's, not mine.

**Repaired claim (Numerical, on the paper's equations).** Along the very run that produces Figure 6, the electric field fails Gauss's law by an amount comparable to the charge density it is supposed to carry. The hologram's 9% density dip is not matched by the Coulomb field that such a dip would require.

**Residual obligations.**
- My input amplitude from (A88)–(A89) is 2.13, where the paper says "approximately 3" (its factor of 3.9 drops the subtraction terms). A run scaled to 3 brackets this.
- The printed (A88) has $-\partial_1^2 u_1$, but the text says the $\partial_2^2 u_1$ term vanishes. I used the form consistent with (A82). For these targets the two forms differ only at the kinks.
- A transverse-only model, with $M^2$ and $\gamma$ acting on transverse $\mathbf A$, could be consistent. It would have to be re-derived and rerun. Whether the hologram survives in such a model is open.

## R2. Do equal reports give equal likelihoods?

**Claim (board and ledger, before repair).** $q(A) = q(B) \Rightarrow BF = 1$.

**Counterexample.** Let $q(a) = q(b) = 0$ and $q(c) = 1$. Hypothesis $H_1$ puts mass ½ on each of $a, b$. Hypothesis $H_2$ puts mass ½ on each of $a, c$. Then $a$ and $b$ give the same report, but $P(D{=}0\mid H_1) = 1$ and $P(D{=}0\mid H_2) = ½$, so $BF = 2$ ([R3](code/retest_checks.py)). *Derived, exact.*

**Repair.** $BF = 1$ holds when each hypothesis is a single state and the report is deterministic, or more generally when both hypotheses give the same *distribution* of reports. The board's blind-spot card and §1b of the ledger now state this condition: "on this channel".

**Retest.** The counterexample is no longer a counterexample to the repaired statement, because $H_1$ and $H_2$ give different report distributions. *Passes.*

**Residual obligation.** For the rendering claim, someone has to say what distribution over reports "rendered" and "not rendered" each predict. Until then, the Bayes factor is undefined rather than 1.

## R3. Can a finite observer separate every state of a small enough domain?

**Claim (board, before repair).** "Every finite observer has differences it cannot report."

**Counterexample.** Three states and three reports, with $q$ injective. Every pair is separated ([R4](code/retest_checks.py)). *Exact.*

**Repair.** The condition is $\lvert P\rvert < \lvert X\rvert$, as in the Lean theorem `pigeonhole_resolution_limit`. Both the board and the ledger now state it.

**Retest.** The repaired statement does not apply to the counterexample, because $\lvert P\rvert = \lvert X\rvert$. *Passes.*

**Residual obligation.** For a tree, the air or a brain, $\lvert P\rvert < \lvert X\rvert$ is supplied, not shown.

## R4. Can one channel fail to separate two models that a wider channel separates?

**Claim.** Yes. This is the content of Picture 2 on the board.

**Retest.** On the board, worlds A and B give the same report with the viewport in the middle. They give different reports with the viewport on the right, or with an object count added, even when the extra object is never on screen. *Passes, by construction.*

**Residual obligation, ChatGPT's point accepted.** The absence of a proposed test is not proof that no test exists. One reading of the rendering claim is "unobserved systems stop evolving". That reading could predict a different state when measurement resumes, and so be testable. The ledger now says B4 is not evaluable *with the presentations in use*, and becomes evaluable once she names a channel.

## Also audited

| Claim | Status after retest |
|---|---|
| About $4\times10^9$ molecules in a (500 nm)³ cube | Arithmetic holds: 33.4 molecules/nm³ × $1.25\times10^8$ nm³ ≈ $4.2\times10^9$. ChatGPT is right that this is not the number of coherent emitters and does not size the dropped near-field term. That needs charge density, geometry and screening. Open. |
| "Unexperienced" is an easy answer to the public opener | ChatGPT is right. If she picks that reading, her claim has been clarified into ordinary limited observation, and that is a result. |
| 2.6 PB vs 2.5 PB | ChatGPT has withdrawn its objection. Recorded in [board_repair_log.md](board_repair_log.md). |
| Landauer recovery (one year needs a barrier of about 1.2 eV) | Narrowed by the self-review ([self_review.md](self_review.md) A8–A10). Overwriting an occupied medium *does* cost $k_BT\ln2$ per bit. The 1.2 eV threshold holds only for a record held by a single barrier. A collective order parameter can have an extensive barrier. The 33 ps illustration is withdrawn. What remains is an obligation, not a refutation: the barrier has to be computed. |

## Not yet checked by anyone outside the LLM loop

- The rerun in R1 is my own implementation of (A82)–(A90). Nobody has compared it with the authors' code. Its match to the paper's density dips is the only evidence that it is the same simulation.
- The physics citations: super-radiance near-field dephasing, the Ward identity, Bennett on reversible copying, and the hydrogen-bond energy.
- Whether a transverse-only version of Appendix C would still form the hologram.
- The size of the near-field term that Appendix A drops.
- None of this has had expert human review.

## Rule taken from this round

A repair is accepted only if it discharges the original objection **and** the repaired statement passes a retest against the counterexample that broke it, with every new assumption listed as a residual obligation. Surviving one adversarial exchange is not enough.
