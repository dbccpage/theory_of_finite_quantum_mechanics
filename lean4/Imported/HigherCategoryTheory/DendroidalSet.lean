/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/research_programs/higher_category_theory/DendroidalSet.lean
   Original sha256: f64ff0ca87c216ee8c1f3d43470c827fae69688b1feeba37ced8fff3cd9ec945 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.HigherCategoryTheory.DendroidalSet
   Reason         : HCT
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/-
DendroidalSet.lean
Pilot Formalization of the Planar Tree Category Ω and Minimal Dendroidal Set Inner Horn Filler Λ^e(T) → Ω(T).

AuthorityEffect: None.
Standard foundational axioms only: {propext, Quot.sound, Classical.choice}.
Zero sorry, zero admit.
-/

import Imported.HigherCategoryTheory.OperadicNerve

namespace HigherCategoryTheory

universe u

/-- A Corolla C_k in the planar tree category Ω is a rooted tree with a single vertex,
    k leaf edges (inputs), and 1 root edge (output). -/
structure Corolla (Colour : Type u) where
  arity : Nat
  inputs : List Colour
  output : Colour
  arity_eq : inputs.length = arity

/-- Minimal composite tree T_graft(p, q, i) in Ω obtained by grafting an upper corolla
    of arity q onto the i-th input leaf of a lower corolla of arity p.
    The grafted edge is the unique inner edge e of the tree. -/
structure GraftedTree (Colour : Type u) where
  p : Nat
  q : Nat
  i : Nat
  hi : i < p
  bot_inputs : List Colour
  bot_output : Colour
  top_inputs : List Colour
  top_output : Colour
  bot_len : bot_inputs.length = p
  top_len : top_inputs.length = q
  inner_edge_match : bot_inputs.get ⟨i, by rw [bot_len]; exact hi⟩ = top_output

/-- The contracted corolla ∂_e(T_graft) obtained by contracting the unique inner edge e.
    The resulting corolla has arity p + q - 1, output bot_output, and inputs
    obtained by substituting top_inputs into the i-th position of bot_inputs. -/
def contractInnerEdge {Colour : Type u} (T : GraftedTree Colour) : Corolla Colour where
  arity := T.p + T.q - 1
  inputs := (T.bot_inputs.take T.i) ++ T.top_inputs ++ (T.bot_inputs.drop (T.i + 1))
  output := T.bot_output
  arity_eq := by
    rw [List.length_append, List.length_append]
    rw [List.length_take, List.length_drop, T.bot_len, T.top_len]
    have hmin : min T.i T.p = T.i := Nat.min_eq_left (Nat.le_of_lt T.hi)
    rw [hmin]
    have hlt := T.hi
    omega

/-- An element of a Dendroidal Set evaluated on a corolla C_k:
    an operation with k inputs and 1 output in an operadic carrier O. -/
structure CorollaSimplex (O : ColouredOperad.{u}) (C : Corolla O.Colour) where
  op : O.Op C.inputs C.output

/-- An element of a Dendroidal Set evaluated on the grafted tree T_graft:
    a pair of operations (top, bot) assigned to the two vertices together with
    the composite operation assigned to the contracted tree. -/
structure GraftedTreeSimplex (O : ColouredOperad.{u}) (T : GraftedTree O.Colour) where
  top_op : O.Op T.top_inputs T.top_output
  bot_op : O.Op T.bot_inputs T.bot_output
  composite_op : O.Op (contractInnerEdge T).inputs T.bot_output

/-- Elementary outer face d_top: drops the lower vertex, restricting to the upper corolla. -/
def dendroidal_face_top {O : ColouredOperad.{u}} {T : GraftedTree O.Colour}
    (sigma : GraftedTreeSimplex O T) : CorollaSimplex O ⟨T.q, T.top_inputs, T.top_output, T.top_len⟩ where
  op := sigma.top_op

/-- Elementary outer face d_bot: drops the upper vertex, restricting to the lower corolla. -/
def dendroidal_face_bot {O : ColouredOperad.{u}} {T : GraftedTree O.Colour}
    (sigma : GraftedTreeSimplex O T) : CorollaSimplex O ⟨T.p, T.bot_inputs, T.bot_output, T.bot_len⟩ where
  op := sigma.bot_op

/-- Elementary inner face d_e: contracts the inner edge e, yielding the composite operation. -/
def dendroidal_face_inner {O : ColouredOperad.{u}} {T : GraftedTree O.Colour}
    (sigma : GraftedTreeSimplex O T) : CorollaSimplex O (contractInnerEdge T) where
  op := sigma.composite_op

/-- An Inner Horn Λ^e(T_graft) on the minimal grafted tree:
    consists of the two outer faces (d_top and d_bot) meeting at the inner edge e.
    Crucially, the inner face ∂_e(T) is omitted! -/
structure DendroidalInnerHorn (O : ColouredOperad.{u}) (T : GraftedTree O.Colour) where
  x_top : O.Op T.top_inputs T.top_output
  x_bot : O.Op T.bot_inputs T.bot_output

