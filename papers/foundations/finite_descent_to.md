# 008 Finite Descent To Gtfoc Projection

## GTOC Foundations — Quantum Contact Series (qm_008_finite_descent_to_gtfoc_projection)

**Date:** 2026-07-29 · **Version:** v1.0  
**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)  
**Status:** RELEASED  
**Authority:** `AuthorityEffect::None`  

## Mechanism inventory

| Slot | Value / Description |
| --- | --- |
| **Primitive Differences** | $\delta c = \text{{defect mass}}$ |
| **Carriers / Structure** | Finite Graph 0-Cochain / Hilbert Space |
| **Cochain complex** | $C^0 \to C^1 \to C^2$ |
| **Coboundary maps** | $\delta^0, \delta^1$ |
| **ZeroRel** | Preserved under $L_1$ quotient |
| **Licensed repairs** | None |
| **Quotient / Q1** | Banach Quotient |
| **Residuals** | $\delta c \neq 0$ boundary defect |
| **Witnesses** | Replayable Python / Rust Certifiers |
| **Observers / profiles** | Operational Observer |
| **Anomalons** | None |
| **CompletionLaw** | Finite Cochain Completion |
| **Terminal / route** | Route to 003 Quantum Foundations |
| **AuthorityEffect** | None |

The Finite Descent of QM to CODA-FOC — Completion & Census Projection
==================================================================

**This document is a census, not a result:** it records how far each load-bearing
ingredient of quantum mechanics currently descends down the Omega Tower toward the
finite obstruction calculus CODA-FOC (Ω∂), names the layer at which each *stalls today*,
and hands the open gaps off to two follow-on tracks. It proves no new theorem and mints
no authority; the conjecture that "few/maybe-unique versions of QM descend all the way,
and no other way" is recorded as an **open conjecture** (deferred; tracked as obligation
PL-QM013-2), not asserted. `[CENSUS / PROJECTION]`

Role: Internal maintainer map / release-control document (NOT a Zenodo paper).
Scope: the **finite physics of QM inside GTLA** — driving every load-bearing QM
ingredient *down* the Omega Tower to CODA-FOC (Ω∂), mapping how far each descends today.
Authority: **none minted.** This is a map, not a result. A sealed CODA-FDA-Q
`Pi_sharp` receipt can support a non-authoritative terminal route; it cannot
grant authority. Any promotion remains an external authenticated human decision.

Last synchronized against:
  QM_081 ledger: 2026-06-14
  QM_101 ledger: 2026-06-14
  QM_005 ledger: 2026-06-14
  QM_081 ledger: 2026-06-14
  QM_110 ledger: 2026-06-14
  QM_010 ledger: 2026-06-14
  QM_030 ledger: 2026-06-14
  Lean ledger: 2026-06-14
  proof ledger: 2026-06-14

Census aim (operator ruling 2026-06-13): **map current descent depths only.** The
"few/maybe-unique versions of QM descend all the way to CODA-FOC, and no other way"
statement is recorded here as an **OPEN CONJECTURE**, not a target this projection
commits to proving.

> **How to read this file.** §1 defines the bar ("descends to CODA-FOC"). §2 decomposes QM
> into ingredients and pins each to the layer it currently bottoms at. §3 is the
> formalism census (where each *version* of QM stalls today). §4 is the finite/continuum
> cut — which is exactly the **CODA-CS → layer-Q boundary**. §5 is the consolidated
> finish-off worklist. §6 hands off to the two tracks: **(1) Finite**, **(2) QM → Q**.
> Live status lives in `QM_Series_Paper_Map`, `lean4_ledger`, `proof_ledger`,
> and `QM_Series_Falsifiability_Ledger`; this file reorganizes them around the
> descent-to-CODA-FOC spine and does not restate per-row detail.

Status vocabulary (series-standard, kept separate from scope/evidence/authority):
`Derived | Imported | Conditional | Heuristic | Refused | Open |
Prose-proved-not-mechanized | Executable-witness-only | Lean-checked | Rust-tested |
Registry-relative | Packet-relative`.

