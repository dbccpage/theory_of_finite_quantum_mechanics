import Init

/-!
# Integral chain-certificate soundness

This module proves the algebraic consequence of checked integral chain maps and
chain homotopies. A `ChainWindow` is the three consecutive chain groups around
one degree. Its groups are actual finite integer coordinate modules; the
differentials and all certificate maps preserve addition and integer scaling.
The zero-dimensional coordinate module handles absent bottom and top groups.

This is a soundness theorem for a certificate satisfying the stated equations.
It does not construct the all-capacity schedule-complex certificates or verify
an external parser, matrix implementation, or Rust executable.
-/

namespace WitnessedDifference.GuardedChainTransport

abbrev IVec (n : Nat) := Fin n → Int

def zeroVec {n : Nat} : IVec n := fun _ => 0
def addVec {n : Nat} (x y : IVec n) : IVec n := fun j => x j + y j
def subVec {n : Nat} (x y : IVec n) : IVec n := fun j => x j - y j
def scaleVec {n : Nat} (a : Int) (x : IVec n) : IVec n := fun j => a * x j
def basisVec {n : Nat} (j : Fin n) : IVec n := fun k => if k = j then 1 else 0
def tailVec {n : Nat} (x : IVec (n + 1)) : IVec n := fun j => x j.succ
def embedTail {n : Nat} (x : IVec n) : IVec (n + 1) := Fin.cases 0 x

@[simp] theorem addVec_zero {n : Nat} (x : IVec n) : addVec x zeroVec = x := by
  funext j
  exact Int.add_zero (x j)

@[simp] theorem zeroVec_add {n : Nat} (x : IVec n) : addVec zeroVec x = x := by
  funext j
  exact Int.zero_add (x j)

@[simp] theorem scaleVec_zero {n : Nat} (x : IVec n) : scaleVec 0 x = zeroVec := by
  funext j
  exact Int.zero_mul (x j)

theorem subVec_as_add {n : Nat} (x y : IVec n) :
    subVec x y = addVec x (scaleVec (-1) y) := by
  funext j
  simp [subVec, addVec, scaleVec, Int.sub_eq_add_neg]

@[simp] theorem subVec_zero_zero {n : Nat} :
    subVec (zeroVec : IVec n) zeroVec = zeroVec := by
  funext j
  rfl

theorem addVec_subVec_cancel {n : Nat} (x y : IVec n) :
    subVec (addVec x y) y = x := by
  funext j
  exact Int.add_sub_cancel (x j) (y j)

/-- The unique vector in a rank-zero group is zero. -/
theorem empty_vector_eq_zero (x : IVec 0) : x = zeroVec := by
  funext j
  exact Fin.elim0 j

theorem embedTail_basis {n : Nat} (j : Fin n) :
    embedTail (basisVec j) = basisVec j.succ := by
  funext k
  refine Fin.cases ?_ (fun k => ?_) k
  · have h : (0 : Fin (n + 1)) ≠ j.succ := fun e => Fin.succ_ne_zero j e.symm
    change (0 : Int) = if (0 : Fin (n + 1)) = j.succ then 1 else 0
    rw [if_neg h]
  · change (if k = j then (1 : Int) else 0) =
      (if k.succ = j.succ then (1 : Int) else 0)
    by_cases h : k = j
    · rw [if_pos h, if_pos (congrArg Fin.succ h)]
    · have hs : k.succ ≠ j.succ := fun e => h (Fin.succ_inj.mp e)
      rw [if_neg h, if_neg hs]

theorem vector_head_tail {n : Nat} (x : IVec (n + 1)) :
    x = addVec (scaleVec (x 0) (basisVec 0)) (embedTail (tailVec x)) := by
  funext k
  refine Fin.cases ?_ (fun k => ?_) k
  · simp [addVec, scaleVec, basisVec, embedTail]
  · have h : k.succ ≠ (0 : Fin (n + 1)) := Fin.succ_ne_zero k
    simp [addVec, scaleVec, basisVec, embedTail, tailVec, h]

