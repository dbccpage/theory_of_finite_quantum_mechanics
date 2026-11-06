\\ Exact orthogonality of every pair in each candidate clique, in the compositum of the two factors.
\\ Real embedding chosen by matching the certified real roots (PARI polrootsreal order).
default(parisizemax, 2*10^9); default(realprecision, 200);
read(CF);
ipre(P,Q)=1+sum(j=1,5,P[j]*Q[j]+P[j+5]*Q[j+5]);
ipim(P,Q)=sum(j=1,5,P[j]*Q[j+5]-P[j+5]*Q[j]);
RR=vector(#FAC,k,polrootsreal(FAC[k]));
pair(u,v)={my(k1,k2,r1,r2,res=-1,C,Rp,aa,bb,P,Q); k1=u[1]; k2=v[1]; r1=RR[k1][u[2]]; r2=RR[k2][v[2]];
  if(k1==k2 && u[2]==v[2], error("same ray"));
  C=polcompositum(FAC[k1],FAC[k2],1);
  for(c=1,#C, Rp=C[c][1]; aa=C[c][2]; bb=C[c][3];
    foreach(polrootsreal(Rp), g, if(abs(subst(lift(aa),A,g)-r1)<10^-25 && abs(subst(lift(bb),A,g)-r2)<10^-25,
      if(k1==k2 && abs(subst(lift(aa),A,g)-subst(lift(bb),A,g))<10^-25, next);
      P=vector(10,i,Mod(subst(X[k1][i],A,lift(aa)),Rp)); Q=vector(10,i,Mod(subst(X[k2][i],A,lift(bb)),Rp));
      res=[ipre(P,Q)==0 && ipim(P,Q)==0, subst(lift(ipre(P,Q)),A,g), subst(lift(ipim(P,Q)),A,g)]; break(2))));
  if(res==-1,error(Str("no embedding ",u," ",v))); res};
{for(c=1,#CL, my(cl=CL[c], ok=1, n=0);
  for(s=1,6, for(t=s+1,6, n++; my(r=pair(cl[s],cl[t])); if(!r[1], ok=0; print("  pair ",s,t," not zero: ",r[2]*1.," ",r[3]*1.))));
  print("clique ",c,": ",n," pairs exactly orthogonal: ",ok))};