**Why a maintainer (or reader) should care.** The QM series is large and accreted; it
is easy to lose track of which quantum ingredients have actually been driven down to the
finite obstruction calculus, which only *import* their structure, and which remain
continuum monsters. This census is the single sheet that says, per ingredient and per
rival formalism, *where it bottoms out today* — so that follow-on work targets the
genuine gaps (the §5 Lean worklist, the §4 continuum membrane) instead of re-proving what
already descends or chasing the deferred uniqueness conjecture. It is a reading map and a
gap ledger, not a claim of new physics. `[INTERPRETIVE / SCOPE]`

**Related work / nearest neighbours.** Within the corpus: `993_GTFOC` (the descent
target Ω∂), `000`/`000a`/`000b` (primitive obstruction axiomatics), `QM_081` (the
finite-descent realization paper), `QM_090` (the CODA-CS→Q continuum-shadow non-promotion
membrane), `9999_Q` (the layer-Q quarantine this census feeds), and `QM_Series_Falsifiability_Ledger` (the series
falsifiability ledger). In the wider literature the bar in §1 is adjacent to:
sheaf-theoretic contextuality (Abramsky–Brandenburger) for the Bell/KS obstructions in §2;
the reconstruction-of-QM program (Hardy; Chiribella–D'Ariano–Perinotti; Masanes–Müller)
for the §3 formalism census; and Gleason's theorem (Born uniqueness, imported, not
re-derived). This document differs from all of these by being a *descent-depth census*
under a fixed Authority Firewall — it ranks how far each result mechanizes down a finite
tower, and it explicitly refuses to mint authority or assert the uniqueness conjecture.
`[INTERPRETIVE / POSITIONING]`

**Falsifiability.** This census is wrong if any row of §2 or §3 misstates a descent depth
relative to the live ledgers it summarizes — i.e. if a load-bearing QM ingredient is
recorded here as bottoming at a layer (or carrying a finite packet) that the cited paper /
Lean file does not actually support, or if any item it records as still open is in fact
discharged in the cited source (or vice versa). It is also falsified if a "Lean-checked"
tag here names a target that `lake` does not check. `[SCOPE FENCE]`

> **What this document does NOT claim.**
>
> - It does **not** prove that QM (or any formalism) descends fully to CODA-FOC; it records
>   *current depths only* (operator ruling 2026-06-13). Several rows are still open or
>   conditional, and that is the correct state for a census.
> - It does **not** assert the uniqueness / "no other way" statement of §3 — that is an
>   open **conjecture**, deferred (§5.E; tracked as obligation PL-QM013-2), not a result of
>   this pass.
> - It mints **no** authority. No depth recorded here — zero or nonzero obstruction,
>   membership, coherence, transport, continuum limit, or registry/packet-relative
>   survival — confers authority; no CODA-FDA-Q terminal does so. None is supplied here, and any promotion is a
>   separate authenticated human decision.
> - It does **not** refute any rival formalism (real / quaternionic / GPT / epistemic).
>   Each is recorded as *stalling at a named finite layer with a named finite witness*,
>   which is a descent-depth statement, not an impossibility claim.
> - It states no new theorem; the formal content is owned by the cited papers and their
>   encyclopedia entries, not by this map.


1. The descent contract — what "descends to CODA-FOC" means


The Omega Tower bottoms out at **CODA-FOC = Ω∂**, the finite obstruction calculus
(published `theorem_ledger`; primitive axiomatics
`000_*`, `000a_*`, `000b_*`). The compressed CODA-FOC kernel is
**Difference → Repair → Quotient → Closure**.

A QM ingredient **descends to CODA-FOC** iff, on a **finitely-realized carrier**
(GTFOC-1 Finite Realization Gate / GTFOC-15 Target Realization — "no rabbit": larger
targets add no authority), it reduces to a **finite cochain obstruction**:

