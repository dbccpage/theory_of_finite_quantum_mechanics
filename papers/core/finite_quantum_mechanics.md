<div align="center">

# Finite Quantum Mechanics

### Can Quantum Mechanics Be Presented on a Finite Carrier — and If Not, Exactly Where Does It Break?

**Author:** Jeremy H. Carroll

**Date:** 2026-10-21

**Version:** 0.56.0

**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)

</div>

## Abstract

We study finite-dimensional quantum models over specified rational and
algebraic scalar fields, distinguishing a finite presentation from a finite set
of states. The principal results are exact constructions and obstructions under
explicit assumptions on states, effects, composition, dynamics, and readout. A
normalized clock seed gives a constructive finite Weyl intertwiner. Equal
population reports can fail to preserve answers to a common future experiment.
An unconditional measure-and-prepare transfer of an unknown qubit has average
survival probability at most three quarters on four specified preparations,
with an attaining strategy. Finite Bell tables distinguish support compatibility
from the existence of a positive common joint distribution, while central-sector
weights constrain purification in a specified direct-sum tensor model.

Exact finite examples, written arguments, and selected formalizations accompany
one another with separate scopes. A positive global joint law implies the CHSH
bound $|S|\leq 2$; a supplied rational quantum model reaches $S=14/5$; and a
supplied tensor-state-observable model with entries in $\mathbb Q(\sqrt 2)$ (carried
in $\mathbb Q(\zeta_8)$ by the implementations) attains
$S=2\sqrt 2$ and has an exact sum-of-squares upper certificate. These results do
not derive the quantum state space, Born pairing, tensor composition, or
continuous dynamics from primitive difference. They identify which supplied
structures each conclusion uses and which reconstruction questions remain open.

## Guide to the paper

The main text is organized by mathematical questions. Source provenance and
reproduction details accompany the results without determining their truth.

| Question | Location | Evidential boundary |
| --- | --- | --- |
| Which finite and algebraic structures are being assumed? | §1 | Declared carrier and scalar data are not derived conclusions |
| What counts as a proof or finite certificate? | §§2–3 | Evidence is matched to the quantifiers of the statement |
| Which mathematical results are established? | §§4 and 11 | Each theorem keeps its scalar, dimension, positivity, and composition premises |
| Where does the proposed reconstruction remain open? | §§5, 7, and 9 | A missing selection argument is not an impossibility theorem |
| How can the computations be reproduced? | §§6, 10, and 12 | Validation and serialization checks do not establish physical predicates that fields only name |
| What do the carrier and measurement examples establish? | §13 | Conditional operational separations; no individual-outcome selection law |
| What does the derivation DAG record, and what did its reviews find? | §§13.8.8, 13.8.12 and 13.8.13 | Status labels are not mechanization claims; each reviewed node has a narrowest claim and a non-claim |

## 1. Finite presentations, supplied structure, and target examples

A finite-dimensional quantum model need not have finitely many states. This
paper distinguishes four notions:

1. a finite graph or cell complex;
2. a finite presentation by exact algebraic data;
3. a finite-dimensional vector space, which normally has infinitely many
   normalized states; and
4. a finite list of preparations, effects, or experiments.

On a declared directed graph the primitive coboundary is

$$
(d_0f)(u,v)=f(v)-f(u).
$$

For an edge cochain $x$, a weighted quotient such as

$$
\Phi_1([x])=\inf_{\alpha}\|x-d_0\alpha\|_{1,w}
$$

measures the residual after the admitted vertex repairs. This construction is
mathematically useful, but it does not by itself select complex scalars,
positivity, inner products, tensor composition, the Born pairing, or continuous
time. Those choices must be supplied or derived separately.

### 1.1 An eight-rung inventory

The eight rungs below are an assumption audit, not an eight-step derivation of
quantum mechanics.

| Rung | Established once the inputs are supplied | Additional supplied structure | Remaining boundary |
| --- | --- | --- | --- |
| 1. Difference | Finite differences, equality tests, and graph coboundaries | A carrier and equality relation | No preferred norm, topology, or physical geometry is selected |
| 2. Quotient repair | Exact finite quotient values and primal/dual certificates | Coefficient space, weights, and repair image | The quotient does not choose a quantum state space |
| 3. State--effect pairing | Positive normalized weights and conditional identities in stated models | Positive states, effects, and a pairing | The Born rule is not derived from difference |
| 4. Phase | Relative phases and phase-sensitive interference on a supplied complex or cyclotomic carrier | Complex conjugation and a phase group | Population data alone do not select the phase fiber |
| 5. Composition | Product states, entangled states, partial traces, and Bell tables in a supplied tensor model | Tensor composition and positivity | Tensor products are not forced by graph products |
| 6. Reversible dynamics | Exact finite unitaries and rational Cayley steps | An inner product, reversible maps, and a time step | Continuous time and a generator require topology and interpolation |
| 7. Measurement and channels | POVM probabilities, conditional updates, exact channels, and finite dilations | Effect algebra, instruments, and completely positive maps | Unitary dilation does not select one realized outcome |
| 8. Representation boundary | Finite frame constraints, contextuality witnesses, and finite-dimensional commutator obstructions | The hypotheses of Gleason/Busch-type representation theorems | Restricted algebraic ray sets do not automatically extend to complete projective geometry |

Two elementary cautions are important. First, the difference and equality
relation do not select the norm, topology, or physical geometry needed later;
they do not exclude every metric construction. Second, projective
state space is

$$
\mathbb P(\mathcal H)
=(\mathcal H\setminus\{0\})/\mathbb C^\times
\cong S(\mathcal H)/U(1),
$$

where $S(\mathcal H)$ is the unit sphere. The group quotient
$\mathbb C^\times/U(1)$ instead records positive scale and is not the
projectivization of the state space.

### 1.2 Twenty-two finite targets

The target list tests exact finite presentations against familiar structures.
Each row states the object actually considered; it is not a claim that the
corresponding general physical theory has been reconstructed.

| Target | Finite object and present scope |
| --- | --- |
| 1 | Primitive difference and zero self-difference on a declared carrier |
| 2 | A diamond-shaped 2-complex with exact cyclotomic holonomy data |
| 3 | A three-path amplitude fixture with vanishing Sorkin third-order term [7] under a supplied quadratic readout |
| 4 | Rational Cayley transforms in $\mathfrak{so}(8,\mathbb Q)$ and exact orthogonality checks |
| 5 | Rational $S_3$ braid relations and recoupling-shaped examples; no general pentagon theorem |
| 6 | Cabello's 18-ray parity system, its 146-vertex rational frame polytope, and exact positivity filtering |
| 7 | Signed permutation unitaries on a finite layered model |
| 8 | A rational CHSH model with $S=14/5$ and an exact positive-extension obstruction |
| 9 | The three-qubit bit-flip code, whose distance is one against unrestricted Pauli errors |
| 10 | Four-branch teleportation identities over exact Gaussian-rational data |
| 11 | Superdense-coding identities on a supplied Bell pair and gate set |
| 12 | A four-qubit $[[4,2,2]]$ stabilizer example with exact syndrome and distance checks |
| 13 | Prime-$5$ discrete Wigner phase-point operators and selected covariance/negativity witnesses (Python: floating-point diagnostic with absolute tolerance $10^{-10}$; exact arithmetic: Rust `wigner.rs`) |
| 14 | The Shor $[[9,1,3]]$ stabilizer construction and single-qubit error syndromes |
| 15 | Four-point phase-estimation identities over a specified cyclotomic carrier (exact replay: Rust `phase_estimation.rs`; the Python function returns the closed-form probabilities, not values computed from the transform) |
| 16 | A finite toric/surface-code incidence model and its declared anyon relations |
| 17 | Four-item Grover search as two exact Householder reflections |
| 18 | Finite Clifford conjugation identities and a scoped transversal-gate limitation [25] |
| 19 | The finite commutator trace obstruction and a constructive finite Weyl representation |
| 20 | Exact Richardson weights and the variance cost of finite zero-noise extrapolation |
| 21 | A finite quantum walk on a supplied Cayley graph with exact norm preservation |
| 22 | Exact mutually unbiased-basis tomography in dimensions three and four, with positivity checked separately from linear reconstruction |

The detailed target definitions, implementation addresses, and formalization
scope are in the source-notes supplement. Three results deserve emphasis here:
the Bell separation in §11.4, the Cabello census in §11.5, and the following
finite Weyl construction.

### 1.3 Constructive finite Weyl equivalence from an anchored seed

Let $N \ge 1$ and let $K \subseteq \mathbb C$ be a conjugation-stable subfield containing a primitive $N$th root of unity $\omega$. Equip $K^N$ with the standard Hermitian pairing. Supply unitary $N \times N$ matrices $X', Z'$ over $K$ satisfying the finite Weyl relations [4]

$$
Z'X'=\omega X'Z',\qquad (X')^N=I,
$$

and a normalized vector $v \in K^N$ satisfying

$$
Z'v=v,\qquad v^\dagger v=1.
$$

Define the canonical shift and clock by $X e_j = e_{j+1 \pmod N}$ and $Z e_j = \omega^j e_j$, for $0 \le j < N$. Then

$$
W = \begin{pmatrix} v & X'v & \cdots & (X')^{N-1}v \end{pmatrix}
$$

is unitary and satisfies $X'W=WX$ and $Z'W=WZ$. The joint commutant of $X'$ and $Z'$ consists of scalar matrices. Any two unitary intertwiners between the fixed pairs differ by multiplication by a unit-modulus scalar in $K$.

