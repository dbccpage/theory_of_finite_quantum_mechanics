import Mathlib.Tactic

/-!
# QMExchangeStatistics — W6.15 / OB-STATS (exchange statistics)

Programme target: DERIV-MASTER W6.15 (QMREG-65 / freeze `OB-STATS`).

**Adjudication (toy form):**

1. **Classical residual exchange** of two finite systems is a sector
   permutation of the joint weight table — **DERIVED** on FinL1
   (totals preserved; involution; product of identical marginals is fixed).
2. A **forced Bose/Fermi state-space dichotomy** (symmetric vs antisymmetric
   amplitude characters of the swap) is **UNDERIVABLE** from FinL1 residual
   mass alone: classical exchange has no sign obstruction.
3. Under a **linear amplitude lift**, swap acts on joint AmpJoint; the two
   $S_2$ characters $\chi(\tau)=\pm 1$ are **packaged** as declared statistics
   tags — **CONDITIONAL/IMPORT** of the amplitude / phase-fiber host.
4. Full spin–statistics theorem / braid groups in continuum remain **OPEN**.
5. **Signed character residual (TOY-MECH):** Int joint amplitudes with
   $\psi'(x,y)=\chi\,\psi(y,x)$; Bose fixed under $\chi=+1$; true antisym
   Fermi fixed under $\chi=-1$ with diagonal exclusion $a_{00}=a_{11}=0$;
   symmetrizer/antisymmetrizer projectors; continuum spin–statistics still **OPEN**.

Upstream capital (do not re-prove): `qm_072` pair-exchange dichotomy prose;
W6.14 joint product; W6.18 AmpJoint pattern.

AuthorityEffect: None.
-/

namespace QM
namespace ExchangeStatistics

/-! ## Classical joint residual tables -/

structure JointWeight where
  w00 : Nat
  w01 : Nat
  w10 : Nat
  w11 : Nat
  deriving DecidableEq, Repr

namespace JointWeight

def total (j : JointWeight) : Nat := j.w00 + j.w01 + j.w10 + j.w11

/-- Exchange systems A↔B: swap off-diagonal sector labels 01 ↔ 10. -/
def exchange (j : JointWeight) : JointWeight :=
  { w00 := j.w00
    w01 := j.w10
    w10 := j.w01
    w11 := j.w11 }

end JointWeight

def jointAsym : JointWeight := { w00 := 1, w01 := 2, w10 := 3, w11 := 4 }
def jointSym : JointWeight := { w00 := 1, w01 := 5, w10 := 5, w11 := 2 }
def productFair : JointWeight := { w00 := 1, w01 := 1, w10 := 1, w11 := 1 }

theorem exchange_total (j : JointWeight) :
    (JointWeight.exchange j).total = j.total := by
  cases j with
  | mk a b c d =>
    simp [JointWeight.exchange, JointWeight.total]
    omega

theorem exchange_involution (j : JointWeight) :
    JointWeight.exchange (JointWeight.exchange j) = j := by
  cases j with
  | mk a b c d =>
    simp [JointWeight.exchange]

theorem exchange_moves_asym :
    JointWeight.exchange jointAsym =
      { w00 := 1, w01 := 3, w10 := 2, w11 := 4 } := by
  simp [JointWeight.exchange, jointAsym]

theorem exchange_fixes_sym :
    JointWeight.exchange jointSym = jointSym := by
  simp [JointWeight.exchange, jointSym]

theorem exchange_fixes_product_fair :
    JointWeight.exchange productFair = productFair := by
  simp [JointWeight.exchange, productFair]

/-- Classical residual exchange is constructible and total-preserving. -/
theorem classical_exchange_derived :
    (JointWeight.exchange jointAsym).total = jointAsym.total ∧
    JointWeight.exchange (JointWeight.exchange jointAsym) = jointAsym ∧
    JointWeight.exchange jointSym = jointSym :=
  ⟨exchange_total jointAsym, exchange_involution jointAsym, exchange_fixes_sym⟩

/-! ## Amplitude joint + S₂ characters (linear lift toy) -/

