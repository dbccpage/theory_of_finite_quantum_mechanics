def lines(data):return ['defect'+'\t'+'\t'.join(r['output']) for r in data['records']]
