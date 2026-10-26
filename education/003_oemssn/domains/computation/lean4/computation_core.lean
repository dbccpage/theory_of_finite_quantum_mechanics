/-!
  Theoretical Computer Science & Automata Theory — Lean 4 Formal Core
  AuthorityEffect: None
  Compiler results are recorded separately; this header is not a verification receipt.
-/

namespace ComputationDomainSetting

/-- Base setting for computation: Carrier, asserted relation, endpoints, and irreflexivity. -/
structure Setting where
  X : Type
  r : X → X → Prop
  a : X
  b : X
  irrefl : ∀ x, ¬ r x x

/-- The fundamental theorem of distinctness: irreflexive witnessed difference implies endpoints are distinct. -/
theorem irrefl_distinct {X : Type} {r : X → X → Prop} (irrefl : ∀ x, ¬ r x x) {a b : X} (h : r a b) : a ≠ b :=
  fun heq => irrefl a (heq ▸ h)

/-- In this domain setting, designated endpoints S.a and S.b are formally distinct under the witnessed relation. -/
theorem setting_endpoints_distinct (S : Setting) (h : S.r S.a S.b) : S.a ≠ S.b :=
  irrefl_distinct S.irrefl h

/-- Cotransitivity: an asserted difference splits against every third candidate. -/
def Cotrans {X : Type} (r : X → X → Prop) : Prop :=
  ∀ x y, r x y → ∀ z, r x z ∨ r z y

/-- Every endomap fixes the designated root. This is a singleton condition,
    not a theorem about continuum, computation, SQL or physical recovery. -/
def EveryEndomapFixesRoot (S : Setting) : Prop :=
  ∀ f : S.X → S.X, f S.a = S.a

theorem every_endomap_fixes_root_iff (S : Setting) :
    EveryEndomapFixesRoot S ↔ ∀ x : S.X, x = S.a := by
  constructor
  · intro h x
    exact h (fun _ => x)
  · intro h f
    exact h (f S.a)

theorem witnessed_pair_refutes_fixed_root (S : Setting) (h : S.r S.a S.b) :
    ¬ EveryEndomapFixesRoot S := by
  intro fixed
  have hb : S.b = S.a := fixed (fun _ => S.b)
  exact setting_endpoints_distinct S h hb.symm


/-- Relational database model representing relational table state. -/
structure RelationalModel where
  Carrier : Type
  Relation : Carrier → Carrier → Prop
  a_sql : Carrier
  b_sql : Carrier
  irrefl_sql : ∀ x, ¬ Relation x x

/-- A bisimulation mapping from the operational domain setting to the relational model. -/
structure BisimulationMapping (S : Setting) (M : RelationalModel) where
  f : S.X → M.Carrier
  map_a : f S.a = M.a_sql
  map_b : f S.b = M.b_sql
  rel_forward : ∀ x y, S.r x y → M.Relation (f x) (f y)
  rel_backward : ∀ x y, M.Relation (f x) (f y) → S.r x y
  inj : ∀ x y, f x = f y → x = y

/-- Theorem: Forward simulation preserves irreflexivity across the bisimulation mapping. -/
theorem bisimulation_preserves_irreflexivity (S : Setting) (M : RelationalModel) (B : BisimulationMapping S M) :
    ∀ x, ¬ M.Relation (B.f x) (B.f x) := by
  intro x hrel
  have h_orig : S.r x x := B.rel_backward x x hrel
  exact S.irrefl x h_orig

/-- Theorem: Bisimulation preserves endpoint distinctness in the relational SQL model. -/
theorem bisimulation_preserves_distinctness (S : Setting) (M : RelationalModel) (B : BisimulationMapping S M) (h : S.r S.a S.b) :
    M.a_sql ≠ M.b_sql := by
  have h_distinct : S.a ≠ S.b := setting_endpoints_distinct S h
  intro heq
  have h_f : B.f S.a = B.f S.b := by
    rw [B.map_a, B.map_b, heq]
  have h_eq : S.a = S.b := B.inj S.a S.b h_f
  exact h_distinct h_eq

/-- Theorem: The witnessed difference relation is preserved under the bisimulation mapping. -/
theorem bisimulation_witness_preserved (S : Setting) (M : RelationalModel) (B : BisimulationMapping S M) (h : S.r S.a S.b) :
    M.Relation M.a_sql M.b_sql := by
  rw [← B.map_a, ← B.map_b]
  exact B.rel_forward S.a S.b h

/-- Fuel-bounded execution state: operational state paired with fuel. -/
structure FuelState (X : Type) where
  node : X
  fuel : Nat
  deriving DecidableEq, Repr

/-- Fuel status taxonomy matching Scenario 4 Steps 08 and 09. -/
inductive FuelStatus where
  | running
  | halted
  | out_of_fuel
  deriving DecidableEq, Repr

/-- One step of fuel-bounded reduction. -/
def step_fuel {X : Type} (trans : X → Option X) (s : FuelState X) : FuelStatus × FuelState X :=
  match s.fuel with
  | 0 => (.out_of_fuel, s)
  | Nat.succ f' =>
    match trans s.node with
    | none => (.halted, s)
    | some next_node => (.running, { node := next_node, fuel := f' })

/-- Theorem: Fuel strictly decreases on every non-terminal transition step. -/
theorem fuel_strictly_decreases {X : Type} (trans : X → Option X) (s : FuelState X)
    (next_node : X) (f' : Nat) (h_fuel : s.fuel = Nat.succ f') (h_step : trans s.node = some next_node) :
    (step_fuel trans s).2.fuel < s.fuel := by
  unfold step_fuel
  rw [h_fuel]
  dsimp
  rw [h_step]
  dsimp
  exact Nat.lt_succ_self f'

/-- Theorem: Fuel exhaustion triggers deterministically when fuel reaches 0 on an active transition. -/
theorem fuel_exhaustion_at_zero {X : Type} (trans : X → Option X) (node : X) :
    (step_fuel trans { node := node, fuel := 0 }).1 = FuelStatus.out_of_fuel := by
  rfl

end ComputationDomainSetting
