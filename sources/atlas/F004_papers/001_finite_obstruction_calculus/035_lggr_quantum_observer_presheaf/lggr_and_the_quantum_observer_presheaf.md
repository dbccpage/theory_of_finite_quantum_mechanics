# Local Green, Global Red: the Observer Tuple, the Empirical Presheaf and the Three-Role Gate

**AuthorityEffect:** None.

**Register:** FOC-035. **Status:** derivation note with executable evidence. Every
claim below names the Rust or Python test that computed its instances. No Lean
was elaborated for the first version of this note (Mathlib is unreachable from
the session that wrote it). Since 2026-10-17 the Mathlib-free file
`lean4/quantum_mechanics/LggrFiniteResults.lean` elaborates under Lean 4.34.0
and checks the finite statements named as Lean-checked in the ledger (rows B1
and B11 in part, with the narrowing stated there). Every other row stays as its
status says.

**Parent texts.** The Witnessed Difference Programme (WDP) monograph, chapters
10, 14 and 15 (`witnessed_difference_programme.md` under `000_witnessed_difference_programme/`);
the authority note `docs/what_the_hell_is_authority_v002.md` in the same folder;
FOC-034 (`034_quantum_observer_quantum_carrier/`), which asks the question this
note answers in the finite case.

**Code.** Rust: `omega_engine/crates_rs/omega_sheaf_theory/src/empirical_presheaf.rs`,
tests in `omega_engine/crates_rs/tests/omega_sheaf_theory/empirical_presheaf.rs`
(`cargo test -j 1 -p omega_sheaf_theory --test empirical_presheaf`, 15 tests).
Python: `omega_engine_pfp/domain/provenance/three_role_gate.py`, fixture
`omega_engine_pfp/domain/fixtures/three_role_provenance_fixtures.json`, tests in
`omega_engine_pfp/tests/normal_forms/test_three_role_gate.py` (13 tests).
The claim ledger is `claim_ledger.md` beside this file.

---

## 0. What the mission cites, and what `main` carries

The mission specification that commissioned this note cites identifiers. Each
was looked up on `main` at `ae38eaa89` before being used.

