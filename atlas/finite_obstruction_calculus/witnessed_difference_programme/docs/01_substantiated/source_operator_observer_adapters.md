# Original operator and observer-object semantic adapters

AuthorityEffect: None. This note addresses the actual recovered source texts,
not a finite enumeration substituted for their operator semantics.

## Source identity and fields

The source-recovery inventory binds the exact original bytes of
`vector_and_quantum_observer_geometries.md`, `the_observer_object.md`,
`what_the_hell_is_an_observer_v001.md`,
`obstruction_diagnostics_observer_control.md`, and
`wd3_operational_observer_level_repair.md`. The originals were inspected in
`/workspace/.wdp-source-recovery/004_calculus_of_observers_and_observation/merged_sources/`.
Their retained source inventory, rather than current rewritten deposit prose,
is the custody reference. Recovery alone is documentary custody, not semantic
validation.

The observer-object original is the nine-tuple
`(K,F,R,delta,d0,d1,J,M,tau)` with a separately declared linear `Adm`.
The general-media original is also a nine-tuple, replacing `F` by a state
presheaf `S`; it is not a six-component memory machine. The triple
`(A,M,Jlocal)` uses `A` for aggregation, **not** admissible repairs.
Assembly folds aggregation and local gauges into global `J` and imports the
carrier, repair budget and terminalizer independently.

| Original field | Actual operator interpretation | Executable boundary |
| --- | --- | --- |
| K | finite vertices, directed incidence edges | state array and `OperatorComparison {from,to,channel}` |
| F/S | finite Hilbert stalks and their real traceless Hermitian perturbation spaces | nonzero, possibly heterogeneous matrix dimensions; no finite-state enumeration |
| R | declared CPTP `r_ba: Herm(H_b) -> Herm(H_a)` | existing checked `ExactKrausChannel` |
| delta | `r_ba(rho_b)-rho_a`, or separately declared observed edge cochain | `operator_section_problem`, or explicitly distinct `OperatorRepairProblem.defects` |
| d0 and Adm | `r_ba(alpha_b)-alpha_a` restricted to declared real linear repair span | actual vertex repair generators mapped to actual edge generators |
| d1 | optional coherent 2-cell operator with `d1 d0=0` | never invented by this adapter; closure requires its separate checked source data |
| J | sum over edges of half trace norm, with optional positive weights | positive rational weights and checked exact Jordan witnesses |
| M | transformations with repair-image transport and gauge compatibility | actual CPTP maps and checked generator intertwining expansions |
| tau | declared evaluator status function or policy | independently owned terminalization; no status/authority follows from norm alone |

The source supplement explicitly uses `sum_e ||h_e||_1/2`, not unscaled
`sum_e ||h_e||_1`; the verifier preserves this convention. Repairs are
Hermitian **perturbations**, not density states, and may have negative eigenvalues.

## Full finite-dimensional representation and quotient theorem

For any finite graph and finite-dimensional complex Hilbert stalks, choose
real bases of `Herm_0(H_v)` and `Herm_0(H_e)`. A source `d0|Adm` becomes a
finite real matrix B, retaining all coherence coordinates. Its repair image
W is a real linear subspace of the finite-dimensional edge space X.
Coordinates are a linear bijection, not a diagonal shadow or a finite sample.
Set `J(h)=sum_e w_e ||h_e||_1/2`, with `w_e>0`.
Define `Phi([delta])=inf_{w in W} J(delta-w)`.

This is well-defined: translation by any member of W bijects the feasible
set. Because J is a norm in finite dimension, its closed bounded sublevel
sets are compact. The affine feasible set `delta-W` is closed, so its
minimum exists. Zero magnitude is equivalent to `delta in W`. The actual
quotient is X/W; neither J nor tau changes its equivalence classes.
These statements cover arbitrary finite real/complex source coefficients.

For arbitrary functional J, the same translation proof establishes
representative independence if the extended infimum is defined, but neither
attainment nor `Phi=0 iff delta in W` follows. For a nonlinear repair set A,
the exact necessary and sufficient condition for this translation proof is
`d0(A)+w=d0(A)` for every proposed gauge shift w. A source with A={0,1},
d0=id, J=absolute value violates invariance: Phi(0)=0 and Phi(2)=1 although
repeated declared unit shifts would identify them. One must use the actual
linear repair span or supply a different equivalence proof.