*Proof.* Induction in the Weyl relation gives $Z'(X')^j v = \omega^j (X')^j v$. These $N$ eigenvalues are distinct. Since $Z'$ is unitary, their eigenvectors are orthogonal, and unitarity of $X'$ makes all $N$ orbit vectors have norm one. The explicitly $N$-dimensional carrier makes them a basis. The period of $X'$ closes the shift relation, and the displayed eigenvalue equation gives the clock relation. A matrix commuting with the canonical clock is diagonal; commuting with the shift makes all its diagonal entries equal. Conjugating by $W$ establishes the commutant statement, and applying it to the ratio of two intertwiners establishes uniqueness up to scalar.

The normalized eigenvalue-one seed and scalar field are supplied inputs. This result does not find or normalize such a seed over every number field. If a supplied seed has eigenvalue $\omega^r$ instead, replace it by $(X')^{-r}v$ before using this construction. On a larger carrier the orbit spans a cyclic invariant subspace, not necessarily the whole carrier; no scalar-commutant conclusion for the larger carrier follows.

## 2. Standards of evidence

The mathematical statement, its premises, its implementation and its
reproduction record are separate. We use the following evidence classes
throughout the paper:

| Class | What it supports | What it does not support |
| --- | --- | --- |
| Written proof | The quantified statement under the assumptions used in its argument | A claim of Lean verification or physical realization |
| Scoped Lean proof | The actual elaborated declaration, including its input hypotheses and coefficient types | A broader theorem suggested by a filename, comment or surrounding prose |
| Exact finite computation | An identity, enumeration or certificate replay on its declared input domain | An unrestricted theorem from a sample of instances |
| Numerical demonstration | A reported approximation with its algorithm and tolerance | Exact zero, exact positivity or exact optimality without additional certificates |
| Imported theorem or conditional model | A standard theorem with its hypotheses, or a result conditional on supplied structures | Derivation of those hypotheses or structures from finite history data |
| Historical observation / unreproduced claim | What an identified earlier source or execution record reported | A fresh successful run or endorsement of every present source claim |

A finite computation can decide a finite theorem completely, and a checked
linear basis can establish an identity for its entire finite-dimensional
space. Conversely, a general written proof remains a proof even when no
Lean mechanization is supplied. Neither direction should be collapsed into
the ledger's software status labels.

The most important conclusions have these boundaries:

| Conclusion | Premises and supporting argument | Current scope |
| --- | --- | --- |
| Finite Weyl equivalence and scalar commutant | Primitive root, unitary $N \times N$ pair, period and normalized eigenvalue-one clock seed; explicit eigenvector-orbit proof in Target 19 | Written theorem; the exact verifier is Rust `intertwiner_from_clock_seed` (intertwiner and refusals, not the commutant or uniqueness conclusions); no Python verifier; Lean checks the stated commutant fragment |
| Born normalization | Supplied positive trace-one state, POVM summing to identity and trace pairing; linearity of trace | General algebraic identity; specialized two-level Lean models and exact channel checks |
| Gleason/Busch representation [1,3] | Full projective domain at dimension at least three, or an all-effects additive positive normalized domain | Imported theorems; rational-plane obstruction and finite tomography do not prove a general number-field representation theorem |
| Phase-blind reports can lose future answers | Two equal present reports separated by an admitted common future experiment | Explicit exact counterexample; no exclusion of every classical enlarged model |
| Bell joint-extension obstruction | Four supplied pair tables and one positive joint law on all sixteen local assignments | Finite convex separation and CHSH proof; a physical Bell reading also assumes setting independence and local response factorization |
| Classical-storage survival at most $3/4$ | Full qubit positive states/effects, affine unconditional encoding/retrieval, unknown input and no quantum side memory | General written proof with sharp control in §13.7; exact native instances |
| Central-sector purification obstruction and bounds | Full states of direct-sum complex matrix algebras and standard tensor composition | General written proof in §13.8; sharpness needs sufficient ancilla capacity; Lean assumes the pure-block representation |
| Native history quotient | A declared finite reachable history/action system and protected future questions, including availability | Minimal report relative to those questions; no quantum scalar, positivity or composition selection |

Repository-only checks validate status vocabulary, evidence paths and named
Rust test functions. They enforce bookkeeping; they do not decide whether a
file establishes a claim.
The source-by-source discussion in the source-notes supplement (its §4, subsections 11.1–11.60) supplies that interpretation and
retains counterexamples and open obligations. Its old execution counts are
historical unless an explicitly dated current replay is named.

## 3. Claims and supporting evidence

The evidence obligation is determined by the statement's quantifiers. A general
mathematical statement requires an adequate written proof or a formal proof of
the same statement. A claim over a finite domain may instead be settled by a
complete exact enumeration, provided the domain and enumeration are justified.
An example test establishes only the stated example.

Accordingly, each unresolved statement must receive one of the following
treatments:

1. an adequate written proof;
2. a matching formal proof;
3. a complete exact finite argument appropriate to its quantifiers;
4. a restriction to the domain actually established;
5. an explicit statement that it remains open; or
6. withdrawal after a counterexample.

File existence, compilation, schema validation, serialization, access control,
and a change of status label cannot decide whether this obligation has been
discharged. The repository maintains a historical evidence register for
reproduction, but its row counts and labels are not a measure of mathematical
progress and are not part of this monograph's scientific summary.

The sixty-seven source manuscripts are preserved in the paper archive. Six
are redirect, alias or annex stubs whose mathematical content is treated with
the destination result: the residual-density redirect (source-notes
supplement §11.4), the finite-realization redirect (§11.6), the earlier
phase-selector alias (§11.27), and the annex stubs for phase-gauge residuals
(§§11.28–11.29), the no-signaling model (§§11.33–11.34) and the completely
positive import boundary (§11.38).

## 4. Established results

The results below are stated by mathematical content rather than by repository
status. Their detailed hypotheses, arguments, and source addresses appear in
§§11–13.

1. **Finite Weyl equivalence from an anchored seed (§1.3, Target 19).** Given the
   stated conjugation-stable scalar field $K \subseteq \mathbb C$, primitive $N$th root $\omega$,
   unitary $N \times N$ pair $X', Z'$ with $(X')^N = I$, and normalized clock eigenvector
   $Z'v = v$ with $v^\dagger v = 1$, the orbit columns form an orthonormal eigenbasis and give
   an explicit unitary intertwiner $W$. The scalar-commutant conclusion on $K^N$ follows by the
   displayed basis argument. Finding or normalizing such a seed over an arbitrary number field
   is not included; on a larger carrier the orbit spans an invariant cyclic subspace.
2. **Finite cochain certificates (source-notes supplement §§11.3, 11.4 and 11.8).** An exact potential establishes
   membership in $\operatorname{im}d_0$; a separating functional vanishing on
   that image establishes non-exactness; and a nonzero $d_1x$ establishes
   failure of closure. Numerical linear programming is reported separately.
3. **Power-family context dependence (source-notes supplement §11.58, positive-power context independence).** Two rational contexts assign a
   shared ray the weights $1/2$ and
   $1/(1+(3/5)^p+(4/5)^p)$. For positive real $p$, equality holds exactly at
   $p=2$. This classifies the specified family, not all frame functions.
   The real-exponent equation $(3/5)^p+(4/5)^p=1 \iff p=2$ is kernel-checked,
   including the strict-monotonicity step (`power_real_unique` in
   `lean4/PromptStructure.lean`; DAG node `FQ-POWER-RULE-P2-SELECTION`, status
   `PROVED_LEAN` after its review narrowed the statement to this scope). Native exact
   replay reproduces the shared-ray context weights for integer $p=1,\dots,8$.
   Not mechanized: the transport from the concrete context normalization to the
   `Real.rpow` equation, the power-law family itself and the real orthonormal
   contexts, which are admitted. No readout-uniqueness or Gleason statement follows.
4. **Positive Bell extension (§13.8).** The full-support rational table has CHSH
   value $14/5$. Every deterministic assignment is support-compatible, yet no
   nonnegative common joint distribution reproduces the four marginals. The
   separating inequality is verified on all sixteen deterministic vertices.
5. **Classical-storage survival bound (§13.7).** Under the stated full qubit
   state/effect domain, affine unconditional measure-and-prepare transfer,
   unknown input, and absence of quantum side memory, the average survival on
   four preparations is at most $3/4$, and the bound is attained. Replayed exactly
   on declared instances in Rust; there is no Python or Lean replay.
6. **Central-sector bounds (§13.8).** In the specified direct-sum matrix-algebra
   state space with standard tensor composition, central weights bound extension
   purity and the trace distance from a pure-composite marginal. Attainability
   requires sufficient ancilla capacity.
7. **Primal and dual trace-norm certificates (source-notes supplement §11.35).** For
   $H=P-N$, positivity of $P,N$, the inequalities $-I\preceq W\preceq I$, and
   $\operatorname{tr}(WH)=\operatorname{tr}P+\operatorname{tr}N$ certify the
   claimed value independently of the implementation's label. Lean covers the
   two-coordinate integer inequality only.
8. **Phase-blind descent with a retained zero point (§11.1).** When the
   quotient keeps the zero vector as a distinct output, the population report
   of $Ac$ depends only on that of $c$ exactly when every row of $A$ has at
   most one nonzero entry. On projective space alone the rank-one all-ones
   matrix is a counterexample. Written proof and exact two-dimensional replay.
9. **Trace-zero repair duality (§11.2).** The dual norm of
   $\frac12\|\cdot\|_1$ on $\operatorname{Herm}_0(n)$ is the spectral diameter.
   On $K_{2,3}$ with the stated qutrit defects the trace-zero repair value is
   $6$ and the all-Hermitian value is $9/2$, each certified by an exact primal
   potential and a dual witness [13]. Lean covers the two-eigenvalue integer
   duality gap (`Eig2` in `lean4/TraceZeroDuality.lean`), scalar-shift invariance under a
   trace-zero hypothesis, and the integer-scaled diagonal $K_{2,3}$ primal minima
   (`k23_uncentered_zero_duality_gap`, `k23_centered_scaled2_zero_duality_gap` in
   `lean4/DerivationDagQMClosure.lean`). Lean does not state the matrix-norm duality or an LP
   strong-duality theorem for $K_{2,3}$; the values $6$ and $9/2$ rest on the explicit
   primal and dual arrays and their native replay. DAG node
   `FQ-TRACE-ZERO-DUALITY-K23` is `COMPUTATIONALLY_CHECKED` (lowered from `PROVED_LEAN`
   by its review).
10. **CPTP monotonicity selects the trace norm (§11.3).** A family of norms on
   trace-zero Hermitian matrices that no CPTP map increases is one positive
   multiple of the trace norm. Written proof by exact measure-and-prepare
   transport, with Rust transport replays. Lean (`TraceZeroDuality.lean`)
   records only that positive multiples of a contractive metric stay
   contractive.
11. **The Cabello frame polytope (§11.5).** The frame polytope of the eighteen
   Cabello rays has exactly 146 vertices, all half-integral, and none of their
   unique trace-one real-symmetric representatives is positive semidefinite.
   Exact enumeration with characteristic-polynomial certificates.

## 5. Open problems and limitations

The unresolved scientific questions are stated here directly rather than by
internal tracking codes. A question is closed only by a dated argument or
replayable result; renaming or reclassifying it does not resolve it.

The seven principal finite-to-continuum boundaries are:

1. **The continuum Hilbert lift: construction and selection are separate.**
   The *construction* is now kernel-checked once two inputs are supplied. With the scalar
   field ($\mathbb R$ or $\mathbb C$) and the $\ell^2$ uniformity taken as named
   hypotheses, the Hausdorff completion of the exact finite carriers is a complete inner
   product space into which they embed inner-product-preservingly, it is isometric to
   $\ell^2(\mathbb N,k)$, and a $\mathbb Q$-linear map with a rational quadratic bound lifts to
   a continuous operator (DAG node `FQ-CONTINUUM-HILBERT-LIFT-CONSTRUCTION`, `PROVED_LEAN`;
   §13.8.13). The *selection* is not done: no source derives the choice of scalar field or of
   the $\ell^2$ uniformity from finite-theory primitives, so `FQ-GAP-CONTINUUM-HILBERT-LIFT`
   stays `CONDITIONAL` and `GP-IMPORT-CONTINUUM-HILBERT` stays `IMPORTED_ASSUMPTION`.
   Dynamics and generators are not lifted. Source Notes §11.52 refuses the stronger
   conclusion that the finite data force a Hilbert space, and that refusal stands.
2. **Born uniqueness (Gleason [1]).** The Born rule is imported
   as a declared input throughout, never derived. The effect-additive route of §13.8.13
   proves a trace representation *given* effect additivity, positivity and normalization;
   it does not derive those hypotheses, and `FQ-GAP-BORN-UNIQUENESS-GLEASON` stays
   `CONDITIONAL`.
3. **Continuous time and Stone's theorem.** The finite examples distinguish
   finite-order integral evolutions from specified infinite-order rational
   rotations. Rational unitaries can also have finite order (the identity and
   rational quarter-turn suffice).
   A dense cyclic orbit has a closure only after choosing an ambient topology;
   that closure neither selects a time parameter nor a unique logarithm.
   Topology, continuous interpolation and its generator therefore remain
   additional inputs in both sectors. The carrier-level specification of §13.8.13
   (a $\mathbb Q$-parameter group needs roots of every order, which the rational
   $(3,4,5)$ rotation lacks at order two) sharpens this boundary; it does not cross it, and
   `FQ-GAP-STONE-CONTINUOUS-TIME` stays `CONDITIONAL`.
4. **The Gleason dimension condition at $n \ge 3$.**
   Gleason's theorem [1] uses every orthonormal basis of a space of dimension
   at least three, and Busch's version [3] uses every effect. A finite ray set
   gives only part of that conclusion. On the Cabello set in $\mathbb Q^4$, on
   its three- and six-basis prefixes, and on the 24-ray Peres set, every
   function that sums to one on each declared basis is the restriction of a
   real-symmetric trace-one form (exact rank computation). The form is unique
   once the ray projectors span the ten-dimensional space of real symmetric
   $4\times4$ matrices, which holds on every listed set except the
   three-basis prefix. Nonnegativity on the declared rays does not give
   positive semidefiniteness: the 146 vertex representatives of §11.5 are
   nonnegative on the eighteen Cabello rays, the research note
   `research/frame_function_finite_map.md` displays a rational
   trace-one form nonnegative on both the Cabello and the Peres rays, and none
   of these is positive semidefinite. The finite data fix the linear
   representative but not the positive cone, so the dimension condition
   remains an imported premise.
5. **The rational boundary of Everett-style branch counting.**
   Branch counting on fine-grained trees reproduces Born weights if and only if all weights lie
   in $\mathbb{Q}$. For weights in $\mathbb{Q}(\zeta_n)^+ \setminus \mathbb{Q}$, finite integer
   fine-graining encounters an exact arithmetic obstruction.
6. **Choice of real embedding.**
   The maximal totally real subfield $\mathbb{Q}(\zeta_n)^+$ has $\phi(n)/2$ real embeddings into $\mathbb{R}$ (16 at target conductor $n = 120$). Gram matrices of pure states stay positive semidefinite under every Galois conjugation, since each conjugate is again a Gram matrix, but mixed-state witnesses (starting at $n = 5$) exhibit embedding-relative positivity. The Galois group acts transitively on embeddings; selecting an ordered real embedding is an external declaration.
7. **The transcendental von Neumann entropy interface for mixed states.**
   For a non-pure density operator with algebraic spectrum, entropy in
   natural-log units, $S=-\sum_{\lambda_i>0}\lambda_i\ln\lambda_i$, is
   positive and is a nonzero algebraic linear combination of logarithms of
   algebraic numbers. Baker's theorem on linear forms in logarithms [24,27] makes
   this value transcendental.
   The claim is unit-sensitive: in bits, $S(I_2/2)=1$, so it does not assert
   that every base-two entropy is transcendental. The natural-log quantity
   lies outside $\mathbb Q(\zeta_n)$; the declared external interface uses a
   certified rational enclosure $[L_k,U_k]$ of width at most $2^{-k}$,
   with its midpoint error bounded by half that width.

If finite quantum mechanics fails as a reconstruction programme, the failure is
most likely to be exhibited at one of these seven boundaries. The useful outcome
would be a precise theorem locating that boundary, not a change in a project
status label. Historical packaging corrections and evidence-register statistics
are retained in the source notes and reproduction records. They are not measures of
the mathematical content established here.

### 5.1 Executable examples do not close the derivation gap

The repository contains executable interferometer, finite-cochain, Cayley-step,
and positive-semidefinite filtering examples. They consume a declared graph,
scalar field, state or amplitude data, readout rule, and experiment. Their
successful execution establishes facts about those inputs; it does not derive
the inputs or their quantum interpretation from primitive difference.

The exact examples retained in the main text use rational or specified
algebraic arithmetic. Older numerical linear-programming examples remain
numerical demonstrations. Historical execution counts and migration details
are recorded in the source-notes supplement, not used as theorem counts.

### 5.2 Three-layer finite-map decomposition of the quantum imports (QM-207 to QM-231)

Each of the five external imports (`QM-207` to `QM-211`), the perturbative loop-graph enclosure extension (`QM-212`), the hierarchical non-Abelian dressing control (`QM-213`), the second Symanzik 2-forest and BPHZ forest renormalization control (`QM-214`), the Dirac / Kulish–Faddeev dressed matter and Clifford Ward–Takahashi identity $Z_1 = Z_2$ control (`QM-215`), the 1-loop QED vacuum polarization $\Pi_R(q^2)$, running coupling $\alpha_{\mathrm{eff}}(q^2)$, and Uehling / Lamb shift control (`QM-216`), the exact $\mathfrak{su}(2)$ Kravchuk harmonic oscillator and $\mathfrak{so}(4)$ Pauli–Runge–Lenz Hydrogen bound-state spectrum control (`QM-217`), the relational Page–Wootters clock dressing, cyclotomic $\mathbb{Q}(\zeta_8)$ Tsirelson SOS certificate, and $(\mathbb{Z}_3)^2$ discrete Weyl–Wigner phase space control (`QM-218`), the foundational derivation closure for bipartite composition, $5 \times 5$ countermodel independence, and $\mathbb{Z}[\zeta_{12}]$ Sorkin readout classification (`QM-219`), the electroweak and strong gauge controls (`QM-220`, `QM-221`), the Gribov-copy-free tree dressing and Regge deficit controls (`QM-222`), the finite-graph spin-statistics and Pauli exclusion controls (`QM-223`), the relativistic Dirac–Coulomb, Lamb-shift, and Helium / Roothaan–Hartree–Fock controls (`QM-224`, `QM-225`), the tree-level QED Klein–Nishina / Bhabha / Møller, chiral $V-A$ muon decay / CKM, and ABJ / Gell-Mann–Okubo hadronic controls (`QM-226`–`QM-228`), and the post-Newtonian gravity, 3-qubit GHZ/Mermin + Page–Wootters + Kraus phase-damping, and QWZ/Haldane Chern parity controls (`QM-229`–`QM-231`) separates into three distinct layers: (i) an exact finite invariant computed over $\mathbb{Q}$ or a finite cyclotomic field $\mathbb{Q}(\zeta_N)$ on the declared carrier, (ii) the Cauchy-completion, direct-limit, or rational interval-enclosure step, and (iii) the residual external import that is not derived from transition weights.

| Import locus | Exact finite invariant (computed over $\mathbb{Q}$ or $\mathbb{Q}(\zeta_N)$) | Completion or enclosure step | Residual import |
| :--- | :--- | :--- | :--- |
| `QM-207` complex phase fiber and $\mathrm{U}(1)$ transport | $N$-torsion $\mu_N \subset \mathbb{Q}(\zeta_N)^\times$ edge 1-cochain $\tau$; gauge classes $\operatorname{Hom}(H_1(G,\mathbb{Z}), \mu_N)$ of size $N^{\beta_1(G)}$; relative report phase equals path holonomy $\tau(p_1)\tau(p_2)^{-1}$ | $\varinjlim_N \mu_N = \mathbb{Q}/\mathbb{Z}$ and metric completion to $\mathbb{R}/\mathbb{Z} \cong \mathrm{U}(1)$ | Non-triviality and order $N$ of the edge phase cochain $\tau$ |
| `QM-208` quadratic $L^2$ readout and Sorkin $I_3$ | Inside the phase-blind family $\alpha |c|^2 + \beta |c|^4$, third-order Sorkin interference satisfies $I_3 \equiv 0 \iff \beta = 0$; two-path cross term $2|a|^2 \operatorname{Re}\operatorname{Hol}(p_1 p_2^{-1})$ is gauge-invariant | None required for finite rational weights ($\sqrt{w}$ algebraic; $\sqrt{3} \in \mathbb{Q}(\zeta_{12})$) | Add-then-square amplitude composition rule and restriction to the polynomial readout family |
| `QM-209` noncommutative algebra and context parity | Weyl commutator $X^a Z^b X^{-a} Z^{-b} = \omega^{-ab} I$ over $\mathbb{Q}(\zeta_d)$ for a primitive $d$th root of unity $\omega = \zeta_d$, trivial ($\omega^{-ab} = 1$) iff the phase-exponent congruence $d \mid ab$ holds; Peres-Mermin $\mathbb{F}_2$ incidence matrix has rank $5$ with cokernel $H_0(K_{3,3};\mathbb{F}_2)$ and total-parity obstruction $1$ | Density of cyclotomic unitaries in $\mathrm{U}(d)$ and norm closure of $\mathcal{B}(\mathcal{H})$ | Admission of a second, non-diagonal measurement context |
| `QM-210` Born pairing and frame functions | Exact frame identity $\sum_i (v_i \otimes v_i)/\langle v_i, v_i\rangle = I_d$; zero linear Gleason residual on Cabello prefixes ($3$ tetrads inside the $8$-dim projector span; $6$ and $9$ tetrads and Peres $24$-ray set on the full $10$-dim $\operatorname{Sym}_4(\mathbb{Q})$, modulo the $6$-dim imaginary skew-Hermitian kernel in $\operatorname{Herm}_4(\mathbb{C})$); $\mathbb{F}_2$ Kochen-Specker parity inconsistency; explicit rational trace-one $\rho_2 \ge 0$ on all $24$ Peres rays (which contain the $18$ Cabello rays) with leading $2 \times 2$ minor $-1/16 < 0$ and quadratic value $-1/2 < 0$ on $(2,1,0,0)^{\mathsf{T}}$ | Gleason positivity closure requires the full continuum frame bundle $S^{d-1}$ for $d \ge 3$ | Positive-semidefinite cone requirement ($\rho \succeq 0$) and real-symmetric vs. complex-Hermitian quadratic carrier |
| `QM-211` cyclotomic clock tower and unitary steps | Finite spectral projection $U = \sum_k \lambda_k P_k$ over $\mathbb{Q}(\zeta_{24})$ ($F_4$ multiplicities $[2,1,1,0]$); $2^{|\{k : m_k > 0\}|}$ diagonal phase-choice unitary square roots within a fixed spectral decomposition (while sectors with $m_k \ge 2$ admit continuous unitary square-root families inside $\mathrm{U}(m_k)$); clock refinement iff $m \mid m'$; stochastic swap has $4$ unitary half-steps over $\mathbb{Q}(i)$ and $0$ real or stochastic half-steps | Direct limit $\varinjlim_m \frac{1}{m}\mathbb{Z}/\mathbb{Z} = \mathbb{Q}/\mathbb{Z}$, metric completion to $\mathbb{R}$, and Stone's theorem | Strong continuity, physical action scale $\hbar$, and coherent branch selection across refinements |
| `QM-212` dressed Symanzik graph polynomial and QED $g-2$ | Exact spanning-tree polynomial $\mathcal{U}_G(x) = \sum_{T} \prod_{e \notin T} x_e$ on $L = 1, 2, 3$ loop graphs with $\deg = L$; vertex dressing $C = d_0 \phi$ preserves cycle holonomy and $\mathcal{U}_G$; rational interval enclosure of $a_e^{(1,2,3)}$ to $12$ decimal places (width $\le 10^{-15}$, asserted in Python; the coefficients $c_2$, $c_3$ and $\alpha^{-1}$ are typed-in literature constants) | Period-integral brackets for $\pi, \zeta(2), \zeta(3), \zeta(4), \zeta(5), \ln 2, a_4$ and truncated loop order $L \le 3$ | Feynman parameter integration measure, UV renormalization subtraction, and external $\alpha^{-1}$ input |
| `QM-213` substantial vs. artificial and hierarchical non-Abelian DFM | Patch-cohomology separation of artificial (`LocalGreen` + `GlobalGreen`) vs. substantial (`LocalGreen` + `GlobalRed`) dressings; two-stage Borel factorization $N \triangleleft B_2(\mathbb{Q})$ with quotient $B_2/N \cong T_2$; exact $B_2/N$-covariance of dressed curvature $K^u = bA^u + A^u \smile A^u$ and discrete Bianchi identity $D_{A^u}K^u = 0$ on $P_5$ | None required for finite poset/cell-complex carriers over $\mathbb{Q}$ | Non-Abelian fiber dimension $d \ge 2$, normal subgroup filtration $N \triangleleft B$, and spanning-tree gauge choice $T \subset E(G)$ |
| `QM-214` second Symanzik 2-forest polynomial $\mathcal{F}_G$, DFM momentum routing, and BPHZ forest subtraction | Combinatorial 2-forest sum $\mathcal{F}_0(\alpha; q) = \sum_{(F, V_1, V_2)} (\prod_{e \notin F}\alpha_e)\|\sum_{v \in V_1} q_v\|^2$ equals Kirchhoff-Schur complement $\mathcal{U}_G \tilde{q}^{\mathsf{T}} (L_G^{(0)})^{-1}\tilde{q}$ and DFM tree-routing loop completion across all $8$ diamond spanning trees; Zimmermann BPHZ forest sum $\sum_{\mathfrak{F}} \prod_{\gamma \in \mathfrak{F}}(-T^{\omega(\gamma)})$ cancels $(\lambda_1, \lambda_2) \to (0, 0)$ UV boundary poles over $\mathbb{Q}$ | Schwinger-parameter period quadrature of the BPHZ-subtracted regular rational integrand | External renormalization point $\mu^2$, spacetime dimension $D = 4$ entering $\omega(\gamma)$, and physical mass parameters $m_e^2$ |
| `QM-215` Dirac / Kulish–Faddeev dressed matter and Clifford Ward–Takahashi $Z_1 = Z_2$ | $C\ell_{1,3}(\mathbb{Q}(i))$ anticommutation $\{\gamma^\mu, \gamma^\nu\} = 2\eta^{\mu\nu}I_4$; spanning-tree fermion dressing $\Psi_v = u_T[U](v)^{-1}\psi_v$ restores $\mathrm{U}(1)$ gauge invariance of $\langle\bar{\Psi}_y, \Psi_x\rangle$ across all $8$ diamond trees; 1-loop integrand Ward–Takahashi $q_\mu\mathcal{I}_\Lambda^\mu = \mathcal{I}_\Sigma(p,k) - \mathcal{I}_\Sigma(p+q,k)$ and $\mathcal{I}_\Lambda^\mu(p,p;k) = -\partial_{p_\mu}\mathcal{I}_\Sigma(p,k)$ in $M_4(\mathbb{Q}(i))$ give $Z_1 / Z_2 = 1$; exact IR cutoff $\lambda_{\mathrm{IR}}$ and pole $\varepsilon_{\mathrm{IR}}^{-1}$ cancellation | Certified `BigRational` / `RationalInterval` enclosure of the Kulish–Faddeev soft-photon attenuation factor $\mathcal{S}_{\mathrm{KF}} = 0.997892261461\ldots$ to $12$ decimal places (width $< 10^{-14}$) at $v = 3/5$, $2\Delta E / m = 1/2$ | External fine-structure constant $\alpha^{-1}$, fermion mass $m$, and soft-photon detector resolution $\Delta E / m$ |
| `QM-216` 1-loop QED vacuum polarization $\Pi_R(q^2)$, running $\alpha_{\mathrm{eff}}(q^2)$, and Uehling / Lamb shift | Transverse Ward projector $P_T^{\mu\nu}(q) = \eta^{\mu\nu} - q^\mu q^\nu / q^2 \in M_4(\mathbb{Q})$ ($q_\mu P_T^{\mu\nu} = 0$, $P_T^2 = P_T$, $\operatorname{tr}(P_T) = 3$); exact $4 \times 4$ Clifford Dirac trace on the 1-loop bubble numerator in $M_4(\mathbb{Q}(i))$; Symanzik bubble reduction $\mathcal{U}_{G_{\mathrm{bub}}}(x, 1-x) = 1$, $\mathcal{F}_{G_{\mathrm{bub}}} = m^2 - x(1-x)q^2$; BPHZ on-shell subtraction $\Pi_R(q^2) = \Pi(q^2) - \Pi(0)$ cancelling $\Lambda^2$; Feynman-parameter moments $M_n = ((n+1)!)^2 / (2n+3)!$ ($M_1 = 1/30 \implies$ Uehling slope $1/15$, $M_2 = 1/140$, $M_3 = 1/630 \implies 1/945$); Hydrogen $2S_{1/2}$–$2P_{1/2}$ rational contact sum $5/6 + 1/8 - 1/5 = 91/120$ (self-energy $5/6$, removal of the $2P_{1/2}$ anomalous-moment term $-1/8$, Uehling $-1/5$; equal to the QM-224 constant) | Certified `BigRational` / `RationalInterval` enclosures to $12$ decimal places (width $< 10^{-14}$) for $\Pi_R(-9m^2/4) = -0.000284802666\ldots$, $\alpha_{\mathrm{eff}}^{-1}(-9m^2/4) = 136.996970947974\ldots$, and Uehling $2S_{1/2}$–$2P_{1/2}$ shift $-27.128756729153\ldots\,\mathrm{MHz}$ | External fine-structure constant $\alpha^{-1}$, electron Compton frequency $m_e c^2 / h$, and relativistic Bethe logarithm $\ln k_0(n,l)$ |
| `QM-217` Exact $\mathfrak{su}(2)$ Kravchuk harmonic oscillator and $\mathfrak{so}(4)$ Pauli–Runge–Lenz Hydrogen spectrum | $\mathfrak{sl}(2, \mathbb{Q})$ Kravchuk oscillator ($N = 2j \in \{1,2,3,4\}$) with $G$-metric adjointness $J_+^{\mathsf{T}} G = G J_-$, Casimir $C_2 = j(j+1)I_{2j+1}$, equidistant spectrum $H_{\mathrm{osc}} = \operatorname{diag}(1/2, 3/2, \dots, 2j+1/2)$, ground-state Robertson–Schrödinger saturation $\langle Q^2\rangle_0\langle P^2\rangle_0 = 1/16 = \frac{1}{4}|\langle J_z/(2j)\rangle_0|^2$, and Kravchuk polynomial orthogonality $\sum_x \binom{N}{x}K_k K_{k'} = 2^N\binom{N}{k}\delta_{k,k'}$; $\mathfrak{so}(4) \cong \mathfrak{su}(2)_A \oplus \mathfrak{su}(2)_B$ Hydrogen shell $\mathcal{H}_n = V_j \otimes V_j$ ($n = 2j+1 \in \{1,2,3,4\}$, $\dim = n^2$) with Pauli constraint $\mathbf{L}\cdot\mathbf{K} = 0$, Casimir $C_2(\mathfrak{so}_4) = (n^2 - 1)I_{n^2}$, Balmer–Rydberg spectrum $E_n / E_{\mathrm{Ryd}} = -1/n^2 \in \{-1, -1/4, -1/9, -1/16\}$ (Lyman-$\alpha$ jump $3/4$, Balmer-$\alpha$ jump $5/36$), $\operatorname{tr}(\mathbf{L}^2) = n^2(n^2-1)/2 \in \{0, 6, 36, 120\}$, and $n=2$ projectors $\Pi_{2S} = I_4 - \frac{1}{2}\mathbf{L}^2$ ($\operatorname{tr}=1$), $\Pi_{2P} = \frac{1}{2}\mathbf{L}^2$ ($\operatorname{tr}=3$) with Dirac fine-structure degeneracy $C_{\mathrm{FS}}(2S_{1/2}) = C_{\mathrm{FS}}(2P_{1/2}) = -5/128$ lifted by radiative contact coefficient $91/120$ | Certified `BigRational` / `RationalInterval` enclosures to $12$ decimal places (width $< 10^{-14}$) for gross Lyman-$\alpha$ frequency $2467.381467264629\ldots\,\mathrm{THz}$ and $2S_{1/2}$–$2P_{1/2}$ radiative contact splitting $617.179215588248\ldots\,\mathrm{MHz}$ | External fine-structure constant $\alpha^{-1}$, electron Compton frequency $m_e c^2 / h$, and relativistic Bethe logarithm $\ln k_0(n,l)$ |
| `QM-218` Relational Page–Wootters clock dressing, $\mathbb{Q}(\zeta_8)$ Tsirelson SOS bound, and $(\mathbb{Z}_3)^2$ Weyl–Wigner phase space | Page–Wootters history shift $W = S_C \otimes U_S \in \mathrm{U}(8, \mathbb{Q}(i))$ ($W^4 = I_8$), static constraint projector $\Pi_{\mathrm{PW}} = \frac{1}{4}\sum_{k=0}^3 W^k$ ($C_{\mathrm{PW}}\Pi_{\mathrm{PW}} = 0$, $\operatorname{tr}(\Pi_{\mathrm{PW}}) = 2$), DFM clock dressing $D^\dagger W D = S_C \otimes I_2$, and relational observables $\mathcal{O}_{\mathrm{rel}}(\tau; O_S)$ reproducing $\langle\sigma_x\rangle_\tau = (1,0,-1,0)$ and $\langle\sigma_y\rangle_\tau = (0,1,0,-1)$ on static $|\Psi_{\mathrm{hist}}\rangle$; classical CHSH polytope bound $2$ ($16$ vertices) vs. $\mathbb{Q}(\zeta_8)$ ($s_2 = z - z^3$, $s_2^2 = 2$) Landau identity $\mathcal{B}_{\mathrm{CHSH}}^2 = 4I_4 - [A_0,A_1][B_0,B_1]$ and SOS decomposition $4I_4 - s_2\mathcal{B}_{\mathrm{CHSH}} = W_1^\dagger W_1 + W_2^\dagger W_2$ with $\mathcal{B}_{\mathrm{CHSH}}|\Phi^+\rangle = 2s_2|\Phi^+\rangle$; $(\mathbb{Z}_3)^2$ phase-point operators $A(q,p) \in M_3(\mathbb{Q}(\zeta_3))$ with exact line marginals and Wigner negativity $W_{|0\rangle - |1\rangle}(2,0) = -1/3 < 0$ ($\mathcal{N}_{\mathrm{Wigner}} = 2/3$) | Self-certified rational bracket $\mathrm{lo}^2 \le 2 \le \mathrm{hi}^2$ over $\mathbb{Q}$ enclosing $2\sqrt{2} = 2.828427124746\ldots$, Bell excess $2\sqrt{2} - 2 = 0.828427124746\ldots$, and $\sqrt{2}/2 = 0.707106781186\ldots$ to $12$ decimal places (width $< 10^{-14}$) | Zero external constant imports; only unbounded continuum time $t \in \mathbb{R}$ and $L^2(\mathbb{R})$ phase space lie outside the finite cyclic carrier $(\mathbb{Z}_d)^2$ |
| `QM-219` Foundational derivation closure: bipartite composition triad, $5 \times 5$ proxy-predicate separation, and $\mathbb{Z}[\zeta_{12}]$ Sorkin readout classification | Bipartite ($d_A = d_B = 2$) separation of direct sum ($3+3=6$ local parameters, $S_{\mathrm{CHSH}}^2 \le 4$), tensor product ($3+3+9=15$ local-tomography parameters, Tsirelson $S_{\mathrm{CHSH}}^2 = 8$), and PR box ($S_{\mathrm{PR}}^2 = 16 > 8$, violating Landau/SOS); $5 \times 5$ countermodel matrix $\mathcal{M}_{-207\dots-211}$ separating the five finite diagnostic proxy predicates (`AdmitsImport` in `FiniteQM.lean`), accompanied by the explicit Born-vs-quartic divergence on $\psi=(3/5,4/5,0,0)^{\mathsf{T}}$ ($\operatorname{tr}(\rho E_0)=9/25 \neq 81/625$, basis sum $337/625 \neq 1$, renormalized $81/337 \neq 9/25$) and the $3$-ray positivity vs. full-PSD witness $\rho_{\mathrm{alt}} = \begin{pmatrix}1/2 & -3/4 \\ -3/4 & 1/2\end{pmatrix}$ ($\det = -5/16 < 0$); $\mathbb{Z}[\zeta_{12}]$ unit identity $(\zeta - 1)(-\zeta^2 - \zeta^3) = 1$ forcing $L \equiv 0$, rank-$8$ / nullity-$2$ $\mu_{12}$-action on $\operatorname{Sym}^2(\mathbb{Q}^4)$ spanned by $(N_0, N_1)$ where $R_{A,B}(x) = A N_0(x) + B N_1(x)$ ($A=\alpha+\beta$, $B=\sqrt{3}(\alpha-\beta)$) is $\mathbb{Q}$-valued for all $(A,B)\in\mathbb{Q}^2$ and positive definite iff $A > 0$ and $B^2 < 3A^2$ (leading Gram minors on $1,\zeta,\zeta^2,\zeta^3$ are $A$, $(4A^2-B^2)/4$, $A(3A^2-B^2)/4$, $(3A^2-B^2)^2/16$; $(A,B)=(1,1)$ gives an integer-valued positive-definite counterexample with minors $(1,3/4,1/2,1/4)>0$ and unequal unit weights $R_{1,1}(v_+)=11 \neq 3=R_{1,1}(v_-)$), while Galois invariance under $\sigma(\zeta_{12})=\zeta_{12}^5$ ($\sigma(\sqrt{3})=-\sqrt{3}$) selects $B = 0 \iff \alpha = \beta$ | Self-certified rational bracket $\mathrm{lo}^2 \le 3 \le \mathrm{hi}^2$ over $\mathbb{Q}$ enclosing $\sqrt{3} = 1.732050807568\ldots$, $2 + \sqrt{3} = 3.732050807568\ldots$, and $2 - \sqrt{3} = 0.267949192431\ldots$ to $12$ decimal places (width $< 10^{-14}$) | Bipartite local tomography + joint PSD cone (`FQM-COMPOSITION-IMPORT`), full semantic import independence beyond proxy predicates, and Galois/automorphism invariance selecting $\alpha = \beta$ |
| `QM-220` Finite electroweak $\mathrm{SU}(2)_L \times \mathrm{U}(1)_Y \to \mathrm{U}(1)_{\mathrm{EM}}$ DFM dressing, Weinberg projectors, custodial $\rho_{\mathrm{EW}} = 1$, and $\mathrm{U}(1)_Y^3$ anomaly cancellation | Doublet dressing $U(\alpha, \beta) \in M_2(\mathbb{Q}(i))$ eliminates all $3$ real Goldstone modes via $\Phi^u = U(\alpha,\beta)^\dagger(\alpha,\beta)^{\mathsf{T}} = (0,1)^{\mathsf{T}}$ when $|\alpha|^2 + |\beta|^2 = 1$ and leaves the dressed vacuum $\Phi^u$ invariant under the unbroken electric charge generator $Q_{\mathrm{EM}} = T_3 + Y = \operatorname{diag}(1,0)$ ($Q_{\mathrm{EM}}\Phi^u = 0$, while $[U(\alpha,\beta), Q_{\mathrm{EM}}] \neq 0$ for $\alpha \neq 0$); neutral mass matrix $M_0^2 = \frac{v^2}{4}\begin{pmatrix}g^2 & -gg' \\ -gg' & g'^2\end{pmatrix}$ has $\det(M_0^2) = 0$, $\operatorname{tr}(M_0^2) = M_Z^2$, orthogonal Weinberg projectors $P_\gamma, P_Z \in M_2(\mathbb{Q}(g,g'))$, and custodial $\rho_{\mathrm{EW}} = M_W^2 / (M_Z^2 \cos^2\theta_W) = 1$ vs. a pure $Y=1$ triplet vacuum value, for which $\rho_{\mathrm{EW}} = 1/2 \neq 1$ (no mixed doublet-triplet formula is implemented); one-generation Standard Model chiral hypercharges cancel $[\mathrm{SU}(3)_c]^2\mathrm{U}(1)_Y$, $[\mathrm{SU}(2)_L]^2\mathrm{U}(1)_Y$, $[\mathrm{grav}]^2\mathrm{U}(1)_Y$, and $\mathrm{U}(1)_Y^3$ at $N_c = 3$, while $[\mathrm{SU}(2)_L]^2\mathrm{U}(1)_Y$ ($-1/3$) and $\mathrm{U}(1)_Y^3$ ($+1/2$) fail at $N_c = 1$ | Certified `BigRational` / `RationalInterval` enclosures to $12$ decimal places (width $< 10^{-14}$) at the exact rational samples $\sin^2\theta_W \in \{9/25, 3/8\}$ used in the controls; no enclosure at $\sin^2\theta_W = 23122/100000$ is implemented | External vacuum expectation value $v$, weak mixing parameter $\sin^2\theta_W$, and empirical Yukawa couplings |
| `QM-221` 1-loop $\mathfrak{su}(3)_c$ QCD Gross–Wilczek–Politzer $\beta_0 = 11 - \frac{2}{3}n_f$, 2-loop Banks–Zaks ratio $1/302$, and Wilson-loop Creutz confinement witness | Rational-weighted Gell-Mann generators $\tilde{T}_a \in M_3(\mathbb{Q}(i))$ with weights $w = (1,1,1,1,1,1,1,1/3)$ satisfy $9 \times 9$ Fierz completeness $\sum_a w_a (\tilde{T}_a)_{ij}(\tilde{T}_a)_{kl} = \frac{1}{2}\delta_{il}\delta_{kj} - \frac{1}{6}\delta_{ij}\delta_{kl}$, $C_F = \frac{4}{3}I_3$, $C_A = 3$, singlet attraction $-4/3 < 0$ vs. octet repulsion $+1/6 > 0$ ($\operatorname{tr} = 8(1/6) - 4/3 = 0$), and $512$ Jacobi triples; $\beta_0(n_f) = 11 - \frac{2}{3}n_f > 0$ for $0 \le n_f \le 16$ ($\beta_0(16) = 1/3$, $\beta_0(17) = -1/3$) and $\beta_1(n_f) = 102 - \frac{38}{3}n_f$ give Banks–Zaks ratio $-\beta_0(16)/\beta_1(16) = 1/302 > 0$; on the $3 \times 3$ planar grid ($V=9, E=12, T=8, b_1=4$), Creutz ratio $\chi(R,T)$ isolates $u_\sigma$ under area-law $W_{\mathrm{area}}(R,T) = C u_p^{2(R+T)}u_\sigma^{RT}$ and gives $1$ under perimeter-law $W_{\mathrm{perim}}(R,T) = C u_p^{2(R+T)}$ | Certified `BigRational` / `RationalInterval` enclosures to $12$ decimal places (width $< 10^{-14}$) for strong-coupling string tension $\sigma a^2 = 2\ln 3 = 2.197224577336\ldots$ and 1-loop running $\alpha_s$ ($0.103072040480\ldots$ and $0.091557149048\ldots$) at $n_f = 5$, $\alpha_s(M_Z^2) = 1179/10000$ | Non-perturbative continuum Yang–Mills mass gap in $D = 4$, physical reference coupling $\alpha_s(M_Z^2)$, and the lattice coupling $\beta = 2$ ($u = 1/9$) with the area law behind the Creutz witness |
| `QM-222` Spanning-tree Gribov-copy-free non-Abelian dressing and discrete Regge hinge curvature | Unique spanning-tree trivialization of non-Abelian graph connections vs. lattice Landau-gauge Gribov copies on the 4-vertex diamond graph ($64 = 4^3$ anchored copies); rational boost-composition hinge holonomies (trace $16/3$ in 4D, $10/3$ in the boost plane) and a telescoping Bianchi product over $\mathbb{Q}$ | None required for finite simplicial / graph carriers over $\mathbb{Q}$ | Choice of spanning tree $T \subset E(G)$ and continuum metric identification |
| `QM-223` Finite-graph $\operatorname{Conf}_2^{(2)}(G)$ square 2-complex spin-statistics, Pauli exclusion, and shell closures | Square 2-complex $\operatorname{Conf}_2^{(2)}(G)$ homology over $\mathbb{Q}$ and $\mathbb{F}_2$: $P_3$ has $(V,E,F_\square)=(3,2,0)$, $b_1^{(2)}=0$; star $Y=K_{1,3}$ has $(6,6,0)$, $b_1^{(2)}(\mathbb{Q})=b_1^{(2)}(\mathbb{F}_2)=1$, $\operatorname{tors}_{\mathbb{Z}_2}=0$; $C_4$ has $(6,8,2)$, $b_1^{(1)}=3$, $\operatorname{rank}(\partial_2)=2$, $b_1^{(2)}(\mathbb{Q})=b_1^{(2)}(\mathbb{F}_2)=1$, $\operatorname{tors}_{\mathbb{Z}_2}=0$; planar 3-connected $K_4$ has $(6,12,3)$, $b_1^{(1)}=7$, $\operatorname{rank}(\partial_2)=3$, $b_1^{(2)}(\mathbb{Q})=b_1^{(2)}(\mathbb{F}_2)=4$, $\operatorname{tors}_{\mathbb{Z}_2}=0$ ($H_1 \cong \mathbb{Z}^4$); nonplanar 3-connected $K_5$ has $(10,30,15)$, $b_1^{(1)}=21$, $\operatorname{rank}_{\mathbb{Q}}(\partial_2)=15$, $\operatorname{rank}_{\mathbb{F}_2}(\partial_2)=14$, $b_1^{(2)}(\mathbb{Q})=6$, $b_1^{(2)}(\mathbb{F}_2)=7$, $\operatorname{tors}_{\mathbb{Z}_2}=1$ ($H_1 \cong \mathbb{Z}^6 \oplus \mathbb{Z}_2$; whether the exchange loop represents the $\mathbb{Z}_2$ class is not established here, and Lean shows only $\chi^2 = 1 \iff \chi \in \{+1,-1\}$ over $\mathbb{Q}$ from supplied $(V,E,F)$ counts); Slater determinant vanishing on equal orbitals, Jordan–Wigner CAR $c_i^2 = 0$, HBT factor $2$, and shell capacities $2n^2 = (2,8,18,32)$ with noble-gas closures $Z \in \{2,10,18,36,54,86,118\}$ (Lean checks the closures through $Z = 86$) | None required (exact combinatorial and integer/rational homology identities) | 3D orbital energy ordering $(n+l, n)$ beyond hydrogenic degeneracy |
| `QM-224` & `QM-225` Relativistic Dirac–Coulomb fine structure, Lamb shift, and Helium / RHF screening | $n=2$ Dirac–Coulomb coefficients $c_{2,1/2}^{(4)} = 5/128$ ($2S_{1/2}$ kinetic $13/128$ + Darwin $-8/128$ = $2P_{1/2}$ kinetic $7/384$ + spin–orbit $8/384$) and $c_{2,3/2}^{(4)} = 1/128$, splitting $\Delta c_{\mathrm{FS}}^{(4)} = 1/32$; Lamb contact sum $5/6 - 1/5 + 1/8 = 91/120$; Helium Kellner optimum $E_{\mathrm{He}}(27/16) = -729/256\,E_h$ with $2T+V=0$, $1s2s$ exchange $K_{1s2s} = 32/729\,E_h > 0$, and $\ell_1$-contractive affine Clementi–Slater screening relaxation ($\lambda = 1/4$) | Certified rational brackets for $2P_{3/2}$–$2P_{1/2}$ splitting ($[10949.28, 10949.29]\,\mathrm{MHz}$), $2S$–$2P$ Bethe logarithm $\ln k_0(2S) - \ln k_0(2P) \in [2.841786, 2.841787]$ yielding pure 1-loop non-recoil shift $[1052.19, 1052.20]\,\mathrm{MHz}$ + higher-order $[5.645, 5.655]\,\mathrm{MHz} \subset [1057.70, 1057.95]\,\mathrm{MHz}$, and 4-term Hylleraas Helium ground state ($[-2.9038, -2.9024]\,E_h$) | External $\alpha^{-1}$, Rydberg energy, Bethe logarithm $\ln k_0(n,l)$, higher-order $\mathcal{O}(\alpha(Z\alpha)^5)$ / 2-loop / recoil / proton-radius remainder, and empirical Clementi–Slater screening constants $\sigma$ |
| `QM-226`–`QM-228` Tree-level QED Klein–Nishina / Bhabha / Møller, chiral $V-A$ muon decay / CKM, and ABJ / Gell-Mann–Okubo | Klein–Nishina ratio $R(x,u) = \frac{1}{2}\eta^2(\eta + \eta^{-1} - (1-u^2))$ ($R(x,1)=1$, Thomson $\frac{3}{8}(1+u^2)$ normalized to $1$); $s \leftrightarrow u$ crossing $M_{\mathrm{M\o ller}}(s,t,u) = M_{\mathrm{Bhabha}}(u,t,s)$ vs. $s \leftrightarrow t$ counterexample at $(5,-2,-3)$; Weyl-basis $P_L + P_R = I_4$, $P_L P_R = 0$; muon phase polynomial $f_0(x) = (1-x)(1-7x-7x^2+x^3)$; Cayley CKM $V = (I-A)(I+A)^{-1} \in \mathrm{U}(3,\mathbb{Q}(i))$ with $z_1+z_2+z_3=0$ and $J \neq 0$; ABJ factor $S(3)/S(1) = 3 \implies \Gamma(3)/\Gamma(1) = 9$; polynomial Gell-Mann–Okubo octet ($2(M_N+M_\Xi) = 3M_\Lambda + M_\Sigma$) and decuplet equal-spacing identities | Machin $\pi$, atanh $\ln x$, and integer-sqrt rational enclosures for $G_F/(\hbar c)^3 \in [1.16638176, 1.16638177]\times 10^{-5}\,\mathrm{GeV}^{-2}$ and $\Gamma(\pi^0\to\gamma\gamma)_{N_c=3} \in [7.690, 7.882]\,\mathrm{eV}$ vs. $N_c=1 \in [0.854, 0.876]\,\mathrm{eV}$ | PDG-style rational mass/lifetime inputs, the Wolfenstein parameters $\lambda = 9/40$, $A = 4/5$ that tune the CKM generator, and higher-loop electroweak/QCD corrections |
| `QM-229`–`QM-231` PPN light deflection / perihelion, 3-qubit GHZ/Mermin + Page–Wootters + Kraus phase damping, and QWZ/Haldane Chern parity | Null-probe tracelessness $e\,\eta(k,k) = 0$ vs. dust trace $\rho$; PPN factors $(1+\gamma)/2 = 1$ ($\delta\varphi_{\mathrm{GR}} = 2\delta\varphi_{\mathrm{Newton}}$) and $(2+2\gamma-\beta)/3 = 1$, $\pi$-free Mercury advance $3888000\,GM/(a(1-e^2)c^2)$ arcsec/orbit; 3-qubit GHZ $A_1 A_2 A_3 = -B$ over $\mathbb{Q}(i)$ giving Mermin eigenvalue $4$ vs. exhaustive 64-vertex classical bound $\le 2$; 4-tick Page–Wootters lowering constraint $(I_C\otimes U - S\otimes I_S)|\Psi\rangle = 0$; Pythagorean $(p,r,q)$ Kraus completeness $K_0^\dagger K_0 + K_1^\dagger K_1 = I_2$ with 3-step $(3,4,5)$ coherence $(3/5)^3 = 27/125$; QWZ Dirac-point parity $2C_1(m) \in \{2,-2,0,0\}$ at $m \in \{-1,1,3,-3\}$ and Haldane sign table | Machin $\pi$ rational enclosure for solar-limb deflection $[1.751190, 1.751191]''$ (GR) vs. $[0.875595, 0.875596]''$ (Newtonian) and Mercury centennial advance $42.980654'' \in [42.97, 42.99]''$ | Solar/planetary orbital parameters ($GM_\odot/(c^2 R_\odot)$, $a, e$) and continuum torus integration beyond Dirac-point parity |

Mechanization scope of `QM-213` to `QM-231`. Rows `QM-213`, `QM-214`, `QM-215` and `QM-218` are Rust and Python only; no Lean theorem states them. For `QM-220` Lean covers a real $\mathrm{SO}(2)$ slice of the doublet dressing and one witness; the three-mode Goldstone statement over $M_2(\mathbb{Q}(i))$ is in Python and Rust. For `QM-221` Lean checks six Cartan entries, not the 81-entry Fierz identity. For `QM-222` the Lean statement is a scalar abelian triangle fixture and $2\times2$ boosts. For `QM-229`–`QM-231` Lean states the single-site Pauli products, the Mermin bound over 64 assignments and the Pythagorean Kraus steps; the $8\times8$ GHZ eigenvalue $4$, the Page–Wootters constraint, the CKM Cayley step, $G_F$, the $\pi^0$ widths, the solar enclosures and the Haldane table are Python and Rust only.

This decomposition isolates the exact finite algebraic content from the completion steps and external postulates, and establishes via `QM-219` the pairwise separation of the five finite diagnostic proxy predicates (`FQM-IMPORT-INDEPENDENCE`) alongside the explicit Born-vs-quartic and 3-ray-vs-PSD gap witnesses, the separation of tensor-product composition from direct-sum and PR-box alternatives (`FQM-COMPOSITION-IMPORT`), and the two-parameter $\mathbb{Z}[\zeta_{12}]$ Sorkin $I_3 = 0$ rational readout cone $R_{A,B}$ together with its Galois-invariance selection of equal embedding weights $\alpha = \beta$ (`FQM-QM208-READOUT-CLASS`), while `QM-220` through `QM-231` extend the same finite-algebraic and rational-enclosure discipline to electroweak and strong gauge sectors, square 2-complex configuration-space homology, atomic structure, tree-level QED/weak/hadronic observables, post-Newtonian gravity, 3-qubit GHZ contextuality, and topological Chern parity. It does not derive Gleason's positive half from finite ray sets, Stone's theorem from finite roots of unity, or continuum spacetime from graph combinatorics.

## 6. How to read the publication package

The main paper states current mathematical results and limitations. The
source-notes supplement preserves the paper-by-paper corrections, original
source addresses, and detailed implementation scope. All retained source
manuscripts cited there are included under `sources/original_papers/` in the
paper ZIP. Companion papers used in the current exposition are included under
`companion_papers/`.

The separate code-companion ZIP contains the shared Rust and Lean source trees
in the same relative layout used by their manifests. This split keeps the
scientific paper readable while allowing a reader to inspect and run the
actual code instead of relying on absent repository paths. Section 12 gives
the focused commands and distinguishes mathematical proof, finite replay,
formal checking, and archive custody.

For an unresolved statement, the obligation is unchanged: provide an adequate
written proof, a formal proof of the same statement, or a complete exact finite
argument appropriate to its quantifiers; otherwise restrict it, identify it as
open, or withdraw it. An example test remains evidence only for its stated
inputs.

## 7. Scope limits

- Nothing here derives the Born rule, complex structure, unitarity, tensor
  factorization, or continuous time. Every one of those enters the source papers
  as a **declared import**, and importing a thing is not deriving it.
- A green test suite in this application certifies that its mechanical constraints
  hold — that files exist, commands exit 0, syntax parses, and unit tests execute.
  It does not by itself certify semantic mathematical validity or that prose claims
  are fully entailed by code/proof terms; those boundaries require substantive review.

## 8. Sources, code, and public-record corrections

The companion publication ZIP contains the retained source manuscripts under
`sources/original_papers/`, the source-notes supplement, and the code used by
the package-local reproductions. A separate code-companion ZIP preserves the
shared Rust workspace and the Lean workspace in their repository-relative
locations so the named commands do not depend on files absent from the
download. Section 12 states the exact commands and the limits of the latest
replay.

Two earlier Zenodo records require author-controlled correction before this
edition is promoted. Prepared errata are included locally:

- `docs/zenodo_errata/20683775_erratum.md` narrows the claimed relationship
  between phase averaging, the Born rule, and Hilbert-space emergence;
- `docs/zenodo_errata/20550459_erratum.md` replaces the incorrect centered
  trace-zero dual and records the exact $K_{2,3}$ counterexample.

These files are proposed public-record corrections, not evidence that Zenodo
has already been updated. The source-notes supplement contains the full
version and custody discussion.

## 9. Limits of the proposed finite derivation

An earlier version of this section claimed a complete 50-step derivation, a
minimal ambient carrier, and resolution of every proposed test. The proofs and
computations do not establish those claims, so they are withdrawn. The
historical wording remains available in version control.

| Topic | What the Lean statements cover | What they do not cover |
| --- | --- | --- |
| Carrier labels | Natural-number divisibility, a directed label system, and Gaussian record identities | An actual field colimit, all-target embedding, or minimal carrier |
| Probability and contextuality | Declared squared-norm weights, two Sorkin fixtures, and finite CHSH/parity arithmetic | Quotient-fiber transport, marginal no-signaling, or a derivation of Born weights |
| Cabello witness | Cabello matrix checks and a norm-25 integer partition | Topology or non-Bornian functions on the dense cyclotomic sphere |
| Discrete dynamics | Boolean endomaps, a scaled $2\times2$ Gaussian square root, integer Cayley identities, and integer-labelled records | Continuous Hamiltonians, logarithms, Stone's theorem, or a necessity proof |
| Commutator obstruction | A $2\times2$ integer commutator trace obstruction and one Weyl example | All dimensions and rings, a completion functor, or an exclusive continuum classification |
| Conductor bounds | Divisibility and least common multiples of declared labels | State embeddings, field minimality, or a general stabilizer or unextendible-product-basis theorem |

The Python Cabello witness satisfies the 18-ray/9-context constraints and has
a checked negative eigenvector. The Peres computation checks 33 rays, 72 pairs
and 16 triads; its binary valuation count is zero. Its finite linear system
has rank 16 (`gleason_cyclotomic.py`, exact row reduction). For the constructed function `f=1/3+z`, the residual
`z`, not `f`, is orthogonal to the declared trace-free quadratic rows.
Neither construction is a frame function on a dense sphere.

Python constructs ten bounded triads. Rust's legacy higher-conductor report
checks four rational triads only; its former six additional offers were not
computed and are withdrawn. No cross-language higher-triad parity is claimed.
The topology, rational-sphere colorability, p-adic and nonstandard-model flags
that lacked implementations are now explicitly unknown. Modular witnesses and
four-conductor discriminant checks retain their finite scope.

Preserving an earlier prediction text does not validate its conclusion. The
proposed refusals are not established, and both Gleason-related questions
remain open under explicit conditions. No “probability wall is absolute” or
“completion is necessary” conclusion survives this review.

The strongest result here is a collection of exact finite computations and
scoped Lean theorems under declared carriers and measures. Finite-dimensional
does not mean finite carrier; countable does not mean discrete topology.

## 10. Higher-dimensional bounds and the Tiles construction

Conductor labels here are sufficient declarations for the named objects, not a
search proving minimality. In particular, a generator or parity-check matrix is
not the same object as a normalized state.

- The five-qubit stabilizer generator/projector declaration uses $\mathbb Q(i)$, label 4;
  the Steane parity-check declaration uses $\mathbb Q$, label 1. No normalized-codeword
  carrier or all-stabilizer classification follows.
- The named GHZ and W normalization declarations use labels 8 and 12.
  A seven-qubit W normalization uses the positive root $\sqrt7$, discriminant 28.
- Prime-qudit normalized setting declarations combine roots of unity and
  the positive root $\sqrt p$. At $p=7$ the bound uses 28 and
  $\operatorname{lcm}(120,28)=840$. (The field $\mathbb Q(\sqrt{-7})$ has
  discriminant $-7$, not 28.)
- Collins–Gisin–Linden–Massar–Popescu (CGLMP) setting bounds use
  $\operatorname{lcm}(4d,\operatorname{disc}\mathbb Q(\sqrt d))$; they exclude an
  optimal entangled state's amplitudes. For $d=3,4,5,6,7,8$ the labels are
  respectively 12, 16, 20, 24, 28, 32, giving joint least common multiples
  with 120 of 120, 240, 120, 120, 840, 480.

The Tiles $3\times3$ example is actual matrix data, not a trace-only
assertion. With five unnormalized product vectors $v_i$, it constructs the
rational matrix

$$
\rho=\frac14\left(I_9-\sum_i\frac{v_iv_i^{\mathsf T}}{v_i^{\mathsf T}v_i}\right).
$$

Python and Rust verify mutual orthogonality, trace one, symmetry, the projector
identity `4 rho^2 = rho`, and equality with its partial transpose.
All 32 assignments of local orthogonality conditions are checked by exact
rank-three minors, excluding a nonzero product vector in the complement.
The entanglement reading uses the declared UPB-complement criterion; this is a
deterministic finite certificate, not a Lean UPB theorem or general classifier.
Duplicate and zero product-vector inputs are rejected.

From `python/`, `python -m finite_qm.entrypoints.replay_review_receipts --check`
regenerates both repaired computation receipts byte-for-byte. Receipt identity does not promote the declarations above.

## 11. Principal exact results

This section collects the strongest results that emerged from the exact
finite analysis. The long source-by-source record is in
[`finite_quantum_mechanics_source_notes.md`](finite_quantum_mechanics_source_notes.md).
Each result below is stated by its mathematical content. Implementation names
are supplied only as reproduction pointers. The exact certificates for §11.1,
§11.2, §11.3 and §11.5 are Rust and Python tests; the Lean declarations that touch
§11.2 and §11.3 cover only the scopes stated in §4, items 9 and 10. In §11.6 the
real-exponent equation $(3/5)^p+(4/5)^p=1\iff p=2$ is a kernel-checked Lean theorem
(`power_real_unique`, `lean4/PromptStructure.lean`); the rest of that section is
replayed natively.

### 11.1 Phase-blind descent requires a retained zero point

Let $A$ be a matrix acting on nonzero vectors and let

$$
\pi(c)_g=\frac{|c_g|^2}{\sum_h|c_h|^2}
$$

be the phase-blind population report. A tempting claim says that
$\pi(Ac)$ depends only on $\pi(c)$ exactly when every row of $A$ has at most
one nonzero entry. That claim is false on projective space. A rank-one matrix
such as

$$
A=\begin{pmatrix}1&1\\1&1\end{pmatrix}
$$

sends every non-annihilated input to the same ray even though each row has two
nonzero entries.

The row-sparsity characterization becomes correct when the quotient retains
the zero vector as a distinct output. If two nonzero entries occur in one row,
relative phase can be chosen so that this row cancels for one representative
but not for another representative with the same population report. The
retained zero point detects that annihilation. Conversely, a row-sparse matrix
cannot create such phase-sensitive cross terms. The exact two-dimensional
counterexamples and the zero-retaining proof are replayed in
`phase_blind_quotient` and described in source-notes supplement §11.25.

### 11.2 Trace-zero repair quotients have a scalar-divergence dual

For Hermitian trace-zero edge defects, compare

$$
\Phi_0(\delta)=\inf_{\alpha_v\in\operatorname{Herm}_0(n)}
\sum_e\frac12\|\delta_e-(d_0\alpha)_e\|_1
$$

with the same infimum over all Hermitian vertex potentials. The polar of
$\frac12\|\cdot\|_1$ on $\operatorname{Herm}_0(n)$ is an observable class
modulo scalar identity, with norm

$$
\|[M]\|^*=\lambda_{\max}(M)-\lambda_{\min}(M).
$$

Accordingly, the trace-zero dual requires spectral diameter at most one and
$(d_0^*M)_v\in\mathbb RI$. The all-Hermitian dual instead requires
$\|M_e\|_{\mathrm{op}}\leq1/2$ and $d_0^*M=0$.

On $K_{2,3}$, orient the legs $u\to w_k\to v$ and put
$D_k=3E_{kk}-I$ on $u\to w_k$. Zero repair and the witnesses $D_k/3$ on both
edges of each leg certify

$$
\Phi_0=6.
$$

The all-Hermitian potential
$\alpha_u=0$, $\alpha_v=-I$, $\alpha_{w_k}=D_k$, together with the witnesses
$D_k/4$, certifies

$$
\Phi_{\mathrm{all}}=\frac92.
$$

The complete theorem and dependency-free exact replay are in the companion
paper *Trace-Zero Repair Quotients on a Finite Graph* [13].

### 11.3 CPTP monotonicity selects the trace norm on state differences

For each finite dimension $n$, let $N_n$ be a norm on the real vector space $\operatorname{Herm}_0(n, \mathbb C)$. Suppose

$$
N_m(\Phi(X)) \le N_n(X)
$$

for every CPTP map $\Phi$ from $M_n(\mathbb C)$ to $M_m(\mathbb C)$ and every $X \in \operatorname{Herm}_0(n, \mathbb C)$. Then there is a single $c > 0$ such that $N_n(X) = c \|X\|_1$ on every nonzero such space. The dimension-one space is zero and satisfies the identity trivially.

To prove this, let $X = X_+ - X_-$ be nonzero and set $t = \operatorname{tr} X_+ = \|X\|_1 / 2 > 0$. For any target $Y = Y_+ - Y_-$ with $s = \operatorname{tr} Y_+ \le t$, choose an output density matrix $\tau$ and put

$$
A = \frac{Y_+}{t} + \left(1 - \frac{s}{t}\right)\tau, \qquad B = \frac{Y_-}{t} + \left(1 - \frac{s}{t}\right)\tau.
$$

These are normalized positive states. If $P$ is the positive spectral support projection of $X$, the map

$$
\Phi(T) = \operatorname{tr}(PT)A + \operatorname{tr}((I-P)T)B
$$

is CPTP and satisfies $\Phi(X) = t(A - B) = Y$ exactly. Equal trace norms admit exact transports in both directions, hence the $N$-values are equal. Absolute homogeneity then gives the common constant $c$. This is a theorem on the full stated channel and matrix domain, not a selection of that domain from primitive difference or an assertion that every construction stays inside an arbitrary smaller scalar field. Exact difference-transport examples are in source-notes supplement §11.36.

### 11.4 Full-support Bell tables require positivity, not support alone

Four rational pair distributions can have full support while admitting no
positive common joint law. The supplied qubit construction uses a rational density matrix and $(3,4,5)$-triangle observables and has

$$
S_{\mathrm{CHSH}}=\frac{14}{5}>2.
$$

Every deterministic assignment is compatible with the support, so a
possibilistic classifier returns no obstruction. A positive common
distribution would be a convex combination of the sixteen deterministic
vertices, each of which satisfies $|S|\leq2$; therefore no such distribution
exists. This cleanly separates support gluing from positive probabilistic
extension. The broader contextuality and no-signaling scope is in §13.8.

### 11.5 The Cabello frame polytope has 146 half-integral vertices

Let $v_1,\ldots,v_{18}$ be the eighteen integer rays

$$
\begin{gathered}
(1,1,1,1),\ (1,1,1,-1),\ (1,1,0,0),\ (1,1,-1,-1),\ (1,0,1,0),\ (1,0,0,1),\\
(1,0,0,-1),\ (1,0,-1,0),\ (1,-1,1,1),\ (1,-1,0,0),\ (1,-1,-1,1),\ (1,-1,-1,-1),\\
(0,1,0,1),\ (0,1,0,0),\ (0,1,-1,0),\ (0,0,1,0),\ (0,0,1,-1),\ (0,0,0,1),
\end{gathered}
$$

and let the nine tetrads be their orthogonal four-element subsets. Every ray lies in exactly two tetrads, and the orthogonality graph and tetrad incidence are isomorphic to those of the Cabello configuration [2]. Put $P_i = v_i v_i^T / (v_i^T v_i)$, and let $A$ be its $9 \times 18$ tetrad incidence matrix. The frame polytope is $\mathcal P = \{f \in \mathbb R^{18} : f \ge 0,\ Af = \mathbf 1\}$. Its real-symmetric operator representative $H_f$ is defined by $\operatorname{tr}(H_f P_i) = f_i$. The ten-dimensional real-symmetric projector span and the rank-nine tetrad constraints give the unique trace-one representative.

Every extreme valuation is obtained by covering the nine tetrad vertices with disjoint isolated edges of weight one and odd cycles of weight one half. An exact enumeration yields 146 valuations. Their characteristic polynomials and multiplicities are:

| Multiplicity | Characteristic polynomial of $H_f$ | Smallest eigenvalue |
| :--- | :--- | :--- |
| 24 | $t^2(t-3/2)(t+1/2)$ | $-1/2$ |
| 72 | $t^2(t^2-t-1/4)$ | $(1-\sqrt2)/2$ |
| 2 | $(t-1)^2(t+1/2)^2$ | $-1/2$ |
| 48 | $(t^2-t/2-1/8)^2$ | $(1-\sqrt3)/4$ |

Hence no vertex representative is positive semidefinite; 26 have smallest eigenvalue $-1/2$, and the other 120 have smallest eigenvalue greater than $-1/4$. The complete input, enumeration argument, vertex list and exact reconstruction checks accompany the result. These statements concern the real-symmetric representatives, not arbitrary complex-Hermitian matrices that agree only on the sampled real rays. The enumeration, rank checks, and exact characteristic-polynomial certificates are described in source-notes supplement §11.52.

In the companion `QM-210` finite-map control (`python/finite_qm/use_cases/frame_function_control.py` and `omega_quantum_physics::quantum_import_finite_maps`), exact $\mathbb{Q}$-rank elimination shows that the linear Gleason residual vanishes not only on the full $9$-tetrad Cabello system (rank $9$, affine dimension $9$ inside the $10$-dimensional real-symmetric space $\operatorname{Sym}_4(\mathbb{Q})$) but also on prefixes of $3$ and $6$ tetrads (affine dimensions $7$ and $9$, with projector-span dimensions $8$ and $10$ respectively) and on the $24$-ray Peres configuration ($24$ contexts, rank $15$, affine dimension $9$, projector-span dimension $10$). Every rational frame function on the $6$-tetrad and $9$-tetrad Cabello sets and on the $24$-ray Peres set is represented by a unique trace-one real-symmetric quadratic form $P \mapsto \operatorname{tr}(\rho P)$ on $\operatorname{Sym}_4(\mathbb{Q})$ (while on the $3$-tetrad prefix, $10$ rays span an $8$-dimensional subspace of $\operatorname{Sym}_4(\mathbb{Q})$, leaving a $2$-dimensional real-symmetric annihilator; in $\operatorname{Herm}_4(\mathbb{C})$ of real dimension $16$, any real ray set additionally leaves open the $6$-dimensional imaginary skew-Hermitian subspace $i\mathfrak{so}(4)$). Over $\mathbb{F}_2$, the corresponding $\{0,1\}$ Kochen-Specker assignment systems have ranks $8$ and $14$ with augmented ranks $9$ and $15$, confirming inconsistency by exact parity elimination. What finite ray sets leave open is the positive-semidefinite cone: the rational trace-one matrix $\rho_2$ with rows $(0,-1/4,0,0)$, $(-1/4,1/2,0,1/4)$, $(0,0,1/2,0)$, $(0,1/4,0,0)$ is nonnegative on all $18$ Cabello rays and all $24$ Peres rays (minimum $0$ on both), yet has leading $2 \times 2$ principal minor $-1/16 < 0$ and quadratic value $-1/2$ on $(2,1,0,0)^T$.

### 11.6 A single rational context pair selects $p=2$ among power rules

Consider the positive-power family

$$
P_p(i)=\frac{|c_i|^p}{\sum_j|c_j|^p},\qquad p>0.
$$

For $\psi=(1,1,0)$, compare the standard basis with the rational orthonormal
basis obtained by a $(3,4,5)$ rotation fixing the first coordinate. The shared
ray has weight $1/2$ in the first context and

$$
\frac{1}{1+(3/5)^p+(4/5)^p}
$$

in the second. Agreement is equivalent to
$(3/5)^p+(4/5)^p=1$. The left side is strictly decreasing for $p>0$ and equals
one at $p=2$, so $p=2$ is the unique positive solution. This classifies the
declared power family; it is not a general Gleason theorem. Sorkin's
third-order sum [7] does not make this selection: for the polynomial measures
$(a+b+c)^p$ it vanishes identically at $p=1$, the additive case, and at $p=2$,
the quadratic case (source-notes supplement §11.52, check C46). Exact rational
controls for the integer powers $p = 1, \dots, 4$ accompany the general
monotonicity argument in source-notes supplement §11.58; the monotonicity step and
the equation over real $p$ are kernel-checked as stated in §4, item 3.

## 12. Reproduction and package boundaries

The publication is distributed as two archives with different purposes.

1. The paper archive contains this monograph, the source-notes supplement,
   retained source manuscripts, package-local Python reproductions, exact
   receipts, and checksum manifests.
2. The code-companion archive preserves the shared Rust workspace, the finite
   quantum mechanics native crate and campaign crate, and the Lean workspace in
   their repository-relative locations. Its own manifest binds every member.

The exact filename, byte count, and SHA-256 digest of the code companion are
recorded in `docs/code_companion.md` and bound again by
`CODE_COMPANION.sha256`.

From the extracted code-companion root, the focused trace-zero certificate is
run with

```text
cargo test --manifest-path omega_engine/crates_rs/Cargo.toml \
  -p omega_quantum_physics --test channels \
  trace_zero_repairs_need_uncentred_witnesses_on_two_cycles_of_qutrit_defects
```

The complete Lean workspace is built with

```text
cd lean4/quantum_mechanics
lake build
```

The dependency-free replay for the standalone $K_{2,3}$ paper (standard-library
rational arithmetic and focused `pytest` tests) lives in the sibling package
`F004_papers/013_trace_zero_quotient_duality/code` and is not part of this
archive; `companion_papers/trace_zero_quotient_duality_monograph.md` holds the
monograph text only. The paper archive is checked by

```text
python scripts/regen_sha256sums.py --check
python verify_deposit.py
```

These commands have separate evidence scopes. Exact certificate replay establishes
the displayed finite identities. A Rust or Lean build checks the statements
actually encoded in those sources. Manifest and archive verification establish
byte custody. None of these operations derives the physical premises named in
the manuscript, and this edition does not claim a fresh successful build of
every Rust and Lean target. The full implementation history and per-module
scope are retained in the source-notes supplement.

## 13. The quantum carrier, observer, and measurement problem

### 13.1 The current answer and the questions it leaves open

Our best current answer is a conditional operational account. A quantum carrier
supports the declared states, interactions and effects. An observer specifies
which of those operations are available, how an apparatus registers a result,
and which distinctions its reports must preserve. Measurement couples carriers
and makes information available in a record. A classical description can then
be sufficient for a specified set of questions even while the larger carrier
retains quantum coherence.

That account separates three objects: **the probability distribution of
records, the state conditioned on an obtained record, and one actual event**.
Neither a report label nor a reduced density matrix supplies the last object
by itself. A decision rule evaluates a supplied record; it is not a physical
mechanism that makes a particular outcome occur.

This account does not imply that every observer requires a quantum carrier. Defining
an observer model requires an adequate carrier, but does not determine
complex scalars, a Hilbert space, a tensor product or the Born rule. Those are
currently explicit inputs to the quantum models in this paper.

There are several measurement problems, with different obligations [9]:

- **Carrier and interaction:** why this state space, composition law and
  measuring dynamics are physically appropriate.
- **Preferred records:** which alternatives are distinguishable and stable
  under the actual apparatus and environmental couplings.
- **Probabilities:** why a specified instrument has its stated outcome weights,
  and under which domain and assumptions those weights have a Born form.
- **Definite outcomes:** what accounts for one event rather than the joint
  state or its distribution of possible records.
- **Agreement:** when records from different observers can be compared and
  composed without assigning incompatible experiments an unsupported common
  history.

Decoherence addresses the suppression of accessible interference and the
stability of certain records [8, 10]. It does not, under unitary evolution
alone, select a single event. Our finite account makes this boundary explicit
and offers tests at it; it does not announce a solution to every problem above.

### 13.2 The carrier and the declared observer

A finite-dimensional quantum model may have continuously many states; finite
dimension, a finite presentation and a finite state set are different claims.
In our exact models, entries lie in a declared field such as the Gaussian
rationals or a cyclotomic extension, with a specified conjugation and real
embedding. State admission requires Hermiticity, positivity and trace one.
Effects satisfy the operator inequalities between zero and the identity.
Some spectral operations require scalar extensions or supplied witnesses;
an exact implementation can refuse an unsupported input.

One abstract observer model,
\[
\mathcal O=(K,\mathcal F,\mathcal R,\delta,d_0,d_1,J,\mathcal M,\tau),
\]
names the carrier, local spaces, comparisons, defects, repairs, closure test,
gauge, compatible transformations and decision rule. For a quantum experiment
it also needs a preparation domain, system/apparatus/environment split,
interaction, instrument, accessible effect menu, readout and calibration
conditions. A physical apparatus realizes part of that model; a person or
conscious experience is not a required mathematical component.

One declared obstruction observer uses Hermitian edge defects and
\[
 J_Q(h)=\frac12\sum_e\|h_e\|_1,
 \qquad
 \Phi_Q([\delta])=\inf_\alpha J_Q(\delta-d_0\alpha).
\]
For a finite-dimensional real space of Hermitian edge defects and a linear
repair image, this is the quotient norm induced by $J_Q$; finite dimension
makes that image closed. It does not identify every
formal repair with a realizable quantum operation. Nor is every algebraic
projector a positive or completely positive channel. Positivity, physical
availability and question preservation
must be checked separately.

Observer relativity therefore means that the experiment and evaluation are
specified. It does not mean that an arbitrary decision label changes the
physical state, or that different descriptions license contradictory reports
about the same compatible experiment.

### 13.3 Interaction, readout and conditional updating

On a supplied finite quantum carrier, an instrument has completely positive
maps indexed by record labels. In Kraus form,
\[
 \mathcal I_i(\rho)=\sum_a K_{ia}\rho K_{ia}^{\dagger},
 \qquad
 \sum_{i,a}K_{ia}^{\dagger}K_{ia}=I.
\]
The sum of these maps preserves trace. Given the positive trace pairing,
\[
 E_i=\sum_aK_{ia}^{\dagger}K_{ia},\qquad
 p_i=\operatorname{tr}(E_i\rho)
     =\operatorname{tr}\mathcal I_i(\rho),\qquad
 \rho_i=\mathcal I_i(\rho)/p_i\quad(p_i>0).
\]
The unnormalized maps are linear; normalization is conditional on a
nonzero-probability record. A zero-probability branch has no normalized
conditional state. The non-selective state is the sum of the unnormalized
branches. These identities follow from the declared instrument and pairing;
they are not a reconstruction of either from inscription histories.

For an ideal projective instrument, the Kraus operators are the orthogonal
projectors themselves. This gives the Lüders conditional update and an
idempotent non-selective dephasing channel. General instruments need not be
projective, repeatable or idempotent. An effect specifies an outcome's
probability functional, but does not uniquely specify its disturbance map.
The measuring interaction and record grouping are therefore necessary data.

The exact finite implementation checks these identities and a dilation
for admitted Gaussian-rational inputs. It does not generate one physical
event. Conditional updating answers what follows **if this record occurred**;
it cannot be used as its own explanation of occurrence.

### 13.4 An exact record with recoverable coherence

Take two qubits, a system and an apparatus, with
\[
 |\psi\rangle=\tfrac35|0\rangle+\tfrac45|1\rangle,
 \qquad |A\rangle=|0\rangle.
\]
A controlled-NOT from system to apparatus gives
\[
 |\Psi\rangle=\tfrac35|00\rangle+\tfrac45|11\rangle,
 \qquad \rho_{SA}=|\Psi\rangle\langle\Psi|.
\]
Compare this with the dephased joint state
\[
 \sigma_{SA}=\tfrac9{25}|00\rangle\langle00|
             +\tfrac{16}{25}|11\rangle\langle11|.
\]
Both states give the same system reduction, apparatus reduction and pointer
distribution: the diagonal weights are nine twenty-fifths and sixteen
twenty-fifths. Repeated sharp pointer reads are consistent within the ideal
instrument. This is an available classical record distribution under the
declared pointer readout. It is not a proof that the joint state is the mixture
or that one pointer label was selected.

Their difference has only two nonzero entries, each twelve twenty-fifths,
between the basis vectors labelled 00 and 11. Its eigenvalues are
\[
 \tfrac{12}{25},\quad-\tfrac{12}{25},\quad0,\quad0,
 \qquad
 D_{\rm tr}(\rho_{SA},\sigma_{SA})=\tfrac{12}{25}.
\]
The bounded observable consisting of Pauli X on each qubit distinguishes
them: its expectation is twenty-four twenty-fifths for the coherent state
and zero for the mixture. Alternatively, applying the same controlled-NOT
again recovers the initial coherent system state from the first preparation;
the mixture yields a diagonal system state with the apparatus reset to zero.
The system's Pauli-X readout then distinguishes them by the same amount.

Every matrix entry in this example is rational. Its conclusion depends on
the admitted joint controls. If the apparatus or environment cannot be
controlled coherently, this erasure experiment may be unavailable. Extending
the model with an orthogonal environmental record can remove the coherence
from the system/apparatus reduction while retaining it globally. Losing access
to that distinction explains the adequacy of a reduced description for a
restricted task; it is not a derivation of objective collapse.

### 13.5 When a classical report is sufficient

Let the report be a map from the admissible histories or states to a record
space, and let a protected question have answer map q. Exact sufficiency is
\[
 q=\widehat q\circ p
 \quad\Longleftrightarrow\quad
 p(x)=p(y)\ \Longrightarrow\ q(x)=q(y).
\]
The factor is unique on the report image. Equality of the two maps' fibers
would impose a stronger faithfulness condition; factorization only requires
that the report never identifies different protected answers. For a future
experiment, the answer includes its probabilities or conditional reports,
so present agreement alone may be insufficient.

For a supplied nonempty effect menu, denoted separately from the compatible
transformation class by \(\mathcal E_{\rm adm}\), define accessible
distinguishability by
\[
 D_{\mathcal E_{\rm adm}}(\rho,\sigma)
   =\sup_{E\in\mathcal E_{\rm adm}}
      |\operatorname{tr}(E(\rho-\sigma))|.
\]
It is bounded by trace distance. The full complex effect domain implies
equality; a restricted menu also attains equality if it contains an optimal
distinguishing effect for the given pair. An arbitrary finite menu need not.
A classical
description is adequate at a declared tolerance only when it preserves the
protected answers under the admitted preparations, future controls, readouts
and time horizon. If a later control converts a discarded phase into a
readable population, the original population report was not dynamically
sufficient. An algebraic completion may require observables the apparatus
cannot measure jointly or cannot access at all.

A sharp pointer record algebra generated by orthogonal projectors is
commutative. The complete quantum algebra containing it need not be; even the
block-diagonal fixed-point algebra of dephasing can retain noncommuting
degrees of freedom within a higher-rank block. Thus a classical record can
be a subalgebra of a quantum carrier, rather than a moment at which the entire
carrier becomes classical. Its preferred basis comes from a specified
coupling and stability criterion. A degenerate coupling does not choose a
unique basis without further apparatus information.

The existing
[finite sufficient-record derivation](research/quantum_to_classical_descent/README.md)
establishes static factorization and invariant-row-space completion on its
declared linear carriers. It also distinguishes autonomous expectation
coordinates from jointly sharp measurements and from a realized event.
Its finite certificates and conditional analytic bounds retain those premises.

### 13.6 Outcomes, observer agreement and the remaining boundary

There is a useful elementary restriction on a density-only deterministic
outcome rule. Suppose an affine map sends every density state to a vertex
of a classical probability simplex and sends two pointer eigenstates to
distinct vertices. On their equal mixture, affinity requires the midpoint
of those vertices, which is not a vertex. No such map satisfies all three
requirements. This argument assumes the density state is the complete input
and classical mixing is represented affinely. It does not exclude an
additional configuration, a stochastic event law, a relative-branch account
or another explicitly enlarged carrier.

Different interpretations provide different further premises. A definite
configuration account supplies variables and dynamics beyond the density
description; an objective-collapse account modifies dynamics; a relative-state
account changes how outcomes are associated with observers and branches;
an operational account can take outcome occurrence as a primitive. These
are distinct positions, not alternative names for the same derived theorem.
None follows solely by assigning a software label or discarding an environment.

Records from multiple observers require compatible instruments, a declared
comparison protocol and retained history. Separate outcome tables do not
automatically admit a common nonnegative joint assignment across incompatible
contexts. Conversely, contextuality does not prevent agreement on compatible
pointer records. An observer who performs a coherent erasure has changed the
experiment relative to one who preserves and rereads the mark; a comparison
must include that change rather than merge both into an undeclared history.

Our current answer therefore explains, under supplied quantum premises,
how interactions furnish record probabilities, why particular reduced
descriptions can be adequate and stable, and how conditional updates compose.
It leaves two foundational burdens explicit: deriving the operational carrier
from native histories, and accounting for actual outcome occurrence under a
stated ontology or event law. Both questions remain open.

### 13.7 Testing two foundational carrier types

Begin with the hypothesis that a quantum carrier and a classical carrier are
distinct foundational types. The claim becomes testable only after declaring
their state spaces, readouts, allowed transfers and composition. Calling the
types distinct does not specify a prediction. Conversely, embedding a classical
register into a quantum matrix algebra does not prove that only quantum things
exist. We separate the following versions of the hypothesis.

| Hypothesis | Finite operational content | Result here |
|---|---|---|
| Two types coexist | Quantum systems and classical registers have their own admitted states and transfers. | Consistent hybrid models exist; the bare claim is not refuted. |
| A population record is the complete future carrier | Presently equal populations imply equal answers after every admitted control. | Refuted on the declared coherent-control protocol below. |
| Classical storage faithfully replaces quantum storage | Positive, normalized encoding and retrieval preserve arbitrary unknown qubit inputs. | Refuted by the sharp four-state bound below. |
| Additional classical variables explain quantum predictions | An enlarged classical description may depend on preparation, context, hidden variables or nonlocal dynamics. | Not excluded by the storage bound; its own premises and predictions must be tested. |
| The full quantum carrier is all that exists | No additional ontology is needed or exists. | Operational sufficiency does not decide this ontological assertion. |

**A consistent two-type countermodel.** Let
\[
 \mathcal A=\bigoplus_{\lambda=1}^{m}M_2(\mathbb C).
\]
A state is a tuple \((\rho_\lambda)_\lambda\), with each block positive and
\[
 \sum_\lambda\operatorname{tr}\rho_\lambda=1.
\]
Effects are tuples \(0\le E_\lambda\le I\); their probabilities are
\[
 \sum_\lambda\operatorname{tr}(E_\lambda\rho_\lambda).
\]
The center carries a
classical label, while each block retains noncommuting qubit observables.
Stochastic label changes and within-block quantum channels furnish consistent
finite operations. A normalized POVM and supplied density preparations give
the block transfer
\[
 \rho_\lambda=\operatorname{tr}(F_\lambda\rho)\sigma_\lambda.
\]
Summing the blocks discards the label.
The model can be presented over \(\mathbb Q(i)\) on its exact finite fixtures.

This is a genuine restriction of the full \(M_{2m}\) quantum model if
coherences and controls between label blocks are prohibited. Its matrix
embedding does not remove that restriction or decide its ontology. It also
supplies a distribution on labels, not a derivation of one occurring event.
Thus the existence of two operational types is mathematically consistent.
A claim that a particular apparatus must inhabit such a restricted type needs
evidence for the prohibited coherences and controls.

**Present equality is not future equality.** In the declared qubit basis let
\[
 |\psi_\pm\rangle=\tfrac35|0\rangle\pm\tfrac45|1\rangle,
 \qquad
 U=\begin{pmatrix}3/5&4/5\\-4/5&3/5\end{pmatrix}.
\]
Both states have population report \((9/25,16/25)\), but after the same
available unitary \(U\), the probability of the first basis outcome is
respectively \(1\) and \(49/625\). A model that identifies these states as the
same complete state cannot predict both answers using only that record.
Dephasing them to the same diagonal density operator makes their future
answers equal; it has changed the state, rather than faithfully retained the
discarded phase. This establishes that the population report is insufficient for
that future question. It does not rule out classical storage of additional
variables, nor assume that the displayed control is available in every device.

**A sharp classical-storage obstruction.** Consider an unconditional,
trace-preserving transfer of an unknown input qubit through a finite classical
alphabet and back to a qubit. The intermediate outcome may be random; the
protocol must succeed without postselection. Use the full positive qubit
state/effect model and affine mixing. The
encoder sees only the input state; it has no preparation label, quantum side
memory or retained coherent environment. The decoder returns a normalized
positive qubit state for each letter. No postselection or conditional success
loophole is included. The test basis is disclosed only after the returned
qubit is fixed; requesting a basis-dependent classical answer is a different
protocol. These premises give the measure-and-prepare form
\[
 \Phi(\rho)=\sum_\lambda
     \operatorname{tr}(F_\lambda\rho)\sigma_\lambda,
 \quad F_\lambda\ge0,\quad\sum_\lambda F_\lambda=I,
 \quad\sigma_\lambda\ge0,\quad
     \operatorname{tr}\sigma_\lambda=1.
\]
A positive affine encoder on the full density-state domain has POVM response
operators; an affine decoder from a probability simplex is specified by its
states at the vertices. Thus the displayed form follows from the stated
operational premises. It is also the standard classical-transfer form of an
entanglement-breaking channel [11]. The finite Choi matrix, with input factor
first, is
\[
 J_\Phi=\sum_\lambda F_\lambda^T\otimes\sigma_\lambda.
\]
It is positive, and tracing its output factor gives \(I\); complete
positivity and trace preservation therefore follow without choosing Kraus
square roots outside the coefficient field.

Let the four equiprobable inputs be
\[
 P_{Z\pm}=\tfrac12(I\pm Z),\qquad
 P_{X\pm}=\tfrac12(I\pm X),
\]
and define their average survival probability
\[
 S(\Phi)=\frac14\sum_{a\in\{X,Z\},\,s\in\{+,-\}}
      \operatorname{tr}\bigl(P_{as}\Phi(P_{as})\bigr).
\]
All four projectors have rational entries. The exact theorem is
\[
 \boxed{S(\Phi)\le\frac34.}
\]
It holds for every finite number of classical letters under the premises
above, and the constant is attained.

For a proof, use the real trace coordinates
\[
 w_\lambda=\operatorname{tr}F_\lambda,\qquad
 f_{\lambda a}=\operatorname{tr}(F_\lambda a),\qquad
 s_{\lambda a}=\operatorname{tr}(\sigma_\lambda a).
\]
The two-by-two determinant and trace conditions for positivity imply
\[
 f_{\lambda X}^{\,2}+f_{\lambda Z}^{\,2}\le w_\lambda^2,
 \qquad
 s_{\lambda X}^{\,2}+s_{\lambda Z}^{\,2}\le1.
\]
The omitted \(Y\) coordinates can only strengthen these inequalities.
Cauchy–Schwarz and \(w_\lambda\ge0\) give the nonnegative margin
\[
 d_\lambda=w_\lambda
       -f_{\lambda X}s_{\lambda X}
       -f_{\lambda Z}s_{\lambda Z}\ge0.
\]
Expanding the four traces and using \(\sum_\lambda w_\lambda=2\) yields
\[
 S(\Phi)=\frac12+\frac{1}{8}\sum_\lambda
      (f_{\lambda X}s_{\lambda X}+f_{\lambda Z}s_{\lambda Z}).
\]
\[
 \frac34-S(\Phi)=\frac18\sum_\lambda d_\lambda.
\]
Measuring \(Z\) and preparing its obtained eigenstate gives survival
probabilities \((1,1,1/2,1/2)\) in the order \(Z+,Z-,X+,X-\), attaining
\(S=3/4\). Identity quantum storage gives \(S=1\). A faithful positive
classical replacement preserving even these four preparations and their
retrieval tests therefore cannot exist under these premises. More classical
letters, shared randomness independent of the input, or an additional letter cannot
improve the bound: each normalized strategy has the same inequality, and
convex mixtures retain it.

For a declared error criterion, if all four survival probabilities are at
least \(1-\varepsilon\), the bound requires \(\varepsilon\ge1/4\).
More generally, if each retrieved state is within trace distance
\(\varepsilon\) of its input, its own projector's survival probability is
at least \(1-\varepsilon\), giving the same necessary bound. Randomly choosing
between \(X\) and \(Z\) measurement/preparation with equal weights attains
survival \(3/4\) and trace distance \(1/4\) on each of the four states:
the retrieved state is \(\tfrac34P+\tfrac14(I-P)\), whose difference from
\(P\) has eigenvalues \(\pm1/4\). Both four-state error bounds are sharp.
This is a bound on an unconditional classical-storage protocol, not a noise estimate
for an arbitrary apparatus or a statement about selectively successful trials.
Its exact rational certificate is the Rust module `classical_storage.rs`; no Lean
proof of this bound is provided.

**A static classical control and the boundary of the conclusion.** Four
classical letters with predetermined signs \((z,x)\in\{+,-\}^2\) reproduce
all the four preparations' static \(X/Z\) readouts: for a \(Z\) eigenstate,
put equal probability on the two matching \(z\) letters, and similarly for
an \(X\) eigenstate. This also preserves the equal-mixture identity
\[
 \tfrac12(P_{Z+}+P_{Z-})=\tfrac12(P_{X+}+P_{X-})=I/2.
\]
These finite tables do not refute a classical explanation.

What they cannot supply is a positive encoding/retrieval on the full qubit
carrier. A letter with definite \(x=z=+1\) would require a retrieved qubit
with both expectations equal to one: the unit-probability readouts force
that requirement on every letter with nonzero weight in both preparations.
The candidate
\((I+X+Z)/2\) has determinant \(-1/4\); allowing an extra \(Y\) coefficient
makes this determinant still smaller. Similarly, extending that letter's
response probability affinely to all qubits requires
\(F_{++}=(I+X+Z+bY)/4\), whose determinant is
\(-(1+b^2)/16\). Positivity fails. Restricting the admitted states and probes
to the four-state convex hull, allowing contextual responses, or supplying
a preparation label changes these premises and can evade the conclusion.
A classical computer storing known matrix entries is also a description of
inputs, not a positive physical encoding of an unknown qubit.

The result establishes a concrete asymmetry: classical records can live
inside a supplied quantum model, and may be sufficient for selected questions;
an unknown quantum state cannot in general be replaced and restored through
a solely classical positive carrier. Classical-looking behavior can reflect
restricted access to coherence, actual loss of coherence, or a restricted
hybrid model. Those possibilities must be distinguished by declared future
controls and protected questions. Neither this obstruction nor coherent
erasure refutes every two-type ontology, establishes that quantum ontology is
exhaustive, or supplies the missing event-selection law.

### 13.8 Three separate carrier distinctions

The two-type hypothesis becomes sharper when three different obstructions
are kept separate. A report can lose a required future answer; compatible
local probability tables can fail to have a positive global extension; and
a declared classical center can conflict with purification of every state. None
of these statements alone establishes that the quantum carrier is all that
exists.

**Test 1: future-question sufficiency.** Supply a finite preparation family,
a present POVM report, a CPTP control and a future POVM. The report is the
whole ensemble probability vector, not one sampled outcome. Ask whether the
probability of outcome zero of the future POVM factors through that report.
Two preparations with the same report and different answers disprove such
a decoder; otherwise a finite decoder is returned on the supplied family.
For
\[
 |\psi_\pm\rangle=(3|0\rangle\pm4|1\rangle)/5,\qquad
 U=\frac15\begin{pmatrix}3&4\\-4&3\end{pmatrix},
\]
Z populations coincide at \((9/25,16/25)\), but the probabilities of zero
after \(U\) are \(1\) and \(49/625\). Identity control passes the same
sufficiency test. Reporting the pulled-back future effect also restores
sufficiency on this family. This is the finite protected-question
criterion and the phase-blind descent obstruction on an exact
fixture. A pass on these two states does not prove sufficiency for every
preparation or every future control.

**Test 2: positive Bell gluing.** Supply the four binary pair distributions
for settings \(00,01,10,11\). Ask for nonnegative weights on the sixteen
assignments \((a_0,a_1,b_0,b_1)\) reproducing all four marginals. Exact convex
membership returns either those weights or a separating functional verified
on all sixteen deterministic vertices. Signed solutions to linear equations
are insufficient. For \(|\Phi^+\rangle\), take
\[
 A_0=Z,\quad A_1=X,\quad B_0=(4Z+3X)/5,\quad B_1=(4Z-3X)/5.
\]
The correlation vector is \((4/5,4/5,3/5,-3/5)\), hence
\(S=E_{00}+E_{01}+E_{10}-E_{11}=14/5>2\). Every context probability is
strictly positive: their numerators over 20 are respectively
\((9,1,1,9),(9,1,1,9),(8,2,2,8),(2,8,8,2)\), in
\((++,+-,-+,--)\) order. Thus a support-only compatibility test admits
all sixteen assignments and misses this obstruction. Another regression
has \(S=0\) for this orientation but violates a different CHSH facet;
the implementation tests the complete convex hull. Uniform independent
outcomes provide the positive extension control. The numerators displayed
here are the ones encoded in the Lean fixture; the Rust violation door V2 in
source-notes supplement §11.33 uses the companion orientation
\(B_1=(3Z-4X)/5\), with correlation vector \((4/5,3/5,3/5,-4/5)\) and the
same \(S=14/5\).

Bell locality and setting independence explain why one would require such
a joint table in a physical model; they are additional premises, not outputs
of the solver. In detail, suppose a common, setting-independent probability
measure $\mu$ on hidden states $\lambda$ and local response distributions
$A(a\mid x,\lambda)$, $B(b\mid y,\lambda)$ give the four pair tables.
Then
\[
 w(a_0,a_1,b_0,b_1)=\int
 A(a_0\mid0,\lambda)A(a_1\mid1,\lambda)
 B(b_0\mid0,\lambda)B(b_1\mid1,\lambda)\,d\mu(\lambda)
\]
is a nonnegative normalized table on the sixteen assignments and has those
pair marginals: sum out the unused response factors, whose sums are one.
This reduction works for finite, countable or continuous hidden-state spaces,
provided the stated probabilities are measurable. Increasing their cardinality
does not evade the obstruction. This finite result excludes that conjunction for the supplied
statistics. It does not exclude nonlocal hidden-variable models or establish
a unique ontology. The obstruction is failure of positivity-constrained
global gluing, which must not be conflated with signed linear exactness or
with a support-only contextuality obstruction. The source manuscript on
finite Bell bounds (source-notes supplement §11.33) already identifies this
joint-table premise; this test adds a shared executable experiment [26] and a
Lean marginal-to-CHSH proof.

**Test 3: central sectors and purification.** Declare the full positive
normalized states of \(A=\bigoplus_i M_{n_i}(\mathbb C)\), standard tensor
composition with another such algebra, and the available ancilla block
sizes. A state has normalized central weights \(p_i\) and block states
\(\rho_i\). A pure composite state occupies one joint central block, so
its marginal has one central weight equal to one. A state with two positive
central weights therefore has no pure extension within this model, for any
ancilla of this form. More quantitatively, every extension \(\omega\) of
that state and every marginal \(\sigma\) of a pure composite state obey
\[
 \operatorname{Tr}(\omega^2)\le\sum_i p_i^2,\qquad
 \tfrac12\|\rho-\sigma\|_1\ge1-\max_i p_i.
\]
For the first inequality, sum the squared weights of normalized joint
blocks, use purity at most one within each block, and then use
\(\sum_j p_{ij}^2\le(\sum_j p_{ij})^2=p_i^2\). For the second, the
central measurement is a trace-distance contraction and distinguishes
\(p\) from a point mass by \(1-p_k\). With a sufficiently large quantum
ancilla both bounds are sharp: purify each \(\rho_i\) inside a chosen
ancilla block for the first; for the second purify \(\rho_k\) in a block
of maximal central weight. The half-half classical mixture gives both
bounds \(1/2\). The exact finite calculation separately computes tighter
purity, rank and marginal-distance constraints for the listed ancilla sizes.
Lean establishes only the qualitative no-pure-extension statement, taking the
pure-block fact as a premise; the purity and trace-distance inequalities have
the prose proof above and a Rust replay.

A single sector has no central obstruction, but an undersized ancilla can
still prevent purification. The control with spectrum \((9/25,16/25)\)
needs an ancilla block of size at least two. Requiring purification for every
state rules out nontrivial centers only under these state-space,
composition and purity premises. It neither rules out a consistent hybrid
model that declines that requirement nor derives purification as a law of
nature. This is the conditional center-elimination step in the companion obstruction analysis;
real quantum theory's purification and the associativity of quaternion
multiplication are unaffected.

#### 13.8.1 Relation to finite report quotients

The three tests address distinct interfaces. Phase-sensitive readouts ask
whether a report preserves answers to declared future experiments. Positive
Bell extension asks whether compatible pair distributions are marginals of one
nonnegative joint law. The central-sector bounds ask what extensions are
possible in a specified direct-sum tensor model. None of these questions
selects the underlying quantum state space.

A finite protected-question quotient identifies two histories only when every
admitted continuation gives the same answer and remains available. That is a
minimal report relative to one finite experiment, not a derivation of positive
operator algebras, complex scalars, or tensor composition. Similarly, true
marginals and products of one-site marginals can each satisfy their consistency
conditions even when their difference is nonzero. Report locality, local
tomography, and Bell local causality therefore require different hypotheses.
The detailed comparison and local source addresses are in the source-notes
supplement and companion manuscript [12].

#### 13.8.2 From primitive difference to Bell: the endpoint and the open step

Two questions must be separated. First, the finite algebra of a Bell/CHSH
model closes once its state, observables, composition and probability rule are
supplied. Second, primitive difference alone does not force those quantum
inputs. Positive $L^1$ weights are additional carrier data, not a theorem of a
bare distinction relation. Once four binary response variables
$A_0,A_1,B_0,B_1\in\{\mathord{-}1,+1\}$ share one positive normalized joint
law, every deterministic assignment has

$$
S=A_0(B_0+B_1)+A_1(B_0-B_1)\in\{-2,2\},
$$

and convexity gives $|S|\leq2$. This conditional joint-extension theorem is proved in source-notes
supplement §11.33; it is not a derivation of Bell's theorem from $L^1$ alone. In
the CHSH scenario, Fine's theorem identifies existence of the relevant common
joint distribution with satisfaction of the complete Bell/CHSH family under
the compatibility assumptions [16]. Bell's physical conclusion additionally
uses locality and an identification of preparations, settings and outcomes
[14,15].

The quantum side is now equally explicit. On the declared bipartite carrier,
let

$$
\begin{aligned}
A_0&=Z,& A_1&=X,\\
B_0&=(Z+X)/\sqrt2,& B_1&=(Z-X)/\sqrt2,
\end{aligned}
$$

and use the entangled state $|\Phi^+\rangle=(|00\rangle+|11\rangle)/\sqrt2$
with the trace/Born pairing. The exact implementation constructs the CHSH
operator and verifies the two sum-of-squares inequalities

$$
-2\sqrt2 I\leq B_{\rm CHSH}\leq2\sqrt2 I\, .
$$

The same witness evaluates to
$S=2\sqrt2$ [17]. Every matrix entry in this witness is fixed by complex
conjugation: the construction lives in the real field $\mathbb Q(\sqrt2)$, the real subfield of $\mathbb Q(\zeta_8)$ in which the QM-218 code computes.
It is also static. Therefore a specifically complex $U(1)$ phase fiber and
continuous unitary time evolution are not necessary for a Tsirelson-saturating
CHSH witness.

| Boundary | What is now closed | What remains supplied or open |
| --- | --- | --- |
| primitive difference to positive weights | finite difference/cochain and quotient machinery | positivity and normalized preparation weights are admitted data |
| classical Bell face | one positive global joint law implies $\lvert S\rvert\leq2$ exactly | physical locality, setting independence and experiment identification |
| strict quantum violation | rational density matrix and observables give $S=14/5>2$ and no positive joint table | tensor composition, entangled preparation, measurements and Born/trace readout |
| quantum endpoint | exact SOS upper bound and exact witness give $S=2\sqrt2$ over $\mathbb Q(\sqrt2)$ | derivation or operational selection of the quantum inputs from native histories |

This also corrects the proposed “five-import boundary.” Its five imports (the
phase fiber, the quadratic readout, context parity, the frame function and the
clock tower, each mapped to finite data in the finite-map notes `research/phase_fiber_holonomy_bridge_finite_map.md`
through `research/clock_tower_finite_map.md`) remain useful as a catalogue of structures used by **full complex quantum
mechanics**, but they are neither proved independent nor a minimal basis for
Bell. Quadratic/inner-product geometry and the Born pairing overlap rather than
forming an established independence theorem. Same-party noncommutativity is
load-bearing for the maximal CHSH construction, while cross-party observables
commute. Bipartite composition and entangled preparation are load-bearing but
absent from the five-item cascade. Complex phase and continuous dynamics belong
to the larger theory, not to the static Bell minimum.

**Verdict.** The finite algebraic road ends at Bell: conditional on the declared
quantum interface, this repository now contains the classical bound, an exact
violation, the Tsirelson upper certificate and an attaining witness. The
foundational road from primitive difference does not end there. Its remaining
step is the first derivation target in Source Notes §6 (retained subsection
§13.9):
derive or operationally justify the positive composite algebra, state, effects
and pairing without silently importing the quantum model that the Bell calculation
uses.

#### 13.8.3 Čech contextuality and the Regge firewall

The sheaf-theoretic language sharpens the local-to-global part of this story,
but only when its objects and degrees are kept distinct. A measurement
scenario consists of a measurement set and a cover by compatible contexts. An
empirical model is a family of probability distributions on those contexts
whose marginals agree on overlaps. In Bell scenarios this compatibility is the
no-signalling condition; in general contextuality scenarios it is often called
no-disturbance. This is the compatible-family, or Čech degree-zero, condition
for the declared distribution presheaf [18]. It is not yet a first-cohomology
obstruction.

Abramsky and Brandenburger identify a global section of the distribution
presheaf with a noncontextual hidden-variable realization for a general
measurement cover [18]. Fine's theorem is the more specific CHSH result used
in §13.8.2 [16]. The cohomological refinement instead chooses a local section
in an abelian presheaf derived from the support and constructs an obstruction
class. A nonzero class is sufficient for contextuality, but the test is not
complete: contextual models with a vanishing chosen cohomological obstruction
exist [19]. Three distinctions follow.

1. Vanishing of the relevant obstruction class does not say that the whole
   cohomology group is zero.
2. Compatible local distributions do not automatically constitute a nonzero
   Čech $H^1$ class; the coefficient presheaf, chosen local section and
   coboundary maps must be declared.
3. The scalar CHSH excess

   $$
   \Delta_{\rm CHSH}=\max(0,|S|-2)
   $$

   is a useful violation margin, not a magnitude or norm of a Čech class. Thus
   the rational witness in §13.8.2 has $\Delta_{\rm CHSH}=4/5$, and a PR box
   would have $\Delta_{\rm CHSH}=2$, but these arithmetic facts do not define
   a cohomology theory. The rational witness excludes a positive global joint
   law; it does not, without a separately declared support construction,
   compute a Čech obstruction. PR boxes are among the examples for which the
   standard support-derived obstruction is known to be nonzero [19].

The Mermin--Peres scenario does support an exact finite local-to-global obstruction. Let
$d_0:\mathbb F_2^V\to\mathbb F_2^C$ map nine observable values to the six
context parities, let $s\in\mathbb F_2^C$ be the declared sign vector, and let
$\ell$ sum all six context coordinates. Every observable occurs twice, so
$\ell d_0=0$, while the odd target has $\ell(s)=1$. Hence
$s\notin\operatorname{im}d_0$. Every individual context and every five-context
subfamily is satisfiable, but the complete six-context family is not. This is
the exact locally satisfiable but globally inconsistent parity obstruction verified in source-notes supplement §11.50 and is
the finite combinatorial core of the Peres--Mermin argument [5,6,20]. It is safe
to call it a nonzero cokernel class. Calling it an $H^1$ class additionally
requires a declared next coboundary $d_1$ with $d_1s=0$; calling it a class in
$H^2$ requires a declared two-complex. The bare carrier graph has no degree-two
cochains. Finally, the parity contradiction itself is finite $\mathbb F_2$
algebra, but identifying its signs with quantum measurements uses the supplied
commuting two-qubit Pauli operator realization. It is not a derivation of that
quantum realization from parity alone.

Phase holonomy needs the same firewall. Transition functions for a specified
$U(1)$ bundle can form a Čech 1-cocycle, but Aharonov--Bohm and Berry holonomies
also depend on a connection and a loop [22,23]. Nontrivial connection holonomy
can occur on a trivial bundle, so it is not automatically a nonzero class in a
bare $\check H^1$ of transition data. Likewise, calling a phase a coboundary
requires a declared coefficient sheaf, cover and coboundary map. The paper
therefore retains phase holonomy as a conditional structural analogy, not as a
general identification with the contextuality obstruction above.

The same discipline blocks the proposed Regge identification. Regge calculus
places curvature on codimension-two hinges, with deficit

$$
\epsilon_h=2\pi-\sum_{\sigma\supset h}\theta_{\sigma h}
$$

for the appropriate dihedral angles [21]. In a two-dimensional equilateral
triangulation the hinge is a vertex: six triangles give zero deficit, five a
positive deficit and seven a negative deficit. That is a geometric curvature
diagnostic. It neither supplies a measurement cover nor empirical
probabilities. Even zero local deficits do not, without global hypotheses,
force trivial topology or holonomy.

Accordingly, no result here identifies a Čech obstruction with
$|\epsilon_h|$, establishes the bound $S_{\rm CHSH}\leq\min(4,2+|\epsilon_h|)$ or makes
curvature a prerequisite for Bell violation. The existing experimental API records
the angle but returns `None` for the Čech obstruction, Bell bound and
contextuality flag, including at zero deficit. The exact CHSH witness in
§13.8.2 is independent of Regge curvature and reaches $2\sqrt2$, so the
proposed unconditional implication $\epsilon=0\Rightarrow |S|\leq2$ cannot be
a general quantum theorem.

**Narrow claim and next test.** Čech cohomology can witness a declared
local-to-global obstruction, while Regge deficits measure declared simplicial
curvature; their resemblance is presently an analogy, not a bridge. A genuine
bridge must map a specified triangulation and hinge data to a measurement
cover, outcome presheaf and empirical distributions, prove overlap
compatibility, define the coefficient complex, and then derive a bound that
survives both a classical control and the zero-deficit quantum CHSH
counterexample. Until those data and proofs exist, the proposed bridge remains
open.

#### 13.8.4 Three-way finite expressibility, the four-wall reconstruction boundary, and finite-graph spin-statistics (`QM-223`)

The finite-carrier controls implemented in `python/finite_qm/use_cases/finite_qm_expressibility_and_measurement_control.py`, `python/finite_qm/use_cases/four_wall_reconstruction_and_operad_control.py`, and `python/finite_qm/use_cases/pauli_spin_statistics_graph_control.py` and formalized in Parts VIII–X of `lean/FiniteQM.lean` organize the results of this monograph into a three-way finite expressibility classification, four algebraic reconstruction walls, and the finite-graph spin-statistics and Pauli exclusion mechanism:

1. **Class I — Exact finite / cyclotomic algebraic and combinatorial identities of the finite models (zero truncation error on the declared algebraic spine).** Eleven structural pillars are exact on their declared finite-dimensional or finite-graph models over $\mathbb{Q}$ or $\mathbb{Q}(\zeta_N)$ (while continuum UV/IR analytic evaluations and transcendental periods enter via Class II rational interval enclosures):
   - *(i)* Exact finite Weyl clock-and-shift algebra $XZ = \omega ZX$ and discrete Fourier intertwiner $F X F^\dagger = Z$ over $\mathbb{Q}(\zeta_d)$.
   - *(ii)* Contextual parity and Bell/CHSH marginal-compatibility polytope separation ($S_{\mathrm{rational}} = 14/5 > 2$ over $\mathbb{Q}$, $S_{\mathrm{Tsirelson}} = 2\sqrt{2}$ with SOS certificate over $\mathbb{Q}(\zeta_8)$).
   - *(iii)* Exact $\mathfrak{su}(2)$ Kravchuk finite oscillator spectrum and $\mathfrak{so}(4) \cong \mathfrak{su}(2)_+ \oplus \mathfrak{su}(2)_-$ discrete hydrogen degeneracy $n^2$ over $\mathbb{Q}$.
   - *(iv)* Relational Page–Wootters clock dressing on the static constraint kernel $\ker(H_C \otimes I_S + I_C \otimes H_S)$ over $\mathbb{Q}(\zeta_N)$.
   - *(v)* Symanzik spanning-tree ($U_G$) and spanning-2-forest ($F_G$) polynomials and exact rational BPHZ Taylor forest subtraction on finite graphs.
   - *(vi)* Exact tree-gauge dressing and discrete Ward–Takahashi divergence identity $d^* J = 0 \implies Z_1 = Z_2$ over $\mathbb{Q}$.
   - *(vii)* Exact rational Dirac Clifford algebra $\{ \gamma^\mu, \gamma^\nu \} = 2\eta^{\mu\nu} I_4$, chiral projectors $P_L + P_R = I_4$, and $d = 2$ Schwinger axial anomaly census.
   - *(viii)* Exact electroweak $SU(2)_L \times U(1)_Y \to U(1)_{\mathrm{EM}}$ Weinberg projectors ($P_\gamma + P_Z = I_2$), custodial $\rho_{\mathrm{EW}} = 1$, and cubic hypercharge anomaly cancellation $\sum Y^3 = 0$ over $\mathbb{Q}$.
   - *(ix)* Exact 1-loop $\mathfrak{su}(3)_c$ Casimir invariants ($C_A = 3$, $C_F = 4/3$, $T_F = 1/2$) and Gross–Wilczek–Politzer coefficient $\beta_0(n_f) = 11 - \frac{2}{3}n_f > 0$ for $0 \le n_f \le 16$ over $\mathbb{Q}$.
   - *(x)* Spanning-tree Gribov-copy-free non-Abelian graph dressing vs. discrete lattice Gribov ambiguity on the 4-vertex diamond graph, and rational boost-composition hinge holonomy over $\mathbb{Q}$.
   - *(xi)* Finite-graph 2-particle configuration space and Abramsky–Ghrist square 2-complex $\operatorname{Conf}_2^{(2)}(G)$ (`QM-223`, Part X of `lean/FiniteQM.lean`): $P_3$ has $(V,E,F_\square)=(3,2,0)$ and $b_1^{(2)}=0$ (no exchange in 1D); the star $Y=K_{1,3}$ has $(6,6,0)$, $b_1^{(2)}(\mathbb{Q})=b_1^{(2)}(\mathbb{F}_2)=1$, and $\operatorname{tors}_{\mathbb{Z}_2}=0$ ($H_1 \cong \mathbb{Z}$, torsion-free); $C_4$ has $(6,8,2)$, $b_1^{(1)}=3$, $\operatorname{rank}(\partial_2)=2$, $b_1^{(2)}(\mathbb{Q})=b_1^{(2)}(\mathbb{F}_2)=1$, and $\operatorname{tors}_{\mathbb{Z}_2}=0$; planar 3-connected $K_4$ has $(6,12,3)$, $b_1^{(1)}=7$, $\operatorname{rank}(\partial_2)=3$, $b_1^{(2)}(\mathbb{Q})=b_1^{(2)}(\mathbb{F}_2)=4$, and $\operatorname{tors}_{\mathbb{Z}_2}=0$ ($H_1 \cong \mathbb{Z}^4$); whereas nonplanar 3-connected $K_5$ has $(10,30,15)$, $b_1^{(1)}=21$, $\operatorname{rank}_{\mathbb{Q}}(\partial_2)=15$, $\operatorname{rank}_{\mathbb{F}_2}(\partial_2)=14$, $b_1^{(2)}(\mathbb{Q})=6$, $b_1^{(2)}(\mathbb{F}_2)=7$, and $\operatorname{tors}_{\mathbb{Z}_2}=7-6=1 > 0$ ($H_1(\operatorname{Conf}_2^{(2)}(K_5);\mathbb{Z}) \cong \mathbb{Z}^6 \oplus \mathbb{Z}_2$; whether the exchange loop represents the $\mathbb{Z}_2$ class is not established here, and Lean shows only $\chi^2 = 1 \iff \chi \in \{+1, -1\}$ over $\mathbb{Q}$, with the Betti numbers computed from supplied $(V,E,F)$ counts and the $\mathbb{F}_2$/$\mathbb{Q}$ ranks computed in Python and Rust), yielding Slater determinant Pauli exclusion, Jordan–Wigner CAR nilpotency $c_i^2 = (c_i^\dagger)^2 = 0$, the Hanbury Brown–Twiss factor of $2$, and periodic-table shell capacities $2n^2 = (2, 8, 18, 32)$ with Madelung noble-gas closures $Z \in \{2, 10, 18, 36, 54, 86, 118\}$ (Lean checks the closures through $Z = 86$).

2. **Class II — Finite combinatorial spine + certified rational interval enclosures.** Four continuum period and renormalization-group observables have an exact finite graph/matrix spine in Layer 1 while their transcendental/irrational values are enclosed by nested certified rational intervals $[q_{\mathrm{lo}}^{(k)}, q_{\mathrm{hi}}^{(k)}] \subset \mathbb{Q}$ in Layer 2:
   - *(i)* 1-loop QED Schwinger anomalous magnetic moment $a_e^{(1)} = \alpha/(2\pi)$ enclosed to $12$ decimal places over $\mathbb{Q}$.
   - *(ii)* Renormalized 1-loop QED vacuum polarization $\Pi_R(q^2)$ and Uehling/Lamb-shift $s$-wave potential: the Uehling contribution to the $2S_{1/2}$–$2P_{1/2}$ difference is negative (about $-27.13\,\mathrm{MHz}$); separate $2S$ and $2P$ shifts are not computed here.
   - *(iii)* Multi-loop BPHZ forest-subtracted Feynman period integrals over rational simplex quadratures.
   - *(iv)* Integrated non-Abelian RG running coupling flow from rational Padé / interval step bounds.

3. **Class III — Strict finite no-go theorems and the Four-Wall Reconstruction Boundary (Parts VIII & IX of `lean/FiniteQM.lean`).**
   - *(a) Weyl–Heisenberg canonical commutation trace obstruction (`weyl_heisenberg_finite_trace_obstruction`):* For any $d \times d$ matrices $X, P$ over a commutative ring (the standard trace identity; Lean mechanises the $2 \times 2$ case over $\mathbb{Q}$ only), $\mathrm{Tr}(XP - PX) = 0 \neq \mathrm{Tr}(c I_d) = c d$ for $c \neq 0$, obstructing $[X, P] = c I_d$ on the full $d$-dimensional carrier; on the $d$-dimensional truncated / Kravchuk oscillator, $[a_d, a_d^\dagger] = I_d - d\,|d-1\rangle\langle d-1|$ satisfies $P_{d-1}[a_d, a_d^\dagger]P_{d-1} = I_{d-1}$ on the $(d-1)$-dimensional interior subspace $V_{d-1} = \operatorname{span}\{|0\rangle,\dots,|d-2\rangle\}$ while concentrating the trace-restoring boundary defect $-(d-1)$ on the top state $|d-1\rangle$.
   - *(b) Non-compact Lorentz boost unitarity obstruction (`lorentz_boost_non_unitary_in_finite_dim`):* In $1+1$ dimensions ($2 \times 2$; the $4 \times 4$ case is computed in Python only), hyperbolic boosts $\Lambda(\beta)$ preserve $\Lambda(\beta)^T \eta \Lambda(\beta) = \eta$ over $\mathbb{Q}$ but have Euclidean Gram trace excess $\mathrm{Tr}(\Lambda^T\Lambda) - 2 = (4\beta/(1-\beta^2))^2 > 0$ for $\beta \neq 0$.
   - *(c) Closed finite clock Poincaré recurrence vs. Kraus decoherence and Wigner's-Friend obstruction (`finite_clock_poincare_recurrence_vs_kraus_decoherence`, `wigners_friend_rational_chsh_multi_observer_obstruction`):* Closed cyclic clocks recur at $t = N$, whereas CNOT pre-measurement followed by partial trace reduces subsystem purity on $\frac{3}{5}|0\rangle + \frac{4}{5}|1\rangle$ from $1$ to $337/625$, and two-laboratory pre-measurements attain $S_{\mathrm{WF}} = 14/5 > 2$ ($S_{\mathrm{WF}}^2 = 196/25 > 4$).
   - *(d) Four-Wall Finite Reconstruction & Positivity Boundary (Part IX of `lean/FiniteQM.lean`):* (Wall 1) Busch 4-effect IC-POVM reconstruction in $d=2$ using unit Pythagorean Bloch vectors ($\det(M_{\mathrm{prob}}) = 9/1000 \neq 0$, $\det(M_{\mathrm{Bloch}}) = 18/125 \neq 0$) vs. the polyhedral Cabello/Peres frame-cone witness $\rho_2 \ge 0$ on all $24$ Peres rays (which contain the $18$ Cabello rays) with leading $2 \times 2$ minor $-1/16 < 0$ and quadratic value $-1/2 < 0$ on $(2,1,0,0)^{\mathsf{T}}$; (Wall 2) Galois-invariant SOS total positivity in $\mathbb{Q}(\sqrt{5}) \subset \mathbb{Q}(\zeta_5)$ (field norm $1/81 > 0$) vs. Galois-conjugate-indefinite field elements (field norm $-1/16 < 0$); (Wall 3) Characteristic-0 Mermin–Peres parity cocycle ($-1 \neq +1$) and Choi transpose singlet expectation ($-1/2 < 0$) vs. $\mathbb{F}_2$ collapse ($2 \equiv 0 \pmod 2$); and (Wall 4) exact rational Cayley unitarity $(1 - (\delta/2)^2)^2 + \delta^2 = (1 + (\delta/2)^2)^2$ and rational Rényi moments ($337/625, 193/625$) vs. truncated Taylor norm drift $1 + \delta^2 > 1$.

#### 13.8.5 Relativistic hydrogen fine structure, $2S_{1/2}$–$2P_{1/2}$ Lamb shift, and multi-electron helium / Roothaan–Hartree–Fock (`QM-224` & `QM-225`)

The atomic bound-state controls in `python/finite_qm/use_cases/atomic_dirac_lamb_hartree_fock_control.py` (`omega_quantum_physics::atomic_dirac_lamb_hartree_fock` and Part XI of `lean/FiniteQM.lean`) extend the finite algebraic spine to relativistic single-electron fine structure, radiative Lamb-shift degeneracy lifting, and multi-electron Coulomb-exchange and affine screening relaxation over $\mathbb{Q}$:

1. **Relativistic Dirac–Coulomb fine structure and $j=1/2$ degeneracy (`QM-224`, `dirac_coulomb_fine_structure_n2_and_darwin_spin_orbit_degeneracy`).**
   In the Sommerfeld–Dirac power series $E_{n,j}/(m_e c^2) = 1 - \alpha^2/(2n^2) - c_{n,j}^{(4)}\alpha^4 + \mathcal{O}(\alpha^6)$ with $c_{n,j}^{(4)} = \frac{1}{2n^4}\!\left(\frac{n}{j+1/2} - \frac{3}{4}\right) \in \mathbb{Q}$, the $n=2$ levels satisfy:
   - For $2S_{1/2}$ ($n=2, l=0, j=1/2$), the relativistic kinetic coefficient $13/128$ and Darwin contact coefficient $-8/128$ sum to $c_{2,1/2}^{(4)} = 5/128$.
   - For $2P_{1/2}$ ($n=2, l=1, j=1/2$), the relativistic kinetic coefficient $7/384$ and spin–orbit coefficient $+8/384$ sum to the identical rational value $15/384 = 5/128$, preserving exact $2S_{1/2}$–$2P_{1/2}$ degeneracy in the Dirac–Coulomb tree problem.
   - For $2P_{3/2}$ ($n=2, l=1, j=3/2$), the relativistic kinetic coefficient $7/384$ and spin–orbit coefficient $-4/384$ sum to $c_{2,3/2}^{(4)} = 3/384 = 1/128$, giving the exact rational fine-structure splitting coefficient $\Delta c_{\mathrm{FS}}^{(4)} = 5/128 - 1/128 = 1/32$ (or $\frac{1}{16}\alpha^2\,\mathrm{Ry}$), enclosing the Dirac–Coulomb splitting within $[10949.28, 10949.29]\,\mathrm{MHz}$ and the anomalous-moment-corrected splitting within $[10969.00, 10969.10]\,\mathrm{MHz}$.

2. **1-loop QED $2S_{1/2}$–$2P_{1/2}$ Lamb shift (`qed_one_loop_lamb_shift_contact_and_bethe_lifting`).**
   Combining the 1-loop vertex/self-energy contact coefficient $5/6$, the Uehling vacuum polarization coefficient $-1/5$ (`QM-216`), and the anomalous magnetic moment difference $1/12 - (-1/24) = 1/8$ gives the exact rational contact constant $5/6 - 1/5 + 1/8 = 19/30 + 1/8 = 91/120 \in \mathbb{Q}$ (the same constant enters `QM-216` and `QM-217`). Together with the true $2S$–$2P$ Bethe-logarithm difference enclosure $\ln k_0(2S) - \ln k_0(2P) \in [2.841786, 2.841787]$ ($\ln k_0(2S) \approx 2.81176989$, $\ln k_0(2P) \approx -0.03001671$), the Python and Rust controls compute the pure 1-loop non-recoil shift $\Delta E_{\mathrm{Lamb}}^{(1\text{-loop})} \in [1052.19339, 1052.19355]\,\mathrm{MHz} \subset [1052.19, 1052.20]\,\mathrm{MHz}$ (the Bethe logarithms are imported literature constants; Lean establishes the rational contact sum and the bracket arithmetic, not the MHz enclosure). Adding an externally supplied net higher-order remainder of $[5.645, 5.655]\,\mathrm{MHz}$ (which already includes the $\mathcal{O}(\alpha(Z\alpha)^5)$ binding term of about $+7.14\,\mathrm{MHz}$, two-loop, nuclear-recoil and proton-radius terms) gives an enclosure $[1057.70, 1057.95]\,\mathrm{MHz}$ that contains the Lundeen–Pipkin benchmark $1057.845\,\mathrm{MHz}$; this is consistency with an imported benchmark, not a prediction.

3. **Helium ground state, $1s2s$ ortho/para exchange splitting, and affine Clementi–Slater screening relaxation (`QM-225`, `helium_kellner_variational_bound_and_virial_identity`, `helium_ortho_para_exchange_splitting_and_rhf_contraction`).**
   - *Kellner–Hartree variational identity & Hylleraas secular matrix:* For $Z=2$, the hydrogenic screening functional $E_{\mathrm{He}}^{(1)}(Z_{\mathrm{eff}}) = Z_{\mathrm{eff}}^2 - \frac{27}{8}Z_{\mathrm{eff}}$ completes the square over $\mathbb{Q}$ as $(Z_{\mathrm{eff}} - 27/16)^2 - 729/256$, attaining its stationary minimum $E_{\mathrm{He}}^{\mathrm{var}} = -729/256\,E_h = -2.84765625\,E_h$ at $Z_{\mathrm{eff}}^* = 27/16 = 1.6875$ (improving on the unscreened value $-11/4 = -2.75\,E_h$ with exact virial balance $2T + V = 0$), while the 4-term rational Hylleraas correlated basis $(1, s, u, t^2)$ at $\zeta = 29/16$ gives the Rayleigh–Ritz upper bound $E_4 \approx -2.902450\,E_h$ (3-term $(1, u, t^2)$: $-2.902425\,E_h$); the displayed window $[-2.9038, -2.9024]\,E_h$ contains both, and its lower end is an imported benchmark, not a computed lower bound.
   - *Orthohelium vs. parahelium exchange splitting:* On the excited $1s2s$ manifold at $Z=2$, the direct Coulomb integral $J_{1s2s} = 34/81\,E_h$ and strictly positive exchange integral $K_{1s2s} = 32/729\,E_h > 0$ separate triplet orthohelium ($E({}^3S_1) = E_0 + J_{1s2s} - K_{1s2s} = -3097/1458\,E_h$) below singlet parahelium ($E({}^1S_0) = E_0 + J_{1s2s} + K_{1s2s} = -2969/1458\,E_h$) by $2K_{1s2s} = 64/729\,E_h > 0$.
   - *Affine Clementi–Slater screening relaxation and effective single-particle ionization surrogates:* For $\mathrm{He}$ ($1s^2$), $\mathrm{Be}$ ($1s^2 2s^2$), and $\mathrm{Ne}$ ($1s^2 2s^2 2p^6$), the damped affine relaxation map $T_{\mathrm{RHF}}(\mathbf{Z}_{\mathrm{eff}}) = \frac{1}{4}\mathbf{Z}_{\mathrm{eff}} + \frac{3}{4}(\mathbf{Z} - \sigma)$ driven by fixed imported empirical screening constants (He: $\sigma_{1s} = 5/16$; Be: $(5/16, 7/5)$; Ne: $(5/16, 11/4, 83/20)$ for $(1s, 2s, 2p)$; their provenance is not recorded in the repository) contracts in $\ell_1$ with factor $\lambda = 1/4 < 1$ toward $\mathbf{Z}_{\mathrm{eff}}^* = \mathbf{Z} - \sigma$ (He $27/16$; Be valence $13/5$; Ne valence $117/20$) and yields the effective screened single-particle ionization surrogates $I_1(\mathrm{Be}) = 169/500\,E_h < I_1(\mathrm{He}) = 217/256\,E_h < I_1(\mathrm{Ne}) = 13689/16000\,E_h$ (where $I_1(\mathrm{He}) = 729/256 - 2$ uses the Kellner functional, $I_1(\mathrm{Be}) = Z_{2s}^2/20$ and $I_1(\mathrm{Ne}) = Z_{2p}^2/40$).

#### 13.8.6 Tree-level QED scattering, chiral $V-A$ weak decay and CKM unitarity, and ABJ / Gell-Mann–Okubo hadronic identities (`QM-226`, `QM-227`, `QM-228`)

The controls in `python/finite_qm/use_cases/qed_weak_hadronic_control.py` (`omega_quantum_physics::qed_weak_hadronic_finite_maps` and sections `QM-226`–`QM-228` of `lean/FiniteQFTAndGravity.lean`) extend the three-layer architecture to tree-level Compton/Bhabha/Møller scattering, chiral $V-A$ weak currents and CKM mixing over $\mathbb{Q}(i)$, and anomalous/flavor hadronic identities:

1. **Klein–Nishina ratio, Thomson normalization, and Bhabha/Møller $s \leftrightarrow u$ crossing (`QM-226`, `kn_forward`, `kn_thomson`, `thomson_normalized`, `moller_eq_bhabha_su`, `crossing_st_witness`).**
   With $x = \hbar\omega/(m_e c^2)$, $u = \cos\theta$, and $\eta(x,u) = 1/(1+x(1-u))$, the Klein–Nishina ratio $R(x,u) = \frac{1}{2}\eta^2(\eta + \eta^{-1} - (1-u^2))$ satisfies $R(x,1) = 1$, reduces at $x = 0$ to $R(0,u) = \frac{1}{2}(1+u^2)$ with normalized angular antiderivative $F(1) - F(-1) = 1$, and takes exact rational values on the sample grid $x \in \{1/10, 1, 2\} \times u \in \{-1, 0, 1\}$. For massless tree-level $e^+e^-$ (Bhabha) and $e^-e^-$ (Møller) reduced amplitudes with $s + t + u = 0$, the $s \leftrightarrow u$ crossing identity $M_{\mathrm{M\o ller}}(s,t,u) = M_{\mathrm{Bhabha}}(u,t,s)$ and $t \leftrightarrow u$ symmetry $M_{\mathrm{M\o ller}}(s,t,u) = M_{\mathrm{M\o ller}}(s,u,t)$ hold over $\mathbb{Q}$ for all nonzero $(s,t,u)$, while the $s \leftrightarrow t$ exchange is refuted at $(s,t,u) = (5,-2,-3)$ ($361/25 \neq 1444/225$).
2. **Weyl-basis chiral projectors, muon phase-space polynomial and $G_F$ enclosure, and Cayley CKM matrix over $\mathbb{Q}(i)$ (`QM-227`, `chiral_projectors`, `projL_projR_vec`, `muonF0_factor`, `muon_qed_correction_negative`).**
   In the Weyl representation over $\mathbb{Q}(i)$ with $\gamma^5 = \operatorname{diag}(-1,-1,1,1)$, the projectors $P_L = (I_4 - \gamma^5)/2 = \operatorname{diag}(1,1,0,0)$ and $P_R = (I_4 + \gamma^5)/2 = \operatorname{diag}(0,0,1,1)$ satisfy $P_L^2 = P_L$, $P_R^2 = P_R$, $P_L P_R = P_R P_L = 0$, $P_L + P_R = I_4$, and $\operatorname{tr}(P_L) = \operatorname{tr}(P_R) = 2$, so the $V-A$ projector $P_L$ annihilates every right-handed spinor $P_R v$. The muon tree phase-space polynomial $f_0(x) = 1 - 8x + 8x^3 - x^4$ factors as $(1-x)(1-7x-7x^2+x^3)$, and any rational lower bound $p > 5/2$ for $\pi$ makes the 1-loop Kinoshita–Sirlin factor $25/4 - \pi^2 < 0$, enclosing $G_F/(\hbar c)^3 \in [1.16638176, 1.16638177]\times 10^{-5}\,\mathrm{GeV}^{-2}$. A skew-Hermitian generator $A \in M_3(\mathbb{Q}(i))$ near $\lambda = 9/40$, $A_W = 4/5$ produces via the exact Cayley transform $V = (I_3 - A)(I_3 + A)^{-1} \in \mathrm{U}(3,\mathbb{Q}(i))$ a unitary CKM matrix with exact $d$–$b$ unitarity-triangle closure $z_1 + z_2 + z_3 = 0$ and nonzero Jarlskog invariant $J = \operatorname{Im}(V_{ud}V_{cs}V_{us}^*V_{cd}^*) \neq 0$.
3. **Adler–Bell–Jackiw $\pi^0 \to \gamma\gamma$ colour factor and Gell-Mann–Okubo octet/decuplet relations (`QM-228`, `abj_factor_closed`, `abj_rate_ratio`, `gmo_octet`, `gmo_decuplet_equal_spacing`, `gmo_omega_from_spacing`).**
   For $Q_u = 2/3$ and $Q_d = -1/3$, the ABJ anomaly trace $S(N_c) = N_c(Q_u^2 - Q_d^2) = N_c/3$ gives $S(3) = 1$, $S(1) = 1/3$, and rate ratio $\Gamma(3)/\Gamma(1) = 9$, separating the $N_c = 3$ decay width enclosure $[7.690, 7.882]\,\mathrm{eV}$ from the $N_c = 1$ enclosure $[0.854, 0.876]\,\mathrm{eV}$. Under the broken-$\mathrm{SU}(3)_F$ mass operator $M = M_0 + M_1 Y + M_2(I(I+1) - Y^2/4)$, the baryon octet relation $2(M_N + M_\Xi) = 3M_\Lambda + M_\Sigma$ and the decuplet equal-spacing relations $M_{\Sigma^*} - M_\Delta = M_{\Xi^*} - M_{\Sigma^*} = M_\Omega - M_{\Xi^*} = -(M_1 + \frac{3}{2}M_2)$ hold identically as polynomials in $(M_0, M_1, M_2)$.

#### 13.8.7 Post-Newtonian light deflection and perihelion advance, 3-qubit GHZ/Mermin and 4-tick Page–Wootters / Kraus phase damping, and QWZ/Haldane Chern parity (`QM-229`, `QM-230`, `QM-231`)

The controls in `python/finite_qm/use_cases/regge_gravity_ghz_chern_control.py` (`omega_quantum_physics::regge_gravity_ghz_chern_finite_maps` and sections `QM-229`–`QM-231` of `lean/FiniteQFTAndGravity.lean`) complete the finite-map sequence across post-Newtonian gravity, 3-qubit multipartite contextuality and open-system decoherence, and 2D lattice Chern numbers:

1. **Stress-tensor trace separation, PPN light deflection, and $\pi$-free Mercury perihelion advance (`QM-229`, `flow_tensor_trace`, `null_probe_traceless`, `dust_trace`, `deflection_factor_values`, `gr_deflection_twice_newton`, `perihelion_factor_gr`, `mercury_per_orbit_arcsec`).**
   For the flow tensor $T^{\mu\nu} = e\,k^\mu k^\nu$, the Minkowski trace $T^\mu{}_\mu = e\,\eta(k,k)$ vanishes identically for a null probe $k = (1,1,0,0)$ and equals $\rho$ for rest dust $u = (1,0,0,0)$. The PPN deflection factor $(1+\gamma)/2$ equals $1$ at $\gamma = 1$ (GR) and $1/2$ at $\gamma = 0$ (Newtonian), giving $\delta\varphi_{\mathrm{GR}} = 4GM/(c^2 b) = 2\delta\varphi_{\mathrm{Newton}}$ ($[1.751190, 1.751191]''$ vs. $[0.875595, 0.875596]''$ at the solar limb), while the PPN perihelion factor $(2+2\gamma-\beta)/3 = 1$ at $(\gamma,\beta) = (1,1)$ yields the $\pi$-free exact rational per-orbit advance $3888000\,GM/(a(1-e^2)c^2)$ arcseconds ($42.980654''/\text{century} \in [42.97, 42.99]''/\text{century}$).
2. **Three-qubit GHZ/Mermin parity contradiction, 4-tick Page–Wootters clock history, and Pythagorean Kraus phase damping (`QM-230`, `pauli_ghz_sites`, `mermin_deterministic_bound`, `mermin_bound_attained`, `step_unitary_order_four`, `clock_shift_order_four`, `kraus_completeness`, `phase_damping_three_applications`, `phase_damping_coherence_three_steps`).**
   Over $\mathbb{Q}(i)$, the 3-qubit Pauli observables $A_1 = X\otimes Y\otimes Y$, $A_2 = Y\otimes X\otimes Y$, $A_3 = Y\otimes Y\otimes X$, and $B = X\otimes X\otimes X$ commute pairwise and satisfy $A_1 A_2 A_3 = -B$ via the single-site identities $XYY = X$, $YXY = -X$, $YYX = X$; the unnormalized GHZ state $(1,0,0,0,0,0,0,1)^{\mathsf{T}}$ has exact eigenvalues $(-1,-1,-1,+1)$ and Mermin eigenvalue $4$ for $M = B - A_1 - A_2 - A_3$, whereas all $64$ deterministic assignments $(x_i, y_i) \in \{\pm 1\}^6$ satisfy $|x_1 x_2 x_3 - x_1 y_2 y_3 - y_1 x_2 y_3 - y_1 y_2 x_3| \le 2$ (and non-eigenvectors such as $Z\otimes X\otimes X|\mathrm{GHZ}\rangle$ raise a typed `ReggeGravityGhzChernRefusal`). For the non-diagonal Gaussian-rational unitary $U = W\operatorname{diag}(1,i)W^\dagger$ ($W = \frac{1}{5}\begin{pmatrix}3 & 4i \\ 4i & 3\end{pmatrix}$, $U^4 = I_2$) and cyclic lowering shift $S$ ($S^4 = I_4$), the 4-tick history $|\Psi\rangle = \sum_{t=0}^3 |t\rangle \otimes U^t|\psi_0\rangle$ satisfies $(I_C\otimes U - S\otimes I_S)|\Psi\rangle = 0$ while the raising shift fails on $\psi_0 = (1,0)^{\mathsf{T}}$. For any Pythagorean triple $p^2 + r^2 = q^2$, the phase-damping Kraus pair $K_0 = \operatorname{diag}(1, p/q)$, $K_1 = \operatorname{diag}(0, r/q)$ satisfies $K_0^\dagger K_0 + K_1^\dagger K_1 = I_2$ and after three steps at $(3,4,5)$ maps $\rho_+$ to off-diagonal entry $27/250$ (coherence $(3/5)^3 = 27/125$).
3. **Qi–Wu–Zhang (QWZ) Dirac-point Chern parity and Haldane phase table (`QM-231`, `chern_table`, `chern_gap_closings_odd`, `chern_parity`).**
   Evaluating $\operatorname{sgn}(m + \cos k_x + \cos k_y)$ at the four high-symmetry Brillouin-zone points $k \in \{0,\pi\}^2$ gives $2C_1(m) = \operatorname{sgn}(m+2) - 2\operatorname{sgn}(m) + \operatorname{sgn}(m-2)$, which equals $(2, -2, 0, 0)$ at $m = (-1, 1, 3, -3)$ ($C_1 = (+1, -1, 0, 0)$), is odd at $m = \pm 2$, and is even for all $m \notin \{-2, 0, 2\}$; at $m = 0$ the gap also closes, the formula gives $0$, and $C_1$ is undefined there. In the Haldane honeycomb model, comparing $M^2$ against $27 t_2^2 s^2$ over $\mathbb{Q}$ classifies the topological phases $C = \mp 1$ ($|M| < |D|$) and trivial insulator $C = 0$ ($|M| > |D|$) without square roots.

#### 13.8.8 Derivation DAG status census and the closure module (`DerivationDagQMClosure`)

This section reports what the derivation DAG records and what the Lean closure module states. It is a census of status labels. It does not claim that the DAG is mechanized. A node's status labels that node's statement only. After the review of §13.8.12 a node stays `PROVED_LEAN` only when its statement lies within the narrowest claim the review supports; where it did not, the statement was narrowed or the status lowered.

<!-- BEGIN GENERATED dag-census (papers/core/tools/build_results_audit_table.py) -->

The derivation DAG (`dag/derivation_dag.json`, schema `derivation_dag.v2`) now has 880 nodes in 32 stages and 885 routes. The tables below are generated from that file by `papers/core/tools/build_results_audit_table.py`; they replace the earlier 177-node, 172-route partition.

| Node status | Nodes | PFP-reviewed |
| --- | ---: | ---: |
| `ADMITTED_PRIMITIVE` | 3 | 3 |
| `DEFINITION` | 91 | 14 |
| `PROVED_PROSE` | 27 | 0 |
| `PROVED_LEAN` | 261 | 100 |
| `COMPUTATIONALLY_CHECKED` | 152 | 22 |
| `CONDITIONAL` | 34 | 12 |
| `IMPORTED_ASSUMPTION` | 63 | 21 |
| `OPEN` | 168 | 5 |
| `REFUTED` | 2 | 0 |
| `SOURCE_RECORD` | 79 | 0 |
| **Total** | **880** | **177** |

| Route status | Routes |
| --- | ---: |
| `DERIVED_PROSE` | 104 |
| `DERIVED_LEAN` | 268 |
| `COMPUTED` | 156 |
| `CONDITIONAL_ON_IMPORT` | 91 |
| `GAP_NO_DERIVATION` | 185 |
| `RECORD_PARENT` | 81 |
| **Total** | **885** |

Of the 177 reviewed nodes, 69 are `consistent`, 18 are `caveat_added`, 65 are `statement_narrowed`, 25 are `status_lowered`. Only 213 of the 880 nodes cite two or more Lean declarations and two or more Rust witnesses; 388 cite no Lean declaration and 503 cite no Rust witness. A node's status is a label on its statement; it does not say that the statement is mechanized in both languages.

<!-- END GENERATED dag-census (papers/core/tools/build_results_audit_table.py) -->

Correction of edition 0.55.0. That edition called a "177-node, 172-route" DAG mechanized and said that every node carries at least two Lean 4 theorem bindings and two Rust witness bindings. The sentence was false and is withdrawn. The census above replaces it, and its last sentence states how many nodes actually carry both kinds of binding.

The closure module in this checkout is `lean4/DerivationDagQMClosure.lean`: 122 `theorem` declarations, no `sorry` and no `axiom` declaration in the file. It was not rebuilt for this edition. The earlier text also named a mirror `lean/DerivationDagQMClosure.lean` and a Rust file `native/src/derivation_dag_witnesses.rs` with 30 witness families; neither path exists in this checkout, and the earlier counts (112 theorems, 30 families) are historical, not re-verified. The Lean theorems summarized below prove statements about finite fixtures and generic algebraic identities. Their DAG nodes carry the status and the review boundary shown in each item.

1. **Partition conservation arithmetic (`master_dag_177_node_10_stage_and_172_route_partition_conservation`).**
   This theorem is a `decide` over numerals: it checks that a stated split of 177 nodes over 10 stages and of 172 routes sums correctly (its status split, $132+0+25+14+3+3=177$, is not the split quoted by edition 0.55.0). It does not read the graph and does not track the live DAG. The Rust witness named in the earlier text (`verify_tranche16_master_177_node_172_route_dag_completeness_and_operad_audit_witness`) is not in this checkout. Non-claim: the theorem validates no node, route or status of the live DAG.
2. **Coordinatewise $\ell_1$ emergence, Tier-1 maximal-symmetry gauge proportionality, replica extensivity, and $Z$-pinched branch localization (`gs003_coordinate_l1_weighted_sum_and_orbit_collapse`, `gs001_maximal_symmetry_direction_independence_and_gauge_proportionality`, `wdp_ch08_c01_replica_extensivity_homogeneity_and_l2_separation`, `l1_qm020_c10_branch_pinching_and_residual_sector_orbit_closure`, Family 26).**
   Section 21 of `lean/DerivationDagQMClosure.lean` and Family 26 of `native/src/derivation_dag_witnesses.rs` establish: (i) coordinatewise weighted $\ell_1$ decomposition $\nu(x_0, x_1, x_2) = \sum_i x_i \nu(e_i)$ under disjoint-support additivity and single-axis homogeneity, collapsing to $w \sum_i x_i$ under edge-transitive automorphisms, with drop-one countermodels separating quadratic $(1+1)^2 = 4 \neq 2$, anisotropic weights $(1,2,1)$, and $\ell_\infty$ max gauges; (ii) Tier-1 direction independence $j(u) = j(v)$ on unit vectors when endomorphism contractions act transitively, yielding gauge proportionality $j(x) = j(u_0)\|x\|$ and single-orbit weight uniformity; (iii) disjoint-replica extensivity of both $\ell_1$ and $\ell_2^2$, paired with degree-1 homogeneity failure of $\ell_2^2$ ($100 \neq 50$ on $2\cdot(3,4)$) and disjoint-support additivity failure of unsquared $\ell_2$ ($5 \neq 3+4$); and (iv) off-diagonal annihilation under $Z$-decoherence pinching $A + ZAZ = 2\operatorname{diag}(d_0, d_1)$, whereby $2|+\rangle\langle+|$ and $2|-\rangle\langle-|$ share the identical diagonal shadow $\operatorname{diag}(2,2)$ while separating on $\operatorname{Tr}(X\cdot)$ ($+2 \neq -2$).
   **Scope (DAG reviews) and non-claims.** `L1-GS000-EDGEWISE-L1` and `L1-GS001-GAUGE-L1` are `PROVED_LEAN` with `statement_narrowed`: they support the weighted two-edge $\ell_1$ decomposition, the exact transposition defect, the $\ell_\infty$ disjoint-additivity countercontrols and general transposition algebra under positive coordinates, and the eight signed-permutation gauge values, the swap anisotropy and an equal-length direction countercontrol. They do **not** prove the full H1–H5 classification or the graph-orbit theorem on its stated carrier, and they do not establish the maximal bounded-linear symmetry or the faithful edge-additive hypotheses, which must not be inferred from an eight-element test; nonnegative zero weights give a seminorm, not faithfulness. The orbit statements in (i) and (ii) therefore hold under the stated transitivity hypotheses only. `L1-WDP-CH08-C01-REPLICA-L1` (`statement_narrowed`) does not derive physical replica independence and does not exclude $\ell_2$. `L1-QM020-C10-BRANCH-LOCALIZATION` (`statement_narrowed`) gives a mathematical non-descent counterexample; it neither establishes nor refutes a branching or many-worlds interpretation.
3. **Spanning-tree holonomy gauge triviality, bit-shadow $P_7\text{-}C_{10}$ Bloch-contraction refutation, bare-table CHSH / PR-box separation, and `O022` registry-relative minimality (`ds_qm063_tree_gauge_triviality_vertex_repair_and_l1_non_factorization`, `ds_qm072_bit_shadow_q1_q4_obstruction_and_p7_c10_bloch_refutation`, `ds_qm073_bare_table_separability_single_joint_bound_and_pr_box_obstruction`, `ds_qm090_093_o022_registry_minimality_and_tier3_pr_box_bridge`, Family 27).**
   Section 22 of `lean/DerivationDagQMClosure.lean` and Family 27 of `native/src/derivation_dag_witnesses.rs` establish: (i) the Gaussian-integer two-path coherent intensity identity $|z_1 + z_2|^2 = |z_1|^2 + |z_2|^2 + 2\operatorname{Re}(\bar{z}_1 z_2)$, quarter-turn vertex gauge invariance $|i z_1 + i z_2|^2 = |z_1 + z_2|^2$, explicit vertex-potential trivialization $(\phi_0,\phi_1,\phi_2,\phi_3) = (0, c_1, c_1+c_2, c_1+c_3)$ on any 3-edge spanning tree, and $\ell_1$ non-factorization ($4 \neq 0$ at unit modulus); (ii) classical bit-shadow collapse of $2|+\rangle\langle+|$, $2|-\rangle\langle-|$, and $I_2$ onto $(1,1)$ alongside the $P_7\text{-}C_{10}$ linear map $(r_x, r_y, r_z) \mapsto (2r_x, 0, r_z)$ that preserves the diagonal coordinate on $(0,0,1)$ ($r^2 = 1$) while expanding $(1,0,0)$ to $r^2 = 4 > 1$ without complete positivity; (iii) exact rank-1 local product decomposition of any single $2\times 2$ context table, the 16-vertex deterministic CHSH identity $S^2 = 4$ ($|S| = 2$), and the four-tier squared CHSH hierarchy $100 < 196 < 200 < 400$ ($2^2 < (14/5)^2 < (2\sqrt{2})^2 < 4^2$, cleared by $25$); and (iv) unique selection of Row 6 (complex-Hilbert CPTP) within the frozen 7-row `O022` capability registry, paired with the $[5,7]$ super-registry non-transfer witness ($\min(5,7) = 5 \neq 7$) and the $24 = 16 + 8$ decomposition of $(2,2,2)$ no-signaling extreme rays into $16$ local deterministic vertices and $8$ PR-box vertices.
   **Scope (DAG reviews) and non-claims.** `DS-QM063-HOLONOMY-COHERENT-INTENSITY` is `PROVED_LEAN` with `statement_narrowed`: relative Gaussian holonomy and the two-path intensity are invariant under the retained common unit phases, and the rational unit-phase conditional is general in Lean. It does **not** prove the full graph-connection and tree gauge-trivialization theorem or matrix-valued holonomy transports, and no SU(2) trace bound or higher-form result is claimed; the vertex-potential trivialization in (i) is the displayed three-edge, four-vertex tree, not a theorem for every spanning tree. `DS-QM072-QUBIT-SUPERPOSITION-OBSTRUCTED` does not construct or admit the qubit/coherence carrier, and no generalized Bloch-contraction statement is accepted. `DS-QM073-FINITE-CHSH-AND-PR-BOX` does not formalize the transport from the concrete table to the general convex theorem, a full Fine converse or a quantum realization; "separable" for a bare classical table differs from quantum separability. `DS-QM090-092-AUTHORITY-FIREWALL` was lowered to `COMPUTATIONALLY_CHECKED`: it is toy zero-defect gate arithmetic and proves no authorization or no-constructor theorem. `DS-QM090-093-O022-REGISTRY-RELATIVE-MINIMALITY` is registry-relative; no all-registry or unique-QM minimality is proved.
4. **Three-layer $\mathrm{U}(1)$ selector exclusions, Everett reduced-state overlap and isometric refinement, threshold repair-image monotonicity, and four-tier plaquette descent (`ds_qm062_and_l1_u1_selector_frob_exclusions_and_gaussian_ring_injectivity`, `ds_qm094_everett_reduced_state_overlap_isometric_refinement_and_collapse_refutation`, `ds_qm101_threshold_repair_image_monotonicity_and_nogo_suppression_corollary`, `ds_qm206_four_tier_cochain_exactness_holonomy_invariance_and_nonfull_nonfaithful_descent`, Family 28).**
   Section 23 of `lean/DerivationDagQMClosure.lean` and Family 28 of `native/src/derivation_dag_witnesses.rs` establish: (i) the three-layer $\mathrm{U}(1)$ selector algebra across `DS-QM062-U1-SELECTOR-LAYERS` and `L1-U1-SELECTOR-OTHER-SEGMENT`, combining conjugation involution $S^2 = I_2$ ($S \neq I_2$), Frobenius exclusion of split-real zero divisors ($K^2 = +I_2$ with $(I_2+K)(I_2-K) = 0$) and non-abelian Pauli pairs ($X_2 Z_2 \neq Z_2 X_2$), and Gaussian-integer $\operatorname{cx}(a,b) = aI_2 + bJ$ ring additivity and injectivity; (ii) the Everett relative-state reduced-density record-overlap formula (`DS-QM094-EVERETT-RELATIVE-STATE-CONTACT`), where off-diagonal coherence $c_0 c_1 r$ vanishes at orthogonal record overlap $r = 0$, Pythagorean child sub-amplitudes $p^2 + q^2 = s^2$ conserve parent branch weight $p^2 w_0 + q^2 w_0 = s^2 w_0$, and the global swap observable separates the coherent entangled composite state from a genuinely collapsed diagonal mixture ($4 \neq 2$); (iii) combinatorial repair-image monotonicity (`DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE`, $B(x) \Rightarrow B'(x)$ implies $(1 - \mathbf{1}_{B'(x)}) \le (1 - \mathbf{1}_{B(x)})$), five-obligation conditional no-go suppression equivalence, and sub-threshold vs. super-threshold geometric scaling ($32 > 16 > 8$ vs. $96 < 144 < 216$); and (iv) 4-vertex plaquette cochain exactness $d_1(d_0 f) = 0$, coboundary invariance of plaquette holonomy, and Theorem 2.1 non-full / non-faithful diagonal descent $F_{\mathrm{Descent}}$ (`DS-QM206-BOUNDARY-SYNTHESIS`).
   **Scope (DAG reviews) and non-claims.** No $\mathrm{U}(1)$ selector is proved here. `DS-QM062-U1-SELECTOR-LAYERS` was lowered from `PROVED_LEAN` to `COMPUTATIONALLY_CHECKED`: the actual rational matrix products, Gaussian coefficients and the norm-multiplicativity and conjugation polynomials are checked, but the full ring homomorphism or embedding, the $\mathbb R/\mathbb C/\mathbb H$ selection hypotheses, continuity and global uniqueness are not, and algebraic controls do not exclude $\mathbb H$ by themselves; `DS-QM062-U1-RESIDUES-IMPORT` stays `IMPORTED_ASSUMPTION`. `L1-U1-SELECTOR-OTHER-SEGMENT` is `PROVED_LEAN` in the DAG but has not been reviewed (its prompt was never executed). `DS-QM094-EVERETT-RELATIVE-STATE-CONTACT` (`statement_narrowed`) does not prove the full tensor and partial-trace coordinate bridge or a physical record basis, and no branch selection or many-worlds ontology follows. `DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE` (`statement_narrowed`) is a toy queue, not a threshold theorem. `DS-QM206-BOUNDARY-SYNTHESIS` was lowered to `COMPUTATIONALLY_CHECKED`: the C4 map is a toy map, not a descent functor between defined GTOC and Hilb categories, and the QM205 pointer-basis stub is not discharged.
