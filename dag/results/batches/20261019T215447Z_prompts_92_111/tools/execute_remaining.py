import subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
subprocess.run([sys.executable,'-X','utf8',str(HERE/'run.py'),'0','p3'],check=True)
for i in range(1,20):
 subprocess.run([sys.executable,'-X','utf8',str(HERE/'prepare.py'),str(i)],check=True)
 subprocess.run([sys.executable,'-X','utf8',str(HERE/'run.py'),str(i)],check=True)
