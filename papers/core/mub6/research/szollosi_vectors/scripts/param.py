import flint
from parse import load
def load_param(path):
    r=load(path); b=r[1]
    P=b[5][1]
    elim=flint.fmpz_poly(P[0][1]); der=flint.fmpz_poly(P[1][1])
    nums=[(flint.fmpz_poly(n[0][1]), n[1]) for n in P[2]]
    return b[3], b[4], elim, der, nums, r[2]
if __name__=="__main__":
    import sys
    names,lin,elim,der,nums,real=load_param(sys.argv[1])
    print(names, lin, "deg", elim.degree(), "nums", len(nums), [n[1] for n in nums][:3])
    c,fl=elim.factor()
    print(sorted((f.degree(),e) for f,e in fl))
