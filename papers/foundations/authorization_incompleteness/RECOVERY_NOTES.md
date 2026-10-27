# Recovery notes: authorization as an incompleteness boundary

**Recovery date:** 2026-10-21. **Branch:** `auth-prose`. **Scope:** the prose half of the package.

Source: `C:\.ana\coda_university\coda_research\authorization_an_incompleteness_theory` (42 files, about 457 KB, read-only). The formal, code and evidence half (`formal/`, `code/`, `evidence/`, `*.json`, `formal_binding_manifest.md`, the PowerShell tooling) is recovered by the parallel branch `auth-formal`; this directory holds the prose half and this audit. Nothing in the source folder was executed.

Every recovered file keeps its source body byte-for-byte after a provenance header, and states "recovered verbatim; statuses below are the source's, not audited". The audit lives only in this file. Statuses in the recovered files (proved, closed, rooted, replayed) are the source's own words.

## 0. What the source is, and how it relates to what the repository already cites

- The package is a v0.14 research prospectus dated 2026-08-21: Primitive Difference to authorization to Turing-machine control experiments to a Rice-style lift. It is the earliest attempt in the user's own work to leave Genesis for computability: it never reaches a universal machine, and it says so (`computability_lift_admission.md`, `README.md:86-91`).
- The repository cites this package only as F000.S001 (`omega_engine_atlas/.../F000_finite/S001_authorization_and_incompleteness/001_authorization_an_incompleteness_theory`, external). TFQ-0327..0332 (`dag/derivations/04_authorization/`) summarise a **later atlas book** of that shelf: its chapters 01-06, gap ids `S001-GAP-*`, and Lean/Python names `ReportFactorization.lean`, `DescentAuthority.lean`, `TuringBarrier.lean`, `replay_fiber.py`, `MHC1`..`MHC5`. None of those names occurs in this source, and none of this source's names (`split_fiber_blocks_total_authorization`, `no_source_decider_blocks_total_authorizer`, `AIT-DTM0`, ...) occurs in the repository. The two are different versions of one line of work, so the repository holds the shelf-level frame and none of the theorem content recovered here.
- Two id schemes coexist in the source and collide: the ledger numbers AIT-0..AIT-9 (AIT-3 a definition, AIT-4 a proof checker), the proof program numbers AIT-G0..AIT-G8 (AIT-G3 the replay packet, AIT-G4 report adequacy). Only AIT-1=G1, AIT-2=G2, AIT-5=G5, AIT-6=G6 and AIT-7=G7 coincide; AIT-8 (a corollary) and AIT-G8 (the protocol that would support it) are related but not the same. This file uses the ledger spelling and gives both where they coincide.

Line coordinates below are **source** lines. A recovered line is the source line plus 6 (plus 4 for `goals.yaml`), because of the provenance header. File keys:

| Key | File (under `papers/foundations/authorization_incompleteness/`) |
| --- | --- |
| README | `README.md` |
| PAPER | `authorization_incompleteness_theory.md` |
| LEDGER | `authorization_incompleteness_theory_claim_ledger.md` |
| LOG | `authorization_incompleteness_theory_change_log.md` |
| CTS | `controlled_turing_derivation_series.md` |
| CLA | `computability_lift_admission.md` |
| SAS | `seal_derivation_series.md` |
| PP | `proof_program.md` |
| GOALS | `goals.yaml` |
| S-TH-P | `_support/authorization_incompleteness_theory_update_packet.md` |
| S-TH-D | `_support/authorization_incompleteness_theory_red_team_dialogue_raw.md` |
| S-G5C-P | `_support/authorization_incompleteness_g5c_terminalization_update_packet.md` |
| S-G5C-D | `_support/authorization_incompleteness_g5c_terminalization_red_team_dialogue_raw.md` |
| S-DTM1-P | `_support/authorization_incompleteness_dtm1_token_code_update_packet.md` |
| S-DTM1-D | `_support/authorization_incompleteness_dtm1_token_code_red_team_dialogue_raw.md` |
| S-DTM2-P | `_support/authorization_incompleteness_dtm2_input_execution_update_packet.md` |
| S-DTM2-D | `_support/authorization_incompleteness_dtm2_input_execution_red_team_dialogue_raw.md` |

## 1. Files recovered

| Recovered file | Role |
| --- | --- |
| `README.md` | directory README of the source (stale: still says v0.9) |
| `authorization_incompleteness_theory.md` | the paper, v0.14 |
| `authorization_incompleteness_theory_claim_ledger.md` | claim ledger, AIT-0..AIT-9 |
| `authorization_incompleteness_theory_change_log.md` | change log v0.1..v0.14 |
| `controlled_turing_derivation_series.md` | SEAL-TC-00..08 controlled Turing ladder and blind protocol |
| `computability_lift_admission.md` | AIT-G5b admission gate (eight fields) |
| `seal_derivation_series.md` | SEAL-AIT-00..08 derivation plan |
| `proof_program.md` | AIT-PD0..AIT-G8 goals |
| `goals.yaml` | machine-readable dependency graph of those goals |
| `_support/ (8 files)` | four producer-side Stage-0 dialogues and four update packets (direct machine, G5c, DTM1, DTM2) |
| `RECOVERY_NOTES.md` | this file |

The relative links inside the recovered files (to `formal/`, `code/`, `evidence/`) point at material recovered by `auth-formal`; they resolve only once that branch is merged.

## 2. Inventory

Every theorem, definition, claim id, derivation step, series item and goal of the prose half. Classification is against this checkout: **PRESENT** means the same content is already here (location given), **PARTIAL** means a real piece of it is here (what is missing is stated), **ABSENT** means nothing of it is here.

**Totals: 101 items; PRESENT 4, PARTIAL 29, ABSENT 68.**

### A. Claim-ledger and proof-program claims (32 items: PRESENT 3, PARTIAL 12, ABSENT 17)