/-- A map with explicit additive and integer-linear laws. -/
structure LinearMap (m n : Nat) where
  apply : IVec m → IVec n
  map_add : ∀ x y, apply (addVec x y) = addVec (apply x) (apply y)
  map_scale : ∀ a x, apply (scaleVec a x) = scaleVec a (apply x)

namespace LinearMap

@[simp] theorem map_zero {m n : Nat} (f : LinearMap m n) :
    f.apply zeroVec = zeroVec := by
  have h := f.map_scale 0 zeroVec
  simpa only [scaleVec_zero] using h

theorem map_sub {m n : Nat} (f : LinearMap m n) (x y : IVec m) :
    f.apply (subVec x y) = subVec (f.apply x) (f.apply y) := by
  rw [subVec_as_add, f.map_add, f.map_scale, ← subVec_as_add]

def zero (m n : Nat) : LinearMap m n where
  apply := fun _ => zeroVec
  map_add := by intros; exact (zeroVec_add zeroVec).symm
  map_scale := by
    intros a x
    funext j
    exact (Int.mul_zero a).symm

def identity (n : Nat) : LinearMap n n where
  apply := id
  map_add := by intros; rfl
  map_scale := by intros; rfl

def compose {a b c : Nat} (g : LinearMap b c) (f : LinearMap a b) :
    LinearMap a c where
  apply := fun x => g.apply (f.apply x)
  map_add := by intros; rw [f.map_add, g.map_add]
  map_scale := by intros; rw [f.map_scale, g.map_scale]

def add {m n : Nat} (f g : LinearMap m n) : LinearMap m n where
  apply := fun x => addVec (f.apply x) (g.apply x)
  map_add := by
    intro x y
    rw [f.map_add, g.map_add]
    funext j
    simp only [addVec]
    omega
  map_scale := by
    intro a x
    rw [f.map_scale, g.map_scale]
    funext j
    exact (Int.mul_add a (f.apply x j) (g.apply x j)).symm

def tailEmbedding (n : Nat) : LinearMap n (n + 1) where
  apply := embedTail
  map_add := by
    intro x y
    funext j
    refine Fin.cases ?_ (fun k => ?_) j
    · rfl
    · rfl
  map_scale := by
    intro a x
    funext j
    refine Fin.cases ?_ (fun k => ?_) j
    · exact (Int.mul_zero a).symm
    · rfl

/-- Equality of the finitely many basis columns implies equality on every
integer vector. This is the algebraic basis-test contract used by a matrix
certificate checker, not an assumption of the checked universal identity. -/
theorem equal_of_equal_basis {m n : Nat} (f g : LinearMap m n)
    (basis_equal : ∀ j, f.apply (basisVec j) = g.apply (basisVec j)) :
    ∀ x, f.apply x = g.apply x := by
  induction m with
  | zero =>
    intro x
    rw [empty_vector_eq_zero x, f.map_zero, g.map_zero]
  | succ m inductionHypothesis =>
    intro x
    let ft := f.compose (tailEmbedding m)
    let gt := g.compose (tailEmbedding m)
    have tail_basis : ∀ j, ft.apply (basisVec j) = gt.apply (basisVec j) := by
      intro j
      change f.apply (embedTail (basisVec j)) = g.apply (embedTail (basisVec j))
      rw [embedTail_basis]
      exact basis_equal j.succ
    have tail_equal := inductionHypothesis ft gt tail_basis (tailVec x)
    change f.apply (embedTail (tailVec x)) = g.apply (embedTail (tailVec x)) at tail_equal
    have decomposition := vector_head_tail x
    calc
      f.apply x = f.apply (addVec (scaleVec (x 0) (basisVec 0))
          (embedTail (tailVec x))) := congrArg f.apply decomposition
      _ = addVec (scaleVec (x 0) (f.apply (basisVec 0)))
          (f.apply (embedTail (tailVec x))) := by rw [f.map_add, f.map_scale]
      _ = addVec (scaleVec (x 0) (g.apply (basisVec 0)))
          (g.apply (embedTail (tailVec x))) := by rw [basis_equal 0, tail_equal]
      _ = g.apply (addVec (scaleVec (x 0) (basisVec 0))
          (embedTail (tailVec x))) := by rw [g.map_add, g.map_scale]
      _ = g.apply x := congrArg g.apply decomposition.symm

