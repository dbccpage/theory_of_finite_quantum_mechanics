"""Extract the real-solution boxes (last top-level element) of an msolve output without parsing the rest."""
import sys
from parse import F, _fix
import re, json
def realsols(path):
    s=open(path).read().strip().rstrip(':')
    depth=0
    for i in range(len(s)-1,-1,-1):
        c=s[i]
        if c==']': depth+=1
        elif c=='[': depth-=1
        elif c==',' and depth==1: break
    t=s[i+1:-1].strip()
    t=re.sub(r'(?<![0-9])(-?\d++)\s*/\s*2\^(\d+)', r'{"n":"\1","e":\2}', t)
    return _fix(json.loads(t))
if __name__=="__main__":
    r=realsols(sys.argv[1]); print(r[0], len(r[1]))
