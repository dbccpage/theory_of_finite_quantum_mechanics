"""Regression checks for evidence refusal, using retained actual campaigns."""
import unittest
import copy
import json
import tempfile
from pathlib import Path
from records import package_runs_pass, select_challenges, read, apply_individual_engineering_review
from replay import ROOT
from mutations import matching_literals, candidates, resume_kills, calibrated_headroom, classify

class EvidenceRefusalTests(unittest.TestCase):
    def test_empty_restoration_is_not_success(self):
        self.assertFalse(package_runs_pass([], {'tfqm_homotopy_type_theory'}))
        self.assertFalse(package_runs_pass([], set()))

    def test_failed_duplicate_and_timed_out_runs_are_not_success(self):
        run = dict(package='hott', exit_code=0, timed_out=False)
        self.assertTrue(package_runs_pass([run], {'hott'}))
        self.assertFalse(package_runs_pass([run, run], {'hott'}))
        self.assertFalse(package_runs_pass([{**run, 'exit_code': None}], {'hott'}))
        self.assertFalse(package_runs_pass([{**run, 'timed_out': True}], {'hott'}))

    def test_retained_disk_limited_restoration_is_refused(self):
        receipt = read(ROOT/'evidence/quality/l4a_six/20261020T051536Z-mutations/receipt.json')
        packages = {r['package'] for r in receipt['baselines']}
        self.assertTrue(package_runs_pass(receipt['baselines'], packages))
        self.assertFalse(package_runs_pass(receipt['restored_baselines'], packages))

    def test_captured_complete_restoration_is_accepted(self):
        receipt = read(ROOT/'evidence/quality/l4a_six/20261020T061219Z-mutations/receipt.json')
        packages = {r['package'] for r in receipt['baselines']}
        self.assertEqual(len(packages), 5)
        self.assertTrue(package_runs_pass(receipt['baselines'], packages))
        self.assertTrue(package_runs_pass(receipt['restored_baselines'], packages))

    def test_linked_observer_challenge_requires_exact_id_and_source(self):
        entries = read(ROOT/'evidence/quality/l4a_six/20261020T061219Z-mutations/mutations.json')
        source = 'code/rust/src/local_green_global_red_lggr/lggr_v.rs'
        subject = 'code/rust/src/local_green_global_red_lggr/tests/lggr_allocation.rs'
        links = {'LG06-witness-nonzero': dict(source=source, claim='early refusal before observation allocation')}
        selected, complete = select_challenges(entries, subject, links)
        self.assertTrue(complete)
        self.assertEqual([e['id'] for e in selected], ['LG06-witness-nonzero'])
        # Preserve the actual surviving outcome. Sharing evidence cannot turn it into a kill.
        self.assertEqual(selected[0]['outcome'], 'survived')
        links['LG06-witness-nonzero']['source'] = 'wrong-source.rs'
        self.assertEqual(select_challenges(entries, subject, links), ([], False))
        self.assertEqual(select_challenges(entries, subject, {'missing': dict(source=source, claim='missing fault')}), ([], False))

    def test_unexplained_evidence_link_is_refused(self):
        with self.assertRaises(RuntimeError):
            select_challenges([], 'subject.rs', {'fault': dict(source='other.rs')})

    def test_line_ending_correction_changes_only_the_unique_recipe_site(self):
        for source in ['prefix\na\nb\nsuffix\n', 'prefix\r\na\r\nb\r\nsuffix\r\n']:
            before, after = matching_literals(source, 'a\nb', 'a\nc')
            self.assertEqual(source.replace(before, after, 1), source.replace('b', 'c', 1))
            self.assertIsNone(matching_literals(source + source, 'a\nb', 'x'))
        self.assertIsNone(matching_literals('unrelated', 'a\nb', 'x'))

    @staticmethod
    def historical_continuation_entries(receipt_path):
        # This regression replays the retained 265-fault epoch. New designated
        # campaigns have their own IDs and must not change this fixture.
        keys = ("id", "source", "snapshot_source", "before", "after", "package", "target", "filter")
        return [{**{key: entry[key] for key in keys if key in entry}, "outcome": "unrun"}
                for entry in read(receipt_path.parent / "mutations.json")]

    def test_historical_continuation_refuses_different_candidate_bytes(self):
        path = ROOT/'evidence/quality/l4a_six/20261020T145348Z-mutations/receipt.json'
        prior = read(path)
        entries = self.historical_continuation_entries(path)
        sources = read(path.parent/'source_manifest.json')
        with self.assertRaisesRegex(RuntimeError, 'candidate bytes differ|fault site differs'):
            resume_kills(entries, path, sources, prior['versions'])

    def test_continuation_refuses_different_toolchain_and_source_epoch(self):
        path = ROOT/'evidence/quality/l4a_six/20261020T145348Z-mutations/receipt.json'
        prior = read(path)
        sources = read(path.parent/'source_manifest.json')
        with self.assertRaisesRegex(RuntimeError, 'toolchain differs'):
            resume_kills(candidates(), path, sources, {**prior['versions'], 'rustc': 'other'})
        with self.assertRaisesRegex(RuntimeError, 'source epoch differs'):
            resume_kills(candidates(), path, {}, prior['versions'])

    def test_continuation_refuses_changed_fault_and_duplicate_ids(self):
        path = ROOT/'evidence/quality/l4a_six/20261020T145348Z-mutations/receipt.json'
        prior = read(path)
        sources = read(path.parent/'source_manifest.json')
        changed = self.historical_continuation_entries(path)
        changed[0]['before'] += 'different'
        with self.assertRaisesRegex(RuntimeError, 'recipe differs'):
            resume_kills(changed, path, sources, prior['versions'])
        duplicate = self.historical_continuation_entries(path)
        duplicate.append(duplicate[0])
        with self.assertRaisesRegex(RuntimeError, 'duplicate current IDs'):
            resume_kills(duplicate, path, sources, prior['versions'])

    def test_cache_calibration_retains_a_margin_and_refuses_too_small_a_reserve(self):
        path = ROOT/'evidence/quality/l4a_six/20261020T145348Z-mutations/receipt.json'
        measured = calibrated_headroom(path, 1536 * 1024**2)
        self.assertEqual(measured['largest_observed_completed_cache_file_bytes'], 713309921)
        self.assertEqual(measured['additional_margin_bytes'], 512 * 1024**2)
        with self.assertRaisesRegex(RuntimeError, 'exceeds cold admission'):
            calibrated_headroom(path, 1024**3)

    def test_disk_compiler_failure_is_not_structural_invalidity_or_a_kill(self):
        parent = ROOT/'code/rust/target/l4a-six'
        with tempfile.TemporaryDirectory(prefix='disk-classifier-', dir=parent) as folder:
            self.assertEqual(Path(folder).resolve().parent, parent.resolve())
            path = Path(folder)/'diagnostic.log'
            path.write_text('error: could not compile test crate: There is not enough space on the disk. (os error 112)\n', encoding='utf8')
            run = dict(timed_out=False, exit_code=101, log=path.relative_to(ROOT).as_posix())
            self.assertEqual(classify(run, Path(folder))[0], 'inconclusive')

    def test_ratio_above_95_percent_does_not_hide_an_unresolved_critical_fault(self):
        # Pure grading-policy fixture, never saved as execution evidence.
        path = ROOT/'code/rust/src/homology/rank_certificate.rs.scoring.yaml'
        record = json.loads(path.read_text(encoding='utf8').split('\n', 1)[1])
        record['gates'] = dict.fromkeys(['G1', 'G2', 'G3', 'G4', 'G5'])
        record['mutation_accounting']['conservative_ratio'] = .96
        record['verification'].update(baseline=dict(exit_code=0), designated_challenges_present=True,
            mutation_restoration_baselines_ok=True, designated_critical_faults_decisive=False)
        specification = {"engineering_assessment": {
            "source_sha256": record["artifact"]["sha256"],
            "gates": {gate: {"grade": "A", "basis": "Synthetic grading-policy fixture; not an accepted review."}
                      for gate in ["G1", "G2", "G3", "G4", "G5"]}}, "open_obligations": []}
        refused = copy.deepcopy(record)
        apply_individual_engineering_review(refused, specification)
        self.assertIsNone(refused['gates']['G4'])
        self.assertFalse(refused['is_complete'])
        self.assertIsNone(refused['score_token'])
        record['mutation_accounting']['conservative_ratio'] = 1
        record['verification']['designated_critical_faults_decisive'] = True
        apply_individual_engineering_review(record, specification)
        self.assertEqual(record['gates']['G4'], 'A')

    def test_known_failure_remains_visible_without_a_completed_score(self):
        # Synthetic policy fixture; never written as a measured assessment.
        record = dict(artifact=dict(sha256="policy-fixture"), level="L3",
            gates=dict(G1=None, G2="E", G3=None, G4=None, G5=None),
            structure=dict(metric_ceiling="A"), grade_ceiling="A", open_findings=[],
            is_complete=False, composite_grade=None, score_token=None)
        specification = dict(engineering_assessment=dict(source_sha256="policy-fixture",
            gates={gate: dict(grade=None, basis="Unassessed synthetic policy input")
                   for gate in record["gates"]}))
        apply_individual_engineering_review(record, specification)
        self.assertEqual(record["gates"]["G2"], "E")
        self.assertEqual(record["grade_ceiling"], "E")
        self.assertFalse(record["is_complete"])
        self.assertIsNone(record["score_token"])

if __name__ == '__main__': unittest.main()
