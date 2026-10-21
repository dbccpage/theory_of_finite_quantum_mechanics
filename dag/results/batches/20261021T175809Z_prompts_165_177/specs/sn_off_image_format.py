FIELDS = ['universe', 'accepted', 'refused', 'image_size', 'lift_collisions', 'iff_violations', 'payload_failures', 'roundtrip_holds',
          'roundtrip_fails', 'stage_mismatch_refused', 'long_body_refused', 'lax_law_holds', 'lax_refused']
TOY_FIELDS = ['points', 'on_image', 'refused', 'law_failures', 'sound_failures']


def lines(data):
    out = []
    for r in data['records']:
        names = FIELDS if r['kind'] == 'offimage' else TOY_FIELDS
        out.append('\t'.join([r['kind']] + [str(x) for x in r['input']] + [str(r[f]) for f in names]))
    return out
