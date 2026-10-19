def lines(data):return ['firewall'+'\t'+'\t'.join(r['output']) for r in data['records']]
