import Std
namespace ReportFiberDescent
universe u v w z
abbrev Image {X : Type u} {R : Type v} (report : X → R) := {r : R // ∃ x, report x = r}
def lifted {X : Type u} {R : Type v} (report : X → R) (x : X) : Image report := ⟨report x, x, rfl⟩
def ConstantOnFibers {X : Type u} {R : Type v} {D : Type w} (r : X → R) (d : X → D) :=
  ∀ x y, r x = r y → d x = d y

theorem unique_decoder_iff {X : Type u} {R : Type v} {D : Type w}
    (report : X → R) (decision : X → D) :
    (∃ decoder : Image report → D, (∀ x, decoder (lifted report x) = decision x) ∧
      ∀ other : Image report → D, (∀ x, other (lifted report x) = decision x) → other = decoder) ↔
    ConstantOnFibers report decision := by
  constructor
  · rintro ⟨decoder, h, _⟩ x y he
    have hi : lifted report x = lifted report y := Subtype.ext he
    exact (h x).symm.trans ((congrArg decoder hi).trans (h y))
  · intro h
    classical
    let decoder : Image report → D := fun r => decision (Classical.choose r.property)
    have hd : ∀ x, decoder (lifted report x) = decision x := by
      intro x; exact h _ x (Classical.choose_spec (lifted report x).property)
    refine ⟨decoder, hd, ?_⟩
    intro other ho; funext r
    obtain ⟨x, hx⟩ := r.property
    have hr : lifted report x = r := Subtype.ext hx
    rw [← hr, ho, hd]

theorem postprocess_obstruction {X : Type u} {R : Type v} {S : Type z} {D : Type w}
    (r : X → R) (p : R → S) (d : X → D) (x y : X)
    (same : r x = r y) (different : d x ≠ d y) :
    ¬ ConstantOnFibers (p ∘ r) d := by
  intro h; exact different (h x y (congrArg p same))

theorem joint_report_sufficient {X : Type u} {R : Type v} {D : Type w}
    (r : X → R) (d : X → D) : ConstantOnFibers (fun x => (r x, d x)) d := by
  intro x y h; exact congrArg Prod.snd h

theorem lost_bit_obstruction : ¬ ConstantOnFibers (fun _ : Bool => ()) (fun b : Bool => b) := by
  intro h; have bad := h false true rfl; cases bad
end ReportFiberDescent
#print axioms ReportFiberDescent.unique_decoder_iff
#print axioms ReportFiberDescent.postprocess_obstruction
#print axioms ReportFiberDescent.joint_report_sufficient
#print axioms ReportFiberDescent.lost_bit_obstruction