1. a quotient class in `Q¹ = C¹ / im(d₀)` (GTFOC-2, normed cokernel), with `d₁∘d₀ = 0`
2. an obstruction signature `(Φ₁, Γ₂, R_cl)` (the 000-series diagnostic; `Φ₁` quotient
   residual mass, `Γ₂` the `d₁`-closure charge) — the **minimal nonredundant basis**
   (GTFOC-L20A, `Φ`–`Γ` separation)

3. classified by the total, pairwise-disjoint diagnostic/refusal result
   `ExactClass | ClosedResidual | ActiveClosureFailure | Refusal`.
   The current machine-checked classifier uses historical constructor spellings;
   those spellings are decode-only and do not directly construct a terminal.

**Full descent** = a finite packet at *every* layer down the chain
`GTLA → Ω_ΛΩ → Ω_κ → Ω_O → Ω_χ → Ω_A → Ω∂`, **checked by the CODA-FDA (Ω_A) terminal-policy boundary**, with the
Authority Firewall held at every step: membership, coherence, transport,
completion, a continuum limit, registry-relative survival, and a sealed
CODA-FDA-Q `Pi_sharp` route **never** mint authority. Any bounded promotion is a
separate authenticated human decision. CODA-FOC
obstruction data — zero *or* nonzero — confers no authority by itself (993 ledger §17).

> **The finite-physics claim (informal target of Track 1).** "QM has finite physics in
> GTLA" means *every* load-bearing QM ingredient meets this bar. The uniqueness statement is an **open conjecture, deferred (see Appendix A; tracked as obligation PL-QM013-2)**. This projection
> maps the current state; it does not assert the conjecture.


2. Ingredient → descent map (current depths)


Each row: a load-bearing QM ingredient, the layer it currently bottoms at, the carrying
paper(s), the Lean target/file, current status, whether a finite packet exists, and the
gap remaining to clean CODA-FOC descent.

| QM ingredient | Bottoms at | Paper(s) | Lean target / file | Status (today) | Finite packet? | Gap to CODA-FOC | Source type |
|---|---|---|---|---|---|---|---|
| **State carrier / Hilbert selection** | Ω∂ (gauge selection) | `05_`, `01_`, pub `005`, pub `000a` | `QM.TraceZeroDuality` (dual-ball eigenvalue core; migrating from `PaperQF000`) | Conditional (carrier *imported*; gauge selected by operational axioms, not forced) | Yes (M₂ carrier, imported) | complex-vs-real-vs-quaternionic selection is registry-relative → §3, not forced at Ω∂ | maintainer census |
| **Probability / Born normalization** | Ω_O (import isolation) → Ω∂ (pairing) | pub `010`, `08_` | `QM.PaperQF002`, `QM.L010_01_BornRedundancy` (PL-010-1, migrating from `PaperQF002`); `QM.PairingNonSelection` (LT-K/LT-Q) | Normalization **Derived** (finite, Lean-hardened); Born *uniqueness* Imported/Conditional (Gleason); no-Born-without-pairing **Lean-checked** | Yes (ℓ¹ sector weights) | uniqueness never descends to Ω∂ as *forced*; stronger declared axioms would be needed to redirect LT-K/LT-Q | Lean-checked |
| **Effects / measurement pairing** | Ω∂ / Ω_χ | `08_` (O024) | `QM.PairingNonSelection` (LT-K) | Conditional selector audit (does **not** select Born); pairing non-selection **Lean-checked** | Yes (7-row pairing registry) | no current Lean gap for the non-selection firewall | Lean-checked |
| **CPTP dynamics / trace norm** | Ω_χ (transport) | `10_` (O025), pub `005`, O025a KCS pentagon | `LT-L TraceNonSelect` (Lean-checked); `LT-M stochastic ℓ¹` (Lean-checked); (exec) | CPTP-monotone **⊬** trace-norm-select (firewall); finite non-selection and classical shadow Lean-checked | Partial (imported channel) | O025 metric audit | Lean-checked |
| **Composition / tensor / purification** | Ω∂ (composition contracts) / Ω_χ | `11_`, `04_` | (exec) | Derived discipline gate; purification **Refused** w/o marginal + dilation | Partial | purification contract harness (missing prototype, index §9.3) | maintainer census |
| **Contextuality / no-go (Bell, KS, Gleason)** | **Ω∂ (native home)** | `01_` (results 006–009), P-KS (proposed) | `LT-C trichotomy` (Rust-tested; Lean Open), | Bell/CHSH = **exact CODA-FOC obstruction (Derived)**; KS refused-pending-packet; Gleason Imported (no finite-descent interface) | Bell yes; KS no; Gleason no | finite KS packet (P-KS) + Gleason finite-frame import | maintainer census |
| **Dynamics: path-sum / Feynman / generator** | Ω_κ-facing (CODA-A-Feynman) → Ω∂ for the graded core | `11_` (FWTE), `12_` | `LT-N sliced path-sum` (core `lsum_mul_right` Lean-checked; full Open), `LT-O overcount` (Open), `LT-P coboundary holonomy` (**Lean-checked, done**), `SemiringTransportKernel` | Finite graded path-sum Derived/Lean-core-checked; ungraded **overcounts 3:1** | Yes (graded finite histories) | `exp(tH)` / continuum generator **OracleNeeded** → §4 / Track 2 | Lean-checked |
| **Operator order / noncommutativity** | Ω_χ | `11_`, pub `013`, | (representation-pressure only) | Derived toy; representation pressure, not dynamics | Yes (toy) | does not promote to QM dynamics; remains representation-only | maintainer census |


