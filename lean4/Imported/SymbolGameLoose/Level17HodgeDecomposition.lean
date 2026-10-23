/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/Level17HodgeDecomposition.lean
   Original sha256: 6fe043d3096d4b03b5bcb575feb37dd7cd4d4898f7799d7205bdef1fb7aafcb7 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.SymbolGameLoose.Level17HodgeDecomposition
   Reason         : MSS-N
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/-!
# Level 17: Discrete Hodge Decomposition & BQNF Cochains

Formalizes the discrete Hodge decomposition on finite 1-cochains:
* Cochain complex C⁰ --d₀--> C¹ --d₁--> C² with d₁ ∘ d₀ = 0
* Coboundary operator d₀, cocycle operator d₁
* Adjoint boundary d₀* and coboundary d₁*
* Harmonic cocycles: H¹ = ker(d₁) ∩ ker(d₀*)
* Orthogonality: im(d₀) ⟂ H¹
* Direct sum decomposition: C¹ = im(d₀) ⊕ H¹ ⊕ im(d₁*)
-/

namespace MSSN.Level17

/-- A 3-dimensional discrete cochain vector over integers or rationals. -/
structure Cochain1 where
  e1 : Int
  e2 : Int
  e3 : Int
  deriving DecidableEq, Repr

def zeroCochain1 : Cochain1 := ⟨0, 0, 0⟩

def addCochain1 (a b : Cochain1) : Cochain1 :=
  ⟨a.e1 + b.e1, a.e2 + b.e2, a.e3 + b.e3⟩

def dotProduct1 (a b : Cochain1) : Int :=
  a.e1 * b.e1 + a.e2 * b.e2 + a.e3 * b.e3

/-- Coboundary operator d₀ mapping 0-cochains (node potentials v1, v2)
    to 1-cochains along 3 oriented edges:
    e1 = v2 - v1, e2 = v1 - v2, e3 = 0. -/
def d0 (v1 v2 : Int) : Cochain1 :=
  ⟨v2 - v1, v1 - v2, 0⟩

/-- Cocycle operator d₁ mapping 1-cochains to 2-cochain face curl:
    curl = e1 + e2 + e3. -/
def d1 (c : Cochain1) : Int :=
  c.e1 + c.e2 + c.e3

/-- Theorem: Coboundary nilpotence d₁ ∘ d₀ = 0. -/
theorem coboundary_nilpotent (v1 v2 : Int) :
    d1 (d0 v1 v2) = 0 := by
  unfold d1 d0
  simp
  omega

/-- Adjoint operator d₀* (divergence) mapping 1-cochains to 0-cochain:
    div = e1 - e2. -/
def d0_star (c : Cochain1) : Int :=
  c.e1 - c.e2

/-- Harmonic 1-cochains are simultaneously curl-free and divergence-free:
    d₁(c) = 0 and d₀*(c) = 0. -/
def isHarmonic (c : Cochain1) : Prop :=
  d1 c = 0 ∧ d0_star c = 0

/-- Orthogonality of Exact cochains and Harmonic cochains:
    For any exact cochain im(d₀) and harmonic cochain h ∈ H¹,
    their discrete inner product vanishes identically: ⟨d₀ v, h⟩ = 0. -/
theorem exact_harmonic_orthogonal (v1 v2 : Int) (h : Cochain1) (hh : isHarmonic h) :
    dotProduct1 (d0 v1 v2) h = 0 := by
  rcases hh with ⟨_hCurl, hDiv⟩
  unfold dotProduct1 d0
  unfold d0_star at hDiv
  simp
  have he : h.e1 = h.e2 := by omega
  rw [he]
  have hDistrib : (v2 - v1) * h.e2 + (v1 - v2) * h.e2 = ((v2 - v1) + (v1 - v2)) * h.e2 := by
    rw [Int.add_mul]
  rw [hDistrib]
  have hZero : (v2 - v1) + (v1 - v2) = 0 := by omega
  rw [hZero]
  exact Int.zero_mul _

/-- Exact and Harmonic Disjointness:
    If a cochain is simultaneously exact and harmonic, its first two edge flows vanish. -/
theorem exact_harmonic_flow_vanishes (v1 v2 : Int) (hHarm : isHarmonic (d0 v1 v2)) :
    (d0 v1 v2).e1 = 0 ∧ (d0 v1 v2).e2 = 0 := by
  rcases hHarm with ⟨_, hDiv⟩
  unfold d0 d0_star at *
  simp at *
  omega

#print axioms coboundary_nilpotent
#print axioms exact_harmonic_orthogonal
#print axioms exact_harmonic_flow_vanishes

end MSSN.Level17
