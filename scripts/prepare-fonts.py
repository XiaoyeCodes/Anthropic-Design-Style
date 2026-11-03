"""Maintainer tool: reproducible OFL font derivatives. Not needed for installation."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import urllib.request
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT=Path(__file__).resolve().parents[1]
COMMIT='2fe1e8c6b137fb13041a7cfca6fdcd8a910ea4dc'
BASE=f'https://raw.githubusercontent.com/google/fonts/{COMMIT}/ofl/'
SOURCES=[('serif','notoserifsc','NotoSerifSC[wght].ttf','Editorial Serif SC'),('body','notosanssc','NotoSansSC[wght].ttf','Editorial Sans SC')]

def make(spec):
    role,folder,name,family=spec
    raw=ROOT/'.font-sources'/name
    raw.parent.mkdir(exist_ok=True)
    url=BASE+folder+'/'+urllib.parse.quote(name)
    if not raw.exists():urllib.request.urlretrieve(url,raw)
    f=instantiateVariableFont(TTFont(raw),{'wght':400},inplace=True)
    # Name derived static fonts distinctly, retaining original copyright and licence records.
    for n in f['name'].names:
        names={1:family,2:'Regular',3:family+' Regular 1.0',4:family+' Regular',6:family.replace(' ','')+'-Regular',16:family,17:'Regular'}
        if n.nameID in names:n.string=names[n.nameID].encode(n.getEncoding(),errors='replace')
    out=ROOT/'assets/fonts'/f'{role}.ttf'
    f.save(out)
    lic=ROOT/'assets/fonts'/('OFL-NotoSerifSC.txt' if role=='serif' else 'OFL-NotoSansSC.txt')
    urllib.request.urlretrieve(BASE+folder+'/OFL.txt',lic)
    return {'file':str(out.relative_to(ROOT)).replace('\\','/'),'family':family,'source':url,'upstream_commit':COMMIT,'source_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'modification':'Static weight 400, distinct family names; all original glyphs retained.','license':lic.name,'bytes':out.stat().st_size}

if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=2) as pool:manifest=list(pool.map(make,SOURCES))
    (ROOT/'assets/fonts/manifest.json').write_text(json.dumps(manifest,indent=2),'utf-8')
    print(json.dumps(manifest,indent=2))
