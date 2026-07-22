# ChatGPT 管家与 Office-AI-OS 关系

## 核心定位

Office-AI-OS 的目标不是只能依赖 ChatGPT。系统要同时支持两种工作方式：

```text
有 ChatGPT 管家：ChatGPT 负责理解复杂需求、拆解任务、调用本地能力。
没有 ChatGPT 管家：Office-AI-OS 依靠本地知识库和 DeepSeek、Doubao、Kimi 等模型完成任务。
```

## 关系图

```text
用户需求
  -> ChatGPT 管家 / 桌面 App
  -> Office-AI-OS 本地核心
  -> Chief Coordinator 分配任务
  -> 文件读取 Agent / Word Agent / PPT Agent / Excel Agent
  -> Model Router 调用不同 AI 模型
  -> 统一优秀素材库与制作技巧库
  -> 生成或修改后的 Office 文件
  -> QA Agent 检查
```

## ChatGPT 管家的作用

ChatGPT 管家适合处理高级任务：

```text
理解复杂用户需求
拆解 Word / PPT / Excel 混合任务
决定先读文件、先查素材，还是先调用模型
把多个 Agent 的结果合并成最终方案
```

## 本地核心的作用

Office-AI-OS 本地核心负责真正执行：

```text
读取和生成 Office 文件
读取优秀素材库
读取制作技巧库
调用 DeepSeek、Doubao、Kimi 等模型
输出修改后文件
做基础质量检查
```

## 没有 ChatGPT 时的兜底能力

没有 ChatGPT 管家时，系统也要能运行：

```text
Chief Coordinator 负责基础任务分配
Model Router 负责选择可用模型
ProductionTechniqueLibrary 负责提供制作技巧
TechniqueLibrary 负责读取素材库建议
Word / PPT / Excel Agent 负责生成结果
QA Agent 负责检查结果
```

## 制作技巧范围

当前制作技巧重点覆盖：

```text
版面设计
文案生成
图片查找
图片生成
数据图表表达
```
