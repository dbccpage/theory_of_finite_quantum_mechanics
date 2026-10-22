<div align="center">

# Finite Quantum Mechanics: Source Notes and Reproduction Supplement

### Historical Claims, Corrections, Local Source Addresses, and Executable Scope

**Author:** Jeremy H. Carroll

**Date:** 2026-10-14

**Version:** 0.55.0

**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)

</div>

## Purpose and reading rule

This supplement preserves the detailed source-by-source analysis removed from
the reader-facing edition of *Finite Quantum Mechanics*. It records original
manuscript addresses, corrected statements, counterexamples, implementation
pointers, and unresolved obligations. A file path, test name, successful build,
or historical status label is not itself a mathematical proof. The main paper
states the current results by their hypotheses and conclusions; this document
records how those results relate to the retained source manuscripts.

The source manuscripts referred to below are included under
`sources/original_papers/` in the paper archive. They are historical inputs,
not automatically endorsed claims. Two public-record corrections prepared for
author submission are included under `docs/zenodo_errata/`.

## 1. Evidence standards and historical claim treatment

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
are redirect or alias stubs whose mathematical content is treated with the
destination result: residual density in §11.4, finite realization in §11.6,
the earlier phase selector in §11.27, and the three packaging annexes QM_064
(phase gauge, §11.28–§11.29), QM_074 (no-signalling, §11.33–§11.34) and QM_083
(complete positivity, §11.38).

## 2. Historical executable-model note

### 2.1 The executable model walk and its remaining derivation gap

The historical claim that no executable model sequence existed is refuted by
the legacy integration tests. The deeper derivation problem remains open:
direct packet consumption does not derive the packet or its quantum
interpretation from primitive difference. The current test is
`tests/legacy/e2e/test_quantum_walk_e2e.py::TestDirectCochainPacketWalkE2E`.

The engines compute interferometer fringes, Sorkin cancellation, rational
Cayley isometries and PSD filtering under declared inputs. The previous
complete-walk test computed `D(10, 10 + pi/2)` and then independently supplied
its complexes, Cayley parameter, cyclotomic weights and detector. The scalar
difference did not construct those inputs. The pairing fixture explicitly
applies `norm_sq`, so its third-order cancellation is a consequence of the
chosen quadratic readout. The legacy cochain classifier is a numerical LP
with a declared tolerance; its output is not an exact certificate.

An exact control keeps the three-slit cochain carrier and amplitudes fixed
and varies only the readout. If each open slit contributes amplitude $1/3$,
then $P_2(S)=(|S|/3)^2$ and $P_4(S)=(|S|/3)^4$ are nonnegative, bounded by one,
and have the same empty/full endpoint values. Yet their third-order terms
are respectively $0$ and $4/9$. Even $P_1(S)=|S|/3$ has zero third-order term
without being quadratic. These are readout tables on the declared finite
experiments, not reconstructions of full operational theories. The proof,
source audit and native check are in
[the primitive/readout boundary note](research/qm_primitive_readout_boundary.md).
The later note `research/quadratic_readout_finite_map.md` treats the
phase-blind polynomial readouts $\alpha|c|^2+\beta|c|^4$, where the
third-order term vanishes identically exactly when $\beta=0$; it does not
treat general readouts.

## 3. Publication provenance and public-record obligations

The paper archive contains all sixty-seven current original manuscripts under
`sources/original_papers/`, and every subsection 11.N of §4 gives the
corresponding local address. Historical hashes and per-source evidence observations remain
in repository custody records; the public `sha256sums` binds the exact copies
shipped with this paper. The current repository custody tests read all sixty-seven
manuscripts: fifty-four match their historical hashes and thirteen have
separately pinned current differences.
The 2026-10-13 reconciliation permits current claim use, including the five
retained-copy comparisons described in §9, through eighteen
version comparisons across sixteen sources. Each assessment identifies the
current premise, supported conclusion, correction or refusal, and affected
claim rows. All historical hashes and dispositions remain intact.

Repository custody also retains exact historical manuscript bytes for the primitive-difference,
superposition, channel-geometry, Mermin–Peres, and finite-Hilbert-boundary
papers. The affected versions of the Born-normalization, interference, and
later synthesis papers were assessed independently for their declared current
scope; unrecovered historical bytes are not claimed equivalent to them.
The omitted placeholder sources contribute no mathematical construction. This
completes the current-use version assessment, not a replay of historical Lean/Python receipts or closure of
scientific premise gaps. Published-version obligations and stale proof-receipt
scope remain separate.

**Publication status: sixty-five of the sixty-seven are unpublished.**
Established 2026-09-04 against `omega_engine_atlas/coda_atlas/F004_papers/zenodo_records.md` and
confirmed by the author. Those sixty-five may be rewritten or retired freely.

Retiring a package from this repository does not touch its public record.
**The two exceptions are the Born-normalization paper (§11.11) and the
channel-geometry paper (§11.35)**, each with a public Zenodo deposit
([20683775](https://zenodo.org/records/20683775) and
[20550459](https://zenodo.org/records/20550459)). A rewrite of either forks from
the published record rather than replacing it, so the relationship — erratum, new
version, or superseding paper — must be decided first. Repository custody tests
record and enforce that restriction.

The primitive-difference paper's header nevertheless read `**Status:
published Zenodo release**`, and
fifty-seven others read `RELEASED`, which in this tree means released-in-tree. That
false header is treated as a false receipt: a status line asserting a
public record is a receipt, and this one does not bind. The earlier retirement
removed those packages from the active corpus; restoring them does not validate
their headers. Those discrepancies remain provenance obligations, and §11.1
records the correction.

The restored original, its copy under
`sources/original_papers/000_primitive_difference_for_quantum_carriers/` and the
curated copy under `sources/000_primitive_difference_for_quantum_carriers/` now
read `UNPUBLISHED_LOCAL_SOURCE` on that status line. The historical text that
carried the false header is pinned by its digest and its recovered version in
`claims/source_inventory.yaml`; it is evidence of the discrepancy, not a
publication receipt.

Both published quantum-foundations papers carry a title drift:

| Dir | In-tree title | Zenodo |
| --- | --- | --- |
| `020_born_normalization_and_conditional_hilbert_lift` | Conditional Hilbert Lifts of $\ell^1$ Sector Weights and Born Normalization Redundancy | [20683775](https://zenodo.org/records/20683775) — *The Born Rule and Hilbert Space Emergence from $\ell^1$ Phase Averaging* |
| `080_cptp_trace_norm_geometry_and_quantum_dual_witnesses` | CPTP-**Compatible** Obstruction Theory: Trace-Norm Geometry and Quantum Dual Witnesses | [20550459](https://zenodo.org/records/20550459) — CPTP-**Invariant** Obstruction Theory… |

The second drift is not cosmetic. In this tree's vocabulary *invariant* is a
strictly stronger claim than *compatible*, so the public record may overclaim
relative to the paper it names. Settle which title the deposit carries before
either is cited.

## 4. Detailed constructions, corrections, and source addresses

This section retains the historical subsection numbers so references from the
main paper remain stable. Placeholder-only subsections 11.13 and 11.44 and the
source-note inventory formerly at 11.53 are omitted. The remaining results are
grouped by mathematical subject: finite cochains and state-effect models
(§§11.1–11.12), phase and dynamics (§§11.14–11.29), composition, Bell inequalities, and channels
(§§11.30–11.38), operational interpretation and error thresholds
(§§11.39–11.47), gravity, contextuality, and the finite Hilbert boundary
(§§11.48–11.52), and synthesis (§§11.54–11.60). Each subsection begins with a
local link to the relevant original manuscript in the paper archive. The link
records provenance; the argument is the stated object, hypotheses, proof or
certificate, and counterexample in the present text.

### Retained redirects and reservation records

Eight retained files do not warrant apparent mathematical sections. The phase
selector file is a redirect to the substantive treatment in §11.27; the
Copenhagen file contains only a reserved interpretation slot; and the six
later files contain no construction. They remain in the archive for provenance
and can be inspected at these local addresses:

- [Earlier $U(1)$ selector redirect](sources/original_papers/028_the_u1_selector/the_u1_selector.md)
- [Copenhagen interpretation reservation](sources/original_papers/095_copenhagen_as_authority_shadow/copenhagen_as_authority_shadow.md)
- [Inner-product admission reservation](sources/original_papers/200_inner_product_admission/inner_product_admission.md)
- [Bra-ket section admission reservation](sources/original_papers/201_braket_section_admission/braket_section_admission.md)
- [Operator-algebra reservation](sources/original_papers/202_operator_algebra_shadow/operator_algebra_shadow.md)
- [Measurement-problem reservation](sources/original_papers/203_measurement_problem_obstruction/measurement_problem_obstruction.md)
- [Born-uniqueness reservation](sources/original_papers/204_born_uniqueness_import_boundary/born_uniqueness_import_boundary.md)
- [Pointer-basis reservation](sources/original_papers/205_pointer_basis_obstruction/pointer_basis_obstruction.md)

These links establish custody only. They do not turn a redirect or reservation
into a result.

The following conventions apply:

- **Arithmetic.** The native results below use rationals, Gaussian rationals
  `Q(i)` or specified cyclotomic fields. Legacy floating implementations remain
  numerical demonstrations unless an exact counterpart is explicitly named.
- **Certificates.** A primal potential, dual separator, closure defect, exact
  factorization, or exhaustive finite enumeration is described by the
  predicate and witness it checks. The module that evaluates it is a
  reproduction pointer, not the source of its mathematical force.
- **Lean** for this programme lives in `lean4/quantum_mechanics/`, a separate
  Lake workspace at the repository root and at the root of the code-companion
  archive, not under this paper folder.
- **Paths.** A Rust test cited as `tests/<area>/<name>.rs`, as
  `<area>/<name>.rs`, as `tests/<name>.rs` or by its file name alone belongs to
  `omega_quantum_physics`. In the repository it is at
  `omega_engine/crates_rs/tests/omega_quantum_physics/<area>/<name>.rs`; the
  2026-10-14 code-companion archive keeps the earlier layout
  `omega_engine/crates_rs/omega_quantum_physics/tests/<area>/<name>.rs`. Tests
  of this paper's own `finite_qm_native` crate are cited as
  `native/tests/<name>.rs`, relative to this paper folder. A test of another
  crate names that crate.
- **Former module names.** Some "Now computed by" cells keep the module names
  of the former port. The item of that name now lives as follows:
  `finite_cochain_packet` in `omega_solvers::data_cochain_packet`
  (`FiniteCochainPacket` with `classify`, `quotient_mass`, `dimensions`,
  `primitive_difference` and `face_coboundary`, and the free function
  `certified_trichotomy`; no `certified_quotient_mass` is in the repository);
  `binary_pattern_carrier::PatternCarrier` in
  `omega_homology::graph_f2::PatternCarrier`; `cohomology_admission` in
  `omega_solvers::cert_cohomology_admission`; `rational_spin_lift` in
  `omega_lie_theory::su2_matrix::unit_quaternion_matrix` and
  `omega_lie_theory::su2::{rodrigues_quaternion, spin_lift, rotation_of_quaternion}`;
  `finite_classical_shadow::StochasticMap` in
  `omega_finite_probability::stochastic_map::StochasticMap`;
  `repair_quotient_bridge::RepairPacket` in
  `omega_solvers::data_repair_packet::RepairPacket`; and `sector_measurement`
  in `omega_quantum_physics::residual_density_calculus`. Other cells name the
  current items directly.
- **Citations.** Bracketed numbers refer to the References at the end. An
  imported theorem named in prose without a number, such as Minkowski's
  inequality or the Stinespring and Choi theorems, has no entry there.
- **Scope.** A finite check of a general statement remains a finite check. An
  exact counterexample refutes the quantified statement it violates; an audit
  label without the counterexample does not.

### 11.1 Primitive difference for quantum carriers

**Original paper in the paper archive:** [Primitive difference for quantum carriers](sources/original_papers/000_primitive_difference_for_quantum_carriers/primitive_difference_for_quantum_carriers.md).

The paper separated three constructions that are often conflated: real graph
cochains with a weighted `L1` quotient, separately declared U(1) connections,
and an independently declared `SU(N)` label space. All three now compute
exactly.

| Claim | Now computed by | Checked by (`tests/foundations/quantum_carrier_primitive_difference.rs`) |
| --- | --- | --- |
| QMC-T1 quotient norm with circulation dual | `finite_cochain_packet::FiniteCochainPacket::quotient_mass` | attained value and dual circulation on a weighted triangle; `I1` moves with the representative while `Phi1` does not; forests and the edgeless graph give zero; tampered certificates are refused |
| QMC-T2 gauge covariance | `u1_graph_connection::U1Connection::{covariant_difference, gauge_transform}` | edgewise `D_A' psi' = g(v) D_A psi`; the swapped convention `g(u) A conj(g(v))` fails |
| QMC-T3 closed-loop gauge invariance | `U1Connection::{holonomy, transport}`, `OrientedWalk` | closed holonomy invariant, open transport changes by `g(end) conj(g(start))`; walks are checked for edge index, orientation, continuity and closure; agrees with `omega_holonomy`'s loop product |
| QMC-T4 connection Laplacian | `U1Connection::laplacian`, `exact_hermitian` | Hermitian, PSD (exact LDLᵀ of the realification), `<psi, Delta psi>` equals the weighted Dirichlet energy, `Delta_A' = G Delta_A G*`; on the connected, positively weighted fixtures, definite when some loop holonomy is nontrivial and rank `V - 1` when flat |
| QMC-T5 cochain exponential descends | `u1_graph_connection::CochainExponential` | `Exp(omega + d0 f)` is the `u^f` gauge transform of `Exp(omega)` for `u = i`, `(3+4i)/5`, `(-7+24i)/25` |
| QMC-T6 Gell-Mann basis | `su_n::GellMannBasis` | count `N^2 - 1`, Gram `2 delta_ab` and real independence for `N = 2..6`; closure, total antisymmetry and Jacobi for `N = 2..4`; SU(2) and SU(3) structure constants match the standard tables, including `f_458 = f_678 = sqrt(3)/2` |
| QMC-P1 mass/phase embedding | `mass_phase_embedding::MassPhaseEmbedding` | unit `L2` norm; scale, phase and sign losses exhibited; implicit phases refused |

**Corrections and scope.**

- The source evaluated the quotient LP and the spectra numerically "up to
  declared tolerance". The implementation is exact: `Phi1` carries a replayed
  primal/dual certificate, and positivity is an exact inertia computation.
- The cochain exponential `exp(i alpha omega_e)` is implemented for integer
  cochains and a declared unit `u = exp(i alpha)` of `Q(i)`, so
  `Exp(omega)_e = u^(omega_e)` exactly. The only roots of unity in `Q(i)` are
  `±1, ±i`. For them, cochains that differ by the order on one edge collapse.
  Any other unit has infinite order, and the integer exponential is injective.
  Real-valued cochains and irrational scales are not covered.
- The diagonal Gell-Mann scales `sqrt(2/(l(l+1)))` are irrational. Generators
  are stored as `sqrt(r_a) M_a`. Structure constants are exact surds
  `q sqrt(s)`, and the Jacobi identity is checked as a rational identity after
  the common surd factor is removed.
- `omega_holonomy`'s connection Laplacian puts `-w U(u->v)` in block `(u, v)`.
  That is the entrywise conjugate of the paper's `D_A* W D_A`, which a test
  pins. For non-abelian fibres the same placement is not gauge covariant: with
  rational SO(3) fibres on a graph with two cycles, its characteristic
  polynomial changes under `omega_holonomy`'s own gauge action, while
  `D* W D` does not. That is a latent issue in `omega_holonomy`, not in this
  paper's U(1) setting.
- The source's `Status: published Zenodo release` was false.
  Its earlier retirement did not correct that header. The status line now
  reads `UNPUBLISHED_LOCAL_SOURCE`; the historical version remains evidence of
  the discrepancy, not a publication receipt.

**What stays outside.** Continuum limits and physical model selection. The
phase scale, the edge weights and the `SU(N)` label space remain declared
inputs, and no graph constructs the label space. QMC-NC1 is still a scope
fence. No quantum dynamics, Born rule, carrier emergence or authority follows.

### 11.2 A registry-relative quantum interface

**Original paper in the paper archive:** [Tower walk / registry-relative interface lift](sources/original_papers/001_tower_walk_registry_relative_interface_lift/tower_walk_registry_relative_interface_lift.md).

The paper's central statement is conditional: a failed commutative
representation forces a declared quantum interface only relative to a declared
lift registry, a valid transport, a resolving lift and registry-relative
minimality. `tower_walk_validator` computes every part of that statement that
has finite content. Three registry verdicts are computed; the scalar and
rotational rows fail by declared witnesses, and the GPT and quaternionic rows
are refused while no composite rule is declared.

| Claim | Now computed by | Checked by (`native/tests/tower_walk_registry.rs`) |
| --- | --- | --- |
| C1, C17 controlling implication (conditional) | `validate_tower_walk`, `canonical_prerequisites` | with registry-relative minimality supplied, the conclusion is restricted to that declared registry; when minimality is absent, the output is explicitly `ConditionalOnMinimality`; failed minimality is rejected |
| C6 exact trichotomy | `finite_cochain_packet::classify`, `m2_quantum_packet::VerifiedM2Packet::classify` | all three classes on the triangle packet; agreement with `omega_functional`'s trichotomy on `M_2` residuals |
| C7 lift trigger (definition) | `find_lift_trigger` | a context that separates merged points is found; a faithful projection or identity context gives none; malformed contexts refused |
| C13–C15 norm branches (conditional) | `scalar_edge_norm`, `rotational_edge_norm`, `half_trace_norm_2x2` | $\sum_e w_e\|x_e\|_2$ is an exact surd sum and rotation invariant while $\sum_e w_e|x_e|$ is not; $\frac12\|X\|_1$ is exact for Hermitian $2\times2$ matrices; the half trace norm contracts under three rational channels on two inputs, strictly under dephasing and with equality under a unitary; every positive multiple contracts too, so monotonicity cannot fix the factor $1/2$, which distinguishability fixes: orthogonal pure states are at distance $1$ |
| C16 packet non-absorption and commutator fence | `holonomy_commutator` via `omega_holonomy`; Mermin–Peres search | noncommuting loop holonomies are detected exactly, commuting ones are not; the classical gluing packet fails on all 512 assignments |
| C20 linearized Born comparison | `m2_quantum_packet` `d1` | see §11.5 (QM_005) |
| C22 validator ledger (definition) | `validate_tower_walk` | row statuses, including the three refused firewall rows |
| C29 registry audit (conditional) | `declared_registry`, `audit_registry`, `RegistryAudit::minimal_interface` | six rows fail or refuse and the complex packet resolves; a failed `M_2` replay removes the only resolver, and so does a packet that replays but declares a Born probability off `Tr(E rho)`, which fails with the defect as its witness; declaring a GPT or quaternionic composite rule adds a second resolver and destroys uniqueness |
| C30 rebit count | `adjudicate` with `composition_tomography::LocalTomographyReport` | `3 * 3 = 9 != 10` |

**Corrections and scope.**

- The paper's §11 registry block was an empty placeholder, and its O020, O021
  and O022 prototypes were never vendored. The registry is now executable. The
  classical gluing row fails on an exhaustive search, the rebit row on the
  local-tomography count, and the complex row resolves only when its finite
  `M_2` obligations replay and its declared Born table has no defect.
- A review found that the complex row resolved whenever the packet replayed,
  even when a declared Born probability differed from `Tr(E rho)`. Such a
  defect is an active closure failure. It now fails the row and removes
  `Resolve`, because an open obstruction dominates.
- Three antecedents (lift protocol, admissibility, valid transport) are
  declared inputs of the canonical walk; they are not computed. `Open_comm` and
  `Resolve` are computed.
- "Registry-relative minimality" is shown to be exactly that: adding one row
  with a declared composite rule removes uniqueness. When minimality has not
  been supplied, no unconditional forced-lift conclusion is emitted.
- The package's only test, `code/test_qm_001_tower_walk.py`, compared a dict
  comprehension with the expression that built it. It retires
  with the package; the tests above replace it.
- The O021 survival flags (`origin_derived`, `full_survives_descent_claim`,
  sealed terminal) are fields the validator has no path to set.
- $\text{CPTPMonotone} \nRightarrow \frac{1}{2}\|\cdot\|_1$ is exhibited only by rescaling. That shows
  the normalization axiom is independent, and nothing more.

**What stays outside.** The six-role tower narrative, the survival doctrine
(C24–C26, still `OPEN`), the cofiber bridge (C31, see QM_002) and every
authority statement. The walk derives no Hilbert space, Born rule or CPTP law.
Those are imports of the complex packet, and registry-relative minimality is
not comprehensive uniqueness.

### 11.3 A finite Banach quotient model of repair (QM-002 merged and retired)

**Original paper in the paper archive:** [Cofiber to Banach quotient bridge](sources/original_papers/002_cofiber_to_banach_quotient_bridge/cofiber_to_banach_quotient_bridge.md) (standalone manuscript retired; reduced to a single proposition merged into the shared finite-obstruction quotient treatment in WDP Chapter 4 §4.2.1 and §11.3 here).

The paper's one theorem is scalar: for a declared finite-dimensional linear repair map
$d_0: C^0 \to C^1$ with repair subspace $M = \operatorname{im}(d_0)$, the repair-distance functional
$\Phi_1([x]) = \inf_{\alpha \in C^0} \|x - d_0 \alpha\|_{1,w}$ is the quotient norm of the finite Banach cokernel
$C^1 / \operatorname{im}(d_0)$. Its Lean kernel only stored a supplied equality (`phi1_eq_banachShadow` is a definitional
store/read, not the analytic identity; C6 remains prose-proved and computational, not mechanized).
`repair_quotient_bridge::RepairPacket` computes both sides for any rational $d_0$, not just graph incidences.

| Claim | Now computed by | Checked by (`tests/foundations/repair_cofiber_banach_shadow.rs`) |
| --- | --- | --- |
| C3, C4 repair residual `coker(d0)` and its quotient norm (definitions) | `RepairPacket::{cokernel_dimension, quotient_norm}` | cokernel dimensions `m - rank d0`; quotient norm certified primal and dual |
| C5 finite images are closed | `RepairPacket::repair_witness` (exact membership) | the quotient norm is zero exactly on the image, with a replayed preimage, on a rank-two map `Q^2 -> Q^4` with unequal weights |
| C6 scalar bridge $\Phi_1=\|[x]\|_{\mathrm{quot}}$ | `quotient_norm` | the certified value is below every repair on a rational grid and attained; class invariance, absolute homogeneity and the triangle inequality hold on classes; the graph and repair presentations using the same $d_0$ give the same value |
| C7 `Phi1 = R_Lambda` refused (type separation) | `cokernel_dimension` | two repair maps on the same `Q^3` give `x = (0,0,1)` the same `Phi1 = 1`, but their cokernels have dimensions 2 and 1 |
| C9 executable witness | `quotient_norm`, `repair_witness` | `d0 = (1,-1,0)`, unit weights, `x = (0,0,1)` gives `1` with minimiser `a = 0`; `x = (1,-1,0)` gives `0` with preimage `a = 1` |

**Corrections and scope.**

- **Closedness has a different job:** The original source suggested finite-dimensional closedness was needed for equality between distance to the repair image and distance to its closure. It is not: $\operatorname{dist}(x, M) = \operatorname{dist}(x, \overline{M})$ holds for any subspace in any normed space (`Metric.infDist_closure`). What closedness establishes is the separation implication $\operatorname{dist}(x, M) = 0 \implies x \in M$, ensuring that the algebraic quotient $C^1/M$ is a Hausdorff-separated normed space and distinguishing exact repair from limiting repair. In infinite dimensions, e.g. $T:\ell^1\to\ell^1, (Ta)_n = a_n/n$, the range is dense so $\inf_a \|x - Ta\|_1 = 0$, but $x_n = 1/n^2 \notin \operatorname{ran} T$. Finite dimensionality ensures $\Phi_1([x]) = 0 \iff x \in \operatorname{im}(d_0)$.
- **Categorical language describes a chosen finite model:** "A finite linear repair map has an ordinary Banach cokernel whose quotient norm is the repair-distance functional." This identifies the cokernel in $\operatorname{Arr}(\mathsf{FinBan}_{\mathbb{R}})$ as a chosen model; it leaves open an unrestricted categorical comparison, which would require an explicit universal comparison theorem and isometric preservation.
- **Closed quotient norm formula:** For $d_0(\alpha) = (\alpha, -\alpha, 0)$ on $\mathbb{R}^3$, the quotient norm evaluates in closed form: $\Phi_1([x_1, x_2, x_3]) = |x_1 + x_2| + |x_3|$, attaining $1$ on $(0,0,1)$ and $0$ on $(1,-1,0)$. This replaces the previous toy calculation and resolves the §6 text splice.
- **Boundary to residual density:** A quotient residual does not descend to coordinatewise absolute-value density: for $M = \operatorname{span}\{(1,-1)\}$, $[(1,0)] = [(0,1)]$ with minimal $\ell^1$ norm $1$, but their normalized densities $\operatorname{diag}(1,0)$ and $\operatorname{diag}(0,1)$ are orthogonal. Density is a diagnostic of a selected representative, not a quotient class invariant.
- **Corrected proof status:** C6 is prose-proved and verified via certified Rust solver, not mechanized in Lean (`phi1_eq_banachShadow` is store/read only); contradictory ledger footer claiming mechanization is discarded.
- The "executable witness" `cofiber_banach_bridge` was a pointer to code that did not exist. The witness now runs in `omega_solvers`, together with the norm axioms the bridge relies on.
- `Phi1` for a general `d0` goes through the same certified path as the graph packets (`finite_cochain_packet::certified_quotient_mass`: `omega_solvers` proposes, `omega_functional` replays). No second solver was written.
- The type-separation refusal (C7) has a sharper witness than the Lean `cofiber_richer_than_scalar`: equal scalars on the same ambient space and the same representative, with non-isomorphic cokernels.

**What stays outside.** The unrestricted amplitude/composition bridge is not defined until a
realization functor is declared (C8). The `(infinity,1)`-categorical setting
(C2) is not modelled. The theorem is a bridge, not an origin statement, and it
does not establish physical realization (C1, C10).

### 11.4 Residual density across the $L^1/L^2$ boundary (QM-003 and QM-004 absorbed and retired)

**Original papers in the paper archive:** [Residual density calculus](sources/original_papers/003_residual_density_calculus_l1_l2_boundary/residual_density_calculus_l1_l2_boundary.md) and [General obstruction management calculus](sources/original_papers/004_general_obstruction_management_calculus/general_obstruction_management_calculus.md) (both standalone manuscripts retired; mathematical core consolidated into WDP Chapter 4 §4.2.2 and §11.4 here).

QM_003 was a redirect stub; its RDB-1..13 rows were absorbed as Part I of
QM_004 (GOMC). Standalone QM-004 is now retired. Its mathematical core—normalized
mass ledgers as diagonal densities modulo positive overall scaling, the static
observer factorization criterion $O(x) = O(y) \implies h(x) = h(y)$, and exact-repair
translation commutativity $R_a R_b = R_b R_a$ ruling out noncommuting operator
algebras from exact repair rearrangement—is consolidated into WDP Chapter 4 §4.2.2.
Everett/MCTS analogies, branch-search framing, and repeated authority results are
omitted as separate derivation burdens. Both papers leaned on Lean files that survive only as
unbuildable reading guides (`research/lean4/qm_rdb_*.md`, `qm_gomc_*.md`), and
on an `f64` engine slice, `omega_engines::quantum::gomc_diagnostics`. The
exact statements now compute in two modules. `residual_density_calculus`
holds ledgers, diagonal densities, licensed coherence and stochastic
pushforward. `obstruction_management_calculus` holds observer
nonfaithfulness, local satisfiability with global obstruction, Born-pairing non-selection, branch search,
reconstruction terminals, the coherence-lift gate and the composed report.

| Claims | Now computed by | Checked by (`native/tests/residual_density_boundary.rs`, `native/tests/obstruction_management_firewall.rs`) |
| --- | --- | --- |
| RDB-1, RDB-2, 003-C14, 004-C5, C6 normalization and diagonal density | `ResidualLedger::{weights, diagonal_density, purity}`, `sector_measurement` | `mu = (3,1,0)` gives `p = (3/4,1/4,0)`, a PSD trace-one `diag(p)` whose sector measurement returns `p`, purity `5/8` |
| RDB-3, 004-C7 weights do not determine phase | `conjugate` | `\|+><+\|` and `\|-><-\|` share weights `(1/2,1/2)`; a rational rotation sends them to `(1/50,49/50)` and `(49/50,1/50)` |
| RDB-3b orientation blindness | `ResidualLedger::from_signed_residual` | `(2,-3)` and `(-2,3)` give the same ledger `(2/5,3/5)` |
| 004-C11 ledger and diagonal density are one boundary | `ledger_from_diagonal_density` | round trip; normalized ledgers are fixed points; coherent, negative or trace-two matrices are refused |
| RDB-6 licensed coherence | `evaluate_coherence`, `licensed_coherent_density` | sector identity, PSD and phase presence are computed; the observer basis is declared; each missing field refuses |
| RDB-12, RDB-7, 004-C20 stochastic pushforward | `row_stochastic_pushforward` | total mass and nonnegativity preserved; negative or leaky rows refused |
| RDB-4, RDB-5b, 004-C9, C12 observer nonfaithfulness and composition | `hidden_separation`, `pair_observer` | a merging observer with a separating hidden readout; two locally green fragments whose visible pair is green while a hidden glue separates |
| RDB-5, 004-C2 local agreement with global obstruction | `lggr_cochain_witness` | on a 4-cycle, `(1,-1,1,-1) = d0(0,1,0,1)` and `(1,1,1,1)` have equal edge masses but classes `ExactRepair` and `ClosedResidual`; two zero cochains give no witness rather than a refusal |
| 004-C13 `L1` readouts do not select Born | `born_pairing`, `dephased_pairing` | agree on diagonal data, both normalized on `{\|+><+\|, \|-><-\|}`, disagree (`1` versus `1/2`) off the diagonal |
| 004-C14 amplitudes do not fix coherence | `mass_phase_embedding` | same weights `(9/25,16/25)`, amplitudes `(3/5, ±4/5)` |
| RDB-8, RDB-11, 004-C18 branch search | `obstruction_branch_search` | tiers `Phi1 > Gamma2 > Xi`, masses `2, 3/2, 1`, probabilities `(4/9,1/3,2/9,0,0)`; a worse `Phi1` is never rescued; the ranking orders the candidates' own points lexicographically, so `(2, 10)` precedes `(3, 0)` from `(3, 10)` although its mass is `1` against `10`; negative coordinates refused |
| 004-C17 packet-relative reconstruction obstruction | `terminalize_reconstruction` | complete imports are `Hosted`; missing ones are named, and there is no impossibility variant |
| RDB-9 coherence license does not license a lift | `evaluate_lift_candidate`, `licensed_coherence_lift` | with certified `(Phi1, Gamma2)` from a filled triangle, a complete license plus a `Phi1`-reducing move with declared carrier and replay is a lift; the reverse move, or no replay, is not |
| RDB-7, 004-C8, C10, C15, C16 no physical conclusion | `GomcReport` (one-variant `ReportAuthorityTag`) | `None` with and without channel and branch search, including a strict descent proposal |

**Corrections and scope.**

- Three of the five coherence-license fields are now computed rather than
  declared, and the observer basis is declared. The source's Lean took all
  five as booleans. The fifth, an internal policy flag, is not stored because
  it contributes no mathematical datum. A review found that a license or a lift checklist could be written
  by hand with every field true. Both now have private fields and come only
  from their evaluators, and the lift evaluator refuses negative coordinates.
- The branch search is exact rational lexicographic descent with no
  tolerances. The `f64` engine in `omega_engines` stays the production
  diagnostic and is not a claim source. A review found that the ranking
  followed the masses, which measure improvement in different coordinates
  and are not comparable across tiers. It now orders the candidates' points
  lexicographically.
- The GOMC-06 "universality" companion and the GOMC-08A/09A countermodels
  imported Mathlib in the source. Here they are replaced by the exact
  countermodels above.
- The report type contains no field for a physical conclusion. This is a
  software access restriction, not a theorem about observation or ontology.

**What stays outside.** The abstract thesis (004-C1) and the claim that GOMC
supersedes quantum formalism as Omega's base language (004-C22) are
interpretive, so they stay `ASSERTED` and `UNTYPED`. The stronger future
representation target (003-C17) is still `OPEN`. Physical QM does not follow
from GOMC (004-C23). The retired `f64` Plan002 surface (003-C16) is untouched.

### 11.5 A finite $M_2$ state-effect model (QM-005 consolidated and retired)

**Original paper in the paper archive:** [Finite quantum packet theorem for $M_2$](sources/original_papers/005_finite_quantum_packet_theorem_m2/finite_quantum_packet_theorem_m2.md) (standalone manuscript retired; mathematical core consolidated into Main Paper §11.7 and §11.5 here).

The paper's concrete construction is retained as finished infrastructure: the
state/effect deformation complex $d_0(A) = (0, [A,E], [A,\rho])$ and
$d_1(\delta p, \delta E, \delta\rho) = \delta p - \operatorname{Tr}(E\,\delta\rho) - \operatorname{Tr}(\delta E\,\rho)$
with $d_1 d_0 = 0$ by trace cyclicity in $M_n$, the completed exact classifier with
separating functionals, the distinction between infinitesimal tangent gauge directions
($\det(\rho + t \delta\rho) = -t^2$) and finite unitary conjugation, and the operational
interpretation of $H^1$ (demonstrated by the $\rho = I/2, E = |0\rangle\langle 0|$
example of hidden variation / observational ambiguity). `m2_quantum_packet` and
`gauge_cochain_complex` compute this verifier exactly over $\mathbb{Q}(i)$.

| Claim | Now computed by | Checked by (`native/tests/finite_m2_packet.rs`) |
| --- | --- | --- |
| C1 lead result | `verify`, `VerifiedM2Packet::{d1_d0, classify}` | every test below |
| C6 schema completeness | `verify` (only constructor of `VerifiedM2Packet`) | rejection reasons in declared order: missing field, carrier shape, non-PSD or non-unit-trace state, effect outside `[0, I]`, POVM not summing to `I`, non-trace-preserving channel, malformed Born entry; a packet with two faults is rejected for the earlier one |
| C8 cochain identity, Born defects land in `C^2` | `d0(A) = (0, [A,E], [A,rho])`, Born rows of `d1` | `d1 d0 = 0` as an exact matrix identity on the worked example and on a three-entry packet; the paper's hand commutators reproduced |
| C9 computability of `Phi_Q`, `Gamma_Q` (conditional) | `quotient_mass_l1`, `functional_trichotomy` | with the declared `l1` norm, `Phi_Q` is replayed by `omega_functional` and is zero exactly on `im d0` |
| C10 total, exclusive, witness-producing classifier | `classify` | `ExactRepair` with a gauge generator that reproduces `x`; `ClosedResidual` with a separator `lambda` (`lambda . d0 = 0`, `lambda . x != 0`); `ActiveClosureFailure` with the nonzero Born coordinate; same class as `omega_functional` on every residual tried |
| C12 worked example | `worked_example_packet` | `p = 1/2` is exact repair; `p = 3/4` puts `1/4` in the Born coordinate |
| C13 falsifiability conditions | as C8 and C10 | the tests are the falsification attempts the paper names |

**Corrections and scope.**

- The classifier's historical spellings `ExactClass`, `StabilizedSurvivor` and
  `OpenObstruction` map onto `omega_policy::trichotomy`'s
  `ExactRepair`, `ClosedResidual` and `ActiveClosureFailure`. No new class enum
  was created.
- With several Born entries, one gauge generator acts on every state and
  effect, and each entry contributes its own `d1` row. The identity
  `d1 d0 = 0` holds row by row by trace cyclicity.
- Membership in `im d0` is decided by `omega_linear_algebra`'s exact row
  reduction. Separators come from its kernel basis of `d0^T`.
- The Born-table refusal `InconsistentBornEntry` covers malformed entries only.
  A declared probability that disagrees with `Tr(E rho)` is a residual to
  classify, as the source's section PO-D19b (Born defect placement) requires,
  not a refusal.
- The row typed `REFUSAL` (C10) was a parse artefact. It is the classifier's
  totality claim and is now evidenced as a computation.

**What stays outside.** The complex carrier, the Born pairing and CPTP
discipline are declared packet fields (C2). The classifier mints no authority
(C3, C5). Schema completeness does not show that the schema is the only
possible one (C7). Coefficient fields beyond `Q(i)` are not implemented.

### 11.6 Conditions required for a finite quantum realization (QM-006 dropped from active derivation stack)

**Original papers in the paper archive:** [Quantum realization requires finite descent](sources/original_papers/006_quantum_realization_requires_finite_descent/quantum_realization_requires_finite_descent.md) and [Quantum realization spine](sources/original_papers/007_quantum_realization_spine/quantum_realization_spine.md) (both standalone manuscripts retired; QM-006 dropped from active derivation stack).

QM-006 is retired as an independent contribution to the derivation stack. Its
substantive ingredients belong to QM-001 (tower walk validator), QM-005 ($M_2$
deformation complex), and the transport papers. The dynamic observer factorization
criterion $O(x) = O(y) \implies O(Tx) = O(Ty)$ is preserved with QM-001 in WDP
Chapter 4 §4.2.2. The "survival theorem" packaging, comparative census of surviving
interfaces, six-role organizational map, and broad repair-capacity no-go are
retired. Most of their finite content restates what QM_001, QM_002 and QM_005 now compute: the
`M_2` complex and classifier, the registry-relative lift, the norm-branch
firewall and the scalar bridge. The rows below cite those tests. The papers
add four pieces of finite content of their own, now computed in
`descent_evidence_routes`, `repair_capacity` and the shared `exact_channel`.

| Claims | Now computed by | Checked by (`native/tests/finite_descent_interface.rs` unless noted) |
| --- | --- | --- |
| 006-C10, C11, C13 exact and scoped evidence routes are disjoint | `route_evidence`, `EvidenceRoute::class` | `(0,0)` with no tolerance is the only exact route; any declared tolerance, even zero, stays scoped; closed non-exact residuals (`Gamma = 0`, `Phi > eps`) stay scoped; open obstructions are rejected; routed on certified `M_2` values, where the gauge displacement is exact, the Born mismatch `(1/4, 1/4)` is rejected without tolerance and scoped with `(1/2, 1/2)` |
| 006-C24 projection-obstruction quotient | `finite_cochain_packet` dual witness | the `Phi1` dual circulation pairs to `3` with a nonzero class and keeps that value under every admissible repair |
| 006-C25, C26 repair-capacity recurrence and its conditional no-go | `RepairBudget`, `residual_lower_bounds`, `windows_to_exceed`, `satisfies_recurrence` | gap `1/2` from `(lambda, mu, eps) = (3, 2, 1/2)`: bounds `1, 3/2, 2, 5/2, 3`; threshold `10` exceeded after exactly `19` windows; a nonpositive gap implies nothing; violating trajectories detected |
| 007-C13 Kraus, Choi and Stinespring presentations agree on the pairing | `exact_channel::{ExactKrausChannel, apply_choi, apply_stinespring, choi_is_cptp}` | rational amplitude damping, a rational Pauli channel and a qubit-to-qutrit isometry: identical outputs from all three presentations, Choi PSD with `Tr_out J = I`, `V* V = I`, and equal Schrödinger and Heisenberg pairings |
| 007-C14 channel rejection cases | `ExactKrausChannel::try_new` | a non-trace-preserving family and an empty family are rejected; the transpose map's Choi matrix (the swap) is trace preserving but not PSD |
| 006-C5, C7–C9, 007-C19–C21 | `m2_quantum_packet` | see §11.5 (QM_005) |
| 006-C17, C18, C21, 007-C6, C18, C22, C25 | `tower_walk_validator` | see §11.2 (QM_001) |
| 007-C26 | `repair_quotient_bridge` | see §11.3 (QM_002) |

**Corrections and scope.**

- The body jumped from §9 to §25. Part IV (§16–§22) exists only as ledger
  rows. The recurrence of §18 and the arithmetic of §19's conditional no-go are
  implemented from those rows. The architecture complex of §16 is the general
  `finite_cochain_packet` machinery.
- The historical exact set also named `UniqueOutput`, which has no finite
  definition in either paper. It is not implemented.
- The Kraus, Choi and Stinespring toolkit is shared library code
  (`exact_channel`, with partial traces in `exact_hermitian`) rather than
  paper-local. The channels papers (QM_080–083) build on the same functions.
- 006-C22 ("scalable physical QC requires a repair-capacity packet") was
  untyped. Its finite content is the conditional recurrence, so it is now
  recorded as `CONDITIONAL`.

**What stays outside.** The six-role tower narrative, the continuum
approximation theorem (conditional on H1–H5, with H4 expected to fail), the
survival theorem (006-C19, C20; 007-C23, C24), the architecture-class no-go
(006-C27) and the comparative census (006-C30): all `OPEN` or `SCOPE FENCE`.
Whether any physical architecture has a persistent positive repair gap is the
open physical question. The recurrence only makes its consequence exact.

### 11.7 Inventory of finite and imported structure

**Original paper in the paper archive:** [Inventory of finite and imported structure](sources/original_papers/008_finite_descent_to_gtfoc_projection/finite_descent_to_gtfoc_projection.md).

QM_008 was a maintainer census. It proved no theorem. For each quantum
ingredient and each rival formalism it recorded the layer where descent to the
finite obstruction calculus stalls today. Three pieces of it are finite: the
descent bar itself, the stall witnesses of the Hilbert-carrier rivals, and the
contract a continuum object must meet to leave quarantine. The first two
compute in this crate, the third in `omega_wdp::coda::q`.

| Claims | Now computed by | Checked by (`tests/foundations/descent_census.rs` unless noted) |
| --- | --- | --- |
| 008-C4, C5 the descent bar: a certified `(Phi1, Gamma2)` and one class of a total, disjoint classification | `finite_cochain_packet::FiniteCochainPacket::classify` | a filled triangle sharing an edge with an unfilled one (`H^1 = 1`): a coboundary is `ExactRepair`; the unfilled cycle's edge is `ClosedResidual` with `Phi1 = 1`, and adding a coboundary does not change that; an edge of the filled face is `ActiveClosureFailure` with `Gamma2 = 1`; a wrong cochain length, a zero weight and a weight-count mismatch are refused before any class is assigned |
| 008-C8, C14, C16 where the Hilbert-carrier rivals stall | `composition_tomography`, `operational_axiom_selection` | two rebits: product effects span 9 of 10 joint directions, and the states `I/4 ± (J⊗J)/8` agree on all nine yet give `3/4` and `1/4` on the projector `(I + J⊗J)/2`; complex qubits span all 16; the quaternionic qubit has dimension 6 and its tensor carrier 28 against a product of 36; no real carrier of any size has dimension 9 and no quaternionic carrier has dimension 36; for every pair of dimensions from 2 to 5, declared local tomography keeps the classical simplex and the complex carrier, and drops the real carrier (deficit equal to the skew–skew sector) and the quaternionic one |
| 008-C10 the pairing does not select Born | `obstruction_management_calculus` | see §11.4 (QM_003 and QM_004) |
| 008-C11 CPTP monotonicity does not select the trace-norm normalization | `tower_walk_validator` | see §11.2 (QM_001) |
| 008-C17, C18 continuum-admission inputs | `omega_wdp::coda::q::continuum::ContinuumDebt`, `omega_wdp::coda::q::admission::QAdmissionGate` | `omega_engine/crates_rs/tests/omega_wdp/test_coda_q_qm_finite_shadow_membrane_admission.rs` checks that four fields are present; refinement and convergence remain declared strings, including `route-named-not-proved`, so this is input completeness rather than a convergence certificate |
| 008-C25 the physical-QC cluster is conditional | `repair_capacity` | see §11.6 (QM_006 and QM_007) |

**Corrections and scope.**

- The census called four Lean files machine-checked:
  `FiniteObstructionTrichotomy.lean`, `TerminalDisjointness.lean` and
  `ProjectionObstructionQuotient.lean` (C7), and `ContinuumNonPromotion.lean`
  (C19). None of them is in this repository, and neither is the
  `PairingNonSelection` target. C7 and C19 stay `ASSERTED`. The Rust
  computations above are not Lean checks.
- The stall witnesses were already computed by `composition_tomography` and
  `operational_axiom_selection`. No second implementation was written. The new
  test adds one sharper point and one guard. The sharper point: no real
  carrier of any size has the two-rebit product dimension 9, and no
  quaternionic carrier has 36, so neither stall depends on choosing the tensor
  carrier. The guard: a dimension count is only necessary. Two real qutrits
  give `6 · 6 = 36 = dim Sym(R^8)`, yet their product effects span only 36 of
  the 45 symmetric directions of the tensor carrier `R^9`.
- Local tomography keeps the classical simplex as well. On its own it selects
  complex QM among the three Hilbert carriers, not among all four rivals. The
  census's registry-relative reading is the right one.
- `omega_wdp::coda::q` checks that the four membrane ingredients are declared. It does
  not verify a refinement relation or a convergence certificate. Those are
  declared strings, and the fixture's route says `route-named-not-proved`.
- The quaternionic refusal is attributed to the lack of a canonical tensor
  product. That reason is recorded, not computed. The dimension witness is
  computed.
- The GPT square-bit, Spekkens and threshold rows name no finite object this
  crate holds. They are not implemented.

**What stays outside.** The per-ingredient depths of §2 summarize other
papers' rows. They move when those rows move: C9 with QM_020, C12 with QM_073
and QM_120, C13 with QM_031. The full-descent definition (C6) names tower
layers no code models. The uniqueness conjecture (C15, Appendix A), the open
Lean targets (C22) and the missing prototypes (C23) stay `OPEN`. The ontology
paragraph (C20, C21) and the two-track hand-off (C26) are not finite
statements.

### 11.8 Hilbert-space cochains and cohomology

**Original paper in the paper archive:** [Hilbert space cochains and quantum cohomology](sources/original_papers/010_hilbert_space_cochains_qm_cohomology/hilbert_space_cochains_qm_cohomology.md).

The paper declared an adapter from a residual into a cochain complex and
a four-way admission rule for the residual it carries: exact, closed but not
exact, closure failure, or refused. It added a non-selection result: classical
and quantum realizations can land in the same class. The rule now runs in
`cohomology_admission`, on top of `omega_functional`'s validated complex
`ExactCochainComplexQ`, and every outcome carries a certificate that is
replayed independently.

| Claims | Now computed by | Checked by (`tests/foundations/hilbert_cochain_admission.rs`) |
| --- | --- | --- |
| 010-C1, C3 adapter and four-way admission | `cohomology_admission::{admit, verify_admission}` | on a path, `(2, 3) = d0 (0, 2, 5)` is exact with a replayed preimage; on a 4-cycle, a single-edge cochain is closed but not exact, with the circulation as separator; on a filled triangle, an edge is a closure failure with defect `1`; a residual with no declared adapter and an ill-typed cochain are refused; tampered preimages, separators and defects are rejected, and a separator cannot certify an exact cochain; on six residuals of a mixed complex the admission class equals the `Phi1`/`Gamma2` trichotomy class |
| 010-C2 `im d0` lies in `ker d1` | `ExactCochainComplexQ::try_new` | a declaration with `d1 d0 = (-1, 1)` is refused; every basis coboundary of the mixed complex is closed and admitted as exact |
| 010-C4 `d1 = 0` gives `H^1 = Q^1` | `cohomology_dimensions` | on the path, 4-cycle, filled triangle and mixed complex, `dim Q^1 - dim H^1 = rank d1`, so the two agree exactly when `d1 = 0` |
| 010-C5 cohomology does not select quantum mechanics | `admit` reads only `(s, d0, d1)` | a classical realization (vertex distributions, one column-stochastic transport) and a quantum one (vertex states, one rational rotation channel, readout `\|0><0\|`) give identical residual cochains in every class: exact with identity transports, closed but not exact with the transport on the unfilled cycle, closure failure with it on the filled face (defect `-12/25` in both); their sources differ, since dephasing the vertex states removes the quantum residual, which came from coherence, while the classical one, from the transport, stays |
| 010-C6 a quotient obstruction is an `H^1` class only when closed | `image_preimage`, `admit` | an edge of the filled triangle lies outside `im d0` with `Phi1 = 1`, yet it is a closure failure, not a class of `H^1`; declaring no 2-cells makes the same cochain closed but not exact; with no declared `d1` the complex is refused (`MissingComplex2`) |

**Corrections and scope.**

- `m2_quantum_packet` (QM_005) carried its own copy of this classifier. It now
  calls `cohomology_admission::admit` and maps the certificates onto its gauge,
  separator and Born-defect witnesses.
- Membership in `im d0` is decided by exact row reduction and certified by a
  preimage or a separator. On a finite complex the image is closed, so this
  agrees with `Phi1 = 0`. The test checks the agreement rather than assuming
  it.
- The source side and the imported quantum side of the bridge are not a Rust
  type. They enter only through the residual they produce and through whether
  an adapter was declared.
- The complex is over `Q`. QM_120's Mermin–Peres parity target is a mod-2
  cochain. The promotion rule (C6) reads the same over any field, but
  membership over `Q` and over `GF(2)` can differ, so the rule is checked here
  over `Q` only.
- C2 was `OPEN` only because its Lean target was never mechanized. Every
  accepted complex satisfies it by construction, and it is now recorded as
  `FINITE COMPUTATION`.

**What stays outside.** The architecture reading (C7) and the nonclaims (C8).
The discriminators the paper lists as imported (complex phase, nonclassical
composition, Born readout, channel transport, contextuality) are not derived
from cohomology here either. The Lean targets PL-QM032-1 to 3 remain
unmechanized.

### 11.9 The state–effect pairing

**Original paper in the paper archive:** [State-effect pairing audit](sources/original_papers/011_state_effect_pairing_audit/state_effect_pairing_audit.md).

The paper grades candidate probability pairings on declared finite packets by
one set of checks and gives each a typed terminal. Its headline is a
non-result: the checks do not select the Born pairing. `pairing_audit` now
holds the audit, for any bilinear pairing or, as a nonlinear control, a
polynomial of the dot product. It builds the seven registry rows on exact
carriers and replays every check from the declared data.

| Claims | Now computed by | Checked by (`tests/foundations/state_effect_pairing_audit.rs`) |
| --- | --- | --- |
| 011-C2, C4 the audit: compatibility is passing the declared checks | `pairing_audit::{PairingPacket, audit_row}` | normalization, positivity and transport coherence on every row, plus local tomography (the rank of the product effects, computed from the declared effects) and local-to-global agreement where a composite is declared; a marginal of the wrong length or a table that does not sum to one fails gluing; a transport whose declared dual is the map itself rather than its transpose fails the transport check and nothing else; malformed packets are refused |
| 011-C5 to C8, C10, C11 the seven rows | `pairing_audit::declared_registry` | classical simplex (dot pairing, a column-stochastic transport, a fully correlated table): passes; square bit (affine pairing, a quarter-turn transport, no composite): refused; Spekkens bit (overlap pairing, an ontic permutation, one correlated table over 16 ontic pairs): passes; real rebit (imported trace pairing, a rational rotation): its declared tensor composite has product effects of rank 9 in a 10-dimensional joint space; complex qubit (imported Born pairing, four measurements including a three-outcome POVM and the `Y` basis, Hadamard transport, Bell-state tables): its product effects span all 16 joint directions and it passes, while without the `Y` basis they span 9 and local tomography fails; quaternionic qubit (positivity through its complex `4 x 4` representation, conjugation by `diag(1, j)`, states spanning 6 real dimensions): refused, no composite declared; nonlinear control `2 (e.s)^2 - e.s`: fails normalization, positivity, transport and gluing |
| 011-C9 the complex local replay | `complex_born_row` | every declared check passes; there is no sealed terminal in the crate, so the row's open part stays open |
| 011-C3, C12, C13 non-selection | `transport_gram_row`, `noisy_born_row` | on the classical packet, the pairing `e^T T s` through the declared transport passes every check and gives `2/3` where the dot pairing gives `1`; on the complex packet, `Tr(E N(rho))` for the Pauli channel with Kraus operators `I/3, 2X/3, 2Z/3`, which commutes with Hadamard conjugation, passes every check, Bell tables included, and gives `5/9` where Born gives `1` |
| 011-C13, C14 probability is effect-relative | `PairingPacket::value` | the state `\|0><0\|` gets `1` from `\|0><0\|` and `1/2` from `\|+><+\|`; the worked example: `(1, 1)` and `(2, 0)` both total 2, and `<1, 1> = 1 != 2 = <2, 1>` |
| 011-C15 CPTP monotonicity does not select the trace norm | `tower_walk_validator` | see §11.2 (QM_001) |

**Corrections and scope.**

- The paper named carriers and checks but no samples. The states, effects,
  measurements, transports and joint tables are declared here on exact
  carriers, so each terminal replays explicit data. A different declaration
  could get a different terminal. The audit is registry-relative, as the paper
  says.
- Checks 6 (quotient non-promotion) and 7 (finite replay) are not separate
  computations: every terminal is recomputed from its packet and says nothing
  beyond it. The scoped terminalizer `Pi_sharp` is not modelled, and no row is
  sealed.
- The paper's non-selection witness was the arithmetic `(1, 1)` against
  `(2, 0)`. The audit now puts a second pairing on the actual classical and
  Born packets, and it passes the whole skeleton, transport and gluing
  included. The finite checks cannot tell Born from Born composed with a
  Hadamard-symmetric channel. A further declared axiom, for example that a
  pure state gives probability 1 on its own projector, would.
- The paper's body and ledger name the rebit terminal differently ("failed"
  and "conditional ... local tomography issue"). The audit reports
  `LocalTomographyFails { 9, 10 }`: the single-system checks pass, and the
  declared tensor composite fails local tomography.
- The audit computes the product-effect rank from each row's own declared
  effects. An earlier version took the rank from `composition_tomography`'s
  full bases, so a row could pass on numbers it did not earn; the complex
  packet then needed the `Y` basis, whose imaginary off-diagonal its other
  effects lack.
- Quaternions enter through the standard complex representation
  `q = z + wj -> [[z, w], [-conj w, conj z]]`, so positivity is the crate's
  exact PSD decision on `4 x 4` complex matrices.
- The Lean module `QM.PairingNonSelection` that the paper cites is not in this
  repository. C13 now rests on the exact countermodels above.

**What stays outside.** The proposed gluing theorems (C1) are prose and are not
mechanized here. The open conclusion in C9 has no mathematical implementation
in the crate. The downstream trace-norm and interface audits
(O025, O026) belong to their own papers.

### 11.10 Density matrices as diagonal residual weights

**Original paper in the paper archive:** [Density matrices as diagonal residual weights](sources/original_papers/012_density_matrices_as_diagonal_residual_weights/density_matrices_as_diagonal_residual_weights.md).

The paper read a finite residual-weight distribution as a diagonal density: it
is a state, its purity `sum p^2` is one exactly on one sector, and coherence is
a lift the weights do not force. QM_003's `residual_density_calculus` already
held the ledger, the diagonal density and the purity. The paper's own
statements are now checked against it.

| Claims | Now computed by | Checked by (`native/tests/diagonal_residual_density.rs` unless noted) |
| --- | --- | --- |
| 012-C1, C3, C6, C7 carrier, diagonal density, worked example, mixedness | `residual_density_calculus::ResidualLedger::{weights, diagonal_density, purity}` | `w = (3, 1)` gives `diag(3/4, 1/4)` with purity `5/8` and mixedness `3/8`; `w = (4, 0)` gives `p = (1, 0)` and purity `1` |
| 012-C5 the theorem: a state, with purity in `(0, 1]` and one exactly when pure | `ResidualLedger` | all 81 ledgers with masses `0..3` on one to three sectors: PSD (exact `LDLᵀ`), trace one, `tr(rho^2) = sum p^2` in `(0, 1]`, equal to one exactly when one sector carries the mass; the zero ledger is refused |
| 012-C4 same density iff same normalized weights | `ResidualLedger::diagonal_density` | `(3, 1)`, `(6, 2)`, `(15, 5)` and `(21, 7)` give one density; `(1, 3)` and `(2, 2)` do not |
| 012-C9 the diagonal is basis-relative | `residual_density_calculus::{conjugate, sector_measurement}` | the rational rotation `[[3/5, -4/5], [4/5, 3/5]]` turns `diag(3/4, 1/4)` into populations `(43/100, 57/100)` with coherence `6/25`; `tr(rho^2)` stays `5/8` while the diagonal's own purity becomes `2549/5000` |
| 012-C8 coherence is not a function of the weights | `residual_density_calculus` | see §11.4 (QM_003 and QM_004) (`native/tests/residual_density_boundary.rs`) |

**Corrections and scope.**

- No new module was needed: the ledger, density and purity were QM_003's
  code. This paper's rows now cite tests of their own statements.
- The theorem was cited as mechanized in `QM.DiagonalDensity` (ENC-1126). That
  Lean file is not in this repository, and `FiniteDensity.lean` in
  `lean4/quantum_mechanics/` is a different, two-level module. C5 is recorded
  as `FINITE COMPUTATION`: an exhaustive check on declared ledgers, with the
  general statement proved in prose.
- The basis-relativity row (C9) was interpretive. It now has a computed
  witness, and the same witness separates the purity of the state from the
  purity of its diagonal.

**What stays outside.** The descent from sector populations (C2), the
nonclaims (C10) and the firewall (C11) are fences. Channel dynamics on the
density (rung 4) belong to the channels papers.

### 11.11 Born normalization and the conditional Hilbert lift

**Original paper in the paper archive:** [Conditional Hilbert lifts and Born normalization redundancy](sources/original_papers/020_born_normalization_and_conditional_hilbert_lift/born_normalization_and_conditional_hilbert_lift.md).

The paper separated three things: normalizing sector weights, which already
gives a unit-sum profile; lifting them to amplitudes `sqrt(w) e^(i theta)`,
which returns the same profile; and uniqueness of the quadratic rule, which
needs Gleason's imported hypotheses. Most of its theorems land on modules that
already existed. The new piece is `phase_averaged_shadow`, which replaces the
paper's Monte Carlo phase average with an exact average over a declared finite
phase group.

| Claims | Now computed by | Checked by (`native/tests/born_normalization_lift.rs` unless noted) |
| --- | --- | --- |
| 020-C1 Theorem 1, direct normalization | `residual_density_calculus::ResidualLedger::weights` | `(2, 1, 1)` normalizes to `(1/2, 1/4, 1/4)`; normalizing again and scaling by 3 change nothing; another ray gives another profile |
| 020-C2 Theorem 2 and Proposition 2.1, additive aggregation | `finite_cochain_packet::FiniteCochainPacket::quotient_mass` (`Phi1` from `omega_functional`); exact rational arithmetic | the crate's `l1` quotient mass adds over disjoint blocks: a triangle cochain of mass `7` and a square cochain of mass `17` join to mass `24` on the disjoint packet, and a second pair adds the same way; `D1(x, y) = abs(x) + abs(y) - abs(x + y)` is nonnegative and zero exactly when `x y >= 0`, on all pairs in `[-6, 6]^2`; the squared `l2` norm of the join of `(3, 4)` and `(5, 12)` is `194 < 18^2`, and the `l2` defect ratio is at most 2, with equality exactly at equal norms (arithmetic in the test; the crate has no global `l2` norm) |
| 020-C3 Theorem 3, row-sparse descent | `phase_blind_quotient::classify_descent` | CNOT and a monomial unitary with entries `i` and `(-3 + 4i)/5` descend; a rational rotation and `[[1, 1], [1, 1]]` do not |
| 020-C4 Theorem 4, lift redundancy | `mass_phase_embedding` | the lift `(2, 1, 1)` of `w = (4, 1, 1)` reads back `w`; see also §11.15 (QM_031) (`finite_path_sum_graded_transport.rs`) |
| 020-C5, C9 Theorem 5 and the worked replay, the phase-averaged shadow | `phase_averaged_shadow::{phase_group_average, averages_to_dephasing}` | averaging `D rho D*` over the sign group and over the quarter turns equals the dephasing channel on every matrix unit for `n = 1, 2, 3`, hence on every matrix; the trivial group leaves coherence; for `w = (4, 1, 1)` and readout `u = (1, -1/2, 1/4)` the mean readout over all 64 quarter-turn phase choices is `4 + 1/4 + 1/16`, as is `u* avg(c c*) u`; for the paper's `w = (2, 1, 1)` the shadow is exactly `37/16` |
| 020-C6 Theorem 6, part 1: weights do not force a Hilbert space | `pairing_audit` | the classical simplex passes the same checks as the Born packet, and a second pairing passes on the Born packet itself (`state_effect_pairing_audit.rs`) |
| 020-C7 Theorem 6, part 2: the conditional Gleason route | `born_gleason` | its own tests: dimension 2 and real scalars are refused, a matching frame in dimension 3 is accepted |
| 020-C8 Theorem 7, redundant for probability but not for dynamics | `coherent_interference` | see §11.26 (QM_061) |

**Corrections and scope.**

- The phase-averaged shadow was checked by a `3 x 10^5`-sample Monte Carlo
  estimate (about `2.313`). The average is now exact over a declared finite
  phase group. Because the average is linear, checking it on the matrix units
  decides it for every matrix, including the irrational lift of `(2, 1, 1)`.
  The value is `37/16`. The continuous Haar measure is not computed.
- Theorem 3's row-sparsity criterion holds with the zero vector kept as a
  point of the quotient; QM_060's entry records why `[[1, 1], [1, 1]]` needs
  that.
- The paper's Lean, `BornRedundancy.lean` and its axiom-printing companion,
  now lives in `lean4/quantum_mechanics/`. Its report was produced on
  `v4.34.0`. A Mathlib-free staging build on the workspace toolchain
  `v4.33.1` compiled it with the same axioms (`propext`, `Classical.choice`,
  `Quot.sound`; `descent_compatible_iff_row_sparse` without
  `Classical.choice`). That is a build, not a receipted replay, so the rows
  rest on the Rust tests. Its row-sparsity theorem covers `2 x 2` matrices.
- The ledger rows cited `PaperQF002` declarations in a Lean tree that is not
  in this repository; they now cite the computations above. Theorem 6 part 1
  was backed by a `True := by trivial` stub; it now has a countermodel.
- The paper's Python (`choi_certifier.py`, `dephasing_channel.py`,
  `schatten_norms.py`) used floats. The exact counterparts are
  `exact_channel` (Choi, Kraus and dephasing) and this entry's tests.

**What stays outside.** Strict `l^p` subadditivity for real `p > 1` is the
imported Minkowski fact. Gleason's theorem [1] (Theorem 6, part 2) stays
imported. The branch-localization and many-worlds remarks (C10) and the
packaging assertion are open prose. The note
`research/frame_function_finite_map.md` computes the linear half of the
Gleason statement, with nullity zero, on the Cabello prefixes of 3, 6 and 9
bases and on the 24-ray Peres set, and gives a trace-one rational form that is
nonnegative on every declared ray and is not positive semidefinite; it does
not replace the import.

### 11.12 Measurement update as idempotent conditioning (QM-021 merged and retired)

**Original paper in the paper archive:** [Selective measurement update as idempotent conditioning](sources/original_papers/021_measurement_update_as_idempotent_conditioning/measurement_update_as_idempotent_conditioning.md) (standalone manuscript retired to redirect stub; reduced to one finite conditioning-and-composition lemma beside normalized weights).

The paper cast a selective measurement on finite outcome weights as conditioning on a declared outcome sector: keep the sector and renormalize. The surviving mathematical core is a single finite conditioning-and-composition lemma:

**Proposition (Finite conditioning and compatible composition).**
For nonnegative weights $w_i$, a declared event $S$, and positive sector mass $Z_S = \sum_{i \in S} w_i > 0$, define the normalized conditioned weights:
$$
C_S(w)_i = \frac{\mathbf{1}_S(i) w_i}{Z_S}.
$$
Then $C_S(w)$ is normalized ($\sum_i C_S(w)_i = 1$), supported on $S$, and satisfies idempotence:
$$
C_S(C_S(w)) = C_S(w).
$$
The event $S$ has probability one after this update ($\sum_{i \in S} C_S(w)_i = 1$). The original event probability is the prior sector mass fraction $p_S(w) = Z_S / \sum_i w_i$. Furthermore, compatible composition holds for arbitrary events on the same classical carrier:
$$
C_T(C_S(w)) = C_{S \cap T}(w) = C_S(C_T(w))
$$
whenever the intersection has positive mass $Z_{S \cap T} > 0$, since the intermediate normalizations cancel directly.

| Claims | Now computed by | Checked by (`native/tests/measurement_conditioning.rs`) |
| --- | --- | --- |
| 021-C1, C3, C4, C6, C7 carrier, update, fixed points, worked example, removed mass | `sector_conditioning::{condition, sector_probability}` | `w = (3, 1)`, `S = {1}`: probability `1/4`, update `(0, 1)`, idempotent, recurrence `1`, removed share `3/4` |
| 021-C5 the theorem: collapse, idempotence, repeatability, Born share | `condition`, `sector_probability` | every ledger with masses `0..3` on three outcomes against every nonempty sector: zero off the sector, idempotent, probability one afterwards, probability `Z_S / sum w` before; exactly the weights already normalized on the sector are fixed; a sector with zero weight is refused |
| 021-C8 the measurement is a declared partition | `condition` | conditioning on a sector and then on a subsector equals conditioning on the subsector; the same weights `(3, 1, 2)` update to `(3/4, 1/4, 0)` under one declared sector and to `(0, 1/3, 2/3)` under another |
| 021-C12 Lüders on diagonal densities is conditioning | `sector_conditioning::{luders_update, sector_projector}` | `P rho P / Tr(P rho)` on every diagonal density above equals the diagonal of the conditioned weights, and both refuse the same null sectors |
| 021-C10 within-sector coherence is outside | `luders_update` | on `J/3` the sector `{0, 1}` keeps coherence `1/2` between its outcomes; conditioning the diagonal gives the same diagonal and no coherence |
| 021-C9 incompatible measurements are outside | `luders_update` | on `I/2`, updating by `|0><0|` then `|+><+|` gives `|+><+|`, the other order gives `|0><0|`; compatible sector projectors commute; non-projectors and wrong sizes are refused |

**Corrections, qualifications, and boundaries.**

- **Zero-probability conditioning is undefined:** When $Z_S = 0$, the conditioning rule $C_S(w)$ is undefined; there is no missing state to manufacture.
- **Normalized update is nonlinear:** The normalized update $C_S$ is an idempotent nonlinear retraction onto a face of the probability simplex. The raw indicator mask $w \mapsto \mathbf{1}_S w$ is the linear projection. This distinction separates the classical conditioning lemma from a linear Hilbert-space projector.
- **Idempotence does not derive the quantum Lüders update:** The paper acknowledged that it establishes only the diagonal outcome-weight update, without deriving the full density-matrix Lüders rule $\mathcal{I}_S(\rho) = P_S \rho P_S$. If $P_S = \sum_{i \in S} P_i$ contains at least two one-dimensional sectors, compare the Lüders operation $\mathcal{I}_S^L(\rho) = P_S \rho P_S$ with the dephasing update $\mathcal{I}_S^D(\rho) = \sum_{i \in S} P_i \rho P_i$. Both have outcome probability $\operatorname{Tr}(P_S \rho)$, both produce states supported on $S$, and their selective updates are idempotent and repeatable. Yet they differ on coherence within $S$ ($\mathcal{I}_S^L$ preserves within-sector coherence, while $\mathcal{I}_S^D$ destroys it). Proving that ordinary conditioning is idempotent does not select the quantum state-change instrument.
- **Crate implementation:** The crate module `omega_engine/crates_rs/omega_quantum_physics/src/sector_conditioning.rs` contains exact conditioning, full Lüders updates for declared projectors, and the nonselective Lüders channel, verified by `native/tests/measurement_conditioning.rs`. Standalone paper QM-021 is retired; its elementary extensions are closed and not reopened as research projects.

**What stays outside.** The measurement problem, the projection postulate as ontology, and preferred-basis selection (C10) are not addressed; the fence has a computed witness for coherence. The descent from a measured state (C2) and the firewall (C11) are fences. The operational conditions selecting a state-update instrument remain open wherever selection is intended.

### 11.14 Finite weighted transport calculus (QM-030 extracted and retired)

**Original paper in the paper archive:** [Finite weighted transport calculus](sources/original_papers/030_finite_weighted_transport_calculus/finite_weighted_transport_calculus.md) (standalone synthesis retired to redirect stub; finite path-sum transfer identity extracted, and gauge/holonomy corrections merged into the general obstruction framework).

The paper proposed a finite weighted transport calculus: histories on a finite graph weighted in a commutative semiring, coupled to a cochain layer that carries phase and closure. The surviving core is a single finite path-sum/transfer-matrix identity under a unique-cut decomposition:

**Proposition (Path sums with a unique cut).**
Let $X_0, \ldots, X_n$ be finite layers of carriers. For transitions between adjacent layers, define the transfer matrix in a commutative semiring:
$$
A_k(y, x) = \sum_{e: x \to y} w(e).
$$
Then:
$$
\sum_{\gamma: a \to b} \prod_{e \in \gamma} w(e) = (A_{n-1} \cdots A_0)_{ba}.
$$
This is finite distributivity over a commutative semiring; no inner product, metric, or Hamiltonian generator is required. The essential structural condition is that every allowed history crosses the chosen intermediate cut exactly once. Graded structure alone is insufficient if transitions can skip layers, nor does a finite graph automatically have finitely many paths if cycles are present.

| Claim | Now computed by | Checked by (`tests/dynamics/weighted_transport_calculus.rs`) |
| --- | --- | --- |
| QM-030-C3 T1 graded path-sum | `graded_path_sum::TimeSlicedTransport::{path_sum, propagator, sliced_composition}` | enumeration, the transfer-matrix product and the cut at every slice agree over `Boolean`, `NonNegative`, `i64`, `GaussianWeight` and formal phase sums; hand value `T2 T1 T0 = [[16, -2], [-6, 6]]` |
| QM-030-C4 ungraded overcount | `graded_path_sum::TransportGraph::{all_histories, total_path_sum, ungraded_split_sum}` | on `a -> b -> c` the split sum is `3 Z` (45 against 15; 3 against 1 with unit weights) while the graded cut gives `Z`; with paths of lengths 2 and 1 it is `sum (l + 1) w = 32` against `Z = 13`; the same tree has `h1 = 0` and `Phi1 = Gamma2 = 0` in `finite_cochain_packet`, which is vacuous; on the unfilled triangle (`h1 = 1`) a circulation and its triple share the class `ClosedResidual` while the mass goes from `3` to `9`, so the class is blind to the overcount factor and the mass is not |
| QM-030-C6 T2 finite transfer shadow | `TimeSlicedTransport::propagator` | the identity holds over `Boolean` and `NonNegative`, which have no subtraction; the generator `T - I` of a stochastic `T` has diagonal `-1/2, -1/3`, which `NonNegative` refuses |
| QM-030-C9, C10 T3 phase as a gauge obstruction | `u1_gauge_triviality::trivializing_gauge`, using the spanning-forest fixing of `holonomy_interference` | exponentials of coboundaries return a gauge `g` with `A = 1^g`; cycle sum 3 returns a closed walk with holonomy `u^3`, replayed by `U1Connection::holonomy`; under `u = i` a cycle sum of 4 is pure gauge although `Phi1 = 4`; filling the face turns the same flux into curvature (`Gamma2 = 3`); coboundary step phases telescope to a single phase |
| QM-030-C20 cancellation needs signs, not `C` | `TimeSlicedTransport::path_sum` | on a two-history diamond all 16 Boolean and 256 nonnegative assignments vanish exactly when both histories are blocked; `1 + (-1) = 0` over `i64` |
| QM-030-C25 worked example | the rows above | (i) the 3:1 count, (ii) the cancellation, (iii) the loop `a -> b -> a`: `Exp(d0 f)` has holonomy 1 and is pure gauge, flux 2 gives `u^2` and a witness |

**Corrections and scope.**

- **The overcounting example and cohomological blindspot:** On the path $a \to b \to c$, splitting the history at $a$, $b$, and $c$ counts it three times ($\sum_\gamma (|\gamma|+1)w(\gamma)$), whereas a single intermediate cut counts it once. Crucially, the vanishing of cohomological obstruction ($H^1 = 0$) on that graph does not certify that a path decomposition counts each history exactly once.
- **Phase section corrections (periodicity and action):**
  1. *Exponentiation loses integral periods:* The claim that $w = \exp(a)$ is gauge-trivial if and only if $a = d^0 \varphi$ fails in the forward direction. On edges $0 \to 1$, $1 \to 2$, and $0 \to 2$ with angles $\theta_{01} = \theta_{12} = 0, \theta_{02} = 2\pi$, all multiplicative phase weights $e^{i\theta_e} = 1$ are gauge-trivial, yet the angle assignment is not an additive coboundary without winding: $\theta = d^0 \varphi + 2\pi k$ with $k \in \mathbb{Z}^E$. The correct multiplicative criterion on a graph is trivial phase holonomy around every cycle.
  2. *Globally defined path action need not be an endpoint potential:* A globally defined action $S[\gamma]$ additive under concatenation can assign different values to different paths between identical endpoints (interference). Only when $S[\gamma] = V(\operatorname{end}\gamma) - V(\operatorname{start}\gamma)$ does the action telescope to endpoint potentials. "Endpoint potentials telescope" is retained; the blanket classification of dynamical phase as an exact coboundary is discarded.
- **Retired structural syntheses & non-selections:**
  - Proving that the transport tuple is a "weakest host", turning "equipment" into formal categorical equipment, and extending the interface census are retired as requirements for finite QM.
  - *Dagger compactness does not select complex Hilbert space:* Real inner-product spaces and relational categories provide counterexamples and are explicitly dagger-compact.
  - *Cancellation does not force $\mathbb{Z}$-embedding:* In $\mathbb{F}_2$, $1+1=0$ exhibits cancellation without embedding $\mathbb{Z}$.
  - The repeated pairing, density, quotient, and terminalization sections point to their existing homes in WDP and QM-002..006.

**What stays outside.** C1, C2, C5, C8, C11, C16, C18, C19, C21, C23 and C24 are fences or retired synthesis prose. C7 stays a refusal; its finite witnesses are in QM_034 and QM_035. Born terminalization and pairing non-uniqueness (C12, C13) belong to the state–effect pairing audit, the trace-norm firewall (C14) to the norm-selection papers, and C22 collects results owned by other papers. Dagger-compact comparison and uniqueness of the host stay open. Standalone QM-030 is dismantled and retired.

### 11.15 Finite path sums as graded transport

**Original paper in the paper archive:** [Finite path-sum as graded transport](sources/original_papers/031_finite_path_sum_as_graded_transport/finite_path_sum_as_graded_transport.md).

The paper split a sum over histories into a graded skeleton (matrix powers), a
phase lift (interference) and an imported continuum, and took a position that
quantum probability is L1 normalization. The skeleton and the finite facts
under the position now compute exactly; the continuum and the framing stay
outside.

| Claim | Now computed by | Checked by (`tests/dynamics/finite_path_sum_graded_transport.rs`) |
| --- | --- | --- |
| QM-031-C5 path-sum `= M^n`, Chapman–Kolmogorov | `graded_path_sum::TransportGraph::unroll`, `semiring_matrix::{power, multiply}` | length-`n` path-sums equal `M^n` for `n <= 4` over five semirings on a 3-state `M` with loops and a zero entry; `M^4 = [[25, 20, 36], [18, 25, 30], [10, 12, 25]]`; `M^(m+n) = M^m M^n` for `m, n <= 3`; every cut of the five-step transport gives `(M^5)[2][0] = 35` |
| QM-031-C6 swap example | `semiring_matpow`, `TimeSlicedTransport::histories` | `M^2 = I`, `M^3 = M`; the only weighted length-2 walk from 0 to 0 passes through 1 |
| QM-031-C11 probability is L1 normalization | `TimeSlicedTransport::path_sum` over `NonNegative`; `mass_phase_embedding` | the columns of a stochastic path-sum sum to 1 for `n <= 5`; history weights `1/4, 1/3` normalize to `3/7, 4/7` |
| QM-031-C12 the Born square is redundant | `mass_phase_embedding::MassPhaseEmbedding` | `born_weights = probabilities = (1/9, 4/9, 4/9)` for two phase declarations; the normalized squared moduli of the exact amplitudes return the same law |
| QM-031-C9, C13 interference is the non-L1 part | `TimeSlicedTransport<GaussianWeight>::path_sum` with `u1_graph_connection` | two histories with diagonal weights `(1, 1)` have coherent intensity `Z conj(Z)` = 4, 0 or 2; on a diamond `Z conj(Z) = 2 + 2 Re Hol = 4096/1105`, and a vertex gauge moves `Z` by `g(d) conj(g(a))` only |

**Corrections and scope.**

- C5 cited Lean modules (`QM.FinitePathSum`, ENC-1128; `FinitePathSumReplay`,
  ENC-1072) that are not in the tree; the library certificate for the latter
  records its source as missing. The identity is now checked in Rust on
  declared instances, over any semiring rather than a fixed one.
- The phase carrier is a declared Gaussian-rational connection. The chosen
  positive-real square-root lift requires rational-square probabilities.
  A Gaussian-rational lift can sometimes exist without a rational real lift;
  the more general criterion is stated in §11.25.
- "The only place the amplitude lift departs from the classical path-sum" is
  interpretation. What is computed is that equal diagonal weights allow
  different coherent intensities, and that the two-path cross term is twice
  the real part of the loop holonomy.

**What stays outside.** C1–C4 are definitions, C7, C16 and C18 fences, C8 and
C15 the interpretive decomposition and position, and C10 and C14 declared
imports (the `U(1)` carrier and Gleason's route to Born uniqueness). C17, the
population shadow of a CPTP channel, belongs to QM_082. No continuum measure
is constructed.

### 11.16 A finite Feynman-history model

**Original paper in the paper archive:** [Finite Feynman-history model](sources/original_papers/032_gtta_feynman_finite_shadow_histories/gtta_feynman_finite_shadow_histories.md).

The paper admitted a continuum path integral only as the certified limit of
finite time-sliced shadows. The finite shadow now replays exactly: histories
are enumerated once each, actions are exact rationals, and the kernel is kept
as a formal sum of phases, so `1 + 2e^i` is an exact object rather than a
decimal. Comparing shadows exactly shows that the paper's own free-particle
family is torn by refinement.

| Claim | Now computed by | Checked by (`tests/dynamics/feynman_finite_shadow_histories.rs`) |
| --- | --- | --- |
| QM-032-C3 the finite shadow is replayable | `time_sliced_action_shadow::FreeParticleShadow::{replay, transfer_kernel}` on `graded_path_sum` | two slices on `{-1, 0, 1}`: three histories with actions 1, 0, 1 and kernel `1 + 2e^i`; three slices: nine distinct histories and `1 + 6e^i + 2e^(3i)`; enumeration equals the transfer-matrix product; the carrier `{-1, -1/2, 0, 1/2, 1}` and half steps give `1 + 2e^(i/4) + 2e^i` and `1 + 2e^(2i)`; mass 3, `hbar` 2 and `Z = 3` give `(1 + 2e^(3i/2))/3` |
| QM-032-C8, C9 declared packet and replay | `FreeParticleShadow::new` | non-increasing times, an empty or repeated carrier, endpoints off the carrier, non-positive mass or `hbar` and a zero normalization are refused before any replay |
| QM-032-C10 worked example | `time_sliced_action_shadow::PhaseSum::evaluate` | the kernel is `{0: 1, 1: 2}`; a number exists only at a declared unit: `(11 + 8i)/5` at `u = (3 + 4i)/5`, `(11 + 48i)/25` with quantum 1/2, `1 + 2i` at `u = i`; an incommensurate quantum, a zero quantum and a non-unit `u` are refused |
| QM-032-C4, C13 refinement compatibility | `time_sliced_action_shadow::refinement_residual` | the coarse partition `(0, 2)` gives 1 and the fine `(0, 1, 2)` gives `1 + 2e^i`: residual `2e^i`, and normalization 3 leaves `-2/3 + (2/3)e^i`; a one-point carrier does not tear; non-refinements are refused |

**Corrections and scope.**

- The phase policy is exact: `e^(i theta)` is a basis element of the group ring
  `Q(i)[Q]`, so the kernel is the graded path-sum over that ring, and a number
  is produced only at a declared unit commensurate with every phase. The
  decimal `2.0806 + 1.6829i` is not reproduced.
- The "exact algebraic" worked example is wrong as stated. With phase 1 for
  returning and `i` for moving away, each history weighs `i`, so `K = 2i`;
  the source's `-2` charges `i` on both steps.
- The refinement-compatibility hypothesis of part (ii) fails for the paper's
  first target: on a finite carrier the free-particle kernel changes with the
  partition, and no declared normalization closes the tear. The limit clause is
  not reached for that family; a compatible family needs a declared
  coarse-graining other than the identity on kernels.
- The implementation sketch's `ComplexDecimal` value is replaced by
  `PhaseSum`. The Lean modules cited for parts (i) and (ii)
  (`QM.FiniteFeynmanShadow`, recorded under the same ENC-1072 as §11.15's
  `FinitePathSumReplay`; `QM.ContinuumNonPromotion`, ENC-1078)
  are not in the tree.

**What stays outside.** C1, C2, C6, C7 and C14 are fences. Of the
terminalization vocabulary (C5, C12) only the refusals and the refinement tear
are typed here; no `ClosureAbsorbed`, `OracleNeeded` or `BudgetUnknown` terminal
is produced. Convergence, topologies, the infinity path category and any
Lagrangian other than the free particle are not constructed. C15 was an
illustrative sketch.

### 11.17 Discrete Schrödinger cochain transport

**Original paper in the paper archive:** [Discrete Schrödinger cochain transport](sources/original_papers/033_schrodinger_finite_shadow/schrodinger_finite_shadow.md).

The paper stated the continuous-time Schrödinger equation on a finite graph,
norm conservation for Hermitian `H`, and a holonomy obstruction. The finite
content now computes exactly: the instantaneous norm rate, an exactly unitary
and a non-unitary finite step, and holonomy as the invariant that local data
miss. The claim ledger has no QM_033 rows, so the table uses the paper's own
claim IDs.

| Claim | Now computed by | Checked by (`tests/dynamics/schrodinger_finite_shadow.rs`) |
| --- | --- | --- |
| QM_033-C2 norm conservation | `finite_schrodinger_step::{norm_rate, euler_propagator}`, `cayley_unitary::cayley_unitary` | $2\operatorname{Im}\langle\psi,H\psi\rangle=0$ for the Laplacian of a non-flat kite connection, and $-6$ after an absorbing $-i/3$ at one vertex; the Cayley step keeps $\sum_v\psi_v\overline{\psi_v}=20$ over three steps for $\tau=1/2,3,-2/7$; the explicit step has $E^*E=I+\tau^2H^2$ exactly, gains $\tau^2\|H\psi\|^2$, keeps the kernel of $H$, and sends an eigenvector of eigenvalue $\lambda$ to $(1-i\tau\lambda)$ times itself |
| QM_033-C3 holonomy against local data | `finite_schrodinger_step::cycle_product`, `u1_gauge_triviality` | triangle Laplacians with equal diagonals and hopping moduli have cycle products `-1` and `+1` and `tr H^3 = 54` and `66`, so no unitary relates them; on the kite the cycle product is `-(1 * 2 * 3) Hol = (336 + 198i)/65`, reverses to its conjugate and is gauge invariant; the flat connection on the open triangle (`h1 = 1`) has trivial holonomy |

**Corrections and scope.**

- C2 is a statement about continuous time. Its exact finite content is that
  the rate vanishes for Hermitian `H`, and that conservation then depends on
  the step: the Cayley (Crank–Nicolson) step conserves the norm exactly for
  every rational `tau`, and the explicit step conserves it only on `ker H`.
- The "$L^1$ probability mass" is $\sum_v|\psi_v|^2$: the $L^1$ norm of
  `rho = |psi|^2`, which is the squared `L2` norm of `psi`.
- C3's "`Theta(C)` is non-zero whenever `H^1(G; U(1)) != 0`" is false:
  nonzero `H^1` allows a nontrivial holonomy but does not force one. What
  holds is gauge invariance of the cycle product, and that vertex terms and
  hopping moduli do not fix the unitary class. The angle sum `sum arg H` is
  transcendental; the exact invariant is the cycle product itself.
- The discrete Hamiltonian is QM_000's connection Laplacian `D_A* W D_A`.
- The Lean targets the paper names are not Lake modules;
  `research/lean4/qm_schrodinger_discrete_cochain.md`
  holds Lean text for a two-state swap.

**What stays outside.** C1, the equation `i hbar dpsi/dt = H psi` itself, and
C4, the lift to `L^2(R^3)`: continuous time, the exponential `exp(-itH)` and
continuum limits are not computed.

### 11.18 Finite unitary evolution

**Original paper in the paper archive:** [Unitary finite model](sources/original_papers/034_unitary_finite_shadow/unitary_finite_shadow.md).

The source was a reserved slot with one placeholder row and no text. Its finite
content is the following: discrete unitary dynamics preserves the norm, and the
continuous-time generator is not
determined by the finite map. Both now compute exactly, replacing a NumPy check
with a floating tolerance.

| Claim | Now computed by | Checked by (`tests/dynamics/unitary_finite_shadow.rs`) |
| --- | --- | --- |
| Unitary steps preserve the norm | `scalar::is_unitary`, `cayley_unitary::cayley_unitary` | a Cayley unitary (entries `(±1 ± i)/2`) and the swap preserve `sum psi conj(psi)` on three fields; the explicit step of an `H` with `H^2 = 3I` is not unitary and multiplies it by 4 |
| A finite map need not fix a generator | `semiring_matrix::boolean_square_roots`, exact determinants, `ExactMatrix<Cyc8>` | the swap has no Boolean half-step (all 16 candidates), none over any real field (`det X = -1`, while a real `M` has `det(M)^2 >= 0`), and four distinct unitary half-steps over `Q(i)`, each with `det = ±i`; a quarter-step exists over `Q(zeta_8)` and not inside `Q(i)`; the three-cycle's only Boolean half-step is its inverse |

**Corrections and scope.**

- The legacy evidence counted "branches" of a matrix logarithm in a window
  `|k| <= 2` with floating tolerance. The exact replacement says which
  carriers have half-steps of the swap and how many: none over the Boolean
  semiring or the reals, four over `Q(i)`; the quarter step needs
  `Q(zeta_8)`.
- No logarithm is computed. Its finite shadow is the non-uniqueness and field
  dependence of fractional steps, together with the Cayley chart's excluded
  eigenvalue (QM_035).

**What stays outside.** The exponential, the logarithm and any one-parameter
group in real time. QM_034-C0 remains a reserved-slot definition.

### 11.19 Hamiltonian generator admission

**Original paper in the paper archive:** [Hamiltonian generator admission](sources/original_papers/035_hamiltonian_generator_admission/hamiltonian_generator_admission.md).

QM_035 was a reserved slot with one placeholder row (QM_035-C0) and no text.
Its topic, admitting a Hamiltonian generator for a given unitary step, is now an
exact decision in the Cayley chart. The source had no claims, so the table
names the computed statements directly.

| Claim | Now computed by | Checked by (`tests/dynamics/hamiltonian_generator_admission.rs`) |
| --- | --- | --- |
| generator admission (no ledger row) | `cayley_unitary::cayley_generator` | `cayley_generator(C_tau(H)) = tau H` on the kite Laplacian for `tau = 1, 1/2, -3/5`; the product of two non-commuting Cayley steps is admitted with the Hermitian generator `[[13/7, -1/7 - i], [-1/7 + i, -1/7]]`, which is not the sum of the parts; the swap and `-I` (eigenvalue `-1`) are refused; `iX` is admitted with generator `-X` |
| composition of steps (no ledger row) | `cayley_unitary::cayley_unitary`, `cayley::compactified_circle_composition` | tangent addition `(s + t)/(1 - st)` holds for the toggle, where `X^2 = I`; for `H^2 = 3I` the parameter is `(s + t)/(1 - 3st)` and tangent addition fails; on the kite the product's generator `G` solves `(I - st H^2) G = (s + t) H` and is not a multiple of `H` |
| agreement with existing charts (no ledger row) | `cayley_unitary`, `dynamics::cayley_transform_toggle`, `cayley::cayley_transform` | the general transform equals the toggle formula for `tau = 1/2, 3/4, 1`, and its realification equals the real skew-symmetric Cayley transform of the realification of `iH` |
| refusals (no ledger row) | `cayley_unitary`, `cayley_generator` | non-Hermitian, non-unitary and non-square inputs are refused |

**Corrections and scope.**

- Admission is decided in the Cayley chart `U = (I - iH)(I + iH)^(-1)`,
  which excludes eigenvalue `-1` as a logarithm excludes a branch cut. The
  chart is a declared choice. Inside it the generator is unique and rational.
- The tangent addition of `cayley::compose_circle_parameters` composes points
  of the circle. For two Cayley steps of one matrix `H` it needs the hypothesis
  `H^2 = I`. In general two Cayley steps of `H` compose
  to the step of `(s + t) H (I - st H^2)^(-1)` when that denominator is
  invertible. It need not be a multiple of `H`; a sufficient condition is
  that `H^2` acts as a scalar on the range of `H`. Special parameters such as
  `s = -t` give zero regardless of that spectral condition.

**What stays outside.** `exp(-itH)`, matrix logarithms, Stone's theorem and
one-parameter groups in real time. QM_035-C0 remains a reserved-slot
definition.

### 11.20 Trace-zero observables and a nonzero commutator

**Original paper in the paper archive:** [Matrix and differential-equation representations](sources/original_papers/040_matrix_vs_diffeq_representation/matrix_vs_diffeq_representation.md).

The package is named for matrix versus differential-equation representation,
but its text makes a narrower point. In the `3 x 3` Gaussian-integer matrices,
the first three Gell-Mann matrices have trace zero while their commutators do
not vanish, so a trace readout cannot see noncommutativity. Everything in the
paper is closed arithmetic on named matrices. It now runs on the crate's
Gell-Mann basis of `C^3` rather than on a second copy of the matrices, and the
single witness is extended to all 28 pairs of that basis. The claim ledger has
no QM_040 rows, so the table uses the paper's own claim IDs.

| Claim | Now computed by | Checked by (`tests/representation/trace_zero_commutator.rs`) |
| --- | --- | --- |
| QM_040-C2 coordinate projections are idempotent | `exact_field::matrix::{diagonal, multiply}` | `P0^2 = P0`, `P1^2 = P1`, `P0 P1 = 0`, and `Lambda_3 = P0 - P1`; `(2 P0)^2 = 4 P0`, not `2 P0` |
| QM_040-C3 the three matrices have trace zero | `su_n::GellMannBasis::new(3)`, `exact_field::matrix::trace` | `tr Lambda_1 = tr Lambda_2 = tr Lambda_3 = 0` |
| QM_040-C4 three commutators | `exact_field::matrix::commutator`, `GellMannBasis::rational_structure_part` | `[L1, L2] = 2i L3`, `[L2, L3] = 2i L1`, `[L3, L1] = 2i L2`; the hand products `L1 L2 = diag(i, -i, 0)` and `L2 L1 = diag(-i, i, 0)`; the reversed bracket `[L2, L1]` is `-2i L3`; the basis gives `f_123 = 1` |
| QM_040-C5 local trace green with a nonzero commutator | same | `tr L1 = tr L2 = 0` while `[L1, L2] = diag(2i, -2i, 0)`; `L3` and the second diagonal generator are also trace zero, and they commute |
| QM_040-C5 over the whole basis | same | on all 28 pairs of the eight generators every trace and every commutator trace is 0; 25 pairs fail to commute and 3 commute (the second diagonal generator with `L1`, `L2` and `L3`) |

**Corrections and scope.**

- The carrier `Z[i]^(3x3)` sits inside the crate's exact `Q(i)` matrices. The
  paper's `Lambda_1`, `Lambda_2`, `Lambda_3` are the unscaled shapes of the
  first three generators of `gell_mann_basis`, so no second copy of the
  matrices was written.
- The paper declined to construct all eight SU(3) generators; the crate
  already has them. The census over the 28 pairs replaces the single witness:
  the trace readout is zero on every pair, so it cannot separate the 3
  commuting pairs from the 25 others. The trace of a commutator is always
  zero, so no trace readout of the bracket helps either.
- The twelve cited declarations `QM.GellMann.*` are not in the Lake workspace
  `lean4/quantum_mechanics/`. Their text survives as Markdown in
  `research/lean4/qm_gellmann_matrix_projections.md`.
  The `ENC-1262` binding was not checked.
- The package name promises a comparison of matrix and differential-equation
  representations that the text never makes. The finite comparison of the
  Schrödinger and Heisenberg pictures is under QM_041.

**What stays outside.** C1 (the carrier) is a definition and C6 (the authority
predicate) a scope fence. Physical locality or colour, SU(N) representation
theory, Hermitian dynamics and any continuum reading are not treated.

### 11.21 Heisenberg-picture evolution and history decoherence

**Original paper in the paper archive:** [Heisenberg-picture model](sources/original_papers/041_heisenberg_picture_shadow/heisenberg_picture_shadow.md).

The paper made three statements: the Gell-Mann–Hartle decoherence matrix
`D(j, k) = Tr(C_j rho C_k*)` has a nonnegative diagonal equal to the path
probabilities; vanishing off-diagonal entries give probability additivity; and
the Heisenberg-picture observable `A(t) = U(t)* A U(t)` obeys
`dA/dt = i [H, A(t)]`. The first two now compute exactly in
`decoherence_functional`, on class operators built from Heisenberg-picture
projectors. The third has the wrong sign for the paper's own `U(t)`. Its exact
finite content, the Schrödinger–Heisenberg duality of declared steps and the
derivative of the Cayley path, is computed in `heisenberg_picture`.

| Claim | Now computed by | Checked by (`tests/representation/heisenberg_picture_shadow.rs`) |
| --- | --- | --- |
| QM_041-C1 nonnegative diagonal equal to the path probability | `decoherence_functional::{chain_histories, DecoherenceFunctional::{matrix, coarse_grain}}` | histories through the basis at three times, with `rho = diag(1/3, 2/3)` and two rational rotation steps: each diagonal entry is `rho_(x0)` times the unistochastic path weight of `graded_path_sum` (the path `0 -> 0 -> 0` gives `81/1875`); each off-diagonal entry with shared endpoints is the product of the two path amplitudes; coarse-graining over the middle time gives the Born weight of the propagator (`49/1875` from 0 to 0), which differs from the sum of the path weights (`337/1875`) by `rho_(x0)` times `coherent_interference::cross_term` of the path amplitudes (`-288/1875`); with the indefinite `rho = diag(3/2, -1/2)` a diagonal entry is `-8/25` |
| QM_041-C2 vanishing off-diagonal entries give additivity | `DecoherenceFunctional::{coarse_grain, sum_rule_residual, medium_decoherence_witness, weak_decoherence_witness}` | a second qubit that records the first outcome through a CNOT makes `D = diag(81, 144, 256, 144)/625`, and all 15 coarse-grainings of the four histories obey the sum rule; without the record the pair `(0, 2)` breaks it by `-288/625`; with the complex second step `[[3/5, -4i/5], [-4i/5, 3/5]]` the entries `D_02 = 144i/625` and `D_13 = -144i/625` are nonzero, yet all 15 coarse-grainings obey the sum rule |
| QM_041-C3, corrected: the Heisenberg picture of declared steps | `heisenberg_picture::{schrodinger_state, heisenberg_observable}` over `exact_channel::ExactKrausChannel` | along three Cayley steps of two non-commuting generators `Tr(rho_3 A) = Tr(rho A_3)`, and conjugating in the Schrödinger order pairs a different operator; `C_(1/2)(Z) = diag(3/5 - 4i/5, 3/5 + 4i/5)` turns `X` into `-(7/25) X - (24/25) Y`; the evolution preserves products, commutators and adjoints, and Cayley steps of `H` fix `H` and `H^2 + 2H`; a non-unitary Euler step is refused |
| QM_041-C3, corrected: the derivative of the Cayley path | `heisenberg_picture::{cayley_jet, heisenberg_jet, cayley_rate_generator}` | the exact derivative of `C_tau(H)* A C_tau(H)` at `tau = 0` is `2i [H, A]` (for `H = Z`, `A = X`: `-4Y`); along `C_t(-H/2)`, whose derivative at 0 is `iH` like `exp(itH)`, it is `-i [H, A] = 2Y`, not the paper's `i [H, A] = -2Y`; at `tau = 1/2, -3, 2/7` it is `i [G_tau, A(tau)]` with `G_tau = 2H (I + tau^2 H^2)^(-1)`, which is `(8/7) H` at `tau = 1/2` when `H^2 = 3I`, but for `H = diag(0, 1, 2)` scales the `(0,1)` and `(0,2)` entries of `i [H, A(tau)]` by `8/5` and `1` |

**Corrections and scope.**

- `rho` was "the discrete `L1` diagonal density". The diagonal of `D` equals
  the classical path mass only for fine-grained histories whose first
  projection is in the eigenbasis of a diagonal `rho`. For coarse-grained
  histories it is a Born weight and differs from the path masses by the
  interference term. Nonnegativity needs `rho >= 0`, and then `D` is positive
  semidefinite, which is more than the paper claimed.
- Projectors that all commute, as diagonal projectors with no dynamics between
  them do, make every family decohere trivially. The decoherent example here is
  the standard one: a record kept in a second system.
- Additivity under every coarse-graining holds exactly when `Re D_jk = 0` for
  `j != k`. Vanishing `D_jk` is sufficient, not necessary; the complex family
  above is the countermodel. The paper's `Phi_int(D) = sum |D_jk|` needs square
  roots; only its vanishing is used, and that is decided entrywise. It is not an
  `omega_functional` functional.
- C3 is off by a sign. With the paper's `U(t) = exp(i t H)`,
  `dA/dt = -i [H, A(t)]`; with `U(t) = exp(-i t H)` the paper's formula holds.
  No exponential is computed. The derivative is taken exactly, with first-order
  jets of the rational Cayley path, at rational points. The ledger row
  QM_041-C3 is now `REFUTED BY COMPUTATION`, citing the sign test and the
  failure of finite steps away from `t = 0`; the corrected statement is the
  one in the table, and it is recorded here rather than in the ledger.
- C1 and C2 are now `FINITE COMPUTATION` with the scopes above: C1 needs
  `rho >= 0` and holds as "path probability" only for fine-grained histories,
  and C2 is sufficient, not necessary.
- The Cayley steps are not a one-parameter group in the additive parameter.
  The composite and rate generator need not be scalar multiples of the
  original generator; the sufficient spectral condition and exceptional
  parameters are recorded in QM_035.

**What stays outside.** C4, the quarantine of infinite history spaces and
master equations, is a scope fence. Continuous time, `exp(-itH)` and master
equations are not computed.

### 11.22 A two-history decoherence residual

**Original paper in the paper archive:** [Gell-Mann–Hartle cochain decoherence](sources/original_papers/043_gellmann_hartle_cochain_decoherence/gellmann_hartle_cochain_decoherence.md).

The paper kept the complex decoherence functional as imported context and
proved one integer identity: for a triple `(d11, d12, d22)`, the global weight
minus the local diagonal weight is `2 d12`. The functional itself now computes
in `decoherence_functional`, and the identity turns out to concern the real
part: for complex entries the residual is `2 Re D12`. The two conditional
standard facts, positivity and normalization, are computed together with the
failure of each hypothesis. The claim ledger has no QM_043 rows, so the table
uses the paper's own claim IDs.

| Claim | Now computed by | Checked by (`tests/representation/gell_mann_hartle_decoherence.rs`) |
| --- | --- | --- |
| QM_043-C1 `D_jk = Tr(C_j rho C_k*)` (imported definition) | `decoherence_functional::DecoherenceFunctional::new` | every entry equals the trace computed directly, and `D` is Hermitian, for the four histories of a qubit through two basis measurements |
| QM_043-C2 `rho >= 0` makes `D` positive semidefinite | `DecoherenceFunctional::matrix`, `exact_hermitian::is_positive_semidefinite`, `exact_field::ordered::hermitian_form` | `D` is PSD for `rho = diag(1, 0)`; for `z = (1, i, 2 - i, 1/2)`, `z* D z = Tr(A rho A*)` with `A = sum conj(z_j) C_j`, and the unconjugated `sum z_j C_j` gives a different value because `D` has the entries `144i/625` and `-144i/625`; with the indefinite `rho = diag(3/2, -1/2)` a diagonal entry is `-8/25` (`heisenberg_picture_shadow.rs`) |
| QM_043-C3 the two-history residual is `2 d12` | `DecoherenceFunctional::{coarse_grain, sum_rule_residual}` | the worked example `(2, 1, 3)`, realized by `C_1 = [[1, 1], [0, 0]]`, `C_2 = [[1, 0], [1, 1]]` and `rho = I`: local weight 5, global weight 7, residual 2; on a complex functional every pairwise residual equals `2 Re D_jk`, and `D_02 = 144i/625` leaves the union weight at `337/625 = D_00 + D_22` |
| QM_043-C4 no certificate, no promotion | `omega_wdp::coda::q::admission::QAdmissionGate` | `omega_engine/crates_rs/tests/omega_wdp/test_coda_q_qm_finite_shadow_membrane_admission.rs`: a finite shadow without a convergence-certificate route is `OracleNeeded`, and a self-declared terminal falls to `OpenResidual` |
| QM_043-C6 the diagonal sums to `Tr(rho)` under `sum C* C = I` | `DecoherenceFunctional::is_complete` | chain histories satisfy `sum C = I` and `sum C* C = I`, and `tr D = 1`; `C_1 = [[1, 1], [0, 0]]` and `C_2 = [[0, -1], [0, 1]]` sum to `I` but are not complete, and give `tr D = 3` for `rho = diag(0, 1)` (and `1` for `rho = diag(1, 0)`, so one state does not detect the missing premise) |

**Corrections and scope.**

- The paper declined to build a bridge from the complex functional to the
  integer triple. The bridge is the real part: for two class operators
  the union weight is `D_11 + D_22 + 2 Re D_12`. Reading `d12` as the complex
  entry makes "`d12 != 0` implies global `!=` local" false, with the
  countermodel `D_02 = 144i/625` and residual 0. Read as `Re D12`, the integer
  statement is the computed identity restricted to integer data.
- C2 and C6 were prose-only conditional arguments. They are now computed with
  their hypotheses separated: the positivity hypothesis fails for an indefinite
  `rho`, and the completeness premise for a pair that sums to `I` without being
  complete.
- Of the ten Lean declarations cited for C3, the three `OmegaCore` theorems are
  in `lean4/PrimitiveDifference.lean`, a Lake root; no build
  was run for this entry. `QM.GellMann.DecoherenceMatrix2x2.*` and
  `QM.GellMann.decoherence_structure_not_auth` exist only as Markdown in
  `research/lean4/qm_gellmann_decoherence_matrix.md`,
  and C4's `QM.shadow_no_cert_*` only in `research/lean4/qm_continuum_non_promotion.md`.

**What stays outside.** C5, persistence of a phase class under a map on
`H^1(G; U(1))`, stays `OPEN`: the paper declares no map. For a declared map on
a declared graph, persistence is the gauge-equivalence decision that
`holonomy_interference::gauge_equivalence` already makes (QM_063). No
probability is assigned to a family that breaks a sum rule.

### 11.23 Dirac equation admission

**Original paper in the paper archive:** [Dirac equation admission](sources/original_papers/050_dirac_equation_admission/dirac_equation_admission.md).

QM_050 was a reserved slot with one placeholder row (QM_050-C0) and no text.
Its topic, admitting the Dirac equation on a finite exact carrier, is now
computed in two modules. `dirac_gamma_admission` admits a declared family of
gamma matrices when it satisfies the Clifford relations, and then computes the
Dirac operator at rational momenta, its solutions, its adjoint structure and
the spin elements that act on it. `lattice_dirac_doubling` puts the operator on
a declared periodic lattice, where the naive discretization doubles. The source
had no claims, so the table names the computed statements directly.

| Claim | Now computed by | Checked by (`tests/representation/dirac_equation_admission.rs`) |
| --- | --- | --- |
| Clifford admission (no ledger row) | `dirac_gamma_admission::CliffordFamily::{admit, dirac, weyl}` | the Dirac and chiral representations, built from the Pauli matrices of `gell_mann_basis`, satisfy `{gamma^mu, gamma^nu} = 2 eta^(mu nu) I` with `eta = (+, -, -, -)`; the Dirac matrices with a Euclidean metric fail at `(1, 1)` and a repeated matrix at `(1, 2)`; `2 x 2` matrices suffice for three generators (`X, Y, Z` Euclidean, `Z, iX, iY` with `(+, -, -)`); empty, ragged, mismatched and non-unit metric declarations are refused |
| Klein–Gordon square (no ledger row) | `CliffordFamily::{slash, interval}` | `slash(p)^2 = (p . p) I` on four momenta in both representations, among them the null `(3, 1, 2, 2)`; a momentum of the wrong length is refused |
| solutions exactly on the mass shell (no ledger row) | `CliffordFamily::solution_dimension` | at `(5, 4, 0, 0)` with `m = 3` there are 2 solutions and at `(5, 3, 0, 0)` none; negative energy and `m = -5` at `(13, 0, 12, 0)` also give 2; massless: 2 at a null momentum, 0 at a timelike one, 4 at `p = 0`; the columns of `slash(p) + m` have rank 2 and solve the equation; massless solutions split one and one by chirality |
| adjoint, irreducibility, chirality (no ledger row) | `CliffordFamily::{has_dirac_adjoint, product_span_rank, chirality}` | both representations satisfy `gamma^0 (gamma^mu)* gamma^0 = gamma^mu` and are related by `T = [[1, -1], [1, 1]] (x) I`, which is `sqrt(2)` times a unitary; the non-unitary similarity by `[[1, 1], [0, 1]] (x) I` keeps every anticommutator and loses the adjoint; the 16 ordered products have rank 16, the three Pauli matrices only 4 (`XYZ = iI`), the doubled `I (x) gamma` 16 of 64, and a family of seven `8 x 8` generators is admitted but its 128 products are not enumerated; `gamma^5 = i gamma^0 gamma^1 gamma^2 gamma^3` squares to `I`, anticommutes with every `gamma^mu` and is `diag(-1, -1, 1, 1)` in the chiral form; an odd family is refused |
| spin elements and covariance (no ledger row) | `CliffordFamily::{plane_spin_element, vector_action}`, `boost_half_parameters` | `5/4 + (3/4) gamma^0 gamma^1` acts as the boost `(cosh, sinh) = (17/8, 15/8)`, which is `lorentz_boost::boost_power_analytic(2)`; `L eta L^T = eta`; `-S` acts as `S` and `S^2` as `L^2`; `3/5 + (4/5) gamma^1 gamma^2` rotates by cosine `-7/25`; `-I` acts as the identity; `S` carries every solution at `(5, 4, 0, 0)` to a solution at `L p = (145/8, 143/8, 0, 0)`; singular and non-Clifford `S` are refused |
| the canonical rational boost has no spin lift (no ledger row) | `boost_half_parameters`, `CliffordFamily::vector_action` | `lorentz_boost::LorentzBoostB1` (`cosh = 5/4`, `sinh = 3/4`) needs the half-rapidity `sqrt(9/8)`, square class 2, and is refused; the rational `3 + gamma^0 gamma^1` acts as `B1`, but `(3 + gamma^0 gamma^1)(3 - gamma^0 gamma^1) = 8 I` and 8 is not a rational square; `B1^2` lifts to `5/4 + (3/4) gamma^0 gamma^1`; over `Q(zeta_8)` the element `(3 sqrt 2)/4 + (sqrt 2 / 4) gamma^0 gamma^1` has reverse product `I` and acts as `B1`; data off the future unit hyperbola are refused |
| lattice doubling (no ledger row) | `lattice_dirac_doubling::LatticeDirac::{naive_operator, wilson_operator, zero_mode_count, anticommutes_with_chirality}` | in one dimension the naive operator has 2 zero modes for periods 4 and 6 (constant and staggered) and 1 for periods 3 and 5, the Wilson operator 1; in two dimensions with the Pauli pair on `4 x 4` sites, 8 naive zero modes (2 spin components at 4 corners) and 2 Wilson zero modes, and 2 naive zero modes on `3 x 3`; the naive operator is anti-Hermitian and anticommutes with `gamma_*`, the Wilson term is Hermitian and does not; Minkowski families, period 2 and carriers above 128 are refused |

**Corrections and scope.**

- There was no source text. The implementation is limited to what a finite
  exact carrier decides: algebraic admission of the gamma matrices,
  plane-wave solutions at rational momenta, and the lattice operator on
  declared periodic lattices.
- A rotation or boost is never given by an angle or a rapidity. Spin elements
  are declared by rational half-parameters, and a rational boost whose
  half-rapidity is irrational is refused with its square class rather than
  approximated.
- The crate's canonical rational boost `B1` in `lorentz_boost` has no spin lift
  with entries in `Q(i)`: its Doppler factor `e^eta = 5/4 + 3/4 = 2` is not a
  square there. Its square, with Doppler factor 4, lifts. The refusal is
  relative to the field: over `Q(zeta_8)`, which contains `sqrt 2`, `B1`
  lifts exactly.
- The lattice counts are the finite form of fermion doubling on the declared
  lattices, and the Wilson term trades the doublers for chiral symmetry there.
  The Nielsen–Ninomiya theorem itself is not proved.

**What stays outside.** The Dirac equation in position space on a continuum,
the Dirac sea and quantum field theory, spin lifts of rational Lorentz
transformations other than plane boosts and rotations, and any continuum
limit of the lattice operator. QM_050-C0 remains a reserved-slot definition.

### 11.24 Spinor structure admission

**Original paper in the paper archive:** [Spinor structure admission](sources/original_papers/051_spinor_structure_admission/spinor_structure_admission.md).

QM_051 was a reserved slot with one placeholder row (QM_051-C0) and no text.
Its topic is now two exact computations. `rational_spin_lift` computes the
double cover `SU(2) -> SO(3)` on rational points and decides which rational
rotations lift. `spin_structure_obstruction` decides whether a flat rational
rotation transport on a declared 2-complex lifts to a flat `SU(2)` transport,
and counts the lifts up to vertex gauge. The source had no claims, so the table
names the computed statements directly.

| Claim | Now computed by | Checked by (`tests/representation/spinor_structure_admission.rs`) |
| --- | --- | --- |
| the double cover on rational points (no ledger row) | `rational_spin_lift::{unit_quaternion_matrix, rotation_of}`, the linear part of `qubit_bloch_map::QubitBlochMap` | five rational unit quaternions give `SU(2)` matrices over `Q(i)` with determinant 1 whose images are rotations; `U` and `-U` have the same image; `(3/5, 4/5, 0, 0)` is the complex mixer `[[3/5, -4i/5], [-4i/5, 3/5]]` and rotates about `x` by cosine `-7/25`; the image of a product is the product of the images, and the phase `i` changes nothing; off-sphere quaternions and non-unitary matrices are refused |
| rational lifts and the spinor norm (no ledger row) | `rational_spin_lift::{rodrigues_quaternion, spin_lift}` | every rotation made from a rational quaternion lifts back to `+-U`; the quarter turn about `z` has Rodrigues vector `(2, 0, 0, 2)`, class 2, and is refused; the rotation with cosine `3/5` has class 5, and its square (cosine `-7/25`) lifts to `+-(3/5, 0, 0, 4/5)`; the S gate `diag(1, i)` realizes the quarter turn with determinant `i`, not 1; over `Q(zeta_8)` the quarter turn lifts to `diag(zeta^-1, zeta)`, whose square is the rational lift `-iZ` of the half-turn and whose fourth power is `-I`; improper and non-orthogonal matrices are refused |
| octahedral census (no ledger row) | `spin_lift`, `rotation_groups::{build_octahedral_group, build_tetrahedral_group}` | of the 24 octahedral rotations exactly the 12 tetrahedral ones lift, and the other 12 have class 2; over all 576 pairs the class of a product is the product of the classes modulo squares |
| the cover does not split (no ledger row) | `spin_lift` | the 24 lifts of the tetrahedral group are closed under multiplication; only `+-I` square to `I` among them, against 4 rotations with `R^2 = I`, and only `+-I` lie over the identity; every half-turn lifts to elements with `U^2 = -I`, and over the order-3 rotation one lift has order 3 and the other order 6 |
| flat spin lifts on declared 2-complexes (no ledger row) | `spin_structure_obstruction::FlatRotationTransport::{new, obstruction, flat_lifts, gauge_classes}` | for the trivial transport the one-vertex torus has 4 gauge classes of flat lifts, the Klein bottle 4, the projective plane 2, a sphere made of two triangles 1 (also for a pure-gauge transport), each equal to the order of `H^1(X; F_2)` computed from ranks over `F_2` (`omega_homology::matrix_reduction::rank_z2`); half-turns about `x` and `y` on the torus commute, but their lifts give face product `-I` and no flat lift exists, in agreement with `F_2` linear algebra (the obstruction is not in the image of `d1`); a single half-turn is unobstructed on the torus and obstructed on the Klein bottle and the projective plane; curved faces, edges without rational lifts, broken walks and malformed declarations are refused |

**Corrections and scope.**

- There was no source text. "Spinor structure" is implemented in its two finite
  senses: lifting single rotations through the double cover, and lifting a flat
  transport on a finite complex.
- Rotations are declared by rational matrices; no angle is formed. A lift is
  exact or refused. The obstruction for one rotation is its spinor norm, the
  squarefree part of the norm of its Euler–Rodrigues vector, computed with
  `quadratic::Surd`.
- For a transport the obstruction is a face cochain over `F_2`: a flat lift
  exists exactly when it equals the traversal parities of some sign change.
  That is decided by exhaustive search over the `2^E` sign changes and
  checked against ranks over `F_2`. The class counts 4, 4, 2 and 1 are
  compared with the order of `H^1(X; F_2)`, computed independently, for the
  torus, the Klein bottle, the projective plane and the sphere. That the two
  always agree (the flat lifts form a torsor over `H^1(X; F_2)`) is checked on
  these complexes, not proved.

**What stays outside.** Spin structures on smooth manifolds, Stiefel–Whitney
classes as characteristic classes, `Spin(n)` for `n > 3`, and transports whose
edge rotations have no rational lift, which are refused rather than lifted
over a quadratic field. QM_051-C0 remains a reserved-slot definition.

### 11.25 Superposition as a quotient fiber

**Original paper in the paper archive:** [Superposition as the quotient fiber](sources/original_papers/060_superposition_as_the_quotient_fiber/superposition_as_the_quotient_fiber.md).

The paper placed the phase content of a superposition in the fiber of the
phase-blind projection $\pi(c)_g=|c_g|^2/\sum_h|c_h|^2$ over a declared
sector basis: invisible to the diagonal readout, visible after a mixing map.
The projection, its fibers and the descent question now compute exactly over
`Q(i)`. Two statements had to be corrected. The descent criterion holds only
when the zero vector is kept as a point of the quotient, and not every
rational simplex point is a quotient point.

| Claim | Now computed by | Checked by (`tests/superposition/superposition_as_the_quotient_fiber.rs`) |
| --- | --- | --- |
| QM-060-C1, C2 carrier and phase-blind difference (definitions) | `phase_blind_quotient::{phase_blind_projection, phase_equivalent}` | exact projections of real, complex and 80-digit configurations; invariance under unit phases and nonzero scalars of `Q(i)`; 150 generated configurations of length up to 20; empty and zero configurations and length mismatches are refused |
| QM-060-C3 base and fiber | `FiberPoint`, `UnitPhaseGroup`, `discrete_fiber`, `gaussian_lift`, `rational_lift` | relative phase dimension `\|supp\| - 1` for supports 1 to 5; the `{±1}` and `{±1, ±i}` fibers have `2^(k-1)` and `4^(k-1)` distinct members, all over one point; `(1/3, 2/3)` has the preimage `(i/3, (1+i)/3)` and no real one; `(1/4, 3/4)` has none |
| QM-060-C4 fiber theorem and descent | `classify_descent`, `MonopolarDescent::apply`, `separates`, `zero_extended_projection` | maps with at most one nonzero entry per row agree with their induced simplex map on all 35 nonzero configurations of a box; `H2`, `H4`, a 3-4-5 rotation, a `3 x 3` mixer, a complex map and a `1 x 3` map are refused with a constructed separating pair; 58 generated mixing matrices are refused; `[[-3,5],[-3,5]]` is separated only through annihilation |
| QM-060-C5 worked example | same | `(1,1)` and `(1,-1)` project to `(1/2, 1/2)`; `H` sends them to `(2,0)` and `(0,2)`, which project to `(1,0)` and `(0,1)`; `H^2 = 2I`, and the corrupted `H[1][1] = +1` fails it |
| QM-060-C6 no diagonal mass on the fiber (fence) | `coherent_interference::cross_term` | on the 16 quarter-turn representatives of `(1,1,1)` the projection stays `(1/3, 1/3, 1/3)` while the cross term takes the values `-2, 2, 6` |
| QM-060-C7 readout relativity (interpretive) | `classify_descent`, `separates` | the identity readout does not separate `(1,1)` from `(1,-1)`; the Hadamard readout does |

**Corrections and scope.**

- The source stated that a linear map descends through the quotient exactly
  when it has at most one nonzero entry per row. For the projection defined
  on nonzero vectors only, this is false: `[[1,1],[1,1]]` sends every
  configuration it does not annihilate to `(1/2, 1/2)`, so it descends to a
  constant. The criterion holds once the zero vector is a separate point.
  Then a row with nonzero entries `m_j, m_k` is refused with the pair
  `e_j - (m_j/m_k) e_k` and `e_j + (m_j/m_k) e_k`: they are phase equivalent,
  and the row annihilates the first but not the second. The source's stress
  suite raised an error on exactly this case, `[[-3,5],[-3,5]]`.
- The source took the quotient base to be the rational simplex. A point `p`
  has a preimage in `Q(i)^n` only when each product `p_g p_h` of nonzero
  coordinates is a sum of two rational squares, and a real rational preimage
  only when each is a rational square. So `(1/4, 3/4)` is not a quotient
  point, and a lift `c_g = sqrt(w_g) e^(i theta_g)` need not exist in the
  declared carrier.
- The source enumerated a "discrete fiber" from the base point itself,
  `(p_0, ±p_1, ...)`. That vector lies over `p` only when the nonzero weights
  are equal: `(1/3, 2/3)` projects to `(1/5, 4/5)`. The port enumerates
  through a declared representative and a declared finite unit group.
- Amplitudes are Gaussian rationals rather than real rationals. Where the
  source answered "not equivalent" for zero vectors and length mismatches,
  the port refuses with a typed error; floating-point input cannot be
  represented.
- The package's Lean modules (`GaussIntKernel`, `PhaseBlindPresentation`,
  `QuotientFiber`, `MixingObstruction`) prove the two-sector witness and the
  non-descent of the Hadamard map. They now live in `lean4/quantum_mechanics/`
  as roots of its library, next to the overlapping `H008PhaseBlindPresentation`,
  `H009PhaseFiber` and `H010InterferenceNonDescent`. A Mathlib-free staging
  build with toolchain `v4.33.1` compiled them without `sorry`; the only axiom
  reported is `Quot.sound`, in `no_descent_through_quotient`. That is a build,
  not a receipted replay.

**What stays outside.** QM-060-C8 and C9 remain fences: nothing here derives
Hilbert space, unitarity or the Born rule. The quadratic readout, the sector
basis and the phase groups stay declared. The continuous relative-phase torus
`U(1)^(|E_w| - 1)` is not constructed; only rational points of the circle and
the finite groups `{±1}` and `{±1, ±i}` are used. The monopolar half of the
descent criterion is checked on declared maps and configurations; its general
argument is prose.

### 11.26 Interference beyond $L^1$ weights

**Original paper in the paper archive:** [Interference as the non-$L^1$ resource](sources/original_papers/061_interference_as_the_non_l1_resource/interference_as_the_non_l1_resource.md).

The paper had two parts. Part A re-packaged an earlier result: the interfered
weight $I(c)=|\sum_s c_s|^2$ is not a function of the diagonal weights
`|c_s|^2`, and a primitive-difference phase has no holonomy. Part B defined a
buildability set `S` of four conditions on a declared architecture. Part A now
computes exactly over `Q(i)`, and the non-identifiability is sharpened to a
characterization. Part B is small: apart from the race condition it is a
definition.

| Claim | Now computed by | Checked by (`tests/superposition/interference_as_the_non_l1_resource.rs`) |
| --- | --- | --- |
| QM-061-C1..C3 diagonal layer, interfered weight, cross term (definitions) | `coherent_interference::{interfered_weight, cross_term}` | the cross term equals $2\sum_{j<k}\operatorname{Re}(c_j\overline{c_k})$ on 50 generated complex and 50 real configurations; one-coordinate configurations have cross term zero; empty input is refused |
| QM-061-C4 Theorem A1 | `coherent_interference::diagonal_twin` | one explicit pair decides A1; of the 125 configurations in `{0, ±1, ±i}^3`, the 112 with two or more nonzero coordinates have a twin with the same diagonal weights and a different interfered weight, and the other 13 satisfy `I = sum \|c_s\|^2`; real configurations are twinned by a sign flip |
| QM-061-C5 worked example | `interfered_weight`, `cross_term` | `(1,1)`, `(1,-1)` and `(1,i)` share diagonal weights and have interfered weights `4, 0, 2` and cross terms `2, -2, 0` |
| QM-061-C6 relation to RDB-03 (standard) | same | the cross-term identity and the diagonal twins above |
| QM-061-C7 Theorem A2 | `holonomy_interference::walk_integral` with `finite_cochain_packet` | `d0 f` integrates to `f(end) - f(start)` along open walks and to 0 around closed walks on a triangle and a 4-cycle; a perturbed edge gives circulation `1` or `1/2`; a loop integral `s` gives `Phi1 = \|s\|` on the unit-weight triangle, replayed by `omega_functional` |
| QM-061-C12 Theorem B1 | `buildability_criterion::{ResidualRace, ArchitectureDeclaration}` | `rho(n) = rho0 + n step` agrees with iteration; the residual stays at or below `rho0` for 100 cycles when `step <= 0`; `step = 10^-12` exceeds `rho0` at cycle 1; all 16 assignments of `S1..S4` give the conjunction |
| QM-061-C13 Theorem B2 | same | four drop-one declarations each fail exactly one condition; the missing `S4` is realized by a connection on a tree, which is always gauge trivial |
| QM-061-C14 Theorem B3 | same | a declaration that satisfies all four conditions |

**Corrections and scope.**

- The source's engine called `Delta(v) = (sum |v_s|)^2 - sum v_s^2` the
  non-L1 resource deficit, and its mutation audit tied `S4` to `Delta > 0`.
  `Delta` depends only on the `|v_s|`, so it is a function of the diagonal
  weights: `(1,1)` and `(1,-1)` have the same `Delta = 2` and opposite cross
  terms `±2`. It is the largest cross term among the sign changes of `v`
  (checked over every sign pattern of 40 generated vectors), a bound on the
  interference rather than the part the diagonal misses. It is kept as
  `l1_coherence_deficit` with its exact identities: invariance under all 552
  signed permutations tested, the disjoint and sign-aligned superadditivity
  formulas, `d(d - 1)` on the uniform vector, and the normalized form, which
  is the l1-coherence of the normalized state.
- A1 is sharpened. On a fiber of the diagonal layer, `I` is constant exactly
  when the support has one point: with two nonzero coordinates, multiplying
  one of them by `-1` or by `i` changes `I`.
- `S4` is computed rather than declared: an architecture carries a U(1)
  connection on a finite carrier, and `S4` holds when that connection is not
  gauge trivial. `S3` stays a declared boolean; no Lieb–Robinson cone is
  computed. The rates are exact rationals. The only non-definitional content
  of B1 is that `rho(n) <= rho0` for every `n` exactly when `step <= 0`.
- The source's summary said that the four conditions are necessary and
  sufficient for computational advantage and partition finite architectures
  into classical and non-classical ones. Nothing computes advantage or
  simulability; `S` is a conjunction of predicates on declared data.
- C8 read the interference resource as non-coboundary holonomy and said the
  cross term was not yet a closed-form function of the holonomy. Over unit
  Gaussian rationals it is: for walks with a common source and sink,
  $I-\sum_p w_p=2\sum_{p<q}\sqrt{w_pw_q}\operatorname{Re}(H(p)\overline{H(q)})$ (QM_063). A
  gauge-trivial connection does not give zero interference. It makes every
  relative holonomy one and $I=(\sum_p\sqrt{w_p})^2$, again a function of the
  weights. The row stays interpretive.
- The ledger's evidence for C5, C6, C7, C12, C13 and C14 named test classes
  that the package does not contain (`TestInterferenceDeficitEngine`,
  `TestGraphComplex`, `TestSetSConditions`), and the package's mutation audit
  describes twelve mutations that do not match its test file.
- The package's Lean modules (`InterferenceDeficit`, `CoboundaryHolonomy`,
  `BuildabilitySetS`) now live in `lean4/quantum_mechanics/`. Its
  `GaussIntKernel.lean` duplicated QM_060's apart from a header comment, so the
  two were merged into one module. All of them compiled without `sorry` in the
  same staging build as QM_060's; that is a build, not a receipted replay.

**What stays outside.** QM-061-C9 (the complex phase carrier is imported),
C10, C11, C15 and C17 remain definitions and fences. C8 and C16 (threshold
theorems read as `S`-witnesses, the make-or-break read as `S1 ∩ S4`) stay
interpretive. Nothing here says that any device satisfies `S`, and no link
between `S4` and classical simulability is computed.

### 11.27 Selecting a $U(1)$ phase structure (QM-028 redirect removed; QM-062 qualified)

**Original paper in the paper archive:** [The $U(1)$ selector](sources/original_papers/062_the_u1_selector/the_u1_selector.md) (historical alias stub QM-028 removed from paper count; QM-062 retained with qualified algebraic scope).

The paper proposes a conditional complex-carrier selector. Its verified finite content is narrower:
1. **Complex structure matrix representation:**
   $$
   J = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}, \qquad J^2 = -I.
   $$
   Multiplication by $aI + bJ$ represents complex arithmetic over real matrices and Gaussian integers over integer matrices:
   $$
   (aI + bJ)(cI + dJ) = (ac - bd)I + (ad + bc)J.
   $$
2. **Conditional pairing selection on $\mathbb{Q}(i)$:**
   For the two field automorphisms $\sigma \in \{\operatorname{id}, \text{conj}\}$ of $\mathbb{Q}(i)$, the sesquilinear cross term of $B_\sigma(a, b) = \sigma(a)b$ scales under a common phase $u$ by $\sigma(u)u$. Conjugation makes this factor $1$ for all norm-one phases, whereas the identity automorphism leaves $u^2$. This selects the pairing involution within the already declared coefficient field $\mathbb{Q}(i)$; it does not select the field itself.

| Claim | Now computed by | Checked by (`tests/superposition/the_u1_selector.rs`) |
| --- | --- | --- |
| QM-062-C2 a conjugation is forced (Layer 1) | `complex_structure_selector::PairingInvolution` | for the two automorphisms `sigma` of `Q(i)`, a global phase `u` multiplies the cross term of `B(a,b) = sigma(a) b` by `sigma(u) u`: under conjugation the factor is 1 for all 20 test units and the cross term is `2 Re(conj(a) b)`; under the identity only `u = ±1` leave it invariant, and `B(i,i) = -1`; in a box of Gaussian rationals only `±i` square to `-1` |
| QM-062-C3 Frobenius comparison (Layer 2) | `multiplicative_order`, `close_under_multiplication`, `commuting_pairs` | `{±1}` has exponent 2; the group generated by two `2 x 2` Gaussian matrices realizing `i, j` has 8 elements and 40 commuting ordered pairs out of 64, while the quarter-turn group is abelian; `Q(zeta_n)` holds an element of order exactly `n` for `n = 3, 4, 5, 6, 8, 10, 12, 24`; `Q(i)` holds none of order 3, and `(3+4i)/5` has no order up to 1000 |
| QM-062-C4 the U(1)-versus-torsion gap (fence) | same | as above: roots of unity appear field by field, never all in one exact field |
| QM-062-C5 complex structure (Layer 3) | `regular_representation`, `regular_coordinates` | `J^2 = -I`, `S^2 = I` for `S = diag(1, -1)`, `J^2 != S^2`; `J` is the image of `i`, and `S` is not the image of any complex scalar |
| QM-062-C6 `C` as the `J`-algebra | same | `Q`-linearity and the products on the basis `{1, i}` decide that `a + b i -> [[a, -b], [b, a]]` is a unital ring homomorphism `Q(i) -> M_2(Q)`; it is also checked, with injectivity, on all 2401 pairs of Gaussian integers with coordinates in `-3..3` |
| QM-062-C7 `SO(2)` as the unit circle (interpretive) | same | unit Gaussian rationals go to rational rotations, `R^T R = I` and `det R = 1`, and products of units go to products of rotations; `2` goes to `2I`, which is not a rotation |

**Corrections, qualifications, and boundaries.**

- **$J^2 = -I$ does not establish continuous $U(1)$:** The subgroup generated by $J$ is $\langle J \rangle = \{I, J, -I, -J\} \cong \mathbb{Z}_4$ (order 4). It distinguishes a quarter-turn from a sign flip; it does not distinguish continuous from discrete dynamics. As mechanized in `lean4/U1TorsionExclusion.lean`, $J$ has exact order 4 and does not select a continuum phase group.
- **A complex subalgebra does not select a complex operational theory:** A real plane admits $J$, but also admits real reflections such as $Z = \operatorname{diag}(1, -1)$ with $ZJ = -JZ$. Embedding $\mathbb{R}[J] \cong \mathbb{C}$ into $M_2(\mathbb{R})$ does not make every permitted real operation complex-linear. Moreover, a real 2D plane equipped with $J$ corresponds to one complex dimension, not a two-level complex qubit.
- **Surviving compatibility condition:** For an operation $T$ to be complex-linear with respect to $J$, it must satisfy $TJ = JT$ (or intertwining between carriers).
- **Quaternionic comparison:** Quaternions contain abelian circle subgroups; excluding them requires stronger assumptions regarding the entire phase group.
- **QM-028 resolution:** The 11-line dual-alias redirect stub QM-028 is removed from the active paper count. The small algebraic results survive in QM-062, with the open field-selection obligation kept at its actual scope.

**What stays outside.** QM-062-C1 and C11 remain fences. C8 (conditional forcing) stays interpretive, and C9 and C10 (continuity of reversible dynamics; field uniqueness across dimensions) stay imports. No continuous $SO(2)$ or $U(1)$ is constructed. Field selection is not completed.

### 11.28 Holonomy-structured superposition

**Original paper in the paper archive:** [Holonomy-structured superposition](sources/original_papers/063_holonomy_structured_superposition/holonomy_structured_superposition.md).

The paper made a U(1) connection on a finite carrier an explicit import and
derived what follows under it: two-path interference is controlled by the
relative loop holonomy, holonomy and intensity are gauge invariant, every
connection on a tree is gauge trivial, face curvature is gauge invariant, and a
flat connection can keep global holonomy. All of it now computes exactly over
unit Gaussian rationals. Amplitudes `sqrt(w_p) H(p)` are formed only for
weights that are rational squares.

| Claim | Now computed by | Checked by (`tests/superposition/holonomy_structured_superposition.rs`) |
| --- | --- | --- |
| QCS-C1 normalization | `holonomy_interference::CoherentPathFamily::amplitudes`, `phase_blind_quotient::phase_blind_projection` | the phase-blind shadow of the amplitudes is `w / W = (4/13, 9/13)` under two different connections; zero total weight is refused |
| QCS-C2 two-path identity | `CoherentPathFamily::{sink_intensity, holonomy_expansion, relative_holonomy}`, `relative_loop` | on a square with `w = (1/4, 9/16)`, `h = (-56-33i)/65` is the holonomy of `p` followed by `q` reversed, and `I = 13/16 + 2 (1/2)(3/4) Re(h) = 173/1040`; a three-path family on a theta graph obeys the pairwise expansion |
| QCS-C3 gauge invariance | same, with `u1_graph_connection::VertexGauge` | intensity and relative holonomy are unchanged by a vertex gauge, while every amplitude picks up the one factor `g(t) conj(g(s))`; changing a single edge value moves the intensity |
| QCS-C4 L1 non-factorization | same | relative holonomy `1` and `-1` over one L1 packet give `(r_p + r_q)^2` and `(r_p - r_q)^2`, which differ by `4 r_p r_q`; equal weights `1/4` give 1 and 0 |
| QCS-C5 trees are gauge trivial | `TreeGaugeFixing` | all 64 quarter-turn connections on a four-vertex path, and a star with rational units, are gauged to the trivial connection |
| gauge classes (supporting C3, C5) | `TreeGaugeFixing::cycle_holonomies`, `gauge_equivalence` | the values left off a breadth-first spanning forest are the fundamental-cycle holonomies; gauge-related connections are recognized with an explicit relating gauge, and a changed cycle holonomy is refused; quarter-turn connections fall into 4 classes of 16 on a triangle and 16 classes of 64 on a filled square with diagonal |
| QCS-C6 face curvature is gauge invariant | `finite_cochain_packet::{face_coboundary, primitive_difference}`, `face_holonomies` | `d1 (x + d0 f) = d1 x` and `d1 d0 = 0` on the filled square with diagonal; face holonomies are gauge invariant; the face holonomies of `Exp(omega)` are `u^(d1 omega)` |
| Corollary 4.2, plaquette interference | `face_holonomies` | the face holonomy of the filled square equals `h_pq` and gives the intensity |
| QCS-C7 flat connections with global holonomy | `holonomy_verdict` | the triangle graph with holonomy `i` is `FlatNontrivial`, and the same edge values on the filled triangle are `Curved`; an annulus of four faces carries a flat connection with holonomy `(3+4i)/5` around the hole |
| Corollary 4.4, contractible 1-connected flat case | `holonomy_verdict` | all 1024 quarter-turn connections on the filled square with diagonal: 960 curved, 64 gauge trivial, none flat and nontrivial |
| QCS-C8 curvature needs a 2-cell | `holonomy_verdict`, `face_holonomies` | all 64 quarter-turn connections on the triangle graph: 48 flat and nontrivial, 16 gauge trivial, none curved; on the filled triangle: 48 curved, 16 gauge trivial |

**Corrections and scope.**

- The source took real weights and phases in `R/2piZ`. Here transports take
  values in the unit Gaussian rationals, a dense subgroup of `U(1)`, and a
  weight with an irrational square root is refused rather than approximated,
  as in `mass_phase_embedding`. The two-path identity is then an equality of
  rationals, and `cos(kappa_f)` is the real part of the face holonomy.
- The source derived Corollary 4.4 from the imported classification
  `H^1(X; R/2piZ) = Hom(H_1(X), U(1))`. What is computed is finite: a
  connection is gauge trivial exactly when its spanning-forest residual is 1,
  the residual classes of quarter-turn connections are counted exhaustively,
  and the verdict never reports a flat nontrivial connection on the filled
  square.
- The executable target QC-SUP-PL4 asked a verifier to reject inconsistent
  reverse-edge transport, endpoint mismatches and gauge-equivalence claims
  with unequal loop holonomy. Reverse transport is conjugation by
  construction, so it cannot be declared inconsistently; endpoint mismatches,
  irrational weights, and connections or walks from another carrier are
  refused; `gauge_equivalence` returns `None` when the residuals differ. A
  review found that a walk from another carrier was refused only when it
  named an edge the carrier lacks; a walk that fit the edge count was
  accepted, and `relative_loop` could panic on it. A walk must now replay on
  the carrier (`OrientedWalk::replays_on`), in `holonomy_interference` and in
  `U1Connection::holonomy`.
- The paper had no code or Lean package; its mechanization section listed
  targets only. The packaging annex QM_064 is absorbed into this entry.

**What stays outside.** QCS-C9 (higher-form holonomy) stays refused and
QCS-C10 stays a fence. QCS-C11, that the trace of a matrix-valued SU(2)
relative holonomy lower-bounds separability defects, is a conjecture without a
defined defect and is not implemented. Nothing here derives the U(1) carrier,
the square root or the quadratic readout; graphs and 2-complexes stay declared
carriers.

### 11.29 Phase-gauge residuals

**Original paper in the paper archive:** [Phase-gauge residual](sources/original_papers/064_phase_gauge_residual/phase_gauge_residual.md).

The package was an annex redirect to QM_063 and is absorbed into that entry.
Its four rows (`QM_064-C1` to `QM_064-C4`) appear only in the package's own
ledger, not in the consolidated repository record, so no ledger row changes. The
finite ones are computed as follows.

| Claim | Now computed by | Checked by (`tests/superposition/holonomy_structured_superposition.rs`) |
| --- | --- | --- |
| QM_064-C1 a gauge adds a primitive difference to the phase cochain | `finite_cochain_packet::primitive_difference`, `u1_graph_connection::CochainExponential::{connection, gauge}` | `theta + d0 alpha` and `theta` have the same loop integral 4 on the triangle; for `u = (3+4i)/5`, `Exp(theta + d0 alpha)` is the `u^alpha` gauge transform of `Exp(theta)` |
| QM_064-C2 cycle holonomy is gauge invariant | `holonomy_interference::{walk_integral, gauge_equivalence}`, `U1Connection::holonomy` | both connections have loop holonomy `u^4`, and `gauge_equivalence` recovers a relating gauge |
| QM_064-C3 a local gauge does not remove global holonomy | `TreeGaugeFixing`, `U1Connection::gauge_transform` | on the triangle with holonomy `i`, none of the 64 quarter-turn vertex gauges makes every edge value 1, and the spanning-tree gauge leaves `i` on the one edge off the tree |

**Corrections and scope.** C1 was written as
`(delta theta')(u,v) = (delta theta)(u,v) + (delta alpha)(u,v)`; it is read as
`theta' = theta + d0 alpha`. The Lean files the stub cited
(`003_qm_phase_fiber_interference.lean`, `003_qm_holonomy_curvature.lean`,
`003_qm_continuum_non_promotion.lean`) are not in `lean4/`; texts with these
topics survive as Markdown under `research/lean4/`.

**What stays outside.** QM_064-C4, a continuous Lie-group gauge lift read as
an external `L^2` observer projection, has no finite content.

### 11.30 Product non-factorization in bipartite systems (QM-070 merged into QM-071 and retired)

**Original paper in the paper archive:** [Product non-factorization as a bipartite obstruction](sources/original_papers/070_product_non_factorization_as_a_bipartite_obstruction/product_non_factorization_as_a_bipartite_obstruction.md); consolidated living home at [Consolidated Account](../../003_quantum_foundations/qm_071_entanglement_as_a_separability_obstruction.md).

The paper defined the product defect of a finite joint weight table,
`delta_prod(w) = w - w_A (x) w_B / W`, and its `l1` mass `Phi(w)`. It stated that
the mass vanishes exactly on tables that factor, and that the mass is blind
to entanglement. Both compute exactly in sovereign Rust. Standalone paper QM-070
is now retired and merged into the consolidated correlation and separability
account (QM-071). Factorization is decided through `2 x 2` minors, so the
equivalence compares two independent computations. The entanglement firewall is
an explicit countermodel.

| Claim | Now computed by | Checked by (`tests/entanglement/product_non_factorization.rs`) |
| --- | --- | --- |
| QM-070-C1 carrier (definition) | `joint_table::JointTable::new` | empty, ragged, negative and zero-total declarations are refused |
| QM-070-C2 phase-blind descent (definition) | `bipartite_operator::descend_to_table` | `w(a,b) = <u_a v_b\| rho \|u_a v_b> / (\|u_a\|^2 \|v_b\|^2)` in declared local orthogonal bases; non-orthogonal or zero basis vectors and non-PSD operators are refused |
| QM-070-C3, C4 defect and ZeroRel (definitions) | `JointTable::{marginal_a, marginal_b, product_defect}` | the exact defect `(1/4, -1/4, -1/4, 1/4)` of the diagonal-half table |
| QM-070-C5 mass zero exactly on products | `JointTable::{product_defect_mass, has_vanishing_minors}` | the two agree on every nonzero `2 x 2` table with entries `0..3` (255 tables, 63 products), `2 x 3` with entries `0..2` (728, 92) and `3 x 3` with entries `0..1` (511, 49) |
| QM-070-C6 witnesses | same | diagonal half: uniform marginals, mass 1; uniform quarter: mass 0 |
| QM-070-C7 Bell state and classical mixture | `bipartite_operator::{descend_to_table, partial_trace_a, partial_trace_b, is_ppt, DecomposableWitness, ProductDecomposition}` | both give the diagonal-half table and the reduced states `I/2`; the Bell state has a non-PSD partial transpose, and `W = \|Psi-><Psi-\|^(T_B) = I/2 - \|Phi+><Phi+\|` gives it `-1/2`; the mixture is PPT, gets `0`, and decomposes into product states; `W` is nonnegative on 49 declared product states; the certificate is refused for `-I` (not PSD) and `2 Phi+` (trace 2), which also pair negatively with `W` |
| QM-070-C8 local maps | `JointTable::{apply_local_maps, convex_mixture}` with `finite_classical_shadow::StochasticMap` | products stay products under three map pairs; the mass of `[[3,1],[0,2]]` falls from 4 to `1/2` and to `1/3`, and a permutation leaves it at 4; a half-and-half mixture of `id x id` and `flip x flip` takes a point table (mass 0) to the diagonal-half table (mass 1); hand-built maps that are not row-stochastic are refused on either side |
| QM-070-C9 basis dependence | `descend_to_table` in declared bases | the mixture has mass 1 in the `Z x Z` basis and 0 in the Hadamard basis; the Bell state has mass 1 in the Hadamard basis and 0 in the mixed `Z x X` basis |
| QM-070-C11 dependence gauge (interpretive) | `JointTable::l1_distance` | the mass is the `l1` distance to the marginal product; a product table lies at distance `21/25 < 1` from the diagonal-half table |

**Corrections and scope.**

- The source called the mass `Phi` and read the equivalence classes of
  equal defect as a quotient `Q^1_prod` with the mass as its gauge. The mass
  is the raw `l1` norm of a nonlinear defect, named `product_defect_mass`. It
  is the distance to the product of the table's own marginals; for normalized
  $p = w/W$, $\Phi(w)/(2W) = \frac{1}{2}\|p - p_A \otimes p_B\|_1$ is the
  scale-independent total-variation distance to the marginal product.
- Contraction under independent stochastic maps: for independent column-stochastic
  maps $K_A, K_B$, $\delta_{\mathrm{prod}}((K_A \otimes K_B)w) = (K_A \otimes K_B)\delta_{\mathrm{prod}}(w)$.
  Because stochastic maps contract $\ell^1$ norm, $\Phi((K_A \otimes K_B)w) \le \Phi(w)$.
  This settles the classical extension noted in the original §10. The hypothesis
  of independent maps is required: a mixture of local maps (shared random bit)
  can prepare correlated tables from a product state, raising $\Phi$ without entanglement.
- Information-loss boundary: every product-basis table $p_{ab}$ has the separable
  realization $\rho_{\mathrm{diag}} = \sum_{a,b} p_{ab} |a\rangle\langle a| \otimes |b\rangle\langle b|$.
  Thus, a single measurement table alone cannot certify entanglement.
- The Bell state $\rho_B = |\Phi^+\rangle\langle\Phi^+|$ and the classical mixture
  $\rho_C = \frac{1}{2}|00\rangle\langle00| + \frac{1}{2}|11\rangle\langle11|$
  yield the exact same table $p = (1/2, 0, 0, 1/2)$ and $\Phi = 1$, yet $\rho_C$
  is separable. Conversely, $|\psi\rangle = \frac{1}{2}(|00\rangle+|01\rangle+|10\rangle-|11\rangle)$
  is entangled (rank 2 coefficient matrix), but gives a uniform table with $\Phi = 0$.
- The cited Lean module `QM.ProductNonFactorization` (ENC-1123) is not in
  `lean4/`. The Rust checks replace it.

**What stays outside.** QM-070-C10 (firewall and authority fence) and
QM-070-C12 (falsifiability) remain fences. QM-070-C11 stays interpretive;
mutual information and Kullback–Leibler divergence are not computed. Multipartite
gluing is not addressed. Standalone draft QM-070 is retired.

### 11.31 Consolidated Account: Classical Independence, Finite-Catalogue Hull Obstruction, and Quantum Separability (QM-071 consolidated with QM-070)

**Original paper in the paper archive:** [Entanglement as a separability obstruction](sources/original_papers/071_entanglement_as_a_separability_obstruction/entanglement_as_a_separability_obstruction.md); consolidated living home at [Consolidated Account](../../003_quantum_foundations/qm_071_entanglement_as_a_separability_obstruction.md).

The consolidated account unifies the classical independence diagnostic of QM-070
with the convex-hull witness theorem of QM-071, replacing the old toy quantum
discussion with the sovereign universal Bell witness and removing historical
backlog tasks. Both directions of finite-hull membership now compute: for an
explicitly declared finite family $P$, completeness is finite LP duality. Every
vector receives either a verified convex decomposition or a verified separating
functional via `omega_solvers::solver_convex_finite_hull`.

| Claim | Now computed by | Checked by (`tests/entanglement/separability_witness.rs`) |
| --- | --- | --- |
| QM-071-C3, C4, C7 defect, ZeroRel, `P`-nonseparability (definitions) | `solver_convex_finite_hull::{DeclaredFamily, ConvexDecomposition::verify}` | negative weights, weights not summing to one, wrong counts and wrong reconstructions are refused |
| QM-071-C5 witness soundness | `SeparatingWitness::{verify, value_on_decomposition}` | for all 25 integer functionals on `[-2, 2]^2`, with the tightest threshold the family satisfies, the value on a decomposed point equals `sum_k lambda_k phi(P_k)` and never falls below the threshold; a functional that fails on a member, or does not fall strictly below, is refused |
| QM-071-C6 worked witnesses & Bell witness | `ConvexDecomposition::verify`, `SeparatingWitness::verify`, `decide_membership`, `bipartite_operator::DecomposableWitness` | `(1/2, 1/2, 0) = (P_0 + P_1)/2`; `(0, 0, 1)` separated by `phi = (1, 1, 0)`, `t = 1`; the zero vector separated from the unit vectors by the all-ones functional; universal Bell witness $F = \frac{1}{2}I - \rho_B = Q^{T_B}$ ($Q \ge 0$) checks $\operatorname{Tr}(F\rho_B) = -1/2$ and $\operatorname{Tr}(F\rho_C) = 0$ |
| QM-071-C8 family-preserving maps | `transport_decomposition`, `apply_linear_map` | a map that keeps the simplex inside the target hull carries `(1/3, 1/3, 1/3)` to `(1/2, 1/2)`; a map that sends `e_1` outside is refused, naming that member |
| QM-071-C9 completeness over declared finite family | `decide_membership` | 36 grid points against the unit square: 16 members with verified decompositions and 20 points with verified witnesses, exactly the points with `0 <= x, y <= 1` |
| QM-071-C10 relative to a declared family | `decide_membership`, `bipartite_operator::{hermitian_coordinates, ProductDecomposition, is_ppt}` | `(\|++><++\| + \|--><--\|)/2` is separable (explicit decomposition, PPT, product computational table), yet it is separated from the four computational product states; declaring its two components makes it a member; the Bell state stays separated from the enlarged family |
| QM-071-C13 no verdict without a certificate (fence) | `decide_membership` | every returned certificate is re-verified directly; a solver or replay refusal is an error, never a verdict |

**Corrections, Scope, and Backlog Pruning.**

- **Finite-Hull Completeness Resolved:** For a declared finite rational family,
  membership is the linear program $P\lambda = w, \mathbf{1}^T\lambda = 1, \lambda \ge 0$.
  Finite LP duality supplies the decomposition-or-separator alternative. The solver
  in `omega_solvers` constructs exact primal/dual certificates. Algorithmic pivot
  budgets do not make completeness an unclosed theorem.
- **Bell Instantiation Resolved:** The universal partial-transpose witness
  $F = \frac{1}{2}I - \rho_B = Q^{T_B}$ ($Q = |\Psi^-\rangle\langle\Psi^-| \ge 0$)
  satisfies $\langle a \otimes b | F | a \otimes b \rangle \ge 0$ for every product
  vector by Cauchy–Schwarz. By convexity $\operatorname{Tr}(F\rho) \ge 0$ for all
  separable states. It yields $\operatorname{Tr}(F\rho_B) = -1/2$ and $\operatorname{Tr}(F\rho_C) = 0$.
  Both the Bell instantiation and finite-hull completeness are removed from the
  research backlog.
- **$P$-Nonseparability vs. Entanglement:** Exclusion from a finite catalogue
  $P$ ($\varphi(P_k) \ge t, \varphi(w) < t$) certifies $w \notin \operatorname{conv}(P)$,
  not general entanglement. Pure product state $w = |++\rangle\langle++|$ has entries
  $1/4$; under functional $\varphi(\rho) = -\operatorname{Re}\rho_{00,11}$ with $t = 0$,
  $\varphi(P_k) = 0$ on all computational basis products, while $\varphi(w) = -1/4 < 0$.
  Thus $w$ is excluded from the computational product hull despite being a pure product
  state. Pure product states are extreme points; finite matrix dimension does not make
  the product family finite.
- **Classical Tables Cannot Be Given a Convex-Product Test:** Every normalized table
  already decomposes as $p = \sum_{a,b} p_{ab} \delta_a \otimes \delta_b \in \operatorname{conv}(\text{classical products})$.
  Convex product testing requires quantum state operators and admissible local states.
- **Preservation of Convex Constraints:** Weights $\lambda_k \ge 0, \sum_k \lambda_k = 1$
  are essential. The real linear span of product density matrices is the entire space
  of bipartite Hermitian matrices; relaxing convexity to linear combinations would make
  Bell states pass the linear representability test and erase entanglement.
- Standalone drafts QM-070 and QM-071 are retired into redirect stubs; the consolidated
  account is published in `003_quantum_foundations/qm_071_entanglement_as_a_separability_obstruction.md`.

**What stays outside.** General separability over the continuous manifold of
unrestricted product states in arbitrary dimension (known to be NP-hard),
multipartite entanglement structures, and asymptotic entanglement distillation.
QM-071-C11 remains a fence. QM-071-C12 stays interpretive. Both standalone drafts
QM-070 and QM-071 are retired.

### 11.32 From classical bits to qubits

**Original paper in the paper archive:** [Bit models and qubits](sources/original_papers/072_bit_shadow_and_qubit/bit_shadow_and_qubit.md).

The paper corrected its own brief. The two-locus one-edge carrier supports a
bit-shadow, not a qubit. Its finite content now computes over `F_2` and
`Z/n`:

- the two-pattern alphabet;
- removability on the edge, relative to the declared family of repairs;
- the parity-forced obstruction of the triangle, and its least-ness among
  small simple graphs;
- the two exchange characters of a pair.

The qudit contraction conjecture appended to the paper (P7-C10) fails on
exact qubit channels.

| Claim | Now computed by | Checked by (`tests/entanglement/bit_shadow.rs`) |
| --- | --- | --- |
| P7-C1 carrier and alphabet | `binary_pattern_carrier::PatternCarrier::{pattern_count, coboundary, image}` | two patterns; constant assignments give `same`, separating ones give `diff` |
| P7-C2 tree-triviality over a family full for the cut (conditional) | `PatternCarrier::{image, is_removable, has_unremovable_pattern}` | all 16 families on the edge: the image is both patterns exactly for the 9 families holding a constant and a separating assignment; the full function space removes every pattern |
| P7-C3 family-indexed binary residual (conditional) | `PatternCarrier::binary_residual` | the residual is 0 or 1 for all 15 nonempty families; `diff` keeps residual 1 exactly when no separating assignment is declared (3 families), `same` exactly when no constant one is (3); the empty family is refused |
| P7-C4 three-way minimality split | `PatternCarrier::{is_even_subgraph, has_cycle}`, `pattern_pairing`, `simple_graphs`, with `finite_cochain_packet::FiniteCochainPacket::dimensions` | the triangle's all-`diff` pattern pairs to 1 with the even subgraph while every coboundary pairs to 0; the triangle's image is the four even patterns and the residual is 1; on all 75 simple graphs with up to four vertices, an unremovable pattern exists exactly when there is a cycle, exactly when the rational `H^1` is nonzero (1 of 8 graphs on three vertices, 26 of 64 on four); the three-edge ones are the 5 triangles; with parallel edges a digon is already forced |
| P7-C5 two exchange characters (conditional) | `pair_exchange_characters::exchange_characters_mod` | exactly `{1, p - 1}` for the primes 3 to 61; one character in `Z/2`, four in `Z/8` |
| P7-C8 superposition obstructed (finite part only) | `mass_phase_embedding::MassPhaseEmbedding` | masses `(9, 16)` with phases `(1, 1)` and `(1, -1)`: the same Born weights, interference terms `24/25` and `-24/25` |
| P7-C10 qudit contraction conjecture | `qubit_bloch_map::QubitBlochMap` | false at `d = 2`: complete dephasing and a rational measure-and-prepare channel have `\|T\| = 1` exactly, rank 1, and lose coherence (the purity of `\|+>` goes to `1/2`); the replacement channel has `\|E(r)\| / \|r\| = 10` at `r = (1/10, 0, 0)`; amplitude damping at `gamma = 9/25` and a noisy measure-and-prepare channel are strict contractions; a rational rotation is an isometry |

**Corrections and scope.**

- The least-ness of the triangle was proposed but not proved. It is
  now decided for simple graphs on up to four vertices. It depends on the
  carrier convention: if two edges may join the same pair of loci, a digon
  already carries a pattern that no family removes. The general statement
  follows from `rank d0 = |V| - (number of components)` over `F_2`: every
  pattern is removable on a forest, and some pattern is not removable on a
  graph with a cycle. The tests compare it on all small graphs with a
  union-find cycle test and with the rational `H^1` of
  `finite_cochain_packet`.
- The parity-forced residual has a dual certificate. An even subgraph `z` has
  `<d0 f, z> = 0` for every assignment `f`, so `<h, z> = 1` rules out every
  repair family at once. This is the `F_2` counterpart of the circulation
  dual of `Phi1`.
- The source's "Adm-indexed `Phi1`" is a Hamming distance over `F_2` with
  unit weights. It is named `binary_residual`. It is not the rational
  quotient mass of `omega_functional`.
- The exchange dichotomy uses two separate hypotheses: `x^2 = 1` must force
  `x = +-1` (an integral domain), and `+1 != -1`. `Z/8` has four characters
  and `Z/2` has one. Over `Q` and `Q(i)` both hypotheses hold.
- P7-C10 is false as stated, under either reading. Read on the affine Bloch
  map, `gamma(E) <= 1` fails for the replacement channel. Read on the linear
  part, a strict contraction is not necessary for loss: dephasing and
  measure-and-prepare lose coherence at norm exactly one. For qubits the
  linear part of a positive trace-preserving map always has norm at most
  one, because the Bloch ball maps into itself; the tests check this on the
  declared channels only.
  The row is now typed `REFUTED BY COMPUTATION`, citing the countermodel test.
- The finite product-pattern obligation is discharged by exhaustive Rust computation over
  all 16 families on the edge, not by Lean.

**What stays outside.** P7-C6 and P7-C7, the price list and its completeness
reading, stay open and interpretive. Their finite parts are computed
elsewhere: the phase fiber as the mass/phase embedding of §11.1, the
interference boundary in QM_061's entry, and the Mermin–Peres parity core in
`separating_predictions::MerminPeresSquare`. Continuity of dynamics has no
finite content. P7-C8's claim about derivability, and P7-C9's naming ruling,
have no finite content beyond the rows above. No qubit, Hilbert space or
Bloch sphere is derived; the qubit Bloch maps are declared channels.

### 11.33 Correlation, separability, and finite Bell bounds

**Original paper in the paper archive:** [Correlation, separability, and finite Bell bounds](sources/original_papers/073_correlation_separability_finite_bell/correlation_separability_finite_bell.md).

The paper proved three finite results. Every bare joint table is a mixture of
point product tables. Every box with a single joint table satisfies
`|S| <= 2`. Exchange equivariance under the alternating character removes
weight from diagonal loci. It then priced the ways past the bound. All three
results now compute exactly, together with the two boxes that go past the
bound without a joint table: the PR box, and an entangled box with rational
entries. Its annex, QM_074, is covered here.

| Claim | Now computed by | Checked by (`tests/entanglement/finite_bell_bounds.rs`) |
| --- | --- | --- |
| P8-C1 composite carriers, joint tables, marginals (conditional) | `joint_table::JointTable` | as in QM_070's entry |
| P8-C2 product defect criterion (corpus standard) | `JointTable::product_defect_mass` | QM_070's exhaustive check |
| P8-C3 general separability of bare tables (conditional) | `JointTable::{point_product_decomposition, convex_mixture}` | every nonzero `2 x 2` table with entries `0..3` (255) and `2 x 3` table with entries `0..2` (728) equals the mixture of its point tables, each of mass 0; against the four point tables, `decide_membership` returns a verified decomposition for all 255 |
| P8-C4 no entanglement at the bare-table grade (conditional) | same, with `bipartite_operator` | the diagonal-half table has mass 1 and equals `e_00/2 + e_11/2`; the Bell state and the classical mixture share it (QM_070) |
| P8-C5 relative machinery (corpus standard) | `declared_family_separability` | QM_071's entry |
| P8-C6 finite CHSH bound (conditional) | `finite_chsh_correlations::{JointAssignment, PairwiseBox::from_joint_table}` | the 16 joint assignments give `S = 2` eight times and `S = -2` eight times; five joint tables give `S = 0, 2, -2/3, 1, -2`, each without signalling; the CHSH functional is at least `-2` on every assignment's marginal vector |
| P8-C7 the PR box: `S = 4`, no joint table (conditional) | `PairwiseBox::{chsh, support_compatible_assignments, joint_extension}`, `chsh_witness` | `S = 4`; no signalling; no joint assignment fits the supports; the CHSH functional separates it with gap 2; `joint_extension` returns a verified separating functional |
| P8-C8 violation doors (source claim remains open) | `PairwiseBox::from_state` | door V1 is the PR box; door V2: `\|Phi+>` with `A_0 = Z`, `A_1 = X`, `B_0 = (4Z + 3X)/5`, `B_1 = (3Z - 4X)/5` gives `S = 14/5 > 2` with `S^2 < 8`; the source's broader pricing/derivation claim is not discharged |
| Current Bell endpoint (conditional on the declared quantum model) | `finite_chsh_correlations::{tsirelson_certificate, verify_tsirelson_certificate}`, `tensor_commuting_correlation_frontier::chsh_game_certificate` | the real matrices `A_0=Z`, `A_1=X`, `B_0=(Z+X)/sqrt(2)`, `B_1=(Z-X)/sqrt(2)` give an exact sum-of-squares certificate for `-2 sqrt(2) I <= B_CHSH <= 2 sqrt(2) I` and `\|Phi+>` attains `S=2 sqrt(2)`; every state and observable entry is fixed by conjugation |
| P8-C9 diagonal suppression (conditional) | `pair_exchange_characters::{is_exchange_equivariant, alternating_fixed_values_mod}` | of the 625 `2 x 2` tables with entries in `-2..2`, the 5 equivariant under the alternating character have zero diagonal, while 120 of the 125 symmetric ones do not; in `Z/n` (`n <= 64`), `c = -c` forces `c = 0` exactly for odd `n`; in `Z/4` the value 2 survives |
| QM_074 no-signalling (annex) | `PairwiseBox::{is_no_signalling, context_table}`, `bipartite_operator::partial_trace_b` | see QM_074's entry |

**Corrections and scope.**

- Door V2 does not need the radical for a violation. `|Phi+>` has a rational
  density matrix and the four observables have rational entries, and the box
  already reaches `S = 14/5 > 2`. The exact owner now also certifies the operator
  inequalities `-2 sqrt(2) I <= B_CHSH <= 2 sqrt(2) I` by two sum-of-squares
  identities and
  evaluates the standard `|Phi+>` witness at `S = 2 sqrt(2)`. The witness uses
  only the real subfield `Q(sqrt(2))` of `Q(zeta_8)`; no complex phase or time
  evolution enters this static construction. The Rust test
  `measurement_exact_laws::chsh_square_sos_attainment_and_moment_replay_reject_corruption`
  checks the square identity, both operator certificates, the state-derived
  moment matrix, exact attainment and a corrupted-certificate refusal.
- Door V2 uses `B_1 = (3Z - 4X)/5`. The main paper (§13.8, Test 2) uses
  `B_1 = (4Z - 3X)/5` instead, a different rational observable with correlation
  vector `(4/5, 4/5, 3/5, -3/5)` and the same `S = 14/5`; the Lean fixture
  `bellNumerator` in `lean4/CarrierTests.lean` encodes that
  table's numerators over 20.
- Joint extension is decided for any box. The box is a vector in `Q^16`, and
  a joint table exists exactly when that vector lies in the hull of the 16
  marginal vectors of joint assignments. `declared_family_separability`
  returns either the joint table or a separating functional. The paper's
  support ("parity") check decides the PR box but not the rational entangled
  box, whose probabilities are all positive.
- The finite CHSH bound is decided completely. The 16 vertex values are all
  `+-2`, and `S` is affine in the joint weights.
- The corrected orientation statement is confirmed: `c = -c => c = 0` holds
  where 2 is not a zero divisor and fails in `Z/4`.
- `lean4/CarrierTests.lean` states `weighted_chsh_bound`
  (the CHSH score of every finite nonnegative joint table lies between `-2`
  and `2` times its mass), `context_score_from_marginals`, and
  `bell_has_no_positive_joint_extension` (no joint table of positive mass
  reproduces that file's rational Bell fixture, the main paper's
  `B_1 = (4Z - 3X)/5` table with denominator 20). The file is a root of the
  repository-level `lean4/lakefile.lean` (library `QmCarrierTests`), not of
  the `lean4/quantum_mechanics/` workspace, and imports `ExactRat` and
  `ShadowBoundary` from `lean4/`. The 2026-10-14 code-companion archive
  carries `CarrierTests.lean` but neither that lakefile nor the two imported
  modules, so the file does not build from the archive alone; no build was run
  for this entry. The door V2 box itself rests on the exact Rust computation. The mechanized corpus
  results the paper builds on (ENC-1123, ENC-1124) have no Lean module in
  `lean4/`, as recorded in QM_070's and QM_071's entries.
- The paper types these results as conditional on corpus packages (the
  scalar package, H1–H3, K9, K10). Over `Q` and `Q(i)` those conditions hold,
  and the computations above use no further hypothesis. The ledger types are
  left as they are.

**What stays outside.** P8-C10: applying Bell's theorem to nature requires
local-response factorization, setting independence and an empirical
identification of preparations, settings and outcomes. No continuum premise
is needed for the finite CHSH contradiction. P8-C11: the physics readings.
The Tsirelson ceiling [17] and attaining witness are now derived **inside a supplied
finite quantum model**; tensor composition, positivity, the state, observables
and trace/Born pairing remain declarations rather than consequences of `<>`.

### 11.34 A finite no-signaling model

**Original paper in the paper archive:** [No-signaling finite model](sources/original_papers/074_no_signaling_finite_shadow/no_signaling_finite_shadow.md).

The package was already a redirect stub pointing to QM_073, and it is
absorbed into that entry. Its four claim rows (`QM_074-C1` to `QM_074-C4`)
appear only in the package's own ledger, not in the consolidated repository record,
so no ledger row changes. The finite ones are computed as follows.

| Claim | Now computed by | Checked by (`tests/entanglement/finite_bell_bounds.rs`) |
| --- | --- | --- |
| QM_074-C1 no-signalling marginals | `finite_chsh_correlations::PairwiseBox::{from_state, is_no_signalling}` | the box of `\|Phi+>` with rational observables, the PR box and the five jointly tabled boxes of QM_073's entry do not signal; boxes that signal towards either side are detected |
| QM_074-C2 local marginal independent of the remote choice | `bipartite_operator::partial_trace_b`, `no_signalling::verify_no_signalling_on_bell_states` | a rational rotation or a dephasing on the second factor changes the state of `\|Phi+>` but not its first reduced state `I/2`; the crate's existing Bell-state check covers operations on the first factor |
| QM_074-C3 no-signalling does not imply factorization | `PairwiseBox::{context_table, joint_extension}`, `joint_table::JointTable::product_defect_mass` | the rational entangled box does not signal, yet its four contexts have product-defect masses `4/5, 3/5, 3/5, 4/5` and it has no joint table |

**Corrections and scope.** The stub cited Lean files
(`003_qm_no_signalling_marginal.lean`, `003_qm_product_non_factorization.lean`,
`003_qm_continuum_non_promotion.lean`) that do not exist in `lean4/`. C1 was
phrased with a derivative, `d rho_A / d y = 0`. On a finite box it means that
the marginal is equal across the finite set of remote settings, which is what
is checked.

**What stays outside.** QM_074-C4, light-cone causality as an `L^2` observer
projection, has no finite content. No locality or spacetime structure is
derived.

### 11.35 Trace-norm geometry and dual witnesses for quantum channels

**Original paper in the paper archive:** [CPTP trace-norm geometry and quantum dual witnesses](sources/original_papers/080_cptp_trace_norm_geometry_and_quantum_dual_witnesses/cptp_trace_norm_geometry_and_quantum_dual_witnesses.md).

The paper puts the trace distance $\frac12\|\cdot\|_1$ on Hermitian trace-zero
edge defects of a finite directed graph, takes the quotient by trace-zero
vertex repairs, and describes its dual by bounded divergence-free observable
circulations. `trace_distance_quotient` now certifies that quotient exactly. A
primal certificate (repairs and PSD splits of the residuals) bounds it from
above, a dual certificate (edge observables in operator-norm balls, decided by
exact PSD tests) bounds it from below, and the value is returned only when the
two agree. `trace_norm_certificate` supplies the exact trace norms, the
operator-norm balls, the dual-ball lemma and the qubit closed form, and
`difference_transport_channel` decides what CPTP monotonicity leaves free. One
of the paper's dual formulas is false; the correct one is computed, and the
countermodel is below.

| Claim | Now computed by | Checked by (`tests/channels/cptp_trace_norm_geometry.rs` unless noted) |
| --- | --- | --- |
| C2, C6 CPTP monotonicity does not fix the gauge's scale; Schatten `p > 1` are not monotone | `tower_walk_validator` (rescaling), `difference_transport_channel::DifferenceTransport`, `trace_norm_certificate::SignCertificate::schatten_power` | `native/tests/tower_walk_registry.rs`: the half trace norm contracts under three rational channels, and so does every positive multiple of it; here `X = Z (x) I/2` and `Tr_B X = Z` have trace norm `2`, the `p`-th powers grow by exactly `2^(p-1)` for `p = 2..6`, and the operator norm grows `1/2 -> 1`; `tests/channels/trace_norm_transport_audit.rs`: the scale is the only freedom |
| C9 quotient invariance | `trace_distance_quotient::TraceDefectPacket::{residuals, certify, diagonal_certificates}` | on `K_{2,3}` with qutrit defects, a non-diagonal trace-zero coboundary shift carries the certificates along and keeps the value `6`; after a diagonal shift the replayed weighted-`l1` optimum is `6` again while the unrepaired edge mass moves from `6` to `12`; a coboundary certifies `0` |
| C10 trace-zero dual ball | `trace_norm_certificate::{dual_ball_value, sum_zero_dual_pair, within_operator_ball}` | for $\left(\begin{smallmatrix}1&2&0\\2&1&0\\0&0&-2\end{smallmatrix}\right)$, declared eigenvectors of $3$ and $-2$ and the exact ball test certify diameter $5$, attained by a trace-zero $X$ with $\frac12\|X\|_1=1$; the value ignores $M\mapsto M+7I$; a non-extreme or non-eigen declaration is refused; $\operatorname{diag}(1,0)$ has diameter $1$ but operator norm $1$, so the dual norm is not twice the operator norm; eigenvalue core: $\operatorname{sign}(x)/2$ attains $\frac12\|x\|_1$ and a transport plan bounds every $m$ of spread at most one, on all 85 sum-zero $x\in\{-2,\ldots,2\}^4$ |
| C11 quotient duality as stated, with uncentred witnesses; C12 corrected to them | `TraceDefectPacket::{upper_bound, lower_bound, certify, diagonal_certificates, cycle_certificates}` | equal bounds on every packet below; the countermodel in the next row |
| C12, C13, C14 the centred, exactly divergence-free dual (false) | same | `K_{2,3}`, defects `3E_kk - I` on the legs `u -> w_k`: trace-zero value `6` (no repair; `M_k = D_k/3` on both edges of leg `k`, exactly divergence-free, centre `1/6`, operator norm `2/3`), all-Hermitian value `9/2`; centring `M_k` keeps `6` only with divergence `I/2` at `u`; exactly divergence-free witnesses of operator norm `1/2`, such as `diag(1/2, -1/4, -1/4)` or the centred `diag(1/2, -1/2, 0)` and their cyclic shifts, reach `9/2` and leave a gap of `3/2`; on qubits the two values agree (`5`) |
| C12 cycle support and tree vanishing | `cycle_certificates`, `lower_bound`, `finite_cochain_packet::dimensions` | a path has $h_1=0$, is repaired exactly, and refuses a nonzero circulation; on a triangle with a tail the tail edge carries no exactly divergence-free witness; on a weighted 4-cycle with two reversed edges, $\Phi=w_{\min}\frac12\|S\|_1=3/2$, with residual $-S$ on the lightest edge; $\operatorname{diag}(1,1,-1,-1)$ needs the full sign witness (value $2$), while the rank-two difference gives $1$ |
| C15 one-qubit cycle replay | `cycle_certificates` | triangle with defect $Z$: $\Phi=1$ for both repair spaces, witness $Z/2$ on every edge, $\|Z/2\|_{\mathrm{op}}=1/2$, and $\operatorname{Tr}((Z/2)Z)=1$ |
| Depolarizing contraction | `exact_channel::{apply_choi, choi_is_cptp}`, `su_n::GellMannBasis` | the Choi matrix `(1-p)\|Omega><Omega\| + (p/d) I`, with `\|Omega> = sum_i \|ii>` unnormalized, is CPTP at `p = 0, 3/10, 1, 4/3` and not at `-1/10, 3/2` (`d = 2`), CPTP at `1/2, 9/8` and not at `5/4` (`d = 3`); on every Gell-Mann generator the map is `1 - p` times the identity, so every trace-zero difference contracts by exactly `\|1 - p\|`; the sampled pair goes `2 -> 7/5`, and the half trace norm `sqrt(34)/10 -> 7 sqrt(34)/100` |
| The polar witness attains the trace norm | `trace_norm_certificate::qubit_polar_pairing`, `tower_walk_validator::half_trace_norm_2x2` | on the three sampled pairs `X^2 = qI`, so `W = X / sqrt(q)` is a Hermitian unitary with `Tr(WX) = sqrt(34)/5, sqrt(2), sqrt(37)/5`, equal to twice `half_trace_norm_2x2`; `-W` gives the negative |
| sign certificates | `SignCertificate`, `sign_from_spectrum` | trace norm `6`, Jordan parts and `Tr\|X\|^p = 6, 14, 36` of the example; Pauli `X` from two declared eigenvalues; a declared value outside the spectrum gets a zero projector; each of the four sign identities and an incomplete or repeated declared spectrum is refused |

**Corrections and scope.**

- **The dual formula.** Theorem 5 states $\Phi=\max_M\sum_e\operatorname{Tr}(M_e\delta_e)$
  over $d_0^*M=0$ with
  $\lambda_{\max}(M_e)-\lambda_{\min}(M_e)\leq1$. That
  statement is right, and it is what the lower bound checks (one centre `c_e`
  per edge). But the proof ends, and Theorem 6's set `W`, the §2.6b dual SDP,
  §2.8's `W_tr` and §2.9 continue, with centred witnesses
  ($\|M_e\|_{\mathrm{op}}\leq1/2$)
  that are exactly divergence-free. That set is the dual of the quotient by
  *all* Hermitian repairs, scalar parts included. The proof's step "finite
  iff `d0* M = 0`" is, for trace-zero repairs, "finite iff every `(d0* M)_v`
  is a multiple of `I`", and §2.6b drops the multipliers of its own trace-zero
  constraints. On `K_{2,3}` with defects `3E_kk - I` the trace-zero quotient is
  `6`; every exactly divergence-free witness of operator norm at most `1/2`,
  centred or not, gives at most `9/2`, which the all-Hermitian repair
  certifies. Centring the right witness is harmless for the value but moves the
  divergence to a multiple of `I`. The two quotients agree on qubits (scalar
  parts never lower the trace norm of a trace-zero `2 x 2` matrix) and on a
  single cycle, for every `n`, so the gap needs `n >= 3` and two independent
  cycles. Those two agreements are prose arguments; the tests check one qubit
  packet and three cycles. The source's tests covered only cycles,
  trees and qubits, and its LP code centred the multipliers and noted that the
  divergence was then zero "modulo scalar identity".
- **Selection.** Under axiom 1 (absolute homogeneity) and axiom 2 (CPTP
  monotonicity) the gauge is already $c\|\cdot\|_1$. The measure-and-prepare map of
  `difference_transport_channel` sends any trace-zero `X` to any `Y` with
  $\|Y\|_1\leq\|X\|_1$, so a CPTP-monotone gauge is a nondecreasing function of
  the trace norm, and the embedding pair gives one `c` for all dimensions.
  CPTP monotonicity is therefore not inert: it implies unitary invariance and
  fixes total-variation reduction up to that scale. What it leaves free is one
  number. PL-005-2 (a CPTP-monotone norm not proportional to the trace norm)
  is answered in the negative for every norm, not only in the Schatten family.
  Inside one dimension the countermodels need `n >= 3` (Hilbert–Schmidt) and
  `n >= 4` (operator norm); on trace-zero qubits every unitarily invariant norm
  is a multiple of the trace norm.
- **Exactness.** The source solved the duality numerically (HiGHS, ADMM) with
  tolerances. Here nothing is optimised over matrices: certificates are
  declared or built in closed form and replayed exactly. For diagonal defects
  the value comes from `finite_cochain_packet::certified_quotient_mass` on a
  stacked cochain with a declared rational repair map (`omega_solvers`
  proposes, `omega_functional` replays), and the replayed witnesses are lifted
  to matrix certificates that the packet verifier checks independently. Trace
  norms come from sign certificates when the spectrum is rational and from the
  closed surd form on qubits; both results are now exact.
- **Lean.** The package's `TraceZeroDuality.lean` and its axiom-printing
  companion `TraceZeroDualityAxioms.lean` now live in `lean4/quantum_mechanics/`.
  They are Mathlib-free. Their report was produced on `v4.34.0`; a staging
  build on the workspace toolchain `v4.33.1` compiled them with the same
  axioms (`propext` and `Quot.sound` at most; the coboundary lemmas use none).
  That is a build, not a receipted replay, so the rows rest on the Rust tests.
  The file verifies the dual-ball identity for two-point integer spectra
  (`Eig2`), the scaling lemma, and quotient invariance of a functional that is
  assumed invariant. The paper cites `half_l1_isGreatest` over `R^n` in
  `QM.TraceZeroDuality`, built with Mathlib in 8493 jobs; that theorem is not
  in the package. The Rust certificates cover sum-zero rational vectors of any
  length and matrices with declared extreme eigenvectors. They are
  computations, not Lean proofs.
- **Ledger.** C2, C6, C9 and C10 are `FINITE COMPUTATION`, and so is C11 for
  the duality as Theorem 5 states it. C12 and C14 are `REFUTED BY COMPUTATION`
  with the `K_{2,3}` countermodel, because the witness set of Theorem 6 and the
  dual display of §2.9 are the centred ones. C15, the worked replay, is
  `EXACT FINITE ALGEBRA`. The two application summaries sourced to this paper
  now cite the exact tests above instead of the earlier floating-point check.
  The polar-witness result is exact finite algebra about the three sampled
  pairs, where it was previously only a fixture. The open question asked for an
  exact duality-gap certificate; zero-gap certificates now exist on declared
  packets.

**What stays outside.** The corrected duality is computed on declared
packets only. Nothing here solves the matrix SDP: for defects with irrational
spectra on graphs with several cycles, a value is certified only when
certificates are declared. C1 and C4 stay conditional on the operational
axioms; C5 (necessity), C7 (the wider monotone landscape) and the definitions
C3, C8 and C13 are unchanged, although C13's remark that any maximizer over
`W_tr` attains `Phi_tr` fails on the same countermodel. Reading `M_e` as a measurable observable, binary
discrimination as an experiment, and every physical reading of the graph stay
outside.

### 11.36 Trace-norm transport under quantum channels

**Original paper in the paper archive:** [Trace-norm CPTP transport audit](sources/original_papers/081_trace_norm_cptp_transport_audit/trace_norm_cptp_transport_audit.md).

The audit separated three statements under declared imports: CPTP
monotonicity does not select the trace distance; the trace norm contracts
under CPTP maps (imported as the data-processing inequality); and the
classical shadow of that contraction, `l1` contraction under stochastic
kernels. All three now compute exactly, and the first is sharper than stated.
The measure-and-prepare maps of `difference_transport_channel` show that CPTP
monotonicity leaves exactly one free scale for a norm of differences, not a
family of rival norms.

| Claim | Now computed by | Checked by (`tests/channels/trace_norm_transport_audit.rs` unless noted) |
| --- | --- | --- |
| QM-081-C1 non-selection firewall | `tower_walk_validator` (rescaling), `difference_transport_channel::{DifferenceTransport, embedding_pair}` | `native/tests/tower_walk_registry.rs`: the half trace norm contracts under three rational channels, and so does every positive multiple of it; here an exact CPTP map carries each declared trace-zero difference to each declared difference of no larger trace norm (qubits, qutrits, a non-diagonal qutrit, four levels), expansion is refused, and the embedding `C^2 -> C^4` with its CPTP left inverse keeps the trace norm |
| QM-081-C2 non-vacuity | `exact_channel::{apply_choi, choi_is_cptp}`, `su_n::GellMannBasis`, `trace_norm_certificate::SignCertificate` | qubit depolarizing noise with `p = 1/3` is CPTP and equals `2/3` times the identity on the Pauli basis of the trace-zero space, so both `j = (1/2)\|\|.\|\|_1` and `2j` strictly decrease on every nonzero difference, and they differ |
| QM-081-C3 Helstrom admission (conditional) | `SignCertificate::helstrom_effect` | for `rho = (1/3)[[1,1,0],[1,1,0],[0,0,1]]`, `sigma = I/3`: the effect `(I + S)/2` has bias `Tr(E(rho - sigma)) = 1/3 = (1/2)\|\|rho - sigma\|\|_1` (success probability `2/3`); 32 other declared effects, each checked `0 <= E <= I`, do no better |
| QM-081-C4 trace-norm contraction (imported) | `exact_channel::ExactKrausChannel::{apply, adjoint_apply}`, `trace_norm_certificate::within_operator_ball` | a Heisenberg certificate on amplitude damping, a Pauli channel and a qubit-to-qutrit isometry: with `W` the sign of `Lambda(Z)`, `Lambda*(W)` lies in the operator unit ball and `Tr(Lambda*(W) Z) = \|\|Lambda(Z)\|\|_1 = 18/25, 2/9, 2`; an irrational pair goes from `sqrt(34)/10` to `sqrt(466)/90` in half trace norm |
| QM-081-C5 `l1` contraction under stochastic kernels | `residual_density_calculus::row_stochastic_pushforward` | worked number `(1, -1) -> (0, 0)`; all 125 signed `x` in `{-2..2}^3` under three kernels, strict for two and isometric for a cyclic permutation; leaky or signed kernels are refused; the population shadow of amplitude damping carries `diag(Z)` to `diag(Lambda(Z))` |
| QM-081-C6 breadth of monotone measures | `difference_transport_channel` | see the correction below |

**Corrections and scope.**

- **The firewall is pinned down.** A functional of trace-zero differences
  that never increases under CPTP maps $M_n\to M_n$ is a nondecreasing function
  of the trace norm: for $\|Y\|_1\leq\|X\|_1$ the map
  $Z\mapsto\operatorname{Tr}(PZ)A+\operatorname{Tr}((I-P)Z)B$, with $P$ the projector onto the
  nonnegative part of `X` and `A`, `B` states built from the Jordan parts of
  $Y$, is CPTP and sends $X$ to $Y$. For norms this leaves $c\|\cdot\|_1$ only, so
  CPTP monotonicity plus absolute homogeneity selects the trace distance up to
  one normalization. The breadth that C6 and QM-091-N2 cite (relative
  entropies, fidelity quantities, monotone metrics) belongs to functionals of
  the *pair* `(rho, sigma)`, not of the difference. QM-091-N2's "infinitely
  many unitarily-invariant norms ... are CPTP-monotone" is false beyond
  rescaling: the Schatten norms with `p > 1` grow under `Tr_B` (QM_080), the
  Hilbert–Schmidt norm grows `3/2 -> 2` (squared) between two qutrit
  differences of trace norm `2`, and the operator norm grows `1/2 -> 1` between
  two four-level ones, each time through an exact CPTP map.
- **Falsifiability condition (i) is not met.** The structural imports with
  CPTP monotonicity fix the functional only up to a nondecreasing
  reparametrization of the trace norm (up to scale for norms). The
  normalization still comes from the imported discrimination axiom.
- **Non-vacuity.** The Lean seal used the halving step `x -> x/2` over `N`,
  which is not a channel. The witness is now a genuine CPTP strict contraction,
  decided on a basis of the trace-zero space.
- **Contraction.** The paper imported data processing. The Heisenberg
  certificate verifies it on each declared channel and input: `Lambda*` is
  unital and positive, so it keeps the operator unit ball, and it moves the
  optimal witness back to the input.
- **Lean.** `QM.TraceNonSelect`, `QM.StochasticL1` and
  `003_qm_stochastic_channel.lean` (ENC-0247, ENC-0246, ENC-1055) are not in
  the repository. The Rust checks replace them; C5 is a finite computation, not
  a proof of the general statement.

**What stays outside.** The four imports (QM-091-D1) and the non-claims
(QM-091-N1) stay fences. The Helstrom reading as an operational experiment
(C3) and data processing as a general theorem (C4) stay imported; the
computations above are instances. QM-091-N2 is not retyped: its breadth clause
is false for norms, as shown. The classification of monotone metrics on pairs
(Petz, Morozova–Chentsov) is not computed.

### 11.37 Channels as stochastic kernels and completely positive maps

**Original paper in the paper archive:** [Channels as stochastic kernels and the CPTP lift](sources/original_papers/082_channels_as_stochastic_kernels_and_the_cptp_lift/channels_as_stochastic_kernels_and_the_cptp_lift.md).

The paper's one theorem is elementary: stochastic kernels carry distributions
to distributions and compose, and a CPTP map read on the output diagonal of a
declared basis induces a stochastic population shadow `K(h|g)`. Its content is
in the fences around it: the shadow does not keep diagonality, does not
determine the channel, and does not force complete positivity. Each is now an
exact computation. The shadow is `population_shadow`, shared with QM_121's
channel rung; kernels act through `residual_density_calculus`, and channels
come from `exact_channel`.

| Claim | Now computed by | Checked by (`tests/channels/channels_as_stochastic_kernels.rs`) |
| --- | --- | --- |
| QM-082-C4 (i), (ii) kernels preserve distributions and compose | `population_shadow::compose_kernels`, `residual_density_calculus::row_stochastic_pushforward` | `(1/2, 1/3, 1/6)` goes to `(19/60, 5/12, 4/15)`; the composite of a `3 x 3` and a `3 x 2` kernel is stochastic and acts as the two steps; the identity kernel is a unit and composition is associative |
| QM-082-C4 (iii) a CPTP map has a stochastic population shadow | `population_shadow::population_shadow`, `exact_channel::ExactKrausChannel` | for the identity, dephasing, a rational rotation, amplitude damping and a qubit-to-qutrit isometry, the shadow is the diagonal of the Choi matrix, row stochastic, and the output populations of the basis states; a completely positive family that loses trace is refused, and its Choi diagonal is not stochastic |
| QM-082-C4 scope: coherence and non-determination | same | the rotation sends `\|0><0\|` to a state with coherence `12/25`; for the coherent input `(3/5, -4/5)` the output populations are `(1, 0)`, while the kernel applied to the input populations gives `(337/625, 288/625)`; the identity and complete dephasing share the identity kernel and differ on `\|+><+\|` |
| QM-082-C5 bit-flip worked example | `population_shadow`, `compose_kernels` | `K = [[0,1],[1,0]]`, `(3/4, 1/4) -> (1/4, 3/4)`, `K K = I`; `X rho X` conjugates the coherence of `\|+i><+i\|`, while a bit flip followed by dephasing has the same kernel and sends it to `I/2` |
| QM-082-C6 complete positivity is not forced by the kernel | `exact_channel::{apply_choi, choi_is_cptp}`, `exact_hermitian::partial_transpose_second` | the transpose map (Choi matrix: the swap) is trace preserving, sends the declared states to states and has the identity kernel, but the swap is not PSD and the partial transpose of the Bell state has the negative direction `(0, 1, -1, 0)`; every stochastic kernel has a CPTP lift with diagonal Choi matrix, which returns the kernel and dephases, and for square rational entries rational Kraus operators `sqrt(K(h\|g)) \|h><g\|`; a signed kernel has none |
| QM-082-C7 the shadow is basis-relative | `population_shadow` on conjugated Kraus operators | complete dephasing has the identity kernel in the computational basis and `[[337, 288], [288, 337]] / 625` in the basis `{R e_0, R e_1}`; conjugating back reproduces the dephasing on every declared input |
| composition of shadows | `population_shadow::composition_defect` | the rotation followed by its inverse is the identity channel, yet the product of the two shadows is `[[337, 288], [288, 337]] / 625`; when the first map leaves only populations the defect is zero |
| QM-082-C8 Kraus, Choi and Stinespring presentations | `exact_channel` | `native/tests/finite_descent_interface.rs` (QM_007-C13); `tests/channels/completely_positive_import_boundary.rs` for the non-uniqueness of Kraus families |

**Corrections and scope.**

- The kernel is stored row stochastic, `rows[g][h] = K(h|g)`, the transpose of
  the paper's column convention, as in `finite_classical_shadow` and
  `residual_density_calculus`.
- Composition. Kernels compose, as (ii) says, but the population shadow of a
  composite channel is not the composite of the shadows. The descent from
  channels to kernels respects composition when the first map leaves only
  populations, and not in general.
- The lift. Every stochastic kernel does have a completely positive lift, the
  measure-and-prepare map with a diagonal Choi matrix, so "the lift is not
  implied" means that it is not unique (identity and dephasing share a kernel)
  and that a positive map with a stochastic kernel need not be completely
  positive (the transpose). It does not mean that a kernel may lack a CPTP
  pre-image.
- The cited Lean module `QM.StochasticChannel` (ENC-1127: `stochastic_preserves_simplex`,
  `stochastic_compose`, `kraus_diagonal_stochastic`) is not in the repository,
  so the row's "MECHANIZED" status had no surviving evidence. C4 is now a
  finite computation on declared kernels and channels; the general
  statement is the paper's prose proof.

**What stays outside.** The carrier and kernel definitions (C1–C3), the
green/red firewall and authority fence (C9, C10) and the literature comparison
(C11) are unchanged. C9's clause that CPTP monotonicity does not select the
trace-norm gauge is sharpened in QM_081: it leaves one free scale. When
coherence transport is admissible (the "harder rung" of the support ledger)
is not addressed. C5, C7 and C8 keep their types; the report suggests retypes.

### 11.38 The boundary between positivity and complete positivity

**Original paper in the paper archive:** [Completely positive import boundary](sources/original_papers/083_completely_positive_import_boundary/completely_positive_import_boundary.md).

The package was an annex stub pointing to QM_082 and is absorbed into that
entry. Its four claims (`QM_083-C1` to `QM_083-C4`) appear only in the
package's own ledger, not in the consolidated repository record, so no ledger row
changes. The finite ones are computed as follows.

| Claim | Now computed by | Checked by (`tests/channels/completely_positive_import_boundary.rs` unless noted) |
| --- | --- | --- |
| QM_083-C1 stochastic kernel transport | `population_shadow::compose_kernels`, `residual_density_calculus::row_stochastic_pushforward` | see QM_082-C4 (i), (ii) in `tests/channels/channels_as_stochastic_kernels.rs` |
| QM_083-C2 `l1` contraction | `row_stochastic_pushforward` | see QM-081-C5 in `tests/channels/trace_norm_transport_audit.rs` |
| QM_083-C3 positivity and complete positivity | `exact_channel::{apply_choi, choi_is_cptp}`, `exact_hermitian::partial_transpose_second` | corrected: a nonnegative kernel `K` and `K (x) I_2` both have diagonal, nonnegative Choi lifts, which are CPTP; the transpose map is positive on states, but its extension by an identity sends the Bell state to a matrix with the negative direction `(0, 1, -1, 0)` |
| QM_083-C4 Kraus decompositions are presentations | `exact_channel::ExactKrausChannel::{choi, apply, stinespring_isometry}`, `linear_algebra::exact_field::elimination::rank` | amplitude damping, its Kraus family mixed by the orthogonal `[[3/5, 4/5], [-4/5, 3/5]]`, and the family padded with a zero operator have one Choi matrix and one action; the Kraus rank is the Choi rank `2` (one for a unitary channel); the Stinespring isometries differ by `I (x) U` on the environment |

**Corrections and scope.** C3 claimed that local positivity
`K >= 0` does not force complete positivity `K (x) I >= 0`. On the classical
carrier the stub names, it does: a nonnegative kernel tensored with an identity
is still nonnegative, and its measure-and-prepare lift is completely positive.
The gap between positivity and complete positivity opens only for maps that
move coherence, such as the transpose. The cited Lean targets
(`003_qm_stochastic_channel.lean`, `003_qm_stochastic_l1.lean`,
`003_qm_trace_non_select.lean`, `003_qm_continuum_non_promotion.lean`) do not
exist in `lean4/`; C3 cited a non-selection file for a positivity claim.

**What stays outside.** C4's reading of a Kraus decomposition as an "external
`L^2` observer projection" is interpretive; its finite content is that the
decomposition is not determined by the channel. No continuum statement is
made.

### 11.39 Operational equivalence and interpretive underdetermination

**Original paper in the paper archive:** [Interpretations and operational equivalence](sources/original_papers/090_interpretations_as_authority_shadows/interpretations_as_authority_shadows.md).

The paper reads the interpretations of quantum mechanics as narratives laid
over one finite packet calculus, and gives one sharp criterion: a reading
becomes adjudicable only when it changes a packet number. It formalizes no new
theorem of its own. Its residual signature, its distinguishability criterion,
its worked example and its two non-implications have finite content, and all
of them now compute. The six interpretation rows are prose and get no code.

| Claim | Now computed by | Checked by (`tests/interpretations/interpretations_as_authority_shadows.rs`) |
| --- | --- | --- |
| C1 residual signature (definition) | `finite_cochain_packet::certified_trichotomy` | the paper's packet has `Phi1 = 1`, `Gamma2 = 0` and class `ClosedResidual` |
| C3, C10 non-implications | `FiniteCochainPacket::classify`; `contextuality_obstruction`; `composition_tomography`; `tower_walk_validator` | the signature on an unfilled real triangle, with no Hilbert space; Kochen–Specker contextuality on Cabello's integer rays, whose carrier `R^2 (x) R^2` fails local tomography (rank `9 < 10`) while `C^2 (x) C^2` spans; an obstruction with another antecedent missing emits no lift ledger (§11.2 (QM_001)) |
| C7 packet-distinguishability (definition) | `relative_state_branching::{system_only_observables, first_separating_observable}` | a coherent state and its branch mixture agree on a spanning system-only family and are separated only by the recoherence projector, `1` against `337/625` |
| C9 authority firewall | `omega_types::authority` (its own tests); `certified_authority_fence` | `IsAuth` holds only when all seven of its guards hold, and no outcome becomes authority without a descent witness and an `IsAuth` token (`omega_types`' own tests); a certified `Phi1` fixes only the residual mass, and its certificate has no terminal, packet or authority field; `CertifiedAuthority` cannot be named in this crate (`certified_authority_fence`) |
| C13 worked example | `certified_trichotomy`, `certified_quotient_mass`, `omega_functional::phi1::Phi1Functional` | Reading A: the representative `(3, -2)` has raw mass `5` and the same certified class as `(0, 1)`; Reading B: the decayed residual `(9/10) x` has `Phi1 = 9/10`, and a certificate claiming `9/10` for the actual packet is refused |

**Corrections and scope.**

- Reading B's decay was a decimal, `Phi_Q = 0.9`. The predicted packet is
  now the residual `(9/10) x`, whose certified value is `9/10`.
- "Adjudicable by replay" is literal: the dual witness `z = (1, 1)` of the
  replayed certificate pins `Phi1 = 1`, and `omega_functional` refuses the
  same certificate reporting `9/10`.
- "Classical gluing failure does not imply complex Hilbert QM" is witnessed
  twice: in the paper's own formalism by a graph cycle, and in the
  Kochen–Specker sense by real rays. The same countermodels decide C3, which
  the source typed `OPEN`. The reconstruction question it points to is C4,
  and that stays open.
- The firewall ENC-1063 was cited as a Lean theorem. No such file is in the
  tree. Its Rust form is `omega_types`' sealed authority constructor, which
  this crate cannot name; the row now cites `omega_types`' own tests and the
  worked instance of QM_091.

**What stays outside.** The interpretation classifier (C6, C8) is narrative.
The reconstruction conjecture and its five-condition target (C2, C4, C5) stay
`OPEN`. The registry-relative lift (C11, C12) belongs to QM_001. No
interpretation is scored true or false, and nothing here grants authority.

### 11.40 Formal possibility is not physical realization

**Original paper in the paper archive:** [Deutsch, Everett, Wolfram, and the promotion error](sources/original_papers/091_deutsch_everett_wolfram_promotion_error/deutsch_everett_wolfram_promotion_error.md).

The paper states one typed non-implication, that deriving a structure does
not mint authority, and applies it as three argued readings of Deutsch,
Everett–DeWitt and Wolfram. Its finite content is small: the worked instance
of the type separation, and the firewall itself, whose Rust form is the
sealed authority constructor in `omega_types`. The three readings, the
fairness ledger and the appendix on Deutsch's resource count are prose.

| Claim | Now computed by | Checked by (`tests/interpretations/formal_possibility_promotion_error.rs`) |
| --- | --- | --- |
| C1a bare non-implication | `omega_types::authority` (its own tests); `certified_authority_fence`; the worked instance below | `IsAuth` holds only when all seven of its guards hold, and no outcome becomes authority without a descent witness and an `IsAuth` token (`omega_types`' own tests); a certified `Phi1` fixes only the residual mass, and its certificate has no terminal, packet or authority field; `CertifiedAuthority` cannot be named in this crate (`certified_authority_fence`) |
| C4 worked instance | `finite_cochain_packet::certified_quotient_mass`, `FiniteCochainPacket::quotient_mass` | `d0(alpha) = (alpha, -alpha)`, weights `(1, 1)`, `x = (0, 1)`: `Phi1 = 1` for every representative, with dual `z = (1, 1)`; the digon `g -> v -> g` gives the same value; the certificate holds only structure; the ledger's transposed data is refused |

**Corrections and scope.**

- The ledger row stated the instance as `C^0 = R^2, C^1 = R, d0 = (1, -1),
  omega = (1, 1)`: two weights for one edge. That is refused as malformed.
  With one weight it is a single edge, on which every residual is a repair
  (`Phi1 = 0`). The body's version, `C^0 = R, C^1 = R^2`, is the one
  implemented, over `Q`.
- The body computed `Phi1` "by the declared finite rule" without giving the
  value. It is `1`, proposed by `omega_solvers` and replayed by
  `omega_functional`.
- "The structure fixes the diagnostic, the packet fixes the authority" is now
  precise. Of the ten fields of `omega_types`' guard evidence, the structure
  supplies one, the residual mass; the others are declarations it does not
  contain. A test that filled the guard evidence from the structure was
  dropped at integration, because `omega_quantum_physics` must not name
  `omega_types` (`certified_authority_fence`); `omega_types`' own tests cover
  the guard logic.
- Tier 1b (authority factors only through `Pi_sharp`) is superseded in the
  source itself and stays `OPEN`.

**What stays outside.** The Deutsch, Everett–DeWitt and Wolfram readings (C5,
C6, C8, C10, C12, C13), their defeat conditions (C16), the conditional
physical no-go (C7) and the finiteness argument against the resource-count
reading of Deutsch (Appendix A) are argued prose with no finite object. The
mathematical core of the Everett reading, that a branch representation is not
fixed by the state, is computed under QM_092 (C23) and QM_094.

### 11.41 Typed boundaries for quantum claims

**Original paper in the paper archive:** [Typed authority boundary suite](sources/original_papers/092_qm_typed_authority_boundary_suite/qm_typed_authority_boundary_suite.md).

The suite lists twenty-four Lean results, each a finite fact, a decidable
classifier or a typed non-implication, and imports thirteen GOMC firewall
rows from QM_004. None of the Lean modules it names is in the tree. Most of
its kernels belong to other papers and are computed there. This entry
computes the kernels the suite owns, exhaustively on declared boxes of
cochains, and points the rest at their owners.

| Claim | Now computed by | Checked by (`tests/interpretations/typed_authority_boundary_suite.rs`) |
| --- | --- | --- |
| C1 ANP-001 | `omega_types::authority` (its own tests); `certified_authority_fence` | see QM_091 C1a |
| C2 TERM-DISJ-001 | `omega_functional::trichotomy::{classify_exact, TrichotomyOutcome}` | exactly one of three classes on each of 297 box cochains; evidence from two different residuals is `TriRefused`, not classified |
| C3 PROJ-QUOT-001 | `finite_cochain_packet::{FiniteCochainPacket::classify, certified_quotient_mass}` | `Phi1 = 0` exactly when row reduction finds `f` with `d0 f = x`, on every box cochain and every repair map tried |
| C4 REPAIR-MONO-001 | `certified_quotient_mass` on nested repair maps | on the unfilled triangle, potentials supported on `{}`, `{a}`, `{a,b}`, `{a,b,c}` strand 26, 24, 20, 20 of the 27 cochains in `{-1,0,1}^3`, and `Phi1` never increases pointwise |
| C6 TRI-001 | `FiniteCochainPacket::classify` | total, exclusive, and equal to "in `im d0`" / "closed" / "not closed" on the unfilled triangle (7, 20, 0), the filled triangle (7, 0, 20) and two triangles sharing an edge, one filled (17, 46, 180) |
| C23 EVE-001, mathematical core | `relative_state_branching` | one global state with two relative-state decompositions, both with orthonormal records (`everettian_relative_state_contact.rs`) |
| C5 schema refusal, C13 `d1 d0 = 0`, C14 `M_2` classifier | `m2_quantum_packet` | see §11.5 (QM_005) |
| C10 trace norm not selected, C18 registry-relative minimality, C19 lift trigger | `tower_walk_validator` | see §11.2 (QM_001) |
| C12 Born pairing not selected | `obstruction_management_calculus` | see §11.4 (QM_003 and QM_004) |
| C21 finite shadows do not promote to a continuum kernel | `omega_wdp::coda::q::{continuum, admission}` | see §11.7 (QM_008) |

**Corrections and scope.**

- The suite presents every row as machine-checked. The paper records a Lake
  build of 2026-06-14, but the `OmegaCore` and `QM` modules it names are not
  in this tree. The rows implemented here are Rust computations, not Lean
  replays.
- TERM-DISJ-001's pairwise disjointness is a property of any Rust enum. Its
  finite content is that the classifier agrees with an independent
  characterization on every declared cochain.
- PROJ-QUOT-001 was "tautological by design". The computation also checks
  the non-trivial direction: the quotient mass is zero only on the repair
  image.
- REPAIR-MONO-001 is realized with repair maps restricted to nested vertex
  supports. Both the stranded counts and the pointwise `Phi1` values are
  monotone.
- The packaging rows `QM-092-C01`..`C09` restate `C1`..`C9` and are left as
  they are.

**What stays outside.** C22 (Deutsch) and C24 (Wolfram) have no finite
quantum content and get no code. C23 is computed only in its mathematical
core; no ontology predicate exists. The trace-zero ball (C8), Born redundancy
(C9), stochastic `l1` contraction (C11), path sums (C15–C17) and the cofiber
separation (C20) belong to the papers that own them. Of C7, only
`im d0 ⊆ ker d1` is used here, replayed whenever a packet is built. The GOMC
rows belong to QM_004. Nothing in the suite mints authority.

### 11.42 A finite-descent audit of the imported quantum interface

**Original paper in the paper archive:** [Finite checks of imported quantum structure](sources/original_papers/093_from_q_to_gtfoc_finite_descent_of_quantum_structure/from_q_to_gtfoc_finite_descent_of_quantum_structure.md).

The paper assembles per-layer results stated elsewhere into one descent chain
and establishes no new theorem of its own. Its core claim is a correction: the tower
audits an imported interface and derives neither the interface nor its
ontology. The diagnostic layer it defines and two finite facts it relies on
compute here. The other layers point at the papers that own them.

| Claim | Now computed by | Checked by (`tests/interpretations/quantum_interface_descent_audit.rs`) |
| --- | --- | --- |
| C12 authority non-promotion | `omega_types::authority` (its own tests); `certified_authority_fence` | see QM_091 C1a |
| C14 obstruction classes (definition) | `FiniteCochainPacket::classify` | see QM_092 C6 (`typed_authority_boundary_suite.rs`) |
| C15 classical gluing fails for contextual observables | `contextuality_obstruction::{compute_obstruction_class, verify_global_section}` | the Cabello configuration has a nonzero class in `H^1` over `Z_2`; all `2^18` parity assignments fail, the best violating exactly one of nine contexts; the product control glues |
| C20 rebit local tomography | `composition_tomography::{local_tomography_spanning_real, local_tomography_spanning_complex, real_local_tomography_witness}` | the nine product effects of two rebits have rank `9 < 10`, with an explicit symmetric direction that all of them miss; the sixteen complex product effects span |
| C3, C19 registry-relative minimality (conditional) | `tower_walk_validator` | see §11.2 (QM_001) |
| C11 trace norm not selected by monotonicity | `tower_walk_validator` | see §11.2 (QM_001) |
| C16 `d1 d0 = 0` for `M_2` packets | `m2_quantum_packet` | see §11.5 (QM_005) |
| C13 exact and scoped evidence routes are disjoint and non-authoritative | `descent_evidence_routes` | see §11.6 (QM_006 and QM_007) |

**Corrections and scope.**

- C15 was stated as "`Phi_Q > 0` for contextual observables". What computes
  is the classical-gluing obstruction as a nonzero `Z_2` class, confirmed by
  exhaustive search. No `l1` magnitude `Phi_Q` is evaluated for it. The rays
  are integer vectors, so the obstruction already lives in real Hilbert
  space.
- The rebit row of the O022 table ("local tomography `9 != 10`") is now an
  exact rank with a witness direction, not a parameter count.
- The source's falsifiability row (C23) says the paper fails if a classical
  carrier passes the $L^1$ normalization step, but §5 says classical distributions
  do pass it. The body's own falsifiability paragraph is narrower and
  consistent: a non-quantum interface outside the frozen registry does not
  falsify the paper, because no general selection theorem is claimed.

**What stays outside.** The descent map and the Q frontier (C1, C2, C5–C7,
C17, C21, C22) are definitions and fences. The
 Survival Theorem (C18) assembles policy predicates and does not derive an
 origin theorem. The stochastic-kernel, path-sum, and pairing results (C8,
 C9, C10) belong to their respective mathematical sections. Tier 3
uniqueness (C4) is open.

### 11.43 Everettian relative states

**Original paper in the paper archive:** [Everettian relative-state contact](sources/original_papers/094_everettian_relative_state_contact/everettian_relative_state_contact.md).

The paper gives the relative-state formalism a finite anatomy: squared
coefficients form an `L1` shadow, record overlaps and phases carry the `L2`
coherence, and U(1) holonomy matters only where histories recombine. Every
positive statement is conditional on a declared Hilbert carrier and
factorization, and all of them now compute exactly over `Q(i)`. The ontology,
preferred-basis and probability rows stay open or refused, and the refusals
now rest on exact countermodels.

| Claim | Now computed by | Checked by (`tests/interpretations/everettian_relative_state_contact.rs`) |
| --- | --- | --- |
| QCE-C1 reduced-state formula | `relative_state_branching::RelativeStatePacket::{reduced_state, record_gram, global_state}` | equals the partial trace of the global projector (`exact_hermitian::partial_trace_second`) with overlapping records; the off-diagonal entries are `c_i conj(c_j) G_ij / N` |
| QCE-C2 orthogonal records diagonalize | `RelativeStatePacket::{reduced_state, diagonal_shadow, branch_weights}` | `rho_S = diag(9/25, 16/25)`, also for orthonormal records that are not standard basis vectors; overlapping records stay off the diagonal |
| QCE-C3 `Phi_off` bound | `RelativeStatePacket::{off_diagonal_mass, local_deviation}`, `is_contraction` | on eight declared contractions the squared modulus of `Tr A(rho_S - rho_diag)` is at most `Phi_off^2 = (72/125)^2`, with equality at `sigma_x` for real phases and at `sigma_y` for phase `i`; `2 sigma_x` and an irrational `Phi_off` are refused |
| QCE-C4 equal local shadows, distinguishable globally | `system_only_observables`, `first_separating_observable`, `expectation` | for `u = 1, -1, i, (3+4i)/5, (-7+24i)/25` the reduced state is `I/2` and no observable of a spanning system-only family separates, while the recoherence projector reads `(1 + Re u)/2 = 1, 0, 1/2, 4/5, 9/25` |
| QCE-C5, C10 coherent state and branch mixture | `RelativeStatePacket::branch_mixture` | same reduced state and weights; the recoherence projector reads `1` against `1/2`, and purity is `1` against `1/2` |
| QCE-C6 weight conservation | `RelativeStatePacket::refine` | child weights `81/625 + 144/625 = 9/25` across two cuts; non-isometric amplitudes refused; the same refinement moves the parent's share of branch labels from `1/2` to `2/3` (`everett::EverettForkingNode`), and counting matches the weights only after the weight-dependent fine-graining `N* = 25` (`branch_finegraining`) |
| QCE-C7 tree gauge triviality | `holonomy_interference::TreeGaugeFixing` (QM_063) | two connections on a two-level branch tree are gauge trivial; a recombination diamond keeps one fundamental-cycle phase |
| QCE-C8 recombination governed by relative holonomy | `holonomy_interference::{CoherentPathFamily, relative_loop}` (QM_063) | `h = (16 + 63i)/65` is the holonomy of the diamond loop and is gauge invariant while each route's transport is not; the recombined intensity is `w_a + w_b + 2 sqrt(w_a w_b) Re h` (`162/65` for unit weights), `4` at `h = 1` and `0` at `h = -1` |
| QCE-C9, C11 refused promotions | `RelativeStatePacket::with_system_family` | the state `(e_0 e_0 + e_1 e_1)/sqrt 2` has a second decomposition on the rotated basis `(3/5, 4/5), (-4/5, 3/5)` with orthonormal records, the same reduced state and weights, and a different branch mixture; both sit on a branch tree where every connection is gauge trivial; with unequal weights the reduced state is not diagonal in the rotated basis (off-diagonal `84/625`) |

**Corrections and scope.**

- Coefficients are declared up to a positive scale, so equal-weight branches
  such as `1/sqrt 2` need no surd. Records must be exact unit vectors.
- Witness 3.2's `(1 + cos phi)/2` is evaluated at unit Gaussian rationals `u`
  as `(1 + Re u)/2`. That covers the requested `phi = 0` and `phi = pi`, and
  three intermediate phases, exactly.
- `Phi_off` is a sum of moduli, which are generally irrational over `Q(i)`.
  It is returned only when every summand is rational and refused otherwise.
  The hypothesis $\|A\|_{\mathrm{op}}\leq1$ is decided exactly as
  $I-A^*A\succeq0$.
- The multiplicity warning is computed: the refinement that conserves
  squared-norm weight changes the share of branch labels.
- The tree and diamond statements are computed by QM_063's module, which is
  the "Quantum Contact 1" this paper cites, rather than by a second copy.

**What stays outside.** Many-worlds ontology (C11) and a preferred basis from
holonomy (C9) stay refused. The countermodel shows that the branch
decomposition is not a function of the state; that is the reason for the
refusal, not a proof that the Everett reading is wrong. Everettian
probability (C12) stays open: the weights are a normalized valuation
conserved under refinement, and branch counting is another normalized
valuation that is not, so normalization alone does not choose between them.
No dynamics, decoherence rate or collapse model is implemented.

### 11.45 Threshold theorems and repair capacity

**Original paper in the paper archive:** [Threshold theorems as repair-capacity certificates](sources/original_papers/101_threshold_theorems_as_repair_capacity_certificates/threshold_theorems_as_repair_capacity_certificates.md).

The paper reads a fault-tolerance threshold theorem as a conditional
repair-capacity certificate: under the theorem's own hypotheses it fills the
repair-capacity packet, and below threshold the projection-obstruction no-go
does not fire. The threshold theorems are imported, not re-proved. What
follows from their declared numbers now computes in
`threshold_repair_certificate`, on the recurrence of `repair_capacity`, and the
packet the mapping fills is checked by `realization_packet_protocol` (QM_103).

| Claim | Now computed by | Checked by (`tests/repair_and_gravity/threshold_repair_certificates.rs`) |
| --- | --- | --- |
| C10 worked example | `ThresholdScaling::pairing_bound` | `C = 1`, `p = 1/1000`, `p_th = 1/100` give `1/100, 1/1000, 1/10^4, 1/10^5` at `d = 3, 5, 7, 9`, and an even distance repeats the odd one below it; at `p = 2 p_th` the bound is `2, 4, 8, 16` at `d = 1, 3, 5, 7`; at `p = p_th` it is the constant `C` |
| C2, C4, C8 the no-go does not fire (conditional) | `read_threshold_packet`, `ThresholdScaling::least_distance_below`, `repair_capacity::windows_to_exceed` | with `lambda = p`, `mu = p_th` and a declared slack `epsilon`, `p < p_th` gives a negative gap: the recurrence forces nothing, and the least distance with `p_pair < tau` is returned (`5` for `tau = 1/100`, `2k + 1` for `tau = 10^-k`); on 84 declared cases the reading is survival exactly when `p < p_th`, no-go exactly when `p > p_th + epsilon`, with the forced window count replayed, and undecided otherwise (54, 8 and 22 cases) |
| C7 THR-001 mapping (definition) | `realization_packet_protocol::RealizationPacket::from_threshold_theorem` | fills ten declared fields; the checker then asks, in order, for the carrier, the logical distinction, the repair image, the closure map, the defect history, the mixing bound and the claim scope (`native/tests/show_the_packet_protocol.rs`) |
| C9 repair-image monotonicity | `binary_pattern_carrier::PatternCarrier::{image, binary_residual}` | on the triangle, all 6561 nested pairs of repair families: the number of stranded patterns and every binary residual never increase; without nesting, one repair strands `7` patterns and the full family `4` |

**Corrections and scope.**

- The distance rule `floor((d+1)/2) >= log(tau/C) / log(p/p_th)` gives
  `p_pair <= tau`, not the `p_pair < tau` the paper states. With `C = 1`,
  `p/p_th = 1/10` and `tau = 1/100` it admits `d = 3`, where `p_pair = tau`.
  The least distance strictly below is `5`; it is computed by exact
  iteration, with no logarithms.
- "Flip to `p > p_th` and the packet enters the conditional no-go regime"
  holds only without mixing slack. On the band `p_th < p <= p_th + epsilon`
  the recurrence forces nothing while the bound grows: `p = 11/1000`,
  `p_th = 1/100`, `epsilon = 1/500` give gap `-1/1000` and ratio `11/10`. The
  reading therefore has three outcomes, not two.
- THR-001 says a threshold theorem fills every packet field (C3). Its table
  names 11 of the 18 rows of the QM_103 schema. The carrier, the logical
  distinction, the repair image, the closure map, the quotient gauge, the
  defect history and the mixing bound are not among them, and the mixing
  bound is what decides the band above. C3 keeps its type and is reported.
  The paper's "17-field schema" has 18 rows.
- `lambda = p` and `mu = p_th` is the paper's own §2.0 reading. It is a
  declaration of the mapping, not a derived relation between rates.
- `OmegaCore.QM.repair_monotone` (ENC-1066) is not in the repository; it
  survives only inside the reading guide
  `research/lean4/qm_survival_theorem.md`. C9 rests on the exhaustive check
  and is `FINITE COMPUTATION`; the general statement is set inclusion. The
  other cited theorem, `threshold_repair_nonzero_of_unabsorbed`, is in
  `lean4/PrimitiveDifference.lean` as the integer fact
  `a - b != 0` for `a > b`; it says nothing about repair.

**What stays outside.** The threshold theorems themselves (C6) are imported
and stay `ASSERTED`. Whether any architecture meets their hypotheses at the
target scale (the antecedent of C4, and C11), the rate inequality at scale
(C9b), and the doctrine and fence rows (C1, C3, C5, C12–C14). Nothing here says
scalable quantum computation is viable or obstructed, and no reading is a
physical terminal.

### 11.46 Cochain repair capacity and error thresholds

**Original paper in the paper archive:** [Fault-tolerance repair capacity](sources/original_papers/102_fault_tolerance_repair_capacity/fault_tolerance_repair_capacity.md).

The paper reads error syndromes as coboundaries `d1 e` of a cochain complex
over GF(2), bounds repair capacity by `t = floor((d - 1)/2)` with
`d = min{|c| : c in ker d1 \ im d0}`, and says that above threshold logical
errors occur with probability approaching 1. Its four rows are not in
the consolidated repository record; the table uses the paper's own IDs. The finite
content computes in `stabilizer_code_distance` (distances, decoders and
correction radii of declared stabilizer codes) and `cochain_repair_code` (the
code of a GF(2) complex, and exact decoding probabilities).

| Claim | Now computed by | Checked by (`native/tests/cochain_repair_capacity.rs`) |
| --- | --- | --- |
| QM_102-C1 syndrome as coboundary | `CochainRepairCode::{syndrome, is_coboundary, stabilizer_code}` | on the 2x2 torus, for all 256 bit-flip errors, `d1 e` is the `Z`-check syndrome of the CSS code read off the complex, and `e` is a coboundary exactly when its `X` string lies in the stabilizer group; the least weight of a cocycle that is not a coboundary is `2`, found by brute force and by the distance search |
| QM_102-C2 repair capacity `t = floor((d - 1)/2)` | `StabilizerCode::{distance, minimum_weight_decoder, is_corrected}`, `CodeDistance::uncorrectable_pair` | distances are computed, not declared: Shor `[[9,1,3]]`, Steane `[[7,1,3]]`, the five-qubit `[[5,1,3]]`, `[[4,2,2]]`, the 2x2 torus `[[8,2,2]]`, the 3x3 torus (distance 3), repetition of length 5 (bit-flip distance 5); on each, minimum-weight decoding corrects every error of weight at most `t`, and two errors of weights `ceil(d/2)` and `floor(d/2)` with one syndrome multiply to a logical operator, so no decoder corrects every error of weight `t + 1`; Shor corrects all 27 single errors, phase flips in one block sharing a syndrome, with 22 table entries, and agrees with the library's `recover_error` |
| QM_102-C3 locally satisfied checks with a global obstruction | `CochainRepairCode::{repair_distance, syndrome, is_coboundary}` | on the 3x3 torus a weight-3 cocycle passes every face check and is not a coboundary; a star coboundary passes every check and is harmless; one flip trips two faces |
| QM_102-C3 "probability approaching 1" | `CochainRepairCode::logical_success_probability` | maximum-likelihood success is at least `1/\|H^1\|` at every flip probability, and equals `1/4` at `p = 1/2` on the 2x2 torus for every rule; on repetition codes of length 3, 5, 7 at `p = 3/5`, minimum-weight failure rises (`81/125`, `2133/3125`, `11097/15625`) while maximum-likelihood failure falls (`44/125`, `992/3125`, `4528/15625`) |

**Corrections and scope.**

- Theorem 1 is right and tight, but its proof compared `e` with `e + c`. The
  argument that works is about the decoder: two errors of weight at most `t`
  with one syndrome differ by a cocycle of weight at most `2t < d`, hence by a
  coboundary. Tightness is the split of a minimal logical operator.
- A cochain code covers one Pauli type. The three-qubit bit-flip code has
  bit-flip distance 3 and code distance 1, since a single `Z` is logical. The
  claim that fault-tolerant syndromes "are" coboundary defects holds for CSS
  codes read off a complex, one error type at a time; the five-qubit code is
  not CSS, and its distance comes from the stabilizer module.
- The second half of C3 is false as stated. For maximum-likelihood decoding
  the failure probability is at most `1 - 1/|H^1|` on every code and at every
  noise level: for each syndrome it keeps the largest of `|H^1|` class
  probabilities, which is at least their mean. Failure approaching 1 is a
  property of a fixed decoder, here minimum weight, not of the code. The
  asymptotic statement itself is not computed.
- `d` is undefined when `H^1 = 0`; such a code is refused
  (`NoLogicalQubit`).
- `shor::ShorNineQubitCode` declared `distance: 3` and
  `foundational_targets` declared `code_distance: 2` for `[[4,2,2]]`; both now
  compute `n`, `k` and `d` from the generators (§5, stabilizer code distance),
  and the computed distances agree with the former declarations.

**What stays outside.** No threshold value is computed, and nothing is said
about code families as they grow beyond the declared instances. C4, the
quarantine of continuum qudit baths, is a scope fence. The Lean targets the
ledger names (`003_qm_m2_packet_classifier.lean`,
`003_qm_continuum_non_promotion.lean`) are not in the repository, and the
shared-kernel theorem of its mechanization line is the integer fact QM_101
records.

### 11.47 An evidence-presentation protocol

**Original paper in the paper archive:** [Show-the-packet protocol](sources/original_papers/103_show_the_packet_protocol/show_the_packet_protocol.md).

The paper is a protocol, not a theorem: a claim of scalable physical quantum
computation must expose a finite packet of declared fields before the checker
reports a result, and each missing or invalid field has a stated rejection
reason. Its support record asks for the decision procedure itself.
`realization_packet_protocol::terminalize` is that procedure: it refuses in
the protocol's order, replays the finite algebra the packet declares, and
computes the terminal instead of accepting one.

| Claim | Now computed by | Checked by (`native/tests/show_the_packet_protocol.rs`) |
| --- | --- | --- |
| C1, C4 minimum acceptable evidence (definitions) | `terminalize` | a complete packet on a square with one filled triangle: `rank d0 = 3`, `dim Q^1 = 2`; the defect history is `ClosedResidual` with certified `Phi1 = 1`, visible to the hole's circulation and not to the filled face's; gap `-11/1000`; the lower bound does not establish failure within 1000 windows; a coboundary history is `ExactRepair`, an edge of the filled face `ActiveClosureFailure`, and doubling the hole class doubles `Phi1` and the pairing |
| C4 replay (definition) | `terminalize` | refused: an image vector outside `im d0`, an image one dimension short, a wrong `dim Q^1`, a `d1` with `d1 d0 != 0`, a history of the wrong length, a negative repair capacity or mixing bound, a witness that does not vanish on `im d0`, a pairing bound above 1, a nonpositive visibility threshold |
| C3, C5 fields and refusal vocabulary (definitions) | `RealizationPacket`, `PacketRefusal` | each of the 17 required fields (every field but the optional `claimed_terminal`; the terminal is computed) removed alone gives its own refusal, and the same refusal when every later field is removed as well; a blank carrier is refused like a missing one |
| C7 threshold theorem into the packet (definition) | `RealizationPacket::from_threshold_theorem` | fills the defect and repair spaces, `d0`, `dim Q^1`, `lambda = p`, `mu = p_th`, the witnesses, the scaling bound, the overhead and the theorem as evidence; the refusals then name, one by one, the fields it does not fill; completed, the packet gets `ConditionalSurvival` from distance 5 |
| C11 worked surface-code example | `terminalize`, `threshold_repair_certificate::ThresholdScaling` | with the placeholder numbers `p = 1/1000`, `p_th = 1/100`, the finite recurrence reports only `FailureNotEstablished`; offered for human-significant scale the same packet is rejected as overreach unless a stated threshold theorem supplies the stronger survival premise |
| recurrence replay | `terminalize` | with gap `1/125` the lower bound from `Phi1 = 1` passes visibility 2 after exactly 126 windows: `ResidualForced` for a claim of 126 or 1000 windows, `FailureNotEstablished` for 125; a residual already above the threshold is forced at window 0; a claimed result that differs from the computed one is rejected |

**Corrections and scope.**

- The vocabulary had no refusal for two fields the packet requires, the
  closure map `d1` and the mixing bound `epsilon`. `NoClosureMap` and
  `NoMixingBound` are added. `quotient_gauge_Phi` and `terminal_status` are
  computed by the checker, not declared.
- The paper names outputs and works one example; it states no decision rule.
  The recurrence is a lower bound. It can establish failure when the bound
  crosses the visibility threshold, but failure of the bound to cross establishes
  no survival statement. For example, with initial residual $1$, gap $0$, and
  threshold $2$, both $r_n=1$ and $r_n=1+n$ satisfy
  $r_{n+1}\ge r_n+0$; one remains below the threshold and the other crosses it.
  The checker therefore reports `FailureNotEstablished`, not success, whenever
  this lower bound is inconclusive. A positive finite-window conclusion would
  require an upper bound, an exact trajectory check, or another sufficient
  argument. A claim at human-significant scale can only get the conditional result of
  an imported threshold scaling with `p < p_th`, with a theorem among the
  declared evidence and a nonpositive gap. A missing claim scope is
  `NoHumanSignificantScale`; a finite packet offered for an asymptotic claim is
  `ClaimOverreach`, the escalation described in §9 of the source paper.
- Evidence is declared as a set of sources (theorem, experiment, simulation),
  so a combination says which sources it combines.
- `Phi1` of the defect history is certified by
  `finite_cochain_packet::certified_trichotomy` with unit weights; no declared
  value of it is trusted.
- This paper's claim IDs repeat QM_101's (`QM-101-C1` to `QM-101-C14`); only
  the `103:` prefix in the ledger separates them.
- The ENC entries the ledger cites as mechanized (ENC-1063, 1065, 1066, 1067,
  1071) have no Lean source in the repository.

**What stays outside.** The fences and doctrine (C2, C8, C9, C13, C14), the
open questions at human-significant scale (C10), the notation row (C12) and the
positioning of threshold theorems (C6). The finite checks do show one half of
C13: the fields that are replayed cannot be satisfied by an arbitrary value. A
complete packet yields a terminal status, never authority.

### 11.48 Loop quantum gravity kinematical models

**Original paper in the paper archive:** [Loop quantum gravity kinematical models](sources/original_papers/110_loop_quantum_gravity_kinematical_shadows/loop_quantum_gravity_kinematical_shadows.md).

The paper collects finite shadows of five kinematical motifs of loop quantum
gravity, each on a toy carrier, and cites seven Lean files for them. None of
those files is in the repository; their text survives as reading guides in
`research/lean4/`. The shadows now compute: connections and loop holonomy
through `omega_holonomy`, the quaternion group and the flux operators in
`quaternion_gauge_shadow`, the spin-`j` Casimir and the area labels in
`spin_area_spectrum`.

| Claim | Now computed by | Checked by (`tests/repair_and_gravity/loop_quantum_gravity_kinematical_shadows.rs`) |
| --- | --- | --- |
| C2 pure gauge has trivial loop holonomy | `omega_holonomy::{DiscreteConnection::from_pure_gauge, compute_loop_holonomy, compute_path_holonomy}`, `quaternion_group` | all 512 `Q8`-valued vertex gauges on a triangle, on four closed walks, with open paths telescoping to `g(end) g(start)^-1`; all 30 closed walks of length 2 to 4 on `K4`, for eight gauges |
| C3 interference cross term | `holonomy_interference::CoherentPathFamily`, `cyclotomic::Cyc24` | on a two-path square with weights 1 and 4 the cross term is `4 Re(u)` for the four Gaussian units and two rational points of the circle; `\|1 + 2z\|^2 - 5 = 2 (z + conj z)` for every 24th root of unity, rational at exactly eight of them |
| C4 the quaternion plaquette | `omega_holonomy::{group_commutator, wilson_loop_trace, is_flat}`, `is_special_unitary` | the plaquette `i, j, i^-1, j^-1` has Wilson loop `-1`, trace `-2`, and is not flat, while a pure-gauge `Q8` connection on the same square is; of the 64 ordered pairs of `Q8` the 24 non-commuting ones have commutator `-1`, the rest `1`; the commutator-built plaquette `a,b,a^-1,b^-1` is flat for abelian phases, although a general U(1) plaquette can be curved; `Q8` lies in `SU(2)` |
| C5 `hol d0 = 0`, `ker hol = im d0` | `cohomology_admission::{admit, verify_admission}`, `holonomy_interference::walk_integral` | on cycles of length 3 to 7 holonomy vanishes on a basis of coboundaries and `rank d0 = n - 1`; on `{-1, 0, 1}^n`, `n <= 5`, a cochain is admitted exact exactly when its holonomy vanishes (7, 19 and 51 cochains), and every other one gets the circulation as separator |
| C6 `dim H^1`, `\|H^1\|`, loop resource | `FiniteCochainPacket::dimensions`, `omega_homology::smith_normal_form::invariant_factors`, `CoherentPathFamily` | `dim H^1 = 1` on cycles; on all 1088 simple graphs with 4 or 5 labelled vertices `dim H^1 = E - V + C`, and every nonzero invariant factor of `d0` over `Z` is 1, so `\|H^1(G; F_p)\| = p^(E - V + C)` for every prime `p`; three loops give eight distinct interference profiles over identical weights, and four when one path has weight 0 |
| C7 flux/holonomy commutator | `FiniteGroupAlgebra::{flux_holonomy_commutator, translated_difference}` | the matrix commutator equals `f -> (phi(x g) - phi(x)) f(x g)` for every `g` in `Q8` and every `phi` (by linearity from the eight indicators, and for one generic `phi`); at `g = i`, `phi = delta_1` its entry at `x = -i` is 1; it vanishes exactly when `phi` is constant on the cosets `x<g>`, 296 of 2048 pairs |
| C8 discrete area labels | `area_label`, `area_label_squared`, `SpinRepresentation`, `casimir`, `commutant_dimension` | `0, sqrt(3)/2, sqrt(2), sqrt(15)/2, sqrt(6)` as exact surds; squares strictly increasing for `n = 0..200`, the least positive `3/4`, attained once; on the `(n + 1)`-dimensional representation the `sl(2)` brackets hold and the Casimir is `j (j + 1)` for `n <= 12`, irreducible for `n <= 6`; a triple with `J_-` doubled fails the bracket and has a non-scalar Casimir |

**Corrections and scope.**

- All seven Lean modules are cited as mechanized, and none is present. The
  shared-kernel theorem the paper's mechanization line adds,
  `holonomy_curvature_nonzero_of_nonabelian`, is in
  `lean4/PrimitiveDifference.lean` as the integer fact
  `a - b != 0` for `a != b`; no holonomy appears in it. The rows now rest on
  exact Rust checks: `FINITE COMPUTATION` where a general statement is
  checked on declared instances, `EXACT FINITE ALGEBRA` where a finite
  statement is decided completely.
- The Casimir value `j (j + 1)`, imported in the source, is computed on the
  spin-`j` representation of `sl(2)` in a rational basis. That the flux acts
  as `J` at a puncture, the area operator and the scale `8 pi gamma l_P^2`
  stay imported.
- `quaternion_group` builds `Q8` through
  `rational_spin_lift::unit_quaternion_matrix`
  (`a + b i + c j + d k -> a I - i (b X + c Y + d Z)`), the crate's one
  quaternion convention, which QM_051's spin lifts also use.
- Flux and holonomy already fail to commute on the abelian group `{1, -1}`.
  The non-commutation is the discrete canonical commutation, not a mark of
  `SU(2)`; the non-abelian content is the plaquette commutator of C4.
- The general-graph count `b1 = E - V + C`, open in the source (C11), is a
  standard theorem. It is checked exhaustively on the declared graph
  families, over `Q` and, through the Smith normal form, over every prime.
- The continuum limit `cross_Zn_to_U1_refinement` is not a finite
  computation; C3 covers the finite samples only.

**What stays outside.** Continuum `SU(2)` with its measure, spin-network
states, intertwiners and the area operator (C1b, C10); the Hamiltonian
constraint (C11); the readings (C9) and the non-claims (C12). `Q8` is a finite
subgroup of `SU(2)`, not `SU(2)`.

### 11.49 General relativity kinematical models

**Original paper in the paper archive:** [General relativity kinematical models](sources/original_papers/111_general_relativity_kinematical_shadows/general_relativity_kinematical_shadows.md).

The GR sibling of QM_110: curvature as non-abelian holonomy, a Bianchi-shaped
identity, metric compatibility, parallel transport, the singularity as a
refusal and the continuum as a certified limit, each on a toy carrier with a
Lean file that is not in the repository. The first five compute, with
`omega_holonomy`, `finite_cochain_packet` and `transport_isometry_orbits`
(isometries of declared pairings, and transport orbits of a partial step).

| Claim | Now computed by | Checked by (`tests/repair_and_gravity/general_relativity_kinematical_shadows.rs`) |
| --- | --- | --- |
| C2 curvature | as QM_110 C2 and C4 | `loop_quantum_gravity_kinematical_shadows.rs` |
| C3 Bianchi shadow | `FiniteCochainPacket::{d0, d1, face_coboundary}`, `cohomology_admission::admit`, `omega_holonomy::verify_discrete_bianchi_identity` | on the filled triangle `d1 d0 = 0` as a matrix identity; the coboundary of each of the 125 potentials with values in `{-2, ..., 2}` is closed and admitted exact; `H^1 = 0`, and an edge of the face is not closed; on a tetrahedron with a `Q8` connection whose four faces are all curved, the face holonomies based at one vertex multiply to 1, and without the base-point transport the product is `-1`; for a U(1) connection both products are 1 |
| C4 metric compatibility | `is_isometry` | the 48 signed permutations of `Q^3` preserve the standard pairing and are closed under products; all 512 products of three `Q8` elements preserve the Hermitian pairing, and one non-unitary step breaks it; the rational boost with `gamma = 5/4` preserves `diag(1, -1)` and not `I`, a rational rotation the reverse, a unimodular stretch neither |
| C5 parallel transport | `omega_holonomy::{compute_path_holonomy, compute_loop_holonomy}` | for a pure-gauge `Q8` connection on `K4`, all five simple paths from `a` to `d` carry `g(d) g(a)^-1`; transport along a concatenated path is the product, later steps on the left, flat or curved; on the curved plaquette the two paths from `a` to `c` differ by the loop holonomy `-1` |
| C5a singularity as refusal | `transport_orbit`, `orbit_value` | for all 64 partial steps on three vertices and every start, the orbit either refuses at a step index at most 3 and is `None` from then on, or is periodic and never refuses; the index and period agree with direct iteration |

**Corrections and scope.**

- The finite Bianchi shadow `d1 d0 = 0` is abelian and holds on every
  complex. Its non-abelian form needs base points: the discrete identity holds
  for face loops transported to one vertex and fails, with value `-1`, for face
  loops based at their own first vertices. `omega_holonomy`'s
  `verify_discrete_bianchi_identity` checks the based form; its documentation
  states the identity without that condition.
- "Which pairing is the metric is imported" is exhibited: the same transport
  is an isometry of one declared pairing and not of another.
- The singularity row became an orbit dichotomy. On a finite carrier,
  incompleteness is decided within as many steps as there are vertices.
- The six Lean modules the paper cites are not in the repository; the
  reading guides keep them. Its shared-kernel citation,
  `holonomy_curvature_nonzero_of_nonabelian`, is integer subtraction (see
  QM_110).

**What stays outside.** The continuum limit (C5b) is a `Tendsto` statement and
stays `ASSERTED`; a continuum object without a convergence certificate is held
by the membrane of `omega_wdp::coda::q`. The manifold, the metric, the Levi-Civita connection,
the Riemann and Einstein tensors and the gauge group (C1b, C7), the Einstein
equation (C8), the readings (C6) and the non-claims (C9).

### 11.50 Mermin–Peres contextuality as a parity obstruction

**Original paper in the paper archive:** [Mermin–Peres contextuality and cochain obstruction](sources/original_papers/120_mermin_peres_contextuality_cochain_obstruction/mermin_peres_contextuality_cochain_obstruction.md).

The paper packaged the Mermin–Peres square as a finite parity packet: nine
variables, six row and column contexts, sign `-1` on the third column and `+1`
elsewhere, and the statement that this sign vector lies outside the image of
the incidence coboundary over `F_2`. Its Lean modules survive only as
uncompiled Markdown transcriptions under `research/lean4/`, and its
certificate generator is not in the package. `parity_context_packet` now
decides the packet exactly, with certificates, a complete census of the `512`
assignments and a second decision through the Cech complex of
`contextuality_obstruction`. `pauli_context_table` computes the sign table from
Mermin's two-qubit Pauli operators, which the paper had left as a future
target.

| Claim | Now computed by | Checked by (`tests/boundary/mermin_peres_parity_obstruction.rs`) |
| --- | --- | --- |
| QM-120-C1 the packet (definition) and its operator provenance | `pauli_context_table::PauliContextTable::{sign_table, packet}`, `parity_context_packet::ParityContextPacket::from_square` | Mermin's nine words are Hermitian involutions; the rows multiply to `+I` and the columns to `+I, +I, -I`; the induced packet equals the one read from `separating_predictions::MerminPeresSquare::standard`; two observables commute exactly when they share a row or a column (18 of 36 pairs), in agreement with `pauli`'s symplectic form; bad words, a non-commuting context and an unsigned product are refused |
| C2 every variable in two contexts | `incidence_counts` | nine incidences of two; a variable in three contexts has no context graph |
| C3 the left global product is `+1` | `d0`, `transpose_d0` | `ell(d0 a) = 0` for all 512 assignments, and `d0^T` of the all-ones cochain is zero; removing one incidence breaks both |
| C4 the declared signs multiply to `-1` | `targets` | `ell(s) = 1` |
| C5 no global assignment | `satisfiable`, `violation_histogram`, `in_image`; `contextuality_obstruction::compute_obstruction_class` | no assignment meets all six contexts; every assignment violates 1, 3 or 5 of them (`96, 320, 96`); the existing search in `separating_predictions` agrees; the Cech complex of the nerve (`dim C^0 = 12`, `dim C^1 = 9`, no triple overlaps, `rank = 8`, `H^1 = F_2`) gives a nonzero class, and it agrees with the packet on all 64 sign tables |
| C6 each context satisfiable | `satisfiable` | all six single contexts |
| C7 every five contexts satisfiable | `satisfiable`, `is_minimally_unsatisfiable` | all six five-context families; each context is the only violated one for exactly 16 assignments |
| C8 local satisfiability with global inconsistency | `satisfiable` | both hold together for exactly the 32 sign tables of odd parity |
| C11 the `F_2` cochain statement | `rank_d0`, `certificate`, `verify_certificate`, `context_graph`, `h1_dimension`, `admit_with_d1` | `rank d0 = 5`, so `F_2^6 / im d0 = F_2` and the all-ones functional is the only nonzero separator; the rank test and the certificates agree on all 64 cochains, and the image is the 32 even ones; `ker d0` is the 16 even subgraphs of the context graph `K_{3,3}`; tampered certificates are refused |

**Corrections and scope.**

- The claims rested on `QM.MerminPeresF2Cochain`, `QM.ParityContextObstruction`,
  `QM.MerminPeresCochainObstruction` and a certificate JSON with a SHA-256
  manifest. The three modules exist only as Markdown transcriptions in
  `research/lean4/`, which no build elaborates, and the certificate JSON is in
  neither the package nor the repository. The claims now
  rest on exact Rust: C2 to C8 and C11 are `EXACT FINITE ALGEBRA`, decided on
  all 512 assignments and all 64 sign tables.
- The operator provenance of the sign table (tensor products, commutation,
  context products) was a declared input. It is computed.
- Earlier versions of the paper said "C2/parity closure obstruction" without
  declaring a `d1`; the version in the paper archive declares `d1 = ell` into
  one 2-cell. What is established is `s ∉ im d0`, a nonzero class of the quotient
  `F_2^6 / im d0`. Whether `s` is a class of `H^1` depends on the declared
  `d1`: with no 2-cells, `H^1 = F_2` and `[s]` is its nonzero class; with
  `d1 = ell` (the parity functional, `ell d0 = 0`) the complex is exact at
  `C^1` and `s` is a closure failure with defect `1`. The Cech complex of the
  nerve is a third reading; it has no triple overlaps, so there `d1 = 0` and
  the obstruction is an `H^1` class. A `d1` that does not annihilate `im d0`
  is refused.
- For this packet `F_2` and `Q` agree: the context graph is bipartite, and
  over `Q` the target is separated by `(1, 1, 1, -1, -1, -1)`. They differ in
  general: on a triangle of contexts the target `(1, 0, 0)` is outside
  `im d0` over `F_2` and equals `d0 (1/2, 1/2, -1/2)` over `Q`.
- `separating_predictions::MerminPeresSquare::verify_no_noncontextual_assignment`
  returned its declared flag instead of searching or refusing above twelve
  observables, read a product of `2` as unsatisfiable, and silently dropped
  contexts that had no declared product. A thirteen-observable square that
  the all-plus assignment satisfies was reported as having no noncontextual
  assignment. The packet decides that square and refuses the other two
  inputs. The defect was pinned by a test and fixed on 2026-09-29 (see
  "Defects fixed in pre-existing code" below); the function now returns a
  `Result` from an exhaustive search and refuses malformed squares.
  `MerminPeresCochainBridge` called the obstruction a degree-2 (`H^2`) class
  without computing one; it now computes the degree-two class with
  `ParityContextPacket`.

**What stays outside.** C9 and C10 are fences: the packet derives no quantum
mechanics, Hilbert space or measurement ontology, and the FSP/Meron link is
methodological. The words' reading as physical measurements, and
contextuality of other scenarios (QM_122's Peres and Cabello rays), are not
part of this packet. The Lean modules the paper names are not reconstructed.

### 11.51 Ingredients of a finite quantum model

**Original paper in the paper archive:** [The finite quantum-mechanics ingredient ladder](sources/original_papers/121_the_finite_qm_ingredient_ladder/the_finite_qm_ingredient_ladder.md).

The ladder assembled six rungs from earlier papers: probability as `l1`
normalization, the diagonal density, channels as stochastic kernels with a
population shadow of CPTP maps, path sums as matrix powers, the phase fiber of
superposition, and interference as the cross term no weight functional
computes. Its four `LEAN SOURCE (UNREPLAYED)` rows pointed at Lean that no
build covers. Each rung now has exact Rust. Five rungs were already computed
by library modules; the missing one, the population shadow of a Kraus channel,
is `population_shadow`. The worked example runs through all rungs.

| Claim | Now computed by | Checked by (`native/tests/ingredient_ladder.rs`) |
| --- | --- | --- |
| QM-121-C1 probability is `l1` normalization; the Born square re-encodes it | `residual_density_calculus::ResidualLedger::weights`, `phase_blind_quotient::{phase_blind_projection, gaussian_lift}`, `mass_phase_embedding` | `w = (3, 1)` gives `(3/4, 1/4)`; five exact lifts with moduli `(3, 4)`, among them `(9/5 + 12/5 i, -16/5 + 12/5 i)`, all return `(9/25, 16/25)`; see also `dynamics/finite_path_sum_graded_transport.rs` |
| C2 the diagonal density, its purity, coherence not forced | `ResidualLedger::{diagonal_density, purity}`, `sector_measurement`, `ledger_from_diagonal_density` | `diag(3/4, 1/4)` is PSD with trace one and purity `5/8`, equal to `Tr(rho^2)`; `(4, 0)` gives a projector of purity one; `\|+><+\|` has the same diagonal as `diag(1/2, 1/2)`, is pure, and is refused as a diagonal density; see also `native/tests/residual_density_boundary.rs` |
| C3 kernels compose; the population shadow of a CPTP map | `population_shadow::{population_shadow, compose_kernels, compose_channels, composition_defect}` | for identity, bit flip, complete dephasing, a rational rotation, amplitude damping and a qubit-to-qutrit isometry the shadow is row stochastic and reproduces the channel's output populations on four declared laws; the bit-flip shadow moves `(3/4, 1/4)` to `(1/4, 3/4)`; identity and dephasing share a shadow and differ on `\|+><+\|`; the rotation sends `diag(1, 0)` to a coherent state; malformed and mismatched kernels are refused |
| C4 path sum `= M^n`, Chapman–Kolmogorov | `graded_path_sum`; `compose_kernels` | the bit-flip kernel squares to the identity and cubes to itself; the path-sum and Chapman–Kolmogorov identities are the QM_031 tests in `dynamics/finite_path_sum_graded_transport.rs` |
| C5 phase content is the quotient fiber | `phase_blind_quotient::{FiberPoint, discrete_fiber}` | `(1, 1)` and `(1, -1)` project to one point; relative-phase dimension `\|E_w\| - 1 = 1`, unchanged by a zero-weight coordinate; the fiber over the quarter turns has `4 = 4^(2-1)` classes |
| C6 interference is the non-`l1` cross term | `coherent_interference::{interfered_weight, cross_term}`, `phase_blind_quotient::{classify_descent, separates}` | the two-row mix sends the pair to `(2, 0)` and `(0, 2)`: interfered weights `4` and `0`, cross terms `2` and `-2`; the mix is refused descent with a separated phase-equivalent pair; see also `superposition/interference_as_the_non_l1_resource.rs` |
| C7 useful QC as the buildability set `S` | `buildability_criterion` | the QM_061 tests in `superposition/interference_as_the_non_l1_resource.rs` |
| C9 support: normalization does not force the square | plain arithmetic, `phase_blind_projection` | the power readouts `p = 1..4` of `(3, 4)` are normalized and pairwise different; only `p = 2` equals the projection |

**Corrections and scope.**

- The worked example's lift `(sqrt 3, 1)` is irrational. Over `Q(i)` the
  point `(3/4, 1/4)` has no preimage at all (`3/16` is not a sum of two
  rational squares), so the redundancy of the Born square is shown on
  `(9/25, 16/25)`, where exact lifts exist.
- The shadow is stored row stochastic, rows indexed by inputs, so that it is
  applied by the existing `row_stochastic_pushforward`; the ladder's
  column-stochastic `K(j | i)` is its transpose.
- "Channels compose" holds for kernels, not for shadows. The shadow of a
  rotation followed by itself is `(49, 576; 576, 49)/625`, while the product of
  the two shadows is `(337, 288; 288, 337)/625`. The defect vanishes when the
  first channel keeps diagonal inputs diagonal or the second reads only
  populations (dephasing, bit flip, amplitude damping), and not otherwise: the
  coherence the first step creates is interference for the second.
- Rung 5's fiber is enumerated only for declared finite unit groups. QM_122
  shows that the mixing leftover already runs on `{+1, -1}`, so the circle
  `U(1)` of the source's `U(1)^(|E_w|-1)` is not constructed here.
- The four Lean rows (`PaperQF002.L010_01_BornRedundancy`,
  `QM.DiagonalDensity`, `QM.StochasticChannel`, `QM.FinitePathSum`) are not in
  the repository. The rows now rest on the Rust above, not on a Lean replay.
- C7's "proven predicate equivalence" is a definition apart from the race
  condition, as QM_061 recorded.

**What stays outside.** C0, C11 and C12 are fences, and C8 (the stand) is a
position. C9 and C10 are imports: the countermodel above shows that
normalization does not select the square, and the `C/U(1)` carrier is not
derived (QM_062). The audit rows PL-QM043-1, OB-U1 and OB-BORN remain open
obligations. Continuous time and the continuum path integral are not
modelled.

### 11.52 The finite Hilbert boundary from primitive difference

**Original paper in the paper archive:** [Finite Hilbert boundary from primitive difference](sources/original_papers/122_finite_hilbert_boundary_from_primitive_difference/finite_hilbert_boundary_from_primitive_difference.md).

The paper walked from a report-fiber primitive difference toward Hilbert
language one named extra at a time, with a receipted Lean walk for its core
(`H000`–`H018`, the `HW*` threads). Those rows keep their Lean status. A later
§7.6–§7.7 added higher-dimensional ray configurations, cyclotomic hosts and
declared simplicial and spin-foam models, supported by Python fixtures. The
finite content now computes in Rust: the report-walk fixtures in
`report_fiber`, the configurations in `finite_geometry`, the models in
`simplicial_gravity` and `finite_spinfoam`, and three new modules:
`gaussian_frame_readout` (frame additivity), `finite_report_dynamics`
(dilations, half steps, interpolants) and `frame_function_polytope` (frame
functions, their polytope and the states they come from). Several §7 claims
turned out false or overstated; each has an exact countermodel below.

| Claim | Now computed by | Checked by (`native/tests/finite_hilbert_boundary_hosts.rs`) |
| --- | --- | --- |
| C1–C8, C10, C11, C17, C18, C21, C24–C37 (Lean, receipted) | unchanged; fixtures replayed by `report_fiber` and `finite_report_dynamics` | collapse is not reversible; four reversible dilations of the report identity and four of collapse with the ancilla prepared at false (C33, C36); the mixing leftover of C10 in the C9 test |
| C9 phase-blind squares | `report_fiber::{phase_blind, mix}`, `phase_blind_quotient::discrete_fiber` | `(1, 1)` and `(1, -1)` have weights `(1, 1)`; the fiber over `(1, 1)` in `Z[i]^2` has 16 vectors in 4 global-phase orbits, and `(1, -1)` is not in the orbit of `(1, 1)`; mixing gives `(4, 0)` and `(0, 4)`; non-integral amplitudes are refused |
| C12 the fourth power against scale-2 frames | `gaussian_frame_readout::{orthogonal_frames, frame_operator, square_is_frame_additive, frame_total, frame_additivity_violation, report_basis_law}` | all 96 orthogonal scale-2 frames of `Z[i]^2` have frame operator `2I`, so the square gives every state the same total on every frame (also at scales 1, 4, 5); the fourth power gives 82 and 50 at `(2, 1)`, the sixth 730 and 250, and violations are found for powers 2–4; at scale 1 no power is excluded; `(4, 1)` and `(16, 1)` are not proportional; every power normalizes |
| C13, C22 products on `Bool x Bool` | `report_fiber::{tensor2, dump_right, entanglement_determinant}` | both maps equal their basis expansion on a box; Kronecker normalization pins the pointwise product; `dump_right` tags `(a, b)` with `(a, false)`, is not injective, and disagrees (0 against 1) at `(false, true)`; every product has determinant 0, while `(1, 0, 0, 1)` has determinant 1 and coefficient rank 2 |
| C14 collapse, dilations, half steps, interpolants | `finite_report_dynamics::{reversible_dilations, half_steps, swap_interpolants}` | collapse's basis images have Gram matrix `(1, 1; 1, 1)`; no dilation of collapse exists without a prepared ancilla; the toggle has no half step among maps of the labels (`sigma(sigma(q)) = f(q)`; a single transposition has none; a double transposition has two); `M^2 = 4 X` has exactly four solutions in `M_2(Z[i])`, among them the Lean `sqrtSwap` and its negative; over scales 1–16 only 4 and 16 have solutions |
| C23 two effect rules, one unit total | `report_fiber::phase_blind`, `pairing_audit::audit_row` | unit totals agree and nonnegative effects stay nonnegative for all 625 amplitude pairs with coordinates in `[-2, 2]`; 4 against 1 on the false indicator at `(2, 1)`; as audit rows both pass the single-system checks and give `4/5` against `1/5` |
| C39 carrier stages | `report_fiber::carrier_stage` | `(H_0, H_1, Aut)` for stages 0–5 is `(0,0,1), (1,0,1), (2,0,2), (1,0,1), (1,1,2), (1,1,2)`; `∂r = b - a`; the self-loop has boundary 0; the filled triangle kills the loop |
| C40 the tripartite derivation | as C9 and C13, plus the scaling law | `‖Hv‖_p^p / ‖v‖_p^p = 2` on `e_0, e_1, (1, 1), (1, -1), (2, 1)` exactly for `p = 2` among `p = 1..6` |
| C41 cyclotomic hosts | `cyclotomic_integer::CyclotomicInteger`, `cyclotomic::Cyc8`, `report_fiber::carrier_stage` | reduced powers keep at most `phi(n)` coefficients for `n = 3, 4, 5, 8, 12`; `zeta_8 - zeta_8^3` squares to 2; `F* F = 3 I` for the qutrit Fourier matrix over `Z[zeta_3]`; bad coefficients and conductors are refused |
| C42 Peres 33 rays | `finite_geometry::peres` | 33 rays, 72 orthogonal pairs, 16 triads, rank 16, nullity 17, no coloring; every ray lies in a triad; `17 > 5 = dim` of trace-one symmetric `3 x 3` matrices |
| C43 Cabello 18 rays (refuted) | `finite_geometry::cabello`, `frame_function_polytope::FrameSystem` | 18 rays, 63 pairs, 9 tetrads, no coloring, and the tetrads are exactly the orthogonal 4-cliques; the ray projectors span all 10 symmetric directions and `rank A = 9`, so the frame functions are exactly the trace-one symmetric matrices; the polytope has 146 vertices, all half-integral with a `1/2` entry, none PSD, every one with least eigenvalue `>= -1/2`; the bare 24-cell has three disjoint tetrads holding all 18 orthogonal pairs |
| C44 E8 (not retyped) | `finite_geometry::e8`, `FrameSystem::projector_span_rank` | the 120 ray projectors span all 36 symmetric directions; with the octad rank 85 of `finite_geometry`'s own E8 test, frame functions and trace-one symmetric `8 x 8` matrices coincide (both of dimension 35) |
| C45 diamond and declared generators | `omega_homology::chain_complex::ChainComplex`, `cyclotomic::Cyc12`, `exact_field::matrix` | `∂_2(A + B) = (1, -1, 0, 1, -1)`: the interior edge cancels, `b_0 = 1`, `b_1 = 0`, and a misoriented face is refused; `-rho_J rho_tau = zeta_12`, `zeta_12^3 = rho_J`, `zeta_12^4 = rho_tau`, `zeta_12^4 - zeta_12^2 + 1 = 0`; `J^2 = -I`, `J^4 = I`, `tau^3 = I`, `tau^2 + tau + I = 0` |
| C46 Sorkin sums | `finite_geometry::{sorkin_coefficients, sorkin}` | `I_3 = 0` identically exactly for `p = 1, 2` among `p = 1..8`; `p = 3` gives `6abc`; `I_2 = 0` identically only for `p = 1` |
| C47 `so(8, Q)` and Cayley isometries | `cayley::{cayley_transform, is_orthogonal}` | 28 independent skew generators, all brackets skew; Cayley transforms at three parameters are isometries with determinant 1 and `I + C` invertible (as for every Cayley transform, `I + C = 2 (I + tau X)^(-1)`), so `diag(-1, -1, 1, .., 1)`, a rational rotation with `I + R` singular, is not one; `cayley` agrees with the corrected `H019` numerator `N(i, j, p, q) / (p^2 + q^2)` for every `X_ij` at `tau = 1, 1/2, 3/4, 2`, the zero generator `X_ii` included, where the published numerator is singular at `p = q = 1` |
| C48 recoupling (not retyped) | exact `2 x 2` rational matrices | `s12^2 = s23^2 = (s12 s23)^3 = I`, the generated group has six elements, characters `(2, 0, -1)` are orthogonal to the trivial and sign characters; the source's "pentagon" check is the braid relation `s23 s12 s23 = s12 s23 s12` |
| C50 signed permutations (not retyped) | exhaustive enumeration | the form-preserving matrices in `{-1, 0, 1}^(n x n)` are the 8 and 48 signed permutations for `n = 2, 3`, each preserving `l1` on a box |
| C51 Cayley hinge spectrum (refuted) | `cayley::{unit_from_parameter, cayley_transform}`, `scalar::multiplicative_order`, `cyclotomic::{Cyc8, Cyc12}` | on the 183 reduced rationals `p/q` with `\|p\|, q <= 12` the Cayley rotation has finite order only at `-1, 0, 1` (orders 4, 1, 4); `2 - Tr U >= 0`, with equality exactly at `U = I`, on 216 products of three rotations; the countermodels below |
| C52–C54, C56, C58, C60, C62 declared simplicial models (not retyped) | `simplicial_gravity` | two tetrahedra glued along one face: area 6 and `256 = 64 x 4` states; Page entropies `0, 1/2, 1, 3/2, 1, 1/2, 0` on the declared schedule, final clock `2/9` and rate `4/9`; see below |
| C57, C59, C61, C63, C64 declared spin-foam models (C61 refuted, the others not retyped) | `finite_spinfoam`, `ModelVersion::Published` | every tetrahedron amplitude at spin levels 2 and 3, and every 4-simplex amplitude at level 2, is 0, 1 or −1; `[2]_q^2 = 3`, `[6]_q = 0`; see below |
| the corrected `H025` and `H027` (not ledger claims) | `finite_spinfoam::{transition_matrix, adjoint_bulk, real_value}` and `PachnerState::partition`, `ModelVersion::Corrected` | on the eight admissible binary boundaries the corrected transition matrix is `a(W) I`: unitary for exactly the 64 binary bulks with `a(W) != 0` (there `a(W) = ±1`) and zero for the other 960; the published matrix has `a(W)` in every entry, and `T* T` is 8 in every entry; the reversed bulk gives the conjugate transpose in both versions; the vacuum bulk is the identity channel and keeps the norm of a wavepacket, and a bulk with `a(W) = -1` flips its sign; the corrected partition `conj(a) (P a)` is real and nonnegative for all 81 amplitudes with coefficients in `{-1, 0, 1}` on five boundary configurations, zero exactly on the zero amplitude and on inadmissible states, and unchanged by unit phases and by the 2–3 move; at `1 + zeta` it is `2 + sqrt(3)`; the published product gives `-1` at `i` and the non-real `zeta^2` at `zeta` |

**Corrections and scope.**

- C12 said the square agrees with itself only on the two exhibited frames and
  that global frame additivity was not proved. At scale 2 it is now decided:
  the square's frame total is `<psi, F psi>`, and each of the 96 orthogonal
  scale-2 frames has `F = 2I`, so the constraint holds for every state of
  `Z[i]^2`. Powers 2–4 violate it. At scale 1 the frames are the coordinate
  axes up to units and no power is excluded, so the constraint discriminates
  from scale 2 on.
- C43 is false as stated, and its row is now `REFUTED BY COMPUTATION`; the
  ray, pair, tetrad and parity counts it also states hold and are computed
  above. All 146 vertices of the Cabello frame polytope are
  non-Bornian (not PSD), but none has least eigenvalue below `-1/2`: exactly
  26 reach `-1/2` and the other 120 stay above `-1/4`. The source's claim
  `lambda_min < -0.5` holds for no vertex. The enumeration covers every basis
  of the incidence (each ray lies in exactly two tetrads, so bases are
  unicyclic subgraphs of the tetrad graph, solved by peeling and checked
  against `A f = 1`).
- C49 is false in three places (`REFUTED BY COMPUTATION`). The two matrices
  the source calls canonical
  extreme vertices are feasible frame functions with 12 nonzero coordinates,
  more than `rank A = 9`, so they are not vertices. The 18 ray projectors are
  states but are not vertices either (support 11). "Eliminating vertices with
  `lambda_min = -1/2`" describes 26 of 146 vertices. In the source code the
  "glued 2-simplex interface operator" is the identity matrix and its boundary
  condition `e_0^T rho e_0 >= 0` follows from positivity, so the filter is the
  PSD test; it removes every vertex.
- C51 is false as stated (`REFUTED BY COMPUTATION`). The closure condition
  `cay_tau(X)^k in {I, -I}` does
  not confine `tau` to the listed spectrum in `Z[zeta_12]`: `tau = sqrt 2 - 1`
  gives the eighth turn, with `C^4 = -I` and `C^2 != +-I`, so its eigenvalue
  has order 8 and does not lie in `Q(zeta_12)`; `tau` is a root of none of the
  listed polynomials. The source's per-hinge list gives `tau^2 - 4 tau + 1` for
  order 12 and misses `tau = sqrt 3 - 2`, which has order exactly 12 and solves
  `tau^2 + 4 tau + 1 = 0`. The listed `1/sqrt 3` squares to `1/3` and is not an
  algebraic integer, so the spectrum is not a subset of `Z[zeta_12]`. The
  "retarded" parameter `(tau_0 - eps) / (1 + tau_0 eps)` is the Cayley
  parameter of the turn by `tau_0` followed by the inverse turn by `eps`; it is
  below `tau_0` only when `1 + tau_0 eps > 0` (`tau_0 = -2`, `eps = 1` gives 3).
- C46: `I_3 = 0` alone does not select `p = 2`; the linear readout also has it.
  Only together with `I_2 != 0` is `p = 2` singled out among the powers.
- C40's "discrete Gleason scaling uniqueness" is the `l2` scaling of the
  unnormalized Hadamard on declared vectors, not a Gleason-type theorem.
- C48: no 6j symbol or Biedenharn–Elliott identity is computed anywhere; the
  check the source names a pentagon is the braid relation of `S_3`.
- C52–C65 put physical names on declared arithmetic. The bound `S <= A/4` is
  the declared unit `A_cell = 4 ln d`; no Schmidt decomposition is computed.
  The Page curve's zero endpoint is the declared schedule. Total Bianchi force
  and torque vanish for arbitrary declared weights (they are sums of opposite
  pairs), while vertex sums do not; `J_B + J_R` is conserved by construction
  for arbitrary `(r, p)`; the four-simplex sum vanishes for arbitrary hinge
  weights, which is `∂∂ = 0`. The constraint "bracket" is a commutator of two
  rational numbers, always 0, so the "anomaly" is minus the induced term. The
  spin-foam amplitudes are signs, so orientation "conjugation" holds because
  they are real. On the eight admissible four-spin boundaries every transition
  is 1: the vacuum column has squared norm 8, so C61's unitarity fails for the
  paper's model (`ModelVersion::Published`); the row is now
  `REFUTED BY COMPUTATION`. The Pachner "partition" multiplies an amplitude by
  itself: amplitude `i` gives `-1`. C64 does not claim a norm, so it keeps its
  type, with this defect recorded here.
- The copies in `lean4/quantum_mechanics/` of `H025` and `H027` have since been
  corrected: the vacuum cobordism is the identity channel on admissible
  boundaries, and the partition conjugates. `finite_spinfoam` now carries both
  versions. `ModelVersion::Published` is the paper's model, the one the ledger
  rows C57 to C64 describe, so their types do not change. C61 stays
  `REFUTED BY COMPUTATION`; its evidence now also cites the corrected model's
  test, marked as a different model. C64 keeps its type.
  `ModelVersion::Corrected` is the corrected Lean's model. The Lean formalizes
  unitarity and norm preservation only for the
  vacuum cobordism, and phase invariance only for vacuum states. The Rust checks
  more instances, all of them finite: the transition matrix `a(W) I` for all
  1024 binary bulks, unitary exactly when `a(W) != 0`, and the partition as a
  Hermitian norm on every declared amplitude (table above). Nothing here
  claims unitarity of a general spin foam.
- `H019` corrects the Cayley numerator of a zero generator, a closed form that
  the Rust never copied: `cayley::cayley_transform` solves the transform exactly
  and agrees with the corrected numerator, the zero generator included.
- `report_fiber::run` reported seven "checks" that were constant expressions
  (`2 + 3 + 5 = 10`, `1 != 2`, `2 < 3`, `4 + 1 = 1 + 4`, `i^2 != 1`,
  `Im i != 0`, `|i|^2 = 1`) and were not tied to the claims they were named
  after; each now computes the property it is named for (2026-09-29). The
  tests here do not rely on them.
- The E8 enumeration in `finite_geometry` takes about a minute in a debug
  build; it is cited through its own test, not re-run.
- C12 is now `EXACT FINITE ALGEBRA`: every statement in the row holds, and its
  remark that global frame additivity is not proved is superseded at scale 2.
  C9, C13 and C39 were fixtures and are now `FINITE COMPUTATION`, as are C14,
  C22, C23, C40, C41, C42 and C47; C45 and C46 are `EXACT FINITE ALGEBRA`.
- The Lean did not move. The package's 52 Lean modules are also tracked,
  byte for byte, in `sources/122_finite_hilbert_boundary_from_primitive_difference/`,
  whose axiom report and build receipt the `LEAN PROVED (RECEIPTED)` rows cite,
  so the rows still resolve after the paper is deleted. Against
  `lean4/quantum_mechanics/`: 8 modules are identical, 29 differ only in how
  they spell their imports, 9 have diverged (the corrected `H019`, `H025` and
  `H027` among them), and 6 have no counterpart (`H000`, `H002` and four `HW*`
  threads, which import files that exist only in `coda_atlas`). Moving them
  would change what the receipts describe, so they stay with their receipts.

**What stays outside.** The receipted Lean rows keep their type; Rust replays
are not substitutes. C0, C19 and C20 are fences, C15 describes the Lean
assembly, C16 points at §7. C38 (the Python dual) is untyped; its finite
content is computed by `report_fiber` and the tests above. C44's MIP and Lie
algebra parts, C50's "layer admission residue", C55's Lean and every physical
reading of C52–C65 are not modelled. Ordinary `M_n(C)`, Gleason uniqueness at
`n >= 3`, CPTP channels, Hilbert-tensor uniqueness, the circle group and
continuous time remain imports, as the paper says.

### 11.54 Boundary synthesis and cochain lifts

**Original paper in the paper archive:** [Universal boundary synthesis and cochain lift](sources/original_papers/206_universal_boundary_synthesis_and_cochain_lift/universal_boundary_synthesis_and_cochain_lift.md).

The paper claims that every earlier contact point factors through one exact
sequence `0 -> C^0 -> C^1 -> C^2 -> Obs -> 0`, that a descent functor to
finite Hilbert spaces is neither full nor faithful, and that the pointer basis
is the zero-curvature kernel `ker d1`. The asserted initial exactness fails on every nonempty graph complex
with ordinary vertex cochains, because constants are killed by `d0`.
The pointer basis is not determined by the complex: the counterexample
below changes it while keeping the complex fixed. The proposed functor is
not defined. What holds is computed here or by the papers the synthesis cites.

| Claim | Now computed by | Checked by (`tests/synthesis/universal_boundary_synthesis.rs` unless noted) |
| --- | --- | --- |
| C1 canonical exact sequence | `finite_cochain_packet::FiniteCochainPacket::{dimensions, primitive_difference, face_coboundary, classify}` | refuted: the sequence is a complex (`d1 d0 = 0` is replayed), but constants lie in `ker d0`, so it is never exact at `C^0`; the failures of exactness `(dim ker d0, dim H^1, dim coker d1)` are `(1, 1, 0)` on the open triangle, `(1, 0, 0)` on the filled triangle and `(1, 0, 1)` on the boundary of a tetrahedron, each checked against the Euler characteristic; the unit circulation of the open triangle is `ClosedResidual` with `Phi1 = 3`; on the tetrahedron the all-ones face functional kills `im d1`, so the fourth term is the top cohomology of the declared surface |
| C4 pointer basis is `ker d1` | `exact_channel::ExactKrausChannel`, `FiniteCochainPacket::dimensions` | refuted: on one carrier (a single edge, `dim ker d1 = 1`) vertex dephasing fixes `\|0><0\|` and `\|1><1\|` and sends `\|+><+\|` to `I/2`, and Hadamard dephasing does the reverse; on a three-vertex path `dim ker d1 = 2` against three pointer states |
| C6 Mermin–Peres parity defect as a 2-cochain `F_2` holonomy | see QM_209 C3 (`tests/synthesis/noncommutative_readout_algebra.rs`) | holds on a declared closed 2-complex whose faces are the six contexts; the "holonomy" is the all-ones face functional |
| C2 lift of weights into U(1) and SU(2) holonomies | `holonomy_interference` (QM_063), `tower_walk_validator` (QM_001) | no lift is constructed; one set of weights carries different relative holonomies (`coherent_intensity_does_not_factor_through_the_l1_weights`), and non-commuting O(2) loop holonomies are detected exactly (`noncommuting_holonomies_are_detected_exactly`); nothing SU(2)-specific is computed |
| C5 Born non-promotion | `pairing_audit` (QM_011) | the finite pairing checks admit a second pairing on the Born packet |
| C7 the descent functor | not defined | its non-faithfulness bullet, equal diagonal densities from different states, is QM_003/QM_004's `sector_weights_do_not_determine_phase` |

**Corrections and scope.**

- C1 is false as written, and its row is now `REFUTED BY COMPUTATION`.
  Exactness at `C^0` needs `d0` injective, and `d0`
  kills constants on every nonempty complex; exactness at `C^1` needs
  `H^1 = 0`. With `Obs = coker d1` the sequence is exact at its last two terms
  by definition, and `Obs` is `H^2` of the declared complex: zero for a disk,
  one-dimensional for a sphere. It is a topological invariant of the carrier,
  not a residual gap between cochain transport and quantum mechanics. The
  first term was declared as nonnegative `L1` weights, a cone rather than a
  group, and the U(1) transports of the second term form a multiplicative
  group, so no exact sequence of groups could start there in any case.
- C4 is false (`REFUTED BY COMPUTATION`). `ker d1` is fixed by the carrier,
  while the pointer basis is fixed by the declared environment; the dimensions
  differ as well. C7 stays `OPEN`: an undefined functor is not refuted by a
  computation.
- C6 is true only on a declared 2-complex. On a carrier graph there are no
  2-cochains (QM_209).
- C7: the functor sends `d^k : C^k -> C^(k+1)` to endomorphisms of
  `l2(V, C)`, which does not define a map on morphisms, so neither fullness
  nor faithfulness is a decidable statement. Its non-fullness bullet
  (continuous unitaries need a time parameter) is QM_211's topic.
- C3, "contraction ratio invariance under cochain boundaries", has no
  definition in the paper. The only reading that makes it a statement,
  composing a channel with gauge (diagonal unitary) channels, is unitary
  invariance of the trace norm, which belongs to QM_080 and QM_081; nothing was
  computed here.
- The claimed "replayable Python / Rust certifiers" and the claim-code map
  point to a module that does not exist.

**What stays outside.** C8, the scope limitation. The category-theoretic framing
is not modelled, no lift of weights is constructed, and
no physical statement follows from any of the computations above.

### 11.55 Complex phase and $U(1)$ transport

**Original paper in the paper archive:** [Complex phase fiber and $U(1)$ transport lift](sources/original_papers/207_complex_phase_fiber_and_u1_transport_lift/complex_phase_fiber_and_u1_transport_lift.md).

The paper's three mathematical statements are already computed by QM_060,
QM_062 and QM_063's modules: weights are blind to vertex phases, a
phase-invariant cross term needs a conjugation, and the relative transport of
two paths is the holonomy of the loop they form. This entry adds no code; it
records which tests hold each statement and what had to be corrected.

| Claim | Now computed by | Checked by (existing tests, file per row) |
| --- | --- | --- |
| C1 `L1` phase blindness under vertex gauges | `phase_blind_quotient::{phase_blind_projection, phase_equivalent, discrete_fiber}` | `tests/superposition/superposition_as_the_quotient_fiber.rs`: the projection is unchanged by per-coordinate unit phases and nonzero scalars; one weight point carries `2^(k-1)` sign and `4^(k-1)` quarter-turn configurations |
| C2 the phase fiber and the involution are imported | `complex_structure_selector::PairingInvolution`, `phase_blind_quotient` | `tests/superposition/the_u1_selector.rs`: under conjugation the cross term is invariant under every unit phase, under the identity only under `±1`; the sign group already gives a nontrivial fiber |
| C3 relative phase is loop holonomy | `holonomy_interference::{CoherentPathFamily, relative_loop}` | `tests/superposition/holonomy_structured_superposition.rs`: `h` is the holonomy of `p` followed by `q` reversed, and it and the intensity survive every vertex gauge while each route's transport does not |
| main claim, `Obs_Phase` in `H^1(G, U(1))` | `holonomy_interference::TreeGaugeFixing` | same file: gauge classes are the fundamental-cycle holonomies, decided with an explicit relating gauge |

**Corrections and scope.**

- "Requires importing a continuous `S^1`" is stronger than anything finite
  shows. Every statement above is exact over the unit Gaussian rationals or
  finite groups of units, and the sign group `{±1}` already gives a nontrivial
  fiber and interference (QM_060, QM_061). What is forced, conditionally, is
  the conjugation for a phase-invariant cross term (QM_062).
- The lift `c = sqrt(w) e^(i phi)` needs square roots. Over `Q(i)` a weight
  point has a lift only when products of weights are sums of two squares;
  `(1/4, 3/4)` has none (QM_060).
- `Delta phi = Arg(U(p1) conj U(p2))` is transcendental; the exact invariant is
  the unit `U(p1) conj U(p2)` itself.
- The claim-code map pointed to a module that does not exist.

**What stays outside.** C4, the scope fence: no Hilbert space or Born pairing
follows from the phase fiber. The continuous circle is not constructed.

### 11.56 Quadratic $L^2$ readout and the cross-term interference boundary

**Original paper in the paper archive:** [Quadratic $L^2$ readout and interference boundary](sources/original_papers/208_quadratic_l2_readout_and_interference_boundary/quadratic_l2_readout_and_interference_boundary.md).

The paper separates the additive $L^1$ readout from a quadratic $L^2$ readout
and puts interference in the cross term
$2\operatorname{Re}(c_1\overline{c_2})$. The separation is
right, but the displayed formula puts the cross term in the wrong quantity:
over orthonormal loci $\|\psi\|^2$ has no cross term. The cross term belongs to
the recombined amplitude $|c_1+c_2|^2$, the quantity the abstract calls
`I_int`. Its vanishing criterion also misses zero amplitudes. Both corrections
compute exactly over `Q(i)`.

| Claim | Now computed by | Checked by (`tests/synthesis/quadratic_readout_interference.rs`) |
| --- | --- | --- |
| C1 `L1` readouts add without cross terms | `exact_field::involution::inner_product` | the norm of `(1, 1)`, `(1, -1)` and `(1, i)` is 2, of `(2, 1 + i)` 6 and of `(3/5, 4i/5)` 1: the sum of the weights for every phase |
| C2 the quadratic readout is an import | `coherent_interference::{interfered_weight, cross_term}` | the recombined readout gives 4, 0, 2, 10 and 1 on the same five configurations, and the first three share their weights; the source's formula equals the recombined readout on all five and differs from the norm on `(1, 1)`, 4 against 2; with two nonzero coordinates a diagonal twin always exists (QM_061, A1) |
| C3 the cross term is nonzero iff `l2` is imported | `coherent_interference::cross_term` | refuted as an equivalence: with the recombined readout imported, `(1, i)` and `(3/5, 4i/5)` have cross term 0, and a zero amplitude gives cross term 0 whatever the phase of its partner; `(1, (3 + 4i)/5)` gives `6/5` |

**Corrections and scope.**

- §1's $P_{L^2}(\psi)=\|\psi\|^2=|c_1|^2+|c_2|^2+
  2\operatorname{Re}(c_1\overline{c_2})$ is false for orthonormal
  $|1\rangle,|2\rangle$. The right-hand side is
  $|\langle\chi,\psi\rangle|^2$ for $\chi=(1,1)$, the readout of the
  recombined amplitude. The norm itself is
  phase blind.
- Theorem 2.1's criterion, nonzero "iff `phi1 - phi2` is not `±pi/2 mod pi`",
  needs `w1 w2 > 0`: a zero amplitude carries every phase, including its
  partner's, and gives no cross term. Exactly: the cross term vanishes when
  `c1 conj c2` is imaginary, zero included.
- C3's "iff `l2` is imported" is kept in its true half: the `L1` readout never
  shows a cross term. Importing the quadratic readout does not make it nonzero.
  The row stays `OPEN`: read as "a cross term can appear only once the
  quadratic readout is imported" it holds, and read as a biconditional for
  every amplitude it fails as shown. C1 and C2 are `FINITE COMPUTATION`.
- The claim-code map pointed to a module that does not exist; the audit row on
  ledger canonicality is refuted and is not cited.

**What stays outside.** C4, the scope fence. Which readout is imported is a
declaration; nothing here selects the Born pairing or an operator algebra.

### 11.57 Noncommutative operator algebras and contextuality

**Original paper in the paper archive:** [Noncommutative operator algebra and contextuality](sources/original_papers/209_non_commutative_operator_algebra_and_contextuality/non_commutative_operator_algebra_and_contextuality.md).

The paper states that diagonal (`L1`) readouts commute, that incompatible
observables need non-diagonal matrices, and that the Mermin–Peres parity
contradiction is a nonzero class in `H^2(G, F_2)`. The first two compute
directly. The third needs a correction: a carrier graph has no 2-cochains, so
the class exists only once a 2-complex whose faces are the six contexts is
declared. On such a complex it is computed exactly over `F_2`.

| Claim | Now computed by | Checked by (`tests/synthesis/noncommutative_readout_algebra.rs`) |
| --- | --- | --- |
| C1 diagonal readouts commute | `exact_field::matrix::{diagonal, commutator}` | all 729 pairs of diagonal readouts with entries in `{-1, 0, 2}^3` commute; `[X, Y] = 2iZ` cyclically, the source's `[X, Z] = -2iY`, and `Z` and `X` do not commute |
| C3 the Mermin–Peres parity class in degree two | `separating_predictions::MerminPeresSquare`, `omega_homology::matrix_reduction::{rank_z2, multiply_z2, is_zero_z2}` | nine observables as edges, the six contexts as faces, and three vertices, the edge in row `i` and column `j` joining `k` and `k + 1` for `k = i + j mod 3`: `d1 d0 = 0`, every edge on two faces, `F_2` Betti numbers `(1, 2, 1)`; the square's sign cochain `(0, 0, 0, 0, 0, 1)` is outside `im d1` (the rank rises from 5 to 6), the all-ones face functional separates it, and none of the 512 edge assignments has it as coboundary, as the square's own search agrees; a second `-1` sign makes the class vanish; the carrier graph has cycle rank 7 and no 2-cochains |

**Corrections and scope.**

- "`H^2(G, F_2)`" with `G` the paper's carrier graph is zero. The class lives
  in the cokernel of the incidence map from observables to contexts. That
  cokernel is the top cohomology of a declared 2-complex with the contexts as
  faces, as here, or the degree-one quotient of QM_120's parity packet, where
  the observables sit in degree zero. The degree is a declaration.
- The existing `separating_predictions::MerminPeresCochainBridge` labelled
  the obstruction an "H^2 obstruction stand-in" without computing a class; it
  now computes the class (2026-09-29).
- C2 (`B(H)` is not derived from `L1` data) has no finite content beyond C1:
  the diagonal algebra is closed under sums, products and adjoints and contains
  no non-commuting pair.
- The package claimed replayable certifiers; the audit refuted that row, and it
  is not cited.

**What stays outside.** C2's derivability statement and C4, the scope fence.
Nothing here says which observables a device measures.

### 11.58 The Born rule and state–effect pairing

**Original paper in the paper archive:** [Born-rule postulate and state-effect pairing](sources/original_papers/210_born_rule_postulate_and_state_effect_pairing/born_rule_postulate_and_state_effect_pairing.md).

For positive real $p$ and a nonzero vector, the paper's power rule
$P_p(i)=|c_i|^p/\sum_j|c_j|^p$ is a probability vector in each orthonormal
context. Theorem 2.1 points to
Gleason's theorem as one route to selecting `p = 2`, under
noncontextuality, positivity and normalization on the full projective domain
in dimension at least three. The finite content computes exactly on declared real rational
contexts: each tested power rule is a probability vector context by context;
the square is basis invariant by Parseval, whereas powers 1, 3 and 4 fail
on the exhibited three-dimensional contexts. In
dimension two every positive-power rule is context free, so the dimension hypothesis
carries weight. `power_rule_outcomes` holds the rules and the search for a
context dependence.

| Claim | Now computed by | Checked by (`tests/synthesis/born_power_rule_pairing.rs` unless noted) |
| --- | --- | --- |
| C1 $L^1$ proportions $w_i/\sum_jw_j$ | `residual_density_calculus::ResidualLedger` | `native/tests/residual_density_boundary.rs`: $(3,1,0)$ gives $(3/4,1/4,0)$; empty, negative and zero-mass ledgers are refused |
| C2 the Born rule as a quadratic trace pairing, imported | `exact_hermitian::{outer, hs_inner}`; `pairing_audit` | with `E = (1, 1)(1, 1)*`, `Tr(E rho)` reads 1 on `e_0` and on `e_1`, 4 on their sum and 0 on their difference, and a mixture reads the mixture of the readings (`5/3`); the finite pairing checks admit a second pairing on the Born packet (`tests/foundations/state_effect_pairing_audit.rs`) |
| C3 normalized power rules; the square follows from Parseval, broader uniqueness imports Gleason | `power_rule_outcomes::{Context, power_rule, normalizer, find_context_dependence}` | powers 1 to 4 give probability vectors on three rational contexts of `Q^3`; for `psi = (1, 1, 0)` the normalizers are `2, 2, 2` for the square and `2, 12/5, 8/5`, `2, 216/125, 344/125`, `2, 962/625, 2402/625` for powers 1, 3, 4; `e_1` gets `1/2` in the standard basis and `5/12`, `125/216`, `625/962` in a basis rotated about it, also when that basis lists `-e_1`; the square gives the Born weight and no dependence on every context; in `Q^2` no power rule is context dependent, the first power gives `e_1 -> 1`, `e_2 -> 0`, `(3/5, 4/5) -> 3/7`, `(4/5, 3/5) -> 4/7`, and the only symmetric matrix matching the first three values, `[[1, 1/14], [1/14, 0]]`, gives `124/175` on the fourth and has determinant `-1/196` |

**Corrections and scope.**

- "`P_p` defines a valid probability measure" holds context by context only.
  For the nonzero vector $\psi=(1,1,0)$, compare the standard basis with
  $(e_1,(3e_2+4e_3)/5,(-4e_2+3e_3)/5)$. The common ray $e_1$ has weight
  $1/2$ in the first and $1/(1+(3/5)^p+(4/5)^p)$ in the second. For
  $p>0$, the sum $(3/5)^p+(4/5)^p$ is strictly decreasing and equals one
  precisely at $p=2$. Thus every positive $p\ne2$ fails context independence
  on this same rational pair of bases. This written argument covers all
  positive real powers; the exact native tests evaluate powers 1, 3 and 4.
  At $p=2$, Parseval gives the same total in every orthonormal context.
- In dimension two a unit vector has one orthogonal complement up to sign, so
  every positive-power rule is context free there, and the first power is not of the
  form `<b, rho b>` for any Hermitian `rho` (on real rays only the real part of
  `rho` acts). Non-contextuality does not select the square in dimension two;
  that is why Gleason's theorem needs dimension three.
- Gleason is not needed to select the square within this power family.
  Its broader conclusion, that a
  nonnegative normalized frame assignment on the full real or complex
  Hilbert projective domain in dimension at least three is of Born form,
  is imported. The finite examples do not prove it on a restricted number field.
- C2's "non-linear" holds in the amplitude only: the pairing is linear in the
  density matrix.
- The paper's "`L_p` norm pairings" are powers of moduli, not norms. Complex
  amplitudes with irrational moduli are outside this exact carrier. The
  displayed integer-power checks use real rational vectors. The argument for
  arbitrary positive real powers uses ordinary real arithmetic; it is not
  claimed as a new exact native implementation or Lean proof.

**What stays outside.** C4, the scope fence. Gleason's and Busch's theorems
and any physical selection of the pairing are not computed.

### 11.59 Continuous unitary dynamics and the remaining synthesis problem

**Original paper in the paper archive:** [Continuous unitary dynamics and $L^1$-to-quantum synthesis](sources/original_papers/211_continuous_unitary_dynamics_and_l1_to_qm_synthesis/continuous_unitary_dynamics_and_l1_to_qm_synthesis.md).

Theorem 1.1 says that discrete stochastic steps cannot generate a continuous
unitary group without importing continuous time, a Hermitian generator and a
differentiable structure, and its proof says that discrete steps allow only
integer powers. The conclusion holds, for a different reason. Stochastic steps
can have fractional powers on continuous stochastic semigroups; what they
cannot be, short of a permutation, is an `l2` isometry. So the stochastic
matrices meet the unitary group in a finite group, whatever time parameter is
declared. `stochastic_unitary_boundary` computes both halves. The five-import
synthesis (C2, C3) is not a finite statement.

| Claim | Now computed by | Checked by (`tests/synthesis/unitary_dynamics_import_boundary.rs`) |
| --- | --- | --- |
| C1 unitary dynamics import boundary | `stochastic_unitary_boundary::{isometric_permutation, TwoStateGenerator, two_state_embedding}`, `scalar::is_unitary`, `cayley_unitary::{cayley_unitary, cayley_generator}` | of 25 two-state and 216 three-state stochastic steps on rational grids, the `l2`-isometric ones are exactly the 2 and 6 permutation matrices; the semigroups `T(s) = I + (1 - s) Q / (a + b)` satisfy `T(s) T(s') = T(s s')` and `det T(s) = s`, and are isometric only at `s = 1`; `[[5/8, 3/8], [3/8, 5/8]] = T(1/4)` has the stochastic square root `T(1/2) = [[3/4, 1/4], [1/4, 3/4]]`; the swap (determinant `-1`) and the averaging step (determinant `0`) lie on no semigroup, while `iX` is the Cayley step of `-X` at `tau = 1`; `C_1(diag(1, 0)) = diag(-i, 1)` has determinant `-i` |

**Corrections and scope.**

- "Discrete carrier steps permit only integer matrix powers" is false:
  `[[5/8, 3/8], [3/8, 5/8]]` has a stochastic square root, and every
  two-state step with positive determinant lies on a semigroup `T(s)` with a
  continuous parameter. The obstruction is isometry: an `l2`-isometric
  stochastic matrix is a permutation matrix (a row with entries in `[0, 1]`
  summing to one and squares summing to one has a single entry 1), so no
  nonconstant continuous path of unitaries runs through the stochastic
  matrices. The populations of a unitary step do not compose as a semigroup
  either (QM_082, `the_shadow_of_a_composite_is_not_the_composite_of_the_shadows`).
- "`U(t)` in `SU(N)`" is too narrow: a Hermitian generator gives a unitary, and
  with nonzero trace its Cayley step `C_1(diag(1, 0))` has determinant `-i`.
- No exponential is computed. The unitary family is the Cayley chart
  `tau -> C_tau(H)` of §11.19 (`cayley_unitary::cayley_unitary`),
  and the stochastic semigroup is parametrised by
  `s = exp(-(a + b) t)`.
- C3's "five independent imports" is not a finite statement: independence is
  not defined, and as written the Born import `P(i) = |<i|psi>|^2` already uses
  the inner product of the quadratic-readout import. The cascade's second step
  repeats QM_208's misplaced cross term ($\|\psi\|^2$ has none).
- The cascade is not a minimal Bell price list. The exact static CHSH endpoint
  uses a bipartite composition, an entangled state, incompatible same-party
  observables and a positive trace/Born pairing. Its matrices are real and no
  continuous dynamics appears, so QM_207's specifically complex phase fiber
  and QM_211's continuous-time import are not individually necessary for
  Tsirelson saturation. Conversely, the five-item diagram omits the composition
  and locality structure that makes a Bell scenario a Bell scenario.

**What stays outside.** C2 (the diagram), C3 (the synthesis theorem) and C4
(space-time and ontology) have no finite content. Continuous time,
differentiability and Stone's theorem are not modelled.

### 11.60 The Microsoft Majorana problem

**Original paper in the paper archive:** [The Microsoft Majorana problem](sources/original_papers/212_microsoft_majorana_problem/microsoft_majorana_problem.md).

The paper names a packet gap: hardware narratives about Majorana devices and
declared finite algebra live on different carriers, and neither discharges the
other. It keeps two exact cores, the `GF(2)` residual trichotomy on declared
complexes and specialized Ising identities, and fences everything physical.
The `GF(2)` core already lives in the `omega_majorana` crate and in QM_120's
`parity_context_packet`; this entry does not duplicate it. What was missing is
the declared operator algebra that the Majorana and Ising vocabulary refers
to. It now computes exactly over `Q(i)` in `majorana_fock_algebra` and
`omega_fusion_categories::fusion_ring`: Jordan–Wigner Majoranas on a declared Fock space, the
parity, a declared Kitaev chain, Majorana braid unitaries whose restriction to
a parity sector is the paper's Ising pair, and the Ising fusion table. None of
it is evidence about a device.

| Claim | Now computed by | Checked by (`omega_engine/crates_rs/tests/omega_majorana/majorana_parity_algebra.rs`, kept under `omega_quantum_physics/tests/synthesis/` in the 2026-10-14 archive, unless noted) |
| --- | --- | --- |
| C8 parity as a `Z_2` observable commuting with a declared Hamiltonian (fence) | `majorana_fock_algebra::{FockCarrier, first_anticommutation_failure}` | for 1 to 4 modes the Majoranas are Hermitian with `{g_a, g_b} = 2 delta_ab I`, and the `c_j` satisfy the canonical anticommutation relations; without the `Z` strings the first failure is `(gamma_1, gamma_3)`; the parity is `(-1)^N`, anticommutes with every Majorana and commutes with every bilinear; the declared chain is Hermitian and commutes with the parity at all 27 points of `t, Delta, mu in {-1, 1/2, 2}` on two modes and at a point on three |
| C6 the Kitaev chain is an imported model (fence) | `FockCarrier::{kitaev_chain, restrict_to_sector}`, `exact_field::{elimination::rank, ordered::hermitian_is_positive_semidefinite}` | at `t = Delta`, `mu = 0` the chain equals `i t sum_j gamma_(2j) gamma_(2j+1)` for 2 to 4 modes and `t = 1, 2/3, -3`, and exactly the two end Majoranas commute with it; on three modes its spectrum is `-2, 0, 2` with multiplicities `2, 4, 2`, and the ground space holds one state of each parity; at `mu = 1/2` or `Delta = 1/2` the end Majorana does not commute with the chain, and on two modes the odd ground energy is exactly `-1` while the even one lies strictly below it |
| C7 Ising fusion and specialized braid identities (fence) | `FockCarrier::braid_unitary`, `omega_fusion_categories::fusion_ring::FusionTable`, `close_under_multiplication` (a helper declared in the test) | the braid unitaries `((1 + i)/2)(I + gamma_(a+1) gamma_a)` are unitary of order 4, square to `i gamma_(a+1) gamma_a`, satisfy the braid and far-commutation relations and conserve parity for 2 and 3 modes; on the even sector of two modes they are `R' = diag(1, i)`, `F R' F` and `R'`, the source's `R` and `F R F` times `e^(i pi/8)`, with `F^2 = I`; the images are finite groups of order 96 (with 4 scalars) on that sector and 768 on the whole two-mode Fock space; the declared fusion table is unital, commutative and associative in all 81 cases, and three mutated tables fail at the expected law; `2L` copies of `sigma` have `2^(L-1)` fusion paths to each of `1` and `psi`, the dimensions of the two parity sectors, for `L = 1..5` |
| C13 the retracted tetron carrier | `omega_homology::matrix_reduction::rank_z2` | the carrier of `omega_engine_atlas/coda_atlas/F004_papers/009_ms_majorana/code/majorana/carriers/tetron_carrier.py` (source 212's `carriers/tetron_carrier.py`), rebuilt, has graph cycle rank `T - 1` and `dim H^1 = 0` over `F_2` for `T = 1..4`: every cycle it has is filled |
| C2 to C4, C11, C12, C14, C15 `GF(2)` trichotomy, rejection cases, local/global parity obstruction, tetron homology, distances, `Phi1` | `omega_majorana::{classify, gf2_terminalizer, lggr, tetron, harmonic}` | that crate's own tests, not rerun here; see QM_120 for the parity packet |

**Corrections and scope.**

- The anticommutation check is `dirac_gamma_admission::CliffordFamily::admit`
  with a Euclidean metric (QM_050); `first_anticommutation_failure` only
  translates its refusals.
- The paper points at `omega_engine/crates/omega_majorana`; the crate is
  `omega_engine/crates_rs/omega_majorana`. Its `Cyclotomic16Element` multiplies
  in `Q(zeta_16)`, but no braid identity is checked there. The braid relation
  is now checked over `Q(i)`: the global phase `e^(-i pi/8)` of the Ising `R`
  is the only part outside `Q(i)`, and it cancels in every relation that is
  homogeneous in `R`.
- The Ising matrices of §3.2 are the Majorana braid unitaries restricted to the
  even sector of two modes. The Kitaev sweet-spot statements are identities of
  declared matrices. The phase table `|mu| < 2t` is not: at `mu = 1/2`, inside
  it, the end Majorana is not conserved at any size checked, and on two modes
  the parity degeneracy splits.
- "Ising alone is computationally non-dense" has a finite core: the braid image on the
  four-`sigma` space is a finite group of order 96, 24 up to scalars, so it is
  not dense in `SU(2)`. Computational density with supplements is not computed.
- C13, the retraction of the old tetron carrier, is confirmed on the carrier
  rebuilt from its Python source.
- C16's timing (17 ms per residual at `6 x 6`) is a measurement and is not
  reproduced. C17 stands: on `{0, 1}` vectors every powered norm is the weight,
  so every `l^p` has the same minimisers.
- C15 says that certifying `Phi1` over `GF(2)` is minimum-weight coset
  decoding, which the source calls NP-hard in general; the carriers here are
  small and declared, and no hardness statement about them is made or
  computed. The lemma `transfer_defect_lower_bound_pos` belongs to the separate
  Majorana package (`omega_engine_atlas/coda_atlas/F004_papers/009_ms_majorana/lean4/MajoranaCore.lean`),
  not to source 212. It establishes only that the product of two declared
  positive natural-number parameters is positive (`Nat.mul_pos`) and is not a
  formal leakage result.

**What stays outside.** C1 is a definition, and C5, C6, C8, C9, C10 and C17
remain fences. No device, capacitance, topological phase, Pfaffian sign
structure, fermion sign problem or vendor result is touched by any
computation here.

### Defects fixed in pre-existing code (2026-09-29)

Found during the port and fixed after it. Each fix refuses bad input with a
typed error or computes what it names, and has a test that fails on the old
code.

- **QM_120** — `MerminPeresSquare::verify_no_noncontextual_assignment`
  returns `Result`: it searches up to 16 observables and refuses unpaired,
  malformed and oversized squares. Above twelve observables it used to return
  the declared flag. `MerminPeresCochainBridge` computes the degree-two class
  with `ParityContextPacket` instead of multiplying the declared signs.
- **QM_122** — `report_fiber::run` computes each check it names (scaled
  simplex, Gram forms, orthonormal frames, rival pairings, exponent-two phase
  groups, Pauli `Y`, the isometry envelope, fraction pairs, power readouts);
  seven of them were constant expressions. `finite_geometry_host::run` reports the
  braid relation `s23 s12 s23 = s12 s23 s12` as `braid_relation` (it was
  called `rational_pentagon`; no 6j symbols exist here) and derives the `S_3`
  characters from the generated group. C48's check path is updated in both
  claim maps.
- **Channels** — `cptp_channels_stinespring` computes each
  census channel's dilation conductor from an exact `LDL*` of its Choi matrix
  and a four-square split of the weights. Every census dilation lives over
  `Q`; the old constants 12 and 28 were the conductors of `sqrt(3)` and
  `sqrt(7)`, which no dilation needs.
- **Target 13** — `import_bundle::ob_u1_holds` computes the phase fiber of the
  declared phase group on the amplitudes; its imaginary-part test could never
  change the result. Monoidal, OB-U1, BornGleason and Instruments are
  documented as declaration slots.
- **Target 18** — `born_gleason`'s non-contextuality and the other assumption
  flags are documented as declarations wherever they are reported; its
  scalar is now `BigRational` (the `Ratio<i64>` sum overflowed).
- **Smaller fixes** — `Pauli::from_char` refuses unknown letters (they became
  `I`); `quadratic::Surd::new` refuses a negative radicand (it panicked);
  `lorentz_boost`, `boost_composition`, `quantum_correlation` and
  `group_parameter` use `crate::rational::Rational` instead of `i128`
  rationals that wrapped silently in release builds (the c1000 JSON is
  unchanged); `omega_holonomy` reports `SingularMatrix` and documents that the
  Bianchi check needs face loops at one base point; `omega_majorana`'s
  element is documented as `Z[zeta_16]` with no braid check, and its product
  is overflow-checked. `rotation_groups` keeps its own overflow-checked
  `i128` rational.

## 5. Detailed implementation and reproduction record

This section records how selected finite certificates can be reproduced. The
software properties described here are not substitutes for the mathematical
arguments in §4 of this supplement and main paper §13. The Rust crate
`omega_engine/crates_rs/omega_quantum_physics` held parallel versions
of several finite objects: a fixed-width stochastic kernel, a floating-point channel
stack with tolerances, a Hermitian spectral face on its own `Ratio<i64>` scalar, and
code distances written in as constants. Each concept now has one exact
implementation; every other module calls it or is labelled a floating-point
diagnostic.

| Concept | Source | Exact implementation | Change |
| --- | --- | --- | --- |
| Stochastic kernels | QM_082 | `finite_classical_shadow::StochasticMap` | `BigRational` entries replace `Ratio<i64>`. Fields are private, so a kernel exists only after `try_from_rows` has checked shape, signs and exact row sums; `ProbabilitySimplex` likewise. |
| CPTP channels | QM_080, QM_082 | `exact_channel` | New. Weighted Kraus form over ℚ(i) with zero-defect trace preservation; Choi matrix with complete positivity by exact PSD and `Tr_out J = I`. |
| Hermitian operators over ℚ(i) | QM_080 | `exact_hermitian` | `BasicMatrix<GaussianRat>` supplies the matrix carrier. The earlier `QiMatrix` compatibility alias is retired. PSD is decided exactly on the real embedding by the LDLᵀ of `omega_linear_algebra`. Spectral projectors are built for a declared rational spectrum and accepted only if the declaration is exactly the spectrum. |
| Trace norm, dual witnesses | QM_080 | `trace_norm_certificate` | New. `H = P − N` with `P, N ⪰ 0` and `−I ⪯ W ⪯ I`, accepted only at zero duality gap `tr(W H) = tr P + tr N`. `sign_from_spectrum` covers every rational spectrum at any `n`. |
| Hermitian spectral face | — | `hermitian_spectral` | Its scalar `GaussianQ` (`Ratio<i64>`) is removed; it stores a `BasicMatrix<GaussianRat>` and uses the checks above. It still finds spectra only in its supported cases (diagonal, 2×2 split) and rejects the rest as before. `certify_trace_norm` passes an admitted spectrum to `sign_from_spectrum`. Its callers moved with it; `instruments` narrows eigenvalues to its `Ratio<i64>` with an explicit range error, never a wrap. |
| Stabilizer code distance | Targets 12, 14 | `stabilizer_code_distance` | New. `k = n − rank_F2(S)`; the distance is the least weight in `N(S) \ S`, by exhaustive search in increasing weight, refused past its budget. `shor.rs` (`[[9, 1, 3]]`) and Target 12 (`[[4, 2, 2]]`) now compute `n`, `k` and `d` instead of declaring them. |

**QM_082 — channels as stochastic kernels.** A channel's classical shadow is a
`StochasticMap`. Composition now runs past the `i64` ceiling: a composite entry
with a 79-bit reduced denominator is exact, where the old carrier could not hold it.

**QM_080 — trace-norm geometry and dual witnesses.** In the tested case the exact
trace distance contracts under an exact CPTP map: depolarizing at `p = 1/2` takes
`½‖ρ − σ‖₁` from `1` to `1/2`. That is one certified instance, not the
data-processing inequality.

**The floating-point channel modules are diagnostics.** `kraus_operators`,
`quantum_channel`, `completely_positive_map` and `stinespring_dilation` remain,
because they accept floating inputs and numerical SVD output. An algebraic
number such as `√0.3` has an exact algebraic form but lies outside the
rational scalar face used here; a floating approximation is not converted
into an exact witness. Each caller keeps the float path
and says so.

| Caller | Decision |
| --- | --- |
| `completely_positive_map` → `quantum_channel`, `kraus_operators` | Diagnostic. Its complete-positivity check read singular values, which are never negative, so it could not reject any Choi matrix. It now reads Hermitian eigenvalues and refuses the transpose map, as `ExactChoiMatrix` does. |
| `stinespring_dilation` → `quantum_channel` | Diagnostic: its Kraus entries are irrational. |
| `tests/mutation_kill_tests.rs` MUT-01 → `quantum_channel`, `kraus_operators` | Tests the float face itself; the exact counterpart is in `exact_channel`. |

`kraus_operators::DEFAULT_TP_TOL = 1e-6` is a diagnostic threshold, not a
certificate. Where both paths exist the float channel is checked against the exact
one: depolarizing at `p = 1/5`, and amplitude damping at `γ = 9/25`, where `√γ` and
`√(1 − γ)` are rational.

The port's historical validation records describe the tests then executed.
This section does not assert a fresh run of every pre-existing test. Current
focused reproduction has the explicitly recorded scope; code ownership alone
does not promote a claim.

**Merged with the section-11 port.** The paper port of section 11 had created
modules with the same four names on its own branch. The merge kept one
implementation of each concept:

- `exact_hermitian`: one Hermiticity check (`check_hermitian`, with
  `is_hermitian` as its yes/no form), one PSD decision (`is_psd`, with
  `is_positive_semidefinite` as its yes/no form) and one error type
  (`ExactHermitianError`), next to the port's builders, products and partial
  traces.
- `trace_norm_certificate`: `TraceNormCertificate` is the one trace-norm
  verifier. The port's `SignCertificate` checks its four sign identities and
  then certifies the norm by passing `(X_+, X_-, S)` through
  `TraceNormCertificate::try_new`. Its builder, now
  `sign_certificate_from_spectrum`, uses `spectral_resolution`, so a declared
  spectrum with a value that is not an eigenvalue is refused where the port
  accepted it.
- `exact_channel`: `ExactKrausChannel` is the one Kraus channel; the port's
  `KrausChannel` is gone. It gained the Heisenberg dual and fixed-family
  Stinespring/complementary-channel helpers. These helpers require rational
  square roots of the supplied weights; that restriction belongs to the chosen
  presentation. The separate `LDL*`/four-square construction above can instead
  enlarge the Kraus family. `apply_choi` and `choi_is_cptp` run on the one Choi
  implementation.
- `stabilizer_code_distance`: one `StabilizerCode`, with the port's alphabets,
  syndromes, decoder and uncorrectable pairs. Every enumeration is budgeted, and
  the correction radius is refused over a two-letter alphabet, where it was
  wrong: for the bit-flip code over `{X, Y}`, `XII` and `YII` share a syndrome
  and their product `ZII` is logical.
- `u1_phase_completion` (`FQ-GAP-U1-CIRCLE`, `FQ-GAP-BORN-UNIQUENESS-GLEASON`):
  `code/python/src/qm/u1_phase_completion.py` and `code/rust/src/qm/u1_phase_completion.rs`
  replay in exact rational and quadratic $\mathbb{Q}(\sqrt{5})(i)$ / $\mathbb{Q}(i)$ arithmetic
  the seven kernel-checked Lean 4 modules `lean4/U1PythagoreanObstruction.lean`,
  `lean4/U1PowerMapInjectivity.lean`, `lean4/U1CayleyProjectiveCircle.lean`,
  `lean4/U1CyclotomicTorsionTower.lean`, `lean4/U1CauchyCircleCompletion.lean`,
  `lean4/U1ChebyshevCauchyBridge.lean`, and `lean4/U1PhaseSynthesis.lean`
  (sealed in `dag/results/FQ-GAP-U1-CIRCLE/runs/20261020T223000Z_u1_phase_completion_lean`),
  covering projective $\mathbb{P}^1(\mathbb{Q})$ Cayley compactification, 5-adic
  non-square half-angle obstruction, mod-5 Gaussian power injectivity,
  cyclotomic $\mathbb{Q}/\mathbb{Z}$ torsion-tower divisibility and Haar
  orthogonality, Chebyshev/Taylor Cauchy completion over `RegPhaseSeq`, and the
  4D $\mathbb{Q}(i)$ Hermitian Frobenius-trace Born representation (`HermitianMat2Qi`).

## 6. Open implementation programme and supporting files

### 13.9 The five next derivations, in priority order

These are programme targets, not completed general derivations or a new
success census. The classical-storage obstruction of main paper §13.7 advances the
sufficient-record and premise-separation targets on a supplied qubit model;
it does not derive that model from native histories. Their order follows the
dependencies of the measurement account.

1. **Native histories to an available positive operational algebra.** Start
   with one Genesis/S(n) history presentation and prove which questions its
   quotient preserves. Construct the chosen dagger/groupoid algebra and state
   exactly where scalars, a positive cone, composition and available effects
   enter. Compare a classical commutative realization and the coherent one on
   the same protected experiments. The target is a faithful finite bridge with
   a premise-minimality countermodel for each unearned quantum input, not an
   inference from a dimension count. Reuse the category, Lie, number-theory,
   linear-algebra and WDP owners; finite sign holonomy alone does not supply
   the entire complex phase structure.

2. **Born representation on an explicitly closed effect domain.** Extend the
   present four-effect tomography and finite frame checks to a precise
   additivity, noncontextuality, normalization and positivity theorem on the
   chosen domain. Prove a positive trace-one representation there, or exhibit
   a valid non-Born countermodel. Distinguish all effects from a finite probe
   set and projective rays from normalized vectors; state any scalar extension
   or regularity needed to enlarge the domain. Reuse the exact linear-algebra
   and quantum-physics owners and the scoped Gleason/Busch Lean fragments.
   Representation under these assumptions would still price, rather than
   derive, those assumptions from primitive difference.

3. **An instrument derived from a declared apparatus coupling and report.**
   Starting with admitted preparation, isometry/unitary and pointer data,
   derive the grouped outcome maps, their effects, disturbance, non-selective
   channel and null-sector refusals. Prove the diagram from interaction to
   protected record questions commutes, and compare distinct instruments with
   the same effects. Reuse the exact instrument, Kraus, conditioning and WDP
   packet owners. The target closes a finite apparatus-to-instrument splice;
   conditioning remains dependent on an obtained outcome.

4. **Stable, sufficient records under composition and limited control.**
   For one specified open-system dynamics and effect menu, derive a pointer
   record algebra and the least available completion needed for future
   reports. Prove explicit error bounds for a declared time horizon and a
   compatible multi-observer comparison. Include an erasure control and a
   noncommuting-observable counterexample. Reuse exact population shadows,
   trace-norm witnesses, finite report gluing and the cochain/closure owners.
   An unrestricted linear completion, a product residual or a small sampled
   defect alone cannot certify physical record availability or entanglement.

5. **Outcome-premise separation with a finite observer/eraser protocol.**
   Extend the example above to a record-preserving observer and an observer
   with coherent joint control. For each proposed event or relative-record
   premise, derive its probabilities, repeatability and compatible-history
   conditions on exactly that protocol. Retain the affine deterministic-label
   obstruction as a control and identify what enlarged carrier escapes its
   hypotheses. Reuse finite instruments, history descent, contextuality and
   probability owners. A finished result must distinguish experimentally
   different predictions from empirically equivalent interpretive choices;
   it must not present a simulation's selected branch as a derived ontology.

### 13.10 What supports this account

The instrument formulae and reversible example are finite algebra on supplied
quantum inputs. The factorization and midpoint arguments are the explicit
mathematical reasoning above. Existing exact Rust controls include
`tests/exact_instrument_finite.rs` and the conditioning test in
`tests/measurement_exact_laws.rs` under the quantum-physics owner. Their scope
is admitted instrument/dilation identities, conditional states, probabilities
and refusal controls; these tests do not establish every claim in this section.
The broader Weyl/Gleason reproduction uses a separately dated audit and is not
a fresh complete build in this edition.
The classical-storage proof is separate from the eight exact native tests in
`tests/classical_storage.rs`: sharp and strict-margin
fixtures, a refined/zero-letter POVM, rectangular retrieval, complex Choi
orientation, malformed/nonpositive refusals, a static classical countermodel,
and available-control failure of a population-only report. They do not test
unrestricted hidden-variable ontologies or realize a laboratory protocol.
The additional Lean results have exactly the scope stated in main paper §13.8. No physical
record-selection law or completed primitive-to-QM derivation is asserted. A suitable next result must retain
its premises, a protected-question contract and an independently replayable
finite witness or counterexample.

## 7. Removed implementation-specific carrier passages

Retained as a historical record. Nothing below is asserted beyond main paper
§13.8; where the two differ, §13.8 governs.

#### 13.8.1 Connection to Projection Obstruction and native Genesis

The three tests of main paper §13.8 (future-question sufficiency, positive
Bell gluing, central sectors and purification) belong to distinct
mathematical interfaces. Phase-sensitive
readouts and minimal report spaces concern sufficiency relative to declared
future experiments; the central-weight bounds concern extensions of states on
direct-sum matrix algebras. None of these statements selects the underlying
quantum state space. A detailed comparison is retained in the local companion
manuscript [12].

The native construction now closes a declared finite reachable passage
carrier and identifies states exactly when all admitted continuations have
equal protected answers and equal availability. Explicit joint operations
either preserve paired local reports or return a distinguishing continuation
and a stable refinement. These constructions implement a minimal report
relative to that finite experiment; they do not yet provide the positive
observable algebra, complex scalars or tensor composition of a quantum model.
The native experiment guide [26] states the source, implementation and Lean
boundaries.

The native Bell experiment and Test 2 have different premises. Shared positive
preparation weights and local native responses construct a Bell-local model.
Changing those weights with the settings gives the guide's full-support,
no-signalling table with $S=12/5$; its setting dependence is explicit. Test 2's
$S=14/5$ instead has the supplied quantum realization above. Both tables
exclude a common positive local extension, but only the latter is furnished
here with quantum states and measurements. Neither constructs those quantum
operations from Genesis.

Reference [12], §4.3.2, also separates partial-trace consistency from product independence:
true marginals and products of one-site marginals each form a closed section,
even when their difference is nonzero. Its §7.4 in the local companion copy
(version 6.9.18; [12] does not list that section) concerns defects hidden by
observer kernels; Bell gluing additionally requires positivity across
measurement contexts. “Local observer,” “local tomography,” and Bell “local
causality” therefore carry separate hypotheses. Appendix E's premise table
records the remaining algebraic, composition and availability assumptions,
including the distinct roles of finite Weyl representations and Gleason-type
probability uniqueness. The first derivation target below remains open at
precisely that operational quantum realization step.

## 8. Detailed foundational walk and target implementation notes

The mathematical exposition is organized by question and result. Main paper
§11 collects its six principal exact results; this supplement records the
detailed constructions, corrections, and a local address for every source
manuscript used there. Provenance supports the argument but does not
organize it.

Several sources share the following proposed interface. It is a list of supplied
objects, not a theorem and not a structure instantiated by every paper:

| Slot | Proposed common interface |
| --- | --- |
| **Primitive difference** | $(d_0 f)(u,v) = f(v) - f(u)$ on a declared finite directed graph; $\delta c$ read as defect mass |
| **Carrier** | Finite graph $0$-cochain, lifted toward a Hilbert space |
| **Cochain complex** | $C^0 \to C^1 \to C^2$ |
| **Coboundary maps** | $\delta^0,\ \delta^1$, with $\delta^1\delta^0 = 0$ |
| **Equality criterion** | The declared zero relation used by the $L^1$ quotient |

The main paper's argument proceeds from the eight-rung inventory and
twenty-two finite targets in its §1 to evidence standards (§§2–3), established results (§4), open
boundaries (§§5, 7, and 9), higher-dimensional examples (§10), principal exact
theorems (§11), reproduction (§12), and the measurement synthesis (§13).
Continuous time and the Born rule remain supplied structures; its §5 states the
missing selection arguments directly.

Individually scoped Lean statements and exact programs accompany selected
results. Their precise file and theorem addresses are in §4 of this
supplement and in the code companion; a module name does not establish a broader theorem.

### 1.1 The 8-Rung Foundational Walk (Rungs 1 to 8)

The foundational walk arranges finite constructions and imported quantum
structures across eight rungs. It is not an eight-step derivation of quantum
mechanics. Numerical examples are reached through
`python/finite_qm/use_cases/foundations.py`, which re-exports them; the rung
functions are defined in `rungs.py` (some also in `interference.py`) in that
folder;
selected algebraic statements are formalized in Lean 4 (`PrimitiveDifference.lean`, `FiniteCochain.lean`, `FiniteDensity.lean`,
`DualWitness.lean`, `BornNormalization.lean`, `Superposition.lean`, `Entanglement.lean`,
`GleasonTheorem.lean`). Each rung answers three mandatory questions:

#### Rung 1: Primitive Difference

- **(i) What is derived here?** The primitive difference operator $D(x, y) := y - x$ on discrete
  carrier coordinates, certified sameness ($x \sim y \iff D(x, y) = 0$), antisymmetry
  ($D(x, y) = -D(y, x)$), and the 1-cocycle identity on 0-simplexes ($D(x, y) + D(y, z) = D(x, z)$).
  Mechanized in `lean4/PrimitiveDifference.lean` (`diff_self`, `same_iff_eq`, `diff_antisymm`,
  `diff_cocycle`) and computed in `python/finite_qm/use_cases/foundations.py`.
- **(ii) What is imported here, and named as an import?** A declared discrete carrier set equipped
  with an abelian subtraction operation (integer coordinates $\mathbb{Z}$). No metric, topology,
  probabilities, or Hilbert space are imported.
- **(iii) What is not selected by these data?** The declared difference and
  equality relation do not select the norm, topology, or physical geometry
  required by the later quantum models. Those structures must be specified
  separately. For example, the same equality relation already defines the
  discrete metric $d_D(x,y)=0$ when $D(x,y)=0$ and $d_D(x,y)=1$ otherwise, so
  the issue is nonselection of the intended geometry, not impossibility of
  defining any metric. A finite discrete state set admits no nontrivial continuous action
  of the connected translation group; a finite set of basis labels does not
  prevent continuous transformations of amplitudes over a supplied scalar field.

#### Rung 2: Finite Cochain Packet

- **(i) What is derived here?** The coboundary sequence $C^0 \xrightarrow{d_0} C^1 \xrightarrow{d_1} C^2$
  on a declared directed 2-complex, boundary nilpotence $d_1 d_0 = 0$, a finite linear-program formulation of
  quotient mass $\Phi_1([x]) = \inf_\alpha \|x - d_0 \alpha\|_{1, w}$, the gauge-invariant closure defect
  $\Gamma_2([x]) = \|d_1 x\|_1$, and the diagnostic trichotomy (`ExactClass`, `ClosedResidual`,
  `ActiveClosureFailure`). Mechanized in `lean4/FiniteCochain.lean` (`d1_d0_zero`, `coboundary_is_cocycle`,
  `d1_add_coboundary`, `non_trivial_circulation_not_coboundary`) and computed in
  `python/finite_qm/use_cases/cochain.py` and `python/finite_qm/use_cases/foundations.py`.
  The cochain Python implementation uses floating-point HiGHS with tolerance
  $10^{-9}$; it does not certify exact zero or exact LP optimality. The cited
  Lean declarations prove algebraic identities, not correctness of that solver.
- **(ii) What is imported here, and named as an import?** A declared finite directed 2-complex
  (vertices, directed edges, oriented 2-cells) and positive edge weights $w_e > 0$.
- **(iii) What cannot be reached from below, and why?** Non-trivial 1-cohomology $H^1 \ne 0$ and
  circulation around holes cannot be reached from 0-cochain boundaries ($B^1 = \mathrm{im}(d_0)$).
  Coboundaries strictly vanish on cycles (`non_trivial_circulation_not_coboundary`).

#### Rung 3: Weights to Probabilities ($L^1 \to L^2$ & Born Normalization)

- **(i) What is derived here?** $L^1$ normalization of positive residual weights into probability
  distributions $p_i = w_i / \sum w_k$, ray invariance under positive scaling $w \mapsto c w$ ($c > 0$),
  rank-1 projector construction $P = |\psi\rangle\langle\psi|$ with idempotence $P^2 = P$ and
  self-adjointness $P^\dagger = P$, and the algebraic redundancy theorem showing that for any complete
  POVM partition of identity $\sum_k E_k = I$, the outcome probabilities satisfy
  $\sum_k \operatorname{Tr}(E_k \rho) = \operatorname{Tr}((\sum_k E_k)\rho) = \operatorname{Tr}(I \rho) = \operatorname{Tr}(\rho) = 1$.
  The general trace identity is the displayed linear-algebra argument.
  `lean4/BornNormalization.lean` mechanizes a two-level
  diagonal model with natural-number effect coefficients and scaled integer
  rank-one matrices (`born_normalization_redundancy`, `projector_self_adjoint`,
  `projector_trace`, `projector_idempotence_00`, `projector_idempotence_01`, `ray_invariance_sign_flip`)
  rather than arbitrary complex POVMs. Numerical examples are computed in
  `python/finite_qm/use_cases/foundations.py` (`born_normalization`, `verify_born_normalization_redundancy`,
  `weights_to_born_density`).
- **(ii) What is imported here, and named as an import?** The quadratic Born rule mapping state amplitudes
  to detection probabilities ($p_i = |\psi_i|^2$). It is imported as a declared postulate/contract;
  it is not derived from $L^1$ weights.
- **(iii) What cannot be reached from below, and why?** The $L^1$ simplex alone
  does not select the quadratic Born readout. A Gleason or Busch route adds
  explicit projection/effect-domain, positivity and additivity premises.
  Projective Gleason uniqueness fails in dimension two; stronger all-effects
  assumptions allow a different representation route even there. Neither route
  derives its operational domain from primitive difference.

#### Rung 4: Phase, Interference & Superposition as Quotient Fiber

- **(i) What follows under the declared complex carrier?** The $U(1)$ phase fiber $e^{i \theta}$, holonomy around closed cycles
  in the complex, and superposition as the fiber over the classical probability simplex. Standard
  projectivization is
  $\mathbb P(\mathcal H)=(\mathcal H\setminus\{0\})/\mathbb C^\times
  \cong S(\mathcal H)/U(1)$, where $S(\mathcal H)$ is the unit sphere. This is
  distinct from the group quotient $\mathbb C^\times/U(1)$, which retains only
  positive scale. The basis-dependent projection
  $[\psi] \mapsto (|\psi_i|^2 / \|\psi\|^2)_{i=1}^d \in \Delta^{d-1}$, whose fiber over an outcome distribution with $k$
  nonzero components is the torus $T^{k-1}$ parameterized by $k-1$ relative phases that govern interference capacity
  (the largest constructive cross term is $2 \sum_{j < k} |\psi_j| |\psi_k|$), real two-state interference with cross-term $2 c_0 c_1$, and
  Sorkin's [7] third-order term $I_3(A,B,C)=0$ for a quadratic readout;
  the second-order term can be nonzero. The torus description is the
  usual complex-coordinate argument: fix the nonzero moduli and quotient the
  $k$ independent phases by their common phase.
  `lean4/Superposition.lean` establishes integer two-state and
  integer polynomial identities (`superposition_not_basis`, `basis_state_zero_interference`,
  `superposition_positive_interference`, `beam_splitter_interference_expansion`,
  `sorkin_third_order_interference_vanishes`, `sorkin_second_order_interference`);
  it does not construct that complex torus. Numerical examples are computed in
  `python/finite_qm/use_cases/foundations.py` (`superposition_quotient_fiber`, `superposition_interference_test`,
  `two_path_interference`, `sorkin_3slit_parameter`).
- **(ii) What is imported here, and named as an import?** The complex numbers $\mathbb{C}$ and the
  circle group $U(1)$ as the phase fiber.
- **(iii) What cannot be reached from below, and why?** The continuous circle group $U(1)$ and phase
  interference are not supplied by the stated classical stochastic or $L^1$ transport alone. In pure $L^1$ cochain
  transport, probabilities add linearly without cross-terms, so the interference term
  $2\sqrt{p_1 p_2}\cos(\Delta \theta)$ is obstructed from below.

#### Rung 5: Composition, Entanglement & Non-Separability

- **(i) What follows under the declared tensor carrier?** The standard Schmidt
  decomposition characterizes pure-state entanglement by Schmidt rank greater
  than one. On the supplied carrier $\mathcal H_A\otimes\mathcal H_B$, we check
  the 2x2 Schmidt minor condition ($\Delta(\psi) = c_{00} c_{11} - c_{01} c_{10} = 0$ for all separable
  product states), and non-product certification of the Bell state
  $|\Phi^+\rangle=(|00\rangle+|11\rangle)/\sqrt2$ ($\Delta=1/2$;
  its unnormalized integer representative has $\Delta=1$),
  partial trace $\rho_A = \operatorname{Tr}_B(\rho_{AB})$, linear and von Neumann entanglement entropies,
  the non-signaling theorem under local operations on subsystem B
  ($\operatorname{Tr}_B((I_A \otimes U_B)\rho_{AB}(I_A \otimes U_B^\dagger)) = \operatorname{Tr}_B(\rho_{AB})$),
  and the Mermin–Peres contextuality parity obstruction. The partial-trace
  identity follows by cyclicity on the traced factor and $U_B^\dagger U_B=I$.
  Lean coverage is narrower: the parity argument is mechanized in
  `lean4/DualWitness.lean` (`mermin_peres_parity_obstruction`), `lean4/Entanglement.lean`
  uses integer $2\times2$ coefficients for the minor and establishes marginal
  invariance for a local bit flip and sign change
  (`product_state_minor_zero`, `bell_phi_plus_minor_non_zero`, `bell_state_is_entangled`,
  `non_signaling_under_local_b_flip`, `non_signaling_under_local_b_phase`) and computed in
  `python/finite_qm/use_cases/foundations.py` (`partial_trace`, `bipartite_linear_entropy`, `bipartite_von_neumann_entropy`,
  `bell_state`, `verify_non_signaling`, `is_entangled_pure_state`).
- **(ii) What is imported here, and named as an import?** The Hilbert space tensor product $\otimes$
  as the composition rule. The finite tests check
  bilinearity, local unitary covariance, product-state marginal consistency and
  no-signalling, and exclude one report-discarding rival. It does not prove
  uniqueness among all composites. A generation, local-tomography or minimality
  premise must exclude additional invisible sectors before such a classification.
- **(iii) What remains an additional premise?** A single-carrier cochain
  construction supplies no bipartite composition law. Under ordinary
  classical Cartesian composition every joint distribution is a mixture of
  point products (§11.33 above). Quantum tensor composition permits nonseparable
  states; the Mermin–Peres experiment excludes its specified noncontextual
  assignments. Contextuality by itself neither requires this tensor
  presentation nor selects complex quantum theory among all operational models.

#### Rung 6: Dynamics (Discrete Unitary Evolution)

- **(i) What is derived here?** Discrete unitary operators $U^\dagger U = I$, discrete state evolution
  $\psi(t+1) = U \psi(t)$ and $\rho(t+1) = U \rho(t) U^\dagger$, and conservation of $L^2$ state norm
  $\|\psi\|_2 = 1$. Computed in `python/finite_qm/use_cases/foundations.py`.
- **(ii) What is imported here, and named as an import?** The requirement of reversibility/unitarity
  and a discrete time step parameter.
- **(iii) What cannot be reached from below, and why?** Continuous time and self-adjoint Hamiltonian
  generators $H$ via Stone's theorem ($U(t) = \exp(-i H t)$) cannot be reached from discrete dynamics. Discrete toggles (e.g. Pauli X) have infinitely many matrix logarithms
  (branch ambiguities), so continuous time remains a declared hypothesis.

#### Rung 7: Measurement & Open Systems (Effects, POVMs, CPTP)

- **(i) What is derived here?** Positive Operator-Valued Measure (POVM) effects $E_m \ge 0$, $\sum E_m = I$,
  Born rule outcome probabilities $P(m) = \operatorname{Tr}(E_m \rho)$, Lüders state update and non-selective
  measurement decoherence $\rho \mapsto \sum M_m \rho M_m^\dagger$, and trace-norm contractivity under CPTP maps.
  These are consequences of the imported quantum definitions. The cited
  `FiniteDensity.lean` theorem `born_probability_in_unit_interval` establishes
  only the bound for a two-entry diagonal rational spectrum and binary
  diagonal projective effects; it is not a proof of general CPTP
  contractivity. `python/finite_qm/use_cases/foundations.py` supplies
  numerical examples; §§11.35–11.38 above give the exact finite checks.
- **(ii) What is imported here, and named as an import?** The POVM effect algebra and the definition of
  completely positive trace-preserving (CPTP) maps, defined via Choi positivity in the declared
  embedding and exact trace preservation. A chosen spectral Kraus construction
  can require square roots outside the base field; this is not a channel-wide
  obstruction. The native rational/Gaussian-rational LDL* construction can split
  positive rational pivots into four squares and enlarge the Kraus family
  without adjoining those square roots (see the channel census below).
- **(iii) What cannot be reached from below, and why?** Non-selective measurement/dephasing channels admit
  finite-dimensional Stinespring dilations (e.g. coupling to a single ancilla qubit via CNOT followed by
  partial trace), but selective projective collapse to a single measurement branch is non-unitary and
  irreversible. Unitary coupling and a discarded environment can produce the
  non-selective reduced channel, but do not select one realized branch.
  Conditional updating presupposes a recorded outcome; an account of its
  occurrence needs an additional stated premise: this is the unresolved
  quantum measurement problem.

#### Rung 8: The Boundary & Gleason's Theorem Obstruction

- **(i) What is derived here?** `GleasonTheorem.lean` formalizes integer quadratic
  frame identities and an odd-integer obstruction, not a general Gleason theorem.
  `GleasonRationalPlane.lean` now constructs a binary function on every nonzero
  rational two-vector, verifies invariance under nonzero rational rescaling and
  normalization on every orthogonal pair, and rules out a rational quadratic
  representation using four rays. `H054GleasonCyclotomicObstruction.lean` establishes
  the nine-context Cabello parity contradiction [2] and checks that a trace-one
  non-PSD matrix passes all 18 sampled ray bounds and nine frame sums.
  `H058EffectFrameBusch.lean` formalizes four-effect tomographic uniqueness
  and recovery on a supplied two-dimensional Hermitian coordinate space.
  Its rational-homogeneity result assumes an explicit homogeneity witness;
  its three-dimensional uniqueness result assumes the needed coordinate
  equations. The repaired three-dimensional effect predicate checks all
  principal minors, including the determinant. These declarations are not
  Busch's full positive representation theorem [3].
  The Rust `FrameSystem::density_state_of` now enforces that separation with
  the linear-algebra owner's exact inertia checker.
- **(ii) What is imported here, and named as an import?** The full Gleason theorem in dimension $d \ge 3$
  (showing that normalization and additivity across every orthonormal basis of the full real or complex Hilbert space force nonnegative frame functions to be quadratic Born
  valuations $f(v) = v^\dagger \rho v$) is a classical continuum theorem on complete projective geometries.
  Applying it to a restricted
  number-field ray domain requires an additional extension theorem; neither
  countability nor a finite test configuration demonstrates such an extension or
  the necessity of a continuum completion.
- **(iii) What cannot be reached from below, and why?** Continuous canonical observables $[X, P] = i\hbar I$
  cannot be reached in any finite dimension (trace obstruction: $\operatorname{Tr}([X, P]) = 0 \ne i\hbar d$).
  This is the finite-dimensional trace obstruction; Wintner–Wielandt is the
  stronger bounded-operator obstruction. Constructing an infinite-dimensional
  Hilbert completion additionally requires a directed family, inner products
  and a topology. None is supplied by a finite graph alone.

### 1.2 The 22 Foundational Targets (Loops 1 to 22)

To test the finite quantum mechanics programme against concrete physical and computational
structures, 22 Foundational Targets (organized across Loops 1 to 22) specify
finite models and examples. Their mathematical specifications, numerical
Python demonstrations, exact native checks and scoped Lean declarations are
different evidence. The list is not a certificate that every named target
or general theorem has been implemented. The declared algebraic carriers include the rationals $\mathbb{Q}$, Gaussian integers $\mathbb{Z}[i]$,
Eisenstein rationals $\mathbb{Q}(\zeta_3)$, cyclotomic rings $\mathbb{Z}[\zeta_5], \mathbb{Z}[\zeta_8], \mathbb{Z}[\zeta_{12}]$,
quadratic fields $\mathbb{Q}(\sqrt{3}), \mathbb{Q}(\sqrt{N})$, finite fields $\mathbb{F}_p$,
and cyclic groups $\mathbb{Z}/N\mathbb{Z}$.

#### Summary of Foundational Targets 1 to 12 (Loops 1 to 12)

Targets 1 through 12 collect finite algebraic models. The historical
`code_rs` label denotes the former native namespace; current reusable owners
are in `omega_engine/crates_rs`, with application dispatch under `native/`.
In particular, a name such as "pentagon" or "Gleason" does not enlarge the
statement actually checked:

- **Target 1 (Loop 1):** Primitive difference $D(x, y) = y - x$, zero self-difference certified (`python/finite_qm/domain/primitive_difference.py`, the historical Rust port, Lean 4 `H000`).
- **Target 2 (Loop 2):** Simplicial diamond 2-complex holonomy ring $\mathbb{Z}[\zeta_{12}]$ (`python/finite_qm/use_cases/simplicial_complex_qm.py`, `code_rs`, Lean 4 `H021`).
- **Target 3 (Loop 3):** Chain-cochain bilinear evaluation & vanishing Sorkin 3-path interference $I_3 \equiv 0$ (`python/finite_qm/use_cases/interference.py`, `code_rs`, Lean 4 `H010`).
- **Target 4 (Loop 4):** Exact rational Cayley transform flows over $\mathfrak{so}(8, \mathbb{Q})$ preserving $\mathrm{SO}(8, \mathbb{Q})$ isometries (`python/finite_qm/use_cases/advanced_targets.py`, `code_rs`, Lean 4 `H003`).
- **Target 5 (Loop 5):** Rational $S_3$ braid relations and finite recoupling-shaped models (`python/finite_qm/use_cases/advanced_targets.py`, `code_rs`, Lean 4 `H020`). No Biedenharn–Elliott or general associator pentagon theorem is established; source-notes supplement §11.52 records the corrected interpretation.
- **Target 6 (Loop 6):** Cabello 18-ray parity obstruction and exact positivity filtering. The published "glued transfer" was the identity with a PSD filter; it is not a derivation of positive quantum states from incidence data (source-notes supplement §11.52, C43/C49).
- **Target 7 (Loop 7):** Monotone layer signed permutation unitarity with irreversible non-exchangeable residue (`code_rs`, Lean 4 `H006`).
- **Target 8 (Loop 8):** Discrete Pythagorean Bell-CHSH nonlocality $S = 14/5 > 2$ via integer Pythagorean triples (`python/finite_qm/use_cases/quantum_protocols.py`, `code_rs`, Lean 4 `H032`).
- **Target 9 (Loop 9):** 3-qubit bit-flip quantum error correcting code $[[3, 1, 1]]$ with discrete syndrome recovery (`python/finite_qm/use_cases/stabilizer_codes.py`, `code_rs`, Lean 4 `H036`).
- **Target 10 (Loop 10):** Discrete quantum teleportation across 4 Bell measurement branches with fidelity $1/1$ (`python/finite_qm/use_cases/quantum_protocols.py`, `code_rs`, Lean 4 `H039`).
- **Target 11 (Loop 11):** Superdense coding protocol transmitting 2 classical bits via 1 entangled qubit with probability $1/1$ in $\mathbb{Z}[i]$ (`python/finite_qm/use_cases/quantum_protocols.py`, `code_rs`, Lean 4 `H040`).
- **Target 12 (Loop 12):** 4-qubit $[[4, 2, 2]]$ CSS surface code on a square plaquette with distance-2 error detection (`python/finite_qm/use_cases/stabilizer_codes.py`, `code_rs`, Lean 4 `H037`).

#### Detailed Mathematical Specifications for Targets 13 through 22 (Loops 13 to 22)

##### Target 13 (Loop 13): Prime-$p$ Discrete Wigner Phase Space ($p=5$)

- **Mathematical Specification & Operators:**
  On a discrete phase space $\mathbb{F}_p \times \mathbb{F}_p$ for an odd prime $p=5$, the finite Weyl-Heisenberg group [4] is generated by the cyclic coordinate shift operator $X |k\rangle = |k + 1 \pmod p\rangle$ and clock operator $Z |k\rangle = \omega^k |k\rangle$, where $\omega = \zeta_p = \exp(2\pi i / p)$.
  The parity reflection operator is defined on basis states by $P |k\rangle = |-k \pmod p\rangle$, which acts on integer coordinate vectors $(v_0, v_1, v_2, v_3, v_4)^T \in \mathbb{Z}^5$ via
  $$P (v_0, v_1, v_2, v_3, v_4)^T = (v_0, v_4, v_3, v_2, v_1)^T.$$
  Writing phase-space coordinates as $(q,r)$ to distinguish them from the
  prime dimension $p$, the symmetric Weyl displacement convention is
  $$D(q, r) = \omega^{2^{-1} q r \pmod p} X^q Z^r,$$
  where $2^{-1} \equiv \frac{p+1}{2} \equiv 3 \pmod 5$. The Gross discrete phase-point operators are constructed as displaced parity reflections:
  $$A(q, r) = D(q, r) P D(q, r)^\dagger.$$
  This positive displacement exponent matches $ZX=\omega XZ$; scalar phase
  changes in $D$ cancel in $A$. The discrete Wigner function for a state
  $\rho$ is then $W_\rho(q, r) = \frac{1}{p} \operatorname{Tr}(\rho A(q, r))$.
- **Discrete Carrier:**
  Exact cyclotomic field $\mathbb{Q}(\zeta_5)$ with minimal polynomial $\Phi_5(x) = x^4 + x^3 + x^2 + x + 1 = 0$, ring of integers $\mathbb{Z}[\zeta_5]$, discrete field $\mathbb{F}_5$, and coordinate lattice $\mathbb{Z}^5$.
- **Invariants & Algebraic Relations:**
  1. Involution: $P^2 = I_5$.
  2. Hermiticity: $A(u)^\dagger = A(u)$ for all $u = (q, r) \in \mathbb{F}_5 \times \mathbb{F}_5$.
  3. Trace normalization: $\operatorname{Tr}(A(u)) = 1$.
  4. Phase-point orthogonality: $\operatorname{Tr}(A(u) A(v)) = 5 \, \delta_{u, v}$.
  5. Completeness: $\sum_{u \in \mathbb{F}_5 \times \mathbb{F}_5} A(u) = 5 \, I_5$.
  6. Gross stabilizer covariance: $P X P = X^{-1}$ and $U_S A(u) U_S^\dagger = A(S u)$ for all $S \in \operatorname{Sp}(2, \mathbb{F}_5)$.
  7. Stabilizer non-negativity: the stabilizer eigenstates $|0\rangle$ and $|+\rangle = \frac{1}{\sqrt{5}} \sum_k |k\rangle$ satisfy $P |0\rangle = |0\rangle$ and $P |+\rangle = |+\rangle$, yielding non-negative Wigner values ($W_{|0\rangle}(0, 0) = 1/5 > 0$).
  8. Point negativity witness: the non-stabilizer vector $|M\rangle = (0, 1, 0, 0, -1)^T \in \mathbb{Z}^5$ satisfies $P|M\rangle=-|M\rangle$, yielding $\langle M|P|M\rangle=-2$. Its normalized projector $|M\rangle\langle M|/2$ has Wigner value $-1/5$ at the origin. The projector remains in the stated field even when a normalized vector requires an extension.
- **Cross-References:**
  - Python: `python/finite_qm/use_cases/advanced_targets.py` (`build_prime_p_phase_point_operators`, `evaluate_prime_p_discrete_wigner`, `verify_gross_stabilizer_covariance`). The phase-point builder and Fourier/shear covariance checks are floating-point diagnostics restricted to the paper's $p=3,5$ fixtures. Their measured residuals use the stated absolute tolerance $10^{-10}$ and are not exact algebraic certificates. The odd-prime algebraic construction is separate from this numerical replay.
  - Rust: `omega_quantum_physics::wigner` supplies exact phase-point operators, using `omega_lie_theory::heisenberg` and `omega_number_theory` cyclotomic scalars. These owners live in the external Rust workspace.
  - Lean 4: `lean4/H041PrimePWignerPhaseSpace.lean` establishes the integer five-coordinate parity, shift and displayed-vector identities (`parity_is_involution`, `magic_wigner_negativity_witness`, `gross_parity_covariance`). It does not formalize the full cyclotomic phase-point family or every symplectic covariance identity above.

##### Target 14 (Loop 14): Shor [[9, 1, 3]] Concatenated Quantum Error Correcting Code

- **Mathematical Specification & Operators:**
  The Shor code concatenates a 3-qubit phase-flip repetition code with an inner 3-qubit bit-flip code, encoding $k=1$ logical qubit into $n=9$ physical qubits.
  The code space is the $+1$ eigenspace of 8 independent commuting stabilizer generators:
  - Six local $Z$-type stabilizer checks, which detect bit-flip ($X$) errors:
    $$S_1 = Z_0 Z_1, \quad S_2 = Z_1 Z_2, \quad S_3 = Z_3 Z_4, \quad S_4 = Z_4 Z_5, \quad S_5 = Z_6 Z_7, \quad S_6 = Z_7 Z_8.$$
    For example, $\{Z_0 Z_1, X_0\} = 0$ while $[Z_0 Z_1, Z_0] = 0$.
  - Two global $X$-type stabilizer checks, which detect phase-flip ($Z$) errors:
    $$S_7 = X_0 X_1 X_2 X_3 X_4 X_5, \quad S_8 = X_3 X_4 X_5 X_6 X_7 X_8.$$
    For example, $\{S_7, Z_0\} = 0$ while $[S_7, X_0] = 0$.
  The logical operators are given by:
  $$X_L = \bigotimes_{j=0}^8 X_j \quad (\text{weight } 9), \qquad Z_L = Z_0 Z_3 Z_6 \quad (\text{weight } 3).$$
- **Discrete Carrier:**
  9-qubit tensor space $(\mathbb{C}^2)^{\otimes 9}$ restricted to exact integer Pauli matrices over $\mathbb{Z}$, binary syndrome space $\mathbb{F}_2^8$.
- **Invariants & Algebraic Relations:**
  1. Pairwise stabilizer commutation: $[S_i, S_j] = 0$ for all $i, j \in \{1, \dots, 8\}$.
  2. Logical-stabilizer commutation: $[X_L, S_i] = 0$ and $[Z_L, S_i] = 0$ for all $i$.
  3. Logical anticommutation: $\{X_L, Z_L\} = 0$ via symplectic inner product $(-1)^3 = -1$.
  4. Code distance $d = 3$: the minimum weight of an undetectable logical operator in $N(S) \setminus S$ is 3.
  5. Syndrome decoding completeness: all 27 single-qubit Pauli errors $\{X_i, Y_i, Z_i\}_{i=0}^8$ produce non-zero 8-bit syndrome vectors $s(E) \in \mathbb{F}_2^8$ with $s_j(E) = 0$ if $[E, S_j] = 0$ and $1$ if $\{E, S_j\} = 0$.
  6. Recovery fidelity: minimum-weight syndrome lookup yields exact recovery fidelity $F = 1.0$ across all 27 single-qubit error channels.
- **Cross-References:**
  - Python: `python/finite_qm/use_cases/advanced_targets.py` (`build_shor_nine_qubit_code`, `extract_shor_syndrome`, `decode_and_recover_shor`, `simulate_shor_error_recovery`, `verify_all_single_qubit_errors_recovery`).
  - Lean 4: `lean4/H042ShorNineQubitCode.lean` (`s1_s7_commute`, `xl_commutes_with_stabilizers`, `zl_commutes_with_stabilizers`, `logical_operators_anticommute`, `all_x_errors_detected`, `all_z_errors_detected`, `all_y_errors_detected`).

##### Target 15 (Loop 15): Discrete Quantum Phase Estimation over Cyclotomic Ring

- **Mathematical Specification & Operators:**
  Discrete Phase Estimation measures the eigenphase $\theta \in [0, 1)$ of a unitary operator $U$ satisfying $U |\psi\rangle = e^{2\pi i \theta} |\psi\rangle$.
  When $\theta$ is a dyadic rational $\theta = k / 2^m$ for $k \in \{0, \dots, 2^m - 1\}$, the register state before the inverse quantum Fourier transform is
  $$|\Psi_k\rangle = \frac{1}{\sqrt{2^m}} \sum_{l=0}^{2^m - 1} e^{2\pi i \theta l} |l\rangle = \frac{1}{\sqrt{2^m}} \sum_{l=0}^{2^m - 1} \zeta_{2^m}^{k l} |l\rangle.$$
  For $m=2$ ($M=4$ register levels), $\zeta_4 = i \in \mathbb{Z}[i]$. The unnormalized inverse discrete Fourier transform operator $F_4^\dagger$ has matrix entries:
  $$(F_4^\dagger)_{j, l} = (-i)^{j \cdot l} \in \mathbb{Z}[i].$$
  Applying $F_4^\dagger$ to $|\Psi_k\rangle$ yields the transformation:
  $$(F_4^\dagger |\Psi_k\rangle)_j = \frac{1}{\sqrt{4}} \sum_{l=0}^3 (-i)^{j l} i^{k l} = \frac{1}{2} \sum_{l=0}^3 i^{(k - j) l}.$$
- **Discrete Carrier:**
  Gaussian integers $\mathbb{Z}[i] = \mathbb{Z}[\zeta_4]$ with minimal polynomial $x^2 + 1 = 0$, dyadic rational field $\mathbb{Q}$, integer coordinate vectors $\mathbb{Z}^4$.
- **Invariants & Algebraic Relations:**
  1. Destructive interference: for all false bins $j \ne k \pmod 4$, the geometric series evaluates to
     $$\sum_{l=0}^3 i^{(k - j) l} = \frac{1 - i^{4(k - j)}}{1 - i^{k - j}} = \frac{1 - 1}{1 - i^{k - j}} = 0.$$
  2. Constructive reinforcement: for the true bin $j = k$, each term is $i^0 = 1$, yielding
     $$\sum_{l=0}^3 1 = 4.$$
  3. Deterministic projection: $\frac{1}{\sqrt{2^m}} F_4^\dagger |\Psi_k\rangle = |k\rangle$ (or unnormalized $F_4^\dagger |\Psi_k\rangle = 2 |k\rangle$), establishing exact dyadic phase extraction with zero phase leakage.
- **Cross-References:**
  - Python: `python/finite_qm/use_cases/advanced_targets.py` (`discrete_qft`, `discrete_phase_estimation`, `verify_cyclotomic_dyadic_projection`).
  - Lean 4: `lean4/H043DiscretePhaseEstimation.lean` (`phase_est_k0`, `prob_one_k0`, `zero_leakage_all_branches`, `geom_sum_4_cancellation`, `geom_sum_4_reinforcement`, `dyadic_qft_orthonormality_all_16_pairs`).

##### Target 16 (Loop 16): Surface Code Toric Topology & Anyon Defect Algebra

- **Mathematical Specification & Operators:**
  On a 2-dimensional periodic lattice representing the torus $T^2$ with $V=4$ vertices, $E=8$ edges, and $P=4$ plaquettes, Kitaev's toric code is defined by:
  - Star operators: $A_s = \prod_{e \in \operatorname{star}(s)} X_e$ for each vertex $s$.
  - Plaquette operators: $B_p = \prod_{e \in \partial p} Z_e$ for each face $p$.
  The lattice geometry satisfies the Euler characteristic relation:
  $$\chi = V - E + P = 4 - 8 + 4 = 0 \implies g = 1 - \chi / 2 = 1.$$
  The first homology group over $\mathbb{Z}_2$ has dimension $b_1 = \dim H_1(T^2, \mathbb{Z}_2) = 2$, encoding $k = b_1 = 2$ logical qubits into $n = 8$ physical edge qubits.
- **Discrete Carrier:**
  Cellular chain complex $C_2 \xrightarrow{\partial_2} C_1 \xrightarrow{\partial_1} C_0$ over $\mathbb{Z}_2$, integer Pauli group on 8 qubits, Abelian anyon defect algebra (mutual braiding phase $-1$).
- **Invariants & Algebraic Relations:**
  1. Star-plaquette commutation: each star and plaquette share an even number of edges ($|s \cap p| \in \{0, 2\}$), ensuring $[A_s, B_p] = 0$ via $(-1)^0 = (-1)^2 = +1$ across all 16 pairs.
  2. Ground state degeneracy: the number of independent checks is $(V - 1) + (P - 1) = 3 + 3 = 6$, leaving $8 - 6 = 2$ logical qubits and a 4-fold degenerate ground state space $\mathcal{H}_{\text{code}}$.
  3. Anyon defect pairs: an open $Z$-string creates two electric ($e$) defects at star endpoints ($A_s = -1$), while an open $X$-string creates two magnetic flux ($m$) defects at plaquette endpoints ($B_p = -1$).
  4. Abelian mutual braiding phase: a closed $e$-loop encircling a single $m$-defect intersects the dual $m$-string at an odd number of edges (exactly 1 edge in the minimal cell), resulting in the topological braiding phase factor $(-1)^1 = -1 = e^{i\pi}$.
- **Cross-References:**
  - Python: `python/finite_qm/use_cases/advanced_targets.py` (`build_toric_code_2x2`, `verify_toric_homology_and_degeneracy`, `evaluate_anyon_defect_algebra`, `simulate_anyon_braiding_phase`).
  - Lean 4: `lean4/H044SurfaceCodeToricTopology.lean` (`torus_euler_characteristic`, `torus_genus`, `homology_dimension_k2`, `all_star_plaq_commute`, `star_plaq_geometric_overlaps`, `anyon_loop_string_intersection`, `anyon_braiding_phase_pi`).

##### Target 17 (Loop 17): Discrete Grover Search via Householder Reflections

- **Mathematical Specification & Operators:**
  Discrete Grover search on an unstructured database of size $N=4$ operates in a 2-dimensional invariant subspace spanned by the marked target state $|\omega\rangle$ and the uniform superposition $|s\rangle = \frac{1}{\sqrt{N}} \sum_{x=0}^{N-1} |x\rangle$.
  The Grover iteration is $G = D R_\omega$, where:
  - Oracle reflection: $R_\omega = I - 2 |\omega\rangle\langle\omega|$.
  - Householder diffusion reflection: $D = 2 |s\rangle\langle s| - I$.
  Scaled by 2 to clear denominators, the diffusion operator is $\widetilde{D} = J_4 - 2 I_4$, where $J_4$ is the all-ones matrix.
  The initial overlap angle $\theta$ satisfies $\sin\theta = \frac{1}{\sqrt{N}} = \frac{1}{2}$, giving $\theta = \pi/6$ and Grover step rotation angle $2\theta = \pi/3$.
- **Discrete Carrier:**
  Quadratic ring $\mathbb{Z}[\sqrt{3}]$ with $(a + b\sqrt{3})$, rational field $\mathbb{Q}(\sqrt{N})$, and integer matrix ring $M_4(\mathbb{Z})$.
- **Invariants & Algebraic Relations:**
  1. Diffusion involution: $\widetilde{D}^2 = (J_4 - 2 I_4)^2 = J_4^2 - 4 J_4 + 4 I_4 = 4 J_4 - 4 J_4 + 4 I_4 = 4 I_4$.
  2. Exact 1-step target concentration: for initial state $|s\rangle = (1, 1, 1, 1)^T$ and target $|\omega\rangle = (1, 0, 0, 0)^T$, applying the oracle and scaled diffusion yields
     $$\widetilde{D} R_0 |s\rangle = (J_4 - 2 I_4) (-1, 1, 1, 1)^T = (4, 0, 0, 0)^T = 4 |\omega\rangle,$$
     recovering the target state with 100% fidelity in a single discrete step.
  3. Discrete Chebyshev recurrence: the target amplitude sequence $s_k = \sin((2k+1)\theta)$ satisfies the linear difference equation $s_{k+1} = s_k - s_{k-1}$ over $\mathbb{Z}[\sqrt{3}]$, producing the exact periodic sequence $(1/2, 1, 1/2, -1/2, -1, -1/2, \dots)$ with period 6.
- **Cross-References:**
  - Python: `python/finite_qm/use_cases/advanced_targets.py` (`discrete_grover_step`, `grover_exact_trigonometric_orbit`, `verify_grover_n4_exact_one_step`).
  - Lean 4: `lean4/H045DiscreteGroverSearch.lean` (`diffusion_squared`, `grover_one_step_exact`, `grover_target_isolation`, `rotation_to_target`, `grover_periodicity_six`).

##### Target 18 (Loop 18): Discrete Clifford Group Structure & Eastin-Knill Limit

- **Mathematical Specification & Operators:**
  The $n$-qubit Clifford group $C_n$ is the normalizer of the Pauli group $P_n$ in $\operatorname{U}(2^n)$. After dividing out all scalar phases, write $\overline C_n$ and $\overline P_n$ for the projective groups. The quotient $\overline C_n/\overline P_n$ is isomorphic to the finite symplectic group $\operatorname{Sp}(2n,\mathbb F_2)$ preserving the symplectic bilinear form
  $$\omega(u, v) = u_x v_z + u_z v_x \pmod 2.$$
  For a single qubit ($n=1$), $\operatorname{Sp}(2, \mathbb{F}_2) = \operatorname{SL}(2, \mathbb{F}_2)$, consisting of $2 \times 2$ binary matrices with determinant $1 \pmod 2$.
  The group is generated by the symplectic images of the Hadamard gate $H$ and Phase gate $S$:
  $$H = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \qquad S = \begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}.$$
- **Discrete Carrier:**
  Finite field $\mathbb{F}_2$, symplectic space $\mathbb{F}_2^2$, permutation group $S_3$.
- **Invariants & Algebraic Relations:**
  1. Symplectic group order formula:
     $$|\operatorname{Sp}(2n, \mathbb{F}_2)| = 2^{n^2} \prod_{j=1}^n (2^{2j} - 1) \implies |\operatorname{Sp}(2, \mathbb{F}_2)| = 2^1 (2^2 - 1) = 6.$$
  2. Isomorphism to $S_3$: the 6 matrices partition into:
     - Identity: $I$ (order 1).
     - Three order-2 involutions: $H, S, HSH$ (satisfying $M^2 = I$).
     - Two order-3 rotations: $SH, HS$ (satisfying $M^3 = I$).
  3. Symplectic invariance: $\omega(M u, M v) = \omega(u, v)$ for all $M \in \operatorname{Sp}(2, \mathbb{F}_2)$ and all $u, v \in \mathbb{F}_2^2$.
  4. Symplectic quotient closure and Eastin-Knill transversal restriction: the single-qubit projective Clifford group quotient $\mathcal{C}_1 / \mathcal{P}_1 \cong \operatorname{Sp}(2, \mathbb{F}_2)$ has finite order 6 (projective Clifford order 24), closed under multiplication. Their finiteness precludes a dense projective gate set generated by those elements alone.
     A separate imported theorem of Eastin and Knill [25] states that a quantum error-correcting code detecting arbitrary errors on any single physical subsystem, in the stated finite-dimensional setting, admits no transversal encoded gate set that generates a dense subgroup of the encoded unitary group. The finite group checks here do not prove that general theorem or classify every transversal encoded operation of an arbitrary code.
- **Cross-References:**
  - Python: `python/finite_qm/use_cases/advanced_targets.py` (`compute_symplectic_group_order`, `build_sp2_f2_generators_and_elements`, `verify_clifford_symplectic_isomorphism_n1`, `evaluate_eastin_knill_obstruction`).
  - Lean 4: `lean4/H046DiscreteCliffordSymplectic.lean` (`sp2_elements_cardinality`, `sp2_group_closure`, `canonical_pairing`, `symplectic_preservation_all_six`, `order_two_elements`, `order_three_elements`, `order_sp2_f2`, `order_sp4_f2`, `sp2_finite_symplectic_quotient_closure`, `eastin_knill_representation_obstruction`).

##### Target 19 (Loop 19): The Finite CCR Trace Obstruction and the Weyl Representation

- **Mathematical Specification & Operators:**
  In continuous quantum mechanics, the canonical commutation relation $[Q, P] = i \hbar I$ governs conjugate position and momentum observables.
  On a finite-dimensional carrier $\mathbb{C}^N$ (or cyclic coordinate space $\mathbb{Z}/N\mathbb{Z}$), the trace of any matrix commutator $[Q, P] = Q P - P Q$ satisfies the algebraic identity:
  $$\operatorname{Tr}([Q, P]) = \operatorname{Tr}(QP) - \operatorname{Tr}(PQ) = 0.$$
  Taking the trace of the canonical relation yields the obstruction:
  $$0 = \operatorname{Tr}([Q, P]) \ne \operatorname{Tr}(i \hbar I_N) = i \hbar N \quad (\text{for } N \ge 1, \hbar \ne 0).$$
  This trace argument excludes the additive canonical commutation relation
  in finite dimension over characteristic zero. It is not the Stone–von Neumann
  uniqueness theorem, and the obstruction concerns dimension rather than
  the cardinality of scalar coordinates.
  The finite presentation circumvents this obstruction via the discrete Weyl-Heisenberg shift $X$ and clock $Z$:
  $$X |k\rangle = |k + 1 \pmod N\rangle, \qquad Z |k\rangle = \omega^k |k\rangle, \quad \omega = e^{2\pi i / N},$$
  which satisfy the discrete Weyl commutation relation:
  $$Z X = \omega X Z \iff X^a Z^b = \omega^{-ab} Z^b X^a.$$
- **Discrete Carrier:**
  The cyclic label set is $\mathbb Z/N\mathbb Z$. The shift is integral, but
  the clock needs a scalar field containing a primitive $N$th root of unity,
  for example $\mathbb Q(\zeta_N)$ with its declared complex embedding.
  Unitary equivalence may require normalization scalars beyond that field.
- **Invariants & Algebraic Relations:**
  1. Vanishing trace identity: $\operatorname{Tr}([A, B]) = 0$ holds identically for all finite matrices over any commutative ring.
  2. Multiplicative Weyl relation: $[X,Z]=(1-\omega)XZ$ has trace zero
     since $\operatorname{Tr}(XZ)=0$ for $N\ge2$. This commutator is generally
     not central; it does not assert the additive CCR, which has no
     finite-dimensional solution (trace argument).
  3. Under a fixed nondegenerate multiplier (primitive $\omega$), the standard
     finite Stone–von Neumann theorem over $\mathbb C$ gives the irreducible
     representation up to unitary equivalence. Our exact construction has
     the more explicit supplied-seed premises below; it does not find or
     normalize an eigenvector over every input number field.
- **Cross-References:**
  - Python: `python/finite_qm/use_cases/advanced_targets.py` (`evaluate_finite_commutator_trace_obstruction`, `evaluate_discrete_weyl_commutation`, `stone_von_neumann_finite_cyclic_report`).
  - Rust: `native/src/campaigns/carrier.rs` (`carrier_finite_commutator_obstruction`); `commutator.rs` and `weyl.rs` are former `code_rs` labels.
  - Lean 4: `lean4/H047StoneVonNeumannObstruction.lean` (`tr_comm2_vanishes`, `tr_comm3_vanishes`, `tr_eye3_nonzero`, `finite_heisenberg_obstruction`, `discrete_weyl_commutation`).

**Constructive Weyl equivalence (written proof).** Let $K\subseteq\mathbb C$
be closed under conjugation and contain a primitive $N$th root $\omega$.
Supply unitary $N\times N$ matrices $X',Z'$ over $K$ satisfying
$Z'X'=\omega X'Z'$ and $(X')^N=I$, and a vector $v\in K^N$ with
$Z'v=v$ and $v^\dagger v=1$. Then the matrix with columns
$v,X'v,\ldots,(X')^{N-1}v$ is unitary and intertwines the pair with the
canonical shift and clock. Indeed these columns have norm one and are
$Z'$-eigenvectors with the distinct eigenvalues $1,\omega,\ldots,\omega^{N-1}$.
Unitary $Z'$ makes distinct eigenvectors orthogonal, and $(X')^N=I$ closes
the last shift column. These facts give both intertwining equations.
An operator commuting with the canonical clock is diagonal, because its
eigenvalues are distinct; commuting also with the shift makes that diagonal
constant. Two unitary intertwiners therefore differ only by a unit scalar.

The reusable implementation is
`omega_lie_theory::heisenberg::WeylHeisenberg::intertwiner_from_clock_seed`.
It checks the premises and both unitary/intertwining equations exactly;
its test `weyl_intertwiner.rs` (`omega_engine/crates_rs/tests/omega_lie_theory/` in
the repository) includes dimensions three and six and malformed
seed/period controls. `WeylCommutant.lean` establishes the dimension-independent
entrywise scalar-commutant lemma with distinct clock values and adjacent
diagonal equalities supplied. `H047` establishes integer trace identities at
dimensions two and three and an Eisenstein three-dimensional Weyl fixture.
Neither Lean module establishes the full classification of irreducible
representations or the existence of a normalized seed over arbitrary $K$.

##### Target 20 (Loop 20): Quantum Error Mitigation via Richardson Zero-Noise Extrapolation

- **Mathematical Specification & Operators:**
  Zero-Noise Extrapolation (ZNE) estimates an unmitigated expectation value $E_0 = \lim_{\lambda \to 0} E(\lambda)$ from measurements collected at amplified noise scales $\lambda_0 < \lambda_1 < \dots < \lambda_M$.
  Assuming a polynomial noise response model $E(\lambda) = E_0 + \sum_{k=1}^M c_k \lambda^k + \mathcal{O}(\lambda^{M+1})$, the Richardson estimator is
  $$\widehat{E}_0 = \sum_{j=0}^M \gamma_j E(\lambda_j).$$
  The extrapolation weights $\gamma \in \mathbb{Q}^{M+1}$ are determined by the exact Vandermonde linear system:
  $$\sum_{j=0}^M \gamma_j = 1, \qquad \sum_{j=0}^M \gamma_j \lambda_j^k = 0 \quad \text{for } k \in \{1, \dots, M\}.$$
  For uniform integer noise scale factors $\lambda_j = j + 1$:
  - Linear extrapolation ($M=1$, scales $\{1, 2\}$): $\gamma = (2, -1)$.
  - Quadratic extrapolation ($M=2$, scales $\{1, 2, 3\}$): $\gamma = (3, -3, 1)$.
  - Cubic extrapolation ($M=3$, scales $\{1, 2, 3, 4\}$): $\gamma = (4, -6, 4, -1)$.
- **Discrete Carrier:**
  Exact rational field $\mathbb{Q}$, integer weight vectors $\mathbb{Z}^{M+1}$, discrete noise scale lattice.
- **Invariants & Algebraic Relations:**
  1. Weight normalization: $\sum_{j=0}^M \gamma_j = 1$.
  2. Noise moment nullification: $\sum_{j=0}^M \gamma_j \lambda_j^k = 0$ for all $1 \le k \le M$.
  3. Exact reconstruction: for any noisy polynomial model of degree $\le M$, $\sum_{j=0}^M \gamma_j E(\lambda_j) = E_0$ identically without residual bias.
  4. Extrapolation coefficient 1-norm and variance overhead:
     $\|\gamma\|_1=2^{M+1}-1$ for these equally spaced scales, giving
     $3,7,15$. If independent sample means each have variance $v$, the
     estimator variance is $v\sum_j\gamma_j^2$, giving $5v,19v,69v$.
     If instead each shot has variance $\sigma^2$ and $N$ shots are shared
     optimally with continuous allocation $n_j\propto|\gamma_j|$, the
     minimum is $\sigma^2\|\gamma\|_1^2/N$, giving factors $9,49,225$
     relative to $\sigma^2/N$. Integer allocation and unequal per-scale
     variances require their own budget calculation.
- **Cross-References:**
  - Python: `python/finite_qm/use_cases/advanced_targets.py` (`compute_richardson_weights`, `richardson_zero_noise_extrapolate`, `simulate_mitigated_quantum_expectation`).
  - Lean 4: `lean4/H048RichardsonErrorMitigation.lean` (`linear_weight_sum`, `linear_moment1_cancelled`, `linear_variance_amplification`, `quadratic_weight_sum`, `quadratic_moment1_cancelled`, `quadratic_moment2_cancelled`, `quadratic_variance_amplification`, `cubic_weight_sum`, `cubic_moment1_cancelled`, `cubic_moment2_cancelled`, `cubic_moment3_cancelled`, `cubic_variance_amplification`, `richardson_cubic_exact_recovery`).

##### Target 21 (Loop 21): Discrete Quantum Walk on Permutation Group Cayley Graphs

- **Mathematical Specification & Operators:**
  A discrete-time quantum walk (DTQW) on a regular directed graph $G = (V, E)$ operates on the tensor space $\mathcal{H} = \mathcal{H}_{\text{coin}} \otimes \mathcal{H}_{\text{position}}$.
  The evolution operator per time step is $U = S (C \otimes I_V)$, where $C$ is a unitary coin operator (e.g. Hadamard or Grover diffusion) on $\mathcal{H}_{\text{coin}}$ and $S$ is the position shift operator $S |c, v\rangle = |c, v \cdot g_c\rangle$ determined by generator $g_c$.
  We evaluate Cayley graphs of finite symmetric groups generated by Coxeter generators (adjacent transpositions $s_i = (i, i+1)$):
  - $\operatorname{Cay}(S_3, \{s_1, s_2\})$: order $|S_3| = 6$, degree 2, diameter $D=3$.
  - $\operatorname{Cay}(S_4, \{s_1, s_2, s_3\})$: order $|S_4| = 24$, degree 3, diameter $D=6$.
- **Discrete Carrier:**
  Finite symmetric groups $S_3, S_4$, Coxeter generators, integer distance distributions, discrete graph coin-shift unitary algebra.
- **Invariants & Algebraic Relations:**
  1. Exact distance distribution / Poincaré polynomial:
     - For $S_3$, distance distribution from identity is $(1, 2, 2, 1)$, summing to $|S_3| = 6$, with diameter $D=3$.
     - For $S_4$, distance distribution is $(1, 3, 5, 6, 5, 3, 1)$, summing to $|S_4| = 24$, matching the Poincaré polynomial $P_{S_4}(q) = (1+q)(1+q+q^2)(1+q+q^2+q^3)$, with diameter $D=6$.
  2. Finite propagation: for a state initially at the identity, position support
     satisfies $d_{\text{front}}(t)\le\min(t,D)$. Equality requires a specified
     coin and initial coin state; with the identity coin and one occupied
     involutory generator, the walker returns at step two and the front is zero.
  3. The distance variance is bounded by $D^2/4$ at every time. The formal
     envelope $\min(t,D)$ alone does not prove ballistic spread of an evolved
     state. The cited $S_4$ module checks its actual walk only at steps 0, 1 and 2.
  4. For the declared $S_3$ fixture, nonzero amplitude reaches the longest word
     $w_0=s_1s_2s_1$ at step three; this is a fixture result, not a coin-independent law.
- **Cross-References:**
  - Python: `python/finite_qm/use_cases/advanced_targets.py` (`build_cayley_graph_s3`, `build_cayley_graph_s4`, `simulate_discrete_quantum_walk_cayley`, `evaluate_ballistic_propagation`).
  - Lean 4: `lean4/H049QuantumWalkSymmetricCayley.lean` (`s3_order`, `s3_diameter`, `s4_order`, `s4_diameter`, `s3_ballistic_t1`, `s3_ballistic_t3`, `dtqw_t3_ballistic_antipode_reached`, `s4_walk_ballistic_propagation`).

##### Target 22 (Loop 22): Discrete Mutually Unbiased Basis (MUB) State Tomography in Dimension $d=3$

- **Mathematical Specification & Operators:**
  In prime dimension $d=3$, there exist $d + 1 = 4$ mutually unbiased bases (MUBs) $\{B_0, B_1, B_2, B_3\}$, each consisting of $d=3$ orthonormal states, providing $d(d+1) = 12$ rank-1 projection operators $\Pi_{b, j} = |v_{b, j}\rangle\langle v_{b, j}|$:
  - $B_0$: Computational basis $\{|0\rangle, |1\rangle, |2\rangle\}$.
  - $B_1$: Discrete Fourier basis (eigenbasis of shift operator $X$).
  - $B_2$: Eigenbasis of $X Z$.
  - $B_3$: Eigenbasis of $X Z^2$.
  Within each basis, projectors are mutually orthogonal: $\operatorname{Tr}(\Pi_{b, j} \Pi_{b, k}) = \delta_{j, k}$.
  Across different bases, projectors have constant mutual overlap:
  $$\operatorname{Tr}(\Pi_{b, j} \Pi_{b', k}) = \frac{1}{d} = \frac{1}{3} \quad (\text{for } b \ne b').$$
  For any density operator $\rho \in M_3(\mathbb{C})$, measurement probabilities are $p_{b, j} = \operatorname{Tr}(\rho \Pi_{b, j})$.
  The density matrix is reconstructed via the exact rational linear inversion formula:
  $$\rho = \sum_{b=0}^3 \sum_{j=0}^2 p_{b, j} \Pi_{b, j} - I_3.$$
- **Discrete Carrier:**
  Eisenstein cyclotomic field $\mathbb{Q}(\zeta_3)$ (minimal polynomial $x^2 + x + 1 = 0$) embedded in $\mathbb{Q}(\zeta_{24})$, ring of integers $\mathbb{Z}[\zeta_3]$, exact rational arithmetic $\mathbb{Q}$.
- **Invariants & Algebraic Relations:**
  1. Orthonormality within basis: $\operatorname{Tr}(\Pi_{b, j} \Pi_{b, k}) = \delta_{j, k}$.
  2. Unbiasedness across bases: $\operatorname{Tr}(\Pi_{b, j} \Pi_{b', k}) = 1/3$ for $b \ne b'$.
  3. Projector resolution: $\sum_{j=0}^2 \Pi_{b, j} = I_3$ for each basis $b \in \{0, 1, 2, 3\}$.
  4. Total sum identity: $\sum_{b=0}^3 \sum_{j=0}^2 \Pi_{b, j} = 4 I_3 = (d+1) I_d$.
  5. Exact tomography inversion identity: for any state $\rho$, $\operatorname{Tr}\left(\left(\sum_{b, j} p_{b, j} \Pi_{b, j} - I_3\right) \Pi_{\beta, \mu}\right) = p_{\beta, \mu}$, establishing exact state recovery without information loss.
- **Cross-References:**
  - Python: `python/finite_qm/use_cases/advanced_targets.py` (`build_d3_mub_projectors`, `reconstruct_d3_state_from_mub_probabilities`, `simulate_mub_tomography`, `verify_mub_inversion_completeness`, an alias of `verify_mub_inversion_all_tested_states`).
  - Rust: `native/src/campaigns/carrier.rs` (`carrier_d3_mub_tomography`); `mub.rs`, `tomography.rs` and `cyclotomic.rs` are former `code_rs` labels.
  - Lean 4: `lean4/H050MubTomographyInversion.lean` (`mub_orthonormal_diag`, `mub_orthogonal_01`, `mub_orthogonal_02`, `mub_orthogonal_12`, `mub_cross_overlap`, `exact_inversion_b0_j0`, `mixed_state_inversion_all_bases`, `pure_state_0_inversion`).

##### Target 22 Extension: Galois Field $\mathbb{F}_4$ and 5 MUBs in Dimension $d=4$ (Positive-Reconstruction Obstruction)

- **Mathematical Specification & Operators:**
  In prime-power dimension $d = 2^2 = 4$ (two qubits), the maximal set of $d + 1 = 5$ mutually unbiased bases $\{B_0, B_1, B_2, B_3, B_4\}$ is constructed from the 5 maximal abelian subalgebras (MASAs) of the 2-qubit Pauli group $P_2 / Z(P_2)$, corresponding to the 5 isotropic lines of the symplectic spread in $\mathbb{F}_4 \times \mathbb{F}_4$:
  - MASA 0: $\{Z \otimes I, I \otimes Z, Z \otimes Z\}$ (computational basis)
  - MASA 1: $\{X \otimes I, I \otimes X, X \otimes X\}$ (Hadamard-dual basis)
  - MASA 2: $\{Y \otimes I, I \otimes Y, Y \otimes Y\}$ (phase basis)
  - MASA 3: $\{X \otimes Y, Y \otimes Z, Z \otimes X\}$ (entangled cyclic MASA A)
  - MASA 4: $\{X \otimes Z, Y \otimes X, Z \otimes Y\}$ (entangled cyclic MASA B)
  Each MASA yields 4 simultaneous orthogonal rank-1 projectors $\Pi(s_0, s_1) = \frac{1}{4}(I_4 + s_0 M_0)(I_4 + s_1 M_1)$ for $s_0, s_1 \in \{+1, -1\}$, providing 20 rank-1 projectors total.
  For any state $\rho$, the exact rational linear inversion formula reconstructs $\rho$:
  $$\rho = \sum_{b=0}^4 \sum_{j=0}^3 p_{b, j} \Pi_{b, j} - I_4.$$
- **Discrete Carrier:**
  Gaussian cyclotomic field $\mathbb{Q}(i) = \mathbb{Q}(\zeta_4)$ embedded in $\mathbb{Q}(\zeta_{24})$, ring of integers $\mathbb{Z}[i]$, Galois field $\mathbb{F}_4 \cong \mathbb{F}_2[x]/(x^2 + x + 1)$, and exact rational arithmetic $\mathbb{Q}$.
- **Invariants & Algebraic Relations:**
  1. Orthonormality within basis: $\operatorname{Tr}(\Pi_{b, j} \Pi_{b, k}) = \delta_{j, k}$ for all $b \in \{0, \dots, 4\}$.
  2. Unbiasedness across bases: $\operatorname{Tr}(\Pi_{b, j} \Pi_{b', k}) = 1/4$ for all $b \ne b'$.
  3. Total sum identity: $\sum_{b=0}^4 \sum_{j=0}^3 \Pi_{b, j} = 5 I_4 = (d+1) I_d$.
  4. Trace preservation: for any valuation or probability assignment, $\operatorname{Tr}(\rho) = \sum_{b=0}^4 (1) - 4 = 1$.
  5. Entangled state tomography: linear inversion reconstructs the entangled Bell state $|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$ with machine fidelity ($F = 1.000000$, error $< 2 \times 10^{-15}$).
  6. Valuation reconstruction obstruction: for any deterministic assignment
     $v\in\{0,1,2,3\}^5$ choosing one projector per basis, the linearly
     reconstructed trace-one operator has exact squared trace:
     $$\operatorname{Tr}(\rho(v)^2) = 5(1) + 20(1/4) - 2(5) + 4 = 4 > 1.$$
     Because physical density matrices satisfy $\operatorname{Tr}(\rho^2) \le (\operatorname{Tr}\rho)^2 = 1$, a purity of 4 algebraically forces at least one eigenvalue to be negative.
  7. Numerical demonstration: in floating point, all $4^5 = 1,024$ extreme vertices have $\lambda_{\min}(v) \le -1/2$ (minimum $\approx -0.8968$); the exact argument is item 6.
  8. For a complete set of $d+1$ MUBs the same calculation gives
     $\operatorname{Tr}(\rho(v)^2)=d$, hence excess $d-1$: one at $d=2$,
     two at $d=3$ and three at $d=4$. This excludes representing each
     deterministic assignment by a positive quantum state. It does not exclude
     a classical joint distribution for these separate basis measurements:
     $\mu(v)=\prod_b p_b(v_b)$ reproduces any declared basis marginals.
     A contextuality no-go needs additional shared-context or operational constraints.
- **Cross-References:**
  - Python: `python/finite_qm/use_cases/advanced_targets.py` (`build_d4_mub_projectors`, `reconstruct_d4_state_from_mub_probabilities`, `simulate_d4_mub_tomography`, `evaluate_d4_clifton_kent_deficit`).
  - Rust: former `code_rs` labels (`mub.rs` with `MubD4System`, `verify_orthonormality` and `verify_cross_basis_unbiasedness`; `lib.rs`). No `MubD4System` is in the current tree; `omega_quantum_physics::mub::MubSystem` has a method `verify_cross_basis_unbiasedness`.
  - Lean 4: `lean4/H051Mub4GaloisFieldContextuality.lean` (`mub4_orthonormal_diag`, `mub4_cross_overlap`, `total_projectors_d4`, `reconstructed_trace_is_one`, `valuation_purity_eval`, `mub4_non_psd_reconstruction_obstruction`, `clifton_kent_d4_purity_obstruction`, `five_mub_isotropic_lines_partition`).

## 9. Historical package map and evidence-record guidance

```text
omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/
├── finite_quantum_mechanics.md              the main paper (.tex and .pdf are built from it)
├── finite_quantum_mechanics_source_notes.md this supplement
├── finite_quantum_mechanics_change_log.md
├── finite_qm_guide_map.md
├── README.md                                the finite-qm wheel and its commands
├── verify_deposit.py                        manifest sweep and companion tests
├── sources/original_papers/                 67 original manuscripts cited in §4 (subsections 11.1–11.60)
├── docs/references.md                       bibliography with stable external links
├── python/finite_qm/                        commands and evidence orchestration
├── native/                                  the finite_qm_native Rust crate
├── tests/
│   ├── e2e/                                 package end-to-end checks
│   ├── oracles/                             independent reference computations
│   └── legacy/e2e/                          standalone deposit checks
└── research/                                selected mathematical derivations

omega_engine/crates_rs/omega_quantum_physics/  the exact implementation (described in §4 of this supplement), outside this deposit
lean4/quantum_mechanics/                       the programme's Lean workspace, outside this deposit
```

The public archive holds all 67 current original manuscripts under
`sources/original_papers/`. Every subsection 11.N of §4 links its corresponding
ZIP-local paper. Those links are the public
source index: a reader can move from a consolidated result directly to the
original manuscript in the same archive. The receipted Lean rows and retained
fixtures continue to cite the version against which they were actually checked.
Six historical package snapshots remain under repository custody but are not
part of the public ZIP. Repository tests check current originals and retained
copies separately and reject unrecorded changes.
Five retained copies differ from their historical disposition digests. The
2026-10-13 semantic reconciliation permits current claim use by assessing each pinned
version and binding its corrected downstream statements. It does not declare
the bytes identical or erase the historical disposition. In particular, the
new zero-centered dual proposed in the retained channel paper is rejected; the correct
spectral-diameter dual in §11.35 of this supplement remains in force. Source archives are preserved.
`tests/legacy/unit/test_retained_sources.py` binds the 37 superposition-paper
and 336 finite-Hilbert-boundary snapshot files to the earlier checked-in
catalog, without requiring equality to the evolving originals or silently
skipping an absent source.

For each unresolved mathematical statement:

1. state its domain, quantifiers, assumptions, and conclusion precisely;
2. supply an adequate written proof, a matching formal proof, or a complete
   exact finite argument appropriate to those quantifiers;
3. otherwise restrict the statement, identify it as open, or withdraw it; and
4. record any example test only as evidence about its stated inputs.

The repository-only evidence record tracks provenance and reproduction. Its
status transitions do not determine whether the mathematical obligation has
been discharged.

`tests/legacy/e2e/` contains the historical model-integration suite. Its old
execution counts describe their recorded revisions. The reference engines
consume the declared cochain packet directly, so an executable sequence exists.
The derivation problem remains open because the packet, scalar field, readout,
composition and physical interpretation still need justified bridges.

## 12. Synthesized Foundational Monograph: papers/foundations/theory_of_finite_quantum_foundations.md

The 43 individual discrete quantum foundation source packets (`QM_002` through `QM_212`), preserved historically in `sources/original_papers/`, have been systematically reviewed, audited, and synthesized into the dedicated monograph:
[`papers/foundations/theory_of_finite_quantum_foundations.md`](../foundations/theory_of_finite_quantum_foundations.md).

That document establishes the unified discrete obstruction calculus from primitive difference to quantum error correction:
- **§1 (Pre-Genesis, Primitive Difference & Coboundary)**: Synthesizes `QM_002`, `QM_003`, `QM_004`, `QM_005`, `QM_006`, `QM_008`, `QM_010`, `QM_012`. Formalizes $d_0$, the $\ell^1$ repair functional $\Phi_1([x])$, bipartite zero duality gap, even-cycle non-uniqueness, the 8-rung assumption ladder, and the 5 single-system countermodels ($M_{207}\text{--}M_{211}$).
- **§2 (Superposition, Sorkin $I_3 = 0$ & $U(1)$ Phase Selection)**: Synthesizes `QM_060`, `QM_061`, `QM_062`, `QM_063`. Formalizes quotient fibers, double-slit cross terms $2ab \ne 0$, Sorkin $I_3 = 0$ degree-4 selection, and the elliptic division involution $i^2 = -1$.
- **§3 (Born Normalization, Hilbert Lifts & POVM Audits)**: Synthesizes `QM_011`, `QM_020`, `QM_021`. Establishes diagonal $\ell^1$ weight sufficiency, rank-1 Hilbert lift redundancy, rational Gleason elimination on $S^2(\mathbb{Q})$, Busch IC-POVM state reconstruction, and the polyhedral cone gap.
- **§4 (Reversible Dynamics, Cayley Stepping & Feynman Path Sums)**: Synthesizes `QM_030`, `QM_031`, `QM_032`, `QM_033`, `QM_034`, `QM_035`, `QM_040`, `QM_041`, `QM_043`. Proves the finite Wintner-Wielandt trace obstruction $[X,P] \ne i\hbar I$, the Schwinger-Weyl clock-shift intertwiner, exact unitary Cayley stepping, and graded path sums.
- **§5 (Non-Factorization, Entanglement & Contextuality)**: Synthesizes `QM_070`, `QM_071`, `QM_072`, `QM_073`, `QM_120`. Demonstrates bipartite correlation tensor separability failure, rational Bell violation ($S=14/5$), cyclotomic Tsirelson bound ($S=2\sqrt{2}$ in $\mathbb{Q}(\zeta_8)$), and Mermin-Peres $\mathbb{F}_2$ Čech contextuality.
- **§6 (CPTP Channels, Trace Norm Geometry & Dual Witnesses)**: Synthesizes `QM_080`, `QM_081`, `QM_082`. Formulates CPTP channels as stochastic kernel lifts with trace-norm contractions and exact dual certificates.
- **§7 (Interpretations as Authority Shadows & Modal Realism Refusal)**: Synthesizes `QM_090`, `QM_091`, `QM_093`, `QM_094`, `QM_095`. Refuses modal realism and establishes interpretation indistinguishability on finite packets.
- **§8 (Asymptotics, Repair Capacity & Parity Schedules)**: Synthesizes `QM_101`, `QM_102`, `QM_103`, `QM_122`, `QM_212`. Formalizes quantum error-correcting code thresholds as cochain repair capacities and analyzes Majorana measurement-only parity schedules obeying non-Abelian Ising fusion.
- **§9 (Foundational Claim Ledger & Verification Index)**: Indexes claims `002:C1` through `212:C1` with their exact Lean 4 theorems and verification tests.

## 13. Master Derivation Ledger: papers/core/master_derivation_ledger.md

Every individual derivation step in the Theory of Finite Quantum Mechanics—from the bare, inert literal inscription `<>` (`TFQ-0000`) through primitive difference, discrete cochain repair, algebraic Hilbert lifts, Cayley dynamics, entanglement, gauge theory, QED, electroweak, QCD, topological phases, to quantum gravity constraints (`TFQ-0111`), the continuum interface (`TFQ-0124`), and all application branches (`TFQ-0397` through `TFQ-0416`)—is indexed without omission in the companion master ledger:
- [`papers/core/master_derivation_ledger.md`](./master_derivation_ledger.md)
- [`dag/derivations/MASTER_DERIVATION_LEDGER.md`](../../dag/derivations/MASTER_DERIVATION_LEDGER.md)

Each derivation in the ledger links 1-to-1 to its standalone Markdown paper in `dag/derivations/` and documents its direct DAG parent, epistemic status, mathematical statement, governing obligation, and multi-tier proof witnesses in Lean 4, Rust, and Python.

## References

Numbered references in square brackets match the bibliography of the master paper and `docs/references.md`; some entries are cited only in the main paper.

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
13. J. H. Carroll, *Trace-Zero Repair Quotients on a Finite Graph: An Exact Qutrit Counterexample and the Correct Scalar-Divergence Dual*, Version 0.55.0 (2026). Local companion address: `companion_papers/trace_zero_quotient_duality_monograph.md`.
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
26. *Native joint operations and a Genesis-to-Bell experiment*, The Symbol Game repository, revision `4a4fd192f` (2026); included in the code-companion archive as `omega_engine/crates_rs/omega_wdp/docs/genesis_bell_experiment.md`.
27. A. Baker, “Linear Forms in the Logarithms of Algebraic Numbers (I),” *Mathematika* **13**, 204–216 (1966).
