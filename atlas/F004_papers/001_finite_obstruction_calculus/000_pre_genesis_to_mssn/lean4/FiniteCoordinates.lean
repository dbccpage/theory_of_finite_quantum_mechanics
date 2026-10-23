import IntegerAction
import GraphHomology

/-! Explicit integral coordinates of finite free abelian groups. Both maps and
their inverse equations are constructed. Coefficients use the canonical integer
action proved in IntegerAction.lean, including negative coefficients. -/
namespace PreMssn.FiniteCoordinates
open Lean.Grind
open AddCommMonoid AddCommGroup
open Homology FreeAbelian IntegerAction
universe u v w

abbrev Vector (n : Nat) := Fin n → Int

instance vectorGroup (n : Nat) : AddCommGroup (Vector n) where
  zero := fun _ => 0
  add a b := fun i => a i + b i
  neg a := fun i => -a i
  sub a b := fun i => a i - b i
  add_zero a := funext (fun i => Int.add_zero (a i))
  add_comm a b := funext (fun i => Int.add_comm (a i) (b i))
  add_assoc a b c := funext (fun i => Int.add_assoc (a i) (b i) (c i))
  neg_add_cancel a := funext (fun i => neg_add_cancel (a i))
  sub_eq_add_neg _ _ := funext (fun _ => Int.sub_eq_add_neg)

def basis {n : Nat} (i : Fin n) : Vector n := fun j => if i = j then 1 else 0

def coordinates {n : Nat} : AddHom (Free (Fin n)) (Vector n) := extend basis

def coordinate {n : Nat} (i : Fin n) : AddHom (Free (Fin n)) Int where
  toFun q := coordinates q i
  map_zero := rfl
  map_add a b := congrArg (fun v : Vector n => v i) (coordinates.map_add a b)

theorem coordinate_multiple_gen {n : Nat} (k : Int) (i j : Fin n) :
    coordinate j (multiple k (gen i)) = k * (if i = j then 1 else 0) := by
  rw [hom_multiple, multiple_integer]
  rfl

theorem shift_coordinate_zero {n : Nat} (q : Free (Fin n)) :
    coordinate (0 : Fin (n+1)) (FreeAbelian.map Fin.succ q) = 0 := by
  apply hom_ext ((coordinate (0 : Fin (n+1))).comp (FreeAbelian.map Fin.succ))
    (AddHom.zero (Free (Fin n)) Int) _ q
  intro i
  change (if i.succ = 0 then (1 : Int) else 0) = 0
  simp [Fin.succ_ne_zero]

theorem shift_coordinate_succ {n : Nat} (q : Free (Fin n)) (j : Fin n) :
    coordinate j.succ (FreeAbelian.map Fin.succ q) = coordinate j q := by
  apply hom_ext ((coordinate j.succ).comp (FreeAbelian.map Fin.succ)) (coordinate j) _ q
  intro i
  change (if i.succ = j.succ then (1 : Int) else 0) = if i = j then 1 else 0
  simp

def synthesize : (n : Nat) → Vector n → Free (Fin n)
  | 0, _ => 0
  | n+1, a => multiple (a 0) (gen 0) +
      FreeAbelian.map Fin.succ (synthesize n (fun i => a i.succ))

theorem synthesize_zero (n : Nat) : synthesize n 0 = 0 := by
  induction n with
  | zero => rfl
  | succ n ih =>
    change multiple 0 (gen 0) + FreeAbelian.map Fin.succ (synthesize n 0) = 0
    rw [multiple_zero, ih, (FreeAbelian.map Fin.succ).map_zero, zero_add]

theorem synthesize_add (n : Nat) (a b : Vector n) :
    synthesize n (a+b) = synthesize n a + synthesize n b := by
  induction n with
  | zero => exact (zero_add 0).symm
  | succ n ih =>
    change multiple (a 0 + b 0) (gen 0) +
      FreeAbelian.map Fin.succ (synthesize n (fun i : Fin n => a i.succ + b i.succ)) =
      (multiple (a 0) (gen 0) + FreeAbelian.map Fin.succ (synthesize n (fun i => a i.succ))) +
      (multiple (b 0) (gen 0) + FreeAbelian.map Fin.succ (synthesize n (fun i => b i.succ)))
    rw [multiple_add, show synthesize n (fun i : Fin n => a i.succ + b i.succ) =
      synthesize n (fun i => a i.succ) + synthesize n (fun i => b i.succ) from ih _ _,
      (FreeAbelian.map Fin.succ).map_add]
    rw [add_assoc, add_left_comm (multiple (b 0) (gen 0))
      (FreeAbelian.map Fin.succ (synthesize n (fun i => a i.succ))), ← add_assoc]

