import Mathlib.Data.Int.Basic

/-! AuthorityEffect: None. Exact rejected-index payloads and Boolean inversion
parity. No categorical, simplicial-homology, provenance or rank theorem is
claimed. Rust try_from, Vec/iterator and representation correspondence are
separately reviewed; these are not compiler-extracted Rust/MIR proofs.
-/
namespace TFQM.DegreeRepair

inductive Failure where
  | signed (value : Int)
  | index (value : Nat)
  deriving DecidableEq

def reject (index : Nat) : Failure :=
  if index ≤ 2147483647 then .signed index else .index index

def payload : Failure → Int
  | .signed value => value
  | .index value => value

theorem payload_exact (index : Nat) : payload (reject index) = index := by
  unfold reject
  split <;> rfl

theorem signed_index (index : Nat) (fits : index ≤ 2147483647) :
    reject index = .signed index := by simp [reject, fits]

theorem large_index (index : Nat) (large : 2147483647 < index) :
    reject index = .index index := by simp [reject, Nat.not_le.mpr large]

def dimension (a b c index : Nat) : Except Failure Nat :=
  match index with
  | 0 => .ok a
  | 1 => .ok b
  | 2 => .ok c
  | other => .error (reject other)

theorem dimension_zero (a b c : Nat) : dimension a b c 0 = .ok a := rfl
theorem dimension_one (a b c : Nat) : dimension a b c 1 = .ok b := rfl
theorem dimension_two (a b c : Nat) : dimension a b c 2 = .ok c := rfl

theorem outside_support (a b c index : Nat) (outside : 3 ≤ index) :
    dimension a b c index = .error (reject index) := by
  cases index with
  | zero => omega
  | succ n =>
    cases n with
    | zero => omega
    | succ n =>
      cases n with
      | zero => omega
      | succ n => rfl

theorem outside_payload (a b c index : Nat) (outside : 3 ≤ index) :
    ∃ failure, dimension a b c index = .error failure ∧ payload failure = index := by
  exact ⟨reject index, outside_support a b c index outside, payload_exact index⟩

def inversionCount : List Bool → Nat
  | [] => 0
  | flag :: flags => (if flag then 1 else 0) + inversionCount flags

def parity : List Bool → Bool
  | [] => false
  | flag :: flags => if flag then !parity flags else parity flags

def scan (initial : Bool) : List Bool → Bool
  | [] => initial
  | flag :: flags => scan (Bool.xor initial flag) flags

theorem scan_append (left right : List Bool) (initial : Bool) :
    scan initial (left ++ right) = scan (scan initial left) right := by
  induction left generalizing initial with
  | nil => rfl
  | cons flag flags ih => simp only [List.cons_append, scan, ih]

theorem scan_parity (flags : List Bool) (initial : Bool) :
    scan initial flags = Bool.xor initial (parity flags) := by
  induction flags generalizing initial with
  | nil => cases initial <;> rfl
  | cons flag flags ih =>
    cases initial <;> cases flag <;> simp [scan, parity, ih]

theorem parity_count (flags : List Bool) :
    parity flags = decide (inversionCount flags % 2 = 1) := by
  induction flags with
  | nil => rfl
  | cons flag flags ih =>
    cases flag with
    | false => simpa [parity, inversionCount] using ih
    | true =>
      have bound := Nat.mod_lt (inversionCount flags) (by decide : 0 < 2)
      cases remainder : inversionCount flags % 2 with
      | zero => simp [parity, inversionCount, ih, Nat.add_mod, remainder]
      | succ n =>
        have zero : n = 0 := by omega
        subst n
        simp [parity, inversionCount, ih, Nat.add_mod, remainder]

theorem scan_count (flags : List Bool) :
    scan false flags = decide (inversionCount flags % 2 = 1) := by
  rw [scan_parity, parity_count]
  cases decide (inversionCount flags % 2 = 1) <;> rfl

def orientation (flags : List Bool) : Int := if scan false flags then -1 else 1

theorem orientation_sign (flags : List Bool) :
    orientation flags = -1 ∨ orientation flags = 1 := by
  cases value : scan false flags <;> simp [orientation, value]

#print axioms payload_exact
#print axioms signed_index
#print axioms large_index
#print axioms dimension_zero
#print axioms dimension_one
#print axioms dimension_two
#print axioms outside_support
#print axioms outside_payload
#print axioms scan_append
#print axioms scan_parity
#print axioms parity_count
#print axioms scan_count
#print axioms orientation_sign

end TFQM.DegreeRepair
