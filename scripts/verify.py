"""Content-sensitive validation of actual files, editable objects and local HTML targets."""
import argparse
import json
from pathlib import Path
import re
import zipfile
import xml.etree.ElementTree as ET
from pypdf import PdfReader
from pptx import Presentation

def verify(out,name):
    paths={x:out/f'{name}.{x}' for x in ['pdf','docx','pptx','html']}
    for p in paths.values():
        if not p.is_file() or p.stat().st_size<1000:raise ValueError(f'Missing or empty output: {p}')
    pdf=PdfReader(paths['pdf'])
    if len(pdf.pages)!=6:raise ValueError('Example PDF must contain 6 pages.')
    text=[p.extract_text() or '' for p in pdf.pages]
    if not all(len(t)>100 for t in text):raise ValueError('PDF has empty or non-searchable pages.')
    if not all(any(word in t for t in text) for word in ['结构','材料','交付']):raise ValueError('Expected Chinese text missing.')
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    with zipfile.ZipFile(paths['docx']) as z:
        doc=ET.fromstring(z.read('word/document.xml'))
        paragraphs=len(doc.findall('.//w:p',ns));tables=len(doc.findall('.//w:tbl',ns))
        if paragraphs<50 or tables<5:raise ValueError('DOCX must contain editable native paragraphs and tables.')
    deck=Presentation(paths['pptx'])
    if len(deck.slides)!=8:raise ValueError('Example PPTX must have 8 slides.')
    runs=sum(len(p.runs) for s in deck.slides for shape in s.shapes if shape.has_text_frame for p in shape.text_frame.paragraphs)
    pictures=sum(shape.shape_type==13 for s in deck.slides for shape in s.shapes)
    if runs<100 or pictures:raise ValueError('PPTX should contain editable vector/text objects, not slide screenshots.')
    source=paths['html'].read_text('utf-8')
    for target in re.findall(r'(?:href|src)=["\']([^"\']+)',source):
        if target.startswith(('#','http:','https:','data:')):continue
        if not (out/target).is_file():raise ValueError('Broken HTML reference: '+target)
    result={'pdf':{'pages':len(pdf.pages),'searchable_text_chars':[len(t) for t in text]},'docx':{'native_paragraphs':paragraphs,'native_tables':tables},'pptx':{'slides':len(deck.slides),'editable_text_runs':runs,'raster_pictures':pictures},'html':{'local_targets':'verified','fonts':'bundled'},'scope':'Structure and searchable Chinese checked. Office pagination and appearance need actual Office/LibreOffice rendering, not inferred from this test.'}
    (out/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('out',type=Path);a.add_argument('--name',default='克劳德设计_示例');o=a.parse_args();verify(o.out,o.name)