def fromVector {n : Nat} : AddHom (Vector n) (Free (Fin n)) where
  toFun := synthesize n
  map_zero := synthesize_zero n
  map_add := synthesize_add n

theorem coordinates_synthesize (n : Nat) (a : Vector n) :
    coordinates (synthesize n a) = a := by
  induction n with
  | zero => exact funext (fun i => Fin.elim0 i)
  | succ n ih =>
    funext j
    refine Fin.cases (motive := fun j => coordinates (synthesize (n+1) a) j = a j) ?_ ?_ j
    · change coordinate (0 : Fin (n+1))
        (multiple (a 0) (gen 0) + FreeAbelian.map Fin.succ (synthesize n (fun i => a i.succ))) = a 0
      rw [(coordinate _).map_add, coordinate_multiple_gen, shift_coordinate_zero]
      simp
    · intro j
      change coordinate j.succ
        (multiple (a 0) (gen 0) + FreeAbelian.map Fin.succ (synthesize n (fun i => a i.succ))) = a j.succ
      rw [(coordinate _).map_add, coordinate_multiple_gen, shift_coordinate_succ]
      have h := congrArg (fun v : Vector n => v j) (ih (fun i => a i.succ))
      change coordinate j (synthesize n (fun i => a i.succ)) = a j.succ at h
      simpa [eq_comm, Fin.succ_ne_zero] using h

theorem synthesize_basis (n : Nat) (i : Fin n) : synthesize n (basis i) = gen i := by
  induction n with
  | zero => exact Fin.elim0 i
  | succ n ih =>
    refine Fin.cases (motive := fun i => synthesize (n+1) (basis i) = gen i) ?_ ?_ i
    · have ht : (fun j : Fin n => basis (0 : Fin (n+1)) j.succ) = 0 := by
        funext j
        change (if (0 : Fin (n+1)) = j.succ then (1 : Int) else 0) = 0
        simp [eq_comm, Fin.succ_ne_zero]
      change multiple 1 (gen 0) + FreeAbelian.map Fin.succ
        (synthesize n (fun j => basis (0 : Fin (n+1)) j.succ)) = gen 0
      rw [ht, synthesize_zero, multiple_one, (FreeAbelian.map Fin.succ).map_zero, add_zero]
    · intro i
      have ht : (fun j : Fin n => basis i.succ j.succ) = basis i := by
        funext j
        simp [basis]
      change multiple 0 (gen 0) + FreeAbelian.map Fin.succ
        (synthesize n (fun j => basis i.succ j.succ)) = gen i.succ
      rw [ht, ih, multiple_zero, zero_add, map_gen]

def freeFiniteIso (n : Nat) : AddIso (Free (Fin n)) (Vector n) where
  forward := coordinates
  backward := fromVector
  left_inverse q := hom_ext (fromVector.comp coordinates) (AddHom.identity _)
    (synthesize_basis n) q
  right_inverse := coordinates_synthesize n

def carrierIso {A : Type u} {B : Type v} (f : A → B) (g : B → A)
    (left : ∀ a, g (f a) = a) (right : ∀ b, f (g b) = b) :
    AddIso (Free A) (Free B) where
  forward := FreeAbelian.map f
  backward := FreeAbelian.map g
  left_inverse q := hom_ext ((FreeAbelian.map g).comp (FreeAbelian.map f))
    (AddHom.identity _) (fun a => by
      change gen (g (f a)) = gen a
      rw [left]) q
  right_inverse q := hom_ext ((FreeAbelian.map f).comp (FreeAbelian.map g))
    (AddHom.identity _) (fun b => by
      change gen (f (g b)) = gen b
      rw [right]) q

