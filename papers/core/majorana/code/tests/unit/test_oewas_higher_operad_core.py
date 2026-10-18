"""Core and adversarial laws for the dependency-free OEWAS operad kernel."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

KERNEL_ROOT = Path(__file__).resolve().parents[1] / "kernel"
PACKAGE_ROOT = KERNEL_ROOT / "higher_operad"
if "higher_operad" not in sys.modules:
    spec = importlib.util.spec_from_file_location(
        "higher_operad",
        PACKAGE_ROOT / "__init__.py",
        submodule_search_locations=[str(PACKAGE_ROOT)],
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load higher_operad package")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

from higher_operad import (  # noqa: E402
    AgentLicense,
    AuthorityEffect,
    BudgetTransition,
    ColourSpec,
    Err,
    ExecutionEvent,
    Identity,
    InvocationGrade,
    ObligationBundle,
    ObligationKind,
    Ok,
    OperandRef,
    OperationSpec,
    PortSpec,
    Primitive,
    ProofObligation,
    Refusal,
    Substitute,
    authorize_term,
    canonical_id,
    export_lean_obligations,
    identity,
    normalize,
    normalize_term,
)

D0 = "sha256:" + "0" * 64
D1 = "sha256:" + "1" * 64
D2 = "sha256:" + "2" * 64
D3 = "sha256:" + "3" * 64
D4 = "sha256:" + "4" * 64
D5 = "sha256:" + "5" * 64
D6 = "sha256:" + "6" * 64
D7 = "sha256:" + "7" * 64
D8 = "sha256:" + "8" * 64
D9 = "sha256:" + "9" * 64


def port(name: str, colour: str) -> PortSpec:
    return PortSpec(name, colour, f"schema:{colour}:v1")


def operation(
    name: str,
    inputs: tuple,
    output: PortSpec,
    *,
    grade: InvocationGrade = InvocationGrade.DISCIPLINE,
    tools: tuple = (),
    effects: tuple = (),
    effect: AuthorityEffect = AuthorityEffect.NONE,
    ceiling: AuthorityEffect = AuthorityEffect.NONE,
) -> OperationSpec:
    return OperationSpec(
        operation_id=name,
        version="v1",
        input_ports=inputs,
        output_port=output,
        executor_ref=f"executor:{name}",
        executor_digest=D1,
        tool_refs=tools,
        effects=effects,
        invocation_grade=grade,
        authority_effect=effect,
        authority_ceiling=ceiling,
    )


class ResultAndCanonicalTests(unittest.TestCase):
    def test_result_bind_short_circuits_refusal(self) -> None:
        failure = Err(Refusal("NO_WITNESS", "missing witness"))
        self.assertIs(failure.bind(lambda value: Ok(value)), failure)
        self.assertEqual(Ok(2).bind(lambda value: Ok(value + 1)).unwrap(), 3)

    def test_colour_and_operand_bind_schema_provenance(self) -> None:
        colour = ColourSpec("Code", "software", "schema:Code:v1", D1, "validator:code", D2)
        changed = replace(colour, schema_digest=D3)
        self.assertNotEqual(colour.canonical_id, changed.canonical_id)
        operand = OperandRef(D4, "Code", "schema:Code:v1", D5, D6)
        self.assertTrue(operand.matches(port("code", "Code")))
        self.assertNotEqual(operand.canonical_id, replace(operand, provenance_root=D7).canonical_id)

    def test_canonical_maps_reject_normalized_key_collision(self) -> None:
        with self.assertRaisesRegex(ValueError, "key collision"):
            canonical_id("omega.test.v1", {"e\u0301": 1, "é": 2})

    def test_operation_is_immutable_and_id_binds_ordered_tools_effects(self) -> None:
        op = operation(
            "lint",
            (port("code", "Code"),),
            port("audit", "Audit"),
            tools=("tool:a", "tool:b"),
            effects=("effect:read", "effect:emit"),
        )
        with self.assertRaises(FrozenInstanceError):
            op.operation_id = "evil"
        self.assertNotEqual(op.canonical_id, replace(op, tool_refs=("tool:b", "tool:a")).canonical_id)
        self.assertNotEqual(op.canonical_id, replace(op, effects=("effect:emit", "effect:read")).canonical_id)

    def test_operation_effect_cannot_exceed_its_ceiling(self) -> None:
        with self.assertRaisesRegex(ValueError, "exceeds"):
            operation(
                "mutate",
                (port("state", "State"),),
                port("state_out", "State"),
                effect=AuthorityEffect.STATE_TRANSITION,
                ceiling=AuthorityEffect.NONE,
            )


class TermNormalizationTests(unittest.TestCase):
    def setUp(self) -> None:
        a = port("a", "A")
        b = port("b", "B")
        c = port("c", "C")
        d = port("d", "D")
        self.f = operation("f", (a,), b)
        self.g = operation("g", (b,), c)
        self.h = operation("h", (c,), d)

    def test_associativity_normalizes_to_same_rooted_tree(self) -> None:
        left = Substitute(Substitute(Primitive(self.h), 0, Primitive(self.g)), 0, Primitive(self.f))
        right = Substitute(Primitive(self.h), 0, Substitute(Primitive(self.g), 0, Primitive(self.f)))
        left_n = normalize_term(left).unwrap()
        right_n = normalize_term(right).unwrap()
        self.assertEqual(left_n.canonical_id, right_n.canonical_id)
        self.assertEqual(left_n.boundary.inputs[0].colour_id, "A")
        self.assertEqual(left_n.boundary.output.colour_id, "D")

    def test_units_normalize_away(self) -> None:
        right_unit = normalize_term(Substitute(Primitive(self.f), 0, Identity(port("same", "A")))).unwrap()
        left_unit = normalize_term(Substitute(Identity(port("same", "B")), 0, Primitive(self.f))).unwrap()
        primitive = normalize_term(Primitive(self.f)).unwrap()
        self.assertEqual(right_unit.canonical_id, primitive.canonical_id)
        self.assertEqual(left_unit.canonical_id, primitive.canonical_id)

    def test_ill_typed_and_out_of_range_composition_refuse(self) -> None:
        mismatch = normalize_term(Substitute(Primitive(self.h), 0, Primitive(self.f)))
        self.assertIsInstance(mismatch, Err)
        self.assertEqual(mismatch.error.code, "BOUNDARY_MISMATCH")
        out = normalize_term(Substitute(Primitive(self.f), 1, Primitive(self.f)))
        self.assertIsInstance(out, Err)
        self.assertEqual(out.error.code, "SLOT_OUT_OF_RANGE")

    def test_many_unary_parenthesizations_have_one_id(self) -> None:
        for _ in range(20):
            left = normalize_term(Substitute(Substitute(Primitive(self.h), 0, Primitive(self.g)), 0, Primitive(self.f))).unwrap()
            right = normalize_term(Substitute(Primitive(self.h), 0, Substitute(Primitive(self.g), 0, Primitive(self.f)))).unwrap()
            self.assertEqual(left.canonical_id, right.canonical_id)


class CapabilityAndTraceTests(unittest.TestCase):
    def _license(self, op: OperationSpec, **changes: object) -> AgentLicense:
        data = dict(
            agent_id="agent:test",
            allowed_operation_keys=(op.key,),
            allowed_colour_ids=tuple(sorted({p.colour_id for p in op.input_ports + (op.output_port,)})),
            allowed_executor_refs=(op.executor_ref,),
            allowed_tool_refs=op.tool_refs,
            allowed_effects=op.effects,
            authority_ceiling=op.authority_ceiling,
            lifecycle="Active",
            policy_digest=D2,
        )
        data.update(changes)
        return AgentLicense(**data)

    def test_capability_closure_checks_operation_colour_executor_tool_effect(self) -> None:
        op = operation(
            "compile",
            (port("code", "Code"),),
            port("audit", "Audit"),
            tools=("tool:compiler",),
            effects=("effect:read",),
        )
        term = Primitive(op)
        self.assertIsInstance(authorize_term(self._license(op), term), Ok)
        attacks = (
            ("allowed_operation_keys", (), "OPERATION_CAPABILITY_ESCAPE"),
            ("allowed_colour_ids", ("Code",), "COLOUR_CAPABILITY_ESCAPE"),
            ("allowed_executor_refs", (), "EXECUTOR_CAPABILITY_ESCAPE"),
            ("allowed_tool_refs", (), "TOOL_CAPABILITY_ESCAPE"),
            ("allowed_effects", (), "EFFECT_CAPABILITY_ESCAPE"),
        )
        for field, value, code in attacks:
            with self.subTest(field=field):
                result = authorize_term(self._license(op, **{field: value}), term)
                self.assertIsInstance(result, Err)
                self.assertEqual(result.error.code, code)

    def test_entry_over_entry_refuses(self) -> None:
        inner = operation(
            "inner-entry",
            (port("x", "X"),),
            port("y", "Y"),
            grade=InvocationGrade.ENTRY,
        )
        outer = operation(
            "outer-entry",
            (port("y2", "Y"),),
            port("z", "Z"),
            grade=InvocationGrade.ENTRY,
        )
        license = AgentLicense(
            "agent:entry",
            (inner.key, outer.key),
            ("X", "Y", "Z"),
            (inner.executor_ref, outer.executor_ref),
            (),
            (),
            AuthorityEffect.NONE,
            "Active",
            D2,
        )
        result = authorize_term(license, Substitute(Primitive(outer), 0, Primitive(inner)))
        self.assertIsInstance(result, Err)
        self.assertEqual(result.error.code, "ENTRY_OVER_ENTRY")

    def test_execution_event_binds_all_replay_inputs_and_parent_order(self) -> None:
        operand_in = OperandRef(D1, "Code", "schema:Code:v1", D2, D3)
        operand_out = OperandRef(D4, "Audit", "schema:Audit:v1", D5, D6)
        event = ExecutionEvent(
            run_id="run:1",
            sequence=2,
            plan_digest=D1,
            operation_spec_digest=D2,
            executor_digest=D3,
            policy_digest=D4,
            environment_digest=D5,
            validator_ref="validator:audit",
            validator_digest=D6,
            verifier_ref="verifier:replay",
            verifier_digest=D7,
            admission_receipt_refs=(D2, D5),
            inputs=(operand_in,),
            outputs=(operand_out,),
            parent_event_refs=(D8, D9),
            budget=BudgetTransition(4, 3),
            outcome_code="Completed",
            outcome_digest=D0,
        )
        self.assertEqual(event.authority_effect, AuthorityEffect.NONE)
        variants = (
            replace(event, plan_digest=D0),
            replace(event, operation_spec_digest=D0),
            replace(event, executor_digest=D0),
            replace(event, policy_digest=D0),
            replace(event, environment_digest=D0),
            replace(event, validator_ref="validator:other"),
            replace(event, validator_digest=D0),
            replace(event, verifier_ref="verifier:other"),
            replace(event, verifier_digest=D0),
            replace(event, admission_receipt_refs=(D5, D2)),
            replace(event, parent_event_refs=(D9, D8)),
            replace(event, budget=BudgetTransition(4, 2)),
            replace(event, outcome_digest=D1),
        )
        self.assertTrue(all(event.canonical_id != variant.canonical_id for variant in variants))
        with self.assertRaisesRegex(ValueError, "AuthorityEffect None"):
            replace(event, authority_effect=AuthorityEffect.FACT_ONLY)

    def test_budget_cannot_increase(self) -> None:
        with self.assertRaisesRegex(ValueError, "increase"):
            BudgetTransition(1, 2)

    def test_execution_event_requires_operand_admission_receipts(self) -> None:
        operand = OperandRef(D1, "Code", "schema:Code:v1", D2, D3)
        with self.assertRaisesRegex(ValueError, "cover"):
            ExecutionEvent(
                "run:missing-receipt",
                0,
                D1,
                D2,
                D3,
                D4,
                D5,
                "validator:code",
                D6,
                "verifier:replay",
                D7,
                (),
                (operand,),
                (),
                (),
                BudgetTransition(1, 0),
                "Completed",
                D0,
            )


class ObligationTests(unittest.TestCase):
    def test_export_is_deterministic_and_open_not_proved(self) -> None:
        first = ProofObligation("assoc:1", ObligationKind.ASSOCIATIVITY, "left = right", (D1, D2))
        second = ProofObligation("unit:1", ObligationKind.UNIT, "id(f) = f", (D3,))
        bundle_a = ObligationBundle("bundle:1", "v1", (D4,), (second, first))
        bundle_b = ObligationBundle("bundle:1", "v1", (D4,), (first, second))
        self.assertEqual(bundle_a.canonical_id, bundle_b.canonical_id)
        self.assertIn(b'"status":"Open"', bundle_a.export_bytes())
        self.assertEqual(bundle_a.authority_effect, AuthorityEffect.NONE)

    def test_public_identity_normalize_and_bounded_obligation_export(self) -> None:
        typed_port = port("input", "A")
        identity_term = normalize(identity(typed_port)).unwrap()
        bundle = export_lean_obligations((identity_term,), 4)
        self.assertEqual(len(bundle.obligations), 4)
        self.assertTrue(all(row.to_canonical()["status"] == "Open" for row in bundle.obligations))
        self.assertEqual(bundle.authority_effect, AuthorityEffect.NONE)


if __name__ == "__main__":
    unittest.main()