| ID | Item | Source (file:line) | Repo status | Where in repo / what is missing | Recovered to (key:line) |
| --- | --- | --- | --- | --- | --- |
| AIT-0 | Definition: total certainty = soundness and completeness on a named domain and predicate | LEDGER:18; PAPER:209-211 | ABSENT | No definition of certainty in dag/ or papers/; TFQ-0330 uses terminals without defining it. | LEDGER:24; PAPER:215-217 |
| AIT-PD0 | Two extensions of one primitive interface with different validity and terminal policy | LEDGER:19; PP:12-39; GOALS:5-15 | PARTIAL | Supplied-validity-bit discipline is in TFQ-0328 and TFQ-0332 (prose). The two-extension model is absent. The interface itself is in lean4/PrimitiveDifference.lean (OmegaCore.PrimitiveDifference). | LEDGER:25; PP:18-45; GOALS:9-19 |
| AIT-PD1 | J011 quotient report pdProj: a validity predicate splitting a ZeroRel class cannot factor through it | LEDGER:20; PAPER:155-162; PAPER:244-265; PP:41-68; GOALS:24-37 | PARTIAL | TFQ-0332 names AIT-PD1 as a statement-level specialization with a supplied valid bit; no theorem. Interface present (lean4/PrimitiveDifference.lean: PrimitiveDifference, ZeroRel, classOf_eq_iff_zeroRel). The one-argument factor-through lemma is absent; deltaFactor_exists_iff_deltaCongruent is the two-argument analogue. J011_minimal_publication is not in this checkout. | LEDGER:26; PAPER:161-168; PAPER:250-271; PP:47-74; GOALS:28-41 |
| AIT-P0 | PO-000: a validity predicate splitting a report fiber has no decision by the report alone | LEDGER:21; PP:70-86; GOALS:38-47 | PRESENT | PG-HISTORY-REPORT-CRITERION (factor through report iff constant on fibers), PG-COLLAPSE-BARRIER. PO-000 itself (AuthorizationBoundary.no_report_decision) is external to this checkout. | LEDGER:27; PP:76-92; GOALS:42-51 |
| AIT-1 (= AIT-G1) | Split report fiber blocks every report-only total authorizer; equality-chain proof | LEDGER:22; PAPER:213-242; PP:108-124; GOALS:48-55 | PRESENT | PG-HISTORY-REPORT-CRITERION and PGW-REPLAY-NECESSITY (TFQ-0426: an auditor that sees only pi). The trunk statement is more general (iff, uniqueness). The Bool-validity "authorization" wording is not stated. | LEDGER:28; PAPER:219-248; PP:114-130; GOALS:52-59 |
| AIT-2 (= AIT-G2) | Constant self-receipt cannot decide a Bool packet; a bit-retaining report can | LEDGER:23; PAPER:267-279; PP:126-141; GOALS:56-63 | PARTIAL | PGW-REPLAY-NECESSITY is the auditor instance. The constant-receipt toy and the positive complete-receipt witness are absent. | LEDGER:29; PAPER:273-285; PP:132-147; GOALS:60-67 |
| AIT-E0 | Physical separation is neither necessary nor sufficient for bounded authorization (site-label toy) | LEDGER:24; PAPER:164-197; PP:143-170; GOALS:64-76 | PARTIAL | TFQ-0329 records that authorization is not treated as requiring an external host. The finite countermodel is absent. | LEDGER:30; PAPER:170-203; PP:149-176; GOALS:68-80 |
| AIT-TC0 | Tape control: read token, unread report, halt outcome and terminal policy are separate; control-only report splits a content contract | LEDGER:25; PAPER:395-441; PP:172-199; GOALS:77-92 | ABSENT | The presentation-versus-class and absence-versus-symbol disciplines exist (PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT, PGW-PREGENESIS-GRAMMAR); nothing about read, halt or policy. | LEDGER:31; PAPER:401-447; PP:178-205; GOALS:81-96 |
| AIT-TC1 | Frozen blind-derivation protocol (freeze, seal, post-seal literature audit) | LEDGER:26; PP:201-217; GOALS:93-105; CTS:369-405; CTS:46-63 | PARTIAL | Practice present: sealed Genesis 19L57G1, the second derivation and its post-seal audits (TFQ-0486, PGW-GENESIS-THREE-AXIS-VERDICT, PGW-RUNG0-INHERITANCE-REPLAY). The written protocol is absent. | LEDGER:32; PP:207-223; GOALS:97-109; CTS:375-411; CTS:52-69 |
| AIT-TC2 | Four-configuration transition table: one contract preserved, one countertrace, full report adequate, control report not | LEDGER:27; PAPER:442-451; PP:219-245; GOALS:106-122 | ABSENT | Conceptual analogues only (PG-GEN-NO-RETURN, PG-GEN-ONGOING-OBSTRUCTION, obstruction persistence in PG-GEN-REWRITING-COMMUTATION). | LEDGER:33; PAPER:448-457; PP:225-251; GOALS:110-126 |
| AIT-DTM0 | Direct finite-rule machine: total tape, left-biased lookup, fuel-bounded evaluator, halted/stuck/fuel-exhausted | LEDGER:28; PAPER:453-462; PP:390-415; GOALS:196-210; CTS:183-202 | ABSENT | No operational Turing-style semantics in dag/, papers/ or lean4/. lean4/HaltingQuotient.lean is a three-point pigeonhole fact (PO-023-C1/C2 in traceability_matrix.md), with no machine. | LEDGER:34; PAPER:459-468; PP:396-421; GOALS:200-214; CTS:189-208 |
| AIT-DTM1 | Finite List Nat token code for DTM0 machines; decodeMachine_encodeMachine; four rejection fixtures | LEDGER:29; PAPER:464-473; PP:417-441; GOALS:211-223; CTS:204-231 | ABSENT | No machine encoding anywhere in the repository. | LEDGER:35; PAPER:470-479; PP:423-447; GOALS:215-227; CTS:210-237 |
| AIT-DTM2 (planned) | Length-delimited initial-input request grammar and result-level agreement with DTM0 | S-DTM2-P:1-119; S-DTM2-D:1-138 | ABSENT | Planned in the source only: seven target theorems named, no Lean file, and no entry in ledger, proof program, goals.yaml, change log or paper. | S-DTM2-P:7-125; S-DTM2-D:7-144 |
| AIT-G3a | Finite structural replay model: trust root, exact submission, receipt, four substitution attacks | LEDGER:30; PAPER:607-618; PP:247-274; GOALS:123-139 | PARTIAL | TFQ-0505 (Alpha M1-M8: License bound to source, target, measure and bounds; mismatches refused) and TFQ-0331 (packet attached to a named terminal). The structural trust-root/receipt model is absent. | LEDGER:36; PAPER:613-624; PP:253-280; GOALS:127-143 |
| AIT-G3 | Byte-bound SHA-256 replay packet, 23 unit cases, 21 rejected mutations | LEDGER:31; PAPER:619-628; PP:276-302; GOALS:140-153 | PARTIAL | TFQ-0216 and TFQ-0217 (replay hash; a digest does not widen the statement). The packet itself is code-half material. | LEDGER:37; PAPER:625-634; PP:282-308; GOALS:144-157 |
| AIT-G4 | Executable report adequacy: full report adequate, control-only report routes to open | LEDGER:32; PAPER:503-517; PP:304-327; GOALS:154-166 | ABSENT | - | LEDGER:38; PAPER:509-523; PP:310-333; GOALS:158-170 |
| AIT-G5a | Class-relative transport of a no-decider boundary through a validity-preserving reduction | LEDGER:33; PAPER:311-321; PP:329-355; GOALS:167-179 | ABSENT | - | LEDGER:39; PAPER:317-327; PP:335-361; GOALS:171-183 |
| AIT-G5c | Terminalization consequence: no closed two-sided sound terminalizer under a no-decider premise; Boolean fixture | LEDGER:34; PAPER:323-341; PP:357-389; GOALS:180-195 | PARTIAL | Terminal vocabulary only (TFQ-0330: authorized, rejected, unresolved, refused, not admitted). No theorem. | LEDGER:40; PAPER:329-347; PP:363-395; GOALS:184-199 |
| AIT-G5b | Computability-carrier admission gate (eight frozen fields) | LEDGER:35; PP:443-467; GOALS:224-243; CLA:1-120 | PARTIAL | TFQ-0330 cites S001-GAP-MHC3-MHC5: proposal-language coverage, ordinary-computable decision-class binding and replayed custody. These are three of the eight fields, by name only. | LEDGER:41; PP:449-473; GOALS:228-247; CLA:7-126 |
| AIT-3 | Logical authorization boundary: fixed contract, checker, semantics and replay root outside proposal-controlled content | LEDGER:36; PAPER:164-211; PAPER:580-632 | PARTIAL | TFQ-0329 (no forced external host) and TFQ-0331; the stated definition is absent. | LEDGER:42; PAPER:170-217; PAPER:586-638 |
| AIT-4 | Local proof checker decides a fixed proof-object language (Necula 1997) | LEDGER:37 | ABSENT | External citation; no counterpart. | LEDGER:43 |
| AIT-5 (= AIT-G5) | Rice lift: no total computable sound-and-complete authorizer for a nontrivial extensional property | LEDGER:38; PAPER:299-309; PP:469-496; GOALS:244-256; CTS:325-338 | ABSENT | No Rice or halting statement in dag/ or lean4/. Mathlib carries ComputablePred.rice, rice₂ and halting_problem (see section 4). | LEDGER:44; PAPER:305-315; PP:475-502; GOALS:248-260; CTS:331-344 |
| AIT-6 (= AIT-G6) | Second-incompleteness self-soundness boundary | LEDGER:39; PAPER:343-357; PP:498-513; GOALS:257-264; CTS:340-352 | ABSENT | Mathlib has only the Goedel beta function, no incompleteness theorem. | LEDGER:45; PAPER:349-363; PP:504-519; GOALS:261-268; CTS:346-358 |
| AIT-7 (= AIT-G7) | LLM-only corollary: a computable proposal source cannot supply total semantic authorization | LEDGER:40; PAPER:519-554; PP:515-538; GOALS:265-274; CTS:354-367 | PARTIAL | TFQ-0330 names AIT-7 and forbids citing it as closed; no statement. | LEDGER:46; PAPER:525-560; PP:521-544; GOALS:269-278; CTS:360-373 |
| AIT-8 | A passing replay licenses only the policy scope of an independently fixed checker | LEDGER:41; PAPER:580-632 | PARTIAL | TFQ-0506 (zero residual, replay, packet admission never authorize), DS-QM090-092-AUTHORITY-FIREWALL, TFQ-0221. | LEDGER:47; PAPER:586-638 |
| AIT-9 | Sealed derivation record is evidence about mechanical gates, not semantic correspondence | LEDGER:42; PAPER:634-663 | PRESENT | TFQ-0327 (the sealed tag is a mechanical command receipt, not a verdict on the mathematics) and PGW-GENESIS-THREE-AXIS-VERDICT. | LEDGER:48; PAPER:640-669 |
| AIT-G0 | Contract vocabulary freeze | PP:88-106; GOALS:16-23 | ABSENT | - | PP:94-112; GOALS:20-27 |
| AIT-G8 | Attacked authorization protocol (proposal, checker, receipt, terminal policy) | PP:540-553; GOALS:275-283 | ABSENT | - | PP:546-559; GOALS:279-287 |
| Stopping condition | Conditions for stating the LLM conclusion as an in-tree result | PP:555-568 | ABSENT | - | PP:561-574 |
| Ledger: exact statements | Ten theorem statements presently formalized | LEDGER:45-91 | ABSENT | - | LEDGER:51-97 |
| Ledger: required status | Seven requirements before a public global sentence | LEDGER:93-111 | ABSENT | - | LEDGER:99-117 |
| Nonclaims | Ledger nonclaims (7) and paper section 8 nonclaims (9) | LEDGER:113-126; PAPER:688-711 | ABSENT | - | LEDGER:119-132; PAPER:694-717 |

