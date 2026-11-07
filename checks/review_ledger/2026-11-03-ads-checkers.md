# AdS checker implementation review — 2026-11-03

AuthorityEffect: None.

This pass reads the four AdS independent checkers and their finite formal
counterparts, repairs their implementations, and verifies their actual public
boundaries. The accompanying source-bound records assess the four applications
and two verification applications at L4B. The retention label is 5 for each
retained source and its validated companion. Label 5 is a retention decision,
not a claim of perfection. This is one completed part of the continuing
`checks`-then-`code` review.

## Errors and corrections

1. `cayley_menger_triangle_area_sq(1, 1, 2)` returned a binary float. Its three
   parameters also admitted floats and booleans. Normalize each parameter using
   exact rational admission before computing the polynomial. Integer inputs now
   produce `Fraction(1, 4)`. The formal definition is a polynomial on Q, so signed
   and nongeometric coefficients remain admitted; this is not a triangle
   realizability certificate.
2. `uniform_defect_regge_action` multiplied unvalidated inputs, admitting floats
   and booleans. Both factors now use exact rational admission. Signed factors
   match the formal polynomial; no unproved sign restriction was introduced.
3. Subdivision admitted arbitrarily large integer counts without a stated bit
   budget. Counts now have the same 4096-bit resource bound as rational
   components. Computation stays closed-form, with no loop proportional to the
   value of the count. Negative areas, nonpositive counts, bools and noninteger
   counts are refused before arithmetic.
4. Manual counter updates did not consistently count executed validations.
   In particular, RT pasting and spectral normalization each performed two
   validations while increasing a shared count once; subdivision performed
   three validations per reported case. Each invocation now owns `Cases`
   aggregates and counts each actual `require` call. A conjunction is one
   validation call. Current totals are 829 (CFT), 499 (HaPPY), 553 (Regge), and
   528 (RT). Old receipts retain their historical case-count meaning.
5. RT and Regge returned positional counter tuples, and HaPPY duplicated bucket
   classification and failure counters. Compose those responsibilities into the
   existing aggregate. The checkers stop on a failed obligation and the CLI
   returns a typed nonzero failure. They print a success report only after all
   obligations pass. No run state persists across invocations.
6. The regression loader assumed a non-null import specification and did not
   register a module during execution. This breaks ordinary dataclass/module
   inspection expectations. Restrict it to the reviewed source population,
   validate the loader, register for execution, and restore the previous module
   on success, error, or cancellation. Capture preserves return values and
   propagates unexpected errors. Strict typing now checks both suites.
7. The original lineon oracle exceeded the nesting ceiling. Extract its
   independent simultaneous-hop calculation within the same test module;
   retain the 8,200-case comparison and one class per file.
8. Two mutation survivors identified missing challenges: an unadmitted object
   could execute multiplication in the mutated implementation before an inner validator rejected it, and the
   refusal helper was not challenged with inconsistent success/error fields.
   Add a no-arithmetic-before-admission probe and an inconsistent result
   challenge. Keep the original 66/68 run and both focused reruns in separate
   receipts; no candidate is silently removed.

## Evidence and limits

- `2026-11-03-ads-requirements.json` maps every source symbol to a requirement
  and tests, pins formal origins, and records downstream references discovered
  in the requested source checkout. Existing consumers use the script
  entrypoints or the reviewed loader. Section functions take trusted `Cases`
  aggregates supplied by the application, not deserialized run state.
- `2026-11-03-ads-quality.json` contains strict pinned mypy and normal/optimized
  runs of the 15 AdS test groups and 24 first-25 regression groups. Its final
  test amendment records additional focused verification without rewriting
  prior outcomes. Fixed finite graph and matrix oracles supplement generated
  scalar properties; no production implementation supplies expected results.
- `ads_mutations.json` is the explicit mutation manifest. The original outcome
  receipt and `2026-11-03-ads-mutations-closure.json` retain all 68 candidates and
  the two additional challenge results. Mutation detection is evidence of test
  sensitivity, not a mathematical proof or an exhaustive bug census.
- The application dependencies are pinned. Structural metrics meet B ceilings:
  CCN at most 15, cognitive complexity at most 20, nesting at most four, and
  one class or fewer per source. Resource costs are stated per source.
- The graph and entropy helpers are independently tested shared infrastructure.
  Sharing them does not give multiple independent confirmations of the same
  algorithm. The HaPPY-like state is a supplied hand-encoded finite fixture;
  its identification with a tensor-network contraction is not established.
- Historical DAG campaign receipts keep their original scope and counts. This
  implementation review does not promote imported or open research nodes,
  prove a continuum duality, or claim a hosted CI run. The workflow now includes
  the new verification commands for future CI execution.
