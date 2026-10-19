"""Independent exhaustive integer-determinant/Cramer census and matrix predicates.

Does not import the Python graph-prefilter enumerator, Rust port, or their matrix
helpers. Every size-row-rank basis is visited without the graph prefilter.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json,re,sys
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'dag/pfp/prepare_stage.py').is_file());sys.path.insert(0,str(ROOT/'dag/pfp'))
from exact_json import bound,require,rational,vector
TASK='FQ-CABELLO-FRAME-POLYTOPE-146'


def det(a):
    a=[list(row) for row in a];n=len(a)
    if n==0:return 1
    sign=1;previous=1
    for k in range(n-1):
        p=next((i for i in range(k,n) if a[i][k]),None)
        if p is None:return 0
        if p!=k:a[k],a[p]=a[p],a[k];sign=-sign
        pivot=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator=a[i][j]*pivot-a[i][k]*a[k][j]
                a[i][j]=numerator/previous if type(numerator) is Q or type(previous) is Q else numerator//previous
                if type(numerator) is int and type(previous) is int:require(numerator%previous==0,'G3_WITNESS:nonexact_Bareiss_division')
            a[i][k]=0
        previous=pivot
    return sign*a[-1][-1]


def geometry(public):
    rays,frames=public['rays'],public['frames'];require(type(rays) is list and len(rays)==18 and all(type(r) is list and len(r)==4 and all(type(x) is int for x in r) and any(r) for r in rays),'G1_SCHEMA:rays')
    require(type(frames) is list and len(frames)==9,'G1_SCHEMA:frames')
    for f in frames:
        require(type(f) is list and len(f)==4 and all(type(i) is int and 0<=i<18 for i in f) and len(set(f))==4,'G1_SCHEMA:frame_members')
        require(all(sum(x*y for x,y in zip(rays[i],rays[j]))==0 for i,j in combinations(f,2)),'G3_WITNESS:orthogonality')
    require(all(sum(r in f for f in frames)==2 for r in range(18)),'G3_WITNESS:degree_two')
    return rays,frames,[[int(r in f) for r in range(18)] for f in frames]


def complete_bases(a):
    found=set();examined=0;n=len(a[0]);m=len(a);nonsingular=0
    for indices in combinations(range(n),m):
        examined+=1;basis=[[row[j] for j in indices] for row in a];d=det(basis)
        if d==0:continue
        nonsingular+=1;solution=[]
        for j in range(m):
            changed=[row[:] for row in basis]
            for row in changed:row[j]=1
            solution.append(Q(det(changed),d))
        if min(solution)<0:continue
        full=[Q(0)]*n
        for j,x in zip(indices,solution):full[j]=x
        require(all(sum(row[j]*full[j] for j in range(n))==1 for row in a),'G3_WITNESS:Cramer_equations')
        found.add(tuple(full))
    require(nonsingular>0,'G3_WITNESS:rank_deficient')
    return found,examined


def vertex(public,a,answer):
    fields={'weights','representative','negative_vector','quadratic_value','spectral_class','half_shift_determinant','quarter_shift_leading_minors','denominator','matrix_numerators','weights_twice','negative_value_numerator'}
    require(type(answer) is dict and set(answer)==fields,'G1_SCHEMA:vertex_fields')
    weights=vector(answer['weights'],18);require(min(weights)>=0 and all(sum(weights[j] for j in f)==1 for f in public['frames']),'G3_WITNESS:frame_valuation')
    raw=answer['representative'];require(type(raw) is list and len(raw)==4,'G1_SCHEMA:representative')
    h=[vector(row,4) for row in raw]
    require(all(h[i][j]==h[j][i] for i in range(4) for j in range(4)) and sum(h[i][i] for i in range(4))==1,'G3_WITNESS:trace_symmetry')
    for r,f in zip(public['rays'],weights):
        require(sum(Q(r[i])*h[i][j]*r[j] for i in range(4) for j in range(4))==f*sum(x*x for x in r),'G3_WITNESS:tomography')
    v=answer['negative_vector'];require(type(v) is list and len(v)==4 and all(type(x) is int for x in v),'G1_SCHEMA:negative_vector')
    q=sum(Q(v[i])*h[i][j]*v[j] for i in range(4) for j in range(4))
    require(q<0 and rational(answer['quadratic_value'])==q,'G4_COUNTERMODEL:negative_quadratic')
    half=[[h[i][j]+Q(i==j,2) for j in range(4)] for i in range(4)];quarter=[[h[i][j]+Q(i==j,4) for j in range(4)] for i in range(4)]
    half_det=det(half);leading=[det([r[:k] for r in quarter[:k]]) for k in range(1,5)]
    require(rational(answer['half_shift_determinant'])==half_det and vector(answer['quarter_shift_leading_minors'],4)==leading,'G3_WITNESS:spectral_determinants')
    if answer['spectral_class']=='at_minus_half':
        require(half_det==0 and all(det([[half[i][j] for j in indices] for i in indices])>=0 for k in range(1,5) for indices in combinations(range(4),k)),'G3_WITNESS:half_spectral_class')
    else:
        require(answer['spectral_class']=='above_minus_quarter' and all(x>0 for x in leading),'G3_WITNESS:quarter_spectral_class')
    d=answer['denominator'];nums=answer['matrix_numerators'];twice=answer['weights_twice'];neg=answer['negative_value_numerator']
    require(type(d) is int and d>0 and type(nums) is list and len(nums)==16 and type(twice) is list and len(twice)==18 and all(type(x) is int for x in nums+twice) and type(neg) is int,'G1_SCHEMA:integer_certificate')
    require(all(nums[4*i+j]==d*h[i][j] for i in range(4) for j in range(4)) and all(twice[i]==2*weights[i] and 0<=twice[i]<=2 for i in range(18)) and neg==d*q,'G3_WITNESS:integer_transport')
    return tuple(weights)


def check(request,candidate):
    _,certificate,public=bound(request,candidate,TASK);data=certificate['data'];rays,frames,a=geometry(public)
    require(type(data) is dict and set(data)=={'basis_supports_examined','incidence_rank','projector_span_rank','vertex_count','spectral_counts','vertices'},'G1_SCHEMA:data')
    answers=data['vertices'];require(type(answers) is list and bool(answers),'G1_SCHEMA:empty_vertices')
    listed=[vertex(public,a,v) for v in answers]
    require(len(listed)==len(set(listed)) and listed==sorted(listed),'G3_WITNESS:duplicate_or_unordered_vertex')
    complete,examined=complete_bases(a)
    require(set(listed)==complete and type(data['basis_supports_examined']) is int and data['basis_supports_examined']==examined,'G3_WITNESS:incomplete_census')
    require(data['incidence_rank']==9 and data['projector_span_rank']==10 and data['vertex_count']==len(listed)==146,'G3_WITNESS:stated_census')
    # Exhibit a nonzero 10x10 projector minor, avoiding reliance on a rank label.
    coordinates=[(i,j) for i in range(4) for j in range(i,4)]
    projectors=[[Q(r[i]*r[j]*(1 if i==j else 2),sum(x*x for x in r)) for i,j in coordinates] for r in rays]
    reduced=[row[:] for row in projectors];ids=list(range(18));rk=0
    for j in range(10):
        pivot=next((i for i in range(rk,18) if reduced[i][j]),None)
        if pivot is None:continue
        reduced[rk],reduced[pivot]=reduced[pivot],reduced[rk];ids[rk],ids[pivot]=ids[pivot],ids[rk]
        c=reduced[rk][j];reduced[rk]=[x/c for x in reduced[rk]]
        for i in range(18):
            if i!=rk:
                c=reduced[i][j];reduced[i]=[x-c*y for x,y in zip(reduced[i],reduced[rk])]
        rk+=1
    require(rk==10 and det([projectors[i] for i in ids[:10]])!=0,'G3_WITNESS:projector_span')
    counts={k:sum(v['spectral_class']==k for v in answers) for k in ('at_minus_half','above_minus_quarter')}
    require(type(data['spectral_counts']) is dict and data['spectral_counts']==counts and counts=={'at_minus_half':26,'above_minus_quarter':120},'G3_WITNESS:stated_spectral_counts')
    pins=[p for p in certificate['source_pins'] if p['path'].endswith('/lean4/CabelloVertexData.lean')]
    require(len(pins)==1,'G5_SCOPE:kernel_data_source')
    source=(ROOT/pins[0]['path']).read_text()
    expected={'raysData':rays,'contextsData':frames,'weightsData':[v['weights_twice'] for v in answers],'matrixData':[v['matrix_numerators'] for v in answers],'denominatorData':[v['denominator'] for v in answers],'vectorData':[v['negative_vector'] for v in answers],'negativeData':[v['negative_value_numerator'] for v in answers]}
    for name,value in expected.items():
        matches=re.findall(r'^def '+name+r' : [^\n]+ :=\n(\[[\s\d,\-\[\]]*\])\n',source,re.M)
        require(len(matches)==1 and json.loads(matches[0])==value,'G5_SCOPE:kernel_data_translation:'+name)
    return {'basis_supports_checked':examined,'distinct_vertices':len(listed),'spectral_counts':counts,'actual_negative_quadratic_witnesses':len(listed),'scope':'Exact fixed finite input census and matrix witnesses; no promotion of the old arithmetic census lemma into a real-polytope completeness proof.'}


if __name__=='__main__':
    import json
    print(json.dumps(check(*sys.argv[1:]),indent=2))
