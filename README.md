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

Word Agent 现在可以生成 Markdown 文档草稿。

测试命令：

```bash
python test_word_agent.py
```

生成文件位置：

```text
outputs/word_documents/
```

## v0.3 Excel Agent

Excel Agent 现在可以生成 CSV 表格草稿。

测试命令：

```bash
python test_excel_agent.py
```

生成文件位置：

```text
outputs/excel_files/
```

## v0.3 PPT Agent

PPT Agent 现在可以生成 Markdown 演示稿大纲。

测试命令：

```bash
python test_ppt_agent.py
```

生成文件位置：

```text
outputs/ppt_outlines/
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