/-- A supplied enumeration of the actual components gives explicit integral
coordinates, independently of the graph's chosen vertex/edge enumeration. -/
def graphH0Iso (G : GraphHomology.Graph.{u}) (c : Nat)
    (number : GraphHomology.Component G → Fin c)
    (representative : Fin c → GraphHomology.Component G)
    (left : ∀ a, representative (number a) = a)
    (right : ∀ i, number (representative i) = i) :
    AddIso (GraphHomology.H0 G) (Vector c) :=
  ((GraphHomology.h0ComponentIso G).comp (carrierIso number representative left right)).comp
    (freeFiniteIso c)

def total : (n : Nat) → Vector n → Int
  | 0, _ => 0
  | n+1, a => a 0 + total n (fun i => a i.succ)

theorem total_zero (n : Nat) : total n 0 = 0 := by
  induction n with
  | zero => rfl
  | succ n ih =>
    change 0 + total n 0 = 0
    rw [ih, Int.zero_add]

theorem total_add (n : Nat) (a b : Vector n) : total n (a+b) = total n a + total n b := by
  induction n with
  | zero => rfl
  | succ n ih =>
    change (a 0 + b 0) + total n (fun i => a i.succ + b i.succ) =
      (a 0 + total n (fun i => a i.succ)) + (b 0 + total n (fun i => b i.succ))
    rw [show total n (fun i => a i.succ + b i.succ) =
      total n (fun i => a i.succ) + total n (fun i => b i.succ) from ih _ _]
    omega

def augmentation (n : Nat) : AddHom (Vector n) Int where
  toFun := total n
  map_zero := total_zero n
  map_add := total_add n

theorem total_basis (n : Nat) (i : Fin n) : total n (basis i) = 1 := by
  induction n with
  | zero => exact Fin.elim0 i
  | succ n ih =>
    refine Fin.cases (motive := fun i => total (n+1) (basis i) = 1) ?_ ?_ i
    · have ht : (fun j : Fin n => basis (0 : Fin (n+1)) j.succ) = (0 : Vector n) := by
        funext j
        change (if (0 : Fin (n+1)) = j.succ then (1 : Int) else 0) = 0
        simp [eq_comm, Fin.succ_ne_zero]
      change 1 + total n (fun j => basis (0 : Fin (n+1)) j.succ) = 1
      rw [ht, total_zero, Int.add_zero]
    · intro i
      have ht : (fun j : Fin n => basis i.succ j.succ) = basis i := by
        funext j
        simp [basis]
      change 0 + total n (fun j => basis i.succ j.succ) = 1
      rw [ht, ih, Int.zero_add]

def graphAugmentation (G : GraphHomology.Graph.{u}) : AddHom (GraphHomology.H0 G) Int :=
  (extend (fun _ : GraphHomology.Component G => (1 : Int))).comp (GraphHomology.toComponents G)

theorem graph_augmentation_coordinates (G : GraphHomology.Graph.{u}) (c : Nat)
    (number : GraphHomology.Component G → Fin c)
    (representative : Fin c → GraphHomology.Component G)
    (left : ∀ a, representative (number a) = a)
    (right : ∀ i, number (representative i) = i) (q : GraphHomology.H0 G) :
    augmentation c ((graphH0Iso G c number representative left right).forward q) =
      graphAugmentation G q := by
  induction q using Quotient.inductionOn with
  | _ x =>
    apply hom_ext ((augmentation c).comp
      ((graphH0Iso G c number representative left right).forward.comp
        (quotientProjection (GraphHomology.boundary G))))
      ((graphAugmentation G).comp (quotientProjection (GraphHomology.boundary G))) _ x
    intro v
    exact total_basis c (number (GraphHomology.component G v))

