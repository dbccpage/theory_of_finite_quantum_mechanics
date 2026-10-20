# GF frame-function review

AuthorityEffect: None. CONDITIONAL REPRESENTATION THEOREM ACCEPTED WITH CORRECTIONS. D1-D3 remain OPEN; purity D4 separate; general Lean verification pending. Original attachment preserved byte for byte. This is a replacement candidate in the results folder, not an applied replacement of a live manuscript or registry.

## Verdict and the crucial quantifier

Theorem 5 correctly obtains a unique representing state FOR EACH given admissible assignment after importing Theorem 4. The opening 'there is exactly one probability assignment' is false: g_1(v,B)=|v_1|^2 and g_2(v,B)=1/n both satisfy A0-A3 and differ. The theorem classifies assignments by density operators; it does not select a preparation or a state. Nonuniqueness of classical distributions in CE-5 therefore does not distinguish them from this quantum statement.

The elementary lemmas do not assume the quadratic ansatz. The nonquadratic-to-quadratic step is explicitly IMPORTED, not proved by the submitted architecture. This is a useful clarification of the claim, not a solution of the original framework-to-Born bridge. Neither theorem citation nor bounded replay discharges D1-D3 or provides a kernel proof.

## Elementary dictionary and geometry

H, its real/complex field, norm, orthogonality relation and all orthonormal bases are inputs. Unit length, Hilbert structure and projectors also use the inner product; it is probabilities whose quadratic dependence has not been assumed.

Lemma 1's well-definedness and frame sum use A1-A2. Its nonnegativity conclusion additionally uses A3, omitted from the stated assumptions. Lemma 2's shared-complement argument is correct for the resulting frame function, with A2 having already made f well defined. It is not a consequence of A1 alone for arbitrary contextual g. Use vector bases until ray invariance is established, or specify phase-invariant lifts of ray contexts. Every unit vector extends to a basis in the declared R/C model.

Lemma 3 and its converse are correct. Include mu>=0 and the zero-projector case. No sigma-additivity assumption is required in finite dimension. Each basis is finite but there are uncountably many bases: universal frame normalization is not a finite family of witnesses.

## Imported theorem and operator category

Theorem 4 is standard under the stated R/C and dimension>=3 hypotheses. Gleason 1957, Theorem 3.5 supplies it. Its complex compatibility and global gluing are not consequences of the phrase 'any two vectors share a subspace' alone; the source includes separate Lemmas 3.3 and 3.4. Retain the whole theorem as an external import unless those arguments are reproduced. The hard real three-dimensional core does not eliminate the remaining compatibility obligations.

Theorem 5's consequences are valid: positivity makes T PSD, normalization makes its trace one, the projector measure is Tr(TP), and polarization makes T unique for the supplied assignment. Over R it is real symmetric, over C complex Hermitian. Real rays do not identify imaginary coherences: the distinct complex states I/3 +/- i(E12-E21)/6 agree on every real unit vector. They are PSD since their nontrivial block has eigenvalues 1/3 +/- 1/6. This is consistent with real-category uniqueness and does not select C.

Purity is an additional hypothesis. The vector representative is unique up to sign over R or phase over C. The purported discipline 'first quadratic/trace formula at Theorem 5' is literally contradicted by Theorem 4 and earlier summary formulas. Replace it with the meaningful statement that no quadratic dependence is assumed in the elementary dictionary before the regularity import. The discharge section is section 8, not section 7.

## Counterexamples

CE-1 is a correct continuous non-Born qubit function. Bloch vectors represent rays/projectors; an orthogonal context corresponds to antipodal Bloch vectors. Its real 2D version also works. Plain continuity cannot repair projector uniqueness for a qubit. The finite exact contradiction used in replay fixes a candidate Bloch state from the x,y,z axes, then refutes it at n=(4/5,0,3/5): the nonlinear value is 76/125 versus the candidate 4/5.

CE-2 is valid. Interpret the displayed decimals exactly as 2/5,3/5,3/10. For a completely rational replay let v=(20/29,21/29,0), u=(21/29,-20/29,0), z=(0,0,1), B'=(v,u,z), B=(v,(3u+4z)/5,(-4u+3z)/5). These are orthonormal and share v. In B, v's squared overlap 400/841 beats both others; in B' the u value 441/841 beats v. No ties occur. A global tie convention can be placed on rays to keep phase-consistent atom labels; it is extra ordering data.

CE-3 is valid. With psi=e1 and the rational 3D basis ((3/5,4/5,0),(-4/5,3/5,0),(0,0,1)), the fourth-power sum is 337/625, not the coordinate sum 1. Any trace-form function has constant sum across bases, so this is an exact refutation without least-squares fitting.

