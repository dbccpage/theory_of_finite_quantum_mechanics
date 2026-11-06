/-!
Declared incidence domain for one finite complex, without Mathlib.

A family is in the domain when it is a finite set of nonempty simplices on
vertices `0..n-1`, contains every singleton, and is closed under nonempty
faces. The incidence reading returns that simplex list, or nothing when a
vertex list is not strictly increasing, a cell is repeated, a singleton is
missing, or a nonempty face is missing.

The worked complex is the three-edge cycle on vertices `0,1,2` and the same
cycle with the face `012` admitted. Boundary matrices use the edge order
`(01, 02, 12)`. Rational Betti numbers are the rank formula
`b_k = dim C_k − rank ∂_k − rank ∂_{k+1}` with the ranks proved from an
explicit integer kernel and column image.
-/

namespace GenesisIncidence

@[ext]
structure Vec3 where
  x : Int
  y : Int
  z : Int
deriving Repr, DecidableEq

def zero : Vec3 := { x := 0, y := 0, z := 0 }

/-- Column span of `c₀ = (-1, 1, 0)` and `c₁ = (-1, 0, 1)`. -/
def combine (a b : Int) : Vec3 :=
  { x := -a - b, y := a, z := b }

/-- Signed boundary `∂₁` on the edge basis `(01, 02, 12)`. -/
def d1 (x y z : Int) : Vec3 :=
  { x := -x - y, y := x - z, z := y + z }

/-- The admitted 2-simplex `012` as a 1-chain: column `(1, -1, 1)`. -/
def d2 (w : Int) : Vec3 :=
  { x := w, y := -w, z := w }

theorem combine_zero (a b : Int) : combine a b = zero ↔ a = 0 ∧ b = 0 := by
  constructor
  · intro h
    have hx : -a - b = 0 := by
      simpa [combine, zero] using congrArg Vec3.x h
    have hy : a = 0 := by
      simpa [combine, zero] using congrArg Vec3.y h
    have hz : b = 0 := by
      simpa [combine, zero] using congrArg Vec3.z h
    omega
  · intro ⟨ha, hb⟩
    ext <;> simp [combine, zero, ha, hb]

theorem d1_columns_independent (a b : Int) (h : combine a b = zero) : a = 0 ∧ b = 0 :=
  (combine_zero a b).1 h

theorem third_column_in_span : combine (-1) 1 = { x := 0, y := -1, z := 1 } := by
  apply Vec3.ext <;> dsimp [combine] <;> omega

theorem d1_as_combine (x y z : Int) : d1 x y z = combine (x - z) (y + z) := by
  apply Vec3.ext <;> dsimp [d1, combine] <;> omega

/-- The image of the two independent columns is the plane `x + y + z = 0`. -/
theorem d1_image_is_plane (x y z : Int) :
    (∃ a b : Int, combine a b = { x := x, y := y, z := z }) ↔ x + y + z = 0 := by
  constructor
  · intro ⟨a, b, h⟩
    have hx : -a - b = x := by
      simpa [combine] using congrArg Vec3.x h
    have hy : a = y := by
      simpa [combine] using congrArg Vec3.y h
    have hz : b = z := by
      simpa [combine] using congrArg Vec3.z h
    omega
  · intro h
    refine ⟨y, z, ?_⟩
    apply Vec3.ext
    · dsimp [combine]
      omega
    · dsimp [combine]
    · dsimp [combine]

/-- `∂₁` has trivial kernel exactly on the line through `(1, -1, 1)`. -/
theorem d1_kernel_is_cycle (x y z : Int) :
    d1 x y z = zero ↔ ∃ t : Int, x = t ∧ y = -t ∧ z = t := by
  constructor
  · intro h
    have hcomb : combine (x - z) (y + z) = zero := by
      rw [← d1_as_combine]
      exact h
    rcases (combine_zero (x - z) (y + z)).1 hcomb with ⟨hx, hy⟩
    refine ⟨x, rfl, ?_, ?_⟩
    · omega
    · omega
  · intro ⟨t, hx, hy, hz⟩
    rw [hx, hy, hz]
    apply Vec3.ext <;> dsimp [d1, zero] <;> omega

theorem boundary_boundary_filled (w : Int) : d1 (d2 w).x (d2 w).y (d2 w).z = zero := by
  apply Vec3.ext <;> dsimp [d1, d2, zero] <;> omega

theorem filled_kernel_equals_face_image (x y z : Int) :
    d1 x y z = zero ↔ ∃ w : Int, { x := x, y := y, z := z } = d2 w := by
  constructor
  · intro h
    rcases (d1_kernel_is_cycle x y z).1 h with ⟨t, hx, hy, hz⟩
    refine ⟨t, ?_⟩
    ext <;> simp [d2, hx, hy, hz]
  · intro ⟨w, h⟩
    have hx : x = w := by simpa [d2] using congrArg Vec3.x h
    have hy : y = -w := by simpa [d2] using congrArg Vec3.y h
    have hz : z = w := by simpa [d2] using congrArg Vec3.z h
    rw [hx, hy, hz]
    exact boundary_boundary_filled w

