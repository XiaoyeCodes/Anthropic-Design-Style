---
name: anthropic-design-style
description: 用暖纸色、陶土橙、宋体标题、墨线与编辑式留白制作中文方案、报告、手册及演示文稿。按阅读场景重新设计 HTML、PDF、DOCX、PPTX。用户提到克劳德设计、Anthropic 灵感排版、雅致文档或跨格式文档设计时使用。
metadata:
  display_name: 克劳德设计
  version: 1.0.0
---

# 克劳德设计

以阅读为尺度，让设计退后，让思想向前。这是独立的编辑式中文文档设计方案，灵感来自暖纸、书页与克制表达，不是 Anthropic 官方模板。

## 决策顺序

1. 保留用户的内容、用途、读者、篇幅和格式要求。先梳理结论、证据、行动，再决定页数。示例内容、假设数据和真实成果明确区分。
2. 读取[视觉规范](references/design-system.md)与[品牌与主题图形](references/art-direction.md)。暖纸承载阅读，宋体建立层级，细线连接信息，陶土色只点亮重点。已有品牌规范优先。
3. 每个新项目先确定品牌、字标与主题插画。四格式共享同一品牌；新主题重新构思图形。案例“拾页”和 AI 文档助手插画只属于该案例，禁止套用到所有主题。
4. 读取[密度与版式库](references/layouts.md)。按内容混用图文、图表、表格、步骤、架构、路线图和结论页。留白是阅读停顿，不用编造数据或无意义装饰填空。
5. 按[格式与验收](references/formats.md)分别设计：HTML 连续阅读，A4 PDF 从容阅读，DOCX 保持稳定可编辑的内容层级，16:9 PPTX 按讲述拆分观点。不以整页截图冒充可编辑文档。
6. 交付前实际打开文件并渲染所有页面，检查中文、溢出、分页、表格、统一品牌、主题图形和移动端。使用[质量清单](references/quality-checklist.md)，区分结构验证、实际渲染和审美观察。

## 自包含参考实现

本仓库包含所有脚本、中文字体、规范和示例。不要求另外安装 docx、theme-factory、canvas-design 技能。需要 Python 3.10+ 和 Node.js 22.20+；无 API Key 和模型服务依赖。

在技能根目录首次运行：

```bash
python scripts/bootstrap.py
python scripts/run.py
```

macOS / Linux 可用 python3。bootstrap 仅创建本目录的 .venv 与 node_modules；run 自动使用该环境，输出到 out/，不必激活虚拟环境。异常先用 .venv 中的 Python 运行 scripts/doctor.py，参见[安装指南](docs/INSTALL.md)。

自定义参考内容：

```bash
python scripts/run.py --input /path/to/content.json --out /path/to/output --name 项目名称
```

输入必须带 identity 与 visuals，visuals.topic 等于 title。主题场景路径相对内容 JSON 解析，字段见 art-direction.md。

**参考生成器针对六页 A4、八张 PPT 案例优化，不是任意长文的通用分页器。** 新文种、长文、不同图表范围和复杂内容，须由智能体按规范调整或重新编写布局，再验证。不要只换标题填入固定版式。

## 交付与边界

- PDF：嵌入中文字体、可检索文本、逐页预览。
- DOCX：原生段落、标题、表格与页眉页脚；插画及图表为图片，相关数值提供原生表格。
- PPTX：原生文字、线条、图形和可编辑自由曲线。示例图表是形状，不是联动 Excel 的原生 Chart。
- HTML：语义正文、离线字体、SVG 线稿和窄屏重排；下载链接必须对应实际文件。

verify.py 检查可检索文本、原生对象、页数和本地引用，不能代替 Office 实际渲染。Windows 有 Office 时可运行 scripts/render-office.ps1 -OutputDir <目录>；其他系统使用可用阅读器或 LibreOffice 导出并检查。为统一 Office 字体，应安装 assets/fonts 中两款 OFL 字体。

设计依据见[sources.md](references/sources.md)。示例、安装与影片见[README](README.md)。
