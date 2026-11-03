# 安装与运行

## 安装到智能体

推荐在终端使用 Skills CLI（Node.js 22.20+ 与 Git）：

```bash
npx skills add XiaoyeCodes/Anthropic-Design-Style --skill anthropic-design-style --agent codex -g -y
```

--agent 可改为 claude-code 或 cursor，也可一次填写多个名称。安装只是复制技能文件，生成器的 Python / Node 依赖需要另外安装。

Codex 当前用户级技能目录为 ~/.agents/skills，项目级为 .agents/skills。也可把完整仓库克隆到该目录：

```bash
git clone https://github.com/XiaoyeCodes/Anthropic-Design-Style.git ~/.agents/skills/anthropic-design-style
```

Windows PowerShell：

```powershell
$skillRoot = Join-Path $env:USERPROFILE '.agents/skills/anthropic-design-style'
git clone https://github.com/XiaoyeCodes/Anthropic-Design-Style.git $skillRoot
```

同名目录已存在时先比较内容，不覆盖用户修改。不同智能体的实际目录以其版本和配置为准；Skills CLI 可处理这些差异。

## 安装本地依赖

进入包含 SKILL.md 的技能根目录：

```bash
python scripts/bootstrap.py
python scripts/run.py
```

macOS / Linux 可使用 python3。要求 Python 3.10+、Node.js 22.20+（含 npm）。首次 pip/npm 安装需要联网，之后示例生成无需 API Key、模型服务或网络。

bootstrap.py 只创建技能内的 .venv 与 node_modules，不修改全局 Python 包。run.py 自动调用本地环境，即使在其他工作目录调用绝对路径也能正确解析技能资源。

## 环境检查

```bash
# Windows
.venv/Scripts/python.exe scripts/doctor.py
# macOS / Linux
.venv/bin/python scripts/doctor.py
```

doctor 检查 Python 包、Node/docx、两款随附字体中的中文字形与主题场景文件。

## 自定义内容

```bash
python scripts/run.py --input assets/example.json --out out --name 我的方案
```

参考 assets/example.json。identity.mark 与 visuals.hero 是相对输入 JSON 的 scene.json 文件；visuals.topic 必须与 title 一致。新项目先创作当前主题图形，再调整页面和图表。

生成器是六页 A4、八张 PPT 的具体示例。长文、其他文种或图表数据范围改变时，需要修改布局和坐标，不应只替换 JSON 后假定自动分页。

## 字体与 Office

PDF 嵌入字体；HTML 从相邻 assets/fonts 离线加载字体。DOCX / PPTX 使用 Editorial Serif SC 与 Editorial Sans SC 字体名称。为保持 Office 外观一致，请安装 assets/fonts/serif.ttf 与 assets/fonts/body.ttf：Windows 双击字体文件并选择安装；macOS 用字体册；Linux 放入用户字体目录并运行 fc-cache。字体各自的 OFL 许可和来源清单随文件保留。

需要校验 Word/PowerPoint 实际分页时，Windows 且已安装 Office 可运行：

```powershell
powershell -NoProfile -File scripts/render-office.ps1 -OutputDir out -Name 我的方案
```

没有 Office 时可使用 LibreOffice 或可用阅读器，记录实际检查范围。PPTX_vector-proof.pdf 是共享场景导出的矢量证明稿，不能当作 Office 导出。

## 常见问题

| 现象 | 处理 |
| --- | --- |
| node 版本过旧 | 查看 node --version 和 PATH，确保命中 Node.js 22.20+ |
| 缺少 Python 包或 docx | 在技能根目录重新执行 bootstrap.py |
| 字体丢失或中文缺字 | 保留完整 assets/fonts；生成器会报告缺字，避免静默输出方框 |
| HTML 看不到样式或下载失败 | 下载整个目录并保留相对路径，不单独保存源码页 |
| Office 换字体或页数变化 | 安装随附字体，实际导出后再检查分页 |
| 长文或图表溢出 | 按用途调整布局、字级、页数与轴范围，不缩小所有文字硬塞 |

安装行为参考：[Codex 官方技能文档](https://learn.chatgpt.com/docs/build-skills)、[Skills CLI](https://github.com/vercel-labs/skills)。