/-- Executable equality test: compare every integer entry of every basis image. -/
def checkEqualOnBasis {m n : Nat} (f g : LinearMap m n) : Bool :=
  (List.finRange m).all fun j =>
    (List.finRange n).all fun k => decide (f.apply (basisVec j) k = g.apply (basisVec j) k)

theorem checkEqualOnBasis_sound {m n : Nat} (f g : LinearMap m n)
    (accepted : checkEqualOnBasis f g = true) : ∀ x, f.apply x = g.apply x := by
  apply equal_of_equal_basis f g
  intro j
  funext k
  unfold checkEqualOnBasis at accepted
  have columns := List.all_eq_true.mp accepted
  have rows := List.all_eq_true.mp (columns j (List.mem_finRange j))
  exact of_decide_eq_true (rows k (List.mem_finRange k))

theorem checkEqualOnBasis_complete {m n : Nat} (f g : LinearMap m n)
    (equal : ∀ x, f.apply x = g.apply x) : checkEqualOnBasis f g = true := by
  unfold checkEqualOnBasis
  apply List.all_eq_true.mpr
  intro j _
  apply List.all_eq_true.mpr
  intro k _
  apply decide_eq_true
  exact congrFun (equal (basisVec j)) k

/-- Negative control: an incorrect nonempty column is rejected. -/
theorem checker_rejects_identity_as_zero :
    checkEqualOnBasis (identity 1) (zero 1 1) = false := by decide

/-- Empty dimensions are handled by the same finite checker. -/
theorem checker_accepts_empty_identity :
    checkEqualOnBasis (identity 0) (zero 0 0) = true := by decide

end LinearMap

/-- Three consecutive finite free integral chain groups, with `down ∘ up = 0`. -/
structure ChainWindow where
  upperRank : Nat
  middleRank : Nat
  lowerRank : Nat
  up : LinearMap upperRank middleRank
  down : LinearMap middleRank lowerRank
  consecutive_zero : ∀ x, down.apply (up.apply x) = zeroVec

namespace ChainWindow

/-- Finite basis checks of the consecutive-differential identity suffice. -/
def fromBasis (u m l : Nat) (up : LinearMap u m) (down : LinearMap m l)
    (checked : ∀ j, down.apply (up.apply (basisVec j)) = zeroVec) : ChainWindow where
  upperRank := u
  middleRank := m
  lowerRank := l
  up := up
  down := down
  consecutive_zero :=
    LinearMap.equal_of_equal_basis (down.compose up) (LinearMap.zero u l) checked

def fromChecked (u m l : Nat) (up : LinearMap u m) (down : LinearMap m l)
    (accepted : LinearMap.checkEqualOnBasis (down.compose up) (LinearMap.zero u l) = true) :
    ChainWindow :=
  fromBasis u m l up down
    (fun j => LinearMap.checkEqualOnBasis_sound _ _ accepted (basisVec j))

def IsCycle (C : ChainWindow) (z : IVec C.middleRank) : Prop :=
  C.down.apply z = zeroVec

def Bounds (C : ChainWindow) (z : IVec C.middleRank) : Prop :=
  ∃ u, C.up.apply u = z

theorem boundary_is_cycle (C : ChainWindow) {z : IVec C.middleRank}
    (h : C.Bounds z) : C.IsCycle z := by
  obtain ⟨u, rfl⟩ := h
  exact C.consecutive_zero u

theorem zero_is_cycle (C : ChainWindow) : C.IsCycle zeroVec := C.down.map_zero

theorem zero_bounds (C : ChainWindow) : C.Bounds zeroVec :=
  ⟨zeroVec, C.up.map_zero⟩

