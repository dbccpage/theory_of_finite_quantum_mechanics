def _b(x):
    return str(int(x))


def _list(xs):
    return ','.join(str(x) for x in xs) or '-'


def lines(data):
    out = []
    for r in data['records']:
        out.append('\t'.join(['carrier'] + [str(x) for x in r['input']] + [
            _list(r['shapes']), str(r['base_total']), _list(r['stage_shape_counts']), _list(r['table_prefix']),
            _list(int(x) for x in r['table_matches']), _list(r['table_equal_total_stages']),
            str(r['old_image_checked']), str(r['old_image_failures']), _list(r['lift_image_sizes']),
            str(r['universe_size']), str(r['non_base_presentations']), str(r['unrestricted_image_size']),
            str(r['unrestricted_fibre_over_ground']), _b(r['unrestricted_injective']),
            _b(r['refusal_round_trip_accepts_ground']), _b(r['refusal_round_trip_returns_token']),
            str(r['stage_mismatch_refused']), str(r['long_body_refused']), _list(r['cumulative_stage_counts']),
            _list(int(x) for x in r['cumulative_matches'])]))
    return out
