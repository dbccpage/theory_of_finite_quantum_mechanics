/-!
# CODA-CS-Q Algebra: Finite Profile Factorization and Sampling Limits

Self-contained formal counterparts of CODA-CS-Q, with the scope stated below:
1. CSQ-T1: `exact_on_image` — A query factors through the profile on the realized
   image iff it is fiber constant.
2. CSQ-T2: `approximate_collision_bound` — Approximate decoder error bounds collisions
   by 2ε; metric separation corollary; and indiscrete pseudometric countermodel.
3. CSQ-T3: `lipschitz_access` — abstract monotone-scale inequality; no real-number instance is constructed here.
4. CSQ-T4 analogue: `samples_not_query` — Boolean signals on Point3 have an
   unobserved third value. The real quadratic example is proved in the manuscript.
5. CSQ-T5: `whole_codomain_needs_extension` — Factorization on the whole codomain requires
   extension; fiber constancy on empty domain does not produce a total factor into an empty codomain.
6. `total_factor_of_inhabited` — Total factor exists when codomain is inhabited.

AuthorityEffect: None.
-/

namespace Coda.CSQ

set_option linter.unusedVariables false
set_option warn.classDefReducibility false

/-- Fiber constancy: equal profiles imply equal query values. -/
def FiberConstant {X P Y : Type _} (p : X → P) (q : X → Y) : Prop :=
  ∀ x y : X, p x = p y → q x = q y

/-- Total profile factorization: q = g ∘ p for some g : P → Y. -/
def Factors {X P Y : Type _} (p : X → P) (q : X → Y) : Prop :=
  ∃ g : P → Y, ∀ x : X, g (p x) = q x

/-- Bundled realized image point: a profile value with an explicit domain witness. -/
structure ImagePoint {X P : Type _} (p : X → P) where
  val : P
  witness : X
  eq : p witness = val

/-- Canonical injection from domain element to ImagePoint. -/
def imagePointOf {X P : Type _} (p : X → P) (x : X) : ImagePoint p :=
  ⟨p x, x, rfl⟩

/-- Factorization predicate on the realized image of p. -/
def ImageFactor {X P Y : Type _} (p : X → P) (q : X → Y) (g : ImagePoint p → Y) : Prop :=
  (∀ x : X, g (imagePointOf p x) = q x) ∧
  (∀ p₁ p₂ : ImagePoint p, p₁.val = p₂.val → g p₁ = g p₂)

/--
CSQ-T1: A query factors through the profile on the realized image
if and only if it is fiber constant.
-/
theorem exact_on_image {X P Y : Type _} (p : X → P) (q : X → Y) :
    (∃ g : ImagePoint p → Y, ImageFactor p q g) ↔ FiberConstant p q := by
  constructor
  · rintro ⟨g, hg1, hg2⟩ x y same
    calc
      q x = g (imagePointOf p x) := (hg1 x).symm
      _ = g (imagePointOf p y) := hg2 (imagePointOf p x) (imagePointOf p y) same
      _ = q y := hg1 y
  · intro hfc
    refine ⟨fun pt => q pt.witness, ?_, ?_⟩
    · intro x; rfl
    · intro p₁ p₂ h_val
      apply hfc
      calc
        p p₁.witness = p₁.val := p₁.eq
        _ = p₂.val := h_val
        _ = p p₂.witness := p₂.eq.symm

/-- Image factors recovering the same query are equal, including explicit witness carriers. -/
theorem image_factor_unique {X P Y : Type _} (p : X → P) (q : X → Y)
    (g h : ImagePoint p → Y) (hg : ImageFactor p q g) (hh : ImageFactor p q h) :
    g = h := by
  funext pt
  calc
    g pt = g (imagePointOf p pt.witness) := hg.2 pt _ pt.eq.symm
    _ = q pt.witness := hg.1 _
    _ = h (imagePointOf p pt.witness) := (hh.1 _).symm
    _ = h pt := hh.2 _ pt pt.eq

