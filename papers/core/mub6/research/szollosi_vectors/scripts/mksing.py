import sys
lines=open(sys.argv[1]).read().split("\n",2)
vars_=lines[0]; body=lines[2].strip().rstrip(',').replace("\n","")
open(sys.argv[2],'w').write(f"""ring r=0,({vars_}),dp;
ideal i={body};
int t=timer; ideal g=std(i);
print("dim="+string(dim(g))+" vdim="+string(vdim(g))+" time="+string(timer-t));
quit;
""")
