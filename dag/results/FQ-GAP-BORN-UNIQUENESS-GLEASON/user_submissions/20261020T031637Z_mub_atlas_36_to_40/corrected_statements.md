# MUB-36--40: corrected conditional statements

Status: written supporting mathematics; general Lean verification pending. No quartet exclusion or positive value of delta* is proved here.

## MUB-36. Exact reduction and allowed normalizations

Let X0 consist of 6-by-6 complex matrices with every entry of squared modulus 1/6, and X=X0 intersect U(6). Then (I,U1,U2,U3) is a MUB quartet iff Ui in X and Ui*Uj in X0 for each distinct i,j. Any quartet can first be sent to this form by common unitary rebasing. Independent right monomials and common left monomials preserving the standard basis let U1 be dephased, with first row/column 1/sqrt(6). Its remaining 25 phases define an ambient torus T^25; unitarity remains an additional constraint.

Common conjugation and permutations of the three nonstandard basis labels preserve all constraints. Naive componentwise transposition does not. For exact triples a valid coupled map is

    (U,V,W) -> (U^T, U^T conjugate(V), U^T conjugate(W)).

Proof: rebase the four bases (I,U,V,W) by U*, conjugate them all, then relabel the standard basis first. The resulting four are (I,U^T,U^T conjugate(V),U^T conjugate(W)). This proof uses U unitary and the complete tuple constraints; it does not give an unconditional action on nonunitary box centers.

A concise exact counterexample to naive transpose uses H=[[1,1],[1,-1]]/sqrt(2) and V=diag(1,i)H. They are flat unitaries and H*V is flat, while conjugate(H)V^T=diag(1,i) is not. Tensor with a qutrit MU pair for a dimension-six pair counterexample (see exact_checks.py). No fourth basis is produced by this example.

## MUB-37. Attainment, zero set, and matching bridges

For U in X0 let f(U,V,W) be the maximum of the three squared-modulus defects in the submission, with V,W in X. Put D(U)=min f(U,V,W), E(U)=||U*U-I||max-entry. X0 is compact; X is a nonempty compact subset. Thus D's minimum is attained, and the quartet condition with first Hadamard U is E(U)=D(U)=0.

For fixed V,W, only the U*V and U*W terms vary. Each column has norm one. The reverse triangle inequality for squared absolute inner products gives

    | |<u,y>|² - |<u',y>|² | <= 2||u-u'|| <= 2||U-U'||op.

Taking maxima and then minima in both directions gives |D(U)-D(U')|<=2||U-U'||op.

For E, write u_a,u_b and u'_a,u'_b for columns. Then

    |<u_a,u_b>-<u'_a,u'_b>| <= ||u_a-u'_a|| + ||u_b-u'_b||
                                    <= 2||U-U'||op.

The max-entry norm and its reverse triangle inequality give the stronger bound |E(U)-E(U')|<=2||U-U'||op. This requires unit column norms, which hold everywhere in X0; it does not assume U unitary.

If k entries vary with radian phase distance at most rho, then

    ||U-U'||op <= ||U-U'||F <= sqrt(k/6) rho.

For k=25, both D and E have phase Lipschitz constant L=10/sqrt(6). A point lower bound ell>0 excludes the whole closed box if ell-L rho>0. This justifies rho<ell sqrt(6)/10. If only the manuscript's weaker E constant is used, use rho<ell/10 instead.

For exact rational box coordinates use turns t=theta/(2 pi), with endpoints identified. A conservative rational Lipschitz constant for both functionals is 32: 20 pi/sqrt(6)<10 pi<220/7<32. Hence ell-32 rho>0 is a sufficient purely rational bridge comparison, once the point lower bound ell is certified. These are sufficient constants, not claims of optimal Lipschitz constants.

## MUB-38. Finite positive-margin cover, conditional on nonexistence

Let delta*=min_(U in X) D(U). By continuity and compactness, no quartet exists iff delta*>0.

Assume delta*>0. In X0 let A={D>delta*/2}. This open set contains X. If C=X0 minus A is nonempty, it is compact and disjoint from X, so eta0=min_C E>0. Set B={E>eta0/2}. Then A union B=X0. If C is empty, A alone covers X0. Pull this open cover back to the compact dephased phase torus. A finite refinement by sufficiently small closed boxes exists with each box contained in A or B. Write eta=eta0/2 in the nonempty case: each box has D>=delta*/2 or E>=eta. This repairs the original proof's loss of constants.

Using normalized turns gives rational box endpoints by density; split wrapped boxes at 0=1. Positive slack lets each selected center admit a rational positive lower bound and a smaller radius satisfying MUB-37. This is an existence argument about true bounds. It does not provide their values, an effective runtime bound, or a particular certificate format for computing D. Any actual run must supply independently checked point lower bounds and exhaustive coverage.

Conversely a finite exhaustive cover by correctly tagged positive-margin boxes excludes all dephased first Hadamards and hence every quartet. Three MUBs already exist in dimension six (tensor the standard qubit and qutrit three-basis constructions). Therefore such an exclusion implies mu(6)=3 without needing the external upper bound five.

## MUB-39. Exact threshold logic and sound outer search

For delta>0 define S_<delta(U) to be flat vectors v whose six squared-overlap defects with U are all strictly below delta. Then

    D(U)>=delta iff no V,W in X have every column in S_<delta(U)
                    and every cross-defect of V*W strictly below delta.

Proof: D<delta iff an attained minimizer has all three maximum defects <delta; the reverse direction follows by evaluation. A closed S_<=delta enclosure is a larger candidate set. Excluding all such pairs still proves D>=delta, but it is a stronger sufficient test, not the same iff.

Every flat vector has nonzero first coordinate, so multiplication by a unit phase can set v0=1/sqrt(6), leaving five turns. A finite rational outer box cover must include all gauge-fixed candidates. Assign six column vectors to each of V,W; assignments must permit box reuse unless a rigorous occupancy bound rules it out. Reject an assignment only when an outward enclosure proves a required equality impossible (for example zero excluded from an orthogonality interval) or a required strict inequality impossible. Retaining an impossible assignment is safe but may prevent closure. Discarding a feasible one is unsound.

To prove D>=delta, an exhaustive search must eliminate every possible twelve-column assignment. To exclude a center with a positive margin, choose delta>0 and attach the verified complete search receipt. A feasible approximate or exact pair gives only an upper bound on D.

Do not infer nonemptiness of S_0(U) from U's own columns. Do not infer an explicit margin from the mere report that a specialized exclusion exists. No measure-zero claim is made.

## MUB-40. Sufficient replay contract

An atlas proof requires:

1. A precise domain, gauge, closed/wrapped box convention, and rational endpoint encoding.
2. Optional symmetry maps with a proved constraint-preserving action and a verified orbit-cover argument; omit quotienting if covering the full torus.
3. A finite list of boxes with certified positive point lower bounds on E or D, including the actual inner search data for D-tagged boxes.
4. Sound exact/outward interval arithmetic for every rejection, including transcendental phase evaluation, gauges, strict endpoints, box reuse, and all branch/pruning rules.
5. A checked strictly positive bridge remainder for every box; rational constant 32 in turns is one sufficient choice.
6. Exact exhaustive coverage, including seams and boundaries. Search metadata, counts, hashes, compiler/runtime assumptions and source pins belong to the replay evidence.

This is sufficient, not the only admissible global proof architecture. An analytic or algebraic proof of the same universally quantified exclusion may have a different certificate. No existing external computation has been replayed by this bundle, and no D-tagged box or 25-dimensional cover is certified here.
