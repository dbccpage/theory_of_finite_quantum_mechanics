# CAQD: conditional discrete proof scope

The original Lean proof sources, `lean-toolchain`,
`lake-manifest.json`, and `axiom_report.txt` are preserved in this repair.
The toolchain pin is **leanprover/lean4:v4.34.0**. The stored report is historical;
no fresh kernel run was performed during the 2026-10-02 repair because Lake/Lean
were unavailable in that environment.

On 2026-10-11, `lake build` and `lake env lean CAQD/AxiomAudit.lean`
passed under the pinned Lean 4.34.0 toolchain. All 11 selected declarations
were reported: nine depend only on `propext` and `Quot.sound`, and the two
short-time identities have no axiom dependencies. Proof sources and the
historical report remain unchanged. This new replay retains the abstract
conditional scope described below.

`OperatorSpace` has an abstract carrier, Nat-valued operator and trace norm
fields, and an Int-valued pairing. It is not a concrete complex matrix model.
`DiscreteTrajectory` supplies Hölder and propagator contractivity as
hypotheses. The local-rate theorems assume residual domination. No matrix norm
laws, positivity, CPTP construction, continuous derivative, or Duhamel integral
are derived.

- `duhamel_observable_bound` bounds an abstract finite pairing sum.
- `certificate_honesty` and `margin_nonnegative` use an assumed
  local residual bound.
- `certified_tolerance_satisfaction` assumes that the accumulated bound
  already meets tolerance.
- `refinement_monotonicity` assumes pointwise smaller rates for all
  compared edges and steps; it does not establish that a merge achieves this.
- `single_step_rate` and
  `leading_linear_rate_matches_defect_sum` are one-step Nat sum identities,
  not continuous short-time asymptotics.

A logical axiom report lists kernel axioms, not theorem parameters. A theorem can
have only standard logical axioms while still depending on substantial
mathematical hypotheses.

For a fresh scoped check from this directory:

~~~bash
lake build
lake env lean CAQD/AxiomAudit.lean
~~~

The package verifier runs both commands when Lean is not skipped and rejects
`sorryAx`. It does not overwrite the historical report. From the package
root, `python verify_deposit.py --skip-lean` explicitly reports that these
checks were skipped. A successful skipped run is not a fresh proof audit.

