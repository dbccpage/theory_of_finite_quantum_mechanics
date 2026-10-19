def lines(data):return ['histories'+'\t'+'\t'.join(r['output']) for r in data['records']]
