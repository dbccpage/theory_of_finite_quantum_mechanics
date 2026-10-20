import Mathlib.Algebra.Group.Basic
import Mathlib.Tactic.Group

/-!
General graph dressing over an arbitrary group. No finiteness, commutativity,
matrix representation, or continuum hypothesis is used by the algebraic proof.
The finite application supplies a root and a tree path in each component.
AuthorityEffect: None.
-/
namespace FiniteGraphDressing

variable {V E G : Type*} [Group G] (src dst : E → V)

inductive Walk : V → V → Type _ where
  | nil (v : V) : Walk v v
  | edge (e : E) : Walk (src e) (dst e)
  | reverse {a b : V} (p : Walk a b) : Walk b a
  | append {a b c : V} (p : Walk a b) (q : Walk b c) : Walk a c

def transport (U : E → G) : {a b : V} → Walk src dst a b → G
  | _, _, .nil _ => 1
  | _, _, .edge e => U e
  | _, _, .reverse p => (transport U p)⁻¹
  | _, _, .append p q => transport U q * transport U p

def dress (U : E → G) (u : V → G) (e : E) : G :=
  u (dst e) * U e * (u (src e))⁻¹

theorem dress_eq_one_iff (U : E → G) (u : V → G) (e : E) :
    dress src dst U u e = 1 ↔ U e = (u (dst e))⁻¹ * u (src e) := by
  constructor
  · intro h
    calc
      U e = (u (dst e))⁻¹ * dress src dst U u e * u (src e) := by
        simp only [dress]
        group
      _ = (u (dst e))⁻¹ * u (src e) := by rw [h]; group
  · intro h
    simp [dress, h]

theorem transport_of_pure (U : E → G) (u : V → G)
    (h : ∀ e, U e = (u (dst e))⁻¹ * u (src e))
    {a b : V} (p : Walk src dst a b) :
    transport src dst U p = (u b)⁻¹ * u a := by
  induction p with
  | nil v => simp [transport]
  | edge e => exact h e
  | reverse p ih => simp [transport, ih]
  | append p q ihp ihq =>
      simp only [transport, ihp, ihq]
      group

/-- Connected form; apply separately to each component of a finite graph. -/
theorem neutralizable_iff_closed_walks (U : E → G) (root : V)
    (paths : ∀ v, Walk src dst root v) :
    (∃ u : V → G, ∀ e, dress src dst U u e = 1) ↔
      ∀ v (p : Walk src dst v v), transport src dst U p = 1 := by
  constructor
  · rintro ⟨u, hu⟩ v p
    have hp := transport_of_pure src dst U u
      (fun e => (dress_eq_one_iff src dst U u e).mp (hu e)) p
    simpa using hp
  · intro h
    refine ⟨fun v => (transport src dst U (paths v))⁻¹, ?_⟩
    intro e
    have hc := h root (.append (.append (paths (src e)) (.edge e))
      (.reverse (paths (dst e))))
    simpa [dress, transport, mul_assoc] using hc

theorem loop_residual {r r' a b : V} (U : E → G) (hr : r = r')
    (p : Walk src dst r a) (q : Walk src dst r' b) (e : Walk src dst a b)
    (h : ∀ v (w : Walk src dst v v), transport src dst U w = 1) :
    (transport src dst U q)⁻¹ * transport src dst U e * transport src dst U p = 1 := by
  cases hr
  have hc := h r (.append (.append p e) (.reverse q))
  simpa [transport, mul_assoc] using hc

/-- Disconnected form: roots and paths are supplied by a spanning forest. -/
theorem neutralizable_iff_closed_walks_forest (U : E → G) (root : V → V)
    (paths : ∀ v, Walk src dst (root v) v)
    (edgeRoots : ∀ e, root (src e) = root (dst e)) :
    (∃ u : V → G, ∀ e, dress src dst U u e = 1) ↔
      ∀ v (p : Walk src dst v v), transport src dst U p = 1 := by
  constructor
  · rintro ⟨u, hu⟩ v p
    have hp := transport_of_pure src dst U u
      (fun e => (dress_eq_one_iff src dst U u e).mp (hu e)) p
    simpa using hp
  · intro h
    refine ⟨fun v => (transport src dst U (paths v))⁻¹, ?_⟩
    intro e
    have hc := loop_residual src dst U (edgeRoots e)
      (paths (src e)) (paths (dst e)) (.edge e) h
    simpa [dress, transport] using hc

/-- The finite chord test needs a supplied rooted tree transport, not an enumeration of walks. -/
theorem tree_dressing_iff (U : E → G) (T : V → G) :
    (∀ e, dress src dst U (fun v => (T v)⁻¹) e = 1) ↔
      ∀ e, U e * T (src e) = T (dst e) := by
  constructor
  · intro h e
    have hp := (dress_eq_one_iff src dst U (fun v => (T v)⁻¹) e).mp (h e)
    simp only [inv_inv] at hp
    rw [hp]
    group
  · intro h e
    simp only [dress, inv_inv]
    rw [mul_assoc, h e]
    simp

theorem change_dressing (U : E → G) (u u' : V → G) (e : E) :
    dress src dst U u' e =
      (u' (dst e) * (u (dst e))⁻¹) * dress src dst U u e *
        (u' (src e) * (u (src e))⁻¹)⁻¹ := by
  simp only [dress]
  group

/-- Any two global neutralizers differ by a left constant on a connected component. -/
theorem neutralizers_constant (U : E → G) (u u' : V → G)
    (hu : ∀ e, dress src dst U u e = 1)
    (hu' : ∀ e, dress src dst U u' e = 1)
    {a b : V} (p : Walk src dst a b) :
    u' b * (u b)⁻¹ = u' a * (u a)⁻¹ := by
  have hp := transport_of_pure src dst U u
    (fun e => (dress_eq_one_iff src dst U u e).mp (hu e)) p
  have hp' := transport_of_pure src dst U u'
    (fun e => (dress_eq_one_iff src dst U u' e).mp (hu' e)) p
  have heq : (u b)⁻¹ * u a = (u' b)⁻¹ * u' a := hp.symm.trans hp'
  calc
    u' b * (u b)⁻¹ = u' b * ((u b)⁻¹ * u a) * (u a)⁻¹ := by group
    _ = u' b * ((u' b)⁻¹ * u' a) * (u a)⁻¹ := by rw [heq]
    _ = u' a * (u a)⁻¹ := by group

#print axioms neutralizable_iff_closed_walks
#print axioms neutralizable_iff_closed_walks_forest
#print axioms tree_dressing_iff
#print axioms change_dressing
#print axioms neutralizers_constant
end FiniteGraphDressing
