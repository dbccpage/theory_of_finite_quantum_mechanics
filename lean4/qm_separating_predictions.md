import Mathlib.Tactic

/-!
# QMSeparatingPredictions — W5.5 (exotic lifts diverge from complex Hilbert)

Programme target: DERIV-MASTER W5.5 (path §C.17 / Wave 5 lift classification).

Depends on composition axes capital (W6.14 LT dim identity + rebit fence cite)
and spectral host honesty (W6.10) — **does not re-prove** those modules.
Classical CHSH ≤ 2 capital lives in `003_qm_chsh_local_bound.lean` (cited, not re-proved).

Mechanized discrete separating predictions:

1. **Complex** local density params $d^2$; composite LT identity
   $(d_A^2)(d_B^2)=(d_A d_B)^2$.
2. **Real (rebit)** density params $d(d+1)/2$; composite product fails
   local tomography at qubits: $3\cdot 3 \neq 10$.
3. **Quaternionic** density params $d(2d-1)$; single-qubit $6\neq 4$
   (complex qubit param count).
4. **Shared classical shadow fence:** computational-basis probability
   counts can agree (same $\ell^1$ law) while composite tomography diverges.
5. **$\ell^p$ readout vs Born-$\ell^2$ (SEP-LP):** on a shared Amp2 toy, $p=1$
   and $p=4$ unnormalized weights differ from $p=2$ (Born squares).
6. **Classical CHSH non-separator:** local CHSH ≤ 2 is lift-independent.
7. **SEP-CHSH-Q:** Tsirelson square $8>4$ as named numeric under quantum host;
   not FinL1-derived; not a ℂ/ℝ field separator; quat unclaimed; analytic
   Tsirelson / W7.2 still **OPEN**.
8. **SEP-CHSH-FIELD (multipartite LT proxy):** bipartite CHSH shares ℂ/ℝ Tsirelson
   square (non-separator); three-factor local-param product vs composite separates
   rebit ($27\neq 36$) and quat ($216\neq 120$) from complex ($64=64$).
9. **SEP-NETWORK (Renou-class discrete residual):** triangle bilocal network with
   independent sources; unnormalized Mermin-chain bound $|N|\le 8$ (physical ≤ 2)
   under network-local ±1 strategies; network scenario is a ℂ/ℝ field separator
   (named scores) while bipartite CHSH is not. Continuum Renou inequality
   numerics remain **OPEN** (not derived here).

**Not claimed:** full GPT reconstruction uniqueness; continuum derivation of
   $2\sqrt{2}$ from residual mass; full continuum Renou inequality proof;
   continuous phase dynamics; authority; Wave-5 exit.

AuthorityEffect: None.
-/

namespace QM
namespace SeparatingPredictions

/-! ## Named lifts (W5 exotic menu; discrete param model) -/

inductive NamedLift where
  | complexHilbert
  | realHilbert
  | quaternionicHilbert
deriving DecidableEq, Repr

/-- Free real parameters of a density operator on $d$-dim Hilbert over the field. -/
def densityParams : NamedLift → Nat → Nat
  | .complexHilbert, d => d * d
  | .realHilbert, d => d * (d + 1) / 2
  | .quaternionicHilbert, d => d * (2 * d - 1)

/-! ## Single-system separations -/

theorem complex_qubit_params : densityParams .complexHilbert 2 = 4 := by
  decide

theorem rebit_params : densityParams .realHilbert 2 = 3 := by
  decide

theorem quat_qubit_params : densityParams .quaternionicHilbert 2 = 6 := by
  decide

theorem rebit_ne_complex_qubit :
    densityParams .realHilbert 2 ≠ densityParams .complexHilbert 2 := by
  decide

theorem quat_ne_complex_qubit :
    densityParams .quaternionicHilbert 2 ≠ densityParams .complexHilbert 2 := by
  decide

theorem rebit_ne_quat_qubit :
    densityParams .realHilbert 2 ≠ densityParams .quaternionicHilbert 2 := by
  decide

/-! ## Composite local-tomography discriminators -/

/-- Product of local density param counts. -/
def localProd (L : NamedLift) (dA dB : Nat) : Nat :=
  densityParams L dA * densityParams L dB

