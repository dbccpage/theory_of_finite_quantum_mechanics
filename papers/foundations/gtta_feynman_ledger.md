Claim Ledger — Paper QM_032: CODA-A-Feynman-1 — Infinity Path Category from Finite-Shadow Histories
=================================================================================================

**Paper Key:** `003_quantum_foundations/032_gtta_feynman_finite_shadow_histories`  

Date: 2026-06-17
Version: v0.1.0 Pre-Print
Series: qm / QM Atlas
Companions: QM_110 (Finite Weighted Transport Calculus — QM_032 backs T1 / the finite path-sum),
QM_111 (Finite Path-Sum as Graded Transport — the finite path-sum = matrix-power identity,
ENC-1128), QM_090 (Continuum Shadow Non-Promotion — the CODA-CS firewall, ENC-1078), QM_032 (Finite
Descent to CODA-FOC Projection), QM_081 (formal-vs-physical QM split, finite descent), QM_Series_Falsifiability_Ledger
(falsifiability ledger).

Firewall note: QM is a realization spine. QM_032 mints **no** tower authority. It is the
**path-integral instance** of the GTLA continuum firewall: the Feynman path integral is
reconstructed only as the limit of **finite, replayable** sum-over-histories shadows, and the
continuum kernel is **imported** under a declared topology + convergence certificate, never derived
from the finite shadows alone. The controlling discipline is the authority firewall
$\mathsf{StructureDerived}(F,c)\not\Rightarrow\mathsf{IsAuth}(t)$ (ENC-1063) together with the CODA-CS
non-promotion theorem (ENC-1078): a finite-shadow family does not construct a continuum kernel
without a `ConvergenceCertificate`; absent it the output is `OracleNeeded(Convergence)`.

Three honest fences (load-bearing — must not be weakened):

1. **The continuum path integral / $\exp(tH)$ is a smuggle to refuse.** The continuum kernel
   $K=\lim_\lambda K_\lambda$, a measure on path space, and any generator/flow built from it are
   **continuum** objects. They are not constructed here. They are authorized only by a declared
   topology + convergence certificate (`OracleNeeded(Convergence)` absent it). MECHANIZED as the
   non-promotion direction of ENC-1078 (CONTINUUM-001 / LT-S).

2. **"Finite shadow ⇒ continuum integral" is NOT a claim.** The finite shadow $K_\lambda$ is
   certified; the continuum limit is a *non-forced lift*. The implication finite$\Rightarrow$continuum
   is explicitly refused without the certificate; the *absence* of a continuum limit is the typed
   `OracleNeeded` terminal, not an error or a refutation.

3. **No authority minted; the continuum object is imported, not derived.** Per the firewall
   $\mathsf{StructureDerived}\not\Rightarrow\mathsf{IsAuth}$ (ENC-1063), no part of this construction
   mints tower authority; when authorized, the continuum object is imported under its certificate.

Securing note: QM_032's load-bearing finite content (finite history enumeration $\Rightarrow$
replayable finite propagator $K_\lambda$) is already secured + MECHANIZED as **ENC-1072**
(*Finite Graded Path-Sum and Feynman Shadow Replay*, PATHSUM-001 / FEYNMAN-001 / LT-N / LT-R;
quantum layer, alias `paper:qm092`, Lean [index:index:FiniteFeynmanShadow.lean](omega_engine/research/_indexes/_master_index.yaml) +
`FinitePathSumReplay.lean`); the finite path-sum = transfer-matrix entry is **ENC-1128**
(PATHSUM-MXP-001, QM_111); the continuum non-promotion fence is **ENC-1078** (CONTINUUM-001 / LT-S,
whose Notes explicitly name "Papers that rely on it: **12**, 27, 29"); and the authority firewall is
**ENC-1063**. Per the QM-series sign-off precedent (QM_081/QM_100/QM_081/QM_006/QM_001/QM_101/QM_110 —
QM is a realization spine that mints no authority), QM_032 secures under the shared `paper:qm092`
namespace; the proof-signoff stage adjudicates whether any genuinely new theorem original to QM_032
requires a per-paper view (none is expected — the finite content is ENC-1072, the fence is ENC-1078).

Claim index
-----------