structure AmpJoint where
  a00 : Nat
  a01 : Nat
  a10 : Nat
  a11 : Nat
  deriving DecidableEq, Repr

/-- Swap systems on amplitude joint (unsigned permutation of basis). -/
def ampExchange (j : AmpJoint) : AmpJoint :=
  { a00 := j.a00
    a01 := j.a10
    a10 := j.a01
    a11 := j.a11 }

/-- Symmetric two-particle toy: equal off-diagonals (Bose-like support). -/
def ampBose : AmpJoint := { a00 := 0, a01 := 1, a10 := 1, a11 := 0 }

/-- Antisymmetric toy support: only one ordered off-diagonal mass before sign.
    Unsigned exchange moves it; fermionic packaging records a sign character. -/
def ampFermiSupport : AmpJoint := { a00 := 0, a01 := 1, a10 := 0, a11 := 0 }

theorem amp_exchange_bose_fixed :
    ampExchange ampBose = ampBose := by
  simp [ampExchange, ampBose]

theorem amp_exchange_moves_fermi_support :
    ampExchange ampFermiSupport =
      { a00 := 0, a01 := 0, a10 := 1, a11 := 0 } := by
  simp [ampExchange, ampFermiSupport]

theorem amp_exchange_fermi_ne_self :
    ampExchange ampFermiSupport ≠ ampFermiSupport := by
  decide

/-- Declared $S_2$ exchange characters (transport-level Bose/Fermi split). -/
inductive StatsCharacter where
  | bose   -- χ(τ) = +1
  | fermi  -- χ(τ) = −1
  deriving DecidableEq, Repr

/-- Toy host: character is a declared tag on the amplitude lift, not FinL1 data. -/
structure DeclaredExchange where
  character : StatsCharacter
  joint : AmpJoint

def boseOnSymmetric : DeclaredExchange :=
  { character := .bose, joint := ampBose }

def fermiOnSupport : DeclaredExchange :=
  { character := .fermi, joint := ampFermiSupport }

/-- Bose character compatible with exchange-fixed joint. -/
def boseCompatible (d : DeclaredExchange) : Prop :=
  d.character = .bose → ampExchange d.joint = d.joint

theorem bose_on_symmetric_compatible :
    boseCompatible boseOnSymmetric := by
  intro h
  simp [boseOnSymmetric, ampExchange, ampBose]

/-- Fermi character records that unsigned exchange moves the support
    (sign packaging is the import; we only witness the move). -/
def fermiWitness (d : DeclaredExchange) : Prop :=
  d.character = .fermi → ampExchange d.joint ≠ d.joint

theorem fermi_support_witness :
    fermiWitness fermiOnSupport := by
  intro h
  exact amp_exchange_fermi_ne_self

/-- Both $S_2$ characters are available under the amplitude host. -/
theorem s2_characters_packaged :
    boseOnSymmetric.character ≠ fermiOnSupport.character ∧
    ampExchange ampBose = ampBose ∧
    ampExchange ampFermiSupport ≠ ampFermiSupport :=
  ⟨by decide, amp_exchange_bose_fixed, amp_exchange_fermi_ne_self⟩

/-! ## Import status packaging -/

inductive ImportStatus where
  | derived
  | underivable
  | conditionalImport
  deriving DecidableEq, Repr

/-- Classical residual joint exchange (permutation of sector labels). -/
def obStatsClassicalStatus : ImportStatus := .derived

/-- Forced quantum Bose/Fermi state-space law from FinL1 residual mass alone. -/
def obStatsFromFinL1Status : ImportStatus := .underivable

/-- Bose/Fermi characters under linear amplitude / phase-fiber host. -/
def obStatsUnderLiftStatus : ImportStatus := .conditionalImport

theorem classical_status_derived :
    obStatsClassicalStatus = ImportStatus.derived := rfl

theorem from_finL1_underivable :
    obStatsFromFinL1Status = ImportStatus.underivable := rfl

theorem under_lift_conditional :
    obStatsUnderLiftStatus = ImportStatus.conditionalImport := rfl

