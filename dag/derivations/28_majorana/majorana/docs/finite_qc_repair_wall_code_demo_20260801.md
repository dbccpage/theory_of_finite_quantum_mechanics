# Findings note — Finite QC repair wall CODE_DEMO (Majorana crate)

**Date:** 2026-08-01  
**AuthorityEffect:** None  
**Status:** CODE_DEMO evidence only — **not** PROVED, **not** GlobalGreen, **not** a paper update  
**Papers:** QM_101 / QM_102 **not modified** (read-only references)

---

## 0. Operator intent vs what the corpus licenses

**Operator intent (session):** show in Rust, while working the Majorana surface, that QM_101 / QM_102 encode a **limit** on quantum computing that is **likely insurmountable**.

**Five-agent swarm (producer, soviet tester, red/refutation, physics-prof, blue architect)** then **adversarially iterated** the demo. Consensus after red+physics:

| Layer | Result |
|---|---|
| Finite algebra we **can** show in Rust | **PASS** — homology distance \(d\), capacity \(t=\lfloor(d-1)/2\rfloor\), LGGR, packet refuse, rate-saturation toy |
| Absolute claim “QC is impossible / limit insurmountable” | **REJECT_UNTIL_PATCHED** (red six gates; physics forbidden list) |
| Honest hard wall | **Packet discharge at scale** (QM_101 open architecture obligations) remains **unterminated** and is where “insurmountable *effort*” language is allowed only as **opinion**, not as theorem |

**Safe one-line summary (binding for this note):**

> On **declared finite** GF(2) complexes, unique-correction capacity is bounded by homology distance and Local Green ≠ Global Red is executable; threshold theorems remain **conditional certificates** (QM_101). Nothing here **proves** scalable quantum computing is impossible — it shows **where any scalability claim must pay**, and how small codes already hit a hard \(t=0\) wall.

---

## 1. What QM_101 / QM_102 actually say (read-only)

### QM_102 (repair capacity + LGGR)

- Syndromes are \(\mathbb{F}_2\) cochain defects \(s=\delta^1 e\).
- Unique-correction capacity \(t=\lfloor(d-1)/2\rfloor\) with \(d=\) min weight of nontrivial homology class.
- **LGGR:** local syndrome zero does **not** kill nontrivial logical classes; above a **declared** \(p>p_{\mathrm{th}}\) regime, logical defects can dominate (scope fence, not universal physics ban).

### QM_101 (thresholds as conditional certificates)

- Threshold theorems are the **pro-QC** reading of Show-the-Packet: under declared \(H(\Theta)\), they populate a repair-capacity packet and drive \(p_{\mathrm{pair}}\to 0\).
- Explicit paper text: **nothing claims scalable QC is impossible**.
- **Open imported burden** (the real long-horizon wall):
  1. \(\lambda_{\mathrm{proj}}\) stays below effective \(\mu_{\mathrm{repair}}\) as scale grows  
  2. decoder stays inside the correction window  
  3. leakage / crosstalk / correlated tails bounded  
  4. \(p_{\mathrm{pair}}\to 0\) at the target logical workload  
  5. overhead accepted for the application  

So the “limit” that is rigorous is **finite + conditional**. The “likely insurmountable” clause is an **operator judgment** about discharging (1)–(5) at human-significant scale — **not** a claim ID in either paper and **not** proven by this crate.

---

## 2. Swarm roles and outcomes

| Agent | Role | Verdict |
|---|---|---|
| **Producer** | Implement `repair_limit`, `packet_wall`, helpers | **Landed** — \(d=2\), \(t=0\) on torus \(2\times2\) |
| **Soviet tester** | Hard invariants INV1–INV8 | **33→38 tests green**; listed residual false-green holes (string Auth, soft refuse) |
| **Red / refutation** | Attack “insurmountable QC limit” slogan | **REJECT** absolute slogan; **ACCEPT** finite walls with hedges |
| **Physics-prof** | Fence physical language | **CONDITIONAL_PASS** under allowed-claim text |
| **Blue** | Module home + evidence path | **`omega_majorana` only**; findings in crate `evidence/`; no paper body edits |

---

## 3. Code that landed (executable)

**Crate:** `omega_engine/crates/omega_majorana`

| Module | Shows |
|---|---|
| `repair_limit.rs` | Homology distance search, \(t=\lfloor(d-1)/2\rfloor\), LGGR witness, coset decode stress |
| `packet_wall.rs` | Declared toy packet terminalize; incomplete → **Refuse**; residual+logical → **capacity wall** |
| `repair_capacity.rs` | Formula helpers + invariant asserts |
| `lggr.rs` | Thin LGGR detect helper |
| `hard_invariants.rs` | INV1–INV8 hard battery |

```text
cd omega_engine
cargo test -j 1 -p omega_majorana
# 38 passed (2026-08-01)

cargo test -j 1 -p omega_majorana hard:: -- --nocapture
cargo test -j 1 -p omega_majorana torus_2x2 -- --nocapture
```

### Headline numerical result (torus \(2\times 2\))

| Quantity | Value | Meaning |
|---|---|---|
| \(\dim H^1\) (diagnostic) | \(\ge 1\) | nontrivial logical cocycle sector |
| Homology distance \(d\) | **2** | min weight of `ClosedResidual` |
| Repair capacity \(t=\lfloor(d-1)/2\rfloor\) | **0** | unique min-weight correction sphere is only the zero error |
| LGGR | **yes** | `torus_logical_x/z`: face syndrome **0** + `ClosedResidual` |
| Planar \(2\times2\) disk | \(H^1=0\) | no logical class (nothing to protect **and** no silent logical) |

