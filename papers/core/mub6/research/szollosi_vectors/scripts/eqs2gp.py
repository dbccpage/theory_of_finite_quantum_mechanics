import sys
lines=open(sys.argv[1]).read().split("\n",2)
vars_=lines[0]; body=lines[2].strip()
with open(sys.argv[2],'w') as f:
    f.write("EQS=["+body.replace("\n","")+"];\n")
