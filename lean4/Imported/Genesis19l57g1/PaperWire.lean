/- Imported from the sibling atlas so that this repository carries its own Lean evidence.
   Original path : omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/PaperWire.lean
   Original sha256: 4923b0f88a304ba97fae296eae71618f2d0162d84bdcc7b242f9cc9379883014 (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.Genesis19l57g1.PaperWire
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.Genesis19l57g1.PaperCanonical
import Init.Data.List.TakeDrop
import Init.Data.UInt.Lemmas

/-! The actual version-1 wire layout: length-prefixed structural fields,
followed by unsigned 64-bit big-endian words. No search hypotheses are used
to establish that the encoding retains the supplied structural tuple. -/

namespace GenesisPaper.Wire

open Derivation

def readMany {A S : Type} (read : List S → Option (A × List S)) :
    Nat → List S → Option (List A × List S)
  | 0, input => some ([], input)
  | n + 1, input => do
      let (a, rest) ← read input
      let (as, tail) ← readMany read n rest
      pure (a :: as, tail)

theorem readMany_encode_append {A S : Type}
    (read : List S → Option (A × List S)) (encode : A → List S)
    (xs : List A)
    (h : ∀ x ∈ xs, ∀ tail, read (encode x ++ tail) = some (x, tail))
    (tail : List S) :
    readMany read xs.length (xs.flatMap encode ++ tail) = some (xs, tail) := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
      simp only [List.length_cons, List.flatMap_cons, List.append_assoc, readMany]
      rw [h x (by simp)]
      change (do
        let (as, rest) ← readMany read xs.length (xs.flatMap encode ++ tail)
        pure (x :: as, rest)) = some (x :: xs, tail)
      rw [ih (fun y hy => h y (by simp [hy]))]
      rfl

def counted (xs : List Nat) : List Nat := xs.length :: xs

def readCounted : List Nat → Option (List Nat × List Nat)
  | [] => none
  | n :: rest =>
      if n ≤ rest.length then some (rest.take n, rest.drop n) else none

theorem readCounted_append (xs tail : List Nat) :
    readCounted (counted xs ++ tail) = some (xs, tail) := by
  simp [counted, readCounted]

def instWords (p : Inst) : List Nat := p.1 :: counted p.2

def readInst : List Nat → Option (Inst × List Nat)
  | [] => none
  | f :: rest => do
      let (args, tail) ← readCounted rest
      pure ((f, args), tail)

theorem readInst_append (p : Inst) (tail : List Nat) :
    readInst (instWords p ++ tail) = some (p, tail) := by
  rcases p with ⟨f, args⟩
  simp [instWords, readInst, readCounted_append]

def pairWords (p : Nat × Nat) : List Nat := [p.1, p.2]

def readPair : List Nat → Option ((Nat × Nat) × List Nat)
  | a :: b :: rest => some ((a, b), rest)
  | _ => none

theorem readPair_append (p : Nat × Nat) (tail : List Nat) :
    readPair (pairWords p ++ tail) = some (p, tail) := by
  rcases p with ⟨a, b⟩
  rfl

def collectionWords {A : Type} (encode : A → List Nat) (xs : List A) : List Nat :=
  xs.length :: xs.flatMap encode

def readCollection {A : Type} (read : List Nat → Option (A × List Nat)) :
    List Nat → Option (List A × List Nat)
  | [] => none
  | n :: rest => readMany read n rest

theorem readCollection_append {A : Type}
    (read : List Nat → Option (A × List Nat)) (encode : A → List Nat)
    (h : ∀ x tail, read (encode x ++ tail) = some (x, tail))
    (xs : List A) (tail : List Nat) :
    readCollection read (collectionWords encode xs ++ tail) = some (xs, tail) := by
  exact readMany_encode_append read encode xs (fun x _ => h x) tail

def structuralWords (key : StructuralKey) : List Nat :=
  key.1 :: (counted key.2.1 ++ collectionWords instWords key.2.2.1 ++
    counted key.2.2.2.1 ++ collectionWords pairWords key.2.2.2.2)

def readStructural : List Nat → Option (StructuralKey × List Nat)
  | [] => none
  | n :: rest => do
      let (forms, rest) ← readCounted rest
      let (insts, rest) ← readCollection readInst rest
      let (rules, rest) ← readCounted rest
      let (reqs, rest) ← readCollection readPair rest
      pure ((n, forms, insts, rules, reqs), rest)

theorem readStructural_append (key : StructuralKey) (tail : List Nat) :
    readStructural (structuralWords key ++ tail) = some (key, tail) := by
  rcases key with ⟨n, forms, insts, rules, reqs⟩
  simp [structuralWords, List.cons_append, List.append_assoc, readStructural,
    readCounted_append, readCollection_append readInst instWords readInst_append,
    readCollection_append readPair pairWords readPair_append]

theorem structuralWords_injective {r s : StructuralKey}
    (h : structuralWords r = structuralWords s) : r = s := by
  have := congrArg (fun words => readStructural (words ++ [])) h
  simpa only [readStructural_append, Option.some.injEq, Prod.mk.injEq, and_true] using this

def digitsLE : Nat → Nat → List UInt8
  | 0, _ => []
  | width + 1, value => UInt8.ofNat (value % 256) :: digitsLE width (value / 256)

def valueLE : List UInt8 → Nat
  | [] => 0
  | byte :: rest => byte.toNat + 256 * valueLE rest

theorem digitsLE_length (width value : Nat) : (digitsLE width value).length = width := by
  induction width generalizing value with
  | zero => rfl
  | succ width ih => simp [digitsLE, ih]

theorem valueLE_digitsLE (width value : Nat) (h : value < 256 ^ width) :
    valueLE (digitsLE width value) = value := by
  induction width generalizing value with
  | zero =>
      have : value = 0 := by simpa using h
      simp [digitsLE, valueLE, this]
  | succ width ih =>
      have hdiv : value / 256 < 256 ^ width := by
        apply (Nat.div_lt_iff_lt_mul (by decide : 0 < 256)).mpr
        simpa [Nat.pow_succ, Nat.mul_comm] using h
      simp only [digitsLE, valueLE]
      rw [UInt8.toNat_ofNat_of_lt' (Nat.mod_lt _ (by decide)), ih _ hdiv]
      exact Nat.mod_add_div value 256

def word64 (value : Nat) : List UInt8 := (digitsLE 8 value).reverse

def readWord64 (input : List UInt8) : Option (Nat × List UInt8) :=
  if 8 ≤ input.length then
    some (valueLE (input.take 8).reverse, input.drop 8)
  else none

theorem word64_length (value : Nat) : (word64 value).length = 8 := by
  simp [word64, digitsLE_length]

theorem readWord64_append (value : Nat) (h : value < 2 ^ 64) (tail : List UInt8) :
    readWord64 (word64 value ++ tail) = some (value, tail) := by
  have hvalue : value < 256 ^ 8 := by simpa using h
  have roundtrip : valueLE (word64 value).reverse = value := by
    simp only [word64, List.reverse_reverse]
    exact valueLE_digitsLE 8 value hvalue
  have hlen := word64_length value
  simp only [readWord64, List.length_append, hlen, Nat.le_add_right, ↓reduceIte]
  rw [← hlen, List.take_append, List.take_length, Nat.sub_self, List.take_zero,
    List.append_nil, List.drop_append, List.drop_length, Nat.sub_self,
    List.drop_zero, List.nil_append, roundtrip]

def bytes (words : List Nat) : List UInt8 := words.flatMap word64

theorem bytes_length (words : List Nat) : (bytes words).length = 8 * words.length := by
  induction words with
  | nil => rfl
  | cons x xs ih => simp [bytes, List.flatMap_cons, word64_length, ← ih, Nat.mul_add, Nat.add_comm]

theorem readBytes_append (words : List Nat) (bounded : ∀ x ∈ words, x < 2 ^ 64)
    (tail : List UInt8) :
    readMany readWord64 words.length (bytes words ++ tail) = some (words, tail) :=
  readMany_encode_append readWord64 word64 words
    (fun x hx => readWord64_append x (bounded x hx)) tail

theorem bytes_injective {xs ys : List Nat}
    (hx : ∀ x ∈ xs, x < 2 ^ 64) (hy : ∀ y ∈ ys, y < 2 ^ 64)
    (h : bytes xs = bytes ys) : xs = ys := by
  have hlen : xs.length = ys.length := by
    have := congrArg List.length h
    rw [bytes_length, bytes_length] at this
    omega
  have decoded := congrArg (fun stream => readMany readWord64 xs.length (stream ++ [])) h
  rw [readBytes_append xs hx, hlen, readBytes_append ys hy] at decoded
  simpa only [Option.some.injEq, Prod.mk.injEq, and_true] using decoded

def wirePrefix : List UInt8 := [71, 69, 78, 69, 83, 73, 83, 45, 75, 69, 89, 0, 1]

def portableBytes (key : StructuralKey) : List UInt8 := wirePrefix ++ bytes (structuralWords key)

theorem portableBytes_injective {r s : StructuralKey}
    (hr : ∀ x ∈ structuralWords r, x < 2 ^ 64)
    (hs : ∀ x ∈ structuralWords s, x < 2 ^ 64)
    (h : portableBytes r = portableBytes s) : r = s := by
  apply structuralWords_injective
  exact bytes_injective hr hs (List.append_cancel_left h)

theorem portableBytes_sound {r s : Regime}
    (pir : DRen r.data) (phir : DRen r.forms.length)
    (pis : DRen s.data) (phis : DRen s.forms.length)
    (hr : r.wf) (hs : s.wf)
    (br : ∀ x ∈ structuralWords (serializedRelabel r pir phir), x < 2 ^ 64)
    (bs : ∀ x ∈ structuralWords (serializedRelabel s pis phis), x < 2 ^ 64)
    (heq : portableBytes (serializedRelabel r pir phir) =
      portableBytes (serializedRelabel s pis phis)) : Nonempty (Iso r s) :=
  serializedRelabel_sound pir phir pis phis hr hs (portableBytes_injective br bs heq)

end GenesisPaper.Wire
