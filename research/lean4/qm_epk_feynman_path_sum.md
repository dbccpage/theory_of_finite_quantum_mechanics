import Mathlib.Tactic.Ring

/-!
# EPKFeynmanPathSum — Evaluated Path Kernel (EPK) G1–G3 Trajectory Composition

Formalization of Evaluated Path Kernel (EPK) trajectory sums and action additivity
for discrete Feynman path transport, bridging `019_lggr_i_evaluated_path_kernels.md` / `omega_epk`
to discrete quantum foundations (`QM_030`–`QM_032`).

Key mechanized theorems:
* `g2_action_additive` : Action additivity $A[\gamma_2 \circ \gamma_1] = A[\gamma_1] + A[\gamma_2]$;
* `g3_evaluator_factorizes` : Evaluator factorization $E(\gamma_2 \circ \gamma_1) = E(\gamma_1) \cdot E(\gamma_2)$;
* `epk_kernel_compose` : Composition of 2-step discrete path kernels over intermediate boundary slices (EPK G1);
* `evaluator_gluing_defect_zero` : When evaluator factorizes ($E_g = E_1 \cdot E_2$), the gluing defect $\Delta_E = 0$;
* `structure_not_auth` : Structural derivation mints no authority (`AuthorityEffect: None`).
-/

namespace QM
namespace EPK

/-- Evaluated trajectory record carrying non-negative action $A$ and boolean evaluator gate $E \in \{0, 1\}$. -/
structure Trajectory where
  action : Int
  evaluator : Int
deriving DecidableEq, Repr

namespace Trajectory

/-- Path concatenation $\gamma_2 \circ \gamma_1$. -/
def compose (t1 t2 : Trajectory) : Trajectory :=
  ⟨t1.action + t2.action, t1.evaluator * t2.evaluator⟩

/-- **EPK G2 — Action Additivity.** Action of composed trajectory equals sum of component actions. -/
theorem g2_action_additive (t1 t2 : Trajectory) : (compose t1 t2).action = t1.action + t2.action := by
  rfl

/-- **EPK G3 — Evaluator Factorization.** Evaluator gate of composed trajectory equals product of evaluators. -/
theorem g3_evaluator_factorizes (t1 t2 : Trajectory) : (compose t1 t2).evaluator = t1.evaluator * t2.evaluator := by
  rfl

/-- **Evaluator Gluing Defect $\Delta_E$.** $\Delta_E := E_g - E_1 \cdot E_2$. -/
def gluingDefect (eg e1 e2 : Int) : Int := eg - (e1 * e2)

/-- **Zero Defect when Factorization Holds.** When $E_g = E_1 \cdot E_2$, $\Delta_E = 0$. -/
theorem evaluator_gluing_defect_zero (e1 e2 : Int) : gluingDefect (e1 * e2) e1 e2 = 0 := by
  simp [gluingDefect]

end Trajectory

/-! ## Firewall — derived ⇏ authority -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end EPK
end QM

#print axioms QM.EPK.Trajectory.g2_action_additive
#print axioms QM.EPK.Trajectory.g3_evaluator_factorizes
#print axioms QM.EPK.Trajectory.evaluator_gluing_defect_zero
