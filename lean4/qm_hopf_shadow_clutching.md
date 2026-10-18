/-
QM.HopfShadow — finite Hopf clutching certificates (TUFT B3).

Mechanizes exactly what the Rust `omega_discrete_deformation_algebra::hopf_shadow`
module checks (PR #1046), discharging the two proof-ledger targets of
`research/encyclopedia/proof_ledgers/proof_ledger_20260716.md`:

* PL-GTOC-TUFT-1 — `section_exists_iff_deg_zero` (a global section of the finite
  degree-d clutching model exists iff the clutching degree vanishes) and
  `pullback_trivializes` (the tautological fiber gauge kills the pulled-back
  transition on the total space — the twisted-bundle DDA lift absorbs the
  obstruction).
* PL-GTOC-TUFT-2 — `z6_joint_factorization_iff` (joint ℤ₂ × ℤ₃ factorization of
  the reduced models iff `6 ∣ d`) plus the decidable blocking table mirroring the
  Rust `z6_shadow` tests.

Model: the two-chart S² with a k-sampled equator; a chart gauge is one constant
per chart (the DECLARED contractible-chart feature of the finite presentation);
the transition cochain is `i ↦ d·i` in `ZMod k`. Everything is stated at the
finite level only — no continuum claim, no physics claim, no authority
(the continuum readings live in ENC-1173/1174; the classical linking-number
interpretation stays there too).
-/
import Mathlib.Data.ZMod.Basic

namespace QM.HopfShadow

/-- **PL-GTOC-TUFT-1 (section decision).** In the two-chart finite clutching
model over `ZMod k`, a global section — a constant gauge pair `(aN, aS)` with
`aN - aS = d·i` at every equator sample `i` — exists iff the clutching degree
`d` vanishes. (For `k = 0`, `ZMod 0 = ℤ` and the statement still holds; no
`NeZero` hypothesis is needed.) Mirrors `ClutchingShadow::decide_section`. -/
theorem section_exists_iff_deg_zero {k : ℕ} (d : ZMod k) :
    (∃ aN aS : ZMod k, ∀ i : ZMod k, aN - aS = d * i) ↔ d = 0 := by
  constructor
  · rintro ⟨aN, aS, h⟩
    have h0 : aN - aS = 0 := by simpa using h 0
    have h1 : aN - aS = d := by simpa using h 1
    rw [h0] at h1
    exact h1.symm
  · rintro rfl
    exact ⟨0, 0, fun i => by simp⟩

/-- **PL-GTOC-TUFT-1 (lift absorbs).** On the total space, the tautological
fiber-coordinate gauges `aN(i, j) = j` and `aS(i, j) = j - d·i` exhibit the
pulled-back transition as a coboundary at every overlap point — the DDA
lift-to-total-space certificate. Mirrors `ClutchingShadow::lift_to_total_space`
(whose guard branch is exactly the failure of this identity, hence unreachable). -/
theorem pullback_trivializes {k : ℕ} (d i j : ZMod k) :
    j - (j - d * i) = d * i :=
  sub_sub_cancel j (d * i)

/-- **PL-GTOC-TUFT-2 (joint factorization).** The reduced ℤ₂- and ℤ₃-models are
both trivial iff `6 ∣ d`: the finite shadow of the ℤ₆ = ℤ₂ × ℤ₃ splitting used
by ENC-1174 (TUFT Thm 9), at the strength the finite model proves — nothing
about the continuum obstruction class is asserted. Mirrors
`ClutchingShadow::z6_shadow` / `factors_through`. -/
theorem z6_joint_factorization_iff (d : ℕ) :
    ((d : ZMod 2) = 0 ∧ (d : ZMod 3) = 0) ↔ (d : ZMod 6) = 0 := by
  rw [CharP.cast_eq_zero_iff (ZMod 2) 2, CharP.cast_eq_zero_iff (ZMod 3) 3,
    CharP.cast_eq_zero_iff (ZMod 6) 6]
  constructor
  · rintro ⟨h2, h3⟩
    exact Nat.Coprime.mul_dvd_of_dvd_of_dvd (by decide) h2 h3
  · intro h6
    exact ⟨dvd_trans ⟨3, rfl⟩ h6, dvd_trans ⟨2, rfl⟩ h6⟩

/-- The reduced-model section decision agrees with divisibility: pushing the
degree forward to `ZMod m` and asking for a section is asking `m ∣ d`.
(Composition of `section_exists_iff_deg_zero` at `m` with the characteristic
of `ZMod m`; stated for the natural-number degree the Rust module consumes.) -/
theorem reduced_section_iff_dvd (m d : ℕ) :
    (∃ aN aS : ZMod m, ∀ i : ZMod m, aN - aS = (d : ZMod m) * i) ↔ m ∣ d := by
  rw [section_exists_iff_deg_zero, CharP.cast_eq_zero_iff (ZMod m) m]

/-- Blocking table, `d = 1..5` over the ℤ₆ shadow — the Lean mirror of the Rust
`z6_shadow_blocking_table` test: each nonzero residue is blocked (fails joint
factorization). Decidable, checked by `decide`. -/
theorem z6_blocked_d1 : ¬(((1 : ℕ) : ZMod 2) = 0 ∧ ((1 : ℕ) : ZMod 3) = 0) := by decide
theorem z6_blocked_d2 : ¬(((2 : ℕ) : ZMod 2) = 0 ∧ ((2 : ℕ) : ZMod 3) = 0) := by decide
theorem z6_blocked_d3 : ¬(((3 : ℕ) : ZMod 2) = 0 ∧ ((3 : ℕ) : ZMod 3) = 0) := by decide
theorem z6_blocked_d4 : ¬(((4 : ℕ) : ZMod 2) = 0 ∧ ((4 : ℕ) : ZMod 3) = 0) := by decide
theorem z6_blocked_d5 : ¬(((5 : ℕ) : ZMod 2) = 0 ∧ ((5 : ℕ) : ZMod 3) = 0) := by decide
theorem z6_unblocked_d6 : (((6 : ℕ) : ZMod 2) = 0 ∧ ((6 : ℕ) : ZMod 3) = 0) := by decide

/-- Hopf instance (`k = 6`, `d = 1`): no section exists — the finite Hopf shadow
refuses flat repair. Decidable instance mirroring the Rust
`hopf_d1_refused_then_lift_absorbs` test (the lift half is
`pullback_trivializes`, which holds for every `k, d`). -/
theorem hopf_shadow_k6_d1_refused :
    ¬(∃ aN aS : ZMod 6, ∀ i : ZMod 6, aN - aS = (1 : ZMod 6) * i) := by decide

#print axioms QM.HopfShadow.section_exists_iff_deg_zero
#print axioms QM.HopfShadow.pullback_trivializes
#print axioms QM.HopfShadow.z6_joint_factorization_iff
#print axioms QM.HopfShadow.reduced_section_iff_dvd
#print axioms QM.HopfShadow.hopf_shadow_k6_d1_refused
#print axioms QM.HopfShadow.z6_blocked_d1
#print axioms QM.HopfShadow.z6_blocked_d2
#print axioms QM.HopfShadow.z6_blocked_d3
#print axioms QM.HopfShadow.z6_blocked_d4
#print axioms QM.HopfShadow.z6_blocked_d5
#print axioms QM.HopfShadow.z6_unblocked_d6

end QM.HopfShadow
