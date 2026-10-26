# S(n) examples and verification scope

AuthorityEffect: None.

These Python modules are local educational examples. Source admission and
production mathematics are owned by the canonical Rust crates. See
[the source correspondence](../source_correspondence.md) for the distinction.

| Module | Actual scope |
| --- | --- |
| [sn_core.py](sn_core.py) | Supplied finite models; distinguishes supply/admission and accepts exact descent only on the section image. Counts and cost fields are fixture parameters. |
| [sn_realizations.py](sn_realizations.py) | Elementary graph, boundary, reversal, quantifier and dimension operations. No categorical composition or general Hodge solver. |
| [sn_applications.py](sn_applications.py) | Finite set join, two-step channel state machine, floating-point triangle and hinge examples. |
| [sn_verification.py](sn_verification.py) | Local cycle/progress monitor, twelve-field affordability record, Kleene truth operations and separate verification/policy calls. |
| [sn_codec.py](sn_codec.py) | Flat AST parsing/rendering; integer stage values normalize leading zeroes. |
| [sn_audit.py](sn_audit.py) | Explicit-profile syntax, spelling-preserving tagged codec, finite relation/colouring checks and YAML shape validation. |
| [check_sn.py](check_sn.py) | EBNF conformance against cases SN_001–SN_085. |
| [../lean4](../lean4/SnTheorems.lean) | Declared finite carriers and syntax; source-typed old-image law. |

Passing grammar tests does not verify the semantic examples E10–E21.
`AdjunctionCochain.verify_counit` is a legacy name for a section/retraction
identity; `DiscreteHodge.verify_dimension_sum` checks integer arithmetic.
`AutopoieticAudit` returns observed metadata, not a passing audit verdict.
The local Blue and Green callbacks are unsigned and do not authenticate a
policy authority; the calls demonstrate their separation only.

From the repository root, with Python 3.10+ and pytest/PyYAML installed:

```sh
python -m pytest omega_engine_education/documentation/002_oesn/code/tests -q
python omega_engine_education/documentation/002_oesn/code/check_sn.py
python omega_engine_education/documentation/002_oesn/code/sn_audit.py contracts --schema omega_engine_education/documentation/002_oesn/normal_forms/normal_form_contract_schema.yaml omega_engine_education/documentation/002_oesn/normal_forms/nf.*.yaml
```

On Windows select the installed interpreter, for example `py -3.12`, and
expand the YAML path list if the shell does not expand wildcards. The Lean
package pins its toolchain in `lean-toolchain`; run `lake build` in `lean4/`
with that toolchain. Proof compilation checks these local definitions, not
an unstated cross-language correspondence.
