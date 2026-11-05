"""Bounded authority-checker contracts and independent rejection/oracle tests.

AuthorityEffect: None. Syntactic envelopes, finite behavior quotients and record
consistency are checked. No evaluator agreement or authorization is inferred.
"""
from __future__ import annotations

from collections.abc import Callable
import contextlib
from dataclasses import FrozenInstanceError
import hashlib
import io
from itertools import product
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from typing import cast
import unittest
from unittest.mock import patch

from hypothesis import given, settings, strategies as st

TESTS = Path(__file__).resolve().parent
sys.path.insert(0, str(TESTS))
from test_review_repairs import load
from checker_support.boundary import cli, evaluate, Violation
from checker_support.outcome import Outcome
from checker_support.domains import Failure

FAMILY = ("auth-dtm2-input-request-planned", "auth-rice-theorem-import", "authf-carrier-admission-gate")
PROPERTIES = settings(max_examples=80, derandomize=True, deadline=None, database=None)
WORDS = st.lists(st.integers(min_value=0, max_value=1 << 40), max_size=40)


def _fixture() -> dict[str, object]:
    return {"schema_version": "ait.computability_carrier_candidates.v1", "authority_effect": "None",
            "admission_status": "open", "candidates": [{"id": "AIT-DTM0", "admission_status": "partial",
            "selected": False, "fields": {"syntax_and_encoding": {"status": "partial"},
            "execution_semantics": {"status": "partial"}, "universality": {"status": "open"}}}]}


def _direct(record: dict[str, object]) -> dict[str, object]:
    return cast(list[dict[str, object]], record["candidates"])[0]


