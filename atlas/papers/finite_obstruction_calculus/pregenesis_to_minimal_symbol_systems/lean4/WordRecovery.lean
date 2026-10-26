import Paper

/-! The separate word and language contracts in sections 11-12. These are
explicit encoders, partial recoveries, total erasures and renamings, rather than
one unspecified inverse operation. -/
namespace PreMssn.WordRecovery
universe u v

def digitCode (d : Fin 10) : List Bool :=
  [d.val.testBit 3, d.val.testBit 2, d.val.testBit 1, d.val.testBit 0]

def digitValue (a b c d : Bool) : Nat :=
  (if a then 8 else 0) + (if b then 4 else 0) + (if c then 2 else 0) + (if d then 1 else 0)

def decodeDigit (a b c d : Bool) : Option (Fin 10) :=
  if h : digitValue a b c d < 10 then some ⟨digitValue a b c d, h⟩ else none

theorem decode_encoded_digit (d : Fin 10) :
    decodeDigit (d.val.testBit 3) (d.val.testBit 2) (d.val.testBit 1) (d.val.testBit 0) = some d := by
  have all : ∀ d : Fin 10,
      decodeDigit (d.val.testBit 3) (d.val.testBit 2) (d.val.testBit 1) (d.val.testBit 0) = some d := by
    decide +kernel
  exact all d

def encodeDecimal (word : List (Fin 10)) : List Bool := word.flatMap digitCode

def decodeDecimal : List Bool → Option (List (Fin 10))
  | [] => some []
  | a :: b :: c :: d :: rest => do
    let digit ← decodeDigit a b c d
    let tail ← decodeDecimal rest
    return digit :: tail
  | _ => none

theorem decimal_roundtrip (word : List (Fin 10)) :
    decodeDecimal (encodeDecimal word) = some word := by
  induction word with
  | nil => rfl
  | cons d word ih =>
    change decodeDecimal (digitCode d ++ encodeDecimal word) = some (d :: word)
    simp only [digitCode, List.cons_append, List.nil_append, decodeDecimal, decode_encoded_digit]
    change (do let tail ← decodeDecimal (encodeDecimal word); return d :: tail) = some (d :: word)
    rw [ih]
    rfl

theorem decimal_encoding_injective (x y : List (Fin 10))
    (h : encodeDecimal x = encodeDecimal y) : x = y := by
  have back := congrArg decodeDecimal h
  rw [decimal_roundtrip, decimal_roundtrip] at back
  exact Option.some.inj back

theorem decimal_encoding_append (x y : List (Fin 10)) :
    encodeDecimal (x++y) = encodeDecimal x ++ encodeDecimal y := List.flatMap_append

theorem decimal_encoding_length (word : List (Fin 10)) :
    (encodeDecimal word).length = 4 * word.length := by
  induction word with
  | nil => rfl
  | cons d word ih =>
    simp only [encodeDecimal, List.flatMap_cons, List.length_append, digitCode,
      List.length_cons, List.length_nil] at *
    omega

theorem decimal_encoding_not_surjective :
    ¬∀ bits : List Bool, ∃ word, encodeDecimal word = bits := by
  intro onto
  obtain ⟨word, h⟩ := onto [false]
  have size := congrArg List.length h
  rw [decimal_encoding_length] at size
  change 4 * word.length = 1 at size
  omega

theorem map_injective {A : Type u} {B : Type v} (f : A → B)
    (injective : ∀ a b, f a = f b → a = b) (x y : List A)
    (h : x.map f = y.map f) : x = y := by
  induction x generalizing y with
  | nil =>
    cases y with
    | nil => rfl
    | cons b y => contradiction
  | cons a x ih =>
    cases y with
    | nil => contradiction
    | cons b y =>
      have head := injective a b (List.cons.inj h).1
      have tail := ih y (List.cons.inj h).2
      rw [head, tail]

