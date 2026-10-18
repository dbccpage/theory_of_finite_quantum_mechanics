import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic

/-!
# Bell–CHSH local (deterministic) bound (cycle 009, QM_029 neighborhood)

A finite, recognizable contextuality/nonlocality brick. For deterministic ±1 local assignments
`a₀,a₁,b₀,b₁ ∈ {−1,+1}`, the CHSH combination `a₀b₀ + a₀b₁ + a₁b₀ − a₁b₁` is bounded by `2`
(the local-realism / Bell bound), and the bound is tight.

This is the **classical** bound only. It is **not** a claim about the quantum value `2√2`, nor that
QM violates it — that is a separate (quantum) statement. No authority minted (LGGR). Mathlib-light
(`decide`).
-/

namespace QM.CHSH

/-- Sign of a bit: `true ↦ +1`, `false ↦ −1`. -/
def s (b : Bool) : ℤ := if b then 1 else -1

/-- The deterministic CHSH combination for local ±1 assignments. -/
def chsh (a₀ a₁ b₀ b₁ : Bool) : ℤ := s a₀ * s b₀ + s a₀ * s b₁ + s a₁ * s b₀ - s a₁ * s b₁

/-- **Local CHSH bound.** Every deterministic ±1 local assignment satisfies `chsh ≤ 2` — the
Bell–CHSH local-realism bound. -/
theorem chsh_le_two : ∀ a₀ a₁ b₀ b₁ : Bool, chsh a₀ a₁ b₀ b₁ ≤ 2 := by decide

/-- The symmetric lower bound `−2 ≤ chsh`. -/
theorem neg_two_le_chsh : ∀ a₀ a₁ b₀ b₁ : Bool, -2 ≤ chsh a₀ a₁ b₀ b₁ := by decide

/-- **Tightness.** The bound `2` is achieved (all `+1`). -/
theorem chsh_eq_two : chsh true true true true = 2 := by decide

/-! ## Tsirelson is not on this carrier — `T19`, the arithmetic core

The header above is careful to say this file proves the **classical** bound only,
and that `2√2` is "a separate (quantum) statement". This section makes precise
*why* it must be separate on an exact-rational carrier: the quantum value is not
merely unproved here, it is **unnameable** here.

`2√2` is the positive root of `x² = 8`. No rational satisfies that. So the
separation between the local bound and the Tsirelson bound is **algebraic, not
numerical** — the same carrier-relative class as `OB-SPECTRAL`, whose witness
`[[1,1],[1,0]]` has characteristic polynomial `x² − x − 1` and irrational
eigenvalues (see `qm_ob_spectral_finite.lean`, `no_rational_root_golden`).

Consequence for the ledger: `T19` (exact `2√2` Tsirelson) is a **priced import**
of an algebraic extension, not a pending computation. Proving it "harder" over ℚ
cannot succeed, for the same reason `T15` cannot.

**Not claimed:** that quantum mechanics attains `2√2` (that needs the operator
host), nor that no carrier expresses it — `ℚ(√2)` obviously does. Only that
**this** carrier does not. AuthorityEffect: None. -/

/-- No rational squares to `8`; equivalently `2√2 ∉ ℚ`.

Proof stays in `ℤ`: clear denominators to `a² = 8b²`, so `b ∣ a²`; `q.reduced`
makes `b` coprime to `a²`, forcing `b = 1`; then `a² = 8` bounds `a` into
`[-3, 3]`, where no integer works. -/
theorem no_rational_squares_to_eight : ¬ ∃ q : ℚ, q ^ 2 = 8 := by
  rintro ⟨q, hq⟩
  have hb : ((q.den : ℤ) : ℚ) ≠ 0 := by
    exact_mod_cast (Int.natCast_ne_zero.mpr q.den_nz)
  have hnd : (q.num : ℚ) / ((q.den : ℤ) : ℚ) = q := by
    push_cast
    exact Rat.num_div_den q
  have key : (q.num : ℚ) ^ 2 = 8 * ((q.den : ℤ) : ℚ) ^ 2 := by
    rw [← hnd] at hq
    field_simp at hq
    linarith
  have keyZ : q.num ^ 2 = 8 * (q.den : ℤ) ^ 2 := by exact_mod_cast key
  have hdvdZ : (q.den : ℤ) ∣ q.num ^ 2 := ⟨8 * (q.den : ℤ), by rw [keyZ]; ring⟩
  have hdvdN : q.den ∣ q.num.natAbs ^ 2 := by
    have h := Int.natAbs_dvd_natAbs.mpr hdvdZ
    simpa [Int.natAbs_pow] using h
  have hcop : Nat.Coprime q.den (q.num.natAbs ^ 2) := (q.reduced.symm).pow_right 2
  have hden1 : q.den = 1 := Nat.eq_one_of_dvd_coprimes hcop dvd_rfl hdvdN
  rw [hden1] at keyZ
  push_cast at keyZ
  have hub : q.num ≤ 3 := by nlinarith [keyZ, sq_nonneg (q.num - 3)]
  have hlb : -3 ≤ q.num := by nlinarith [keyZ, sq_nonneg (q.num + 3)]
  interval_cases h : q.num <;> omega