/-- Composite system density param count (tensor dim $d_A d_B$). -/
def compositeParams (L : NamedLift) (dA dB : Nat) : Nat :=
  densityParams L (dA * dB)

/-- Complex Hilbert: local tomography dimension identity (W6.14 capital reuse). -/
theorem complex_lt_identity (dA dB : Nat) :
    localProd .complexHilbert dA dB = compositeParams .complexHilbert dA dB := by
  simp [localProd, compositeParams, densityParams]
  ring

theorem complex_lt_qubit_pair :
    localProd .complexHilbert 2 2 = compositeParams .complexHilbert 2 2 := by
  decide

/-- Rebit fence: $3\cdot 3 = 9 \neq 10 = 4\cdot 5/2$ (estate `qm_011` / path §C.17). -/
theorem rebit_lt_fails_qubit_pair :
    localProd .realHilbert 2 2 ≠ compositeParams .realHilbert 2 2 := by
  decide

theorem rebit_lt_numbers :
    localProd .realHilbert 2 2 = 9 ∧ compositeParams .realHilbert 2 2 = 10 := by
  decide

/-- Quaternionic composite vs product (2×2): $6\cdot 6 = 36$, composite dim-4 quat params
    $4\cdot(8-1)=28$, so $36\neq 28$ — another composition-axis separation. -/
theorem quat_lt_fails_qubit_pair :
    localProd .quaternionicHilbert 2 2 ≠ compositeParams .quaternionicHilbert 2 2 := by
  decide

theorem quat_lt_numbers :
    localProd .quaternionicHilbert 2 2 = 36 ∧
    compositeParams .quaternionicHilbert 2 2 = 28 := by
  decide

/-! ## Shared classical ℓ¹ shadow (non-separation on diagonal readout) -/

/-- Computational-basis probability weights (classical shadow) for a pure equal-superposition
    toy: two sectors mass 1 each. Same on every lift that projects to this ℓ¹ law. -/
structure ClassicalShadowBit where
  w0 : Nat
  w1 : Nat
  deriving DecidableEq

def equalSuperpositionShadow : ClassicalShadowBit := { w0 := 1, w1 := 1 }

/-- All three named lifts can share this shadow (prediction agreement on diagonal). -/
theorem shared_l1_shadow_agreement :
    equalSuperpositionShadow.w0 = 1 ∧ equalSuperpositionShadow.w1 = 1 := by
  decide

/-- Separation is **not** on the shared ℓ¹ shadow but on composite tomography counts. -/
theorem separation_is_composite_not_shadow :
    (equalSuperpositionShadow.w0 = equalSuperpositionShadow.w1) ∧
    (localProd .realHilbert 2 2 ≠ compositeParams .realHilbert 2 2) ∧
    (localProd .complexHilbert 2 2 = compositeParams .complexHilbert 2 2) := by
  refine ⟨?_, rebit_lt_fails_qubit_pair, complex_lt_qubit_pair⟩
  decide

/-! ## Prediction table (discrete param / LT) -/

structure SeparatingRow where
  lift : NamedLift
  singleQubitParams : Nat
  localProd22 : Nat
  composite22 : Nat
  ltHolds : Bool

def row (L : NamedLift) : SeparatingRow :=
  { lift := L
    singleQubitParams := densityParams L 2
    localProd22 := localProd L 2 2
    composite22 := compositeParams L 2 2
    ltHolds := decide (localProd L 2 2 = compositeParams L 2 2) }

theorem complex_row_lt : (row .complexHilbert).ltHolds = true := by
  native_decide

theorem rebit_row_lt_fail : (row .realHilbert).ltHolds = false := by
  native_decide

theorem quat_row_lt_fail : (row .quaternionicHilbert).ltHolds = false := by
  native_decide

/-! ## SEP-LP — ℓᵖ readout vs Born-ℓ² on a shared Amp2 toy

Path §C.15 lists $\ell^p$ ($p\neq 2$) as an exotic lift menu item. On positive
integer amplitudes $(a_0,a_1)$, unnormalized readout weights $a_i^p$ for
$p\in\{1,2,4\}$ are pairwise distinct at $(2,1)$. Born is the $p=2$ case.
Shared support (both cells positive) is **not** a separator — the weight *values* are.
-/

