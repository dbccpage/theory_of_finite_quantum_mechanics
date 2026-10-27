namespace FreshLetterRecoveryContracts

/-- One old letter and one new letter. -/
inductive Letter where
  | a
  | fresh
  deriving DecidableEq, Repr

abbrev Word := List Letter

def allOld (w : Word) : Bool :=
  w.all (fun x => decide (x = Letter.a))

/-- Language restriction: keep only words whose letters are old. Result type `List Word`. -/
def restrictLanguage (lang : List Word) : List Word :=
  lang.filter (fun w => allOld w)

/-- Partial recovery: return the word only when every letter is old. Result type `Option Word`. -/
def recoverWord (w : Word) : Option Word :=
  if allOld w then some w else none

/-- Total erasure: delete every new letter and always return a word. Result type `Word`. -/
def eraseWord (w : Word) : Word :=
  w.filter (fun x => decide (x = Letter.a))

def oldWord : Word := [Letter.a]

/-- One new letter, beside one old letter. -/
def witness : Word := [Letter.a, Letter.fresh]

def sample : List Word := [witness, oldWord]

theorem letters_are_old_or_fresh :
    ∀ x : Letter, x = Letter.a ∨ x = Letter.fresh := by
  intro x
  cases x
  · exact Or.inl rfl
  · exact Or.inr rfl

theorem fresh_is_not_old : Letter.fresh ≠ Letter.a := by
  decide

theorem witness_uses_one_fresh :
    witness = [Letter.a, Letter.fresh]
      ∧ (witness.filter (fun x => decide (x = Letter.fresh))).length = 1 := by
  decide

theorem old_word_agrees :
    recoverWord oldWord = some oldWord ∧ eraseWord oldWord = oldWord
      ∧ restrictLanguage [oldWord] = [oldWord] := by
  decide

/-- Restriction, recovery, and erasure on the witness word. -/
theorem three_contracts_differ_on_a_new_letter :
    (restrictLanguage sample : List Word) = [oldWord]
      ∧ (recoverWord witness : Option Word) = none
      ∧ (eraseWord witness : Word) = oldWord
      ∧ recoverWord witness ≠ some (eraseWord witness)
      ∧ eraseWord witness ≠ witness
      ∧ oldWord ∈ restrictLanguage sample
      ∧ witness ∉ restrictLanguage sample := by
  decide

#print axioms letters_are_old_or_fresh
#print axioms fresh_is_not_old
#print axioms witness_uses_one_fresh
#print axioms old_word_agrees
#print axioms three_contracts_differ_on_a_new_letter

end FreshLetterRecoveryContracts
