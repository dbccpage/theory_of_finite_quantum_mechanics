# Interference as the Non-L1 Resource and the Buildability Set S

## GTOC Foundations — Quantum Contact Series (qm_061_interference_as_the_non_l1_resource)

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

document_id: "OMEGA-QM-INTERFERE-044"
version: "0.2.0"
last_updated: "2026-06-19"
status: "DRAFT — component note (rung 6) of QM_121 (The Finite QM Ingredient Ladder)"
series: "qm / QM ingredient ladder"
companions:
- "pub-010 Born Normalization … Redundancy (the interference cross term this paper reads)"
- "QM_060 Superposition as the Quotient Fiber (the phase fiber this paper activates)"
- "QM_007 Density Matrices as Diagonal Residual Weights (the L1 / diagonal layer)"
- "QM_101 Threshold Theorems as Repair-Capacity Certificates (credited)"
- "QM_061 Repair-Capacity Conditional No-Go (Track C stub; set S is a two-sided finite criterion corresponding to it)"
- "QM_091 Deutsch–Everett–Wolfram Promotion Error (the firewall)"
mechanization: "QM.InterferenceBuildability (lean 4.31.0-rc1, RC 0, axioms ⊆ {propext, Quot.sound}); secured ENC-1135 (paper:qm061:INTERFERE-001, MECHANIZED)"

---

### A finite criterion schema — not a physical no-go or existence theorem

> **Component note (rung 6) of *QM_121 — The Finite QM Ingredient Ladder*.** The publishable synthesis
> is QM_121; this note is the detailed source for the interference rung (the one genuinely non-classical
> rung) and the buildability set S, and keeps its own claim ledger.

Abstract

**Scope fence (read first).** This is a **finite criterion schema, not a physical
no-go or existence theorem.** It does **not** claim quantum computing is impossible,
$\mathrm{BQP}\subseteq\mathrm P$, efficient classical simulation of arbitrary quantum
systems, or a derivation of the $\mathbb C$/$U(1)$ carrier, the Born rule, or unitary
dynamics (full non-claims in the closing section). The $\mathbb C$/$U(1)$ phase
carrier, the size-independent generation density $\lambda_{\mathrm{gen}}$, and the
Lieb–Robinson cone are **imported** inputs, not derived here.

**Structure.** **Part A re-packages an existing mechanized result** (pub-010
Theorem 7); **Part B is the new content** (the buildability criterion $S$).

**Main result (informal).**
*(A) — reuse.* The L1 layer is the *diagonal* Born data, the per-sector weights
$|c_s|^2$ (QM_007); interference is the coherent-sum weight $|\sum_s c_s|^2$, which
depends on relative phase. Two configurations can share *identical* L1 data yet
differ in interfered outcome, so **no function of the L1 weights determines
interference** — the advantage resource cannot be reconstructed by classical
diagonal algebra. This is pub-010 Theorem 7 re-packaged (same $(1,1)/(1,-1)$
witness). We then add an *interpretive* reading: the non-L1 interference resource is
**tracked by** non-coboundary phase holonomy (a nonzero $H^1$ class); the numerical
cross term is **not yet proved** to be a closed-form function of that holonomy object.
*(B) — new.* Define a finite buildability predicate `UsefulQC` for a *declared*
architecture (repair/generation rates, a persistent logical floor, in-cone
reachability, and an $H^1$ interference resource). **Inside this declared finite
model, the `UsefulQC` predicate is equivalent to** $S_1\wedge S_2\wedge S_3\wedge S_4$;
each $S_i$ is independently necessary (drop-one witnesses); and the $S$-predicate is
**formally satisfiable** (the criterion is non-vacuous). This is a **packet criterion
— not a proof that any physical device satisfies $S$, and not a no-go.**

