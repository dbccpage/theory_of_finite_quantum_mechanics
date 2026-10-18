import json

def process():
    with open('.agents/teamwork/worker_m4_matrix/all_claims.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open('.agents/teamwork/worker_m4_matrix/claims_analysis.txt', 'w', encoding='utf-8') as out:
        for domain in ['mub', 'fsp', 'majorana']:
            claims = data[domain]['claims']
            out.write(f"=== DOMAIN: {domain.upper()} ({len(claims)} claims) ===\n\n")
            for c in claims:
                cid = c.get('id')
                name = c.get('name')
                stmt = c.get('statement')
                ctype = c.get('claim_type')
                lean = c.get('lean4') or c.get('lean4_formalization') or c.get('conditional_lean_reference')
                code = c.get('code_evidence', {})
                out.write(f"ID: {cid}\nName: {name}\nType: {ctype}\nStatement: {stmt}\nLean: {lean}\nCode Evidence: {code}\n")
                out.write("-" * 50 + "\n")

if __name__ == '__main__':
    process()
