"""Read-only audit replay. Receipts record executions, not independent authority.

The original run is sealed. This successor verifies its inventory, stricter
certificate predicates, unchanged repair problem, controls, and fresh receipts.
Pass --working-sources to require the current checkout to match audited bytes.
"""
import argparse
from collections import Counter, defaultdict
import contextlib
from decimal import Decimal
from fractions import Fraction as Q
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
REVIEW = Path(__file__).resolve().parent
BASE = REVIEW.parent.parent
RUN = BASE / 'runs/20261018T233710Z_separator_extension'
ROOT = next(p for p in REVIEW.parents if (p / 'dag/pfp/prepare_stage.py').is_file())
TASK = 'FQ-BELL-CLASSICAL-JOINT-EXTENSION'
ANCHORS = ('separator_iff_chsh', 'split_triple_exists', 'chsh_has_two_triples', 'full_family_joint_necessity')


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


checker = module('audited_separator_checker', REVIEW / 'check_candidate.py')
legacy = module('sealed_separator_replay', RUN / 'replay.py')
require, read, sha, safe = checker.require, checker.load, legacy.sha, legacy.safe


def public_input(request):
    return request['public_context']['reviewed_work']['work_unit']['operad_slots']['slot_m1_layer0_ambient_carrier']['public_input']


def repair_binding(first, repaired, old, new):
    for key in ('original_target', 'reviewed_work'):
        require(first['public_context'][key] == repaired['public_context'][key], 'binding:repair_problem_changed')
    ignored = {'task_id', 'stage_id', 'attempt_id', 'input_sha256'}
    require({k: v for k, v in old.items() if k not in ignored} ==
            {k: v for k, v in new.items() if k not in ignored}, 'binding:repair_numbers_changed')


def lean_reports(output):
    require('sorryAx' not in output and 'error:' not in output, 'native:unproved_anchor')
    rows = re.findall(r"'QuantumMechanics\.BellSeparatorExtension\.([^']+)' depends on axioms:\s*\[([^\]]*)\]", output)
    require(len(rows) == len(ANCHORS) and {n for n, _ in rows} == set(ANCHORS), 'native:axiom_report_coverage')
    for _, axioms in rows:
        require({x.strip() for x in axioms.split(',') if x.strip()} <= {'propext', 'Classical.choice', 'Quot.sound'}, 'native:unapproved_axiom')


def command_receipts(receipts, commands, cwd, root):
    require(type(receipts) is list and len(receipts) == len(commands) and bool(receipts), 'native:receipt_coverage')
    for receipt, command in zip(receipts, commands):
        require(receipt.get('argv') == command and Path(receipt.get('cwd', '')).resolve() == cwd.resolve(), 'native:wrong_command')
        require(type(receipt.get('exit_code')) is int and receipt['exit_code'] == 0, 'native:failed_command')
        for field in ('stdout', 'stderr'):
            require(type(receipt.get(field)) is str and safe(root, receipt[field]).is_file(), 'native:missing_log')


