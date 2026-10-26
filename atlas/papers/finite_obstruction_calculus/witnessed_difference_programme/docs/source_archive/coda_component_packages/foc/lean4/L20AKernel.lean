/-!
# Φ–Γ separation kernel

Logical core of the finite obstruction Φ–Γ split:

  (1) Φ₁(q) = 0  ⇒  Γ₂(q) = 0
  (2) Φ₁(q) > 0 ∧ Γ₂(q) = 0  ↔  q ∈ H¹ ∖ {0}
  (3) Γ₂(q) > 0  ⇒  Φ₁(q) > 0 ∧ q ∉ H¹

with the two nonredundancy corollaries (Γ₂ cannot separate ExactRepair from
CoherentResidual; Φ₁ cannot separate CoherentResidual from NonclosedDefect).

These follow by pure logic from the four **declared primitive** facts of the
finite obstruction complex at the quotient seam Q¹/Q² where Q² = C² / im(a₂),
captured as the fields of `FOCSep`:

* P1 `phi_pos_def`   — Φ₁ is positive-definite on Q¹ (quotient-gauge separation);
* P2 `gamma_pos_def` — the declared Q² norm is positive-definite on the quotient;
* P3 `H1_iff_ker`    — H¹ is the kernel of the induced coboundary d̄₁ : Q¹ → Q²;
* P4 `d1_zero`       — d̄₁ sends 0 to 0.

## Scope (honest)

This kernel proves the **separation/classification implications** *from* P1–P4.
It does **not** re-derive P1–P4 themselves — those are the normed-space /
quotient-gauge construction of Φ₁, Γ₂, H¹ and live outside this pure-Lean core
(the reference Python implementation `code/finite_obstruction.py` checks the
exact rational (Φ,Γ) split via linear programming certificates; cf. `finite_obstruction.py`).
Magnitudes are modeled by `Nat` because
the kernel uses only the zero/positive dichotomy (`= 0` vs `> 0`): for any
ℝ≥0-valued norm `> 0 ↔ ≠ 0`, which `Nat` captures exactly. No `Mathlib`
dependency (pure Lean 4), consistent with the `OmegaCore` library.
-/

namespace FOC.L20A

variable {Q Q2 : Type}

/-- Declared structure of the finite obstruction complex at the Q¹/Q² quotient seam.
Here `Q2` represents the stage-2 quotient space `Q₂ = C₂ / im(a₂)` on which `Γ₂`
evaluates, and `d1bar` represents the induced coboundary `d̄₁ : Q¹ → Q²` sending
`q ↦ [d₁ x]`.
The fields P1–P4 are the standard positive-definiteness / kernel facts; the
theorems below derive L20A from them. -/
structure FOCSep (Q Q2 : Type) where
  zeroQ : Q
  zeroQ2 : Q2
  /-- The induced degree-1 coboundary `d̄₁` from `Q¹` to the quotient `Q²`. -/
  d1bar : Q → Q2
  /-- Φ₁ (only the zero/positive dichotomy is used; `≥ 0` modeled by `Nat`). -/
  phi1 : Q → Nat
  /-- Γ₂ (likewise). -/
  gamma2 : Q → Nat
  /-- Membership `q ∈ H¹`. -/
  inH1 : Q → Prop
  /-- P1: Φ₁ positive-definite on Q¹ (quotient-gauge separation). -/
  phi_pos_def : ∀ q, phi1 q = 0 ↔ q = zeroQ
  /-- P2: the declared Q² norm is positive-definite (zero in quotient Q₂). -/
  gamma_pos_def : ∀ q, gamma2 q = 0 ↔ d1bar q = zeroQ2
  /-- P3: H¹ = ker d̄₁. -/
  H1_iff_ker : ∀ q, inH1 q ↔ d1bar q = zeroQ2
  /-- P4: d̄₁ 0 = 0. -/
  d1_zero : d1bar zeroQ = zeroQ2

namespace FOCSep

variable (S : FOCSep Q Q2)

/-- (1) `Φ₁(q) = 0 ⇒ Γ₂(q) = 0`. -/
theorem phi_zero_imp_gamma_zero (q : Q) (h : S.phi1 q = 0) : S.gamma2 q = 0 := by
  have hq : q = S.zeroQ := (S.phi_pos_def q).mp h
  have hd : S.d1bar q = S.zeroQ2 := by rw [hq]; exact S.d1_zero
  exact (S.gamma_pos_def q).mpr hd

/-- (2) `Φ₁(q) > 0 ∧ Γ₂(q) = 0  ↔  q ∈ H¹ ∧ q ≠ 0`. -/
theorem coherent_residual_iff (q : Q) :
    (0 < S.phi1 q ∧ S.gamma2 q = 0) ↔ (S.inH1 q ∧ q ≠ S.zeroQ) := by
  constructor
  · rintro ⟨hphi, hgam⟩
    have hne : q ≠ S.zeroQ := by
      intro hq
      have hz : S.phi1 q = 0 := (S.phi_pos_def q).mpr hq
      exact Nat.ne_of_gt hphi hz
    have hd : S.d1bar q = S.zeroQ2 := (S.gamma_pos_def q).mp hgam
    exact ⟨(S.H1_iff_ker q).mpr hd, hne⟩
  · rintro ⟨hH, hne⟩
    have hd : S.d1bar q = S.zeroQ2 := (S.H1_iff_ker q).mp hH
    have hgam : S.gamma2 q = 0 := (S.gamma_pos_def q).mpr hd
    have hphi_ne : S.phi1 q ≠ 0 := fun h0 => hne ((S.phi_pos_def q).mp h0)
    exact ⟨Nat.pos_of_ne_zero hphi_ne, hgam⟩