theorem cycles_subtract (C : ChainWindow) {x y : IVec C.middleRank}
    (hx : C.IsCycle x) (hy : C.IsCycle y) : C.IsCycle (subVec x y) := by
  change C.down.apply (subVec x y) = zeroVec
  rw [C.down.map_sub, hx, hy, subVec_zero_zero]

theorem no_lower_group_all_cycles (C : ChainWindow) (h : C.lowerRank = 0)
    (z : IVec C.middleRank) : C.IsCycle z := by
  unfold IsCycle
  funext j
  have impossible : j.val < 0 := h ▸ j.isLt
  exact False.elim (Nat.not_lt_zero _ impossible)

theorem no_upper_group_bounds_iff_zero (C : ChainWindow) (h : C.upperRank = 0)
    (z : IVec C.middleRank) : C.Bounds z ↔ z = zeroVec := by
  constructor
  · rintro ⟨u, hu⟩
    have uz : u = zeroVec := by
      funext j
      have impossible : j.val < 0 := h ▸ j.isLt
      exact False.elim (Nat.not_lt_zero _ impossible)
    rw [uz, C.up.map_zero] at hu
    exact hu.symm
  · intro hz
    rw [hz]
    exact C.zero_bounds

end ChainWindow

/-- The two adjacent chain-map squares, around the selected degree. -/
structure ChainMap (C D : ChainWindow) where
  upper : LinearMap C.upperRank D.upperRank
  middle : LinearMap C.middleRank D.middleRank
  lower : LinearMap C.lowerRank D.lowerRank
  upper_square : ∀ u, middle.apply (C.up.apply u) = D.up.apply (upper.apply u)
  lower_square : ∀ z, D.down.apply (middle.apply z) = lower.apply (C.down.apply z)

namespace ChainMap

/-- A checker need only compare the columns in the two chain-map squares. -/
def fromBasis {C D : ChainWindow}
    (upper : LinearMap C.upperRank D.upperRank)
    (middle : LinearMap C.middleRank D.middleRank)
    (lower : LinearMap C.lowerRank D.lowerRank)
    (upper_checked : ∀ j,
      middle.apply (C.up.apply (basisVec j)) = D.up.apply (upper.apply (basisVec j)))
    (lower_checked : ∀ j,
      D.down.apply (middle.apply (basisVec j)) = lower.apply (C.down.apply (basisVec j))) :
    ChainMap C D where
  upper := upper
  middle := middle
  lower := lower
  upper_square := LinearMap.equal_of_equal_basis (middle.compose C.up)
    (D.up.compose upper) upper_checked
  lower_square := LinearMap.equal_of_equal_basis (D.down.compose middle)
    (lower.compose C.down) lower_checked

def fromChecked {C D : ChainWindow}
    (upper : LinearMap C.upperRank D.upperRank)
    (middle : LinearMap C.middleRank D.middleRank)
    (lower : LinearMap C.lowerRank D.lowerRank)
    (upper_accepted : LinearMap.checkEqualOnBasis
      (middle.compose C.up) (D.up.compose upper) = true)
    (lower_accepted : LinearMap.checkEqualOnBasis
      (D.down.compose middle) (lower.compose C.down) = true) : ChainMap C D :=
  fromBasis upper middle lower
    (fun j => LinearMap.checkEqualOnBasis_sound _ _ upper_accepted (basisVec j))
    (fun j => LinearMap.checkEqualOnBasis_sound _ _ lower_accepted (basisVec j))

theorem maps_cycle {C D : ChainWindow} (f : ChainMap C D)
    {z : IVec C.middleRank} (hz : C.IsCycle z) : D.IsCycle (f.middle.apply z) := by
  change D.down.apply (f.middle.apply z) = zeroVec
  rw [f.lower_square, hz, f.lower.map_zero]

theorem maps_boundary {C D : ChainWindow} (f : ChainMap C D)
    {z : IVec C.middleRank} (hz : C.Bounds z) : D.Bounds (f.middle.apply z) := by
  obtain ⟨u, rfl⟩ := hz
  exact ⟨f.upper.apply u, (f.upper_square u).symm⟩

end ChainMap

