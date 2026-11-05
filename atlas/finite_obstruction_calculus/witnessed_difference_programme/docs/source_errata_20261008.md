# Corrections to retained sources

Historical files retain their original words, formulae and status claims.
They are evidence of source content, not evidence that those claims hold.
The current manuscript and this register supersede the following claims.

| Source | Error | Correct statement |
| --- | --- | --- |
| FDA component, terminal soundness equivalence | A bad proposal or checker was assumed to force an unsound terminal. A pipeline can refuse it. | Sound checking and valid grants are sufficient for sound authorized terminals under the stated binding assumptions. The converse requires reachability and non-refusal hypotheses and is not proved. |
| CODA component, restricted repair quotient | The allowed repair set $R$ was declared but the quotient used the image of every potential. | When $R$ is a linear subspace, use $C^1/d_0(R)$. For $d_0=I$ and $R=\{0\}$ this quotient is $C^1$, not zero. A closed cochain need not be exact. |
| Prime Algorithms, weighted Hodge decomposition | An ordinary transpose was used as the adjoint for a weighted inner product. | For weights $W_1,W_2$, the adjoint of $d_1$ is $W_1^{-1}d_1^TW_2$. Its coexact image is $\operatorname{im}(W_1^{-1}d_1^T)$ when $W_2$ is invertible. Exact rational projection claims require rational matrix entries and rational weights. |
| WDP generated swarm receipt | Proof and complete-test statuses were assigned without execution. | The generator and its receipt are [withdrawn](source_archive/rejected_verification_2026_10_08/README.md). No theorem or test result is supported by those assigned statuses. |
| WDP general horizon Lean credit | Six credited declarations do not occur in the source. | `NativeFutureCompression.lean` proves the listed horizon-two results. The generalized horizon argument is written mathematics only. |
| WDP historical coverage report | A partial report was offered with a 95% coverage gate. | `manifests/coverage.json` records 150/6004 covered lines and 11/2264 covered branches. It does not establish 95% coverage, or current coverage. |

Two archive files were restored to the exact bytes recorded by their original
manifests: the Gate E JSON receipt's CRLF line endings and the original CODA
SVG from its retained ZIP. The [recovery record](source_archive/rejected_verification_2026_10_08/custody_recovery.json)
identifies both inputs and expected hashes; the displaced derivatives remain
in that directory. No historical expected hash was changed to fit an amendment.

## Detailed corrections from the complete source review

## Retained component packages, manuscripts and responses

These corrections apply to the cited historical bytes. They do not alter the originals, revive withdrawn verification routes or transfer a historical theorem status to the maintained WDP manuscript. Each identifier matches the read-only archive review.

**ARCH-R2-01.** [Historical source](source_archive/coda_component_packages/a/lean4/T02ResidualNonCreation.lean), source lines 25–46. The Lean result separates the residual and authorization predicates on the same object. It does not quantify over arbitrary maps between objects. A constant function into an inhabited authorization constructor exists. Constructor disjointness therefore establishes neither impossibility of remapping nor enforcement of an authorization policy.

**ARCH-R2-02.** [Historical source](source_archive/coda_component_packages/a/code/coda_a_core.py), source lines 440–460. Administrative states do not report mathematical closure reliably. With $d_0=(1,0)^T$, $d_1=(0,1)$ and $x=(0,5)^T$, `pending_lift=True` produces `is_closed=True` although $d_1x=5$. A refusal can conversely mark a closed input as not closed. These fields describe routing decisions; closure requires a separate calculation of $d_1x$.

**ARCH-R2-03.** [Historical source](source_archive/coda_component_packages/coda/code/tests/test_adversarial_obstruction_sheaf.py), source lines 32–123. The tests named for nonabelian gluing, HoTT and infinite search exercise a finite observation collision, a substring rule and a menu of 52 candidates. They establish only the stated fixture behavior. They do not constitute a nonabelian sheaf theorem, a theorem about HoTT, an infinite-search result or an evaluation of a language model.

**ARCH-R2-04.** [Historical source](source_archive/coda_component_packages/coda/code/coda_discipline_core.py), source lines 85–150. The nonnegative-cost guards admit NaN because they test only whether a value is negative. The step-count field also admits noninteger values. Approximate diagonal equality is used where exact zero is advertised, and the public owning array can be made writable again, invalidating a hash derived from its contents. These records are not independent certificates of exact costs, integer counts or immutable data.

**ARCH-R2-05.** [Historical source](source_archive/coda_component_packages/cs_q/verify_deposit.py), source lines 151–174. The archived `--lean` route names `AxiomAudit.lean`, which is absent from both the copied package and its original ZIP. The supplied audit file is `Census.lean`; the corresponding command is `lake env lean Census.lean` from that extracted Lean package. The historical verifier's success claims cannot substitute for running the correct command.

**ARCH-R2-06.** [Historical source](source_archive/coda_component_packages/a/code/cochain_presentation.py), source lines 61–85. The archived A/CS, GTLA, CS-Q and MUR/OR exactness-certificate methods accept a rounded floating witness for a false exactness claim. For $A=(1,1)^T$ and $x=(2^{60},2^{60}+1)^T$, the entries of $x$ are unequal, so $x\notin\operatorname{im}A$, yet the supplied low-precision floating witness passes. These methods do not independently enforce exact rational input. FDA rejects this control. An exact checker must validate its own witness domain, dimensions and binding to the declared problem.

**ARCH-R2-07.** [Historical source](source_archive/prime_algorithm_package/code/oe_prime_algorithms.py), source lines 937–976. The transition evaluator treats an omitted closure or harmonic field as zero and can report `EXACT_CLASS` from either field alone. On a hollow triangle, $(1,0,0)$ has zero closure defect but quotient distance one. Missing diagnostic evidence therefore leaves exactness undetermined; it does not establish exactness.

**ARCH-R2-08.** [Historical source](source_archive/prime_algorithm_package/code/oe_prime_algorithms.py), source lines 867–935. The weighted Hodge routine admits negative weights and can report a negative harmonic squared mass while returning `HODGE_DECOMPOSED`. Its closure and adjoint diagnostics are also assigned zero without checking the returned components. The inner-product interpretation requires strictly positive weights and independently checked decomposition identities; the historical routine does not enforce those conditions.

**ARCH-R2-09.** [Historical source](source_archive/prime_algorithm_package/code/oe_prime_algorithms.py), source lines 1014–1050. `extract_orthonormal_harmonic_basis` returns a rational nullspace basis without orthogonalization. On the face-free $K_4$, its Gram matrix is $\left(\begin{smallmatrix}3&1&-1\\1&3&1\\-1&1&3\end{smallmatrix}\right)$. The result is a harmonic basis, not an orthogonal or orthonormal basis. Rational Gram–Schmidt can produce orthogonal vectors, but unit normalization may require irrational scalars.

**ARCH-R2-10.** [Historical source](source_archive/prime_algorithm_package/code/oe_prime_algorithms.py), source lines 1171–1190. `check_adapter` checks that field names occur in the target record. It ignores their values, the source state and the protected distinctions; every named value may be `False` while it returns `ADAPTER_SOUND`. This is a presence checklist. Its output establishes no semantic relation between source and target and no authorization guarantee.

**ARCH-R2-11.** [Historical source](source_archive/prime_algorithm_package/verify_deposit.py), source lines 254–270. The artifact verifier compares a rebuilt file only when that file exists. A successful command that produces no artifacts can therefore pass the extracted-package comparison. The historical result does not establish that the required outputs were rebuilt. Artifact verification requires existence and content checks for every required output.