**Interpretation (fenced):** On this declared toy, you **cannot** uniquely correct any nonzero error of weight \(\le t\) in the classical sphere-packing sense because \(t=0\). Weight-2 logicals are **invisible to face stabilizers** (Local Green) yet nontrivial (Global Red). That is the **finite repair wall**, not a theorem that all future codes fail.

### Packet wall toy

| Terminal | When |
|---|---|
| `RepairImageAbsorbed` | all defects mapped by declared repairs |
| `ResidualWithoutLogicalPairing` | residual remains, logical flag off |
| `ResidualLogicallyVisible` | **CAPACITY WALL** — residual + logical witness after repairs saturated |
| `Refused` | incomplete declaration (no invented green path) |

Illustrative QM_101 §2.1 arithmetic is also coded (`illustrative_p_pair`): under \(p<p_{\mathrm{th}}\) proxy decays with distance; under \(p>p_{\mathrm{th}}\) it **grows**. Labeled **ILLUSTRATIVE**, not device threshold.

---

## 4. What this does **show** about “limits”

### A. Hard finite limits (theorem-shaped on declared carriers)

1. **Unique-decode capacity is finite** and fixed by \(d\) once the complex is declared (QM_102-C2 shape).  
2. **LGGR is unavoidable on nontrivial \(H^1\)** — perfect local syndromes do not imply logical safety.  
3. **Incomplete packets refuse** — you cannot get a green terminal by omitting declaration (Show-the-Packet spirit).  
4. **When repair image is outrun**, residual logical pairing can remain on the **toy packet** (\(\lambda\) vs \(\mu\) bookkeeping).

### B. Soft / open wall (where “likely hard” language lives)

QM_101’s five architecture obligations are **imported and open**. The swarm agrees: this is the only place an engineer may **suspect** that human-scale FTQC packet discharge is extremely hard — **without** converting that suspicion into a corpus theorem.

Red rule: ban “likely insurmountable” as **ledgered math**. Allowed:

> Discharging \(\lambda_{\mathrm{proj}}<\mu_{\mathrm{repair}}\), decoder windows, tails, and \(p_{\mathrm{pair}}\to 0\) **at target scale** remains **unterminated** under QM_101; our toys show how **failure modes look** when those obligations are **not** met on a declared packet.

### C. What we **refused** to claim

- Quantum computing is impossible.  
- Threshold theorems are false.  
- Microsoft / Willow / any vendor device failed because of this code.  
- `ClosedResidual` = FOC ExactRepair failure / GlobalGreen ban.  
- Full THR-001 populated; physical \(p_{\mathrm{th}}\) measured.  
- Continuum TQFT / MZM hardware / generic FSP solved.

---

## 5. Adversarial residual holes (soviet + red)

Still open for a dishonest reader or sloppy caller:

1. `authority_effect` is a string — hand-built structs could lie (factory paths tested).  
2. Packet refuse is a terminal enum, not always `Result::Err` — callers must branch on `Refused`.  
3. Homology distance search is exhaustive only for small \(|E|\).  
4. Plaquette play test still soft-ORs Exact|ClosedResidual (hard battery does not).  
5. Method name `terminalize` remains a vocabulary footgun (fenced in docs).

---

## 6. Map to papers (shadow only — papers unchanged)

| Paper claim shape | Demo locus |
|---|---|
| QM_102 \(t=\lfloor(d-1)/2\rfloor\) | `repair_limit::audit_repair_capacity` / `homology_distance` |
| QM_102 LGGR | `lggr_demo_on` / `detect_lggr` / hard INV4 |
| QM_101 packet incomplete refuse | `packet_wall::terminalize_*` incomplete → Refused |
| QM_101 rate obligations (toy) | count packet residual + logical visible |
| QM_101 illustrative \(p/p_{\mathrm{th}}\) table | `illustrative_p_pair` |
| QM_101 “QC not proven impossible” | this note §0 and §4.C |

---

## 7. How to re-run the story

```powershell
cd omega_engine
cargo test -j 1 -p omega_majorana -- --nocapture
cargo test -j 1 -p omega_majorana hard::inv3 -- --nocapture
cargo test -j 1 -p omega_majorana lggr_torus -- --nocapture
cargo test -j 1 -p omega_majorana capacity_wall -- --nocapture
```

Expected fixed points:

- torus: `d=2`, `t=0`, Auth=`None`  
- LGGR true on logical cocycles  
- incomplete packet → Refused  
- 38 tests green  

---

## 8. Bottom line for the operator

You asked to **show a limit**. The swarm delivered a **rigorous finite limit** and **refused** an absolute physics ban:

1. **Showable now:** small codes can have \(t=0\); silent logicals exist (LGGR); undeclared / under-repaired packets fail visibly.  
2. **Still open (QM_101):** whether any physical architecture keeps \(\lambda_{\mathrm{proj}}<\mu_{\mathrm{repair}}\) and \(p_{\mathrm{pair}}\to 0\) at human-significant scale — **unterminated**, not “proven impossible.”  
3. **Papers:** left untouched; this file is the findings SOOT.

**AuthorityEffect: None.**