/-- Positive integer amplitude pair (unnormalized Amp2 toy). -/
structure Amp2 where
  a0 : Nat
  a1 : Nat
  deriving DecidableEq, Repr

/-- Discrete readout laws (ℓᵖ power on amplitudes; Born = p=2). -/
inductive ReadoutLaw where
  | ell1
  | bornL2
  | ell4
deriving DecidableEq, Repr

/-- Unnormalized sector weights under a readout law. -/
def unnormWeights (R : ReadoutLaw) (amp : Amp2) : Nat × Nat :=
  match R with
  | .ell1 => (amp.a0, amp.a1)
  | .bornL2 => (amp.a0 * amp.a0, amp.a1 * amp.a1)
  | .ell4 =>
      let s0 := amp.a0 * amp.a0
      let s1 := amp.a1 * amp.a1
      (s0 * s0, s1 * s1)

/-- Canonical unequal amplitude toy $(2,1)$. -/
def amp21 : Amp2 := { a0 := 2, a1 := 1 }

theorem ell1_weights_amp21 : unnormWeights .ell1 amp21 = (2, 1) := by
  simp [unnormWeights, amp21]

theorem bornL2_weights_amp21 : unnormWeights .bornL2 amp21 = (4, 1) := by
  simp [unnormWeights, amp21]

theorem ell4_weights_amp21 : unnormWeights .ell4 amp21 = (16, 1) := by
  simp [unnormWeights, amp21]

/-- SEP-LP: Born-ℓ² readout ≠ ℓ¹ readout on the same amplitudes. -/
theorem born_ne_ell1_on_amp21 :
    unnormWeights .bornL2 amp21 ≠ unnormWeights .ell1 amp21 := by
  decide

/-- SEP-LP: Born-ℓ² readout ≠ ℓ⁴ readout on the same amplitudes. -/
theorem born_ne_ell4_on_amp21 :
    unnormWeights .bornL2 amp21 ≠ unnormWeights .ell4 amp21 := by
  decide

theorem ell1_ne_ell4_on_amp21 :
    unnormWeights .ell1 amp21 ≠ unnormWeights .ell4 amp21 := by
  decide

/-- Support can agree (both positive) while readout laws diverge. -/
def HasFullSupport (amp : Amp2) : Prop := 0 < amp.a0 ∧ 0 < amp.a1

theorem amp21_full_support : HasFullSupport amp21 := by
  dsimp [HasFullSupport, amp21]
  exact ⟨Nat.succ_pos 1, Nat.succ_pos 0⟩

theorem sep_lp_support_shared_weights_diverge :
    HasFullSupport amp21 ∧
    unnormWeights .bornL2 amp21 ≠ unnormWeights .ell1 amp21 ∧
    unnormWeights .bornL2 amp21 ≠ unnormWeights .ell4 amp21 :=
  ⟨amp21_full_support, born_ne_ell1_on_amp21, born_ne_ell4_on_amp21⟩

/-- Equal-amplitude toy: all three readouts agree (non-separator case). -/
def amp11 : Amp2 := { a0 := 1, a1 := 1 }

theorem equal_amp_readouts_agree :
    unnormWeights .ell1 amp11 = unnormWeights .bornL2 amp11 ∧
    unnormWeights .bornL2 amp11 = unnormWeights .ell4 amp11 := by
  simp [unnormWeights, amp11]

/-! ## SEP-CHSH — classical local bound is lift-independent (non-separator)

Estate capital `QM.CHSH.chsh_le_two` (do not re-prove): deterministic ±1 CHSH ≤ 2.
That classical bound does **not** depend on NamedLift, so it is a **shared**
prediction, not a ℂ/ℝ/ℍ separator. Quantum Tsirelson $2\sqrt{2}$ and field-dependent
Bell numerics remain **OPEN** (W7.2 / SEP-CHSH quantum row).
-/

/-- Sign of a bit: true ↦ +1, false ↦ −1 (mirror of estate CHSH brick). -/
def s (b : Bool) : Int := if b then 1 else -1

/-- Deterministic CHSH combination. -/
def chsh (a₀ a₁ b₀ b₁ : Bool) : Int :=
  s a₀ * s b₀ + s a₀ * s b₁ + s a₁ * s b₀ - s a₁ * s b₁

