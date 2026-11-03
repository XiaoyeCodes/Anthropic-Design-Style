"""Maintainer: compose the Markdown README and its bespoke, offline HTML reading edition.
Design method: huashu-md-html designer mode; established warm-paper editorial direction.
"""
from pathlib import Path
import html
import json
import shutil
from PIL import Image,ImageDraw,ImageFont

R=Path(__file__).resolve().parents[1]
REPO='https://github.com/XiaoyeCodes/Anthropic-Design-Style'
AGENT_PROMPT=f'请将 {REPO} 中的 anthropic-design-style 技能完整安装到当前智能体支持的 skills 目录，保留 SKILL.md、references、scripts、assets 和 agents。按 README 完成依赖安装与环境检查，再运行四格式示例验证；同名目录已存在时先比较，不覆盖我的修改。'
USE_PROMPT='请用 $anthropic-design-style 根据以下材料制作一份中文方案。先梳理结论、证据与行动，再确定品牌和当前主题的原创线稿；沿用暖纸、宋体、墨线与克制的陶土强调。分别为 HTML、A4 PDF、可编辑 DOCX、16:9 PPTX 设计阅读节奏。保留来源与假设标注，最后逐页检查实际渲染。材料如下：……'
INSTALL='npx skills add XiaoyeCodes/Anthropic-Design-Style --skill anthropic-design-style --agent codex -g -y'
FORMATS=[('HTML','连续阅读','沿思路展开内容；窄屏重排，宽图表独立横向阅读。'),('PDF','一页有一页的秩序','用版心、页边、字级和分页，让目光知道在哪里停顿。'),('DOCX','思考可以继续','原生段落与表格保持稳定层级，便于修改、审阅与协作。'),('PPTX','一屏讲清一个重点','按讲述拆分长文；观点放大，图文关系替你解释。')]