| Cited identifier | On `main`? | Where, and how it is used here |
| --- | --- | --- |
| `WDP-CH10-D01` … `D04` | yes | observer presentation, memory, evaluator, policy (monograph ch. 10). The mission's "5-tuple" is a reading of these four packets; the monograph itself defines no 5-tuple. Section 1 gives the map. |
| `WDP-CH14-T01`, `C01`, `N03` | yes | the three-axis regress, its corollary and its nonclaim (monograph ch. 14). Section 3.1 restates T01 with its hypotheses made explicit. |
| `WDP-CH15-D01`, `D02`, `P04` | yes | authority packet, executable receipt $(c,\Delta,\varphi^*,\mathrm{status})$, prose impotence (monograph ch. 15). |
| `collapsed_of_no_insts` | name only | a Genesis (`19L57G1`) theorem name; on `main` it appears in a pinned copy of the Genesis claim ledger under `015_pfp/021_.../g03/pinned_sources/`. Not re-run here; Genesis is out of scope for this note. |
| `ENC-0118`, `ENC-0195` | name only | Genesis encoding identifiers cited by the monograph and by `005_mind_and_consciousness/001_awareness_mind_consciousness/what_is_awareness.md`. Their statements are not on `main`. |
| Lemma D | no statement | named in `WDP-CH14-T01` and in the awareness note; no file on `main` states it. Section 3.1 does not rest on it. |
| `NS-14`, `CL-13` | yes, in prose | stated in `coda_atlas/prompts/pilots/pilot_002/test_cases/ooutwire_argon_synthesis.md` (Gemini Argon's synthesis, cited, not edited). |
| `NB-9` | REFUTED | the same synthesis records `NB-9` as refuted by `budgetSim_enc_injective`; the review at `/mnt/project-files/reports/argon_notebook_review_2026-10-15/report.md` confirms it. Axis 3 is derived without it (section 3.1). |
| Test 482 | yes, vacuous | `omega_engine_pfp/tests/normal_forms/test_tranche25_acyclic_cohomology_and_bell_contextuality.py` line 82 sets `is_gyo_acyclic = True` and asserts it. It computes nothing. Section 2.5 replaces it. |
| `DescentOutcome::NoGlobalExtension` | yes | `omega_engine/crates_rs/omega_category_theory/src/finite_report_descent.rs`. Section 2.3 says what it does and does not witness. |
| `PresheafGlueReceipt::NoGlobalExtension` | no | no such type exists; the descent outcome above is the one used. |
| `AP_AB_UNADMITTED_SHEAF_BRIDGE` | no | proposed in section 3.2 as a candidate anti-pattern card; unregistered. |
| `RULE_AUTHORITY_SEPARATION_001` | no | the nearest registered rule is `RULE_EVALUATOR_SUPREMACY_AUTHORITY_SEPARATION_001` in `.claude/rules/papers/rl_paper_epistemic_evaluator_and_namespace_discipline.md`. |
| PR #1050's LGGR test | not on `main` | PR #1050 is open; nothing from it is cited. |

---

## 1. Obligation A: the observer tuple

### 1.1 Reading the five components off chapter 10

The monograph's observer is four packets: a presentation
$\mathsf{Pres}_{\mathcal O}=(X_{\mathcal O},P_{\mathcal O},q_{\mathcal O},\mathcal C_{\mathcal O})$
(`WDP-CH10-D01`), a memory (`D02`), an evaluator
$\mathsf{Eval}_{\mathcal O}=(D_{\mathcal O},A_{\mathcal O},d_{\mathcal O},\dots)$ (`D03`)
and a policy (`D04`), with the standing of any output fixed outside the
observer by the authority packet of chapter 15. The mission's tuple

$$
\mathcal O=(K,\ \mathrm{Adm},\ \|\cdot\|,\ \mathrm{Term},\ \mathcal L)
$$

is the projection of those packets onto the five things an evaluation of a
single claim needs:

| Component | Chapter 10 / 15 source | Empirical instance (section 2) |
| --- | --- | --- |
| $K$, the kernel | $X_{\mathcal O}$ with the context family $\mathcal C_{\mathcal O}$ | the measurement cover and the section space $\mathcal E(C)$ over each context |
| $\mathrm{Adm}$, admissibility | $A_{\mathcal O}$ in the evaluator | the noncontextual polytope $\mathrm{conv}\{\delta_g : g \in \mathcal E(X)\}$ |
| $\|\cdot\|$, the norm | $d_{\mathcal O}$ | $\ell^1$ on the stacked distributions |
| $\mathrm{Term}$, the terminal rule | the routing of $\mathsf{Eval}_{\mathcal O}$ | `TERMINAL_RULE_L1`: defect $0 \to$ `ExactRepair`; defect $>0$ with a support-level global section $\to$ `ClosedResidual`; otherwise `OpenObstruction` |
| $\mathcal L$, the layer | the grade carried by the chapter-15 packet | diagnostic; the receipt carries `AuthorityEffect: None` |

Nothing in the tuple is a person. FOC-034's question ("without giving the
observer an undeclared exemption") is answered here in the finite case by
refusing to evaluate until every component is on the record.

### 1.2 Definition A1 (observer tuple, empirical instance)

Fix a measurement scenario $(M, \mathcal C)$: a finite set of measurements with
arities, and a cover $\mathcal C$ of $M$ by maximal contexts. For $U \subseteq M$
write $\mathcal E(U)$ for the set of outcome assignments on $U$. An observer
tuple for empirical claims is

$$
\mathcal O = \bigl(K = (M,\mathcal C,\mathcal E),\ \mathrm{Adm} = \mathrm{conv}\{(\delta_g|_C)_{C\in\mathcal C} : g\in\mathcal E(M)\},\ \|\cdot\|_1,\ \mathrm{Term},\ \mathcal L = \text{diagnostic}\bigr).
$$

The evaluator of a claim $e = (e_C)_{C\in\mathcal C}$ (one distribution per
context) is

$$
\Delta_{\mathcal O}(e) = \min_{p \in \mathrm{Adm}} \|e - p\|_1,\qquad
\mathrm{status} = \mathrm{Term}(\Delta_{\mathcal O}(e), e),
$$

and its receipt is $(c, \Delta_{\mathcal O}(e), \varphi^*, \mathrm{status})$ in
the sense of `WDP-CH15-D02`, where $\varphi^*$ is the optimal dual of the
$\ell^1$ linear programme (section 2.6).

In code: `ObserverTuple { kernel, admissibility, norm, terminal, layer }`,
built only through `ObserverDraft::declare()`, which returns
`EmpiricalError::UndeclaredObserverComponent(name)` for the first missing,
empty or whitespace component and never a default. The five strings are then
bound to the one profile the evaluator implements by
`ObserverTuple::l1_profile(scenario)`: the kernel must equal
`scenario.kernel_label()`, which names the cover and the arities of the model
under evaluation (for the Bell scenario,
`support presheaf over the maximal-context cover {0,2}|{0,3}|{1,2}|{1,3} with arities 2,2,2,2`);
the admissibility must be `ADMISSIBILITY_NONCONTEXTUAL`, the norm `NORM_L1`,
the terminal `TERMINAL_RULE_L1` and the layer `LAYER_DIAGNOSTIC`. Any other
declared value is refused with
`UnsupportedObserverComponent { component, declared }`, and the typed
`L1EvaluationProfile` that the declaration was bound to is carried in the
receipt beside the declared strings. `evaluate_l1_claim(draft, claim, model,
pivots)` calls `declare()` and `l1_profile()` before any arithmetic. In the
reviewed head of PR #1080 the five strings were free text copied into the
receipt while the same $\ell^1$ evaluation ran whatever they said (a norm
"L2", a terminal "always OpenObstruction" and a layer "authoritative" all
yielded $\ell^1$, `ExactRepair` and `AuthorityEffect: None`); that is recorded
as negative evidence in the ledger (N5) and refused now.

### 1.3 Lemma A2 (conditional underdetermination) and Policy A2′ (five-field refusal)

**What the reviewed draft claimed, and why it is narrowed.** The draft of
this section stated that an undeclared component leaves *no function* from
claims to receipts. Two completions with different receipts refute only the
existence of a completion-independent receipt; any one completion still
defines a function. The review of PR #1080 recorded this, and two further
defects in the witness table: the layer row's second completion was an
authority grade, which the row itself said is not an observer and which
Definition A1 excludes (the layer is fixed to diagnostic); and the norm and
terminal rows were arithmetic on the computed $\Delta = 2$, not receipts of a
configurable evaluator. The lemma below states what the witnesses establish,
and the refusal policy is separated from it and labelled as policy.

**Lemma A2 (conditional underdetermination).** Let $\mathcal O'$ leave one of
$K$, $\mathrm{Adm}$, $\|\cdot\|$, $\mathrm{Term}$ undeclared, and require of
an evaluation of $\mathcal O'$ that its receipt for a claim agree across every
admissible completion of the undeclared component (the *agreement
requirement*). Then no evaluation of $\mathcal O'$ meets the requirement: for
each of the four components there are two admissible completions, agreeing on
the other components, whose receipts for one claim differ.

| Undeclared | Completion 1 | Completion 2 | Claim | Receipts differ in | How established |
| --- | --- | --- | --- | --- | --- |
| $K$ | the Bell cover $\{ab, ab', a'b, a'b'\}$ | the acyclic sub-cover $\{ab, ab'\}$ on $\{a,b,b'\}$ | the PR box read on each cover | $\Delta = 2$ versus $\Delta = 0$ (Vorob'ev gluing, section 2.5); status `OpenObstruction` versus `ExactRepair` | both receipts computed: `pr_box_is_strongly_contextual_with_zero_noncontextual_fraction`, `vorobev_product_formula_glues_acyclic_covers_and_refuses_cycles` |
| $\mathrm{Adm}$ | the noncontextual polytope | the no-signalling polytope | the PR box | $\Delta = 2$ versus $\Delta = 0$ | the first computed; the second proved (the PR box is no-signalling, Proposition B5), not executed: the evaluator implements one admissibility |
| $\|\cdot\|$ | $\|\cdot\|_1$ | $2\|\cdot\|_1$ | the PR box | $\Delta = 2$ versus $\Delta = 4$ | arithmetic on the computed $\Delta = 2$; not an executed receipt |
| $\mathrm{Term}$ | `TERMINAL_RULE_L1` | "defect $<3 \to$ `ExactRepair`" | the PR box | status `OpenObstruction` versus `ExactRepair` | arithmetic on the computed status; not an executed receipt |

The layer $\mathcal L$ has no row. Definition A1 fixes it to diagnostic, so a
tuple with another layer is not a completion of an observer but a different
kind of packet (chapter 15 places the grade outside the observer). What the
lemma does not say: that no function exists. Fix any completion and the
evaluator is a function. The lemma says that the receipt is not determined by
the claim together with the declared part of $\mathcal O'$. $\square$

**Policy A2′ (five-field refusal) [POLICY INVARIANT — by construction].**
`evaluate_l1_claim` refuses a draft with any of the five fields undeclared,
empty or whitespace (`UndeclaredObserverComponent(name)`), and refuses a
declared field the evaluator does not implement
(`UnsupportedObserverComponent { component, declared }`), in both cases before
any arithmetic. A sentence emitted in place of a receipt carries
$\mathrm{AuthorityEffect}=\text{None}$ by `WDP-CH15-P04`, which is the
monograph's own proposition and a policy invariant by construction: prose has
no authority effect because the programme defines authority that way. The
policy is not a consequence of Lemma A2. The lemma motivates refusing on the
four underdetermined components; the layer is refused because the receipt
declares its grade, and a declaration naming another grade would otherwise be
copied into a receipt that computes none.

**Coverage, stated exactly.** Executed: both receipts of the $K$ row and the
first receipt of the $\mathrm{Adm}$ row; every one of the five drops and every
blank (`an_undeclared_observer_component_is_refused_before_any_arithmetic`,
`pr1080_blank_observer_fields_are_refused`); every unsupported declaration
(`pr1080_receipt_does_not_accept_an_unsupported_observer_profile`: the norm
"L2 rather than L1", the terminal "always OpenObstruction", the layer
"authoritative", a kernel phrase not bound to the scenario, a kernel label of
another scenario, another admissibility); the typed profile in a receipt of a
supported declaration. Not executed: the second receipts of the
$\mathrm{Adm}$, $\|\cdot\|$ and $\mathrm{Term}$ rows. The evaluator implements
no second norm, terminal rule or admissibility, so those entries are derived
by hand from the executed $\Delta = 2$, and a declaration asking for them is
refused rather than computed. The reviewed draft said the refusal test drops
each of the five components; at that head it dropped two (admissibility and
layer). It drops five now, and blanks five.

---

## 2. Obligation B: the presheaf of empirical observations

### 2.1 Contexts, probability vectors, restriction

**Definition B1.** Let $\mathbf{Ctx}$ be the poset of subsets of $M$ that lie
inside some maximal context, ordered by inclusion. For $U \in \mathbf{Ctx}$ let
$\mathbf{ProbVect}(U)$ be the set of probability vectors on $\mathcal E(U)$,
with entries in $\mathbb Q_{\ge 0}$ summing to $1$. For $V \subseteq U$ the
restriction is marginalisation,

$$
\rho^U_V : \mathbf{ProbVect}(U) \to \mathbf{ProbVect}(V),\qquad
(\rho^U_V d)(t) = \sum_{s \in \mathcal E(U),\ s|_V = t} d(s).
$$

An *empirical model* is a family $e = (e_C)_{C \in \mathcal C}$ with
$e_C \in \mathbf{ProbVect}(C)$.

**Lemma B2 (functoriality).** $\rho^U_U = \mathrm{id}$ and
$\rho^U_W = \rho^V_W \circ \rho^U_V$ for $W \subseteq V \subseteq U$, so
$\mathcal E : \mathbf{Ctx}^{op} \to \mathbf{ProbVect}$ is a functor.

*Proof.* Summing over $s$ with $s|_W = t$ is summing first over the values on
$U \setminus V$ and then over those on $V \setminus W$; the identity case is
the empty sum. $\square$

In code `Scenario::marginalize` is $\rho$, and
`EmpiricalModel::restriction_is_functorial` checks both equations on every
chain $W \subseteq V \subseteq C$ of the cover.
Executable: `restriction_is_a_functor_and_the_pr_box_is_a_presheaf`.

### 2.2 Global sections and the Abramsky–Brandenburger equivalences

Write $G(e) = \{g \in \mathcal E(M) : e_C(g|_C) > 0 \text{ for all } C\}$ for
the *global support* and $A$ for the matrix whose column $g \in \mathcal E(M)$
is the stacked vector $(\delta_{g|_C})_{C}$.

**Proposition B3.** For an empirical model $e$:

1. $e$ has a global section in $\mathbf{ProbVect}$ (a $d \in \mathbf{ProbVect}(M)$
   with $\rho^M_C d = e_C$ for all $C$) if and only if $e \in \mathrm{conv}(A)$,
   if and only if the noncontextual fraction $\mathrm{NCF}(e)$ equals $1$. This is
   the local-hidden-variable condition.
2. $e$ is no-signalling (its marginals agree on every overlap $C \cap C'$) if
   and only if $e$ has a *signed* global section: a $d : \mathcal E(M) \to \mathbb Q$
   with $\sum d = 1$ and the same marginals. (Abramsky–Brandenburger; the module
   computes such a $d$ by linear programming and the note verifies instances
   only.)
3. $e$ is strongly contextual ($G(e) = \varnothing$) if and only if
   $\mathrm{NCF}(e) = 0$.

Here $\mathrm{NCF}(e) = \max\{\sum_g \lambda_g : \lambda \ge 0,\ A\lambda \le e\}$,
the weight of the largest noncontextual sub-distribution, with dual the Bell
functional.

*Proof.* (1) A global section $d$ is a convex combination $\sum_g d(g)\delta_g$
whose stacked marginals are $Ad$; conversely a point of $\mathrm{conv}(A)$ is
such a $d$. Feasibility with $\sum\lambda = 1$ is exactly $\mathrm{NCF} = 1$.
(3) If $\lambda_g > 0$ then $e_C(g|_C) \ge \lambda_g > 0$ for every $C$, so
$g \in G(e)$; conversely $g \in G(e)$ makes
$\lambda = \min_C e_C(g|_C)\cdot\delta_g$ feasible with positive weight.
(2) is cited. $\square$

Executable, exact values:

| Model | $\mathrm{NCF}$ | $\Delta_{\mathcal O}$ ($\ell^1$ to the polytope) | $\lvert G\rvert$ | signed section |
| --- | --- | --- | --- | --- |
| PR box | $0$ | $2$ | $0$ | exists, with a negative entry |
| noisy PR, $\lambda = 1/4$ | $1/2$ | — | — | — |
| noisy PR, $\lambda = 1/2$ | $1$ | $0$ | $16$ | a distribution |
| mixture of two deterministic assignments | $1$ | $0$ | $2$ | a distribution |

Tests: `pr_box_is_strongly_contextual_with_zero_noncontextual_fraction`,
`noisy_pr_box_has_exact_noncontextual_fraction_two_lambda` ($\mathrm{NCF} = 2\lambda$
on the tested points), `tampered_receipts_are_rejected_by_replay` (a changed
fraction, functional or witness fails `verify_noncontextual_fraction` and
`verify_l1_defect`), `pr1080_embedded_lp_corruption_is_not_silently_accepted`
(on the noisy PR box at $\lambda = 1/4$: a cleared primal, a changed dual
entry, a changed primal entry, a zeroed LP value and a changed dual offset each
fail replay; at the reviewed head of PR #1080 only `lp.value` was read, so the
first three passed).

### 2.3 Descent, `NoGlobalExtension`, and what "local green, global red" means

The LGGR pathology is: every patch passes, the whole fails. For empirical
models the patches are contexts, "passes" is "has a section", and "the whole"
is a global section. The repository's descent classifier
(`finite_report_descent::classify_cover`) reports, for a target $U$, a cover of
$U$ and a presheaf of finite report sets, the matching families over the cover
and whether each glues: `Unique`, `Ambiguous`, or `NoGlobalExtension`.

The presheaf fed to it here is the *admissible assignment presheaf*
$S(U) = \{s \in \mathcal E(U) : s|_C \in \mathrm{supp}\, e_C \text{ for every maximal } C \subseteq U\}$,
on the down-closure of the cover plus any extra sets named (`admissible_presheaf(extra)`).
$S(M) = G(e)$.

**Proposition B4.**

1. Over the maximal cover $\mathcal C$ of $M$, every matching family of $S$
   glues. Hence `classify_cover(M, C)` never reports `NoGlobalExtension`; its
   fibers biject with $G(e)$, and strong contextuality shows up as *zero
   matching families*, not as a failed gluing.
2. Over a cover of $M$ by unions of contexts (arcs) that omits some context,
   `NoGlobalExtension` can occur for a noncontextual model.
3. $e$ is strongly contextual if and only if $S(M) = \varnothing$, if and only if
   every matching family over every cover of $M$ gets `NoGlobalExtension`.

*Proof.* (1) Given $s_C \in S(C)$ agreeing on overlaps, define $g(m) = s_C(m)$
for any $C \ni m$; agreement on overlaps makes $g$ well defined, and
$g|_C = s_C \in \mathrm{supp}\, e_C$ for every $C$, so $g \in S(M)$ and the
family glues to it; uniqueness holds because $g$ is determined pointwise.
(2) Witness: the Bell scenario with
$e = \tfrac12(\delta_{g_1} + \delta_{g_2})$, $g_1 = (a,a',b,b') = (0,0,0,0)$,
$g_2 = (1,0,0,1)$, so $\mathrm{NCF} = 1$ and $G = \{g_1, g_2\}$. Take the arcs
$\{a,a',b\}$ and $\{a',b,b'\}$, which omit the context $\{a,b'\}$. Each arc has
two sections ($a$ free on the left, $b'$ free on the right, with $a' = b = 0$
forced), all four pairs agree on the overlap $\{a',b\}$, and the glued
assignments $(a,0,0,b')$ lie in $S(M)$ only when $(a,b') \in \{(0,0),(1,1)\}$:
two fibers are `Unique` and two are `NoGlobalExtension`. The failure reports
the omitted context, not contextuality. (3) A gluing of any matching family is
an element of $S(M)$; conversely any $g \in S(M)$ restricts to a matching family
over any cover that glues to $g$. $\square$

**Consequence for LGGR.** `DescentOutcome::NoGlobalExtension` is a statement
about a cover: "these patches agree on their overlaps and no section of the
target extends them". It witnesses contextuality only when the cover's patches
jointly carry every constraint of the model, and even then only as "this
family fails"; the model-level fact is $S(M) = \varnothing$, which the
noncontextual-fraction receipt reports as $\mathrm{NCF} = 0$ with a Bell
functional as the replayable witness. An LGGR *event* is therefore defined
here as: a matching family over a cover of $M$ whose descent outcome is
`NoGlobalExtension`. An LGGR event is evidence that the cover's local checks do
not reach the global object; it is not by itself evidence that no global object
exists.

Executable: `maximal_cover_descent_never_reports_no_global_extension` (PR box:
$0$ families; noisy PR at $\lambda = 1/2$: $16$ families, all `Unique`),
`a_noncontextual_model_can_still_fail_descent_on_an_arc_cover` ($4$ families,
$2$ `NoGlobalExtension`, $2$ `Unique`, $\mathrm{NCF} = 1$).

### 2.4 The Čech complex, no-signalling, and the cocycle witness on a cycle

**Definition.** Let $N$ be the nerve of $\mathcal C$: vertices the contexts,
edges the pairs with $C \cap C' \ne \varnothing$, triangles the triples with
nonempty triple intersection. Čech cochains with values in the presheaf of
rational vectors $U \mapsto \mathbb Q^{\mathcal E(U)}$ are

$$
\check C^0 = \prod_C \mathbb Q^{\mathcal E(C)},\quad
\check C^1 = \prod_{C<C'} \mathbb Q^{\mathcal E(C\cap C')},\quad
\check C^2 = \prod_{C<C'<C''} \mathbb Q^{\mathcal E(C\cap C'\cap C'')},
$$

with $(\delta_0 \alpha)_{CC'} = \rho^{C}_{C\cap C'}\alpha_C - \rho^{C'}_{C\cap C'}\alpha_{C'}$
and $\delta_1$ the alternating sum of restrictions on triples.

**Proposition B5.** $\delta_1\delta_0 = 0$; and for an empirical model $e$
read as the 0-cochain $(e_C)_C$, $\delta_0 e = 0$ if and only if $e$ is
no-signalling. The quotient evaluator on 1-cochains,
$\Phi_1([\omega]) = \min_\alpha \|\omega - \delta_0\alpha\|_1$, is invariant
under $\omega \mapsto \omega - \delta_0\beta$.

*Proof.* $\delta_1\delta_0 = 0$ is the usual cancellation of the six terms on
a triple, using Lemma B2 for the composed restrictions. The second statement
is the definition of no-signalling read off the formula for $\delta_0$. The
third holds because $[\omega - \delta_0\beta] = [\omega]$ in
$\check C^1/\mathrm{im}\,\delta_0$. $\square$

$\Phi_1$ is owned by `omega_functional`; the module flattens $\delta_0$ to a
matrix and delegates to `omega_solvers::certified_phi1`, whose
`VerifiedExactPhi1` is replayed there. Executable:
`cech_coboundary_squares_to_zero_and_signalling_is_detected` (a tampered
marginal is reported with its context pair),
`cech_quotient_defect_detects_a_cocycle_outside_the_coboundaries` (a unit
cochain on one edge of the Bell nerve, a 4-cycle, has $\Phi_1 = 2$; every
$\delta_0\beta$ has $\Phi_1 = 0$; a cochain with a missing edge is refused with
`Shape`).

The shape of a cochain is checked as a whole before any incidence is read:
`delta0` requires one vector per context, of that context's section count;
`delta1` and `flatten1` require exactly the nerve pairs as keys, each vector of
the overlap's section count. So two empty vectors over two disjoint singleton
contexts (where the nerve has no pair), an extraneous key, a missing pair and a
short vector are all refused with `Shape`
(`pr1080_disconnected_cochain_shape_is_still_checked`; at the reviewed head the
first case returned an empty coboundary). On the Bell nerve
$\delta_1\delta_0 = 0$ is vacuous, there being no triple intersection; it is
exercised on the cover $\{\{0,1\},\{0,2\},\{0,3\}\}$, whose nerve has the
one triple $(0,1,2)$ over the shared measurement, where
$\delta_1\delta_0\alpha = 0$ for a non-constant $\alpha$ and a 1-cochain
supported on one pair has $\delta_1\beta \ne 0$
(`delta1_of_delta0_vanishes_on_a_nerve_with_a_triple_and_detects_a_non_cocycle`).

**What the 0-cocycle test does not see.** Every no-signalling model has
$\delta_0 e = 0$, the PR box included. So the test "$\delta_0 e = 0$" does not
separate contextual from noncontextual no-signalling models. That is a
statement about the test, not about the class of $e$: in the unaugmented
complex $\check H^0 = \ker \delta_0$, so distinct no-signalling models are
distinct classes and the class of $e$ determines $e$. What the class does not
carry is an invariant that separates $\mathrm{conv}(A)$ from its complement;
that separation is a positivity constraint, which is why the receipts of
section 2.2 are linear-programming receipts and not cohomology classes. The
cohomological witness that does separate something is the $\mathbb Z_2$
holonomy of parity constraints, next.

**Proposition B6 (parity cycles).** Let $m_0,\dots,m_{n-1}$ ($n \ge 3$) be
binary measurements, $\mathcal C = \{\{m_i, m_{i+1}\}\}$ with indices mod $n$,
and $e_i$ uniform on the two outcome pairs with $x_i \oplus x_{i+1} = t_i$.
Write $h = \bigoplus_i t_i$ for the holonomy. Then:

1. the nerve of $\mathcal C$ is the $n$-cycle (the triple intersections are
   empty), the $\mathbb Z_2$-valued 1-cochain $t$ is a cocycle, and
   $[t] = h \in \check H^1(N;\mathbb Z_2) \cong \mathbb Z_2$;
2. $G(e) \ne \varnothing$ if and only if $h = 0$, if and only if
   $t = \delta_0 x$ for some $x \in \mathbb Z_2^n$;
3. over the arc cover $\{m_0..m_{n-2}\}, \{m_1..m_{n-1}\}$ there are exactly two
   matching families, and both are `NoGlobalExtension` if $h = 1$, both
   `Unique` if $h = 0$;
4. $\mathrm{NCF}(e) = 0$ if $h = 1$ and $1$ if $h = 0$.

*Proof.* (1) Two consecutive contexts meet in one measurement; three
consecutive ones meet in nothing; on a graph every 1-cochain is a cocycle, and
$H^1$ of a cycle with $\mathbb Z_2$ coefficients is $\mathbb Z_2$, the class of
$t$ being the sum of its values. (2) A global assignment $x$ satisfies all $n$
constraints if and only if $x_{i+1} = x_i \oplus t_i$ for $i < n-1$ and the
closing constraint $x_{n-1}\oplus x_0 = t_{n-1}$, which after substitution
reads $h = 0$; that system is $t = \delta_0 x$. (3) Each arc carries $n-2$
constraints and has two sections (the value of its first measurement is free);
the left section fixes $x_1$, so each left section matches exactly one right
section; the glued assignment satisfies the closing constraint if and only if
$h = 0$. (4) If $h = 1$ then $G = \varnothing$ and B3(3) gives $0$; if $h = 0$
the two global assignments $x$ and $\bar x$ each restrict to one of the two
supported pairs in every context, so $e = \tfrac12(\delta_x + \delta_{\bar x})$
and $\mathrm{NCF} = 1$. $\square$

This is the Čech 1-cocycle witness over a cycle of agent contexts that the
mission asks for: $n$ agents, each seeing two neighbours, each pair locally
consistent, the whole inconsistent exactly when the holonomy is $1$. The
witness is replayable (`ParityCycle::report`), and on this family the
cohomological witness and the LP witness agree. On other families the
$\mathbb Z_2$ cohomological witness can be silent where the LP is not; that
false-negative behaviour is known and is not claimed away here.

Executable: `parity_cycles_holonomy_decides_descent_and_strong_contextuality`
for $n = 3, 4, 5$ and both holonomies.

### 2.5 Vorob'ev's theorem and Test 482

**Proposition B7.** If the hypergraph $(M, \mathcal C)$ is GYO-acyclic (reduces
to nothing by removing ears and absorbed vertices; equivalently, it has a join
tree), then every no-signalling model has a global section, given on the join
tree $T$ by the product formula

$$
d(g) = \frac{\prod_{C \in \mathcal C} e_C(g|_C)}{\prod_{(C,C') \in T} e_{C\cap C'}(g|_{C\cap C'})}
$$

with the convention $0/0 = 0$, where $e_{C\cap C'}$ is the common marginal.

*Proof sketch.* Induct on the number of contexts. Remove a leaf $C$ of $T$ with
neighbour $C'$; by induction the remaining family has a global section $d'$ on
$M' = M \setminus (C \setminus C')$ given by the formula. Set
$d(g) = d'(g|_{M'})\, e_C(g|_C)/e_{C\cap C'}(g|_{C\cap C'})$ when the
denominator is positive and $0$ otherwise. Marginalising over $C \setminus C'$
returns $d'$ because the ratio sums to $1$ for each fixed value on $C \cap C'$
with positive marginal; marginalising to $C$ returns $e_C$ because $d'$ has
marginal $e_{C\cap C'}$ on $C \cap C'$ by no-signalling. $\square$

The converse (for every non-acyclic hypergraph some no-signalling family has
no global section) is the other half of Vorob'ev's theorem; it is not
implemented, and the PR box on the 4-cycle is its instance here.

In code `Scenario::is_gyo_acyclic` and `join_tree` implement the reduction,
and `EmpiricalModel::acyclic_global_section` the product formula, refusing a
non-acyclic scenario with `NotAcyclic` and a signalling family with
`Signalling`. Executable:
`vorobev_product_formula_glues_acyclic_covers_and_refuses_cycles` (a
three-context path glues and the section's marginals are checked; the Bell
4-cycle is refused).

**Test 482.** The test on `main` named for Vorob'ev assigned
`is_gyo_acyclic = True` and asserted it. It exercised no hypergraph, no
reduction and no model; it was a tautology and is not cited as evidence anywhere
in this note or its ledger. It was rewritten on 2026-10-17 to run a GYO
reduction, glue two rational tables on the path cover by the product formula
with exact marginal checks, and exhaust the assignments of the cyclic parity
cover (ledger row B14).

### 2.6 The receipts

Both receipts are exact-rational linear programmes with replay.

- `NoncontextualFractionReceipt { noncontextual_fraction, contextual_fraction, noncontextual_part, bell_functional, lp }`;
  `verify_noncontextual_fraction` rebuilds the standard-form LP from the
  model, verifies the embedded `lp` as a certificate of that LP (lengths,
  nonnegative primal, $Ax = b$, $A^{\mathsf T} y \le c$, equal objectives) and
  binds it to the receipt: the first $n$ primal coordinates are the
  sub-distribution, the dual is the negated Bell functional, the value is the
  negated fraction. It then checks the sub-distribution, the functional and
  the fraction as before.
- `L1DefectReceipt { defect, coefficients, residual, dual_witness, dual_offset, lp }`
  for $\Delta_{\mathcal O}(e) = \min_{p \in \mathrm{conv}(A)} \|e - p\|_1$; the
  standard form has variables $(p, u, v)$ with $Ap - u + v = e$, $\sum p = 1$,
  objective $\sum(u + v)$. `verify_l1_defect_receipt` checks: the
  coefficients lie in the simplex, the residual equals $A p - e$ and its
  $\ell^1$ norm equals the defect, the dual witness has sup-norm at most $1$,
  $A^{\mathsf T}\varphi^* + y_0 \le 0$ coordinatewise, and
  $\langle \varphi^*, e\rangle + y_0$ equals the defect (zero duality gap);
  and it binds the embedded `lp`: $p$ is the coefficient vector and the dual
  is $(\varphi^*, y_0)$.
- `lp.pivots` is the solver's pivot trace. It is carried for reproduction of
  the run and is not bound by replay: a receipt with a changed trace and an
  unchanged solution verifies. The decision rests on the primal, the dual and
  the value, which are verified.

Sizes are refused before anything is allocated. `Scenario::section_count` is a
checked fold against `MAX_GLOBAL_ASSIGNMENTS` ($2^{20}$) and returns
`EnumerationLimit` where the reviewed head multiplied without a check (64
binary singletons have $2^{64}$ assignments; the product wrapped to zero in a
release build, `global_support` returned an empty support and
`is_strongly_contextual` returned `true`); every local section count and
`AssignmentPresheaf::from_rule` use the same fold. Dense matrices (the
incidence, both standard forms, the signed section) are bounded separately by
`MAX_LP_ENTRIES` ($2^{22}$ entries) and refuse with `LpSizeLimit`.
`pr1080_oversized_global_carrier_is_refused_without_overflow` checks the
refusal on `global_support`, `is_strongly_contextual`, `incidence`,
`l1_defect`, `admissible_presheaf` and `evaluate_l1_claim`, and at the local
level on one context of 21 binary measurements.

A tampered field fails replay (`tampered_receipts_are_rejected_by_replay`,
`pr1080_embedded_lp_corruption_is_not_silently_accepted`,
`convex_hull_distance_receipt_replays_and_rejects_shape_errors`).

---

## 3. Obligation C: the regress, the demarcation, and the gate

### 3.1 `WDP-CH14-T01` with its hypotheses made explicit

The monograph states: self-certification of factual correctness by an
autonomous process $S$ without external observer grounding is obstructed
along three independent axes. Each axis is restated here with the hypothesis
under which it holds and the status of its evidence on `main`.

**Axis 1 (well-foundedness of admission).** *Hypothesis:* $S$ admits rule
instances through an admission calculus in which every `AdmitInst` depends on
a previously admitted base datum (the Genesis calculus). *Statement:* with no
base instance, no rule instance is admitted, so $S$ has nothing to certify
(`collapsed_of_no_insts`). *Status:* the theorem name is Genesis's; only a
pinned copy of its ledger is on `main`, and it was not re-run. For a process
whose admissions are not of this shape, Axis 1 says nothing.

**Axis 2 (meta-carrier regress).** The monograph cites Tarski, `ENC-0118`,
Lemma D and `ENC-0195`. Tarski's undefinability theorem needs the diagonal
lemma, so it applies to a carrier $K_n$ whose language interprets enough
arithmetic; a finite carrier does not satisfy that hypothesis. The statement
that holds in both cases is this. *Statement:* let $\mathrm{eval}_n : K_n \to \{\mathsf{PASS}, \mathsf{FAIL}\}$
be $S$'s evaluator on carrier $K_n$. "$\mathrm{eval}_n$ is sound" is a
statement about the relation between $\mathrm{eval}_n$ and a standard of
correctness for $K_n$; that standard is not an element of $K_n$, so the
statement is a sentence of a carrier $K_{n+1}$ in which both $K_n$ and the
standard are objects. In the arithmetic case Tarski adds that no formula of
$K_n$ can serve as the standard. Either way, $\mathrm{eval}_n$'s own output
$\mathsf{PASS}$ on the sentence "$\mathrm{eval}_n$ is sound" is a value in
$K_n$ and not a sentence of $K_{n+1}$; it carries no standing at $K_{n+1}$,
which is what the monograph records as $\mathrm{AuthorityEffect}=\text{None}$
(`ENC-0195`). *Status:* the level statement is by construction (a sentence
about $K_n$ is not an element of $K_n$); the Tarski strengthening is standard
and conditional on the arithmetic hypothesis; Lemma D has no locatable
statement on `main` and nothing here rests on it.

**Axis 3 (relabeling blindness), derived without `NB-9`.** The monograph
cites `NS-14`, `NB-9` and `CL-13`. `NB-9` is refuted, so the axis is derived
from the other two together with a premise that the reviewed draft of this
note left implicit and that the review of PR #1080 showed to be necessary.

*Hypotheses:* (i) `NS-14`: an injective renaming $\sigma$ of presentation
tokens commutes with the transition step and with full-history replay;
(ii) `CL-13` (`passage_charge_const`): any quantity conserved by internal
transitions is constant on all reachable states and equals its genesis value;
(iii) *declared export:* the verdict $V$ reads a history only through a
declared export $\mathrm{Exp}$ built from internal receipts read up to
renaming and from conserved charges, so that $V = \bar V \circ \mathrm{Exp}$ and
$\mathrm{Exp}(\sigma(H)) = \mathrm{Exp}(H)$ for every injective renaming
$\sigma$. This is the premise the Argon synthesis's Proposition 3.1 states
when it posits two external states with identical accessible exports and
different required bindings: the identical export is assumed there, not
derived.

*Statement:* under (i)–(iii), $V(\sigma(H)) = V(H)$: a fixed $V$ cannot tell
a history from its relabeling. *Proof.* $V(\sigma(H)) = \bar V(\mathrm{Exp}(\sigma(H))) = \bar V(\mathrm{Exp}(H)) = V(H)$
by (iii). What (i) and (ii) contribute is that the exports named in (iii) are
in fact invariant: by (i) every replayable receipt of $\sigma(H)$ is the
$\sigma$-image of the corresponding receipt of $H$, so a receipt read up to
renaming is unchanged, and by (ii) every conserved charge takes the same value
on both. $\square$

*Why (iii) cannot be dropped.* Without it the conclusion is false. Take two
states $a, b$; let $\sigma$ swap them; let the one transition swap them, so
that (i) holds; let the only conserved charge be the constant zero, so that
(ii) holds; and let $V(H)$ be "the first token of $H$ is $a$". Then
$V((a)) = \mathrm{true}$ and $V(\sigma((a))) = V((b)) = \mathrm{false}$. This
$V$ is a function of the internal history, so the reviewed draft's "any
verdict that is a function of internal receipts and conserved charges" was
too wide: that $V$ reads the raw history, not an invariant export. The
renamed evaluator $\sigma(V)$, which reads $b$ where $V$ reads $a$, does
satisfy $\sigma(V)(\sigma(H)) = V(H)$; that is `NS-14` restated, and it is a
different statement from $V(\sigma(H)) = V(H)$. Axis 3 is about a fixed $V$,
and the two are kept apart here.

*Two claims that stay apart.* (1) An invariant defect can be detected by
internal computation when the supplied data determine it: $\Delta_{\mathcal O}(e)$
of section 2 is such a defect, computed from $e$ alone and certified by its
dual witness. (2) A relabeling cannot change that defect:
$\Delta_{\mathcal O}(\sigma e) = \Delta_{\mathcal O}(e)$ for a renaming of
outcome tokens, since the polytope is permuted onto itself. Claim (2) does not
deny claim (1), and the reviewed draft slid from the second into denying the
first. What Axis 3 adds is narrower than either. In the form of the no-go
used throughout this programme, with $E : W \to K$ the export and $q : W \to A$
a question about the world, $E(w) = E(w')$ and $q(w) \ne q(w')$ exclude any
$f : K \to A$ with $f \circ E = q$; the substantive obligation is to exhibit
the indistinguishable pair. Here the pair is $H$ and $\sigma(H)$ (identical
export by (i)–(iii)) and $q$ is a question that depends on the grounding map
$\pi_0$ of the tokens, such as "do the tokens of this history denote what the
tokens of that one denote", which a nontrivial $\sigma$ on grounded tokens
answers differently. So a drop in the internal defect is certified as a drop
(claim (1)), and what no export-reading verdict decides is whether the drop
is a repair, the same referents with a smaller defect, or a reinterpretation,
new referents under old tokens. That is the question about $\pi_0$ (the
synthesis's "Boundary Conclusion"), that is, about a declared observer in the
sense of section 1. The sentence "a process with no declared external observer
cannot certify that it has repaired anything rather than renamed it" is kept
in that reading only: the defect remains computable, and what is missing is
the grounding that makes "repaired" rather than "renamed" a fact about the
tokens.

*Where `NB-9` stood.* `NB-9` would have offered a route around this: a
commuting diagram together with an injective encoding as a certificate of
semantic transport. Its refutation (`budgetSim_enc_injective`: the square
commutes through budget writes alone) closes that route. The refutation
therefore does not weaken Axis 3; it removes the one internal object that
could have been mistaken for grounding. *Status:* (i) and (ii) are stated in
the Argon synthesis as theorems of Genesis; their Lean sources are not on
`main` and were not re-run. The derivation above is a two-line consequence of
them and is recorded as such.

**`WDP-CH14-C01` and `N03`.** The corollary (an unhosted token predictor
cannot issue self-authorizing certificates) follows from Axes 2 and 3 for any
process whose only outputs are presentations with no attached receipt and
whose evaluation of its own history, if it makes one, factors through its
internal exports as premise (iii) says; a process that reads a declared
external grounding is not unhosted. The nonclaim (`N03`) is kept: a process
coupled to an external oracle that emits receipts in the sense of
`WDP-CH15-D02` is outside the theorem, and that is precisely the coupling the
three-role gate asks for.

### 3.2 The demarcation: proposal engines and the unadmitted bridge

A *proposal engine* is any process whose output about a claim is a
presentation with no executable receipt for that output. Large language
models are proposal engines; so is a human writing a sentence. The
demarcation is not about species; it is about which of the three roles of
`WDP-CH15-D01` the output can occupy. An output with no receipt can occupy
the *proposer* role only.

Read the sentence **"I verified this and certify it"** as a provenance packet:

$$
\pi = (\text{proposer}, \text{evaluator}, \text{authorizer}) = (p, p, p).
$$

The authority note's role policy requires
$\mathrm{PairwiseDistinct}(\text{proposer}, \text{evaluator}, \text{authorizer})$
and adds that distinct identifiers do not ensure independent actors, so the
check is on principals as well. The packet above fails three times
(proposer $=$ authorizer, evaluator $=$ proposer, evaluator $=$ authorizer).
Under a regime whose policy permits self-attestation the same packet is
marked `SELF_ATTESTED`, which the note says no separated-roles regime
accepts.

**Why this is a sheaf bridge.** Let the *role cover* be the three roles, and
let the authority presheaf assign to each role the statements that role has
standing to make: to the proposer "$c$ is proposed", to the evaluator the
receipt $(c, \Delta, \varphi^*, \mathrm{status})$, to the authorizer "$c$ is
admitted under root $r$". A certificate is a global section over the role
cover: a compatible triple with the receipt and the root attached. The
sentence supplies one local section, the proposer's, and asserts the global
section. The gluing data, an evaluator's receipt from a different principal
and an authorizer's admitted root, is absent, so the assertion is a bridge
from a single patch to the global object that no descent datum admits. That
is the LGGR move of section 2.3 performed on the authority presheaf: the
proposer's patch is green and the global section is missing.

The mission names this `AP_AB_UNADMITTED_SHEAF_BRIDGE` and the rule it
violates `RULE_AUTHORITY_SEPARATION_001`. Neither name exists on `main`. The
nearest registered rule, `RULE_EVALUATOR_SUPREMACY_AUTHORITY_SEPARATION_001`,
already states the consequence: a passing checklist yields
`CHECKLIST_CERTIFIED` and never `AUTHORITY` without a verified terminal
witness. The anti-pattern name is proposed here as a candidate card, with the
packet above as its fixture case; it is unregistered until the pattern estate
takes it.

### 3.3 The three-role gate

`ThreeRoleGate(scope, admitted_roots)` reads a packet
`(claim_id, scope, proposer, evaluator, authorizer, observer, authority_root, policy)`
where each role binding is `(identifier, principal)` and `observer` is the
five-component declaration of section 1. Its verdicts:

| Packet | Verdict | Reasons |
| --- | --- | --- |
| three distinct principals, declared observer, admitted root, scope matches | `ADMITTED_FOR_AUTHORIZATION` | none |
| "I verified this and certify it": one principal in all roles | `REJECTED` | `SELF_AUTHORIZATION`, `EVALUATOR_IS_PROPOSER`, `EVALUATOR_IS_AUTHORIZER` |
| proposer signs as authorizer | `REJECTED` | `SELF_AUTHORIZATION` |
| two identifiers, one principal | `REJECTED` | `SHARED_PRINCIPAL` |
| a third principal hidden by counting (`id-A/p1`, `id-B/p1`, `id-A/p2`) | `REJECTED` | `SELF_AUTHORIZATION`, `SHARED_PRINCIPAL` |
| self-attested policy, admitted root | `SELF_ATTESTED` | none; valid only under that regime |
| any missing field, empty identifier, unknown field, unknown policy, non-string value, or missing observer component | `REJECTED` | the typed shape reason; never a default |

Every verdict, including admission, carries `authority_effect = "None"`:
the gate says the authorizer *may* act under the named root; the
certificate, if one is issued, is the external act of `WDP-CH15-D01`.
`GateVerdict` refuses construction with any other authority effect.
Expected verdicts are data in the JSON fixture, and a test checks that every
refusal reason is reached by some fixture case.

### 3.4 Public surface

Rust (`omega_sheaf_theory::empirical_presheaf`): `Scenario`, `EmpiricalModel`,
`NoncontextualFractionReceipt`, `L1DefectReceipt`, `l1_distance_to_convex_hull`,
`verify_l1_defect_receipt`, `AssignmentPresheaf`, `DescentSummary`,
`summarize_descent`, `ParityCycle`, `ParityCycleReport`, `ObserverDraft`,
`ObserverTuple`, `L1EvaluationProfile` with `KernelProfile`,
`AdmissibilityProfile`, `NormProfile`, `TerminalProfile`, `LayerProfile`,
`EvaluationStatus`, `EvaluationReceipt`, `evaluate_l1_claim`,
`EmpiricalError`, `AUTHORITY_EFFECT`, `DEFAULT_PIVOT_BUDGET`,
`MAX_GLOBAL_ASSIGNMENTS`, `MAX_LP_ENTRIES`, `TERMINAL_RULE_L1`,
`KERNEL_SUPPORT_PRESHEAF`, `ADMISSIBILITY_NONCONTEXTUAL`, `NORM_L1`,
`LAYER_DIAGNOSTIC`. `Scenario::section_count` returns `Result` and
`Scenario::kernel_label` names the carrier an observer declaration must bind
to. All arithmetic is `BigRational`; no path unwraps or panics on data.

Python (`omega_engine_pfp.domain.provenance`): `Role`, `RolePolicy`,
`VerdictCode`, `RefusalReason`, `PacketShapeError`, `RoleBinding`,
`ObserverDeclaration`, `ProvenancePacket`, `GateVerdict`, `ThreeRoleGate`,
`AUTHORITY_EFFECT`.

---

## 4. What this note does not show

- It does not show that `NoGlobalExtension` detects contextuality. Section 2.3
  shows the opposite on the maximal cover (vacuous) and on an arc cover (a
  noncontextual model fails).
- It does not show that the 0-cocycle test $\delta_0 e = 0$ detects
  probabilistic contextuality; section 2.4 shows every no-signalling model
  passes it. It does not say that the $\check H^0$ class of $e$ carries no
  information: in the unaugmented complex distinct models are distinct
  classes. The $\mathbb Z_2$ witness of B6 is exact on parity cycles and
  silent on other families.
- It does not show Axis 3 for a verdict that reads the raw history. Premise
  (iii) of section 3.1 is needed, and the countermodel there refutes the
  statement without it. It does not deny that an invariant defect is
  computable internally; it says that whether a change in it is a repair or
  a reinterpretation is a question about the grounding map.
- It does not show Lemma A2's second receipts for the norm and terminal rows
  by execution; the evaluator implements one norm and one terminal rule and
  refuses declarations of others.
- It does not re-run any Genesis theorem (`collapsed_of_no_insts`, `NS-14`,
  `CL-13`, `ENC-*`); those are cited by name as the monograph and the Argon
  synthesis state them.
- It does not cite `NB-9` as support for anything. It is refuted, and
  section 3.1 derives Axis 3 without it.
- It elaborates Lean only for the finite statements listed in ledger rows B1, B11 and L1; no other row is Lean-checked.
- It does not register an anti-pattern card or a rule; it proposes a name.
- It does not mint authority. Every receipt and every verdict carries
  `AuthorityEffect: None`, by construction and by test.

## 5. References

Bibliographic entries were not checked against publisher records in the
session that wrote this note; they are given as the author recalls them and
should be verified before any release.

- S. Abramsky and A. Brandenburger, "The sheaf-theoretic structure of
  non-locality and contextuality", New Journal of Physics 13 (2011) 113036,
  arXiv:1102.0264.
- S. Abramsky, R. S. Barbosa and S. Mansfield, "Contextual fraction as a
  measure of contextuality", Physical Review Letters 119 (2017) 050504,
  arXiv:1705.07918.
- S. Abramsky, S. Mansfield and R. S. Barbosa, "The cohomology of non-locality
  and contextuality", EPTCS 95 (2012) 1–14, arXiv:1111.3620.
- N. N. Vorob'ev, "Consistent families of measures and their extensions",
  Theory of Probability and its Applications 7 (1962) 147–163.
- A. Tarski, "Der Wahrheitsbegriff in den formalisierten Sprachen", Studia
  Philosophica 1 (1935) 261–405.
