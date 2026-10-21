"""Semantic near misses for the history-report criterion certificate (PG-HISTORY-REPORT-CRITERION).

Each mutant is a well-formed record a reviewer could believe; each breaks one premise of the node or is a
counterexample to the unpaid bridge named in does_not_support.
"""


def _record(data, h, v, s):
    return next(r for r in data['records'] if r['input'] == [h, v, s])


def semantic_mutants(data, profile):
    def every_question_factors(d):
        r = _record(d, 3, 3, 2)
        r['factoring'] = r['pairs']
        r['fiber_constant'] = r['pairs']

    def only_injective_reports_factor(d):
        r = _record(d, 3, 3, 2)
        r['factoring'] = 48
        r['fiber_constant'] = 48

    def extension_unique_off_image(d):
        r = _record(d, 4, 3, 2)
        r['nonunique_off_image'] = 0
        r['extensions_total'] = r['factoring']

    def surjective_report_still_has_freedom(d):
        _record(d, 3, 3, 2)['surjective_nonunique'] = 6

    def image_confused_with_codomain(d):
        _record(d, 3, 3, 2)['image_hist'] = [[3, 27]]

    def criterion_fails_on_one_pair(d):
        r = _record(d, 2, 2, 2)
        r['mismatch'] = 1
        r['factoring'] = 11

    def two_factors_on_the_image(d):
        _record(d, 2, 3, 2)['max_factor_multiplicity'] = 2

    def empty_histories_do_not_factor(d):
        r = _record(d, 0, 2, 2)
        r['factoring'] = 0
        r['fiber_constant'] = 0

    def coarser_kernel_than_the_report(d):
        r = _record(d, 3, 3, 2)
        r['factoring'] = 54
        r['fiber_constant'] = 54

    def empty_answers_extend_uniquely(d):
        r = _record(d, 0, 2, 0)
        r['extensions_total'] = 1

    return [
        {'id': 'every_question_factors', 'rationale': 'Drop the fiber-constancy hypothesis: claim every question over three histories factors through the image of a report.', 'mutate': every_question_factors},
        {'id': 'only_injective_reports_factor', 'rationale': 'Confuse factoring through the image with the report being injective: only 6 injective reports, 48 pairs.', 'mutate': only_injective_reports_factor},
        {'id': 'extension_unique_off_image', 'rationale': 'Read uniqueness on the image as uniqueness of the extension to all reports; unreported points leave s^(v-k) free values.', 'mutate': extension_unique_off_image},
        {'id': 'surjective_report_still_has_freedom', 'rationale': 'Claim off-image non-uniqueness also when the report is surjective, where there is no off-image point.', 'mutate': surjective_report_still_has_freedom},
        {'id': 'image_confused_with_codomain', 'rationale': 'Count every report as having full image, ignoring that the image of a report can be smaller than the codomain.', 'mutate': image_confused_with_codomain},
        {'id': 'criterion_fails_on_one_pair', 'rationale': 'Claim one question over two histories factors without being fiber constant (or conversely); the criterion is an iff.', 'mutate': criterion_fails_on_one_pair},
        {'id': 'two_factors_on_the_image', 'rationale': 'Claim a question has two distinct factorizations through the image; uniqueness on the image is a theorem.', 'mutate': two_factors_on_the_image},
        {'id': 'empty_histories_do_not_factor', 'rationale': 'Treat the empty history set as a refusal case; the empty question factors through the empty image, vacuously.', 'mutate': empty_histories_do_not_factor},
        {'id': 'coarser_kernel_than_the_report', 'rationale': 'Count answers constant on the fibers of the constant report (a coarser equivalence than the own kernel of each report): 27 reports times 2 answers, instead of the own fibers of each report.', 'mutate': coarser_kernel_than_the_report},
        {'id': 'empty_answers_extend_uniquely', 'rationale': 'Claim the empty question over the empty history set extends to the two-element report type in one way; with no answer values there are none (s^v = 0), although it factors through the empty image.', 'mutate': empty_answers_extend_uniquely},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The cases are a set; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