/-- Both homotopy equations are exact integer-vector identities.
The convention is `i p = id + d H + H d`, and likewise for `p i`. -/
structure TransportCertificate (C D : ChainWindow) where
  p : ChainMap C D
  i : ChainMap D C
  hMiddle : LinearMap C.middleRank C.upperRank
  hLower : LinearMap C.lowerRank C.middleRank
  gMiddle : LinearMap D.middleRank D.upperRank
  gLower : LinearMap D.lowerRank D.middleRank
  source_equation : ∀ z, i.middle.apply (p.middle.apply z) =
    addVec z (addVec (C.up.apply (hMiddle.apply z)) (hLower.apply (C.down.apply z)))
  target_equation : ∀ z, p.middle.apply (i.middle.apply z) =
    addVec z (addVec (D.up.apply (gMiddle.apply z)) (gLower.apply (D.down.apply z)))

namespace TransportCertificate

/-- Build the two-sided certificate from finitely many checked homotopy columns.
All maps carry explicit linear laws; no universal homotopy identity is assumed
in place of these basis checks. -/
def fromBasis {C D : ChainWindow} (p : ChainMap C D) (i : ChainMap D C)
    (hMiddle : LinearMap C.middleRank C.upperRank)
    (hLower : LinearMap C.lowerRank C.middleRank)
    (gMiddle : LinearMap D.middleRank D.upperRank)
    (gLower : LinearMap D.lowerRank D.middleRank)
    (source_checked : ∀ j, i.middle.apply (p.middle.apply (basisVec j)) =
      addVec (basisVec j)
        (addVec (C.up.apply (hMiddle.apply (basisVec j)))
          (hLower.apply (C.down.apply (basisVec j)))))
    (target_checked : ∀ j, p.middle.apply (i.middle.apply (basisVec j)) =
      addVec (basisVec j)
        (addVec (D.up.apply (gMiddle.apply (basisVec j)))
          (gLower.apply (D.down.apply (basisVec j))))) : TransportCertificate C D where
  p := p
  i := i
  hMiddle := hMiddle
  hLower := hLower
  gMiddle := gMiddle
  gLower := gLower
  source_equation := LinearMap.equal_of_equal_basis (i.middle.compose p.middle)
    ((LinearMap.identity C.middleRank).add
      ((C.up.compose hMiddle).add (hLower.compose C.down))) source_checked
  target_equation := LinearMap.equal_of_equal_basis (p.middle.compose i.middle)
    ((LinearMap.identity D.middleRank).add
      ((D.up.compose gMiddle).add (gLower.compose D.down))) target_checked

def fromChecked {C D : ChainWindow} (p : ChainMap C D) (i : ChainMap D C)
    (hMiddle : LinearMap C.middleRank C.upperRank)
    (hLower : LinearMap C.lowerRank C.middleRank)
    (gMiddle : LinearMap D.middleRank D.upperRank)
    (gLower : LinearMap D.lowerRank D.middleRank)
    (source_accepted : LinearMap.checkEqualOnBasis (i.middle.compose p.middle)
      ((LinearMap.identity C.middleRank).add
        ((C.up.compose hMiddle).add (hLower.compose C.down))) = true)
    (target_accepted : LinearMap.checkEqualOnBasis (p.middle.compose i.middle)
      ((LinearMap.identity D.middleRank).add
        ((D.up.compose gMiddle).add (gLower.compose D.down))) = true) :
    TransportCertificate C D :=
  fromBasis p i hMiddle hLower gMiddle gLower
    (fun j => LinearMap.checkEqualOnBasis_sound _ _ source_accepted (basisVec j))
    (fun j => LinearMap.checkEqualOnBasis_sound _ _ target_accepted (basisVec j))

