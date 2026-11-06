import ClassicalModel
import QubitModel
import ConcreteJordanProducts

/-! Supported part of the reviewed state-catalogue contract. Every classical tag and both
qubit spellings have constructed models. Unsupported tags have no fabricated fallback.
This is a state-space catalogue; matrix-algebra identification and classification remain separate. -/
noncomputable section
open scoped Classical
namespace FiniteQM.SupportedJordanCatalogue
open Set ReconstructionGeometry ReconstructionArithmetic ClassicalExclusion

/-- A single fully calibrated entry of the existing state-catalogue contract. -/
structure Entry (J : EJA) where
  ambient : ℕ
  model : System ambient
  model_dim : model.dim = J.dim
  model_rank : model.rank = J.rank
  classical_geometry : J.IsClassical → FinitePolytope model.states
  qubit_geometry : ∀ s, J.summands = [s] → s.IsQubitAlgebra →
    ∃ e : Space ambient ≃ᵃ[ℝ] Space 3, e '' model.states = ball3

def Supported (J : EJA) : Prop :=
  J.IsClassical ∨ ∃ s, J.summands = [s] ∧ s.IsQubitAlgebra

theorem qubit_invariants (J : EJA) (s : SimpleEJA) (hs : J.summands = [s])
    (hq : s.IsQubitAlgebra) : J.rank = 2 ∧ J.dim = 4 := by
  rcases hq with rfl | rfl <;>
    simp [EJA.rank, EJA.dim, hs, sumRank, sumDim, SimpleEJA.rank, SimpleEJA.dim]

theorem qubit_not_classical (J : EJA) (s : SimpleEJA) (hs : J.summands = [s])
    (hq : s.IsQubitAlgebra) : ¬ J.IsClassical := by
  intro hc
  have h1 := hc s (by simp [hs])
  rcases hq with rfl | rfl <;> simp [SimpleEJA.rank] at h1

def classicalEntry (J : EJA) (hc : J.IsClassical) : Entry J where
  ambient := J.rank - 1
  model := ClassicalModel.system (J.rank - 1)
  model_dim := by
    change (J.rank - 1) + 1 = J.dim
    rw [EJA.classical_dim_eq_rank J hc]
    have h := J.rank_pos
    omega
  model_rank := by
    change (J.rank - 1) + 1 = J.rank
    have h := J.rank_pos
    omega
  classical_geometry := fun _ => ClassicalModel.finite_polytope _
  qubit_geometry := by
    intro s hs hq
    exact False.elim (qubit_not_classical J s hs hq hc)

def qubitEntry (J : EJA) (s : SimpleEJA) (hs : J.summands = [s])
    (hq : s.IsQubitAlgebra) : Entry J where
  ambient := 3
  model := QubitModel.system
  model_dim := (qubit_invariants J s hs hq).2.symm
  model_rank := (qubit_invariants J s hs hq).1.symm
  classical_geometry := fun hc => False.elim (qubit_not_classical J s hs hq hc)
  qubit_geometry := fun _ _ _ => ⟨AffineEquiv.refl ℝ (Space 3), QubitModel.state_chart⟩

/-- Total on precisely the supported subset. Classical choice only selects proved witnesses. -/
def entry (J : EJA) (supported : Supported J) : Entry J :=
  if hc : J.IsClassical then classicalEntry J hc else
    let hq := supported.resolve_left hc
    qubitEntry J (Classical.choose hq) (Classical.choose_spec hq).1 (Classical.choose_spec hq).2

theorem classical_entry_calibrated (J : EJA) (hc : J.IsClassical) :
    (classicalEntry J hc).model.rank = J.rank ∧ (classicalEntry J hc).model.dim = J.dim :=
  ⟨(classicalEntry J hc).model_rank, (classicalEntry J hc).model_dim⟩

theorem supported_entry_calibrated (J : EJA) (h : Supported J) :
    (entry J h).model.rank = J.rank ∧ (entry J h).model.dim = J.dim :=
  ⟨(entry J h).model_rank, (entry J h).model_dim⟩

def complexQubitTag : EJA where
  summands := [.complexHerm 2]
  nonempty := by decide
  wf := by intro s hs; simp only [List.mem_singleton] at hs; subst s; decide

def spinQubitTag : EJA where
  summands := [.spin 3]
  nonempty := by decide
  wf := by intro s hs; simp only [List.mem_singleton] at hs; subst s; decide

theorem complexQubit_supported : Supported complexQubitTag :=
  Or.inr ⟨.complexHerm 2, rfl, Or.inl rfl⟩
theorem spinQubit_supported : Supported spinQubitTag :=
  Or.inr ⟨.spin 3, rfl, Or.inr rfl⟩

/-- Extension operation only. The unbuilt entries remain an explicit argument, not a new axiom. -/
def completeEntry (remaining : ∀ J, ¬ Supported J → Entry J) (J : EJA) : Entry J :=
  if h : Supported J then entry J h else remaining J h

def completeCatalogue (remaining : ∀ J, ¬ Supported J → Entry J) : JordanStateCatalogue where
  ambient J := (completeEntry remaining J).ambient
  model J := (completeEntry remaining J).model
  model_dim J := (completeEntry remaining J).model_dim
  model_rank J := (completeEntry remaining J).model_rank
  classical_geometry J := (completeEntry remaining J).classical_geometry
  qubit_geometry J := (completeEntry remaining J).qubit_geometry

theorem extension_agrees (remaining : ∀ J, ¬ Supported J → Entry J) (J : EJA) (h : Supported J) :
    completeEntry remaining J = entry J h := by simp [completeEntry, h]

#print axioms qubit_invariants
#print axioms qubit_not_classical
#print axioms classicalEntry
#print axioms qubitEntry
#print axioms entry
#print axioms classical_entry_calibrated
#print axioms supported_entry_calibrated
#print axioms complexQubit_supported
#print axioms spinQubit_supported
#print axioms completeCatalogue
#print axioms extension_agrees
end FiniteQM.SupportedJordanCatalogue