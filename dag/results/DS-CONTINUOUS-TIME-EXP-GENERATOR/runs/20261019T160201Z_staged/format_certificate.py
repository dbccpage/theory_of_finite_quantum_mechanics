def lines(data):return ['time'+'\t'+'\t'.join(r['output']) for r in data['records']]
