"""Mutation regressions for reproduced gaps and evidence-custody predicates."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('audit_replay_tests', HERE / 'verify_review.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
checker = audit.checker


class ReviewGuards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.request = checker.load(audit.RUN / 'p3/request.json')
        cls.candidate = checker.load(audit.RUN / 'p3/candidate.json')
        cls.public = audit.public_input(cls.request)['cases']
        cls.i = next(i for i, a in enumerate(cls.candidate['cases']) if a['facets'] == ['0'] * 8)

    def fixture(self):
        request = copy.deepcopy(self.request)
        audit.public_input(request)['cases'] = [self.public[self.i]]
        request['input_sha256'] = hashlib.sha256(json.dumps(request['public_context'], sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
        candidate = dict(self.candidate, cases=[copy.deepcopy(self.candidate['cases'][self.i])], input_sha256=request['input_sha256'])
        return request, candidate

    def check(self, request, candidate):
        with tempfile.TemporaryDirectory() as tmp:
            rp, cp = Path(tmp)/'request.json', Path(tmp)/'candidate.json'
            rp.write_bytes(json.dumps(request).encode()); cp.write_bytes(json.dumps(candidate).encode())
            return checker.check(rp, cp)

    def test_valid_certificate_control(self):
        self.assertEqual(self.check(*self.fixture())['counts'], {'extended': 1, 'blocked': 0})

    def test_string_facet_array_is_rejected(self):
        case = copy.deepcopy(self.candidate['cases'][self.i]); case['facets'] = '00000000'
        with self.assertRaisesRegex(ValueError, 'G1_SCHEMA:facets_shape'):
            checker.check_case(self.public[self.i], case)

    def test_interval_arrays_require_two_cells(self):
        case = copy.deepcopy(self.candidate['cases'][0]); case['lower'] = '00'
        with self.assertRaisesRegex(ValueError, 'G1_SCHEMA:lower_shape'):
            checker.check_case(self.public[0], case)
        case['lower'] = self.candidate['cases'][0]['lower']; case['upper'] = None
        with self.assertRaisesRegex(ValueError, 'G1_SCHEMA:upper_shape'):
            checker.check_case(self.public[0], case)

    def test_consistently_relabelled_task_is_rejected(self):
        request, candidate = self.fixture(); request['task_id'] = candidate['task_id'] = 'UNRELATED-TASK'
        with self.assertRaisesRegex(ValueError, 'G1_SCHEMA:task'):
            self.check(request, candidate)

    def test_consistently_relabelled_stage_is_rejected(self):
        request, candidate = self.fixture(); request['stage_id'] = candidate['stage_id'] = 'P5_RECORD'
        with self.assertRaisesRegex(ValueError, 'G1_SCHEMA:stage'):
            self.check(request, candidate)

    def test_unbound_work_task_is_rejected(self):
        request, candidate = self.fixture(); request['public_context']['reviewed_work']['work_unit']['task_id'] = 'OTHER'
        with self.assertRaisesRegex(ValueError, 'G1_SCHEMA:work_task'):
            self.check(request, candidate)

    def test_context_digest_is_enforced(self):
        request, candidate = self.fixture(); request['public_context']['bounded_failure_codes'] = []
        with self.assertRaisesRegex(ValueError, 'G1_SCHEMA:context_digest'):
            self.check(request, candidate)

    def test_duplicate_case_ids_are_rejected(self):
        request, candidate = self.fixture(); audit.public_input(request)['cases'] *= 2; candidate['cases'] *= 2
        request['input_sha256'] = candidate['input_sha256'] = hashlib.sha256(json.dumps(request['public_context'], sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
        with self.assertRaisesRegex(ValueError, 'G1_SCHEMA:duplicate_case_id'):
            self.check(request, candidate)

    def test_duplicate_and_inexact_json_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)/'bad.json'
            for raw in ('{"x":1,"x":2}', '{"x":0.5}', '{"x":NaN}'):
                p.write_bytes(raw.encode())
                with self.assertRaisesRegex(ValueError, 'G1_SCHEMA:'):
                    checker.load(p)

    def test_same_counts_do_not_bind_a_repair_problem(self):
        first, second = copy.deepcopy(self.request), copy.deepcopy(self.request)
        second['public_context']['original_target']['source_statement'] += ' altered'
        with self.assertRaisesRegex(ValueError, 'binding:repair_problem_changed'):
            audit.repair_binding(first, second, self.candidate, self.candidate)

    def test_repair_witness_change_is_detected(self):
        changed = copy.deepcopy(self.candidate); changed['cases'][self.i]['separator'] = '1'
        with self.assertRaisesRegex(ValueError, 'binding:repair_numbers_changed'):
            audit.repair_binding(self.request, self.request, self.candidate, changed)

    def test_named_strings_do_not_replace_axiom_reports(self):
        output = '\n'.join("'QuantumMechanics.BellSeparatorExtension." + n + "'" for n in audit.ANCHORS)
        with self.assertRaisesRegex(ValueError, 'native:axiom_report_coverage'):
            audit.lean_reports(output)

    def test_custom_axiom_is_rejected(self):
        output = '\n'.join("'QuantumMechanics.BellSeparatorExtension." + n + "' depends on axioms: [madeUp]" for n in audit.ANCHORS)
        with self.assertRaisesRegex(ValueError, 'native:unapproved_axiom'):
            audit.lean_reports(output)

    def test_empty_receipts_and_substitute_commands_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'native:receipt_coverage'):
            audit.command_receipts([], [['lean', 'BellSeparatorExtension.lean']], HERE, HERE)
        receipt = {'argv': ['echo', 'passed'], 'cwd': str(HERE), 'exit_code': 0}
        with self.assertRaisesRegex(ValueError, 'native:wrong_command'):
            audit.command_receipts([receipt], [['lean', 'BellSeparatorExtension.lean']], HERE, HERE)

    def test_changed_two_sided_control_summary_is_rejected(self):
        control = checker.load(audit.RUN / 'p4/two_sided_chsh_control.json'); control['standard_CHSH_value'] = '1'
        saved = checker.load(audit.RUN / 'p4/host_check.json')['predicate_results']['controls']
        with self.assertRaisesRegex(ValueError, 'control:summary_not_derived'):
            audit.controls(control, self.candidate, self.public, saved)

    def test_inventory_corruption_empty_and_path_escape_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); p = root/'evidence.txt'; p.write_bytes(b'original')
            manifest = {'artifacts': [{'path': p.name, 'sha256': audit.sha(p)}]}
            audit.review_inventory(root, manifest); p.write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'custody:artifact:'):
                audit.review_inventory(root, manifest)
            with self.assertRaisesRegex(ValueError, 'custody:empty_manifest'):
                audit.review_inventory(root, {'artifacts': []})
            with self.assertRaisesRegex(ValueError, 'custody:path_escape'):
                audit.safe(root, '../outside')


if __name__ == '__main__':
    unittest.main()