CE-4 is valid as a choice-dependent proof obstruction, not an executable function. A normalized nonlinear additive phi cannot be nonnegative on [0,1], since that would force monotonicity and real linearity. Its composition ranges over phi([0,1]) and is unbounded; finite self-adjoint quadratic evaluations are bounded. This proves nonrepresentation. Such a phi is the identity on rational numbers, so rational squared-overlap tests cannot detect it. No finite table or random sampler realizes the full Hamel function. Replay does not claim to execute it.

CE-5 is NOT a counterexample to existence of trace form. Classical p has the representation diag(p) with diagonal subset projectors. Its valid role is a restricted-context identifiability example: I/3 and I/3+(E12+E21)/6 are PSD states agreeing on the coordinate context but differing on a rotated ray. A Boolean algebra does not see all noncommuting projectors. It neither lacks trace representation nor uniquely selects a probability vector, and neither does A0-A3 uniquely select one vector. Do not claim every proper context subfamily is non-identifying; 'not in general' is the valid qualification.

The shared blanket statement that every CE is a non-trace assignment therefore needs repair. CE-5 changes the event algebra, while CE-1 changes dimension. They cannot all use one unchanged test interface.

## Effect route and scalar scope

The finite-dimensional effect result is valid in every positive dimension, provided finite POVMs are INDEXED FAMILIES or multisets, not sets collapsing repeated effects. In particular (I/2,I/2), repeated zero slots and their multiplicities must be admitted. E2 makes equal effects carry equal values across slots and contexts. Comparison of (E,F,I-E-F) and (E+F,I-E-F) then gives partial additivity. Positivity supplies monotonicity, subdivision supplies rational homogeneity, and rational squeezing gives real homogeneity on the full R/C carrier.

Prove positive-cone scaling and differences independent of choices. Real symmetric trace duality suffices in the real case. The optional extension A+iB is complex-linear and applies only over C. Busch's infinite-dimensional source includes a countable normality hypothesis; it is unnecessary for this finite-dimensional argument. Caves et al. explicitly separate rational-field statements by omitting the real-linearity extension. Do not silently upgrade the earlier rational-effect proofs to full real contexts.

Step (2) alone is not the whole theorem: positivity, homogeneity and extension still matter. Appendix A is not the only conceivable strengthening for qubits; an explicitly declared extension to a larger full-projector model can also impose compatibility. No such extension is derived here.

## Appendix B and discharge obligations

Finite random tests are diagnostics. A sample may exhibit a violation, but cannot establish universal A1-A3 or prove nonrepresentation from a rounded least-squares residual. Exact inconsistent probe equations or certified bounds can refute a specified model. CE-4 must stay proof-only, never a fabricated numeric table. A classical distribution agrees with the pure-state fixed-basis data only when selected to do so. For n>=3 'bases containing psi' include varying complementary bases, not just one basis; the named rivals can agree on that family without making it universally uninformative.

D1 needs an actual carrier, scalar field, dimension and full outcome/context identification. Laplacian eigenvector orthogonality generally uses a previously chosen inner product and self-adjointness, so naming it does not derive the metric. The all-bases quantifier cannot be replaced by a tested family of eigenbases.

D2 must prove positivity and basis-invariant normalization. Normalized absolute amplitudes give an exact failure of shared-ray independence on the CE-2 rational bases: g(v,B')=20/41 but g(v,B)=100/247. Coordinate additivity on one sector partition is not universal frame normalization.

D3 requires compatible LOCAL EVALUATION, not sheaf gluing alone. If s_B and s_B' agree at v and g(v,B)=h_v(s_B restricted to v) with the same h_v in both contexts, then A2 follows. Context-dependent evaluation can destroy it even on identical glued sections. D4 is separately needed for purity.

## Implementation boundary and verdict

The existing lean4/GleasonTheorem.lean assumes a QuadraticFrameFunction2; lean4/GleasonRationalPlane.lean is a 2D rational obstruction. The inspected native quadratic-frame routine explicitly disclaims a general Gleason proof. No new compiler run or theorem is claimed from these source files. No live Rust/Python/Lean implementation, paper, frozen registry or previous sealed artifact is modified.

Accept the corrected conditional classification and elementary dictionary. Keep Gleason regularity explicitly imported, D1-D3 OPEN, purity D4 separate, and the original finite-program closure unresolved. Exact replay checks only the explicit finite witnesses and algebraic dictionary, not universal regularity or the framework bridge.
