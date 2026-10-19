def lines(data):return ['gauge'+'\t'+'\t'.join(r['output']) for r in data['records']]
