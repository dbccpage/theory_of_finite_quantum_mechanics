/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/Level80ScopedAuthorization.lean
   Original sha256: e89838df09f2d24fdb50a02a04a25fbfe870269b19b639c0e9d2d7dee454db9f (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.SymbolGameLoose.Level80ScopedAuthorization
   Reason         : MSS-N
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/-
Copyright (c) 2026 The Symbol Game Authors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: The Symbol Game Authors
-/

/-!
# Level 80: Scoped Authorization and Non-Escalating Delegation

Formal verification kernel for MSS-80 / GEN-080:
1. Exact authorization bounds for (Principal, Action, Resource) tuples.
2. Grant scope confinement: actions outside declared scope are refused.
3. Monotonic delegation attenuation: child grants cannot broaden parent scope.
4. Non-escalation theorem: ungranted capabilities in parent cannot be derived by child.

AuthorityEffect: None.
-/

namespace MSSN.Level80

/-- Finite declared principals in the authorization regime. -/
inductive Principal where
  | root : Principal
  | admin : Principal
  | operator : Principal
  | guest : Principal
  deriving DecidableEq, Repr

/-- Declared finite actions. -/
inductive Action where
  | read : Action
  | write : Action
  | execute : Action
  deriving DecidableEq, Repr

/-- Declared finite resources. -/
inductive Resource where
  | publicData : Resource
  | metrics : Resource
  | config : Resource
  | keys : Resource
  deriving DecidableEq, Repr

/-- Atomic permission pair combining an action and target resource. -/
structure Permission where
  action : Action
  resource : Resource
  deriving DecidableEq, Repr

/-- Scope is a predicate selecting admitted permissions. -/
def Scope := Permission → Prop

/-- Permission membership in a scope. -/
def InScope (perm : Permission) (s : Scope) : Prop :=
  s perm

/-- Explicit authorization grant issued by an authority to a subject. -/
structure Grant where
  grantId : Nat
  issuer : Principal
  subject : Principal
  scope : Scope

/-- Predicate: a principal is authorized for a permission under grant `g`. -/
def isAuthorized (g : Grant) (p : Principal) (perm : Permission) : Prop :=
  g.subject = p ∧ InScope perm g.scope

/-- Soundness of authorized execution: authorization implies scope membership. -/
theorem authorization_soundness (g : Grant) (p : Principal) (perm : Permission)
    (h : isAuthorized g p perm) : InScope perm g.scope ∧ g.subject = p :=
  ⟨h.2, h.1⟩

/-- Falsification/refusal of action out of scope. -/
theorem unauthorized_action_refused (g : Grant) (p : Principal) (perm : Permission)
    (h : ¬ InScope perm g.scope) : ¬ isAuthorized g p perm := by
  intro h_auth
  exact h h_auth.2

/-- Falsification/refusal of subject mismatch. -/
theorem unauthorized_principal_refused (g : Grant) (p : Principal) (perm : Permission)
    (h : g.subject ≠ p) : ¬ isAuthorized g p perm := by
  intro h_auth
  exact h h_auth.1

/-- Sub-scope relation: every permission in `s₁` is present in `s₂`. -/
def isSubScope (s₁ s₂ : Scope) : Prop :=
  ∀ perm, InScope perm s₁ → InScope perm s₂

/-- Delegation chain step: issuer of child must be subject of parent, and scope must attenuate. -/
structure DelegationChain where
  parent : Grant
  child : Grant
  valid_issuer : child.issuer = parent.subject
  attenuation : isSubScope child.scope parent.scope

/-- Monotonic delegation non-escalation: child grant permissions are subset of parent grant. -/
theorem delegation_non_escalation (d : DelegationChain) (p : Principal) (perm : Permission)
    (h_child_auth : isAuthorized d.child p perm) :
    InScope perm d.parent.scope := by
  have h_in_child : InScope perm d.child.scope := h_child_auth.2
  exact d.attenuation perm h_in_child

/-- Strict privilege escalation refusal: parent ungranted permission cannot be authorized by child. -/
theorem privilege_escalation_impossible (d : DelegationChain) (p : Principal) (perm : Permission)
    (h_not_in_parent : ¬ InScope perm d.parent.scope) :
    ¬ isAuthorized d.child p perm := by
  intro h_child_auth
  have h_in_parent := delegation_non_escalation d p perm h_child_auth
  exact h_not_in_parent h_in_parent

#print axioms authorization_soundness
#print axioms unauthorized_action_refused
#print axioms unauthorized_principal_refused
#print axioms delegation_non_escalation
#print axioms privilege_escalation_impossible

end MSSN.Level80
