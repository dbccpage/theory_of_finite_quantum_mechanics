# Alpha paper: ideas for the strips and a bounded first review

Source: [primitive_axiomatics.md](C:/.ana/coda_university/coda_research/001_finite_obstruction_calculus/006_primitive_axiomatics/primitive_axiomatics.md).

Read on 2026-11-03. SHA-256: `260a7ff81b7ea062a3ff40169fa1ddb400d11fc7cbe024362c9055051ca38717`.

The supplied copy calls itself a corrected republication and gives a last-updated date of 2026-07-24. This note does not reconstruct an earlier version. The source has not been edited. This is a source-reading and teaching crosswalk, with a few independently checkable mathematical observations; it is not a fresh Lean build, verification of the cited companion papers, or a full theorem audit.

## The central idea the pictures should inherit

Start with a declared comparison and permitted changes of local reference. Ask what those changes can remove, what survives them, and what a specified observer can still distinguish. Do not start by assigning an unexplained length, angle, norm, phase space, or amplitude to every difference.

That is more specific than the initial classical picture sheet. The v2 sheets construct a conditional classical model after supplying a state plane and its area pairing. They are not a derivation of Hamilton or Noether from this alpha paper.

## Source-grounded visual sequence

| Idea and source | Candidate three-panel captions | What must stay on the math sheet |
|---|---|---|
| Typed oriented comparison, §0.2 and §1.0 ([line 164](C:/.ana/coda_university/coda_research/001_finite_obstruction_calculus/006_primitive_axiomatics/primitive_axiomatics.md:164)) | “Compare these.” / “Reverse the comparison.” / “The difference reverses.” | Reversal is justified for the declared scalar/additive comparison, not every possible defect carrier. |
| Direct versus composed comparison, §1.0 and §1.3 | “Go by the first route.” / “Go by the second.” / “Do they agree?” | A path sum belongs to a specified additive realization. Edge data need not be exact differences of one global assignment. |
| Reference changes and quotient residual, §1.3 | “Change the local references.” / “The marks change.” / “What survives every allowed change?” | The permitted change is delta → delta+d0 f. The quotient is by precisely this repair class. |
| Triangle closure, worked example ([line 865](C:/.ana/coda_university/coda_research/001_finite_obstruction_calculus/006_primitive_axiomatics/primitive_axiomatics.md:865)) | “Compare two steps with one.” / “They miss.” / “Moving the references cannot remove this miss.” | d1(delta+d0 f)=d1 delta because d1 d0=0. Declare which triangle is actually a tested 2-cell. |
| A balanced witness, §1.6 ([line 823](C:/.ana/coda_university/coda_research/001_finite_obstruction_calculus/006_primitive_axiomatics/primitive_axiomatics.md:823)) | “What enters also leaves.” / “Shift the references.” / “This comparison gives the same answer.” | d0*phi=0 implies pairing invariance. Norm bounds become necessary when claiming the quantitative optimal certificate. |
| Observer-selected measurement, §§1.4–1.7 | “Choose what can be distinguished.” / “Choose how to measure it.” / “Now give the remainder a size.” | A quotient residual class is distinct from its measured magnitude. A passive quotient may erase a witness. Scalar l1 is conditional, not universal. |
| Context can expose a hidden distinction, §1.8 ([line 1019](C:/.ana/coda_university/coda_research/001_finite_obstruction_calculus/006_primitive_axiomatics/primitive_axiomatics.md:1019)) | “These look the same here.” / “Apply the same next move.” / “Now can you distinguish them?” | The common operation must be defined on the underlying states. Failure to preserve profile equality is the contextual-congruence witness; an operation already well-defined on the quotient cannot do this. |

These are caption/storyboard candidates, not newly rendered diagrams. The already-rendered v2 classical sheets remain separately identified, with their own assumptions and review trail.

## The closest link to the remembered conservation argument

The strongest direct bridge here is in the dual-witness section:

\[
\langle\varphi,\delta+d_0f\rangle
=\langle\varphi,\delta\rangle+\langle d_0^*\varphi,f\rangle
=\langle\varphi,\delta\rangle
\quad\text{if }d_0^*\varphi=0.
\]

