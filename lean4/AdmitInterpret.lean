import AdmitCore

/-!
# Admit interpretations

AuthorityEffect: None.

Three scoped readings. None is an embedding of the whole of the named theory.

* IdRefl(2): two atoms and reflexivity only. No `J`, no `Π`, no universe.
  Soundness sends a derivable identity to an admitted index in `twoPoint`
  together with metatheoretic equality of the atoms. Conservativity is stated
  for that conjunction, not for the admission judgment alone.
* Dimension at most 1: a vertex index and an edge with distinct endpoints,
  defined in this file. An admitted cut reads as an edge. Every such edge is
  a cut in some regime reached from the empty regime. The empty regime holds
  no cut, so this is not conservative over the empty regime.
* Hereditarily finite terms built by `empty` and `insert`, without
  extensionality. An admitted cut reads as membership of the two von Neumann
  terms in an insert-pair. Conservativity over the core is not claimed.
-/

namespace AdmitInterpret

/-! ## IdRefl(2) -/

inductive Atom where
  | zero
  | one

inductive IdJudg : Atom → Atom → Prop where
  | refl : (a : Atom) → IdJudg a a

def atomIndex : Atom → Nat
  | .zero => 0
  | .one => 1

def tp1 : AdmitCore.Regime := { AdmitCore.Regime.empty with data := [1] }

def twoPoint : AdmitCore.Regime := { tp1 with data := 0 :: tp1.data }

theorem twoPoint_mem0 : 0 ∈ twoPoint.data := List.Mem.head tp1.data

theorem twoPoint_mem1 : 1 ∈ twoPoint.data := List.Mem.tail 0 (List.Mem.head (a := 1) [])

theorem twoPoint_reaches : AdmitCore.Reaches AdmitCore.Regime.empty twoPoint :=
  AdmitCore.Reaches.step (AdmitCore.Step.admitData (n := 1))
    (AdmitCore.Reaches.step (AdmitCore.Step.admitData (Γ := tp1) (n := 0))
      AdmitCore.Reaches.refl)

theorem id_sound (a b : Atom) (h : IdJudg a b) :
    AdmitCore.Holds twoPoint (.admittedData (atomIndex a)) ∧ a = b := by
  cases h with
  | refl =>
    cases a with
    | zero => exact ⟨AdmitCore.Holds.admittedData twoPoint_mem0, rfl⟩
    | one => exact ⟨AdmitCore.Holds.admittedData twoPoint_mem1, rfl⟩

theorem id_conservative (a b : Atom)
    (h : AdmitCore.Holds twoPoint (.admittedData (atomIndex a)) ∧ a = b) : IdJudg a b := by
  cases h with
  | intro _ eq =>
    cases eq
    exact IdJudg.refl a

theorem not_id_zero_one : ¬ IdJudg .zero .one := by
  intro h
  cases h

theorem admission_is_not_identity :
    AdmitCore.Holds twoPoint (.admittedData 0) ∧ ¬ IdJudg .zero .one :=
  ⟨AdmitCore.Holds.admittedData twoPoint_mem0, not_id_zero_one⟩

/-! ## Finite 1-skeletal data -/

structure Edge where
  src : Nat
  tgt : Nat
  sep : src ≠ tgt

def edgeOfCut {Γ : AdmitCore.Regime} {a b : Nat}
    (h : AdmitCore.Holds Γ (.admittedCut a b)) : Edge where
  src := a
  tgt := b
  sep := AdmitCore.endpoints_apart h

theorem cut_as_edge {Γ : AdmitCore.Regime} {a b : Nat}
    (h : AdmitCore.Holds Γ (.admittedCut a b)) :
    (edgeOfCut h).src = a ∧ (edgeOfCut h).tgt = b ∧
      (edgeOfCut h).src ≠ (edgeOfCut h).tgt :=
  ⟨rfl, rfl, (edgeOfCut h).sep⟩