5. **Feynman two-slice action and refinement compatibility, discrete Hermitian graph Schrödinger mass conservation, diagonal exchange suppression, and Tier-3 survival / five-import cascade (`ds_qm032_feynman_refinement_compatibility_terminalizer_and_two_slice_action`, `ds_qm033_hermitian_graph_schrodinger_mass_conservation_and_lggr_holonomy`, `ds_qm073_diagonal_exchange_suppression_and_bell_three_clause_obstruction`, `ds_qm090_093_and_207_211_tier3_survival_rebit_tomography_and_five_import_cascade`, Family 29).**
   Section 24 of `lean/DerivationDagQMClosure.lean` and Family 29 of `native/src/derivation_dag_witnesses.rs` establish: (i) the finite-shadow two-slice free-particle action values $(2, 0, 2)$ on $\{-1, 0, 1\}$, two-step coarse-graining compatibility $r_{n,n+1}(r_{n+1,n+2}(k_2(y))) = k_0(y)$ vs. explicit `RefinementTear` refusal on mismatched intermediate slices, and the `CODA-A` convergence terminalizer (`DS-QM032-CONTINUUM-LIMIT-CONDITIONAL`); (ii) 2-vertex Hermitian graph Schrödinger probability mass rate conservation $\sum_v \dot{\rho}_v = 0$ via skew-symmetry of the off-diagonal probability current $(a_0 b_1 - b_0 a_1) + (a_1 b_0 - b_1 a_0) = 0$, paired with LGGR 3-cycle phase holonomy gauge invariance (`DS-QM033-SCHRODINGER-DISCRETE-COCHAIN`); (iii) characteristic-0 diagonal exchange suppression $c = -c \iff c = 0$ (`PL-GTOC-20` / `P8-C9`) vs. the $\mathbb{Z}/4\mathbb{Z}$ zero-divisor countermodel $2 \equiv -2 \pmod 4$, together with the three-clause Bell nature-claim obstruction (`DS-QM073-BELL-THEOREM-OBSTRUCTED`); and (iv) the `QM-093` Tier-3 survival theorem (`DS-QM090-093-QM-UNIQUENESS-TIER3`, with real-rebit local-tomography dimension failure $9 \neq 10$ vs. complex qubit $16 = 16$) and the 5-import `L1 -> QM` cascade (`DS-QM207-211-FIVE-IMPORT-CASCADE`).
   **Scope (DAG reviews) and non-claims.** `DS-QM032-FINITE-FEYNMAN-SHADOW` and `DS-QM032-CONTINUUM-LIMIT-CONDITIONAL` were lowered to `COMPUTATIONALLY_CHECKED`. The first supports the two-path interference residual $2pq$ with its cancellation and rational controls; the second supports that affine restriction maps compose and singleton states are compatible, and its retained separations show that this bookkeeping supplies no convergence bound. Neither supplies action weights, refinement, a measure or a convergence theorem, so no continuum limit is established, and (i) is not a convergence theorem. `DS-QM033-SCHRODINGER-DISCRETE-COCHAIN` was lowered to `COMPUTATIONALLY_CHECKED`: the full Gaussian $H\psi$ and derivative coordinates reproduce a zero instantaneous mass rate **and a nonzero exact Euler drift**, so an explicit Euler step has nonzero drift; item (ii) states only the instantaneous rate. It does not derive $H$, its units or interface, an exact propagator, or the matrix-to-rate transport, and gives no solution of a differential equation and no continuum limit. `DS-QM073-BELL-THEOREM-OBSTRUCTED` (`statement_narrowed`) does not derive a Bell, quantum or Tsirelson statement without the global-joint, operator and measurement assumptions admitted separately. `DS-QM090-093-QM-UNIQUENESS-TIER3` (`statement_narrowed`) does not give Tier-3 complex-Hilbert uniqueness: the full equivalence notion and the exclusion of competing packet theories are missing. `DS-QM093-SURVIVAL-THEOREM` was lowered to `COMPUTATIONALLY_CHECKED`: it is a truth table over a declared three-field antecedent, and the real survival antecedent is undischarged. `DS-QM207-211-FIVE-IMPORT-CASCADE` was lowered to `COMPUTATIONALLY_CHECKED`: it does not derive the five imports or establish their independence.
