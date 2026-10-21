ORDER = ('traces', 'refused', 'rooted_ok', 'supply_deletion_changes', 'supply_only_traces', 'supply_only_moved', 'moved',
         'reachable_states', 'with_coproduct', 'inscribed_no_coproduct', 'inscribed_with_coproduct', 'uninscribed_with_coproduct',
         'rooted_with_coproduct', 'rooted_without_coproduct', 'root_traces', 'root_traces_with_coproduct',
         'mention_prefix_diff', 'rival_mention_prefix_diff', 'rival_supply_only_moved',
         'rooted_later_supply_changes', 'root_omission_visible', 'rooted_refuses_unrooted_accepted')


def lines(data):
    out = []
    for r in data['records']:
        fields = ['inert', str(r['input'][0])] + [str(r[key]) for key in ORDER]
        out.append('\t'.join(fields))
    return out
