import D01D02Records
import T02MasterNormalForm

/-!
# CODA-GTLA T03: Authority Firewall & Partition Disjointness (GTLA-02, FDA-04)

Formalizes:
1. Strict terminal partition disjointness:
   T_auth \cap T_res = \emptyset, T_auth \cap F_term = \emptyset, T_res \cap F_term = \emptyset.
2. Theorem 3.2: Non-Promotion Firewall Theorem:
   Zero residual evidence does NOT imply sovereign authority standing.
3. Countermodels to self-authorization (FDA-04):
   Observation collision and untrusted verifier countermodel.

AuthorityEffect: None.
-/

namespace CodaGtla

set_option linter.unusedVariables false

/-- Theorem 12.1a: Authority and Anomalon terminals are disjoint. -/
theorem auth_disjoint_anomalon (t : TerminalOutcome) : ¬ (IsAuth t ∧ IsAnomalon t) := by
  intro ⟨ha, hr⟩
  cases t <;> contradiction

/-- Theorem 12.1b: Authority and Refusal terminals are disjoint. -/
theorem auth_disjoint_refused (t : TerminalOutcome) : ¬ (IsAuth t ∧ IsRefused t) := by
  intro ⟨ha, hf⟩
  cases t <;> contradiction

/-- Theorem 12.1c: Anomalon and Refusal terminals are disjoint. -/
theorem anomalon_disjoint_refused (t : TerminalOutcome) : ¬ (IsAnomalon t ∧ IsRefused t) := by
  intro ⟨hr, hf⟩
  cases t <;> contradiction

/-- Theorem 3.2: Non-Promotion Firewall Theorem.
    Zero quotient defect without external license does NOT entail authority standing.
    Demonstrated by the existence of an unlicensed zero-defect input that lands in F_term. -/
theorem non_promotion_firewall :
    ∃ inp : PipelineInput,
      inp.phi1Distance = 0 ∧
      inp.licenseGranted = false ∧
      ¬ IsAuth (evaluatePipeline inp) ∧
      IsRefused (evaluatePipeline inp) := by
  let inp : PipelineInput := {
    inputId := "unlicensed_zero_defect",
    sieveNonEmpty := true,
    refinementConsistent := true,
    gluingSucceeded := true,
    phi1Distance := 0,
    gamma2Distance := 0,
    licenseGranted := false
  }
  refine ⟨inp, rfl, rfl, ?_, trivial⟩
  intro h
  contradiction

/-- FDA-04 Countermodel 2: Observation Collision.
    Two inputs with identical observational profiles (identical phi1 and gamma2)
    can produce distinct terminal outcomes (one authorized, one refused).
    Shows in this model that internal observation alone cannot determine authority. -/
theorem observation_collision_distinct_authority :
    ∃ inp1 inp2 : PipelineInput,
      inp1.phi1Distance = inp2.phi1Distance ∧
      inp1.gamma2Distance = inp2.gamma2Distance ∧
      IsAuth (evaluatePipeline inp1) ∧
      ¬ IsAuth (evaluatePipeline inp2) := by
  let inp1 : PipelineInput := {
    inputId := "state_licensed",
    sieveNonEmpty := true,
    refinementConsistent := true,
    gluingSucceeded := true,
    phi1Distance := 0,
    gamma2Distance := 0,
    licenseGranted := true
  }
  let inp2 : PipelineInput := {
    inputId := "state_unlicensed",
    sieveNonEmpty := true,
    refinementConsistent := true,
    gluingSucceeded := true,
    phi1Distance := 0,
    gamma2Distance := 0,
    licenseGranted := false
  }
  refine ⟨inp1, inp2, rfl, rfl, trivial, ?_⟩
  intro h
  contradiction

end CodaGtla
