# Change Log — PO-000: Projection Obstruction Anchor

**Paper:** `PO-000`
**Canonical manuscript/release version:** `v6.9.18`
**Python code version:** `6.9.6`
**Legacy filename:** `000_projection_obstruction_v5_6.md`
**Status:** Canonical repository changelog
**Date:** 2026-10-14

## v6.9.18 modular monograph streamlining (2026-10-14)

- Decomposed and streamlined the manuscript from 4,606 to 3,398 lines, focusing on
  physical quantum lattice dynamics (§§5–6) and the Local Green / Global Red
  visibility gap (§7.4 and Theorem 7.12).
- Decoupled abstract Banach chart catalogs to PO-006, classical field contractions to
  PO-001, continuous-time enclosures to PO-033, and Jordan–Lie quantum reconstructions
  to Finite QM (§13.8) and PO-035.
- Maintained exact constant derivations in Appendix B and sibling cross-references in
  Appendix C; full 1058-test suite, replay receipts, and standalone deposit verified.

## v6.9.18 publication-facing claim audit (2026-10-13)

- Publication-facing claim audit corrects the Hermitian trace-zero derivative
  domain, the unbounded-generator split formulas and the Example 3.14 image
  domain. It separates the sharp derivative norm 2 from the residual bound 3,
  requires retained cohomology when curvature is insufficient, and corrects
  commuting perturbation, Lindblad-rate and Strang-order statements.
- Clarified uniform incident summability, support-order versus time-derivative
  conditioning, the weighted K-cut scope and degree-regular minimax proof.
  Removed unsupported blanket PO-D1–PO-D20 certificate coverage and stale
  certification claims in active ledgers; selected numerical results remain
  distinct from written proofs.

## v6.9.17 adversarial corrections (2026-10-13)

- Defined six internal Paper components within the single publication.
- Restored the model-residual term in total predictive error; capped the trace
  pairing using two independent bounds, without a false conditional-expectation
  residual cap. Sampled Duhamel output is explicitly non-certifying.
- Corrected graph-state Heisenberg and computational-basis phases, the ring
  minimax summary, and the claimed strictness of cluster merging.
- Kept graph-domain derivatives separate from ambient Banach derivatives and
  narrowed the Lean claim to its actual selected declarations.
- Repaired native adapter discovery and bound replay identities to the current
  release record. Current software version is 6.9.6.
- Marked thresholded tangent-cone and SLSQP outputs as numerical candidates;
  explicit certification requests refuse. Exact written witnesses remain
  separate from unverified numerical polar candidates.
- Regenerate and independently check both checksum manifests. A stale inner
  manifest is rejected even if its outer checksum is recomputed.
- Historical tests and archives below retain their original scope. The prior
  eight-site “honeycomb” fixture is a hexagon with a square and uses numerical
  evolution, not a validated continuous-time enclosure.

## v6.9.16 observer and Bell bridge revision (2026-10-13)

- Retained the v6.9.15 marginal/cochain correction and added an exact separable
  control distinguishing marginal consistency from product independence.
- Added §7.10: native protected futures, joint report refinement, and the
  distinction between report loss, support gluing and positive Bell extension.
- Kept the quantum CHSH 14/5 and setting-dependent native CHSH 12/5 examples
  separate, with explicit preparation and locality premises.
- Added Appendix E's premise table and scoped Weyl/Gleason and central-sector
  cross-references. No new Lean scope, operational reconstruction or deposit.
- Manuscript/release version 6.9.16; unchanged Python code version 6.9.5.

## v6.9.15 research revision (2026-10-13)

- **Edge-Decomposed TDVP Duhamel Master Theorem (Theorem 5.10.A / §5.10.2):** Formulated and proved
  the general master theorem for projected product trajectories under time-dependent variational
  principles (TDVP). Proved that equation residuals vanish identically on 1-local Hamiltonian terms
  and decompose into centered 2-site edge normal contributions $R(s) = \sum_{e\in E} n_e(s)\otimes\widetilde{\rho}_{V\setminus e}(s)$
  satisfying $\operatorname{Tr}_u n_e = \operatorname{Tr}_w n_e = 0$. Wrote out the explicit local conditional
  expectation subtraction $\mathbb{E}_{V\setminus e}(\tau_\tau(O))\otimes I_e$ and established the weighted
  edgewise convolution bound $|\langle O\rangle_\rho - \langle O\rangle_{\widetilde{\rho}}| \le \|O\|_\infty \|\delta\rho_0\|_1 + \sum_{e\in E} \int_0^t w_{O,e}(t-s)\nu_e(s)\,ds$
  with Lieb--Robinson weights $w_{O,e}(\tau) \le \min(\|O\|_\infty, C_0 \|O\|_\infty e^{v_{\mathrm{LR}}\tau - \mu d(e, X)})$.
- **Integration Test Suite (`code/tests/test_honeycomb_tdvp_duhamel_integration.py`):** Implemented and verified
  against exact Krylov subspace time evolution (`scipy.sparse.linalg.expm_multiply`) on an 8-qubit 2D
  honeycomb lattice cluster ($z=3$ coordination at bulk shared bond). Validated strict enclosure of
  two-body bond correlator expectation error $|\langle Z_2 Z_3\rangle_{\mathrm{exact}} - \langle Z_2 Z_3\rangle_{\mathrm{MF}}|$
  along the TDVP trajectory, and verified exponential spatial decay of influence weights for boundary
  observable $Z_0$ across graph distances.
- **Cut-Edge Pythagorean Cluster Rate Law (Theorem 5.10.B & Remark 5.10.B.1 / §5.10.3):** Proved that for any
  cluster partition $\mathcal{C} = \{V_1, \dots, V_K\}$ and fully site-factorized pure state
  $m = \bigotimes_{v\in V} \lvert u_v\rangle\langle u_v\rvert \in \mathcal{M} \subseteq \mathcal{M}_{\mathcal{C}}$,
  the global cluster normal leakage satisfies $\nu_{\mathrm{global},\mathcal{C}}^2(m) = \sum_{e\in E_{\mathrm{cut}}(\mathcal{C})} \nu_e^2(m)$,
  establishing the exact Min-Cut criterion at site-factorized states. Added Remark 5.10.B.1 giving the explicit
  4-qubit Bell-pair counterexample ($\chi_{e_1}=\chi_{e_2}=\lvert\Phi^-\rangle_{12}\otimes\lvert\Phi^-\rangle_{34}$,
  $\nu_{\mathrm{global},\mathcal{C}}^2 = 16 \ne 8$ or $0 \ne 8$) when intra-cluster entanglement is present across multiple cut edges.
- **Quantum Partial-Trace Poset Cochain Adapter (Theorem 4.3.A / §4.3.2):** Formalized the quantum
  marginal Banach diagram over the site-subset inclusion poset $(\mathcal{P}(V), \subseteq)$ with
  contractive partial-trace maps $r_{B,A} = \operatorname{Tr}_{B\setminus A}$, showing that $d_0 s_{\mathrm{true}}=0$
  and $d_0 s_{\mathrm{prod}}=0$, explaining why a single 0-cochain cannot simultaneously assign $s(B)=\rho_B$
  and $s(A)=\bigotimes_{v\in A}\rho_v$, and formulating $D_A(\rho_V) = \lVert(s_{\mathrm{true}}-s_{\mathrm{prod}})(A)\rVert_1$
  and the induced two-site 1-cochain $\omega_e(\rho_V) = (I-\Pi_e)(\rho_e)$.
- **Higher-Degree Graph-State Minimax Theorem (Theorem 7.12 / §7.8):** Renumbered from 7.11 to avoid collision
  with Corollary 7.11 and generalized cycle-graph results to finite simple graphs of minimum degree $d_{\min} \ge 2$.
  Proved complete edge marginal blindness ($\rho_{uv}(t_*) = I_4/4$) for girth $\ge 4$ and all-pair blindness for
  girth $\ge 5$. Accounted for degree-parity stabilizers ($O_v = X_v$ for even $d_v$, $O_v = Y_v$ for odd $d_v$),
  distinguished the relaxed-box polynomial root $r_d$ ($r_d^{d+1}+r_d-1=0$) from the exact Bloch-disk quantum
  minimax $r_d^{\mathrm{Q}} = \min_{x,z\in[0,1],\,x^2+z^2\le 1}\max\{1 - x z^d, x, z\}$
  ($r_d^{\mathrm{Q}}=r_d$ for $d\in\{1,2\}$, $r_d^{\mathrm{Q}}>r_d$ strictly for $d\ge 3$), and bounded the
  joint Pauli measurement settings by $M_{\mathrm{settings}} \le \chi(G^2)+1 \le \Delta(G)^2+2$.
- **Exact Finite Witnesses (`PO-D1`–`PO-D20` / §7.9) & Manuscript Presentation Overhaul:**
  - Added §7.9 summarizing `PO-D1`–`PO-D20` (exact rational $\ell^1$ quotient LP solvers on $\Delta^4$, $K_\Pi=3$
    tightness, $J_2$ Ising perturbation, girth-4 $C_4$ plaquette curvature, Lindbladian dephasing/damping envelopes,
    Strang–Trotter discretization error, and $K$-patch visibility scaling).
  - Replaced the §5.17 $W_6/\mathrm{GHZ}_6$ paragraph with the exact opposite-parity 6-qubit GHZ family
    $\lvert\mathrm{GHZ}_6^\pm\rangle$, whose proper marginals ($1\le |A|\le 5$) coincide identically while
    $\lVert\kappa_6(\rho_+)-\kappa_6(\rho_-)\rVert_1 = 2$.
  - Relocated Lemmas 3.4–3.14 and Examples 3.4–3.14 to Appendix A, added the explicit Heisenberg dissipator
    commutator identity in §5.4.1, and stripped internal audit scaffolding and house jargon from the manuscript prose.

## 2026-10-11: post-merge artifact custody correction

The current main-branch integrity check found ten stale checksum entries for
five Python modules and their five regression files. Their source bytes were
unchanged from the reviewed research branch. The manifest and deterministic
archive are regenerated against the actual tree after focused regression checks.
The E.6/E.7 statements, assumptions, Lean sources and manuscript are unchanged.
This is an artifact repair within the existing 6.9.14 candidate, not a new
mathematical result, full-profile certification, or external publication.

## v6.9.14 research revision (2026-10-11)

- Added Proposition E.6: construct the positive invariant multiplication-trace
  form from supplied real spectral decompositions and Jordan--Lie identities.
  The scoped Lean proof has nine axiom reports using only standard axioms.
- Added Proposition E.7: sharp central-weight ceiling on extension purity and
  trace-distance obstruction to pure-composite marginals, with ancilla scope.
- Corrected real purification, quaternion associativity, Albert verification
  scope and sector-changing channels. Exact fixtures reject floats and booleans.
- Separated imported classification facts, written proofs and finite checks.
  No primitive-to-QM reconstruction or external deposit is claimed.
- Decoupled the exploratory zero-container relational spacetime, emergent Lorentz causality,
  and Regge holonomy research program into dedicated standalone paper package
  `zero_container_relational_spacetime_and_witness_holonomy`.
- Restored `projection_obstruction.md` strictly to its core mathematical physics scope:
  short-time projection obstruction, boundary tangent-cone geometry, and Lieb-Robinson
  Duhamel prediction bounds.
- Excised Section 8 and claims V70-V73 from `projection_obstruction.md`, claim ledgers,
  and verification harnesses, ensuring zero category smuggling and strict adherence
  to claim hygiene.

