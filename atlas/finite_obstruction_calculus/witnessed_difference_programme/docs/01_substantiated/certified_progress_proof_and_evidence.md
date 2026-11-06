# Certified progress: proof and evidence supplement

Appendix S is the authoritative written theorem statement. This supplement
connects its proofs to concrete files without promoting one evidence type into
another. Its revised finite model excludes the seven supplied review failures.
The reviewed submission remains a historical source, not a second current proof.
Its [source manifest](source_archive/appendix_s_review/source_manifest.json)
binds the original submission and review bytes; the standalone appendix has
been removed after exact integration into the canonical manuscript.

## 1. Certificate soundness and existence

Let B be the input-derived reachable beliefs, T the supplied stopping targets,
and Succ(b,a) the nonempty successors of each universally enabled action.
The attractor construction is increasing and must stabilize because each strict
round adds a belief. Assign first-entry layers to its chosen actions. The
complement L includes dead ends and has an actual L-successor for every enabled
action. This gives the exhaustive win/loss characterization of S.3.

The checker does not reproduce this search. It verifies the submitted rank and
closure witnesses. A natural rank gives termination by induction. A
target-disjoint closure prevents success by induction along adversarial choices.
Full W/L coverage for a win certificate then characterizes the entire reachable
arena, independently of whether the producer was correct.

For optimality, the submitted selected action gives an upper bound under rank
induction. Every competing enabled action supplies a lower-bound successor,
either in the already checked trap or with V(b)≤c(b,a)+V(y). Induct on an
arbitrary successful finite contingent plan. A trap successor cannot occur in
a guaranteed success; a winning successor requires the lower subtree budget.
Thus every successful budget is at least V(b). Terminal value zero anchors the
bound. The original shifted-terminal example shows why it cannot be omitted.

Finite positive costs give certificate existence: an attractor plan bounds cost
by M=c_max R, and every strategy with cost at most M has depth at most
floor(M/epsilon). Exact finite-horizon minimax attains the optimum; selected
minimizers strictly decrease value and receive their own acyclic strategy rank.
This construction is proved in writing. It is not yet a Lean theorem about the
actual producer algorithm.

## 2. Quotient and refinement proof boundaries

The quotient acts on beliefs. At a block it must preserve target truth,
enabled actions, costs, and successor-block sets. These laws supply a forward
map on successors and an actual fine predecessor for every coarse successor.
Induction on horizon transports both reachability and all remaining-budget
inequalities. Hence attainable-budget sets, winning status, and optimal values
agree. Arbitrary fine strategies need not descend; class-constant strategies do.

The Python procedure splits an existing block by those four signatures.
Each strict round adds a block, proving the bound |B|−|Pi_0|. Any stable finer
partition survives every split: equality of its successor blocks implies
equality after mapping them to the current coarser blocks. This establishes
coarseness of the stable result, not just eventual stability.

The Lean module also constructs a finite relation refinement. Starting from
the listed seed pairs, filter by target/action/price agreement and two-sided
successor matching through the current relation. A strict filter loses at
least one list entry. Iterating with fuel equal to the seed-list length therefore
reaches a fixed point. Every stable relation beneath the seed is retained at
each filter step by monotonicity. The result is the greatest stable subrelation.
If the seed relation is an equivalence, the result is also an equivalence:
the identity, converse, and relational composite are stable refinements,
so maximality gives reflexivity, symmetry, and transitivity.

For an equivalence relation, two-sided successor matching is exactly equality
of successor equivalence-class sets. Thus the relation proof and signature
partition proof describe the same stable congruence. The Lean termination
bound is the listed-pair count; the sharper block-round bound is proved in
writing and checked by Python. No native physical observer is extracted.

## 3. Formal versus executable bindings

| Written obligation | Lean declarations | Python owner |
|---|---|---|
| Finite reachability and trap completeness | `winning_fixed_point`, `least_closed_region`, `loss_iff_trap_at_initial` | `producer.py`; independently `checker.py` |
| Rank/trap partition soundness | `rank_certificate_sound`, `checked_partition_characterizes_winning` | Rank and closure replay |
| Target cannot be stalled loss | `successful_terminal_cannot_be_stalled_loss` | Model-derived target and stall checks |
| Exact lower/upper budgets | `optimal_upper_budget`, `optimal_lower_budget`, `certificate_exact_optimality` | All-action lower and selected-action upper checks |
| Price descent along selected steps | `positive_upper_step_decreases_value` | Selected strategy rank construction |
| Two-sided quotient | `reach_transport`, `budget_transport`, `achievable_budgets_equal` | `observation.py` signatures and quotient tables |
| Constructive greatest refinement | `stabilization_is_fixed`, `coarsest_stable_relation`, `stable_seed_equivalence` | Signature splits and fixed-point replay |
| Optional-action monotonicity | `optional_actions_preserve_budget` | Added-action and restrictive-guard examples |

All formal modules use the core-only Lean 4.33.1 harness. The selected axiom
receipts bind source SHA-256 and printed declarations, and permit only
`propext`, `Classical.choice`, and `Quot.sound`. No `sorry` or new custom axiom
is allowed. The historical Mathlib audit remains separate.

The Python checker accepts strict original-model/certificate objects and exact
rational strings. It validates every supplied witness before attributing
success. The offline replay package retains each actual submitted witness,
its independent receipt, and source hashes; resynthesizing a solution is not
replay of a failed proposal.

The scoped tests include the seven reviewed failures, all previous valid
regressions, independent all-policy comparison on 4,096 small games, and
observer/guard/budget controls. Passing these tests is concrete finite evidence,
not universal source verification. A complete game win still needs sound
target interpretation; a source-negative conclusion additionally needs
constructive original-solution coverage. CODA evaluation supplies neither
authorization nor the missing interpretation maps.

## 4. Claim changes required by the review

- P08 changes the false necessity/sufficiency claim into congruence sufficiency.
- P14 restricts literal strategy descent to class-constant strategies.
- D02 retains only the immediate-emission upper bound unless the example
  excludes cheaper routes.
- P05/P19 distinguish an unsound restrictive transfer from an actual
  initial-containing losing trap.
- P01's action domain is nonterminal winners; successful targets stop before
  dead-end reporting.
- A2 explicitly lists a finite resolution vocabulary. Checker completeness
  on that vocabulary does not provide original-solution strategy coverage.
- L includes dead ends. Reporting precedence never changes trap closure.
- Invalid certificate refusal is distinct from a controller's refusal action.

These repairs close the declared finite reachability and certificate questions.
They leave parity objectives, original-world checker fidelity, native Rust
binding, physical observation realization, and general guarded-history
coherence open.
