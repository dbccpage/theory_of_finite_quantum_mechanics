"""Exact selected degree-two context covers over F2.

The incidence map on global variables and the overlap map on zero-sum local
adjustments are distinct matrices. No floating Pauli check is used.
"""
from itertools import combinations

def _binary_matrix(rows, columns):
    if type(columns) is not int or columns < 0:
        raise ValueError('nonnegative integer column count required')
    if type(rows) not in (list, tuple) or any(type(r) not in (list, tuple) for r in rows):
        raise ValueError('binary rectangular matrix required')
    a = [list(r) for r in rows]
    if any(len(r) != columns or any(type(x) is not int or x not in (0, 1) for x in r) for r in a):
        raise ValueError('binary rectangular matrix required')
    return a

def rank(rows,columns):
    a=_binary_matrix(rows,columns)
    k=0
    for j in range(columns):
        i=next((i for i in range(k,len(a)) if a[i][j]),None)
        if i is None:continue
        a[k],a[i]=a[i],a[k]
        for i in range(k+1,len(a)):
            if a[i][j]:a[i]=[x^y for x,y in zip(a[i],a[k])]
        k+=1
    return k

def solve(rows,rhs,n):
    rows=_binary_matrix(rows,n)
    if type(rhs) not in (list, tuple) or len(rhs)!=len(rows) or any(type(b) is not int or b not in (0,1) for b in rhs):
        raise ValueError('one binary right-hand side per row required')
    a=[r+[b] for r,b in zip(rows,rhs)];pivots=[];k=0
    for j in range(n):
        i=next((i for i in range(k,len(a)) if a[i][j]),None)
        if i is None:continue
        a[k],a[i]=a[i],a[k]
        for i in range(len(a)):
            if i!=k and a[i][j]:a[i]=[x^y for x,y in zip(a[i],a[k])]
        pivots.append(j);k+=1
    if any(not any(r[:n]) and r[n] for r in a):return None
    result=[0]*n
    for i,j in enumerate(pivots):result[j]=a[i][-1]
    return result

def certify(case):
    n,contexts,targets=case['measurements'],case['contexts'],case['targets']
    if type(n) is not int or n<1 or len(contexts)!=len(targets) or not contexts:raise ValueError('nonempty context system required')
    if any(type(b) is not int or b not in (0,1) for b in targets):raise ValueError('F2 target required')
    if any(len(c)<2 or len(c)!=len(set(c)) or any(type(i) is not int or not 0<=i<n for i in c) for c in contexts):raise ValueError('distinct in-range context variables required')
    if any(sum(r in c for c in contexts)!=2 for r in range(n)):raise ValueError('this operation requires degree-two cover')
    overlaps=[[i,j,r] for i,j in combinations(range(len(contexts)),2) for r in sorted(set(contexts[i])&set(contexts[j]))]
    triples=[[i,j,k,r] for i,j,k in combinations(range(len(contexts)),3) for r in sorted(set(contexts[i])&set(contexts[j])&set(contexts[k]))]
    if triples:raise ValueError('degree-two cover has no triple intersections')
    offsets=[0]
    for c in contexts:offsets.append(offsets[-1]+len(c)-1)
    delta=[];discrepancy=[]
    for i,j,r in overlaps:
        row=[0]*offsets[-1]
        for k in (i,j):
            pos=contexts[k].index(r)
            for u in range(1,len(contexts[k])):
                if pos==0 or pos==u:row[offsets[k]+u-1]^=1
        delta.append(row);discrepancy.append((targets[i] if contexts[i][0]==r else 0)^(targets[j] if contexts[j][0]==r else 0))
    incidence=[[int(r in c) for r in range(n)] for c in contexts]
    rd=rank(delta,offsets[-1]);ra=rank([r+[b] for r,b in zip(delta,discrepancy)],offsets[-1]+1)
    ri=rank(incidence,n);ria=rank([r+[b] for r,b in zip(incidence,targets)],n+1)
    # The actual column sums are checked, not inferred from a status label.
    annihilates=[sum(row[j] for row in delta)%2 for j in range(offsets[-1])]
    if any(annihilates):raise ArithmeticError('claimed character does not annihilate image')
    dot=sum(discrepancy)%2
    global_section=solve(incidence,targets,n)
    return {'id':case['id'],'incidence':incidence,'overlaps':overlaps,'local_dimension':offsets[-1],
            'delta0':delta,'discrepancy':discrepancy,'d1':{'rows':0,'columns':len(overlaps),'entries':[]},
            'incidence_rank':ri,'incidence_augmented_rank':ria,'delta0_rank':rd,'delta0_augmented_rank':ra,
            'h1_dimension':len(overlaps)-rd,'left_character':[1]*len(overlaps),'character_on_columns':annihilates,
            'obstruction_pairing':dot,'global_section':global_section}