6. **Genesis-to-WDP five-obligation bridge, residual sector-weight non-uniqueness vs. $C_4$ orbit selector, `QM-122` eight-extra finish table, and conductor-5 real-embedding / `C750` Baker dichotomy (`pg_wdp_genesis_bridge_o01_o05_observer_completion_and_diamond_curl`, `l1_residual_sector_weights_minimizer_nonuniqueness_and_dihedral_selector`, `l1_qm122_leftover_mnc_eight_extra_finish_table_and_dilation_classifications`, `fq_embedding_relativity_and_entropy_baker_dichotomy_closure`, Family 30).**
   Section 25 of `lean/DerivationDagQMClosure.lean` and Family 30 of `native/src/derivation_dag_witnesses.rs` establish: (i) the `GEN-WDP-O01..O05` five-obligation Genesis-to-WDP bridge gate, observer completion dimension decomposition $d_H + (d_K - d_H) = d_K$ (`GEN-WDP-46`/`70`), two-event causal diamond price-curl flatness vs. assertion-fee curl $(1+2)-(1+1)=1\neq 0$ (`GEN-WDP-42`/`45`), and rational scalar norm obstruction $p^2 \neq 2q^2$ (`PG-WDP-GENESIS-BRIDGE-OBLIGATIONS`); (ii) 4-cycle minimum-$\ell_1$ representative non-uniqueness $(1,1,0,0)$ vs. $(0,0,1,1)$ yielding distinct 2-sector weights $(2,0) \neq (0,2)$ at $\Phi_1 = 2$ without a selector (`QM-020` Thm 3), collapsed by the dihedral $C_4$ orbit average to $(4,4)$ (`L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED`); (iii) the `QM-122-C31..C37` eight-extra finish table ($3+4+1=8$), $\mathbb{Z}[i]$ two-mode mixing weight doubling $|z_0+z_1|^2 + |z_0-z_1|^2 = 2(|z_0|^2+|z_1|^2)$ (`QM-122-C34`), `swapI` norm preservation outside the 2 real coordinate permutations (`QM-122-C35`), and the $2\times 2 = 4$ reversible dilation count on $\mathrm{Bool}\times\mathrm{Bool}$ (`L1-QM122-LEFTOVER-MNC-NOT-RECOVERED`); and (iv) 2D pure-state Gram minor vanishing $c_0^2 c_1^2 - (c_0 c_1)^2 = 0$ under every real embedding vs. the conductor-5 mixed witness $W_5 = \operatorname{diag}(-2+\sqrt{5}, 3-\sqrt{5})$ Galois conjugate sign flip ($\operatorname{evalAtS}(9) = (1,3) > 0$ vs. $\operatorname{evalAtS}(-9) = (-17,21)$ with $\varphi(120)/2 = 16$, `FQ-GAP-REAL-EMBEDDING-CHOICE`), together with the Rényi-2 purity deficit $d^2 - (p^2 + (d-p)^2) = 2(dp - p^2)$ and `C750` prime-reduction linear form vanishing $\gamma = 0$ on pure weights vs. $\gamma = 6 \neq 0$ on the uniform 4-state mixture (`FQ-ENTROPY-DICHOTOMY-BAKER`).
   **Scope (DAG reviews) and non-claims.** `PG-WDP-GENESIS-BRIDGE-OBLIGATIONS` and `L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED` are `PROVED_LEAN` in the DAG and have not been reviewed (their prompts were never executed). The first names five *open* bridge obligations; only its scoped control items are done, and no end-to-end Genesis-to-WDP claim follows. In the second the sector weights are declared inputs (to QM_003, QM_012 and QM_020), not derived from the $\Phi_1/\Gamma_2$ residual; the minimizer non-uniqueness and the $C_4$ orbit average concern the displayed 4-cycle, and the orbit average is a selector that has to be supplied. `L1-QM122-LEFTOVER-MNC-NOT-RECOVERED` (`statement_narrowed`) supports exact matrix-unit products and noncommutativity with Gaussian unit and nonunit controls; the finish table is not completion evidence and does not recover the complex field, the circle, Born uniqueness, the tensor and CPTP class, continuous time or the source carrier maps, which are retained as admitted. `FQ-GAP-REAL-EMBEDDING-CHOICE` was lowered to `COMPUTATIONALLY_CHECKED`: exact quadratic-field Gram and conjugate coefficients and a mixed-signature control are checked, but the coefficient-to-real embedding homomorphisms, the full Gram positivity and the cyclotomic fixed-field degree are not formalized, and a declared evaluation is not that embedding. `FQ-ENTROPY-DICHOTOMY-BAKER` (`consistent`) carries Baker's theorem as an explicit hypothesis; it proves no transcendence unconditionally and makes no base-two claim.

