def lines(data):return ['supply'+'\t'+'\t'.join(r['output']) for r in data['records']]
