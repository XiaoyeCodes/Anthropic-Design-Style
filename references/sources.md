# 设计依据、来源与边界

克劳德设计从 huashu-editorial-docs 的暖纸、宋体、陶土强调、编辑式留白与跨格式规范发展而来。当前公开版本将原有本机实现整理为可安装的独立技能，增加跨平台字体、依赖安装、环境检查、四格式验证与公开示例。

视觉灵感包括纸张和书页的阅读感、细线插画以及 Anthropic 网站的克制表达。这里提炼设计规律，不是官方品牌指南，不使用官方 Logo。项目与 Anthropic 无隶属或背书关系。

“拾页 · AI 文档助手”是排版案例。品牌和主题插画只属于该案例；时间比较为演示假设，验证数量为建议计划，不代表产品实测或完成结果。

基础技能的思路参考：[docx](https://github.com/anthropics/skills/tree/main/skills/docx)、[theme-factory](https://github.com/anthropics/skills/tree/main/skills/theme-factory)、[canvas-design](https://github.com/anthropics/skills/tree/main/skills/canvas-design)。本仓库不复制它们，也不依赖它们才能运行。

字体来自 Google Fonts 的 Noto Serif SC / Noto Sans SC。静态衍生版保留全部字形，更名为 Editorial Serif SC / Editorial Sans SC。来源提交、SHA-256 与改动记录在 assets/fonts/manifest.json，分别保留 SIL OFL 许可。

README 编排采用 huashu-md-html 的设计师模式和阅读规范；影片由 huashu-motion 制作，配乐为该影片原创，保留制作签名。上述两个技能本身不包含在发行包中。
