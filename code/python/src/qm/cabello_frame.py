"""Exact finite frame-polytope enumeration and rational tomography.

Every square incidence basis is visited. A graph-component prefilter rejects
only structurally singular bases; surviving systems are solved over Q. The
real-polytope/linear-basis completeness bridge is stated separately in results.
"""
from fractions import Fraction as Q
from itertools import combinations,product
from math import comb,lcm
from .pfp_exact import determinant,eye,is_psd,matrix,rank,solve_unique


def system(rays,frames):
    rays=tuple(tuple(r) for r in rays);frames=tuple(tuple(f) for f in frames)
    if not rays or not frames or not rays[0]:raise ValueError('nonempty frame system required')
    d=len(rays[0]);n=len(rays)
    if any(len(r)!=d or any(type(x) is not int for x in r) or not any(r) for r in rays):raise ValueError('nonzero integer rays of one dimension required')
    for frame in frames:
        if len(frame)!=d or len(set(frame))!=d or any(type(i) is not int or not 0<=i<n for i in frame):raise ValueError('frame must contain distinct declared rays')
        if any(sum(a*b for a,b in zip(rays[i],rays[j]))!=0 for i,j in combinations(frame,2)):raise ValueError('orthogonal frame required')
    return rays,frames


def incidence(rays,frames):
    rays,frames=system(rays,frames)
    return tuple(tuple(Q(int(i in frame)) for i in range(len(rays))) for frame in frames)


def _unicyclic(m,edges,support):
    parent=list(range(m))
    def root(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for edge in support:
        a,b=map(root,edges[edge]);parent[a]=b
    vertices=[0]*m;counts=[0]*m
    for i in range(m):vertices[root(i)]+=1
    for edge in support:counts[root(edges[edge][0])]+=1
    return vertices==counts


def vertices(rays,frames,budget):
    rays,frames=system(rays,frames);a=incidence(rays,frames);m,n=len(frames),len(rays)
    if type(budget) is not int or budget<0:raise ValueError('nonnegative support budget required')
    if rank(a)!=m:raise ValueError('full row rank needed for square-basis enumeration')
    holders=[tuple(i for i,f in enumerate(frames) if r in f) for r in range(n)]
    if any(len(h)!=2 for h in holders):raise ValueError('degree-two ray incidence required')
    if comb(n,m)>budget:raise ValueError('enumeration budget exhausted; no infeasibility conclusion')
    found=set();examined=0
    for support in combinations(range(n),m):
        examined+=1
        if not _unicyclic(m,holders,support):continue
        try:x=solve_unique([[row[j] for j in support] for row in a],[1]*m)
        except ValueError:continue
        if min(x)<0:continue
        full=[Q(0)]*n
        for j,v in zip(support,x):full[j]=v
        if any(sum(row[j]*full[j] for j in range(n))!=1 for row in a):raise ArithmeticError('basis solution failed actual frame equations')
        found.add(tuple(full))
    return tuple(sorted(found)),examined


def projector_rows(rays):
    coordinates=list(combinations(range(len(rays[0])),2));coordinates=sorted([(i,i) for i in range(len(rays[0]))]+coordinates)
    rows=[]
    for ray in rays:
        norm=sum(x*x for x in ray)
        rows.append([Q(ray[i]*ray[j]*(1 if i==j else 2),norm) for i,j in coordinates])
    return rows,coordinates


def tomography(rays,weights):
    rows,coordinates=projector_rows(rays);values=solve_unique(rows,weights);d=len(rays[0]);rho=[[Q(0)]*d for _ in range(d)]
    for (i,j),v in zip(coordinates,values):rho[i][j]=rho[j][i]=v
    if sum(rho[i][i] for i in range(d))!=1:raise ArithmeticError('frame representative has nonunit trace')
    return matrix(rho)


def quadratic(rho,v):
    return sum((Q(v[i])*rho[i][j]*Q(v[j]) for i in range(len(v)) for j in range(len(v))),Q(0))


def shifted(rho,t):
    return tuple(tuple(x+t*int(i==j) for j,x in enumerate(row)) for i,row in enumerate(rho))


def certify(rays,frames,budget,negative_radius):
    rays,frames=system(rays,frames)
    if len(rays[0])!=4 or type(negative_radius) is not int or negative_radius<1:raise ValueError('four-dimensional witness system and positive search radius required')
    points,examined=vertices(rays,frames,budget);records=[];at_half=0;above_quarter=0
    for point in points:
        rho=tomography(rays,point);half=shifted(rho,Q(1,2));quarter=shifted(rho,Q(1,4))
        half_det=determinant(half)
        leading=[determinant([row[:k] for row in quarter[:k]]) for k in range(1,5)]
        if is_psd(half) and half_det==0:bound='at_minus_half';at_half+=1
        elif all(v>0 for v in leading):bound='above_minus_quarter';above_quarter+=1
        else:raise ArithmeticError('vertex falls outside the target spectral classes')
        witness=None
        for radius in range(1,negative_radius+1):
            for v in product(range(-radius,radius+1),repeat=4):
                value=quadratic(rho,v)
                if value<0:witness=(v,value);break
            if witness is not None:break
        if witness is None:raise ValueError('bounded negative-vector search found no witness; no PSD conclusion')
        v,value=witness
        denominator=lcm(*(x.denominator for row in rho for x in row))
        twice=[2*x for x in point];nums=[x*denominator for row in rho for x in row];negative=value*denominator
        if any(x.denominator!=1 for x in twice+nums+[negative]):raise ArithmeticError('nonintegral cleared certificate')
        records.append({'weights':list(map(str,point)),'representative':[[str(x) for x in row] for row in rho],
                        'negative_vector':list(v),'quadratic_value':str(value),'spectral_class':bound,
                        'half_shift_determinant':str(half_det),'quarter_shift_leading_minors':list(map(str,leading)),
                        'denominator':denominator,'matrix_numerators':list(map(int,nums)),'weights_twice':list(map(int,twice)),
                        'negative_value_numerator':int(negative)})
    return {'basis_supports_examined':examined,'incidence_rank':rank(incidence(rays,frames)),
            'projector_span_rank':rank(projector_rows(rays)[0]),'vertex_count':len(records),
            'spectral_counts':{'at_minus_half':at_half,'above_minus_quarter':above_quarter},'vertices':records}
