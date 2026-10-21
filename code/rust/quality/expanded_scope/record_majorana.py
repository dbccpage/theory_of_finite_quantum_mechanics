"""Store five authored, source-bound reviews and preserve all earlier outcomes.

Passing tests and observations are preconditions, not automatic level inference.
The authored capability/gate decisions live in batch6_reviews.json.
"""
from collections import Counter
import ast
import json
from pathlib import Path

from record_batch2 import ROOT, add, pin, store

BASE = ROOT / 'evidence/quality/expanded_scope'
FIRST = BASE / '20261020T233919Z-majorana-challenge/receipt.json'
INTERIM = BASE / '20261020T234301Z-majorana-followup-challenge/receipt.json'
FINAL = BASE / '20261020T234424Z-majorana-followup-challenge/receipt.json'
METRICS = BASE / '20261020T233818Z-source-metrics/receipt.json'
BEFORE = BASE / '20261020T231517Z-majorana-before'
CHECKER_BEFORE = BASE / '20261020T233101Z-majorana-checker-before'
REVIEWS = Path(__file__).with_name('batch6_reviews.json')


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def document(source):
    target = source.with_name(source.stem + store.SUFFIX)
    return target, store.load(target) if target.is_file() else store.empty(source)


def validate_current_receipt(path):
    receipt = load(path)
    assert receipt['inputs_unchanged']
    for name, digest in receipt['inputs'].items():
        assert pin(ROOT / name)['sha256'] == digest, 'Stale challenge dependency: ' + name
    for row in receipt['files'].values():
        assert row['baseline_passed'] and row['baseline']['status'] == 'SURVIVED'
        assert row['source_sha256'] == pin(ROOT / row['source'])['sha256']
    return receipt


def audit_campaign(first, final):
    resolved, invalid = {}, []
    for path, receipt in [(FIRST, first), (FINAL, final)]:
        for module, result in receipt['files'].items():
            table = resolved.setdefault(module, {})
            for mutant in result['mutants']:
                if mutant['status'] == 'INVALID':
                    invalid.append({'module': module, 'receipt': pin(path), **mutant,
                        'review': 'No candidate was constructed: the class-callback site matched twice. Excluded as structurally inadmissible, never counted as a kill; replaced by a unique function-site candidate in the final replay.'})
                    continue
                key = mutant['source_sha256']
                table[key] = {'module': module, 'receipt': pin(path), **mutant}
    assert len(invalid) == 1 and invalid[0]['matches'] == 2
    assert all(row['status'] == 'KILLED' for table in resolved.values() for row in table.values())
    assert sum(map(len, resolved.values())) == 69
    interim = load(INTERIM)
    assert interim['inputs_unchanged']
    for row in interim['files'].values():
        assert row['source_sha256'] == pin(ROOT / row['source'])['sha256']
    attempts = Counter()
    for receipt in [first, interim, final]:
        for row in receipt['files'].values():
            attempts.update(item['status'] for item in row['mutants'])
    assert dict(attempts) == {'SURVIVED': 6, 'KILLED': 75, 'INVALID': 1}
    audit = {
        'AuthorityEffect': 'None', 'status': 'PASS',
        'receipts': [pin(FIRST), pin(INTERIM), pin(FINAL)],
        'raw_attempt_outcomes': dict(attempts),
        'resolved_unique_valid_candidates': {module: list(rows.values()) for module, rows in resolved.items()},
        'final_outcomes': {'KILLED': 69, 'SURVIVED': 0, 'INCONCLUSIVE': 0, 'UNRUN': 0},
        'excluded_invalid_attempts': invalid,
        'detection_fraction': {'numerator': 69, 'denominator': 69},
        'accounting': 'Candidate-byte SHA-256, within each module, deduplicates replays. The six raw survivors remain six survivor observations, not six kills. Current source-bound replays resolve the distinct valid faults; one invalid ambiguous site is excluded with a written reason. No equivalence exclusions are used in this batch.',
        'review_findings': [
            'The initial float-guard removal changed an advertised refusal invariant but the chosen tests asserted only the exception class. The separate follow-up tests check the promised diagnostic.',
            'The internal product-degree and output-term checks have later public-constructor checks. Follow-up tests check the internal degree-result and accumulation-buffer postconditions directly. Detection at that internal scope is not claimed as a newly discovered public algebra error.',
            'The first follow-up output-term test name contained mutation, so the runner deselected it under not mutation. Its survivor remains. The final input snapshot uses buffer_change; the binding log confirms the direct helper and the candidate source.',
            'Parity site preflight is tested before identity allocation using a forbidden allocation fixture. Exponent preflight is tested with an otherwise cancelling quotient. These are declared engineering resource policies, not derived physical constants.',
            'The initial bounded diagnostic collection is terminal with five missing-native-package import errors. It is neither a passed Majorana integration suite nor evidence of an E-level mathematical defect.',
            'The final six-file focused regression passes 60 tests including the legacy finite mutation suites; those legacy candidate counts are not added to this deduplicated source-bound count.',
        ],
        'interim_test_custody': 'The first follow-up test source was later changed to repair the name-filter issue and add the helper postcondition. Its exact bytes remain in that capsule. It supplies raw history, not a current-test certification; current dependencies are required for FIRST and FINAL only.',
        'scope_ceiling': 'Finite Python provider/codec and controlled-checker claims only. No complete Majorana package, native deployment, Rust/Python equivalence, theorem build or full-scope certification.',
    }
    path = BASE / 'batch6-challenge-review.json'
    path.write_text(json.dumps(audit, indent=2) + '\n', encoding='utf-8')
    return path, resolved


