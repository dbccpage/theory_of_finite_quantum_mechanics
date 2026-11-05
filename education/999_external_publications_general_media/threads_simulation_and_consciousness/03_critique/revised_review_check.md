# The revised outside review, checked

**Input.** A package of ten documents and a 30-check script, forwarded by Jeremy on 2026-11-05 and kept unedited in [outside_review_revised/](outside_review_revised/RECEIVED.md). It is a revision of earlier outside reviews and it was written with this folder's own critique in view: it answers several of this folder's claims directly. It is say-so until checked.

**Its script.** Run here against this folder's copies of the paper (hashes match its record): 30 of 30 pass, and its deliberate-failure switch fails exactly once. That shows the script does what it says; it does not show the review is right, because the script checks the review's own arithmetic, not the paper's.

**Method.** As for the math examination: agrees (this folder has it, evidence named), adds (new here, re-derived before acceptance), differs (the two readings disagree, with the resolution stated). Re-derivations are in `../code/revised_review_checks.py`.

---

## 1. Findings about the paper

| Package claim | Verdict | What it rests on |
|---|---|---|
| A⁰ = 0 with ∇·A = 0 makes (A7) read 0 = −e\|φ\|²; with the integration function kept, e\|φ\|² = c(x), a static background. | agrees | Check 1; mutation audit rows D1, F1. |
| "A static density alone does not exclude every transverse current; the stronger assertion that it forces all two-level coherence to vanish is not established." | **differs, resolved** | Write the density in the paper's own two-level basis: \|φ\|² = \|χ₀\|²\|φ₀\|² + \|χ₁\|²\|φ₁\|² + 2 Re(χ₀*χ₁ e^{−iΩt} φ₀*φ₁). The cross term oscillates at Ω while χ is slow by (A33)–(A34). A density frozen pointwise therefore needs χ₀*χ₁ = 0 wherever φ₀*φ₁ ≠ 0, and where φ₀*φ₁ = 0 the coupling J₀₁ = ∫φ₀*∇₃φ₁ has no support either. So R = 2χ₀*χ₁ = 0 and (A38) gives no pulse. The package's general remark is true of currents in general and does not reach the two-level ansatz the paper uses. Re-derived in the script. |
| The Appendix A objection does not transfer to Appendix C, which keeps A₀. | agrees | Critique §5; mutation audit row I2. |
| Appendix C: ∂_t(∇·E − ρ_m) = ∇·S with S the M², γ, v terms; the matter-only Gauss law is not preserved, but an effective medium could carry charge, so this is not by itself total charge nonconservation. | agrees, and narrows this folder | The identity is the sibling's check 1a and the rerun's residual. The narrowing is accepted: the mutation audit's rows K2, L2 and finding 7 now say "matter-charge Gauss law", and note that the paper names no medium charge. |
| **(A88)/(A89) carry −∂₁²u₁ and −∂₂²u₂ where (A82)/(A84) give −∂₂²u₁ and −∂₁²u₂.** | **adds** | Witnessed in the transcript at (A82) and (A88). The static inverse of (A82) satisfies (A82); the printed (A88) leaves the residual ∂₂²u₁ − ∂₁²u₁ (symbolic check). The paper's own sentence after Figure 4 names ∂₂²u₁ and ∂₁∂₂u₂, that is, the (A82) form; the displayed (A88) does not match its own text. |
| For the paper's targets, the corrected inverse has no derivative terms (u₁ depends on n¹ only, u₂ on n² only) and reduces to u_{n−1} = 2.5u_n − u_{n+1}, giving u₀ = 2.13125; the quoted 0.1·(2/0.8)⁴ = 3.90625 drops the backward term. | agrees, and corrects the math examination | The README of this folder already listed 2.13 against the paper's "approximately 3" as open. The consequence for the math examination: its corner-difference finding (and this folder's item 5 in `math_exam_review.md`) applied the printed ∂₁² to the paper's sentence about ∂₂²; under the (A82) inverse the paper's sentence is exactly right. Corrected there. |
| The resonance threshold must be Ω² ≥ e²n̄/m; the printed Ω ≥ e²n̄/m compares an energy with an energy squared. | **adds**, and corrects this folder | (A13): ω_k = √(k² + e²n̄/m), so a real resonant k needs Ω² ≥ e²n̄/m. Mutation audit row U1 had repeated the printed form; corrected. At the §4 numbers the threshold is Ω ≥ 0.3 m, not 0.09 m. |
| (A31) χ₁ for χ₀; (A52) input for response; (A70) sign; (A76)/(A78) e for e². | agrees | Transcript notes; check 3; sibling check 1b. |
| The sech pulse is a solution of the reduced equation after the loss term and the adiabatic step, with θ₀, g, Ω, N, L₃ as inputs. | agrees | Check 2; self-audit S1; mutation audit rows R1, S1, T1. |
| (A13)'s ansatz does not derive an axially guided mode; the 21 nm cutoff needs a waveguide model; a conducting guide puts 500 nm below cutoff; dielectric guiding is not excluded. | agrees | Check 6 (pipe model and dielectric V ≈ 0.11); check 7. |
| Screening: T(n) = 1/(1 + 0.045n); the density change 1 → 0.79 changes T by 0.00873; 0.045 is a screening parameter, not an image amplitude. | agrees, with a number added | Check 5 and critique §4.2 (after Jeremy's review). The 0.00873 figure is re-derived in the script. |
| Capacity 2.6 PB and 31.25 TB; conditional counts, not usable capacity. | agrees | Mutation audit rows E2 to H2 (which add that the petabyte is the thickness factor). |
| Figure 6 shows increasing contrast, not erasure; retention needs a write-stop, a readout and a criterion. | agrees | Critique §7.2 (after Jeremy's review); mutation audit rows C2, Y2. |
| One-year retention under a single-barrier model: 1.199 eV (1 ps attempt) or 0.461 eV (1 s); a 1 % failure criterion raises these to 1.322 and 0.584 eV. | agrees, with a number added | Self-audit S3e; the reliability variant is re-derived in the script. |
| The 4 meV rotational scale is not the barrier and not the simulated mass. | agrees | Critique §7.2; mutation audit row B1. |
| Next result: one complete write–hold–read example with a classical comparator. | agrees | Mutation audit §6. |

## 2. Findings about this folder's critique

| Package claim | Verdict | Resolution |
|---|---|---|
| "Neglecting fluctuation contributions does not uniquely specify a coherent-product density operator"; first moments do not determine the marginals; so neither the marginal-product nor the coherent-state reconstruction is established as the paper's map. | **differs, accepted as a narrowing** | The critique's §6.1 reads the mean-field equations as the coherent-state reconstruction. That is the natural reading, not something the paper states. The §5.6 transfer bound (error ≥ D_e/3 against any product state) does not depend on which map is meant, so the critique's bound survives; its identification of the map is now marked as a reading. |
| The projection theorem needs a Hilbert-space decomposition, a cutoff, explicit interactions and an initial state before it certifies anything about Figure 6; the damping constant is not a Lindblad generator; the bound targets the state, not the readout observable. | agrees | Critique §6.2 says the toy shows the quantities exist, not their values; the paper never computes ν, g or the window. The observable-versus-state point is right and is the reason the mutation audit's comparator test defines a read first. |
| A nonzero correlation defect is not entanglement for mixed states. | agrees | The critique does not claim entanglement. |
| Dropping ∂β while holding A fixed changes the state; a gauge change does not. | agrees | Mutation audit row N2 (unitary gauge is exact when β is smooth). |
| Report-channel results (two states with one report get one verdict; pigeonhole needs \|X\| > \|P\|; equal joint likelihoods leave prior odds unchanged; equal marginals are not equal joint predictions) are conventions for this analysis, not laws about observers. | agrees | These are the sibling's finite results, stated there with the same scope. |

## 3. Its public replies

The package carries four plain posts and four variants, all under 500 characters. They are not used here; the posts for the thread are owned by `../01_thread/replies.md`. They are worth reading for one move this folder's posts also make: ask what counts as observing, and what changes without it.

## 4. What changed in this folder because of this package

1. Mutation audit row U1: threshold corrected to Ω² ≥ e²n̄/m.
2. Mutation audit rows K2, L2 and finding 7: "Gauss's law" narrowed to "the matter-charge Gauss law".
3. Math examination review, §11 and item 5: the corner-difference finding withdrawn as stated; it holds only for the printed (A88).
4. Mutation audit §7 records the three corrections; `../code/revised_review_checks.py` re-derives the (A88) mismatch, the 2.13 recursion, the Ω² threshold, the two-level density argument, and the package's three new numbers.

Two readings agreeing is still not evidence. Each line above names the check it rests on.
