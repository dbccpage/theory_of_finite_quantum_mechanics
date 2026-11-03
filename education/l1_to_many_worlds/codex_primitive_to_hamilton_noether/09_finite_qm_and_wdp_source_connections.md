# What the newer finite-QM and WDP sources add to the strips

Read on 2026-11-03 for the ongoing picture-and-math teaching task. Sources remain unchanged. This is a targeted mathematical reading, not a full audit of the 17,685-line WDP monograph, a Lean build, or verification of its publication history. The reviewed v3 picture and math sheets remain a conditional classical construction; this note supplies material for a subsequent revision.

## The main change in understanding

The sources supply a more explicit sequence than the earlier papers:

**Declared comparisons → composable histories → signed differences → reports that may forget needed distinctions → an observer-relative pairing → a compatible quarter-turn → conditional quantum states and transformations.**

Each arrow in that sentence has a hypothesis. It is possible to teach the operations before naming the algebra, while keeping the hypotheses visible on the math sheet. These texts do not claim that the hypotheses follow from an unstructured mark.

## Source locations

- **FQM:** [Finite Quantum Mechanics](C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/atlas/papers/core/finite_quantum_mechanics.md), version 0.56.0, dated 2026-10-21.
- **Proofs:** [Proofs of the Core Results](C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/atlas/papers/core/finite_quantum_mechanics_proofs.md), dated 2026-10-26.
- **WDP:** [The Witnessed Difference Programme](C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md), version 2.4.5, dated 2026-10-16.

## 1. The Noether-adjacent passage is now located

[WDP §5.12, lines 2329–2361](C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md:2329) states two different balance facts:

\[
\sum_v(d_0^*x)(v)=0,
\qquad
\langle A+d_0\lambda,\gamma\rangle=\langle A,\gamma\rangle
\quad\text{when }\partial\gamma=0.
\]

The first says that each internal edge contributes opposite amounts at its endpoints. The second says a closed-loop comparison ignores an allowed vertex-potential change. They require no Hilbert space or complex amplitude.

Possible captions, for an explicitly drawn redistribution rule:

1. “Take this much from here.”
2. “Put the same amount there.”
3. “The total stays.”

For a loop-comparison strip:

1. “Change the local references.”
2. “Follow the same closed route.”
3. “The changes cancel around the route.”

These are candidate captions, not new rendered panels. A precise added update law, \(z_{k+1}=z_k+d_0^*j_k\), makes the first identity a discrete conservation result: \(\sum_vz_{k+1}(v)=\sum_vz_k(v)\). This small extension supplies a dynamics rather than pretending the static identity already contains one. It is still not a derivation of Noether's symmetry/action theorem. WDP itself explicitly declines that identification at lines 2356–2361. A graph with an edge leaving the system requires accounting for the omitted endpoint; internal cancellation is then not conservation of the restricted subsystem.

## 2. There is a stronger route to addition and a pairing

[WDP §17.7](C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md:5871) starts with typed moves and histories. Two histories are interchangeable only if every permitted preceding and following context preserves the declared answers. Present agreement alone is insufficient.

It then supplies finite alternative formation and signed completion:

\[
\mathbb N^{(X)}\longrightarrow\mathbb Z^{(X)}.
\]

The derived result is the unique extension property for additive maps into groups. Likewise, explicitly requiring independent composition to be additive in each input gives the free integer tensor construction. Neither physical independence nor quantum entanglement follows from that algebra alone.

[WDP §17.8](C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md:5948) supplies an additive observer \(L\) and defines

\[
g_L(a,b)=L(a)^TL(b).
\]

It proves \(\operatorname{Rad}(g_L)=\ker L\): the signed differences invisible to that observer are exactly the null directions of its supplied sum-of-squares comparison. This is a precise observer-relative construction. The observer and coordinate pairing are inputs; the picture must not suggest that an observer-independent metric has been forced.

## 3. The quarter-turn has an exact algebraic role

[WDP §17.9](C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md:5974) assumes a rational-linear move \(J\) such that

