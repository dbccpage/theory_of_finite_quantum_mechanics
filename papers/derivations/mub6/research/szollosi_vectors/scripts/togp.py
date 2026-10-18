"""Write a gp data file from an msolve parametrization: elim, der, nums, lin."""
import sys
from param import load_param
names,lin,elim,der,nums,real=load_param(sys.argv[1])
def gpol(p): return "Pol(["+",".join(str(c) for c in reversed(p.coeffs()))+"],A)"
with open(sys.argv[2],'w') as f:
    f.write(f"NAMES=[{",".join(chr(34)+n+chr(34) for n in names[:-1])}];\nLIN={lin};\nELIM={gpol(elim)};\nDER={gpol(der)};\n")
    f.write("NUMS=["+",".join(f"[{gpol(n)},{c}]" for n,c in nums)+"];\n")
    f.write(f"NREAL={len(real[1]) if isinstance(real,list) and len(real)>1 else -1};\n")