def historical(doc, target, source, definition):
    folder = CHECKER_BEFORE if source.name == 'test_majorana_control.py' else BEFORE
    snapshot = folder / 'sources' / source.relative_to(ROOT)
    assert snapshot.is_file()
    subject = {'path': source.relative_to(ROOT).as_posix(), 'sha256': pin(snapshot)['sha256']}
    evidence = [pin(snapshot), pin(folder / 'receipt.json')]
    if source.name == 'majorana_modes.py':
        evidence.append(pin(CHECKER_BEFORE / 'sealed-mode-alias-replay.json'))
    gates = dict.fromkeys(['G1', 'G2', 'G3', 'G4', 'G5'])
    gates.update(definition['historical_gates'])
    contract = {'AuthorityEffect': 'None', 'artifact': subject, 'profile': 'Exact',
        'purpose': 'Historical pre-repair implementation under independent checks; later policies and capabilities are not retroactive.',
        'captured_claims_verbatim': ast.get_docstring(ast.parse(snapshot.read_bytes())),
        'claims_status': 'Captured source claims, not endorsed scores or proof receipts.',
        'finding': definition['historical_finding'], 'evidence': evidence}
    score = {'AuthorityEffect': 'None', 'artifact': subject, 'profile': 'Exact', 'rubric': pin(ROOT / 'SCORING.md'),
        'level': definition['historical_level'], 'gates': gates, 'is_complete': False,
        'composite_grade': None, 'score_token': None, 'target_achieved': False,
        'grade_ceiling': 'E' if 'E' in gates.values() else 'D',
        'finding': definition['historical_finding'], 'evidence': evidence}
    add(doc, target, 'historical-before-majorana-repair', contract, score)