theorem edge_realizable (e : Edge) :
    ∃ Γ, AdmitCore.Reaches AdmitCore.Regime.empty Γ ∧
      AdmitCore.Holds Γ (.admittedCut e.src e.tgt) := by
  let Γ1 : AdmitCore.Regime :=
    { AdmitCore.Regime.empty with data := e.tgt :: AdmitCore.Regime.empty.data }
  let Γ2 : AdmitCore.Regime := { Γ1 with data := e.src :: Γ1.data }
  let Γ3 : AdmitCore.Regime := { Γ2 with cuts := (e.src, e.tgt) :: Γ2.cuts }
  have hsrc : e.src ∈ Γ2.data := List.Mem.head Γ1.data
  have htgt : e.tgt ∈ Γ2.data := List.Mem.tail e.src (List.Mem.head (a := e.tgt) [])
  refine ⟨Γ3, ?_, ?_⟩
  · exact AdmitCore.Reaches.step (AdmitCore.Step.admitData (n := e.tgt))
      (AdmitCore.Reaches.step (AdmitCore.Step.admitData (Γ := Γ1) (n := e.src))
        (AdmitCore.Reaches.step
          (AdmitCore.Step.admitCut (a := e.src) (b := e.tgt) hsrc htgt e.sep)
          AdmitCore.Reaches.refl))
  · exact AdmitCore.Holds.admittedCut (List.Mem.head []) e.sep

theorem edge_not_held_in_empty (e : Edge) :
    ¬ AdmitCore.Holds AdmitCore.Regime.empty (.admittedCut e.src e.tgt) := by
  intro h
  cases h with
  | admittedCut hm _ => cases hm

/-! ## Hereditarily finite terms, without extensionality -/

inductive HF where
  | empty
  | insert : HF → HF → HF

inductive Mem : HF → HF → Prop where
  | here : Mem x (.insert x t)
  | there : Mem x t → Mem x (.insert y t)

def vonNeumann : Nat → HF
  | 0 => .empty
  | n + 1 => .insert (vonNeumann n) (vonNeumann n)

theorem vn_inj : ∀ m n, vonNeumann m = vonNeumann n → m = n
  | 0, 0, _ => rfl
  | 0, _ + 1, h => nomatch h
  | _ + 1, 0, h => nomatch h
  | m + 1, n + 1, h => by
    have h1 : vonNeumann m = vonNeumann n := by
      injection h
    exact congrArg Nat.succ (vn_inj m n h1)

theorem vn_ne {m n : Nat} (h : m ≠ n) : vonNeumann m ≠ vonNeumann n :=
  fun eq => h (vn_inj m n eq)

def pairSet (a b : HF) : HF := .insert a (.insert b .empty)

theorem cut_hf_sound {Γ : AdmitCore.Regime} {a b : Nat}
    (h : AdmitCore.Holds Γ (.admittedCut a b)) :
    Mem (vonNeumann a) (pairSet (vonNeumann a) (vonNeumann b)) ∧
      Mem (vonNeumann b) (pairSet (vonNeumann a) (vonNeumann b)) ∧
        vonNeumann a ≠ vonNeumann b :=
  ⟨Mem.here, Mem.there Mem.here, vn_ne (AdmitCore.endpoints_apart h)⟩

theorem insert_order_differs (a b : HF) (h : a ≠ b) :
    HF.insert a (HF.insert b .empty) ≠ HF.insert b (HF.insert a .empty) := by
  intro eq
  injection eq with h1
  exact h h1

theorem example_cut_hf :
    Mem (vonNeumann 0) (pairSet (vonNeumann 0) (vonNeumann 1)) ∧
      Mem (vonNeumann 1) (pairSet (vonNeumann 0) (vonNeumann 1)) ∧
        vonNeumann 0 ≠ vonNeumann 1 :=
  cut_hf_sound AdmitCore.example_admitted_cut

end AdmitInterpret

#print axioms AdmitInterpret.twoPoint_mem0
#print axioms AdmitInterpret.twoPoint_mem1
#print axioms AdmitInterpret.twoPoint_reaches
#print axioms AdmitInterpret.id_sound
#print axioms AdmitInterpret.id_conservative
#print axioms AdmitInterpret.not_id_zero_one
#print axioms AdmitInterpret.admission_is_not_identity
#print axioms AdmitInterpret.cut_as_edge
#print axioms AdmitInterpret.edge_realizable
#print axioms AdmitInterpret.edge_not_held_in_empty
#print axioms AdmitInterpret.vn_inj
#print axioms AdmitInterpret.vn_ne
#print axioms AdmitInterpret.cut_hf_sound
#print axioms AdmitInterpret.insert_order_differs
#print axioms AdmitInterpret.example_cut_hf
