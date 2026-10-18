Claim Ledger — Paper 005: CPTP-Invariant Obstruction Theory Trace-Norm Geometry and Quantum Dual Witnesses
==========================================================================================================

**Paper Key:** `003_quantum_foundations/080_cptp_trace_norm_geometry_and_quantum_dual_witnesses`  

**Paper:** `000_cptp_invariant_obstruction_theory_trace_norm_geometry_and_quantum_dual_witnesses.md` (v0.1 Pre-Print, 2026-06-09)
**Pipeline stage:** Improver (Stage 1) pass of 2026-06-09; **GTOC/GTLA compliance pass 2026-07-17** (red note: `reviews/gtoc_gtla_red_005.md`).
**Verdict shape:** quantum branch paper, already audit-hardened (v002/v003 notes); the central demotion — CPTP monotonicity is compatible, not selecting — is prominent and enforced everywhere. One asserted-without-proof step in the worked replay repaired in the Improver pass.

**Compliance-pass verdict shape (2026-07-17).** This is the **highest import-density paper in the
001–009 block** — its title alone names four doctrine §3 import-list items. The pass found **no
overclaim of results**: the paper refuses the Born rule, refuses a universal quantum metric,
refuses CPTP-selection, and correctly scopes its Lean citation. Every P0 was a **declaration**
defect: the paper never *named and priced* what it borrows. Its imports enter as unpriced
**premises**, not smuggled **conclusions** — the converse of the usual QM-paper failure, and the
same shape as Paper 001's R3.

The structurally important finding, now recorded per-claim below: **most of this paper's
load-bearing mathematics is quantum-free.** Theorems 3, 4, and 6 hold for a finite digraph valued
in any finite-dimensional normed real vector space; delete $\mathcal H$ and they survive verbatim.
The "quantum" in the title qualifies the *imported representation*, not the results.

---

1. Claim-by-claim typing

------------------------

Columns added 2026-07-17 per doctrine §8 (import/oracle status; GTLA authority status). **Authority
is `none` for every claim** — the paper mints none, and the column records that the check was
performed per-claim rather than assumed globally.