/-- (3) `Γ₂(q) > 0 ⇒ Φ₁(q) > 0 ∧ q ∉ H¹`. -/
theorem nonclosed_of_gamma_pos (q : Q) (h : 0 < S.gamma2 q) :
    0 < S.phi1 q ∧ ¬ S.inH1 q := by
  have hg_ne : S.gamma2 q ≠ 0 := Nat.ne_of_gt h
  have hd_ne : S.d1bar q ≠ S.zeroQ2 := fun hd => hg_ne ((S.gamma_pos_def q).mpr hd)
  have hnotH : ¬ S.inH1 q := fun hH => hd_ne ((S.H1_iff_ker q).mp hH)
  have hq_ne : q ≠ S.zeroQ := by
    intro hq; rw [hq] at hd_ne; exact hd_ne S.d1_zero
  have hphi_ne : S.phi1 q ≠ 0 := fun h0 => hq_ne ((S.phi_pos_def q).mp h0)
  exact ⟨Nat.pos_of_ne_zero hphi_ne, hnotH⟩

/-- Nonredundancy A: `Γ₂` cannot distinguish `ExactRepair` (Φ₁=0) from
`CoherentResidual` (Φ₁>0 ∧ Γ₂=0) — both have `Γ₂ = 0`. -/
theorem gamma_cannot_separate_exact_coherent_residual (q q' : Q)
    (hexact : S.phi1 q = 0) (hcoherent : 0 < S.phi1 q' ∧ S.gamma2 q' = 0) :
    S.gamma2 q = 0 ∧ S.gamma2 q' = 0 :=
  ⟨S.phi_zero_imp_gamma_zero q hexact, hcoherent.2⟩

/-- Nonredundancy B: `Φ₁` cannot distinguish `CoherentResidual` (Φ₁>0 ∧ Γ₂=0)
from `NonclosedDefect` (Γ₂>0) — both have `Φ₁ > 0`. -/
theorem phi_cannot_separate_coherent_residual_nonclosed (q q' : Q)
    (hcoherent : 0 < S.phi1 q ∧ S.gamma2 q = 0) (hnonclosed : 0 < S.gamma2 q') :
    0 < S.phi1 q ∧ 0 < S.phi1 q' :=
  ⟨hcoherent.1, (S.nonclosed_of_gamma_pos q' hnonclosed).1⟩

end FOCSep

/-! ## Non-vacuity witness

A concrete `FOCSep` is exhibited so the theorems above are not quantified over
an empty/degenerate structure (the `Prop`-field vacuity trap). The witness uses
a 3-element carrier, one element per trichotomy regime, and all four primitives
P1–P4 discharge by `decide`. -/
namespace Witness

/-- Concrete 3-class carrier, one constructor per trichotomy regime. -/
inductive Q3 where
  | qE  -- ExactRepair witness   (Φ₁ = 0)
  | qS  -- CoherentResidual      (Φ₁ > 0, Γ₂ = 0)
  | qO  -- NonclosedDefect       (Γ₂ > 0)
deriving DecidableEq

def d1bar : Q3 → Bool
  | .qE => false
  | .qS => false
  | .qO => true

def phi1 : Q3 → Nat
  | .qE => 0
  | .qS => 1
  | .qO => 1

def gamma2 : Q3 → Nat
  | .qE => 0
  | .qS => 0
  | .qO => 1

def inH1 : Q3 → Prop
  | .qE => True
  | .qS => True
  | .qO => False

/-- The witness is a genuine `FOCSep`: all four declared primitives hold. -/
def witness : FOCSep Q3 Bool where
  zeroQ := .qE
  zeroQ2 := false
  d1bar := d1bar
  phi1 := phi1
  gamma2 := gamma2
  inH1 := inH1
  phi_pos_def := by intro q; cases q <;> decide
  gamma_pos_def := by intro q; cases q <;> decide
  H1_iff_ker := by intro q; cases q <;> simp [inH1, d1bar]
  d1_zero := rfl

-- All three regimes are actually inhabited (the trichotomy is non-vacuous):
example : witness.phi1 .qE = 0 := rfl                                  -- ExactRepair
example : 0 < witness.phi1 .qS ∧ witness.gamma2 .qS = 0 := by decide   -- CoherentResidual
example : 0 < witness.gamma2 .qO := by decide                          -- NonclosedDefect

-- The proved characterizations fire on the witness:
example : witness.gamma2 .qE = 0 := witness.phi_zero_imp_gamma_zero .qE rfl
example : witness.inH1 .qS ∧ (Q3.qS ≠ Q3.qE) := (witness.coherent_residual_iff .qS).mp (by decide)
example : 0 < witness.phi1 .qO ∧ ¬ witness.inH1 .qO :=
  witness.nonclosed_of_gamma_pos .qO (by decide)

end Witness

#print axioms FOC.L20A.FOCSep.phi_zero_imp_gamma_zero
#print axioms FOC.L20A.FOCSep.coherent_residual_iff
#print axioms FOC.L20A.FOCSep.nonclosed_of_gamma_pos
#print axioms FOC.L20A.FOCSep.gamma_cannot_separate_exact_coherent_residual
#print axioms FOC.L20A.FOCSep.phi_cannot_separate_coherent_residual_nonclosed

end FOC.L20A
