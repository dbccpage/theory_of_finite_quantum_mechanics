import yaml
import json

def inspect():
    ledgers = {
        'mub': 'papers/core/mub6/mub6_claim_ledger.yaml',
        'fsp': 'papers/core/fsp/claim_ledger.yaml',
        'majorana': 'papers/core/majorana/claim_ledger.yaml'
    }
    summary = {}
    for k, p in ledgers.items():
        with open(p, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        claims = data.get('claims', [])
        summary[k] = {
            'count': len(claims),
            'claims': claims
        }
        print(f"{k}: {len(claims)} claims loaded")
        
    with open('.agents/teamwork/worker_m4_matrix/all_claims.json', 'w', encoding='utf-8') as out:
        json.dump(summary, out, indent=2)
    print("Dumped to all_claims.json")

if __name__ == '__main__':
    inspect()
