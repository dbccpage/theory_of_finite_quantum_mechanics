\\ Sturm count and real-root approximations of every factor. Needs FACF (file setting FAC) and OUTF.
default(parisizemax, 4*10^9); default(realprecision, 120);
read(FACF);
{for(k=1,#FAC, my(n=polsturm(FAC[k]), r=polrootsreal(FAC[k]));
  if(#r!=n, error("count mismatch"));
  write(OUTF, [k-1, n, apply(x->Str(x), r)]))};