/-- Linear tree specialization: When p = 1 and q = 1, T_graft has two unary vertices
    and 1 inner edge, corresponding to the 2-simplex Δ^2 in the simplicial spine. -/
def linearTree2 (Colour : Type u) (c0 c1 c2 : Colour) : GraftedTree Colour where
  p := 1
  q := 1
  i := 0
  hi := Nat.lt_succ_self 0
  bot_inputs := [c1]
  bot_output := c2
  top_inputs := [c0]
  top_output := c1
  bot_len := rfl
  top_len := rfl
  inner_edge_match := rfl

/-- Theorem: For the linear tree, contracted inner edge inputs collapse to [c0]. -/
theorem linearTree2_contracted_inputs (Colour : Type u) (c0 c1 c2 : Colour) :
    (contractInnerEdge (linearTree2 Colour c0 c1 c2)).inputs = [c0] := by
  dsimp [contractInnerEdge, linearTree2]
  rfl

/-- Constructive Inner Horn Filler for the linear tree case (p = 1, q = 1):
    Fills Λ^e(T_linear) by assigning the unary operadic composite O.comp1 x_bot x_top
    to the contracted inner face. -/
def fillLinearDendroidalInnerHorn (O : ColouredOperad.{u}) {c0 c1 c2 : O.Colour}
    (horn : DendroidalInnerHorn O (linearTree2 O.Colour c0 c1 c2)) :
    GraftedTreeSimplex O (linearTree2 O.Colour c0 c1 c2) where
  top_op := horn.x_top
  bot_op := horn.x_bot
  composite_op := by
    have hEq : (contractInnerEdge (linearTree2 O.Colour c0 c1 c2)).inputs = [c0] :=
      linearTree2_contracted_inputs O.Colour c0 c1 c2
    rw [hEq]
    exact O.comp1 horn.x_bot horn.x_top

/-- Theorem: The dendroidal filler matches the outer face d_top. -/
theorem fillLinear_matches_top (O : ColouredOperad.{u}) {c0 c1 c2 : O.Colour}
    (horn : DendroidalInnerHorn O (linearTree2 O.Colour c0 c1 c2)) :
    dendroidal_face_top (fillLinearDendroidalInnerHorn O horn) = ⟨horn.x_top⟩ :=
  rfl

/-- Theorem: The dendroidal filler matches the outer face d_bot. -/
theorem fillLinear_matches_bot (O : ColouredOperad.{u}) {c0 c1 c2 : O.Colour}
    (horn : DendroidalInnerHorn O (linearTree2 O.Colour c0 c1 c2)) :
    dendroidal_face_bot (fillLinearDendroidalInnerHorn O horn) = ⟨horn.x_bot⟩ :=
  rfl

/-- Theorem: The inner face of the filler is the exact unary operadic composite. -/
theorem fillLinear_inner_face_eq_composite (O : ColouredOperad.{u}) {c0 c1 c2 : O.Colour}
    (horn : DendroidalInnerHorn O (linearTree2 O.Colour c0 c1 c2)) :
    dendroidal_face_inner (fillLinearDendroidalInnerHorn O horn) =
      ⟨by
        have hEq : (contractInnerEdge (linearTree2 O.Colour c0 c1 c2)).inputs = [c0] :=
          linearTree2_contracted_inputs O.Colour c0 c1 c2
        rw [hEq]
        exact O.comp1 horn.x_bot horn.x_top⟩ :=
  rfl

/-- Every linear-tree inner horn admits a filler whose outer faces recover the horn.
    The missing inner face equals the unary composite by `fillLinear_inner_face_eq_composite`. -/
theorem dendroidal_linear_inner_horn_fills (O : ColouredOperad.{u}) (c0 c1 c2 : O.Colour) :
    ∀ (horn : DendroidalInnerHorn O (linearTree2 O.Colour c0 c1 c2)),
      ∃ (sigma : GraftedTreeSimplex O (linearTree2 O.Colour c0 c1 c2)),
        (dendroidal_face_top sigma).op = horn.x_top ∧
        (dendroidal_face_bot sigma).op = horn.x_bot := by
  intro horn
  exact ⟨fillLinearDendroidalInnerHorn O horn, rfl, rfl⟩

/-- On the arity-1 tree, the dendroidal filler's composite equals the simplicial inner-horn filler's missing face. -/
theorem dendroidal_simplicial_nerve_agreement (O : ColouredOperad.{u}) (c0 c1 c2 : O.Colour)
    (f01 : O.Op [c0] c1) (f12 : O.Op [c1] c2) :
    let horn_dend : DendroidalInnerHorn O (linearTree2 O.Colour c0 c1 c2) := ⟨f01, f12⟩
    let horn_simp : InnerHorn2_1 O := ⟨⟨c1, c2, f12⟩, ⟨c0, c1, f01⟩, rfl⟩
    (fillLinearDendroidalInnerHorn O horn_dend).composite_op =
      (fillInnerHorn2_1 O horn_simp).f02 := by
  rfl

end HigherCategoryTheory