#### 13.8.9 Projective Cayley compactification, 5-adic half-angle obstruction, torsion-tower Haar orthogonality, Chebyshev/Taylor Cauchy completion, iterated quadratic square-root tower, and 4D $\mathbb{Q}(i)$ Hermitian Born + discrete Cayley Stone step (`FQ-GAP-U1-CIRCLE`, `FQ-GAP-BORN-UNIQUENESS-GLEASON`, `FQ-GAP-STONE-CONTINUOUS-TIME`)

The eight kernel-checked Lean 4 modules `lean4/U1PythagoreanObstruction.lean`, `lean4/U1PowerMapInjectivity.lean`, `lean4/U1CayleyProjectiveCircle.lean`, `lean4/U1CyclotomicTorsionTower.lean`, `lean4/U1CauchyCircleCompletion.lean`, `lean4/U1ChebyshevCauchyBridge.lean`, `lean4/U1QuadraticTowerAndCayleyStone.lean`, and `lean4/U1PhaseSynthesis.lean` (mirrored in `dag/results/FQ-GAP-U1-CIRCLE/runs/20261020T223000Z_u1_phase_completion_lean/` and replayed in `code/python/src/qm/u1_phase_completion.py` and `code/rust/src/qm/u1_phase_completion.rs`) formalize the exact algebraic obstructions and completion steps separating finite and rational phase models from the compact circle group $\mathrm{U}(1)$, the 4D $\mathbb{Q}(i)$ Hermitian Born trace pairing, and the discrete Cayley unitary step:

1. **Affine Cayley puncture, tangent-addition pole collision, and projective $\mathbb{P}^1(\mathbb{Q})$ closure (`cayley_misses_south_pole`, `cayley_mul_pole_collision`, `homCayley_infinity`, `homCayley_surjective`, `homCayley_projMul`).**
   Over $\mathbb{Q}$, the elliptic norm $u^2 + v^2$ is anisotropic (`elliptic_norm_anisotropic`), whereas the hyperbolic split-complex form $u^2 - v^2$ admits non-zero null vectors at $(1,1)$ (`hyperbolic_split_zero_divisor`). The affine Cayley map $t \mapsto \left(\frac{1-t^2}{1+t^2}, \frac{2t}{1+t^2}\right)$ bijects $\mathbb{Q}$ onto the punctured circle $S^1(\mathbb{Q}) \setminus \{(-1,0)\}$ and collides with the missing south pole whenever $t_1 t_2 = 1$; passing to homogeneous projective coordinates $[u:v] \in \mathbb{P}^1(\mathbb{Q})$ (`ProjRatLine`) maps the point at infinity $[0:1]$ to $(-1,0)$, surjects onto all of $S^1(\mathbb{Q})$, and intertwines globally with Gaussian circle multiplication via $\operatorname{projMul}([u_1:v_1],[u_2:v_2]) = [u_1 u_2 - v_1 v_2 : u_1 v_2 + v_1 u_2]$.
2. **Unbounded 5-adic half-angle obstruction, mod-5 Gaussian power injectivity, and quadratic restoration in $S^1(\mathbb{Q}(\sqrt{5}))$ (`four_fifths_not_rat_square`, `u345_no_rat_circle_sqrt`, `rat_circle_not_two_divisible`, `no_rat_add_to_rat_circle_hom_u345`, `u345IntPow_injective`, `wHalf_sq_eq_u345`).**
   Any square root $z = (x,y) \in S^1(\mathbb{Q})$ of the Pythagorean point $u_{3,4,5} = (3/5, 4/5)$ must satisfy $x^2 = 4/5$ and $y^2 = 1/5$. Unbounded 5-adic infinite descent over $\mathbb{N}$ and $\mathbb{Z}$ establishes that neither $4/5$ nor $1/5$ is a square in $\mathbb{Q}$, so $S^1(\mathbb{Q})$ is not $2$-divisible and admits no group homomorphism $\varphi : (\mathbb{Q}, +) \to S^1(\mathbb{Q})$ sending $1 \mapsto u_{3,4,5}$. Conversely, the Gaussian recurrence $(3+4i)^{n+1} \equiv 3+4i \pmod 5$ (`gaussPow34_succ_mod_five`) forces the integer power map $k \mapsto u_{3,4,5}^k$ on $\mathbb{Z}$ to be globally injective and torsion-free (`u345_infinite_order`). Adjoining $\sqrt{5}$ in `CircleQuadSqrt5` supplies the exact half-angle point $w_{\mathrm{half}} = \left(\frac{2}{5}\sqrt{5}, \frac{1}{5}\sqrt{5}\right)$ satisfying $w_{\mathrm{half}}^2 = u_{3,4,5}$.
3. **Cyclotomic torsion tower $\mu_N \hookrightarrow \mathbb{Q}/\mathbb{Z}$, finite Haar character orthogonality, and Chebyshev/Taylor Cauchy completion over `RegPhaseSeq` (`torsionPhase_refine_eq`, `rat_phase_divisible`, `rat_phase_every_element_torsion`, `haar_sum_root_of_unity`, `chebyshev_double_eq_ratCircle_sq`, `chebyshev_triple_eq_ratCircle_cube`, `taylorCos_nested_enclosure`, `taylor_pythagorean_defect_identity`, `cayleyDyadicPoint_on_circle`, `regPhaseSeq_precompact_approx`).**
   In contrast to $S^1(\mathbb{Q})$, the additive rational phase quotient $\mathbb{Q}/\mathbb{Z}$ is $m$-divisible for every $m > 0$ and satisfies exact finite Haar character cancellation $(1 - \zeta)\sum_{j=0}^{N-1} \zeta^j = 1 - \zeta^N = 0$, yet every element is torsion (`rat_phase_every_element_torsion`). On $S^1(\mathbb{Q})$, the Chebyshev polynomials $T_n, U_n$ satisfy the Pell-Chebyshev norm identity $T_n(c)^2 + s^2 U_{n-1}(c)^2 = 1$ and match the $n$-th multiplicative power in `RatCircle`, while the dyadic Cayley-Chebyshev approximant $\operatorname{cayleyDyadicPoint}(\theta, k) = \operatorname{cayley}(\theta / 2^{k+1})^{2^k}$ remains on $S^1(\mathbb{Q})$ at every finite depth $k$. The alternating Taylor cosine/sine partial sums satisfy nested interval enclosures $C_2(\theta) \le C_6(\theta) \le C_4(\theta) \le C_0(\theta)$ and $S_3(\theta) \le S_7(\theta) \le S_5(\theta) \le S_1(\theta)$ on $[0,1]$ with exact degree-6 unit-circle defect $1 - (C_4(\theta)^2 + S_3(\theta)^2) = \theta^6(8 - \theta^2)/576 \in [0, 1/72]$, and the finite $N$-torsion grids $\{k/N\}_{k=0}^N$ form an explicit $1/N$-net approximating every `[0,1]`-valued regular Cauchy sequence in `RegPhaseSeq` within $\frac{1}{N} + \frac{1}{N+1} + \frac{1}{m+1}$.
4. **Effect-additive 4D Hermitian $\mathbb{Q}(i)$ Born trace representation and Pauli-$Y$ coherence orthogonality (`HermitianMat2Qi.linear_functional_is_frobeniusTrace`, `HermitianMat2Qi.frobeniusTrace_weight_unique`, `HermitianMat2Qi.sigmaY_orthogonal_to_realSym`, `HermitianMat2Qi.frobeniusTrace_rankOneKet_eq_inner_mod_sq`).**
   Extending the 3D real-symmetric matrix carrier ($b_i = 0$) by the imaginary Pauli-$Y$ basis operator $\sigma_y = \begin{psmallmatrix}0 & -i \\ i & 0\end{psmallmatrix}$ yields the 4D $\mathbb{Q}$-vector space `HermitianMat2Qi` of $2\times 2$ Hermitian matrices over $\mathbb{Q}(i)$ spanned by $\{E_{11}, E_{22}, \sigma_x, \sigma_y\}$. Any $\mathbb{Q}$-linear effect-additive functional $f : \mathrm{Herm}_2(\mathbb{Q}(i)) \to \mathbb{Q}$ is uniquely represented by the Hermitian Frobenius trace $f(H) = \operatorname{tr}(W_f H)$ with $W_f = \langle f(E_{11}), f(E_{22}), \frac{1}{2}f(\sigma_x), \frac{1}{2}f(\sigma_y)\rangle$. For any unnormalized Gaussian-rational kets $\psi, \phi \in \mathbb{Q}(i)^2$, the rank-1 projector $P_\psi = |\psi\rangle\langle\psi|$ has determinant zero (`rankOneKet_det_zero`), trace $\|\psi\|_2^2$, and Frobenius pairing $\operatorname{tr}(P_\psi P_\phi) = |\langle\psi|\phi\rangle|^2$, while $\sigma_y$ is Frobenius-orthogonal to the entire 3D real-symmetric subspace (`sigmaY_orthogonal_to_realSym`), isolating the imaginary $\mathrm{U}(1)$ phase coherence $b_i = x_1 y_2 - y_1 x_2$ missed by real-symmetric tomography.
5. **Iterated real quadratic square-root tower $K_{m+1} = K_m(\sqrt{(1+c_m)/2})$ and discrete Cayley unitary step $(I - i t H)(I + i t H)^{-1}$ (`towerState_on_circle`, `towerState_pow_two_pow_eq_u345`, `TracelessHerm2Qi.cayleyStep_resolvent_right`, `TracelessHerm2Qi.cayleyStep_unitary_left`, `TracelessHerm2Qi.cayleyStep_comp_regular`, `TracelessHerm2Qi.cayleyStep_comp_pole`, `TracelessHerm2Qi.cayleyStep_preserves_born_trace`).**
   For any commutative ring $R$ with half-angle state $(c_m, s_m, w_m, v_m, \mathrm{half}_m)$ satisfying $c_m^2 + s_m^2 = 1$, $(1+c_m)w_m = 1$, $s_m v_m = 1$, and $2\cdot\mathrm{half}_m = 1$, the parametric quadratic extension $K_{m+1} = \mathrm{QuadExt}(K_m, d_m)$ with radicand $d_m = \frac{1+c_m}{2}$ and radical generator $\rho_m^2 = d_m$ constructs $c_{m+1} = \rho_m$, $s_{m+1} = \frac{1}{2}s_m w_m \rho_m$, $w_{m+1} = 2v_m^2(1+c_m)(1-\rho_m)$, and $v_{m+1} = 2v_m\rho_m$ purely polynomially (`HalfAngleState.step`). Inducting from $K_0 = \mathbb{Q}$ and $(c_0,s_0) = (3/5, 4/5)$ produces for every $m \in \mathbb{N}$ a commutative ring $K_m$ (`TowerRing m`) and unit-circle point $(c_m, s_m) \in S^1(K_m)$ whose $m$-fold circle square equals the embedded base point $(3/5, 4/5)$ (`towerState_pow_two_pow_eq_u345`). On the 3D traceless Hermitian subspace `TracelessHerm2Qi` over $\mathbb{Q}(i)$ with $H^2 = \|H\|^2 I_2$ ($\|H\|^2 = a^2 + b_r^2 + b_i^2$), the Cayley denominator $\Delta_H(t) = 1 + t^2\|H\|^2 \ge 1$ is strictly positive (`cayleyDenom_ge_one`), so the discrete Cayley step $U_H(t) = \frac{1 - t^2\|H\|^2}{1 + t^2\|H\|^2}I_2 - \frac{2t}{1 + t^2\|H\|^2}iH$ is well-defined over $\mathbb{Q}(i)$ for every $t \in \mathbb{Q}$, satisfies the exact resolvent identity $(I_2 + itH)U_H(t) = I_2 - itH$, left and right unitarity $U_H(t)^\dagger U_H(t) = I_2 = U_H(t)U_H(t)^\dagger$, $\det U_H(t) = 1$, and Born trace invariance $\operatorname{tr}(U_H(t) W U_H(t)^\dagger) = \operatorname{tr}(W)$ (`cayleyStep_preserves_born_trace`). Two Cayley steps compose via the projective-tangent parameter law $U_H(t_1)U_H(t_2) = U_H\!\left(\frac{t_1+t_2}{1 - t_1 t_2 \|H\|^2}\right)$ whenever $1 - t_1 t_2 \|H\|^2 \neq 0$ (`cayleyStep_comp_regular`) and collide with the south-pole obstruction $-I_2$ when $\|H\|^2 = 1$ and $t_1 t_2 = 1$ (`cayleyStep_comp_pole`), while the Pauli generators $\sigma_z, \sigma_x, \sigma_y$ at $t = 1/2$ recover the exact Pythagorean $(3/5, 4/5)$ rotations (`cayleyStep_pauliZ_half`, `cayleyStep_pauliX_half`, `cayleyStep_pauliY_half`).

