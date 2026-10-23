import D01D02Records
import T01FactorizationFiberConstancy
import T02BridgeAdmissibility

/-!
# CODA-CS-Q T03: Named Terminalizer Agreement & Step-8 Independence (BRIDGE-006)

Formalizes:
1. Named terminal maps τ_Q and τ_CODA-CS pointwise agreement.
2. Factorization implies named query terminals agree.
3. Independence from flags: terminal agreement is NOT automatic from boolean flags alone.
4. Step-8 discharge for query-via-(q_bar ∘ Prof).

AuthorityEffect: None.
-/

namespace CodaCsQ

open CodaCsQ

set_option linter.unusedVariables false

variable {α β γ : Type}

/-- Query-via-factor terminals: τ_Q := q, τ_CODA-CS := q_bar ∘ Prof. -/
def query_via_qbar_prof_terminals (Prof : α → β) (q : α → γ) (q_bar : β → γ) :
    NamedTerminalizers α γ where
  tau_q := q
  tau_coda_cs := fun x => q_bar (Prof x)

/-- Factorization implies named query terminals agree. -/
theorem factorization_implies_named_terminalizers_agree
    (Prof : α → β) (q : α → γ) (q_bar : β → γ)
    (h : profile_factorization Prof q q_bar) :
    terminalizers_agree (query_via_qbar_prof_terminals Prof q q_bar) := by
  intro x
  exact h x

/-- Counterexample showing terminal agreement does not follow from flags alone. -/
def disagreeing_bool_terminals : NamedTerminalizers Bool Bool where
  tau_q := id
  tau_coda_cs := fun _ => true

theorem terminalizers_not_automatic_from_flags :
    ¬ terminalizers_agree disagreeing_bool_terminals := by
  intro h
  have h_contra := h false
  dsimp [disagreeing_bool_terminals] at h_contra
  contradiction

theorem terminalizers_disagree_despite_true_flags :
    (True ∧ True ∧ True) ∧ ¬ terminalizers_agree disagreeing_bool_terminals :=
  ⟨⟨trivial, trivial, trivial⟩, terminalizers_not_automatic_from_flags⟩

def factorization_discharges_named_query_step8
    (Prof : α → β) (q : α → γ) (q_bar : β → γ)
    (h : profile_factorization Prof q q_bar) :
    TerminalAgreement α γ where
  named := query_via_qbar_prof_terminals Prof q q_bar
  pointwise := factorization_implies_named_terminalizers_agree Prof q q_bar h

theorem admissible_profile_fact_discharges_query_step8
    (packet : BridgePacket14 α β γ)
    (adm : BridgeAdmissible8 packet) :
    terminalizers_agree
      (query_via_qbar_prof_terminals packet.Prof packet.q packet.q_bar) :=
  factorization_implies_named_terminalizers_agree
    packet.Prof packet.q packet.q_bar adm.profile_fact

end CodaCsQ
