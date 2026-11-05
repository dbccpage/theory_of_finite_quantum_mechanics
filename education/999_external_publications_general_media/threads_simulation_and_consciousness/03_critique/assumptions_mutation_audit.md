# Assumption mutation audit

**Paper.** Nishiyama, Tanaka, Tuszynski, Tsenkova, "Holographic Brain Theory: Super-Radiance, Memory Capacity and Control Theory", International Journal of Molecular Sciences 25(4):2399 (2024).

**Input.** The 78-row ledger in [assumptions_ledger.md](assumptions_ledger.md), forwarded by Jeremy on 2026-11-05 from another reviewer. The ledger is say-so. Nothing below is stronger because two reviews agree on it; each row says what it rests on.

**Method.** For every row: (1) find the claim in the paper's text and check the ledger's location and status; (2) mutate the assumption (negate it, or move it to the other plausible value); (3) try to recover the paper's claim under the mutation, using only the paper's own equations, the numbered checks of the companion script, and named outside results; (4) record the outcome.

Outcomes:

- **unchanged**: the mutation changes nothing the paper computes. The claim survives because it never depended on the assumption.
- **recovers, with a price**: the claim can be rebuilt, but only by adding something the paper does not supply (a term, a bound, a number, a different formula).
- **no recovery**: under the mutation the claim is gone and the paper offers no way back.

