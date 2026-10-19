"""Independent local-section response construction and packed-bit span ranks."""
from itertools import combinations
from pathlib import Path
import sys
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'dag/pfp/prepare_stage.py').is_file());sys.path.insert(0,str(ROOT/'dag/pfp'))
from exact_json import bound,require
TASK='FQ-CONTEXTUALITY-CECH-F2'
def rank(rows):
    basis={}
    for row in rows:
        v=sum(x<<i for i,x in enumerate(row))
        while v:
            p=v.bit_length()-1
            if p not in basis:basis[p]=v;break
            v^=basis[p]
    return len(basis)
def exact_tree(value):
    if value is None or type(value) is str:return
    if type(value) is int:return
    if type(value) is list:
        for v in value:exact_tree(v)
        return
    if type(value) is dict:
        for v in value.values():exact_tree(v)
        return
    raise ValueError('G1_SCHEMA:non_integer_tree')
def expected(p):
    n,cs,bs=p['measurements'],p['contexts'],p['targets'];m=len(cs)
    require(all(len(c)==len(set(c)) and all(type(r) is int and 0<=r<n for r in c) for c in cs),'G3_WITNESS:cover')
    require(all(sum(r in c for c in cs)==2 for r in range(n)),'G3_WITNESS:degree_two')
    edges=[[i,j,r] for i,j in combinations(range(m),2) for r in range(n) if r in cs[i] and r in cs[j]]
    base=[[b]+[0]*(len(c)-1) for b,c in zip(bs,cs)]
    def overlap(sections):return [sections[i][cs[i].index(r)]^sections[j][cs[j].index(r)] for i,j,r in edges]
    discrepancy=overlap(base);columns=[]
    for i,c in enumerate(cs):
        for k in range(1,len(c)):
            local=[[0]*len(context) for context in cs];local[i][0]=local[i][k]=1;columns.append(overlap(local))
    delta=[list(x) for x in zip(*columns)];incidence=[[int(r in c) for r in range(n)] for c in cs]
    rd=rank(delta);ri=rank(incidence);ra=rank([r+[b] for r,b in zip(delta,discrepancy)]);ria=rank([r+[b] for r,b in zip(incidence,bs)])
    annihilate=[sum(col)%2 for col in columns];dot=sum(discrepancy)%2
    require(not any(annihilate),'G3_WITNESS:annihilator')
    require(not any(set(cs[i])&set(cs[j])&set(cs[k]) for i,j,k in combinations(range(m),3)),'G3_WITNESS:actual_C2_not_empty')
    return {'id':p['id'],'incidence':incidence,'overlaps':edges,'local_dimension':len(columns),'delta0':delta,'discrepancy':discrepancy,'d1':{'rows':0,'columns':len(edges),'entries':[]},'incidence_rank':ri,'incidence_augmented_rank':ria,'delta0_rank':rd,'delta0_augmented_rank':ra,'h1_dimension':len(edges)-rd,'left_character':[1]*len(edges),'character_on_columns':annihilate,'obstruction_pairing':dot,'global_section':[0]*n if not any(bs) else None}
def check(request,candidate):
    _,c,p=bound(request,candidate,TASK);d=c['data'];exact_tree(d)
    require(type(d) is dict and set(d)=={'cases'} and type(d['cases']) is list and len(d['cases'])==len(p['cases']),'G1_SCHEMA:cases')
    for public,actual in zip(p['cases'],d['cases']):
        require(actual==expected(public),'G3_WITNESS:actual_cochain_matrices_and_ranks')
        if actual['global_section'] is not None:require(all(sum(actual['global_section'][r] for r in ctx)%2==b for ctx,b in zip(public['contexts'],public['targets'])),'G3_WITNESS:global_section')
        else:require(actual['obstruction_pairing']==1 and actual['delta0_augmented_rank']==actual['delta0_rank']+1,'G3_WITNESS:actual_obstruction')
    require([(c['incidence_rank'],c['delta0_rank'],c['delta0_augmented_rank']) for c in d['cases']]==[(5,8,9),(8,17,18),(5,8,8)],'G3_WITNESS:selected_rank_claims')
    return {'cases':3,'peres_overlap_rank':8,'peres_incidence_rank':5,'cabello_overlap_rank':17,'scope':'Actual degree-two covers, exact native matrices; generic d-squared and parity kernel results have their literal separate scope.'}
if __name__=='__main__':
    import json
    print(json.dumps(check(*sys.argv[1:]),indent=2))