def Kernel {A : Type u} {B : Type v} [AddCommGroup A] [AddCommGroup B]
    (f : AddHom A B) := {a : A // f a = 0}

instance kernelGroup {A : Type u} {B : Type v} [AddCommGroup A] [AddCommGroup B]
    (f : AddHom A B) : AddCommGroup (Kernel f) where
  zero := ⟨0, f.map_zero⟩
  add a b := ⟨a.val+b.val, by rw [f.map_add, a.property, b.property, zero_add]⟩
  neg a := ⟨-a.val, by rw [f.map_neg, a.property, neg_zero]⟩
  sub a b := ⟨a.val-b.val, by rw [f.map_sub, a.property, b.property, sub_self]⟩
  add_zero a := Subtype.ext (add_zero a.val)
  add_comm a b := Subtype.ext (add_comm a.val b.val)
  add_assoc a b c := Subtype.ext (add_assoc a.val b.val c.val)
  neg_add_cancel a := Subtype.ext (neg_add_cancel a.val)
  sub_eq_add_neg a b := Subtype.ext (sub_eq_add_neg a.val b.val)

def complete (n : Nat) (a : Vector n) : Vector (n+1) := Fin.cases (-total n a) a

theorem complete_total_zero (n : Nat) (a : Vector n) : total (n+1) (complete n a) = 0 := by
  change -total n a + total n (fun i => complete n a i.succ) = 0
  simp only [complete, Fin.cases_succ]
  exact Int.add_left_neg _

def reducedVectorIso (n : Nat) : AddIso (Kernel (augmentation (n+1))) (Vector n) where
  forward := {
    toFun := fun a i => a.val i.succ
    map_zero := rfl
    map_add := fun _ _ => rfl
  }
  backward := {
    toFun := fun a => ⟨complete n a, complete_total_zero n a⟩
    map_zero := by
      apply Subtype.ext
      funext i
      refine Fin.cases (motive := fun i => complete n 0 i = (0 : Vector (n+1)) i) ?_ ?_ i
      · change -total n 0 = 0
        rw [total_zero, Int.neg_zero]
      · intro i
        rfl
    map_add := fun a b => by
      apply Subtype.ext
      funext i
      refine Fin.cases (motive := fun i => complete n (a+b) i =
        (complete n a + complete n b) i) ?_ ?_ i
      · change -total n (a+b) = -total n a + -total n b
        rw [total_add, Int.neg_add]
      · intro i
        rfl
  }
  left_inverse a := by
    apply Subtype.ext
    funext i
    refine Fin.cases (motive := fun i => complete n (fun j => a.val j.succ) i = a.val i) ?_ ?_ i
    · change -total n (fun j => a.val j.succ) = a.val 0
      have h := a.property
      change a.val 0 + total n (fun j => a.val j.succ) = 0 at h
      omega
    · intro i
      rfl
  right_inverse _ := rfl

def kernelIso {A : Type u} {B : Type v} {R : Type w}
    [AddCommGroup A] [AddCommGroup B] [AddCommGroup R]
    (i : AddIso A B) (f : AddHom A R) (g : AddHom B R)
    (commutes : ∀ a, g (i.forward a) = f a) : AddIso (Kernel f) (Kernel g) where
  forward := {
    toFun := fun a => ⟨i.forward a.val, (commutes a.val).trans a.property⟩
    map_zero := Subtype.ext i.forward.map_zero
    map_add := fun a b => Subtype.ext (i.forward.map_add a.val b.val)
  }
  backward := {
    toFun := fun b => ⟨i.backward b.val, by
      have h := commutes (i.backward b.val)
      rw [i.right_inverse] at h
      exact h.symm.trans b.property⟩
    map_zero := Subtype.ext i.backward.map_zero
    map_add := fun a b => Subtype.ext (i.backward.map_add a.val b.val)
  }
  left_inverse a := Subtype.ext (i.left_inverse a.val)
  right_inverse b := Subtype.ext (i.right_inverse b.val)

abbrev ReducedH0 (G : GraphHomology.Graph.{u}) := Kernel (graphAugmentation G)

/-- For c=n+1 actual connected components, reduced integral H0 is explicitly
isomorphic to n-tuples of integers. The nonempty condition is essential. -/
def graphReducedH0Iso (G : GraphHomology.Graph.{u}) (n : Nat)
    (number : GraphHomology.Component G → Fin (n+1))
    (representative : Fin (n+1) → GraphHomology.Component G)
    (left : ∀ a, representative (number a) = a)
    (right : ∀ i, number (representative i) = i) : AddIso (ReducedH0 G) (Vector n) :=
  (kernelIso (graphH0Iso G (n+1) number representative left right)
    (graphAugmentation G) (augmentation (n+1))
    (graph_augmentation_coordinates G (n+1) number representative left right)).comp
    (reducedVectorIso n)

end PreMssn.FiniteCoordinates
