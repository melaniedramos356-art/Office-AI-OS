# Office AI OS

## v0.2 命令行运行方式

运行入口：

```bash
python office_ai.py
```

测试命令：

```bash
python test_v02.py
```

## v0.3 Word Agent

Word Agent 现在可以生成正式 `.docx` 成品文档。

测试命令：

```bash
python test_word_agent.py
```

生成文件位置：

```text
outputs/word_documents/
```

## v0.3 Excel Agent

Excel Agent 现在可以生成正式 `.xlsx` 成品表格。

测试命令：

```bash
python test_excel_agent.py
```

生成文件位置：

```text
outputs/excel_files/
```

## v0.3 PPT Agent

PPT Agent 现在可以生成正式 `.pptx` 成品演示稿。

测试命令：

```bash
python test_ppt_agent.py
```

生成文件位置：

```text
outputs/ppt_files/
```

## v0.4 QA Agent

QA Agent 现在可以在生成文件后自动做基础质量检查。

检查内容：

```text
文件是否存在
文件是否为空
文件是否包含原始需求
文件类型是否在当前支持范围内
```

测试命令：

```bash
python test_qa_agent.py
```

## v0.4 Research Agent

Research Agent 现在可以生成资料搜索计划，暂时不联网搜索。

适合输入：

```text
帮我调研 AI 办公工具
帮我搜索某个行业的资料
帮我做竞品研究
```

测试命令：

```bash
python test_research_agent.py
```

生成文件位置：

```text
outputs/research_plans/
```

## v0.4 Browser Agent

Browser Agent 现在可以生成浏览器操作计划，暂时不真实控制浏览器。
操作计划会提前写出预计耗时、操作前准备、最短操作路径和异常处理规则，用来减少实际执行时间。

适合输入：

```text
帮我打开官网网页并整理关键信息
帮我打开某个网站截图
帮我下载网页上的资料
```

测试命令：

```bash
python test_browser_agent.py
```

生成文件位置：

```text
outputs/browser_plans/
```

## v0.4 Learning Agent

Learning Agent 现在可以扫描优秀素材库，并把结构、标题和关键词沉淀到 `memory`。

素材库位置：

```text
materials/
```

适合输入：

```text
请学习素材库里的优秀素材
```

测试命令：

```bash
python test_learning_agent.py
```

输出文件：

```text
memory/learned_techniques.md
memory/material_index.md
memory/generation_advice.md
memory/production_techniques.md
```

Word / Excel / PPT Agent 生成成品文件时，只写入用户可直接使用的正文、演示内容或表格数据。

素材库技巧和图片搜索建议只作为后台生成参考，不直接写入最终 Word / PPT / Excel 成品文件。

Learning Agent 也会更新 `memory/production_techniques.md`，让版面设计、文案生成、图片查找、图片生成和数据表达技巧持续迭代。

## v0.5 Model Router

Model Router 是多模型调度框架。ChatGPT App / Codex 管家先理解用户任务，再让 Model Router 按模型特点选择可用模型。

当前关系：

```text
ChatGPT App / Codex 管家：负责理解需求、拆任务、压缩上下文、决定调用哪个 Agent
Model Router：负责按任务类型和 API Key 可用情况选择模型
OpenAI API：适合 Word 文案、PPT 结构、语言润色和综合判断
DeepSeek：适合 Excel 数据逻辑、字段设计、质量检查和中文推理
本地规则：任何模型不可用时兜底，保证程序能继续生成文件
```

关系说明：

```text
ChatGPT Plus / Pro 会员：让用户在 ChatGPT App / Codex 里使用 GPT 模型和管家能力
OpenAI API Key：让 Office-AI-OS 本地程序脱离 ChatGPT App 后，也能自动调用 OpenAI 模型
```

已支持或预留模型供应商：

```text
DeepSeek
OpenAI
豆包 Doubao
Kimi
Claude
Gemini
本地模型
```

测试命令：

```bash
python test_model_router.py
```

DeepSeek 真实调用测试：

```bash
python test_deepseek_client.py
```

DeepSeek API Key 只从环境变量读取：

```text
DEEPSEEK_API_KEY
```

OpenAI API Key 只从环境变量读取：

```text
OPENAI_API_KEY
```

Word / PPT / Excel Agent 会先尝试使用当前可用模型生成 JSON 成品内容；如果模型未配置、网络失败或返回内容不合格，就自动使用本地成品规则兜底。

Excel 数据分析网站灵感库会在 Inspiration Agent 和后续分析规划中使用，不直接写入 `.xlsx` 成品表格。

Excel Agent 已增加表格使用说明、数据填写规则、推荐分析图表和质量检查清单，方便把表格继续完善成数据分析看板或汇报材料。

PPT Agent 已增加目录页。最终 PPT 只保留成品演示内容。

Word Agent 已增加文档摘要和专题报告生成能力。最终 Word 只保留成品文档内容。

## v0.5 Inspiration Library

Inspiration Library 会保存常用灵感网站入口。Research Agent、Browser Agent 和 PPT Agent 会自动读取这些网站，用于查找素材、活动视觉和制作灵感。

当前已内置：

```text
奇迹秀导航
Dribbble
Behance
Panda
Pinterest
站酷
花瓣
Sketchfab
Refero
ArtStation
BrandGuidelines
lapa
```