### B. Paper-level content not carried by a ledger row (13 items: PRESENT 1, PARTIAL 2, ABSENT 10)

| ID | Item | Source (file:line) | Repo status | Where in repo / what is missing | Recovered to (key:line) |
| --- | --- | --- | --- | --- | --- |
| P-01 | Omega Engine primitives binding table | PAPER:19-38 | ABSENT | - | PAPER:25-44 |
| P-02 | Starting-interface chain: primitive difference, quotient, report, validity, evaluation, replay, terminal | PAPER:101-128 | PARTIAL | TFQ-0327..0332 are chapters 01-06 of the later atlas book in the same order; the chain statement itself is absent. | PAPER:107-134 |
| P-03 | P0 descent discipline: evaluation and authorization must descend through the report | PAPER:130-153; README:64-78 | PRESENT | PG-HISTORY-REPORT-CRITERION and the descent vocabulary of the L1-to-L2 stage (FQ-PHASE-BLIND-DESCENT-ZERO-RETAINED). | PAPER:136-159; README:70-84 |
| P-04 | Three-level table: local replay, contract authorization, global semantic authorization | PAPER:199-207 | ABSENT | - | PAPER:205-213 |
| P-05 | Turing-is-not-wrong table: tape, read, transition, halt, decoder, policy and the structure each still needs | PAPER:359-393; CTS:65-78 | ABSENT | - | PAPER:365-399; CTS:71-84 |
| P-06 | Typed tape roles: TapeCell, ReadControl, ReadReport, SemanticAdapter, TerminalPolicy; unread versus blank versus Option absence | PAPER:395-431; CTS:33-44 | PARTIAL | The absent/empty/token distinction exists (PGW-PREGENESIS-GRAMMAR: absent input, empty word, <>, ground carrier; PGW-ABSENCE-OF-RULE-NOT-IDENTIFICATION). The typed read/adapter/policy layers are absent. | PAPER:401-437; CTS:39-50 |
| P-07 | P versus NP fence: fixed-witness verification is a bounded contract case | PAPER:475-483; CTS:283-306 | ABSENT | Nearest: the Troyer-Wiese scope fence in tfq_1192 (FSP), a different problem. | PAPER:481-489; CTS:289-312 |
| P-08 | Bounded executable adequacy packet narrative | PAPER:492-517 | ABSENT | - | PAPER:498-523 |
| P-09 | LLM consequence: report-only case, arbitrary-program case, randomness, external tools | PAPER:519-554 | ABSENT | - | PAPER:525-560 |
| P-10 | Chinese Room as a bounded illustration | PAPER:556-578 | ABSENT | - | PAPER:562-584 |
| P-11 | Falsifiability conditions | PAPER:665-686 | ABSENT | - | PAPER:671-692 |
| P-12 | References: Turing 1936, Rice 1953, Goedel 1931, Loeb 1955, Necula 1997, Searle 1980 | PAPER:713-736 | ABSENT | No citation of these works in dag/ or papers/. | PAPER:719-742 |
| P-13 | README: contents map, v0.9 status line, fast-replay axiom ceilings | README:1-62; README:93-134 | ABSENT | README restates paper and ledger; its v0.9 status line is stale against v0.14. | README:7-68; README:99-140 |

### C. Controlled Turing derivation series (SEAL-TC) (13 items: PRESENT 0, PARTIAL 4, ABSENT 9)

| ID | Item | Source (file:line) | Repo status | Where in repo / what is missing | Recovered to (key:line) |
| --- | --- | --- | --- | --- | --- |
| SEAL-TC-00 | Inscription and Primitive Difference: alphabet of at least two marks, blank as declared symbol | CTS:96-116 | PARTIAL | PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT, PGW-PREGENESIS-GRAMMAR, PGW-MSSN-ALPHABET-DECLARATIONS, PG-FREE-MONOID-NONISO. | CTS:102-122 |
| SEAL-TC-01 | Read is syntactic selection; two adapters over one read trace | CTS:118-141 | PARTIAL | Observation families and profiles (TFQ-0433, PGW-OBSERVATIONAL-EQUIVALENCE); the read/adapter layering is absent. | CTS:124-147 |
| SEAL-TC-02 | Transition and motion: preserved invariant and named countertrace | CTS:142-181 | ABSENT | Conceptual analogues only (see AIT-TC2). | CTS:148-187 |
| SEAL-TC-02b | Direct finite-rule operational semantics | CTS:183-202 | ABSENT | - | CTS:189-208 |
| SEAL-TC-02c | Finite token grammar and parser | CTS:204-231 | ABSENT | - | CTS:210-237 |
| SEAL-TC-03 | Halt is terminality, not authorization | CTS:233-250 | PARTIAL | PGW-NO-TRANSITION-QUIESCENCE (empty transition relation), DS-QM090-092-AUTHORITY-FIREWALL (derived structure does not imply authority). The halt-versus-policy split is absent. | CTS:239-256 |
| SEAL-TC-04 | Trace, receipt and replay: replay establishes only the fixed checker result on frozen bytes | CTS:252-281 | PARTIAL | TFQ-0217 (a digest is byte agreement only), TFQ-0216, PGW-REPLAY-NECESSITY. | CTS:258-287 |
| SEAL-TC-05 | Certificate verification and the P/NP boundary | CTS:283-306 | ABSENT | - | CTS:289-312 |
| SEAL-TC-06 | Arbitrary-program semantic boundary (Rice reduction) | CTS:325-338 | ABSENT | - | CTS:331-344 |
| SEAL-TC-07 | Self-description and formal soundness | CTS:340-352 | ABSENT | - | CTS:346-358 |
| SEAL-TC-08 | LLM corollary | CTS:354-367 | ABSENT | - | CTS:360-373 |
| CTS-matrix | Controlled experiment matrix (hold fixed / vary / allowed conclusion) | CTS:407-419 | ABSENT | - | CTS:413-425 |
| CTS-exit | Exit condition for the branch | CTS:421-427 | ABSENT | - | CTS:427-433 |

