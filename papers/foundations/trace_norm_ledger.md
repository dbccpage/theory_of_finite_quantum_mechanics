Claim Ledger — Paper QM_081 (O025): Trace-Norm and CPTP Transport Audit
=======================================================================

**Paper Key:** `003_quantum_foundations/081_trace_norm_cptp_transport_audit`  

Date: 2026-06-17
Version: v0.1 (Pre-Print)
Series: qm / QM Atlas
Companions: O024 = `qm_101_state_effect_pairing_audit.md` (Born-compatible pairing audit; upstream non-selection sibling), the O025a Kraus–Choi–Stinespring (KCS) transport pentagon, and `qm_030_gtq_quantum_realization_spine.md` §4.7 (the realization-spine firewall, of which §3 below is the finite mechanized instance). Source paper of the trace-norm material: published-005 (`000_cptp_invariant_obstruction_theory_trace_norm_geometry_and_quantum_dual_witnesses`), Theorems 1 & 2. Downstream: O026 (minimal quantum-interface survival theorem).

Firewall note: QM is a realization spine. QM_081 mints **no** tower authority.
It is a **conditional selector / non-selection audit** of trace-norm transport: it
separates the *imported* formal structure (CPTP maps, the trace distance, single-shot
state discrimination) from the *operational* metric, and shows that CPTP-monotonicity
**alone underdetermines** the metric. The controlling discipline is
$\mathsf{StructureDerived}(\mathcal F,c)\not\Rightarrow\mathsf{IsAuth}(t)$: a
contractivity/monotonicity replay *diagnoses* transport; it does not *authorize* and
never *derives* the trace distance, CPTP dynamics, or the Born rule. **CPTP, the
trace/trace-distance, and Born are IMPORTED throughout, never derived.**

Non-claim discipline (held throughout): the corpus does **not** claim "CPTP
monotonicity alone selects the trace distance" — that exact statement is *refused*
(§3, the non-selection firewall) and explicitly fenced as Strict Non-Claim 2. Trace
distance is conditionally admitted only once single-shot state-discrimination axioms
are imported (§4, [STANDARD, CONDITIONAL]); it is **not** a new derivation.

Standard-result note (def-as-theorem / standard-result watch): the §5 audit-target
inequality $\|\Phi(\rho)-\Phi(\sigma)\|_1 \le \|\rho-\sigma\|_1$ is the **standard
data-processing inequality** (trace-norm contractivity under CPTP maps; Nielsen &
Chuang Ch. 9, Wilde) — it is correctly typed `[STANDARD]` and **imported**, not
presented as a new "transport theorem." The genuinely proven content of this paper is
the §3 *non-selection* firewall (the mechanized scalar-family counterexample), not the
contraction inequality.

Securing note: QM_081's load-bearing content is secured in the encyclopedia `quantum`
layer under the **published-005** namespace (the trace-norm material is extracted from
paper 005, of which this audit is the finite mechanized realization): **ENC-0247** —
*CPTP Monotonicity Is Necessary but Not Sufficient* (INTERPRETIVE; MECHANIZED-PARTIAL;
backs §3, ENC Notes name "`10_trace_norm_cptp_transport_audit.md` §3"); **ENC-0246** —
*Conditional Trace-Distance Selection* (CONDITIONAL; NOT-STARTED; backs §4); **ENC-1055**
— *Column-Stochastic ℓ¹ Contraction* (MECHANIZED; backs §5.1, ENC source names
"`10_trace_norm_cptp_transport_audit.md` §5.1"). All three are indexed in
`indexes/ledgers/paper_005.md`. Per the QM-series sign-off precedent
(QM_081/006/007/008/009 — QM is a realization spine that mints no authority), **no
`paper_qm010.md` per-paper view is required**: QM_081 carries no theorem of its own to
extract beyond the published-005 entries it realizes.

Paper character: a **conditional selector / non-selection audit**. Its one positive
*proven* claim is a non-uniqueness firewall (§3, the scalar-family counterexample,
mechanized in LT-L). Every other load-bearing statement is either `[STANDARD]`
(imported data-processing / contractivity), `[STANDARD, CONDITIONAL]` (the
Holevo–Helstrom single-shot selection, conditional on imports), `[DEFINITION]` (the
four declared imports of §2), or `[PROVEN]` (the LT-M classical ℓ¹ shadow).

Claim index
-----------

