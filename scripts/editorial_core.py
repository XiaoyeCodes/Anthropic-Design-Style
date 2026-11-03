"""Small vector scene renderer shared by PDF, HTML and editable PowerPoint."""
import json, math, html
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from PIL import Image,ImageDraw
import pypdfium2 as pdfium
from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE,MSO_CONNECTOR
from pptx.oxml.ns import qn
from pptx.oxml.xmlchemy import OxmlElement
C={'paper':'FAF9F5','wash':'EFE9DE','ink':'292923','muted':'68665F','accent':'CC785C','action':'A9583E','rule':'CFC7B9','olive':'898875','sage':'E7E8DE','rose':'EFDED4'}
def color(c):return C.get(c,c)
FONT_FAMILIES={'serif':'Editorial Serif SC','body':'Editorial Sans SC','latin':'Editorial Serif SC'}
def fonts(path=None):
 folder=Path(path) if path else Path(__file__).resolve().parents[1]/'assets'/'fonts'
 for n,f in [('serif','serif.ttf'),('body','body.ttf'),('latin','serif.ttf')]:
  target=folder/f
  if not target.is_file():raise FileNotFoundError(f'Missing font {target}; keep the complete assets/fonts directory.')
  pdfmetrics.registerFont(TTFont(n,str(target),subfontIndex=0))
class Scene:
 def __init__(self,w,h,label=''):self.w=w;self.h=h;self.ops=[];self.label=label
 def rect(self,x,y,w,h,fill='paper',stroke=None,r=0):self.ops.append(['rect',x,y,w,h,color(fill),color(stroke),r])
 def line(self,x,y,xx,yy,c='rule',width=.7):self.ops.append(['line',x,y,xx,yy,color(c),width])
 def path(self,pts,c='ink',width=1.3,fill=None):self.ops.append(['path',pts,color(c),width,color(fill)])
 def text(self,x,y,t,size=11,font='body',c='ink',width=None,leading=None):
  face=pdfmetrics.getFont(font).face
  missing=sorted({ch for ch in str(t) if not ch.isspace() and ord(ch) not in face.charToGlyph})
  if missing:raise ValueError('Font '+font+' has no glyphs for: '+''.join(missing)+'. Supply a suitable font instead of shipping boxes.')
  leading=leading or size*1.6;lines=[]
  for para in str(t).split('\n'):
   cur=''
   for ch in para:
    if width and pdfmetrics.stringWidth(cur+ch,font,size)>width:
     if ch in '，。；：！？、）》】”’' and len(cur)>1:lines.append(cur[:-1]);cur=cur[-1]+ch
     else:lines.append(cur);cur=ch
    else:cur+=ch
   lines.append(cur)
  for i,t in enumerate(lines):self.ops.append(['text',x,y+i*leading,t,size,font,color(c)])
  return y+len(lines)*leading
 def embed(self,scene,x,y,w):self.ops.append(['group',x,y,w,scene])
 def save(self,p):
  Path(p).write_text(json.dumps({'width':self.w,'height':self.h,'label':self.label,'ops':self.ops},ensure_ascii=False,indent=2),encoding='utf-8')
 @classmethod
 def load(cls,p):
  d=json.loads(Path(p).read_text(encoding='utf-8'));s=cls(d['width'],d['height'],d.get('label',''));s.ops=d['ops'];return s
def flat(s,x=0,y=0,k=1):
 for a in s.ops:
  op=a[0]
  if op=='group':yield from flat(a[4],x+a[1]*k,y+a[2]*k,k*a[3]/a[4].w)
  elif op=='rect':yield [op,x+a[1]*k,y+a[2]*k,a[3]*k,a[4]*k,a[5],a[6],a[7]*k]
  elif op=='line':yield [op,x+a[1]*k,y+a[2]*k,x+a[3]*k,y+a[4]*k,a[5],a[6]*k]
  elif op=='text':yield [op,x+a[1]*k,y+a[2]*k,a[3],a[4]*k,a[5],a[6]]
  elif op=='path':yield [op,[[p[0]]+[v*k+(x if j%2==0 else y) for j,v in enumerate(p[1:])] for p in a[1]],a[2],a[3]*k,a[4]]
def draw(s,c):
 for a in flat(s):
  op=a[0]
  if op=='rect':
   _,x,y,w,h,f,st,r=a;c.setFillColor(HexColor('#'+f));c.setStrokeColor(HexColor('#'+(st or f)));c.setLineWidth(.7);c.roundRect(x,s.h-y-h,w,h,r,fill=1,stroke=bool(st))
  elif op=='line':
   _,x,y,xx,yy,co,sw=a;c.setStrokeColor(HexColor('#'+co));c.setLineWidth(sw);c.line(x,s.h-y,xx,s.h-yy)
  elif op=='text':
   _,x,y,t,sz,fo,co=a;c.setFillColor(HexColor('#'+co));c.setFont(fo,sz);c.drawString(x,s.h-y-sz,t)
  elif op=='path':
   _,pts,co,sw,fill=a;p=c.beginPath()
   for b in pts:
    if b[0]=='M':p.moveTo(b[1],s.h-b[2])
    elif b[0]=='L':p.lineTo(b[1],s.h-b[2])
    elif b[0]=='C':p.curveTo(b[1],s.h-b[2],b[3],s.h-b[4],b[5],s.h-b[6])
    elif b[0]=='Z':p.close()
   c.setStrokeColor(HexColor('#'+co));c.setLineWidth(sw)
   if fill:c.setFillColor(HexColor('#'+fill))
   c.drawPath(p,stroke=1,fill=bool(fill))