### D. SEAL-AIT derivation series (10 items: PRESENT 0, PARTIAL 6, ABSENT 4)

| ID | Item | Source (file:line) | Repo status | Where in repo / what is missing | Recovered to (key:line) |
| --- | --- | --- | --- | --- | --- |
| SEAL-AIT-00 | Primitive Difference: a raw distinction chooses no look, report, predicate or policy | SAS:43-57 | PARTIAL | TFQ-0326, TFQ-0327 and the S000 primitive-difference trunk; two-extension proof absent. | SAS:49-63 |
| SEAL-AIT-01 | Presentation and quotient: report fibers, no unique section | SAS:59-76 | PARTIAL | TFQ-0327, PG-HISTORY-REPORT-CRITERION. | SAS:65-82 |
| SEAL-AIT-02 | Proposal and semantic predicate: bytes, parser, interpretation, validity are distinct | SAS:78-90 | PARTIAL | TFQ-0327, TFQ-0328. | SAS:84-96 |
| SEAL-AIT-03 | Evaluation and report adequacy | SAS:92-105 | PARTIAL | TFQ-0328; PG-HISTORY-REPORT-CRITERION. | SAS:98-111 |
| SEAL-AIT-04 | Replay and evidence custody | SAS:107-126 | PARTIAL | TFQ-0331, TFQ-0216, TFQ-0217, TFQ-0505. | SAS:113-132 |
| SEAL-AIT-05 | Authorization and terminal policy | SAS:128-148 | PARTIAL | TFQ-0330. | SAS:134-154 |
| SEAL-AIT-06 | Turing-computation boundary | SAS:150-174 | ABSENT | - | SAS:156-180 |
| SEAL-AIT-07 | Self-soundness boundary | SAS:176-190 | ABSENT | - | SAS:182-196 |
| SEAL-AIT-08 | LLM authorization corollary | SAS:192-206 | ABSENT | - | SAS:198-212 |
| SAS-rule | Seven-point design rule per derivation, and the convincing-series criteria | SAS:13-27; SAS:208-216 | ABSENT | - | SAS:19-33; SAS:214-222 |

### E. Computability-lift admission sheet (11 items: PRESENT 0, PARTIAL 5, ABSENT 6)

| ID | Item | Source (file:line) | Repo status | Where in repo / what is missing | Recovered to (key:line) |
| --- | --- | --- | --- | --- | --- |
| ADM-1 | Field 1: syntax, program encoding, input encoding, equality on programs | CLA:51-52 | PARTIAL | TFQ-0330: intended proposal-language coverage (by name). | CLA:57-58 |
| ADM-2 | Field 2: partial or step-indexed evaluator, malformed programs, bounds | CLA:53-55 | ABSENT | - | CLA:59-61 |
| ADM-3 | Field 3: universality witness, theorem or audited imported theorem | CLA:56-58 | ABSENT | - | CLA:62-64 |
| ADM-4 | Field 4: extensional property with named observational equivalence | CLA:59-61 | ABSENT | - | CLA:65-67 |
| ADM-5 | Field 5: one satisfying and one failing encoded program | CLA:62-63 | ABSENT | - | CLA:68-69 |
| ADM-6 | Field 6: effective reduction from a source undecidable problem | CLA:64-66 | PARTIAL | TFQ-0330: ordinary-computable decision-class binding (by name). | CLA:70-72 |
| ADM-7 | Field 7: split of semantic predicate, reports and terminal policy | CLA:67-69 | PARTIAL | TFQ-0328: a supplied validity bit is data for a later terminal. | CLA:73-75 |
| ADM-8 | Field 8: replay closure of bytes, evaluator, toolchain, command, theorem | CLA:70-72 | PARTIAL | TFQ-0330: independently replayed custody (by name). | CLA:76-78 |
| ADM-tests | Six admission-failure tests | CLA:74-87 | ABSENT | - | CLA:80-93 |
| ADM-cands | Candidate carriers and ceilings: DTM0/DTM1, PO-022, PO-023, AIT transition packet | CLA:22-44 | PARTIAL | PO-023: lean4/HaltingQuotient.lean and traceability_matrix.md PO-023-C1/C2 (pigeonhole only). PO-022, NSA-000 and FOC-028 are absent from the repository. | CLA:28-50 |
| ADM-seq | Recommended sequence and exit evidence | CLA:89-118 | ABSENT | - | CLA:95-124 |

### F. Support packets and Stage-0 dialogues (8 items: PRESENT 0, PARTIAL 0, ABSENT 8)

| ID | Item | Source (file:line) | Repo status | Where in repo / what is missing | Recovered to (key:line) |
| --- | --- | --- | --- | --- | --- |
| SUP-DTM0-P | Update packet: direct-machine seed (AIT-DTM0), v0.8 | S-TH-P:1-102 | ABSENT | - | S-TH-P:7-108 |
| SUP-DTM0-D | Dialogue R1-R5: Turing scope, halting, Lean correspondence, carrier admission, existing research | S-TH-D:1-114 | ABSENT | - | S-TH-D:7-120 |
| SUP-G5C-P | Update packet: G5c terminalization, v0.12 | S-G5C-P:1-105 | ABSENT | - | S-G5C-P:7-111 |
| SUP-G5C-D | Dialogue R1-R5 (R4 rejected): open-is-not-universal, Rice and LLM scope, externality | S-G5C-D:1-127 | ABSENT | - | S-G5C-D:7-133 |
| SUP-DTM1-P | Update packet: DTM1 token code, v0.13 | S-DTM1-P:1-111 | ABSENT | - | S-DTM1-P:7-117 |
| SUP-DTM1-D | Dialogue R1-R5: token code is not bytes, round-trip law, what is not encoded | S-DTM1-D:1-126 | ABSENT | - | S-DTM1-D:7-132 |
| SUP-DTM2-P | Update packet: DTM2 initial-input request (planned), v0.14 | S-DTM2-P:1-119 | ABSENT | - | S-DTM2-P:7-125 |
| SUP-DTM2-D | Dialogue R1-R5 (R3 rebutted and rejected): input words, framing, result-level agreement | S-DTM2-D:1-138 | ABSENT | - | S-DTM2-D:7-144 |

### G. Change log (all history; no mathematical claims beyond the ledger) (14 items: PRESENT 0, PARTIAL 0, ABSENT 14)

