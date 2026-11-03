"""Verify imports, all bundled assets, node/docx and actual font glyph coverage."""
import importlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def main():
    for module in ['reportlab', 'PIL', 'pptx', 'pypdfium2', 'pypdf']:
        importlib.import_module(module)
        print('OK Python: '+module)
    for name in ['serif.ttf','body.ttf','OFL-NotoSerifSC.txt','OFL-NotoSansSC.txt']:
        if not (ROOT/'assets/fonts'/name).is_file():
            raise SystemExit('Missing bundled font: '+name)
    from reportlab.pdfbase.ttfonts import TTFont
    for name in ['serif','body']:
        font=TTFont(name,str(ROOT/'assets/fonts'/f'{name}.ttf'))
        if not all(ord(c) in font.face.charToGlyph for c in '克劳德设计暖纸墨线阅读中文'):
            raise SystemExit('Chinese glyphs missing from '+name)
    print('OK Bundled Chinese fonts')
    node=shutil.which('node')
    if not node:
        raise SystemExit('Node.js 22.20+ is required.')
    version=tuple(int(n) for n in subprocess.check_output([node,'--version'],text=True).strip().lstrip('v').split('.'))
    if version<(22,20,0):raise SystemExit('Node.js 22.20+ is required; check PATH.')
    subprocess.run([node,'-e',"require('docx'); console.log('OK Node: docx')"],cwd=ROOT,check=True)
    d=json.loads((ROOT/'assets/example.json').read_text('utf-8'))
    for key in [d['identity']['mark'],d['visuals']['hero']]:
        assert (ROOT/'assets'/key).is_file(),key
    print('OK Topic scene sources; no external skill is required to run the example.')

if __name__ == '__main__':
    main()