| ID | Claim (abbreviated) | Status | Location |
|---|---|---|---|
| QM-032-C1 | Lead result: a Feynman path integral is reconstructed only as the limit of **finite, replayable** sum-over-histories shadows; the continuum kernel is authorized only under a declared topology + convergence certificate, otherwise a typed residual | [SCOPE FENCE + PROVEN, CONDITIONAL — finite shadow MECHANIZED ENC-1072; continuum import gated ENC-1078] | Lead / Status Packet |
| QM-032-C2 | Status Packet "Not claiming" block (QED / Standard Model / physics-from-CODA-CS / continuum authority without finite shadows) is the load-bearing fence | [SCOPE FENCE] | Status Packet |
| QM-032-C3 | CODA-A-Feynman-1 **(i)**: given finite partition λ, finite carrier $X_\lambda$, endpoints, declared discrete Lagrangian $L_\lambda$, normalization $Z_\lambda$, numeric policy, the finite shadow propagator $K_\lambda$ is replayable by finite enumeration | [PROVEN — finite, elementary; MECHANIZED ENC-1072 (FEYNMAN-001 / LT-R)] | Theorem (i); Proof Part 1 |
| QM-032-C4 | CODA-A-Feynman-1 **(ii)**: if $\{K_\lambda\}$ is compatible under declared refinement maps $\chi_{\lambda\lambda'}$ and converges under declared topology Τ, the limit $K$ is authorized as a CODA-CS finite-shadow continuum object — **imported** under the certificate, not constructed; absent it, `OracleNeeded(Convergence)` | [PROVEN, CONDITIONAL + convergence oracle — non-promotion direction MECHANIZED ENC-1078 (CONTINUUM-001 / LT-S)] | Theorem (ii); Proof Parts 2–3 |
| QM-032-C5 | CODA-A-Feynman-1 **(iii)**: CODA-A closure $\Lambda_F$ disposes of the residual as `ClosureAbsorbed`/`Certificate(K)` or a typed residual — the *output rule* of the terminalizer, not a separately proven theorem | [DEFINITION / OPERATIONAL RULE] | Theorem (iii); Proof Part 4 |
| QM-032-C6 | CODA-CS finite-shadow evidence rule: a continuum claim enters this bounded check only through declared finite shadows and refinement compatibility; shadows are required evidence carriers, not an authority substrate | [SCOPE FENCE — firewall; MECHANIZED ENC-1078, ENC-1063] | CODA-CS finite-shadow rule |
| QM-032-C7 | The **infinity path category** $\mathrm{Path}_\infty^L(a,b)$ is **not primitive**: it exists only when the refinement system, coarse-graining functors $\rho_{\lambda\lambda'}$, cofinality certificate, and limit construction are declared; otherwise CODA-A returns the finite shadow ledger $\mathrm{NAbs}(\mathrm{Path}_\infty^L)$ with status `BudgetUnknown` until cofinality is proven | [DEFINITION / SCOPE FENCE — declared limit, never a primitive] | Infinity Path Category |
| QM-032-C8 | Finite history set $\mathrm{Hist}_\lambda(a,b)=\{\gamma\in X_\lambda^{n+1}:\gamma_0=a,\gamma_n=b\}$ is finite, so every sum is replayable by enumeration; finite-shadow action $S_\lambda(\gamma)=\sum_k L_\lambda\,\Delta t_k$, phase $A_\lambda=\exp(iS_\lambda/\hbar)$, propagator $K_\lambda=Z_\lambda^{-1}\sum_\gamma A_\lambda$ | [DEFINITION] | Finite Time-Sliced System; Declared Discrete Action |
| QM-032-C9 | Replayable Packet `gttc<…>` + the 9-step host-validator replay (endpoints, carrier membership, slice validity, Lagrangian eval, action eval, phase eval, history enumeration once-each, normalization, kernel assembly) — $K_\lambda$ certified by finite replay, not explanation | [DEFINITION / OPERATIONAL RULE] | Replayable Packet |
| QM-032-C10 | Worked example (hand-replayable): two-slice free particle, $m=\hbar=Z_\lambda=1$, $a=b=0$, midpoint carrier $\{-1,0,1\}$ ⇒ three histories, $K_\lambda(0,0)=1+2e^{i}=(1+2\cos1)+2i\sin1\approx 2.0806+1.6829\,i$, replayed over a 3-element set with no continuum/measure/limit | [WORKED EXAMPLE — exact finite enumeration] | Free Particle Target / Worked example |
| QM-032-C11 | Free-particle discrete Lagrangian $L_\lambda=(m/2)((x_{k+1}-x_k)/\Delta t_k)^2$ is the first concrete CODA-A-Feynman bridge; all finite-shadow ingredients are locally replayable | [DEFINITION + WORKED EXAMPLE — declared discretization, not derived from the continuum] | Free Particle Target |
| QM-032-C12 | Terminalization tables (`Certificate(K_lambda)` / `Repair` / `Refusal` / `OracleNeeded` / `Certificate(K)` / `OpenResidual(RefinementTear)` / `BudgetUnknown` / `RefusedClosure`) | [DEFINITION / OPERATIONAL RULE] | CODA-A Wrapper; Terminalization |
| QM-032-C13 | Falsifiability: fails if (1) a finite shadow cannot be replayed over the declared finite carrier, (2) a refined shadow does not coarse-grain to the declared coarse kernel (`RefinementTear`), or (3) someone constructs a continuum path-integral object from a finite-shadow family **without** a declared topology + convergence certificate (refuting ENC-1078); **not** falsified by the absence of a continuum limit (that is the typed `OracleNeeded` terminal) | [FALSIFIABILITY] | Falsifiability |
| QM-032-C14 | Non-claim box: does **not** prove QED, the Standard Model, physical correctness of a chosen Lagrangian, existence of every continuum path integral, continuum authority without finite shadows, convergence without a declared topology, or compatibility without declared refinement maps; **"finite shadow ⇒ continuum" is not claimed**; no authority minted ($\mathsf{StructureDerived}\not\Rightarrow\mathsf{IsAuth}$, ENC-1063) | [SCOPE FENCE — authority firewall] | What This Does Not Prove |
| QM-032-C15 | Implementation Sketch (Rust type signatures): `FeynmanShadowPacket`, `FinitePropagator`, `InfinityPathCategory`, `FeynmanResidual`, validator outline — type signatures only, not a proof dependency | [DEFINITION / OPERATIONAL RULE — illustrative, not load-bearing] | Implementation Sketch |

Support ledger (Part C — upgrade engine)
----------------------------------------

Each entry records what would strengthen a conditional/open/refused claim. **None gates current
honesty**: every target claim is correctly typed conditional / scope-fenced / open / refused in the
paper, the load-bearing finite content is MECHANIZED (ENC-1072), and the continuum fence is
MECHANIZED (ENC-1078). Global proof-ledger IDs are in `proof_ledger_20260617.md`.

1. **PL-QM012-1 — Derive (or refute) convergence of the free-particle finite-shadow family.** For
   the §"Free Particle Target" discretization, exhibit a declared refinement system + topology + a
   `ConvergenceCertificate` under which $\{K_\lambda\}$ converges to the standard free-particle
   propagator (the Gaussian kernel), or prove that no such certificate exists for the declared
   finite-carrier scheme. *Strengthens:* C4/C11 — would discharge the `OracleNeeded(Convergence)`
   obligation for the first concrete model and turn the continuum import into a checked instance.
   *Type:* `Prose` / `Numerical` (analytic convergence + a finite mesh-refinement study).
   *Difficulty:* Medium-Hard — the continuum measure question the paper deliberately imports.
   **Not honesty-gating** — the paper refuses the continuum object absent the certificate.

2. **PL-QM012-2 — Declared coarse-graining functor + cofinality certificate for the infinity path
   category.** Declare the refinement category $\mathrm{Part}(T)$ coarse-graining functors
   $\rho_{\lambda\lambda'}$ and a cofinality certificate that proves the finite-shadow family is
   cofinal/exhaustive, so $\mathrm{Path}_\infty^L(a,b)$ exists as a declared limit rather than the
   `BudgetUnknown` shadow ledger $\mathrm{NAbs}(\mathrm{Path}_\infty^L)$. *Strengthens:* C7 — lifts
   the infinity path category from `BudgetUnknown` to a certified limit for the declared system.
   *Type:* `Prose` / `Mechanical` (cofinality proof + a replayable refinement family).
   *Difficulty:* Medium — depends on the chosen carrier/refinement scheme. **Not honesty-gating** —
   the category is correctly typed a declared (non-primitive) limit, replaced by the shadow ledger
   absent its data.

3. **PL-QM012-3 — Vendor an in-tree replayable finite-shadow path-sum validator + golden fixtures.**
   *(reproducibility — NOT honesty-gating.)* Implement and vendor an in-tree replayable validator
   that takes the §"Replayable Packet" `gttc<…>` packet and re-runs the 9-step replay (the worked
   two-slice free-particle example as a golden fixture: $K_\lambda(0,0)=1+2e^{i}$), emitting
   `Certificate(K_lambda)` or the typed residual, then re-run on the published copy. *Strengthens:*
   C3/C9/C10 — turns the prose replay protocol + worked example into in-tree replayable
   certificates. *Type:* `Mechanical` (validator) / `Numerical` (re-run). *Difficulty:* Low —
   engineering over a finite enumeration; the load-bearing finite content is already Lean-checked
   (ENC-1072) and the worked numbers are hand-verifiable. Mirrors the QM_081/QM_006/QM_001/QM_110
   vendoring targets. **Not honesty-gating.**