| ID | Item | Source (file:line) | Repo status | Where in repo / what is missing | Recovered to (key:line) |
| --- | --- | --- | --- | --- | --- |
| LOG-v0.14 | Change-log entry v0.14 | LOG:5-16 | ABSENT | - | LOG:11-22 |
| LOG-v0.13 | Change-log entry v0.13 | LOG:18-29 | ABSENT | - | LOG:24-35 |
| LOG-v0.12 | Change-log entry v0.12 | LOG:31-37 | ABSENT | - | LOG:37-43 |
| LOG-v0.11 | Change-log entry v0.11 | LOG:39-45 | ABSENT | - | LOG:45-51 |
| LOG-v0.10 | Change-log entry v0.10 | LOG:47-59 | ABSENT | - | LOG:53-65 |
| LOG-v0.9 | Change-log entry v0.9 | LOG:61-74 | ABSENT | - | LOG:67-80 |
| LOG-v0.8 | Change-log entry v0.8 | LOG:76-89 | ABSENT | - | LOG:82-95 |
| LOG-v0.7 | Change-log entry v0.7 | LOG:91-110 | ABSENT | - | LOG:97-116 |
| LOG-v0.6 | Change-log entry v0.6 | LOG:112-127 | ABSENT | - | LOG:118-133 |
| LOG-v0.5 | Change-log entry v0.5 | LOG:129-147 | ABSENT | - | LOG:135-153 |
| LOG-v0.4 | Change-log entry v0.4 | LOG:149-161 | ABSENT | - | LOG:155-167 |
| LOG-v0.3 | Change-log entry v0.3 | LOG:163-179 | ABSENT | - | LOG:169-185 |
| LOG-v0.2 | Change-log entry v0.2 | LOG:181-200 | ABSENT | - | LOG:187-206 |
| LOG-v0.1 | Change-log entry v0.1 | LOG:202-206 | ABSENT | - | LOG:208-212 |

### Disposition for the DAG draft

Items on the Genesis-to-computability path are drafted in `authorization_recovery.json` (section 7). The rest are **inventory only**:

- **AUTHORIZATION-stage, not drafted:** AIT-0, AIT-PD0, AIT-PD1, AIT-2, AIT-E0, AIT-G3a, AIT-G3, AIT-G4, AIT-3, AIT-8, AIT-9, AIT-G0, AIT-G8, SEAL-AIT-00..05, SEAL-TC-03.
- **Not drafted (not on the computation path):** AIT-4, AIT-6, AIT-7, SEAL-TC-05 (P versus NP fence), SEAL-TC-07, SEAL-TC-08, the Chinese Room, references, change-log history, support dialogues other than as cited sources.

## 3. Repository anchors used for the comparison

| Anchor | Location | What it holds |
| --- | --- | --- |
| PG-HISTORY-REPORT-CRITERION | `dag/derivation_dag.json` | A question over histories factors through the report iff it is constant on report fibers; factorization unique on the image. This is the AIT-1 / PO-000 obstruction in its general form. |
| PGW-REPLAY-NECESSITY (TFQ-0426) | `dag/derivations/01_pregenesis/tfq_0426_replay_necessity.md` | No auditor that sees only a view pi can report the state sigma when pi(h1)=pi(h2) and sigma(h1) differs from sigma(h2): the auditor form of AIT-1. |
| PG-COLLAPSE-BARRIER | `dag/derivation_dag.json` | Equal profiles: no function of the quotient separates the data. |
| PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT (TFQ-0422) | `dag/derivations/01_pregenesis/` | A presentation distinction does not give an internal class; the form of SEAL-TC-00. |
| PGW-PREGENESIS-GRAMMAR (TFQ-0417), PGW-ABSENCE-OF-RULE-NOT-IDENTIFICATION (TFQ-0424), PGW-NO-TRANSITION-QUIESCENCE | `dag/derivations/01_pregenesis/` | Absent input, empty word, token and ground carrier are four states; absence of a rule is not identification (UNDECIDABLE verdict); an empty transition relation has no successors. |
| TFQ-0327..0332 | `dag/derivations/04_authorization/` | Shelf-level chapters 01-06 of the later atlas book (proposal/report, evaluation, no forced external host, terminals, replay, Paper 0 boundary). |
| TFQ-0505..0510 (pfp-*) | `dag/derivations/04_authorization/` | Alpha license binding M1-M8, PFP tripartite law, carrier origin and nilpotency, Phi1/Gamma2, C4 certificate. TFQ-0506 and TFQ-0505 are the repository's versions of "replay and admission never authorize" and "reuse with any bound field changed is refused". |
| TFQ-0216, TFQ-0217 | `dag/derivations/23_engine_custody/` | Replay custody; a digest is byte agreement only. TFQ-0216 already mentions ReplayFiber of the authorization book. |
| DS-QM090-092-AUTHORITY-FIREWALL | `dag/derivation_dag.json` | StructureDerived does not imply IsAuth. |
| `OmegaCore.PrimitiveDifference` | `lean4/PrimitiveDifference.lean:7-60` | PrimitiveDifference, ZeroRel, ResidualQuotient, classOf, classOf_eq_iff_zeroRel; stand-in for the source's unavailable J011 (`pdProj` is `classOf`, `pdSetoid` is `zeroSetoid`). |
| `HaltingQuotient` | `lean4/HaltingQuotient.lean`; `traceability_matrix.md:193-194` | A pigeonhole fact on a three-element type (HaltsWith0, HaltsWith1, Diverges): any Bool projection collides. No machine, no step relation. |
| Genesis frontier | PGW-GENESIS-FREEZE-ENDPOINT-LEDGER (TFQ-0486), PGW-CONTEXT-DECISION-PROCEDURE (TFQ-0497), PGW-RUNS-PAST-DECLARED-BOUNDS (TFQ-0501), PG-GEN-REWRITING-COMMUTATION, PGW-CONTEXTS-PLUGGING-PROFILES (TFQ-0433), PG-FREE-MONOID-NONISO | See section 5. |

Searches that came back empty: no `Turing`, `Nat.Partrec`, `ComputablePred` or `Mathlib.Computability` in any `.lean` file of the repository; no Rice, halting-problem, semi-Thue or Post-correspondence statement in `dag/derivations/` or `dag/research/`; no citation of Turing 1936, Rice 1953, Goedel 1931, Loeb 1955, Necula 1997 or Searle 1980 in `dag/` or `papers/`; PO-022, NSA-000 and FOC-028 occur only in the recovered files.

## 4. Audit

### 4.1 Declaration names

I extracted every backticked identifier and every `goals.yaml` evidence item that looks like a Lean name (77) from the prose half and matched it against the declarations of the source `formal/*.lean` (245 declaration names and constructors). 48 matched. The 29 that did not are: file names and Lake targets (`AuthorizationIncompletenessTheory`, the `*.lean` and `*.md` names), the unbound fields `selfPass`, `allowedHard`, `allowedProposal`, the packet outcome string `open_due_to_inadequate_report`, the J011 symbol `ZeroRel`, the status words `OpenObstruction` and `LeanObligation`, PO-000's `AuthorizationBoundary.no_report_decision` (external), and the **seven DTM2 targets** (`decodeInputWord_encodeInputWord`, `decodeRunRequest_encodeRunRequest`, `executeRunRequestCode_encodeRunRequest`, `missing_request_header_is_rejected`, `machine_length_overrun_is_rejected`, `invalid_input_symbol_is_rejected`, `invalid_machine_segment_is_rejected`), whose module `direct_turing_machine_input_execution_models.lean` does not exist in the source. So every theorem name the ledger, paper, proof program and goals file cite is a real declaration, except the DTM2 ones, which are plans.

### 4.2 Build and axiom claims