Thus a balanced detector ignores allowed reference changes. At each vertex, its incoming and outgoing weights cancel. This invariant pairing is available before selecting the l1 quotient norm or invoking its dual optimum. Under the finite l1/l-infinity assumptions, the bounded maximization additionally certifies the exact minimal repair remainder.

For an explicitly supplied path delta(t)=delta(0)+d0 f(t), the fixed detector response remains constant. This is conservation under those reference changes. It is not, on its own, Noether's dynamical theorem, a Hamiltonian, energy conservation, or physical current conservation.

Neither “Hamilton” nor “Noether” occurs in this supplied version. The nearest path-comparison section is §1.8.1, “Homotopy of Contexts”: it compares two declared context paths and classifies their quotient discrepancy. It does not provide a general identification of that discrepancy with geometric holonomy. A connection/transport law would need to be declared for that further interpretation.

## What a later Hamilton/Noether bridge must add

The paper does not supply a time evolution, conjugate q,p pairing, symplectic form, action, or the variational hypotheses of Noether. The classical v2 sheets explicitly introduce those structures. Their local construction—smooth preservation of oriented area in two dimensions implies a locally Hamiltonian generator—is conditional on those additions.

To connect the two honestly, first identify the exact state variables carried from the finite comparison system, specify the evolution and pairing on them, and prove compatibility with the quotient/observer distinctions. Only then claim the Hamilton or Noether consequence. The paper's finite repair policy alone does not establish this connection.

## Initial review issues worth checking

### 1. Align the l1-selection theorem's hypotheses with its proof

In §1.4, Theorem 003-A lists identical-replica additivity at [line 654](C:/.ana/coda_university/coda_research/001_finite_obstruction_calculus/006_primitive_axiomatics/primitive_axiomatics.md:654), while the singleton decomposition in its proof uses arbitrary disjoint additivity at [line 660](C:/.ana/coda_university/coda_research/001_finite_obstruction_calculus/006_primitive_axiomatics/primitive_axiomatics.md:660).

If “edge decomposability” means only its parenthetical wording, “dependence only on local stalk magnitudes,” then the listed conditions do not force a sum. On nonnegative vectors define

\[
J_n(a)=\sqrt{n\sum_{i=1}^n a_i^2}.
\]

This family is continuous, monotone, convex, positively homogeneous, permutation-invariant, faithful and singleton-normalized. Replicating an n-entry vector N times gives J_(Nn)(a repeated N times)=N J_n(a). Nevertheless J_2(1,2)=sqrt(10), while J_1(1)+J_1(2)=3.

If decomposability instead means genuinely independent, additive component composition, say so as a precise equation; that stronger condition excludes the counterexample. The nearby Theorem F and open S5 already recognize the missing bridge. The actionable repair is to make Theorem 003-A's list and proof express the same strength of hypothesis, not to discard the valid conditional additive result.

### 2. Repair the scalar-specialization summary attribution

The summary at [line 1201](C:/.ana/coda_university/coda_research/001_finite_obstruction_calculus/006_primitive_axiomatics/primitive_axiomatics.md:1201) attributes D(x,y)=y−x to antisymmetry, path additivity and faithfulness. Those properties also hold for D(x,y)=2(y−x), so they do not fix the stated formula or scale.

The body correctly obtains y−x by declaring real scalar stalks, identity comparison maps and ordinary subtraction. Align the summary with that specialization, or add the normalization/structure that actually fixes the numerical representation. This matters directly for the illustrations: a length scale must not appear to have been forced by comparison alone.

### 3. Keep the already-admitted open results open

The paper itself labels the initiality-to-reflection step S6 conjectural. A terminating search and a minimal choice do not establish a universal initial choice. Preserve that status. Likewise, do not infer exact repair from zero closure charge: a nonzero closed residual may remain in H1. The paper explicitly distinguishes this case; the teaching sequence must do so as well.

## Provenance boundary

The supplied document reports Lean-backed finite-core results and a prior build. This reading has not rerun them or inspected their current proof terms. The algebraic triangle/witness calculation and the two counterexamples above can be checked directly; they do not certify the whole paper. The original paper and the adversary's criticism of the picture sheets remain unmodified.
