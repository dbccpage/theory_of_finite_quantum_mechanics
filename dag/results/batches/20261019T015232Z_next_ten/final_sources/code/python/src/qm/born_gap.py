"""Exact finite insufficiency witnesses; no Gleason uniqueness theorem is derived."""
from fractions import Fraction as Q
from .pfp_exact import determinant,matrix
def weak_contract(weights,effect):
    if len(weights)!=2 or len(effect)!=2 or any(type(x) not in (int,Q) for x in weights+effect):raise ValueError('exact two-label inputs required')
    w,e=list(map(Q,weights)),list(map(Q,effect));total=sum(w)
    if min(w)<0 or total<=0 or min(e)<0 or max(e)>1:raise ValueError('nonnegative nonzero weights and [0,1] effects required')
    p=[x/total for x in w];born=sum(x*y for x,y in zip(p,e));swap=sum(x*y for x,y in zip(p,reversed(e)))
    return {'normalized_weights':list(map(str,p)),'Born':str(born),'swapped':str(swap),'unit_total_Born':'1','unit_total_swapped':'1','difference':str(born-swap)}
def frame_certificate(psi,frames):
    n=len(psi)
    if n not in (2,3) or len(frames)!=2 or any(type(x) not in (int,Q) for x in psi):raise ValueError('exact two- or three-dimensional source comparison required')
    psi=list(map(Q,psi));norm=sum(x*x for x in psi)
    if norm<=0:raise ValueError('nonzero state required')
    qs=[];fourths=[];grams=[];dets=[]
    for f in frames:
        if len(f)!=n or any(len(v)!=n or any(type(x) not in (int,Q) for x in v) for v in f):raise ValueError('complete exact frame required')
        gram=[[sum(Q(x)*Q(y) for x,y in zip(v,w)) for w in f] for v in f]
        if any(gram[i][i]<=0 or any(gram[i][j] for j in range(n) if j!=i) for i in range(n)):raise ValueError('orthogonal nonzero frame required')
        q=[sum(Q(x)*y for x,y in zip(v,psi))**2/(norm*gram[i][i]) for i,v in enumerate(f)];qs.append(q);fourths.append([x*x for x in q]);grams.append(gram);dets.append(determinant(matrix(f)))
    return {'dimension':n,'gram_matrices':[[[str(x) for x in r] for r in g] for g in grams],'determinants':list(map(str,dets)),'quadratic_values':[list(map(str,q)) for q in qs],'quartic_values':[list(map(str,q)) for q in fourths],'quadratic_sums':[str(sum(q)) for q in qs],'quartic_sums':[str(sum(q)) for q in fourths],'quartic_deficit':str(sum(fourths[0])-sum(fourths[1]))}
def dimension(labels):
    if not labels or any(type(x) is not str for x in labels):raise ValueError('explicit labels required')
    return {'listed_count':len(labels),'distinct_count':len(set(labels)),'dimension_three_guard':len(set(labels))>=3}