**ARCH-R2-12.** [Historical source](source_archive/coda_component_packages/coda/docs/references.md), source lines 30–47. The reference list assigns Zenodo record `20710065` to two different works and uses a draft upload URL for another. The archived CODA `zenodo_metadata.json` also contains a related-identifier record with no identifier. These entries do not establish a one-to-one correspondence between titles and deposited sources. The conflicting identifiers remain unresolved; no replacement DOI is inferred from the titles.

**ARCH-R2-13.** [Historical source](source_archive/coda_component_packages/coda_gtla/coda_gtla_claim_ledger.md.txt), source lines 92–97. The GTLA-06 ledger describes a seal minted from a verified external grant. The actual archived token model accepts a declared, unauthenticated license. Its record checks establish neither an external signature nor the legitimacy of the grantor. The ledger's external-authentication claim is withdrawn.

**ARCH-R2-14.** [Historical source](source_archive/coda_original_source_snapshot/8e03b0928d0689432d42a6fdb1980f3fad072c4c2f6da281dec7a2cc6d5c3f0f.txt), source lines 99–102. Absence of directed cycles does not imply a zero edge-cochain quotient. The directed acyclic triangle $0\to1\to2$, together with $0\to2$, has $\dim(C^1/\operatorname{im}d_0)=1$. The zero-quotient assertion applies when the underlying undirected multigraph is a forest.

**ARCH-R2-15.** [Historical source](source_archive/coda_original_source_snapshot/f4ef46aed4be745be55c50d54619c3911d4a70f541b0348da55874c52e5ba1be.txt), source lines 19–19. The displayed convention is $\operatorname{Tr}(\lambda_a\lambda_b)=2\delta_{ab}$. These generalized Gell-Mann matrices are orthogonal and have Hilbert–Schmidt norm $\sqrt2$. They are orthonormal only after rescaling, or under the explicitly chosen half-trace inner product.

**ARCH-R2-16.** [Historical source](source_archive/wdp_distinct_image_closure_2026_10_05/bytes/g3_g4_meron_field_theorems/meron_spacetime_field_theorems.md), source lines 151–280. The Meron synthesis's established/closed labels are withdrawn. Its asserted zero-mode formula omits the linear $\theta/8$ term appearing elsewhere in the same source; perturbative formulas lose their remainder terms; and 10,000 sampled points are used as a bound over an entire complex polydisk. The negative-mode argument loses factors of $M$ and assumes that one witnessed negative direction describes the whole negative spectrum. A uniform bound by $c\|\Psi\|_\infty^2$ is incompatible with temporal covariance eigenvalues tending to zero. The exact finite Gate E witness remains a counterexample to universal finite-discretization positivity. Gaussian field convergence still requires the stated uniform estimates, a probability interpretation and tightness.

**ARCH-R2-17.** [Historical source](source_archive/meron_model_generation_history/responses/deepseek_sprint6_g3_closure.md), source lines 54–83. For $0<\zeta<1$, the full lattice sum is $\sum_{(u,v)\ne(0,0)}\zeta^{|u|+|v|}=4\zeta/(1-\zeta)^2$. The response instead multiplies two sums excluding zero and obtains $4\zeta^2/(1-\zeta)^2$, omitting both coordinate axes. Its resulting constant is unsupported. It also interchanges a fixed total coupling with $\theta=r/M$. Correcting the sum does not establish the assumed polymer decay or the claimed uniform cumulant estimate.

**ARCH-R2-18.** [Historical source](source_archive/coda_original_source_snapshot/a01721f59cbcceeb3768145e1492ac56d3f7acff4e20f592ad55a16d307895e5.txt), source lines 180–282. The master synthesis supplies no proofs of its claimed physical-time construction, phenomenal-awareness impossibility, classification of every history weight, classical hidden-variable theorem or ontology of unobserved distinctions. Its generic mechanism table also changes the meanings of several symbols without compatible definitions. These statements are withdrawn as results. The file remains a historical outline; only separately stated and proved model-specific results carry forward.

**ARCH-R2-19.** [Historical source](source_archive/coda_original_source_snapshot/e0038457914f2e7d348640276222f385b90ae29a083e7d5d084a263b7c4521c2.txt), source lines 140–145. The threshold relation $|x-y|\le3/2$ is not transitive: $0$ is related to $1$, and $1$ to $2$, but $0$ is not related to $2$. Its connected-component closure is an equivalence relation, but is a different relation. Likewise, exhibiting a carrier does not supply a tally or prove finite enumeration. A finite-dimensional rational vector space is usually infinite, so finite-search arguments do not establish minimizer attainment over all its rational points.

**ARCH-R2-20.** [Historical source](source_archive/coda_original_source_snapshot/e0038457914f2e7d348640276222f385b90ae29a083e7d5d084a263b7c4521c2.txt), source lines 263–266. Additivity on disjoint positive sectors does not determine a norm on signed vectors. The norm $J(x,y)=\max\{|x+y|,|x-y|/2\}$ agrees with $x+y$ on the nonnegative quadrant, but $J(1,-1)=1$ rather than $2$. A weighted-$\ell^1$ conclusion needs an additional sign-invariance condition or the corresponding additivity on signed supports. A single symmetry orbit forces equal coordinate weights; multiple orbits do not prohibit declaring equal weights.

**ARCH-R2-21.** [Historical source](source_archive/coda_original_source_snapshot/655a90322e149f40255f31f2551507b719530967ca7cda8e36d1aeb46b628dd4.txt), source lines 300–431. A nonzero signed cycle period need not be realized by two directed paths with the same endpoints. In the graph $a,b\to c,d$, assign value one to $a\to c$ and zero to the other edges. The alternating cycle has nonzero period, but every directed path has at most one edge. The general conclusion is failure of a vertex potential. A directed-path comparison needs explicit path witnesses or suitable common-root reachability. Literal `##`, doubled escapes and corrupted symbols in the historical displays are transcription defects.

**ARCH-R2-22.** [Historical source](source_archive/coda_original_source_snapshot/576d1612d55c64d11344d79ca1457e4a00dc8ddc3c77122d5b45bbdfc5d1da09.txt), source lines 368–381. Nilpotence of the degree-zero Lie algebra does not imply nilpotence of its action on other degrees: an abelian Lie algebra may act nonnilpotently. In finite-dimensional real or complex settings, the matrix exponential and divided-exponential series are defined analytically without nilpotence. A formal gauge-action construction instead needs a compatible filtration or other convergence condition on the whole action.

**ARCH-R2-23.** [Historical source](source_archive/coda_original_source_snapshot/1de647f0b3a5c90fbec1549ecd4703e799fe54ffc666650f21cff0ecdb278251.txt), source lines 573–1430. A sheaf of five status labels does not by itself define the claimed additive $H^1$ obstruction. That construction needs suitable abelian coefficients, or an explicitly different nonabelian or torsor construction. The source's refusal to infer a proposition or its negation from missing evidence also does not refute excluded middle: classical logic permits incomplete knowledge. Both issues remain separate from the outline's proposed mathematical programme.

**ARCH-R2-24.** [Historical source](source_archive/coda_component_packages/q/docs/coda_q_legacy_ledger.md), source lines 99–112. The Q legacy ledger adds positive quotient-distance and product-distance bounds to set-theoretic factorization statements without defining the required normed quotients or comparison constants. Its Boolean equivalence is not an optimization duality theorem and establishes no duality gap. Those quantitative annotations are withdrawn; only the stated factorization implications remain. The prose count of nine unregistered rows also conflicts with the twelve rows displayed.