I did not build anything and did not run the PowerShell packet. The source's statements that the Lake target builds (40 jobs), that the printed declarations have the stated axiom ceilings, and that the packet has 23 unit cases and 21 rejected mutations are therefore the source's. For context I read the axiom report that `auth-formal` produced for the original files under Lean v4.35.0 (`evidence/axiom_reports/originals_axioms_v4.35.0.txt` in that worktree): its 58 declarations reproduce the source's ceilings one by one (no axioms for the information core, tape-control, transition, replay, global-transport and PD models; `propext` only for the DTM0 generic and stuck/fuel declarations, the DTM1 rule-list/machine round trips and rejection fixtures, and four of the five G5c declarations). It contains no entry for the AIT-PD1 bridge, which imports `J011_minimal_publication`, a module that is not available.

### 4.3 Claims whose status is lowered

| Claim | Source status | Audited status | Reason |
| --- | --- | --- | --- |
| AIT-PD0 | proved (finite) | fixture; no content about Primitive Difference | `RawPrimitiveDifference` has fields `Carrier`, `mark`, `zero` and no laws, and `AuthorizationExtension` (`valid`, `terminal`) never mentions `mark` or `zero`. "Same primitive, different validity" is two Bool functions over a type that happens to carry a primitive. It shows that alternatives exist, not that a primitive fails to select one. `by decide`/`rfl` on a fixed instance. |
| AIT-PD1 | proved, rooted target | unreproduced here; conditional on a port | Depends on `J011_minimal_publication` (`ProjectionFiber.J011`), absent from this checkout and from the v4.35.0 report. The repository has the interface under other names (`OmegaCore.PrimitiveDifference`, `classOf`), so a port is routine; the content is AIT-1 instantiated on the quotient, so it adds no strength beyond AIT-1. |
| AIT-E0 | proved, rooted target | fixture; near-vacuous as a statement about placement | `Presentation` carries `sourceSite` and `evaluatorSite`, but `CanAuthorize` quantifies only over `report` and `valid`. The sites cannot affect the conclusion, so "physical separation is neither necessary nor sufficient" is true by construction and restates that adequacy decides `CanAuthorize`. The source's caveat that `Site` is only a label understates this: it is an unused parameter. |
| AIT-2 | proved | instance of AIT-1 on `Packet(Bool)` | The generic part is AIT-1; the rest is `decide` on one packet. |
| AIT-TC0 | proved, axiom-free | computationally checked on a fixed two-presentation carrier | Two declarations are `rfl` on definitions chosen to differ (two adapters, two policies); the two no-go statements are case analysis on a two-element domain, with a contract written to separate exactly those two presentations. |
| AIT-TC2 | proved, rooted target | computationally checked on an enumerated four-constructor type | The carrier is not a tape. The contracts were written to give a preserved case and a countertrace. `full_configuration_report_adequate_for_marked_cell_contract` holds for the identity report and any contract; `full_configuration_report_admits_marked_cell_decider` returns the contract function itself. |
| AIT-G4 | proved, bounded scope | positive half is a tautology | Same two declarations as AIT-TC2 plus a PowerShell evaluator that I did not run; the evaluator-to-Lean correspondence is, as the source says, an import. |
| AIT-DTM0 | proved; partial carrier only | definition plus closed fixtures | `step_halted_iff_declared_halt` unfolds `step`; the fixtures are `rfl` evaluations. The tape is `Int -> TapeSymbol`, so initial tapes of infinite support are included, unlike Mathlib's finite-support `Tape`. Determinism is first-match on a list, not a property of the machine. |
| AIT-DTM1 | proved; partial carrier only | stands (general round trip by induction) | No converse; token alphabet is the natural numbers, an infinite alphabet; four rejection fixtures are `rfl` on closed lists. |
| AIT-DTM2 | not in the ledger; packet only | OPEN (planned) | No Lean file; absent from ledger, proof program, goals, paper and change log although the packet is dated 2026-08-21 and targets v0.14. |
| AIT-G5a | proved, rooted target | stands, scoped | Contrapositive of function composition with arbitrary predicates as "allowed classes"; no computability content until instantiated, as the file header says. |
| AIT-G5c | proved, rooted target | stands, conditional | Three terminal values in Lean against five in TFQ-0330 (authorized, rejected, unresolved, refused, not admitted); the Boolean fixture holds because its predicate is decidable. |
| AIT-G3a | proved, rooted target | computationally checked on enumerated tags, plus one general lemma | `replayed_status_requires_bound_submission` is general; the four attacks are `rfl` on closed submissions; equality is structural, not a hash. |
| AIT-G3 | replayed; bounded scope | unverified here | PowerShell tests were not run; 23 and 21 are the source's counts. |
| AIT-5 / AIT-6 | cited; local formalization open | AIT-5: import with a Mathlib witness; AIT-6: no witness | Mathlib (v4.33.1 checkout) has `ComputablePred.rice`, `rice₂`, `halting_problem`; for Goedel it has only the beta function (`Mathlib/Logic/Godel/GodelBetaFunction.lean`), no incompleteness theorem. |
| AIT-7 | pending AIT-5 model binding | open, unchanged | No LLM execution model exists; TFQ-0330 forbids citing it as closed. |

### 4.4 Internal inconsistencies of the source (recorded, not repaired)

- README.md still reports "v0.9" and "three standalone seed modules"; paper and ledger are v0.14 and the formal folder has eleven files.
- The DTM2 update packet (dated 2026-08-21, target v0.14) is the only trace of AIT-DTM2: no ledger row, no goal, no change-log entry, no Lean file.
- Counts disagree: the proof program says AIT-TC2 has "six listed declarations" and lists five; the ledger lists five; the v4.35.0 report prints nine for that file.
- The paper numbers its sections 1-6, then an unnumbered "Falsifiability and proof program", then 8; there is no section 7.
- Two numbering schemes (AIT-n and AIT-Gn) collide on 3 and 4, see section 0.
- The ledger calls AIT-P0 "established in PO-000", which is external; the claim is not checkable from the package.

### 4.5 The source's machine against Mathlib

Names checked in the only Mathlib available to me, the **v4.33.1** checkout in the shared main checkout's `lean4/.lake/packages/mathlib` (this worktree has no `.lake`, so **v4.35.0 was not checked**; the repository pins v4.35.0 in `lean4/lake-manifest.json`).

| Mathlib declaration | File:line (v4.33.1) | Relevance |
| --- | --- | --- |
| `ComputablePred.rice`, `ComputablePred.rice₂` | Computability/Halting.lean:33, 43 | Rice for `Nat.Partrec.Code`: an extensional set of codes is computable iff empty or everything. This is the AIT-5 / SEAL-TC-06 theorem. |
| `ComputablePred.halting_problem`, `halting_problem_re`, `halting_problem_not_re` | Computability/Halting.lean:61, 65, 68 | Source predicate for the G5a transport; r.e. but not computable. |
| `computable_of_manyOneReducible` | Computability/Reduce.lean:125 | The closure-under-reduction hypothesis of G5a, for `ComputablePred`. |
| `Nat.Partrec.Code.eval`, `exists_code` | Computability/PartrecCode.lean:464, 536 | The program carrier and universality (every partial recursive function has a code). |
| `Turing.TM0.Machine`, `Stmt`, `Cfg`, `step`, `eval`, `Supports` | Computability/TuringMachine/PostTuringMachine.lean:135, 118, 144, 159, 173, 183 | Closest to DTM0. |
| `Turing.TM1`, `TM1to0.tr_eval`, `TM1to1.tr`, `TM0to1.tr_respects` | same file:286, 542, 753, 999 | TM1to1 re-presents any machine over a `Bool` alphabet: the binary-alphabet reduction. |
| `Turing.TM2`, `TM2to1.tr_eval` | Computability/TuringMachine/StackTuringMachine.lean:107, 735 | Stack machines to TM1. |
| `Turing.PartrecToTM2.tr_eval` | Computability/TuringMachine/ToPartrec.lean:945 | Partial-recursive codes to TM2: universality for Turing machines from codes. |