/-- **The separation is algebraic.** The classical bound `2` is a rational this
carrier both states and *saturates*; the Tsirelson value satisfies `x² = 8` and
is **not an element of `ℚ`**.

Stated precisely, because the stronger reading is false: the value is not
"unnameable" and it can be written down over rational syntax — `x > 0 ∧ x² = 8`
characterises it uniquely. What fails is *membership*, not expressibility. This
file also does not prove the Tsirelson inequality itself, nor that quantum
mechanics attains it; it proves rational non-membership of the saturating
scalar. -/
theorem local_bound_rational_tsirelson_not :
    (∃ a₀ a₁ b₀ b₁ : Bool, chsh a₀ a₁ b₀ b₁ = 2) ∧ ¬ ∃ q : ℚ, q ^ 2 = 8 :=
  ⟨⟨true, true, true, true, chsh_eq_two⟩, no_rational_squares_to_eight⟩

/-- Neither `√8` (T19) nor `√5` (T15) is rational.

**Scope, because the name used to overreach.** This is a conjunction of two
non-membership facts, not a classification theorem. It does *not* say the two
obstructions are one class, and they are not the same extension:
`ℚ(√8) = ℚ(√2) ≠ ℚ(√5)`. What they share is a degree — both are quadratic — and
that shared degree is **not** proved here. If "same obstruction class" is to
mean "both require a degree-2 extension of `ℚ`", that class needs a definition
and a membership proof; neither exists in this file. -/
theorem sqrt_eight_and_sqrt_five_not_rational :
    (¬ ∃ q : ℚ, q ^ 2 = 8) ∧ (¬ ∃ q : ℚ, q ^ 2 = 5) := by
  refine ⟨no_rational_squares_to_eight, ?_⟩
  rintro ⟨q, hq⟩
  have hnd : (q.num : ℚ) / ((q.den : ℤ) : ℚ) = q := by
    push_cast
    exact Rat.num_div_den q
  have hb : ((q.den : ℤ) : ℚ) ≠ 0 := by
    exact_mod_cast (Int.natCast_ne_zero.mpr q.den_nz)
  have key : (q.num : ℚ) ^ 2 = 5 * ((q.den : ℤ) : ℚ) ^ 2 := by
    rw [← hnd] at hq
    field_simp at hq
    linarith
  have keyZ : q.num ^ 2 = 5 * (q.den : ℤ) ^ 2 := by exact_mod_cast key
  have hdvdZ : (q.den : ℤ) ∣ q.num ^ 2 := ⟨5 * (q.den : ℤ), by rw [keyZ]; ring⟩
  have hdvdN : q.den ∣ q.num.natAbs ^ 2 := by
    have h := Int.natAbs_dvd_natAbs.mpr hdvdZ
    simpa [Int.natAbs_pow] using h
  have hcop : Nat.Coprime q.den (q.num.natAbs ^ 2) := (q.reduced.symm).pow_right 2
  have hden1 : q.den = 1 := Nat.eq_one_of_dvd_coprimes hcop dvd_rfl hdvdN
  rw [hden1] at keyZ
  push_cast at keyZ
  have hub : q.num ≤ 3 := by nlinarith [keyZ, sq_nonneg (q.num - 3)]
  have hlb : -3 ≤ q.num := by nlinarith [keyZ, sq_nonneg (q.num + 3)]
  interval_cases h : q.num <;> omega

end QM.CHSH

#print axioms QM.CHSH.no_rational_squares_to_eight
#print axioms QM.CHSH.local_bound_rational_tsirelson_not
#print axioms QM.CHSH.sqrt_eight_and_sqrt_five_not_rational


#print axioms QM.CHSH.chsh_le_two
#print axioms QM.CHSH.neg_two_le_chsh
#print axioms QM.CHSH.chsh_eq_two
