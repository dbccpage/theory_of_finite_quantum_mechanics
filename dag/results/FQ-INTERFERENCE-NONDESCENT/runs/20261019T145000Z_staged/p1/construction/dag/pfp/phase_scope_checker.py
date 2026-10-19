"""Independent certificate predicates; does not import the native producer."""
from fractions import Fraction as Q
from pathlib import Path
from exact_json import require, rational
from review_exact_json import audit_bound

def square(z):return z*z

def verify(kind,values,raw,root):
    out=[rational(v) for v in raw]
    if kind in ('corpus','custody'):
        b=(root/values[0]).read_bytes()
        # Split-based non-overlapping literal counts, distinct from producer loops.
        checks=[len(b),len(b.split(b'\n'))-1]+[len(b.split(t))-1 for t in (b'sorry',b'Classical.choice',b'axiom')]
        require(out==checks,'G3_WITNESS:literal_inventory');return
    x=list(map(rational,values))
    if kind=='continuum':
        a,b,l=x
        require(len(out)==5 and out[0]==a+a and out[1]==b+b and out[2]==l*(l-1)-1 and out[3]==square(l+l-1) and out[4]==5,'G3_WITNESS:continuum_polynomial')
        require(4*out[2]+5==out[3],'G3_WITNESS:discriminant_identity')
    elif kind=='tensor':
        require(len(out)==7,'G1_SCHEMA:tensor_length');a,b,c,d=x
        require(out[:4]==[a*c,a*d,b*c,b*d],'G3_WITNESS:outer_product')
        require(out[4]==out[0]*out[3]-out[1]*out[2]==0 and out[5]==sum(z*z for z in out[:4])==out[6]==(a*a+b*b)*(c*c+d*d),'G3_WITNESS:tensor_det_norm')
    elif kind=='u1':
        require(len(out)==8,'G1_SCHEMA:u1_length');t,k=x
        require(k.denominator==1 and abs(k)<=32,'G1_SCHEMA:bounded_power')
        a,b,n,plus,inv,z,w,pnorm=out;den=1+t*t
        require(a*den==1-t*t and b*den==t+t and n==a*a+b*b==1 and plus==a+1 and plus!=0 and inv*plus==b and inv==t,'G3_WITNESS:cayley')
        def mul(v,w):return (v[0]*w[0]-v[1]*w[1],v[0]*w[1]+v[1]*w[0])
        def power(v,k):
            if k==0:return (Q(1),Q(0))
            u=power(v,k//2);u=mul(u,u)
            return mul(u,v) if k%2 else u
        target=power((Q(3,5),Q(4 if k>=0 else -4,5)),abs(int(k)))
        require((z,w)==target and pnorm==z*z+w*w==1,'G3_WITNESS:power_not_injectivity_proof')
    elif kind=='d2':
        require(len(out)==7,'G1_SCHEMA:d2_length');a,b,k,u,v=x
        require(k!=0 and (a!=0 or b!=0) and (u!=0 or v!=0),'G1_SCHEMA:nonzero_rays')
        def ray(a,b):return Q(int((a>0 and b>0) or (a<0 and b<0) or b==0))
        require(out==[ray(a,b),ray(k*a,k*b),ray(-b,a),a*u+b*v,ray(u,v),a*(a+b),ray(a,b)*(a*a+b*b)],'G3_WITNESS:binary_ray')
        require(out[0]==out[1] and out[0]+out[2]==1,'G3_WITNESS:ray_relations')
        if out[3]==0:require(out[0]+out[4]==1,'G3_WITNESS:orthogonal_sum')
    elif kind in ('interference','zero'):
        require(len(out)==8,'G1_SCHEMA:probe_length');a,b,c,d,v,w=x
        plus=[a*v+b*w,c*v+d*w];minus=[a*v-b*w,c*v-d*w]
        require(out[:2]==[v*v,w*w] and out[2:4]==[square(z) for z in plus] and out[4:6]==[square(z) for z in minus],'G3_WITNESS:actual_readout')
        require(out[6:]==[out[2]-out[4],out[3]-out[5]]==[4*a*b*v*w,4*c*d*v*w],'G3_WITNESS:cross_terms')
    elif kind=='fiber':
        require(all(z.denominator==1 for z in x+out),'G1_SCHEMA:Gaussian_integers');a,b=map(int,x);n,oc,fc=map(int,out[:3]);r=abs(a)+abs(b)
        require(r<=10 and n==a*a+b*b and len(out)==3+2*(oc+fc),'G1_SCHEMA:fiber_shape')
        pairs=list(zip(out[3::2],out[4::2]));orbit=pairs[:oc];fiber=pairs[oc:]
        units=[(1,0),(0,1),(-1,0),(0,-1)]
        require(orbit==sorted(set((u*a-v*b,u*b+v*a) for u,v in units)),'G3_WITNESS:unit_orbit')
        require(fiber==sorted(set(fiber)) and all(u*u+v*v==n for u,v in fiber),'G3_WITNESS:fiber_norms')
        require(set(fiber)=={(u,v) for u in range(-r,r+1) for v in range(-r,r+1) if u*u+v*v==n},'G3_WITNESS:bounded_fiber_completeness')
    elif kind=='weights':
        p,q,s,t=x
        require(len(out)==5 and out[0]==p+q and out[1]==min(p,q) and out[2]==p*s+q*t and out[3]==-2*out[0] and out[4]==2*out[0],'G3_WITNESS:weight_contract')
        if p>=0 and q>=0 and abs(s)<=2 and abs(t)<=2:require(out[3]<=out[2]<=out[4],'G3_WITNESS:convex_bound')
    else:raise ValueError('G1_SCHEMA:unknown_domain')

def check(request,candidate,task,config,root):
    _,c,public=audit_bound(request,candidate,task,config)
    data=c['data'];require(set(data)=={'records'} and len(data['records'])==len(public['cases']),'G1_SCHEMA:record_coverage')
    for record,values in zip(data['records'],public['cases']):
        require(record['input']==values,'G5_SCOPE:public_input_identity')
        verify(public['kind'],values,record['output'],root)
    return {'records_checked':len(data['records']),'scope':'Exact submitted inputs and literal Lean signatures; target imports remain open.'}
