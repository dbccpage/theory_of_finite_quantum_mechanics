import GenesisHottHorns

/-!
# A 0-truncated deep embedding of a small identity-type fragment

AuthorityEffect: None.

This file does not add univalence. It does not postulate a univalent universe,
an ∞-groupoid, or an (∞,1)-category. Those three names are imports in the
derivation note, not axioms and not theorems.

The object language is a fragment with one bound variable of type `vtx`,
constants for the three vertices of `GenesisHottHorns`, reflexivity,
a dependent product `Π (_ : vtx), B` whose body may mention the variable
through an identity type, application, and weakening of closed judgments.
Identity elimination (`J`) is not a rule of the fragment. It is open.

Interpretation. Closed and open terms are read in the vertex set of the
Stage A carrier. An identity type is interpreted as a Lean equality of
vertices, so it has at most one element: the model is 0-truncated, and its
identity types are mere propositions. The 1-simplices of the carrier are not
identity proofs: `edge_reading_refutes_refl` uses `no_loop`.

`soundness` says that every derivation is interpreted by a semantic value
that fits its type. `vertex_id_elim` is path induction for motives valued
in `Sort u` along equalities of vertices. It is not object-language `J`.
-/

namespace GenesisHottModel

open GenesisHottHorns

universe u

inductive Term where
  | cst (v : Vtx)
  | bvar
  | refl (t : Term)
  | lam (body : Term)
  | app (f a : Term)
  deriving DecidableEq

inductive Ty where
  | vtx
  | iden (t1 t2 : Term)
  | pi (body : Ty)
  deriving DecidableEq

inductive Ctx where
  | emp
  | ext

def substTerm (t a : Term) : Term :=
  match t with
  | .cst v => .cst v
  | .bvar => a
  | .refl u => .refl (substTerm u a)
  | .lam b => .lam b
  | .app f x => .app (substTerm f a) (substTerm x a)

def substTy (A : Ty) (a : Term) : Ty :=
  match A with
  | .vtx => .vtx
  | .iden t1 t2 => .iden (substTerm t1 a) (substTerm t2 a)
  | .pi B => .pi B

/-- Derivation trees of the fragment. There is no `J` constructor. -/
inductive Deriv : Ctx → Term → Ty → Type where
  | cst (Γ : Ctx) (v : Vtx) : Deriv Γ (.cst v) .vtx
  | bvar : Deriv .ext .bvar .vtx
  | refl {Γ : Ctx} {t : Term} : Deriv Γ t .vtx → Deriv Γ (.refl t) (.iden t t)
  | lam {body : Term} {B : Ty} : Deriv .ext body B → Deriv .emp (.lam body) (.pi B)
  | app {f a : Term} {B : Ty} :
      Deriv .emp f (.pi B) → Deriv .emp a .vtx →
        Deriv .emp (.app f a) (substTy B a)
  | weaken {t : Term} {A : Ty} : Deriv .emp t A → Deriv .ext t A

inductive Sem where
  | vtx (v : Vtx)
  | pth (a b : Vtx)
  | fn (f : Vtx → Sem)

def interp (t : Term) (env : Vtx) : Sem :=
  match t with
  | .cst v => .vtx v
  | .bvar => .vtx env
  | .refl u =>
      match interp u env with
      | .vtx v => .pth v v
      | s => s
  | .lam body => .fn (fun x => interp body x)
  | .app f a =>
      match interp f env, interp a env with
      | .fn g, .vtx v => g v
      | _, _ => .vtx .v0

def fits (s : Sem) : Ty → Vtx → Prop
  | .vtx, _ =>
      match s with
      | .vtx _ => True
      | _ => False
  | .iden t1 t2, env =>
      match s with
      | .pth a b =>
          match interp t1 env, interp t2 env with
          | .vtx x, .vtx y => a = x ∧ b = y ∧ a = b
          | _, _ => False
      | _ => False
  | .pi B, _ =>
      match s with
      | .fn g => ∀ x, fits (g x) B x
      | _ => False

theorem interp_subst (body a : Term) (env v : Vtx) (ha : interp a env = .vtx v) :
    interp (substTerm body a) env = interp body v := by
  induction body with
  | cst _ => rfl
  | bvar =>
      simpa [substTerm, interp] using ha
  | refl _ ih =>
      simp [substTerm, interp, ih]
  | lam _ _ =>
      rfl
  | app _ _ ihf ihx =>
      simp [substTerm, interp, ihf, ihx]

theorem fits_vtx_inv (s : Sem) (env : Vtx) (h : fits s .vtx env) : ∃ v, s = .vtx v := by
  cases s with
  | vtx v => exact ⟨v, rfl⟩
  | pth _ _ => cases h
  | fn _ => cases h

theorem fits_pi_inv (s : Sem) (B : Ty) (env : Vtx) (h : fits s (.pi B) env) :
    ∃ g, s = .fn g ∧ ∀ x, fits (g x) B x := by
  cases s with
  | fn g => exact ⟨g, rfl, h⟩
  | vtx _ => cases h
  | pth _ _ => cases h

