"""Semantic near misses for the PG-DEMAND-ACCOUNTING certificate.

Each mutant is a well-formed record a reviewer could believe, and each breaks one premise of the node.
"""


def _demand(data, u):
    return next(r for r in data['records'] if r['kind'] == 'demand' and r['u'] == u)


def _seq(data, seq):
    return next(r for r in data['records'] if r['kind'] == 'sequence' and r['seq'] == seq)


def _listreg(data, a, maxlen):
    return next(r for r in data['records'] if r['kind'] == 'listreg' and r['input'] == [a, maxlen])


def semantic_mutants(data, profile):
    def subset_hypothesis_dropped(d):
        r = _demand(d, 3)
        r['classes'][1][1] = r['classes'][1][0]

    def disjointness_hypothesis_dropped(d):
        r = _demand(d, 3)
        r['classes'][2][1] = r['classes'][2][0]

    def natural_subtraction_detects_violation(d):
        r = _demand(d, 3)
        r['classes'][1][2] = 0

    def accidental_agreement_denied(d):
        r = _demand(d, 4)
        r['classes'][3][1] = 0

    def births_on_discharged_read_as_violation(d):
        r = _demand(d, 3)
        r['classes'][0] = [4 ** 3, 4 ** 3, 4 ** 3]

    def survivor_sequence_read_as_law(d):
        _seq(d, [0, 1, 1, 1, 0, 1, 1])['underdetermined'] = False

    def split_forced_by_counts(d):
        r = _seq(d, [0, 1, 1, 1, 0, 1, 1])
        r['decompositions'] = [1] * len(r['decompositions'])

    def list_length_identity_needs_disjointness(d):
        r = _listreg(d, 2, 2)
        r['identity_holds'] = r['total'] - (r['nodup_inputs'] - r['disjoint_inputs'])

    def duplicate_free_register_without_disjointness(d):
        _listreg(d, 2, 2)['nodup_when_overlap'] = 1

    return [
        {'id': 'subset_hypothesis_dropped', 'rationale': 'Claim the integer identity s-d+b also holds for every triple with D not inside W (u=3); it holds for none of them.', 'mutate': subset_hypothesis_dropped},
        {'id': 'disjointness_hypothesis_dropped', 'rationale': 'Claim the identity holds for every triple whose births overlap the survivors (u=3); it holds for none of them.', 'mutate': disjointness_hypothesis_dropped},
        {'id': 'natural_subtraction_detects_violation', 'rationale': 'Claim the truncated natural-number identity never holds when D is not inside W; truncation makes it hold for 152 of the 218 such triples at u=3.', 'mutate': natural_subtraction_detects_violation},
        {'id': 'accidental_agreement_denied', 'rationale': 'Claim the identity cannot hold when both hypotheses fail (u=4); an excess of D outside W can cancel an overlap exactly.', 'mutate': accidental_agreement_denied},
        {'id': 'births_on_discharged_read_as_violation', 'rationale': 'Take disjointness against W or D instead of W minus D, so births coinciding with discharged elements count as a violation (4^3 instead of 5^3 admissible triples at u=3); the source hypothesis ranges over the survivors only.', 'mutate': births_on_discharged_read_as_violation},
        {'id': 'survivor_sequence_read_as_law', 'rationale': 'Claim the displayed survivor sequence (0,1,1,1,0,1,1) leaves no freedom in the discharged/born split; three of its six steps admit two splits.', 'mutate': survivor_sequence_read_as_law},
        {'id': 'split_forced_by_counts', 'rationale': 'Claim exactly one (d,b) split per step of the displayed sequence, so the counts determine the accounting.', 'mutate': split_forced_by_counts},
        {'id': 'list_length_identity_needs_disjointness', 'rationale': 'Multiset/list register: claim the length identity fails when births overlap the survivors; the list register counts multiplicity so the identity holds for all 196 triples at (2,2).', 'mutate': list_length_identity_needs_disjointness},
        {'id': 'duplicate_free_register_without_disjointness', 'rationale': 'Claim a duplicate-free register can result from overlapping births; for duplicate-free inputs the register is duplicate-free exactly when the births avoid the survivors.', 'mutate': duplicate_free_register_without_disjointness},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The cases are a set; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
