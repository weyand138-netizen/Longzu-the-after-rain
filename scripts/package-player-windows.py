"""Turn a Ren'Py 8.5.3 Windows build into the player-only distribution.

Requires the official SDK ZIP; preserves game bytes, replaces only the two
icon-customized launchers with official stock files, and removes root readmes.
"""
from pathlib import Path,PurePosixPath
import argparse,hashlib,zipfile
SDK_SHA256='ff57648f9c04f27e381c48af6d8e3ee3cdec296bed4d3831f47f09b0a71b505e'
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--sdk-zip',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 if a.output.exists():p.error('Output exists; use a new path to preserve previous packages')
 if sha(a.sdk_zip)!=SDK_SHA256:p.error('SDK checksum differs from the official RenPy 8.5.3 ZIP')
 omitted={'README.md','README_EN.md','THIRD_PARTY_NOTICES.md'};renamed={'After rain.exe':'雨停之后.exe','After rain.py':'雨停之后.py'};seen=set();expected={}
 with zipfile.ZipFile(a.input) as source,zipfile.ZipFile(a.sdk_zip) as sdk,zipfile.ZipFile(a.output,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as out:
  roots={n.split('/')[0] for n in source.namelist()};assert len(roots)==1
  stock={n:sdk.read('renpy-8.5.3-sdk/lib/py3-windows-x86_64/'+s) for n,s in [('After rain.exe','renpy.exe'),('lib/py3-windows-x86_64/pythonw.exe','pythonw.exe')]}
  for member in source.infolist():
   if member.is_dir():continue
   parts=PurePosixPath(member.filename).parts;assert len(parts)>1 and '..' not in parts and ':' not in member.filename and '\\' not in member.filename
   rel='/'.join(parts[1:]);assert rel.casefold() not in seen;seen.add(rel.casefold())
   assert parts[1] in {'game','lib','renpy','After rain.exe','After rain.py',*omitted},rel
   if rel in omitted:continue
   assert '/saves/' not in '/'+rel and not rel.endswith(('.save','.log')) and not rel.startswith('game/testcases.') and not rel.startswith('game/zz_'),rel
   data=stock[rel] if rel in stock else source.read(member)
   name='雨停之后/'+renamed.get(rel,rel);out.writestr(name,data,compress_type=zipfile.ZIP_DEFLATED,compresslevel=6);expected[name]=hashlib.sha256(data).hexdigest()
 with zipfile.ZipFile(a.output) as z:
  assert z.testzip() is None and set(z.namelist())==set(expected)
  for n,digest in expected.items():assert hashlib.sha256(z.read(n)).hexdigest()==digest,n
 print('Player ZIP created:',a.output,'files:',len(expected),'SHA-256:',sha(a.output))
if __name__=='__main__':main()