**ARCH-R2-25.** [Historical source](source_archive/coda_original_source_snapshot/49c1a90173125c8340d8bf31c8800ba47b7165951cfd27c36c5bbb1bc929dbc4.txt), source lines 68–220. The historical ledger retains disjointness and exhaustiveness claims in C24 and N18 that conflict with its own correction R21. Only the corrected theorem characterization applies. Its criticism of a universal theorem having an existential falsifier is also mistaken without a domain mismatch: one admissible counterexample is exactly what refutes a universal statement over that admissible class.

**ARCH-R2-26.** [Historical source](source_archive/coda_original_source_snapshot/a347551c50364c3430049e47da68aea09c9c6dafc916f3770cba225ada39561b.txt), source lines 29–230. The master observer synthesis does not establish its combined `DERIVED/PASS` table. A differential satisfying $d_1d_0=0$ cannot also acquire nonzero $d_1d_0$ without changing the mathematical structure. Edge data $f_j-f_i$ are exact and cannot witness a nonzero quotient class. A set-valued presheaf supplies neither vector cochains nor a quotient norm. Nonisomorphic spaces may still admit transport maps, such as $\mathbb R\hookrightarrow\mathbb R^2$. The consciousness, agent-validity and universal-authorization conclusions are not derived by these definitions. General interference formulas additionally require the measurement coefficients.

**ARCH-R2-27.** [Historical source](source_archive/coda_original_source_snapshot/35044e09f649a00f50bf050acdbbc5ab685df45e553a5d24b36a8467b89be05e.txt), source lines 214–503. Placing every composite in $V_A\otimes V_B$ already assumes the relevant local-tomography dimension. Two rebits have a ten-dimensional real symmetric operator space, whereas $3\times3=9$; their full composite is outside that declared class. The same outline's torsion formula is false: $\mathbb Q/\mathbb Z$ is divisible, while $\bigoplus_n\mathbb Z/n\mathbb Z$ is not. The correct decomposition is $\mathbb Q/\mathbb Z\cong\bigoplus_{p\text{ prime}}C_{p^\infty}$. The interference identity is $|a+b|^2-|a|^2-|b|^2=2\operatorname{Re}(\overline a b)$; the broken source display changes its arithmetic.

**ARCH-R2-28.** [Historical source](source_archive/coda_original_source_snapshot/35044e09f649a00f50bf050acdbbc5ab685df45e553a5d24b36a8467b89be05e.txt), source lines 194–1140. No decision procedure or effective model bound supports the outline's decidability claim. A separate finite construction also cannot refute a statement about which declarations a particular Lean module contains. Quantum experiments with a single context or commuting measurements may have global sections, so a nonzero contextuality obstruction is not necessary for every quantum empirical model. The 2011 global-section account and later cohomological witnesses are distinct results. The source's open classical countermodel is not promoted to an established theorem by its later citation rule.

**ARCH-R2-29.** [Historical source](source_archive/coda_original_source_snapshot/9d76d181437080621025e995480a54130577b5352803f5639d6ec0722a321597.txt), source lines 109–123. Pure equality still permits invariant structures: empty and complete adjacency, and discrete and indiscrete partitions. A nonselection theorem must specify a target with no fixed point and exclude these trivial choices. The full symmetric group is not transitive on $X^k$ for $|X|>1$ and $k\ge2$, because equality patterns are invariant. Invariant subsets are unions of orbits without that transitivity assumption.

**ARCH-R2-30.** [Historical source](source_archive/coda_original_source_snapshot/9d76d181437080621025e995480a54130577b5352803f5639d6ec0722a321597.txt), source lines 845–953. Three ordered points already distinguish flat from nonflat composition: choose adjacent scalar restriction maps $1,1$ and direct restriction $0$. Four points are needed only for a nonvacuous test indexed by a spatial quadruple. A fixture with two square-zero operators and a failed mixed law does not refute $\Lambda=0\Rightarrow$ the mixed law unless the same fixture also satisfies $\Lambda=0$.

**ARCH-R2-31.** [Historical source](source_archive/coda_original_source_snapshot/ab0c18a5ab547f69d216ff8f1c21476781bc576fb10a6af9e27596fd9da17d04.txt), source lines 66–103. Acyclicity does not make an arbitrary length truncation composition-closed: the two-edge chain fails at cutoff one. A cutoff at least the longest directed path suffices in a finite acyclic graph. Conversely, weighted nilpotence does not imply graph acyclicity over arbitrary coefficients; zero weights or cancellation can hide cycles. The vertex-potential criterion requires signed cycle sums or suitable rooted path comparisons. Equality of $e^{-\beta A}$ implies equality of real actions only when $\beta\ne0$.

**ARCH-R2-32.** [Historical source](source_archive/coda_original_source_snapshot/ab0c18a5ab547f69d216ff8f1c21476781bc576fb10a6af9e27596fd9da17d04.txt), source lines 260–263. The finite-support nonnegative-real semimodule construction is a monad on `Set`, not on `FinSet`: its value on a singleton is already infinite. Its Kleisli category can be restricted to finite objects, yielding finite nonnegative matrices. Such matrices are not automatically substochastic; the one-state matrix $(2)$ is a counterexample. Substochastic kernels require an explicit sum-at-most-one condition.

**ARCH-R2-33.** [Historical source](source_archive/coda_original_source_snapshot/bd26a348d15096671aed5148aae7393b4de4a6272f545b0a21c809ff54d37ad0.txt), source lines 126–130. A witness in $B\setminus A$ establishes $B\nsubseteq A$. It establishes $A\subsetneq B$ only after $A\subseteq B$ has also been proved. The awareness ledger's separating witnesses therefore do not preserve proper-inclusion claims after the proposed containments fail. The surviving statements are the individual existential separations.

**ARCH-R2-34.** [Historical source](source_archive/general_media_2026_10_06/bytes/causal_ai_is_not_authority_v001.md.txt), source lines 157–494. The causal-AI example shows that its chosen terminal answer does not factor through the displayed report. It does not establish the nonexistence of every observer-independent functor; the relevant categories are not defined, and a constant refusal map remains possible. The quotient formulas additionally need linear coefficient objects and representative invariance, such as $d_1d_0=0$. Distance zero implies exact repair only under a suitable closed-image or attainment hypothesis. Authorization remains a separately declared decision policy.

**ARCH-R2-35.** [Historical source](source_archive/general_media_2026_10_06/bytes/linkedin_article_001_what_the_hell_is_an_observer_v001.md.txt), source lines 50–697. A two-outcome measurement need not act on a two-dimensional system; a $2\times2$ density matrix describes a two-level system. The essay's numerical triangle quotient values also require the stated unit edge weights and edge-$\ell^1$ product norm. Quotient-zero/exactness needs the linear and closed-image hypotheses. Separately repairable edges need not admit one simultaneous repair. The evaluator reports checked results; an authorizer makes the permission decision. The archived wording that assigns authorization to the evaluator is withdrawn.

**ARCH-R2-36.** [Historical source](source_archive/toric_code_chapter_23_import.md), source lines 40–142. For the standard $L\times L$ toric code with $L\ge3$ and $n=2L^2$ qubits, the binary Pauli space has dimension $2n=4L^2$, the syndrome kernel has dimension $2L^2+2$, and the stabilizer subspace has dimension $2L^2-2$. The logical quotient is four-dimensional and has 16 elements, not four. Stars lie in the row space of the displayed incidence matrix. A simple torus cycle need not bound a disk. The bounded-error condition concerns admissible pair differences; a distance relative to tolerated subgroup $B$ is minimized over $\ker Q\setminus B$, with value infinity for an empty set. Component weight counts overlapping X and Z coordinates separately. The claimed halved lattice size and its cost consequences are withdrawn. The byte-identical imported chapter has the same corrections.

