import Mathlib.Data.Finset.Image
import HistoryReport

/-!
# Finite distinguishability and report fibers (CT-FINITE-DISTINGUISHABILITY-REPORT-FIBERS)

AuthorityEffect: None.
Scope: Finite sets `X`, report maps `q : X → R`, and pairs of attributes `A, B : Finset X`.
Proves that two attributes `A` and `B` are separated by a deterministic binary task `f : R → Bool`
(`f (q a) = false` on `A` and `f (q b) = true` on `B`) if and only if their report images `A.image q`
and `B.image q` are disjoint, links the forward direction to `HistoryReport.FiberConstant`, and
executes the exhaustive check over all `(q, A, B)` with `|X| ≤ 4` and `|R| ≤ 3`.
-/

namespace FrontierDistinguishability

variable {X R : Type*}

/-- Two attributes `A` and `B` of `X` are separated through `q : X → R` by a deterministic binary task
`f : R → Bool` when `f (q a) = false` for all `a ∈ A` and `f (q b) = true` for all `b ∈ B`. -/
def SeparatedByTask (q : X → R) (A B : Finset X) : Prop :=
  ∃ f : R → Bool, (∀ a ∈ A, f (q a) = false) ∧ (∀ b ∈ B, f (q b) = true)

/-- Forward direction: if a deterministic binary task separates `A` and `B` through `q`, then
the report images `A.image q` and `B.image q` are disjoint. -/
theorem separatedByTask_imp_disjoint_image [DecidableEq R] {q : X → R} {A B : Finset X}
    (h : SeparatedByTask q A B) : Disjoint (A.image q) (B.image q) := by
  rcases h with ⟨f, hA, hB⟩
  rw [Finset.disjoint_left]
  intro r hrA hrB
  rcases Finset.mem_image.mp hrA with ⟨a, ha, rfl⟩
  rcases Finset.mem_image.mp hrB with ⟨b, hb, hqb⟩
  have h0 : f (q a) = false := hA a ha
  have h1 : f (q a) = true := by rw [← hqb]; exact hB b hb
  rw [h0] at h1
  cases h1

/-- Reverse direction: if `A.image q` and `B.image q` are disjoint, the indicator of `B.image q`
is a deterministic binary task separating `A` and `B`. -/
theorem disjoint_image_imp_separatedByTask [DecidableEq R] {q : X → R} {A B : Finset X}
    (h : Disjoint (A.image q) (B.image q)) : SeparatedByTask q A B := by
  refine ⟨fun r => decide (r ∈ B.image q), ?_, ?_⟩
  · intro a ha
    have hqa : q a ∈ A.image q := Finset.mem_image_of_mem q ha
    have hnot : q a ∉ B.image q := Finset.disjoint_left.mp h hqa
    exact decide_eq_false hnot
  · intro b hb
    have hqb : q b ∈ B.image q := Finset.mem_image_of_mem q hb
    exact decide_eq_true hqb

/-- Biconditional: two attributes `A` and `B` are separated by a deterministic binary task through `q`
if and only if their report images `A.image q` and `B.image q` are disjoint. -/
theorem separatedByTask_iff_disjoint_image [DecidableEq R] (q : X → R) (A B : Finset X) :
    SeparatedByTask q A B ↔ Disjoint (A.image q) (B.image q) :=
  ⟨separatedByTask_imp_disjoint_image, disjoint_image_imp_separatedByTask⟩