**Non-claims.** The eight modules do not construct the compact circle group $\mathrm{U}(1)$, do not derive Born uniqueness or Gleason's theorem, and do not construct continuous time or Stone's theorem. The three DAG nodes named in the heading, `FQ-GAP-U1-CIRCLE`, `FQ-GAP-BORN-UNIQUENESS-GLEASON` and `FQ-GAP-STONE-CONTINUOUS-TIME`, remain `CONDITIONAL`. Items 1 to 3 are statements about $S^1(\mathbb Q)$, $\mathbb Q/\mathbb Z$ and rational Cauchy sequences; the continuous circle $\mathbb R/\mathbb Z$ stays an explicit completion structure. In item 4 effect additivity, positivity and normalization are hypotheses, not derived, and no projection-only (Gleason) route is proved. In item 5 the quadratic tower and the Cayley step are algebraic constructions over $\mathbb Q(i)$ and the fields $K_m$; they give no topology, no strong continuity and no generator selection, and the Cayley composition law is the tangent-addition law, not a one-parameter group. The reviews of these three nodes (§13.8.12) predate the eight modules, so their narrowest claims do not describe the modules; no second review of the Lean modules exists yet.

#### 13.8.10 Foundational monograph synthesis across QM_002 through QM_212: papers/foundations/theory_of_finite_quantum_foundations.md

The full structural landscape spanning the 43 discrete quantum foundation packets (`QM_002` through `QM_212`) is synthesized and unified in the dedicated monograph [`papers/foundations/theory_of_finite_quantum_foundations.md`](../foundations/theory_of_finite_quantum_foundations.md). That work provides the systematic 8-chapter obstruction calculus that underpins the finite quantum programme:
1. **§1 (Primitive Difference & Coboundary)**: Formulates cochain repair $\Phi_1([x])$ over directed graphs, obligation monoid cost floors $\ge 2$, and the 8-rung assumption ladder with 5 single-system countermodels ($M_{207}\text{--}M_{211}$).
2. **§2 (Superposition, Sorkin $I_3 = 0$ & Phase Selection)**: Distinguishes quotient fibers from diagonal mixtures, proves degree-4 selection of quadratic readout from $I_3 = 0$, and eliminates split-complex/dual-number rings via the norm-multiplicative elliptic involution $i^2 = -1$.
3. **§3 (Born Normalization & POVM Audits)**: Demonstrates rank-1 Hilbert lift redundancy on diagonal observables, eliminates quartic Gleason rivals in $d=3$ on $S^2(\mathbb{Q})$, and identifies the Busch polyhedral cone gap in $d=2$.
4. **§4 (Reversible Dynamics & Cayley Stepping)**: Formalizes the finite Wintner-Wielandt trace obstruction $[X,P] \ne i\hbar I$, constructs the Schwinger-Weyl intertwiner, and establishes exact unitary Cayley stepping over $\mathbb{Q}(i)$.
5. **§5 (Entanglement, CHSH & Contextuality)**: Evaluates bipartite correlation tensor obstructions, rational Bell violation ($S=14/5$), minimal cyclotomic Tsirelson attainment ($S=2\sqrt{2}$ in $\mathbb{Q}(\zeta_8)$), and Mermin-Peres $\mathbb{F}_2$ Čech cohomology obstructions.
6. **§6 (CPTP Channels & Trace Geometry)**: Formulates completely positive maps as stochastic kernel lifts bounded by trace-norm contractions and dual witnesses.
7. **§7 (Interpretations as Authority Shadows & Modal Realism Refusal)**: Enforces packet indistinguishability of interpretations and explicit refusal of modal realism on finite carriers.
8. **§8 (Asymptotics & Parity Schedules)**: Certifies quantum error correction threshold bounds as cochain repair capacities and formalizes measurement-only Majorana parity schedules obeying non-Abelian Ising fusion.

#### 13.8.11 Master derivation ledger from <> to quantum gravity: papers/core/master_derivation_ledger.md

Every individual derivation step in the Theory of Finite Quantum Mechanics—from the bare inert inscription `<>` (`TFQ-0000`) through primitive difference, discrete cochain repair, algebraic Hilbert lifts, Cayley stepping, entanglement, gauge theory, QED, electroweak, QCD, topological phases, to quantum gravity constraints (`TFQ-0111`), the continuum interface (`TFQ-0124`), and all application branches (`TFQ-0397` through `TFQ-0416`)—is indexed without omission in the companion master ledger:
- [`papers/core/master_derivation_ledger.md`](./master_derivation_ledger.md)
- [`dag/derivations/MASTER_DERIVATION_LEDGER.md`](../../dag/derivations/MASTER_DERIVATION_LEDGER.md)

Every ledger row binds directly to its standalone Markdown derivation paper in `dag/derivations/` and documents its DAG parent, epistemic status, mathematical statement, governing obligation, and multi-tier proof witnesses in Lean 4, Rust, and Python.

#### 13.8.12 DAG results audit

Each node of the derivation DAG that went through a PFP review (§13.8.13, item 8) carries a `pfp_review` object. The object records the narrowest claim the review supports, what the result does *not* support, and the effect on the node: `consistent`, `caveat_added`, `statement_narrowed` or `status_lowered`. The table below is that object, one row per reviewed node. It is the place to look before citing a node: the status label of a node is read together with its row. The review never raises a status. A node stays `PROVED_LEAN` only when its statement lies within the narrowest claim, or when the cited declaration was read and states it.

The table is generated, not typed. Regenerate it with `python -I -X utf8 papers/core/tools/build_results_audit_table.py --write` and test that it is current with `--check`. The script reads `dag/derivation_dag.json` and edits nothing under `dag/`. Every DAG-style identifier cited anywhere in this paper, including those in the table, resolves to a DAG node or a `theory_of_finite_qm.jsonl` record; `python -I -X utf8 papers/core/tools/check_dag_citations.py` checks that.

Three limits apply to every row. The reviews were written by a single local researcher and are not independent; the P5 host checks of the sealed runs read `recorded_pending_batch_review`. A review covers the result folder as it stood on the date of its review, and where a later run exists the node's `superseded_by` field names it; such a node is described by the later run's sealed record, not by the narrowest claim shown. A `consistent` row says that the DAG statement was found within the narrowest claim; it does not say that the statement is proved beyond that claim.

<!-- BEGIN GENERATED dag-results-audit (papers/core/tools/build_results_audit_table.py) -->

The table has one row for each of the 177 DAG nodes that carry a `pfp_review` object, in DAG order. *DAG status* is the status the node holds now; where the review lowered it, the earlier status is shown. *scope_effect* is `consistent` (statement kept), `caveat_added`, `statement_narrowed` (the statement was rewritten down to the narrowest claim) or `status_lowered`. *Narrowest claim* and *Does not support* are copied from the review.