## v0.6 AI Butler 与通用制作技巧

AI Butler Agent 是管家规划层，负责把复杂任务拆成可执行步骤。它不替代 Word / PPT / Excel Agent，而是负责安排它们工作。

核心关系：

```text
ChatGPT / Codex 管家：理解复杂需求、拆解任务、协调模型和 Agent
Office-AI-OS 本地核心：读取知识库、调用模型、生成或修改 Office 文件
DeepSeek / Doubao / Kimi：通过 Model Router 提供不同 AI 能力
ProductionTechniqueLibrary：提供版面设计、文案生成、图片查找、图片生成技巧
Word / PPT / Excel Agent：负责具体文件生成或修改
QA Agent：负责最后质量检查
```

没有 ChatGPT 管家时，Office-AI-OS 仍然会读取本地知识库和模型路由完成任务。

测试命令：

```bash
python test_ai_butler_agent.py
```

通用制作技巧位置：

```text
memory/production_techniques.md
materials/shared/
```

## v0.6 File Reader Agent

File Reader Agent 可以读取用户提供的 `.docx`、`.pptx`、`.xlsx`、`.md`、`.txt`、`.csv` 文件，并输出内容预览和下一步处理建议。

它是后续“参考原文件进行文案修改、版面设计、图片建议和数据分析”的前置能力。

测试命令：

```bash
python test_file_reader_agent.py
```

## v0.6 File Improvement Agent

File Improvement Agent 可以读取用户提供的 Word / PPT / Excel 文件，并输出改进建议。

当前覆盖：

```text
当前内容判断
制作技巧建议
文案修改建议
版面设计建议
图片素材建议
数据图表建议
下一步执行建议
```

测试命令：

```bash
python test_file_improvement_agent.py
```

当前已支持 Word / PPT / Excel 改进版生成：

```text
请生成改进版 原文件.docx
请生成改进版 原文件.pptx
请生成改进版 原文件.xlsx
```

系统会生成新的 Office 文件，不会覆盖原文件。

## v0.7 Iteration Agent

Iteration Agent 用来管理系统持续迭代。

当前负责：

```text
生成代码迭代计划
生成制作技巧迭代计划
提醒减少重复代码
提醒把优秀制作技巧沉淀到知识库
记录下一轮优先级
```

它不会自动乱改代码，也不会覆盖用户文件。

测试命令：

```bash
python test_iteration_agent.py
```

经验库位置：

```text
memory/experience_library.md
```

经验库分为两大块：

```text
程序迭代经验：代码合理性、安全性、简洁性、测试和架构经验
制作技巧与素材查找经验：版面设计、文案生成、图片查找、图片生成、优秀作品网站查找经验
```

## v0.7 China Inspiration Library

China Inspiration Library 用来保存中国素材与灵感来源，补充更适合中文办公、中文海报、中文 PPT 和国内活动视觉的参考。

当前已内置：

```text
站酷
花瓣
优设网
阿里巴巴矢量图标库
即时设计资源广场
稿定设计
图怪兽
Canva 可画
```

素材目录：

```text
materials/china/
```

测试命令：

```bash
python test_china_inspiration_library.py
```

## v0.8 Inspiration Agent

Inspiration Agent 用来生成素材灵感计划，自动融合国际灵感库、中国素材库、数据分析网站灵感库和通用制作技巧库。

适合输入：

```text
帮我找 PPT 优秀作品和素材网站
帮我找 Word 报告版面灵感
帮我找 Excel 数据分析看板参考
```

测试命令：

```bash
python test_inspiration_agent.py
```

生成文件位置：

```text
outputs/inspiration_plans/
```

## v0.9 Office Panel Agent

Office Panel Agent 是后续桌面 App 办公首页的后端雏形，用来输出办公功能卡片、按钮建议和每个按钮对应的命令。

它会同时生成：

```text
office_panel_*.md：给人看的办公板块说明
office_panel_*.json：给桌面 App 读取的结构化数据
```

当前办公板块包含：

```text
Word 文档生成
PPT 演示生成
Excel 表格生成
已有文件改进
素材灵感计划
质量检查
```

适合输入：

```text
请完善办公板块，准备做桌面 App 交互页面
显示办公首页功能
整理三大办公功能
```

测试命令：

```bash
python test_office_panel_agent.py
```

生成文件位置：

```text
outputs/office_panels/
```

## v0.10 Desktop App

Desktop App 是最小桌面交互页面，当前使用 Python 自带的 Tkinter，不需要额外安装界面框架。

启动方式一：

```bash
python desktop_app.py
```

启动方式二：

```text
双击 start_desktop_app.bat
```

当前界面支持：

```text
新建 Word
新建 PPT
新建 Excel
改进文件
找素材
查看结果
```

测试命令：

```bash
python test_desktop_app.py
```

## v0.11 Desktop Shortcut

现在可以创建桌面图标。当前先创建 Windows 桌面快捷方式，后续再升级为带自定义 `.ico` 图标和安装包的版本。

创建方式：

```text
双击 create_desktop_shortcut.bat
```

创建后，桌面会出现：

```text
Office-AI-OS
```

测试命令：

```bash
python test_desktop_shortcut.py
```