## v6.9.13 release revision (2026-10-10)

- Declared separate manuscript/release 6.9.13 and Python 6.9.4 identities.
- Scoped the future-observer criterion uniformly over the full lifted carrier;
  recorded the difference-set criterion for restricted admitted states.
- Separated standalone tests from optional native integration and renamed the
  lexical Lean check to `--lean-source-scan`. It does not compile Lean.
- Rebuilt the manuscript artifacts and qualified the exact selected archive.
  See `docs/publication_revision.md` for executed checks and remaining limits.
  No claim status promotion or external deposit is made.

## PR #673 review repair (2026-10-10) — numerical diagnostics

- Add explicit quartic-crossover status; unresolved cancellation returns no
  ratio, with `NaN` in the legacy tuple API, rather than infinite validity.
- Replay the review's zero-quartic example across three Hamiltonian scales
  and the Markovian local-noise concurrence counterexample.
- Correct residual theorem numbering and bulk-penetration test descriptions.
- Replaced the sampled quadrature's bound claim with a distinct estimate and
  conservative interaction-norm envelope; numerical certification remains false.
- Replaced fixed-window fitting with sparse fourth-order Taylor jets.
- Normalize both evolution inputs; refuse zero or malformed site vectors.
- Declare SciPy for clean installs and add reviewer regression cases.
- Scope the supplementary modules as finite numerical artifacts. No numbered
  theorem, manuscript proof, general mixed-state slope or release status is added.
- Validation receipts are revision-specific. Test and archive checks do not
  certify general analytic claims or numerical error bounds.

## v6.9.4 (2026-10-09) — constant-shear graph chart derivative

- Proved Lemma 3.5: if \(g(e,n)=e+L(n-f(e))\) for a constant bounded
  \(L:F\to E\) and \(\Pi=m\circ g\), then \(\Pi\) is a \(C^2\) retraction onto
  the graph and \(b(u)=Q(u)\alpha(u)+L\beta(u)\) with
  \(Q(u)=I_E-L\circ Df(u)\). The case \(L=0\) is Lemma 3.4. Theorem 3.1
  excludes affine-linearity when \(Db\) is nonconstant.
- Recorded Example 3.5: on \(y=x^2\) with \(A(x,y)=(-x,0)\) and unit shear,
  \(Db(0)=-1\) and \(Db(1)=3\). The vertical retraction on the same data has
  constant \(Db\). Thus moving the chart coordinate can create chart
  nonlinearity that the vertical formula does not see.
- Left S1 open for a fiber displacement that depends nonlinearly on the
  base point, and for a submanifold not presented as a graph. Example 3.3
  stays inside Lemma 3.3. Proposition 3.C still refutes unqualified C4.
  No new Lean proof. The rendered PDF was not rebuilt.

## v6.9.3 (2026-10-09) — vertical graph chart derivative

- Proved Lemma 3.4: on a vertical retraction onto a $C^2$ graph of a fixed
  splitting, the chart field is $b(u)=P_E A m(u)$ and
  $Db(u_1)-Db(u_0)=P_E A(Df(u_1)-Df(u_0))$. Theorem 3.1 then excludes
  affine-linearity when that difference is nonzero. If $P_E A$ vanishes on
  $F$, the chart derivative does not depend on $f$.
- Recorded Example 3.4: $f(s)=s^2$ and $A(x,y)=(-x-y,-y)$ generate a
  Euclidean contraction semigroup, with $Db(0)=-1$ and $Db(1)=-3$. The same
  identity recovers Proposition 3.C when $P_E A|_F=0$.
- Left S1 open for a retraction that moves the chart coordinate and for a
  submanifold not presented as a graph. The unqualified C4 implication
  remains false by Proposition 3.C. Theorem 5.1 does not use the bridge.
  No new Lean proof. The rendered PDF was not rebuilt.

## v6.9.2 (2026-10-09) — affine-subspace chart transfer

- Proved Lemma 3.3: if the retracted manifold is relatively open in a closed
  affine subspace and the chart is the restriction of an ambient affine
  isomorphism, then nonconstancy of the tangent-restricted ambient derivative
  is equivalent to nonconstancy of the coordinate derivative. The chain rule
  has no chart-variation term under those hypotheses. Theorem 3.1 then
  excludes affine-linearity of the coordinate field.
- Recorded Remark 3.3.1: the unrestricted ambient derivative can depend on
  base point through normal directions while the chart derivative stays
  constant. The lemma compares only the tangent restriction.
- Gave Example 3.3, a Euclidean contraction generator on the x-axis whose
  chart derivative takes the distinct values -1 and 1, with a nonzero
  projection-curvature term. The flat hypothesis is not vacuous.
- Proved Proposition 3.C: the graph retraction onto y = x^2, with generator
  A(x, y) = (-x, 0), has nonconstant ambient derivative and nonzero
  projection curvature, while the declared chart field is b(s) = -s. Claim
  C4, read without the flat hypotheses, is false.
- Left S1 open off affine subspaces. No noncancellation estimate is proved
  when the second fundamental form is nonzero. Theorem 5.1 does not use
  the bridge. No new Lean proof and no external deposit.

## v6.9.1 (2026-10-08) — finite certificate integration and proof scope

- Added separate aggregate measurement certificates for the Ising five-cycle,
  a three-factor contract and a separable correlated state. Native functional
  evaluation supplies corrected moments, the witnessed exact quotient and
  the error-adjusted product-distance bound; independent replay binds the
  declared input and checks the mathematical consequence.
- Added the Proposition 5.20 local-zero checker: exact operator basis,
  identity, independence, local invariance, every declared crossing term,
  state, polynomial and cyclic annihilator. Changing the boundary invalidates
  the certificate even when the first jet still vanishes.
- Upgraded aggregate schema to v4 while preserving the general theorem
  refusals. Missing native or symbolic capabilities remain explicit refusals.
  Laboratory error coverage and Hamiltonian completeness remain premises.
- Added the active per-result hypothesis/dependency inventory without
  altering the historical ledgers. Added the two-module E.1 Lean build for
  the algebraic bridge, closed C*-image and positive-cone identification
  from the complexified B1 identities. The real-to-complex input construction,
  block classification and selector remain written proofs.
- Corrected the external-source screen and planning bridges: expansion gives
  detectability, licensed representative changes preserve the quotient, and
  witnessed choice needs a declared output equivalence and recorded costs.
  The proposed evidence-revision/self-maintenance derivation is not started.

## v6.9 (2026-10-08) — conditional Jordan–Lie quantum selection

- Replaced Appendix E's sketch with explicit base axioms B1–B4 and written
  proofs of associative complexification, positivity, finite matrix blocks,
  standard composites and corners, and the complete three-family
  classification under tensor/compression closure.
- Established pure-state purification as a selector for the sector-free
  complex quantum theory within this base, with classical and superselected
  deletion countermodels. Continuous reversible pure-state transitivity is
  equivalent in the same class.
- Derived the Born pairing and all effects, channels and instruments, with
  the full-process assumption stated. Purification uniqueness follows for
  equal ancillary dimensions; unequal dimensions require an isometry or
  an explicit enlargement.
- Stated the explanatory cost: the Jordan–Lie compatibility identity,
  positive form, dynamical composition, compression and process assumptions
  are added axioms, not consequences of finite records or obstruction norms.
  No general-GPT or minimal-axiom claim is made.
- Added exact Pauli, classical-bit, superselection, purification, compression
  and Choi/Kraus checks. Added explicit aggregate refusals for the general
  algebra/classification and selector theorem groups; no new Lean proof.
- Preserved the owner's post-review import annotation in the onset test.
- Synchronized the v6.9 manuscript, README, quick start, replay/verifier
  metadata, running PDF header, rendered artifacts and manifest.
  This remains an author-review revision, not an external publication.

## v6.8 (2026-10-08) — physical adapter and sharp onset derivations

- Added §7.8: a declared cycle-gradient repair complex, local Pauli adapter,
  exact quotient/observer kernel calculation, and noisy lower bound on
  distance from product states. The homogeneous Ising ring has a uniform
  quadratic onset window and a positive quotient at a pair-blind graph-state
  time. At most four product basis settings suffice; shot count is not constant.
- Added §5.17: finite algebraic onset strata, a constructive nonzero coefficient
  for every incidence-qubit tree, exact delay/cancellation examples, a scoped
  symmetry test, a boundary-checked local zero certificate, and a measurement
  protocol with explicit coefficient-estimation error.
- Resolved S11--S12 only for the declared ring quotient. Arbitrary physical
  adapters, unrestricted qubit-tree sharpness, and decision authorization
  remain outside these results. The ring diagnostic is not an entanglement
  witness or a claim of priority over graph-state stabilizer methods.
- Added Appendix E as a classification target and proof-obligation sketch
  only. No selecting axiom, countermodel construction or reconstruction proof
  is derived there.
- Added exact rational cycle certificates and independent symbolic matrix
  regression checks, including forged-certificate and observer-blindness
  controls. General theorems have written proofs, not new Lean mechanization.
- Corrected the prior positioning paragraph: a jet may vanish through
  cyclic order kappa minus two before onset, not through kappa minus one.
- Aligned manuscript, README, package metadata and running PDF header to v6.8.
  This is an author-review revision, not an external deposit.

## v6.7 (2026-10-07) — optional-dependency reproducibility and theorem positioning

- Fixed optional-dependency handling in `code/tests/test_polynomial_onset.py`:
  used `pytest.importorskip("sympy")` prior to importing `polynomial_onset` so that
  test collection skips cleanly when SymPy is not installed, matching the declared
  optional extras in `pyproject.toml` and documentation.
- Positioned Theorem 5.16 and Corollary 5.17 against established literature on polynomial
  lifting, Carleman linearization, and finite observability (citing Brunton et al., PLOS ONE 2016).
  Explicitly disclaimed priority for the underlying generic polynomial lifting mechanism, and
  identified the exact contributions: application to non-product projection defects and non-equilibrium
  defect fields, reconstructible state-space annihilator certificates distinguishing vanishing truncated
  jets from persistent zero, interplay with interaction locality bounds, and fail-closed certificate contracts.
- Articulated the mathematical roadmap for the minimal linear observer predicting future defects:
  defined the unobservable subspace $N = \bigcap_{j=0}^{\kappa-1} \ker(O\mathcal L^j|_{\mathcal C_m})$,
  characterized future residual determination by $\ker Q \subseteq N$, and derived the minimum
  number of additional unrestricted linear measurements as $\dim\ker Q - \dim(\ker Q \cap N)$ via
  rank-nullity on the cyclic space $\mathcal C_m$, establishing the mathematical foundation for PFP certificate
  architectures.

## v6.6 (2026-10-07) — finite onset and consistency pass

- Added Theorem 5.16: symmetric-power lifting, the cyclic annihilator recurrence,
  a finite zero certificate and the sharp bound onset <= kappa - 1. Corollary
  5.17 applies it to pair defects and connected cumulants; cutoffs remain
  model-specific and require exact full residual jets.
- Added rational lift/certificate reconstruction and adversarial replay cases;
  these check finite instances, not the general analytic argument.
- Reconciled the manuscript and both retained companion inventories with the
  v6.5 theorem groups and v6.6 additions. Rebound E3-general and E4-general to
  Lemma 5.4 and Theorem 5.5; supplied the missing Proposition 4.7 rank-nullity
  proof for the retained P4-7 entry.
- Recorded Proposition 5.12's negative global/edge comparison result and the
  established local dynamical and specified spatial density limits accurately.