/-- Strict retraction is the special case in which the target homotopy is zero. -/
def ofStrictRetraction {C D : ChainWindow} (p : ChainMap C D) (i : ChainMap D C)
    (hMiddle : LinearMap C.middleRank C.upperRank)
    (hLower : LinearMap C.lowerRank C.middleRank)
    (source_equation : ∀ z, i.middle.apply (p.middle.apply z) =
      addVec z (addVec (C.up.apply (hMiddle.apply z)) (hLower.apply (C.down.apply z))))
    (retraction : ∀ z, p.middle.apply (i.middle.apply z) = z) :
    TransportCertificate C D where
  p := p
  i := i
  hMiddle := hMiddle
  hLower := hLower
  gMiddle := LinearMap.zero _ _
  gLower := LinearMap.zero _ _
  source_equation := source_equation
  target_equation := by
    intro z
    simpa only [LinearMap.zero, C.up.map_zero, D.up.map_zero, addVec_zero]
      using retraction z

theorem source_cycle_equation {C D : ChainWindow} (e : TransportCertificate C D)
    {z : IVec C.middleRank} (hz : C.IsCycle z) :
    e.i.middle.apply (e.p.middle.apply z) = addVec z (C.up.apply (e.hMiddle.apply z)) := by
  rw [e.source_equation, hz, e.hLower.map_zero, addVec_zero]

theorem target_cycle_equation {C D : ChainWindow} (e : TransportCertificate C D)
    {z : IVec D.middleRank} (hz : D.IsCycle z) :
    e.p.middle.apply (e.i.middle.apply z) = addVec z (D.up.apply (e.gMiddle.apply z)) := by
  rw [e.target_equation, hz, e.gLower.map_zero, addVec_zero]

/-- The reconstructed filler, including the homotopy correction and its sign. -/
def reconstructBoundary {C D : ChainWindow} (e : TransportCertificate C D)
    (z : IVec C.middleRank) (u : IVec D.upperRank) : IVec C.upperRank :=
  subVec (e.i.upper.apply u) (e.hMiddle.apply z)

theorem reconstructed_boundary_equation {C D : ChainWindow}
    (e : TransportCertificate C D) {z : IVec C.middleRank} (hz : C.IsCycle z)
    {u : IVec D.upperRank} (hu : D.up.apply u = e.p.middle.apply z) :
    C.up.apply (e.reconstructBoundary z u) = z := by
  unfold reconstructBoundary
  rw [C.up.map_sub, ← e.i.upper_square, hu, e.source_cycle_equation hz,
    addVec_subVec_cancel]

theorem bounds_iff_report_bounds {C D : ChainWindow} (e : TransportCertificate C D)
    {z : IVec C.middleRank} (hz : C.IsCycle z) :
    C.Bounds z ↔ D.Bounds (e.p.middle.apply z) := by
  constructor
  · exact e.p.maps_boundary
  · rintro ⟨u, hu⟩
    exact ⟨e.reconstructBoundary z u, e.reconstructed_boundary_equation hz hu⟩

/-- The encoding also preserves equality of the integral homology classes of
two cycles, expressed without constructing a quotient carrier. -/
theorem homologous_iff_reports_homologous {C D : ChainWindow}
    (e : TransportCertificate C D) {x y : IVec C.middleRank}
    (hx : C.IsCycle x) (hy : C.IsCycle y) :
    C.Bounds (subVec x y) ↔ D.Bounds (subVec (e.p.middle.apply x) (e.p.middle.apply y)) := by
  have h := e.bounds_iff_report_bounds (C.cycles_subtract hx hy)
  rw [e.p.middle.map_sub] at h
  exact h

theorem source_roundtrip_homologous {C D : ChainWindow}
    (e : TransportCertificate C D) {z : IVec C.middleRank} (hz : C.IsCycle z) :
    C.Bounds (subVec (e.i.middle.apply (e.p.middle.apply z)) z) := by
  refine ⟨e.hMiddle.apply z, ?_⟩
  rw [e.source_cycle_equation hz]
  funext j
  simp only [subVec, addVec]
  omega

theorem target_roundtrip_homologous {C D : ChainWindow}
    (e : TransportCertificate C D) {z : IVec D.middleRank} (hz : D.IsCycle z) :
    D.Bounds (subVec (e.p.middle.apply (e.i.middle.apply z)) z) := by
  refine ⟨e.gMiddle.apply z, ?_⟩
  rw [e.target_cycle_equation hz]
  funext j
  simp only [subVec, addVec]
  omega

