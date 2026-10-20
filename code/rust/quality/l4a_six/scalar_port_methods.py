"""Change only scalar method sites identified by a pinned staged compiler run.
AuthorityEffect: None. This is a first pass; closure/error propagation still needs review.
"""
import argparse,re,json
from pathlib import Path as _FilesystemPath
import sys as _contract_sys
_contract_sys.path.insert(0, str(_FilesystemPath(__file__).resolve().parents[4] / "scripts"))
from contract_scores import RecordPath as Path, copy_file as _copy_record_file
from replay import digest

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--log',type=Path,required=True);args=parser.parse_args()
    stage=Path(__file__).parent/'scalar_port/linear_algebra';manifest=json.loads((args.log.parent/'staged_sources.json').read_text(encoding='utf8'))
    todo={};names={'add':'try_add','sub':'try_sub','mul':'try_mul','neg':'try_neg','is_zero':'try_is_zero','conjugate':'try_conj'}
    pattern=r'src[\\/]linear_algebra[\\/]([^:]+):(\d+):(\d+): error\[E0599\]: no method named `([^`]+)`'
    for match in re.finditer(pattern,args.log.read_text(encoding='utf8')):
        filename,line,col,method=match.groups()
        if method not in names:continue
        p=stage/filename
        if p.resolve().parent!=stage.resolve():raise RuntimeError('Out-of-scope diagnostic path')
        expected=manifest.get(str(p.resolve()),manifest.get(str(p)))
        if expected!=digest(p):raise RuntimeError('Staged source changed since diagnostic: '+filename)
        text=p.read_text(encoding='utf8');lines=text.splitlines(keepends=True);row=lines[int(line)-1]
        hits=list(re.finditer(r'\.'+method+r'\s*\(',row))
        if not hits:continue
        chosen=min(hits,key=lambda h:abs(h.start()+1-(int(col)-1)))
        if abs(chosen.start()+1-(int(col)-1))>5:continue
        pos=sum(len(x)for x in lines[:int(line)-1])+chosen.start();todo.setdefault(p,{})[pos]=method
    changes={}
    for p,sites in todo.items():
        text=p.read_text(encoding='utf8')
        for pos,method in sorted(sites.items(),reverse=True):
            opening=text.index('(',pos);depth=0;closing=None
            for j in range(opening,len(text)):
                if text[j]=='(':depth+=1
                elif text[j]==')':
                    depth-=1
                    if depth==0:closing=j;break
            if closing is None:raise RuntimeError('Unmatched method argument parentheses')
            text=text[:closing+1]+'?'+text[closing+1:]
            text=text[:pos+1]+names[method]+text[pos+1+len(method):]
        p.write_bytes(text.encode('utf8'));changes[p.name]=len(sites)
    print('Staged compiler-identified method changes',changes)
if __name__=='__main__':main()