An arbitrary gauge does not license canonical residual choice. The trace
norm is not strictly convex. For scalar diagonal copies on two edges with
fixed circulation c=1, every residual `(t,1-t)` for `0<=t<=1` minimizes the
edge-additive norm. Thus a downstream Xi/residual-based policy requires its
declared tie-break; the adapter does not invent one.

## Exact trace-gauge primal/dual theorem

For Hermitian h, write its spectral Jordan decomposition h=P-N with
P,N positive semidefinite and PN=0. Then `||h||_1=Tr(P)+Tr(N)`.
This decomposition exists for every finite complex Hermitian operator.
The trace-gauge dual ball on full Hermitian space is
`-w_e I/2 <= phi_e <= w_e I/2`. For traceless h one may equivalently use an
effect E and `phi=w_e(E-I/2)`; scalar identity shifts do not change pairing.

For any such dual tuple annihilating W and any repair Bc,
`sum Tr(phi_e delta_e)=sum Tr(phi_e(delta_e-(Bc)_e)) <= J(delta-Bc)`.
The inequality follows by pairing each positive and negative Jordan part
with the two PSD bounds; it needs no numerical eigenvalue approximation.
If a supplied residual, Jordan parts, dual tuple and repair coefficients
give equality, they certify the global quotient minimum over the **entire
real repair span**, including irrational coefficients. This is sufficient
without any solver oracle.

It is also necessary at theorem level over the full real/complex domain.
At an attained minimizer the continuous convex norm J has a subgradient
phi annihilating W: restrict to the affine subspace and use finite-dimensional
convex optimality, or extend a norming functional on the quotient by
Hahn–Banach. Its edge components lie in the dual balls, and it pairs with
the residual to J(residual). Together with the spectral Jordan parts this
is exactly the asserted certificate. No rational witness existence follows.

`TraceObserverWitness::verify` replays the actual residual equation,
Hermiticity, shape, trace-zero defect/repair domains, positivity of P/N,
PN=0, exact polar bounds, annihilation of every repair generator, and
primal/dual equality. `OperatorRepairProblem` has no trusted objective or
receipt flag. All supplied rational entries and coefficients must have
positive denominators and be canonical; `BigRational::new_raw(1,0)` is
explicitly refused before arithmetic. A malformed matrix is refused before
access. The native owner reuses existing exact Hermitian positivity and
Gaussian-rational matrix operations; WDP only delegates.

The executable subdomain is Q(i) operators with Q-valued supplied witnesses.
It is nonempty and includes genuinely nondiagonal certificates. It is a
partial certificate interface, not a complete spectral algorithm. For
`h=[[1,1],[1,-1]]`, h has eigenvalues plus/minus sqrt(2), so its positive and
negative parts involve sqrt(2) and its half trace norm is sqrt(2). A Q(i)
Jordan payload cannot represent them: P+N=|h|=sqrt(2)I. This case remains
covered by the theorem, while this rational verifier refuses a fabricated
rational Jordan witness. A real/algebraic spectral host would be an explicit
additional implementation, not a silently rounded certificate.

## Comparison transport: necessary and sufficient licensing hypothesis

A linear map Lambda descends from X/W to X'/W' exactly when Lambda(W)
is contained in W'. Necessity follows by transporting [w]=[0]; sufficiency
follows by transporting differences. In source generator coordinates this
is exactly the existence of an expansion `Lambda B = B' T`.
`verify_operator_repair_transport` checks actual CPTP edge channels, actual
target defects, and every column of this equation. It also requires target
weights no larger than source weights.

Positive trace-preserving maps contract trace norm on Hermitian operators:
if h=P-N is its Jordan decomposition then
`||Lambda(h)||_1 <= Tr(Lambda(P))+Tr(Lambda(N))=||h||_1`.
CPTP is the declared stronger source hypothesis. Applying this pointwise,
and the repair inclusion, gives `Phi'([Lambda delta])<=Phi([delta])` by
transporting every feasible repair and taking the infimum. The native
verifier certifies hypotheses for this theorem, not a numerical estimate.

Without repair inclusion even the identity channel need not contract
quotient obstruction: source W=X gives Phi=0 while target W'=0 gives
Phi'(nonzero delta)>0. Without gauge calibration target weights 2 instead
of 1 double the same obstruction. Without trace preservation the CP map
`h -> 2h` expands trace norm. Without positivity trace preservation alone
does not guarantee contraction: on diagonal two-state vectors the matrix
`[[2,-1],[-1,2]]` preserves total mass and triples traceless differences.
No transport, invariance or physical channel claim is paid by shape alone.