3. Candidate-formalism census — current descent depths ("no other way" = OPEN)


Source: master-index §6 (interpretation/formalism audit) and §7 (where they are stuck),
reorganized as descent depth. **Uniqueness / exhaustiveness is an OPEN CONJECTURE (see Appendix A)**; this
table records only *where each version stalls today* and the finite witness of the stall.

| QM formalism | Deepest layer reached | Stall layer | Finite stall witness | What would move it | Source type |
|---|---|---|---|---|---|
| **Complex Hilbert QM** | Ω_A (local replay) | Ω_A (sealed) | `O021` sealed CODA-FDA `Pi_sharp` + multi-interface census open | seal one imported complex-Hilbert/CPTP packet (LT-target K / `O026`) | maintainer census |
| **Real Hilbert QM (rebit)** | Ω∂ / registry | Ω∂ (registry LT row) | local-tomography dimension `9 ≠ 10` (pub `010`,) | declare an alternate composition/interface package (not a refutation) | maintainer census |
| **Quaternionic QM** | Ω∂ (single carrier) | composition | `D₁ = 6` exact but composite **Refused** (no canonical tensor) (`012`) | supply a canonical declared composition package (not a refutation) | maintainer census |
| **GPT (square-bit / non-classical)** | Ω∂ (registry) | Ω∂ | self-duality + cone-homogeneity excludes the square candidate under declared axioms (`003`-adjacent,) | expand registry + prove minimal sufficient axioms | maintainer census |
| **Classical simplex** | Ω∂ (descends trivially) | — | classical gluing terminal | n/a (not QM; baseline) | maintainer census |
| **Spekkens epistemic toy** | Ω∂ (exact toy) | composition | one two-system table glues; broader family unaudited (`spekkens_*`) | declare broader composition family + replay | maintainer census |
| **Threshold / physical QC** | Ω∂ (toy repair) | architecture | `O1`–`O4`, `λ`,`μ`,`p_pair`,`Pi_sharp` open | architecture packet + checked evidence route + external human decision → **Track C** | maintainer census |

Reading: today, In the current maintained registry, **complex Hilbert QM is the only candidate
currently recorded as reaching local CODA-FDA replay** (sealed replay still open); every rival stalls at a **named** finite layer with a
**named** finite witness, and **none is refuted**. Whether that pattern hardens into
"complex-Hilbert is the unique full-descent survivor, no other way" is the deferred
conjecture (§5.E, future capstone; tracked as obligation PL-QM013-2) — **open**, not a
result of this census.