| ID | Claim (abbreviated) | Status | Location |
|---|---|---|---|
| QM-081-C1 | **Non-selection firewall:** CPTP-monotonicity of a functional $j$ does **not** imply $j(X)=\tfrac12\|X\|_1$ — from any nonzero CPTP-monotone $j$, $j$ and $2j$ are two distinct CPTP-monotone functionals, so monotonicity cannot pin a unique functional and in particular does not single out the trace-norm shadow | [PROVEN — Lean-mechanized, non-selection direction] MECHANIZED-PARTIAL ENC-0247 (`QM.cptp_monotone_not_select`, `QM.cptp_monotone_not_select_traceNorm`, `QM.scale_monotone` axiom-free) | §3 |
| QM-081-C2 | The §3 counterexample is **non-vacuous**: under a genuine non-increasing contraction (the halving step $x\mapsto x/2$ over $\mathbb N$) both $\mathrm{id}$ and $2\cdot\mathrm{id}$ are CPTP-monotone and distinct | [PROVEN — Lean-mechanized] ENC-0247 (`QM.id_cptpMonotone_halving`) | §4.1 |
| QM-081-C3 | The half-trace-norm $D(\rho,\sigma)=\tfrac12\|\rho-\sigma\|_1$ is the **conditionally admitted** operational distinguishing metric under the four imports H1–H4 of §2 — an **admission of a standard result** (Holevo–Helstrom single-shot discrimination), **not** a derivation from first principles or from the CPTP property alone | [STANDARD, CONDITIONAL — conditional on imports H1–H4 of §2; Holevo–Helstrom] ENC-0246 (CONDITIONAL) | §4 |
| QM-081-C4 | **Trace-norm contracts under CPTP maps** (the data-processing inequality): for any declared CPTP map $\Phi$ and density states $\rho,\sigma$, $\|\Phi(\rho)-\Phi(\sigma)\|_1\le\|\rho-\sigma\|_1$ — the **standard** result, imported, not a new transport theorem | [STANDARD — data-processing inequality; Nielsen–Chuang Ch. 9, Wilde] | §5 |
| QM-081-C5 | **Column-stochastic ℓ¹ contraction** (finite classical shadow of C4): a finite column-stochastic kernel $S$ does not increase the ℓ¹ norm, $\|Sx\|_1\le\|x\|_1$; selects no metric, and (with C1) confirms contractivity/CPTP-monotonicity alone does not pin the trace norm | [PROVEN — Lean-mechanized over $\mathbb Q$] MECHANIZED ENC-1055 (`QM.stochastic_l1_contraction`) | §5.1 |
| QM-081-C6 | **Many** CPTP-monotone distinguishability measures exist (relative entropies, fidelity-based metrics, any positive rescaling of a monotone), not just the trace norm — the breadth that makes the §3 firewall reflect structure | [STANDARD — monotone-metric classification; Petz; Morozova–Chentsov] | §1.1, §3 |
| QM-091-D1 | The four declared imports of §2 (Quantum Interface $M_n(\mathbb C)$; Trace-Distance Axioms; CPTP Compatibility; Edge Additivity) are **definitions / scope fences**, not theorems — the audit's conclusions are conditional on them | [DEFINITION / SCOPE FENCE — the imported interface; conclusions conditional on these] | §2 |
| QM-091-N1 | **Strict non-claims:** (1) not a derivation of the Born rule or CPTP dynamics; (2) not a claim that trace distance is the unique metric for operational distinguishability; (3) not a physical assertion about channel authority | [SCOPE FENCE ×3 — the "what this does NOT claim" fence] | §1 |
| QM-091-N2 | **Scope of the §3 mechanization:** LT-L establishes the non-selection *direction* abstractly (two distinct monotone functionals); it does **not** mechanize the full analytic breadth claim that infinitely many unitarily-invariant norms / relative entropies are CPTP-monotone — that broader statement remains `[STANDARD]` (Morozova–Chentsov / Petz) | [SCOPE FENCE — mechanization scope; breadth half stays STANDARD, necessity half stays axiomatic per ENC-0247] | §3 |

Support ledger (Part C — upgrade paths)
---------------------------------------