/-- Connection to `HistoryReport.FiberConstant`: when `A.image q` and `B.image q` are disjoint,
the indicator of `B` on the subtype `{x // x ∈ A ∪ B}` is constant on fibers of `q`. -/
theorem fiberConstant_indicator_of_disjoint_image [DecidableEq X] [DecidableEq R]
    (q : X → R) (A B : Finset X) (h : Disjoint (A.image q) (B.image q)) :
    HistoryReport.FiberConstant
      (fun x : {x : X // x ∈ A ∪ B} => q x.1)
      (fun x : {x : X // x ∈ A ∪ B} => decide (x.1 ∈ B)) := by
  rcases disjoint_image_imp_separatedByTask h with ⟨f, hA, hB⟩
  have hfactor : ∀ x : {x : X // x ∈ A ∪ B},
      f (q x.1) = decide (x.1 ∈ B) := by
    intro ⟨x, hx⟩
    rcases Finset.mem_union.mp hx with hxA | hxB
    · have hf0 : f (q x) = false := hA x hxA
      have hxnotB : x ∉ B := by
        intro hxB
        have h1 : f (q x) = true := hB x hxB
        rw [hf0] at h1
        cases h1
      rw [hf0, decide_eq_false hxnotB]
    · rw [hB x hxB, decide_eq_true hxB]
  intro x y hq
  dsimp at hq ⊢
  rw [← hfactor x, ← hfactor y, hq]

/-- Executable bitmask check for a fixed carrier size `n`, report codomain size `m`,
encoded report table `qCode < m^n`, and nonempty attribute bitmasks `maskA, maskB ∈ [1, 2^n - 1]`. -/
def decodeReport (m : Nat) (qCode : Nat) (x : Nat) : Nat :=
  (qCode / (m ^ x)) % m

def inMask (mask x : Nat) : Bool :=
  ((mask >>> x) &&& 1) == 1

def imageMask (n m qCode mask : Nat) : Nat :=
  (List.range n).foldl
    (fun acc x => if inMask mask x then acc ||| (1 <<< decodeReport m qCode x) else acc)
    0

def imagesDisjointBool (n m qCode maskA maskB : Nat) : Bool :=
  (imageMask n m qCode maskA &&& imageMask n m qCode maskB) == 0

def taskSeparatesImgsBool (imgA imgB fMask : Nat) : Bool :=
  ((fMask &&& imgA) == 0) && ((fMask &&& imgB) == imgB)

def existsSeparatingTaskImgsBool (m imgA imgB : Nat) : Bool :=
  (List.range (2 ^ m)).any fun fMask =>
    taskSeparatesImgsBool imgA imgB fMask

def checkPairSizes (n m : Nat) : Bool :=
  let numMasks := 2 ^ n
  let nonEmptyMasks := (List.range (numMasks - 1)).map (· + 1)
  (List.range (m ^ n)).all fun qCode =>
    let imgs := nonEmptyMasks.map (imageMask n m qCode)
    imgs.all fun imgA =>
      imgs.all fun imgB =>
        existsSeparatingTaskImgsBool m imgA imgB == ((imgA &&& imgB) == 0)

set_option maxRecDepth 20000 in
set_option maxHeartbeats 800000 in
/-- Exhaustive verification over all `(q, A, B)` with nonempty `A, B ⊆ X` for all `1 ≤ |X| ≤ 4`
and `1 ≤ |R| ≤ 3`. -/
theorem exhaustive_distinguishability_check_le4_le3 :
    checkPairSizes 1 1 = true ∧
    checkPairSizes 1 2 = true ∧
    checkPairSizes 1 3 = true ∧
    checkPairSizes 2 1 = true ∧
    checkPairSizes 2 2 = true ∧
    checkPairSizes 2 3 = true ∧
    checkPairSizes 3 1 = true ∧
    checkPairSizes 3 2 = true ∧
    checkPairSizes 3 3 = true ∧
    checkPairSizes 4 1 = true ∧
    checkPairSizes 4 2 = true ∧
    checkPairSizes 4 3 = true := by
  decide

end FrontierDistinguishability

#print axioms FrontierDistinguishability.separatedByTask_imp_disjoint_image
#print axioms FrontierDistinguishability.disjoint_image_imp_separatedByTask
#print axioms FrontierDistinguishability.separatedByTask_iff_disjoint_image
#print axioms FrontierDistinguishability.fiberConstant_indicator_of_disjoint_image
#print axioms FrontierDistinguishability.exhaustive_distinguishability_check_le4_le3

private def l5aProvenance : String :=
  "Origin: lean4/FrontierDistinguishability.lean Claim: separatedByTask_iff_disjoint_image AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
