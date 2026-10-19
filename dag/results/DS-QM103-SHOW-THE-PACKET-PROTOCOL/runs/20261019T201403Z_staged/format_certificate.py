def lines(data):return ['packet'+'\t'+'\t'.join(r['output']) for r in data['records']]