- Gave the new written theorem groups explicit `not_executable` / `refused`
  aggregate dispositions and independently pinned their evidence scope.
  Rejected raw matrix strings before symbolic conversion and added adversarial
  cases for generator and initial-state scalars.
- Reduced the abstract to fewer than 300 words. Removed repeated retired-module and
  withdrawn-path asides from the body; prior entries below retain that history.
- Kept the rejected five-way RE independence claim out of current results;
  its failed examples and their replacement are documented in prior revisions.
- This is an author-review revision, not an external republication. General
  analytic claims remain written proofs with their stated hypotheses; no new
  general Lean mechanization is claimed.

## v6.5 republication review (2026-10-07)

- Rejected floating-point and nonfinite inputs in the new exact metric, phase
  and cumulant helpers before conversion or partial trace can hide them.
- Required one correctly sized matrix per tensor block; missing factors
  previously produced a different matrix through truncated `zip` iteration.
- Added 13 regression cases for these defects and exact algebraic/nonuniform
  dimension controls. General analytic statements are unchanged.
- Corrected section references to §§7.5--7.7 (theorems run through 7.9), and
  aligned manuscript reproduction instructions with the README: the shipped
  v6.3 receipt is historical; current receipts are generated separately.
- Updated publication status wording so a prepared v6.5 package does not
  assert an external deposit. Regenerated reader artifacts and package hashes.
- Review follow-up (same date): corrected the Appendix A publication note
  and the claim-ledger canonical version from v6.4 to v6.5, sorted imports in
  the new replay module and tests, scoped the README `--check` note to one
  Pandoc writer version, rebuilt the PDF from the edited TeX, and
  regenerated package hashes. No mathematical statement changed.

## v6.5 (2026-10-07) — metric, phase and connected-correlation derivations

Author-review revision; no external deposit or publication action is implied.

- Proved the finite nearest-product comparison, full-rank tangent/dual slope,
  strict mixed-state distortion family, and pure-state leading optimality.
- Derived orthogonal pair-sector rates, exact rational squared-rate certificates,
  and the declared normalization bridge; separated weights from directions.
- Refuted unrestricted global/edge trace-norm equivalence with disjoint pairs
  and an exact five-cycle state, settling the unrestricted S7 question.
- Proved support decomposition, connected-cumulant cancellation, Steiner onset,
  radius-(j-k+1) coefficient locality, all-order remainders, short-time spatial
  decay and a fixed-shape all-time density limit.
- Proved sharp full-phase scalar intervals and minimax errors, an exact all-time
  population formula, effect-specific descent, and full-density observer
  completion and operator-norm minimax. Distinguished finite phase hosts,
  block reports, phase means and joint probability-vector prediction.
- Proved augmented cohomology observability and a conditional repair-invariant,
  finite-group-equivariant extension. Kept the external extension and unitary
  stability premises explicit; broader propagation/transport targets stay open.
- Added 24 exact regression cases and a finite-example replay module. These
  check instances and counterexamples, not the general analytic proofs.
  Historical Lean and certificate receipts retain their original scope.

## v6.4 (2026-10-06) — higher-order defect and thermodynamic limits

Author-review revision; no external deposit or publication action is implied.

- Added centered interactions and the pure-product identity relating the
  normal rate to the established correlated-uncertainty timescale.
- Added two-sided, all-order Taylor bounds, exact coefficient locality,
  finite-region constants and explicit Schatten-norm scope.
- Corrected the proposed all-zero transverse-field Ising example: its
  product defect starts cubically, not quadratically. Added a separate
  genuine quadratic example and exact cancellation controls.
- Constructed the all-time local thermodynamic limit on the quasilocal
  observable algebra under compatible bounded interactions on a locally
  finite graph. Under additional lattice translation invariance, proved
  convergence of the edge-defect density along cubes.
- Added 29 targeted Python cases and ten Lean arithmetic declarations.
  These do not formalize the analytic quantum or infinite-volume proofs.
- Identified standard literature explicitly; no new general existence
  theorem, equilibrium limit, phase-selection or late-time persistence
  claim is made.
- Enabled single-backslash math delimiters in the Markdown renderer.
  Historical verification receipts retain their original scope.

## v6.3 (2026-10-06, addendum 8) — house-language pass and the authority fence check

No theorem, proof, or claim status changed.

### In-house programme names removed from reader-facing text

`projection_obstruction.md` and `README.md` no longer use the names of the
in-house programme and its frameworks. Each sentence was rewritten by hand to
say what the name stood for:

- the programme name in the vocabulary note, §4.3.1, §4.6, §7.4.8(3), the
  Compliance Note and Appendix A became "the earlier component papers" or a
  description of the requirement itself;
- the authority-layer framework and its decision layer became "layered
  standing" and "the separation of admission from decision";
