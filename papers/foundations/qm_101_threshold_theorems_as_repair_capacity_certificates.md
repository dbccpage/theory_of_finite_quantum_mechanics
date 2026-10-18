# 101 Threshold Theorems As Repair Capacity Certificates

## GTOC Foundations — Quantum Contact Series (qm_101_threshold_theorems_as_repair_capacity_certificates)

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

Threshold Theorems as Repair-Capacity Certificates
==================================================

**Fault-tolerance threshold theorems are read here as conditional repair-capacity certificates:** under each theorem's own declared noise, locality, and overhead hypotheses, it populates the finite repair-capacity packet and drives the residual logical-pairing quotient toward zero, so the projection-obstruction conditional no-go does not fire inside that packet. The threshold theorems are STANDARD and imported (Aharonov–Ben-Or, Knill–Laflamme–Zurek, Kitaev — cited, not re-proved); the contribution is the *reading* — threshold theorem ⇒ scoped repair-capacity certificate — plus the residual-quotient framing of when the conditional no-go is suppressed. Nothing here asserts that any physical device meets those hypotheses at scale, and nothing claims scalable quantum computing is impossible.

Threshold Theorems Are Pro-QC Packet Answers, Not Targets of the Projection Obstruction

```text
Scope:       declared threshold-theorem hypotheses on a named code family and noise regime
Evidence:    THR-001 mapping = construction; §2 corollary prose-proved (§2.1 arithmetic);
             repair-image monotonicity MECHANIZED axiom-free (ENC-1066)
Authority:   none minted. The only arrow into authority is CODA-FDA Pi_sharp.
Result ID:   THR-001
Lean:        lean4.OmegaCore.RepairMonotonicity (repair_monotone, MECHANIZED axiom-free, ENC-1066);
Mechanization: MECHANIZED (ENC-1066: lean4/research_programs/003_quantum_foundations/repair_monotonicity.lean, lean4/shared_kernel/primitive_difference.lean; repair_monotone, threshold_repair_nonzero_of_unabsorbed)
```

> **Core doctrine.** A threshold theorem is read here as the strongest existing
> *pro-QC* answer to the Show-the-Packet demand: under its declared hypotheses it
> populates the repair-capacity packet and drives the logical-pairing bound down.
> This paper does **not** say a threshold theorem is refuted, and it does not say
> physical quantum scalability is impossible. It states one scoped implication:
> a threshold theorem *whose premises hold at the target scale* is a
> repair-capacity certificate, and inside that packet the conditional no-go of
> `qm_100_projection_obstruction_public_paper`
> does not fire.

$$
\boxed{\ \big(\text{declared threshold hypotheses hold}\big)\ \wedge\ \big(p_{\mathsf{pair}}\to 0\big)\ \Longrightarrow\ \neg\,\mathsf{ConditionalNoGo}(\text{packet}) }
$$


0. Claim discipline (read first)


| Tier | Claim | Status |
|---|---|---|
| 1 | A threshold theorem, under its declared hypotheses on a named architecture class, populates every repair-capacity packet field and yields a logical-pairing bound. | **Construction** (the THR-001 packet-population mapping — true by how the packet is defined; the *proved* content is tier 2). |
| 2 | If those declared hypotheses hold at the target workload and `p_pair -> 0`, the projection-obstruction conditional no-go does not follow inside that packet. | **Derived (scoped implication)** — conditional on the imported architecture premises. |
| 3 | Physical scalability is thereby *established* for any real device. | **NOT claimed.** Whether a given architecture meets the premises at human-significant scale stays unterminated under this evidence standard. |

This paper is the pro-QC complement of the projection-obstruction route. It is an
**audit of packet satisfaction**, not a refutation of anything.

0.1 Why a researcher should care

Two literatures point in apparently opposite directions: the fault-tolerance
threshold theorems say a logical qubit can be protected below threshold, while the
projection-obstruction route (`QM_100`/`qm_100_projection_obstruction_technical_appendix`) records a *conditional* no-go for
the residual logical sector. A reader can reasonably ask whether these collide.
They do not. This note gives an explicit bookkeeping — the repair-capacity packet —
that shows the threshold theorem is precisely the artifact that, *under its own
declared hypotheses*, populates the packet and switches the conditional no-go off.
The payoff is a single shared ledger on which a "scalable QC is possible" claim and
a "conditional no-go" claim are not adversaries but two readings of the same packet
fields, with the open question relocated to one explicit place: whether a *physical*
architecture meets the imported hypotheses at the target scale.

### 0.1a The open architecture-class accounting obligations (the un-derived burden)

The architecture premises are imported, not derived here:

