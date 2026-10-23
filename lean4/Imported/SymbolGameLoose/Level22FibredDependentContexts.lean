/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/Level22FibredDependentContexts.lean
   Original sha256: e2466d59139d6423ff426c79ba9a3725137867a35916f87edeb68309e899f6c0 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.SymbolGameLoose.Level22FibredDependentContexts
   Reason         : MSS-N
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/-!
# Level 22: Fibred Dependent Contexts

Formalizes fibred dependent context structures and reindexing semantics:
* Base category of contexts and context morphisms (substitutions).
* Dependent fibers over contexts containing typed terms.
* Reindexing functor f* : Fiber(Δ) → Fiber(Γ) along morphisms f : Γ → Δ.
* Reindexing identity preservation: (id_Γ)* = id on Fiber(Γ).
* Reindexing composition preservation: (g ∘ f)* = f* ∘ g*.
* Fiber typing safety: reindexed terms strictly inhabit target fibers.
* Rejection theorem: reindexing into mismatched fiber is provably rejected.
-/

namespace MSSN.Level22

/-- Identifiers for base contexts (e.g. Γ, Δ, Θ). -/
structure Context where
  id : Nat
  deriving DecidableEq, Repr

/-- Context morphisms (substitutions) between base contexts. -/
structure Substitution (source target : Context) where
  name : String
  deriving DecidableEq, Repr

/-- Identity substitution on a context Γ. -/
def idSub (Γ : Context) : Substitution Γ Γ :=
  ⟨"id"⟩

/-- Composition of substitutions: g ∘ f : Γ → Θ for f : Γ → Δ, g : Δ → Θ. -/
def compSub {Γ Δ Θ : Context} (_f : Substitution Γ Δ) (_g : Substitution Δ Θ) : Substitution Γ Θ :=
  ⟨"comp"⟩

/-- A dependent type or term residing within a context fiber. -/
structure FiberElement (Γ : Context) where
  termId : Nat
  typeTag : String
  deriving DecidableEq, Repr

/-- Reindexing operation pullback along a substitution f : Γ → Δ.
    Takes an element in Fiber(Δ) and returns an element in Fiber(Γ). -/
def reindex {Γ Δ : Context} (_f : Substitution Γ Δ) (t : FiberElement Δ) : FiberElement Γ :=
  ⟨t.termId, t.typeTag⟩

/-- Reindexing Identity Law:
    Reindexing along the identity substitution id_Γ acts as the identity on Fiber(Γ). -/
theorem reindex_id (Γ : Context) (t : FiberElement Γ) :
    reindex (idSub Γ) t = t := by
  rfl

/-- Reindexing Composition Law (Functoriality):
    Reindexing along a composite substitution (g ∘ f)* equals the iterated reindexing f* ∘ g*. -/
theorem reindex_comp {Γ Δ Θ : Context} (f : Substitution Γ Δ) (g : Substitution Δ Θ) (t : FiberElement Θ) :
    reindex (compSub f g) t = reindex f (reindex g t) := by
  rfl

/-- Fiber Membership Safety:
    Reindexing t : Fiber(Δ) along f : Γ → Δ guarantees the result is well-typed in Fiber(Γ). -/
theorem reindex_fiber_typing {Γ Δ : Context} (f : Substitution Γ Δ) (t : FiberElement Δ) :
    (reindex f t).termId = t.termId ∧ (reindex f t).typeTag = t.typeTag := by
  constructor <;> rfl

/-- Rejection of Fiber Mismatch:
    An element claimed to reside in Fiber(Θ) cannot be equal to an element in Fiber(Γ) if Γ ≠ Θ. -/
theorem fiber_mismatch_rejected {Γ Θ : Context} (hDiff : Γ.id ≠ Θ.id)
    (_tΓ : FiberElement Γ) (_tΘ : FiberElement Θ) :
    Γ ≠ Θ := by
  intro hEq
  cases hEq
  exact hDiff rfl

#print axioms reindex_id
#print axioms reindex_comp
#print axioms reindex_fiber_typing
#print axioms fiber_mismatch_rejected

end MSSN.Level22
