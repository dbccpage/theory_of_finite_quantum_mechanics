# Reading S(n): stages, survivors and realizations

AuthorityEffect: None. S(n) numbers derivational stages. It does not number
simplex dimensions, physical dimensions or entries in the MSS verification atlas.

Start with the seven [core pages](levels/level_00_ground.md) and read them in
order; the former core-stage lesson tree was retired on 2026-10-06. At each transition,
identify the actual unresolved challenge, the admitted response and its
preservation obligations. A mathematical realization has no authority to
admit a successor stage.

## Keep the two ledgers separate

The native core's active-obstruction counts are `(0,1,1,1,0,1,1)`.
They count unresolved receipts W, not all retained historical receipts H.
For example, [S(4)](levels/level_04_simplex_graph_expansions.md) closes the orbit requirement:
W is empty and s=0. H still records the separation and closure certificates.
Deleting those certificates to make H empty would lose provenance.

Distinguish also an ordered replay history (replay log) from the persistent history ledger H.
A replay log preserves temporal order and event multiplicity; H is the deduplicated set
of valid historical certificates and receipts emitted up to stage n.

## Separate inscription from admission

- `<>` is one opaque presentation lexeme, two ASCII bytes, and zero admitted carrier elements ($|V_0| = 0$).
- `<a>` records a single mark, but does not alone force carrier admission ($|V_1| = 1$ requires an explicit consumer or retention receipt).
- In Genesis, `<ab>` is one opaque token. The local S(n) grammar interprets the same spelling as two glyphs; use an explicit parser map before transferring claims.

## The binary germ and endpoint support ($\Delta_{\mathrm{support}} = 2$)

For an irreflexive relation R, $R(a,b) \implies a \neq b$. Consequently, every admitted primitive cut
has exactly two distinct endpoints: $\Delta_{\mathrm{support}}(a,b) := |\{a,b\}| = 2$.
Witness occurrences, however, may be 1, 2, or more (e.g. `single_oriented_witness_consistent` in `PrimDiff.lean`
constructs an explicit model with 1 forward witness and 0 reverse witnesses).
Pointed universal binary germ $D_2 = (\{0,1\}, 0 \to 1)$ admits a unique edge-preserving map
$f: D_2 \to (A,R)$ with $f(0)=a, f(1)=b$ (`D2_initial_pointed`).
When an observation collapses a pair ($q(a)=q(b)$), supply a tag $t(a)=0, t(b)=1$ to define
$q'(x) = (q(x), t(x))$, resolving the collision while preserving previous readouts.

## Decouple construction stage ($n$) from homotopy depth ($j$)

For a fixed space X, its Postnikov stages $P_j X = \tau_{\le j} X$ preserve homotopy groups through degree j
and remove higher ones. Truncations preserve $\pi_0$, so an empty space followed by a point cannot be successive
truncations of the same space. At fixed stage n, $P_j(\rho(S(n)))$ is the candidate Postnikov tower of realization $\rho$.
Growth across construction stages n remains a separate construction requiring its own maps and preservation proofs.

## Read a realization as an explicit map

A realization specifies its source stage, target carrier, preserved questions
and lost information. Beyond the locally labelled S(6) construction, candidate pages retain
`realizes: null` and a candidate bridge from S(6). Their richer mathematics
does not establish S(7) or a later native derivation.

For a section u and typed retraction $\widehat{r}_n: P_{n+1} \to P_n \sqcup \{\mathrm{NON\_DESCENT}\}$,
the correctly typed law is $\widehat{r}_n \circ u_n = \mathrm{inl}$.
Rejecting every element outside $\operatorname{im}(u_n)$ defines exact recovery from that image.
Keep this separate from a total forgetful projection or Postnikov down-map.
The old-image law also needs a separate theorem showing that the lift resolves the selected obstruction.

## Distinguish a representation quotient from a native stage

[Declared] In a supplied complex model, one coordinate at each site gives
two doubled real carriers and four ordinary tensor coordinates. The balance
map sends (rr,ri,ir,ii) to (rr-ii,ri+ir). [Proved] Its exact kernel is
the complex balancing relation, as shown in the
[tensor supplement](/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/complex_tensor_balancing.md).

Let u=T^t/2 and r=T. Calculate r u=I_2 and u r=P on the four-dimensional
ordinary tensor. The vector (1,0,0,1) survives as input but lies in ker(T),
so P does not equal I_4. State the declared questions preserved by this
representation and the information intentionally quotiented away.
[Open] A lawful representation of the selected quantum composite supplies
neither a new native S(n) obstruction nor permission to advance beyond S(6).
The richer candidate pages retain their declared representation status.

