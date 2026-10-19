def lines(data):return ['chsh'+'\t'+'\t'.join(r['output']) for r in data['records']]
