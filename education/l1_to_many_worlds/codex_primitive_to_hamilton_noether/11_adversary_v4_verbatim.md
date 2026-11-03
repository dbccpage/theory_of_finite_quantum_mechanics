# Independent review of v4

**Verdict:** v4 presents a coherent conditional route and substantially improves the source connection. I found no wrong numerical result in the mixing, redistribution, oscillator, or translation examples. The classical Hamiltonian calculation and the separate matrix-generator calculation have the correct signs. Four bounded revisions remain advisable before presenting the sheets as self-contained novice teaching.

## Scope

I visually inspected both v4 PNGs and read the v4 renderer and mathematical companion. I checked the cited WDP passages on balance, the observer Gram form, compatible complex structure, and inner derivations, and used the finite-QM passages already inspected in this review. I did not modify the sources, execute the renderer, run Lean, inspect the PDF separately, or perform a broader corpus audit.

## 1. Medium — The return arrow in strip 2 is difficult to see

In the last panel, the green reverse arrow is drawn directly over a thick black forward arrow. At the displayed size, the result reads primarily as one rightward arrow; the leftward green head is hard to distinguish.

The caption says “Follow a step back. You return,” but the crucial opposite direction is visually weak. This is a rendering problem, not incorrect cancellation arithmetic.

**Remedy:** separate the forward and reverse strokes slightly, or make their opposite heads clearly visible through stroke width and contrast. The reader should be able to identify the return without relying on the caption.

## 2. Medium — State the Hamiltonian hypothesis as a vector field and its flow

The strip-6 companion says “a time-independent continuously differentiable flow” and immediately uses \(u,v\) and their derivatives. These symbols have not been defined as the instantaneous rates, and autonomy belongs to the generating rule; the flow itself varies with elapsed time.

The intended theorem is sound, but the compressed wording blurs the objects and their regularity.

**Remedy:** write, for example:

> Let \(X(q,p)=(u(q,p),v(q,p))\) be a time-independent continuously differentiable vector field, and suppose its local flow preserves \(dq\wedge dp\).

Then identify \(u=\dot q\) and \(v=\dot p\). This supplies the regularity used when computing \(d(u\,dp-v\,dq)\). A short gloss of “simply connected” as a patch without holes would also recover useful clarity from earlier versions.

## 3. Medium — Specify what is completed in the “rational turns” sentence

The companion correctly distinguishes a circle from the real time line, but “rational turns complete to a circle” omits the admitted group and metric.

The move actually pictured generates only
\[
\{I,J,-I,-J\}.
\]
That finite four-element group is already complete in its usual metric; repeating the pictured quarter-turn does not produce a dense circle.

**Remedy:** either remove the completion sentence from this stage, or say that admitting all rational fractions of a full turn gives \(\mathbb Q/\mathbb Z\), whose completion in the chosen circle metric is \(\mathbb R/\mathbb Z\). That enlargement and metric are additional inputs.

This does not undermine the valid finite conclusion \(J^2=-I\), \(J^4=I\), or the Gaussian-rational scalar action.

## 4. Medium — Name the full matrix algebra and the adjoint law in the separate generator route

The final block compresses WDP §19A.6 to “matrix multiplication, an adjoint and a K-linear derivation.” The source theorem specifically concerns the full algebra \(M_d(\mathbb Q(i))\), with its declared conjugate-linear adjoint, and requires
\[
\delta(A^\dagger)=\delta(A)^\dagger.
\]

The displayed matrix-unit construction relies on that full algebra. General algebras with multiplication and an adjoint need not have only inner derivations.

**Remedy:** name \(M_d(\mathbb Q(i))\), state the displayed adjoint condition, and explicitly record \(H_0^\dagger=H_0\). The conclusion “unique modulo rational scalar identity” is then correctly scoped.

The existing warning that this constructs no clock or flow is accurate and should remain.

## Checks that passed

- **Strip 3:** the normalized inputs and rotation are correct:
  \[
  U(3,4)/5=(1,0),\qquad U(3,-4)/5=(-7,-24)/25.
  \]
  The renderer applies scale \(1.5\) consistently, yielding output components \((1.5,0)\) and \((-0.42,-1.44)\). The different horizontal lengths are real, and the supplied squared readout gives first values \(1\) and \(49/625\). The non-descent claim concerns the declared component-magnitude report; it does not establish Born uniqueness.

- **Strip 4:** the displayed redistribution is \(3+1=2+2=4\). The more general conservation statement follows from the explicitly added update law and cancellation over both endpoints of each internal edge. It is appropriately distinguished from Noether’s theorem.

- **Strip 5 and WDP:** the orientation agrees with \(J(x,y)=(-y,x)\). WDP §§17.8–17.9 supports the observer-relative Gram form and the conditional construction
  \[
  h(x,y)=g(x,y)+i\,g(Jx,y),
  \]
  with the first slot conjugate-linear. The sheet correctly treats \(J\) and its compatibility as supplied.

- **Strips 6–7:** the patch has area \(3\times1.8=5.4\). The shears preserve its orientation and area. The oscillator uses \(-J\), as the text explicitly states. Rate magnitudes, shared starting state, and exact sampled rotation remain consistent.

- **Strips 8–9:** both operation orders end at \((4.15,0.65)\). The unshifted sequence \((2,0.65),(2.65,0.65),(3.3,0.65)\) is correct. The symmetry, action variation, endpoint distinction, and conserved charge \(p\) are correctly scoped.

- **Matrix route:** for the intended full matrix algebra, the signs in
  \[
  \delta=[S,\cdot],\qquad H_0=iS,\qquad
  \delta=-i[H_0,\cdot]
  \]
  are correct after the skew-adjoint adjustment. WDP expressly distinguishes this from Stone’s theorem and physical Hamiltonian selection.

The revised sheets preserve the important boundaries between a report, an observer-relative pairing, an admitted complex structure, classical area-preserving dynamics, and an algebraic matrix generator. These checks support the conditional constructions shown; they do not establish novice comprehension or any claimed derivation of Born, Bell, Everett, or physical laws.
