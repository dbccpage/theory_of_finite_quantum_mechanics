# Scoped review of the finite quantum mechanics core

**Conclusion:** the newer main paper resolves both mathematical issues identified in Paper 080. It also supplies strong finite examples for explaining phase-sensitive reports, records, conditional updating, and Bell obstruction. It does **not** derive Hilbert geometry, a Hamiltonian time law, Noether’s theorem, or Everett’s ontology from primitive difference.

Sources:

- **M:** [finite_quantum_mechanics.md](C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/atlas/papers/core/finite_quantum_mechanics.md).
- **P:** [finite_quantum_mechanics_proofs.md](C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/atlas/papers/core/finite_quantum_mechanics_proofs.md).

**Read scope:** P §§1–8, including dynamics, Hilbert completion, and the Gaussian-carrier limitations; selected main-paper statements in §§1, 4–5, 9, 11, 13.1–13.8, and the later-results summary. This was not a full corpus audit. I did not read the WDP monograph, inspect implementations, run Lean or replay programs, or contact external services.

## 1. The two Paper 080 findings are resolved in the newer main paper

### Scalar-divergence duality: resolved

M §11.2, lines 623–661, explicitly distinguishes:

\[
(d_0^*M)_v\in\mathbb RI
\]
for trace-zero vertex repairs, from literal zero divergence for unrestricted Hermitian repairs.

Its \(K_{2,3}\) example correctly separates the two primal values:
\[
\Phi_0=6,\qquad \Phi_{\mathrm{all}}=\frac92.
\]

The displayed certificates are arithmetically consistent. For \(D_k=3E_{kk}-I\), each \(D_k\) has eigenvalues \(2,-1,-1\); its trace-distance norm is \(2\). The witnesses \(D_k/3\) have spectral diameter one and attain the trace-zero value. The supplied unrestricted potentials leave residuals \(-3E_{kk}\), each of trace-distance norm \(3/2\), and \(D_k/4\) supplies the matching bounded dual value.

P §2.5, lines 327–345, correctly proves the **local** dual norm modulo scalar identity. It does not itself present the graph-level distinction, which M supplies.

**Do not carry the historical centered-balance objection forward as an unresolved mathematical defect of M §11.2.**

### All-channel norm selection: resolved

M §11.3, lines 663–685, supplies the full measure-and-prepare argument. Given trace-zero Hermitian \(X,Y\) with \(\|Y\|_1\le\|X\|_1\), it constructs a CPTP map carrying \(X\) exactly to \(Y\). Equal trace norms therefore permit transports in both directions; homogeneity gives one common proportionality constant.

The proof is valid on the stated full complex matrix/channel domain. It does not select that domain from primitive difference or guarantee closure inside a smaller arithmetic field.

**Do not present non-proportional all-channel-contractive norm families as an outstanding mathematical possibility under these exact assumptions.**

## 2. Strongest finite bridges for the strips

### A. A report can erase a distinction needed by a later operation

**Derived:** P §§1.2–1.4, lines 59–144; M §13.8, lines 1261–1278.

The particularly useful normalized rational example is
\[
\psi_\pm=(3,\pm4)/5,\qquad
U=\frac15
\begin{pmatrix}
3&4\\
-4&3
\end{pmatrix}.
\]
Both preparations have population report
\[
(9/25,16/25),
\]
but the first output population after the same \(U\) is respectively
\[
1,\qquad 49/625.
\]

This gives a concrete three-panel lesson: **same present magnitudes; apply the same mixing rule; different later magnitudes.**

**Supplied:** signed linear coordinates, the mixing operation, and squared-magnitude readout. This demonstrates the insufficiency of a report for a specified future question. It does not derive complex amplitudes or Born weights.

For the simpler P §1.3 example, remember that \(H(a,b)=(a+b,a-b)\) is **unnormalized**: \(H^\dagger H=2I\). It must not be presented as a norm-preserving unitary without its normalization.

