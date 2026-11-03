const fs=require('fs'),path=require('path');
const {Document,Packer,Paragraph,TextRun,HeadingLevel,Table,TableRow,TableCell,WidthType,ShadingType,BorderStyle,Header,Footer,PageNumber,TabStopType,SectionType,ImageRun}=require('docx');
const d=JSON.parse(fs.readFileSync(process.argv[2],'utf8')),out=process.argv[3];
const C={ink:'292923',muted:'68665F',action:'A9583E',rule:'CFC7B9',wash:'EFE9DE'};
const run=(text,size=21,font='Editorial Sans SC',color=C.ink)=>new TextRun({text,size,font,color});
const p=(text,size=21,font='Editorial Sans SC',color=C.ink,after=130,before=0,extra={})=>new Paragraph({spacing:{before,after,line:Math.round(size*15),lineRule:'exact'},...extra,children:[run(text,size,font,color)]});
const line={style:BorderStyle.SINGLE,size:4,color:C.rule},none={style:BorderStyle.NONE,size:0};
const img=(name,width,height,after=200)=>new Paragraph({spacing:{before:150,after},children:[new ImageRun({type:'png',data:fs.readFileSync(path.join(out,'assets',name+'.png')),transformation:{width,height},altText:{title:name,description:name==='hero'?d.visuals.brief:'文档内容图示 '+name,name}})]});
const tbl=(rows,widths,header=true)=>new Table({width:{size:10146,type:WidthType.DXA},columnWidths:widths,borders:{top:none,bottom:line,left:none,right:none,insideHorizontal:line,insideVertical:none},rows:rows.map((r,i)=>new TableRow({tableHeader:header&&i===0,cantSplit:true,children:r.map((t,j)=>new TableCell({width:{size:widths[j],type:WidthType.DXA},margins:{top:160,bottom:160,left:120,right:120},shading:{type:ShadingType.CLEAR,fill:header&&i===0?C.wash:'FAF9F5'},children:[p(t,20,'Editorial Sans SC',i===0&&header?C.ink:C.muted,0)]}))}))});
function header(label){return new Header({children:[new Paragraph({tabStops:[{type:TabStopType.RIGHT,position:10146}],border:{bottom:line},spacing:{after:200},children:[new ImageRun({type:'png',data:fs.readFileSync(path.join(out,'assets/brand-mark.png')),transformation:{width:28,height:28}}),run('  '+d.identity.name,30,'Editorial Serif SC'),run('  '+d.identity.descriptor,17,'Editorial Sans SC',C.muted),run('\t'+label,16,'Editorial Serif SC',C.muted)]})]});}
function footer(){return new Footer({children:[new Paragraph({tabStops:[{type:TabStopType.RIGHT,position:10146}],border:{top:line},spacing:{before:120},children:[run(d.identity.name+' / 概念方案 · 供讨论',16,'Editorial Sans SC',C.muted),run('\t',16),new TextRun({children:[PageNumber.CURRENT,' / ',PageNumber.TOTAL_PAGES],size:18,font:'Editorial Serif SC',color:C.action})]})]});}
const section=(children,label)=>({properties:{type:SectionType.NEXT_PAGE,page:{size:{width:11906,height:16838},margin:{top:1500,bottom:1000,left:880,right:880,header:440,footer:400}}},headers:{default:header(label)},footers:{default:footer()},children});
const callout=t=>p(t,25,'Editorial Serif SC',C.ink,160,190,{shading:{type:ShadingType.CLEAR,fill:C.wash},border:{left:{style:BorderStyle.SINGLE,size:12,color:'CC785C',space:10}},indent:{left:170,right:120}});
const cover=[p('PRODUCT PROPOSAL / 2026',20,'Editorial Serif SC',C.action,280),p(d.title,72,'Editorial Serif SC',C.ink,240),p(d.subtitle.replace('\n',''),42,'Editorial Serif SC',C.ink,200),p(d.intro,22,'Editorial Sans SC',C.muted,160),img('hero',660,385,230),tbl([['01 / 结构先行','02 / 表达有据','03 / 交付一致'],['先确认提纲，再成稿。','关键结论保留出处。','一套品牌，四种文件。']],[3382,3382,3382]),p(d.version,17,'Editorial Sans SC',C.action,110,180),p(d.note,16,'Editorial Sans SC',C.muted)];
const sections=[section(cover,'PRODUCT BRIEF / V2.0')];
for(let i=0;i<d.chapters.length;i++){
 const ch=d.chapters[i],kids=[p(ch.eyebrow,18,'Editorial Serif SC',C.action,190),new Paragraph({heading:HeadingLevel.HEADING_1,keepNext:true,spacing:{after:190,line:680,lineRule:'exact'},children:[run(ch.title,46,'Editorial Serif SC')]}),p(ch.lead,21,'Editorial Sans SC',C.muted,320)];
 if(i===0){
  kids.push(tbl([['价值主张','具体行为'],...ch.items],[2200,7946]));kids.push(img('time',660,277));kids.push(tbl([['演示数据 / 分钟','手工流程','辅助流程'],...d.charts.time.labels.map((t,j)=>[t,String(d.charts.time.before[j]),String(d.charts.time.after[j])])],[4800,2673,2673]));kids.push(p('验证重点：记录真实任务耗时与改写次数，同时核对产出质量。',20,'Editorial Sans SC',C.muted,180,180));
 }else if(i===1){
  kids.push(tbl([['步骤','用户操作'],...ch.items.map((r,j)=>['0'+(j+1)+' / '+r[0],r[1]])],[2200,7946]));kids.push(img('flow',660,254));kids.push(tbl([['确认点','用户决定'],['提纲确认','章节顺序、核心结论及待补充信息'],['交付确认','正文内容、材料出处及最终格式']],[2200,7946]));
 }else if(i===2){
  kids.push(tbl(ch.table,[1900,4746,3500]));kids.push(img('architecture',660,173));kids.push(p('范围边界',28,'Editorial Serif SC',C.ink,130,160));kids.push(p('首期先完成单人路径，保留内容和来源。复杂多人协同与自动发布，待验证基本流程后再扩展。',21,'Editorial Sans SC',C.muted,180));kids.push(tbl([['扩展条件','需要回答的问题'],['增加文种','新文种的结构是否已被真实任务验证？'],['加入协同','单人流程是否稳定，版本责任能否明确？']],[2500,7646]));
 }else if(i===3){
  kids.push(img('gantt',660,228,120));kids.push(img('coverage',660,273,180));kids.push(tbl([['阶段','关键产物'],['01—02 周','任务简报与可讨论原型'],['03—04 周','可编辑、可导出的审阅稿'],['05—06 周','试用反馈与排版问题清单']],[2200,7946]));
 }else{
  kids.push(tbl([['维度','检查方法','交付证据'],...ch.items.map((r,j)=>[r[0],['核对原始来源','实际编辑与保存','逐页渲染与对照','打开四种成品'][j],['引用与假设清单','可编辑源文件','全页预览图','验收记录'][j]])],[2000,4073,4073]));
  kids.push(p('从“看起来完成”到“可以交付”',34,'Editorial Serif SC',C.ink,200,330));
  for(const [title,body] of [['内容检查','事实、假设和待确认项分开，避免图表暗示未经验证的收益。'],['视觉检查','检查密度、对齐、字号与行首标点；空白应服务阅读节奏。'],['格式检查','核对字体替换、表格分页和不同阅读器的实际显示。']]){kids.push(p(title,26,'Editorial Serif SC',C.action,100,130));kids.push(p(body,21,'Editorial Sans SC',C.muted,170));}kids.push(tbl([['发现的问题','建议处理'],['来源缺失或结论存疑','标记待确认，不自动补成事实'],['内容溢出或字体替换','调整版式，重新渲染受影响页面'],['格式可以打开但无法编辑','恢复原生文字与表格后重新交付']],[3600,6546]));
 }
 kids.push(callout(ch.quote));kids.push(p(ch.caption,17,'Editorial Sans SC',C.muted,0));sections.push(section(kids,ch.eyebrow));
}
const doc=new Document({title:d.title,creator:'克劳德设计',description:'V2.0 编辑式布局、统一品牌与主题插画',background:{color:'FAF9F5'},styles:{default:{document:{run:{font:'Editorial Sans SC',size:21,color:C.ink},paragraph:{spacing:{line:320},widowControl:true}}},paragraphStyles:[{id:'Heading1',name:'heading 1',basedOn:'Normal',next:'Normal',quickFormat:true,run:{font:'Editorial Serif SC',size:46},paragraph:{outlineLevel:0,keepNext:true}}]},sections});
Packer.toBuffer(doc).then(b=>fs.writeFileSync(path.join(out,(d._output_stem||'克劳德设计_示例')+'.docx'),b));