**ARCH-R2-37.** [Historical source](source_archive/toric_code_chapter_23_import.md), source lines 26–479. Current syndrome, XOR of syndromes and a stacked measurement transcript are different reports. Logical Pauli operators remain in the full syndrome kernel, which is larger than the stabilizer subspace. Requiring a full-syndrome row to be one on an element of its kernel is inconsistent. Full measurement rank is not necessary for every bounded-error problem: with no allowed error, no measurement is needed. The asserted adaptive rank and cost equalities do not follow. The proposed greedy ratio $c/(c-0)$ is constant for positive costs and undefined at zero; it does not select a minimum-cost basis.

**ARCH-R2-38.** [Historical source](source_archive/toric_code_chapter_23_import.md), source lines 596–822. A Lieb–Robinson estimate gives a quantitative tail, not an exact causal cutoff, and an upper bound on reach is not an attained reach. The displayed boundary equation adds elements of different chain degrees. Unequal independent noisy samples do not imply different conditional distributions. Under finite full-support bit-flip noise, distinct protected answers cannot be recovered exactly from overlapping report supports. Repetition therefore needs an explicit confidence target and tie rule; no universal $R\ge L$ threshold follows. Component-weight Pauli counts use $2n$ coordinates.

**ARCH-R2-39.** [Historical source](source_archive/locality_and_smearing/trotter_cochain_extinction_derivation.md.txt), source lines 143–512. At $r=1/10$, $r^2+4r+8=841/100$, not $281/100$. The consistent small-$r$ expansion printed later is $-r^4/64+r^5/64-5r^6/512+O(r^7)$, not the earlier expression beginning $-r^4/4$. The stated response matrix has dimension $8M$; the printed positive multiplicities give four at $M=1$, contradicting the table's three. These finite entries do not prove a general spectral pattern. The expanded quadratic form must retain both test-profile factors and both time indices.

**ARCH-R2-40.** [Historical source](source_archive/locality_and_smearing/trotter_cochain_extinction_derivation.md.txt), source lines 636–990. For a single spatially uniform, normalized staggered negative mode, put $N=2M$, $A_M(x)=N^{-1}\sum_j(-1)^j\Psi(j/N,x/L)$ and $\overline A=L^{-1}\sum_x A_M(x)$. Its contribution is $q_-=-\mu_M|\overline A|^2/N$, giving $|q_-|\le\mu_M\|\partial_\tau\Psi\|_\infty^2/(32M^3)$. This conditional rank-one estimate does not describe an unproved full negative spectrum. The source's Parseval identity uses the wrong multiplier, and its kernel average converges to the zero Fourier coefficient rather than the kernel itself. At fixed $L$, $\sin(2\pi Lx)$ vanishes on the sampling grid while having positive continuous covariance under the claimed positive kernel. A uniform fixed-grid comparison on all smooth profiles therefore fails.

**ARCH-R2-41.** [Historical source](source_archive/locality_and_smearing/trotter_cochain_extinction_derivation.md.txt), source lines 1057–1490. A strict positivity threshold must exceed the error-to-margin ratio; a ceiling permits equality when that ratio is an integer. Fermionic Wick factorization does not make every observable Gaussian: a single occupation variable is Bernoulli. A Fourier projector has entries $P_{jk}=N^{-1}\sum_{p\in S}e^{2\pi i p(j-k)/N}$ for distinct retained residues, not the printed $jk$ phase. Harmonic projection represents cohomology and discards nonzero coexact classes in $C^1/\operatorname{im}d_0$. Low-pass filtering need not annihilate exact cochains, and periodic constant cochains need not be coboundaries. The asserted subdivision invariance and conversion to a cochain norm require explicit typed, norm-compatible maps.

**ARCH-R2-42.** [Historical source](source_archive/coda_component_packages/a/jupyter_notebooks/002_moving_leftovers_with_a_linear_map.ipynb), source lines 1–150. For a general linear map $C$, equal residuals mean $x-y\in\ker(I-C)$, not $x-y\in\operatorname{im}C$. The latter equivalence holds when $C^2=C$. For $C=2I$, every difference lies in the image, but the residual map is $-I$ and distinguishes every pair of distinct inputs. The notebook's projection example remains valid under its idempotence hypothesis.

**ARCH-R2-43.** [Historical source](source_archive/coda_component_packages/foc/jupyter_notebooks/002_when_the_calculator_is_wrong.ipynb), source lines 1–175. Strictly positive coordinate weights make the ambient weighted-$\ell^1$ expression a norm and are the calculator's input policy. They are not necessary for every quotient norm. With weights $(1,0)$ and repair subspace $\operatorname{span}(0,1)$, the quotient still has the norm $|x|$. The ambient norm, quotient norm and implementation policy are distinct assertions.

**ARCH-R2-44.** [Historical source](source_archive/coda_component_packages/fda/jupyter_notebooks/001_the_five_fields_and_seven_guards.ipynb), source lines 1–260. The FDA notebook directly supplies acceptance, replay and skeleton-preservation flags; related CS and OR notebooks supply cofinality or source-authority flags and certificate names. Their examples verify a conditional rule on those inputs, not the inputs' authenticity. The Prime tamper example likewise detects an unrepaired hash change; detecting an internally rehashed replacement needs an independently retained checkpoint. Printed fixture success does not establish either external grant verification or general tamper detection.

**ARCH-R2-45.** [Historical source](source_archive/meron_model_generation_history/responses/deepseek_g3_field_theorem_response.md), source lines 1–114. The initial G3 response does not prove its stated conditional field theorem. Subtracting the product of means does not remove every diagonal Lehmann term: a nonconstant observable commuting with the Hamiltonian retains positive thermal variance. The proposed time-ordering argument is invalid. Exponential decay does not remove a contact cusp, and $\theta=0$ is the infinite-temperature limit in these conventions. At that limit the same-site temporal covariance is $1/4$ for every pair of labels, refuting uniform exponential decay in the unscaled temporal index.

**ARCH-R2-46.** [Historical source](source_archive/meron_model_generation_history/responses/deepseek_final_convergenced_theorem.md), source lines 31–103. The response headed “Fully Corrected” still has an incorrect spectral-positivity argument. Its full-frequency commutator spectral density is odd and has negative weight at negative frequency, not a nonnegative measure on the whole line. Positivity follows from a correctly paired positive-energy expression. Its Matsubara denominator also divides an already normalized frequency by $\theta$ again. The thermal cross term is needed for the periodic time expansion. Exponential microscopic spatial clustering is compatible with macroscopic spatial white noise, not smooth spatial sample paths.

**ARCH-R2-47.** [Historical source](source_archive/meron_model_generation_history/responses/deepseek_g3_gate3_exact_proof.md), source lines 82–120. Sections 1–4 correctly give $K_0(s)=1/4$ and zero nonzero-frequency coefficients. Section 5 omits the Gibbs-state cross term. For $n\ne0$, $\int_0^1t^2e^{2\pi int}\,dt=(2\pi in)^{-1}+(2\pi^2n^2)^{-1}$; it is not the printed purely real integral. A two-level thermal example gives $1+\tfrac12\theta^2(t^2-t)+O(\theta^4)$, displaying the missing linear term. The asserted positive-temperature coefficient does not follow from the source's expansion.

**ARCH-R2-48.** [Historical source](source_archive/meron_model_generation_history/responses/deepseek_g4_covariance_response.md), source lines 54–217. The G4 response reverses the operator degrees: $P_x$ contains a quartic density interaction, while the source exponent is quadratic. The interacting density covariance is not a free one-particle propagator. At $q=1,z=0$, the normalization leaves $X=2^L$, not an intensive value. A boundary-hop sign depends on occupations, not just even $L$. Its proposed volume-independent double spatial sum equals $L/4$ at $\theta=0$. The final covariance also drops one of the two time-dependent test factors. The response's exact/proved labels are withdrawn.