## State-generated data and the reference-section obstruction

There is a source distinction that a free-edge fixture must not erase.
Suppose a compatible trace-one reference section sigma exists:
`r_ba(sigma_b)=sigma_a`. For any density section rho, `alpha=rho-sigma`
is a traceless Hermitian perturbation and
`d0 alpha=delta(rho)-delta(sigma)=delta(rho)`.
If Adm contains that alpha (in particular if full traceless repairs are
declared), Phi(delta(rho))=0. Identity restrictions admit a common reference,
so arbitrary nonzero cycle circulation cannot be presented as their actual
state-generated defect. It is independent edge data or restricted repairs.

This is not a proof that all CPTP-comparison sources are trivial. A concrete
actual nonzero fixture uses three qubit vertices, with edges 0->1 and 0->2.
The first comparison resets its input to |0><0|, the second resets it to
|1><1|. All source states are |0><0|. Defects are (0,Z), with
Z=diag(-1,1). Both comparisons kill traceless inputs, so the full repair
image is `(A,A)` for any traceless Hermitian A (overall sign is irrelevant).
The lower witness `(-Z/2,Z/2)` annihilates this full image and gives value1.
Residual `(0,Z)` attains value1. The two resets require incompatible reference
states at vertex0, so no compatible sigma exists. This fixture uses actual
offered state fields and comparison channels, not an invented diagonal shadow
of an unspecified channel. The native test declares the full X,Y,Z
repair-image basis at vertex0; all remaining vertex perturbations are killed
by the reset comparisons.

## Closure, control and interpretation boundaries

For any optional linear closure D, `D(delta+Bc)=Ddelta` holds for all data
and repairs iff DB=0. This is the exact necessary/sufficient condition for
closure descent. It cannot be assumed merely because graph cycles exist.
The source ratio Gamma/Phi is undefined at Phi=0; an epsilon-stabilized
controller ratio is a separately declared policy convention.

The recovered control source specifies normalized channels, costs,
tolerances, protected set, Rmax, stabilizer and optional Xi tie-break.
Those are extra actual fields, not derivable from operator geometry.
The native theorem supplies a geometric channel when its source hypotheses
are met; it does not supply transition probabilities, detector adequacy,
missing Xi selections, or terminal authorization. Weighted-score improvement
alone does not protect channels: `(Phi_geom,Phi_curv)=(2,0)` to `(0,1)`
decreases their equally weighted sum while worsening curvature. Guarded
control requires the declared per-channel inequalities and evaluator policy.

For M, an evaluation-preserving quotient automorphism additionally needs
bijective repair-image transport and invariance of the declared gauge. CPTP
contraction alone is not a reversible symmetry and does not select a gauge:
both half trace norm and twice half trace norm are CPTP-monotone. A declared
operational binary-discrimination normalization can select the scale and
trace norm; the original source leaves that selection conditional/open.
Neither a theorem about these observers nor corpus coverage derives Born
selection, physical quantum ontology, observer-independent authority,
consciousness, or general infinite-dimensional operator theory.

For an infinite-dimensional extension, norm-closed repair image is necessary
for `Phi=0 iff delta in W`; without it the quotient is only a seminormed
algebraic quotient. For example W=finitely supported sequences in ell2 is
dense and proper, so every coset has zero distance but W is not all ell2.
Even closed subspaces of general Banach spaces need not attain nearest
points. The original finite-dimensional source avoids these issues; native
finite certificates do not establish such an extension.

## Vector and enriched operator source scopes

The original vector carrier is `(R^k)^V -> (R^k)^E`, not a list of report
labels. Choosing bases identifies its coboundary with a finite real matrix
and its repair image with a real linear subspace exactly. The coordinate
gauge is edge-additive coordinate absolute value; the vector gauge is
edge-additive Euclidean length. They are distinct norms on the same quotient.
Finite norm-duality gives the corresponding annihilating polar witnesses:
coordinate dual boxes versus Euclidean dual balls. Norm attainment and
quotient well-definedness follow as above; irrational Euclidean lengths
require a real/algebraic host rather than rational scalar rounding.

