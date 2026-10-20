# Review verdict

The submission is useful supporting mathematics, not a completed exclusion. Accept the exact reduction, existence/continuity of the defect minimum, and compactness logic after the repairs below. Do not accept the manuscript verbatim or promote any numeric/global claim. No new general Lean proof or global dimension-six computation was performed.

## Literature and status

The primary [formalization scope document](https://raw.githubusercontent.com/openai/math/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/docs/266.md) distinguishes the paper's claimed bound three from the linked weaker bound five. This review inspected that scope, not an executed Lean build or certificate replay. Record the five-bound as an externally documented formalization, not as locally independently verified here.

The 'atlas and scripts are not public' sentence is too broad and stale. The cited [issue discussion](https://github.com/google-deepmind/formal-conjectures/issues/6918) records an October 11 missing-code observation at a specific release commit, then an October 14 author report of a public independent reproduction with code/log/data DOIs. The latter explicitly retains a machine-arithmetic assumption and says it is not Lean-formalized. Both linked Zenodo records were inaccessible through this browsing tool; availability and correctness of their payloads were not independently established here. Preserve the historical missing-code observation, the later claimed reproduction, and the access limitation separately. Do not assert global present-day nonavailability or that no one has proved the result.

The [SoS paper](https://arxiv.org/abs/2606.13903) concerns the specified degree-four vector encodings, not every polynomial formulation. The [2012 discretization paper](https://arxiv.org/html/1201.0640) gives the ambient phase-grid approach and a Fourier-family exclusion; its authors are Jaming, Matolcsi and Mora, not the five-author list in the submission. Its historical classification/status remarks are not a fresh classification audit. [More mutually unbiased bases](https://arxiv.org/abs/2609.40311) concerns constructions in other dimensions; it is not a proof of the six-dimensional upper bound three. Numerical optimized distances are evidence from optimization, not a certified global maximum merely because a decimal is below one.

Calling this Zauner's dimension-six MUB conjecture is supported by [primary literature](https://arxiv.org/abs/2103.08703); distinguish it from the different SIC conjecture associated with the same name.

## MUB-36: normal form and symmetries

The quartet/Hadamard reduction and dephasing are correct. Twenty-five phases parametrize an ambient torus of dephased flat matrices, not twenty-five freely varying unitary Hadamard parameters. Orthogonality still imposes equations. Complete Hadamard classification is not required to define this exhaustive ambient torus.

With the standard basis fixed, common left monomial multiplication, independent right monomials, common conjugation and basis-label permutations are valid. Naively transposing every nonstandard basis is not valid. Exact local controls give both a qubit counterexample and a dimension-six tensor example with a zero overlap after transposition.

There is a valid coupled transformation for exact Hadamard triples: (U,V,W) maps to (U^T, U^T conjugate(V), U^T conjugate(W)). It comes from rebasing by U* followed by common conjugation and swapping the standard/first basis labels. Thus transposing the first Hadamard can be legitimate, but the other matrices must transform too. It is not an entrywise transpose action on the ambient flat matrices or their coordinate boxes. Any symmetry reduction must specify and verify its actual action and the set on which it acts.

Q(i) is not an adequate blanket carrier for the normalized complex matrices. This does not force interval methods as the only exact representation: algebraic number coordinates and polynomial real/imaginary coordinates are alternatives. Rational turns as phase coordinates do not mean the resulting amplitudes are Gaussian-rational.

## MUB-37: retain D and strengthen E

X is compact and nonempty; the finite Fourier matrix supplies nonemptiness. Hence the minimum defining D is attained. The submitted 2-Lipschitz bound for D in operator norm is correct. The stated bound 2 sqrt(6) for E is valid but loose.

Multiplying that loose E bound by sqrt(25/6) gives 10, so its radius implication is rho<eta/10, not eta sqrt(6)/10. However the latter radius is still valid after an explicit stronger argument: since every column of U and U' has norm one, each entry of U*U-U'*U' is bounded by 2||U-U'||op. Therefore E itself is 2-Lipschitz in this metric. Both bridges then share the phase constant 10/sqrt(6), and rho<margin sqrt(6)/10 follows. The corrected note supplies this proof; no unsafe radius is retained by merely accepting the manuscript's arithmetic.

Closed boxes require a strictly positive remaining margin. A point lower bound is already a universal claim about all V,W in X. A locally optimized feasible V,W supplies an upper bound on D, not a lower bound.

## MUB-38: compactness is conditional, and constants need slack

No quartet iff min_X D>0 is correct. The proof's intermediate atlas guarantees D>=delta*/4 and E>=eta/2, while its statement claims delta*/2 and eta. Those constants do not match. A finite open-cover argument fixes this cleanly: D>delta*/2 contains X; on its compact complement E has a strictly positive minimum. Cover the torus by small boxes subordinate to these two open sets. The written correction states the empty-complement case and rational torus endpoints.

The half-open angle cube is not itself compact. Use the phase torus, or a closed cube with endpoints identified. For rational box corners, normalized turns in [0,1] avoid the irrational endpoint 2 pi. Existence of a finite positive-margin cover is a qualitative compactness conclusion; actual rational point lower-bound certificates and sound coverage objects remain required inputs for replay.

## MUB-39: strict thresholds and enclosure semantics

D>=delta means no pair has all three defect terms strictly less than delta. The submission instead permits the first two defects to equal delta via S_delta and makes only the third strict. That gives a sufficient no-candidate condition for D>=delta, not the asserted equivalence. The scalar singleton min-max example in the controls exposes this endpoint mismatch; it is a logical control, not a purported dimension-six quartet.

Define S_<delta using strict inequalities for the exact equivalence. Closed outer enclosures of S_<delta (or the stronger S_<=delta) can still support a sound exclusion if every possible vector is covered and every discarded candidate has a valid interval reason. 'Twelve points of the enclosure' must mean actual vectors assigned to sound boxes, not a sampled list or box centers. Multiple columns may occupy the same vector box; a clique search without reuse is unsound unless occupancy is separately bounded. Orthonormality, cross-unbiasedness and the first-coordinate phase gauge must be checked with necessary conditions that never discard a feasible tuple.

A basis's own columns are not unbiased to that basis: U* u_j=e_j. They do not prove S_0(U) nonempty. For arbitrary nonunitary U in X0, the manuscript's no-emptiness assertion is unsupported and is not imported. No measure on the possibly stratified space X was specified, so 'measure zero until upgraded' is not established. A qualitative positive D already implies a nonempty open exclusion neighborhood; an explicit lower margin is needed to compute its certified radius.

## MUB-40: one sufficient proof format, not the only route

A sound finite atlas with exhaustive coverage and verified bridges is a sufficient certificate format. It is not the definition of every possible proof. The submission itself mentions Positivstellensatz certificates; an analytic or algebraic global proof can bypass a grid. A validated symmetry quotient is optional if the full domain is covered. The external bound five is unnecessary for atlas exclusion to imply mu(6)=3: the independently constructed three-basis lower bound and exclusion of four suffice.

The corrected replay contract rejects uncertified point margins, incomplete covers, invalid symmetries, and heuristic rejection rules. Its toy coverage controls are not an implementation or verification of a 25-dimensional atlas. Gap 9 remains open in this project's evidence ledger; this is a local acceptance status, not a claim to adjudicate the entire current literature.