## Retrieval checks

1. At S(4), how can s=0 while historical certificates remain? The ledgers
   answer different questions: unresolved demands versus retained evidence.
2. Does a nonzero cycle in a graph realization become a native survivor?
   Only a source-bound Genesis obstruction may populate the native register.
3. Does r∘u=id imply u∘r=id? Exhibit the new coordinate (0,1).
4. What proves a successor stage? An actual unresolved obstruction and a
   licensed response with its preservation and cost evidence.

Finite model examples exercise these distinctions. They do not prove a
native stage merely by assigning its expected survivor count.

For a source-specific cost exercise, the [COUNT admission derivation](/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/admission_execution_refinement.md)
proves a minimum of n+sum(r+s)+2*sum(L) changes on its declared source-16
states. A remove/admit cycle can preserve the final tables while adding
a paid occurrence. Relate that distinction to retained history H and
unresolved receipts W; do not identify a source leftover table with either
native ledger without a declared map.

For a second source-specific exercise, use the [persistent primitive floor](/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/primitive_execution_refinement.md).
Three admitted data with no forms and all three pair requirements need a
two-item form/instance response of arity at least two. Four data with all
six pair requirements need arity at least three. In each case the tuple's
mentioned data must meet every requirement edge. Compute the cover before
selecting the form; an arity price cannot always select a unary witness.
These carrier sizes and costs are not S(n) stage indices. The declared
stage ledger still requires its own obstruction and licensed response.

The [raising result exercise](/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/gauge_result_refinement.md)
starts with two terms and zero assertion excess. Raising term 0 gives
e=[0,1;-1,0], with the same source result key. Its raw plain-state cost
changes from 2 to 4. Explain why the key cannot recover that cost, and why
a one-term raising still has an occurrence even when it changes no table.
This source equivalence is a declared realization; it supplies neither an
S(n) successor nor permission to erase its retained history.

The [oriented-mark calculation](/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/marked_result_refinement.md) separates an admitted triangle
from its balance condition. With one r assertion 0→1 and all other counts
zero, (0,1,2) has diagnostic 1, while (0,2,1) has diagnostic 0. Cyclic
rotations preserve each sum; reversal need not. Explain which additional
reverse-arc law would make reversal negate the sum before importing a
simplicial interpretation.

Then identify 0 and 1 in the four-term example with fillings (0,2,3) and
(1,2,3). The source drops degenerate fillings and merges duplicates, but
does not require the remaining filling to balance. Compute its diagnostic
before claiming that this raw carrier edit induces a quotient map.

## Keep a presentation level separate from S(n)

[Declared] A level n in the [dyadic presentation](/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/dyadic_refinement_and_duality.md)
means the carrier Z/(2^n). It is a supplied realization index. Map 3 in
Z/8 to 6 in Z/16 and verify the unchanged rational coordinate 3/8.
[Proved] A character index 3 downstairs has two extensions, 3 and 11
upstairs. They answer the same restricted questions and different new
questions. An extension choice therefore needs more data than the old index.

[Pinned] Exact finite tests compute these pairings and sums; selected Lean
laws prove the restriction fiber at arbitrary levels. [Open] Neither
enlarging this carrier nor admitting its circle completion establishes a
native S(n) successor. Name the unresolved native obstruction and its
licensed response before assigning any new stage status.

## A completion is a declared realization

The [metric presentation criterion](/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/cs_q_presentation_completion.md)
is now mechanized for actual metric spaces. It requires nearby presented
values to control nearby protected answers. For p(n)=1/n, p(0)=0 and
q(n)=1, q(0)=0, explain why exact image descent still fails this requirement.
A finite replay cannot exhibit the missing all-level modulus.

Give dyadic torsion first its discrete topology and then its circle-subspace
topology. Name the corresponding duals Z_2 and Z. The second branch completes
to the supplied circle; the chosen topology is part of the realization.
Neither this completion nor the formal metric proof establishes an unresolved
native obstruction or licenses advancement beyond S(6).

## Keep the source query fixed during refinement

The [Meron time/volume proof](/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/meron_time_and_volume_refinement.md)
uses an admitted CAR Hamiltonian and its full-Fock partition. At fixed q,
adding checkerboard repetitions changes theta=M log(q). A time refinement
must retain the selected temperature and include its parameter error.
Identify that protected question before judging the refined receipt.

The derived time/volume limit is a realization with extra model commitments.
It does not supply a new native obstruction, stage successor or physical
interpretation of the initial inscription. Explain why its mathematical
closure does not move the native stage ledger beyond S(6).