DTM0 is not Mathlib's TM0, and the differences decide what a bridge has to prove:

| | DTM0 (source) | Mathlib `Turing.TM0` |
| --- | --- | --- |
| Tape | `Int -> TapeSymbol`, any support | `Tape Γ`, blank outside a finite set (ListBlank) |
| Action per step | next state, write and move together; moves left, right, stay | `Stmt` is move or write, one per step |
| Halting | designated halt state `haltState`; "no rule" is a separate `stuck` result | halt is `none`: no applicable transition |
| States | `Nat`, no finiteness | arbitrary `Λ`; finiteness only via `Supports` |
| Determinism | first match in a rule list | a function `Λ -> Γ -> Option (Λ × Stmt)` |
| Evaluator | fuel-bounded, total, returns `StepResult` | `Part`-valued `eval`, partial |
| Alphabet | two symbols `blank`, `marked` | any `Γ` with a default; `TM1to1` reaches `Bool` |

## 5. How this work maps onto today's Genesis frontier

The frontier nodes are an endpoint ledger (TFQ-0486), a missing decision procedure (TFQ-0497), runs stopped at declared bounds (TFQ-0501), the rewriting-commutation theorem, contexts (TFQ-0433) and the free monoid. The earlier work offers typing discipline and a transport lemma for these, and one concrete place where the Genesis machinery meets a machine model. It proves nothing about Genesis itself.

| Frontier node | What is open there | What the recovered work contributes | Attach point (draft record) |
| --- | --- | --- | --- |
| TFQ-0486 freeze-endpoint ledger (PGW-GENESIS-FREEZE-ENDPOINT-LEDGER) | Three axes (research_phase CLOSED_WITH_OPEN_OBSTRUCTIONS, alpha_reference READY_WITHIN_DECLARED_SCOPE, original_seed_completion_gate UNSATISFIED); residuals D2-D5, D10, H-1..H-9, X-1; none closed or reclassified without a cited later source. | AIT-9 and the sealed-record discipline: mechanical gates do not establish semantic correspondence, which is the reason for independent axes. AIT-G5c is the formal reading of an endpoint ledger as a terminalizer with the values authorized, rejected, unresolved: when the acceptance bit lies in a class with no total decider, a closed two-sided sound terminalizer is excluded, so "unresolved" is forced rather than chosen. AIT-TC1 is the freeze protocol (frozen inputs, sealing, post-seal audit). | `auth-g5c-terminalization-consequence` (parent includes TFQ-0486), `auth-blind-derivation-protocol` (parent TFQ-0486) |
| TFQ-0497 context decision procedure (PGW-CONTEXT-DECISION-PROCEDURE) | No decision procedure for collapse and separability over the well-formed contexts of a finite regime (X-1); a Lean decider would settle Y-2, T-1, holding two and exhaustion. | Decision classes are explicit parameters (`allowedHard`), never "all Bool functions". For a fixed finite regime the decider exists and the G5c fixture `finite_closed_terminalizer_remains_possible` is the pattern: a decidable contract has a closed two-sided sound terminalizer. Across regimes of growing size the question is an extensional property of the derivability relation, which is Rice-shaped once the rule class can encode computation (conjectural here, see section 6). The admission gate (AIT-G5b) lists what would have to be frozen before such a claim. | `auth-g5a-class-relative-transport` (see_also), `auth-g5b-carrier-admission-gate` (see_also) |
| TFQ-0501 runs past declared bounds (PGW-RUNS-PAST-DECLARED-BOUNDS) | 11,266 nodes stopped at the guard, 368 at the bound, 116 runs not closed; H-2..H-9; whether the augmentation sequence is unbounded (question 7). | The typing of bounded outcomes: DTM0 `StepResult` separates halted, stuck and fuelExhausted, and the source insists that fuel exhaustion is not non-halting (`AIT-DTM0`, dialogue R2). A guard or bound stop in Genesis should carry the same type: unresolved, neither closed nor diverging. TFQ-0505 M6 ("bound or guard outcomes are typed stops, never admitted successes") is the repository's existing statement of the same discipline. Question 7 has the form of a halting question once the engine class can simulate a machine. | `auth-fuel-exhaustion-typed-stop` (parent TFQ-0501) |
| PG-GEN-REWRITING-COMMUTATION | Genesis `Step`/`Reach` and injective renaming of terms commute; obstructions persist along `ReachNoRemove`. | DTM0 `step` and `execute` are the `Step`/`Reach` analogue for a machine. The matching theorem would be that relabelling the state numbers by an injective map commutes with `execute`; the source does not state it, and it is the natural first bridge between the Genesis rewriting layer and a machine model. TC2's preserved-contract / countertrace pair parallels obstruction persistence. | `auth-dtm0-finite-rule-machine` (parent), `auth-tc2-finite-transition-contract` (see_also) |
| TFQ-0433 contexts, plugging, profiles (PGW-CONTEXTS-PLUGGING-PROFILES) | Collapse and separability defined through contexts; decision procedure open. | A rule lookup keyed by (state, scanned symbol) is a context of width one around the head, and the read report is an observation by such a context. SEAL-TC-01 says the read token does not select its interpretation: one profile, two supplied adapters, exactly collapse without separation. The source never states this connection. | `auth-tc0-tape-control-typing` (parent) |
| Free monoid (PG-FREE-MONOID-NONISO, PGW-PREGENESIS-GRAMMAR, PGW-MSSN-ALPHABET-DECLARATIONS) | Re-presenting over alphabets of different sizes is not an isomorphism of structure. | DTM1 encodes a machine as a word of the free monoid on the natural numbers (infinite alphabet) while DTM0 tapes use two symbols. A binary tape encoding of a DTM1 code is therefore an embedding through a prefix code, not an isomorphism, which is the situation PG-FREE-MONOID-NONISO describes. The source never makes this step. | `auth-dtm1-token-code-roundtrip` (parent PG-FREE-MONOID-NONISO) |

Where the two recovered strands attach:

```text
Genesis side                                   controlled-Turing series            computability lift
--------------------------------------------   --------------------------------    ----------------------------------------
TFQ-0433 contexts / profiles  ------------->   SEAL-TC-00/01 inscription, read
PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT  ----->   (alias of SEAL-TC-00)
PG-GEN-REWRITING-COMMUTATION (Step/Reach) ->   SEAL-TC-02 transition (AIT-TC2)
                                               SEAL-TC-02b DTM0 step / execute
TFQ-0501 runs past declared bounds  <-------   fuel-exhausted typed stop
PG-FREE-MONOID-NONISO, PGW-PREGENESIS-GRAMMAR  SEAL-TC-02c DTM1 token code    ->  AIT-G5b admission gate (8 fields)
                                                                                       |  DTM2 request, trace agreement,
TFQ-0497 decision procedure  <---------------------------------------------------  AIT-G5a transport    universality (Mathlib), reduction
TFQ-0486 endpoint ledger  <-------------------  SEAL-TC-08 / AIT-TC1 protocol  <-  AIT-G5c terminalization   |
                                                                                   AIT-5 Rice (Mathlib rice₂) -> AIT-G5 lift
```

## 6. Relation to the C1-C8 chain (branch `comp-utm`)

Judged from the step names only (alphabet from separation; words and contexts as semi-Thue; bounded-regime decidability no-go; unbounded supply as an import; TM-as-rewriting; universality via Mathlib; undecidability of Reach; binary minimality). I did not read the `comp-utm` branch, so where a step could be read two ways I say so.

