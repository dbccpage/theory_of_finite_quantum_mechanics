def lines(data):return ['branch'+'\t'+'\t'.join(r['output']) for r in data['records']]