**ARCH-R2-49.** [Historical source](source_archive/meron_model_generation_history/responses/deepseek_g4_followup_response.md), source lines 19–149. The G4 follow-up still has a factor-of-two error in the local spin conversion. With the standard neighboring-site convention, $K_{x,x+1}=(Z_xZ_{x+1}-X_xX_{x+1}-Y_xY_{x+1})/4$; the displayed XY coefficient is half this value. Boundary parity conventions require separate treatment. The response repeats the incorrect ground-state interpretation of $\theta=0$ and the unjustified exponential temporal Fourier decay. Nonconservation of a local observable alone does not identify the spatial row-sum spectral weight. Distinct time arguments in the test profiles must remain distinct.

**ARCH-R2-50.** [Historical source](source_archive/meron_model_generation_history/responses/deepseek_sprint1_exact_cusp.md), source lines 20–48. The Sprint 1 trace calculation is internally inconsistent. For commuting $a_0,A$, cyclicity gives $\operatorname{Tr}(a_0[K,[K,A]])=2\operatorname{Tr}(K[K,a_0]A)$. The response sets the right-hand trace to zero while assigning a nonzero value to the left-hand trace. It also removes the linear time term and then requires that term for KMS symmetry. Its complete zero-mode formula omits a static term linear in $\theta$. The purported coefficient derivation is withdrawn.

**ARCH-R2-51.** [Historical source](source_archive/meron_model_generation_history/responses/deepseek_sprint3_spatial_clt.md), source lines 7–45. The $L=4,M=1$ witness refutes universal finite-$M$ positivity; it does not establish indefiniteness for every $L,M$. The volume-uniform clustering estimate is asserted rather than proved, and its distinct-site hypothesis is lost when all tuples are summed. The displayed lattice count $(2\xi)^{k-1}$ is not generally valid: for $k=2$, the exact one-dimensional geometric sum already exceeds $2\xi$. Higher-cumulant vanishing without covariance control, a probability law and tightness does not establish the asserted random-field convergence.

**ARCH-R2-52.** [Historical source](source_archive/meron_model_generation_history/responses/deepseek_sprint4_gate_d.md), source lines 11–110. At $\theta=0,z=0$, the two parity sectors have equal dimension, so their ratio is one rather than exponentially small. A modulus bound below one does not exclude argument $\pi$: take $\xi=-1/2$. The response changes $r/M\le1/192$ into $r/M\le1/(192M)$ and then invokes the result at $r=1/10,M=1$, outside the stated region. The source functional is exponential, not polynomial, in the source variables. The uniform constants and time-label summability claims are unproved. The exact high-temperature center $\theta=0$ is not a breakdown of the expansion.

**ARCH-R2-53.** [Historical source](source_archive/meron_model_generation_history/responses/deepseek_sprint5_theorem_b.md), source lines 13–177. Theorem B remains unproved by Sprint 5. The response extrapolates one finite negative eigenvector to all dimensions and loses normalization factors. Temporal high-frequency tests refute its uniform lower bound by $c_0\|\Psi\|_\infty^2$. Smoothness may suppress a negative contribution asymptotically without extinguishing it at $M\ge2$. A volume-uniform connected Trotter estimate needs its own summable insertion bound; changing the splitting does not supply one. Signed finite histories are not a discrete probability field. The stated total convergence rate also requires the appropriate odd-cumulant control.

**ARCH-R2-54.** [Historical source](source_archive/meron_model_generation_history/responses/mimo_v2_6_pro_g3_response.md), source lines 27–66. The MIMO response's obstruction to an analytic proof is false. If the stated analytic polydisk bound is $|\log Z(z)-\log Z(0)|\le CL$, apply Cauchy's estimate to $f(t)=\log Z(t\Psi/\sqrt L)-\log Z(0)$. For $B=\|\Psi\|_\infty>0$, its radius is $R_*\sqrt L/B$, giving $|f^{(n)}(0)|\le n!C(B/R_*)^nL^{1-n/2}$. Thus that assumption does imply the desired smeared-cumulant scale. Conversely, the proposed unweighted time-label Lemma A fails at $\theta=0$: its second-order sum at a fixed spatial site is $(2M-1)/4$. Repeated labels also require treatment. A normalized temporal average is a different possible hypothesis.

**ARCH-R2-55.** [Historical source](source_archive/meron_model_generation_history/responses/g4_sakana_fugu_ultra_v2_response.md), source lines 166–446. The paired finite-volume Lehmann formula is a useful part of the Fugu response. Its claimed closure at the explicit endpoint $1/192$ nevertheless relies on estimates not derived there: the linked-cluster coefficient bound with constant 96, the thermal commutator-moment lower bound $1/4$ and the uniform fourth-moment bound. Verbal enumeration of factors does not establish the first bound or its consequences. Nonnegative finite-volume coefficients can converge to zero. The strict limiting nonzero-mode conclusion therefore remains conditional on quantitative cluster and moment estimates.

**ARCH-R2-56.** [Historical changelog](../witnessed_difference_programme_change_log.md), source lines 1059–1061. A nonzero cycle pairing of a new repair column does not by itself reduce the quotient distance of every defect. On two edge-disjoint hollow triangles, a defect with unit circulation on the first retains that obstruction when the new column is supported only on the second. The column has a nonzero cycle pairing, but the quotient distance remains one. The historical one-cycle reasoning does not extend to independent cycles.

**ARCH-R2-57.** [Historical changelog](../witnessed_difference_programme_change_log.md), source line 1805. The printed quantity $\inf_{x\sim x'}d(x,x')$ is zero for a metric and reflexive relation, since $x'=x$ is allowed. In the declared additive repair model, the quotient defect is instead $\inf_{r\in\operatorname{im}d_0}\|x-r\|$. A state's distance to its own equivalence class is not its quotient norm.

**ARCH-R2-58.** [Supersession policy in the changelog](../witnessed_difference_programme_change_log.md), source lines 2075–2080. The original shared-checkout wording describes custody before source recovery. The current provenance manifest binds all 44 recovered inputs, whose bytes are retained in the source archive. The manifest itself is a binding record; it is not the byte archive. The earlier uncommitted-input wording is not a current source-availability limitation.

## Additional corrections to retained mathematical sources

The sources linked below preserve historical wording. The corrections here
supersede the identified claims; retaining a source does not endorse its
theorems, proposed constructions, or reported verification status. No correction
below selects physical premises, grants authority, or establishes an external
realization.

### Torsion-group decomposition — M2-A01

The [original quantum claim ledger](source_archive/coda_original_source_snapshot/51e9b0e9fd70cf98c6495967f30af5a27a66708df673d71a233d66e3716e7abd.txt)
incorrectly identifies $\mathbb Q/\mathbb Z$ with
$\bigoplus_{n\ge1}\mathbb Z/n\mathbb Z$. The former has two elements killed
by $2$; the latter has infinitely many, contributed by its even-indexed
summands. The correct decomposition is
$\mathbb Q/\mathbb Z\cong\bigoplus_{p\ {\rm prime}}\mathbb Z(p^\infty)$,
where $\mathbb Z(p^\infty)$ is the Prüfer $p$-group. Equivalently,
$\mathbb Q/\mathbb Z$ is the direct limit of its finite cyclic subgroups
under the divisibility-compatible inclusions.

### Damaged duration formulas — M2-A02

