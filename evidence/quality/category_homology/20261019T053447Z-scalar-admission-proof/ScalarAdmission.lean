import Mathlib.Data.Int.GCD
import Mathlib.Data.Rat.Defs
import Mathlib.Data.List.Basic

/-! AuthorityEffect: None. Canonical integer pairs are exactly the stored
representation of Rat. The indexed scan rejects the first noncanonical pair;
literal receipt transport does not assert any theorem about its annotations.
BigInt/GCD, Vec enumeration, BasicMatrix storage and Rust/serde correspondence
are separate source/runtime obligations. No Rust/MIR extraction is claimed.
-/
namespace TFQM.ScalarAdmission

structure Raw where
  num : Int
  den : Int

def Canonical (value : Raw) : Prop := 0 < value.den ∧ Int.gcd value.num value.den = 1

def reify (value : Raw) (valid : Canonical value) : Rat where
  num := value.num
  den := value.den.natAbs
  den_nz := Int.natAbs_ne_zero.mpr (ne_of_gt valid.1)
  reduced := valid.2

theorem reify_fields (value : Raw) (valid : Canonical value) :
    (reify value valid).num = value.num ∧ ((reify value valid).den : Int) = value.den := by
  exact ⟨rfl, Int.natAbs_of_nonneg (le_of_lt valid.1)⟩

theorem canonical_roundtrip (value : Rat) : Canonical ⟨value.num, value.den⟩ := by
  constructor
  · exact_mod_cast value.den_pos
  · simpa only [Int.gcd_def, Int.natAbs_natCast] using value.reduced

theorem zero_has_unit_denominator (value : Raw) (valid : Canonical value)
    (zero : value.num = 0) : value.den = 1 := by
  have reduced : value.den.natAbs = 1 := by simpa [zero] using valid.2
  rw [← Int.natAbs_of_nonneg (le_of_lt valid.1), reduced]

theorem zero_denominator_refused (num : Int) : ¬ Canonical ⟨num, 0⟩ := by
  simp [Canonical]

theorem negative_denominator_refused (value : Raw) (negative : value.den < 0) :
    ¬ Canonical value := by
  intro valid
  exact (not_lt_of_ge (le_of_lt valid.1)) negative

noncomputable def scan : List Raw → Nat → Except Nat Unit
  | [], _ => .ok ()
  | value :: tail, offset =>
    if Canonical value then scan tail (offset + 1) else .error offset

theorem scan_success_iff (values : List Raw) (offset : Nat) :
    scan values offset = .ok () ↔ ∀ value ∈ values, Canonical value := by
  induction values generalizing offset with
  | nil => simp [scan]
  | cons value tail ih =>
    by_cases valid : Canonical value <;> simp [scan, valid, ih]

theorem scan_failed_head (value : Raw) (tail : List Raw) (offset : Nat)
    (invalid : ¬ Canonical value) : scan (value :: tail) offset = .error offset := by
  simp [scan, invalid]

theorem first_invalid (prefix : List Raw) (bad : Raw) (tail : List Raw) (offset : Nat)
    (valid : ∀ value ∈ prefix, Canonical value) (invalid : ¬ Canonical bad) :
    scan (prefix ++ bad :: tail) offset = .error (offset + prefix.length) := by
  induction prefix generalizing offset with
  | nil => simp [scan, invalid]
  | cons head rest ih =>
    have first : Canonical head := valid head (by simp)
    have remaining : ∀ value ∈ rest, Canonical value := by
      intro value member
      exact valid value (by simp [member])
    rw [List.cons_append, scan, if_pos first, ih (offset + 1) remaining]
    congr 1
    simp only [List.length_cons]
    omega

def store (raw : α) : α := raw

theorem store_preserves (raw : α) : store raw = raw := rfl

#print axioms reify_fields
#print axioms canonical_roundtrip
#print axioms zero_has_unit_denominator
#print axioms zero_denominator_refused
#print axioms negative_denominator_refused
#print axioms scan_success_iff
#print axioms scan_failed_head
#print axioms first_invalid
#print axioms store_preserves

end TFQM.ScalarAdmission
