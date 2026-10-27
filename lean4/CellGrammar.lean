
import CochainWindow




namespace ObstructionCore.CellGrammar

open ObstructionCore.CochainWindow

structure ChainGrammar (C0 C1 C2 : Type) where
  zero0 : C0
  boundary1 : C1 → C0
  boundary2 : C2 → C1
  boundarySquare : ∀ face, boundary1 (boundary2 face) = zero0

structure Dualization
    (C0 C1 C2 D0 D1 D2 : Type)
    (chain : ChainGrammar C0 C1 C2) where
  d0Carrier : AddCommGroupCarrier D0
  d1Carrier : AddCommGroupCarrier D1
  d2Carrier : AddCommGroupCarrier D2
  d0 : D0 → D1
  d1 : D1 → D2
  d0_zero : d0 d0Carrier.zero = d1Carrier.zero
  d0_add : ∀ x y,
    d0 (d0Carrier.add x y) = d1Carrier.add (d0 x) (d0 y)
  d1_zero : d1 d1Carrier.zero = d2Carrier.zero
  d1_add : ∀ x y,
    d1 (d1Carrier.add x y) = d2Carrier.add (d1 x) (d1 y)
  pairing0 : D0 → C0 → Int
  pairing1 : D1 → C1 → Int
  pairing2 : D2 → C2 → Int
  adjoint0 : ∀ alpha edge,
    pairing1 (d0 alpha) edge = pairing0 alpha (chain.boundary1 edge)
  adjoint1 : ∀ omega face,
    pairing2 (d1 omega) face = pairing1 omega (chain.boundary2 face)
  pairing0_zero_right : ∀ alpha, pairing0 alpha chain.zero0 = 0
  pairing2_zero_left : ∀ face, pairing2 d2Carrier.zero face = 0
  pairing2_separates : ∀ left right,
    (∀ face, pairing2 left face = pairing2 right face) → left = right

variable {C0 C1 C2 D0 D1 D2 : Type}

theorem boundarySquare_implies_cochain
    (chain : ChainGrammar C0 C1 C2)
    (dual : Dualization C0 C1 C2 D0 D1 D2 chain)
    (alpha : D0) :
    dual.d1 (dual.d0 alpha) = dual.d2Carrier.zero := by
  apply dual.pairing2_separates
  intro face
  rw [dual.adjoint1, dual.adjoint0, chain.boundarySquare]
  rw [dual.pairing0_zero_right, dual.pairing2_zero_left]

def toWindow
    (chain : ChainGrammar C0 C1 C2)
    (dual : Dualization C0 C1 C2 D0 D1 D2 chain) :
    Window D0 D1 D2 where
  c0 := dual.d0Carrier
  c1 := dual.d1Carrier
  c2 := dual.d2Carrier
  d0 := dual.d0
  d1 := dual.d1
  d0_zero := dual.d0_zero
  d0_add := dual.d0_add
  d1_zero := dual.d1_zero
  d1_add := dual.d1_add
  chain := boundarySquare_implies_cochain chain dual

theorem constructed_window_chain
    (chain : ChainGrammar C0 C1 C2)
    (dual : Dualization C0 C1 C2 D0 D1 D2 chain)
    (alpha : D0) :
    (toWindow chain dual).d1 ((toWindow chain dual).d0 alpha) =
      (toWindow chain dual).c2.zero := by
  exact (toWindow chain dual).chain alpha

#print axioms boundarySquare_implies_cochain
#print axioms constructed_window_chain

end ObstructionCore.CellGrammar

private def l5aProvenance : String :=
  "Origin: lean4/CellGrammar.lean Claim: boundarySquare_implies_cochain AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
