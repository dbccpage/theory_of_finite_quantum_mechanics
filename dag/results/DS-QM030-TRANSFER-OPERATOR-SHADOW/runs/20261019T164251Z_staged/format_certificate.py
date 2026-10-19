def lines(data):return ['transfer'+'\t'+'\t'.join(r['output']) for r in data['records']]
