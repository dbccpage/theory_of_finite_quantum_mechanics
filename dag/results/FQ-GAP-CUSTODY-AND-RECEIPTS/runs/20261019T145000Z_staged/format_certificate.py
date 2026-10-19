def lines(data):return ['custody'+'\t'+'\t'.join(r['output']) for r in data['records']]