theorem fits_subst (B : Ty) (s : Sem) (a : Term) (env v : Vtx)
    (ha : ∀ env', interp a env' = .vtx v) :
    fits s B v ↔ fits s (substTy B a) env := by
  cases B with
  | vtx =>
      cases s <;> simp [fits, substTy]
  | pi _ =>
      cases s <;> simp [fits, substTy]
  | iden t1 t2 =>
      have h1 := interp_subst t1 a env v (ha env)
      have h2 := interp_subst t2 a env v (ha env)
      cases s <;> simp [fits, substTy, h1, h2]

/-- A term reads the outer vertex environment only through a free `bvar`. -/
def usesBvar : Term → Bool
  | .cst _ => false
  | .bvar => true
  | .refl u => usesBvar u
  | .lam _ => false
  | .app f a => usesBvar f || usesBvar a

theorem interp_indep (t : Term) (env env' : Vtx) (h : usesBvar t = false) :
    interp t env = interp t env' := by
  induction t with
  | cst _ => rfl
  | bvar =>
      simp [usesBvar] at h
  | refl _ ih =>
      simp [usesBvar] at h
      simp [interp, ih h]
  | lam _ _ =>
      rfl
  | app _ _ ihf iha =>
      simp [usesBvar] at h
      simp [interp, ihf h.1, iha h.2]

theorem deriv_emp_no_bvar {Γ t A} (d : Deriv Γ t A) (hΓ : Γ = .emp) : usesBvar t = false := by
  induction d with
  | cst _ _ => rfl
  | bvar => cases hΓ
  | refl d ih =>
      simpa [usesBvar] using ih hΓ
  | lam _ _ =>
      rfl
  | app df da ihf iha =>
      have hf := ihf rfl
      have ha := iha rfl
      simp [usesBvar, hf, ha]
  | weaken _ _ =>
      cases hΓ

theorem interp_closed {t A} (d : Deriv .emp t A) (env env' : Vtx) :
    interp t env = interp t env' :=
  interp_indep t env env' (deriv_emp_no_bvar d rfl)

theorem soundness_refl {t : Term} (env : Vtx) (ih : fits (interp t env) .vtx env) :
    fits (interp (.refl t) env) (.iden t t) env := by
  rcases fits_vtx_inv _ _ ih with ⟨v, hv⟩
  have hinter : interp (.refl t) env = .pth v v := by
    simp [interp, hv]
  simp [fits, hinter, hv]

theorem soundness_app {f a : Term} {B : Ty}
    (da : Deriv .emp a .vtx)
    (ihf : ∀ env, fits (interp f env) (.pi B) env)
    (iha : ∀ env, fits (interp a env) .vtx env) (env : Vtx) :
    fits (interp (.app f a) env) (substTy B a) env := by
  rcases fits_vtx_inv _ _ (iha env) with ⟨v, hv⟩
  rcases fits_pi_inv _ _ _ (ihf env) with ⟨g, hg, hgfit⟩
  have hclosed : ∀ env', interp a env' = .vtx v := by
    intro env'
    rcases fits_vtx_inv _ _ (iha env') with ⟨v', hv'⟩
    have heq := interp_closed da env env'
    rw [hv, hv'] at heq
    cases heq
    exact hv'
  have happ : interp (.app f a) env = g v := by
    simp [interp, hg, hv]
  rw [happ]
  exact (fits_subst B (g v) a env v hclosed).mp (hgfit v)

theorem soundness {Γ t A} (d : Deriv Γ t A) (env : Vtx) :
    fits (interp t env) A env := by
  induction d generalizing env with
  | cst Γ v =>
      simp [interp, fits]
  | bvar =>
      simp [interp, fits]
  | refl d ih =>
      exact soundness_refl env (ih env)
  | lam d ih =>
      intro x
      exact ih x
  | app df da ihf iha =>
      exact soundness_app da ihf iha env
  | weaken d ih =>
      exact ih env

/-- Path induction along vertex equalities, into any `Sort u`.
Ambient eliminator on `Vtx`. Not a syntactic `J` rule. -/
def vertex_id_elim {a : Vtx} (C : ∀ x : Vtx, a = x → Sort u)
    (c : C a rfl) {x : Vtx} (p : a = x) : C x p :=
  match p with
  | rfl => c

theorem vertex_id_elim_prop {a : Vtx} (C : ∀ x : Vtx, a = x → Prop)
    (c : C a rfl) {x : Vtx} (p : a = x) : C x p :=
  vertex_id_elim C c p

theorem identity_zero_truncated (a b : Vtx) (p q : a = b) : p = q := by
  cases p
  cases q
  rfl

theorem transport_refl {C : Vtx → Sort u} {a : Vtx} (c : C a) :
    Eq.rec (motive := fun x _ => C x) c (Eq.refl a) = c := rfl

theorem edge_reading_refutes_refl (v : Vtx) :
    ¬ ∃ e : Edge, src e = v ∧ tgt e = v := by
  intro ⟨e, hs, ht⟩
  exact no_loop e (hs.trans ht.symm)

theorem no_path_between_cut_endpoints (s : Sem) (env : Vtx) :
    ¬ fits s (.iden (.cst .v0) (.cst .v1)) env := by
  intro h
  cases s with
  | vtx _ => cases h
  | fn _ => cases h
  | pth a b =>
      simp [fits, interp] at h
      rcases h with ⟨ha, hb, hab⟩
      exact cut_endpoints_apart ((ha.symm.trans hab).trans hb)

inductive BaseCode where
  | unitC
  | reflC
  deriving DecidableEq

theorem toRefl (u : Unit) : Vtx.v0 = Vtx.v0 := by
  cases u
  rfl

def toUnit : (Vtx.v0 = Vtx.v0) → Unit := fun _ => ()

theorem toUnit_toRefl (u : Unit) : toUnit (toRefl u) = u := rfl

theorem toRefl_toUnit (p : Vtx.v0 = Vtx.v0) : toRefl (toUnit p) = p := by
  cases p
  rfl

theorem base_codes_distinct : BaseCode.unitC ≠ BaseCode.reflC := by
  intro h
  cases h

/-- The two codes have inverse interpretations, and they are not equal.
Code equality does not match bijection of carriers in this two-point set. -/
theorem code_univalence_fails :
    (∀ u : Unit, toUnit (toRefl u) = u) ∧
      (∀ p : Vtx.v0 = Vtx.v0, toRefl (toUnit p) = p) ∧
        BaseCode.unitC ≠ BaseCode.reflC :=
  ⟨toUnit_toRefl, toRefl_toUnit, base_codes_distinct⟩

def reflV0 : Term := .refl (.cst .v0)

def reflV0Deriv : Deriv .emp reflV0 (.iden (.cst .v0) (.cst .v0)) :=
  Deriv.refl (Deriv.cst .emp .v0)

theorem reflV0_typed :
    Nonempty (Deriv .emp reflV0 (.iden (.cst .v0) (.cst .v0))) :=
  ⟨reflV0Deriv⟩

def reflLam : Term := .lam (.refl .bvar)

def reflLamDeriv : Deriv .emp reflLam (.pi (.iden .bvar .bvar)) :=
  Deriv.lam (Deriv.refl Deriv.bvar)

theorem reflLam_typed :
    Nonempty (Deriv .emp reflLam (.pi (.iden .bvar .bvar))) :=
  ⟨reflLamDeriv⟩

def reflAt (v : Vtx) : Term := .app reflLam (.cst v)

def reflAtDeriv (v : Vtx) : Deriv .emp (reflAt v) (.iden (.cst v) (.cst v)) :=
  Deriv.app reflLamDeriv (Deriv.cst .emp v)

theorem reflAt_typed (v : Vtx) :
    Nonempty (Deriv .emp (reflAt v) (.iden (.cst v) (.cst v))) :=
  ⟨reflAtDeriv v⟩

theorem id_cut_endpoints_uninhabited (t : Term)
    (d : Deriv .emp t (.iden (.cst .v0) (.cst .v1))) : False :=
  no_path_between_cut_endpoints (interp t .v0) .v0 (soundness d .v0)

theorem hott_fragment_status :
    fits (interp reflV0 .v0) (.iden (.cst .v0) (.cst .v0)) .v0 ∧
      (∀ (a b : Vtx) (p q : a = b), p = q) ∧
        (∀ v, ¬ ∃ e : Edge, src e = v ∧ tgt e = v) ∧
          BaseCode.unitC ≠ BaseCode.reflC :=
  ⟨soundness reflV0Deriv .v0,
    identity_zero_truncated,
    edge_reading_refutes_refl,
    base_codes_distinct⟩

end GenesisHottModel

#print axioms GenesisHottModel.interp_subst
#print axioms GenesisHottModel.fits_vtx_inv
#print axioms GenesisHottModel.fits_pi_inv
#print axioms GenesisHottModel.fits_subst
#print axioms GenesisHottModel.interp_indep
#print axioms GenesisHottModel.deriv_emp_no_bvar
#print axioms GenesisHottModel.interp_closed
#print axioms GenesisHottModel.soundness_refl
#print axioms GenesisHottModel.soundness_app
#print axioms GenesisHottModel.soundness
#print axioms GenesisHottModel.vertex_id_elim
#print axioms GenesisHottModel.vertex_id_elim_prop
#print axioms GenesisHottModel.identity_zero_truncated
#print axioms GenesisHottModel.transport_refl
#print axioms GenesisHottModel.edge_reading_refutes_refl
#print axioms GenesisHottModel.no_path_between_cut_endpoints
#print axioms GenesisHottModel.toUnit_toRefl
#print axioms GenesisHottModel.toRefl_toUnit
#print axioms GenesisHottModel.base_codes_distinct
#print axioms GenesisHottModel.code_univalence_fails
#print axioms GenesisHottModel.reflV0_typed
#print axioms GenesisHottModel.reflLam_typed
#print axioms GenesisHottModel.reflAt_typed
#print axioms GenesisHottModel.id_cut_endpoints_uninhabited
#print axioms GenesisHottModel.hott_fragment_status