Tags: *supplied* (the paper declares it), *derived* (follows from something supplied), *witnessed* (computed here or reproduced in a rerun), *cited* (a result from outside the paper, named), *another review* (the ledger's own reading).

Location labels "(An)" are the paper's appendix equation numbers; "§n" its sections; "line" means the sentence around that equation. Where the ledger's location differs from the paper's text, the corrected location is given.

---

## 1. Corrections to the ledger before mutating

| Row | Ledger says | Paper says | Consequence |
|---|---|---|---|
| D1, E1 | "temporal gauge A⁰=0" and "transversality ∇·A=0" as two gauge/constraint items | The paper calls the pair "the Coulomb gauge" (line before (A2)). The Coulomb gauge fixes ∇·A=0 and leaves A⁰ to Poisson's equation; setting A⁰=0 as well is an extra condition, not a gauge choice. | The ledger's split is the right one. The paper's name for it is wrong. Both rows are supplied, not derived. |
| F1 | "time-independent integration term set to zero" | (A7) integrates ∂⁰J₀ = ∂⁰∂^νF_{ν0} in time; "time-independent terms that might represent boundary conditions are set to be zero". With A⁰=0 and ∇·A=0 the left side ∂^νF_{ν0} vanishes identically. | Two readings coexist. Integrated with the constant zero: J₀ = 0 (the ledger's "0 = J₀"). Differential form, constant kept: ∂₀J₀ = 0, the density is frozen, static, nonzero (check 1). Either way the oscillating coherence term in \|φ\|² that superradiance needs is excluded. |
| I1 | source "A11" | "We then adopt A₁ = A₂ = 0" is the sentence after (A10); (A11) is the A₃ equation that follows from it. | Location off by one sentence. Status "field restriction" stands. |
| M1 | "2D wavevector modes with k³=0", status "geometry restriction" | k = (k¹,k²,0) is set at (A13). With ∇·A=0 (E1) and A = (0,0,A₃) (I1), transversality reads k³A₃ = 0, so k³ = 0 is forced. | M1 is derived from E1 and I1, not an independent restriction. It cannot be mutated alone (see row). |
| Q1 | "collective identical coupling g and coherent phase", status "collective model" | In the dipole limit (P1) every emitter sees the same field, and the field locks the phases once a seed θ₀ ≠ 0 (T1) exists. | Q1 is derived given P1 and T1. Its obligations are theirs. |
| T1 | "initial angle θ₀ and integration origin", source A40–A47 | Section 2 says "definition of θ₀ is in Appendix A". Appendix A writes θ(x⁰) = θ₀ + 2g∫𝒜 at (A41) and uses θ₀ in (A44), (A47). No value, no origin t₀, no definition. | The ledger's "initial data" is right; the paper's cross-reference is empty. |
| P1 | "dipole limit exp(ik·x) ≈ 1", "small-system approximation" | Sentence before (A24): "the system size is sufficiently small compared with the wavelength of photons". Section 3 then takes a sheet 2 mm thick and 2500 cm² wide at λ = 500 nm. | The paper's own geometry violates its dipole limit by 4×10³ in thickness and 10⁵ in width, unless the emitters are sub-wavelength domains (the ledger does not note this). |
| C2 | "recording, retention, retrieval occur in brain tissue", "optical algebra cannot establish memory" | Section 4 and Appendix C drive \|φ\|² to a supplied target and show the density depression surviving, and deepening, after the field is gone (Figure 6: 1.3 % at m x⁰ = 5 to 21 % at 200, field zero by 200). | The ledger undercounts: in simulation the paper has a write and a retention. It has no read. |
| H2 | "~2.6 PB and ~31.25 TB unrounded" | 4·1.3·2 mm/(500 nm)³ × 2500 cm² = 2.08×10¹⁶ bit = 2.6 PB; 250×10¹² bit = 31.25 TB. | Witnessed: agrees. |
| S | "quantum collapse plays a role" | Section 5: "orchestrating the collapse of such qubits giving rise to a conscious event". | Present as the ledger says; it appears in no equation. |
| L | "microtubules as coherent optical emitters" | Section 5: "We have adopted microtubules as coherent super-radiant light sources ... Super-radiance suffers from the dephasing effect". | The paper itself names the dephasing obligation and does not discharge it. |

---

## 2. Row by row

Columns: the ledger's label; where the claim sits in the paper (checked); the ledger's status and whether this audit keeps it; the mutation; what happens when one tries to recover the paper's claim; outcome; what the row rests on.

### 2.1 Bridges to mind, memory and biology (A to V)

None of these rows appears in an equation. Every mutation leaves (A1) to (A91), Section 3 and Section 4 untouched. The point of mutating them is to see which claims of the paper were ever connected to a computed variable: none of these.

| Row | Checked location | Status (ledger → audit) | Mutation | Recovery attempt | Outcome | Rests on |
|---|---|---|---|---|---|---|
| A | §5: "a 'quantum mind' could bridge the gap between mind and brain" | conjecture → kept | Mind is brain activity, nothing separate. | Nothing in §2–4 changes. The "separate dynamical sector" names no variable, so it cannot be emptied either. | unchanged | §5 text (supplied) |
| B | §§1, 5, 6: "memory involving our subjective experience" | target undefined → kept | The target is pattern storage, not experience. | The paper improves: §3 and §4 become testable statements about storage. No report criterion is lost because none was given. | unchanged | §1 opening (supplied) |
| C | §5: "separate dynamical sector ... quantum brain" | conjecture → kept | The quantum sector is the water–photon field of Appendix A itself. | Then the two-way traffic of §5 needs a coupling between (φ, A) and neurons. (A1) has only U(x); no coupling term exists. | unchanged | (A1), §5 (supplied) |
| D | §§1, 5: "mixed system of classical neurons ... and quantum degrees of freedom" | model choice → kept | Everything is classical. | Appendix C already is: with Γ₂ = D¹¹ = 0 the equations are the Madelung pair of a classical charged fluid (check 3). §4 recovers in full. | unchanged | check 3 (witnessed) |
| E | §6: "the outside world of the observable phenomena and the inner life of our mind" | framing choice → kept | No outside/inside split. | §6's "where is the image formed" dissolves. Appendix B still needs a source for the object wave o (row A2). | unchanged | §6 text (supplied) |
| F | §6: "where is the image of the outside world formed inside the brain?" | open premise → kept | The brain forms no image. | (A52) still reconstructs o from \|r\|²o. The reconstruction has no job, and nothing else changes. | unchanged | (A52) (supplied) |
| G | §§1, 3, 5 | biological hypothesis → kept | Memory is synaptic; the hologram stores nothing biological. | §3 survives as the optical capacity of a 2 mm slab: still 2.6 PB. Only the word "memory" leaves. | unchanged | §3 eq. (3)–(4) (derived from supplied inputs) |
| H | §1: Lashley's dilemma, "degrees of freedom present in the entire brain" | inferential bridge → kept | Distributed memory is done by distributed synaptic coding. | No equation uses the premise. Motivation leaves, mathematics stays. | unchanged | §1 (supplied) |
| I | §1 | inferential bridge → kept | Synaptic processing suffices. | As H. | unchanged | §1 (supplied) |
| J | §1, (A1)–(A2): "modeling dynamics of water molecular conformational states" | biological hypothesis → kept | φ is any charged boson with discrete levels. | Water enters one number only: molecules per λ³ (check 11). Nothing in (A1)–(A91) uses a property of water. | unchanged | (A1) text; check 11 (witnessed) |
| K | §1: photons and water as the "main actors" | biological hypothesis → kept | The carrier is a phonon field, not light. | (A3) becomes a different wave equation; superradiance of other boson fields exists as a cited phenomenon, but the §3 capacity then uses that field's wavelength and changes by λ⁻³. | recovers, with a price | §3 eq. (3) (derived); outside result (cited, unnamed here) |
| L | §5: microtubules adopted as sources; dephasing admitted | biological hypothesis → kept | Microtubules emit nothing. | Appendix A never uses microtubule geometry. The emitter size enters only through the dipole limit (P1). | unchanged | §5 line, (A24) preface (supplied) |
| M | §1 quotes a 10⁻¹³ s decoherence time; §5 | required mechanism unverified → kept | Coherence lasts at most 10⁻¹³ s. | Superradiance needs τ_R = 2π/(g²ΩN) shorter than that; g and Ω are never given, so it cannot be checked. Retention over seconds cannot be quantum. Section 4 is untouched by the mutation because Appendix C is classical (check 3). | recovers, with a price | (A47); check 3 (witnessed); §1 decoherence figure (cited by the paper) |
| N | §§1, 5 | bridge → kept | Correlations implement no cognition. | No variable changes. | unchanged | §1, §5 (supplied) |
| O | §§3, 5 | encoding bridge absent → kept | Patterns encode nothing. | Capacity stays; (A52) still returns o. | unchanged | §3, (A52) |
| P | §§3, 5–6; the "headset" of §5 | missing mechanism → kept | A readout exists. | It must then be a map from A or \|φ\|² to a report. The paper offers one candidate, an external headset, which is outside the brain. Nothing internal reads the record. | no recovery | §5 (supplied) |
| Q | §5 | bridge unproved → kept | Collective emission has nothing to do with consciousness. | §2 unchanged. | unchanged | §5 (supplied) |
| R | §5: "directed actions commanded by the quantum mind" | conjectured causal bridge → kept | Intention causes nothing. | No equation involved. | unchanged | §5 (supplied) |
| S | §5: "orchestrating the collapse of such qubits" | discussed hypothesis → kept | Collapse plays no role. | Collapse appears in no equation (A1)–(A91). | unchanged | §5 (supplied) |
| T | §§5–6; the four operations (register, decipher, decide, encode) | not supplied → kept | An observer is specified: a presentation (which variable is read), a memory, an evaluator, a policy. | The paper supplies at most the presentation candidate, \|φ\|² of Figure 6. The other three layers have no variable. The four operations of §5 are the rungs of an observation ladder with no carrier under them. | no recovery | §5 list (supplied); observer packet definition (cited, companion) |
| U | §5 | biological bridge untested → kept | Control does alter memory. | Then the record is \|φ\|² and the write exists in simulation (row C2). A read is still missing (row P). | recovers, with a price | Figure 6 (supplied); row C2 |
| V | §§5–6 | phenomenological bridge untested → kept | Control alters experience. | No variable stands for experience; nothing to recover with. | no recovery | §5–6 (supplied) |

### 2.2 Framework and model admissions (W to C1)

| Row | Checked location | Status (ledger → audit) | Mutation | Recovery attempt | Outcome | Rests on |
|---|---|---|---|---|---|---|
| W | §1 framework; (A1) | standard framework → kept | Spacetime is a lattice. | §4 is computed on a lattice already (a_s = 1/m, 128², periodic). Only the Appendix A–C derivations use the continuum, and their ∫_k become sums. | unchanged | §4 setup (supplied) |
| X | natural units | convention → kept | Restore ħ. | ħ reappears in one place: the Bohm term, the only quantum term in Appendix C (check 4). Harmless. | unchanged | check 4 (witnessed) |
| Y | (A1) | chosen model → kept | Replace the quantum Lagrangian by a classical charged fluid. | Appendix C: identical equations (check 3). Appendix A: Maxwell–Bloch for classical two-level oscillators gives the same (A36)–(A38); what a classical model cannot supply is the seed θ₀ (row T1). | recovers, with a price | check 3 (witnessed); (A36)–(A38) |
| Z | (A1)–(A2) | physical identification → kept | φ is not water. | As row J. | unchanged | check 11 |
| A1 | e appears numerically only in §4 (e = 0.3) | parameter admission → kept | e → 0. | Appendix A: g ∝ e, τ_R → ∞, no pulse. §4: matter and field decouple, the e²A² term in the matter equation vanishes, no density depression. The 21 % is an e-dependent response (row T2). Nothing in the paper fixes e. | no recovery | (A24), (A47), (A81)/(A87) (supplied) |
| B1 | m appears only as the unit of §4 | parameter admission → kept | Read m two ways. | m = 4 meV (the §1 figure): a_s = ħc/m = 49 µm, the lattice is 6.3 mm, M = 5.7 meV, γ = 0.8 meV. m = the mass of a water molecule: a_s ≈ 10⁻¹⁷ m. The paper never says which (check 9). | no recovery | check 9 (witnessed) |
| C1 | (A1) U(x); (A8)–(A9) "conformational energy E_n (for vibrational motion, and so on)" | model admission → kept | U = 0. | Continuous spectrum, no discrete levels, (A8) has no basis, no two levels, no superradiance. Appendix C does not contain U, so §4 survives. | no recovery (Appendix A); unchanged (§4) | (A1), (A9) (supplied) |

### 2.3 Superradiance (D1 to U1)

| Row | Checked location | Status (ledger → audit) | Mutation | Recovery attempt | Outcome | Rests on |
|---|---|---|---|---|---|---|
| D1 | line before (A2): "A⁰ = 0 and ∇_iA_i = 0", called Coulomb gauge; (A7) | gauge/constraint → supplied, misnamed | Keep ∇·A = 0, let A⁰ obey Poisson's equation ∇²A⁰ = −J₀ (the actual Coulomb gauge). | (A7) stops saying 0 = J₀. The density is free to oscillate, the coherence R and the pulse of (A38) return. Price: a Coulomb term eA⁰ enters (A2) and the chain (A24)–(A38); it is a mean-field term of order e²N/L and the paper would have to show it is negligible. | recovers, with a price | (A2)–(A7); check 1 (witnessed) |
| E1 | same line | gauge/constraint → kept | Keep A⁰ = 0, drop ∇·A = 0 (temporal gauge). | (A7) becomes −∂₀(∇·A) = J₀: a longitudinal part of A carries the charge. The transverse plane waves of (A13)–(A17) need a longitudinal mode added, and Gauss's law becomes a constraint on initial data, which reopens F1. | recovers, with a price | (A7); standard temporal-gauge treatment (cited, generic) |
| F1 | line after (A7) | boundary admission → kept | Keep the time-independent term. | J₀ = ρ₀(x), static. The density is frozen rather than zero (check 1 reads it this way; the ledger reads J₀ = 0). Both exclude the oscillating \|φ\|² cross term b₀b₁*φ₀φ₁* that the superradiant coherence is. | no recovery | (A5)–(A7); check 1 (witnessed) |
| G1 | (A8)–(A9), Σ\|b_n\|² = N | model admission → kept | Normalize to 1. | N moves from the normalization into g; τ_R = 2π/(g²ΩN) keeps its form with g rescaled. Nothing lost. The ledger's point stands: "N water molecules" needs the spectrum of C1. | unchanged | (A9), (A47) |
| H1 | (A10) | approximation → kept | Isotropic gradients. | J_i has three components, the one-component reduction fails, and the vector Maxwell–Bloch system replaces it (a standard form). Superradiance survives; the dispersion (A13) and the sideways, axially polarized emission (check 7) change to a dipole pattern. | recovers, with a price | (A10)–(A13); check 7 (witnessed) |
| I1 | sentence after (A10) | field restriction → kept (location corrected) | Keep A₁, A₂. | As H1. Note that dropping I1 also removes the reason for M1. | recovers, with a price | (A11) |
| J1 | (A8)–(A12) | truncation → kept | Three levels. | Cascade superradiance exists (cited, generic); the sech form (A45) is not exact and (A47) fails, but N² scaling per transition survives. | recovers, with a price | (A12), (A45) |
| K1 | (A12): Ω = E₁ − E₀ | model parameter → kept | Ω differs across emitters by δΩ. | Superradiance needs τ_R < 1/δΩ. The paper names the dephasing problem (§5) and gives neither τ_R nor δΩ. No number, no recovery. | no recovery | (A47); §5 dephasing sentence (supplied) |
| L1 | line before (A14): "rotating-wave approximation where we leave only resonant mode" | approximation → kept | Keep the counter-rotating terms. | Valid when g√N ≪ Ω (Bloch–Siegert regime, cited, generic). Neither g nor Ω is given. | recovers, with a price | (A14)–(A17) |
| M1 | (A13): k = (k¹,k²,0) | geometry restriction → derived from E1 + I1 | k³ ≠ 0 alone. | Not possible: with A = (0,0,A₃) and ∇·A = 0, k³A₃ = 0. To mutate M1 one must first mutate I1. | unchanged (not independent) | (A13), ∇·A = 0 |
| N1 | (A19): Fourier dominance l ~ k | approximation → kept | Keep all modes. | The mode equations couple through the spatial structure of \|φ̄\|². The paper takes \|φ̄\|² = N/V uniform (A13), and for a uniform background the modes decouple exactly. | unchanged (given uniform background) | (A13), (A19) |
| O1 | (A20)–(A23) | approximation → kept | Keep second derivatives. | (A23) becomes the full wave equation; Maxwell–Bloch with the full wave equation still gives superradiance (cited, generic). The sech pulse is its mean-field limit. | recovers, with a price | (A23) |
| P1 | sentence before (A24) | small-system approximation → kept, and in conflict with §3 | System size ≫ λ. | Phases e^{ik·x} no longer cancel; superradiance in an extended sample is directional with a rate set by the domain's N and λ²/A (cited, generic). The paper's τ_R would use the N of a sub-wavelength domain, not the brain's. Phase locking across domains, which the hologram's coherent source needs, is not supplied. | recovers, with a price | (A24) preface; §3 geometry (supplied) |
| Q1 | (A24)–(A38) | collective model → derived from P1 + T1 | Random emitter phases. | Intensity ∝ N, the sech pulse goes. Recovery is the standard one: in the dipole limit the common field locks the phases once seeded. So Q1 falls or stands with P1 and T1. | unchanged (not independent) | (A24)–(A38) |
| R1 | (A42): loss 𝒜/L₃ added "setting the length L₃" | geometry + phenomenological term → kept | No loss (L₃ → ∞); then finite L₃. | Without loss (A36)–(A38) conserve the Bloch length and θ oscillates (Rabi); with finite L₃ the field equation is a damped pendulum. The sech (A45) is obtained only as L₃ → 0 (check 2), the opposite of a thick slab. | no recovery | (A36)–(A45); check 2 (witnessed) |
| S1 | line before (A43): ∂₀ ≪ 1/L₃ | approximation → kept | ∂₀ comparable to 1/L₃. | Second-order equation for θ; sech only in the overdamped limit. Same as R1. | no recovery | (A42)–(A43); check 2 |
| T1 | (A41), (A44), (A47) | initial data → kept | θ₀ = 0; θ₀ = π. | θ₀ = 0: τ₀ = ∞, no pulse. θ₀ = π: τ₀ = −∞, the pulse is already past. The usual seed is θ₀ ~ 2/√N from the vacuum (cited, generic), which the paper neither states nor uses. | recovers, with a price | (A41)–(A47) |
| U1 | after (A47): "necessary condition Ω ≥ e²\|φ̄\|²/m" | derived condition, unchecked → kept, and misprinted | Violate it. | ω_k ≥ √(e²\|φ̄\|²/m) for all k by (A13), so a resonant mode needs Ω² ≥ e²\|φ̄\|²/m; the printed condition compares an energy with an energy squared (correction from the revised outside review). With the §4 numbers e²\|φ̄\|²/m = 0.09 m², so Ω ≥ 0.3 m; Ω is never given, so the condition cannot be checked. | no recovery | (A13), (A47) (supplied); `../code/revised_review_checks.py` |

### 2.4 Holography and capacity (V1 to H2)

| Row | Checked location | Status (ledger → audit) | Mutation | Recovery attempt | Outcome | Rests on |
|---|---|---|---|---|---|---|
| V1 | (A48): "we have added the term M²A_i ... by ionic bioplasma" | added term → kept | M² = 0; then M² → ∞. | M² = 0: the forcing of (A48) is M²Ã, so the external wave stops entering at all, and (A49) divides by zero. M² → ∞: A → Ã exactly, screening s = e²\|φ\|²/(M²m) → 0 and the image term vanishes. The image lives only in a window of M², and its size is bounded by s (0.045 at the §4 numbers, check 5). | no recovery | (A48)–(A49); check 5 (witnessed) |
| W1 | (A48)–(A50) | input admission → kept | No external wave. | Only the homogeneous solution remains; no reconstruction. | no recovery | (A48) |
| X1 | (A48)–(A49): O(∂φ, ∂φ*) dropped | approximation → kept, unbounded | Keep the gradient terms. | ∇·A = 0 then requires the density gradient perpendicular to the polarization: fine for a pattern in (x¹,x²) with A₃ polarization. The size of the correction needs a length scale; Appendix B gives none. | recovers, with a price | (A48)–(A49); check 1 (witnessed) |
| Y1 | line before (A50): "2-dimensional surface ... with thickness" | geometry choice → kept | Surface only, d → 0. | Capacity becomes 4/λ² × 2500 cm² = 4×10¹² bit = 0.5 TB, below the paper's own synaptic baseline (31 TB). The 2.6 PB rests entirely on the thickness factor n_r d/λ = 5200. | no recovery | §3 eq. (3) (derived); arithmetic (witnessed) |
| Z1 | (A50) | input assumed → kept | No reference wave. | (A52) is zero. | no recovery | (A50)–(A52) |
| A2 | (A51): o has no equation | input assumed → kept | o is generated inside: o = the field's own A. | (A51) becomes a self-consistency condition, \|φ\|² ∝ \|r + A\|² with A depending on \|φ\|² through (A49). A fixed-point problem the paper does not pose. With o = 0: A ∝ r\|r\|², no image. | no recovery | (A49)–(A52) |
| B2 | (A51) | hologram premise → kept | \|φ\|² constant; then \|φ\|² ∝ \|o\|². | Constant: A = (1 − s)Ã, screening only. ∝ \|o\|²: A ∝ r\|o\|², no \|r\|²o term. The image term exists exactly when the cross term r*o + ro* has been written into the medium, which is what B2 assumes and C2 asks for. | no recovery | (A49)–(A52); check 5 |
| C2 | §§3, 5; and §4 | mechanism not demonstrated → partly demonstrated in simulation | A write mechanism is present. | The candidate is Section 4: supplied inputs drive \|φ\|² to a target, and Figure 6 shows the depression persisting and deepening after the field is gone. Write and retention exist in the classical simulation; the read does not, and the "hologram" is a continuous density dip of 1.3 % to 21 %, not a binary record. | recovers, with a price | Figure 6, §4 (supplied); PR #517 rerun (witnessed by another thread) |
| D2 | §3 eqs. (6)–(9), Lohmann binary holograms | engineering design → kept | Grey-scale hologram. | §3's 4/λ² does not use the binary scheme. Nothing else depends on it. | unchanged | §3 eq. (3) |
| E2 | §3 eq. (3): 4/λ² | optical estimate → kept | 1/λ² instead. | 0.65 PB instead of 2.6 PB. The petabyte order survives; the factor 4 rests on one sentence about radiation angles. | recovers, with a price | §3 line before eq. (3) (supplied) |
| F2 | §3 eq. (3): n_r = 1.3, d = 2 mm | numerical inputs → kept | d = 1 mm; n_r = 1.4. | 1.3 PB; ×1.08. Survives at PB order, but see Y1: d is the whole advantage. | recovers, with a price | arithmetic (witnessed) |
| G2 | §3 eq. (4): λ = 500 nm, 2500 cm² | numerical inputs → kept | λ = 1500 nm (the paper's own §5 near-infrared figure). | 0.096 PB; the paper's §5 says "about 0.1 PB" for this case. Survives at 0.1 to 2.6 PB. | recovers, with a price | §3, §5 (supplied); arithmetic (witnessed) |
| H2 | §3 eq. (5): 250×10¹² synapses, 1 bit each | comparison baseline → kept | 4.7 bits per synapse (a published estimate from reconstructed hippocampal synapses; cited, outside the paper). | 147 TB; the ratio drops from 80 to 17. Combined with Y1 (surface only, 0.5 TB) the advantage reverses. The sign of the comparison depends on d and on bits per synapse. | recovers, with a price | eq. (5) (supplied); arithmetic (witnessed); outside estimate (cited) |

### 2.5 Control theory and simulation (I2 to Z2)

| Row | Checked location | Status (ledger → audit) | Mutation | Recovery attempt | Outcome | Rests on |
|---|---|---|---|---|---|---|
| I2 | (A53)–(A55): background field gauge, ā set to 0 | formalism choice → kept | No background/fluctuation split. | The mean-field equations with ā = 0 are the same. | unchanged | (A53)–(A62) |
| J2 | (A56)–(A61) | formal machinery → kept | Skip the 2PI action; write the classical field equations from (A1) plus M² and γ by hand. | Identical to (A76)–(A81) (check 3). The machinery does no work in §4. | unchanged | check 3 (witnessed) |
| K2 | (A62)–(A75): Γ₂ "higher order", D¹¹ neglected | truncation → kept | Γ₂ = 0 with no M² and no γ. | Gauss's law then holds in the pure Maxwell part and nothing relaxes: the target is not reached (the paper: "due to damping"). The terms that replace Γ₂ are the ones that make §4 work, and they are also the ones that break Gauss's law for the matter charge: ∂₀(∇·E − ρ_m) = ∇·S with S the M², γ and v terms, and the rerun measures a residual of 1.1 to 2.3 times the charge change. A medium or external charge could absorb that residual; the paper supplies none. | no recovery | (A75); sibling check 1a and PR #517 rerun (witnessed by another thread) |
| L2 | (A75): Σ ≃ −M² − γ∂₀, "factors dependent on T and e" | effective approximation → kept | M² = 0, γ = 0; then γ larger. | As K2. A larger γ relaxes faster; the dip size under it is not in the paper and needs a rerun. | no recovery | (A75) |
| M2 | line before (A76): A₃ = 0, homogeneity in x³ | geometry reduction → kept | Keep A₃ and x³. | The layer hierarchy of §4 is a one-cell-per-layer discretization of x³ with A₃ dropped and v as the coupling. A 3D run would also carry the ∂₃ part of the Gauss residual. Partial recovery at best. | recovers, with a price | (A76), (A82) |
| N2 | (A76)–(A81): "we omit terms −∂_μβ/e" | simplification → kept | Keep the phase β. | A − ∂β/e is the gauge-invariant combination, so dropping β is the unitary gauge, exact when β is smooth. The run starts uniform with zero field, so no vortices. Recovers in full; the e versus e² misprint in (A76)/(A78) stays. | unchanged | (A76)–(A81); sibling check 1b (witnessed by another thread) |
| O2 | §4, (A82)–(A87) | model transfer → kept | Layer-specific coefficients (fluid, membrane, bone). | The inversion (A88) is linear per layer, so it works with any coefficients; the gain 0.1·2^N/0.8^N becomes a product of per-layer ratios. Formal recovery; the numbers change. | recovers, with a price | (A82)–(A88) |
| P2 | (A82): v(A^{(n−1)} + A^{(n+1)}) | chosen coupling → kept | v = 0; then all-to-all. | v = 0: layers decouple, the input never reaches layer N. All-to-all: the inversion changes. Any known v works because the drive is designed from v (W2). | recovers, with a price | (A82), (A88) |
| Q2 | §4: N = 4, u^{(N+1)} = 0 | simulation setup → kept | N = 1; N = 8. | Gain 0.25; 153. The input needed grows by 2/0.8 per layer. Formal recovery. | recovers, with a price | §4 gain formula (supplied); arithmetic (witnessed) |
| R2 | §4: 128², periodic | numerical setup → kept | Dirichlet boundary. | The polygonal targets near the edge change; needs a rerun. | no recovery (untested) | §4 setup |
| S2 | §4: a_t/a_s = 0.001, RK4 | numerical method → kept | a_t/a_s = 0.01. | Still far inside the 2D wave stability limit 1/√2. The paper reports no convergence test; the rerun used the same ratio, so the step is not independently verified. | recovers, with a price | §4 setup; PR #517 rerun (another thread) |
| T2 | §4: e = 0.3, v/m² = 0.8, γ/m = 0.2, M² = 2m² | free parameters → kept | e → 0. | The e²A²/2m term leaves the matter equation; the density stays at 1; no depression. The 21 % is the matter's response to the field's intensity, an e-dependent effect. | no recovery | (A81)/(A87) structure; check 4 (witnessed) |
| U2 | §4: γ₂/m = 0.01; (A90)–(A91) e^{−γ₂x⁰} | imposed input history → kept | γ₂ = 0; γ₂ large. | γ₂ = 0: the input never stops and the field never vanishes, so "the record outlives the field" cannot be tested. γ₂ large: the input is gone before the target forms. | no recovery | (A90)–(A91), Figure 5 |
| V2 | §4 eqs. (10)–(11): three polygonal lines, ±0.1, N₁ = 30, N₂ = 20 | designed target → kept | Any other smooth target. | (A88) inverts linearly; it works. Nothing is specific to the polygon, and nothing is discovered. | unchanged | (A88) |
| W2 | (A88)–(A89): static inversion "neglecting time derivatives and the matter term" | inverse construction → kept | Forward (random) drive; then include the matter term in the inversion. | Random drive: no target. Including the matter term: the "slightly distorted" Figure 5 is the price the paper already pays for omitting it. Open-loop inverse design, not learning. | no recovery | (A88)–(A89); Figure 5 text (supplied) |
| X2 | §4: \|φ̄\| = 1, A = E = 0 | initial conditions → kept | Random initial density. | (A88) omits the matter term, so the drive is the same, and the field equation's e²\|φ\|²A term then differs point by point. Needs a rerun. | no recovery (untested) | (A88), (A82) |
| Y2 | §4, Figure 6 | interpretation bridge → kept | Call it a density depression. | Nothing in the paper distinguishes the two names: no read-out, no binary threshold (values 1.3 % to 21 % are continuous). | unchanged | Figure 6 (supplied) |
| Z2 | §§4–6 | biological bridge → kept | Fix the scale. | At m = 4 meV the slab is 6.3 mm wide (row B1), cortex-like; at other readings of m it is microns or 10⁻¹⁷ m. Without m the extrapolation has no length. | no recovery | check 9 (witnessed) |

---

## 3. What the mutations found that the ledger did not

1. **The gauge pair can be rescued, at a price (D1).** The superradiance branch dies under A⁰ = 0 with ∇·A = 0 because (A7) then reads 0 = J₀ (ledger) or ∂₀J₀ = 0 (check 1). Replacing A⁰ = 0 by Poisson's equation restores the coherence and the pulse, and adds a Coulomb term of order e²N/L to (A2) that the paper would have to bound. The ledger stops at "inconsistency as written"; the repair exists and has a cost.
2. **Two rows are derived, not supplied (M1, Q1).** k³ = 0 follows from transversality with a single polarization; identical coupling with a locked phase follows from the dipole limit with a seed. The ledger counts 25 superradiance imports; two of them are consequences of others.
3. **The dipole limit contradicts the §3 geometry (P1).** A 2 mm by 2500 cm² sheet at 500 nm is not "sufficiently small compared with the wavelength". The emitters must be sub-wavelength domains, and then τ_R uses a domain's N and the coherence across domains is unsupplied.
4. **The petabyte is the thickness (Y1, H2).** 4/λ² over the area is 0.5 TB. The factor n_r d/λ = 5200 turns it into 2.6 PB. With a surface hologram and 4.7 bits per synapse the comparison reverses.
5. **The external wave enters only through M² (V1).** With M² = 0 the hologram's forcing vanishes; with M² large the image vanishes. The image amplitude is bounded by the screening parameter, 0.045 at the §4 numbers.
6. **Section 4 has a write and a retention, not only "optical algebra" (C2, U).** The classical simulation writes a supplied target into \|φ\|² and the record outlives the field. It has no read. The decoherence objection (M) does not touch it, because nothing in Appendix C is quantum (check 3).
7. **The terms that make §4 work are the terms that break the matter-charge Gauss law (K2, L2).** Without M² and γ nothing relaxes to the target; with them the matter charge is not conserved by the field equations, at 1.1 to 2.3 times the charge change in the rerun. The paper names no medium charge to take up the difference.
8. **The 21 % is e-dependent (T2, A1).** Set e = 0 and the depression is gone. The "memory" of Figure 6 is the matter's response to the field intensity. That is a candidate for the classical comparator, not an argument against the paper.
9. **One paper cross-reference is empty (T1).** "Definition of θ₀ is in Appendix A": Appendix A uses θ₀ and never defines it.

Items 1, 3, 4, 5 and 8 are witnessed here by arithmetic on the paper's own expressions. Item 7 rests on another thread's rerun. Items 2, 6 and 9 rest on the paper's text.

---

## 4. Tally

| Outcome | Rows |
|---|---|
| unchanged | A, B, C, D, E, F, G, H, I, J, L, N, O, Q, R, S, W, X, Z, G1, M1, N1, Q1, D2, I2, J2, N2, V2, Y2 (29); C1 for §4 only |
| recovers, with a price | K, M, U, Y, D1, E1, H1, I1, J1, L1, O1, P1, T1, X1, C2, E2, F2, G2, H2, M2, O2, P2, Q2, S2 (24) |
| no recovery | P, T, V, A1, B1, C1, F1, K1, R1, S1, U1, V1, W1, Y1, Z1, A2, B2, K2, L2, R2, T2, U2, W2, X2, Z2 (25) |

Twenty-nine rows change nothing the paper computes: the claims they carry were never attached to a variable. The ledger's "what changes" column says this row by row; the tally says it once.

The ledger's category counts (biology 22, superradiance 25, holography 13, control 18) are the other reviewer's; they sum to 78 and are not re-derived here.

---

## 5. The five erasures, re-checked

| Erasure | Ledger's claim | Audit |
|---|---|---|
| Superradiance (A24)–(A47) | Maxwell–Bloch and the conditional sech survive; no site or content derived. | Agreed, with two additions: the sech needs L₃ → 0 (R1, S1), and the whole branch needs the gauge pair repaired (D1) or it has no coherence to radiate. |
| Holography (A48)–(A52) | The central import is (A51); the object wave and the encoding are not produced. | Agreed. Added: the image amplitude is bounded by the screening parameter and vanishes at both ends of M² (V1). |
| Capacity §3 | Arithmetic survives for supplied inputs; the biological channel is not linked. | Agreed. Added: the thickness factor is the whole petabyte (Y1); the synaptic baseline is at the low end of published estimates (H2). |
| Control (A53)–(A91) | The driven PDE and the 21 % survive; the target was built into the input. | Agreed. Added: the simulation is classical (check 3), the relaxation terms break charge conservation (K2), and the depression is e-dependent (T2). It does contain a write and a retention (C2). |
| Quantum mind §5 | No derived variable tests consciousness, an observer, a memory identity or experience. | Agreed. The four operations of §5 are rungs without a carrier (T); the only read-out candidate is an external headset (P). |

The ledger's Appendix A finding (0 = J₀) and its Appendix C finding (classical form) coincide with checks 1 and 3 of the companion script. That coincidence is two readings of the same equations, not two pieces of evidence; the checks are what the findings rest on.

---

## 6. The next test: a classical comparator

The ledger's "no-go needed" asks what a purely classical model cannot reproduce. Rows D, Y, J2 and T2 give the shape of the test, and most of it already exists in the paper:

1. **Comparator.** The Madelung pair (A69)–(A71) with Γ₂ = D¹¹ = 0, the Bohm term removed, M² and γ kept, on the same 128² periodic lattice with the same targets, inputs and parameters. Check 3 shows this is Appendix C minus one term.
2. **Prediction.** The Bohm term is the only ħ in Appendix C and the paper itself calls it a distortion. Check 4 bounds it against the e²A² term at the Figure 6 edge. If the comparator reproduces Figure 5 and Figure 6 within that bound, the paper's numerical result is classical.
3. **Variations.** e ∈ {0, 0.1, 0.3, 1}; M² ∈ {0, m², 2m², 10m²}; γ, v, γ₂ around the paper's values; two more targets; a Dirichlet boundary (R2); a random initial density (X2).
4. **Retrieval task.** Define a read: a map from the final \|φ\|² to the supplied target (for example, the correlation with the polygonal pattern). Report it for the paper's model and the comparator. Without a read there is no memory claim to compare (P, Y2).
5. **Gauss residual.** Report ∂_iE_i − J₀ alongside, as the rerun did, for both models.

What the test can decide: whether anything in Figures 5 and 6 depends on the one quantum term. What it cannot decide: anything in rows A to V, which no simulation touches.

---

## 7. Corrections after the revised outside review (2026-11-05)

- Row U1: the resonance threshold is Ω² ≥ e²\|φ̄\|²/m, not Ω ≥ e²\|φ̄\|²/m; the printed form is dimensionally inconsistent and this audit had repeated it.
- Rows K2, L2 and finding 7: "break Gauss's law" now reads "break the matter-charge Gauss law"; an unspecified medium charge could absorb the residual, and the paper specifies none.
- Row W2 gains a fact: (A88)/(A89) as printed carry −∂₁²u₁ and −∂₂²u₂ where (A82)/(A84) give −∂₂²u₁ and −∂₁²u₂; for the paper's targets the correct inverse has no derivative terms and gives an input amplitude of 2.13, not the quoted 3.9. See `revised_review_check.md`.

## 8. Companion references

Checks are numbered as in `../code/critique_checks.py` (run from the folder above with `python -I code/critique_checks.py`; last output in `../code/critique_checks_output.txt`). "Sibling check 1a/1b" are in `../code/adversarial_review_checks.py`. The Appendix C rerun and its Gauss residual are in `../04_self_audit/retest_log.md` and `../04_self_audit/self_review.md` (PR #517). The projection-obstruction and observer-packet material the critique uses is in `critique_wdp_po.md`, with its own companion list. The paper's transcript used for every location check is `../02_paper/ijms-25-02399.md`; equation labels follow the published appendices. The 4.7 bits-per-synapse figure is from a published reconstruction study of hippocampal synapses and is the only number here taken from outside the paper and this folder.