def controls(control, candidate, public, saved):
    answers = {a['id']: a for a in candidate['cases']}
    inputs = {p['id']: p for p in public}
    require(checker.check_case(control['case'], control['answer']) == 'blocked', 'control:obstruction')
    e = [p[0] - p[1] - p[2] + p[3] for p in checker.valid_pairs(control['case']['pairs'])]
    standard = e[0] + e[1] + e[2] - e[3]
    a = control['answer']; masks = [1, 2, 4, 7, 8, 11, 13, 14]
    violated = Q(a['facets'][masks.index(a['violating_mask'])])
    require(Q(control['standard_CHSH_value']) == standard and abs(standard) <= 2 and
            Q(control['violated_facet_value']) == violated and violated > 2, 'control:summary_not_derived')
    uniform = answers[saved['valid_control']]
    checker.check_case(inputs[uniform['id']], uniform)
    left, right = [list(map(Q, t)) for t in uniform['triples']]
    naive = sum(left[(m & 3) + 4 * ((m >> 2) & 1)] * right[(m & 3) + 4 * ((m >> 3) & 1)] for m in range(16))
    require(Q(saved['naive_unconditional_product_mass']) == naive and naive != 1 and
            Q(saved['correct_glued_mass']) == sum(map(Q, uniform['weights'])) == 1, 'control:mass')
    zero_cases = sum(a['status'] == 'extended' and any(Q(a['triples'][0][s]) + Q(a['triples'][0][s+4]) == 0 for s in range(4)) for a in candidate['cases'])
    require(zero_cases == saved['zero_separator_cases_checked'], 'control:zero_count')
    try:
        checker.valid_pairs(saved['invalid_compatible_premise']['pairs'])
    except ValueError as error:
        require(str(error) == saved['invalid_compatible_premise']['rejection'], 'control:invalid_input_reason')
    else:
        raise ValueError('control:invalid_input_accepted')
    ts = [list(map(Q, saved['mismatched_triples'][k])) for k in ('left', 'right')]
    require(all(len(t) == 8 and min(t) >= 0 and sum(t) == 1 for t in ts), 'control:mismatch_premise')
    require([ts[0][s]+ts[0][s+4] for s in range(4)] != [ts[1][s]+ts[1][s+4] for s in range(4)], 'control:mismatch_missing')
    c = saved['nonstandard_facet_control']; old = answers[c['case']]
    checker.check_case(inputs[c['case']], old)
    facets = list(map(Q, old['facets']))
    require(Q(c['standard_facet_value']) == facets[4] == -4 and
            Q(c['actual_violated_value']) == facets[masks.index(c['violating_mask'])] == 4, 'control:one_sided_summary')
    return {'zero_separator_cases': zero_cases, 'naive_product_mass': str(naive), 'two_sided_control_standard': str(standard), 'other_facet': str(violated)}


def coverage(public, answers):
    """Independently enumerate nonnegative row tables and join shared unaries.

    This does not use cases.py or the solver's marginal-parameter loop.
    """
    per_d = {}
    rational_keys = []
    for d in (1, 2, 3, 4):
        rows = [(a, b, c, d-a-b-c) for a in range(d+1) for b in range(d-a+1) for c in range(d-a-b+1)]
        by_a, by_b, by_ab = defaultdict(list), defaultdict(list), defaultdict(list)
        for row in rows:
            a, b = row[2]+row[3], row[1]+row[3]
            by_a[a].append(row); by_b[b].append(row); by_ab[a, b].append(row)
        expected = set()
        for p00 in rows:
            for p01 in by_a[p00[2]+p00[3]]:
                for p10 in by_b[p00[1]+p00[3]]:
                    for p11 in by_ab[p10[2]+p10[3], p01[1]+p01[3]]:
                        expected.add((p00, p01, p10, p11))
        observed = []
        counts = Counter()
        for case, answer in zip(public, answers):
            if not case['id'].startswith('grid_' + str(d) + '_'):
                continue
            p = checker.valid_pairs(case['pairs'])
            ints = tuple(tuple(q*d for q in row) for row in p)
            require(all(q.denominator == 1 for row in ints for q in row), 'coverage:wrong_denominator')
            params = (d, ints[0][2]+ints[0][3], ints[2][2]+ints[2][3], ints[0][1]+ints[0][3], ints[1][1]+ints[1][3], *(row[3] for row in ints))
            require(case['id'] == 'grid_' + '_'.join(str(int(x)) for x in params), 'coverage:case_id')
            observed.append(ints); counts[answer['status']] += 1
            rational_keys.append(tuple(tuple(row) for row in p))
        require(len(observed) == len(set(observed)) and set(observed) == expected, 'coverage:grid_not_complete')
        per_d[str(d)] = {'inputs': len(observed), **dict(counts)}
    extra = [p for p in public if not p['id'].startswith('grid_')]
    require(len(extra) == 1 and extra[0]['id'] == 'arbitrary_precision_marginals', 'coverage:extra_inputs')
    # Reconstruct this control from its stated integer weights, independently.
    weights = [Q(i+1) for i in range(16)]; weights[0] += 10**80+7
    total = sum(weights); weights = [w/total for w in weights]
    p = [[[sum(weights[m] for m in range(16) if 2*((m >> x)&1)+((m >> (2+y))&1) == cell) for cell in range(4)] for y in range(2)] for x in range(2)]
    require([row for setting in p for row in setting] == checker.valid_pairs(extra[0]['pairs']), 'coverage:precision_control')
    rational_keys.append(tuple(tuple(map(Q, row)) for row in extra[0]['pairs']))
    return {'per_denominator': per_d, 'inputs': len(public), 'distinct_rational_pair_data': len(set(rational_keys)), 'repeated_representations': len(public)-len(set(rational_keys))}


