"""Independent, stdlib-only check of a staged Bell candidate's ORIGINAL bytes.

Does not import either producer. Lean compilation is a separate required gate.
"""
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
import sys


def exact(value):
    if type(value) is not str:
        raise ValueError('rational_not_string')
    result = Q(value)
    if str(result) != value:
        raise ValueError('noncanonical_rational')
    return result


def check(request_path, candidate_path):
    request = json.loads(Path(request_path).read_bytes())
    original = Path(candidate_path).read_bytes()
    candidate = json.loads(original)
    required = {'schema_id', 'task_id', 'stage_id', 'attempt_id', 'input_sha256', 'samples', 'anchors', 'scope'}
    if set(candidate) != required or candidate['schema_id'] != 'finite-qm.bell-operad-certificate.v1':
        raise ValueError('G1_SCHEMA:fields')
    for key in ('task_id', 'stage_id', 'attempt_id', 'input_sha256'):
        if candidate[key] != request[key]:
            raise ValueError('G1_SCHEMA:binding')
    public = request['public_context']['reviewed_work']['work_unit']['operad_slots']['slot_m1_layer0_ambient_carrier']['public_input']
    cases = public['cases']
    if [x['id'] for x in candidate['samples']] != [x['id'] for x in cases]:
        raise ValueError('G1_SCHEMA:sample_binding')
    for given, instance in zip(candidate['samples'], cases):
        if set(given) != {'id', 'weights', 'correlators', 'chsh', 'positive_score_mass', 'negative_score_mass', 'lower_slack', 'upper_slack'}:
            raise ValueError('G1_SCHEMA:sample_fields')
        if given['weights'] != instance['weights']:
            raise ValueError('G1_SCHEMA:changed_public_law')
        weights = list(map(exact, given['weights']))
        if len(weights) != 16 or min(weights) < 0 or sum(weights) != 1:
            raise ValueError('G3_WITNESS:law')
        # Direct products, no producer's factored CHSH or shared helper.
        products = [[(-1 if not (mask >> i) & 1 else 1) * (-1 if not (mask >> j) & 1 else 1)
                     for i, j in ((0, 2), (0, 3), (1, 2), (1, 3))] for mask in range(16)]
        correlations = [sum((p * row[k] for p, row in zip(weights, products)), Q(0)) for k in range(4)]
        scores = [row[0] + row[1] + row[2] - row[3] for row in products]
        if any(s not in (-2, 2) for s in scores):
            raise ValueError('checker_internal_score_error')
        plus = sum((p for p, s in zip(weights, scores) if s == 2), Q(0))
        minus = sum((p for p, s in zip(weights, scores) if s == -2), Q(0))
        s = correlations[0] + correlations[1] + correlations[2] - correlations[3]
        scalars = {'chsh': s, 'positive_score_mass': plus, 'negative_score_mass': minus,
                   'lower_slack': 2 + s, 'upper_slack': 2 - s}
        if list(map(exact, given['correlators'])) != correlations or any(exact(given[k]) != v for k, v in scalars.items()):
            raise ValueError('G3_WITNESS:false_certificate')
        if plus + minus != 1 or s != 2 * (plus - minus) or 2 + s != 4 * plus or 2 - s != 4 * minus:
            raise ValueError('G3_WITNESS:partition_relation')
    if candidate['scope'] != public['scope'] or candidate['anchors'] != public['required_anchors']:
        raise ValueError('G5_SCOPE:claim_or_anchor_binding')
    return {'candidate_sha256': hashlib.sha256(original).hexdigest(), 'checked_samples': len(cases),
            'domain_predicates': 'all certificate fields independently recomputed; public laws and scope unchanged'}


if __name__ == '__main__':
    print(json.dumps(check(*sys.argv[1:]), indent=2))