With identity stalk restrictions `d0=B tensor I_k`, a common orthogonal
stalk action R gives `(I_E tensor R)d0=d0(I_V tensor R)`. It preserves the
Euclidean gauge and its quotient norm. Independent edge rotations generally
fail repair-image transport. For nonidentity restrictions, common rotation
alone is insufficient; one needs its actual intertwining. Rotation invariance
does not hold for the coordinate gauge: the source's circulation `(1,1)`
reads2, whereas its pi/4 rotation `(0,sqrt(2))` reads sqrt(2).

The source's declared Hilbertization is an extra inner product, not an
identification with its edge-additive gauges. For a finite Hilbert complex,
`L0=d0* d0` and `L1=d0 d0*+d1* d1` inhabit different degrees. If degreewise
unitaries define `d0'=U1 d0 U0*`, `d1'=U2 d1 U1*`, direct multiplication gives
`L0'=U0 L0 U0*`, `L1'=U1 L1 U1*`. Thus spectra with multiplicities are equal;
the analytic exponential series gives `exp(-tL1')=U1 exp(-tL1) U1*`.
This is exact finite-dimensional complex mathematics, not a rational
transcendental implementation or an inference from one degree to another.
For an independently offered second complex, the relevant intertwining
must be checked; no relation follows from a mere matching matrix shape.
The source's numerical real degree0 solver does not certify complex
degree1 spectral claims. This source item retains its explicit conformance/
admission boundary, independently of observer-packet semantic coverage.

The source also declares a dg Lie algebra enrichment. It is not a linear
repair quotient and must not be encoded as one. Its curvature is
`F(tau)=d tau+[tau,tau]/2`. Over characteristic0, with x of degree0,
the flow `tau'(t)=[x,tau(t)]-dx` has the source solution
`tau(t)=exp(t ad_x)tau(0)-integral_0^t exp(s ad_x)dx ds`.
The derivation rule and graded Jacobi identity give
`F'(t)=[x,F(t)]`: the terms `[dx,tau]` and `[tau,dx]` cancel because both
have degree1, and `[tau,[x,tau]]=[x,[tau,tau]]/2`.
Hence `F(tau(t))=exp(t ad_x)F(tau(0))`. The exponential is invertible,
with inverse exp(-t ad_x), so a nonzero curvature cannot become zero.
For nilpotent ad_x these expressions are finite polynomials and the
integral is termwise rational division; in the source's complete filtered
pronilpotent setting they are formal convergent series. Outside declared
typing/convergence conditions the action has no domain and must be refused.
This conditional proof supplies the source enrichment's actual gauge
equivariance argument. It does not turn nonlinear curvature or a completed
filtered Lie algebra into the native finite matrix certificate, and does
not discharge a separate source release/admission process.

A precise convergence qualification matters: nilpotence of degree0 Lie
algebra alone does not imply that ad_x is nilpotent on every other degree.
Take degree0 `Q x`, degree1 `Q v`, bracket `[x,v]=v`, all other brackets zero,
and differential zero. Degree0 is abelian, but `ad_x^n(v)=v` for every n.
The finite real/complex analytic host still has a convergent exponential;
a purely rational finite-polynomial host does not. A filtered pronilpotent
host must declare the filtration on the whole action. Thus the source's
degree0-nilpotent shorthand is not treated as a standalone rational
convergence certificate.

## Validation artifacts

Native owner: `omega_quantum_physics/src/trace_observer_certificate.rs`.
Thin adapter: `omega_wdp/src/operator_observer_adapter.rs`.
Targeted native tests: `omega_quantum_physics/tests/trace_observer_source.rs`.
They include a non-diagonal Pauli-X cycle certificate, forged polar/Jordan/
annihilation/residual/shape/domain refusals, actual reference flattening with
negative perturbations, incompatible reset comparisons with nonzero actual
obstruction, and paid/refused repair transport. Paper Python witnesses are
fixed rational fixtures, not duplicated spectral or optimization algorithms.
Production receipt (2026-10-01):

- `cargo test -p omega_quantum_physics --test trace_observer_source -j2`: 5 passed.
- `cargo test -p omega_wdp --test source_operator_observer_adapter -j2`: 1 passed.
- `PYTHONPATH=code python -m pytest code/unit_tests/test_source_operator_observer_witness.py -o addopts='' -q`: 2 passed.

Rust used the actual workspace and production dependencies, with existing
contract warnings disclosed by the normal build; no gate was bypassed or
digest rewritten for these tests. No new Lean claim about trace norms or
spectral calculus is made. The general operator and analytic enrichment
proofs above are prose mathematics; the actual native checker establishes
the declared rational certificate hypotheses only.
