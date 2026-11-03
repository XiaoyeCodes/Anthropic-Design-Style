"""Topic-directed editorial composition. Artwork must be supplied for the current brief."""
import argparse,json,os,subprocess,html,shutil
from pathlib import Path
from editorial_core import *
def table(s,rows,x,y,widths,rowh=43,size=10):
 for i,row in enumerate(rows):
  if i==0:s.rect(x,y,sum(widths),rowh,'wash')
  xx=x
  for j,t in enumerate(row):s.text(xx+9,y+11,t,size,'body','ink' if i==0 else 'muted',width=widths[j]-16,leading=size*1.5);xx+=widths[j]
  y+=rowh;s.line(x,y,x+sum(widths),y)
 return y
def arrow(s,x,y,xx,yy):
 s.line(x,y,xx,yy,'olive',1);s.line(xx-5,yy-4,xx,yy,'olive',1);s.line(xx-5,yy+4,xx,yy,'olive',1)
def visuals(d):
 v={};ch=d['charts']['time'];s=Scene(520,218,ch['title']+'。'+ch['source'])
 s.text(0,0,ch['title'],16,'serif');s.rect(320,7,10,7,'olive');s.text(335,3,'手工流程',9,'body','muted');s.rect(410,7,10,7,'accent');s.text(425,3,'辅助流程',9,'body','muted')
 for n in [0,5,10,15,20]:
  x=100+n*18;s.line(x,40,x,179,'rule',.45);s.text(x-3,185,str(n),8,'latin','muted')
 for i,label in enumerate(ch['labels']):
  y=42+i*35;s.text(0,y+3,label,10,'body')
  for j,key in enumerate(['before','after']):
   val=ch[key][i];s.rect(100,y+j*12,val*18,8,'olive' if j==0 else 'accent');s.text(105+val*18,y+j*12-2,str(val),8,'latin','muted')
 s.text(477,185,'分钟',8,'body','muted');s.text(0,207,ch['source'],8,'body','muted');v['time']=s
 s=Scene(520,200,'资料到交付的结构示意图，不代表真实系统实现');s.text(0,0,'材料、判断与交付之间的关系',16,'serif')
 for x,t,labels in [(0,'素材层',['会议记录','参考资料','需求说明']),(190,'组织层',['任务简报','章节提纲','引用索引']),(380,'交付层',['正文与图表','审阅记录','多格式文件'])]:
  s.text(x,37,t,11,'body','action');s.rect(x,61,138,112,'wash' if x!=190 else 'sage',r=8)
  for i,label in enumerate(labels):s.text(x+16,75+i*29,label,11,'body')
 arrow(s,145,116,181,116);arrow(s,335,116,371,116);s.text(0,188,'结构示意 / 用户确认提纲、核对出处、决定最终交付。',8,'body','muted');v['flow']=s
 s=Scene(520,180,'六周建议排期的甘特图');s.text(0,0,'六周交付路径',16,'serif')
 for i in range(6):s.text(146+i*61,37,f'W{i+1}',10,'latin','muted');s.line(137+i*61,58,137+i*61,143,'rule',.5)
 for i,(t,start,end) in enumerate([('内容与原型',0,2),('生成与导出',2,4),('试用与修整',4,6)]):
  y=63+i*30;s.text(0,y,t,11,'body');s.rect(139+start*61,y+1,(end-start)*61-7,17,'accent' if i==1 else 'olive',r=2)
 s.text(0,162,'建议排期 / 每个阶段以可审阅的产物结束。',8,'body','muted');v['gantt']=s
 ch=d['charts']['coverage'];s=Scene(520,215,ch['title']+'。'+ch['source']);s.text(0,0,ch['title'],16,'serif');s.text(456,4,'单位：项',8,'body','muted')
 for val in [0,10,20,30,40]:
  y=164-val*2.7;s.line(35,y,493,y,'rule',.5);s.text(5,y-5,str(val),8,'latin','muted')
 last=None
 for i,val in enumerate(ch['values']):
  x=42+i*88;y=164-val*2.7
  if last:s.line(*last,x,y,'action',1.7)
  s.rect(x-2.5,y-2.5,5,5,'action',r=2.5);s.text(x-6,y-21,str(val),10,'latin','action');s.text(x-8,177,ch['labels'][i],9,'latin','muted');last=(x,y)
 s.text(0,204,ch['source'],8,'body','muted');v['coverage']=s
 s=Scene(520,136,'内容到格式的工程结构示意');s.text(0,0,'一份内容源，四条呈现路径',16,'serif');s.rect(0,47,128,58,'sage',r=4);s.text(14,60,'结构化内容源',13,'serif');s.text(14,83,'章节 / 引用 / 图表',8,'body','muted')
 for i,label in enumerate(['PDF','DOCX','PPTX','HTML']):
  x=175+i*86
  if i==0:arrow(s,137,77,168,77)
  s.rect(x,47,72,58,'paper','rule',4);s.text(x+13,66,label,12,'latin','action')
 s.text(0,121,'共用内容和品牌；按阅读、讲述与浏览分别排版。',8,'body','muted');v['architecture']=s
 return v
