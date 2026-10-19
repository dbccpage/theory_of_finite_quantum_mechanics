from pathlib import Path
import subprocess,sys
B=Path(__file__).resolve().parents[1]
for i in range(14,20):
    for tool in ['prepare.py','run.py']:
        subprocess.run([sys.executable,'-X','utf8',str(B/'tools'/tool),str(i)],check=True)
