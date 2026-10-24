/-!
TFQ-0008, narrowed finite case. AuthorityEffect: None.

Proved here, and nowhere wider:
- the length-1 and length-2 path sums on one two-edge integer path;
- an unnormalized two-weight sector mask;
- the integer Cayley column identity, against the Euler step;
- one distance-1 witness that is not a scaled stochastic kernel.

No continuum generator, CPTP lift, or general instrument is constructed.
-/

namespace CampaignTfq0008FiniteDynamics

structure Edge where
  src : Nat
  dst : Nat
  w : Int

def addIf (cond : Bool) (acc w : Int) : Int :=
  if cond then acc + w else acc

def sumLen1 : List Edge → Int
  | [] => 0
  | e :: rest => addIf (e.src == 0 && e.dst == 2) (sumLen1 rest) e.w

def sumLen2From (e1 : Edge) : List Edge → Int
  | [] => 0
  | e2 :: rest =>
      addIf (e1.src == 0 && e1.dst == e2.src && e2.dst == 2)
        (sumLen2From e1 rest) (e1.w * e2.w)

def sumLen2 : List Edge → List Edge → Int
  | [], _ => 0
  | e1 :: rest, es => sumLen2From e1 es + sumLen2 rest es

def pathGraph (a b : Int) : List Edge := [⟨0, 1, a⟩, ⟨1, 2, b⟩]

theorem path_len1_zero (a b : Int) : sumLen1 (pathGraph a b) = 0 := by
  simp [pathGraph, sumLen1, addIf]

theorem path_len2_product (a b : Int) : sumLen2 (pathGraph a b) (pathGraph a b) = a * b := by
  simp [pathGraph, sumLen2, sumLen2From, addIf]

def mask : Int → Int → Int × Int
  | _w0, w1 => (0, w1)

theorem mask_support (w0 w1 : Int) : (mask w0 w1).1 = 0 := rfl

theorem mask_keeps_sector (w0 w1 : Int) : (mask w0 w1).2 = w1 := rfl

theorem mask_idempotent (w0 w1 : Int) :
    mask (mask w0 w1).1 (mask w0 w1).2 = mask w0 w1 := rfl

theorem mask_zero_mass (w0 : Int) : mask w0 0 = (0, 0) := rfl

def cayleyColSq (t : Int) : Int :=
  (1 - t * t) * (1 - t * t) + (2 * t) * (2 * t)

def eulerColSq (t : Int) : Int := 1 + t * t

theorem cayley_norm (t : Int) :
    cayleyColSq t = (1 + t * t) * (1 + t * t) := by
  unfold cayleyColSq
  grind

theorem euler_unit_iff (t : Int) : eulerColSq t = 1 ↔ t = 0 := by
  unfold eulerColSq
  constructor
  · intro h
    have h0 : t * t = 0 := by omega
    rcases Int.mul_eq_zero.mp h0 with ht | ht
    · exact ht
    · exact ht
  · intro ht
    subst ht
    rfl

theorem cayley_at_1 : cayleyColSq 1 = 4 := by
  unfold cayleyColSq
  decide

theorem euler_inflation_at_2 : eulerColSq 2 - 1 = 4 ∧ eulerColSq 2 = 5 := by
  unfold eulerColSq
  decide

theorem cayley_at_2 : cayleyColSq 2 = 25 ∧ (1 + 2 * 2) * (1 + 2 * 2) = 25 := by
  unfold cayleyColSq
  decide

structure M2 where
  a00 : Int
  a01 : Int
  a10 : Int
  a11 : Int

def row0 (M : M2) : Int := M.a00 + M.a01

def row1 (M : M2) : Int := M.a10 + M.a11

def absDiff (x y : Int) : Nat := (x - y).natAbs

def entryDist (A B : M2) : Nat :=
  max (max (absDiff A.a00 B.a00) (absDiff A.a01 B.a01))
      (max (absDiff A.a10 B.a10) (absDiff A.a11 B.a11))

def scaledId : M2 := ⟨2, 0, 0, 2⟩

def nearby : M2 := ⟨2, 0, 0, 3⟩

theorem tolerance_not_exact :
    entryDist nearby scaledId = 1 ∧
    row0 scaledId = 2 ∧ row1 scaledId = 2 ∧
    row0 nearby = 2 ∧ row1 nearby = 3 ∧
    row0 nearby ≠ row1 nearby := by
  unfold entryDist absDiff row0 row1 scaledId nearby
  decide

#print axioms path_len1_zero
#print axioms path_len2_product
#print axioms mask_support
#print axioms mask_keeps_sector
#print axioms mask_idempotent
#print axioms mask_zero_mass
#print axioms cayley_norm
#print axioms euler_unit_iff
#print axioms cayley_at_1
#print axioms euler_inflation_at_2
#print axioms cayley_at_2
#print axioms tolerance_not_exact

end CampaignTfq0008FiniteDynamics