def furniture(s,d,mark,n,total,label):
 s.rect(0,0,s.w,s.h);m=44 if s.w<700 else 42;s.embed(mark,m,20,26);s.text(m+34,19,d['identity']['name'],17,'serif');s.text(m+79,26,d['identity']['descriptor'],8,'body','muted');s.text(s.w-m-152,28,label,8,'latin','muted');s.line(m,59,s.w-m,59)
 s.line(m,s.h-44,s.w-m,s.h-44);s.text(m,s.h-29,d['identity']['name']+' / 概念方案 · 供讨论',8,'body','muted');s.text(s.w-m-43,s.h-29,f'{n:02d} / {total:02d}',9,'latin','action')
def chapter(s,ch):
 s.text(44,81,ch['eyebrow'],9,'latin','action');s.text(44,109,ch['title'],24,'serif',width=507,leading=33);s.text(44,157,ch['lead'],10.5,'body','muted',width=507,leading=17)
def callout(s,text,y=716):
 s.rect(44,y,507,44,'wash');s.line(44,y,44,y+44,'accent',2);s.text(58,y+12,text,12,'serif',width=479)
def a4(d,mark,hero,v):
 pages=[];s=Scene(595.28,841.89);furniture(s,d,mark,1,6,'PRODUCT BRIEF / V2.0');s.text(44,91,'PRODUCT PROPOSAL / 2026',10,'latin','action');s.text(44,127,d['title'],38,'serif');s.text(44,186,d['subtitle'].replace('\n',''),23,'serif');s.text(44,237,d['intro'],11,'body','muted',width=505);s.embed(hero,40,308,515)
 for i,(n,t,b) in enumerate([('01','结构先行','先确认提纲，再组织成稿。'),('02','表达有据','关键结论保留材料出处。'),('03','交付一致','一套品牌，四种文件。')]):
  x=44+i*173;s.line(x,638,x+156,638);s.text(x,653,n,14,'latin','action');s.text(x+28,652,t,14,'serif');s.text(x,683,b,9,'body','muted',width=151)
 s.text(44,747,d['note'],8,'body','muted',width=507);pages.append(s)
 for idx,ch in enumerate(d['chapters']):
  s=Scene(595.28,841.89);furniture(s,d,mark,idx+2,6,ch['eyebrow']);chapter(s,ch)
  if idx==0:
   for i,(t,b) in enumerate(ch['items']):
    y=217+i*58;s.text(44,y,f'0{i+1}',18,'latin','action');s.text(85,y,t,15,'serif');s.text(188,y+1,b,10,'body','muted',width=353,leading=16);s.line(85,y+45,551,y+45)
   s.embed(v['time'],44,419,507);s.text(44,665,'验证重点',11,'body','action');s.text(117,665,'用真实任务记录时间与改写次数，再评估辅助流程是否有效。',10,'body','muted',width=424)
  elif idx==1:
   for i,(t,b) in enumerate(ch['items']):
    x=44+i*130;s.rect(x,218,117,113,'wash' if i%2==0 else 'sage',r=6);s.text(x+12,230,f'0{i+1}',12,'latin','action');s.text(x+12,253,t,16,'serif');s.text(x+12,281,b,9,'body','muted',width=96,leading=14)
   s.embed(v['flow'],44,367,507);table(s,[['确认点','用户控制的决定'],['提纲确认','章节顺序与核心结论'],['交付确认','内容、来源和最终格式']],44,594,[110,397],32,9.5)
  elif idx==2:
   table(s,ch['table'],44,215,[90,237,180],43,10);s.embed(v['architecture'],44,514,507);s.text(44,677,'范围边界',11,'body','action');s.text(117,677,'首期先做单人完整路径；复杂协同留待验证后再扩展。',10,'body','muted',width=430)
  elif idx==3:
   s.embed(v['gantt'],44,219,507);s.line(44,407,551,407);s.embed(v['coverage'],44,431,507);s.text(44,672,'阶段产物',11,'body','action');s.text(117,672,'原型 → 可导出审阅稿 → 试用反馈与问题清单。',10,'body','muted',width=430)
  else:
   rows=[['维度','检查方法','交付证据']]+[[t,['核对原始来源','实际编辑与保存','逐页渲染与对照','打开四种成品'][i],['引用与假设清单','可编辑源文件','全页预览图','验收记录'][i]] for i,(t,b) in enumerate(ch['items'])];table(s,rows,44,219,[90,219,198],47,10);s.text(44,489,'从“看起来完成”到“可以交付”',19,'serif')
   for i,(t,b) in enumerate([('内容检查','事实、假设和待确认项分开，避免图表暗示未经验证的收益。'),('视觉检查','检查密度、对齐、字重和行首标点；空白应服务阅读节奏。'),('格式检查','核对字体替换、表格分页及不同阅读器的实际显示。')]):
    x=44+i*173;s.text(x,537,f'0{i+1}',15,'latin','action');s.text(x,566,t,13,'serif');s.text(x,596,b,10,'body','muted',width=148,leading=18)
  callout(s,ch['quote']);s.text(44,773,ch['caption'],8,'body','muted',width=507);pages.append(s)
 return pages