Several displays in the [original duration synthesis](source_archive/coda_original_source_snapshot/9b5a6b5747d2ffdc81a2b0de8135ed2b921d87b0439066a60cf161ac1877aecf.txt)
contain literal Markdown heading markers in place of mathematical operators.
In particular, the displayed face pairing loses the subtraction between its
two directed path sums. These damaged displays are withdrawn. For a face
bounded by declared paths $p$ and $q$, the pairing is the signed difference
$\langle\tau,\partial F\rangle=\sum_{e\in p}\tau_e-\sum_{e\in q}\tau_e$,
with incidence signs when an edge is traversed against its orientation.
The generic mechanism table supplies no proof of a cochain or Hilbert-space
structure.

### Joint diagnostics, rational norms, and repair invariance — M2-A03–A07

The [original diagnostics and observer-control source](source_archive/coda_original_source_snapshot/a52400b06bba9d51da49cd42ea614310b04acd3481a630b67b0a0f3cd8ca512a.txt)
requires the following corrections.

**M2-A03.** Joint reports can distinguish more than any individual report.
On $\{0,1\}^2$, the two coordinate projections are individually noninjective,
but their joint report is injective. The equivalence kernel of a joint report
is the intersection of the individual equivalence kernels. There need not be
a finest individual report. Adequacy for a protected answer still requires
that answer to be constant on the joint report fibers.

**M2-A04.** Faithfulness of a norm over $\mathbb Q$ does not imply that
zero distance to a rational repair subspace means membership. On
$\mathbb Q^2$, $J(x,y)=|x-\sqrt2y|$ is a faithful rational norm. For
$B=\operatorname{span}_{\mathbb Q}(0,1)$,
$\inf_{t\in\mathbb Q}J((1,0)-(0,t))=0$, although $(1,0)\notin B$.
The zero-distance criterion requires a closed repair subspace or attainment
of the minimum. Finite-dimensional real normed spaces supply closedness;
rational polyhedral data also supply rational optimal certificates.

**M2-A05.** An acyclic carrier does not make an independently declared
protected-channel test vacuous. Its cochain obstruction may vanish while,
for example, a protected violation count rises from $0$ to $1$ at tolerance
$0$. Only the diagnostics that vanish on that carrier become uninformative.

**M2-A06.** A gauge repair cannot lower an already minimized quotient
functional. For an unrestricted linear repair space,
$\inf_fJ(\delta-d_0g-d_0f)=\inf_hJ(\delta-d_0h)$.
Optimizing a representative cost and changing a quotient class are different
operations.

**M2-A07.** Normalization requires a strictly positive denominator. Empty
action windows and zero total mass do not define normalized weights.
Entropy expressions use the continuous convention $0\log0=0$. Nonnegative
weights summing to one form a mathematical probability distribution; an
empirical or physical interpretation requires additional premises.

### Finite path sums and scalar structures — M2-A08–A12

The [original finite witness-history integral](source_archive/coda_original_source_snapshot/8c6af871da216b8e16236fdf8ef9606340e0ddb34e275a20ca227e2afadfa54f.txt)
overstates several construction conditions.

**M2-A08.** Acyclicity does not make paths truncated at length $L$ closed
under composition. On $a\to b\to c$, both one-edge paths are allowed when
$L=1$, but their composite is not. Truncated composition needs a length
admission rule. A sum over paths of lengths at most $L$ is also distinct
from the single $L$-fold matrix iterate.

**M2-A09.** Acyclic support implies nilpotence of a finite weighted adjacency
matrix, but the converse fails for general weights. Zero weights may hide
cycles, and the nonzero matrix
$\begin{pmatrix}1&1\\-1&-1\end{pmatrix}$ has cyclic support and square zero.
An equivalence requires additional conditions excluding cancellation and
zero-weight concealment.

**M2-A10.** Equality of weights $e^{-\beta S(p)}$ detects equality of real
path actions when $\beta\ne0$; within the declared nonnegative range this
requires $\beta>0$. At $\beta=0$, every such weight is $1$.
Moreover, equality on directed paths with common endpoints need not imply a
global potential. The DAG with edges
$a\to c,a\to d,b\to c,b\to d$, and weight $1$ only on $a\to c$, has no
distinct directed paths with common endpoints, but its signed cycle period
is $1$. A converse using directed paths requires a root reaching every
vertex and a path family containing all relevant edge extensions.

**M2-A11.** The free nonnegative-real semimodule on a nonempty finite set is
infinite, so it is not an endofunctor on finite sets. Its monad belongs on
sets; the resulting matrix description may then be restricted to finite
objects. Unrestricted nonnegative matrices are not substochastic: the
one-entry matrix $[2]$ already violates a unit mass bound. Substochastic
claims require the appropriate row- or column-sum restriction.

**M2-A12.** An integer-valued interference fixture is not a complex-phase or
$U(1)$ construction. Matrix multiplication over a semiring with both
distributive laws is associative. A weaker interface omitting one of those
laws does not refute that theorem.

### Reachability and self-report — M2-A13–A15

In the [original self-witnessing outline](source_archive/coda_original_source_snapshot/0d58e1a5e70eb5da86000c280c46907a16835792f1f91e35ae912d96154cf748.txt),
the following implications need narrower statements.

**M2-A13.** State-independent reports on the whole carrier imply failure of
O1, but the converse need not hold: O1 tests only reachable states. With
states $\{0,1\}$, initial state $0$, identity updates and reports
$r(0,a)=0$, $r(1,a)=1$, O1 fails although the whole-carrier report depends on
state. Equivalence holds after restricting the report to reachable states,
or when every state is reachable.

**M2-A14.** Restricting an O2 witness to reachable input states is not enough
to infer O1 from report refinement. Let $x,y$ be reachable, let $z$ be
unreachable, give $x,y$ report and profile $0$, and give $z$ report and
profile $1$. A context sending $x$ to $x$ and $y$ to $z$ produces an O2
witness, while all reachable reports remain equal. The implication also
needs reachable context images, for example because contexts preserve the
reachable carrier.

**M2-A15.** A prediction map typed $S\times\Sigma\to R$ may depend on both
the state and the present input; “state alone” requires another hypothesis.
Finiteness by itself does not block diagonal arguments: Cantor's
non-surjectivity argument for $S\to\{0,1\}^S$ applies to finite sets too.
Any stronger self-reference result requires its own representation,
naming, and fixed-point assumptions.

### Scope of symmetry and retention claims — M2-A16–A17

The [consolidated original root outlines](source_archive/coda_original_source_snapshot/af161808e6d9e922259899d50d2a6b5bf5ccf310aa88e6074a32d72ecf9104e4.txt)
do not establish the unrestricted non-selection and retention claims.

**M2-A16.** Symmetry prevents selection of an asymmetric point or orientation
on the original pure-equality carrier. It does not prohibit every directed
relation, derived carrier, or canonical construction. The off-diagonal
relation is invariant. For $|X|\ge2$, the equality-pattern quotient of
$X^2$ has two canonical classes, diagonal and off-diagonal; taking the former as an
unmarked state and mapping off-diagonal pairs to the latter supplies a
nontrivial marking map without selecting a point of $X$. The identity
endomap and equality partial order are invariant as well.

**M2-A17.** The proposed five-way independence is not well typed as stated.
Once an occurrence $d\in D$ is fixed, nonemptiness of $D$ cannot fail.
A tuple declaring a total comparator cannot use an undefined comparator as
a countermodel. The literal claim that a component has no definable partial
order fails because equality is one. The relevant non-selection questions
concern nonempty strict orders or total orders with the stated invariance.
Finally, an empty cell in a bounded census is not a universal entailment,
and a census fixing $|D|=2$ cannot test failure of nonemptiness.