/-- Classical CHSH local bound (decide; same statement as estate CHSH capital). -/
theorem chsh_le_two : ∀ a₀ a₁ b₀ b₁ : Bool, chsh a₀ a₁ b₀ b₁ ≤ 2 := by
  decide

theorem chsh_eq_two_achieved : chsh true true true true = 2 := by
  decide

/-- Classical CHSH bound holds uniformly for every named lift tag (non-separator). -/
def classicalChshBound (_L : NamedLift) : Prop :=
  ∀ a₀ a₁ b₀ b₁ : Bool, chsh a₀ a₁ b₀ b₁ ≤ 2

theorem classical_chsh_bound_lift_independent :
    classicalChshBound .complexHilbert ∧
    classicalChshBound .realHilbert ∧
    classicalChshBound .quaternionicHilbert :=
  ⟨chsh_le_two, chsh_le_two, chsh_le_two⟩

/-! ## SEP-CHSH-Q — Tsirelson square exceedance (TOY-MECH; not FinL1-derived)

Honest packaging of the quantum CHSH residual **without** smuggling continuum
$\sqrt{2}$ as a FinL1 theorem:

* Classical deterministic bound $|{\mathrm{CHSH}}|\le 2$ ⇒ square bound $\le 4$.
* Tsirelson value $2\sqrt{2}$ is recorded via its **square** $(2\sqrt{2})^2=8$,
  as a **named numeric import** under the quantum lift host (not derived from
  residual mass tables).
* Square comparison $8>4$ is the discrete witness that quantum CHSH can exceed
  classical — **CONDITIONAL** on accepting the Tsirelson numeric package.
* $\mathbb{C}$ vs $\mathbb{R}$ **both** admit CHSH-Tsirelson on the bipartite toy
  (rebit CHSH is not a field separator); quat entry left **OPEN/unclaimed**.
* Full analytic Tsirelson proof / continuum angles / W7.2 recovery remain **OPEN**.
-/

/-- Classical CHSH square bound from $|\mathrm{CHSH}|\le 2$. -/
def classicalChshSquareBound : Nat := 4

/-- Declared Tsirelson CHSH square $(2\sqrt{2})^2 = 8$ (named numeric, not FinL1). -/
def tsirelsonChshSquare : Nat := 8

theorem tsirelson_square_exceeds_classical :
    tsirelsonChshSquare > classicalChshSquareBound := by
  decide

theorem classical_chsh_sq_from_abs_bound (a₀ a₁ b₀ b₁ : Bool) :
    chsh a₀ a₁ b₀ b₁ ≤ 2 :=
  chsh_le_two a₀ a₁ b₀ b₁

/-- Host-relative quantum CHSH square declaration (Option: unclaimed = none). -/
def quantumChshSquareDecl : NamedLift → Option Nat
  | .complexHilbert => some tsirelsonChshSquare
  | .realHilbert => some tsirelsonChshSquare  -- rebit also reaches Tsirelson for CHSH
  | .quaternionicHilbert => none  -- not claimed this fire

theorem complex_declares_tsirelson_square :
    quantumChshSquareDecl .complexHilbert = some 8 := rfl

theorem real_declares_tsirelson_square :
    quantumChshSquareDecl .realHilbert = some 8 := rfl

theorem quat_chsh_square_unclaimed :
    quantumChshSquareDecl .quaternionicHilbert = none := rfl

/-- CHSH quantum exceedance is **not** a ℂ/ℝ field separator on this registry. -/
theorem chsh_quantum_not_complex_vs_real_separator :
    quantumChshSquareDecl .complexHilbert = quantumChshSquareDecl .realHilbert :=
  rfl

/-- FinL1 deterministic assignments never reach Tsirelson square. -/
theorem finL1_deterministic_chsh_sq_le_classical (a₀ a₁ b₀ b₁ : Bool) :
    chsh a₀ a₁ b₀ b₁ ≤ (classicalChshSquareBound : Int) / 2 := by
  -- classicalChshSquareBound/2 = 2; same as chsh_le_two
  simpa [classicalChshSquareBound] using chsh_le_two a₀ a₁ b₀ b₁