def main():
    first, final = validate_current_receipt(FIRST), validate_current_receipt(FINAL)
    audit_path, resolved = audit_campaign(first, final)
    metrics = load(METRICS)
    assert metrics['status'] == 'PASS'
    baseline = BASE / 'batch6-baseline.log'
    assert '60 passed' in baseline.read_text()
    assert 'all_passed=True' in (BASE / 'batch6-atlas.log').read_text()
    assert '5 passed' in (BASE / 'batch6-atlas-tests.log').read_text()
    definitions = load(REVIEWS)
    evidence = [pin(path) for path in [FIRST, FINAL, audit_path, METRICS, REVIEWS, baseline,
        BASE / 'batch6-atlas.log', BASE / 'batch6-atlas-tests.log',
        BASE / '20261020T231621Z-majorana-collection/receipt.json']]
    assessments = {}
    for name, definition in definitions.items():
        source = ROOT / name
        subject = pin(source)
        assert definition['claim'] in source.read_text()
        measured = metrics['sources'][name]
        assert measured['source_sha256'] == subject['sha256'] and measured['unchanged']
        assert not measured['unsupported_syntax']
        assert measured['maxima']['radon_ccn'] <= 10 and measured['maxima']['lizard_ccn'] <= 10
        assert measured['maxima']['weighted_control_upper_bound'] <= 25
        assert measured['maxima']['control_nesting'] <= 5
        target, doc = document(source)
        doc['assurance'] = 'Append-only captured defects and individually authored bounded reviews; no whole-package or full-scope certification.'
        historical(doc, target, source, definition)
        contract = {'AuthorityEffect': 'None', 'artifact': subject, 'profile': 'Exact',
            'claim': definition['claim'], 'role': definition['role'], 'operations': definition['operations'],
            'engineering_policy': definition['policy'], 'failure_boundary': definition['failure'],
            'cost_model': definition['cost'], 'scope_ceiling': definition['ceiling'],
            'origin': 'Exact pre-repair workspace source snapshot and literal source origin annotation retained in the historical contract. Fock names the Rust owner; this run does not compile or prove cross-language equivalence.',
            'trust': 'Pinned provider/test and rubric bytes, CPython 3.14 and installed SymPy/Fraction semantics. Closed built-in/canonical types avoid ordinary user hooks. Other conftest/provider transitive code, OS/interpreter state, hostile metaclasses, deliberate reflection, monkeypatching, hostile concurrent mutation and host exhaustion are not independently certified or sandboxed.',
            'negative_float_fixture_policy': 'Binary floats are used only in deliberate rejection or detached-export probes; no admitted exact arithmetic uses them.',
            'evidence': evidence}
        count = len(resolved[definition['module']])
        score = {'AuthorityEffect': 'None', 'artifact': subject, 'profile': 'Exact',
            'rubric': pin(ROOT / 'SCORING.md'), 'level': definition['level'],
            'level_basis': definition['level_basis'], 'gates': definition['gates'],
            'basis': {
                'G1': 'Literal claim URN, authority ceiling, current subject/dependency pins, retained origin bytes and reviewed exported signatures. No full downstream/AST equivalence or external provenance attestation.',
                'G2': 'Exact profile fixed before checks; independent Fraction-pair matrix arithmetic, adjacent-swap blade oracle, occupation action and valid/invalid canonical values. Finite laws and resource/type boundaries only; no exhaustive theorem inferred.',
                'G3': definition['failure'],
                'G4': str(count) + ' unique valid designated candidate-byte faults resolved KILLED against passing source-bound baselines. Original raw survivors and invalid site retained, with current replays and candidate bindings. Systematic finite negative/composition checks support C, not complete error-space, provider deployment or alternate-checker assurance.',
                'G5': definition['g5_basis']},
            'metrics': measured['maxima'], 'mutation_outcomes': {'KILLED': count},
            'is_complete': True, 'composite_grade': 'C', 'score_token': 'L4C',
            'requested_target': 'L4E or higher', 'target_achieved': True,
            'target_scope': 'This exact source only; full 24-directory objective remains open.',
            'open_higher_grade_findings': ['Full downstream/provider provenance', 'Exhaustive or formal semantic/failure assurance', 'Alternate independent harness replay', 'Measured peak-memory and wall-clock guarantees'],
            'evidence': evidence}
        assert definition['level'] == 'L4' and min(definition['gates'].values(), key=['E','D','C','B','A','A+'].index) == 'C'
        add(doc, target, 'bounded-majorana-source-review', contract, score)
        store.save(target, doc)
        assessments[name] = {'source': subject, 'companion': pin(target), 'score_token': 'L4C', 'evidence': evidence}
    ancillary = []
    names = ['code/python/src/majorana/__init__.py', 'code/python/tests/test_majorana_integrity.py',
        'code/python/tests/test_majorana_boundaries_followup.py', 'code/python/tests/test_majorana_modes.py',
        'code/rust/quality/expanded_scope/check_majorana.py', 'code/rust/quality/expanded_scope/check_majorana_followup.py',
        'code/rust/quality/expanded_scope/record_majorana.py', 'code/rust/quality/expanded_scope/batch6_reviews.json',
        'code/rust/quality/expanded_scope/summarize.py']
    for name in names:
        source = ROOT / name
        target, doc = document(source)
        is_package = name == 'code/python/src/majorana/__init__.py'
        doc['assurance'] = 'Explicit partial support or package-export review; no completed source capability/grade token.'
        purpose = ('The scalar seal boundary was repaired and its legacy checks run. The broad reexport surface and its providers remain unreviewed, so no package-wide L4 token is issued.' if is_package else
            'Review/test/receipt support outside the requested directories; its own source assessment remains partial. Passing this suite does not certify the test file or its unrelated existing protocol.')
        contract = {'AuthorityEffect': 'None', 'artifact': pin(source), 'purpose': purpose,
            'scope_ceiling': 'Partial review only; no inherited provider grade.', 'evidence': evidence}
        score = {'AuthorityEffect': 'None', 'artifact': pin(source), 'rubric': pin(ROOT / 'SCORING.md'),
            'level': None, 'gates': {'G1': 'C', 'G2': None, 'G3': None, 'G4': None, 'G5': None},
            'is_complete': False, 'composite_grade': None, 'score_token': None, 'target_achieved': False,
            'refusal': purpose, 'evidence': evidence}
        add(doc, target, 'partial-majorana-review-support-' + pin(source)['sha256'][:12], contract, score)
        store.save(target, doc)
        ancillary.append({'source': pin(source), 'companion': pin(target)})
    summary = {'AuthorityEffect': 'None', 'full_scope_target_achieved': False, 'files': assessments,
        'ancillary_partial_reviews': ancillary, 'challenge_review': pin(audit_path)}
    (BASE / 'batch6-assessments.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'complete_at_target': len(assessments), 'new_unique_valid_faults_killed': 69,
        'full_scope_target_achieved': False}))


if __name__ == '__main__':
    main()