### Original observer claims — M2-A18–A20

The observer sections of the [same root outlines](source_archive/coda_original_source_snapshot/af161808e6d9e922259899d50d2a6b5bf5ccf310aa88e6074a32d72ecf9104e4.txt)
contain three distinct failures.

**M2-A18.** Ignoring input identity does not force a constant reachable
profile. A two-state update that toggles on every symbol, with the identity
profile, distinguishes the empty word from a one-symbol word. The correct
O0 condition is constancy of the report on the reachable carrier.

**M2-A19.** Finite input and context alphabets do not make arbitrary context
operations on $D^*$ finite or decidable. A total context program can inspect
a word's length and encode whether a fixed machine halts within that many
steps; existence of a context witness can then encode eventual halting.
Finite exhaustive procedures require bounded words, finite state-level
actions, or a proved finite quotient through which the contexts factor.

**M2-A20.** Coarsening a report can create a context witness. Start with the
identity profile on $\{a,b,c\}$ and a context sending $a$ to $a$ and $b$ to
$c$. Coarsen by identifying $a,b$ while retaining $c$ separately. The pair
$a,b$ becomes a witness. No-new-witness claims require the coarsened
equivalence relation itself to be a context congruence. A constant
post-processing map can also create report agreement.

### Redundancy and persistence — M2-A21–A22

The observer-descent section of the [root outlines](source_archive/coda_original_source_snapshot/af161808e6d9e922259899d50d2a6b5bf5ccf310aa88e6074a32d72ecf9104e4.txt)
uses incorrect criteria.

**M2-A21.** Recoverability from any $k$ of $n$ reports is upward monotone in
$k$: excess reports can be ignored. Its maximum is therefore $n$ whenever
all $n$ reports suffice; if $k>n$ is allowed, the quantifier is vacuous.
A recovery threshold uses the least sufficient $k$, with an explicit
failure case. A redundancy count based on disjoint sufficient fragments is
a different definition. Neither supplies a stability theorem by itself.

**M2-A22.** The persistence condition uses equality of a fact map $\phi$ in
its premise and equality of the profile $p$ in its conclusion, so its
failure is not automatically a $p$-context witness. On two states, take
$\phi$ constant, $p$ the identity and the context the identity. The displayed
condition fails, although $p$ has no distinct equal-profile pair. A
congruence test must use one declared equivalence relation consistently,
or supply the missing compatibility.

### Observation categories and exactness — M2-A23–A24

Two categorical/cohomological claims in the [projection-to-cochain outline](source_archive/coda_original_source_snapshot/af161808e6d9e922259899d50d2a6b5bf5ccf310aa88e6074a32d72ecf9104e4.txt)
are withdrawn.

**M2-A23.** An initial observation object does not imply that a full,
isomorphism-closed observation class is a quotient class. For nonzero $N$,
take the full subcategory consisting of isomorphisms $N\to V$.
The identity is initial and every object is isomorphic to it. This category
is not equivalent to the class of all maps out of $N$, which contains both
$\operatorname{id}_N$ and $N\to0$ as nonisomorphic objects. The quotient map
$N\to N/K$ is initial in the class of maps annihilating $K$; that sufficient
construction does not prove the proposed converse.

**M2-A24.** A particular closed cochain can be exact even when $H^1\ne0$;
the zero cochain is an immediate example. Vanishing of $H^1$ characterizes
the assertion that every closed cochain is exact. For a supplied cochain,
exactness is membership in $\operatorname{im}d_0$, certified by a preimage.

### Product-state tangent spaces and locality — M2-A25–A26

The physical example in the [same outline](source_archive/coda_original_source_snapshot/af161808e6d9e922259899d50d2a6b5bf5ccf310aa88e6074a32d72ecf9104e4.txt)
mixes different carriers and does not support its predicted invisible
triple-rate mechanism.

**M2-A25.** Trace-one product states lie in an affine state space; trace-zero
Hermitian operators are its tangent model. The product-of-marginals map is
polynomial in its single state argument. Its stated derivative is a tangent
projection on trace-zero variations, not an unrestricted projection on all
operators. For $s$ qubits, full-support adapted correlation terms have
dimension $3^s$, whereas the full traceless operator space has dimension
$4^s-1$ and includes lower-support terms. A diameter cutoff is not a
cardinality cutoff: at $L=4,R=2$, the Rips complex contains the four-site
cell even though $4>R+1$.

**M2-A26.** At a product state, the commutator with a two-site Hamiltonian
term has adapted support only on that pair and its subsets. Subtracting
the one-site tangent component leaves pair support. A nearest-neighbor
two-local Hamiltonian therefore produces no invisible triple component
of the instantaneous normal rate in the stated model. Static states with
triple correlations and higher-order evolved correlations do not establish
the outline's first-order prediction.

### Mixed signs and curved structures — M2-A27–A30

The spatial-history section of the [root outlines](source_archive/coda_original_source_snapshot/af161808e6d9e922259899d50d2a6b5bf5ccf310aa88e6074a32d72ecf9104e4.txt)
requires four corrections.

**M2-A27.** Its displayed untwisted history formula commutes with the
spatial differential for commuting stalk transports; it does not
anticommute. On one spatial edge, take restriction $1$, uniform duration
action $S_\tau=2$, $S_{2\tau}=4$, and a section with endpoint values $0,1$.
The two mixed composites both give $1$, so their sum is $2$ although the
locality commutator vanishes. Either insert $(-1)^p$ into the history
differential and use anticommutation, or retain commuting maps and apply
that sign in the total differential.

**M2-A28.** Three chain points already distinguish flatness from curvature.
For $a<b<c$, restrictions $r_{b,a}=r_{c,b}=1$, $r_{c,a}=0$ give curvature
$1$, while all three restrictions equal to $1$ are flat. Four points are
needed to exercise the specified degree-three expression, not to detect
nonzero degree-two curvature.

**M2-A29.** The sectionwise expression $d_2(K(s))$ is not the curved
dg-algebra Bianchi identity. A curved dg-algebra has
$d^2(a)=[h,a]$ and $d(h)=0$; multiplication by curvature is the
corresponding module law. For any degree-one operator $D$, the graded
endomorphism algebra has derivation $[D,-]$ and curvature $D^2$, with
$[D,D^2]=0$ even when $D^3s\ne0$. Thus the outline's sectionwise test
cannot exclude all curved dg realizations. Its calculated section defect
remains a separate quantity.

**M2-A30.** A bigraded family need not arise from a literal product
factorization of an underlying category. A family supported only at
$(0,0),(1,0),(1,1)$ is already bigraded. Product factorization is an
additional assumption of the proposed model, not a prerequisite for the
definition of every bigraded family.

### Fermion exchange and syndrome recovery — M2-A31–A32

The [unified locality submission](source_archive/locality_and_smearing/unified_lieb_robinson_observer_completion_derivation.md.txt)
contains incorrect calculations preceding otherwise useful conditional
criteria.

**M2-A31.** Its occupation cycle uses hops
$1\to0,0\to3,2\to0,0\to1,3\to0,0\to2$.
In the increasing occupation convention their fermionic signs are
$+,-,+,+,-,-$, whose product is $-1$. The printed assertion
$(-1)^6=-1$ is false, and a hop is not automatically a particle exchange.
The odd-exchange holonomy survives this correction. A site-to-configuration
locality transfer still needs an explicit operator map and support bound.