- the §7.4.9 companion sequence is described by subject ("local acceptance
  with a global obstruction") rather than by its series acronym, and the
  governance-doctrine slogan is called an informal slogan;
- the §5 heading "Genesis-Bias Fence" became "Imported-Structure Fence";
- the Appendix A slot "AuthorityEffect" became "Authorization", the slot
  "Anomalons" became "Stabilized survivors", the v6.1 provenance row no longer
  names an in-house notebook ladder, and the Authority paragraph and the
  README scope fence carry the academic nonclaim: "This monograph assigns no
  authorization and changes no jurisdiction. It carries no operational
  authority or institutional standing." The README bullet had been an empty
  bold marker since an earlier token removal.

Claim IDs, code spans, file names and the reference list are unchanged.

### Substantive text fixes found in the same read

- Eleven sentences (thirteen occurrences) said a proof or a Lean file "shows
  in this model" a general statement, wording left by an earlier automated
  word replacement; they now say "establishes" or "machine-checks".
- The Import/Oracle boundary pointed to the Compliance Note "below"; it is
  above.
- Data and Code Availability said the replay receipt is "not shipped"; the
  deposit ships `evidence/000_mechanization_run.json` as a hash-bound copy of
  the replay output, and the bullet now says so.
- §7.4.11 said every listed binding has a `#print axioms` report;
  `ThreePatch.scaledDefect_is_section_defect` has none, and is now marked as a
  supporting lemma. The Lean bullet's "14 declarations" now reads "14
  axiom-reported declarations" (the file has 26 theorems).
- The README said this release commits the archive under `dist/`; no `dist/`
  is committed, and the sentence now says the builder writes it there.
- Three excluded adverb occurrences were replaced.
- The Claim-Type Ledger row for the Python replay package said "no authority
  effect", which the review gate reads as the governance token once spaces
  are stripped; it now says the package "authorizes nothing".
- A horizontal rule directly under a blockquote marker (§3.4) read as a
  setext heading underline; a blank line now separates them.

### Two build inputs that put the wrong text in the PDF

- `scripts/obstruction-preamble.tex` set `AuthorityEffect: None` in the
  right-hand running header, so the rebuilt PDF carried the token on every
  page (42 times; the PDF it replaces had none). The header now reads
  "Preprint v6.3".
- `scripts/build_paper_artifacts.py` replaced the manuscript's subtitle with
  "Local correlation lower bounds, additive diagnostics, and observer
  recovery", a subtitle no other file in this package uses. It is restored to
  the manuscript's subtitle.

### The replay's authority fence now checks the nonclaim sentence

`code/replay.py::_scope_fence_receipt` required the literal fragment
`authorityeffect: none` in `README.md` plus the manuscript. Reader-facing text
must not carry that token, and neither document contained it, so the committed
`evidence/000_mechanization_run.json`, which recorded `pass`, was stale. The
fragment is replaced by the academic nonclaim sentence, matched
case-insensitively after whitespace normalisation; every other fragment is
checked exactly as before. A temporary copy with the sentence altered
returns `fail` with the sentence listed as missing. The evidence file, its
manifest, the `.tex`/`.pdf` and `SHA256SUMS` were regenerated after these
edits.

## v6.3 (2026-09-03, addendum 7) — the release objects, repaired

 No theorem, proof, or claim status changed.

A second review rejected the first release objects. It was right on every
count, and three of the five were mine.

### The PDF rendered with holes in it

Eleven characters were **silently dropped**. `ω`, `₁`, `≤`, `≥` and `ν`
vanished out of the dependency diagram on page 39, corrupting the formulas
into ordinary-looking text, and `ℓ` vanished from a reference title on page 43.

The cause was my font choice. I set Latin Modern Mono for portability —
correctly, after a first attempt named DejaVu Sans Mono, which this machine
does not have — without checking that it carries the characters the manuscript
uses. No monospace face shipping with a TeX distribution has Greek or the
relational symbols. xelatex reported all eleven and **exited 0**.

Two repairs, because either alone would leave the trap open:

- The ASCII diagram now uses ASCII: `omega`, `<=`, `>=`, `nu`, `_1`, `^2`.
  Inside an ASCII-art block that was the right register anyway. The one
  character outside a code block, `ℓ¹` in reference 5, is now `$\ell^1$`.
- **The build now fails on a dropped glyph.** `audit_log` parses the xelatex
  log and refuses the PDF on any `Missing character`, or on an overfull box
  wider than 10pt. A PDF that renders with holes is worse than one that fails
  to build, because it looks finished.

### Text ran past the margin

Nine overfull boxes, the worst 150pt. Long Lean filenames set in typewriter
neither hyphenate nor break, so a name wider than the line ran into the
margin. `hyphenat` with `[htt]` plus `xurl`, `\emergencystretch` and `\sloppy`
bring it to **zero** overfull boxes — not only under the new threshold.

### Byte-reproducibility was not portable

The claim was true only on the machine that made it. A Linux rebuild produced
content-identical members at 606,567 bytes against 607,244. Two causes, both
platform rather than content: `zipfile.ZipInfo` stamps `create_system` 0 on
Windows and 3 elsewhere, and this machine's zlib is **zlib-ng**, whose deflate
output differs from stock zlib at the same level.

`create_system` is now pinned to 3, and members are **stored, not deflated**,
which removes the compressor from the question entirely. The archive roughly
doubles, 607 KB to 1.33 MB, which is a cheap price for a claim that survives
leaving this laptop.

The `.tex` and the `.pdf` are weaker cases and are now described as such.
Pandoc's LaTeX writer changes between releases, so `--check` reports
reproducibility **against a named Pandoc version** and prints the toolchain.
The reviewer's `False` under a different Pandoc was correct, not a defect.

**Corrected 2026-09-04.** An earlier version of this entry, and a comment in
`build_paper_artifacts.py`, said the PDF was byte-identical *on any machine*.
That was false. The same shipped `.tex` gives **271,208 bytes at PDF 1.7 under
MiKTeX** and **271,122 bytes at PDF 1.5 under TeX Live**: engine build, font
files and default PDF version all enter the bytes. Pinning `SOURCE_DATE_EPOCH`
removes the wall clock, which is what makes two builds agree *on one
toolchain*; it does not make the PDF portable. The correct statement, now the
  one in the code: **the ZIP is cross-platform byte-reproducible from the
  committed payload bytes; regenerating the TeX or PDF with a different
  Pandoc/XeLaTeX/font toolchain changes those inputs and therefore changes the
  archive.**

### Two wording corrections

`A1`'s pointer still called §5.1 a `subsection` of §5.5, which it is not; the
field is `supporting_section` now, renamed rather than deleted because the
relationship is real and was only mislabelled. And the paper said dependencies
are "pinned" while `pyproject.toml` declares minimum versions; it now says so.

### Figures for the artifacts actually released

- Manuscript 1,577 lines; PDF 43 pages, 0 missing characters, 0 overfull
  boxes. 271,208 bytes under the recorded toolchain; a different TeX
  distribution gives a different size for the same input.
- Archive: **85 payload files** covered by `SHA256SUMS`, and **86 ZIP
  entries** — the payload plus the `SHA256SUMS` generated from it. The
  builder now prints both, because quoting either alone has already
  produced a false statement. Byte-identical across builds and across
  platforms.
  The size and hash are not quoted here: this file is a member of that
  archive, so any figure written into it changes the number it claims. That is
  how the stale "605,677 bytes" above came to describe nothing — it was
  accurate when written and obsolete one edit later. The authority is
  `dist/projection_obstruction_v6.3.0.zip.sha256`, written by the builder
  after the tree is final.
- 391 tests: `code/tests/test_paper_artifacts.py` pins the log gate in
  both directions (a dropped glyph and a 150pt box must block; a 1.5pt box and
  a clean log must not), the archive's pinned `create_system`, timestamps and
  stored members, and the rule that no character outside the monospace
  repertoire may sit in a fenced block.
- Toolchain recorded in every build: pandoc 3.7.0.2, MiKTeX-XeTeX 4.16.

## v6.3 (2026-09-03, addendum 6) — review corrections, and the TeX/PDF/ZIP release objects

 No theorem, proof, or claim status changed. Two status
fields were **downgraded** to match evidence that was already recorded.

### The four corrections the review made release-blocking

- **The paper's index listed 49 of 51 claims.** The `E: Quantum Defect` row ran
  `E1 … E9` and omitted `E4-second` and `E4-commutator`, which were added to the
  ledger earlier today. Both are now listed and the row points at Appendix B as
  well. Summing the eight group rows now gives 51.
- **`A1`'s YAML pointer was incoherent**: `section: §1`, `subsection: §5.1`,
  `heading: "Section 5.5 Density Corollary"` — three different locations for one
  claim. The principal location is now §5.5, where the density corollary is
  actually proved, with §5.1 retained as the subsection it rests on.
- **`D6` claimed more mechanization than it has.** `MECHANIZED` became
  `MECHANIZED-LOCAL`. The Lean module verifies four displayed instances
  (`l2_combination_not_additive`, `l2_combination_calibrated`,
  `doubled_sum_additive`, `doubled_sum_not_calibrated`), not the general RE
  countermodels; the markdown ledger had always said so and the YAML had not.
- **`E4-commutator` bound one lemma where its own statement names four.** The
  single `symbol: double_factor_k2` is now a `symbols:` list carrying
  `first_order_k1`, `first_order_k2`, `double_factor_k1` and `double_factor_k2`.
  Nothing consumes the `symbol` key, so the shape change breaks no consumer.

The review also asked for the TeX-only refusal box to be replaced. It was
`$$\boxed{\parbox{0.88\textwidth}{…}}$$`, which renders in LaTeX and in
nothing else — GitHub and Pandoc both show the raw macro. It is now a
blockquote, which renders everywhere including the PDF built below.

### A fifth item, not in the review

Seven YAML `file_location` values named
a Lean directory that does not exist in this deposit; the Lean sources sit flat under
`lean4/`. 52 occurrences repointed. Every `file_location` in the ledger now
resolves to a file that is present, checked mechanically rather than by eye. A
citation that does not resolve is not a citation, and the archive would have
shipped seven of them.

### Release objects

`scripts/build_paper_artifacts.py` renders the canonical Markdown to `.tex` and
`.pdf`; `scripts/obstruction-preamble.tex` is the house preamble. The Markdown
stays the source of truth — the TeX is regenerated rather than hand-maintained,
so the two cannot drift.

- 43 pages, 271,215 bytes, built by xelatex through Pandoc.
- **xelatex, not pdflatex**: the manuscript carries twelve non-ASCII characters
  (`§ — – ² ℓ ¹ Π ω ₁ ≤ ≥ ν`) that pdflatex cannot set without per-character
  declarations.
- **Latin Modern Mono**, not DejaVu or Consolas: it ships with every TeX
  distribution, so the archive builds on a machine carrying only TeX Live or
  MiKTeX. The first attempt named a font this machine did not have.
- The PDF is byte-reproducible **on one toolchain**. A PDF embeds its
  creation time, so `SOURCE_DATE_EPOCH` and `FORCE_SOURCE_DATE` pin the run to
  the declared publication date and two builds here agree exactly. (This line
  originally claimed portability. Corrected in addendum 7: MiKTeX and TeX Live
  produce different bytes from the same `.tex`.)

Three build defects worth recording, because each was silent in a different way:
the subtitle's `\ell` was written into a double-quoted YAML scalar, where `\e`
is an escape for ESC — xelatex received a raw `0x1B` byte and refused the file;
`breaklines` is an `fvextra` option, not a `fancyvrb` one; and `subprocess` with
`text=True` raised `UnicodeDecodeError` in its reader thread on output the
Windows locale codec cannot decode, which would have hidden a successful build
behind a traceback.

Archive and test counts for this entry were superseded within the day;
see addendum 7 for the figures that describe the artifacts actually
released. The intermediate archive quoted here was never uploaded.

## v6.3 (2026-09-03, addendum 5) — public_export removed; four ledger repairs

 No theorem, proof, or claim status changed.

`public_export/` is deleted in full: three PNG figures, eight launcher scripts
and its README. `code/generate_figures.py` goes with it, since that folder was
its only output target and its only consumer.

Nothing depended on them. The manuscript references the figures **zero** times,
and neither claim ledger cites the figures or the generator. The folder existed
to be looked at, and it had become a second surface to keep in sync with the
paper: a review had just found its README describing the redrawn Figure 3 as
"illustrative values" while the figure itself says "computed, not illustrative",
and calling the folder "zero-setup" when the launchers require `uv` and a
first-run download. One fewer surface is one fewer thing to contradict.

Cleaned with it: `verify_certificate.py`'s source inventory, the README, the
quick start, two notebooks, `scripts/build_enter_notebook.py`, and four tests
whose subject no longer exists (`test_generate_figures`,
`test_all_three_figures_render`, and the two archive launcher-mode tests). The
figure *arithmetic* guards in `test_figures_match_claims.py` are kept: the
half-slope threshold, the zero crossing, the fact that the bound equals
`nu_e t / 2` exactly at the window edge, and the three-patch and scaling values
are all still pinned, because those are claims about the paper rather than
about a PNG.

One self-inflicted correction, and the second time today for the same reason:
deleting by whole line removed the README's **Tier 1 and Tier 2** rows, because
each *mentioned* the folder — Tier 2 only for its launcher, while the row
itself describes the primary front door. Tier 2 is restored without its launcher
clause and Tier 1 rewritten around the quick start. Line-based deletion is the
wrong tool for table rows, and this is now twice.

Manifest 90 → 77 files. Suite 381 → 377 tests. 7 notebooks, all executing.

### Four ledger repairs found by review

Reported against the same tree and fixed here. None changes a proof.

- **`E4-commutator`'s markdown row was corrupted.** The downgrade earlier today
  (addendum, above) rewrote it by pattern replacement, and the `\|` pipe
  escapes inside the displayed commutator inequalities were treated as column
  boundaries. The result concatenated the new wording with most of the retired
  row: eleven cells instead of seven, a cell beginning mid-formula with
  `\le 2kg\|A\|`, an unbalanced `$`, and the superseded `MECHANIZED-LOCAL`
  status still sitting there beside the new one. The row is rewritten as seven
  cells with the inequalities described rather than displayed, so no escaped
  pipe survives in a table. A cell-count check across the whole ledger now
  reports every row at seven.
- **`A4`'s YAML pointer still named the frontmatter.** The mechanism inventory
  moved to Appendix A when the abstract was cut from 94 lines to 23; the
  pointer did not follow. Both `paper_pointer` and the `static_scope_fence`
  evidence pointer now say Appendix A.
- **`G3` and `G4` claimed prose proof they do not carry.** Their status is
  `IMPORTED; NOT VERIFIED IN THIS DEPOSIT`, but the mechanization cell still
  read `Prose-proved`. It now reads "None in this deposit; companion
  cross-reference only", which is what an imported cross-reference is.
- **The bound-declaration list named a withdrawn symbol.**
  `one_site_first_from_double` was the citation withdrawn from `E3` in
  addendum 2; the summary paragraph still carried it, so a reader met two
  apparent bindings. It now names the same four factor lemmas the
  `E4-commutator` row does.

The review also asked for `public_export/run_falsify.sh` to be documented. That
file no longer exists -- it went out with the folder above. Every route the
README advertises is now a `python ...` invocation, which needs no per-platform
variant, and the falsification wing is reached through
`jupyter_notebooks/falsification_sandbox.ipynb` or `code/falsification_sandbox.py`.
The stale `(+ refute / falsify wings)` label in the README tree is corrected to
`(+ reviewer / falsify wings)`, the refutation wing having been cut in
addendum 4.

## v6.3 (2026-09-03, addendum 4) — refutation sandbox removed

`jupyter_notebooks/refutation_sandbox.ipynb` is removed as a near-duplicate of
`falsification_sandbox.ipynb`. Measured before deleting: **85% code similarity,
and 7 of its 8 code cells more than 85% identical** to a falsification cell.

Its one non-duplicated cell was itself a liability. It ran a single test file
and printed `EMBEDDED PYTEST UNIT SUITE: 100% PASSING` — the same overclaim
shape that got `interactive_museum_of_reality.ipynb` removed earlier today
(one test file, a "100%" headline). Nothing of value is lost.

Removed with it: `public_export/run_refutation.sh` and `.bat`, and its rows in
`docs/quick_start.md` and `public_export/README.md`. `falsification_sandbox` is
now the single canonical attack notebook, which is what the review recommended.

Two corrections made during the removal, both self-inflicted:

- Deleting by whole line destroyed the README's **Tier 2** row — the row that
  describes the primary interactive front door — because it happened to mention
  the sandbox among its wings. Restored with only the Refutation wing dropped.
  The first restore attempt also introduced mojibake, because `git show` output
  was decoded as cp1252 rather than UTF-8; redone with an explicit decode and
  checked for `Â`/`â€` before writing.
- `test_shell_launchers_are_executable_in_the_archive` asserted `>= 5` POSIX
  launchers and failed at 4. The expected set is now derived from
  `public_export/*.sh` rather than hard-coded: a test that fails because the
  deposit legitimately changed shape is noise, not a guard.

Notebooks 8 → 7, all executing. Suite: 384 → 381 tests (the three lost are the
per-notebook parametrised portability guards for the removed file).

## v6.3 (2026-09-03, addendum 3) — notebook layer: a 3.11 crash and a withdrawn claim revived

- **`observer_carriers_demo.ipynb` crashed on Python 3.11.** It formatted an
  exact `Fraction` with a width spec, `f"{instance.tallies.I:>15}"`.
  `Fraction.__format__` was added in CPython **3.12**; before that the call
  falls through to `object.__format__` and raises *unsupported format string
  passed to Fraction.__format__*. `pyproject.toml` declares
  `requires-python = ">=3.11"`, so the notebook was broken on a version the
  deposit claims to support, and passed locally only because the development
  interpreter is 3.14. Values are now `str()`-wrapped. This is the same failure
  shape as the release archive that was only ever built outside its documented
  output directory: verified in the author's configuration, not the advertised
  one.
- **`replica_hierarchy_demo.ipynb` revived a withdrawn claim.** It asserted in
  two places that *every* RE axiom is load-bearing, then stated at the end that
  the five-way independence claim had been withdrawn — a self-contradiction
  whose first half is precisely the withdrawn claim. The paper says that once
  RE3 and RE5 are assumed, RE1, RE2 and RE4 are **redundant** for the
  unweighted conclusion, and only the RE3-drop and RE5-drop countermodels
  survive. The narrative now says that, and the RE1/RE2 plain-language glosses
  are corrected: RE1 is that the whole-system score is a genuine gauge, RE2
  that it depends only on declared local magnitudes rather than direction or
  phase.
- **Observer metaphor corrected.** "The problem falls between the monitors" is
  not the constructed mechanism. Each defect lies in the kernel of its assigned
  monitor's projection — a direction that monitor cannot see. Not between the
  monitors: inside one, in a direction it is blind to.
- **Notebook hygiene.** All 88 cells across the eight notebooks now carry
  stable ids (`nbformat` warns today and is expected to make this an error),
  and saved outputs are cleared. Only the inline companion had carried outputs,
  with inconsistent execution counts including output attached to cells whose
  `execution_count` was null — worse than none, since it implies a run that
  never happened in that order.

`code/tests/test_notebook_portability.py` (27 tests) guards all of it: the
declared Python floor, the `Fraction` format hazard simulated through
`object.__format__` so it fails on any interpreter, cell ids, absence of stale
outputs, and a check that the withdrawn independence claim cannot reappear in
the replica notebook.

Reconfirmed from the review's adjacent list: `docs/quick_start.md` now gives
`nu_e = ||n_e||_1 = ||(I - P_e) L_e||_1`, `code/tests/test_so_k_3cell_benchmark.py`
exists, and no README names `run_museum.bat`. Suite: 357 → 384 tests.

## v6.3 (2026-09-03, addendum 2) — E3's Lean citation withdrawn

 The markdown ledger was already correct here; the YAML
was not, and it is brought into line rather than the reverse.

`E3` recorded a Lean binding the markdown ledger never claimed. Three defects,
all in the YAML:

- **Wrong object.** The statement read "operator norm bounds on ... *reduced
  state* second derivatives". Lemma 5.2 bounds `||[H,[H,A_S]]||_inf` for a
  local **observable** `A_S` with `||A_S||_inf <= 1`. The reduced-state
  derivative bounds Theorem 5.1 consumes are **trace-norm** quantities obtained
  from those by duality, and that conversion is paper-resident. The right norm
  was attached to the wrong object.
- **Wrong order.** The cited symbol was
  `PO000.DoubleCommutatorEstimates.one_site_first_from_double`, which verifies
  `firstOrderFactor 1 g = 2 g` — a **first**-order identity — for a claim about
  **second**-derivative bounds `8g^2` and `24g^2`. The second-order lemmas
  `one_site_second_from_double` and `two_site_second_from_double` sit directly
  above it in the same file, so this reads as a neighbouring-line slip.
- **Overstated status.** That evidence entry carried `MECHANIZED-LOCAL` while
  the markdown recorded evidence `None`.

The citation is **withdrawn rather than repointed**. The arithmetic factors are
already credited under `E4-commutator`; citing the same lemmas again under `E3`
would inflate the apparent mechanization by counting one fact twice. Two
limitations now record that these are operator-norm bounds on observables, that
the trace-norm conversion is not mechanized, and that
`ReducedStateBounds` carries the `8g^2` and `24g^2` fields as **hypotheses**,
not as results.

Both ledgers now agree: E3 is prose-proved with no Lean evidence. Ledger Lean
references 48 → 47, all resolving. 357 tests; checksums clean.

## v6.3 (2026-09-03, addendum) — E4-commutator downgraded; manuscript pointer corrections

- **`E4-commutator` downgraded to `ARITHMETIC FACTORS MECHANIZED ONLY`.** It had
  been recorded as `MECHANIZED-LOCAL` and cited
  `PO000.DoubleCommutatorEstimates.second_deriv_from_double_factor`, which is
  proved by `rfl` with an unused hypothesis: it states that a definition equals
  its own body and carries no mathematical content. The Lean module's own
  header was already honest — it says the operator-norm and support-expansion
  argument "remains paper-resident" — but the ledger was not.

  What the module does prove is the arithmetic: the support-counting factors
  `2k` and `4k(k+1)` and their specialisations to the paper's `2g`, `8g^2` and
  `24g^2`. The citation now names `double_factor_k1` / `double_factor_k2`,
  which have that content, and the status says only that. The commutator
  inequalities themselves are explicitly recorded as a structured hypothesis
  record that is *not* proved in Lean, and the limitation notes that the module
  contains no matrices, commutators or Schatten norms. Downgraded consistently
  across both ledgers, `replay.py`, `claim_coverage.py` and `lean4/README.md`.

  **`E4-second` is deliberately left at `MECHANIZED-LOCAL`.** Its
  `product_rule_second_deriv_bound` discharges `48 g^2` from the structured
  bounds by `nlinarith` over real hypotheses, which is a real derivation rather
  than an unfolding. The two claims are not in the same position and are no
  longer described as though they were.

- **Manuscript pointer corrected.** The authority-status paragraph said the
  authorization record is "described in the front matter"; it moved to
  Appendix A in the presentation pass above.
- **Duplicate horizontal rule removed** before Appendix B, introduced by that
  same relocation.
- **Contribution 1 retitled** to "Exact Short-Time Local Defect and Density
  Corollaries (Theorem 5.1 and §5.5)". Theorem 5.1 is edge-local; the density
  statement is the §5.5 corollary, and the previous title conflated them.

All 48 Lean references in the YAML ledger still resolve to declarations that
exist. 357 tests pass; checksums clean.

## v6.3 (2026-09-03) — release-integrity pass

 No theorem, proof, or claim status changed anywhere in
this entry; the manuscript's mathematics is untouched. What changed is the
apparatus around it: the ledgers, the machine evidence rail, the packaging, and
what a reader meets first.

An earlier revision of this section recorded the same work as nine separately
numbered same-day passes running to 4,300 words — longer than Theorem 5.1's own
section. That was the same failure the mechanism-inventory move below was
meant to fix, reintroduced one layer down. Collapsed here; every finding is
kept, the pass-by-pass narration is not.

### Ledgers and cross-references

- **Canonical H1–H9 numbering restored in the YAML.** It fused the markdown's
  H1 and H2 and ran H2/H3 one behind, so no H4 existed — while `H7` declared
  `depends_on: H4`. Under the markdown numbering that dependency resolves to
  Proposition 7.4.4, exactly the lemma Corollary 7.4.7 uses.
- **Four rows added** that the markdown ledger had and the YAML did not:
  `E4-second`, `E4-commutator`, `G4`, `H2`. Both ledgers now carry the same 51
  claim ids with no dangling dependencies.
- **H6 rescoped** to the fixed three-patch family. It had generalised over
  observer families lacking joint-kernel triviality, which `H8` in the same
  file refutes.
- **Lean bindings completed** for D3, D4, H3 and H5–H9. Ledger Lean references
  went 19 → 48, and all 48 resolve to declarations that exist in `lean4/`.
  `D6` had named the H5 three-patch theorem rather than its own RE3/RE5
  countermodel arithmetic.
- **RE1–RE5 were misnamed.** The YAML called RE2 homogeneity and RE3 singleton
  additivity; §4 names them global gauge, local magnitude sufficiency, disjoint
  replica additivity, edge-exchange symmetry, singleton calibration. The error
  had propagated into D3 and D5.
- **E5 carried a spurious factor 1/2.** §5.5 gives
  `C(t)/N ≥ aη(ν_min t − 24g²t²)`; the half belongs only to the subsequent
  half-slope form on `0 < t ≤ ν_min/(48g²)`.
- **E4** named a nonexistent anchor `thm-5-1` and a moved line range, and
  scoped the whole theorem to the half-slope window. The quadratic inequality
  holds for every `t ≥ 0`.
- **E2/E3 section pointers were swapped**, the claim index stopped the H group
  at H7 while H8 and H9 were active, **G3/G4** disagreed across ledgers (now
  `IMPORTED; NOT VERIFIED IN THIS DEPOSIT`, since those companions are
  unpublished), and reference `[9]` — an external Nachtergaele–Ogata–Sims paper
  — sat inside the companion-paper set.
- **`published_root` named a nonexistent `published_papers` tree** in both
  `manifest.json` copies, and they named *different* nonexistent paths. That
  divergence made `lean4/README.md`'s byte-identical claim false; repairing it
  made the claim true rather than weakening it, re-verified by `cmp` across all
  17 shared files. Retired `omega_engine` build paths are annotated in place.

### Machine evidence rail

- **The claim universe is derived from the ledger,** in both `evidence.py` and
  the independent `verify_certificate.py`. Each had carried its own stale
  47-id set ending at H7, so `claim_disposition_complete` could report true
  while `E4-second`, `E4-commutator`, `H8` and `H9` had never been considered.
  Both now fail closed if the ledger is absent.
- **`D8a` unbound from the quantum replay.** The ledger defines it as the scope
  fence that repairable mass `R` is *not established here*, evidence `None`; a
  passing simulation was reporting evidence for it. It is now a static scope
  fence auditing the paper's own `R` disclaimer.
- **`H1`/`H2` unswapped** in `claim_coverage.py`, which had the §7.4.2 tallies
  under H1 and observer-family nonemptiness under H2.
- **`source_hashes()` fails closed.** An `exists()` filter meant a tree holding
  only `code/one.py` produced a valid-looking hash dictionary.
- **The YAML ledger and `README.md` are bound by the receipt.** Both feed the
  certificate — the README supplies its scope fences — and neither was hashed.
- **Every claim's expected disposition is pinned** in the verifier, which now
  refuses to load if any is missing. `D8a`, `E4-second`, `E4-commutator`, `H8`
  and `H9` were unpinned, so the disposition loop skipped them and accepted any
  evidence kind and verdict.
- **Exit status covers disposition completeness**, as a secondary guard behind
  the `ArithmeticError` that already fails closed on coverage mismatch.

### Tests: 166 → 357

- **Adversarial falsification** of the PROVED claims rather than confirmation
  of them. Theorem 5.1 survived 660 randomised draws, worst margin `3.5e-08`.
  Several tests assert the search was *not vacuous*; an early H7 test met its
  hypotheses once in 400 draws and now exercises 150.
- **Fault injection** broke the shipped source one line at a time. Four
  mutations survived the suite: Theorem 5.1's constant changed from 24 to 20
  (a randomised inequality search cannot pin a constant that only tightens the
  bound), `bound_satisfied_with_tolerance` hard-wired true, `covered !=
  required` weakened to `<=`, and the fail-closed hashing guard removed. All
  four are now killed; re-running the injection kills 10 of 10.
- **109 verifier mutation tests** mutate a real receipt one claim at a time.
- **Exact-engine refusal paths** took `exactsym.py` from 78% to 91%. One
  boundary is recorded as a characterisation test rather than a guarantee:
  `Rational` *is* `fractions.Fraction`, so `Rational(1) + 0.5` yields a float
  before any guard runs. `Matrix` and `Basic` are guarded.
- **Release-packaging and figure tests** lock the items below.

Branch coverage of production modules is 91%, reported rather than raised by
excluding modules from measurement.

### Removed

- **`code/lattice_simulation.py`** labelled trace norms of nested *global*
  commutators as Taylor coefficients of the *edgewise* defect (its `H_int`
  argument was unused), called `c₂t²` a theoretical lower bound where Theorem
  5.1 states `ν_e t − 24g²t²`, clipped the signed RHS at zero, and marked every
  `t ≤ t₀` point valid without testing the inequality — vacuous in exactly the
  regime the theorem covers. Removed with its two tests.
- **`interactive_museum_of_reality.ipynb`** asserted "zero-assumption", "every
  claim is powered by executable Python" and "100% of claims mechanized and
  verified" (printed after running one test file), against a ledger with 24
  prose/Lean-only dispositions and `promotion_eligible=False`.
- **`docs/claim_code_map.yaml`** assigned the wrong meaning to every one of
  D1–D4 — it called D1 the short-time defect theorem, while the ledger defines
  D1 as the RE1–RE5 structural declarations — and overstated statuses as
  `MECHANIZED`. Its only consumer now resolves against the canonical ledger:
  31 Python evidence pointers, all resolving.
- **`docs/lean_claim_map.md`** was stale throughout (`H7-B` for `H8`, `H12` for
  `H9`, `rawNorm_scaled` under H5 rather than H6, two of D6's four declarations
  missing, the `PO000.` namespace dropped).
  **`docs/dev_rips/run_po000_20260805_receipt.yaml`** was a v6.1-era
  development receipt nothing in the deposit read.

### Release object

`scripts/build_release_zip.py` builds the archive from the tree at release
time, packs only what `SHA256SUMS` covers, and normalises text to LF *inside*
the archive so the manifest verifies on any platform — this tree is CRLF while
the repository stores LF, so the manifest had been checkout-dependent.

Two defects in that script were self-inflicted and worth recording. The
documented `--output dist` path was **not reproducible**: `regen_sha256sums.py`
did not exclude `dist/`, so the second build hashed the first archive and its
sidecar (93 members, then 95). Every development run had built into a directory
outside the package tree and passed — the one configuration never tested was
the one the documentation tells a reader to use. And POSIX launchers shipped
mode `0644`, so `./run_paper.sh` failed straight out of the archive.

Verified from a clean extraction of the built archive, not from the working
tree: `SHA256SUMS` all matching, full suite passing, replay and bundle exit 0,
independent verifier `verdict: pass`.

### Presentation

- **The mechanism inventory moved to Appendix A.** It occupied the first 1,434
  words — four times the abstract — so a reader met `AuthorityEffect`,
  `Anomalons`, `ZeroRel` and `CompletionLaw` before learning what the paper was
  about. The abstract moved from line 94 to line 23.
- **§7.4 promoted from third-tier to a headline result.** The local-green /
  global-red gap was 3,044 words against Theorem 5.1's 1,647, sitting in a
  subsection of a section titled "Discussion", and absent from the abstract
  entirely. It is now in the abstract, listed second in the contributions, and
  §7 is retitled. **No subsection was renumbered**, so all 104 cross-references
  across the paper, both ledgers, the Lean sources and the tests remain valid.
- **Theorem 3.1 demoted** to a supporting criterion: in an affine chart it is
  close to the definition of affine-linearity.
- **Figures 2 and 3 redrawn from computed values.** Figure 2 had shaded a band
  labelled "Certificate Validity Domain" to `t = 0.05` while its own parameters
  put the certified window at `0.00463` and the zero crossing at `0.00926`;
  both thresholds are now computed, drawn and annotated. Figure 3 had plotted
  invented bars and called their difference the visibility gap, which §7.4
  defines as `Λ_max = I − max_α J^α` over an observer family that did not
  appear in the plot; it is now the actual three-patch witness and scaling
  family.
- **Notebooks.** Two were code dumps carrying an obsolete paper title and are
  rewritten to explain before computing; the quantum demo had displayed a
  *global* commutator norm under the label "Thermal Normal Rate ν_e(β)" and now
  uses `FiniteQuantumLattice.normal_rate_replay`. Six positional
  `FloatSlider(value, min, max, step)` calls broke the front-door notebook for
  anyone who installed the documented `[notebooks]` extra — fixed in both the
  notebook and its generator.
- **Consistency.** The receipt path, the `pytest` invocation, and the
  unpack/no-zip contradiction were unified across paper, README and quick
  start; `docs/quick_start.md` had defined `ν_e` differently from the paper;
  the version table's "Release Date" column is now "Manuscript Revision Date",
  with a note that Zenodo's publication date is the deposit date.
- **`LICENSE`** was a 46-byte MIT stub naming a fourth license contradicting
  Zenodo, the paper, `pyproject.toml` and every sibling paper. Replaced with
  the CC-BY-4.0 / Apache-2.0 dual statement the published v6.0 already carried.

### Considered and deliberately not changed

- **Bold usage.** 216 spans looked excessive, but 54 are table cells, 65 list
  lead-ins, 33 paragraph-initial run-in headings and 13 theorem labels. Only 34
  are mid-sentence, most bolding a term at its definition.
- **The three closing ledgers.** Compliance Note, Claim-Type Ledger and Support
  Ledger are not overlapping: the first sets the operating layer, the second is
  a per-result status table, the third the S1–S15 open-problem register.
- **Eight `zip()` calls without `strict=`.** Each is preceded by a shape check
  that short-circuits, so no length mismatch can reach the zip.

## v6.3 (2026-08-31, fourth pass) — verified code-review repairs (findings F2, F5–F10)

A verified code review of the staged release found seven defects in this
package; every one is repaired here, in place.

- **Stale public zip deleted (F2).** `projection_obstruction_20260831_public.zip`
  — adopted "as shipped" by the third pass above, with a note that it predated
  the landing — was extracted and inspected: its contents are the **pre-audit
  sympy v6.1.1 package** (its `exact.py` imports sympy, its `replay.py` is
  `__version__ 6.1.1` with the removed can-never-fail fallback, no
  `exactsym.py`). A Zenodo reader would have taken the current-dated "public"
  zip as the v6.3 deposit and obtained a green certificate for the retired
  package. Deleted for the same reason the author approved deleting the
  20260805 zip: its contents contradict the tree it sits in. No public zip
  now ships at this root; README and the paper's deposit-parity note say so.
  `SHA256SUMS` regenerated after the deletion.
- **Demo notebooks repaired to real APIs (F5).** `quantum_lattice_demo.ipynb`
  and `replica_hierarchy_demo.ipynb` imported `tfim_open_chain`,
  `simulate_thermal_normal_rate`, and `verify_re_axioms_on_grid` — none of
  which exists in `code/`. Their code cells now use the real exports
  (`lattice_simulation.build_1d_tfim_hamiltonian`,
  `lattice_simulation.run_thermal_defect_simulation_replay`,
  `replica_hierarchy.FiniteDiagnosticFamily.audit`) and both notebooks were
  executed headlessly end-to-end after the repair.
- **Claim-code map dead names fixed (F6).** Three of four
  `docs/claim_code_map.yaml` rows named `code_function` values that existed
  nowhere (`short_time_defect_bound`, `so_k_3cell_defect`, `cochain_defect`).
  They now name the real exports (`SecondDerivativeBoundCertificate`,
  `solve_so_k_vector_residual`, `ObservationPresentation`), and D3's
  `test_file` now points at the file that actually exercises the
  presentation class.
- **Reviewer notebook made genuine (F7).**
  `reviewer_projection_obstruction.ipynb` was byte-identical to
  `falsification_sandbox.ipynb` while every reference presented it as
  distinct Reviewer Walkthrough content. Chosen repair: replace it with a
  genuine thin walkthrough (runs the replay, verifies the certificate with
  the stdlib verifier, resolves the D1–D4 sample map, and points at the full
  evidence surfaces), rather than deleting it and retitling every reference
  — the references were correct about what *should* exist; the file was the
  lie. The new notebook states this provenance in its first cell.
- **Verifier fails closed on missing requirements (F8).**
  `code/verify_certificate.py` filtered its own required-path sets to files
  that exist, so a required-but-missing file silently shrank the contract.
  Requirements are no longer filtered; the publication set is split into
  three genuinely required files (paper, claim ledger, change log) and an
  explicit commented `OPTIONAL_PUBLICATION_PATHS` allowlist (pdf/tex and the
  historical release-flow artifacts). `verify_po000_release.py` is removed
  from both the verifier's and `replay.py`'s inventories entirely — the
  paper disclaims that script, and the old `exists()` guard meant a stray
  file dropped at that name would be silently hashed into the publication
  surface. `replay.py` now raises on a missing required publication file.
  The replay→bundle→verify round trip was re-run green, and both failure
  directions were demonstrated on a scratch copy (missing file on disk;
  missing entry in the certificate) and shown to recover on restore.
- **Benchmark receipt reports real convergence (F9).**
  `code/so_k_3cell_benchmark.py` unpacked the optimizer's `converged` flag
  and never used it; `"success"` was `np.isfinite(size)`, true on every
  non-diverging run. The receipt now carries `converged` (the real flag),
  `residual_finite` (the old check, kept separately), and
  `success = converged AND finite`. Doing so exposed a genuine
  non-convergence at k=5: the scipy-free L-BFGS rewrite had dropped scipy's
  function-decrease (`ftol`) stopping criterion, so nearly-nonsmooth
  objectives ran to `max_iter`. The criterion is restored with scipy's
  default (`factr=1e7` ⇒ `ftol = 1e7·eps`), and the benchmark tests re-run
  green with the honest flag.
- **Launcher CWD bug fixed (F10).** `run_notebook.sh/.bat` and
  `run_sandbox.sh/.bat` referenced `../jupyter_notebooks` relative to the
  caller's CWD; invoked from the package root per the README they resolved
  to a nonexistent path. All four now begin with the same
  cd-to-script-dir preamble as the other eight launchers.

A path-filtered CI workflow (`.github/workflows/po000_deposit_checks.yml` at
the repository root) now runs `scripts/regen_sha256sums.py --check` and the
test suite on pull requests touching this package, and the 029 deposit's
`verify_deposit.py` on pull requests touching that one — previously no CI
job ran either checker.

## v6.3 (2026-08-31, third pass) — landing the republication pass that missed its window, plus the approved pruning

Two automations worked this package the same day, and this entry records what
actually happened rather than the first diagnosis. The republication pass's
final 73-file push arrived on its pull-request branch *after* that pull
request had already merged, so the audited package never landed on `main` —
`main` kept the pre-audit README (dead links included) and the sympy-dependent
code, not by any revert but by an early merge. Separately, a parallel
automation deleted the notebook, launcher, quick-start, and receipt trees on
`main` (which that README still references — three deleted figures also
remained hashed in the manifest) and added two things kept here:
`docs/lean_claim_map.md` and `projection_obstruction_20260831_public.zip`
(adopted as shipped; the zip predates this landing and should be regenerated
at the next release build). An earlier wording of this entry called the
situation "a parallel-agent revert"; that mechanism claim was wrong and is
corrected, not preserved. This pass lands the audited, tested v6.3 package
wholesale.

The author-approved pruning is also in force: `scripts/migrate_to_src_po000.py`
and `scripts/sync_code_mirror_from_src.py` (relics of a src-layout migration
never applied), `scripts/check_claim_ir.py` (a dormant gate — its default
input never shipped, it needed a dependency the deposit deliberately excludes,
and nothing invoked it), and `projection_obstruction_20260805_public.zip` (the
stale v6.1-era export) are deleted. The withdrawn-mirror-doctrine note in
`code/README.md` records the deletion. `SHA256SUMS` regenerated: 93 files,
verified; test suite re-run after restoration: 59 passed.

## v6.3 (2026-08-31) — Zenodo republication preparation pass (documentation and receipts; no mathematical change)

Repairs from a full republication audit of the package (all Lean compile claims
below were verified by actually compiling each file standalone:
`cd lean4/mathlib_lab; lake env lean <file>`, toolchain
`leanprover/lean4:v4.34.0-rc1`). The version stays v6.3: no theorem, proof,
claim status, or claim ID changed.

- **E8 receipt gap closed:** `po000_l001_projection_transfer.lean` carried no
  trailing `#print axioms` block; its only audit surface was the aggregator
  `po000_axiom_audit.lean`, which imports sibling modules by name and
  currently compiles in **no** context (the old lake home is retired), so
  E8's axiom report was backed by no green receipt. The file now ends in its
  own block (verified: exit 0, 4 reports — `transfer`,
  `transfer_of_lipschitz`, `tensor_subadd`, `transfer_product_KPi_three` —
  all within `propext` / `Classical.choice` / `Quot.sound`).
- **Lean estate documentation rebuilt against reality:** `lean4/README.md`
  previously named a retired `research_programs/004_...` lake home and the
  nonexistent `PaperPO000` namespace, tabulated 8 of 15 files, and declared
  "flat paths are retired" from a directory of flat paths. It now lists all
  16 files (15 package + 1 estate-only scaffold) with per-file compile
  status from the audit: 13 standalone-green, 2 package-context-only with
  **no current green receipt** (`po000_core.lean`, `po000_axiom_audit.lean`),
  and 1 broken parked draft. `lean4/manifest.json` carries the same per-file
  status machine-readably.
- **`po000_beyond_paper_advancements.lean` labelled broken, not repaired:**
  it has no `import` lines yet uses `Real`, `Real.log`, `positivity`,
  `linarith`, `nlinarith`, and fails standalone compilation. It carries no
  ledger claim and is now explicitly labelled a parked draft in the Lean
  README and manifest rather than shipping silently as if green.
- **Paper front matter:** `date` corrected from the v6.2 date `2026-08-10`
  to `2026-08-31` (Table 0.1, the change log, and the status block already
  said 2026-08-31).
- **Paper prose:** the two retired `PaperPO000.L001_*` lake-module names
  (§5.6 and the Compliance Note's Mechanization status) replaced by the real
  flat files and namespaces (`ReplicaHierarchy`, `ProjectionTransfer`), with
  the retirement recorded in place; "FDA" glossed in plain words at both
  occurrences (authority-decision layer); "Anomalons" and "trinity map"
  given plain-word glosses at first use.
- **Data and Code Availability rewritten for this deposit:** the section
  described the superseded v6.1 80-file archive (`004_`-prefixed filenames,
  `verify_po000_release.py` — a script not in this tree). It now describes
  the actual v6.3 deposit: current filenames, l004/l005 folded in (the
  "Repository head beyond the deposit" paragraph is discharged and removed),
  verification via the test suite and `scripts/regen_sha256sums.py --check`,
  and the old public zip marked historical.
- **`SHA256SUMS` regeneration:** the committed manifest was an unlabelled
  fossil of the v6.1 staging tree — 16 entries named files that do not
  exist, 26 present files were unlisted, and 10 listed files had hash
  mismatches as measured against the working checkout on 2026-08-31 (6 of
  the 10 are `.bat` files, so that count is checkout-dependent: line-ending
  conversion moves it; an earlier draft of this entry said 13, which did
  not reproduce and is corrected here). `scripts/regen_sha256sums.py` (new,
  stdlib-only,
  deterministic) regenerates it over the actual deposit tree and verifies it
  with `--check`; the manifest must be regenerated as the final assembly
  step of the deposit.
- **Claim ledger (md):** paper filename corrected (was
  `projection_obstruction_paper.md`); six body-only sync rows (`PO-002`,
  `PO-003`, `PO-004`, `PO-005`, `GS-000`, `GS-001`) pruned with an in-place
  record because those identifiers no longer occur in the v6.3 body, per the
  section's own rule; the sealed-repository source-freeze citation replaced
  the floating commit reference with release tag `sealed-derivation-v1`
  (commit `3100c4e`); `anomalonpy` glossed.
- **Claim ledger (yaml):** `paper_file` corrected; all 42 retired
  `omega_research`/`omega_engine` evidence paths repointed at the real
  `code/` and estate `lean4/` locations (every repointed target verified to
  exist), with the repointing recorded in the header.
- **Package documentation:** root `README.md`, `code/README.md`,
  `public_export/README.md`, and `docs/quick_start.md` rewritten against
  the actual tree — v6.3, the real paper title and filenames, the real
  notebook names, `code/` + `code/tests/` layout (the advertised `src/po000/`
  and root `tests/` directories do not exist), current programme key
  `projection_obstruction`, and dead links removed. `pyproject.toml`
  version set to 6.3.0 and its pytest/packaging configuration pointed at
  directories that exist.

## v6.3 (2026-08-31) — §7.4 mechanized; S13 settled negatively; S14 closed; reference honesty pass

- **S15 closed:** `po000_l004_observer_visibility.lean` (new, 14 declarations)
  mechanizes Propositions 7.4.3--7.4.5 and Corollaries 7.4.6--7.4.7 — the
  abstract layer over arbitrary seminormed edge fibers with contractive
  observers, and both witnesses with their defect families realized from
  explicit sections. Compiled standalone against the pinned `mathlib_lab`
  toolchain (`leanprover/lean4:v4.34.0-rc1`), exit 0; every `#print axioms`
  report within `propext` / `Classical.choice` / `Quot.sound`; no `sorry`.
- **S13 settled in the negative (new result):** Proposition 7.4.7-B exhibits a
  coupled two-edge carrier (zero restriction maps through a shared overlap
  fiber) with full coverage and a nontrivial joint watcher kernel on every
  edge, where All-Green at any section still forces `I(s) = 0`. Joint-kernel
  triviality is sufficient but not necessary. Mechanized
  (`Coupled.allGreen_forces_zero` et al.) with an inline replay.
- **S14 closed (new result):** §7.4.12 gives the missing `Φ > 0` side — on the
  scalar coupled gauge, `ω = (1, -1)` has exact quotient obstruction `Φ = 2`,
  lower bound by the triangle inequality, attained at the zero repair, `ω` not
  exact. Mechanized (`QuotientWitness.*`) with an inline replay.
- **Theorem 4.2 items 2--3 mechanized:** `po000_l005_weighted_hierarchy.lean`
  (new, 7 declarations) machine-checks the weighted singleton core
  (`singleton_aggregator_linear`, `singleton_weight_pos`), the RE4 orbit weight
  identification (`orbit_weights_equal`), and the §4.5 counterexample
  arithmetic. The full-edge-set assembly remains prose via the mechanized D2
  decomposition.
- **Unpublished-reference honesty pass (author-requested):** references [6],
  [7], [8], [10], [11], [12], [13] are unpublished manuscripts or series
  labels and are now annotated as such; §1.3 and §4.6 no longer lean on [7] or
  [8] — the consumed cores are mechanized in-package, and those citations are
  provenance/orientation only. Publicly deposited [5] and the external
  references are unchanged. **Deferred:** inlining the actual content of the
  unpublished references as prose/code/Lean, per the author, is future work.
- **Ledger sync:** claim ledger (md) rows D3, D4, D6, H3--H7 upgraded to name
  their Lean bindings; new rows H8 (7.4.7-B) and H9 (§7.4.12); the canonical
  Lean bindings paragraph now names the post-reorganization estate path
  with a correction note. YAML ledger: `canonical_version` v6.3, stale
  `lean_sources_directory` fixed, H-entries updated, H8/H9 appended, and the
  pre-existing md/yaml H-numbering offset is now recorded in the header rather
  than silently renumbered.
- **Front-matter drift fixed:** the publication note said v6.1 while the front
  matter said v6.2; both now read v6.3 with the drift recorded in place.
- **Data availability honesty:** the v6.1 Zenodo archive description is
  unchanged; a note marks the two new Lean modules as repository evidence not
  yet in any deposit.
- **GTLA retirement pass (author directive, 2026-08-31):** the GTLA governance
  framework is retired (its paper to be republished as a dead paper); its
  authority rules now live in the CODA discipline documents at the FDA level.
  All GTLA/GTOC references in the paper are replaced by plain-language
  statements of the actual requirement: the front-matter authority clause and
  the Compliance Note's authority status now spell out the authorization
  record in words; the formalization firewall and layer fence drop framework
  acronyms; the compliance note is retitled with the rename recorded in place;
  the LGGR III companion title is marked historical; and the mechanism
  inventory gains a preface explaining what the slot vocabulary is and where
  it is defined. House terms that remain are explained where they stand.

## 2026-08-18 — estate Lake roots, not a green build

WD and PO have `lakefile.lean` homes under
`lean4/research_programs/`, toolchain `leanprover/lean4:v4.34.0-rc1`,
mathlib from the local `mathlib_lab` package, every on-disk `.lean`
file listed as a root (205 and 24). Affine obstruction and several
other PO Mathlib modules now build. Full PO `lake build` still fails
(stale `l001a_*` imports, matching-skeleton `Finset.sum`,
`po000_beyond_paper_advancements.lean`, three olean write failures).
This does not revive the 2026-07-30 `omega_engine/lean4` `PaperPO000`
GREEN line below. A003 stays open.

## v6.0 draft (2026-07-30) — `/paper-build` artifacts

Author-invoked final artifact build (; no Zenodo mint).

> **Retired paths (annotation added 2026-09-03; the record below is historical
> and is left as written).** `omega_engine/lean4` and the `PaperPO000` lake
> target no longer exist. The house paper kit moved from
> `omega_engine/research/published/_kits/obstruction_paper_kit/` to
> `coda_university/_kits/obstruction_paper_kit/`, which is where
> `obstruction_preamble.tex` and `build.sh` live now.

- **Lean 4 hard gate:** `cd omega_engine/lean4 && lake build PaperPO000` — GREEN
  (1308 jobs), toolchain `leanprover/lean4:v4.31.0-rc1`, zero `sorry`/`admit` on
  `004_po000_*.lean`. Load-bearing `#print axioms` restricted to
  `propext` / `Classical.choice` / `Quot.sound` (or none).
- **PDF/TeX:** house style via
  `omega_engine/research/published/_kits/obstruction_paper_kit/obstruction_preamble.tex`;
  pandoc + dual `pdflatex` exit 0; **39 pages**.
- **Release zip:**
  `build_artifacts/000_projection_obstruction_2026-07-30.zip`
  (SHA-256 `b35d3e55163ed30fe7deee8e1df4ebd21181b85274a6b9eff4fe4e27439d96f7`).
- **Structural release verify:**
  `verify_po000_release.py --no-python-gates` on the staging root — **pass**
  (required files, SHA256SUMS, independent certificate verifier). Full
  Python gates (ruff/mypy/`-m po000_projection_obstruction.artifact_bundle`)
  remain pre-existing package-layout debt, not a PDF/tex failure.
- **Receipts:** `publication_hashes` now include pdf/tex/metadata when present
  (`code/replay.py`) so `verify_certificate.py` stays closed after build.

## v6.0 draft (2026-07-30) — Discovery docs, falsification sandbox, paper-build prep

Republication packaging pass (Track A). No load-bearing theorem statement changed.

- **Zenodo discovery copy filled.** `docs/descriptions.md` now carries a Primary
  Description (abstract + why-care + non-claims + closed forms + DOI chain) and a
  Secondary 1-minute summary. `docs/keywords.md` lists deposit keywords and
  explicit anti-keywords (internal branding / retired GT\* acronyms).
- **Tier-1 quick-start repaired.** `docs/000_quick_start.md` uses relative links
  (no `file:///`), the correct pytest command
  (`python -m pytest tests -q -p no:debugging`), and the closed-form table
  (Bell $1/\sqrt{2}+1/4$, TFIM $\nu_e=2|J|$, short-time bound, tripartite $I=6$).
- **Interactive Falsification Sandbox added.** New module
  `code/falsification_sandbox.py`, tests `tests/test_falsification_sandbox.py`,
  notebook `jupyter_notebooks/004_falsification_sandbox.ipynb`, and launchers
  `public_export/run_sandbox.bat` / `.sh`. Deliberate breaks: unsigned Bell
  formula at negative $\theta$, max aggregation vs edge additivity, short-time
  bound outside the near-zero window, raw $I$ vs watched $J$ without observers.
  All expected failures trip above $10^{-12}$.
- **Public export README rewritten** to match the real package layout (figures,
  notebooks, verifiers); stale math-spine / single-test paths removed.
- **Top-level README** updated with DOI chain, sandbox links, and the stdlib
  `code/` shadow note for pytest.
- **Paper-build prep drafts** under `docs/paper_build_prep/`:
  `BUILD_CHECKLIST.md`, Zenodo metadata draft, release notes/readme drafts,
  reproduction requirements, dual-license notice, Lean axiom + environment
  receipt templates. These are **drafts for `/paper-build`**, not a completed
  build or Zenodo mint.
- **Claim→code map** extended with FS1–FS4 sandbox rows.

## v6.0 draft (2026-07-30) — Fourth-Pass Red-Team Repairs

External red-team review of the v6.0 packet returned `HOLD — CORE MATHEMATICS GREEN,
RELEASE BUNDLE RED`. Two repairs below address its mechanically checkable findings.
One further finding it raised is recorded as declined, with reasons.

- **Two-qubit example now covers both signs of $J$ (§6.1).** The derivation was fenced to
  $0<Jt\le\pi/4$ and the displayed result read $D_{12}(\pi/(8J))$, so the negative-$J$
  case was never covered. The exact formula is now $D_{12}(t)=2|cs|+2c^2s^2$ on
  $|Jt|\le\pi/4$, with an explicit argument that the two eigenvalues $c^2s^2\pm cs$
  exchange roles under $cs<0$ and leave the trace norm unchanged; the display reads
  $D_{12}(\pi/(8|J|))$. The inline replay now runs both $\theta=\pm\pi/8$ and uses
  $2|cs|+2a$. **The 2026-07-29 entry below claimed this correction, but only the
  surrounding prose had been updated — the displayed equation still carried $\pi/(8J)$.
  This entry completes it.** Verified: the previous unsigned formula returns
  $-0.4571$ at $\theta=-\pi/8$, a negative trace norm, so the repair was required
  rather than cosmetic. Both signs now return $0.9571067811865476$.
- **D8 narrowed to what is proved.** The row claimed a `PROVEN TYPE DISTINCTION /
  FINITE CERTIFICATE` over $I$, $\Phi$, and a repair cost $R$ that this paper never
  defines, deferring to an unlocatable "Paper 016". D8 is now scoped to the $I$-vs-$\Phi$
  non-interchangeability the paper actually establishes; $R$ moves to new row **D8a**,
  typed `OUT OF SCOPE / NOT ESTABLISHED HERE` with a definition-and-locator obligation.
  The §4.3.1 prose no longer cites "Paper 016" and states plainly that $R$ is not defined
  here and that nothing depends on it.
- **Stale body-only ID removed.** The claim-ledger "Body-only ID sync" section registered
  `PKT-20260722-RES-EPOCH19`, which occurs **zero** times in the paper body, so the
  section failed its own stated purpose. Removed; `PO-000` (20 body occurrences) is
  retained, and the section now states the rule it enforces.
- **Data and Code Availability section added.** The review could not locate the
  mechanization artifacts from the four-file packet it was given. They were always in the
  archive, not a private repository: 4 Lean sources, the `lake build` + `#print axioms`
  receipt, a 15-module Python package with 15 test modules, a machine-readable run
  receipt, two independent verifiers, and a 49-file `SHA256SUMS`. The new section states
  this, gives the one-command verification path, types the inline NumPy replays as finite
  floating-point replays rather than exact certificates, and records the concept and
  preceding-version DOIs.

**Claim-ID body index removed (operator ruling 2026-07-30).** The 47-row
`claim-id-body-index` appendix, which sat after the references, has been deleted along
with its section separator. The review flagged it as repository packaging rather than
scholarship; the operator ruled that it is needed **only as a reference during paper
development**, on the basis that papers are heading for storage as database pieces
reassembled at print time, at which point an in-paper enumeration is redundant rather
than noisy. The **claim ledger is the home and the authority** for claim IDs, so
the paper is not required to enumerate them and every row of that appendix already
pointed at the ledger as its home. Recorded in the `paper-release` skill as checklist
item 6b and enforced by `scripts/paper_preflight.py` gate `G8a-claim-id-index`: WARN
during development, BLOCK under `--strict`. This supersedes the earlier reading of
compliance §5a under which claim-ID ownership was discharged by an in-paper index.

**Declined, with reasons.**

- *"Rebuild the mathematical spine."* No `000_projection_obstruction_math_spine.md`
  exists in this programme, and the release archive contains no spine file. The critique
  of that artifact is sound in itself — $n_\Pi=I-\Pi$ does collapse the three residuals
  this paper separates, and $[H_e,n_\Pi]$ is undefined for nonlinear $\Pi$ — but no such
  document is part of this deposit, so there is nothing here to rebuild or withdraw.

## v6.0 draft (2026-07-29) — Third-Pass Release-Hold Repairs

- **Geometry criterion repaired:** Narrowed Theorem 3.1 to the declared affine-chart vector field $b=D\phi\cdot D\Pi A$; moved the ambient derivative formula to a separate calculation; and typed the ambient-to-chart nondegeneracy bridge as open S1 rather than a proved sufficient test.
- **Non-invariance proposition corrected:** Replaced the stronger Proposition 3.B reading with the exact requirement for a projected-motion witness $\Pi(T_tm)\ne m$; non-invariance alone now only shows in this model that retraction is applied off manifold.
- **Observer gap semantics corrected:** Renamed §7.4's scalar to the best-single-observer visibility gap $\Lambda_{\max}$ and added the edgewise observation/contraction plus single-observer fragmentation decomposition.
- **Quotient scope fenced:** Stated the finite-dimensional/closed-range requirement for quotient exactness; Banach presentations no longer silently identify zero distance with image membership.
- **Python release object hardened:** Updated the replay schema to `po000.mechanization_run.v3`, made aggregate status fields required and model-validated, renamed the higher-differential API to `AdmittedComplexCoboundaryProblem`, kept `CoboundaryProblem` at the d0-only level, and added decomposition/API failure-path tests.
- **Publication cleanup:** Corrected D8 to the positive type-distinction claim, corrected the two-qubit time to $t=\pi/(8|J|)$, removed the lingering reference-matching note and prototype-roadmap wording, aligned §7.4 obligations to S13--S15, and refreshed the Python package version to `6.1.1`.

## v6.0 draft (2026-07-28) — Pass 45 Red-Team Repair

- **Pass45-R1 (Theorem 5.1):** Restored the load-bearing full incident norm $g=\max_v\sum_{X\ni v}\lVert h_X\rVert_\infty$ in the theorem itself and defined the family norms $g_N$ identically in Corollary 5.1.A. Removed the invalid endpoint-only norm.
- **Pass45-R2 (Notation):** Separated the normal projector $Q_e:=I-P_e$ from its rate vector $n_e:=Q_eL_e$, with $\nu_e=\lVert n_e\rVert_1$, throughout the theorem, proof, examples, appendix, and ledgers.
- **Pass45-R3 (Observer family):** Required the §7.4 watcher index set to be finite and nonempty, making $\max_{\alpha\in A}J^\alpha$ defined, and renamed the combined watcher map $\mathcal Q_e$ to avoid collision with the quantum projector.
- **Pass45-R4 (Claims and placement):** Added dedicated ledger rows for Corollary 5.1.A and §7.4.1--§7.4.7; corrected RE hierarchy pointers and Lean bindings; synchronized ENC-0764--ENC-0769; retained PO-000 Lean sources only in the canonical programme directory.
- **Pass45-R5 (Provenance and evidence):** Recorded concept DOI `10.5281/zenodo.18896776` and published v5.6 DOI `10.5281/zenodo.20650922`; typed v6.0 as an unpublished new-version draft; corrected Hall and Haegeman references; and fenced the sibling Python package to finite/symbolic/numerical evidence rather than finite-structural proof.

- Earlier v6.0-draft work accumulated proof, technical, and structural revisions across multiple audits; the numbered Pass 45 items above are the current repair delta.
- Inserted canonical identity block, core kernel chain, and refusal/anti-kernel box in front matter.
- Theorem 3.1 retitled to **Affine Nonlinearity Criterion** ($\boxed{DB \text{ nonconstant} \implies B \text{ non-affine}}$), split into Lemma 3.A and Proposition 3.B, hardened domain condition for unbounded $A$, and enforced residual taxonomy.
- Theorem 4.2 updated to explicit edgewise gauge sum $J_E(x) = \sum_{e \in E} j_e(x_e)$, added observer selection framing, and bound the Lean 4 target to `ReplicaHierarchy.unweighted_sum_of_replicaAdditive_of_singleton_calibration`.
- Theorem 5.1 retitled to **Exact Finite-System Short-Time Lower-Bound Certificate**, fenced to pure/mixed product initial states, added the Schatten norm loss factor $d^{2(1-1/p)}$, restored stable Lemma 5.2/5.3 numbering, and now distinguishes $Q_e=I-P_e$ from $n_e=Q_eL_e$ while using the full incident norm.
- Separated edge-normalized $C(t)/|E|$ and site-normalized $C(t)/N$ density metrics, added detector-local warning callout, and inserted **§5.7 Non-Firing and Boundary Cases** detailing 7 non-firing failure modes.

## v5.8 (2026-07-25) — Projection Obstruction Programme Normalization

- Standardized primary paper identity as `PO-000 — Projection Obstruction Anchor: Product Projections and Exact Short-Time Defect Bounds` (canonical version: `v5.8`, legacy file: `000_projection_obstruction_v5_6.md`).
- Consolidated in-body revision history into this companion change log.
- Fenced Section 7.4 fiber-projection LGGR material as a companion observer theorem.
- Registered open obligation S1 (Product-Retraction Nondegeneracy Theorem for nonconstant derivative hypothesis in Theorem 3.1).

## v5.7 / July 2026 Correction Pass

- Withdrew false full-independence claim for RE1–RE5.
- Theorem 4.2 updated: RE3 gives singleton separability; RE1+RE2+RE3 give weighted $\ell^1$; RE4 controls orbit weights; RE3+RE5 give unweighted sum.
- Replaced Lieb–Robinson proof route with exact finite-system double-commutator estimate ($D_e(t) \ge \nu_e t - 24g^2t^2$) using local interaction norm $g$ (including one-local fields) and local raw rate $\nu_e$, yielding system-size uniformity under Corollary 5.1.A's explicit uniform hypotheses.
- Separated projection residuals from induced cochains and coboundaries.

## v5.6 (June 2026)

- Pre-print revision consolidating $C^2$ retraction non-degeneracy and short-time density lower bounds.
