Status: AI-drafted, awaiting human review.

# FSP-DISCRETE-WDW-CONSTRAINT: an indefinite constraint and its distinct kernel projector

On integer triples, the declared constraint H(x,y,z)=(0,2y,-z) is symmetric for the usual dot product and has kernel exactly the vectors with y=z=0. The map P(x,y,z)=(x,0,0) is idempotent, maps into that kernel, fixes exactly the kernel, and has residual orthogonal to every kernel vector. H has a nonzero kernel but is indefinite and is not idempotent. Thus this finite-dimensional constraint and its kernel projector are distinct operators.

AuthorityEffect: None.

## Derivation

Declare H to be the diagonal integer operator with entries 0, 2 and -1. Direct expansion of the dot product shows ⟨Hv,w⟩=⟨v,Hw⟩ for every pair of integer triples. The equation Hv=0 is equivalent to y=z=0, so the kernel contains the nonzero first coordinate vector.

Define P to retain the first coordinate and discard the other two. Then P^2=P, HP=0, and Pv=v exactly when Hv=0. For every kernel vector w, the residual v-Pv has dot product zero with w. These statements identify P as the orthogonal kernel projection in this declared integer model.

The quadratic form of H has value 2 at the second coordinate vector and -1 at the third. H is therefore indefinite. Applying H twice to the second vector gives coefficient 4 instead of 2, so H is not idempotent. A nonzero constraint kernel does not by itself supply positivity or make the constraint equal to its kernel projector.

The independent checker computes the exact diagonal matrix spectrum and nullspace, checks the symbolic projection identities, and enumerates integer vectors for the kernel and fixed-point characterizations. It does not execute a Wheeler-DeWitt or diffeomorphism model.

## What is proved

On integer triples, the declared constraint H(x,y,z)=(0,2y,-z) is symmetric for the usual dot product and has kernel exactly the vectors with y=z=0. The map P(x,y,z)=(x,0,0) is idempotent, maps into that kernel, fixes exactly the kernel, and has residual orthogonal to every kernel vector. H has a nonzero kernel but is indefinite and is not idempotent. Thus this finite-dimensional constraint and its kernel projector are distinct operators.

## What is assumed

The mathematical structures and operations are exactly those declared in `lean4/CampaignConstraintKernelProjector.lean`. This is a declared finite-dimensional integer model; its set of integer triples is infinite. It constructs no discrete Wheeler-DeWitt operator, triangulation dynamics, diffeomorphism action, physical state space or continuum limit. Its counterexample concerns an inference from symmetry and a nonzero kernel to positivity or idempotence, not a specified gravitational model.

## What is open

Claimed: a discrete Wheeler-DeWitt operator H_perp on spatial triangulations is nonnegative and acts as a projection on diffeomorphism-invariant states; no such operator is constructed here, and the DeWitt supermetric of the continuum constraint is indefinite.

Construct H_perp on a declared finite state space and determine its spectrum; the manuscript separates the constraint H_perp Psi = 0 from thermal Hamiltonians (Section 2.5).