\[
J^2=-I,\qquad g(Jx,y)=-g(x,Jy).
\]

Then \((a+ib)x=ax+bJx\) defines a Gaussian-rational scalar action, and

\[
h(x,y)=g(x,y)+i\,g(Jx,y)
\]

is a positive-semidefinite Hermitian form with the same invisible directions. These consequences are derived from the two displayed laws. The move \(J\), its compatibility with the pairing, and rational scalar operations are supplied. The equally admissible move \(-J\) reverses the complex orientation.

For the picture: “Turn once. Turn again: reversed. Twice more: returned.” The math sheet can name the algebra after the reader has seen the move. Four applications return here because this particular move has fourth power equal to identity; arbitrary rational rotations need not return after finitely many steps (Proofs §4.2).

## 4. The Hamiltonian result is more specific than a turning arrow

[WDP §19A.6](C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md:8226) supplies a linear change rule \(\delta\) on matrices over \(K=\mathbb Q(i)\), satisfying the product rule and respecting the declared adjoint. It constructs

\[
S=\sum_j\delta(E_{j1})E_{1j},\qquad
\delta=[S,\cdot]=-i[H_0,\cdot],\qquad H_0^\dagger=H_0.
\]

The generator is unique up to a rational scalar multiple of the identity. The product rule is a substantial assumption: it is not obtained merely by showing two frames of an arrow.

This is an algebraic generator theorem. It supplies no clock, exponential flow, physical energy or selected continuous interpolation. It also differs from the classical local Hamiltonian theorem on the v3 math sheet, which assumes a smooth area-preserving flow on a conjugate-coordinate plane. Neither theorem should silently stand in for the other.

[Proofs §4.3](C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/atlas/papers/core/finite_quantum_mechanics_proofs.md:508) gives a particularly useful visual limit: a two-label toggle has no half-step among two-label maps, but admits multiple square roots after enlarging the representation. Even a fixed unitary full step has multiple logarithms. The endpoints do not determine the motion between them.

## 5. What is now available for Born, Everett and Bell

| Teaching target | Useful exact material | What remains an input |
|---|---|---|
| Direction matters after joining | Proofs §§1.2–1.4: equal square reports can separate after the same mixing map; population descent for integer matrices holds exactly when each row has at most one nonzero entry | The signed carrier, report and mixing operation. This is failure of a particular report, not failure of all l1 geometry |
| A squared rule | Proofs §2.2: \((3/5)^p+(4/5)^p=1\) selects \(p=2\) within the stated power family | The Pythagorean context, power family and normalization requirement; not uniqueness among all readouts |
| A broader Born representation | FQM §13.8.13, item 1: positive normalized valuations additive on all effects have trace form on the supplied rational/Hermitian matrix carrier | Matrix order and effect additivity. Projection-only rational frame additivity is weaker; the account explicitly retains that boundary |
| Records without erasing global coherence | FQM §13.4: a coherent joint state and its dephased mixture share pointer reports but respond differently to an admitted joint control | The joint carrier, preparation, coupling, readout and ability to reverse the coupling; no unique-outcome or many-worlds selection theorem |
| Limits of branch counting | Proofs §4.5: finite equal-weight counting represents rational weights and cannot exactly represent the exhibited irrational weights | A branch decomposition and the interpretation of counts as probabilities |
| Bell | Proofs §§3.1–3.3: a positive common joint law bounds CHSH by 2; a supplied rational quantum model gives 14/5; a real algebraic model attains 2√2 | State, tensor composition, measurements and Born pairing; physical locality and setting independence for the physical interpretation |

The strongest Everett-oriented picture is therefore a record made by a reversible interaction, followed by an admitted joint reversal that recovers a distinction invisible in the pointer report. It must not identify an entangled pure state with a classical mixture. Nor does it prove many-worlds uniquely.

## 6. Later sources resolve earlier review findings

The original reviews remain unchanged. Their conclusions belong to the files they examined. Three later passages improve the situation:

