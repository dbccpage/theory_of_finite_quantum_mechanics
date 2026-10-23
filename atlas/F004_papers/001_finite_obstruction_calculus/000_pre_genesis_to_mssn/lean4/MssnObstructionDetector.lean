/-!
# Finite obstruction predicates and a cycle-circulation example

AuthorityEffect: None. GenesisEffect: None.
The four-gate result factors the Boolean predicate defined here. Its observation
columns are supplied lists, not a checked partition or the full Genesis passage
state. The cycle calculation proves non-exactness relative to the displayed d0.
The final candidate predicate consumes a supplied Boolean; it verifies neither
that a proposed edit resolves an obstruction nor that the edit is authorized.
-/

namespace MssnObstruction

/-- State of the primitive passage evaluator tracking witness pairs,
    protected demand pairs, and declared observation equivalence classes. -/
structure PState where
  wit : List (Nat × Nat)
  prot : List (Nat × Nat)
  obs : Option (List (List Nat))
deriving DecidableEq, Repr

/-- Auxiliary check: whether two elements share the same observation column. -/
def zeroP (cols : List (List Nat)) (i j : Nat) : Bool :=
  cols.any (fun c => c.contains i && c.contains j)

/-- Gate 1: The pair (i, j) is retained in the witness store. -/
def retainedP (s : PState) (i j : Nat) : Bool :=
  (s.wit.contains (i, j))

/-- Gate 2: The pair (i, j) carries a protected demand. -/
def protectedP (s : PState) (i j : Nat) : Bool :=
  (s.prot.contains (i, j))

/-- Gate 3: An observation is formally declared (not pre-observational). -/
def declaredP (s : PState) : Bool :=
  match s.obs with
  | none => false
  | some _ => true

/-- Gate 4: The declared observation does not separate the pair (vacuously true if undeclared). -/
def zeroDeclP (s : PState) (i j : Nat) : Bool :=
  match s.obs with
  | none => true
  | some cols => zeroP cols i j

/-- The Active Obstruction Detector (`obstP`):
    Active measurement of unbridged structural demand pressure. -/
def obstP (s : PState) (i j : Nat) : Bool :=
  retainedP s i j && protectedP s i j &&
    (match s.obs with
     | none => false
     | some cols => zeroP cols i j)

/-- **Theorem 1: The Four-Gate Factorization.**
    Active obstruction is identical to the conjunction of all four total gates. -/
theorem obstP_factors (s : PState) (i j : Nat) :
    obstP s i j = (retainedP s i j && protectedP s i j && declaredP s && zeroDeclP s i j) := by
  unfold obstP retainedP protectedP declaredP zeroDeclP
  cases s.obs with
  | none => simp
  | some cols => simp

/-- **Theorem 2: Sufficiency of the Four Gates.** -/
theorem obst_of_gates (s : PState) (i j : Nat)
    (h1 : retainedP s i j = true)
    (h2 : protectedP s i j = true)
    (h3 : declaredP s = true)
    (h4 : zeroDeclP s i j = true) :
    obstP s i j = true := by
  rw [obstP_factors, h1, h2, h3, h4]
  rfl

/-- **Fixture: protected observation collision.**
    Two distinct points (0, 1) retained and protected, collapsed under
    a single observation partition, generate an active obstruction. -/
def chasmState : PState :=
  { wit := [(0, 1)], prot := [(0, 1)], obs := some [[0, 1]] }

theorem chasm_0d_obstruction_certified : obstP chasmState 0 1 = true := by
  decide

/-- 1-Dimensional Circulation Functional on a triangle cycle (a -> b -> c -> a).
    Edge 0: a -> b, Edge 1: b -> c, Edge 2: c -> a. -/
def cycleCirculation (x : Int × Int × Int) : Int :=
  x.1 + x.2.1 + x.2.2

/-- Exact boundary coboundary (d0 g) on vertices (g_a, g_b, g_c):
    (d0 g)(a -> b) = g_b - g_a
    (d0 g)(b -> c) = g_c - g_b
    (d0 g)(c -> a) = g_a - g_c -/
def d0_coboundary (g : Int × Int × Int) : Int × Int × Int :=
  (g.2.1 - g.1, g.2.2 - g.2.1, g.1 - g.2.2)

/-- **Theorem 4: Exact Circulation Vanishing on Coboundaries.**
    For any scalar potential g, the circulation functional along a closed cycle vanishes identically. -/
theorem cycle_circulation_coboundary_vanishes (g : Int × Int × Int) :
    cycleCirculation (d0_coboundary g) = 0 := by
  rcases g with ⟨ga, gb, gc⟩
  unfold cycleCirculation d0_coboundary
  simp
  omega


/-- **Theorem 5: Magnetic/Gauge Flux Obstruction (Levels 12 & 18).**
    Edge configuration x = (1, 0, 0) has non-zero circulation I(x) = 1,
    preventing the existence of any global scalar potential g with d0 g = x. -/
theorem circulation_flux_obstruction :
    cycleCirculation (1, 0, 0) = 1 := by
  rfl

theorem no_scalar_potential_for_unit_flux :
    ∀ g : Int × Int × Int, d0_coboundary g ≠ (1, 0, 0) := by
  intro g h
  have h_circ := cycle_circulation_coboundary_vanishes g
  rw [h] at h_circ
  revert h_circ
  decide

/-- Number of obstructed entries in the supplied list; duplicates count again. -/
def activeDemandPressure (s : PState) (pairs : List (Nat × Nat)) : Nat :=
  (pairs.filter (fun (i, j) => obstP s i j)).length

/-- Necessary candidate condition on supplied metadata. This is not an
    implementation of the Genesis lift laws or an authorization decision. -/
def candidateLiftCondition (w_active : Nat) (resolves_obstruction : Bool) : Bool :=
  (w_active > 0) && resolves_obstruction

theorem zero_pressure_fails_candidate_condition (resolves : Bool) :
    candidateLiftCondition 0 resolves = false := by
  rfl

theorem positive_pressure_and_flag_satisfy_condition :
    candidateLiftCondition 1 true = true := by
  rfl

end MssnObstruction
