"""Independent finite contract and complete-frame equations; no uniqueness flag."""
from fractions import Fraction as Q
from itertools import permutations
from pathlib import Path
import sys
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'dag/pfp/prepare_stage.py').is_file());sys.path.insert(0,str(ROOT/'dag/pfp'))
from exact_json import bound,require,vector,rational
TASK='FQ-GAP-BORN-UNIQUENESS-GLEASON'
def check(request,candidate):
    _,c,p=bound(request,candidate,TASK);d=c['data'];require(type(d) is dict and set(d)=={'weak_contracts','dimensions','frames','uniqueness_status'},'G1_SCHEMA:data')
    for field in ('weak_contracts','dimensions','frames'):require(type(d[field]) is list and len(d[field])==len(p[field]),'G1_SCHEMA:coverage')
    for x,a in zip(p['weak_contracts'],d['weak_contracts']):
        require(type(a) is dict and set(a)=={'id','normalized_weights','Born','swapped','unit_total_Born','unit_total_swapped','difference'} and a['id']==x['id'],'G1_SCHEMA:weak')
        w,e=vector(x['weights'],2),vector(x['effect'],2);require(min(w)>=0 and sum(w)>0 and min(e)>=0 and max(e)<=1,'G3_WITNESS:weak_premise');v=[z/sum(w) for z in w];b=v[0]*e[0]+v[1]*e[1];s=v[0]*e[1]+v[1]*e[0]
        require(vector(a['normalized_weights'],2)==v and [rational(a[k]) for k in ('Born','swapped','unit_total_Born','unit_total_swapped','difference')]==[b,s,Q(1),Q(1),b-s],'G3_WITNESS:actual_weak_rules')
    for x,a in zip(p['dimensions'],d['dimensions']):
        require(type(a) is dict and set(a)=={'id','listed_count','distinct_count','dimension_three_guard'} and a['id']==x['id'],'G1_SCHEMA:dimension')
        require(type(a['listed_count']) is int and type(a['distinct_count']) is int and type(a['dimension_three_guard']) is bool and (a['listed_count'],a['distinct_count'],a['dimension_three_guard'])==(len(x['labels']),len(set(x['labels'])),len(set(x['labels']))>=3),'G3_WITNESS:distinct_dimension')
    for x,a in zip(p['frames'],d['frames']):
        n=len(x['psi']);require(type(a) is dict and set(a)=={'id','dimension','gram_matrices','determinants','quadratic_values','quartic_values','quadratic_sums','quartic_sums','quartic_deficit'} and a['id']==x['id'] and type(a['dimension']) is int and a['dimension']==n,'G1_SCHEMA:frame')
        psi=vector(x['psi'],n);norm=sum(z*z for z in psi);grams=[];dets=[];qv=[]
        for f in x['frames']:
            f=[vector(row,n) for row in f];require(len(f)==n and norm>0,'G3_WITNESS:complete_frame');g=[[sum(f[i][k]*f[j][k] for k in range(n)) for j in range(n)] for i in range(n)]
            require(all(g[i][i]>0 and all(g[i][j]==0 for j in range(n) if i!=j) for i in range(n)),'G3_WITNESS:orthogonal_frame');grams.append(g)
            det=Q(0)
            for perm in permutations(range(n)):
                z=Q((-1)**sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n)))
                for i in range(n):z*=f[i][perm[i]]
                det+=z
            require(det!=0,'G3_WITNESS:rank');dets.append(det);qv.append([sum(psi[k]*f[i][k] for k in range(n))**2/(norm*g[i][i]) for i in range(n)])
        quart=[[z*z for z in row] for row in qv];expected={'gram_matrices':[[[str(z) for z in row] for row in g] for g in grams],'determinants':list(map(str,dets)),'quadratic_values':[list(map(str,row)) for row in qv],'quartic_values':[list(map(str,row)) for row in quart],'quadratic_sums':list(map(str,map(sum,qv))),'quartic_sums':list(map(str,map(sum,quart))),'quartic_deficit':str(sum(quart[0])-sum(quart[1]))}
        require(all(a[k]==v for k,v in expected.items()) and all(sum(row)==1 for row in qv) and sum(quart[0])!=sum(quart[1]),'G3_WITNESS:actual_frame_rival')
    require(d['weak_contracts'][0]['difference']=='3/5' and d['frames'][1]['quartic_deficit']=='288/625','G3_WITNESS:selected_source_values')
    require(d['uniqueness_status']=='NOT_DISCHARGED','G5_SCOPE:uniqueness_promoted')
    return {'weak_contracts':len(d['weak_contracts']),'complete_frame_pairs':len(d['frames']),'three_dimensional_quartic_deficit':'288/625','Gleason_uniqueness_discharged':False}
if __name__=='__main__':
    import json
    print(json.dumps(check(*sys.argv[1:]),indent=2))