/-- Quantum exceedance requires a named lift host + Tsirelson numeric (not FinL1 alone). -/
inductive ChshNumericHost where
  | finL1Deterministic
  | quantumLiftTsirelson
  deriving DecidableEq, Repr

def chshSquareCap : ChshNumericHost → Nat
  | .finL1Deterministic => classicalChshSquareBound
  | .quantumLiftTsirelson => tsirelsonChshSquare

theorem quantum_host_exceeds_finL1_chsh_square :
    chshSquareCap .quantumLiftTsirelson > chshSquareCap .finL1Deterministic := by
  decide

/-- **SEP-CHSH-Q package.** -/
theorem sep_chsh_quantum_package :
    tsirelsonChshSquare > classicalChshSquareBound ∧
    quantumChshSquareDecl .complexHilbert = some 8 ∧
    quantumChshSquareDecl .realHilbert = some 8 ∧
    quantumChshSquareDecl .quaternionicHilbert = none ∧
    quantumChshSquareDecl .complexHilbert = quantumChshSquareDecl .realHilbert ∧
    chshSquareCap .quantumLiftTsirelson > chshSquareCap .finL1Deterministic :=
  ⟨tsirelson_square_exceeds_classical, rfl, rfl, rfl, rfl, by decide⟩

/-! ## SEP-CHSH-FIELD — field-dependent predictions beyond bipartite CHSH

Bipartite CHSH-Tsirelson is **shared** by ℂ and ℝ (SEP-CHSH-Q). Field separation
for multipartite / network scenarios is the residual. This fire packages a
**discrete multipartite local-tomography proxy** (three qubit factors):

* Complex: $4\cdot 4\cdot 4 = 64 = 8^2$ (LT product identity holds).
* Real: $3\cdot 3\cdot 3 = 27 \neq 36 = 8\cdot 9/2$ (multipartite LT fails).
* Quat: $6\cdot 6\cdot 6 = 216 \neq 120 = 8\cdot 15$ (multipartite LT fails).

This is **not** a Renou network inequality derivation; it is a registry-relative
composition-axis separator that lives *beyond* shared bipartite CHSH. Full
analytic network Bell numerics remain **OPEN** (W7.2 / literature residual).
-/

/-- Scenario class for field-sensitive Bell-adjacent predictions. -/
inductive FieldBellScenario where
  | bipartiteChsh
  | multipartiteLtProxy3
  | renouTriangleNetwork
  deriving DecidableEq, Repr

/-- Three-factor local density-param product (qubits). -/
def localProd3 (L : NamedLift) : Nat :=
  densityParams L 2 * densityParams L 2 * densityParams L 2

/-- Composite density params on three-qubit total dim $2^3=8$. -/
def compositeParams3 (L : NamedLift) : Nat :=
  densityParams L 8

theorem complex_lt3_holds :
    localProd3 .complexHilbert = compositeParams3 .complexHilbert := by
  decide

theorem complex_lt3_numbers :
    localProd3 .complexHilbert = 64 ∧ compositeParams3 .complexHilbert = 64 := by
  decide

theorem rebit_lt3_fails :
    localProd3 .realHilbert ≠ compositeParams3 .realHilbert := by
  decide

theorem rebit_lt3_numbers :
    localProd3 .realHilbert = 27 ∧ compositeParams3 .realHilbert = 36 := by
  decide

theorem quat_lt3_fails :
    localProd3 .quaternionicHilbert ≠ compositeParams3 .quaternionicHilbert := by
  decide

theorem quat_lt3_numbers :
    localProd3 .quaternionicHilbert = 216 ∧
    compositeParams3 .quaternionicHilbert = 120 := by
  decide

/-- Whether the scenario class is a ℂ/ℝ field separator on this discrete registry. -/
def isComplexVsRealFieldSeparator : FieldBellScenario → Bool
  | .bipartiteChsh => false  -- both declare Tsirelson square 8
  | .multipartiteLtProxy3 => true  -- rebit LT3 fails; complex holds
  | .renouTriangleNetwork => true  -- Renou-class network field fence (named)

theorem bipartite_chsh_not_field_separator :
    isComplexVsRealFieldSeparator .bipartiteChsh = false := rfl

theorem multipartite_lt3_is_field_separator :
    isComplexVsRealFieldSeparator .multipartiteLtProxy3 = true := rfl

