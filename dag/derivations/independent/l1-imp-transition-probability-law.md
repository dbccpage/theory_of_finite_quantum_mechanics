Status: AI-drafted, awaiting human review.

# Transition-probability law: a conditional hypothesis map

AuthorityEffect: None. Outcome: **Narrowed**, with countermodels to specified
candidate implications. The target remains **IMPORTED_ASSUMPTION**.

The carrier is \(V_n=\mathbb Q(i)^n\), with its supplied positive Hermitian form.
Write \(N(x)=\sum_j |x_j|^2\) and
\(p(x,y)=|\langle x,y\rangle|^2/(N(x)N(y))\) for nonzero vectors.
The existing kernel identifies this with the normalized Born readout of the
rank-one effect \(P_x\) in state \(y\). Rays identify nonzero scalar multiples.
These spaces are finite dimensional; their ray sets are not finite.

All new declarations are in
[TransitionProbability.lean](../../../lean4/TransitionProbability.lean),
namespace TransitionProbability. Every hypothesis below is explicitly
defined there. No sufficient theorem takes TpPreserving as an input.

## Hypothesis map

| Hypotheses | Result and declarations | Boundary |
|---|---|---|
| LinearLift T, OrthogonalCalibration T, NonzeroAnchor T i₀ | linear_calibration_tpPreserving; calibration_similarity identifies the Gram matrix | Arbitrary positive dimension, but a linear lift is supplied |
| Nonvanishing T, TomographicStatistics T | tomography_sameRay, tomography_tpPreserving | Fixed-frame probabilities for finitely many effects, in **every** nonzero state; actually fixes each ray |
| Nonvanishing T, dimension one | oneSector_sameRay, oneSector_tpPreserving | The nonzero ray space has one point |
| Born rule, reversibility, ray compatibility, norm preservation, basis statistics, covariance under the two-sector report swap, orthogonality in both directions, and finite orthogonality calibration | Insufficient, even jointly: insufficient_operational_package, countermodelRayEquiv | Explicit global countermodel on dimension two |
| The previous countermodel also preserves all real pair-probe statistics | Still insufficient: conditionalConjugation_realProbes, conditionalConjugation_not_tpPreserving | Imaginary pair probes detect it |
| Born rule, linear lift, reversibility and preservation of the full subspace lattice as an order isomorphism | Insufficient: insufficient_lattice_package, stretchLattice, stretchRayEquiv | Order/meet/join preservation; orthocomplement preservation is **not** claimed |

BornRule is a static formula, not preservation of that formula under dynamics.
ReportSwapCovariant means \(T(Sx)=S(Tx)\), where \(S(x_0,x_1)=(x_1,x_0)\).
The identity and this swap exhaust the two-sector relabelings. This does not
mean agreement of all transported effect/state statistics; that would restate
the target and is not used as a premise.

## Sufficient route: linear lift plus finite orthogonality calibration

LinearLift T says that a single Gaussian-rational matrix \(F\) acts on every
vector: \(T(x)=Fx\). This is explicit superposition structure, not a consequence
of the Born formula. OrthogonalCalibration T requires only
\[
 \langle Te_i,Te_j\rangle=0,\qquad
 \langle T(e_i+e_j),T(e_i-e_j)\rangle=0\quad(i\ne j).
\]
These are finitely many zero-probability tests, rather than an assumption about
all transition probabilities.

Put \(f_i=Fe_i\). The first tests make the Gram matrix diagonal. By linearity,
the second tests become
\(\langle f_i+f_j,f_i-f_j\rangle=N(f_i)-N(f_j)=0\).
Every diagonal entry therefore equals \(d=N(Fe_{i_0})\); the nonzero anchor
gives \(d>0\). Hence \(F^H F=dI\). The existing exact similarity algebra yields
\(p(Fx,Fy)=p(x,y)\). These steps are calibration_similarity and
linear_calibration_tpPreserving.

linear_calibration_wigner explicitly composes the new result with finite_wigner.
The conclusion is a similarity over the exact scalar field, not necessarily a
unitary: the existing scale obstruction remains unchanged. The identity
witnesses consistency of the premises. The countermodel below satisfies the
finite calibration but is not a linear lift (conditionalConjugation_not_linearLift).

## Sufficient route without a linear-lift assumption: fixed-frame tomography

ProbeStatistics x y asks for equality of probabilities against the families
\(e_i\), \(e_i+e_j\), and \(e_i+i e_j\), with distinct indices in the pair
families. TomographicStatistics T asks for these equalities between \(x\) and
\(Tx\), for every nonzero \(x\). The effect frame is held fixed.

Choose \(i_0\) with \(x_{i_0}\ne0\). Its basis probability and nonvanishing of
\(y\) force \(y_{i_0}\ne0\). Rescale both vectors to make their anchor coordinate
one. Equality of the anchor probability makes their squared norms equal.
Each other basis probability fixes the modulus of that coordinate. The real
pair probe fixes its real part:
\(|1+z|^2=1+2\operatorname{Re}z+|z|^2\).
The imaginary pair probe fixes its imaginary part:
\(|1-iz|^2=1+2\operatorname{Im}z+|z|^2\).
The existing coord_rigidity lemma discharges this calculation. The normalized
vectors coincide, so \(y\) is on the ray of \(x\).

