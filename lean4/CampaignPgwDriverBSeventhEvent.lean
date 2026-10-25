/-
Narrowed boundary for PGW-DRIVER-B-SEVENTH-EVENT.
Six named labels have indices 0, 1, 2, 3, 4 and 5.
A guard accepts a natural number exactly when it is strictly less than 6.
That guard refuses 6. A guard with bound 7 accepts 6.
This module does not run the Alpha harness and does not amend a seal.
-/

inductive SealedEventKind where
  | supply
  | admitDatum
  | admitForm
  | admitInst
  | admitRuleAll
  | impose

def sealedIndex : SealedEventKind → Fin 6
  | .supply => 0
  | .admitDatum => 1
  | .admitForm => 2
  | .admitInst => 3
  | .admitRuleAll => 4
  | .impose => 5

def ofIndex : Fin 6 → SealedEventKind
  | ⟨0, _⟩ => .supply
  | ⟨1, _⟩ => .admitDatum
  | ⟨2, _⟩ => .admitForm
  | ⟨3, _⟩ => .admitInst
  | ⟨4, _⟩ => .admitRuleAll
  | ⟨5, _⟩ => .impose

def appendSealed (label : Nat) : Bool :=
  decide (label < 6)

def appendAmended (label : Nat) : Bool :=
  decide (label < 7)

theorem sealedIndex_supply : (sealedIndex .supply).val = 0 := rfl

theorem sealedIndex_admitDatum : (sealedIndex .admitDatum).val = 1 := rfl

theorem sealedIndex_admitForm : (sealedIndex .admitForm).val = 2 := rfl

theorem sealedIndex_admitInst : (sealedIndex .admitInst).val = 3 := rfl

theorem sealedIndex_admitRuleAll : (sealedIndex .admitRuleAll).val = 4 := rfl

theorem sealedIndex_impose : (sealedIndex .impose).val = 5 := rfl

theorem ofIndex_roundtrip (e : SealedEventKind) : ofIndex (sealedIndex e) = e := by
  cases e <;> rfl

theorem index_roundtrip (i : Fin 6) : sealedIndex (ofIndex i) = i := by
  rcases i with ⟨v, hv⟩
  match v with
  | 0 => rfl
  | 1 => rfl
  | 2 => rfl
  | 3 => rfl
  | 4 => rfl
  | 5 => rfl
  | n + 6 =>
    have : n + 6 < 6 := hv
    omega

theorem six_labels_admitted :
    appendSealed (sealedIndex .supply).val = true ∧
    appendSealed (sealedIndex .admitDatum).val = true ∧
    appendSealed (sealedIndex .admitForm).val = true ∧
    appendSealed (sealedIndex .admitInst).val = true ∧
    appendSealed (sealedIndex .admitRuleAll).val = true ∧
    appendSealed (sealedIndex .impose).val = true := by
  decide

theorem seventh_label_refused : appendSealed 6 = false := by
  decide

theorem amended_bound_accepts_seventh : appendAmended 6 = true := by
  decide

theorem seventh_label_not_a_sealed_index :
    ∀ e : SealedEventKind, (sealedIndex e).val ≠ 6 := by
  intro e
  cases e <;> decide

#print axioms sealedIndex_supply
#print axioms sealedIndex_admitDatum
#print axioms sealedIndex_admitForm
#print axioms sealedIndex_admitInst
#print axioms sealedIndex_admitRuleAll
#print axioms sealedIndex_impose
#print axioms ofIndex_roundtrip
#print axioms index_roundtrip
#print axioms six_labels_admitted
#print axioms seventh_label_refused
#print axioms amended_bound_accepts_seventh
#print axioms seventh_label_not_a_sealed_index
