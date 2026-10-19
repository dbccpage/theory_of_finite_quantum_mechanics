def lines(data):return ['events'+'\t'+'\t'.join(r['output']) for r in data['records']]
