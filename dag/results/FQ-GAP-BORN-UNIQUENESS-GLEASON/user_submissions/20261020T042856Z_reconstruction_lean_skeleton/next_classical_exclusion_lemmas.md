# Five small lemmas to discharge the geometric classical-exclusion branch

Work in actual finite-dimensional real convex state spaces. These requests instantiate missing geometry; the compiled abstract-hull transport theorem is available, but these concrete results are not claimed kernel-checked here.

RC-L1. **Affine hull transport.** For affine f and a finite set S, prove f(conv(S))=conv(f(S)). Give the finite barycentric-coefficient proof, including singleton and empty cases.

RC-L2. **Marginal surjectivity.** If a first-system state a0 exists and margB(prod(a0,b))=b, prove margB is surjective. State separately the affine law required to apply RC-L1. This set-level part already has the compiled interface proof.

RC-L3. **Infinitely many exposed qubit-ball points.** In the Euclidean unit ball B^3, prove every unit vector u is the unique maximizer of x -> u dot x. Show u(t)=(2t/(1+t^2),(1-t^2)/(1+t^2),0), t in Q_ge0, gives infinitely many distinct unit vectors; recover t from x/(1+y).

RC-L4. **Finite polytopes have finitely many exposed points.** If P=conv(S) with S finite and u uniquely maximizes a linear functional over P, prove u belongs to S. Combine with RC-L3 to show B^3 is not a finite polytope.

RC-L5. **Classical-composite exclusion.** Suppose AB is a finite simplex, margB is affine, and the product/marginal section exists with a first-system state. Apply RC-L1--L4 to rule out B affinely equivalent to B^3. No purity-of-product assumption is needed. Explain which genuine JordanIso and convex-composite hypotheses would connect this theorem to the original T4.

After these, the other work remains: actual System geometry, a valid Barnum-Hilgert bridge, Hanche-Olsen-compatible composites, physical effect/process availability, and object/monoidal completeness.