1. **Trace-zero dual balance:** [FQM §11.2](C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/atlas/papers/core/finite_quantum_mechanics.md:623) explicitly uses scalar-identity vertex divergence for trace-zero repairs and distinguishes it from literal zero divergence for unrestricted Hermitian repairs. It even supplies an example where the two optimization problems differ. The historical Paper 080 objection should not be repeated as an unresolved defect of this passage.
2. **Trace-norm selection:** [FQM §11.3](C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/atlas/papers/core/finite_quantum_mechanics.md:663) proves that all-dimensional, all-CPTP-channel contractivity selects trace norm up to one common scale. This closes the shape ambiguity under those assumptions; the domain and normalization remain inputs. Proofs §2.5 contains only local duality and qubit pinching lemmas, and still carries an OPEN node label. It does not reproduce the main paper's selection proof.
3. **L1 aggregation:** [WDP §8.5](C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md:3362) states strong disjoint additivity directly, then gives a separate replica-extensivity argument with an explicit continuous associative aggregation operation. The earlier alpha counterexample does not refute this stronger formulation. The passage also distinguishes positive-sector aggregation from a norm on signed data.

These are mathematical corrections in the supplied texts, not claims that the associated Lean code was run here.

## 7. Independent review and the remaining corrections

The [independent core review is preserved verbatim](10_adversary_finite_qm_core_verbatim.md). It confirms the two Paper 080 issues are resolved in the main paper and identifies a concrete clock-completion error at FQM line 427: the rational turns Q/Z complete to the circle R/Z under the usual circle metric, not to the time line R. A full-turn clock reading does not retain the number of completed turns. An unwrapped time parameter is a further choice.

It also finds documentation drift: the proof companion's trace-norm and real-exponent mechanization descriptions do not match the main paper's later statements. The exact current Lean status was not checked. Its smaller CHSH presentation point is that the minus sign changes position between sections; the bounds are equivalent under a local sign relabeling, but a novice sequence should use one convention.

**Correction to this crosswalk's first draft:** I initially wrote that Proofs §2.5 also proves the full trace-norm selection theorem. The reviewer caught the distinction: that section proves two local lemmas and still labels the wider node OPEN. The full written selection proof is in FQM §11.3. The entry above is corrected, and this note retains the mistake and its resolution.

The review also identifies a better normalized mixing example than the unnormalized integer Hadamard:

\[
\psi_\pm=(3,\pm4)/5,\qquad
U=\frac15\begin{pmatrix}3&4\\-4&3\end{pmatrix}.
\]

The input square reports agree: (9/25,16/25). The same orthogonal move gives Uψ₊=(1,0) and Uψ₋=(-7,-24)/25, whose first square reports are 1 and 49/625. This uses only real rational coordinates and an exact length-preserving move. The chosen square report remains supplied. It is a strong candidate for the early “same report, different later answer” strip without introducing complex numbers.

## Reading and file custody

Root reading covered the WDP entrance/theorem map; §§1.1–1.4, 5.1–5.2 opening, 5.12, 8.5, 17.7–17.10, 19.3–19.4 opening, 19.8, 19A.1 opening, 19A.6, and P.7 opening/proofs; the FQM abstract, §§11.2–11.3, 13.4–13.5, 13.8.2 and 13.8.13; and the proof companion's report/mixing, selected readout, Bell, dynamics and completion sections. The independent reviewer reports its own scope separately. Sections outside those ranges were indexed/searched, not audited.

SHA-256 of the supplied files at reading:

| File | SHA-256 |
|---|---|
| finite_quantum_mechanics.md | `18e4f36cb038d9f4453c0b073bd381e7877de44b974e9dae0b40576740df476f` |
| finite_quantum_mechanics_proofs.md | `327c240aa5ef7f0b27ea83359ad638c70cdd08e2fc8c768037fed8c178b67298` |
| witnessed_difference_programme.md | `753d1c99c799f84f9a71912b98082d590c89c531f980c112b62ee2a86ab2726b` |