### B. A recorded distinction need not destroy global coherence

**Derived:** M §13.4, lines 924–968.

A supplied CNOT transforms
\[
(3|0\rangle+4|1\rangle)|0\rangle/5
\]
into
\[
(3|00\rangle+4|11\rangle)/5.
\]

The coherent joint state and its dephased mixture have identical subsystem populations and pointer statistics. Nevertheless, their trace distance is \(12/25\); the \(X\otimes X\) expectations are \(24/25\) and zero. Applying CNOT again exposes the difference in the system alone.

This is a strong record/recombination strip, provided the diagram explicitly distinguishes the **joint preparation**, the **restricted report**, and the **later joint control**.

**Supplied:** tensor composition, states, CNOT, trace pairing, and available controls. Neither a mixture nor one actual event follows merely from the reduced report.

### C. Conditional updates are calculations conditional on a record

**Derived:** M §13.3, lines 890–922.

Given a supplied instrument,
\[
p_i=\operatorname{tr}\mathcal I_i(\rho),\qquad
\rho_i=\mathcal I_i(\rho)/p_i
\]
when \(p_i>0\).

A branch with zero probability has no normalized conditional state. An effect determines an outcome’s probability functional but does not uniquely determine its disturbance.

A picture should say **“If this record is obtained…”**, not depict normalization itself as the mechanism selecting that record.

### D. Bell obstruction is failure of a positive common table

**Derived:** P §§3.1–3.3, lines 358–434; M §11.4 and §13.8, lines 687–701 and 1280–1325.

The finite argument has two distinct parts:

1. Every deterministic four-answer assignment gives a CHSH value of magnitude two, so every positive mixture does too.
2. Supplied quantum states and observables produce \(14/5\), with strictly positive probabilities in all four contexts.

The full support is significant: every deterministic assignment is support-compatible, yet no nonnegative joint distribution reproduces the probabilities.

**Supplied:** the pair tables or the quantum model producing them. A physical locality conclusion additionally uses setting independence and local response factorization. M states that reduction explicitly.

This supports a finite incompatibility lesson, not a unique ontology or an Everett conclusion.

### E. Quadratic readout can be selected within a declared candidate family

**Derived:** P §2.2, lines 249–266; M §11.6, lines 730–755.

Within the positive-power family, shared-ray consistency across the supplied rational contexts gives
\[
(3/5)^p+(4/5)^p=1,
\]
whose unique solution is \(p=2\).

**Supplied:** the power-law candidate family, orthonormal contexts, and context-consistency requirement. This is not unrestricted Born uniqueness.

The later effect-additive trace-representation route, M:1920, is stronger in a different direction: it assumes a matrix/effect carrier, positivity, normalization, and additivity on **all effects**. Those premises must remain visible.

### F. Finite branch counting has an exact rational boundary

**Derived:** P §4.5, lines 552–567.

A finite collection of equal-weight branches can reproduce rational proportions by construction. It cannot exactly reproduce irrational weights such as
\[
(5\pm\sqrt5)/10.
\]

This establishes a limitation of **finite equal-weight counting**, not a refutation of every relative-state interpretation. It also does not derive the prescribed rational weights by drawing the corresponding number of branches.

M §13.6, lines 1020–1053, appropriately keeps distributions, conditional states, and actual occurrence separate.

## 3. What these sources contribute toward Hamilton and Noether

P §4 establishes useful boundaries:

- **Lines 470–481:** finite-dimensional characteristic-zero matrices cannot satisfy \([X,P]=i\hbar I\) with \(\hbar\ne0\).
- **Lines 492–501:** the rational \((3,4,5)\) rotation has infinite order. Finite dimension does not imply periodic evolution.
- **Lines 512–529:** a report-level toggle has no half-step, while the enlarged matrix carrier has multiple half-steps; a discrete unitary does not select a unique logarithm or generator.