4. The finite/continuum cut = the CODA-CS → layer-Q boundary


This is the cut the operator's **layer Q** ($\Omega_Q$; now built — `9999_Q` v1.0.1, `Paper_Q` + `Paper_Q`) consumes. Q is the quarantine for **all surplus that outruns finite operational authority**, and that surplus is two kinds: **(a) continuum-math** monsters, routed via the CODA-CS (Ω_κ) finite-shadow membrane (§4a); and **(b) ontology / interpretation** surplus (Hilbert-space / wavefunction realism, measurement / observer / consciousness ontology, participatory realism), routed when the finite operational packet obtains a checked route while the interpretation claim is non-identifiable (§4b). Q mints **no** authority; it emits obstruction receipts. CODA-CS is the membrane for kind (a); the full GTLA/CODA-FDA/CODA-CS/CODA-A stack's failure-to-terminalize is the route for kind (b).

### 4a. Continuum-math surplus → Level Q via the CODA-CS membrane

CODA-CS (Ω_κ) is the existing continuum-facing layer of the tower; it is the **membrane** between the finite descent and the continuum monsters that Q holds.

**Track 1 — descends finitely (to Ω∂, conditionally):** ingredients 1–6 of §2 plus the
*graded* finite path-sum (7-core). These are the finite physics of QM.

**Track 2 — continuum monsters (route to Q via CODA-CS):** the objects that **cannot**
descend finitely and are currently `OracleNeeded` in the `27_` quarantine sidecar —
`exp(tH)` evolution generator, the continuum path integral, unbounded operators,
continuous spectra, infinite-dimensional Hilbert spaces.

**The membrane contract (the checked evidence exit from Q).** A monster leaves
quarantine as bounded evidence — without gaining authority — only by supplying all four CODA-CS ingredients
(`27_` §"finite-shadow requirements"):

1. a cofinal family of finite shadows
2. a certified refinement relation between shadows
3. a declared topology
4. a convergence certificate
then descending the certified shadow through CODA-CS → … → a checked CODA-FDA terminal-policy receipt. The route remains non-authoritative. Absent any
ingredient the intake returns `RefusedContinuumNoShadow` / `OracleNeededConvergence`.

**The CODA-CS ↔ Q interface (what to build for Track 2):**

| Element | Where it lives now | Needed for Q |
|---|---|---|
| Typed separation `ShadowFamily` vs `ContinuumKernel` | `LT-S ContinuumNonPromotion` (**LeanChecked**, `QM.ContinuumNonPromotion`) | the type boundary Q's intake enforces |
| Finite Feynman shadow replay `K_λ` | `LT-R` (Open), `12_`, | the shadow constructor feeding the membrane |
| Refusal terminals | `27_`, intake engine (`AlgebraicQFT` / `FeynmanFiniteShadow`) | Q's non-authority default |
| Non-promotion paper | **P-Continuum** — now published as `QM_090` (`QM_014_Continuum%20Shadow%20Non%20Promotion/QM_014_Continuum%20Shadow%20Non%20Promotion`) | the published statement of the membrane |
| Firewall guard | universal #4 (continuum membership ⊬ authority) | Q mints nothing |

