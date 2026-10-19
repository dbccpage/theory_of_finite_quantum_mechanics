def lines(data):return ['channel'+'\t'+'\t'.join(r['output']) for r in data['records']]
