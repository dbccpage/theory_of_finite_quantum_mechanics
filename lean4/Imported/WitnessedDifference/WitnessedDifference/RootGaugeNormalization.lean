/- Imported from the sibling atlas so that this repository carries its own Lean evidence.
   Original path : omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/RootGaugeNormalization.lean
   Original sha256: 908ce9ef46a269bf2427e7f167d6f55846b77c89e4b667ba27d0a10e480b95cc (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.WitnessedDifference.WitnessedDifference.RootGaugeNormalization
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/-!
# Source-23 root normalization, complete obstruction and transport

Tables retain every ordered integer pair, including root loops. The root's
potential is zero, not its loop value. The gauge criterion holds on arbitrary
types; the finite certificate criterion checks exactly the source's loops,
ascending two-way pairs and ascending three-term cycles, including n=0.
Pullback/re-normalization is coherent for every map. This is not the source's
fiber-sum identification, nor a machine verification of concrete programs.
-/
namespace WitnessedDifference.RootGaugeNormalization

universe u v
abbrev Table (V : Type u) := V → V → Int
variable {V : Type u} [DecidableEq V]

def potential (root : V) (e : Table V) (x : V) : Int :=
  if x=root then 0 else e x root
def normal (root : V) (e : Table V) : Table V :=
  fun x y => e x y - potential root e x + potential root e y
def shifted (e : Table V) (g : V → Int) : Table V :=
  fun x y => e x y + g x - g y

theorem potential_at_root (root : V) (e : Table V) : potential root e root = 0 := by
  simp [potential]

theorem potential_after_shift (root : V) (e : Table V) (g : V → Int) (x : V) :
    potential root (shifted e g) x = potential root e x + g x - g root := by
  by_cases h : x=root
  · subst x; simp [potential]
  · simp [potential,shifted,h]

theorem normal_after_shift (root : V) (e : Table V) (g : V → Int) :
    normal root (shifted e g) = normal root e := by
  funext x y
  simp only [normal,shifted,potential_after_shift]
  omega

theorem normal_column_at_nonroot (root : V) (e : Table V) (x : V) (distinct : x≠root) :
    normal root e x root = 0 := by
  simp [normal,potential,distinct]

theorem normal_preserves_loops (root : V) (e : Table V) (x : V) :
    normal root e x x = e x x := by
  unfold normal
  omega

theorem normal_preserves_two_way_sums (root : V) (e : Table V) (x y : V) :
    normal root e x y + normal root e y x = e x y + e y x := by
  unfold normal
  omega

theorem normal_preserves_round_sums (root : V) (e : Table V) (x y z : V) :
    normal root e x y + normal root e y z + normal root e z x =
      e x y + e y z + e z x := by
  unfold normal
  omega

theorem normal_is_idempotent (root : V) (e : Table V) :
    normal root (normal root e) = normal root e := by
  have hp : ∀ x, potential root (normal root e) x = 0 := by
    intro x
    by_cases h : x=root
    · subst x; exact potential_at_root root _
    · simp only [potential,if_neg h]
      exact normal_column_at_nonroot root e x h
  funext x y
  simp only [normal,hp]
  omega

theorem equal_normal_iff_gradient_difference (root : V) (e f : Table V) :
    normal root e = normal root f ↔
      ∃ g : V → Int, ∀ x y, f x y = e x y + g x - g y := by
  constructor
  · intro same
    refine ⟨fun x => potential root f x - potential root e x,?_⟩
    intro x y
    have h := congrFun (congrFun same x) y
    simp only [normal] at h
    dsimp
    omega
  · rintro ⟨g,hg⟩
    have h : f=shifted e g := by
      funext x y
      exact hg x y
    rw [h]
    exact (normal_after_shift root e g).symm

theorem zero_normal_iff_exact_gradient (root : V) (e : Table V) :
    (∀ x y, normal root e x y = 0) ↔ ∃ g : V → Int, ∀ x y, e x y = g x - g y := by
  constructor
  · intro zero
    refine ⟨potential root e,?_⟩
    intro x y
    have h := zero x y
    simp only [normal] at h
    omega
  · rintro ⟨g,hg⟩
    have h : e=shifted (fun _ _ => 0) g := by
      funext x y
      simp only [shifted,Int.zero_add]
      exact hg x y
    rw [h,normal_after_shift]
    simp [normal,potential]

def pullback {W : Type v} (f : W → V) (e : Table V) : Table W :=
  fun x y => e (f x) (f y)

omit [DecidableEq V] in
theorem pullback_shift {W : Type v} (f : W → V) (e : Table V) (g : V → Int) :
    pullback f (shifted e g) = shifted (pullback f e) (fun x => g (f x)) := rfl

theorem renormalize_after_pullback {W : Type v} [DecidableEq W]
    (f : W → V) (sourceRoot : V) (targetRoot : W) (e : Table V) :
    normal targetRoot (pullback f (normal sourceRoot e)) = normal targetRoot (pullback f e) := by
  have h : normal sourceRoot e = shifted e (fun x => -potential sourceRoot e x) := by
    funext x y
    simp only [normal,shifted]
    omega
  rw [h,pullback_shift,normal_after_shift]

def ObstructionFree (n : Nat) (e : Table Nat) : Prop :=
  (∀ x, x<n → e x x = 0) ∧
  (∀ x y, x<y → y<n → e x y + e y x = 0) ∧
  (∀ x y z, x<y → y<z → z<n → e x y + e y z + e z x = 0)
def FiniteNormalZero (n : Nat) (e : Table Nat) : Prop :=
  ∀ x y, x<n → y<n → normal 0 e x y = 0

theorem finite_obstruction_certificate_complete (n : Nat) (e : Table Nat) :
    FiniteNormalZero n e ↔ ObstructionFree n e := by
  constructor
  · intro zero
    refine ⟨?_,?_,?_⟩
    · intro x hx
      have h := zero x x hx hx
      rw [normal_preserves_loops] at h
      exact h
    · intro x y hxy hy
      have hx : x<n := by omega
      have h := normal_preserves_two_way_sums 0 e x y
      rw [zero x y hx hy,zero y x hy hx] at h
      omega
    · intro x y z hxy hyz hz
      have hx : x<n := by omega
      have hy : y<n := by omega
      have h := normal_preserves_round_sums 0 e x y z
      rw [zero x y hx hy,zero y z hy hz,zero z x hz hx] at h
      omega
  · intro h
    have ordered : ∀ a b, a<b → b<n → normal 0 e a b = 0 := by
      intro a b hab hb
      by_cases ha : a=0
      · subst a
        have pair := h.2.1 0 b hab hb
        have bne : b≠0 := by omega
        change e 0 b - (if (0:Nat)=0 then 0 else e 0 0) + (if b=0 then 0 else e b 0) = 0
        simp only [ite_true,if_neg bne]
        omega
      · have ha0 : 0<a := by omega
        have han : a<n := by omega
        have pair := h.2.1 0 a ha0 han
        have triangle := h.2.2 0 a b ha0 hab hb
        have bne : b≠0 := by omega
        change e a b - (if a=0 then 0 else e a 0) + (if b=0 then 0 else e b 0) = 0
        rw [if_neg ha,if_neg bne]
        omega
    intro x y hx hy
    by_cases same : x=y
    · subst y
      rw [normal_preserves_loops]
      exact h.1 x hx
    · by_cases before : x<y
      · exact ordered x y before hy
      · have reverse : y<x := by omega
        have hz := ordered y x reverse hx
        have pair := h.2.1 y x reverse hx
        have law := normal_preserves_two_way_sums 0 e x y
        omega

theorem finite_zero_normal_iff_exact_gradient (n : Nat) (e : Table Nat) :
    FiniteNormalZero n e ↔ ∃ g : Nat → Int, ∀ x y, x<n → y<n → e x y = g x - g y := by
  constructor
  · intro zero
    refine ⟨potential 0 e,?_⟩
    intro x y hx hy
    have h := zero x y hx hy
    simp only [normal] at h
    omega
  · rintro ⟨g,hg⟩ x y hx hy
    have hn : 0<n := by omega
    have hp : ∀ a, a<n → potential 0 e a = g a - g 0 := by
      intro a ha
      by_cases same : a=0
      · subst a; simp [potential]
      · simp only [potential,if_neg same]
        exact hg a 0 ha hn
    simp only [normal]
    rw [hp x hx,hp y hy,hg x y hx hy]
    omega

def raisingExcess (r s : Table V) (g : V → Int) : Table V :=
  fun x y => (r x y + if x=y then 0 else g x) - (s x y + if x=y then 0 else g y)

theorem raising_changes_excess_by_gradient (r s : Table V) (g : V → Int) :
    raisingExcess r s g = shifted (fun x y => r x y - s x y) g := by
  funext x y
  by_cases same : x=y
  · subst y
    simp only [raisingExcess,shifted,ite_true]
    omega
  · simp only [raisingExcess,shifted,if_neg same]
    omega

theorem raising_preserves_normal (root : V) (r s : Table V) (g : V → Int) :
    normal root (raisingExcess r s g) = normal root (fun x y => r x y - s x y) := by
  rw [raising_changes_excess_by_gradient,normal_after_shift]

end WitnessedDifference.RootGaugeNormalization

#print axioms WitnessedDifference.RootGaugeNormalization.potential_at_root
#print axioms WitnessedDifference.RootGaugeNormalization.potential_after_shift
#print axioms WitnessedDifference.RootGaugeNormalization.normal_after_shift
#print axioms WitnessedDifference.RootGaugeNormalization.normal_column_at_nonroot
#print axioms WitnessedDifference.RootGaugeNormalization.normal_preserves_loops
#print axioms WitnessedDifference.RootGaugeNormalization.normal_preserves_two_way_sums
#print axioms WitnessedDifference.RootGaugeNormalization.normal_preserves_round_sums
#print axioms WitnessedDifference.RootGaugeNormalization.normal_is_idempotent
#print axioms WitnessedDifference.RootGaugeNormalization.equal_normal_iff_gradient_difference
#print axioms WitnessedDifference.RootGaugeNormalization.zero_normal_iff_exact_gradient
#print axioms WitnessedDifference.RootGaugeNormalization.pullback_shift
#print axioms WitnessedDifference.RootGaugeNormalization.renormalize_after_pullback
#print axioms WitnessedDifference.RootGaugeNormalization.finite_obstruction_certificate_complete
#print axioms WitnessedDifference.RootGaugeNormalization.finite_zero_normal_iff_exact_gradient
#print axioms WitnessedDifference.RootGaugeNormalization.raising_changes_excess_by_gradient
#print axioms WitnessedDifference.RootGaugeNormalization.raising_preserves_normal