def slides(d,mark,hero,v):
 arr=[]
 def new(title,label,sub=''):
  s=Scene(960,540);furniture(s,d,mark,len(arr)+1,8,label);s.text(42,88,title,31,'serif',width=876);s.text(42,145,sub,16,'body','muted',width=876,leading=25);arr.append(s);return s
 s=new(d['title'],'PRODUCT BRIEF / V2.0');s.text(42,158,d['subtitle'],27,'serif',leading=41);s.text(42,266,d['intro'],17,'body','muted',width=374,leading=28);s.embed(hero,425,159,510);s.text(42,438,d['version'],10,'body','action')
 ch=d['chapters'][0];s=new(ch['title'],'01 / PURPOSE',ch['lead']);s.embed(hero,22,236,405)
 for i,(t,b) in enumerate(ch['items']):
  y=226+i*82;s.text(459,y,f'0{i+1}',22,'latin','action');s.text(504,y,t,21,'serif');s.text(504,y+33,b,16,'body','muted',width=397,leading=24);s.line(504,y+75,916,y+75)
 s=new('用假设提出问题，再用真实任务验证。','02 / HYPOTHESIS','下面的数据只用于演示，不代表产品已实现的节省效果。');s.embed(v['time'],45,220,635);s.rect(722,227,194,218,'wash',r=6);s.text(741,245,'如何验证',21,'serif');s.text(741,292,'选同类真实任务\n记录各阶段耗时\n核对产出质量\n同时记录修改次数',16,'body','muted',width=158,leading=33)
 ch=d['chapters'][1];s=new(ch['title'],'03 / EXPERIENCE',ch['lead']);s.embed(v['flow'],43,224,626)
 for i,(t,b) in enumerate(ch['items']):s.text(712,221+i*61,f'0{i+1}  {t}',18,'serif','action');s.text(712,249+i*61,b,13,'body','muted',width=202,leading=20)
 ch=d['chapters'][2];s=new(ch['title'],'04 / SCOPE',ch['lead']);table(s,ch['table'],42,218,[135,312,245],38,14);s.rect(765,218,151,227,'sage',r=6);s.text(784,239,'首期边界',20,'serif');s.text(784,284,'单人完整路径\n可审阅方案\n可编辑交付\n\n暂缓多人协同',14,'body','muted',leading=26)
 ch=d['chapters'][3];s=new('每两周交付一个可以讨论的结果。','05 / ROADMAP',ch['lead']);s.embed(v['gantt'],43,222,623)
 for i,r in enumerate(ch['items']):s.text(715,220+i*78,r[0],13,'body','action');s.text(715,244+i*78,r[1],19,'serif');s.text(715,274+i*78,['任务简报与原型','可导出审阅稿','试用反馈清单'][i],12,'body','muted')
 s=new('把验证工作放进排期。','06 / VALIDATION','以累计测试用例组织验证工作，计划值需随真实范围调整。');s.embed(v['coverage'],43,217,626);s.rect(721,230,195,219,'wash',r=6);s.text(740,250,'覆盖四个维度',20,'serif');s.text(740,300,'内容与出处\n编辑与版本\n布局与字体\n四格式打开检查',16,'body','muted',leading=32)
 ch=d['chapters'][4];s=new(ch['title'],'07 / DECISION',ch['lead'])
 for i,(t,b) in enumerate(ch['items']):
  x=42+i%2*450;y=221+i//2*108;s.line(x,y,x+414,y);s.text(x,y+17,f'0{i+1}',19,'latin','action');s.text(x+44,y+16,t,22,'serif');s.text(x+44,y+53,b,16,'body','muted',width=366,leading=24)
 s.text(42,465,ch['quote'],13,'serif','action');return arr
