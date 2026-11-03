"""Check distributable completeness and local links; exclude generated environments."""
import json
from pathlib import Path
import re
import urllib.parse

R=Path(__file__).resolve().parents[1]
required=['SKILL.md','agents/openai.yaml','README.md','docs/readme.html','docs/INSTALL.md','requirements.txt','package.json','package-lock.json','assets/fonts/serif.ttf','assets/fonts/body.ttf','assets/fonts/manifest.json','docs/media/header.png','docs/media/design-philosophy-full.gif','docs/media/design-philosophy.mp4','examples/showcase/克劳德设计_示例.pdf','examples/showcase/克劳德设计_示例.docx','examples/showcase/克劳德设计_示例.pptx','examples/showcase/克劳德设计_示例.html','LICENSE','THIRD_PARTY.md']
for f in required:
    assert (R/f).is_file(), 'Missing: '+f
skill=(R/'SKILL.md').read_text('utf-8')
assert re.search(r'^name: anthropic-design-style$',skill,re.M)
assert '../docx/SKILL.md' not in skill
links=0
for f in [R/'README.md',R/'SKILL.md',R/'docs/readme.html',R/'docs/INSTALL.md']:
    s=f.read_text('utf-8')
    # Ignore fenced shell/code examples before validating Markdown relative links.
    s=re.sub(r'```.*?```','',s,flags=re.S)
    targets=re.findall(r'\]\(([^)]+)\)',s)+re.findall(r'(?:src|href)="([^"]+)"',s)
    for t in targets:
        if t.startswith(('http:','https:','#','data:')):continue
        t=urllib.parse.unquote(t.split('#')[0])
        assert (f.parent/t).exists(), f'Broken reference in {f.relative_to(R)}: {t}'
        links+=1
for name in ['design-system.md','art-direction.md','formats.md','layouts.md','quality-checklist.md','sources.md']:
    assert (R/'references'/name).exists(),name
for n in json.loads((R/'assets/fonts/manifest.json').read_text('utf-8')):
    import hashlib
    assert hashlib.sha256((R/n['file']).read_bytes()).hexdigest()==n['sha256'],n['file']
print(f'Package complete: {len(required)} required entries, {links} local links, font hashes and standalone skill name verified.')
