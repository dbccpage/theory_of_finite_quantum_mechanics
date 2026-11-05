# The holographic brain paper, taken apart and put back together

Nishiyama, Tanaka, Tuszynski, Tsenkova, "Holographic Brain Theory: Super-Radiance, Memory Capacity and Control Theory", *International Journal of Molecular Sciences* 25(4):2399 (2024).

This is written for a reader who has not seen the paper and does not want to take anyone's word for it. Every statement below is one of three kinds, and says which:

- **the paper shows**: an equation or a number that follows from what the paper wrote down, and can be checked by anyone with the paper open;
- **the paper assumes**: something written down without an argument, which the rest depends on;
- **the paper claims**: a sentence that goes beyond anything shown or assumed.

Equation labels such as (A51) are the paper's own, from its appendices. Section numbers are the paper's. Nothing here depends on any theory of ours. Anyone who thinks a line below is wrong can refute it by pointing at the line in the paper that settles it.

A short version of the whole thing: the paper contains four separate calculations and one story. The calculations are a light pulse from a medium of two-level emitters, an optical hologram, a storage-capacity count, and a computer simulation of a driven field on a grid. The story is that these are memory and experience in a brain. The calculations have errors, some fixable at a price. The story is never connected to the calculations by a single equation. The paper's own last sentences agree: it says how a quantum mind perceives the world is "yet another mystery altogether", and it proposes the connecting experiment as future work.

---

## 1. Section 5, the Discussion, sentence by sentence

Section 5 is where the paper says what its mathematics means. This is the section to read most carefully, because it is where things enter that were not in the mathematics.

### 1.1 "The existence of a 'quantum mind' could bridge the gap between mind and brain"

**The paper claims.** A "quantum mind" is introduced as "a separate dynamical sector" that "would determine the state of the brain at a quantum level", "could access the sensory inputs", and "would affect the macroscopic classical brain and result in directed actions".

What this would need. A sector is a set of variables with its own equations and a coupling to the other variables. The paper's model has exactly two kinds of variable: a charged field φ (its "water") and the electromagnetic potential A (its "light"). Their equations are (A2) and (A3). Nothing in them is called a mind, receives a sensory input, or produces an action. The only external term in the whole paper is the potential U(x) in (A1), which is never specified.

So the "separate sector" has no variable, and the two-way traffic (inputs in, actions out) has no coupling term. The sentence is a description of a model the paper does not write down.

### 1.2 The paragraph on wave-particle duality, blurred boundaries, collapse and uncertainty

**The paper claims.** Quantum systems "act as a whole", have "blurred" boundaries, "occupy multiple physical states simultaneously", collapse "through interaction with its environment or spontaneously", are "never completely knowable", and these are "attractive properties for implementation in the context of understanding the human mind".

This paragraph is about quantum mechanics in general. None of its properties is used anywhere in the paper's equations. In particular:

- collapse appears in no equation from (A1) to (A91);
- the one calculation that is run on a computer (Section 4, Appendix C) is, after the paper's own truncations, a set of classical field equations. Appendix C starts from a quantum formalism and then drops every term that distinguishes it from a classical charged fluid, keeping one: a term the paper itself calls a "distortion" (Section 5, the control paragraph). We come back to this in Section 4.4 below.

"Attractive properties" is not an inference. That quantum systems are hard to know fully does not make them a mind, any more than it makes a laser one.

### 1.3 The four steps: register, decipher, decide, encode

**The paper claims.** "A quantum mind would have to: 1. Register quantum level changes in neurons caused by sensory inputs, 2. Decipher this information and translate into high-level concepts, 3. Make a decision on the quantum level about the reaction to the inputs, 4. Encode that decision back into the quantum level to produce a macroscopic effect."

This is a correct list of what any account of perception and action has to supply. It is also, read against the paper, a list of four things the paper does not have. Each step is an operation. An operation needs a carrier: a variable that changes when the operation happens. Go through the paper's variables:

