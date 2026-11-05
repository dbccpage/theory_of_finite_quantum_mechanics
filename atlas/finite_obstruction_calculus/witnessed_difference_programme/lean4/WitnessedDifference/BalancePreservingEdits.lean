/-!
Selected integer cycle laws for Source-25 balance preservation.
This checks local algebra and the directed tetrahedron distinction. The full
all-carrier edit classification and its connection to runtime storage remain
the written theorem and separately replayed native evidence.
-/
namespace WitnessedDifference.BalancePreservingEdits
abbrev Table := Nat → Nat → Int
abbrev Triple := Nat × Nat × Nat
def cycle (e : Table) (t : Triple) : Int :=
  e t.1 t.2.1 + e t.2.1 t.2.2 + e t.2.2 t.1
def Balanced (e : Table) (faces : List Triple) : Prop :=
  ∀ t ∈ faces, cycle e t = 0
def update (e : Table) (x y : Nat) (delta : Int) : Table :=
  fun a b => e a b + if a=x ∧ b=y then delta else 0

theorem gradient_balanced (g : Nat → Int) (faces : List Triple) :
    Balanced (fun a b => g a-g b) faces := by
  intro t _
  simp only [cycle]
  omega

theorem cycle_add (e f : Table) (t : Triple) :
    cycle (fun a b => e a b+f a b) t = cycle e t+cycle f t := by
  simp only [cycle]
  omega

theorem update_outside_cycle (e : Table) (x y a b c : Nat) (delta : Int)
    (hab : ¬(a=x ∧ b=y)) (hbc : ¬(b=x ∧ c=y)) (hca : ¬(c=x ∧ a=y)) :
    cycle (update e x y delta) (a,b,c) = cycle e (a,b,c) := by
  simp [cycle,update,hab,hbc,hca]

theorem update_at_first_arc (e : Table) (a b c : Nat) (delta : Int)
    (hab : a≠b) (hca : c≠a) :
    cycle (update e a b delta) (a,b,c) = cycle e (a,b,c)+delta := by
  simp [cycle,update,Ne.symm hab,hca]
  omega

theorem zero_unit_update_nonzero (a b c : Nat) (hab : a≠b) (hca : c≠a) :
    cycle (update (fun _ _ => 0) a b 1) (a,b,c) ≠ 0 := by
  rw [update_at_first_arc _ _ _ _ _ hab hca]
  simp [cycle]

theorem fill_balance_iff (e : Table) (faces : List Triple) (t : Triple) :
    Balanced e (t::faces) ↔ cycle e t=0 ∧ Balanced e faces := by
  simp [Balanced]

theorem preserved_cycle_when_entries_agree (e f : Table) (a b c : Nat)
    (hab : e a b=f a b) (hbc : e b c=f b c) (hca : e c a=f c a) :
    cycle e (a,b,c)=cycle f (a,b,c) := by
  simp [cycle,hab,hbc,hca]

theorem directed_tetrahedron_identity (e : Table) (a b c d : Nat) :
    cycle e (a,b,c)-cycle e (a,c,b)-cycle e (a,b,d)+cycle e (a,d,b)
      +cycle e (a,c,d)-cycle e (a,d,c)-cycle e (b,c,d)+cycle e (b,d,c)=0 := by
  simp only [cycle]
  omega

theorem seven_faces_force_eighth (e : Table) (a b c d : Nat)
    (h1 : cycle e (a,c,b)=0) (h2 : cycle e (a,b,d)=0)
    (h3 : cycle e (a,d,b)=0) (h4 : cycle e (a,c,d)=0)
    (h5 : cycle e (a,d,c)=0) (h6 : cycle e (b,c,d)=0)
    (h7 : cycle e (b,d,c)=0) : cycle e (a,b,c)=0 := by
  have identity := directed_tetrahedron_identity e a b c d
  omega

def threeFaceCounter : Table := fun a b => if a=2 ∧ b=0 then 1 else 0
theorem three_faces_do_not_force_fourth :
    cycle threeFaceCounter (0,1,3)=0 ∧ cycle threeFaceCounter (0,2,3)=0 ∧
    cycle threeFaceCounter (1,2,3)=0 ∧ cycle threeFaceCounter (0,1,2)=1 := by
  decide
end WitnessedDifference.BalancePreservingEdits