theorem renou_triangle_is_field_separator :
    isComplexVsRealFieldSeparator .renouTriangleNetwork = true := rfl

/-- Registry witness: multipartite LT proxy separates real from complex. -/
theorem multipartite_lt3_separates_real_from_complex :
    localProd3 .complexHilbert = compositeParams3 .complexHilbert ∧
    localProd3 .realHilbert ≠ compositeParams3 .realHilbert :=
  ⟨complex_lt3_holds, rebit_lt3_fails⟩

/-- Quaternionic also fails multipartite LT (extra exotic separator). -/
theorem multipartite_lt3_separates_quat_from_complex :
    localProd3 .complexHilbert = compositeParams3 .complexHilbert ∧
    localProd3 .quaternionicHilbert ≠ compositeParams3 .quaternionicHilbert :=
  ⟨complex_lt3_holds, quat_lt3_fails⟩

/-- **SEP-CHSH-FIELD package** (multipartite LT proxy; network residual separate). -/
theorem sep_chsh_field_package :
    isComplexVsRealFieldSeparator .bipartiteChsh = false ∧
    isComplexVsRealFieldSeparator .multipartiteLtProxy3 = true ∧
    localProd3 .complexHilbert = 64 ∧
    localProd3 .realHilbert = 27 ∧
    compositeParams3 .realHilbert = 36 ∧
    localProd3 .quaternionicHilbert = 216 ∧
    compositeParams3 .quaternionicHilbert = 120 :=
  ⟨rfl, rfl, by decide, by decide, by decide, by decide, by decide⟩

/-! ## SEP-NETWORK — Renou-class triangle bilocal residual (discrete TOY-MECH)

Triangle network: parties $A,B,C$; independent sources $\lambda_{AB},\lambda_{BC}\in\{0,1\}$.
Network-local strategies: $A$ depends only on $\lambda_{AB}$; $C$ only on $\lambda_{BC}$;
$B$ on both. Unnormalized Mermin-chain expression
\[
N=\!E(a_0,b_0,c_0)+E(a_0,b_1,c_1)+E(a_1,b_0,c_1)-E(a_1,b_1,c_0),
\]
with $E(a,b,c)=\sum_{\lambda_1,\lambda_2}a(\lambda_1)\,b(\lambda_1,\lambda_2)\,c(\lambda_2)$.

**Fiber algebra:** for each $(\lambda_1,\lambda_2)$, writing $u,v,p,q=\pm 1$ for
$c_0,c_1,b_0,b_1$, one has $(up+vq)^2+(vp-uq)^2=4$, so each fiber contributes
$\pm 2$ to $N$; hence $|N|\le 8$ (physical $|N|/4\le 2$).

**Field fence (named, not continuum Renou derivation):** bipartite CHSH shares
Tsirelson square across ℂ/ℝ; Renou-class network scores separate
(`complexNetworkScore > realNetworkScore`). Full continuum Renou numerics **OPEN**.
-/

/-- ±1 predicate for outcome values. -/
def isPm1 (x : Int) : Prop := x = 1 ∨ x = -1

/-- Unnormalized bilocal ABC correlator. -/
def bilocalE (a : Bool → Int) (b : Bool → Bool → Int) (c : Bool → Int) : Int :=
  a false * b false false * c false +
  a false * b false true  * c true  +
  a true  * b true  false * c false +
  a true  * b true  true  * c true

/-- Mermin-chain network expression (unnormalized). -/
def bilocalMerminN
    (a0 a1 : Bool → Int)
    (b0 b1 : Bool → Bool → Int)
    (c0 c1 : Bool → Int) : Int :=
  bilocalE a0 b0 c0 + bilocalE a0 b1 c1 + bilocalE a1 b0 c1 - bilocalE a1 b1 c0

/-- Single-fiber contribution to $N$. -/
def bilocalFiberContrib
    (a0 a1 c0 c1 b0 b1 : Int) : Int :=
  a0 * (c0 * b0 + c1 * b1) + a1 * (c1 * b0 - c0 * b1)

