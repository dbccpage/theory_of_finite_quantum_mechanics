# Review of submitted Steps 11-20

AuthorityEffect: None. Original attachment retained byte-for-byte. Status is written mathematical review, not Lean/kernel verification or an operational derivation of quantum mechanics.

## Main arguments

- 11: zero-pivot argument, positive-pivot Schur complement, permutation assembly and unit lower-triangular LDL* construction are correct. Explicitly use the d=1 base case. A zero chosen coordinate can be discarded; only when all remaining diagonal entries vanish does the zero-pivot lemma terminate the entire active block. PSD over C is the standing assumption; replacing complex tests by rational-vector tests uses the density argument already identified in Step 10.
- 12: four-rational-square conversion delta=a/b=(ab)/b^2 is correct, with integer four-square theorem explicitly imported. Gram factorization and the row bound 4 rank(A) are correct. This does not claim a square rational matrix square root.
- 13: stacking factors gives W*W=I and the exact compression identities. Zero-row blocks may represent labeled zero projections; if labels matter, retain those zero outcomes rather than silently changing a measurement's outcome set. No rational unitary completion was assumed.
- 14: the common realization for A,B,I-A-B and compression consistency give effect additivity. This is conditional on all declared inputs, including the family of normalized positive projection valuations and the matrix/isometry model.
- 15: codomain generalization to R, basis formula, positivity via rational rank-one tests and complex-vector density are correct. Uniqueness on effects passes through the unique rational-linear extension. The reusable claim about basis effects needs the affine repair below.
- 16: shrink/shift approximants remain in [0,I]; the stated loose error bound <=6d delta is valid. Lipschitz derivation is correct; handle distance=1 by the [0,1] probability bounds or epsilon=1, rather than requiring a strictly decreasing sequence inside [0,1]. Existence imports complex PSD factorization or an equivalent trace-positivity lemma. Uniqueness is established for the specified rational effect interval. The last generic dense-sub-interval record is not accepted as an existence theorem for arbitrary dense subsets without closure/compatibility hypotheses.
- 17: explicit d=2 and d=1 counterexamples are correct for the requested per-dilation assumptions. The factorization/converse descriptions require a single common map across all W; see below.
- 18: rational Bloch coordinates, lexicographic selector, orthogonal additivity and the four-direction contradiction are correct. The assertion that three axes alone rule out arbitrary Hermitian affine representation is false; see below.
- 19: both projections, exact rational order bounds, weighted lexicographic selector and the no-effect-extension contradiction are correct. The general binary obstruction can be justified with an explicit intermediate rational projection rather than merely citing density/chain-connectivity; see corrected_notes.md.
- 20: normalization of LK, marginal effects, trace duality, matrix associativity and identity laws up to the displayed index bijections are correct. This establishes composition of indexed instruments. A colored symmetric operad with fixed substitution slots needs a precise equality/profile convention, and zero-outcome deletion is not equality under the stated bijection-only convention.

## Claims requiring correction

1. Indefinite S_jk and T_jk cannot be scaled by a positive scalar into [0,I]. Use affine effects (I+S_jk)/2 and (I+T_jk)/2. This repairs the tomography record without changing the actual Step 15 proof.
2. Compression consistency means there is ONE p with mu_W(Q)=p(W*QW) for every W,Q. Separate maps p_W do not suffice. With Steps 14-15, consistency is equivalent to existence of one common input density matrix rho realizing every mu_W(Q)=Tr(W rho W* Q). The state map rho -> W rho W* is a pushforward; operator compression Q -> W*QW is the pullback.
3. Three Bloch coordinate axes, even with antipodes, admit a Hermitian affine representative (I+sigma_x+sigma_y+sigma_z)/2, though it is not PSD. The submitted proof correctly uses a further rational direction to rule out every Hermitian representative.
4. Keep the outcome profile and its slots fixed when defining partial substitution. Outcome permutations act by reindexing profiles and continuations, not by forgetting which slot is grafted. Branch-index permutations within a fixed slot may be quotiented. A scalar counterexample in corrected_notes.md shows why naive fixed-slot grafting on the outcome-unlabeled quotient fails.
5. A zero-Kraus outcome remains an outcome slot under bijection-only equality; deleting it changes arity. An empty branch set denotes a zero outcome, not an absent slot. A coarser operational quotient or a coarse-graining operation must be defined separately.
6. The final scope sentence overstates (C) as the sole non-algebraic input. The matrix model, PSD interpretation, positive normalized orthogonal valuations, allowed dilations and real/complex background are also inputs. What 14 and 17 isolate is the independence and role of the additional consistency axiom within that supplied setting.

## Verification ceiling

The corrected core proofs are accepted on written mathematical review. Exact finite checks replay only the displayed counterexamples and matrices. All newly submitted general theorems remain without Lean certificates. Original projective Gleason uniqueness and the derivation of the physical matrix/effect/instrument assumptions remain open. No commit, push, PR, merge or provider inference occurred in this review.