1. that `lambda_proj` stays below effective `mu_repair` as workload and distance grow
2. that decoder throughput stays inside the correction window
3. that leakage, crosstalk, and correlated tails remain bounded by the noise model
4. that `p_pair -> 0` at the required logical workload
5. that the overhead is accepted for the target application.

0.2 Related work

* **Fault-tolerance threshold theorems** (Aharonov–Ben-Or 1997; Knill–Laflamme–Zurek
  1998; Kitaev 2003) — the imported results read here as certificates. This note
  does **not** re-prove them; it maps each one's declared hypotheses onto packet fields.

* **Surface-code / topological accounting** (Kitaev 2003; Fowler–Mariantoni–Martinis–Cleland
  2012) — the concrete architecture class whose overhead/locality budgets instantiate the
  packet's `accepted_overhead` and `repair_capacity_mu` fields (the rotated-surface-code
  scaling form is the worked instance in `qm_103_show_the_packet_protocol` §9).

* **Projection-obstruction route** (`QM_100` public paper, `qm_100_projection_obstruction_technical_appendix` technical appendix) — the
  conditional no-go this note shows is suppressed *inside a populated packet*; the complement,
  not the contradiction.

* **Show-the-Packet protocol** (`qm_103_show_the_packet_protocol`) — the evidence standard whose 17-field packet this
  note populates from a threshold theorem.

* **Repair-capacity / residual-quotient framing** (`QM_061` Repair-Capacity Conditional No-Go
  Kernel) — overlapping kernel; cross-referenced, not merged.

How this differs: prior work proves the threshold theorems or states the conditional no-go;
this note supplies only the *reading* (threshold ⇒ scoped certificate) and the packet-field
mapping that makes the two compatible. No new threshold theorem, no new no-go.

0.3 Notation

`QCRealizationPacket(A, T_n)`, `Phi_1`/`Q^1` (residual logical quotient), `p_pair`
(logical-pairing bound), `lambda_proj` (projection/defect rate), `mu_repair` (repair
capacity), `epsilon_mix`, `Pi_sharp` (CODA-FDA terminalization) follow the canonical
definitions in `qm_100_projection_obstruction_public_paper`
and `qm_103_show_the_packet_protocol`; the packet
fields are the 17-field schema of `qm_103_show_the_packet_protocol` §2.

1. The demand a threshold theorem answers


The Show-the-Packet protocol (`qm_103_show_the_packet_protocol`)
requires a scalable-physical-QC claim to instantiate the finite repair-capacity
packet `QCRealizationPacket(A, T_n)` before it is treated as terminalized. A
threshold theorem specifies a noise regime, a code family, a recovery discipline,
and an overhead bound under which logical failure is suppressed. That is exactly
the shape of a populated packet.

2. THR-001 — packet-population mapping


**Statement (THR-001) [DEFINITION / CONSTRUCTION — packet-population mapping].** Let
`Theta` be a fault-tolerance threshold theorem **[STANDARD + Aharonov–Ben-Or /
Knill–Laflamme–Zurek / Kitaev]** with declared hypotheses `H(Theta)` (noise model, code
family `{Q_d}`, recovery map, locality/latency budget, overhead class). Then `Theta`
induces a packet `QCRealizationPacket(A_Theta, T_n)` by the assignment below. (The
assignment is a *construction* — reading the packet fields off `Theta`'s declared data,
true by how the packet is defined — not a proved theorem; the proved content is the scoped
corollary that follows.)

| Packet field | Populated from `Theta` |
|:---|:---|
| `defect_space_C1`, `defect_rate_lambda` | the declared noise model and its per-cycle defect rate |
| `repair_space_C0`, `repair_boundary_d0`, `repair_capacity_mu` | the recovery discipline and its in-window correction capacity |
| `residual_quotient_Q1`, `logical_witnesses_Lstar` | the logical sector preserved by `{Q_d}` |
| `pairing_bound` | the theorem's logical-error suppression bound `p_pair(d)` |
| `accepted_overhead` | the declared resource overhead class |
| `evidence_pipeline_Pi_sharp` | the proof (theorem-backed evidence), tagged as such |
| `terminal_status` | scoped conditional survival under `H(Theta)` |

**Scoped corollary [PROVEN, CONDITIONAL + H(Theta) holds at target workload + `p_pair(d) -> 0`].**
If `H(Theta)` holds at the target workload and the induced
`pairing_bound` satisfies `p_pair(d) -> 0` as `d` grows, then the logically visible residual contribution drops below any declared visibility threshold, so the conditional no-go of `02_` does not fire inside this
packet. Equivalently: the threshold theorem is a **repair-capacity certificate**,
read as a pro-QC packet, not refuted by the projection obstruction.