def main():
 a=argparse.ArgumentParser();a.add_argument('--input',type=Path,required=True);a.add_argument('--out',type=Path,required=True);a.add_argument('--font-dir',default=None);a.add_argument('--name',default='克劳德设计_示例');a.add_argument('--node',default='node');a.add_argument('--node-modules');o=a.parse_args();fonts(o.font_dir);d=json.loads(o.input.read_text(encoding='utf-8'));d['_output_stem']=o.name;base=o.input.resolve().parent
 if d.get('visuals',{}).get('topic')!=d['title']:raise ValueError('为当前主题新创作 visuals.hero，并使 visuals.topic 与 title 一致；不要复用无关样例插画。')
 mark=Scene.load(base/d['identity']['mark']);hero=Scene.load(base/d['visuals']['hero']);v=visuals(d);out=o.out.resolve();out.mkdir(parents=True,exist_ok=True);assets=out/'assets';assets.mkdir(exist_ok=True);(out/'内容源.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
 for source in [d['identity']['mark'],d['visuals']['hero']]:
  target=out/source;target.parent.mkdir(parents=True,exist_ok=True)
  if (base/source).resolve()!=target.resolve():shutil.copyfile(base/source,target)
 for key,scene in {'brand-mark':mark,'hero':hero,**v}.items():asset(scene,assets/key)
 shutil.copytree(Path(__file__).resolve().parents[1]/'assets'/'fonts',assets/'fonts',dirs_exist_ok=True)
 pages=a4(d,mark,hero,v);pdf(pages,out/(o.name+'.pdf'),d['title']);contact(render(out/(o.name+'.pdf'),out/'previews','pdf'),out/'PDF全页预览.jpg');deck=slides(d,mark,hero,v);ppt(deck,out/(o.name+'.pptx'));pdf(deck,out/'PPTX_vector-proof.pdf',d['title']);contact(render(out/'PPTX_vector-proof.pdf',out/'previews','ppt'),out/'PPT全页预览.jpg')
 from editorial_html import export_html
 export_html(d,mark,hero,v,out)
 env=os.environ.copy()
 if o.node_modules:env['NODE_PATH']=o.node_modules
 subprocess.run([o.node,str(Path(__file__).with_name('build-docx.cjs')),str(out/'内容源.json'),str(out)],env=env,check=True);print(json.dumps({'pdf_pages':len(pages),'ppt_slides':len(deck),'hero':d['visuals']['hero'],'graphs':list(v)},ensure_ascii=False))
if __name__=='__main__':main()