theorem renaming_inverse_iff_bijective {A : Type u} {B : Type v} (f : A → B) :
    (∃ g : B → A, (∀ a, g (f a) = a) ∧ (∀ b, f (g b) = b)) ↔
    ((∀ a a', f a = f a' → a = a') ∧ (∀ b, ∃ a, f a = b)) := by
  constructor
  · rintro ⟨g, left, right⟩
    refine ⟨?_, fun b => ⟨g b, right b⟩⟩
    intro a a' h
    rw [← left a, ← left a', h]
  · rintro ⟨injective, onto⟩
    classical
    let g : B → A := fun b => Classical.choose (onto b)
    have right : ∀ b, f (g b) = b := fun b => Classical.choose_spec (onto b)
    exact ⟨g, fun a => injective _ _ (right (f a)), right⟩

theorem renaming_word_roundtrip {A : Type u} {B : Type v} (f : A → B) (g : B → A)
    (left : ∀ a, g (f a) = a) (word : List A) : (word.map f).map g = word := by
  induction word with
  | nil => rfl
  | cons a word ih => simp only [List.map_cons, left, ih]

def Image {A : Type u} {B : Type v} (f : A → B) := {b : B // ∃ a, f a = b}
def intoImage {A : Type u} {B : Type v} (f : A → B) (a : A) : Image f :=
  ⟨f a, ⟨a, rfl⟩⟩

theorem image_recovery_iff_injective {A : Type u} {B : Type v} (f : A → B) :
    (∃ g : Image f → A, ∀ a, g (intoImage f a) = a) ↔
    (∀ a a', f a = f a' → a = a') := by
  constructor
  · rintro ⟨g, left⟩ a a' h
    have eq : intoImage f a = intoImage f a' := Subtype.ext h
    rw [← left a, ← left a', eq]
  · intro injective
    classical
    refine ⟨fun b => Classical.choose b.property, ?_⟩
    intro a
    apply injective
    exact Classical.choose_spec (intoImage f a).property

def embed {B : Type u} (old : B → Prop) (word : List {b // old b}) : List B :=
  word.map Subtype.val

theorem embed_injective {B : Type u} (old : B → Prop) (x y : List {b // old b})
    (h : embed old x = embed old y) : x = y :=
  map_injective Subtype.val (fun _ _ eq => Subtype.ext eq) x y h

def includeLanguage {B : Type u} (old : B → Prop)
    (language : List {b // old b} → Prop) (word : List B) : Prop :=
  ∃ source, embed old source = word ∧ language source

def restrictLanguage {B : Type u} (old : B → Prop)
    (language : List B → Prop) (word : List {b // old b}) : Prop :=
  language (embed old word)

theorem language_retraction {B : Type u} (old : B → Prop)
    (language : List {b // old b} → Prop) :
    restrictLanguage old (includeLanguage old language) = language := by
  funext word
  apply propext
  constructor
  · rintro ⟨source, same, h⟩
    exact (embed_injective old source word same) ▸ h
  · intro h
    exact ⟨word, rfl, h⟩

def recoverWord {B : Type u} (old : B → Prop) [DecidablePred old] :
    List B → Sum (List {b // old b}) Unit
  | [] => .inl []
  | b :: word =>
    if h : old b then
      match recoverWord old word with
      | .inl tail => .inl (⟨b, h⟩ :: tail)
      | .inr _ => .inr ()
    else .inr ()

theorem recover_old_word {B : Type u} (old : B → Prop) [DecidablePred old]
    (word : List {b // old b}) : recoverWord old (embed old word) = .inl word := by
  induction word with
  | nil => rfl
  | cons b word ih =>
    simp only [embed, List.map_cons, recoverWord, dif_pos b.property] at *
    rw [ih]

theorem recover_word_sound {B : Type u} (old : B → Prop) [DecidablePred old]
    (word : List B) (source : List {b // old b})
    (h : recoverWord old word = .inl source) : embed old source = word := by
  induction word generalizing source with
  | nil =>
    have eq : [] = source := Sum.inl.inj h
    rw [← eq]
    rfl
  | cons b word ih =>
    by_cases hb : old b
    · cases ht : recoverWord old word with
      | inl tail =>
        have eq : (⟨b, hb⟩ :: tail) = source := by simpa [recoverWord, hb, ht] using h
        rw [← eq]
        change b :: embed old tail = b :: word
        rw [ih tail ht]
      | inr refusal => simp [recoverWord, hb, ht] at h
    · simp [recoverWord, hb] at h

theorem recover_word_refuses_iff {B : Type u} (old : B → Prop) [DecidablePred old]
    (word : List B) :
    recoverWord old word = .inr () ↔ ¬∃ source, embed old source = word := by
  constructor
  · intro refused
    rintro ⟨source, same⟩
    have back := recover_old_word old source
    rw [same, refused] at back
    contradiction
  · intro offImage
    cases h : recoverWord old word with
    | inl source => exact False.elim (offImage ⟨source, recover_word_sound old word source h⟩)
    | inr refusal => cases refusal; rfl

def eraseWord {B : Type u} (old : B → Prop) [DecidablePred old]
    (word : List B) : List {b // old b} :=
  word.filterMap (fun b => if h : old b then some ⟨b, h⟩ else none)

theorem erasure_homomorphism {B : Type u} (old : B → Prop) [DecidablePred old]
    (x y : List B) : eraseWord old (x++y) = eraseWord old x ++ eraseWord old y :=
  List.filterMap_append

theorem erasure_recovers_old {B : Type u} (old : B → Prop) [DecidablePred old]
    (word : List {b // old b}) : eraseWord old (embed old word) = word := by
  induction word with
  | nil => rfl
  | cons b word ih =>
    simp only [embed, List.map_cons, eraseWord, List.filterMap_cons, dif_pos b.property] at *
    rw [ih]

theorem erasure_loses_new {B : Type u} (old : B → Prop) [DecidablePred old]
    (b : B) (new : ¬old b) : eraseWord old [b] = [] := by
  simp [eraseWord, new]

structure EdgeSyntax (A : Type u) where
  first : A
  arrow : Bool
  last : A

def decodeEdge {A : Type u} (e : EdgeSyntax A) : A × A :=
  if e.arrow then (e.first, e.last) else (e.last, e.first)

def reverseEdge {A : Type u} (e : EdgeSyntax A) : EdgeSyntax A :=
  ⟨e.last, !e.arrow, e.first⟩

theorem reverse_edge_preserves_direction {A : Type u} (e : EdgeSyntax A) :
    decodeEdge (reverseEdge e) = decodeEdge e := by
  cases e with
  | mk a direction b => cases direction <;> rfl

def reverseTrace {A : Type u} (trace : List (EdgeSyntax A)) := trace.reverse.map reverseEdge

theorem reversed_edge_list {A : Type u} (trace : List (EdgeSyntax A)) :
    (reverseTrace trace).map decodeEdge = (trace.map decodeEdge).reverse := by
  simp only [reverseTrace, List.map_map]
  have h : decodeEdge ∘ reverseEdge = (decodeEdge : EdgeSyntax A → A × A) :=
    funext reverse_edge_preserves_direction
  rw [h, List.map_reverse]

theorem reversal_preserves_edge_multiset {A : Type u} (trace : List (EdgeSyntax A)) :
    ((reverseTrace trace).map decodeEdge).Perm (trace.map decodeEdge) := by
  rw [reversed_edge_list]
  exact List.reverse_perm _

end PreMssn.WordRecovery