README=f'''<p align="center">
  <img src="docs/media/header.png" alt="克劳德设计：让内容找到合适的表达，Anthropic Design Style" width="100%">
</p>

# 克劳德设计 · Anthropic Design Style

**给思想，留出呼吸的空间。**

一套可安装的中文文档设计技能。用暖纸、宋体、墨线与克制的陶土色组织内容，让同一种设计语言，在 HTML、PDF、DOCX、PPTX 中形成各自的阅读节奏。

[![克劳德设计 · 设计风格与哲学，点击查看完整影片](docs/media/design-philosophy-full.gif)](docs/media/design-philosophy.mp4)

*40 秒完整循环 GIF · 点击查看有声影片 · [观看完整影片](docs/media/design-philosophy.mp4) · [HTML 阅读版](docs/readme.html)*

[快速安装](#快速安装) · [设计哲学](#设计哲学) · [四格式示例](#四格式示例) · [开始创作](#开始创作) · [本地运行](#本地运行)

## 设计哲学

先把思想理清，再决定页面的形状。设计从结论、证据和行动开始，以比例、疏密和清楚的层级，把信息变成可以阅读的表达。

- **内容先行。** 先理解用途与读者，再梳理结构；不为了留白删掉关键内容。
- **留白有度。** 暖纸为阅读留出时间，宋体建立层级，细线连接信息。
- **强调克制。** 陶土色只点亮关键词、编号和转折；正文与版心严格对齐。
- **图形有义。** 插画回应当前主题，图表回答具体问题；真实数据与演示假设清楚区分。

> 以阅读为尺度，让设计退后，让思想向前。

完整规范：[视觉系统](references/design-system.md) · [品牌与主题图形](references/art-direction.md) · [密度与版式库](references/layouts.md) · [格式与验收](references/formats.md)

## 一种语言，四种阅读节奏

| 格式 | 设计目的 | 呈现方式 |
| --- | --- | --- |
'''+''.join(f'| {f} | {t} | {d} |\n' for f,t,d in FORMATS)+f'''
四格式共用内容、字体、色彩和品牌；信息密度、顺序与页面节奏按载体重新组织。

## 快速安装

### 复制给你的智能体

把下面这句话发给 Codex、Claude Code 或其他能够读写本地文件的智能体：

```text
{AGENT_PROMPT}
```

### 一条命令安装到 Codex

```bash
{INSTALL}
```

也可以一次安装到多个智能体：

```bash
npx skills add XiaoyeCodes/Anthropic-Design-Style --skill anthropic-design-style --agent codex claude-code cursor -g -y
```

命令采用 [Skills CLI](https://github.com/vercel-labs/skills)，需要 Node.js 22.20+ 与 Git。安装完成后开启新的智能体会话。安装技能会放入规范与脚本；首次运行生成器时，再按下方步骤安装本地运行依赖。

不使用 CLI 时，可下载仓库 ZIP 并把完整目录放入智能体支持的 skills 路径，见 [安装指南](docs/INSTALL.md)。

## 开始创作

复制这段话，附上你的真实材料：

```text
{USE_PROMPT}
```

适合方案、研究报告、手册、提案与演示稿。新项目应重新确定品牌与主题插画，不能把案例“拾页”的标记或同一张封面套用到所有主题。

## 四格式示例

案例为「拾页 · AI 文档助手」：同一内容源制作 6 页 A4 阅读稿、8 张 16:9 演示稿、可编辑 Word 与离线网页。案例用于展示版式；其中时间比较是演示假设，六周排期是建议计划。

| 直接查看或下载 | 说明 |
| --- | --- |
| [HTML 示例](examples/showcase/克劳德设计_示例.html) | 离线字体、SVG 线稿、响应式阅读 |
| [PDF 示例](examples/showcase/克劳德设计_示例.pdf) | 6 页，可检索中文 |
| [DOCX 示例](examples/showcase/克劳德设计_示例.docx) | 原生段落与表格，可继续编辑 |
| [PPTX 示例](examples/showcase/克劳德设计_示例.pptx) | 8 张，原生文字、线条与可编辑图形 |
| [内容源 JSON](assets/example.json) | 章节、品牌、主题插画与图表数据 |
| [验证记录](examples/showcase/validation.json) | 页数、中文文本、原生对象与链接检查 |

![六页 A4 示例总览](examples/showcase/PDF全页预览.jpg)

![八张 16:9 示例总览](examples/showcase/PPT全页预览.jpg)

GitHub 源码页不会直接运行 HTML。下载后用浏览器打开，或在本地启动静态服务即可查看网页效果。

## 本地运行

环境：**Python 3.10+、Node.js 22.20+（含 npm）和 Git**。首次安装依赖需要联网，之后示例生成无需 API Key 或模型服务。

```bash
git clone {REPO}.git
cd Anthropic-Design-Style
python scripts/bootstrap.py
python scripts/run.py
```

macOS / Linux 若只有 `python3`，将命令里的 `python` 换成 `python3`。脚本自动使用仓库内 `.venv`，不用激活环境。

自定义内容源与输出位置：

```bash
python scripts/run.py --input assets/example.json --out out --name 我的方案
```

`out/` 中会生成四格式文件、品牌与图表素材、PDF 全页预览、PPT 矢量排版证明稿和 `validation.json`。详细依赖、字体与故障处理见 [安装指南](docs/INSTALL.md)。

### 运行与验收边界

- 仓库自带可再分发的中文字体、脚本与示例，不依赖其他技能或本机绝对路径。
- 为使 Office 的字体外观一致，请先安装 `assets/fonts/serif.ttf` 与 `assets/fonts/body.ttf`。PDF 和 HTML 直接使用随文件提供的字体。
- DOCX 正文及表格原生可编辑，插画为图片；PPTX 图表是可编辑形状，不是联动 Excel 数据的原生 Chart。
- 生成器是针对当前案例优化的 **6 页 A4 / 8 张 PPT 参考实现**。新文种、长文或不同数据范围，需要智能体按规范调整布局，不能直接当作通用分页引擎。
- 自动验证检查文件结构与中文文本；Office 的真实分页与外观仍须实际渲染确认。`PPTX_vector-proof.pdf` 是共享场景导出的证明稿，不冒充 Office 导出。

## 仓库里有什么

```text
SKILL.md                 智能体入口与工作方法
agents/                  Codex 展示名称与默认提示语
references/              视觉、主题图形、版式与验收规范
assets/                  内容源、场景图形与 OFL 中文字体
scripts/                 环境安装、四格式生成与验证
examples/showcase/       可直接下载的成品与预览
docs/                    安装指南、HTML 阅读版、影片与 GIF
```

## 来源与许可

这套设计从 **huashu-editorial-docs** 的编辑式文档规范发展而来；README 编排采用 **huashu-md-html** 的设计师模式，影片由 **huashu-motion** 制作。来源与实现边界见 [设计依据](references/sources.md) 和 [第三方说明](THIRD_PARTY.md)。

项目为独立设计方案，与 Anthropic 无隶属或背书关系。项目代码与原创文档采用 [MIT](LICENSE)；随附字体分别采用其 SIL OFL 许可。
'''
(R/'README.md').write_text(README,'utf-8')