**Why a researcher should care.** Two deflations fail. First, "the quantum advantage
is just clever classical bookkeeping" — result A shows the interference resource is
provably *not* L1/diagonal-computable (compatible with the Holevo lesson that
classical/diagonal readouts do not exhaust quantum information, though **not** a
derivation or finite version of Holevo's theorem; cf. RDB-03). Second, "buildability
is an open-ended fog" — $S$ states finite, falsifiable conditions and locates the
make-or-break at $S_1\cap S_4$ (keep a nonzero $H^1$ holonomy alive *inside* the
Lieb–Robinson cone, which local repair cannot restore once lost). Threshold theorems
can be **read as architecture-specific witnesses for some $S$-conditions under their
own declared hypotheses**; $S$ is a unifying audit schema, not a restatement or
completion of the threshold-theorem literature.


Part A — Interference is the non-L1 resource

### 1. Carrier

Residual sector amplitudes $c_s$ over a finite sector set; the **L1 / diagonal
carrier** is the per-sector Born weight $|c_s|^2$ (QM_007: density matrices as
diagonal residual weights). This is all the classical diagonal layer reads.
[DEFINITION]

### 2. Primitive difference

The L1-blind primitive difference between two configurations is compared on the
diagonal weights only, $\delta(c,c')_s = |c_s|^2 - |c'_s|^2$ (pub-010, the
phase-blind quotient; cf. QM_060). It ignores phase entirely. [DEFINITION]

### 3. ZeroRel

$\delta \equiv 0$ identifies configurations with equal moduli at *any* phases:
**L1-equivalence**. Configurations sharing diagonal weights are one point of the L1
quotient. [DEFINITION]

### 4. Structure

The **interfered (coherent-sum) weight** $\mathcal I(c) = \big|\sum_s c_s\big|^2$ is a
functional on configurations. Its deviation from the diagonal sum is the
**interference cross term** $\mathcal I(c) - \sum_s|c_s|^2 = \sum_{i\neq j} c_i^{*}c_j$
(pub-010 Thm 7) — exactly the fiber content QM_060 showed is invisible to the
phase-blind quotient, here *activated* by mixing. [DEFINITION]

### 5. The non-L1 theorem

**Theorem A1 (interference is not an L1 functional).** There is no function $f$ of the
L1 (diagonal Born) weights with $\mathcal I(c) = f(L1(c))$ for all $c$. Equivalently,
two L1-equivalent configurations can have different interfered outcomes.
[PROVEN, MECHANIZED — **reuse of pub-010 Theorem 7**; re-packaged zero-import as
`L1_cannot_compute_interference`, `InterferenceBuildability`]

**Source / non-novelty (read first).** Theorem A1 is *not new here* — it is exactly
**pub-010 Theorem 7** ("the Hilbert lift is probability-redundant but
dynamics-capable"), which already proves this with the *same* witness `(1,1)`/`(1,−1)`
and mechanizes it far more extensively (`PaperQF002.L010_01_BornRedundancy`: the
`twoRowMix*` suite, the phase-blind-quotient non-factorization, the imbalance
$2xy/(x^2+y^2)$). `InterferenceBuildability` only **re-packages** that result
as a self-contained, zero-import kernel for the buildability bundle. The genuinely
new content of this paper is Part A §6 (the *holonomy* reading of interference,
`[INTERPRETIVE]`) and Part B (the set `S`), not A1 itself.

**Worked example.** $c=(1,1)$ and $c'=(1,-1)$ have identical L1 data
$(|c_0|^2,|c_1|^2)=(1,1)=(|c'_0|^2,|c'_1|^2)$ but interfered outcomes
$\mathcal I(c)=|1+1|^2=4$ and $\mathcal I(c')=|1-1|^2=0$ — total constructive vs total
destructive at the *same* L1. The L1-invisible deviation is $\mathrm{cross}(c)=+2$,
$\mathrm{cross}(c')=-2$. [WORKED EXAMPLE — `cPlus_cMinus_*`, decided]

This is the same fact as **pub-010 Theorem 7** (primary, in-corpus source) and the
finite form of the corpus's RDB-03 (sector probabilities do not determine phase/sign):
the diagonal/classical layer provably cannot carry the interference content. It is
**compatible with the Holevo lesson** that classical/diagonal readouts do not exhaust
quantum information, but it is **not** a derivation or finite version of Holevo's
theorem (Holevo bounds *accessible information*; A1 is a *non-identifiability* fact —
same L1, different coherent sum). [PROVEN — reuse of pub-010 Thm 7; cf. RDB-03;
Holevo-*compatible*, not Holevo]

### 6. The holonomy bridge

Interference is the **holonomy** $\oint_\gamma a$ of the phase 1-cochain $a$ around
the two-path loop $\gamma$. A *coboundary* (gauge) phase $a=d_0\varphi$ telescopes to
**zero holonomy** around any closed walk.

**Theorem A2 (coboundary phase has no holonomy).** For a coboundary phase along any
closed walk, $\oint a = 0$. [PROVEN, MECHANIZED — `coboundary_loop_zero_holonomy`,
the self-contained LT-P fact; cf. `SemiringTransportKernel.coboundary_trivial_holonomy`]

**Reading (interference is *tracked by* the $H^1$ holonomy).** Combining A1 and A2: the gauge
part is removable and carries no gauge-invariant interference, while A1 shows
genuine interference is content beyond the diagonal. So the interference resource
lives in the **non-coboundary class** — a nonzero $H^1=\ker d_1/\operatorname{im}d_0$
holonomy. This identification is *argued from* the two mechanized facts; it is not a
single closed-form theorem (the numerical value of the cross term as a function of
the holonomy requires the continuum cosine and is out of finite scope). [INTERPRETIVE]

**Import fence.** That amplitudes carry phase at all — the $\mathbb C$/$U(1)$ carrier —
is **imported**, not derived here; it is the open $U(1)$-selector of the Force-$\mathbb C$
program. *Given* a phase-bearing transport, interference is its holonomy; this paper
mechanizes only that conditional structure. [IMPORTED]


Part B — The buildability set S

### 7. Useful versus merely working

A device that holds a logical qubit but offers no resource beyond the
stabilizer/coboundary regime is classically simulable (Gottesman–Knill; and, in this
corpus's own terms, **pub-010 Theorem 3** — phase-blind descent forces *monomial*
/ permutation-and-phase maps, the row-sparse "classically-trackable" class) — "four
qubits that do nothing." **Useful** means *working and advantageous*: it must carry
the non-L1 resource of Part A. [SCOPE FENCE / DEFINITION]

### 8. The set S

For a declared finite architecture (rates $\lambda_{\mathrm{gen}},\mu_{\mathrm{rep}},
\varepsilon_{\mathrm{mix}}$; declared capabilities):

- **$S_1$ — race:** $\mathrm{step}=\lambda_{\mathrm{gen}}-\mu_{\mathrm{rep}}-
  \varepsilon_{\mathrm{mix}}\le 0$ (in-cone repair beats generation);

- **$S_2$ — logical floor:** a protected logical class persists ($p_{\mathrm{floor}}>0$);
- **$S_3$ — reachability:** the correctable (coboundary) syndrome is within the
  Lieb–Robinson cone, so repair can act;

- **$S_4$ — advantage:** a genuine non-coboundary $H^1$ interference resource exists
  (Part A) — else classically simulable. [DEFINITION]

### 9. The criterion

**Theorem B1 (finite buildability-predicate equivalence).** *Inside the declared
finite model*, the predicate `UsefulQC` is equivalent to
$S_1\wedge S_2\wedge S_3\wedge S_4$. The content (not a relabeling) is the genuine
biconditional $\mathrm{Bounded}\Leftrightarrow \mathrm{step}\le 0$ — the residual
stays correctable for all cycles iff the net increment is nonpositive. This is a
**packet criterion over declared predicates, not a physical existence theorem about
scalable quantum computers.** [PROVEN, MECHANIZED — `useful_qc_iff_setS`,
`bounded_iff_step_nonpos`]

**Theorem B2 (each member is independently necessary).** For each $i$ there is a
system satisfying every $S_j$ ($j\neq i$) but $\neg S_i$ that is not useful (drop-one
witnesses): drop $S_1$ → residual unbounded; drop $S_2$ → no class to protect; drop
$S_3$ → repair cannot act; drop $S_4$ → classically simulable. [PROVEN, MECHANIZED —
`S1_necessary` … `S4_necessary`]

**Theorem B3 (non-vacuity).** The formal $S$-predicate is **satisfiable** — some
declared system satisfies all of $S$ — so the criterion is non-vacuous (it admits a
buildable+advantageous model; it is not a disguised no-go). This is satisfiability of
a predicate, **not** the claim that a physical useful-QC device exists. [PROVEN,
MECHANIZED — `setS_satisfiable`]

**Fence.** The members of $S$ are *declared* conditions on an architecture; Theorem
B1 is a finite criterion, **not** a proof that any physical device satisfies $S$. The
race uses two imported inputs as cited hypotheses: the size-independent generation
density $\lambda_{\mathrm{gen}}$ (PAPER001 / Zenodo 20650922 finding 3) and the
Lieb–Robinson cone bound on $\mu_{\mathrm{rep}}$. [CONDITIONAL / SCOPE FENCE]

### 10. Relation to threshold theorems (QM_101)

Fault-tolerance threshold theorems can be **read as architecture-specific witnesses
for some $S$-conditions under their own declared hypotheses** (noise model, code
family, decoder, locality, overhead) — candidate instantiations, credited not
refuted (QM_101). $S$ is a **unifying audit schema**, not a restatement or completion
of the threshold-theorem literature. Relative to the earlier Track-C conditional
no-go stub (an archived precursor) — which gave only the one-directional "persistent
gap $\Rightarrow$ unbounded residual" — $S$ supplies a **two-sided finite criterion** (B1's biconditional) that
also folds in the advantage requirement $S_4$. The make-or-break is read as
$S_1\cap S_4$: keep a nonzero $H^1$ holonomy alive inside the Lieb–Robinson cone,
which local repair provably cannot restore once lost (`H1_not_in_cone_repairable`,
`H1_repair_invariant`). [INTERPRETIVE]


Mechanization

`QM.InterferenceBuildability` is Mathlib-free (checks with direct
`lean`), `sorry`/`admit`-free, and every theorem depends only on
$\{$`propext`, `Quot.sound`$\}$ (five are fully axiom-free). It carries: Part A
(`L1_cannot_compute_interference`, `cPlus_cMinus_*`, `holo_telescope`,
`coboundary_loop_zero_holonomy`), the $H^1$-irreparability mirror
(`H1_not_in_cone_repairable`, `H1_repair_invariant`), the race biconditional
(`rho_closed_form`, `bounded_iff_step_nonpos`), and Part B
(`useful_qc_iff_setS`, `S1_necessary`…`S4_necessary`, `setS_satisfiable`). The
companion `LiebRobinsonBuildability` supplies the race/dichotomy substrate.

**Mechanization receipt.** The evidence ledger records a zero-import checked replay of the stable target `QM.InterferenceBuildability`. Per load-bearing theorem it reports either `does not depend on any axioms` or `depends on axioms: [propext, Quot.sound]` — for example:

```text
'QM.InterferenceBuildability.L1_cannot_compute_interference' depends on axioms: [Quot.sound]
'QM.InterferenceBuildability.useful_qc_iff_setS' depends on axioms: [propext, Quot.sound]
'QM.InterferenceBuildability.S2_necessary' does not depend on any axioms
```

The file ends with `#print axioms` directives for all 15 theorems; it is
`sorry`/`admit`-free and emits no `sorryAx`.

Claim status (the honest hierarchy)

| status | claims |
|---|---|
| **PROVEN / MECHANIZED** | A1 L1-data ⊬ interference (*reuse* of pub-010 Thm 7); A2 coboundary phase ⇒ zero closed-walk holonomy; `Bounded ⟺ step ≤ 0`; the declared `UsefulQC` predicate ⟺ $S_1\wedge S_2\wedge S_3\wedge S_4$; each $S_i$ drop-one necessary; the $S$-predicate is satisfiable |
| **INTERPRETIVE** | the interference resource is *read as* non-coboundary $H^1$ holonomy (no closed-form cross-term↔holonomy theorem yet); threshold theorems *instantiate* some $S$-conditions under their own hypotheses; make-or-break read as $S_1\cap S_4$ |
| **IMPORTED / CONDITIONAL** | the $\mathbb C$/$U(1)$ phase carrier; $\lambda_{\mathrm{gen}}$ (PAPER001 / Zenodo 20650922); the Lieb–Robinson cone; whether any *physical* architecture satisfies $S$ |
| **NOT CLAIMED** | QC impossible; $\mathrm{BQP}\subseteq\mathrm P$; efficient classical simulation of arbitrary quantum systems; derivation of Born / $\mathbb C$/$U(1)$ / unitary dynamics; any interpretation of QM |

Falsifiability

This paper fails if any of the following is exhibited: a function of the L1 diagonal
weights that reproduces the interfered outcome (refuting A1); a coboundary phase with
nonzero holonomy around a closed walk (refuting A2); a *useful* (advantageous)
scalable device violating some $S_i$ while satisfying the rest (refuting B1/B2); or a
proof that the $H^1$ interference class is in-cone repairable (refuting the make-or-
break). Each is a finite, checkable target.

What this does not claim

1. **Not** that quantum computing is impossible — $S$ is satisfiable (B3) and the
   threshold theorems live in its satisfied regime.

2. **Not** $\mathrm{BQP}\subseteq\mathrm P$, and **not** efficient classical
   simulation of arbitrary quantum systems (the coboundary $\Leftrightarrow$
   classically-efficient correspondence is the cited Gottesman–Knill, at the
   obstruction-class level only).

3. **Not** that any interpretation of QM is true or false. Result A is
   interpretation-neutral: the interference resource is a finite $H^1$ holonomy,
   readable by an Everettian as branch interference and by a single-worlder as a
   phase obstruction; "worlds" adds nothing packet-distinguishable (QM_091).

4. **Not** a derivation of the $\mathbb C$/$U(1)$ carrier, the Born rule, or unitary
   dynamics — all imported (QM_091, GOMC-08).

5. Mints no authority: a proof is a verified finite computation
   ($\mathsf{StructureDerived}\not\Rightarrow\mathsf{IsAuth}$).

References

- pub-010, *Born Normalization … Redundancy* — **the primary source.** **Theorem 7**
  IS the interference-not-L1 result re-packaged here as Part A (same `(1,1)`/`(1,−1)`
  witness, mechanized in `PaperQF002.L010_01_BornRedundancy`); **Theorem 3** (phase-blind
  descent ⇒ row-sparse/monomial maps) is the in-corpus form of the classically-trackable
  (coboundary) class used in Part B; Theorem 4 is the Born-redundancy QM_060 reuses.

- QM_060, *Superposition as the Quotient Fiber*; QM_007, *Density Matrices as
  Diagonal Residual Weights*; QM_101, *Threshold Theorems as Repair-Capacity
  Certificates*; QM_061, *Repair-Capacity Conditional No-Go*; QM_091,
  *Deutsch–Everett–Wolfram Promotion Error*.

- A. S. Holevo, *Bounds for the quantity of information transmitted by a quantum
  communication channel*, Probl. Peredachi Inf. **9** (1973) 3–11.

- D. Gottesman (1998); S. Aaronson & D. Gottesman, PRA **70** (2004) 052328
  (stabilizer = classically efficient, cited at the obstruction-class level).

- E. H. Lieb & D. W. Robinson, Commun. Math. Phys. **28** (1972) 251 (the cone).
- J. H. Carroll, *Projection Obstruction for Factorized States*, Zenodo 20650922
  (finding 3: the size-independent generation density $\lambda_{\mathrm{gen}}$).

<!-- claim-id-body-index:begin -->

Claim-ID body index (packaging)

| ID | Home |
|---|---|
| `QM-061-C1` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `061:QM-061-C1`) |
| `QM-061-C2` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `061:QM-061-C2`) |
| `QM-061-C3` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `061:QM-061-C3`) |
| `QM-061-C4` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `061:QM-061-C4`) |
| `QM-061-C5` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `061:QM-061-C5`) |
| `QM-061-C6` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `061:QM-061-C6`) |
| `QM-061-C7` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `061:QM-061-C7`) |
| `QM-061-C8` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `061:QM-061-C8`) |
| `QM-061-C9` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `061:QM-061-C9`) |
| `QM-061-C10` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `061:QM-061-C10`) |
| `QM-061-C11` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `061:QM-061-C11`) |
| `QM-061-C12` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `061:QM-061-C12`) |
| `QM-061-C13` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `061:QM-061-C13`) |
| `QM-061-C14` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `061:QM-061-C14`) |
| `QM-061-C15` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `061:QM-061-C15`) |
| `QM-061-C16` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `061:QM-061-C16`) |
| `QM-061-C17` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `061:QM-061-C17`) |

<!-- claim-id-body-index:end -->
