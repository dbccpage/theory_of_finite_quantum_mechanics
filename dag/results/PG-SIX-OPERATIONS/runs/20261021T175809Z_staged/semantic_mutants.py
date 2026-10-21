"""Semantic near misses for PG-SIX-OPERATIONS. Each is a well-formed record a reviewer might believe."""


def _rec(data, kind, **match):
    return next(r for r in data['records'] if r['kind'] == kind and all(r.get(k) == v for k, v in match.items()))


def semantic_mutants(data, profile):
    def supply_also_admits(d):
        _rec(d, 'footprint', op='supply')['new_item_fields'] = '010100'

    def readings_collapse_in_six_ops(d):
        r = _rec(d, 'reading', conflation='supply_includes_admit')
        r['six_F_admitted'] = []
        r['six_separated'] = False

    def repeated_admit_counts_as_change(d):
        r = _rec(d, 'trace', init_mask=1)
        r['changed'] = r['with_admit']

    def designate_retain_conflation_admits(d):
        r = _rec(d, 'conflation', name='designate_includes_retain')
        r['differing_fields'] = '000100'
        r['admitted_differs'] = True

    def retain_needs_no_admission(d):
        _rec(d, 'footprint', op='retain')['new_item_fields'] = '000010'

    def operate_writes_admitted(d):
        _rec(d, 'footprint', op='operate')['old_item_fields'] = '000101'

    def retain_equals_operate(d):
        r = _rec(d, 'pair', a='retain', b='operate')
        r['min_len'] = -1
        r['contexts'] = 0

    def mention_equals_supply(d):
        r = _rec(d, 'pair', a='mention', b='supply')
        r['min_len'] = -1
        r['contexts'] = 0

    def full_admission_never_changes(d):
        r = _rec(d, 'trace', init_mask=0)
        r['changed'] = 0
        r['with_new_admit'] = 0

    def admit_including_supply_collapses(d):
        r = _rec(d, 'reading', conflation='admit_includes_supply')
        r['conflated_L_admitted'] = [0]
        r['conflated_separated'] = False

    def operate_admission_not_visible(d):
        _rec(d, 'conflation', name='operate_includes_admit')['admitted_differs'] = False

    def designate_equals_admit(d):
        r = _rec(d, 'pair', a='designate', b='admit')
        r['min_len'] = -1
        r['contexts'] = 0

    return [
        {'id': 'admit_including_supply_collapses', 'rationale': 'Claim the readings also collapse when Admit additionally supplies; admitting a token that was supplied or not still separates the readings, because Reading L never admits.', 'mutate': admit_including_supply_collapses},
        {'id': 'operate_admission_not_visible', 'rationale': 'Claim a model in which Operate also admits leaves the admitted component alone; the admitted set then contains the operated item.', 'mutate': operate_admission_not_visible},
        {'id': 'designate_equals_admit', 'rationale': 'Declare Designate and Admit indistinguishable; they write different components (designated versus admitted).', 'mutate': designate_equals_admit},
        {'id': 'supply_also_admits', 'rationale': 'Read delivery of a payload as adoption: supply would then write the admitted component, the conflation the six-operation list forbids.', 'mutate': supply_also_admits},
        {'id': 'readings_collapse_in_six_ops', 'rationale': 'Claim Readings L and F end in the same admitted state even when Supply and Admit are kept distinct; they differ by exactly one Admit.', 'mutate': readings_collapse_in_six_ops},
        {'id': 'repeated_admit_counts_as_change', 'rationale': 'Take the source counter model (every Admit increments) for the set model: re-admitting an already admitted item changes nothing in the set.', 'mutate': repeated_admit_counts_as_change},
        {'id': 'designate_retain_conflation_admits', 'rationale': 'Claim that merging designation with retention touches the admitted component; it only turns an overwritable designation into a permanent retained item.', 'mutate': designate_retain_conflation_admits},
        {'id': 'retain_needs_no_admission', 'rationale': 'Let Retain succeed on an item that was never admitted; retaining preserves an ADMITTED object.', 'mutate': retain_needs_no_admission},
        {'id': 'operate_writes_admitted', 'rationale': 'Let Operate write the admitted component; its result stays in outputs until an explicit Admit.', 'mutate': operate_writes_admitted},
        {'id': 'retain_equals_operate', 'rationale': 'Declare Retain and Operate indistinguishable; they differ once an item is admitted (retained versus outputs).', 'mutate': retain_equals_operate},
        {'id': 'mention_equals_supply', 'rationale': 'Declare Mention and Supply indistinguishable; they write different components (mentioned versus supplied).', 'mutate': mention_equals_supply},
        {'id': 'admission_never_changes_state', 'rationale': 'Claim no trace from the empty state changes the admitted set although every trace with an Admit does.', 'mutate': full_admission_never_changes},
    ]


def semantic_controls(data, profile):
    def reverse_record_order(d):
        d['records'].reverse()

    return [{'id': 'reverse_record_order', 'rationale': 'The cases are a set; any order of the same records is the same certificate.', 'mutate': reverse_record_order}]
