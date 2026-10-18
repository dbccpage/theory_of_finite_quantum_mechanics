# The U(1)-Selector: What Forces ℂ — a Conditional Forcing of the Complex Carrier

## GTOC Foundations — Quantum Contact Series (qm_062_the_u1_selector)

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

document_id: "OMEGA-QM-U1SELECTOR-046"
version: "0.1.0 (Pre-Print)"
last_updated: "2026-06-19"
status: "DRAFT — sharpens OB-U1 (the open ℂ/U(1) selector of QM_121); not a derivation of ℂ from nothing"
series: "qm / QM ingredient ladder — the imported-ceiling selector"
companions:
  - "QM_121 The Finite QM Ingredient Ladder (OB-U1: ℂ/U(1) is the open selector this paper sharpens)"
  - "QM_061 Interference / QM_110 FWTE (only signedness is forced by the ladder, not ℂ)"
  - "QM.ForceComplexCarrier (T-FORCE-★ conjugation; T-FORCE-ℂ Frobenius exclusions)"
  - "QM.U1Selector (the complex-structure layer: J²=−I, ℂ as the J-algebra)"
mechanization: "ForceComplexCarrier (Mathlib-free, conjugation forced + ℝ-signed/ℍ excluded within the declared Frobenius comparison class, FCAI honest gap) + U1Selector (Mathlib-light: J²=−I, {aI+bJ}≅ℤ[i] complex product, cx ring-embedding, axioms ⊆ {propext,Quot.sound}); secured ENC-1136"

The U(1)-Selector: What Forces ℂ
================================