class AuthorityCheckerTests(unittest.TestCase):
    def refused(self, result: Outcome[object], kind: str) -> None:
        self.assertFalse(result.ok)
        self.assertIsNone(result.value)
        if result.error is None:
            self.fail("expected a typed refusal")
        self.assertEqual(result.error.kind, kind)

    def test_refusal_helper_rejects_success_and_wrong_failure_kind(self) -> None:
        with self.assertRaises(AssertionError):
            self.refused(Outcome(value=1), "input")
        with self.assertRaises(AssertionError):
            self.refused(Outcome(error=Failure("input", "bad input")), "resource")

    @PROPERTIES
    @given(fuel=st.integers(min_value=0, max_value=1 << 40), machine=WORDS, input_word=WORDS)
    def test_request_round_trip_and_independent_layout(self, fuel: int, machine: list[int], input_word: list[int]) -> None:
        module = load(FAMILY[0])
        request = module.RequestEnvelope(fuel, machine, input_word)
        expected = tuple([1, fuel, len(machine)] + machine + input_word)
        self.assertEqual(request.encode(), expected)
        self.assertEqual(module.RequestEnvelope.decode(expected).value, request)
        self.assertEqual(module.RequestEnvelope.decode(list(expected)).value.encode(), expected)
        self.assertEqual(request.machine, tuple(machine))
        self.assertEqual(request.input_word, tuple(input_word))

    def test_request_snapshot_immutability_and_resource_endpoints(self) -> None:
        module = load(FAMILY[0])
        machine, input_word = [7], [3, 4]
        request = module.RequestEnvelope(2, machine, input_word)
        machine[0], input_word[0] = 99, 99
        self.assertEqual(request.encode(), (1, 2, 1, 7, 3, 4))
        with self.assertRaises(FrozenInstanceError):
            request.fuel = 9
        maximum = (1 << 4096)-1
        request = module.RequestEnvelope(maximum, [maximum]*4093, [])
        self.assertEqual(len(request.encode()), 4096)
        self.assertEqual(module.RequestEnvelope.decode(request.encode()).value, request)
        self.refused(evaluate(module.RequestEnvelope, 0, [0]*4093, [0]), "resource")
        self.refused(evaluate(module.RequestEnvelope, 0, [0]*4094, []), "resource")
        self.refused(module.RequestEnvelope.decode([1, 0, 0]+[0]*4094), "resource")

    def test_request_every_token_boundary(self) -> None:
        module = load(FAMILY[0])
        bad: object
        for bad in (True, False, -1, 1.5, "1", None):
            self.refused(evaluate(module.RequestEnvelope, bad, (), ()), "input")
            self.refused(evaluate(module.RequestEnvelope, 0, (bad,), ()), "input")
            self.refused(evaluate(module.RequestEnvelope, 0, (), (bad,)), "input")
            for index in range(6):
                word: list[object] = [1, 2, 1, 7, 3, 4]
                word[index] = bad
                self.refused(module.RequestEnvelope.decode(word), "input")
        for index in range(6):
            word = [1, 2, 1, 7, 3, 4]
            word[index] = 1 << 4096
            self.refused(module.RequestEnvelope.decode(word), "resource")
        for bad in (None, "123", 4, iter([1, 2, 0])):
            self.refused(module.RequestEnvelope.decode(bad), "input")
            self.refused(evaluate(module.RequestEnvelope, 0, bad, ()), "input")
            self.refused(evaluate(module.RequestEnvelope, 0, (), bad), "input")
        for malformed in ([], [1], [1, 2], [0, 2, 1, 7], [2, 2, 1, 7], [1, 2, 4, 7, 3, 4]):
            self.refused(module.RequestEnvelope.decode(malformed), "input")

    def test_behavior_partition_and_all_three_code_predicates(self) -> None:
        module = load(FAMILY[1])
        carrier = module.RECORDED_CARRIER
        self.assertEqual(carrier.equivalence_classes(), ((0, 1), (2,)))
        for bits in product((False, True), repeat=3):
            result = carrier.factor_property(bits)
            self.assertEqual(result.ok, bits[0] == bits[1])
            if bits[0] == bits[1]:
                self.assertEqual(result.value, (bits[0], bits[2]))
            else:
                self.refused(result, "check")
        self.assertEqual(carrier.identity_bits(), (True, True, False))
        for code, point in product(range(3), range(2)):
            self.assertEqual(module.beh(code, point), point if code < 2 else 0)

    @PROPERTIES
    @given(width=st.integers(min_value=1, max_value=5), data=st.data())
    def test_generated_behavior_equivalence_and_descent(self, width: int, data: st.DataObject) -> None:
        rows = data.draw(st.lists(st.lists(st.integers(min_value=0, max_value=width-1),
                            min_size=width, max_size=width), min_size=1, max_size=12))
        module = load(FAMILY[1])
        carrier = module.FiniteBehaviorCarrier(rows)
        groups = carrier.equivalence_classes()
        self.assertEqual(sorted(code for block in groups for code in block), list(range(len(rows))))
        for left, right in product(range(len(rows)), repeat=2):
            same_block = any(left in block and right in block for block in groups)
            self.assertEqual(same_block, rows[left] == rows[right])
        bits = data.draw(st.lists(st.booleans(), min_size=len(rows), max_size=len(rows)))
        expected = all(rows[left] != rows[right] or bits[left] == bits[right]
                       for left, right in product(range(len(rows)), repeat=2))
        result = carrier.factor_property(bits)
        self.assertEqual(result.ok, expected)
        if expected:
            self.assertEqual(result.value, tuple(bits[block[0]] for block in groups))
        else:
            self.refused(result, "check")
        self.assertEqual(carrier.identity_bits(), tuple(row == list(range(width)) for row in rows))

    def test_behavior_constructor_and_property_refusals(self) -> None:
        module = load(FAMILY[1])
        invalid: object
        for invalid in (None, "rows", (), ((),), ((0, 1), (0,)), ((True,),), ((0.0,),), ((-1,),)):
            self.refused(evaluate(module.FiniteBehaviorCarrier, invalid), "input")
        for invalid in (((1,),), ((0,)*33,), ((0,),)*65):
            self.refused(evaluate(module.FiniteBehaviorCarrier, invalid), "resource")
        carrier = module.FiniteBehaviorCarrier([[0, 1], [0, 1], [0, 0]])
        for bits in ((), (False, True), (False, True, 0), "001", None):
            self.refused(carrier.factor_property(bits), "input")
        self.refused(carrier.factor_property([False]*65), "resource")
        for invalid in (True, -1, 0.5, "0"):
            self.refused(evaluate(carrier.behavior, invalid, 0), "input")
            self.refused(evaluate(carrier.behavior, 0, invalid), "input")
            self.refused(evaluate(module.id_bit, invalid), "input")
            self.refused(evaluate(module.code_zero, invalid), "input")
        self.refused(evaluate(carrier.behavior, 3, 0), "resource")
        self.refused(evaluate(carrier.behavior, 0, 2), "resource")

    def test_behavior_snapshot_and_maximum_table(self) -> None:
        module = load(FAMILY[1])
        rows = [[0, 1], [0, 1]]
        carrier = module.FiniteBehaviorCarrier(rows)
        rows[0][0] = 1
        rows.append([1, 1])
        self.assertEqual(carrier.rows, ((0, 1), (0, 1)))
        with self.assertRaises(FrozenInstanceError):
            carrier.rows = ()
        largest = module.FiniteBehaviorCarrier([list(range(32)) for _ in range(64)])
        self.assertEqual(largest.behavior(63, 31), 31)
        self.assertEqual(largest.equivalence_classes(), (tuple(range(64)),))
        self.assertEqual(largest.factor_property([True]*64).value, (True,))
        self.assertEqual(largest.identity_bits(), (True,)*64)

    def test_candidate_schema_and_identity_refusals(self) -> None:
        module = load(FAMILY[2])
        invalid: object
        for invalid in (None, [], 1, {1: "wrong key"}):
            self.refused(module.DirectCandidateCeiling.from_record(invalid), "input")
        for key in ("schema_version", "authority_effect", "admission_status", "candidates"):
            record = _fixture()
            del record[key]
            self.refused(module.DirectCandidateCeiling.from_record(record), "input")
        for candidates in ([], [None], [{"id": None}], [{"id": ""}], [{"id": "OTHER"}], "bad"):
            record = _fixture()
            record["candidates"] = candidates
            self.refused(module.DirectCandidateCeiling.from_record(record), "input")
        record = _fixture()
        record["candidates"] = [_direct(record)]*2
        self.refused(module.DirectCandidateCeiling.from_record(record), "input")
        record["candidates"] = [_direct(_fixture())]*65
        self.refused(module.DirectCandidateCeiling.from_record(record), "resource")
        record = _fixture()
        record["schema_version"] = "other schema"
        self.refused(module.DirectCandidateCeiling.from_record(record), "input")
        record["schema_version"] = module.SCHEMA
        record["authority_effect"] = "Approve"
        self.refused(module.DirectCandidateCeiling.from_record(record), "check")

    def test_candidate_fields_and_selection_are_typed(self) -> None:
        module = load(FAMILY[2])
        invalid: object
        for key in ("fields", "selected", "admission_status"):
            record = _fixture()
            del _direct(record)[key]
            self.refused(module.DirectCandidateCeiling.from_record(record), "input")
        for invalid in (0, 1, "false", None):
            record = _fixture()
            _direct(record)["selected"] = invalid
            self.refused(module.DirectCandidateCeiling.from_record(record), "input")
        for field in ("syntax_and_encoding", "execution_semantics", "universality"):
            for invalid in (None, {}, {"status": True}, {"status": "unknown"}):
                record = _fixture()
                cast(dict[str, object], _direct(record)["fields"])[field] = invalid
                self.refused(module.DirectCandidateCeiling.from_record(record), "input")
        for key in ("record_status", "candidate_status", "syntax_status", "execution_status", "universality_status"):
            kwargs: dict[str, object] = dict(record_status="open", candidate_status="partial", syntax_status="partial",
                                          execution_status="partial", universality_status="open", selected=False)
            kwargs[key] = 1
            self.refused(evaluate(lambda: module.DirectCandidateCeiling(**kwargs)), "input")
        self.refused(evaluate(module.DirectCandidateCeiling, "open", "partial", "partial", "partial", "open", 0), "input")

    def test_candidate_promotion_cannot_become_verification(self) -> None:
        module = load(FAMILY[2])
        original = ("open", "partial", "partial", "partial", "open", False)
        for index in range(5):
            for status in ("open", "partial", "closed", "admitted"):
                values = list(original)
                values[index] = status
                result = module.DirectCandidateCeiling(*values).verify()
                if tuple(values) == original:
                    self.assertTrue(result.ok)
                else:
                    self.refused(result, "check")
        self.refused(module.DirectCandidateCeiling(*original[:-1], True).verify(), "check")
        record = _fixture()
        ceiling = module.DirectCandidateCeiling.from_record(record).value
        _direct(record)["selected"] = True
        self.assertTrue(ceiling.verify().ok)
        with self.assertRaises(FrozenInstanceError):
            ceiling.selected = True

    def test_source_custody_rejects_changed_ceiling(self) -> None:
        module = load(FAMILY[2])
        with TemporaryDirectory(dir=TESTS) as directory:
            path = Path(directory)/"record.json"
            raw = json.dumps(_fixture()).encode()
            path.write_bytes(raw)
            result = module.verify_source(path)
            self.assertTrue(result.ok)
            self.assertEqual(result.value[1], hashlib.sha256(raw).hexdigest())
            record = _fixture()
            _direct(record)["selected"] = True
            path.write_text(json.dumps(record), encoding="utf-8")
            self.refused(module.verify_source(path), "check")
            output = io.StringIO()
            with contextlib.redirect_stderr(output):
                    self.assertEqual(cli(lambda: module.main(path)), 1)
            self.assertEqual(json.loads(output.getvalue())["kind"], "check")

    def test_source_invalid_json_and_bounded_io(self) -> None:
        module = load(FAMILY[2])
        fixtures = [(b'{"x":1,"x":2}', "duplicate"), (b'{"x":NaN}', "input"),
                    (b'{"x":Infinity}', "input"), (b'{', "input"), (b'\xff', "input"),
                    (b'['*2000+b']'*2000, "resource"), (b' '*((1 << 20)+1), "resource")]
        valid_prefix = json.dumps(_fixture())[:-1]
        fixtures.extend(((valid_prefix+',"extra":'+constant+'}').encode(), "input")
                        for constant in ("NaN", "Infinity", "-Infinity"))
        with TemporaryDirectory(dir=TESTS) as directory:
            path = Path(directory)/"record.json"
            for raw, kind in fixtures:
                path.write_bytes(raw)
                self.refused(module.verify_source(path), kind)
            path.unlink()
            self.refused(module.verify_source(path), "resource")
        self.refused(module.verify_source("record.json"), "input")
        raw = json.dumps(_fixture()).encode()
        stream = io.BytesIO(raw)
        with patch.object(Path, "open", return_value=stream):
            result = module.verify_source(Path("ignored"))
        self.assertTrue(result.ok)
        self.assertTrue(stream.closed)
        self.assertEqual(result.value[1], hashlib.sha256(raw).hexdigest())
        stream = io.BytesIO(raw)
        with patch.object(Path, "open", return_value=stream), patch.object(module.json, "loads", side_effect=RecursionError()):
            self.refused(module.verify_source(Path("ignored")), "resource")
        self.assertTrue(stream.closed)

    def test_source_byte_limit_and_scope_preservation(self) -> None:
        module = load(FAMILY[2])
        raw = json.dumps(_fixture()).encode()
        with TemporaryDirectory(dir=TESTS) as directory:
            path = Path(directory)/"record.json"
            path.write_bytes(raw+b' '*(module.MAX_RECORD_BYTES-len(raw)))
            self.assertTrue(module.verify_source(path).ok)
            record = _fixture()
            record["unrelated_note"] = "not an adequacy proof"
            cast(list[object], record["candidates"]).append({"id": "OTHER", "selected": True})
            path.write_text(json.dumps(record), encoding="utf-8")
            self.assertTrue(module.verify_source(path).ok)

    def test_json_depth_ignores_quoted_brackets_and_escapes(self) -> None:
        module = load(FAMILY[2])
        record = _fixture()
        record["unrelated_note"] = '\\"'+'['*200+'\\\\'+']'*200
        with TemporaryDirectory(dir=TESTS) as directory:
            path = Path(directory)/"record.json"
            path.write_text(json.dumps(record), encoding="utf-8")
            self.assertTrue(module.verify_source(path).ok)
            raw = json.dumps(_fixture())[:-1]+',"extra":'+'['*127+'0'+']'*127+'}'
            path.write_text(raw, encoding="utf-8")
            self.assertTrue(module.verify_source(path).ok)
            path.write_text(raw.replace('"extra":[', '"extra":[[').replace('0]', '0]]'), encoding="utf-8")
            self.refused(module.verify_source(path), "resource")

    def test_current_source_cli_and_repeatability(self) -> None:
        for stem in FAMILY:
            module = load(stem)
            operation: Callable[[], int] = module.check if stem == FAMILY[1] else module.main
            outputs = []
            for _ in range(2):
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    self.assertEqual(operation(), 0)
                outputs.append(output.getvalue())
            self.assertEqual(outputs[0], outputs[1])
            self.assertIn("failures", outputs[0])
        module = load(FAMILY[2])
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(module.main(), 0)
        result = module.verify_source(module.SOURCE_RECORD)
        self.assertEqual(result.value[1], hashlib.sha256(module.SOURCE_RECORD.read_bytes()).hexdigest())
        with patch.object(module, "verify_source", return_value=Outcome(value=None)):
            self.refused(evaluate(module.main), "check")


if __name__ == "__main__":
    unittest.main(verbosity=2)