def cross_language(output, answers):
    lines = output.splitlines()
    require(len(lines) == len(answers), 'native:replay_count')
    for line, answer in zip(lines, answers):
        row = line.split('\t')
        values = answer['lower'] + answer['upper'] + answer['facets']
        values += [answer['separator']] + answer['triples'][0] + answer['triples'][1] + answer['weights'] if answer['status'] == 'extended' else [str(answer['violating_mask'])]
        require(row[:2] == [answer['id'], answer['status']] and row[2:] == values, 'native:cross_language_difference')
    return len(lines)


def review_inventory(root, manifest):
    rows = manifest['artifacts']
    require(type(rows) is list and bool(rows), 'custody:empty_manifest')
    names = [r['path'] for r in rows]
    require(len(names) == len(set(names)), 'custody:duplicate_path')
    for row in rows:
        require(sha(safe(root, row['path'])) == row['sha256'], 'custody:artifact:' + row['path'])
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p != root/'review_manifest.json'}
    require(actual == set(names), 'custody:inventory_changed')
    return len(rows)


def verify(working_sources=False):
    manifest = read(REVIEW / 'review_manifest.json')
    inventory = review_inventory(REVIEW, manifest)
    expected_sources = {p['path'] for p in read(RUN / 'manifest.json')['working_sources']} | {'code/python/src/qm/bell_joint_extension.py', 'code/rust/src/finite_probability/bell_joint_extension.rs', 'dag/results/FQ-BELL-CLASSICAL-JOINT-EXTENSION/README.md'}
    require(type(manifest['source_pins']) is list and len(manifest['source_pins']) == len(expected_sources) and {p['path'] for p in manifest['source_pins']} == expected_sources, 'custody:source_pin_coverage')
    for pin in manifest['source_pins']:
        require(sha(safe(REVIEW, pin['snapshot'])) == pin['sha256'], 'custody:source_snapshot')
        if working_sources:
            require(sha(safe(ROOT, pin['path'])) == pin['sha256'], 'custody:working_source:' + pin['path'])
    # Original replay checks immutable evidence only; new source pins are above.
    captured = io.StringIO()
    old_argv = sys.argv
    try:
        sys.argv = [str(RUN / 'replay.py')]
        with contextlib.redirect_stdout(captured):
            legacy.main()
    finally:
        sys.argv = old_argv
    sealed_summary = json.loads(captured.getvalue())
    first, repaired = read(RUN / 'p1/request.json'), read(RUN / 'p3/request.json')
    old, candidate = read(RUN / 'p1/candidate.json'), read(RUN / 'p3/candidate.json')
    repair_binding(first, repaired, old, candidate)
    checked = [checker.check(RUN / stage / 'request.json', RUN / stage / 'candidate.json') for stage in ('p1', 'p3')]
    for folder, stage in (('p0', 'P0_MINE_OPERAD'), ('p1', 'P1_DERIVE'), ('p3', 'P3_REPAIR'), ('p4', 'P4_CHALLENGE')):
        packet = read(RUN / folder / 'request.json')
        require(packet['task_id'] == TASK and packet['stage_id'] == stage and packet['attempt_id'] == folder, 'binding:stage_identity')
    for folder in ('p0', 'p1', 'p2', 'p3', 'p2_after_repair', 'p4', 'p5'):
        request, submission, host = [read(RUN / folder / name) for name in ('request.json', 'candidate.json', 'host_check.json')]
        for key in ('task_id', 'stage_id', 'attempt_id', 'input_sha256'):
            require(request[key] == host[key], 'binding:host_checkpoint')
            if key in submission:
                require(request[key] == submission[key], 'binding:submitted_checkpoint')
        if folder in ('p2', 'p2_after_repair'):
            previous = 'p1' if folder == 'p2' else 'p3'
            require(submission['candidate_sha256'] == host['candidate_sha256'] == request['input_sha256'] == sha(RUN / previous / 'candidate.json'), 'binding:host_candidate')
        elif 'candidate_sha256' in host:
            require(host['candidate_sha256'] == sha(RUN / folder / 'candidate.json'), 'binding:checkpoint_candidate')
    p5req, p5, p5host = [read(RUN / 'p5' / name) for name in ('request.json', 'candidate.json', 'host_check.json')]
    for key in ('task_id', 'stage_id', 'attempt_id', 'input_sha256'):
        require(p5req[key] == p5[key] == p5host[key], 'binding:final_record')
    require(p5host['candidate_sha256'] == sha(RUN / 'p5/candidate.json'), 'binding:final_candidate')
    public = public_input(repaired)['cases']
    cov = coverage(public, candidate['cases'])
    ctrl = controls(read(RUN / 'p4/two_sided_chsh_control.json'), candidate, public, read(RUN / 'p4/host_check.json')['predicate_results']['controls'])
    plan = read(REVIEW / 'validation_plan.json')
    for kind, record in plan.items():
        # Timings are metadata; mathematical certificates still use the strict
        # no-JSON-float loader. Decimal preserves receipt timing bytes exactly.
        receipts = json.loads((REVIEW / 'validation' / (kind + '_receipt.json')).read_bytes(), object_pairs_hook=checker._object, parse_float=Decimal, parse_constant=checker._nonexact)
        command_receipts(receipts, record['commands'], safe(ROOT, record['cwd']) if record['cwd'] != '.' else ROOT, REVIEW)
        for receipt in receipts:
            require(receipt.get('stdin') == record.get('stdin'), 'native:stdin_binding')
        if 'stdin' in record:
            require(sha(safe(ROOT, record['stdin']['path'])) == record['stdin']['sha256'], 'native:stdin_digest')
    lean_reports((REVIEW / 'validation/logs/lean_4.stdout.log').read_text())
    require('version 4.33.1' in (REVIEW / 'validation/logs/lean_0.stdout.log').read_text(), 'native:Lean_version')
    n = cross_language((REVIEW / 'validation/logs/rust_replay_0.stdout.log').read_text(), candidate['cases'])
    python_replay = read(REVIEW / 'validation/python_replay.json')
    require(python_replay == {'cases_checked': n, 'counts': checked[1]['counts'], 'mode': 'fresh native Python; complete certificates compared'}, 'native:Python_replay')
    for kind, expected in (('python', 10), ('rust', 6), ('protocol', 12), ('guards', manifest['guard_test_count']), ('guards_optimized', manifest['guard_test_count'])):
        stdout = (REVIEW / ('validation/logs/' + kind + '_0.stdout.log')).read_text()
        stderr = (REVIEW / ('validation/logs/' + kind + '_0.stderr.log')).read_text()
        pattern = r'test result: ok\. (\d+) passed; 0 failed' if kind == 'rust' else r'Ran (\d+) tests[\s\S]*\bOK\s*$'
        match = re.search(pattern, stdout if kind == 'rust' else stderr)
        require(match is not None and int(match.group(1)) == expected, 'native:test_summary:' + kind)
    structure = read(REVIEW / 'validation/structure.json')
    require(structure['prompts'] == structure['collections'] == 177 and structure['errors'] == [], 'native:corpus_structure')
    result = {'review_artifacts': inventory, 'sealed_run_artifacts': sealed_summary['artifacts_checked'], 'counts': checked[1]['counts'], 'coverage': cov, 'controls': ctrl, 'fresh_cross_language_cases': n, 'kernel_anchors': len(ANCHORS), 'guard_tests': manifest['guard_test_count'], 'working_sources_checked': working_sources, 'claim_boundary': 'Integer separator theorem and finite exact native certificates; full formal rational Fine converse remains open.'}
    require(read(REVIEW / 'audit_results.json') == {k: v for k, v in result.items() if k not in ('review_artifacts', 'working_sources_checked')}, 'audit:summary_changed')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--working-sources', action='store_true')
    print(json.dumps(verify(parser.parse_args().working_sources), indent=2))
