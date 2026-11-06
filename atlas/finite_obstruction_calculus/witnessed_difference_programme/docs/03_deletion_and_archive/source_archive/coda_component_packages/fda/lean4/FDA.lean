import Foundations

/-!
CodaReconstruction.FDA

Self-contained reconstruction theorems for CODA-FDA (FDA-T5 through FDA-T8).
Includes:
- FDA-T5: terminal_has_history
- FDA-T6: routing_refusal_persists
- FDA-T7: standing_sound
- FDA-T8: untrusted_verifier_countermodel
- authority_not_observation
- replay_standing

Zero external dependencies; ordinary Lean 4 kernel only.
AuthorityEffect: None.
-/

namespace Coda.FDA

universe u v w

structure Regime (P : Type u) (E : Type v) (G : Type w) where
  verifies : P → E → Prop
  recordedGrant : G → P → Prop
  truth : P → Prop
  entitled : G → P → Prop

def Standing {P E G : Type _} (R : Regime P E G) (g : G) (p : P) : Prop :=
  (∃ e, R.verifies p e) ∧ R.recordedGrant g p

/-- FDA-T7: Standing is sound under two extra hypotheses (verifier soundness and grant soundness). -/
theorem standing_sound {P E G : Type _} (R : Regime P E G)
    (verifierSound : ∀ p e, R.verifies p e → R.truth p)
    (grantSound : ∀ g p, R.recordedGrant g p → R.entitled g p)
    {g : G} {p : P} (standing : Standing R g p) : R.truth p ∧ R.entitled g p := by
  obtain ⟨⟨e, he⟩, hg⟩ := standing
  exact ⟨verifierSound p e he, grantSound g p hg⟩

theorem authority_not_observation :
    ¬ Coda.Factors (fun _ : Bool => ()) (fun authorized : Bool => authorized) := by
  exact Coda.collision_obstructs_factor (x := false) (y := true) rfl (by decide)

/-- FDA-T8: Untrusted verifier countermodel — standing holds but truth fails without soundness hypotheses. -/
theorem untrusted_verifier_countermodel :
    ∃ R : Regime Unit Unit Unit, Standing R () () ∧ ¬ R.truth () := by
  exact ⟨⟨fun _ _ => True, fun _ _ => True, fun _ => False, fun _ _ => True⟩,
    ⟨⟨(), trivial⟩, trivial⟩, id⟩

theorem replay_standing {P E G : Type _} (R S : Regime P E G)
    (verify : ∀ p e, R.verifies p e → S.verifies p e)
    (grant : ∀ g p, R.recordedGrant g p → S.recordedGrant g p)
    {p : P} {g : G} (h : Standing R g p) : Standing S g p := by
  obtain ⟨⟨e, he⟩, hg⟩ := h
  exact ⟨⟨e, verify p e he⟩, grant g p hg⟩

/-- Stages are separate supplied maps; the result type exposes refusal. -/
structure Pipeline (P S X E T F : Type _) where
  route : P → Except F S
  descend : S → P → Except F X
  verify : S → X → Except F E
  terminalize : S → X → E → Except F T

def Pipeline.run {P S X E T F : Type _} (R : Pipeline P S X E T F) (p : P) : Except F T :=
  match R.route p with
  | .error f => .error f
  | .ok s => match R.descend s p with
    | .error f => .error f
    | .ok x => match R.verify s x with
      | .error f => .error f
      | .ok e => R.terminalize s x e

/-- FDA-T5: A successful terminal has an intermediate execution history. -/
theorem terminal_has_history {P S X E T F : Type _} (R : Pipeline P S X E T F)
    {p : P} {t : T} (h : R.run p = .ok t) :
    ∃ s x e, R.route p = .ok s ∧ R.descend s p = .ok x ∧
      R.verify s x = .ok e ∧ R.terminalize s x e = .ok t := by
  cases hs : R.route p with
  | error f => simp [Pipeline.run, hs] at h
  | ok s =>
    cases hx : R.descend s p with
    | error f => simp [Pipeline.run, hs, hx] at h
    | ok x =>
      cases he : R.verify s x with
      | error f => simp [Pipeline.run, hs, hx, he] at h
      | ok e =>
        exact ⟨s,x,e,rfl,hx,he,by simpa [Pipeline.run,hs,hx,he] using h⟩

/-- FDA-T6: A routing refusal persists and cannot be overwritten by later stages. -/
theorem routing_refusal_persists {P S X E T F : Type _} (R : Pipeline P S X E T F)
    {p : P} {f : F} (h : R.route p = .error f) : R.run p = .error f := by
  simp [Pipeline.run,h]

end Coda.FDA