**M2-A32.** A syndrome decoder does not satisfy $RQ=\operatorname{id}_V$
when $Q$ has a nonzero kernel. Choose a representative map
$R:Q(\mathcal E)\to V$ and require
$e-R(Qe)\in B$ for admitted errors. Such a recovery exists exactly when
$(\mathcal E-\mathcal E)\cap\ker Q\subseteq B$, under the declared additive
model. The source's applications of $R$ directly to error vectors and its
displayed corrected-error identity are withdrawn.

### Upper bounds and the triangle gauge example — M2-A33–A34

In the [same locality submission](source_archive/locality_and_smearing/unified_lieb_robinson_observer_completion_derivation.md.txt):

**M2-A33.** A divergent upper bound can be valid but uninformative. For a
trace distance $\Delta\le1$, the bound $\Delta\le T^{-2}$ is valid for
$0<T\le1$ despite divergence at zero. Replacing a proved bound by its
minimum with $1$ improves it only within the domain where it was proved;
it does not extend a perturbative theorem to other times.

**M2-A34.** On the oriented triangle $a\to b\to c\to a$, with
$(d\alpha)_{uv}=\alpha(u)-\alpha(v)$ and $\alpha=(0,1,0)$, the correct
vector is $d\alpha=(-1,1,0)$, with norm $2$ and zero circulation.
The printed vector $(-1,1,1)$ has norm $3$ and is not that coboundary.
The raw cost depends on its chosen potential; minimization over all
potentials gives the stated gauge-invariant quotient cost.

### Local indistinguishability and decoder scope — M2-A35–A36

The analytic proof in the [locality submission](source_archive/locality_and_smearing/unified_lieb_robinson_observer_completion_derivation.md.txt)
is withdrawn in its printed form.

**M2-A35.** In finite dimensions, $\operatorname{Tr}[O,\rho_0-\rho_1]=0$
always; it cannot equal the readout difference in general. For
$O=\rho_0-\rho_1=\operatorname{diag}(1,-1)$, the readout pairing is $2$.
The correct local estimate uses equality of the reduced states on the
support of $O^{(r)}$:
$$
\operatorname{Tr}((\rho_0-\rho_1)O^{(r)})=0,\qquad
|\operatorname{Tr}((\rho_0-\rho_1)O)|
\le \|\rho_0-\rho_1\|_1\|O-O^{(r)}\|
\le 2C e^{-\mu(r-vT)}.
$$
No correlation-decay assumption is needed for this cancellation.
Replacing the state trace norm by its operator norm requires a dimension
factor: uniform states on disjoint halves of a $d$-dimensional space have
operator-norm difference $2/d$ but readout difference $2$ for the
corresponding $\pm1$ observable.

**M2-A36.** A reconstruction map must act on reports and recover a declared
answer map. Its Lipschitz bound then reads
$\|a(\rho_0)-a(\rho_1)\|\le L\|Q_T(\rho_0)-Q_T(\rho_1)\|$.
A Lipschitz map on states alone supplies no such relation to $Q_T$.
The printed approximate inequalities about readout noise are withdrawn.
For bounded adversarial noise in a normed report space, radius-$\varepsilon$
balls overlap when their centers are at distance at most $2\varepsilon$;
amplifying a common noisy report cannot distinguish its two origins.
No calibrated recovery or abstention theorem is established here.

### Partial trace, product projection, and residual — M2-A37

The [locality submission](source_archive/locality_and_smearing/unified_lieb_robinson_observer_completion_derivation.md.txt)
uses a reduced density matrix for three different objects.
The partial trace maps $\rho_{AB}$ to $\rho_A$ on a smaller carrier.
The product-of-marginals map is
$\Pi(\rho_{AB})=\rho_A\otimes\rho_B$ on the composite carrier.
Its residual is $\rho_{AB}-\Pi(\rho_{AB})$, which has trace zero and is
positive semidefinite only when zero. A positive scalar norm of that
residual is distinct from positivity of a reduced density matrix.

### Withdrawn antibody-transfer submission — M2-28

The [original antibody submission](source_archive/superseded_derivations_20261008/antibody_transfer.md)
is superseded by [the corrected transfer supplement](antibody_transfer_and_amortization.md).
Its principal errors are:

- With the stated triangle incidence map,
  $d_0(0,1,0)=(1,-1,0)$, not $(0,1,0)$; the latter has boundary $1$.
  The exact nonzero witness is $(1,-1,0)$.
- Accumulation needs sound transferred rejections, or the adapter condition
  $\alpha(G_T)\subseteq G_S$. Source soundness alone is insufficient, as
  the submission's own transfer of the rejection of $5x$ demonstrates.
- Polynomial truncation already fails on $F=x^{k+1}$, whose derivative has
  degree $k$. The claimed correction using derivative degree $>k$, and the
  proposed degree-$k+1$ pool restriction, do not repair the example.
- Valid-image inclusion is not fiber constancy. A partial adapter defined
  on all valid candidates can still be undefined on invalid candidates.
  Matching names of binding fields does not prove either property.
- A generic rejection certificate need not be a separating linear
  functional. “No surviving candidate is rejected” and “no valid candidate
  is rejected” are not equivalent checks.
- The projected vector $(1/3,1/3,2/3)$ is exact on the filled triangle and
  has quotient mass zero; replacing the original cochain by it is still
  not an admitted gauge repair.
- A codimension-one rational subspace does not determine an invalid
  fraction of $1/3$ without a distribution. Hit-rate transport remains a
  separate statistical obligation.
- Cost thresholds require their stated positive denominators.
  The case $c'=c$ cannot use division by $c'-c$; $C_0=0$ also invalidates
  the printed strict negative inequality. No strict coverage/fragility
  tradeoff follows for every enlargement of a guard. The receipt list has
  five kinds, despite its four-kind heading.

### Withdrawn sufficient-observation submission — M2-29

The [original observation-pricing submission](source_archive/superseded_derivations_20261008/finite_observation.md)
is superseded by [the corrected sufficient-observation supplement](minimum_cost_sufficient_observation.md).
The instrument hypergraph has edges
$H_u=\{i:u\in D_i\}$ on instrument vertices; the $D_i$ themselves are sets
of unresolved pairs. A decoder exists when the answer is constant on
report fibers. The submission reverses this condition and several
refinement implications.

An infeasible shelf has no finite attained optimum. Disjoint-support
packing certificates are feasible LP dual bounds and cannot exceed the
optimal LP bound. The claimed star examples do not demonstrate a packing
gap. A local branch-and-bound prune does not certify complete global
coverage of the search.

The three-state example omits unresolved pair $\{2,3\}$ and its measured
distinction. More decisively, in the printed adaptive table, states $1$
and $5$ both have report $(A,B,C)=(0,0,0)$ but different answers. That table
is unresolvable and does not have fixed and adaptive costs $7$ and $4$.
Its stated outcome fibers also disagree with its entries. With a
nonconstant free initial report, the global adaptive cost is the maximum
over attained initial-report fibers, rather than a recursion that ignores
that report. Failure of exact coverage does not itself construct an
approximate decoder or certify its error.

### Monotone maps are not necessarily embeddings — M2-S01

The archived Prime [claim IR](source_archive/prime_algorithm_package/docs/claim_ir.yaml)
and [claim ledger](source_archive/prime_algorithm_package/oe_prime_algorithms_claim_ledger.yaml)
describe OE004-02 as an embedding statement. The
[formal interface](source_archive/prime_algorithm_package/lean4/Prime/Basic.lean)
assumes only monotonicity, and its theorem returns that assumption.
The constant map $n\mapsto0$ satisfies it but is neither injective nor
order-reflecting. The proved conclusion is order preservation by the
supplied map; an order embedding requires the additional property.