## Preserve a selected query through a model map

The [spin/query derivation](/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/meron_spin_and_observable_transport.md) keeps a parity selector in the
periodic fermion-to-spin map. Compute (-1)^(N-1) for a hop across the closing
bond, then apply the odd-sublattice sign change. Explain why even and odd
sectors require different XY boundary twists. The finite carrier is admitted;
neither the glyph nor a stage label chooses it.

The canonical time-average square is 48/19 and the equal-time square is
149/57. Their difference is 5/57. Explain which history coordinate the first
query retains. A representation preserving a Hamiltonian still needs an
actual map for each protected readout. Distinguish the written fixed-volume
time-limit proof from its finite native checks and the open spatial limit.

## Execute one finite presentation without losing its contract

The [normal-form standards](../../../omega_engine_pfp/infrastructure/yaml/normal_forms/normal_forms_schema.sql) take the existing
AutoP contract through actual PTIR and SQL. Under A→B, explain why projecting
R(A,B,C) into (A,B),(A,C) and naturally joining recovers every legal relation,
not merely the current instance. Replay its recorded FD-closure applications.

For SJ→T,T→J, compute the closure of T and check the (J,T),(S,T) split.
Both components are BCNF and the split is lossless; identify why SJ→T is
nevertheless lost as a locally enforceable dependency. State which edits leave
the actual image of the projection. The [written argument](/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/sql_normal_form_presentation.md)
and eight native/twenty-two compiler-SQL checks have separate scopes. Explain
why a zero decision budget is unknown and why a checked snapshot does not
authorize a migration or establish a universal mathematics language.

## A vanishing pressure error does not close every query

Read the [actual source-field derivation](/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/meron_source_field_response.md). Track one theta and three
field points x-epsilon,x,x+epsilon. Show why holding the transfer multipliers
fixed changes the target as time slices grow. Compute the response error
(b_minus+2b_zero+b_plus)/epsilon^2 and explain what remains protected when
epsilon is retained. The convex countermodel converges uniformly everywhere
while its second derivative at zero converges to the wrong value: identify
the additional witness a pointwise response would need.

## A pointwise response with an actual regularity witness

The [analytic-source proof](/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/meron_analytic_response.md) supplies a uniform source disk and
derivative bounds for the declared theta<=1/192 region. Distinguish a finite mark, a declared circle topology and an actual
response convergence estimate. Show where each becomes an added premise.
Check why the q=3,M=2 example is outside this theorem even though its
finite exact readout remains valid. Finally state which spatial scaling
estimates are still needed before claiming a continuum field theory.

## From the selected circle to a spatial Gaussian source

Read the [spatial-source derivation](/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/meron_spatial_gaussian_source.md). Keep one profile F across the grids and explain which admitted data
make x/L a point of the completed circle. Derive the time and site factors
in SG-2; changing them changes the protected query.
For the triangle profile (0,0),(1/2,1),(1,0), compute its norm, Lipschitz
constant and squared integral. At theta=0 compare the four-site query 3/32
with the common target 1/12, and identify the spatial error that covers their
difference. State what remains needed for an interacting dynamical field.

## Read CODA through six common constructions

Use [Appendix P and the CODA decomposition](/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/coda_mathematical_decomposition.md).
First derive the report fiber criterion, then apply it to a repair quotient.
For the map `(0,0,1,2)` and potential `(0,0,1,0)`, compute the transported
cycle `−1`; explain why no quotient arrow descends on all representatives.
Repeat with three size-2 fibers and derive `T(dg)=d(2s)`.

Next compare `d1x=0` with `d1x` belonging to a second repair image. State the
image equality needed for a chosen residual projection to represent FOC.
Finally distinguish a uniform completion of one query from a terminal path,
a local grant verification and grantor standing. List the additional overlap,
physical-model and institutional premises needed before making broader claims.

## Predict which Genesis edits preserve balance

Read [Appendix P.7](/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md#p7-complete-balance-preservation-rules-for-the-five-source-25-edits)
and [lesson 720.24](../witnessed_difference_programme/curriculum/720_wdp_levels/concepts/lesson_720_24_balance_preserving_edits.md).
Classify an assertion on a forward arc, its reverse, a loop and an identification
whose merged vertex touches a surviving face. Distinguish one balanced output
from a rule valid for every old balanced state. Explain the three-face
tetrahedron counterexample and the seven-directed-face implication. State why
these balance rules still leave global quotient descent and higher sites open.