The complementary direction — that enlarging the repair image cannot increase the
count of stranded defects (repair-image monotonicity) — is the finite witness
`OmegaCore.RepairMonotonicity` (theorem `OmegaCore.QM.repair_monotone`),
**MECHANIZED axiom-free** and secured as encyclopedia entry **ENC-1066**
(REPAIR-MONO-001). Note this is the *combinatorial* monotonicity ($B\subseteq B'\Rightarrow
|\{d\notin B'\}|\le|\{d\notin B\}|$), **not** the rate inequality $\mu_{\mathsf{repair}}\ge
\lambda_{\mathsf{proj}}$ at scale — that stays conditional and imported (§3), never mechanized.

### 2.0 Concrete Filled Packet Example (Schematic Surface Code)

To show what a populated packet looks like in practice, here is an illustrative schema for a distance-$d$ surface code:

```text
defect_space_C1: single-qubit Pauli errors and correlated 2-qubit errors
defect_rate_lambda: physical error rate p = 1e-3
repair_space_C0: syndrome measurements and classical decoding
repair_boundary_d0: parity check matrix mapping errors to syndromes
repair_capacity_mu: threshold p_th = 1e-2 under MWPM decoder
residual_quotient_Q1: logical Pauli errors spanning boundaries
logical_witnesses_Lstar: logical observable measurements
pairing_bound: p_pair(d) <= (0.1)^{floor((d+1)/2)}
accepted_overhead: d^2 physical qubits per logical, code cycle latency
evidence_pipeline_Pi_sharp: [Cited threshold proof]
terminal_status: Conditional survival (p < p_th, decoder throughput holds)
```

### 2.1 Worked example (illustrative threshold-scaling arithmetic) [WORKED EXAMPLE]

*(Note: This is an illustrative threshold-scaling form, not a universal theorem statement. Real bounds include constants, decoder assumptions, correlated-noise caveats, and architecture-specific effects.)*

A reader can run the suppression direction by hand on the standard surface-code
threshold-theorem scaling form `p_pair(d) <= C (p / p_th)^{floor((d+1)/2)}` for a
distance-`d` code (the form used in `qm_103_show_the_packet_protocol` §9),
with the illustrative numbers `C = 1`, physical error rate `p = 1e-3`, threshold
`p_th = 1e-2` (so `p/p_th = 0.1`); for the odd distances below the floor is exact:

| `d` | exponent `floor((d+1)/2)` | `p_pair(d) = (0.1)^{floor((d+1)/2)}` |
|---:|---:|---:|
| 3 | 2 | `1e-2` |
| 5 | 3 | `1e-3` |
| 7 | 4 | `1e-4` |
| 9 | 5 | `1e-5` |

So `p_pair(d) -> 0` as `d` grows **precisely because `p < p_th`** (the declared
hypothesis). Drive `p_pair` below any fixed logical-visibility threshold `tau < C` by
choosing the distance so `floor((d+1)/2) >= log(tau/C)/log(p/p_th)` (the right side
is a positive number — numerator and denominator are both negative since `tau < C`
and `p < p_th`); at that `d` the logically visible residual contribution drops below `tau`, so the conditional no-go does not fire inside this packet.
This is **arithmetic on imported hypotheses**, not a claim that any device achieves
`p < p_th`: flip the inequality to `p > p_th` and `p_pair(d)` *grows*, populating the
packet's `terminal_status` as the conditional no-go regime instead. The combinatorial
repair-image monotonicity (enlarging the repair image strands no more defects) is the
MECHANIZED axiom-free witness `OmegaCore.QM.repair_monotone` (ENC-1066); the *rate*
inequality `mu_repair >= lambda_proj` at scale is the imported, never-mechanized
burden of §3.

3. What stays imported (the open burden)


THR-001 is a packet-population implication, **not** a proof that any physical
device satisfies `H(Theta)` at human-significant scale. The architecture premises
are imported, not derived here:

These are architecture-class accounting obligations (the open burden flagged in
`qm_100_projection_obstruction_technical_appendix`),
not slogans, and not discharged by THR-001.

4. Status / Scope / Evidence / Authority


* **Status:** the THR-001 packet-population mapping is a *construction* (fields read off
  `Theta`'s declared data); the *derived* content is the scoped, conditional
  no-go-does-not-fire implication (§2 corollary).

* **Scope:** declared threshold-theorem hypotheses on a named code family and noise
  regime; carrier- and architecture-class relative.

* **Evidence:** the packet-population mapping is a construction; the §2 scoped corollary is
  prose-proved (the §2.1 hand-runnable arithmetic). The combinatorial repair-image monotonicity
  is MECHANIZED axiom-free (`OmegaCore.QM.repair_monotone`, ENC-1066); the §2 scoped corollary is
  not yet mechanized (open Lean target, PL-QM015-2).

* **Authority:** none minted. A complete packet records a *conditional* terminal;
  the only arrow into authority is a CODA-FDA `Pi_sharp` terminalization
  (`StructureDerived ⇏ IsAuth`).

5. Falsifiability ledger entry


* **What would falsify it:** a demonstration that a threshold theorem's declared
  hypotheses hold at the target workload while `p_pair` provably fails to approach
  zero (i.e. the induced `pairing_bound` is not a suppression bound).

* **What would weaken it:** showing the packet-population mapping in §2 omits a
  load-bearing field for some architecture class.

* **What would strengthen it:** mechanizing the §2 corollary in Lean so the
  "no-go does not fire" step is checked, not prose-proved.

6. Non-claims


> **[OBLIGATION]** Verify the exact threshold theorem citations and titles against primary sources.
> **[OBLIGATION]** Add a one-line relation to Willow / current experiments only after primary-source verification of their specific error budgets.
> **[RELEASE NOTE]** Release near QM_100, not alone.

* Does **not** say any threshold theorem is refuted.
* Does **not** say physical quantum scalability is established or impossible —
  physical quantum scalability remains unterminated under this evidence standard.

* Does **not** derive QM, derive a threshold theorem, or mint authority.

7. Dependencies


`qm_100_projection_obstruction_public_paper`,
`qm_100_projection_obstruction_technical_appendix`,
`qm_103_show_the_packet_protocol`. Falsifier
recorded in `QM_Series_Falsifiability_Ledger`
Mechanized repair-image monotonicity at
`OmegaCore.RepairMonotonicity`
(ENC-1066); the §2 scoped-corollary Lean target is open (PL-QM015-2). Overlapping kernel:
QM_061 (archived to `qm_archived_stubs_022_026`)
(cross-reference, not merged).

> **Series-wide link note (consolidation pass).** Links to folderized siblings
> (QM_081/002/003/004/032/035/036) are flat in this draft and need folder segments;
> this is a pre-existing, series-wide condition flagged for the consolidation pass, not
> fixed piecemeal here.

Changelog

Version Note: v2.0 (2026-06-17)** — first hygiene-pipeline Improver pass. Added a payoff lead
  sentence (threshold ⇒ conditional repair-capacity certificate; threshold theorems
  STANDARD/imported, not re-proved); added §0.1 "why care", §0.2 related work (3 imported
  theorem families + 3 sibling papers; citation years verified against qm_103_show_the_packet_protocol's bibliography),
  §0.3 notation pointer, and a §2.1 hand-runnable suppression-bound worked example (surface-code
  scaling form, aligned to qm_103_show_the_packet_protocol §9). Fixed two §4 typos. Created the companion Claim Ledger.
  No claim widened; honest hedges and the "physical scalability unterminated" non-claim left intact.

* *Stage 2 (adversary):* demoted the THR-001 packet-population mapping from `[PROVEN — prose]` to
    `[DEFINITION / CONSTRUCTION]` (true by how the packet is defined; the genuinely derived content is the
    §2 scoped corollary, `[PROVEN, CONDITIONAL + H(Theta)]`); resolved the citation-year `[VERIFY]` against
    qm_103_show_the_packet_protocol's bibliography.

* *Stage 3 (proof sign-off):* corrected a paper↔encyclopedia status drift — the repair-image monotonicity
    is **MECHANIZED axiom-free** (`OmegaCore.QM.repair_monotone`, ENC-1066), not the "open Lean target" the
    draft claimed, and the cited path `QM.RepairMonotonicity` was wrong → `OmegaCore/...`.
    Separated the (mechanized) combinatorial monotonicity from the (imported, never-mechanized) rate
    inequality; tightened the §2.1 crossover condition to `tau < C`. The remaining open Lean target is the §2
    scoped corollary (PL-QM015-2).

<!-- claim-id-body-index:begin -->

Claim-ID body index (packaging)

| ID | Home |
|---|---|
| `QM-101-C1` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `101:QM-101-C1`) |
| `QM-101-C2` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `101:QM-101-C2`) |
| `QM-101-C3` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `101:QM-101-C3`) |
| `QM-101-C4` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `101:QM-101-C4`) |
| `QM-101-C5` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `101:QM-101-C5`) |
| `QM-101-C6` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `101:QM-101-C6`) |
| `QM-101-C7` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `101:QM-101-C7`) |
| `QM-101-C8` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `101:QM-101-C8`) |
| `QM-101-C9` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `101:QM-101-C9`) |
| `QM-101-C9b` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `101:QM-101-C9b`) |
| `QM-101-C10` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `101:QM-101-C10`) |
| `QM-101-C11` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `101:QM-101-C11`) |
| `QM-101-C12` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `101:QM-101-C12`) |
| `QM-101-C13` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `101:QM-101-C13`) |
| `QM-101-C14` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `101:QM-101-C14`) |

<!-- claim-id-body-index:end -->