# Typographic header: real type, restrained colour and a margin-note detail.
S=2;im=Image.new('RGB',(1600*S,500*S),'#FAF9F5');d=ImageDraw.Draw(im)
ser=lambda size:ImageFont.truetype(str(R/'assets/fonts/serif.ttf'),size*S)
body=lambda size:ImageFont.truetype(str(R/'assets/fonts/body.ttf'),size*S)
def text(x,y,t,size,color='#292923',font='serif'):
    d.text((x*S,y*S),t,font=ser(size) if font=='serif' else body(size),fill=color)
def line(x,y,xx,yy,color='#CFC7B9',w=1):d.line((x*S,y*S,xx*S,yy*S),fill=color,width=w*S)
d.rectangle((1060*S,0,1600*S,500*S),fill='#EFE9DE')
line(70,65,1530,65);text(72,28,'EDITORIAL STUDIES / 01',15,'#A9583E')
text(72,106,'克劳德设计',112);text(78,254,'ANTHROPIC DESIGN STYLE',27,'#A9583E')
text(78,334,'给思想，留出呼吸的空间。',29);line(80,408,985,408)
text(80,430,'HTML  /  PDF  /  DOCX  /  PPTX',18,'#68665F')
text(1120,110,'CONTENT',17,'#A9583E');text(1120,151,'先有内容，再有版式。',24)
line(1120,213,1530,213);text(1120,241,'SPACE',17,'#A9583E');text(1120,282,'疏密之间，自有秩序。',24)
line(1120,344,1530,344);text(1120,372,'FORM',17,'#A9583E');text(1120,413,'因阅读方式，重新设计。',24)
im.resize((1600,500),Image.Resampling.LANCZOS).save(R/'docs/media/header.png',optimize=True)

