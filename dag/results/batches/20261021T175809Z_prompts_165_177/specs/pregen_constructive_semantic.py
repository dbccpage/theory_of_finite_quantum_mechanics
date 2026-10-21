"""Semantic near misses for the listed-history summary certificate (PG-PREGEN-CONSTRUCTIVE-SUMMARY).

Each mutant is a well-formed record a reviewer could believe; each breaks one premise of the node or is a
counterexample to the unpaid bridge named in does_not_support.
"""


def _record(data, p, ell, v, s):
    return next(r for r in data['records'] if r['input'] == [p, ell, v, s])


def semantic_mutants(data, profile):
    def first_match_always_right(d):
        r = _record(d, 3, 3, 2, 2)
        r['recon_correct'] = r['triples']
        r['mismatch'] = r['triples'] - r['listed_fc']

    def partial_listing_implies_global(d):
        r = _record(d, 3, 3, 2, 2)
        r['partial_false_positive'] = 0

    def off_listing_never_wrong(d):
        r = _record(d, 3, 3, 2, 2)
        r['unlisted_correct'] += r['unlisted_wrong']
        r['unlisted_wrong'] = 0

    def repeats_ignored(d):
        r = _record(d, 3, 3, 2, 2)
        r['lists'] = 16

    def off_listing_never_refused(d):
        r = _record(d, 3, 3, 2, 2)
        r['unlisted_wrong'] += r['unlisted_refused']
        r['unlisted_refused'] = 0

    def criterion_fails_on_one_triple(d):
        r = _record(d, 2, 3, 2, 2)
        r['mismatch'] = 1
        r['recon_correct'] -= 1

    def complete_listing_disagrees(d):
        _record(d, 2, 3, 2, 2)['complete_mismatch'] = 2

    def full_length_listing_is_complete(d):
        _record(d, 3, 3, 2, 2)['complete_triples'] = 1728

    return [
        {'id': 'first_match_always_right', 'rationale': 'Drop the fiber-constancy hypothesis: claim first-match reconstruction returns every listed answer for every triple.', 'mutate': first_match_always_right},
        {'id': 'partial_listing_implies_global', 'rationale': 'Claim fiber constancy on an incomplete listing already gives global fiber constancy; unlisted histories can still disagree.', 'mutate': partial_listing_implies_global},
        {'id': 'off_listing_never_wrong', 'rationale': 'Claim that when reconstruction answers for an unlisted history it is right; an unlisted history of a listed report may have another answer.', 'mutate': off_listing_never_wrong},
        {'id': 'repeats_ignored', 'rationale': 'Count only duplicate-free listings (16) instead of all 40 lists of length at most 3; repeats are allowed listings.', 'mutate': repeats_ignored},
        {'id': 'off_listing_never_refused', 'rationale': 'Claim the reconstruction never refuses for an unlisted history; an unlisted history with an unreported report is refused with none.', 'mutate': off_listing_never_refused},
        {'id': 'criterion_fails_on_one_triple', 'rationale': 'Claim one triple is correctly reconstructed without being listed-fiber-constant; the listed criterion is an iff.', 'mutate': criterion_fails_on_one_triple},
        {'id': 'complete_listing_disagrees', 'rationale': 'Claim a complete listing can disagree with the global criterion of node 163; completeness makes the two coincide.', 'mutate': complete_listing_disagrees},
        {'id': 'full_length_listing_is_complete', 'rationale': 'Treat every listing of length 3 over 3 histories as complete (1728 triples); with repeats allowed only the 6 permutations are complete (384), which is the completeness hypothesis of listed_factor_exists.', 'mutate': full_length_listing_is_complete},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The cases are a set; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
