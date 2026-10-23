/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/research_programs/higher_category_theory/Master.lean
   Original sha256: 5606cc693b8a7380823a08175857cfa26bc679b4d0ab8a13e37104fb201ca80c (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.HigherCategoryTheory.Master
   Reason         : HCT
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/-
Copyright (c) 2026 Anomalon Research. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Worker M1 (Lean 4 HCT Formalization)
-/

import Imported.HigherCategoryTheory.Bicategory
import Imported.HigherCategoryTheory.TwoCategory
import Imported.HigherCategoryTheory.Monoidal
import Imported.HigherCategoryTheory.Braided
import Imported.HigherCategoryTheory.Ribbon
import Imported.HigherCategoryTheory.HigherFunctor
import Imported.HigherCategoryTheory.HigherNaturalTransformation
import Imported.HigherCategoryTheory.CoherenceTheorems
import Imported.HigherCategoryTheory.Regression
import Imported.HigherCategoryTheory.DGCategory
import Imported.HigherCategoryTheory.Triangulated
import Imported.HigherCategoryTheory.DerivedCategory
import Imported.HigherCategoryTheory.DoubleCategory
import Imported.HigherCategoryTheory.Enriched
import Imported.HigherCategoryTheory.ModelCategory
import Imported.HigherCategoryTheory.SimplicialSet
import Imported.HigherCategoryTheory.StableInfinityCategory
import Imported.HigherCategoryTheory.CompactlyGenerated
import Imported.HigherCategoryTheory.OperadicNerve
import Imported.HigherCategoryTheory.DendroidalSet

/-!
# Higher Category Theory Root Aggregator

This module serves as the master entrypoint for the `HigherCategoryTheory` library.
It re-exports the full categorical hierarchy across Phase 1, Phase 2, and Phase 3:

1. `Bicategory`: 0-cells, 1-cells, 2-cells, vertical/horizontal compositions,
   left/right whiskering, associator, unitors, middle-four interchange,
   and the Mac Lane pentagon and triangle axioms.
2. `TwoCategory`: Strict 2-categories where associators and unitors are identities,
   canonical equality-induced isomorphism `eqToIso2`, and laws on horizontal 2-cell composition.
3. `Monoidal`: Monoidal categories (tensor product, unit, associators, unitors)
   and the canonical one-object delooping theorem to a bicategory (`MonoidalCategory.toBicategory`).
4. `Braided`: Braided monoidal categories with natural braiding $\beta_{X,Y}$
   and the forward/reverse hexagon identities.
5. `Ribbon`: Rigid monoidal categories with duals, snake/zig-zag equations,
   ribbon twist automorphism $\theta_X$, quantum trace, and quantum dimension.
6. `HigherFunctor`: Weak 2-functors (pseudofunctors) with compositors and unitors,
   strict 2-functors, and the identity pseudofunctor.
7. `HigherNaturalTransformation`: Pseudonatural transformations, strict 2-natural
   endotransformations of the identity, and modifications with vertical composition.
8. `CoherenceTheorems`: Constructive coherence theorems for cartesian types,
   1-cell equality paths, and projections of assumed interchange and ribbon laws.
9. `Regression`: Explicit counterexamples and strictness refutations.
10. `DGCategory`: Differential Graded (DG) categories, graded Hom-modules,
    differential $d$ with $d^2 = 0$, graded Leibniz rule, closed degree 0 morphisms $Z^0$,
    chain homotopy equivalence, and the 0th cohomology category $H^0(\mathcal{C})$.
11. `Triangulated`: Additive categories, autoequivalence translation functor $T=[1]$,
    distinguished triangles, Verdier rotation TR2, morphism extension TR3,
    and the octahedral axiom TR4.
12. `DerivedCategory`: Chain complexes, 2x2 block morphism calculus, mapping cone
    $C(f) = D \oplus C[-1]$ with differential matrix squaring to zero identically,
    quasi-isomorphisms, roofs, bounded derived categories $\mathcal{D}^b(\mathcal{A})$,
    and unbounded derived categories $\mathcal{D}(\mathcal{A})$.
13. `DoubleCategory`: Double categories with horizontal/vertical categories, 2-cell squares,
    horizontal and vertical composition of squares, horizontal/vertical identity squares,
    and the middle-four square interchange law.
14. `Enriched`: $\mathcal{V}$-enriched categories over monoidal categories $\mathcal{V}$,
    composition morphisms, identity morphisms, enriched associativity diagram,
    enriched left/right unit diagrams, and underlying ordinary categories $\mathcal{C}_0$.
15. `ModelCategory`: Quillen model categories, weak equivalences, fibrations, cofibrations,
    2-out-of-3, retract closure, lifting properties, and functorial factorizations.
16. `SimplicialSet`: Simplicial sets $\Delta^{\text{op}} \to \text{Set}$, simplicial identities,
    horns $\Lambda^k_n$, Kan complexes, and quasi-categories ($(\infty, 1)$-categories).
17. `StableInfinityCategory`: Pointed quasi-categories, fiber/cofiber sequences, suspension $\Sigma$
    and loop $\Omega$ functors, mutual adjoint equivalence, and $\Omega$-spectra.
18. `CompactlyGenerated`: Compact objects, filtered colimits, and compactly generated categories.
-/

namespace HigherCategoryTheory

/-- Version and metadata record for the HigherCategoryTheory library. -/
def libraryVersion : String := "0.3.0"

end HigherCategoryTheory