e=html.escape
def code(s):return '<div class="code-wrap"><button class="copy" type="button">复制</button><pre><code>'+e(s)+'</code></pre></div>'
formatrows=''.join(f'<tr><th scope="row">{f}</th><td><strong>{t}</strong><p>{desc}</p></td></tr>' for f,t,desc in FORMATS)
downloads=''.join(f'<a href="../examples/showcase/克劳德设计_示例.{ext}"><span>{label}</span><small>{detail}</small><b aria-hidden="true">↗</b></a>' for ext,label,detail in [('html','HTML','连续阅读'),('pdf','PDF','A4 阅读稿'),('docx','DOCX','原生段落与表格'),('pptx','PPTX','16:9 讲述稿')])
reading=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>克劳德设计 · Anthropic Design Style</title><meta name="description" content="暖纸、宋体、墨线与克制强调。为四种载体设计各自的阅读节奏。"><style>
@font-face{{font-family:EditorialSerif;src:url('../assets/fonts/serif.ttf')}}@font-face{{font-family:EditorialSans;src:url('../assets/fonts/body.ttf')}}
:root{{--paper:#FAF9F5;--wash:#EFE9DE;--ink:#292923;--muted:#68665F;--accent:#A9583E;--terra:#CC785C;--rule:#CFC7B9;--serif:EditorialSerif,Georgia,serif;--body:EditorialSans,sans-serif}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--paper);color:var(--ink);font:17px/1.85 var(--body)}}a{{color:var(--accent);text-underline-offset:5px;text-decoration-thickness:1px}}a:hover{{text-decoration-thickness:2px}}a:focus-visible,button:focus-visible{{outline:2px solid var(--accent);outline-offset:5px}}img{{max-width:100%;height:auto;display:block}}h1,h2,h3,blockquote{{font-family:var(--serif);font-weight:400}}h1{{font-size:clamp(40px,6vw,78px);line-height:1.3;letter-spacing:-2px;margin:25px 0}}h2{{font-size:34px;line-height:1.5;margin:12px 0 26px}}h3{{font-size:24px;margin:28px 0 14px}}p{{margin:0 0 1.2em}}header,footer,.wide{{max-width:1180px;margin:auto}}header{{padding:30px 34px;display:flex;justify-content:space-between;border-bottom:1px solid var(--rule);gap:18px}}.wordmark{{font:22px var(--serif);color:var(--ink);text-decoration:none}}nav{{display:flex;gap:28px;font-size:13px}}nav a{{color:var(--muted);text-decoration:none}}main{{max-width:820px;margin:0 auto;padding:0 28px}}.hero{{padding:70px 0 42px}}.eyebrow{{font:12px/1.5 var(--serif);letter-spacing:3px;color:var(--accent)}}.hero .lead{{font:27px/1.8 var(--serif);margin-top:28px}}.hero .intro{{color:var(--muted);max-width:650px}}.film{{margin:16px 0 64px}}.film img{{border:1px solid var(--rule)}}figcaption{{font-size:12px;color:var(--muted);margin-top:14px;display:flex;justify-content:space-between;gap:15px}}section{{border-top:1px solid var(--rule);padding:48px 0;scroll-margin-top:20px}}.principles{{counter-reset:item}}.principles article{{display:grid;grid-template-columns:42px 130px 1fr;gap:14px;padding:23px 0;border-bottom:1px solid var(--rule)}}.principles article:last-child{{border-bottom:0}}.principles .number{{font:20px var(--serif);color:var(--accent)}}.principles h3{{font-size:21px;margin:0}}.principles p{{font-size:15px;margin:0;color:var(--muted)}}blockquote{{font-size:29px;line-height:1.7;padding:12px 0 12px 30px;margin:35px 0 15px;border-left:1px solid var(--terra)}}.aside{{font-size:13px;color:var(--muted)}}table{{width:100%;border-collapse:collapse;margin:25px 0}}th,td{{text-align:left;padding:22px 16px;border-bottom:1px solid var(--rule);vertical-align:top}}th{{font:24px var(--serif);width:115px;color:var(--accent)}}td strong{{font:21px var(--serif)}}td p{{font-size:14px;color:var(--muted);margin:6px 0 0}}.code-wrap{{position:relative;margin:24px 0}}pre{{margin:0;background:var(--wash);padding:30px 25px;font:13px/1.85 Consolas,'SF Mono',monospace;white-space:pre-wrap;overflow-wrap:anywhere}}.copy{{position:absolute;right:12px;top:8px;background:var(--paper);color:var(--accent);border:1px solid var(--rule);font:12px var(--body);padding:4px 11px;cursor:pointer}}.downloads{{display:grid;grid-template-columns:1fr 1fr;gap:0 32px;margin:24px 0 35px}}.downloads a{{display:grid;grid-template-columns:90px 1fr 20px;align-items:center;gap:12px;padding:20px 0;border-bottom:1px solid var(--rule);text-decoration:none}}.downloads span{{font:24px var(--serif)}}.downloads small{{font-size:13px;color:var(--muted)}}.downloads b{{font-weight:400}}.gallery{{display:grid;grid-template-columns:1fr 1fr;gap:26px;margin:28px 0}}.gallery figcaption{{display:block}}figure{{margin:0}}.steps{{list-style:decimal;padding-left:25px}}.steps li{{padding-left:8px;margin:12px 0}}.links{{display:flex;flex-wrap:wrap;gap:8px 24px;font-size:14px}}footer{{padding:38px 34px 52px;border-top:1px solid var(--rule);font-size:12px;color:var(--muted);display:flex;justify-content:space-between;gap:35px}}footer p{{margin:0}}.foot-label{{font:18px var(--serif);color:var(--ink)}}.license{{font-size:13px;color:var(--muted)}}code{{font-size:.88em}}.readme-link{{display:inline-block;border-bottom:1px solid var(--accent);text-decoration:none}}
@media(max-width:720px){{header{{padding:24px}}nav{{gap:16px}}nav a:first-child{{display:none}}main{{padding:0 24px}}.hero{{padding:42px 0 25px}}.hero .lead{{font-size:20px}}h1{{letter-spacing:-1px}}h2{{font-size:28px}}section{{padding:36px 0}}.principles article{{grid-template-columns:32px 1fr;gap:12px}}.principles p{{grid-column:2}}.downloads{{grid-template-columns:1fr}}.gallery{{grid-template-columns:1fr}}blockquote{{font-size:24px}}footer{{padding:30px 24px;flex-direction:column;gap:20px}}th,td{{padding:18px 9px}}th{{font-size:20px;width:78px}}pre{{font-size:12px;padding:32px 17px 23px}}figcaption{{flex-wrap:wrap}}}}
@media(prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}@media print{{nav,.copy{{display:none}}body{{font-size:11pt}}main{{max-width:none}}.code-wrap,figure,table{{break-inside:avoid}}}}
</style></head><body><header><a class="wordmark" href="#top">克劳德设计</a><nav aria-label="章节导航"><a href="#philosophy">设计哲学</a><a href="#install">安装</a><a href="#examples">示例</a><a href="{REPO}">GitHub ↗</a></nav></header><main id="top">
<div class="hero"><div class="eyebrow">ANTHROPIC DESIGN STYLE / EDITORIAL STUDIES</div><h1>给思想，<br>留出呼吸的空间。</h1><p class="lead">暖纸、宋体、墨线与克制的陶土色。<br>一种设计语言，四种阅读节奏。</p><p class="intro">克劳德设计是一套可安装的中文文档设计技能。从内容结构出发，用比例、疏密与清楚的层级，把材料变成可以阅读的表达。</p><a class="readme-link" href="#install">开始使用　↓</a></div>
<figure class="film"><a href="media/design-philosophy.mp4"><img src="media/design-philosophy-full.gif" alt="克劳德设计：暖纸、墨线、留白，点击查看40秒影片" width="960" height="540"></a><figcaption><span>40 秒设计风格哲学片 / 完整循环 GIF</span><a href="media/design-philosophy.mp4">观看完整影片 ↗</a></figcaption></figure>
<section id="philosophy"><div class="eyebrow">01 / PHILOSOPHY</div><h2>先有内容，再有版式。</h2><div class="principles"><article><span class="number">01</span><h3>内容先行</h3><p>先理解用途与读者，再梳理结论、证据和行动；不为了留白删掉关键内容。</p></article><article><span class="number">02</span><h3>留白有度</h3><p>暖纸为阅读留出时间，宋体建立层级，细线连接信息。用疏密，组织目光的停顿。</p></article><article><span class="number">03</span><h3>强调克制</h3><p>陶土色只点亮关键词、编号和转折。正文与版心保持严格对齐。</p></article><article><span class="number">04</span><h3>图形有义</h3><p>插画回应当前主题，图表回答具体问题；真实数据与演示假设清楚区分。</p></article></div><blockquote>以阅读为尺度，<br>让设计退后，让思想向前。</blockquote><p class="aside">字、线与留白都要有理由。设计的精致，来自信息被认真组织。</p></section>
<section id="formats"><div class="eyebrow">02 / FOUR READING RHYTHMS</div><h2>同一份思想，因阅读而重组。</h2><table><caption class="aside">四格式共用内容、字体、色彩与品牌</caption><tbody>{formatrows}</tbody></table></section>
<section id="install"><div class="eyebrow">03 / START HERE</div><h2>把设计方法，交给你的智能体。</h2><h3>复制这一句话</h3><p>适用于 Codex、Claude Code 或其他能够读写本地文件的智能体。</p>{code(AGENT_PROMPT)}<h3>或在终端安装到 Codex</h3>{code(INSTALL)}<p class="aside">需要 Node.js 22.20+ 与 Git。安装后开启新会话；首次运行生成器时，另行安装本地依赖。<a href="INSTALL.md">完整安装指南 ↗</a></p><h3>给它一份真实材料</h3>{code(USE_PROMPT)}</section>
<section id="examples"><div class="eyebrow">04 / REAL OUTPUTS</div><h2>先看作品，再开始创作。</h2><p>「拾页 · AI 文档助手」是一份实际可下载的排版案例。六页 A4、八张 16:9 演示稿，与原生 Word、离线 HTML 一起呈现同一种设计语言。</p><div class="downloads">{downloads}</div><div class="gallery"><figure><a href="../examples/showcase/PDF全页预览.jpg"><img loading="lazy" src="../examples/showcase/PDF全页预览.jpg" alt="六页PDF全页预览"></a><figcaption>A4 / 六页阅读稿</figcaption></figure><figure><a href="../examples/showcase/PPT全页预览.jpg"><img loading="lazy" src="../examples/showcase/PPT全页预览.jpg" alt="八张PPT全页预览"></a><figcaption>16:9 / 八张讲述稿</figcaption></figure></div><p class="aside">案例品牌仅属于案例；其中时间比较是演示假设，排期是建议计划。新项目应重新创作主题插画。</p></section>
<section id="run"><div class="eyebrow">05 / LOCAL WORKFLOW</div><h2>下载之后，有一条完整的路径。</h2><p>Python 3.10+、Node.js 22.20+，无需 API Key。仓库自带可再分发的中文字体和全部示例依赖清单。</p>{code('git clone '+REPO+'.git\ncd Anthropic-Design-Style\npython scripts/bootstrap.py\npython scripts/run.py')}<p class="aside">macOS / Linux 可将 python 换成 python3。运行库仅安装到仓库内；首次依赖安装需要联网。</p><ol class="steps"><li>阅读规范，梳理内容与用途。</li><li>确定品牌，创作当前主题的图形。</li><li>按阅读、修改、讲述分别排版。</li><li>逐页检查实际渲染，再交付源文件。</li></ol><p class="license">参考生成器针对六页 A4 / 八张 PPT 案例优化。新文种、长文与不同数据范围需要调整布局。DOCX 正文与表格原生可编辑；PPTX 图表为可编辑形状。Office 字体外观须安装随附字体并实际渲染确认。</p></section>
<section><div class="eyebrow">06 / THE DESIGN DESK</div><h2>规范与来源，都留在桌面上。</h2><div class="links"><a href="../SKILL.md">智能体入口</a><a href="../references/design-system.md">视觉系统</a><a href="../references/art-direction.md">主题图形</a><a href="../references/layouts.md">版式库</a><a href="../references/formats.md">格式与验收</a><a href="../references/sources.md">设计依据</a></div><p class="license" style="margin-top:28px">设计从 huashu-editorial-docs 的规范发展而来。README 采用 huashu-md-html 的设计师模式，影片由 huashu-motion 制作。项目代码与原创文档采用 MIT；字体分别保留 SIL OFL 许可。</p></section>
</main><footer><p><span class="foot-label">克劳德设计</span><br>结构清楚 · 表达有据 · 因阅读而设计</p><p>独立设计方案，与 Anthropic 无隶属或背书关系。<br><a href="../README.md">Markdown README</a> · <a href="{REPO}">GitHub</a> · <a href="../LICENSE">MIT</a></p></footer><script>document.querySelectorAll('.copy').forEach(b=>b.addEventListener('click',async()=>{{const t=b.nextElementSibling.textContent;try{{await navigator.clipboard.writeText(t);b.textContent='已复制';}}catch(e){{const s=window.getSelection(),r=document.createRange();r.selectNodeContents(b.nextElementSibling);s.removeAllRanges();s.addRange(r);b.textContent='已选中';}}}}));</script></body></html>'''
(R/'docs/readme.html').write_text(reading,'utf-8')
print('README.md, docs/readme.html and the typographic header are ready.')
