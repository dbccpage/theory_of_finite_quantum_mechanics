"""Strict raw-byte Bell certificate check; compilation is a separate host gate.

This checks exact finite samples and public scope labels. Matching anchor names
does not prove that any declaration exists or that a theorem was compiled.
"""
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def _object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'G1_SCHEMA:duplicate_key:' + key)
        result[key] = value
    return result


def _nonexact(value):
    raise ValueError('G1_SCHEMA:nonexact_json_number')


def read_json(path, exact_numbers=False):
    try:
        return json.loads(Path(path).read_bytes(), object_pairs_hook=_object,
                          parse_float=_nonexact if exact_numbers else float, parse_constant=_nonexact)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValueError('G1_SCHEMA:invalid_json') from error


def context_digest(context):
    data = json.dumps(context, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()
    return hashlib.sha256(data).hexdigest()


def exact(value):
    require(type(value) is str, 'G1_SCHEMA:rational_not_string')
    try:
        result = Q(value)
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError('G1_SCHEMA:invalid_rational') from error
    require(str(result) == value, 'G1_SCHEMA:noncanonical_rational')
    return result


def check(request_path, candidate_path):
    request = read_json(request_path, exact_numbers=True)
    require(type(request) is dict and 'public_context' in request, 'G1_SCHEMA:request_shape')
    require(request.get('input_sha256') == context_digest(request['public_context']),
            'G1_SCHEMA:public_context_digest')
    candidate = read_json(candidate_path, exact_numbers=True)
    fields = {'schema_id', 'task_id', 'stage_id', 'attempt_id', 'input_sha256', 'samples', 'anchors', 'scope'}
    require(type(candidate) is dict and set(candidate) == fields, 'G1_SCHEMA:fields')
    require(candidate['schema_id'] == 'finite-qm.bell-operad-certificate.v1', 'G1_SCHEMA:schema_id')
    for key in ('task_id', 'stage_id', 'attempt_id', 'input_sha256'):
        require(type(candidate[key]) is str and candidate[key] == request.get(key), 'G1_SCHEMA:binding')
    require(candidate['task_id'] == 'FQ-BELL-CLASSICAL-JOINT-EXTENSION' and candidate['stage_id'] == 'P1_DERIVE',
            'G1_SCHEMA:task_and_stage')
    try:
        public = request['public_context']['reviewed_work']['work_unit']['operad_slots']['slot_m1_layer0_ambient_carrier']['public_input']
        cases = public['cases']
    except (KeyError, TypeError) as error:
        raise ValueError('G1_SCHEMA:public_contract') from error
    require(type(cases) is list and bool(cases), 'G1_SCHEMA:empty_cases')
    require(all(type(x) is dict and set(x) == {'id', 'weights'} and type(x['id']) is str for x in cases),
            'G1_SCHEMA:public_cases')
    ids = [x['id'] for x in cases]
    require(len(ids) == len(set(ids)), 'G1_SCHEMA:duplicate_case_id')
    samples = candidate['samples']
    require(type(samples) is list and all(type(x) is dict for x in samples), 'G1_SCHEMA:samples')
    require([x.get('id') for x in samples] == ids, 'G1_SCHEMA:sample_binding')
    sample_fields = {'id', 'weights', 'correlators', 'chsh', 'positive_score_mass', 'negative_score_mass', 'lower_slack', 'upper_slack'}
    products = [[(-1 if not (mask >> i) & 1 else 1) * (-1 if not (mask >> j) & 1 else 1)
                 for i, j in ((0, 2), (0, 3), (1, 2), (1, 3))] for mask in range(16)]
    scores = [row[0] + row[1] + row[2] - row[3] for row in products]
    require(set(scores) == {-2, 2}, 'checker_internal:score_partition')
    for given, instance in zip(samples, cases):
        require(set(given) == sample_fields, 'G1_SCHEMA:sample_fields')
        require(type(given['weights']) is list and given['weights'] == instance['weights'], 'G1_SCHEMA:changed_public_law')
        weights = list(map(exact, given['weights']))
        require(len(weights) == 16 and min(weights) >= 0 and sum(weights) == 1, 'G3_WITNESS:law')
        require(type(given['correlators']) is list and len(given['correlators']) == 4, 'G1_SCHEMA:correlator_shape')
        correlations = [sum((p*row[k] for p, row in zip(weights, products)), Q(0)) for k in range(4)]
        plus = sum((p for p, score in zip(weights, scores) if score == 2), Q(0))
        minus = sum((p for p, score in zip(weights, scores) if score == -2), Q(0))
        s = correlations[0] + correlations[1] + correlations[2] - correlations[3]
        scalars = {'chsh': s, 'positive_score_mass': plus, 'negative_score_mass': minus, 'lower_slack': 2+s, 'upper_slack': 2-s}
        require(list(map(exact, given['correlators'])) == correlations and all(exact(given[k]) == v for k, v in scalars.items()),
                'G3_WITNESS:false_certificate')
        require(plus+minus == 1 and s == 2*(plus-minus) and 2+s == 4*plus and 2-s == 4*minus,
                'G3_WITNESS:partition_relation')
    require(candidate['scope'] == public.get('scope') and candidate['anchors'] == public.get('required_anchors'),
            'G5_SCOPE:public_label_binding')
    return {'candidate_sha256': hashlib.sha256(Path(candidate_path).read_bytes()).hexdigest(),
            'checked_samples': len(cases), 'domain_predicates': 'all certificate fields independently recomputed',
            'scope_gate': 'public labels match only; source existence, compilation and theorem scope require separate host checks'}


if __name__ == '__main__':
    print(json.dumps(check(*sys.argv[1:]), indent=2))
