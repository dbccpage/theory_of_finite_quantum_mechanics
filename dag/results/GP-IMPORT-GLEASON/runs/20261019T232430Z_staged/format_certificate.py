def lines(data):return ['gleason'+'\t'+'\t'.join(r['output']) for r in data['records']]
