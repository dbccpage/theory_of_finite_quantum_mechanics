\\ Exact orthogonality / unbiasedness status between all real solutions of an msolve parametrization.
\\ Usage: gp -q graph.gp with DATA, EQSF, OUT set via a preamble file.
default(parisizemax, 4*10^9);
\p 150
read(DATA); read(EQSF);
V=[a1,a2,a3,a4,a5,b1,b2,b3,b4,b5];
Fac=factor(ELIM)[,1]; nfac=#Fac;
X=vector(nfac,k, vector(10,i, Mod(-NUMS[i][1],Fac[k])/Mod(NUMS[i][2]*DER,Fac[k])));
bad=0; for(k=1,nfac, if(substvec(EQS,V,X[k])!=vector(#EQS,i,0)*Mod(1,Fac[k]), bad++));
print("factors ",nfac,"  degrees ",vecsort(vector(nfac,k,poldegree(Fac[k]))),"  factors failing the equations: ",bad);
R=vector(nfac,k,polrootsreal(Fac[k]));
print("real solutions: ", sum(k=1,nfac,#R[k]));
sep=1.;
{for(k=1,nfac, for(i=1,#R[k], for(j=i+1,#R[k], sep=min(sep,abs(R[k][i]-R[k][j])))))};
print("min separation of real roots within a factor: ", sep);
ipre(P,Q)=1+sum(j=1,5,P[j]*Q[j]+P[j+5]*Q[j+5]);
ipim(P,Q)=sum(j=1,5,P[j]*Q[j+5]-P[j+5]*Q[j]);
match(v,t)={my(d=vector(#v,i,abs(v[i]-t)),p=vecsort(d,,1)); if(#v>1 && d[p[2]]<10^-60, error("ambiguous match")); if(d[p[1]]>10^-60, error("no match")); p[1]};
out=List(); nz=0;
{for(k1=1,nfac, for(k2=k1,nfac,
  if(#R[k1]==0 || #R[k2]==0, next);
  C=polcompositum(Fac[k1],Fac[k2],1);
  for(c=1,#C,
    my(Rp=C[c][1],aa=C[c][2],bb=C[c][3]);
    my(rr=polrootsreal(Rp)); if(#rr==0, next);
    my(P=vector(10,i,subst(lift(X[k1][i]),A,aa)), Q=vector(10,i,subst(lift(X[k2][i]),A,bb)));
    my(re=ipre(P,Q), im=ipim(P,Q), st);
    st = if(re==0 && im==0, 0, if(re^2+im^2-6==0, 1, 2));
    for(g=1,#rr,
      my(al=subst(lift(aa),A,rr[g]), be=subst(lift(bb),A,rr[g]));
      my(i1=match(R[k1],al), i2=match(R[k2],be));
      listput(out,[k1,i1,k2,i2,st])))))};
print("real pairs recorded: ", #out);
write(OUT, Vec(out));