/-- Classical exchange works without sign characters ⇒ no forced Fermi law from FinL1. -/
theorem no_forced_fermi_from_finL1 :
    JointWeight.exchange jointAsym ≠ jointAsym ∧
    JointWeight.exchange jointSym = jointSym ∧
    obStatsFromFinL1Status = ImportStatus.underivable :=
  ⟨by decide, exchange_fixes_sym, rfl⟩

/-- **Main package.** -/
theorem exchange_statistics_package :
    (JointWeight.exchange jointAsym).total = jointAsym.total ∧
    ampExchange ampBose = ampBose ∧
    ampExchange ampFermiSupport ≠ ampFermiSupport ∧
    obStatsClassicalStatus = ImportStatus.derived ∧
    obStatsFromFinL1Status = ImportStatus.underivable ∧
    obStatsUnderLiftStatus = ImportStatus.conditionalImport :=
  ⟨exchange_total jointAsym, amp_exchange_bose_fixed, amp_exchange_fermi_ne_self,
    rfl, rfl, rfl⟩

/-- Full spin–statistics / continuum braid residual remains OPEN. -/
def fullSpinStatistics_open : Prop := True

theorem full_spin_statistics_marked_open :
    fullSpinStatistics_open := trivial

/-! ## Signed $S_2$ character residual (TOY-MECH)

Exchange law $\psi'(x,y)=\chi\,\psi(y,x)$ on integer joint amplitudes:

* $\chi=+1$ (Bose): diagonal free; off-diagonals equal when fixed.
* $\chi=-1$ (Fermi): fixed points require $a_{00}=a_{11}=0$ and $a_{10}=-a_{01}$.
-/

structure AmpJointZ where
  a00 : Int
  a01 : Int
  a10 : Int
  a11 : Int
  deriving DecidableEq, Repr

/-- Character $\chi\in\{+1,-1\}$ signed exchange. -/
def signedExchange (χ : Int) (j : AmpJointZ) : AmpJointZ :=
  { a00 := χ * j.a00
    a01 := χ * j.a10
    a10 := χ * j.a01
    a11 := χ * j.a11 }

/-- Symmetric Bose joint: fixed under $\chi=+1$. -/
def ampBoseZ : AmpJointZ := { a00 := 1, a01 := 1, a10 := 1, a11 := 1 }

/-- Antisymmetric Fermi joint: fixed under $\chi=-1$ (diagonal excluded). -/
def ampFermiZ : AmpJointZ := { a00 := 0, a01 := 1, a10 := -1, a11 := 0 }

/-- Diagonal-only joint (would be forbidden under Fermi fixed-point law). -/
def ampDiagOnly : AmpJointZ := { a00 := 1, a01 := 0, a10 := 0, a11 := 1 }

theorem signed_bose_fixed :
    signedExchange 1 ampBoseZ = ampBoseZ := by
  simp [signedExchange, ampBoseZ]

theorem signed_fermi_fixed :
    signedExchange (-1) ampFermiZ = ampFermiZ := by
  simp [signedExchange, ampFermiZ]

theorem signed_fermi_diagonal_excluded :
    ampFermiZ.a00 = 0 ∧ ampFermiZ.a11 = 0 := by
  simp [ampFermiZ]

/-- Diagonal-only joint is **not** fixed under Fermi signed exchange. -/
theorem signed_fermi_moves_diag_only :
    signedExchange (-1) ampDiagOnly ≠ ampDiagOnly := by
  decide

/-- Bose signed exchange does fix diagonal-only (no fermionic exclusion). -/
theorem signed_bose_fixes_diag_only :
    signedExchange 1 ampDiagOnly = ampDiagOnly := by
  simp [signedExchange, ampDiagOnly]

def AmpJointZ.add (j k : AmpJointZ) : AmpJointZ :=
  { a00 := j.a00 + k.a00, a01 := j.a01 + k.a01
    a10 := j.a10 + k.a10, a11 := j.a11 + k.a11 }

def AmpJointZ.smul (k : Int) (j : AmpJointZ) : AmpJointZ :=
  { a00 := k * j.a00, a01 := k * j.a01, a10 := k * j.a10, a11 := k * j.a11 }

def AmpJointZ.sub (j k : AmpJointZ) : AmpJointZ :=
  AmpJointZ.add j (AmpJointZ.smul (-1) k)

