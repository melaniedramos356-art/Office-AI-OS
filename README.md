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

Word Agent 现在可以生成正式 `.docx` 文档草稿。

测试命令：

```bash
python test_word_agent.py
```

生成文件位置：

```text
outputs/word_documents/
```

## v0.3 Excel Agent

Excel Agent 现在可以生成正式 `.xlsx` 表格草稿。

测试命令：

```bash
python test_excel_agent.py
```

生成文件位置：

```text
outputs/excel_files/
```

## v0.3 PPT Agent

PPT Agent 现在可以生成正式 `.pptx` 演示稿草稿。

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
```

Word / Excel / PPT Agent 会读取 `memory/generation_advice.md`，把素材库技巧和图片搜索建议写入生成文件。

## v0.5 Model Router

Model Router 是多模型调度框架，当前先使用 Mock 模型，不连接真实 API。

已预留模型供应商：

```text
DeepSeek
豆包 Doubao
Kimi
OpenAI
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

Excel Agent 已接入 Model Router。当前会优先使用 DeepSeek 生成字段建议，并写入 `.xlsx` 文件。

Excel Agent 已增加数据分析网站灵感库。生成 `.xlsx` 时会写入 Tableau Public、Power BI Data Stories、Looker Studio Gallery、Flourish Examples 等数据分析参考来源。

Excel Agent 已增加表格使用说明、数据填写规则、推荐分析图表和质量检查清单，方便把表格继续完善成数据分析看板或汇报材料。

PPT Agent 已增加目录页和 AI 结构建议页。当前在 Kimi / Doubao 未接入前，会先写入本地兜底结构建议。

Word Agent 已增加文档摘要、AI 结构建议和灵感素材查找建议。当前在 Kimi 未接入前，会先写入本地兜底结构建议。

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
