import Mathlib.Data.List.Basic

/-! AuthorityEffect: None. Reader/state/writer/error value semantics for total
callbacks. Rust Fn does not enforce purity, termination, panic freedom or lawful
Clone. Clone is an explicit arbitrary function here; side effects and concrete
invocation counts require separate source/trace evidence. No rollback theorem.
-/
namespace TFQM.ArrowEffects

def Arrow (R S E W A B : Type) := R → S → A → Except E (List W × S × B)

def lift (f : A → B) : Arrow R S E W A B := fun _ s a => .ok ([],s,f a)
def tell (w : W) : Arrow R S E W A A := fun _ s a => .ok ([w],s,a)
def compose (f : Arrow R S E W A B) (g : Arrow R S E W B C) : Arrow R S E W A C :=
  fun ctx s a => match f ctx s a with
  | .error e => .error e
  | .ok (w,s',b) => match g ctx s' b with
    | .error e => .error e
    | .ok (v,t,c) => .ok (w ++ v,t,c)
def fanout (clone : A → A) (f : Arrow R S E W A B) (g : Arrow R S E W A C) : Arrow R S E W A (B × C) :=
  fun ctx s a => match f ctx s (clone a) with
  | .error e => .error e
  | .ok (w,s',b) => match g ctx s' a with
    | .error e => .error e
    | .ok (v,t,c) => .ok (w ++ v,t,(b,c))
def split (f : Arrow R S E W A B) (g : Arrow R S E W C D) : Arrow R S E W (A × C) (B × D) :=
  fun ctx s (a,c) => match f ctx s a with
  | .error e => .error e
  | .ok (w,s',b) => match g ctx s' c with
    | .error e => .error e
    | .ok (v,t,d) => .ok (w ++ v,t,(b,d))
def choice (f : Arrow R S E W A C) (g : Arrow R S E W B C) : Arrow R S E W (Sum A B) C :=
  fun ctx s input => match input with
  | .inl a => f ctx s a
  | .inr b => g ctx s b

theorem lift_value (f : A → B) (ctx : R) (s : S) (a : A) :
    (lift f : Arrow R S E W A B) ctx s a = .ok ([],s,f a) := rfl
theorem tell_value (w : W) (ctx : R) (s : S) (a : A) :
    (tell w : Arrow R S E W A A) ctx s a = .ok ([w],s,a) := rfl
theorem compose_first_error (f : Arrow R S E W A B) (g : Arrow R S E W B C)
    (ctx : R) (s : S) (a : A) (e : E) (h : f ctx s a = .error e) :
    compose f g ctx s a = .error e := by simp [compose,h]
theorem compose_second_error (f : Arrow R S E W A B) (g : Arrow R S E W B C)
    (ctx : R) (s s' : S) (a : A) (b : B) (w : List W) (e : E)
    (hf : f ctx s a = .ok (w,s',b)) (hg : g ctx s' b = .error e) :
    compose f g ctx s a = .error e := by simp [compose,hf,hg]
theorem compose_success (f : Arrow R S E W A B) (g : Arrow R S E W B C)
    (ctx : R) (s s' t : S) (a : A) (b : B) (c : C) (w v : List W)
    (hf : f ctx s a = .ok (w,s',b)) (hg : g ctx s' b = .ok (v,t,c)) :
    compose f g ctx s a = .ok (w++v,t,c) := by simp [compose,hf,hg]
theorem compose_associative (f : Arrow R S E W A B) (g : Arrow R S E W B C) (h : Arrow R S E W C D) :
    compose (compose f g) h = compose f (compose g h) := by
  funext ctx s a
  cases hf : f ctx s a with
  | error e => simp [compose,hf]
  | ok value =>
    rcases value with ⟨w,s',b⟩
    cases hg : g ctx s' b with
    | error e => simp [compose,hf,hg]
    | ok value =>
      rcases value with ⟨v,t,c⟩
      cases hh : h ctx t c <;> simp [compose,hf,hg,hh,List.append_assoc]
theorem fanout_success (clone : A → A) (f : Arrow R S E W A B) (g : Arrow R S E W A C)
    (ctx : R) (s s' t : S) (a : A) (b : B) (c : C) (w v : List W)
    (hf : f ctx s (clone a) = .ok (w,s',b)) (hg : g ctx s' a = .ok (v,t,c)) :
    fanout clone f g ctx s a = .ok (w++v,t,(b,c)) := by simp [fanout,hf,hg]
theorem fanout_first_error (clone : A → A) (f : Arrow R S E W A B) (g : Arrow R S E W A C)
    (ctx : R) (s : S) (a : A) (e : E) (hf : f ctx s (clone a) = .error e) :
    fanout clone f g ctx s a = .error e := by simp [fanout,hf]
theorem split_success (f : Arrow R S E W A B) (g : Arrow R S E W C D)
    (ctx : R) (s s' t : S) (a : A) (b : B) (c : C) (d : D) (w v : List W)
    (hf : f ctx s a = .ok (w,s',b)) (hg : g ctx s' c = .ok (v,t,d)) :
    split f g ctx s (a,c) = .ok (w++v,t,(b,d)) := by simp [split,hf,hg]
theorem split_first_error (f : Arrow R S E W A B) (g : Arrow R S E W C D)
    (ctx : R) (s : S) (a : A) (c : C) (e : E) (hf : f ctx s a = .error e) :
    split f g ctx s (a,c) = .error e := by simp [split,hf]
theorem choice_left (f : Arrow R S E W A C) (g : Arrow R S E W B C) (ctx : R) (s : S) (a : A) :
    choice f g ctx s (.inl a) = f ctx s a := rfl
theorem choice_right (f : Arrow R S E W A C) (g : Arrow R S E W B C) (ctx : R) (s : S) (b : B) :
    choice f g ctx s (.inr b) = g ctx s b := rfl

end TFQM.ArrowEffects

#print axioms TFQM.ArrowEffects.lift_value
#print axioms TFQM.ArrowEffects.tell_value
#print axioms TFQM.ArrowEffects.compose_first_error
#print axioms TFQM.ArrowEffects.compose_second_error
#print axioms TFQM.ArrowEffects.compose_success
#print axioms TFQM.ArrowEffects.compose_associative
#print axioms TFQM.ArrowEffects.fanout_success
#print axioms TFQM.ArrowEffects.fanout_first_error
#print axioms TFQM.ArrowEffects.split_success
#print axioms TFQM.ArrowEffects.split_first_error
#print axioms TFQM.ArrowEffects.choice_left
#print axioms TFQM.ArrowEffects.choice_right