def svg(s):
 b=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s.w} {s.h}" role="img" aria-label="{html.escape(s.label)}">']
 for a in flat(s):
  if a[0]=='rect':_,x,y,w,h,f,st,r=a;b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#{f}" stroke="{("#"+st) if st else "none"}"/>')
  elif a[0]=='line':_,x,y,xx,yy,co,sw=a;b.append(f'<path d="M{x},{y} L{xx},{yy}" stroke="#{co}" stroke-width="{sw}"/>')
  elif a[0]=='path':
   _,pts,co,sw,f=a;dd=' '.join(p[0]+' '.join(str(v) for v in p[1:]) for p in pts);b.append(f'<path d="{dd}" stroke="#{co}" stroke-width="{sw}" fill="{("#"+f) if f else "none"}" stroke-linejoin="round" stroke-linecap="round"/>')
  elif a[0]=='text':
   _,x,y,t,sz,fo,co=a;font=FONT_FAMILIES[fo];b.append(f'<text x="{x}" y="{y+sz}" fill="#{co}" font-size="{sz}" font-family="{font}">{html.escape(t)}</text>')
 return ''.join(b)+'</svg>'
def asset(s,path):
 p=Path(path);p.with_suffix('.svg').write_text(svg(s),encoding='utf-8');c=canvas.Canvas(str(p.with_suffix('.pdf')),pagesize=(s.w,s.h));draw(s,c);c.save();doc=pdfium.PdfDocument(str(p.with_suffix('.pdf')));doc[0].render(scale=3,fill_color=(250,249,245,255)).to_pil().convert('RGB').save(p.with_suffix('.png'))
def pdf(pages,path,title):
 c=canvas.Canvas(str(path),pagesize=(pages[0].w,pages[0].h));c.setTitle(title)
 for s in pages:c.setPageSize((s.w,s.h));draw(s,c);c.showPage()
 c.save()
def render(p,out,prefix):
 out=Path(out);out.mkdir(exist_ok=True);doc=pdfium.PdfDocument(str(p));files=[]
 for i in range(len(doc)):
  f=out/f'{prefix}-{i+1:02}.png';doc[i].render(scale=1.5).to_pil().convert('RGB').save(f);files.append(f)
 return files
def contact(files,p):
 wide=Image.open(files[0]).width>Image.open(files[0]).height;th=240 if wide else 525;im=Image.new('RGB',(1122,math.ceil(len(files)/3)*th),'#e6e1d7')
 for i,f in enumerate(files):
  a=Image.open(f).convert('RGB');a.thumbnail((350,th-30));x=i%3*374;y=i//3*th;im.paste(a,(x+(374-a.width)//2,y+9));ImageDraw.Draw(im).text((x+12,y+th-17),f.stem,fill='#555')
 im.save(p)
def ppt(pages,path):
 prs=Presentation();prs.slide_width=Pt(pages[0].w);prs.slide_height=Pt(pages[0].h)
 for s in pages:
  sl=prs.slides.add_slide(prs.slide_layouts[6])
  for a in flat(s):
   op=a[0];sh=None
   if op=='text':
    _,x,y,t,sz,fo,co=a;sh=sl.shapes.add_textbox(Pt(x),Pt(y-1),Pt(s.w-x-24),Pt(sz*1.7));tf=sh.text_frame;tf.word_wrap=False;tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0;p=tf.paragraphs[0];p.text=t;p.font.name=FONT_FAMILIES[fo];p.font.size=Pt(sz);p.font.color.rgb=RGBColor.from_string(co);ea=OxmlElement('a:ea');ea.set('typeface',FONT_FAMILIES[fo]);p._p.get_or_add_pPr().get_or_add_defRPr().append(ea)
   elif op=='rect':
    _,x,y,w,h,f,st,r=a;sh=sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if r else MSO_SHAPE.RECTANGLE,Pt(x),Pt(y),Pt(w),Pt(h));sh.fill.solid();sh.fill.fore_color.rgb=RGBColor.from_string(f)
    if st:sh.line.color.rgb=RGBColor.from_string(st);sh.line.width=Pt(.7)
    else:sh.line.fill.background()
   elif op=='line':
    _,x,y,xx,yy,co,sw=a;sh=sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,Pt(x),Pt(y),Pt(xx),Pt(yy));sh.line.color.rgb=RGBColor.from_string(co);sh.line.width=Pt(sw)
   elif op=='path':
    # Native freeform; sample Bezier segments so artwork remains editable.
    pts=[];closed=False
    for b in a[1]:
     if b[0] in ['M','L']:pts.append((b[1],b[2]))
     elif b[0]=='C':
      x0,y0=pts[-1]
      for i in range(1,17):
       t=i/16;u=1-t;pts.append((u**3*x0+3*u*u*t*b[1]+3*u*t*t*b[3]+t**3*b[5],u**3*y0+3*u*u*t*b[2]+3*u*t*t*b[4]+t**3*b[6]))
     elif b[0]=='Z':closed=True
    if len(pts)>1:
     fb=sl.shapes.build_freeform(pts[0][0],pts[0][1],scale=12700);fb.add_line_segments(pts[1:],close=closed);sh=fb.convert_to_shape();sh.line.color.rgb=RGBColor.from_string(a[2]);sh.line.width=Pt(a[3]);
     if a[4]:sh.fill.solid();sh.fill.fore_color.rgb=RGBColor.from_string(a[4])
     else:sh.fill.background()
   if sh is not None:
    st=sh._element.find(qn('p:style'))
    if st is not None:sh._element.remove(st)
  sl.notes_slide.notes_text_frame.text=s.label
 prs.save(path)