**Blindness caution.** The source's own protocol (AIT-TC1, `controlled_turing_derivation_series.md:369-405`) says a literature-blind run must receive no prior derivation text until it is sealed, and that the comparison with earlier work is a post-seal source classification (step 6). If `comp-utm` is meant to be blind, it should not read this file or the recovered prose until it is sealed; this section is then that classification.

| Step | Relation | Specifics |
| --- | --- | --- |
| C1 alphabet from separation | anticipates the aim; differs in method | SEAL-TC-00 (CTS:96-116) takes "a finite alphabet with at least two declared marks" from Primitive Difference's two unequal marks (PAPER:101-110); DTM0 fixes `TapeSymbol` to the two constructors `blank` and `marked` (`direct_turing_machine_models.lean:24-27`) and DTM1 tags them 0 and 1. The two marks and the count are declared, not derived from a separation requirement; AIT-PD0 only records that a raw distinction selects no predicate. What it adds is the typing fence: a declared blank, an unread observation and a meta-level absent cell are three carriers (PAPER:395-431), which the Genesis side keeps as the four states of PGW-PREGENESIS-GRAMMAR. |
| C2 words and contexts as semi-Thue | differs; no overlap | No string rewriting appears anywhere. DTM0's `Rule.matches` keys on (state, scanned symbol), a context of width one around the head, and `applyRule` rewrites the state, one cell and the head. The tape is a total function, not a word, so a semi-Thue reading covers only finite-support tapes. DTM1 does put machines into the free monoid on `Nat`. The source never connects rule matching to Genesis contexts and plugging (TFQ-0433). |
| C3 bounded-regime decidability no-go | depends on the statement: agrees on one reading, contradicts on another | If the no-go says a bounded evaluation cannot settle the unbounded question: agrees. DTM0 types `fuelExhausted` apart from `halted` and `stuck` and never reads it as divergence (PAPER:453-462); the admission test fails any proposal that treats "a finite-horizon simulation as a universal simulation" (CLA:81-82). If the no-go says decidability fails already inside a bounded regime: the source says the opposite. `execute` is total by recursion on fuel, "halts within n steps" is decidable, and `finite_closed_terminalizer_remains_possible` (LEDGER:34) is a closed two-sided sound terminalizer for a decidable contract. The source's own no-go (G5a, G5c) is class-relative and conditional on a supplied `NoTotalDecider` premise. |
| C4 unbounded supply as an import | anticipates | Nothing is derived about unboundedness. `Tape := Int -> TapeSymbol`, `Nat` states and `List Nat` codes are Lean primitives; universality enters only as "a theorem or audited imported theorem" (CLA:56-58); the decision classes of G5a are explicit parameters (PAPER:311-321); TFQ-0501 question 7 is likewise unresolved. It differs in that the import is never priced: the source does not list what unbounded supply buys, and infinite-support tapes go beyond what a finite supply gives. |
| C5 TM-as-rewriting | partly anticipates; differs | DTM0 is a rewriting of configurations (state, head, tape) by an ordered rule list, with `step` a function using first-match lookup. There is no encoding of configurations as words, no semi-Thue presentation and no relation to the Genesis `Step`/`Reach`. The natural bridge (injective state relabelling commutes with `execute`, parallel to PG-GEN-REWRITING-COMMUTATION) is not in the source. |
| C6 universality via Mathlib | anticipates the route; differs in the object | The source defers universality to "a fully audited reduction to a mechanized computability library" (PP:477-479) and "an audited imported theorem" (CLA:56) and names no library. Mathlib has `Turing.TM0/TM1/TM2`, `PartrecToTM2.tr_eval` and `Nat.Partrec.Code.eval`/`exists_code` (section 4.5). DTM0 differs from `TM0` in tape support, one-action-per-step, halted versus stuck, states and determinism, so a bridge must restrict to finite-support tapes, split write-and-move rules and merge halted with stuck. No contradiction; one convention to watch: DTM0 separates halted from stuck, Mathlib does not. |
| C7 undecidability of Reach | anticipates the shape; differs in target | AIT-G5a is the transport lemma (reduce a source predicate with no total decider into the target predicate, with the decision class closed under the reduction) that a Reach undecidability proof needs, with `halting_problem` as source and `computable_of_manyOneReducible` as closure. The source states its target as the validity of proposals, not Reach, and leaves the source undecidability as "an explicit input". It does allow for Reach being only semi-decidable: SEAL-TC-06's nonclaim keeps "semi-decision procedures" (CTS:337-338), which matches `halting_problem_re`. |
| C8 binary minimality | anticipates the binary choice; no minimality | DTM0 has exactly two symbols and DTM1 tags only 0 and 1. SEAL-TC-00 says "at least two", a lower bound that follows from Primitive Difference (one mark carries no difference) but is never formalized beyond `boolPrimitive_has_two_marks` by `decide`. There is no argument that two symbols suffice or that fewer cannot; Mathlib's `TM1to1` gives the sufficiency direction, with a state blow-up. DTM0 also allows write and move in one rule and a `stay` move, which a minimal presentation would not. |

**Contradictions found: none outright.** Two conflict risks: the reading of C3 above, and the halted/stuck convention in C6. Terminal vocabulary also differs without conflict: three values in the G5c Lean module against five in TFQ-0330; a Reach result (semi-decidable) needs the `unresolved` value.

## 7. DAG draft

`C:\Users\a343o\.claude\jobs\cc182852\tmp\drafts\authorization_recovery.json`, built to `domain_draft_spec.md`. No DAG file was edited.

- Records: 16 (ALIAS 4, NEW 12). Stage `COMPUTATION` for every NEW record, slug prefix `auth-`.
- Status histogram (NEW): COMPUTATIONALLY_CHECKED 2, DEFINITION 4, IMPORTED_ASSUMPTION 1, OPEN 2, PROVED_LEAN 3.
- ALIAS: AIT-1 and AIT-P0 to PG-HISTORY-REPORT-CRITERION; SEAL-TC-00 to PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT; SEAL-TC-04 to TFQ-0217.
- `COMPUTATION` is not yet in the stage vocabulary of `dag/validate_derivation_dag.py` (lines 40-60); `merge_domain_drafts.py` reports it as an added stage, and the validator list needs the same addition when the draft is merged.
- `lean` references point at `papers/foundations/authorization_incompleteness/evidence/original/formal/*.lean`, the layout currently produced by `auth-formal`; I checked each symbol against that worktree. They resolve only after that branch is merged. `authorization_recovery.standalone.json` is the same draft with those references moved to `external_witnesses` and the Lean-dependent statuses lowered to OPEN, for use if the draft is validated without `auth-formal`.
- Statuses lowered relative to the source are listed in section 4.3: AIT-TC0 and AIT-TC2 (proved to computationally checked), AIT-DTM0 (proved to definition), AIT-DTM2 (planned to open), AIT-5 (cited to imported assumption with a Mathlib witness).

## 8. Not done, and limits

- No Lean or PowerShell was executed; build, axiom and mutation-count claims are the source's, supplemented by the `auth-formal` v4.35.0 axiom report for the original files.
- Mathlib names were checked in a v4.33.1 checkout, not v4.35.0.
- The code half (`code/`, `*.ps1`, `packet_manifest.json`) and `evidence/source_map.md` were read only for context; their claims are not audited here.
- The C1-C8 comparison uses step names only; `comp-utm` was not read.
- The repository comparison searched `dag/`, `papers/`, `docs/`, `lean4/` and `traceability_matrix.md`; `code/` was searched for Turing/halting vocabulary only.
- Classification of PARTIAL items is a judgement about content overlap; the cited repository nodes are listed so it can be checked.
