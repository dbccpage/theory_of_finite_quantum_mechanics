def lines(data):return ['proxy'+'\t'+'\t'.join(r['output']) for r in data['records']]