| Node | DAG status | scope_effect | Narrowest claim | Does not support |
| --- | --- | --- | --- | --- |
| `PG-ROOT-DIFF-STRUCTURE` | `ADMITTED_PRIMITIVE` | `statement_narrowed` | The typed coproduct of two payload types (same two-constructor shape as OntologyBasic.Real0) is a categorical coproduct that supplies no map between the channels and no element of either channel: a map out of it that is the identity on one channel exists exactly when that channel is nonempty or the other is empty (so bare existence of such a map is not a reduction theorem for inhabited channels), and the two nonemptiness conditions are independent of the construction and of each other. | Anything about the actual OntologyBasic.Real0 beyond its constructor shape (the file is not imported; its payloads are universe-polymorphic record types). The real Real0 has the record TYPES PrimitiveDifference and Structure as channels; both are inhabited, so by retracts_to_pd_iff and retracts_to_s_iff retractions in both directions exist for it: the emptiness cases of this file are not instances of the real node, and nothing here says either channel is irreducible to the other. That either channel exists, is real or has an origin (admitted posits, ENC-1138 lineage withdrawn); the passage from the literal inscription (PG-INERT-DIAMOND, route marked GAP_NO_DERIVATION); the clauses "carrier-Structure precedes a primitive difference", "residual-Structure Q^1 = C^1/im d0 is what the difference produces" and "the ladder is a definability order"; any physical or interpretive reading. |
| `PG-INERT-DIAMOND` | `DEFINITION` | `caveat_added` | In a three-event admission model where supply is the identity by stipulation: in the unrooted replay a mention of <> (or any token) is invisible to every function of the admitted state; in the rooted replay the first supply of <> is an admission precondition and only later supplies are inert; the model predicate HasCoproduct is independent of inscribing <> (the identification Real_0 = Difference join Structure is not modelled), and coproduct without inscription occurs only in the unrooted model; inertness is the model rule rather than a consequence of the spelling; verified exhaustively for all traces of length <= 5. | The identification Real_0 = Difference joined with Structure (it is not modelled; only a stand-in predicate is shown independent of the inscription); the remaining three events of the six-operation alphabet (instance, rule, imposition) and their refusal rules; the Rust partial admission rules beyond the three-event fragment; any claim that supply is inert independently of the stipulated step rule; inertness of the FIRST supply in the rooted replay; any physical or interpretive reading of <>. |
| `PG-SIX-OPERATIONS` | `DEFINITION` | `caveat_added` | By construction of its six state components, only Admit writes the admitted component of the six-operation state machine, and it changes it iff the item is new; the Reading L / Reading F pair has different admitted states in this machine and the same admitted state in the machine in which Supply also admits (a two-machine comparison for every token). | That these six operations or state fields match any host, the Genesis Python model or the Genesis event semantics (forms, instances, requirements); that the six operations are distinct beyond writing distinct fields of this machine (Retain and Operate are gated on admission by definition); that conflating operations is the source of the Reading L / Reading F split of Genesis (a causal reading; only the model-level two-machine comparison is checked); more than two items or traces longer than 4 natively (the Lean statements are general, the Lean instances are Nat items); the inert-inscription model of PG-INERT-DIAMOND (cross-referenced, not imported); any physical or interpretive reading. |
| `PG-PRIMDIFF-AXIOMS` | `DEFINITION` | `caveat_added` | In a small product model (carriers of at most three points, at most one triangular face, A10 a free flag), the transcribed axioms A1, A4, A5 and A10 are jointly satisfiable and A1, A4, A10 are each violable alone from one point and A5 (together with A7) from three points; A3 holds because a reflexive-transitive closure is a preorder; A7 is A5 under the reading of A7 as d1 vanishing on im d0; the kernel enforces only A1 and carrier membership (the token is stored, never checked); and the transcribed R_cl rule refuses exactly on the exact-but-not-closed cell that d1 o d0 = 0 empties, a branch the source cannot reach because it rejects d1 o d0 != 0 at construction. This is evidence about a transcription of the list, not a derivation of it. | A derivation of the axiom list (obligation GEN-WDP-O01 and paper pin tfq_0394 stay open: this is a transcription and a small-model study, not a justification); that the predicates for A2, A4 and A6-A9 are the intended ones (the pinned file has names only; the one-line glosses come from an external copy of the file whose bytes differ from the pin); independence of A1 and A10 as a finding about the axioms (it holds by construction of the product model); A9: the relabelling check is an isomorphism (permuting vertex labels while keeping the cochain index-wise) and cannot fail, so it says nothing about observer-selected metrics; carriers of more than 3 points; real-valued Phi1, Gamma2 and R_cl values (here Phi1 is the unit-weight L1 distance to im d0 in integers and Gamma the L1 norm of d1 h); that the exact/closed classification equals classify_exact; any reachability of the source r_cl None branch; the Born, Hilbert or physical reading of any axiom. |
| `PG-ADMISSION-FLOOR` | `PROVED_LEAN` | `consistent` | A law-bearing cut (an irreflexive relation with an exhibited pair) exists exactly on carriers with two distinct points, its endpoints are apart, and a map separates the endpoints of every cut it carries into an irreflexive target; the pair of marks alone does not supply the relation or its law. | Deriving the law (irreflexivity) from the primitive difference <> or from Real_0: the relation and its law remain supplied data; any selection of a preferred cut or orientation (two orientations exist on two points); infinite carriers beyond the Lean statements; the arity-cost tie-breaker of the source (declared_arity_cost_selects is a decide on a priced toy, not used here); the aggregate local theorem pg_to_sn_and_wdp_route_chain_composition, which is a fixed enumeration. |
| `PG-COLLAPSE-BARRIER` | `PROVED_LEAN` | `caveat_added` | For maps p : X -> Y and s : X -> Z, no function of p reproduces s as soon as one fibre of p contains two points with different s values; with Z inhabited this is the only obstruction, and for finite X a nonempty tag alphabet of size k recovers s through (p, t) exactly when every fibre has at most k distinct s values. | Which tag or instance is added (the node does not select one, and the paper only exhibits predicates under a supplied decoder); the barrier for the inscription strings of the Pre-Genesis paper; infinite or non-function observation structures; universes above Type; any claim that an added tag exists in the physical or inscription regime; the source aggregate pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed, which is a bundle of fixed instances proved by rfl and decide. |
| `PG-HISTORY-REPORT-CRITERION` | `PROVED_LEAN` | `statement_narrowed` | For arbitrary types, an answer factors through the report image iff it is constant on report fibers, uniquely on the image; the direction constancy => factoring is proved from a selector of fiber representatives (a hypothesis, axiom-free) and, for an arbitrary report, with Classical.choice; necessity of a selector or of choice is not shown; verified exhaustively on 16 small function-space triples. | Necessity of a selector or of Classical.choice for the direction constancy => factoring (this node establishes no independence or unprovability result; the selector is a hypothesis, not a construction); the constructive listed-history reconstruction (node PG-PREGEN-CONSTRUCTIVE-SUMMARY); any structure on H, V or S, probability, measurement or physical interpretation of reports. |
| `PG-PREGEN-CONSTRUCTIVE-SUMMARY` | `PROVED_LEAN` | `caveat_added` | Over an explicit listing with decidable report equality, first-match reconstruction returns every listed answer iff the answer is constant on the listed report fibers, with no axiom in the kernel for the seven general theorems (relative to the supplied DecidableEq instance on reports); off the listing it refuses unreported values and can be wrong on unlisted histories; verified exhaustively on 11 non-degenerate small tuples. | Report types without decidable equality (only the classical instance is covered, its proof term uses Classical.choice, and necessity of choice there is not shown); infinite or unlisted populations beyond the explicit complete-listing hypothesis; the unconditional factorization for an arbitrary history type (node PG-HISTORY-REPORT-CRITERION); the external ListedHistorySummary.lean (not in this repository); any probability, measurement or physical reading of reports. |
| `PG-DEMAND-ACCOUNTING` | `PROVED_LEAN` | `statement_narrowed` | For finite sets, \|(W minus D) union B\| = \|W\| - \|D\| + \|B\| holds when D is inside W and the births avoid W minus D (births may coincide with discharged elements), it fails whenever exactly one of the two hypotheses is violated; when both are violated it holds if and only if \|D minus W\| = \|(W minus D) cap B\| (exact cancellation); and it imposes no constraint on a sequence of counts. | Which demands an engine actually carries; any claim that the displayed survivor sequence (0,1,1,1,0,1,1) is a native or general law (the source itself calls it a chosen ledger example); the preservation.py demand_step frozenset reading and any Python or Rust wrapper over it; multiset or ordered-log registers as a state beyond the filter-based list register of Paper.lean (the erase-based removeAll register of Paper001.lean is not re-proved, and the Nodup conjunct of that List Nat statement is only matched by the filter-based list_register_nodup_iff and the native census); the identification of the active count s_n with the cumulative history \|H_n\|; universes of more than five elements; any physical or thermodynamic interpretation. |
| `PG-REFINE-SEPARATES` | `PROVED_LEAN` | `statement_narrowed` | For a report q and a conflict relation C inside its collapse, SOME b-bit tag resolves all conflicts iff C has a proper 2^b-colouring (refine_separates_many); a GIVEN tag resolves C iff it is proper (resolves_iff_proper). The source refine_separates is the forward direction for one pair; refine_separates_iff is the one-pair equivalence on collapsed pairs. | Any algorithm, complexity or guarantee for FINDING a tag (the tables and the iff are existence statements, not search procedures); which tag a host should supply; the converse of the odd-closed-walk theorem in the kernel (Konig; native only); conflict graphs on more than 5 vertices beyond the 14 named ones; infinite carriers; any measurement, physical or interpretive reading of tags. |
| `PG-OLD-IMAGE-INJECTIVE` | `PROVED_LEAN` | `statement_narrowed` | A recovery r : B -> A + Unit obeying r(u a) = inl a exists exactly when u is injective. For an injective lift it is determined only on the image: there are (\|A\|+1)^(\|B\|-\|A\|) of them, exactly one of which refuses every off-image point; when \|A\| >= 1 and \|B\| > \|A\| the others accept some off-image point as an old term, and for \|B\| = \|A\| or \|A\| = 0 the recovery is unique. The law fixes neither observations nor obstruction predicates (persistence through the identity lift only). | Off-image rejection as a property of the S(n) retraction (that is PG-SN-OFF-IMAGE-REFUSAL, which needs an added soundness hypothesis on r); the pinned SnCarrier lift and retraction; any definition of obstruction repair beyond persistence of a Boolean predicate through a lift (the source repair_not_implied instance uses the constant-true predicate and defines no repair); sets with more than four elements in the native census (the Lean count law_card is general for finite types); infinite types for the count; any physical or categorical reading. |
| `PG-SN-OFF-IMAGE-REFUSAL` | `PROVED_LEAN` | `caveat_added` | For a restatement over an arbitrary glyph alphabet of the pinned S(n) section and retraction (five base shapes at a given stage), the retraction refuses exactly the presentations that are not section images at that stage, and the restated pair is a section/retraction pair (law and soundness) in the abstract sense, where refusal is the failure of the round trip s(r(p)) = p; this rests on the soundness of the specific retraction (accepted_only_from_section), because the old-image law alone is satisfied by a retraction that refuses nothing. | The claim that this closes the domain-restriction half of ledger row WDP-P001-019 (a ledger interpretation, not examined); the external prompt file fable_theorems_2026-10-17/05_sn_off_image_refusal.md named in the DAG source list, which was not read; off-image refusal for sections other than the five base shapes (nested lift, retraction or refusal terms as base members are outside the model); any cardinality claim about Carrier n or the declared table (node PG-SN-CARRIER); unrestricted old-image recovery (ledger row WDP-P001-019 stays a negative boundary for the unrestricted interface); the 36-glyph source alphabet beyond the generic statement, and alphabets above three glyphs in the native universes; wire parsing of the source grammar; decidability beyond this syntactic model (the source itself says the image condition is not a general computability theorem); the circular reading in which off-image is defined as failure of the round trip; any physical interpretation. |
| `PG-FREE-MONOID-NONISO` | `PROVED_LEAN` | `statement_narrowed` | A monoid isomorphism between free monoids on any two alphabets induces a bijection of the alphabets, so free monoids on finite alphabets of different sizes are not isomorphic and discrete categories with different finite object counts are not equivalent; a bare bijection of the underlying sets does exist for sizes at least one, so a numeral or alphabet re-presentation cannot be an isomorphism of the free-monoid (word concatenation) structure or of the discrete-category structure; other structures are not addressed. | Any structure on numerals or alphabets other than the free-monoid multiplication or the discrete category (a numeral or alphabet re-presentation may still be a non-isomorphic map, a set bijection, or an isomorphism of some other structure; no other structure, such as free commutative monoids, is examined); language restriction, partial recovery and total erasure (separate ledger row WDP-P001-009); infinite alphabets beyond the general Lean statement; the native homomorphism search covers short generator images only and is an instance, not the general theorem. |
| `PG-CHAIN-RETRACTION` | `PROVED_LEAN` | `caveat_added` | For chain maps i: C -> D and r: D -> C over a ring with r . i = id on the middle module and r commuting with the boundary, the induced map on homology is injective, so an extension admitting such an r cannot kill an old class; the two-points and triangle-with-face extensions kill a class (kernel, in the modelled degree fragment, and native) and admit no linear chain retraction (kernel, same fragment). | The bridge from declared inclusions to WDP-CH04-N02 (growth of the Genesis/WDP complexes does not repair an obstruction) for any actual Genesis/WDP complex pair; coefficient rings other than the declared one in the native tables; infinite or non-free complexes in the native tables; non-linear retractions and the full-complex (all degrees at once) formalisation of the two named cases; an integral failure of the converse for a genuine subcomplex inclusion (the Z instance is a one-term map, not a subcomplex); the converse over Q as a Lean theorem (it is a standard fact over a field, only observed here on the listed complexes); any physical reading. |
| `PG-MSS0-ONLY-DIAMOND` | `DEFINITION` | `consistent` | Exact declared stage-zero/node eligibility controls and an explicit structural-only authority ceiling are kernel/native checked. | Connect these tags to the actual profile registry and separate real mathematical/empirical validation. This structural rule supplies no physical, proof or authority certificate. |
| `PG-GEN-REGIME-EVENTS` | `DEFINITION` | `consistent` | Actual finite event/replay guards and complete state fields are retained; generic history composition and admitted-step evaluation are kernel checked. | Prove the full interpreter-to-source Regime equivalence and any event-to-obligation-vector transport. A declared event schema is not a derived physical or authority mechanism. |
| `PG-GEN-SUPPLY-NO-OP` | `PROVED_LEAN` | `caveat_added` | Exact supply-only and supply-plus-admission regimes are distinct; no-op supply and nontrivial admission are kernel checked on the generic event model. | Prove the exact source Regime representation bridge and retain both Reading L and Reading F. An external presentation cannot license an unrecorded admission. |
| `PG-GEN-SUPPLY-ERASURE` | `PROVED_LEAN` | `caveat_added` | Full guarded replay states agree after supply erasure on the retained histories; generic erasure/filterMap and supply-prefix identities are kernel checked. | Prove the partial Option/failure and five-field Regime representation bridge for every source history. Erasure does not erase guard failures, actual admissions or external custody requirements. |
| `PG-GEN-COLLAPSE-AND-FIRST-SEPARATION` | `COMPUTATIONALLY_CHECKED` (was `PROVED_LEAN`) | `status_lowered` | All 111 declared candidate sequences are replayed; no cost<2 response separates, six cost-two responses tie, and the two unary responses minimize the secondary arity sum. | Transport this bounded alphabet to arbitrary source Item arguments/arities and the full validResponse requirements; do not claim a global or physical minimum from a finite declared candidate set. |
| `PG-GEN-NO-RETURN` | `PROVED_LEAN` | `caveat_added` | Actual guarded regime traces, duplicate/no-op controls and two-switch mode cycles are retained; conditional count no-return/cycle lemmas are kernel checked. | Prove the complete array-to-source Regime interpreter refinement and that every real source regime change strictly raises the source potential. A count comparison alone is not that refinement. |
| `PG-GEN-IRREFLEXIVE-DISTINCT` | `PROVED_LEAN` | `consistent` | All two-term relation tables are checked, and irreflexive related endpoints are generally distinct in Lean. | Relate the bounded tables to the intended Genesis semantics and retain the irreflexivity premise. No assertion of seed-free distinctness, transitivity or orientation selection is made. |
| `PG-GEN-ONGOING-OBSTRUCTION` | `PROVED_LEAN` | `caveat_added` | All stated finite merge/addition/refusal controls and the remove-first/remove-last image equality are exact, with literal loop/Boolean kernel statements. | Formalize the full Legal/WF/Reach refinement and the build-structure answer with its minimality theorem. The illegal intermediate image is diagnostic, not an authorized performed change. |
| `PG-GEN-ONGOING-FEWEST-CHANGES` | `PROVED_LEAN` | `caveat_added` | Complete 68-state shortest-path tables for both apart seeds and exact edit-cost identities are retained; scalar lower-bound algebra is kernel checked. | Extend the refinement to merged-name states, arbitrary labels and all source identification steps and prove the full lower/upper transport. This apart-state search is not the unrestricted fewest_changes_A/B theorem. |
| `PG-GEN-REWRITING-COMMUTATION` | `PROVED_LEAN` | `caveat_added` | Full six-permutation merge squares and legality invariance are exact; general injective merge rewriting and map composition are kernel checked. | Prove source Step/ReachNoRemove and cost-potential transports for all term writings and the multi-step obstruction persistence theorem. Do not promote a finite permutation test into that source-wide result. |
| `PG-GEN-SAMENESS-REFINEMENTS` | `COMPUTATIONALLY_CHECKED` (was `PROVED_LEAN`) | `status_lowered` | Actual excess/plain/together arrays, cancellation cost and bounded two-term rewriting orbits are exact; pointwise excess/cost identities are kernel checked. | Formalize the generated-sameness equivalence with rewriting, then address raising (23), filled terms (24) and filled triples/balance (25). Their ledgers are inspected source material, not newly verified results. |
| `PG-SN-CARRIER` | `PROVED_LEAN` | `statement_narrowed` | For a Lean restatement of the pinned restricted S(n) model (SnCarrier.lean sha 357376de..., glyph alphabet abstracted, wrappers flattened), the base-presentation lift is injective with a left-inverse retraction at every stage and its image has 1+g+3g^2 points; the unrestricted lift has no recovery; the declared carrier table differs from the stage-independent base total 1+g+3g^2 at stages 0, 2 and 3 for every g (and at stage 1 unless g = 0), and no alphabet matches the per-shape counts g and g^2 at stages 1 and 2 together; the table is a declaration, not derived from the model. | A corrected cardinality theorem for the S(n) carriers: the table carrierCard remains a declared definition with no theorem relating Carrier n to the base presentations or the lift; off-image refusal completeness (node PG-SN-OFF-IMAGE-REFUSAL); nested lift, retraction or refusal terms as members of the base type; any theorem identifying the restatement with the pinned types at G = Glyph (36 letters and digits), and per-stage shape-count or cumulative-count statements in Lean (native-only); the real 36-glyph syntax beyond the instance baseCard 36 = 3925 and alphabets above six glyphs in the native certificate; wire parsing and the Python/Lean correspondence of the source; the locally defined UnrepairedCarrier of SnCarrierDischarge (a different type from Carrier); any physical, categorical or adjunction reading, including the string metadata of the custody-successor file mssn_functor_bridge.rs. |
| `PG-OBLIGATION-MONOID` | `PROVED_LEAN` | `statement_narrowed` | Obligation counters under pointwise sum are the free commutative monoid on the ids (cancellative, not a group); the re-declared copy of the source four-event three-counter trace is a homomorphism from event lists with total cost equal to length; in the abstract unbounded k-id model every successful generate/discharge run from the empty ledger keeps discharged within generated and a discharge succeeds exactly when it fits the outstanding count; Genesis events and S(n) maps being morphisms remains unproved. | That Genesis events or S(n) maps are monoid morphisms into the obligation monoid (TFQ-0342, PG-GAP-EVENT-OBLIGATION): the event-to-vector table evOb is copied from the source, not derived, and only lists of the four declared events are covered; any theorem tying Ev/evOb/trace to PrimGenEvent/eventObligation/traceObligation of DerivationDagQMClosure.lean (they are a re-declaration); any theorem connecting the Lean abstract-k unbounded ledger to the three-id u64 Python/Rust ledger; the Rust crate itself (nothing in omega_kernel is executed); unbounded or string-keyed ids; any claim that the 3-counter vector equals the free monoid on the real obligation ids. |
| `PG-WDP-PROTECTED-QUESTIONS` | `PROVED_LEAN` | `statement_narrowed` | On a bare set of at least two points no point is invariant under all permutations, and in the pointwise-stabiliser model the minimal selecting declarations are exactly the single declared points (price one declared point; price zero on a one-point carrier; no selection on the empty carrier); symmetry-price bookkeeping only. | Retention, dynamics or observers being not possible or available (WDP-CH03-N01 is a nonclaim, not formalised); that Selecting / MinimalSelecting formalises WDP-CH03-D01 (D01 minimises declared input sets whose removal restores a symmetry that moves the output, relative to an implementation class and dependency preorder; here the minimal declarations making some point invariant under the pointwise stabiliser are computed, and the two agree on singletons only because the output is the declared point); a Lean notion of equivariant selection function (no_fully_invariant_point is its bare-set specialisation); the price of selection on structured carriers (rigid, cyclic, graph) or under the setwise stabiliser; WDP-CH03-P03; infinite-carrier cardinality; any physical or interpretive claim. |
| `PG-WDP-DEGREE1-WINDOW` | `DEFINITION` | `statement_narrowed` | For modules over a field (the graph windows tensored with Q), kappa1 exists on Q1 = C1/im d0 exactly when d1 d0 = 0 (kernel); for graph windows with positive weights the weighted-L1 cost is the IsPhi defect of a nonnegative definite J, so Phi1 = 0 iff the class is zero (kernel); on the 17 tabulated integer windows Phi1 is the weighted-L1 minimum over rational potentials with a verified primal potential and dual vector; each (Phi1, Gamma2) pair has exactly one class: ExactClass iff Phi1 = 0, ClosedResidual iff Phi1 > 0 and Gamma2 = 0, ActiveClosureFailure iff both are positive (the Lean diag theorems state phi != 0, equivalent for Phi1 >= 0). | Any derivation of the window from Genesis admission or Real_0 (it stays a declared datum); norms other than weighted L1; non-graph d0 beyond the module-level lemmas; existence of the attained minimum for the weighted-L1 cost as a Lean theorem (attainment is part of IsPhi and is witnessed natively by x and y, but LP strong duality / minimiser existence is not formalised); complex coefficients; any meaning of Gamma2 for a non-window (representative dependent); that R_cl = Gamma2/Phi1 mixes the weighted Phi1 with the unweighted Gamma2 and so depends on the weight scale; any physical reading of the three classes. |
| `PG-WDP-QUOTIENT-EXACT-SEQUENCE` | `PROVED_LEAN` | `statement_narrowed` | For a window over a field with d1 d0 = 0 the sequence 0 -> H1 -> Q1 -> im d1 -> 0 is exact; no section is invariant under 1 + incl f pi when dim H1 > 0 and dim im d1 > 0 (kernel), and when dim H1 * dim im d1 = 0 there is exactly one section and it is invariant (kernel); every class has exactly one diagnostic class; Phi1 = 0 iff the class is zero for a definite J; and \|\|d1 h\|\|_1 <= c Phi1 for an attained minimum and c at least the J-to-L1 column bound. | Any derivation of the window; norms other than weighted L1 for the inequality; complex coefficients; a statement that the sequence has or lacks a section natural for automorphisms of the window (graph automorphisms preserving d0, d1 and the weights); the converse "if there is an invariant section then dim H1 * dim im d1 = 0" is native by dimension (section_dim) with the trivial-factor halves in the kernel; existence of minimisers for general norms; Phi1 >= 0 as a theorem for the weighted-L1 window (gamma2_nonneg is anchored, Phi1 >= 0 needs the cost bridge of the degree-1 window node); any physical reading of the classes. |
| `PG-WDP-GROWTH-NO-REPAIR` | `PROVED_LEAN` | `statement_narrowed` | For weighted-L1 graph windows with attained minima, restricting to a sub-window whose d0, cochain and weights are the restrictions (weights at most the restrictions of the big weights) never raises Phi1, and attaching 2-cells with d1 d0 = 0 leaves Phi1 unchanged and cannot lower Gamma2; in the native table, deleting cells, lowering weights and changing the cochain strictly lowered Phi1 (kernel instances exist only for raised weights and a changed d0). | Monotonicity for arbitrary norms J or renormalised weights (the instances show it fails), or when the sub d0 is not the restriction of d0; existence of minimisers for weighted L1 as a Lean theorem; that each of the three failing hypotheses is by itself sufficient to lower Phi1 in general (kernel instances exist for raised weights and a changed d0; the native rows cover deletion, a changed cochain and lowered weights); equal-weight subdivision and filtration limit pages (clauses of WDP-CH04-P09 absent from the source Lean); the source Gamma2 at a minimal residual of a non-closed window (non-unique, withheld); complex coefficients; any physical reading. |
| `PG-WDP-DIAGNOSTIC-NOT-ROUTING` | `DEFINITION` | `caveat_added` | Over hand-transcribed source tables, the diagnostic class, routing terminal, residual class and authority tag are different finite axes and nothing forces the partial class-to-terminal composite the source declares (the exact class is unrouted); a diagnostic value is at most a necessary eligibility gate for sealing a certificate, never authority. The source code itself names the exact class ExactRepair and tags ClosedResidual as StabilizedSurvivor, contrary to ledger N01. | That any policy from diagnostic classes to terminals is the correct one or is forced; WDP-CH04-O01, which stays conditional; any identification of terminal_status::ResidualClass (Exact, ClosedSurvivor, Open, Refused) with the diagnostic class (the unrelated omega_homology ResidualClass with values ExactRepair, StabilizedSurvivor, OpenObstruction has the three values of the diagnostic class and is not modelled); that the Rust class name ExactRepair and the ledger name ExactClass denote different things (the Lean exactRepairAllowed is the same predicate as certEligible, so the clause "ExactClass is not ExactRepair" has no anchor of its own); a route for the exact class (the source declares none); budget, rule or lift availability as routing inputs (none exist in the source routing code); evidence about the source from the leaves that are definitional in the model (authority counts, AuthTag); any physical or interpretive claim. |
| `PG-WDP-GENESIS-BRIDGE-OBLIGATIONS` | `OPEN` (was `PROVED_LEAN`) | `status_lowered` | In a three-status ledger model in which end-to-end is defined as all five discharged, scoped controls passing for all five obligations do not make the end-to-end claim hold, which holds exactly when all five are discharged; the node reading (all five control-only) is therefore not end-to-end; ledger bookkeeping only, no obligation is discharged. | That any of O01..O05 is discharged, dischargeable or refutable; the truth of any end-to-end bridge claim; any independent semantics of "end-to-end" beyond the definitional conjunction; that the register status of O01..O05 is control-only: the register labels each OPEN, and Open/ControlOnly/Discharged and the all-ControlOnly vector 11111 are this node's reading of the node statement (scoped controls done, end-to-end not); that no_sq_eq_two_sq bears on O04; the programme order as a logical dependency; Hilbert, Born, scalar or governance choices; any physical or institutional interpretation. |
| `L1-WDP-WINDOW-PHI1-GAMMA2` | `DEFINITION` | `consistent` | Actual flatness refusal, weighted quotient residual and Gamma2/Phi1 with explicit zero-denominator handling; generic kernel identities and refusal control. | Provide arbitrary typed cochain-window validation and norm choices and prove refinement to the production Phi1/Gamma2 contract. No probability or sector weight follows. |
| `L1-OBSERVER-AXIOMS-H1-H5` | `ADMITTED_PRIMITIVE` | `consistent` | Exact named rival defects and admitted weighted aggregate controls, with l-infinity and squared-energy counterexamples in Lean. | State and prove all observer axioms on the full finite projection and derive the conditional classification; these samples do not establish general axioms. |
| `L1-GS000-EDGEWISE-L1` | `PROVED_LEAN` | `statement_narrowed` | Weighted two-edge l1 decomposition, exact transposition defect and l-infinity disjoint-additivity countercontrols; general transposition algebra under positive coordinates. | Prove the full H1-H5 classification and graph-orbit theorem on its stated carrier, separately from finite examples. Nonnegative zero weights give a seminorm, not faithfulness. |
| `L1-GS001-GAUGE-L1` | `PROVED_LEAN` | `statement_narrowed` | All eight signed-permutation gauge values, swap anisotropy, and equal-length direction countercontrol; exact sign/swap laws in Lean. | Establish the actual maximal bounded-linear symmetry and faithful edge-additive hypotheses; do not infer them from an eight-element test. |
| `L1-WDP-CH08-C01-REPLICA-L1` | `PROVED_LEAN` | `statement_narrowed` | Exact concatenated l1, squared energy and coherent scalar-scaling comparisons; general algebraic replication/scaling distinction in Lean. | Specify the source aggregation and independent-replica axioms and prove a classification under them. This does not derive physical replica independence or exclude l2. |
| `L1-WDP-WITNESS-MASS` | `DEFINITION` | `consistent` | Exact atom and cell normalization, negative/zero refusal and generic rational normalization identity in Lean. | Prove arbitrary finite Boolean-algebra valuation uniqueness and source carrier refinement; declared mass does not derive probability interpretation. |
| `L1-QM002-O022A-PHI1-QUOTIENT` | `PROVED_LEAN` | `statement_narrowed` | Exact rational triangle primal construction, minimum weighted cost and gauge-shift invariance, plus general telescoping and lower-bound assumptions in Lean. | Refine arbitrary finite repair packets to Banach quotients and the unrestricted CODA-A bridge. The literal Lean bound theorem is a scalar interface, not an array refinement. |
| `L1-FRAMEWORK-KKT-CERT` | `PROVED_LEAN` | `consistent` | Exact supplied primal/dual certificate predicates for a triangle, with accepted and capacity/divergence/gap failures; generic rational bound-to-optimality implication in Lean. | Prove representation refinement to the external arbitrary-list integer certificate and arbitrary real-vector attainment. A valid numeric triangle certificate does not establish unrestricted dual attainment. |
| `L1-CHAIN-D1D0-AXIOM` | `ADMITTED_PRIMITIVE` | `consistent` | Actual triangle d1*d0 arrays, potential images and flat/nonflat controls, with general telescoping and a defective-row witness in Lean. | Derive functorial restrictions from admitted presheaf data and transport arbitrary finite cochain windows; zero on one potential is insufficient. |
| `L1-OPERATOR-LIFT-TRACE-EMBED-013` | `PROVED_LEAN` | `consistent` | Exact diagonal/singular-value mass, nonzero-scale invariance and declared-mass reconstruction controls; generic absolute scaling and sign-loss statements in Lean. | Construct the real Banach/operator embedding and exact signed-data reconstruction contract. Retain sign data separately; probability weights plus mass cannot recover signs. |
| `L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED` | `CONDITIONAL` (was `PROVED_LEAN`) | `status_lowered` | For the n-cycle with the unweighted L1 form, the set of minimizing residuals is the scaled simplex of sign-definite cochains with sum S (minimizer_iff); the sector weights are its block sums, which are not a function of (Phi1, Gamma2 = holonomy) for n >= 2, S != 0 and at least two sectors (sector_weights_not_determined), because (Phi1, Gamma2) determine only the signed holonomy S (hence Phi1 = \|S\| and the sign pattern); any single choice, including the cyclically symmetric average S/n, is an extra declaration, and with unequal declared masses the minimizer concentrates on the minimal-mass edges (native rows) so the masses themselves are the declared input. | Any derivation of declared sector weights from Phi1 and Gamma2 in the setting of the node source: the result is specific to EQUAL edge masses; for a weighted L1 form with a unique minimal-mass edge the minimizer, hence the sector weights, are unique (native weighted rows), so non-derivability can fail in the weighted setting that the node source declares (the masses are then the declared input); a Lean proof of the weighted statement or of the sum-of-squares reading of Gamma2; connected graphs of cycle rank > 1 (only two DISJOINT cycles are tabulated natively); the Hilbert lift, density matrices or any physical reading of the weights; that the dihedral or cyclic symmetry is itself available (it is an extra declared input). |
| `L1-DENSITY-LIFT-SIGNED-SQRT-PUB009` | `PROVED_LEAN` | `statement_narrowed` | Exact signed-square density projectors, overlap/Xi², zero-mass refusal, saturation and positive-support controls; general normalized Cauchy algebra and zero-weight strictness counterexample in Lean. | Prove the full real-square-root/trace-distance transport and conditional KKT overlap theorem under positive weights. Only Xi² is reported; no fabricated decimal Xi or unconditional Xi<1 is admitted. |
| `L1-QM020-THM1-DIRECT-NORMALIZATION` | `PROVED_LEAN` | `statement_narrowed` | Exact idempotence, nonzero scaling and positive-ray-premise controls; general normalization algebra and a negative-ray counterexample in Lean. | Refine arbitrary lists and positive-mass ray classification to the source theorem. Do not claim positive-ray equivalence under nonzero totals alone. |
| `L1-QM020-THM2A-L1-ADDITIVITY-DEFECT` | `PROVED_LEAN` | `statement_narrowed` | Exact scalar and disjoint-vector defect arrays, with a general disjoint-sign identity and the opposite-sign counterexample in Lean. | Prove source/list refinement and extend any l^p statement only under its real/natural exponent hypotheses. The false disjoint-same-sign biconditional is explicitly rejected. |
| `L1-QM020-THM2B-MINKOWSKI` | `IMPORTED_ASSUMPTION` | `consistent` | Exact natural-power strictness/equality controls, with general p2 positivity and p3 algebra in Lean. | Discharge the full real-p Minkowski/strict-convexity import and arbitrary-vector transport. Zero vectors are equality cases, not strict cases. |
| `L1-QM020-THM3-ROW-SPARSITY` | `PROVED_LEAN` | `statement_narrowed` | Exact phase-sign readouts, row sparsity, determinant, monomial and rank distinctions; general row interference and a singular sparse control in Lean. | Prove the full representation refinement and add injectivity/column conditions before claiming monomial invertibility. No scalar label licenses the stronger claim. |
| `L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY` | `PROVED_LEAN` | `consistent` | Exact supplied-lift matching and Born/direct normalization arrays; generic equality under matching weights and an invalid-lift control in Lean. | Prove arbitrary source lift refinement and supply square-root/complex structure where required. Matching normalized probabilities alone is weaker than raw lift equality. |
| `L1-QM020-THM5-PHASE-AVERAGED-SHADOW` | `PROVED_LEAN` | `statement_narrowed` | Complete3-sector phase-conjugation mean, diagonal map and64 exact scalar readouts, with scalar cross cancellation in Lean. | Supply Haar measure, independence and Hilbert/source refinement. A finite polynomial-moment identity is not a continuum integration construction. |
| `L1-QM020-THM6-P1-SCOPE-FENCE` | `PROVED_LEAN` | `statement_narrowed` | Two exact positive normalized atom maps and additive cell controls, with a concrete disagreement and normalization identity in Lean. | Specify and prove additional frame/affinity/phase hypotheses for uniqueness. Finite cell additivity alone is insufficient. |
| `L1-QM020-THM6-P2-GLEASON` | `IMPORTED_ASSUMPTION` | `consistent` | Exact quadratic-frame resolution, positivity determinant and coefficient reconstruction, plus general quadratic frame identity and known-ansatz reconstruction in Lean. | Discharge full Gleason or POVM uniqueness with its dimension and measure hypotheses. A source named Gleason or a quadratic ansatz is not that theorem. |
| `L1-QM020-THM7-REPRESENTATION-CAPACITY` | `PROVED_LEAN` | `consistent` | Actual rotation/inverse product, conserved norm and sign-dependent probability arrays, with generic norm and interference identities in Lean. | Justify physical linear isometric dynamics, source refinement and the complex Hilbert carrier. Capacity does not supply these hypotheses. |
| `L1-IMP-SQRT-FIELD` | `IMPORTED_ASSUMPTION` | `consistent` | Exact normalized-square classification on the retained rational packets, including zero/negative mass refusal and nonsquare controls. | Prove the rational-square decision refinement and construct any admitted algebraic/real square-root field. No blanket irrationality theorem is inferred from finite search. |
| `L1-IMP-COMPLEX-FIELD` | `CONDITIONAL` | `consistent` | Exact Q(i) multiplication/norm/reciprocal controls, general norm multiplicativity and integer norm5 nonunit control in Lean. | Construct the field instance/refinement and topology/completion required for C; these rational pairs do not admit a complete field. |
| `L1-IMP-U1-PHASES` | `IMPORTED_ASSUMPTION` | `consistent` | Full relative-phase readouts and common-phase invariance, with generic interference identities and the two sign controls in Lean. | Supply a justified circle selector, continuity and source representation bridge. A finite subgroup or one rational unit phase is not U(1) selection. |
| `L1-IMP-HILBERT-INNER-PRODUCT` | `CONDITIONAL` | `consistent` | Exact three Gram pairings/norms and anisotropy controls, with general weighted difference and concrete nonuniqueness in Lean. | Prove positive-definite inner-product instances and source-carrier refinement, then justify any physical selection. The inner product remains admitted structure. |
| `L1-IMP-ORTHOGONAL-ADDITIVITY` | `CONDITIONAL` | `consistent` | Exact projector resolution of identity, quadratic frame totals and quartic basis dependence, with generic orthogonal-frame algebra in Lean. | Prove source/array refinement and the full frame-law uniqueness theorem; a few frame values neither derive orthogonality nor prove Gleason. |
| `L1-IMP-HAAR-INDEPENDENT-PHASES` | `IMPORTED_ASSUMPTION` | `consistent` | Complete exact independent/correlated C4 intensity tables and averages, with general four-phase cancellation and correlated-gap identities in Lean. | Admit/construct Haar probability on U(1)^n and justify independence and continuum integration. C4 cancellation of this polynomial moment is not Haar construction. |
| `L1-IMP-LINEAR-ISOMETRIC-DYNAMICS` | `CONDITIONAL` | `consistent` | Every Boolean map has an exact linear-extension control; only the two bijections have identity Gram matrices. Lean establishes swap preservation and collapse loss. | Refine the native extension to the source carrier and justify linearity/reversibility/isometry of physical dynamics. No permutation envelope derives a complex Hilbert unitary. |
| `L1-WDP-REALIFICATION-J` | `DEFINITION` | `caveat_added` | Complex matrices here are the declared pair model (P, Q) with the hand-written product. R(A) = [[P,-Q],[Q,P]] is an injective ring-linear multiplicative embedding of these into real matrices with J_m R(A) = R(A) J_n and Tr R(A) = 2 Re Tr A, and its image is exactly the real matrices that intertwine the DECLARED J (block coordinate order); the same J^2 = -1 identity holds for other matrices (kernel instance, bounded census), so the choice of J remains an input. | Any selection of J or of the complex field (J is a declaration; a second square root of -I exists in the kernel instance and the census exhibits many more); the identification of the pair model CMat with Mathlib complex matrices (no anchor shows CMat is an associative ring or equals Matrix m n Complex); the block-ordering convention (all real coordinates before all imaginary ones) is part of the definition: the interleaved ordering gives a different J and a different matrix; states sigma = R(rho)/2, positivity as a theorem (native instances only), effects, instruments / Kraus intertwining (Theorem 3), the balanced tensor lift, or any operational or physical reading; infinite dimensions; the claim that every real channel is a realified complex one (it is not). |
| `L1-QM121-LADDER-RUNGS-2-6` | `PROVED_LEAN` | `statement_narrowed` | Complete retained stochastic path tables and matrix-power equality, diagonal action and exact two-phase readout, with finite composition algebra in Lean. | Prove arbitrary-rung/source representation refinements and discharge the admitted carrier, Born uniqueness and continuous/unitary limits. |
| `L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE` | `PROVED_LEAN` | `statement_narrowed` | Over Z[i] with the unnormalized two-sector Hadamard readout: both sector amplitudes nonzero implies the weight pair does not determine the readout; a zero first or zero second sector implies it does. | Complex-Hilbert amplitudes beyond Z[i]; normalized or projective states; more than two sectors; mixes other than the unnormalized 2x2 Hadamard; the embedding of Z[i] into C (non-descent on the Gaussian-lattice fibers gives non-descent on the full complex phase fibers only after that embedding is formalised); the identification of the module readout with the source declarations phaseBlind/mix/readout over Vec GaussInt Bool (H008/H010), which is a modelling identification, not a checked one; any measurement, branch or physical interpretation of the phase fiber. |
| `L1-QM122-CIRCLE-SELECTOR-BOUNDARY` | `PROVED_LEAN` | `statement_narrowed` | Actual cyclic regular-representation shift/square matrices and group-order controls, plus finite modular alternatives in Lean. | Provide genuine topological connectedness, selector uniqueness and source refinement. A Boolean selector pack or finite shadow cannot discharge U(1). |
| `L1-QM122-BORN-PAIRING-NONUNIQUE` | `PROVED_LEAN` | `statement_narrowed` | Exact quadratic/quartic/swapped atom values, honest normalization contracts and Gaussian Hadamard/rotated frame countercontrols; literal unit and frame identities in Lean. | Formalize full source pairing refinement and the additional frame/POVM/Gleason uniqueness hypotheses. These rivals share only their stated weak contracts. |
| `L1-QM122-LEFTOVER-MNC-NOT-RECOVERED` | `PROVED_LEAN` | `statement_narrowed` | All matrix-unit products and noncommutativity are exact, alongside Gaussian unit/nonunit controls; generic matrix-unit scalar multiplication and a commutator control in Lean. | Recover the claimed complex field, circle, Born uniqueness, tensor/CPTP class, continuous time and source carrier maps, or retain them as admitted. A finish table is not completion evidence. |
| `L1-U1-SELECTOR-OTHER-SEGMENT` | `OPEN` (was `PROVED_LEAN`) | `status_lowered` | Inside the unit Gaussian rationals the only phases of finite order are the four elements of mu_4; the rational circle points outside mu_4 are exactly those with 2x not an integer and they have infinite order (kernel instance: (3/5, 4/5)), so a finite phase group inside the Gaussian rationals has order dividing 4, whereas the unit circle over a finite field F_p is a different finite carrier with p -+ 1 elements (native table, not a kernel statement). | Any derivation of C or U(1) from finite carriers, or a proof that no such derivation exists: the node is a pointer to QM_028 / QM_062 owned by another segment and its selection is NOT established here; finite carriers in the sense of finite fields or finite rings (the unit circle over F_p has order p -+ 1, native table only): the theorem is a no-go only for finite subgroups of the unit Gaussian rationals, and the identification of a finite phase carrier with such a subgroup is not argued; larger finite phase groups in cyclotomic extensions (Q(zeta_8), Q(zeta_3), ...) which this result does not treat; completion, continuity, compactness or Haar measure of the circle; that there are infinitely many infinite-order points as a kernel statement (only the instance u345_infinite_order and the native census); the rival split-complex hyperbola x^2 - y^2 = 1 (the H011 flag rival_excluded); the H011 selector pack, whose selector_not_free is rfl on a record with a hand-set Boolean field; any physical reading of phases. |
| `L1-QM020-C10-BRANCH-LOCALIZATION` | `PROVED_LEAN` | `statement_narrowed` | Exact coherence/dephasing arrays and the resulting dynamical non-descent counterexample; literal sign/readout obstruction identities in Lean. | Provide any branching or many-worlds interpretation and its empirical criteria separately; mathematical non-descent neither establishes nor refutes an interpretation. |
| `L1-QM003-C17-COMPOSABLE-FACTORIZATION` | `PROVED_LEAN` | `statement_narrowed` | Exact stochastic composition/action equality and diagonal density presentation, plus scalar matrix multiplication identities and the Hadamard defect in Lean. | Prove source residual-density factorization on its full carrier and channel class. The source diagonal multiplication anchor alone does not prove it. |
| `FQ-CARRIER-CONTRACT-V2` | `DEFINITION` | `consistent` | LCM120 on the actual inventory, literal conductor directedness and star-compatible RingHom theorem signatures, and seven independently checked quotient computations. | Constructed Q^ab colimit, proved Kronecker-Weber, field minimality, or verification of all amplitudes in all targets. |
| `FQ-PRIMDIFF-QUOTIENT-KERNEL` | `PROVED_LEAN` | `consistent` | The supplied ZeroRel is an equivalence and class equality iff ZeroRel is rechecked generally; finite report partitions and their full equality kernels are recomputed on the retained inputs. | Zero, difference laws and report map remain inputs. A quotient construction alone supplies no coefficient field, norm, Hilbert structure or preferred physical readout. |
| `FQ-POSITIVE-WEIGHTS-ADMITTED` | `IMPORTED_ASSUMPTION` | `consistent` | The general two-weight rational convex bound is proved with explicit nonnegativity and score bounds; distinct positive normalized preparations, a signed violation and an unnormalized scaled control are checked. | Derive a preparation measure from native histories with a stated selection principle. Same-carrier examples only show insufficiency of that bare carrier; no stronger impossibility theorem is claimed. |
| `FQ-DECLARED-QUANTUM-INTERFACE` | `IMPORTED_ASSUMPTION` | `consistent` | Three exact rational-real examples on an admitted finite quantum carrier with explicit source and import boundaries. | Derivation, necessity or independence of the quantum interface from primitive difference, or a derived time/dynamics. |
| `FQ-PRIM-TO-QM-SELECTION-OPEN` | `CONDITIONAL` | `consistent` | Identical two-label input carrier and amplitudes admit distinct positive normalized quadratic and quartic rules, with a symmetric agreement control; the 1:2 example is checked in Lean. | Derive a quantum carrier/readout selection principle and its hypotheses. Full continuum matrix/Hilbert/Gleason imports are not discharged by executing a declared packet walk. |
| `FQ-PHASE-FIBER-QUOTIENT` | `PROVED_LEAN` | `caveat_added` | Source phase-equivalence and relative/global-phase kernel statements are rechecked; the full single-coordinate norm25 integer fiber has twelve points while the declared unit orbit has four. | Relate multi-report unit-group orbits to the intended quotient without identifying an orbit with the full norm fiber. A general finite-group action/quotient operad and coherence proof remain open. |
| `FQ-PHASE-BLIND-DESCENT-ZERO-RETAINED` | `PROVED_LEAN` | `statement_narrowed` | Exact integer population descent iff every row is sparse is rechecked generally. The all-ones zero-cancellation control is explicit; native cross-term differences are 4abxy and 4cdxy. | Prove the advertised normalized/projective characterization, with its exact carrier and retained-zero convention, separately; do not promote the stronger-looking target wording from the integer theorem. |
| `FQ-BORN-NORMALIZATION-REDUNDANCY` | `PROVED_LEAN` | `consistent` | The quotient is by positive scaling of weight vectors, with a unique normalized representative; equal weights can still come from different amplitude rays. | Classification of complex amplitude rays, derivation or uniqueness of Born pairing, a formal probability-subtype operad, or publication/erratum completion. |
| `FQ-INTERFERENCE-NONDESCENT` | `PROVED_LEAN` | `consistent` | No function of the original exact populations can reproduce the source mixed readout for all Gaussian-integer vectors. The source Hadamard witness doubles total weight; the rational rotation control separately preserves mass. | Derive or explicitly admit the non-diagonal context, preparation access and any physical interpretation. The raw Hadamard output is not normalized probability. |
| `FQ-SORKIN-READOUT-CLASS-QM208` | `PROVED_LEAN` | `statement_narrowed` | general I3(alpha*t²+beta*t⁴)=12*beta*abc(a+b+c), hence general vanishing iff beta=0. Exact Q(zeta12) control norms (7,±4) give R_AB invariance iff B=0; no full positivity-cone classification is inferred. | Formalize the embedding-weight/basis-coordinate conversion and full rational readout positivity cone. Polynomial restriction and amplitude addition are admitted, and this is not a classification of all readouts. |
| `FQ-POWER-RULE-P2-SELECTION` | `PROVED_LEAN` | `statement_narrowed` | The real power equation (3/5)^p+(4/5)^p=1 iff p=2 is kernel checked. Integer p=1..8 reproduce actual shared-ray context weights; mixed-sign p=1 supplies a retained counterexample to unrestricted Sorkin vanishing. | The power-law family, real exponentiation and the real orthonormal contexts are admitted; formal transport of the concrete context normalization to the Real.rpow equation remains a separate bridge. No unrestricted readout uniqueness or Gleason theorem follows. |
| `FQ-FIVE-IMPORT-PROXY-SEPARATION` | `PROVED_LEAN` | `consistent` | The actual 5x5 proxy separation matrix and intermediate rational matrices are checked independently; Lean computes the same declared predicates and a three-ray counterexample. | Strengthen and justify the physical interfaces before claiming independence of phase/Born/operator/continuous-dynamics imports. Finite proxy separation does not establish that independence. |
| `FQ-GLEASON-D2-RATIONAL-PLANE-OBSTRUCTION` | `PROVED_LEAN` | `consistent` | The source rational-plane binary frame function is generally scale-invariant, additive on nonzero orthogonal frames, and has no quadratic representation; the concrete fitting residual is reproduced exactly. | No extension to dimension at least three, arbitrary real frames or a general Gleason reconstruction is supplied. A complete refined-carrier operad remains open. |
| `FQ-CABELLO-NO-INTEGER-FRAME` | `PROVED_LEAN` | `consistent` | Literal general integer parity, full measured-ray/source scaled checks, and the independently verified normalized M_bad/2 countermodel with a negative quadratic direction. | Arbitrary complex-Hermitian frame systems, general even-parity sufficiency, or a fully instantiated refined-carrier operad. |
| `FQ-CABELLO-FRAME-POLYTOPE-146` | `COMPUTATIONALLY_CHECKED` (was `PROVED_LEAN`) | `status_lowered` | Independently exhaustive exact basis computations and every actual finite matrix witness, with a separate literal integer-list kernel certificate; the general real-polytope completeness bridge remains open. | A formal Lean theorem identifying the entire real polytope vertex set, a general real spectral/PSD transport theorem, or positivity from finite frame additivity. |
| `FQ-GAP-BORN-UNIQUENESS-GLEASON` | `CONDITIONAL` | `consistent` | Concrete weak-contract and quartic-frame countermodels with exact normalized values and literal kernel scope. | general Born/Gleason uniqueness from one rejected rival, or necessity/regularity assumptions inferred from flags. |
| `FQ-BUSCH-EFFECT-FRAME` | `PROVED_LEAN` | `statement_narrowed` | Exact six-effect readouts and reconstruction, plus a finite-probe-versus-PSD counterexample, are native/kernel checked at the stated scalar/coordinate scopes. | Prove full effect positivity, matrix/trace transport, arbitrary Busch hypotheses and the separate real-place/Galois/SOS claims. Finite informational completeness alone is not full positivity or Born uniqueness. |
| `FQ-TENSOR-LU-RIVAL-EXCLUSION` | `PROVED_LEAN` | `statement_narrowed` | Exact tensor/right-Z and dump/right-Z arrays plus the genuine report-action non-descent witness are native/kernel checked. | Transport to the original abstract bilinear Kronecker interface, full local-unitary group and physical tensor/basis/inner-product admission. The rival counterexample alone does not derive the tensor product. |
| `FQ-GAP-TENSOR-UNIQUENESS` | `CONDITIONAL` | `consistent` | On the admitted 2x2 rational coefficient host every simple tensor has zero coefficient determinant; [[1,0],[0,1]] has determinant one and is not simple. Native norm multiplication is checked on retained inputs. | Formalize state/effect cones, covariance requirements, their min/max comparison and any uniqueness theorem; general tensor selection remains an import. |
| `FQ-CPTP-CLASS-DEFINITION` | `DEFINITION` | `consistent` | Full depolarizing Choi arrays, eigenvector actions, rank controls and TP partial trace are exact; eigenvalue nonnegativity iff -1/3<=p<=1 and trace2 are kernel checked. | Prove the full Choi-PSD/Kraus/Stinespring bridge, environment metric and any actual field/conductor necessity. A class definition and data flags do not derive the channel class. |
| `FQ-TRACE-NORM-FROM-CPTP-MONOTONICITY` | `PROVED_LEAN` | `statement_narrowed` | Exact squared trace norms for the stated 2x2 trace-zero Hermitian family contract under the admitted diagonal pinching; the scalar inequality and positive rescaling implication are kernel checked. | Prove the norm-family uniqueness theorem over all dimensions and the full CPTP class. Diagonal pinching and a scale family are necessary controls, not that theorem. |
| `FQ-TRACE-ZERO-DUALITY-K23` | `COMPUTATIONALLY_CHECKED` (was `PROVED_LEAN`) | `status_lowered` | Actual diagonal K23 primal/dual arrays have equal objectives6 and9/2 at unit defect scale, with correct polar balls and divergence. Native certificates bind each edge and potential. Lean checks scalar-shift invariance under a trace-zero hypothesis and the exact objective arithmetic. | Transport the explicit matrix/graph certificates to a full Lean matrix-norm duality/LP theorem. No scalar4/12 substitution, no general strong-duality theorem, and no publication correction is inferred from these local certificates. |
| `FQ-BELL-CLASSICAL-JOINT-EXTENSION` | `PROVED_LEAN` | `statement_narrowed` | Integer separator theorem and finite exact native certificates; full formal rational Fine converse remains open. | The full formal rational Fine converse (common positive joint law versus the CHSH family over the rationals) remains open. |
| `FQ-BELL-RATIONAL-VIOLATION-14-5` | `PROVED_LEAN` | `statement_narrowed` | Five literal kernel anchors for the fixed admitted quantum matrices and arbitrary Nat-weighted assignment obstruction, plus three independently checked exact native cases and actual mutation rejections. | Deriving Born/tensor structure, physical locality/setting independence, a complete formal arbitrary-rational-table transport theorem, or general probability-subtype operad coherence. |
| `FQ-TSIRELSON-SOS-Q-SQRT2` | `PROVED_LEAN` | `statement_narrowed` | Two exact Q(sqrt2) SOS matrix certificates and Bell-density expectation2sqrt2 are reproduced independently. general rational four-coordinate scaled SOS inequalities and attainment ratio are kernel checked for this fixed operator. | Formalize the concrete Q(sqrt2)-matrix to real quadratic-form transport before claiming a full Lean operator certificate; arbitrary observables, tensor selection and quantum probability are not derived. |
| `FQ-CONTEXTUALITY-CECH-F2` | `PROVED_LEAN` | `statement_narrowed` | Two explicit degree-two parity covers and a genuine global-section control, exact matrices/ranks and literal source kernel parity/differential signatures. | Conflation of incidence rank with overlap rank, general sheaf equivalence, a kernel proof of the native rank outputs, or physical reconstruction. |
| `FQ-WEYL-FINITE-SCHRODINGER-IRREDUCIBILITY` | `PROVED_LEAN` | `statement_narrowed` | Exact d=3 Weyl basis reconstruction and commutator controls, plus the generic conditional scalar-commutant theorem and literal cubic-root algebra. | Transport the array model to field/matrix semantics and prove representation irreducibility for all admitted odd primes. Primitive-root existence, seed selection and infinite-dimensional results are not derived. |
| `FQ-COMMUTATOR-TRACE-OBSTRUCTION` | `PROVED_LEAN` | `consistent` | The exact finite-dimensional scalar commutator obstruction is kernel checked for arbitrary n>0 over Q. | Transport to other coefficient fields and domain/unbounded-operator settings with their actual hypotheses. The supplied finite matrix carrier is an assumption. |
| `FQ-U1-TRANSPORT-N-TORSION` | `PROVED_LEAN` | `statement_narrowed` | Actual finite graph gauge normal forms, relative path phase and N² orbit-invariant counts are exact; cycle identities over ZMod n and pair-cardinality arithmetic are kernel checked. | Prove full graph gauge-orbit classification and the cyclotomic mu_N embedding/order hypotheses for arbitrary graphs/N; no continuous circle or topological connectedness is derived. |
| `FQ-GAP-U1-CIRCLE` | `CONDITIONAL` | `consistent` | The rational Cayley parametrization satisfies the unit-circle equation on retained points, with exact inverse t=y/(x+1), and a general cleared identity. The square-root equations force a^2=4/5; bounded powers are computed exactly. | Prove 4/5 is not a rational square, full power-map injectivity, and the additive-Q homomorphism obstruction without bounded-search substitution; compact continuous U(1) remains imported. |
| `FQ-DISCRETE-DYNAMICS-DICHOTOMY` | `PROVED_LEAN` | `statement_narrowed` | An all-natural-index integer numerator is nonzero in Lean; actual normalized retained powers have unit mass and never equal identity, unlike periodic controls. | Prove the recurrence-to-normalized-matrix bridge for all powers, then formulate any closure/topology or generator selection claim. No full dynamics dichotomy is inferred. |
| `FQ-DISCRETE-TIME-STONE-AMBIGUITY` | `PROVED_LEAN` | `statement_narrowed` | The report-map obstruction and two distinct scaled Gaussian roots are kernel checked; native enumeration and normalized unitarity are replayed. | Construct logarithms, an actual continuous one-parameter group, topology and a generator selection rule. Tags do not supply analytic branches. |
| `FQ-GAP-STONE-CONTINUOUS-TIME` | `CONDITIONAL` | `consistent` | All-integer modulo-four aliasing is kernel checked; exact modulo-eight controls distinguish declared half-step tags. | Supply topology, strong continuity, actual exponentials and generator domains before invoking Stone; finite tags do not prove existence. |
| `FQ-GAP-CONTINUUM-HILBERT-LIFT` | `CONDITIONAL` | `consistent` | 2 has no Gaussian-integer inverse because its real equation 2a=1 has no integer solution; the stated matrix has characteristic polynomial l^2-l-1 and discriminant identity 4p(l)+5=(2l-1)^2. | Construct an actual completion with specified topology, carrier and embedding; prove any claimed rational/Gaussian spectral exit separately. No impossibility of completion follows from this obstruction. |
| `FQ-EVERETT-RATIONAL-SECTOR-BOUNDARY` | `PROVED_LEAN` | `statement_narrowed` | general rational-pair fine graining and full rational-root exclusion are kernel checked; retained multi-outcome multiplicities and quadratic-field root coefficients are exact. | Prove arbitrary finite-vector fine-graining transport and that the declared quadratic-field coefficients realize the intended physical readout. Counting is an admitted interpretation. |
| `FQ-GAP-REAL-EMBEDDING-CHOICE` | `COMPUTATIONALLY_CHECKED` (was `PROVED_LEAN`) | `status_lowered` | Exact quadratic-field Gram/conjugate coefficients, a mixed signature control and real-root inequalities are checked; the fake 9/4 root is explicitly rejected. | Formalize the coefficient-to-real embedding homomorphisms, full Gram PSD and cyclotomic fixed-field degree identification. A declared evaluation is not that embedding. |
| `FQ-ENTROPY-DICHOTOMY-BAKER` | `PROVED_LEAN` | `consistent` | Literal general-dimension source entropy signatures with explicit Baker hypothesis, plus five exact rational series computations with an explicit analytic remainder argument. | An unconditional proof of Baker or transcendence from a native flag, base-two entropy claims, or a kernel-verified finite-tail array transport. |
| `FQ-GAP-CUSTODY-AND-RECEIPTS` | `OPEN` | `consistent` | Every retained available source is bound to actual bytes; unavailable or changed historical pins remain explicit. Fresh named Lean reports cover only the declarations listed in this run, not an H000-H053 campaign. | Resolve the original claim-row discrepancies, missing-library maps, publication/provenance corrections and full original axiom/build receipts individually. This scoped inventory does not discharge the historical custody register. |
| `FQ-GAP-CORPUS-REWRITE` | `OPEN` | `consistent` | The captured source scope is inventoried with exact byte/newline/literal counts and cryptographic source custody; a proper subset cannot discharge a missing obligation. | Create a claim-by-claim whole-corpus rewrite/retirement ledger with original exit contracts and independently checked content; captured filenames and constant flags cannot supply it. |
| `FQ-GAP-C500-ORIGINAL-TARGETS` | `OPEN` | `consistent` | The examined records do not discharge the original contracts; their scoped labels and partial evidence are retained without promotion. | Original campaign completion, independent rerun of every cited finite computation, historical freeze certification, or proof that any open target is false. |
| `FQ-IMPL-F64-GATING` | `DEFINITION` | `consistent` | Exact integer differences and bounded binary64 diagnostic rounding collisions are retained; distinctness and the literal rounding-model collision are kernel checked. | Audit the full tracked Rust policy/ledger and prove an IEEE754-model transport before making repository-wide gating claims. A diagnostic collision or declared zero authority tag is not an implemented global enforcement theorem. |
| `FQ-IMPL-WDP-AMPLITUDE-BRIDGE` | `PROVED_LEAN` | `statement_narrowed` | Exact bounded phase/holonomy/readout controls and a general positive-power mod5 residue induction are retained with literal gauge/norm kernel identities. | Formalize the Gaussian numerator/denominator transport and the rational-additive-group obstruction to a homomorphism sending1 to this u. Do not infer a preferred readout or a general phase-selection theorem. |
| `FQ-IMPL-REALIFICATION-ADAPTER` | `PROVED_LEAN` | `statement_narrowed` | Actual scalar realification products, multiplication quotient, balancing kernel and normalization factor are exact; literal algebraic product/balancing identities are kernel checked. | Prove the full operator/density adapter, balanced tensor metric and positivity/admission transport for arbitrary finite matrices. No derivation or selection of the complex structure is supplied. |
| `FQ-IMPL-PAIRING-AUDIT` | `COMPUTATIONALLY_CHECKED` (was `PROVED_LEAN`) | `status_lowered` | Actual state/projector arrays and pairing differences plus a negative nonlinear extension are exact; off-diagonal and polynomial-negative identities are kernel checked. | Run the full source registry and its complete positivity/normalization/composite contracts, then justify a uniqueness theorem if available. This small packet neither selects Born nor makes every nonlinear alternative physically admissible. |
| `FQ-QM207-231-FINITE-MAP-CONTROLS` | `PROVED_LEAN` | `statement_narrowed` | The selected rational energy polynomial, exact minimizer and virial identity are kernel/native checked for all rational z where stated. | Derive the variational functional from the actual Hamiltonian/ansatz and audit the remaining finite-map rows and their residual imports. No batch closure of all25 controls, QED/QCD/gravity or physical spectrum is claimed. |
| `GP-IMPORT-COMPLEX-FIELD` | `IMPORTED_ASSUMPTION` | `consistent` | Exact reciprocals/units and a no-integer-root obstruction control; generally no integer inverse to1+i and no integer square2 in Lean. | Complete complex field, spectral theorem and completeness remain imports. The computed finite polynomial samples do not prove a full spectral theorem. |
| `GP-IMPORT-CIRCLE-U1` | `IMPORTED_ASSUMPTION` | `consistent` | Complete C2/C3/C4 group tables, exponent-two controls and sign-interference values, plus exact cyclic controls in Lean. | A circle group, topology and continuous one-parameter action remain extra hypotheses. Finite alternatives do not select U(1). |
| `GP-IMPORT-GLEASON` | `IMPORTED_ASSUMPTION` | `consistent` | Exact unit-contract rivals and frame quartic obstruction arrays, with general quadratic/quartic frame identities in Lean. | Prove uniqueness only after admitting the full intended Gleason/frame hypotheses and dimension. These counterexamples do not refute Gleason under its hypotheses. |
| `GP-IMPORT-TENSOR-PRODUCT` | `IMPORTED_ASSUMPTION` | `consistent` | Exact tensor/dumpRight and norm-multiplicativity arrays, with generic bilinearity and a basis-collision control in Lean. | Refine the complete CombiningEmbed/Kronecker uniqueness theorem and justify the physical composition rule; weak tag interfaces do not select a Hilbert tensor product. |
| `GP-IMPORT-CPTP-CLASS` | `IMPORTED_ASSUMPTION` | `consistent` | Four actual reversible dilation maps/inverses and exact reset-channel Choi/TP/action arrays, with generic inverse and reset trace identities in Lean. | Prove the native-array-to-channel/dilation refinement and classify arbitrary CPTP maps under admitted complex Hilbert structure. The ancilla convention is essential. |
| `GP-IMPORT-CONTINUOUS-TIME` | `IMPORTED_ASSUMPTION` | `consistent` | Complete Boolean square-root obstruction and both exact complex unitary square roots of toggle; generic projector-square algebra and Boolean enumeration in Lean. | Supply topology, continuous time and the one-parameter group; invoke Stone only under its hypotheses. Square roots alone do not define continuous dynamics. |
| `GP-IMPORT-CONTINUUM-HILBERT` | `IMPORTED_ASSUMPTION` | `caveat_added` | Exact truncation coordinates, norm, positive tail and successive difference controls; general finite recurrence identity and positivity interface in Lean. | Construct and verify the topology, Cauchy completion and infinite-dimensional Hilbert carrier. No finite truncation settles those imports. |
| `GP-GAP-EXACT-DUALITY` | `COMPUTATIONALLY_CHECKED` (was `PROVED_LEAN`) | `status_lowered` | A complete nine-witness rational l1 dual control has exact zero gap; Lean establishes the literal triangle/positive-sign identities. | Construct the actual QM080 primal/dual quotient maps, hypotheses and attainment proof. This two-coordinate support function is not the general quotient theorem or a revalidation of the source K2,3 model. |
| `GP-FIN-GAUSS-MATRIX-ALGEBRA` | `PROVED_LEAN` | `consistent` | Finite Gauss-integer matrix recovery, uniqueness, composition and adjoint laws are rechecked generally on the source finite enumeration interface; exact native 2x2 examples independently verify the concrete laws. | Gaussian coefficients, linearity, finite enumeration and pairing remain assumptions. M_n(Z[i]) supplies neither M_n(C), spectral completeness, CPTP, unique tensor nor continuous time. |
| `GP-DROP-ONE-CENSUS` | `PROVED_LEAN` | `consistent` | The actual source-declared eight-entry import census has no duplicates and partitions into three lost labels and five open labels. Counts and partition are recomputed without promoting labels to necessity theorems. | Necessity of the five open extras requires mathematical constructions or countermodels. Source labels and this census alone cannot supply those arguments. |
| `DS-QM030-GRADED-PATHSUM` | `COMPUTATIONALLY_CHECKED` (was `PROVED_LEAN`) | `status_lowered` | Exact two-state path enumeration, matrix powers and graded composition agree on retained lengths, including zero. | Prove the full path-enumeration/matrix-power bridge and transport to a selected physical dynamics; a weighted graph and chosen grading are inputs. |
| `DS-QM030-UNGRADED-OVERCOUNT` | `COMPUTATIONALLY_CHECKED` (was `PROVED_LEAN`) | `status_lowered` | Actual acyclic arrays give Z20=d+ab and (Z²)20=2d+3ab, with pure and mixed-length controls. | Grading is one sufficient bookkeeping choice. Do not claim that every possible ungraded formulation is not possible or that the old arithmetic identity was a path-count theorem. |
| `DS-QM030-TRANSFER-OPERATOR-SHADOW` | `COMPUTATIONALLY_CHECKED` (was `PROVED_LEAN`) | `status_lowered` | All coefficients of AB, (AB)v, A(Bv), fA, f(Av), and (fA)v agree on exact retained inputs. | Formalize the full arbitrary finite action/dual sum transport; the state carrier, linearity and coefficients are supplied. |
| `DS-CONTINUOUS-TIME-EXP-GENERATOR` | `IMPORTED_ASSUMPTION` | `consistent` | No Boolean report-map half-step exists, while two distinct normalized Q(i) amplitude half-steps square to swap and are unitary. The source scaled-root and report obstruction proofs are rechecked. | Construct a continuous-time group, analytic logarithms, generator selection, convergence and any continuum measure with their actual hypotheses. Discrete roots or injective branch tags do not supply those interfaces. |
| `DS-QM032-FINITE-FEYNMAN-SHADOW` | `COMPUTATIONALLY_CHECKED` (was `PROVED_LEAN`) | `status_lowered` | Two-path interference has residual 2pq, including cancellation and rational controls. | Supply action weights, refinement, measure and convergence before invoking a Feynman continuum formula. |
| `DS-QM032-CONTINUUM-LIMIT-CONDITIONAL` | `COMPUTATIONALLY_CHECKED` (was `PROVED_LEAN`) | `status_lowered` | Affine restriction maps compose and the singleton states are compatible; retained ambient separations show that this bookkeeping alone supplies no convergence bound. | Specify compatible approximation spaces, a common embedding/topology, quantitative error and a real convergence proof before any continuum limit. This example does not refute a correctly hypothesized convergence theorem. |
| `DS-QM033-SCHRODINGER-DISCRETE-COCHAIN` | `COMPUTATIONALLY_CHECKED` (was `PROVED_LEAN`) | `status_lowered` | Full Gaussian Hψ and derivative coordinates reproduce zero instantaneous mass rate and the nonzero exact Euler drift formula. | Derive H and its units/interface; construct an exact propagator and prove the formal matrix-to-rate transport. No differential equation solution or continuum limit is provided. |
| `DS-QM033-064-074-083-QHELD-CONTINUUM` | `IMPORTED_ASSUMPTION` | `consistent` | Exact phase-blind data agree while the declared mixed readouts differ by 4ab, with a zero-amplitude control. | Choose and justify an amplitude lift, admissible mixing operations and any continuum closure. Fixed presentation data do not select these. |
| `DS-QM034-035-050-051-095-RESERVED-STUBS` | `CONDITIONAL` | `consistent` | Declared Cayley matrices are orthogonal while Euler expands norm at nonzero t; concrete two-generator Clifford identities are recomputed. | Supply spinor/Dirac carrier, Hamiltonian, dynamics and formal matrix bridges before closing the reserved paper stubs. |
| `DS-QM040-GAUSSINT-LAMBDA-COMMUTATOR-WITNESS` | `COMPUTATIONALLY_CHECKED` (was `PROVED_LEAN`) | `status_lowered` | All cyclic identities [Li,Lj]=2ir Lk hold entrywise at retained scales, and declared coordinate projectors are idempotent. | Formalize every Gaussian matrix entry and projector relation in Lean, then transport to the proposed Lambda mechanism. No dynamics is selected by these witnesses. |
| `DS-QM041-HEISENBERG-PICTURE-FINITE` | `COMPUTATIONALLY_CHECKED` (was `PROVED_LEAN`) | `status_lowered` | The two exact expectation pairings agree on the declared two-state carrier. | Transport the expanded quadratic identity to full Gaussian matrices, and supply any selected time law, Hamiltonian and physical readout. |
| `DS-QM043-DECOHERENCE-FUNCTIONAL-IMPORT` | `IMPORTED_ASSUMPTION` | `consistent` | Actual class-operator Gram tables are positive semidefinite, and exact controls separate class completeness, Kraus completeness, diagonal trace and global weight. | Justify the class-operator family, density and physical history normalization, and formalize the native Gram-table bridge. No general decoherence functional is derived. |
| `DS-QM043-OFFDIAG-GLOBAL-WEIGHT-IDENTITY` | `PROVED_LEAN` | `consistent` | Exact global and diagonal weights differ by twice the off-diagonal coefficient, with a sign-flip control. | Prove the actual phase quotient/H1 descent conditions and state the permitted history and readout maps. |
| `DS-QM021-IDEMPOTENT-CONDITIONING` | `COMPUTATIONALLY_CHECKED` (was `PROVED_LEAN`) | `status_lowered` | Exact sector normalization, support collapse and repeated-conditioning idempotence are reproduced on retained finite tables. | Formalize the masked support/restriction bridge and justify any physical sector rule. Classical normalization is not a derived projection postulate or solution to measurement. |
| `DS-QM030-PROJECTION-POSTULATE-AND-BORN-PAIRING-IMPORT` | `IMPORTED_ASSUMPTION` | `consistent` | Scalar idempotence holds exactly at 0 and 1 in Lean; retained diagonal effect controls and two different normalized pairings are exact. | Derive or explicitly admit the spectral/projector structure and the physical observer pairing. The bare finite carrier does not select the Born rule or an actual event. |
| `DS-QM060-SUPERPOSITION-QUOTIENT-FIBER` | `PROVED_LEAN` | `consistent` | Gaussian population invariance and the two-path cross-term identity are checked on exact records and literal rational Lean identities. | Construct and justify any full U(1) lift, quotient and physical readout; finite Gaussian controls alone do not select that carrier. |
| `DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE` | `PROVED_LEAN` | `consistent` | The cross term is general over rational coordinates in Lean, and no function of the two squared coordinate weights produces every coherent squared sum. | Transport to a chosen complex amplitude carrier and physical measurement rule. Non-descent relative to an admitted quadratic readout is not a derivation of interference from bare populations. |
| `DS-QM061-BUILDABILITY-SET-S` | `COMPUTATIONALLY_CHECKED` (was `PROVED_LEAN`) | `status_lowered` | The declared rate inequality and all four Boolean conjunction controls are exact; the alias and Boolean characterization are kernel checked. | Provide measured or derived rate/floor/reachability/advantage evidence and a justified device-to-fields bridge before claiming a buildable useful quantum computer. |
| `DS-QM062-U1-SELECTOR-LAYERS` | `COMPUTATIONALLY_CHECKED` (was `PROVED_LEAN`) | `status_lowered` | Actual rational matrix products, Gaussian coefficients and norm-multiplicativity/conjugation polynomials are checked. | Prove the full ring homomorphism/embedding and the R/C/H selection hypotheses, continuity and global uniqueness separately; algebraic controls do not exclude H by themselves. |
| `DS-QM062-U1-RESIDUES-IMPORT` | `IMPORTED_ASSUMPTION` | `consistent` | Actual J powers show order-four periodicity on retained indices; modulo-four aliasing is kernel checked for every natural k. | Supply continuity/topology, local tomography and a real exclusion/selection theorem if a full U(1) carrier is wanted. No finite-order exclusion follows from unbounded multiples. |
| `DS-QM063-HOLONOMY-COHERENT-INTENSITY` | `PROVED_LEAN` | `statement_narrowed` | Relative Gaussian holonomy and two-path intensity are invariant under the retained common unit phases; the rational unit-phase conditional is general in Lean. | Prove the full graph connection/tree gauge-trivialization and matrix-valued holonomy transports; no SU(2) trace bound or higher-form result is claimed. |
| `DS-QM064-074-083-ANNEX-REDIRECT-ROWS` | `PROVED_LEAN` | `statement_narrowed` | Triangle identities, retained stochastic outputs and contextual marginal residuals are recomputed exactly; generic finite rational contraction is kernel checked. | Supply graph-to-phase, channel-to-kernel and physical composition/causality transports. The three control families do not by packaging close the annex interpretations. |
| `DS-QM070-PRODUCT-NONFACTORIZATION` | `PROVED_LEAN` | `statement_narrowed` | Actual marginals, normalized product reconstruction, signed residuals and Phi are checked; residual and zero-defect polynomials are general over Q in Lean. | Formalize arbitrary finite table reconstruction and justify any tensor/basis/quantum coherence lift; a product defect of diagonals does not test entanglement. |
| `DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS` | `PROVED_LEAN` | `consistent` | Exact product-density and Bell-fidelity controls plus a general rational normalized-product gap and finite convex separator soundness are kernel/native checked. | Supply complex/tensor physical imports, arbitrary mixed-state separability and full matrix-functional transport. Soundness for a declared family is not completeness of witnesses. |
| `DS-QM072-QUBIT-SUPERPOSITION-OBSTRUCTED` | `PROVED_LEAN` | `statement_narrowed` | Exact phase-reversed pure densities and their dephased mixture share populations but differ under an admitted coherent readout; scalar readout/purity differences are kernel checked. | Construct or admit the qubit/coherence carrier, transformations and measurement rule; no generalized Bloch-contraction conjecture is accepted. |
| `DS-QM073-FINITE-CHSH-AND-PR-BOX` | `PROVED_LEAN` | `statement_narrowed` | Every deterministic row, weighted correlation and PR entry is exact; deterministic CHSH and generic convex absolute bound are kernel checked. | Formalize the concrete table-to-general convex theorem transport and any full Fine converse or quantum realization. Product/separable for a bare classical table has a different meaning from quantum separability. |
| `DS-QM073-BELL-THEOREM-OBSTRUCTED` | `PROVED_LEAN` | `statement_narrowed` | Actual contextual arrays and all marginal residuals are computed; 4v readout and the v=1 algebraic countermodel are kernel checked. | Admit or derive the global-joint, quantum operator/tensor, measurement and source assumptions separately before claiming a Bell/quantum/Tsirelson derivation. |
| `DS-QM074-NO-SIGNALING-MARGINAL` | `PROVED_LEAN` | `statement_narrowed` | Exact contextual marginals distinguish nonsignaling correlated tables from the signaling control; scalar PR-family marginal and nonproduct controls are kernel checked. | Prove full admitted-composition/channel-to-table transport and justify physical subsystem/setting independence; no causality law is derived. |
| `DS-QM080-IMPORT-FREE-TRACE-NORM-CORE` | `PROVED_LEAN` | `statement_narrowed` | Two-coordinate quotient shift invariance, dual upper bound and existence of a bounded attaining rational witness are kernel checked with exact controls. | Prove arbitrary finite-dimensional normed-space duality and the matrix/spectral lift separately. This coordinate result is not the original general theorem. |
| `DS-QM080-081-TRACE-NORM-CONDITIONAL-SELECTION` | `PROVED_LEAN` | `statement_narrowed` | Exact diagonal half-trace/total-variation identity is kernel checked; rescaling controls retain normalization ambiguity. | Supply spectral/matrix interface, unitary invariance, CPTP compatibility, edge additivity and the actual uniqueness proof before promoting to full quantum half trace norm. |
| `DS-QM081-CPTP-MONOTONE-NOT-SELECTING` | `PROVED_LEAN` | `consistent` | Exact stochastic contraction controls, nonnegative rescaling and distinct positive-scale values are kernel/native checked. | Admit a full channel class and prove a full quantum monotonicity theorem or a nonproportional counterexample if that broader selection question is pursued. |
| `DS-QM081-STOCHASTIC-L1-CONTRACTION` | `PROVED_LEAN` | `consistent` | Generic finite rational column-stochastic L1 contraction is kernel checked; retained three-state outputs and triangle budgets are exact. | Transport the array implementation to the formal finite sums and any supplied quantum/CPTP interface. Classical contraction does not derive a quantum carrier. |
| `DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL` | `PROVED_LEAN` | `statement_narrowed` | Exact Kraus completeness, channel outputs, stochastic kernel and same-diagonal distinct-output controls are retained; scalar Cayley and population conservation are kernel checked. | Formalize all matrix/Kraus/tensor positivity transports and physical channel admission. Basis-relative stochastic shadows do not select a unique quantum channel. |
| `DS-CPTP-COMPLETE-POSITIVITY-IMPORT` | `IMPORTED_ASSUMPTION` | `consistent` | A genuine Bell-input partial-transpose negative witness is computed entrywise and its positive-input and negative-output scalar forms are kernel checked. | Prove full transpose positivity, the native tensor-index transport and a full CP/Stinespring theorem. This counterexample does not derive the physical tensor product or channel law. |
| `DS-QM090-092-AUTHORITY-FIREWALL` | `COMPUTATIONALLY_CHECKED` (was `PROVED_LEAN`) | `status_lowered` | Toy zero-defect gate arithmetic and logical nonimplication are kernel checked; every run retains AuthorityEffect None. | Define a trusted receipt-validation/packet policy before any real authorization; no general no-constructor theorem, publication terminal or physical claim is proved. |
| `DS-QM090-093-O022-REGISTRY-RELATIVE-MINIMALITY` | `PROVED_LEAN` | `consistent` | The frozen row conjunction and failure of rank minimality to transfer to an expanded registry are exact; the limited list/rank and Boolean statements are kernel checked. | Establish semantic capability evidence and a justified interface ordering before any physical minimality theorem. No all-registry or unique-QM minimality is proved. |
| `DS-QM090-093-QM-UNIQUENESS-TIER3` | `PROVED_LEAN` | `statement_narrowed` | Actual context tables, global-assignment exclusion and spectator marginal recovery are exact; the odd-cycle and rational recovery statements are kernel checked. | Give the full theory/equivalence notion and exclude competing packet theories before Tier-3 complex-Hilbert uniqueness. No ontology or arbitrary non-QM theory classification is asserted. |
| `DS-QM093-SURVIVAL-THEOREM` | `COMPUTATIONALLY_CHECKED` (was `PROVED_LEAN`) | `status_lowered` | The declared three-field antecedent truth table and missing-seal refusal are kernel/native checked; the real survival antecedent remains undischarged. | Obtain and validate the imported interface, replay evidence and sealed external terminalizer. A true input flag is not that evidence and does not terminalize anything. |
| `DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO` | `PROVED_LEAN` | `statement_narrowed` | Full conjugated arrays, composition control and trace-pairing/coboundary identities are checked exactly with a general rational conditional kernel identity. | Formalize the array-to-matrix interpretation, full complex unitary packet and contextual gluing/physical readout. Gauge invariance alone is not selection. |
| `DS-QM094-EVERETT-RELATIVE-STATE-CONTACT` | `PROVED_LEAN` | `statement_narrowed` | Actual relative-state density, partial trace and expectation controls are exact; the scalar orthogonality and absolute-bound identities are kernel checked. | Prove the full tensor/partial-trace coordinate bridge and justify a physical record basis/probability rule. No branch selection or many-worlds ontology follows. |
| `DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE` | `PROVED_LEAN` | `statement_narrowed` | Exact finite backlog trajectories and declared gate controls are checked; lambda<=mu implies non-increasing natural backlog in Lean. | Supply actual workload/noise/overhead assumptions, scaled repair rates and a p_pair convergence argument or the correctly cited threshold theorem. This toy queue is not a threshold theorem. |
| `DS-QM102-SYNDROME-CAPACITY-BOUND` | `PROVED_LEAN` | `statement_narrowed` | Complete retained repetition-code error tables and zero-syndrome logical controls are exact; the distance arithmetic and three-bit correction statement are kernel checked. | Prove the arbitrary code/homology distance and decoder transport under the actual error model. A guaranteed-correctable lower bound is not a general upper-bound theorem. |
| `DS-QM103-SHOW-THE-PACKET-PROTOCOL` | `DEFINITION` | `consistent` | Exact field-completeness/scale/refusal controls are checked; presence of fields is not logical validation of their contents. | Provide substantive verified packet contents and meaningful scale/noise/throughput/leakage/overhead evidence. Eligibility for audit is not a physical or authority terminal. |
| `DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS` | `PROVED_LEAN` | `statement_narrowed` | Q8 group operations, pure-gauge loops and noncommuting plaquette controls are native/kernel checked on the declared eight-element group. | Supply continuum manifold/metric/connection, SU(2) representations, measure, physical scales and Hamiltonian/Einstein dynamics before any quantum-gravity interpretation. |
| `DS-QM120-MERMIN-PERES-F2-OBSTRUCTION` | `PROVED_LEAN` | `statement_narrowed` | Actual subset solution counts and five-context witnesses are exact; global signed-parity obstruction and each explicit dropped-context witness are kernel checked. | Transport the enumeration to a fully formal incidence/cochain object and any physical observable realization. This finite parity packet does not derive Hilbert space or quantum mechanics. |
| `DS-QM206-BOUNDARY-SYNTHESIS` | `COMPUTATIONALLY_CHECKED` (was `PROVED_LEAN`) | `status_lowered` | Actual C4 image/kernel and all composition controls are exact; additive homomorphism, collision and missed-arrow statements are kernel checked. | Define the intended GTOC/Hilb categories and actual descent functor, prove its properties and discharge the QM205 pointer-basis stub. The toy map is not that functor. |
| `DS-QM207-211-FIVE-IMPORT-CASCADE` | `COMPUTATIONALLY_CHECKED` (was `PROVED_LEAN`) | `status_lowered` | Exact phase/readout and noncommutative matrix controls are retained; cross-term and quartic-gap polynomials are general rational kernel identities. | Prove each correctly specified physical necessity claim and supply phase, quadratic pairing, operator algebra, Born uniqueness and continuous dynamics. These controls do not derive or establish independence of all five imports. |
| `DS-QM204-BORN-UNIQUENESS-IMPORT-BOUNDARY` | `IMPORTED_ASSUMPTION` | `consistent` | Exact normalized alternative profiles, quadratic rotation identity and a genuine Born/quartic divergence are kernel/native checked on the declared rational carrier. | Supply frame-function/effect/continuity/dimension hypotheses and a uniqueness theorem. Bare normalization does not derive Born pairing. |
| `DS-QM212-MAJORANA-PROBLEM` | `PROVED_LEAN` | `consistent` | Full gamma/parity/braid matrices and the general rational Clifford/scaled-braid identities are kernel/native checked. | Supply physical mode, braid dynamics, device/noise and tensor interpretation. Canonical normalization and experimental realization are not inferred from the algebra. |
| `IMPL-FSP-SWITCHING-NORMAL-FORM-NF002` | `PROVED_LEAN` | `consistent` | All edge signings and vertex-switching orbits for the four declared graphs are exact; cycle XOR invariance and2^b Boolean-function cardinality are kernel checked. | Prove the general graph/forest refinement and freshly compile all source NF002 declarations before claiming its full core-only/no-Classical.choice theorem suite. This finite graph stage is not that suite. |
| `IMPL-THYMUS-SCREENING-SOUNDNESS` | `PROVED_LEAN` | `statement_narrowed` | Complete finite panel/predicate controls and mismatch witnesses are exact; zero in-panel false positives under the actual screened predicate is kernel checked. | Bind an actual production detector, executed code and authenticated self-panel to these predicates, and state any out-of-panel assumptions. No generalization beyond the sealed panel or physical immune-system theorem is claimed. |
| `IMPL-LGGR-FINITE-RESULTS-LEAN` | `PROVED_LEAN` | `caveat_added` | Actual bounded cycle sections, gate fields, triangle primal mixture and matching2/3 dual controls are exact; the conditional source-model gate equivalence and attainment arithmetic are kernel checked. | Prove the external Rust gate/representation and arbitrary LP/cycle refinements. Proposition II-open and physical-selection claims remain open; a census/route partition is not this proof. |

