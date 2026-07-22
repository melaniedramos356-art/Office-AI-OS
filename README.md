# Office-AI-OS

Office-AI-OS 当前采用“ChatGPT App 制作模式”。本地程序不再用固定模板直接生成低质量 Word、PPT、Excel；它负责将需求整理为创作任务单，由 ChatGPT App / Codex 完成网页检索、案例参考、素材筛选、排版、动画和最终文件制作。

## 使用方式

1. 双击 `start_desktop_app.bat` 打开桌面程序。
2. 选择“新建 Word / PPT / Excel”，输入主题和要求，点击“执行”。
3. 点击“打开任务单”。
4. 将任务单上传到 ChatGPT App / Codex；如有参考文件，也一并上传。
5. ChatGPT App 按任务单生成最终 `.docx`、`.pptx` 或 `.xlsx` 成品。

## 本地 Agent 的职责

- Word Agent：生成 Word 创作任务单。
- PPT Agent：生成 PPT 创作任务单，包含图文、版式和动画要求。
- Excel Agent：生成 Excel 创作任务单，包含数据口径、公式和分析要求。
- File Improvement Agent：为已有文件生成改进任务单。
- Reference Imitation Agent：为参考文件生成仿写任务单。

任务单统一保存在：

```text
outputs/creation_briefs/
```

## 重要说明

ChatGPT 会员用于在 ChatGPT App / Codex 中完成制作；它不能被本地桌面程序直接作为接口调用。未来若要实现“桌面程序一键自动生成最终文件”，需要单独配置 OpenAI API。

## 简易测试

```bash
python test_v02.py
python test_word_agent.py
python test_ppt_agent.py
python test_excel_agent.py
python test_file_improvement_agent.py
python test_reference_imitation_agent.py
python test_desktop_app.py
```