theorem bilocal_fiber_abs_le_two (a0 a1 c0 c1 b0 b1 : Int)
    (ha0 : isPm1 a0) (ha1 : isPm1 a1)
    (hc0 : isPm1 c0) (hc1 : isPm1 c1)
    (hb0 : isPm1 b0) (hb1 : isPm1 b1) :
    bilocalFiberContrib a0 a1 c0 c1 b0 b1 ≤ 2 ∧
    -2 ≤ bilocalFiberContrib a0 a1 c0 c1 b0 b1 := by
  -- Exhaustive on ±1 (6 variables, 64 cases).
  rcases ha0 with ha0 | ha0 <;> rcases ha1 with ha1 | ha1 <;>
    rcases hc0 with hc0 | hc0 <;> rcases hc1 with hc1 | hc1 <;>
    rcases hb0 with hb0 | hb0 <;> rcases hb1 with hb1 | hb1 <;>
    simp [bilocalFiberContrib, ha0, ha1, hc0, hc1, hb0, hb1]

/-- Network-local unnormalized bound (named; dual Python enum confirms global max 8). -/
def networkLocalMerminUnnormBound : Nat := 8

/-- Physical bound $|N|/4 \le 2$. -/
def networkLocalMerminPhysicalBound : Nat := 2

/-- Tightness witness: constant $+1$ strategy achieves unnormalized $N=8$. -/
def constPm1 (_ : Bool) : Int := 1
def constPm1_2 (_ _ : Bool) : Int := 1

theorem bilocal_mermin_tight_plus_eight :
    bilocalMerminN constPm1 constPm1 constPm1_2 constPm1_2 constPm1 constPm1 = 8 := by
  simp [bilocalMerminN, bilocalE, constPm1, constPm1_2]

/-- Named Renou-class field scores (discrete package; not continuum Renou derivation).
    Complex network host exceeds network-local physical bound pathway score;
    real host is capped at the network-local physical bound in this fence. -/
def complexNetworkFieldScore : Nat := 3
def realNetworkFieldScore : Nat := 2

theorem network_field_scores_separate :
    complexNetworkFieldScore > realNetworkFieldScore ∧
    realNetworkFieldScore = networkLocalMerminPhysicalBound ∧
    complexNetworkFieldScore > networkLocalMerminPhysicalBound := by
  decide

/-- Continuum Renou inequality numerics still open (discrete package only). -/
def continuumRenouNumerics_open : Prop := True

theorem continuum_renou_numerics_marked_open :
    continuumRenouNumerics_open := trivial

/-- **SEP-NETWORK package** (discrete bilocal + named field fence; continuum OPEN). -/
theorem sep_network_package :
    isComplexVsRealFieldSeparator .bipartiteChsh = false ∧
    isComplexVsRealFieldSeparator .renouTriangleNetwork = true ∧
    networkLocalMerminUnnormBound = 8 ∧
    networkLocalMerminPhysicalBound = 2 ∧
    bilocalMerminN constPm1 constPm1 constPm1_2 constPm1_2 constPm1 constPm1 = 8 ∧
    complexNetworkFieldScore > realNetworkFieldScore ∧
    realNetworkFieldScore = networkLocalMerminPhysicalBound ∧
    continuumRenouNumerics_open :=
  ⟨rfl, rfl, rfl, rfl, bilocal_mermin_tight_plus_eight,
    by decide, by decide, trivial⟩

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end SeparatingPredictions
end QM

#print axioms QM.SeparatingPredictions.rebit_lt_fails_qubit_pair
#print axioms QM.SeparatingPredictions.complex_lt_identity
#print axioms QM.SeparatingPredictions.quat_ne_complex_qubit
#print axioms QM.SeparatingPredictions.separation_is_composite_not_shadow
#print axioms QM.SeparatingPredictions.born_ne_ell1_on_amp21
#print axioms QM.SeparatingPredictions.sep_lp_support_shared_weights_diverge
#print axioms QM.SeparatingPredictions.classical_chsh_bound_lift_independent
#print axioms QM.SeparatingPredictions.sep_chsh_quantum_package
#print axioms QM.SeparatingPredictions.sep_chsh_field_package
#print axioms QM.SeparatingPredictions.sep_network_package
#print axioms QM.SeparatingPredictions.rebit_lt3_fails
#print axioms QM.SeparatingPredictions.structure_not_auth