/-- Report equality preserves the protected bounds question on cycles. -/
theorem report_fiber_preserves_bounds {C D : ChainWindow}
    (e : TransportCertificate C D) {x y : IVec C.middleRank}
    (hx : C.IsCycle x) (hy : C.IsCycle y)
    (same : e.p.middle.apply x = e.p.middle.apply y) : C.Bounds x ↔ C.Bounds y := by
  rw [e.bounds_iff_report_bounds hx, e.bounds_iff_report_bounds hy, same]

theorem report_fiber_cannot_mix_answers {C D : ChainWindow}
    (e : TransportCertificate C D) {x y : IVec C.middleRank}
    (hx : C.IsCycle x) (hy : C.IsCycle y) (xb : C.Bounds x) (yn : ¬ C.Bounds y) :
    e.p.middle.apply x ≠ e.p.middle.apply y := by
  intro same
  exact yn ((e.report_fiber_preserves_bounds hx hy same).mp xb)

/-- An accepted target filler is checked by an equality, then reconstructed. -/
theorem sound_boundary_checker {C D : ChainWindow} (e : TransportCertificate C D)
    {z : IVec C.middleRank} (hz : C.IsCycle z) (u : IVec D.upperRank)
    (accepted : D.up.apply u = e.p.middle.apply z) : C.Bounds z :=
  ⟨e.reconstructBoundary z u, e.reconstructed_boundary_equation hz accepted⟩

end TransportCertificate

/-- Integer-valued linear cochains, with actual additive evaluation. -/
structure Cochain (n : Nat) where
  apply : IVec n → Int
  map_add : ∀ x y, apply (addVec x y) = apply x + apply y
  map_scale : ∀ a x, apply (scaleVec a x) = a * apply x

namespace Cochain

@[simp] theorem map_zero {n : Nat} (f : Cochain n) : f.apply zeroVec = 0 := by
  have h := f.map_scale 0 zeroVec
  simpa only [scaleVec_zero, Int.zero_mul] using h

def Closed (C : ChainWindow) (f : Cochain C.middleRank) : Prop :=
  ∀ u, f.apply (C.up.apply u) = 0

def Exact (C : ChainWindow) (f : Cochain C.middleRank) : Prop :=
  ∃ b : Cochain C.lowerRank, ∀ z, f.apply z = b.apply (C.down.apply z)

def pullback {m n : Nat} (f : Cochain n) (p : LinearMap m n) : Cochain m where
  apply := fun z => f.apply (p.apply z)
  map_add := by intros; rw [p.map_add, f.map_add]
  map_scale := by intros; rw [p.map_scale, f.map_scale]

theorem exact_is_closed (C : ChainWindow) {f : Cochain C.middleRank}
    (hf : f.Exact C) : f.Closed C := by
  obtain ⟨b, hb⟩ := hf
  intro u
  rw [hb, C.consecutive_zero, b.map_zero]

theorem closed_zero_on_boundary (C : ChainWindow) {f : Cochain C.middleRank}
    (hf : f.Closed C) {z : IVec C.middleRank} (hz : C.Bounds z) : f.apply z = 0 := by
  obtain ⟨u, rfl⟩ := hz
  exact hf u

theorem exact_zero_on_cycle (C : ChainWindow) {f : Cochain C.middleRank}
    (hf : f.Exact C) {z : IVec C.middleRank} (hz : C.IsCycle z) : f.apply z = 0 := by
  obtain ⟨b, hb⟩ := hf
  rw [hb, hz, b.map_zero]

theorem nonzero_pairing_not_boundary (C : ChainWindow) {f : Cochain C.middleRank}
    (hf : f.Closed C) {z : IVec C.middleRank} (hne : f.apply z ≠ 0) : ¬ C.Bounds z := by
  intro hz
  exact hne (closed_zero_on_boundary C hf hz)