> Q **holds** the monsters; **CODA-CS audits them downward.** Continuum elegance, a
> path-integral limit, or a TOE narrative carries no descent authority by membership
> (`27_` "No authority"; firewall universal #4).

### 4b. Ontology / interpretation surplus → Level Q (operator review 2026-06-14)

Level Q is now the official quarantine for QM **ontology surplus** — the interpretation claims that exceed finite operational authority. Discipline (per `9999_Q` v1.0.1): a quantum system represented by a Hilbert vector is **not thereby identical** with that representation (the chair/oak/tree seed); "being" is **repeatable descent + terminalization under a declared engagement mode** (`PrimitiveDescent` / `ModeBeing`), never an input predicate; and **finite descent permission = target factorization through the declared profile** (`FiniteDescentPermission`) — *local operational shadows may be green while the ontological target stays red*. The Hilbert worked example (`9999_Q` §8) is the direct bridge: a finite operational Hilbert packet terminalizes a prediction while marking "the system *is* the Hilbert vector" as `representation_only` — packet non-identifiability, **not** a refutation of wavefunction realism.

**Standard fence (the canonical paragraph QM finite papers carry).** Operational claims descend in the QM packet; ontology claims go to Q unless independently terminalized:

> **Level Q boundary.** This paper checks and routes only the finite operational claims declared in its packet; every route has `AuthorityEffect::None`. It does not promote Hilbert-space representation, wavefunction state, measurement formalism, observer language, or interpretation surplus into ontology. Such claims are routed to **Level Q** ($\Omega_Q$; `9999_Q`) as quarantined frontier probes. A Q receipt may record representation, obstruction, residual uncertainty, or a next admissible probe, but it is **not** authority for the quantum ontology claim and cannot promote itself.

Applied this pass to `05_`, `09_`, `13_`, `19_` (the ontology-exposed series papers). The freshly-republished `005`/`010` are intentionally left as-is. **Red line:** no QM paper may cite Q as proving or disproving any quantum interpretation; Q refuses promotion, it does not adjudicate truth.

**Mechanized 2026-06-14 (Track-2 + Phase C):** the CODA-CS→Q membrane is now Lean-checked — `LT-S` (`QM.ContinuumNonPromotion`: shadows ⊬ continuum kernel without a convergence certificate) + the **P-Continuum** paper (`qm_090_continuum_shadow_non_promotion`). The Track-A boundary firewalls (Deutsch/Everett/Wolfram; carried by `QM_091`/`QM_092`, the former 22–25 stubs now archived to `qm_archived_stubs_022_026`) are mechanized in `QM.PossibilityBoundaries`, and Born **Stage 2** (M₂ ℂ) in `QM.BornDefectCancellation`.


5. Gap ledger & finish-off worklist


Consolidated from `TARGETS` (Lean target ledger), master
index §8/§9.3, and the housekeeping found in this pass. Ordered roughly by leverage.
(The former `QM_011` publication-plan §3 P-series source was deleted from the corpus on
2026-06-18; the P-series items it carried are restated directly in D below.)

**A. Housekeeping / reconciliation (do first — cheap, unblocks accurate status):**

- **QM Lean home = `QM` (operator decision 2026-06-13).** All QM-series
  mechanization lives here: migrate the existing QM paper Lean
  (`PaperQF000.TraceZeroDuality`, `PaperQF002.PaperQF002`,
  `PaperQF002.L010_01_BornRedundancy`) into `QM`, and author every new QM
  `LT-*` target there. Tower GT* kernels stay in `Paper99x_*`. The shared
  tower/CODA-FOC primitives currently in `OmegaCore` that QM reuses
  (`FiniteObstructionTrichotomy`, `SemiringTransportKernel`, `AuthorityNonPromotion`,
  `TerminalDisjointness`, `ProjectionObstructionQuotient`, `RepairMonotonicity`,
  `PacketSchemaRefusal`) stay in `OmegaCore` and `QM` **imports** them — *open
  sub-point:* the operator may instead elect to move the QM-authored kernels into `QM`.

- `TARGETS` and `00_MASTER_INDEX` Lean paths are **stale**: GT* kernels moved
  `OmegaCore/ → Paper99x_*`; tower ledgers moved from the historical theory tree
  to the canonical Paper99x publication units; QM Lean now targets `QM`. Refresh both against these homes
  (master index partly refreshed 2026-06-13 §3.0c).

- `FiniteObstructionTrichotomy` **already exists** in OmegaCore — re-verify with
  `Lean replay` and update `LT-C/LT-E` status (the ledger may understate progress).

- Re-run `Lean replay` on the Tier-1 kernels (LT-B/D/E/F/T/P) and stamp green in
  `lean4_ledger` (the canonical Lean ledger; 17 is superseded by it).

**B. Finite track — Lean targets still Open (build order from 17 §"build order"):**
`LT-A` (AuthorityNonPromotion — started) → confirm Tier-1 green → `LT-C` (trichotomy,
general) → `LT-I` (M₂ classifier) → `LT-N`/`LT-O` (graded path-sum / overcount) →
`LT-L`/`LT-M` (trace non-select / stochastic ℓ¹) → `LT-J` (Born defect cancellation,
matrix last) → `LT-K`/`LT-Q` (pairing non-uniqueness / no-Born-without-pairing).

**C. Missing finite prototypes (index §9.3):**
finite Kochen–Specker packet (P-KS); purification composition contract harness; sealed
CODA-FDA-Q `Pi_sharp` replay (`O021`); multi-interface census (`O026`).

**D. New papers needed (P-series; the deleted `QM_011` plan's list, restated):**
P-KS (finite KS); P-PairingNonUnique (`08_`/LT-K); P-TraceNonSelect (`10_`/LT-L);
P-FiniteFeynman (LT-N/O). **P-Continuum (LT-S — the Track-2 bridge paper) is now published
as `QM_090`** (no longer outstanding). The Track-A boundary firewall (the former 22–25
stubs, archived 2026-06-18 to `qm_archived_stubs_022_026`; content already covered by
`QM_091`/`QM_092`) is mechanized in `QM.PossibilityBoundaries` — scoped strictly to
terminalization failure, never "X impossible."

**E. Deferred capstone (NOT in scope this pass; tracked as obligation PL-QM013-2):**
harden §3 from "current depths" into the uniqueness/"no-other-way" census. Recorded as an
**open conjecture** per the 2026-06-13 ruling; revisit only after Track 1's finite gaps
close. (Stronger ≠ more sweeping: closing the §5.B/§5.C finite gaps strengthens the census;
asserting the conjecture before they close would only overclaim.)

**F. Sweep cross-check (omega_sweeper 01–15, 2026-06-13; `sweep_01_15`).**
An offline deterministic run (`gate-api` OFF) over papers 01–15. The four obstruction passes
(P2/P3/P5/P7) were skipped, so the survivor / killed / open-obstruction census is **not
computed** — the empty `obstruction_report` / `failure_atlas` are an artifact of the
offline build, **not** a clean bill of health. Verified signal:

- **Structural skeleton clean:** P0 found no undeclared-symbol violations and P4 no
  layer-collapse pairs across all 15 (the series is layer-disciplined).

- **Track-C formalization backlog (NEW, verified):** paper `03_` carries 11 named theorems
  (Thm 1 @403 … Thm 6 @3119, line-verified). Thm 1 = LT-D; **Thm 2–6 + Lemma 1 + Cor
  3.1/3.2 are unformalized and uncovered by 17's LT-\* set** — the physical-QC *conditional
  no-go* cluster (Track C; carried by `QM_100`/`qm_100_projection_obstruction_technical_appendix`/`QM_101`, with `QM_021` absorbed into
  `QM_100`, and the former `26_`
  stub now archived to `qm_archived_stubs_022_026`), firewall-bound (conditional on architecture
  hypotheses, never "QC impossible"). This is a **third track** (physical-QC), distinct from
  Track 1 (finite CODA-FOC descent) and Track 2 (QM→Q); its Lean backlog is owned by the Track-C
  plan, not this finite plan.

- **"Blind spots" 01/15 corrected (token artifacts):** the high "thm-mention" counts are the
  word *theorem* as subject/reference, not hidden formal results — 0 formal theorem headers in
  either. `01_`'s real content is Result 001–014 (already in master-index §4 + code witnesses),
  `15_`'s is THR-001; both already inventoried. No new Track-1 gap.

- **Owed:** a **gated re-run** (`--features gate-api`, author ≠ gate per author-blind law)
  is what would empirically populate §2 (stall depths) and §3 (the census) as an adversarial
  cross-check of this hand-built projection. `operad_lattice` is produced only
  by a `perfect` run (currently absent).


6. Two-track hand-off


**Track 1 — Finite (finish the descent to CODA-FOC).**
Entry = §5.A housekeeping, then §5.B Lean build order, then §5.C/§5.D close the finite
gaps so every Track-1 ingredient in §2 meets the §1 contract. Guardrail: no target mints
authority; "Lean-checked" only when `lake` checks it; registry/packet-relative status
never silently becomes universal.

**Track 2 — QM → Q (continuum monsters via CODA-CS).**
Entry = §4. Formalize the membrane (`LT-S` / P-Continuum), define layer Q's intake
contract (the four shadow ingredients + the `ShadowFamily`/`ContinuumKernel` type
boundary + refusal terminals), and route the §4 monsters into Q. Guardrail: Q holds, CODA-CS
audits; nothing in Q mints authority. A certified cofinal shadow may support checked
bounded evidence through a CODA-FDA-Q terminal-policy receipt; any authority
promotion remains a separate authenticated human decision.

**Shared firewall (both tracks).** panepistimion-math-prof Authority Firewall, universal #1–#13
plus the Ω∂/Ω_A/Ω_χ/Ω_O/Ω_κ/Ω_ΛΩ layer-specific prohibitions. QM is a **realization
spine audited by the tower**, not a tower layer; authority is CODA-FDA-Q's alone.


**Companion:** `qm_008_finite_descent_to_gtfoc_projection Claim Ledger` (same folder).


Appendix A: Deferred Uniqueness Conjecture

The uniqueness statement — that the set of QM formalisms completely meeting the descent bar is small (conjecturally `{complex-Hilbert QM}` under declared axioms) and exhaustive ("no other way") — is an **open conjecture**. It is deferred (tracked as obligation PL-QM013-2) and not asserted by this census.

Appendix B: Alias Table for Stale Old Numbering

| Old Number | Alias / New Name |
|---|---|
| `000` / `000a` / `000b` | Primitive obstruction axiomatics / CODA-FOC |
| `01_` | QM_081 |
| `04_` | QM_101 |
| `05_` | QM_005 |
| `08_` | QM_010 |
| `10_` | QM_091 / QM_081 Trace Norm |
| `11_` | QM_101 |
| `12_` | QM_030 |
| `13_` | QM_008 |
| `14_` | QM_090 |
| `15_` | QM_092 |
| `19_` | QM_070 (Retired/Absorbed into QM_081) |
| `26_`, `27_` | QM_061 / Layer Q |
| `O021`, `O022`, `O024`, `O025` | Results tracked in QM_030 and related |

Version history

> **[RELEASE PREFLIGHT]** Do not release until the status table is generated from ledgers or manually reconciled line by line.

- **v0.2.0 (2026-06-18)** — first paper-hygiene-pipeline pass (Improver). Added the Part-A
  rubric block (lead-sentence payoff, why-care, related-work, falsifiability line, "what
  this does not claim" box); typed the uniqueness/"no other way" statements explicitly as
  ``OPEN`` (§1 box, §3 reading, §5.E); retired the deleted `QM_011` reference (§5, §4a) and
  the archived `22–26` stub references (now → `qm_archived_stubs_022_026` / `QM_091`,
  `QM_092`, `QM_100`, `qm_100_projection_obstruction_technical_appendix`, `QM_101`); pointed P-Continuum to its published
  home `QM_090`; fixed broken publication cross-links with percent-encoded targets;
  created the companion Claim Ledger. No depth-row content changed.

- **v0.1.0 (2026-06-13)** — initial maintainer-authored census / projection / outline.

<!-- claim-id-body-index:begin -->

Claim-ID body index (packaging)

| ID | Home |
|---|---|
| `QM-008-C1` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C2` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C3` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C4` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C5` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C6` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C7` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C8` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C9` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C10` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C11` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C12` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C13` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C14` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C15` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C16` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C17` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C18` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C19` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C20` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C21` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C22` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C23` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C24` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C25` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |
| `QM-008-C26` | [`finite_quantum_mechanics_claim_ledger.md`](../core/finite_quantum_mechanics_claim_ledger.md) |

<!-- claim-id-body-index:end -->
