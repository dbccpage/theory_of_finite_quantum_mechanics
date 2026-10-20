# Review of the CC-26--CC-30 proof manuscript

## Verdict and evidence ceiling

Accept the Gaussian-rational normalization argument, exact Omega criterion, rational four-square classical lift, Choi-injectivity argument, and generalized Householder induction as written mathematics after the repairs below. Do not accept the manuscript unchanged. No general statement here is kernel-checked. These are conditional channel-algebra results, not a derivation of the physical CPTP postulate or Born uniqueness from the finite-QM ontology.

The original attachment is untouched. Corrections and additional arguments belong to the host review. In particular, the rational equal-Gram bridge below is an additional host argument, not text supplied by the user or a provider.

## CC-26: field, query model, and coefficients

The imaginary probes contain i, so they are not matrices in M_d(Q). Their basis inversion works over Q(i). For Q use diagonal probes and real plus probes, a basis of the real symmetric matrices, with d(d+1)/2 elements. Under the Choi/CP hypothesis, the trace effect Phi†(I) is symmetric and those probes suffice. They do not span all of M_d(Q).

The manuscript infers minimality from the existence of a basis. That establishes sufficiency, not the lower bound. A lower bound can be supplied for scalar trace-normalization queries over unrestricted CP maps; the corrected note states the model and proves it. Extra promises can reduce the number: for a CP trace-nonincreasing map, equality on a single faithful state forces TP.

Scaling and mixing coefficients must preserve the carrier. For Q and Q(i), a real scalar in the field is rational. These classes are rationally convex; an arbitrary real mixture can leave them. The exact fixture lambda=sqrt(2)/2 mixing Id and dephasing makes the E01 coefficient irrational. This irrational fixture is intentionally rejected as outside the stated field; admitted channel examples are exact over Q(i).

## CC-27: a strict sufficiency statement and one incorrect value

The exact criterion Omega=Delta Phi (Id-Delta) Psi Delta=0 is correct. So are the no-creation and no-detection sufficient conditions. But term-by-term annihilation of every supported E_ab is stronger than Omega=0. Contributions can cancel. The exact replacement is that Delta Phi vanishes on the image of the actual coherence map, not on every matrix unit occurring in its support.

The independent counterexample uses U=[[3,4],[-4,3]]/5 and V=[[3,4i],[4i,3]]/5. Both are unitary. Psi=Ad_U creates E01+E10 coherence, while Delta Ad_V(E01)=diag(-12i,12i)/25 and the E10 image is its negative. Omega vanishes, despite both individual detected terms being nonzero. The composed shadow is [[337,288],[288,337]]/625, equal to S_V S_U. This directly refutes the manuscript's phrase 'exact content ... written positionally'.

In the 3D example, Delta(B E12 B*)=(12/25)(E11-E22), not (12/25)E11 (zero-based indices). The omitted term is forced by trace preservation. The example remains a valid sufficient-condition example.

Kernel matrices always multiply associatively. The shadow assignment can fail to preserve quantum composition. Pairwise Omega conditions are sufficient for iterated factorization, not necessary for an overall identity; this must replace 'the condition must be imposed at each junction'.

## CC-28: the target category and scalar output

The rational four-square construction and its 4*nnz bound are valid, including the eleven-operator S7 example from the earlier script. Composition and E(I)=Delta are correct. An ordinary functor into full Chan must preserve the ambient identity Id_Md; the assignment E does not, so the phrase 'faithful functor ... does not preserve identities' is inconsistent.

Take diagonal algebras, or objects (M_d,Delta_d) with dephased CPTP arrows Phi=Delta_e Phi Delta_d. Then Delta is the identity, E is full and faithful for the rational stochastic hom sets, and composition is correctly typed. Merely calling it 'not full' refers to the ambient full channel hom sets and cannot be carried over to the corrected target.

For a column-stochastic 1-by-d matrix every entry is 1; E(S)=Tr. A general weighted diagonal functional is not TP unless all weights are 1. The d=1 state preparation formula is fine.

## CC-29 and CC-30: adjoints and rational mixing

Choi injectivity, composition/tensor descent, and the input-first formulas are valid. HS adjoints preserve CP, but send CPTP maps to unital CP maps. They need not preserve TP. For the normalized qubit reset channel Phi(X)=Tr(X)E00, the dual sends E00 to I, whose trace is 2. Thus the CPTP slice is not closed under this adjoint. All CP Choi classes are.

CC-30's completion proof works over the stated fields, including its separate v=e1 case. It completes a supplied orthonormal-column isometry. It does not by itself construct a rational intertwiner between arbitrary Kraus presentations. Choosing an orthonormal basis of a rational subspace may leave the field. The corrected note fills the missing step via equal-Gram row matching without square roots. After padding both families to R=max(r,s), it produces an R-by-R unitary over K. A rectangular isometry in an arbitrarily chosen direction is not available when its source dimension exceeds its target dimension.

## Reported checks and provenance

The manuscript says 67 checks, all PASS. The only prior companion script supplied in this chat printed 66 PASS lines in each mode (receipts and outputs snapshotted in inputs). No revised companion script accompanied this attachment. Record the new count claim as unverified, not as an observed result. The earlier corrected suite had 137 controls; that receipt belongs to the earlier bundle and was not rerun or promoted here. This bundle adds 61 exact controls and four invalid-input refusals in normal and optimized Python, both exit 0.

The standard complex CP/Choi, adjoint, and Kraus-presentation facts can be compared with John Watrous, The Theory of Quantum Information (author-hosted draft), chapter 2: https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf . Its complex unitary mixing theorem alone does not establish rational entries; the field-preserving proof here supplies that additional argument. Conventions are input-first throughout this bundle.