theorem nonzero_pairing_not_exact (C : ChainWindow) {f : Cochain C.middleRank}
    {z : IVec C.middleRank} (hz : C.IsCycle z) (hne : f.apply z ≠ 0) : ¬ f.Exact C := by
  intro hf
  exact hne (exact_zero_on_cycle C hf hz)

theorem pullback_closed {C D : ChainWindow} (p : ChainMap C D)
    {f : Cochain D.middleRank} (hf : f.Closed D) : (f.pullback p.middle).Closed C := by
  intro u
  change f.apply (p.middle.apply (C.up.apply u)) = 0
  rw [p.upper_square]
  exact hf (p.upper.apply u)

/-- Pullback preserves the specified repair differential, hence exactness. -/
theorem pullback_exact {C D : ChainWindow} (p : ChainMap C D)
    {f : Cochain D.middleRank} (hf : f.Exact D) : (f.pullback p.middle).Exact C := by
  obtain ⟨b, hb⟩ := hf
  refine ⟨b.pullback p.lower, ?_⟩
  intro z
  change f.apply (p.middle.apply z) = b.apply (p.lower.apply (C.down.apply z))
  rw [hb, p.lower_square]

end Cochain

namespace TransportCertificate

/-- Under an exact retraction even arbitrary cochains and chains have identical
evaluation after pushforward and pullback. Closedness is needed for the
obstruction conclusions, not for this stronger retraction identity. -/
theorem strict_pairing_preserved {C D : ChainWindow} (p : ChainMap C D)
    (i : ChainMap D C) (retraction : ∀ z, p.middle.apply (i.middle.apply z) = z)
    (f : Cochain D.middleRank) (z : IVec D.middleRank) :
    (f.pullback p.middle).apply (i.middle.apply z) = f.apply z := by
  change f.apply (p.middle.apply (i.middle.apply z)) = f.apply z
  rw [retraction]

/-- Closed cochain evaluation is preserved as an exact integer, not just a sign. -/
theorem pairing_preserved {C D : ChainWindow} (e : TransportCertificate C D)
    {f : Cochain D.middleRank} (hf : f.Closed D)
    {z : IVec D.middleRank} (hz : D.IsCycle z) :
    (f.pullback e.p.middle).apply (e.i.middle.apply z) = f.apply z := by
  change f.apply (e.p.middle.apply (e.i.middle.apply z)) = f.apply z
  rw [e.target_cycle_equation hz, f.map_add, hf, Int.add_zero]

theorem pairing_preserved_value {C D : ChainWindow} (e : TransportCertificate C D)
    {f : Cochain D.middleRank} (hf : f.Closed D)
    {z : IVec D.middleRank} (hz : D.IsCycle z) {value : Int} (hv : f.apply z = value) :
    (f.pullback e.p.middle).apply (e.i.middle.apply z) = value := by
  rw [e.pairing_preserved hf hz, hv]

/-- The transported witness is a cycle and cocycle with the same nonzero value;
it obstructs both being a boundary and being an exact cochain. -/
theorem transported_obstruction {C D : ChainWindow} (e : TransportCertificate C D)
    {f : Cochain D.middleRank} (hf : f.Closed D)
    {z : IVec D.middleRank} (hz : D.IsCycle z) (hne : f.apply z ≠ 0) :
    C.IsCycle (e.i.middle.apply z) ∧
    (f.pullback e.p.middle).Closed C ∧
    (f.pullback e.p.middle).apply (e.i.middle.apply z) = f.apply z ∧
    ¬ C.Bounds (e.i.middle.apply z) ∧ ¬ (f.pullback e.p.middle).Exact C := by
  have hc := e.i.maps_cycle hz
  have hf' := Cochain.pullback_closed e.p hf
  have hp := e.pairing_preserved hf hz
  have hn : (f.pullback e.p.middle).apply (e.i.middle.apply z) ≠ 0 := by
    rw [hp]
    exact hne
  exact ⟨hc, hf', hp, Cochain.nonzero_pairing_not_boundary C hf' hn,
    Cochain.nonzero_pairing_not_exact C hc hn⟩

end TransportCertificate

end WitnessedDifference.GuardedChainTransport