| ID | What would upgrade it | Difficulty | Lean/numerical? | Global obligation |
|---|---|---|---|---|
| QM-081-C4 | **Mechanize operator trace-norm contractivity on $M_n(\mathbb C)$** — for every CPTP map $\Phi$ and Hermitian density $\rho,\sigma$, $\|\Phi(\rho)-\Phi(\sigma)\|_1\le\|\rho-\sigma\|_1$ — promoting §5 (C4) from `[STANDARD]` (imported prose) to `[PROVEN]` for the finite quantum interface. Currently only the classical ℓ¹ shadow (C5, LT-M) is mechanized | Non-trivial — needs Mathlib Schatten-1 + a CPTP (Kraus/Stinespring) encoding over $M_n(\mathbb C)$; the classical ℓ¹ case is the commuting specialisation. Standard but heavy | LEAN4 (**not honesty-gating** — §5 is correctly imported `[STANDARD]`; the paper's proven content is the §3 firewall, already mechanized) | PL-O025-1 (`proof_ledger_20260614.md`) |
| QM-081-C3 | **Mechanize the spectral Conditional Trace-Distance Selection** (ENC-0246, `lean_status: NOT-STARTED`): a homogeneous + unitary-invariant + classical-reduction gauge equals $\tfrac12\|\cdot\|_1$ on Hermitian trace-zero operators | Medium — a finite spectral reduction; ENC-0246 carries the prose proof | LEAN4 (**not honesty-gating** — C3 is correctly typed `[STANDARD, CONDITIONAL]`; the selection is an admission, not a claim) | ENC-0246 Lean-obligation row (S3); shares the trace-distance-selection program (PL-000BN-1, Paper 000a) |
| QM-091-N2 | **Construct (or refute the existence of) a CPTP-monotone *norm*** on Hermitian trace-zero operators not proportional to $\|\cdot\|_1$ — the breadth upgrade that would mechanize the full analytic non-selection landscape rather than only the scalar family | Hard — an open construction (`looks hard`; worth a counterexample hunt) | LEAN4 / Prose (**not honesty-gating** — breadth is correctly `[STANDARD]`) | PL-005-2 (`proof_ledger_20260609.md`; ENC-0527 breadth target) |

All three are **upgrade / hardening targets, not honesty gates**: the load-bearing
non-selection firewall (C1, §3) is already MECHANIZED-PARTIAL (ENC-0247 / LT-L), the
classical ℓ¹ shadow (C5) is MECHANIZED (ENC-1055 / LT-M), §5 is correctly imported
`[STANDARD]`, and §4 is correctly typed `[STANDARD, CONDITIONAL]` (an admission, not a
derivation). No obligation is duplicated here — PL-O025-1 / PL-005-2 are already logged
in the dated global ledgers, and the §3 and §5.1 Lean targets are recorded DISCHARGED in
`proof_ledger_20260614.md`.

Encyclopedia foundation (secured — for proof-signoff verification)
------------------------------------------------------------------

| ENC | Result | Status | Lean status | Backs |
|---|---|---|---|---|
| ENC-0247 | CPTP Monotonicity Is Necessary but Not Sufficient | INTERPRETIVE | MECHANIZED-PARTIAL (`QM/TraceNonSelect.lean`; `scale_monotone` axiom-free, others `propext`/`Quot.sound`) | §3 non-selection firewall (C1/C2); ENC Notes name "`10…` §3" |
| ENC-0246 | Conditional Trace-Distance Selection | CONDITIONAL (unitary invariance + classical TV reduction + homogeneity) | NOT-STARTED | §4 conditional admission (C3) |
| ENC-1055 | Column-Stochastic ℓ¹ Contraction | MECHANIZED | MECHANIZED (`QM/StochasticL1.lean`; `propext`/`Classical.choice`/`Quot.sound`) | §5.1 classical ℓ¹ shadow (C5); ENC source names "`10…` §5.1" |

All three are indexed in `indexes/ledgers/paper_005.md` (the trace-norm material is
extracted from published-005, of which this audit is the finite mechanized realization);
aliases tie to `paper:005:*` and `paper:O025:*`.

Lean (v4.31.0-rc1): the §3 firewall is mechanized in the **import-free** kernel
[index:index:TraceNonSelect.lean](omega_engine/research/_indexes/_master_index.yaml) (LT-L; theorems `scale_monotone`,
`cptp_monotone_not_select`, `cptp_monotone_not_select_traceNorm`, `id_cptpMonotone_halving`;
Mathlib-free, core `Nat`/`List`/`omega`). The §5.1 classical shadow is mechanized in
[index:index:StochasticL1.lean](omega_engine/research/_indexes/_master_index.yaml) (LT-M; theorem `stochastic_l1_contraction`;
`import Mathlib`, so a full `lake build QM` is needed to recompile it from cold). Both
were `lake build QM`-checked 2026-06-14 (`published/003_quantum_foundations/lean4_ledger.md` TRACE-001 LT-L,
STOCH-L1-001 LT-M).

Namespace note: the encyclopedia `paper_005.md` view and `lean4/PaperQF000/` belong to
**published-005** (CPTP-Invariant Obstruction Theory) — QM_081 is the QM-series finite
realization of that paper's Theorems 1 & 2 and secures under the published-005 entries
(ENC-0246/0247) plus the qm-extracted ENC-1055. This is *not* the `paper:NNN`
published-vs-QM alias collision affecting other QM papers (here the dependency is
intentional and tracked in the ENC sources).

Series-wide note (flag for the consolidation pass, **not** fixed here): this flat
paper's prose links to folderized siblings (QM_081/002/003/004/032/035/036) need
folder path segments; this is a pre-existing, series-wide link-hygiene issue, out of
scope for the per-paper rip. The legacy O-number references (O024, O025a) are likewise
left as-is per the in-paper QM_081↔O025 series-numbering bridge note.
