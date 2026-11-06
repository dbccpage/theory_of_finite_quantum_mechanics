import re, sys, json
from fractions import Fraction as F
sys.set_int_max_str_digits(0)
def _fix(o):
    if isinstance(o, dict): return F(int(o["n"]), 2**o["e"])
    if isinstance(o, list): return [_fix(x) for x in o]
    return o
def load(path):
    """msolve output -> nested lists; 'n / 2^k' becomes Fraction(n, 2**k). Parsed as JSON for speed."""
    s=open(path).read().strip().rstrip(':').replace("'",'"')
    s=re.sub(r'(?<![0-9])(-?\d++)\s*/\s*2\^(\d+)', r'{"n":"\1","e":\2}', s)
    return _fix(json.loads(s))
if __name__=="__main__":
    r=load(sys.argv[1]); print("dim flag",r[0],"; real solutions:",len(r[1][1]))