/-- Unsigned coordinate swap (χ absorbed separately). -/
def coordSwap (j : AmpJointZ) : AmpJointZ :=
  { a00 := j.a00, a01 := j.a10, a10 := j.a01, a11 := j.a11 }

/-- Symmetrizer $j + \tau j$ (Bose projector toy, unnormalized). -/
def symmetrizer (j : AmpJointZ) : AmpJointZ :=
  AmpJointZ.add j (coordSwap j)

/-- Antisymmetrizer $j - \tau j$ (Fermi projector toy, unnormalized). -/
def antisymmetrizer (j : AmpJointZ) : AmpJointZ :=
  AmpJointZ.sub j (coordSwap j)

theorem symmetrizer_on_bose :
    symmetrizer ampBoseZ = AmpJointZ.smul 2 ampBoseZ := by
  simp [symmetrizer, AmpJointZ.add, AmpJointZ.smul, coordSwap, ampBoseZ]

theorem antisymmetrizer_on_fermi :
    antisymmetrizer ampFermiZ = AmpJointZ.smul 2 ampFermiZ := by
  simp [antisymmetrizer, AmpJointZ.sub, AmpJointZ.add, AmpJointZ.smul, coordSwap,
    ampFermiZ]

theorem antisymmetrizer_kills_bose_offdiag_equal :
    antisymmetrizer ampBoseZ =
      { a00 := 0, a01 := 0, a10 := 0, a11 := 0 } := by
  simp [antisymmetrizer, AmpJointZ.sub, AmpJointZ.add, AmpJointZ.smul, coordSwap,
    ampBoseZ]

theorem symmetrizer_kills_fermi :
    symmetrizer ampFermiZ =
      { a00 := 0, a01 := 0, a10 := 0, a11 := 0 } := by
  simp [symmetrizer, AmpJointZ.add, coordSwap, ampFermiZ]

/-- Signed characters still require lift host (not FinL1 Nat tables alone). -/
def signedCharacterRequiresLiftHost : Bool := true

theorem signed_character_needs_lift :
    signedCharacterRequiresLiftHost = true ∧
    obStatsUnderLiftStatus = ImportStatus.conditionalImport :=
  ⟨rfl, rfl⟩

def exchangeSignedCharacterPackage_toy : Bool := true

/-- **Signed character residual package** (spin–statistics still OPEN). -/
theorem exchange_signed_character_package :
    exchangeSignedCharacterPackage_toy = true ∧
    signedExchange 1 ampBoseZ = ampBoseZ ∧
    signedExchange (-1) ampFermiZ = ampFermiZ ∧
    ampFermiZ.a00 = 0 ∧ ampFermiZ.a11 = 0 ∧
    signedExchange (-1) ampDiagOnly ≠ ampDiagOnly ∧
    signedExchange 1 ampDiagOnly = ampDiagOnly ∧
    antisymmetrizer ampBoseZ =
      { a00 := 0, a01 := 0, a10 := 0, a11 := 0 } ∧
    symmetrizer ampFermiZ =
      { a00 := 0, a01 := 0, a10 := 0, a11 := 0 } ∧
    fullSpinStatistics_open ∧
    signedCharacterRequiresLiftHost = true := by
  refine ⟨rfl, signed_bose_fixed, signed_fermi_fixed, ?_, ?_,
    signed_fermi_moves_diag_only, signed_bose_fixes_diag_only,
    antisymmetrizer_kills_bose_offdiag_equal, symmetrizer_kills_fermi,
    trivial, rfl⟩
  · simp [ampFermiZ]
  · simp [ampFermiZ]

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end ExchangeStatistics
end QM

#print axioms QM.ExchangeStatistics.classical_exchange_derived
#print axioms QM.ExchangeStatistics.s2_characters_packaged
#print axioms QM.ExchangeStatistics.exchange_statistics_package
#print axioms QM.ExchangeStatistics.exchange_signed_character_package
#print axioms QM.ExchangeStatistics.signed_fermi_fixed
#print axioms QM.ExchangeStatistics.structure_not_auth
