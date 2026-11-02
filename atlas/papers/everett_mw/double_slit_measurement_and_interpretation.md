# The Double-Slit Experiment: What Changes When We Measure, and What the Mathematics Does Not Tell Us

**Jeremy H. Carroll** · November 2026

## The question is better than it sounds

Send electrons one at a time toward a barrier with two slits and let them land on a screen. Each electron arrives at one spot. Only after thousands of arrivals does a pattern appear: bands of many hits and bands of almost none, the pattern waves make when they pass through two openings and overlap. Now add a device that records which slit each electron went through. The bands disappear; the hits pile up behind the two slits, the way marbles would. So why does measuring change the result? That is not a beginner's confusion. It is the question the mathematics of quantum mechanics answers precisely. What the mathematics does not answer is "what is really going on," and the gap between those two questions is the subject of this paper.

## The mathematics of two alternatives

Quantum mechanics attaches to each route a complex number called an amplitude, and turns amplitudes into probabilities by squaring their sizes. Call the amplitude for reaching a given point on the screen through the left slit *a*, and through the right slit *b*. When nothing tells the two routes apart, the amplitudes add first and are squared afterward:

> P = |a + b|² = |a|² + |b|² + 2 Re(a* b).

The first two terms are what marbles would give: the chance of arriving through the left slit plus the chance of arriving through the right. The third term is the interference term. It depends on the *relative phase* of a and b, the angle between them if you draw each as an arrow. That angle changes from place to place across the screen, so the term is positive in some places (bright band) and negative in others (dark band). It is not an extra ingredient; it is what you get from adding before squaring instead of squaring before adding.

A small example shows how much the phase carries. Compare amplitudes (1, 1) with (1, −1). Both have the same per-slit weights, (1, 1). Now mix them, add and subtract, which is what a beam splitter does: the first becomes (2, 0), the second (0, 2). Same weights, opposite outcomes. A tally of how many electrons took each slit therefore does not contain the information that decides where the bands fall. That information is the relative phase, and only an operation that recombines the routes can read it.

## What a detector changes

A which-path detector is a physical system whose own state is changed by the electron. Write that state as d_L if the electron went left and d_R if it went right. Electron and detector then form one combined state,

> Ψ = a |L⟩|d_L⟩ + b |R⟩|d_R⟩,

with nothing "collapsed." Ask for the probability of a hit at a screen point, counting every possible detector state as a companion, which is what happens when nobody reads the detector:

> P = |a|² + |b|² + 2 Re(a* b ⟨d_L|d_R⟩),

where ⟨d_L|d_R⟩ is the *overlap* of the two detector states, a number of size between 0 and 1 that measures how alike they are. The interference term has simply been multiplied by the overlap.

- **Overlap of size 1.** The detector ends in the same state either way, holds no path information, and the fringes are untouched.
- **Overlap 0.** The detector states are perfectly distinguishable. The interference term is multiplied by zero and the fringes vanish, whether or not anyone ever looks at the detector.
- **In between.** Partial fringes. For equally lit slits the fringe contrast V equals |⟨d_L|d_R⟩|, and the best possible path guess has distinguishability D with V² + D² = 1 (Jaeger, Shimony and Vaidman 1995; Englert 1996). You can buy a little path knowledge for a little contrast, never both in full.

The honest answer, then: the interference term is a cross term between two routes, and it survives only as long as the rest of the world cannot tell the routes apart. A detector that records the route makes the two detector states orthogonal, and the cross term is gone. No consciousness enters the calculation; a stray gas molecule bumped differently by the two routes suppresses fringes as well as a physicist with a notebook does. Nor is "the measurement kicked the electron" the whole story: the overlap formula never mentions disturbance, and Scully, Englert and Walther (1991) designed detectors that record the path while leaving the particle's motion essentially unchanged.

Two cautions. The combined state is still one coherent state, so "no fringes" describes what the screen alone can show. In a quantum eraser the detector is later measured in a way that cannot tell L from R, and fringes reappear, but only within subsets of the hits sorted by that later result; the complete set shows none, and the two subsets' fringes are shifted so that they add up to none. Nothing travels backward in time. Deleting a record is not quantum erasure. When path information spreads into air, light and heat, the overlap can become extremely small and the loss of local fringes effectively irreversible because controlling all those records is impractical. Unitary evolution does not make that loss permanent in principle: coherently reversing the recording interactions before detection can restore interference. Simply spreading information among more systems does not imply an exactly zero overlap.

## What this does not establish

These equations are among the most precisely confirmed in science. By themselves they say nothing about three popular readings.

**Consciousness.** The calculation never uses an observer. The overlap is fixed by physical interactions.

**Simulation.** A simulation that reproduced these predictions would produce these bands, so the double-slit experiment alone cannot tell a simulated world from an unsimulated one. If a simulation hypothesis predicts something extra, that can be tested. If not, calling the world a simulation explains the bands no better than the mathematics already does.

**Many worlds.** The combined state can be written as a sum of terms, one per route, each tied to its own detector record. Everett (1957) held that every term is equally real; Deutsch (1997) reads each as a separate universe containing its own copy of the detector, and of you. That reading is coherent and is held by serious physicists. But writing a sum does not make its terms places. The same mathematics, with identical predictions for every experiment yet designed, is used by physicists who read the terms as alternatives rather than worlds. Deutsch's famous challenge, to explain where a quantum computer that factors a large number found "10^500 or so times the computational resources that can be seen to be present," is one he says adds psychological impact to a case he regards as already made by interference alone. Steane (2003) replied that a quantum computer does not perform 2ⁿ separate calculations: the sum of 2ⁿ terms is a feature of the notation, and the computation works only because those terms stay one coherent system that interferes, the same cross term as above. None of this disproves many worlds. It shows that the experiment does not establish them, and that you need not believe in another version of yourself to understand the bands.

## The better question

When two explanations agree on every experiment, no experiment can choose between them, and physicists stop asking "which one is true?" and start asking "where would they predict differently?" Theories in which large objects lose their interference on their own, for example, make predictions now being tested with ever heavier molecules. That is how speculation becomes research: not by declaring the question meaningless, but by finding the observation that would answer it. The double-slit experiment teaches the difference between what is measured, what the mathematics predicts, and what we add to make it feel like a story. Keep the wonder. Make it precise.

## References

1. G. Jaeger, A. Shimony and L. Vaidman, *Phys. Rev. A* **51**, 54 (1995); B.-G. Englert, *Phys. Rev. Lett.* **77**, 2154 (1996).
2. M. O. Scully, B.-G. Englert and H. Walther, *Nature* **351**, 111 (1991).
3. H. Everett III, *Rev. Mod. Phys.* **29**, 454 (1957); D. Deutsch, *The Fabric of Reality* (Penguin, 1997), chapters 2 and 9.
4. A. M. Steane, *Stud. Hist. Phil. Mod. Phys.* **34**, 469 (2003), doi:10.1016/S1355-2198(03)00038-8.
5. J. H. Carroll, *Theory of Finite Quantum Mechanics* (2026), github.com/dbccpage/theory_of_finite_quantum_mechanics; the (1, 1) versus (1, −1) example is kernel-checked in Lean 4 there (`lean4/InterferenceNonDescent.lean`), with complex amplitudes and the squared-size rule recorded as supplied inputs, not derived.