| # | Claim (location) | Type | Import / oracle status | GTLA authority | Notes |
|---|---|---|---|---|---|
| C1 | Lead claim: $\ell^1(E;\mathrm{trace})$ is the obstruction geometry for replica-extensive observers with trace-distance local gauge | [PROVEN, CONDITIONAL + finite-dim Hilbert, trace-distance gauge, replica-extensive aggregation] | **IMPORTED** — finite-dim Hilbert space + trace norm are premises, never constructed | none | Conditionality stated in-line. |
| C2 | CPTP monotonicity necessary-not-sufficient demotion (header box, §2.3, §2.9) | [INTERPRETIVE / AXIOMATIC] (necessity) + [PROVEN BY COUNTEREXAMPLE] (non-sufficiency) | **IMPORTED** — CPTP maps | none | The corpus-audit demotion box is intact and load-bearing. |
| C3 | $V$ = Hermitian trace-zero operators; $\|X\|_{\mathrm{tr}}=\frac12\|X\|_1$ | [DEFINITION / STANDARD NORMALIZATION] | **IMPORTED** — $\mathcal H$, $B(\mathcal H)$, trace norm | none | Factor-of-two convention explicit; dual bound $\le\frac12$ tracks it. |
| C4 | Theorem 1 — conditional trace-distance selection | [PROVEN, CONDITIONAL + unitary invariance + classical total-variation reduction + homogeneity] | **IMPORTED (fully)** — spectral theorem, CPTP, density matrix $\rho$, tensor $\otimes$. Does **not** survive removal of $\mathcal H$. Axioms 2 & 4 (CPTP, tensor stability) are declared **inert** by the paper's own audit note + S4 — unpriced imports doing no work (red R9) | none | Spectral proof complete; audit note correctly separates load-bearing axioms (unitary invariance + classical reduction) from compatibility axioms (CPTP, tensor stability). Differences-of-distributions variant also proven. |
| C5 | Theorem 2(i) — CPTP necessity | [INTERPRETIVE / AXIOMATIC] | **IMPORTED** (CPTP) + **Q-gated** — "a physical open-system evolution" invokes physical dynamics, constructed nowhere | none | Honest: definitional once "operational gauge" presupposes data processing. |
| C6 | Theorem 2(ii) — CPTP non-sufficiency | [PROVEN BY COUNTEREXAMPLE] | **IMPORTED** — CPTP, trace norm | none | Counterexample = scalar family $c\|\cdot\|_1$; shows normalization not fixed. Breadth upgrade (non-proportional example) tracked as PL-005-2. |
| C7 | Broader monotone quantities (relative entropy etc.) | [INTERPRETIVE / STANDARD + citation [7]] | **IMPORTED** — [STANDARD + citation [7]] | none | Cited as landscape, not as alternative norms. |
| C8 | Theorem 3 — global $\ell^1(E;\mathrm{trace})$ | [PROVEN, CONDITIONAL / PARTLY DEFINITIONAL] | **Import-free core** — edge aggregation holds over any normed $V$; only the trace-distance *instantiation* is imported | none | Honest typing: aggregation form is near-definitional given edge decomposability; weighted form stated without normalization. |
| C9 | Theorem 4 — quotient invariance of $\Phi_{\mathrm{tr}}$ | [PROVEN] | **IMPORT-FREE** — finite derived shadow. Change of variables; holds for any normed $V$ | none | Complete change-of-variables proof. |
| C10 | Trace-zero dual ball lemma (in Thm 5) | [PROVEN] (matrix level); eigenvalue core [MECHANIZED] | **Split.** Eigenvalue core: **import-free** + machine-checked. Matrix lift: **IMPORTED** (spectral theorem), prose only — PL-005-1 | none | Self-contained: centered representative + Hölder + explicit attainment. **Re-verified 2026-07-17:** `lake build QM.TraceZeroDuality` exit 0 (8493 jobs); `#print axioms half_l1_isGreatest` = `[propext, Classical.choice, Quot.sound]`; zero `sorry`. Lean statement confirmed to match S1's eigenvalue core exactly. |
| C11 | Theorem 5 — quotient duality | [PROVEN, finite-dimensional convex duality + S1] | **Import-free core** — finite convex duality over any finite-dim normed $V$; the identification of $V^*$ is imported | none | Sion's minimax [8] cited with the compactness hypothesis identified; Lagrangian elimination of $d_0^*M\ne0$ explicit. |
| C12 | Theorem 6 — dual witnesses exist, divergence-free, bounded | [PROVEN, finite-dimensional] | **IMPORT-FREE** — finite derived shadow. Compactness + continuity only. The reading of $M_e$ as a physically measurable *quantum observable* is **Q-gated** (red R6) | none | Compactness + continuity; sign convention matched to $d_0$. A witness certifies a **number**, not a decision; it licenses no action. |
| C13 | $W_{\mathrm{tr}}$, $R_{\mathrm{tr}}$ signature components | [DEFINITION] | Import-free as definitions | none | |
| C14 | §2.9 final consolidated result | [PROVEN, CONDITIONAL on Theorem 1 operational axioms] | Inherits C4's imports | none | Restatement; conditionality carried. |
| C15 | Worked replay — one-qubit cycle, $\Phi_{\mathrm{tr}}=1$, witness $M=\frac12 Z$ | [WORKED EXAMPLE] | **IMPORTED** — $\mathbb C^2$, Pauli $Z$ | none | v1.2: single-cycle quotient formula justified in-line (cycle-sum invariance + triangle inequality + concentration). Python replay with expected output. |

**No claim status was changed by the compliance pass.** C10's mechanization row was *verified*, not
altered — the paper's own scoping ("Lean verifies the eigenvalue-level core; matrix lift in prose")
was already accurate and is now attested by an independent build receipt.

2. Definition-as-theorem audit

------------------------------

PASSED with the paper's own annotations: Theorem 3 is self-declared `PARTLY DEFINITIONAL`; Theorem 2(i) self-declared `AXIOMATIC`. Theorems 1, 4, 5, 6 are genuine derivations. No silent definition-as-theorem found.

3. Open obligations (global ledger cross-reference)

---------------------------------------------------

* **PL-005-1** — Lean matrix-level lift of the trace-zero dual ball lemma (spectral-theorem reduction from the machine-checked eigenvalue core). Hardening; not honesty-gating.
* **PL-005-2** — Construct (or refute existence of) a CPTP-monotone *norm* on Hermitian trace-zero operators not proportional to $\|\cdot\|_1$. Genuine upgrade: widens Theorem 2(ii) beyond the normalization family and tests whether classical total-variation reduction is independently necessary.

Inherited context: the operational-selection question (axioms uniquely selecting trace distance among CPTP-monotone gauges) is tracked corpus-wide as **PL-000BN-1** (Paper 000a); Theorem 1 here is the conditional version given classical reduction — it does not discharge PL-000BN-1 and does not claim to.