/-- Abstract distance structure. -/
class Dist (Y : Type _) (D : outParam (Type _)) where
  dist : Y → Y → D

/-- Abstract pseudometric structure on Y over an ordered commutative carrier D. -/
class PseudoMetricSpace (Y : Type _) (D : outParam (Type _)) [Add D] [LE D] extends Dist Y D where
  dist_comm : ∀ a b : Y, dist a b = dist b a
  dist_triangle : ∀ a b c : Y, dist a c ≤ dist a b + dist b c
  add_le_add : ∀ {a b c d : D}, a ≤ b → c ≤ d → a + c ≤ b + d
  le_trans : ∀ {a b c : D}, a ≤ b → b ≤ c → a ≤ c

/-- Metric space structure adding separation axiom: dist a b = zero → a = b. -/
class MetricSpace (Y : Type _) (D : outParam (Type _)) [Add D] [LE D] extends PseudoMetricSpace Y D where
  zero : D
  zero_add : zero + zero = zero
  dist_nonneg : ∀ a b : Y, zero ≤ dist a b
  le_antisymm : ∀ {a b : D}, a ≤ b → b ≤ a → a = b
  eq_of_dist_zero : ∀ a b : Y, dist a b = zero → a = b

/--
CSQ-T2: Approximate decoder collision bound.
If g achieves uniform error ε on evaluated points, collisions in p have distance ≤ 2ε.
-/
theorem approximate_collision_bound {X P Y D : Type _} [Add D] [LE D] [M : PseudoMetricSpace Y D]
    (p : X → P) (q : X → Y) (g : P → Y) (epsilon : D)
    (bound : ∀ x, M.dist (q x) (g (p x)) ≤ epsilon)
    {x y : X} (same : p x = p y) : M.dist (q x) (q y) ≤ epsilon + epsilon := by
  have tri := M.dist_triangle (q x) (g (p x)) (q y)
  have hy : M.dist (g (p x)) (q y) ≤ epsilon := by
    rw [same, M.dist_comm]
    exact bound y
  have hx := bound x
  have h_add := M.add_le_add hx hy
  exact M.le_trans tri h_add

/--
CSQ-T2 Metric Corollary:
When the target satisfies the metric separation axiom and ε = 0,
zero decoder error implies exact value equality q(x) = q(y).
-/
theorem metric_zero_error_implies_equality {X P Y D : Type _} [Add D] [LE D]
    [M : MetricSpace Y D]
    (p : X → P) (q : X → Y) (g : P → Y)
    (bound : ∀ x, M.dist (q x) (g (p x)) ≤ M.zero)
    {x y : X} (same : p x = p y) : q x = q y := by
  have h_bound := approximate_collision_bound p q g M.zero bound same
  rw [M.zero_add] at h_bound
  have h_nonneg := M.dist_nonneg (q x) (q y)
  have h_dist_zero : M.dist (q x) (q y) = M.zero := M.le_antisymm h_bound h_nonneg
  exact M.eq_of_dist_zero (q x) (q y) h_dist_zero

/-- Canonical indiscrete pseudometric on any type Y. -/
def IndiscretePseudoMetric (Y : Type _) : PseudoMetricSpace Y Nat where
  dist := fun _ _ => 0
  dist_comm := fun _ _ => rfl
  dist_triangle := fun _ _ _ => Nat.le_refl 0
  add_le_add := fun hab hcd => Nat.add_le_add hab hcd
  le_trans := fun hab hbc => Nat.le_trans hab hbc