| Step | Would need | What the paper has |
|---|---|---|
| Register | a term through which a sensory signal changes the model's state | no input term; U(x) is unspecified and fixed |
| Decipher | a map from a state of the model to a "concept" | nothing; "concept" occurs here only |
| Decide | a rule that selects an action from a state | nothing |
| Encode | a term through which the model's state drives an effector | nothing |

The paper says as much in the sentence that opens the paragraph containing the list: "how a quantum mind could perceive the macro-world is yet another mystery altogether". The list is an honest statement of the debt. It is not a result.

### 1.4 "Manipulating holograms by external electric fields, we might be able to affect our memory and subjective experiences"

**The paper shows** (Section 4, Appendix C): on a 128 × 128 periodic grid, four identical copies of a damped, screened field equation, coupled in a chain, driven at one end by an input that was computed backwards from a chosen target, reach a field close to that target (Figure 5) and produce a dip in the field φ's density in the shape of the target, growing from 1.3 % to 21 % over the run (Figure 6).

**The paper claims** that this is "affecting our memory and subjective experiences".

Three things are imported in that one step, none of them from the mathematics:

1. that the density dip in φ is a memory. In the model it is the response of a charged fluid to the intensity of the field driving it: switch the coupling e to zero and the dip is gone, because the term that produces it is proportional to e²;
2. that a memory in the model would be a memory of something. The target was a shape the authors chose (three line segments, the paper's "3 polygonal lines", equations (10) and (11)). Nothing was learned, recognised, or recalled; a pattern was written by a drive designed to write it;
3. that a memory is an experience. No variable in the paper stands for an experience, so nothing can be said to change one.

The sentence "artificial memory induced by external electromagnetic fields might be recalled with our subjective experiences" has the same shape: "might be recalled" names a read-out, and the paper contains none. There is no equation that takes the density pattern and returns anything.

### 1.5 Microtubules, dephasing, rings, and energy supply

**The paper claims** that microtubules are the coherent light sources, that superradiance "suffers from the dephasing effect", that arranging water molecules on a ring would reduce it, and that microtubules have rings.

**The paper assumes** all of this. The superradiance calculation (Appendix A) never uses a microtubule: no geometry, no ring, no dephasing rate enters any equation. The paper names the obstacle (dephasing) and proposes a cure (rings) without computing either. The condition superradiance needs is that its own time scale τ_R = 2π/(g²ΩN) (equation (A47)) be shorter than the dephasing time. Neither number is given, so the condition cannot be checked, by the authors or by anyone else.

**The paper claims** that "microtubules work as single mode waveguides with a cutoff wavelength 21 nm, in brief they should be able to guide light from strong ultra-violet to near-infrared region".

This is backwards. For a hollow conducting guide, a cutoff wavelength of 21 nm means waves *longer* than 21 nm do not propagate. Visible light at 500 nm is twenty-four times longer than the cutoff. If the guide is instead treated as a thin dielectric rod (which is closer to what a microtubule is), its ability to confine light at 500 nm is set by a dimensionless number (the rod's radius times 2π/λ times the square root of the difference of the squared refractive indices inside and outside); with a 12.5 nm radius, index 1.5 for protein and 1.33 for water, that number is about 0.1, and at that value almost all of the light travels outside the rod. Either way, the sentence does not follow from the number it quotes.

**The paper claims** that waste energy from mitochondria, "on the order of 10⁻¹³ W", "might be used as a supply for emission of super-radiant light".

At 500 nm, 10⁻¹³ W is about 250 000 photons per second. Writing the paper's 2.5 petabytes at one photon per bit from one such source would take about 2500 years. That is not a refutation of anything in Appendix A; it is a reason the power figure does no work in the argument.

### 1.6 Memory capacity and the Landauer paragraph

**The paper shows**: capacity per area 4n_r d/λ³ with n_r = 1.3, d = 2 mm, λ = 500 nm is 8.3 × 10¹⁰ bits per mm²; over 2500 cm² that is 2.6 petabytes (the paper rounds to 2.5). With 250 trillion synapses at one bit each, the comparison figure is 31 terabytes (the paper rounds to 30). At 1500 nm the capacity is about 0.1 petabytes. All of this is arithmetic and it is right.

What the arithmetic rests on, and what the paper does not say:

- The factor that makes it petabytes is the thickness. Over the same area, a hologram recorded on a *surface* at 500 nm holds 4/λ² × 2500 cm² = 0.5 terabytes, below the synaptic figure. The paper's 2.6 PB is 0.5 TB multiplied by n_r d/λ = 5200, the number of half-wavelengths across the 2 mm slab. Whether the medium resolves depth at the wavelength scale is exactly what a write-and-read mechanism would have to establish, and there is none.
- One bit per synapse is the low end of published estimates. At 4.7 bits per synapse (a published reconstruction figure) the comparison becomes 2.6 PB against 147 TB; with a surface hologram it reverses.
- The wavelength was chosen, not derived. The superradiance model has its own emission frequency Ω, and it is never computed. Had the paper used the 4 meV scale it quotes elsewhere for water, the wavelength would be 310 µm and the same formula gives 11 megabytes.

**The paper claims** that because a 500 nm photon (2.4 eV) carries far more energy than k_BT ln 2 (20 meV at body temperature), "information can be recorded at physiological temperatures with no risk of thermal degradation", and that the Landauer principle sets a "maximum wavelength" of 60 µm.

This does not follow. k_BT ln 2 is the least heat that must be released to *erase* one bit. It says nothing about how long a bit, once written, survives. In the paper's own model the record is a density pattern in φ, not a photon; how long that pattern survives at 310 K depends on the energy barrier that holds it in place, and the paper never writes one down. A photon's energy being large is irrelevant to the lifetime of a pattern the photon helped write. The "60 µm" is simply the wavelength whose photon energy equals k_BT ln 2; it is a conversion between units, not a limit on holography.

### 1.7 The control paragraph

**The paper shows** equation (12), the continuity equation, and says "what we can manipulate is the velocity". Correct: in the model the field A moves the fluid φ, and the density changes where the flow converges or diverges.

**The paper claims**: "Using damping input functions, density distributions of charged bosons for holograms stops evolving over time, and target binary holograms are achieved."

Three points. First, the density does not stop evolving: the paper's own Figure 6 shows the dip deepening at every sampled time, 1.3 %, 4.5 %, 9.1 %, 16 %, 21 %, with the drive already gone. What stops is the driver, by construction (its decay rate γ₂ was put in by hand). Second, "binary" is a word, not a feature of the result: the dip is a continuous number between 1.3 % and 21 %, and nothing in the paper thresholds it. Third, the same paragraph says that because the velocity is still nonzero at late times, "charged bosons will collect into the peripheral regions": by the paper's own account the pattern keeps moving after the drive is gone, so whatever was written is not held.

**The paper shows**, and this is worth quoting, that the "slight distortions" in Figure 6f "originate from the Laplacian of |φ| in A⁰" in equation (A87). That Laplacian term is the only term in Appendix C that is not classical: it is the quantum-pressure term, the one place where Planck's constant survives the paper's truncations. The paper calls it a distortion and reports that it "does not seriously affect" the result. So by the paper's own account, the simulation works despite its only quantum term, not because of it.

### 1.8 The headset

**The paper claims** that to manipulate holograms in real three-dimensional tissue "we have to adopt a hemispherical or spherical surface headset covering our head".

This sentence answers a question the paper never asks: who reads the hologram? In the whole paper, the only agent that writes or reads a pattern is this external device and whoever operates it. The brain in the model never reads its own record. If one asks where the "observer" is in this theory of memory, this is the answer: outside the head, holding a headset.

### 1.9 "One-to-one correspondence"

**The paper claims**: "Once our subjective experiences and memory are manipulated by external stimuli, we find one-to-one correspondence between holograms induced by external input functions and our subjective experiences. Our approach might indicate the reductionism of subjective experiences to holograms of water media."

A one-to-one correspondence is a map between two sets, each element of one matched with exactly one of the other. The paper has one set: patterns on a grid. It has no second set: no variable, measurement, or report stands for an experience. There is no map. The word "once" at the start of the sentence assumes the manipulation of experience that the sentence then says would be found. The conclusion is in the premise.

This is the central move of Section 5 and it is the same move each time: a word that names a thing with structure (sector, register, memory, recall, correspondence, experience) is placed next to a calculation that has no such structure, and the calculation is then read as being about the thing.

---

## 2. Section 6, the Concluding Remarks

### 2.1 "Vision is perhaps the most important link between the outside world of the observable phenomena and the inner life of our mind"

Two things are put in place by this sentence: an *outside world* that exists and is observable, and an *inner life* that images it. The rest of Section 6 asks where the image is formed. Everything in the paper takes the world as given and asks how a brain represents it.

This matters for how the paper has been cited. It has been offered as support for the claim that "the universe does not render what is offscreen", that is, that unobserved things are not there. The paper says the opposite. Its world is outside, observable, and prior to the brain; the brain's problem is to form an image of it. The word "render" does not occur in the paper.

### 2.2 Sheldrake or Pribram: "Which of these ideas is closer to the truth?"

**The paper claims** that "the holographic brain hypothesis has merits that have not yet been fully explored". It does not decide the question it poses, and it offers no observation that would decide it. "Merits not yet explored" is a research plan, not a finding.

### 2.3 Pribram, Bohm, ordered water, and the 2022 MRI result

**The paper claims** that a 2022 MRI study "implies the involvement of nuclear proton spins of brain water molecules in an entangled quantum state" and is "a major step toward providing evidence that at least some brain functions have hallmarks of non-classical, quantum behavior and are involved in consciousness".

Whatever that study shows, it cannot be evidence for this paper's model, because this paper's model has no spin variable at all. The field φ is a spinless charged scalar. A result about proton spins, if it stands, is about a different physical quantity than anything in (A1) to (A91).

### 2.4 The summary paragraph

Each clause, against what was shown:

| The paper's clause | What was shown |
|---|---|
| "A super-radiance solution in holographic brain theory is derived" | A pulse of the hyperbolic-secant shape is obtained (A45) under conditions that include a gauge choice which, as written, sets the emitting medium's charge to zero (Section 4.1 below), a loss term added by hand (A42), an undefined initial angle θ₀, and a dipole approximation the paper's own geometry violates. Conditional at best; see 4.1. |
| "holographic aspect has been shown with deriving the limitation of memory capacity" | An optical count for a 2 mm slab, right as arithmetic; the hologram itself is assumed (A51), not produced. |
| "a control theory of holograms by adopting morphological computation" | One simulation at one parameter set, with a supplied target and an input computed from it. |
| "a hierarchical model with multiple layers (input layer: scalp, intermediate layers: skull, dura, and celebrospinal [sic] fluid, and output layer: neocortex)" | Four copies of the same equation with the same constants. Bone, membrane, fluid and cortex differ in nothing but their index n. |
| "We intend to apply our approach to manipulate holographic memory and subjective experiences by external electromagnetic fields in a future experimental study." | Agreed: the experiment that would connect the calculations to memory is future work. Until it is done the connection is a plan. |

---

## 3. What enters from nowhere: the full list

The things below are each used as if already available. For each: where it first appears, what it would have to be for the argument to go through, and what the paper gives.

| Imported thing | First appears | Would have to be | The paper gives |
|---|---|---|---|
| The outside world | §6, first sentence | — (it is simply assumed; no issue in itself) | assumed; it rules out the "not rendered" reading of the paper |
| The inner life, the image | §6 | a representation with a reader | the word |
| The quantum mind, its "sector" | §5 | variables with equations and a coupling to the rest | the word |
| Register, decipher, decide, encode | §5 | four operations with carriers | a list and the admission that it is "yet another mystery" |
| Subjective experience | §5, §6 | a variable or a report | the word |
| Memory, recall | §§1, 3, 5 | a write, a hold, and a read | a write (in simulation, of a supplied target), a hold (in simulation, with damping chosen), no read |
| One-to-one correspondence | §5 | two sets and a map | one set |
| The reader of the hologram | §5 (the headset) | something in the brain | an external device |
| Water | (A1) | a reason the field is water | a name; nothing in the equations is specific to water |
| Microtubules | §§1, 5 | a geometry in the emission calculation | a name; no geometry enters (A24)–(A47) |
| The emitters' size being below one wavelength | before (A24) | sub-wavelength emitter domains | a 2 mm by 2500 cm² sheet at 500 nm, which is not |
| The seed θ₀ | (A41) | a nonzero initial coherence, with its origin | "definition of θ₀ is in Appendix A", where it is only used, never defined |
| The loss length L₃ | (A42) | a radiation-escape mechanism | a term inserted "setting the length L₃" |
| The screening mass M² | (A48) | a property of the medium | "ionic bioplasma", a phrase, with a chosen value 2m² |
| The reference wave r | (A50) | a light source in the brain | an input |
| The object wave o | (A51) | the thing remembered, as a wave | an input with no source |
| The hologram pattern \|r + o\|² in the density | (A51) | the outcome of a write process | assumed outright |
| The targets | (10), (11) | something to be remembered | three straight line segments chosen by the authors |
| The drives | (A88)–(A91) | a stimulus | functions computed backwards from the target |
| The mass scale m | §4 | a number | none; at the 4 meV reading the grid cell is 49 µm, at a molecular reading it is 10⁻¹⁷ m |

---

## 4. The mathematics, in plain terms

This section is shorter than the full technical audit and states only what a reader needs to judge the story. Each item can be checked against the equation named.

### 4.1 The light pulse (Appendix A)

**The paper assumes** two conditions on the electromagnetic potential: A⁰ = 0 and ∇·A = 0 (stated before (A2); the paper calls the pair "the Coulomb gauge", which it is not; the Coulomb gauge fixes only the second).

**The paper shows** (A7), its own charge equation, derived from its own (A2)–(A6). Under the two conditions, the left side of (A7) is identically zero, so (A7) reads 0 = −e|φ|²: the charged medium has no charge. Kept with its integration constant, it reads instead: the charge density never changes in time. Either way the medium is frozen, and a frozen medium does not radiate a pulse. Concretely, the pulse in (A38) is driven by the coherence R = 2χ₀*χ₁ between the two levels; write the density in the paper's own two-level basis and the coherence appears as a term oscillating at the frequency Ω; a density that does not change in time forces that term, and so R, to zero.

This can be repaired: keep ∇·A = 0, let A⁰ obey Poisson's equation instead of being set to zero. Then the charge can move. The price is an electrostatic term in (A2) that the paper would then have to show is small. The paper does neither.

**The paper assumes** three more things on the way to the pulse: that all emitters sit within one wavelength of each other (the sentence before (A24)), that a loss term can be added to (A38) by hand (A42), and that the field adjusts instantly to the loss (before (A43)). The first is violated by the paper's own geometry in Section 3 (a 2 mm by 2500 cm² sheet is thousands of wavelengths across). The second and third are what make the hyperbolic-secant shape; without the loss, the equations oscillate instead of pulsing, and the shape is exact only in the limit of vanishing L₃.

**The paper shows** the pulse (A45)–(A47) under those assumptions, with an initial angle θ₀. With θ₀ = 0 there is no pulse at all (τ₀ becomes infinite). The paper says "definition of θ₀ is in Appendix A"; it is not there.

Two misprints: (A31) has χ₁ where χ₀ is needed; the necessary condition after (A47) compares Ω with e²n/m, which is Ω² not Ω (the two sides have different units).

### 4.2 The hologram (Appendix B)

**The paper assumes** an added term M²A in (A48) ("Meissner effect by ionic bioplasma") and an external wave Ã. Note that the external wave enters (A48) only through M²Ã: set M² = 0 and the external wave does nothing at all. Set M² very large and the medium becomes transparent and no image is formed. So the image lives only in a window of M², and its strength is bounded by the screening number e²|φ|²/(M²m), which at the paper's Section 4 values is 0.045.

**The paper assumes** (A51): that the medium's density is proportional to |r + o|², the interference of a reference wave r and an object wave o. This is the hologram. It is not produced by anything in the paper; it is written down. The object wave o has no source anywhere in the model.

**The paper shows** that, given (A51), the screened wave (A52) contains a term |r|²o proportional to the object wave. That is the standard algebra of holography and it is correct, with one misprint ((A52) labels the response with the symbol of the input). It also contains the usual twin term r²o*, and nothing selects the image from the twin.

So: if a pattern were written, and if something read the screened wave, the object would be present in it at a small amplitude. Neither "if" is discharged.

### 4.3 The capacity (Section 3)

Treated in 1.6 above. Right as arithmetic; the petabyte is the thickness factor; the baseline is a choice; the wavelength is a choice.

### 4.4 The simulation (Section 4, Appendix C)

**The paper shows** a derivation that starts from a quantum formalism (A53)–(A61) and arrives at (A76)–(A81) by dropping, in turn, every fluctuation term and replacing the remaining self-interaction by two constants, a mass M² and a damping γ, chosen by hand (A75). What is left is, exactly, a classical charged fluid coupled to a field: a continuity equation (A69) and a pressure balance (A70), plus Maxwell's equations with the two added constants. The quantum formalism does no work in the result; the same equations can be written in three lines from a classical starting point.

**The paper shows** one quantum term surviving: the Laplacian-of-|φ| term in (A70), (A81), (A87). The paper calls its effect a distortion (Section 5).

Misprints that affect anyone trying to reproduce the figures: (A70) prints a minus on the squared-velocity term where (A81) and (A87), and the derivation, give plus; (A76) and (A78) print e where (A82) has e²; and (A88)/(A89), the formula for computing the drive from the target, prints the second derivative in the wrong direction relative to (A82)/(A84). For the paper's targets, which vary in one direction each, the correct formula has no derivative terms at all and reduces to u_{n−1} = 2.5u_n − u_{n+1}, which gives a drive amplitude of 2.13; the paper quotes 3.9 from a formula that drops the backward term and says the figure shows "approximately 3".

**The paper shows** (A82)–(A86), and from these it follows that the added constants break Gauss's law. The paper reports that the number of bosons is conserved on the lattice to better than 10⁻⁶ %, and that is right: the fluid's own continuity equation holds. But Maxwell's equations also require ∇·E − ρ to stay at zero, and from (A82)–(A86) its rate of change equals the divergence of the M², γ and v terms, which is not zero. A rerun of the simulation at the paper's parameters measures this drift at between 1.1 and 2.3 times the change in charge density that the simulation is reporting. The paper could absorb this by declaring a medium charge that compensates, but it declares none. Without the added terms Gauss's law holds and nothing relaxes to the target, which the paper itself notes ("due to damping").

**The paper shows** the result: Figure 5, the field reaching the target; Figure 6, the density dip growing to 21 %. What produces the dip is the term e²A²/2m in the fluid's pressure balance: the fluid is pushed out of regions of high field intensity. Set e = 0 and there is no dip. This is a classical effect with a name (the ponderomotive force), and nothing in the paper distinguishes the simulated dip from it.

---

## 5. Put back together: what the paper establishes

Stated so that each claim is checkable and none goes past its support.

1. **A pulse.** A medium of identical two-level charged emitters, all within one wavelength of each other, coupled to light, with a seed coherence θ₀ ≠ 0, with a radiation loss added and the field adjusting instantly to it, emits a pulse of the hyperbolic-secant shape with time scale 2π/(g²ΩN). For this to hold, the condition A⁰ = 0 must be dropped in favor of Poisson's equation, at the cost of an electrostatic term that remains to be bounded. The values of g, Ω, N, L₃, θ₀ and the dephasing time are not given, so whether any of this happens in tissue is open.
2. **A hologram.** If the density of a medium is proportional to |r + o|² and the medium screens an incoming wave r weakly (screening number 0.045 at the paper's values), the screened wave contains the object wave o at an amplitude bounded by that number, together with its twin. How the density would come to be |r + o|², where o comes from, and what reads the screened wave, are not given.
3. **A count.** A 2 mm slab of refractive index 1.3 and area 2500 cm², resolved at 500 nm in all three dimensions, has 2.6 × 10¹⁶ distinguishable cells; a surface alone has 4 × 10¹². These are counts of cells, not of bits written and read.
4. **A simulation.** A classical charged fluid with chosen screening and damping, on a periodic 128 × 128 grid, in four identical coupled copies, driven by an input computed from a chosen three-segment target, develops a density depression in the target's shape that reaches 21 % after the drive has decayed. The depression is proportional to the coupling and vanishes at e = 0. The field equations as written do not keep Gauss's law, although the boson number is conserved. The quantity "approximately 3" for the drive amplitude does not match the formula in the text once that formula is corrected.
5. **No reader, no world-making.** None of 1 to 4 contains a sensory input, a read-out of the stored pattern, an action, an experience, or an observer. The one reader named in the paper is an external headset. The paper assumes an outside world throughout, and contains no claim that unobserved things are absent.

What would turn the story into a result, in order:

- a consistent set of field equations (the gauge repair, the charge accounting, the three misprints resolved) and the numbers g, Ω, N, L₃, θ₀ for the proposed medium;
- a write process: something that takes an object and produces |r + o|² in the medium, rather than assuming it;
- a read: a rule that takes the medium's state and returns the object, with an error rate;
- a hold: the pattern surviving, with noise, for a stated time, against a stated barrier;
- a comparison: the same simulation with the quantum-pressure term removed, to see whether anything in Figures 5 and 6 depended on it;
- only then, a mapping from patterns to reports, and an experiment on it.

The paper's final sentence promises the last step. The first five come before it.

---

## 6. For anyone who wants to push back

Each of these is a statement about a specific line of the paper. Each can be refuted by showing the line that answers it.

1. Under A⁰ = 0 and ∇·A = 0, the left side of (A7) is identically zero, so (A7) sets e|φ|² to zero or to a constant in time.
2. Written in the two-level basis of (A8)–(A12), the density contains the term 2 Re(χ₀*χ₁ e^{−iΩt} φ₀*φ₁), which cannot be constant in time unless χ₀*χ₁ = 0; and (A38) is driven by χ₀*χ₁.
3. θ₀ is used in (A41), (A44), (A47) and defined nowhere; with θ₀ = 0, (A47) gives no pulse.
4. The dipole condition stated before (A24) is violated by the geometry of Section 3 by a factor of thousands.
5. The condition after (A47) compares a frequency with a squared frequency; the resonant mode of (A13) exists only when Ω² ≥ e²n/m.
6. In (A48) the external wave enters only through M²Ã; with M² = 0 it has no effect.
7. (A51) is assumed. No equation produces |r + o|², and o has no source.
8. (A70) prints the opposite sign of the squared-velocity term from (A81) and (A87); the free plane wave satisfies the latter and not the former.
9. (A88) prints −∂₁²u₁ where the static form of (A82) gives −∂₂²u₁; for the targets (10)–(11) the corrected recursion gives 2.13, not 3.9.
10. From (A82)–(A86), ∂₀(∇·E − ρ) equals the divergence of the M², γ and v terms, which is not zero.
11. The density depression of Figure 6 is produced by the e²A²/2m term and vanishes at e = 0.
12. Figure 6 reports 1.3, 4.5, 9.1, 16, 21 %: the pattern deepens after the drive is gone; it is not binary and it is not read.
13. 4/λ² × 2500 cm² at 500 nm is 0.5 TB; the factor n_r d/λ = 5200 is what makes 2.6 PB.
14. k_BT ln 2 bounds the cost of erasing a bit, not the lifetime of a pattern; no barrier for the pattern is given.
15. No equation in the paper contains a sensory input, a read-out, an action, or an experience; the only reader named is the headset of Section 5.
16. The word "render" does not occur; Section 6 assumes the outside world in its first sentence.

Where one of these is wrong, the paper improves. Where none is, the story and the calculations stay apart, and the paper's own closing sentence says the experiment that would join them has not been done.
