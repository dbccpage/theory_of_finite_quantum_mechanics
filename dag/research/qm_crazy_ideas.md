# qm_crazy_ideas.md

**As of:** 2026-10-11

---

## Standing

The programme question, from `README.md` and `finite_quantum_mechanics.md` heading and §0, is: can quantum mechanics be presented on a finite carrier — and if not, exactly where does it break? Acceptable terminals are only two: the finite presentation closes on declared inputs, or it does not and the obstruction is exhibited.

Opened files do **not** claim either terminal. Paper version line is `v0.50.0` (2026-09-05), `AuthorityEffect: None`, status WORKING DOCUMENT. §0 refuses both “achievable” and “obstructed.” §7 refuses derivation of Born, complex structure, unitarity, tensor factorization, and continuous time (declared imports), and states that nothing here bears on the sealed derivation `sealed-derivation-v1` (`3100c4e`, cut 2026-08-17) in `dbccpage/19L57G1`. §9 (PR #205) withdraws the previous complete-derivation / minimal-carrier / all-HIT reading; both standing bets are `REVIEWED_MIXED_OPEN`; Gleason gaps 004 and 010 remain `OPEN (CONDITIONAL)`; strongest recorded result is scoped finite computation plus candidate Lean under declared carriers.

This file inherits that fence. Speculative programmes may attack remaining gaps. They may not mint authority, re-prove genesis, or treat a campaign banner as a mathematical close.

In-tree authority shadows used below (not as 19L57G1 text, which was not fetched):

- `lean4/OntologyBasic.lean`: current engine boundary `Real₀ = PrimitiveDifference ∪ Structure`; `ClaimPacket.HasAuthority` requires descent **and** an authoritative terminal status; representation-layer language does not have authority merely by being expressible.
- `lean4/OntologyPrimitiveBridge.lean`: `primitive_claim_no_authority_without_descent`.
- `research/090_interpretations_as_authority_shadows/interpretations_as_authority_shadows.md`: firewall `StructureDerived(x) ⇏ IsAuth(x)` (ENC-1063 cited; encyclopedia Lean path is not in this application lake).
- `research/004_general_obstruction_management_calculus/general_obstruction_management_calculus.md`: “Physical QM follows from GOMC: REFUSED.”
- `omega_engine/crates_rs/omega_certifiers/src/authority_minting.rs`: deprecated module seals evidence only; no item constructs authority.
- `omega_engine/crates_rs/omega_atlas_reconciliation/src/governance.rs`: a Model mints nothing; any authority-expanding change needs a complete ten-field licensed lift or is refused.

---

## Gaps

**Continuum & Functional Analysis Interfaces.** These define the boundary conditions, asymptotic scaling limits, and representation theorems connecting discrete carriers to infinite-dimensional continuum QM:

| ID | Title | Interface Characteristics |
| --- | --- | --- |
| GAP-F001-S000-002 | Continuum Hilbert lift & CCR | Wintner–Wielandt trace identity $\operatorname{Tr}([X,P])=0$ shows finite-dimensional matrices cannot represent $[X,P]=i\hbar I$. Discrete Weyl-Heisenberg groups over $\mathbb{Q}(\zeta_d)$ serve as discrete representations converging to continuous CCR as $d \to \infty$. |
| GAP-F001-S000-008 | Continuous time / Stone's theorem | Discrete dynamics $U^n$ classify periodic vs aperiodic orbits; continuous unitary flow $U(t)=\exp(-iHt)$ connects via Stone's theorem. |
| GAP-F001-S000-011 | Everett branch counting beyond $\mathbb{Q}$ | Exact rational-sector fine-graining (`FineGraining2`) reproduces Born weights; extending to general algebraic weights interfaces with infinite branches and continuous limits. |
| GAP-FQM-023 | Mixed-state von Neumann entropy | $S(\rho)=-\operatorname{Tr}(\rho \ln \rho)$ is transcendental over $\mathbb{Q}(\zeta_n)$ by Baker's theorem; evaluated via certified rational interval enclosures or continuum embeddings. |

**Conditional / open bridges the machine may attack (theorem, counterexample, or typed refusal on a declared carrier).** Appearing here does not close them.

| ID | Title | Honest remainder |
| --- | --- | --- |
| GAP-F001-S000-004 | Born uniqueness (Gleason) on projection lattices / dense cyclotomic spheres | `OPEN (CONDITIONAL)`. Finite Cabello/Peres/triad checks and `GleasonTheorem.lean` d=2 obstruction are not a topology or a non-Bornian frame function on `S(Q(ζ_n)³)`. |
| GAP-F001-S000-010 | Gleason dimension extra at n≥3 | `OPEN (CONDITIONAL)`. PR #205 withdrew historical `REFUSED-DERIVABLE`. H017Gleason falsifies a Bool cardinality surrogate, not uniqueness. |
| GAP-F001-S000-005 | U(1) circle construction | `open_bridge`, no status. H011Circle: Gaussian units and Fin 3 meet the named extra; continuity remains imported. |
| GAP-F001-S000-001 | Exact duality gap certificate | DualWitness is a 2-integer pairing bound plus Mermin–Peres sign parity; not QM_080 Thm 5–6. |
| GAP-F001-S000-006 | Hilbert tensor uniqueness | `CONDITIONAL_AXIOMATIC_CLOSURE` on four declared axioms; H062 does not prove necessity among bilinear maps. |
| GAP-F001-S000-007 | CPTP class | `DEFINED` via Choi PSD under a declared embedding; Stinespring still escalates conductor; H017Finish still has `finish_cptp_imported`. |
| GAP-F001-S000-012 | Ordered real embedding | `DECLARED_EXTERNAL_ASSUMPTION` (count=1), not a continuum-unclosable verdict. Mixed-state PSD is embedding-relative (n=5 witness). |
| GAP-FQM-003 | Named algorithms unimplemented | Register still asks for V_Q, four-way classifier including Refusal, descent audit, cofiber–Banach bridge. `cochain.py` is a 3-way numerical LP (`TOL=1e-9`). |
| GAP-FQM-019 | Unreplayed Mathlib snapshot | `lean4/original_lean_20260809` is absent. Replay or re-state; do not cite a dead path as proof. |
| GAP-C500-B01 | C500 original 250-target contract | Live tests keep 250 OPEN / launch preconditions `NOT_ESTABLISHED`. Naming `C500_FQMC1_CLOSURE.md` does not discharge T301–T550. |
| GAP-C1000-002 | No-signalling from Q(i) alone | Register type is `declared_assumption`, not a refused theorem (`claims/gap_register.yaml`). Description: no-signalling from admitted tensor + partial trace, not from the carrier. |
| GAP-C1000-006 | CHSH field supremum without height | At H=5, exact max on Q and Q(i) is 14/5; unconstrained cyclotomic supremum OPEN. |
| GAP-C1000-007 | Contextuality cohomology off Z₂ | Cabello global-section facts in Lean; H¹ classes bind to Python/receipts over Z₂ only. Z/Q/cyclotomic classes open. |

Specialist NEW- ids (not yet in the register) that a quiet machine should **ledger first**, not “solve”: Busch H058 uniqueness still a bridge; SRC-011 pairing audit has no surviving Lean; density off-diagonal coherence is an imported lift; operator Lüders is not derived; MUB(6) fourth basis is a live research problem; C_qa vs C_qc is a cited MIP*=RE guardrail, not a finite-carrier close.

---

## 19L57G1 reasoning machine

**SPECULATIVE.** This section is the reserved programme. It is not a standing claim that such a machine exists, works, or is licensed.

### External source status

Tried `web_fetch` on `https://github.com/dbccpage/19L57G1` and `https://github.com/dbccpage/19L57G1.git`: GitHub 404 page. Editor re-fetch 2026-09-18: still GitHub 404. Tried `web_search` for `19L57G1`, `dbccpage/19L57G1`, `sealed-derivation-v1 3100c4e`: no public repository, README, or Alpha Engine law text was retrieved. `https://github.com/dbccpage` did not yield a usable user/repo listing in this session. Treat the URL as **404 or private**. Do not invent 19L57G1 theorems. Outline below uses (i) this charter’s description — ontology / genesis / Alpha Engine law — and (ii) in-tree shadows that already cite the tag without rebuilding it.

Paper §7: no result in the finite_qm estate cites, rebuilds, or extends `sealed-derivation-v1` (`3100c4e`). README Non-claims repeat that fence. The machine **must keep that fence**. Citation of the tag is custody, not evidence for Born uniqueness, Hilbert lift, or campaign closure.

### What “ontology / genesis / Alpha Engine law” means here (reconstructed, not fetched)

Until 19L57G1 is readable, the working reconstruction — labelled **SPECULATIVE** and replaceable if the repo appears — is:

1. **Genesis (distinction before physics).** The only origin of a finite claim is a declared primitive difference. In-tree genesis is **not** `PrimitiveDifference.lean` as `D(x,y)=y-x`. Opened `lean4/PrimitiveDifference.lean` is an **abstract** `δ` with ZeroRel / residual quotient; a later Int kernel `diff x y := y - x` lives in the same file. Concrete coboundary `(d0 α)(u,v) = α(v) - α(u)` is `FiniteCochain.d0` / `omega_engine/crates/finite_qm/use_cases/cochain.py`. Hilbert space, Born, U(1), tensor, CPTP, and continuous time are representation layers, not genesis.
2. **Ontology (descent or typed refusal).** A claim packet is representation until it descends to Primitive Difference or Structure, or carries an explicit typed refusal (`OntologyBasic.lean` `ClaimPacket.Terminalized`). Positive authority additionally requires an authoritative terminal status. This application’s `AuthorityEffect` is None; the machine therefore **never** inhabits `HasAuthority` for a finite-QM claim. It may inhabit `refused`, `noRule`, or `budgetUnknown`.
3. **Alpha Engine law (no silent promotion).** Structure derived is not authority (`research/090_…`; `research/091_…` even demotes a vacuous `AuthorityNonPromotion` lemma). `omega_atlas_reconciliation` governance: a Model may not diagnose authoritatively; enforcement, diagnosis, voting, waiving, and doctrine revision are separated. GOMC explains residual accounting and **refuses** physical QM (`research/004_…`). Interpretations (Copenhagen, Everett, …) are packet-indistinguishable authority shadows unless they make a finite, distinguishable false claim (`research/090_…`).

If a future public 19L57G1 text contradicts this reconstruction, rewrite this section; do not keep a fan-fiction law.

### SPECULATIVE programme: a quiet methodical gap-attack machine

**Object.** A deterministic loop that consumes `claims/claim_ledger.yaml`, `claims/gap_register.yaml`, `claims/source_inventory.yaml`, campaign seals, and existing kernels, and emits only: a more precise statement, a file-backed test or Lean candidate, a typed refusal, a priced-import row, or `budgetUnknown`. It does not emit Atlas admissions, HIT scores as mathematics, or `AuthorityEffect` other than None.

**Quiet.** No completion banners. C250 review supersedes campaign completion interpretations; C500 withdrawal leaves all 250 original targets OPEN (`campaigns/c500_execution/WITHDRAWAL.md`); C750/C1000 README vs `sealed_targets.json` vs block_10 terminals currently disagree. The machine treats conflicting receipts as **open custody**, not as a vote.

**Methodical loop (proposed, not implemented as this agent).**

1. **Pick a row** typed ASSERTED, UNTYPED, OPEN, or CONDITIONAL (paper working loop, §6/README). State it precisely enough to be false. If it cannot be stated on a declared carrier, emit `noRule`.
2. **Bind evidence or unbind it.** A type stronger than ASSERTED requires an existing file (`finite_quantum_mechanics.md` §1–§2). Dead paths (`lean4/quantum_mechanics/original_lean_20260809`, legacy `code/`, `code_rs/src/continuum.rs`, encyclopedia `AuthorityNonPromotion.lean`) are false receipts, not proofs (GAP-FQM-019, GAP-FQM-003 prose, stale kernel paths).
3. **Classify the residual, do not narrate it.** Use the pointed classifier already in `PointedObstructionClassifier.lean`: `Phi=0` exact repair; `Phi>0, Gamma=0` stabilized survivor; `Phi>0, Gamma>0` open obstruction. `cochain.py` currently omits Refusal (GAP-FQM-003). The machine’s missing fourth bucket is **typed refusal / priced import**, not a fourth physics.
4. **Route by gap type.**
   - `Continuum / Functional Interface`: characterize the interface theorem, asymptotic scaling limit, or interval enclosure (002, 008, 011 beyond Q, FQM-023).
   - `OPEN (CONDITIONAL)`: investigate typed theorems or counterexamples on the declared carrier (004, 010).
   - `DECLARED_EXTERNAL_ASSUMPTION`: thread the explicit embedding through mixed-state and CPTP PSD checks (012).
   - `declared_assumption`: preserve explicit axiomatic declarations (C1000-002).
   - `false_receipt` / `missing_implementation` / `triage_required`: repair code paths and verification receipts (FQM-003, 019, C750 Lean layout, kernel paths).
5. **Licensed lift or verification.** Ensure proposed promotions of claims or code are backed by executed test suites and verified machine receipts.
6. **Defensible outcomes.** Settle claims on declared inputs, exhibit formal mathematical boundaries, or isolate open research questions.

**First work queue.**

- Address ledger-first IDs: H058 Busch uniqueness constructors; SRC-011 pairing audit; QM_012 diagonal-only densities; QM_021 operator Lüders rule.
- Verification and replay: Replay or update GAP-FQM-019 citations; reconcile 060-C4 with live `MixingObstruction.lean`.
- Interface management: Treat continuum interfaces (002, 008, 023) as external functional-analytic boundaries rather than internal finite-carrier derivations.

---

### SPECULATIVE idea 1 — Cochain as computational engine

Grounded in: `omega_engine/crates/finite_qm/use_cases/cochain.py`; `lean4/FiniteCochain.lean`; `WorldCycle3Quotient.lean`; `PointedObstructionClassifier.lean`; `omega_engine/crates_rs/omega_wdp/src/solver_of_solvers.rs` / `phi1_l1_boundary_solver.rs`; ledger `000:QMC-T1` ASSERTED; GAP-FQM-003.

**Idea.** Implement the cochain packet directly as an exact computational and verification engine: run exact $\Phi_1 / \Gamma_2$ descent on declared finite 2-complexes: primitive difference → coboundary nilpotence → quotient mass → classifier. `omega_solvers` already implements exact rational network simplex routines; modernize `cochain.phi_1` to exact rational solvers.

**Mathematical boundary.** Exact $\Phi_1$ evaluation on declared graphs is a concrete finite optimization task; distinguishing scalar vs cofiber representations maintains clean algebraic typing.

---

### SPECULATIVE idea 2 — Campaign as solver

Grounded in: `campaigns/{c250,c500,c500_execution,c750,c1000}/`; `check_result_schema.py`; `check_independence.py`; `omega_engine/code/tests/unit/test_c500_execution.py`; C750 `class/fqmi1_class.json`; C1000 `class/fqmr1_class.json`; GAP-C500-B01; GAP-C1000-010 nested type `open_question`.

**Idea.** Treat C250/C500/C750/C1000 not as human tournaments with HIT/MISS theatre but as a **frozen solver grammar**: a machine-readable class, a result schema, independence pins, and two acceptable block terminals (finite replacement priced, or named failure). `check_result_schema.py` already records that C250’s 65 OPEN verdicts were schema drift (“field missing or null”), not mathematics. A campaign-as-solver would refuse to emit a terminal that tests contradict (C500 still 250 OPEN; C750 README `NOT_STARTED` vs seals `EXECUTED`; C1000 tests `FQMR1_CLOSED_AT_DECLARED_CLASS` vs seals `NOT_STARTED`).

**Honest remainder.** Closing schema/seal hygiene is operator-judgment cheap custody and is **not** a spacetime theorem, not FQMC-1, not FQMI-1, not FQMR-1. GAP-C500-B01 is `no` for the original launch contract. GAP-C1000-002 is `declared_assumption`, not a refused theorem. Conflicting receipts do not close FQMR-1.

---

### SPECULATIVE idea 3 — Solver-frontier as the only selector

Grounded in: `lean4/SolverFrontier.lean`; `DualWitness.lean`; GAP-F001-S000-001; `omega_engine/crates_rs/omega_engines/src/obstruction_branch_search.rs` (lexicographic `(Phi_1, Gamma_2, Xi)`, `AuthorityEffect::None`).

**Idea.** Replace narrative “next paper” choice with the already-typed finite selector: a caller supplies a batch of plans, a verifier bit, and a strict cost; retain every verified non-dominated plan; choose no representative among ties. Costs would be declared (Lean replay hours, cyclotomic conductor, LP size), not “importance.” Dual-witness work would be exact Φ₁ primal/dual on named graphs, not QM_080 Sion/minimax by renaming.

**Honest remainder.** `SolverFrontier.lean` header: it does not prove the batch exhausts a grammar, that verifier bits are sound, or that a selected plan has authority. `obstruction_branch_search.rs` uses f64 diagnostics. Operator duality for Φ_tr remains an open_bridge. MIP* / C_qa vs C_qc is priced outside the finite host (specialist NEW-CQA-CQC-MIPSTAR).

---

### SPECULATIVE idea 4 — Atlas reconciliation as a live auditor (still AuthorityEffect None)

Grounded in: `omega_engine/crates_rs/omega_atlas_reconciliation/reconciliation_architecture_summary.md`; invariants I–III (primitive difference residual, cochain d₁d₀=0, identity conservation); two-axis honesty (no paper-only “mechanized” claims); `WorldWGOCSealedRefusal.lean` (finite refusal at a sealed REC-FULL entry; not a WGOC theorem).

**Idea.** Run reconciliation continuously over finite-QM rows: code ↔ claim ↔ paper ↔ proof ↔ contract, and fail any row that says MECHANIZED without a live file, or PROVEN without a lake receipt, or CLOSED while tests assert OPEN. Seed rows already exist for oversold statements and authority drift. Pair with `WorldObserverDirectedColimitNoGo.lean`: observer colimits are not a back door to continuum Hilbert.

**Honest remainder.** The crate is a diagnostic wrapper over metadata, not Atlas admission. This application is deliberately outside the Atlas (`README.md`). Sealed-derivation-v1 is not rebuilt. A green reconciliation run would be custody, not genesis.

---

Four other ideas is the cap. Further temptations (MUB(6) as a campaign-solver bake-off; Busch squeeze as a uniqueness engine; H074 Boolean table as an axiom-selection oracle) stay unlisted so they cannot be mistaken for a queue that closes 004/010/006.

---

## Effort and resources

Estimates are operator judgment. Priced-continuum items are **not closable** inside the finite programme. Person-week/month numbers are not evidence; residual duration words sit under this fence.

| Programme / surface | Effort (band) | Closable in finite? |
| --- | --- | --- |
| 19L57G1 machine MVP: packet schema, classifier, dead-path unbinding, governance-record gate, no authority bit | medium (tooling) | n/a (tooling). Does not close 004/010. |
| Replace reconstructed law with actual 19L57G1 text if the repo becomes public | cheap | n/a |
| GAP-FQM-003 four-way classifier + V_Q on declared graphs | medium for finite scalar identity; object-level cofiber identification refused (C1) | conditional / no for the C1 identification |
| Exact Φ₁ primal/dual (QMC-T1) on declared finite graphs | cheap–medium | yes, scoped; not Hilbert |
| GAP-FQM-019 Mathlib replay or Mathlib-free re-state | cheap if toolchain exists; otherwise re-state shadows already in `BornNormalization.lean` | yes as custody; not uniqueness |
| GAP-F001-S000-004 / 010 typed theorem or counterexample on declared dense cyclotomic spheres | hard; unknown outcome | conditional; **not** priced unclosable; **not** discharged by more finite rays |
| Busch H058 uniqueness for all additive effect frame functions on declared d=2,3 carriers | medium | conditional; YAML “resolved” overclaims the Lean header |
| GAP-F001-S000-005 U(1) construction | medium for Gaussian J-algebra restoration; continuity still imported | conditional for algebra; continuum for the circle |
| Campaign-as-solver hygiene (seals, README, tests, schema) | cheap | yes as custody; **no** for original C500 250-target contract |
| GAP-C1000-006 cyclotomic CHSH supremum without height | hard | conditional; does not prove Bell-as-nature |
| GAP-C1000-007 cohomology off Z₂ | hard | yes as finite classification; not operator KS |
| GAP-F001-S000-002, 008, 011 (beyond Q), FQM-023 | n/a | **not closable** in finite |
| Fourth MUB in d=6 | unbounded; may remain open | unknown; live research |
| C_qa vs C_qc / MIP* | n/a | **not closable** on the finite host |

Skills actually required if any programme is later staffed: Lean 4 without smuggling Mathlib topology; exact cyclotomic arithmetic; claim-ledger hygiene; refusal to treat pytest green as a theorem.

---

## What would change our mind

These are falsifiers for the **speculations**, not for quantum mechanics.

1. **19L57G1 becomes public** and states a different law (e.g. representation-layer minting, or a sealed derivation that this app is supposed to rebuild). Then this reconstruction is withdrawn, not “interpreted.”
2. **The machine emits `AuthorityEffect ≠ None`**, HIT-as-mathematics, or a campaign CLOSED while live tests assert OPEN. Then kill the machine; it has become the defect `check_result_schema.py` was written to catch.
3. **A file-backed dense-sphere Gleason theorem or counterexample** on a declared `Q(ζ_n)^d` lands in the application lake. Then 004/010 leave the speculative queue and become ordinary register work. Finite Cabello/Peres counts would **not** suffice.
4. **A finite construction of continuous U(1) or Stone’s theorem** without a branch-cut / completeness import. Then 005/008 pricing is wrong. H011Circle currently says the circle is not constructed; H055 currently says no Hamiltonian/log/exp/Stone.
5. **A proof that continuum completion is necessary for Born uniqueness**, or the opposite. Paper §9 explicitly says neither “probability wall is absolute” nor “completion is necessary” survives PR #205. Either theorem would change the 004/010 routing (still not by appearing in this file).
6. **Exact Φ₁ dual + Refusal classifier exist in-tree** with lake/pytest receipts. Then GAP-FQM-003’s “none of it exists as code” sentence is false (it is already stale about “five kernel routines” relative to 42 crate use-cases). That still would not close Hilbert lift.
7. **C500 live tests stop asserting 250 OPEN** under a new freeze, or the original contract is formally withdrawn as the test oracle. Until then, campaign-as-solver may not report FQMC-1 closed.
8. **Empty-list discipline fails:** a programme claims a source, Lean file, or 19L57G1 law it did not open. Then the programme is a narrative, and this file should say so.

---

## Sources opened

- `README.md`
- `finite_quantum_mechanics.md` (§0, §1 spine, §7 non-claims including 19L57G1 citation, §8 provenance, §9 PR #205 terminal scope)
- `claims/gap_register.yaml` (schema 1.0.0, `authority_effect: None`; F001, FQM, C500, nested C1000 ids)
- `claims/claim_ledger.yaml` (header; 000:QMC-T1..T6 ASSERTED; 001:QM-001-C1/C2; 002:C1/C3/C7; 060:QM-060-C4)
- `claims/source_inventory.yaml` (header; SRC-000..003 sample; `authority_effect: None`)
- `sources/` listing: retained `060_superposition_as_the_quotient_fiber/` (MixingObstruction + local lakefile) and `122_finite_hilbert_boundary_from_primitive_difference/` only
- `research/` listing (source-paper tree; **no** `finite_qm_roadmaps/` before this write; `coda_atlas/F004_papers` not present here)
- `research/004_general_obstruction_management_calculus/general_obstruction_management_calculus.md`
- `research/090_interpretations_as_authority_shadows/interpretations_as_authority_shadows.md`
- `research/092_qm_typed_authority_boundary_suite/qm_typed_authority_boundary_suite.md` (header)
- `research/121_the_finite_qm_ingredient_ladder/the_finite_qm_ingredient_ladder.md` (header/abstract)
- `omega_engine/crates/finite_qm/` (domain, 42 use-case `.py` including `cochain.py`, `finite_qm_engine.py`; entrypoints)
- `omega_engine/code/` (C750/C1000 Python, tests)
- `omega_engine/code_rs/` (remaining PyO3/C750/C1000 Rust)
- `omega_engine/crates_rs/` (including `omega_finite_qm`, `omega_quantum_physics`, `omega_engines`, `omega_solvers`, `omega_certifiers`, `omega_atlas_reconciliation`)
- `lean4/quantum_mechanics/` listing plus opened: `OntologyBasic.lean`, `OntologyPrimitiveBridge.lean`, `SolverFrontier.lean`, `PointedObstructionClassifier.lean`, `H074OperationalAxiomSelection.lean`, `WorldWGOCSealedRefusal.lean`, `WorldObserverDirectedColimitNoGo.lean`, `PrimitiveDifference.lean`, `FiniteCochain.lean`, `lakefile.lean`
- `campaigns/` listing; `c750/README.md`; `c500_execution/WITHDRAWAL.md`; `check_result_schema.py`
- `omega_engine/crates_rs/omega_atlas_reconciliation/reconciliation_architecture_summary.md`; `…/src/governance.rs`
- `omega_engine/crates_rs/omega_engines/src/lib.rs`; `…/obstruction_branch_search.rs`
- `omega_engine/crates_rs/omega_solvers/src/lib.rs`; `…/solver_of_solvers.rs`
- `omega_engine/crates_rs/omega_certifiers/src/authority_minting.rs`
- External: `web_fetch` `https://github.com/dbccpage/19L57G1` (404); editor re-fetch 2026-09-18 still 404; `web_fetch` `.git` URL (404); `web_search` for 19L57G1 / sealed-derivation-v1 (no public repo text retrieved)

Empty confirmation: encyclopedia path `lean4/007_authority_firewall/.../AuthorityNonPromotion.lean` was not found as a live application file; papers cite it. `lean4/quantum_mechanics/original_lean_20260809` is absent (GAP-FQM-019).