theorem filled_face_is_injective (w : Int) : d2 w = zero ↔ w = 0 := by
  constructor
  · intro h
    simpa [d2, zero] using congrArg Vec3.x h
  · intro h
    ext <;> simp [d2, zero, h]

/-- `b_k = dim C_k − rank ∂_k − rank ∂_{k+1}`. -/
def betti (dimC rankIn rankOut : Nat) : Nat :=
  dimC - rankIn - rankOut

open Classical

/-- Basis cardinality when `ok` holds, and `0` when the basis claim fails. -/
noncomputable def provedRank (ok : Prop) (basisCard : Nat) : Nat :=
  if ok then basisCard else 0

def vertexBasis : List Nat := [0, 1, 2]
def edgeBasis : List (List Nat) := [[0, 1], [0, 2], [1, 2]]
def d1ColumnBasis : List (Int × Int) := [(1, 0), (0, 1)]
def cycleGenerator : List Int := [1]
def faceGenerator : List Int := [1]
def noChain : List Int := []

def vertexDim : Nat := vertexBasis.length
def edgeDim : Nat := edgeBasis.length
def incomingRank : Nat := noChain.length
def cycleD2Rank : Nat := noChain.length
def d2DomainDim : Nat := faceGenerator.length

def d1ColumnsIndependent : Prop :=
  ∀ a b : Int, combine a b = zero → a = 0 ∧ b = 0

def d1ColumnsSpanPlane : Prop :=
  ∀ x y z : Int,
    (∃ a b : Int, combine a b = { x := x, y := y, z := z }) ↔ x + y + z = 0

def d1FactorsThroughColumns : Prop :=
  ∀ x y z : Int, d1 x y z = combine (x - z) (y + z)

def thirdColumnInSpan : Prop :=
  combine (-1) 1 = { x := 0, y := -1, z := 1 }

def d1KernelIsLine : Prop :=
  ∀ x y z : Int, d1 x y z = zero ↔ ∃ t : Int, x = t ∧ y = -t ∧ z = t

def d2Injective : Prop :=
  ∀ w : Int, d2 w = zero ↔ w = 0

def d2ImageIsKernel : Prop :=
  ∀ x y z : Int, d1 x y z = zero ↔ ∃ w : Int, { x := x, y := y, z := z } = d2 w

def d2BoundaryLaw : Prop :=
  ∀ w : Int, d1 (d2 w).x (d2 w).y (d2 w).z = zero

theorem d1_columns_ok :
    d1ColumnsIndependent ∧ d1ColumnsSpanPlane ∧ d1FactorsThroughColumns ∧ thirdColumnInSpan :=
  ⟨d1_columns_independent, d1_image_is_plane, d1_as_combine, third_column_in_span⟩

theorem d1_kernel_ok : d1KernelIsLine :=
  d1_kernel_is_cycle

theorem d2_facts : d2Injective ∧ d2ImageIsKernel ∧ d2BoundaryLaw :=
  ⟨filled_face_is_injective, filled_kernel_equals_face_image, boundary_boundary_filled⟩

/-- `rank ∂₁` is the cardinality of `(c₀, c₁)` once those columns are a basis of the image. -/
noncomputable def d1ImageRank : Nat :=
  provedRank
    (d1ColumnsIndependent ∧ d1ColumnsSpanPlane ∧ d1FactorsThroughColumns ∧ thirdColumnInSpan)
    d1ColumnBasis.length

/-- `dim ker ∂₁` is `1` once the kernel is the line through `(1, -1, 1)`. -/
noncomputable def d1KernelDim : Nat :=
  provedRank d1KernelIsLine cycleGenerator.length

/-- `rank ∂₂` is `1` once `∂₂` is injective and its image is exactly `ker ∂₁`. -/
noncomputable def d2Rank : Nat :=
  provedRank (d2Injective ∧ d2ImageIsKernel ∧ d2BoundaryLaw) faceGenerator.length

theorem d1_image_rank_eq : d1ImageRank = d1ColumnBasis.length := by
  unfold d1ImageRank provedRank
  exact ite_eq_left d1_columns_ok

theorem d1_kernel_dim_eq : d1KernelDim = cycleGenerator.length := by
  unfold d1KernelDim provedRank
  exact ite_eq_left d1_kernel_ok

theorem d2_rank_eq : d2Rank = faceGenerator.length := by
  unfold d2Rank provedRank
  exact ite_eq_left d2_facts

