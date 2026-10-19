def lines(data):return ['registry'+'\t'+'\t'.join(r['output']) for r in data['records']]
