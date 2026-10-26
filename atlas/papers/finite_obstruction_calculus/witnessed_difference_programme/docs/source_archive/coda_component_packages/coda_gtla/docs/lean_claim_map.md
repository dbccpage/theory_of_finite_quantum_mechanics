# Statement-level Lean map — CODA-GTLA 3.2.1

The local `CodaGtla` declarations concern records and a finite evaluator.
Lean `Presentation` has a carrier type and decidable equality; it has no
finiteness field. The Python implementation restricts carriers to finite
sets and adds symmetry and inhabitedness checks. The identities below do
not require the omitted finiteness hypothesis.

The reported axiom lists are per declaration. Rebuilding the current source
and comparing `#print axioms` output is a release gate; a table is not a build log.

| Paper claim | Exact declaration(s), namespace CodaGtla | Module | Actual conclusion | Reported dependencies |
|---|---|---|---|---|
| GTLA-T1 | `diagSpan_cost_zero` | `T01SpanPullback.lean` | Diagonal cost is zero | none |
| GTLA-T2 | `compSpan_cost_subadditive` | `T01SpanPullback.lean` | Defined composite cost is at most the sum (in fact equal) | none |
| GTLA-T3 | `idTrace_work_zero` | `T01SpanPullback.lean` | Identity trace work is zero | none |
| GTLA-T4 | `eraseTrace_id` | `T01SpanPullback.lean` | Erasure preserves the defined identity | none |
| GTLA-T5 | `eraseTrace_comp` | `T01SpanPullback.lean` | Erasure preserves the defined composition | none |
| GTLA-T6 | `pipeline_empty_sieve_refused` | `T02MasterNormalForm.lean` | A false sieve flag routes to refusal | propext |
| GTLA-T7 | `pipeline_closed_residual_anomalon` | `T02MasterNormalForm.lean` | Successful earlier flags and positive Phi/zero Gamma route to residual | propext |
| GTLA-T8 | `auth_disjoint_anomalon; auth_disjoint_refused; anomalon_disjoint_refused` | `T03AuthorityFirewall.lean` | The three local constructors are pairwise disjoint | propext |
| GTLA-T9 | `non_promotion_firewall` | `T03AuthorityFirewall.lean` | An explicit zero-distance/unlicensed record refuses | propext |
| GTLA-T10 | `observation_collision_distinct_authority` | `T03AuthorityFirewall.lean` | Two records share distances but differ in declared licence and output | propext |

The additional `pipeline_licensed_exact_authorized` theorem states that an
exact record with the declared licence flag takes the local authorized
constructor. It does not authenticate an external grant.

## Vendored residual algebra

`lean4/A.lean` is included and imported by
`Algebra.lean`. Its custom `LinearMap` is an additive map between
its declared additive groups; it is not a mathlib vector-space structure.
The wrapper prints dependencies for `Coda.A.residual_zero_iff`,
`residual_in_kernel`, `residual_idempotent`, `residual_transport`,
`range_fixed_iff`, `quotient_residual_iff`, `quotient_universal`, and
`quotient_section`. The quotient statements retain their explicit
submodule/annihilation and projection hypotheses.

The 2026-09-27 local census reports `propext` for `residual_zero_iff`,
no axioms for the next five identities, and `Quot.sound` for
`quotient_universal` and `quotient_section`. The main GTLA wrapper reports
no axioms for T1–T5 and `propext` for T6–T10 and the licensed-exact clause.
Reproduce with `lake build`, `lake env lean Core.lean`, and
`lake env lean Algebra.lean`.

There is no Lean theorem here for the Python regular groupoid action,
monodromy certificates, LP duality, bicategorical coherence, or the bounded
E2 cycle quotient. These have separately scoped computational examples.