/--
CSQ-T2 Pseudometric Countermodel (B1):
In an indiscrete pseudometric space, zero decoder error (ε = 0) does NOT imply
value equality q(x) = q(y) without metric separation.
-/
theorem pseudometric_zero_error_does_not_imply_equality :
    ∃ (X P Y : Type) (M : PseudoMetricSpace Y Nat) (p : X → P) (q : X → Y) (g : P → Y),
      (∀ x, M.dist (q x) (g (p x)) ≤ 0) ∧
      (∃ x y, p x = p y ∧ q x ≠ q y) := by
  refine ⟨Bool, Unit, Bool, IndiscretePseudoMetric Bool, fun _ => (), id, fun _ => false, ?_, ?_⟩
  · intro x; exact Nat.le_refl 0
  · refine ⟨false, true, rfl, ?_⟩
    intro h; cases h

/--
CSQ-T3: Lipschitz access bounds query error by sample resolution.
-/
theorem lipschitz_access {X Y D : Type _} [LE D]
    (distX : X → X → D) (distY : Y → Y → D)
    (scale : D → D) (mono : ∀ {a b : D}, a ≤ b → scale a ≤ scale b)
    (le_trans : ∀ {a b c : D}, a ≤ b → b ≤ c → a ≤ c)
    (q : X → Y)
    (lip : ∀ a b : X, distY (q a) (q b) ≤ scale (distX a b))
    (x a : X) (epsilon : D) (h : distX x a ≤ epsilon) :
    distY (q x) (q a) ≤ scale epsilon := by
  have h1 := lip x a
  have h2 := mono h
  exact le_trans h1 h2

/-- Three-point domain modeling {0, 1, 1/2}. -/
inductive Point3
  | p0
  | p1
  | pMid
  deriving DecidableEq

def endpoint_profile (f : Point3 → Bool) : Bool × Bool :=
  (f Point3.p0, f Point3.p1)

def midpoint_query (f : Point3 → Bool) : Bool :=
  f Point3.pMid

/--
CSQ-T4 Boolean analogue: two observed coordinates do not determine the third.
The false signal and a Boolean bump share the profile (false, false) but differ at pMid.
This declaration does not quantify over real functions or evaluate a quadratic.
-/
theorem samples_not_query :
    ¬ Factors endpoint_profile midpoint_query := by
  rintro ⟨g, hg⟩
  let zero_sig : Point3 → Bool := fun _ => false
  let bump_sig : Point3 → Bool := fun pt => match pt with
    | Point3.pMid => true
    | _ => false
  have h_prof : endpoint_profile zero_sig = endpoint_profile bump_sig := rfl
  have h0 := hg zero_sig
  have h1 := hg bump_sig
  have contra : false = true := by
    calc false = midpoint_query zero_sig := rfl
    _ = g (endpoint_profile zero_sig) := h0.symm
    _ = g (endpoint_profile bump_sig) := by rw [h_prof]
    _ = midpoint_query bump_sig := h1
    _ = true := rfl
  cases contra

/--
CSQ-T5: Factorization on the whole codomain requires extension.
Fiber constancy on Empty does not produce a total factor into an empty codomain.
-/
theorem whole_codomain_needs_extension :
    FiberConstant (fun _ : Empty => ()) (fun x : Empty => x) ∧
    ¬ Factors (fun _ : Empty => ()) (fun x : Empty => x) := by
  constructor
  · intro x; exact nomatch x
  · rintro ⟨g, _⟩; exact nomatch g ()

/--
Total factor existence when codomain is inhabited (via Classical choice).
-/
theorem total_factor_of_inhabited {X P Y : Type _} [Inhabited Y]
    (p : X → P) (q : X → Y) (h : FiberConstant p q) : Factors p q := by
  classical
  refine ⟨fun z => if hz : ∃ x : X, p x = z then q (Classical.choose hz) else default, ?_⟩
  intro x
  have hex : ∃ x' : X, p x' = p x := ⟨x, rfl⟩
  dsimp
  split
  · rename_i h_ex
    apply h
    exact Classical.choose_spec h_ex
  · rename_i h_nex
    exact False.elim (h_nex hex)

end Coda.CSQ