> **Honest headline.** This paper does **not** derive ℂ from nothing. This is a ceiling-selector note, not a ladder rung that derives QM. It *localizes the import*:
> it shows precisely which named ingredients force the complex carrier ℂ/U(1) at the two-level core,
> and names the residue that genuinely stays imported. OB-U1 (QM_121's open selector) is **sharpened
> from "ℂ imported, open" to "ℂ/U(1) conditionally forced; the residual import named"** — not discharged.

Abstract

**Main result (informal).** The finite obstruction ladder (QM_061/QM_121) forces **signedness** — a
two-row mix distinguishes $(1,1)$ from $(1,-1)$ — but only signedness: a real-signed ($\mathbb{Z}/2$)
carrier already produces interference, so the ladder alone does **not** select $\mathbb{C}$. We
assemble the carrier-selection in two mechanized layers and state the honest conditional forcing.
*(1) A nontrivial invariant phase forces a conjugation* (`ForceComplexCarrier`, T-FORCE-★): a
phase-invariant interference cross-term is incompatible with a symmetric/bilinear modulus and
**requires a genuine involution** $\ast$ — the $\mathbb{C}$-shape, not the $\mathbb{R}$-bilinear one.
*(2) Within the declared Frobenius comparison class ($\mathbb{R}/\mathbb{C}/\mathbb{H}$)*, the real-signed carrier is excluded
(its phase fiber is discrete, exponent 2), the quaternionic carrier is excluded (non-abelian phase),
and $\mathbb{C}$ is admitted (T-FORCE-ℂ) — but the abstract phase-group shadow **cannot separate
$U(1)$ from the torsion shadow $\mathbb{Q}/\mathbb{Z}$**. Without continuity, the selector does not uniquely choose $U(1)$. With continuous reversible pairing-preserving transport, the $J$-algebra selects the complex carrier at the two-level core. *(3, new — `U1Selector`)* at the concrete
two-level system, the generator of continuous reversible pairing-preserving transport is a **complex
structure** $J$ with $J^2=-I$, the algebra it generates **is $\mathbb{C}$** (realized over the
integers as the Gaussian integers $\mathbb{Z}[i]$, via an injective ring embedding $\mathbb{Z}[i]\hookrightarrow
M_2(\mathbb{Z})$), and the continuous transport group is $SO(2)\cong U(1)$ — the unit circle of
$\mathbb{C}$ — separated from the discrete sign $\mathbb{Z}/2$ by $J^2=-I\neq+I=S^2$.

**The conditional forcing.** $\mathbb{C}/U(1)$ is forced **at the two-level core**, *given*: a
nontrivial invariant phase (⇒ conjugation), an abelian phase action (excludes $\mathbb{H}$), and a
**continuous reversible pairing-preserving transport** (⇒ the complex structure $J^2=-I$ and
$SO(2)=U(1)$, excluding the discrete real-signed carrier). The residue that **stays imported**, now
named: (i) the *continuity* of reversible dynamics itself (a one-parameter flow exists — the corpus's
already-imported continuum/dynamics clause); (ii) the *global* field-uniqueness across all dimensions
(why global real QM exclusion is imported for composite systems ($n>2$)) — local tomography (Hardy 2001; Masanes–Müller 2011) and the empirical
real-vs-complex falsification (Renou et al., *Nature* 2021).

**Why a researcher should care.** "Why is quantum theory complex?" is usually answered either by an
imported reconstruction axiom (local tomography) or left as a postulate. This paper separates the
question into a part that is *forced and machine-checked* — the complex **structure** $J^2=-I$ and the
$\mathbb{C}$-algebra of continuous two-level transport — and a part that is *genuinely imported* and
now *named precisely* (continuity; global field-uniqueness). It converts a vague "ℂ is imported" into
an auditable "ℂ/U(1) is forced by *these* ingredients; the import is *exactly* this."

1. The gap OB-U1 (what the ladder leaves open)


The ladder (QM_061 signedness) forces only **signedness**: $(1,1)$ and $(1,-1)$ share the identical
$\ell^1$ law but mix to interfered $4$ vs $0$. A real-signed carrier (phase fiber $\{\pm1\}=\mathbb{Z}/2$)
already exhibits this. So the question "why $\mathbb{C}$ (and $U(1)$), not $\mathbb{R}$-signed or
$\mathbb{H}$?" is **not** answered by interference alone. [SCOPE FENCE — the open obligation QM_121 OB-U1.]

2. Layer 1 — a nontrivial invariant phase forces a conjugation (T-FORCE-★)


`ForceComplexCarrier` (Mathlib-free) proves the sharp dichotomy on the modulus pairing: the
interference cross-term is invariant under a *global phase* applied to both branches **iff** the
pairing carries a genuine involution $\ast$ with $\ast(u)\,u=1$. With $\ast=\mathrm{id}$ (the
symmetric/bilinear, real-signed shape) the cross-term rescales by $u^2$ and is invariant **only** for
the trivial signs $u=\pm1$; a nontrivial continuous phase is then *excluded*. So a nontrivial invariant
phase **forces a conjugation** — the $\mathbb{C}$-shape (`conjugation_forced`,
`realSigned_phaseInvariant_only_signs`). [PROVEN, MECHANIZED — `ForceComplexCarrier`.]

3. Layer 2 — Frobenius exclusions, and the honest $U(1)$-vs-torsion gap (T-FORCE-ℂ)


Modelling the unit-fiber phase group abstractly, `ForceComplexCarrier` proves: real-signed
($\mathbb{Z}/2$) is **excluded** — its fiber is discrete (exponent 2, no element of order $>2$);
quaternionic ($Q_8$) is **excluded** — its phase action is non-abelian ($i\!\cdot\!j=k\neq-k=j\!\cdot\!i$);
$\mathbb{C}$ **admits** the abelian, order-unbounded ("faithful-continuous") interference fiber. [PROVEN,
MECHANIZED — `Z2_not_FCAI`, `Qua_not_FCAI`, `ProdCyc_FCAI`.]

**The honest gap, stated by that file itself:** the abstract phase-group property (abelian +
order-unbounded) does **not** uniquely pick $\mathbb{C}$ — it is also satisfied by the torsion shadow
$\mathbb{Q}/\mathbb{Z}$ (which contains $\mathbb{Z}/n$ for every $n$ but is not $U(1)$). The finite
phase-group shadow cannot see the topology that separates $U(1)$ from its torsion subgroup. [SCOPE
FENCE — uniqueness-among-FCAI not established by Layer 2.]

4. Layer 3 (new) — the complex structure of continuous two-level transport


`U1Selector` (Mathlib-light, over $\mathbb{Z}$) supplies exactly the piece Layer 2 cannot see, at the
concrete two-level system. The generator of continuous reversible transport (rotation) is

$$
J=\begin{psmallmatrix}0&-1\\1&0\end{psmallmatrix},\qquad J^2=-I,
$$

a **complex structure**; the discrete sign carrier $S=\operatorname{diag}(1,-1)$ has $S^2=+I$, and
$J^2=-I\neq+I=S^2$ separates the continuous from the discrete carrier (`J_sq`, `S_sq`,
`continuous_vs_discrete`). The algebra it generates,

$$
\{aI+bJ\},\qquad (aI+bJ)(cI+dJ)=(ac-bd)I+(ad+bc)J,
$$

**is the complex multiplication** — realized over the integers as an injective ring embedding
$\mathbb{Z}[i]\hookrightarrow M_2(\mathbb{Z})$ (`cx_mul`, `cx_add`, `cx_one`, `cx_realizes_gaussian`,
`cx_injective`): $\mathbb{C}$ (its integer form) **appears** as the J-generated algebra, not by fiat.
The continuous transport group is $SO(2)\cong U(1)$ — the unit circle of $\mathbb{C}$, composing by
angle addition — separated from the torsion shadow by the existence of a **connected one-parameter
generator** $J$ (which a torsion group lacks). [PROVEN, MECHANIZED over $\mathbb{Z}$ — `U1Selector`;
the continuous $SO(2)=U(1)$ angle-addition over $\mathbb{R}$ is standard, its discrete $\mathbb{Z}/n$
rotation shadow mechanized in `ForceComplexCarrier` (`Cyc n`).]

5. The conditional forcing (the honest synthesis)


Assembling Layers 1–3, **at the two-level core**:

$$
\boxed{\;\text{conjugation (L1)}\;\wedge\;\text{abelian phase (L2, excludes }\mathbb{H})\;\wedge\;\text{continuous reversible pairing-preserving transport (L3)}\;\Longrightarrow\;\mathbb{C}/U(1);}
$$

The discrete real-signed carrier is excluded (L2 discreteness; L3 $S^2=+I\neq J^2$); $\mathbb{H}$ is
excluded (L2 non-abelian); and the surviving carrier carries the complex structure $J^2=-I$ with
algebra $\mathbb{C}$ and transport group $U(1)$ (L3). [INTERPRETIVE synthesis over the MECHANIZED
L1–L3.]

**What remains imported (named, not removed):**

1. **Continuity of reversible dynamics** — that a *connected one-parameter* transport exists at all. Without continuity, the selector does not uniquely choose $U(1)$. With continuous reversible pairing-preserving transport, the $J$-algebra selects the complex carrier at the two-level core.
   This is the corpus's already-imported continuum/dynamics clause; without it, only the discrete sign
   and the torsion shadow are forced, not $U(1)$. [IMPORTED.]

2. **Global field-uniqueness across all $n$** — why global real QM exclusion is imported for composite systems ($n>2$),
   pinning $\mathbb{C}$ over $\mathbb{R}$ globally: local tomography (Hardy 2001; Masanes–Müller 2011)
   and the empirical real-vs-complex falsification (Renou et al., *Nature* 600 (2021) 625). [IMPORTED.]

So OB-U1 is **sharpened, not discharged**: the complex *structure* is forced and mechanized at the
two-level core; the two imports above are the precise, named residue. This is the same firewall move
as pub-010's Born-uniqueness fence (imported via Gleason, named precisely) — bold in localizing the
import, conservative in claim.

Worked example

Over $\Gamma=\{0,1\}$ amplitudes: the sign carrier $S=\operatorname{diag}(1,-1)$ flips $(1,1)\mapsto(1,-1)$
(the $\mathbb{Z}/2$ interference of QM_061), and $S^2=I$ — it returns in two steps, a discrete phase.
The matrix $J=\begin{psmallmatrix}0&-1\\1&0\end{psmallmatrix}$ has $J^2=-I$ and $J^4=I$, generating the cyclic
order-4 subgroup $\langle J\rangle = \{I, J, -I, -J\}\cong \mathbb{Z}_4$. Iterating $J$ distinguishes a
quarter-turn from a sign flip; it does not trace the continuous circle or distinguish continuous from discrete
dynamics (as formalized in `lean4/quantum_mechanics/U1TorsionExclusion.lean`). The algebra $\{aI+bJ\}$ multiplies
as $\mathbb{C}$ (and $\mathbb{Z}[i]$ over the integers), $(aI+bJ)(cI+dJ)=(ac-bd)I+(ad+bc)J$.

However, finding $\mathbb{R}[J]\cong\mathbb{C}$ inside $M_2(\mathbb{R})$ does not select a complex operational theory:
the real plane also admits the real reflection $Z=\operatorname{diag}(1,-1)$ with $ZJ=-JZ$. Permitted real operations
fail to be complex-linear unless the compatibility condition $TJ=JT$ is explicitly required. Furthermore, a real
two-dimensional plane equipped with $J$ corresponds to one complex dimension, not a complex two-level qubit.
[WORKED EXAMPLE — `J_sq`, `S_sq`, `cx_mul`, `U1TorsionExclusion`.]

Falsifiability

Falsified if: a symmetric/bilinear (real) modulus admitted a nontrivial phase-invariant cross-term
(it cannot — T-FORCE-★); a real-signed fiber hosted an order-$>2$ rotation, or a quaternionic phase
commuted (they cannot — T-FORCE-ℂ); or the $2\times2$ rotation generator failed $J^2=-I$ or the
$\{aI+bJ\}$ product departed from complex multiplication (it cannot — `U1Selector`). The **conditional**
is weakened — not refuted — if continuous reversible 2-level transport could be had **without** a
complex structure, or if real QM were shown empirically indistinguishable from complex QM across all
networks (contra Renou et al. 2021).

What this paper does NOT claim

[SCOPE FENCE]

* **Not "ℂ derived from nothing."** The complex *structure* $J^2=-I$ is forced *given* continuous
  reversible pairing-preserving transport; continuity and the global field-uniqueness are imported.

* **Not continuous $U(1)$ from $J^2=-I$ alone:** $J^4=I$ generates the cyclic group $\mathbb{Z}_4$; it distinguishes
  a quarter-turn from a sign flip, but does not select continuous dynamics or a continuum circle without external continuity.

* **A complex subalgebra does not select complex operational theory:** $M_2(\mathbb{R})$ contains $Z=\operatorname{diag}(1,-1)$ with $ZJ=-JZ$;
  operations must separately satisfy the intertwining / compatibility equation $TJ=JT$.

* **Not a field selection:** The sesquilinear pairing result on $\mathbb{Q}(i)$ selects the conjugation involution within an already declared field; it does not select the coefficient field itself.

* **Not a full lattice-minimality theorem.** Layer 2 excludes $\mathbb{R}$-signed and $\mathbb{H}$ among
  the Frobenius trio and admits $\mathbb{C}$; it does **not** prove "no other $\ast$-field works," and
  quaternions contain abelian circle subgroups as well.

* **Not a reconstruction of QM.** The mechanized content is over $\mathbb{Z}[i]$ (integer form of ℂ);
  the field extension to $\mathbb{R}/\mathbb{C}$ and continuous $U(1)$ are standard.

* **Mints no authority:** $\mathsf{StructureDerived}\not\Rightarrow\mathsf{IsAuth}$.

Mechanization

`ForceComplexCarrier` (Mathlib-free; conjugation forced, Frobenius exclusions, the honest FCAI
gap) and `U1Selector` (Mathlib-light over $\mathbb{Z}$: `J_sq` $J^2=-I$, `S_sq` $S^2=+I$,
`continuous_vs_discrete`, `cx_mul`/`cx_add`/`cx_one` the $\mathbb{C}$-product, `cx_realizes_gaussian` +
`cx_injective` the $\mathbb{Z}[i]\hookrightarrow M_2(\mathbb{Z})$ ring embedding) — axioms ⊆
`{propext, Quot.sound}` (several axiom-free). Secured as **ENC-1136**. The evidence ledger records checked replays for the stable targets `QM.ForceComplexCarrier` and `QM.U1Selector`, bound to toolchain `leanprover/lean4:v4.31.0-rc1` and commit `fd009949156901e6cf15b6d9bf1122294b8e697a`. The receipt reports axioms within `{propext, Quot.sound}`. Exact commands and source locations remain in the evidence ledger.

Claim status

| status | claims |
|---|---|
| **PROVEN / MECHANIZED** | T-FORCE-★ conjugation forced; ℝ-signed & ℍ excluded within the declared Frobenius comparison class; $J^2=-I$ vs $S^2=+I$; $\{aI+bJ\}$ = complex product; $\mathbb{Z}[i]\hookrightarrow M_2(\mathbb{Z})$ ring embedding |
| **STANDARD / INTERPRETIVE** | the conditional-forcing synthesis (L1∧L2∧L3 ⇒ ℂ/U(1) at the 2-level core); $SO(2)=U(1)$ as the unit circle of the J-algebra |
| **IMPORTED** | continuity of reversible dynamics (the one-parameter flow); global field-uniqueness across $n$ (local tomography; Renou et al. 2021) |
| **NOT CLAIMED** | ℂ derived from nothing; lattice-minimality among all $\ast$-fields; $\mathbb{Q}/\mathbb{Z}$ torsion gap (the abstract phase-group shadow alone cannot uniquely select $U(1)$); any grant of authority |

References

* `ForceComplexCarrier`, `U1Selector` (this corpus). QM_121 (OB-U1), QM_061 (signedness),
  QM_110 (only-signedness-forced), QM_101 (pairing-relativity), pub-010 (the Born-uniqueness firewall
  this fence mirrors).

* L. Hardy, *Quantum theory from five reasonable axioms* (2001), arXiv:quant-ph/0101012.
* Ll. Masanes, M. P. Müller, *A derivation of quantum theory from physical requirements*, New J. Phys.
  **13** (2011) 063001.

* M.-O. Renou et al., *Quantum theory based on real numbers can be experimentally falsified*, Nature
  **600** (2021) 625–629. *(empirical ℂ-vs-ℝ selector.)*

* E. C. G. Stueckelberg, real-Hilbert-space QM and the universal $J$ (the complex structure of real QM
  dynamics).

Changelog

Version Note: v1.0 (2026-06-19)** — Initial. Assembles the ℂ/U(1) selector in three mechanized layers
  (conjugation forced; Frobenius exclusions; the new two-level complex-structure layer `U1Selector`),
  states the honest conditional forcing, and names the residual imports (continuity; global
  field-uniqueness). Sharpens OB-U1 of QM_121 from open to conditional. No "ℂ from nothing"; mints no
  authority.

<!-- claim-id-body-index:begin -->

Claim-ID body index (packaging)

| ID | Home |
|---|---|
| `QM-062-C1` | sibling `qm_062_the_u1_selector_claim_ledger.md` |
| `QM-062-C2` | sibling `qm_062_the_u1_selector_claim_ledger.md` |
| `QM-062-C3` | sibling `qm_062_the_u1_selector_claim_ledger.md` |
| `QM-062-C4` | sibling `qm_062_the_u1_selector_claim_ledger.md` |
| `QM-062-C5` | sibling `qm_062_the_u1_selector_claim_ledger.md` |
| `QM-062-C6` | sibling `qm_062_the_u1_selector_claim_ledger.md` |
| `QM-062-C7` | sibling `qm_062_the_u1_selector_claim_ledger.md` |
| `QM-062-C8` | sibling `qm_062_the_u1_selector_claim_ledger.md` |
| `QM-062-C9` | sibling `qm_062_the_u1_selector_claim_ledger.md` |
| `QM-062-C10` | sibling `qm_062_the_u1_selector_claim_ledger.md` |
| `QM-062-C11` | sibling `qm_062_the_u1_selector_claim_ledger.md` |
| `QM-U1SELECTOR-046` | sibling `qm_062_the_u1_selector_claim_ledger.md` |

<!-- claim-id-body-index:end -->