**Added 2026-07-17 (compliance pass) — [SCOPE FENCE], no new obligation opened:**

* **Degree-2 data absent.** The paper constructs $C^0$, $C^1$, and $d_0$, but **no $C^2$ and no
  $d_1$**. Consequently the closure law $d_1\circ d_0=0$ is unavailable, and a nonzero
  $\Phi_{\mathrm{tr}}$ **cannot be classified** as `ClosedSurvivor` vs `ActiveClosureFailure`. The
  paper classifies only $\Phi_{\mathrm{tr}}=0$ (`ExactRepair`, observer-relative) vs
  $\Phi_{\mathrm{tr}}>0$ (obstruction present, unclassified). Recorded in the paper's GTOC regime
  declaration under the doctrine §2 failure protocol. This is a **scope fence, not a defect** — the
  paper never claimed the survivor/active split, so nothing was downgraded.

* **Detector adequacy.** No `DetectorAdequacy` certificate exists for $\Phi_{\mathrm{tr}}$, whose
  blind spots are structural: it is a *quotient* norm (collapses coboundaries to zero by
  construction), edge-decomposable (blind to defects off declared edges), and replica-extensive
  (discards cross-edge orientation). Warning added at §2.8. Required before any authority-bearing
  GTLA use; not required for the paper's own diagnostic claims.

* **Q-gated, unconstructed:** physical realizability of $M^*$ as a measurement; identification of
  $\Phi_{\mathrm{tr}}$ with a physical distinguishability experiment.

4. Improver pass record (2026-06-09)

------------------------------------

* Part A rubric: all six elements verified present (no padding).
* Claims retyped: none (existing typing accurate, including the two self-demotions).
* Edits: single-cycle formula justification added to the worked replay; version lineage normalized (header v1.2 canonical); ledger files created/registered.

5. GTOC / GTLA compliance pass record (2026-07-17)

--------------------------------------------------

Red note: `omega_engine/research/published/reviews/gtoc_gtla_red_005.md`. Found 5 P0, 5 P1, 3 P2.

**Patched into the paper (5 P0, 4 P1):**

| # | Finding | Repair |
|---|---|---|
| R1 | Front-matter `Authority:` field described *results* — converting diagnostics into authority (doctrine §4, §9 rule 3) | `Authority: none.` + authority-firewall block; the result description moved to `Scope:`, where it is true |
| R2 | No GTOC/GTLA compliance note | `## GTOC / GTLA Compliance Note` added before References, concrete entries |
| R3 | Zero import declarations (`OracleNeeded`/`Q-gated`/`IMPORTED`/`SCOPE FENCE` all 0 hits) in the block's most import-dense paper | Import/Oracle boundary block + a 9-row concrete import register |
| R4 | Required QM-paper three-layer split absent (doctrine §7) | Three-layer split table: finite derived shadow \| imported representation layer \| Q-gated layer |
| R5 | §1 Genesis Bias — "state space of density matrices", "spatial points", "causal transport channels" presuppose a prior physical host (three §5F forbidden antecedents in two sentences) | Genesis-Bias Fence "No Prior Physical Host" + `GENESIS-BIAS AUDIT` answering **yes**, with the antecedent declared and priced rather than denied |
| R7 | No formalization-status firewall | Added at the §2.6 Lean citation |
| R8 | No detector adequacy for a wholly detector-relative paper | Detector-adequacy warning at §2.8, naming the three structural blind spots |
| R10 | L867 asserted *"there is no separate `PaperQF000` lib"* — **false** (`lakefile.lean` L59–60 declares it) | Clause struck and corrected in-place; build attestation refreshed to this pass |
| R6 | "quantum observable" / "observable certificate layer" reads a dual vector as physically measurable | Priced via the register + split (C12 row); no prose surgery (rule 16) |

**Not patched (recorded):** R9 (title advertises an axiom the paper's own notes call inert — fenced
at §0, retitling is out of scope); R11 (ledger status strings are freeform extensions of §8's list
but each is honest and maps to a legal status — rewriting accurate labels is churn); R12 (v003 note
calls S1 "non-load-bearing" while Theorem 5's label cites "+ S1" — both routes proved, labels
disagree about which is the spine); R13 (`PaperQF000/Witness.lean` is a toy whose sole theorem is an
identity function — **not cited by the paper**, so no overclaim; Lean tree outside write boundary).

**Invariants held:** no status upgraded; no version stamp bumped (v1.2 retained); no conjecture
deleted; no theorem restated; no claim promoted. Every Lean assertion independently verified
against the repo rather than accepted on the paper's word.