A modest further algebraic bridge follows from the supplied adjoint pairing in P §1.7: if an admitted unitary satisfies \(U^\dagger Q U=Q\), then
\[
\langle U\psi,Q\,U\psi\rangle=\langle\psi,Q\psi\rangle.
\]
That is discrete conservation **under the stated preservation assumption**. It is not a derivation of a Noether charge from an action symmetry.

These sources therefore support illustrations of preserved quantities and generator ambiguity. They do not close the missing action, time, or Hamiltonian-selection step.

## 4. The Hilbert lift is a construction after choosing its geometry

P §6, lines 608–690, is explicit and mathematically coherent:

- Supply \(\mathbb R\) or \(\mathbb C\), the inner product, and the \(\ell^2\) uniformity.
- Form the zero-padding tower and finitely supported sequences.
- Complete to a Hilbert space isometric to \(\ell^2\).
- Extend operators satisfying the supplied quadratic bound.

The harmonic truncations
\[
h_N=\sum_{i<N}\frac1{i+1}e_i
\]
make the distinction tangible: they are \(\ell^2\)-Cauchy, while their coordinate sums diverge. The choice of geometry changes which approximations converge and which operations extend.

**Not derived:** the selection of \(\ell^2\), the scalar field, dynamics, or generators. This is not an \(\ell^1\)-to-Hilbert selection theorem.

P §7, lines 709–724, also correctly limits the Gaussian-carrier results: Gaussian integers lack inverses and some Hermitian eigenvalues, and a Boolean toggle lacks a square root. These examples establish specific missing capabilities; they do not prove that complex continuum quantum mechanics is the unique repair.

## 5. Remaining concrete criticisms

### Medium — Clock completion is misstated in the main inventory

M:427 says the clock group
\[
\varinjlim_m \tfrac1m\mathbb Z/\mathbb Z=\mathbb Q/\mathbb Z
\]
has metric completion \(\mathbb R\).

With the usual compatible circle metric, its completion is \(\mathbb R/\mathbb Z\), as M:423 correctly states for the corresponding phase group. It does not become the real time line. A group embedding into the torsion-free additive group \(\mathbb R\) cannot preserve the nonzero torsion already present.

**Remedy:** distinguish a periodic clock completion from an unwrapped time parameter. Completing \(\mathbb Q\) under its usual metric yields \(\mathbb R\); completing \(\mathbb Q/\mathbb Z\) yields the circle. Passing between them requires additional structure.

### Medium — The proof companion and audit excerpts lag behind the main statements

P:324–325 and 345–347 describe all-channel trace-norm selection as open or unclaimed. M:315–320 and 663–685 contain the general written proof. M:1826 still repeats the older open obligation.

Similarly, P:263–266 says Lean does not check the real-exponent power theorem, while M:271–274 and 590–591 report a named real-exponent Lean theorem.

**Remedy:** distinguish the now-present prose theorem, the scope of each mechanized statement, and historical review status. These conflicts should be reconciled without treating a stale label as a mathematical refutation or inferring fresh build success.

I did not inspect the referenced Lean files, so I cannot adjudicate their current compilation or exact declarations.

### Low — Use one CHSH sign convention in a novice sequence

P §3.1 uses the minus sign on \(A_1B_0\); §§3.2–3.3 use the minus sign on the last correlation. The bounds are equivalent by a local sign relabeling, so the conclusions are valid, but that relabeling is unstated in the transition.

**Remedy:** use one convention throughout the teaching sequence or show the sign relabeling explicitly.

## Evidence ceiling

The directly checked content here is the written reasoning and the displayed finite arithmetic. Enumerations, exact replay claims, kernel checks, publication status, and physical realization were not independently verified.

The strongest next strip sequence is **equal report → shared mixing → different answer → correlated record → restricted indistinguishability → recoverable coherence**. Its supplied operations and readout must be declared. Bell and branch-counting results then add precise limitations; they do not select an interpretation or complete the Hamilton/Noether derivation.