<!-- END GENERATED dag-results-audit (papers/core/tools/build_results_audit_table.py) -->

#### 13.8.13 Results added after the 177-node DAG (pull requests #113 to #133)

The items below describe what each merged piece of work added, in the scope its DAG node supports. Each item ends with the DAG status, and a non-claim where one is needed. None of them changes the seven boundaries of §5 from "open" to "closed".

1. **Effect-additive Born trace representation (#113 and the code-review repairs of #120; run `20261020T205000Z_effect_valuation_lean`, Gaussian case `20261020T224000Z_gaussian_hermitian_carrier`).** On the $n\times n$ rational matrices, ordered by the quadratic-form preorder with the identity as order unit, every effect-additive, positive, normalized valuation has the form $E\mapsto\operatorname{tr}(\rho E)$ for a unique matrix $\rho$; that $\rho$ is symmetric, positive semidefinite on rational vectors and of trace one, and conversely such a $\rho$ defines a valuation (`BornFable.MatrixCarrier.born_representation`, `density_is_state`, `born_rule`, `state_valuation_correspondence` in `lean4/BornTraceRepresentation.lean`). The same statement holds on Gaussian-rational Hermitian matrices with the real part of the trace (`lean4/BornHermitianTraceRepresentation.lean`). A parity function on the rational rays of $S^2$ sums to one on every orthogonal triple but is not a quadratic form (`parity_frame_function`, `parity_not_quadratic` in `lean4/BornRationalSphereObstruction.lean`), so frame additivity on rational rays alone does not force a quadratic form. Exact Python and Rust twins accompany the modules (`code/python/src/qm/born_effect_valuation.py`, `code/rust/src/qm/born_effect_valuation.rs`, and the Hermitian counterparts). *DAG status:* `FQ-GAP-BORN-UNIQUENESS-GLEASON` is `CONDITIONAL`. *Non-claims:* the matrix carrier and additivity on all effects, not only on projections, are supplied; there is no continuity, no real scalar field and no projection-lattice Gleason theorem; the operational justification of effect additivity and the projection-only frame-function route at $n\ge 3$ are open.
2. **Carrier-level specification of continuous time (merged with #113; run `20261020T225000Z_discrete_time_spec`, `lean4/DiscreteTimeStoneSpec.lean`).** Continuous time on the finite carrier means a $\mathbb Q$-parameter group extending the $\mathbb Z$-action of a unit step. Such a group needs roots of every order (`QParamGroup.roots_of_all_orders`). The rational $2\times 2$ Pythagorean rotation of angle $(3/5,4/5)$ has no rational half-step (`no_rational_half_step`, `no_qparam_group_through_R345`), and matrix half-steps are not unique (`matrix_half_step_not_unique`); a half-step appears only after adjoining $\sqrt5$. *DAG status:* `FQ-GAP-STONE-CONTINUOUS-TIME` is `CONDITIONAL`. *Non-claims:* the general triviality of $\mathbb Q$-parameter groups over $\mathbb Q(i)$ is open, and strong continuity, the $\mathbb R$-completion and a generator selection remain declared imports. The specification states what continuous time would need; it does not construct it.
3. **Controlled Hilbert completion (#117) and its steps (#122; runs `20261020T230000Z_completion`, `20261021T003000Z_lift_steps`).** This is the *construction* half of the split described in §5, item 1. With the scalar field $k\in\{\mathbb R,\mathbb C\}$ and the $\ell^2$ uniformity supplied as named hypotheses, the exact carriers $\mathrm{Fin}\,n\to\mathbb Q$ form a tower under zero padding exhausted by its finite stages; the Hausdorff completion of $\mathbb N\to_0 k$ is a complete inner product space into which the exact carrier embeds injectively, inner-product-preservingly and compatibly with padding; a sequence of exact vectors is Cauchy in the lift exactly when it is rational-$\ell^2$-Cauchy, and then it converges; over $\mathbb R$ the exact carrier is dense and the lift is strictly larger than the carrier; the completion under the intrinsic rational uniformity is uniformly isomorphic to the lift, which is linearly isometric to $\ell^2(\mathbb N,k)$; a $\mathbb Q$-linear map with a rational quadratic bound $C$ lifts uniquely to a continuous operator of norm at most $\sqrt C$ (the shift lifts to an isometry), and the coordinate-sum functional has no continuous extension (`lean4/HilbertLift*.lean`, capstones `HilbertLift.controlled_completion`, `controlled_completion_complex`, `intrinsic_completion`, `l2_model_summary`, `operator_lift_summary`). *DAG status:* `FQ-CONTINUUM-HILBERT-LIFT-CONSTRUCTION` is `PROVED_LEAN` (no PFP review); `FQ-GAP-CONTINUUM-HILBERT-LIFT` is `CONDITIONAL` and `GP-IMPORT-CONTINUUM-HILBERT` is `IMPORTED_ASSUMPTION`. *Non-claims:* the selection of the scalar field and of the $\ell^2$ uniformity from finite-theory primitives is not derived; the bound $C$ is a hypothesis; dynamics and generators are not lifted.
4. **Uniqueness of the inner product on the sector carrier (#125; run `20261021T013500Z_sector_form`).** On $\mathbb Q^n$ (and, for the Hermitian form, on $\mathbb Q(i)^n$), a symmetric (Hermitian) Gram form whose quadratic readout is additive on disjoint sector supports and invariant under sector permutations that generate a transitive group equals a positive scalar times the standard form (`InnerProductFable.SectorForm.eq_smul_one_generated`, `eq_one_of_normalized` in `lean4/SectorFormUniqueness.lean`; `lean4/SectorFormHermitian.lean`). Sector additivity alone forces the sector basis to be orthogonal. The $H005$ form $\mathrm{diag}(1,2)$ is sector-additive and violates the symmetry law, so the earlier non-uniqueness is exactly the absence of that law. *DAG status:* `L1-IMP-HILBERT-INNER-PRODUCT` is `CONDITIONAL`; `L1-IMP-ORTHOGONAL-ADDITIVITY` is `CONDITIONAL`; `L1-IMP-SECTOR-SYMMETRY-LAW` is `IMPORTED_ASSUMPTION`. *Non-claims:* both laws are supplied as laws of the readout, not derived from primitive difference; the sector carrier, the scalar field and the quadratic shape of the readout remain imports; frame additivity on arbitrary orthogonal frames, as a Gleason-type uniqueness needs, is not derived. The PFP review of `L1-IMP-HILBERT-INNER-PRODUCT` predates this run and is marked superseded by it.
5. **Derivation papers from pre-genesis to WDP (#128; `TFQ-0417` to `TFQ-0558`).** 142 new derivation papers, with the 72 existing ones, give the route from the inert inscription `<>` (`TFQ-0000`) through Genesis, its expansion past the `dbccpage/19L57G1` freeze, $S(n)$ and MSS-N to the Witnessed Difference Programme. The reading order is `dag/derivations/PREGENESIS_TO_WDP_ROUTE.md`; the papers are generated from `dag/fragments/pregenesis_to_wdp.json`. Frontier items are kept as `OPEN_OBLIGATION`; a step whose Lean source exists only in an external repository is a `CONDITIONAL` node with a named import, never `PROVED_LEAN`. The route contributes 137 `PGW-*` nodes (44 `PROVED_LEAN`, 40 `DEFINITION`, 16 `OPEN`, 15 `CONDITIONAL`, 13 `PROVED_PROSE`, 9 `COMPUTATIONALLY_CHECKED`); none has a PFP review. *Non-claims:* the papers record the route and its obligations. They do not close the `GAP_NO_DERIVATION` routes (one example is the step from `<>` to the admitted root Difference joined with Structure), and a `PROVED_LEAN` label on an unreviewed `PGW-*` node has the scope of its node text only.
6. **Python dual of the QM-122 witnesses (#130).** `code/python/src/qm122_lib/qm122_dual.py` (with `code/python/src/qm/qm122_dual.py` and `code/python/tests/test_qm122_dual.py`) is an exact Python dual of the named QM-122 report, dilation and Gauss-integer witnesses, from claim `QM-122-C38`; the exhibited vectors are the `psi1` and `psi2` of `lean4/H008PhaseBlindPresentation.lean`. The same change moved `papers/core/fsp/000_meron_sign_problem` and `001_hubbard_sign_problem` up to `papers/core/` and refactored Rust modules for the Gate 5 complexity limits. *DAG status:* the related nodes are `L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE` (`PROVED_LEAN`, not reviewed; its prompt was never executed) and `L1-QM122-LEFTOVER-MNC-NOT-RECOVERED` (`PROVED_LEAN`, `statement_narrowed`). *Non-claims:* the file is a computation and not a Lean proof; it proves no Gleason uniqueness and does not recover $M_n(\mathbb C)$; it promotes no node.
7. **One graph for the DAG and the TFQ tree, with four audited corpora (#131).** `dag/derivation_dag.json` and `dag/theory_of_finite_qm.jsonl` are joined by `dag/sync_unified_dag.py`: every TFQ record names at least one DAG node and every DAG node is named by at least one record. A record that named no node received a node with the record's id and a route from its parent's node; its status is the record status mapped *down*, never up. The audited records of the fermion-sign (41 nodes), dimension-six MUB (66), Majorana (46) and Dressing Field Method (43) corpora are application-branch nodes carrying both the status the source claims and the audited status; the audit lowered several claims. Examples: `FSP-MASTER-DICHOTOMY-REFUTED` (the source record `FSP-DERIV-056` claims `PROVED_LEAN`; the dichotomy fails as stated), `MUB6-AFFINE-FIBER-THIRD-BASIS` (`REFUTED`) and `MUB6-MAX-MUB-SIX-EQUALS-THREE` (`OPEN`: the maximum number of mutually unbiased bases in $\mathbb C^6$ is not known). *Non-claims:* the corpus papers in `papers/core/fsp`, `mub6`, `majorana` and `papers/ravera_dfm_dossier.md` have not been reconciled with these audits in this edition; the DAG status of a corpus node, not the corpus paper's own label, is the status to cite.
8. **PFP reviews of 151 nodes (#133; 9 batches, 2026-10-19 and 2026-10-20).** For each of 151 nodes the result folder `dag/results/<NODE-ID>/reviews/` was read and its decision written onto the node as the `pfp_review` object of §13.8.12: 68 nodes `consistent`, 9 `caveat_added`, 52 `statement_narrowed` and 22 `status_lowered` (all 22 from `PROVED_LEAN` to `COMPUTATIONALLY_CHECKED`). The sealed runs and the review files were not edited; later runs reach the result folders through addenda. *Non-claims:* 26 prompts were never executed (4 `L1-*` and 22 `PG-*`), and 560 of the 737 nodes have no prompt at all, so the reviewed set is not the DAG; the reviewer is one local researcher; a review does not run an independent proof check.

## References

Numbers in square brackets refer to this list; it is also shipped as `docs/references.md`.

1. A. M. Gleason, “Measures on the Closed Subspaces of a Hilbert Space,” Journal of Mathematics and Mechanics 6, 885–893 (1957).
2. A. Cabello, J. M. Estebaranz and G. García-Alcaine, “Bell-Kochen-Specker Theorem: A Proof with 18 Vectors,” Physics Letters A 212, 183–187 (1996).
3. P. Busch, “Quantum States and Generalized Observables: A Simple Proof of Gleason's Theorem,” Physical Review Letters 91, 120403 (2003).
4. H. Weyl, “The Theory of Groups and Quantum Mechanics,” Dover Publications (1950).
5. N. D. Mermin, “Hidden Variables and the Two Theorems of John Bell,” Reviews of Modern Physics 65, 803–815 (1993).
6. A. Peres, “Incompatible Results of Quantum Measurements,” Physics Letters A 151, 107–108 (1990).
7. R. D. Sorkin, “Quantum Mechanics as Quantum Measure Theory,” Modern Physics Letters A 9, 3119–3127 (1994).
8. M. Schlosshauer, “Decoherence, the Measurement Problem, and Interpretations of Quantum Mechanics,” Reviews of Modern Physics 76, 1267–1305 (2004). [arXiv:quant-ph/0312059](https://arxiv.org/abs/quant-ph/0312059).
9. T. Maudlin, “Three Measurement Problems,” Topoi 14, 7–15 (1995). [doi:10.1007/BF00763473](https://doi.org/10.1007/BF00763473).
10. W. H. Zurek, “Decoherence, Einselection, and the Quantum Origins of the Classical,” Reviews of Modern Physics 75, 715–775 (2003). [doi:10.1103/RevModPhys.75.715](https://doi.org/10.1103/RevModPhys.75.715).
11. M. Horodecki, P. W. Shor and M. B. Ruskai, “General Entanglement Breaking Channels” (2003). [arXiv:quant-ph/0302031](https://arxiv.org/abs/quant-ph/0302031); journal version [doi:10.1142/S0129055X03001709](https://doi.org/10.1142/S0129055X03001709).
12. J. H. Carroll, *Projection Obstruction for Factorized States*, author-review version 6.9.16 (2026), §§4.3.2, 7.6, 7.10 and Appendix E. Local companion address: `companion_papers/projection_obstruction.md`.
13. J. H. Carroll, *Trace-Zero Repair Quotients on a Finite Graph: An Exact Qutrit Counterexample and the Correct Scalar-Divergence Dual*, Version 0.57.0 (2026-10-16). Local companion address: `companion_papers/trace_zero_quotient_duality_monograph.md` (byte copy of the sibling release `013_trace_zero_quotient_duality`).
14. J. S. Bell, “On the Einstein Podolsky Rosen Paradox,” *Physics* **1**, 195–200 (1964). [doi:10.1103/PhysicsPhysiqueFizika.1.195](https://doi.org/10.1103/PhysicsPhysiqueFizika.1.195).
15. J. F. Clauser, M. A. Horne, A. Shimony and R. A. Holt, “Proposed Experiment to Test Local Hidden-Variable Theories,” *Physical Review Letters* **23**, 880–884 (1969). [doi:10.1103/PhysRevLett.23.880](https://doi.org/10.1103/PhysRevLett.23.880).
16. A. Fine, “Hidden Variables, Joint Probability, and the Bell Inequalities,” *Physical Review Letters* **48**, 291–295 (1982). [doi:10.1103/PhysRevLett.48.291](https://doi.org/10.1103/PhysRevLett.48.291).
17. B. S. Cirel'son, “Quantum Generalizations of Bell's Inequality,” *Letters in Mathematical Physics* **4**, 93–100 (1980). [doi:10.1007/BF00417500](https://doi.org/10.1007/BF00417500).
18. S. Abramsky and A. Brandenburger, “The Sheaf-Theoretic Structure of Non-Locality and Contextuality,” *New Journal of Physics* **13**, 113036 (2011). [doi:10.1088/1367-2630/13/11/113036](https://doi.org/10.1088/1367-2630/13/11/113036).
19. S. Abramsky, S. Mansfield and R. Soares Barbosa, “The Cohomology of Non-Locality and Contextuality,” *Electronic Proceedings in Theoretical Computer Science* **95**, 1–14 (2012). [doi:10.4204/EPTCS.95.1](https://doi.org/10.4204/EPTCS.95.1).
20. N. D. Mermin, “Simple Unified Form for the Major No-Hidden-Variables Theorems,” *Physical Review Letters* **65**, 3373–3376 (1990). [doi:10.1103/PhysRevLett.65.3373](https://doi.org/10.1103/PhysRevLett.65.3373).
21. T. Regge, “General Relativity without Coordinates,” *Il Nuovo Cimento* **19**, 558–571 (1961). [doi:10.1007/BF02733251](https://doi.org/10.1007/BF02733251).
22. Y. Aharonov and D. Bohm, “Significance of Electromagnetic Potentials in the Quantum Theory,” *Physical Review* **115**, 485–491 (1959). [doi:10.1103/PhysRev.115.485](https://doi.org/10.1103/PhysRev.115.485).
23. M. V. Berry, “Quantal Phase Factors Accompanying Adiabatic Changes,” *Proceedings of the Royal Society A* **392**, 45–57 (1984). [doi:10.1098/rspa.1984.0023](https://doi.org/10.1098/rspa.1984.0023).
24. A. Baker, “Linear Forms in the Logarithms of Algebraic Numbers (III),” *Mathematika* **14**(2), 220–228 (1967). [doi:10.1112/S0025579300003843](https://doi.org/10.1112/S0025579300003843).
25. B. Eastin and E. Knill, “Restrictions on Transversal Encoded Quantum Gate Sets,” *Physical Review Letters* **102**, 110502 (2009). [doi:10.1103/PhysRevLett.102.110502](https://doi.org/10.1103/PhysRevLett.102.110502).
26. *Native joint operations and a Genesis-to-Bell experiment*, The Symbol Game repository, revision `4a4fd192f` (2026); executable as `omega_engine/crates_rs/omega_wdp/src/genesis_bell.rs` with the tests `omega_engine/crates_rs/tests/omega_wdp/genesis_bell_joint.rs`.
27. A. Baker, “Linear Forms in the Logarithms of Algebraic Numbers (I),” *Mathematika* **13**, 204–216 (1966).