Consequently \(Tx\) is a nonzero multiple of \(x\), and scale invariance gives
transition-probability preservation. This is a finite-effect separation
argument, but its premise fixes every ray. It is **not** claimed to be a
strictly weaker law than arbitrary transition-preserving dynamics. Neither
route qualifies as a derivation from primitive difference or as a campaign
Reduced outcome.

The tomography proof handles dimension zero vacuously: there are no nonzero
rays. The separate one-sector theorem handles the single-ray case.

## Countermodel: orthogonality, Born statistics and reversibility together

For every \(x\in\mathbb Q(i)^2\), define
\[
 T(x)=
 \begin{cases}\bar x,&|x_0|^2=|x_1|^2,\\x,&|x_0|^2\ne|x_1|^2.\end{cases}
\]
Conjugation leaves the branch condition unchanged, so \(T^2=\mathrm{id}\).
It preserves each coordinate norm and the total norm. This gives reversibility,
nonvanishing, and all basis-effect probabilities.

The condition is unchanged by any nonzero Gaussian-rational rescaling. On a
balanced ray the scalar is conjugated; otherwise it is unchanged. Thus the rule
descends to the actual quotient of all nonzero vectors:
countermodelRayEquiv has type Ray 2 ≃ Ray 2. It commutes with report swap.
Real pair probes cannot distinguish a vector from its conjugate, so their
fixed-frame statistics are also preserved.

If nonzero \(x\) is balanced and \(\langle x,y\rangle=0\), then
\(\bar x_0y_0=-\bar x_1y_1\). Taking squared norms and cancelling the nonzero
common coordinate norm gives \(|y_0|^2=|y_1|^2\).
Nonzero orthogonal pairs therefore lie in the same branch. Both members are
conjugated or neither is; orthogonality is preserved. The involution supplies
the reverse implication. Lean also handles zero-vector inputs.

Take \(a=(1,i)\), \(b=(1,2i)\). Then
\(N(a)=2\), \(N(b)=5\), \(\langle a,b\rangle=3\), and \(p(a,b)=9/10\).
Only \(a\) is conjugated, giving
\(\langle T(a),T(b)\rangle=-1\) and probability \(1/10\).
The imaginary probe \(a=e_0+i e_1\) has probability one in \(a\) and zero in
\(T(a)\). countermodel_probabilities and imaginary_probe_probabilities prove
the probabilities; the independent checker recomputes the arithmetic.

This refutes the listed candidate implications, including their conjunction,
on the entire dimension-two ray space. It is not a countermodel to an
unspecified collection of all repository primitives.

## Countermodel: preserving the subspace lattice

The linear equivalence \(D(x_0,x_1)=(x_0,2x_1)\) has inverse
\(D^{-1}(y_0,y_1)=(y_0,y_1/2)\). Its map on subspaces is a genuine order
isomorphism of Submodule GaussRat (Vec 2), constructed by Mathlib's
Submodule.orderIsoMapComap. stretch_lattice identifies its action on every
one-dimensional span; stretchRayEquiv constructs its ray bijection.

Nevertheless \(p(e_0,(1,1))=1/2\), while
\(p(D e_0,D(1,1))=1/5\). Subspace order and reversibility, even with a
linear lift and the Born formula, are insufficient. This example does not
preserve orthogonality, and says nothing about automorphisms of the entire
ordered interval of positive effects with its affine operations.

## Verification and scope

See [the Lean replay receipt](../../research/campaign_l1-imp-transition-probability-law_lean_replay.json).
The non-default Lake target uses Lean 4.35.0 and Mathlib
56a005855ea17e0b0958f73ec801ae140b0a1679. Each explicitly named source declaration has an axiom
report. Digests bind the accepted sources and output.

The [independent checker](../../../checks/independent/l1-imp-transition-probability-law.py)
uses standard Python and SymPy, with no repository imports. It checks symbolic
norm and probe identities, independently constructs Born projectors, recomputes
the witnesses, and tests a declared finite grid. Invalid-input rejection and
executable semantic mutations are exercised. Normal and optimized runs must
agree. Sampling does not replace the unrestricted Lean theorems. Artifact
scores do not certify the physical adequacy of an imported hypothesis.

## What is proved

The sufficient implications and their nonvacuity; global dimension-two ray
bijections with the stated preserved properties and failed transition law;
the one-sector boundary; separation of subspace order from probability
preservation. The existing Wigner theorem is used after obtaining its premise.

## What is assumed

The scalar field, vector carrier, Hermitian form and Born readout. A linear lift
and finite orthogonality calibration in one route; all-state fixed-frame
tomographic statistics and nonvanishing in the other. These remain supplied.

## What is open

An operational reason that the actual dynamics obeys either sufficient package,
or a sufficient package with less structural commitment. Orthogonality alone
for arbitrary ray bijections above dimension two is not decided here.
Orthocomplemented lattice automorphisms in those dimensions, affine
positive-effect automorphisms, and a freely evolving measurement frame are
not classified. The physical imported law, unitary-normalization gap and
continuous-time gap remain open.
