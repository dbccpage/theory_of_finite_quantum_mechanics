import Mathlib.Analysis.Normed.Group.Quotient

/-!
# PL-QM007-2 — The Φ₁ analytic identity (QM_003 / cofiber-to-Banach bridge)

Discharges the prose obligation `PL-QM007-2`: the quotient diagnostic `Φ₁` equals the
Banach quotient norm. For a seminormed additive group `E` and the admissible-repair
subgroup `S = im(d₀)`, the residual mass

  `Φ₁([x]) := ⨅_{s ∈ S} ‖x − s‖`

equals the quotient norm `‖mk x‖` in `E ⧸ S`.

Companion to `CofiberScalarSeparation.lean` (LT-H), which fences the scalar ≠ object
conflation on a toy `ℕ` shadow; this file supplies the real functional-analytic identity
over a seminormed group, using Mathlib's quotient-norm machinery.

**No authority (LGGR).** This mechanizes a *diagnostic* identity. A checked norm equality
is still a measurement; it mints no global authority and does not select a QM structure.
-/

namespace QM.CofiberPhi1

variable {E : Type*} [SeminormedAddCommGroup E] (S : AddSubgroup E)

/-- The quotient diagnostic `Φ₁`: the infimal residual norm over admissible repairs
`s ∈ S = im(d₀)`. -/
noncomputable def phi1 (x : E) : ℝ := ⨅ s : S, ‖x - (s : E)‖

/-- The residual norms are bounded below by `0`. -/
theorem bddBelow_residuals (x : E) :
    BddBelow (Set.range fun s : S => ‖x - (s : E)‖) :=
  ⟨0, by rintro _ ⟨s, rfl⟩; exact norm_nonneg _⟩

/-- `Φ₁` is nonnegative. -/
theorem phi1_nonneg (x : E) : 0 ≤ phi1 S x :=
  le_ciInf fun _ => norm_nonneg _

/-- **The Φ₁ analytic identity.** `Φ₁([x])` equals the quotient norm of `mk x` in `E ⧸ S`:
the infimum over admissible repairs is exactly the Banach quotient norm. This discharges
`PL-QM007-2` (QM_003): the prose `Φ₁ = ‖[·]‖_quotient` claim is now a checked theorem.

With `S := d₀.range` this is the paper's `Φ₁([x]) = inf_α ‖x − d₀ α‖`; reindexing the infimum
from repairs `α` to the image subgroup `S = im(d₀)` is immediate (same set). -/
theorem phi1_eq_quotient_norm (x : E) :
    phi1 S x = ‖(QuotientAddGroup.mk x : E ⧸ S)‖ := by
  have hbdd := bddBelow_residuals S x
  have mk_sub_eq : ∀ a b : E, (QuotientAddGroup.mk (a - b) : E ⧸ S)
      = QuotientAddGroup.mk a - QuotientAddGroup.mk b := by
    intro a b; simp
  apply le_antisymm
  · -- Φ₁ ≤ ‖mk x‖ : a near-optimal coset representative
    refine le_of_forall_pos_le_add fun ε hε => ?_
    obtain ⟨m, hm, hmlt⟩ := QuotientAddGroup.exists_norm_mk_lt (QuotientAddGroup.mk x) hε
    have hsS : x - m ∈ S := by
      rw [← QuotientAddGroup.eq_zero_iff, mk_sub_eq, hm, sub_self]
    calc phi1 S x ≤ ‖x - ((⟨x - m, hsS⟩ : S) : E)‖ := ciInf_le hbdd _
      _ = ‖m‖ := by simp [sub_sub_cancel]
      _ ≤ ‖(QuotientAddGroup.mk x : E ⧸ S)‖ + ε := le_of_lt hmlt
  · -- ‖mk x‖ ≤ Φ₁ : every residual dominates the quotient norm
    refine le_ciInf fun s => ?_
    have hs0 : (QuotientAddGroup.mk (s : E) : E ⧸ S) = 0 :=
      (QuotientAddGroup.eq_zero_iff _).mpr s.2
    have hmk : (QuotientAddGroup.mk x : E ⧸ S)
        = QuotientAddGroup.mk (x - (s : E)) := by rw [mk_sub_eq, hs0, sub_zero]
    rw [hmk]; exact QuotientAddGroup.norm_mk_le_norm

end QM.CofiberPhi1

#print axioms QM.CofiberPhi1.phi1_eq_quotient_norm