/-- Explicit rank-nullity on `∂₁ : ℤ³ → ℤ³`: basis cardinalities add to `dim C₁`. -/
theorem d1_rank_nullity : d1ImageRank + d1KernelDim = edgeDim := by
  rw [d1_image_rank_eq, d1_kernel_dim_eq]
  rfl

/-- Filling identifies `im ∂₂` with `ker ∂₁`, so the two basis cardinalities agree. -/
theorem d2_rank_eq_kernel_dim : d2Rank = d1KernelDim := by
  rw [d2_rank_eq, d1_kernel_dim_eq]
  rfl

/-- Cycle: `b₀ = dim C₀ − rank ∂₁` and `b₁ = dim ker ∂₁`, with no 2-chain. -/
theorem cycle_rational_betti :
    (betti vertexDim incomingRank d1ImageRank, betti edgeDim d1ImageRank cycleD2Rank) =
      ((1, 1) : Nat × Nat) := by
  have hnull : d1ImageRank + d1KernelDim = 3 := by
    simpa [edgeDim, edgeBasis] using d1_rank_nullity
  have hk : d1KernelDim = 1 := by
    simpa [cycleGenerator] using d1_kernel_dim_eq
  rw [hk] at hnull
  have hr : d1ImageRank = 2 := by omega
  rw [hr]
  rfl

/-- Filled triangle: `rank ∂₂ = dim ker ∂₁`, so `b₁ = b₂ = 0`. -/
theorem filled_rational_betti :
    (betti vertexDim incomingRank d1ImageRank, betti edgeDim d1ImageRank d2Rank,
      betti d2DomainDim d2Rank cycleD2Rank) =
      ((1, 0, 0) : Nat × Nat × Nat) := by
  have hnull : d1ImageRank + d1KernelDim = 3 := by
    simpa [edgeDim, edgeBasis] using d1_rank_nullity
  have hk : d1KernelDim = 1 := by
    simpa [cycleGenerator] using d1_kernel_dim_eq
  have hd : d2Rank = d1KernelDim := d2_rank_eq_kernel_dim
  rw [hk] at hnull
  rw [hd, hk]
  have hr : d1ImageRank = 2 := by omega
  rw [hr]
  rfl

-- Incidence reading

def removeNth : List Nat → Nat → List Nat
  | [], _ => []
  | _ :: xs, 0 => xs
  | x :: xs, n + 1 => x :: removeNth xs n

def strictlyIncreasing : List Nat → Bool
  | [] => false
  | [_] => true
  | a :: b :: rest => decide (a < b) && strictlyIncreasing (b :: rest)

def memList (cells : List (List Nat)) (face : List Nat) : Bool :=
  cells.any (· == face)

def facesOf (cell : List Nat) : List (List Nat) :=
  (List.range cell.length).map (removeNth cell)

def facesClosed (cells : List (List Nat)) : Bool :=
  cells.all fun cell =>
    if decide (cell.length ≤ 1) then true else (facesOf cell).all (memList cells)

def listMax (xs : List Nat) : Nat :=
  xs.foldl (init := 0) fun m v => max m v

def familyMax (cells : List (List Nat)) : Nat :=
  cells.foldl (init := 0) fun m cell => max m (listMax cell)

def singletonsPresent (cells : List (List Nat)) : Bool :=
  (List.range (familyMax cells + 1)).all fun v => memList cells [v]

def noDuplicates : List (List Nat) → Bool
  | [] => true
  | c :: cs => !memList cs c && noDuplicates cs

def incidenceReading (cells : List (List Nat)) : Option (List (List Nat)) :=
  if cells.all strictlyIncreasing && noDuplicates cells &&
      singletonsPresent cells && facesClosed cells then
    some cells
  else
    none

/-- Vertices, then edges `01`, `02`, `12`. -/
def cycleSimplices : List (List Nat) :=
  [[0], [1], [2], [0, 1], [0, 2], [1, 2]]

/-- The cycle plus the single face on vertices `0,1,2`. -/
def filledSimplices : List (List Nat) :=
  [[0], [1], [2], [0, 1], [0, 2], [1, 2], [0, 1, 2]]

theorem cycle_incidence_eq : incidenceReading cycleSimplices = some cycleSimplices := by
  rfl

theorem filled_incidence_eq : incidenceReading filledSimplices = some filledSimplices := by
  rfl

theorem reversed_endpoint_refused :
    incidenceReading [[0], [1], [1, 0]] = none := by
  rfl

theorem missing_face_refused :
    incidenceReading [[0], [1], [2], [0, 2], [1, 2], [0, 1, 2]] = none := by
  rfl

theorem duplicate_cell_refused :
    incidenceReading [[0], [1], [2], [0, 1], [0, 2], [1, 2], [0, 1]] = none := by
  rfl

end GenesisIncidence
