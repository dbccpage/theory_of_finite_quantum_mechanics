import Mathlib.Data.Nat.Choose.Basic

/-! AuthorityEffect: None. Digits are least significant first here, the reverse
of the Rust Vec. This model proves range, exact successor, maximal exhaustion
and rank injectivity, not extracted Rust or allocator crash freedom. -/
namespace TFQM.CartesianWords

def Valid (base : Nat) (word : List Nat) : Prop := ∀ digit ∈ word, digit < base

def value (base : Nat) : List Nat → Nat
  | [] => 0
  | digit :: tail => digit + base * value base tail

def advance (base : Nat) : List Nat → Option (List Nat)
  | [] => none
  | digit :: tail => if digit + 1 < base then some ((digit + 1) :: tail)
      else (advance base tail).map (0 :: ·)

theorem value_bound (base : Nat) (word : List Nat) (h : Valid base word) :
    value base word < base ^ word.length := by
  induction word with
  | nil => simp [value]
  | cons digit tail ih =>
    have hd : digit < base := h digit (by simp)
    have ht : Valid base tail := fun d hm => h d (by simp [hm])
    have hb := Nat.mul_le_mul_left base (Nat.succ_le_of_lt (ih ht))
    simp only [Nat.mul_add, Nat.mul_one] at hb
    simp only [value, List.length_cons, Nat.pow_succ]
    rw [Nat.mul_comm (base ^ tail.length) base]
    omega

theorem advance_success (base : Nat) (word next : List Nat)
    (hv : Valid base word) (hs : advance base word = some next) :
    next.length = word.length ∧ Valid base next ∧ value base next = value base word + 1 := by
  induction word generalizing next with
  | nil => simp [advance] at hs
  | cons digit tail ih =>
    have hd : digit < base := hv digit (by simp)
    have ht : Valid base tail := fun d hm => hv d (by simp [hm])
    by_cases hi : digit + 1 < base
    · simp only [advance, hi, ↓reduceIte, Option.some.injEq] at hs
      subst next
      refine ⟨rfl, ?_, ?_⟩
      · intro d hm
        simp only [List.mem_cons] at hm
        rcases hm with rfl | hm
        · exact hi
        · exact ht d hm
      · simp only [value]
        omega
    · have he : digit + 1 = base := by omega
      cases hp : advance base tail with
      | none => simp [advance, hi, hp] at hs
      | some result =>
        simp only [advance, hi, ↓reduceIte, hp, Option.map_some, Option.some.injEq] at hs
        subst next
        obtain ⟨hlen, hvalid, hvalue⟩ := ih result ht hp
        refine ⟨by simp [hlen], ?_, ?_⟩
        · intro d hm
          simp only [List.mem_cons] at hm
          rcases hm with rfl | hm
          · omega
          · exact hvalid d hm
        · simp only [value, Nat.zero_add, hvalue, Nat.mul_add, Nat.mul_one]
          omega

theorem exhausted_value (base : Nat) (word : List Nat)
    (hv : Valid base word) (hs : advance base word = none) :
    value base word + 1 = base ^ word.length := by
  induction word with
  | nil => simp [value]
  | cons digit tail ih =>
    have hd : digit < base := hv digit (by simp)
    have ht : Valid base tail := fun d hm => hv d (by simp [hm])
    by_cases hi : digit + 1 < base
    · simp [advance, hi] at hs
    · have he : digit + 1 = base := by omega
      have hp : advance base tail = none := by
        cases htstep : advance base tail with
        | none => rfl
        | some result => simp [advance, hi, htstep] at hs
      have heq := ih ht hp
      calc
        value base (digit :: tail) + 1 = base * (value base tail + 1) := by
          simp only [value, Nat.mul_add, Nat.mul_one]
          omega
        _ = base * base ^ tail.length := by rw [heq]
        _ = base ^ (digit :: tail).length := by simp [Nat.pow_succ, Nat.mul_comm]

theorem exhausted_iff (base : Nat) (word : List Nat) (hv : Valid base word) :
    advance base word = none ↔ value base word + 1 = base ^ word.length := by
  constructor
  · exact exhausted_value base word hv
  · intro h
    cases hs : advance base word with
    | none => rfl
    | some next =>
      obtain ⟨hlen, hn, he⟩ := advance_success base word next hv hs
      have hb := value_bound base next hn
      rw [hlen, he, h] at hb
      exact (Nat.lt_irrefl _ hb).elim

theorem digit_remainder (base digit : Nat) (tail : List Nat) (hd : digit < base) :
    value base (digit :: tail) % base = digit := by
  simp [value, Nat.add_mod, Nat.mod_eq_of_lt hd]

theorem tail_quotient (base digit : Nat) (tail : List Nat) (hd : digit < base) :
    value base (digit :: tail) / base = value base tail := by
  simp [value, Nat.add_mul_div_left _ _ (by omega : 0 < base), Nat.div_eq_of_lt hd]

theorem value_injective (base : Nat) (left right : List Nat)
    (hl : Valid base left) (hr : Valid base right) (hlen : left.length = right.length)
    (he : value base left = value base right) : left = right := by
  induction left generalizing right with
  | nil => simpa using hlen.symm
  | cons digit tail ih =>
    cases right with
    | nil => simp at hlen
    | cons other rest =>
      have hd : digit < base := hl digit (by simp)
      have ho : other < base := hr other (by simp)
      have heq : digit = other := by
        have := congrArg (· % base) he
        simpa only [digit_remainder base digit tail hd, digit_remainder base other rest ho] using this
      have htail : value base tail = value base rest := by
        have := congrArg (· / base) he
        simpa only [tail_quotient base digit tail hd, tail_quotient base other rest ho] using this
      have ht : Valid base tail := fun d hm => hl d (by simp [hm])
      have hs : Valid base rest := fun d hm => hr d (by simp [hm])
      have hlen' : tail.length = rest.length := by simpa using hlen
      rw [heq, ih rest ht hs hlen' htail]

theorem nullary_count (base : Nat) : base ^ 0 = 1 := Nat.pow_zero base
theorem empty_alphabet (width : Nat) (hw : 0 < width) : 0 ^ width = 0 := by simp [Nat.ne_of_gt hw]
theorem width_admitted (width caller hard : Nat) :
    width ≤ min caller hard ↔ width ≤ caller ∧ width ≤ hard := by omega
theorem increment_fits (base digit bound : Nat) (hd : digit < base) (hb : base ≤ bound) :
    digit + 1 ≤ bound := by omega

#print axioms value_bound
#print axioms advance_success
#print axioms exhausted_value
#print axioms exhausted_iff
#print axioms digit_remainder
#print axioms tail_quotient
#print axioms value_injective
#print axioms nullary_count
#print axioms empty_alphabet
#print axioms width_admitted
#print axioms increment_fits
end TFQM.CartesianWords
