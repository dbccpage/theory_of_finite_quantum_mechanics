"""Check and bind the mathematical/refusal model, without exporting OLean files.

The receipt is proof-model evidence, not automatic Rust refinement or a grade.
Uses the repository's already prepared Lean/Mathlib project; never fetches it.
"""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

from run_audit import ROOT, digest, execute, write_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model",choices=("rank","category","metadata","degree","counter","parameters","finite-set","literal-reversal","shape-inventory","root-records","homology-protocols","degree-repair","two-step-complex","simplicial-closure","simplicial-boundary","simplicial-homology","scalar-admission","carrier-dimensions","vector-maps","graph-incidence","validation-inventory","arrow-effects","finite-builder","em-samples","lawvere-inventory","higher-functor-inventory","finite-functor","functor-operations","finite-naturality","natural-composition","joint-carrier","finite-simulation","finite-independence","finite-trace","finite-dagger","finite-groupoid","cauchy-inventory","tagged-coend","condensation-metadata","root-catalog","finite-profunctor-inventory","finite-continuation","finite-moore","partial-structure","finite-path","family-registry","functional-dependencies","functional-classification","finite-relational","joint-dynamics","history-context","context-reflection","finite-enumeration","cartesian-words","finite-partitions","minimum-colors","finite-geometry","weyl-bundles","surface-witnesses","fusion-admission","fusion-ring-model","fusion-scalars","braid-tensor-actions","modular-catalog"),default="rank")
    parser.add_argument("--memory-mb", type=int, default=1024,
        help="Explicit Lean memory limit, from 256 to 2048 MiB; default remains 1024.")
    args = parser.parse_args()
    if not 256 <= args.memory_mb <= 2048:
        parser.error("Lean memory must stay within 256..2048 MiB")
    model = args.model
    if model == "modular-catalog":
        proof_name, import_name, namespace = "ModularCatalog", "GroupTheory/OrderOfElement", "TFQM.ModularCatalog."
        declarations = ("signed_phase_period", "reduced_phase_order", "reduced_denominator_divides", "lcm_stays_bounded", "integer_phase_sum_bound", "phase_add_left", "phase_add_right", "phase_sub_left", "phase_sub_right", "quadratic_balancing", "zero_divisor_refused", "admitted_division", "cached_balancing", "indicator_factorization", "grouped_genus_sum", "equal_square_ratio", "phase_angle_bounds", "genus_exponent_fits", "right_diagonal_entry")
        scope = "Signed root periods and reduced phase orders, bounded bilinear phase arithmetic, checked-division model, exact modular caching/indicator/genus identities, rational angle bounds and actual right-diagonal matrix multiplication. No full Rust refinement, category realization, physical entropy interpretation or arbitrary bit-cost theorem."
    elif model == "braid-tensor-actions":
        proof_name, import_name, namespace = "BraidTensorActions", "Data/Fintype/Card", "TFQM.BraidTensorActions."
        declarations = ("run_append", "run_mul_left", "reachable_one", "reachable_step", "reachable_mul", "closed_run", "closed_exploration_exact", "finite_inverse", "frontier_step", "retained_and_scratch", "normalize_reconstruct", "normalize_pivot", "normalize_scale", "flip_involutive", "flipped_eq", "conjugation_apply", "outer_pair_conjugation")
        scope = "Actual ordered-word closure/minimality and finite-submonoid inverses in arbitrary ambient groups, exact scalar normalization, indexed frontier/storage arithmetic and actual matrix conjugation for outer tensor embedding. Rust refinement/bit costs/allocator bounds remain source-review obligations."
    elif model == "fusion-scalars":
        proof_name, import_name, namespace = "FusionScalars", "Data/Int/ModEq", "TFQM.FusionScalars."
        declarations = ("scaled_reduction", "residue_nonnegative", "residue_below_order", "exponent_bounds", "exponent_fits", "old_maximum_overflows", "maximum_reduced", "minimum_reduced")
        scope = "Exact modular scaling, nonnegative bounded residue/product and extreme signed witnesses. No extracted Rust refinement or generic client field-law proof."
    elif model == "fusion-ring-model":
        proof_name, import_name, namespace = "FusionRingModel", "LinearAlgebra/Matrix/Charpoly/Basic", "TFQM.FusionRingModel."
        declarations = ("advance_matrix", "matrix_word_product", "empty_word", "word_concatenation", "total_mass", "mass_bound", "power_growth_bound", "coefficient_square_bound", "rank_row_bound", "mixed_radix_digit", "integer_charpoly_embedding", "charge_monotone", "charge_acceptance", "prefix_failure_stays")
        scope = "Actual finite matrix path products and concatenation, total-mass/power bounds, exact coefficient/rank bounds, mixed-radix digit recovery, integer characteristic-polynomial embedding and monotone work admission. Full Rust refinement, spectral PF interpretation and categorical realization are separate source-review obligations."
    elif model == "fusion-admission":
        proof_name, import_name, namespace = "FusionAdmission", "Data/Rat/Defs", "TFQM.FusionAdmission."
        declarations = ("zero_denominator_refused", "exact_lift", "aggregate_exact", "aggregate_nonpositive", "aggregate_permutation", "cancellation_preserves_aggregate", "sum_step", "rank_admission", "bounded_cube", "admitted_level", "level_addition_fits", "maximum_level_overflows", "su2_subtraction_exact")
        scope = "Exact rational aggregate, malformed-denominator refusal, rank/cube/level admission and nontruncating SU2 subtraction. No complete fusion-law assessment, allocator theorem or full Rust refinement is claimed."
    elif model == "surface-witnesses":
        proof_name, import_name, namespace = "SurfaceWitnesses", "Data/Nat/Choose/Basic", "TFQM.SurfaceWitnesses."
        declarations = ("assemble_exact", "first_error", "factorial_error", "mub_error", "fano_error", "affine_error", "partition_acceptance", "partition_refusal", "listed_partition_count", "listed_partition_invariants", "fixed_factorial", "prime_bundle_count", "fano_pair_count", "affine_pair_count", "fixed_report")
        scope = "Fixed report assembly, ordered error propagation, scalar comparison and small exact list/arithmetic witnesses. Actual mathematical providers are separately reviewed; mutable reports are not admission tokens and no full Rust refinement is claimed."
    elif model == "weyl-bundles":
        proof_name, import_name, namespace = "WeylBundles", "Data/ZMod/Basic", "TFQM.WeylBundles."
        declarations = ("alternating", "antisymmetric", "additive", "ray_isotropic", "unique_direction", "distinct_directions_disjoint", "direction_count", "bundle_mass", "bundle_mass_bound", "basis_count_bound", "bounded_add", "bounded_product", "subtract_representative_safe", "singleton_admission", "bounded_plus_one")
        scope = "Actual alternating form, unique projective ray directions over fields, isotropy/disjointness, finite disjoint-bundle mass and d+1 bound, coordinate arithmetic and singleton admission. Rust-to-field/list correspondence and checked machine domain are separately reviewed; no eigenbasis construction."
    elif model == "finite-geometry":
        proof_name, import_name, namespace = "FiniteGeometry", "Data/ZMod/Basic", "TFQM.FiniteGeometry."
        declarations = ("slope_exists", "slope_unique", "same_x_excludes_slope", "fano_unique", "dot_symmetric", "equal_width_tails", "dot_cons", "adjacency_symmetric", "diagonal_false", "product_admission", "ray_pair_bound", "point_successor_safe", "affine_encoding_bound")
        scope = "Actual field affine-line existence/uniqueness, concrete Fano incidence, exact integer dot symmetry/step, irreflexive adjacency and bounded admission/index arithmetic. Checked-i64 prefix gates and complete Rust refinement are separately reviewed."
    elif model == "finite-partitions":
        proof_name, import_name, namespace = "FinitePartitions", "GroupTheory/Perm/Centralizer", "TFQM.FinitePartitions."
        declarations = ("admitted_parts", "admitted_sum", "member_bounded", "dp_previous_index", "dfs_child_smaller", "dfs_preserves_sum", "descending_child", "part_cursor_decreases", "admission_exact", "rows_before_cells", "cell_refusal", "grouped_denominator", "actual_conjugacy_size", "conjugacy_denominator_divides", "cycle_realization")
        scope = "Positive lists realize actual Nat.Partition; actual symmetric-group conjugacy size/integral denominator and cycle realization, plus DP/DFS arithmetic and ordered conservative cell admission. Complete Rust DP/enumerator and source-to-multiset correspondence remain separate review obligations."
    elif model == "minimum-colors":
        proof_name, import_name, namespace = "MinimumColors", "Data/List/Basic", "TFQM.MinimumColors."
        declarations = ("undirected_symmetric", "new_candidate", "strict_improvement", "tie_keeps_first", "update_good", "fold_good", "minimum_good", "minimum_none_iff", "minimum_optimal", "zero_stays", "zero_global", "positive_word_count", "work_bound")
        scope = "Actual finite candidate argmin, membership/global optimality, stable ties, valid zero early termination, undirected constraints and exact work bounds. Rust graph admission/index order, Cartesian coverage and buffer ownership correspondence are separately reviewed."
    elif model == "cartesian-words":
        proof_name, import_name, namespace = "CartesianWords", "Data/Nat/Choose/Basic", "TFQM.CartesianWords."
        declarations = ("value_bound", "advance_success", "exhausted_value", "exhausted_iff", "digit_remainder", "tail_quotient", "value_injective", "nullary_count", "empty_alphabet", "width_admitted", "increment_fits")
        scope = "Admitted digit range, positional-value bound/injectivity, exact carry successor, maximal exhaustion and width/increment boundaries, with least-significant-first model words. Rust reverse-Vec traversal, bounded ownership/admission and costs are separately reviewed."
    elif model == "finite-enumeration":
        proof_name, import_name, namespace = "FiniteEnumeration", "Data/Nat/Choose/Basic", "TFQM.FiniteEnumeration."
        declarations = ("factorial_exact", "binomial_step", "binomial_step_integral", "binomial_loop_exact", "binomial_final", "symmetric_choice", "choose_outside", "numerator_fits", "composition_count", "no_parts_nonzero", "empty_composition", "admission_exact", "width_first", "rows_before_cells", "cells_refused", "pivot_sum", "pivot_increment_fits", "pivot_remainder_lt", "subset_increment_fits")
        scope = "Exact factorial/binomial recurrences including integral division, multichoose identity, ordered resource refusal and arithmetic pivot/subset bounds. Rust iterator storage, complete lexicographic enumeration, admission correspondence and costs are separately reviewed."
    elif model == "rank":
        proof_name, import_name, namespace = "RankCertificate", "LinearAlgebra/Matrix/Rank", "TFQM.RankCertificate."
        declarations = ("valid_rank","runChecks_ok_iff","admit_success","admit_success_rank",
            "producer_failure","explicit_failure","failed_predicate","first_error_preserved",
            "row_major_index_lt","pivot_increment_fits","augmented_column_lt","identity_area_le")
        scope = "Exact Q-matrix rank theorem and explicit-refusal model."
    elif model == "category":
        proof_name, import_name, namespace = "FiniteCategory", "CategoryTheory/Category/Basic", "TFQM.FiniteCategory."
        declarations = ("checks_true_iff","admit_preserves_data","admit_success_laws","failed_guard",
            "composite_spec","composeArrow_spec","identity_compose","compose_identity",
            "compose_associative","categoryOfAdmitted")
        scope = "Finite table admission realizes Mathlib Category; explicit guard refusal and data preservation."
    elif model == "metadata":
        proof_name, import_name, namespace = "MetadataValidation", "Data/List/Basic", "TFQM.MetadataValidation."
        declarations = ("success_iff", "failed_head", "valid_head", "first_error_preserved",
                        "inspect_preserves_raw", "failed_check_returns_no_value")
        scope = "Ordered metadata predicates, exact first-error preservation and raw-value observation; no mathematical law certification."
    elif model == "degree":
        proof_name, import_name, namespace = "DegreeWindow", "Data/Int/Basic", "TFQM.DegreeWindow."
        declarations = ("ordered_span_fits_u32", "same_endpoint_zero", "inverted_span_negative")
        scope = "Exact i32 endpoint difference bounds, zero span and inverted-window refusal premise; no category-law claim."
    elif model == "context-reflection":
        proof_name, import_name, namespace = "ContextReflection", "CategoryTheory/NatTrans", "TFQM.ContextReflection."
        declarations = ("arrow_ext", "contextCategory", "composition_map", "identity_map", "reflect_congruent", "saturation_preserved", "unit", "factor", "factor_triangle", "factor_unique", "reflectMap", "reflectFunctor", "unitNatural", "factorEquiv", "factor_natural_left", "factor_natural_right", "saturated_iff_of_congruent", "reflection_idempotent", "reflecting_congruent", "obstruction_no_reflecting", "unit_reflects_iff")
        scope = "Actual Mathlib contextual category,congruence reflector/natural identity-carrier unit and Hom equivalence,unique comma factor and no reflecting repair;Rust finite admission/canonical merge refinement separate."
    elif model == "history-context":
        proof_name, import_name, namespace = "HistoryContext", "Data/Set/Lattice", "TFQM.HistoryContext."
        declarations = ("run_empty", "run_append", "step_source", "step_control", "step_output", "product_correct", "product_append", "final_correct", "reachable_successor", "closed_covers_all", "factor_spec", "factor_iff", "collision_refuses", "lifted_action", "lift_requires_reachable", "lift_exists")
        scope = "Exact all-word transducer/product/final-emission semantics,kernel descent on realized profiles and reachable-state action lifting;finite BFS/Rust refinement separate."
    elif model == "joint-dynamics":
        proof_name, import_name, namespace = "JointDynamics", "Data/Set/Lattice", "TFQM.JointDynamics."
        declarations = ("unavailable", "defined_found", "defined_missing", "no_missing_as_unavailable", "success_found", "refusal_missing", "left_none", "left_some", "right_none", "right_some", "left_closure", "no_collision_iff", "collision_no_factor", "factor_spec", "factor_unique", "paired_profile", "defined_observably_distinct")
        scope = "Closed partial coordinate updates,missing-target refusal versus genuine unavailability,paired profile fibers and collision/factor boundary;Rust admission costs/provider all-word refinement separate."
    elif model == "finite-relational":
        proof_name, import_name, namespace = "FiniteRelational", "Data/Set/Lattice", "TFQM.FiniteRelational."
        declarations = ("equality_bisim", "flip_bisim", "compose_bisim", "contains", "greatest_refl", "greatest_symm", "greatest_trans", "greatest_bisim", "greatest_reports", "bounded_kernel", "bounded_fibers", "factor_spec", "factor_unique", "coverage_iff", "reach_trans", "reach_least", "le_refl", "le_trans", "scc_refl", "scc_symm", "scc_trans", "representative_invariant", "strict_irreflexive", "strict_trans", "distinct_components_strict")
        scope = "Greatest strong report bisimulation,bounded fibers/factors,behavior class coverage,positive reachability and SCC strict order;finite partition/W arshall/source refinement separate."
    elif model == "functional-classification":
        proof_name, import_name, namespace = "FunctionalClassification", "Data/List/Basic", "TFQM.FunctionalClassification."
        declarations = ("factor_spec", "factor_iff", "injective_fibers", "linked_stable", "functional_necessary", "recognized_injective_iff", "empty_word", "injective_minimal", "inactive_run", "inactive_future", "inactive_minimal", "inactive_bijective", "retention_injective_necessity", "retention_inactive_necessity", "singleton_injective", "singleton_no_tolerance", "singleton_inactive", "singleton_minimal", "twenty_signatures", "implication_countermodel_iff")
        scope = "Universal factor/stability and all-word retention necessity,singleton laws,20Boolean patterns and countermodel duality;fixed Rust witness sufficiency/source refinement separate."
    elif model == "functional-dependencies":
        proof_name, import_name, namespace = "FunctionalDependencies", "Data/Set/Lattice", "TFQM.FunctionalDependencies."
        declarations = ("extensive", "least", "closure_closed", "monotone", "idempotent", "implication", "replay_extensive", "replay_sound", "accepted_exact", "projected_implication", "nontrivial_projected", "agree_refl", "agree_symm", "agree_trans", "agree_restrict", "join_extensive", "lossless_left", "lossless_right")
        scope = "FD closed-superset least closure, replay exactness, projected implication and sufficient binary lossless row criterion; no SQL/MVD or Rust extraction."
    elif model == "family-registry":
        proof_name, import_name, namespace = "FamilyRegistry", "Data/List/Basic", "TFQM.FamilyRegistry."
        declarations = ("source_rejected", "inactive_rejected", "existing_unchanged", "fresh_appended", "prefix_preserved", "collect_append", "duplicate_unchanged", "inactive_source_empty", "empty_rules", "register_self", "register_other", "register_twice")
        scope = "Raw string membership,stable eligible target accumulation and key-list append/query preservation. No categorical functor,agent reference/execution or provenance certification;Rust parsers/borrowed sets/order and metadata fields refined separately."
    elif model == "finite-path":
        proof_name, import_name, namespace = "FinitePath", "CategoryTheory/PathCategory/Basic", "TFQM.FinitePath."
        declarations = ("identity_comp", "comp_identity", "comp_associative", "length_identity", "length_composition", "edgeWord", "word_identity", "word_composition", "word_length", "rank_length", "rank_bound", "rank_no_cycle", "lift_identity", "lift_edge", "lift_composition", "lift_unique", "bounded_fresh", "bounded_count")
        scope = "Actual Mathlib quiver path category/lift universal property,chronological edge-word concatenation/length,strict-rank acyclicity/finite length and count cap. Rust Kahn rank,complete enumeration/lookup/table and owned category-certificate refinement separate;no new Rust lift API."
    elif model == "partial-structure":
        proof_name, import_name, namespace = "PartialStructure", "Data/List/Basic", "TFQM.PartialStructure."
        declarations = ("factor", "factor_spec", "factor_unique", "exists_descent_iff", "conflict_refuses", "none_reflected", "none_some_conflict", "collapsed_defined", "false_true_conflict", "output_map_composition", "descent_composition", "coordinate_bound", "mixed_digit_bound", "mixed_value_fits", "nullary_product", "prefix_refused", "zero_prefix", "overflow_before_zero")
        scope = "Surjective fiber descent iff constancy/unique factor,Option undefinedness and Boolean reflection,composition,mixed-radix and ordered checked-prefix bounds. Rust many-sorted table/map admission,first conflict order,storage and replay refinement separate."
    elif model == "finite-moore":
        proof_name, import_name, namespace = "FiniteMoore", "Data/List/Basic", "TFQM.FiniteMoore."
        declarations = ("run_append", "future_refl", "future_symm", "future_trans", "future_congruence", "congruence_future", "depth_refines", "depth_readout", "future_in_depth", "fixed_point_exact", "preserving_run", "map_kernel_future", "factor", "factor_spec", "factor_unique", "split_counter_bound")
        scope = "All-word total Moore future equivalence/greatest readout congruence at a stable finite-depth relation,homomorphic kernel and surjective factor uniqueness. Rust canonical IDs/strict finite split progress,chain/storage replay and disjoint-union comparison refined separately."
    elif model == "finite-continuation":
        proof_name, import_name, namespace = "FiniteContinuation", "Data/List/Basic", "TFQM.FiniteContinuation."
        declarations = ("run_empty", "next_unavailable", "run_unavailable", "run_append", "sink_observably_distinct", "future_refl", "future_symm", "future_trans", "closed_pairs_no_distinction", "replay_distinguishes", "replay_saved_answers", "predecessor_length", "charge_success", "charge_refused", "charge_bounded")
        scope = "All-word partial execution/observable absorbing sink,future equivalence,closed pair-search completeness,replay and bounded charge. Rust FIFO shortest/lexicographic order,Moore refinement,constructor/bounds and predecessor storage refined separately."
    elif model == "finite-profunctor-inventory":
        proof_name, import_name, namespace = "FiniteProfunctorInventory", "Data/List/Basic", "TFQM.FiniteProfunctorInventory."
        declarations = ("product_empty_left", "product_empty_right", "product_append", "product_length", "product_member", "middle_empty", "middle_append", "middle_duplicate", "weight_iff", "zero_denominator", "negative_numerator", "zero_weight")
        scope = "Ordered raw finite Cartesian product/duplicate-preserving middle concatenation and defined nonnegative raw-weight predicate. No profunctor action/category laws,general coend or string encoding injectivity;Rust lookup/order/weight comparison/storage/refinement separate."
    elif model == "root-catalog":
        proof_name, import_name, namespace = "RootCatalog", "Data/List/Basic", "TFQM.RootCatalog."
        declarations = ("newWitness", "stored_conversion", "defaultEquality", "forwarded_result", "opaque_true", "opaque_false")
        scope = "Exact post-conversion label storage and opaque equality callback forwarding only. No category/law/typeclass admission,arbitrary callback purity or child-module graph proof;Rust callback counts/provider identities separately tested."
    elif model == "condensation-metadata":
        proof_name, import_name, namespace = "CondensationMetadata", "Data/List/Basic", "TFQM.CondensationMetadata."
        declarations = ("update_success", "update_refused", "boundary_refused", "next_level_bound", "base_ignored", "asserted_ignored", "positive_false", "flags_append", "flags_empty", "duplicate_failure", "all_empty", "all_append", "false_base_can_pass")
        scope = "Checked level update/refusal and ordered caller-flag metadata inventory,including ignored base/true flags and vacuity. No higher-cell/homotopy/infinity-category theorem;Rust names,diagnostic order/storage/refinement separate."
    elif model == "tagged-coend":
        proof_name, import_name, namespace = "TaggedCoend", "Logic/Relation", "TFQM.TaggedCoend."
        declarations = ("connected_refl", "connected_symm", "connected_trans", "supplied_pair", "project", "projection_exact", "respects_closure", "factor", "factor_projection", "factor_unique", "closed_contains_component", "frontier_fresh_sound", "frontier_reverse_sound", "labels_exact", "dense_nonempty", "range_after_increment", "new_root_fits", "component_increment_fits", "local_equal_no_range")
        scope = "Actual equivalence closure/quotient of supplied tagged relation,factorization/uniqueness,worklist soundness/closure and dense-label range/counter obligations. No category/bifunctor or general coend theorem;Rust traversal/storage/order refinement separate."
    elif model == "cauchy-inventory":
        proof_name, import_name, namespace = "CauchyInventory", "Data/List/Basic", "TFQM.CauchyInventory."
        declarations = ("equal_defined", "missing_left", "missing_right", "pair_checks", "first_empty", "first_head", "first_skip", "first_sound", "first_exists", "first_append", "inventory_member", "inventory_append", "inventory_duplicates", "three_checks", "admit_preserves_raw", "admit_success_flags", "failed_flag")
        scope = "Raw defined-only named equality,ordered first matching pair and duplicate-preserving inventory,three observed checks and historical raw-value admission. No category typing/completeness or Karoubi theorem."
    elif model == "finite-groupoid":
        proof_name, import_name, namespace = "FiniteGroupoid", "CategoryTheory/Groupoid", "TFQM.FiniteGroupoid."
        declarations = ("checks_true_iff", "admit_preserves_data", "admit_success_laws", "failed_guard", "groupoidOfLaws", "groupoid_inverse", "groupoidOfAdmitted", "related_refl", "related_symm", "related_trans", "reconstruct_coordinate", "coordinate_reconstruct", "coordinateEquiv", "coordinate_identity", "coordinate_composition", "thin_from_root", "removal_progress", "empty_not_connected_thin")
        scope = "Complete inverse laws realize actual Mathlib Groupoid; connected-arrow relation,chosen-connector isotropy equivalence/composition and thinness,finite removal progress. Rust deterministic selection/full partition/storage/budgets and any complex algebra interpretation remain separate."
    elif model == "finite-dagger":
        proof_name, import_name, namespace = "FiniteDagger", "CategoryTheory/Functor/Basic", "TFQM.FiniteDagger."
        declarations = ("checks_true_iff", "admit_preserves_data", "admit_success_laws", "failed_guard", "certifiedOfAdmitted", "certified_arrow", "dagger_involutive", "dagger_injective", "dagger_surjective", "dagger_identity", "dagger_composition", "unitary_identity", "unitary_dagger", "unitary_composite", "unitary_check_iff")
        scope = "Total reversed typed arrows over actual Mathlib Category carry admitted involution/identity/composition laws; unitary requires both inverse equations and is closed under dagger/composition. Rust finite domain/boundary/enumeration/storage/budget refinement remains separate."
    elif model == "finite-trace":
        proof_name, import_name, namespace = "FiniteTrace", "Data/List/Basic", "TFQM.FiniteTrace."
        declarations = ("initial_sound", "fresh_sound", "insert_sound", "closed_contains_reachable", "empty_frontier_closed", "complete_component", "existing_self_edge", "adjacent_length", "adjacent_inventory", "charge_success", "charge_refusal", "charge_bounded", "charge_strict", "machine_increment_fits", "replay_complete", "replay_refuses_missing")
        scope = "Worklist soundness/empty-frontier complete graph component, adjacent word length/inventory, bounded strict checks and full replay. Concrete certified state-relative edges, BFS order and Rust scratch/Rc/storage refinement remain separate."
    elif model == "finite-independence":
        proof_name, import_name, namespace = "FiniteIndependence", "Data/List/Basic", "TFQM.FiniteIndependence."
        declarations = ("future_refl", "future_symm", "future_trans", "witness_refuses_future", "unequal_can_share_futures", "defined_order_has_first_step", "final_orders_enable_singles", "unavailable_never_enabled", "witness_sound", "witness_uses_saved_answers", "endpoint_replay", "endpoint_mismatch", "unavailable_ignores_search", "equivalent_ignores_search", "distinction_requires_success", "resource_refusal_preserved")
        scope = "All-word future equivalence, two enabled orders, explicit witness soundness and endpoint binding, with no unavailable/resource refusal interpreted as independence. Finite quotient/search/storage and test-only alpha renaming are separate."
    elif model == "finite-simulation":
        proof_name, import_name, namespace = "FiniteSimulation", "Data/List/Basic", "TFQM.FiniteSimulation."
        declarations = ("run_empty", "run_unavailable", "run_append", "exact_macro_words", "exact_iff", "extension_preserves_defined", "extension_absent", "extension_does_not_drop", "extension_does_not_change", "added_is_allowed", "added_changes_availability", "map_first", "encoding_second", "budget_third", "admission_success", "replay_success")
        scope = "Exact partial-step simulation lifts to every flattened encoded word; extension preserves defined targets and lists added availability, with ordered admission/refusal and decision replay. Carrier/macro typing, readout dictionary and checked Rust costs remain separate."
    elif model == "joint-carrier":
        proof_name, import_name, namespace = "JointCarrier", "Data/List/Basic", "TFQM.JointCarrier."
        declarations = ("profile_equal", "profile_retains_left", "profile_retains_right", "profile_retains_answer", "coarsest_refinement", "fiber_member", "fiber_disjoint", "fiber_cover", "fiber_answer", "empty_fiber_answers", "decoder_unique_on_image", "collision_refuses_decoder", "replay_success", "replay_refuses", "budget_boundary")
        scope = "Exact relation-indexed profile kernel/coarsest refinement, complete fiber/answer semantics, decoder uniqueness on realized image, collision refusal and replay equality; local quotient construction and Rust representation remain separate."
    elif model == "natural-composition":
        proof_name, import_name, namespace = "NaturalComposition", "CategoryTheory/NatTrans", "TFQM.NaturalComposition."
        declarations = ("identity_component", "vertical_component", "vertical_left_identity", "vertical_right_identity", "vertical_associative", "left_component", "right_component", "left_preserves_vertical", "right_preserves_vertical", "horizontal_component", "horizontal_paths", "horizontal_other_path", "horizontal_naturality", "horizontal_identity", "interchange")
        scope = "Actual Mathlib natural-transformation identity/vertical composition, constructed whiskering, horizontal naturality/path equality and interchange; raw partial diagram failures and Rust storage/context refinement remain separate."
    elif model == "finite-naturality":
        proof_name, import_name, namespace = "FiniteNaturality", "CategoryTheory/NatTrans", "TFQM.FiniteNaturality."
        declarations = ("checks_true_iff", "admit_preserves_data", "admit_success", "failed_guard", "natTrans_app", "natTrans_naturality", "natTransOfAdmitted", "admitted_component")
        scope = "Admitted endpoint categories/functors and typed total components with exact naturality admission realize actual Mathlib NatTrans; Rust finite storage/enumeration/boundary normalization remains separate."
    elif model == "functor-operations":
        proof_name, import_name, namespace = "FunctorOperations", "CategoryTheory/Functor/Basic", "TFQM.FunctorOperations."
        declarations = ("identity_object", "identity_arrow", "composite_object", "composite_arrow", "identity_then", "then_identity", "compose_associative", "first_missing", "second_missing", "partial_success", "partial_associative", "equal_middle", "unequal_middle", "names_insufficient", "reverse_entry", "reverse_twice", "guarded_insert_eq", "registration_eq", "registered_member")
        scope = "Actual Mathlib identity/composition, pure partial-map composition, exact endpoint-data guard and raw table reversal; no automatic opposite/inclusion admission or Rust extraction."
    elif model == "finite-functor":
        proof_name, import_name, namespace = "FiniteFunctor", "CategoryTheory/Functor/Basic", "TFQM.FiniteFunctor."
        declarations = ("checks_true_iff", "admit_preserves_data", "admit_success_laws", "failed_guard", "functor_object", "functor_arrow", "functor_identity", "functor_composition", "functorOfAdmitted", "admitted_object")
        scope = "Law admission of typed total maps between admitted endpoint categories yields an actual Mathlib Functor; Rust finite domain/image/boundary refinement and legacy diagnostics remain separate."
    elif model == "higher-functor-inventory":
        proof_name, import_name, namespace = "HigherFunctorInventory", "Data/List/Basic", "TFQM.HigherFunctorInventory."
        declarations = ("image_missing", "source_missing", "target_missing", "actual_missing", "both_boundaries_wrong", "source_wrong", "target_wrong", "correct_boundaries", "boundary_passes_iff", "pair_absent", "forward_missing", "inverse_missing", "names_present", "pair_passes_iff", "empty_inventory", "inventory_append")
        scope = "Literal raw boundary-presence precedence, independent endpoint failures and forward/inverse name membership inventory; no 2-functor, invertibility or coherence theorem."
    elif model == "lawvere-inventory":
        proof_name, import_name, namespace = "LawvereInventory", "Data/List/Basic", "TFQM.LawvereInventory."
        declarations = ("slot_fits", "slot_refused", "slot_exact", "slot_max_zero", "slot_max_positive", "equal_defined", "absent_left", "absent_right", "pair_iff", "unsplit_member", "unsplit_empty", "unsplit_append", "unsplit_duplicate", "split_excluded")
        scope = "Exact bounded slot admission and pure raw declared-name pair/unsplit inventory, with defined-only equality, ordered duplicates and empty scope; no typed Lawvere or Cauchy category theorem."
    elif model == "em-samples":
        proof_name, import_name, namespace = "EMSamples", "Data/List/Basic", "TFQM.EMSamples."
        declarations = ("bind_left", "bind_right", "bind_associative", "map_identity", "map_composition", "join_spec", "free_unit", "free_associativity", "clone_first", "law_after_clone", "step_pass", "scan_empty", "scan_ok_iff", "algebra_empty", "unit_before_associativity", "observed_counts")
        scope = "Concrete Maybe value equations and finite observed clone/law flags with typed first refusal/counts; no generic Monad or callback certification and no exhaustive-domain claim."
    elif model == "finite-builder":
        proof_name, import_name, namespace = "FiniteBuilder", "Data/List/Basic", "TFQM.FiniteBuilder."
        declarations = ("update_self", "update_other", "update_shadow", "checked_missing", "checked_existing_iff", "no_identities", "source_only", "target_only", "both_identities", "complete_empty", "complete_append")
        scope = "Raw table overwrite, optional loop-boundary guard and ordered source/target identity completion; no fresh-name/free-category or Rust allocation theorem."
    elif model == "validation-inventory":
        proof_name, import_name, namespace = "ValidationInventory", "Data/List/Basic", "TFQM.ValidationInventory."
        declarations = ("empty_passes", "empty_name", "allPassed_iff", "add_preserves", "add_pass_count", "add_fail_count", "violation_projection", "violation_fails", "empty_batch", "nonempty_batch", "nonempty_batch_fails", "violation_count_append", "failure_count_bound")
        scope = "Literal caller-supplied report flags and typed diagnostics, append/projection/count behavior; no validation-unit checker or authenticated certificate."
    elif model == "arrow-effects":
        proof_name, import_name, namespace = "ArrowEffects", "Data/List/Basic", "TFQM.ArrowEffects."
        declarations = ("lift_value", "tell_value", "compose_first_error", "compose_second_error", "compose_success", "compose_associative", "fanout_success", "fanout_first_error", "split_success", "split_first_error", "choice_left", "choice_right")
        scope = "Reader/state/ordered writer/explicit error value semantics for total callbacks with arbitrary Clone function; no Rust callback purity/termination, external-effect rollback or MIR theorem."
    elif model == "graph-incidence":
        proof_name, import_name, namespace = "GraphIncidence", "Data/Matrix/Mul", "TFQM.GraphIncidence."
        declarations = ("incidence_loop_zero", "incidence_reverse", "triangle_cancellation", "distinct_edge_pairs",
                        "triangle_at_ab", "triangle_at_bc", "triangle_at_ac", "row_action", "row_product_zero")
        scope = "Finite directed incidence and signed triangle-row product cancellation; separate Rust index-map, admission, rank and storage correspondence."
    elif model == "vector-maps":
        proof_name, import_name, namespace = "VectorMaps", "Data/Matrix/Mul", "TFQM.VectorMaps."
        declarations = ("compatible_iff", "degree_first", "basis_after_degree", "length_after_context",
                        "zero_entry", "add_entry", "sub_entry", "scalar_entry", "subtract_then_add", "scaled_sum",
                        "dot_prefix_spec", "matrix_entry", "matrix_zero", "matrix_add", "matrix_scale")
        scope = "Ordered graded-coordinate compatibility, exact pointwise operations and finite matrix-vector dot sums/linearity; separate canonical-pair, degree, Rust storage and backend review."
    elif model == "carrier-dimensions":
        proof_name, import_name, namespace = "CarrierDimensions", "LinearAlgebra/Dimension/DivisionRing", "TFQM.CarrierDimensions."
        declarations = ("quotient_dimension", "admitted_subtraction_bounds")
        scope = "Rational image-quotient dimension and subtraction bounds under the admitted rank/inclusion predicates; separate matrix/certificate and Rust representation review."
    elif model == "scalar-admission":
        proof_name, import_name, namespace = "ScalarAdmission", "Data/Int/GCD", "TFQM.ScalarAdmission."
        declarations = ("reify_fields", "canonical_roundtrip", "zero_has_unit_denominator", "zero_denominator_refused",
                        "negative_denominator_refused", "scan_success_iff", "scan_failed_head", "first_invalid", "store_preserves")
        scope = "Canonical integer-pair/Rat representation, exact first-invalid index, domain refusal and literal metadata preservation; separate BigInt/Rust storage and matrix/caller review."
    elif model == "simplicial-homology":
        proof_name, import_name, namespace = "SimplicialHomology", "LinearAlgebra/Dimension/DivisionRing", "TFQM.SimplicialHomology."
        declarations = ("range_in_cycles", "rank_sum_bound", "betti_dimension")
        scope = "Rational homology as cycles modulo boundaries, nonnegative rank sum and exact Betti dimension formula; concrete basis, zero-composition and certified rank correspondence are separate obligations."
    elif model == "simplicial-boundary":
        proof_name, import_name, namespace = "SimplicialBoundary", "Data/Matrix/Mul", "TFQM.SimplicialBoundary."
        declarations = ("paired_term", "pair_cancellation", "signed_faces_cancel", "mapMatrix_comp", "mapMatrix_identity")
        scope = "Alternating two-face cancellation and exact indicator-matrix composition; concrete list/basis and Rust representation correspondence requires separate review."
    elif model == "simplicial-closure":
        proof_name, import_name, namespace = "SimplicialClosure", "Data/Finset/Card", "TFQM.SimplicialClosure."
        declarations = ("initial_cover", "initial_frontier", "duplicate_cover", "fresh_cover", "duplicate_frontier",
                        "fresh_frontier", "fresh_sound", "finish_contains", "finish_closed", "fresh_card_bound",
                        "duplicate_potential", "fresh_potential", "erase_commute", "erase_preserves_distinct", "erase_preserves_order")
        scope = "Worklist coverage/soundness/closure, cardinality and decreasing work potential, and ordered/distinct face erasure; separate Rust representation review."
    elif model == "two-step-complex":
        proof_name, import_name, namespace = "TwoStepComplex", "Data/Matrix/Mul", "TFQM.TwoStepComplex."
        declarations = ("admission_success_iff", "admission_failure", "admission_preserves", "input_zero_product",
                        "differential_square_zero", "image_is_cycle", "failed_gate", "passed_gate")
        scope = "Two-step exact Q matrix admission, owned data preservation, differential square zero, image-as-cycles and typed guard propagation."
    elif model == "degree-repair":
        proof_name, import_name, namespace = "DegreeRepair", "Data/Int/Basic", "TFQM.DegreeRepair."
        declarations = ("payload_exact", "signed_index", "large_index", "dimension_zero", "dimension_one",
                        "dimension_two", "outside_support", "outside_payload", "scan_append", "scan_parity",
                        "parity_count", "scan_count", "orientation_sign")
        scope = "Exact full-index refusal and finite-support dimension payloads, with Boolean inversion parity and sign; no simplicial homology or rank theorem."
    elif model == "homology-protocols":
        proof_name, import_name, namespace = "HomologyProtocols", "Data/Int/Basic", "TFQM.HomologyProtocols."
        declarations = ("numeric_zero", "numeric_success_iff", "numeric_preserves_payload", "predecessor_success_iff",
                        "successor_success_iff", "predecessor_refusal_iff", "successor_refusal_iff", "degree_drop_inverts")
        scope = "Nonzero numeric identifier payload preservation and exact bounded i32 predecessor/successor refusal and inverse law."
    elif model == "root-records":
        proof_name, import_name, namespace = "RootRecords", "Data/Int/Basic", "TFQM.RootRecords."
        declarations = ("joinable_iff", "foreign_category_refused", "report_empty", "report_valid_head",
                        "report_failed_head", "threshold_iff", "mass_success_iff", "mass_label_first")
        scope = "Literal arrow/category guard, ordered missing-label diagnostics, inventory threshold and nonnegative defined mass; no categorical or model certification."
    elif model == "shape-inventory":
        proof_name, import_name, namespace = "ShapeInventory", "Data/Nat/Basic", "TFQM.ShapeInventory."
        declarations = ("context_shape", "context_law", "context_precondition", "contextual_failure",
                        "context_success_iff", "endomorphism_success_iff", "alignment_success_iff",
                        "members_success_iff", "label_binding_success_iff")
        scope = "Literal endomorphism boundary, optional inventory alignment, conditional label binding and exact typed-error context preservation."
    elif model == "literal-reversal":
        proof_name, import_name, namespace = "LiteralReversal", "Data/List/Basic", "TFQM.LiteralReversal."
        declarations = ("reverse_involution", "list_involution", "length_preserved", "names_and_order_preserved")
        scope = "Literal boundary-triple reversal involution, length, names and list-order preservation; no category-law claim."
    elif model == "finite-set":
        proof_name, import_name, namespace = "FiniteLiteralSet", "Data/Finset/Basic", "TFQM.FiniteLiteralSet."
        declarations = ("scan_success_iff", "first_empty", "first_duplicate", "cardinality_success_iff",
                        "bind_unit_success", "checks_success_iff", "admit_preserves_raw", "admit_invariants")
        scope = "Finite literal-string-set admission, first entry failures, optional cardinality, raw-data preservation and admitted invariants."
    elif model == "parameters":
        proof_name, import_name, namespace = "ParameterMetadata", "Data/Int/Basic", "TFQM.ParameterMetadata."
        declarations = ("signed_success_iff", "optional_level_success_iff", "positive_bound_success_iff",
                        "arity_success_iff", "variance_success_iff", "first_error", "accepted_prefix")
        scope = "Literal metadata threshold/tag admission and ordered typed refusal; no underlying mathematical law claim."
    else:
        proof_name, import_name, namespace = "BoundedCounter", "Data/Nat/Basic", "TFQM.BoundedCounter."
        declarations = ("clip_bound", "guard_exact", "increment_step", "decrement_step",
                        "increment_branch_bound", "separator_bound", "decrement_separator", "short_words_legal")
        scope = "Finite-depth clipping quotient, native guard correspondence, exact event steps and minimal decrement separators."
    project = ROOT/"lean4"
    proof = Path(__file__).resolve().parent/"proofs"/(proof_name+".lean")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-"+model+"-proof"
    output = ROOT/"evidence/quality/category_homology"/stamp
    output.mkdir(parents=True)
    shutil.copyfile(proof,output/proof.name)
    runtime = {}
    for source in (Path(__file__),Path(__file__).parent/"run_audit.py"):
        shutil.copyfile(source,output/source.name)
        runtime[source.name] = digest(output/source.name)
    inputs = {str(proof):digest(proof)}
    mathlib = project/".lake/packages/mathlib"
    imported = mathlib/"Mathlib"/(import_name+".lean")
    inputs[str(imported)] = digest(imported)
    write_json(output/"source_manifest.json",inputs)
    tool = subprocess.run(["elan","which","lean"],cwd=project,text=True,capture_output=True)
    if tool.returncode != 0: raise RuntimeError("Cannot resolve the prepared Lean compiler")
    binary = Path(tool.stdout.strip())
    bootstrap = json.loads(subprocess.check_output(["lake","env",sys.executable,"-c",
        "import json,os; print(json.dumps({key:os.environ.get(key,'') for key in ('LEAN_PATH','LEAN_SRC_PATH')}))"],cwd=project,text=True))
    # Exclude mutable output modules of the user's main theory project. The
    # standalone model uses only the prepared third-party dependency libraries.
    package_dir = (project/".lake/packages").resolve()
    environment = {}
    for key,search_path in bootstrap.items():
        libraries = dict.fromkeys(Path(entry).resolve() for entry in search_path.split(";")
            if entry and Path(entry).resolve().is_relative_to(package_dir))
        if not libraries: raise RuntimeError("No prepared proof dependency path: "+key)
        environment[key] = ";".join(str(path) for path in libraries)
    write_json(output/"environment.json",{"lean_binary":str(binary),"environment":environment,"excluded_main_project_outputs":True})
    common = [str(binary),"--memory="+str(args.memory_mb),"--threads=2","--root="+str(proof.parent)]
    dependencies = execute([*common,"--deps",str(proof)],proof.parent,output/"dependencies.log",timeout=60,environment_overlay=environment)
    sources = execute([*common,"--src-deps",str(proof)],proof.parent,output/"dependency-sources.log",timeout=60,environment_overlay=environment)
    paths = set()
    for log in ("dependencies.log","dependency-sources.log"):
        for line in (output/log).read_text(encoding="utf-8").splitlines():
            candidate = Path(line.strip())
            if not candidate.is_absolute(): candidate = project/candidate
            if candidate.is_file():
                paths.add(candidate.resolve())
                # Lean 4 stores auxiliary private/server data next to OLean.
                for suffix in (".private",".server"):
                    if Path(str(candidate)+suffix).is_file(): paths.add(Path(str(candidate)+suffix))
    dependency_inputs = {str(path):digest(path) for path in sorted(paths)}
    write_json(output/"dependency_manifest.json",dependency_inputs)
    head_before = subprocess.check_output(["git","-C",str(mathlib),"rev-parse","HEAD"],text=True).strip()
    status_before = subprocess.check_output(["git","-C",str(mathlib),"status","--porcelain","--untracked-files=no"],text=True).strip()
    checked = execute([*common,str(proof)],proof.parent,output/"check.log",timeout=300,environment_overlay=environment)
    text = (output/"check.log").read_text(encoding="utf-8")
    warnings = "warning:" in text
    reports = {name:[item.strip() for item in axioms.split(",") if item.strip()]
               for name,axioms in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",text)}
    reports.update({name:[] for name in re.findall(r"'([^']+)' does not depend on any axioms",text)})
    expected = {namespace+name for name in declarations}
    unexpected = sorted({axiom for axioms in reports.values() for axiom in axioms} - {"propext","Classical.choice","Quot.sound"})
    head_after = subprocess.check_output(["git","-C",str(mathlib),"rev-parse","HEAD"],text=True).strip()
    status_after = subprocess.check_output(["git","-C",str(mathlib),"status","--porcelain","--untracked-files=no"],text=True).strip()
    receipt = {
        "AuthorityEffect":"None", "proof_sha256":digest(proof),
        "lean_memory_limit_mb":args.memory_mb,
        "source_manifest_sha256":digest(output/"source_manifest.json"),
        "dependency_manifest_sha256":digest(output/"dependency_manifest.json"),
        "sources_unchanged":all(Path(path).is_file() and digest(Path(path)) == value for path,value in inputs.items()),
        "direct_dependencies_unchanged":all(Path(path).is_file() and digest(Path(path)) == value for path,value in dependency_inputs.items()),
        "dependency_scope":"Direct import source/OLean roots and Lean 4 private/server data. Transitive sources use the clean pinned Mathlib revision and retained targeted build; not a complete compiler file-read trace.",
        "lean_version":subprocess.check_output([str(binary),"--version"],cwd=proof.parent,text=True).strip(),
        "lean_binary":None if binary is None else {"path":str(binary),"sha256":digest(binary)},
        "mathlib_head":head_after,"mathlib_revision_stable":head_before == head_after,
        "mathlib_tracked_source_clean":not status_before and not status_after,
        "environment_sha256":digest(output/"environment.json"),
        "runner_sha256":runtime[Path(__file__).name],
        "runner_source_unchanged":digest(Path(__file__))==runtime[Path(__file__).name],
        "runtime_snapshots":runtime,
        "runs":[checked,dependencies,sources],
        "check_ok":checked["exit_code"] == 0 and dependencies["exit_code"] == 0 and sources["exit_code"] == 0 and expected == set(reports) and not unexpected and not warnings,
        "diagnostic_warnings_detected":warnings,
        "axiom_reports":reports,"unexpected_axioms":unexpected,
        "unfinished_axiom_detected":"sorryAx" in text,
        "scope":scope+" Rust construction/representation refinement, MIR, allocator totality and crash freedom require separate evidence.",
    }
    write_json(output/"receipt.json",receipt)
    print(json.dumps({"check_ok":receipt["check_ok"],"sources_unchanged":receipt["sources_unchanged"],"unfinished_axiom_detected":receipt["unfinished_axiom_detected"]}))
    print("Receipt:",output)
    return 0 if receipt["check_ok"] and receipt["sources_unchanged"] and receipt["direct_dependencies_unchanged"] and receipt["mathlib_revision_stable"] and receipt["mathlib_tracked_source_clean"] and not receipt["unfinished_axiom_detected"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
